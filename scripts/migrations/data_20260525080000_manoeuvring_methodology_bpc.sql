-- data_20260525080000_manoeuvring_methodology_bpc.sql
-- Registers the new manoeuvring-footprint-vs-turning-radius-methodology BPC,
-- adds the two evidence_sources rows it depends on that were not yet in DB
-- (Vergara 2023 biomechanics; Steinfeld 2006 RESNA empirical envelope), links
-- them to the new slug, and closes GAP-272.
--
-- Owner directive 2026-05-25: "yes, but you have to include a discussion about
-- why turning radius is disingenuous compared to swept path/turning maneouvres".
-- The methodology BPC at references/bpc/frameworks-and-methodology/manoeuvring-
-- footprint-vs-turning-radius-methodology.md is the discussion. This migration
-- attaches the supporting evidence rows and registers the slug.
--
-- Per governance/tier-system.md §3 (best practice ≠ convergence), the deprecation
-- of "turning radius / turning circle" as a Guidebook-authored parameter name is
-- now enshrined alongside the T2-sr_meta canonicalization from 2026-05-25.

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ────────────────────────────────────────────────────────────────────────
-- 1. Add Vergara et al. 2023 wheelchair-turning-biomechanics paper
-- ────────────────────────────────────────────────────────────────────────
INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, is_corporate_primary, author_display,
    pub_year, pub_title, journal_name, journal_abbrev, volume,
    doi, pmid, pmcid, language, lang_detected, lang_detection_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status,
    derivation_chain, created_at, created_by_session, updated_at, updated_by_session
)
VALUES (
    'REF-00736', 'journal_article', NULL, 0,
    'Vergara', 'Mariana', 0, 'Vergara M, van der Slikke RMA, et al.',
    2023, 'Biomechanics of wheelchair turning manoeuvres: novel insights into wheelchair propulsion',
    'Frontiers in Sports and Active Living', 'Front Sports Active Living', NULL,
    '10.3389/fspor.2023.1127514', '37383064', 'PMC10293636', 'eng', 'eng', 'manual',
    1, 'clinical', 'INT',
    'COMPLETE', 'VERIFIED',
    'Identified via PubMed search "wheelchair manoeuvring space anthropometry clear floor area" and confirmed via direct full-text retrieval from PMC10293636. n=10 able-bodied novice users; instrumented ultra-light wheelchair (Quickie); 240 Hz force-and-torque-sensing wheel + 100 Hz 7-camera Vicon kinematics. Documents spin-turn dominance (97% of 90° corridor-entry turns); peak braking force 15.3× SSSFP; force impulse 4.5× SSSFP; corroborates ~900 turns/day daily-living frequency from Sonenblum et al. data. Direct Tier 1 biomechanical evidence for the manoeuvring-footprint-vs-turning-radius-methodology BPC.',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

-- ────────────────────────────────────────────────────────────────────────
-- 2. Add Steinfeld 2006 RESNA paper (no DOI; conference proceedings)
-- ────────────────────────────────────────────────────────────────────────
-- This is the paper that the existing MOB BPC cites for the 2400mm IDEA+BS8300
-- entire-sample 180° turn envelope and the 1925mm UDI sub-sample envelope.
-- It is cited inline in MOB and accessible-circulation-geometry but has no
-- evidence_sources row. Added here for the methodology BPC; will need
-- additional bibliographic completion (page numbers, exact title) at next
-- verification pass.
INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, is_corporate_primary, author_display,
    pub_year, pub_title, publisher, language, lang_detected, lang_detection_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status,
    derivation_chain, notes,
    created_at, created_by_session, updated_at, updated_by_session
)
VALUES (
    'REF-00737', 'conference_paper', NULL, 0,
    'Steinfeld', 'Edward', 0, 'Steinfeld E, Maisel J, Feathers D, D''Souza C',
    2006, 'Anthropometry of Wheeled Mobility — IDeA Center / RESNA Annual Conference proceedings',
    'RESNA', 'eng', 'eng', 'manual',
    3, 'clinical', 'US',
    'AUTHOR-TITLE-ONLY', 'UNVERIFIED-1',
    'Cited inline in existing mobility-built-environment.md and accessible-circulation-geometry.md for the empirical envelope values (2400mm IDEA+BS8300 entire-sample 180° turn; 1925mm UDI sub-sample). Not previously in evidence_sources. Added as AUTHOR-TITLE-ONLY pending direct retrieval of the RESNA 2006 conference proceedings volume for full bibliographic completion (exact paper title, page numbers, volume). Does NOT clear PI rule #10 evidence verification gate at AUTHOR-TITLE-ONLY metadata_quality; methodology BPC notes this in §9 bibliographic placeholders.',
    'Bibliographic completion required: this row carries AUTHOR-TITLE-ONLY metadata_quality pending direct retrieval of RESNA 2006 conference proceedings. The companion paper Steinfeld 2010 (REF-00060 / REF-00192) reports overlapping data and is fully verified; until Steinfeld 2006 RESNA is retrieved, the 2400mm and 1925mm values in the methodology BPC should be cross-cited to Steinfeld 2010 where the same data appears.',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

-- ────────────────────────────────────────────────────────────────────────
-- 3a. Add slugs row (must exist before source_slug_links FK can be satisfied)
-- ────────────────────────────────────────────────────────────────────────
INSERT INTO slugs (
    slug, topic_directory, sl_path, bpc_path, status,
    created_at, created_by_session, updated_at, updated_by_session
)
VALUES (
    'manoeuvring-footprint-vs-turning-radius-methodology',
    'frameworks-and-methodology',
    'references/search-log/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md',
    'references/bpc/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md',
    'ACTIVE',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

-- ────────────────────────────────────────────────────────────────────────
-- 3b. Add bpc_metadata row for the new methodology slug
-- ────────────────────────────────────────────────────────────────────────
INSERT INTO bpc_metadata (
    slug, population, evidence_state, last_updated,
    citation_mining_complete, supersession_check_complete, closure_definition_version,
    created_at, created_by_session, updated_at, updated_by_session
)
VALUES (
    'manoeuvring-footprint-vs-turning-radius-methodology',
    'MOB',
    'METHODOLOGY-AUTHORED',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    0, 0, NULL,
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

-- ────────────────────────────────────────────────────────────────────────
-- 4. Add source_slug_links for the methodology BPC's anchors
-- ────────────────────────────────────────────────────────────────────────
INSERT INTO source_slug_links (slug, local_ref_id, ref_id, created_at, created_by_session, updated_at, updated_by_session)
VALUES
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-01', 'REF-00736', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-02', 'REF-00737', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-03', 'REF-00060', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-04', 'REF-00192', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-05', 'REF-00059', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-06', 'REF-00338', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-07', 'REF-00342', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure'),
    ('manoeuvring-footprint-vs-turning-radius-methodology', 'MFM-08', 'REF-00341', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), 'session_2026-05-23-bpc-rewrite-phase-b-closure');

-- ────────────────────────────────────────────────────────────────────────
-- 5. Close GAP-272
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET status = 'CLOSED-FIXED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'CLOSED 2026-05-25 per owner directive "yes, but you have to include a discussion about why ' ||
         'turning radius is disingenuous compared to swept path/turning maneouvres". Resolution: ' ||
         'methodology BPC authored at references/bpc/frameworks-and-methodology/' ||
         'manoeuvring-footprint-vs-turning-radius-methodology.md. Four substantive grounds for the ' ||
         'deprecation enumerated in §2: (1) wheelchairs do not pivot in place (97% spin-turn dominance ' ||
         'per Vergara 2023); (2) footrests and forward-swept geometry excluded by pivot model; ' ||
         '(3) drive systems (MWD/RWD/FWD) produce different swept envelopes; (4) the manoeuvre type ' ||
         'matters (90° entry, 180° within bay, 360° reorientation, transfer turns are all distinct). ' ||
         'Convergence-not-evidence trap (governance/tier-system.md §3) applied to the 1500mm code ' ||
         'convergence — Steinfeld 2010 international-comparison diagnoses the 1970s anthropometric ' ||
         'inheritance. Biomechanical consequence in §6: undersized footprints force inferior spin-turn ' ||
         'manoeuvres with 15× braking force, accumulating upper-limb injury over decades. Parameter-' ||
         'name deprecation table in §5; downstream BPC update queue in §10. 2 new evidence_sources ' ||
         'rows added in this migration: REF-00736 Vergara 2023 (COMPLETE/VERIFIED, doi 10.3389/' ||
         'fspor.2023.1127514) and REF-00737 Steinfeld 2006 RESNA (AUTHOR-TITLE-ONLY pending RESNA ' ||
         'proceedings retrieval).'
 WHERE gap_id = 'GAP-272';

COMMIT;
