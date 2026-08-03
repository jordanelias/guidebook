-- data_20260524195000_b11_room_acoustic_batch2.sql
-- B.11 batch 2: 16 remaining T1-3 sources in room-acoustic-performance.
-- 14 fully mined (B=1, F=1) via CrossRef (backward) + OpenAlex cites: (forward).
-- 1 backward-deferred (RAP-27, CrossRef HTTP 404 — forward complete).
-- 1 fully-deferred (RAP-10, no DOI — alt path required).
-- After this migration: room-acoustic-performance has 21 of 22 T1-3 sources with
--   mining rows. RAP-13 excluded (misclassified — see GAP-292).
-- Discovery surfaces:
--   sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-backward.json (143 NEW refs)
--   sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-forward.json  (469 NEW refs)
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-01', '10.3390/app11093942', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=73; relevant after acoustic/hearing/ND filter=15; NEW vs evidence_sources=14). FORWARD: OpenAlex cites:W3158784760 (40 citers; 9 relevant; 8 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-10', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: REF-00569 (Condran 2017, Shannex Arborstone dementia/noise framework) has no DOI (grey-lit institutional document). CrossRef ref-list lookup and OpenAlex cites: filter both require a resolvable DOI or OpenAlex work_id. Mining requires alternative path: (a) locate the document via Google Scholar to obtain OpenAlex work_id via title match, or (b) defer to author/title-keyword backward + forward harvest. Re-queue with explicit OpenAlex title-match attempt next batch.', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-12', '10.1044/2022_LSHSS-21-00181', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=60; relevant after acoustic/hearing/ND filter=5; NEW vs evidence_sources=5). FORWARD: OpenAlex cites:W4306802968 (27 citers; 20 relevant; 20 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-15', '10.61782/fa.2025.0068', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.61782/fa.2025.0068 (publisher did not deposit references; backward mining complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W7117303371 (0 citers; 0 relevant; 0 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json.', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-18', '10.1097/AUD.0b013e31825aecad', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=18; relevant after acoustic/hearing/ND filter=9; NEW vs evidence_sources=8). FORWARD: OpenAlex cites:W2069909064 (77 citers; 56 relevant; 53 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-19', '10.1097/AUD.0b013e3181d3d514', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=27; relevant after acoustic/hearing/ND filter=15; NEW vs evidence_sources=15). FORWARD: OpenAlex cites:W2041119287 (212 citers; 150 relevant; 145 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-20', '10.1044/2016_AJA-15-0064', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=55; relevant after acoustic/hearing/ND filter=13; NEW vs evidence_sources=13). FORWARD: OpenAlex cites:W2416991908 (29 citers; 24 relevant; 20 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-21', '10.1044/0161-1461(2004/017)', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=59; relevant after acoustic/hearing/ND filter=14; NEW vs evidence_sources=14). FORWARD: OpenAlex cites:W2019024534 (99 citers; 60 relevant; 57 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-22', '10.3766/jaaa.15096', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.3766/jaaa.15096 (publisher did not deposit references; backward mining complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W2550522341 (13 citers; 10 relevant; 8 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json.', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-25', '10.1097/AUD.0000000000000623', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=49; relevant after acoustic/hearing/ND filter=36; NEW vs evidence_sources=35). FORWARD: OpenAlex cites:W2807843516 (93 citers; 82 relevant; 81 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-26', '10.1097/AUD.0b013e31827ad76f', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.1097/AUD.0b013e31827ad76f (publisher did not deposit references; backward mining complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W2062102759 (18 citers; 13 relevant; 12 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json.', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-27', '10.4103/nah.NAH_15_19', 0, 1, '[]', 'BACKWARD: CrossRef returned HTTP 404 for DOI 10.4103/nah.NAH_15_19 — backward DEFERRED (record present in publisher metadata at Annals of Neurosciences but ref-list either not deposited to CrossRef or DOI-encoding issue with special char). FORWARD: OpenAlex cites:W3016626701 (4 citers; 2 relevant; 2 NEW). Discovery: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-forward.json. Re-attempt backward when an alternative ref source (publisher direct, Semantic Scholar) becomes available.', 'BACKWARD-DEFERRED: CrossRef HTTP 404 on DOI 10.4103/nah.NAH_15_19; alternative ref-list source (publisher direct, Semantic Scholar Open Citations) not attempted this batch; re-queue when ready. Forward mining is complete.', '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-28', '10.1097/AUD.0b013e31825641e4', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=33; relevant after acoustic/hearing/ND filter=12; NEW vs evidence_sources=12). FORWARD: OpenAlex cites:W2318105913 (4 citers; 2 relevant; 2 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-29', '10.3766/jaaa.18048', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.3766/jaaa.18048 (publisher did not deposit references; backward mining complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W2954844056 (4 citers; 4 relevant; 3 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json.', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-30', '10.1044/1059-0889(2004/009)', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=55; relevant after acoustic/hearing/ND filter=23; NEW vs evidence_sources=22). FORWARD: OpenAlex cites:W2021997416 (43 citers; 28 relevant; 27 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('room-acoustic-performance', 'RAP-31', '10.1177/13623613221102753', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=54; relevant after acoustic/hearing/ND filter=5; NEW vs evidence_sources=5). FORWARD: OpenAlex cites:W4282826350 (68 citers; 33 relevant; 31 NEW). Discovery surfaces: sessions/artifacts/2026-05-23-b11-room-acoustic-batch2-*.json. Per-discovery INSERT deferred per PI rule #10 (tier + verification needed).', NULL, '2026-05-24 19:45', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 19:45:13', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
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
