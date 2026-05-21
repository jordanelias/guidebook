-- data_20260521040000_uk_guidelines_batch_1.sql
--
-- UK guidelines no-identifier cohort web-search verification batch 1.
-- Per DR-2026-05-18 statutory-metadata-completeness: gray-lit / regulatory /
-- institutional sources verify via issuing body + edition + year + publisher
-- + ISBN/URL — NOT via DOI. These rows have been web-search confirmed against
-- official publisher and government sources.
--
-- 6 rows promoted from AUTHOR-TITLE-ONLY to COMPLETE-STATUTORY.
--
-- REF-00425: Approved Document M Vol 2 (HM Government, 2024 amendments)
-- REF-00405: Wheelchair Housing Design Guide 3rd ed (Habinteg/RIBA, 2018)
-- REF-00404: Inclusive Housing Design Guide (Runnalls/Habinteg/RIBA, 2024)
-- REF-00437: Inclusive Housing Design Guide — threshold provisions (same source as REF-00404)
-- REF-00378: Adaptations Without Delay (RCOT/Housing LIN, 2019)
-- REF-00053: Housing Adaptations Without Delay (RCOT/Housing LIN, 2019; same source as REF-00378)

BEGIN TRANSACTION;

-- REF-00425: Approved Document M Vol 2 — Access to and use of buildings
-- Stored year 2026 → corrected to 2024 (2015 edition incorporating 2024 amendments)
UPDATE evidence_sources SET
    pub_title = 'Approved Document M: Access to and Use of Buildings, Volume 2 — Buildings other than dwellings (2015 edition with 2020 and 2024 amendments)',
    pub_year = 2024,
    first_author_last = 'HM Government',
    is_corporate_primary = 1,
    author_display = 'HM Government (Ministry of Housing, Communities and Local Government)',
    publisher = 'RIBA Publishing (on behalf of HM Government)',
    standard_number = 'Approved Document M Vol 2',
    isbn = '9781915722676',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: web-search verified via gov.uk + Planning Portal + RIBA Books. Stored year 2026 corrected to 2024 (current valid edition: 2015 incorporating 2020 + 2024 amendments, effective 1 October 2024). ISBN 9781915722676 (printed RIBA edition Aug 2024). Per DR-2026-05-18 statutory protocol.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00425';

-- REF-00405: Wheelchair Housing Design Guide 3rd ed
UPDATE evidence_sources SET
    pub_title = 'Wheelchair Housing Design Guide, 3rd Edition',
    pub_year = 2018,
    first_author_last = 'Habinteg Housing Association',
    is_corporate_primary = 1,
    author_display = 'Habinteg Housing Association; Centre for Accessible Environments (CAE); Royal College of Occupational Therapists Specialist Section — Housing (RCOTSS-Housing)',
    publisher = 'RIBA Publishing',
    isbn = '9781859468289',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: web-search verified via Habinteg + CAE + RIBA Books + LABC. Third edition published 12 February 2018, 136pp; designed to complement Building Regulations Approved Document M4 Category 3 (wheelchair accessible standard). Per DR-2026-05-18 statutory protocol.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00405';

-- REF-00404: Inclusive Housing Design Guide
UPDATE evidence_sources SET
    pub_title = 'The Inclusive Housing Design Guide',
    pub_year = 2024,
    first_author_last = 'Runnalls',
    first_author_first = 'Jacquel',
    is_corporate_primary = 0,
    author_display = 'Runnalls, J. (peer reviewed by Walker, M.)',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'RIBA Publishing (in partnership with Habinteg Housing Association and Centre for Accessible Environments)',
    isbn = '9781915722355',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: web-search verified via Habinteg + CAE + Amazon UK. Authored by Jacquel Runnalls (Specialist Housing Occupational Therapist), peer reviewed by Dr Marney Walker. Published 1 October 2024 in partnership Habinteg + CAE + RIBA. ISBN 9781915722355 (also published as Routledge e-book DOI 10.4324/9781003564164). Per DR-2026-05-18 statutory protocol.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00404';

-- REF-00437: Inclusive Housing Design Guide — threshold provisions (same source as REF-00404)
UPDATE evidence_sources SET
    pub_title = 'The Inclusive Housing Design Guide — threshold provisions section',
    pub_year = 2024,
    first_author_last = 'Runnalls',
    first_author_first = 'Jacquel',
    is_corporate_primary = 0,
    author_display = 'Runnalls, J. (peer reviewed by Walker, M.)',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'RIBA Publishing (in partnership with Habinteg Housing Association and Centre for Accessible Environments)',
    isbn = '9781915722355',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00404',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: same source as REF-00404 (Inclusive Housing Design Guide 2024). REF-00437 cites the threshold-provisions section specifically; may be intentional section-level multi-citation or duplicate — owner review. Web-search verified.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified; potential duplicate of REF-00404',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00437';

-- REF-00378: Adaptations Without Delay
UPDATE evidence_sources SET
    pub_title = 'Adaptations without delay: A guide to planning and delivering adaptations differently',
    pub_year = 2019,
    first_author_last = 'Russell',
    first_author_first = 'Rachel',
    is_corporate_primary = 0,
    author_display = 'Russell, R.; Walker, M.; Copeman, I.; Porteus, J.',
    author_count = 4,
    author_count_is_complete = 1,
    publisher = 'Royal College of Occupational Therapists (RCOT) and Housing Learning & Improvement Network (Housing LIN)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: web-search verified via Housing LIN + RCOT + Foundations UK. Published June 2019 by RCOT, prepared by Housing LIN. Authors: Russell R., Walker M., Copeman I., Porteus J. Supersedes 2006 Minor Adaptations Without Delay guide. Available at housinglin.org.uk/_assets/Resources/Housing/Support_materials/Other_reports_and_guidance/Adaptations-Without-Delay.pdf. Per DR-2026-05-18 statutory protocol.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00378';

-- REF-00053: Housing Adaptations Without Delay — same source as REF-00378
UPDATE evidence_sources SET
    pub_title = 'Adaptations without delay: A guide to planning and delivering adaptations differently',
    pub_year = 2019,
    first_author_last = 'Russell',
    first_author_first = 'Rachel',
    is_corporate_primary = 0,
    author_display = 'Russell, R.; Walker, M.; Copeman, I.; Porteus, J.',
    author_count = 4,
    author_count_is_complete = 1,
    publisher = 'Royal College of Occupational Therapists (RCOT) and Housing Learning & Improvement Network (Housing LIN)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00378',
    metadata_integrity_detail = 'uk-guidelines-batch-1 2026-05-21T04:00:00Z: same source as REF-00378 (Adaptations Without Delay 2019). Stored title variant "Housing Adaptations Without Delay" appears to be a paraphrase; canonical title is "Adaptations without delay". Owner: merge into REF-00378 or keep separate.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T04:00:00Z uk-guidelines-batch-1] web-search verified; potential duplicate of REF-00378',
    updated_at = '2026-05-21T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00053';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
