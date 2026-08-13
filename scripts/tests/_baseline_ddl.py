"""Pull object DDL out of the current baseline migration.

WHY THIS EXISTS. Two fixtures used to reconstruct schema by scanning the whole
migration history for a literal table name. That approach broke twice in one day:

  1. When `evidence_cell_state` was renamed to `specifications`, a token sweep
     rewrote the *selector string* — which had to keep matching the immutable
     migrations' own text — so the scan silently collected a different file set
     and the fixture built the wrong schema.
  2. When the history was frozen behind `057_baseline_2026-08-12.sql`, the files
     the scan read were no longer in `scripts/migrations/` at all.

Reading the baseline is simpler and self-correcting: there is exactly one file, it
holds the CURRENT schema, and a future baseline replaces it in place under the same
glob. No rename replay, no hand-copied DDL, nothing to drift.

`ddl_for()` fails loudly on a name it cannot find, rather than returning a short
list — a fixture that quietly builds fewer tables is the "a gate reporting zero may
have examined zero" failure wearing a test's clothes.
"""
import pathlib
import re
import sys

MIGRATIONS = pathlib.Path(__file__).resolve().parents[1] / "migrations"

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
    return "\n".join(found[n] for n in wanted)
