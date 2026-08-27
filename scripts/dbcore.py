#!/usr/bin/env python3
"""scripts/dbcore.py — the one place this repository opens, stamps and keys the database.

WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live
files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37+ files computing their own
repo root -- while `scripts/db.py` already held a correct connect() that NOTHING IMPORTED.
Every lesson that connect() had learned (read-only URI, query_only, the journal_mode trap
below) was therefore un-inherited by 55 files. Owner directive 2026-08-25: "we only need one
set of tools that manages how to write to a table, read a table, and cross-reference them."

WHAT BELONGS HERE: mechanics. Connection, paths, audit stamps, the case-folded join keys, the
reference-id rules, and the one list of tables a session may write.

WHAT DELIBERATELY DOES NOT, each for a reason that outlives this docstring:
  * schemas/*.py Pydantic mirrors -- "schema drift is a bug, not a convention" (CLAUDE.md §8)
    only works while the mirror is independent of the thing it mirrors.
  * scripts/research/retrieval_log.py -- its whole value is being OUTSIDE the write path.
    `--verify-authors` diffs stored rows against the bytes actually received; a writer that
    verifies itself verifies nothing.
  * Check and audit SQL -- a gate that imports the library it polices fails together with it.
    Rule 5 forbids two STORED homes of a fact, not two independent COMPUTATIONS of it;
    re-derivation is precisely what a gate is for.
  * emit_data_migration.py / migrate_db.py internals -- the sanctioned write pair works.
  * Query/business logic -- that stays in db.py. This module is mechanics, not model.

IMPORTING IT. Consumers need one preamble, because you cannot import a shared module without
first locating it:

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[N] / "scripts"))
    import dbcore

That relative hop is the one piece of boilerplate consolidation cannot remove. It replaces
3-6 lines of per-file path/root/connect duplication and is identical everywhere but `N`.
"""

import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — one resolution each, and no other module should compute these.
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]


def db_path() -> Path:
    """The database this process should use.

    Resolved at CALL time, not import time. The research runbook points
    GUIDEBOOK_DB_PATH at a scratch copy inline on every invocation because the
    harness resets env between shells; a module-level constant captured at import
    would silently ignore that and write the canonical file.
    """
    return Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO_ROOT / "data" / "guidebook.db")))


CANONICAL_DB = REPO_ROOT / "data" / "guidebook.db"


def is_canonical(path=None) -> bool:
    """True when the given path IS the committed database.

    Callers that must never touch the canonical file (CLAUDE.md rule 3: migrations
    only) use this to refuse, rather than trusting that GUIDEBOOK_DB_PATH was set.
    """
    p = Path(path) if path is not None else db_path()
    try:
        return p.resolve() == CANONICAL_DB.resolve()
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

@contextmanager
def connect(dry_run: bool = False, readonly: bool = False, path=None):
    """Open the database at GUIDEBOOK_DB_PATH (or `path`).

    `readonly=True` opens the file with URI mode=ro and sets PRAGMA query_only,
    so a read cannot write. Every caller that only SELECTs passes it.

    PRAGMA journal_mode is deliberately NOT set here. journal_mode is persisted
    in the database header, so setting it rewrote the committed blob on EVERY
    invocation of this module -- including pure reads and including --dry-run.
    That made `git status` dirty after a query and defeated the sha256 check
    the research runbook uses to prove the canonical database was untouched.
    The default (delete) is what the committed file already carries.
    """
    target = Path(path) if path is not None else db_path()
    if not readonly and is_canonical(target):
        # CLAUDE.md rule 3: the canonical database is written by migrations only.
        # is_canonical() existed solely to enforce this and had no caller but its own
        # selftest until 2026-08-27, while db_path() defaults to canonical when
        # GUIDEBOOK_DB_PATH is unset -- so a script that forgot the variable wrote the
        # committed file. This is the wiring.
        #
        # NO OVERRIDE, deliberately. migrate_db.py opens the database with raw
        # sqlite3.connect and never imports this module, so migrations do not pass
        # through here and need nothing unblocked. Every db.py write is required by the
        # runbook to target a scratch copy. There is no legitimate canonical write on
        # this path to permit, and a bypass that exists will be used.
        #
        # dry_run is refused too, not just committing writes: it still opens the
        # committed blob read-write, and this file already records an incident of that
        # exact class -- PRAGMA journal_mode "rewrote the committed blob on EVERY
        # invocation ... including pure reads and including --dry-run".
        raise RuntimeError(
            "dbcore.connect: refusing to open the CANONICAL database read-write "
            f"({target}). CLAUDE.md rule 3 -- migrations only. Copy it and point "
            "GUIDEBOOK_DB_PATH at the copy:\n"
            "    cp data/guidebook.db $SCRATCH/guidebook.db\n"
            "    GUIDEBOOK_DB_PATH=$SCRATCH/guidebook.db python3 scripts/db.py ...\n"
            "Then ship the delta with scripts/research/emit_batch_sql.py -> "
            "emit_data_migration.py -> migrate_db.py. To READ canonical, pass readonly=True."
        )
    if readonly:
        conn = sqlite3.connect(f"file:{target}?mode=ro", uri=True, timeout=10)
    else:
        conn = sqlite3.connect(str(target), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    if readonly:
        # After foreign_keys: query_only blocks further schema-affecting pragmas.
        conn.execute("PRAGMA query_only=ON")
    else:
        conn.execute("PRAGMA synchronous=NORMAL")
    try:
        yield conn
        if readonly:
            pass          # nothing to commit; mode=ro would refuse anyway
        elif not dry_run:
            conn.commit()
        else:
            conn.rollback()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Audit stamps
# ---------------------------------------------------------------------------

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def audit(session: str) -> dict:
    ts = now()
    return {
        "created_at": ts, "created_by_session": session,
        "updated_at": ts, "updated_by_session": session,
    }


def upd(session: str) -> dict:
    return {"updated_at": now(), "updated_by_session": session}


def validate_cols(data_keys, whitelist: frozenset, context: str):
    unknown = set(data_keys) - whitelist
    if unknown:
        raise ValueError(
            f"{context}: unknown column(s) {unknown}. "
            f"Permitted: {whitelist}"
        )


# ---------------------------------------------------------------------------
# Join keys — case-folded, because plain equality has already failed here
# ---------------------------------------------------------------------------

def norm_doi(doi):
    """Canonical form for DOI comparison and storage.

    `10.1044/2019_AJA-19-0010` and `10.1044/2019_aja-19-0010` are the SAME DOI and
    were stored as two, in citation_mining against evidence_sources. Case-folded
    they match; to `=` they do not. Any join written with plain equality on a DOI
    is a defect waiting for its second row.
    """
    return None if doi is None else doi.strip().lower()


def fold_ref(ref_id):
    """Canonical form for reference-id comparison. Ids are upper-case by convention."""
    return None if ref_id is None else ref_id.strip().upper()


# REF-NNNNN is the global id. REF-VERIFIED-NNN are human-verified standards predating
# the DOI pipeline; Co1-NN are lived-experience records (schemas/evidence_source.py).
# Both are RECOGNISED but never MINTED -- they are closed namespaces.
REF_ID_SHAPE = re.compile(r"REF-\d{5}|REF-VERIFIED-\d{3}|Co1-\d{2,3}")

_MINTABLE = re.compile(r"REF-(\d{5})")

# Tables that hold a global reference id and therefore constrain the mint.
#
# DERIVED FROM THE SCHEMA, NEVER LISTED HERE. This was a hardcoded pair
# ("source_locators", "evidence_sources") until 2026-08-27. Two defects, and the
# second is the dangerous one:
#
#   (1) rule 5 -- a list in code is a second home for a fact the schema already
#       states. Any new table carrying a ref_id was silently outside the mint.
#   (2) the loop swallowed OperationalError with `continue`, so after a table
#       RENAME every home vanished, high water fell to 0, and next_ref_id minted
#       REF-00001 -- on top of live data, with no error. A silent wrong answer,
#       which is worse than a crash. Found by adversarial audit before the rename
#       that would have triggered it.
#
# The schema is the single home: any table with a `ref_id` column constrains the mint.
def ref_id_homes(conn) -> tuple:
    """Every table carrying a `ref_id` column, read from the schema."""
    homes = []
    for (name,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ):
        cols = [r[1] for r in conn.execute('PRAGMA table_info("%s")' % name)]
        if "ref_id" in cols:
            homes.append(name)
    return tuple(sorted(homes))


def ref_id_high_water(conn) -> int:
    """Highest minted REF-NNNNN across EVERY table that holds one.

    CLAUDE.md said for weeks: "mint above the source_locators high-water mark."
    That was INCOMPLETE and would have collided. Measured 2026-08-25:
        source_locators  max REF-00964
        evidence_sources max REF-00970
    Minting at 965 -- exactly what the documented rule produced -- lands on a live
    evidence row. The high-water mark is the UNION, and this function is that rule.

    REFUSES rather than guessing: a database with no ref_id column at all means the
    caller is pointed somewhere unexpected, and returning 0 would mint onto live rows.
    """
    homes = ref_id_homes(conn)
    if not homes:
        raise RuntimeError(
            "ref_id_high_water: no table in this database carries a `ref_id` column. "
            "Refusing to return a high-water mark of 0, which would mint REF-00001 "
            "onto live data. Check GUIDEBOOK_DB_PATH points at the intended database."
        )
    high = 0
    for table in homes:
        for (ref,) in conn.execute(
            'SELECT ref_id FROM "%s" WHERE ref_id IS NOT NULL' % table
        ):
            m = _MINTABLE.fullmatch((ref or "").strip())
            if m:
                high = max(high, int(m.group(1)))
    return high


def next_ref_id(conn) -> str:
    """The next free global reference id.

    COMPUTED, NEVER STORED. A counter table or a `last_ref_id` column would be a
    second home for a fact the reference-id columns already jointly state, which is
    the copy rule 5 forbids. There is no allocator and there should not be one.
    """
    return "REF-%05d" % (ref_id_high_water(conn) + 1)


# ---------------------------------------------------------------------------
# Refusal helpers — the CLI's value is that it REFUSES, and a refusal is only
# trustworthy if its vocabulary is the live one.
# ---------------------------------------------------------------------------

def columns(conn, table: str) -> list:
    """The table's real column names, read from the live schema."""
    return [r[1] for r in conn.execute('PRAGMA table_info("%s")' % table)]


def stamp_for(conn, table: str, session: str) -> dict:
    """Audit columns THIS table actually has, filled in.

    NOT every table carries created_at/created_by_session. `source_locators` carries
    NEITHER -- it is a pre-reset stash whose rows predate the audit convention. A
    writer that assumes the stamp is universal fails at INSERT with "table X has no
    column named created_at", which is how this function came to exist: the Act-2
    rehearsal refused all 8 writes for exactly that reason, and the refusal was mine,
    not the data's.

    Derive from the schema; never assume the convention holds.
    """
    have = set(columns(conn, table))
    return {k: v for k, v in audit(session).items() if k in have}


def exists(conn, table: str, column: str, value) -> bool:
    """Is `value` a live key in table.column? The FK check a CLI does before writing."""
    if value is None:
        return False
    row = conn.execute(
        'SELECT 1 FROM "%s" WHERE "%s" = ? LIMIT 1' % (table, column), (value,)
    ).fetchone()
    return row is not None


def live_vocab(conn, table: str, column: str) -> set:
    """The set of values a column actually holds today.

    DERIVED, NEVER LISTED IN CODE. A hardcoded vocabulary in the CLI would be a
    second home for a fact the table already states (rule 5) and would drift the
    first time doctrine adds a value -- the §2(b) defect. Where a vocabulary has
    no table (a status enum), point at the guard that owns it in
    scripts/emit_data_migration.py (ENUM_GUARDS / RANGE_GUARDS) rather than
    copying its members here.

    A refusal built on this is only as good as the corpus: on an EMPTY table it
    returns the empty set and would refuse everything. Callers must therefore
    treat an empty vocabulary as "unconstrained", not as "nothing is valid" --
    `check_vocab` below does exactly that, and says so.
    """
    return {r[0] for r in conn.execute(
        'SELECT DISTINCT "%s" FROM "%s" WHERE "%s" IS NOT NULL' % (column, table, column)
    )}


def check_values(conn, table: str, column: str) -> set:
    """The value set a column's own CHECK constraint declares, or empty if none.

    THE SCHEMA IS THE SINGLE HOME OF A CLOSED VOCABULARY. `source_locators.status`
    declares CHECK(status IN ('REFERENCE-ONLY','PROMOTED','RETIRED')) in the table
    definition; listing those three in this file would be a second home (rule 5) and
    would drift the first time a migration changes them. Read the declaration.

    Found by walking into it: the Act-2 rehearsal passed status='UNVERIFIED' -- a
    legitimate value of a DIFFERENT column (search_candidates.locator_status) -- and
    got `CHECK constraint failed` from SQLite, which is correct but tells the caller
    nothing about what WOULD be accepted. A refusal that cannot name the alternative
    is a worse tool than hand SQL.
    """
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    if not row or not row[0]:
        return set()
    m = re.search(
        r"CHECK\s*\(\s*%s\s+IN\s*\(([^)]*)\)" % re.escape(column), row[0], re.I)
    if not m:
        return set()
    return {v.strip().strip("'\"") for v in m.group(1).split(",") if v.strip()}


def check_declared(conn, table: str, column: str, value, context: str):
    """Refuse a value the column's CHECK constraint would reject, naming the set."""
    allowed = check_values(conn, table, column)
    if allowed and value not in allowed:
        raise ValueError(
            "%s: %s.%s does not accept %r. The schema's own CHECK declares: %s. "
            "Nothing was written."
            % (context, table, column, value, sorted(allowed)))


def check_vocab(conn, table: str, column: str, value, context: str):
    """Refuse a value outside the live vocabulary -- unless there is no vocabulary yet.

    THE EMPTY-CORPUS CASE IS THE WHOLE SUBTLETY. `economics_entries` and
    `case_studies` hold 0 rows, so their vocabularies are empty and every value is
    "unknown". Refusing on that would make the first legitimate write impossible --
    the CLI stalling the next batch against its own tooling, which is the failure
    mode this consolidation was warned about in both directions. So: empty
    vocabulary means unconstrained, and the write proceeds.
    """
    # THE SCHEMA'S CHECK WINS WHERE ONE EXISTS. Live rows are a SAMPLE of a
    # vocabulary, not the vocabulary. Measured 2026-08-25:
    # search_candidates.disposition declares OUT-OF-SCOPE in its CHECK and no live
    # row uses it -- a live-rows refusal would have rejected a legitimate value and
    # stalled the next batch against its own tooling. Ask the declaration first.
    declared = check_values(conn, table, column)
    if declared:
        if value not in declared:
            raise ValueError(
                "%s: %s.%s does not accept %r. The schema's own CHECK declares: %s. "
                "Nothing was written." % (context, table, column, value, sorted(declared)))
        return

    vocab = live_vocab(conn, table, column)
    if not vocab:
        return          # no corpus yet; the first writer defines the vocabulary
    if value not in vocab:
        raise ValueError(
            "%s: %r is not in the live vocabulary of %s.%s, which is %s. "
            "If this value is legitimately new, it is a doctrine change -- add it "
            "in a migration with its justification, not as a CLI argument."
            % (context, value, table, column, sorted(vocab))
        )


# ---------------------------------------------------------------------------
# The one list of tables a session may write
# ---------------------------------------------------------------------------
# MOVED HERE FROM scripts/research/emit_batch_sql.py 2026-08-25, comments intact.
#
# WHY IT MOVED, and this is the structural point of the consolidation: the CLI and
# the capture tool used to carry SEPARATE knowledge of which tables exist. That is
# how a table became writable-but-invisible to capture -- a rescue wrote 8
# source_locators rows and the capture emitted 32 statements instead of 40, losing
# them with no error raised. One constant, two importers: a table cannot again be
# writable by one and unknown to the other.
TABLES = [
    "evidence_sources",
    # ADDED 2026-08-22. Its absence was not neutral: evidence_source_authors is
    # where the 2026-08-19 fabrication happened (12 of 19 author rows named
    # non-authors, including the deletion of the autistic community co-authors
    # from the paper whose Co-1 warrant IS their co-authorship), and because this
    # capture path could not see the table, that repair had to be hand-written —
    # the same hand-SQL channel the fabrication entered through. PK is `id`
    # (INTEGER PRIMARY KEY AUTOINCREMENT), so the generic PK diff below applies
    # unchanged. What reads it: this script, invoked by the DR-2026-08-19 runbook
    # at step 11.
    "evidence_source_authors",
    # ADDED 2026-08-23, and it is the THIRD tool found blind to this one table in a
    # single day. source_locators is the identifier stash — 835 rows, 441 DOIs. R9
    # could not see it (fixed the same morning as R9a/R9b); validate_jurisdiction.py
    # never opens the DB at all; and this capture path silently DROPPED every
    # source_locators row a session wrote. That last one was found by counting: a
    # rescue that inserted 8 locator rows emitted 32 statements, not 40, and the
    # eight would have been lost between the scratch DB and the migration with no
    # error raised. A table the tooling cannot see is a table the project does not
    # really have. What reads it: this script, invoked by the DR-2026-08-19 runbook.
    "source_locators",
    "source_slug_links",
    "search_executions",
    "search_admissions",
    "search_candidates",
    "evidence_population_match",
    "citation_mining",
    "jurisdictional_values",
    "economics_entries",
    "case_studies",
    "gaps",
]

WRITABLE_TABLES = TABLES          # the name this module exports; TABLES is the moved original


def _selftest() -> int:
    """Prove the pieces that have already failed in this repository.

    Run: python3 scripts/dbcore.py --selftest
    """
    fails, examined = [], []

    def check(name, cond, detail=""):
        examined.append(name)
        print(("  [%s] %s" % ("PASS" if cond else "FAIL", name)) + (("  " + detail) if detail and not cond else ""))
        if not cond:
            fails.append(name)

    print("dbcore selftest")

    # The DOI case-drift that produced two identities for one source.
    check("norm_doi folds the drift that actually happened",
          norm_doi("10.1044/2019_AJA-19-0010") == norm_doi("10.1044/2019_aja-19-0010"))
    check("norm_doi passes None through", norm_doi(None) is None)
    check("fold_ref normalises whitespace and case", fold_ref("  ref-00965 ") == "REF-00965")

    # The mint rule. Build the exact live shape: the stash's high-water mark BELOW
    # a live evidence row. The old one-table rule returns a colliding id here.
    mem = sqlite3.connect(":memory:")
    mem.execute("CREATE TABLE source_locators (ref_id TEXT)")
    mem.execute("CREATE TABLE evidence_sources (ref_id TEXT)")
    mem.executemany("INSERT INTO source_locators VALUES (?)", [("REF-00964",), ("REF-VERIFIED-001",)])
    mem.executemany("INSERT INTO evidence_sources VALUES (?)", [("REF-00970",), ("Co1-07",)])
    got = next_ref_id(mem)
    check("next_ref_id spans BOTH ref-id homes, not just the stash", got == "REF-00971",
          "got %s -- the one-table rule would give REF-00965, which is a live evidence row" % got)
    check("closed namespaces are never minted from",
          ref_id_high_water(mem) == 970)

    # A fixture schema missing a table must not crash the mint.
    bare = sqlite3.connect(":memory:")
    bare.execute("CREATE TABLE evidence_sources (ref_id TEXT)")
    bare.execute("INSERT INTO evidence_sources VALUES ('REF-00042')")
    check("a missing ref-id home is skipped, not fatal", next_ref_id(bare) == "REF-00043")

    check("REF_ID_SHAPE accepts every live shape",
          all(REF_ID_SHAPE.fullmatch(x) for x in ("REF-00965", "REF-VERIFIED-011", "Co1-07")))
    check("REF_ID_SHAPE refuses a per-slug local label",
          not REF_ID_SHAPE.fullmatch("RAP-04"))

    # The write path must never be pointed at the committed blob by default in a
    # scratch run; and is_canonical must be able to say so.
    check("is_canonical identifies the committed database", is_canonical(CANONICAL_DB))
    check("is_canonical is False for a scratch path", not is_canonical("/tmp/scratch-xyz.db"))

    check("WRITABLE_TABLES is the moved list, non-empty and FK-ordered at the head",
          WRITABLE_TABLES[0] == "evidence_sources" and "source_locators" in WRITABLE_TABLES)

    # DERIVED, never written by hand. The first draft of this line hardcoded "12"
    # over 11 assertions -- CLAUDE.md §2(b)'s exact defect, in the selftest of the
    # module written to end duplicated facts. Count the list.
    print("EXAMINED: %d assertion(s)" % len(examined))
    print("SELFTEST: %s" % ("PASS" if not fails else "FAIL — " + ", ".join(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    import sys as _sys
    if "--selftest" in _sys.argv:
        raise SystemExit(_selftest())
    print(__doc__)
