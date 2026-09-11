"""
scripts/validate_parameters.py — CI validator for the design-parameter registry
(`base_parameters` pointing at `terms`).

WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §8):
a parameter whose name states its own answer. The item layer existed for months as
exactly that shape -- `E-08 Corridor Clear Width (>=1200 mm Minimum on All Primary
Routes)` -- a container that announces its determination before any evidence is
weighed against it, which "biases every finding... predisposed to filing into a
container that already exists" (CLAUDE.md §7). The owner deleted the whole item
layer on 2026-09-01 over exactly this defect (DR-2026-08-19 §1.1: 42 of 93 item
names embedded a determination). `base_parameters` is the item layer's replacement
as the thing a determination is filed against (owner ruling 2026-08-26, "the
judgment object is the canonical parameter"). If this check does not exist, the
same defect can recur one layer down and nothing catches it before it reaches a
reader: a parameter named "corridor width >=1200 mm" would read, to every session
that files a determination against it, exactly like a pre-decided answer -- the
same bias, in a new table.

THE ONE INVARIANT: no `terms.canonical_en` reached by a live `base_parameters` row
matches the value-bearing pattern -- a digit, a comparator (>= <= < > =), or a
min/max word. A name is a parameter (what is under determination); a value belongs
to the determination that names it (`specifications`), never to the parameter.

THIS IS A BACKSTOP, NOT THE FIRST LINE. `scripts/db.py` already refuses this at
write time -- both `add-term` and `add-parameter` call the identical test before
they will mint a row (scripts/db.py:3087, :3185). This check exists for what a
CLI refusal cannot cover: a data migration written directly against dbcore, a
future writer that does not route through `db.py`, or a bug in the refusal itself.
`validate_items.py`'s own precedent is the same shape -- it re-checked FKs
SQLite's own DDL "forbids" because "a declared constraint is not an observed one."

ONE PATTERN, NOT TWO (CLAUDE.md rule 5 -- "never write the same fact into a second
table. Point, do not copy."). The exact regex already lives at `scripts/db.py`'s
`_VALUE_BEARING` and is imported from there, not retyped: two regexes asserting one
rule is the dual-home rule 5 forbids one level down from a table, and the risk is
concrete -- `db.py` refuses new value-bearing terms already, so retyping this
pattern here would recreate the identical fork alias-provenance and V5 (population
codes) rewrites both found and killed: a second copy that drifts the moment either
one is edited and nobody remembers the other exists.

`base_parameters` is empty today (2026-09-10) -- no owner batch has minted a
parameter yet. That makes this check's live run NOTHING-IN-SCOPE, correctly: there
is nothing to examine yet, not a broken sweep. `min_items: 1` is still the right
declaration (not `no_floor`) because a `base_parameters` row IS repo content the
owner intends to populate, not a corpus retired to empty by decision -- the day the
first parameter is minted, this floor is what turns a silent gap into a reported one.

Exit codes: 0 = pass (including NOTHING-IN-SCOPE), 1 = a value-bearing name found.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import _VALUE_BEARING  # noqa: E402  (single source of truth; see header)

import sqlite3  # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def validate():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    if "base_parameters" not in tables or "terms" not in tables:
        print("SKIP: base_parameters/terms not present — base_parameters migration "
              "not yet applied")
        conn.close()
        sys.exit(0)

    rows = conn.execute(
        "SELECT bp.parameter_id, t.term_id, t.canonical_en "
        "FROM base_parameters bp JOIN terms t ON t.term_id = bp.term_id "
        "ORDER BY bp.parameter_id"
    ).fetchall()
    conn.close()

    errors = []
    for r in rows:
        if _VALUE_BEARING.search(r["canonical_en"] or ""):
            errors.append(
                f"P1 FAIL parameter_id={r['parameter_id']} (term {r['term_id']}): "
                f"canonical_en {r['canonical_en']!r} carries a number, a comparator, "
                f"or a min/max word — it states a determination in its own name"
            )

    total = len(rows)
    if errors:
        print(f"parameters validation: {len(errors)} issue(s) across {total} parameter(s)")
        for e in errors:
            print(f"  {e}")
        print(f"EXAMINED: {total}")
        sys.exit(1)

    print(f"parameters validation: PASS ({total} parameter(s), "
          f"no value-bearing canonical_en found)")
    print(f"EXAMINED: {total}")
    sys.exit(0)


if __name__ == "__main__":
    validate()
