-- data_20260519073000_v2_manual_verification_pilot_batch_6_pattern.sql
--
-- DR-2026-05-19 channel-2 manual verification — pilot batch 6 (jurisdiction-pattern routing).
-- Per the DR amendment 2026-05-19 (jurisdiction-pattern routing mechanic), 6 remaining NULL-
-- verification COMPLETE-STATUTORY rows across CN/JP route to DEFERRED-V2-AUTOMATED via
-- pattern match without per-row portal probes. Each row's verification_note names the
-- establishing canonicals (≥3 probes per pattern) and the routing-matrix branch.
--
-- Pattern: non-EN free + URL-discovery-fails → DEFERRED-V2-AUTOMATED
-- Establishing canonicals across batches 2/3/5:
--   REF-00016 (CN GB 50763-2012 via openstd SPA + mohurd DNS-block)
--   REF-00198 (JA MEXT 特別支援学校施設整備指針 via 4-URL guess)
--   REF-00237 (SE BFS 2024:12 via boverket.se 3-URL 404)
--   REF-00419 (JP MLIT バリアフリー法 via mlit.go.jp wrong-subpage)
--
-- All 6 inheriting rows publish non-EN free government regulations under document-ID URLs
-- not predictable from standard name/number. No owner action available; awaits V2-automated
-- per-body scrapers.
--
-- Eligible-pool delta: 0 (pattern routing only writes non-VERIFIED states).
-- Queue delta: 6 → 0 NULL-verification COMPLETE-STATUTORY rows remaining.

BEGIN;

-- ZH (Chinese non-EN free pattern)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-ZH-pattern',
    last_verified_at = '2026-05-19 21:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual jurisdiction-pattern routing per DR-2026-05-19 amendment 2026-05-19 (jurisdiction-pattern mechanic). Pattern: non-EN free + URL-discovery-fails → DEFERRED-V2-AUTOMATED. Establishing canonicals from prior batches: REF-00016 (CN GB 50763-2012 openstd SPA), REF-00198 (JA MEXT 4-URL guess), REF-00419 (JP MLIT wrong-subpage). Chinese-language regulatory publication; no portal probe attempted given established pattern. Future per-row re-probe allowed if a static portal route becomes available; routing is non-destructive.',
    updated_at = '2026-05-19 21:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00195','REF-00196','REF-00197');

-- JP (Japanese non-EN free pattern)
UPDATE evidence_sources SET
    verification_status = 'DEFERRED-V2-AUTOMATED',
    verified_by_tool = 'manual-JP-pattern',
    last_verified_at = '2026-05-19 21:30',
    verification_attempt_count = verification_attempt_count + 1,
    verification_note = COALESCE(verification_note || char(10), '') ||
        '[session_2026-05-19-deployment-state-reconciliation 2026-05-19] V2-manual jurisdiction-pattern routing per DR-2026-05-19 amendment 2026-05-19 (jurisdiction-pattern mechanic). Pattern: non-EN free + URL-discovery-fails → DEFERRED-V2-AUTOMATED. Establishing canonicals from prior batches: REF-00198 (JA MEXT 4-URL guess), REF-00419 (JP MLIT wrong-subpage), REF-00016 (CN openstd SPA — shared pattern). MLIT バリアフリー法 building-regulation document under MLIT-internal document IDs not predictable from law name. Future per-row re-probe allowed if MEXT/MLIT publishes a static catalog index.',
    updated_at = '2026-05-19 21:30',
    updated_by_session = 'session_2026-05-19-deployment-state-reconciliation'
WHERE ref_id IN ('REF-00065','REF-00440','REF-00463');

COMMIT;
