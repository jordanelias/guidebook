-- 109_drop_axes.sql
-- SCHEMA migration -- the axes layer is retired as one act (plan step 1.4; RULINGS R3 and R35, DRS-024).
--
-- THE OWNER'S REASON. "Axes" is a coined term the owner ruled bad and retired (2026-08-18, "standing
-- decisions, do not relitigate"; again 2026-08-24, "I don't want axis to be used"; 2026-09-13, "AX-"
-- for an ICF code must never exist). ICF codes with their names replace it, and `population_icf_links`
-- is the mechanical re-derivation of `population_axis_map` (WRK-181). DR-2026-08-24 section R8 required
-- the retirement to be one act with a full caller sweep, never piecemeal: this migration is the schema
-- half and the same commit carries the sweep.
--
-- R3 MARKER (LED-169 ACTION (4); this migration destroys rows, and the departure is recorded here).
-- Rows destroyed, measured 2026-10-14 before the migration (re-run rather than trust):
--     select count(*) from axes;                  -- 17
--     select count(*) from access_need_axis_map;  -- 21
--     select count(*) from population_axis_map;   -- 53
--     select slug, serves_axes from slugs where serves_axes is not null;
--                                                  -- 1 row: vestibular-balance-built-environment, ["AX-BAL"]
--     select count(*) from situations;             -- 0
-- All of them are reproduced by `migrate_db.py --rebuild` (057_baseline and the data migrations replay
-- them before this migration), so nothing here is provenance the project cannot reconstruct.
--
-- NO DATA MIGRATION WRITES THESE OBJECTS (derived):
--     grep -nE "(INSERT( OR [A-Z]+)? INTO|UPDATE|DELETE FROM) \"?(axes|access_need_axis_map|population_axis_map|situations|slugs)\"?[ (]" scripts/migrations/data_*.sql
--   finds nothing; the value ["AX-BAL"] comes from 057_baseline. The marker below is the boundary 092-095
--   already set, restated so the ordering R3 requires is declared here and does not depend on inheriting it:
--   it is later than data_20260902220357, the newest data migration that names AX- strings.
--
-- DEPENDENCIES (derived from sqlite_master and pragma foreign_key_list):
--   * the only inbound foreign keys are access_need_axis_map.axis_code and population_axis_map.axis_code
--     into axes, so the two maps are dropped first;
--   * `situations` has 0 rows and no inbound key; the word appears in access_needs.absorbs only inside
--     a comment;
--   * slugs.serves_axes is the last column, outside every index, CHECK, view and trigger, so
--     ALTER TABLE ... DROP COLUMN (SQLite 3.35 or later; the runner is 3.45.1) applies directly.
--
-- AFTER_DATA: 20260920060857

DROP TABLE access_need_axis_map;
DROP TABLE population_axis_map;
DROP TABLE axes;
DROP TABLE situations;
ALTER TABLE slugs DROP COLUMN serves_axes;

PRAGMA user_version = 109;
