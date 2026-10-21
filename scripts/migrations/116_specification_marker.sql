-- 116_specification_marker.sql
-- SCHEMA migration -- a determination carries its evidence marker (plan Phase 3 specification;
-- RULINGS R7, R39; COMPARISON P18). The marker is the band of the evidence a determination rests
-- on (tier-system section 5: full, partial, weak), computed by assess_cell.determine from
-- schemas.tier_derivation.band and floor_mean and stored once, here. Before this file nothing
-- computed or stored it: EvidenceMarker had no reader, and v_best_practice offered a second,
-- two-valued band (strength_band) that no code read.
--
-- ONE COLUMN, ALTER TABLE ... ADD COLUMN, NOT A REBUILD: the AUTOINCREMENT sequence, 065's lens
-- CHECK, the inbound foreign keys, idx_spec_row_identity, trg_spec_retire_needs_reason and the views
-- that read specifications stay untouched. Two column CHECKs, each naming sibling columns:
--
--   (1) marker is a glyph of the vocabulary, and a determination resting only on the regulatory
--       stratum is never above weak. The glyphs are EvidenceMarker's values; dbcore.check_values
--       reads them from this CHECK.
--   (2) a live stated or provisional determination carries a marker, and a pending,
--       not_applicable or retired row does not have to. A retired row is exempt: the eight rows
--       written before this file are all retired, and SQLite checks an added CHECK against
--       existing rows.
--
-- WHAT THE CHECK CANNOT HOLD: a proxy determination (rests_on_proxy_inference) is weak unless a
-- confirming study reaches a governing extraction (R39). Confirmation lives in extraction_relations,
-- and a CHECK cannot read another table, so that rule is the engine's alone.
--
-- v_best_practice is redefined without strength_band, which marker now supersedes; SELECT * carries
-- the new column. Nothing else reads the view: re-derive with
--   python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from sqlite_master where sql like '%v_best_practice%' and name<>'v_best_practice'\").fetchall())"
--
-- AFTER_DATA: 20261016003719 -- the latest committed data migration at the time of writing. The
-- marker is chronology, not load: 095's marker already places this file after every specifications
-- write.

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
