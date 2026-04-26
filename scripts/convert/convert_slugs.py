#!/usr/bin/env python3
"""
scripts/convert/convert_slugs.py — Convert slug-registry.md to validated YAML.

Usage:
    python3 scripts/convert/convert_slugs.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.slug import Slug


def parse_slug_table(text: str) -> list:
    """Parse slug registry markdown table."""
    records = []
    in_table = False

    for line in text.split("\n"):
        if "| Slug" in line:
            in_table = True
            continue
        if in_table and re.match(r"^\|[\s\-|]+$", line):
            continue

        if in_table and "|" in line:
            cells = [c.strip().strip("`") for c in line.split("|") if c.strip()]
            if len(cells) < 5:
                continue

            slug_name = cells[0].strip("~~ ").strip("`").strip()
            if not slug_name or slug_name.lower() == "slug":
                continue

            # Detect MERGED (strikethrough ~~slug~~)
            is_merged = "~~" in line.split("|")[1] if len(line.split("|")) > 1 else False
            status = "MERGED" if is_merged else cells[4] if len(cells) > 4 else "ACTIVE"

            # Extract merge target from status field
            merged_into = None
            if "MERGED" in status or "→" in status:
                m = re.search(r"→\s*(.+)", status)
                if m:
                    merged_into = m.group(1).strip().strip("`")
                status = "MERGED"

            records.append({
                "slug": slug_name,
                "topic_directory": cells[1].strip("`") if len(cells) > 1 else "",
                "sl_path": cells[2].strip("`") if len(cells) > 2 else "",
                "bpc_path": cells[3].strip("`") if len(cells) > 3 else "",
                "status": status,
                "merged_into": merged_into,
            })

        elif in_table and not line.strip():
            break

    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="references/slug-registry.md")
    parser.add_argument("--output-dir", default="data/slugs")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    records = parse_slug_table(text)
    print(f"Parsed {len(records)} slug records")

    os.makedirs(args.output_dir, exist_ok=True)
    passed = failed = 0

    for rec in records:
        try:
            slug_obj = Slug.model_validate(rec)
            if not args.dry_run:
                fname = rec["slug"] + ".yaml"
                slug_obj.to_yaml(os.path.join(args.output_dir, fname))
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {rec['slug']}: {e}", file=sys.stderr)

    print(f"\nResults: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
