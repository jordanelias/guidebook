#!/usr/bin/env python3
"""
Audit query for adversarial research protocol compliance.
Flags closed gaps that lack required protocol fields.

Per DR-2026-05-09. Run before each session close.
"""
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = REPO / "data" / "guidebook.db"

def audit():
    db = sqlite3.connect(str(DB))
    
    # Find gaps closed-via-research that lack protocol fields
    research_closed = db.execute("""
        SELECT gap_id, category, section, status, description
        FROM gaps
        WHERE status IN ('CLOSED-FIXED', 'CLOSED-RESOLVED')
        AND (
            category = 'RP'
            OR description LIKE '%research%'
            OR description LIKE '%RESEARCH%'
            OR description LIKE '%FDR%'
            OR description LIKE '%THIN-BASE%'
            OR description LIKE '%THIN BASE%'
        )
        ORDER BY gap_id
    """).fetchall()
    
    deficient = []
    for gap_id, cat, section, status, desc in research_closed:
        # Check protocol fields
        row = db.execute("""
            SELECT confidence_interval, shift_conditions, named_dissenter, falsification_condition
            FROM gaps WHERE gap_id = ?
        """, (gap_id,)).fetchone()
        
        ci, shift, dissenter, falsif = row
        missing = []
        if not ci: missing.append('confidence_interval')
        if not shift: missing.append('shift_conditions')
        if not dissenter: missing.append('named_dissenter')
        if not falsif: missing.append('falsification_condition')
        
        if missing:
            deficient.append((gap_id, section, status, missing))
    
    # Open gaps that should also have protocol fields once researched
    open_research = db.execute("""
        SELECT COUNT(*) FROM gaps WHERE status = 'OPEN' AND category = 'RP'
    """).fetchone()[0]
    
    # Population matches
    pop_match_count = db.execute("SELECT COUNT(*) FROM evidence_population_match").fetchone()[0]
    closed_with_evidence = db.execute("""
        SELECT COUNT(*) FROM gaps 
        WHERE status IN ('CLOSED-FIXED','CLOSED-RESOLVED')
        AND category = 'RP'
    """).fetchone()[0]
    
    # Report
    print("=" * 60)
    print("ADVERSARIAL RESEARCH PROTOCOL — COMPLIANCE AUDIT")
    print("=" * 60)
    print(f"\nResearch gaps closed without protocol fields: {len(deficient)}")
    print(f"Research gaps still OPEN (await protocol-compliant closure): {open_research}")
    print(f"Population match records: {pop_match_count}")
    print(f"Closed-with-research / population-matches ratio: {closed_with_evidence}/{pop_match_count}")
    
    if deficient:
        print(f"\n--- DEFICIENT GAPS ({len(deficient)}) ---")
        for gap_id, section, status, missing in deficient[:20]:
            print(f"  {gap_id} [{section}] {status}: missing {', '.join(missing)}")
        if len(deficient) > 20:
            print(f"  ... +{len(deficient)-20} more")
    
    # Match grade distribution check
    if pop_match_count > 0:
        grades = db.execute("""
            SELECT match_grade, COUNT(*) FROM evidence_population_match GROUP BY match_grade
        """).fetchall()
        total = sum(c for _, c in grades)
        print(f"\n--- POPULATION MATCH DISTRIBUTION ---")
        for grade, count in grades:
            pct = round(100 * count / total)
            flag = " ⚠ SUSPECT (>70% EXACT)" if grade == 'EXACT' and pct > 70 else ""
            print(f"  {grade}: {count} ({pct}%){flag}")
    
    # Exit code: 0 = clean, 1 = deficient
    return 0 if not deficient else 1


if __name__ == "__main__":
    sys.exit(audit())
