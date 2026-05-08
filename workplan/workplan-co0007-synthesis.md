<!-- DEPRECATED 2026-05-08 04:16 -->
> **⚠ DEPRECATED:** SUPERSEDED — Stage 0 work product. Findings incorporated into workplan-co0007-v4.md. Historical reference only.

# CO-0007 Synthesis: Mission, Throughlines, and Workplan
**Created:** 2026-04-25 00:14
**Status:** SYNTHESIS DOCUMENT — produced for your decision; not auto-committed
**Source:** Conversation 2026-04-24 covering bathroom turning space → BPC consensus error → population non-uniformity → questions vs prescriptions → architectural shift → multi-modal navigation → exhaustive critique
**Methodology note:** This document was produced from a long conversation state. Per my own prior critique, foundational decisions of this magnitude are better made in fresh Opus context. You requested it anyway. I have applied the critique's lessons to mitigate the risk, but you should treat this as a draft for review, not a final architecture.

---

## Part I: Multi-Perspective Analysis

### Top-down (mission → atoms)

The project exists to **improve accessibility outcomes in the built environment by changing how people who shape those environments think.** Everything else serves this. From this top-level purpose, five Core Doctrine principles operationalize the mission. From those principles, a strategic stance emerges: build a structured knowledge resource that supports multiple navigation modes and embeds questions, variability, co-occurrence, evidence-tier transparency, and tier handoffs at every level. From that strategy, an architectural form follows: graph-shaped data with rendering layers, atomic entities with explicit relationships, version-aware. From that form, atomic data populate the resource: parameters, populations, sub-population variations, evidence sources, jurisdictions, items, rooms, conflicts, questions, specialist handoffs, design stages.

The chain only works in this direction. Reading from atoms upward (which is what most accessibility resources do — they collect numbers and let the reader figure out the rest) loses the mission. The data architecture must reflect the mission shape, not the convenience of any particular medium.

### Bottom-up (existing artifacts → what they imply)

The project has accumulated approximately 280 commits of substantive work: 78 BPC files (synthesised research per topic-population), 90 search-log files (with multilingual + jurisdictional coverage), 92 Part 4 item specifications, 73 spec-database records, 20 Appendix A jurisdiction comparison tables, a standards registry covering 46 jurisdictions, a CRPD ratification map, a bibliography of approximately 557 sources (94% verified), a connection register of 189 entries, six tier-by-tier verification reports, and an Opus divergence synthesis covering 13 parameters at the doctrinal level.

What this corpus actually contains is **research output with a partly-contaminated synthesis layer.** The contamination is the consensus-as-best-practice error identified this session. The underlying research data — actual jurisdictional values, actual evidence chains, actual lived-experience accounts, actual jurisdictional spread — is largely sound. The synthesis decisions made on top of that data are what need re-examination.

What the corpus implies about the next form: the atomic entities are not stipulated, they are **emergent**. The data already organizes around parameters (turning space, threshold height, illuminance), evidence sources, jurisdictions, populations, conflicts, and connections. These entities exist in the markdown — but as prose, with implicit relationships. The structured form's job is to make explicit what is currently implicit, not to invent new entity types.

The corpus also reveals **specific structural inconsistencies the structured form would resolve**: turning space appears in eight or more Part 4 items, each as its own copy; threshold height is referenced inconsistently across E-06, E-12, and G-04; jurisdictional values appear in both Part 4 tables and Appendix A tables with potential drift; the same conflict resolution may live in Part 4 (item-level), Parts 6/7 (room-level), and Part 5 (building-level). Single-source-of-truth architecture eliminates this category of correction debt.

### Lateral (parallel concerns at same level)

At the **artifact level**, parallel structures with conceptual overlap include: Part 4 item specs ↔ Parts 6/7 room matrices ↔ Part 5 building-level conflicts (three views of the same conflict resolutions); Part 4 specs ↔ spec-database (two stores of parameter values); Part 4 jurisdiction tables ↔ Appendix A tables (two locations of comparison data); BPC best_practice_synthesis ↔ Part 4 description ↔ Opus divergence synthesis (three locations of synthesis claims).

At the **population level**, eleven canonical codes carry different epistemological foundations that the project has not surfaced. MOB is functionally defined. DEAF is culturally-linguistically and functionally defined. PAIN is symptomatically defined. OFS is a syndromic cluster (ME, POTS, MCAS) without a unifying mechanism. Treating these as a single taxonomy obscures real differences in how evidence applies, how Co-1 should be gathered, and how specifications should be framed.

At the **evidence level**, the seven-tier hierarchy compresses meaningfully different evidence types. Tier 1 OT clinical research and Tier 1 anthropometric research use different methods and produce different kinds of certainty. Co-1 lived experience as primary evidence and Co-1 as confirmation of clinical findings have different epistemic roles. Tier 4 international standards (ISO 21542) and Tier 6 statutory codes are both "standards" but carry very different evidence weight in our doctrine.

At the **jurisdiction level**, definitional inconsistency: 24 canonical jurisdictions per jurisdiction-tracker §4.7.3 versus 46 in standards registry. Tier A / Tier B Global South tiering overloads the "tier" terminology that already names the evidence hierarchy. CRPD signatory status is treated as discrete when implementation is continuous.

### Diagonal (cross-cutting relationships spanning levels)

**Mission ↔ atoms:** The "questions for the designer" requirement connects the highest-level mission directly to the lowest-level data atom. Every parameter, every population, every conflict must surface a question. This is the only relationship in the data model that traverses every level.

**Doctrine ↔ tooling:** Each Core Doctrine rule implies tooling. "Best practice ≠ code" implies the validator must check evidence-tier of values. "Populations not uniform" implies the schema must support within-population variability as first-class data. "Questions are primary" implies the rendering layer must be able to surface questions independently of values.

**Evidence tier ↔ skill methodology:** The skill that generates BPC must search for Tier 1–3 evidence FIRST, then code data. The current sequence places Tier 1 toward the end, which structurally biases synthesis toward code consensus.

**Audience ↔ navigation:** Each prioritized audience implies a navigation mode. Architect mid-project → item view. Architect at programming → population view. OT collaborating → conflict-resolution view. Disabled person reviewing the work → respect-visibility view (an unnamed mode that asks: "has anyone thought about people like me with the actual specificity of my experience?"). Policymaker → jurisdiction-comparison view with evidence-tier transparency.

**Population ↔ Co-1 representation:** The doctrine treats Co-1 as co-primary with Tier 1, but our actual Co-1 corpus is uneven across populations. Heavy on autism (NDV/AUT) and physical (MOB); light on PTSD (NDV/MH), MS (NEU), DBL. The structure must make this imbalance visible so it can be addressed methodically.

**Jurisdiction ↔ disability worldview:** Different jurisdictions encode different theories of disability. ADA = rights-based / non-discrimination framework. EU = standards-harmonization / market-access framework. Japan = barrier-free design / universal-design ideology. India = ICF-aligned framework. The structured form must capture worldview, not just numbers, because two jurisdictions can specify the same number for different reasons, and the reason is sometimes more useful than the number.

---

## Part II: Throughlines

Six consistent threads run through every layer of the analysis.

**T1: Specifications serve questions; questions serve people; people are not uniform.** The whole project is a chain from people back to specifications through questions. Reverse the chain and the project loses meaning. This is the master throughline; the others elaborate it.

**T2: Codes are the floor; evidence is the basis; experience is co-primary.** The seven-tier evidence hierarchy is the spine of the project. Wherever any artifact treats codes as authoritative, the spine is broken. Wherever Co-1 is treated as illustrative rather than co-primary, the spine is broken.

**T3: Single sources of truth resolve propagation problems.** Every place the same value lives in multiple files creates correction debt. Every place one source can be referenced by many views resolves it. This is true at the atom level (parameter values) and at the methodology level (a single voice rule referenced by every prose decision).

**T4: Three tiers describe the gradient of context-specificity.** Universal Mode = no person known (universal). Tier 1 = some context known (population). Tier 2 = full context known (person). The same parameter shows up at all three; what changes is what we can responsibly say about it at each level.

**T5: Co-occurrence is the norm.** Every artifact that handles populations one at a time fails the lived reality of users. The structured form must default to combinatorial views, not single-population views.

**T6: The guidebook teaches; it does not prescribe.** Authority comes from teaching well, not from being correct about every number. The product is the reader's improved capacity to think, not the data points the reader takes away.

---

## Part III: Meta-Throughlines

Seven patterns about the patterns themselves.

**M1: Data shape follows mission shape.** The mission is multi-modal (questions, populations, parameters, evidence, jurisdictions, design stages). The data must be multi-modal too. Any architecture that flattens this loses the mission. Markdown is single-modal. Hierarchical taxonomies are single-modal in different ways. Graph-shaped data with view-layer queries is the minimum form that matches the mission's multi-modality.

**M2: The product is questions; the medium is structured data; the rendering is human language.** All three layers must be present and aligned. Most accessibility resources have only the rendering. Codes have rendering plus implicit data. Design guides have rendering plus some data. A complete resource has questions as first-class entities, structured data as the medium, and human language as the surface.

**M3: Authority and humility coexist through method.** If you can show your evidence, your range, your variability, your gaps — you have both authority (this is what I know) and humility (I'm not pretending it's everything). The structured form makes this method visible by construction. Prose alone cannot reliably hold both.

**M4: The project is a teaching tool that must be teachable to itself.** Whatever methodology we develop must be applicable by the project to new evidence, new jurisdictions, new conditions, new design parameters as they emerge. If the methodology only works for the current snapshot, it's the wrong methodology. The tooling and skill set must be self-applying.

**M5: Co-1 is not an audit step; it is a co-author relationship.** Disabled people are not reviewers of the work; they are evidence sources whose evidence is co-primary with clinical research. The methodology must operationalize this in every workflow, not just in a review pass at the end.

**M6: The project's deepest commitment is epistemic.** It stakes itself on a theory of evidence (the seven-tier hierarchy with Co-1 co-primary) that is not universally accepted in architecture or in disability studies. Every critique of the project will eventually land here. The methodology must be defensible at the epistemic level, not just the operational level. Mission language must articulate why this evidence theory is the right one for this purpose.

**M7: Time is part of the data.** Codes change; evidence accumulates; populations get recognized (long COVID, post-acute sequelae, IntD reconsideration); jurisdictions adopt and supersede. Static representations break. Versioned representations with explicit temporal structure are the minimum viable form.

---

## Part IV: Mission Statement

> **The Accessible Built Environments Guidebook teaches people who shape the built environment to ask better questions about accessibility, depending on the circumstance. It does this by surfacing the considerations they might not otherwise encounter, the variability of human functional experience, the dynamics of co-occurring conditions, and the points where specialist input becomes essential. It is grounded in a seven-tier evidence hierarchy in which clinical research and lived experience are co-primary and codes are the floor. It defines best practice as the most accommodating, thoughtful, respectful, dignified, and usable condition the evidence supports. It is structured to be navigable by architects, occupational therapists, policymakers, and disabled people themselves, each entering the resource through the path most useful to their work. It does not prescribe. It teaches; the better the questions a designer carries into a project, the better the project will serve the people who use it.**

This statement is the test against which every methodological, architectural, and editorial decision must be evaluated.

---

## Part V: Comprehensive Workplan

### Workplan structure

The workplan has three macro-stages. Each stage gates the next; their outputs accumulate.

- **Stage A: Foundations.** Settle conceptual, audience, voice, evidence-methodology, and Co-1 questions. No content production. No schema lock-in. Produces decision documents that constrain everything downstream.

- **Stage B: Architecture and pilot.** Design schema and tooling. Build an end-to-end pilot covering one item, one room, one population concern. Validate that the structured form serves the mission. Iterate. Lock architecture.

- **Stage C: Migration and scaling.** Migrate existing artifacts into the structured form, simultaneously auditing them against Core Doctrine. Build out missing content. Run quality gates. Establish maintenance lifecycle.

Stages A and B together establish the foundation. Stage C is the bulk of the work.

The original 280-commit corpus is **input** to Stages B and C. Existing artifacts are not "fixed" or "patched"; they are migrated through a process that audits them as a byproduct.

---

### Stage A: Foundations
**Sessions:** 18–28
**Models:** Predominantly Opus; Sonnet for procedural support
**Output:** Five governance documents that bind all subsequent work

#### A1. Audience priority document
**Sessions:** 1–2 · **Model:** Opus

Produce explicit statement of primary, secondary, and tertiary audiences. For each, state typical entry path, decision-stage, information need, and risk if poorly served. State conflict-resolution rules where audiences' needs diverge (e.g., when does the architect's need for decisive answers override the disabled person's need for visible specificity?).

**Output:** `governance/audience-priority.md`
**Decision points:** You confirm the priority ordering and conflict-resolution rules.

#### A2. Mission articulation and project identity
**Sessions:** 1 · **Model:** Opus

Refine the mission statement above into a public-facing version (suitable for Part 1) and an internal version (suitable as governance test). State the project's epistemic commitments explicitly: why the seven-tier hierarchy, why Co-1 co-primary, why best-practice-as-dignified, why questions over prescriptions. These commitments are the project's defensible core; they must be articulated before they can be defended.

**Output:** `governance/mission-and-epistemics.md`
**Decision points:** You confirm or revise the epistemic commitments.

#### A3. Conceptual model
**Sessions:** 4–6 · **Model:** Opus

Settle definitions of all atomic entities and relationships:
- **Entities:** parameter, sub-parameter, population, sub-population variation, evidence claim, evidence source, jurisdiction, jurisdictional worldview, item, room/space, design stage, project type, conflict, question, specialist handoff, time-version
- **Relationships:** parameter↔population (with variability notes), parameter↔jurisdiction (with worldview), population↔Co-1 (with representativeness flag), item↔parameter (composition), room↔item (composition), conflict↔population-pair↔parameter, question↔(parameter|population|conflict|design-stage), specialist-handoff↔functional-trigger, claim↔evidence-source-with-tier
- **Governing rules:** what makes an entity atomic versus composite; what relationships are mandatory versus optional; what cardinality each relationship carries; how time-versioning works for each entity

This is the most consequential phase in Stage A. Every downstream decision references it.

**Output:** `governance/conceptual-model.md` (with diagrams)
**Decision points:** You approve the model. Disabled-user reviewer (per A5) reviews the population entity.

#### A4. Voice and framing resolution
**Sessions:** 2–3 · **Model:** Opus

Resolve the authority + humility tension in concrete prose. Method: write three full versions of the same parameter section in three different voices (e.g., textbook-authoritative; mentor-teaching; peer-discussing). Test each against the mission statement. Identify what works and what doesn't. Produce a consolidated voice rule that incorporates the working elements.

This work supersedes parts of voice-style_SKILL.md as it stands. The current voice skill predates the doctrinal shifts and may not survive the test.

**Output:** `governance/voice-and-framing.md`; revised `skills/voice-style_SKILL.md`
**Decision points:** You select among the worked drafts.

#### A5. Co-1 co-author relationship design
**Sessions:** 4–6 · **Model:** Opus + you

This phase operationalizes M5. Co-1 is treated as co-author, not reviewer. That means:
- Disabled people are recruited as project collaborators, not survey subjects
- Compensation, recognition, and decision authority must be defined
- Recruitment paths must be defined (DPOs to partner with; populations needing representation given current Co-1 imbalance)
- Decision-stage involvement (when in each session do co-authors weigh in?)
- Output review process distinct from clinical-evidence review
- Disagreement-handling protocol when Co-1 evidence and Tier 1 evidence conflict
- Specific representation goals across populations to address current Co-1 imbalance

This phase has practical, ethical, and resource implications and may require external advice. Outcome may be that the project as currently resourced cannot fully operationalize Co-1 co-authorship and must explicitly acknowledge a methodological limitation in mission language.

**Output:** `governance/co1-coauthor-relationship.md`
**Decision points:** You determine resource availability and accept any methodological limitations.

#### A6. Evidence methodology refinement
**Sessions:** 2–3 · **Model:** Opus

Refine the seven-tier hierarchy in light of the analysis above:
- Disambiguate within-tier evidence types (Tier 1 OT clinical vs Tier 1 anthropometric)
- State Co-1 epistemic role(s) explicitly (primary source vs confirmation of clinical findings)
- State evidence-applicability assessment criteria (when does a Tier 1 study with narrow population justify a generalization?)
- State conflict resolution between tiers (when Tier 1 and Co-1 disagree; when Tier 3 systematic review contradicts Tier 1 trial)
- State minimum search effort for declaring [RESEARCH-GAP]
- State temporal handling (when does evidence become stale?)

**Output:** `governance/evidence-methodology.md`; updates to project-standards.md
**Decision points:** You approve refinements; epistemic commitments from A2 must remain coherent.

#### A7. Population taxonomy refinement
**Sessions:** 2–3 · **Model:** Opus + Co-1

Address the lateral inconsistencies identified above. State explicitly what each population code represents (functional/cultural/symptomatic/syndromic), what its evidence base looks like, what within-population variability means for it, and what co-occurrence patterns are most important for it. Resolve sub-code inconsistencies. Resolve IntD proxying. Address emerging populations not yet captured (e.g., long COVID).

**Output:** `governance/population-taxonomy.md`; updates to project-standards.md
**Decision points:** You and Co-1 collaborators approve.

#### A8. Jurisdiction philosophy
**Sessions:** 1–2 · **Model:** Opus

State how the structured form treats jurisdictional differences. Capture that jurisdictions encode worldviews, not just numbers. Define how worldview is represented in data. Resolve the 24-vs-46 jurisdiction definitional inconsistency. Determine whether "Tier A / Tier B" Global South tiering survives or is replaced.

**Output:** `governance/jurisdiction-philosophy.md`
**Decision points:** You confirm.

**Stage A done criteria:**
- All eight governance documents committed
- Project standards updated to reference them
- No content work has been started on the new architecture

---

### Stage B: Architecture and Pilot
**Sessions:** 22–34
**Models:** Mixed; Opus for design, Sonnet for build, Co-1 for review
**Output:** Working pilot demonstrating end-to-end the structured form serves the mission better than current state

#### B1. Schema design
**Sessions:** 4–6 · **Model:** Opus

Translate the conceptual model (A3) into a concrete schema. Decisions:
- Storage form: graph database (Neo4j, TigerGraph, Neptune); RDF/JSON-LD with triplestore; structured markdown with explicit relationship markers; or hybrid
- Property structures for each entity
- Relationship types and properties
- Time-versioning approach
- Identity and uniqueness constraints
- Validation rules

The decision should optimize for: queryability for the navigation modes (B3), maintainability over years, alignment with the existing GitHub-based workflow (which constrains the technical surface).

Output is a schema specification AND a recommendation on storage form with rationale.

**Output:** `architecture/schema-spec.md`; `architecture/storage-decision.md`
**Decision points:** You select storage form. This decision has long-term implications (12+ years of project life).

#### B2. Tooling design
**Sessions:** 3–4 · **Model:** Opus + Sonnet

Specify the tools the project needs to operate on the schema:
- Validators (schema-aware, replacing or extending the markdown-aware validators)
- Query tools (for navigation modes)
- Rendering pipelines (to markdown, to web, to other forms)
- Migration tools (markdown → structured)
- Authoring helpers (replacing/extending the current skill set)
- Co-1 review interfaces (so Co-1 collaborators can review work in their preferred form)

For each tool, specify: build-or-buy, language/framework, integration with GitHub workflow, ownership.

**Output:** `architecture/tooling-spec.md`
**Decision points:** You approve build-or-buy decisions; resource allocation.

#### B3. Navigation mode specification
**Sessions:** 2–3 · **Model:** Opus + Co-1

For each prioritized audience (from A1), specify the navigation mode in detail:
- Entry points
- Faceted-filter dimensions
- Result structures
- Cross-navigation (how do you move from one mode to another mid-task?)
- Interactive features (population-checkbox-driven content per the conditional-content discussion this session)

The "respect-visibility view" for disabled-person readers needs particular care; it is a navigation mode that doesn't yet have analogues in existing accessibility resources, and the design should be Co-1-led.

**Output:** `architecture/navigation-modes.md`
**Decision points:** You and Co-1 approve.

#### B4. Pilot construction — content
**Sessions:** 6–8 · **Model:** Opus + Co-1

Build the structured-form content for a deliberately scoped pilot:
- One item: G-04 (Bathroom — Wet Room) — the case that triggered this entire conversation
- One room: Bathroom (containing G-04 plus all related items: G-03 grab bars, E-07 slip resistance, F-07 thermal, B-08 lighting, A-13 acoustics, etc.)
- One population concern: PTSD (NDV/MH) — chosen because Co-1 evidence is currently sparse, forcing the pilot to exercise the Co-1 co-author relationship from A5

For each, populate every entity type the schema supports. Surface every question the designer should ask. Include all functional variability, all co-occurrence relevant to scope, all jurisdictional overlay, all evidence with tier, all conflicts, all specialist handoffs.

**Output:** Populated schema instances for the pilot scope
**Decision points:** Co-1 approval at multiple checkpoints

#### B5. Pilot rendering
**Sessions:** 2–3 · **Model:** Sonnet

Render the pilot through every navigation mode (B3) AND in markdown form. Verify:
- Each navigation mode produces a coherent, useful result
- Markdown rendering is faithful to the structured source (no information loss)
- Cross-navigation between modes works
- Interactive features (e.g., population-checkbox-driven combination view) work

**Output:** Rendered pilot in all forms; identified rendering issues
**Decision points:** You inspect each rendering; identify gaps

#### B6. Pilot validation against mission
**Sessions:** 3–4 · **Model:** Opus + Co-1 + you (and ideally one practicing architect)

Validate the pilot against the mission statement. Test:
- Does the pilot help the reader ask better questions? (Specifically test with one architect at programming stage and one at design development stage)
- Does the pilot acknowledge non-uniformity visibly?
- Does the pilot differentiate Universal Mode/1/2 in ways that change the reader's behavior?
- Does the pilot ground best practice in evidence, not codes?
- Does the pilot meet the most-accommodating/dignified/usable standard? (Co-1 review is decisive here)
- Does the pilot allow each prioritized audience to do their work?

Identify what works and what fails. Iterate the architecture (back to B1–B3) if structural issues are found. Iterate the content (B4) if content issues are found.

**Output:** `architecture/pilot-validation-report.md`; iteration backlog if any
**Decision points:** You decide whether the architecture is locked or requires another iteration

#### B7. Architecture lock
**Sessions:** 1–2 · **Model:** Opus

Lock the architecture decisions. Update governance documents. Communicate the locked architecture to all skills, validators, and CI gates.

**Output:** `architecture/architecture-lock.md`; supersession notes for any prior architectural assumptions

**Stage B done criteria:**
- Pilot exists in structured form
- Pilot renders to all navigation modes
- Pilot passes Co-1 review
- Pilot validates against mission criteria
- Architecture is locked and governance updated

---

### Stage C: Migration and Scaling
**Sessions:** 140–200
**Models:** Mixed
**Output:** Complete project in structured form, with audit-as-byproduct

The honest scope: this is the bulk of the work. It is large because the mission is large and the existing corpus is substantial. Speed of execution depends on resource availability. Quality cannot be compromised.

#### C1. Migration tooling build
**Sessions:** 4–6 · **Model:** Sonnet

Build the tools specified in B2 that handle migration from existing markdown to structured form. Include automated extraction (where possible), manual-entry interfaces (where needed), validation (to ensure migration integrity), and rollback (in case migrations fail review).

**Output:** Migration tool suite

#### C2. Skill set rebuild
**Sessions:** 8–12 · **Model:** Sonnet + Opus

The current skill set (multilingual-research, ISW, evidence-auditor, connection-scout, FDR, etc.) was built for markdown-output workflows. Rebuild or substantially modify each so they:
- Output to the structured form, not markdown
- Apply the corrected evidence methodology (Tier 1–3 first, codes as overlay)
- Surface questions as first-class outputs
- Include functional variability and co-occurrence prompts
- Enforce the new voice rules
- Integrate Co-1 review at appropriate points

The skill set is approximately 40 skill files. Not all need rebuild; some need only modification. Triage the set, then execute.

**Output:** Rebuilt/modified skill files

#### C3. Migration of parameters
**Sessions:** 30–40 · **Model:** Sonnet + Opus + Co-1
Each parameter (turning space, threshold height, illuminance, RT60, etc.) is migrated independently. Migration combines: extraction of existing values from BPC, Part 4, Appendix A, spec database; consolidation into single source; tier verification; evidence chain reconstruction; functional variability narrative authoring; co-occurrence narrative authoring; question authoring; jurisdictional overlay with worldview annotation; specialist handoff identification; validation by Co-1; commit.

Estimated 60–80 atomic parameters in the corpus. Pace: approximately 2 parameters per session at 2-session daily rate. Some parameters are larger and slower (turning space, illuminance, force/torque); some are smaller and faster (specific lux values, specific dB values).

**Output:** Migrated parameter library

#### C4. Migration of populations
**Sessions:** 15–25 · **Model:** Opus + Co-1

For each population code: define the population entity, populate within-population variability, populate co-occurrence patterns, populate jurisdiction-specific worldview implications, identify Co-1 representation gaps for that population, identify population-specific questions that recur across parameters, identify specialist handoff patterns.

11 populations in the canonical set; pace dictated by Co-1 availability.

**Output:** Populated population entities

#### C5. Migration of items and rooms
**Sessions:** 30–45 · **Model:** Opus + Sonnet

Items and rooms become composed views over the parameter and population libraries. This phase verifies that compositions render correctly through all navigation modes. Where current items conflate distinct functional needs (the structural question raised in critique), the structured form decomposes them.

92 items + the room-set that compose them.

**Output:** Composed item and room views

#### C6. Migration of conflicts
**Sessions:** 25–40 · **Model:** Opus + Co-1

Conflicts as combinatorial entities are heavy work. Each population pair × each parameter where conflict actually arises requires evidence, harm-asymmetry analysis, and resolution. The combinatorial explosion (55 pairs × ~60 parameters = 3,300 potential entries) is mitigated by the fact that most pairs do not conflict for most parameters; estimated 200–400 actual conflict entries.

**Output:** Populated conflict entities

#### C7. Migration of evidence base
**Sessions:** 10–15 · **Model:** Sonnet

The 557-source bibliography becomes a structured evidence-source library. Each source is a discrete entity with full bibliographic metadata, tier classification, applicability notes (population, parameter scope, methodological strengths/weaknesses), and links to claims it supports. The verification work already complete (94% of sources verified across six tier reports) is preserved as input data.

**Output:** Structured evidence-source library

#### C8. Migration of jurisdictions
**Sessions:** 8–12 · **Model:** Sonnet + Opus

The 46-jurisdiction standards registry becomes a jurisdiction library with worldview annotations. Each jurisdiction's parameter overlays are linked to the jurisdiction entity. Temporal handling for code changes is operationalized.

**Output:** Structured jurisdiction library

#### C9. Cross-cutting prose migration (Parts 1–3, 5, 9, 10–12)
**Sessions:** 20–30 · **Model:** Opus

The prose-heavy parts of the document must be rewritten in the new voice (A4) and aligned with the new methodology. Part 1 establishes mission and approach. Part 2 catalogs populations. Part 3 describes methodology. Parts 5, 9, 10–12 cover building-level resolution, OT collaboration, supplementary topics. Each is a substantial editorial pass.

**Output:** Rewritten prose sections

#### C10. Quality gates and validation
**Sessions:** 5–8 · **Model:** Sonnet

Run schema validators on all migrated content. Run cross-reference resolvers. Run Co-1 representation checks. Run evidence-tier audits. Run navigation-mode rendering tests. Identify failures; route to appropriate skill for repair.

**Output:** Validation reports; repair backlog

#### C11. Maintenance lifecycle establishment
**Sessions:** 3–5 · **Model:** Opus

Define how the structured form is maintained going forward:
- New evidence ingestion process
- Code-change tracking
- New population recognition pathway
- Co-1 ongoing relationship management
- Skill set update protocol
- Versioning and release cadence
- Deprecation process

**Output:** `governance/maintenance-lifecycle.md`

**Stage C done criteria:**
- All atomic entities migrated and validated
- All composed views (items, rooms) rendering correctly
- All navigation modes operational
- Co-1 review complete across all populations
- Schema validators passing
- Maintenance lifecycle documented and exercised at least once

---

### Estimated total scope

| Stage | Sessions | Real-time at 2/day | Real-time at 1/day |
|---|---|---|---|
| A: Foundations | 18–28 | 9–14 days | 18–28 days |
| B: Architecture and pilot | 22–34 | 11–17 days | 22–34 days |
| C: Migration and scaling | 140–200 | 70–100 days | 140–200 days |
| **Total** | **180–262** | **~3–6 months at intensive pace** | **~6–11 months at sustained pace** |

In practice neither pace is realistic. Co-1 work has its own cadence (collaborator availability, review windows). Real-world projects of this scope typically run **12–18 months** when staffed appropriately, with significant work happening in parallel rather than serially.

---

### Decision points the workplan defers to you

- **A1 (audience):** Primary, secondary, tertiary; conflict-resolution rules
- **A2 (mission):** Public version language; epistemic commitment articulation
- **A3 (conceptual model):** All entity definitions and relationship rules
- **A4 (voice):** Selection among worked drafts
- **A5 (Co-1):** Resource and methodological limit decisions
- **A6 (evidence):** Refinement approvals
- **A7 (populations):** Taxonomy approval
- **A8 (jurisdictions):** Philosophy approval
- **B1 (schema):** Storage form
- **B2 (tooling):** Build vs buy
- **B6 (pilot validation):** Architecture lock vs iterate
- **C11 (maintenance):** Lifecycle approval

Plus all Co-1 collaborator decisions throughout, which are not yours to make alone.

---

### What is salvageable from existing work

**Fully reusable:** All research data (jurisdictional values, evidence sources verified, multilingual coverage, lived-experience accounts in Co-1 corpus). The 280+ commits represent real research that the structured form ingests.

**Reusable with adjustment:** Skill methodologies (the structure of multilingual-research, ISW, FDR remains valid; what changes is output target and synthesis logic). Validators (the CI/branch-protection paradigm remains; the validators themselves rewrite). Voice work (some current voice rules survive; others are superseded by A4).

**Superseded:** Best_practice_synthesis as currently written in many BPCs. Item specifications as currently written in Part 4. Appendix A tables as currently framed (they will be regenerated from the jurisdiction library). The prior CO-0007 audit workplan I drafted earlier this session.

**Open question:** voice-style_SKILL.md — survives or is rewritten depends on A4 outcome.

---

### Risks and mitigations

**Risk: scope optimism.** Mitigation: stage gating; if Stage A overruns budget, Stage B does not start.

**Risk: Co-1 collaborator unavailability.** Mitigation: A5 explicitly addresses this; if resourcing cannot support full Co-1 co-authorship, the project must declare the limitation in its mission language.

**Risk: schema lock-in too early.** Mitigation: pilot validation (B6) is designed to surface architectural problems before lock; iteration is permitted.

**Risk: existing work feels wasted, demoralizing momentum.** Mitigation: explicit "salvageable" framing above; the research data IS the foundation.

**Risk: the project becomes too large to finish.** Mitigation: each migrated parameter is independently usable; the project releases value incrementally rather than only at completion.

**Risk: this synthesis itself is wrong.** Mitigation: Stage A includes audience priority and mission articulation as explicit decision points; if those expose flaws in this synthesis, the workplan adapts before any irreversible work.

---

## Coda

This document does not commit anything. It is delivered for your review and decision.

The strongest single recommendation: **before adopting this workplan, sit with the mission statement (Part IV) for at least a day and test whether you actually believe it. If yes, the workplan follows. If you would qualify it or change it, the workplan must be redrafted from the qualified mission. Mission language in this domain is load-bearing for years of downstream work; it is worth getting right before scaling effort against it.**
