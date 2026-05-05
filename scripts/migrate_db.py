"""
scripts/migrate_db.py — Run pending schema migrations against guidebook.db.

Spec: architecture/sqlite-data-layer.md §7

Usage:
    python3 scripts/migrate_db.py            # apply pending migrations
    python3 scripts/migrate_db.py --dry-run  # preview only
"""

import os
import sqlite3
import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def get_user_version(conn) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]


def set_user_version(conn, version: int):
    conn.execute(f"PRAGMA user_version = {version}")


def run_migrations(dry_run: bool = False):
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    current = get_user_version(conn)
    print(f"Current schema version: {current}")

    migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
    pending = [m for m in migrations if int(m.stem.split("_")[0]) > current]

    if not pending:
        print(f"Schema at version {current} — no pending migrations.")
        conn.close()
        return

    print(f"Pending migrations: {len(pending)}")

    for mig in pending:
        version = int(mig.stem.split("_")[0])
        sql = mig.read_text()
        print(f"  Applying migration {mig.name} (→ version {version})...")
        if not dry_run:
            conn.executescript(sql)
            set_user_version(conn, version)
            conn.commit()
            print(f"    Applied.")
        else:
            print(f"    [DRY-RUN] Would apply {len(sql)} chars of SQL")

    final_version = max(int(m.stem.split("_")[0]) for m in pending)
    conn.close()

    if dry_run:
        print(f"[DRY-RUN] Would migrate to version {final_version}.")
    else:
        print(f"Schema migrated to version {final_version}.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run_migrations(dry_run=dry_run)
