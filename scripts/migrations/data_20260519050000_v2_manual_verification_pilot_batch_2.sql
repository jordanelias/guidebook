-- data_20260519050000_v2_manual_verification_pilot_batch_2.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 2 (hard-case test).
-- Per the counterclaim recorded in batch 1's attestation, batch 2 deliberately
-- sampled the hard-case cohort (CN/JP/NL/BR/JA) to test population-representative
-- yield rather than extending the easy-case streak.
--
-- Two new verification_status enum values introduced by DR-2026-05-19 amendment
-- (2026-05-19) per owner directive: IS-PAYWALL (paywalled commercial catalog
-- confirmed; purchase resolves) and DEFERRED-V2-AUTOMATED (non-EN non-paywall
-- SPA; no manual path; V2 scrapers required).
--
-- Yield: 0 VERIFIED / 0 UNVERIFIED-1 / 3 IS-PAYWALL / 2 DEFERRED-V2-AUTOMATED.
-- Zero rows added to rule #10 eligible pool. Five rows moved out of NULL into
-- explicit-cause states.
--
-- Note on TRANSIENT: V1 state machine §4 specifies TRANSIENT = retry next run,
-- no state mutation. Batch 2 maps sustained TRANSIENT on commercial catalogs
-- (ABNT 503 across attempts) to IS-PAYWALL since the 503 reflects load on a
-- paywalled-catalog server, not absence of the resource. One-off TRANSIENT
-- continues to write nothing.

-- REF-00016 CN GB 50763-2012 — non-English, free, openstd SPA (no manual path)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-CN',
    last_verified_at = '2026-05-19 19:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8541E2BE3CFEF7EA31D45F69C13B62F2 (HTTP 200 size 19841, JS-rendered shell with zero GB 50763 tokens), https://www.gov.cn/zhengce/2012-12/24/content_2295782.htm (HTTP 404), https://www.mohurd.gov.cn/ (DNS unresolved from container). Body publishes ZH-language GB national standards; specific document fetchable only via headless browser. Non-EN non-paywall SPA route per DR-2026-05-19 §3.4 CN entry amended 2026-05-19. No owner action available; awaits V2-automated openstd scraper.',
    updated_at = '2026-05-19 19:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00016';

-- REF-00017 JP JIS T 9251:2006 — Japanese, paywalled (JSA commercial)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-JP',
    last_verified_at = '2026-05-19 19:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.jisc.go.jp/app/jis/general/GnrJISSearch.html?show=JIS_T_9251 (HTTP 403 service-stopped page, JISC actively refuses container-class traffic), https://webdesk.jsa.or.jp/books/W11M0070/?bookId=00084036 (HTTP 200 size 56127, JSA catalog page with 販売/購入 commercial-sale tokens in body, title 規格検索結果). JSA commercial Japanese catalog confirmed; standard is paid product. Routing per DR-2026-05-19 §3.4 JP refinement: JP commercial standards route to JSA paywall directly. Owner action: purchase via JSA.',
    updated_at = '2026-05-19 19:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00017';

-- REF-00071 NL NEN 9120:2025 — Dutch, paywalled (NEN commercial)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-NL',
    last_verified_at = '2026-05-19 19:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.nen.nl/nen-9120-2025-nl-323858 (HTTP 404, body 139KB with one NEN 9120 token in URL back-reference only), https://www.nen.nl/zoeken?text=NEN+9120 (HTTP 404), https://www.nen.nl/ (HTTP 200 size 163928, NEN body reachable but no 9120 catalog tokens — corporate homepage not catalog detail). NEN commercial Dutch catalog confirmed via reachable NEN home; specific 9120:2025 catalog page is SPA. Routing per DR-2026-05-19 §3.4 NL refinement: route directly to NEN paywall. Owner action: purchase via NEN.',
    updated_at = '2026-05-19 19:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00071';

-- REF-00077 BR NBR 9050:2020 — Portuguese, paywalled (ABNT commercial; sustained 503)
UPDATE evidence_sources SET
    verification_status = 'IS-PAYWALL',
    verified_by_tool = 'manual-BR',
    last_verified_at = '2026-05-19 19:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.abntcatalogo.com.br/norma.aspx?ID=464229 (HTTP 503 size 239, sustained), https://www.abntcatalogo.com.br/ (HTTP 503 size 239, sustained), https://www.abnt.org.br/ (HTTP 200 size 258517, abnt.org.br corporate site reachable but no 9050 tokens — corporate homepage not catalog detail). ABNT catalog sustained 503 across attempts reflects load on paywalled-catalog server, not absence of resource. Per DR-2026-05-19 amendment 2026-05-19 (TRANSIENT handling): sustained TRANSIENT on commercial catalogs maps to IS-PAYWALL. ABNT commercial Portuguese catalog confirmed. Owner action: purchase via ABNT.',
    updated_at = '2026-05-19 19:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00077';

-- REF-00198 JA MEXT 特別支援学校施設整備指針 — Japanese, free MEXT publication (URL discovery fails)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-JA',
    last_verified_at = '2026-05-19 19:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 probe; URLs attempted: https://www.mext.go.jp/ (HTTP 200 size 17766, MEXT home reachable, title 文部科学省), https://www.mext.go.jp/a_menu/shotou/tokubetu/material/1339311.htm (HTTP 200 size 15525, special-ed materials index with 7 特別支援学校 tokens but 0 施設整備指針 tokens — wrong subpage), https://www.mext.go.jp/a_menu/shotou/tokubetu/ (HTTP 200 size 1426, 1.4KB redirect-stub index), https://www.mext.go.jp/a_menu/shotou/zyouhou/detail/1414568.htm (HTTP 404). MEXT publishes via document-ID-keyed URLs not predictable from standard number. Non-EN (JA) free MEXT publication. Per DR-2026-05-19 §3.4 JA refinement: URL-guess for specific MEXT guidelines unreliable. No owner action available; awaits V2-automated URL-discovery via MEXT API integration if any exists.',
    updated_at = '2026-05-19 19:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00198';

INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'data_20260519050000_v2_manual_verification_pilot_batch_2',
    '2026-05-19 19:30',
    'update_5_evidence_sources_3_IS-PAYWALL_2_DEFERRED-V2-AUTOMATED_hard_case_cohort',
    'session_2026-05-19-deployment-state-reconciliation',
    'DR-2026-05-19 channel-2 manual verification pilot batch 2 (hard-case test). Five rows walked: REF-00016 (CN GB 50763-2012 DEFERRED-V2-AUTOMATED), REF-00017 (JP JIS T 9251 IS-PAYWALL), REF-00071 (NL NEN 9120:2025 IS-PAYWALL), REF-00077 (BR NBR 9050:2020 IS-PAYWALL), REF-00198 (JA MEXT guideline DEFERRED-V2-AUTOMATED). Zero rows added to rule #10 eligible pool. Five rows moved from NULL to explicit-cause states per the DR amendment 2026-05-19 introducing IS-PAYWALL and DEFERRED-V2-AUTOMATED. Three IS-PAYWALL rows establish the purchase queue; two DEFERRED rows establish the V2-scraper queue. Combined batch 1 + batch 2 pilot: 9 rows attempted, 4 cleared gate (44%), 3 paywall-queued, 2 V2-deferred.'
);
