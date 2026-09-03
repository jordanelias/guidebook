-- 069_prior_expectation_is_a_research_fact.sql
-- SCHEMA migration — a prior expectation belongs to the SEARCH, not to the source.
--
-- THE DEFECT. DR-2026-05-09 §24 defines the field exactly: "evidence_sources.
-- prior_expectation -- what Claude expected BEFORE searching", logged in advance "to
-- expose confirmation bias". But it was placed on evidence_sources, whose rows are
-- written in the LOG action, after a source has been searched, screened, retrieved and
-- READ. At that moment a prior cannot be recorded, only reconstructed -- and a prior
-- reconstructed after reading the source is a post-hoc rationalisation wearing the
-- field that exists to prevent one. The register says so itself, at D05-025.
--
-- So the field could never be honestly populated where it sat: 0 of 9 verified rows
-- carry it, and research_protocol_audit CHECK 7 has been red on exactly those 9, alone
-- holding the whole audit red.
--
-- THIS IS ALSO A RULE 5 VIOLATION, and the fix has a precedent in the same file.
-- A pre-search expectation is a RESEARCH-stage fact. Holding it on an evidence row is
-- the identical defect CHECK 8 was repointed for on 2026-08-25: "The query that
-- surfaced a source is a RESEARCH-stage fact. It was being read off
-- evidence_sources.search_queries_used -- a research fact copied onto an evidence row,
-- which is the §2.2 violation the stage ruling forbids." CHECK 8 now reaches
-- search_executions.query_text through v_source_admission. CHECK 7 gets the same
-- treatment, and this migration gives it the column to reach.
--
-- WHY THE OLD COLUMN IS NOT DROPPED. CLAUDE.md rule 5: "a column a committed data
-- migration INSERTs can never be dropped". Four committed data migrations INSERT
-- evidence_sources.prior_expectation (batches 01, 01b, 02 and 05). So the sequence is
-- the documented one -- writer-retire, reader-retire, NULL forward. This migration does
-- the schema half; db.py drops the add-source flag (writer-retire) and CHECK 7 stops
-- reading it (reader-retire) in the same change. It holds 0 non-empty values today, so
-- nothing is stranded.

ALTER TABLE search_executions ADD COLUMN prior_expectation TEXT;

PRAGMA user_version = 69;
