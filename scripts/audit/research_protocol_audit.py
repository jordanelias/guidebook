#!/usr/bin/env python3
"""
Audit query for adversarial research protocol compliance.

Flags:
1. Closed gaps lacking required protocol fields
2. Verified citations without population match records
3. Population match grade distribution suspicious (>70% EXACT)
4. Confidence intervals using narrative instead of numerical ranges
5. "Topic-evidence vs claim-evidence" pattern (per strict-review session)
6. NONE FOUND dissenter entries that lack logged search queries

Per DR-2026-05-09. Run before each session close.
"""
import sqlite3
import sys
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = REPO / "data" / "guidebook.db"


def audit():
    db = sqlite3.connect(str(DB))
    issues = []

    # CHECK 1: Research-closed gaps without protocol fields
    research_closed = db.execute("""
        SELECT gap_id, category, section, status FROM gaps
        WHERE status IN ('CLOSED-FIXED', 'CLOSED-RESOLVED')
        AND (category = 'RP' OR description LIKE '%research%' 
             OR description LIKE '%FDR%' OR description LIKE '%THIN-BASE%')
    """).fetchall()

    deficient = []
    for gap_id, cat, section, status in research_closed:
        row = db.execute("""SELECT confidence_interval, shift_conditions, named_dissenter, falsification_condition
                          FROM gaps WHERE gap_id = ?""", (gap_id,)).fetchone()
        missing = [f for f, v in zip(
            ['confidence_interval', 'shift_conditions', 'named_dissenter', 'falsification_condition'], row
        ) if not v]
        if missing:
            deficient.append((gap_id, section, status, missing))

    # CHECK 2: Verified citations without population match (uses ref_id FK)
    verified_refs = set(r[0] for r in db.execute(
        "SELECT ref_id FROM evidence_sources WHERE verification_status='VERIFIED'"))
    matched_refs = set(r[0] for r in db.execute(
        "SELECT DISTINCT ref_id FROM evidence_population_match WHERE ref_id IS NOT NULL"))
    unmatched_verified = verified_refs - matched_refs

    # CHECK 3: Suspicious population match grade distribution
    grades = dict(db.execute("SELECT match_grade, COUNT(*) FROM evidence_population_match GROUP BY match_grade").fetchall())
    total_matches = sum(grades.values())
    exact_pct = round(100 * grades.get('EXACT', 0) / total_matches) if total_matches else 0
    suspicious_grades = exact_pct > 70

    # CHECK 4: Narrative confidence intervals (should be numerical ranges)
    narrative_ci = db.execute("""
        SELECT gap_id, confidence_interval FROM gaps
        WHERE confidence_interval IS NOT NULL
        AND confidence_interval NOT GLOB '*[0-9]*-[0-9]*%*'
        AND confidence_interval != 'NOT-RESEARCHED'
    """).fetchall()

    # CHECK 5: Topic-evidence vs claim-evidence pattern
    # Look for closed gaps where dissenter mentions standard/citation but doesn't address SPECIFIC claim
    topic_evidence_pattern = db.execute("""
        SELECT gap_id, named_dissenter FROM gaps
        WHERE status IN ('CLOSED-FIXED', 'CLOSED-RESOLVED')
        AND named_dissenter LIKE 'NONE FOUND%'
        AND named_dissenter NOT LIKE '%STRICT REVIEW%'
        AND named_dissenter NOT LIKE '%queries used%'
        AND named_dissenter NOT LIKE '%logged queries%'
    """).fetchall()

    # CHECK 6: NONE FOUND without logged queries
    unlogged_none_found = db.execute("""
        SELECT gap_id, named_dissenter FROM gaps
        WHERE named_dissenter LIKE 'NONE FOUND%'
        AND named_dissenter NOT LIKE '%search%' 
        AND named_dissenter NOT LIKE '%queries%'
        AND named_dissenter NOT LIKE '%review%'
    """).fetchall()

    # Report
    print("=" * 60)
    print("ADVERSARIAL RESEARCH PROTOCOL — COMPLIANCE AUDIT")
    print("=" * 60)
    
    print(f"\n[CHECK 1] Research gaps closed without protocol fields: {len(deficient)}")
    if deficient:
        for gap_id, section, status, missing in deficient[:10]:
            print(f"  ⚠ {gap_id} [{section}] {status}: missing {', '.join(missing)}")
    
    print(f"\n[CHECK 2] Verified citations without population match: {len(unmatched_verified)}")
    for ref in sorted(unmatched_verified)[:5]:
        print(f"  ⚠ {ref}: needs evidence_population_match record")

    print(f"\n[CHECK 3] Population match grade distribution:")
    for g, c in sorted(grades.items()):
        flag = " ⚠ SUSPECT (>70% EXACT)" if g == 'EXACT' and exact_pct > 70 else ""
        print(f"  {g}: {c} ({round(100*c/total_matches)}%){flag}")

    print(f"\n[CHECK 4] Narrative (non-numerical) confidence intervals: {len(narrative_ci)}")
    for gap_id, ci in narrative_ci[:5]:
        print(f"  ⚠ {gap_id}: '{ci}' should be numerical range like '60-75%'")

    print(f"\n[CHECK 5] Closed-with-NONE-FOUND lacking review markers: {len(topic_evidence_pattern)}")
    if topic_evidence_pattern:
        print(f"  Pattern: closure asserts no dissent without showing what was searched.")
        for gap_id, dissent in topic_evidence_pattern[:3]:
            print(f"  ⚠ {gap_id}: '{dissent[:80]}'")

    print(f"\n[CHECK 6] NONE FOUND without logged search queries: {len(unlogged_none_found)}")
    for gap_id, dissent in unlogged_none_found[:3]:
        print(f"  ⚠ {gap_id}: '{dissent[:80]}'")

    # Summary
    total_issues = (len(deficient) + len(unmatched_verified) + 
                    (1 if suspicious_grades else 0) + len(narrative_ci) + 
                    len(topic_evidence_pattern) + len(unlogged_none_found))
    
    print(f"\n--- TOTAL ISSUES: {total_issues} ---")
    if total_issues == 0:
        print("Audit clean. Reminder: protocol creates audit trails, not truth.")
        print("Human spot-check is the actual control mechanism.")
    
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
