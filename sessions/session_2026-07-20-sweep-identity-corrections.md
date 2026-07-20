# Session — anchor-correctness sweep corrections, batch 2 (2026-07-20)

Branch: `claude/evidence-base-state-slug-lz8up0` (restarted from `main` after PR #33 merged)

## Ask

Owner: "Please proceed with next steps in a careful but comprehensive manner." Apply the held
anchor-correctness-sweep corrections now that the weighted-strength tier model is enshrined (DR-2026-07-20).

## Applied (two migrations)

**Identity corrections (`data_20260720155301`) — 54 rows.** Adversarially-verified author_display / pub_title
/ journal_name fixes from the anchor sweep (`audits/anchor-correctness-sweep-2026-07-20.md`). Only clean,
non-prose values applied; 7 prose author entries (REF-00054, -00063, -00076, -00148, -00223, -00246, and the
hedged title REF-00523) held for hand-transcription.

**Tier/type reclassifications (`data_20260720155454`) — 59 rows.** Applied under the enshrined weighted-
strength model (DR-2026-07-20 / tier-system.md §8–§10). Only fully-determined, internally-consistent
(tier, evidence_type) pairs applied. Overwhelmingly **downgrades of mislabeled anchors**:
- academic studies mislabeled as Co-1 lived-experience → T3 clinical (REF-00009, -00036);
- individual-authored papers mislabeled as named-org standards (`standard_eb`) → T3 grey (many);
- high-control T1 rows that are lower-control primary → T3 clinical (many);
- a few adversarially-upheld elevations to T2 sr_meta where the row is genuinely a systematic review
  (REF-00356, -00518, -00601, -00787); statutory codes mislabeled standard_eb → T6 code (REF-00119, -00347).

Tier profile shift (T1 down, T3 up) reflects false anchors moving to their true tiers.

## Held for the next careful pass (41 tier/type + 7 identity)

Ambiguous cases the deterministic pass could not resolve safely: clinical rows where high-vs-low control
tier is undetermined; practice-stream candidates (REF-00062/-00063); scoping-vs-systematic review species
(REF-00700/-00710/-00804 etc., per GAP-298); Co-1 elevations needing confirmation (REF-00223/-00231/-00234);
and the 7 DISPUTED rows (untouched). These need a finalization workflow or hand review.

## Integrity

`PRAGMA foreign_key_check` / `integrity_check` clean after each migration; migration-reproducibility (7-invariant
rebuild) clean; audit regenerated.

## Remaining backlog

- 41 held tier/type + 7 held identity + 71 model-dependent defects → finalization pass.
- **Audit rework** (`tools/evidentiary_audit.py`): strength-band + weak-only flag; exclude DISPUTED; encode
  practice-stream. Now the highest-leverage remaining item — makes the enshrined model visible in the audit.
- English grey subset (~24 rows); extend the correctness sweep to the full 779.
