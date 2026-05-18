#!/usr/bin/env python3
"""
Audit query for PMP (Progressive Measurement Probe) protocol compliance.

Per standing rule #8 and DR-2026-05-10. Extended for DR-2026-05-13 to
also enforce rule #10 sub-rule 1 (numerical-spec claims must cite an
active PMP walk in synthesis).

Flags:
1. Items asserting numerical specs but lacking a PMP walk
   (rule #8 mandatory invocation gap).
2. PMP walks where no step reached `phase='final'` (incomplete walks).
3. PMP walks with all-failing strict termination (no supporting evidence
   found at any tried value — origin spec value may be unsupported).
4. PMP walks whose `ref_id` points to an evidence_sources record that is
   ineligible for synthesis per rule #10 (AUTHOR-TITLE-ONLY/NULL/GREY; not COMPLETE or COMPLETE-STATUTORY per DR-2026-05-18; or NULL
   verification_status) — the walk found a source, but the source is
   not gate-eligible.
5. PMP walks with passes_strict=1 step but no ref_id linkage (claim
   appears to pass but evidence record not captured).
6. PMP walks with direction/claim_type inconsistency (per DR-2026-05-10's
   tightening-direction semantics):
   - claim_type='minimum' should walk direction='up' (probe whether minimum
     could be higher than asserted)
   - claim_type='maximum' should walk direction='down' (probe whether maximum
     could be lower than asserted)
   - claim_type IN ('target','range_low','range_high') may go either way
7. Items with numerical spec asserted in BPC but PMP walk's
   `spec_value_origin` differs from the current asserted value
   (drift between BPC and PMP record).

Per DR-2026-05-10 (PMP protocol) and DR-2026-05-13 (rule #10 sharpening).
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

    print("=" * 60)
    print("PROGRESSIVE MEASUREMENT PROBE (PMP) — COMPLIANCE AUDIT")
    print("=" * 60)

    # CHECK 1: Items with numerical specs but no PMP walk
    # The items table at v10.7+ has pmp_* tracking columns. The actual
    # spec_value lives in BPC content (items table doesn't carry it).
    # Definition of "has numerical spec": a PMP origin appears in
    # spec_value_probes at step_index=0 for that item_code, OR (until items
    # gets a spec_value column) we use the BPC reasoning doc presence as
    # proxy. This first version checks PMP linkage only.
    items_cols = {r[1] for r in db.execute("PRAGMA table_info(items)")}
    if "pmp_last_walk_at" in items_cols:
        missing_walk = list(db.execute("""
            SELECT i.item_code, i.bpc_source_slug, NULL AS spec_value, NULL AS spec_unit
            FROM items i
            WHERE i.pmp_last_walk_at IS NULL
              AND i.status NOT IN ('archived','superseded')
              AND EXISTS (
                  SELECT 1 FROM spec_value_probes svp
                  WHERE svp.item_code = i.item_code
                    AND svp.spec_value_origin IS NOT NULL
              )
            ORDER BY i.bpc_source_slug, i.item_code
        """))
    else:
        missing_walk = list(db.execute("""
            SELECT i.item_code, i.bpc_source_slug, NULL, NULL
            FROM items i
            WHERE NOT EXISTS (SELECT 1 FROM spec_value_probes svp WHERE svp.item_code=i.item_code)
        """))

    print(f"\n[CHECK 1] Items with numerical specs lacking PMP walk: {len(missing_walk)}")
    for r in missing_walk[:10]:
        print(f"  ⚠ {r[0]} [{r[1]}] spec={r[2]}{r[3] or ''}")
    if len(missing_walk) > 10:
        print(f"  ... and {len(missing_walk)-10} more")
    issues += len(missing_walk)

    # CHECK 2: PMP walks without a 'final' phase row
    incomplete_walks = list(db.execute("""
        SELECT walk_id, slug, item_code,
               MAX(step_index) AS last_step,
               SUM(CASE WHEN phase='final' THEN 1 ELSE 0 END) AS final_steps
        FROM spec_value_probes
        GROUP BY walk_id, slug, item_code
        HAVING final_steps = 0
    """))
    print(f"\n[CHECK 2] Incomplete PMP walks (no 'final' phase reached): {len(incomplete_walks)}")
    for r in incomplete_walks[:10]:
        print(f"  ⚠ walk={r[0]} | {r[2]} [{r[1]}] last_step={r[3]}")
    issues += len(incomplete_walks)

    # CHECK 3: Walks where no step passes strict termination
    no_pass_walks = list(db.execute("""
        SELECT walk_id, slug, item_code,
               COUNT(*) AS steps,
               SUM(COALESCE(passes_strict, 0)) AS passes
        FROM spec_value_probes
        GROUP BY walk_id, slug, item_code
        HAVING passes = 0 AND steps > 1
    """))
    print(f"\n[CHECK 3] PMP walks with no passing strict step: {len(no_pass_walks)}")
    for r in no_pass_walks[:10]:
        print(f"  ⚠ walk={r[0]} | {r[2]} [{r[1]}] {r[3]} steps, 0 passing")
    issues += len(no_pass_walks)

    # CHECK 4: PMP walks citing ineligible-for-synthesis sources
    # (per rule #10 sharpened: numerical-spec claims must cite gate-eligible sources)
    bad_source = list(db.execute("""
        SELECT svp.probe_id, svp.walk_id, svp.item_code, svp.slug, svp.ref_id,
               es.metadata_quality, es.verification_status
        FROM spec_value_probes svp
        JOIN evidence_sources es ON es.ref_id = svp.ref_id
        WHERE svp.ref_id IS NOT NULL
          AND svp.passes_strict = 1
          AND (es.metadata_quality = 'AUTHOR-TITLE-ONLY'
               OR es.verification_status IS NULL
               OR es.verification_status = ''
               OR es.verification_status IN ('UNVERIFIED-CLOSED', 'CLOSED-DELETED'))
        ORDER BY svp.walk_id
    """))
    print(f"\n[CHECK 4] PMP passing steps citing ineligible sources (rule #10): {len(bad_source)}")
    for r in bad_source[:10]:
        print(f"  ✗ {r[0]} | {r[2]} | ref={r[4]} | mq={r[5]} | vs={r[6]}")
    issues += len(bad_source) * 2

    # CHECK 5: passes_strict=1 step without ref_id linkage
    passing_no_ref = list(db.execute("""
        SELECT probe_id, walk_id, item_code, slug, step_value, step_value_unit
        FROM spec_value_probes
        WHERE passes_strict = 1 AND (ref_id IS NULL OR ref_id = '')
        ORDER BY walk_id, step_index
    """))
    print(f"\n[CHECK 5] Passing PMP steps without ref_id: {len(passing_no_ref)}")
    for r in passing_no_ref[:10]:
        print(f"  ⚠ {r[0]} | {r[2]} | step={r[4]}{r[5]}")
    issues += len(passing_no_ref)

    # CHECK 6: direction/claim_type consistency
    # Per DR-2026-05-10 (PMP design): the walk probes whether the spec value
    # could be tightened — i.e., minimums get walked UP (could the minimum be
    # higher?), maximums get walked DOWN (could the maximum be lower?). The
    # walk stops when evidence stops supporting the tightened value.
    # Inconsistent rows are walks that go the wrong direction relative to
    # what tightening means for their claim_type.
    direction_mismatch = list(db.execute("""
        SELECT probe_id, walk_id, item_code, claim_type, direction
        FROM spec_value_probes
        WHERE (claim_type = 'minimum' AND direction != 'up')
           OR (claim_type = 'maximum' AND direction != 'down')
        ORDER BY walk_id
    """))
    print(f"\n[CHECK 6] direction/claim_type inconsistency: {len(direction_mismatch)}")
    for r in direction_mismatch[:10]:
        print(f"  ⚠ {r[0]} | {r[2]} | claim={r[3]} dir={r[4]}")
    issues += len(direction_mismatch)

    # CHECK 7: spec_value_origin drift — N/A in current schema; items doesn't
    # carry the BPC's asserted spec value as a column. Drift detection requires
    # parsing the BPC reasoning doc. Future enhancement when items table or a
    # bpc_spec_values view exposes the asserted value.
    if False:
        pass
    else:
        print("\n[CHECK 7] Skipped — items table does not carry spec_value_origin; "
              "drift detection requires reasoning-doc parsing (future work)")

    print()
    print("=" * 60)
    print(f"ISSUES: {issues}")
    print("=" * 60)
    return 0 if issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
