-- data_20260519070000_v2_manual_verification_pilot_batch_5.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 5.
-- 8 probed rows + 6 inherited rows = 14 rows total.
--
-- Probed (8):
--   REF-00326 US  ANSI/ASA S12.60-2010    → IS-PAYWALL  (ASA portals 404 + Cloudflare; ANSI commercial)
--   REF-00334 INT IEC TR 63079:2017       → IS-PAYWALL  (IEC webstore 404 + IEC TR catalog 403; IEC commercial)
--   REF-00335 US  ANSI S12.60:2010        → IS-PAYWALL  (same ANSI publisher pattern as REF-00326)
--   REF-00473 US  NFPA 72                 → VERIFIED    (nfpa.org/72 200 OK, NFPA + National Fire Alarm in body; same page used by REF-00536)
--   REF-00559 US  IES RP-46-23            → IS-PAYWALL  (ies.org 403 + store SSL error; IES commercial)
--   REF-00560 INT CIE TN 015:2023         → IS-PAYWALL  (cie.co.at home reachable, specific page 404; CIE commercial)
--   REF-00575 DA  SBi-anvisning 218       → IS-PAYWALL  (sbi.dk reorganized to BUILD/AAU, specific anvisning not URL-discoverable; historically commercial)
--   REF-00419 JP  MLIT バリアフリー法     → DEFERRED-V2-AUTOMATED  (mlit.go.jp BF page returns wrong subpage; non-EN free, URL-discovery brittle)
--
-- Inherited (6) per the standard-number-inheritance mechanic (DR amendment 2026-05-19):
--   REF-00326 ANSI/ASA          IS-PAYWALL              → REF-00563, REF-00604
--   REF-00237 SE BFS 2024:12    DEFERRED-V2-AUTOMATED   → REF-00413, REF-00423, REF-00439, REF-00449
--
-- Net writes by status:
--   +1 VERIFIED, +9 IS-PAYWALL, +4 DEFERRED-V2-AUTOMATED (= 14 rows)
-- Net to rule #10 eligible pool: +1 (235 → 236; 35.1% → 35.2%).

BEGIN;

-- ============================================================
-- PROBED ROWS
-- ============================================================

-- REF-00326 US ANSI/ASA S12.60-2010 — English commercial standards
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-US',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://asastandards.org/Standards-and-Specifications-for-Acoustics-/ (HTTP 404 stylized page), https://acousticalsociety.org/standards/ (HTTP 403 Cloudflare-blocked). ANSI/ASA jointly-published commercial standard; ANSI webstore Cloudflare-blocked (established in earlier batch). Per DR-2026-05-19 amendment routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase ANSI/ASA S12.60-2010/Part 1 via ANSI Webstore or ASA Standards.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00326';

-- REF-00334 INT IEC TR 63079:2017 — commercial IEC technical report
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-INT',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://webstore.iec.ch/publication/29571 (HTTP 404 351KB stylized), https://www.iec.ch/standardsdev/publications/tr.htm (HTTP 403 919-byte block). IEC publishes commercial standards including TRs. English, commercial. Per DR-2026-05-19 amendment routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase IEC TR 63079:2017 (Code of practice for hearing-loop systems) via IEC Webstore.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00334';

-- REF-00335 US ANSI S12.60:2010 — same publisher pattern as REF-00326
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-US',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URL attempted: https://webstore.ansi.org/standards/asa/ansiasas12602010partr2020 (HTTP 403 Cloudflare). DB standard_number = ANSI S12.60:2010 (slightly different string from ANSI/ASA S12.60-2010 — same source acoustics standard, distinct catalog labeling). ANSI commercial publisher, Cloudflare-blocked from container. Per DR-2026-05-19 amendment routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase via ANSI Webstore. Note: REF-00326 and REF-00335 refer to the same school-acoustics standard under different ANSI vs ANSI/ASA labeling — these are not duplicates per the project''s same-source-multiple-citations pattern.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00335';

-- REF-00473 US NFPA 72 — same publisher as REF-00536 (VERIFIED), nfpa.org/72 page resolves
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-US',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via nfpa.org; URL=https://www.nfpa.org/codes-and-standards/nfpa-72-standard-development/72; matched: issuer=NFPA, std_num=NFPA 72 (DB std_num is general "NFPA 72" without edition suffix; nfpa.org/72 is the canonical code-development page), title=National Fire Alarm and Signaling Code (1 token match), most-current edition surfaced in JSON-in-HTML; HTTP=200 size=259866. Cert-validation issue (container clock TLS strictness) bypassed with -k. Same page used by REF-00536 (NFPA 72-2022 specific edition).',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00473';

-- REF-00559 US IES RP-46-23 — English commercial IES publication
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-US',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.ies.org/standards/published-standards/ (HTTP 403 5KB block), https://store.ies.org/product/ansi-ies-rp-46-23-recommended-practice-for-lighting-people-with-low-vision/ (SSL error — server-cert not-yet-valid on container clock; site reachable but TLS strict). IES is American Illuminating Engineering Society — commercial publisher of RP-46-23 (Recommended Practice for Lighting People with Low Vision). Per DR-2026-05-19 amendment routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase via IES store.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00559';

-- REF-00560 INT CIE TN 015:2023 — English commercial CIE technical note
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-INT',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://cie.co.at/publications/second-international-workshop-circadian-and-neurophysiological-effects-light (HTTP 404 stylized), https://cie.co.at/ (HTTP 200 70KB, no TN 015 tokens — corporate home not catalog detail). CIE = International Commission on Illumination; commercial English publisher. Per DR-2026-05-19 amendment routing matrix: EN + commercial paywall = IS-PAYWALL. Owner action: purchase CIE TN 015:2023 via CIE webshop.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00560';

-- REF-00575 DA SBi-anvisning 218 — Danish, historically commercial publication
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-DA',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://build.dk/Publications.aspx (HTTP 403 5KB block), https://sbi.dk/anvisninger (HTTP 200 139KB, title BUILD''s arbejde til byggebranchen - Aalborg Universitet — generic landing, 2 anvisning tokens but no document detail), https://sbi.dk/anvisninger/Pages/218-Lydforhold-i-skoler-Anvisning.aspx (HTTP 200 same 139KB generic body — URL-guess redirected to landing). SBi merged into BUILD/Aalborg University; legacy sbi.dk catalog URLs no longer resolve directly to specific anvisning pages. SBi-anvisning 218 (school acoustics) was historically a paid Danish publication. Per DR-2026-05-19 amendment routing matrix: covered-language (DA in 19-lang coverage) + paywalled = IS-PAYWALL. Owner action: purchase via BUILD/AAU successor catalog or library access.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00575';

-- REF-00419 JP MLIT バリアフリー法 建築物移動等円滑化誘導基準 — non-EN free, URL-discovery brittle
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-JP',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.mlit.go.jp/sogoseisaku/barrierfree/sosei_barrierfree_tk_000044.html (HTTP 200 9KB, wrong subpage about Hankyu Railway video communication accessibility, 0 バリアフリー法 tokens, 0 建築物移動等円滑化 tokens). MLIT publishes accessibility regulations under document-ID URLs not predictable from law name. Non-EN (JA) free government publication. Per DR-2026-05-19 amendment routing matrix: non-EN + free + URL-discovery-fails = DEFERRED-V2-AUTOMATED. Same pattern as batch 2 REF-00198 MEXT and REF-00016 CN openstd. No owner action available.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00419';

-- ============================================================
-- INHERITED ROWS
-- ============================================================

-- ANSI/ASA inheritance from REF-00326 (manual-US IS-PAYWALL)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-US-inherited',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00326 (ANSI/ASA S12.60-2010 US, manual-US IS-PAYWALL via ANSI Webstore Cloudflare-block) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match ("ANSI/ASA" string).',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00563','REF-00604');

-- SE BFS 2024:12 inheritance from REF-00237 (manual-SE DEFERRED-V2-AUTOMATED)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-SE-inherited',
    last_verified_at = '2026-05-19 21:00',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual inheritance from canonical REF-00237 (SE BFS 2024:12, manual-SE DEFERRED-V2-AUTOMATED via boverket.se 3-URL 404) per DR-2026-05-19 amendment 2026-05-19 standard-number-inheritance mechanic. standard_number exact match.',
    updated_at = '2026-05-19 21:00',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00413','REF-00423','REF-00439','REF-00449');

COMMIT;
