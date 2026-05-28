-- 021_value_claim_population_junctions.sql
-- Schema migration: FK-enforced, multi-valued population membership for the
-- three value-claim tables, replacing comma-separated free-text population.
--
-- BACKGROUND. The project already models population membership relationally
-- via item_population_links (item_code <-> population_code, FK-enforced, 361
-- rows) and links evidence to populations via evidence_population_match. The
-- three value-claim tables, however, stored population as free text:
--   reasoning_doc_citations.population   TEXT  (e.g. 'NDV,AUT')
--   spec_value_probes.population          TEXT  (e.g. 'AUT, PCS, DEM, MH, PAIN, OFS')
--   source_value_extractions.population_code TEXT (single FK, cannot hold compounds)
-- This conflated multi-valued membership into a string, made population
-- validity un-enforceable at the DB level, and left drift detection to the
-- UI render layer only.
--
-- This migration adds three junction tables mirroring item_population_links:
--   citation_population_links     (citation_id   <-> population_code)
--   probe_population_links        (probe_id       <-> population_code)
--   extraction_population_links   (extraction_id  <-> population_code)
-- Each FK-references populations(population_code), so every population value
-- is structurally constrained to the canonical 22-code taxonomy. Compound
-- populations become first-class multi-row sets.
--
-- The scalar population / population_code columns on the parent tables are
-- RETAINED but DEPRECATED: audit scripts still read them, so they are kept in
-- sync (denormalized) as a transition convenience. A companion Level-2 audit
-- (scripts/audit/population_integrity_audit.py) enforces scalar<->junction
-- consistency. Dropping the scalar columns is deferred until a caller-sweep
-- per architecture <migration_and_growth>.
--
-- A companion data migration (data_*_populate_population_junctions.sql)
-- back-fills the junctions from current scalar values.
--
-- Schema-only, additive. PRAGMA foreign_keys governs enforcement at runtime;
-- CI db_integrity runs PRAGMA foreign_key_check.

BEGIN;

CREATE TABLE citation_population_links (
  citation_id        TEXT NOT NULL,
  population_code    TEXT NOT NULL,
  note               TEXT,
  created_at         TEXT,
  created_by_session TEXT,
  PRIMARY KEY (citation_id, population_code),
  FOREIGN KEY (citation_id) REFERENCES reasoning_doc_citations(citation_id),
  FOREIGN KEY (population_code) REFERENCES populations(population_code)
);

CREATE TABLE probe_population_links (
  probe_id           TEXT NOT NULL,
  population_code    TEXT NOT NULL,
  note               TEXT,
  created_at         TEXT,
  created_by_session TEXT,
  PRIMARY KEY (probe_id, population_code),
  FOREIGN KEY (probe_id) REFERENCES spec_value_probes(probe_id),
  FOREIGN KEY (population_code) REFERENCES populations(population_code)
);

CREATE TABLE extraction_population_links (
  extraction_id      INTEGER NOT NULL,
  population_code    TEXT NOT NULL,
  note               TEXT,
  created_at         TEXT,
  created_by_session TEXT,
  PRIMARY KEY (extraction_id, population_code),
  FOREIGN KEY (extraction_id) REFERENCES source_value_extractions(extraction_id),
  FOREIGN KEY (population_code) REFERENCES populations(population_code)
);

CREATE INDEX idx_cpl_pop ON citation_population_links(population_code);
CREATE INDEX idx_ppl_pop ON probe_population_links(population_code);
CREATE INDEX idx_epl_pop ON extraction_population_links(population_code);

COMMIT;
