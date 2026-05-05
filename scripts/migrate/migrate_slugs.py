"""
scripts/migrate/migrate_slugs.py — Migrate slug-registry.md → SQLite slugs table.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 1
Source: references/slug-registry.md
Validation: row count matches registry

Usage:
    python3 scripts/migrate/migrate_slugs.py --source slug-registry.md --session SESSION [--dry-run]
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def parse_slug_registry(path: str) -> list[dict]:
    """Parse slug-registry.md markdown table into list of dicts."""
    text = Path(path).read_text()
    rows = []

    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # parts[0] and parts[-1] are empty due to leading/trailing |
        if len(parts) < 7:
            continue

        slug_raw = parts[1]
        topic_dir = parts[2]
        sl_path = parts[3]
        bpc_path = parts[4]
        status_raw = parts[5]

        # Skip header and separator rows
        if slug_raw in ("Slug", "---") or slug_raw.startswith("---"):
            continue
        if topic_dir == "Topic directory":
            continue

        # Clean slug: remove backticks and strikethrough
        slug = slug_raw.replace("`", "").replace("~~", "").strip()

        # Clean paths: remove backticks
        topic_dir = topic_dir.replace("`", "").strip()
        sl_path = sl_path.replace("`", "").strip()
        bpc_path = bpc_path.replace("`", "").strip()

        # Parse status
        merged_into = None
        if status_raw.startswith("MERGED"):
            status = "MERGED"
            # Extract target: MERGED → `target-slug`
            m = re.search(r"→\s*`([^`]+)`", status_raw)
            if m:
                merged_into = m.group(1)
        elif status_raw.startswith("STUB"):
            status = "STUB"
        elif status_raw.startswith("PROVISIONAL"):
            status = "PROVISIONAL"
        else:
            status = "ACTIVE"

        rows.append({
            "slug": slug,
            "topic_directory": topic_dir,
            "sl_path": sl_path,
            "bpc_path": bpc_path,
            "status": status,
            "merged_into": merged_into,
        })

    return rows


def migrate(source: str, session: str, dry_run: bool = False):
    rows = parse_slug_registry(source)
    print(f"Parsed {len(rows)} slugs from {source}")

    status_counts = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    print(f"  Status breakdown: {json.dumps(status_counts)}")

    merged = [r for r in rows if r["merged_into"]]
    if merged:
        print(f"  MERGED slugs ({len(merged)}):")
        for r in merged:
            print(f"    {r['slug']} → {r['merged_into']}")

    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    inserted = 0
    errors = []

    for r in rows:
        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO slugs "
                    "(slug, topic_directory, sl_path, bpc_path, status, "
                    " merged_into, created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    [r["slug"], r["topic_directory"], r["sl_path"],
                     r["bpc_path"], r["status"], r["merged_into"],
                     ts, session, ts, session]
                )
            inserted += 1
        except sqlite3.IntegrityError as e:
            errors.append(f"  {r['slug']}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{inserted}/{len(rows)} slugs")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)

    # Validation
    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        count = conn2.execute("SELECT COUNT(*) FROM slugs").fetchone()[0]
        conn2.close()
        print(f"\nValidation: {count} rows in slugs table "
              f"({'✓ MATCH' if count == len(rows) else '✗ MISMATCH'})")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    migrate(args.source, args.session, args.dry_run)
