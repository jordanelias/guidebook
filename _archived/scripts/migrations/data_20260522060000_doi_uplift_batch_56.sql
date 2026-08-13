-- data_20260522060000_doi_uplift_batch_56.sql
-- DOI uplift batch 56: 2 rows verified.
--
-- REF-00591: Allen 1988 — Hospital and Community Psychiatry (now Psychiatric Services) — DOI 10.1176/ps.39.2.140 — JOURNAL+TOPIC CORRECTION from AJOT
-- REF-00531: Canada LRV 30% — Accessibility Standards Canada CAN-ASC-2.4 Wayfinding+Signage clause 10

BEGIN TRANSACTION;

-- REF-00591: Allen 1988 Psychiatric Services (JOURNAL CORRECTION)
UPDATE evidence_sources SET
    pub_title = 'Occupational Therapy: Functional Assessment of the Severity of Mental Disorders',
    pub_year = 1988,
    first_author_last = 'Allen',
    first_author_first = 'CK',
    is_corporate_primary = 0,
    author_display = 'Allen CK (Claudia K)',
    publisher = 'American Psychiatric Association (APA); Hospital and Community Psychiatry (renamed Psychiatric Services 1995)',
    journal_name = 'Hospital and Community Psychiatry',
    journal_abbrev = 'Hosp Community Psychiatry',
    doi = '10.1176/ps.39.2.140',
    issn = '0022-1597',
    volume = '39',
    issue = '2',
    pages_start = '140',
    pages_end = '142',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTION-FROM-AJOT',
    metadata_integrity_detail = 'doi-uplift-batch-56 2026-05-22T06:00:00Z: Crossref-confirmed via API search "Claudia Allen 1988". Prior DB cited "Am J Occup Ther" but actual journal is *Hospital and Community Psychiatry* (renamed Psychiatric Services in 1995). DOI 10.1176/ps.39.2.140 resolves to American Psychiatric Association archive. Companion: Allen Cognitive Disabilities Model (CDM) developed in psychiatric inpatient settings; ACLS-5 lacing-stitch screening; CD Model 6 cognitive levels expanded to 26 Modes of Performance (Allen 1992 with Earhart CA). Foundational CDM reference.',
    url = 'https://doi.org/10.1176/ps.39.2.140',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+ot-innovations+statpearls',
    last_verified_at = '2026-05-22T06:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T06:00:00Z doi-uplift-batch-56] DOI resolved + journal corrected AJOT→Hosp Community Psychiatry',
    updated_at = '2026-05-22T06:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00591';

-- REF-00531: Canada LRV 30% — Accessibility Standards Canada CAN-ASC-2.4
UPDATE evidence_sources SET
    pub_title = 'Light Reflectance Value (LRV) minimum 30-point contrast — multi-jurisdictional design standard for adjacent-surface luminance contrast (Accessibility Standards Canada CAN-ASC-2.4 Wayfinding and Signage clause 10 + BS 8300-2:2018 + AS 1428.1:2009)',
    pub_year = 2024,
    first_author_last = 'Accessibility Standards Canada',
    is_corporate_primary = 1,
    author_display = 'Accessibility Standards Canada (Normes d''accessibilité Canada, ASC/NAC) + UK BSI (BS 8300-2:2018) + Standards Australia (AS 1428.1:2009)',
    publisher = 'Accessibility Standards Canada (ASC), Gatineau QC — Government of Canada; companion BSI (London) + Standards Australia (Sydney)',
    standard_number = 'CAN-ASC-2.4 Wayfinding and Signage (Accessibility Standards Canada) clause 10 General requirements for lighting and contrast — Table 1 minimum luminance contrast values for matte surfaces; large surfaces ≥40 LRV light surface + ≥30% Michelson + ≥45% Weber; hazards ≥50 LRV + ≥60% Michelson + ≥75% Weber; text ≥70 LRV + ≥60% Michelson + ≥75% Weber. Companion standards: BS 8300-2:2018 Code of practice (UK 30-point LRV minimum); AS 1428.1:2009 + AS 1428.4.1:2009 (Australia 30% luminance contrast minimum via Bowman-Sapolinski equation Y1-Y2). Underlying: Accessible Canada Act (S.C. 2019, c. 10) + UK Equality Act 2010 + Australia DDA + AS/NZS framework. Argument: 30% is regulatory FLOOR, not functional optimum — Canadian Museum for Human Rights (CMHR) Inclusive and Accessible Design Guidelines uses 70% LRV difference for text legibility as best practice.',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'doi-uplift-batch-56 2026-05-22T06:00:00Z: web-search verified via accessible.canada.ca (official ASC public-comment draft) + id.humanrights.ca (CMHR design standards) + grestec.co.uk + supawood.com.au + formica.com + classic-arch.com + catflooringaccessories.com + fitzroyoflondon.com + tredsafe.com. CAN-ASC-2.4 currently in public consultation (2024); BS 8300-2:2018 is the operative UK code; AS 1428.1:2009 is the operative AU code. The 30-point/30% threshold is consistent across jurisdictions; CMHR adopts 70% as enhanced best-practice for typographic installations.',
    url = 'https://accessible.canada.ca/creating-accessibility-standards/can-asc-24-wayfinding-and-signage/10-general-requirements-lighting-and-contrast',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+accessible-canada-official+cmhr+multi-jurisdiction',
    last_verified_at = '2026-05-22T06:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T06:00:00Z doi-uplift-batch-56] multi-jurisdiction standard verified',
    updated_at = '2026-05-22T06:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00531';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
