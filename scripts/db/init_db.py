#!/usr/bin/env python3
"""
scripts/db/init_db.py — Create SQLite database from DDL.

Creates all tables from D-0139 Amendment 1 + Amendment 2.
Idempotent — drops and recreates all tables on each run.

Usage:
    python3 scripts/db/init_db.py                 # creates data/db/guidebook.db
    python3 scripts/db/init_db.py --path /tmp/test.db
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "db" / "guidebook.db"

DDL = """
-- ============================================================
-- Core specification tables (D-0139 + Amendment 1)
-- ============================================================

CREATE TABLE IF NOT EXISTS specification (
  spec_id              TEXT PRIMARY KEY,
  item_code            TEXT NOT NULL,
  title                TEXT NOT NULL,
  parameter            TEXT,
  value_type           TEXT,
  design_mode          TEXT,
  recommendation_strength TEXT DEFAULT 'UNSET',
  evidence_tier        INTEGER,
  universal_value      TEXT,
  population_value     TEXT,
  person_specific_note TEXT,
  question_heading     TEXT,
  question_summary     TEXT,
  summary              TEXT,
  evidence_summary     TEXT,
  why_md               TEXT,
  schedule_md          TEXT,
  diagram_svg          TEXT,
  diagram_type         TEXT,
  dar_relevant         INTEGER DEFAULT 0,
  dar_note             TEXT,
  structural_backing_required INTEGER DEFAULT 0,
  retrofit_category    TEXT,
  ot_evidence_basis    TEXT,
  curation_status      TEXT DEFAULT 'automated',
  conflict_domains     TEXT,
  failures_json        TEXT,
  install_notes_json   TEXT,
  detail_groups_json   TEXT,
  pop_reasons_json     TEXT,
  topics_json          TEXT,
  percentile_basis     TEXT,
  notes                TEXT,
  context_note         TEXT,
  bpc_source_slug      TEXT,
  status               TEXT DEFAULT 'active',
  created_at           TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_spec_item ON specification(item_code);
CREATE INDEX IF NOT EXISTS idx_spec_status ON specification(status);

CREATE TABLE IF NOT EXISTS measurement (
  measurement_id  INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id         TEXT NOT NULL,
  design_mode     TEXT NOT NULL,
  population_code TEXT,
  value_min       REAL,
  value_max       REAL,
  value_median    REAL,
  value_fixed     REAL,
  unit            TEXT,
  unit_display    TEXT,
  source_ref      TEXT,
  notes           TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE INDEX IF NOT EXISTS idx_meas_spec ON measurement(spec_id);

CREATE TABLE IF NOT EXISTS jurisdictional_value (
  jv_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id         TEXT NOT NULL,
  jurisdiction    TEXT NOT NULL,
  standard_name   TEXT,
  clause_ref      TEXT,
  value_text      TEXT,
  value_numeric   REAL,
  unit            TEXT,
  notes           TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE INDEX IF NOT EXISTS idx_jv_spec ON jurisdictional_value(spec_id);
CREATE INDEX IF NOT EXISTS idx_jv_jurisdiction ON jurisdictional_value(jurisdiction);

CREATE TABLE IF NOT EXISTS performance_criterion (
  criterion_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  spec_id         TEXT NOT NULL,
  description     TEXT NOT NULL,
  test_method     TEXT,
  pass_threshold  TEXT,
  notes           TEXT,
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id)
);

CREATE TABLE IF NOT EXISTS population (
  code            TEXT PRIMARY KEY,
  label           TEXT NOT NULL,
  functional_profile TEXT,
  co1_status      TEXT,
  co1_gap_note    TEXT,
  evidence_confidence TEXT,
  co_occurrence_notes TEXT,
  status          TEXT DEFAULT 'active',
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS specification_population (
  spec_id         TEXT NOT NULL,
  population_code TEXT NOT NULL,
  role            TEXT DEFAULT 'primary',
  PRIMARY KEY (spec_id, population_code),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);

CREATE TABLE IF NOT EXISTS conflict (
  conflict_id     TEXT PRIMARY KEY,
  conflict_label  TEXT NOT NULL,
  domain          TEXT,
  population_a    TEXT,
  population_b    TEXT,
  governing_principle TEXT,
  resolution_status TEXT,
  resolution_description TEXT,
  strategy_codes  TEXT,
  decision_tree   TEXT,
  unresolvable_residual TEXT,
  mode_s_trigger  TEXT,
  mitigation      TEXT,
  specifications_involved TEXT,
  citations       TEXT,
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS evidence_source (
  ref_id          TEXT PRIMARY KEY,
  authors         TEXT,
  year            INTEGER,
  title           TEXT NOT NULL,
  journal         TEXT,
  doi             TEXT,
  url             TEXT,
  evidence_tier   INTEGER,
  jurisdiction    TEXT,
  co1_status      INTEGER DEFAULT 0,
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS specification_source (
  spec_id         TEXT NOT NULL,
  ref_id          TEXT NOT NULL,
  role            TEXT DEFAULT 'supporting',
  PRIMARY KEY (spec_id, ref_id),
  FOREIGN KEY (spec_id) REFERENCES specification(spec_id),
  FOREIGN KEY (ref_id) REFERENCES evidence_source(ref_id)
);

CREATE TABLE IF NOT EXISTS connection_endpoint (
  connection_id   TEXT NOT NULL,
  spec_id         TEXT NOT NULL,
  target_spec_id  TEXT,
  target_item_code TEXT,
  connection_type TEXT,
  description     TEXT,
  PRIMARY KEY (connection_id, spec_id)
);

-- ============================================================
-- Amendment 2 tables (B3.2)
-- ============================================================

CREATE TABLE IF NOT EXISTS doctrine (
  doctrine_id     TEXT PRIMARY KEY,
  slug            TEXT NOT NULL UNIQUE,
  title           TEXT NOT NULL,
  doctrine_group  TEXT NOT NULL,
  statement       TEXT NOT NULL,
  implications    TEXT,
  body_md         TEXT,
  part_section    TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS doctrine_specification (
  doctrine_id     TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  PRIMARY KEY (doctrine_id, item_code)
);

CREATE TABLE IF NOT EXISTS room (
  room_id         TEXT PRIMARY KEY,
  room_label      TEXT NOT NULL,
  building_type   TEXT NOT NULL,
  part_source     INTEGER NOT NULL,
  section         TEXT,
  criticality_note TEXT,
  evidence_density TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS room_item (
  room_id         TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  design_stage    TEXT,
  must_appear_on  TEXT,
  notes           TEXT,
  PRIMARY KEY (room_id, item_code)
);

CREATE TABLE IF NOT EXISTS room_item_population (
  room_id         TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  population_code TEXT NOT NULL,
  applicability   TEXT,
  PRIMARY KEY (room_id, item_code, population_code)
);

CREATE TABLE IF NOT EXISTS room_dar_provision (
  provision_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id         TEXT NOT NULL,
  description     TEXT NOT NULL,
  construction_stage TEXT,
  drawing_reference TEXT,
  notes           TEXT
);

CREATE TABLE IF NOT EXISTS room_conflict (
  conflict_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id         TEXT NOT NULL,
  description     TEXT NOT NULL,
  resolution      TEXT,
  conflict_domain TEXT
);

CREATE TABLE IF NOT EXISTS specialist (
  specialist_id   TEXT PRIMARY KEY,
  role            TEXT NOT NULL UNIQUE,
  role_label      TEXT NOT NULL,
  part_section    TEXT,
  role_description TEXT NOT NULL,
  assessment_format TEXT,
  co_design_notes TEXT,
  guidebook_relationship TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS specialist_trigger (
  trigger_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  specialist_id   TEXT NOT NULL,
  trigger_text    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS specialist_stage_scope (
  scope_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  specialist_id   TEXT NOT NULL,
  stage           TEXT NOT NULL,
  scope_text      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS specialist_specification (
  specialist_id   TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  PRIMARY KEY (specialist_id, item_code)
);

CREATE TABLE IF NOT EXISTS specialist_population (
  specialist_id   TEXT NOT NULL,
  population_code TEXT NOT NULL,
  PRIMARY KEY (specialist_id, population_code)
);

CREATE TABLE IF NOT EXISTS economics_entry (
  entry_id        TEXT PRIMARY KEY,
  pillar          TEXT NOT NULL,
  entry_type      TEXT NOT NULL,
  source          TEXT NOT NULL,
  jurisdiction    TEXT,
  finding         TEXT NOT NULL,
  study_design    TEXT,
  sample          TEXT,
  value_numeric   REAL,
  value_unit      TEXT,
  currency        TEXT,
  bcr             TEXT,
  evidence_tier   INTEGER,
  confidence      TEXT,
  year            INTEGER,
  journal         TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS case_study (
  case_study_id   TEXT PRIMARY KEY,
  slug            TEXT NOT NULL UNIQUE,
  title           TEXT NOT NULL,
  building_type   TEXT NOT NULL,
  location        TEXT NOT NULL,
  architect       TEXT,
  year            INTEGER,
  setting         TEXT,
  population_description TEXT,
  evidence_quality_tier INTEGER,
  cost_data       TEXT,
  cost_data_quality TEXT,
  part_section    TEXT,
  limitations     TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS case_study_population (
  case_study_id   TEXT NOT NULL,
  population_code TEXT NOT NULL,
  PRIMARY KEY (case_study_id, population_code)
);

CREATE TABLE IF NOT EXISTS case_study_specification (
  case_study_id   TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  PRIMARY KEY (case_study_id, item_code)
);

CREATE TABLE IF NOT EXISTS throughline (
  throughline_id  TEXT PRIMARY KEY,
  title           TEXT NOT NULL,
  slug            TEXT,
  description     TEXT NOT NULL,
  implications    TEXT,
  body_md         TEXT,
  category        TEXT,
  status          TEXT DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  modified_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS throughline_specification (
  throughline_id  TEXT NOT NULL,
  item_code       TEXT NOT NULL,
  description     TEXT,
  PRIMARY KEY (throughline_id, item_code)
);

-- ============================================================
-- Schema version
-- ============================================================

CREATE TABLE IF NOT EXISTS schema_version (
  version         INTEGER PRIMARY KEY,
  applied_at      TEXT NOT NULL DEFAULT (datetime('now')),
  description     TEXT
);

INSERT OR IGNORE INTO schema_version (version, description) VALUES
  (1, 'D-0139 + Amendment 1 + Amendment 2: full schema');
"""


def init_db(db_path: Path):
    """Create the SQLite database with all tables."""
    os.makedirs(db_path.parent, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.executescript(DDL)
    conn.commit()

    # Verify
    cursor = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
    table_count = cursor.fetchone()[0]

    cursor = conn.execute("SELECT version, description FROM schema_version")
    version = cursor.fetchone()

    conn.close()

    print(f"Database created: {db_path}")
    print(f"Tables: {table_count}")
    print(f"Schema version: {version[0]} — {version[1]}")


def main():
    db_path = DEFAULT_DB
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--path" and i + 2 < len(sys.argv):
            db_path = Path(sys.argv[i + 2])

    init_db(db_path)


if __name__ == "__main__":
    main()
