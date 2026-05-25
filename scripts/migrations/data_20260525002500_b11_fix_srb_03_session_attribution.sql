-- data_20260525002500_b11_fix_srb_03_session_attribution.sql
-- Cosmetic fix: SRB-03 citation_mining row had created_by_session='session_test' due to
-- a stray test invocation during turn-11 debugging. Reset to the actual session.
-- Forward-only; no functional impact.

BEGIN TRANSACTION;

UPDATE citation_mining
   SET created_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'stair-ramp-threshold-biomechanics-accessibility'
   AND local_ref_id = 'SRB-03'
   AND created_by_session = 'session_test';

COMMIT;
