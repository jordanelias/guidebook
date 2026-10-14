-- 111_drop_empty_orphan_tables.sql
-- SCHEMA migration -- four empty tables with no foreign key and no view are dropped (plan step 1.9;
-- RULINGS R22 for bpc_metadata, R46 for the coverage grids).
--
-- WHAT IS DROPPED: reference_stubs, search_coverage, search_languages, bpc_metadata.
--
-- EVIDENCE (derived, 2026-10-14, before this migration; re-run rather than trust):
--   * every table holds 0 rows:  select count(*) from <table>
--   * no table has a foreign key into any of them, and no view or trigger names them; the only
--     dependents are the two indexes on reference_stubs, which go with it:
--       pragma foreign_key_list on every table; sqlite_master
--   * data migrations that write them:
--       grep -lE "(INSERT( OR [A-Z]+)? INTO|UPDATE|DELETE FROM) \"?<table>\"?[ (]" scripts/migrations/data_*.sql
--     finds only data_20260823223839 (reference_stubs: it inserts 531 rows and deletes them again).
--     It precedes 095's AFTER_DATA marker, which every later schema migration inherits, so a rebuild
--     replays it before this migration and then drops the empty table; no marker is needed here.
--
-- THE COVERAGE GRIDS (search_coverage, search_languages) were frozen when search_executions became the
-- log and v_coverage_* the derived views; nothing has written them since. bpc_metadata is the BPC
-- reasoning-document layer's state table (R22); external_root_registry is NOT dropped, three views
-- read it.

DROP TABLE reference_stubs;
DROP TABLE search_coverage;
DROP TABLE search_languages;
DROP TABLE bpc_metadata;

PRAGMA user_version = 111;
