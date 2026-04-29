# Co-1 Operational Specification
**Status:** DRAFT — A5 Session 1 of 2–3 (sections 1–3 below; sections 4–7 in subsequent sessions)
**Phase:** Stage A Phase 5 — Co-1 operational specification
**Created:** 2026-04-29 14:30 UTC
**Doctrinal basis:** D-03 revised (`governance/pre-stage-a-decisions.md` 2026-04-26 03:45) · Amendment 7 (`workplan/workplan-co0007-v3-amendments.md`) · Core Doctrine 2026-04-26 03:45 (`references/project-standards.md`) · Mission §3, §Operational reality, §Epistemic commitments
**Pattern:** Prose only (no Python; A5 is the second prose-only Stage A phase after A4)
**Sessions estimated:** 2–3 (Amendment 7-revised; was 5–7 in v3 baseline)

---

## 1. What Co-1 is

Co-1 is the evidence tier that the Seven-Tier Evidence Hierarchy designates as **co-primary with Tier 1 OT-intervention clinical research** for purposes of best-practice claims in this guidebook. The full canonical text is in `governance/mission-and-epistemics.md` §Doctrinal commitments §3 and §Epistemic commitments §Evidence hierarchy. This specification operates within that text; it does not revise it.

### 1.1 Definition

Co-1 evidence is **lived experience and participatory design research produced by, with, or under the methodological authority of disabled people**. Per the doctrinal commitments, it is co-primary with Tier 1 — not subordinate, not equivalent-by-flattening, but answering different questions to which Tier 1 clinical research alone cannot answer.

The four types of Co-1 source recognized in `governance/mission-and-epistemics.md` §Evidence hierarchy:

1. Peer-reviewed lived-experience literature
2. Disabled People's Organizations (DPO) research outputs
3. Named advocacy organizational positions
4. Co-1-authored academic narratives

Each carries `tier: 1, evidence_type: co1` in the schema (per Stage 0.5 Decision T-03). The encoding preserves the co-primary relationship with Tier 1 (`tier: 1, evidence_type: clinical`) without flattening either tier into the other.

### 1.2 What Co-1 is not

Co-1 is **not** an aggregation of disabled-person opinion. The methodological authority of Co-1 derives from:

- **Peer review** (in the case of academic literature)
- **Organizational accountability** (in the case of DPO research and advocacy positions — published under the name of an organization that is itself answerable to a disabled constituency)
- **Authorship by people whose lived experience is the subject of the research** (in the case of academic narratives)

A statement by a single disabled person speaking only for themselves is not Co-1 evidence. It is a personal testimony — meaningful, but not Co-1 in the schematic sense. Co-1 requires methodological grounding: peer review, organizational accountability, or scholarly authorship. The distinction matters because Co-1's epistemic weight in best-practice claims rests on this grounding, not on disability identity alone.

### 1.3 Co-1 vs. Co-2

Co-1 is paired in the hierarchy with **Co-2 (OT professional body Clinical Practice Guidelines** — CAOT, AOTA, RCOT, COTEC, WFOT). The two are parallel co-primary tiers at different levels: Co-1 sits beside Tier 1 (clinical research); Co-2 sits beside Tier 2 (NGO/DPO/advocacy guidelines). Both encode professional or community methodological authority that clinical research alone does not capture.

In schema terms: Co-1 records carry `tier: 1, evidence_type: co1`; Co-2 records carry `tier: 2, evidence_type: co2`. The two are not interchangeable. Co-2 is OT professional consensus; Co-1 is disabled-person methodological authority. A specification may cite both; they do not substitute for each other.

### 1.4 The CRPD Article 4.3 grounding

CRPD Article 4.3 establishes the State Party obligation to "closely consult with and actively involve persons with disabilities, including children with disabilities, through their representative organizations" in the development and implementation of legislation and policies affecting them. This is **the participation principle** — meaningful participation of disabled people in decisions affecting them.

The mission-and-epistemics §Doctrinal commitments §3 grounds Co-1's co-primary status in this principle. The reasoning: Tier 1 OT clinical research, however rigorous, does not by its method include disabled-people-as-co-producers-of-knowledge. CRPD Art. 4.3 names that absence as a thing that needs filling. Co-1 evidence — produced by disabled people, by their representative organizations, or under their methodological authority — fills it.

This is not a courtesy; it is a methodological commitment. A best-practice claim in a domain where Co-1 evidence is available, made without engaging Co-1 evidence, is methodologically incomplete. The seven-tier hierarchy makes this explicit.

---

## 2. Pre-launch operational reality

### 2.1 The current state

The project is currently authored by a single person. There are no Co-1 collaborator panels, no DPO partnerships, no recruitment thread, no compensation infrastructure. There is no Reviewer state. There is no Drafting state. There are no triggers between states.

This is the operational reality declared in:

- `references/project-standards.md` Core Doctrine 2026-04-26 03:45 (RULE: Pre-launch operational reality — solo authorship; no collaborator infrastructure)
- `governance/pre-stage-a-decisions.md` D-03 revised 2026-04-26 03:45
- `governance/mission-and-epistemics.md` §Operational reality
- `workplan/workplan-co0007-v3-amendments.md` Amendment 7

Co-1 *evidence* is engaged through the published corpus only. Co-1 *participation* is not happening pre-launch.

### 2.2 What this distinction means

The distinction between **evidence-level engagement** and **participation-level engagement** is the core of A5. The two are not equivalent.

| | Evidence-level engagement | Participation-level engagement |
|---|---|---|
| **What** | Reading, citing, synthesizing Co-1 evidence already produced and published | Disabled people involved as co-producers of synthesis, as decision-makers about the project's content |
| **Methodological authority** | The published corpus carries the participation it was produced through | The project itself is a participatory production |
| **Pre-launch state** | Operative — this is what the project does | Inoperative — there are no participants |
| **Post-launch state** | Continues; corpus engagement is ongoing | Contingent on launch occurring + resources permitting + the form being co-designed with disabled people |
| **CRPD Art. 4.3 honoring** | Partial — engaging participatory products | Full — making the synthesis itself participatory |

The project is in the left column pre-launch. It may move to the right column post-launch if launch occurs and resources permit. **It may not. Solo-only-permanent is a possible end-state.** The methodology must hold integrity in either case.

### 2.3 The honesty constraint

The original D-03 resolution (2026-04-26 02:42 UTC, superseded 2026-04-26 03:45) described an operational structure that did not exist: Co-1 collaborators at "Reviewer level" with pending triggers for "Drafting" state. The revision corrected this. The corrected language is the only operative language.

The honesty constraint that follows: **the guidebook may not, in its prose or in its citation conventions, imply Co-1 participation that does not exist**. This rule is the highest-priority adversarial-use risk in the project (per A10 framework, pending). Misrepresentation here is not an editorial slip — it is a methodological lie that undermines the project's claim to honor CRPD Art. 4.3 even partially.

The voice convention §5 below operationalizes this rule. A4 voice-style §8.1 already provides the language pattern (tier-located, authority-located). A5 specifies how it applies to Co-1 specifically.

### 2.4 What pre-launch solo authorship can do

Within the evidence-level-engagement column, the project can do — and is doing — the following:

1. **Curate Co-1 sources.** Read peer-reviewed Co-1 literature, DPO research, named advocacy positions, Co-1-authored academic narratives. Identify the sources that bear methodological weight on each design parameter.
2. **Cite Co-1 evidence with attribution.** Every Co-1 citation names its source organization or author and identifies the source as Co-1 (`evidence_type: co1`).
3. **Synthesize across Co-1 sources.** Where multiple Co-1 sources address the same parameter, the guidebook draws synthesis claims from the convergence. Where they diverge, both are presented per the §3 evidence-state machine in mission-and-epistemics §Epistemic commitments.
4. **Treat Co-1 evidence as co-primary.** Tier 1 clinical research is not allowed to override Co-1 evidence by default; the two answer different questions and a synthesis approach is specified per parameter where they diverge.
5. **Declare partial honoring.** Mission and prose declare that pre-launch is partial CRPD Art. 4.3 honoring — corpus engagement, not participation. The gap is visible and named.

### 2.5 What pre-launch solo authorship cannot do

The following are foreclosed pre-launch:

1. **Claim in-house Co-1 representation.** No Co-1 collaborator role exists. The guidebook may not imply otherwise.
2. **Claim Co-1 endorsement of synthesis decisions.** The Co-1 sources cited produced the evidence; they did not review or endorse the guidebook's synthesis of their work.
3. **Operate the CS2 recruitment thread.** Recruitment is inoperative pre-launch (Amendment 7).
4. **Operate CS5 collaborator-representation monitoring.** Re-scoped to corpus-representation monitoring (a different question — addressed in §3.2 below).
5. **Run Co-1 review at iteration boundaries.** A1-A2, A4, B6 validation rigor is solo-author cross-checking against committed mission language. Weaker rigor than external Co-1 review would provide; declared in mission §6.
6. **Speak as a Co-1 voice.** The author is one disabled person; this is not Co-1 representation in the methodological sense (per §1.2). Solo authorship by a disabled person is not equivalent to Co-1 production. The mission declares the synthesis as solo authorship informed by Co-1 evidence, not as Co-1 production.

---

## 3. Resolution of substantive open questions

The handoff document `workplan/a5-handoff.md` §4 surfaced five substantive judgments A5 must make. Sections 3.1–3.5 below resolve them. Each resolution carries a `[CONFIDENCE]` flag per `<logging>` standard, with rationale.

### 3.1 Q1 — How does the guidebook represent Co-1 evidence honestly under solo authorship?

**Resolution:** Three-part rule.

**Part A — This guidebook treats provenance marking as mandatory.** Every Co-1 citation in the guidebook carries explicit provenance. The schema (B1) needs a `co1_provenance` field on the EvidenceSource entity. The values:

- `published_corpus` — peer-reviewed Co-1 literature, DPO research outputs, named advocacy positions, Co-1-authored academic narratives that the guidebook engages by reading and citing
- `participatory_synthesis` — guidebook content produced through Co-1 collaborator participation in the synthesis itself

**Pre-launch, every Co-1 citation has `co1_provenance: published_corpus`.** None has `participatory_synthesis`. This is the schematic correlate of the §2.2 evidence-level-vs-participation-level distinction. Post-launch, if Co-1 collaboration activates, some new citations may carry `participatory_synthesis` — but the pre-launch corpus citations do not retroactively become participatory.

**Part B — Voice conventions distinguish single-source citation from multi-source synthesis.** Per A4 voice-style §8.1, specification voice locates authority appropriately. For Co-1, two patterns:

- *Single Co-1 source citation:* "[Source name] documents…" — names the source, locates the claim in their authority. Example: "*Disabled World*'s 2023 fragrance-sensitivity report documents that..."
- *Multi-source Co-1 synthesis:* "Co-1 sources document [claim]; sources cited: [list]." — declares the multi-source nature, lists the sources, leaves the synthesis attribution to the guidebook. Example: "Co-1 sources document a population-level preference for matte over glossy interior surfaces; sources cited: NDV/AUT-Aspect (2024), CAS Vision Australia (2022), Mostafa ASPECTSS 2.0 (2021)."

**Pattern selection rule:** if the claim is found in one source, use single-source. If the claim is the guidebook's synthesis across multiple sources, use multi-source. Never imply multi-source convergence from a single source.

**Part C — Convergence and divergence with Tier 1 are surfaced.** Per `governance/mission-and-epistemics.md` §3: "Where they converge, the convergence is itself evidence. Where they diverge, the divergence is documented and a synthesis approach is specified per parameter."

The voice convention for convergence: "Co-1 and Tier 1 evidence converge on [value]: Tier 1 ([source]) shows [Tier 1 finding]; Co-1 ([source/list]) document [Co-1 finding]; the converged best-practice value is [value]."

The voice convention for divergence: "Co-1 and Tier 1 evidence diverge on [parameter]. Tier 1 ([source]) shows [Tier 1 finding]. Co-1 ([source/list]) document [Co-1 finding]. The Tier 1 range encompasses both findings: [range]. Per Part 1 §1.5, both are presented; OT assessment at Tier 2 resolves position within range based on individual functional and lived-experience profile."

[CONFIDENCE: high — Part A is the schematic correlate of D-03 revised, directly entailed; Part B follows from voice-style §8.1 pattern; Part C is direct application of mission §3.]

### 3.2 Q2 — What do CS2 and CS5 look like operationally pre-launch?

**Resolution:**

**CS2 (Co-1 recruitment):** INOPERATIVE pre-launch. No pre-launch operational substitute. The recruitment thread does not run; coordination overhead is zero. This is the Amendment 7 specification, restated here.

**CS5 (Co-1 representation monitoring):** Re-scoped pre-launch to **corpus-representation monitoring**. This is a different question from collaborator-representation monitoring.

- *Collaborator-representation monitoring* (post-launch concept): Are the people involved in the project as collaborators representative of the populations the project serves? Pre-launch: not applicable. There are no collaborators.
- *Corpus-representation monitoring* (pre-launch operative concept): Is the Co-1 evidence corpus the project draws on representative across the populations the project serves? Are some populations under-represented in the corpus? Are some Co-1 sources over-represented?

**Pre-launch CS5 operates as corpus-representation monitoring.** The operational form: per-population Co-1 corpus inventory; gap-flagging against `gap_register.md` for populations with thin or absent Co-1 source coverage; expanded literature search triggered by corpus-thinness rather than recruitment triggered by collaborator absence.

**Post-launch contingent activation of CS2:** If launch occurs and resources permit, CS2 activates with a recruitment specification co-designed with disabled people. This specification is not produced pre-launch — pre-specifying the form of participation in the absence of participants reproduces the substantive problem CRPD Art. 4.3 exists to address (per D-03 revised).

**Triggers for post-launch CS2 activation (when activation is appropriate):**

1. Launch occurs (the guidebook becomes a public artifact)
2. Resources are committed for compensation infrastructure (the project can pay collaborators meaningfully)
3. A co-design process is initiated with disabled people on the form CS2 takes (the recruitment specification is itself the product of participation, not solo authorship)

All three triggers must be met. Any one being unmet means CS2 stays inoperative.

**If launch never occurs:** CS2 remains permanently inoperative. CS5 stays in corpus-representation monitoring form. Solo-only-permanent is a possible end-state and is not a project failure under that condition; the methodology was honest about its limit.

[CONFIDENCE: high — direct application of Amendment 7 + D-03 revised. Corpus-representation monitoring concept is named in Amendment 7's CS5 row; this section operationalizes the name.]

### 3.3 Q5 — What is the relationship between Co-1 status and audience priority?

**Resolution:** Co-1 (evidence tier) and audience-priority "disabled people" (audience class) are related but distinct. They must not be conflated.

**Audience-priority "disabled people"** (per `governance/audience-priority.md` §Primary audiences) names *who reads the guidebook*. Disabled people are primary audience because the guidebook's claim to evidence-based best practice is empty if it is not legible and accountable to the people whose needs it claims to specify. Their use-patterns are information-finding and representation-checking.

**Co-1 evidence** names *whose lived experience the evidence draws from*. The lived-experience evidence in the guidebook is produced by, with, or under methodological authority of disabled people.

The two are linked: a guidebook that draws on Co-1 evidence and is read by disabled people closes a loop — the synthesis of disabled-people-produced evidence is read by disabled people who can test whether the synthesis honors the evidence. This is the representation-checking use-pattern.

But the link is operational, not definitional. Audience-priority is about who reads. Co-1 is about whose evidence is drawn on. The two answer different questions and operate at different points in the production chain.

**Solo authorship by a disabled person.** The current sole author of the guidebook is one disabled person. This is **not Co-1 representation in the methodological sense** (per §1.2 above). It is solo authorship by someone with lived experience. The two are not equivalent.

**The author's lived experience is part of the evidence base the project draws on**, in the same sense that any author's domain expertise is part of what they bring to a synthesis. But the author's lived experience is not Co-1 evidence in the schematic sense — it is not peer-reviewed, not produced under organizational accountability, not authored as participatory research output.

**The voice convention for handling this:** the guidebook does not cite the author's lived experience as Co-1 evidence. It does not foreground the author's identity as a substitute for Co-1 representation. It does not claim representational legitimacy on the basis of the author being one disabled person. The mission's pre-launch operational reality declaration (the synthesis is solo work by someone with lived experience, drawing on the published Co-1 corpus) is the truthful framing.

**What this rules out:** a front-matter "By an autistic author" or "Author lived-experience disclosure" section that functions as a Co-1 claim. The author's identity may be relevant to publication transparency post-launch, but it is not a substitute for Co-1 representation in the methodological sense.

**What this rules in:** the published Co-1 corpus, treated as co-primary with Tier 1, cited with provenance, with multi-source synthesis declared. The legitimate Co-1 commitment is in the corpus engagement, not in the author's identity.

[CONFIDENCE: high — direct entailment of §1.2 distinction (Co-1 = methodological grounding, not identity) + audience-priority canonical text + mission §Operational reality.]

### 3.4 Q3 and Q4 — Deferred to Session 2

Q3 (what the guidebook owes Co-1 sources whose work it cites — attribution and disclosure protocols) and Q4 (Co-1 ↔ Three-Tier Design Hierarchy interaction) are deferred to Session 2 of A5.

**Reasons for deferring:**

- **Q3** requires research into named DPO and Co-1 source organization attribution practices and may interact with A11 (legal and regulatory framework) on notification protocols. Best handled with Session 2's fresh context and possible external research cycle.
- **Q4** depends on completed §5 voice conventions (Session 2 deliverable) and on the schema specification work that B1 will undertake. Specifying Q4 fully now risks pre-empting B1.

Sessions 2 and possibly 3 of A5 close out Q3, Q4, and §§4–7 of this document.

---

## 4. Sections deferred

§§4–7 of the original handoff §5 plan are deferred to Session 2:

- **§4 — CS2 and CS5 trigger specification.** Foundation laid in §3.2 above; full specification with activation procedure, decision authority, and timeline form deferred.
- **§5 — Voice conventions for Co-1 evidence in guidebook prose.** Foundation laid in §3.1 above; full voice convention spec with worked examples across populations deferred.
- **§6 — Documentation requirements per Co-1 citation.** Schema implications named (§3.1 Part A); full documentation requirements deferred.
- **§7 — Schema implications and pointers to B1.** Named in §3.1 Part A and §1.1; full pointer document for B1 deferred.

These are not blocked. Session 2 produces them.

---

## 5. Cross-stage impact recorded by this Session 1 draft

| Thread | Effect of this Session |
|---|---|
| **CS2** (Co-1 recruitment) | Confirmed INOPERATIVE pre-launch. Trigger spec partial (§3.2); full spec Session 2. |
| **CS5** (Co-1 representation monitoring) | Re-scoped to corpus-representation monitoring (per Amendment 7 + this §3.2). Operational form named: per-population Co-1 corpus inventory + gap-flagging. Implementation deferred to Stage C. |
| **CS8** (Decision capture) | Three substantive resolutions (Q1, Q2, Q5) captured per §3 with [CONFIDENCE] flags. CS8 doesn't go LIVE until A12, so this capture is provisional in format. |
| **CS4** (Re-issue cadence) | A5 closure does not trigger synthesis re-issue (CS4 specifies end-of-Stage-A and B7 lock as triggers). |
| **B1** (schema design) | New `co1_provenance` field required on EvidenceSource entity, with values `published_corpus` / `participatory_synthesis`. Pre-launch: all values are `published_corpus`. |

---

## 6. Open work for A5 Session 2

1. Resolve Q3 — attribution and disclosure protocols for cited Co-1 sources
2. Resolve Q4 — Co-1 ↔ Three-Tier Design Hierarchy interaction in voice conventions
3. Produce §4 — full CS2 / CS5 trigger specification (activation procedure, decision authority, timeline form)
4. Produce §5 — full voice convention specification with worked examples across populations
5. Produce §6 — documentation requirements per Co-1 citation
6. Produce §7 — schema implications and pointers to B1
7. Update voice-style §8.1 with Co-1-specific construction patterns from §3.1 (Single Co-1 source citation; Multi-source Co-1 synthesis; Convergence; Divergence)

Session 3 (if needed) handles externally-researchable items in Q3 (DPO attribution practice review).

---

## 7. Status

DRAFT — A5 Session 1 sections 1–3 complete. Sections 4–7 deferred to Session 2.

| Field | Value |
|---|---|
| Created | 2026-04-29 14:30 UTC |
| Phase | Stage A Phase 5 (Co-1 operational specification) — Session 1 of 2–3 |
| Status | DRAFT — not yet canonical; canonical lock at end of A5 final session |
| Author | Project owner (solo, pre-launch) |
| Doctrinal anchor | D-03 revised (`pre-stage-a-decisions.md`) + Amendment 7 + Mission §3, §Operational reality, §Epistemic commitments + project-standards 2026-04-26 03:45 |
| Companion governance | `governance/mission-and-epistemics.md` (canonical) · `governance/audience-priority.md` (canonical) · `governance/pre-stage-a-decisions.md` |
| Resolves Q's | Q1 (representation honesty); Q2 (CS2/CS5 pre-launch substitute); Q5 (audience ↔ Co-1 distinction) |
| Defers Q's | Q3 (attribution/disclosure); Q4 (Co-1 ↔ Three-Tier interaction) |

**Next session entry condition:** confirm Q3 external research scope; load `governance/repo-strategy.md` (B1 schema design implications); load existing Co-1 source samples from BPC files to ground worked-example voice conventions.

---

**End of A5 Session 1 draft.**
