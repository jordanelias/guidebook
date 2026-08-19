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


_TXN_CTL = re.compile(
    r"^\s*(BEGIN(\s+(DEFERRED|IMMEDIATE|EXCLUSIVE))?(\s+TRANSACTION)?"
    r"|COMMIT(\s+TRANSACTION)?|END(\s+TRANSACTION)?)\s*;?\s*$", re.I)
_PRAGMA_FK = re.compile(r"^\s*PRAGMA\s+foreign_keys\s*=", re.I)
_PRAGMA_UV = re.compile(r"^\s*PRAGMA\s+user_version\s*=\s*(\d+)", re.I)
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def _split_statements(sql: str) -> list:
    """Split a migration body into individual statements.

    Uses sqlite3.complete_statement, which is quote-, comment- and
    CREATE TRIGGER-aware: a semicolon inside a string literal, inside a comment,
    or inside a trigger body does not end a statement. A naive split(';') would
    desync on a source title containing a semicolon, which this corpus can carry.
    """
    out, buf = [], ""
    for line in sql.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            if buf.strip():
                out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return out


def _code_of(chunk: str) -> str:
    """The chunk with comments removed, for CLASSIFICATION only.

    A statement is buffered together with any comment lines preceding it -- a
    comment is not a complete statement, so it accumulates until real SQL closes
    the chunk. Every migration in this repository opens with a comment header,
    so the first chunk of a wrapped file is literally
    "-- Generated: ...\nBEGIN TRANSACTION;". Matching the raw chunk against
    ^BEGIN therefore fails and the wrapper survives, which is how the runner
    ended up starting a transaction inside a transaction. Classify on this;
    execute the original, where the comments are harmless.
    """
    text = _BLOCK_COMMENT.sub("", chunk)
    return "\n".join(l for l in text.splitlines()
                      if l.strip() and not l.strip().startswith("--")).strip()


def _is_noop(chunk: str) -> bool:
    """True if the chunk is only comments/whitespace and must not be executed."""
    return not _code_of(chunk).strip(";").strip()


def _prepare_body(sql: str):
    """Return (statements, declared_user_version) with the runner owning control.

    Three classes of statement are removed from the body, because the runner
    must own them rather than the file (DR-2026-08-19 §12.0, F5/F6):

    * Transaction control. A file carrying its own BEGIN/COMMIT commits itself
      mid-run, which is exactly how a data migration's body could commit while
      its `data_migrations` ledger row rolled back. The five already-committed
      data migrations are immutable and carry the wrapper, so it is stripped
      here rather than edited there.
    * PRAGMA foreign_keys. It is a SILENT NO-OP inside a transaction, so a body
      that disables FK enforcement for a bulk load would not actually do so once
      wrapped. It is hoisted and re-issued in autocommit, before BEGIN.
    * PRAGMA user_version. Returned to the caller so it is stamped INSIDE the
      transaction; it lives in the database header and is fully transactional,
      so DDL and version stamp commit or vanish together.
    """
    statements, declared_uv = [], None
    for st in _split_statements(sql):
        code = _code_of(st)
        if not code.strip(";").strip() or _TXN_CTL.match(code):
            continue
        if _PRAGMA_FK.match(code):
            continue
        m = _PRAGMA_UV.match(code)
        if m:
            declared_uv = int(m.group(1))
            continue
        statements.append(st)
    return statements, declared_uv


def _apply_atomically(conn, statements, *, label, ledger=None, user_version=None,
                      fk_blocking=True, is_bootstrap=False):
    """Apply one migration so body, FK verdict, ledger row and version stamp are
    one atomic unit.

    The ordering is the point (DR-2026-08-19 §12.0, F5/F6). Previously the body
    committed, THEN the FK check ran, so a "rolled back" FK failure left the bad
    data committed and discarded only the ledger row.

      1. PRAGMA foreign_keys=OFF     -- in autocommit, so it takes effect
      2. snapshot foreign_key_check  -- pre-existing drift must not fail a clean run
      3. BEGIN IMMEDIATE
      4. body statements
      5. re-check; ROLLBACK on any NEW violation
      6. ledger INSERT and/or user_version stamp -- same transaction
      7. COMMIT                      -- all of it becomes visible together
      8. PRAGMA foreign_keys=ON

    Requires a connection opened with isolation_level=None; step 1 is a silent
    no-op otherwise.
    """
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        pre = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall())
        conn.execute("BEGIN IMMEDIATE")
        try:
            for st in statements:
                conn.execute(st)
            new = set(tuple(r) for r in conn.execute(
                "PRAGMA foreign_key_check").fetchall()) - pre
            if new and fk_blocking and not is_bootstrap:
                conn.execute("ROLLBACK")
                print(f"    ERROR: {len(new)} new FK violations after {label} "
                      f"— ROLLED BACK, nothing committed", file=sys.stderr)
                for v in list(new)[:5]:
                    print(f"      {v}", file=sys.stderr)
                raise sqlite3.IntegrityError(f"{len(new)} new FK violations in {label}")
            if user_version is not None:
                set_user_version(conn, user_version)
            if ledger is not None:
                conn.execute(ledger[0], ledger[1])
            conn.execute("COMMIT")
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        if new:
            label_txt = ("WARNING (bootstrap, legacy data drift)" if is_bootstrap
                         else "WARNING (advisory)")
            print(f"    {label_txt}: {len(new)} FK violations after {label}",
                  file=sys.stderr)
            for v in list(new)[:5]:
                print(f"      {v}", file=sys.stderr)
        return new
    finally:
        conn.execute("PRAGMA foreign_keys = ON")


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
    # 2026-08-12: 057_baseline_2026-08-12.sql bakes in the FULL schema and data, and
    # every earlier migration is frozen at _archived/scripts/migrations/. The cutoff
    # sits past the last archived data migration (20260812083254) so nothing
    # pre-baseline is looked for. It stays as a guard rather than being deleted: if a
    # pre-baseline file is ever restored to this directory by mistake, it is skipped
    # instead of replayed on top of a database that already contains its effect.
    BASELINE_DATA_CUTOFF_TS = "20260812083255"
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
    Body and ledger row now commit as one unit -- see _apply_atomically.
    """
    body = path.read_bytes()
    sha = hashlib.sha256(body).hexdigest()
    text = body.decode('utf-8')
    statements, _uv = _prepare_body(text)
    is_bootstrap = "BOOTSTRAP" in text[:500].upper()
    ledger = (
        "INSERT INTO data_migrations (migration_id, applied_at, content_sha,"
        " applied_by_session) VALUES (?, ?, ?, ?)",
        (migration_id, datetime.now(timezone.utc).isoformat(timespec='seconds'),
         sha, applied_by_session),
    )
    try:
        _apply_atomically(conn, statements, label=migration_id, ledger=ledger,
                          fk_blocking=True, is_bootstrap=is_bootstrap)
    except sqlite3.Error as e:
        print(f"    ERROR applying {migration_id}: {e}", file=sys.stderr)
        raise


def run_migrations(dry_run: bool = False, schema_only: bool = False,
                   applied_by_session: str = None):
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    # isolation_level=None -- true autocommit. Without it, PRAGMA foreign_keys
    # is issued inside an implicit transaction and silently does nothing.
    conn = sqlite3.connect(str(DB_PATH), isolation_level=None)
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
                stmts, declared_uv = _prepare_body(path.read_text(encoding="utf-8"))
                # Baselines declare their own user_version inside the script;
                # honour it. Non-baseline migrations follow the filename number.
                stamp = declared_uv if "baseline" in path.name else version
                # Advisory only on the schema path: adding a blocking referential
                # gate here is OD-7/D7, a separate owner decision, not this fix.
                _apply_atomically(conn, stmts, label=path.name,
                                  user_version=stamp, fk_blocking=False)
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
    conn = sqlite3.connect(str(target), isolation_level=None)
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
            if not dry_run:
                stmts, declared_uv = _prepare_body(path.read_text(encoding="utf-8"))
                stamp = declared_uv if "baseline" in path.name else version
                _apply_atomically(conn, stmts, label=path.name,
                                  user_version=stamp, fk_blocking=False)
            continue

        _, ts, migration_id, path = step
        if not data_migrations_table_exists(conn):
            continue  # pre-007: nothing to record against
        body = path.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        text = body.decode('utf-8')
        if not dry_run:
            statements, _uv = _prepare_body(text)
            is_bootstrap = "BOOTSTRAP" in text[:500].upper()
            ledger = (
                "INSERT INTO data_migrations (migration_id, applied_at, content_sha,"
                " applied_by_session, notes) VALUES (?, ?, ?, ?, ?)",
                (migration_id, now, sha, None, "rebuilt by runner"),
            )
            try:
                _apply_atomically(conn, statements, label=migration_id, ledger=ledger,
                                  fk_blocking=True, is_bootstrap=is_bootstrap)
            except sqlite3.Error as e:
                print(f"  ERROR applying {migration_id}: {e}", file=sys.stderr)
                sys.exit(1)

    conn.close()
    print(f"Rebuilt {target} successfully.")


def selftest() -> int:
    """Prove the transaction properties F5/F6 assert, rather than asserting them.

    Each case states the defect it pins. Run: python3 scripts/migrate_db.py --selftest
    """
    import tempfile
    global MIGRATIONS_DIR, DB_PATH
    results, failures = [], 0

    def check(name, cond, detail=""):
        nonlocal failures
        results.append((name, bool(cond), detail))
        if not cond:
            failures += 1

    seq = [0]

    def fresh(tmp):
        seq[0] += 1
        db = Path(tmp) / f"t{seq[0]}.db"
        c = sqlite3.connect(str(db), isolation_level=None)
        c.execute("CREATE TABLE parent (id TEXT PRIMARY KEY)")
        c.execute("CREATE TABLE child (id TEXT PRIMARY KEY, "
                  "pid TEXT REFERENCES parent(id))")
        c.execute("CREATE TABLE data_migrations (migration_id TEXT PRIMARY KEY, "
                  "applied_at TEXT, content_sha TEXT, applied_by_session TEXT, notes TEXT)")
        c.execute("INSERT INTO parent VALUES ('P1')")
        return c

    with tempfile.TemporaryDirectory() as tmp:
        # --- F5: a body that violates FK must leave NOTHING behind -------------
        c = fresh(tmp)
        body = ("-- Generated: test\n"
                "BEGIN TRANSACTION;\n"
                "INSERT INTO child VALUES ('C1','P1');\n"
                "INSERT INTO child VALUES ('C2','GHOST');\n"
                "COMMIT;\n")
        stmts, _ = _prepare_body(body)
        ledger = ("INSERT INTO data_migrations (migration_id, applied_at, content_sha,"
                  " applied_by_session) VALUES (?, ?, ?, ?)", ("m1", "now", "sha", None))
        raised = False
        try:
            _apply_atomically(c, stmts, label="m1", ledger=ledger, fk_blocking=True)
        except sqlite3.IntegrityError:
            raised = True
        rows = c.execute("SELECT COUNT(*) FROM child").fetchone()[0]
        led = c.execute("SELECT COUNT(*) FROM data_migrations").fetchone()[0]
        check("F5 FK violation raises", raised)
        check("F5 body rolled back (the defect: this used to be 2)", rows == 0,
              f"child rows = {rows}")
        check("F5 ledger row rolled back", led == 0, f"ledger rows = {led}")
        check("F5 foreign_keys restored", c.execute("PRAGMA foreign_keys").fetchone()[0] == 1)
        c.close()

        # --- F5: a clean body commits body AND ledger together -----------------
        c = fresh(tmp)
        stmts, _ = _prepare_body("BEGIN TRANSACTION;\n"
                                 "INSERT INTO child VALUES ('C1','P1');\nCOMMIT;\n")
        _apply_atomically(c, stmts, label="m2", ledger=ledger, fk_blocking=True)
        check("F5 clean body commits", c.execute("SELECT COUNT(*) FROM child").fetchone()[0] == 1)
        check("F5 clean ledger commits",
              c.execute("SELECT COUNT(*) FROM data_migrations").fetchone()[0] == 1)
        c.close()

        # --- F6: the file's own BEGIN/COMMIT is stripped, not nested -----------
        stmts, _ = _prepare_body("-- header comment\nBEGIN TRANSACTION;\n"
                                 "INSERT INTO child VALUES ('C9','P1');\nCOMMIT;\n")
        check("F6 wrapper stripped past the comment header",
              not any(_TXN_CTL.match(_code_of(s)) for s in stmts),
              f"statements = {stmts}")

        # --- F6: PRAGMA foreign_keys is hoisted out of the body ----------------
        c = fresh(tmp)
        stmts, _ = _prepare_body("PRAGMA foreign_keys = OFF;\n"
                                 "INSERT INTO child VALUES ('C1','P2');\n"
                                 "INSERT INTO parent VALUES ('P2');\n"
                                 "PRAGMA foreign_keys = ON;\n")
        check("F6 fk pragmas hoisted out of body",
              not any(_PRAGMA_FK.match(_code_of(s)) for s in stmts))
        _apply_atomically(c, stmts, label="m3", fk_blocking=True)
        check("F6 out-of-order bulk load succeeds (pragma honoured in autocommit)",
              c.execute("SELECT COUNT(*) FROM child").fetchone()[0] == 1)
        c.close()

        # --- F6: user_version stamp is atomic with the DDL ---------------------
        c = fresh(tmp)
        stmts, uv = _prepare_body("PRAGMA user_version = 42;\n"
                                  "CREATE TABLE ok (x);\n"
                                  "INSERT INTO child VALUES ('C3','GHOST');\n")
        check("F6 declared user_version captured", uv == 42, f"uv = {uv}")
        try:
            _apply_atomically(c, stmts, label="m4", user_version=uv, fk_blocking=True)
        except sqlite3.IntegrityError:
            pass
        check("F6 user_version rolled back with the DDL",
              c.execute("PRAGMA user_version").fetchone()[0] == 0,
              f"user_version = {c.execute('PRAGMA user_version').fetchone()[0]}")
        check("F6 DDL rolled back too",
              c.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='ok'").fetchone()[0] == 0)
        c.close()

        # --- splitter: a semicolon inside a string must not desync -------------
        stmts = _split_statements("INSERT INTO t VALUES ('a;b');\nINSERT INTO t VALUES (2);\n")
        check("splitter is quote-aware", len(stmts) == 2, f"got {len(stmts)}: {stmts}")
        stmts, _ = _prepare_body("-- only a comment\n")
        check("comment-only body yields no statements", stmts == [], f"got {stmts}")

    print("\n--- migrate_db selftest ---")
    for name, ok, detail in results:
        print(f"  {'PASS' if ok else '**FAIL**'}: {name}" + (f"  [{detail}]" if not ok else ""))
    print(f"\nRESULTS: {len(results) - failures}/{len(results)} selftest cases pass")
    if failures:
        print("SELFTEST: FAIL")
        return 1
    print("SELFTEST: PASS")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--schema-only", action="store_true",
                   help="Apply only schema migrations (skip data migrations)")
    p.add_argument("--rebuild", metavar="PATH",
                   help="Rebuild a DB from scratch at PATH by applying every migration in order")
    p.add_argument("--session", help="Tag applied_by_session in data_migrations rows")
    p.add_argument("--selftest", action="store_true",
                   help="Prove the F5/F6 transaction properties and exit")
    args = p.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if args.rebuild:
        rebuild_from_migrations(args.rebuild, dry_run=args.dry_run)
    else:
        run_migrations(dry_run=args.dry_run, schema_only=args.schema_only,
                       applied_by_session=args.session)


if __name__ == "__main__":
    main()
