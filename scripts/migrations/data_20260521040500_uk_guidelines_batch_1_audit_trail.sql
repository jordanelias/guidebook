-- data_20260521040500_uk_guidelines_batch_1_audit_trail.sql
-- Companion to data_20260521040000_uk_guidelines_batch_1.sql.
-- C01 db_integrity: VERIFIED rows must have audit trail (doi/url/pmid or
-- verified_by_tool). Populates url + verified_by_tool + last_verified_at
-- for the 6 newly-verified UK guideline rows.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    url = 'https://www.gov.uk/government/publications/access-to-and-use-of-buildings-approved-document-m',
    url_accessed = '2026-05-21',
    verified_by_tool = COALESCE(verified_by_tool, 'web-search-multi+gov-uk-official'),
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00425';

UPDATE evidence_sources SET
    url = 'https://www.ribabooks.com/wheelchair-housing-design-guide_9781859468289',
    url_accessed = '2026-05-21',
    verified_by_tool = COALESCE(verified_by_tool, 'web-search-multi+riba-books'),
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00405';

UPDATE evidence_sources SET
    url = 'https://www.habinteg.org.uk/the-inclusive-housing-design-guide/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+habinteg-official',
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00404';

UPDATE evidence_sources SET
    url = 'https://www.habinteg.org.uk/the-inclusive-housing-design-guide/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+habinteg-official',
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00437';

-- REF-00378 already has url + verified_by_tool from prior session; no change needed but refresh
UPDATE evidence_sources SET
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00378';

UPDATE evidence_sources SET
    url = 'https://www.housinglin.org.uk/_assets/Resources/Housing/Support_materials/Other_reports_and_guidance/Adaptations-Without-Delay.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+housing-lin-pdf',
    last_verified_at = '2026-05-21T04:00:00Z'
WHERE ref_id = 'REF-00053';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
