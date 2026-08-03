-- data_20260524205000_b11_mental_health_built_environment.sql
-- B.11 slug closure: mental-health-built-environment (20 sources).
-- 16 fully mined (B=1, F=1) via CrossRef + OpenAlex; 4 full-DEFERRED with reasons.
-- Improvement over room-acoustic batch: 2 no-DOI sources resolved to DOIs
--   via OpenAlex pmid:/title-search before falling to DEFER (MHB-12 → 10.1016/j.jpsychires.2024.07.045 via PMID;
--   MHB-17 → 10.1111/inm.13277 via title search). The other 4 no-DOI sources are grey-lit
--   institutional docs (SAMHSA, DiMHN, CHD) or unresolvable metadata (MHB-23 author pending);
--   structurally not mineable until grey-lit harvester or source completion.
-- Discoveries: 264 backward + 359 forward = 623 NEW candidate refs in
--   sessions/artifacts/2026-05-24-b11-mental-health-{backward,forward}-discoveries.json.
-- Forward-only; idempotent via ON CONFLICT.

BEGIN TRANSACTION;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-01', '10.3390/ijerph192114279', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=110; relevant=68; NEW=68). FORWARD: OpenAlex cites:W4307990038 (40 cited_by_count; 40 fetched; 28 relevant; 28 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-02', '10.1007/s40653-023-00528-y', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=72; relevant=47; NEW=46). FORWARD: OpenAlex cites:W4327605590 (15 cited_by_count; 15 fetched; 13 relevant; 13 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-03', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: REF-(SAMHSA TIP-57) — institutional gov-doc with no DOI. CrossRef + OpenAlex DOI/PMID lookups not applicable. OpenAlex title search did not return a citable work record (institutional reports often not indexed). Re-queue with grey-lit-specific harvester.', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-07', '10.1136/bmjopen-2020-046647', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=66; relevant=40; NEW=40). FORWARD: OpenAlex cites:W3180186138 (44 cited_by_count; 44 fetched; 33 relevant; 30 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-08', '10.1177/1937586720937995', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=44; relevant=3; NEW=3). FORWARD: OpenAlex cites:W3042375701 (30 cited_by_count; 23 fetched; 17 relevant; 17 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-09', '10.1111/inm.13065', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=53; relevant=8; NEW=8). FORWARD: OpenAlex cites:W4295047892 (37 cited_by_count; 37 fetched; 18 relevant; 18 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-10', '10.4135/9781071891414.n126', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.4135/9781071891414.n126 (publisher did not deposit references; backward complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W4391891002 (0 cited_by_count; 0 fetched; 0 relevant; 0 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-11', '10.1192/bjp.bp.112.118422', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=38; relevant=6; NEW=6). FORWARD: OpenAlex cites:W2066573625 (126 cited_by_count; 126 fetched; 82 relevant; 78 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-12', '10.1016/j.jpsychires.2024.07.045', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=53; relevant=28; NEW=27). FORWARD: OpenAlex cites:W4401275087 (14 cited_by_count; 14 fetched; 12 relevant; 12 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-13', '10.1186/s12913-022-08322-6', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=21; relevant=13; NEW=13). FORWARD: OpenAlex cites:W4286560514 (12 cited_by_count; 12 fetched; 7 relevant; 7 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-14', '10.1136/bmjopen-2022-067943', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=18; relevant=4; NEW=4). FORWARD: OpenAlex cites:W4321211316 (8 cited_by_count; 8 fetched; 5 relevant; 5 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-15', '10.1186/1472-6963-10-89', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=60; relevant=31; NEW=31). FORWARD: OpenAlex cites:W1991543277 (170 cited_by_count; 169 fetched; 94 relevant; 94 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-16', '10.1111/jpm.12576', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=36; relevant=4; NEW=4). FORWARD: OpenAlex cites:W2991221260 (29 cited_by_count; 28 fetched; 22 relevant; 22 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-17', '10.1111/inm.13277', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=64; relevant=10; NEW=10). FORWARD: OpenAlex cites:W4390731812 (6 cited_by_count; 6 fetched; 5 relevant; 5 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-19', '10.7202/smq', 1, 1, '[]', 'BACKWARD: CrossRef ref-list empty for DOI 10.7202/smq (publisher did not deposit references; backward complete-but-empty, no DEFER). FORWARD: OpenAlex cites:W4235604137 (3 cited_by_count; 3 fetched; 1 relevant; 1 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-20', '10.1111/inm.13070', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=38; relevant=4; NEW=4). FORWARD: OpenAlex cites:W4295441857 (19 cited_by_count; 19 fetched; 14 relevant; 14 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-21', '10.1177/19375867231219031', 1, 1, '[]', 'BACKWARD: CrossRef (total_refs=57; relevant=0; NEW=0). FORWARD: OpenAlex cites:W4392047736 (17 cited_by_count; 17 fetched; 15 relevant; 15 NEW). Discoveries: sessions/artifacts/2026-05-23-b11-mental-health-*-discoveries.json. Per-row INSERT deferred per PI rule #10.', NULL, '2026-05-24 20:27', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-22', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Industry-association resources page; no DOI; not a peer-reviewed citable work. Mining citations of a resources hub is structurally undefined. Owner may retire the source_slug_links row or convert to specific cited works.', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-23', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Metadata has placeholder author and the title ''Patient perspectives on outpatient mental health environment design'' did not return a confident OpenAlex match — top hits were all COVID/digital-health unrelated. P3 metadata gap; owner action: complete the citation or retire the source_slug_links row.', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
ON CONFLICT(slug, local_ref_id) DO UPDATE SET
    doi = excluded.doi,
    backward = excluded.backward,
    forward = excluded.forward,
    connections_produced = excluded.connections_produced,
    notes = excluded.notes,
    deferred_reason = excluded.deferred_reason,
    updated_at = excluded.updated_at,
    updated_by_session = excluded.updated_by_session;

INSERT INTO citation_mining (slug, local_ref_id, doi, backward, forward, connections_produced, notes, deferred_reason, created_at, created_by_session, updated_at, updated_by_session) VALUES ('mental-health-built-environment', 'MHB-25', NULL, 0, 0, '[]', NULL, 'FULL-DEFERRED: Industry toolbox / Issue Brief; grey-lit. No DOI. Structurally undiscoverable via CrossRef + OpenAlex; needs grey-lit harvester. Same class as MHB-03 and MHB-22.', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure', '2026-05-24 20:27:53', 'session_2026-05-23-bpc-rewrite-phase-b-closure')
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
 WHERE slug = 'mental-health-built-environment'
   AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
