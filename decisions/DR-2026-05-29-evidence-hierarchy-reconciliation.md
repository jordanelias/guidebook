# DR-2026-05-29 — Evidence-Hierarchy Reconciliation (sr_meta@T2, tier=anchor-type, T1 composition, de-OT correction)

**Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECORD-2026-07-13.md** *(was: PROPOSED — completes the uncommitted draft begun in `session_2026-05-29`; pending owner commit alongside the Stage 1.1 doctrine bundle.)*
**Authored:** 2026-05-29 (draft); completed 2026-06-09 (`session_2026-06-09` — required reads done: `evidence-methodology.md` §§2–5, `conceptual-model.md`).
**Doctrine SHA at authorship:** `61c7f95`. **Doctrine SHA this DR ratifies into being:** `3da73bd` (revised `governance/mission-and-epistemics.md`).
**Gate:** decisions D-A (α), D-D, D-E (β) — all RULED in `MASTER-WORKPLAN-consolidated-2026-06-05` §1.
**Relates to:** R1 (three-way fork), R9 (hierarchy reconciliation incomplete), tier-system.md (OPERATIVE 2026-05-25), GAP-273/296 (closed by the sr_meta→T2 owner directive).

---

## Context

The evidence hierarchy was, until 2026-05-25, in an unratified three-way fork: `governance/mission-and-epistemics.md` and `governance/evidence-methodology.md` placed systematic reviews at **Tier 3**; `governance/tier-system.md` and the database placed them at **Tier 2**. The owner directive of 2026-05-25 ("t2>t3 this is enshrined") and the migration `data_20260525070000_sr_meta_t2_canonicalization.sql` moved the data and authored `tier-system.md`, but the mission/methodology prose was never reconciled. A reconciliation DR drafted 2026-05-29 was left uncommitted with required reads outstanding. This DR completes it; Stage 1.1 executes the prose edits.

## Decisions recorded

1. **sr_meta sits at Tier 2.** Systematic reviews / meta-analyses are community-consensus synthesis above primary studies and below international standards, alongside named-organisation evidence-based standards. This ratifies `tier-system.md` §2 (PI v10.14 rule #9 reading; evidence-type homology; SR-as-warrant-over-input citation behaviour; GRADE synthesis-above-primary). The unqualified-GRADE wording in the legacy `references/methodology-evidence-hierarchy-mapping.md` — which argues SRs *invert downward* to Tier 3 — is **superseded** (see Stage 1.1 caller-sweep; that file requires its own reconciliation pass).

2. **Tier 3 = lower-control primary clinical + grey-literature primary research.** Cross-sectional, observational, qualitative, single-centre clinical studies and primary grey literature. Supporting evidence, rarely the sole basis. This is the vacated-by-sr_meta Tier 3 redefinition.

3. **Tier is derivable from anchor-type (`evidence_type` × `scope`), not hand-set.** Tier reflects *what kind of claim a source can anchor*, not source quality (`tier-system.md` §1). The hand-set `tier` column is to be replaced by a derivation map at Stage 2.1; this DR records the principle, Stage 2.1 builds the map, Stage 2.5 sweeps for residual `(evidence_type, scope) → tier` inconsistencies (≈19 rows measured 2026-06-09: 7 `standard_eb`@T3, 3 `standard_eb`@T5, 2 `clinical`@T4, 1 `co1`@T5, 3 `grey`@T1, 1 `grey`@T2).

4. **Tier 1 composition — D-E = β (OT-prioritized, not OT-exclusive).** OT leads Tier 1 by claim-type fit, but directly-relevant high-control non-OT primary research (biomechanical / sensory studies on gradients, clearances, acoustic / luminance thresholds) is admitted at Tier 1, not demoted to Tier 3 — paired with the single-study-corroboration expectation (PI rule #8 PMP). A built-environment guidebook is dominated by physical parameters; β keeps OT primacy without demoting the on-point mechanism evidence that is often the best evidence for a specific parameter.

5. **De-OT correction.** The mission/methodology phrasing "OT intervention-tested clinical research" for Tier 1 is corrected to "primary research with intervention-level or biomechanical control … OT-prioritized but not OT-exclusive," matching `tier-system.md` §1 (which was already de-OT'd) and D-E. Tier 1 is defined by *control level on the parameter*, with OT prioritized by claim-type fit — not by author discipline alone.

## Execution (Stage 1.1)

Prose edits to `mission-and-epistemics.md` (hierarchy table; commitment §2; new "Two orthogonal axes of coverage" subsection), `evidence-methodology.md` (§1.1 table; §1.4 amended to scale-conditioned weighting; new §§1.6 mode-asymmetry, 1.7 directness; §1.5 retitled to the named-org-standards stream; §5.2 and §6.4 fork references), `tier-system.md` §5 (T3-clinical placed on the ● marker line), and the canonical governance callers `co1-operational.md` and `adversarial-use-framework.md`. Diff: `1.1-doctrine.diff`. New doctrine SHA: `3da73bd`.

## Consequences flagged (not resolved here)

- **State-machine `stated` threshold vs the new Tier 3.** `evidence-methodology.md` §2.2 / §2.7 treat "Tier 3 alone" as sufficient for `stated`. Under the redefined Tier 3 ("rarely the sole basis"), Tier-3-alone arguably warrants `provisional`, not `stated`. This is a threshold change with validator consequences (`validate_evidence_state.py`); **decision required**, deliberately not made in 1.1.
- `references/methodology-evidence-hierarchy-mapping.md` ("governs all BPC entries") still encodes the fork and argues for it; HIGH-priority caller reconciliation.
- BPC/SR prose "Tier 3 systematic review" labels across `references/bpc/**` and `references/systematic-reviews/**` are DB-superseded narrative (DB already has sr_meta@T2); they are swept during the Stage 2.x ~176-item remapping / Phase E rewrite.
