-- data_20260524212000_b11_cognitive_wayfinding_design.sql
-- B.11 slug closure: cognitive-wayfinding-design (15 sources).
-- 11 fully mined (B=1, F=1) + 4 grey-lit/unresolvable full-DEFER.
-- Filter improvement THIS batch: DOI-only refs (publisher deposits structured DOI but
--   no article-title in CrossRef metadata — common in Sage/SLACK/Karger journals) are
--   now INCLUDED as candidates rather than dropped at the title-relevance filter.
--   The parent paper's editorial process already vouched for them. Net effect on this
--   batch: backward NEW grew from 214 to 520 (rough 2.4× recovery).
-- Prior batches (room-acoustic-performance, mental-health-built-environment) may have
--   under-counted backward discoveries proportionally; not re-run this session.
-- Discoveries: 520 backward + 567 forward = 1,087 NEW candidate refs (after DOI-only fix).
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-01', '10.1177/193758671100400207', 1, 1, '[]', 'BACKWARD: CrossRef (refs=66; doi_only=46; relevant=57; NEW=56). FORWARD: OpenAlex cites:W2003033699 (168 cited_by_count; 168 fetched; 131 relevant; 125 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-02', '10.1177/1533317509334959', 1, 1, '[]', 'BACKWARD: CrossRef (refs=22; doi_only=13; relevant=15; NEW=14). FORWARD: OpenAlex cites:W2014022472 (184 cited_by_count; 183 fetched; 132 relevant; 126 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-03', '10.1177/19375867211043546', 1, 1, '[]', 'BACKWARD: CrossRef (refs=35; doi_only=16; relevant=28; NEW=26). FORWARD: OpenAlex cites:W3199828201 (22 cited_by_count; 22 fetched; 19 relevant; 17 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-04', '10.3389/frdem.2025.1524425', 1, 1, '[]', 'BACKWARD: CrossRef (refs=51; doi_only=0; relevant=38; NEW=33). FORWARD: OpenAlex cites:W4408299319 (4 cited_by_count; 4 fetched; 3 relevant; 3 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-05', '10.1007/s10339-021-01031-8', 1, 1, '[]', 'BACKWARD: CrossRef (refs=155; doi_only=0; relevant=93; NEW=90). FORWARD: OpenAlex cites:W3165181264 (51 cited_by_count; 51 fetched; 39 relevant; 38 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-06', '10.1177/193758671400800111', 1, 1, '[]', 'BACKWARD: CrossRef (refs=167; doi_only=145; relevant=166; NEW=164). FORWARD: OpenAlex cites:W2164173071 (220 cited_by_count; 220 fetched; 172 relevant; 167 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-07', '10.3390/ijerph18063203', 1, 1, '[]', 'BACKWARD: CrossRef (refs=52; doi_only=0; relevant=12; NEW=8). FORWARD: OpenAlex cites:W3138118944 (92 cited_by_count; 92 fetched; 47 relevant; 44 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-08', '10.1177/13623613221102753', 1, 1, '[]', 'BACKWARD: CrossRef (refs=54; doi_only=36; relevant=43; NEW=36). FORWARD: OpenAlex cites:W4282826350 (68 cited_by_count; 68 fetched; 33 relevant; 31 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-09', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: ASPECTSS higher-education framework by Mostafa M; no DOI/PMID. OpenAlex title search found a related Mostafa paper (school-design application, doi 10.1108/arch-11-2022-0258) but not the higher-education version cited here. The cited work may be unpublished or only available via Magda Mostafa''s institutional pages. Owner action: confirm whether CWD-09 should be merged into CWD-08 or remains a separate deliverable.', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-10', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: REF (DSDC EADDAT) — institutional assessment tool; no DOI/PMID. OpenAlex title search returned unrelated falls-prevention/multimorbidity hits — no confident match. Re-queue with grey-lit harvester.', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-11', '10.1002/trc2.12353', 1, 1, '[]', 'BACKWARD: CrossRef (refs=73; doi_only=44; relevant=59; NEW=58). FORWARD: OpenAlex cites:W4303517920 (21 cited_by_count; 21 fetched; 16 relevant; 15 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-17', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: RadarAdvies pilot evaluation report (Dutch dementia-friendly meeting places); no DOI. OpenAlex title search for the Dutch title returned zero results. Grey-lit; needs alternative harvester.', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-19', '10.4324/9781003095460-16', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.4324/9781003095460-16. FORWARD: OpenAlex cites:W4220749106 (0 cited_by_count; 0 fetched; 0 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-20', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Dementia Australia ''Designing dementia-friendly care environments'' resource; no DOI, no year. OpenAlex title search returned unrelated Lancet dementia-prevention papers — no confident match. Grey-lit institutional resource; needs alternative harvester.', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('cognitive-wayfinding-design', 'CWD-22', '10.1177/30495334251345092', 1, 1, '[]', 'BACKWARD: CrossRef (refs=44; doi_only=0; relevant=36; NEW=35). FORWARD: OpenAlex cites:W4411284602 (1 cited_by_count; 1 fetched; 1 relevant; 1 NEW). Discoveries: sessions/artifacts/2026-05-24-b11-cognitive-wayfinding-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:44', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:44:28', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

-- Slug closure per skill §1 BATCH mode step 3
UPDATE bpc_metadata
   SET citation_mining_complete = 1,
       updated_at = datetime('now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'cognitive-wayfinding-design'
   AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
