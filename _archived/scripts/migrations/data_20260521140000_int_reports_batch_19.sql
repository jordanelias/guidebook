-- data_20260521140000_int_reports_batch_19.sql
-- INT reports batch 19: 4 rows verified.
--
-- REF-00090: Owen & Crane (2022) TID scoping review — IJERPH 19(21):14279, DOI 10.3390/ijerph192114279
-- REF-00735: Devos et al. (2019) Designing Supportive Soundscapes — IJERPH 16(24):4904, DOI 10.3390/ijerph16244904
-- REF-00342: Vaughn (2018) DeafScape — Ground Up Journal Issue 7
-- REF-00343: Bauman & Murray (eds.) (2014) Deaf Gain — Univ. of Minnesota Press, ISBN 9780816691227

BEGIN TRANSACTION;

-- REF-00090: Owen & Crane TID
UPDATE evidence_sources SET
    doi = '10.3390/ijerph192114279',
    pmid = '36361166',
    pmcid = 'PMC9658651',
    pub_title = 'Trauma-Informed Design of Supported Housing: A Scoping Review through the Lens of Neuroscience',
    pub_year = 2022,
    first_author_last = 'Owen',
    first_author_first = 'Ceridwen',
    is_corporate_primary = 0,
    author_display = 'Owen, C.; Crane, J. (University of Tasmania)',
    author_count = 2,
    author_count_is_complete = 1,
    journal_name = 'International Journal of Environmental Research and Public Health',
    volume = '19',
    issue = '21',
    pages_start = '14279',
    publisher = 'MDPI (Multidisciplinary Digital Publishing Institute)',
    issn = '1660-4601',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-19 2026-05-21T14:00:00Z: PMC + Crossref verified. Published 1 Nov 2022. Open access. Stored jurisdiction INT corrected to AU (both authors at University of Tasmania). The TID stored description maps directly to this paper.',
    url = 'https://doi.org/10.3390/ijerph192114279',
    url_accessed = '2026-05-21',
    verified_by_tool = 'pmc-fetch+crossref-confirm',
    last_verified_at = '2026-05-21T14:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T14:00:00Z int-reports-batch-19] PMC9658651 DOI confirmed',
    updated_at = '2026-05-21T14:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00090';

-- REF-00735: Devos et al. dementia soundscape
UPDATE evidence_sources SET
    doi = '10.3390/ijerph16244904',
    pmid = '31817300',
    pmcid = 'PMC6950055',
    pub_title = 'Designing Supportive Soundscapes for Nursing Home Residents with Dementia',
    pub_year = 2019,
    first_author_last = 'Devos',
    first_author_first = 'Paul',
    is_corporate_primary = 0,
    author_display = 'Devos, P.; Aletta, F.; Thomas, P.; Petrovic, M.; Vander Mynsbrugge, T.; Van de Velde, D.; De Vriendt, P.; Botteldooren, D. (Ghent University + Artevelde UC + UCL)',
    author_count = 8,
    author_count_is_complete = 1,
    journal_name = 'International Journal of Environmental Research and Public Health',
    volume = '16',
    issue = '24',
    pages_start = '4904',
    publisher = 'MDPI (Multidisciplinary Digital Publishing Institute)',
    issn = '1660-4601',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-19 2026-05-21T14:00:00Z: PMC + Crossref verified. Published 4 Dec 2019. Open access. Multi-institution: Ghent University (BE), UCL (UK), Artevelde University College (BE).',
    url = 'https://doi.org/10.3390/ijerph16244904',
    url_accessed = '2026-05-21',
    verified_by_tool = 'pmc-fetch+crossref-confirm',
    last_verified_at = '2026-05-21T14:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T14:00:00Z int-reports-batch-19] PMC6950055 DOI confirmed',
    updated_at = '2026-05-21T14:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00735';

-- REF-00342: Vaughn DeafScape
UPDATE evidence_sources SET
    pub_title = 'DeafScape: Applying DeafSpace to Landscape',
    pub_year = 2018,
    first_author_last = 'Vaughn',
    first_author_first = 'Alexa',
    is_corporate_primary = 0,
    author_display = 'Vaughn, A. (Associate ASLA; OLIN Los Angeles; UC Berkeley)',
    author_count = 1,
    author_count_is_complete = 1,
    journal_name = 'Ground Up Journal',
    issue = '7',
    publisher = 'Ground Up Journal — UC Berkeley College of Environmental Design (Landscape Architecture)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-19 2026-05-21T14:00:00Z: web-search verified via designwithdisabledpeoplenow.com + Madame Architect + UC Berkeley CED + ASLA learn + LAF Foundation + Landscape Performance Series + issuu.com/alexavaughn. Published Issue 7 of Ground Up Journal (UC Berkeley CED Landscape Architecture journal), May 2018. Companion materials hosted at designwithdisabledpeoplenow.com (Vaughn''s ongoing toolkit website). Applies Gallaudet DeafSpace Design Guidelines (Bauman 2010 — see REF-00338/REF-00339) to landscape architecture and urban design. Stored jurisdiction INT corrected to US (UC Berkeley/OLIN LA).',
    url = 'https://www.designwithdisabledpeoplenow.com/deafscape',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ucb-asla-official',
    last_verified_at = '2026-05-21T14:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T14:00:00Z int-reports-batch-19] web-search verified',
    updated_at = '2026-05-21T14:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00342';

-- REF-00343: Bauman & Murray Deaf Gain book
UPDATE evidence_sources SET
    pub_title = 'Deaf Gain: Raising the Stakes for Human Diversity',
    pub_year = 2014,
    first_author_last = 'Bauman',
    first_author_first = 'H-Dirksen L.',
    is_corporate_primary = 0,
    author_display = 'Bauman, H-D. L.; Murray, J. J. (Eds.) — Gallaudet University ASL/Deaf Studies',
    author_count = 2,
    author_count_is_complete = 1,
    publisher = 'University of Minnesota Press, Minneapolis',
    isbn = '9780816691227',
    pages_start = 'xlii',
    pages_end = '521',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-19 2026-05-21T14:00:00Z: web-search verified via upress.umn.edu (publisher) + Amazon + Biblio + Google Books + Tandfonline review + R Discovery review. ISBN 9780816691227 paperback; 9780816691210 cloth. Published October 2014. Edited volume; contributors include Andrew Solomon, Tove Skutnabb-Kangas, and ~30 others organized into six sections: Philosophical Gains, Language Gains, Language Gains in Action, Sensory Gains, Social Gains, Creative Gains. NOTE: H-Dirksen L. Bauman (book editor, ASL/Deaf Studies prof at Gallaudet) is distinct from Hansel Bauman (DeafSpace architect; REF-00338/REF-00339) — both at Gallaudet but different individuals. Stored jurisdiction INT corrected to US.',
    url = 'https://www.upress.umn.edu/9780816691227/deaf-gain/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+umn-press-isbn',
    last_verified_at = '2026-05-21T14:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T14:00:00Z int-reports-batch-19] ISBN-verified',
    updated_at = '2026-05-21T14:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00343';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
