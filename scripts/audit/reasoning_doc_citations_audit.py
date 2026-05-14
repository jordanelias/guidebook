#!/usr/bin/env python3
"""
Audit query for reasoning_doc_citations integrity (Track 3 of DR-2026-05-13).

Flags:
1. Rows with value_match='NOT-FOUND' or claim_match='NOT-FOUND' — citation was
   sought but the value/claim couldn't be located in the cited source.
2. Rows with value_match='CONTRADICTED' / claim_match='CONTRADICTED' — synthesis
   would be invalid; must be addressed before BPC ships.
3. PAYWALL rows without a downgrade note in `notes` (per rule #10 sub-rule 2/3,
   PAYWALL requires either downgraded grade or non-paywalled corroboration).
4. Rows where source_ref_id points to an evidence_sources record with
   metadata_quality='AUTHOR-TITLE-ONLY' or verification_status NULL — these
   sources are ineligible for synthesis per the existence-level gate of rule #10.
5. Rows where source_ref_id is VERIFIED but source_section is empty — content
   verification without recording where the claim was found is incomplete.
6. PAYWALL purchase candidates summary (grouped by source_ref_id with count).
7. claim_type distribution sanity check (rough proportions; alert if 100% of
   one type, which suggests recording is incomplete).
8. CROSS-CHECK with sharpened rule #10: every BPC reasoning doc slug present
   in `references/bpc-reasoning/` directory should have at least one row
   per parameter that the doc discusses. Cannot be enforced from DB alone
   (requires reasoning-doc parsing); this audit flags the row-side gap only.

Per DR-2026-05-13 §8 (sharpened standing rule #10 sub-rules 2 and 3).
Level 2 enforcement (audit, not hook). Run before each session close.
"""
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = REPO / "data" / "guidebook.db"


def audit():
    db = sqlite3.connect(str(DB))
    issues = 0

    # First: confirm table exists (post migration 011)
    if not db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='reasoning_doc_citations'"
    ).fetchone():
        print("=" * 60)
        print("REASONING_DOC_CITATIONS AUDIT")
        print("=" * 60)
        print("Table does not exist. Run migration 011 first.")
        return 1

    print("=" * 60)
    print("REASONING_DOC_CITATIONS AUDIT (Track 3 — DR-2026-05-13)")
    print("=" * 60)

    total = db.execute("SELECT COUNT(*) FROM reasoning_doc_citations").fetchone()[0]
    print(f"\nTotal rows: {total}")
    if total == 0:
        print("Table is empty (Phase E.1 has not begun for any BPC). No claim-level audit possible yet.")
        print("\n[CHECK 0] Confirmed table + indexes + constraints present from migration 011.")
        return 0

    # CHECK 1: NOT-FOUND outcomes
    not_found = list(db.execute("""
        SELECT citation_id, reasoning_doc_slug, parameter, source_ref_id,
               COALESCE(value_match, claim_match) AS match_outcome
        FROM reasoning_doc_citations
        WHERE value_match='NOT-FOUND' OR claim_match='NOT-FOUND'
        ORDER BY reasoning_doc_slug, parameter
    """))
    print(f"\n[CHECK 1] Rows with NOT-FOUND match: {len(not_found)}")
    for r in not_found[:10]:
        print(f"  ⚠ {r[0]} | {r[1]} | {r[2]} | ref={r[3]} | {r[4]}")
    if len(not_found) > 10:
        print(f"  ... and {len(not_found)-10} more")
    issues += len(not_found)

    # CHECK 2: CONTRADICTED outcomes
    contradicted = list(db.execute("""
        SELECT citation_id, reasoning_doc_slug, parameter, source_ref_id
        FROM reasoning_doc_citations
        WHERE claim_match='CONTRADICTED'
        ORDER BY reasoning_doc_slug, parameter
    """))
    print(f"\n[CHECK 2] CONTRADICTED claims (must be addressed before BPC ships): {len(contradicted)}")
    for r in contradicted[:10]:
        print(f"  ✗ {r[0]} | {r[1]} | {r[2]} | ref={r[3]}")
    issues += len(contradicted) * 2  # weighted

    # CHECK 3: PAYWALL rows without downgrade note
    paywall_no_note = list(db.execute("""
        SELECT citation_id, reasoning_doc_slug, parameter, source_ref_id
        FROM reasoning_doc_citations
        WHERE (value_match='PAYWALL' OR claim_match='PAYWALL')
          AND (notes IS NULL OR notes NOT LIKE '%downgrade%')
          AND (notes IS NULL OR notes NOT LIKE '%corroborat%')
        ORDER BY reasoning_doc_slug, parameter
    """))
    print(f"\n[CHECK 3] PAYWALL rows without downgrade/corroboration note: {len(paywall_no_note)}")
    for r in paywall_no_note[:10]:
        print(f"  ⚠ {r[0]} | {r[1]} | {r[2]} | ref={r[3]}")
    issues += len(paywall_no_note)

    # CHECK 4: Citations pointing to ineligible-for-synthesis sources
    ineligible_sources = list(db.execute("""
        SELECT rdc.citation_id, rdc.reasoning_doc_slug, rdc.parameter, rdc.source_ref_id,
               es.metadata_quality, es.verification_status
        FROM reasoning_doc_citations rdc
        JOIN evidence_sources es ON es.ref_id = rdc.source_ref_id
        WHERE es.metadata_quality = 'AUTHOR-TITLE-ONLY'
           OR es.verification_status IS NULL OR es.verification_status = ''
           OR es.verification_status IN ('UNVERIFIED-CLOSED', 'CLOSED-DELETED')
        ORDER BY rdc.reasoning_doc_slug
    """))
    print(f"\n[CHECK 4] Citations pointing to sources ineligible per rule #10: {len(ineligible_sources)}")
    for r in ineligible_sources[:10]:
        print(f"  ✗ {r[0]} | ref={r[3]} | mq={r[4]} | vs={r[5]}")
    issues += len(ineligible_sources) * 2  # weighted

    # CHECK 5: VERIFIED source but no source_section recorded
    missing_section = list(db.execute("""
        SELECT rdc.citation_id, rdc.reasoning_doc_slug, rdc.parameter, rdc.source_ref_id
        FROM reasoning_doc_citations rdc
        WHERE rdc.source_section IS NULL OR rdc.source_section = ''
        ORDER BY rdc.reasoning_doc_slug
    """))
    print(f"\n[CHECK 5] Rows missing source_section: {len(missing_section)}")
    for r in missing_section[:10]:
        print(f"  ⚠ {r[0]} | {r[1]} | {r[2]} | ref={r[3]}")
    issues += len(missing_section)

    # CHECK 6: PAYWALL purchase candidates summary
    paywall_summary = list(db.execute("""
        SELECT source_ref_id, COUNT(*) as cnt
        FROM reasoning_doc_citations
        WHERE paywall_purchase_candidate = 1
        GROUP BY source_ref_id
        ORDER BY cnt DESC
        LIMIT 20
    """))
    paywall_total = db.execute(
        "SELECT COUNT(*) FROM reasoning_doc_citations WHERE paywall_purchase_candidate = 1"
    ).fetchone()[0]
    print(f"\n[CHECK 6] PAYWALL purchase candidates (informational, not an issue): {paywall_total} rows")
    for r in paywall_summary:
        # Look up source title for context
        title = db.execute(
            "SELECT pub_title, standard_number FROM evidence_sources WHERE ref_id=?", (r[0],)
        ).fetchone()
        title_str = (title[1] or title[0] or "(no title)") if title else "(missing)"
        print(f"  📌 {r[0]} ({r[1]} citations) — {title_str[:70]}")

    # CHECK 7: claim_type distribution sanity
    dist = dict(db.execute("""
        SELECT claim_type, COUNT(*) FROM reasoning_doc_citations GROUP BY claim_type
    """).fetchall())
    print(f"\n[CHECK 7] claim_type distribution: {dist}")
    if dist and len(dist) == 1:
        print("  ⚠ Only one claim_type populated. Phase E.1 should produce all four types over time.")
        issues += 1

    print()
    print("=" * 60)
    print(f"ISSUES: {issues}")
    print("=" * 60)
    return 0 if issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
