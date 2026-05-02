# B1 Session 4 — Candidate B Evaluation
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 4 of 6–9
**Candidate:** B — Relational (SQLite / PostgreSQL / DuckDB)
**Status:** Per-criterion evaluation complete; Candidate B scored against 30 criteria
**Predecessor session:** `sessions/session_2026-05-02-b1-s3.md` (Candidate A evaluation, 132/171)
**Operative governance:** D-0108, D-0110, D-0111, D-0112 (does not apply to Candidate B), D-0113
**Model routing:** opus/150/synth

---

## 1. Session purpose and scope

Apply the 4-question evaluation template (framework §6.1) to Candidate B (Relational) across all 30 criteria. Session 4 also includes the within-Candidate-B sub-substrate sketch (SQLite vs PostgreSQL vs DuckDB) per framework §5.2.

This session does NOT compare B to A/C/D — that is Session 7. Standalone evaluation only.

### 1.1 Inputs read

- `workplan/b1-derivation-framework.md` (D-0108) · `workplan/b1-criteria-weighting.md` (D-0110, D-0111, D-0112, D-0113) · `workplan/b1-candidate-a-markdown-yaml.md` (D-0119) for shared-pattern reference (NOT cross-candidate comparison)
- A6 evidence-methodology, A9 time-model, A10 adversarial-use, A12 decision-protocol, A13 doctrine-recheck — already in context from Sessions 1–3

### 1.2 Candidate B characterization

Atomic entities normalized into tables. Cells are rows. Sources are rows. Citations are join-table rows. Views compose markdown for rendering. Migration: bulk extract from current YAML/markdown into SQL; thereafter, edits go through application or schema-aware tooling.

**Within-Candidate-B sub-substrate sketch:**

| Substrate | Vendor risk | Solo-author ops | Format longevity | Query power |
|---|---|---|---|---|
| **SQLite** | None — public-domain format; CLI ubiquitous; format documented | Single file; `sqlite3 file.db`; no server | High — one of the longest-lived DB formats; SQLite Archive Format is a Library of Congress recommended preservation format | Standard SQL with extensions (FTS5, JSON1) |
| **PostgreSQL** | Low — open-source; large ecosystem; pg_dump portable | Server process; backups via pg_dump; complexity higher than SQLite | High — PostgreSQL on-disk format readable across versions with documented migrations | Strongest SQL feature set; recursive CTEs, window functions, JSON, full-text |
| **DuckDB** | Low-Medium — younger project (2019+); single-vendor steward | Single file or in-memory; no server; CLI mature | Medium — file format documented but younger than SQLite/Postgres; format breaks have occurred | Optimized for analytical queries; columnar; SQL with extensions |

**Operative sub-substrate for evaluation:** SQLite. SQLite is the lowest-risk choice for the project's pre-launch solo-author posture (D-03), highest format longevity, and trivial operational profile. Sessions 7–9 may revisit if Candidate B is selected and a different sub-substrate's properties dominate. PostgreSQL adds operational complexity without a corresponding improvement on solo-author binding requirements; DuckDB's analytical-query strength is appealing for audience modes but its format longevity is materially weaker than SQLite. **Within-B substrate verdict: SQLite is the operative substrate; PostgreSQL and DuckDB are dismissed within Candidate B.**

This sub-decision is captured as **D-0129 D-METH/DG-REVIEW** below.

---

## 2. Per-criterion evaluation

For each criterion, four-question template applied. Scores: **0** absent · **1** adapted high cost · **2** adapted moderate cost · **3** native.

### 2.1 Cluster I — Entity & relationship

#### C-1.1 — Entity-type expressiveness across the 20 A3 types

1. **Native.** Each entity type is a SQL table. 20 tables. Schema is the project's authoritative entity-type inventory. New entity types are new tables — `CREATE TABLE` plus a Pydantic-to-SQLAlchemy mapping.
2. **Cost: 5–7 sessions** to define all 20 tables initially (same scale as Candidate A's schema additions; relational schema work is similar to Pydantic schema work).
3. **Operational risk: medium.** Schema migrations require care — adding a column to a populated table needs `ALTER TABLE`; the migration tool (Alembic or similar) is the operational discipline.
4. **Downstream binding: medium.** Every B-stage tool (B2 validators, B3 query patterns, B4 pilot writes, B5 renderers) operates against the relational schema. Schema changes require migration coordination.

**Score: 3** (native — the relational form's native unit IS the typed table)

#### C-1.2 — Relationship-type expressiveness (1:N, N:N, polymorphic)

1. **Native.** Foreign keys express 1:N. Join tables express N:N (e.g., `specification_evidence_source(spec_id, source_id)`). Polymorphism (Gap.blocks → any entity) requires either table-per-target with discriminator, or a `target_type` + `target_id` pair with application-enforced integrity. The relational form has standard patterns for all three.
2. **Cost: 0–2 sessions** for join-table additions and polymorphic-reference convention. The 188 connections + various other N:N relationships materialize as join tables; polymorphic refs use `target_type, target_id` with the validator enforcing integrity.
3. **Operational risk: low.** FK constraints catch dangling references at write time, not CI time — a strict improvement over Candidate A's CI-time enforcement.
4. **Downstream binding: low.** Joins are expressed naturally in SQL queries.

**Score: 3** (native — write-time FK enforcement is a strict improvement over CI-time YAML cross-ref validation)

#### C-1.3 — Within-population variability as first-class data **[Weight 3]**

1. **Native.** Cell-level records are rows in a `cell` table keyed by (specification_id, population_id). Variability is encoded as cell rows; `state` and `convergence` are columns; cell metadata (which dimensions converged, divergence reasoning) lives in nested tables or JSON columns. Mission §Doctrinal commitment 1's first-class data is exactly the relational table's natural unit.
2. **Cost: 6–10 sessions** to materialize from BPC markdown (same volume as Candidate A — the materialization volume is candidate-independent). Schema work is bounded (1 session for cell table + nested tables); extraction is the cost.
3. **Operational risk: medium.** Materialization extracts from markdown into rows; same risk surface as Candidate A's extraction.
4. **Downstream binding: high.** Same as Candidate A — cell-level state drives all downstream synthesis. The relational form makes the data shape more queryable but does not reduce the materialization volume.

**Score: 3** (native — relational rows are the most natural representation of cell data; materialization cost is shared with all candidates)

#### C-1.4 — Sub-population inheritance

1. **Adapted.** Inheritance is not a native relational concept. Two patterns: (a) `population` table with `parent_population_id` self-reference + view that computes inherited fields; (b) `population` table with all fields denormalized + nullable override columns + materialized view for inheritance resolution. (a) is cleaner but requires query-time computation; (b) duplicates fields but simplifies queries.
2. **Cost: 1–2 sessions** for either pattern + tests.
3. **Operational risk: low-medium.** Inheritance bugs are subtle in either pattern; recursive-CTE pattern is well-tested in SQLite/Postgres.
4. **Downstream binding: low.** Application code calls a resolver function or queries the materialized view; the abstraction is local to the population table.

**Score: 2** (adapted, moderate cost — inheritance is not native to relational; pattern selection is the work)

**Cluster I subtotal: 3+3+3+2 = 11 (weighted: 3×2+3×2+3×3+2×2 = 6+6+9+4 = 25 of max 27)**

### 2.2 Cluster II — Cell-level state

#### C-2.1 — Per-cell state machine encoding

1. **Native.** `cell.state` column with CHECK constraint enumerating 4 values; `cell_state_transition` table for audit trail (cell_id, from_state, to_state, transition_date, rationale). State machine is a CHECK + TRIGGER pattern — standard relational discipline.
2. **Cost: 1 session** for state-transition table + triggers; materialization shared with C-1.3.
3. **Operational risk: low.** Triggers enforce valid transitions at write time.
4. **Downstream binding: high.** Same as Candidate A.

**Score: 3** (native — write-time state-transition enforcement is a strict improvement over CI-time)

#### C-2.2 — Multi-source attribution per cell

1. **Native.** Join table `cell_evidence_source(cell_id, source_id, [synthesis_role])`. Multi-source is the join table's purpose.
2. **Cost: 0** for schema; materialization at C-1.3.
3. **Operational risk: low.** FK constraints on both columns.
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-2.3 — Tier + evidence_type orthogonal encoding

1. **Native.** `evidence_source.tier INT CHECK (tier BETWEEN 1 AND 6)` + `evidence_source.evidence_type` ENUM column. Orthogonal columns; CHECK constraints enforce ranges.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster II subtotal: 3+3+3 = 9 (weighted: 3×2+3×2+3×2 = 18 of max 18) — 100%**

### 2.3 Cluster III — Co-1 schema discipline

#### C-3.1 — Six required Co-1 fields enforced; non-conformance blocked at write **[Weight 3]**

1. **Native.** Co-1 fields are NOT NULL columns on `evidence_source` (or a `co1_fields` extension table joined on source_id with NOT NULL on all six). Database refuses inserts/updates that violate. Write-time enforcement is the relational form's bread and butter.
2. **Cost: 0–1 session** for schema + back-population of existing Co-1 records.
3. **Operational risk: low.** Write rejection is loud and immediate.
4. **Downstream binding: low.**

**Score: 3** (native — addresses Candidate A's CI-time-enforcement weakness directly)

**Cluster III subtotal: 3 (weighted: 3×3 = 9 of max 9) — 100%**

### 2.4 Cluster IV — Synthesis metadata

#### C-4.1 — Convergence/divergence stored per cell

1. **Native.** Columns or sub-tables on `cell` for convergence assessment. JSON column option available for variable-shape data; structured columns for the fixed-shape parts.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-4.2 — Values-criteria assessment stored per cell

1. **Native.** Same pattern as C-4.1 — sub-table or JSON column on `cell`.
2. **Cost: 0–1 session** for the sub-table.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-4.3 — Meta-methodological citations distinguishable from evidence sources at schema layer

1. **Native.** Separate table `meta_methodological_citation` with no `tier`/`evidence_type` columns. Schema-level distinction by table identity.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster IV subtotal: 3+3+3 = 9 (weighted: 3×2×3 = 18 of max 18) — 100%**

### 2.5 Cluster V — Verification

#### C-5.1 — Verification-status state machine

1. **Native.** ENUM column + state-transition table mirroring C-2.1's pattern. Cross-validator (cell-state ↔ verification-status) implemented as a SQL constraint or trigger.
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-5.2 — Evidence markers ●/○ enforced per specification sentence

1. **Adapted.** Specifications still contain prose. Marker enforcement requires either (a) sentence-level rows in a `specification_sentence` table with `evidence_marker` column, or (b) the same markdown-aware sentence-tokenizer as Candidate A but applied to the `specification.body` text column. (a) is the relational-native pattern but requires sentence-level normalization (large extraction work). (b) is the same cost as Candidate A's sentence validator.
2. **Cost: 2–3 sessions** for (a) sentence normalization + extraction; **1–2 sessions** for (b) tokenizer-on-text pattern.
3. **Operational risk: medium.** Sentence normalization is substantial work for marginal gain over a tokenizer.
4. **Downstream binding: medium.** If sentences are normalized to rows (a), downstream rendering can do per-sentence operations natively. If (b), rendering uses the tokenizer.

**Score: 2** (adapted, moderate cost — marginally better than Candidate A's score 1 because the relational form's option (a) provides a path to native enforcement, even if the path is costly)

**Cluster V subtotal: 3+2 = 5 (weighted: 3×2+2×2 = 10 of max 12) — 83%**

### 2.6 Cluster VI — Cross-cutting axes

#### C-6.1 — DesignStage × ProjectType filter dimension

1. **Native.** Filters are `WHERE` clauses on join tables `specification_design_stage(spec_id, stage)` and `specification_project_type(spec_id, ptype)`. Index-supported for performance.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

**Cluster VI subtotal: 3 (weighted: 6 of max 6) — 100%**

### 2.7 Cluster VII — Navigation / audience

This cluster is Candidate A's worst (12/27, 44%). The relational form's premise is that this is its strongest cluster.

#### C-7.1 — Information-finding query mode

1. **Native.** SQL query — `SELECT spec, val FROM specification s JOIN cell c ... WHERE c.population = ? AND s.parameter = ?`. Indexes on (parameter, population) make this O(log n). The audience-priority §Information-finding mode IS a SQL query.
2. **Cost: 1 session** to specify view + index strategy + query patterns.
3. **Operational risk: low.** Query performance is predictable; corpus is bounded pre-launch.
4. **Downstream binding: low.** Renderers consume query results.

**Score: 3** (native — relational is the canonical substrate for this query pattern)

#### C-7.2 — Decision-frame query mode

1. **Native.** Multi-axis filter: `WHERE population = ? AND design_stage = ? AND parameter_class = ?`. Index-supported. The decision-frame mode IS a relational query.
2. **Cost: 0** beyond the C-7.1 query layer.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-7.3 — Representation-checking query mode

1. **Native.** `SELECT spec, count(distinct cell.population) FROM specification s JOIN cell c WHERE cell.state IN ('stated','provisional')` — surfaces representation thinness. Standard aggregation query.
2. **Cost: 0** beyond C-7.1.
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-7.4 — Questions-led query mode **[Weight 3]**

1. **Adapted (extensibility) / Native (when E-20 lands).** B3 specifies the Question entity. When B3 ships, Question is a new table; the query mode is a SQL filter on Question rows joined to cells. Extensibility (adding new entity types without migrating existing) requires `ALTER TABLE` for new columns or new tables for new entities — both are mechanical relational work, not migration of existing data.
2. **Cost: 1 session** when B3 ships, for the question-aware query pattern.
3. **Operational risk: low.** New tables don't disrupt existing.
4. **Downstream binding: low.** Renderers read questions like any other entity.

**Score: 3** (native — Question entity is a new table; query mode is SQL)

**Cluster VII subtotal: 3+3+3+3 = 12 (weighted: 3×2+3×2+3×2+3×3 = 6+6+6+9 = 27 of max 27) — 100%**

This is the dramatic cluster where Candidate B inverts Candidate A's weakness. Cluster VII goes from 44% (Candidate A) to 100% (Candidate B). +15 weighted points.

### 2.8 Cluster VIII — Time model

#### C-8.1 — Entity-level versioning per A9

1. **Adapted.** A9 specifies SupersedenceLink primitive + 7 temporal entities. Relational schema for these is straightforward — each entity is a table; SupersedenceLink is a table with `from_id`, `to_id`, `link_type`. Cycle detection at validator level (recursive CTE). The schema work is comparable to Candidate A.
2. **Cost: 2–3 sessions** for the temporal tables + validators + retrofit converter (same retrofit work as Candidate A — A9's converter parses markdown).
3. **Operational risk: low.** Cycle detection in SQL is well-defined.
4. **Downstream binding: low.**

**Score: 2** (adapted, moderate cost — comparable to Candidate A but with native cycle detection via recursive CTE)

#### C-8.2 — SupersedenceLink representation (5 link types)

1. **Native.** Single `supersedence_link` table with `from_id`, `to_id`, `link_type ENUM`, `effective_date`, `transition_until_date`, `rationale`. Polymorphic links handled by `from_id_type`, `to_id_type` columns + application-enforced integrity (or table-per-link-type).
2. **Cost: 0–1 session.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-8.3 — Standards-edition tracking + freshness windows

1. **Native.** Standards table with `family`, `edition`, `effective_date`. Freshness check is a SQL query: `WHERE last_verified < date('now', '-7 years') AND tier = 1`. Native.
2. **Cost: 1–2 sessions** for materialization (back-populate `last_verified`).
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native)

#### C-8.4 — Stale-evidence detection at query time **[Weight 1]**

1. **Native.** SQL date arithmetic against `last_verified` and `tier`-keyed window. The query layer's natural expression.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 3** (native — same as Candidate A but the relational form makes it queryable in any context, not just validator scripts)

**Cluster VIII subtotal: 2+3+3+3 = 11 (weighted: 2×2+3×2+3×2+3×1 = 4+6+6+3 = 19 of max 21) — 90%**

### 2.9 Cluster IX — Operational

#### C-9.1 — CI validation tractability **[Weight 1]**

1. **Adapted.** Schema validation runs against a SQLite file generated from migration scripts. Each push regenerates the SQLite file from canonical SQL fixtures (or runs against a committed `.db` blob). CI cost is moderate — building the database in CI is a 30-second job; running validators against it is another 30s. Compare Candidate A's 5-job CI which runs in similar time.
2. **Cost: 2–3 sessions** to wire CI for the relational substrate. Includes: SQLite build step, integrity check step, schema-validation step, query-mode test step.
3. **Operational risk: low.** Reproducible build.
4. **Downstream binding: low.**

**Score: 2** (adapted, moderate cost — CI works but requires a build step; lower than Candidate A's 3-native-CI score because Candidate A's CI is already operative)

#### C-9.2 — Solo-author operability without team infrastructure **[Weight 2]**

1. **Adapted.** SQLite is the most solo-author-friendly relational substrate — single file, no server, command-line tools standard. But still requires: SQL knowledge for writes (the project's write workflow becomes "edit YAML fixtures, regenerate DB" or "INSERT/UPDATE statements via CLI"); schema migration discipline (Alembic or equivalent).
2. **Cost: 2–3 sessions** to define write workflow + migration tooling + author documentation.
3. **Operational risk: medium.** Writing the wrong UPDATE statement, or skipping a migration, can corrupt state. SQLite's atomicity protects against partial writes; logical-error mitigation requires test discipline.
4. **Downstream binding: medium.** Stage C migration tooling (B2 spec) writes via this workflow.

**Score: 2** (adapted, moderate cost — SQLite is the lowest-risk relational substrate but still requires a write workflow that markdown+YAML doesn't)

#### C-9.3 — Audit-trail preservation across migration from current state **[Weight 1]**

1. **Adapted.** Migration is the work — current corpus (1,098 records under A3 schemas + ~78 BPCs in markdown + 188 connections + etc.) needs extraction into SQL inserts. Audit trail of pre-migration state is preserved as git history (pre-migration commits stay in history); post-migration audit trail is the SQL diffs (Alembic migrations or commit-level fixtures).
2. **Cost: 4–6 sessions** for migration tooling + verification reports + edge-case handling. Migration is the load-bearing one-time cost of selecting Candidate B.
3. **Operational risk: medium-high.** Migration is the highest-risk operation in the candidate's lifetime; mitigation is multi-pass with verification (post-migration record counts match; sample diffs match; round-trip tests pass).
4. **Downstream binding: low** post-migration.

**Score: 1** (adapted, high cost — migration is substantial and one-time; the relational form's enforced integrity is in tension with the project's audit-trail-as-git-history discipline)

#### C-9.4 — Migration cost from current 1,098 records **[Weight 1]**

1. **Adapted.** Same as C-9.3 — migration tooling is the cost. 1,098 records across heterogeneous types; bounded but non-trivial.
2. **Cost: shared with C-9.3.**
3. **Operational risk: medium.**
4. **Downstream binding: low.**

**Score: 1** (adapted, high cost)

#### C-9.5 — A10/A12/A13 integration cost **[Weight 2]**

1. **Adapted.** A10 catalog, A12 register, A13 cadence currently in YAML form. Migration to relational tables is mechanical for A12 (decision register has tabular shape); A10 catalog is mostly tabular; A13 records are tabular. The validators (`audit_adversarial_use.py`, `decision_capture.py`, `doctrine_recheck.py`) need rewrite to query SQL instead of parse YAML.
2. **Cost: 3–5 sessions** for migration of 3 governance datasets + validator rewrites.
3. **Operational risk: low** post-migration.
4. **Downstream binding: low** post-migration.

**Score: 1** (adapted, high cost — integration is mechanical but volume is non-trivial; validators need rewriting)

**Cluster IX subtotal: 2+2+1+1+1 = 7 (weighted: 2×1+2×2+1×1+1×1+1×2 = 2+4+1+1+2 = 10 of max 21) — 48%**

This is Candidate B's worst cluster — operational cost is the dominant relational-form weakness.

### 2.10 Cluster X — Sustainability

#### C-10.1 — Format longevity (12+ year horizon) **[Weight 1]**

1. **Adapted.** SQLite format is among the longest-lived DB formats; SQLite Archive Format is a Library of Congress preservation recommendation. Format longevity is high but requires SQLite tooling to read — not plaintext.
2. **Cost: 0** beyond export tooling.
3. **Operational risk: low.** SQLite project commits to backwards compatibility.
4. **Downstream binding: low.**

**Score: 2** (adapted, moderate cost — SQLite format is durable but not plaintext; reading requires SQLite library or CLI; longevity is high but tool-dependent)

#### C-10.2 — Tool independence (no vendor lock-in for read access) **[Weight 1]**

1. **Adapted.** SQLite tools are open-source and ubiquitous. Reading requires `sqlite3` CLI or any SQLite library in any language. Strictly more dependent than markdown+YAML's "any text editor" but still tool-independent in any practical sense.
2. **Cost: 0.**
3. **Operational risk: low.**
4. **Downstream binding: low.**

**Score: 2** (adapted, moderate cost — tool-independent in practice but not in the trivial markdown+YAML sense)

#### C-10.3 — Migration-out cost bounded (per D-0111 5-deliverable standard) **[Weight 2]**

Per D-0111, evaluate against the 5 deliverables:

1. **Full data export.** Native — `.dump` to SQL or CSV. Standard SQLite export tooling.
2. **Relationship preservation.** Native — relationships are FK columns; preserved in any export format. Polymorphic refs preserved as `target_type, target_id` pairs.
3. **State preservation.** Native — state-machine values are columns; supersedence chains are rows in the supersedence_link table; audit trails are rows in transition tables.
4. **Schema mapping document.** Required — SQLite schema is canonical SQL; mapping to markdown+YAML is "table → directory of YAML files"; mapping to graph is "table row → node"; mapping to RDF is "table row → set of triples." All three mappings are mechanical given the schema.
5. **Export tooling cost.** ≤2 sessions: `sqlite3 .dump` is trivial; semantic export to a target form is 1–2 sessions. **Within budget.**

All 5 deliverables satisfied. **PASS.**

**Score: 3** (native — relational form's exit story is well-trodden ground)

**Cluster X subtotal: 2+2+3 = 7 (weighted: 2×1+2×1+3×2 = 2+2+6 = 10 of max 12) — 83%**

---

## 3. Score summary

### 3.1 Per-criterion score table

| Criterion | Cluster | Weight | Score | Weighted |
|---|---|---|---|---|
| C-1.1 Entity-type expressiveness | I | 2 | 3 | 6 |
| C-1.2 Relationship-type expressiveness | I | 2 | 3 | 6 |
| C-1.3 Within-population variability | I | 3 | 3 | 9 |
| C-1.4 Sub-population inheritance | I | 2 | 2 | 4 |
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
| C-8.1 Entity-level versioning | VIII | 2 | 2 | 4 |
| C-8.2 SupersedenceLink representation | VIII | 2 | 3 | 6 |
| C-8.3 Standards-edition + freshness | VIII | 2 | 3 | 6 |
| C-8.4 Stale-evidence detection | VIII | 1 | 3 | 3 |
| C-9.1 CI validation tractability | IX | 1 | 2 | 2 |
| C-9.2 Solo-author operability | IX | 2 | 2 | 4 |
| C-9.3 Audit-trail preservation | IX | 1 | 1 | 1 |
| C-9.4 Migration cost from current | IX | 1 | 1 | 1 |
| C-9.5 A10/A12/A13 integration cost | IX | 2 | 1 | 2 |
| C-10.1 Format longevity | X | 1 | 2 | 2 |
| C-10.2 Tool independence | X | 1 | 2 | 2 |
| C-10.3 Migration-out cost (S-05) | X | 2 | 3 | 6 |

### 3.2 Cluster totals

| Cluster | Weighted score | Max | Ratio |
|---|---|---|---|
| I — Entity & relationship | 25 | 27 | 93% |
| II — Cell-level state | 18 | 18 | 100% |
| III — Co-1 schema discipline | 9 | 9 | 100% |
| IV — Synthesis metadata | 18 | 18 | 100% |
| V — Verification | 10 | 12 | 83% |
| VI — Cross-cutting axes | 6 | 6 | 100% |
| VII — Navigation / audience | 27 | 27 | 100% |
| VIII — Time model | 19 | 21 | 90% |
| IX — Operational | 10 | 21 | 48% |
| X — Sustainability | 10 | 12 | 83% |
| **Total** | **152** | **171** | **89%** |

**Candidate B (SQLite) weighted score: 152 / 171 = 89%.**

---

## 4. Distinguishing strengths and weaknesses

### 4.1 Strengths

- **Cluster VII Navigation/audience (100%)** — query modes are SQL queries; the relational form is the canonical substrate for this. **Inverts Candidate A's 44% on the cluster Mission §Doctrinal commitment 6 (questions-led teaching) load-bears.**
- **Cluster III Co-1 schema discipline (100%)** — write-time enforcement via NOT NULL columns. Strict improvement over Candidate A's 67%.
- **Cluster II Cell-level state (100%)** — state-machine via CHECK + TRIGGER patterns; multi-source via join table.
- **Cluster IV Synthesis metadata (100%)** — sub-tables or JSON columns express convergence/values-criteria/meta-methodological natively.
- **Cluster I Entity & relationship (93%)** — only Sub-population inheritance scores below 3 (inheritance is not native to relational; pattern selection has cost).

### 4.2 Weaknesses

- **Cluster IX Operational (48%)** — the dominant Candidate B weakness. Migration cost (C-9.3, C-9.4) is the load-bearing one-time investment; A10/A12/A13 integration (C-9.5) requires validator rewrites; solo-author operability (C-9.2) is moderate but not native; CI integration (C-9.1) requires a database-build step.
- **Cluster X Sustainability (83%)** — SQLite format is durable but not plaintext; reading requires SQLite tooling. Mitigated by C-10.3's strong export story.

### 4.3 Cost summary (sessions to reach near-native scoring)

| Work | Sessions | Notes |
|---|---|---|
| 20 SQL table definitions | 5–7 | C-1.1 |
| Migration tooling + verification | 4–6 | C-9.3, C-9.4 (load-bearing) |
| A10/A12/A13 dataset migration + validator rewrites | 3–5 | C-9.5 |
| Cell-table materialization (78 BPCs × ~20 populations) | 6–10 | C-1.3, C-2.1 (shared with all candidates) |
| Sub-population inheritance pattern + tests | 1–2 | C-1.4 |
| Sentence-marker normalization or tokenizer-on-text | 2–3 | C-5.2 |
| A9 retrofit converter (relational tables) | 2–3 | C-8.1 |
| CI integration (build step + validators) | 2–3 | C-9.1 |
| Solo-author write workflow + migration tooling | 2–3 | C-9.2 |
| **Total to reach near-native** | **27–42 sessions** | |

This is materially higher than Candidate A's 19–29 because Candidate B has the migration-from-current cost on top.

---

## 5. Decision-capture for this session

### 5.1 D-0129 — Within-Candidate-B substrate: SQLite operative; PostgreSQL and DuckDB dismissed within Candidate B

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

DG-REVIEW because the substrate selection within Candidate B is a non-trivial methodological commitment that constrains Sessions 7–9 if Candidate B is selected.

### 5.2 D-0130 — Candidate B (Relational, SQLite) scored 152 / 171 (89%)

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0113, D-0129 |

DG-AUTO (mechanical evaluation under D-0108 + D-0110 + D-0129 substrate choice).

---

## 6. Status

| Field | Value |
|---|---|
| B1 Session 4 | COMPLETE |
| Candidate B (SQLite) score | 152 / 171 (89%) |
| Within-B substrate | SQLite (D-0129); PostgreSQL and DuckDB dismissed within Candidate B |
| Distinguishing strengths | VII (100% — inverts A's 44%); III (100%); II (100%); IV (100%); VI (100%) |
| Distinguishing weaknesses | IX Operational (48%); X Sustainability (83%) |
| Decisions captured | D-0129, D-0130 |
| Working session counter | 5 → 6 |
| Session log | `sessions/session_2026-05-02-b1-s4.md` |
| Predecessor | `sessions/session_2026-05-02-b1-s3.md` |
| Next session | B1 Session 5 — Candidate C (Graph / triplestore) per-criterion evaluation |

---

## 7. Session 5 next-action

**Session 5 = Candidate C (Graph / triplestore) per-criterion evaluation.**

Within-Candidate-C sub-substrates: RDF/JSON-LD with Apache Jena or Blazegraph; Neo4j property graph; Memgraph/TigerGraph (vendor-risk dimensions). Session 5 sketches sub-substrates and evaluates the candidate at the candidate level.

Inputs: Sessions 1, 2, 3, 4 deliverables (Sessions 3 and 4 for shared-pattern reference); A6, A9 already in context.

Output: `workplan/b1-candidate-c-graph.md`. ~400 lines.
