#!/usr/bin/env python3
"""scripts/audit/adversarial_pass_audit.py — the pass exists for what this session wrote.

WHY THIS EXISTS. Three canonical statements already require an adversarial pass on every
research/synthesis diff (the 2026-08-19 RULE; DR-2026-09-11 clause 2; pipeline-contract.yaml's
cross_stage/definition-of-done), and none of the three had a committed enforcer.
`claims_docket.py` scans for claim-words in prose; the word "adversarial" appears in its
comments only. Batch 20's own antagonist pass ran the SAME model as its author while its
record called it independent, and nothing caught that because nothing recorded a pass in
checkable form (DR-2026-09-26-recurring-defect-shapes-remediation.md, RC4).

THE SUBJECT TABLES are not a list in this file (CLAUDE.md rule 8). They are parsed from the
2026-08-19 RULE's own text in references/project-standards.md, anchored on a quote that must
occur exactly once. If the ruling's wording ever moves, this audit exits 2 ("cannot run")
rather than silently examining nothing.

THE COLUMNS are every column of those tables whose name ENDS in `_by_session` (a substring
match would wrongly catch bpc_metadata.supersession_check_complete). `connection_targets` is
NOT one of the RULE's limb-(a) tables and this script never touches it; it is named here only
because it is DR-2026-09-26 section 1.2's own example of why OQ-8's wider scope (every
writable table, not just the RULE's list) needs a separate design -- that table has no
`_by_session` column at all, so a widened version of this script would have to decide what
"this session wrote to it" even means there. This script's own subject, derived below, never
includes it.

SCOPE IS THE RULE'S LIST, DELIBERATELY, until the owner answers OQ-8 (widen to every writable
table). Widening this file ahead of that answer would implement OQ-8 while the DR text says
it is still open.

`CURRENT`, not `LATEST-RESEARCH`: the latter names the PREVIOUS session for the whole life of
the current one (CLAUDE.md section 7), so a mid-session check against it silently audits
someone else's batch. Accepts either spelling (bare stem or `<stem>.md`) when matching rows,
because CURRENT holds the bare form today but has not always (batches 11-15 wrote branch
slugs) and no row in any writable table carries the `.md` form (verified 2026-09-26).
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore                                                        # noqa: E402

REPO_ROOT = dbcore.REPO_ROOT
DB_PATH = dbcore.db_path()
LEDGER = REPO_ROOT / "references" / "project-standards.md"

_ANCHOR = ("An adversarial pass may be commissioned ONLY against a diff that (a) wrote "
           "rows to the research tables (")


def _rule_tables() -> list:
    """Table names parsed from the 2026-08-19 RULE's own limb (a), never listed here."""
    if not LEDGER.exists():
        return []
    text = LEDGER.read_text(encoding="utf-8")
    if text.count(_ANCHOR) != 1:
        return None
    i = text.index(_ANCHOR) + len(_ANCHOR)
    close = text.index(")", i)
    return re.findall(r"`([a-z_]+)`", text[i:close])


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] != "--session":
        print("usage: adversarial_pass_audit.py --session <session-stem-or-.md>")
        print("EXAMINED: 0")
        return 2
    session = sys.argv[2]
    stem = session[:-3] if session.endswith(".md") else session

    tables = _rule_tables()
    if tables is None:
        print(f"[ERROR] the RULE anchor occurs != 1 time in "
              f"{LEDGER.relative_to(REPO_ROOT)} -- the ruling's wording moved. Refusing "
              f"to guess the subject tables.")
        print("EXAMINED: 0")
        return 2
    if not tables:
        print(f"[ERROR] no subject tables parsed from {LEDGER.relative_to(REPO_ROOT)}.")
        print("EXAMINED: 0")
        return 2

    if not DB_PATH.exists():
        print(f"[ERROR] no database at {DB_PATH}.")
        print("EXAMINED: 0")
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    live = {t for (t,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}

    examined = 0
    per_table = {}
    for t in tables:
        if t not in live:
            continue
        cols = [c[1] for c in conn.execute(f'PRAGMA table_info("{t}")')
                if c[1].endswith("_by_session")]
        if not cols:
            continue  # a RULE table with no _by_session column has nothing this audit can match
        # ONE count per table, over an OR across every _by_session column it has — not
        # one count PER COLUMN summed. A table with both created_by_session and
        # updated_by_session double-counts a single row that matches on both under the
        # summed form; EXAMINED must be a row count, not a column-match count.
        where = " OR ".join(f'"{c}" IN (?, ?)' for c in cols)
        params = [v for _ in cols for v in (stem, stem + ".md")]
        n = conn.execute(f'SELECT COUNT(*) FROM "{t}" WHERE {where}', params).fetchone()[0]
        if n:
            per_table[t] = n
        examined += n

    print(f"Subject tables (RULE limb (a), derived): {sorted(tables)}")
    print(f"Session: {stem}")
    if per_table:
        print("Rows written into subject tables by this session:")
        for t, n in sorted(per_table.items()):
            print(f"  {t}: {n}")
    print(f"EXAMINED: {examined}")

    if examined == 0:
        print("VERDICT: PASS — NOTHING-IN-SCOPE (this session wrote no rows into the "
              "RULE's subject tables; it owes no pass).")
        return 0

    passes = conn.execute(
        "SELECT pass_id, closed_at, reviewer_models, author_models FROM adversarial_passes "
        "WHERE subject_session IN (?, ?)", (stem, stem + ".md")).fetchall()
    closed = [p for p in passes if p["closed_at"]]

    if not closed:
        if passes:
            print(f"FAIL: {len(passes)} pass(es) recorded for this session, but none is "
                  f"CLOSED (close-adversarial-pass). An open pass is not a finished one.")
        else:
            print("FAIL: no adversarial_passes row names this session, and it wrote to "
                  "the RULE's subject tables. Record the pass (db.py "
                  "record-adversarial-pass), then close it.")
        return 1

    reports = []
    for p in closed:
        try:
            rev = set(json.loads(p["reviewer_models"]))
            auth = set(json.loads(p["author_models"]))
        except (TypeError, ValueError):
            rev = auth = set()
        if rev & auth:
            reports.append(f"  pass {p['pass_id']}: reviewer/author model overlap {rev & auth} "
                           f"-- same-model pass. Whether this counts as independent is OQ-1, "
                           f"the owner's to answer; this audit only reports it.")
    undisposed = conn.execute(
        "SELECT f.finding_id FROM adversarial_findings f "
        "JOIN adversarial_passes p ON p.pass_id = f.pass_id "
        "WHERE p.subject_session IN (?, ?) AND f.verdict = 'SUSTAINED' "
        "AND f.disposition IS NULL", (stem, stem + ".md")).fetchall()
    if undisposed:
        reports.append(f"  {len(undisposed)} SUSTAINED finding(s) with no disposition: "
                       f"{[r['finding_id'] for r in undisposed]}")

    if reports:
        print("REPORTED (not blocking):")
        print("\n".join(reports))
    print(f"VERDICT: PASS — {len(closed)} closed pass(es) recorded for this session.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
