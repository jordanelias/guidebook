#!/usr/bin/env python3
"""
scripts/convert/convert_connections.py — Convert connection register _index.md
to validated YAML files under data/connections/.

Parses the markdown table from references/connections/_index.md.

Usage:
    python3 scripts/convert/convert_connections.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.connection import Connection


def parse_bool(val: str) -> bool:
    """Parse boolean from markdown table cell."""
    return val.strip().lower() in ("true", "yes", "✓", "1")


def parse_index_table(text: str) -> list:
    """Parse the connection register index table.

    Returns list of dicts, one per table row.
    """
    records = []
    in_table = False
    headers = []

    for line in text.split("\n"):
        # Find table header
        if "| CON-ID" in line:
            headers = [h.strip() for h in line.split("|") if h.strip()]
            in_table = True
            continue

        # Skip separator row
        if in_table and re.match(r"^\|[\s\-|]+$", line):
            continue

        if in_table and "|" in line:
            cells = [c.strip() for c in line.split("|")]
            cells = [c for c in cells if c != ""]

            if len(cells) < 6:
                continue

            con_id = cells[0]
            if not re.match(r"CON-\d{4}", con_id):
                continue

            status = cells[1]
            primary_target = cells[2]
            filed_in = cells[3]
            confidence = cells[4]
            opus_reviewed = parse_bool(cells[5]) if len(cells) > 5 else False
            session_applied = cells[6] if len(cells) > 6 else None

            # Clean session_applied
            if session_applied and session_applied.strip() in ("—", "-", ""):
                session_applied = None

            records.append({
                "con_id": con_id,
                "status": status,
                "primary_target": primary_target,
                "filed_in": filed_in,
                "confidence": confidence,
                "opus_reviewed": opus_reviewed,
                "session_applied": session_applied,
            })

        elif in_table and not line.strip():
            # End of table
            break

    return records


def main():
    parser = argparse.ArgumentParser(
        description="Convert connection register to validated YAML"
    )
    parser.add_argument(
        "--input",
        default="references/connections/_index.md",
        help="Path to connection register index",
    )
    parser.add_argument(
        "--output-dir",
        default="data/connections",
        help="Output directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    records = parse_index_table(text)
    print(f"Parsed {len(records)} connection records")

    os.makedirs(args.output_dir, exist_ok=True)
    passed = 0
    failed = 0

    for rec in records:
        cid = rec["con_id"]
        try:
            conn = Connection.model_validate(rec)
            if not args.dry_run:
                fname = cid.lower().replace("-", "-") + ".yaml"
                conn.to_yaml(os.path.join(args.output_dir, fname))
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {cid}: {e}", file=sys.stderr)

    print(f"\nResults: {passed} passed, {failed} failed")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
