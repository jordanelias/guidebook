# B1 Session 5 — Candidate C Evaluation
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 5 of 6–9
**Candidate:** C — Graph / triplestore (RDF / property graph)
**Status:** Per-criterion evaluation complete; Candidate C scored against 30 criteria
**Predecessor session:** `sessions/session_2026-05-02-b1-s4.md` (Candidate B evaluation, 152/171)
**Operative governance:** D-0108, D-0110, D-0111, D-0112 (does not apply to Candidate C), D-0113
**Model routing:** opus/150/synth

---

## 1. Session purpose and scope

Apply the 4-question evaluation template (framework §6.1) to Candidate C (Graph / triplestore) across all 30 criteria. Within-Candidate-C sub-substrate sketch and selection are Session-5-internal sub-decisions per framework §5.2.

This session does NOT compare C to A/B/D — that is Session 7.

### 1.1 Inputs read

- Sessions 1–4 deliverables (Sessions 3 and 4 for shared-pattern reference only; not cross-candidate comparison)
- A6, A9 already in context

### 1.2 Candidate C characterization

Entities are nodes; relationships are edges; properties are key-value pairs on nodes/edges (property graph) or RDF triples `(subject, predicate, object)` (RDF triplestore). Migration: extract from current YAML/markdown into nodes + edges; thereafter, edits go through application code, SPARQL/Cypher, or graph-aware tooling.

### 1.3 Within-Candidate-C sub-substrate sketch

Three families considered:

| Family | Substrate | Vendor risk | Solo-author ops | Format longevity | Query power |
|---|---|---|---|---|---|
| **RDF/triplestore** | Apache Jena (TDB or Fuseki) | Low — Apache Foundation; mature | Server process (Fuseki) or embedded library (TDB); JVM dependency | High — RDF is a W3C standard; Turtle/N-Triples/JSON-LD format families are stable; SPARQL is W3C-standard | SPARQL with full federation; OWL inference optional |
| **RDF/triplestore** | Blazegraph | High — project deprecated 2020 (Amazon Neptune fork); no active maintenance | Server process; JVM | Medium-High — RDF format outlives the engine; data is portable | SPARQL |
| **Property graph** | Neo4j (Community Edition) | Medium — single-vendor steward; Community Edition stable but Enterprise feature gating | Server process; JVM; CLI tools mature | Medium — Cypher is Neo4j-native (openCypher standardization is partial); on-disk format proprietary | Cypher; very expressive for path queries |
| **Property graph** | Memgraph / TigerGraph | High — newer vendors; smaller ecosystem; vendor-dependent | Server processes | Medium-Low — formats less stable; tooling ecosystem narrower | Cypher (Memgraph) or GSQL (TigerGraph) |

**Operative sub-substrate selection.** For Session 5's evaluation, **RDF/Apache Jena (TDB embedded mode)** is the operative substrate. Rationale:

1. **Format longevity is the highest of the four sub-substrates.** RDF (Turtle, N-Triples, JSON-LD) is W3C-standardized and is the longest-lived graph data format. Underlying storage engines are interchangeable; the data outlives any specific engine.
2. **Standards-based query language.** SPARQL is W3C-standardized; multiple implementations exist (Jena, Virtuoso, RDF4J, GraphDB, Blazegraph, Stardog). Vendor independence is high.
3. **Apache Foundation steward.** Jena is Apache Foundation-stewarded with no single-vendor risk. Mature project; multi-decade ecosystem.
4. **Embedded mode (TDB) avoids server process.** Jena TDB runs as a library against a directory of files — closer to SQLite's solo-author profile than Neo4j's server requirement.
5. **JSON-LD compatibility.** RDF/JSON-LD bridges to JSON tooling; the corpus is JSON-readable for consumers who don't speak SPARQL.

**Dismissed within Candidate C:**
- Blazegraph: deprecated 2020; vendor risk unacceptable.
- Neo4j: server process; Cypher is more developer-friendly than SPARQL but format longevity is materially weaker than RDF; single-vendor steward (Neo4j Inc.) introduces vendor risk; openCypher standardization is partial. Dismissed as primary; could be revisited if Sessions 7–9 select Candidate C and a non-RDF substrate's properties dominate.
- Memgraph / TigerGraph: vendor risk too high for a 12+ year horizon.

This sub-decision is captured as **D-0131 D-METH/DG-REVIEW** below.

---

## 2. Per-criterion evaluation

For each criterion, four-question template applied. Scores: **0** absent · **1** adapted high cost · **2** adapted moderate cost · **3** native.

### 2.1 Cluster I — Entity & relationship

#### C-1.1 — Entity-type expressiveness across the 20 A3 types

1. **Native.** Each entity type is an `rdf:type` value. 20 types map to 20 RDFS classes. New entity types are new classes — `:NewType rdf:type rdfs:Class`. Existing entities untouched.
2. **Cost: 5–7 sessions** to define the ontology (RDFS or OWL classes) for all 20 types. Comparable to Pydantic schema work plus ontology-design effort.
3. **Operational risk: low.** New classes don't affect existing data.
4. **Downstream binding: medium.** Stage C tooling queries via SPARQL; query patterns depend on ontology consistency.

**Score: 3** (native — RDF's `rdf:type` is the canonical entity-typing primitive)

#### C-1.2 — Relationship-type expressiveness (1:N, N:N, polymorphic)

1. **Native.** All relationships are triples `(subject, predicate, object)`. 1:N is multiple triples with same subject; N:N is the natural form (no join tables needed); polymorphism is unconstrained — any subject can have any predicate to any object. Edge properties (e.g., `synthesis_role` on a cell-evidence link) require RDF reification or named graphs (RDF*) — RDF* (RDF-star) is W3C-standardized as of 2023.
2. **Cost: 1–2 sessions** for predicate inventory + reification convention selection (named graphs vs RDF* vs reification triples).
3. **Operational risk: low.** Triple-level integrity validated via SHACL constraints (W3C-standardized 2017).
4. **Downstream binding: low-medium.** SPARQL queries traverse natively; renderers consume query results.

**Score: 3** (native — triples are the ur-relationship primitive; polymorphism is the form's natural state)

#### C-1.3 — Within-population variability as first-class data **[Weight 3]**

1. **Native.** Cell-level "rows" are subjects in RDF; each cell has triples for its state, convergence, and references. Variability is not collapsed into a single canonical value — multiple sources contribute multiple triples about the same cell, with provenance tracked via named graphs or PROV-O ontology.
2. **Cost: 6–10 sessions** for materialization (same volume as A and B — the cost is candidate-independent at this scale).
3. **Operational risk: medium.** Materialization volume same as A/B; SHACL validation ensures shape conformance.
4. **Downstream binding: high.** Cell-level state drives downstream synthesis; same as A/B.

**Score: 3** (native — RDF's open-world model treats variability and multi-perspective evidence as the default, not as exception)

#### C-1.4 — Sub-population inheritance

1. **Native.** RDFS subclass hierarchy: `Sub-population rdfs:subClassOf Population`. Triples about Population apply to Sub-populations via RDFS entailment. OWL adds richer inheritance (sub-property, restrictions). Inheritance is a first-class semantic concept in RDFS/OWL.
2. **Cost: 1 session** for the class hierarchy + entailment regime selection (RDFS vs OWL2-RL — RDFS-only is sufficient for the project's needs).
3. **Operational risk: low.** Inheritance resolution is built into reasoners; well-tested in Jena.
4. **Downstream binding: low.** Application queries with inferred triples enabled.

**Score: 3** (native — RDFS's entire purpose is inheritance among other things)

**Cluster I subtotal: 3+3+3+3 = 12 (weighted: 3×2+3×2+3×3+3×2 = 6+6+9+6 = 27 of max 27) — 100%**

### 2.2 Cluster II — Cell-level state

#### C-2.1 — Per-cell state machine encoding (4 states + transitions + audit trail)

1. **Native.** Cell state is a triple `:cell-id :hasState :stated`. State enum is an RDFS class with 4 instances. Transitions are reified events: `:transition-1 :fromState :pending; :toState :stated; :date "..."; :rationale "..."`. SHACL constraint enforces state-value enumeration.
2. **Cost: 1 session** for state-machine ontology + SHACL shapes; materialization shared with C-1.3.
3. **Operational risk: low.** SHACL validates at write time (before triplestore ingest) or query time.
4. **Downstream binding: high.** Same as A/B.

**Score: 3** (native)

#### C-2.2 — Multi-source attribution per cell

1. **Native.** Multiple `:cited-evidence` triples per cell. Each triple's object is an EvidenceSource node. RDF's open-world model treats this as the default.
2. **Cost: 0** for schema; materialization at C-1.3.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-2.3 — Tier + evidence_type orthogonal encoding

1. **Native.** `:source :hasTier 1; :hasEvidenceType :clinical-research`. Two independent triples; no implied dependency. RDF's open-world model preserves orthogonality natively.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster II subtotal: 3+3+3 = 9 (weighted: 3×2×3 = 18 of max 18) — 100%**

### 2.3 Cluster III — Co-1 schema discipline

#### C-3.1 — Six required Co-1 fields enforced; non-conformance blocked at write **[Weight 3]**

1. **Native.** SHACL shape on EvidenceSource: each Co-1 source must have all six predicates with min/max counts of 1. SHACL validation runs at write time (pre-ingest) or via constraint hooks. Write-time enforcement is achievable.
2. **Cost: 0–1 session** for SHACL shape + validator hook.
3. **Operational risk: low.** SHACL violations are loud and structured.
4. **Downstream binding: low.**

**Score: 3** (native — SHACL is the standard mechanism for shape constraints in RDF)

**Cluster III subtotal: 3 (weighted: 9 of max 9) — 100%**

### 2.4 Cluster IV — Synthesis metadata

#### C-4.1 — Convergence/divergence stored per cell

1. **Native.** Convergence assessment is a sub-resource: `:cell-1 :hasConvergence :conv-1. :conv-1 :converged "true"; :divergedDimensions ("dim-a")`. Triples express the structure naturally.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-4.2 — Values-criteria assessment stored per cell

1. **Native.** Same pattern as C-4.1.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-4.3 — Meta-methodological citations distinguishable from evidence sources at schema layer

1. **Native.** Separate class `:MetaMethodologicalCitation` distinct from `:EvidenceSource`. Schema-level distinction by class identity. SHACL forbids `:hasTier`/`:hasEvidenceType` on `:MetaMethodologicalCitation`.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster IV subtotal: 3+3+3 = 9 (weighted: 18 of max 18) — 100%**

### 2.5 Cluster V — Verification

#### C-5.1 — Verification-status state machine integrated with cell state

1. **Native.** Verification status is a triple on each EvidenceSource. Cross-validator (cell-state ↔ verification-status) is a SHACL property-pair constraint or SPARQL ASK query as a constraint check.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-5.2 — Evidence markers ●/○ enforced per specification sentence

1. **Adapted.** Specifications still contain prose (or normalized into per-sentence resources). Two patterns: (a) sentence-level resources `:spec-1-sentence-3 :hasMarker "●"` — most graph-native but requires sentence normalization; (b) marker-validator on prose content — same cost as Candidate A.
2. **Cost: 2–3 sessions** for (a) sentence normalization + extraction; **1–2 sessions** for (b).
3. **Operational risk: medium.**
4. **Downstream binding: medium.** Pattern (a) makes per-sentence operations native; (b) requires tokenizer at query time.

**Score: 2** (adapted, moderate cost — comparable to Candidate B)

**Cluster V subtotal: 3+2 = 5 (weighted: 3×2+2×2 = 10 of max 12) — 83%**

### 2.6 Cluster VI — Cross-cutting axes

#### C-6.1 — DesignStage × ProjectType filter dimension

1. **Native.** Filter triples: `:spec :appliesToStage :early-design; :appliesToProjectType :renovation`. SPARQL FILTER expressions or pattern matching.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster VI subtotal: 3 (weighted: 6 of max 6) — 100%**

### 2.7 Cluster VII — Navigation / audience

#### C-7.1 — Information-finding query mode

1. **Native.** SPARQL pattern: `SELECT ?spec ?val WHERE { ?cell :forSpec ?spec; :forPopulation :pop-1; :hasValue ?val }`. SPARQL is designed exactly for this kind of pattern matching.
2. **Cost: 1–2 sessions** for query pattern library + index strategy (Jena TDB indexes).
3. **Operational risk: low.** Query performance bounded by triple count and index quality; TDB handles millions of triples comfortably.
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-7.2 — Decision-frame query mode

1. **Native.** Multi-axis SPARQL filter. Same as relational form's WHERE clauses, expressed in SPARQL syntax.
2. **Cost: 0** beyond C-7.1.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-7.3 — Representation-checking query mode

1. **Native.** SPARQL aggregation: `SELECT ?spec (COUNT(DISTINCT ?pop) AS ?coverage) WHERE { ?cell :forSpec ?spec; :forPopulation ?pop; :hasState ?state. FILTER (?state IN (:stated, :provisional)) } GROUP BY ?spec`.
2. **Cost: 0** beyond C-7.1.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-7.4 — Questions-led query mode **[Weight 3]**

1. **Native.** Question entity is a new class `:Question`. Questions link to populations, parameters, specifications via predicates. SPARQL filter on Question subgraph.
2. **Cost: 1 session** when B3 ships.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster VII subtotal: 3+3+3+3 = 12 (weighted: 27 of max 27) — 100%**

Same Cluster VII strength as Candidate B, achieved through different means (SPARQL vs SQL).

### 2.8 Cluster VIII — Time model

#### C-8.1 — Entity-level versioning per A9

1. **Native.** A9's 7 temporal entities map to 7 RDF classes. Versioning is a property `:hasVersion` linking versioned subjects to version resources. Named graphs (or PROV-O `prov:wasRevisionOf`) express version chains natively.
2. **Cost: 2–3 sessions** for temporal ontology + retrofit converter.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — RDF's named graphs and PROV-O ontology are designed for exactly this)

#### C-8.2 — SupersedenceLink representation (5 link types)

1. **Native.** SupersedenceLink is a class with `:linkType` predicate. Link types are instances of an enum class. Cycle detection via SPARQL property-path queries (`?x (:supersedes)+ ?x`).
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — property paths in SPARQL handle transitive closure natively)

#### C-8.3 — Standards-edition tracking + freshness windows

1. **Native.** Standards edition relations as triples; freshness checks as SPARQL date arithmetic with FILTER expressions.
2. **Cost: 1–2 sessions** for materialization.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-8.4 — Stale-evidence detection at query time **[Weight 1]**

1. **Native.** SPARQL FILTER on `:lastVerified` against tier-keyed window.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster VIII subtotal: 3+3+3+3 = 12 (weighted: 3×2+3×2+3×2+3×1 = 6+6+6+3 = 21 of max 21) — 100%**

### 2.9 Cluster IX — Operational

#### C-9.1 — CI validation tractability **[Weight 1]**

1. **Adapted, high cost.** Graph CI requires: JVM in CI environment; Jena library; SHACL validator; SPARQL query test runner. Substantially more CI machinery than markdown+YAML or SQLite. Build time materially higher (JVM startup + triplestore initialization).
2. **Cost: 3–4 sessions** for CI integration.
3. **Operational risk: medium.** JVM dependency adds CI fragility (Java version drift, Jena version updates).
4. **Downstream binding: low.**

**Score: 1** (adapted, high cost — JVM CI is a step backward from Candidate A's pure-Python CI and Candidate B's SQLite CI)

#### C-9.2 — Solo-author operability without team infrastructure **[Weight 2]**

1. **Adapted, high cost.** RDF/Jena requires: JVM installed; ontology authoring (RDFS/OWL classes); SHACL shape authoring; SPARQL competence. Tooling exists (Jena CLI, Protégé for ontology authoring) but the cognitive load is materially higher than markdown+YAML or SQLite. Solo author needs to maintain all of: ontology, SHACL shapes, SPARQL query patterns, retrofit converter.
2. **Cost: 4–6 sessions** for tooling + author documentation + retrofit.
3. **Operational risk: high.** Single-author with graph stack is the hardest of the four candidates to maintain. RDF has a steeper learning curve and a more specialized tooling ecosystem.
4. **Downstream binding: high.** All future authoring requires graph-stack competence.

**Score: 1** (adapted, high cost — solo-author operability is the dominant Candidate C concern given D-03's pre-launch binding)

#### C-9.3 — Audit-trail preservation across migration from current state **[Weight 1]**

1. **Adapted.** Migration extracts current YAML/markdown into RDF triples. Audit trail of pre-migration state is git history; post-migration audit trail is named-graph-per-commit or version annotations. More complex than relational migration.
2. **Cost: 5–7 sessions** for migration tooling + verification + named-graph version strategy.
3. **Operational risk: medium-high.** Migration is the most complex of the four candidates because the data model transformation is most distant from the source.
4. **Downstream binding: low** post-migration.

**Score: 1** (adapted, high cost)

#### C-9.4 — Migration cost from current 1,098 records **[Weight 1]**

1. **Adapted.** Same migration as C-9.3.
2. **Cost: shared with C-9.3.**
3. **Operational risk: medium-high.**
4. **Downstream binding: low.**

**Score: 1** (adapted, high cost)

#### C-9.5 — A10/A12/A13 integration cost **[Weight 2]**

1. **Adapted.** A10 catalog, A12 register, A13 cadence migration to RDF requires: ontology classes for adversarial-use scenarios, decisions, recheck sessions; SHACL shapes; SPARQL queries replacing the existing Python validators. The validators (`audit_adversarial_use.py`, `decision_capture.py`, `doctrine_recheck.py`) are completely rewritten in SPARQL.
2. **Cost: 5–7 sessions** for migration + ontology + validator rewrites.
3. **Operational risk: medium-high.** SPARQL validators are less familiar than Python; debugging is harder.
4. **Downstream binding: low** post-migration.

**Score: 1** (adapted, high cost — A10/A12/A13 are mature in YAML/Python; rebuilding in graph stack is substantial work for marginal benefit)

**Cluster IX subtotal: 1+1+1+1+1 = 5 (weighted: 1×1+1×2+1×1+1×1+1×2 = 1+2+1+1+2 = 7 of max 21) — 33%**

This is Candidate C's worst cluster — operational cost is the dominant graph-form weakness. Worse than Candidate B's 48% on this cluster because graph stack adds JVM dependency + ontology cognitive load + more complex migration on top of relational's already-substantial migration cost.

### 2.10 Cluster X — Sustainability

#### C-10.1 — Format longevity (12+ year horizon) **[Weight 1]**

1. **Native.** RDF (Turtle, N-Triples, JSON-LD) is W3C-standardized; format longevity is high. Triples are plaintext-serializable. Format outlives any specific engine.
2. **Cost: 0.**
3. **Operational risk: low.** W3C standards are stable across decades.
4. **Downstream binding: low.**

**Score: 3** (native — RDF's W3C standardization gives it format-longevity properties comparable to plaintext markdown for the data structure itself)

#### C-10.2 — Tool independence (no vendor lock-in for read access) **[Weight 1]**

1. **Native.** Multiple SPARQL implementations (Jena, RDF4J, Virtuoso, Stardog, Blazegraph). Multiple language bindings (Java, Python, JavaScript, Ruby). RDF data is portable across engines.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-10.3 — Migration-out cost bounded (per D-0111 5-deliverable standard) **[Weight 2]**

Per D-0111:

1. **Full data export.** Native — triples export to Turtle, N-Triples, or JSON-LD. Standard SPARQL CONSTRUCT or `tdbdump` tooling.
2. **Relationship preservation.** Native — relationships are triples; preserved by definition.
3. **State preservation.** Native — state-machine values, supersedence chains, audit trails are all triples.
4. **Schema mapping document.** Required — RDF→relational mapping is well-trodden (R2RML W3C standard); RDF→markdown mapping is "triple → list-form record"; RDF→JSON-LD is the inverse direction (JSON-LD IS an RDF serialization).
5. **Export tooling cost.** ≤2 sessions: tdbdump is trivial; semantic export documents are 1–2 sessions.

All 5 deliverables satisfied. **PASS.**

**Score: 3** (native — RDF's interchange-format properties are designed for migration-out)

**Cluster X subtotal: 3+3+3 = 9 (weighted: 3×1+3×1+3×2 = 3+3+6 = 12 of max 12) — 100%**

---

## 3. Score summary

### 3.1 Per-criterion score table

| Criterion | Cluster | Weight | Score | Weighted |
|---|---|---|---|---|
| C-1.1 Entity-type expressiveness | I | 2 | 3 | 6 |
| C-1.2 Relationship-type expressiveness | I | 2 | 3 | 6 |
| C-1.3 Within-population variability | I | 3 | 3 | 9 |
| C-1.4 Sub-population inheritance | I | 2 | 3 | 6 |
| C-2.1 Cell-level state machine | II | 2 | 3 | 6 |
| C-2.2 Multi-source attribution | II | 2 | 3 | 6 |
| C-2.3 Tier + evidence_type orthogonal | II | 2 | 3 | 6 |
| C-3.1 Six required Co-1 fields | III | 3 | 3 | 9 |
| C-4.1 Convergence/divergence per cell | IV | 2 | 3 | 6 |
| C-4.2 Values-criteria assessment per cell | IV | 2 | 3 | 6 |
| C-4.3 Meta-methodological citations distinct | IV | 2 | 3 | 6 |
| C-5.1 Verification-status state machine | V | 2 | 3 | 6 |
| C-5.2 Evidence markers ●/○ enforced | V | 2 | 2 | 4 |
| C-6.1 DesignStage × ProjectType filter | VI | 2 | 3 | 6 |
| C-7.1 Information-finding query mode | VII | 2 | 3 | 6 |
| C-7.2 Decision-frame query mode | VII | 2 | 3 | 6 |
| C-7.3 Representation-checking query mode | VII | 2 | 3 | 6 |
| C-7.4 Questions-led query mode | VII | 3 | 3 | 9 |
| C-8.1 Entity-level versioning | VIII | 2 | 3 | 6 |
| C-8.2 SupersedenceLink representation | VIII | 2 | 3 | 6 |
| C-8.3 Standards-edition + freshness | VIII | 2 | 3 | 6 |
| C-8.4 Stale-evidence detection | VIII | 1 | 3 | 3 |
| C-9.1 CI validation tractability | IX | 1 | 1 | 1 |
| C-9.2 Solo-author operability | IX | 2 | 1 | 2 |
| C-9.3 Audit-trail preservation | IX | 1 | 1 | 1 |
| C-9.4 Migration cost from current | IX | 1 | 1 | 1 |
| C-9.5 A10/A12/A13 integration cost | IX | 2 | 1 | 2 |
| C-10.1 Format longevity | X | 1 | 3 | 3 |
| C-10.2 Tool independence | X | 1 | 3 | 3 |
| C-10.3 Migration-out cost (S-05) | X | 2 | 3 | 6 |

### 3.2 Cluster totals

| Cluster | Weighted score | Max | Ratio |
|---|---|---|---|
| I — Entity & relationship | 27 | 27 | 100% |
| II — Cell-level state | 18 | 18 | 100% |
| III — Co-1 schema discipline | 9 | 9 | 100% |
| IV — Synthesis metadata | 18 | 18 | 100% |
| V — Verification | 10 | 12 | 83% |
| VI — Cross-cutting axes | 6 | 6 | 100% |
| VII — Navigation / audience | 27 | 27 | 100% |
| VIII — Time model | 21 | 21 | 100% |
| IX — Operational | 7 | 21 | 33% |
| X — Sustainability | 12 | 12 | 100% |
| **Total** | **155** | **171** | **91%** |

**Candidate C (RDF/Jena) weighted score: 155 / 171 = 91%.**

---

## 4. Distinguishing strengths and weaknesses

### 4.1 Strengths

- **8 of 10 clusters at 100%.** Candidate C has the most clusters at full score of any candidate evaluated so far.
- **Cluster I (100%)** — RDF's native semantic model expresses entity types, relationships, variability, and inheritance as primitives; only candidate to score 3 on Sub-population inheritance (C-1.4).
- **Cluster VIII Time model (100%)** — RDF's named graphs and PROV-O make versioning native; transitive closure (cycle detection, supersedence chains) via SPARQL property paths.
- **Cluster X Sustainability (100%)** — W3C standardization gives format longevity comparable to plaintext.

### 4.2 Weaknesses

- **Cluster IX Operational (33%)** — the dominant Candidate C weakness, materially worse than Candidate B's 48%. JVM dependency in CI; ontology + SHACL + SPARQL cognitive load for solo author; migration cost is highest of the three substrates evaluated; A10/A12/A13 integration requires SPARQL validator rewrites.
- **Cluster V Verification (83%)** — same C-5.2 cost as B (sentence-marker enforcement requires either sentence normalization or tokenizer-on-text).

### 4.3 Cost summary

| Work | Sessions |
|---|---|
| Ontology design (20 classes + properties) | 5–7 |
| Migration tooling + verification (RDF transformation) | 5–7 (load-bearing) |
| A10/A12/A13 ontology + SHACL + SPARQL validators | 5–7 |
| Cell-level materialization | 6–10 (shared) |
| SHACL shape authoring (full corpus) | 2–3 |
| A9 retrofit (named graphs) | 2–3 |
| CI integration (JVM + Jena + SHACL) | 3–4 |
| Solo-author tooling + documentation | 4–6 |
| Sentence-marker handling | 2–3 |
| **Total** | **34–50 sessions** |

This is materially higher than Candidate B (27–42) and substantially higher than Candidate A (19–29). The cost-to-score ratio for Candidate C: 91% score at 34–50 sessions vs Candidate B's 89% at 27–42 — the 2-percentage-point gain costs ~7 additional sessions.

### 4.4 Solo-author operability concern

D-03 (Stage A) binds the project to pre-launch solo-author posture. Per A5 §1, solo-author means "no DPO collaborator infrastructure, Co-1 evidence engaged through the published corpus only, no resources for participatory synthesis." The same constraint binds B1 selection: any candidate that materially worsens solo-author operability incurs a doctrinal-level cost beyond its weighted-score impact.

Candidate C's solo-author cost is the highest of the three substrates evaluated. The graph stack (RDF + SHACL + SPARQL + Jena + JVM) adds cognitive surface area and tooling complexity that markdown+YAML and SQLite do not. A future-Claude-session reading the codebase to make an edit must know SPARQL to query, SHACL to validate, and ontology semantics to understand class relationships.

This is Cluster IX score 1 on C-9.2 already captured — but it is worth surfacing explicitly that **Cluster IX's 33% understates the doctrinal weight**. C-9.2 is weight-2; if it were weight-3 (sourced to D-03 directly rather than to A5+D-03 operationalization), Candidate C's score would drop ~4 weighted points further.

Sessions 7–9 must weigh this against Candidate C's Cluster I and VIII strengths.

---

## 5. Decision-capture for this session

### 5.1 D-0131 — Within-Candidate-C substrate: RDF/Apache Jena (TDB embedded) operative; Blazegraph/Neo4j/Memgraph/TigerGraph dismissed within Candidate C

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

DG-REVIEW because the substrate selection within Candidate C is a non-trivial methodological commitment that constrains Sessions 7–9 if Candidate C is selected.

### 5.2 D-0132 — Candidate C (Graph/RDF, Apache Jena) scored 155 / 171 (91%)

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0113, D-0131 |

DG-AUTO (mechanical evaluation under D-0108 + D-0110 + D-0131).

---

## 6. Status

| Field | Value |
|---|---|
| B1 Session 5 | COMPLETE |
| Candidate C (RDF/Jena) score | 155 / 171 (91%) |
| Within-C substrate | RDF/Apache Jena TDB embedded (D-0131); Blazegraph/Neo4j/Memgraph/TigerGraph dismissed |
| Distinguishing strengths | 8 of 10 clusters at 100% (I, II, III, IV, VI, VII, VIII, X) |
| Distinguishing weakness | IX Operational (33% — JVM CI; solo-author cognitive load; migration cost) |
| Decisions captured | D-0131, D-0132 |
| Working session counter | 7 → 8 |
| Session log | `sessions/session_2026-05-02-b1-s5.md` |
| Next session | B1 Session 6 — Candidate D (Hybrid) per-criterion evaluation + eliminator test per D-0112 |

---

## 7. Session 6 next-action

**Session 6 = Candidate D (Hybrid) per-criterion evaluation + hybrid eliminator test per D-0112.**

Hybrid sub-substrate sketch from framework §5.4: relational for normalized records + markdown for prose specifications, OR triplestore for relationships + relational for tabular records.

After Session 6 produces D's per-criterion scores `D_i`, apply D-0112's strict-dominance test: D survives elimination iff there exists at least one criterion `i` such that `D_i > max(A_i, B_i, C_i)`. With Candidate C scoring 3 (native) on 24 of 30 criteria, the bar for D's survival is high — D must outscore C on a criterion where C scored 2 or below.

Output: `workplan/b1-candidate-d-hybrid.md`. Eliminator-test outcome captured separately as a Decision record.
