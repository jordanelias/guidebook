#!/usr/bin/env python3
"""
scripts/convert/convert_gaps.py — Convert gap_register.md to validated YAML.

Usage:
    python3 scripts/convert/convert_gaps.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.gap import Gap


def parse_gap_table(text: str) -> list:
    """Parse gap register markdown table."""
    records = []

    for line in text.split("\n"):
        if "|" not in line or "GAP-" not in line:
            continue

        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]

        if len(cells) < 7:
            continue

        gap_id = cells[0]
        if not gap_id.startswith("GAP-"):
            continue

        records.append({
            "gap_id": gap_id,
            "category": cells[1],
            "priority": cells[2],
            "status": cells[3],
            "skill": cells[4],
            "section": cells[5],
            "description": cells[6][:500],  # Truncate very long descriptions
            "date": cells[7].strip(" |") if len(cells) > 7 else "UNKNOWN",
        })

    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="gap_register.md")
    parser.add_argument("--output-dir", default="data/gaps")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    records = parse_gap_table(text)
    print(f"Parsed {len(records)} gap records")

    os.makedirs(args.output_dir, exist_ok=True)
    passed = failed = 0

    for rec in records:
        gid = rec["gap_id"]
        try:
            gap = Gap.model_validate(rec)
            if not args.dry_run:
                fname = gid.lower().replace("-", "-") + ".yaml"
                gap.to_yaml(os.path.join(args.output_dir, fname))
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {gid}: {e}", file=sys.stderr)

    print(f"\nResults: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
