-- data_20260524011500_b11_room_acoustic_mining_batch1.sql
-- B.11 batch 1: backward mining for 5 Tier-1 sources in room-acoustic-performance.
-- Backward complete (CrossRef-sourced reference lists; relevance-filtered, dedup against
--   evidence_sources by DOI). Discovery surface captured in sessions/artifacts/
--   2026-05-23-b11-room-acoustic-mining-discoveries.json for next-session triage.
-- Forward DEFERRED: Scholar Gateway connector in this environment exposes semanticSearch
--   only (no cited-by API); per skill §0 partial-availability rule.
-- Per-row insertion of NEW discovered references into evidence_sources is intentionally
--   NOT performed in this migration — each new row requires tier classification +
--   verification + population_match per PI rule #10, a separate workflow.
-- Forward-only; idempotent via ON CONFLICT clauses.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-11', '10.1044/2019_AJA-19-0010', 1, 0, '[]', 'Backward mining via CrossRef (api.crossref.org/works/10.1044/2019_AJA-19-0010). Total refs=52, relevance-filtered=5 (acoustic/hearing/classroom/listening-effort/ND keywords). Already-in-evidence_sources=0; NEW discoveries=5. Discoveries logged in /tmp/b11_mining_analysis.json (frozen for next-session triage; per-row tier classification + verification + INSERT deferred per session scope). Forward mining: see deferred_reason.', 'FORWARD-DEFERRED: Scholar Gateway connector in this environment exposes only semanticSearch (semantic similarity), not citation-relationship lookup. Per skill §0 partial-availability rule, forward mining DEFERRED with backward complete. Re-run forward pass when a cited-by API (Scholar Gateway citations, OpenAlex/Semantic Scholar inbound-citations) becomes available.', '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 06:24:57', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-23', '10.1097/AUD.0000000000001110', 1, 0, '[]', 'Backward mining via CrossRef (api.crossref.org/works/10.1097/AUD.0000000000001110). Total refs=97, relevance-filtered=74 (acoustic/hearing/classroom/listening-effort/ND keywords). Already-in-evidence_sources=4; NEW discoveries=70. Discoveries logged in /tmp/b11_mining_analysis.json (frozen for next-session triage; per-row tier classification + verification + INSERT deferred per session scope). Forward mining: see deferred_reason.', 'FORWARD-DEFERRED: Scholar Gateway connector in this environment exposes only semanticSearch (semantic similarity), not citation-relationship lookup. Per skill §0 partial-availability rule, forward mining DEFERRED with backward complete. Re-run forward pass when a cited-by API (Scholar Gateway citations, OpenAlex/Semantic Scholar inbound-citations) becomes available.', '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 06:24:57', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-24', '10.1044/2019_AJA-19-0041', 1, 0, '[]', 'Backward mining via CrossRef (api.crossref.org/works/10.1044/2019_AJA-19-0041). Total refs=20, relevance-filtered=1 (acoustic/hearing/classroom/listening-effort/ND keywords). Already-in-evidence_sources=0; NEW discoveries=1. Discoveries logged in /tmp/b11_mining_analysis.json (frozen for next-session triage; per-row tier classification + verification + INSERT deferred per session scope). Forward mining: see deferred_reason.', 'FORWARD-DEFERRED: Scholar Gateway connector in this environment exposes only semanticSearch (semantic similarity), not citation-relationship lookup. Per skill §0 partial-availability rule, forward mining DEFERRED with backward complete. Re-run forward pass when a cited-by API (Scholar Gateway citations, OpenAlex/Semantic Scholar inbound-citations) becomes available.', '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 06:24:57', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-marzi-2024', '10.1016/j.buildenv.2024.112254', 1, 0, '[]', 'Backward mining via CrossRef (api.crossref.org/works/10.1016/j.buildenv.2024.112254). Total refs=146, relevance-filtered=40 (acoustic/hearing/classroom/listening-effort/ND keywords). Already-in-evidence_sources=3; NEW discoveries=37. Discoveries logged in /tmp/b11_mining_analysis.json (frozen for next-session triage; per-row tier classification + verification + INSERT deferred per session scope). Forward mining: see deferred_reason.', 'FORWARD-DEFERRED: Scholar Gateway connector in this environment exposes only semanticSearch (semantic similarity), not citation-relationship lookup. Per skill §0 partial-availability rule, forward mining DEFERRED with backward complete. Re-run forward pass when a cited-by API (Scholar Gateway citations, OpenAlex/Semantic Scholar inbound-citations) becomes available.', '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 06:24:57', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-marzi-2025', '10.1038/s41598-025-02358-4', 1, 0, '[]', 'Backward mining via CrossRef (api.crossref.org/works/10.1038/s41598-025-02358-4). Total refs=160, relevance-filtered=65 (acoustic/hearing/classroom/listening-effort/ND keywords). Already-in-evidence_sources=5; NEW discoveries=60. Discoveries logged in /tmp/b11_mining_analysis.json (frozen for next-session triage; per-row tier classification + verification + INSERT deferred per session scope). Forward mining: see deferred_reason.', 'FORWARD-DEFERRED: Scholar Gateway connector in this environment exposes only semanticSearch (semantic similarity), not citation-relationship lookup. Per skill §0 partial-availability rule, forward mining DEFERRED with backward complete. Re-run forward pass when a cited-by API (Scholar Gateway citations, OpenAlex/Semantic Scholar inbound-citations) becomes available.', '2026-05-24 06:24', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 06:24:57', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
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
