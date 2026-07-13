# DR-2026-07-12: Tier-3-alone `stated` threshold — proposed resolution

- Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECORD-2026-07-13.md** *(was: **PROPOSED — pending owner ratification**)*
- Date: 2026-07-12
- Prepared by: Claude, at the owner's request to reconcile identified conflicts and propose a path forward. **Not owner-ratified.** This is the specific threshold question `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md` explicitly flagged and declined to resolve — resolving it now is a genuine evidence-methodology judgment call for the owner to review, not a fact Claude can establish unilaterally.
- Affects (if ratified): `governance/evidence-methodology.md` §2.2/§2.7, `scripts/validate_evidence_state.py`
- Related: `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md`, `governance/tier-system.md` §1/§5, `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`

## Context

`decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md` redefined Tier 3 as "rarely the sole basis" for best-practice claims (now codified in `governance/tier-system.md` line 19: *"Supporting evidence for best-practice claims; rarely the sole basis"*), while flagging, explicitly unresolved:

> **State-machine `stated` threshold vs the new Tier 3.** `evidence-methodology.md` §2.2 / §2.7 treat "Tier 3 alone" as sufficient for `stated`. Under the redefined Tier 3 ("rarely the sole basis"), Tier-3-alone arguably warrants `provisional`, not `stated`. This is a threshold change with validator consequences (`validate_evidence_state.py`); **decision required**, deliberately not made in 1.1.

`tier-system.md` §5 additionally splits Tier 3 into two species with different confidence markers: **T3-clinical** (lower-control primary clinical research — confirmed primary evidence, marked `●`, alongside T1/T2/Co-1/Co-2) and **T3-grey** (grey-literature primary research — unconfirmed/thin, marked `○`, alongside `[EXPERT CONSENSUS]`/`[THIN BASE]`/T6). The unresolved threshold question does not distinguish between these two species, and should.

## Proposed decision

**Tier-3-alone, of either species, does not satisfy the `stated` threshold.** Specifically:

1. A cell whose only governing evidence is **T3-clinical** (with no Co-1/Co-2/T1/T2 corroboration) is `provisional`, not `stated` — consistent with `tier-system.md`'s "rarely the sole basis" characterization and with the general principle (already established for Tier 6 in `best-practices-assessment-system.md` §3's hard rule) that a determination's confidence should reflect the actual strength of its anchoring evidence, not just whether *some* evidence exists.
2. A cell whose only governing evidence is **T3-grey** does not satisfy even `provisional` on its own — it is `pending` (or explicitly `[THIN BASE]`-flagged per existing convention) unless corroborated, consistent with its `○` (unconfirmed) marker.
3. **Convergence remains the path to `stated`**: if T3-clinical evidence *converges* with Co-1, Co-2, T1, or T2 evidence (i.e., `convergence_assessment.status = 'convergent'` with ≥2 evidence axes, one of which may be T3-clinical), the cell can be `stated` — this is unchanged and is exactly what the existing `convergent` status already requires (≥2 axes). Only the *single-axis, T3-alone* case is being downgraded.
4. This is a **narrowing** of `stated`, not a loosening of anything else: no cell that was correctly `stated` under a stronger evidence basis (T1, T2, Co-1, Co-2, or genuine convergence) is affected.

## Consequences if ratified

- `governance/evidence-methodology.md` §2.2/§2.7 would need updating to state the above explicitly (not done by this DR — text edit is a small follow-up once ratified).
- `scripts/validate_evidence_state.py`'s `validate_cell_states_db()` would need a new check: for `state == 'stated'` cells, when `convergence_assessment.status == 'single_axis'`, verify the single axis is not T3-alone (i.e., not all of `clinical_sources` resolve to `evidence_sources.tier == 3`). **This DR is accompanied by that validator addition**, implemented now so the check exists and can be reviewed alongside the policy, rather than left as an unscoped follow-up (the schema-reconciliation DR's companion review flagged exactly this kind of unscoped-follow-up gap as a real problem — this DR does not repeat it).
- `references/methodology-evidence-hierarchy-mapping.md` — already flagged by DR-2026-05-29 as still arguing for the old (superseded) tier ordering — remains a separate, HIGH-priority caller-reconciliation item, not resolved here.
- No cells exist yet (`evidence_cell_state` has 0 rows as of this DR), so there is no backfill or re-classification of existing data required — this purely sets the rule going forward for the Phase E synthesis work that will populate the table.

## What would make this ACCEPTED

Owner review of the specific threshold call in "Proposed decision" item 1 (T3-clinical-alone → `provisional`, not `stated`) — this is the one substantive judgment call in this DR — followed by an explicit ratification note or session directive. Items 2–4 are largely consequences of `tier-system.md`'s already-ratified `●`/`○` split and the existing convergence-count rule, not new judgment calls.
