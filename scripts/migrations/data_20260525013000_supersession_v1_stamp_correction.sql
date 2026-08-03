-- data_20260525013000_supersession_v1_stamp_correction.sql
-- Migration 015 added bpc_metadata.closure_definition_version with DEFAULT 'v1' which
-- inadvertently stamped 75 unclosed slugs with the v1 closure marker. Closure-definition-
-- version is only meaningful for closed slugs. This migration NULLs out the marker on
-- unclosed slugs (citation_mining_complete = 0) and confirms v1 on the 6 actually-closed slugs.
--
-- The schema CHECK constraint on closure_definition_version (CHECK IN ('v1','v2')) would
-- block NULL — so this migration also relaxes the CHECK to allow NULL.

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Relax the CHECK constraint to allow NULL on unclosed slugs.
-- SQLite can't ALTER a CHECK in place; rebuild the column.
-- Strategy: add a new column with the relaxed constraint, copy values, drop old, rename.

ALTER TABLE bpc_metadata ADD COLUMN closure_definition_version_v2 TEXT
    CHECK(closure_definition_version_v2 IS NULL OR closure_definition_version_v2 IN ('v1', 'v2'));

-- Copy only meaningful values: NULL for unclosed slugs, v1 for closed ones.
UPDATE bpc_metadata
   SET closure_definition_version_v2 = CASE
        WHEN citation_mining_complete = 1 THEN 'v1'
        ELSE NULL
       END;

-- Drop the old column and rename the new one. SQLite ≥ 3.35 supports DROP COLUMN.
ALTER TABLE bpc_metadata DROP COLUMN closure_definition_version;
ALTER TABLE bpc_metadata RENAME COLUMN closure_definition_version_v2 TO closure_definition_version;

COMMIT;
