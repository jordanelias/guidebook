-- data_20260518045500_publisher_backfill_bb93_sbi_guide_acoustique.sql
--
-- Pre-flight to data_20260518050000_promote_statutory_metadata.sql.
-- Three statutory documents linked to room-acoustic-performance carry no
-- standard_number because their issuing tradition does not assign one in the
-- ISO/DIN sense (publication-series identifiers, ministerial guides).
-- Backfill publisher field so DR-2026-05-18 criterion 6 is satisfied via
-- the publisher branch rather than the standard_number branch.
--
-- All three values web-verifiable against issuing-body catalog pages.

-- REF-00562 BB93:2015 — UK Building Bulletin 93
UPDATE evidence_sources
SET publisher = 'UK Department for Education',
    standard_number = 'Building Bulletin 93 (2015)',
    verification_note = COALESCE(verification_note || char(10) || '---' || char(10), '')
        || '[session_2026-05-17-pilot-pass-3-blocker-resolution 2026-05-18] '
        || 'Publisher backfilled to UK Department for Education (issuing body for Building Bulletin series). '
        || 'Standard_number set to publication-series identifier "Building Bulletin 93 (2015)" — '
        || 'BB series is not ISO/DIN-formal but is the canonical UK schools-acoustics identifier. '
        || 'Pre-flight to DR-2026-05-18 statutory promotion.',
    updated_at = '2026-05-18 04:55',
    updated_by_session = 'session_2026-05-17-pilot-pass-3-blocker-resolution'
WHERE ref_id = 'REF-00562';

-- REF-00575 SBi-anvisning 218 — Danish Building Research Institute, school acoustics
-- Also missing pub_year (per earlier audit). Backfill both.
UPDATE evidence_sources
SET publisher = 'Statens Byggeforskningsinstitut (Aalborg University)',
    pub_year = 2008,
    verification_note = COALESCE(verification_note || char(10) || '---' || char(10), '')
        || '[session_2026-05-17-pilot-pass-3-blocker-resolution 2026-05-18] '
        || 'Publisher backfilled to Statens Byggeforskningsinstitut (SBi), now part of Aalborg University. '
        || 'pub_year backfilled to 2008 (SBi-anvisning 218 publication year). '
        || 'Pre-flight to DR-2026-05-18 statutory promotion.',
    updated_at = '2026-05-18 04:55',
    updated_by_session = 'session_2026-05-17-pilot-pass-3-blocker-resolution'
WHERE ref_id = 'REF-00575';

-- REF-00572 Guide acoustique pour personnes malentendantes — French ministerial guide
UPDATE evidence_sources
SET publisher = 'Ministere de la Sante (France)',
    verification_note = COALESCE(verification_note || char(10) || '---' || char(10), '')
        || '[session_2026-05-17-pilot-pass-3-blocker-resolution 2026-05-18] '
        || 'Publisher backfilled to Ministere de la Sante (France) — ministerial guide for hearing accessibility. '
        || 'No formal standard_number; ministerial guidance documents are identified by title + ministry. '
        || 'Pre-flight to DR-2026-05-18 statutory promotion.',
    updated_at = '2026-05-18 04:55',
    updated_by_session = 'session_2026-05-17-pilot-pass-3-blocker-resolution'
WHERE ref_id = 'REF-00572';

INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'publisher_backfill_bb93_sbi_guide_acoustique_2026-05-18',
    '2026-05-18 04:55',
    'update_REF_00562_REF_00575_REF_00572_publisher_fields_for_DR_2026_05_18_pre_flight',
    'session_2026-05-17-pilot-pass-3-blocker-resolution',
    'Publisher backfill for three statutory documents (BB93, SBi-anvisning 218, French Guide acoustique) that lack ISO/DIN-formal standard numbers but are issued by named authoritative bodies. Pre-flight to DR-2026-05-18 statutory metadata promotion. Unblocks UK + DK/NO/SE/FI + FR jurisdiction-comparison cells in pilot Pass 3.'
);
