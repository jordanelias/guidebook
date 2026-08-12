-- data_20260524063500_b11_room_acoustic_forward_mining.sql
-- B.11 batch 1 forward mining via OpenAlex cites:{work_id} API.
-- Supersedes the FORWARD-DEFERRED state from data_20260524011500. OpenAlex provides
--   free programmatic cited-by lookup; skill §2 lists Google Scholar as an alternative,
--   and OpenAlex is the cleaner programmatic equivalent. The DEFERRED state was a
--   premature read of skill §0 (Scholar Gateway unavailability does not mean ALL forward
--   sources unavailable — OpenAlex/Semantic Scholar fill the same role).
-- Forward discoveries: 2/15/43/22/19 citers per source; relevance-filtered to
--   1/11/32/15/12 = 71 total; dedup against evidence_sources yields 69 NEW candidates.
-- Forward discovery surface: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-11', '10.1044/2019_AJA-19-0010', 1, 1, '[]', 'BACKWARD: CrossRef ref-list relevance-filtered. FORWARD: OpenAlex cites:W2995960266 (23 citers; 15 relevant after acoustic/hearing/ND filter; 14 NEW discoveries vs existing evidence_sources). Backward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json. Forward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json. Both surfaces preserved for next-session per-row triage (tier classification + verification + INSERT to evidence_sources, per PI rule #10) — protocol-complete partial state per skill §0/§4.', NULL, '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 18:59:14', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-23', '10.1097/AUD.0000000000001110', 1, 1, '[]', 'BACKWARD: CrossRef ref-list relevance-filtered. FORWARD: OpenAlex cites:W3187823847 (44 citers; 32 relevant after acoustic/hearing/ND filter; 32 NEW discoveries vs existing evidence_sources). Backward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json. Forward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json. Both surfaces preserved for next-session per-row triage (tier classification + verification + INSERT to evidence_sources, per PI rule #10) — protocol-complete partial state per skill §0/§4.', NULL, '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 18:59:14', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-24', '10.1044/2019_AJA-19-0041', 1, 1, '[]', 'BACKWARD: CrossRef ref-list relevance-filtered. FORWARD: OpenAlex cites:W2987309630 (19 citers; 12 relevant after acoustic/hearing/ND filter; 12 NEW discoveries vs existing evidence_sources). Backward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json. Forward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json. Both surfaces preserved for next-session per-row triage (tier classification + verification + INSERT to evidence_sources, per PI rule #10) — protocol-complete partial state per skill §0/§4.', NULL, '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 18:59:14', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-marzi-2024', '10.1016/j.buildenv.2024.112254', 1, 1, '[]', 'BACKWARD: CrossRef ref-list relevance-filtered. FORWARD: OpenAlex cites:W4403969072 (15 citers; 11 relevant after acoustic/hearing/ND filter; 10 NEW discoveries vs existing evidence_sources). Backward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json. Forward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json. Both surfaces preserved for next-session per-row triage (tier classification + verification + INSERT to evidence_sources, per PI rule #10) — protocol-complete partial state per skill §0/§4.', NULL, '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 18:59:14', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-marzi-2025', '10.1038/s41598-025-02358-4', 1, 1, '[]', 'BACKWARD: CrossRef ref-list relevance-filtered. FORWARD: OpenAlex cites:W4410838466 (2 citers; 1 relevant after acoustic/hearing/ND filter; 1 NEW discoveries vs existing evidence_sources). Backward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json. Forward discoveries: sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json. Both surfaces preserved for next-session per-row triage (tier classification + verification + INSERT to evidence_sources, per PI rule #10) — protocol-complete partial state per skill §0/§4.', NULL, '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 18:59:14', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

COMMIT;
