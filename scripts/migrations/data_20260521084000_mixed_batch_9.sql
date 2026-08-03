-- data_20260521084000_mixed_batch_9.sql
--
-- Mixed batch 9: classic book + journal article verification.
--
-- REF-00484: Kahneman D. (1973) Attention and Effort, Prentice-Hall
-- REF-00203: Walton C. et al. (2020) Rising prevalence of multiple sclerosis worldwide: Insights
--            from the Atlas of MS, third edition. Multiple Sclerosis Journal 26(14):1816-1821

BEGIN TRANSACTION;

-- REF-00484: Kahneman 1973 Attention and Effort
UPDATE evidence_sources SET
    pub_title = 'Attention and Effort',
    pub_year = 1973,
    first_author_last = 'Kahneman',
    first_author_first = 'Daniel',
    is_corporate_primary = 0,
    author_display = 'Kahneman, D. (Hebrew University of Jerusalem)',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'Prentice-Hall, Englewood Cliffs, NJ',
    isbn = '9780130505187',
    pages_start = 'x',
    pages_end = '246',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-9 2026-05-21T08:40:00Z: web-search verified via Amazon + Abebooks + PDF (Knowen-production AWS-hosted) + 2018 Frontiers in Psychology retrospective. Prentice-Hall Series in Experimental Psychology. ISBN-13 9780130505187, ISBN-10 0130505188. LCCN 73-3375. 246 pages. Foundational work on attentional resource theory; introduced the equivalence claim attention=effort. Kahneman was awarded 2002 Nobel Memorial Prize in Economic Sciences.',
    url = 'https://www.amazon.com/Attention-effort-Prentice-Hall-experimental-psychology/dp/0130505188',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+isbn-confirm',
    last_verified_at = '2026-05-21T08:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T08:40:00Z mixed-batch-9] web-search + ISBN verified',
    updated_at = '2026-05-21T08:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00484';

-- REF-00203: Walton et al. 2020 MS Atlas paper
UPDATE evidence_sources SET
    doi = '10.1177/1352458520970841',
    pub_title = 'Rising prevalence of multiple sclerosis worldwide: Insights from the Atlas of MS, third edition',
    pub_year = 2020,
    first_author_last = 'Walton',
    first_author_first = 'Clare',
    is_corporate_primary = 0,
    author_display = 'Walton, C.; King, R.; Rechtman, L.; Kaye, W.; Leray, E.; Marrie, R. A.; Robertson, N.; La Rocca, N.; Uitdehaag, B.; van der Mei, I.; Wallin, M.; Helme, A.; Angood Napier, C.; Rijke, N.; Baneke, P.',
    author_count = 15,
    author_count_is_complete = 1,
    journal_name = 'Multiple Sclerosis Journal',
    volume = '26',
    issue = '14',
    pages_start = '1816',
    pages_end = '1821',
    publisher = 'SAGE Publications',
    issn = '1352-4585',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-9 2026-05-21T08:40:00Z: web-search-identified candidate + Crossref-confirmed canonical metadata. DOI 10.1177/1352458520970841 resolves to the 3rd-edition academic publication of the MS Atlas (MSIF). Stored row title "MS International Federation Atlas 2023" likely refers to the live atlasofms.org web platform data updates (most recent Nov 2023); the 3rd-edition formal paper is Walton et al. 2020 in Multiple Sclerosis Journal. For citation purposes the 2020 journal article is canonical; live web data updates the underlying numbers.',
    url = 'https://journals.sagepub.com/doi/10.1177/1352458520970841',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T08:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T08:40:00Z mixed-batch-9] web-search + Crossref confirmed; stored year 2023 -> 2020 (publication year of 3rd-edition paper)',
    updated_at = '2026-05-21T08:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00203';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
