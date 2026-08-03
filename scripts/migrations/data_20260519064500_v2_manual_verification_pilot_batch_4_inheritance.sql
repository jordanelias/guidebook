-- data_20260519064500_v2_manual_verification_pilot_batch_4_inheritance.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 4 (inheritance).
-- Per the DR amendment 2026-05-19 (standard-number-inheritance mechanic),
-- rows that share an exact standard_number with a canonical pilot-walked row
-- inherit that row's verification_status without re-probing the catalog.
--
-- Inheritance batch composition (21 rows across 7 standards):
--   NCC 2022           VERIFIED               REF-00416, REF-00548                              (2 AU)
--   RHFAC v4.0         VERIFIED               REF-00210, REF-00410, REF-00470                   (3 CA)
--   TEK17              VERIFIED               REF-00349, REF-00411, REF-00432, REF-00448        (4 NO)
--   NZS 4121:2001      UNVERIFIED-1           REF-00450                                         (1 NZ)
--   NEN 9120:2025      IS-PAYWALL             REF-00433, REF-00466                              (2 NL)
--   NBR 9050:2020      IS-PAYWALL             REF-00208, REF-00414, REF-00435, REF-00456        (4 BR)
--   GB 50763-2012      DEFERRED-V2-AUTOMATED  REF-00359, REF-00375, REF-00462, REF-00475, REF-00510 (5 CN)
--
-- Net writes by status:
--   +9 VERIFIED, +1 UNVERIFIED-1, +6 IS-PAYWALL, +5 DEFERRED-V2-AUTOMATED
-- Net to rule #10 eligible pool: +10 (225 -> 235; 33.6% -> 35.1%).
--
-- verified_by_tool convention: <canonical-tool>-inherited, e.g., 'manual-AU-inherited'.

BEGIN;

-- NCC 2022 inheritance from REF-00146 (manual-AU VERIFIED)
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-AU-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00146 (NCC 2022 AU, manual-AU VERIFIED via ncc.abcb.gov.au) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00416','REF-00548');

-- RHFAC v4.0 inheritance from REF-00117 (manual-CA VERIFIED)
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-CA-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00117 (RHFAC Rating Survey v4.0 CA, manual-CA VERIFIED via rickhansen.com) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00210','REF-00410','REF-00470');

-- TEK17 inheritance from REF-00145 (manual-NO VERIFIED)
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-NO-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00145 (TEK17 NO, manual-NO VERIFIED via dibk.no) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match (TEK17 is year-encoded NO national code, edition 2017).',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00349','REF-00411','REF-00432','REF-00448');

-- NZS 4121:2001 inheritance from REF-00081 (manual-NZ UNVERIFIED-1)
UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-1',
    verified_by_tool = 'manual-NZ-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00081 (NZS 4121:2001 NZ, manual-NZ UNVERIFIED-1 via standards.govt.nz SPA route) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00450';

-- NEN 9120:2025 inheritance from REF-00071 (manual-NL IS-PAYWALL)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-NL-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00071 (NEN 9120:2025 NL, manual-NL IS-PAYWALL via nen.nl Dutch commercial catalog) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00433','REF-00466');

-- NBR 9050:2020 inheritance from REF-00077 (manual-BR IS-PAYWALL)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-BR-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00077 (NBR 9050:2020 BR, manual-BR IS-PAYWALL via abntcatalogo.com.br Portuguese commercial catalog with sustained 503) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00208','REF-00414','REF-00435','REF-00456');

-- GB 50763-2012 inheritance from REF-00016 (manual-CN DEFERRED-V2-AUTOMATED)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-CN-inherited',
    last_verified_at = '2026-05-19 20:45',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00016 (GB 50763-2012 CN, manual-CN DEFERRED-V2-AUTOMATED via openstd.samr.gov.cn SPA + mohurd.gov.cn DNS-blocked) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match (Chinese national standard, ZH non-EN free).',
    updated_at = '2026-05-19 20:45',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00359','REF-00375','REF-00462','REF-00475','REF-00510');

COMMIT;
