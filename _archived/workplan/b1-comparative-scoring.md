# B1 Session 7 — Comparative Scoring + Dismissed-Alternatives Drafting
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 7 of 6–9
**Status:** Cross-candidate comparison among A, B, C; selection-question framed for Session 8
**Predecessor session:** `sessions/session_2026-05-02-b1-s6.md` (Candidate D dismissed under D-0112)
**Operative governance:** D-0108, D-0110, D-0111, D-0113, D-0119, D-0121, D-0132, D-0134
**Model routing:** opus/150/synth

---

## 1. Session purpose

Session 7 produces the cross-candidate comparison among Candidates A, B, C. It does NOT make the selection — that is Session 8. It produces the inputs Session 8 uses to make the selection: per-criterion comparison matrix, weighted-difference analysis, selection-question framing, and dismissed-alternatives draft.

Per D-0134, Candidate D is dismissed; Sessions 7–9 input set is {A, B, C}.

### 1.1 Per-candidate weighted totals (recap)

| Candidate | Score | Cost (sessions to reach near-native) |
|---|---|---|
| A — Markdown + YAML | 132 / 171 (77%) | 19–29 |
| B — Relational / SQLite | 152 / 171 (89%) | 27–42 |
| C — Graph / RDF (Apache Jena) | 155 / 171 (91%) | 34–50 |

---

## 2. Per-criterion comparison matrix

The full per-criterion table from extracted A, B, C scores. **Bold** in the "best" column indicates a candidate that *uniquely* outscores the other two on that criterion (no ties at the top).

| Criterion | W | A | B | C | Best | Unique winner? |
|---|---|---|---|---|---|---|
| C-1.1 Entity-type expressiveness | 2 | 2 | 3 | 3 | B/C | — |
| C-1.2 Relationship-type expressiveness | 2 | 2 | 3 | 3 | B/C | — |
| C-1.3 Within-population variability **[W3]** | 3 | 2 | 3 | 3 | B/C | — |
| C-1.4 Sub-population inheritance | 2 | 3 | 2 | 3 | A/C | — |
| C-2.1 Cell-level state machine | 2 | 2 | 3 | 3 | B/C | — |
| C-2.2 Multi-source attribution | 2 | 3 | 3 | 3 | A/B/C | — |
| C-2.3 Tier + evidence_type orthogonal | 2 | 3 | 3 | 3 | A/B/C | — |
| C-3.1 Six required Co-1 fields **[W3]** | 3 | 2 | 3 | 3 | B/C | — |
| C-4.1 Convergence/divergence per cell | 2 | 3 | 3 | 3 | A/B/C | — |
| C-4.2 Values-criteria assessment | 2 | 2 | 3 | 3 | B/C | — |
| C-4.3 Meta-methodological distinction | 2 | 2 | 3 | 3 | B/C | — |
| C-5.1 Verification-status state machine | 2 | 3 | 3 | 3 | A/B/C | — |
| C-5.2 Evidence markers ●/○ enforced | 2 | 1 | 2 | 2 | B/C | — |
| C-6.1 DesignStage × ProjectType filter | 2 | 3 | 3 | 3 | A/B/C | — |
| C-7.1 Information-finding query | 2 | 1 | 3 | 3 | B/C | — |
| C-7.2 Decision-frame query | 2 | 1 | 3 | 3 | B/C | — |
| C-7.3 Representation-checking query | 2 | 1 | 3 | 3 | B/C | — |
| C-7.4 Questions-led query mode **[W3]** | 3 | 2 | 3 | 3 | B/C | — |
| C-8.1 Entity-level versioning per A9 | 2 | 2 | 2 | 3 | **C** | **C unique** |
| C-8.2 SupersedenceLink representation | 2 | 3 | 3 | 3 | A/B/C | — |
| C-8.3 Standards-edition + freshness | 2 | 2 | 3 | 3 | B/C | — |
| C-8.4 Stale-evidence detection | 1 | 3 | 3 | 3 | A/B/C | — |
| C-9.1 CI validation tractability | 1 | 3 | 2 | 1 | **A** | **A unique** |
| C-9.2 Solo-author operability | 2 | 3 | 2 | 1 | **A** | **A unique** |
| C-9.3 Audit-trail preservation | 1 | 3 | 1 | 1 | **A** | **A unique** |
| C-9.4 Migration cost from current | 1 | 3 | 1 | 1 | **A** | **A unique** |
| C-9.5 A10/A12/A13 integration cost | 2 | 3 | 1 | 1 | **A** | **A unique** |
| C-10.1 Format longevity | 1 | 3 | 2 | 3 | A/C | — |
| C-10.2 Tool independence | 1 | 3 | 2 | 3 | A/C | — |
| C-10.3 Migration-out cost (S-05) | 2 | 3 | 3 | 3 | A/B/C | — |

### 2.1 Unique-winner analysis

| Candidate | Unique winner on | Total criteria where unique | Weighted points from unique wins |
|---|---|---|---|
| A | C-9.1, C-9.2, C-9.3, C-9.4, C-9.5 | 5 (all of Cluster IX where A=3 and B/C<3) | 3+(2×3)+3+3+(2×3) = 21 weighted score from these criteria; weighted advantage over best-of-others = (3-2)×1 + (3-2)×2 + (3-1)×1 + (3-1)×1 + (3-1)×2 = 1+2+2+2+4 = **+11 weighted points over best-of-(B,C)** |
| B | (none) | **0** | B never strictly exceeds both A and C on any criterion |
| C | C-8.1 | 1 (C=3 vs A=2 and B=2) | (3-2)×2 = **+2 weighted points over best-of-(A,B)** |

**Critical observation: B has zero unique wins.** B never strictly outscores both A and C on any criterion. B's value proposition is its consistency — high score on most criteria — not unique advantage.

**A has 5 unique wins, all in Cluster IX (operational).** A's value proposition is operational nativeness — the candidate IS the project's incumbent state.

**C has 1 unique win (C-8.1, A9 versioning via named graphs).** C's value proposition is expressive richness on the time model and entity relationships, with W3C-standardization sustainability.

### 2.2 Cluster-level comparison

| Cluster | Max | A | B | C | A% | B% | C% | Notes |
|---|---|---|---|---|---|---|---|---|
| I — Entity & relationship | 27 | 20 | 25 | 27 | 74% | 93% | 100% | C native (RDFS); B near-native; A adapted |
| II — Cell-level state | 18 | 16 | 18 | 18 | 89% | 100% | 100% | B/C tied; A near |
| III — Co-1 schema | 9 | 6 | 9 | 9 | 67% | 100% | 100% | B/C tied; A's CI-time enforcement = 67% |
| IV — Synthesis metadata | 18 | 14 | 18 | 18 | 78% | 100% | 100% | B/C tied; A schema gaps |
| V — Verification | 12 | 8 | 10 | 10 | 67% | 83% | 83% | B/C tied; A bounded by markdown sentence-tokenizer |
| VI — Cross-cutting axes | 6 | 6 | 6 | 6 | 100% | 100% | 100% | All native |
| VII — Navigation | 27 | 12 | 27 | 27 | 44% | 100% | 100% | B/C tied; A's query-layer cost dominant weakness |
| VIII — Time model | 21 | 17 | 19 | 21 | 81% | 90% | 100% | C native (named graphs); B near; A schema present, materialization pending |
| IX — Operational | 21 | 21 | 10 | 7 | 100% | 48% | 33% | A native (incumbent); C worst |
| X — Sustainability | 12 | 12 | 10 | 12 | 100% | 83% | 100% | A/C tied (plaintext + W3C); B SQLite tool-dependent |
| **Total** | **171** | **132** | **152** | **155** | **77%** | **89%** | **91%** | |

### 2.3 Cluster-level head-to-head

**A vs B:** B leads by 20 weighted points overall.
- B gains in Clusters I (+5), II (+2), III (+3), IV (+4), V (+2), VII (+15), VIII (+2). Total B gain: **+33 points.**
- B loses in Clusters IX (-11), X (-2). Total B loss: **-13 points.**
- Net: B +20.

**A vs C:** C leads by 23 weighted points overall.
- C gains in Clusters I (+7), II (+2), III (+3), IV (+4), V (+2), VII (+15), VIII (+4). Total C gain: **+37 points.**
- C loses in Cluster IX (-14). C ties on X. Total C loss: **-14 points.**
- Net: C +23.

**B vs C:** C leads by 3 weighted points.
- C gains in Cluster I (+2 — C-1.4 sub-population inheritance native to RDFS via subclass; B adapted), VIII (+2 — C-8.1 named graphs), X (+2 — W3C sustainability). Total C gain: **+6 points.**
- C loses in Cluster IX (-3 — B's 48% vs C's 33% on operational). Total C loss: **-3 points.**
- Net: C +3.

---

## 3. Selection-question framing

### 3.1 Three configurations of the selection question

The 3-way comparison resolves into three pairwise selection questions, each with a different shape:

#### 3.1.1 A vs (B or C) — operational nativeness vs expressive nativeness

- A's value: 5 unique wins in Cluster IX (operational). Migration cost 0. The candidate IS the project.
- B/C value: 23+ weighted-point gains in Clusters I/II/III/IV/V/VII/VIII (expressive richness). Migration cost 4–7 sessions just for migration; 27–50 sessions total to reach native scoring.
- **Selection question:** Is the operational native (A's 21/21 in Cluster IX) worth the 23+ weighted-point gap to C? Equivalently: does adapting A's query layer (19–29 sessions) cost less than migrating to B/C and rebuilding the validator stack?

A's adaptation reaches what ceiling? A's untouched score is 132. The 19–29 sessions of investment (cell materialization + query layer + missing schemas) push A into the same zone B and C occupy untouched. The asymptotic comparison is between A's adapted ceiling (~150–160) and B's untouched 152 / C's untouched 155.

**This selection question is genuinely close** — A's adapted ceiling sits in the same zone as B and C untouched. The framework's §7.1 strain pattern conjectured this would be the case.

#### 3.1.2 B vs C — relational consistency vs graph richness, with operational concerns

The B-vs-C comparison is the closest in raw score (3 points). It's also where the doctrinal binding from D-03 (solo-author pre-launch) bites hardest.

- C's structural gains: C-8.1 (named graphs for versioning), C-1.4 (RDFS subclass for inheritance), C-10.1/C-10.2 (W3C standardization).
- C's structural losses: Cluster IX entirely. SPARQL+SHACL+ontology cognitive load on a solo author. JVM CI dependency. Migration is the heaviest of three.
- B's structural gains: Cluster IX +3 over C. SQL is more solo-author-tractable than SPARQL. SQLite has no JVM dependency.
- B's structural losses: Cluster I/VIII/X totaling -6 over C.

**Selection question:** Does C's +6 expressive-richness gain justify the -3 operational loss given D-03's binding force? In dollar terms, what does the project pay each year (in solo-author time and cognitive load) to query SPARQL instead of SQL — and is the structural gain worth that recurring cost?

This question lives at the boundary of the doctrinal anchor: D-03 is binding, but the framework already assigned weights to operational criteria reflecting that binding. The 3-point B-vs-C gap survives the weight assignment. Session 8 must judge whether the framework's weights captured D-03's binding fully or whether the binding requires additional weight.

#### 3.1.3 A vs B vs C — three-way tradeoff frame

This is the actual selection. Three candidates with distinct profiles:

- **A — operational native, expressive adapted.** Adaptation ceiling ~150–160 with 19–29 sessions investment. No migration cost.
- **B — operational adapted, expressive near-native.** Untouched 152. 27–42 sessions of build-out + migration to reach native. 0 unique wins.
- **C — operational poor, expressive native.** Untouched 155. 34–50 sessions. 1 unique win on A9 versioning. Highest cognitive load.

The framework's §7.2 explicitly bars first-pass calibration sketches from selection rationale. Session 8 must reason from the per-criterion scores, the weighted totals, the doctrinal anchors, and the tradeoff structure — not from which calibration sketch happens to favor which candidate.

### 3.2 What Session 7 deliberately does not do

- Does not select. Session 8 selects.
- Does not weight the doctrinal anchors beyond what D-0110 already specified.
- Does not introduce new criteria.
- Does not amend the per-criterion scores (those are locked under D-0119, D-0121, D-0132).

### 3.3 Decision-rule options for Session 8

Three possible decision rules Session 8 could adopt (Session 7 surfaces; Session 8 commits to one):

**Rule 1 — Highest weighted total wins.** C selected (155 > 152 > 132). Mechanical; ignores cost-to-native and doctrinal binding beyond what weights captured.

**Rule 2 — Highest weighted total subject to doctrinal-anchor constraint.** Filter candidates that fail any weight-3 criterion (none does — all three are at score ≥ 2 on weight-3 criteria); then apply Rule 1. Same outcome as Rule 1 in this case (C selected) because none of the three fails a weight-3 criterion.

**Rule 3 — Tradeoff-aware selection.** Consider weighted total AND cost-to-native AND doctrinal binding force AND the project's pre-launch posture. Use the per-criterion comparison to identify which candidate's profile best fits the project's actual constraints — not which scores highest in the abstract.

Rule 3 is the framework's intent (§7 specifies that calibration sketches must not foreclose selection rationale; the rationale is structured deliberation about tradeoffs). Sessions 8–9 should adopt Rule 3.

**Under Rule 3, the selection question becomes:**

> Which candidate's profile — A's operational nativeness with expressive adaptation cost, B's relational consistency with moderate operational cost, or C's expressive nativeness with high operational cost — best fits the project's pre-launch solo-author posture (D-03), the 12+ year sustainability commitment (S-01, S-02), and the corpus's expected growth trajectory at Stage C?

This is the question Session 8 must answer.

---

## 4. Dismissed-alternatives draft

This section drafts the dismissed-alternatives summary for the architecture/storage-derivation.md final document (Session 8). It records which alternatives were considered and dismissed at each level.

### 4.1 Candidate-level dismissals

**Candidate D (Hybrid) — DISMISSED.**

Configuration evaluated: H1 (SQLite + Markdown + YAML). Score: 143/171 (84%, informational only). Eliminator test outcome: 0 wins, 18 ties, 12 losses across 30 criteria. Strictly dominated under D-0112's strict-dominance test.

Pivotal criterion: C-5.2 (sentence-level evidence-marker enforcement). The hybrid form did not provide a structural advantage over Candidate B alone or Candidate A with structured-marker convention. The structured-marker advantage (H1' variant) is form-agnostic; it does not uniquely belong to the hybrid.

Configuration H2 (RDF + SQLite, no markdown for prose) dismissed by transitivity: H2's operational scores are necessarily worse than H1's, and H2 cannot satisfy any criterion H1 cannot.

Decision records: D-0133 (substrate H1), D-0134 (dismissal), D-0135 (informational score).

### 4.2 Within-Candidate-B sub-substrate dismissals

**PostgreSQL — DISMISSED within Candidate B per D-0120.**

Server process adds operational discipline that solo-author pre-launch posture (D-03) does not need. PostgreSQL's ecosystem advantages (replication, advanced features) are post-launch concerns; pre-launch they are operational overhead without value-add.

**DuckDB — DISMISSED within Candidate B per D-0120.**

File format longevity is materially weaker than SQLite (younger project, single steward, format breaks have occurred). Analytical-query strength does not compensate at the project's data volume; the audience-priority modes are well-served by indexed SQLite.

Operative substrate within Candidate B: **SQLite**.

### 4.3 Within-Candidate-C sub-substrate dismissals

**Blazegraph — DISMISSED within Candidate C per D-0131.**

Project deprecated 2020 (acquired by Amazon Neptune team; codebase no longer actively maintained for general release). Format longevity at risk; tool independence eroding. Selecting Blazegraph would inherit the project's unmaintained status as a transitive risk.

**Neo4j — DISMISSED within Candidate C per D-0131.**

Single-vendor steward (Neo4j Inc.); proprietary query language Cypher partially standardized as openCypher but Neo4j's implementation diverges; format longevity contingent on vendor commitment. Tool independence is not present in the W3C-standards sense available to RDF/Jena.

**Memgraph / TigerGraph — DISMISSED within Candidate C per D-0131.**

Vendor-risk concentration similar to Neo4j; smaller ecosystems; format longevity contingent on commercial viability of single vendors.

Operative substrate within Candidate C: **RDF / Apache Jena (TDB embedded mode)**.

### 4.4 Surviving alternatives entering Session 8

Three single-substrate candidates with operative sub-substrates:

| Candidate | Operative sub-substrate | Score |
|---|---|---|
| A | Markdown + YAML (current state extended) | 132/171 (77%) |
| B | SQLite | 152/171 (89%) |
| C | RDF / Apache Jena (TDB embedded) | 155/171 (91%) |

---

## 5. Decision-capture for this session

Two records.

### 5.1 D-0136 — Cross-candidate comparative scoring matrix produced

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0113, D-0119, D-0121, D-0132, D-0134 |

DG-AUTO. Mechanical assembly of the comparative matrix from per-candidate scores.

### 5.2 D-0137 — Selection decision rule = Rule 3 (tradeoff-aware)

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0136 |

DG-REVIEW because the choice of decision rule for Session 8's selection is itself a methodological commitment that constrains Sessions 8–9.

---

## 6. Status

| Field | Value |
|---|---|
| B1 Session 7 | COMPLETE |
| Cross-candidate comparison | A 132/171 (77%) · B 152/171 (89%) · C 155/171 (91%) |
| Unique winners | A: 5 criteria (Cluster IX); B: 0; C: 1 (C-8.1) |
| Selection-question shape | Three-way tradeoff frame; Rule 3 (tradeoff-aware) committed under D-0137 |
| Dismissed-alternatives draft | Candidate D (D-0134); PostgreSQL/DuckDB within B (D-0120); Blazegraph/Neo4j/Memgraph/TigerGraph within C (D-0131) |
| Decisions captured | D-0136, D-0137 |
| Working session counter | 9 → 10 |
| Session log | `sessions/session_2026-05-02-b1-s7.md` |
| Predecessor | `sessions/session_2026-05-02-b1-s6.md` |
| Next session | B1 Session 8 — Selection + architecture/storage-derivation.md final writeup |

---

## 7. Session 8 next-action

**Session 8 = Selection of operative storage form + architecture/storage-derivation.md final document.**

Inputs: All Sessions 1–7 deliverables; the comparative matrix from this session; the dismissed-alternatives draft; the per-candidate cost-to-native estimates.

Session 8 produces:
- The selection decision (one of A, B, C) under D-0137's Rule 3 (tradeoff-aware).
- `architecture/storage-derivation.md` — the canonical B1 deliverable per workplan v3 §B1. This is a D-DOCT decision per A12 §4 (storage form is item #21 on the DG-NON always-list — irrevocably governs synthesis structure for 12+ years). Decision record: D-0138 D-DOCT/DG-NON.
- A revision proposal for `governance/repo-strategy.md` (Session 9).

**Session 8 must NOT produce schema spec details — that is Session 9.**

The selection rationale in `architecture/storage-derivation.md` must:
- State the doctrinal anchors (mission §Doctrinal commitments 1, 3, 6; D-03 pre-launch solo-author; S-01 12+ year horizon)
- State the tradeoff (which weighted-point gain or loss across which clusters)
- Reason from the doctrinal anchors AND the tradeoffs to a selection
- Document why the dismissed candidates (and within-candidate alternatives) were not selected
- Be defensible as an artifact 12+ years from now when re-read by future maintainers
