#!/usr/bin/env python3
"""
scripts/convert/convert_items.py — part04-item-index.md → item YAML

Reads references/part04-item-index.md and produces one YAML file per item
in data/items/. Optionally reads item body text from parts/v10/part04.md
using the line ranges specified in the index.

Usage:
    python3 scripts/convert/convert_items.py
    python3 scripts/convert/convert_items.py --dry-run
    python3 scripts/convert/convert_items.py --with-body
"""

import os
import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INDEX_PATH = REPO_ROOT / "references" / "part04-item-index.md"
PART4_PATH = REPO_ROOT / "parts" / "v10" / "part04.md"
OUTPUT_DIR = REPO_ROOT / "data" / "items"

# Category name lookup
CATEGORY_NAMES = {
    "A": "Acoustics",
    "B": "Lighting and Visual Environment",
    "C": "Colour and Contrast",
    "D": "Wayfinding and Cognitive Environment",
    "E": "Circulation and Entrances",
    "F": "Thermal and Air Quality",
    "G": "Seating, Surfaces, and Fixtures",
    "H": "Controls and Hardware",
    "I": "Bathroom and Wet Areas",
    "J": "Kitchen and Workspace",
    "K": "Communication and Alerting",
}

# Item status inference from title
MERGED_PATTERN = re.compile(r"\[MERGED INTO .+ per .+\]", re.IGNORECASE)
ABSORBED_PATTERN = re.compile(r"\[ABSORBED INTO .+ per .+\]", re.IGNORECASE)


def parse_index(index_path: Path) -> list[dict]:
    """Parse the markdown table from part04-item-index.md."""
    items = []
    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    for line in lines:
        line = line.strip()

        # Detect table header row
        if line.startswith("| Code"):
            in_table = True
            continue

        # Skip separator
        if line.startswith("|---"):
            continue

        if not in_table or not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 5:
            continue

        code, title, start, end, num_lines = cells[:5]

        # Determine status
        status = "active"
        if MERGED_PATTERN.search(title):
            status = "merged"
        elif ABSORBED_PATTERN.search(title):
            status = "merged"

        # Extract category
        category = code.split("-")[0] if "-" in code else code[0]

        items.append(
            {
                "item_code": code,
                "name": title.strip(),
                "category": category,
                "category_name": CATEGORY_NAMES.get(category, "Unknown"),
                "part_section": f"§4.{category}",
                "line_start": int(start) if start.isdigit() else None,
                "line_end": int(end) if end.isdigit() else None,
                "status": status,
            }
        )

    return items


def extract_body(part4_path: Path, start: int, end: int) -> str:
    """Extract item body text from Part 4 using line numbers."""
    with open(part4_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Line numbers are 1-indexed
    body_lines = lines[start - 1 : end]
    return "".join(body_lines).strip()


def convert(dry_run: bool = False, with_body: bool = False):
    """Convert item index to per-item YAML files."""
    if not INDEX_PATH.exists():
        print(f"ERROR: Index file not found: {INDEX_PATH}", file=sys.stderr)
        sys.exit(1)

    items = parse_index(INDEX_PATH)

    if dry_run:
        print(f"Would write {len(items)} item records to {OUTPUT_DIR}/")
        for item in items:
            status_tag = f" [{item['status'].upper()}]" if item["status"] != "active" else ""
            print(f"  {item['item_code']}: {item['name'][:60]}{status_tag}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, item in enumerate(items):
        item_id = f"ITEM-{i + 1:04d}"

        record = {
            "item_id": item_id,
            "item_code": item["item_code"],
            "category": item["category"],
            "category_name": item["category_name"],
            "name": item["name"],
            "part_section": item["part_section"],
            "status": item["status"],
        }

        if with_body and PART4_PATH.exists() and item["line_start"] and item["line_end"]:
            record["body_md"] = extract_body(PART4_PATH, item["line_start"], item["line_end"])

        filename = item["item_code"].lower().replace("-", "_") + ".yaml"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                record,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )
        print(f"  Wrote {filepath}")

    print(f"\nTotal: {len(items)} item records")


def main():
    dry_run = "--dry-run" in sys.argv
    with_body = "--with-body" in sys.argv
    convert(dry_run=dry_run, with_body=with_body)


if __name__ == "__main__":
    main()
