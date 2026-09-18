#!/usr/bin/env python3
"""scripts/audit/jurisdiction_db_vocabulary.py — jurisdiction codes IN THE DATABASE.

WHY THIS EXISTS. `governance/jurisdiction-philosophy.md` states the UK/GB rule at
ERROR level -- "GB appearing as a jurisdiction code is rejected; must be UK" -- and
says on line 116 that it is "enforced by the validator". It was not enforced on the
database. `validate_jurisdiction.py` globs source YAML and the standards-registry
markdown; it never reads a table. So it passed with 0 errors over a corpus holding
27 rows of the rejected code across five tables, two of which were written the same
day by the session that then found this.

That is CLAUDE.md failure mode (b) inverted: not prose contradicting the database,
but prose CLAIMING an enforcement the database never had.

The tables are DERIVED from the live schema, never listed here (rule 8): any table
with a `jurisdiction` column is in scope the moment it is created. The rejected
spellings are read from the governance document that rules on them, so this file
holds no vocabulary of its own.
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
PHILOSOPHY = REPO_ROOT / "governance" / "jurisdiction-philosophy.md"

# Columns that are named `jurisdiction` but are not one. source_locators.jurisdiction
# holds free text -- cost figures, percentages, prose -- across most of its populated
# rows. That is a real defect and it is GAP-008's column-shuffle territory, not this
# check's: flagging 343 prose strings as bad jurisdiction codes would drown the
# signal this check exists for.
EXEMPT = {"source_locators"}


def rejected_spellings() -> dict:
    """{bad: good} read from the governance table that rules on it, not hardcoded."""
    out = {}
    if not PHILOSOPHY.exists():
        return out
    for line in PHILOSOPHY.read_text(encoding="utf-8").splitlines():
        # e.g. "| UK not GB | ERROR | `GB` ... is rejected; must be `UK` |"
        m = re.search(r"`([A-Z]{2,4})`[^|]*rejected[^|]*must be\s+`([A-Z]{2,4})`", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def main() -> int:
    conn = sqlite3.connect(f"file:{DEFAULT_DB}?mode=ro", uri=True)
    bad_map = rejected_spellings()
    if not bad_map:
        print("[ERROR] no rejected-spelling rule parsed from "
              f"{PHILOSOPHY.relative_to(REPO_ROOT)} -- the rule moved or the table "
              "changed shape. Refusing to pass by finding nothing to check.")
        print("EXAMINED: 0")
        return 1

    tables = []
    for (t,) in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"):
        if t in EXEMPT:
            continue
        if any(c[1] == "jurisdiction" for c in conn.execute(f'PRAGMA table_info("{t}")')):
            tables.append(t)

    findings, examined = [], 0
    for t in tables:
        for bad, good in bad_map.items():
            n = conn.execute(
                f'SELECT COUNT(*) FROM "{t}" WHERE jurisdiction = ?', (bad,)).fetchone()[0]
            examined += 1
            if n:
                findings.append(f"  {t}.jurisdiction: {n} row(s) hold '{bad}' "
                                f"-- rejected, must be '{good}'")

    print(f"Rejected spellings, read from {PHILOSOPHY.relative_to(REPO_ROOT)}: {bad_map}")
    print(f"Tables with a jurisdiction column (derived, {len(EXEMPT)} exempt): {len(tables)}")
    if findings:
        print("\n".join(findings))
    print(f"EXAMINED: {examined} (table x rejected-spelling pair)")
    print(f"VERDICT: {'FAIL' if findings else 'PASS'}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
