#!/usr/bin/env python3
"""
scripts/convert/convert_throughlines.py — throughline-analysis.md → YAML

Extracts throughline entries from references/throughline-analysis.md
and produces one YAML file per throughline in data/throughlines/.

Usage:
    python3 scripts/convert/convert_throughlines.py
    python3 scripts/convert/convert_throughlines.py --dry-run
"""

import os
import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_PATH = REPO_ROOT / "references" / "throughline-analysis.md"
OUTPUT_DIR = REPO_ROOT / "data" / "throughlines"


def parse_throughlines(input_path: Path) -> list[dict]:
    """Parse throughline entries from the analysis document."""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # Split by ### T-NN headings
    sections = re.split(r"(?=^### T-\d{2}\.)", content, flags=re.MULTILINE)

    for section in sections:
        m = re.match(r"^### (T-\d{2})\.\s*(.+)$", section, re.MULTILINE)
        if not m:
            continue

        tid = m.group(1)
        title = m.group(2).strip()

        # Extract description — first paragraph after heading
        lines = section.split("\n")
        desc_lines = []
        in_desc = False
        for line in lines[1:]:
            stripped = line.strip()
            if not in_desc and stripped:
                in_desc = True
            if in_desc:
                if not stripped and desc_lines:
                    break
                desc_lines.append(stripped)

        description = " ".join(desc_lines).strip()
        if len(description) > 500:
            description = description[:500] + "..."

        # Extract item code references
        spec_refs = sorted(set(re.findall(r"\b([A-K]-\d{2})\b", section)))

        # Extract population codes
        pop_pattern = re.compile(
            r"\b(MOB|VIS|DEAF|NEU|DEM|NDV|PAIN|DBL|OFS|IntD|ALL)\b"
        )
        pop_codes = sorted(set(pop_pattern.findall(section)))

        slug = title.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")

        entries.append({
            "throughline_id": tid,
            "title": title,
            "slug": slug,
            "description": description,
            "specification_refs": spec_refs,
            "population_codes": pop_codes,
            "status": "active",
        })

    return entries


def convert(dry_run: bool = False):
    """Convert throughline analysis to per-entry YAML files."""
    if not INPUT_PATH.exists():
        print(f"ERROR: Input not found: {INPUT_PATH}", file=sys.stderr)
        sys.exit(1)

    entries = parse_throughlines(INPUT_PATH)

    if dry_run:
        print(f"Would write {len(entries)} throughline records to {OUTPUT_DIR}/")
        for e in entries:
            print(f"  {e['throughline_id']}: {e['title']}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for entry in entries:
        filename = entry["throughline_id"].lower() + ".yaml"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                entry, f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )
        print(f"  Wrote {filepath}")

    print(f"\nTotal: {len(entries)} throughline records")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
