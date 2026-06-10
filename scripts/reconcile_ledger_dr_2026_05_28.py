#!/usr/bin/env python3
"""One-shot, idempotent migration-ledger reconciliation (DR-2026-05-28).

Background
----------
The committed `data/guidebook.db` already contains every post-cutoff data
effect (the CI reproducibility gate in .github/workflows/audit.yml confirms the
seven entity invariants match a fresh `--rebuild`). What drifted is the
`data_migrations` *ledger*: a number of migrations were applied out-of-band and
either recorded under ad-hoc slugs the runner cannot match, or not recorded at
all. As a result `scripts/migrate_db.py --dry-run` reports a large pending set
against a DB whose data is in fact already present.

This script corrects the ledger to reflect reality, WITHOUT re-executing any
migration SQL (doing so would double-insert rows). For every migration the
runner would consider pending, it inserts a ledger row whose `content_sha`
matches exactly what the runner computes (sha256 of the file body), so a future
rebuild's recorded shas line up.

It deliberately does NOT touch any entity table. The only writes are:
  1. INSERTs into `data_migrations` (ledger rows for the pending set).
  2. `db_meta.schema_version` aligned to PRAGMA user_version (per workplan 1.3).

Idempotent: the pending set is computed via the runner's own functions, which
already exclude applied ids; a second guard skips any id present in the ledger.
Re-running after a successful run is a no-op.

Usage
-----
    GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/reconcile_ledger_dr_2026_05_28.py --dry-run
    GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/reconcile_ledger_dr_2026_05_28.py

Run once against the authoritative DB. Safe to re-run.
"""

import argparse
import hashlib
import sqlite3
import sys
from datetime import datetime, timezone

# Reuse the runner's own discovery so the pending set is provably identical.
import migrate_db

SESSION_TAG = "reconcile-ledger-DR-2026-05-28"
NOTES = ("reconciliation backfill per DR-2026-05-28: applied out-of-band, "
         "ledger corrected (data already present in committed DB; "
         "ledger-only insert, migration SQL not re-executed)")


def reconcile(dry_run: bool) -> int:
    db_path = migrate_db.DB_PATH
    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(str(db_path))

    if not migrate_db.data_migrations_table_exists(conn):
        print("ERROR: data_migrations table absent — run schema migration 007 first.",
              file=sys.stderr)
        conn.close()
        return 2

    applied = migrate_db.applied_data_migrations(conn)
    discovered = migrate_db.discover_data_migrations()
    pending = [(ts, mid, p) for ts, mid, p in discovered if mid not in applied]

    print(f"  Ledger rows currently applied: {len(applied)}")
    print(f"  Data migrations discovered:    {len(discovered)}")
    print(f"  Pending (to be backfilled):    {len(pending)}")

    # schema_version alignment
    user_version = migrate_db.get_user_version(conn)
    sv_row = conn.execute("SELECT value FROM db_meta WHERE key='schema_version'").fetchone()
    current_sv = sv_row[0] if sv_row else None
    sv_needs_fix = str(current_sv) != str(user_version)
    if sv_needs_fix:
        print(f"  db_meta.schema_version {current_sv!r} -> {user_version} (align to user_version)")
    else:
        print(f"  db_meta.schema_version already aligned at {current_sv!r}")

    if dry_run:
        if pending:
            print("  [DRY-RUN] would insert the following ledger rows:")
            for ts, mid, _ in pending:
                print(f"    + {mid}")
        print(f"  [DRY-RUN] no writes performed. pending={len(pending)} "
              f"schema_version_fix={'yes' if sv_needs_fix else 'no'}")
        conn.close()
        return 0

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    inserted = 0
    for ts, migration_id, path in pending:
        # Second idempotency guard (belt and suspenders vs. the pending filter).
        exists = conn.execute(
            "SELECT 1 FROM data_migrations WHERE migration_id = ?", (migration_id,)
        ).fetchone()
        if exists:
            continue
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        conn.execute(
            "INSERT INTO data_migrations (migration_id, applied_at, content_sha, "
            "applied_by_session, notes) VALUES (?, ?, ?, ?, ?)",
            (migration_id, now, sha, SESSION_TAG, NOTES),
        )
        inserted += 1

    if sv_needs_fix:
        if sv_row is None:
            conn.execute(
                "INSERT INTO db_meta (key, value) VALUES ('schema_version', ?)",
                (str(user_version),),
            )
        else:
            conn.execute(
                "UPDATE db_meta SET value = ? WHERE key = 'schema_version'",
                (str(user_version),),
            )

    conn.commit()
    final = conn.execute("SELECT COUNT(*) FROM data_migrations").fetchone()[0]
    print(f"  Inserted {inserted} ledger row(s). data_migrations now holds {final} row(s).")
    if sv_needs_fix:
        print(f"  db_meta.schema_version set to {user_version}.")
    conn.close()
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change; perform no writes.")
    args = p.parse_args()
    sys.exit(reconcile(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
