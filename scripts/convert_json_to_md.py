#!/usr/bin/env python3
import json
import argparse
import sys
import textwrap
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional


def first_byte_prefix(public_key: str) -> str:
    """Return the first byte (two hex chars) in uppercase."""
    if not public_key or len(public_key) < 2:
        return ""
    return public_key[:2].upper()


def is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def wrap_hex(h: str, width: int) -> str:
    """Optionally wrap a hex string to multiple lines."""
    if width <= 0:
        return h
    return "\n".join(textwrap.wrap(h, width=width))


def sanitize_name(raw: str) -> str:
    """
    Make the repeater name safe for markdown table output.
    Only rule: replace '|' with '/'.
    """
    if raw is None:
        raw = ""
    return raw.replace("|", "/")


def tick_or_blank(value: Any) -> str:
    """For advert_location / internet_location: True -> '✔', else ''."""
    return "✔" if value is True else ""


def status_icon(status_val: Any) -> str:
    """
    First-column icon:
    - if status == 'parked' (case-insensitive) -> red 'X' via HTML
    - otherwise (including missing) -> '✔'
    """
    try:
        if isinstance(status_val, str) and status_val.strip().lower() == "parked":
            # Red X using inline HTML; falls back to 'X' if styles are stripped.
            return "<span style='color:red'>X</span>"
    except Exception:
        pass
    return "✔"


def load_height_map(csv_path: Optional[str]) -> Dict[str, str]:
    """
    Load optional height CSV mapping public_key -> height_m.
    Tolerates header variations by normalizing them.

    Expected headers (case/space/BOM tolerant):
      - 'Public Key'
      - 'Antenna Height Above Ground (m)'
    """
    height_map: Dict[str, str] = {}

    if not csv_path:
        return height_map

    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)

            def norm(s: str) -> str:
                return (
                    s.strip()
                     .lstrip("\ufeff")  # handle BOM
                     .lower()
                     .replace(" ", "")
                )

            header_map = {norm(h): h for h in (reader.fieldnames or [])}

            public_key_header = None
            for candidate in ["publickey"]:
                if candidate in header_map:
                    public_key_header = header_map[candidate]
                    break

            height_header = None
            for candidate in [
                "antennaheightaboveground(m)",
                "antennaheightaboveground",
                "heightaboveground",
            ]:
                if candidate in header_map:
                    height_header = header_map[candidate]
                    break

            if public_key_header is None:
                print(
                    "Warning: couldn't find 'Public Key' column in height CSV headers:",
                    reader.fieldnames,
                    file=sys.stderr,
                )
                return height_map

            if height_header is None:
                print(
                    "Warning: couldn't find 'Antenna Height Above Ground (m)' column in height CSV headers:",
                    reader.fieldnames,
                    file=sys.stderr,
                )

            for row in reader:
                pub_raw = (
                    (row.get(public_key_header) or "")
                    .strip().replace(" ", "").replace("\n", "")
                )
                if not pub_raw:
                    continue
                height_raw = (row.get(height_header) or "").strip() if height_header else ""
                height_map[pub_raw] = height_raw

    except FileNotFoundError:
        print(f"Warning: height CSV '{csv_path}' not found, continuing without heights", file=sys.stderr)
    except Exception as e:
        print(f"Warning: could not read height CSV '{csv_path}': {e}", file=sys.stderr)

    return height_map


def _rows_from_list(items: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Handle list format and normalize fields."""
    rows = []
    for i, item in enumerate(items, 1):
        name = (item.get("name") or "").strip()
        pub = (item.get("public_key") or "").strip().replace(" ", "").replace("\n", "")
        if not name or not pub:
            print(f"Warning: skipping item {i} (missing name or public_key)", file=sys.stderr)
            continue
        if not is_hex(pub):
            print(f"Warning: item {i} public_key is not valid hex; emitting anyway", file=sys.stderr)

        prefix = (item.get("public_key_prefix") or first_byte_prefix(pub)).upper()
        rows.append({
            "public_key_prefix": prefix,
            "name": name,
            "public_key": pub,
            "last_seen": (item.get("last_seen") or "").strip(),
            "advert_location": item.get("advert_location"),
            "internet_location": item.get("internet_location"),
            "status": item.get("status"),
            "height_m": "",
        })
    return rows


def _rows_from_dict(obj: Dict[str, Any]) -> List[Dict[str, str]]:
    """Handle dict keyed by public_key and normalize fields."""
    rows = []
    for i, (key_pub, info) in enumerate(obj.items(), 1):
        if isinstance(info, dict):
            raw_pub_in_obj = info.get("public_key") or key_pub
        else:
            raw_pub_in_obj = key_pub
        pub = str(raw_pub_in_obj).strip().replace(" ", "").replace("\n", "")

        name = ""
        last_seen = ""
        prefix = ""
        advert_location = None
        internet_location = None
        status_val = None

        if isinstance(info, dict):
            name = (info.get("name") or "").strip()
            last_seen = (info.get("last_seen") or "").strip()
            advert_location = info.get("advert_location")
            internet_location = info.get("internet_location")
            status_val = info.get("status")
            if "public_key_prefix" in info:
                prefix = str(info["public_key_prefix"]).strip().upper()

        if not prefix:
            prefix = first_byte_prefix(pub).upper()
        if not name or not pub:
            print(f"Warning: skipping entry {i} (missing name or public_key)", file=sys.stderr)
            continue
        if not is_hex(pub):
            print(f"Warning: entry {i} public_key is not valid hex; emitting anyway", file=sys.stderr)

        rows.append({
            "public_key_prefix": prefix,
            "name": name,
            "public_key": pub,
            "last_seen": last_seen,
            "advert_location": advert_location,
            "internet_location": internet_location,
            "status": status_val,
            "height_m": "",
        })
    return rows


def load_rows(path: str) -> List[Dict[str, str]]:
    """Load entries from JSON (list or dict keyed by public_key)."""
    with open(path, "r") as f:
        data = json.load(f)
    if isinstance(data, list):
        return _rows_from_list(data)
    if isinstance(data, dict):
        return _rows_from_dict(data)
    raise ValueError("Data JSON must be a list or an object keyed by public_key.")


def apply_heights(rows: List[Dict[str, str]], height_map: Dict[str, str]) -> None:
    """Apply CSV heights to rows in-place."""
    for r in rows:
        pub = r["public_key"]
        if pub in height_map:
            r["height_m"] = height_map[pub]


def load_meta(path: str) -> Dict[str, str]:
    """Load metadata with title and preamble."""
    with open(path, "r") as f:
        meta = json.load(f)
    title = (meta.get("title") or "").strip()
    preamble = (meta.get("preamble") or "").strip()
    if not title:
        raise ValueError("Meta JSON must include a non-empty 'title'.")
    if not preamble:
        raise ValueError("Meta JSON must include a non-empty 'preamble'.")
    return {"title": title, "preamble": preamble}


def format_as_of(date_str: str | None) -> str:
    """Return date formatted as '19 October 2025'."""
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str)
        except ValueError:
            return date_str
    else:
        dt = datetime.now()
    day = str(int(dt.strftime("%d")))
    return f"{day} {dt.strftime('%B %Y')}"


def table_markdown(rows: List[Dict[str, str]], wrap: int) -> str:
    """
    Build the Markdown table.

    Columns (status first):
      status | public_key_prefix | name | public_key | last_seen | advert_location | internet_location | antenna height above ground (m)
    """
    header = (
        "| status | public_key_prefix | name | public_key | last_seen | advert_location | internet_location | antenna height above ground (m) |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    body_lines = []
    for r in rows:
        icon = status_icon(r.get("status"))
        safe_name = sanitize_name(r["name"])
        pubkey_cell = wrap_hex(r["public_key"], wrap)
        last_seen_cell = r.get("last_seen", "")
        advert_cell = tick_or_blank(r.get("advert_location"))
        internet_cell = tick_or_blank(r.get("internet_location"))
        height_cell = r.get("height_m", "")
        body_lines.append(
            f"| {icon} | {r['public_key_prefix']} | {safe_name} | {pubkey_cell} | {last_seen_cell} | {advert_cell} | {internet_cell} | {height_cell} |"
        )
    return header + "\n" + "\n".join(body_lines) + "\n"


def build_document(title: str, preamble: str, as_of: str, table_md: str) -> str:
    """Assemble final Markdown doc."""
    front_matter = f"---\ntitle: {title}\n---\n"
    lead = f"\nAs of {as_of}, {preamble}\n\n\n"
    return front_matter + lead + table_md


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Markdown file with title/preamble and a table from repeater JSON and optional height CSV."
    )
    parser.add_argument("data_json", help="Path to data JSON (list or dict keyed by public_key).")
    parser.add_argument("meta_json", help="Path to meta JSON containing 'title' and 'preamble'.")
    parser.add_argument("output_md", help="Path to output Markdown file.")
    parser.add_argument("--height-csv", default=None, help="Optional CSV with 'Public Key' and 'Antenna Height Above Ground (m)'.")
    parser.add_argument("--no-sort", action="store_true", help="Do not sort by prefix then name (default: sort ascending).")
    parser.add_argument("--wrap", type=int, default=0, help="Wrap public_key every N chars (default: 0 = no wrap).")
    parser.add_argument("--date", default=None, help="Override date used in 'As of ...' (YYYY-MM-DD).")
    args = parser.parse_args()

    rows = load_rows(args.data_json)
    height_map = load_height_map(args.height_csv)
    apply_heights(rows, height_map)

    if not args.no_sort:
        rows.sort(key=lambda r: (r["public_key_prefix"], r["name"].lower()))

    meta = load_meta(args.meta_json)
    as_of_str = format_as_of(args.date)
    table_md = table_markdown(rows, wrap=args.wrap)
    doc = build_document(meta["title"], meta["preamble"], as_of_str, table_md)

    with open(args.output_md, "w") as f:
        f.write(doc)

    print(f"Wrote {len(rows)} sorted rows to {args.output_md}")


if __name__ == "__main__":
    main()
