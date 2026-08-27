#!/usr/bin/env python3
"""Pin the evidence -> judgment hand-off shape ruled 2026-08-27.

WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §1).
The owner ruled evidence -> judgment is 1:N, with a worked example: "one evidence
source may provide many rows of judgment (eg a code document like Canada's NBC
3.8)". A UNIQUE index on the hand-off column would silently collapse that fan-out
-- NBC 3.8's many clauses would yield ONE determination instead of many, and the
book would lose real values with no error anywhere. It would also abolish the
dissent contest that DR-2026-08-19 §7 deliberately preserves, so a divergent
adversarial grade would become unwritable rather than readable as a contest.

WHY A CHECK AND NOT A COMMENT. The subject table holds 0 rows. Every other gate in
this repository is blind to it -- CLAUDE.md rule 4: "treat a 0-row object as
unproven, not clean". A regression here is invisible until the first extraction
pass, which is exactly when it is most expensive to discover.

The shape, measured 2026-08-27 and already correct in the schema:
  source_value_extractions.ref_id   NOT NULL      -- the hand-off key
  no UNIQUE index on that table                   -- the fan-out
  FK ref_id -> evidence_sources(ref_id)           -- points at the evidence item

Records: references/project-standards.md, 2026-08-27, both rules; the ruling
adopting items #1 and #2 of the owner architecture note.
"""
import os
import sqlite3
import sys

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
TABLE = "source_value_extractions"   # the judgment item; a rename must sweep this
KEY = "ref_id"
PARENT = "evidence_sources"


def main() -> int:
    if not os.path.exists(DB):
        print(f"FAIL: no database at {DB}")
        return 1
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)

    cols = {r[1]: r for r in con.execute(f"PRAGMA table_info({TABLE})")}
    if not cols:
        print(f"FAIL: {TABLE} does not exist. If it was renamed, this check is a "
              f"caller and must be swept (CLAUDE.md rule 4).")
        return 1

    checks, failures = [], []

    # 1 - the hand-off key is NOT NULL
    key = cols.get(KEY)
    if key is None:
        failures.append(f"{TABLE}.{KEY} is absent")
    elif not key[3]:
        failures.append(f"{TABLE}.{KEY} is nullable; the hand-off must be NOT NULL")
    checks.append(f"{TABLE}.{KEY} NOT NULL")

    # 2 - no UNIQUE index anywhere on the table: that is the ruled fan-out
    uniques = [r[1] for r in con.execute(f"PRAGMA index_list({TABLE})") if r[2]]
    if uniques:
        failures.append(
            f"UNIQUE index present on {TABLE}: {uniques}. The owner ruled one "
            f"evidence source may provide MANY judgment rows (NBC 3.8). A UNIQUE "
            f"on {KEY} abolishes that fan-out and the DR-2026-08-19 §7 dissent contest."
        )
    checks.append(f"no UNIQUE index on {TABLE}")

    # 3 - the key points at the evidence item
    fks = [r for r in con.execute(f"PRAGMA foreign_key_list({TABLE})")]
    if not any(r[2] == PARENT and r[3] == KEY for r in fks):
        failures.append(f"{TABLE}.{KEY} does not reference {PARENT}({KEY})")
    checks.append(f"{TABLE}.{KEY} -> {PARENT}({KEY})")

    print(f"EXAMINED: {len(checks)} invariant(s) of the evidence->judgment hand-off")
    for c in checks:
        print(f"  - {c}")
    if failures:
        print("\nFAIL: the ruled 1:N hand-off shape has regressed.")
        for f in failures:
            print(f"  * {f}")
        return 1
    rows = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    print(f"PASS: shape holds ({TABLE} currently {rows} rows — shape is checked, "
          f"not content).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
