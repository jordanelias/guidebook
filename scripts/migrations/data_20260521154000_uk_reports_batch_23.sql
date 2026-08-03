-- data_20260521154000_uk_reports_batch_23.sql
-- UK reports batch 23: 1 row verified — REF-00258 M4(3) cost study cites Provan 2023.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    pub_title = 'M4(3) Wheelchair Standard Cost Study — cost-benefit estimates from Provan et al. (LSE CASEreport 147)',
    pub_year = 2023,
    first_author_last = 'Provan',
    first_author_first = 'James Albert',
    is_corporate_primary = 0,
    author_display = 'Provan, J. A.; Lane, L.; Horne Rowan, J. (LSE Housing and Communities); commissioned by Habinteg Housing Association',
    publisher = 'London School of Economics — Centre for Analysis of Social Exclusion (CASE); commissioned by Habinteg',
    standard_number = 'CASEreport 147',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00268',
    metadata_integrity_detail = 'uk-reports-batch-23 2026-05-21T15:40:00Z: web-search verified via eprints.lse.ac.uk/121508 + Inside Housing report + Habinteg + Manchester DPAG NPPF response. The "M4(3) Wheelchair Standard Cost Study" framing of this row maps to the cost figures published in the Provan/Lane/Horne Rowan 2023 LSE CASEreport 147 (also published by Habinteg as "Living Not Existing"). Key cost figures: +£22,000 build cost for working-age wheelchair user M4(3) home vs M4(2); +£26,000 for child/older household; 10-year benefits £94,000 / £66,000 / £101,000 respectively. Owner: consolidate with REF-00268 or keep separate if the BPC distinguishes.',
    url = 'https://eprints.lse.ac.uk/121508/1/casereport147.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+lse-eprints',
    last_verified_at = '2026-05-21T15:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:40:00Z uk-reports-batch-23] web-search verified; flagged as potential duplicate of REF-00268',
    updated_at = '2026-05-21T15:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00258';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
