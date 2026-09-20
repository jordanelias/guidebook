-- 094_amendments_register.sql
--
-- A CHANGE HISTORY THAT WAS BEING WRITTEN AS SENTENCES.
--
-- When a session corrects a record it has six structured facts in hand -- which table,
-- which row, which field, what the value was, what it became, and the warrant -- and every
-- correction path in this repository has been concatenating them into a text column:
--
--     || 2026-09-18 verification_status CORRECTED (I4 CAUGHT A GRADING ERROR ...).
--        Replaced text was: 'VERIFIED'
--
-- Measured 2026-09-20: 83 rows across ten columns carry roughly 112,000 characters of that
-- form -- gaps.description alone holds 37,929, search_executions.findings_note 22,679,
-- source_value_extractions.notes 16,109. Five of those six facts are columns wearing a
-- sentence. The consequence is not untidiness: "what did the 2026-09-16 adversarial pass
-- change" cannot be asked, a corrected field cannot be counted, and no gate can see a
-- correction at all, because to a gate the column is free text.
--
-- THE WARRANT STAYS PROSE, DELIBERATELY. Rule 8 draws the line: "Where judgment IS
-- genuinely required, the script asks for it -- constraining the answer to the live
-- vocabulary, demanding the evidence for it, and recording the answer and its warrant in
-- named columns." `reason` is an argument and belongs in text. `field`, `value_was`,
-- `value_now`, `amended_at` and `amended_by_session` are not arguments and stop being
-- sentences here.
--
-- NOT A SECOND HOME. `amend-source` stops composing the structured prefix into
-- `metadata_integrity_detail` in the same commit that adds this table; that column keeps
-- only the warrant, which is what `metadata_integrity_audit.py` prints (it keys on
-- metadata_integrity_status and never parses the text -- verified before writing this).
-- Rows amended before today keep their full prose, because that is what the committed
-- migrations say they held.
--
-- WHAT IS NOT BACKFILLED, AND WHY NOT. The 83 existing prose trails are NOT parsed into
-- rows. Recovering (field, was, now) from a hand-written sentence is per-row judgment, the
-- formats are not uniform, and a regex that is right 90% of the time would manufacture a
-- structured record that reads as authoritative and is wrong in eight places. Rule 8 says
-- the script asks for judgment rather than inventing it; there is no one to ask inside a
-- migration, so it does not guess. The trails stay where they are, legible to a person.
--
-- `table_name`/`row_key` are deliberately a loose pair rather than a foreign key: the
-- amended rows live in tables keyed on TEXT (evidence_sources.ref_id), INTEGER
-- (specifications.specification_id) and composites, and one FK cannot span them. The
-- integrity that matters here is that the fields are separate and queryable, which they now
-- are. `table_name` IS checked against the live schema by the writer.
--
-- AFTER_DATA: 20260920060857

CREATE TABLE amendments (
    amendment_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name          TEXT NOT NULL,
    row_key             TEXT NOT NULL,
    field               TEXT NOT NULL,
    value_was           TEXT,
    value_now           TEXT,
    -- The warrant. Prose on purpose: this is the argument for the change, and rule 8 keeps
    -- judgment in text while refusing to let the machine-decidable facts live there too.
    reason              TEXT NOT NULL,
    amended_at          TEXT NOT NULL,
    amended_by_session  TEXT NOT NULL
);

CREATE INDEX idx_amendments_target  ON amendments(table_name, row_key);
CREATE INDEX idx_amendments_session ON amendments(amended_by_session);
CREATE INDEX idx_amendments_field   ON amendments(table_name, field);

PRAGMA user_version = 94;
