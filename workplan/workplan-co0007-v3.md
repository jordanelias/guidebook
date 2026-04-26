# CO-0007 Workplan v3
**Created:** 2026-04-25 05:00 UTC
**Model:** Opus 4.7
**Supersedes:** synthesis Part V (`co0007-synthesis-workplan-1.md`); workplan v2 (`co0007-workplan-2.md`)
**Audit basis:** `co0007-audit-2.md` (31 findings)
**Status:** WORKPLAN v3 — not committed; pre-adoption

---

## What changed from prior versions

**From workplan v2:** Stage 0.4 (Opus arbitration of Sonnet output) is removed — the v2 framing depended on a model-tier misclassification that audit v2 corrected. The Stage 0 structure is otherwise expanded to address newly-identified findings (contamination sampling, doctrinal pre-decisions). Stage B's pilot phase is expanded to multi-pilot per N-09. Stage B1 is reframed to derive architectural form rather than implement an asserted one (N-05). A5 is expanded to operational specification plus recruitment thread (N-06). A6 absorbs values-criteria assessment (N-02), sparse-evidence decision (T-04 promoted to Critical), and pedagogy literature engagement (N-08). A3 is expanded to include cross-cutting axis interactions (N-03 + T-06).

**From synthesis Part V:** Adds Stage 0 entirely; expands Stage A from 8 to 13 phases; merges A1 and A2 to resolve circularity; expands B4 pilot scope; adds C0 skill responsibility matrix; moves time-handling operations from C11-only to C1-onward; corrects budget arithmetic.

**Critical pre-Stage-A decisions identified (3):** Co-1 tier encoding (T-03), sparse-evidence behavior (T-04), Co-1 operational role (D-03). These shape the schema and validator design and cannot be deferred to within-Stage-A phases without architectural incoherence.

---

## Finding-resolution map

All 31 findings from audit v2 mapped to workplan elements.

| Finding | Severity | Resolved by |
|---|---|---|
| **T-01** Mission not committed | High | Stage 0.6 provisional commit; A1-A2 canonical |
| **T-02** Questions claim no rendering | High | B3 questions-led mode; C2 `questions-renderer`; C10 question-coverage gate |
| **T-03** Co-1 tier encoding under-specified | Medium | Stage 0.5 framing decision; A6 final; B1/B2 implementation |
| **T-04** Sparse-evidence behavior undefined | **Critical** | Stage 0.5 doctrinal pre-decision; A6 implementation |
| **T-05** Respect-visibility view exceeds audience | Medium | A1-A2 use-patterns within audiences |
| **T-06** Design-stage absent from skills | Medium | A3 cross-cutting axis; C2 stage-aware authoring requirement |
| **T-07** Entity list incomplete | High | A3 expanded inventory: + audience, Co-1 collaborator, best-practice claim, building type, sub-population, citation |
| **B-01** Quantitative claims unverified | High | Stage 0.2 verification |
| **B-03** Session protocol skipped | **Critical** | Stage 0.1 |
| **B-04** Skill scope asserted | High | Stage 0.3 inventory; C0 responsibility matrix |
| **B-05** 6% bibliography residual | Medium | C7 expanded scope: explicit disposition |
| **B-06** Long-context drift | Medium | A13 doctrine-recheck cadence; periodic fresh-context decision sessions |
| **L-01** Stage A header inconsistency | Low | Stage 0.7 synthesis re-issue |
| **L-02** Decision-point count diverges | Low | Stage 0.7 synthesis re-issue |
| **L-03** Skill internal coherence | Medium | C0 responsibility matrix |
| **L-04** Three version-aware requirements | Medium | A9 unified time model; B1 implements |
| **L-05** Model-routing inconsistency | Low | A12 standardized notation |
| **L-06** Budget arithmetic | Low | This document (Budget section below) |
| **L-07** A1→A2 circular | Medium | A1-A2 merged |
| **D-01** Questions traverse incompletely | High | Same as T-02 |
| **D-02** SSoT at edit but not read time | High | B5 rendering refresh policy; C2 `rendering-refresh-coordinator` |
| **D-03** Co-1 reviewer-shaped operationally | **Critical** | Stage 0.5 framing; A5 operational specification; phase tables show Drafting / Decision / Review per Co-1 role |
| **D-04** Epistemic defense doc-only | High | A6 `epistemic-defense` skill spec; C2 builds it; CS doctrine-recheck operates it |
| **D-05** Time-as-data deferred | High | A9 time model; C1 active from start of Stage C |
| **N-01** Pilot conflates failure modes | High | B4 multi-pilot strategy separates architecture validation from corpus testing |
| **N-02** Respectful/dignified non-evidence | Medium | A6 values-criteria assessment via Co-1 mechanism |
| **N-03** Project-type × design-stage | Medium | A3 cross-cutting axis interaction explicit |
| **N-04** T1 has no validator | Medium | B2 `variability-coverage` validator |
| **N-05** Architectural form asserted | High | B1 derives from ≥3 candidate forms |
| **N-06** A5 implausible session count | Medium | A5 reframed: operational spec + recruitment plan; recruitment is parallel cross-stage thread |
| **N-07** Salvage matrix qualitative | Medium | Stage 0.4 contamination sampling |
| **N-08** Questions-led pedagogy thin meta-evidence | High | A6 engages design-pedagogy literature; A1-A2 cites; B6 tests with practicing architects |
| **N-09** Single-pilot fragile | Medium | B4 multi-pilot |

All 31 findings have at least one mapped resolution.

---

## Stage 0 — Verification and decision freeze
**Sessions:** 8–12
**Output:** Verified factual base; pre-Stage-A doctrinal decisions; provisional mission; revised synthesis and roadmap

This stage exists because the audit found that all conversation artifacts cascade without ground anchor (B-01, B-03, B-04, N-07) and that three doctrinal decisions (T-03, T-04, D-03) shape downstream architecture and cannot be left to within-Stage-A phases.

### 0.1 Session protocol grounding · 1 session · *Resolves B-03*

Run PI Session Protocol with connector authorization. Read `sessions/LATEST`, `references/project-standards.md`, `skills/workplan-orchestrator_SKILL.md`. Read latest session file. Read `gap_register.md` filtered for OPEN P1. Reconcile against synthesis claims.

**Output:** `co0007-session-grounding-report.md`

### 0.2 Quantitative verification · 1–2 sessions · *Resolves B-01*

Verify each quantitative claim: 280 commits, 78 BPC files, 90 search-logs, 92 Part 4 specs, 73 spec-database records, 20 Appendix A tables, 46 jurisdictions, 557 sources / 94% verified, 189 connection register entries, 13 doctrinal-divergence parameters, 11 population codes, 60–80 atomic parameters, 55 population pairs.

**Output:** `co0007-quantitative-verification.md`

### 0.3 Skill inventory · 1 session · *Resolves B-04*

Enumerate `skills/` directory. Map each skill to NEW / REBUILT / MODIFIED / DEPRECATED status against the inventory proposed in safeguards analysis. Identify missing-but-named and present-but-unnamed.

**Output:** `co0007-skill-inventory.md`

### 0.4 Contamination sampling · 1–2 sessions · *Resolves N-07*

Sample N=15 BPC files. For each `best_practice_synthesis` field, classify against doctrine: code-driven consensus (contaminated), evidence-driven (clean), mixed. Estimate contamination ratio across the 78 BPC corpus. Result informs C-stage scope realism.

**Output:** `co0007-contamination-sample.md`

### 0.5 Pre-Stage-A doctrinal decisions · 2–3 sessions · *Resolves T-03, T-04, D-03*

Three decisions made before A1-A2 because they shape downstream architecture:

**T-03 framing — Co-1 tier encoding.** Decide how Co-1 is represented in evidence-claim records. Options: single `tier` field with Co-1 as Tier 1 marker; `tier` plus `evidence_type` taxonomy; Co-1 as separate dimension parallel to tier scale. Decision shapes A6 detail, B1 schema, B2 validator.

**T-04 — sparse-evidence behavior.** Decide what best practice means when Tier 1–3 clinical and Co-1 corpus are both sparse. Options: `[BEST-PRACTICE-PENDING]` marker with research-gap pointer; reduced-confidence best-practice category with rendering distinction; doctrinal silence on evidence-thin populations. Decision frames the doctrine's defensibility.

**D-03 — Co-1 operational role.** Decide whether Co-1 is operationally co-author or operationally reviewer. If co-author: A5 produces drafting-role specification; phase tables show Drafting role for Co-1 in C3, C4, C6 and elsewhere. If reviewer: mission language is updated to honesty before A1-A2.

This sub-phase is the audit's three Critical pre-adoption blockers, brought to a single decision-set freeze.

**Output:** `governance/pre-stage-a-decisions.md`

### 0.6 Provisional mission commit · 0.5 sessions · *Resolves T-01*

Per 0.5 outcomes, commit mission language as `governance/mission-PROVISIONAL.md` with version stamp. PROVISIONAL until A1-A2 canonical version. Synthesis Coda's "sit with mission ≥1 day" test now operates on this artifact.

### 0.7 Synthesis and roadmap re-issue · 1 session · *Resolves L-01, L-02*

Synthesis revised: corrects Stage A header (5 → 8); adds adoption decision; incorporates 0.2/0.4 quantitative corrections; reflects 0.5 doctrinal decisions. Issued as `co0007-synthesis-workplan-2.md`. Roadmap similarly: `co0007-roadmap-2.md`. Workplan also re-issued as v4 if Stage 0 findings invalidate parts of v3.

### 0.8 Repo strategy decision · 0.5 sessions

Decide between: continue in `jordanelias/guidebook` main; create `rebuild` branch; create dedicated repo; subdirectory. The audit recommends `rebuild` branch as defensible interim, with final decision deferrable to B1 storage-form decision. Document the decision and dependencies.

**Output:** `governance/repo-strategy.md`

### 0.9 Workplan adoption decision · 0.5 sessions

Decide whether workplan v3 (this document, possibly v4 after Stage 0 findings) is adopted as the path forward. Decision is informed by 0.1–0.8 outputs. If adopted, Stage A begins. If revised, workplan v5 issued.

### Stage 0 done criteria

- Live project state grounded
- Quantitative claims verified
- Current skill set inventoried
- Contamination ratio estimated
- Three Critical doctrinal decisions made
- Mission committed PROVISIONAL
- Synthesis and roadmap re-issued
- Repo strategy decided
- Workplan adopted (this version or revised)

If any criterion fails, Stage A does not start.

---

## Stage A — Foundations
**Sessions:** 25–37
**Output:** Thirteen governance documents binding all subsequent work; recruitment thread initiated

### A1-A2. Audience and mission iteration · 4–6 sessions · *Resolves L-07, T-01 canonical, T-05, partly N-08*
**Co-1 role:** Drafting on disabled-reader audience definition

Merged because A1 → A2 was circular: audience shapes mission; epistemic commitments shape audience priority. Single iterative phase produces both.

Tasks:
- Audience priority (primary, secondary, tertiary) with conflict-resolution rules
- **Use-patterns within audiences** (T-05): disabled reader has information-finding AND representation-checking; architect has at-programming AND mid-project; etc.
- Mission articulation (public-facing version + internal governance version)
- Epistemic commitments stated explicitly with citations to relevant literature, including design-pedagogy literature for the questions-led commitment (N-08)
- Iteration: each audience cut tests against mission language; each mission revision tests against audience priority

**Output:** `governance/audience-priority.md`; `governance/mission-and-epistemics.md` (canonical)
**Decisions:** Audience priority + use patterns; mission language; epistemic commitments

### A3. Conceptual model · 5–7 sessions · *Resolves T-06, T-07, N-03*
**Co-1 role:** Drafting on population, sub-population, Co-1 collaborator entities

Settle definitions of all entities and relationships. Per T-07, entity inventory expanded:

**Original (synthesis line 142):** parameter, sub-parameter, population, sub-population variation, evidence claim, evidence source, jurisdiction, jurisdictional worldview, item, room/space, design stage, project type, conflict, question, specialist handoff, time-version

**Added per audit:** `audience` (with use-pattern children), `Co-1 collaborator` (people, distinct from claims), `best-practice claim` (entity identity for citation, supersession, validation), `building type`, `sub-population` (promoted to entity), `citation` (relation between claim and source)

**Cross-cutting axes (T-06, N-03):** `design stage` and `project type` promoted from entities to cross-cutting axes interacting orthogonally with parameters. Every parameter has applicability across the design-stage × project-type matrix; schema and skills must reflect both axes.

**Output:** `governance/conceptual-model.md` (with diagrams)
**Decisions:** Entity inventory; cross-cutting axes; relationship rules; cardinality

### A4. Voice and framing · 2–3 sessions
**Co-1 role:** Review of voice samples for resonance with disabled-reader use patterns

Per synthesis: write three versions of the same parameter section in three voices; test against mission; consolidate. Decisions about `voice-style_SKILL.md` survival depend on outcome.

**Output:** `governance/voice-and-framing.md`; revised `skills/voice-style_SKILL.md`

### A5. Co-1 co-author relationship — operational specification + recruitment thread · 5–7 sessions for design; recruitment is **parallel cross-stage thread** · *Resolves D-03, N-06*
**Co-1 role:** Drafting of the document itself — collaborators define their own relationship to the project

Reframed per N-06. The phase produces operational specification *and* recruitment plan; **recruitment execution is a parallel thread running through Stages A and B**, gated against C4 (population migration) which cannot start without adequate corpus per population.

Operational specification includes:
- Per-phase Co-1 role: Drafting / Decision / Review (resolves D-03)
- Compensation rates (concrete numbers)
- Recognition mechanisms (authorship credit, named contribution)
- Decision authority specification (what Co-1 decides; what advises; what cannot be overridden)
- Disagreement-handling protocol (Tier 1 vs. Co-1 conflicts → aligned synthesis OR documented disagreement OR escalation)
- Burnout prevention (workload caps, rotation, off-ramps)
- Resource-honest declaration: if resourcing cannot fund drafting-stage involvement, A5 declares methodological limitation in mission language

Recruitment plan includes:
- DPO partnerships (organizational identification and outreach plan)
- Per-population recruitment goals informed by current Co-1 corpus density
- Trust-building cadence (recognizing this takes weeks-months of clock time)
- Onboarding pathway

**Output:** `governance/co1-coauthor-relationship.md` (operational); `governance/co1-recruitment-plan.md`
**Decisions:** Resourcing; methodological-limit acceptance if any; per-phase role assignments

### A6. Evidence methodology · 3–5 sessions · *Resolves T-03 final, T-04 final, N-02, N-08, D-04 (partial)*
**Co-1 role:** Decision on Co-1 tier encoding; Drafting on disagreement protocol

Per synthesis core scope plus:
- **T-03 final:** Co-1 tier encoding (decided in 0.5; A6 details schema implications)
- **T-04 final:** sparse-evidence behavior implementation (decided in 0.5; A6 specifies how `[BEST-PRACTICE-PENDING]` or reduced-confidence category operates)
- **N-02:** values-criteria assessment ("respectful" and "dignified") — explicit acknowledgment that these are evaluated through Co-1 mechanism rather than independent evidence; methodology specifies this rather than leaving implicit
- **N-08:** engages design-pedagogy literature (inquiry-based learning, scaffolded questioning, problem-based learning in professional formation); cites in mission-and-epistemics document
- **D-04 partial:** `epistemic-defense` skill specification (skill builds in C2; periodically tests current claims against simulated external critique)

**Output:** `governance/evidence-methodology.md`; updates to `project-standards.md`; `skills/epistemic-defense_SKILL.md` (spec)
**Decisions:** Co-1 tier encoding details; sparse-evidence implementation; values-criteria assessment mechanism; pedagogy literature integration; epistemic defense practice

### A7. Population taxonomy · 2–3 sessions
**Co-1 role:** Decision per population

Per synthesis. Foundation tag (functional/cultural/symptomatic/syndromic) as first-class data per safeguards S20. Within-population variability operationalization. Sub-code consistency. IntD proxying. Emerging populations (long COVID, etc.).

**Output:** `governance/population-taxonomy.md`

### A8. Jurisdiction philosophy · 2–3 sessions

Per synthesis. Worldview as first-class entity. 24-vs-46 inconsistency resolved. Tier-A/Tier-B Global South tiering retained or replaced.

**Output:** `governance/jurisdiction-philosophy.md`

### A9. Time model unification · 2–3 sessions · *Resolves L-04, D-05*

Establish single temporal substrate unifying entity-level versioning, governance document re-issue, skill-output versioning. Decisions:
- Time model: commit DAG, semantic versioning, point-in-time queries, hybrid
- Entity metadata: created / modified / superseded / valid-from / valid-to
- Document versioning approach
- Skill-output basis-version tracking
- Cross-layer query mechanism
- **Operationalization timing:** time model live from start of Stage C, not end (resolves D-05)

**Output:** `governance/time-model.md`
**Decisions:** Time model selection (12+ year implication)

### A10. Adversarial-use review framework · 1–2 sessions

Define how the project addresses adversarial uses: minimum-compliance weaponization, exclusionary ROI, surveillance via inferred functional needs. Pre-public-release review process. Mitigation tactics (licensing, framing, omissions).

**Output:** `governance/adversarial-use-framework.md`

### A11. Legal and regulatory framework · 1–2 sessions + external counsel

Counsel review of "teaches not prescribes" doctrine in liability terms. Disclaimer structure. Licensing model. Trajectory positioning (does the project pursue, avoid, or accept jurisdictional adoption / certification).

**Output:** `governance/legal-regulatory.md`
**Decisions:** Disclaimer language; licensing; trajectory positioning

### A12. Decision proxy and capture protocol · 1 session · *Resolves L-05*

Define:
- Which decisions can be delegated; to whom; under what conditions
- Which decisions cannot be delegated (named explicitly)
- Decision capture protocol: each decision produces written rationale alongside outcome
- **Standardized model-routing notation across phase tables** (resolves L-05)

**Output:** `governance/decision-protocol.md`

### A13. Doctrine-recheck cadence · 1 session · *Resolves B-06, partial D-04*

Periodic operational audit cadence:
- Every N working sessions OR at each major phase transition
- Checks: evidence-tier inversion, single-source violations, Co-1 representation drift, doctrine-operations alignment, model-routing compliance
- Includes periodic fresh-context decision-checking sessions for major decisions (counters long-context drift, B-06)
- Skill: `doctrine-recheck` (specified here; built in C2)

**Output:** `governance/doctrine-recheck-cadence.md`; `skills/doctrine-recheck_SKILL.md` (spec)

### Stage A done criteria

- All thirteen governance documents committed
- `project-standards.md` updated
- Co-1 recruitment thread active; representation goals defined per population
- Time model decided (A9)
- Adversarial-use and legal frameworks established
- Decision protocol live
- Doctrine-recheck cadence operational
- No content work started on new architecture

---

## Stage B — Architecture and pilot
**Sessions:** 26–40 (was 22–34; expanded for B1 derivation, B4 multi-pilot)
**Output:** Working multi-pilot demonstrating end-to-end the structured form serves the mission

### B1. Schema design with architectural derivation · 6–9 sessions · *Resolves N-05, partial L-04, D-05*

Reframed per N-05. B1 evaluates ≥3 storage forms against requirements before committing. Candidate forms:
1. Graph database (Neo4j, TigerGraph, Neptune)
2. RDF/JSON-LD with triplestore + reasoner
3. Structured markdown with explicit relationship markers + build pipeline
4. Relational database with views
5. Hybrid (relational atoms + graph relationships)

Evaluation criteria:
- Queryability for proposed navigation modes (B3)
- Maintainability over 12+ years
- Alignment with GitHub-based workflow (constrains technical surface)
- Co-1 review interface feasibility
- Migration path from current markdown
- Tooling maturity and ecosystem

Output is the chosen form **with derived rationale**, the schema spec, and the dismissed alternatives with reasons. **Time model from A9 implemented in schema** (resolves D-05 + L-04 in storage layer). Schema validators run in CI.

**Output:** `architecture/storage-derivation.md`; `architecture/schema-spec.md`; `architecture/storage-decision.md`
**Decisions:** Storage form (12+ year implication)

### B2. Tooling design with expanded validator suite · 4–6 sessions · *Resolves multiple findings as validators*

Per synthesis core plus expanded validator suite addressing audit-identified gaps:

| Validator | Resolves | Purpose |
|---|---|---|
| Schema | foundation | Mechanical schema conformance |
| Evidence-tier (Co-1-aware) | T-03 | Best-practice claims must cite ≥Tier 3, with correct Co-1 handling |
| Single-source | safeguards S13 | Detect duplicate values across files |
| Cross-reference | foundation | Reference integrity |
| Round-trip rendering | D-02 | Markdown ↔ structured form fidelity |
| **Question-coverage** | T-02, D-01 | Every parameter exposes ≥1 question |
| **Variability-coverage** | N-04 | Every parameter exposes within-population variability |
| **Design-stage coverage** | T-06 | Every parameter has stage-applicability per project-type |
| **Refresh-staleness** | D-02 | Detect rendering staleness against source |
| **Co-1-representation** | safeguards S24 | Flag representation drift per population |
| **Temporal-coherence** | D-05, A9 | Detect stale evidence; supersession integrity |
| **Epistemic-defense** | D-04 | Periodically tests claims against simulated external critique |

Build-or-buy decisions per tool. Co-1 review interfaces specified.

**Output:** `architecture/tooling-spec.md`
**Decisions:** Build-or-buy per tool; resource allocation

### B3. Navigation mode specification · 3–4 sessions · *Resolves T-02, T-05, D-01*
**Co-1 role:** Drafting of respect-visibility view; Decision on navigation taxonomy

Per synthesis core plus:
- **Questions-led navigation mode** as first-class entry surface (T-02, D-01)
- **Use-pattern-aware modes per audience** (T-05): disabled-reader has both information-finding AND representation-checking modes; architect has at-programming AND mid-project modes; OT has clinical-collaboration AND specialist-handoff modes; policymaker has comparison AND rationale modes

Cross-navigation specifications between modes. Interactive features (population-checkbox-driven content per the conditional-content discussion).

**Output:** `architecture/navigation-modes.md`

### B4. Multi-pilot construction · 8–12 sessions (was 6–8 single pilot) · *Resolves N-01, N-09*
**Co-1 role:** per A5 specification — Drafting if recruitment supports; Decision at minimum

Reframed per N-09 and N-01. Three pilot tracks span the dimensions that matter for architecture validation:

**Pilot track 1: Adequate-evidence parameter, adequate-corpus population.**
- Parameter: turning space (well-evidenced)
- Population: MOB (adequate Co-1 corpus)
- Item: G-04 (Bathroom — Wet Room)
- Tests architecture's ability to handle good evidence flowing cleanly

**Pilot track 2: Contested parameter, multi-population.**
- Parameter: lighting illuminance (contested across populations)
- Populations: NDV/AUT + MOB + OFS (conflict zone)
- Item: B-08 (Lighting)
- Tests architecture's conflict-resolution and combinatorial views

**Pilot track 3: Sparse-evidence parameter, sparse-corpus population.**
- Parameter: acoustic privacy / RT60
- Population: NDV/MH (specifically PTSD-relevant sub-cohort)
- Item: A-13 (Acoustics)
- Tests architecture's sparse-evidence handling (T-04 implementation in practice)

All three tracks operate against the same room (Bathroom, plus Lighting and Acoustics adjacencies) so the room-level composition is also exercised.

For each track: populate every entity type the schema supports. Surface every question the designer should ask. Include functional variability, co-occurrence, jurisdictional overlay, evidence with tier, conflicts, specialist handoffs.

**Output:** Populated schema instances for three pilot tracks
**Decisions:** Co-1 approval at multiple checkpoints per track

### B5. Pilot rendering with refresh policy · 3–4 sessions · *Resolves D-02*

Per synthesis core plus rendering refresh policy decision (D-02): continuous-deploy, periodic-snapshot, or versioned-release. Round-trip rendering verification (S12) integrated.

Render each pilot track through every navigation mode and in markdown form. Verify:
- Each navigation mode produces coherent, useful results
- Markdown is faithful to structured source (no information loss)
- Cross-navigation works
- Interactive features work
- Refresh policy implementation works

**Output:** Rendered pilots in all forms; rendering refresh policy committed; identified rendering issues

### B6. Pilot validation against mission · 4–5 sessions · *Resolves N-08 (partial)*
**Participants:** Opus + Co-1 + project owner + practicing architects (≥2)

Per synthesis core plus expanded criteria:
- Does the pilot help the reader ask better questions? (Tested with practicing architects at programming AND DD stages) — **directly tests N-08 hypothesis**
- Does the pilot acknowledge non-uniformity visibly?
- Does the pilot differentiate Tier 0 / 1 / 2 in ways that change reader behavior?
- Does the pilot ground best practice in evidence, not codes?
- Does the pilot meet the most-accommodating / dignified / usable standard? (Co-1 review decisive)
- Does the pilot allow each prioritized audience to do their work?
- **Question-coverage validation passes**
- **Variability-coverage validation passes**
- **Design-stage coverage validation passes**
- **Co-1-as-co-author test passes** (per A5 specification)
- **Round-trip rendering verification passes**

Multi-pilot allows distinguishing architectural from corpus failure modes (resolves N-01).

**Output:** `architecture/pilot-validation-report.md`; iteration backlog
**Decisions:** Architecture lock vs. iterate

### B7. Architecture lock · 2 sessions

Lock the architecture decisions. Update governance documents. Communicate to all skills, validators, CI gates. Periodic fresh-context decision-checking session held here per A13.

**Output:** `architecture/architecture-lock.md`; supersession notes for prior architectural assumptions

### Stage B done criteria

- Multi-pilot exists in structured form
- Pilots render to all navigation modes including questions-led
- Pilots pass Co-1 review (in operationally-specified role)
- Pilots validate against expanded mission criteria
- Architecture is locked
- Rendering refresh policy decided
- All proposed validators specified and integration-tested

---

## Stage C — Migration and scaling
**Sessions:** 165–245 (was 140–200)
**Output:** Complete project in structured form, audit-as-byproduct, ongoing time-handling

### C0. Skill responsibility matrix · 2–3 sessions · *Resolves L-03, B-04*

From skill inventory (Stage 0.3) and C2-target inventory, produce responsibility matrix. Each skill has single distinct named responsibility. Overlaps from L-03 resolved by consolidation or boundary specification:
- `evidence-auditor` vs. `evidence-tier-validator` boundary specified
- `jurisdiction-tracker` vs. `standards-registry` consolidated or boundary specified
- `markdown-extractor` and `migration-orchestrator` sequence specified
- `single-source-validator` vs. `cross-reference-resolver` boundary specified
- `Co-1-review-prep` vs. `markdown-renderer` boundary specified

**Output:** `architecture/skill-responsibility-matrix.md`

### C1. Migration tooling build · 4–6 sessions

Build tools specified in B2 that handle migration. Includes automated extraction (where possible), manual-entry interfaces (where needed), validation, rollback. **Time-handling integrated from this point onward** (resolves D-05). Validators (B2) ship before migration tools so silent corruption is caught at extraction.

**Output:** Migration tool suite

### C2. Skill set rebuild · 12–16 sessions (was 8–12) · *Resolves multiple*

Expanded scope per audit. Skill ecosystem inventory:

**Research:** multilingual-research (REBUILT), Co-1-evidence-intake (NEW), evidence-auditor (REBUILT), jurisdiction-tracker (REBUILT), standards-registry (REBUILT)

**Synthesis:** BPC-orchestrator (REBUILT — Tier 1–3 first, code overlay), conflict-resolver (REBUILT), divergence-synthesis (REBUILT), question-author (NEW), specialist-handoff-author (NEW)

**Migration (deprecates after C):** markdown-extractor (NEW), entity-validator (NEW), migration-orchestrator (NEW), supersession-marker (NEW)

**Authoring:** voice-style (REBUILT post-A4), entity-authoring (NEW), narrative-prose (REBUILT)

**Validation:** schema-validator, evidence-tier-validator (Co-1-aware), single-source-validator, Co-1-representation-validator, temporal-coherence-validator, cross-reference-resolver (REBUILT), round-trip-rendering-validator, **question-coverage-validator** (NEW per T-02), **variability-coverage-validator** (NEW per N-04), **design-stage-coverage-validator** (NEW per T-06), **refresh-staleness-validator** (NEW per D-02)

**Co-1 interface (entire category NEW):** Co-1-recruitment, Co-1-review-prep, Co-1-disagreement-tracker, Co-1-compensation-tracker

**Project orchestration:** session-consolidator, workplan-orchestrator, gap-register, research-log-manager, toc-editor (REBUILT for entity-composition rather than markdown TOC), change-order, **doctrine-recheck** (NEW per A13), **decision-capture** (NEW per A12), **supersession-checker** (NEW per D-05)

**Rendering:** markdown-renderer (NEW), web-renderer (NEW), navigation-mode-renderer (NEW), respect-visibility-renderer (NEW), **questions-renderer** (NEW per T-02), **rendering-refresh-coordinator** (NEW per D-02)

**Epistemic:** **epistemic-defense** (NEW per D-04)

Cross-cutting requirements every skill must satisfy:
- Operates on structured form, not markdown
- Mechanically enforces evidence-tier discipline
- **Stage-aware authoring output** (NEW per T-06)
- Consults Co-1 representation status before population-specific claims
- Produces decision-capture artifacts alongside content
- Version-aware
- Schema-validator runs in CI
- Doctrine-recheck hook
- Explicit dependency graph
- Self-applying (per M4)

Sequenced per C0 responsibility matrix.

**Output:** Rebuilt/modified skill files

### C3. Migrate parameters · 30–40 sessions · *60–80 atomic parameters*
**Co-1 role:** per A5 — Drafting where recruitment supports

Each parameter migrated independently. Per parameter: extraction from BPC + Part 4 + Appendix A + spec database; consolidation; tier verification; evidence chain reconstruction; functional variability narrative; co-occurrence narrative; question authoring; jurisdictional overlay with worldview; specialist handoff identification; design-stage × project-type applicability matrix; Co-1 validation; commit. Time-handling live throughout.

### C4. Migrate populations · 18–28 sessions · *11 populations*
**Co-1 role:** Drafting (decisive); pace gated by recruitment readiness per population

Per population: define entity; populate within-population variability; populate co-occurrence patterns; populate jurisdiction-specific worldview implications; identify specialist handoff patterns; identify population-specific recurring questions across parameters. **C4 cannot start migrating populations whose Co-1 corpus is below threshold; recruitment thread (A5) gates this.**

### C5. Migrate items and rooms · 30–45 sessions · *92 items + room set*

Items and rooms become composed views over parameter and population libraries. Composition correctness validated through navigation modes. Where current items conflate distinct functional needs, structured form decomposes.

### C6. Migrate conflicts · 28–45 sessions · *Estimated 200–400 actual conflict entries*
**Co-1 role:** Drafting on harm-asymmetry analysis

Population-pair × parameter combinatorial. Most pairs do not conflict for most parameters. Per conflict: evidence; harm-asymmetry analysis; resolution.

### C7. Migrate evidence base · 12–17 sessions · *557 sources + 6% residual disposition · Resolves B-05*

The 557-source bibliography becomes structured library. Each source: bibliographic metadata; tier classification; applicability notes; links to claims. **Explicit disposition of unverified 6% residual** (resolves B-05): re-verify; deprecate as unverifiable with research-gap flag; migrate-with-marker pending re-verification.

### C8. Migrate jurisdictions · 8–12 sessions · *46 jurisdictions*

Standards registry becomes jurisdiction library with worldview annotations. Parameter overlays linked to jurisdiction entity. Temporal handling live (per A9 and time model).

### C9. Cross-cutting prose migration · 20–30 sessions · *Parts 1–3, 5, 9, 10–12*
**Model:** Opus

Rewritten in voice from A4, aligned with corrected methodology. Part 1 establishes mission and approach. Part 2 catalogs populations. Part 3 describes methodology. Parts 5, 9, 10–12 cover building-level resolution, OT collaboration, supplementary topics.

### C10. Quality gates and validation · 6–10 sessions

All validators run on all migrated content. Cross-reference resolvers. Co-1 representation checks. Evidence-tier audits. Navigation-mode rendering tests. Question-coverage. Variability-coverage. Design-stage coverage. Refresh staleness. Failures route to appropriate skill for repair.

### C11. Maintenance lifecycle establishment · 3–5 sessions · *Narrowed scope per D-05*

Documents the operational practice that has been live throughout Stage C (per A9 and C1 onward). Formalizes:
- New evidence ingestion process
- Code-change tracking
- New population recognition pathway
- Co-1 ongoing relationship management
- Skill set update protocol
- Versioning and release cadence
- Deprecation process

**Output:** `governance/maintenance-lifecycle.md`

### Stage C done criteria

- All atomic entities migrated and validated
- All composed views rendering correctly
- All navigation modes operational including questions-led
- Co-1 review/drafting complete across all populations
- Schema validators passing
- Time-handling has been live since C1
- Maintenance lifecycle documented

---

## Cross-stage requirements

These operate continuously, not at single phases:

**CS1. Doctrine-recheck cadence.** Per A13. Every N working sessions or stage transition. Includes periodic fresh-context decision-checking sessions.

**CS2. Co-1 recruitment thread.** Per A5. Active from A5 forward. Gates C4 per population.

**CS3. Versioning continuity.** Per A9. Time model live from C1. All entities, governance documents, skill outputs carry version metadata.

**CS4. Document re-issue cadence.** Synthesis re-issued after Stage 0; after Stage A complete; after B7 lock. Roadmap re-issued after Stage 0; after each major phase complete.

**CS5. Co-1 representation monitoring.** Per safeguards S24, A5. Dashboard updated as corpus grows. Drift triggers recruitment.

**CS6. Standards monitoring.** Per safeguards S29. Active from B7 onward. New standards releases ingested via supersession-checker.

**CS7. Salvage re-evaluation.** Per safeguards S25. At each stage transition. What was salvageable at Stage A may be partly superseded by Stage B decisions.

**CS8. Decision capture.** Per A12. Every decision point produces written rationale alongside outcome.

**CS9. Adversarial-use review.** Per A10. Pre-public-release gate; periodic review during Stage C.

---

## Budget arithmetic

Corrected per L-06.

| Stage | Min | Max | Notes |
|---|---|---|---|
| Stage 0 | 8 | 12 | NEW; verification + decision freeze |
| Stage A | 25 | 37 | 13 phases including 5 new (A9–A13); A1-A2 merged |
| Stage B | 26 | 40 | B1 derives form; B4 multi-pilot; B6 expanded |
| Stage C | 165 | 245 | C0 added; expanded C2; C7 includes residual |
| **Total** | **224** | **334** | |

| Calendar pace | Min | Max |
|---|---|---|
| 2 sessions/day intensive | ~4 months | ~5.5 months |
| 1 session/day sustained | ~7.5 months | ~11 months |
| Real-world (with Co-1 cadence, parallelism, project-management overhead) | **15 months** | **24 months** |

The 12–18 month estimate from synthesis was built on understated session counts. Realistic real-world is 15–24 months. Recruitment alone may push the lower bound up — A5 recruitment thread takes weeks-to-months of clock time independent of session count.

---

## Decision inventory

23 decision points (was 13).

| # | Phase | Decision |
|---|---|---|
| 1 | precondition | Adopt synthesis (per Coda's mission-test) |
| 2 | 0.4 | Contamination ratio acceptance — does it change scope? |
| 3 | 0.5 | T-03 Co-1 tier encoding |
| 4 | 0.5 | T-04 sparse-evidence behavior |
| 5 | 0.5 | D-03 Co-1 operational role |
| 6 | 0.8 | Repo strategy |
| 7 | 0.9 | Workplan adoption (this version or revised) |
| 8 | A1-A2 | Audience priority + use patterns |
| 9 | A1-A2 | Mission language + epistemic commitments |
| 10 | A3 | Conceptual model + entity inventory + cross-cutting axes |
| 11 | A4 | Voice selection |
| 12 | A5 | Co-1 resourcing; per-phase role assignments; recruitment plan |
| 13 | A6 | Co-1 tier encoding details; sparse-evidence implementation; values-criteria mechanism; pedagogy integration; epistemic defense |
| 14 | A7 | Population taxonomy |
| 15 | A8 | Jurisdiction philosophy |
| 16 | A9 | Time model selection |
| 17 | A10 | Adversarial-use mitigation tactics |
| 18 | A11 | Disclaimer language; licensing; trajectory positioning |
| 19 | A12 | Decision protocol; standardized model-routing notation |
| 20 | A13 | Doctrine-recheck cadence |
| 21 | B1 | Storage form (12+ year implication) |
| 22 | B2 | Build-vs-buy per tool |
| 23 | B5 | Rendering refresh policy |
| — | B6 | Architecture lock vs. iterate |
| — | C11 | Maintenance lifecycle approval |

Plus ongoing Co-1 collaborator decisions throughout, scoped per A5.

---

## Salvage matrix (revised)

| Status | Items | Adjustment from synthesis salvage matrix |
|---|---|---|
| **Fully reusable** | Research data: jurisdictional values, verified evidence sources, multilingual coverage, Co-1 corpus | Same as synthesis |
| **Reusable with adjustment** | Skill methodologies (structure intact, output target + synthesis logic change); validators (paradigm intact, code rewrites); parts of voice work; bibliography metadata for the 94% verified | Same as synthesis |
| **Reusable conditionally** *(NEW)* | BPC `best_practice_synthesis` fields where contamination sample shows clean | Per Stage 0.4 contamination sampling outcome |
| **Superseded** | BPC `best_practice_synthesis` fields where sample shows contamination; Part 4 specs as currently written; Appendix A tables as currently framed; prior CO-0007 audit workplan; the audit v1; workplan v2 | Per Stage 0.4 + this workplan |
| **Open** | `voice-style_SKILL.md` (depends on A4); 6% unverified bibliography (depends on C7 disposition) | Same as synthesis + B-05 |

The "reusable conditionally" category is added because the synthesis treated contamination as binary; Stage 0.4 surfaces it as continuous.

---

## What this workplan does not solve

- **The mission adoption decision.** Sit with the PROVISIONAL mission committed in Stage 0.6. Adopt or revise. The workplan does not pre-empt this.
- **The three Critical pre-Stage-A doctrinal decisions** (T-03, T-04, D-03). The workplan stages them at 0.5 with the materials needed to decide; it does not decide for the project owner.
- **Whether resources support operational Co-1 co-authorship vs. operational Co-1 review.** That is a project-owner determination constrained by funding and DPO partnership realities. A5 produces honest declaration either way.
- **The storage form selection** (B1). Architectural derivation work for B1 itself. The workplan ensures alternatives are evaluated rather than asserted.
- **Whether the questions-led pedagogical hypothesis is empirically supported.** B6 tests it with practicing architects at the pilot scale. Larger validation is post-rebuild research.
- **How values-criteria ("respectful," "dignified") are weighted against accommodating/usable when they conflict.** A6 specifies the assessment mechanism; weighting is per-case Co-1 judgment.

---

## Coda

The audit's central observation — doctrine articulated, operations under-specified — drives the structural changes in this workplan. New phases (A9–A13), expanded phases (A5, A6, B1, B4, C2), and a verification-first Stage 0 collectively close the operational gaps the audit identified. The workplan still does not *make* the doctrinal decisions, but it stages them where they belong (0.5 for the three Critical, A6 for the implementation details) and ensures the architecture work that depends on them does not begin until they're made.

The 15–24 month real-world horizon is honest. Recruitment cadence (A5), Co-1 review windows, and external counsel/architect input are the binding constraints; session count is not. The project is large because the mission is large and the existing corpus is substantial. Each migrated parameter is independently usable, so value is released incrementally rather than only at completion.

The synthesis Coda's instruction stands: sit with the mission language before adopting the workplan that operationalizes it.
