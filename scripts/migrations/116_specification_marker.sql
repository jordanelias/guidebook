-- 116_specification_marker.sql
-- SCHEMA migration -- a determination carries its evidence marker (plan Phase 3 specification;
-- RULINGS R7, R39; COMPARISON P18): the tier-system section 5 band of the evidence it rests on
-- (full, partial, weak), computed by assess_cell.determine from schemas.tier_derivation.band and
-- floor_mean and stored once, here.
--
-- ONE COLUMN, ALTER TABLE ... ADD COLUMN, NOT A REBUILD: the AUTOINCREMENT sequence, 065's lens
-- CHECK, the inbound foreign keys, idx_spec_row_identity, trg_spec_retire_needs_reason and the views
-- that read specifications stay untouched. Two column CHECKs, each naming sibling columns:
--
--   (1) marker is a glyph of the vocabulary (dbcore.check_values reads it from here), and a
--       determination resting only on the regulatory stratum is never above weak.
--   (2) a live stated or provisional determination carries a marker; a pending, not_applicable or
--       retired row need not. SQLite checks an added CHECK against existing rows, so the ALTER
--       fails loudly if a live stated or provisional row exists (re-derive: select count(*) from
--       specifications where retired_at is null).
--
-- The proxy rule (weak unless a confirming study reaches a governing extraction, R39) and the
-- cache caveat (derivation_sha does not hash extraction_relations) are the engine's alone, because
-- a CHECK cannot read another table: see determine() in scripts/assess/assess_cell.py.
--
-- v_best_practice is redefined without strength_band, which marker supersedes; SELECT * carries the
-- new column. The reader is render step 3.R (plan Phase 3), which shows the marker beside
-- has_unverified_sources; until it is built nothing reads the column but the CHECKs, and no other
-- object reads the view (sqlite_master). A determination without its marker would be an error to
-- the reader (mission: "Unmarked = error"), which is what the column exists to prevent.
--
-- The marker below is chronology, not load: 095's already places this file after every
-- specifications write. It sits alone on its line because migrate_db's pattern needs it so.
-- AFTER_DATA: 20261016003719

ALTER TABLE specifications ADD COLUMN marker TEXT
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker = '○')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL));

DROP VIEW v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0
      AND retired_at IS NULL;

PRAGMA user_version = 116;
