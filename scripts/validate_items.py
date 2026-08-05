"""
scripts/validate_items.py — CI validator for items table.

Checks:
  V1: item_code matches [A-K]-NN[a-z]? (2 digits, optional lowercase suffix)
  V2: category is single letter A-K
  V3: status is draft|active|merged|retired
  V4: name is non-empty
  V5: every item_population_links row resolves to a live populations row,
      and its applicability is a value the schema allows

Exit codes: 0 = pass, 1 = fail

V5 REWRITTEN 2026-08-05, for two reasons that were each independently fatal.

It read `items.applicable_groups`, a CSV of population codes packed into one
column. That column was dropped when `item_population_links` replaced it, so
every run of this validator raised `IndexError: No item with that key` on the
first row. It validated nothing, loudly, for as long as that was true.

It also compared against KNOWN_POPS, a population list hardcoded here — 23 codes
including compounds like `NDV/MH` and the pseudo-code `ALL`. A taxonomy
transcribed into a validator is a taxonomy that drifts from the one it validates,
and this one had: the live `populations` table is the authority (CLAUDE.md §2 —
the DB is canonical and the other store is the thing to reconcile), and it does
not agree with that list. The codes now come from the table, so the validator
cannot disagree with the data it is checking.
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

ITEM_CODE_RE   = re.compile(r"^[A-K]-\d{2}[a-z]?$")
CATEGORY_RE    = re.compile(r"^[A-K]$")
VALID_STATUS   = {"draft", "active", "merged", "retired"}

# NOT re-checked here: `item_population_links.applicability`. The schema already
# enforces it with a CHECK constraint over five values — `applies`,
# `applies_strictly`, `applies_loosely`, `context_dependent`, `does_not_apply`.
#
# The first draft of this rewrite DID re-check it, against a two-value set read
# off the live data (only `applies` and `context_dependent` are populated today).
# A fault-injection run caught it: the injection could not even write a bad value,
# because the CHECK rejected it first, and the narrow copy would have failed a
# legitimate `applies_strictly` row the schema permits. Re-transcribing a
# constraint the schema owns is how a validator ends up disagreeing with the data
# it validates — the same defect as the KNOWN_POPS list this rewrite removed, one
# layer down. Where the schema enforces, the validator stays quiet.


def validate():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    if "items" not in tables:
        print("SKIP: items table not present — migration 004 not yet applied")
        sys.exit(0)

    rows  = conn.execute("SELECT * FROM items").fetchall()
    errors = []

    # V5 inputs: the live taxonomy, and the links to check against it.
    known_pops = {r[0] for r in conn.execute(
        "SELECT population_code FROM populations"
    )}
    links = conn.execute(
        "SELECT item_code, population_code, applicability FROM item_population_links "
        "ORDER BY item_code, population_code"
    ).fetchall()

    for r in rows:
        code = r["item_code"] or ""
        # V1: item_code format
        if not ITEM_CODE_RE.match(code):
            errors.append(f"V1 FAIL {code}: item_code does not match ^[A-K]-NN[a-z]?$")
        # V2: category
        if not CATEGORY_RE.match(r["category"] or ""):
            errors.append(f"V2 FAIL {code}: category '{r['category']}' is not A-K")
        # V3: status
        if r["status"] not in VALID_STATUS:
            errors.append(f"V3 FAIL {code}: status '{r['status']}' not in {VALID_STATUS}")
        # V4: name non-empty
        if not (r["name"] or "").strip():
            errors.append(f"V4 FAIL {code}: name is empty")
    item_codes = {r["item_code"] for r in rows}

    # V5: the population links, checked against the live taxonomy.
    #
    # Both declared foreign keys are re-checked rather than trusted. SQLite
    # enforces FKs per-connection and they are OFF by default, so a file can and
    # does carry orphans that its own DDL forbids — CLAUDE.md records ~18 such
    # rows surviving from the bootstrap snapshot. A declared constraint is not an
    # observed one.
    for link in links:
        ic, pc = link["item_code"], link["population_code"]
        if pc not in known_pops:
            errors.append(f"V5 FAIL {ic}: population_code '{pc}' is not in the populations table")
        if ic not in item_codes:
            errors.append(f"V5 FAIL {ic}: link references an item_code with no items row")

    total = len(rows)
    linked = len({link["item_code"] for link in links})
    conn.close()

    if errors:
        print(f"items validation: {len(errors)} issue(s) across {total} items")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print(f"items validation: PASS ({total} items, {len(links)} population links "
          f"across {linked} items, all codes valid)")
    sys.exit(0)


if __name__ == "__main__":
    validate()
