-- data_20260521031500_revert_ref00731_duplicate.sql
-- Companion to data_20260521030000_multi_source_recovery.sql.
-- D01 audit caught the unintended duplicate DOI on REF-00731 (same canonical
-- DOI as REF-00260 — both Szanton 2019 JAMA Internal Medicine). Reverting
-- REF-00731 to AUTHOR-TITLE-ONLY (its prior state) so owner can decide whether
-- to merge into REF-00260 or upgrade separately. REF-00260 keeps the canonical
-- identifier; REF-00731 holds its forensic "displaced from REF-00150" marker
-- and now ALSO holds the explicit duplicate-of-REF-00260 marker so the owner
-- queue is unambiguous.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    doi = NULL,
    journal_name = NULL,
    pub_title = '$2,825/participant home modification',
    pub_year = 2019,
    first_author_last = 'Szanton',
    first_author_first = 'S.',
    volume = NULL,
    issue = NULL,
    pages_start = NULL,
    pages_end = NULL,
    publisher = NULL,
    issn = NULL,
    metadata_quality = 'AUTHOR-TITLE-ONLY',
    verification_status = NULL,
    doi_resolution_outcome = NULL,
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00260',
    metadata_integrity_detail = 'Displaced from REF-00150 by full-DB-audit 2026-05-21T00:00:00Z. Identified as duplicate of REF-00260 via multi-source recovery probe (both resolve to Szanton 2019 JAMA Int Med CAPABLE RCT 10.1001/jamainternmed.2018.6026). Reverted to AUTHOR-TITLE-ONLY pending owner merge decision — REF-00260 now carries the canonical metadata; REF-00731 should either be merged into REF-00260 (preserving REF-00260 slug link) or removed.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T03:15:00Z multi-source-recovery] reverted to ATO; explicit duplicate flag for owner queue',
    updated_at = '2026-05-21T03:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00731';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
