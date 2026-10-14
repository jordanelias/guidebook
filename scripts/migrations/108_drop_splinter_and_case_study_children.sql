-- 108_drop_splinter_and_case_study_children.sql
-- SCHEMA migration -- the empty population junctions and the case-study child tables are dropped
-- (plan step 1.3; LED-132, RULINGS R12 keeps `case_studies`).
--
-- WHY. LED-132 (owner, 2026-08-28): a determination attaches to a group of disabled people through
-- the four lens columns, never through a `population_*` link table. Five such "splinter" tables
-- survived the restructure; `probe_population_links` went with the item layer (migration 107) and
-- these remain. `case_study_outcomes` and `case_study_strategies` are children of `case_studies` that
-- nothing writes: an outcome or a strategy a source states is an extraction against a parameter
-- (R16), and the case study itself stays in `case_studies` (R12).
--
-- EVIDENCE (derived, 2026-10-14, before this migration; re-run rather than trust):
--   * every table below holds 0 rows:
--       select count(*) from <table>   -- each 0
--   * no table has a foreign key into any of them, and no view or trigger names them:
--       pragma foreign_key_list on every table; sqlite_master
--   * no data migration writes them:
--       grep -lE "(INSERT( OR [A-Z]+)? INTO|UPDATE|DELETE FROM) \"?<table>\"?[ (]" scripts/migrations/data_*.sql
--     finds nothing, so no AFTER_DATA marker is needed here.
--   * the two indexes on them (idx_cpl_pop, idx_epl_pop) go with their tables.
--
-- WHAT IS DROPPED: case_study_populations, citation_population_links, economics_entry_populations,
-- extraction_population_links, case_study_outcomes, case_study_strategies.

DROP TABLE case_study_populations;
DROP TABLE citation_population_links;
DROP TABLE economics_entry_populations;
DROP TABLE extraction_population_links;
DROP TABLE case_study_outcomes;
DROP TABLE case_study_strategies;

PRAGMA user_version = 108;
