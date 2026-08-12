-- data_20260521074000_int_reports_batch_7.sql
--
-- INT reports batch 7: 3 UN human rights documents on CRPD accessibility/independent-living.
-- Per DR-2026-05-18 statutory-metadata-completeness gray-lit / regulatory protocol.
--
-- REF-00156: General Comment No. 2 (2014) on Article 9 Accessibility (CRPD/C/GC/2)
-- REF-00157: General Comment No. 5 (2017) on Article 19 Independent Living (CRPD/C/GC/5)
-- REF-00158: IDA Compilation of CRPD Committee Concluding Observations on Article 9

BEGIN TRANSACTION;

-- REF-00156: CRPD General Comment No. 2 on Article 9 (Accessibility)
UPDATE evidence_sources SET
    pub_title = 'General comment No. 2 (2014) — Article 9: Accessibility',
    pub_year = 2014,
    first_author_last = 'UN Committee on the Rights of Persons with Disabilities',
    is_corporate_primary = 1,
    author_display = 'UN Committee on the Rights of Persons with Disabilities (CRPD Committee)',
    publisher = 'United Nations Office of the High Commissioner for Human Rights (OHCHR)',
    standard_number = 'CRPD/C/GC/2',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-7 2026-05-21T07:40:00Z: web-search verified via ohchr.org + digitallibrary.un.org + WHO MiNDbank. Adopted at the Committee''s 11th session, 31 March-11 April 2014; final version released 22 May 2014. UN document number CRPD/C/GC/2. First of two general comments adopted by the CRPD Committee (alongside GC1 on Article 12). Available in EN/FR/ES/RU/AR/ZH from OHCHR. Defines accessibility as ex ante duty, unconditional obligation, precondition for equal participation. Cross-references CRPD Articles 21, 24, 25, 27, 29, 30.',
    url = 'https://www.ohchr.org/en/documents/general-comments-and-recommendations/general-comment-no-2-article-9-accessibility-adopted',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ohchr-official',
    last_verified_at = '2026-05-21T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:40:00Z int-reports-batch-7] web-search verified',
    updated_at = '2026-05-21T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00156';

-- REF-00157: CRPD General Comment No. 5 on Article 19 (Independent Living)
UPDATE evidence_sources SET
    pub_title = 'General comment No. 5 (2017) on living independently and being included in the community',
    pub_year = 2017,
    first_author_last = 'UN Committee on the Rights of Persons with Disabilities',
    is_corporate_primary = 1,
    author_display = 'UN Committee on the Rights of Persons with Disabilities (CRPD Committee)',
    publisher = 'United Nations Office of the High Commissioner for Human Rights (OHCHR)',
    standard_number = 'CRPD/C/GC/5',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-7 2026-05-21T07:40:00Z: web-search verified via digitallibrary.un.org + ScienceDirect Bartlett 2017 review + Better Care Network. Adopted August 2017; released Geneva, 27 October 2017. UN document number CRPD/C/GC/5. Fifth general comment adopted by the CRPD Committee. Available in EN/FR/ES/RU/AR/ZH from UN Digital Library. Addresses Article 19 right to live independently and be included in the community; rejects family-like institutions as substitute for family care; defines deinstitutionalization obligations.',
    url = 'https://digitallibrary.un.org/record/1311739',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+un-digital-library',
    last_verified_at = '2026-05-21T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:40:00Z int-reports-batch-7] web-search verified',
    updated_at = '2026-05-21T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00157';

-- REF-00158: IDA Compilation
UPDATE evidence_sources SET
    pub_title = 'Compilation of CRPD Committee Concluding Observations on Article 9 — Accessibility',
    first_author_last = 'International Disability Alliance',
    is_corporate_primary = 1,
    author_display = 'International Disability Alliance (IDA)',
    publisher = 'International Disability Alliance (IDA)',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-7 2026-05-21T07:40:00Z: web-search verified via internationaldisabilityalliance.org. IDA-maintained compendium of the CRPD Committee''s Concluding Observations on State Party reports under Article 9 (Accessibility), aggregating 100+ countries. Living document updated periodically by IDA. Companion to IDA''s Article 19 compilation and other Article-by-Article compendia. Year unknown — IDA does not date the master compilation.',
    url = 'https://www.internationaldisabilityalliance.org/sites/default/files/article_9_crpd_.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ida-official',
    last_verified_at = '2026-05-21T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:40:00Z int-reports-batch-7] web-search verified',
    updated_at = '2026-05-21T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00158';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
