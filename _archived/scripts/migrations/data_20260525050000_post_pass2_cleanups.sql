-- data_20260525050000_post_pass2_cleanups.sql
-- DR-2026-05-24 Pass 2 post-completion cleanups.
-- 1. Correct NZS 4121:2001 (MOB-23) audit finding — verified still operative
--    per NZ Building Act 2004 §119 / D1/AS1 Acceptable Solution (NZ MoE March 2025).
-- 2. Resolve PAS 6463:2022 duplication in MHB slug — remove MHB-05 (T5-classified
--    duplicate of MHB-06 T4-classified). Standard is a T4 BSI PAS.
-- 3. Close GAP-292 (RAP-13 Kotloski rat-kindling misclassification) — remove the
--    source_slug_link row that misclassifies the rat-kindling paper as
--    room-acoustic-performance evidence. The supersession_check row for RAP-13
--    is retained as audit history (it records that the misclassification was
--    surfaced during audit).
-- 4. Open new gap row for the Steinfeld 2010 powered-mobility demographic-shift
--    evidence concern surfaced during MOB Pass-2 audit.
-- 5. MHB-10 Price 2024 dementia encyclopedia entry flagged but not auto-removed —
--    requires owner review to confirm misclassification before source_slug_links
--    surgery.

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ────────────────────────────────────────────────────────────────────────
-- 1. NZS 4121:2001 (MOB-23) audit note correction
-- ────────────────────────────────────────────────────────────────────────
-- Update the supersession_check note to reflect verified-current status.
UPDATE supersession_check
   SET notes = 'NZS 4121:2001 New Zealand design for access and mobility. Tier-6 statutory code — out-of-scope per DR §Out-of-scope for supersession determination. POST-AUDIT WEB VERIFICATION (2026-05-25) confirmed standard remains operative per NZ Building Act 2004 §119 / D1/AS1 Acceptable Solution; cited in NZ Ministry of Education March 2025 guidance "Improving Accessibility at Schools" and Auckland Council Unitary Plan 2022. Age (24 years) does not indicate supersession in this case. Skill-file lesson recorded.'
 WHERE slug = 'mobility-built-environment'
   AND local_ref_id = 'MOB-23';

-- ────────────────────────────────────────────────────────────────────────
-- 2. PAS 6463:2022 duplication — remove MHB-05 source_slug_link
-- ────────────────────────────────────────────────────────────────────────
-- MHB-05 (REF-00094) and MHB-06 (REF-00050) both reference PAS 6463:2022.
-- Canonical classification: T4 standard_eb (BSI PAS is international-tier-equivalent).
-- MHB-06 = REF-00050 is the canonical row.
-- Remove the MHB-05 source_slug_link.
-- The MHB-05 evidence_sources row (REF-00094) is RETAINED but should not be
-- linked to mental-health-built-environment under the duplicate local_ref_id.
-- The supersession_check row for MHB-05 is retained for audit history.
DELETE FROM source_slug_links
 WHERE slug = 'mental-health-built-environment'
   AND local_ref_id = 'MHB-05';

-- ────────────────────────────────────────────────────────────────────────
-- 3. Close GAP-292 — remove RAP-13 misclassification
-- ────────────────────────────────────────────────────────────────────────
-- RAP-13 (REF-00571 Kotloski 2020 rat-kindling neuroscience paper) was
-- misclassified as room-acoustic-performance evidence. Surfaced during RAP
-- Pass-2 audit and noted in GAP-292. The audit logged the misclassification
-- as current_best with explicit flagging for cleanup (see skill §8 edge case).
-- Now removing the source_slug_link. The supersession_check row remains as
-- audit history (records that the misclassification was surfaced).
-- The evidence_sources row for REF-00571 is RETAINED (not deleted) because
-- it is a legitimate biomedical reference; it simply doesn't belong in the
-- room-acoustic-performance slug.
DELETE FROM source_slug_links
 WHERE slug = 'room-acoustic-performance'
   AND local_ref_id = 'RAP-13';

-- Close GAP-292.
UPDATE gaps
   SET status = 'CLOSED-FIXED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) || 'CLOSED 2026-05-25 by data_20260525050000_post_pass2_cleanups.sql: source_slug_link removed for (room-acoustic-performance, RAP-13). The Kotloski 2020 evidence_sources row is retained as a valid biomedical reference unattached to this slug. The supersession_check row for RAP-13 is retained as audit history.'
 WHERE gap_id = 'GAP-292';

-- ────────────────────────────────────────────────────────────────────────
-- 4. New gap: Steinfeld 2010 powered-mobility demographic-shift concern
-- ────────────────────────────────────────────────────────────────────────
-- Insert a new gap row for the evidence-base concern surfaced during MOB
-- Pass-2 audit. Not a supersession finding (no replacing study exists) but
-- a real concern that 2010 manual-wheelchair-derived anthropometric
-- dimensions may not capture current powered-mobility user demographics.
INSERT INTO gaps (gap_id, category, priority, status, skill, section, description, created_at, created_by_session, updated_at, updated_by_session)
VALUES (
    'GAP-295',
    'CD',
    'P2',
    'OPEN',
    'supersession-audit',
    'evidence-gap-register',
    'Steinfeld 2010 anthropometric basis for wheeled mobility (REF-00059, REF-00060 / MOB-01, MOB-02 in mobility-built-environment slug) is foundational but the wheelchair-user demographic has shifted materially since 2010: heavier and larger powered chairs, increased scooter adoption, broader age range of users, and changing co-morbidity profiles. No comprehensive replacement anthropometric study has been identified in supersession audit 2026-05-25. The anchor remains current best by absence of replacement, but the parameter values it informs (clear floor widths, manoeuvring spaces, turning radii) may understate current need. Surfaced as a structural evidence gap rather than a supersession finding. Recommend prioritizing for gap-driven mining in revised B.11 protocol once gap register is operationalized.',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

-- ────────────────────────────────────────────────────────────────────────
-- 5. MHB-10 Price 2024 — note flagged for owner review (not auto-removed)
-- ────────────────────────────────────────────────────────────────────────
-- Update the supersession_check note to flag the possible misclassification
-- without removing the source_slug_link. Price 2024 is a Sage encyclopedia
-- entry on "Dementia" (doi:10.4135/9781071891414.n126). It may be valid in
-- mental-health-built-environment if it covers dementia-care-setting topics
-- within mental-health BE scope, or it may belong in cognitive-wayfinding-design.
-- Owner review needed.
UPDATE supersession_check
   SET notes = notes || char(10) || char(10) || 'POST-AUDIT (2026-05-25): Possible misclassification confirmed as open question. Encyclopedia entry on "Dementia" in mental-health slug — could belong in cognitive-wayfinding-design slug. NOT auto-removed pending owner review of the actual entry content. If review confirms misclassification, follow GAP-292 / RAP-13 pattern: remove source_slug_link, retain evidence_sources row, retain supersession_check as audit history.'
 WHERE slug = 'mental-health-built-environment'
   AND local_ref_id = 'MHB-10';

COMMIT;
