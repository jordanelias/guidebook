"""
scripts/validate_audit_runs.py — CI validator for item_audit_runs table.

Checks:
  V1: run_id format is {item_code}_{session} (contains at least one underscore)
  V2: status is IN-PROGRESS|COMPLETE|HANDED-OFF
  V3: steps_started and steps_complete are valid JSON arrays
  V4: all step names in steps_started/steps_complete are valid pipeline steps
  V5: every name in steps_complete is also in steps_started
  V6: item_code exists in items table (FK integrity check)

Exit codes: 0 = pass, 1 = fail
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

VALID_STATUS  = {"IN-PROGRESS", "COMPLETE", "HANDED-OFF"}
VALID_STEPS   = {
    "connection-discovery-spec",
    "connection-discovery-evidence",
    "conflict-mapper",
    "content-gap-analyzer",
    "evidence-auditor",
    "functional-deficit-auditor",
    "economics-auditor",
    "audit-consolidator",
}


def validate():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    if "item_audit_runs" not in tables:
        print("SKIP: item_audit_runs table not present — migration 004 not yet applied")
        sys.exit(0)

    runs       = conn.execute("SELECT * FROM item_audit_runs").fetchall()
    item_codes = {r[0] for r in conn.execute("SELECT item_code FROM items").fetchall()}
    errors     = []

    for r in runs:
        rid = r["run_id"] or ""
        # V1: run_id format (must contain underscore)
        if "_" not in rid:
            errors.append(f"V1 FAIL {rid}: run_id must be {{item_code}}_{{session}}")
        # V2: status
        if r["status"] not in VALID_STATUS:
            errors.append(f"V2 FAIL {rid}: status '{r['status']}' not valid")
        # V3 + V4 + V5: step arrays
        for field in ["steps_started", "steps_complete"]:
            raw = r[field] or "[]"
            try:
                steps = json.loads(raw)
                if not isinstance(steps, list):
                    errors.append(f"V3 FAIL {rid}: {field} is not a JSON array")
                    continue
                unknown = [s for s in steps if s not in VALID_STEPS]
                if unknown:
                    errors.append(f"V4 FAIL {rid}: {field} contains unknown step(s): {unknown}")
            except json.JSONDecodeError as e:
                errors.append(f"V3 FAIL {rid}: {field} is not valid JSON: {e}")
        # V5: steps_complete ⊆ steps_started
        try:
            sc = set(json.loads(r["steps_complete"] or "[]"))
            ss = set(json.loads(r["steps_started"]  or "[]"))
            not_started = sc - ss
            if not_started:
                errors.append(
                    f"V5 FAIL {rid}: step(s) in steps_complete but not steps_started: {not_started}"
                )
        except (json.JSONDecodeError, TypeError):
            pass  # already caught in V3
        # V6: item_code FK
        if r["item_code"] and r["item_code"] not in item_codes:
            errors.append(f"V6 FAIL {rid}: item_code '{r['item_code']}' not found in items table")

    conn.close()
    total = len(runs)

    if errors:
        print(f"audit_runs validation: {len(errors)} issue(s) across {total} run(s)")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"audit_runs validation: PASS ({total} run(s))")
        sys.exit(0)


if __name__ == "__main__":
    validate()
