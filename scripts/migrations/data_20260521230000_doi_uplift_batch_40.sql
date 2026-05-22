-- data_20260521230000_doi_uplift_batch_40.sql
-- DOI uplift batch 40: 4 rows with confirmed DOI matches.
--
-- REF-00386: Kim C et al. 2014 IJIE — DOI 10.1016/j.ergon.2014.07.001 (ramp slope wheelchair) — journal+initial corrections
-- REF-00301: van Buuren L 2022 HERD — DOI 10.1177/19375867211043546 (Dementia-Friendly Design wayfinding) — initial correction R->L
-- REF-00542: Unwin K 2024 Autism — DOI 10.1177/13623613231180266 (multi-sensory environments time spent) — year correction 2023->2024
-- REF-00632: Keating CT et al. 2024 PLOS ONE — DOI 10.1371/journal.pone.0299824 (cross-cultural camouflaging) — owner-queue Crompton-hint-was-wrong

BEGIN TRANSACTION;

-- REF-00386: Kim 2014 IJIE
UPDATE evidence_sources SET
    pub_title = 'Effects of ramp slope, ramp height and users'' pushing force on performance, muscular activity and subjective ratings during wheelchair driving on a ramp',
    pub_year = 2014,
    first_author_last = 'Kim',
    first_author_first = 'C',
    is_corporate_primary = 0,
    author_display = 'Kim C, Lee D, Kwon S, Chung M',
    publisher = 'Elsevier; International Journal of Industrial Ergonomics',
    journal_name = 'International Journal of Industrial Ergonomics',
    journal_abbrev = 'Int J Ind Ergon',
    doi = '10.1016/j.ergon.2014.07.001',
    issn = '0169-8141',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTED-FROM-JMST-AND-INITIAL-W-TO-C',
    metadata_integrity_detail = 'doi-uplift-batch-40 2026-05-21T23:00:00Z: Crossref-confirmed. DB previously had first_author_last="Kim", first_author_first="W" + journal="J Mech Sci Technol" — both incorrect. Actual first author Kim C (with co-authors Lee D, Kwon S, Chung M). Actual journal Int J Ind Ergon. Study examines effects of ramp slope + ramp height + user pushing force on wheelchair driving performance, muscular activity, and subjective ratings. Strong contextual match for DB context "Effect of slope on wheelchair users".',
    url = 'https://doi.org/10.1016/j.ergon.2014.07.001',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:00:00Z doi-uplift-batch-40] DOI resolved + journal + initial corrected',
    updated_at = '2026-05-21T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00386';

-- REF-00301: van Buuren 2022 HERD
UPDATE evidence_sources SET
    pub_title = 'Dementia-Friendly Design: A Set of Design Criteria and Design Typologies Supporting Wayfinding',
    pub_year = 2022,
    first_author_last = 'van Buuren',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'van Buuren LPG (Lyanne), Mohammadi M',
    publisher = 'SAGE Publications; HERD: Health Environments Research & Design Journal',
    journal_name = 'HERD: Health Environments Research & Design Journal',
    journal_abbrev = 'HERD',
    doi = '10.1177/19375867211043546',
    issn = '1937-5867',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'TITLE-CORRECTED-AND-INITIAL-R-TO-L',
    metadata_integrity_detail = 'doi-uplift-batch-40 2026-05-21T23:00:00Z: Crossref-confirmed. DB previously had first_author_first="R" (initials confusion in original Dutch researcher van Buuren); actual is L (Lyanne) van Buuren. Co-author Mohammadi (M, not N). DB title "Dutch facility floor plan evaluation. HERD" is generic description — actual title is "Dementia-Friendly Design: A Set of Design Criteria and Design Typologies Supporting Wayfinding". This is the foundational paper that REF-00520 follow-up (van Buuren 2025 Frontiers in Dementia DOI 10.3389/frdem.2025.1524425) builds on.',
    url = 'https://doi.org/10.1177/19375867211043546',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:00:00Z doi-uplift-batch-40] DOI resolved + title + initial corrected',
    updated_at = '2026-05-21T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00301';

-- REF-00542: Unwin 2024 Autism — year correction + DOI
UPDATE evidence_sources SET
    pub_title = 'Patterns of equipment use for autistic children in multi-sensory environments: Time spent with sensory equipment varies by-population',
    pub_year = 2024,
    first_author_last = 'Unwin',
    first_author_first = 'KL',
    is_corporate_primary = 0,
    author_display = 'Unwin KL, Powell G, Price A, Jones CRG',
    publisher = 'SAGE Publications; Autism (journal of NAS)',
    journal_name = 'Autism',
    journal_abbrev = 'Autism',
    doi = '10.1177/13623613231180266',
    issn = '1362-3613',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-2023-TO-2024',
    metadata_integrity_detail = 'doi-uplift-batch-40 2026-05-21T23:00:00Z: Crossref-confirmed. Karla L. Unwin (Cardiff University) + Powell + Price + Jones (Cardiff) MSE/Snoezelen patterns of use study; online first 2023, print 2024. Original DB row pub_year=2023 corrected to 2024. Confirms K. L. Unwin as lead author (DB hint correct).',
    url = 'https://doi.org/10.1177/13623613231180266',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:00:00Z doi-uplift-batch-40] DOI resolved + year corrected',
    updated_at = '2026-05-21T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00542';

-- REF-00632: Keating 2024 PLOS ONE cross-cultural camouflaging
UPDATE evidence_sources SET
    pub_title = 'Cross-cultural variation in experiences of acceptance, camouflaging and mental health difficulties in autism: A registered report',
    pub_year = 2024,
    first_author_last = 'Keating',
    first_author_first = 'CT',
    is_corporate_primary = 0,
    author_display = 'Keating CT, Hickman L, Geelhand P, Takahashi T, Leung J, Monk R, Schuster B, Rybicki A, Girolamo TM, Clin E, Papastamou F, Belenger M, Eigsti IM, Cook JL, Kosaka H, Osu R, Okamoto Y, Sowden-Carvalho S (18 authors)',
    publisher = 'Public Library of Science; PLOS ONE',
    journal_name = 'PLOS ONE',
    journal_abbrev = 'PLOS ONE',
    doi = '10.1371/journal.pone.0299824',
    issn = '1932-6203',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CROMPTON-HINT-INCORRECT-CORRECTED',
    metadata_integrity_detail = 'doi-uplift-batch-40 2026-05-21T23:00:00Z: Crossref-confirmed. DB hint author_display="(Crompton co-author)" was inaccurate — actual 18-author roster does not include Crompton. Lead author Connor T. Keating (University of Birmingham); registered report design. Owner-queue: confirm Crompton hint was transcription error, not different paper. Strongest cross-cultural camouflaging in autism paper for 2023-2025 window.',
    url = 'https://doi.org/10.1371/journal.pone.0299824',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:00:00Z doi-uplift-batch-40] DOI resolved; Crompton hint was wrong (owner-queue)',
    updated_at = '2026-05-21T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00632';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
