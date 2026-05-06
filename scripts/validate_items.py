"""
scripts/validate_items.py — CI validator for items table.

Checks:
  V1: item_code matches [A-K]-NN[a-z]? (2 digits, optional lowercase suffix)
  V2: category is single letter A-K
  V3: status is draft|active|merged|retired
  V4: name is non-empty
  V5: applicable_groups parseable as CSV of known population codes

Exit codes: 0 = pass, 1 = fail
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
# Known population codes per project taxonomy
KNOWN_POPS     = {
    # Core population codes
    "UPL", "MOB", "DEM", "PAIN", "NDV", "VIS", "DEAF",
    "SCI", "OFS", "ABI", "MH", "ASD", "LOW-VISION",
    "PCS", "AUT", "NEU", "DBL", "ADHD", "SENS", "IntD",
    # Compound and qualified codes used in spec
    "NDV/MH", "NDV/SENS", "NEU/MS", "NEU/PCS", "NEU/epilepsy",
    "MOB/UPL", "OFS/POTS", "OFS/CFS", "OFS/MCAS", "OFS/MCAS",
    # Shorthand used in spec
    "ALL",  # All populations
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
    if "items" not in tables:
        print("SKIP: items table not present — migration 004 not yet applied")
        sys.exit(0)

    rows  = conn.execute("SELECT * FROM items").fetchall()
    errors = []

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
        # V5: applicable_groups parseable
        if r["applicable_groups"]:
            pops = [p.strip() for p in r["applicable_groups"].split(",") if p.strip()]
            unknown = [p for p in pops if p not in KNOWN_POPS]
            if unknown:
                errors.append(f"V5 WARN {code}: unknown population code(s): {unknown}")

    conn.close()
    count = conn.execute if False else None  # ensure conn.execute not used after close

    # Reopen to get count
    conn2 = sqlite3.connect(str(DB_PATH))
    total = conn2.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    conn2.close()

    if errors:
        print(f"items validation: {len(errors)} issue(s) across {total} items")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"items validation: PASS ({total} items, all codes valid)")
        sys.exit(0)


if __name__ == "__main__":
    validate()
