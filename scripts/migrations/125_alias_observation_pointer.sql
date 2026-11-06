-- 125_alias_observation_pointer.sql
-- SCHEMA migration -- a source-attested alias POINTS at the observation it came from.
--
-- Until now an alias's provenance was a substring of `notes` ("source-attested"), which
-- alias_provenance_audit read as text: any row whose free text contained the marker passed, and
-- the phrase, its quote and its source were copied into prose instead of reached by pointer
-- (CLAUDE.md rule 5; the plan scratchpad/session_2026-11-06-base-vocabulary-review/
-- base-population-plan.md, A3 and A17). The observation (observed_terms) already holds the phrase,
-- its language, locator and verbatim quote, and its ref_id reaches the source and so its
-- jurisdiction.
--
-- ONE NULLABLE COLUMN, ALTER TABLE ... ADD COLUMN: NULL means "not attested by an observation"
-- (model-generated, curated, or recorded before the convention), which is what 2382 rows are.
-- `db.py add-alias` writes the pointer and may attach it to a row already held; the audit reads
-- the pointer. Nothing is backfilled: no existing row is attested by an observation.
-- Readers of term_aliases (re-derive with grep and sqlite_master): db.py, the audit above,
-- generate/search-query code that selects named columns. No view names the table.
-- AFTER_DATA: 20261106053823

ALTER TABLE term_aliases ADD COLUMN observation_id INTEGER REFERENCES observed_terms(observation_id);

PRAGMA user_version = 125;
