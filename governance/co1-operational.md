# Co-1 Operational Specification
**Status:** CANONICAL — A5 complete (Session 2 of 2)
**Phase:** Stage A Phase 5 — Co-1 operational specification
**Created:** 2026-04-29 14:30 UTC (S1) · **Closed:** 2026-04-29 15:50 UTC (S2)
**Doctrinal basis:** D-03 revised (`governance/pre-stage-a-decisions.md` 2026-04-26 03:45) · Amendment 7 (`workplan/workplan-co0007-v3-amendments.md`) · Core Doctrine 2026-04-26 03:45 (`references/project-standards.md`) · Mission §3, §Operational reality, §Epistemic commitments
**Pattern:** Prose only (no Python; A5 is the second prose-only Stage A phase after A4)
**Sessions consumed:** 2 of 2–3 budget (Amendment 7 revised)

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

Co-1 is paired in the hierarchy with **Co-2 (OT professional body Clinical Practice Guidelines** — CAOT, AOTA, RCOT, COTEC, WFOT). The two are parallel co-primary tiers at different levels: Co-1 sits beside Tier 1 (primary research); Co-2 sits beside Tier 2 (community-consensus synthesis: systematic reviews / meta-analyses and named-organisation evidence-based standards). Both encode professional or community methodological authority that clinical research alone does not capture.

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

The voice convention for divergence: "Co-1 and Tier 1 evidence diverge on [parameter]. Tier 1 ([source]) shows [Tier 1 finding]. Co-1 ([source/list]) document [Co-1 finding]. The Tier 1 range encompasses both findings: [range]. Per Part 1 §1.5, both are presented; OT assessment resolves the individual's own functional needs — informed by, but not bounded by, that range — based on individual functional and lived-experience profile."

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

### 3.4 Q3 — What does the guidebook owe Co-1 sources whose work it cites?

**Resolution:** Three-tier obligation structure, scaled to the nature of the relationship between the guidebook and the cited Co-1 source.

**Tier 1 obligation — All cited Co-1 sources.** Every Co-1 source cited in the guidebook receives:

1. **Full attribution.** Author/organization name, year, title, publisher/journal, DOI or URL. The format already in use across the corpus (per `references/co1-verified-sources.json`) is the operative format.
2. **Source-type identification.** Whether the source is peer-reviewed literature, DPO research, organizational position, or academic narrative — per the four-type taxonomy in §1.1.
3. **Verification status.** The 2026-04-23 verification report established a status taxonomy (`VERIFIED`, `VERIFIED-WITH-CORRECTION`, `UNVERIFIED-1`, `UNVERIFIED-CLOSED`, `CLOSED-DELETED`). Any cited Co-1 source must hold one of these statuses; cells citing `UNVERIFIED-CLOSED` or `CLOSED-DELETED` sources are themselves removed or marked `[BEST-PRACTICE-PENDING]` per T-04.

**Tier 2 obligation — Co-1 sources whose work the guidebook substantially synthesizes.** Where the guidebook draws on a Co-1 source for multiple cells or builds significant synthesis from a single source, an additional obligation applies:

4. **Synthesis attribution.** The Co-1 source's contribution to the guidebook's synthesis is named, not merely cited. Example: where DSDG (DeafSpace Design Guidelines, Gallaudet 2010) provides the population-level spatial framework that the guidebook's DEAF chapter is built around, the chapter front matter names DSDG as a foundational source, not just a citation. This is editorial transparency: readers see what the synthesis stands on.
5. **No claim of endorsement.** The guidebook may not claim the Co-1 source has endorsed the synthesis. Citing DSDG is not the same as DSDG approving how the guidebook synthesizes its content. The voice convention §5 below operationalizes this distinction.

**Tier 3 obligation — Co-1 sources whose published work explicitly invites adaptation or implementation.** Some Co-1 sources are published as design tools intended for adaptation (e.g., Invalidiliitto ESKEH audit tool; DSDC EADDAT; Mostafa ASPECTSS). For these, the obligation extends:

6. **Tool-use attribution.** Where the guidebook uses, adapts, or extends such a tool, the adaptation is documented, the original tool's authors are attributed, and any modifications are flagged. Original tool integrity is preserved; the guidebook's adaptation is the guidebook's, not the original authors'.
7. **Notification (post-launch contingent).** Pre-launch, no notification is feasible — the guidebook is not a public artifact. Post-launch, if the guidebook becomes public, the cited tool authors should receive notification that their tool has been engaged in this synthesis. This is courtesy and traceability, not licensing — most Co-1 design tools are open in their original publication. Specifying notification protocols is deferred to A11 (legal and regulatory framework) where licensing and citation-formality questions are resolved.

**What this resolution does not do:**

- **Does not commit to seeking Co-1 source review pre-launch.** Pre-launch is solo authorship (per §2.1). Post-launch contingent activation may include reviewer/feedback channels with Co-1 sources whose work is foregrounded, but specifying that pre-launch reproduces the substantive problem (D-03 revised).
- **Does not specify financial compensation.** Compensation infrastructure does not exist pre-launch. Post-launch CS2 activation triggers (§3.2) include compensation as a precondition.
- **Does not constitute legal opinion on attribution sufficiency.** A11 + counsel review establish the legal sufficiency of attribution. This A5 specification is the methodological obligation; A11 specifies the legal form.

[CONFIDENCE: high — Tiers 1–2 are direct application of existing project practice (per `references/co1-verified-sources.json` + verification report); Tier 3 surfaces a real distinction not previously named; no doctrinal conflict.]

### 3.5 Q4 — How does Co-1 status interact with the Design Modes?

**Resolution:** Co-1 status operates alongside the Design Modes, not within it. The two are orthogonal axes that co-locate authority for any given specification.

**The Design Modes** locates *the kind of design decision*: Universal Mode (universal, code-compliant); Tier 1 (population-informed); Tier 2 (person-specific, OT-resolved). It answers: *what kind of design problem is this?*

**The Seven-Tier Evidence Hierarchy** locates *what evidence supports the value*: Tier 1 primary research (OT-prioritized but not OT-exclusive, per D-E), Co-1 lived experience, Tier 2 synthesis (systematic reviews / meta-analyses and named-organisation evidence-based standards), Co-2 OT CPGs, Tier 3 lower-control primary clinical and grey-literature primary research, Tier 4 international standards, Tier 5 national frameworks, Tier 6 codes. It answers: *what is the basis for this number/range/specification?*

**The two interact at every cell** in the guidebook's specification matrix. A Tier 1 design specification (population-informed range) may be supported by:

- Tier 1 OT clinical research (e.g., AOTA grab-bar grip-strength studies)
- Co-1 lived experience (e.g., DSDG signing-space dimensions)
- Both (convergent evidence)
- Either alone with the other absent (provisional state per T-04)

**Voice convention for handling the interaction.** Per A4 voice-style §8.1, specification voice locates authority. For specifications where Co-1 evidence is the basis (alone or alongside Tier 1):

- **Tier 1 design + Tier 1 OT evidence (no Co-1):** "Tier 1 evidence supports a grab bar diameter of 32–35 mm (Sanford 2010; AOTA 2018). Mode P default: 33 mm."
- **Tier 1 design + Co-1 evidence (no Tier 1 clinical):** "Co-1 sources document a signing-space corridor width of 2440 mm (DSDG, Gallaudet 2010; DeafScape, Vaughn 2018). The Mode P default for DEAF-primary corridors is 2440 mm. *Note: this width is derived from ASL proxemics at Gallaudet; signed-language proxemics vary across BSL, DGS, NGT, LSF, and LIS — see DEAF BPC for jurisdictional variation.*"
- **Tier 1 design + both Tier 1 OT + Co-1 evidence (convergent):** "Tier 1 OT evidence (Murgia 2023, Iglehart 2020) and Co-1 sources (DSDG; PVA Accessible Home Design 2021) converge on RT60 ≤0.6 s for shared-use teaching spaces. Mode P default: 0.5 s."
- **Tier 1 design + both, divergent:** "Tier 1 OT evidence (Smith 2022) supports threshold height ≤ 6 mm. Co-1 sources (Concrete Change 1987; PVA 2021) document zero-step preference at primary entrances for visitability and aging-in-place. The Tier 1 range is 0–6 mm; the population-informed default for residential primary entrances is 0 mm (zero-step) per Co-1 visitability framework, with the 6 mm Tier 1 OT clinical maximum applying where structural constraints prevent zero-step."

**Tier 2 (person-specific) and Co-1 evidence.** Tier 2 specifications are resolved by OT assessment of the named individual, against the Tier 1 range. Co-1 evidence informs the Tier 1 range but does not override Tier 2 individual assessment. The OT, working with the individual at Tier 2, may consult Co-1 sources as part of clinical reasoning — but the resolution at Tier 2 is the OT's professional judgment plus the individual's assessed values, not a re-application of population-level Co-1 evidence.

**This means:** Co-1 governs at Tier 1 (population-informed) and contributes at Universal Mode (where universal-design choices reflect cumulative Co-1-grounded evidence). Co-1 does not override Tier 2 individual assessment. An individual's clinical-and-lived-experience profile may differ from any single Co-1 source's reported population pattern; that is exactly what Mode S OT co-design exists to resolve.

[CONFIDENCE: high — direct entailment of mission §3 (Co-1 co-primary with Tier 1) + Design Modes + voice-style §8.1. Worked examples are derived from existing corpus (DEAF BPC + Co-1-verified-sources.json).]

---

## 4. CS2 and CS5 trigger specification

This section operationalizes §3.2 (Q2 resolution) into a complete activation procedure, decision authority, and timeline form. It is the specification document Amendment 7 calls for: "A5 produces design specification for post-launch collaborative form (a how-it-would-work document)."

### 4.1 CS2 (Co-1 recruitment) — full activation specification

**Pre-launch state:** INOPERATIVE. No coordination overhead. No recruitment activity. No collaborator slots. No compensation budget. No DPO outreach. No representation thread.

This is not a deficiency to be fixed; it is the project's truthfully declared operational reality.

**Activation triggers (all three must be met):**

| Trigger | Operationalization |
|---|---|
| **T-CS2-1: Launch occurs** | The guidebook is published or otherwise becomes a publicly available artifact. Solo synthesis as a private working document does not satisfy this trigger. |
| **T-CS2-2: Resources committed for compensation** | A specific budget for Co-1 collaborator compensation exists at meaningful rates (referenced against established DPO-research compensation benchmarks at the time of activation, not at the time of this specification). Volunteer-only or token-honorarium frameworks do not satisfy this trigger; CRPD Art. 4.3 requires meaningful participation, which requires meaningful compensation. |
| **T-CS2-3: Co-design of the recruitment specification itself** | The form CS2 takes is co-designed with disabled people, not pre-specified by the project. Per D-03 revised: "Specifying that form pre-launch, in the absence of participants, would reproduce the substantive problem CRPD Art. 4.3 exists to address." This trigger means: the first Co-1 collaborative engagement is specifying CS2 itself, not delivering on a pre-specified CS2. |

**All three triggers required.** Any one being unmet keeps CS2 inoperative. Particular attention to T-CS2-3: even with launch + compensation, the project may not start CS2 by enacting a pre-specified recruitment plan. The recruitment plan is itself the first co-design output.

**Decision authority for activation:** Project owner, with documented co-design step at T-CS2-3 (i.e., the project owner does not unilaterally specify CS2 form). If post-launch the project transitions to a multi-author or organizational structure, decision authority transitions accordingly; specifying that transition is post-launch work.

**Timeline form:** Indeterminate. The triggers are state-based, not date-based. T-CS2-1 has no deadline because launch is contingent. T-CS2-2 has no deadline because resourcing is contingent. T-CS2-3 has no deadline because it presupposes the prior two.

**If CS2 never activates:** The project's solo-only-permanent end-state (per Amendment 7) is the operative reality. The methodological declaration of partial CRPD Art. 4.3 honoring (corpus engagement only, never full participatory honoring) becomes permanent. This is honest about the project's limit, not a failure.

### 4.2 CS5 (Co-1 representation monitoring) — pre-launch and post-launch forms

**Pre-launch form: Corpus-representation monitoring.**

**Question CS5 answers pre-launch:** Is the Co-1 evidence corpus the project draws on representative across the populations, jurisdictions, and design domains the project serves?

**Operational mechanism:**

1. **Per-population Co-1 source inventory.** For each population code (MOB, VIS, DEAF, DEM, NDV, OFS, PAIN, NEU, UPL, DBL, BAR), enumerate the Co-1 sources currently engaged. Source: `references/co1-verified-sources.json` cross-referenced against population coverage in BPC files.
2. **Per-domain Co-1 source inventory.** For each major design domain (residential, healthcare, education, workplace, cultural, hospitality, transport, retail), enumerate the Co-1 sources providing evidence for that domain.
3. **Per-jurisdiction Co-1 source inventory.** For each jurisdiction in the 24-jurisdiction comparative set, identify whether Co-1 sources from that jurisdiction or about that jurisdiction's lived experience are present.
4. **Gap-flagging.** Where any of (1)–(3) shows thin or absent coverage, an entry is added to `gap_register.md` with priority calibrated to the population's centrality to the guidebook's audience commitments. Gaps trigger expanded literature search, not recruitment.
5. **Cadence.** CS5 inventory is run at each Stage transition (Stage A → B; B → C) and at any synthesis re-issue per CS4 cadence. Continuous monitoring through Stage C is implicit in C7 evidence migration work.

**Post-launch form: Both corpus-representation and collaborator-representation monitoring.**

If CS2 activates post-launch, CS5 expands to also monitor:

6. **Collaborator-representation.** Are the collaborators participating in the project representative of the populations the project serves? Drift triggers expanded recruitment per the (post-launch co-designed) CS2 form. This is the v3-baseline CS5 form, restored if and when CS2 activates.

**If CS2 never activates:** CS5 stays in corpus-representation form permanently. This is a coherent and methodologically defensible monitoring practice in the solo-only-permanent end-state.

### 4.3 The CS2/CS5 distinction in declarable terms

The guidebook's published documentation (front matter, methodology declarations, future website transparency pages) reflects this distinction. Pre-launch:

> *"This guidebook engages the Co-1 evidence corpus — peer-reviewed lived-experience research, DPO research outputs, named advocacy organizational positions, and Co-1-authored academic narratives — through the synthesis of one author. There are no Co-1 collaborators currently participating in the production of this guidebook. The Co-1 evidence base is monitored for population, domain, and jurisdictional representation; gaps are logged and addressed through expanded literature search. This is partial CRPD Article 4.3 honoring at the evidence level. Full participatory honoring requires people; the project's post-launch trajectory may, contingently, expand to that form."*

This declaration may be revised post-launch as conditions change. The pre-launch form is the operative declaration now.

---

## 5. Voice conventions for Co-1 evidence in guidebook prose

This section operationalizes the §3.1 (Q1) and §3.5 (Q4) resolutions into a voice convention specification with worked examples across populations. It updates voice-style §8.1 with Co-1-specific construction patterns.

### 5.1 The four canonical Co-1 voice patterns

**Pattern Co-1-A — Single Co-1 source citation.**

Use when one Co-1 source supports the claim. Names the source; locates the claim in their authority.

> Construction: "[Source name] documents [finding]." OR "[Source name] ([year/citation]) shows [finding]."

> Example (DEAF): "*DSDG* (DeafSpace Design Guidelines, Gallaudet 2010) documents that signing-space corridors should be a minimum 2440 mm (8 ft) wide where ASL signing groups are anticipated."

> Example (PAIN): "*PVA Accessible Home Design* (2nd edition, 2021) shows a population-level preference for slip-resistant matte flooring in primary circulation, attributed to fall-risk consequences of glare-and-glossy interaction with PAIN-population proprioceptive uncertainty."

**Pattern Co-1-B — Multi-source Co-1 synthesis.**

Use when the claim is the guidebook's synthesis across multiple Co-1 sources. Declares the multi-source nature; lists the sources; leaves synthesis attribution to the guidebook (not to any single source).

> Construction: "Co-1 sources document [claim]; sources cited: [list]." OR "Co-1 evidence from [sources] supports [claim]."

> Example (DEM): "Co-1 sources document a population-level preference for matte over glossy surfaces in dementia-primary residential and care settings; sources cited: *DSDC EADDAT* (Stirling 2022); *Dignified Design 22 Elements* (Stirling 2024); *NDTi/NHS CAMHS environment study* (2022, contingent verification)."

> Example (DEAF): "Co-1 sources converge on visual environments calibrated for sustained ASL conversation: matte mid-tone wall surfaces against skin, diffuse shadow-free lighting at face height, and U-shaped or semicircular movable seating for sightline equity. Sources: *DSDG* (Gallaudet 2010); *DeafScape* (Vaughn 2018); *Kusters Deaf Space in Adamorobe* (Gallaudet UP 2015)."

**Pattern Co-1-C — Tier 1 / Co-1 convergence.**

Use when Tier 1 OT clinical research and Co-1 evidence converge on the same value or finding. Treats convergence as itself evidence per mission §3.

> Construction: "Tier 1 OT evidence ([sources]) and Co-1 sources ([sources]) converge on [claim]."

> Example: "Tier 1 OT evidence (Murgia 2023; Iglehart 2020 SR) and Co-1 sources (*DSDG* Gallaudet 2010; *PVA Accessible Home Design* 2021) converge on reverberation time RT60 ≤0.6 s for shared-use teaching spaces serving DEAF and HoH populations."

**Pattern Co-1-D — Tier 1 / Co-1 divergence.**

Use when Tier 1 and Co-1 diverge on a parameter. Per mission §3, both are presented; divergence is documented; synthesis approach is specified per parameter.

> Construction: "Tier 1 OT evidence ([source]) shows [finding-1]. Co-1 sources ([sources]) document [finding-2]. The Tier 1 design range encompasses both: [range]. [Synthesis approach.]"

> Example: "Tier 1 OT evidence (Smith 2022 SR on threshold-height-and-fall-risk) supports threshold height ≤ 6 mm. Co-1 sources (*Concrete Change* 1987 visitability framework; *PVA Accessible Home Design* 2021; *Habinteg IHDG* 2024) document zero-step preference at primary residential entrances, framed by visitability advocacy and aging-in-place evidence over the building life-cycle. The Tier 1 design range is 0–6 mm. Population-informed default for residential primary entrances: 0 mm (zero-step), per the Co-1 visitability framework's broader claim that any threshold above zero forecloses a substantial population from entering. The 6 mm Tier 1 OT clinical maximum applies where structural constraints prevent zero-step."

### 5.2 What these patterns rule out

The four patterns work together to rule out the following voice failures:

| Failure pattern | Why it fails | Replace with |
|---|---|---|
| "Lived experience suggests..." | "Lived experience" with no source named is unfalsifiable and overclaims an undefined Co-1 voice | Pattern Co-1-A or Co-1-B with specific source(s) |
| "Disabled people prefer..." | Pre-launch, the guidebook has no methodology to claim what disabled people prefer in aggregate | Pattern Co-1-A or Co-1-B with specific Co-1-source-grounded claim |
| "Studies have shown..." (with no tier or source) | Generic citation hides whether the basis is Tier 1, Co-1, or other | Tier-located construction per voice-style §8.1 |
| "DSDG (Gallaudet 2010) confirms our recommendation..." | "Confirms" implies Co-1 source endorsement of the synthesis | Pattern Co-1-A: "DSDG (Gallaudet 2010) documents..." |
| "Co-1 evidence supports this guidebook's position that..." | Implies Co-1 endorsement of position rather than evidence basis | "Co-1 sources document [finding]; this guidebook's specification of [value] is based on [synthesis reasoning]" |
| Author-identity claims as Co-1 substitute | Per §3.3 (Q5), one disabled author is not Co-1 representation | Remove the identity-as-Co-1-substitute claim entirely |

### 5.3 Pattern selection decision rule

When drafting any specification cell or BPC entry that engages Co-1 evidence:

1. Is the claim drawn from one Co-1 source? → **Pattern Co-1-A.**
2. Is the claim the guidebook's synthesis across multiple Co-1 sources? → **Pattern Co-1-B.**
3. Does Tier 1 OT clinical research also bear on the claim, agreeing? → **Pattern Co-1-C.**
4. Does Tier 1 OT clinical research bear on the claim, disagreeing? → **Pattern Co-1-D.**

Apply in order. If multiple patterns apply, the one furthest down the list governs (Co-1-D > Co-1-C > Co-1-B > Co-1-A).

### 5.4 Voice-style skill update

This A5 specification updates `skills/voice-style_SKILL.md` §8.1 with the four Co-1 patterns above. Update is committed alongside this document. The voice-style skill is the operational instrument; this A5 specification is the doctrinal grounding.

---

## 6. Documentation requirements per Co-1 citation

This section formalizes the obligations from §3.4 (Q3) into a concrete documentation specification for every Co-1 citation in the guidebook.

### 6.1 Required fields per Co-1 citation

Every Co-1 citation in the corpus carries (in the underlying evidence record, even if not all are surfaced inline):

| Field | Source | Required values |
|---|---|---|
| `ref_id` | Project-assigned | `Co1-NN` format per `references/co1-verified-sources.json` |
| `tier` | Schema | `1` |
| `evidence_type` | Schema | `co1` |
| `co1_provenance` | Schema (new, per A5) | `published_corpus` (pre-launch all) or `participatory_synthesis` (post-launch contingent) |
| `co1_source_type` | A5-defined | One of: `peer_reviewed_literature`, `dpo_research`, `advocacy_position`, `academic_narrative`, `validated_tool` |
| `verification_status` | Per 2026-04-23 verification report | `VERIFIED`, `VERIFIED-WITH-CORRECTION`, `UNVERIFIED-1`, `UNVERIFIED-CLOSED`, `CLOSED-DELETED` |
| `authors` | Source | Full attribution |
| `year` | Source | Publication year |
| `title` | Source | Full title |
| `publisher_or_journal` | Source | Publisher or journal name |
| `doi_or_url` | Source | DOI preferred; URL fallback |
| `population_codes` | Project synthesis | List of MOB/VIS/DEAF/etc. that the source supports |
| `parameters_supported` | Project synthesis | List of design parameters drawing on this source |
| `synthesis_attribution_required` | Project synthesis | Boolean: true if Tier 2 obligation per §3.4 applies (substantial synthesis) |

### 6.2 Inline-rendered fields per citation context

Not all underlying fields surface in every citation. Three contexts:

**Inline text citation (prose):** Authors, year, title (short form). Example: "*DSDG* (Gallaudet 2010)."

**Specification table citation:** Author/source code + tier marker. Example: `EN (DSDG, Gallaudet POE) | Co-1`. (This is the format already in use in `references/bpc/DEAF.md`.)

**Bibliography entry:** All fields surfaced.

### 6.3 Validation

Post-A6 evidence-state validator (per A6 governance + code phase) should:

- Reject any citation lacking required schema fields
- Flag citations with `verification_status: UNVERIFIED-1` for re-search
- Block migration of cells whose only Co-1 source is `UNVERIFIED-CLOSED` or `CLOSED-DELETED`
- Surface `synthesis_attribution_required: true` cells for editorial review of front-matter attribution

This is a B2 / A6 implementation specification; the rules are stated here so A6 design has explicit Co-1 requirements as input.

---

## 7. Schema implications and pointers to B1

This section consolidates schema implications surfaced across §§3–6 as a pointer document for B1 (storage form decision and schema design).

### 7.1 Required EvidenceSource entity fields

Per §6.1, the EvidenceSource entity (already specified at A3 conceptual model level) requires the following fields to support Co-1 evidence handling:

| Field | Type | Source phase | Notes |
|---|---|---|---|
| `tier` | int 1–6 | A3 (existing) | Unchanged |
| `evidence_type` | enum | T-03 (Stage 0.5) | Unchanged; values include `co1` |
| `co1_provenance` | enum | **A5 (new)** | `published_corpus` or `participatory_synthesis` |
| `co1_source_type` | enum | **A5 (new)** | `peer_reviewed_literature`, `dpo_research`, `advocacy_position`, `academic_narrative`, `validated_tool` |
| `verification_status` | enum | 2026-04-23 verification | `VERIFIED`, `VERIFIED-WITH-CORRECTION`, `UNVERIFIED-1`, `UNVERIFIED-CLOSED`, `CLOSED-DELETED` |
| `synthesis_attribution_required` | bool | A5 (new) | Per Tier 2 obligation §3.4 |

B1 schema design integrates these as part of the EvidenceSource specification. No new entity is required; these are EvidenceSource fields.

### 7.2 Required EvidenceSource methods (B2 validator-time)

Per §6.3, validator behavior:

- Schema-level: required-field check on all six A5-affected fields above
- Cross-entity: parameter cells citing Co-1 sources must verify `verification_status ∈ {VERIFIED, VERIFIED-WITH-CORRECTION}`
- State-machine integration: cells with only `UNVERIFIED-CLOSED` or `CLOSED-DELETED` Co-1 sources route to T-04 `pending` state

### 7.3 Voice-style skill integration

Per §5.4, voice-style §8.1 is updated with the four Co-1 voice patterns. This is a parallel deliverable to this document, committed alongside.

### 7.4 Audience-priority and CS5 integration

Per §3.3 (Q5), audience-priority "disabled people" and Co-1 evidence are operationally linked but definitionally distinct. CS5 corpus-representation monitoring (§4.2) operates on Co-1 evidence; audience-priority representation-checking (per `governance/audience-priority.md`) operates on the rendered guidebook prose. Both are operative pre-launch; both feed gap-register entries; both inform synthesis quality. Their distinction is preserved in this document and should be preserved in B1 schema (separate fields, separate gap-register categorization).

### 7.5 A6 evidence methodology dependencies

A6 (next governance+code phase) operationalizes T-03 + T-04 in the evidence-state validator. A6 must:

- Implement the four Co-1 voice patterns from §5 as voice-validator checks (Pattern Co-1-A through Co-1-D detection)
- Enforce required EvidenceSource fields per §6.1 + §7.1
- Integrate `co1_provenance` into the evidence-state machine (cells with `participatory_synthesis` flagged separately, post-launch only)

A6 inherits this A5 specification as a binding input.

---

## 8. Sections deferred — none

All §§4–7 deferred at end of Session 1 are now resolved. Q3 and Q4 resolutions in §§3.4–3.5 are complete. No work is deferred to Session 3.

## 9. Cross-stage impact (updated for Session 2 closure)

| Thread | Effect of A5 closure |
|---|---|
| **CS2** (Co-1 recruitment) | Specification COMPLETE — INOPERATIVE pre-launch with three-trigger activation specification (§4.1). |
| **CS5** (Co-1 representation monitoring) | Specification COMPLETE — pre-launch corpus-representation monitoring form fully specified (§4.2); post-launch expansion form documented. |
| **CS8** (Decision capture) | Five substantive resolutions (Q1–Q5) captured per §§3.1–3.5 with [CONFIDENCE] flags. CS8 LIVE from A12 will retro-format these per protocol; provisional capture is sufficient for now. |
| **CS4** (Re-issue cadence) | A5 closure does not trigger synthesis re-issue. Full Stage A close (post-A13) does. |
| **B1** (schema design) | Six new EvidenceSource fields specified (§7.1) as binding input to B1 schema design. |
| **A6** (evidence methodology — next phase) | Voice-validator pattern specifications (§5), required-field rules (§6.1, §7.1), state-machine integration (§7.5) carried forward as binding input. |
| **A11** (legal and regulatory framework) | Q3 Tier 3 obligation §3.4(7) — post-launch Co-1 source notification protocols — flagged for A11 + counsel review. Not deferred within A5; resolved here as a forward-pointer. |


---

## 10. Status

CANONICAL — A5 complete (Session 2 of 2; no Session 3 needed).

| Field | Value |
|---|---|
| Created | 2026-04-29 14:30 UTC (Session 1) |
| Closed | 2026-04-29 15:50 UTC (Session 2) |
| Phase | Stage A Phase 5 (Co-1 operational specification) — COMPLETE |
| Sessions consumed | 2 of 2–3 budget (Amendment 7 revised) |
| Status | CANONICAL — locked at this commit |
| Author | Project owner (solo, pre-launch) |
| Doctrinal anchor | D-03 revised (`pre-stage-a-decisions.md`) + Amendment 7 + Mission §3, §Operational reality, §Epistemic commitments + project-standards 2026-04-26 03:45 |
| Companion governance | `governance/mission-and-epistemics.md` (canonical) · `governance/audience-priority.md` (canonical) · `governance/pre-stage-a-decisions.md` |
| Resolves Q's | Q1 (representation honesty); Q2 (CS2/CS5 pre-launch substitute); Q3 (attribution/disclosure); Q4 (Co-1 ↔ Three-Tier interaction); Q5 (audience ↔ Co-1 distinction) — all five resolved |
| Forward dependencies | A6 evidence methodology (binding input from §§5, 6.1, 7.5); B1 schema design (binding input from §7.1); A11 legal/regulatory (forward pointer from §3.4 Tier 3 §7) |

**Next phase entry condition:** A6 starts with this document, the existing T-03/T-04 specifications, and `governance/mission-and-epistemics.md` §Epistemic commitments as binding doctrinal inputs.

---

**End of A5 governance document.**
