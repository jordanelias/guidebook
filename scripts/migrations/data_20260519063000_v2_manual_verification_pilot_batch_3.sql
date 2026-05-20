-- data_20260519063000_v2_manual_verification_pilot_batch_3.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 3 (middle-cohort).
-- Per the DR's promotion-gate (§6 step 5) requirement of reproducibility under
-- different session conditions, batch 3 widens the sample from easy-case
-- (batch 1 AU/NO/US) and hard-case (batch 2 CN/JP/NL/BR/JA) to a middle-cohort
-- mix (SE/CA/SG/INT) that tests the routing matrix across:
--   - SE Swedish non-EN free (DEFERRED-V2-AUTOMATED expected)
--   - CA Canadian EN static NGO (VERIFIED expected)
--   - SG English commercial paywall portal with 403 (NEEDS-HUMAN expected)
--   - INT ISO/BSI English commercial paywall (IS-PAYWALL expected)
--   - INT academic English open publication with multi-gate block (NEEDS-HUMAN expected)
--
-- Yield: 1 VERIFIED / 0 UNVERIFIED-1 / 1 IS-PAYWALL / 2 NEEDS-HUMAN / 1 DEFERRED-V2-AUTOMATED.
-- One row added to rule #10 eligible pool (REF-00117 RHFAC v4.0).
--
-- Cumulative pilot across 3 batches (14 rows attempted):
--   4 VERIFIED, 1 UNVERIFIED-1, 4 IS-PAYWALL, 2 NEEDS-HUMAN, 3 DEFERRED-V2-AUTOMATED
--   = 5/14 (36%) cleared gate; 7/14 (50%) downstream-actionable via paywall or human;
--     3/14 (21%) V2-blocked.

BEGIN;

-- REF-00237 SE Boverket BFS 2024:12 — Swedish, free, URL-guess fails
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-SE',
    last_verified_at = '2026-05-19 20:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.boverket.se/sv/lag--ratt/boverkets-forfattningssamling/aktuell/2024/bfs-2024-12/ (HTTP 404 stylized error page), https://www.boverket.se/sv/lag--ratt/boverkets-forfattningssamling/ (HTTP 404), https://www.boverket.se/sv/lag--ratt/forfattningssamling/ (HTTP 404). Boverket.se reachable (returns 883KB stylized 404) but specific BFS 2024:12 document URL not discoverable from guessing — same pattern as JP MEXT. Non-EN (SV) free national regulation; per DR-2026-05-19 amendment 2026-05-19 routing matrix: non-EN + free + URL-guess-fails = DEFERRED-V2-AUTOMATED.',
    updated_at = '2026-05-19 20:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00237';

-- REF-00117 CA Rick Hansen Foundation RHFAC v4.0 — English, static NGO, 4/4 criteria pass
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-CA',
    last_verified_at = '2026-05-19 20:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via rickhansen.com; URL=https://www.rickhansen.com/become-accessible/rating-certification/rhfac-v40; matched: issuer=Rick Hansen Foundation (10 tokens in body), std_num=RHFAC v4.0 (5 tokens) + Rating Survey (1 token, matching DB std_num=RHFAC Rating Survey v4.0), year=2024 (explicit in body); title=Introducing RHFAC v4.0; HTTP=200; size=74988. Discovered via two-hop URL discovery (home → linked v4.0 page) rather than direct-URL guess.',
    updated_at = '2026-05-19 20:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00117';

-- REF-00074 SG BCA Code on Accessibility 2025 — English, free government code, 403 blocked
UPDATE evidence_sources SET
    verification_status = 'NEEDS-HUMAN',
    verified_by_tool = 'manual-SG',
    last_verified_at = '2026-05-19 20:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www1.bca.gov.sg/buildsg/sustainability/universal-design-and-accessibility/code-on-accessibility-in-the-built-environment (HTTP 403 919-byte block page), https://www1.bca.gov.sg/ (HTTP 403 919-byte block page), https://www.bca.gov.sg/ (HTTP 200 only 77 bytes, redirect stub). BCA.gov.sg responds with bot-block 403s to container-class traffic. English source from Singapore government building authority. Per DR-2026-05-19 amendment 2026-05-19 routing matrix: EN + Cloudflare/bot-block + non-paywall = NEEDS-HUMAN. Owner action: different-IP fetch (residential/local), confirm Code on Accessibility 2025 catalog page exists and matches DB metadata.',
    updated_at = '2026-05-19 20:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00074';

-- REF-00116 INT BS EN ISO 10535:2021 — English, ISO/BSI/DIN commercial paywall
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-INT',
    last_verified_at = '2026-05-19 20:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; ISO direct URL guesses returned wrong matches (iso.org/standard/68596 → 404; iso.org/standard/77383 → unrelated ISO 10303-1488); BSI URL guess (standardsdevelopment.bsigroup.com) → redirect loop; CrossRef route confirmed standards-body publication via DIN-republished German editions (DOI 10.31030/3273132 DIN EN ISO 10535:2022-03 and DOI 10.31030/3166958 DIN EN ISO 10535:2020-08) — the specific 2021 edition (BS EN ISO 10535:2021) is the UK English BSI republication, paywalled commercial. Per DR-2026-05-19 amendment 2026-05-19 routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase BS EN ISO 10535:2021 via BSI; alternative: purchase DIN EN ISO 10535:2022-03 via DIN Media (newer edition, would trigger SUPERSEDED state transition on receipt).',
    updated_at = '2026-05-19 20:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00116';

-- REF-00491 INT Mostafa ASPECTSS 2.0 — English, academic open, multi-source block
UPDATE evidence_sources SET
    verification_status = 'NEEDS-HUMAN',
    verified_by_tool = 'manual-INT',
    last_verified_at = '2026-05-19 20:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: archnet.org publications/aspectss + authorities/2173 + search/aspectss (all HTTP 429 rate-limited, 33KB blocked-page responses); dcu.ie pdf guess (HTTP 404); emerald.com search (HTTP 403); CrossRef query returns 5 Mostafa ASPECTSS results but none for the 2023 ASPECTSS 2.0 specifically (Mostafa''s 2014/2015/2018 papers found; 2023 ASPECTSS 2.0 is the version-2 framework update published as DCU/Archnet guide, not CrossRef-indexed). English open publication, multi-source gating. Per DR-2026-05-19 amendment 2026-05-19 routing matrix: EN + Cloudflare/rate-limit blocks + open = NEEDS-HUMAN. Owner action: access via different IP (residential), confirm via DCU institutional repo or direct Mostafa contact; ASPECTSS 2.0 may also be a Co-1 attestation candidate (autism community-attestation publication) rather than catalog-verifiable standard.',
    updated_at = '2026-05-19 20:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00491';

COMMIT;
