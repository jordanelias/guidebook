-- data_20260524223000_b11_mobility_built_environment.sql
-- B.11 slug closure: mobility-built-environment (15 sources).
-- 6 fully mined (B=1, F=1) + 9 grey-lit/no-DOI full-DEFER.
-- This batch surfaced GAP-294: REF-00059 (MOB-01 Steinfeld 2010, PMID 20402047) had
--   an incorrect DOI in evidence_sources ('10.1080/10400430903496580' returns 404 on
--   both CrossRef and OpenAlex). Correct DOI per PubMed eutils: '10.1080/10400430903520280'.
--   Mining used the correct DOI; the evidence_sources.doi correction is pending owner action.
-- Discoveries: 101 backward + 209 forward = 310 NEW candidate refs.
-- 9 full-DEFERs: institutional grey-lit / multilingual government docs (Davies book,
--   Habinteg guide, Norwegian Direktoratet, Japanese MLIT, French Ifop, Ringaert proceedings,
--   Winkler/Newton conference papers, Finnish Invalidiliitto ESKEH, German Bundesverband ABC).
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-01', '10.1080/10400430903520280', 1, 1, '[]', 'BACKWARD: CrossRef (refs=21; doi_only=2; relevant=8; NEW=8). FORWARD: OpenAlex cites:W2168815645 (34 cited_by_count; 34 fetched; 25 relevant; 24 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10. NOTE: evidence_sources.doi for REF-00059 (MOB-01) is INCORRECT (''10.1080/10400430903496580'' — 404 on both CrossRef and OpenAlex). Correct DOI per PubMed PMID 20402047 is ''10.1080/10400430903520280''. Mining used the correct DOI. GAP-294 logged.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-02', '10.1080/10400430903520280', 1, 1, '[]', 'BACKWARD: CrossRef (refs=21; doi_only=2; relevant=8; NEW=8). FORWARD: OpenAlex cites:W2168815645 (34 cited_by_count; 34 fetched; 25 relevant; 24 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-04', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Davies 2021 ''Accessible Home Design: Architectural Solutions for the Wheelchair User, 2nd Edition'' — book/monograph, no DOI; OpenAlex title search returned unrelated IoT/VR/smart-mobility hits.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-05', '10.4324/9781003564164', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.4324/9781003564164 (publisher did not deposit references; backward complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W4402958929 (1 cited_by_count; 1 fetched; 0 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10. NOTE: This row was briefly mis-DEFERRED in an earlier turn-9 step; corrected to B=1/F=1.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:51', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-06', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Direktoratet for byggkvalitet (Norwegian Directorate) 2014 accessible buildings guide — government grey-lit, no DOI.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-08', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: 国土交通省 (Japanese Ministry of Land, Infrastructure, Transport and Tourism) 2024 housing design handbook — government grey-lit, no DOI; OpenAlex CJK title search not pursued this batch.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-10', '10.1016/S0140-6736(14)61006-0', 1, 1, '[]', 'BACKWARD: CrossRef (refs=23; doi_only=0; relevant=8; NEW=8). FORWARD: OpenAlex cites:W2092907196 (226 cited_by_count; 226 fetched; 137 relevant; 136 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-11', '10.1136/bmjopen-2020-046647', 1, 1, '[]', 'BACKWARD: CrossRef (refs=66; doi_only=22; relevant=29; NEW=28). FORWARD: OpenAlex cites:W3180186138 (44 cited_by_count; 44 fetched; 9 relevant; 7 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-12', '10.1097/PHM.0000000000000203', 1, 1, '[]', 'BACKWARD: CrossRef (refs=63; doi_only=0; relevant=51; NEW=49). FORWARD: OpenAlex cites:W2049057222 (26 cited_by_count; 26 fetched; 19 relevant; 18 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-mobility-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-14', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Ifop 2020 sondage for APF France handicap — polling survey grey-lit, no DOI; structurally undiscoverable via CrossRef/OpenAlex.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-15', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Ringaert 2001 conference proceedings / IDEA Center white paper — OpenAlex title search returned zero hits; likely unpublished or unindexed.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-17', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Winkler 2024 qualitative study — OpenAlex title search returned unrelated buildings/sustainability hits; cited work may be under different title or not yet indexed.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-18', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Newton 2023 ''Inclusive and Embodied Approach to Accessible Bathroom Design'' — OpenAlex title search returned unrelated CHI papers; may be unindexed grey-lit or conference proceedings.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-22', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Invalidiliitto ESKEH (Finnish built environment accessibility audit framework, 2018) — institutional methodology document, no DOI.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mobility-built-environment', 'MOB-24', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Bundesverband Selbsthilfe Körperbehinderter (German Federal Self-Help Federation) 2017 ABC Barrierefreies Bauen — institutional resource, no DOI.', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:59:21', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward, forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes, deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at, updated_by_session = excluded.updated_by_session;

-- Slug closure per skill §1 BATCH mode step 3
UPDATE bpc_metadata
   SET citation_mining_complete = 1,
       updated_at = datetime('now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'mobility-built-environment'
   AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
