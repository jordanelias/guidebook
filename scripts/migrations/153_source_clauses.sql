-- 153_source_clauses.sql
-- SCHEMA migration (T-031; no data). The clause inventory, the route the owner chose for a later parameter reaching a
-- source already read (OD-23, 2026-11-12: "Clause inventory backed by retained text; clause NOT shown").
--
-- THE GAP. A source read today had to be read again for every parameter defined tomorrow, and nothing a clause could be
-- pointed at existed. Now the open pass of a full reading (`source_scans.open_pass_done`) records each clause of the
-- source as one row here, with its locator and its text as held for matching; a later parameter is matched against these
-- rows first, then against the retained text, and only where neither reaches is the source read again
-- (`scripts/audit/scan_debt.py --reread`).
--
-- ONE HOME. The source is reached through `scan_id` (source_scans.ref_id), never copied here (CLAUDE.md rule 5): the
-- reading that recorded a clause names the source it read. A figure's extraction points at its clause row
-- (`source_value_extractions.clause_id`, below) instead of typing the locator again; `db.py add-extraction` refuses a
-- locator given beside `--clause-id`, and a clause of another source.
--
-- NOT SHOWN. `clause_text` is held for matching only (OD-23, "clause NOT shown"): no view selects it, and a render
-- surface reads a clause row for its locator only (test T031-08 in scripts/tests/test_scan_contract.py).
--
-- STAGE: evidence (governance/stage-map.yaml), beside the reading that recorded it.
-- WHAT READS IT: `db.py add-extraction --clause-id`; `scan_debt.py --reread` and `db.py cell-status` (the re-read flag);
-- `db.py record-scan --clauses` writes it, and refuses a clause whose text is not in the file the reading names.

CREATE TABLE source_clauses (
    -- AUTOINCREMENT: an extraction points at a clause_id, which must never come to mean another clause.
    clause_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id             INTEGER NOT NULL REFERENCES source_scans(scan_id),
    -- the locator columns source_value_extractions uses (migration 053), with the same meaning
    locator_scheme      TEXT,
    loc_division        TEXT,
    loc_part            TEXT,
    loc_section         TEXT,
    loc_subsection      TEXT,
    loc_paragraph       TEXT,
    loc_clause          TEXT,
    loc_subclause       TEXT,
    loc_division_end    TEXT,
    loc_part_end        TEXT,
    loc_section_end     TEXT,
    loc_subsection_end  TEXT,
    loc_paragraph_end   TEXT,
    loc_clause_end      TEXT,
    loc_subclause_end   TEXT,
    loc_note            TEXT,
    -- the clause as the file read holds it; the writer refuses text not in that file
    clause_text         TEXT    NOT NULL CHECK (length(trim(clause_text, char(32,9,10,13))) > 0),
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    -- a clause row says where the clause stands: at least one level of the hierarchy
    CHECK (COALESCE(loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause,
                    loc_subclause) IS NOT NULL)
);
CREATE INDEX idx_source_clauses_scan ON source_clauses(scan_id);

ALTER TABLE source_value_extractions ADD COLUMN clause_id INTEGER REFERENCES source_clauses(clause_id);

PRAGMA user_version = 153;
