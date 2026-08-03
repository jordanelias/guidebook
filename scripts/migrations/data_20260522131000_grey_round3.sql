-- data_20260522131000_grey_round3.sql
-- GREY round 3 targeted resolution: 2 rows verified.
--
-- REF-00032: Cockayne S et al. (2021) F1000Res 10:500 OTIS trial home hazard assessment falls — DOI 10.12688/f1000research.52313.1
-- REF-00097: Haig S, Hallett N (2023) Int J Ment Health Nurs 32(1):54-75 sensory rooms psychiatric inpatient SR — DOI 10.1111/inm.13065

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Home hazard assessment and environmental modification to prevent falls in older people: the OTIS trial — a study protocol for a multicentre randomised controlled trial',
    pub_year = 2021,
    first_author_last = 'Cockayne',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Cockayne S, Pighills A, Fairhurst C, Adamson J, Crossland S, Drummond A, Hewitt C, Rodgers S, Ronaldson S, McCaffery J',
    publisher = 'F1000 Research Ltd',
    journal_name = 'F1000Research',
    journal_abbrev = 'F1000Res',
    doi = '10.12688/f1000research.52313.1',
    issn = '2046-1402',
    volume = '10',
    pages_start = '500',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND3',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round3 2026-05-22T13:10:00Z: Crossref-resolved OTIS trial protocol Cockayne + York Trials Unit + 10-author team; companion REF-00033/REF-00034 (other UK falls research).',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T13:10:00Z',
    updated_at = '2026-05-22T13:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00032';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Use of sensory rooms in adult psychiatric inpatient settings: A systematic review and narrative synthesis',
    pub_year = 2023,
    first_author_last = 'Haig',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Haig S, Hallett N',
    publisher = 'Wiley',
    journal_name = 'International Journal of Mental Health Nursing',
    journal_abbrev = 'Int J Ment Health Nurs',
    doi = '10.1111/inm.13065',
    issn = '1445-8330',
    volume = '32',
    issue = '1',
    pages_start = '54',
    pages_end = '75',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND3',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round3 2026-05-22T13:10:00Z: Crossref-resolved Haig + Hallett 2023 sensory rooms psychiatric inpatient SR + narrative synthesis; 2-author UK University of Birmingham team.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T13:10:00Z',
    updated_at = '2026-05-22T13:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00097';

COMMIT;
