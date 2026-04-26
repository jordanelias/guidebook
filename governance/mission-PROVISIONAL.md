# Mission Statement (PROVISIONAL)
**Status:** PROVISIONAL — committed 2026-04-26 02:42 UTC per Stage 0.6
**Resolves audit finding:** T-01 (mission not committed as artifact)
**Supersedes:** synthesis Part IV passage (informal embedded text)
**Canonical version:** A1-A2 (pending)
**Coda's "sit with the mission" test:** operates on this file
**Decisions incorporated:** T-03, T-04, D-03 per `governance/pre-stage-a-decisions.md`

---

## Purpose

The Guidebook for Accessible Built Environments equips designers, policymakers, occupational therapists, and disabled people themselves with the questions they need to ask about how to design for accessibility depending on the circumstance.

It is not a prescription manual. It does not dictate values. It does not substitute for professional judgment. It is a thinking tool.

When someone knows better, they do better. The guidebook aims to raise the floor of understanding for everyone who touches the built environment.

---

## Audiences (provisional priority — A1-A2 canonicalizes)

**Primary** — practicing designers (architects, interior designers) and disabled people themselves, in two distinct use patterns each:
- Designers: information-finding (at programming and DD stages) and decision-frame (mid-project)
- Disabled people: information-finding (about their own design needs) and representation-checking (validating that one's experience is acknowledged in the work)

**Secondary** — occupational therapists (clinical-collaboration and specialist-handoff modes) and policymakers (jurisdiction-comparison and rationale modes).

The use-pattern-within-audience distinction (per audit v2 §T-05) is part of the mission, not deferred to architecture. A single audience commonly occupies multiple use patterns; the guidebook serves each pattern explicitly.

---

## Doctrinal commitments

### 1. Specifications serve questions; questions serve people; people are not uniform

Every parameter exposes its within-population variability. Population codes are organizing scaffolding, not a description of any individual within the population. Within-population variation is shown as a first-class data dimension, not buried in narrative caveats.

### 2. Best practice is determined by the evidence hierarchy, not by code consensus

Tier 1 OT-intervention clinical research, Co-1 lived experience, Co-2 OT CPGs, Tier 3 systematic reviews establish best practice. Tier 6 codes are the compliance floor, not the aspiration. **A best-practice claim derived solely from code consensus is in error.**

The seven-tier hierarchy:

| Position | Type | Source examples |
|---|---|---|
| Tier 1 | OT intervention-tested clinical research | RCTs, intervention trials |
| **Co-1** | **Lived experience / participatory design (CRPD Art. 4.3)** | DPO research, Co-1 reviewer panels, peer-reviewed lived-experience literature |
| Tier 2 | NGO / DPO / advocacy guidelines | LPA, RNID, HLAA, IDA, Habinteg |
| **Co-2** | **OT professional body CPGs** | CAOT, AOTA, RCOT, COTEC, WFOT |
| Tier 3 | Systematic reviews and meta-analyses | Cochrane, JBI, narrative SRs |
| Tier 4 | International standards (evidence-based) | ISO 21542, ISO 23599, IEC 60118-4, EN 17210 |
| Tier 5 | National beyond-code frameworks | BS 8300-2 Annex G, NL WMO-keuken, RCOTSS-Housing OT |
| Tier 6 | Statutory codes | Reference baseline only |

Co-1 is co-primary with Tier 1. Co-2 is parallel to Tier 2. Schema encodes both `tier` and `evidence_type` to preserve this parallelism (per Stage 0.5 Decision T-03).

### 3. Co-1 is co-primary evidence with Tier 1 (clean data + transparent methodology)

Co-1 evidence — lived experience and participatory design (CRPD Art. 4.3) — is not subordinate to clinical research; the two answer different questions. Where lived experience and clinical research converge, the convergence is itself evidence. Where they diverge, the divergence is documented and a synthesis approach is specified per parameter.

#### Operational declaration on Co-1 collaboration

Co-1 *evidence* (the corpus) is co-primary with Tier 1. The project's *operational* engagement of Co-1 collaborators (people) is currently at the **review** level: Co-1 representatives review and provide approval at key checkpoints, rather than drafting sections of the guidebook directly.

This declaration is honest about resourcing. Co-1 evidence flows into the guidebook through:
- Peer-reviewed lived-experience literature (papers embedding Co-1 voice — e.g., Wilson 2023 MH spaces, Kennedy 2015 UPL grab bar preferences)
- Confirmed Co-1 advocacy positions from named organizations (LPA on reach range, RNID on hearing loops, HLAA on Auracast, IDA on CRPD Art. 9 implementation)
- Co-1 reviewer consultation at project checkpoints

Co-1 evidence is NOT currently synthesized through Co-1 collaborators directly drafting guidebook text under current resourcing.

#### Trajectory clause

Where DPO partnerships, dedicated funding, and per-collaborator compensation infrastructure can be secured for a given population, the project will expand Co-1 from review to drafting for that population. Trigger conditions are specified in `governance/pre-stage-a-decisions.md` D-03 resolution.

A5 produces operational specifications for both states (Reviewer and Drafting) so transitions are mechanical when triggers fire.

### 4. Best practice for sparse-evidence populations is explicitly stated, not silent (per Stage 0.5 Decision T-04)

Each (parameter × population) cell holds one of four states:

- `stated` — best practice derived from ≥Tier 3 OR Co-1 OR Co-2 evidence
- `provisional` — synthesis based on partial evidence dimension; rich in at least one dimension; rendered with confidence flag
- `pending` — `[BEST-PRACTICE-PENDING]` marker with cross-link to `gap_register.md` entry; evidence sparse across all dimensions
- `not_applicable` — parameter has no design implication for this population; explicit rationale required

**Silence on evidence-thin populations is not the default.** The audit v2 §T-04 yardstick (Cochrane: absence-of-evidence vs evidence-of-absence vs primary-non-clinical-tier) is honored at the cell level.

### 5. Three-Tier Design Hierarchy operationalizes the doctrine

| Tier | Function | Resolution |
|---|---|---|
| Tier 0 | Universal Design / Code Compliance | Population-agnostic; fixed values |
| Tier 1 | Population-Informed Inclusive Design | Ranges; median as default |
| Tier 2 | Person-Specific Co-Design | OT assessment resolves position within Tier 1 range |

DAR (Design for Adaptable Readiness) provisions are mandatory at all tiers — the structural and electrical infrastructure that allows Tier 2 individual adaptation to occur post-construction without major retrofit cost.

### 6. Questions-led teaching is the project's pedagogical commitment

The guidebook organizes around questions readers should ask, not around answers they should adopt. **Questions are first-class data, not annotations.** Navigation modes include a questions-led entry surface (per audit v2 §T-02 / D-01 resolution).

The pedagogical hypothesis — that questions-led resources improve designer outcomes more than prescriptive ones — is informed by inquiry-based learning, scaffolded questioning in design education, and problem-based learning in professional formation literature. The hypothesis is engaged in A6 evidence methodology and tested empirically in B6 pilot validation with practicing architects.

The hypothesis is the project's distinctive epistemic claim. It is acknowledged as a claim, not asserted as established.

### 7. Universal design is co-extensive with code compliance — the floor, not an aspiration

Inclusive design is the positive aspiration. Tier 0 is the compliance baseline. Best practice exceeds Tier 0 wherever evidence supports.

---

## Methodological boundaries

The guidebook specifies for **formal new construction and planned retrofit**. Informal settlement housing is out of specification scope (per project-standards 2026-04-07 00:44, recorded as the project's most significant scope-shaped exclusion).

The guidebook is **not a substitute for professional judgment**. Population-level specifications (Tier 0 and Tier 1) are necessary but insufficient. Tier 2 person-specific co-design with an occupational therapist resolves the individual case.

The guidebook is **not a legal authority**. It does not replace jurisdictional code compliance (which is Tier 6 — the floor). Where evidence-based best practice exceeds code, the guidebook specifies the evidence-based value and notes the code value as the regulatory minimum.

The guidebook does **not pursue universal jurisdictional adoption** as its primary trajectory; it pursues equipping practitioners to make informed decisions in any jurisdiction. Trajectory positioning toward formal adoption is an A11 decision.

The guidebook **acknowledges the formal/informal city divide** as the meta-barrier to global accessible housing. The project specifies for formal contexts and identifies the informal-context gap as the highest-priority research and policy gap (per project-standards 2026-04-07 00:44).

---

## Test against which all downstream decisions are evaluated

Every methodological, architectural, and editorial decision in the project must be evaluated against this mission. The test:

1. Does this decision help readers ask better questions about how to design for accessibility?
2. Does it acknowledge non-uniformity — within-population variability and individual specificity?
3. Does it ground best practice in the evidence hierarchy, not in code consensus?
4. Does it surface where Co-1 evidence governs, where Tier 1 clinical evidence governs, where they converge, and where they diverge?
5. Does it respect the operational declaration on Co-1 (Reviewer with trajectory) and document any expansion?
6. Does it teach professional judgment rather than substitute for it?
7. Is the underlying data verifiable (clean data) and the methodology declared (transparent methodology)?

Decisions that fail this test must be revised, document a justified exception, or trigger a mission revision.

---

## Status

PROVISIONAL until A1-A2 canonical version. The Coda's "sit with the mission ≥1 day before adopting" test now operates against this file.

| Field | Value |
|---|---|
| Version | 0.6.PROVISIONAL.20260426 |
| Supersedes | synthesis Part IV passage (informal) |
| Next revision target | A1-A2 canonical version |
| Resolution principle | Clean data + transparent methodology |
| Adoption decision authority | Project owner |
| Adoption decision pending in | Stage 0.9 (workplan adoption) |

---

## What this file does not do

- **Does not commit A1-A2 canonical mission.** That is the next mission revision.
- **Does not implement schema, validators, or skills.** Implementation is B1, B2, C2.
- **Does not specify A5 (Co-1 relationship operational specification).** A5 produces that, with Reviewer-state and Drafting-state both specified per D-03 trajectory.
- **Does not specify A11 (legal/regulatory framework).** Trajectory positioning toward formal adoption is A11 work.
- **Does not pre-empt the audit-recommended "sit with mission ≥1 day" wait.** This file is the artifact to sit with.
