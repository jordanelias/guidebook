# D-0139 Amendment 1 — Specification Table Expansion
**Created:** 2026-05-03 23:10 UTC
**Amends:** `architecture/schema-spec.md` §2.3 (Specification table)
**Authority:** Amendment 8 (workplan-amendment-8-audit-integrated-2026-05-03.md) + schema reconciliation (architecture/schema-reconciliation.md)
**Decision category:** D-SCHEMA / DG-REVIEW
**Status:** ACTIVE

---

## 1. Summary

This amendment adds 21 columns to the `specification` table, creates 3 new tables, amends 1 join table, and adds corresponding Pydantic model fields. All additions serve the website IA's 14 page templates.

---

## 2. Specification table — 16 new atomic columns

Add after `modified_at` in the existing DDL:

```sql
-- Question mode (DC-6)
question_heading             TEXT,           -- question-form heading, mandatory for rendering
question_summary             TEXT,           -- question-mode summary variant

-- Display atoms
summary                      TEXT,           -- spec-mode one-sentence summary (card view)
evidence_summary             TEXT,           -- short citation string for card view
tier_2_note                  TEXT,           -- person-specific mode note (OT handoff)

-- Authored prose sections
why_md                       TEXT,           -- "Why it matters" authored prose
schedule_md                  TEXT,           -- schedule language (copyable text)

-- Diagrams
diagram_svg                  TEXT,           -- inline SVG content
diagram_type                 TEXT CHECK (diagram_type IN
                               ('plan','section','elevation','isometric','chart',NULL)),

-- DAR integration
dar_relevant                 INTEGER DEFAULT 0,
dar_note                     TEXT,

-- Engineering coordination
structural_backing_required  INTEGER DEFAULT 0,

-- Classification and status
retrofit_category            TEXT CHECK (retrofit_category IN
                               ('LOW-PLANNING','LOW-FIXTURE','MODERATE','HIGH','STRUCTURAL',NULL)),
ot_evidence_basis            TEXT,           -- OT framework citation string
curation_status              TEXT CHECK (curation_status IN
                               ('automated','reviewed','opus_synthesized')) DEFAULT 'automated',

-- Migration tracking
item_code                    TEXT,           -- e.g. 'E-08' (from spec-db JSON)
bpc_source_slug              TEXT,           -- source BPC file slug
recommendation_strength      TEXT CHECK (recommendation_strength IN
                               ('Strong','Conditional','Weak','Consensus',NULL)),
percentile_basis             TEXT,           -- anthropometric percentile basis if applicable
```

### 2.1 Additional indexes

```sql
CREATE INDEX idx_specification_item_code (item_code);
CREATE INDEX idx_specification_dar (dar_relevant);
CREATE INDEX idx_specification_curation (curation_status);
CREATE INDEX idx_specification_bpc (bpc_source_slug);
```

---

## 3. Specification table — 5 JSON columns

Add after the atomic columns. These store content atoms as JSON arrays/objects. Per §4.2 of schema-spec, JSON columns are acceptable when the nested structure is read whole (not queried by sub-field).

```sql
-- Content atoms from prototype ITEMS (read whole, not queried by sub-field)
conflict_domains             TEXT,           -- JSON array of conflict domain IDs, e.g. '["ACOUSTIC-LVL","LIGHT-INT"]'
failures_json                TEXT,           -- JSON array of failure pattern strings
install_notes_json           TEXT,           -- JSON array of installation note strings
detail_groups_json           TEXT,           -- JSON array of {title, items[]} objects
pop_reasons_json             TEXT,           -- JSON object keyed by PopulationCode
topics_json                  TEXT,           -- JSON array of topic strings
```

### 3.1 JSON validation constraints

The CI validator (`validate_schema.py`) validates JSON column content:
- `conflict_domains`: must be JSON array of strings matching `^[A-Z][-A-Z]+$`
- `failures_json`: must be JSON array of non-empty strings
- `install_notes_json`: must be JSON array of non-empty strings
- `detail_groups_json`: must be JSON array of objects with `title` (string) and `items` (array of strings)
- `pop_reasons_json`: must be JSON object with keys matching population codes
- `topics_json`: must be JSON array of non-empty strings

---

## 4. New table: `measurement`

```sql
CREATE TABLE measurement (
  measurement_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  design_mode      TEXT NOT NULL CHECK (design_mode IN ('universal','population_based','person_specific')),
  population_code  TEXT,                    -- NULL for universal mode; required for population_based
  value_type       TEXT NOT NULL CHECK (value_type IN ('fixed','range','minimum','maximum','categorical')),
  value_min        REAL,
  value_max        REAL,
  value_median     REAL,
  unit             TEXT,
  condition_text   TEXT,                    -- conditional applicability, e.g. "DEM primary occupant"
  source_ref       TEXT,                    -- evidence source reference
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code),
  CHECK (design_mode != 'population_based' OR population_code IS NOT NULL)
);
CREATE INDEX idx_measurement_spec (spec_id);
CREATE INDEX idx_measurement_mode (design_mode);
CREATE INDEX idx_measurement_pop (population_code);
```

**Purpose:** Replaces the flat `value_min`/`value_max`/`value_median` on the spec-db JSON record. One specification can have multiple measurements (one per design mode, optionally per population within population_based mode, and per condition).

**Rendering query for spec page:**
```sql
SELECT m.*, p.label AS population_label
FROM measurement m
LEFT JOIN population p ON m.population_code = p.code
WHERE m.spec_id = ?
ORDER BY
  CASE m.design_mode
    WHEN 'universal' THEN 1
    WHEN 'population_based' THEN 2
    WHEN 'person_specific' THEN 3
  END,
  m.population_code;
```

---

## 5. New table: `jurisdictional_value`

```sql
CREATE TABLE jurisdictional_value (
  jv_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  jurisdiction     TEXT NOT NULL,           -- ISO 3166-1 alpha-2 (AU, CA, DE, etc.)
  standard_name    TEXT,                    -- e.g. "AS 1428.1:2021"
  clause_reference TEXT,                    -- e.g. "§7.2(a)"
  value_text       TEXT,                    -- human-readable value string
  value_numeric    REAL,                    -- machine-comparable value (mm, degrees, etc.)
  unit             TEXT,
  is_code_minimum  INTEGER DEFAULT 1,      -- 1 = code minimum (Tier 6); 0 = beyond-code standard
  evidence_tier    INTEGER,                 -- typically 4, 5, or 6
  notes            TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);
CREATE INDEX idx_jv_spec (spec_id);
CREATE INDEX idx_jv_jurisdiction (jurisdiction);
CREATE UNIQUE INDEX idx_jv_unique (spec_id, jurisdiction, standard_name, COALESCE(clause_reference,''));
```

**Purpose:** The jurisdictional master index. Stores code values per specification per jurisdiction. Enables the three-cell-state rendering: value present (green), no requirement (red), not searched (grey).

**Rendering query for master index:**
```sql
SELECT s.spec_id, s.item_code, s.title, j.jurisdiction, j.value_text, j.standard_name
FROM specification s
LEFT JOIN jurisdictional_value j ON s.spec_id = j.spec_id
WHERE s.status = 'active'
ORDER BY s.item_code, j.jurisdiction;
```

---

## 6. New table: `performance_criterion`

```sql
CREATE TABLE performance_criterion (
  criterion_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  metric           TEXT NOT NULL,           -- e.g. "minimum clear width"
  target           TEXT NOT NULL,           -- e.g. "≥1200mm"
  measure          TEXT,                    -- e.g. "physical measurement at narrowest point"
  population_code  TEXT,                    -- NULL if applies universally
  source_ref       TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX idx_pc_spec (spec_id);
```

**Purpose:** Structured performance criteria per specification. Prototype ITEMS have `performance[]` arrays that map to rows here.

---

## 7. Amended join table: `specification_population`

Replace the implicit array-based population linkage with a structured join table that distinguishes role:

```sql
CREATE TABLE specification_population (
  spec_id          TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  role             TEXT NOT NULL CHECK (role IN ('primary','secondary','all')),
  PRIMARY KEY (spec_id, population_code),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX idx_spec_pop_role (role);
```

**Migration:** R3 `populations[]` → all rows with `role='all'`. Population role refinement (primary vs secondary) is a C3/C4 curation task.

---

## 8. Complete specification table DDL (post-amendment)

For reference, the full specification table after this amendment:

```sql
CREATE TABLE specification (
  -- Primary key and identity (from D-0139 original)
  spec_id                      TEXT PRIMARY KEY,
  slug                         TEXT NOT NULL UNIQUE,
  title                        TEXT NOT NULL,
  parameter                    TEXT NOT NULL,
  parameter_class              TEXT NOT NULL,
  body_md                      TEXT,
  guidebook_version            TEXT,
  status                       TEXT CHECK (status IN ('draft','provisional','active','superseded')),
  created_at                   TEXT NOT NULL,
  modified_at                  TEXT NOT NULL,

  -- Question mode (Amendment 1)
  question_heading             TEXT,
  question_summary             TEXT,

  -- Display atoms (Amendment 1)
  summary                      TEXT,
  evidence_summary             TEXT,
  tier_2_note                  TEXT,

  -- Authored prose (Amendment 1)
  why_md                       TEXT,
  schedule_md                  TEXT,

  -- Diagrams (Amendment 1)
  diagram_svg                  TEXT,
  diagram_type                 TEXT CHECK (diagram_type IN
                                 ('plan','section','elevation','isometric','chart',NULL)),

  -- DAR (Amendment 1)
  dar_relevant                 INTEGER DEFAULT 0,
  dar_note                     TEXT,

  -- Engineering (Amendment 1)
  structural_backing_required  INTEGER DEFAULT 0,

  -- Classification (Amendment 1)
  retrofit_category            TEXT CHECK (retrofit_category IN
                                 ('LOW-PLANNING','LOW-FIXTURE','MODERATE','HIGH','STRUCTURAL',NULL)),
  ot_evidence_basis            TEXT,
  curation_status              TEXT CHECK (curation_status IN
                                 ('automated','reviewed','opus_synthesized')) DEFAULT 'automated',

  -- Migration tracking (Amendment 1)
  item_code                    TEXT,
  bpc_source_slug              TEXT,
  recommendation_strength      TEXT CHECK (recommendation_strength IN
                                 ('Strong','Conditional','Weak','Consensus',NULL)),
  percentile_basis             TEXT,

  -- JSON content atoms (Amendment 1)
  conflict_domains             TEXT,
  failures_json                TEXT,
  install_notes_json           TEXT,
  detail_groups_json           TEXT,
  pop_reasons_json             TEXT,
  topics_json                  TEXT
);

-- Indexes (original + Amendment 1)
CREATE INDEX idx_specification_parameter (parameter);
CREATE INDEX idx_specification_class (parameter_class);
CREATE INDEX idx_specification_status (status);
CREATE INDEX idx_specification_item_code (item_code);
CREATE INDEX idx_specification_dar (dar_relevant);
CREATE INDEX idx_specification_curation (curation_status);
CREATE INDEX idx_specification_bpc (bpc_source_slug);
```

---

## 9. Pydantic model impact

`schemas/specification.py` requires the following additions to match this DDL:

- 16 new `Optional[str]` or `Optional[int]` fields for atomic columns
- 6 new `Optional[str]` fields for JSON columns (validated as JSON at write time)
- New enum values in `schemas/enums.py`: `DiagramType`, `RetrofitCategory`, `CurationStatus`, `DesignMode`, `PopulationRole`

B2.4 produces the updated Pydantic models.

---

## 10. Change log

| Date | Change |
|---|---|
| 2026-05-03 23:10 | D-0139 Amendment 1 issued. 21 columns, 3 tables, 1 join table amended. |
