# Methodological Audit of the Accessible Built Environments Guidebook

**Auditor:** Claude (Sonnet 4.6 / interface-resolved)
**Date generated:** 2026-04-30 02:40 UTC
**Conversation context:** Four prior turns of evaluation, strategy, reconciliation, and self-review, consolidated and re-examined here.

**Source material read for this audit:**
- `references/project-standards.md` (full, 544 lines)
- `skills/workplan-orchestrator_SKILL.md` (full, 288 lines)
- `references/effort-guide.md` (full, 118 lines)
- `sessions/session_2026-04-29-a8-s1.md` (full)
- `gap_register.md` (filtered for OPEN P1 items)
- `references/connections/_index.md` (status summary + first 80 entries)

**Source material NOT read but relevant to several findings:**
governance/co1-operational.md, governance/evidence-methodology.md, governance/jurisdiction-philosophy.md, governance/population-taxonomy.md, skills/voice-style_SKILL.md, Part 1 prose, any Part 4 item specifications, Part 11 economics, any BPC files, any case study entries.

---

## 1. Scope and constraints

This document is an audit of project methodology by an AI assistant operating from doctrinal corpus only, without prose-level verification of how the doctrine is implemented in the guidebook's actual content. Findings about doctrine are direct. Findings about prose, operational practice, or downstream effects are inferential and labeled `[UNVERIFIED]`. The audit does not substitute for review by disabled people, OT clinicians, architects, code authorities, or disability studies academics. It is preparatory material for the project owner's governance decisions, not those decisions themselves.

Confidence calibration: medium for doctrinal findings. Low to medium for inferential findings about prose and operational practice. Findings about strategic choices (depth versus reach, niche versus population scale) are framings for the project owner, not conclusions about correctness.

## 2. The recursive problem

The audit replicates a core gap it identifies. A project on accessible design *for* disabled people has, for the duration of this audit, been evaluated *by* a non-disabled (or status-unknown) AI system. This is structurally identical to the project's acknowledged Co-1 participation gap. The audit's claim weight should reflect this. The strongest findings are those most directly grounded in published disability ethics scholarship; weaker findings rely on the auditor's substituted judgment. Where this distinction matters, it is noted in the relevant section.

This problem is named here because it cannot be neutralised by acknowledgement alone. Its only real correction is external review by the people the project nominally serves. See §7.

---

## 3. Consolidated findings

### 3.1 Doctrine-level strengths

**Evidence stratification.** Seven-tier hierarchy with Co-1 (lived experience) elevated to co-primary alongside Tier 1 OT clinical RCTs; codes demoted to Tier 6 floor. The explicit rejection of code-consensus as best practice is the most consequential single methodological move in the doctrine. The treatment of code minima as "informative where nothing else can be" rather than as gold standards is uncommon in the field.

**Three-tier design hierarchy.** Universal Mode universal/code, Tier 1 inclusive ranges with median default, Mode S OT-and-individual co-design. The explicit modeling of the bridge between population-level data and individual variation is uncommon. The "range = bridge between Tier 1 and Tier 2, not expression of uncertainty" rule is a real correction of a common ambiguity in design specifications.

**Anti-essentialism in doctrine.** Population codes "step aside at Tier 2" because a person is not defined by their disabilities. Compound-functioning rule (≈16% per added condition; non-additive interactions). Variable-conflation Step 0 check before asserting cross-population conflicts. These are correctives to the field's pairwise-population framing, present at the doctrinal level.

**Cultural transferability discipline.** Splitting PAS 6463 sensory specifications into physics-based (universal) versus spatial-model (individualist, doesn't transfer to collectivist contexts) shows engagement with the Kawa framework rather than name-checking. Recognising that ISO wayfinding standards transfer universally while implementation does not is a similar move.

**Authority modesty.** "Shall be" voice retired across the corpus because it implies authority the project does not have. Pre-launch operational reality rule (2026-04-26) explicitly disclaims solo-author production as a CRPD Art. 4.3 limitation rather than performing partnership it does not have. Hallucination audit conducted on own output (2026-04-09).

**Process discipline.** Validators in CI; schema co-production with governance; OID capture rule; batch-read protocol; "no jq" rule; prohibition on background curl processes. The engineering hygiene exceeds what most prose-led research projects sustain.

### 3.2 Weaknesses, ranked by ethical/epistemic weight

The list below consolidates and deduplicates issues raised across the four prior conversation turns.

**3.2.1 Co-primary lived-experience claim versus solo-author reality.** Doctrine treats Co-1 as co-primary with RCTs (CRPD Art. 4.3 framing). The 2026-04-26 rule honestly states that Co-1 is currently corpus-only — the author parses published lived-experience research rather than collaborates with disabled people directly. This is *representation* of Co-1, not *participation*. CRPD Art. 4.3 concerns decision-making power, not citation. The project names this gap. It does not close it. The gap is the project's largest unresolvable structural failure and may remain so at launch. Naming honestly is necessary; naming does not resolve.

**3.2.2 Single-population framing of "disabled people."** The doctrine's anti-essentialism is correct. The Co-1 stratification appears to treat each population code as a unitary voice, but communities have non-aligned positions: Deaf cultural-linguistic versus hard-of-hearing functional framing; autistic self-advocacy versus parent-advocacy in NDV; intellectual-disability self-advocate (People First, Inclusion International) resistance to subsumption under DEM and NDV; chronic-illness epistemology (PAIN, OFS) divergence from VIS/MOB framings. Whether sub-community stratification is tracked in the EvidenceSource schema is `[UNVERIFIED — requires governance/co1-operational.md and Co-1 source curation review]`.

**3.2.3 ICF retained without engagement of its critique.** Hughes & Paterson (1997), Shakespeare (2006, ch. 2), Mitra (2006), Imrie (2004) and others have substantial published critique of ICF as carrying residual individual-pathology framing despite biopsychosocial branding. The four-framework layering (ICF + PEO + Capability + Kawa) names ICF as taxonomy; the critique is absent. Importing ICF without engaging the critique imports its baked-in normativity (impairment as deviation from a typical body) into the corpus.

**3.2.4 Capability Approach version unspecified.** Sen (open-list, locally determined) and Nussbaum (fixed list of central capabilities) are operationally different commitments. The project's three-tier hierarchy aligns with Sen; Nussbaum would push toward Universal Mode universalism for a wider set of capabilities. The project should commit to Sen's version explicitly. This is a governance decision, not a literature-review decision.

**3.2.5 Disability justice framework not engaged.** Sins Invalid / Berne ten principles is the framework most directly critical of the professionalised infrastructure (codes, OT-centred Tier 2, expert specifications) the project relies on. The project is not incompatible with disability justice but does not name it. Where the project draws from it (intersectionality through compound functioning; cross-disability solidarity through unified hierarchy; refusal of generic ideal) and where it diverges (reliance on professional gatekeeping; potential commercial-development use cases) should be stated openly.

**3.2.6 Tier 2 geographic contingency.** The Tier 2 mechanism assumes OT availability — a Northern, professionalised assumption. In jurisdictions without an OT workforce (most of the Global South), Tier 2 is structurally unavailable. The formal/informal city divide rule acknowledges scope; the OT-availability divide is the same problem one layer in and is not similarly named.

**3.2.7 IntD proxying as research-system limitation.** Subsuming intellectual disability through DEM (cognitive) and NDV (sensory) reduces IntD to a sum of features. Self-advocate organisations resist exactly that subsumption. The early-close exception ("literature confirmed absent in non-English") is epistemically defensible but ethically uncomfortable for the population most systematically excluded from research production. The framing should name this as a research-system gap, not as a settled finding about the population.

**3.2.8 Disabled people as readers, not only as evidence sources.** Co-1 elevation handles them as evidence sources. Whether Part 1 addresses disabled people as primary readers — with use-case framing equivalent to whatever framing exists for architects, OTs, policymakers — is `[UNVERIFIED]`. Test: count direct second-person addresses by audience in Part 1. Asymmetry there is the symptom.

**3.2.9 BAR placement framing is bare in doctrine.** "Large body size is not a disability → Supplementary only" is contested in fat studies and weight-inclusive design literature. The doctrine states the position; the doctrine does not state the reasoning. If guidebook prose carries the argument, the framing is fine; if not, the rule reads as dismissal.

**3.2.10 Tier 2 visibility risk in prose.** Tier 2 carries the entire load of preventing Tier 1 medians from being read as final answers by time-pressured architects. The handoff lives in prose discipline, not in the data model. Whether the prose hands off vividly enough at the point of use is `[UNVERIFIED — requires Part 4 read]`. This is the project's central operational risk.

**3.2.11 Outstanding rigour debt.** GAP-079 (GRADE retrofit, ~125 specs across Part 4 + Part 7/8 matrices) and GAP-CITE-01 (citation tagging at 28%, 11 ORPHANED claims in Cat A alone) carry P1 status. Until both close, the document carries inconsistent evidence-quality flags and untraceable claims.

**3.2.12 Hallucination audit scope.** The 2026-04-09 audit caught quantified-claim fabrication (3 instances, fixed). The scope was narrow: hallucination risk extends to qualitative claim attribution, page-reference accuracy, drift between paraphrase and source. A second-pass audit on a different vector is warranted before launch.

**3.2.13 Artifact accessibility gap.** The guidebook is currently a markdown corpus on GitHub. Nothing in doctrine addresses screen-reader compatibility for any rendered version, plain-language summary, alternative formats (audio, braille, large-print PDF), Easy Read summary, sensory accessibility of figures and plans, or translation policy. For a project on accessibility, this is the largest standing ethics gap.

**3.2.14 No external ethics gate.** Solo synthesis of published material does not formally require IRB review. For a project aspiring to influence built environment practice for disabled people, the absence of any external methodological review (advisory committee, peer review, DPO sign-off, ethics consultation) scales badly with reach.

**3.2.15 Path-to-impact unstated.** The Core Doctrine asserts a population-scale claim ("raise the floor of understanding for everyone who touches the built environment"). The artifact as architected — multi-tier, evidence-stratified, training-cost-heavy — serves a niche of expert practitioners. The two cannot coexist without an explicit theory of change. The plausible realistic strategy is influence-vector (educators, code-development cycles, DPO advocacy) plus optional digest layer, with the depth corpus as primary deliverable. The choice has not been named.

### 3.3 Reconciliation across stakeholders

The project's reconciliation moves are real and largely sound at the doctrinal level:

- **Three-tier hierarchy** mediates architects/policymakers (Universal Mode = code) and OTs/disabled people (Tier 2 = co-design); Tier 1 negotiates the middle.
- **Voice rule (2026-04-26)** retires "shall be" and locates authority by tier: code at Universal Mode, evidence at Tier 1, OT and individual at Tier 2.
- **Co-1 elevation** to co-primary with Tier 1 RCTs treats lived experience as primary evidence.
- **"Population codes step aside at Tier 2"** refuses essentialist reduction.
- **"Advocacy project, not authority"** disclaims displacement of architect, OT, or policymaker professional roles.

Where reconciliation breaks down:

The architect time-pressure problem is unresolved. Tier 1 medians can be applied as final values without invoking Tier 2; the prevention lives in prose discipline only.

The policymaker authority signal is suppressed by doctrine. The path to code modernisation is not named.

OT primacy in Tier 2 is vulnerable to disability-studies critique not engaged in doctrine.

Disabled people are addressed as evidence sources well; whether they are addressed as readers is `[UNVERIFIED]`.

Solo-author Co-1 corpus is not symmetric with the institutional representation of architects, OTs, and policymakers in the source corpus.

**The four-perspective frame used in earlier turns of this audit is itself a methodological shortcut.** The actual stakeholder set is wider:
- engineers (Part 8)
- specialist consultants (Part 9)
- code authorities (distinct from policymakers — they implement, do not write)
- DPOs as institutional voices (distinct from individual disabled people)
- carers, family, paid support workers
- building owners, facility managers, contractors, inspectors
- design educators and students
- future disabled people (a typical demographic projection puts this near 70%+ of any general population over a lifetime, factoring acquired disability and ageing)

The audit's earlier narrowing was convenient and reproduced the failure mode it nominally critiqued.

### 3.4 Three lenses

**Repository as medium.** A repository is a fixed artifact that gets queried. The Core Doctrine asserts the document is question-asking. The data structure (BPC files, item codes, validators, schemas) trends toward database. The Mode S handoff is the bridge — the repository prepares the question; the responsive resolution happens in the room with the OT and the person. The repository is appropriate to its mission *if and only if* the prose consistently surfaces the Mode S handoff at the point of use, not only in front matter.

The medium also raises sustained-artifact concerns: decay (a 2026 evidence synthesis needs review by 2028–2030); maintenance ownership (solo-author production scales poorly to revision cycles); discoverability (a markdown corpus on GitHub is not findable through architectural design tools, OT clinical references, code-authority resources, or general web search by typical users); citation (DOI assignment, version-tagged permalinks); license and forking (CC-BY-SA-4.0 or equivalent governs whether jurisdictional adaptations and translations can exist); accessibility of the rendering itself (see §3.2.13). None of these are addressed in doctrine.

**Capability approach.** Sen's open-list version maps cleanly onto Tier 1 ranges + Tier 2 individual resolution. *Conversion factors* are engaged through harm-asymmetry and compound-functioning rules. *Adaptive preference* (disabled people having adapted to inaccessible environments may underestimate need when asked) is partially handled by Tier 1 RCT + Co-1 dual evidence base but not discussed explicitly. *Threshold capabilities* map to Universal Mode as code-floor.

The biggest capability-approach gap: the project taxonomy is environment-organised (Categories A–K, room types R-) rather than capability-organised (capability-to-bathe, capability-to-leave-home-unaccompanied, capability-to-host-family, capability-to-work-from-home). A capability-axis cross-cut over the existing taxonomy would close this. The Connection Register has the raw material.

**Ethics, multi-framework.**
- *Procedural ethics* (CRPD Art. 4.3): partially honored, gap acknowledged.
- *Recognition ethics*: Co-1 elevation is good.
- *Distributive ethics* (who pays): lives in Part 11, not read for this audit.
- *Epistemic ethics*: verification, hallucination audit, citation tagging — strong process.
- *Disability justice* (Sins Invalid / Berne): not engaged.
- *Care ethics* (Kittay, Tronto — relational, dependency, carer labour): partially engaged through "adjustable is not universal" rule with population operability notes; carer space and dignity of carer presence not visible.
- *Crip theory* (McRuer, Kafer — non-normative time, non-productive body): implicitly engaged through OFS recognition.
- *Procedural justice* (Rawls): the harm-asymmetry rule could be read as Rawlsian maximin; not named.
- *Communitarian ethics* (MacIntyre, Sandel): the Kawa rule on collectivist-context shared-calm is implicitly communitarian.
- *Indigenous ethical frameworks*: not visible in any jurisdiction's treatment.
- *Casuistry / virtue ethics*: Tier 2 mechanism is structurally casuistic.

The largest standing ethics gap remains §3.2.13 — accessibility of the artifact itself.

---

## 4. Self-audit of the audit

### 4.1 What the prior turns got right

- Disclosing uncertainty consistently with `[UNVERIFIED]` flags and `[CONFIDENCE]` markers.
- Identifying the artifact-accessibility ethics gap (turn 3, expanded in turn 4).
- Identifying the path-to-impact / niche-versus-reach strategic question (turn 4).
- Naming the recursive AI-auditor problem (turn 4).
- Identifying sub-population stratification of Co-1 as a gap (turn 4).
- Suggesting Sen's open-list capability-approach commitment (turn 2 onward).
- The capability-organised cross-cut proposal (turns 3 and 4).
- Engaging disability justice, care ethics, crip theory, communitarian, and indigenous frameworks (turn 4 only).

### 4.2 What the prior turns got wrong or weak

- **The "rating" was unjustified.** Letter grades and numerical scores (B+/8, B/7, B+/8) were assigned without a defensible benchmark or comparison set. "Above the field" is unverifiable claim by an auditor without access to a defined comparison field.
- **Mild flattery slipped through.** "Genuinely strong," "above the field," "uncommonly explicit," "unusually" appeared in turns 1–3. Tone discipline says zero flattery.
- **Treated "disabled people" as unitary in turns 1–3.** The doctrine's anti-essentialism was nominally respected and operationally violated. Corrected in turn 4 but the earlier reasoning remains in the conversation transcript.
- **Engaged only CRPD-flavoured ethics in turns 1–3.** Disability justice, care ethics, crip theory, communitarian, indigenous, and casuistry frameworks all appeared only in turn 4. The omission of disability justice in particular was glaring.
- **Many `[UNVERIFIED]` claims could have been verified.** Reading more files (Part 1 prose, governance documents, voice-style skill) was an option not exercised. Treating the doctrinal limit as fixed inflated unverified-claim rate.
- **Plan inflation across turns.** Turn 2 had 11 items in 3 tiers. Turn 4 had 21 items in 4 buckets. Some are duplicates renamed; some are legitimately new. The accumulation was not deduplicated.
- **Capability-approach analysis thin on conversion factors and adaptive preference.** Both named, neither traced into project specifics.
- **Did not propose external DPO review until turn 4.** This is the most obvious answer to both the recursive AI-auditor problem and the participatory ethics gap; it appeared late.
- **Confidence creep across turns.** Started with cautious flags; ended with a 21-item plan asserted as "the strategy." Plan items are framings for the project owner, not conclusions by the auditor.

### 4.3 What the audit did not address

- Whether the Connection Register's pattern of CONSUMED entries (140 of 181) reflects rigorous synthesis or premature closure. Cannot assess from index scan alone.
- Whether the GRADE methodology used in Part 4 (90/90 items rated) was applied consistently and at appropriate confidence levels. Requires reading rated entries.
- Whether the 24-jurisdiction selection criteria actually achieve geographic and developmental diversity or reproduce existing accessibility-research geographic biases. Requires reading jurisdiction-philosophy.md.
- Whether licensing, citation, and revision-cadence commitments exist anywhere outside what was read.
- Whether Part 1 prose addresses disabled readers, names the four frameworks honestly, or engages the critique of any of them.
- Whether the project has any external review mechanism currently operating.
- Whether the Stage A timeline is realistic for the remaining governance phases (A9–A13) before content writing resumes.
- Comparison with other rigorous accessibility-research projects. The audit was self-referential.

---

## 5. Revised plan

Consolidated and deduplicated from prior turns. 12 items in 4 tiers.

### 5.1 Stage A governance (immediate; achievable in 4–6 sessions)

**G1. Path-to-impact governance phase.** State the project's theory of change. Niche depth + influence-vector (educators, code cycles, DPO advocacy) + optional digest layer. Refusing to choose locks in the implicit current path. Highest leverage of any item in this plan.

**G2. Stakeholder governance phase.** Map the actual reader/user set. Distinguish architects from engineers from contractors, OT clinicians from OT educators, policymakers from code authorities, disabled-people-as-Co-1-source from disabled-people-as-readers, DPOs, carers, students. State which are primary, secondary, out-of-scope.

**G3. Capability Approach version commitment.** Sen's open-list version. One paragraph + RULE + queued for Part 1.

**G4. ICF critique engagement.** Cite Hughes & Paterson 1997, Shakespeare 2006, Mitra 2006. State why ICF is retained operationally despite critique. RULE + queued for Part 1.

**G5. Disability justice engagement.** Name Sins Invalid / Berne framework. State where the project draws from it (intersectionality, cross-disability solidarity, refusal of generic ideal) and where it diverges (reliance on professional gatekeeping, possible commercial-development use cases). RULE + queued for Part 1.

**G6. Tier 2 geographic contingency.** State that where Mode S OT co-design is structurally unavailable, Tier 1 ranges remain in force with harm-asymmetry default. Equivalent in scope-honesty to the formal/informal city divide rule. RULE.

**G7. IntD proxying reframing.** Amend existing rule. Frame the early-close exception as research-system gap, not population fact. RULE amendment.

**G8. License, citation, versioning, revision-cadence governance.** CC-BY-SA-4.0 or equivalent; DOI commitment via Zenodo or institutional repository; stable canonical URL with version-specific permalinks; revision policy with cadence target. Governance document.

### 5.2 Phase B writing and content

**W1. Disabled reader address in Part 1.** Explicit second-person framing. Symmetric with whatever exists for architects, OTs, policymakers.

**W2. Capability-organised cross-cut.** A view layer over existing Categories A–K and room-type taxonomy: capability-to-bathe, capability-to-prepare-food, capability-to-leave-home, capability-to-work, capability-to-host-family. Maps to existing items. Could be Appendix E or a separate digest deliverable. Connection Register has the raw material.

**W3. Tier 2 visibility audit.** Read every Tier 1 specification in Part 4. Confirm Mode S handoff at point of use, not only in front matter. Add to voice-style skill as calibration test.

**W4. Artifact accessibility commitments.** WCAG 2.2 AA conformance for any web rendering. Plain-language version commitment (which Parts? which audience?). Alternative-format commitments (audio, large-print PDF, Easy Read summary, braille policy). Translation policy (which jurisdictions get full versus summary translations?). Governance + Phase B deliverable list.

**W5. GRADE retrofit completion.** ~125 specifications. Hard gate before launch.

**W6. Citation tagging completion.** ~918 PENDING claims. ORPHANED count to zero. Hard gate before launch.

**W7. Hallucination audit second pass.** Sample 20 qualitative claims; verify attribution to cited source. Different vector from the 2026-04-09 quantified-claims audit.

### 5.3 External pre-launch (cannot be done in sessions)

**E1. External methodology review.** Two or three reviewers from disability studies, OT, and architecture. Single review pass; or methodology paper submitted to a disability-studies journal as pre-launch publication.

**E2. DPO outreach for Co-1 representation.** Single-pass review by 2–3 DPOs from underrepresented communities (intellectual-disability self-advocates, Deaf cultural representatives, Global South DPOs). Documented review, attributable. Partial closure of the participatory ethics gap and of the recursive-auditor problem this document instantiates.

**E3. Workflow-integration scoping.** Identify 2–3 BIM library projects, OT clinical-reference projects, code-commentary databases that could embed or link the guidebook. Outreach. No commitment to build integrations; commitment to make them possible.

### 5.4 Strategic acknowledgments

**S1. Niche-depth strategic framing.** Doctrinally state that the project is optimised for depth and reaches mass audiences indirectly through educators, code cycles, and DPO advocacy. Refuses the implicit population-scale claim of the Core Doctrine while preserving the project's actual contribution.

**S2. Solo-author Co-1 gap as standing limitation.** Already named in the 2026-04-26 rule. The plan-level acknowledgement: this gap is the project's largest unresolvable structural failure and may remain unresolved at launch. Frame as the highest-priority post-launch work, contingent on resources.

---

## 6. Highest-leverage actions

In order:

1. **G1 (path-to-impact governance).** Without this, the rest of the plan is arbitrary fixes. With it, recommendations sort cleanly into depth-serving, reach-serving, and ethics-serving buckets.
2. **W4 (artifact accessibility commitments).** A guidebook on accessibility that is not itself accessible to disabled readers in their assistive-technology environments cannot survive scrutiny.
3. **E2 (DPO outreach).** Even a single-pass review by 2–3 DPOs from underrepresented communities partially closes the participatory ethics gap.
4. **G2 (stakeholder governance).** Allows every subsequent decision to be made with the actual user set in view rather than a four-perspective abstraction.
5. **W5 + W6 (GRADE + citation tagging completion).** Already P1 in gap register. Hard pre-launch gates.

The remaining items are real and worth doing. They are not what the project owner should attend to first.

---

## 7. Items requiring external review

This audit cannot validate the following without input from the named reviewers. Each is a question the auditor cannot answer.

- **Disabled-person review of doctrine and Part 1 prose.** Specifically: does the document address disabled people as readers? Does the framing of population codes feel respectful or reductive at point of use? Is the Mode S handoff vivid in prose? Does the prose serve disabled readers or use them?
- **OT clinician review of Tier 2 mechanism.** Does the workflow assumption (architect → OT consultation → individual co-design) match how OT environmental modification actually happens in practice, or does it project a workflow that does not exist for most clients?
- **Architect review of usability at design moment.** Is the document usable in practice or only in theory? What digest or reference layer would make it usable at design moment?
- **Policymaker / code authority review of authority signal.** Does the "advocacy not authority" framing serve their roles or obstruct them? What signal would help code-development cycles incorporate the document's findings?
- **Disability studies academic review of ICF retention, OT primacy, and reliance on professionalised infrastructure.** Does the project's set of strategic choices survive critical scrutiny from the field most likely to push back?
- **Sub-community review across Deaf cultural-linguistic, autistic self-advocacy, intellectual-disability self-advocacy, and chronic-illness epistemology.** Are these communities treated symmetrically? Are their distinct positions visible? Do they recognise themselves in the document?

This audit's claims about each of these are inferential. Their validation requires the reviewers, not the auditor. None of the recommendations in §5 should be treated as final without external input on §7.

---

## Appendix A: Material read for this audit

| File | Extent | Notes |
|---|---|---|
| `references/project-standards.md` | Full (544 lines) | Core doctrinal source |
| `skills/workplan-orchestrator_SKILL.md` | Full (288 lines) | Workflow architecture, model assignment, skill index |
| `references/effort-guide.md` | Full (118 lines) | Effort calibration for skill assignments |
| `sessions/session_2026-04-29-a8-s1.md` | Full | Most recent session state |
| `gap_register.md` | P1 OPEN filter + first 30 lines | Rigour debt tracking |
| `references/connections/_index.md` | Status summary + first 80 entries | Cross-cutting connections register |

## Appendix B: Material not read but probably consequential

| File / scope | Likely impact on audit |
|---|---|
| `governance/co1-operational.md` | §3.2.2 (sub-population stratification): could partly resolve |
| `governance/evidence-methodology.md` | §3.2.4 (Capability version), §3.2.10 (Tier 2 visibility): could affect framing |
| `governance/jurisdiction-philosophy.md` | §3.2.6 (Tier 2 geographic contingency): could affect framing |
| `governance/population-taxonomy.md` | §3.2.7 (IntD framing): could partly resolve |
| `skills/voice-style_SKILL.md` | §3.2.10 (Tier 2 visibility), §3.2.8 (disabled reader address): high relevance |
| Part 1 prose | §3.2.8 (disabled reader address), §3.2.3 (ICF critique), §3.2.5 (disability justice): direct verification |
| Part 4 item specifications (sample) | §3.2.10 (Tier 2 visibility): direct verification |
| Part 11 economics | §3.4 (distributive ethics): direct verification |
| Any BPC files (sample) | Research synthesis quality across the corpus |
| Any case study entries | What "documented accessible built environment" means in practice |
| Stage A governance documents (A2 throughline, A3 entities, A6, A7, A8) | Several findings could be tightened or loosened |

A second-pass audit reading these would tighten or loosen many findings above. The largest shifts would likely be in §3.2.8, §3.2.10, §3.2.13.

---

*End of document. Audit produced for project owner's use; not authoritative; subject to external review per §7.*
