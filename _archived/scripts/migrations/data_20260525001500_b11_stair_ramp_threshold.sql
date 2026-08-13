-- data_20260525001500_b11_stair_ramp_threshold.sql
-- B.11 slug closure: stair-ramp-threshold-biomechanics-accessibility (14 sources).
-- All 14 fully mined (B=1, F=1) via CrossRef + OpenAlex cites: API.
-- This batch surfaced an OpenAlex rate-limit pattern: at ~3 req/s pacing, the daily
--   10k-credit / $1 USD limit hits HTTP 429 with retry-after ~71s. Re-ran with ~1.5s/req
--   pacing after rate-limit reset; completed without further 429s. Future B.11 batches
--   should default to 1.5s/req OpenAlex pacing.
-- Discoveries: 272 backward + 771 forward = 1,043 NEW candidate refs.
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-02', '10.1093/geronj/46.6.m188', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.1093/geronj/46.6.m188. FORWARD: OpenAlex cites:W2133172272 (110 cited_by_count; 110 fetched; 99 relevant; 97 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:03', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-03', '10.1093/ageing/17.6.378', 1, 1, '[]', 'BACKWARD: CrossRef (refs=18; doi_only=6; relevant=14; NEW=14). FORWARD: OpenAlex cites:W2088317987 (372 cited_by_count; 372 fetched; 220 relevant; 220 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_test', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-04', '10.1016/j.ergon.2014.07.001', 1, 1, '[]', 'BACKWARD: CrossRef (refs=52; doi_only=0; relevant=30; NEW=30). FORWARD: OpenAlex cites:W2034355977 (13 cited_by_count; 13 fetched; 8 relevant; 7 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-05', '10.1046/j.1532-5415.2002.50056.x', 1, 1, '[]', 'BACKWARD: CrossRef (refs=28; doi_only=20; relevant=26; NEW=26). FORWARD: OpenAlex cites:W2028222666 (118 cited_by_count; 116 fetched; 82 relevant; 82 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-06', '10.1016/j.apmr.2017.04.023', 1, 1, '[]', 'BACKWARD: CrossRef (refs=26; doi_only=0; relevant=20; NEW=19). FORWARD: OpenAlex cites:W2620870539 (3 cited_by_count; 3 fetched; 3 relevant; 2 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-07', '10.1016/j.apmr.2011.10.023', 1, 1, '[]', 'BACKWARD: CrossRef (refs=30; doi_only=0; relevant=26; NEW=26). FORWARD: OpenAlex cites:W2063263820 (34 cited_by_count; 32 fetched; 24 relevant; 24 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-08', '10.1002/jor.1100070215', 1, 1, '[]', 'BACKWARD: CrossRef (refs=20; doi_only=11; relevant=14; NEW=14). FORWARD: OpenAlex cites:W2034015968 (335 cited_by_count; 335 fetched; 195 relevant; 195 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-09', '10.1016/s0004-9514(14)60454-2', 1, 1, '[]', 'BACKWARD: CrossRef (refs=23; doi_only=0; relevant=10; NEW=10). FORWARD: OpenAlex cites:W2042039900 (44 cited_by_count; 42 fetched; 21 relevant; 21 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-10', '10.2196/69442', 1, 1, '[]', 'BACKWARD: CrossRef (refs=38; doi_only=0; relevant=26; NEW=24). FORWARD: OpenAlex cites:W4410001352 (1 cited_by_count; 1 fetched; 0 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-11', '10.1097/00006324-200105000-00019', 1, 1, '[]', 'BACKWARD: CrossRef (refs=36; doi_only=28; relevant=28; NEW=28). FORWARD: OpenAlex cites:W2030499378 (175 cited_by_count; 175 fetched; 117 relevant; 117 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-12', '10.3233/wor-210997', 1, 1, '[]', 'BACKWARD: CrossRef (refs=28; doi_only=0; relevant=20; NEW=20). FORWARD: OpenAlex cites:W4295030313 (1 cited_by_count; 1 fetched; 1 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-13', '10.3390/s24020526', 1, 1, '[]', 'BACKWARD: CrossRef (refs=28; doi_only=0; relevant=22; NEW=22). FORWARD: OpenAlex cites:W4390879675 (6 cited_by_count; 6 fetched; 5 relevant; 5 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:07', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:08', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-14', '10.2196/60622', 1, 1, '[]', 'BACKWARD: CrossRef (refs=28; doi_only=21; relevant=23; NEW=22). FORWARD: OpenAlex cites:W4406175718 (0 cited_by_count; 0 fetched; 0 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:08', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:08', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('stair-ramp-threshold-biomechanics-accessibility', 'SRB-15', '10.1371/journal.pone.0326850', 1, 1, '[]', 'BACKWARD: CrossRef (refs=38; doi_only=0; relevant=17; NEW=17). FORWARD: OpenAlex cites:W4411675093 (1 cited_by_count; 1 fetched; 1 relevant; 1 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-srb-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-25 00:08', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-25 00:08', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

UPDATE bpc_metadata SET citation_mining_complete = 1, updated_at = datetime('now'),
    updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'stair-ramp-threshold-biomechanics-accessibility'
   AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
