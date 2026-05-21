-- data_20260521001000_add_doi_to_displaced_replacements.sql
-- Companion to data_20260521000000. Step C of the displace-replace pattern
-- for REF-00150 and REF-00240 used PMID as the canonical source (PMID-only
-- input rows). Both PubMed records carry a DOI in articleids, but the prior
-- migration didn't copy that DOI to the row. Adds the canonical DOI, restoring
-- C04 db_integrity for these rows.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    doi = '10.1089/lrb.2017.0090',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit follow-up 2026-05-21T00:10:00Z: canonical DOI from PubMed articleids added (was missing from initial wrong-attribution correction)',
    updated_at = '2026-05-21T00:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00150';

UPDATE evidence_sources SET
    doi = '10.1007/s00296-008-0674-9',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit follow-up 2026-05-21T00:10:00Z: canonical DOI from PubMed articleids added (was missing from initial wrong-attribution correction)',
    updated_at = '2026-05-21T00:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00240';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
