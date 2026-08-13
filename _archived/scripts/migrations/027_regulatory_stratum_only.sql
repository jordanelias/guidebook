-- 027_regulatory_stratum_only.sql
-- Per DR-2026-07-12-evidence-architecture-unification (ACCEPTED 2026-07-13,
-- ratification record decisions/RATIFICATION-RECORD-2026-07-13.md), item G1b
-- execution item 6: the durable regulatory-stratum flag, extending migration
-- 026's code_floor_only (T6-only) to the full T4-6-only case, and the
-- v_best_practice exclusion that closes the convergence-laundering channel
-- at the view layer (adversarial-review finding 1 made this exclusion
-- marker-based and artifact-shipped as an interim; this is the durable form).
--
-- The view excludes BOTH the column and the tier_basis marker: the column is
-- authoritative going forward; the marker guard keeps the exclusion correct
-- for any row written by pre-027 tooling before its flag backfill runs
-- (data_20260713000000 backfills the flag from the marker).

ALTER TABLE evidence_cell_state
    ADD COLUMN regulatory_stratum_only INTEGER NOT NULL DEFAULT 0
        CHECK (regulatory_stratum_only IN (0, 1));

DROP VIEW IF EXISTS v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT * FROM evidence_cell_state
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0
      AND regulatory_stratum_only = 0
      AND (tier_basis IS NULL OR tier_basis NOT LIKE '%(regulatory_stratum_only)');

-- weighting_profile carries the audience emphasis profiles; table created by 026.
-- Seed rows are data, not schema: data_20260713000100_weighting-profile-seed.sql.
