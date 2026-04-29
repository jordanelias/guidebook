# Evidence Methodology
**Status:** DRAFT — A6 Session 1
**Phase:** Stage A Phase 6 — Evidence methodology
**Created:** 2026-04-29 17:35 UTC
**Doctrinal basis:** T-03 (`governance/pre-stage-a-decisions.md`) · T-04 (same) · `governance/co1-operational.md` (A5 CANONICAL) · `governance/mission-and-epistemics.md` §Epistemic commitments · voice-style §§8.1, 8.2, 8.3
**Pattern:** Governance + Code (governance this session; code Session 2)

---

## 1. Evidence hierarchy — operational definition

### 1.1 The seven-tier hierarchy

The guidebook draws on seven tiers of evidence, with two co-primary parallel tiers (Co-1, Co-2). The full hierarchy is defined in `governance/mission-and-epistemics.md` §Epistemic commitments §Evidence hierarchy and reproduced in `references/project-standards.md` Core Doctrine. This section operationalizes it — specifying how each tier is encoded, validated, and used in best-practice synthesis.

| Position | Tier value | Evidence type | Source examples |
|---|---|---|---|
| Tier 1 | `tier: 1` | `evidence_type: clinical` | OT intervention-tested clinical research; RCTs; intervention trials |
| Co-1 | `tier: 1` | `evidence_type: co1` | Lived experience / participatory design (CRPD Art. 4.3); DPO research; peer-reviewed lived-experience literature; named advocacy organizational positions; Co-1-authored academic narratives |
| Tier 2 | `tier: 2` | `evidence_type: standard_eb` or context-dependent | NGO / DPO / advocacy guidelines |
| Co-2 | `tier: 2` | `evidence_type: co2` | OT professional body CPGs (CAOT, AOTA, RCOT, COTEC, WFOT) |
| Tier 3 | `tier: 3` | `evidence_type: sr_meta` | Systematic reviews; meta-analyses; narrative SRs |
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

### 1.4 Relationship to the Three-Tier Design Hierarchy

The Seven-Tier Evidence Hierarchy and the Three-Tier Design Hierarchy are orthogonal axes (per A5 §3.5). They co-locate authority for any specification:

- **Design Hierarchy** locates the *kind of design decision*: Tier 0 (universal, code-compliant); Tier 1 (population-informed, ranges with median); Tier 2 (person-specific, OT-resolved).
- **Evidence Hierarchy** locates *what evidence supports the value*: what tier, what type, how strong.

Every cell in the specification matrix sits at an intersection of both axes. A Design Tier 1 specification (population-informed range) may be supported by evidence at any Evidence Tier — clinical, Co-1, Co-2, standards, or a combination. The evidence tier does not determine the design tier; the design tier does not constrain which evidence tiers are consulted.

### 1.5 Tier 2 NGO/DPO/advocacy evidence vs. Co-1

Tier 2 in the evidence hierarchy ("NGO / DPO / advocacy guidelines") and Co-1 are distinct. They share organizational provenance (both may come from DPOs) but differ in what they encode:

- **Tier 2** encodes organizational *guidelines* — recommendations an organization publishes for how accessible design should be done. The organization's authority is institutional (its reputation, its constituency, its mandate).
- **Co-1** encodes lived-experience *evidence* — findings produced by, with, or under methodological authority of disabled people. The evidence's authority is methodological (peer review, organizational accountability, or scholarly authorship per A5 §1.2).

A DPO may produce both: a design guideline (Tier 2) and a lived-experience research output (Co-1). The same organization, different epistemic products. Encoding matters because best-practice synthesis treats Co-1 as co-primary with Tier 1 clinical evidence — a stronger epistemic claim than Tier 2 guidelines carry.

The validator (Session 2) enforces this: a source classified as both `co1` and `standard_eb` (or `national_fw` or `code`) is an error. A source may have one `evidence_type`; its tier follows from that type. Tier 2 DPO guidelines carry `evidence_type: standard_eb` (if evidence-based) or `national_fw`, not `co1`.

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

A cell reaches `stated` when it has **at least one source meeting any of the following conditions:**

1. **Tier 1–3 clinical evidence** with direct parameter relevance — a clinical research finding, systematic review, or meta-analysis that addresses the design parameter for the target population.
2. **Co-1 evidence** with direct parameter relevance — a Co-1 source (per §1.3 requirements, with `verification_status ∈ {VERIFIED, VERIFIED-WITH-CORRECTION}`) that addresses the design parameter for the target population.
3. **Co-2 evidence** with direct parameter guidance — an OT professional body CPG that addresses the design parameter.

The OR clause is deliberate: Co-1 alone is sufficient for `stated`, as is Co-2 alone, as is Tier 3 alone. This follows from the doctrinal commitment that Co-1 is co-primary with Tier 1 — a best-practice claim grounded solely in strong Co-1 evidence is a legitimate evidence-based claim, not a provisional one.

**What `stated` does not mean:** `stated` does not mean the claim is beyond dispute. It means the evidence basis is sufficient to make a defensible best-practice claim at the tier cited. A `stated` cell may still be revised when new evidence emerges, when higher-tier evidence replaces lower-tier, or when cross-tier divergence is resolved through new research.

### 2.3 The `provisional` threshold — resolves Q1

**Q1 from A6 handoff:** *What constitutes "rich evidence in at least one dimension" for `provisional` state?*

**Resolution:** A cell is `provisional` when it has evidence that is **rich enough to synthesize** but does not meet the `stated` threshold — meaning it has no source at Tier 1–3, no Co-1 source, and no Co-2 source with direct parameter relevance.

Concretely, `provisional` applies when the evidence basis is **Tier 4–6 only** (international standards, national frameworks, or statutory codes) and the evidence is rich enough to produce a qualified synthesis. "Rich enough" means:

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
- **`pending_assessment`**: Evidence exists in multiple dimensions but the convergence assessment has not yet been performed (transitional state during migration).

**The convergence assessment is not a confidence score.** It does not produce a number. It produces a categorical status with documented sources and rationale. The reason: confidence scores imply a false precision about the probability of correctness. The convergence assessment says what the evidence profile is and how the sources relate — the reader (and the Tier 2 OT) applies judgment.

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
| `single_axis` (Tier 4–6 only) | §8.1 Tier 0/1 construction | "Code requires [value] per [standard]." or "[N] jurisdictions' standards converge on [value]." |
| `pending_assessment` | Not rendered | Cell is flagged for assessment before publication |

### 3.5 Cross-entity integration

The convergence assessment interacts with three entity types in the schema:

1. **EvidenceSource** — provides the source records cited in `clinical_sources`, `co1_sources`, `co2_sources`. The convergence assessment does not modify EvidenceSource records; it references them.
2. **Specification** — carries the convergence assessment as a property of the synthesized claim. Each Specification record's best-practice value is the output of the synthesis; the convergence assessment documents the input evidence profile.
3. **BPCMetadata** — the best_practice_synthesis section of the BPC file is where the convergence assessment is first performed (during multilingual-research or Opus synthesis). The Specification entity inherits the assessment when the BPC finding is converted to a specification record via ISW.

**Session 2 schema design** adds the convergence assessment fields to either the Specification entity directly or as a separate linked entity (ConvergenceAssessment). The governance specification here is agnostic to storage form — that is a B1 decision. The fields and their semantics are binding.

---

## 4. Values-criteria assessment mechanism

*Deferred to A6 Session 3 per handoff §5 methodology recommendation.*

## 5. Design-pedagogy literature engagement

*Deferred to A6 Session 3 per handoff §5 methodology recommendation.*

## 6. Epistemic-defense skill specification

*Deferred to A6 Session 3 per handoff §5 methodology recommendation.*

---

## 7. Resolutions register

| Question | Resolution | Confidence | Section |
|---|---|---|---|
| Q1 — "Rich in one dimension" threshold for `provisional` | `provisional` applies to Tier 4–6-only cells meeting richness criteria (≥2 T4–5 convergent, or ≥1 T4 international standard, or ≥3 T6 convergent). Tier 1–3 / Co-1 / Co-2 → `stated`. | high — direct operationalization of T-04 OR clause | §2.3 |
| Q2 — Cross-tier convergence encoding | Convergence assessment is a structured property of the synthesis cell (not of individual sources); four statuses: convergent, divergent, single_axis, pending_assessment | high — follows from mission §3 convergence-as-evidence principle | §3.2 |
| Q3 — Fifth state for divergent evidence? | No. Cell is `stated`; divergence is synthesis metadata via convergence assessment, not a state-machine state. Four states preserved per T-04. | high — separates evidence sufficiency from evidence agreement; T-04 unchanged | §3.3 |
| Q4 — Co-2 alone as "rich" for `stated` | Yes. Co-2 alone satisfies `stated` per T-04 OR clause. OT professional body CPGs carry sufficient epistemic weight. | high — literal application of T-04 definition | §2.6 |
| Q8 — Verification status interaction (partial) | `UNVERIFIED-1`: flag but don't downgrade. `UNVERIFIED-CLOSED`/`CLOSED-DELETED` as sole qualifying sources: downgrade to `pending`. Full implementation deferred to Session 2. | high — extends A5 §6.3 rule to state-machine level | §2.8 |

---

## 8. Forward specifications for Session 2

Session 2 (schema + validator implementation) inherits these binding specifications:

1. **`schemas/evidence_state.py`** — Pydantic model encoding the four T-04 states, the convergence assessment, and the richness thresholds from §§2.2–2.5.
2. **`scripts/validate_evidence_state.py`** — CI validator enforcing:
   - `pending` cells reference `gap_register.md`
   - `provisional` cells carry confidence flag with named dimensions
   - `not_applicable` cells carry rationale
   - `stated` cells cite ≥1 source at Tier 1–3 OR Co-1 OR Co-2
   - Verification-status downgrade logic per §2.8
   - Convergence assessment completeness for `stated` cells with multi-axis evidence
3. **`scripts/convert/convert_sources.py`** — sample converter taking existing BPC/source data and producing validated EvidenceSource records per the A5 six-field specification + A6 convergence assessment.

### Status

| Field | Value |
|---|---|
| Created | 2026-04-29 17:35 UTC |
| Phase | Stage A Phase 6 (Evidence methodology) — Session 1 of 3–5 |
| Status | DRAFT — §§1–3 complete; §§4–6 deferred to Session 3; §§7–8 are registers |
| Resolves | Q1, Q2, Q3, Q4, Q8 (partial) |
| Defers | Q5 (values-criteria), Q6 (design-pedagogy), Q7 (epistemic-defense) |
| Forward dependencies | Session 2 (schema + validator); Session 3 (values-criteria + design-pedagogy + epistemic-defense) |

---

**End of A6 Session 1 governance draft.**
