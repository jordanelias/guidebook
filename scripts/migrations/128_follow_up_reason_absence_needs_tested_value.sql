-- 128_follow_up_reason_absence_needs_tested_value.sql
-- SCHEMA migration -- widen extraction_follow_ups.reason by ONE value:
-- `absence-needs-tested-value`. Tooling (IMP-13, workplan T-012); no research rows.
--
-- SUPERSEDES migration 105's sentence "THE REASON VOCABULARY HAS ONE VALUE, deliberately"
-- (105 is immutable and is not edited).
--
-- WHAT THE NEW VALUE RESTS ON. Owner ruling OR-22 (references/project-standards.md, "Owner
-- rulings 2026-10-29 (third)"): a study whose rows are all absence findings confirms the value
-- it tested, provided that value can be found "by backward citation mining of the study and
-- by contextual clues"; if it cannot be found the source has no value. OR-22 says to MINE. It
-- does not say a database row is required: this follow-up row is the carrier of the debt
-- (REQ-039, IMP-13), a choice made here, so that the work owed on an absence finding cannot be
-- forgotten and the finding later treated as read.
--
-- WHAT THE NEW VALUE RECORDS. A finding with claim_type = 'absent' that reports no change,
-- whose tested value backward citation mining and context are still to find. claim_type =
-- 'absent' also covers rows with no stated value for other reasons (a checklist question, a
-- qualitative requirement), so "this one owes a tested value" is a judgement with a warrant,
-- which is what a follow-up row records. db.py raise-follow-up refuses the reason on a row of
-- any other claim_type.
--
-- WHY NO `skimmed-needs-full-read` VALUE. The typed column
-- source_value_extractions.extraction_method = 'skim' already holds the debt for EVERY
-- skimmed row; a follow-up row for it would be a second home of the same fact (CLAUDE.md
-- rules 5 and 8) that stayed open after the column was amended. What the engine DOES with that
-- column is uneven, and this migration does not claim otherwise: scripts/assess/assess_cell.py
-- names a skimmed FINDING row as owing a dedicated reading; a skimmed claim row is named only
-- in the pending-cell branch; a skimmed condition row gets no reason from the engine at all.
-- The basis for "no row for a skimmed figure" is the assistant's reading, marked [ASSUMPTION:
-- "cue tools" means the engine's report names the tool for the owed pass; no row is written]
-- in the ledger (references/project-standards.md, the entry whose ACTION (4) says not to treat
-- the readings marked ASSUMPTION as ruled). It is NOT a ruling. It is supported, not settled,
-- by OD-10 ("provisional means strength of evidence; a re-read owed is a reading's own
-- status": grep -n 'a re-read owed is a reading' references/project-standards.md). Nothing is
-- named for `provisional` either: that is the cell's computed strength, not a follow-up.
-- 105's sentence that a skimmed figure needs no follow-up row is therefore carried forward as
-- that reading, not as a standing rule.
--
-- WRITERS: db.py raise-follow-up / resolve-follow-up (the --reason choices are read from
-- this CHECK). READER: scripts/audit/extraction_follow_up_audit.py. STAGE: judgment.
--
-- SQLite cannot change a CHECK in place: create, copy, drop, rename. The table is
-- AUTOINCREMENT and DROP TABLE deletes its sqlite_sequence row, so the floor is captured
-- first and restored as a maximum afterwards (as migration 114 does). Where the table holds
-- no row, nothing is captured, but the database still gains a sqlite_sequence row for it,
-- (extraction_follow_ups, 0), made by the copy; a table that never held a row had none
-- before, and 0 is what an unwritten AUTOINCREMENT table means. The one index on the table
-- is recreated exactly as 105 declares it; no view or trigger names the table.
-- Two harmless effects of the rename: the stored CREATE statement names the table in
-- quotes ("extraction_follow_ups"), and the table and its index sit at the end of
-- sqlite_master, in a different order from a database that never ran this migration.

CREATE TEMP TABLE _128_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'extraction_follow_ups';

CREATE TABLE _128_new_extraction_follow_ups (
    follow_up_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    reason              TEXT    NOT NULL CHECK (reason IN ('read-outside-admitting-purpose', 'absence-needs-tested-value')),
    warrant             TEXT    NOT NULL CHECK (length(trim(warrant)) > 0),
    raised_at           TEXT    NOT NULL,
    raised_by_session   TEXT    NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution          TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL AND resolution IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution IS NOT NULL AND length(trim(resolution)) > 0))
);

INSERT INTO _128_new_extraction_follow_ups
    (follow_up_id, extraction_id, reason, warrant, raised_at, raised_by_session,
     resolved_at, resolved_by_session, resolution)
SELECT follow_up_id, extraction_id, reason, warrant, raised_at, raised_by_session,
       resolved_at, resolved_by_session, resolution
  FROM extraction_follow_ups;

DROP TABLE extraction_follow_ups;
ALTER TABLE _128_new_extraction_follow_ups RENAME TO extraction_follow_ups;

CREATE UNIQUE INDEX ux_extraction_follow_ups_open
    ON extraction_follow_ups(extraction_id, reason) WHERE resolved_at IS NULL;

INSERT INTO sqlite_sequence (name, seq)
  SELECT s.name, s.seq FROM _128_seq s
   WHERE s.name NOT IN (SELECT name FROM sqlite_sequence);
UPDATE sqlite_sequence SET seq = MAX(seq, (SELECT COALESCE(MAX(seq), 0) FROM _128_seq))
  WHERE name = 'extraction_follow_ups';
DROP TABLE _128_seq;

PRAGMA user_version = 128;
