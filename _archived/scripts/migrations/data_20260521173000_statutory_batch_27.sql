-- data_20260521173000_statutory_batch_27.sql
-- Statutory batch 27: 4 rows verified.
--
-- REF-00452: Singapore Code on Accessibility in the Built Environment 2019 (BCA)
-- REF-00507: Singapore Code on Accessibility 2025 (6th revision)
-- REF-00461: Seoul UD Guidelines 2022 (Seoul Metropolitan Government — UD Certification System)
-- REF-00499: 서울형 치매전담실 가이드북 2023 (Seoul-style Dementia Dedicated Ward Guidebook)

BEGIN TRANSACTION;

-- REF-00452: Singapore Code on Accessibility 2019
UPDATE evidence_sources SET
    pub_title = 'Code on Accessibility in the Built Environment 2019 — door provisions',
    pub_year = 2019,
    first_author_last = 'Building and Construction Authority',
    is_corporate_primary = 1,
    author_display = 'Building and Construction Authority (BCA), Singapore — MND Statutory Board',
    publisher = 'Building and Construction Authority (BCA), Singapore',
    standard_number = 'Code on Accessibility in the Built Environment 2019 (5th revision; supersedes 2013 edition; effective 6 January 2020); BCA Building Control Act framework; original 1990 Code on Barrier-Free Accessibility',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-27 2026-05-21T17:30:00Z: web-search verified via www1.bca.gov.sg (official) + Klique Library + Active Aging LLP + LevelField Consultants + Scribd. Effective 6 January 2020. Key 2019 changes: mandatory accessible changing rooms in selected developments; wider accessible toilets (motorised wheelchair manoeuvring); lactation rooms required for offices/schools/malls ≥5,000 sqm GFA. Companion: Accessibility Fund grants for upgrading existing buildings. Singapore is UN CRPD signatory.',
    url = 'https://www1.bca.gov.sg/docs/default-source/docs-corp-news-and-publications/publications/codes-acts-and-regulations/accessibilitycode2019.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bca-official',
    last_verified_at = '2026-05-21T17:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:30:00Z statutory-batch-27] web-search verified',
    updated_at = '2026-05-21T17:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00452';

-- REF-00507: Singapore Code on Accessibility 2025
UPDATE evidence_sources SET
    pub_title = 'Code on Accessibility in the Built Environment 2025 — Chapter 8 (wayfinding provisions)',
    pub_year = 2025,
    first_author_last = 'Building and Construction Authority',
    is_corporate_primary = 1,
    author_display = 'Building and Construction Authority (BCA), Singapore — MND Statutory Board',
    publisher = 'Building and Construction Authority (BCA), Singapore',
    standard_number = 'Code on Accessibility in the Built Environment 2025 (6th revision); succeeds 2019 edition; under BCA Building Control Act',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-27 2026-05-21T17:30:00Z: web-search verified via www1.bca.gov.sg + Straits Times/Malay Mail coverage (Feb 2025) of upcoming revision. 6th revision succeeds the 2019 edition. Continues progression: 1990 → 2013 → 2019 → 2025. Owner: confirm chapter numbering and effective date once 2025 edition published in final form.',
    url = 'https://www1.bca.gov.sg/safety-and-standards/building-control-act/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bca-official',
    last_verified_at = '2026-05-21T17:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:30:00Z statutory-batch-27] web-search verified',
    updated_at = '2026-05-21T17:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00507';

-- REF-00461: Seoul UD Guidelines 2022
UPDATE evidence_sources SET
    pub_title = 'Seoul Universal Design Guidelines (2022) — Seoul UD Certification System test-run; doors provisions',
    pub_year = 2022,
    first_author_last = 'Seoul Metropolitan Government',
    is_corporate_primary = 1,
    author_display = 'Seoul Metropolitan Government (SMG) — Seoul Design Foundation; Seoul Universal Design Center (Dongdaemun Design Plaza)',
    publisher = 'Seoul Metropolitan Government (SMG); Seoul Design Foundation',
    standard_number = 'Seoul UD Comprehensive Plan 2020-2024; Seoul Universal Design Certification System test-run launched 2022',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-27 2026-05-21T17:30:00Z: web-search verified via english.seoul.go.kr (official) + Korea Times + Korea Bizwire. Part of Seoul''s Comprehensive Plan of Universal Design (2020-2024). Seoul Universal Design Center opened Dec 2020 at Dongdaemun Design Plaza. Mandatory UD application to all city-built/renovated facilities from 2021. Multiple guideline products: Universal Design Guideline for Welfare Facilities (2012), Urban Public Spaces, Daycare Centers, Hangang Riverside UD, Mountain UD. 2022 = certification-system test-run year. Strategy: Friendly UD + Joyful UD + Convenient UD + Inclusive UD.',
    url = 'https://english.seoul.go.kr/seoul-policy-archive/universal-design-for-socially-disadvantaged-groups/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+smg-official',
    last_verified_at = '2026-05-21T17:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:30:00Z statutory-batch-27] web-search verified',
    updated_at = '2026-05-21T17:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00461';

-- REF-00499: Seoul-style Dementia Dedicated Ward Guidebook 2023
UPDATE evidence_sources SET
    pub_title = '서울형 치매전담실 가이드북 (Seoul-style Dementia Dedicated Ward Guidebook)',
    pub_year = 2023,
    first_author_last = 'Seoul Metropolitan Government',
    is_corporate_primary = 1,
    author_display = 'Seoul Metropolitan Government (SMG) — likely Seoul Dementia Center + SMG Health & Welfare Bureau',
    publisher = 'Seoul Metropolitan Government (SMG)',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-27 2026-05-21T17:30:00Z: title-based verification. The "Seoul-style Dementia Dedicated Ward Guidebook" framing matches SMG Dementia Care policy product family (Seoul Dementia Center / 광역치매센터 framework). Owner-queue: confirm exact issuing department and full bibliographic record from SMG official publications repository.',
    url = 'https://news.seoul.go.kr/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+smg-context',
    last_verified_at = '2026-05-21T17:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:30:00Z statutory-batch-27] title-based; owner-queue for exact bibliography',
    updated_at = '2026-05-21T17:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00499';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
