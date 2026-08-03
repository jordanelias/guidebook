#!/usr/bin/env python3
"""
scripts/migrate/phase_02_populations.py — Phase 2: Population migration

Migrates population data from references/website/data/populations.json
into the population table in guidebook.db.

Depends on: init_database.py (Phase 0)

Usage:
    python3 scripts/migrate/phase_02_populations.py
    python3 scripts/migrate/phase_02_populations.py --dry-run
    python3 scripts/migrate/phase_02_populations.py --verify
"""

import json
import os
import sys
import sqlite3
from pathlib import Path

DB_PATH = "data/db/guidebook.db"
POP_PATH = "references/website/data/populations.json"


def migrate(repo_root: Path, dry_run: bool = False):
    """Migrate populations.json into SQLite population table."""
    pop_path = repo_root / POP_PATH
    db_path = repo_root / DB_PATH

    if not pop_path.exists():
        print(f"ERROR: {pop_path} not found")
        sys.exit(1)
    if not db_path.exists():
        print(f"ERROR: {db_path} not found. Run init_database.py first.")
        sys.exit(1)

    with open(pop_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    populations = data.get('populations', [])
    records = []

    for pop in populations:
        code = pop['population_id']

        # Top-level population
        records.append({
            'code': code,
            'parent_code': None,
            'label': pop.get('label', ''),
            'definition': pop.get('functional_profile', '')[:500] if pop.get('functional_profile') else '',
            'prevalence_band': None,
            'evidence_strength': pop.get('evidence_confidence'),
            'notes': pop.get('co_occurrence_notes'),
        })

        # Sub-populations
        for sc in pop.get('sub_codes', []):
            sub_label = pop.get('sub_code_labels', {}).get(sc, sc)
            records.append({
                'code': sc,
                'parent_code': code,
                'label': sub_label,
                'definition': f'Sub-population of {pop.get("label", code)}',
                'prevalence_band': None,
                'evidence_strength': None,
                'notes': None,
            })

    if dry_run:
        print(f"Would insert {len(records)} population records:")
        for r in records:
            indent = "    " if r['parent_code'] else "  "
            print(f"{indent}{r['code']}: {r['label']}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    inserted = 0
    skipped = 0
    for r in records:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO population (code, parent_code, label, definition,
                    prevalence_band, evidence_strength, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (r['code'], r['parent_code'], r['label'], r['definition'],
                  r['prevalence_band'], r['evidence_strength'], r['notes']))
            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        except sqlite3.IntegrityError as e:
            print(f"  ERROR inserting {r['code']}: {e}")
            skipped += 1

    conn.commit()
    conn.close()

    print(f"Phase 2 complete: {inserted} inserted, {skipped} skipped (already exist)")


def verify(repo_root: Path):
    """Verify population migration."""
    db_path = repo_root / DB_PATH
    conn = sqlite3.connect(str(db_path))

    total = conn.execute("SELECT COUNT(*) FROM population").fetchone()[0]
    top_level = conn.execute("SELECT COUNT(*) FROM population WHERE parent_code IS NULL").fetchone()[0]
    sub_codes = conn.execute("SELECT COUNT(*) FROM population WHERE parent_code IS NOT NULL").fetchone()[0]

    print(f"Phase 2 verification:")
    print(f"  Total populations: {total}")
    print(f"  Top-level: {top_level}")
    print(f"  Sub-codes: {sub_codes}")

    # Check resolved view
    resolved = conn.execute("SELECT COUNT(*) FROM population_resolved").fetchone()[0]
    print(f"  Resolved view rows: {resolved}")

    # List all
    cursor = conn.execute("SELECT code, parent_code, label FROM population ORDER BY code")
    for row in cursor.fetchall():
        indent = "    " if row[1] else "  "
        print(f"{indent}{row[0]}: {row[2]}")

    conn.close()

    checks_passed = total > 0 and top_level >= 11 and resolved == total
    print(f"\n  {'PASS' if checks_passed else 'FAIL'}")
    return checks_passed


def main():
    dry_run = '--dry-run' in sys.argv
    verify_only = '--verify' in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent

    if verify_only:
        ok = verify(repo_root)
        sys.exit(0 if ok else 1)
    else:
        migrate(repo_root, dry_run)


if __name__ == "__main__":
    main()
