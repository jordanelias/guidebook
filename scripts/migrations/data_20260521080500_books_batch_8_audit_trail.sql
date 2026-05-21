-- data_20260521080500_books_batch_8_audit_trail.sql
-- Companion to books batch 8: set doi_resolution_outcome=NO-MATCH per C04.
-- C04 requires COMPLETE rows to have DOI, co1-verified flag, or non-RESOLVED outcome.
-- Books predating DOI era have no DOI by nature; mark as NO-MATCH to clear audit.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    doi_resolution_outcome = 'NO-MATCH'
WHERE ref_id IN ('REF-00176', 'REF-00478', 'REF-00485')
  AND (doi IS NULL OR doi = '');

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
