-- data_20260524223100_gap_294_steinfeld_doi_typo.sql
-- Materialize GAP-294 (DOI typo in REF-00059) for migration-reproducibility.

BEGIN TRANSACTION;

INSERT OR REPLACE INTO gaps (
    gap_id, category, priority, status, skill, section, description,
    created_at, created_by_session, updated_at, updated_by_session,
    falsification_condition, confidence_interval, shift_conditions, named_dissenter
) VALUES (
    'GAP-294',
    'CD', 'P3', 'OPEN',
    NULL, NULL,
    'REF-00059 (Steinfeld 2010 ''Anthropometry and standards for wheeled mobility: an international comparison'', PMID 20402047) has INCORRECT DOI in evidence_sources.doi field. Current value ''10.1080/10400430903496580'' returns HTTP 404 on both CrossRef and OpenAlex. Correct DOI per PubMed eutils lookup is ''10.1080/10400430903520280'' (note the suffix difference: ''496580'' vs ''520280'' — likely a digit transposition or copy-paste error). Surfaced during B.11 backward-mining for slug mobility-built-environment (MOB-01). Owner action: UPDATE evidence_sources SET doi = ''10.1080/10400430903520280'' WHERE ref_id = ''REF-00059''. The mining row for MOB-01 used the correct DOI.',
    '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure',
    '2026-05-24 20:59', 'session_2026-05-23-bpc-rewrite-phase-b-closure',
    NULL, NULL, NULL, NULL
);

COMMIT;
