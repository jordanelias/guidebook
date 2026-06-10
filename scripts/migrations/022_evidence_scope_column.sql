-- 022_evidence_scope_column.sql
-- Schema migration: add `scope` to evidence_sources so that tier becomes a
-- function of (evidence_type, scope) rather than a hand-set integer (closes R6).
--
-- BACKGROUND. Per the ratified evidence hierarchy (doctrine SHA 3da73bd;
-- decisions D-A, D-D, D-E) two evidence types span more than one tier and so
-- cannot be tiered from evidence_type alone:
--   - clinical:    high_control  -> Tier 1 (intervention / RCT / biomechanical /
--                                           sensory threshold; D-E admits
--                                           directly-relevant high-control
--                                           non-OT primary research at T1)
--                  lower_control -> Tier 3 (cross-sectional / observational /
--                                           qualitative / single-centre)
--   - standard_eb: national      -> Tier 2 (named-org / national EB standard)
--                  international  -> Tier 4 (international standard: ISO/IEC/EN)
-- The other six types are tier-determined by evidence_type alone and carry the
-- sentinel scope 'intrinsic' (co1->1, co2->2, sr_meta->2, grey->3,
-- national_fw->5, code->6).
--
-- The canonical (evidence_type, scope) -> tier map lives in
-- schemas/tier_derivation.py. A companion data migration
-- (data_*_backfill_evidence_scope.sql) backfills scope from each row's
-- already-consistent stored tier; rows whose (evidence_type, tier) pair is not
-- on the ratified ladder are left scope NULL and are the Stage 2.5
-- tier-consistency sweep targets.
--
-- Schema-only, additive, nullable. The CHECK admits NULL (existing rows pass;
-- the backfill fills the consistent ones) and constrains non-NULL values to the
-- five scope tokens. The runner sets PRAGMA user_version to 22 after applying.

BEGIN;

ALTER TABLE evidence_sources
  ADD COLUMN scope TEXT
  CHECK (scope IS NULL OR scope IN (
    'high_control', 'lower_control', 'national', 'international', 'intrinsic'
  ));

COMMIT;
