"""
scripts/validate_conflicts.py — CI validator for conflicts table.

Checks:
  V1: conflict_id matches CONF-NNNN
  V2: status is one of the five valid values
  V3: pop_a < pop_b (alphabetical; wrapper must normalise before insert)
  V4: domain is non-empty
  V5: gap_id references an existing gap (if set)
  V6: UNRESOLVED conflicts must have a gap_id (data integrity)

Exit codes: 0 = pass, 1 = fail
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

CONF_ID_RE    = re.compile(r"^CONF-\d{4}$")
VALID_STATUS  = {
    "RESOLVED-EVIDENCE", "RESOLVED-CONSENSUS",
    "RESOLUTION-PROPOSED", "UNRESOLVED", "MODE-S-ONLY",
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
    if "conflicts" not in tables:
        print("SKIP: conflicts table not present — migration 004 not yet applied")
        sys.exit(0)

    rows   = conn.execute("SELECT * FROM conflicts").fetchall()
    gaps   = {r[0] for r in conn.execute("SELECT gap_id FROM gaps").fetchall()}
    errors = []

    for r in rows:
        cid = r["conflict_id"] or ""
        # V1: conflict_id format
        if not CONF_ID_RE.match(cid):
            errors.append(f"V1 FAIL {cid}: conflict_id does not match CONF-NNNN")
        # V2: status
        if r["status"] not in VALID_STATUS:
            errors.append(f"V2 FAIL {cid}: status '{r['status']}' not valid")
        # V3: pop ordering
        if r["pop_a"] and r["pop_b"] and r["pop_a"] > r["pop_b"]:
            errors.append(f"V3 FAIL {cid}: pop_a '{r['pop_a']}' > pop_b '{r['pop_b']}' — wrapper must normalise")
        # V4: domain non-empty
        if not (r["domain"] or "").strip():
            errors.append(f"V4 FAIL {cid}: domain is empty")
        # V5: gap_id references existing gap
        if r["gap_id"] and r["gap_id"] not in gaps:
            errors.append(f"V5 WARN {cid}: gap_id '{r['gap_id']}' not found in gaps table (orphaned)")
        # V6: UNRESOLVED must have gap_id
        if r["status"] == "UNRESOLVED" and not r["gap_id"]:
            errors.append(f"V6 WARN {cid}: UNRESOLVED conflict has no gap_id (should route to CONF gap)")

    conn.close()
    total = len(rows)

    if errors:
        print(f"conflicts validation: {len(errors)} issue(s) across {total} conflict(s)")
        for e in errors:
            print(f"  {e}")
        # Distinguish FAIL (V1-V4) from WARN (V5-V6)
        hard = [e for e in errors if "FAIL" in e]
        sys.exit(1 if hard else 0)
    else:
        print(f"conflicts validation: PASS ({total} conflict(s))")
        sys.exit(0)


if __name__ == "__main__":
    validate()
