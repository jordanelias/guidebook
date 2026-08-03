-- B05 fix: REF-00191 source_type was 'government_report' (invalid enum). Use 'report' (valid).
BEGIN TRANSACTION;
UPDATE evidence_sources SET source_type='report', updated_at='2026-05-22T23:05:00Z', updated_by_session='session_2026-05-20-ato-rehab' WHERE ref_id='REF-00191';
COMMIT;
