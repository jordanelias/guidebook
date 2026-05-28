-- 020_value_tables_setting_column.sql
-- Schema migration: separates setting (space type / context) from population
-- (disability code) across the three value-bearing tables.
--
-- BACKGROUND. Per the project's disability-centric framing (locked
-- 2026-05-11), the `population` field must hold a canonical disability
-- population code from the populations table (e.g. ADHD, AUT, DEAF, MOB,
-- NDV, VIS, plus 'ALL' for universal applicability). Pre-this-migration,
-- the population field on reasoning_doc_citations and spec_value_probes
-- was free text that conflated population with setting (e.g. "general
-- (primary classroom)", "DEAF / hearing-impaired (specially-resourced
-- provision)").
--
-- This migration adds a sibling `setting` column to:
--   - reasoning_doc_citations
--   - spec_value_probes
--   - source_value_extractions
-- so context like classroom type, provision type, or activity context
-- has a structural home distinct from population identity.
--
-- A companion data migration (data_*_population_setting_split.sql)
-- migrates the 7 drifted rdc rows + 1 drifted svp row into the new
-- column. Reads only the affected rows; no entity additions.
--
-- Schema-only, additive, nullable. No CHECK constraint here -- a future
-- audit script will validate population values against the populations
-- table once the existing data is cleaned.

BEGIN;

ALTER TABLE reasoning_doc_citations ADD COLUMN setting TEXT;
ALTER TABLE spec_value_probes ADD COLUMN setting TEXT;
ALTER TABLE source_value_extractions ADD COLUMN setting TEXT;

COMMIT;
