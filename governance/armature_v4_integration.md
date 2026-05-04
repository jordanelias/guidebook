# Armature v4 + Resolutions — Workplan Judgment and Integration

**Date:** 2026-04-28 07:45
**Author:** Opus 4.6
**References:** armature_v4.md, armature_v4_resolutions.md, workplan-orchestrator_SKILL.md, roadmap-2026-04-27.md, governance/conceptual-model.md, governance/pre-stage-a-decisions.md, governance/audience-priority.md, schemas/*.py

---

## 1. Judgment against locked doctrine

### No conflicts

| Locked decision | Armature alignment | Conflict? |
|---|---|---|
| T-03: tier + evidence_type encoding | Armature adds synthesis_method_indicator as a third evidence dimension. Orthogonal to T-03 — does not change tier or evidence_type semantics. | No |
| T-04: sparse-evidence state machine (stated/provisional/pending/not_applicable) | Armature's evidence markers (●/○) are a user-facing presentation of the state machine. ● maps to `stated`. ○ maps to `provisional` or `pending` depending on evidence basis. Consistent. | No |
| D-03 revised: pre-launch solo; Co-1 at evidence level only | Armature §9 (Authority and validation) is directly consistent. Three-tier validation framework (A: published literature / B: clinical specialist / C: PWLE/DPO) aligns with D-03's pre-launch solo + post-launch contingent structure. Tier A = D-03 pre-launch. Tier C = D-03 post-launch contingent. | No |
| Design Modes | Armature carries Universal Mode/1/2 throughout. Maps to CRPD Art 9 / Art 5. Consistent. | No |
| Seven-Tier Evidence Hierarchy | Armature references without modification. Synthesis method indicator is additive, not conflicting. | No |
| Best practice = most accommodating evidence-supported condition | Armature output schema carries recommendation_strength. Consistent. | No |
| Advocacy identity | Armature §7.1 carries advocacy-not-authority framing. Tier-appropriate specification language. Consistent. | No |
| Audience priority: primary (designers, disabled people), secondary (OTs, policymakers) | Armature role layer: 5 roles. Designer and disabled person are listed. Audience-priority doc governs content layering when needs diverge — the armature's role layer is the mechanism for implementing this. Consistent. | No |

**Determination: armature v4 + resolutions introduce no doctrinal conflicts.** All proposals are additive or implementive. No locked decisions require revision.

---

## 2. Judgment against A3 (signed off)

A3 signed off 2026-04-26 with 6 entity types schematized, 1098 records, Pydantic validation operational.

### What the armature proposes that A3 doesn't have

| Proposal | A3 state | Impact |
|---|---|---|
| **PopulationCategory** (7th entity type) | A3 has E-12 (Sub-population) deferred to A7. PopulationCategory subsumes E-12 and is substantially larger — a content-bearing entity with multilingual names, mapping confidence, sub-classification scaffolds, validation provenance, population-specific design considerations. | A3 amendment required. Exceeds E-12 scope. |
| **axes_applicable** array on Specification | A3 has `populations: list[str]` + cross-cutting `design_stages` and `project_types`. No functional-axis attributes. | Schema extension at A7 (when axis set is finalized). |
| **jurisdiction_scope** structured array | A3 has `jurisdictions_supporting: list[str]` + `jurisdictions_divergent: list[str]` + `divergence_note: Optional[str]`. Armature proposes richer structure with per-jurisdiction compliance status. | Schema extension at A8 (when jurisdiction philosophy is settled). |
| **synthesis_method_indicator** + **inference_basis** | Not in current schema. | Schema extension at A6 (evidence methodology). |
| **tier2_handoff** structure | A3 has `person_specific_note: Optional[str]` — free text. Armature proposes structured handoff with parameter, range, referral threshold. | Schema extension at A6 or A7. |
| **adjustability_metadata** structure | Not in current schema. | Schema extension at A7 or later. |
| **physical_variable** identifier | Not in current schema. Needed for variable conflation check algorithm. | Schema extension — timing TBD. |
| **cultural_context** array | Not in current schema. | Schema extension at A8 or later. |
| **version_history** array | A3 deferred time-versioning to A9 (E-19). Consistent. | A9 handles this. |
| **EvidenceSource search_strategy, screening_counts, quality_assessment** | Not in current schema. | Schema extension at A6. |
| **BPCMetadata synthesis_method, quality_summary** | Not in current schema. | Schema extension at A6. |
| **Gap user_facing, population_level, surfacing_method** | Not in current schema. | Schema extension — timing flexible. |

### Determination

A3 does not need to be reopened wholesale. The signed-off entity inventory and relationships are structurally sound. What the armature requires is:

1. **One new entity type** (PopulationCategory) — larger than E-12 but occupying the same conceptual slot. Define at A7 when population taxonomy is settled, not before.
2. **Schema extensions** on existing entities — each timed to the phase that owns the relevant decision (A6 for evidence fields, A7 for axis and population fields, A8 for jurisdiction fields, A9 for versioning).

The A3 amendment is a documented schema amendment, not a rewrite. It follows the CO-0008 pattern: governance document + Pydantic schema + validator update + converter update. It executes at A7 completion (when the axis set and population taxonomy are finalized), with earlier extensions (A6 evidence fields) executing at A6.

**A3 amendment sequence:**
- A6: add synthesis_method_indicator, inference_basis, search_strategy, screening_counts, quality_assessment to EvidenceSource/BPCMetadata/Specification
- A7: add PopulationCategory entity; add axes_applicable to Specification; add communication axis value "sign language user" to enums; extend PopulationCode enum if needed
- A8: restructure jurisdiction_scope on Specification
- A9: add version_history (already planned as E-19)

Each is a scoped amendment at the phase that owns the decision. No single "reopen A3" event.

---

## 3. Judgment against roadmap critical path

```
A4 ──→ A5 ──→ A6 ─┬──→ A7 ──┐
                 ├──→ A8 ──┼──→ A9 ──→ (A10/A11/A12/A13 parallel) ──→ Stage A done
                 └─────────┘
```

### Does the armature change this sequence?

**No.** The critical path is unchanged. A6 still gates A7/A8/A9. The armature expands the scope of A6, A7, A8, and A12 but doesn't change their ordering or dependencies.

### Phase-by-phase impact

**A4 (Voice — NEXT, 2–3 sessions):** Armature's role layer informs A4 but doesn't change its scope. A4 is about specification language, advocacy framing, "shall be" retirement. The armature's plain-language register spec and role-based content variant decisions are A12 territory, not A4. **Impact: none. A4 proceeds as planned.**

**A5 (Co-1 operational — 2–3 sessions):** Armature §9 (Authority and validation) is directly consistent with D-03 revised. The three-tier validation framework (A/B/C) is an operational detail that A5 can incorporate. **Impact: minor scope addition. A5 documents the validation tier framework alongside the Co-1 operational specification. +0 sessions.**

**A6 (Evidence methodology — 3–5 sessions, CRITICAL GATE):** Armature adds:
- Synthesis method indicator (direct/inferred/consensus) — a new evidence dimension alongside tier and evidence_type
- Inference basis documentation requirement for ○-marked specifications
- PRISMA-aligned search/selection transparency requirements on BPCMetadata/EvidenceSource
- Per-specification evidence assessment documentation
- Schema extensions on EvidenceSource, BPCMetadata, Specification

This is significant scope expansion, but it's the right scope for A6. A6 was already tasked with operationalizing T-04 and T-03. The armature adds the transparency requirements that make the evidence methodology academically defensible. **Impact: +1–2 sessions. A6 becomes 4–7 sessions.**

**A7 (Population taxonomy — 2–3 sessions):** Armature substantially expands A7:
- 18-axis functional axis set with ICF cross-mapping
- PopulationCategory entity type definition (subsumes E-12)
- Mapping confidence classification for all populations
- Clinical sub-classification scaffold fitness assessment
- Population code ↔ PopulationCategory coexistence model
- Diagnosis taxonomy source (plain-language controlled vocabulary)
- Deaf cultural/linguistic identity handling
- Cognitive processing sub-classification
- IntD mapping with THIN-BASE handling
- Communication axis "sign language user"
- Respiratory axis confirmation
- Supplementary Volume body size mechanism
- Reverse-mapping algorithm specification
- Schema: PopulationCategory model + axes_applicable on Specification + enum extensions

This is the largest scope expansion. A7 was always the population taxonomy phase, but the armature makes it the core architectural phase for the query system. **Impact: +3–4 sessions. A7 becomes 5–7 sessions.**

**A8 (Jurisdiction — 2–3 sessions):** Armature adds:
- Structured jurisdiction_scope on Specification (replaces flat list)
- Spatial scope coverage against CRPD Art 30/24/27
- Cultural context notes mechanism
- Jurisdiction comparison feature specification

Some of this was already implicit in A8's scope ("specify what jurisdictional comparability means at parameter level"). The structured jurisdiction_scope and cultural context notes are new. **Impact: +1 session. A8 becomes 3–4 sessions.**

**A9 (Time model — 2–3 sessions):** Armature's version_history requirement aligns with E-19 (Time-Version) already deferred to A9. **Impact: none.**

**A10 (Adversarial-use — 1–2 sessions):** No armature impact.

**A11 (Legal/regulatory — 1–2 sessions):** Armature's CRPD mapping (Universal Mode → Art 9, Tier 2 → Art 5) and methodology statement requirements overlap. Minor scope addition. **Impact: +0–1 sessions.**

**A12 (Decision protocol — 1 session):** Armature adds:
- Role-based delivery mechanism decision
- Carer role specification
- Variable conflation check algorithm
- §3.8 Step 0 UI surfacing
- Capability Approach integration depth
- Plain-language register specification
- Easy Read classification

A12 was scoped as "standardized model-routing notation + per-decision-point rationale capture." The armature makes A12 substantially larger — it becomes the decision protocol phase for all presentation-layer questions. **Impact: +2–3 sessions. A12 becomes 3–4 sessions.**

**A13 (Doctrine recheck — 1 session):** The armature itself should be a doctrine-recheck input. No scope change to A13 phase. **Impact: none.**

### Total Stage A budget impact

| Phase | Original | Revised | Delta |
|---|---|---|---|
| A4 | 2–3 | 2–3 | 0 |
| A5 | 2–3 | 2–3 | 0 |
| A6 | 3–5 | 4–7 | +1–2 |
| A7 | 2–3 | 5–7 | +3–4 |
| A8 | 2–3 | 3–4 | +1 |
| A9 | 2–3 | 2–3 | 0 |
| A10 | 1–2 | 1–2 | 0 |
| A11 | 1–2 | 1–2 | 0 |
| A12 | 1 | 3–4 | +2–3 |
| A13 | 1 | 1 | 0 |
| **Total remaining** | **18–28** | **25–38** | **+7–10** |

Stage A total budget was 22–32 sessions (post-Amendment 7) with ~11–12 consumed. Remaining was 10–20. Revised remaining: 25–38, of which ~11–12 consumed. New Stage A total: **33–50 sessions.**

This is a meaningful increase. However: the armature resolves questions that would have emerged at B3 (Navigation mode specification, 3–4 sessions) and partially at B1 (schema design, 6–9 sessions). Work done in Stage A reduces Stage B scope. Net project impact is smaller than the Stage A delta suggests.

---

## 4. Judgment against Stage B

### B3 (Navigation mode specification — 3–4 sessions)

B3 was scoped to specify 7 navigation modes + Question entity (E-20). The armature pre-decides the query architecture that B3 implements. B3 still has work: the specific navigation modes (information-finding, decision-frame, jurisdiction-comparison, questions-led, etc.) are distinct from the person-profile query architecture. But B3's scope reduces because the foundational architecture (two layers, axis system, scope dimensions, role layer, output schema) is settled.

**Impact: B3 reduces to 1–2 sessions** — specifying navigation modes against the settled architecture rather than designing the architecture.

### B1 (Schema design — 6–9 sessions)

B1 derives storage form from ≥3 candidate forms. The armature doesn't pre-decide storage form. But it constrains the schema: whatever form B1 chooses must support PopulationCategory, axes_applicable, structured jurisdiction_scope, synthesis method indicators, and the full specification output schema. This is helpful constraint, not harmful constraint — B1 works from a more complete requirements set.

**Impact: B1 potentially faster** by 1–2 sessions because requirements are clearer. Net: B1 becomes 5–8 sessions.

### Stage B net

| Phase | Original | Revised | Delta |
|---|---|---|---|
| B1 | 6–9 | 5–8 | -1 |
| B3 | 3–4 | 1–2 | -2 |
| Other B | 18–27 | 18–27 | 0 |
| **Total** | **26–40** | **23–37** | **-3** |

---

## 5. Judgment against website-preparation workplan

The website-preparation workplan (v2.0, 2026-04-17) references "8 entity types · 5 interactive tools · 20 page types · 3 community layers · 4 navigation axes." It was authored pre-CO-0008 and pre-armature.

The roadmap already notes: "reconcile at B7 lock." This is correct. The armature changes entity types (adds PopulationCategory), changes navigation architecture (two-layer + 18 axes + 5 scope dimensions + role layer replaces "4 navigation axes"), and changes output schema (structured specification set with full provenance). The website-preparation workplan's Phase B build spec will need revision.

**Impact: no action now.** The roadmap's "reconcile at B7 lock" instruction covers this. The armature feeds into that reconciliation as a primary input.

---

## 6. Net project budget impact

| Stage | Original | Revised | Delta |
|---|---|---|---|
| Stage A remaining | 10–20 | 14–26 | +4–6 |
| Stage B | 26–40 | 23–37 | -3 |
| Stage C | ~170–260 | ~170–260 | 0 |
| **Net** | | | **+1–3 sessions** |

The armature adds 7–10 sessions to Stage A but removes ~3 from Stage B and produces clearer requirements that may reduce Stage C friction. Net project impact: +1–3 sessions. Within noise for a 220–336 session project.

---

## 7. Integration plan

### Immediate (this session)

1. **File armature v4 as governance pre-decision.** Commit `armature_v4.md` to `governance/` — replacing the existing `governance/pre-decision-multimodal-access-armature.md` (v1). This is the canonical pre-decision document for the query architecture.

2. **File armature v4 resolutions as companion.** Commit `armature_v4_resolutions.md` to `governance/`. This carries the specific resolutions that inform A6, A7, A8, A12.

3. **Update roadmap.** Amend session estimates for A6, A7, A8, A12. Add armature as input document for those phases. Note A3 amendment sequence (scoped extensions at A6/A7/A8, not wholesale reopen).

4. **Update gap register.** Close or annotate any armature-related gaps.

### Phase-specific integration

**A4 (next session):** No change to A4 scope. A4 proceeds with voice and framing. The armature's role-layer content variant specifications are A12 territory. A4 may reference the armature's specification language examples (§4.7 worked example uses tier-appropriate language) as validation targets for the voice guidance.

**A6 (evidence methodology):** Add to A6 scope:
- Define synthesis_method_indicator (direct/inferred/consensus) as a third evidence dimension alongside tier and evidence_type
- Specify inference basis documentation requirement
- Specify PRISMA-aligned search/selection transparency requirements
- Schema extensions: synthesis_method_indicator + inference_basis on Specification, search_strategy + screening_counts + quality_assessment on EvidenceSource, synthesis_method + quality_summary on BPCMetadata
- Reconcile with T-04 state machine: map ●/○ to stated/provisional/pending

**A7 (population taxonomy):** Add to A7 scope:
- 18-axis functional axis set (resolved in resolutions Q7) — validate via Opus synthesis against published clinical literature on diagnosis-function relationships
- PopulationCategory entity type definition (resolved in resolutions Q2) — Pydantic schema + converter + validator
- Mapping confidence classification for all populations (resolved in resolutions Q12) — validate classifications
- Clinical sub-classification scaffold fitness assessment (resolved in resolutions Q14)
- Population code ↔ PopulationCategory coexistence model (resolved in Q10)
- Diagnosis taxonomy source: plain-language controlled vocabulary with clinical cross-references (resolved in Q11)
- Deaf cultural/linguistic identity: population category + communication axis value (resolved in Q9)
- Cognitive processing sub-classification structure (resolved in Q8)
- IntD mapping with THIN-BASE handling (resolved in Q17)
- Reverse-mapping algorithm specification (resolved in Q4)
- Supplementary Volume body size scope modifier (resolved in Q15)
- Respiratory axis confirmation (resolved in Q16)
- Intersectional identity scope modifiers — age, gender (resolved in Q19)
- Easy Read as content-format flag (resolved in Q18)
- Schema: PopulationCategory.py, axes_applicable on Specification, FunctionalAxis enum, MappingConfidence enum, communication axis enum extension
- Validators: validate_population.py (expand from original A7 scope)

**A8 (jurisdiction):** Add to A8 scope:
- Structured jurisdiction_scope on Specification (resolved in Q20) — schema extension replacing flat list
- Spatial scope category list against CRPD coverage (resolved in Q21)
- Cultural context notes mechanism (resolved in Q29)
- Jurisdiction comparison feature specification

**A11 (legal/regulatory):** Add:
- CRPD Universal Mode/1/2 mapping to Art 9 / Art 5 (resolved in armature v4 §7.3) — document in legal framework
- Methodology statement template including authority disclosure (resolved in armature v4 §9)

**A12 (decision protocol):** Add to A12 scope:
- Role-based delivery mechanism: filter+emphasis for designer/OT/policymaker; authored content variant for disabled person/carer (resolved in Q25)
- Carer role specification: distinct role with care-context framing (resolved in Q26)
- Variable conflation check algorithm: three-step check (resolved in Q27)
- §3.8 Step 0 UI surfacing: inline annotation + summary banner (resolved in Q28)
- Capability Approach integration depth: specification-only with honest limitation (resolved in Q30)
- Plain-language register specification: ISO 24495-1 governed, authored per category-topic combination (resolved in Q31)
- Easy Read as separate content format (resolved in Q18)

**B3 (navigation mode):** Receives armature v4 as primary architectural input. B3 scope narrows to specifying navigation modes (information-finding, decision-frame, jurisdiction-comparison, questions-led, etc.) against the settled two-layer architecture. Question entity (E-20) still defined at B3.

### Schema amendment tracking

Create `workplan/a3-amendment-register.md` to track scoped schema extensions across phases:

| Amendment | Phase | Entity | Fields added | Status |
|---|---|---|---|---|
| A3-AM-01 | A6 | Specification | synthesis_method_indicator, inference_basis | Pending A6 |
| A3-AM-02 | A6 | EvidenceSource | search_strategy, screening_counts, quality_assessment | Pending A6 |
| A3-AM-03 | A6 | BPCMetadata | synthesis_method, quality_summary, last_review_date, review_cycle | Pending A6 |
| A3-AM-04 | A7 | NEW: PopulationCategory | Full entity (see Q2 resolution) | Pending A7 |
| A3-AM-05 | A7 | Specification | axes_applicable | Pending A7 |
| A3-AM-06 | A7 | Specification | tier2_handoff (structured, replacing person_specific_note) | Pending A7 |
| A3-AM-07 | A7 | Specification | adjustability_metadata | Pending A7 |
| A3-AM-08 | A7 | enums.py | FunctionalAxis enum, MappingConfidence enum, CommunicationMode (add sign_language_user) | Pending A7 |
| A3-AM-09 | A8 | Specification | jurisdiction_scope (structured, replacing flat lists) | Pending A8 |
| A3-AM-10 | A8 | Specification | cultural_context | Pending A8 |
| A3-AM-11 | A9 | All mutable entities | version_history (per E-19 already planned) | Pending A9 |
| A3-AM-12 | A7/A12 | Specification | physical_variable (for variable conflation check) | Pending |
| A3-AM-13 | TBD | Gap | user_facing, population_level, surfacing_method | Pending |

### Effort guide updates

| Skill/Phase | Current effort | Revised | Rationale |
|---|---|---|---|
| A7 (population taxonomy) | Not listed (default 100) | 150 | Now includes best-practice synthesis for axis set, mapping confidence, clinical scaffold fitness. Opus-level judgment across populations and clinical literature. |
| A12 (decision protocol) | Not listed (default 100) | 125 | Now includes role-based delivery mechanism, variable conflation algorithm, plain-language register specification. Heavy multi-source judgment. |
| A6 (evidence methodology) | Not listed as a whole (A6 sub-skills at 150) | 150 for the whole phase | Synthesis method indicator design requires cross-referential evidence methodology judgment. |

---

## 8. Risk assessment

**Risk 1: A7 scope expansion delays critical path.** A7 is on the critical path (A6 → A7 → A9 → ...). Expanding A7 from 2–3 to 5–7 sessions delays everything downstream. **Mitigation:** A7 can be split into A7a (population taxonomy + PopulationCategory entity + enum extensions, 2–3 sessions) and A7b (axis set + mapping confidence + sub-classification scaffolds + reverse-mapping algorithm, 3–4 sessions). A7a gates schema work; A7b can run after A7a without blocking A9.

**Risk 2: A12 expansion adds late-stage work.** A12 was scoped as 1 session. Now 3–4. But A12 is parallelizable with A10/A11/A13 — it's not on the critical path between A9 and Stage A done. **Mitigation:** none needed; A12's expansion doesn't affect the critical path.

**Risk 3: 37 resolutions are Opus-level determinations made without PWLE/DPO input.** All population-specific decisions (mapping confidence classifications, axis names, sub-classification scaffolds, Deaf identity handling) require the three-tier validation framework. Pre-launch, they are Tier A (published literature) only. **Mitigation:** every population-specific resolution carries a validation provenance record. A7 documents each as Tier A validated. Post-launch consultation (Tier B/C) may revise.

**Risk 4: armature v4 + resolutions represent substantial pre-decision work that could be overturned at A7.** The pre-decision status is clear in the document. A7 (Opus-level, effort 150) reviews and may revise. The resolutions are the best available determination given current evidence; A7 may change them. This is the intended workflow — pre-decision drafting followed by formal phase work. **Mitigation:** inherent in the process.

---

## 9. Commit plan

### Files to commit

| File | Destination | Action |
|---|---|---|
| armature_v4.md | governance/armature_v4.md | New file. The canonical pre-decision query architecture document. |
| armature_v4_resolutions.md | governance/armature_v4_resolutions.md | New file. Companion resolutions document. |
| armature_v3_review.md | governance/armature_v3_review.md | New file. Tri-lens review (CRPD, UI/UX, usability). Retained as audit trail for the ethical review that shaped v4. |
| governance/pre-decision-multimodal-access-armature.md | Unchanged | Retain v1 as audit trail. v4 does not overwrite — it supersedes. |

### Roadmap amendment

Amend `workplan/roadmap-2026-04-27.md` §4 phase descriptions with revised session estimates and armature input references for A6, A7, A8, A12. Note A3 amendment sequence. Note B3 scope narrowing.

### Gap register

No new gaps from armature work. Existing OPEN P1s (GAP-079, GAP-CITE-01) unaffected.

### Session file

Update session with armature v4 work completed, resolutions produced, integration plan committed. Next action: A4 (Voice) — unchanged.
