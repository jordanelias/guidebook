# B1 — Derivation Framework
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 1 of 6–9 (per workplan-co0007-v3 §B1 budget)
**Status:** IN PROGRESS — framework established; candidate evaluation begins Session 3
**Predecessor session:** `sessions/session_2026-04-30-ci-s1.md` (Stage A operational close — CI integration sub-session)
**Operative plan:** `workplan/workplan-co0007-v3.md` §B1 + `workplan/workplan-co0007-v3-amendments.md`
**Model routing for this session:** opus/150/synth
**Final B1 outputs (later sessions):** `architecture/storage-derivation.md` · `architecture/schema-spec.md` · `architecture/storage-decision.md`

This file is the in-progress derivation framework. It seeds — but is not — the final `architecture/storage-derivation.md`. Sessions 2–9 extend, narrow, and ultimately commit the architecture artifacts under `architecture/`. This file remains under `workplan/` as the working register of how B1 reached its conclusion.

---

## 1. B1 mandate (verbatim from operative plan)

Per `workplan/workplan-co0007-v3.md` §B1:

> Reframed per N-05. B1 evaluates ≥3 storage forms against requirements before committing… Output is the chosen form with derived rationale, the schema spec, and the dismissed alternatives with reasons. Time model from A9 implemented in schema (resolves D-05 + L-04 in storage layer). Schema validators run in CI.

### 1.1 Findings B1 resolves

| Finding | Disposition | What B1 does |
|---|---|---|
| **N-05** Architectural form asserted | PRIMARY | Derives form from ≥3 candidates against requirements |
| **L-04** Three version-aware requirements | PARTIAL | A9 specified the time model; B1 implements it at the storage layer |
| **D-05** Time-as-data deferred | PARTIAL | A9 specified; B1 implements in schema; C1 activates operationally |

### 1.2 Findings B1 does NOT resolve (carried by other phases)

| Finding | Owner |
|---|---|
| **N-01** Pilot conflates failure modes | B4 (multi-pilot construction) |
| **N-09** Single-pilot fragile | B4 |
| **D-04** Epistemic defense doc-only | A6 spec (LANDED); C2 build; CS doctrine-recheck operates |
| **T-03** Co-1 tier encoding | RESOLVED (Stage 0.5 + A6 §1.2) |
| **T-04** Sparse-evidence behavior | RESOLVED (Stage 0.5 + A6 §2) |
| **T-02** Questions claim no rendering | B3 (navigation modes) |

### 1.3 Doctrinal anchors that bind B1 (carried forward; not relitigated)

- Mission §Purpose — questions over prescription; equip readers to ask better questions
- Mission §Doctrinal commitment 1 — within-population variability is **first-class data**, not narrative caveat
- Mission §Doctrinal commitment 3 — Co-1 evidence is co-primary with Tier 1
- Mission §Doctrinal commitment 6 — questions-led teaching; questions are first-class data
- A6 §1.2 — `tier` (1–6) + `evidence_type` are orthogonal fields on EvidenceSource
- A6 §2.1 — cell-level state machine: `stated` · `provisional` · `pending` · `not_applicable`
- A6 §3 — convergence/divergence are synthesis metadata, not state-machine states
- A6 §4 — values-criteria assessment outputs an explicit broadest-benefit verdict
- A5 §6.1 (`co1-operational.md`) — six required schema fields on Co-1 citations
- A7 — population taxonomy with sub-population hierarchy + inheritance
- A9 — five temporal axes; SupersedenceLink primitive; freshness windows per evidence tier
- A10 — adversarial-use review log keyed to active/in-prep version
- A12 — decision-register references entities; CS8 capture-pair-with-RULE active
- A13 — doctrine-recheck cadence (counter); contamination resampling; baseline-against snapshots

The storage form must support all of these, not just accommodate them.

---

## 2. What this session is and is not

### 2.1 This session produces

1. Requirements inventory (this file §4) — the things the storage form must do, encode, permit, and survive
2. Candidate set (§5) — four storage forms; v3 names ≥3, B1 names four to leave the floor uncrossed
3. Derivation criteria (§6) — questions Sessions 3–6 will answer for each candidate
4. Per-criterion question template (§6.1) — uniform interrogation structure
5. First-pass candidate × criterion-cluster sketch (§7) — surfaces where each candidate prima-facie strains; pre-empts wasted Session 3–6 effort
6. Session arc (§8) — Sessions 2–9 plan
7. Open questions for Session 2 (§9)
8. Two decision-capture records (§10; written to `data/decisions/decision_register.yaml`)

### 2.2 This session does NOT produce

- A storage form selection (Sessions 7–9)
- Per-candidate evaluation (Sessions 3–6)
- Schema specification (Sessions 7–9; lands as `architecture/schema-spec.md`)
- Repo strategy revision (B1 close per `governance/repo-strategy.md` §Trigger; Session 9)
- Weighted scoring of criteria (Session 2; framework here is unweighted)
- Declared candidate winner or pre-judged dismissal (anti-pattern: prejudgment masquerading as derivation)

---

## 3. Inputs assembled this session

Loaded in two GraphQL batch reads across 6 governance documents + roadmap + operative plan + amendments. All were read — not skimmed — under `<document_reading>` `max` rules. References to specific section numbers below cite the version of these documents read at session open (commit `4954bcc` plus operational sub-session updates through `0d9551cd`).

| Document | Why loaded |
|---|---|
| `workplan/roadmap-2026-04-27.md` | B1 budget, gates, position in stage sequence |
| `workplan/workplan-co0007-v3.md` | B1 verbatim mandate; finding cross-references |
| `workplan/workplan-co0007-v3-amendments.md` | Whether any amendment touches B1 (it does not) |
| `governance/conceptual-model.md` (A3) | Entity inventory; relationship map; cross-cutting axes |
| `governance/mission-and-epistemics.md` | Doctrinal commitments the storage form must support |
| `governance/audience-priority.md` | Use-pattern catalogue; conflict rules constrain navigation |
| `governance/pre-stage-a-decisions.md` | T-03, T-04, D-03 framings B1 inherits |
| `governance/evidence-methodology.md` (A6) | State machine, convergence/divergence, values-criteria, verification interaction |
| `governance/repo-strategy.md` | Repo-decision revisit trigger keyed to B1 |
| `governance/workplan-adoption.md` | C2 cut-list; budget context |
| `references/project-standards.md` | Locked rules that constrain schema (e.g. evidence markers ●/○; CS8 capture-pair-with-RULE) |
| `references/connections/_index.md` | Connection register surface; entity connection (E-04) shape |
| Live state: `schemas/`, `scripts/`, `data/` directory listing | Current implemented schema set as starting point |

A6 was read in full headers + selected sections (Schema/State/Encoding/values-criteria/design-pedagogy/epistemic-defense/convergence). Other documents were read complete.

---

## 4. Requirements inventory

The storage form must satisfy four bands. Each requirement is sourced to a specific governance commitment. Sourcing is not decoration — Sessions 3–6 evaluate candidates against this inventory; if the inventory is wrong, the evaluation is wrong.

### 4.1 Functional requirements — what the storage form must support

| ID | Requirement | Source | Note |
|---|---|---|---|
| F-01 | Persist ~20 entity types (10 schemed in A3; 10 deferred to A4–post-launch) | A3 §1.1–1.2 | Currently 6 entity types under Pydantic + 1098 records |
| F-02 | Encode N:N relationships (item↔room, population↔specification, conflict↔specification, item↔item) | A3 §2 | N:N is the dominant relationship pattern |
| F-03 | Encode polymorphic references (Gap.blocks → any entity) | A3 §2 | Polymorphism on Gap is canonical |
| F-04 | Cell-level state per (parameter × population) | A6 §2.1 | The four-state machine is the unit of synthesis |
| F-05 | Multi-source attribution per cell (multiple `EvidenceSource` records cite into one cell) | A6 §3 + A3 §2.1 | Convergence/divergence requires this |
| F-06 | Cross-cutting axes as filter dimensions (DesignStage × ProjectType) | A3 §1.3 | Implemented as optional list attributes; storage form must support filter queries on them |
| F-07 | Connection register (E-04): item↔item with status, confidence, target, opus_review flag | A3 §1.1 + connections/_index.md | 188 records currently |
| F-08 | Within-population variability as first-class data dimension | Mission §1 | A6 §2.x rendering depends on this; not a narrative caveat field |
| F-09 | Sub-population hierarchy + inheritance | A7 | Sub-codes (e.g. NDV/AUT, MOB/AMB) inherit population properties unless overridden |
| F-10 | Question entity (E-20) when B3 specifies it | Mission §6 + roadmap §5 B3 | Questions are first-class data per mission; storage form must accept this without retrofit |
| F-11 | Cross-reference resolvability (REF-IDs, CON-IDs, item codes, slugs) | project-standards Endnote/Source Pipeline | Currently enforced by `validate_cross_refs.py` |
| F-12 | Conflict entity (E-09) with intra-individual / inter-group / both classifications | Project-standards 2026-03-28 21:30 | Deferred from A3; lands at A6 or B1 depending on candidate form |

### 4.2 Epistemic requirements — what the storage form must encode

| ID | Requirement | Source |
|---|---|---|
| E-01 | `tier` (1–6) AND `evidence_type` (9-value enum) as orthogonal fields on EvidenceSource | A6 §1.2 (T-03 operative) |
| E-02 | Cell-level evidence-state (`stated` / `provisional` / `pending` / `not_applicable`) with rationale required for `not_applicable` and gap-link required for `pending` | A6 §2 (T-04 operative) |
| E-03 | Co-1 evidence: six required schema fields per A5 §6.1 (`tier`, `evidence_type`, `co1_provenance`, `co1_source_type`, `verification_status`, `synthesis_attribution_required`) | governance/co1-operational.md §6.1 |
| E-04 | Synthesis metadata for convergence/divergence per cell (which dimensions converged/diverged; which governs and on what reasoning) | A6 §3 |
| E-05 | Values-criteria assessment outcome per cell (broadest-benefit verdict; population breadth; irreversibility; supplementary-provision feasibility) | A6 §4.2 |
| E-06 | State-transition audit trail (which transitions occurred when, why) | A6 §2.7 |
| E-07 | Verification status: `UNVERIFIED-1` / `UNVERIFIED-CLOSED` / `VERIFIED` / `VERIFIED-WITH-CORRECTION` / `CLOSED-DELETED` with state-machine-state interaction per A6 §2.8 | A6 §2.8 |
| E-08 | Evidence markers ● (filled) / ○ (empty) per specification sentence | project-standards Core Doctrine + A6 |
| E-09 | Meta-methodological citations classification (Schön, ICF, PEO/PEOP, Capability, Kawa) — outside the seven-tier hierarchy; not assigned `tier` or `evidence_type`; not validated by evidence-state validator | A6 §5 |

### 4.3 Operational requirements — what the storage form must permit

| ID | Requirement | Source |
|---|---|---|
| O-01 | Mechanical CI validation per CO-0008 governance+code methodology | project-standards 2026-04-26 06:20 + Enforcement Gates |
| O-02 | Pre-launch solo-author operability: a single person can read, edit, and validate without team infrastructure | mission §Operational reality + D-03 revised |
| O-03 | Audit trail preservation (currently 2,259+ commits in `jordanelias/guidebook` `main`) | governance/repo-strategy.md §Rationale 2 |
| O-04 | Time-model integration: A9's five temporal axes; SupersedenceLink primitive; freshness windows per evidence tier | A9 (governance/time-model.md) |
| O-05 | Adversarial-use review machinery integration (A10 catalog + per-version review_log) | A10 (governance/adversarial-use-framework.md) |
| O-06 | Decision-register references entities by stable ID across renames | A12 §3 capture protocol |
| O-07 | Doctrine-recheck cadence operability: contamination resampling source data; baseline-against snapshots | A13 (governance/doctrine-recheck.md) |
| O-08 | Render-ability across audiences: markdown (primary), web (B1 stage informs), questions-led (B3 specifies), jurisdiction-comparison (A8) | audience-priority §Content production + roadmap §B3 |
| O-09 | Migration tractability from current state (1,098 records under A3 schemas; ~78 BPC files; ~531 EvidenceSource records; 191 connections; 73 specifications) | A3 §1.1 record counts |
| O-10 | Cross-stage threads (CS1 doctrine-recheck, CS3 versioning, CS6 standards monitoring, CS8 decision capture, CS9 adversarial-use review) operate against the storage form | roadmap §7 |

### 4.4 Sustainability requirements — what the storage form must survive

| ID | Requirement | Source |
|---|---|---|
| S-01 | Format longevity: readable in 12+ years without specialized tooling | v3 §Decision authority list (#21 — "B1 storage form (12+ year implication)") |
| S-02 | Tool independence: survives loss of any single proprietary tool (no vendor lock-in for read access) | mission §Test items 1, 7 (clean data + transparent methodology) |
| S-03 | Solo-author maintainability: does not require team to operate; does not require ongoing infrastructure ops | mission §Operational reality (solo-only-permanent is a possible end-state) |
| S-04 | Versioning resilience: SupersedenceLink history survives storage-form migrations within the project lifetime | A9 §SupersedenceLink + CS3 |
| S-05 | Migration-out cost is bounded and documented: if B1's choice is later overturned, the corpus can leave with its semantics intact | derivation principle: do not pick a form that traps the project in itself |

### 4.5 Inventory totals

12 functional · 9 epistemic · 10 operational · 5 sustainability = **36 requirements**.

These are the requirements; criteria in §6 are derived from them.

---

## 5. Candidate forms

Four forms. v3 §B1 names ≥3; this session names four. Each form is described in enough detail to evaluate, not to advocate. **Selection happens in Sessions 7–9, not here.**

### 5.1 Candidate A — Structured markdown + YAML frontmatter (status quo extended)

The current state, made more rigorous. Entities live as markdown files with YAML frontmatter (BPC entries, slug records, governance documents). Pure-data entities live as YAML files in `data/`. Cross-references resolve through file-path conventions and explicit ID tables. Validation is Pydantic + bespoke validators in `scripts/`.

**What it inherits from current state:**
- `data/decisions/decision_register.yaml` (107 records, single YAML file)
- `data/adversarial_use/catalog.yaml` (catalogue + per-version review_log files)
- `data/doctrine_recheck/{snapshot,sample,recheck,counter}.yaml`
- `bpc/{slug}/` directories with `bpc.md` (frontmatter) + `search-log.md`
- `parts/` markdown for prose
- `references/` for non-entity reference material

**Extension under this candidate:**
- Atomic parameter cells migrate to per-cell YAML files OR a single large YAML keyed by (parameter × population) — a Session-3 sub-decision
- Connection register decomposes into per-CON-ID YAML rather than the current index.md table
- All entity types schemed with Pydantic; everything else is prose

### 5.2 Candidate B — Relational database with views

Atomic entities normalized into tables. Cells are rows. Sources are rows. Citations are join-table rows. Views compose markdown for rendering. Migration: bulk extract from current YAML/markdown into SQL; thereafter, edits go through application or schema-aware tooling.

**Concrete implementation directions B1 must consider:**
- SQLite single-file (sustainability friendly; format is documented and readable)
- PostgreSQL (richer features; vendor risk if hosted)
- DuckDB (analytical query patterns suit the audience use-patterns)

The choice within Candidate B is itself a sub-decision deferred to Session 4 if Candidate B survives Session 3 sketch.

### 5.3 Candidate C — Graph database / triplestore

Entities are nodes; relationships are edges with types. Cells are property maps on edges or sub-nodes depending on substrate. RDF/JSON-LD with a triplestore + reasoner expresses convergence/divergence and inheritance natively. Property graphs (Neo4j et al.) are easier to operate but require more bespoke modelling for cell-level state.

**Concrete implementation directions:**
- RDF/JSON-LD with Apache Jena or Blazegraph
- Neo4j property graph
- Memgraph / TigerGraph (vendor risk dimensions)

The choice within Candidate C is deferred to Session 5 if Candidate C survives.

### 5.4 Candidate D — Hybrid (split storage by entity nature)

Different entities live in different stores: tabular entities (Specification, EvidenceSource, BPC metadata) in a relational store; relationship-heavy entities (Connection, Conflict) in a graph store; prose (mission, governance, parts) in markdown. A coordination layer exposes a unified read/write API.

**Risk dimension:** complexity. Two stores' worth of operational burden against one author. The candidate is included because v3 §B1's named candidate set includes hybrid-as-option; if Sessions 3–5 show no single substrate satisfies the requirement set, hybrid surfaces as the residual answer.

---

## 6. Derivation criteria

Criteria cluster the 36 requirements into evaluable surfaces. Each cluster maps to a band of related requirements; each criterion within a cluster is an evaluable question Sessions 3–6 will answer per candidate.

### 6.1 Per-criterion question template (uniform across Sessions 3–6)

For each (candidate × criterion) cell, Sessions 3–6 answer four questions:

1. **Native, adapted, or absent?** Does the candidate satisfy this criterion natively, only with adaptation work, or not at all?
2. **Adaptation cost?** If adapted, in sessions and complexity. If absent, in workaround cost or scope reduction.
3. **Operational risk?** What can go wrong in solo-author operation? What does failure look like?
4. **Downstream binding?** What does this criterion's verdict force on Stages B5–B7 and Stage C? (Cluster VIII and IX in particular bind heavily.)

The 4-question template is the same for every cell to keep cross-candidate comparison legible.

### 6.2 Criteria clusters (24 criteria across 10 clusters)

| Cluster | ID | Criterion | Sourced from |
|---|---|---|---|
| **I. Entity & relationship** | C-1.1 | Entity-type expressiveness across the 20 A3 types | F-01 |
| | C-1.2 | Relationship-type expressiveness (1:N, N:N, polymorphic) | F-02, F-03 |
| | C-1.3 | Within-population variability as first-class data | F-08 |
| | C-1.4 | Sub-population inheritance | F-09 |
| **II. Cell-level state** | C-2.1 | Per-cell state machine encoding (4 states + transitions + audit trail) | F-04, E-02, E-06 |
| | C-2.2 | Multi-source attribution per cell | F-05 |
| | C-2.3 | Tier + evidence_type orthogonal encoding | E-01 |
| **III. Co-1 schema discipline** | C-3.1 | Six required Co-1 fields enforced; non-conformance blocked at write | E-03 |
| **IV. Synthesis metadata** | C-4.1 | Convergence/divergence stored per cell | E-04 |
| | C-4.2 | Values-criteria assessment stored per cell | E-05 |
| | C-4.3 | Meta-methodological citations distinguishable from evidence sources at schema layer | E-09 |
| **V. Verification** | C-5.1 | Verification-status state machine integrated with cell state | E-07 |
| | C-5.2 | Evidence markers ●/○ enforced per specification sentence | E-08 |
| **VI. Cross-cutting axes** | C-6.1 | DesignStage × ProjectType filter dimension | F-06 |
| **VII. Navigation / audience** | C-7.1 | Information-finding query mode | F-10, O-08 + audience |
| | C-7.2 | Decision-frame query mode | audience-priority |
| | C-7.3 | Representation-checking query mode | audience-priority |
| | C-7.4 | Questions-led query mode (B3 specifies; storage must accept) | mission §6, F-10 |
| **VIII. Time model** | C-8.1 | Entity-level versioning per A9 | O-04, L-04 |
| | C-8.2 | SupersedenceLink representation (5 types) | O-04, A9 |
| | C-8.3 | Standards-edition tracking + freshness windows | A9 freshness windows |
| | C-8.4 | Stale-evidence detection at query time | D-05, A9 |
| **IX. Operational** | C-9.1 | CI validation tractability | O-01 |
| | C-9.2 | Solo-author operability without team infrastructure | O-02, S-03 |
| | C-9.3 | Audit-trail preservation across migration from current state | O-03 |
| | C-9.4 | Migration cost from current 1,098 records under A3 schemas | O-09 |
| | C-9.5 | A10/A12/A13 integration cost | O-05, O-06, O-07 |
| **X. Sustainability** | C-10.1 | Format longevity (12+ year horizon, no specialized tooling) | S-01 |
| | C-10.2 | Tool independence (no vendor lock-in for read access) | S-02 |
| | C-10.3 | Migration-out cost bounded | S-05 |

That is 30 criteria clustered into 10 clusters. (24 was the Session-1 estimate; the actual count after sourcing is 30.)

### 6.3 Weighting (deferred to Session 2)

Criteria are not weighted in Session 1. Session 2 weights them with the requirements inventory frozen — weighting after candidates are evaluated invites bias toward whatever scored best on lightly-considered criteria. Weighting structure under consideration for Session 2:

- All-equal (default null hypothesis)
- Tiered (Critical / Important / Nice-to-have) with explicit assignment per criterion
- Doctrinal-anchor weighted (criteria sourced from mission/A6 weighted higher than criteria sourced from operational convenience)

Session 2 commits the weighting scheme and writes it into `b1-criteria-weighting.md`.

---

## 7. First-pass candidate × criteria sketch

This is **not the evaluation**. It is the calibration sketch — a coarse-grained read of where each candidate prima-facie strains, surfaced now to direct Session 3–6 effort. Cells use one of:

- **native** — the form supports this without adaptation
- **adapt** — supportable with non-trivial schema or tooling work
- **strain** — the form fights this requirement; significant cost or scope reduction

| Cluster | A: Markdown + YAML | B: Relational | C: Graph | D: Hybrid |
|---|---|---|---|---|
| I. Entity & relationship | adapt (N:N awkward in YAML; works via convention) | native | native | native |
| II. Cell-level state | adapt (validator-enforced; no native cell concept) | native | native | native |
| III. Co-1 fields | native (Pydantic enforced; current state) | native (NOT NULL) | native | native |
| IV. Synthesis metadata | adapt | native | native (RDF reified statements) | native |
| V. Verification | native (current Pydantic) | native | native | native |
| VI. Cross-cutting axes | native | native | native | native |
| VII. Navigation/audience | strain (must build query layer) | native (views) | native (Cypher / SPARQL) | native |
| VIII. Time model | strain (versioning is git-history; not query-able) | adapt (temporal patterns; bi-temporal modelling) | adapt (versioned RDF; named graphs) | mixed |
| IX. Operational | native (zero migration; solo-friendly) | strain (DB ops; migration cost) | strain (substrate learning; solo-friendly question) | strain (two stores' ops) |
| X. Sustainability | native (plaintext; tool-independent) | adapt (DB longevity is moderate; SQLite particularly stable) | strain (RDF tooling churn; graph DB longevity weaker than relational) | mixed |

### 7.1 What the sketch surfaces

Three patterns are visible at first pass:

1. **Candidate A is operationally and sustainably strong but expressively strained.** A surviving Candidate A would require building a query/view layer — that itself is a sub-architecture decision Sessions 3 must scope.
2. **Candidates B and C are expressively native but operationally and sustainably costly.** A surviving Candidate B or C would need to demonstrate that its expressive native-ness pays for its operational cost in a solo-author pre-launch context.
3. **Candidate D's hybrid burden may make it strictly dominated** by either A-with-query-layer or B-with-prose-as-files. Session 6 tests this.

These patterns are **not conclusions**. They are guides for where Session 3–6 effort should concentrate. Sessions 3–6 may invert these readings entirely.

### 7.2 What the sketch must not be used for

The sketch must **not** be cited in Session 7's selection rationale. Selection rationale cites the per-cell evaluation in Sessions 3–6, not this calibration sketch. Treating the sketch as evidence is the prejudgment failure mode.

---

## 8. Session arc (B1 Sessions 2–9)

| Session | Focus | Primary output | Lands in |
|---|---|---|---|
| 1 (this) | Framework | `b1-derivation-framework.md` | `workplan/` |
| 2 | Requirements lock + criteria weighting | `b1-criteria-weighting.md` + frozen requirements | `workplan/` |
| 3 | Candidate A evaluation (per-criterion 4-question template) | `b1-candidate-a-markdown-yaml.md` | `workplan/` |
| 4 | Candidate B evaluation | `b1-candidate-b-relational.md` | `workplan/` |
| 5 | Candidate C evaluation | `b1-candidate-c-graph.md` | `workplan/` |
| 6 | Candidate D evaluation | `b1-candidate-d-hybrid.md` | `workplan/` |
| 7 | Comparative scoring + dismissed-alternatives drafting | `b1-comparative-scoring.md` | `workplan/` |
| 8 | Selection + derivation writeup | `architecture/storage-derivation.md` (final) | `architecture/` |
| 9 | Schema spec + repo strategy revisit | `architecture/schema-spec.md` + `architecture/storage-decision.md` + revision to `governance/repo-strategy.md` | `architecture/` + `governance/` |

### 8.1 Session arc compression rules

- Sessions 3–6 may compress to 2–3 sessions total if a candidate's strain pattern collapses in early evaluation (e.g. Candidate D shown strictly dominated by Sessions 3–4).
- Sessions 7–8 may merge if comparative scoring produces an obvious winner; if scoring is close, they remain separate.
- Total budget remains 6–9 sessions. Compression is not extension.

### 8.2 Session arc expansion triggers

- A surviving Candidate B or C needs sub-substrate selection (SQLite vs PostgreSQL vs DuckDB; RDF vs property-graph) — this is a Session-internal sub-decision under the relevant candidate's evaluation, not a new session.
- If Sessions 3–6 surface a fifth candidate that no source explicitly named (e.g. a content-addressed merkle store), Session 6 evaluates it and the arc extends by one session. Trigger: a present session's reading reveals a credible candidate that satisfies a requirement no listed candidate satisfies.

### 8.3 What Session 9 closes

- Final architecture/ artifacts committed
- `governance/repo-strategy.md` revised per its §Trigger
- `architecture/storage-decision.md` includes audit-trail entry per `governance/decision-protocol.md` (D-METH/DG-NON; storage form is in A12's always-DG-NON list)
- B1 close session log; B2 (tooling design) handoff

---

## 9. Open questions for Session 2

These are explicit deferrals — not unresolved-because-overlooked. Session 2 must address each.

1. **Weighting scheme.** All-equal vs tiered vs doctrinal-anchor-weighted. §6.3.
2. **L-04 partial scope.** v3 §B1 says B1 "implements" the time model in the storage layer (resolves D-05 + L-04 in storage layer). Session 2 must confirm exactly which of A9's five temporal axes are storage-layer concerns vs query-layer concerns vs render-layer concerns. The split affects which criteria in Cluster VIII bind storage choice.
3. **D-05 partial scope.** v3 says "Time-handling integrated from this point onward" activates at C1, with B1 implementing the schema-layer hooks. Session 2 must confirm whether stale-evidence detection (C-8.4) is a storage-layer requirement or a query-layer requirement under the chosen form. If the latter, C-8.4 weights lower in storage selection.
4. **Question entity (E-20) timing.** B3 specifies the Question entity. B1 must accept that without retrofit. Session 2 confirms the minimum schema commitment B1 makes for E-20 acceptance.
5. **Migration-out specification.** S-05 requires a bounded, documented migration-out cost. Session 2 specifies what a satisfactory exit-plan looks like — schema export, semantic preservation, downstream tool independence — so each candidate is evaluated against the same exit standard.
6. **Hybrid eliminator test.** §7.1 conjecture: Candidate D may be strictly dominated. Session 2 specifies the test that would establish dominance (or fail to). Testing happens in Session 6.

---

## 10. Decision-capture for this session

Two records are appended to `data/decisions/decision_register.yaml` at session commit. Per A12 §3 the records are written before the implementing commit; the implementing commit OID is captured in `decision_artifacts` at session close.

### 10.1 D-0108 — Adopt 4-candidate × 30-criterion derivation framework for B1

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| decision_artifacts | this file; data/decisions/decision_register.yaml; sessions/session_2026-04-30-b1-s1.md |

### 10.2 D-0109 — B1 session arc (Sessions 2–9 plan)

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | not_required |
| model_routing | opus/100/route |
| effort_level | 100 |

DG-AUTO because session arcs are routine sequencing under an established framework (D-0108). The decision is captured for audit-trail completeness, not for review.

---

## 11. What this file does not do

- Does not select a storage form (Sessions 7–9)
- Does not weight criteria (Session 2)
- Does not pre-judge any candidate (§7.2)
- Does not commit `architecture/` files (Sessions 8–9)
- Does not revise `governance/repo-strategy.md` (Session 9)
- Does not define the Question entity schema (B3)
- Does not specify validators (B2)
- Does not relitigate T-03, T-04, or T-06 (resolved upstream)

---

## 12. Status

| Field | Value |
|---|---|
| B1 Session 1 | COMPLETE |
| Framework status | LOCKED for Session 2 input; criteria weighting deferred per §6.3 |
| Decisions captured | D-0108, D-0109 |
| Working session counter | incremented 1 → 2 |
| Session log | `sessions/session_2026-04-30-b1-s1.md` |
| Predecessor session | `sessions/session_2026-04-30-ci-s1.md` |
| Next session | B1 Session 2 — requirements lock + criteria weighting |
