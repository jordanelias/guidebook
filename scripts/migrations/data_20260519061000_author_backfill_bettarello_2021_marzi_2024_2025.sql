-- data_20260519061000_author_backfill_bettarello_2021_marzi_2024_2025.sql
--
-- Author-row backfill for 3 COMPLETE non-corporate evidence_sources rows whose
-- evidence_source_authors coverage was incomplete:
--
--   1. REF-00561 (Bettarello et al. 2021): had 1 of 4 author rows. Backfill
--      the missing 3 (Caniato, Scavuzzo, Gasparella).
--   2. REF-00726 (Marzi et al. 2024): had 0 of 3 author rows. Backfill all 3.
--   3. REF-00727 (Marzi et al. 2025): had 0 of 3 author rows. Backfill all 3.
--
-- All three rows have COMPLETE metadata_quality, is_corporate_primary=0,
-- and explicit author_count > 1 with author_display populated. Without ≥
-- author_count rows in evidence_source_authors, db_integrity check G02 fails
-- (and REF-00726/REF-00727 fall below the ≥1 floor entirely).
--
-- Author names taken from evidence_sources.author_display (canonical source
-- per project convention). No external lookup needed; the names were
-- web-verified at original-row creation time (REF-00561 verified 2026-05-16,
-- REF-00726/727 verified 2026-05-17).
--
-- Forward-only and immutable once committed.

BEGIN;

-- REF-00561: append positions 2-4 (position 1 'Bettarello, F.' already exists)
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, is_corporate, role, created_at, created_by_session) VALUES
('REF-00561', 2, 'Caniato',   'M.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00561', 3, 'Scavuzzo',  'G.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00561', 4, 'Gasparella','A.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation');

-- REF-00726 Marzi 2024: all 3 authors
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, is_corporate, role, created_at, created_by_session) VALUES
('REF-00726', 1, 'Marzi',     'A.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00726', 2, 'Caniato',   'M.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00726', 3, 'Gasparella','A.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation');

-- REF-00727 Marzi 2025: all 3 authors
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, is_corporate, role, created_at, created_by_session) VALUES
('REF-00727', 1, 'Marzi',     'A.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00727', 2, 'Caniato',   'M.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation'),
('REF-00727', 3, 'Gasparella','A.', 0, 'author', '2026-05-19 20:10', 'session_2026-05-19-deployment-state-reconciliation');

COMMIT;
