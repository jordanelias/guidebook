# Schema Reconciliation — B2.1
**Created:** 2026-05-03 22:55 UTC
**Model:** Opus 4.6
**Inputs:** 5 schema representations + Amendment 8 + website IA
**Status:** ACTIVE — governs all downstream schema work

---

## 1. Five representations reconciled

This document resolves the five parallel schema representations identified in AF-4 (repository audit finding) into one canonical form: the SQLite DDL specified in `architecture/schema-spec.md` (D-0139), with rendering queries derived from the unified website schema's display requirements.

### 1.1 Representations and their roles

| # | Representation | Location | Role post-reconciliation |
|---|---|---|---|
| R1 | SQL DDL | `architecture/schema-spec.md` §2.3 | **CANONICAL** — storage form. All other representations derive from this. |
| R2 | Unified website schema | `references/website/schema/unified-data-schema.md` | **DISPLAY CONTRACT** — defines what each page template needs. Rendering queries satisfy this contract from R1 storage. |
| R3 | Spec-db JSON | `references/specification-database.json` | **MIGRATION SOURCE** — 73 records with 22 fields. Consumed by migration scripts; superseded by SQLite post-migration. Retained as archival snapshot. |
| R4 | populations.json | `references/website/data/populations.json` | **MIGRATION SOURCE** — population entity data. Consumed by `convert_populations.py` into population table. Retained as archival. |
| R5 | conflicts.json | `references/website/data/conflicts.json` | **MIGRATION SOURCE** — conflict entity data. Consumed by `convert_conflicts.py` into conflict table. Retained as archival. |

**Post-migration state:** R1 (SQLite DDL) is the single source of truth. R2 (display contract) is the rendering specification. R3–R5 are frozen migration sources.

### 1.2 Pydantic layer

`schemas/specification.py` is the write-time validator. It mirrors R1's DDL and rejects records that would violate column constraints. The Pydantic model is the programmatic interface to R1 — not a separate representation.

---

## 2. Display field resolution — 24 fields

For each display field in R2 (unified-data-schema), this table resolves whether the data is: a **SQL column** (stored directly), a **JSON column** (stored as JSON text), a **join query** (computed from related tables), or **render-time computed** (derived by the page generator).

| # | Display field | Resolution | SQL location | Rationale |
|---|---|---|---|---|
| 1 | `item_title` | SQL column | `specification.title` (existing) | Already present as `title` in R1 DDL. R3 stores `item_code` separately; `title` serves display. |
| 2 | `category_name` | Render-time computed | Derive from `item_code` prefix via static lookup | 11 categories (A–K); lookup table or code constant. Not worth a column. |
| 3 | `parameter_label` | SQL column | `specification.parameter` (existing, rename display) | `parameter` column holds the slug; display label computed by replacing hyphens with spaces + title case. No new column needed. |
| 4 | `unit_display` | Render-time computed | Format from `measurement.unit` + values | e.g., "3–5 m" from min=3000, max=5000, unit=mm. Rendering logic. |
| 5 | `universal_value` / `universal_value` | Join query | `measurement` table WHERE `design_mode = 'universal'` | **New table** (Amendment 8). One measurement row per (spec × design_mode). |
| 6 | `population_value` / `population_value` | Join query | `measurement` table WHERE `design_mode = 'population_based'` | Same table, different design_mode. |
| 7 | `person_specific_note` / `person_specific_note` | SQL column | `specification.person_specific_note` (new) | Single text field per spec. Already in R3; add to R1. |
| 8 | `evidence_marker` | Render-time computed | Derive from `evidence_state_record.state` for this spec | ● = stated, ◐ = provisional, ○ = pending. No storage needed. |
| 9 | `evidence_summary` | SQL column | `specification.evidence_summary` (new) | Short citation string for card view. Authored, not derived. |
| 10 | `population_primary` | Join query | `specification_population` join table with `role = 'primary'` | Extend existing `specification_population` with `role` column. |
| 11 | `population_secondary` | Join query | `specification_population` join table with `role = 'secondary'` | Same table, different role. |
| 12 | `jurisdiction_count` | Render-time computed | `SELECT COUNT(DISTINCT jurisdiction) FROM jurisdictional_value WHERE spec_id = ?` | Computed from **new table** (Amendment 8). |
| 13 | `language_count` | Render-time computed | Count from BPC metadata or static | Not a per-spec SQL value; derived from BPC coverage data. |
| 14 | `retrofit_penalty` | SQL column | `specification.retrofit_category` (new) | Enum: LOW-PLANNING, LOW-FIXTURE, MODERATE, HIGH, STRUCTURAL. |
| 15 | `dar_relevant` | SQL column | `specification.dar_relevant` (new, Amendment 8) | INTEGER DEFAULT 0. |
| 16 | `dar_note` | SQL column | `specification.dar_note` (new, Amendment 8) | TEXT. |
| 17 | `cross_references` | Join query | `connection_endpoint` WHERE `entity_type = 'specification'` | Existing connection table handles cross-references. |
| 18 | `connection_ids` | Join query | Same as above | Connection IDs are the relationship entity. |
| 19 | `conflict_domains` | JSON column | `specification.conflict_domains` (new, Amendment 8) | JSON array of conflict domain IDs. Denormalized for rendering speed. |
| 20 | `ot_evidence_basis` | SQL column | `specification.ot_evidence_basis` (new) | TEXT. OT framework citation string. |
| 21 | `fdr_findings` | Join query | `fdr_scenario` via `fdr_scenario_specification` join | Existing table from §3.5. |
| 22 | `citations` | Join query | `evidence_source` via `cell_evidence_source` | Existing evidence_source table. |
| 23 | `last_updated` | SQL column | `specification.modified_at` (existing) | Already in R1 DDL. |
| 24 | `curation_status` | SQL column | `specification.curation_status` (new) | Enum: automated, reviewed, opus_synthesized. |

### 2.1 Resolution summary

| Resolution type | Count | Fields |
|---|---|---|
| Existing SQL column | 4 | title, parameter, modified_at, (person_specific_note via R3) |
| New SQL column | 9 | person_specific_note, evidence_summary, retrofit_category, dar_relevant, dar_note, ot_evidence_basis, curation_status, + Amendment 8 cols |
| New JSON column | 1 | conflict_domains |
| Join query | 7 | universal/population values, population roles, jurisdiction count, cross_references, connection_ids, fdr_findings, citations |
| Render-time computed | 4 | category_name, unit_display, evidence_marker, language_count |

---

## 3. D-SCHEMA records — 18 field resolution decisions

Each display field resolution is a D-SCHEMA decision per A12 protocol.

| D-SCHEMA ID | Field | Decision | Category | Delegation |
|---|---|---|---|---|
| D-SCHEMA-001 | item_title | Map to existing `title` column | D-PRES | DG-AUTO |
| D-SCHEMA-002 | category_name | Render-time computed from item_code prefix | D-PRES | DG-AUTO |
| D-SCHEMA-003 | parameter_label | Render-time computed from parameter slug | D-PRES | DG-AUTO |
| D-SCHEMA-004 | unit_display | Render-time formatted from measurement values | D-PRES | DG-AUTO |
| D-SCHEMA-005 | tier values (universal/population/person) | New `measurement` table + `person_specific_note` column | D-SCHEMA | DG-REVIEW |
| D-SCHEMA-006 | evidence_marker | Render-time from evidence_state_record | D-PRES | DG-AUTO |
| D-SCHEMA-007 | evidence_summary | New column on specification | D-SCHEMA | DG-AUTO |
| D-SCHEMA-008 | population roles | Add `role` to specification_population join | D-SCHEMA | DG-REVIEW |
| D-SCHEMA-009 | jurisdiction/language counts | Render-time COUNT queries | D-PRES | DG-AUTO |
| D-SCHEMA-010 | retrofit_category | New column on specification | D-SCHEMA | DG-AUTO |
| D-SCHEMA-011 | dar_relevant + dar_note | New columns per Amendment 8 | D-SCHEMA | DG-AUTO |
| D-SCHEMA-012 | cross_references | Existing connection table | D-SCHEMA | DG-AUTO |
| D-SCHEMA-013 | conflict_domains | JSON column per Amendment 8 | D-SCHEMA | DG-AUTO |
| D-SCHEMA-014 | ot_evidence_basis | New column on specification | D-SCHEMA | DG-AUTO |
| D-SCHEMA-015 | fdr_findings | Join to fdr_scenario table | D-SCHEMA | DG-AUTO |
| D-SCHEMA-016 | citations | Join to evidence_source table | D-SCHEMA | DG-AUTO |
| D-SCHEMA-017 | curation_status | New column on specification | D-SCHEMA | DG-AUTO |
| D-SCHEMA-018 | Amendment 8 content atoms | 11 new columns + 5 JSON columns per Amendment 8 | D-SCHEMA | DG-REVIEW |

---

## 4. Amendment 8 columns — reconciliation with R2 display fields

The 11 new columns and 5 JSON columns specified in Amendment 8 serve the website IA's page templates. Their relationship to R2 display fields:

| Amendment 8 column | R2 display field served | Relationship |
|---|---|---|
| `question_heading` | Page template: question-mode heading | NEW — not in R2 (R2 predates question-mode IA) |
| `question_summary` | Page template: question-mode summary | NEW — not in R2 |
| `summary` | Card view one-sentence summary | Maps to `evidence_summary` in R2 (consolidate to one column) |
| `why_md` | Spec page "Why it matters" section | NEW — not in R2 |
| `schedule_md` | Spec page schedule language (copyable) | NEW — not in R2 |
| `diagram_svg` | Spec page inline diagram | NEW — not in R2 |
| `diagram_type` | Rendering hint for diagram display | NEW — not in R2 |
| `dar_relevant` | R2 `dar_relevant` | Direct match |
| `dar_note` | R2 `dar_note` | Direct match |
| `conflict_domains` | R2 `conflict_domains` | Direct match |
| `structural_backing_required` | Engineering coordination flag | NEW — not in R2 |
| `failures_json` | Spec page failure patterns section | NEW — not in R2 (from prototype ITEMS) |
| `install_notes_json` | Spec page installation notes | NEW — not in R2 (from prototype ITEMS) |
| `detail_groups_json` | Spec page detail groups | NEW — not in R2 (from prototype ITEMS) |
| `pop_reasons_json` | Population page per-spec reasoning | NEW — not in R2 (from prototype ITEMS) |
| `topics_json` | Topic tagging for search/filter | NEW — not in R2 |

**Reconciliation note:** R2 was drafted at Phase 0.1 (2026-04-09) before the website IA and before B1 schema design. Amendment 8 columns supersede R2's field list for specification page content. R2 remains the display contract for overall page structure; field-level authority transfers to the DDL (R1) with this reconciliation.

---

## 5. New tables — reconciliation

### 5.1 `measurement` table

Replaces R2's inline `universal_value`, `population_value` on the specification record. One row per (spec × design_mode × optional population). Enables multi-value specifications with different measurements per design mode.

```sql
CREATE TABLE measurement (
  measurement_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  design_mode      TEXT NOT NULL CHECK (design_mode IN ('universal','population_based','person_specific')),
  population_code  TEXT,                    -- NULL for universal mode
  value_type       TEXT NOT NULL CHECK (value_type IN ('fixed','range','minimum','maximum','categorical')),
  value_min        REAL,
  value_max        REAL,
  value_median     REAL,
  unit             TEXT,
  condition_text   TEXT,                    -- e.g. "DEM or NEU/PCS primary occupant"
  source_ref       TEXT,                    -- evidence source reference
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX idx_measurement_spec (spec_id);
CREATE INDEX idx_measurement_mode (design_mode);
CREATE INDEX idx_measurement_pop (population_code);
```

**Migration source:** R3 `value_min`, `value_max`, `value_median`, `unit`, `value_type`, `conditions[]` → one or more measurement rows per spec. R3's `conditions` array maps to multiple measurement rows with `condition_text`.

### 5.2 `jurisdictional_value` table

```sql
CREATE TABLE jurisdictional_value (
  jv_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  jurisdiction     TEXT NOT NULL,           -- ISO 3166-1 alpha-2
  standard_name    TEXT,                    -- e.g. "AS 1428.1:2021"
  clause_reference TEXT,                    -- e.g. "§7.2(a)"
  value_text       TEXT,                    -- human-readable value
  value_numeric    REAL,                    -- machine-comparable value
  unit             TEXT,
  is_code_minimum  INTEGER DEFAULT 1,      -- 1 = this is a code minimum, 0 = best-practice from standard
  evidence_tier    INTEGER,                 -- 4, 5, or 6 typically
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);
CREATE INDEX idx_jv_spec (spec_id);
CREATE INDEX idx_jv_jurisdiction (jurisdiction);
CREATE UNIQUE INDEX idx_jv_unique (spec_id, jurisdiction, standard_name, clause_reference);
```

**Migration source:** R3 `jurisdictions_supporting[]`, `jurisdictions_divergent[]` → jurisdiction codes without values. Appendix A (20 tables, ~150-200 rows) → full `(spec_id, jurisdiction, value)` tuples. B2.3 performs the Appendix A migration.

### 5.3 `performance_criterion` table

```sql
CREATE TABLE performance_criterion (
  criterion_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  metric           TEXT NOT NULL,           -- e.g. "minimum clear width"
  target           TEXT NOT NULL,           -- e.g. "≥1200mm"
  measure          TEXT,                    -- e.g. "physical measurement at narrowest point"
  population_code  TEXT,                    -- NULL if universal
  source_ref       TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX idx_pc_spec (spec_id);
```

**Migration source:** Prototype ITEMS `performance[]` arrays + Part 4 content. No equivalent in R3 currently.

### 5.4 `specification_population` join table (amended)

Existing join implied by R3's `populations[]` array. Amendment: add `role` column.

```sql
CREATE TABLE specification_population (
  spec_id          TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  role             TEXT NOT NULL CHECK (role IN ('primary','secondary','all')),
  PRIMARY KEY (spec_id, population_code),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
```

**Migration source:** R3 `populations[]` → all as role='all'. R2 `population_primary[]`, `population_secondary[]` → separate role values. Reconciliation needed per spec.

---

## 6. R3 → R1 migration field map

How spec-db JSON (R3) fields map to the canonical DDL (R1) post-amendment:

| R3 field | R1 location | Migration action |
|---|---|---|
| `spec_id` | `specification.spec_id` | Direct copy |
| `slug` | `specification.slug` | Direct copy |
| `item_code` | Derivable from `spec_id` | Store in `specification.item_code` (add column if not present) |
| `parameter` | `specification.parameter` | Direct copy |
| `value_type` | `measurement.value_type` | Move to measurement table |
| `value_min` | `measurement.value_min` | Move to measurement table |
| `value_max` | `measurement.value_max` | Move to measurement table |
| `value_median` | `measurement.value_median` | Move to measurement table |
| `unit` | `measurement.unit` | Move to measurement table |
| `evidence_tier` | Derive from evidence_source linkage | Not a column on specification; derived |
| `populations` | `specification_population` join | Expand array to join rows |
| `jurisdictions_supporting` | `jurisdictional_value` rows | Create JV rows with `is_code_minimum=1` |
| `jurisdictions_divergent` | `jurisdictional_value` rows | Create JV rows with divergence note |
| `divergence_note` | `jurisdictional_value.value_text` or spec notes | Contextual |
| `opus_synthesized` | `specification.curation_status` | Map: true → 'opus_synthesized' |
| `bpc_source_slug` | `specification.bpc_source_slug` (add column) | Direct copy |
| `recommendation_strength` | `specification.recommendation_strength` (add column) | Direct copy |
| `person_specific_note` | `specification.person_specific_note` (add column) | Direct copy |
| `percentile_basis` | `specification.percentile_basis` (add column) | Direct copy |
| `notes` | `specification.body_md` or separate notes | Merge with body_md |
| `conditions` | `measurement` rows with `condition_text` | Expand array to measurement rows |
| `context_note` | Superseded by structured citations | Migrate to evidence_source linkage |

---

## 7. Parser-to-pipeline mapping (26 parsers)

The `workplan/website-preparation.md` defines 26 parsers for the Claude Code website build (Next.js + PostgreSQL + Directus + Meilisearch). Post-D-0138 (SQLite canonical storage), each parser maps to one of three pipeline roles:

| Role | Description | Count |
|---|---|---|
| **Migration script** | Extracts data from current repo files into SQLite tables. Runs once. | 13 |
| **Rendering query** | SQL query executed by the static site generator at render time. Replaces the parser entirely. | 9 |
| **Redundant** | Parser's function is absorbed by the migration + rendering pipeline. No equivalent needed. | 4 |

### 7.1 Parser mapping detail

| Parser tier | Parser function | Post-D-0138 role | Replacement |
|---|---|---|---|
| **T1 (reference)** | | | |
| p01 standards registry | Migration script | `scripts/migrate/phase_standards.py` → `standard` table |
| p02 glossary | Migration script | `scripts/migrate/phase_glossary.py` → `glossary_entry` table |
| p03 gap register | Migration script | `scripts/migrate/phase_gaps.py` → `gap` table (already exists) |
| p04 population codes | Migration script | `convert_populations.py` (exists) → `population` table |
| p05 connections | Migration script | `convert_connections.py` (exists) → `connection` table |
| **T2 (core)** | | | |
| p09 specifications | Migration script | `scripts/migrate/phase_specifications.py` → `specification` + `measurement` + `specification_population` |
| p11 sources / citations | Migration script | `convert_sources.py` (exists) → `evidence_source` table |
| p18 categories | Rendering query | `SELECT DISTINCT substr(item_code,1,1) AS category FROM specification` |
| p25 spec sources (per-spec) | Rendering query | `SELECT es.* FROM evidence_source es JOIN cell_evidence_source ces ON ... WHERE ces.spec_id = ?` |
| **T3 (complex)** | | | |
| p06 room matrices (Part 6) | Migration script | `scripts/migrate/phase_rooms.py` → `room` + `room_specification` |
| p07 room matrices (Part 7) | Migration script | Same script, non-residential rooms |
| p08 conflict domains | Migration script | `convert_conflicts.py` (exists) → `conflict` table |
| p10 DAR register | Migration script | `scripts/migrate/phase_dar.py` → `dar_relevant`/`dar_note` columns |
| p12 case studies | Migration script | `scripts/migrate/phase_case_studies.py` → `case_study` table |
| **v2 additions** | | | |
| p_func_tasks | Redundant | Absorbed by `fdr_scenario` table + migration |
| p_standards_ext | Rendering query | `SELECT * FROM standard WHERE jurisdiction = ?` |
| p_eng_coord | Rendering query | `SELECT * FROM specification WHERE structural_backing_required = 1` |
| p_brief_builder | Rendering query | Complex query over spec + population + design_stage joins |
| **T4 (dependent)** | | | |
| p13 economics cost data | Migration script | `scripts/migrate/phase_economics.py` → `economics_entry` table |
| p14 grant programmes | Migration script | Same script, grant records |
| p15 throughlines | Migration script | `scripts/migrate/phase_throughlines.py` → `throughline` table |
| p16 doctrine/foundations | Migration script | `scripts/migrate/phase_foundations.py` → `doctrine` table |
| p17 BPC metadata | Redundant | Already migrated via `convert_bpc_metadata.py` |
| **T5 (join tables)** | | | |
| p19 spec-population | Redundant | Produced as byproduct of p09 specification migration |
| p20 spec-room | Redundant | Produced as byproduct of p06/p07 room migration |
| p21 spec-conflict | Rendering query | `SELECT cd.* FROM conflict_party cp JOIN conflict cd ON ... WHERE cp.entity_id = ?` |
| p22 spec-economics | Rendering query | `SELECT * FROM economics_entry WHERE spec_id = ?` |
| p23 pop-conflict | Rendering query | `SELECT * FROM conflict_party WHERE entity_type='population' AND entity_id = ?` |
| p24 spec-case-study | Rendering query | `SELECT cs.* FROM case_study_specification css JOIN case_study cs ON ... WHERE css.spec_id = ?` |

### 7.2 Migration script sequencing

Scripts execute in dependency order (matches D-0139 §5.1 phase order):

1. `phase_populations.py` — population table (no deps)
2. `phase_slugs.py` — slug table (no deps)
3. `phase_sources.py` — evidence_source table (no deps)
4. `phase_bpc.py` — bpc table (no deps)
5. `phase_specifications.py` — specification + measurement + spec_population (deps: population)
6. `phase_jv_appendix_a.py` — jurisdictional_value (deps: specification)
7. `phase_connections.py` — connection + endpoint (deps: specification, population)
8. `phase_conflicts.py` — conflict + conflict_party (deps: specification, population)
9. `phase_rooms.py` — room + room_specification (deps: specification)
10. `phase_case_studies.py` — case_study (deps: specification)
11. `phase_economics.py` — economics_entry (deps: specification)
12. `phase_throughlines.py` — throughline (deps: specification, population, conflict)
13. `phase_foundations.py` — doctrine (no deps, but authored content)

---

## 8. R2 status update

`references/website/schema/unified-data-schema.md` (R2) retains its role as the **display contract** — it defines what each page template needs to show. Its field-level JSON schemas are superseded by this reconciliation's DDL + rendering query specifications.

R2 should be updated to:
- Replace inline JSON schemas with references to R1 DDL tables
- Add rendering query specifications for computed fields
- Add the 14 page template query shapes (deferred to B3.3)
- Reflect DesignMode rename (universal/population/person instead of tier_0/tier_1/tier_2)

This update is a B3.3 deliverable (template specification), not B2.1.

---

## 9. Reconciliation decisions summary

| Decision | Resolution | Confidence |
|---|---|---|
| Where do measurement values live? | `measurement` table (normalized), not JSON on specification | High — enables multi-mode queries |
| Where do jurisdiction values live? | `jurisdictional_value` table (normalized) | High — enables master index rendering |
| Are population roles stored or computed? | Stored in `specification_population.role` column | High — authoring decision, not derivable |
| Are conflict domains stored or computed? | JSON column on specification (denormalized for speed) | Medium — could normalize to join table |
| Are evidence markers stored? | Computed at render time from evidence_state_record | High — derived from authoritative evidence state |
| Is curation_status a separate column? | Yes — distinct from `status` (lifecycle) | High — orthogonal concerns |
| Do we keep body_md on specification? | Yes — prose retained per D-0138 §5.6 | High — decided in B1 |
| Where do prototype ITEMS fields go? | 5 JSON columns on specification (Amendment 8) | High — content atoms, queried whole not by sub-field |
