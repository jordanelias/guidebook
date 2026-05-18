-- data_20260518050000_promote_statutory_metadata.sql
--
-- Per DR-2026-05-18 statutory-metadata-completeness. Promotes qualifying
-- AUTHOR-TITLE-ONLY rows to new metadata_quality value 'COMPLETE-STATUTORY'.
-- Owner directive 2026-05-18: path A (preserve statutory-vs-academic distinction
-- in queryable form).
--
-- Criteria (DR-2026-05-18 S3.1):
--   1. source_type IN ('standard','guideline')
--   2. author_display non-null/non-empty (issuing body)
--   3. pub_title non-null/non-empty
--   4. pub_year non-null
--   5. jurisdiction non-null/non-empty
--   6. standard_number OR publisher non-null/non-empty
--
-- source_type='report' EXCLUDED (181 rows; many are misclassified academic
-- work routing to separate source_type audit).
--
-- Verification history preserved by appending an audit line to verification_note
-- rather than overwriting. Reversible by audit.

UPDATE evidence_sources
SET metadata_quality = 'COMPLETE-STATUTORY',
    verification_note = COALESCE(verification_note || char(10) || '---' || char(10), '')
        || '[session_2026-05-17-pilot-pass-3-blocker-resolution 2026-05-18] '
        || 'Promoted from metadata_quality=AUTHOR-TITLE-ONLY to COMPLETE-STATUTORY '
        || 'per DR-2026-05-18 statutory-metadata-completeness. '
        || 'Criteria satisfied: source_type IN (standard,guideline); author_display, pub_title, '
        || 'pub_year, jurisdiction all populated; standard_number OR publisher present.',
    updated_at = '2026-05-18 05:00',
    updated_by_session = 'session_2026-05-17-pilot-pass-3-blocker-resolution'
WHERE metadata_quality = 'AUTHOR-TITLE-ONLY'
  AND source_type IN ('standard','guideline')
  AND author_display IS NOT NULL AND author_display <> ''
  AND pub_title IS NOT NULL AND pub_title <> ''
  AND pub_year IS NOT NULL
  AND jurisdiction IS NOT NULL AND jurisdiction <> ''
  AND ((standard_number IS NOT NULL AND standard_number <> '')
       OR (publisher IS NOT NULL AND publisher <> ''));

INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'promote_statutory_metadata_2026-05-18',
    '2026-05-18 05:00',
    'bulk_update_metadata_quality_AUTHOR_TITLE_ONLY_to_COMPLETE_STATUTORY_per_DR_2026_05_18',
    'session_2026-05-17-pilot-pass-3-blocker-resolution',
    'Bulk promotion of statutory documents per DR-2026-05-18. ~231 rows expected (140 standards + 91 guidelines meeting 6-criterion gate). Source_type=report excluded pending separate misclassification audit. Unblocks Phase E.1 pilot Pass 3 (rule #10 reasoning-doc-citations) for jurisdiction-comparison cells.'
);
