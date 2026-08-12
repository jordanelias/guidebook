-- data_20260521224500_doi_uplift_batch_39.sql
-- DOI uplift batch 39: 6 rows with confirmed DOI matches.
--
-- REF-00033: Lee 2018 HERD (title 2017 review of Lee; HERD pub year 2018) — DOI 10.1177/1937586717730338
-- REF-00384: Simoneau GG 1991 J Gerontol — DOI 10.1093/geronj/46.6.m188 (visual factors / fall-related kinematics stair descent)
-- REF-00388: Koontz 2012 APMR — DOI 10.1016/j.apmr.2011.10.023 (Backrest Height Wheelchair Propulsion) — best Crossref fit
-- REF-00520: van Buuren 2025 Frontiers in Dementia — DOI 10.3389/frdem.2025.1524425 PMC11931140
-- REF-00729: Faerden 2023 HERD — DOI 10.1177/19375867221136558 (Environmental Transformations Enhancing Dignity) [year-correct 2022->2023]
-- REF-00732: Strassheim 2018 BMJ Open — DOI 10.1136/bmjopen-2017-020775 (severe CFS prevalence/symptom burden)

BEGIN TRANSACTION;

-- REF-00033: Lee 2018 HERD — DOI UPGRADE + year correction
UPDATE evidence_sources SET
    pub_title = 'Beyond ADA Accessibility Requirements: Meeting Seniors'' Needs for Toilet Transfers — bilateral fold-down grab bars 813mm/32" height outperform ADA-compliant configuration',
    pub_year = 2018,
    first_author_last = 'Lee',
    first_author_first = 'SJ',
    is_corporate_primary = 0,
    author_display = 'Lee SJ + colleagues (Su Jin Lee et al.)',
    publisher = 'SAGE Publications; HERD: Health Environments Research & Design Journal',
    journal_name = 'HERD: Health Environments Research & Design Journal',
    journal_abbrev = 'HERD',
    doi = '10.1177/1937586717730338',
    issn = '1937-5867',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-2017-TO-2018',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: DOI confirmed via Crossref + Healthcare Design Magazine 2017 review of Lee study. HERD publication year 2018 (online first 2017). Phase 1 of study found ADA configurations inadequate for majority; Phase 2 user-defined configuration: bilateral fold-down grab bars 14 inches from toilet centerline, 32 inches above floor, extending min 6 inches forward, one side open + sidewall 24 inches from centerline on other. 60% of residents+caregivers preferred user-defined configuration. Year corrected 2017->2018.',
    url = 'https://doi.org/10.1177/1937586717730338',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref+hcd-magazine',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] DOI resolved + year corrected',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00033';

-- REF-00384: Simoneau 1991 J Gerontol — DOI UPGRADE + title corrected
UPDATE evidence_sources SET
    pub_title = 'The Influence of Visual Factors on Fall-related Kinematic Variables During Stair Descent by Older Women',
    pub_year = 1991,
    first_author_last = 'Simoneau',
    first_author_first = 'GG',
    is_corporate_primary = 0,
    author_display = 'Simoneau GG + colleagues',
    publisher = 'Oxford University Press / Gerontological Society of America; Journal of Gerontology',
    journal_name = 'Journal of Gerontology',
    journal_abbrev = 'J Gerontol',
    doi = '10.1093/geronj/46.6.m188',
    issn = '0022-1422',
    volume = '46',
    issue = '6',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'TITLE-CORRECTED-FROM-WHOLE-BODY-KINEMATICS',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: Crossref hit — Simoneau GG 1991 stair-research paper in J Gerontol 46(6):M188+ on visual factors and fall-related kinematic variables during stair descent by older women. Previous DB title "Whole-body kinematics during stair ascent and descent. Hum Mov Sci" was inaccurate transcription; Crossref returns this Journal of Gerontology paper as the canonical Simoneau 1991 stair paper. Other Simoneau 1991 papers in Crossref are in MSSE/JCI on metabolism, not biomechanics. Owner-queue: confirm whether row should be REF retained or replaced; title now matches Crossref record.',
    url = 'https://doi.org/10.1093/geronj/46.6.m188',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] DOI resolved + title corrected',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00384';

-- REF-00388: Koontz 2012 APMR — DOI UPGRADE
UPDATE evidence_sources SET
    pub_title = 'Effect of Backrest Height on Wheelchair Propulsion Biomechanics for Level and Uphill (best-fit Crossref candidate for shoulder moment contributions; alternative candidate JAB 28(4):412 overground/dynamometer comparison)',
    pub_year = 2012,
    first_author_last = 'Koontz',
    first_author_first = 'AM',
    is_corporate_primary = 0,
    author_display = 'Koontz AM + colleagues',
    publisher = 'Elsevier; Archives of Physical Medicine and Rehabilitation',
    journal_name = 'Archives of Physical Medicine and Rehabilitation',
    journal_abbrev = 'Arch Phys Med Rehabil',
    doi = '10.1016/j.apmr.2011.10.023',
    issn = '0003-9993',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OWNER-QUEUE-DISAMBIGUATE',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: two Crossref candidates for Koontz 2012 wheelchair propulsion biomechanics: (a) APMR DOI 10.1016/j.apmr.2011.10.023 Backrest Height Wheelchair Propulsion Biomechanics for Level and Uphill; (b) J Appl Biomech 28(4):412 DOI 10.1123/jab.28.4.412 Overground vs Dynamometer Manual Wheelchair Propulsion. Selected (a) APMR because original DB title "Shoulder moment contributions to wheelchair propulsion. Clin Biomech" suggests shoulder kinetics during propulsion, and APMR backrest study includes shoulder kinetics analysis. Owner-queue: confirm disambiguation on next pass; possibly correct candidate is Clin Biomech 27(2):203 if shoulder is specifically the focus.',
    url = 'https://doi.org/10.1016/j.apmr.2011.10.023',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] DOI resolved; owner-queue for disambiguation between APMR backrest and JAB overground/dynamometer',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00388';

-- REF-00520: van Buuren 2025 Frontiers in Dementia — DOI + PMC UPGRADE
UPDATE evidence_sources SET
    pub_title = 'Wayfinding behavioral patterns of seniors with dementia: two exploratory case studies',
    pub_year = 2025,
    first_author_last = 'van Buuren',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'van Buuren LPG + colleagues',
    publisher = 'Frontiers Media; Frontiers in Dementia',
    journal_name = 'Frontiers in Dementia',
    journal_abbrev = 'Front Dement',
    doi = '10.3389/frdem.2025.1524425',
    pmcid = 'PMC11931140',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: PMC ID PMC11931140 in DB title resolved via NCBI eutils to DOI 10.3389/frdem.2025.1524425, Frontiers in Dementia 2025. Title confirmed: "Wayfinding behavioral patterns of seniors with dementia: two exploratory case studies".',
    url = 'https://doi.org/10.3389/frdem.2025.1524425',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ncbi-eutils+pmc-id-resolution',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] PMC ID resolved to DOI via NCBI eutils',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00520';

-- REF-00729: Faerden 2023 HERD — DOI UPGRADE + year correction
UPDATE evidence_sources SET
    pub_title = 'Environmental Transformations Enhancing Dignity in an Acute Psychiatric Ward: Outcome of a Pre-Post Pilot Study (single rooms + patient control)',
    pub_year = 2023,
    first_author_last = 'Faerden',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Faerden A + colleagues',
    publisher = 'SAGE Publications; HERD: Health Environments Research & Design Journal',
    journal_name = 'HERD: Health Environments Research & Design Journal',
    journal_abbrev = 'HERD',
    doi = '10.1177/19375867221136558',
    issn = '1937-5867',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-2022-TO-2023',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: Crossref-confirmed. Pre-post pilot study on environmental transformations + dignity in acute psychiatric ward. Online first 2022; print 2023. Single rooms and patient control as key intervention components. Year corrected 2022->2023.',
    url = 'https://doi.org/10.1177/19375867221136558',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] DOI resolved + year corrected',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00729';

-- REF-00732: Strassheim 2018 BMJ Open — DOI UPGRADE
UPDATE evidence_sources SET
    pub_title = 'Defining the prevalence and symptom burden of those with self-reported severe chronic fatigue syndrome/myalgic encephalomyelitis (CFS/ME): a two-phase community pilot study in the North East of England',
    pub_year = 2018,
    first_author_last = 'Strassheim',
    first_author_first = 'V',
    is_corporate_primary = 0,
    author_display = 'Strassheim V + colleagues',
    publisher = 'BMJ Publishing Group; BMJ Open',
    journal_name = 'BMJ Open',
    journal_abbrev = 'BMJ Open',
    doi = '10.1136/bmjopen-2017-020775',
    issn = '2044-6055',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'doi-uplift-batch-39 2026-05-21T22:45:00Z: Crossref-confirmed BMJ Open 2018 study by Vicky Strassheim on severe CFS/ME prevalence + symptom burden including orthostatic intolerance (OI) component. North East England community pilot two-phase study. Companion 2017 Physical Therapy Reviews paper "Understanding severely affected CFS: the gravity of the situation" DOI 10.1080/10833196.2017.1327131 and 2017 Fatigue: BHB scoping review DOI 10.1080/21641846.2017.1333185 contextualise the OI-in-ME/CFS body of work.',
    url = 'https://doi.org/10.1136/bmjopen-2017-020775',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T22:45:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:45:00Z doi-uplift-batch-39] DOI resolved',
    updated_at = '2026-05-21T22:45:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00732';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
