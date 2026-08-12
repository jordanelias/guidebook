-- data_20260523003000_drop_v1_legacy.sql
-- Drop evidence_sources_v1_legacy. Schema cutover from v1 to v2 is complete (since 012_baseline_2026-05-15.sql).
-- The legacy table held a denormalized 24-column snapshot of v2's 83-column data; the cutover window has closed.
-- Audit script test_db_integrity.py already handles a dropped legacy table — C05/D02 auto-skip via sqlite_master existence check.
-- Per owner directive 2026-05-23.

BEGIN TRANSACTION;

DROP TABLE IF EXISTS evidence_sources_v1_legacy;

COMMIT;
