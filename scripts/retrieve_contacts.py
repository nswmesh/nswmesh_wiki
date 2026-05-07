#! /usr/bin/env python
import asyncio
import json
import argparse
import time
import os
import csv
import ssl
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, List, Tuple, Set, Iterable
from urllib.request import urlopen, Request

# External lib
from meshcore import MeshCore
from meshcore import SerialConnection
from meshcore import EventType

# -------------------- Config --------------------

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD = 115200
LOCAL_TZ = ZoneInfo("Australia/Sydney")
DEFAULT_NODES_URL = "https://map.meshcore.dev/api/v1/nodes"

CSV_COLS = ["Name", "Public Key", "Antenna Height Above Ground (m)", "Status"]
CSV_HEADER_ALIASES = {
    "name": "Name",
    "public key": "Public Key",
    "height above ground": "Antenna Height Above Ground (m)",
    "antenna height above ground (m)": "Antenna Height Above Ground (m)",
    "status": "Status",   # accept lowercase in existing CSVs
    "Status": "Status",
}

# -------------------- Utilities --------------------

def reorder_contact_keys(contact: Dict[str, Any]) -> Dict[str, Any]:
    """Return contact with keys ordered consistently."""
    if not isinstance(contact, dict):
        return contact
    key_order = [
        "name",
        "last_advert",
        "last_seen",
        "latitude",
        "longitude",
        "advert_location",
        "internet_location",
        "status",
        "public_key",
    ]
    ordered = {k: contact[k] for k in key_order if k in contact}
    for k, v in contact.items():
        if k not in ordered:
            ordered[k] = v
    return ordered


def _first_octet(pk: str) -> str:
    return (pk or "")[:2].upper()

# -------------------- Input sources --------------------

async def get_contacts_from_serial(port: str, baudrate: int) -> Dict[str, Any]:
    con = SerialConnection(port, baudrate)
    await con.connect()
    await asyncio.sleep(0.1)
    mc = MeshCore(con)
    await mc.connect()
    result = await mc.commands.get_contacts()
    if result.type == EventType.ERROR:
        raise RuntimeError(f"Error getting contacts: {result.payload}")
    return result.payload


def get_contacts_from_file(path: str) -> Any:
    if not os.path.exists(path):
        print(f"ERROR: contacts file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: failed to read contacts file {path}: {e}", file=sys.stderr)
        sys.exit(1)
    return data


def _iter_entries(payload: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(payload, dict):
        if "contacts" in payload and isinstance(payload["contacts"], list):
            yield from (i for i in payload["contacts"] if isinstance(i, dict))
        else:
            yield from (v for v in payload.values() if isinstance(v, dict))
    elif isinstance(payload, list):
        yield from (i for i in payload if isinstance(i, dict))

# -------------------- Normalization --------------------

def normalize_contact(entry: Dict[str, Any], keep_location: bool) -> Tuple[str, Dict[str, Any]]:
    pubkey = (entry.get("public_key") or "").strip()
    # Name field can vary across sources
    name = (entry.get("name") or entry.get("adv_name") or entry.get("Name") or "").strip()
    last_advert = entry.get("last_advert")
    if not pubkey or not isinstance(last_advert, (int, float)):
        return "", {}

    last_seen = datetime.fromtimestamp(int(last_advert), tz=LOCAL_TZ).isoformat(timespec="seconds")
    contact: Dict[str, Any] = {
        "name": name,
        "last_advert": int(last_advert),
        "last_seen": last_seen,
    }

    # Location handling
    lat = float(entry.get("adv_lat", entry.get("latitude", 0.0)))
    lon = float(entry.get("adv_lon", entry.get("longitude", 0.0)))
    if (lat, lon) != (0.0, 0.0):
        contact["advert_location"] = True
        if keep_location:
            contact["latitude"] = lat
            contact["longitude"] = lon
    elif keep_location:
        contact["latitude"] = lat
        contact["longitude"] = lon

    contact["public_key"] = pubkey
    return pubkey, contact


def recompute_last_seen(contact: Dict[str, Any]) -> None:
    la = contact.get("last_advert")
    if isinstance(la, (int, float)):
        contact["last_seen"] = datetime.fromtimestamp(int(la), tz=LOCAL_TZ).isoformat(timespec="seconds")

# -------------------- Transform --------------------

def transform_type2_contacts_from_payloads(payloads: List[Any], days: int, keep_location: bool) -> Dict[str, Any]:
    cutoff = time.time() - (days * 86400)
    best: Dict[str, Dict[str, Any]] = {}
    best_la: Dict[str, int] = {}

    for payload in payloads:
        for entry in _iter_entries(payload):
            if entry.get("type") != 2:
                continue
            la = entry.get("last_advert")
            if not isinstance(la, (int, float)) or la < cutoff:
                continue

            pk, contact = normalize_contact(entry, keep_location)
            if not pk:
                continue

            prev_la = best_la.get(pk)
            if prev_la is None or contact["last_advert"] > prev_la:
                best[pk] = contact
                best_la[pk] = contact["last_advert"]

    items = sorted(best.items(), key=lambda kv: (_first_octet(kv[0]), kv[1].get("name", "").lower()))
    return {pk: reorder_contact_keys(c) for pk, c in items}

# -------------------- Merge --------------------

def merge_with_previous(previous: Dict[str, Any], current: Dict[str, Any], keep_location: bool) -> Dict[str, Any]:
    merged = dict(previous) if previous else {}

    for pk, cur in current.items():
        prev = merged.get(pk)
        if prev is None:
            merged[pk] = cur
            continue

        prev_la, cur_la = prev.get("last_advert"), cur.get("last_advert")
        if not isinstance(prev_la, (int, float)) or (isinstance(cur_la, (int, float)) and cur_la > prev_la):
            merged[pk] = cur
        else:
            if "advert_location" not in prev and "advert_location" in cur:
                prev["advert_location"] = cur["advert_location"]
            if keep_location:
                if "latitude" not in prev and "latitude" in cur:
                    prev["latitude"] = cur["latitude"]
                if "longitude" not in prev and "longitude" in cur:
                    prev["longitude"] = cur["longitude"]
            if not prev.get("name") and cur.get("name"):
                prev["name"] = cur["name"]

    for c in merged.values():
        recompute_last_seen(c)

    ordered = dict(sorted(merged.items(), key=lambda kv: (_first_octet(kv[0]), kv[1].get("name", "").lower())))
    return {pk: reorder_contact_keys(c) for pk, c in ordered.items()}

# -------------------- Nodes --------------------

def fetch_node_pubkeys(nodes_url: str, timeout: int = 15) -> Set[str]:
    try:
        ctx = ssl.create_default_context()
        req = Request(nodes_url, headers={"User-Agent": "meshcore-contact-sync/1.0"})
        with urlopen(req, timeout=timeout, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"ERROR: Failed to download node file from {nodes_url}: {e}", file=sys.stderr)
        sys.exit(1)

    keys: Set[str] = set()

    def walk(o):
        if isinstance(o, dict):
            pk = o.get("public_key") or o.get("PublicKey") or o.get("pubkey")
            if isinstance(pk, str) and pk.strip():
                keys.add(pk.strip().lower())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    if not keys:
        print(f"ERROR: No public_key entries found in nodes file {nodes_url}", file=sys.stderr)
        sys.exit(1)
    print(f"Downloaded nodes: found {len(keys)} distinct public_key entries.")
    return keys


def apply_internet_location_flags(contacts: Dict[str, Any], node_keys: Set[str]) -> int:
    count = 0
    for pk, entry in contacts.items():
        if pk.strip().lower() in node_keys:
            entry["internet_location"] = True
            count += 1
    return count

# -------------------- CSV Sync --------------------

def _read_hag_csv(path: str) -> Dict[str, Dict[str, str]]:
    records: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(path):
        return records
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return records
        header_map = {h: CSV_HEADER_ALIASES.get(h.strip().lower(), h) for h in reader.fieldnames}

        def get(row, canonical, default=""):
            for orig, canon in header_map.items():
                if canon == canonical:
                    return (row.get(orig) or "").strip()
            return default

        for row in reader:
            pk = get(row, "Public Key")
            if not pk:
                continue
            records[pk] = {
                "Name": get(row, "Name"),
                "Public Key": pk,
                "Antenna Height Above Ground (m)": get(row, "Antenna Height Above Ground (m)"),
                "Status": (get(row, "Status") or "").strip(),
            }
    return records


def _write_hag_csv(path: str, rows: List[Dict[str, str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS)
        writer.writeheader()
        writer.writerows(rows)


def _sync_contacts_with_csv(contacts: Dict[str, Any], csv_path: str) -> None:
    """
    Sync CSV 'Status' and 'Name' with JSON:
      - CSV rows not in JSON: add if Status != 'delete' (status 'park'/'parked' -> 'parked'; else 'active'), using CSV Name.
      - CSV rows with Status 'delete': remove from JSON.
      - CSV rows with Status 'park' or 'parked': set JSON status to 'parked'.
      - Otherwise: set JSON status to 'active'.
      - If JSON name missing/empty, backfill from CSV Name.
      - Rewrites CSV sorted by first octet then Name, preserving existing heights and Status if JSON lacks them.
    """
    csv_records = _read_hag_csv(csv_path)

    # 1) Add rows present in CSV but not in JSON
    for pk, row in csv_records.items():
        status_raw = (row.get("Status") or "").strip().lower()
        if pk not in contacts:
            if status_raw == "delete":
                continue
            name = row.get("Name", "")
            status = "parked" if status_raw in ("park", "parked") else "active"
            entry = {
                "name": name,
                "status": status,
                "public_key": pk,
            }
            contacts[pk] = reorder_contact_keys(entry)

    # 2) Apply Status effects and backfill names from CSV for contacts already in JSON
    to_delete: List[str] = []
    for pk, entry in contacts.items():
        status_raw = (csv_records.get(pk, {}).get("Status") or "").strip().lower()

        if status_raw == "delete":
            to_delete.append(pk)
            continue
        elif status_raw in ("park", "parked"):
            entry["status"] = "parked"
        else:
            entry["status"] = "active"

        # Backfill name from CSV if missing/empty in JSON
        if not entry.get("name"):
            csv_name = (csv_records.get(pk, {}).get("Name") or "").strip()
            if csv_name:
                entry["name"] = csv_name

        contacts[pk] = reorder_contact_keys(entry)

    for pk in to_delete:
        contacts.pop(pk, None)

    # 3) Rewrite CSV: include all contacts + keep existing rows; prefer JSON name when non-empty
    rows_by_pk = dict(csv_records)
    for pk, entry in contacts.items():
        existing = rows_by_pk.get(pk, {})
        name_for_csv = (entry.get("name") or "").strip() or existing.get("Name", "")
        rows_by_pk[pk] = {
            "Name": name_for_csv,
            "Public Key": pk,
            "Antenna Height Above Ground (m)": existing.get("Antenna Height Above Ground (m)", ""),
            "Status": existing.get("Status", entry.get("status", "")),  # write JSON->CSV mapping directly
        }

    rows = list(rows_by_pk.values())
    rows.sort(key=lambda r: ((r.get("Public Key") or "")[:2].upper(), (r.get("Name") or "").lower()))
    _write_hag_csv(csv_path, rows)

# -------------------- Main --------------------

async def main():
    parser = argparse.ArgumentParser(
        description="Retrieve mesh contacts (contacts file overrides serial; optional combine), merge with previous, flag internet_location from nodes, and maintain HAG CSV."
    )
    parser.add_argument("--port", default=DEFAULT_PORT)
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--keep-location", action="store_true")
    parser.add_argument("--output", default="type2_contacts.json")
    parser.add_argument("--previous")
    parser.add_argument("--also-dump-raw")
    parser.add_argument("--hag-csv", required=True)
    parser.add_argument("--nodes-url", default=DEFAULT_NODES_URL)
    parser.add_argument("--contacts-file")
    parser.add_argument("--combine-sources", action="store_true")

    args = parser.parse_args()
    node_keys = fetch_node_pubkeys(args.nodes_url)

    # Build current from sources
    payloads: List[Any] = []
    if args.contacts_file:
        file_payload = get_contacts_from_file(args.contacts_file)
        if args.combine_sources:
            try:
                serial_payload = await get_contacts_from_serial(args.port, args.baud)
            except Exception as e:
                print(f"Warning: could not read serial while combining sources: {e}")
                serial_payload = None
            payloads = [p for p in [file_payload, serial_payload] if p]
        else:
            payloads = [file_payload]
    else:
        serial_payload = await get_contacts_from_serial(args.port, args.baud)
        payloads = [serial_payload]

    if args.also_dump_raw and payloads:
        with open(args.also_dump_raw, "w", encoding="utf-8") as f:
            json.dump(payloads[0], f, indent=2, ensure_ascii=False)

    current = transform_type2_contacts_from_payloads(payloads, days=args.days, keep_location=args.keep_location)

    previous = {}
    if args.previous and os.path.exists(args.previous):
        try:
            with open(args.previous, "r", encoding="utf-8") as f:
                previous = json.load(f)
        except Exception:
            previous = {}

    final_out = merge_with_previous(previous, current, keep_location=args.keep_location)
    matched = apply_internet_location_flags(final_out, node_keys)
    print(f"Applied internet_location=True to {matched} contact(s) based on nodes list.")

    # CSV sync (Status mapping, name backfill)
    _sync_contacts_with_csv(final_out, args.hag_csv)

    # Enforce key order and write JSON sorted by first octet then name
    sorted_items = sorted(
        final_out.items(),
        key=lambda kv: (_first_octet(kv[0]), kv[1].get("name", "").lower())
    )
    final_out_sorted = {pk: reorder_contact_keys(c) for pk, c in sorted_items}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final_out_sorted, f, indent=4, ensure_ascii=False, sort_keys=False)

    print(f"Processed {len(final_out_sorted)} contact(s). Wrote JSON: {args.output}")
    print(f"Synchronized CSV: {args.hag_csv}")


if __name__ == "__main__":
    asyncio.run(main())
