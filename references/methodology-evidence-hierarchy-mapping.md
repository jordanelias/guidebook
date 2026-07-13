# Methodology: Evidence Hierarchy Mapping and Recommendation Strength Protocol (v2)

**Created:** 2026-04-08 23:05 UTC (v1, Opus 4.6, CO-0006 Phase 1A)
**Revised:** 2026-07-12 (v2 — reconciliation to the canonical ladder)
**Status:** v2 executes the owner directive of 2026-05-25 ("t2>t3 this is enshrined", closing GAP-273/GAP-296) and `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md`. Both DR-2026-05-29 and `decisions/DR-2026-07-12-tier3-stated-threshold.md` flagged v1 of this file as the HIGH-priority unreconciled caller still arguing the superseded ladder; v2 is that reconciliation.
**Governs:** the external-framework correspondence (GRADE / JBI / SIGN) and the Co-1 co-primacy justification. The ladder itself is governed by `governance/tier-system.md`; the state machine by `governance/evidence-methodology.md` §2; the directness layer by `governance/evidence-methodology.md` §1.7 + `schemas/directness.py`; the unified statement is `governance/evidence-architecture.md` (PROPOSED).

## Supersession notice (v1 → v2)

v1 (2026-04-08, DRAFT, never lead-reviewed) placed systematic reviews/meta-analyses at Tier 3 — below Tier 1/Co-1 — and argued the hierarchy "inverts the conventional placement." That placement and argument are **superseded**: the owner directive of 2026-05-25 enshrined synthesis above lower-control primary work (sr_meta at Tier 2), formalized in `governance/tier-system.md` §2 and DR-2026-05-29, with the four affected rows migrated by `scripts/migrations/data_20260525070000_sr_meta_t2_canonicalization.sql`. v1's indirectness argument survives in corrected form: what it tried to do with tier *placement* (account for domain-transfer indirectness) is now done by the **directness conditioning layer** — grain-matching per source per claim (`evidence-methodology.md` §1.7) — which is the methodologically correct home for GRADE's indirectness principle. Tier placement answers "what kind of claim can this source anchor"; directness answers "how well does this particular source's grain match this particular claim." v1 conflated the two.

---

## 1. Purpose

This document establishes the formal relationship between the project's seven-tier evidence hierarchy and three established health-evidence grading frameworks: GRADE, JBI, and SIGN. It serves three functions:

1. **Transparency.** External reviewers can see how the project's evidence tiers correspond to — and deliberately depart from — frameworks they already know.
2. **Justification.** The placement of lived experience (Co-1) as co-primary with primary research (Tier 1) is a deliberate, argued methodological decision (§6), not an oversight.
3. **Operational protocol.** How evidence tiers translate into the specification markers (● / ◐ / ○) and the four-state determination machine (§7).

## 2. The project evidence hierarchy (canonical, per `governance/tier-system.md`)

| Tier | Label | Description |
|---|---|---|
| Tier 1 | Primary research, high control | Intervention-level or biomechanical control on the parameter under design; OT-prioritized, not OT-exclusive (decision D-E) |
| **Co-1** | **Lived experience / participatory design** | Disability-led lived-experience publications; DPO research; CRPD Art. 4.3 consultation outputs. **Co-primary with Tier 1** — non-substitutable on different claim types |
| Tier 2 | Synthesis | Two streams: (a) systematic reviews / meta-analyses (`sr_meta`); (b) named-organisation evidence-based standards — DPO and professional-body guidance (`standard_eb`) |
| Co-2 | OT professional body CPGs | CAOT, AOTA, RCOT, COTEC, WFOT and national equivalents. Co-primary with Tier 2 |
| Tier 3 | Primary research, lower control | Cross-sectional, observational, qualitative, single-centre clinical research; grey-literature primary research. Supporting evidence — "rarely the sole basis" |
| Tier 4 | International standards | ISO, IEC, CEN, EN — evidence-based international instruments |
| Tier 5 | National beyond-code frameworks | BS 8300, DIN 18040 guidance strata, national CPGs scoped to the built environment |
| Tier 6 | Statutory codes | Legally enforceable accessibility codes. **Code-baseline citations only** — the regulatory floor, never a best-practice anchor |

**Key structural features (v2):**

- **Synthesis sits above lower-control primary work.** When a claim cites both an SR and a primary study the SR weighed, the SR is the warrant-source and must rank above its inputs (`tier-system.md` §2). This matches GRADE's synthesis-above-primary principle rather than inverting it.
- **Co-1 and Co-2 are intercalated co-primary tracks,** not appendices — encoded as `tier: 1, evidence_type: co1` and `tier: 2, evidence_type: co2` (T-03 two-field encoding).
- **Tiers 4–6 are the regulatory stratum,** walled off from best-practice anchoring: convergence of standards/codes is convergence-not-evidence (`tier-system.md` §3). A T4/T5 source can support a best-practice claim only where its own evidence basis is documented as traceable to T1/T2 (re-graining rule, `governance/evidence-architecture.md` §4 G1, PROPOSED).
- **Indirectness is handled per-source, per-claim** by the directness conditioning layer (grain-matching, bidirectional, categorical: DIRECT / DOWN-WEIGHTED / DISCOUNTED / NON-ANCHORING) — not by tier placement and not by a blanket downgrade.

## 3. Mapping to GRADE

### 3.1 GRADE overview

GRADE assesses the quality of a body of evidence for a specific question, rating quality High/Moderate/Low/Very Low from study design plus five downgrading factors (risk of bias, inconsistency, **indirectness**, imprecision, publication bias) and three upgrading factors, and classifies recommendations Strong/Conditional.

### 3.2 Correspondence table (v2 placements)

| Project tier | GRADE starting quality | Typical GRADE outcome | Notes |
|---|---|---|---|
| Tier 1 (RCT / high-control) | High (RCT) or Low (quasi-experimental) | Moderate to Low | Domain-transfer indirectness and small samples downgrade most entries; the project records this per source via the directness layer instead |
| Co-1 | Not classifiable | Not classifiable | GRADE has no category for experiential evidence; GRADE-CERQual (§3.3) is the nearest extension |
| Tier 2 — sr_meta | High (SR of RCTs) to Low (SR of observational) | Moderate to Very Low | Direct correspondence at the top of GRADE's own ladder — consistent with the v2 placement of synthesis at Tier 2 |
| Tier 2 — standard_eb (named-org evidence-based standards) | Very Low (expert opinion) | Very Low | The sharpest deliberate departure: GRADE reads organisational guidance as opinion; the project reads *evidence-based* DPO/professional-body standards as synthesis (§2 homology argument) with the evidence-basis requirement doing the quality-gating |
| Co-2 | Not classifiable (consensus guidance = expert opinion; ≈ Very Low) | ≈ Very Low | GRADE does not grade CPGs as an evidence class; consensus guidance without a systematic evidence review is expert opinion — the same reading GRADE gives the standard_eb row above (v1's "starts Low" overstated it, and disagreed with the standard_eb row for the same epistemic move) |
| Tier 3 (lower-control clinical / grey) | Low | Low to Very Low | Matches GRADE's placement of observational designs |
| Tiers 4–6 | Not classifiable | Not classifiable | GRADE does not rate consensus standards; the project classifies them explicitly — as a regulatory stratum, not as best-practice evidence |

### 3.3 GRADE-CERQual and Co-1

CERQual extends GRADE to qualitative evidence synthesis (methodological limitations, coherence, adequacy, relevance). It is the closest established framework to Co-1 appraisal but applies to qualitative *reviews*; most Co-1 evidence is individual-level. CERQual therefore supplies appraisal principles (§6.3) without directly classifying Co-1.

### 3.4 Why GRADE is insufficient for this project — and what is adopted from it

1. **Indirectness.** Nearly all clinical evidence for built-environment specification involves domain transfer; applied as GRADE's blanket downgrade it would flatten the whole evidence base to Low/Very Low, erasing real quality distinctions. **v2 position:** GRADE's indirectness *principle* is adopted, but implemented as bidirectional grain-matching per source per claim (`evidence-methodology.md` §1.7, `schemas/directness.py`) — an aggregate SR is strongest for a population-grain claim and down-weighted for a person-grain claim, and vice versa for direct intervention studies — rather than as a hierarchy-level penalty. This is the corrected form of v1's motivation for inverting the ladder.
2. **Qualitative exclusion.** GRADE's core framework excludes qualitative evidence. In a domain where the person using the space is a primary authority on whether it works, excluding their testimony is methodologically incoherent (§6).
3. **Standards gap.** GRADE has no mechanism for standards/codes, which form a large fraction of the operative corpus here. The project classifies them explicitly — and then *restricts* them (regulatory stratum), which GRADE cannot express.

**Adopted from GRADE:** risk-of-bias and imprecision appraisal within Tiers 1–3; the synthesis-above-primary principle; the directness principle (as a conditioning layer). **Not adopted:** GRADE's level labels and Strong/Conditional grades as governing classifications.

## 4. Mapping to JBI

### 4.1 Overview

JBI maintains separate hierarchies per question type (effectiveness, meaningfulness/qualitative, etc.) — structurally the closest framework to the project's parallel-stream model.

### 4.2 Correspondence — JBI Effectiveness (v2 placements)

| Project tier | JBI effectiveness level | Notes |
|---|---|---|
| Tier 2 — sr_meta (SR of RCTs) | Level 1.a | Direct correspondence — synthesis at the top of both ladders |
| Tier 2 — sr_meta (SR of other designs) | Level 1.b (SR of quasi-experimental/other) | An SR stays a Level-1 synthesis entry; 1.c is an individual RCT, not an SR level |
| Tier 1 (RCT / pseudo-randomised) | Level 1.c–1.d | True RCTs of built-environment interventions are rare |
| Tier 1 (quasi-experimental) | Level 2.d | Pre/post single-group designs typical of home-modification studies |
| Tier 3 (lower-control clinical) | Level 3–4 | Observational/descriptive designs |
| Co-2 | Level 5 (expert opinion) | JBI classifies CPGs without systematic evidence review as expert opinion |
| Tiers 4–6 | Not classified | JBI does not rate standards or codes |

### 4.3 Correspondence — JBI Meaningfulness (qualitative)

| Project stratum | JBI meaningfulness level | Notes |
|---|---|---|
| Co-1 (qualitative meta-synthesis) | Level 1 (SR of qualitative studies) | Rare in the current corpus |
| Co-1 (mixed-methods/qualitative synthesis short of full SR) | Level 2 (synthesis of qualitative findings) | JBI Level 2 is a *synthesis* level, not a single-study level |
| Co-1 (individual participatory/phenomenological study; `co1_source_type: peer_reviewed_literature`, `dpo_research`) | Level 3 (single qualitative study) | The modal Co-1 entry — corrected from v1, which placed single studies at Level 2 |
| Co-1 (testimony/report; `academic_narrative`, `advocacy_position`) | Level 3–4 (single descriptive study / expert opinion) | CRPD shadow reports, DPO submissions — note these carry different *grain* (G3, `evidence-architecture.md` §4): organisational positions are population-grain, narratives individual-grain |
| Tier 2 — standard_eb without primary basis | Level 4 | Named-org guidance whose evidence basis is not documented |

### 4.4 Why JBI is the closest framework

Qualitative evidence has its own hierarchy; participatory action research is explicitly included (Level 2 meaningfulness); ConQual provides structured appraisal applicable to Co-1. **Adopted:** JBI meaningfulness as the Co-1 appraisal frame; JBI effectiveness levels to inform Tier 1/2/3 classification. **Not adopted:** JBI A/B recommendation grading.

## 5. Mapping to SIGN

### 5.1 Correspondence table (v2 placements)

| Project tier | SIGN level | SIGN grade (if sole evidence) |
|---|---|---|
| Tier 2 — sr_meta (SR of RCTs, high quality) | 1++ | A |
| Tier 2 — sr_meta (SR of observational) | 2++ | B |
| Tier 1 (RCT, low bias) | 1+ | B |
| Tier 1 (quasi-experimental) | 2+ | C |
| Co-1 | 3–4 | D or GPP |
| Tier 2 — standard_eb / Co-2 | 4 | D |
| Tier 3 | 2− to 3 | D (2− evidence cannot ground Grade C; 2+ would) |
| Tiers 4–6 | Not classified | — |

### 5.2 SIGN Good Practice Points and the ○ marker

SIGN's GPP maps to the project's ○ stratum (thin base / expert consensus / unconfirmed). The project's gap-disclosure obligation on ○ exceeds SIGN's GPP transparency requirement.

### 5.3 Why SIGN is insufficient

SIGN places lived experience at Level 3–4 → Grade D. A specification supported by robust, convergent Co-1 evidence carries higher confidence in this domain than Grade D implies; SIGN's linear hierarchy cannot express the parallel-stream model. **Adopted:** GPP → ○ correspondence; SIGN levels as secondary discrimination within Tiers 1–3. **Not adopted:** SIGN recommendation grades.

## 6. Co-1 justification

### 6.1 Statement

Lived-experience evidence (Co-1) is co-primary with Tier 1 primary research. A determination grounded solely in strong, verified Co-1 evidence is a legitimate evidence-based claim (`stated`), not a provisional one (`evidence-methodology.md` §2.2).

### 6.2 Argument

**6.2.1 Treaty obligation.** CRPD Art. 4.3 requires close consultation with and active involvement of persons with disabilities; Arts. 9 and 19 apply this to the built environment. A methodology that subordinates disabled people's testimony about their own environments to clinical studies conducted on their behalf violates the participatory principle the treaty embeds.

**6.2.2 Epistemic authority.** The person who uses a space daily has knowledge of its functional adequacy that laboratory study structurally cannot replicate — ecological validity across fatigue variation, pain fluctuation, cumulative environmental stressors.

**6.2.3 Feasibility constraint.** RCTs of built environments face structural (not methodological) barriers: buildings cannot be randomised, occupants cannot be blinded, meaningful outcomes span years, and ethics forbids assigning people to barrier-creating environments. A hierarchy treating SR-of-large-RCTs as the gold standard is structurally empty at the top for this domain.

**6.2.4 JBI precedent.** JBI recognises qualitative evidence as a separate stream with its own levels; the project extends the principle by placing the streams side by side. This is a position statement about *this domain*, not a generic claim that qualitative always equals quantitative.

**6.2.5 Social model alignment.** If the disabling factor is environmental, the person experiencing the barrier is the primary witness. Clinical evidence identifies physiological parameters; lived experience identifies whether specification values actually remove the barrier. Both necessary; neither sufficient; co-primacy reflects it.

### 6.3 Quality appraisal for Co-1

Co-1 is not exempt from appraisal. Criteria adapted from ConQual/CERQual: credibility (direct experience), dependability (documented methodology), confirmability (independent convergence), transferability (barrier attributable to physical features), adequacy (pattern, not anecdote). Operationally enforced via `governance/co1-operational.md` required fields (`co1_provenance`, `co1_source_type`, `verification_status`); Co-1 counts toward `stated` only when VERIFIED (`evidence-methodology.md` §2.2).

### 6.4 Boundary conditions

Co-1 is co-primary for specification *direction* and *barrier identification*; it is not co-primary for dimensional *values*, which require T1/T2/T3 evidence (or regulatory citation for the code minimum). This boundary is now mechanically expressed twice: by value-directness (a Co-1 source without value-level content grades NOT-FOUND on the value dimension) and by grain (G3: population-grain Co-1 — DPO positions — anchors Population-Mode claims and never overrides an individual's assessed position at Person Mode; `governance/co1-operational.md`).

## 7. Recommendation strength protocol (v2)

### 7.1 Markers — the ●/◐/○ system (canonical per `tier-system.md` §5)

| Marker | Meaning | Strata |
|---|---|---|
| ● | Confirmed evidence base | T1, T2 (sr_meta + standard_eb + co2 streams), T3-clinical, Co-1, Co-2 |
| ◐ | Policy/standards basis only — not primary evidence | T4, T5 |
| ○ | Grey, expert consensus, thin base, unconfirmed | T3-grey, `[EXPERT CONSENSUS]`, `[THIN BASE]`, `[UNSUPPORTED]`, T6 |

v1's two-marker system is superseded: it allowed "Tier 4–6 only → ●" with the rationale that "code compliance is inherently evidence-based (the evidence being the code itself)." That rationale is the convergence-laundering failure mode `tier-system.md` §3 names, in its oldest recorded form. Under v2, a T4–6-only basis renders ◐/○ and — per the PROPOSED `governance/evidence-architecture.md` G1 (pending owner ratification) — would be flagged `regulatory_stratum_only` in the determination table and carry the regulatory-stratum register language in every audience rendering, never best-practice language (invariant I3).

Two v1 rules survive unchanged and are restated so they are not lost in the marker-system supersession: **an unmarked specification is an error** — every specification sentence carries a marker; and for quantitative specifications, a confirmed marker requires at least one source that provides or permits derivation of the stated **value**, not only the specification direction (v1 §7.2; the direction/value boundary is §6.4).

### 7.2 The four-state determination machine

Markers annotate sources; determinations live in `evidence_cell_state` (`stated` / `provisional` / `pending` / `not_applicable`, `evidence-methodology.md` §2), produced by a pure, versioned assessment function with mandatory `governing_refs` (anti-hallucination) and a falsification condition per determination. Tier-3-alone does not reach `stated` (`decisions/DR-2026-07-12-tier3-stated-threshold.md`, PROPOSED): T3-clinical-alone ⇒ `provisional`; T3-grey-alone ⇒ `pending`.

### 7.3 Recommendation strength ↔ design mode

The RecommendationStrength enum reconciles with the design scales (`schemas/directness.py` SCALE_FROM_RECOMMENDATION): STRONG_UNIVERSAL ↔ Universal Mode (code floor; mandatory), CONDITIONAL_POPULATION ↔ Population Mode (median + range), CONDITIONAL ↔ Person Mode (OT co-design resolves within the range). This triplet — not a Strong/Conditional grade on each specification — carries the gradation work in this project, because a building element is either specified or not, and case-by-case weighing happens at Person Mode, not in the population specification.

## 8. Cross-framework summary

| Feature | GRADE | JBI | SIGN | This project |
|---|---|---|---|---|
| Qualitative stream | CERQual (synthesis only) | Meaningfulness hierarchy | Not addressed | Co-1, co-primary, integrated |
| Standards/codes | Not addressed | Not addressed | Not addressed | Explicit regulatory stratum (T4–6), walled off from best-practice anchoring |
| Synthesis placement | Top | Top (Level 1) | Top (1++) | Top of the non-co-primary ladder (Tier 2) — v2 alignment |
| Recommendation grades | Strong/Conditional | A/B | A–D/GPP | ●/◐/○ + four-state machine + design-mode triplet |
| Indirectness | Blanket downgrading factor | Implicit | Implicit | Bidirectional grain-matching per source per claim (categorical conditioning layer) |
| Lived experience | Patient values (outside evidence quality) | Meaningfulness Level 2–3 | Level 3–4 | Co-primary with Tier 1 |

## 9. Operational implications

- **multilingual-research / research-log-manager:** record the project tier AND nearest JBI equivalent (`Tier 2 [JBI Eff. 1.a]`, `Co-1 [JBI Mean. 2]`) so external reviewers can locate each source in a recognised framework.
- **item-specification-writer / evidence-auditor:** marker assignment per §7.1; flag any ● resting only on T4–6 (that combination is no longer expressible — it is ◐/○ + `regulatory_stratum_only`).
- **Synthesis passes:** classify confidence via the determination tuple; where T1 and Co-1 both anchor, record axis co-presence and treat value-level convergence as an assessment output (never an assumption; cf. `pending_assessment` status).

## 10. Limitations and future development

Carried forward from v1 (still true): §6.3 criteria are adapted principles, not a validated instrument; ●/◐/○ inter-rater reliability untested; T4 evidence-basis verification varies by standards body (the G1 re-graining rule now gives this a mechanical home: GRAIN_AGGREGATE only with documented T1/T2 traceability); and v1's proposed **○/◌ split** — distinguishing "not studied" from "studied, inconclusive" — remains a live, unresolved idea aligned with the Altman & Bland doctrine (the four-state machine's `pending` covers the first case; the second currently has no distinct surface and deserves one — carried forward as an open item, not silently dropped). New in v2: the `evidence_population_match` (27 rows / 26 of 640 sources) and `source_value_extractions` (0 rows) coverage gaps mean the directness layer currently runs mostly on NOT_ASSESSED inputs, capped conservatively (G2) — the honest posture until assessment coverage grows.

## Amendment register

| Date | Amendment | Author |
|---|---|---|
| 2026-04-08 | Initial draft (v1) | Opus 4.6 — CO-0006 Phase 1A |
| 2026-07-12 | v2: reconciled to the canonical ladder per owner directive 2026-05-25 + DR-2026-05-29 (sr_meta → T2; T3 = lower-control primary; regulatory stratum walled off); two-marker system → ●/◐/○ + four-state machine; v1 §7.3 "Tier 4–6 only → ●" corrected (convergence-laundering); indirectness moved from tier placement to the directness conditioning layer; GRADE/JBI/SIGN tables re-derived for the new placements; Co-1 justification retained and strengthened with operational enforcement pointers | Claude — evidence-architecture unification session |
