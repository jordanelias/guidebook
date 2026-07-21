# Schema Specification — B1 Session 9
**Status:** PROVISIONAL — pending D-0138 (storage form selection) project-owner adoption
**Created:** 2026-05-02 02:50 UTC
**Operative storage form (PROPOSED):** Candidate B / SQLite — per `architecture/storage-derivation.md` (D-0138 D-DOCT/DG-NON, PENDING adoption)
**Decision delegation for this document:** D-SCHEMA / DG-REVIEW per A12 §2 (D-0139 PENDING)
**Doctrinal anchor:** D-0138 selection rationale §5; this document specifies the form D-0138 selected
**Scope:** B1 closing artifact — translates the existing 14 Pydantic schema modules to SQL DDL + specifies the 5 missing entity types' new modules + outlines migration tooling for B2

---

## 1. Purpose and structure

### 1.1 Purpose

The schema specification translates the project's existing 14 Pydantic schema modules into the SQL DDL form required by Candidate B (SQLite operative substrate). It enumerates the 5 entity types currently un-schemed that must be added to reach the 20-entity target inventory (per `b1-derivation-framework.md` §4 A3 entity types). It outlines the migration tooling pattern that B2 will detail.

This document is a **proposal-of-record** that becomes operative only when D-0138 is adopted by the project owner. Until adoption, the project continues operating in Candidate A's incumbent form (Pydantic + YAML + markdown). Schema artifacts written under this specification are PROVISIONAL.

### 1.2 What this document does

- Maps each existing Pydantic schema module to its SQL table form (column types, constraints, indexes, FK relationships).
- Specifies the 5 missing entity-type schema modules (Population, Item, Conflict, Question, FDR Scenario, Specialist Handoff — counted as 5 because Population/Sub-population share a module per A7).
- States the cross-table relationship structure (1:N, N:N, polymorphic).
- Specifies cell-level normalization (the load-bearing structure for DC-1 within-population variability per D-0138 §5.1).
- Outlines migration tooling pattern (B2 produces the actual tooling).

### 1.3 What this document does NOT do

- **Does not produce migration tooling code.** B2 produces validated, tested migration tools.
- **Does not produce SQL DDL files.** The DDL is specified in the form `table_name(columns; constraints; indexes)` inline; the actual `.sql` files are committed at B2 along with the migration tooling that loads from them.
- **Does not specify SQLAlchemy ORM models.** The Pydantic↔SQLAlchemy mapping is mechanical given the schema; B2 produces the ORM layer.
- **Does not specify query patterns or rendering logic.** B5 (rendering) and B3 (navigation) own those.
- **Does not specify pre-commit hooks or CI integration.** B2 produces those.
- **Does not amend D-0138.** If D-0138 is amended in adoption, this document is amended correspondingly under a superseding D-SCHEMA record.

### 1.4 Inputs read

- `architecture/storage-derivation.md` (D-0138 PROPOSED; selection rationale §5)
- `schemas/base.py` · `schemas/enums.py` · all 14 schema modules in `schemas/`
- `governance/co1-operational.md` (A5; Co-1 6-field requirement)
- `governance/evidence-methodology.md` (A6; cell-level state machine, T-03 tier+evidence_type)
- `governance/time-model.md` (A9; 7 temporal entities, SupersedenceLink primitive)
- `governance/decision-protocol.md` (A12; Decision schema)
- `governance/doctrine-recheck.md` (A13; recheck schema)
- `workplan/b1-derivation-framework.md` §4 (entity inventory)

---

## 2. Entity-table mapping (existing 14 modules)

For each of the 14 existing Pydantic modules, the SQL DDL form is specified. Notation: `column_name TYPE [constraints]; FK references; indexes`. Column types use SQLite's affinity types (TEXT, INTEGER, REAL, NUMERIC, BLOB) plus dialect-portable patterns where SQLite's lenient typing differs from strict-mode SQL.

### 2.1 EvidenceSource (`schemas/evidence_source.py`)

**Table: `evidence_source`**

```
source_id        TEXT PRIMARY KEY                       -- e.g. "ES-0001"
slug             TEXT NOT NULL                          -- the project's stable identifier
title            TEXT NOT NULL
authors          TEXT                                    -- newline-separated; large-author lists per Co-1
year             INTEGER NOT NULL CHECK (year BETWEEN 1900 AND 2100)
tier             INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 6)  -- T-03 orthogonal
evidence_type    TEXT NOT NULL CHECK (evidence_type IN
                   ('peer-reviewed', 'systematic-review', 'cohort-study', 'case-study',
                    'standard', 'guideline', 'gray-literature', 'lived-experience', 'co1-collaborator'))
verification_status TEXT NOT NULL CHECK (verification_status IN
                   ('VERIFIED', 'UNVERIFIED-1', 'UNVERIFIED-2', 'UNAVAILABLE', 'STRUCK'))
last_verified    TEXT                                    -- ISO date YYYY-MM-DD
doi              TEXT
url              TEXT
notes            TEXT
created_at       TEXT NOT NULL                           -- YYYY-MM-DD HH:MM
modified_at      TEXT NOT NULL

-- A5 Co-1 required fields (NOT NULL when source is Co-1; NULL otherwise):
co1_provenance              TEXT
co1_source_type             TEXT CHECK (co1_source_type IN
                              ('lived-experience', 'practitioner', 'discipline-specialist', NULL))
synthesis_attribution_required INTEGER CHECK (synthesis_attribution_required IN (0,1,NULL))
-- Note: tier, evidence_type, verification_status are reused; A5 §6.1 specifies all 6 fields.

-- Constraints
CHECK ((evidence_type = 'co1-collaborator') = (co1_provenance IS NOT NULL))
  -- Co-1 enforcement: write-time block when evidence_type='co1-collaborator' but Co-1 fields are NULL
  -- Closes Candidate A's CI-time enforcement gap on C-3.1 (D-0138 §5.1).

-- Indexes
INDEX idx_evidence_source_tier_type (tier, evidence_type)
INDEX idx_evidence_source_verification_status (verification_status)
INDEX idx_evidence_source_last_verified (last_verified)
INDEX idx_evidence_source_year (year)
```

**Notes on translation:**
- The `co1_source_type` enum from Pydantic translates to a CHECK constraint with NULL allowed when not a Co-1 source.
- `synthesis_attribution_required` is `bool` in Pydantic; SQLite stores as INTEGER 0/1 (no native BOOLEAN).
- The compound CHECK on `evidence_type='co1-collaborator'` ↔ Co-1 fields populated is the write-time enforcement that makes C-3.1 score 3 under Candidate B (vs A's 2).

### 2.2 EvidenceStateRecord (`schemas/evidence_state.py`)

**Three tables: `cell` (the EvidenceStateRecord), `cell_provisional_flag`, `cell_convergence`. The Pydantic nested models become joined tables.**

```
-- cell table — per (specification × population) state record per A6 §2
TABLE cell (
  cell_id          TEXT PRIMARY KEY                     -- "CELL-{spec_id}-{population_code}"
  spec_id          TEXT NOT NULL                        -- FK to specification.spec_id
  population_code  TEXT NOT NULL                        -- FK to population.code
  state            TEXT NOT NULL CHECK (state IN
                     ('stated','provisional','silent','contested'))    -- A6 §2.1 four-state
  state_rationale  TEXT                                  -- why this state, in author's words
  values_criteria_assessment TEXT                       -- JSON or NULL; A6 §4 sub-fields
  created_at       TEXT NOT NULL
  modified_at      TEXT NOT NULL
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
  FOREIGN KEY (population_code) REFERENCES population(code)
  UNIQUE (spec_id, population_code)                     -- one cell per (spec, population)
)
INDEX idx_cell_spec (spec_id)
INDEX idx_cell_population (population_code)
INDEX idx_cell_state (state)

-- cell_state_transition — audit trail for state changes per A6 §2.7
TABLE cell_state_transition (
  transition_id    INTEGER PRIMARY KEY AUTOINCREMENT
  cell_id          TEXT NOT NULL
  from_state       TEXT                                  -- NULL on initial set
  to_state         TEXT NOT NULL
  transition_date  TEXT NOT NULL
  rationale        TEXT NOT NULL
  decision_id      TEXT                                  -- FK to decision.decision_id (optional)
  FOREIGN KEY (cell_id) REFERENCES cell(cell_id)
  FOREIGN KEY (decision_id) REFERENCES decision(decision_id)
)
INDEX idx_cell_state_transition_cell (cell_id)

-- cell_provisional_flag — A6 §2.3 ProvisionalConfidenceFlag nested model
TABLE cell_provisional_flag (
  flag_id          INTEGER PRIMARY KEY AUTOINCREMENT
  cell_id          TEXT NOT NULL
  flag_type        TEXT NOT NULL                        -- e.g. 'unverified-source', 'contested-evidence'
  flag_rationale   TEXT NOT NULL
  flag_date        TEXT NOT NULL
  resolved_date    TEXT                                  -- NULL if unresolved
  resolution_decision_id TEXT
  FOREIGN KEY (cell_id) REFERENCES cell(cell_id)
  FOREIGN KEY (resolution_decision_id) REFERENCES decision(decision_id)
)
INDEX idx_cell_provisional_flag_cell (cell_id)

-- cell_convergence — A6 §3 ConvergenceAssessment nested model
TABLE cell_convergence (
  convergence_id   INTEGER PRIMARY KEY AUTOINCREMENT
  cell_id          TEXT NOT NULL
  dimension        TEXT NOT NULL                        -- e.g. 'tier', 'methodology', 'jurisdiction'
  outcome          TEXT NOT NULL CHECK (outcome IN ('converged','diverged','partial'))
  reasoning        TEXT NOT NULL
  FOREIGN KEY (cell_id) REFERENCES cell(cell_id)
)
INDEX idx_cell_convergence_cell (cell_id)

-- cell_evidence_source — N:N join of cell to its citing sources (multi-source attribution, C-2.2)
TABLE cell_evidence_source (
  cell_id          TEXT NOT NULL
  source_id        TEXT NOT NULL
  synthesis_role   TEXT                                  -- e.g. 'primary', 'corroborating', 'co1-attributed'
  PRIMARY KEY (cell_id, source_id)
  FOREIGN KEY (cell_id) REFERENCES cell(cell_id)
  FOREIGN KEY (source_id) REFERENCES evidence_source(source_id)
)
INDEX idx_cell_evidence_source_source (source_id)  -- reverse lookup
```

**Notes:**
- DC-1 within-population variability is operationalized as cell rows: each (spec_id, population_code) pair gets a row; variability is encoded in the `state`/`state_rationale`/`values_criteria_assessment`/`cell_convergence` columns/tables. This is the structure that earns C-1.3 a score of 3 under Candidate B (D-0138 §5.1).
- The cell-state machine (A6 §2.7) is enforced by a trigger or by application logic at write time. Recommended: trigger-based to satisfy "blocked at write" per §C-3.1 reasoning.

### 2.3 Specification (`schemas/specification.py`)

**Table: `specification`**

```
spec_id          TEXT PRIMARY KEY                       -- "SPEC-NNNN" or stable slug
slug             TEXT NOT NULL UNIQUE
title            TEXT NOT NULL
parameter        TEXT NOT NULL                          -- e.g. 'task-light-illuminance'
parameter_class  TEXT NOT NULL                          -- A3 §1.4 hierarchical classification
body_md          TEXT                                    -- the prose specification (markdown, retained)
guidebook_version TEXT                                   -- A9 link
status           TEXT CHECK (status IN ('draft','provisional','active','superseded'))
created_at       TEXT NOT NULL
modified_at      TEXT NOT NULL

INDEX idx_specification_parameter (parameter)
INDEX idx_specification_class (parameter_class)
INDEX idx_specification_status (status)
```

**N:N relationships (join tables):**

```
TABLE specification_design_stage (
  spec_id          TEXT NOT NULL
  design_stage     TEXT NOT NULL                        -- 'pre-design','schematic','DD','CD','RFO','post-occupancy'
  PRIMARY KEY (spec_id, design_stage)
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
)

TABLE specification_project_type (
  spec_id          TEXT NOT NULL
  project_type     TEXT NOT NULL                        -- 'office','residential','healthcare','retail',...
  PRIMARY KEY (spec_id, project_type)
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
)
```

**Note on body_md:** Specification prose remains markdown. The D-0138 selection text in §5.6 explicitly states "Candidate A's incumbent form continues to serve as the corpus's authoring substrate for prose specifications during migration." The `body_md` column holds the prose; sentence-level marker enforcement is a B5 problem (rendering layer), not a B1 storage-form problem. C-5.2 score of 2 means: the storage form does not preclude marker enforcement, but does not natively enforce sentence-level structure either.

### 2.4 Connection (`schemas/connection.py`)

**Table: `connection`**

```
connection_id    TEXT PRIMARY KEY                       -- "CON-NNNN"
slug             TEXT NOT NULL UNIQUE
title            TEXT NOT NULL
description      TEXT
created_at       TEXT NOT NULL

INDEX idx_connection_slug (slug)
```

**Connection endpoints — polymorphic per `references/connections/_index.md` register table:**

```
TABLE connection_endpoint (
  connection_id    TEXT NOT NULL
  entity_type      TEXT NOT NULL CHECK (entity_type IN
                     ('specification','population','source','bpc','decision','gap','question'))
  entity_id        TEXT NOT NULL                         -- references the entity by its ID
  role             TEXT                                   -- e.g. 'subject', 'object', 'context'
  PRIMARY KEY (connection_id, entity_type, entity_id)
  FOREIGN KEY (connection_id) REFERENCES connection(connection_id)
  -- Polymorphic: integrity of (entity_type, entity_id) pair enforced by validator at CI time
  -- (SQLite does not natively support polymorphic FK; the entity_type discriminator + a validator
  -- that joins to the appropriate table per entity_type achieves equivalent integrity)
)
INDEX idx_connection_endpoint_entity (entity_type, entity_id)  -- reverse lookup
```

### 2.5 BPCMetadata (`schemas/bpc_metadata.py`)

**Table: `bpc`**

```
bpc_slug         TEXT PRIMARY KEY                       -- e.g. 'wayfinding-corridor-junctions'
title            TEXT NOT NULL
status           TEXT NOT NULL CHECK (status IN ('CLEAN','AMBIGUOUS','STUB','MERGED','SUPERSEDED'))
merged_into      TEXT                                    -- self-FK if MERGED
search_log_path  TEXT                                    -- relative path to search-log.md
created_at       TEXT NOT NULL
modified_at      TEXT NOT NULL
FOREIGN KEY (merged_into) REFERENCES bpc(bpc_slug)

INDEX idx_bpc_status (status)
```

**Note:** The pre-pivot BPC corpus (~78 directories) is partially superseded per `governance/migration-survival.md` §4.1. Migration tooling (B2) classifies each per the SURVIVES_AS_IS / SURVIVES_WITH_REDERIVATION / SURVIVES_CONDITIONALLY / SUPERSEDED dispositions; only SURVIVES rows are inserted into this table. SUPERSEDED records remain in git history per migration-survival §3 note.

### 2.6 Decision (`schemas/decision.py`)

**Table: `decision`**

```
decision_id      TEXT PRIMARY KEY                       -- "D-NNNN"
category         TEXT NOT NULL CHECK (category IN
                   ('D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'))
delegation       TEXT NOT NULL CHECK (delegation IN
                   ('DG-NON','DG-REVIEW','DG-AUTO'))
delegation_rationale TEXT
summary          TEXT NOT NULL
outcome          TEXT NOT NULL
rationale        TEXT NOT NULL
decision_date    TEXT NOT NULL                          -- "YYYY-MM-DD HH:MM"
decided_by       TEXT NOT NULL
model_routing    TEXT NOT NULL CHECK (model_routing GLOB
                   '*opus/*' OR model_routing GLOB '*sonnet/*' OR
                   model_routing GLOB '*haiku/*' OR model_routing GLOB '*human/*' OR
                   model_routing GLOB '*legacy/*')
                  -- Pattern: {tier}/{effort}/{modifier} per A12 §4.4
effort_level     INTEGER NOT NULL CHECK (effort_level IN (50,75,100,125,150))
status           TEXT NOT NULL CHECK (status IN
                   ('ACTIVE','SUPERSEDED','RETIRED','PROVISIONAL'))
review_status    TEXT NOT NULL CHECK (review_status IN
                   ('NA','PENDING','REVIEWED','REVIEWED-AMENDED'))
notes            TEXT

INDEX idx_decision_category (category)
INDEX idx_decision_delegation (delegation)
INDEX idx_decision_status (status)
INDEX idx_decision_review_status (review_status)
INDEX idx_decision_date (decision_date)
```

**N:N relationships (predecessors, supersedes, decision_artifacts, alternatives_considered):**

```
TABLE decision_predecessor (
  decision_id      TEXT NOT NULL
  predecessor_id   TEXT NOT NULL
  PRIMARY KEY (decision_id, predecessor_id)
  FOREIGN KEY (decision_id) REFERENCES decision(decision_id)
  FOREIGN KEY (predecessor_id) REFERENCES decision(decision_id)
)

TABLE decision_supersedes (
  decision_id      TEXT NOT NULL
  superseded_id    TEXT NOT NULL
  PRIMARY KEY (decision_id, superseded_id)
  FOREIGN KEY (decision_id) REFERENCES decision(decision_id)
  FOREIGN KEY (superseded_id) REFERENCES decision(decision_id)
)

TABLE decision_artifact (
  decision_id      TEXT NOT NULL
  artifact_path    TEXT NOT NULL
  PRIMARY KEY (decision_id, artifact_path)
  FOREIGN KEY (decision_id) REFERENCES decision(decision_id)
)

TABLE decision_alternative (
  decision_id      TEXT NOT NULL
  alternative_seq  INTEGER NOT NULL                     -- ordering within decision
  alternative_text TEXT NOT NULL
  PRIMARY KEY (decision_id, alternative_seq)
  FOREIGN KEY (decision_id) REFERENCES decision(decision_id)
)
```

### 2.7 AdversarialUseCatalog + MisuseVector + MisuseReview + ReleaseOverride (`schemas/adversarial_use.py`)

**Tables: `misuse_vector`, `misuse_review`, `release_override`, `misuse_catalog_version`.**

```
TABLE misuse_vector (
  vector_id            TEXT PRIMARY KEY                 -- "V-NN"
  name                 TEXT NOT NULL
  mechanism            TEXT NOT NULL
  harm                 TEXT NOT NULL
  severity             TEXT NOT NULL CHECK (severity IN ('LOW','MEDIUM','HIGH','CRITICAL'))
  status               TEXT NOT NULL CHECK (status IN ('ACTIVE','RETIRED'))
  introduced_date      TEXT NOT NULL
)

TABLE misuse_vector_mitigation (
  vector_id            TEXT NOT NULL
  mitigation_path      TEXT NOT NULL                    -- reference to project methodology
  PRIMARY KEY (vector_id, mitigation_path)
  FOREIGN KEY (vector_id) REFERENCES misuse_vector(vector_id)
)

TABLE misuse_vector_basis (
  vector_id            TEXT NOT NULL
  basis_path           TEXT NOT NULL                    -- doctrinal reference
  PRIMARY KEY (vector_id, basis_path)
  FOREIGN KEY (vector_id) REFERENCES misuse_vector(vector_id)
)

TABLE misuse_review (
  review_id            INTEGER PRIMARY KEY AUTOINCREMENT
  catalog_version      TEXT NOT NULL                    -- 'v1', 'v2', 'v3'
  vector_id            TEXT NOT NULL
  review_status        TEXT NOT NULL CHECK (review_status IN
                         ('PASS','PASS-WITH-NOTES','ESCALATE','BLOCK'))
  review_notes         TEXT
  reviewed_at          TEXT NOT NULL
  reviewed_by          TEXT NOT NULL
  FOREIGN KEY (vector_id) REFERENCES misuse_vector(vector_id)
)

TABLE release_override (
  override_id          INTEGER PRIMARY KEY AUTOINCREMENT
  review_id            INTEGER NOT NULL
  override_rationale   TEXT NOT NULL
  override_decision_id TEXT NOT NULL                    -- FK to decision.decision_id
  override_date        TEXT NOT NULL
  FOREIGN KEY (review_id) REFERENCES misuse_review(review_id)
  FOREIGN KEY (override_decision_id) REFERENCES decision(decision_id)
)

TABLE misuse_catalog_version (
  catalog_version      TEXT PRIMARY KEY                 -- 'v1', 'v2', 'v3'
  effective_date       TEXT NOT NULL
  superseded_by        TEXT
  FOREIGN KEY (superseded_by) REFERENCES misuse_catalog_version(catalog_version)
)
```

### 2.8 RecheckSession + RecheckFinding + ContaminationSample + DoctrineSnapshot (`schemas/doctrine_recheck.py`)

```
TABLE recheck_session (
  recheck_id           TEXT PRIMARY KEY                 -- "RC-NNN"
  trigger              TEXT NOT NULL CHECK (trigger IN
                         ('PERIODIC','EVENT','SECOND-EYES','OTHER'))
  started_at           TEXT NOT NULL
  closed_at            TEXT
  notes                TEXT
)

TABLE recheck_finding (
  finding_id           TEXT PRIMARY KEY                 -- "RC-NNN-FF"
  recheck_id           TEXT NOT NULL
  severity             TEXT NOT NULL CHECK (severity IN ('INFO','WARNING','BLOCKER'))
  pass_id              TEXT NOT NULL                    -- '2.2' / '2.3' / '2.4' / '2.5' / '2.6'
  description          TEXT NOT NULL
  recommended_action   TEXT NOT NULL
  status               TEXT NOT NULL CHECK (status IN ('OPEN','RESOLVED','DEFERRED'))
  resolution_commit    TEXT
  notes                TEXT
  FOREIGN KEY (recheck_id) REFERENCES recheck_session(recheck_id)
)

TABLE recheck_finding_artifact (
  finding_id           TEXT NOT NULL
  artifact_path        TEXT NOT NULL
  PRIMARY KEY (finding_id, artifact_path)
  FOREIGN KEY (finding_id) REFERENCES recheck_finding(finding_id)
)

TABLE contamination_sample (
  sample_id            INTEGER PRIMARY KEY AUTOINCREMENT
  recheck_id           TEXT NOT NULL
  bpc_slug             TEXT NOT NULL
  classification       TEXT NOT NULL CHECK (classification IN
                         ('CLEAN','AMBIGUOUS','STUB','MERGED'))
  rationale            TEXT
  FOREIGN KEY (recheck_id) REFERENCES recheck_session(recheck_id)
  FOREIGN KEY (bpc_slug) REFERENCES bpc(bpc_slug)
)

TABLE doctrine_snapshot (
  snapshot_id          INTEGER PRIMARY KEY AUTOINCREMENT
  recheck_id           TEXT NOT NULL
  governance_files_count INTEGER NOT NULL
  rules_count          INTEGER NOT NULL
  decisions_count      INTEGER NOT NULL
  snapshot_at          TEXT NOT NULL
  FOREIGN KEY (recheck_id) REFERENCES recheck_session(recheck_id)
)
```

### 2.9 Gap (`schemas/gap.py`)

```
TABLE gap (
  gap_id               TEXT PRIMARY KEY                 -- "GAP-NNN" or "GAP-XX-NN"
  category             TEXT NOT NULL CHECK (category IN
                         ('RP','SW','CR','ST','MX','CD','EC','EG'))
  priority             TEXT NOT NULL CHECK (priority IN ('P1','P2','P3'))
  status               TEXT NOT NULL CHECK (status IN
                         ('OPEN','OPEN-PARTIAL','CLOSED-RESOLVED','CLOSED-DELETED','CLOSED-DEFERRED'))
  skill                TEXT NOT NULL                     -- originating skill
  section              TEXT NOT NULL                     -- affected section
  description          TEXT NOT NULL
  date                 TEXT NOT NULL
)
INDEX idx_gap_priority_status (priority, status)
INDEX idx_gap_category (category)
```

**Polymorphic blocks-relationship** (gap blocks any entity per A3):

```
TABLE gap_blocks (
  gap_id               TEXT NOT NULL
  entity_type          TEXT NOT NULL CHECK (entity_type IN
                         ('specification','population','source','bpc','decision','question'))
  entity_id            TEXT NOT NULL
  PRIMARY KEY (gap_id, entity_type, entity_id)
  FOREIGN KEY (gap_id) REFERENCES gap(gap_id)
  -- Polymorphic FK enforced by validator
)
```

### 2.10 Slug (`schemas/slug.py`)

```
TABLE slug (
  slug                 TEXT PRIMARY KEY
  topic_directory      TEXT NOT NULL
  sl_path              TEXT NOT NULL                    -- search log file path
  bpc_path             TEXT NOT NULL                    -- BPC file path
  status               TEXT NOT NULL CHECK (status IN
                         ('ACTIVE','MERGED','STUB','PROVISIONAL'))
  merged_into          TEXT
  FOREIGN KEY (merged_into) REFERENCES slug(slug)
)
INDEX idx_slug_status (status)
```

### 2.11 Temporal entities (`schemas/temporal.py`) — A9 7-class set

7 tables: `version_tag`, `effective_date_range` (composite type — embedded as columns where used; not own table), `guidebook_version`, `standard_edition`, `project_rule`, `supersedence_link`, `launch_phase_record`.

```
TABLE guidebook_version (
  version_tag          TEXT PRIMARY KEY                 -- "v9.0", "v11.0-draft"
  effective_from       TEXT NOT NULL
  effective_until      TEXT
  status               TEXT NOT NULL CHECK (status IN
                         ('DRAFT','ACTIVE','SUPERSEDED'))
  notes                TEXT
)

TABLE standard_edition (
  edition_id           TEXT PRIMARY KEY                 -- e.g. "ANSI-A117.1-2017"
  family               TEXT NOT NULL                    -- e.g. "ANSI-A117.1"
  edition              TEXT NOT NULL                    -- e.g. "2017"
  jurisdiction         TEXT NOT NULL                    -- e.g. "US-federal", "EU"
  effective_from       TEXT NOT NULL
  effective_until      TEXT
  status               TEXT NOT NULL CHECK (status IN
                         ('CURRENT','SUPERSEDED','WITHDRAWN'))
)
INDEX idx_standard_edition_family (family)
INDEX idx_standard_edition_jurisdiction (jurisdiction)

TABLE project_rule (
  rule_id              TEXT PRIMARY KEY                 -- "R-NNNN"
  text                 TEXT NOT NULL
  effective_from       TEXT NOT NULL
  effective_until      TEXT
  status               TEXT NOT NULL CHECK (status IN
                         ('ACTIVE','SUPERSEDED','RETIRED'))
)

TABLE supersedence_link (
  link_id              INTEGER PRIMARY KEY AUTOINCREMENT
  link_type            TEXT NOT NULL CHECK (link_type IN
                         ('document_version','standard','project_rule','source','launch_phase'))
  from_id              TEXT NOT NULL
  to_id                TEXT NOT NULL
  effective_from       TEXT NOT NULL
  transition_until     TEXT
  rationale            TEXT
  -- from_id/to_id reference the appropriate table per link_type;
  -- polymorphic enforcement at validator level
  -- Cycle detection: recursive CTE in scripts/validate_temporal.py
)
INDEX idx_supersedence_link_type (link_type)
INDEX idx_supersedence_link_from (from_id)
INDEX idx_supersedence_link_to (to_id)

TABLE launch_phase_record (
  phase_id             TEXT PRIMARY KEY                 -- e.g. "Stage-A", "Pre-launch"
  phase_label          TEXT NOT NULL
  effective_from       TEXT NOT NULL
  effective_until      TEXT
  notes                TEXT
)

TABLE version_tag (
  -- A9 §6.1 format: vMAJOR.MINOR
  -- Used as FK references; not its own table at runtime.
  -- Placeholder only — references inline in other tables (guidebook_version.version_tag etc.)
)
-- effective_date_range is a composite (effective_from, effective_until) embedded inline; no separate table.
```

**Note on retrofit:** A9 §7 specifies a converter (`scripts/convert/version_retrofit.py`) that parses `references/project-standards.md` + `references/standards-registry.md` + `versions/` into temporal records. B2 implements this converter against the SQL DDL above; it is currently un-built per Candidate A's score 2 on C-8.1.

---

## 3. Five missing entity types (new schema modules)

The B1 derivation framework §4 lists 20 A3 entity types. The current 14 modules cover 14 of them (counting nested types per A6, and counting A9's 7-class set as 1 module per file convention). Five additional entity types require new schema modules:

### 3.1 Population + Sub-population (`schemas/population.py` — new module)

A7 specifies population codes with sub-codes that inherit parent properties. Single-table inheritance via self-reference.

```
TABLE population (
  code                 TEXT PRIMARY KEY                 -- 'MOB', 'NDV/AUT', etc.
  parent_code          TEXT                              -- NULL for top-level; e.g. 'MOB' for 'MOB/AMB'
  label                TEXT NOT NULL
  definition           TEXT NOT NULL
  -- Default fields (overridable by sub-population):
  prevalence_band      TEXT                              -- e.g. 'common', 'less-common'
  evidence_strength    TEXT                              -- A6 §6 directional
  notes                TEXT
  FOREIGN KEY (parent_code) REFERENCES population(code)
)
INDEX idx_population_parent (parent_code)

-- Inheritance resolution: recursive CTE pattern
-- View: population_resolved that returns each population with inherited+overridden fields
CREATE VIEW population_resolved AS
WITH RECURSIVE pop_chain AS (
  SELECT code, parent_code, label, definition, prevalence_band, evidence_strength, notes,
         0 AS depth
    FROM population WHERE parent_code IS NULL
  UNION ALL
  SELECT p.code, p.parent_code, p.label, p.definition,
         COALESCE(p.prevalence_band, pc.prevalence_band) AS prevalence_band,
         COALESCE(p.evidence_strength, pc.evidence_strength) AS evidence_strength,
         COALESCE(p.notes, pc.notes) AS notes,
         pc.depth + 1
    FROM population p JOIN pop_chain pc ON p.parent_code = pc.code
)
SELECT * FROM pop_chain;
```

**Note:** This is the recursive-CTE pattern that earns C-1.4 a score of 2 under Candidate B (vs A's 3 native). Inheritance resolution is at query time via the `population_resolved` view.

### 3.2 Item (`schemas/item.py` — new module)

A3 §1.7 Items — cross-references between specifications and physical product/system instances.

```
TABLE item (
  item_id              TEXT PRIMARY KEY                 -- "ITEM-NNNN"
  category             TEXT NOT NULL                    -- 'fixture','furniture','assembly',...
  name                 TEXT NOT NULL
  description          TEXT
  specification_refs   TEXT                              -- JSON array of spec_ids; or join table
  notes                TEXT
)

TABLE item_specification (
  item_id              TEXT NOT NULL
  spec_id              TEXT NOT NULL
  PRIMARY KEY (item_id, spec_id)
  FOREIGN KEY (item_id) REFERENCES item(item_id)
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
)
```

### 3.3 Conflict (`schemas/conflict.py` — new module)

A3 §1.8 Conflicts — captures noted divergences between specifications, populations, or specifications-vs-population.

```
TABLE conflict (
  conflict_id          TEXT PRIMARY KEY                 -- "CONF-NNNN"
  conflict_type        TEXT NOT NULL CHECK (conflict_type IN
                         ('spec-vs-spec','spec-vs-population','population-vs-population'))
  description          TEXT NOT NULL
  resolution_status    TEXT NOT NULL CHECK (resolution_status IN
                         ('OPEN','RESOLVED','DEFERRED','UNRESOLVABLE'))
  resolution_decision_id TEXT
  notes                TEXT
  FOREIGN KEY (resolution_decision_id) REFERENCES decision(decision_id)
)

TABLE conflict_party (
  conflict_id          TEXT NOT NULL
  entity_type          TEXT NOT NULL CHECK (entity_type IN ('specification','population'))
  entity_id            TEXT NOT NULL
  party_role           TEXT                              -- 'a-side', 'b-side'
  PRIMARY KEY (conflict_id, entity_type, entity_id)
  FOREIGN KEY (conflict_id) REFERENCES conflict(conflict_id)
)
```

### 3.4 Question (`schemas/question.py` — new module, deferred to B3)

ENT-20 (per b1-criteria-weighting.md §4.4) — Question entity for the questions-led teaching mode (DC-6). The schema is specified here for completeness; implementation is at B3.

```
TABLE question (
  question_id          TEXT PRIMARY KEY                 -- "Q-NNNN"
  question_text        TEXT NOT NULL                    -- e.g. "How wide should this corridor be?"
  applies_to_population TEXT                              -- nullable; FK to population.code
  parameter_class      TEXT                              -- A3 §1.4 hierarchical class
  design_stage         TEXT                              -- when in the design process this question arises
  status               TEXT NOT NULL CHECK (status IN
                         ('DRAFT','ACTIVE','RETIRED'))
  created_at           TEXT NOT NULL
  FOREIGN KEY (applies_to_population) REFERENCES population(code)
)
INDEX idx_question_population (applies_to_population)
INDEX idx_question_class (parameter_class)
INDEX idx_question_design_stage (design_stage)

TABLE question_specification (
  question_id          TEXT NOT NULL                    -- which question
  spec_id              TEXT NOT NULL                    -- which spec answers it
  answer_role          TEXT                              -- 'primary', 'partial', 'related'
  PRIMARY KEY (question_id, spec_id)
  FOREIGN KEY (question_id) REFERENCES question(question_id)
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
)
```

**Note:** B3 owns Question entity specification details; this schema is the storage-form's representation for whatever B3 specifies.

### 3.5 FDR Scenario + Specialist Handoff (`schemas/fdr_specialist.py` — new module)

A3 §1.9 FDR Scenarios — Failure-Demand-Recovery scenarios for resilience analysis. A3 §1.10 Specialist Handoffs — points where specialist consultation is required.

```
TABLE fdr_scenario (
  scenario_id          TEXT PRIMARY KEY                 -- "FDR-NNNN"
  scenario_type        TEXT NOT NULL                    -- 'failure', 'demand-spike', 'recovery'
  description          TEXT NOT NULL
  affected_populations TEXT                              -- JSON array; or use fdr_scenario_population join
  notes                TEXT
)

TABLE fdr_scenario_population (
  scenario_id          TEXT NOT NULL
  population_code      TEXT NOT NULL
  PRIMARY KEY (scenario_id, population_code)
  FOREIGN KEY (scenario_id) REFERENCES fdr_scenario(scenario_id)
  FOREIGN KEY (population_code) REFERENCES population(code)
)

TABLE specialist_handoff (
  handoff_id           TEXT PRIMARY KEY                 -- "SH-NNNN"
  specialist_role      TEXT NOT NULL                    -- 'OT','PT','accessibility-consultant','disability-studies',...
  triggering_condition TEXT NOT NULL                    -- when this handoff is needed
  spec_refs            TEXT                              -- comma-separated spec_ids; or join table
  notes                TEXT
)

TABLE specialist_handoff_specification (
  handoff_id           TEXT NOT NULL
  spec_id              TEXT NOT NULL
  PRIMARY KEY (handoff_id, spec_id)
  FOREIGN KEY (handoff_id) REFERENCES specialist_handoff(handoff_id)
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
)
```

---

## 4. Cross-cutting structural notes

### 4.1 Polymorphic foreign-key pattern

Several tables (`connection_endpoint`, `gap_blocks`, `conflict_party`) require references to "any of N entity types." SQLite's CHECK constraints + a discriminator column + a validator pattern is the operative approach:

```
entity_type TEXT NOT NULL CHECK (entity_type IN ('specification','population',...))
entity_id   TEXT NOT NULL
-- Validator joins to the appropriate table per entity_type to verify entity_id exists.
-- This achieves equivalent integrity to a relational FK at modest cost.
```

Alternative: table-per-target with a discriminator parent (e.g., `gap_blocks_specification`, `gap_blocks_population`, etc.) — rejected as boilerplate-heavy with no integrity advantage given SQLite's lenient typing.

### 4.2 JSON-column usage

Several Pydantic models have variable-shape nested data (`values_criteria_assessment`, `decision_artifacts` arrays, etc.). Two patterns:

- **Normalized to join table** — preferred when the nested structure is queried by content (e.g., `decision_artifact` table because we need to filter decisions by their artifact paths).
- **JSON column** — acceptable when the nested structure is opaque to queries (e.g., `cell.values_criteria_assessment` is read whole, not queried by sub-field).

The DDL above uses join tables wherever queries need to traverse the structure; JSON columns elsewhere. SQLite's JSON1 extension supports query-time JSON path access if a JSON column later requires structured access.

### 4.3 Indexes — sized to query patterns

Indexes are specified above on columns used in WHERE clauses for the audience-priority navigation modes:
- `parameter`, `parameter_class`, `population_code` — for information-finding (C-7.1)
- `design_stage`, `parameter_class` — for decision-frame (C-7.2)
- `cell.population_code`, `cell.state` — for representation-checking (C-7.3)
- `question.applies_to_population`, `question.parameter_class`, `question.design_stage` — for questions-led (C-7.4)

The corpus is bounded; indexes are cheap; over-indexing is a low-cost mitigation against under-indexing.

### 4.4 Triggers for state-machine enforcement

A6 §2.7 specifies cell-state transition rules (e.g., 'silent' → 'stated' requires citing source(s); 'contested' transitions require rationale). These are operationalized as triggers:

```
CREATE TRIGGER cell_state_transition_validate
  BEFORE UPDATE OF state ON cell
  FOR EACH ROW
WHEN NEW.state != OLD.state
BEGIN
  -- Rule 1: 'silent' -> 'stated' requires at least one cell_evidence_source
  SELECT CASE
    WHEN NEW.state = 'stated' AND OLD.state = 'silent'
         AND NOT EXISTS (
           SELECT 1 FROM cell_evidence_source WHERE cell_id = NEW.cell_id
         )
    THEN RAISE(ABORT, 'silent->stated requires at least one cited source')
  END;
  -- Additional rules per A6 §2.7
  -- Rule 2: any state change requires non-empty rationale
  SELECT CASE
    WHEN NEW.state_rationale IS NULL OR LENGTH(TRIM(NEW.state_rationale)) = 0
    THEN RAISE(ABORT, 'state transition requires non-empty state_rationale')
  END;
END;
```

This is the pattern for "blocked at write" enforcement that earns C-2.1 a score of 3 under Candidate B.

### 4.5 Co-1 6-field write-time enforcement

The compound CHECK on `evidence_source` (per §2.1) closes Candidate A's C-3.1 gap:

```
CHECK ((evidence_type = 'co1-collaborator') = (co1_provenance IS NOT NULL
       AND co1_source_type IS NOT NULL
       AND synthesis_attribution_required IS NOT NULL))
```

This makes Co-1 enforcement write-time (the write fails) rather than CI-time (the CI fails).

---

## 5. Migration tooling outline (B2 produces; this section scopes)

Migration from current state (Pydantic-on-YAML files + markdown) to SQLite proceeds in phased order. Each phase is a separate migration script; each script produces a verification report; CI gates progression.

### 5.1 Phase order

| # | Phase | Source data | Target tables | Verification report |
|---|---|---|---|---|
| 1 | Slug migration | `references/slug-set.md` | `slug` | row count match; bpc_path/sl_path resolve |
| 2 | Population taxonomy | `governance/population-taxonomy.md` (A7) | `population` | enumerated 12+ codes present; sub-codes have parent FK |
| 3 | Evidence sources | YAML records under `data/sources/` (when present) + extracted from BPC frontmatter | `evidence_source` | per-tier counts match; Co-1 6-field check on co1-collaborator rows |
| 4 | BPC metadata | `references/bpc/{slug}/bpc.md` frontmatter + `governance/migration-survival.md` classification | `bpc` (only SURVIVES rows) | classification counts match migration-survival §4.1 |
| 5 | Specifications | `parts/v10/` + new spec body extraction | `specification`, `specification_design_stage`, `specification_project_type` | spec_id collision check; parameter+design_stage join coverage |
| 6 | Cells | Per-(spec × population) extraction from BPC content | `cell`, `cell_evidence_source`, `cell_provisional_flag`, `cell_convergence`, `cell_state_transition` | per-spec cell count; state distribution; multi-source attribution coverage |
| 7 | Connections | `references/connections/_index.md` register table + per-CON-ID detail | `connection`, `connection_endpoint` | 188 connection count match; endpoint integrity |
| 8 | Decisions | `data/decisions/decision_register.yaml` | `decision` + 4 join tables | 138+ decision count match (current state); category distribution; FK closure on predecessors/supersedes |
| 9 | Adversarial-use catalog | `data/adversarial_use/catalog.yaml` + per-version review_log files | misuse_vector + supporting tables | vector count match; review counts per version match |
| 10 | Doctrine recheck records | `data/doctrine_recheck/*.yaml` | recheck_session + supporting tables | RC-001, RC-002 records present; sample counts match |
| 11 | Gaps | `gap_register.md` (table form) | `gap`, `gap_blocks` | gap count + priority distribution match |
| 12 | Temporal entities (A9 retrofit) | `references/project-standards.md` + `references/standards-registry.md` + `versions/` | guidebook_version, standard_edition, project_rule, supersedence_link, launch_phase_record | temporal record extraction (specified in A9 §7) |
| 13 | New entity types | (none yet — populated as B3+ produces) | population, item, conflict, question, fdr_scenario, specialist_handoff | per-table integrity |

### 5.2 Per-script structure (B2 specifies in detail)

Each migration script follows the pattern:

```python
# scripts/migrate/NN_target.py
import sqlite3
import yaml
import sys
from pathlib import Path
from schemas.{target} import {EntityType}

def extract():
    """Read source data, validate via Pydantic, produce tuple list."""

def load(conn, rows):
    """Insert tuples into target table(s) using INSERT OR ABORT."""

def verify(conn):
    """Run verification report — count matches, integrity checks."""
    return verification_summary

def main(db_path, source_paths, report_path):
    rows = extract()
    with sqlite3.connect(db_path) as conn:
        load(conn, rows)
        report = verify(conn)
    Path(report_path).write_text(report)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:-1], sys.argv[-1])
```

### 5.3 Verification gate

Each phase's verification report must pass before the next phase runs. CI checks per-phase:
- Row counts match expected (extracted from source).
- FK integrity (no dangling references).
- CHECK constraint compliance (enum values, range checks).
- Phase-specific invariants (per phase column above).

**This validation suite is the work that earns Candidate B its C-9.1 (CI tractability) score of 2 — moderate cost, mechanical work, well-understood patterns.**

### 5.4 Migration-out tooling (S-05 5-deliverable standard)

Per D-0111 and D-0138 §5.6, migration-out cost must be bounded. Two operative paths:

```bash
# Full data export
sqlite3 guidebook.db .dump > export.sql

# Schema-only (for re-creation)
sqlite3 guidebook.db .schema > schema.sql

# CSV per table (for tabular tools)
for table in $(sqlite3 guidebook.db ".tables"); do
  sqlite3 guidebook.db ".mode csv" ".headers on" "SELECT * FROM ${table}" > "export_${table}.csv"
done
```

Schema-mapping documents to alternative forms (markdown, RDF) are produced at need; the SQL DDL above is canonical input.

---

## 6. Decision-capture for Session 9

### 6.1 D-0139 — architecture/schema-spec.md issued

| Field | Value |
|---|---|
| category | D-SCHEMA |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0119, D-0121, D-0132, D-0138 |

DG-REVIEW per A12 §2: "Schema decisions reach all entity types and validators." This is a methodological commitment that constrains B2 and beyond. Project-owner review confirms the schema spec accurately translates the Pydantic schemas, captures the 5 missing types correctly, and outlines the migration phasing soundly.

PROVISIONAL because D-0138 (storage form selection) is itself PROVISIONAL pending project-owner adoption. Schema spec becomes operative in lockstep.

### 6.2 D-0140 — governance/repo-strategy.md revision proposed

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/100/route |
| effort_level | 100 |
| predecessors | D-0138, D-0139 |

DG-REVIEW per A12. The revision proposal updates the repo-strategy with the operative storage form (SQLite) and resolves the deferred trigger from §"Trigger for revisit" of the original document. Project owner adopts.

The proposed revision:
- Same repo: continue in `jordanelias/guidebook` `main`. The trigger table predicted "Likely sibling repo or sub-directory (`db/`) for the database" — the actual recommendation is **subdirectory `data/db/` for the SQLite file**, NOT a sibling repo. Rationale: SQLite is a single file; a sibling repo for one binary file is overhead without benefit; the audit trail of decisions and migrations belongs alongside the corpus.
- Add `architecture/` directory recognition (already created at S8).
- Add `data/db/guidebook.db` as the operative substrate location once adopted.
- Migration tooling lives under `scripts/migrate/`.
- The original "sibling repo" predictions were conservative estimates pre-substrate-selection; SQLite's single-file form makes them moot.

This revision is committed by Session 9 as `governance/repo-strategy-revision-co.md` (a Change Order proposal-of-record); the original `governance/repo-strategy.md` is amended only on project-owner adoption.

---

## 7. Status

| Field | Value |
|---|---|
| B1 Session 9 | COMPLETE |
| Session 9 deliverables | (1) `architecture/schema-spec.md` (this document); (2) `governance/repo-strategy-revision-co.md` (revision proposal) |
| Decisions captured | D-0139 (D-SCHEMA/DG-REVIEW PENDING); D-0140 (D-OP/DG-REVIEW PENDING) |
| Working session counter | 11 → 12 |
| Status of D-0138 (storage form) | PROVISIONAL — project-owner adoption converts to CANONICAL |
| Status of D-0139 (this schema spec) | PROVISIONAL — operative on D-0138 adoption |
| Status of D-0140 (repo-strategy revision) | PROPOSED — project-owner adoption applies |
| **B1 Phase 1 status** | **9 of 6–9 sessions consumed; substantively COMPLETE pending project-owner adoptions** |
| Next phase | B2 — Tooling design with expanded validator suite (4–6 sessions per workplan v3 §B2). Begins after D-0138/D-0139 adoption. |

### 7.1 What Session 9 deliberately did NOT do

- **Did NOT produce `architecture/storage-decision.md`.** Per the S8 next-action note: that lightweight terminal-state document is "created only after D-0138 adoption converts PROVISIONAL → CANONICAL." Session 9 cannot create it because adoption is a project-owner action.
- **Did NOT amend the existing `governance/repo-strategy.md`.** The revision is a proposal-of-record (`repo-strategy-revision-co.md`); the original is amended on adoption.
- **Did NOT produce the actual SQL DDL files.** The DDL above is the specification; B2 produces the `.sql` artifacts and the migration tooling.
- **Did NOT produce SQLAlchemy ORM models.** B2 produces the Pydantic↔SQLAlchemy mapping.
- **Did NOT validate the existing 14 schemas against the proposed DDL.** B2's first verification step does this; finding deltas would be a B2 finding, not a Session 9 amendment.

### 7.2 B1 Phase 1 completion summary

B1 Phase 1 produced 9 sessions worth of work distributed across the framework:

| Session | Output | Decisions |
|---|---|---|
| 1 | `b1-derivation-framework.md` | D-0108, D-0109 |
| 2 | `b1-criteria-weighting.md` | D-0110, D-0111, D-0112, D-0113 |
| 3 | `b1-candidate-a-markdown-yaml.md` | D-0119 |
| 4 | `b1-candidate-b-relational.md` | D-0120 (substrate=SQLite), D-0121 (score 152) |
| 5 | `b1-candidate-c-graph.md` | D-0131 (substrate=RDF/Jena), D-0132 (score 155) |
| 6 | `b1-candidate-d-hybrid.md` | D-0133 (substrate=H1), D-0134 (D dismissed), D-0135 (informational score) |
| 7 | `b1-comparative-scoring.md` | D-0136 (matrix), D-0137 (Rule 3) |
| 8 | `architecture/storage-derivation.md` | **D-0138 (storage = SQLite, PENDING adoption)** |
| 9 | `architecture/schema-spec.md` (this) + `governance/repo-strategy-revision-co.md` | D-0139 (this schema), D-0140 (repo-strategy revision) |

Total: **23 Decision records** (D-0108..D-0140 contiguous; D-0122..D-0128 are unrelated parallel-session decisions). All are either DG-AUTO (no review needed) or DG-REVIEW PENDING / DG-NON PENDING adoption. None are blocking on agent work.

**B1 closes here.** Stage B Phase 2 (B2 Tooling design) begins at project-owner discretion after D-0138/D-0139 adoption.

---

## 8. Change log

- **2026-05-02 02:50** — Created at B1 Session 9. PROVISIONAL pending D-0138 adoption.


---

## 9. D-0139 Amendment 1 (2026-05-03)

**See:** `architecture/d0139-amendment-1.md` for full specification.

**Summary:** 21 new columns added to specification table (16 atomic + 5 JSON). 3 new tables created (measurement, jurisdictional_value, performance_criterion). specification_population join table amended with role column. Schema reconciliation document at `architecture/schema-reconciliation.md` resolves all 5 parallel schema representations into this canonical DDL.

**Columns added to specification:**
question_heading, question_summary, summary, evidence_summary, person_specific_note, why_md, schedule_md, diagram_svg, diagram_type, dar_relevant, dar_note, structural_backing_required, retrofit_category, ot_evidence_basis, curation_status, item_code, bpc_source_slug, recommendation_strength, percentile_basis, conflict_domains, failures_json, install_notes_json, detail_groups_json, pop_reasons_json, topics_json.
