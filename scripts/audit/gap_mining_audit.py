#!/usr/bin/env python3
"""
Audit query for gap-driven mining protocol compliance (DR-2026-05-26).

Flags:
1. Closed gaps lacking gap_mining row when description signals mining-addressability
   (an OPEN-ADDRESSABLE gap moved to CLOSED-FIXED with no gap_mining attempt
   recorded indicates a backdoor closure that bypassed the protocol).
2. gap_mining rows with outcome=closure_evidence_found whose gap lacks the four
   adversarial-research fields (rule #7 interlock).
3. gap_mining rows with outcome=closure_evidence_found on a numerical-spec gap
   that lacks a matching spec_value_probes walk (rule #8 interlock).
4. gap_mining rows with outcome=gap_recategorized whose gap.mining_addressability
   is still ADDRESSABLE (re-categorization not committed to the gap row).
5. gaps with mining_addressability IS NULL and status LIKE 'OPEN%' — triage
   backlog. Informational; counted but not failure-grade.
6. gap_mining rows with discoveries_logged populated but no corresponding
   evidence_sources rows for the listed ref_ids (closure workflow §4.3 step 1
   not completed).
7. gap_mining rows with candidate_dois populated where the DOIs ALREADY exist in
   evidence_sources — the candidate was verified and INSERTed but the
   gap_mining row was not updated to move the DOI to discoveries_logged.
   (Mirrors supersession_check.superseding_dois → superseding_ref_ids promotion
   pattern.)

Per DR-2026-05-26 §Status (adoption gate). Run before each session close that
involved gap-driven mining.

Exit codes: 0 = pass (or only informational findings); 1 = any failure-grade
            check found issues.

DB path: data/guidebook.db (override via GUIDEBOOK_DB_PATH).
Repo root: resolved relative to __file__.
"""
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))

# Patterns from DR §2 that signal mining-addressability
MINING_ADDRESSABLE_SIGNALS = re.compile(
    r"THIN[- ]BASE|thin base|\[RESEARCH TASK\]"
    r"|Co-1 evidence 0/|0/\d+ jurisdictions|Co-1 anchor missing"
    r"|no indexed evidence|no source for|no published evidence base"
    r"|standards named.*not promoted|standard not in evidence base"
    r"|population structurally invisible",
    re.IGNORECASE
)

# Numerical-spec signals (mm, s, lux, dB, NRC, NC, °C, %, N, LRV, kg, etc.)
NUMERICAL_SPEC_SIGNALS = re.compile(
    r"\b\d+\s*(mm|cm|m|s|ms|lux|lx|dB|dBA|dB\(A\)|NC|NRC|°C|C|%|N|kg|kN|mPa|Pa|LRV|cd/m)",
    re.IGNORECASE
)


def audit():
    if not DB_PATH.exists():
        print(f"FAIL: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row

    # Verify migration 017 applied
    user_version = db.execute("PRAGMA user_version").fetchone()[0]
    if user_version < 17:
        print(f"FAIL: schema version {user_version} < 17; migration 017 not applied")
        return 1
    tbl = db.execute(
        "SELECT 1 FROM sqlite_master WHERE name='gap_mining'"
    ).fetchone()
    if not tbl:
        print("FAIL: gap_mining table missing")
        return 1

    issues_failure = []
    issues_info = []

    # ─── CHECK 1: backdoor closures (mining-addressable gap closed without a
    #             gap_mining row) ──────────────────────────────────────────
    backdoor = db.execute("""
        SELECT g.gap_id, g.status, substr(g.description, 1, 100) AS snippet
          FROM gaps g
          LEFT JOIN gap_mining gm ON gm.gap_id = g.gap_id
         WHERE g.status LIKE 'CLOSED-FIXED%'
           AND g.mining_addressability = 'ADDRESSABLE'
           AND gm.gap_id IS NULL
    """).fetchall()
    # Filter by description pattern as secondary check (some legacy closures
    # may have been ADDRESSABLE-backfilled but actually closed by other path)
    for row in backdoor:
        if MINING_ADDRESSABLE_SIGNALS.search(row["snippet"] or ""):
            issues_failure.append(
                f"CHECK 1: {row['gap_id']} CLOSED-FIXED with mining_addressability=ADDRESSABLE "
                f"but no gap_mining row. Closure may have bypassed the protocol. "
                f"Snippet: {row['snippet'][:80]}..."
            )

    # ─── CHECK 2: closure outcomes lacking rule #7 fields ────────────────
    closure_rows = db.execute("""
        SELECT gm.gap_mining_id, gm.gap_id,
               g.falsification_condition, g.confidence_interval,
               g.shift_conditions, g.named_dissenter, g.status
          FROM gap_mining gm
          JOIN gaps g ON g.gap_id = gm.gap_id
         WHERE gm.outcome = 'closure_evidence_found'
    """).fetchall()
    for row in closure_rows:
        missing = [f for f, v in [
            ("falsification_condition", row["falsification_condition"]),
            ("confidence_interval", row["confidence_interval"]),
            ("shift_conditions", row["shift_conditions"]),
            ("named_dissenter", row["named_dissenter"]),
        ] if not v]
        if missing:
            issues_failure.append(
                f"CHECK 2: gap_mining_id={row['gap_mining_id']} ({row['gap_id']}) "
                f"closure_evidence_found but gap missing rule #7 fields: {missing}"
            )

    # ─── CHECK 3: numerical-spec closures lacking PMP walk ───────────────
    for row in closure_rows:
        # Re-fetch gap description and section to detect numerical-spec shape
        g = db.execute(
            "SELECT description, section FROM gaps WHERE gap_id = ?",
            (row["gap_id"],)
        ).fetchone()
        if not g:
            continue
        scan = f"{g['description'] or ''} {g['section'] or ''}"
        if NUMERICAL_SPEC_SIGNALS.search(scan):
            # Numerical-spec gap; require spec_value_probes row mentioning this
            # gap_id OR the gap's slug section.
            section = g["section"] or ""
            probe = db.execute("""
                SELECT 1 FROM spec_value_probes
                 WHERE slug = ?
                    OR notes LIKE ?
                 LIMIT 1
            """, (section, f"%{row['gap_id']}%")).fetchone()
            if not probe:
                issues_failure.append(
                    f"CHECK 3: gap_mining_id={row['gap_mining_id']} ({row['gap_id']}) "
                    f"closure on numerical-spec gap but no spec_value_probes walk "
                    f"found (section={section!r}). Rule #8 interlock."
                )

    # ─── CHECK 4: gap_recategorized rows where gap.mining_addressability is
    #             still ADDRESSABLE ─────────────────────────────────────────
    recat_rows = db.execute("""
        SELECT gm.gap_mining_id, gm.gap_id, g.mining_addressability
          FROM gap_mining gm
          JOIN gaps g ON g.gap_id = gm.gap_id
         WHERE gm.outcome = 'gap_recategorized'
    """).fetchall()
    for row in recat_rows:
        if row["mining_addressability"] == "ADDRESSABLE":
            issues_failure.append(
                f"CHECK 4: gap_mining_id={row['gap_mining_id']} ({row['gap_id']}) "
                f"gap_recategorized but gap.mining_addressability still ADDRESSABLE. "
                f"Run update-gap-addressability to commit the re-categorization."
            )

    # ─── CHECK 5: triage backlog (informational) ─────────────────────────
    backlog = db.execute("""
        SELECT COUNT(*) FROM gaps
         WHERE status LIKE 'OPEN%'
           AND mining_addressability IS NULL
    """).fetchone()[0]
    if backlog > 0:
        issues_info.append(
            f"CHECK 5: {backlog} OPEN gaps with mining_addressability=NULL "
            f"(triage backlog). Run update-gap-addressability per DR §3 default "
            f"class from gaps.skill."
        )

    # ─── CHECK 6: discoveries_logged ref_ids not in evidence_sources ─────
    disc_rows = db.execute("""
        SELECT gap_mining_id, gap_id, discoveries_logged
          FROM gap_mining
         WHERE discoveries_logged IS NOT NULL
           AND discoveries_logged != '[]'
    """).fetchall()
    for row in disc_rows:
        try:
            refs = json.loads(row["discoveries_logged"])
        except json.JSONDecodeError:
            issues_failure.append(
                f"CHECK 6: gap_mining_id={row['gap_mining_id']} discoveries_logged "
                f"is not valid JSON"
            )
            continue
        for ref_id in refs:
            existing = db.execute(
                "SELECT 1 FROM evidence_sources WHERE ref_id = ? LIMIT 1",
                (ref_id,)
            ).fetchone()
            if not existing:
                issues_failure.append(
                    f"CHECK 6: gap_mining_id={row['gap_mining_id']} ({row['gap_id']}) "
                    f"discoveries_logged names {ref_id} but no evidence_sources row "
                    f"exists. Closure workflow §4.3 step 1 incomplete."
                )

    # ─── CHECK 7: candidate_dois that have already been verified+INSERTed
    #             but not promoted from candidates to discoveries ────────
    cand_rows = db.execute("""
        SELECT gap_mining_id, gap_id, candidate_dois
          FROM gap_mining
         WHERE candidate_dois IS NOT NULL
           AND candidate_dois != '[]'
    """).fetchall()
    for row in cand_rows:
        try:
            dois = json.loads(row["candidate_dois"])
        except json.JSONDecodeError:
            issues_failure.append(
                f"CHECK 7: gap_mining_id={row['gap_mining_id']} candidate_dois "
                f"is not valid JSON"
            )
            continue
        for doi in dois:
            if not doi:
                continue
            existing = db.execute(
                "SELECT ref_id FROM evidence_sources WHERE doi = ? LIMIT 1",
                (doi,)
            ).fetchone()
            if existing:
                issues_failure.append(
                    f"CHECK 7: gap_mining_id={row['gap_mining_id']} ({row['gap_id']}) "
                    f"candidate_dois lists {doi} but evidence_sources already has "
                    f"ref_id={existing['ref_id']} for this DOI. Promote candidate "
                    f"to discoveries_logged or write a new gap_mining attempt."
                )

    # ─── Report ──────────────────────────────────────────────────────────
    print("=" * 68)
    print("Gap-driven mining protocol audit (DR-2026-05-26)")
    print("=" * 68)
    print()
    print(f"schema version: {user_version}")
    print(f"gap_mining rows: {db.execute('SELECT COUNT(*) FROM gap_mining').fetchone()[0]}")
    print(f"gaps with mining_addressability set: "
          f"{db.execute('SELECT COUNT(*) FROM gaps WHERE mining_addressability IS NOT NULL').fetchone()[0]}")
    print()

    if issues_failure:
        print(f"FAILURES: {len(issues_failure)}")
        for issue in issues_failure[:20]:
            print(f"  ✗ {issue}")
        if len(issues_failure) > 20:
            print(f"  ... and {len(issues_failure) - 20} more")
        print()
    else:
        print("FAILURES: 0")
        print()

    if issues_info:
        print(f"INFORMATIONAL: {len(issues_info)}")
        for issue in issues_info:
            print(f"  ⓘ {issue}")
        print()

    print("=" * 68)
    if not issues_failure:
        print("PASS. Reminder: protocol creates audit trails, not truth.")
        print("Human spot-check is the actual control mechanism.")
        return 0
    else:
        print("FAIL. See failures above.")
        return 1


if __name__ == "__main__":
    sys.exit(audit())
