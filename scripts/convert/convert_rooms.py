#!/usr/bin/env python3
"""
scripts/convert/convert_rooms.py — Parts 6-7 → room YAML

Extracts room type definitions from Parts 6 (residential) and 7
(non-residential). Produces one YAML file per room in data/rooms/.

Note: Item matrices within rooms are complex table structures that
require manual curation. This converter extracts room identity and
metadata; item_matrix population is a C-stage task.

Usage:
    python3 scripts/convert/convert_rooms.py
    python3 scripts/convert/convert_rooms.py --dry-run
"""

import os
import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "rooms"

# Room definitions — from Parts 6-7 section headings
# Residential rooms (Part 6)
RESIDENTIAL_ROOMS = [
    {"room_id": "R-ENT", "room_label": "Entry", "section": "§6.1",
     "evidence_density": "▓ Moderate"},
    {"room_id": "R-GAR", "room_label": "Garage and Vehicle Space", "section": "§6.2",
     "evidence_density": "· Absent"},
    {"room_id": "R-LAU", "room_label": "Laundry", "section": "§6.3",
     "evidence_density": "░ Thin"},
    {"room_id": "R-HAL", "room_label": "Hallway and Circulation", "section": "§6.4",
     "evidence_density": "░ Thin"},
    {"room_id": "R-LIV", "room_label": "Living Room", "section": "§6.5",
     "evidence_density": "· Absent"},
    {"room_id": "R-KIT", "room_label": "Kitchen", "section": "§6.6",
     "evidence_density": "▓ Moderate"},
    {"room_id": "R-BA", "room_label": "Bathroom", "section": "§6.7",
     "evidence_density": "■ Rich"},
    {"room_id": "R-BED", "room_label": "Bedroom", "section": "§6.8",
     "evidence_density": "░ Thin"},
    {"room_id": "R-STA", "room_label": "Staircase", "section": "§6.9",
     "evidence_density": "░ Thin"},
]

# Non-residential rooms (Part 7) — extracted from Part 7 if it exists
NON_RESIDENTIAL_ROOMS = [
    {"room_id": "NR-EDU", "room_label": "Education", "section": "§7.1",
     "evidence_density": "▓ Moderate"},
    {"room_id": "NR-HLT", "room_label": "Healthcare", "section": "§7.2",
     "evidence_density": "▓ Moderate"},
    {"room_id": "NR-WRK", "room_label": "Workplace", "section": "§7.3",
     "evidence_density": "░ Thin"},
    {"room_id": "NR-RET", "room_label": "Retail and Commercial", "section": "§7.4",
     "evidence_density": "░ Thin"},
    {"room_id": "NR-CUL", "room_label": "Cultural", "section": "§7.5",
     "evidence_density": "░ Thin"},
    {"room_id": "NR-HOS", "room_label": "Hospitality", "section": "§7.6",
     "evidence_density": "░ Thin"},
    {"room_id": "NR-TRP", "room_label": "Transport", "section": "§7.7",
     "evidence_density": "░ Thin"},
]


def convert(dry_run: bool = False):
    """Convert room definitions to YAML files."""
    all_rooms = []

    for room in RESIDENTIAL_ROOMS:
        all_rooms.append({
            **room,
            "building_type": "residential",
            "part_source": 6,
            "status": "active",
        })

    for room in NON_RESIDENTIAL_ROOMS:
        all_rooms.append({
            **room,
            "building_type": "non-residential",
            "part_source": 7,
            "status": "active",
        })

    if dry_run:
        print(f"Would write {len(all_rooms)} room records to {OUTPUT_DIR}/")
        for r in all_rooms:
            print(f"  {r['room_id']}: {r['room_label']} ({r['building_type']})")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for room in all_rooms:
        filename = room["room_id"].lower().replace("-", "_") + ".yaml"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                room,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )
        print(f"  Wrote {filepath}")

    print(f"\nTotal: {len(all_rooms)} room records")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
