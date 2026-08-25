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
_REF_ID_HOMES = ("source_locators", "evidence_sources")


def ref_id_high_water(conn) -> int:
    """Highest minted REF-NNNNN across EVERY table that holds one.

    CLAUDE.md said for weeks: "mint above the source_locators high-water mark."
    That was INCOMPLETE and would have collided. Measured 2026-08-25:
        source_locators  max REF-00964
        evidence_sources max REF-00970
    Minting at 965 -- exactly what the documented rule produced -- lands on a live
    evidence row. The high-water mark is the UNION, and this function is that rule.
    """
    high = 0
    for table in _REF_ID_HOMES:
        try:
            rows = conn.execute('SELECT ref_id FROM "%s" WHERE ref_id IS NOT NULL' % table)
        except sqlite3.OperationalError:
            continue          # table absent in a fixture/scratch schema
        for (ref,) in rows:
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
