-- data_20260522135000_grey_round5.sql
-- Grey round 5: 1 row.
--
-- REF-00217: Christogianni A, Bibb R, Filingeri D (2024) J Thermal Biology 123:103887 DOI 10.1016/j.jtherbio.2024.103887

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'High-density thermal sensitivity maps of the body of people with multiple sclerosis: Implications for inclusive personal comfort systems',
    pub_year = 2024,
    first_author_last = 'Christogianni',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Christogianni A, Bibb R, Filingeri D',
    publisher = 'Elsevier BV',
    journal_name = 'Journal of Thermal Biology',
    journal_abbrev = 'J Therm Biol',
    doi = '10.1016/j.jtherbio.2024.103887',
    issn = '0306-4565',
    volume = '123',
    article_number = '103887',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND5',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round5 2026-05-22T13:50:00Z: Crossref-resolved Christogianni + Bibb + Filingeri 2024 J Therm Biol continuation of 2022 MSARD MS heat sensitivity research (REF-00254 sister paper); University of Southampton thermal physiology group. DB description "MS housing design peer-reviewed source 2025" — year corrected 2025→2024; topic is personal-comfort-system design implications from high-density thermal mapping.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T13:50:00Z',
    updated_at = '2026-05-22T13:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00217';

COMMIT;
