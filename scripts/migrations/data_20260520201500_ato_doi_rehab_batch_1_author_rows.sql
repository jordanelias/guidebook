-- data_20260520201500_ato_doi_rehab_batch_1_author_rows.sql
--
-- Companion to data_20260520200000: insert evidence_source_authors rows for
-- the 3 rows where the rehab batch newly populated first_author_last
-- from Crossref but the join table previously had zero rows for these refs.
-- Resolves G02 db_integrity failure introduced by the rehab batch.
BEGIN TRANSACTION;

-- REF-00012: 5 authors from Crossref
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00012', 1, 'Elf', 'Marie', NULL, '0000-0001-7044-8896', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00012', 2, 'Slaug', 'Björn', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00012', 3, 'Ytterberg', 'Charlotte', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00012', 4, 'Heylighen', 'Ann', NULL, '0000-0001-6811-3464', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00012', 5, 'Kylén', 'Maya', NULL, '0000-0003-2887-3674', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');

-- REF-00332: 3 authors from Crossref
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00332', 1, 'Eurich', 'Bernhard', NULL, '0000-0003-3227-8261', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00332', 2, 'Klenzner', 'Thomas', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00332', 3, 'Oehler', 'Michael', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');

-- REF-00602: 5 authors from Crossref
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00602', 1, 'Kates', 'James M.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00602', 2, 'Lavandier', 'Mathieu', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00602', 3, 'Muralimanohar', 'Ramesh Kumar', NULL, '0000-0001-9440-7888', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00602', 4, 'Lundberg', 'Emily M. H.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00602', 5, 'Arehart', 'Kathryn H.', NULL, '0000-0002-5767-6584', 0, NULL, NULL, 'author', '2026-05-20T20:15:00Z', 'session_2026-05-20-ato-rehab');

INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes) VALUES (
  'data_20260520201500_ato_doi_rehab_batch_1_author_rows',
  '2026-05-20T20:15:00Z',
  'computed-at-apply-time',
  'session_2026-05-20-ato-rehab',
  'Author-row backfill for 3 G02-flagged refs from ATO-DOI-rehab batch 1: 13 author rows added.'
);
COMMIT;