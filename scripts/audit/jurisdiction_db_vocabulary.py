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

# Tables whose `jurisdiction` names a CANDIDATE, not a place the project holds
# evidence for. lang_jur_map is a language-to-jurisdiction reference map covering
# roughly twenty further ISO codes the project may expand into -- the "Phase 3
# expansion" validate_jurisdiction.py warns about. Gating it against the declared
# enum would force every candidate to be admitted as a declared jurisdiction just
# to be listed as a possibility, which inverts what the enum is for.
#
# This is an exemption list and rule 8 dislikes those. It is kept because the
# burden of proof sits on the exclusions: two tables, each with its reason stated
# here, against a table set DERIVED from the live schema.
CANDIDATE_TABLES = {"lang_jur_map"}

# Tables where an undeclared code is REPORTED but does not fail the check. These
# are base-vocabulary stores, not admitted evidence: term_aliases.jurisdiction
# records where an alias is USED, so it reaches places the corpus holds no
# evidence for. An undeclared value here is a question for the owner -- admit the
# jurisdiction, or fix a mis-filed value -- and not a reason to block a push on
# work that did not cause it. The GB rule still FAILS everywhere, because that
# one is ruled.
REPORT_ONLY = {"term_aliases"}


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

    findings, reported, examined = [], [], 0
    for t in tables:
        for bad, good in bad_map.items():
            n = conn.execute(
                f'SELECT COUNT(*) FROM "{t}" WHERE jurisdiction = ?', (bad,)).fetchone()[0]
            examined += 1
            if n:
                findings.append(f"  {t}.jurisdiction: {n} row(s) hold '{bad}' "
                                f"-- rejected, must be '{good}'")

    # Every corpus value must be a DECLARED code. Possible since 2026-09-18, when
    # the owner admitted BE/ES/HR/IT/INT -- before that the corpus held codes the
    # enum did not declare, so the declared vocabulary could not gate the column
    # it describes and this half of the check would have failed on correct data.
    declared, undeclared_note = set(), ""
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from schemas.enums import JurisdictionCode
        declared = {e.value for e in JurisdictionCode}
    except Exception as exc:                                    # pragma: no cover
        undeclared_note = f"  [SKIPPED] could not import JurisdictionCode: {exc}"
    if declared:
        for t in tables:
            if t in CANDIDATE_TABLES:
                continue
            vals = {r[0] for r in conn.execute(
                f'SELECT DISTINCT jurisdiction FROM "{t}" WHERE jurisdiction IS NOT NULL')}
            examined += len(vals)
            for v in sorted(v for v in vals if v not in declared):
                n = conn.execute(f'SELECT COUNT(*) FROM "{t}" WHERE jurisdiction = ?',
                                 (v,)).fetchone()[0]
                msg = (f"  {t}.jurisdiction: {n} row(s) hold '{v}', which "
                       f"JurisdictionCode does not declare. Either it is a real "
                       f"jurisdiction the owner should admit to the enum, or it is "
                       f"not a jurisdiction at all and the value is mis-filed.")
                (reported if t in REPORT_ONLY else findings).append(msg)

    print(f"Rejected spellings, read from {PHILOSOPHY.relative_to(REPO_ROOT)}: {bad_map}")
    print(f"Declared codes in JurisdictionCode: {len(declared)}")
    print(f"Tables with a jurisdiction column (derived, {len(EXEMPT)} exempt, "
          f"{len(CANDIDATE_TABLES)} candidate-only): {len(tables)}")
    if undeclared_note:
        print(undeclared_note)
    if reported:
        print("REPORTED (base vocabulary, not blocking -- owner decision):")
        print("\n".join(reported))
    if findings:
        print("\n".join(findings))
    print(f"EXAMINED: {examined} (table x rejected-spelling pair)")
    print(f"VERDICT: {'FAIL' if findings else 'PASS'}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
