#!/usr/bin/env python3
"""
scripts/convert/convert_doctrines.py — Part 1 → doctrine YAML

Extracts doctrine entries from Part 1 section headings and prose.
Produces one YAML file per doctrine in data/doctrines/.

Usage:
    python3 scripts/convert/convert_doctrines.py
    python3 scripts/convert/convert_doctrines.py --dry-run
"""

import os
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PART1_PATH = REPO_ROOT / "parts" / "v10" / "part01.md"
OUTPUT_DIR = REPO_ROOT / "data" / "doctrines"

# Doctrine definitions — manually curated from Part 1 structure
DOCTRINES = [
    {
        "doctrine_id": "DOC-0001",
        "slug": "code-as-floor",
        "title": "The Code-as-Floor Principle",
        "group": "core",
        "part_section": "§1.2",
        "statement": "Building codes establish minimum legal requirements. This guidebook treats code compliance as the floor, not the ceiling. Every specification meets or exceeds the most demanding code requirement from any jurisdiction surveyed.",
    },
    {
        "doctrine_id": "DOC-0002",
        "slug": "functional-capacity",
        "title": "Functional Capacity Over Category Minimums",
        "group": "core",
        "part_section": "§1.3",
        "statement": "Design for the functional capacity of the individual, not the administrative disability category. Specifications are calibrated to the range of functional capacity within each population, with median values as population-informed defaults.",
    },
    {
        "doctrine_id": "DOC-0003",
        "slug": "design-modes",
        "title": "Design Modes",
        "group": "core",
        "part_section": "§1.3",
        "statement": "Universal Mode (population-agnostic, fixed values), Mode P (population-informed, ranges with median default), and Mode S (person-specific, OT assessment resolves range). DAR mandatory at all modes.",
    },
    {
        "doctrine_id": "DOC-0004",
        "slug": "universal-inclusive-design",
        "title": "Universal Design, Inclusive Design, and This Guidebook",
        "group": "core",
        "part_section": "§1.4",
        "statement": "Universal design provides the baseline. Inclusive design extends it to identified populations. This guidebook integrates both: Universal Mode for population-agnostic provisions, Mode P for population-specific calibration.",
    },
    {
        "doctrine_id": "DOC-0005",
        "slug": "evidence-hierarchy",
        "title": "Evidence Hierarchy",
        "group": "evidence",
        "part_section": "§1.5",
        "statement": "Six evidence tiers (1-6) from systematic reviews to expert consensus. Every specification carries its evidence tier. Co-primary (Co-1) evidence from lived experience has equal standing with academic evidence at the same tier.",
    },
    {
        "doctrine_id": "DOC-0006",
        "slug": "dar-principle",
        "title": "Design for Adaptable Readiness (DAR)",
        "group": "core",
        "part_section": "§1.6",
        "statement": "Build in now what cannot be retrofitted later without structural intervention. DAR provisions appear on construction drawings at the CD stage, whether or not the current occupant needs them.",
    },
    {
        "doctrine_id": "DOC-0007",
        "slug": "crpd-alignment",
        "title": "CRPD Framework Alignment",
        "group": "ethics",
        "part_section": "§1.7",
        "statement": "The Convention on the Rights of Persons with Disabilities (CRPD) provides the human rights framework. Article 9 (accessibility), Article 19 (independent living), and Article 4.3 (participation in design) govern all specifications.",
    },
    {
        "doctrine_id": "DOC-0008",
        "slug": "biomechanical-framework",
        "title": "Biomechanical Frame of Reference",
        "group": "frameworks",
        "part_section": "§1.8.1",
        "statement": "Specifications derived from physical capacity, joint range of motion, muscle strength, grip, reach, balance, and gait. Grab bar diameters, handrail heights, turning radii, and threshold heights are biomechanically derived.",
    },
    {
        "doctrine_id": "DOC-0009",
        "slug": "sensory-processing-model",
        "title": "Dunn's Sensory Processing Model",
        "group": "frameworks",
        "part_section": "§1.8.2",
        "statement": "Four sensory profiles (seeking, avoiding, sensitivity, low registration). Acoustic, lighting, and colour specifications are calibrated across all four profiles.",
    },
    {
        "doctrine_id": "DOC-0010",
        "slug": "ecology-human-performance",
        "title": "Ecology of Human Performance (EHP)",
        "group": "frameworks",
        "part_section": "§1.8.3",
        "statement": "Four intervention strategies: establish, alter, adapt, prevent. Most specifications alter the context (environment) rather than the person.",
    },
    {
        "doctrine_id": "DOC-0011",
        "slug": "compensatory-framework",
        "title": "Compensatory Frame of Reference",
        "group": "frameworks",
        "part_section": "§1.8.4",
        "statement": "Where functional capacity cannot be restored, the environment compensates. Lever hardware, automatic doors, and grab bars are compensatory provisions.",
    },
    {
        "doctrine_id": "DOC-0012",
        "slug": "cognitive-disabilities-model",
        "title": "Allen's Cognitive Disabilities Model",
        "group": "frameworks",
        "part_section": "§1.8.5",
        "statement": "Six cognitive levels (0-6). Wayfinding, signage, and spatial layout specifications for DEM and NDV users are calibrated to the cognitive level range of the target population.",
    },
    {
        "doctrine_id": "DOC-0013",
        "slug": "peop-model",
        "title": "Person-Environment-Occupation-Performance (PEOP)",
        "group": "frameworks",
        "part_section": "§1.8.6",
        "statement": "Dignified access, socially integrated design, and equivalent provisions are PEOP requirements, not aesthetic preferences.",
    },
    {
        "doctrine_id": "DOC-0014",
        "slug": "affordance-theory",
        "title": "Ecological Psychology — Affordance Theory",
        "group": "frameworks",
        "part_section": "§1.8.7",
        "statement": "Accessible environments provide affordances legible to the full range of functional capacities. Grab bar shapes, door pull widths, and floor texture specifications are affordance-based.",
    },
    {
        "doctrine_id": "DOC-0015",
        "slug": "competence-press",
        "title": "Competence-Press Model",
        "group": "frameworks",
        "part_section": "§1.8.8",
        "statement": "Specifications for DEM, CFS/ME, and OFS users maintain environmental press within the performance zone for the lower end of the functional capacity range.",
    },
    {
        "doctrine_id": "DOC-0016",
        "slug": "restoration-recovery-theory",
        "title": "Attention Restoration Theory and Stress Recovery Theory",
        "group": "frameworks",
        "part_section": "§1.8.9",
        "statement": "Evidence basis for biophilic design, natural lighting specifications, and sensory retreat provisions.",
    },
]


def convert(dry_run: bool = False):
    """Convert doctrine definitions to YAML files."""
    if dry_run:
        print(f"Would write {len(DOCTRINES)} doctrine records to {OUTPUT_DIR}/")
        for d in DOCTRINES:
            print(f"  {d['doctrine_id']}: {d['title']}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for doctrine in DOCTRINES:
        record = {**doctrine, "status": "active"}
        filename = doctrine["slug"] + ".yaml"
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

    print(f"\nTotal: {len(DOCTRINES)} doctrine records")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
