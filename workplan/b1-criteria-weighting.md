# B1 Session 2 — Requirements Lock + Criteria Weighting
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 2 of 6–9
**Status:** Requirements LOCKED for Sessions 3–6; criteria weighted; six open questions from Session 1 §9 resolved
**Predecessor session:** `sessions/session_2026-05-01-b1-s1.md` (B1 Session 1 — derivation framework)
**Operative plan:** `workplan/workplan-co0007-v3.md` §B1 + amendments
**Framework anchor:** `workplan/b1-derivation-framework.md` (D-0108)
**Model routing for this session:** opus/150/synth

---

## 1. Session purpose

Session 1 established the framework and explicitly deferred (a) requirements inventory lock, (b) criteria weighting, (c) resolution of six open questions. This session closes those three deferrals so Sessions 3–6 can begin per-candidate evaluation against a frozen, weighted set.

The framework's §6.3 specifies that weighting must precede candidate evaluation — weighting after candidates are sketched introduces post-hoc bias toward whichever candidate scored well on lightly-considered criteria. This session honors that ordering.

---

## 2. Requirements inventory lock

### 2.1 Inventory unchanged from Session 1

The 36 requirements specified in `b1-derivation-framework.md` §4 are reviewed against the governance set in this session. No additions, no removals.

| Band | Count | Source documents |
|---|---|---|
| Functional (F-01..F-12) | 12 | A3 conceptual model; A6 evidence methodology; A7 population taxonomy; mission §Doctrinal commitments 1, 6; audience-priority |
| Epistemic (E-01..E-09) | 9 | A6 §§1–4; co1-operational.md §6.1; mission §Epistemic commitments; project-standards Core Doctrine |
| Operational (O-01..O-10) | 10 | CO-0008 methodology; A5 + D-03 (pre-launch solo); A9 time model; A10 adversarial-use; A12 decision capture; A13 doctrine-recheck; audience-priority §Content production; A3 record counts |
| Sustainability (S-01..S-05) | 5 | v3 §Decision authority list; mission §Test items; A9 SupersedenceLink + CS3 |

**Inventory frozen.** Sessions 3–6 evaluate candidates against this set. Any addition during Sessions 3–6 requires a superseding D-METH record under D-0108. Removals are not permitted (silent compression failure mode per audit B-01).

### 2.2 What lock means operationally

A frozen requirement means three things:

1. **No silent dropping.** A candidate cannot be evaluated against a subset of the inventory; if the candidate "doesn't apply" to a requirement, the evaluation explicitly states that and treats it as absent (score 0), not as not-relevant.
2. **No silent reframing.** Sessions 3–6 cannot reinterpret a requirement to make a candidate look stronger. The text in §4 of the framework is the authoritative wording.
3. **Addition requires superseding decision.** If a Session 3–6 evaluation surfaces a requirement that should have been in §4 but wasn't, the right move is to halt evaluation, capture a D-METH/DG-REVIEW record amending D-0108 with the new requirement, then resume.

### 2.3 What lock does not mean

Lock does not mean the requirement set is correct. It means it is the set this round of evaluation operates on. Discovering an omission during Sessions 3–6 is not a procedural failure; the procedural failure would be folding the omission into an evaluation silently.

---

## 3. Resolution of Session 1 §9 open questions

### 3.1 Q1 — Weighting scheme

**Resolution: tiered weighting (3 / 2 / 1) with assignment rules keyed to source.**

The three options were all-equal (null hypothesis), tiered, and doctrinal-anchor-weighted. The chosen scheme combines the latter two: tiered buckets supply transparency (each criterion has an explicit, citeable weight), anchor-based assignment rules supply the rationale (the weight follows from where the criterion was sourced).

| Weight | Label | Assignment rule |
|---|---|---|
| **3** | Critical-binding | Criterion is sourced directly to mission §Doctrinal commitments 1, 3, or 6 — the project's foundational claims |
| **2** | Important-binding | Criterion is sourced to operationalization-binding governance: T-03, T-04, A3, A5, A6, A7, A8, A9, A10, A12, A13, audience-priority, project-standards |
| **1** | Operational-preference | Criterion is sourced to operational convenience (CI tractability, audit trail preservation) or sustainability concerns (longevity, tool independence) |

The rules are mechanical. Anyone can audit a weight by reading the criterion's source citation in §4 of the framework and applying the rule. The rules do not invite per-criterion judgment.

**Why not all-equal?** Mission commitments 1, 3, 6 are foundational; T-03 and T-04 operationalize them; CI tractability is a project-survival concern but not a doctrinal one. Treating all 30 criteria as equal would silently flatten the distinction. The audit-B-01 failure mode (silent compression) applies to weights as much as to wording.

**Why not pure doctrinal-anchor-only?** A pure scheme would assign higher weight only to criteria sourced from mission §Doctrinal commitments and 1 to everything else. That is too coarse — operationalization-binding criteria (e.g., A6's tier+evidence_type orthogonal encoding) are not optional; they are locked governance. Treating them at the same weight as "audit trail preservation across migration" misrepresents their force.

### 3.2 Q2 — L-04 storage-vs-query-vs-render split

**Resolution: Cluster VIII criteria are predominantly storage-layer; one criterion (C-8.4) is primarily query-layer.**

A9 (`governance/time-model.md`) specifies five temporal axes. The split is established by reading each axis against the storage / query / render distinction:

| A9 Axis | Storage layer (B1 binds) | Query layer (B2 binds) | Render layer (B5 + C9 bind) |
|---|---|---|---|
| §1 Document version | GuidebookVersion records; ACTIVE flag; supersedes field | "current version" lookup; cycle detection | filename pattern enforcement (validator, not render) |
| §2 Standards edition | Family + edition split per record; SupersedenceLink with link_type=standard; transition_until_date | edition-supersedence chain resolution; current-edition selection | transition-period citation flagging |
| §3 Project rule effective date | ProjectRule records; status enum (ACTIVE/SUPERSEDED/RETIRED); supersedes/superseded_by; pre-session anchor | "rule current at date D" lookup; PROVISIONAL link review | display rules (do not display normalized pre-session as authentic date) |
| §4 Source publication and verification | EvidenceSource year + last_verified + publication_date_iso fields; SupersedenceLink with link_type=source | freshness window evaluation; tier-aware window selection | freshness warning visibility (validator emits, render surfaces) |
| §5 Launch phase | LaunchPhaseRecord singleton; phase enum; transition history | phase-conditional validator behavior (e.g., co1_provenance value set) | (no render-layer concern at this phase) |

**The L-04 partial scope at the storage layer is therefore: persist the records in §§1–5 above with their typed fields and SupersedenceLink primitives.** This is a substantial commitment but a finite one — the storage form must support six new entity types (GuidebookVersion, StandardsRecord-with-edition, ProjectRule, the augmented EvidenceSource, LaunchPhaseRecord, SupersedenceLink) with their listed fields.

**Cluster VIII criteria mapped to this split:**

| Criterion | Layer | Implication for B1 weight |
|---|---|---|
| C-8.1 Entity-level versioning per A9 | storage | Full weight under tiered scheme — locked-governance binding |
| C-8.2 SupersedenceLink representation (5 link types) | storage (records) + query (cycle detection) | Full weight — the records are storage-layer |
| C-8.3 Standards-edition tracking + freshness windows | storage (records) + query (window evaluation) | Full weight on storage portion |
| C-8.4 Stale-evidence detection at query time | predominantly query (storage prereq is light: just persist year, last_verified, tier, evidence_type — already in EvidenceSource) | **Lower weight in B1** because the storage prereq is satisfied by all candidates with no differentiating cost |

C-8.4 is the only Cluster VIII criterion downgraded by this resolution. The criterion remains in §6.2 of the framework; its weight under §3.1's assignment rules drops from 2 (was: A9 operationalization-binding) to 1 (since the storage-layer fragment is light enough that no candidate's satisfaction differentiates from another's). The downgrade is captured as a sub-clause of D-0110.

### 3.3 Q3 — D-05 stale-evidence detection layer

**Resolution: stale-evidence detection is a query-layer concern with a light storage prerequisite. The storage prerequisite is the same field set referenced under Q2 §C-8.4.**

D-05 ("Time-as-data deferred") was specified by A9 as freshness windows + last_verified field + supersedence (A9 §4.3). The detection itself — "is this source past its window?" — is a computation over stored fields. Any storage form that persists `year`, `last_verified`, `tier`, and `evidence_type` on EvidenceSource records satisfies the prerequisite. All four candidates trivially satisfy it (the fields exist on the current Pydantic schema and persist into any of the four forms).

**Implication:** the differentiation between candidates on D-05 happens at the query layer (B2 — validator design), not the storage layer (B1). C-8.4 weight reflects this — see §3.2 above.

This resolution narrows the B1 scope on D-05. B1 implements the storage-layer hooks (the field set); B2 specifies the validator that does the detection; C1 activates the validator operationally.

### 3.4 Q4 — Question entity (ENT-20) minimum schema acceptance

**Resolution: B1 commits to "supports addition of new entity types of arbitrary structure without migrating existing entities." This is a property of the storage form, evaluated under criterion C-1.1 (entity-type expressiveness). No new criterion is introduced.**

B3 specifies the Question entity. B3 is several phases away. B1 cannot speculate on ENT-20's schema — that would prejudge B3's scope. What B1 can commit to is a property of the chosen storage form: the form must support adding new entity types without forcing migration of existing entities.

Operationalization in Sessions 3–6 evaluation:

When evaluating C-1.1 per candidate, the four-question template's question 1 ("native, adapted, or absent?") is answered with explicit attention to extensibility. The evaluation cell asks: "Can this form accept ENT-20 (or any other future entity type) when it lands, without requiring migration of the 20 existing entity types?"

| Candidate | Extensibility prima facie | Sessions-3–6 verifies |
|---|---|---|
| A: Markdown + YAML | Native — new entity types are new directories or YAML schemas; existing entities untouched | Confirm Pydantic schema additions don't break existing validation |
| B: Relational | Adapt — new entity types are new tables; existing tables untouched, but cross-references may need new join tables | Migration scripts required only for new cross-references, not for existing data |
| C: Graph | Native — new node types and edge types added without migration; existing data untouched | Schema reasoner/SHACL constraints expanded incrementally |
| D: Hybrid | Per-substrate — depends on which substrate the new entity lands in | Hybrid coordinator's mapping must accommodate new entity types |

This treatment subsumes Q4 into the existing criterion structure. No D-METH amendment to D-0108 is required.

### 3.5 Q5 — Migration-out specification (S-05)

**Resolution: each candidate's S-05 satisfaction is judged against five concrete export deliverables.**

S-05 from §4.4 of the framework: "Migration-out cost is bounded and documented: if B1's choice is later overturned, the corpus can leave with its semantics intact."

The exit standard:

1. **Full data export.** All 20 entity types' data (currently materialized: Specification, EvidenceSource, BPC, Connection, Slug, Gap; deferred: Population, Sub-population, Item, Conflict, Room/Space, Building Type, FDR Scenario, Search Log, Audience, Co-1 Collaborator, Specialist Handoff, Time-Version, Question, plus the six A9 entities under §3.2 above) are exportable to a generic interchange format. The interchange format depends on the candidate substrate but must be one of: CSV, JSON, JSON-LD, RDF/Turtle, or markdown.

2. **Relationship preservation.** N:N relationships, polymorphic references (Gap.blocks → any entity), and inheritance relationships (Sub-population → Population) are preserved in export, even where the export format does not natively express them — foreign-key tables for relational, reified statements for RDF, explicit ID columns for CSV/JSON.

3. **State preservation.** Cell-level state-machine values (`stated` / `provisional` / `pending` / `not_applicable`), verification statuses (`UNVERIFIED-1` / `UNVERIFIED-CLOSED` / `VERIFIED` / `VERIFIED-WITH-CORRECTION` / `CLOSED-DELETED`), supersedence chains, and audit trails are retained.

4. **Schema mapping document.** A specification mapping the candidate's storage primitives to a target form's primitives such that re-import into any of the other three candidates is mechanically tractable. Lossless re-import is not required; documented losses are. The schema mapping document is a deliverable artifact of the S-05 evaluation, not a hypothetical.

5. **Export tooling cost ≤ 2 sessions.** The export tool's specification fits within a 2-session build budget. If a candidate's export tooling specification exceeds that budget, S-05 is failed for that candidate. The 2-session bound matches the scale of one Stage A converter (e.g., A6's `convert_sources.py`).

This is captured as **D-0111 D-METH/DG-REVIEW**.

Each candidate must demonstrate satisfaction of all five deliverables to pass S-05 evaluation. A candidate that satisfies four of five fails the criterion (binary pass/fail at the criterion level; partial scoring not used for S-05).

### 3.6 Q6 — Hybrid eliminator test

**Resolution: Candidate D is eliminated if and only if no criterion shows it satisfying the requirement materially better than max(Candidate A, Candidate B, Candidate C). The test runs in Session 6 after Sessions 3–5 produce per-criterion candidate scores.**

Operationalization:

1. Sessions 3–5 produce per-candidate per-criterion scores 0–3 (0 = absent; 1 = adapted with high cost; 2 = adapted with moderate cost; 3 = native).
2. Session 6 evaluates Candidate D against the same 30 criteria, producing scores `D_i` for each criterion `i`.
3. For each criterion `i`, compute `M_i = max(A_i, B_i, C_i)`.
4. For Candidate D to survive elimination, the test requires: `∃ i such that D_i > M_i`.
5. If for all 30 criteria `D_i ≤ M_i`, Candidate D is **strictly dominated** and dismissed without further evaluation.
6. If for some criterion `D_i > M_i`, Candidate D survives. The criteria where D outscores its competitors are recorded as the candidate's distinguishing strengths and feed into Session 7 comparative scoring normally.

**Why strict dominance and not weighted-sum dominance?** A weighted-sum test could rule out D when D loses on weight-1 criteria but wins on a weight-3 criterion. That is the wrong dismissal. The strict-dominance test ensures D is dismissed only when no single criterion shows it as the best satisfier. This protects against the failure mode "hybrid is eliminated despite uniquely satisfying a doctrinal-binding criterion."

**Threshold question.** What counts as "materially better"? The test uses `D_i > M_i` (strict inequality on the integer scale 0–3). A tie (`D_i = M_i`) does not count as material betterment because the simpler form satisfies equivalently — Candidate D's complexity is not justified by tie-equivalent satisfaction.

This is captured as **D-0112 D-METH/DG-REVIEW**.

---

## 4. Per-criterion weight assignment

The 30 criteria from `b1-derivation-framework.md` §6.2 are now weighted under the §3.1 scheme. Source citations come from the framework's §4 requirements inventory.

### 4.1 Weight 3 — Critical-binding (3 criteria)

| Criterion | Source | Why critical-binding |
|---|---|---|
| **C-1.3** Within-population variability as first-class data | F-08 → mission §Doctrinal commitment 1 | Foundational mission claim that variability is first-class data, not narrative caveat |
| **C-3.1** Six required Co-1 fields enforced | E-03 → mission §Doctrinal commitment 3 + co1-operational.md §6.1 | Co-1 evidence co-primary with Tier 1 — schema discipline operationalizes the claim |
| **C-7.4** Questions-led query mode | F-10 → mission §Doctrinal commitment 6 | Questions are first-class data per pedagogy commitment; storage form must accept this without retrofit |

### 4.2 Weight 2 — Important-binding (21 criteria)

| Criterion | Source |
|---|---|
| C-1.1 Entity-type expressiveness across 20 A3 types | F-01 → A3 |
| C-1.2 Relationship-type expressiveness (1:N, N:N, polymorphic) | F-02, F-03 → A3 §2 |
| C-1.4 Sub-population inheritance | F-09 → A7 |
| C-2.1 Per-cell state machine encoding (4 states + transitions + audit trail) | F-04, E-02, E-06 → A6 §§2.1, 2.7 (T-04 operationalization) |
| C-2.2 Multi-source attribution per cell | F-05 → A6 §3 |
| C-2.3 Tier + evidence_type orthogonal encoding | E-01 → A6 §1.2 (T-03 operationalization) |
| C-4.1 Convergence/divergence stored per cell | E-04 → A6 §3 |
| C-4.2 Values-criteria assessment stored per cell | E-05 → A6 §4 |
| C-4.3 Meta-methodological citations distinguishable from evidence sources at schema layer | E-09 → A6 §5 |
| C-5.1 Verification-status state machine integrated with cell state | E-07 → A6 §2.8 |
| C-5.2 Evidence markers ●/○ enforced per specification sentence | E-08 → project-standards Core Doctrine + A6 |
| C-6.1 DesignStage × ProjectType filter dimension | F-06 → A3 §1.3 |
| C-7.1 Information-finding query mode | F-08, O-08 → audience-priority |
| C-7.2 Decision-frame query mode | audience-priority |
| C-7.3 Representation-checking query mode | audience-priority |
| C-8.1 Entity-level versioning per A9 | O-04, L-04 → A9 §1 |
| C-8.2 SupersedenceLink representation (5 link types) | O-04, A9 → A9 §§2–4 |
| C-8.3 Standards-edition tracking + freshness windows | A9 freshness windows → A9 §§2.3, 4.3 |
| C-9.2 Solo-author operability without team infrastructure | O-02, S-03 → A5 + D-03 (binding pre-launch reality) |
| C-9.5 A10/A12/A13 integration cost | O-05, O-06, O-07 → A10 + A12 + A13 (locked governance) |
| C-10.3 Migration-out cost bounded | S-05 → §3.5 above (D-0111) |

(Count: 21. The 17 figure in the §4.2 heading was a Session-2-draft estimate; the actual count after applying the assignment rules is 21. The header is corrected.)

### 4.3 Weight 1 — Operational-preference (6 criteria)

| Criterion | Source | Why weight 1 |
|---|---|---|
| C-8.4 Stale-evidence detection at query time | D-05, A9 | Storage prereq light; differentiation is query-layer (per §3.3 above) |
| C-9.1 CI validation tractability | O-01 | Operational convenience; project survives without CI native to the storage form (CI is added at the validator layer) |
| C-9.3 Audit-trail preservation across migration from current state | O-03 | Migration-time concern; equally satisfiable by all candidates with documentation |
| C-9.4 Migration cost from current 1,098 records | O-09 | One-time cost; does not bind the chosen form's long-term operation |
| C-10.1 Format longevity (12+ year horizon, no specialized tooling) | S-01 | Sustainability concern; partial differentiation across candidates but not doctrinal |
| C-10.2 Tool independence (no vendor lock-in for read access) | S-02 | Sustainability concern; mitigable through export tooling (S-05 / D-0111) |

### 4.4 Weight assignment reconciliation

| Weight | Count | Sum (weight × count) |
|---|---|---|
| 3 | 3 | 9 |
| 2 | 21 | 42 |
| 1 | 6 | 6 |
| **Total** | **30** | **57** |

Maximum candidate score (each criterion satisfied natively, score 3): 57 × 3 = **171**.

The frozen weight assignment is the input to Sessions 3–6 evaluation. Each candidate's evaluation produces a per-criterion score 0–3; the candidate's weighted total is `sum(weight_i × score_i)` across the 30 criteria.

---

## 5. Decision-capture

Four records appended to `data/decisions/decision_register.yaml`. All capture the methodological commitments this session makes.

### 5.1 D-0110 — Tiered weighting (3/2/1) + per-criterion assignment

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

### 5.2 D-0111 — Migration-out specification (S-05 operationalization)

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

### 5.3 D-0112 — Hybrid eliminator test

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

### 5.4 D-0113 — Requirements inventory locked under D-0108

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/100/route |
| effort_level | 100 |
| predecessors | D-0108 |

DG-AUTO because lock confirmation is mechanical under D-0108: Session 2 reviewed §4 of the framework against the governance set already in context and found no additions or removals warranted. Capture for audit-trail completeness.

---

## 6. Session 3 next-action

**Session 3 = Candidate A (Markdown + YAML status-quo-extended) per-criterion evaluation.**

Inputs to Session 3:
- This file (Session 2 deliverable; weighting + open questions resolved)
- `b1-derivation-framework.md` (Session 1; framework + 4 candidates + 30 criteria + 4-question template)
- Live state of repo: `data/`, `schemas/`, `scripts/`, `bpc/` directories — Candidate A's incumbent implementation
- A6 evidence-methodology, A9 time-model, A10 adversarial-use, A12 decision-protocol — re-read full headers + relevant sections per `<document_reading>` rules under max effort

Output: `workplan/b1-candidate-a-markdown-yaml.md` — per-criterion 4-question template applied to Candidate A across all 30 criteria. ~400–500 lines.

Session 3 does NOT compare A to B/C/D; that's Session 7. Session 3 produces A's standalone evaluation only.

---

## 7. What this file does not do

- Does not evaluate any candidate against any criterion (Sessions 3–6).
- Does not select a storage form (Sessions 7–9).
- Does not commit to ENT-20's schema (B3 specifies; B1 commits only to extensibility property under C-1.1).
- Does not specify validators (B2).
- Does not revise `governance/repo-strategy.md` (Session 9).

---

## 8. Status

| Field | Value |
|---|---|
| B1 Session 2 | COMPLETE |
| Requirements inventory | LOCKED for Sessions 3–6 |
| Criteria weighting | 3 critical-binding (weight 3) · 21 important-binding (weight 2) · 6 operational-preference (weight 1) — sum 57, max candidate score 171 |
| Six open questions from Session 1 §9 | All resolved; three (Q1, Q5, Q6) captured as D-METH records; three (Q2, Q3, Q4) absorbed into existing structure |
| Decisions captured | D-0110, D-0111, D-0112, D-0113 |
| Working session counter | incremented 2 → 3 |
| Session log | `sessions/session_2026-05-01-b1-s2.md` |
| Predecessor session | `sessions/session_2026-05-01-b1-s1.md` |
| Next session | B1 Session 3 — Candidate A evaluation |
