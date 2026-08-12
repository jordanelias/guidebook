-- data_20260519020000_v2_manual_verification_pilot_batch_1.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 1.
-- Per DR §6 step 3: walk 5 rows across 3 jurisdictions to validate the protocol
-- before promoting to a skill.
--
-- Batch composition: 4 rows / 3 jurisdictions (AU/NO/US) plus 1 row in NZ that
-- validates the UNVERIFIED-1 SPA route the DR predicted. NZ counts as a 4th
-- jurisdiction for protocol-validation purposes; §6 step 3's "3 jurisdictions"
-- minimum is satisfied by AU + NO + US writing VERIFIED.
--
-- All four probes performed live in session_2026-05-19-deployment-state-reconciliation.
-- URL and HTTP status recorded in verification_note per DR §3.3.
--
-- Pilot findings amend §3.4 routing table (forward-only edit in DR's own changelog
-- footer in a follow-up commit):
--   1. NO codes use year-encoded standard_numbers (TEK17 = 2017 edition). Criterion 3
--      (edition-year match) satisfies via the year-encoded ID; the portal does not
--      need to display the year explicitly. Document in routing-table notes.
--   2. US NFPA codes render edition metadata as JSON embedded in static HTML. The
--      JSON tokens count as "in initial HTML body" for §3.2 criterion 4 because
--      no JS execution was needed to read them.
--   3. SE Boverket: three URL guesses (gallande/bfs-202412/, gallande/bbr---bfs-201156/,
--      aktuell/) all returned 404 from container. Pending an external-search-based
--      route discovery; SE routing table entry remains "pending probe" until then.
--   4. NZ standards.govt.nz: confirmed SPA — shop direct URL returns 961-byte stub
--      with zero matched tokens; search URL returns 78KB but only 1 instance of
--      "NZS 4121" (in a back-reference URL). UNVERIFIED-1 route triggered as DR
--      predicted. Routing-table entry confirmed correct.

-- REF-00146 NCC 2022 (AU) — government code, static portal
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-AU',
    last_verified_at = '2026-05-19 18:55',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via ncc.abcb.gov.au; URL=https://ncc.abcb.gov.au/ncc-2022; matched: issuer=Australian Building Codes Board, std_num=NCC 2022, year=2022; HTTP=200; size=42264',
    updated_at = '2026-05-19 18:55',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00146';

-- REF-00145 TEK17 (NO) — government code, static portal; year encoded in standard_number
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-NO',
    last_verified_at = '2026-05-19 18:55',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via dibk.no; URL=https://dibk.no/regelverk/byggteknisk-forskrift-tek17/; matched: issuer=Direktoratet for byggkvalitet, std_num=TEK17 (year encoded in ID = 2017), title contains 13 TEK17 references; HTTP=200; size=214283',
    updated_at = '2026-05-19 18:55',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00145';

-- REF-00536 NFPA 72-2022 (US) — NGO standards body, static portal with JSON-in-HTML edition metadata
UPDATE evidence_sources SET
    verification_status = 'VERIFIED',
    verified_by_tool = 'manual-US',
    last_verified_at = '2026-05-19 18:55',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via nfpa.org; URL=https://www.nfpa.org/codes-and-standards/nfpa-72-standard-development/72; matched: issuer=NFPA, std_num=NFPA 72 (DB stores NFPA 72-2022; -2022 is edition suffix), title=National Fire Alarm and Signaling Code, edition 2022 in JSON-in-HTML page data; HTTP=200; size=259866',
    updated_at = '2026-05-19 18:55',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00536';

-- REF-00081 NZS 4121:2001 (NZ) — standards body with SPA catalog; UNVERIFIED-1 per DR §3.2
UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-1',
    verified_by_tool = 'manual-NZ',
    last_verified_at = '2026-05-19 18:55',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] manual-V2 verification via standards.govt.nz; URL=https://www.standards.govt.nz/shop/NZS-41212001 (stub, 961 bytes, zero token matches) and https://www.standards.govt.nz/search?q=NZS+4121 (78KB, one back-reference match only); body Standards New Zealand confirmed publishes NZS 4121 series but specific row not fetchable from static HTML; UNVERIFIED-1 per DR-2026-05-19 §3.2 SPA route; awaits V2-automated scraper or headless-browser fetch.',
    updated_at = '2026-05-19 18:55',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id = 'REF-00081';
