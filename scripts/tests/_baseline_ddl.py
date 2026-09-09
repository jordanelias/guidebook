"""Pull object DDL out of the current baseline migration.

WHY THIS EXISTS. Two fixtures used to reconstruct schema by scanning the whole
migration history for a literal table name. That approach broke twice in one day:

  1. When `evidence_cell_state` was renamed to `specifications`, a token sweep
     rewrote the *selector string* — which had to keep matching the immutable
     migrations' own text — so the scan silently collected a different file set
     and the fixture built the wrong schema.
  2. When the history was frozen behind `057_baseline_2026-08-12.sql`, the files
     the scan read were no longer in `scripts/migrations/` at all.

Reading the baseline is simpler for the two problems above: there is exactly one
file, and a future baseline replaces it in place under the same glob. No rename
replay, no hand-copied DDL.

BUT THE BASELINE IS NOT THE CURRENT SCHEMA, AND THIS DOCSTRING CLAIMED IT WAS.
A baseline is immutable and frozen at the date in its name; every migration after
it moves the schema and the baseline does not follow. So `ddl_for()` returns the
schema AS OF the baseline, which is the current one only until the next migration.
That gap shipped a third failure of exactly the kind this module exists to prevent:
migration 071 re-keyed `specifications`, and `test_evidence_cell_state_2_3` went on
building the pre-071 table from the baseline and reporting "FK: non-existent
item_code" green over a column dropped a fortnight earlier — a gate passing having
examined a fiction (CLAUDE.md §5(a)).

So the rule for a fixture is: read an object from the LIVE schema when a migration
has touched it since the baseline, and from here only when it has not. `ddl_for()`
now says which case you are in — it compares what it hands back against the live
schema and warns on any object whose shape has moved. It cannot fail on that,
because a fixture may legitimately have no database to compare with.

`ddl_for()` fails loudly on a name it cannot find, rather than returning a short
list — a fixture that quietly builds fewer tables is the "a gate reporting zero may
have examined zero" failure wearing a test's clothes.
"""
import os
import pathlib
import re
import sqlite3
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MIGRATIONS = pathlib.Path(__file__).resolve().parents[1] / "migrations"
LIVE_DB = pathlib.Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))

_NAME_RE = re.compile(
    r'CREATE\s+(?:UNIQUE\s+)?(?:TABLE|INDEX|VIEW|TRIGGER)\s+'
    r'(?:IF\s+NOT\s+EXISTS\s+)?"?([A-Za-z_][A-Za-z0-9_]*)"?',
    re.I)


def baseline_path():
    """The highest-numbered baseline migration on disk."""
    files = sorted(MIGRATIONS.glob("[0-9][0-9][0-9]_baseline_*.sql"))
    if not files:
        print(f"  [FAIL] no baseline migration in {MIGRATIONS}", file=sys.stderr)
        sys.exit(1)
    return files[-1]


def _statements(text):
    """CREATE statements, one per yield. The baseline is machine-generated with
    every statement terminated by `;` at end of line, so line accumulation is
    enough and avoids a regex that could split inside a CHECK constraint."""
    buf = None
    for line in text.splitlines():
        if buf is None:
            if line.lstrip().upper().startswith("CREATE "):
                buf = [line]
                if line.rstrip().endswith(";"):
                    yield "\n".join(buf)
                    buf = None
        else:
            buf.append(line)
            if line.rstrip().endswith(";"):
                yield "\n".join(buf)
                buf = None


def ddl_for(*names):
    """CREATE statements for the named objects, in baseline order.

    Raises SystemExit naming every object it could not find.
    """
    text = baseline_path().read_text(encoding="utf-8")
    wanted = list(names)
    found = {}
    for stmt in _statements(text):
        m = _NAME_RE.match(stmt.lstrip())
        if m and m.group(1) in wanted:
            found[m.group(1)] = stmt
    missing = [n for n in wanted if n not in found]
    if missing:
        print(f"  [FAIL] {baseline_path().name} has no CREATE for: {missing}\n"
              f"         The fixture would have built a schema the database does not have.",
              file=sys.stderr)
        sys.exit(1)
    _warn_if_stale(found)
    return "\n".join(found[n] for n in wanted)


def _norm(sql):
    """Collapse whitespace and drop a trailing semicolon, so the comparison is
    about shape rather than formatting. The baseline is generated from
    sqlite_master, so an untouched object matches exactly once normalised."""
    return re.sub(r"\s+", " ", sql.strip().rstrip(";")).strip()


def _warn_if_stale(found):
    """Say which of the returned objects the live schema has since moved.

    Advisory by construction: a fixture may legitimately run with no database
    present, and some fixtures WANT the frozen shape. What this refuses to do is
    stay silent — a fixture building a table the database no longer has passes
    green over a fiction, which is how `test_evidence_cell_state_2_3` asserted FK
    constraints on `specifications.item_code` for a fortnight after migration 071
    dropped it.
    """
    try:
        con = sqlite3.connect(f"file:{LIVE_DB}?mode=ro", uri=True)
    except sqlite3.Error:
        return
    try:
        live = {n: sql for n, sql in con.execute(
            "SELECT name, sql FROM sqlite_master WHERE sql IS NOT NULL")}
    except sqlite3.Error:
        return
    finally:
        con.close()
    if not live:
        return
    for name, sql in found.items():
        if name in live and _norm(live[name]) != _norm(sql):
            print(
                f"  [STALE-BASELINE] {name}: {baseline_path().name} and the live "
                f"schema disagree.\n"
                f"         A migration has moved this object since the baseline was "
                f"frozen. Read it from sqlite_master instead, or the fixture asserts "
                f"against a table the database does not have.",
                file=sys.stderr)
