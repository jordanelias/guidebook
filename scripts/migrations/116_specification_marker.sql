-- 116_specification_marker.sql
-- SCHEMA migration -- a determination carries the evidence marker of the sources it rests on
-- (plan Phase 3 specification; RULINGS R7, R39). The mission and tier-system section 5 say every
-- specification is marked (filled circle, half circle, empty circle) and that an unmarked one is an
-- error; no column held the marker, so none was ever written. `v_best_practice` carried a two-valued
-- `strength_band` computed from regulatory_stratum_only, which no reader used, and is redefined
-- without it: the marker has ONE home, `specifications.marker`, and the view reaches it through `*`.
--
--   marker  TEXT, two column CHECKs:
--     1. marker IS NULL OR (marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○'))
--        the vocabulary is the CHECK's (dbcore.check_values reads it), and a determination resting
--        only on the regulatory stratum can never be marked above the weak band (Option A, 2.3).
--     2. retired_at IS NOT NULL OR (state IN ('stated','provisional')) = (marker IS NOT NULL)
--        a live stated or provisional row carries a marker and a live pending or not_applicable row
--        carries none. Retired rows are history and are exempt.
--
-- ADD COLUMN rather than a table rebuild: the AUTOINCREMENT sequence, the lens CHECK of 065, the
-- inbound foreign keys, idx_spec_row_identity, trg_spec_retire_needs_reason and the other views stay
-- untouched. SQLite checks an added CHECK against the rows that exist; every row is retired, so both
-- hold. A live provisional row with no marker would have made the ALTER fail loudly.
--
-- ORDER: after every committed data migration, so no earlier INSERT meets the new CHECKs.
-- AFTER_DATA: 20261010002423

ALTER TABLE specifications ADD COLUMN marker TEXT
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○') AND (regulatory_stratum_only = 0 OR marker = '○')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL));

DROP VIEW v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0
      AND retired_at IS NULL;

PRAGMA user_version = 116;
