#!/usr/bin/env python3
"""
scripts/migrate/init_database.py — Create empty guidebook.db with DDL

Creates the SQLite database at data/db/guidebook.db with all tables
defined in architecture/schema-spec.md + D-0139 Amendment 1.

Usage:
    python3 scripts/migrate/init_database.py
    python3 scripts/migrate/init_database.py --force  # Recreate from scratch
"""

import os
import sys
import sqlite3
from pathlib import Path

DB_PATH = "data/db/guidebook.db"

DDL = """
-- ═══════════════════════════════════════════════════════════════
-- Guidebook Schema DDL — D-0139 + Amendment 1
-- Created by scripts/migrate/init_database.py
-- ═══════════════════════════════════════════════════════════════

-- ─── Core entities (D-0139 §2) ──────────────────────────────

CREATE TABLE IF NOT EXISTS specification (
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

  -- Amendment 1: Question mode
  question_heading             TEXT,
  question_summary             TEXT,

  -- Amendment 1: Display atoms
  summary                      TEXT,
  evidence_summary             TEXT,
  tier_2_note                  TEXT,

  -- Amendment 1: Authored prose
  why_md                       TEXT,
  schedule_md                  TEXT,

  -- Amendment 1: Diagrams
  diagram_svg                  TEXT,
  diagram_type                 TEXT CHECK (diagram_type IN ('plan','section','elevation','isometric','chart',NULL)),

  -- Amendment 1: DAR
  dar_relevant                 INTEGER DEFAULT 0,
  dar_note                     TEXT,

  -- Amendment 1: Engineering
  structural_backing_required  INTEGER DEFAULT 0,

  -- Amendment 1: Classification
  retrofit_category            TEXT CHECK (retrofit_category IN ('LOW-PLANNING','LOW-FIXTURE','MODERATE','HIGH','STRUCTURAL',NULL)),
  ot_evidence_basis            TEXT,
  curation_status              TEXT CHECK (curation_status IN ('automated','reviewed','opus_synthesized')) DEFAULT 'automated',

  -- Amendment 1: Migration tracking
  item_code                    TEXT,
  bpc_source_slug              TEXT,
  recommendation_strength      TEXT CHECK (recommendation_strength IN ('Strong','Conditional','Weak','Consensus',NULL)),
  percentile_basis             TEXT,

  -- Amendment 1: JSON content atoms
  conflict_domains             TEXT,
  failures_json                TEXT,
  install_notes_json           TEXT,
  detail_groups_json           TEXT,
  pop_reasons_json             TEXT,
  topics_json                  TEXT
);

CREATE INDEX IF NOT EXISTS idx_specification_parameter ON specification(parameter);
CREATE INDEX IF NOT EXISTS idx_specification_class ON specification(parameter_class);
CREATE INDEX IF NOT EXISTS idx_specification_status ON specification(status);
CREATE INDEX IF NOT EXISTS idx_specification_item_code ON specification(item_code);
CREATE INDEX IF NOT EXISTS idx_specification_dar ON specification(dar_relevant);
CREATE INDEX IF NOT EXISTS idx_specification_curation ON specification(curation_status);
CREATE INDEX IF NOT EXISTS idx_specification_bpc ON specification(bpc_source_slug);

-- Join tables for specification
CREATE TABLE IF NOT EXISTS specification_design_stage (
  spec_id          TEXT NOT NULL,
  design_stage     TEXT NOT NULL,
  PRIMARY KEY (spec_id, design_stage),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE TABLE IF NOT EXISTS specification_project_type (
  spec_id          TEXT NOT NULL,
  project_type     TEXT NOT NULL,
  PRIMARY KEY (spec_id, project_type),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE TABLE IF NOT EXISTS specification_population (
  spec_id          TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  role             TEXT NOT NULL CHECK (role IN ('primary','secondary','all')),
  PRIMARY KEY (spec_id, population_code),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX IF NOT EXISTS idx_spec_pop_role ON specification_population(role);

-- ─── Amendment 1: New tables ────────────────────────────────

CREATE TABLE IF NOT EXISTS measurement (
  measurement_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  design_mode      TEXT NOT NULL CHECK (design_mode IN ('universal','population_based','person_specific')),
  population_code  TEXT,
  value_type       TEXT NOT NULL CHECK (value_type IN ('fixed','range','minimum','maximum','categorical')),
  value_min        REAL,
  value_max        REAL,
  value_median     REAL,
  unit             TEXT,
  condition_text   TEXT,
  source_ref       TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code),
  CHECK (design_mode != 'population_based' OR population_code IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS idx_measurement_spec ON measurement(spec_id);
CREATE INDEX IF NOT EXISTS idx_measurement_mode ON measurement(design_mode);
CREATE INDEX IF NOT EXISTS idx_measurement_pop ON measurement(population_code);

CREATE TABLE IF NOT EXISTS jurisdictional_value (
  jv_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  jurisdiction     TEXT NOT NULL,
  standard_name    TEXT,
  clause_reference TEXT,
  value_text       TEXT,
  value_numeric    REAL,
  unit             TEXT,
  is_code_minimum  INTEGER DEFAULT 1,
  evidence_tier    INTEGER,
  notes            TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);
CREATE INDEX IF NOT EXISTS idx_jv_spec ON jurisdictional_value(spec_id);
CREATE INDEX IF NOT EXISTS idx_jv_jurisdiction ON jurisdictional_value(jurisdiction);
CREATE UNIQUE INDEX IF NOT EXISTS idx_jv_unique ON jurisdictional_value(spec_id, jurisdiction, standard_name, COALESCE(clause_reference,''));

CREATE TABLE IF NOT EXISTS performance_criterion (
  criterion_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id          TEXT NOT NULL,
  metric           TEXT NOT NULL,
  target           TEXT NOT NULL,
  measure          TEXT,
  population_code  TEXT,
  source_ref       TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
CREATE INDEX IF NOT EXISTS idx_pc_spec ON performance_criterion(spec_id);

-- ─── D-0139 §3: Missing entity types ───────────────────────

CREATE TABLE IF NOT EXISTS population (
  code                 TEXT PRIMARY KEY,
  parent_code          TEXT,
  label                TEXT NOT NULL,
  definition           TEXT NOT NULL,
  prevalence_band      TEXT,
  evidence_strength    TEXT,
  notes                TEXT,
  FOREIGN KEY (parent_code) REFERENCES population(code)
);
CREATE INDEX IF NOT EXISTS idx_population_parent ON population(parent_code);

CREATE VIEW IF NOT EXISTS population_resolved AS
WITH RECURSIVE pop_chain AS (
  SELECT code, parent_code, label, definition, prevalence_band, evidence_strength, notes, 0 AS depth
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

CREATE TABLE IF NOT EXISTS item (
  item_id              TEXT PRIMARY KEY,
  category             TEXT NOT NULL,
  name                 TEXT NOT NULL,
  description          TEXT,
  notes                TEXT
);

CREATE TABLE IF NOT EXISTS item_specification (
  item_id              TEXT NOT NULL,
  spec_id              TEXT NOT NULL,
  PRIMARY KEY (item_id, spec_id),
  FOREIGN KEY (item_id) REFERENCES item(item_id),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE TABLE IF NOT EXISTS conflict (
  conflict_id          TEXT PRIMARY KEY,
  conflict_type        TEXT NOT NULL CHECK (conflict_type IN
                         ('spec-vs-spec','spec-vs-population','population-vs-population')),
  description          TEXT NOT NULL,
  resolution_status    TEXT NOT NULL CHECK (resolution_status IN
                         ('OPEN','RESOLVED','DEFERRED','UNRESOLVABLE')),
  resolution_decision_id TEXT,
  notes                TEXT,
  FOREIGN KEY (resolution_decision_id) REFERENCES decision(decision_id)
);

CREATE TABLE IF NOT EXISTS conflict_party (
  conflict_id          TEXT NOT NULL,
  entity_type          TEXT NOT NULL CHECK (entity_type IN ('specification','population')),
  entity_id            TEXT NOT NULL,
  party_role           TEXT,
  PRIMARY KEY (conflict_id, entity_type, entity_id),
  FOREIGN KEY (conflict_id) REFERENCES conflict(conflict_id)
);

CREATE TABLE IF NOT EXISTS question (
  question_id          TEXT PRIMARY KEY,
  question_text        TEXT NOT NULL,
  applies_to_population TEXT,
  parameter_class      TEXT,
  design_stage         TEXT,
  status               TEXT NOT NULL CHECK (status IN ('DRAFT','ACTIVE','RETIRED')),
  created_at           TEXT NOT NULL,
  FOREIGN KEY (applies_to_population) REFERENCES population(code)
);
CREATE INDEX IF NOT EXISTS idx_question_population ON question(applies_to_population);
CREATE INDEX IF NOT EXISTS idx_question_class ON question(parameter_class);
CREATE INDEX IF NOT EXISTS idx_question_design_stage ON question(design_stage);

CREATE TABLE IF NOT EXISTS question_specification (
  question_id          TEXT NOT NULL,
  spec_id              TEXT NOT NULL,
  answer_role          TEXT,
  PRIMARY KEY (question_id, spec_id),
  FOREIGN KEY (question_id) REFERENCES question(question_id),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE TABLE IF NOT EXISTS fdr_scenario (
  scenario_id          TEXT PRIMARY KEY,
  scenario_type        TEXT NOT NULL,
  description          TEXT NOT NULL,
  affected_populations TEXT,
  notes                TEXT
);

CREATE TABLE IF NOT EXISTS fdr_scenario_population (
  scenario_id          TEXT NOT NULL,
  population_code      TEXT NOT NULL,
  PRIMARY KEY (scenario_id, population_code),
  FOREIGN KEY (scenario_id) REFERENCES fdr_scenario(scenario_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);

CREATE TABLE IF NOT EXISTS specialist_handoff (
  handoff_id           TEXT PRIMARY KEY,
  specialist_role      TEXT NOT NULL,
  triggering_condition TEXT NOT NULL,
  notes                TEXT
);

CREATE TABLE IF NOT EXISTS specialist_handoff_specification (
  handoff_id           TEXT NOT NULL,
  spec_id              TEXT NOT NULL,
  PRIMARY KEY (handoff_id, spec_id),
  FOREIGN KEY (handoff_id) REFERENCES specialist_handoff(handoff_id),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

-- ─── Existing entities from D-0139 §2 ──────────────────────

CREATE TABLE IF NOT EXISTS evidence_source (
  ref_id               TEXT PRIMARY KEY,
  short_ref            TEXT NOT NULL,
  full_citation        TEXT,
  evidence_type        TEXT NOT NULL,
  tier                 INTEGER CHECK (tier BETWEEN 1 AND 6),
  doi                  TEXT,
  url                  TEXT,
  language             TEXT DEFAULT 'EN',
  year                 INTEGER,
  verification_status  TEXT DEFAULT 'unverified',
  co1_provenance       TEXT,
  co1_source_type      TEXT,
  synthesis_attribution_required INTEGER,
  CHECK ((evidence_type = 'co1-collaborator') = (co1_provenance IS NOT NULL
         AND co1_source_type IS NOT NULL
         AND synthesis_attribution_required IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS connection (
  connection_id    TEXT PRIMARY KEY,
  slug             TEXT NOT NULL UNIQUE,
  title            TEXT NOT NULL,
  description      TEXT,
  created_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_connection_slug ON connection(slug);

CREATE TABLE IF NOT EXISTS connection_endpoint (
  connection_id    TEXT NOT NULL,
  entity_type      TEXT NOT NULL CHECK (entity_type IN
                     ('specification','population','source','bpc','decision','gap','question')),
  entity_id        TEXT NOT NULL,
  role             TEXT,
  PRIMARY KEY (connection_id, entity_type, entity_id),
  FOREIGN KEY (connection_id) REFERENCES connection(connection_id)
);
CREATE INDEX IF NOT EXISTS idx_connection_endpoint_entity ON connection_endpoint(entity_type, entity_id);

CREATE TABLE IF NOT EXISTS bpc (
  bpc_slug         TEXT PRIMARY KEY,
  title            TEXT NOT NULL,
  status           TEXT NOT NULL CHECK (status IN ('CLEAN','AMBIGUOUS','STUB','MERGED','SUPERSEDED')),
  merged_into      TEXT,
  population_primary TEXT,
  last_updated     TEXT,
  FOREIGN KEY (merged_into) REFERENCES bpc(bpc_slug)
);

-- ─── Evidence state (A6) ────────────────────────────────────

CREATE TABLE IF NOT EXISTS cell (
  cell_id          TEXT PRIMARY KEY,
  spec_id          TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  state            TEXT NOT NULL CHECK (state IN ('silent','stated','provisional','contested','not_applicable')),
  state_rationale  TEXT,
  convergence_status TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code),
  UNIQUE (spec_id, population_code)
);
CREATE INDEX IF NOT EXISTS idx_cell_spec ON cell(spec_id);
CREATE INDEX IF NOT EXISTS idx_cell_pop ON cell(population_code);

CREATE TABLE IF NOT EXISTS cell_evidence_source (
  cell_id          TEXT NOT NULL,
  ref_id           TEXT NOT NULL,
  PRIMARY KEY (cell_id, ref_id),
  FOREIGN KEY (cell_id) REFERENCES cell(cell_id),
  FOREIGN KEY (ref_id) REFERENCES evidence_source(ref_id)
);

-- ─── Schema metadata ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS _schema_version (
  version          TEXT PRIMARY KEY,
  applied_at       TEXT NOT NULL,
  description      TEXT
);

INSERT OR IGNORE INTO _schema_version (version, applied_at, description)
VALUES ('D-0139-A1', datetime('now'), 'D-0139 + Amendment 1 — full DDL init');
"""


def main():
    force = '--force' in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent
    db_path = repo_root / DB_PATH

    os.makedirs(db_path.parent, exist_ok=True)

    if db_path.exists():
        if force:
            os.remove(db_path)
            print(f"Removed existing {db_path}")
        else:
            print(f"Database already exists: {db_path}")
            print("Use --force to recreate from scratch")
            sys.exit(0)

    print(f"Creating database: {db_path}")
    conn = sqlite3.connect(str(db_path))
    conn.executescript(DDL)

    # Verify
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables created: {len(tables)}")
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
        print(f"  {t}: {count} rows")

    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
    views = [row[0] for row in cursor.fetchall()]
    print(f"Views created: {len(views)}")
    for v in views:
        print(f"  {v}")

    conn.close()
    print(f"\nDatabase ready: {db_path}")
    print(f"Schema version: D-0139-A1")


if __name__ == "__main__":
    main()
