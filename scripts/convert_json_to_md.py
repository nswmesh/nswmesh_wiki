#!/usr/bin/env python3
import json
import argparse
import sys
import textwrap
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional


def first_byte_prefix(public_key: str) -> str:
    """Return the first two octets (four hex chars) in uppercase."""
    if not public_key or len(public_key) < 4:
        return (public_key or "").upper()
    return public_key[:4].upper()


def is_hex(s: str) -> bool:
    """Check if a string is valid hexadecimal."""
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
    - Replace '|' with '/' so we don't break markdown table cells.
    """
    if raw is None:
        raw = ""
    return raw.replace("|", "/")


def tick_or_blank(value: Any) -> str:
    """
    For advert_location / internet_location:
    - true  -> '✔'
    - false -> ''
    """
    return "✔" if value is True else ""


def settings_shorthand(band: Optional[str]) -> str:
    """
    Map Frequency Band to shorthand:
    - Narrow -> 'N'
    - Wide   -> 'W'
    - Medium -> 'M'
    """
    if not band:
        return ""
    mapping = {
        "narrow": "N",
        "wide": "W",
        "medium": "M"
    }
    return mapping.get(band.strip().lower(), band)


def load_height_map(csv_path: Optional[str]) -> Dict[str, str]:
    """
    Load optional height CSV mapping public_key -> height_m.
    Matches headers: 'Public Key' and 'Antenna Height Above Ground (m)'.
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
                     .lstrip("\ufeff")
                     .lower()
                     .replace(" ", "")
                )

            header_map = {norm(h): h for h in (reader.fieldnames or [])}

            public_key_header = None
            if "publickey" in header_map:
                public_key_header = header_map["publickey"]

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
                print("Warning: couldn't find 'Public Key' column in CSV.", file=sys.stderr)
                return height_map

            for row in reader:
                pub_raw = (row.get(public_key_header) or "").strip().replace(" ", "").replace("\n", "")
                if not pub_raw:
                    continue
                height_raw = (row.get(height_header) or "").strip() if height_header else ""
                height_map[pub_raw] = height_raw

    except Exception as e:
        print(f"Warning: could not read height CSV '{csv_path}': {e}", file=sys.stderr)

    return height_map


def _rows_from_list(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for i, item in enumerate(items, 1):
        name = (item.get("name") or "").strip()
        pub = (item.get("public_key") or "").strip().replace(" ", "").replace("\n", "")

        if not name or not pub:
            continue

        prefix = (item.get("public_key_prefix") or first_byte_prefix(pub)).upper()

        if not is_hex(prefix):
            print(f"Warning: item {i} prefix '{prefix}' is not valid hex; emitting anyway", file=sys.stderr)

        rows.append({
            "public_key_prefix": prefix,
            "name": name,
            "public_key": pub,
            "last_seen": (item.get("last_seen") or "").strip(),
            "advert_location": item.get("advert_location", None),
            "internet_location": item.get("internet_location", None),
            "settings": settings_shorthand(item.get("frequency_band")),
            "height_m": "",
        })
    return rows


def _rows_from_dict(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for key_pub, info in obj.items():
        if isinstance(info, dict):
            pub = str(info.get("public_key") or key_pub).strip().replace(" ", "").replace("\n", "")
            name = (info.get("name") or "").strip()
            prefix = str(info.get("public_key_prefix") or first_byte_prefix(pub)).upper()

            if not is_hex(prefix):
                print(f"Warning: entry '{name}' prefix '{prefix}' is not valid hex; emitting anyway", file=sys.stderr)

            rows.append({
                "public_key_prefix": prefix,
                "name": name,
                "public_key": pub,
                "last_seen": (info.get("last_seen") or "").strip(),
                "advert_location": info.get("advert_location", None),
                "internet_location": info.get("internet_location", None),
                "settings": settings_shorthand(info.get("frequency_band")),
                "height_m": "",
            })
    return rows


def load_rows(path: str) -> List[Dict[str, Any]]:
    with open(path, "r") as f:
        data = json.load(f)
    if isinstance(data, list):
        return _rows_from_list(data)
    if isinstance(data, dict):
        return _rows_from_dict(data)
    raise ValueError("JSON must be a list or a dict.")


def apply_heights(rows: List[Dict[str, Any]], height_map: Dict[str, str]) -> None:
    for r in rows:
        pub = r["public_key"]
        if pub in height_map:
            r["height_m"] = height_map[pub]


def table_markdown(rows: List[Dict[str, Any]], wrap: int) -> str:
    """
    Updated Markdown table with Public Key as the last column.
    """
    header = (
        "| public_key_prefix | name | settings | last_seen | advert_location | internet_location | antenna height (m) | public_key |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    body_lines = []
    for r in rows:
        safe_name = sanitize_name(r["name"])
        pubkey_cell = wrap_hex(r["public_key"], wrap)
        advert_cell = tick_or_blank(r.get("advert_location"))
        internet_cell = tick_or_blank(r.get("internet_location"))
        
        body_lines.append(
            f"| {r['public_key_prefix']} | {safe_name} | {r['settings']} | {r['last_seen']} | {advert_cell} | {internet_cell} | {r['height_m']} | {pubkey_cell} |"
        )
    return header + "\n" + "\n".join(body_lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_json")
    parser.add_argument("meta_json")
    parser.add_argument("output_md")
    parser.add_argument("--height-csv", default=None)
    parser.add_argument("--no-sort", action="store_true")
    parser.add_argument("--wrap", type=int, default=0)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    rows = load_rows(args.data_json)
    height_map = load_height_map(args.height_csv)
    apply_heights(rows, height_map)

    if not args.no_sort:
        # Sorting by 2-octet prefix (4 chars) then name
        rows.sort(key=lambda r: (r["public_key_prefix"], r["name"].lower()))

    with open(args.meta_json, "r") as f:
        meta = json.load(f)

    if args.date:
        as_of = args.date
    else:
        dt = datetime.now()
        as_of = f"{dt.day} {dt.strftime('%B %Y')}"

    table_md = table_markdown(rows, wrap=args.wrap)
    
    doc = f"---\ntitle: {meta['title']}\n---\n\nAs of {as_of}, {meta['preamble']}\n\n\n" + table_md

    with open(args.output_md, "w") as f:
        f.write(doc)

    print(f"Wrote {len(rows)} rows to {args.output_md}")


if __name__ == "__main__":
    main()
