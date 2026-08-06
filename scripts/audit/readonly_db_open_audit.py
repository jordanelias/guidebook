#!/usr/bin/env python3
"""
scripts/audit/readonly_db_open_audit.py — a script that only reads must open read-only.

WHY THIS EXISTS
---------------
Opening the canonical database read-write to read it has two costs, and the
second is the dangerous one.

1. SQLite creates `-wal` and `-shm` sidecars next to `data/guidebook.db` on a
   read-write open, and may checkpoint on close. The repo's `.gitignore` already
   carries an entry for these, which is evidence the mechanism is live rather
   than theoretical.
2. **A read-write handle is a write the reproducibility gate cannot see.** The
   blocking `migration_reproducibility` check compares `PRAGMA user_version` plus
   `COUNT(*)` on six tables (CLAUDE.md §0 rule 4). A checkpoint, a stray UPDATE,
   or an accidental commit of a mutated binary changes none of those counts. The
   migrations-only rule is absolute; its detection floor is not. Every read-write
   handle held by something that never intends to write is an unnecessary way for
   the canonical DB to change without a migration.

Measured 2026-08-06 before the sweep this check was written for: 43 non-legacy
scripts opened the DB, and only 16 of them read-only.

SCOPE — a script is IN SCOPE when all three hold
   1. it is not under a one-time/legacy directory (EXCLUDE_PARTS, mirroring
      db_path_env_audit.py so "legacy" means one thing repo-wide);
   2. it calls `sqlite3.connect`;
   3. it executes NO write SQL — determined by AST, by inspecting the string
      literal passed to `.execute` / `.executemany` / `.executescript` and
      testing its leading keyword.

Condition 3 is what keeps this honest. A keyword scan of the whole file reports
`UPDATE` and `DROP` from prose in comments and docstrings — the first draft of
this analysis did exactly that and produced 35 false "writers", including scripts
that are pure readers. Only strings actually handed to an execute call count.

WHAT IT DOES NOT DO
-------------------
It does not require `mode=ro` on every connect in a file. A read-only consumer may
legitimately open a SCRATCH database read-write — a temp fixture in a selftest, an
in-memory DB, a rebuilt copy for comparison. Only connects that resolve the
CANONICAL path (a module-level `DB`/`DB_PATH`-style constant) are required to be
read-only.

Exit 0 when every read-only consumer opens read-only; exit 1 with the list
otherwise.
"""
import argparse
import ast
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Mirrors db_path_env_audit.py and extract_code.py: one-time / legacy / different-schema.
EXCLUDE_PARTS = {"migrations", "db", "migrate", "probes", "test", "tests",
                 "__pycache__", "_archived"}

WRITE_VERB = re.compile(
    r"^\s*(INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|REPLACE|VACUUM|ATTACH)\b", re.I)
USER_VERSION_SET = re.compile(r"PRAGMA\s+user_version\s*=", re.I)

# Names that denote the canonical database path. Upper-case by convention: a
# lower-case `db_path` / `path` / `copy` is a parameter or a scratch file, and
# those are allowed to be opened read-write.
CANONICAL_NAMES = {"DB", "DB_PATH", "GUIDEBOOK_DB", "DEFAULT_DB"}


def _executed_sql(tree):
    """String literals actually passed to an execute call — not prose."""
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in ("execute", "executemany", "executescript")
                and node.args):
            arg = node.args[0]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                out.append(arg.value)
            elif isinstance(arg, ast.JoinedStr):
                out.append("".join(v.value for v in arg.values
                                   if isinstance(v, ast.Constant)))
    return out


def _writes_sql(tree):
    return any(WRITE_VERB.match(s) or USER_VERSION_SET.search(s)
               for s in _executed_sql(tree))


def _canonical_rw_connects(tree):
    """Connect calls that resolve the canonical DB and are NOT read-only.

    A read-only open is `sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)`,
    i.e. the argument is an f-string containing `mode=ro`. Anything else that
    names a canonical constant is a read-write open.
    """
    bad = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "connect" and node.args):
            continue
        arg = node.args[0]
        if isinstance(arg, ast.JoinedStr):
            lit = "".join(v.value for v in arg.values if isinstance(v, ast.Constant))
            if "mode=ro" in lit:
                continue                       # already read-only
        names = {n.id for n in ast.walk(arg) if isinstance(n, ast.Name)}
        if names & CANONICAL_NAMES:
            bad.append(getattr(node, "lineno", 0))
    return bad


def audit():
    readers, offenders = [], []
    for path in sorted(REPO.glob("**/*.py")):
        rel = path.relative_to(REPO)
        if EXCLUDE_PARTS & set(rel.parts) or rel.parts[0] not in ("scripts", "tools"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr == "connect" for n in ast.walk(tree)):
            continue
        if _writes_sql(tree):
            continue                            # a genuine writer; out of scope
        readers.append(rel)
        lines = _canonical_rw_connects(tree)
        if lines:
            offenders.append((rel, lines))
    return readers, offenders


def selftest():
    """Mutation tests. A checker with no selftest stops checking on its next refactor."""
    cases = [
        ("reader opening rw is caught",
         "import sqlite3\nDB_PATH='x'\nc=sqlite3.connect(str(DB_PATH))\nc.execute('SELECT 1')\n",
         True),
        ("reader opening ro is clean",
         'import sqlite3\nDB_PATH="x"\nc=sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)\nc.execute("SELECT 1")\n',
         False),
        ("writer opening rw is OUT OF SCOPE, not an offender",
         "import sqlite3\nDB_PATH='x'\nc=sqlite3.connect(str(DB_PATH))\nc.execute('INSERT INTO t VALUES (1)')\n",
         False),
        ("prose mentioning UPDATE does not make a reader a writer",
         "import sqlite3\nDB_PATH='x'\n# this UPDATE is discussed, never executed\nc=sqlite3.connect(str(DB_PATH))\nc.execute('SELECT 1')\n",
         True),
        ("scratch path opened rw is allowed",
         "import sqlite3\ndef f(db_path):\n    c=sqlite3.connect(db_path)\n    c.execute('SELECT 1')\n",
         False),
        ("in-memory opened rw is allowed",
         "import sqlite3\nc=sqlite3.connect(':memory:')\nc.execute('SELECT 1')\n",
         False),
    ]
    fails = []
    for name, src, want_offender in cases:
        tree = ast.parse(src)
        is_reader = not _writes_sql(tree)
        got = bool(is_reader and _canonical_rw_connects(tree))
        if got != want_offender:
            fails.append(f"{name}: expected offender={want_offender}, got {got}")
    n = len(cases)
    if fails:
        print("readonly_db_open_audit selftest FAILURES:")
        for f in fails:
            print("  -", f)
        print(f"\nRESULTS: {n - len(fails)}/{n}")
        return 1
    print(f"RESULTS: {n}/{n} selftest cases pass "
          "(rw caught, ro clean, writers out of scope, prose ignored, scratch allowed)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    if ap.parse_args().selftest:
        return selftest()

    readers, offenders = audit()
    print("=" * 70)
    print("readonly_db_open_audit.py — read-only consumers must open read-only")
    print("=" * 70)
    print(f"read-only consumers of the canonical DB: {len(readers)}")

    if not readers:
        # The vacuity guard. A gate passing because nothing is in scope is
        # indistinguishable in CI from one passing on the merits.
        print("\nVACUOUS: no read-only DB consumer found at all. That is not "
              "plausible in this repo; the scope filter is broken.")
        return 1

    for rel, lines in offenders:
        print(f"  FAIL  {rel}  (line{'s' if len(lines) > 1 else ''} "
              f"{', '.join(map(str, lines))})")
    if offenders:
        print(f"\n{len(offenders)} script(s) never write, but open the canonical "
              f"database read-write.")
        print('Fix: sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)')
        print("A read-write handle held by something that never intends to write "
              "is an unnecessary way for the canonical DB to change without a "
              "migration — and the reproducibility gate compares only "
              "user_version plus COUNT(*) on six tables, so it would not see it.")
        return 1

    print(f"\nRESULTS: {len(readers)}/{len(readers)} read-only consumers open read-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
