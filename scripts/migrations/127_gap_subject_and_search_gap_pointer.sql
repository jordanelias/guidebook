-- 127_gap_subject_and_search_gap_pointer.sql
-- SCHEMA migration -- a gap says what it is a gap in, and a search says which gap caused it.
--
-- Until now a gap named its parameter and group only in its description sentence, so the book
-- could not list the stated gaps for one parameter or one group, and a search run to close a gap
-- could not say so (the backward step from a pending cell to research left no trail).
--
-- EIGHT NULLABLE COLUMNS ON `gaps`, ONE ON `search_executions`, all ALTER TABLE ... ADD COLUMN
-- (no CHECK, no rebuild; a NULL default beside REFERENCES is legal, as in 125). Each REFERENCES
-- clause is the one the same column carries on `search_executions`; `jurisdiction` and `language`
-- take no FK, as there. `search_executions` is STRICT, so its new column is typed.
--
-- WHO WRITES THEM: `db.py add-gap` (for a gap that has NO cell: a research or content gap) and
-- `db.py log-search --gap-id`. The assessment engine does NOT write the subject columns of the
-- gap it files for a pending cell: that cell (`specifications`) already holds the parameter and
-- the four lenses and points at the gap through `specifications.gap_register_id`, so copying them
-- here would store the same fact in a second table (CLAUDE.md rule 5). An engine-made gap keeps
-- NULL in these columns and is reached by that pointer (`v_pending`).
-- Nothing is backfilled: no existing row names its subject in a column.
--
-- Views naming either table (re-derive with sqlite_master): v_pending on gaps; the v_coverage_*
-- views and v_source_admission on search_executions. All name their columns, none takes a bare
-- SELECT *, so ADD COLUMN leaves them as they were.

ALTER TABLE gaps ADD COLUMN parameter_id INTEGER REFERENCES base_parameters(parameter_id);
ALTER TABLE gaps ADD COLUMN identity_code TEXT REFERENCES "base_taxonomy_identity"(identity_code);
ALTER TABLE gaps ADD COLUMN icf_code TEXT REFERENCES base_icf(icf_code);
ALTER TABLE gaps ADD COLUMN needs_code TEXT REFERENCES access_needs(need_code);
ALTER TABLE gaps ADD COLUMN medical_code TEXT REFERENCES base_taxonomy_medical(medical_code);
ALTER TABLE gaps ADD COLUMN jurisdiction TEXT;
ALTER TABLE gaps ADD COLUMN language TEXT;
ALTER TABLE search_executions ADD COLUMN gap_id TEXT REFERENCES gaps(gap_id);

PRAGMA user_version = 127;
