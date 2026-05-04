# A6 Handoff — Evidence Methodology
**Issued:** 2026-04-29 16:22 UTC
**Phase predecessor:** A5 Co-1 operational specification — COMPLETE 2026-04-29 15:50
**Phase target:** A6 — Evidence methodology
**Doctrinal basis:** T-03 (`governance/pre-stage-a-decisions.md`) · T-04 (same) · `governance/co1-operational.md` (just committed) · `governance/mission-and-epistemics.md` §Epistemic commitments · voice-style §§8.1, 8.2, 8.3
**Sessions estimated:** 3–5 (per workplan v3 §A6, unaffected by Amendment 7)
**Pattern:** Governance + Code (returns to CO-0008 governance+code co-production methodology after two prose-only phases A4/A5)

---

## 1. What A6 produces

**Primary deliverables:**

1. **`governance/evidence-methodology.md`** — definitive specification of the seven-tier evidence hierarchy in operational form, the evidence-state machine per T-04, the values-criteria assessment mechanism (resolves N-02), the design-pedagogy literature engagement (resolves N-08), and the `epistemic-defense` skill specification (resolves D-04 partial).

2. **`schemas/evidence_state.py`** — Pydantic schema for the evidence-state machine per T-04; encodes the four states (`stated`, `provisional`, `pending`, `not_applicable`) and integrates with EvidenceSource schema per A5 §7.1 (six fields: `tier`, `evidence_type`, `co1_provenance`, `co1_source_type`, `verification_status`, `synthesis_attribution_required`).

3. **`scripts/validate_evidence_state.py`** — CI validator enforcing T-04 state machine rules: `pending` cells must reference `gap_register.md`; `provisional` cells must specify confidence flag and rich-dimension citation; `not_applicable` cells must carry rationale; `stated` cells must cite ≥Tier 3 OR Co-1 OR Co-2 evidence.

4. **`scripts/convert/convert_sources.py`** — sample conversion script that takes existing BPC/source data and produces validated EvidenceSource records per the schema.

5. **Multilingual-research output validator (hybrid)** — wrapper validator for outputs of the multilingual-research skill that confirms Co-1 evidence emerging from non-English literature reviews carries proper provenance and verification status.

**Secondary deliverables:**

- **Voice-style §8.4 (or co-located in §8.1) — `epistemic-defense` voice patterns.** How prose handles questions about evidence basis from skeptical readers. Resolves D-04 partial.
- **`governance/values-criteria.md`** — operational specification of the values-criteria assessment mechanism that allows Co-1 evidence to be weighed against competing population values where conflict exists (e.g., visitability framework's zero-step vs. some PAIN-population preferences for textured threshold landings). Resolves N-02.

---

## 2. Why A6 cannot be deferred

A6 is the **central binding gate** of Stage A (per workplan-orchestrator roadmap §9). Three downstream phases depend on its outputs:

1. **A7 (Population taxonomy)** — sub-population schema needs `evidence_type`-aware validation; A6 specifies the schema layer.
2. **A8 (Jurisdiction philosophy)** — jurisdictional comparison voice depends on A6 evidence-state machine + Co-1 voice patterns from A5.
3. **A9 (Time model unification)** — version metadata for governance docs and skill outputs depends on A6 specifying the `effective_from` / `superseded_by` fields on EvidenceSource.

And **B1 (storage form decision)** depends on A6 fully operational. The schema design in B1 starts with the EvidenceSource entity as the largest and most constraint-laden; A5 specified the Co-1 fields, and A6 specifies the state machine and validation logic.

**And C7 (evidence migration in Stage C)** depends on A6 fully operational. C7 is the migration of 584 sources + 81 unverified residual disposition (per workplan-orchestrator roadmap §6) — bound directly to A6 schema.

---

## 3. Doctrinal anchors carried forward

| Decision | Source | Status entering A6 |
|---|---|---|
| **T-03** | `pre-stage-a-decisions.md` | DECIDED. Co-1 tier encoding: `tier` + `evidence_type` taxonomy. EvidenceSource carries both. |
| **T-04** | same | DECIDED. Four-state machine: `stated` / `provisional` / `pending` / `not_applicable`. |
| **A5 Co-1 specification** | `governance/co1-operational.md` | CANONICAL. Six required fields. CS2/CS5 trigger spec. Four voice patterns. |
| **Co-primary status** | mission §3 | LOCKED. Co-1 co-primary with Tier 1; not subordinate. |
| **Seven-tier hierarchy** | mission §Epistemic commitments | LOCKED. |
| **Tier-appropriate voice** | voice-style §§8.1, 8.2, 8.3 | OPERATIVE. |
| **Pre-launch solo authorship** | D-03 revised | LOCKED. Affects validation rigor declaration in A6 governance text. |

---

## 4. Open questions A6 must resolve

### Q1 — Evidence-state machine validation logic
What constitutes "rich evidence in at least one dimension" for `provisional` state? The T-04 specification names the state but doesn't define the threshold. Concrete rules needed: minimum number of Co-1 sources for Co-1-only `provisional`? Tier 3 SR alone sufficient? PROVISIONAL-marked Tier 1 OT clinical alone?

### Q2 — Cross-tier convergence rules
When Tier 1 OT and Co-1 sources agree on a parameter value, the converged value carries higher confidence than either alone (per mission §3). How is this encoded in the schema? `confidence_score` field? Boolean `cross_tier_convergence`? Free-text justification with validator pattern-matching?

### Q3 — Tier 1 OT conflict with Co-1 (T-04 `stated` ambiguity)
A cell with strong Tier 1 OT clinical evidence AND strong Co-1 evidence that diverge — both are "rich" — is currently classified `stated` per T-04 (each is rich). But the divergence is itself an epistemic state needing handling beyond simple `stated`. A6 must specify whether divergence cells get a fifth state (`stated_divergent`?) or carry a divergence flag within `stated`.

### Q4 — Co-2 evidence handling
Co-2 (OT professional body CPGs, evidence_type: `co2`) is parallel to Tier 2 NGO/advocacy guidelines but encodes professional consensus. A6 must specify the validator's treatment of Co-2 evidence in the state machine: does Co-2 alone count as "rich" for `provisional` purposes? Does Co-2 + Co-1 convergence carry the same confidence as Tier 1 + Co-1?

### Q5 — Values-criteria assessment (resolves N-02)
The values-criteria mechanism: where two populations have evidence-supported preferences that conflict (e.g., visitability framework's zero-step at residential entrances vs. some PAIN-population evidence supporting textured threshold landings), how is the conflict resolved at synthesis time? Mode S OT co-design resolves at the individual scale; what governs at Tier 1 (population-informed)? A6 specifies the mechanism. Per mission §3, "where they diverge, the divergence is documented and a synthesis approach is specified per parameter" — A6 operationalizes "synthesis approach."

### Q6 — Design-pedagogy literature engagement (resolves N-08)
The mission-and-epistemics §Epistemic commitments §Questions-led teaching as testable hypothesis cites Schön 1983, Hmelo-Silver 2004, Royeen 1995. A6 specifies how these cites operate in the evidence base: are they Tier 5 (national framework analog)? Tier 3 (SR analog)? A new tier? The pedagogy claim is foundational to the guidebook; its evidence basis needs proper tier-located treatment.

### Q7 — `epistemic-defense` skill specification (resolves D-04 partial)
The skill specifies how to handle prose objections to the guidebook's evidence claims (e.g., "where's the RCT for that threshold value?"). Voice patterns + decision rules for when to: cite the evidence chain; acknowledge gap; route to T-04 `pending`; route to A11 legal disclaimer. A6 produces this skill.

### Q8 — Validation thresholds for Co-1 source verification status
Per A5 §6.3, validators block migration of cells whose only Co-1 source is `UNVERIFIED-CLOSED` or `CLOSED-DELETED`. But what about `UNVERIFIED-1` (one search, not yet retried)? Cell state: defer migration, flag, or block? A6 specifies.

---

## 5. Methodology recommendation

A6 is the largest Stage A phase outside A3 (already complete). 3–5 sessions structured as:

**Session 1 — Doctrinal scaffolding (governance only).** Produce `governance/evidence-methodology.md` sections 1–3: definition of evidence states; integration with T-03 + T-04 + A5 Co-1 specification; resolution of Q1, Q2, Q3, Q4 (the evidence-state machine refinements).

**Session 2 — Schema + validator implementation (governance+code).** `schemas/evidence_state.py`; `scripts/validate_evidence_state.py`; `scripts/convert/convert_sources.py`. Test against existing corpus (sample of BPC files; `references/co1-verified-sources.json`). Resolve Q8 (verification status thresholds) in implementation.

**Session 3 — Values-criteria + design-pedagogy + epistemic-defense (governance + skill).** `governance/values-criteria.md`; voice-style §8.4 if needed; specification for `epistemic-defense` skill (deferred to C2 actual build). Resolves Q5, Q6, Q7.

**Possible Session 4 — Multilingual-research output validator (code).** If multilingual-research outputs need a wrapper validator for Co-1 provenance + verification status integration, produce that here. May fold into Session 2.

**Possible Session 5 — Integration testing + governance recheck.** Run all validators against existing corpus end-to-end. Adjust thresholds, fix edge cases. Lock A6 deliverables.

**Compress to 3 sessions** if Sessions 4 and 5 fold into earlier sessions. Expand to 5 sessions if integration surfaces unexpected gaps.

---

## 6. Doctrinal risk: what A6 must NOT do

- **MUST NOT** revise T-03 or T-04. They are locked. A6 operationalizes them; it doesn't change them.
- **MUST NOT** weaken Co-1 co-primary status. The state machine treats Co-1 sources at parity with Tier 1 OT clinical for `stated` purposes (per A5 §1).
- **MUST NOT** introduce evidence types that bypass the seven-tier hierarchy. New evidence categorizations route through hierarchy revision (future Stage A phase or post-launch governance), not through A6.
- **MUST NOT** scope-creep into B1 schema design. A6 specifies the EvidenceSource fields and state-machine logic; B1 implements the storage form and integrates with all entities.
- **MUST NOT** scope-creep into C2 skill build. A6 specifies the `epistemic-defense` skill's *requirements*; C2 builds the skill with its file system mechanism.
- **MUST NOT** absorb GAP-079 (GRADE ratings deferred to C9) or GAP-CITE-01 (citation tagging deferred to C7). Those are Stage C migrations bound to A6 outputs, not A6 work.

---

## 7. Reading list for A6 Session 1

Mandatory reads:

1. `governance/co1-operational.md` (just committed; full read)
2. `governance/pre-stage-a-decisions.md` T-03 + T-04 sections
3. `governance/mission-and-epistemics.md` §Epistemic commitments (full read)
4. `references/project-standards.md` Core Doctrine + Stage 0.5 decisions + 2026-04-29 A4/A5 close rules
5. `skills/voice-style_SKILL.md` §§8.1, 8.2, 8.3 (full read of those sections)
6. `references/co1-verified-sources.json` (sample structure; ground for schema design)
7. `references/bpc/_template.md` (current BPC structure that the converter must accept as input)

Reference reads:

8. `references/bpc/DEAF.md` or `references/bpc/MOB.md` (one full BPC file as concrete example of current corpus state)
9. `references/co1-verification-report-2026-04-23.md`
10. `gap_register.md` GAP-079 + GAP-CITE-01 entries (so the validator can flag-but-not-block items already routed to Stage C)

External research reads (only if Q5 values-criteria or Q6 design-pedagogy require depth):
- Schön 1983 (reflective practitioner); Hmelo-Silver 2004 (problem-based learning); Royeen 1995 (clinical reasoning) — for design-pedagogy tier classification
- Sen capability approach + Nussbaum capabilities literature — for values-criteria mechanism design

---

## 8. Cross-stage continuity threads

A6 affects:

| Thread | Effect at A6 |
|---|---|
| **CS2** Co-1 recruitment | Stays INOPERATIVE pre-launch (per A5). A6 does not change this. |
| **CS5** Co-1 representation monitoring | A6 specifies the validator that supports CS5 corpus-representation monitoring (population/domain/jurisdiction inventories). |
| **CS3** Versioning continuity | A6 specifies version metadata fields on EvidenceSource (`effective_from`, `superseded_by`). CS3 doesn't go LIVE until A9 spec → C1 LIVE, but field specification belongs in A6. |
| **CS6** Standards monitoring | Activates at B7. A6 supplies the EvidenceSource version-tracking that CS6 will use. |
| **CS8** Decision capture | A6 produces 8 substantive resolutions (Q1–Q8). Captured per A12-pending protocol. |
| **CS9** Adversarial-use review | A6 produces the `epistemic-defense` skill specification; CS9 activates at A10 with this as binding input. |

---

## 9. Stage A budget impact

Original v3 budget for A6: 3–5 sessions. Unaffected by Amendment 7.

Stage A entering A6: ~17–18 sessions consumed (Stage 0 ~9 + A1-A2 ~3 + A3 ~7 + A4 ~3 + A5 ~2 = ~24; offset by some overlap and the Amendment 7 A5 reduction).

A6 (3–5) + A7 (2–3) + A8 (2–3) + A9 (2–3) + A10 (1–2) + A11 (1–2) + A12 (1) + A13 (1) = ~13–20 more sessions to Stage A complete.

**Stage A done estimated total: ~37–44 sessions**, with budget upper bound at 32 (post-Amendment 7). This is over budget by ~5–12 sessions. Re-budget at A6 close per Amendment 7 deferral specification (re-budget when working rhythm establishes — that point is approaching).

---

## 10. Entry condition for A6 Session 1

Before starting A6 Session 1:

1. ✓ Confirm A5 closure (this handoff confirms it)
2. ✓ Apply PI updates from `workplan/pi-update-co0008.md` if not yet applied
3. Decide whether A6 starts in current conversation or fresh context — A6 is governance + code; the code work benefits from fresh context for Pydantic schema and validator implementation. Recommendation: **fresh context for A6 Session 1**.

A6 Session 1 will load this handoff + 7 mandatory reads. Estimated context load: ~100–150k tokens of input before drafting begins. Comfortable in 1M window.

---

**End of A6 handoff.**
