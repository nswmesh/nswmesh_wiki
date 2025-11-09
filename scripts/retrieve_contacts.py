#!/home/craigp/.venv/meshcore-py/bin/python3
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
from typing import Dict, Any, List, Tuple, Set
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

CSV_COLS = ["Name", "Public Key", "Antenna Height Above Ground (m)"]
CSV_HEADER_ALIASES = {
    "name": "Name",
    "public key": "Public Key",
    "height above ground": "Antenna Height Above Ground (m)",
    "antenna height above ground (m)": "Antenna Height Above Ground (m)",
}

# -------------------- Utilities --------------------

def reorder_contact_keys(contact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a copy of the contact with keys ordered consistently:
    name, last_advert, last_seen, latitude, longitude, advert_location,
    internet_location, public_key. Only includes keys that exist, in that order.
    Any additional keys are appended afterwards.
    """
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
        "public_key",
    ]

    ordered = {k: contact[k] for k in key_order if k in contact}
    for k, v in contact.items():
        if k not in ordered:
            ordered[k] = v
    return ordered

# -------------------- Serial contacts --------------------

async def get_contacts(port: str, baudrate: int) -> Dict[str, Any]:
    """
    Connect via serial and fetch the mesh contacts payload.
    """
    con = SerialConnection(port, baudrate)
    await con.connect()
    await asyncio.sleep(0.1)
    mc = MeshCore(con)
    await mc.connect()

    result = await mc.commands.get_contacts()
    if result.type == EventType.ERROR:
        raise RuntimeError(f"Error getting contacts: {result.payload}")
    return result.payload


def normalize_contact(entry: Dict[str, Any], keep_location: bool) -> Tuple[str, Dict[str, Any]]:
    """
    Convert a raw entry to our normalized contact dict.
    Returns (public_key, contact_dict). Skips invalid records.
    """
    pubkey = (entry.get("public_key") or "").strip()
    name = (entry.get("adv_name") or "").strip()
    last_advert = entry.get("last_advert")

    if not pubkey or not isinstance(last_advert, (int, float)):
        return "", {}

    last_seen = datetime.fromtimestamp(int(last_advert), tz=LOCAL_TZ).isoformat(timespec="seconds")

    contact: Dict[str, Any] = {
        "name": name,
        "last_advert": int(last_advert),
        "last_seen": last_seen,
    }

    # Advert location flag is independent of whether we keep the coordinates.
    lat = float(entry.get("adv_lat", 0.0))
    lon = float(entry.get("adv_lon", 0.0))
    if (lat, lon) != (0.0, 0.0):
        contact["advert_location"] = True
        if keep_location:
            contact["latitude"] = lat
            contact["longitude"] = lon
    elif keep_location:
        # If --keep-location is requested, include zeros explicitly
        contact["latitude"] = lat
        contact["longitude"] = lon

    # public_key stored; final order enforced later
    contact["public_key"] = pubkey
    return pubkey, contact


def recompute_last_seen(contact: Dict[str, Any]) -> None:
    """
    Refresh last_seen from last_advert using Australia/Sydney timezone.
    """
    la = contact.get("last_advert")
    if isinstance(la, (int, float)):
        contact["last_seen"] = datetime.fromtimestamp(int(la), tz=LOCAL_TZ).isoformat(timespec="seconds")


def transform_type2_contacts(
    data: Dict[str, Any],
    days: int,
    keep_location: bool
) -> Dict[str, Any]:
    """
    Build a dict of Type-2 contacts (keyed by public_key) from the raw payload,
    filtered to those seen within 'days' days.
    """
    cutoff = time.time() - (days * 86400)
    items: List[Tuple[str, Dict[str, Any]]] = []

    for entry in data.values():
        if entry.get("type") != 2:
            continue
        last_advert = entry.get("last_advert")
        if not isinstance(last_advert, (int, float)) or last_advert < cutoff:
            continue

        pubkey, contact = normalize_contact(entry, keep_location)
        if pubkey:
            items.append((pubkey, contact))

    # Sort output by first octet (first two hex chars of key), then by name
    items.sort(key=lambda kv: (kv[0][:2].upper(), kv[1].get("name", "").lower()))
    return {pk: reorder_contact_keys(c) for pk, c in items}

# -------------------- Merge logic --------------------

def merge_with_previous(previous: Dict[str, Any], current: Dict[str, Any], keep_location: bool) -> Dict[str, Any]:
    """
    Merge current serial-derived contacts into previous output:
      - Replace entry if current.last_advert is newer or previous missing/invalid
      - Otherwise keep previous; fill missing optional fields where sensible
      - Recompute last_seen in all entries
    """
    merged = dict(previous) if previous else {}

    for pk, cur in current.items():
        prev = merged.get(pk)
        if prev is None:
            merged[pk] = cur
            continue

        prev_la = prev.get("last_advert")
        cur_la = cur.get("last_advert")

        if not isinstance(prev_la, (int, float)) or (isinstance(cur_la, (int, float)) and cur_la > prev_la):
            merged[pk] = cur
        else:
            # carry optional flags if they newly appeared in current
            if "advert_location" not in prev and "advert_location" in cur:
                prev["advert_location"] = cur["advert_location"]
            if keep_location:
                if "latitude" not in prev and "latitude" in cur:
                    prev["latitude"] = cur["latitude"]
                if "longitude" not in prev and "longitude" in cur:
                    prev["longitude"] = cur["longitude"]

    # Recompute times
    for c in merged.values():
        recompute_last_seen(c)

    # Sort and enforce final key order
    ordered = dict(sorted(merged.items(), key=lambda kv: (kv[0][:2].upper(), kv[1].get("name", "").lower())))
    return {pk: reorder_contact_keys(c) for pk, c in ordered.items()}

# -------------------- Nodes (internet_location) --------------------

def fetch_node_pubkeys(nodes_url: str, timeout: int = 15) -> Set[str]:
    """
    Strictly download the nodes JSON and return a set of public_key strings (lowercased)
    found anywhere in the structure. Exit on failure or empty result.
    """
    try:
        ctx = ssl.create_default_context()
        req = Request(nodes_url, headers={"User-Agent": "meshcore-contact-sync/1.0"})
        with urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read()
        data = json.loads(body.decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"ERROR: Failed to download node file from {nodes_url}: {e}", file=sys.stderr)
        sys.exit(1)

    keys: Set[str] = set()

    def walk(obj: Any):
        if isinstance(obj, dict):
            pk = obj.get("public_key") or obj.get("PublicKey") or obj.get("pubkey")
            if isinstance(pk, str) and pk.strip():
                keys.add(pk.strip().lower())
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(data)

    if not keys:
        print(f"ERROR: No public_key entries found in nodes file {nodes_url}", file=sys.stderr)
        sys.exit(1)

    print(f"Downloaded nodes: found {len(keys)} distinct public_key entries.")
    return keys


def apply_internet_location_flags(contacts: Dict[str, Any], node_keys: Set[str]) -> int:
    """
    Set 'internet_location': True for any merged contact whose key exists in node_keys.
    Returns the number of contacts flagged.
    """
    count = 0
    for pk, entry in contacts.items():
        if pk.strip().lower() in node_keys:
            if not entry.get("internet_location"):
                entry["internet_location"] = True
            count += 1
    return count

# -------------------- HAG CSV --------------------

def _read_hag_csv(path: str) -> Dict[str, Dict[str, str]]:
    """
    Read HAG CSV into dict keyed by Public Key.
    Tolerates prior header variants via CSV_HEADER_ALIASES.
    """
    records: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(path):
        return records

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return records

        header_map = {h: CSV_HEADER_ALIASES.get(h.strip().lower(), h) for h in reader.fieldnames}

        def get(row: Dict[str, str], canonical: str, default: str = "") -> str:
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
            }

    return records


def _write_hag_csv(path: str, rows: List[Dict[str, str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS)
        writer.writeheader()
        writer.writerows(rows)


def ensure_hag_csv(csv_path: str, contacts: Dict[str, Any]) -> None:
    """
    Ensure the HAG CSV exists and includes a row for each contact.
    Update names to latest; keep existing height values; sort by first octet then name.
    """
    existing = _read_hag_csv(csv_path)

    for pk, contact in contacts.items():
        name = contact.get("name", "")
        if pk not in existing:
            existing[pk] = {"Name": name, "Public Key": pk, "Antenna Height Above Ground (m)": ""}
        else:
            existing[pk]["Name"] = name

    rows = list(existing.values())
    rows.sort(key=lambda r: (r["Public Key"][:2].upper(), (r["Name"] or "").lower()))
    _write_hag_csv(csv_path, rows)

# -------------------- Main --------------------

async def main():
    parser = argparse.ArgumentParser(
        description="Retrieve mesh contacts, merge with previous, flag internet_location from nodes, and maintain HAG CSV."
    )
    parser.add_argument("--port", default=DEFAULT_PORT, help=f"Serial port (default: {DEFAULT_PORT})")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD, help=f"Baud rate (default: {DEFAULT_BAUD})")
    parser.add_argument("--days", type=int, default=7, help="Include entries seen within N days (default: 7)")
    parser.add_argument("--keep-location", action="store_true", help="Include latitude/longitude fields in output")
    parser.add_argument("--output", default="type2_contacts.json", help="Output JSON file")
    parser.add_argument("--previous", help="Previous output JSON to merge into (optional)")
    parser.add_argument("--also-dump-raw", metavar="RAW.json", help="Also dump the full raw contacts payload (optional)")
    parser.add_argument("--hag-csv", required=True, help="Path to Antenna Height CSV")
    parser.add_argument("--nodes-url", default=DEFAULT_NODES_URL, help="Nodes API URL (must be reachable)")

    args = parser.parse_args()

    # 1) Strictly download nodes and accumulate public keys
    node_keys = fetch_node_pubkeys(args.nodes_url)

    # 2) Retrieve live serial contacts
    payload = await get_contacts(args.port, args.baud)
    if args.also_dump_raw:
        with open(args.also_dump_raw, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    current = transform_type2_contacts(payload, days=args.days, keep_location=args.keep_location)

    # 3) Load previous (if provided)
    previous: Dict[str, Any] = {}
    if args.previous:
        try:
            with open(args.previous, "r", encoding="utf-8") as f:
                previous = json.load(f)
                if not isinstance(previous, dict):
                    print(f"Warning: previous file {args.previous} is not a dict; ignoring.", file=sys.stderr)
                    previous = {}
        except FileNotFoundError:
            print(f"Note: previous file {args.previous} not found; starting fresh.")
        except json.JSONDecodeError:
            print(f"Warning: previous file {args.previous} could not be parsed; ignoring.", file=sys.stderr)

    # 4) Merge previous + current
    final_out = merge_with_previous(previous, current, keep_location=args.keep_location)

    # 5) Apply internet_location to ALL merged entries (keys from previous ∪ current)
    matched = apply_internet_location_flags(final_out, node_keys)
    print(f"Applied internet_location=True to {matched} contact(s) based on nodes list.")

    # 6) Ensure HAG CSV exists/is updated and sorted
    ensure_hag_csv(args.hag_csv, final_out)

    # 7) Save JSON with enforced key order
    final_out = {pk: reorder_contact_keys(c) for pk, c in final_out.items()}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final_out, f, indent=4, ensure_ascii=False)

    print(f"Processed {len(final_out)} contact(s).")
    print(f"Wrote JSON: {args.output}")
    print(f"Updated HAG CSV: {args.hag_csv}")
    if args.also_dump_raw:
        print(f"Wrote raw payload: {args.also_dump_raw}")


if __name__ == "__main__":
    asyncio.run(main())
