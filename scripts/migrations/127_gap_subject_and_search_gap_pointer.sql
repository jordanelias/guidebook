-- 127_gap_subject_and_search_gap_pointer.sql
-- SCHEMA migration -- a gap says what it is a gap in, and a search says which gap caused it.
--
-- Until now a gap named its parameter and group only in its description sentence, so the book
-- could not list the stated gaps for one parameter or one group, and a search run to close a gap
-- could not say so (the backward step from a pending cell to research left no trail).
--
-- NULLABLE COLUMNS ON `gaps` (the parameter, the four lens codes, jurisdiction, language) AND ONE ON
-- `search_executions` (gap_id), all ALTER TABLE ... ADD COLUMN (no CHECK, no rebuild; a NULL default
-- beside REFERENCES is legal, as in 125). Each REFERENCES clause is the one the same column carries on
-- `search_executions`; `jurisdiction` and `language` take no FK, as there. `search_executions` is
-- STRICT, so its new column is typed.
--
-- WHO WRITES THEM: `db.py add-gap` (for a gap that has NO cell: a research or content gap) and
-- `db.py log-search --gap-id`. The assessment engine does NOT write the subject columns of the
-- gap it files for a pending cell: that cell (`specifications`) already holds the parameter and
-- the four lenses and points at the gap through `specifications.gap_register_id`, so copying them
-- here would store the same fact in a second table (CLAUDE.md rule 5). An engine-made gap keeps
-- NULL in these columns and is reached through that pointer.
-- Nothing is backfilled: no existing row names its subject in a column.
--
-- THE VIEW IS THE POINTER. `v_gap_subject` gives, per gap, the subject from the one home that holds
-- it: the gap's own typed columns when the gap names any (a gap with no cell), else the parameter and
-- four lens codes of the `specifications` row whose `gap_register_id` is that gap (the latest such row,
-- INCLUDING a retired one: an OPEN gap whose cell was retired still says what it is a gap in).
-- `subject_home` says which home answered. It stores nothing. It is NOT `v_pending`, which keeps only
-- live pending cells and so is empty exactly when an engine gap's cell has been retired.
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

-- One row per gap, from exactly one of three branches. "Typed" = the gap names any subject itself.
CREATE VIEW v_gap_subject AS
    SELECT g.gap_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code,
           g.jurisdiction, g.language, 'gaps' AS subject_home, NULL AS specification_id
      FROM gaps g
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code,
                    g.jurisdiction, g.language) IS NOT NULL
    UNION ALL
    SELECT g.gap_id, s.parameter_id, s.identity_code, s.icf_code, s.needs_code, s.medical_code,
           NULL, NULL, 'specifications', s.specification_id
      FROM gaps g
      JOIN specifications s
        ON s.specification_id = (SELECT MAX(x.specification_id) FROM specifications x
                                  WHERE x.gap_register_id = g.gap_id)
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code,
                    g.jurisdiction, g.language) IS NULL
    UNION ALL
    SELECT g.gap_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'none', NULL
      FROM gaps g
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code,
                    g.jurisdiction, g.language) IS NULL
       AND NOT EXISTS (SELECT 1 FROM specifications x WHERE x.gap_register_id = g.gap_id);

PRAGMA user_version = 127;
