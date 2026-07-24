-- 034_slug_serves_axes.sql
-- SCHEMA migration — E2 of the 2026-07-21 ratification register (authorized under the
-- merge=ratify rule, 2026-07-24). Adds slugs.serves_axes: a JSON array of axis_codes
-- (e.g. '["AX-BAL"]') declaring which functional axes a research slug serves.
-- DDL only. Additive, nullable — touches no existing value. This UNBLOCKS E2 (the column
-- did not exist); the bulk 106-slug backfill is judgment work that depends on E3
-- (item_axis_links), since only one BPC currently carries an axis code. Populated
-- incrementally per-slug meanwhile (seed: the vestibular slug, in the paired data migration).
-- Forward-only; user_version -> 34 (renumbered from 033 to resolve collision with 033_search_executions from PR #62).
BEGIN TRANSACTION;
ALTER TABLE slugs ADD COLUMN serves_axes TEXT;  -- JSON array of axis_code, nullable
COMMIT;
