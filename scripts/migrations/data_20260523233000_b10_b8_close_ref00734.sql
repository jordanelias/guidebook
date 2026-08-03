-- data_20260523233000_b10_b8_close_ref00734.sql
-- B.10 / B.8 closure: set synthesis_attribution_required = 1 for the one co1 row
-- that still lacks the flag (REF-00734 Tibble 2005 — UK DWP review of extra costs of disability).
-- After this migration: 30/30 co1 rows have synthesis_attribution_required = 1.
-- Phase B item B.10 satisfied; B.8 six-field co1 set complete.
-- Forward-only; idempotent via WHERE clause.

BEGIN TRANSACTION;

UPDATE evidence_sources
   SET synthesis_attribution_required = 1
 WHERE ref_id = 'REF-00734'
   AND evidence_type = 'co1'
   AND (synthesis_attribution_required IS NULL OR synthesis_attribution_required = 0);

COMMIT;
