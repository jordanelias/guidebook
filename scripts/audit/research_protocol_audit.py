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
7. Verified citations lacking prior_expectation (added 2026-05-10 Stage B.5)
8. Verified citations lacking search_queries_used (added 2026-05-10 Stage B.5)
9. search_languages with status=SEARCHED but no PROTOCOL: marker in notes
   (added 2026-05-10 Stage B.5; supports multilingual remediation auditability)

Per DR-2026-05-09 (CHECK 1-6) and Stage B.5 audit findings 2026-05-10 (CHECK 7-9).
Run before each session close.
"""
import os
import sqlite3
import sys
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))


def audit():
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
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

    # CHECK 7 (added 2026-05-10; REPOINTED 2026-09-03, exactly as CHECK 8 was).
    #
    # DR-2026-05-09 §24 defines the field as "what Claude expected BEFORE searching",
    # logged in advance to expose confirmation bias. It was read off
    # evidence_sources.prior_expectation -- a RESEARCH-stage fact copied onto an
    # evidence row, the same §2.2 violation CHECK 8 was repointed for below. Worse
    # than a copy: evidence rows are written in the LOG action, AFTER the source has
    # been searched, screened, retrieved and read, so the column could never be
    # honestly populated where it sat. A prior written after reading the source is a
    # post-hoc rationalisation wearing the field that exists to prevent one, and this
    # check was therefore demanding the artefact it exists to forbid.
    #
    # Migration 069 gives search_executions the column; db.py writes it at log-search
    # time and add-source no longer accepts it. The pointer is v_source_admission,
    # which reaches search_executions through search_admissions on the shared
    # reference id -- the identical route CHECK 8 uses.
    #
    # evidence_sources.prior_expectation is NOT dropped: four committed data
    # migrations INSERT it and CLAUDE.md rule 5 makes such a column undroppable.
    # Writer-retired, now reader-retired, NULL forward. It held 0 non-empty values.
    verified_no_prior = db.execute("""
        SELECT e.ref_id, e.pub_title AS title
        FROM evidence_sources e
        LEFT JOIN v_source_admission v ON v.ref_id = e.ref_id
        WHERE e.verification_status = 'VERIFIED'
        GROUP BY e.ref_id
        HAVING COALESCE(MAX(NULLIF(TRIM(v.prior_expectation), '')), '') = ''
    """).fetchall()

    # CHECK 8 (added 2026-05-10; REPOINTED 2026-08-25).
    #
    # The query that surfaced a source is a RESEARCH-stage fact. It was being read off
    # evidence_sources.search_queries_used -- a research fact copied onto an evidence
    # row, which is the §2.2 violation the stage ruling forbids. The pointer is
    # v_source_admission, which reaches search_executions.query_text through
    # search_admissions on the shared reference id.
    #
    # Verified before repointing: all 10 rows holding the copy are reachable through
    # the pointer WITH a non-empty query_text, so this check loses no subject.
    verified_no_queries = db.execute("""
        SELECT e.ref_id, e.pub_title AS title
        FROM evidence_sources e
        LEFT JOIN v_source_admission v ON v.ref_id = e.ref_id
        WHERE e.verification_status = 'VERIFIED'
        GROUP BY e.ref_id
        HAVING COALESCE(MAX(NULLIF(TRIM(v.query_text), '')), '') = ''
    """).fetchall()

    # CHECK 9 (added 2026-05-10): search_languages with status=SEARCHED but no
    # PROTOCOL: marker in notes. Markers are: 'PROTOCOL: FULL', 'PROTOCOL: PARTIAL',
    # 'PROTOCOL: PRE-REMEDIATION'. Without these, multilingual remediation
    # compliance is unverifiable from the DB.
    unmarked_langs = db.execute("""
        SELECT slug, language FROM search_languages
        WHERE status = 'SEARCHED'
        AND (notes IS NULL OR notes NOT LIKE 'PROTOCOL:%')
        ORDER BY slug, language
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

    print(f"\n[CHECK 7] Verified citations lacking prior_expectation: {len(verified_no_prior)}")
    for ref_id, title in verified_no_prior[:5]:
        print(f"  ⚠ {ref_id}: {(title or '')[:70]}")

    print(f"\n[CHECK 8] Verified citations lacking search_queries_used: {len(verified_no_queries)}")
    for ref_id, title in verified_no_queries[:5]:
        print(f"  ⚠ {ref_id}: {(title or '')[:70]}")

    print(f"\n[CHECK 9] search_languages with no PROTOCOL: marker: {len(unmarked_langs)}")
    if unmarked_langs:
        # Group by slug for compact output
        by_slug = {}
        for slug, lang in unmarked_langs:
            by_slug.setdefault(slug, []).append(lang)
        for slug in sorted(by_slug)[:5]:
            langs = ','.join(sorted(by_slug[slug]))
            print(f"  ⚠ {slug}: {langs}")
        if len(by_slug) > 5:
            print(f"  ... and {len(by_slug) - 5} more slugs")

    # Summary
    total_issues = (len(deficient) + len(unmatched_verified) + 
                    (1 if suspicious_grades else 0) + len(narrative_ci) + 
                    len(topic_evidence_pattern) + len(unlogged_none_found) +
                    len(verified_no_prior) + len(verified_no_queries) +
                    len(unmarked_langs))
    
    # EXAMINED: the corpus rows actually queried across checks 1-9, not the
    # issue counts above (an issue count of 0 is ambiguous between "checked
    # and clean" and "nothing to check" — this disambiguates). Four source
    # tables feed these nine checks; summing their row counts is unambiguous
    # here because every one of them is presently empty (2026-08-06 clean-room
    # reset), so no combination could read as anything but zero.
    n_gaps = db.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]
    n_sources = db.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
    n_matches = db.execute("SELECT COUNT(*) FROM evidence_population_match").fetchone()[0]
    n_langs = db.execute("SELECT COUNT(*) FROM search_languages").fetchone()[0]
    n_examined = n_gaps + n_sources + n_matches + n_langs

    print(f"\n--- TOTAL ISSUES: {total_issues} ---")
    print(f"EXAMINED: {n_examined}")
    if total_issues == 0:
        print("Audit clean. Reminder: protocol creates audit trails, not truth.")
        print("Human spot-check is the actual control mechanism.")
    else:
        print("Reminder: protocol creates audit trails, not truth.")
        print("Human spot-check remains the control mechanism even on clean audits.")
    
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
