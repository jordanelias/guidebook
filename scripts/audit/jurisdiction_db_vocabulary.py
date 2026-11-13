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
# vocabulary would force every candidate to be admitted as a declared jurisdiction just
# to be listed as a possibility, which inverts what the vocabulary is for.
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

    # Every corpus value must be a DECLARED code, one a row of base_jurisdictions holds.
    # With no table (a database below the migration that creates base_jurisdictions) dbcore raises a Refusal, and with an
    # empty one there is no vocabulary: either way this check examined no code, which is
    # failure mode (a), so it FAILS with the reason rather than passing.
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import dbcore
    try:
        declared = dbcore.declared_jurisdictions()
        if not declared:
            raise dbcore.Refusal("base_jurisdictions holds no rows, so no corpus value can "
                                 "be checked against it")
    except dbcore.Refusal as exc:
        print(f"[ERROR] {exc}\nEXAMINED: 0\nVERDICT: FAIL")
        return 1
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
                   f"base_jurisdictions does not hold. Either it is a real "
                   f"jurisdiction the owner should admit (db.py add-jurisdiction), or it is "
                   f"not a jurisdiction at all and the value is mis-filed.")
            (reported if t in REPORT_ONLY else findings).append(msg)

    # AT REST, EVERY ADMISSION ANSWERS FOR ITSELF. A row the verb wrote carries the dated ledger
    # heading that records its approval; a seed row (the migration's) carries neither a pointer
    # nor a session. So a pointer must be found exactly once in the ledger and the entry must
    # name the code (the verb's own test, dbcore.ledger_entry_names), and a row with no pointer
    # but a session landed without an approval (a raw INSERT, or a pointer cleared afterwards).
    for code, ref, session in conn.execute(
            "SELECT jurisdiction_code, admission_ref, created_by_session FROM base_jurisdictions"):
        examined += 1
        if ref is None:
            if session is not None:
                findings.append(f"  base_jurisdictions.{code}: landed without an approval "
                                f"(no admission_ref, written by {session})")
        elif dbcore.ledger_heading_count(ref) != 1:
            findings.append(f"  base_jurisdictions.{code}: admission_ref {ref!r} is the heading of "
                            f"{dbcore.ledger_heading_count(ref)} ledger entries; it must be exactly one")
        elif ref.startswith(dbcore.LEDGER_DELEGATED_PREFIX):
            findings.append(f"  base_jurisdictions.{code}: admission_ref {ref!r} is a delegated "
                            f"resolution, not the owner's words; scope is the owner's decision")
        elif not dbcore.ledger_entry_names(ref, code):
            findings.append(f"  base_jurisdictions.{code}: the ledger entry {ref!r} does not name "
                            f"{code!r}")

    print(f"Rejected spellings, read from {PHILOSOPHY.relative_to(REPO_ROOT)}: {bad_map}")
    print(f"Declared codes in base_jurisdictions: {len(declared)}")
    print(f"Tables with a jurisdiction column (derived, {len(EXEMPT)} exempt, "
          f"{len(CANDIDATE_TABLES)} candidate-only): {len(tables)}")
    if reported:
        print("REPORTED (base vocabulary, not blocking -- owner decision):")
        print("\n".join(reported))
    if findings:
        print("\n".join(findings))
    print(f"EXAMINED: {examined} (table x rejected-spelling pair, declared value, admission row)")
    print(f"VERDICT: {'FAIL' if findings else 'PASS'}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
