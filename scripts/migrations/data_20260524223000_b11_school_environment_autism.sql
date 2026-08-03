-- data_20260524223000_b11_school_environment_autism.sql
-- B.11 slug closure: school-environment-autism (15 T1-3 sources, 2 T4 preserved DEFER).
-- All 15 in-scope (T1-3) sources fully mined (B=1, F=1).
-- 2 T4 rows (SEA-bw-712 Bates 2016 Care and Design, SEA-bw-718 Deochand 2015 'Design
--   Considerations for an Intensive Autism Treatment Centre') remain DEPTH-1-DISCOVERY
--   DEFERRED — Tier 4 is out of scope for B.11 phase; the prior 2026-05-11g DEFER is
--   preserved.
-- This batch RE-MINED the 13 rows that 2026-05-11g had DEFERRED:
--   - SEA-02 + SEA-03: previously FORWARD-DEFERRED (Scholar Gateway unavailable); now
--     forward-mined via OpenAlex.
--   - 11 SEA-bw-71X rows: previously DEPTH-1-DISCOVERY DEFERRED; now backward+forward mined.
-- Discoveries: 360 backward + 544 forward = 904 NEW candidate refs (highest-yield slug
--   to date — academic-dense autism+design literature).
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-01', '10.1080/13603116.2025.2589290', 1, 1, '[]', 'BACKWARD: CrossRef (refs=68; doi_only=61; relevant=67; NEW=63). FORWARD: OpenAlex cites:W4416723462 (3 cited_by_count; 3 fetched; 1 relevant; 1 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-02', '10.3390/ijerph18063203', 1, 1, '["REF-00712", "REF-00713", "REF-00714", "REF-00715", "REF-00716", "REF-00717", "REF-00718", "REF-00719", "REF-00720", "REF-00721", "REF-00722", "REF-00723"]', 'BACKWARD: CrossRef (refs=52; doi_only=0; relevant=26; NEW=14). FORWARD: OpenAlex cites:W3138118944 (92 cited_by_count; 92 fetched; 57 relevant; 54 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g FORWARD-DEFERRED state — Scholar Gateway unavailability bypassed via OpenAlex cites: API per skill §2.', NULL, '2026-05-11T04:19:20', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-03', '10.1192/j.eurpsy.2024.272', 1, 1, '["REF-00724", "REF-00725"]', 'BACKWARD: CrossRef ref-list empty for DOI 10.1192/j.eurpsy.2024.272. FORWARD: OpenAlex cites:W4401921452 (1 cited_by_count; 1 fetched; 1 relevant; 1 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g FORWARD-DEFERRED state — Scholar Gateway unavailability bypassed via OpenAlex cites: API per skill §2.', NULL, '2026-05-11T04:19:21', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-711-724', '10.26687/archnet-ijar.v8i1.314', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.26687/archnet-ijar.v8i1.314. FORWARD: OpenAlex cites:W1932144093 (146 cited_by_count; 143 fetched; 96 relevant; 90 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-711-725', '10.1108/arch-11-2022-0258', 1, 1, '[]', 'BACKWARD: CrossRef (refs=16; doi_only=0; relevant=12; NEW=10). FORWARD: OpenAlex cites:W4385405028 (13 cited_by_count; 12 fetched; 12 relevant; 12 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-712', '10.1002/9781119053484', 0, 0, '[]', 'Depth-1 backward from REF-00710/SEA-01.', 'DEPTH-1-DISCOVERY: queued for separate batch pass', '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-713', '10.1016/j.aej.2018.10.014', 1, 1, '[]', 'BACKWARD: CrossRef (refs=31; doi_only=0; relevant=20; NEW=20). FORWARD: OpenAlex cites:W2914357237 (33 cited_by_count; 33 fetched; 24 relevant; 23 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-714', '10.1108/OHI-01-2010-B0004', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.1108/OHI-01-2010-B0004. FORWARD: OpenAlex cites:W3119440633 (44 cited_by_count; 44 fetched; 28 relevant; 23 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-715', '10.1177/1539449216665116', 1, 1, '[]', 'BACKWARD: CrossRef (refs=40; doi_only=32; relevant=37; NEW=35). FORWARD: OpenAlex cites:W2518765358 (52 cited_by_count; 52 fetched; 42 relevant; 40 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-716', '10.1111/j.1467-9604.2012.01525.x', 1, 1, '[]', 'BACKWARD: CrossRef (refs=37; doi_only=6; relevant=26; NEW=24). FORWARD: OpenAlex cites:W2164672583 (59 cited_by_count; 59 fetched; 41 relevant; 39 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-717', '10.1111/1467-8578.12160', 1, 1, '[]', 'BACKWARD: CrossRef (refs=52; doi_only=16; relevant=36; NEW=36). FORWARD: OpenAlex cites:W2574280766 (64 cited_by_count; 64 fetched; 48 relevant; 44 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-718', '10.1111/1467-9604.12103', 0, 0, '[]', 'Depth-1 backward from REF-00710/SEA-01.', 'DEPTH-1-DISCOVERY: queued for separate batch pass', '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-719', '10.1016/j.ridd.2017.02.004', 1, 1, '[]', 'BACKWARD: CrossRef (refs=44; doi_only=0; relevant=28; NEW=27). FORWARD: OpenAlex cites:W2589787503 (80 cited_by_count; 79 fetched; 57 relevant; 51 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-720', '10.1016/j.healthplace.2018.05.001', 1, 1, '[]', 'BACKWARD: CrossRef (refs=67; doi_only=0; relevant=45; NEW=44). FORWARD: OpenAlex cites:W2804003424 (38 cited_by_count; 38 fetched; 18 relevant; 16 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-721', '10.1007/s10901-008-9129-6', 1, 1, '[]', 'BACKWARD: CrossRef (refs=66; doi_only=0; relevant=58; NEW=58). FORWARD: OpenAlex cites:W2037308411 (54 cited_by_count; 54 fetched; 42 relevant; 39 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-722', '10.5014/ajot.2012.004010', 1, 1, '[]', 'BACKWARD: CrossRef (refs=39; doi_only=0; relevant=29; NEW=29). FORWARD: OpenAlex cites:W1983886763 (113 cited_by_count; 113 fetched; 95 relevant; 88 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('school-environment-autism', 'SEA-bw-723', '10.26687/archnet-ijar.v12i3.1589', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.26687/archnet-ijar.v12i3.1589. FORWARD: OpenAlex cites:W2899040667 (35 cited_by_count; 35 fetched; 25 relevant; 23 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-sea-*-discoveries.json. Per-row INSERT deferred per PI rule #10. RE-MINED: replaces 2026-05-11g DEPTH-1-DISCOVERY DEFERRED state — full backward+forward mining now applied.', NULL, '2026-05-11T04:19:23', 'session_2026-05-11g-citation-mining.md', '2026-05-24 22:55:50', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi, backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

-- Slug closure per skill §1 BATCH mode step 3
UPDATE bpc_metadata SET citation_mining_complete = 1,
       updated_at = datetime('now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'school-environment-autism' AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
