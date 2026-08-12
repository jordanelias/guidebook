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
    """Return ordered list of (version, path) for schema migrations.

    Baseline convention (per DR-2026-05-15): if any schema migration is
    explicitly named with `baseline` in its filename (e.g., 012_baseline_*.sql),
    it supersedes all earlier-numbered schema migrations at rebuild time.
    Earlier migrations remain on disk for archaeological reference but are
    skipped during rebuild. Migrations numbered >= baseline run normally.
    """
    out = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        m = SCHEMA_PATTERN.match(path.name)
        if m:
            out.append((int(m.group(1)), path))
    baselines = [(v, p) for v, p in out if "baseline" in p.name]
    if baselines:
        baseline_version = max(v for v, _ in baselines)
        out = [(v, p) for v, p in out if v >= baseline_version]
    return out


def baseline_version() -> int | None:
    """Highest baseline version present, or None."""
    versions = []
    for path in MIGRATIONS_DIR.glob("*.sql"):
        m = SCHEMA_PATTERN.match(path.name)
        if m and "baseline" in path.name:
            versions.append(int(m.group(1)))
    return max(versions) if versions else None


def discover_data_migrations() -> list:
    """Return ordered list of (timestamp, migration_id, path) for data migrations.

    Baseline convention (per DR-2026-05-15): when a baseline schema migration
    is present, data migrations with timestamps preceding the baseline are
    skipped — the baseline already contains the data they would have loaded.
    The cutoff is encoded as `BASELINE_DATA_CUTOFF_TS`, refreshed whenever a
    new baseline is committed.
    """
    BASELINE_DATA_CUTOFF_TS = "20260515000000"  # 2026-05-15: data baked into 012_baseline
    out = []
    bv = baseline_version()
    for path in sorted(MIGRATIONS_DIR.glob("data_*.sql")):
        m = DATA_PATTERN.match(path.name)
        if m:
            ts = m.group(1)
            if bv is not None and ts < BASELINE_DATA_CUTOFF_TS:
                continue  # pre-baseline; data is in baseline already
            migration_id = path.stem
            out.append((ts, migration_id, path))
    out.sort(key=lambda x: x[0])
    return out


AFTER_DATA_PATTERN = re.compile(r"^--\s*AFTER_DATA:\s*(\d{14})\s*$", re.M)


def build_plan() -> list:
    """The faithful replay order, as a flat list of steps.

    Returns [("schema", version, path), ("data", ts, migration_id, path), ...].

    THE DEFAULT is what it has always been: every schema migration, then every
    data migration. That is right almost always, because schema precedes the
    data it shapes.

    IT IS WRONG WHENEVER A SCHEMA MIGRATION RENAMES OR DROPS SOMETHING THAT
    COMMITTED DATA MIGRATIONS STILL NAME. Data migrations are immutable, so they
    keep writing to the old name forever; a schema-phase rename runs first and
    they die on replay. Migration 025 hit this from the other side and had to
    withdraw a data migration to escape it. The 055 rename hit it from this side
    across 19 data migrations spanning two months, where withdrawal is not
    available.

    A numbered schema migration may therefore declare, on its own line:

        -- AFTER_DATA: YYYYMMDDHHMMSS

    meaning: this migration, and every migration numbered after it, applies only
    once the data migrations up to that timestamp have replayed. That is not a
    special case bolted on for one rename — it is the real chronology, which the
    numbered/timestamped split cannot otherwise express. Several markers may be
    present; each opens another data segment.
    """
    schema_migs = discover_schema_migrations()
    data_migs = discover_data_migrations()
    marks = []
    for i, (_v, path) in enumerate(schema_migs):
        m = AFTER_DATA_PATTERN.search(path.read_text(encoding="utf-8"))
        if m:
            marks.append((i, m.group(1)))

    plan, si, di = [], 0, 0
    for idx, cutoff in marks:
        plan += [("schema", v, p) for v, p in schema_migs[si:idx]]
        si = idx
        while di < len(data_migs) and data_migs[di][0] <= cutoff:
            plan.append(("data",) + data_migs[di])
            di += 1
    plan += [("schema", v, p) for v, p in schema_migs[si:]]
    plan += [("data",) + d for d in data_migs[di:]]
    return plan


def _apply_one_data_migration(conn, migration_id, path, applied_by_session):
    """Apply one data migration and record it, refusing any NEW FK violation.

    Pre-existing production drift must not fail a clean migration, so the
    violation set is compared before and after rather than merely counted.
    """
    body = path.read_bytes()
    sha = hashlib.sha256(body).hexdigest()
    pre_violations = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall())
    # Disable FK checks during bulk load so inserts can be in any order.
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.executescript(body.decode('utf-8'))
        conn.execute(
            "INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session) VALUES (?, ?, ?, ?)",
            (migration_id, datetime.now(timezone.utc).isoformat(timespec='seconds'), sha, applied_by_session)
        )
        conn.commit()
        conn.execute("PRAGMA foreign_keys = ON")
        new_violations = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall()) - pre_violations
        is_bootstrap = "BOOTSTRAP" in body[:500].decode('utf-8', errors='ignore').upper()
        if new_violations:
            label = "WARNING (bootstrap, legacy data drift)" if is_bootstrap else "ERROR"
            print(f"    {label}: {len(new_violations)} {'pre-existing' if is_bootstrap else 'new'} "
                  f"FK violations after applying {migration_id}", file=sys.stderr)
            for v in list(new_violations)[:5]:
                print(f"      {v}", file=sys.stderr)
            if not is_bootstrap:
                raise sqlite3.IntegrityError(f"{len(new_violations)} new FK violations")
    except sqlite3.Error as e:
        conn.rollback()
        conn.execute("PRAGMA foreign_keys = ON")
        print(f"    ERROR applying {migration_id}: {e}", file=sys.stderr)
        raise


def run_migrations(dry_run: bool = False, schema_only: bool = False,
                   applied_by_session: str = None):
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    current = get_user_version(conn)
    print(f"Current schema version: {current}")

    # Walk the same plan the rebuild walks, so a DB that is behind catches up in
    # the same order CI reproduces. Applying pending-schema-then-pending-data
    # here while the rebuild honours AFTER_DATA would let the two paths disagree
    # — which is precisely the divergence the reproducibility gate exists to
    # catch, and it would surface as a mystery rather than as this bug.
    plan = build_plan()
    have_dm = data_migrations_table_exists(conn)
    applied = applied_data_migrations(conn) if have_dm else set()
    final_schema, applied_count, skipped_data = current, 0, 0

    print("\n--- Migrations ---")
    for step in plan:
        if step[0] == "schema":
            _, version, path = step
            if version <= current:
                continue
            print(f"    Applying {path.name} (→ version {version})...")
            if not dry_run:
                conn.executescript(path.read_text(encoding="utf-8"))
                if "baseline" not in path.name:
                    set_user_version(conn, version)
                conn.commit()
            final_schema = version
            continue

        _, _ts, migration_id, path = step
        if schema_only:
            # Everything after a data step may be gated behind it (AFTER_DATA),
            # so --schema-only stops here rather than applying a later schema
            # migration out of order and leaving user_version claiming a schema
            # the DB does not have. With no AFTER_DATA marker every data step is
            # already at the tail, so this is the old behaviour exactly.
            skipped_data = sum(1 for s in plan[plan.index(step):] if s[0] == "data")
            gated_schema = sum(1 for s in plan[plan.index(step):] if s[0] == "schema")
            if gated_schema:
                print(f"  [--schema-only stops here: {gated_schema} schema migration(s) are "
                      f"gated behind data migrations by AFTER_DATA. Run without --schema-only.]")
            break
        if not have_dm:
            have_dm = data_migrations_table_exists(conn)
            if not have_dm:
                print("  [skip data migration — data_migrations table not present yet]")
                continue
            applied = applied_data_migrations(conn)
        if migration_id in applied:
            continue
        print(f"    Applying {path.name}...")
        if not dry_run:
            _apply_one_data_migration(conn, migration_id, path, applied_by_session)
        applied_count += 1

    if schema_only:
        print(f"\n--- {skipped_data} data migration(s) skipped (--schema-only) ---")

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

    # Replay in the faithful order, which is schema-then-data except where a
    # migration declares AFTER_DATA (see build_plan).
    plan = build_plan()
    n_schema = sum(1 for s in plan if s[0] == "schema")
    n_data = len(plan) - n_schema
    print(f"  Applying {n_schema} schema migration(s) and {n_data} data migration(s)")
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for step in plan:
        if step[0] == "schema":
            _, version, path = step
            sql = path.read_text(encoding="utf-8")
            if not dry_run:
                conn.executescript(sql)
                # Baselines set their own PRAGMA user_version inside the script;
                # honor it. Non-baseline migrations follow the filename-number rule.
                if "baseline" not in path.name:
                    set_user_version(conn, version)
                conn.commit()
            continue

        _, ts, migration_id, path = step
        if not data_migrations_table_exists(conn):
            continue  # pre-007: nothing to record against
        body = path.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        sql = body.decode('utf-8')
        if not dry_run:
            pre_violations = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall())
            conn.execute("PRAGMA foreign_keys = OFF")
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes) VALUES (?, ?, ?, ?, ?)",
                (migration_id, now, sha, None, "rebuilt by runner")
            )
            conn.commit()
            conn.execute("PRAGMA foreign_keys = ON")
            post_violations = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall())
            new_violations = post_violations - pre_violations
            is_bootstrap = "BOOTSTRAP" in body[:500].decode('utf-8', errors='ignore').upper()
            if new_violations:
                label = "WARNING (bootstrap, legacy data drift)" if is_bootstrap else "ERROR"
                print(f"  {label}: {len(new_violations)} FK violations after {migration_id}", file=sys.stderr)
                for v in list(new_violations)[:5]:
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
