#!/usr/bin/env python3
"""
scripts/convert/convert_fdr.py — FDR slug registry → FDR YAML

Reads references/fdr/fdr-slug-registry-v2.md and references/fdr/*.md files.
Produces one YAML file per FDR slug in data/fdr/.

Usage:
    python3 scripts/convert/convert_fdr.py
    python3 scripts/convert/convert_fdr.py --dry-run
"""

import os
import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = REPO_ROOT / "references" / "fdr" / "fdr-slug-registry-v2.md"
FDR_DIR = REPO_ROOT / "references" / "fdr"
OUTPUT_DIR = REPO_ROOT / "data" / "fdr"


def parse_registry(registry_path: Path) -> list[dict]:
    """Parse the FDR slug registry tables."""
    slugs = []

    with open(registry_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    for line in lines:
        line = line.strip()

        # Detect table header
        if line.startswith("| File slug") or line.startswith("| Slug"):
            in_table = True
            continue

        # Skip separator
        if line.startswith("|---"):
            continue

        # End table on empty line or non-table line
        if in_table and not line.startswith("|"):
            in_table = False
            continue

        if not in_table:
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue

        slug = cells[0]
        status = cells[1] if len(cells) > 1 else "NOT-RUN"
        remaining = cells[2] if len(cells) > 2 else ""

        # Determine scenario type from slug name or flags
        scenario_type = "failure"  # default
        if "[COMPOUND]" in remaining or "[COMPOUND]" in slug:
            scenario_type = "compound"
            slug = slug.replace("[COMPOUND]", "").strip()
        elif "[OCCUPATION]" in remaining or "[OCCUPATION]" in slug:
            scenario_type = "compound"  # occupation-level mapped to compound
            slug = slug.replace("[OCCUPATION]", "").strip()
        elif "[ENVIRONMENT]" in remaining:
            scenario_type = "failure"  # environment-led still failure-pattern

        # Clean slug
        slug = slug.strip(" `")

        if not slug or slug.startswith("---"):
            continue

        slugs.append(
            {
                "slug": slug,
                "status": status,
                "remaining": remaining if remaining and remaining != "—" else None,
                "scenario_type": scenario_type,
            }
        )

    return slugs


def read_fdr_file(fdr_dir: Path, slug: str) -> dict:
    """Read an FDR .md file and extract structured data."""
    filepath = fdr_dir / f"{slug}.md"
    if not filepath.exists():
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = {}

    # Extract title from first heading
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        result["title"] = title_match.group(1).strip()

    # Extract population codes mentioned
    pop_pattern = re.compile(
        r"\b(MOB|VIS|DEAF|NEU|DEM|NDV|PAIN|DBL|OFS|IntD|ALL|"
        r"MOB/AMB|MOB/UPL|NDV/AUT|NDV/ADHD|NDV/SENS|NDV/MH|"
        r"NEU/PCS|OFS/ME|OFS/POTS|OFS/MCAS)\b"
    )
    pops = sorted(set(pop_pattern.findall(content)))
    if pops:
        result["populations"] = pops

    # Extract item code references
    item_pattern = re.compile(r"\b([A-K]-\d{2})\b")
    items = sorted(set(item_pattern.findall(content)))
    if items:
        result["specification_refs"] = items

    # Word count as proxy for content depth
    result["word_count"] = len(content.split())

    return result


def convert(dry_run: bool = False):
    """Convert FDR registry to per-slug YAML files."""
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found: {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(1)

    slugs = parse_registry(REGISTRY_PATH)

    if dry_run:
        print(f"Would write {len(slugs)} FDR records to {OUTPUT_DIR}/")
        for s in slugs:
            file_exists = (FDR_DIR / f"{s['slug']}.md").exists()
            marker = "✓" if file_exists else "✗"
            print(f"  {marker} {s['slug']} [{s['status']}]")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, entry in enumerate(slugs):
        scenario_id = f"FDR-{i + 1:04d}"
        slug = entry["slug"]

        # Read FDR file if it exists
        file_data = read_fdr_file(FDR_DIR, slug)

        record = {
            "scenario_id": scenario_id,
            "scenario_type": entry["scenario_type"],
            "description": file_data.get("title", slug.replace("-", " ").title()),
            "source_slug": slug,
            "affected_populations": file_data.get("populations", []),
            "specification_refs": file_data.get("specification_refs", []),
            "notes": entry.get("remaining"),
        }

        # Add severity based on status
        if entry["status"] == "COMPLETE":
            record["severity"] = None  # Set during review
        elif entry["status"] == "PARTIAL":
            record["notes"] = (record.get("notes") or "") + " [PARTIAL — remaining scenarios listed in registry]"

        filename = slug + ".yaml"
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

    print(f"\nTotal: {len(slugs)} FDR records")


def main():
    dry_run = "--dry-run" in sys.argv
    convert(dry_run=dry_run)


if __name__ == "__main__":
    main()
