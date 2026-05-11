"""
scripts/migrate_db.py — Run pending migrations against guidebook.db.

Spec: architecture/sqlite-data-layer.md §7 (schema) + governance/concurrent-write-architecture-proposal-2026-05-11.md (data).

Handles BOTH migration types:

1. Schema migrations: `scripts/migrations/NNN_*.sql` (numeric prefix).
   Tracked via PRAGMA user_version. Forward-only.

2. Data migrations: `scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug}.sql`.
   Tracked via the `data_migrations` table (added by schema migration 007).
   Forward-only, append-only. Two sessions can produce data migrations with
   distinct timestamps and both land cleanly on `main` — git merges them as
   text. The DB is then rebuilt deterministically by running the runner.

Order of application:
  - All pending schema migrations (in numeric order)
  - All pending data migrations (in timestamp order)

Usage:
    python3 scripts/migrate_db.py                 # apply pending migrations
    python3 scripts/migrate_db.py --dry-run       # preview only
    python3 scripts/migrate_db.py --schema-only   # skip data migrations
    python3 scripts/migrate_db.py --rebuild       # apply ALL migrations to a fresh DB

The --rebuild option recreates the DB from scratch by applying every migration
in order. Used by CI to verify the committed `data/guidebook.db` matches what
the migration history says it should be (catches direct DB writes that bypass
the migration discipline).
"""

import argparse
import hashlib
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

MIGRATIONS_DIR = Path(os.environ.get("GUIDEBOOK_MIGRATIONS_DIR",
                                     str(Path(__file__).parent / "migrations")))
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

SCHEMA_PATTERN = re.compile(r"^(\d{3})_.*\.sql$")
DATA_PATTERN = re.compile(r"^data_(\d{14})_.*\.sql$")


def get_user_version(conn) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]


def set_user_version(conn, version: int):
    conn.execute(f"PRAGMA user_version = {version}")  # PRAGMA doesn't accept ?


def data_migrations_table_exists(conn) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='data_migrations'"
    ).fetchone()
    return row is not None


def applied_data_migrations(conn) -> set:
    if not data_migrations_table_exists(conn):
        return set()
    return {r[0] for r in conn.execute("SELECT migration_id FROM data_migrations").fetchall()}


def discover_schema_migrations() -> list:
    out = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        m = SCHEMA_PATTERN.match(path.name)
        if m:
            out.append((int(m.group(1)), path))
    return out


def discover_data_migrations() -> list:
    out = []
    for path in sorted(MIGRATIONS_DIR.glob("data_*.sql")):
        m = DATA_PATTERN.match(path.name)
        if m:
            migration_id = path.stem  # filename without .sql
            out.append((m.group(1), migration_id, path))  # (timestamp, id, path)
    out.sort(key=lambda x: x[0])
    return out


def apply_schema_migrations(conn, current_version: int, dry_run: bool) -> int:
    pending = [(v, p) for v, p in discover_schema_migrations() if v > current_version]
    if not pending:
        print(f"  Schema at version {current_version} — no pending schema migrations.")
        return current_version
    print(f"  Pending schema migrations: {len(pending)}")
    for version, mig in pending:
        sql = mig.read_text()
        print(f"    Applying {mig.name} (→ version {version})...")
        if not dry_run:
            conn.executescript(sql)
            set_user_version(conn, version)
            conn.commit()
    return pending[-1][0]


def apply_data_migrations(conn, dry_run: bool, applied_by_session: str = None) -> int:
    if not data_migrations_table_exists(conn):
        print(f"  [skip data migrations — data_migrations table not present, run schema migration 007 first]")
        return 0
    applied = applied_data_migrations(conn)
    pending = [(ts, mid, p) for ts, mid, p in discover_data_migrations() if mid not in applied]
    if not pending:
        print(f"  No pending data migrations ({len(applied)} already applied).")
        return 0
    print(f"  Pending data migrations: {len(pending)}")
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for ts, migration_id, path in pending:
        body = path.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        sql = body.decode('utf-8')
        print(f"    Applying {path.name}...")
        if not dry_run:
            # Disable FK checks during bulk load so inserts can be in any order.
            # FKs are re-validated at the end via PRAGMA foreign_key_check.
            conn.execute("PRAGMA foreign_keys = OFF")
            try:
                conn.executescript(sql)
                conn.execute(
                    "INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session) VALUES (?, ?, ?, ?)",
                    (migration_id, now, sha, applied_by_session)
                )
                conn.commit()
                # Verify FK invariants. Bootstrap migrations may carry pre-existing
                # production drift (legacy data with FK orphans); we surface but don't
                # fail. Subsequent migrations MUST not introduce new violations.
                violations = conn.execute("PRAGMA foreign_key_check").fetchall()
                is_bootstrap = "BOOTSTRAP" in (path.read_text()[:500]).upper()
                if violations:
                    label = "WARNING (bootstrap)" if is_bootstrap else "ERROR"
                    print(f"    {label}: {len(violations)} FK violations after applying {migration_id}", file=sys.stderr)
                    for v in violations[:5]:
                        print(f"      {v}", file=sys.stderr)
                    if not is_bootstrap:
                        raise sqlite3.IntegrityError(f"{len(violations)} FK violations")
            except sqlite3.Error as e:
                conn.rollback()
                print(f"    ERROR applying {migration_id}: {e}", file=sys.stderr)
                raise
            finally:
                conn.execute("PRAGMA foreign_keys = ON")
    return len(pending)


def run_migrations(dry_run: bool = False, schema_only: bool = False,
                   applied_by_session: str = None):
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    current = get_user_version(conn)
    print(f"Current schema version: {current}")

    print("\n--- Schema migrations ---")
    final_schema = apply_schema_migrations(conn, current, dry_run)

    if not schema_only:
        print("\n--- Data migrations ---")
        applied_count = apply_data_migrations(conn, dry_run, applied_by_session=applied_by_session)
    else:
        applied_count = 0
        print("\n--- Data migrations skipped (--schema-only) ---")

    conn.close()
    suffix = " [DRY-RUN]" if dry_run else ""
    print(f"\nDone.{suffix} Schema at version {final_schema}; {applied_count} data migration(s) applied.")


def rebuild_from_migrations(target_db_path: str, dry_run: bool = False):
    """Build a DB from scratch by applying every migration in order. Used by CI."""
    target = Path(target_db_path)
    if target.exists() and not dry_run:
        target.unlink()
    print(f"Rebuilding {target} from migration history...")
    conn = sqlite3.connect(str(target))
    conn.execute("PRAGMA foreign_keys=ON")

    # Apply all schema migrations from version 0
    schema_migs = discover_schema_migrations()
    print(f"  Applying {len(schema_migs)} schema migration(s)")
    for version, path in schema_migs:
        sql = path.read_text()
        if not dry_run:
            conn.executescript(sql)
            set_user_version(conn, version)
            conn.commit()

    # Apply all data migrations in timestamp order
    if data_migrations_table_exists(conn):
        data_migs = discover_data_migrations()
        print(f"  Applying {len(data_migs)} data migration(s)")
        now = datetime.now(timezone.utc).isoformat(timespec='seconds')
        for ts, migration_id, path in data_migs:
            body = path.read_bytes()
            sha = hashlib.sha256(body).hexdigest()
            sql = body.decode('utf-8')
            if not dry_run:
                conn.execute("PRAGMA foreign_keys = OFF")
                conn.executescript(sql)
                conn.execute(
                    "INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes) VALUES (?, ?, ?, ?, ?)",
                    (migration_id, now, sha, None, "rebuilt by runner")
                )
                conn.commit()
                conn.execute("PRAGMA foreign_keys = ON")
                violations = conn.execute("PRAGMA foreign_key_check").fetchall()
                is_bootstrap = "BOOTSTRAP" in (path.read_text()[:500]).upper()
                if violations:
                    label = "WARNING (bootstrap, pre-existing drift)" if is_bootstrap else "ERROR"
                    print(f"  {label}: {len(violations)} FK violations after {migration_id}", file=sys.stderr)
                    for v in violations[:5]:
                        print(f"    {v}", file=sys.stderr)
                    if not is_bootstrap:
                        sys.exit(1)

    conn.close()
    print(f"Rebuilt {target} successfully.")


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--schema-only", action="store_true",
                   help="Apply only schema migrations (skip data migrations)")
    p.add_argument("--rebuild", metavar="PATH",
                   help="Rebuild a DB from scratch at PATH by applying every migration in order")
    p.add_argument("--session", help="Tag applied_by_session in data_migrations rows")
    args = p.parse_args()

    if args.rebuild:
        rebuild_from_migrations(args.rebuild, dry_run=args.dry_run)
    else:
        run_migrations(dry_run=args.dry_run, schema_only=args.schema_only,
                       applied_by_session=args.session)


if __name__ == "__main__":
    main()
