#!/usr/bin/env python3
"""
scripts/convert/convert_economics.py — economics.json → economics YAML

Reads references/website/data/economics.json and produces one YAML
file per entry in data/economics/.

Usage:
    python3 scripts/convert/convert_economics.py
    python3 scripts/convert/convert_economics.py --dry-run
"""

import json
import os
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_PATH = REPO_ROOT / "references" / "website" / "data" / "economics.json"
OUTPUT_DIR = REPO_ROOT / "data" / "economics"

# Map JSON section → pillar + entry_type
SECTION_MAP = {
    "cost_premiums": ("construction", "cost_premium"),
    "retrofit_multipliers": ("construction", "retrofit_multiplier"),
    "grant_programmes": ("inaction", "grant_programme"),
    "health_outcomes": ("health", "health_outcome"),
    "housing_deficit": ("inaction", "housing_deficit"),
    "research_gaps": ("health", "research_gap"),
}


def convert(dry_run: bool = False):
    """Convert economics.json to per-entry YAML files."""
    if not INPUT_PATH.exists():
        print(f"ERROR: Input file not found: {INPUT_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    counter = 1

    for section_key, (pillar, entry_type) in SECTION_MAP.items():
        section_data = data.get(section_key, [])
        if not isinstance(section_data, list):
            continue

        for item in section_data:
            entry_id = f"ECON-{counter:04d}"

            # Extract common fields
            record = {
                "entry_id": entry_id,
                "pillar": pillar,
                "entry_type": entry_type,
                "source": item.get("source", item.get("programme_name", "Unknown")),
                "jurisdiction": item.get("jurisdiction"),
                "finding": item.get("finding", item.get("description", "")),
                "study_design": item.get("study_design") or item.get("design"),
                "sample": item.get("sample"),
                "currency": item.get("currency"),
                "bcr": item.get("bcr"),
                "journal": item.get("journal"),
                "status": "active",
            }

            # Extract numeric value where available
            for num_field in ["premium_percent_min", "multiplier", "max_funding",
                              "accessible_pct", "gap_units"]:
                if num_field in item and item[num_field] is not None:
                    try:
                        record["value_numeric"] = float(item[num_field])
                    except (ValueError, TypeError):
                        pass
                    break

            entries.append(record)
            counter += 1

    # Handle market_value (dict, not list)
    mv = data.get("market_value", {})
    if isinstance(mv, dict):
        for key, val in mv.items():
            if isinstance(val, list):
                for item in val:
                    entry_id = f"ECON-{counter:04d}"
                    record = {
                        "entry_id": entry_id,
                        "pillar": "market",
                        "entry_type": "market_value",
                        "source": item.get("source", key),
                        "jurisdiction": item.get("jurisdiction"),
                        "finding": item.get("finding", ""),
                        "status": "active",
                    }
                    entries.append(record)
                    counter += 1

    if dry_run:
        print(f"Would write {len(entries)} economics records to {OUTPUT_DIR}/")
        for e in entries:
            print(f"  {e['entry_id']}: [{e['pillar']}] {e['source'][:50]}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for entry in entries:
        # Clean None values
        entry = {k: v for k, v in entry.items() if v is not None}
        filename = entry["entry_id"].lower() + ".yaml"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                entry, f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )

    print(f"Total: {len(entries)} economics records written to {OUTPUT_DIR}/")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
