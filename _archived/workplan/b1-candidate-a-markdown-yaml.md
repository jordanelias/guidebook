# B1 Session 3 — Candidate A Evaluation
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 3 of 6–9
**Candidate:** A — Markdown + YAML status-quo-extended
**Status:** Per-criterion evaluation complete; Candidate A scored against 30 criteria
**Predecessor session:** `sessions/session_2026-05-01-b1-s2.md` (B1 Session 2 — requirements lock + criteria weighting)
**Parallel-context predecessor:** `sessions/session_2026-05-01-audit-remediation.md` (audit remediation; no B1 binding impact — see §1.4)
**Operative governance:** D-0108 (framework), D-0110 (weighting), D-0111 (S-05 spec), D-0112 (eliminator test, applies to Candidate D only), D-0113 (requirements lock)
**Model routing for this session:** opus/150/synth

---

## 1. Session purpose and scope

### 1.1 Purpose

Apply the 4-question evaluation template from `b1-derivation-framework.md` §6.1 to Candidate A across all 30 criteria. Produce per-criterion scores 0–3 per the D-0112 rubric. Compute weighted total per D-0110.

This session does NOT compare A to B/C/D — that is Session 7. This session does NOT select a storage form — that is Sessions 7–9. This session produces Candidate A's standalone evaluation only.

### 1.2 Inputs read

| Document | Purpose |
|---|---|
| `workplan/b1-derivation-framework.md` (D-0108) | Framework, candidates §5, criteria §6, 4-question template §6.1 |
| `workplan/b1-criteria-weighting.md` (D-0110, D-0111, D-0112, D-0113) | Per-criterion weights; S-05 5-deliverable standard |
| Live state of `schemas/`, `scripts/`, `data/`, `bpc/`, `references/`, `parts/`, `versions/` | Candidate A's incumbent implementation |
| Schema files: `evidence_source.py`, `evidence_state.py`, `specification.py`, `temporal.py`, `connection.py`, `bpc_metadata.py` | Class structure for Candidate A's typed-Pydantic-on-YAML approach |
| `governance/migration-survival.md` (PROVISIONAL, D-0116) | Read for awareness — not folded into requirements per §1.4 |

### 1.3 Candidate A characterization (ground truth)

The current state of `jordanelias/guidebook` `main` is Candidate A in its un-extended form. Concretely:

**Schemas** — 14 Pydantic modules under `schemas/`:
- Entities with full schema: EvidenceSource, EvidenceStateRecord (with nested ProvisionalConfidenceFlag, ConvergenceAssessment), Specification, Connection, BPCMetadata, Decision, AdversarialUseCatalog, RecheckSession + ContaminationSample + RecheckFinding + DoctrineSnapshot, Gap, Slug
- Temporal (A9): VersionTag, EffectiveDateRange, GuidebookVersion, StandardEdition, ProjectRule, SupersedenceLink, LaunchPhaseRecord — 7 classes

**Validators** — 16 scripts under `scripts/`:
- Schema-shape validators: validate_schema, validate_evidence_state, validate_population, validate_jurisdiction, validate_temporal, validate_bpc, validate_cross_refs
- Governance validators: doctrine_recheck, audit_adversarial_use, decision_capture, contamination_sampler
- Operational: validate_commits, check_phase_a_complete, check_thresholds
- Conversion: under `scripts/convert/`

**Data materialization** — 3 of ~20 entity types have YAML records:
- `data/decisions/decision_register.yaml` (118 records, single file)
- `data/adversarial_use/catalog.yaml` (catalogue with per-version review_log files)
- `data/doctrine_recheck/{recheck,sample,snapshot,counter}.yaml` (per-cycle records + singleton counter)

**Markdown-form entities** — 17 entity types live in markdown + YAML frontmatter or markdown-resolved-by-validator:
- BPC entries: `references/bpc/{slug}/bpc.md` with frontmatter + `search-log.md` (78 dirs)
- Specifications: `parts/v10/` markdown for prose-form spec text
- Connections: `references/connections/_index.md` register table (188 records) + per-CON-ID detail in markdown sections
- Slugs: `references/slug-set.md` (table)
- Gaps: `gap_register.md` (table)
- Populations / Sub-populations / Items / Conflicts / Rooms / Building Types / FDR Scenarios / Search Logs / Audiences / Co-1 Collaborators / Specialist Handoffs / Time-Versions / Questions / Standards-registry / Mission / Audience-priority — all markdown documents under `governance/` or `references/`

The "status quo extended" framing in framework §5.1 means: extend Pydantic schema coverage to all 20 entity types, materialize data into YAML files where currently markdown-only, build query/view layer for the audience-priority navigation modes. The schema work is largely done (only Population, Item, Conflict, Question, FDR Scenario, Specialist Handoff need new Pydantic classes); the materialization and query-layer work is not.

### 1.4 Migration-survival governance read

`governance/migration-survival.md` is PROVISIONAL governance authored in a parallel-context session (audit-remediation 2026-05-01 03:30–04:30 UTC). The document classifies pre-pivot artifacts by survival disposition (SURVIVES_AS_IS / SURVIVES_WITH_REDERIVATION / SURVIVES_CONDITIONALLY / SUPERSEDED / OPEN). Per §7 of that document, B1's storage-form selection affects all SURVIVES_AS_IS estimates.

The direction is one-way: B1 affects migration-survival classifications, not the reverse. The migration-survival register is a corpus-classification register operating on the existing content; it does not introduce new architectural requirements that Candidate A or any other candidate must satisfy. The 36-requirement inventory in framework §4 remains the authoritative input set per D-0113.

CS-MIG cross-stage thread (migration-survival §9) triggers on commits modifying §4 categories. This session's commit modifies workplan/, data/decisions/, data/doctrine_recheck/, sessions/ — none of these are §4 categories of migration-survival. CS-MIG does not trigger on this commit.

---

## 2. Per-criterion evaluation

For each criterion, the four-question template (framework §6.1) is applied:

> 1. Native, adapted, or absent?
> 2. Adaptation cost (sessions; complexity)?
> 3. Operational risk (solo-author failure mode)?
> 4. Downstream binding (effect on B5–B7, Stage C)?

Scores: **0** = absent; **1** = adapted, high cost; **2** = adapted, moderate cost; **3** = native.

### 2.1 Cluster I — Entity & relationship (4 criteria)

#### C-1.1 — Entity-type expressiveness across the 20 A3 types

1. **Adapted.** 12 of 20 entity types have Pydantic schemas; 5 more (Population, Item, Conflict, Question, FDR Scenario, Specialist Handoff) need new schema modules of comparable shape; 3 (Audience, Mission, Co-1 Collaborator) are governance documents that the framework treats as schemed prose (no YAML record per entity). Adding new entity types is mechanical: a new module under `schemas/`, a new directory under `data/`, a new validator step. The 14 existing schemas demonstrate the pattern. New entity types do not migrate existing entities.
2. **Cost: 5–7 sessions** to schema the 5 missing entity types (1 session per non-trivial type plus 1 session for the governance-document trio). Pydantic schema work is well-understood; the cost is shaped by how much definitional work each type requires, not by the storage form itself.
3. **Operational risk: low.** New entity types are added file-by-file. A schema-validation failure on a new type is loud and local — it does not corrupt existing entities. Solo-author rollback is `git revert`.
4. **Downstream binding: low.** The 14 existing schemas are not affected by additions. Stage C migration tools (B2) build per-entity-type extractors regardless of storage form; the count of types affects extractor count, not architecture.

**Score: 2** (adapted, moderate cost — schema additions are well-understood but the count is non-trivial)

#### C-1.2 — Relationship-type expressiveness (1:N, N:N, polymorphic)

1. **Adapted.** Pydantic models express 1:N natively as `list[str]` of foreign IDs. N:N requires a join-table convention — currently implemented in `references/connections/_index.md` (an external table) and as `cited_evidence: list[str]` on Specification. Polymorphism (Gap.blocks → any entity) is implemented as a string field plus convention enforced by `validate_cross_refs.py`. Schema validation for these is implemented but not type-safe in the way a relational FK constraint would be — the validator catches dangling references at CI time, not at write time.
2. **Cost: 0–1 session.** The patterns are already in place; extending to new N:N relationships is adding a `list[str]` field plus a validator entry.
3. **Operational risk: medium.** A typo in a foreign ID is caught at the next CI run, not at write time. The window between a bad write and a CI catch is short (commits push CI), but the risk surface is larger than a relational FK constraint.
4. **Downstream binding: medium.** Query patterns over N:N relationships ("which specifications cite this source?") require traversal logic in the query layer — i.e., reading the source's incoming `cited_evidence` references across all Specification YAML files. This is an O(n) scan per query in the naive implementation, addressable by indexing at query time.

**Score: 2** (adapted, moderate cost — patterns work but type safety is CI-time not write-time; query-layer traversal is non-native)

#### C-1.3 — Within-population variability as first-class data **[Weight 3]**

1. **Adapted.** Mission §Doctrinal commitment 1 requires within-population variability to be first-class data, not narrative caveat. In Candidate A, this is operationalized through (a) per-(parameter × population) cells with explicit `state` and `convergence` fields on EvidenceStateRecord, (b) sub-population records under Population (per A7), (c) divergence assessment per cell. The schema supports it; materialization requires per-cell YAML files (one per parameter × population combination) which currently exist in markdown form within BPC files but not as structured records.
2. **Cost: high — 6–10 sessions** to materialize cell-level records across the 78-BPC × ~20-population matrix. The materialization is an extraction job from existing BPC markdown into YAML records under a new `data/cells/` directory. The cost is not architectural; it is the volume of cells to populate.
3. **Operational risk: medium.** Cell-level YAML records are individually small (a few fields each) and individually verifiable. The risk is not in any single cell but in the consistency of the materialization — that the 78 BPCs' per-population narratives are extracted faithfully. Mitigation: B2 builds the extractor with a verification report.
4. **Downstream binding: high.** Stages B3–B7 and Stage C all read cell-level state. If the cell records are not materialized, B3's question-led mode cannot index by parameter × population variability; B4's pilot cannot demonstrate variability rendering; B5's renderer has nothing to render. This is the load-bearing data shape for the mission's foundational claim.

**Score: 2** (adapted, moderate-to-high cost — schema is native, materialization is the work, but the form itself supports first-class variability)

#### C-1.4 — Sub-population inheritance

1. **Native.** A7 specifies sub-population codes (NDV/AUT, MOB/AMB, etc.) that inherit population properties unless overridden. Candidate A's pattern: Population YAML carries default fields; Sub-population YAML carries `inherits_from: parent_population_code` plus explicit overrides. Validator resolves inheritance at read time. The pattern matches how A7 was specified.
2. **Cost: 1–2 sessions** to implement the inheritance resolver and add validator coverage. Not architectural complexity; just a resolver function.
3. **Operational risk: low.** Inheritance resolution is mechanical and deterministic. A sub-population with a missing parent is caught by `validate_cross_refs.py`.
4. **Downstream binding: low.** Cross-reference resolution at query time uses the resolver; no architectural impact downstream.

**Score: 3** (native — the markdown+YAML form supports inheritance through explicit fields and a resolver, exactly as A7 specified)

**Cluster I subtotal: 2 + 2 + 2 + 3 = 9 (weighted: 2×2 + 2×2 + 2×3 + 3×2 = 4+4+6+6 = 20 of max 27)**

### 2.2 Cluster II — Cell-level state (3 criteria)

#### C-2.1 — Per-cell state machine encoding (4 states + transitions + audit trail)

1. **Adapted.** EvidenceStateRecord schema carries a `state` field (enum of 4 values per A6 §2.1) and a `transitions` list (state-transition audit trail per A6 §2.7). Schema-level support is native. Materialization is per-cell YAML records — same materialization burden as C-1.3.
2. **Cost: shared with C-1.3 materialization — incremental cost 0** (audit trail is already on the schema; materialization extracts both at once).
3. **Operational risk: low.** State machine is enumerated; invalid transitions are caught by `validate_evidence_state.py`. The risk is in materialization completeness, addressed in C-1.3.
4. **Downstream binding: high (shared with C-1.3).** Cell-level state drives synthesis rendering; without it, B5–B7 and Stage C cannot render evidence states.

**Score: 2** (adapted, moderate cost — schema-native, materialization-burdened)

#### C-2.2 — Multi-source attribution per cell

1. **Native.** The current Specification schema carries `cited_evidence: list[str]` referencing EvidenceSource records by ID. EvidenceStateRecord follows the same pattern. Multiple sources per cell is the default, not an extension.
2. **Cost: 0.** Already implemented in the schema layer.
3. **Operational risk: low.** Same as C-1.2 — N:N foreign-ID validation at CI time, not write time. Risk surface bounded.
4. **Downstream binding: low.** Synthesis rendering reads the list; no architectural impact downstream.

**Score: 3** (native — Pydantic schema implements multi-source attribution by default)

#### C-2.3 — Tier + evidence_type orthogonal encoding

1. **Native.** Per A6 §1.2 (T-03 operationalization), EvidenceSource schema carries `tier: int (1–6)` and `evidence_type: enum (9 values)` as separate fields. Validator enforces orthogonality (any tier can pair with any evidence_type). The schema implements T-03 directly.
2. **Cost: 0.** Already implemented.
3. **Operational risk: low.** Field-level enum + integer validation; loud at CI time.
4. **Downstream binding: low.** Synthesis and rendering read both fields independently.

**Score: 3** (native — T-03 operationalization is exactly this schema shape)

**Cluster II subtotal: 2 + 3 + 3 = 8 (weighted: 2×2 + 3×2 + 3×2 = 4+6+6 = 16 of max 18)**

### 2.3 Cluster III — Co-1 schema discipline (1 criterion)

#### C-3.1 — Six required Co-1 fields enforced; non-conformance blocked at write **[Weight 3]**

1. **Adapted.** Per A5 co1-operational.md §6.1, Co-1 EvidenceSource records require six fields: `tier`, `evidence_type`, `co1_provenance`, `co1_source_type`, `verification_status`, `synthesis_attribution_required`. Pydantic enforces required fields when the model is constructed — but Candidate A writes YAML directly to disk, where the model is not constructed until validation runs. So enforcement is at CI time, not at write time. The framework's wording was "non-conformance blocked at write" — Candidate A satisfies this at CI write (next push), not editor write (file save).
2. **Cost: 0–2 sessions** to add a pre-commit hook running the Co-1 validator. Not architectural; tooling layer.
3. **Operational risk: medium.** A non-conforming Co-1 record on disk between editor save and CI run is technically possible, but the window is short (commit, push, CI runs in ~minute). Solo-author workflow makes it bounded.
4. **Downstream binding: low.** The fields are present once enforced; downstream just reads them.

**Score: 2** (adapted, moderate cost — fields are schema-required, but enforcement is CI-time not editor-time; closing the gap requires a pre-commit hook)

**Cluster III subtotal: 2 (weighted: 2×3 = 6 of max 9)**

### 2.4 Cluster IV — Synthesis metadata (3 criteria)

#### C-4.1 — Convergence/divergence stored per cell

1. **Native.** EvidenceStateRecord nests a `ConvergenceAssessment` model with fields for which dimensions converged, which diverged, and on what reasoning. Schema implements A6 §3 directly.
2. **Cost: 0.** Implemented.
3. **Operational risk: low.**
4. **Downstream binding: low.** Rendering reads the nested model.

**Score: 3** (native)

#### C-4.2 — Values-criteria assessment stored per cell

1. **Adapted.** A6 §4 specifies values-criteria assessment outcome per cell (broadest-benefit verdict, population breadth, irreversibility, supplementary-provision feasibility). The current EvidenceStateRecord schema does not have a `values_criteria_assessment` nested model. Adding it is mechanical (new sub-model on the schema).
2. **Cost: 1 session** to add the schema sub-model + validator + populate for existing cells (low volume — only cells where values-criteria assessment was performed).
3. **Operational risk: low.** New required fields default to optional during transition; tightening to required on a follow-up commit.
4. **Downstream binding: low.** Rendering reads the nested model when present.

**Score: 2** (adapted, moderate cost — schema extension is mechanical, but the field set isn't there yet)

#### C-4.3 — Meta-methodological citations distinguishable from evidence sources at schema layer

1. **Adapted.** A6 §5 specifies that meta-methodological citations (Schön, ICF, PEO/PEOP, Capability, Kawa) are outside the seven-tier hierarchy and not assigned `tier` or `evidence_type`. Current EvidenceSource schema has `tier` and `evidence_type` as required. Distinguishing meta-methodological requires either (a) a separate entity type `MetaMethodologicalCitation` with distinct schema, or (b) making `tier`/`evidence_type` optional with an `is_meta_methodological: bool` flag. (a) is the cleaner schema choice.
2. **Cost: 1–2 sessions** for option (a) — new schema module, new YAML directory, validator.
3. **Operational risk: low.** Separate entity isolates the divergence cleanly.
4. **Downstream binding: low.** Synthesis machinery either includes or excludes meta-methodological citations explicitly per A6 §5.

**Score: 2** (adapted, moderate cost — schema bifurcation is clean but not yet present)

**Cluster IV subtotal: 3 + 2 + 2 = 7 (weighted: 3×2 + 2×2 + 2×2 = 6+4+4 = 14 of max 18)**

### 2.5 Cluster V — Verification (2 criteria)

#### C-5.1 — Verification-status state machine integrated with cell state

1. **Native.** EvidenceSource schema carries `verification_status` (enum of 5 values per A6 §2.8). EvidenceStateRecord can reference it through the citing-source linkage. A6 §2.8 specified the cell-state interaction (e.g., a cell citing only UNVERIFIED-1 sources cannot be state=stated).
2. **Cost: 0–1 session** for the cross-validator that enforces the cell-state ↔ verification-status interaction at CI time.
3. **Operational risk: low.** Cross-validator is the same pattern as `validate_cross_refs.py`.
4. **Downstream binding: low.**

**Score: 3** (native — the schema fields and validator pattern are in place; cross-validator is the only addition)

#### C-5.2 — Evidence markers ●/○ enforced per specification sentence

1. **Adapted.** Project-standards Core Doctrine + A6 specify that every spec sentence carries a marker: ● (filled) or ○ (empty). In Candidate A, markers live in markdown body text; enforcement requires a markdown-aware validator that parses spec sentences and checks for marker presence. Such a validator is not implemented; one would parse `specification.body` markdown and run a regex per sentence boundary.
2. **Cost: 1–2 sessions** to build the markdown-spec-marker validator.
3. **Operational risk: medium.** Markdown sentence boundary detection is an inexact problem — line-level checks are easier; sentence-level requires a sentence-tokenizer (nltk or similar). The validator's accuracy bounds the enforcement strength.
4. **Downstream binding: medium.** Marker presence drives evidence-state interpretation downstream. Inaccurate enforcement leaks unmarked sentences into synthesis.

**Score: 1** (adapted, high cost — markdown-aware sentence-level validator is non-trivial; sentence boundary detection is the cost driver)

**Cluster V subtotal: 3 + 1 = 4 (weighted: 3×2 + 1×2 = 6+2 = 8 of max 12)**

### 2.6 Cluster VI — Cross-cutting axes (1 criterion)

#### C-6.1 — DesignStage × ProjectType filter dimension

1. **Native.** A3 §1.3 specifies cross-cutting axes as optional list attributes (Specification.applicable_design_stages, Specification.applicable_project_types). Pydantic models implement them. Filter queries traverse via a query-layer scan.
2. **Cost: 0** for storage; the query layer needs to expose the filter (1 session at B5).
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — list-attribute filter dimensions are exactly the markdown+YAML form's bread and butter)

**Cluster VI subtotal: 3 (weighted: 3×2 = 6 of max 6)**

### 2.7 Cluster VII — Navigation / audience (4 criteria)

#### C-7.1 — Information-finding query mode

1. **Adapted.** Audience-priority §Information-finding requires fast lookup across spec/parameter/population. In Candidate A, this is implemented as a query-layer scan over YAML files. For the corpus size (78 BPCs, ~531 EvidenceSource, 188 connections, 73 specifications), full-scan is tractable but not native — a relational substrate would index this.
2. **Cost: 2–3 sessions** to build query layer with caching/indexing for the audience-priority modes.
3. **Operational risk: medium.** Query performance degrades as corpus grows; pre-launch corpus is bounded but post-launch growth depends on Stage C scope.
4. **Downstream binding: medium.** All audience modes depend on the query layer being adequate.

**Score: 1** (adapted, high cost — building a query/index layer over markdown+YAML is non-trivial; the query layer is itself a sub-architecture decision Sessions 3 must bound — this is the framework §7.1 strain pattern surfacing)

#### C-7.2 — Decision-frame query mode

1. **Adapted.** Same query-layer concern as C-7.1; the decision-frame mode requires filtering by population × design-stage × parameter-class.
2. **Cost: shared with C-7.1.**
3. **Operational risk: same.**
4. **Downstream binding: same.**

**Score: 1** (same reasoning as C-7.1)

#### C-7.3 — Representation-checking query mode

1. **Adapted.** Filter by population to surface specifications with thin coverage. Same query-layer concern.
2. **Cost: shared.**
3. **Operational risk: same.**
4. **Downstream binding: same.**

**Score: 1** (same reasoning)

#### C-7.4 — Questions-led query mode (B3 specifies; storage must accept) **[Weight 3]**

1. **Adapted.** B3 will specify the Question entity (ENT-20). Candidate A accepts new entity types without migrating existing entities (per C-1.1). Once B3 ships the schema, the query mode is "filter by Question.applies_to_population × Question.parameter_class" — same pattern as C-7.1–7.3.
2. **Cost: shared.** When B3 ships, the additional query-layer cost is incremental — adding a question-aware filter to the existing query layer.
3. **Operational risk: low.** Question entity addition does not affect existing entities; query layer extension is the same pattern as the other navigation modes.
4. **Downstream binding: low.** B3 specifies its own schema; B5 renderers read questions like any other entity.

**Score: 2** (adapted, moderate cost — extensibility is native per C-1.1, but the query mode itself shares the C-7.1 query-layer cost; the score is 2 not 1 because the questions-led mode does not add architectural complexity beyond the base query layer)

**Cluster VII subtotal: 1 + 1 + 1 + 2 = 5 (weighted: 1×2 + 1×2 + 1×2 + 2×3 = 2+2+2+6 = 12 of max 27)**

This is Candidate A's worst cluster. The query-layer cost is the dominant factor.

### 2.8 Cluster VIII — Time model (4 criteria)

#### C-8.1 — Entity-level versioning per A9

1. **Adapted.** A9 schema (`schemas/temporal.py`) is implemented with 7 classes (VersionTag, EffectiveDateRange, GuidebookVersion, StandardEdition, ProjectRule, SupersedenceLink, LaunchPhaseRecord). Materialization into `data/temporal/` is partial — the directory does not exist in the current repo state per §1.3. The retrofit converter (`scripts/convert/version_retrofit.py` per A9 §7) needs to run.
2. **Cost: 2–3 sessions** for the retrofit converter to populate `data/temporal/` from `references/project-standards.md` + `references/standards-registry.md` + `versions/`. Specified in A9; not yet built.
3. **Operational risk: medium.** Retrofit is a one-shot extraction from markdown sources; if the parser misclassifies a RULE block, the temporal record is wrong. Mitigation: PROVISIONAL link state for ambiguous cases; manual review.
4. **Downstream binding: medium.** D-05 stale-evidence detection (B2 query layer) and CS3 versioning operations (Stage C) read temporal records.

**Score: 2** (adapted, moderate cost — schema is in place, materialization is the work)

#### C-8.2 — SupersedenceLink representation (5 link types)

1. **Native.** SupersedenceLink schema is implemented with `link_type` enum covering A9's 5 link types (document_version, standard, project_rule, source, launch_phase). A9 §6.5 specifies cycle detection at validator level.
2. **Cost: 0** for schema; **1 session** for the cycle-detection validator (`validate_temporal.py` per A9 §6).
3. **Operational risk: low.** Cycles caught at CI time.
4. **Downstream binding: low.** Validator runs once per push.

**Score: 3** (native)

#### C-8.3 — Standards-edition tracking + freshness windows

1. **Adapted.** Standards registry currently in markdown form (`references/standards-registry.md`) with structured YAML blocks per entry. A9 §7.4 specifies converter to populate `data/temporal/standards/` per-jurisdiction-per-family. Freshness windows are tier-keyed; no per-source `last_verified` field on most existing EvidenceSource records.
2. **Cost: 2 sessions** — converter (shared with C-8.1) + back-populating `last_verified` on Tier 1–3 sources (volume work, ~531 records but most just need a flag set).
3. **Operational risk: low.** Window evaluation is a date arithmetic; loud at CI time when exceeded.
4. **Downstream binding: low.** B2 validator runs the window check.

**Score: 2** (adapted, moderate cost)

#### C-8.4 — Stale-evidence detection at query time **[Weight 1 per D-0110]**

1. **Adapted (storage prereq) / not assessed at storage layer (query layer).** Per D-0110 §3.3, stale-evidence detection is a query-layer concern. Storage prereq is light — `year`, `last_verified`, `tier`, `evidence_type` fields. EvidenceSource has all four. Differentiation between candidates happens at query layer (B2), not storage layer (B1).
2. **Cost: 0 at storage layer.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — storage prereq satisfied; the differentiation deferred to B2)

**Cluster VIII subtotal: 2 + 3 + 2 + 3 = 10 (weighted: 2×2 + 3×2 + 2×2 + 3×1 = 4+6+4+3 = 17 of max 21)**

### 2.9 Cluster IX — Operational (5 criteria)

#### C-9.1 — CI validation tractability **[Weight 1]**

1. **Native.** CI is wired and operational. 5 jobs (Schema validation, Structure validation, Syntax check, Governance, Commit-msg). 16 validator scripts.
2. **Cost: 0.** Already operative.
3. **Operational risk: low.** Per session_2026-04-30-ci-s1, CI integration is mature; 2 jobs currently red are tracked under GAP-082 and predate this session.
4. **Downstream binding: low.**

**Score: 3** (native — Candidate A's CI is the project's incumbent CI; no candidate beats this)

#### C-9.2 — Solo-author operability without team infrastructure **[Weight 2]**

1. **Native.** Markdown + YAML edits with a text editor + git push + CI. No database server, no graph store, no schema migration tooling required at write time. Solo-author workflow is the workflow.
2. **Cost: 0.**
3. **Operational risk: low.** This is the lowest-risk operability profile of any candidate.
4. **Downstream binding: low.** Stage C operations under solo-author posture remain compatible.

**Score: 3** (native — Candidate A is what solo-author operability looks like)

#### C-9.3 — Audit-trail preservation across migration from current state **[Weight 1]**

1. **Native.** No migration required; the current state IS Candidate A. 2,259+ git commits preserved. Audit trail is the git history.
2. **Cost: 0.**
3. **Operational risk: 0.**
4. **Downstream binding: 0.**

**Score: 3** (native — there is no migration; audit trail is git history)

#### C-9.4 — Migration cost from current 1,098 records **[Weight 1]**

1. **Native.** No migration; cost is 0 sessions.
2. **Cost: 0.**
3. **Operational risk: 0.**
4. **Downstream binding: 0.**

**Score: 3** (native — there is no migration)

#### C-9.5 — A10/A12/A13 integration cost **[Weight 2]**

1. **Native.** A10 catalog under `data/adversarial_use/`, A12 register under `data/decisions/`, A13 cadence under `data/doctrine_recheck/` are all implemented in Candidate A's form. CI validators exist for each (audit_adversarial_use.py, decision_capture.py, doctrine_recheck.py).
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — A10/A12/A13 implementations are Candidate A as it stands)

**Cluster IX subtotal: 3 + 3 + 3 + 3 + 3 = 15 (weighted: 3×1 + 3×2 + 3×1 + 3×1 + 3×2 = 3+6+3+3+6 = 21 of max 21)**

This is Candidate A's strongest cluster. Operationally, the candidate is the project's incumbent state.

### 2.10 Cluster X — Sustainability (3 criteria)

#### C-10.1 — Format longevity (12+ year horizon, no specialized tooling) **[Weight 1]**

1. **Native.** Markdown + YAML are plaintext. Readable in any text editor. Format longevity is the longevity of UTF-8, ASCII, and structured-text conventions — measured in decades.
2. **Cost: 0.**
3. **Operational risk: 0.**
4. **Downstream binding: 0.**

**Score: 3** (native — plaintext formats are the longest-lived formats currently available)

#### C-10.2 — Tool independence (no vendor lock-in for read access) **[Weight 1]**

1. **Native.** Any text editor reads the corpus. Pydantic schemas are open-source Python; the YAML files parse with any YAML library in any language.
2. **Cost: 0.**
3. **Operational risk: 0.**
4. **Downstream binding: 0.**

**Score: 3** (native)

#### C-10.3 — Migration-out cost bounded (per D-0111 5-deliverable standard) **[Weight 2]**

Per D-0111, evaluate against the 5 deliverables:

1. **Full data export.** Native — the data IS the export. Markdown + YAML files copy as-is.
2. **Relationship preservation.** Native — N:N relationships are foreign-ID lists; polymorphic refs are string IDs; inheritance is `inherits_from` field. All preserve in copy.
3. **State preservation.** Native — cell-level state, verification status, supersedence chains, audit trails all live in the YAML records or git history.
4. **Schema mapping document.** Required — Candidate A has Pydantic schemas; mapping to relational, graph, or other targets is mechanical given the schema definitions. The mapping document is ~1 session of work.
5. **Export tooling cost.** ≤2 sessions: tar+gzip the corpus is the trivial export; semantic export to a target form is the schema mapping above. **Within budget.**

All 5 deliverables satisfied. **PASS.**

**Score: 3** (native — Candidate A's migration-out is `git clone`)

**Cluster X subtotal: 3 + 3 + 3 = 9 (weighted: 3×1 + 3×1 + 3×2 = 3+3+6 = 12 of max 12)**

---

## 3. Score summary

### 3.1 Per-criterion score table

| Criterion | Cluster | Weight | Score | Weighted |
|---|---|---|---|---|
| C-1.1 Entity-type expressiveness | I | 2 | 2 | 4 |
| C-1.2 Relationship-type expressiveness | I | 2 | 2 | 4 |
| C-1.3 Within-population variability | I | 3 | 2 | 6 |
| C-1.4 Sub-population inheritance | I | 2 | 3 | 6 |
| C-2.1 Cell-level state machine | II | 2 | 2 | 4 |
| C-2.2 Multi-source attribution | II | 2 | 3 | 6 |
| C-2.3 Tier + evidence_type orthogonal | II | 2 | 3 | 6 |
| C-3.1 Six required Co-1 fields | III | 3 | 2 | 6 |
| C-4.1 Convergence/divergence per cell | IV | 2 | 3 | 6 |
| C-4.2 Values-criteria assessment per cell | IV | 2 | 2 | 4 |
| C-4.3 Meta-methodological citations distinct | IV | 2 | 2 | 4 |
| C-5.1 Verification-status state machine | V | 2 | 3 | 6 |
| C-5.2 Evidence markers ●/○ enforced | V | 2 | 1 | 2 |
| C-6.1 DesignStage × ProjectType filter | VI | 2 | 3 | 6 |
| C-7.1 Information-finding query mode | VII | 2 | 1 | 2 |
| C-7.2 Decision-frame query mode | VII | 2 | 1 | 2 |
| C-7.3 Representation-checking query mode | VII | 2 | 1 | 2 |
| C-7.4 Questions-led query mode | VII | 3 | 2 | 6 |
| C-8.1 Entity-level versioning | VIII | 2 | 2 | 4 |
| C-8.2 SupersedenceLink representation | VIII | 2 | 3 | 6 |
| C-8.3 Standards-edition + freshness | VIII | 2 | 2 | 4 |
| C-8.4 Stale-evidence detection | VIII | 1 | 3 | 3 |
| C-9.1 CI validation tractability | IX | 1 | 3 | 3 |
| C-9.2 Solo-author operability | IX | 2 | 3 | 6 |
| C-9.3 Audit-trail preservation | IX | 1 | 3 | 3 |
| C-9.4 Migration cost from current | IX | 1 | 3 | 3 |
| C-9.5 A10/A12/A13 integration cost | IX | 2 | 3 | 6 |
| C-10.1 Format longevity | X | 1 | 3 | 3 |
| C-10.2 Tool independence | X | 1 | 3 | 3 |
| C-10.3 Migration-out cost (S-05) | X | 2 | 3 | 6 |

### 3.2 Cluster totals

| Cluster | Weighted score | Max | Ratio |
|---|---|---|---|
| I — Entity & relationship | 20 | 27 | 74% |
| II — Cell-level state | 16 | 18 | 89% |
| III — Co-1 schema discipline | 6 | 9 | 67% |
| IV — Synthesis metadata | 14 | 18 | 78% |
| V — Verification | 8 | 12 | 67% |
| VI — Cross-cutting axes | 6 | 6 | 100% |
| VII — Navigation / audience | 12 | 27 | 44% |
| VIII — Time model | 17 | 21 | 81% |
| IX — Operational | 21 | 21 | 100% |
| X — Sustainability | 12 | 12 | 100% |
| **Total** | **132** | **171** | **77%** |

Per-criterion arithmetic verified mechanically: 30 criteria, weighted sum 132, max 171.

---

## 4. Distinguishing strengths and weaknesses

### 4.1 Strengths (clusters at 100% or near)

- **Cluster IX Operational (100%)** — Candidate A IS the project's incumbent; CI, A10/A12/A13, solo-author workflow are operative.
- **Cluster X Sustainability (100%)** — plaintext formats are unmatched on longevity, tool independence, migration-out.
- **Cluster VI Cross-cutting axes (100%)** — list-attribute filter dimensions are the markdown+YAML form's natural expression.
- **Cluster II Cell-level state (89%)** — Pydantic schemas implement A6 §2 directly; the only sub-100% criterion is C-2.1 materialization.
- **Cluster VIII Time model (81%)** — A9 schema is implemented; only materialization is outstanding.

### 4.2 Weaknesses (clusters below 70%)

- **Cluster VII Navigation / audience (44%)** — the dominant weakness. Query-layer cost dominates: 3 of 4 criteria score 1 (high-cost adaptation). The query/index layer over markdown+YAML is non-trivial. C-7.4 (questions-led, weight 3) scores 2 because once the query layer exists, extension to questions is incremental; but the query layer itself is the load-bearing cost.
- **Cluster III Co-1 schema discipline (67%)** — single criterion at 2 because enforcement is CI-time not editor-time. Pre-commit hook closes the gap.
- **Cluster V Verification (67%)** — C-5.2 evidence-marker enforcement is the cost driver (markdown sentence-tokenization).
- **Cluster I Entity & relationship (74%)** — within-population variability materialization (C-1.3, weight 3) is the cost driver here; not architectural but volume.

### 4.3 Cost summary (sessions to reach native scoring on all criteria)

| Work | Sessions | Notes |
|---|---|---|
| Schema additions (5 missing entity types) | 5–7 | C-1.1 |
| Cell materialization (78 BPCs × ~20 populations) | 6–10 | C-1.3, C-2.1 (shared) |
| Pre-commit hook for Co-1 fields | 1 | C-3.1 |
| Values-criteria assessment sub-model | 1 | C-4.2 |
| Meta-methodological citation entity | 1–2 | C-4.3 |
| Markdown sentence-marker validator | 1–2 | C-5.2 |
| Query/index layer (audience modes) | 2–3 | C-7.1, C-7.2, C-7.3, C-7.4 |
| A9 retrofit converter + materialization | 2–3 | C-8.1, C-8.3 |
| **Total to reach near-native** | **19–29 sessions** | |

This 19–29 session cost is the materialization and query-layer build-out for Candidate A. It does not include the Stage B–C scope already planned (B2 tooling, B4 pilot, etc.) which any candidate would also incur.

### 4.4 What this score does NOT mean

- It does not mean Candidate A is the selected form. Selection is Sessions 7–9 after Sessions 4–6 produce comparable scores for B, C, D.
- It does not mean Candidate A is dismissed. 77% is a strong baseline; the question Sessions 7–8 must answer is whether B, C, or D outscore A enough to justify their migration, operational, and sustainability costs.
- It does not mean the score is final. Sessions 4–6's evaluations of B, C, D may surface considerations that reframe a Candidate A criterion. The framework's lock principle (D-0113) prevents silent reframing but permits superseding D-METH amendments where the reframe is justified.

---

## 5. Decision-capture for this session

One record. The evaluation itself is mechanical application of D-0108/D-0110/D-0111/D-0112/D-0113 — D-OP/DG-AUTO under the established framework. Captured for audit-trail completeness.

### 5.1 D-0119 — Candidate A scored 132 / 171 (77%)

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0113 |

DG-AUTO because the evaluation applies the framework + weighting + lock as specified. No methodological commitment added.

---

## 6. Status

| Field | Value |
|---|---|
| B1 Session 3 | COMPLETE |
| Candidate A score | 132 / 171 (77%) |
| Distinguishing strength clusters | IX Operational (100%), X Sustainability (100%), VI Cross-cutting (100%) |
| Distinguishing weakness clusters | VII Navigation/audience (44%), V Verification (67%), III Co-1 (67%) |
| Decisions captured | D-0119 |
| Working session counter | incremented 4 → 5 |
| Session log | `sessions/session_2026-05-01-b1-s3.md` |
| Predecessor | `sessions/session_2026-05-01-b1-s2.md` (B1 Session 2) and `sessions/session_2026-05-01-audit-remediation.md` (parallel-context, audit remediation) |
| Next session | B1 Session 4 — Candidate B (Relational) per-criterion evaluation |

---

## 7. Session 4 next-action

**Session 4 = Candidate B (Relational) per-criterion evaluation.**

Candidate B is one of: SQLite, PostgreSQL, DuckDB. The within-Candidate-B sub-substrate decision is itself a Session-4 sub-decision per framework §5.2. Session 4 evaluates B at the candidate level (does relational satisfy each criterion?) and surfaces the sub-substrate question if the candidate survives.

Inputs: this file; Session 1 framework; Session 2 weighting; A6, A9, A10, A12 full reads; relational-form characterization (Pydantic-to-SQLAlchemy mapping; SQLite single-file viability; query-mode satisfaction via SQL views).

Output: `workplan/b1-candidate-b-relational.md`. ~400 lines.
