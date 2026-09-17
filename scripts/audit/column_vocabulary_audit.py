#!/usr/bin/env python3
"""Do the tables agree on what to call the same thing?

WHY THIS EXISTS. `tools/pipeline_walk.py` shipped a session-attribution helper
matching two column names, `created_by_session` and `session`. The corpus spells
that one role EIGHT ways, so the tool silently reported fifteen tables --
including `source_locators`, the largest it places -- as "not attributable to a
session". The drift was not in the tool. It was in the schema, and nothing named
it, so each new reader rediscovers it by being wrong.

WHAT IT CHECKS, and the distinction is the whole point. A role can legitimately
appear under several names: `raised_by_session` and `resolved_by_session` on
`determination_gates` are two DIFFERENT events on one row, not two spellings of
one event. So this does not flag every variant -- it flags the ones where the
same fact is stored under different names, which is rule 5's "point, do not copy"
applied to the naming of columns rather than to their contents.

DERIVED, NOT LISTED. The table and column sets come from `sqlite_master` and
`PRAGMA table_info`, so a new table joins the audit automatically. What is judged
is the canonical spelling per role, and that judgment is stated here with its
reasoning rather than left implicit -- rule 8's "derive it, or name who judged it".

Usage:
  python3 scripts/audit/column_vocabulary_audit.py            # report
  python3 scripts/audit/column_vocabulary_audit.py --selftest # prove it can fail
"""
from __future__ import annotations

import argparse
import collections
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"

#: The canonical spelling for each role, and the deviations that mean the SAME
#: fact under another name. Judged 2026-09-17 against the live schema.
#:
#: `canonical` is the majority spelling, by count, in every case here -- the
#: audit is asking the minority to join the majority, never inventing a third
#: form. `same_fact` lists only spellings whose column holds what the canonical
#: column holds; an event-specific variant that records a DIFFERENT moment is
#: deliberately absent.
ROLES = {
    "row-created, which session": {
        "canonical": "created_by_session",
        "same_fact": {
            # A bare `session` column on a table that has no other session
            # column IS the creating session; it is the same fact, shortened.
            "session": "bare noun where the majority uses the full role name",
            # Domain verbs for "the session that made this row". Each table has
            # exactly one such column and no `created_by_session` beside it, so
            # the verb is decoration on the one fact, not a second event.
            "worked_by_session": "domain verb for 'created'",
            "attempted_by_session": "domain verb for 'created'",
            "checked_by_session": "domain verb for 'created'",
            "run_by_session": "domain verb for 'created'",
            "verified_by_session": "domain verb for 'created'",
            "session_applied": "reversed word order",
        },
    },
    "row-created, when": {
        "canonical": "created_at",
        "same_fact": {
            "worked_at": "domain verb for 'created'",
            "checked_at": "domain verb for 'created'",
            "executed_at": "domain verb for 'created'",
            "attempt_at": "domain verb for 'created', and not even past tense "
                          "beside its own row's attempted_by_session",
        },
    },
    "row-last-changed, when": {
        "canonical": "updated_at",
        "same_fact": {"last_updated": "same fact, different word order"},
    },
    "free text about the row": {
        "canonical": "notes",
        "same_fact": {"note": "singular/plural split with no rule behind it"},
    },
}

#: Spellings that look like drift and are NOT: a second column recording a
#: genuinely different event on the same row. Named so the audit cannot quietly
#: start demanding they be merged, which would destroy a fact.
NOT_DRIFT = {
    # EXEMPT BY BOOTSTRAP, not by preference. `data_migrations.applied_at` and
    # `.applied_by_session` are drift by this audit's own definition, and they are
    # unrenameable: `migrate_db.py` writes `INSERT INTO data_migrations
    # (migration_id, applied_at, ...)` at three call sites DURING the run that
    # would apply the rename, so the run cannot record itself; and updating the
    # writer first breaks it before the migration exists. Migration 085 records
    # the same reasoning.
    "applied_at", "applied_by_session",
    "raised_by_session", "resolved_by_session", "raised_at", "resolved_at",
    "retired_by_session", "retired_at", "updated_by_session",
    "started_at", "completed_at", "last_verified_at", "verified_at",
    "code_currency_verified_at", "code_currency_verified_by_session",
    "icd11_verified_at", "decision_date", "pmp_last_walk_at",
}


def connect_ro(db: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{db}?mode=ro", uri=True)


def schema(con) -> dict:
    tabs = [t for (t,) in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    return {t: [c[1] for c in con.execute(f'PRAGMA table_info("{t}")')] for t in tabs}


def audit(cols_by_table: dict) -> list[dict]:
    """One finding per (table, deviant column). Ordered, so output is stable."""
    where = collections.defaultdict(list)
    for t, cols in cols_by_table.items():
        for c in cols:
            where[c].append(t)

    findings = []
    for role, spec in ROLES.items():
        canon = spec["canonical"]
        for dev, why in sorted(spec["same_fact"].items()):
            if dev in NOT_DRIFT:
                continue
            for t in sorted(where.get(dev, [])):
                findings.append({
                    "table": t, "column": dev, "role": role,
                    "canonical": canon, "why": why,
                    # A table already carrying the canonical name AND a deviant
                    # is a different, worse case: two columns for one fact in one
                    # table, which is rule 5 literally.
                    "both": canon in cols_by_table[t],
                })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", str(DEFAULT_DB)))
    ap.add_argument("--selftest", action="store_true",
                    help="prove the audit can fail: run it over a fixture that drifts")
    a = ap.parse_args()

    if a.selftest:
        fixture = {
            "clean_table": ["id", "created_by_session", "created_at", "notes"],
            "drifting": ["id", "worked_by_session", "worked_at", "note"],
            "doubled": ["id", "created_by_session", "session"],
        }
        got = audit(fixture)
        cols = {(f["table"], f["column"]) for f in got}
        want = {("drifting", "worked_by_session"), ("drifting", "worked_at"),
                ("drifting", "note"), ("doubled", "session")}
        missing, extra = want - cols, cols - want
        both = {f["column"] for f in got if f["both"]}
        ok = not missing and not extra and both == {"session"}
        print(f"EXAMINED: {len(fixture)} fixture tables, {len(got)} finding(s)")
        if missing:
            print("  MISSED:", sorted(missing))
        if extra:
            print("  FALSE POSITIVE:", sorted(extra))
        if both != {"session"}:
            print("  `both` flag wrong:", sorted(both))
        print("SELFTEST:", "PASS — the audit fires on drift and is silent on the "
              "clean table" if ok else "FAIL")
        return 0 if ok else 1

    db = Path(a.db)
    if not db.exists():
        print(f"column_vocabulary_audit: no database at {db}", file=sys.stderr)
        return 1
    con = connect_ro(db)
    try:
        cols_by_table = schema(con)
    finally:
        con.close()

    findings = audit(cols_by_table)
    n_cols = sum(len(v) for v in cols_by_table.values())
    print(f"EXAMINED: {len(cols_by_table)} tables, {n_cols} columns, "
          f"{len(ROLES)} roles")

    if not findings:
        print("VERDICT: CLEAN — every table spells these roles the same way.")
        return 0

    by_role = collections.defaultdict(list)
    for f in findings:
        by_role[f["role"]].append(f)
    for role, fs in by_role.items():
        canon = fs[0]["canonical"]
        print(f"\n  {role} — canonical `{canon}`")
        for f in fs:
            flag = "  [BOTH IN ONE TABLE]" if f["both"] else ""
            print(f"    {f['table']}.{f['column']}  — {f['why']}{flag}")

    print(f"\nRESULTS: {len(findings)} column(s) store a role under a name other "
          f"than the majority spelling.")
    print("A RENAME IS A MIGRATION AND A CALLER SWEEP, never an edit: "
          "CLAUDE.md rule 4 (A VIEW IS A CALLER, so is a skill, so is the check "
          "registry), and migration 064 exists because 063 swept eight Python "
          "readers and six skills and missed v_item_provenance.")
    print("VERDICT: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
