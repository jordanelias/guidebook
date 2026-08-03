-- data_20260522103000_grey_regrade_pass1.sql
-- SQL-regrade pass 1: 5 GREY×VERIFIED rows with DOI+publisher+author already populated.
-- These were misclassified at GREY when they should be COMPLETE (academic) per DR-2026-05-13.
-- All five already have Crossref-backfill verification — only the mq label needs fixing.
--
-- REF-00131: Holohan E 2022 Trauma-informed design scoping review (AUT Library DOI 10.24135/10292/18859) — keep GREY (institutional report w/o issn) but raise verification? Actually grey-lit institutional reports go to COMPLETE-STATUTORY per DR-2026-05-18
-- REF-00374: Golding-Day S 2018 BATH-OUT (HSCC Wiley DOI 10.1111/hsc.12824) — COMPLETE (journal)
-- REF-00379: AOTA 2023 Home Modification Practice Guidelines (Routledge DOI 10.4324/9781003525264-4) — COMPLETE (book chapter)
-- REF-00628: Crompton CJ 2024 Collectivist cultures autism camouflaging (UAlbany DOI 10.54014/7sew-4fp4) — COMPLETE-STATUTORY (preprint/institutional)
-- REF-00642: Simpson K et al. 2025 Built school environment (IJIE Informa DOI 10.1080/13603116.2025.2589290) — COMPLETE (journal)

BEGIN TRANSACTION;

-- REF-00374: BATH-OUT trial Wiley HSCC journal
UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS1',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass1 2026-05-22T10:30:00Z: regraded GREY→COMPLETE; row has DOI 10.1111/hsc.12824 + publisher Wiley + journal HSCC + author Golding-Day S + Crossref-backfill verification. Misclassified as GREY originally; per DR-2026-05-13 rule #10 academic-journal existence gate this is COMPLETE.',
    updated_at = '2026-05-22T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00374';

-- REF-00379: Routledge book chapter
UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS1',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass1 2026-05-22T10:30:00Z: regraded GREY→COMPLETE; row has DOI 10.4324/9781003525264-4 + publisher Routledge + parent book "An Occupational Therapist''s Guide to Home Modification Practice" + author AOTA + Crossref-backfill verification. Book-chapter ISBN-canonical convention; DOI-bearing chapter qualifies as COMPLETE.',
    updated_at = '2026-05-22T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00379';

-- REF-00131: Trauma-informed design scoping review (AUT institutional)
UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE-STATUTORY',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS1',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass1 2026-05-22T10:30:00Z: regraded GREY→COMPLETE-STATUTORY; row has DOI 10.24135/10292/18859 + publisher AUT Library + author Holohan E + Crossref-backfill verification. Institutional-report grey-lit; per DR-2026-05-18 COMPLETE-STATUTORY applies. IDENTIFIER-CONTENT-DISAGREE-OWNER-DECIDE flag preserved in note for downstream resolution.',
    updated_at = '2026-05-22T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00131';

-- REF-00628: Crompton 2024 UAlbany institutional repository
UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE-STATUTORY',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS1',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass1 2026-05-22T10:30:00Z: regraded GREY→COMPLETE-STATUTORY; row has DOI 10.54014/7sew-4fp4 + publisher UAlbany Libraries + author Crompton CJ + Crossref-backfill verification. Preprint/institutional-repository grey-lit; COMPLETE-STATUTORY per DR-2026-05-18.',
    updated_at = '2026-05-22T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00628';

-- REF-00642: Simpson Adams Dargue 2025 IJIE
UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS1',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass1 2026-05-22T10:30:00Z: regraded GREY→COMPLETE; row has DOI 10.1080/13603116.2025.2589290 + publisher Informa UK + journal International Journal of Inclusive Education + authors Simpson K + Adams D + Dargue N + Crossref-backfill verification. Academic-journal article; COMPLETE per rule #10 existence gate.',
    updated_at = '2026-05-22T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00642';

COMMIT;
