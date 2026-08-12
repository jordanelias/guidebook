-- data_20260525100000_code_currency_initial_backfill.sql
-- Initial backfill of code_currency_status / code_currency_verified_at on
-- evidence_sources, following schema migration 016 (2026-05-25).
--
-- Backfill scope:
-- (1) NZS 4121:2001 (REF-00081, REF-00450) — VERIFIED-CURRENT per session
--     web-search 2026-05-25 (NZ Building Act 2004 §119 / D1/AS1 Acceptable
--     Solution; NZ Ministry of Education March 2025 guidance cites it
--     explicitly). Worked example for the "old code, still operative"
--     pattern that the code-currency audit is designed to surface and
--     correctly suppress on verification.
--
-- (2) PERMANENT-FRAMEWORK references — foundational documents that do
--     not revise on the same cadence as standards/codes:
--     - REF-00155 CRPD 2006 (UN treaty; substantive amendments require
--       state-party ratification; no revision since adoption)
--     - REF-00125 ICF 2001 (WHO classification framework; updated by
--       periodic addenda not edition replacement)
--     - REF-00190 WHO Child Growth Standards 2006 (WHO reference data;
--       updated via supplementary tables not edition replacement)
--
-- (3) T6 codes already in supersession_check with outcome=current_best
--     and checked_at >= 2025-05-25 (the 365-day suppression window) —
--     these are automatically suppressed by the audit's supersession_check
--     check but mirroring them as code_currency_status='VERIFIED-CURRENT'
--     makes their currency state queryable without the JOIN:
--     - REF-00566 GB 50118-2010 (China, RAP supersession check 2026-05-25)
--     - REF-00077 NBR 9050:2020 (Brazil, MOB supersession check 2026-05-25)
--     - REF-00065 JP 2025 architectural design standard (MOB)
--     - REF-00067 BFS 2024:12 Sweden (MOB)
--     - REF-00074 BCA SG 2025 (MOB)
--
-- The audit script itself remains the source of triage truth. This
-- migration documents the small set of cases already verified during
-- the 2026-05-25 session and demonstrates the column-update pattern
-- for future verification work.

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ────────────────────────────────────────────────────────────────────────
-- (1) NZS 4121:2001 — VERIFIED-CURRENT (worked example for the audit)
-- ────────────────────────────────────────────────────────────────────────
UPDATE evidence_sources
   SET code_currency_status = 'VERIFIED-CURRENT',
       code_currency_verified_at = '2026-05-25',
       code_currency_verified_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       code_currency_notes = 'Web search 2026-05-25 confirmed standard remains operative per NZ Building Act 2004 §119 / D1/AS1 Acceptable Solution. Cited in NZ Ministry of Education March 2025 guidance "Improving Accessibility at Schools" and Auckland Council Unitary Plan 2022. 24-year-old standard but no replacement exists. Pre-2026-05-25 audit speculation (likely superseded from age) was wrong; corrected per session record. Worked example: age does not predict supersession.',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id IN ('REF-00081', 'REF-00450');

-- ────────────────────────────────────────────────────────────────────────
-- (2) PERMANENT-FRAMEWORK references
-- ────────────────────────────────────────────────────────────────────────
-- CRPD 2006 — UN treaty; substantive content invariant across state-party
-- ratifications; "edition" concept does not apply.
UPDATE evidence_sources
   SET code_currency_status = 'PERMANENT-FRAMEWORK',
       code_currency_verified_at = '2026-05-25',
       code_currency_verified_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       code_currency_notes = 'UN Convention on the Rights of Persons with Disabilities — international treaty; substantive content is invariant across the treaty''s lifetime. Updates take the form of Committee General Comments and Concluding Observations, not edition replacement. Marked PERMANENT-FRAMEWORK to suppress audit fire from age threshold.',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id = 'REF-00155';

-- ICF 2001 — WHO classification framework; revisions are addenda not editions.
UPDATE evidence_sources
   SET code_currency_status = 'PERMANENT-FRAMEWORK',
       code_currency_verified_at = '2026-05-25',
       code_currency_verified_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       code_currency_notes = 'WHO International Classification of Functioning, Disability and Health — foundational classification framework. WHO maintains it via the Family of International Classifications (WHO-FIC) annual update process producing supplementary mappings and clarifications rather than edition replacement. Marked PERMANENT-FRAMEWORK to suppress audit fire from age threshold.',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id = 'REF-00125';

-- WHO Child Growth Standards 2006 — WHO reference data; updated by supplementary tables.
UPDATE evidence_sources
   SET code_currency_status = 'PERMANENT-FRAMEWORK',
       code_currency_verified_at = '2026-05-25',
       code_currency_verified_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       code_currency_notes = 'WHO Child Growth Standards — anthropometric reference data established 2006; subsequent WHO publications add supplementary tables and growth velocity standards rather than replacing the 2006 reference. Marked PERMANENT-FRAMEWORK to suppress audit fire from age threshold.',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id = 'REF-00190';

-- ────────────────────────────────────────────────────────────────────────
-- (3) T6 codes already supersession-checked 2026-05-25 → mirror as
--     VERIFIED-CURRENT for queryability without the JOIN
-- ────────────────────────────────────────────────────────────────────────
UPDATE evidence_sources
   SET code_currency_status = 'VERIFIED-CURRENT',
       code_currency_verified_at = '2026-05-25',
       code_currency_verified_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       code_currency_notes = 'Mirrored from supersession_check current_best outcome (2026-05-25 supersession audit per DR-2026-05-24 Pass 2). The supersession_check JOIN already suppresses this row from the code-currency audit; this column makes the currency state queryable directly without the JOIN.',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id IN ('REF-00566', 'REF-00077', 'REF-00065', 'REF-00067', 'REF-00074');

COMMIT;
