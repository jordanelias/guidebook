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
CANONICAL path (a module-level `DB`/`DB_PATH`-style constant, the literal
`.../guidebook.db`, or the `GUIDEBOOK_DB_PATH` env var) are required to be
read-only — and "resolve" is traced through same-file dataflow (`_tainted_canonical`),
not just read off the connect() call's own argument expression. A canonical path
that reaches `connect()` after passing through a lower-case local — a bare
assignment, a function parameter's default, an `argparse` `--db` option whose
`default=` is canonical, or a same-file call site — still counts; only a
genuinely unconstrained parameter (no canonical default anywhere in its
provenance) is treated as scratch. (Until 2026-08-14 the matcher only looked at
the connect() argument's own literal Names, missing exactly that lower-case-local
case — see workplan/2026-08-14-remediation-workplan.md §2 item 3.)

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
# those are allowed to be opened read-write UNLESS same-file dataflow shows
# they were populated from one of these (see _tainted_canonical below).
CANONICAL_NAMES = {"DB", "DB_PATH", "GUIDEBOOK_DB", "DEFAULT_DB"}

# The other two ways this repo spells "the canonical DB path" (CLAUDE.md §7):
# the literal committed path, and the env var scripts are told to honour.
CANONICAL_LITERAL_RE = re.compile(r"(^|/)guidebook\.db$")
CANONICAL_ENV_VAR = "GUIDEBOOK_DB_PATH"


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


def _is_mode_ro(arg):
    """True if any string-literal fragment of a connect() argument expression
    contains `mode=ro`, however it is built: f-string, plain literal,
    concatenation, `%`/`.format` — any of those still puts the fragment in
    the AST as an `ast.Constant` string, which is all this needs to check.
    """
    return any(isinstance(n, ast.Constant) and isinstance(n.value, str)
               and "mode=ro" in n.value for n in ast.walk(arg))


def _tainted_canonical(tree):
    """Names (and argparse-`dest` attributes) that resolve to the canonical DB
    path, directly or through one or more hops of same-file dataflow.

    This is what closes the lower-case-local blind spot: the previous version
    only looked for `Name` nodes matching CANONICAL_NAMES written literally
    inside the connect() call's own argument expression, so any reader that
    first funnelled the canonical path through a lower-case local — a bare
    assignment (`db_path = DB_PATH`), a function parameter's default value,
    an `argparse` `--db` option whose `default=` is canonical (which taints
    the resulting `args.db` attribute), a fallback chain ending in a literal
    `.../guidebook.db` path or a read of `GUIDEBOOK_DB_PATH`, or a same-file
    call site passing any of the above into another function's parameter —
    was invisible to it. Fixpoint over the whole file; a script is small
    enough that this always terminates quickly.
    """
    names = set(CANONICAL_NAMES)
    attrs = set()                      # argparse dest names, e.g. "db" for args.db

    def tainted(expr):
        if expr is None:
            return False
        for n in ast.walk(expr):
            if isinstance(n, ast.Name) and n.id in names:
                return True
            if isinstance(n, ast.Attribute) and n.attr in attrs:
                return True
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                if n.value == CANONICAL_ENV_VAR or CANONICAL_LITERAL_RE.search(n.value):
                    return True
        return False

    func_defs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}

    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            # x = <expr>  /  x: T = <expr>
            if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
                if tainted(node.value):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    for t in targets:
                        if isinstance(t, ast.Name) and t.id not in names:
                            names.add(t.id)
                            changed = True

            # parser.add_argument("--db", default=<canonical>) taints args.db
            elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "add_argument"):
                dest = None
                for kw in node.keywords:
                    if kw.arg == "dest" and isinstance(kw.value, ast.Constant):
                        dest = kw.value.value
                if dest is None and node.args and isinstance(node.args[0], ast.Constant) \
                        and isinstance(node.args[0].value, str) \
                        and node.args[0].value.startswith("--"):
                    dest = node.args[0].value[2:].replace("-", "_")
                default_expr = next((kw.value for kw in node.keywords if kw.arg == "default"),
                                     None)
                if dest and default_expr is not None and dest not in attrs \
                        and tainted(default_expr):
                    attrs.add(dest)
                    changed = True

            # def f(x=<canonical-default>): ...
            elif isinstance(node, ast.FunctionDef):
                positional = node.args.args
                defaults = node.args.defaults
                offset = len(positional) - len(defaults)
                for a, d in zip(positional[offset:], defaults):
                    if a.arg not in names and tainted(d):
                        names.add(a.arg)
                        changed = True
                for a, d in zip(node.args.kwonlyargs, node.args.kw_defaults):
                    if d is not None and a.arg not in names and tainted(d):
                        names.add(a.arg)
                        changed = True

            # same-file call site: f(<tainted-arg>) taints f's parameter name
            elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in func_defs):
                params = [a.arg for a in func_defs[node.func.id].args.args]
                for i, a in enumerate(node.args):
                    if i < len(params) and params[i] not in names and tainted(a):
                        names.add(params[i])
                        changed = True
                for kw in node.keywords:
                    if kw.arg in params and kw.arg not in names and tainted(kw.value):
                        names.add(kw.arg)
                        changed = True
    return names, attrs


def _canonical_rw_connects(tree):
    """Connect calls that resolve the canonical DB and are NOT read-only.

    A read-only open is `sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)`
    (or any other spelling containing `mode=ro` — see _is_mode_ro). Anything
    else whose argument resolves — directly, or through _tainted_canonical's
    same-file dataflow — to the canonical DB path is a read-write open.
    """
    bad = []
    names, attrs = _tainted_canonical(tree)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "connect" and node.args):
            continue
        arg = node.args[0]
        if _is_mode_ro(arg):
            continue                       # already read-only
        found_names = {n.id for n in ast.walk(arg) if isinstance(n, ast.Name)}
        found_attrs = {n.attr for n in ast.walk(arg) if isinstance(n, ast.Attribute)}
        if (found_names & names) or (found_attrs & attrs):
            bad.append(getattr(node, "lineno", 0))
    return bad


def audit():
    readers, offenders, writers = [], [], []
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
            # A genuine writer; out of scope — and this is the audit's OWN
            # remaining blind spot, stated rather than left for someone to
            # discover. Exclusion is per FILE, so a script that writes to a
            # scratch fixture anywhere in it drops out entirely, canonical
            # read-only opens included. Two real offenders were sitting in that
            # shadow on 2026-08-14 (register_integrity_check.py:141 and
            # validate_pydantic_schemas.py:171 — both pure readers of the
            # canonical DB whose only writes were to temp fixtures); they were
            # found by hand and fixed, and this matcher still cannot see their
            # class. Narrowing the exclusion from file to connect-site is the
            # fix; it is not done here.
            writers.append(rel)
            continue
        readers.append(rel)
        lines = _canonical_rw_connects(tree)
        if lines:
            offenders.append((rel, lines))
    return readers, offenders, writers


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
        # --- lower-case-local blind spot (closed by _tainted_canonical) ---
        ("lower-case local assigned straight from the canonical constant is caught",
         "import sqlite3\nDB_PATH='x'\ndb_path=DB_PATH\nc=sqlite3.connect(db_path)\nc.execute('SELECT 1')\n",
         True),
        ("canonical path reaching connect() through an argparse --db default "
         "and a function call is caught",
         "import argparse, sqlite3\nDEFAULT_DB='x'\n"
         "def audit(db_path):\n    c=sqlite3.connect(db_path)\n    c.execute('SELECT 1')\n"
         "ap=argparse.ArgumentParser()\nap.add_argument('--db', default=DEFAULT_DB)\n"
         "args=ap.parse_args([])\naudit(args.db)\n",
         True),
        ("a required --db with no default stays a scratch parameter, not caught",
         "import argparse, sqlite3\n"
         "def f(db_path):\n    c=sqlite3.connect(db_path)\n    c.execute('SELECT 1')\n"
         "ap=argparse.ArgumentParser()\nap.add_argument('--db', required=True)\n"
         "args=ap.parse_args(['--db','x'])\nf(args.db)\n",
         False),
        ("a fallback chain ending in a literal .../guidebook.db path is caught",
         "import sqlite3, os\n"
         "def g(db_path):\n    c=sqlite3.connect(db_path)\n    c.execute('SELECT 1')\n"
         "db_path = None or os.environ.get('GUIDEBOOK_DB_PATH') or "
         "os.path.join('x', 'data', 'guidebook.db')\ng(db_path)\n",
         True),
        ("mode=ro spelled as a plain (non-f-string) literal is still recognised read-only",
         "import sqlite3\nDB_PATH='x'\n"
         "c=sqlite3.connect('file:' + DB_PATH + '?mode=ro', uri=True)\nc.execute('SELECT 1')\n",
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

    readers, offenders, writers = audit()
    print("=" * 70)
    print("readonly_db_open_audit.py — read-only consumers must open read-only")
    print("=" * 70)
    print(f"read-only consumers of the canonical DB: {len(readers)}")
    # State the scope alongside the count. A bare "39/39" reads as total
    # coverage; it is coverage of the files this audit can see.
    print(f"excluded as writers (NOT examined, see the comment in audit()): "
          f"{len(writers)}")
    print(f"EXAMINED: {len(readers)}")

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
