-- 044_cell_source_links.sql
-- SCHEMA migration — give the cell→source relationship an edge object.
--
-- THE PROBLEM THIS SOLVES
-- `evidence_cell_state.governing_refs` holds the single most important edge in
-- the graph — which sources govern a best-practice determination — as a TEXT
-- column containing a JSON array:
--
--   '["REF-00338", "REF-00339", ..., "REF-00347"]'
--
-- That shape has three costs. It cannot be foreign-keyed, so a ref that does
-- not exist is indistinguishable from one that does. It cannot be indexed, so
-- the reverse walk — "which cells does REF-00338 govern?" — requires scanning
-- every row and parsing every array. And it cannot be joined, so every consumer
-- re-implements the parse; there are nine of them today.
--
-- Measured before writing this migration: 63 ref entries across 14 cells (one
-- cell has none), zero malformed arrays, zero intra-cell duplicates, and zero
-- refs that do not resolve to an `evidence_sources` row. The data is already
-- FK-clean; only the container is wrong.
--
-- WHAT THIS MIGRATION DOES NOT DO
-- It does not touch `governing_refs`. Dropping that column is a separate act
-- requiring a caller sweep across nine scripts — `validate_evidence_state.py`,
-- `test_db_integrity.py`, `assess_cell.py`, `adjudication_integrity.py`,
-- `check_rendered_docs.py`, `validate_verification_consistency.py`,
-- `pilot_renderings.py`, `pipeline_completeness.py` and one test — plus
-- `v_best_practice`, which is `SELECT *` over `evidence_cell_state` and so
-- carries the column implicitly. Per CLAUDE.md §0 rule 5, a structural removal
-- is not done until that sweep is done. The column and the junction coexist
-- until then, and a consistency check should hold them equal.
--
-- ROLE VOCABULARY
-- `role` admits exactly one value, 'governing', because that is the only
-- relationship the data expresses today. Migration 043 removed a table added
-- on speculation about future need; this migration declines to repeat that by
-- pre-coining roles ('contradicting', 'supporting') nothing writes. Widening a
-- CHECK is a one-line migration when a second role actually exists.
--
-- TIMESTAMPS
-- `created_at` deliberately carries NO `DEFAULT (datetime('now'))`. That default
-- appears in migrations 030–033, 039 and 042 and is why a rebuilt database can
-- never be byte-compared against the committed one: every rebuild re-stamps.
-- The populating data migration sets the value explicitly instead. This is the
-- discipline migration 030's own header describes ("timestamps normalised at
-- the tail of this transaction, never datetime('now')") applied at the point of
-- table creation rather than retrofitted.
--
-- Forward-only; user_version -> 44.

CREATE TABLE IF NOT EXISTS cell_source_links (
  cell_id             INTEGER NOT NULL REFERENCES evidence_cell_state(cell_id),
  ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  role                TEXT NOT NULL DEFAULT 'governing'
                        CHECK (role IN ('governing')),
  created_at          TEXT,
  created_by_session  TEXT,
  PRIMARY KEY (cell_id, ref_id)
);

-- The reverse walk is the whole point of the table: without this index,
-- "every page REF-00338 justifies" is a full scan.
CREATE INDEX IF NOT EXISTS idx_cell_source_links_ref ON cell_source_links(ref_id);
