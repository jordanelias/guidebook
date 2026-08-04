-- 050_search_admissions.sql
-- SCHEMA migration — give the search→source relationship an edge object.
--
-- THE PROBLEM THIS SOLVES
-- Hop 3 of the walk (research question → … → admitted source) currently runs
-- through `search_executions.admitted_ref_ids`, a TEXT column holding a JSON
-- array:
--
--   '["REF-00891","REF-00892"]'
--
-- This is the same container fault migration 044 fixed for
-- `evidence_cell_state.governing_refs`, with the same three costs: it cannot be
-- foreign-keyed, so an admitted ref that does not exist is indistinguishable
-- from one that does; it cannot be indexed, so the reverse walk — "which search
-- found REF-00891?" — scans 84 rows and parses every array; and it cannot be
-- joined, so the provenance views cannot reach past the source into the search
-- that admitted it.
--
-- With 044 and this migration in place, every edge on the walk from a research
-- question to a rendered specification is a row with a foreign key. This was
-- the last JSON-array-as-edge in that path.
--
-- MEASURED BEFORE WRITING
-- 39 edge rows across 29 of the 84 executions; 39 distinct refs; zero orphans
-- against `evidence_sources`; zero duplicate (exec_id, ref_id) pairs; zero
-- malformed arrays; and `results_admitted` equals `json_array_length(
-- admitted_ref_ids)` on every row including the 55 with no array. The data is
-- already FK-clean and self-consistent; only the container is wrong.
--
-- THE BOUNDARY — WHAT GETS NO ROW
-- The other 824 sources predate the search-execution substrate
-- (DR-2026-07-24). They were admitted by searches nobody logged. They get no
-- rows here, and that absence is the correct record: minting an exec_id for
-- them would fabricate a search that was never run, which is exactly the
-- failure mode R8 and R14 of the research contract exist to prevent. A source
-- with no admission edge means "we do not know which search found this", not
-- "no search found this", and the schema should not let those two read alike.
--
-- WHAT THIS MIGRATION DOES NOT DO
-- It does not touch `admitted_ref_ids`. The column and the junction coexist,
-- held equal by a parity check in both directions (test_db_integrity H02/H03),
-- exactly as 044 prescribed for `governing_refs`. Dropping it is a separate act
-- requiring a caller sweep; today its only reader outside the migrations is
-- `schemas/search_execution.py`.
--
-- NO ROLE COLUMN
-- 044 gave `cell_source_links` a `role` because a cell could conceivably relate
-- to a source in more than one way. Admission is not like that: a search either
-- admitted a source or it did not. Migration 043 removed a table added on
-- speculation; this declines to add a column on the same basis. Screening
-- outcomes short of admission already have their own home in
-- `search_candidates`.
--
-- TIMESTAMPS
-- `created_at` carries NO `DEFAULT (datetime('now'))`, for the reason 044's
-- header gives: that default is why a rebuilt database cannot be byte-compared
-- against the committed one. The populating data migration sets it explicitly.
--
-- Forward-only; user_version -> 50.

CREATE TABLE IF NOT EXISTS search_admissions (
  exec_id             INTEGER NOT NULL REFERENCES search_executions(exec_id),
  ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  created_at          TEXT,
  created_by_session  TEXT,
  PRIMARY KEY (exec_id, ref_id)
);

-- The reverse walk is the point: without this index, "which search admitted
-- REF-00891" is a full scan of the junction.
CREATE INDEX IF NOT EXISTS idx_search_admissions_ref ON search_admissions(ref_id);
