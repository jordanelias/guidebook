# Evidence Methodology
**Status:** CANONICAL — A6 complete (Sessions 1–3)
**Phase:** Stage A Phase 6 — Evidence methodology
**Created:** 2026-04-29 17:35 UTC · **S2:** 2026-04-29 18:05 · **Closed:** 2026-04-29 19:06
**Doctrinal basis:** T-03 (`governance/pre-stage-a-decisions.md`) · T-04 (same) · `governance/co1-operational.md` (A5 CANONICAL) · `governance/mission-and-epistemics.md` §Epistemic commitments · voice-style §§8.1, 8.2, 8.3
**Pattern:** Governance + Code (governance this session; code Session 2)

---

## 1. Evidence hierarchy — operational definition

### 1.1 The seven-tier hierarchy

The guidebook draws on seven tiers of evidence, with two co-primary parallel tiers (Co-1, Co-2). The full hierarchy is defined in `governance/mission-and-epistemics.md` §Epistemic commitments §Evidence hierarchy and reproduced in `references/project-standards.md` Core Doctrine. This section operationalizes it — specifying how each tier is encoded, validated, and used in best-practice synthesis.

| Position | Tier value | Evidence type | Source examples |
|---|---|---|---|
| Tier 1 | `tier: 1` | `evidence_type: clinical` | Primary research with intervention-level or biomechanical control on the parameter — OT-prioritized but not OT-exclusive (per D-E): OT intervention trials, RCTs, **and** directly-relevant high-control non-OT primary research (biomechanical / sensory studies on gradients, clearances, acoustic / luminance thresholds) |
| Co-1 | `tier: 1` | `evidence_type: co1` | Lived experience / participatory design (CRPD Art. 4.3); DPO research; peer-reviewed lived-experience literature; named advocacy organizational positions; Co-1-authored academic narratives |
| Tier 2 | `tier: 2` | `evidence_type: sr_meta` or `standard_eb` | Community-consensus synthesis above primary studies, below international standards. Two streams: (a) systematic reviews / meta-analyses (`sr_meta`); (b) named-organisation evidence-based standards — DPO guidelines, professional-body standards (`standard_eb`) |
| Co-2 | `tier: 2` | `evidence_type: co2` | OT professional body CPGs (CAOT, AOTA, RCOT, COTEC, WFOT) |
| Tier 3 | `tier: 3` | `evidence_type: clinical` (lower-control) or `grey` | Lower-control primary clinical research (cross-sectional, observational, qualitative, single-centre) and grey-literature primary research — supporting evidence, rarely the sole basis |
| Tier 4 | `tier: 4` | `evidence_type: standard_eb` | International standards with evidence basis (ISO 21542, ISO 23599, IEC 60118-4, EN 17210) |
| Tier 5 | `tier: 5` | `evidence_type: national_fw` | National beyond-code frameworks (BS 8300-2 Annex G, NL WMO-keuken, RCOTSS-Housing OT) |
| Tier 6 | `tier: 6` | `evidence_type: code` | Statutory codes (reference baseline only) |

Additional `evidence_type` values: `grey` (grey literature, organizational reports not classifiable above); `unknown` (not yet classified). Both are transitional states — every source should eventually resolve to a classified type.

### 1.2 Encoding per T-03

Per Stage 0.5 Decision T-03 (DECIDED, locked): the evidence hierarchy is encoded as two orthogonal dimensions on every `EvidenceSource` record:

1. **`tier`** (integer, 1–6): the clinical-evidence position. Higher numbers = weaker evidence. Co-1 records carry `tier: 1` (co-primary); Co-2 records carry `tier: 2` (parallel to Tier 2).
2. **`evidence_type`** (enum): the kind of evidence. Values: `clinical`, `co1`, `co2`, `sr_meta`, `standard_eb`, `national_fw`, `code`, `grey`, `unknown`.

The two-field encoding preserves the doctrinal relationship: Co-1 is *co-primary with* Tier 1, not *identical to* Tier 1. A query for "all Tier 1 evidence" returns both clinical and Co-1 records; a query for "all Co-1 evidence" returns only Co-1 records. Neither subsumes the other.

### 1.3 Co-1 and Co-2 operational requirements

Per A5 (`governance/co1-operational.md`, CANONICAL), every Co-1 citation carries six required schema fields:

| Field | Type | Required values |
|---|---|---|
| `tier` | int | `1` |
| `evidence_type` | enum | `co1` |
| `co1_provenance` | enum | `published_corpus` (pre-launch all) or `participatory_synthesis` (post-launch contingent) |
| `co1_source_type` | enum | `peer_reviewed_literature`, `dpo_research`, `advocacy_position`, `academic_narrative`, `validated_tool` |
| `verification_status` | enum | `VERIFIED`, `VERIFIED-WITH-CORRECTION`, `UNVERIFIED-1`, `UNVERIFIED-CLOSED`, `CLOSED-DELETED` |
| `synthesis_attribution_required` | bool | `true` if the guidebook substantially synthesizes from this source (A5 §3.4 Tier 2 obligation) |

Co-2 records carry `tier: 2, evidence_type: co2`. They do not require the Co-1-specific fields (`co1_provenance`, `co1_source_type`, `synthesis_attribution_required`). Co-2 records do require `verification_status`.

### 1.4 Relationship to the Design Modes — orthogonality of coverage, scale-conditioned weighting

The Seven-Tier Evidence Hierarchy and the Design Modes are orthogonal **axes of coverage** (amending A5 §3.5 per decision D-D): both are always consulted, and neither determines the other. They co-locate authority for any specification:

- **Design Hierarchy** locates the *kind of design decision* and its *scale*: Universal Mode (universal, code-compliant); Population scale (population-informed, ranges with median); Person scale (person-specific, OT-resolved).
- **Evidence Hierarchy** locates *what evidence supports the value*: what tier, what type, how strong.

Every cell in the specification matrix sits at an intersection of both axes. A population-informed specification may be supported by evidence at any Evidence Tier — clinical, Co-1, Co-2, standards, or a combination. The evidence tier does not determine the design scale; the design scale does not constrain which evidence tiers are consulted.

**What D-D amends.** The axes are not merely orthogonal; they are orthogonal *under scale-conditioned weighting*. Orthogonality of coverage is retained — both axes always apply — but which evidence carries the most weight is conditioned by the design scale (§1.6) and by directness grain-matching (§1.7). Orthogonality is refined, not abandoned: the independence of the axes stands; the flat reading under which any tier weighs equally at any scale does not.

### 1.5 Tier 2 named-organisation evidence-based standards vs. Co-1

Tier 2 has two streams (§1.1): (a) systematic reviews / meta-analyses, and (b) named-organisation evidence-based standards (DPO guidelines, professional-body standards). This section concerns the second stream — the standards/guidelines published by named organisations — and how it is distinct from Co-1. The two share organizational provenance (both may come from DPOs) but differ in what they encode:

- **Tier 2 (named-organisation standards stream)** encodes organizational *guidelines / standards* — recommendations an organization publishes for how accessible design should be done. The organization's authority is institutional (its reputation, its constituency, its mandate).
- **Co-1** encodes lived-experience *evidence* — findings produced by, with, or under methodological authority of disabled people. The evidence's authority is methodological (peer review, organizational accountability, or scholarly authorship per A5 §1.2).

A DPO may produce both: a design guideline (Tier 2 standards stream) and a lived-experience research output (Co-1). The same organization, different epistemic products. Encoding matters because best-practice synthesis treats Co-1 as co-primary with Tier 1 — a stronger epistemic claim than Tier 2 organizational guidelines carry. (The SR / meta-analysis stream of Tier 2 is synthesis evidence, a separate case; it is not what this section contrasts with Co-1.)

The validator (Session 2) enforces this: a source classified as both `co1` and `standard_eb` (or `national_fw` or `code`) is an error. A source may have one `evidence_type`; its tier follows from that type. Tier 2 organizational guidelines carry `evidence_type: standard_eb` (if evidence-based) or `national_fw`, not `co1`.

### 1.6 Mode-asymmetry — where source-ranking does its work

The three design scales weight the evidence hierarchy asymmetrically (per decision D-D):

- **Universal Mode** is the code-floor (Tier 6) raised by population-level evidence wherever higher-tier evidence supports a value above the floor. Source-ranking enters only to justify exceeding the floor.
- **Population scale** is where source-ranking does its substantive work. The evidence hierarchy adjudicates the best-practice value and range here: Tier 1 / Co-1 / Tier 2 / Co-2 evidence anchors the claim; Tier 3 supports; Tier 4–6 do not anchor (convergence-not-evidence — §3 here and `governance/tier-system.md` §3).
- **Person scale** is OT process-resolution *within* the Population-scale range. The governing evidence is assessment and clinical-reasoning evidence — how to resolve an individual's position — not parameter-value-ranking. The hierarchy that ranks parameter values does not re-run at the Person scale; a different evidence question applies.

This asymmetry is why §1.4's orthogonality is scale-conditioned: the same evidence hierarchy is consulted at every scale, but its adjudicating force concentrates at the Population scale.

### 1.7 Directness as a conditioning layer — grain-matching, not specificity-ranking

Directness conditions the weight a source carries for a given claim, as a layer over the single population-anchored ladder (per decision D-D) — not as a separate hierarchy per scale. Per GRADE's directness principle, a source is weighted by how well its *grain* matches the *grain of the claim*, bidirectionally:

- An aggregate systematic review (Tier 2) is strongest for a population-level claim and is *down-weighted* for a person-specific functional claim, because its grain is the population, not the individual.
- A directly-relevant intervention or biomechanical study (Tier 1) is the reverse: strongest where the claim's grain matches the study's parameter and population, down-weighted where the claim generalizes beyond what the study measured.

The project **rejects a "most-specific-to-least-specific" gradient.** Specificity is not the axis; grain-match is. A more specific source is not automatically stronger — it is stronger only where the claim's grain matches its grain. The scattered directness primitives currently recorded across the schema (`match_grade`, `value_match`, `passes_strict`, relevance notes) are consolidated into one rule-based directness model at Stage 2.2; this section is the doctrinal basis that build implements.

---

## 2. Evidence-state machine

### 2.1 The four states (T-04 operationalized)

Per Stage 0.5 Decision T-04 (DECIDED, locked): each (parameter × population) cell in the guidebook's specification matrix holds one of four states. T-04 specifies the states; this section operationalizes the thresholds, transitions, and validator rules.

| State | Display | Meaning |
|---|---|---|
| `stated` | Normal rendering | Best-practice claim derived from sufficient evidence. The claim is defensible at the evidence tier cited. |
| `provisional` | Confidence flag rendered | Synthesis based on evidence that is rich enough to produce a qualified claim, but does not meet the `stated` threshold. |
| `pending` | `[BEST-PRACTICE-PENDING]` + gap-register link | Evidence too sparse across all dimensions to synthesize. The absence is visible and traced. |
| `not_applicable` | "Not applicable" + rationale | The parameter has no design implication for this population. Not a gap — a genuine non-intersection. |

### 2.2 The `stated` threshold

A cell reaches `stated` when it has **at least one anchoring source meeting any of the following conditions** (amended per DR-2026-07-12-tier3-stated-threshold and unification-DR item G7, both ACCEPTED 2026-07-13):

1. **Tier 1 clinical evidence** with direct parameter relevance — primary research with intervention-level or biomechanical control addressing the design parameter for the target population.
2. **Tier 2 synthesis evidence** with direct parameter relevance — either stream: a systematic review / meta-analysis (`sr_meta`), or a named-organisation evidence-based standard (`standard_eb` at Tier 2) addressing the parameter (G7: this stream anchored under §1.6 but was unreachable under this section's previous literal wording).
3. **Co-1 evidence** with direct parameter relevance — a Co-1 source (per §1.3 requirements, with `verification_status ∈ {VERIFIED, VERIFIED-WITH-CORRECTION}`) that addresses the design parameter for the target population.
4. **Co-2 evidence** with direct parameter guidance — an OT professional body CPG that addresses the design parameter.

The OR clause is deliberate: Co-1 alone is sufficient for `stated`, as is Co-2 alone, as is Tier 2 alone. **Tier 3 alone is not** (tier3-stated-threshold DR): T3-clinical-alone yields `provisional`; T3-grey-alone yields `pending`; Tier 3 contributes to `stated` only through convergence (≥2 evidence axes, one of which may be T3-clinical). This follows from the doctrinal commitments that Co-1 is co-primary with Tier 1 — a best-practice claim grounded solely in strong Co-1 evidence is a legitimate evidence-based claim, not a provisional one — and that Tier 3 is "rarely the sole basis" (`tier-system.md` §1).

**What `stated` does not mean:** `stated` does not mean the claim is beyond dispute. It means the evidence basis is sufficient to make a defensible best-practice claim at the tier cited. A `stated` cell may still be revised when new evidence emerges, when higher-tier evidence replaces lower-tier, or when cross-tier divergence is resolved through new research.

### 2.3 The `provisional` threshold — resolves Q1

**Q1 from A6 handoff:** *What constitutes "rich evidence in at least one dimension" for `provisional` state?*

**Resolution:** A cell is `provisional` when it has evidence that is **rich enough to synthesize** but does not meet the `stated` threshold — meaning it has no source at Tier 1–3, no Co-1 source, and no Co-2 source with direct parameter relevance.

Concretely, `provisional` applies in two cases (per the tier3-stated-threshold DR and unification-DR item G1b, ACCEPTED 2026-07-13): (a) **T3-clinical-alone** — lower-control primary clinical evidence with direct relevance but no anchoring corroboration; and (b) the evidence basis is **Tier 4–6 only** (international standards, national frameworks, or statutory codes) rich enough to produce a qualified synthesis. **Scale-tagging (G1b):** a T4–6-only determination is a *Universal-Mode regulatory determination* — `design_scale='universal'`, flagged `regulatory_stratum_only` (extending `code_floor_only` from the T6-only case), excluded from `v_best_practice`, and never rendered with best-practice language in any register (invariant I3, `governance/evidence-architecture.md` §6). For the T4–6 case, "rich enough" means:

- **≥2 Tier 4–5 sources** from different jurisdictions with convergent findings on the parameter, OR
- **≥1 Tier 4 international standard** (ISO, IEC, EN) with an evidence-based value directly addressing the parameter, OR
- **≥3 Tier 6 (code) sources** from different jurisdictions converging on the same value or range, establishing code consensus.

A cell with only a single Tier 6 source, or with multiple Tier 6 sources that diverge without convergence, is `pending` — the evidence is too sparse to synthesize even provisionally.

**The `provisional` confidence flag.** Every `provisional` cell carries a rendered confidence flag that names:

1. The evidence dimension(s) present (e.g., "Tier 4–5 international standards")
2. The evidence dimension(s) absent (e.g., "No Tier 1–3 clinical evidence; no Co-1 evidence")
3. The synthesis basis (e.g., "Value derived from ISO 21542 + BS 8300-2 convergence")

The flag is not editorial commentary — it is a structured declaration of the cell's evidence profile. The validator (Session 2) enforces flag presence and completeness.

**What `provisional` is not:** `provisional` is not "we think this might be right but we're not sure." It is "the evidence in the standards/code dimension supports this value, and the clinical/Co-1/Co-2 dimension has not been searched, has been searched and found empty, or contains only sources without direct parameter relevance." The gap is in the evidence profile, not in the synthesis quality.

### 2.4 The `pending` threshold

A cell is `pending` when evidence is too sparse across all dimensions to produce any synthesis — not even a `provisional` one. The cell carries:

1. A `[BEST-PRACTICE-PENDING]` display marker
2. A cross-link to `gap_register.md` identifying the gap and its search history
3. An implicit research trigger: the gap entry routes to the next research cycle for investigation

`pending` is the honest answer to "we don't know yet." Per mission §Epistemic commitments: silence on evidence-thin populations is not the default. The Cochrane yardstick (Altman & Bland, 1995) distinguishes absence-of-evidence from evidence-of-absence. `pending` is the former — the search has not returned usable evidence, not that the parameter is irrelevant.

### 2.5 The `not_applicable` state

A cell is `not_applicable` when the parameter genuinely has no design implication for the population. This is a positive assertion, not a gap. Examples:

- Grab bar diameter for DEM population in a corridor (grab bars are a MOB specification; DEM populations may need grab bars for co-occurring mobility impairment, but the parameter itself — diameter — is not DEM-specific)
- Signing space width for VIS population (signing space is a DEAF specification; VIS populations do not use sign language, though DBL populations do — DBL is a separate code)

`not_applicable` requires explicit rationale. The validator rejects `not_applicable` without a rationale string. The rationale must be population-specific — "not relevant" is insufficient; "this parameter addresses [function X] which is not impacted by [population]'s functional profile" is the minimum.

### 2.6 Co-2 evidence and the `stated` boundary — resolves Q4

**Q4 from A6 handoff:** *Does Co-2 alone count as "rich" for `provisional` purposes? Does Co-2 + Co-1 convergence carry the same confidence as Tier 1 + Co-1?*

**Resolution:** Co-2 alone satisfies the `stated` threshold per §2.2 condition (3) — the T-04 OR clause includes Co-2. A cell supported solely by one or more Co-2 CPGs (e.g., AOTA practice guidelines for home modification, RCOT specialist section housing guidance) is `stated`, not `provisional`.

This follows from the evidence hierarchy design: Co-2 encodes OT professional body consensus, which is a form of evidence above the standards/code tier. OT professional bodies synthesize clinical evidence, practice experience, and population knowledge into guidance documents. A CPG that addresses a design parameter directly carries sufficient epistemic weight for a `stated` claim.

**Co-2 + Co-1 convergence** carries the same structural confidence as Tier 1 + Co-1 convergence for the purpose of the state machine (both are `stated`). The convergence assessment (§3) records the specific combination, so downstream rendering and editorial judgment can distinguish "Tier 1 clinical + Co-1 convergence" from "Co-2 CPG + Co-1 convergence" — but the state-machine state is the same.

**Co-2 + Co-1 divergence** is handled per the same divergence protocol as Tier 1 + Co-1 divergence (§3.3). The cell is `stated`; the divergence is recorded as synthesis metadata, not as a state-machine state.

### 2.7 State transitions

States are not permanent. A cell may transition as evidence accumulates or is revised:

| From | To | Trigger |
|---|---|---|
| `pending` | `provisional` | Evidence at Tier 4–6 meets the §2.3 richness threshold |
| `pending` | `stated` | Evidence at Tier 1–3, Co-1, or Co-2 is found |
| `provisional` | `stated` | Evidence at Tier 1–3, Co-1, or Co-2 is found |
| `provisional` | `pending` | Previously cited Tier 4–5 sources are invalidated (e.g., standard superseded without replacement) |
| `stated` | `provisional` | All Tier 1–3, Co-1, and Co-2 sources are invalidated or retracted; Tier 4–6 evidence remains |
| `stated` | `pending` | All sources invalidated; no evidence remains |
| any | `not_applicable` | Analysis determines parameter is genuinely non-intersecting for this population |
| `not_applicable` | `pending` | Analysis reveals the parameter IS relevant (prior `not_applicable` was in error) |

**Transitions that do not occur:**

- `not_applicable` → `stated` directly (must pass through `pending` first — the evidence search has to run)
- `stated` → `not_applicable` (if evidence exists, the parameter is by definition applicable; the evidence may be wrong, but the state machine records evidence state, not parameter relevance directly)

### 2.8 Evidence-state and verification status interaction — resolves Q8 partial

Per A5 §6.3: validators block migration of cells whose only Co-1 source has `verification_status ∈ {UNVERIFIED-CLOSED, CLOSED-DELETED}`. The interaction with the state machine:

| Verification status of the cell's sources | State-machine effect |
|---|---|
| All cited sources `VERIFIED` or `VERIFIED-WITH-CORRECTION` | No effect — state determined by tier/type per §§2.2–2.5 |
| At least one source `UNVERIFIED-1` (one search attempt, not yet retried) | Cell retains its state but carries an `[UNVERIFIED-PENDING]` flag. The flag triggers a re-search before the cell's state can be used in downstream synthesis (ISW, Part 4 specification). Migration is not blocked — the cell exists in the corpus — but final synthesis is gated. |
| Cell's only qualifying source(s) are `UNVERIFIED-CLOSED` or `CLOSED-DELETED` | Cell state downgrades to `pending`. The evidence that supported the prior state has been disqualified. A gap-register entry is created if one does not exist. |
| Cell has both verified and unverified sources, and the verified sources alone still meet the state threshold | Cell retains its state. Unverified sources are flagged but do not downgrade the cell. |

This resolves the Q8 partial identified in the A6 handoff. Full Q8 resolution (implementation details for the validator's handling of `UNVERIFIED-1` re-search triggering) is deferred to Session 2 code implementation.

---

## 3. Cross-tier convergence and divergence

### 3.1 Convergence as evidence — mission §3 operationalized

Per `governance/mission-and-epistemics.md` §Epistemic commitments §Treatment of evidence convergence and divergence:

> Where Tier 1 clinical evidence and Co-1 lived experience converge on a parameter, the convergence is documented as strengthening the claim — neither dimension subsumes the other.

Convergence is not merely a bibliographic observation ("two sources agree"). It is an epistemic state: two independent evidence dimensions — one clinical, one experiential — arriving at the same finding through different methods. The convergence itself constitutes evidence because the probability of two methodologically independent dimensions converging by chance on the same parameter value is lower than either dimension arriving at that value independently.

This section specifies how convergence is encoded, assessed, and rendered.

### 3.2 Convergence assessment — resolves Q2

**Q2 from A6 handoff:** *When Tier 1 OT and Co-1 sources agree on a parameter value, the converged value carries higher confidence than either alone. How is this encoded in the schema?*

**Resolution:** Convergence is a property of the **synthesis**, not of individual sources. It is assessed at the (parameter × population) cell level, not at the source level. The encoding is a structured assessment attached to the cell (on the Specification entity or equivalently on the BPC best_practice_synthesis):

**Convergence assessment fields** (forward specification for Session 2 schema):

| Field | Type | Values |
|---|---|---|
| `convergence_status` | enum | `convergent`, `divergent`, `single_axis`, `pending_assessment` |
| `clinical_sources` | list[str] | REF-IDs of Tier 1–3 sources supporting the synthesis |
| `co1_sources` | list[str] | REF-IDs of Co-1 sources supporting the synthesis |
| `co2_sources` | list[str] | REF-IDs of Co-2 sources supporting the synthesis |
| `rationale` | str (optional) | Required for `divergent` and `single_axis`; optional for `convergent` |
| `synthesis_approach` | str (optional) | Required for `divergent`; specifies how the divergence is resolved at Tier 1 |

**Status definitions:**

- **`convergent`**: Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range. The converged claim carries higher confidence than either dimension alone. Rendered per voice pattern Co-1-C (A5 §5.1).
- **`divergent`**: Tier 1–3 clinical evidence and Co-1 evidence bear on the same parameter but arrive at different values or ranges. Both are presented; synthesis approach is specified. Rendered per voice pattern Co-1-D (A5 §5.1).
- **`single_axis`**: Evidence exists in only one dimension (clinical only, or Co-1 only, or Co-2 only, or Tier 4–6 only). No convergence or divergence assessment is possible. Rendered per voice pattern Co-1-A or Co-1-B as appropriate.
- **`pending_assessment`**: Evidence exists in multiple dimensions but the value-level convergence assessment has not yet been performed. Per unification-DR item G8 (ACCEPTED 2026-07-13) this is no longer only a transitional migration state: while `source_value_extractions` coverage lags, honestly-assessed multi-axis cells hold this status durably rather than claiming unassessed convergence.

**The convergence assessment is not a confidence score.** It does not produce a number. It produces a categorical status with documented sources and rationale. The reason: confidence scores imply a false precision about the probability of correctness. The convergence assessment says what the evidence profile is and how the sources relate — the reader (and the Person-Mode OT) applies judgment.

### 3.3 Divergence within `stated` — resolves Q3

**Q3 from A6 handoff:** *A cell with strong Tier 1 OT clinical evidence AND strong Co-1 evidence that diverge — both are "rich" — is currently classified `stated` per T-04. But the divergence is itself an epistemic state needing handling beyond simple `stated`. Does this require a fifth state?*

**Resolution:** No fifth state. The cell is `stated`. The divergence is captured through the convergence assessment (§3.2), not through the state machine.

**Rationale:** The four states encode **evidence sufficiency** — whether enough evidence exists to make a defensible claim. Convergence and divergence encode **evidence agreement** — whether the sources point in the same direction. These are independent questions:

- A cell with converging Tier 1 + Co-1 evidence: `stated`, `convergence_status: convergent`
- A cell with diverging Tier 1 + Co-1 evidence: `stated`, `convergence_status: divergent`
- A cell with Co-1 only: `stated`, `convergence_status: single_axis`
- A cell with Tier 5 only: `provisional`, `convergence_status: single_axis`

Adding a fifth state (`stated_divergent`) would conflate the two questions, making the state machine harder to validate and reason about. A validator checking "is this cell's state correct?" should only need to ask "is the evidence sufficient?" — not also "do the sources agree?" Convergence assessment is a separate validation pass.

**How divergence is handled in practice:**

1. The cell is `stated` (evidence is sufficient from both dimensions).
2. The convergence assessment records `divergent` with the sources and rationale.
3. The Tier 1 design range encompasses both findings (per A5 §3.5, Pattern Co-1-D).
4. The synthesis approach specifies which dimension governs the default and why (typically per harm-asymmetry — see project-standards harm-asymmetry rule).
5. Voice pattern Co-1-D renders the divergence in prose.
6. At Tier 2, OT assessment resolves the individual's position within the range — the divergence at Tier 1 becomes input to person-specific co-design.

**What this resolution preserves:** T-04 is not revised. The four states remain exactly as specified. The convergence assessment is a separate metadata layer that operates alongside the state machine, not within it.

### 3.4 Convergence and the specification voice

The convergence assessment determines which voice pattern governs the specification prose:

| Convergence status | Voice pattern | Construction |
|---|---|---|
| `convergent` | Co-1-C | "Tier 1 OT evidence ([sources]) and Co-1 sources ([sources]) converge on [claim]." |
| `divergent` | Co-1-D | "Tier 1 OT evidence shows [finding-1]. Co-1 sources document [finding-2]. The range encompasses both. [Synthesis approach.]" |
| `single_axis` (Co-1 only) | Co-1-A or Co-1-B | "[Source] documents [finding]." or "Co-1 sources document [claim]; sources: [list]." |
| `single_axis` (clinical only) | §8.1 Tier 1 construction | "[Evidence tier] evidence supports [value]." |
| `single_axis` (Co-2 only) | §8.1 adapted | "OT professional body guidance ([CPG]) recommends [value]." |
| `single_axis` (Tier 4–6 only) | §8.1 Universal Mode construction | "Code requires [value] per [standard]." or "[N] jurisdictions' standards converge on [value] — convergence is not evidence: no anchoring (T1/Co-1/T2/Co-2) basis exists; treat as floor, not target" (mandatory disclaimer per G1b; invariant I3 bars best-practice language on these cells in every register) |
| `pending_assessment` | Rendered ONLY with the value-level-convergence-pending disclosure in every register (G8; the register map's `stated_multi_axis` rows carry it) | Axis co-presence is real; value-level convergence is queued, never assumed |

### 3.5 Cross-entity integration

The convergence assessment interacts with three entity types in the schema:

1. **EvidenceSource** — provides the source records cited in `clinical_sources`, `co1_sources`, `co2_sources`. The convergence assessment does not modify EvidenceSource records; it references them.
2. **Specification** — carries the convergence assessment as a property of the synthesized claim. Each Specification record's best-practice value is the output of the synthesis; the convergence assessment documents the input evidence profile.
3. **BPCMetadata** — the best_practice_synthesis section of the BPC file is where the convergence assessment is first performed (during multilingual-research or Opus synthesis). The Specification entity inherits the assessment when the BPC finding is converted to a specification record via ISW.

**Session 2 schema design** adds the convergence assessment fields to either the Specification entity directly or as a separate linked entity (ConvergenceAssessment). The governance specification here is agnostic to storage form — that is a B1 decision. The fields and their semantics are binding.

---

## 4. Values-criteria assessment mechanism — resolves Q5

### 4.1 The problem

Two populations may have evidence-supported preferences that conflict on the same design parameter. Neither preference is wrong; both are grounded in legitimate lived experience or clinical evidence. The conflict is not about harm — it is about values.

Example: residential primary entrance threshold. The visitability framework (Concrete Change 1987; Co-1) specifies zero-step (0 mm) to ensure any person can enter. Some PAIN-population evidence supports textured threshold landings (≤6 mm, with slip-resistant tactile surface) for proprioceptive feedback at the entrance transition. Both positions have evidence. Neither is harmful. They conflict on the same physical parameter.

Person-Mode OT co-design resolves this at the individual scale — the OT and the occupant determine what is right for this person. But at Population Mode, the guidebook must specify a default and a range. The values-criteria mechanism governs how that default is set.

### 4.2 Resolution: three-step values-criteria assessment

When a (parameter × population) synthesis identifies a values-based conflict (as distinct from a function-based harm conflict), the following mechanism applies:

**Step 1 — Classify the conflict type.**

| Type | Definition | Resolution path |
|---|---|---|
| Function-based (harm) | One population faces greater physical, neurological, or psychological harm from the wrong default | Harm-asymmetry rule (project-standards, existing). Higher-harm population sets default. |
| Values-based (preference) | Both populations have evidence-supported preferences; neither faces disproportionate harm from the other's default | Broadest-benefit assessment (this section). |
| Variable-conflation | Apparent conflict dissolves because opposing needs operate on different physical variables | Step 0 in §3.8 decision tree (project-standards). Not a real conflict. |

If a conflict is function-based, the harm-asymmetry rule governs and this section does not apply. Values-criteria applies only to conflicts classified as values-based.

**Step 2 — Broadest-benefit assessment.**

For values-based conflicts, the Population-Mode default is set by asking: *which default serves the broadest population or the most constrained use case?*

Criteria, applied in order:

1. **Population breadth.** If one preference serves a larger number of affected populations (not just the population that generated the evidence, but all populations in the shared space), that preference is the default. Example: zero-step serves MOB, VIS, DEM, NDV, OFS, PAIN (ambulatory), aging-in-place populations. Textured threshold serves some PAIN individuals. Zero-step is broader.

2. **Irreversibility.** If one preference, once built, forecloses future adaptation and the other preserves it, the preserving option is the default. Example: a zero-step threshold can later receive an applied tactile mat; a 6 mm threshold cannot be reduced to zero without structural modification. Zero-step is more adaptable.

3. **Supplementary provision feasibility.** If the non-default preference can be achieved through supplementary provision (personal aids, surface treatments, staff-operated adjustments) without modifying the built structure, this supports setting the other as the structural default. Example: proprioceptive feedback can be provided via an applied threshold mat or entry-zone flooring change, without requiring a raised threshold.

If all three criteria point the same direction, the default is clear. If they conflict, the specification documents the assessment and routes to Tier 2 for individual resolution, with the broadest-population preference as the nominal default.

**Step 3 — Documentation.**

The specification carries:

- The Population-Mode default with rationale ("Broadest-benefit: zero-step serves [N] populations; proprioceptive feedback achievable via supplementary surface treatment")
- The alternative preference with its evidence basis
- The Person-Mode handoff: "OT assessment may specify [alternative] based on individual proprioceptive needs"
- The convergence assessment (§3.2): `divergent` with synthesis_approach documenting the broadest-benefit reasoning

### 4.3 What the values-criteria mechanism does not do

- **Does not override harm-asymmetry.** If one population faces genuine harm (neurological deterioration, fall risk, entrapment), that is function-based, not values-based. Harm-asymmetry governs.
- **Does not claim one population's values are more legitimate.** Both preferences are evidence-grounded. The mechanism selects a structural default, not a correct value.
- **Does not eliminate Person-Mode resolution.** The default is a starting point. Person-Mode OT co-design may override it for an individual whose needs are better served by the alternative.
- **Does not apply to Universal Mode.** Universal Mode (universal design / code compliance) is set by code. Values-criteria applies at Tier 1 only.

## 5. Design-pedagogy literature engagement — resolves Q6

### 5.1 The classification question

The guidebook's questions-led pedagogical commitment (Doctrinal commitment 6; mission §Epistemic commitments §Questions-led teaching) cites three foundational sources:

- Schön, D.A. (1983). *The Reflective Practitioner.* DOI: 10.4324/9781315237473
- Hmelo-Silver, C.E. (2004). Problem-Based Learning: What and How Do Students Learn? *Educational Psychology Review* 16(3). DOI: 10.1023/B:EDPR.0000034022.16470.f3
- Royeen, C.B. (1995). A Problem-Based Learning Curriculum for Occupational Therapists. *AJOT* 49(4). DOI: 10.5014/ajot.49.4.338

Q6 asks: how do these citations operate in the evidence base? What tier are they?

### 5.2 Resolution: meta-methodological citations — outside the evidence hierarchy

These three sources are **meta-methodological citations**. They provide evidence for the guidebook's pedagogical approach — how the guidebook teaches — not evidence for any design parameter. The seven-tier evidence hierarchy governs evidence about built environment design. Pedagogy literature addresses a different question: *does questions-led resource design improve outcomes for the people who use the resource?*

**Classification:** meta-methodological citations sit outside the seven-tier hierarchy. They are not Tier 2 (they are not systematic reviews or evidence-based standards of design evidence), not Tier 5 (they are not national beyond-code frameworks for accessible design), and not any other tier. Forcing them into the hierarchy conflates two distinct evidence questions — "what should the design parameter be?" and "how should the guidebook present design parameters?"

### 5.3 Operational treatment

| Aspect | Treatment |
|---|---|
| **Citation location** | Part 1 (methodology declaration), mission document, front matter. Not in Part 4 specification cells. |
| **Evidence marker** | No ● or ○ marker. Evidence markers govern design parameter specifications; pedagogy citations are not design specifications. |
| **Rendering** | Standard academic citation. Author (Year), title, DOI. No tier badge. |
| **Validator handling** | `validate_evidence_state.py` does not process meta-methodological citations. They do not appear in EvidenceSource records (which are for design parameter evidence). They appear in the bibliography as standard academic references. |
| **Testability** | The questions-led hypothesis is acknowledged as a claim, not established fact (mission §Epistemic commitments). Empirical testing is staged at B6 pilot validation (solo-author cross-checking pre-launch; weaker rigor than external testing). |

### 5.4 Boundary: what qualifies as meta-methodological

A citation is meta-methodological when it provides evidence about the guidebook's method (its pedagogical approach, its evidence synthesis methodology, its theoretical framework) rather than about a design parameter's value. The four-framework theoretical layering (ICF, PEO/PEOP, Capability Approach, Kawa — per project-standards 2026-04-09) is also meta-methodological: these frameworks structure the guidebook's approach, not individual specifications.

Citations that inform both the method and a design parameter — for example, OT clinical reasoning literature that both shapes the guidebook's Tier 2 co-design approach and provides evidence about assessment protocols — carry their design-parameter tier (typically Tier 1 or Co-2) for the parameter evidence and are additionally cited as methodological basis where relevant. The tier governs the parameter cell; the methodological citation is supplementary.

## 6. Epistemic-defense specification — resolves Q7

### 6.1 Purpose

The epistemic-defense specification defines how guidebook prose handles challenges to the guidebook's evidence basis. This is a requirements specification for a future skill (C2 build); A6 defines *what* the skill must do, not *how* it is implemented.

The need: readers, reviewers, and practitioners encountering the guidebook will challenge its evidence claims. Some challenges are legitimate (evidence gaps exist; the guidebook should acknowledge them). Some challenges rest on misunderstanding the evidence hierarchy or the guidebook's epistemic position. The epistemic-defense skill equips the author (and future contributors) with structured response patterns.

### 6.2 Challenge categories and response patterns

| Challenge | Example | Response pattern |
|---|---|---|
| **Evidence-tier challenge** | "Where's the RCT for that threshold value?" | Cite the evidence chain with tier location. If no Tier 1 clinical evidence exists: state the tier that does exist; name the gap per T-04 state; explain that Co-1 or Co-2 evidence is co-primary, not subordinate. Never fabricate a higher-tier basis. |
| **Co-1 legitimacy challenge** | "That's just opinion, not evidence." | Cite CRPD Art. 4.3 grounding. Explain that Co-1 is methodologically grounded (peer review, organizational accountability, scholarly authorship per A5 §1.2), not aggregated opinion. Name the specific sources. |
| **Code-sufficiency challenge** | "Building codes don't require that." | Explain the Universal Mode / Tier 1 distinction. Codes (Tier 6) are the compliance floor, not the aspiration. The guidebook recommends provisions above the code floor where higher-tier evidence supports them. The code floor is already met; the question is what the evidence supports beyond it. |
| **Economic challenge** | "Show me the cost-benefit." | Route to Part 11 evidence. If Part 11 does not cover the specific parameter: acknowledge the gap, note that absence of economic evidence does not invalidate the design evidence, and flag for future Part 11 expansion. |
| **Jurisdictional challenge** | "That's not how we do it here." | Present the jurisdictional comparison from the BPC. Note that best practice is determined by the evidence hierarchy, not by code consensus (project-standards Core Doctrine). Acknowledge legitimate jurisdictional differences in regulatory context. |
| **Authority challenge** | "Who says this is best practice?" | The guidebook is an advocacy project (Core Doctrine). It does not claim mandating authority. Its recommendations are grounded in the evidence hierarchy it discloses. The reader applies professional judgment informed by this evidence. The value is in the comprehensiveness and transparency of the synthesis, not in institutional authority. |
| **Gap challenge** | "You don't have evidence for that." | If the challenge is correct: acknowledge the gap. Cite the T-04 state (`pending` or `provisional` with confidence flag). Route to gap_register.md. If the challenge is incorrect (evidence exists but was not visible to the challenger): cite the evidence with tier and source. |

### 6.3 Decision rules

When a section of prose or a specification cell faces an evidence-basis challenge, the response follows this decision sequence:

1. **Is the challenge factually correct?** Does a gap exist? Is the tier lower than claimed? Is the source unverified?
   - If yes: acknowledge. Update the T-04 state if needed. Route to gap_register. Do not defend a claim that is not defensible.
   - If no: proceed to step 2.

2. **Is the challenge based on a misunderstanding of the evidence hierarchy?**
   - If yes: explain the hierarchy. Most common: confusion between "no RCT" and "no evidence" (Co-1 and Co-2 are evidence); confusion between "not in the code" and "not best practice" (codes are Tier 6).
   - If no: proceed to step 3.

3. **Is the challenge about the guidebook's authority?**
   - If yes: apply the advocacy-identity response (§6.2 authority challenge). The guidebook does not claim authority it does not have.

4. **Is the challenge about economic feasibility?**
   - If yes: route to Part 11. Acknowledge limitations if Part 11 coverage is thin.

5. **Is the challenge irresolvable with current evidence?**
   - If yes: document the challenge as an open question. Add to gap_register if not already there. The epistemic-defense skill does not resolve all challenges — it ensures they are handled honestly.

### 6.4 Voice conventions for epistemic defense

The response voice follows §8.1 (tier-appropriate specification voice) and §8 framing standards (epistemic authority — do not overclaim). Specific patterns:

- **Never claim the guidebook "proves" or "establishes" a design parameter.** The guidebook synthesizes evidence and recommends. The evidence establishes; the guidebook presents.
- **Never dismiss a challenge as uninformed.** Explain the basis. If the challenger's understanding of the hierarchy differs from the guidebook's, present the guidebook's framework transparently.
- **Always name the evidence tier when defending a claim.** "This specification is based on Tier 2 evidence (Sanford 2010 SR)" — not "research supports this."
- **Acknowledge gaps immediately when they exist.** The guidebook's credibility rests on honesty about what it does and does not know. A defended gap is worse than a disclosed one.

### 6.5 Skill build specification (forward to C2)

The `epistemic-defense` skill, when built at C2, implements:

- **Input:** a prose passage or specification cell + the challenge text
- **Processing:** classify the challenge per §6.2 categories; apply §6.3 decision sequence; select response pattern
- **Output:** a draft response with tier-located evidence citations and, if applicable, an updated T-04 state or gap_register entry
- **Validation:** response must not overclaim (per §8 framing standards); response must cite specific sources (no generic "research shows"); response must acknowledge gaps where they exist

The skill is prose-only (no Python validator). Its quality depends on the author's judgment informed by the patterns above. The patterns are the specification; the skill operationalizes them.

---

## 7. Resolutions register

| Question | Resolution | Confidence | Section |
|---|---|---|---|
| Q1 — "Rich in one dimension" threshold for `provisional` | `provisional` applies to Tier 4–6-only cells meeting richness criteria (≥2 T4–5 convergent, or ≥1 T4 international standard, or ≥3 T6 convergent). Tier 1–3 / Co-1 / Co-2 → `stated`. | high — direct operationalization of T-04 OR clause | §2.3 |
| Q2 — Cross-tier convergence encoding | Convergence assessment is a structured property of the synthesis cell (not of individual sources); four statuses: convergent, divergent, single_axis, pending_assessment | high — follows from mission §3 convergence-as-evidence principle | §3.2 |
| Q3 — Fifth state for divergent evidence? | No. Cell is `stated`; divergence is synthesis metadata via convergence assessment, not a state-machine state. Four states preserved per T-04. | high — separates evidence sufficiency from evidence agreement; T-04 unchanged | §3.3 |
| Q4 — Co-2 alone as "rich" for `stated` | Yes. Co-2 alone satisfies `stated` per T-04 OR clause. OT professional body CPGs carry sufficient epistemic weight. | high — literal application of T-04 definition | §2.6 |
| Q5 — Values-criteria mechanism | Three-step assessment: classify conflict type (function/values/conflation) → broadest-benefit assessment (population breadth, irreversibility, supplementary feasibility) → documentation with Person-Mode handoff. Applies at Population Mode only. | high — extends existing harm-asymmetry framework to values-based conflicts without overriding it | §4 |
| Q6 — Design-pedagogy tier classification | Meta-methodological: outside the seven-tier hierarchy. Pedagogy literature supports the guidebook's method, not design parameters. Cited in Part 1 / mission, not in specification cells. No evidence marker. | high — clean separation of "what should the parameter be?" from "how should the guidebook present parameters?" | §5 |
| Q7 — Epistemic-defense skill specification | Seven challenge categories with response patterns; five-step decision sequence; voice conventions; C2 skill build forward spec. Requirements only — C2 builds implementation. | high — direct application of advocacy identity + evidence hierarchy + framing standards | §6 |
| Q8 — Verification status interaction (partial) | `UNVERIFIED-1`: flag but don't downgrade. `UNVERIFIED-CLOSED`/`CLOSED-DELETED` as sole qualifying sources: downgrade to `pending`. Full implementation deferred to Session 2. | high — extends A5 §6.3 rule to state-machine level | §2.8 |

---

## 8. Forward specifications

### Session 2 deliverables (COMPLETE)

Delivered in A6 Session 2 (2026-04-29 18:05):

1. **`schemas/evidence_state.py`** — EvidenceStateRecord, ConvergenceAssessment, ProvisionalConfidenceFlag models.
2. **`schemas/enums.py`** — EvidenceCellState, ConvergenceStatus, Co1Provenance, Co1SourceType, VerificationStatus enums. Co-2 tier corrected to 2 per T-03.
3. **`schemas/evidence_source.py`** — A5 Co-1 fields added; Co-1 field consistency model validator.
4. **`scripts/validate_evidence_state.py`** — CI validator for evidence states and Co-1 source fields.
5. **`scripts/convert/convert_sources.py`** — Updated with Co-1 field population, Co-2 tier fix, `--co1` mode.

### Remaining forward items

- **Multilingual-research output validator** — wrapper validator for Co-1 provenance on non-English literature review outputs. Deferred: may fold into C-stage multilingual-research skill rebuild. Not blocking A6 closure.
- **B1 schema design** — inherits convergence assessment specification (§3.2) and Co-1 field requirements (§1.3, A5 §7.1) as binding input.
- **C2 skill builds** — epistemic-defense skill (§6.5 forward spec) and values-criteria integration into cross-population-conflict-mapper.
- **C7 evidence migration** — 584 sources + 81 unverified residual disposition bound to A6 schema and validator.

### Status

| Field | Value |
|---|---|
| Created | 2026-04-29 17:35 UTC (S1) |
| Session 2 | 2026-04-29 18:05 UTC (schema + validator) |
| Session 3 | 2026-04-29 19:06 UTC (§§4–6 complete) |
| Phase | Stage A Phase 6 (Evidence methodology) — COMPLETE |
| Status | CANONICAL — all 8 questions resolved; all sections complete |
| Resolves | Q1 (provisional threshold), Q2 (convergence encoding), Q3 (no fifth state), Q4 (Co-2 = stated), Q5 (values-criteria), Q6 (design-pedagogy), Q7 (epistemic-defense), Q8 (verification interaction) |
| Sessions consumed | 3 of 3–5 budget |
| Forward dependencies | B1 (schema design), C2 (epistemic-defense skill build), C7 (evidence migration) |

---

**End of A6 governance document.**
