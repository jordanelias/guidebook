-- 033_search_executions.sql
-- Schema migration (Phase 0b, coverage-loop substrate): the single logged-search
-- event table + derived coverage views. Implements search-coverage-completion-workplan
-- §2.2 and coverage-completion-loop-methodology §4. Per DR-2026-07-24-search-executions-substrate
-- (D-SCHEMA / DG-REVIEW, ratified by owner 2026-07-24 "Ratify all"). Doctrine SHA 0f2f525.
--
-- One row = one executed search. Coverage is DERIVED from this log (v_coverage_*), never
-- hand-written. STRICT + CHECK + json_valid, reusing the established pattern from
-- item_population_links / spec_value_probes / evidence_cell_state. executed_at is an explicit
-- ISO string (NOT DEFAULT datetime('now')) so rebuild is byte-deterministic. Legacy
-- search_coverage / search_languages are NOT dropped — frozen read-only historical artifacts,
-- superseded by the views but preserved (redirect-stub discipline).
--
-- Schema-only, additive; ships empty. The runner sets PRAGMA user_version to 33.

BEGIN;

CREATE TABLE search_executions (
  exec_id              INTEGER PRIMARY KEY,
  slug                 TEXT NOT NULL REFERENCES slugs(slug),
  jurisdiction         TEXT,                 -- NULL = jurisdiction-agnostic search
  language             TEXT NOT NULL,        -- ISO; one of the 19 research languages
  -- hierarchy branch the search TARGETED (diffable against what was FOUND):
  target_tier          INTEGER CHECK (target_tier IS NULL OR target_tier BETWEEN 1 AND 6),
  target_evidence_type TEXT CHECK (target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  target_scope         TEXT CHECK (target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')),
  -- the verbatim, replayable query:
  query_text           TEXT NOT NULL,
  terms_used           TEXT,                 -- JSON array of term ids
  engine               TEXT NOT NULL,        -- pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
  -- depth as real method, not booleans:
  depth_method         TEXT NOT NULL CHECK (depth_method IN ('scoping','systematic')),
  mining_direction     TEXT CHECK (mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')),
  -- yield:
  results_found        INTEGER NOT NULL DEFAULT 0,
  results_screened     INTEGER NOT NULL DEFAULT 0,
  results_admitted     INTEGER NOT NULL DEFAULT 0,
  saturation_signal    TEXT CHECK (saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')),
  admitted_ref_ids     TEXT,                 -- JSON array of evidence_sources.ref_id
  deferred_reason      TEXT,                 -- non-NULL => deliberate no-search for this cell
  backfill             INTEGER NOT NULL DEFAULT 0 CHECK (backfill IN (0,1)),
  session              TEXT NOT NULL,
  executed_at          TEXT NOT NULL,        -- explicit ISO ts (deterministic under rebuild)
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids))
) STRICT;

CREATE INDEX ix_se_cell   ON search_executions(slug, jurisdiction, language);
CREATE INDEX ix_se_branch ON search_executions(target_tier, target_evidence_type, target_scope);

-- Derived coverage — replaces the hand-kept grids (which are frozen read-only, not dropped):
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, jurisdiction;

CREATE VIEW v_coverage_language AS
SELECT slug, language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, language;

CREATE VIEW v_coverage_branch AS
SELECT slug, jurisdiction, target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5;

COMMIT;
