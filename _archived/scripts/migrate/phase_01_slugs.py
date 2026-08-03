#!/usr/bin/env python3
"""
scripts/migrate/phase_01_slugs.py — Phase 1: Slug migration

Migrates slug data from references/slug-registry.md into the specification
table slug column. This is the first migration phase — it establishes the
stable identifier mapping.

Usage:
    python3 scripts/migrate/phase_01_slugs.py --verify
"""

import sys
import json
from pathlib import Path


def main():
    verify = '--verify' in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent

    # Read specification-database.json for slug data
    spec_db_path = repo_root / "references/specification-database.json"
    if not spec_db_path.exists():
        print(f"ERROR: {spec_db_path} not found")
        sys.exit(1)

    with open(spec_db_path, 'r') as f:
        data = json.load(f)

    specs = data.get('specifications', [])
    print(f"Phase 1: {len(specs)} specifications with slugs")

    # Verify slug uniqueness
    slugs = [s['slug'] for s in specs]
    spec_ids = [s['spec_id'] for s in specs]

    dupe_slugs = [s for s in slugs if slugs.count(s) > 1]
    dupe_ids = [s for s in spec_ids if spec_ids.count(s) > 1]

    if dupe_slugs:
        print(f"ERROR: Duplicate slugs: {set(dupe_slugs)}")
        sys.exit(1)
    if dupe_ids:
        print(f"ERROR: Duplicate spec_ids: {set(dupe_ids)}")
        sys.exit(1)

    print(f"  Slugs: {len(slugs)} (all unique)")
    print(f"  Spec IDs: {len(spec_ids)} (all unique)")

    if verify:
        print("\n  Verification passed.")
    else:
        print("\n  [Phase 1 applies via init_database.py + phase_05_specifications.py]")
        print("  Slug data is embedded in specification records during Phase 5.")


if __name__ == "__main__":
    main()
