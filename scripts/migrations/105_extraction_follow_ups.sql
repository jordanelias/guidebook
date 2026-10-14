-- 105_extraction_follow_ups.sql
-- SCHEMA migration — a typed, open-until-resolved follow-up on an extraction.
-- Tooling T1; the owner's answer to D1, 2026-10-09: "D1: yes figure from source filed by
-- another slug allowed. skimmed values are not publishable", read with the 03:08 words it
-- answered, "should be yes, but we still tag it for follow up later", which were not
-- withdrawn (catalogue-plan-v2 Addendum 1; the ledger entry "Owner statements 2026-10-09").
--
-- WHAT IT RECORDS. A figure read from a source filed under another slug may be extracted
-- and may set a published value, tagged so a reviewer re-checks it against the
-- parameter's own literature. Nothing could record that tag: no slug-to-parameter map
-- exists to DERIVE "read outside the purpose it was admitted for" (building one would be
-- a curated list beside the thing it describes, CLAUDE.md rule 8), so the judgement is
-- the reader's, recorded with its warrant, and contestable like any other.
--
-- WHY NOT A COLUMN ON source_value_extractions. A follow-up opens and closes; a column
-- would hold one state and lose the history of the other, and the extraction row would
-- become the second home of a judgement about it.
--
-- THE REASON VOCABULARY HAS ONE VALUE, deliberately: `read-outside-admitting-purpose`,
-- the case the owner's answer names. A second reason is a schema change in a tooling PR
-- with its ruling, never a CLI argument. Skimmed figures need no follow-up row: the
-- typed column extraction_method = 'skim' already says it, and the determination engine
-- now leaves those rows out of what sets a value (scripts/assess/assess_cell.py).
--
-- One OPEN follow-up per (extraction, reason): the partial unique index. A resolved one
-- stays as history, and a new one may be opened after it.
--
-- STAGE: judgment (governance/stage-map.yaml) -- whether an extraction is sound.
-- WRITERS: db.py raise-follow-up / resolve-follow-up. READER:
-- scripts/audit/extraction_follow_up_audit.py, which lists open follow-ups and fails any
-- LIVE determination resting on one (or on a skimmed figure) -- vacuous today, because no
-- live determination exists, and registered saying so.

CREATE TABLE extraction_follow_ups (
    follow_up_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    reason              TEXT    NOT NULL CHECK (reason IN ('read-outside-admitting-purpose')),
    warrant             TEXT    NOT NULL CHECK (length(trim(warrant)) > 0),
    raised_at           TEXT    NOT NULL,
    raised_by_session   TEXT    NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution          TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL AND resolution IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND length(trim(resolution)) > 0))
);

CREATE UNIQUE INDEX ux_extraction_follow_ups_open
    ON extraction_follow_ups(extraction_id, reason) WHERE resolved_at IS NULL;

PRAGMA user_version = 105;
