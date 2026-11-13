-- 128_follow_up_reason_absence_needs_tested_value.sql
-- SCHEMA migration -- widen extraction_follow_ups.reason by ONE value:
-- `absence-needs-tested-value`. Tooling (IMP-13, workplan T-012); no research rows.
--
-- SUPERSEDES migration 105's sentence "THE REASON VOCABULARY HAS ONE VALUE, deliberately"
-- (105 is immutable and is not edited). 105's next sentence still holds: a skimmed figure
-- needs no follow-up row, because the typed column source_value_extractions.extraction_method
-- = 'skim' already says it and the determination engine names it as owing a dedicated
-- reading (scripts/assess/assess_cell.py). A follow-up row for it would be a second home of
-- the same fact (CLAUDE.md rules 5 and 8) that stayed open after the column was amended.
-- No `skimmed-needs-full-read` value is added, and none is named for `provisional`
-- (OD-10: provisional is the cell's computed strength, not a follow-up).
--
-- WHAT THE NEW VALUE RECORDS. A finding with claim_type = 'absent' that reports no change,
-- whose tested value backward citation mining and context are still to find (REQ-039).
-- claim_type = 'absent' also covers rows with no stated value for other reasons (a
-- checklist question, a qualitative requirement), so "this one owes a tested value" is a
-- judgement with a warrant, which is what a follow-up row records.
--
-- WRITERS: db.py raise-follow-up / resolve-follow-up (the --reason choices are read from
-- this CHECK). READER: scripts/audit/extraction_follow_up_audit.py. STAGE: judgment.
--
-- SQLite cannot change a CHECK in place: create, copy, drop, rename. The table is
-- AUTOINCREMENT and DROP TABLE deletes its sqlite_sequence row, so the floor is captured
-- first and restored as a maximum afterwards (as migration 114 does). The one index on the
-- table is recreated exactly as 105 declares it; no view or trigger names the table.

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
