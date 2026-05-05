"""
scripts/migrate/migrate_gaps.py — Migrate gap_register.md → SQLite gaps table.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 5
Source: gap_register.md
Validation: No OPEN P1 rows lost

Usage:
    python3 scripts/migrate/migrate_gaps.py --source gap_register.md --session SESSION [--dry-run]
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def parse_gap_register(path: str) -> list[dict]:
    """Parse gap_register.md markdown table into list of dicts."""
    text = Path(path).read_text()
    rows = []
    seen_ids = set()

    for line in text.splitlines():
        if not line.startswith("| GAP-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 9:
            continue

        gap_id = parts[1]
        category = parts[2]
        priority = parts[3]
        status = parts[4]
        skill = parts[5] if parts[5] else None
        section = parts[6] if parts[6] else None
        description = parts[7] if parts[7] else ""

        # Handle duplicates — take first occurrence
        if gap_id in seen_ids:
            continue
        seen_ids.add(gap_id)

        rows.append({
            "gap_id": gap_id,
            "category": category,
            "priority": priority,
            "status": status,
            "skill": skill,
            "section": section,
            "description": description,
        })

    return rows


def migrate(source: str, session: str, dry_run: bool = False):
    rows = parse_gap_register(source)
    print(f"Parsed {len(rows)} gaps from {source}")

    # Stats
    status_counts = {}
    priority_counts = {}
    for r in rows:
        s = "OPEN" if r["status"].startswith("OPEN") else "CLOSED"
        status_counts[s] = status_counts.get(s, 0) + 1
        priority_counts[r["priority"]] = priority_counts.get(r["priority"], 0) + 1

    print(f"  Status: {json.dumps(status_counts)}")
    print(f"  Priority: {json.dumps(priority_counts)}")

    open_p1 = [r for r in rows
                if r["priority"] == "P1" and r["status"].startswith("OPEN")]
    print(f"  OPEN P1 count: {len(open_p1)}")
    for g in open_p1:
        print(f"    {g['gap_id']}: {g['description'][:80]}")

    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    inserted = 0
    errors = []

    for r in rows:
        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO gaps "
                    "(gap_id, category, priority, status, skill, section, "
                    " description, created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    [r["gap_id"], r["category"], r["priority"], r["status"],
                     r["skill"], r["section"], r["description"],
                     ts, session, ts, session]
                )
            inserted += 1
        except sqlite3.IntegrityError as e:
            errors.append(f"  {r['gap_id']}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{inserted}/{len(rows)} gaps")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)

    # Validation
    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        total = conn2.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]
        open_p1_db = conn2.execute(
            "SELECT COUNT(*) FROM gaps "
            "WHERE priority='P1' AND status LIKE 'OPEN%'"
        ).fetchone()[0]
        conn2.close()
        print(f"\nValidation:")
        print(f"  Total rows: {total} "
              f"({'✓' if total == len(rows) else '✗ MISMATCH'})")
        print(f"  OPEN P1: {open_p1_db} "
              f"({'✓ MATCH' if open_p1_db == len(open_p1) else '✗ MISMATCH'})")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    migrate(args.source, args.session, args.dry_run)
