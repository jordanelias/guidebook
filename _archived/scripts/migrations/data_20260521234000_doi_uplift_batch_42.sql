-- data_20260521234000_doi_uplift_batch_42.sql
-- DOI uplift batch 42: 2 rows DOI resolved.
--
-- REF-00296 + REF-00307: Ielegems & Vanrie 2024 Archnet-IJAR 18(4) — DOI 10.1108/arch-07-2023-0178 — dup pair

BEGIN TRANSACTION;

-- REF-00296: Ielegems Vanrie 2024 Archnet-IJAR (parent)
UPDATE evidence_sources SET
    pub_title = 'The cost of universal design for public buildings: exploring a realistic, context-dependent research approach',
    pub_year = 2024,
    first_author_last = 'Ielegems',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'Ielegems E, Vanrie J',
    publisher = 'Emerald Publishing; Archnet-IJAR: International Journal of Architectural Research',
    journal_name = 'Archnet-IJAR: International Journal of Architectural Research',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.1108/arch-07-2023-0178',
    issn = '2631-6862',
    volume = '18',
    issue = '4',
    jurisdiction = 'BE',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00307',
    metadata_integrity_detail = 'doi-uplift-batch-42 2026-05-21T23:40:00Z: Crossref-confirmed. Ielegems E + Vanrie J (Hasselt University, Belgium) study on cost of universal design for public buildings via realistic context-dependent research approach. Archnet-IJAR 18(4) — Emerald. Owner: 2-row pair with REF-00307. Jurisdiction now corrected to BE (Belgium-affiliated authors, though the journal is international); previous DB jurisdiction was INT.',
    url = 'https://doi.org/10.1108/arch-07-2023-0178',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:40:00Z doi-uplift-batch-42] DOI resolved',
    updated_at = '2026-05-21T23:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00296';

-- REF-00307: Ielegems Vanrie 2024 Archnet-IJAR (dup)
UPDATE evidence_sources SET
    pub_title = 'The cost of universal design for public buildings: exploring a realistic, context-dependent research approach',
    pub_year = 2024,
    first_author_last = 'Ielegems',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'Ielegems E, Vanrie J',
    publisher = 'Emerald Publishing; Archnet-IJAR: International Journal of Architectural Research',
    journal_name = 'Archnet-IJAR: International Journal of Architectural Research',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.1108/arch-07-2023-0178',
    issn = '2631-6862',
    volume = '18',
    issue = '4',
    jurisdiction = 'BE',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00296',
    metadata_integrity_detail = 'doi-uplift-batch-42 2026-05-21T23:40:00Z: same parent as REF-00296. Owner: 2-row pair.',
    url = 'https://doi.org/10.1108/arch-07-2023-0178',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:40:00Z doi-uplift-batch-42] DOI resolved',
    updated_at = '2026-05-21T23:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00307';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
