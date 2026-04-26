# Mission and Epistemic Commitments
**Status:** CANONICAL — locked at iter 4 cross-test pass (2026-04-26 05:29). Supersedes `governance/mission-PROVISIONAL.md`.
**Created:** 2026-04-26 04:05 UTC
**Phase:** A1-A2 CANONICAL (iter 4 cross-test pass 2026-04-26 05:29)
**Canonical version of:** `governance/mission-PROVISIONAL.md` (revised 2026-04-26 03:45)
**Companion deliverable:** `governance/audience-priority.md` (iter 1; iter 2 deltas captured this session)
**Operative frame:** Pre-launch solo authorship; partial CRPD Art. 4.3 honoring at evidence level
**Citation status:** Iter 3 citation gaps CLOSED (2026-04-25). All `[cite — iter 3]` flags resolved with DOI-verified sources.

---

## Purpose

The Guidebook for Accessible Built Environments equips designers, disabled people, occupational therapists, and policymakers with the questions they need to ask about how to design for accessibility depending on the circumstance.

It is not a prescription manual. It does not dictate values. It does not substitute for professional judgment. It is a thinking tool.

When someone knows better, they do better. The guidebook aims to raise the floor of understanding for everyone who touches the built environment.

---

## Audience commitments

Audience priority is specified in `governance/audience-priority.md`. Summary:

- **Primary audiences** (production-use endpoints): designers and disabled people, with two use-patterns each (information-finding / decision-frame; information-finding / representation-checking).
- **Secondary audiences** (intermediaries): occupational therapists and policymakers, with two use-patterns each (clinical-collaboration / specialist-handoff; jurisdiction-comparison / rationale).
- **Audiences by extension** (students, researchers, facility managers, builders, inspectors): served through one of the four core use-pattern paths; no dedicated content.

Conflict-resolution rules and content production implications are in the audience-priority document. This mission cross-references those rules; it does not duplicate them.

The mission's claim on audience commitments is operational, not honorific: when content choices privilege one audience's reading flow, the audience-priority structure governs. The four named audiences appear in the Purpose statement above in the same order they are named in the doctrinal commitments below — the order is alphabetical-by-role within audiences-of-the-guidebook, not a priority claim.

---

## Doctrinal commitments

### 1. Specifications serve questions; questions serve people; people are not uniform

Every parameter exposes its within-population variability. Population codes are organizing scaffolding, not a description of any individual within the population. Within-population variation is shown as a first-class data dimension, not buried in narrative caveats. Co-occurring conditions are the norm, not the exception.

### 2. Best practice is determined by the evidence hierarchy, not by code consensus

Tier 1 OT-intervention clinical research, Co-1 lived experience, Co-2 OT CPGs, and Tier 3 systematic reviews establish best practice. Tier 6 codes are the compliance floor, not the aspiration. **A best-practice claim derived solely from code consensus is in error.**

The seven-tier hierarchy is operative throughout the guidebook; full schema is specified under §Epistemic commitments §Evidence hierarchy below.

### 3. Co-1 evidence is co-primary with Tier 1

Co-1 evidence — lived experience and participatory design (CRPD Art. 4.3) — is not subordinate to clinical research. The two answer different questions. Where they converge, the convergence is itself evidence. Where they diverge, the divergence is documented and a synthesis approach is specified per parameter (per evidence-state machine in §Epistemic commitments).

This is a commitment about evidence types, not about operations. The project's pre-launch solo operational reality is specified separately in §Operational reality.

### 4. Three-Tier Design Hierarchy operationalizes the doctrine

| Tier | Function | Resolution |
|---|---|---|
| Tier 0 | Universal Design / Code Compliance | Population-agnostic; fixed values |
| Tier 1 | Population-Informed Inclusive Design | Ranges; median as default |
| Tier 2 | Person-Specific Co-Design | OT assessment resolves position within Tier 1 range |

DAR (Design for Adaptable Readiness) provisions are mandatory at all tiers — the structural and electrical infrastructure that allows Tier 2 individual adaptation post-construction without major retrofit cost.

### 5. Universal design is co-extensive with code compliance — the floor, not an aspiration

Inclusive design is the positive aspiration. Tier 0 is the compliance baseline. Best practice exceeds Tier 0 wherever evidence supports.

### 6. Questions-led teaching is the project's pedagogical commitment

The guidebook organizes around questions readers should ask, not around answers they should adopt. **Questions are first-class data, not annotations.** Navigation modes include a questions-led entry surface (per audit v2 §T-02 / D-01 resolution; B3 specifies the navigation mode).

This commitment has both a doctrinal and an epistemic character. As doctrine: the project chooses questions-led structure as its pedagogical stance. As epistemic claim: the project hypothesizes that questions-led resources improve designer outcomes more than prescriptive ones. The doctrinal stance is held; the epistemic claim is tested. See §Epistemic commitments §Questions-led teaching as testable hypothesis.

### 7. The guidebook teaches professional judgment, it does not substitute for it

Population-level specifications (Tier 0 and Tier 1) are necessary but insufficient. Tier 2 person-specific co-design with an occupational therapist resolves the individual case. The guidebook equips professionals to ask better questions; it does not pretend to deliver final answers.

---

## Epistemic commitments

The guidebook's epistemic commitments specify *how the project knows what it claims to know* — the evidence types it draws on, the states it permits its claims to occupy, and the limits it declares about its own production.

### Evidence hierarchy (seven tiers)

| Position | Type | Source examples |
|---|---|---|
| Tier 1 | OT intervention-tested clinical research | RCTs, intervention trials |
| **Co-1** | **Lived experience / participatory design (CRPD Art. 4.3)** — co-primary with Tier 1 | DPO research, peer-reviewed lived-experience literature, named advocacy organizational positions, Co-1-authored academic narratives |
| Tier 2 | NGO / DPO / advocacy guidelines | LPA, RNID, HLAA, IDA, Habinteg |
| **Co-2** | **OT professional body CPGs** — parallel to Tier 2 | CAOT, AOTA, RCOT, COTEC, WFOT |
| Tier 3 | Systematic reviews and meta-analyses | Cochrane, JBI, narrative SRs |
| Tier 4 | International standards (evidence-based) | ISO 21542, ISO 23599, IEC 60118-4, EN 17210 |
| Tier 5 | National beyond-code frameworks | BS 8300-2 Annex G, NL WMO-keuken, RCOTSS-Housing OT |
| Tier 6 | Statutory codes | Reference baseline only |

Schema encodes both `tier` (1–6) and `evidence_type` (`clinical`, `co1`, `co2`, `sr_meta`, `standard_evidence_based`, `national_framework`, `code`) per Stage 0.5 Decision T-03. Co-primary Co-1 records carry `tier: 1, evidence_type: co1`; Co-2 records carry `tier: 2, evidence_type: co2`. The encoding preserves co-primary parallelism without flattening it into a single tier.

### Evidence-state machine for best-practice claims

Each (parameter × population) cell holds one of four states (per Stage 0.5 Decision T-04):

| State | Display | Meaning | Validator behavior |
|---|---|---|---|
| `stated` | normal | Best practice derived from ≥Tier 3 OR Co-1 OR Co-2 evidence | Schema-validated; passes evidence-tier-validator |
| `provisional` | flagged with confidence | Synthesis based on partial evidence dimension; rich in at least one dimension | Schema-validated; renders with confidence flag |
| `pending` | `[BEST-PRACTICE-PENDING]` + gap link | Evidence sparse across all dimensions | Validator requires gap-register entry |
| `not_applicable` | "Not applicable" | Parameter has no design implication for this population | Validator requires explicit rationale |

**Silence on evidence-thin populations is not the default.** The Cochrane yardstick distinguishing absence-of-evidence from evidence-of-absence from primary-non-clinical-tier evidence is honored at the cell level (Altman & Bland, 1995, DOI: 10.1136/bmj.311.7003.485; operationalized in Higgins et al., 2024, Cochrane Handbook v6.5, DOI: 10.1002/9781119536604).

### Questions-led teaching as testable hypothesis

The questions-led pedagogical commitment (Doctrinal commitment 6) is informed by inquiry-based learning, scaffolded questioning in design education, and problem-based learning in professional formation (Schön, 1983, DOI: 10.4324/9781315237473; Hmelo-Silver, 2004, DOI: 10.1023/B:EDPR.0000034022.16470.f3; Royeen, 1995, DOI: 10.5014/ajot.49.4.338). The hypothesis is that questions-led resources improve designer outcomes more than prescriptive ones.

The hypothesis is the project's distinctive epistemic claim. It is acknowledged as a claim, not asserted as established. Empirical testing is staged in B6 pilot validation; per Amendment 7 in `workplan/workplan-co0007-v3-amendments.md`, B6 pilot validation pre-launch is solo-author cross-checking against committed mission language, which is weaker rigor than external testing would provide. This methodological limit is declared, not papered over.

### Treatment of evidence convergence and divergence

Where Tier 1 clinical evidence and Co-1 lived experience converge on a parameter, the convergence is documented as strengthening the claim — neither dimension subsumes the other.

Where they diverge, the divergence is itself evidence about how the parameter operates differently in clinical assessment versus lived use. The synthesis specifies which dimension governs the best-practice claim and on what reasoning, with the divergence visible to the reader. A synthesis that suppresses divergence is in error.

### Citation discipline

- Every Part-4 specification carries an evidence marker: ● (filled circle, evidence-based) or ○ (empty circle, inferred from clinical reasoning or expert consensus). Unmarked = error.
- Quantified outcome claims require DOI + page/table reference, or failing that, direct URL to source. Unverified claims carry `[UNVERIFIED-QUANT]` flag.
- Two failed independent searches → CLOSED-DELETED disposition for unverifiable values; do not accumulate unresolvable UNVERIFIED flags.
- Source authenticity: confirmed real before citation. "I don't know" governs over invention.

---

## Methodological boundaries

The guidebook specifies for **formal new construction and planned retrofit**. Informal settlement housing is out of specification scope (per project-standards 2026-04-07 00:44, recorded as the project's most significant scope-shaped exclusion). The formal/informal city divide is the meta-barrier to global accessible housing; the guidebook acknowledges this as the highest-priority research and policy gap in its domain.

The guidebook is **not a substitute for professional judgment**. Population-level specifications (Tier 0 and Tier 1) are necessary but insufficient. Tier 2 person-specific co-design with an occupational therapist resolves the individual case.

The guidebook is **not a legal authority**. It does not replace jurisdictional code compliance (which is Tier 6 — the floor). Where evidence-based best practice exceeds code, the guidebook specifies the evidence-based value and notes the code value as the regulatory minimum.

The guidebook does **not pursue universal jurisdictional adoption** as its primary trajectory; it pursues equipping practitioners to make informed decisions in any jurisdiction. Trajectory positioning toward formal adoption is an A11 decision.

The guidebook is a **pre-launch single-author synthesis** drawing on published Co-1 evidence, Tier 1–6 literature, and the author's reading and judgment. Methodological integrity rests on honest evidence engagement and transparent declaration of limits — not on a fictional collaborative production structure.

---

## Operational reality

The project is currently pre-launch and authored by a single person. There are no Co-1 collaborator panels, no DPO partnerships, no recruitment thread, and no compensation infrastructure. Co-1 *evidence* is engaged through the published corpus only — peer-reviewed lived-experience literature, confirmed Co-1 advocacy positions from named organizations, and Co-1-authored academic narratives.

This is **evidence-level engagement** with Co-1, not **participation-level engagement**. CRPD Art. 4.3 is honored in partial form: the corpus engaged was itself produced through participatory processes, and the synthesis here treats that corpus as co-primary with Tier 1. Direct participation in the synthesis is not happening pre-launch. This is the methodological limit, declared.

If the project launches and resources permit, the form of collaboration with disabled people becomes a co-design question — to be answered with disabled people, not for them. Specifying that form pre-launch, in the absence of participants, would reproduce the substantive problem CRPD Art. 4.3 exists to address.

A5 (per `workplan/workplan-co0007-v3-amendments.md` Amendment 7) produces a design specification for the post-launch collaborative form: a how-it-would-work document that activates if and when conditions allow. This may never activate. **Solo-only-permanent is a possible end-state for the project.** The methodology must hold integrity in that case as well as in the launched-with-collaboration case.

The mission's claim to honor CRPD Art. 4.3 is calibrated honestly: partial pre-launch (corpus engagement); full only if launched-and-resourced; possibly never full.

---

## Test against which all downstream decisions are evaluated

Every methodological, architectural, and editorial decision in the project must be evaluated against this mission. The test:

1. Does this decision help readers ask better questions about how to design for accessibility?
2. Does it acknowledge non-uniformity — within-population variability and individual specificity?
3. Does it ground best practice in the evidence hierarchy, not in code consensus?
4. Does it surface where Co-1 evidence governs, where Tier 1 clinical evidence governs, where they converge, and where they diverge?
5. Does it respect the operational reality on Co-1 (pre-launch solo synthesis from published corpus) and document the partial-honoring limit honestly?
6. Does it teach professional judgment rather than substitute for it?
7. Is the underlying data verifiable (clean data) and the methodology declared (transparent methodology)?
8. Does it align with the audience-priority structure in `governance/audience-priority.md` — primary needs governing direct content, secondary needs governing cross-references and supplements?

Decisions that fail this test must be revised, document a justified exception, or trigger a mission revision.

---

## Status

CANONICAL-TRACK — ITERATION 1 (= A1-A2 iter 2). Not yet operative.

| Field | Value |
|---|---|
| Iteration | CANONICAL (iter 4 cross-test pass 2026-04-26 05:29) |
| Operative governance mission | **This file** — supersedes `governance/mission-PROVISIONAL.md` as of 2026-04-26 05:29 |
| Companion | `governance/audience-priority.md` (CANONICAL — locked with this file) |
| Acceptance test for canonical lock | PASSED — iter 4 cross-test 2026-04-26 05:29; one tension (T-01 audience ordering) fixed inline |
| Citation gap | CLOSED — all `[cite — iter 3]` flags resolved with DOI-verified sources (iter 3, 2026-04-25) |
| Public-facing version | Deferred to iter 5 (optional) per iteration plan |

---

## What this file does not do

- **Supersedes `mission-PROVISIONAL.md`** as of iter 4 canonical lock (2026-04-26 05:29).
- **Citations committed.** Iter 3 closed all `[cite — iter 3]` flags (2026-04-25). Citations are now inline.
- **Does not specify navigation modes.** B3 does that. This file supplies the audience-priority cross-reference; B3 must respect it.
- **Does not produce the public-facing mission.** Iter 5 (optional) splits public-facing from internal governance versions.
- **Does not pretend collaborator structures exist.** Pre-launch solo is the operational reality, declared in §Operational reality.
- **Does not specify A3 conceptual model.** A3 begins after A1-A2 closes. Iter 4 identifies A3 inputs: the four-framework layering (ICF, PEO/PEOP, Capability Approach, Kawa) specified in project-standards §2026-04-09 must align with canonical mission commitments.
