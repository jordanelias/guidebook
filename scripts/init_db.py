"""
scripts/init_db.py — Initialize the guidebook SQLite database.

Creates data/guidebook.db, runs migration 001, seeds db_meta, sets PRAGMA user_version = 1.
Spec: architecture/sqlite-data-layer.md §9 Phase 1-A

Usage:
    python3 scripts/init_db.py
    python3 scripts/init_db.py --force   # overwrite existing DB
"""

import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def init_db(force: bool = False):
    if DB_PATH.exists() and not force:
        print(f"ERROR: {DB_PATH} already exists. Use --force to overwrite.",
              file=sys.stderr)
        sys.exit(1)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists() and force:
        DB_PATH.unlink()
        print(f"Removed existing {DB_PATH}.")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    # Run 001_initial_schema.sql
    schema_file = MIGRATIONS_DIR / "001_initial_schema.sql"
    if not schema_file.exists():
        print(f"ERROR: {schema_file} not found.", file=sys.stderr)
        conn.close()
        sys.exit(1)

    sql = schema_file.read_text()
    print(f"Applying {schema_file.name}...")
    conn.executescript(sql)

    # Seed db_meta
    ts = now_utc()
    conn.executemany(
        "INSERT INTO db_meta (key, value) VALUES (?, ?)",
        [
            ("schema_version", "1"),
            ("created_at", ts),
            ("project", "jordanelias/guidebook"),
        ],
    )

    # Set PRAGMA user_version
    conn.execute("PRAGMA user_version = 1")
    conn.commit()

    # Verify
    ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    uv = conn.execute("PRAGMA user_version").fetchone()[0]

    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    ]

    conn.close()

    print(f"\nInitialized {DB_PATH}")
    print(f"  PRAGMA integrity_check: {ic}")
    print(f"  PRAGMA foreign_key_check: {len(fk)} violations")
    print(f"  PRAGMA user_version: {uv}")
    print(f"  Tables ({len(tables)}): {', '.join(tables)}")
    print(f"  db_meta.created_at: {ts}")

    if ic != "ok" or len(fk) > 0:
        print("\nERROR: Integrity checks failed.", file=sys.stderr)
        sys.exit(1)

    print("\nDatabase ready.")


if __name__ == "__main__":
    force = "--force" in sys.argv
    init_db(force=force)
