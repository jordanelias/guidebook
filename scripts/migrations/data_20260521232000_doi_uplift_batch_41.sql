-- data_20260521232000_doi_uplift_batch_41.sql
-- DOI uplift batch 41: 4 rows DOI resolved.
--
-- REF-00607: Tsironis et al. 2024 Trends in Hearing — DOI 10.1177/23312165241273399 (reverberation SR)
-- REF-00256: Tang et al. 2025 J Build Eng — DOI 10.1016/j.jobe.2024.111714 (thermal comfort ageing SR) — year-corrected 2024->2025
-- REF-00391: Levine et al. 2025 JMIR R&AT — DOI 10.2196/69442 (bathtub grab bar) — pre-existing dup with REF-00029 + REF-00367
-- REF-00395: Harper et al. 2025 IJMR — DOI 10.2196/60622 (interstep variation + high-contrast striping)

BEGIN TRANSACTION;

-- REF-00607: Tsironis 2024 Trends in Hearing
UPDATE evidence_sources SET
    pub_title = 'Adaptation to Reverberation for Speech Perception: A Systematic Review',
    pub_year = 2024,
    first_author_last = 'Tsironis',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Tsironis A, Vlahou E, Kontou P, Bagos P, Kopčo N',
    publisher = 'SAGE Publications; Trends in Hearing',
    journal_name = 'Trends in Hearing',
    journal_abbrev = 'Trends Hear',
    doi = '10.1177/23312165241273399',
    issn = '2331-2165',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'doi-uplift-batch-41 2026-05-21T23:20:00Z: Crossref-confirmed. Systematic review of how listeners adapt to reverberation when processing speech. 5-author open-access SR in Trends in Hearing (SAGE).',
    url = 'https://doi.org/10.1177/23312165241273399',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:20:00Z doi-uplift-batch-41] DOI resolved',
    updated_at = '2026-05-21T23:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00607';

-- REF-00256: Tang 2025 J Build Eng (year-correct 2024->2025)
UPDATE evidence_sources SET
    pub_title = 'Indoor thermal comfort and ageing: A systematic review',
    pub_year = 2025,
    first_author_last = 'Tang',
    first_author_first = 'Y',
    is_corporate_primary = 0,
    author_display = 'Tang Y, Yu H, Mao H, Zhang K, Wang M',
    publisher = 'Elsevier; Journal of Building Engineering',
    journal_name = 'Journal of Building Engineering',
    journal_abbrev = 'J Build Eng',
    doi = '10.1016/j.jobe.2024.111714',
    issn = '2352-7102',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-2024-TO-2025',
    metadata_integrity_detail = 'doi-uplift-batch-41 2026-05-21T23:20:00Z: Crossref-confirmed. DOI registered with 2024 manuscript prefix; print publication 2025. Systematic review of indoor thermal comfort needs of older adults. 5-author SR in J Building Engineering (Elsevier).',
    url = 'https://doi.org/10.1016/j.jobe.2024.111714',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:20:00Z doi-uplift-batch-41] DOI resolved + year corrected',
    updated_at = '2026-05-21T23:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00256';

-- REF-00391: Levine 2025 JMIR R&AT (existing dup with REF-00029+00367)
UPDATE evidence_sources SET
    pub_title = 'Grab Bar Grasp Location During Bathtub Exit and Sit-to-Stand Transfers: Biomechanical Evaluation',
    pub_year = 2025,
    first_author_last = 'Levine',
    first_author_first = 'I',
    is_corporate_primary = 0,
    author_display = 'Levine I, Nirmalanathan K, Montgomery R, Novak A',
    publisher = 'JMIR Publications; JMIR Rehabilitation and Assistive Technologies',
    journal_name = 'JMIR Rehabilitation and Assistive Technologies',
    journal_abbrev = 'JMIR Rehabil Assist Technol',
    doi = '10.2196/69442',
    issn = '2369-2529',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'KNOWN-CLUSTER-WITH-REF-00029-AND-REF-00367',
    metadata_integrity_detail = 'doi-uplift-batch-41 2026-05-21T23:20:00Z: Crossref-confirmed. Peak grip force during bathtub exit fall recovery 1.3 kN observation from this Levine et al. biomechanical study. Already in KNOWN_DUP_DOIS allowlist as 10.2196/69442 cluster with REF-00029 + REF-00367 (now 3-row cluster including REF-00391). Toronto Rehabilitation Institute / KITE Research.',
    url = 'https://doi.org/10.2196/69442',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:20:00Z doi-uplift-batch-41] DOI resolved (3-row cluster)',
    updated_at = '2026-05-21T23:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00391';

-- REF-00395: Harper 2025 IJMR
UPDATE evidence_sources SET
    pub_title = 'Interstep Variations of Stairways and Associations of High-Contrast Striping and Fall-Related Events: Observational Study',
    pub_year = 2025,
    first_author_last = 'Harper',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Harper S, Brown C, Poulsen S, Barrett T, Dakin C',
    publisher = 'JMIR Publications; Interactive Journal of Medical Research',
    journal_name = 'Interactive Journal of Medical Research',
    journal_abbrev = 'Interact J Med Res',
    doi = '10.2196/60622',
    issn = '1929-073X',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'doi-uplift-batch-41 2026-05-21T23:20:00Z: Crossref-confirmed. Observational study of interstep variations + high-contrast stripe interventions on stairways with fall-related event associations. 5-author paper in IJMR.',
    url = 'https://doi.org/10.2196/60622',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-21T23:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T23:20:00Z doi-uplift-batch-41] DOI resolved',
    updated_at = '2026-05-21T23:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00395';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
