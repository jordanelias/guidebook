# Storage Derivation
**Status:** PROVISIONAL — proposal-of-record from B1 Session 8 (Opus 4.7); pending project-owner adoption per A12 §2.4 (D-DOCT default DG-NON).
**Doctrinal basis:** `governance/mission-and-epistemics.md` §Doctrinal commitments 1, 3, 6; `governance/decision-protocol.md` (A12) §1.1, §2.2; `governance/co1-operational.md` (A5); `governance/evidence-methodology.md` (A6); `governance/time-model.md` (A9).
**Workplan basis:** `workplan/workplan-co0007-v3.md` §B1.
**Evaluation framework:** `workplan/b1-derivation-framework.md` (D-0108); `workplan/b1-criteria-weighting.md` (D-0110, D-0111, D-0112, D-0113); per-candidate evaluations D-0119 (A), D-0121 (B), D-0132 (C); D-0134 (D dismissed); D-0136 (comparative matrix); D-0137 (Rule 3 selection).
**Decision recorded:** D-0138 D-DOCT/DG-NON storage-form selection — PENDING project-owner adoption.
**Last updated:** 2026-05-02 02:40

---

## 1. Purpose and structure

This document is the canonical derivation of the project's operative storage form. It produces:

1. The doctrinal foundations the storage form must satisfy (§2).
2. The candidate inventory considered (§3).
3. The evaluation outcome from B1 Sessions 3–7 (§4).
4. The selection rationale under Rule 3 (tradeoff-aware) (§5).
5. The dismissed alternatives with reasons (§6).
6. The scope limits — what this document does NOT decide (§7).

The selection itself is **PROPOSED** by this document. The decision is **D-DOCT/DG-NON** per A12 §2.2 — the project owner alone makes the canonical commitment. This document is the proposal-of-record for that commitment.

---

## 2. Doctrinal foundations

The storage form must satisfy three load-bearing doctrinal commitments (mission §Doctrinal commitments 1, 3, 6) and one operational binding (mission §Operational reality / D-03), bounded by one sustainability commitment (workplan v3 §S-01).

### 2.1 DC-1 — Specifications serve questions; people are not uniform

> Every parameter exposes its within-population variability. Population codes are organizing scaffolding, not a description of any individual within the population. Within-population variation is shown as a first-class data dimension, not buried in narrative caveats. Co-occurring conditions are the norm, not the exception.
> — mission §Doctrinal commitments 1

**Storage implication:** The storage form must represent within-population variability as **first-class data** — discrete, queryable, structured records — not as narrative caveat in prose. Per-(parameter × population) cell-level state is the operationalization. The framework operationalized this as criterion **C-1.3 (within-population variability as first-class data)** at weight 3 (critical-binding).

### 2.2 DC-3 — Co-1 evidence is co-primary with Tier 1

> Co-1 evidence — lived experience and participatory design (CRPD Art. 4.3) — is not subordinate to clinical research. The two answer different questions. Where they converge, the convergence is itself evidence. Where they diverge, the divergence is documented and a synthesis approach is specified per parameter.
> — mission §Doctrinal commitments 3

**Storage implication:** Co-1 sources must carry distinguishing schema fields (per A5 co1-operational.md §6.1: tier, evidence_type, co1_provenance, co1_source_type, verification_status, synthesis_attribution_required) that are enforced at write — not optional, not narrative. The framework operationalized this as criterion **C-3.1 (six required Co-1 fields enforced; non-conformance blocked at write)** at weight 3 (critical-binding).

### 2.3 DC-6 — Questions-led teaching is the project's pedagogical commitment

> The guidebook organizes around questions readers should ask, not around answers they should adopt. **Questions are first-class data, not annotations.** Navigation modes include a questions-led entry surface.
> — mission §Doctrinal commitments 6

**Storage implication:** B3 will specify the Question entity (per audit v2 §T-02 / D-01 resolution). The storage form must accept Question as a first-class entity type, indexable and queryable for the questions-led navigation mode. The framework operationalized this as criterion **C-7.4 (questions-led query mode)** at weight 3 (critical-binding).

### 2.4 D-03 — Pre-launch solo-author operational reality

> The project is currently pre-launch and authored by a single person. There are no Co-1 collaborator panels, no DPO partnerships, no recruitment thread, and no compensation infrastructure. … **Solo-only-permanent is a possible end-state for the project.** The methodology must hold integrity in that case as well as in the launched-with-collaboration case.
> — mission §Operational reality

**Storage implication:** Operational cost of the storage form must be tractable for a solo author with no team infrastructure. The "solo-only-permanent" end-state means the storage form's maintenance burden over 12+ year horizon must be one a single technical person can carry. The framework operationalized this as **Cluster IX (Operational)** — five criteria (C-9.1 CI tractability; C-9.2 solo-author operability; C-9.3 audit-trail preservation; C-9.4 migration cost; C-9.5 A10/A12/A13 integration).

### 2.5 S-01 / S-02 — 12+ year sustainability

> The project is conceived as a 12+ year commitment. Storage form, schema, and tooling must outlive any single technology cycle.
> — workplan v3 §Cross-stage requirements (S-01)

**Storage implication:** Format longevity, tool independence, and migration-out cost must be bounded. The framework operationalized this as **Cluster X (Sustainability)** — three criteria (C-10.1 format longevity; C-10.2 tool independence; C-10.3 migration-out cost per the D-0111 5-deliverable standard).

### 2.6 The doctrine-vs-operational tension

Doctrinal commitments DC-1, DC-3, DC-6 demand structural expressive richness. Operational binding D-03 demands minimum cognitive surface area for solo maintenance. These two pull in opposite directions:

- Richer storage forms (graph databases, semantic-web stacks) satisfy doctrine more natively but impose higher operational cost.
- Simpler storage forms (markdown + YAML, plain SQL) satisfy operations more natively but require adaptation work to satisfy doctrine.

The B1 framework's tiered weighting (3/2/1) operationalized the priority structure: critical-binding doctrinal commitments (weight 3) cannot be sacrificed; important-binding requirements (weight 2) carry the bulk of evaluation; operational-preference (weight 1) tunes the choice. Selection under this priority structure walks the doctrine-operations tension explicitly.

---

## 3. Candidate inventory

Per workplan v3 §B1 and B1 Session 1's framework §5, four candidates were evaluated:

| Candidate | Form | Within-candidate sub-substrate operative for evaluation |
|---|---|---|
| A | Markdown + YAML status-quo-extended | (no sub-substrate — the form itself is plain text) |
| B | Relational | SQLite (D-0120: PostgreSQL and DuckDB dismissed within Candidate B) |
| C | Graph / triplestore | RDF / Apache Jena (TDB embedded mode) (D-0131: Blazegraph, Neo4j, Memgraph, TigerGraph dismissed within Candidate C) |
| D | Hybrid | H1 = SQLite + Markdown + YAML (D-0133; H2 dismissed by transitivity) |

The five-form inventory in workplan v3 §B1 collapses to three single-substrate candidates plus one hybrid: workplan's "Graph database" and "RDF/JSON-LD with triplestore" are both subsumed under Candidate C with sub-substrate selection deferred to Session 5; workplan's "Structured markdown" is Candidate A; workplan's "Relational database" is Candidate B; workplan's "Hybrid" is Candidate D.

### 3.1 Within-candidate sub-substrate selections (recap)

**Candidate B → SQLite.** PostgreSQL adds server-process operational discipline that solo-author pre-launch posture (D-03) does not need; the project's pre-launch-and-permanent solo posture means PostgreSQL's ecosystem advantages (replication, advanced features) carry no value-add. DuckDB's file-format longevity is materially weaker than SQLite (younger project, single steward, format breaks have occurred); analytical-query strength does not compensate at the project's data volume. SQLite is the lowest-risk relational substrate for solo-author pre-launch with 12+ year horizon. (D-0120.)

**Candidate C → RDF / Apache Jena (TDB embedded).** Blazegraph deprecated 2020 (vendor-risk crystallized); Neo4j single-vendor with Cypher partial-standardization and proprietary divergence; Memgraph and TigerGraph carry similar vendor-risk concentration. RDF/Jena has W3C-standards backing (RDF, SPARQL, SHACL are W3C Recommendations); Apache Jena is open-source under Apache 2.0; TDB embedded mode requires no external server. (D-0131.)

**Candidate D → H1 (SQLite + Markdown + YAML).** H1 preserves markdown editing affordance for specifications (highest-volume content type); H2 (RDF + SQLite) doubles up on database-substrate operational burden without preserving the markdown workflow. If H1 fails the eliminator test, H2 fails by transitivity. (D-0133.)

---

## 4. Evaluation outcome

### 4.1 Per-candidate weighted totals

| Candidate | Score | Cost to reach near-native scoring (sessions) |
|---|---|---|
| A — Markdown + YAML | 132 / 171 (77%) | 19–29 |
| B — Relational / SQLite | 152 / 171 (89%) | 27–42 |
| C — Graph / RDF | 155 / 171 (91%) | 34–50 |
| D — Hybrid (H1) | 143 / 171 (84%) — informational | (DISMISSED) |

### 4.2 Cluster-level distribution

| Cluster | Max | A | B | C | D (dismissed) |
|---|---|---|---|---|---|
| I — Entity & relationship | 27 | 20 (74%) | 25 (93%) | 27 (100%) | 21 (78%) |
| II — Cell-level state | 18 | 16 (89%) | 18 (100%) | 18 (100%) | 18 (100%) |
| III — Co-1 schema discipline | 9 | 6 (67%) | 9 (100%) | 9 (100%) | 9 (100%) |
| IV — Synthesis metadata | 18 | 14 (78%) | 18 (100%) | 18 (100%) | 18 (100%) |
| V — Verification | 12 | 8 (67%) | 10 (83%) | 10 (83%) | 10 (83%) |
| VI — Cross-cutting axes | 6 | 6 (100%) | 6 (100%) | 6 (100%) | 6 (100%) |
| VII — Navigation / audience | 27 | 12 (44%) | 27 (100%) | 27 (100%) | 27 (100%) |
| VIII — Time model | 21 | 17 (81%) | 19 (90%) | 21 (100%) | 19 (90%) |
| IX — Operational | 21 | 21 (100%) | 10 (48%) | 7 (33%) | 7 (33%) |
| X — Sustainability | 12 | 12 (100%) | 10 (83%) | 12 (100%) | 8 (67%) |
| **Total** | **171** | **132** | **152** | **155** | **143** |

### 4.3 Candidate D dismissal (under D-0112)

Candidate D was dismissed under D-0112's strict-dominance test: D > max(A, B, C) on **0 of 30 criteria** (18 ties; 12 losses). The pivotal criterion was C-5.2 (sentence-level evidence-marker enforcement) — the only criterion where max(A, B, C) = 2 rather than 3. D scored 2 on C-5.2 because the hybrid form does not provide a structural advantage on sentence-level enforcement; the structured-marker convention (H1' variant) that could plausibly achieve score 3 is form-agnostic and does not uniquely belong to the hybrid. Sessions 7–9 input set is {A, B, C}. (D-0134.)

### 4.4 Unique-winner analysis among survivors

| Candidate | Unique winners (criteria where only this candidate scores 3) | Weighted advantage |
|---|---|---|
| A | C-9.1, C-9.2, C-9.3, C-9.4, C-9.5 (all of Cluster IX) | +11 over best-of-(B,C) |
| B | (none) | 0 |
| C | C-8.1 (A9 versioning via named graphs) | +2 over best-of-(A,B) |

**Critical observation: B has zero unique wins.** B never strictly outscores both A and C on any criterion. B's value proposition is *consistency* — high score on most criteria — not unique structural advantage.

### 4.5 Performance on the three weight-3 doctrinal commitments

| Criterion (doctrinal anchor) | A | B | C |
|---|---|---|---|
| C-1.3 within-population variability (DC-1) | 2 | 3 | 3 |
| C-3.1 six required Co-1 fields (DC-3) | 2 | 3 | 3 |
| C-7.4 questions-led query mode (DC-6) | 2 | 3 | 3 |

A scores **2 on all three weight-3 doctrinal criteria** — moderate adaptation cost to satisfy. B and C score **3 on all three** — native satisfaction. This is the structural argument against Candidate A: the form does not natively satisfy the project's three load-bearing doctrinal commitments. Adaptation can close the gap (the 19–29 session cost projection includes the work to do so), but the form itself does not embody doctrine.

### 4.6 Performance on Cluster IX (D-03 operational binding)

| Criterion | A | B | C |
|---|---|---|---|
| C-9.1 CI validation tractability | 3 | 2 | 1 |
| C-9.2 Solo-author operability | 3 | 2 | 1 |
| C-9.3 Audit-trail preservation | 3 | 1 | 1 |
| C-9.4 Migration cost from current | 3 | 1 | 1 |
| C-9.5 A10/A12/A13 integration cost | 3 | 1 | 1 |

A scores **3 on all five Cluster IX criteria** — operationally native (A IS the project's incumbent state). B scores 2/2/1/1/1; C scores 1/1/1/1/1. This is the structural argument against C in particular: SPARQL + SHACL + ontology semantics impose specialized cognitive load that "solo-only-permanent" maintenance cannot reliably absorb.

---

## 5. Selection rationale

**Selection: Candidate B (Relational / SQLite).**

**Decision delegation: D-DOCT / DG-NON** — proposed by B1 Session 8; **PENDING project-owner adoption** per A12 §2.2.

**Decision rule: Rule 3 (tradeoff-aware)** — weighted total + cost-to-native + doctrinal binding force + pre-launch posture (D-0137).

The selection rationale walks four steps under Rule 3.

### 5.1 Step 1 — A is structurally weak on the three weight-3 doctrinal commitments

The framework's weighting (D-0110) assigned weight 3 to three criteria specifically because they operationalize mission §Doctrinal commitments 1, 3, 6. These are the project's load-bearing doctrinal stances; the storage form should embody them, not adapt to them.

Candidate A scores 2 on all three: within-population variability requires cell-level YAML materialization (6–10 sessions of extraction work); Co-1 field enforcement is CI-time not write-time (the gap is 0–2 sessions for a pre-commit hook); questions-led query mode shares the query/index-layer cost with the other navigation modes (2–3 sessions for the layer). The aggregate adaptation closes the doctrinal gap but at a cost — and more importantly, it leaves the corpus structure as markdown+YAML files with custom Python query code on top. The doctrine is satisfied by *a layer above the storage form*, not by the storage form.

Over a 12+ year horizon, the layer-above-storage pattern accumulates technical debt. The custom query code is project-specific; future maintainers (Claude sessions, new collaborators if the project ever launches with a team, a possible solo-only-permanent maintainer in 2038) read both the YAML and the query code to understand "what's here." The cognitive surface is the union of the data shape and the access code.

A is therefore eliminated from selection — not because its weighted total is lowest (132/171 is a strong baseline), but because its structural relationship to the three load-bearing doctrinal commitments is "adapted" rather than "native." On the doctrinal axis, the form should be native.

### 5.2 Step 2 — B and C both natively satisfy doctrine; the question becomes operational cost

Both Candidate B (152/171, 89%) and Candidate C (155/171, 91%) score 3 on all three weight-3 doctrinal criteria. Both natively express within-population variability (cell rows or cell triples), Co-1 field enforcement (NOT NULL columns or SHACL shapes), and questions-led query (SQL or SPARQL).

The B-vs-C selection is not a doctrinal question — both forms satisfy doctrine natively. It is an operational question: which form's recurring cost of operation is sustainable for solo-author pre-launch with possible solo-only-permanent end-state?

### 5.3 Step 3 — Cluster IX gap (B 48% vs C 33%) is structural, not arbitrary

The 15-percentage-point gap between B and C on Cluster IX reflects three distinct operational costs:

1. **CI validation tractability (C-9.1)**: B's SQLite build step in CI is a 30-second job with a 5-line GitHub Actions step. C's CI requires JVM + Apache Jena + SHACL — a heavier toolchain with more failure modes. (B = 2; C = 1.)

2. **Solo-author operability (C-9.2)**: SQL is broadly known. SPARQL + SHACL + ontology semantics are specialized. A solo author maintaining the corpus runs a query: in B, the query is `SELECT spec, val FROM cell WHERE population = 'NDV/AUT' AND parameter = 'task-light-illuminance'` — readable to anyone who's used a database in the last 30 years; in C, the query is `?cell rdf:type :Cell ; :population :NDV_AUT ; :parameter :TaskLightIlluminance ; :value ?val .` — readable to a SPARQL practitioner. The skill differential is real and recurring. (B = 2; C = 1.)

3. **A10/A12/A13 integration cost (C-9.5)**: A10 catalog, A12 register, A13 cadence are tabular by nature. Migration to SQLite tables is mechanical (A10 catalog has 14 columns; A12 register has 11 columns; A13 records have ~6 columns). Migration to RDF requires ontology design for each — encoding A12 categories (D-DOCT, D-METH, D-SCHEMA, D-OP, D-PRES) as a class hierarchy with discriminator predicates is non-trivial methodological work, not just data transformation. (B = 1 because volume is non-trivial; C = 1 because the methodological work compounds the volume.)

These costs recur every working session, every CI run, every contributor onboarding (if the project launches with a team), every maintenance pass for 12+ years. C's structural advantages (named graphs for versioning, RDFS subclass for inheritance, W3C standardization for sustainability) are real but lower-frequency: versioning operations are concentrated in Stage C and at edition transitions; subclass inheritance is one feature; W3C standardization affects export format choice once, not daily.

### 5.4 Step 4 — Recurring cost vs structural advantage tradeoff

The B-vs-C tradeoff has the shape: B is strictly better on the recurring-cost axis; C is strictly better on the structural-advantage axis. The framework's weighting tried to balance these by assigning weights — Cluster IX got mostly weight 1 and 2 because operational criteria are operational-preference (W1) or important-binding (W2), not critical-binding (W3). The 3-weighted-point gap C-over-B reflects this weighting.

But the weighting captures **decision priority**, not **temporal frequency**. A criterion at weight 2 carries half the decision-priority of a weight-3 criterion — but if the weight-2 criterion's cost is paid 1,000 times over 12 years and the weight-3 criterion's cost is paid once, the total cost the project actually pays is dominated by the weight-2.

Cluster IX criteria are paid daily (CI runs, queries written, validators executed). Cluster I/VIII/X structural advantages are paid once-per-feature (versioning operations at edition transitions, subclass inheritance for the population taxonomy, format-export at migration-out events that may never happen). The 3-weighted-point gap C-over-B is technically correct under the framework's weighting but understates the recurring-cost reality.

D-03's "solo-only-permanent is a possible end-state" intensifies this argument. A solo maintainer in 2038, with no team to consult and no specialized SPARQL practitioner to call on, will face the recurring SPARQL cost alone. SQL is the more transferable skill — taught in every CS curriculum, present in every web framework, used in every analytics tool. SPARQL is narrower; a 2038 solo maintainer is more likely to know SQL than SPARQL with no other priors.

### 5.5 Selection: B (SQLite)

**Candidate B (Relational / SQLite) is selected** as the project's operative storage form.

The selection sits at the intersection of:

- **Native satisfaction of all three weight-3 doctrinal commitments** (DC-1, DC-3, DC-6) — ruling out A's adaptation pattern.
- **Lowest recurring operational cost among forms that natively satisfy doctrine** — ruling out C's specialized stack.
- **Sustainable for solo-author pre-launch with possible solo-only-permanent end-state** — SQLite is single-file, no server, format documented at Library of Congress preservation level; SQL is the most-broadly-known query language with stable backwards-compatibility commitment.
- **Migration-out cost bounded** per D-0111's 5-deliverable standard (PASS) — `.dump` to SQL or CSV is trivial; schema mapping to other forms (markdown, RDF) is mechanical given the SQL DDL.
- **Schema work directly continues from Pydantic** — the existing 14 schema modules under `schemas/` map to SQLAlchemy models with high fidelity; the project does not abandon its Pydantic discipline, it extends it.

B's weighted score (152/171, 89%) is 3 points below C's 155 — the gap is at the noise floor of weighting precision and is offset by C's operational disadvantages on solo-author binding force.

### 5.6 What the selection does NOT mean

The selection does not mean:
- **A is wrong as the project's pre-pivot form.** A served the project well from inception through 2026-04 and continues to serve as the corpus's authoring substrate for prose specifications during migration.
- **C is universally inferior.** For projects with team-scale operations, dedicated SPARQL practitioners, or use cases where named-graph versioning is the dominant access pattern, C may be the better choice. For *this* project's pre-launch solo-author posture and 12+ year horizon, B is the better fit.
- **B is irrevocable.** The decision is irrevocable in the sense that synthesis structure for 12+ years is what's being committed; it is *revisable* via formal D-METH amendment if the project's posture changes (e.g., if A5 launches and a Co-1 collaborator panel materializes with SPARQL expertise, C may become viable; if Stage C reveals access patterns that SQL cannot serve efficiently, the form may be re-evaluated). Migration-out cost (per S-05) is bounded by D-0111's 5-deliverable standard.
- **Future entity types must use SQLite.** B3 (Question entity), B4 (pilot data), and C-stage migrations all add new entity types per Candidate B's pattern (new SQL tables; new Pydantic↔SQLAlchemy mappings; new validators). The selection commits to the form, not to the current 14-schema set.

### 5.7 Cost-to-near-native trajectory under Candidate B

The 27–42 session estimate from D-0121 covers:

| Work | Sessions | Stage |
|---|---|---|
| 20 SQL table definitions (5 missing entity types schemed; existing 14 mapped) | 5–7 | B1 cont. into B2 |
| Migration tooling + verification reports (current 1,098 records → SQLite inserts) | 4–6 | B2 |
| A10/A12/A13 dataset migration + validator rewrites (3 governance datasets) | 3–5 | B2 |
| Cell-table materialization (78 BPCs × ~20 populations into cell rows) | 6–10 | B2/C-stage cell migration overlap |
| Sub-population inheritance pattern (recursive CTE or self-reference + view) | 1–2 | B1 cont. |
| Sentence-marker handling (option a sentence normalization OR option b tokenizer) | 2–3 | B5 (rendering) |
| A9 retrofit converter (relational temporal tables) | 2–3 | B2 |
| CI integration (build step + validators) | 2–3 | B2 |
| Solo-author write workflow + migration tooling | 2–3 | B2 |
| **Total** | **27–42** | distributed across B1–B5 + C-stage |

The 27–42 sessions are not all upfront; they distribute across Stages B and C. B2 (Tooling design with expanded validator suite, 4–6 sessions per workplan v3 §B2) absorbs the migration tooling, validator rewrites, and A9 retrofit. B5 (Pilot rendering, 3–4 sessions) absorbs the sentence-marker work. The cell materialization (6–10 sessions) overlaps with C-stage cell migrations.

---

## 6. Dismissed alternatives

### 6.1 Candidate-level dismissals

#### Candidate A — Markdown + YAML status-quo-extended

**Dismissed: Step 1 of selection rationale (§5.1).** Structural relationship to weight-3 doctrinal commitments is "adapted" (score 2/2/2 on C-1.3, C-3.1, C-7.4) rather than "native" (score 3/3/3). Adaptation cost (19–29 sessions) closes the gap quantitatively but leaves the corpus structure as markdown+YAML with custom Python query code — accumulating project-specific technical debt over 12+ year horizon.

A's strengths (Cluster IX 100%, X 100%, VI 100%) are real but do not compensate for the doctrinal-axis weakness. The framework's weight-3 designation specifically marks the criteria where adaptation is not acceptable.

A continues to serve as the corpus's authoring substrate for prose specifications during migration. The dismissal is from "operative storage form" only.

#### Candidate C — Graph / RDF (Apache Jena)

**Dismissed: Steps 3 and 4 of selection rationale (§5.3, §5.4).** Native satisfaction of doctrine matches B (3/3/3 on weight-3 criteria) but Cluster IX gap (33% vs B's 48%) reflects structural recurring costs in CI, solo-author operability, and A10/A12/A13 integration that compound under D-03's "solo-only-permanent is a possible end-state" binding.

C's structural advantages on Clusters I/VIII/X (totaling +6 weighted points over B) are real but lower-frequency than Cluster IX's recurring costs. The framework's weighted-total ranking (C 155 > B 152) is at the noise floor of weighting precision (1.7% of max) and is correctly understood as a tie that is broken by the recurring-cost vs structural-advantage analysis under Rule 3.

#### Candidate D — Hybrid

**Dismissed: D-0134 strict-dominance test under D-0112.** D scored 0 wins, 18 ties, 12 losses across 30 criteria against max(A, B, C). The pivotal criterion C-5.2 (sentence-level evidence-marker enforcement) showed that the hybrid form does not provide a structural advantage over Candidate B alone or Candidate A with structured-marker convention; structured-marker convention is form-agnostic.

Configuration H2 (RDF + SQLite, no markdown for prose) was dismissed by transitivity: H2's operational scores are necessarily worse than H1's and H2 cannot satisfy any criterion H1 cannot.

### 6.2 Within-Candidate-B sub-substrate dismissals (per D-0120)

**PostgreSQL.** Server-process operational discipline adds value-add for team-scale operations; for solo-author pre-launch with possible solo-only-permanent end-state, PostgreSQL's ecosystem advantages (replication, extensions, advanced features) carry no value-add against SQLite's single-file simplicity. Operational cost is strictly higher with no offsetting benefit on the project's binding constraints.

**DuckDB.** File-format longevity is materially weaker than SQLite (younger project established 2019, single-organization steward, format breaks have occurred during DuckDB's evolution). Analytical-query strength does not compensate at the project's data volume (1,098 records growing to estimated ~5,000 by Stage C close — well within SQLite's operational sweet spot of single-file databases up to terabytes). 12+ year horizon argues for the more-mature, more-stewarded format.

### 6.3 Within-Candidate-C sub-substrate dismissals (per D-0131; included for completeness — Candidate C dismissed at top level)

**Blazegraph.** Project deprecated 2020 (acquired by Amazon Neptune team; codebase no longer actively maintained for general release). Vendor-risk crystallized; format longevity at risk; tool independence eroding. Selecting Blazegraph would inherit the project's unmaintained status as a transitive risk to the project's 12+ year horizon.

**Neo4j.** Single-vendor steward (Neo4j Inc.); proprietary query language Cypher partially standardized as openCypher but Neo4j's implementation diverges; format longevity contingent on vendor commitment. Tool independence is not present in the W3C-standards sense available to RDF/Jena. Neo4j Community Edition's GPL licensing creates additional copy-left implications for downstream synthesis renderers.

**Memgraph / TigerGraph.** Vendor-risk concentration similar to Neo4j; smaller ecosystems; format longevity contingent on commercial viability of single vendors. Neither offers a sustainability profile compatible with the 12+ year horizon.

---

## 7. Scope limits

This document does NOT decide:

- **Schema specification details.** The Pydantic schema modules already exist for 14 of 20 entity types. The mapping to SQLAlchemy models, the SQL DDL, the migration files (Alembic or equivalent), and the schema-spec.md document are produced in **B1 Session 9** (workplan v3 §B1 outputs `architecture/schema-spec.md` and `architecture/storage-decision.md`).

- **Tooling design.** Migration tooling, validator rewrites, query-layer patterns, and the database build step in CI are produced in **Stage B2** (workplan v3 §B2).

- **Pilot construction.** The first end-to-end pilot using the SQLite form is produced in **Stage B4** (workplan v3 §B4).

- **Migration phase ordering.** Which entity types migrate first, the verification protocol per migration phase, and the rollback strategy are produced in **Stage C0–C1** (workplan v3 §C0, §C1).

- **PostgreSQL or DuckDB future re-evaluation.** If the project's posture changes (e.g., A5 launches with a team and PostgreSQL's multi-user features become valuable), the within-Candidate-B substrate decision can be revisited under a superseding D-METH amendment to D-0120.

- **Whether Candidate C should be re-evaluated if the project gains SPARQL expertise.** The selection commits to B for the project's currently-projected trajectory. If Stage C operationalization reveals access patterns that SQL cannot serve well or if the project's team composition changes materially, the form is revisable — though migration cost from B to C (or any other form) would be substantial and would itself require D-DOCT amendment.

- **The fate of pre-pivot markdown specifications.** The 78 BPCs in `references/bpc/` and the spec prose in `parts/` continue to serve as the corpus's authoring substrate during migration. Per `governance/migration-survival.md` (PROVISIONAL, D-0116), each pre-pivot artifact category has a survival disposition. The B1 selection of SQLite as operative storage does not retire any pre-pivot artifact category by itself; supersession events are recorded as separate D-OP/DG-REVIEW Decision records per migration-survival.md §9.

- **Long-horizon doctrinal revision.** If the project's mission §Doctrinal commitments are revised (e.g., a future revision of DC-6 changes the questions-led structure), the storage form selection may need to be revisited. This is normal operation under A12 §2.3 (departure from default delegation) and the doctrine-recheck cadence in A13.

---

## 8. Status and adoption

**This document is PROVISIONAL.** The selection of Candidate B (Relational / SQLite) is **proposed** by B1 Session 8.

**D-DOCT/DG-NON adoption is required.** Per A12 §2.2, doctrinal decisions default to DG-NON — the project owner alone makes the canonical commitment. This document is the proposal-of-record; D-0138 records the proposed selection with `review_status: PENDING`.

**Adoption converts PROVISIONAL → CANONICAL.** Project-owner adoption may include amendments — the proposed selection may be modified, the rationale refined, or alternatives reconsidered. Adoption is recorded as a follow-up Decision record; the PROVISIONAL → CANONICAL status change is itself a logged event.

**If adoption is denied or deferred,** the project remains in Candidate A's status-quo-extended form as the de facto storage; B1 Session 9 (schema spec + repo strategy revision) proceeds only after adoption. Sessions B2–B7 schedule depends on adoption status.

**CS-MIG cross-stage thread implication.** Adoption of this document triggers reclassification across `governance/migration-survival.md` per the §7 forward-dependency table — specifically, "B1 storage-form selection: All 'SURVIVES_AS_IS' mechanical-conversion estimates" are re-evaluated under the SQLite target. This is a follow-up reclassification, not a B1 deliverable.

---

## 9. Change log

- 2026-05-02 02:40 — PROVISIONAL issued by B1 Session 8 (Opus 4.7); selection proposed: Candidate B (SQLite). Pending project-owner adoption.
