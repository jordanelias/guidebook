#!/usr/bin/env python3
"""
scripts/convert/convert_specialists.py — Part 9 → specialist YAML

Extracts specialist consultant roles from Part 9 and produces one
YAML file per role in data/specialists/.

Usage:
    python3 scripts/convert/convert_specialists.py
    python3 scripts/convert/convert_specialists.py --dry-run
"""

import os
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "specialists"

# Specialist definitions — from Part 9 §9.2–§9.8
SPECIALISTS = [
    {
        "specialist_id": "SPEC-ROLE-01",
        "role": "OT",
        "role_label": "Occupational Therapist",
        "part_section": "§9.2",
        "role_description": "Assesses individual functional capacity and translates it into spatial requirements. Primary specialist for Mode S resolution — OT assessment determines where within a Mode P range the individual's needs fall.",
        "population_codes": ["MOB", "VIS", "NEU", "DEM", "OFS", "PAIN", "NDV", "DBL"],
        "appointment_triggers": [
            "Mode S design (individual client known)",
            "Complex co-occurring disability profiles",
            "Home modification projects",
            "Specialist residential facilities (DEM, NEU)",
        ],
        "co_design_notes": "CRPD Article 4.3 requires participation of disabled persons in design processes. The OT facilitates co-design between the disabled person and the design team, ensuring the person's own preferences and functional goals — not just clinical assessment — shape the specification.",
        "guidebook_relationship": "The guidebook equips the architect with Mode P defaults. The OT resolves Mode S. The guidebook is not a substitute for OT assessment; it is the brief that frames what the OT assesses against.",
    },
    {
        "specialist_id": "SPEC-ROLE-02",
        "role": "dementia-design",
        "role_label": "Dementia Design Specialist",
        "part_section": "§9.3",
        "role_description": "Expert in environmental design for cognitive impairment, particularly dementia. Advises on wayfinding, spatial legibility, sensory environment, and safety provisions specific to DEM populations.",
        "population_codes": ["DEM"],
        "appointment_triggers": [
            "Specialist dementia care facilities",
            "Residential projects with DEM primary population",
            "Wayfinding design in complex buildings where DEM users are anticipated",
        ],
    },
    {
        "specialist_id": "SPEC-ROLE-03",
        "role": "deafspace",
        "role_label": "DeafSpace / Deaf Design Consultant",
        "part_section": "§9.4",
        "role_description": "Expert in spatial design for Deaf and hard-of-hearing communities. Advises on visual communication, sightlines, lighting for sign language, acoustic management for hearing aid/CI users, and DeafSpace principles.",
        "population_codes": ["DEAF", "DBL"],
        "appointment_triggers": [
            "Buildings serving Deaf communities (schools, clubs, services)",
            "Projects where DEAF is a primary population",
            "Assembly spaces requiring hearing loop or Auracast design",
        ],
    },
    {
        "specialist_id": "SPEC-ROLE-04",
        "role": "sensory-design",
        "role_label": "Sensory Design Consultant",
        "part_section": "§9.5",
        "role_description": "Expert in sensory environment design for neurodivergent populations. Advises on acoustic, lighting, colour, texture, and spatial provisions for NDV users including autism, ADHD, and sensory processing differences.",
        "population_codes": ["NDV", "NDV/AUT", "NDV/ADHD", "NDV/SENS"],
        "appointment_triggers": [
            "Educational facilities (all levels)",
            "Workplace design with NDV population",
            "Sensory room or quiet room specification",
            "Projects with NDV/AUT as primary population",
        ],
    },
    {
        "specialist_id": "SPEC-ROLE-05",
        "role": "accessibility-auditor",
        "role_label": "Accessibility Auditor",
        "part_section": "§9.6",
        "role_description": "Independent reviewer who audits design documentation and completed construction against the guidebook specifications and applicable building codes. Provides compliance verification at stage gates.",
        "population_codes": ["ALL"],
        "appointment_triggers": [
            "Design stage gate reviews (SD, DD, CD)",
            "Pre-occupation inspection",
            "Post-occupancy evaluation",
            "Dispute resolution on accessibility compliance",
        ],
    },
    {
        "specialist_id": "SPEC-ROLE-06",
        "role": "disability-organisation",
        "role_label": "Disability Organisations and Lived Experience Input",
        "part_section": "§9.8",
        "role_description": "Representative organisations of disabled people providing lived experience input to design processes. Not a consulting role in the traditional sense — this is rights-based participation per CRPD Article 4.3.",
        "population_codes": ["ALL"],
        "appointment_triggers": [
            "Public buildings and facilities",
            "Projects funded by public bodies",
            "Any project seeking Co-1 (co-primary) evidence status for design decisions",
        ],
        "co_design_notes": "CRPD Article 4.3: 'States Parties shall closely consult with and actively involve persons with disabilities.' Disability organisations are the primary vehicle for this requirement in building design.",
    },
]


def convert(dry_run: bool = False):
    """Convert specialist definitions to YAML files."""
    if dry_run:
        print(f"Would write {len(SPECIALISTS)} specialist records to {OUTPUT_DIR}/")
        for s in SPECIALISTS:
            print(f"  {s['specialist_id']}: {s['role_label']}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for specialist in SPECIALISTS:
        record = {**specialist, "status": "active"}
        filename = specialist["role"] + ".yaml"
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

    print(f"\nTotal: {len(SPECIALISTS)} specialist records")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
