-- 163_gap_resolution_kind.sql
-- SCHEMA migration, compensating 162 (committed, not edited): T-144's repair after the adversarial pass. No data rows.
--
-- 1. ONE VALUE PER CELL (owner, 2026-11-06: no prefix that says what the rest of the cell means). 162's resolution_ref
--    held a commit, a ledger pointer, a task id or prose told apart only by their shape. resolution_kind names which,
--    and close-gap checks the pointer by its kind:
--      commit     a commit that exists in this repository (git cat-file -e <sha>^{commit});
--      ledger     references/project-standards.md :: "<verbatim quote>", the quote found once;
--      task       a task id with its file under workplan/2026-11-12-bidirectional-pipeline/tasks/;
--      duplicate  another gap that exists;
--      reason     the reason in words (a decided, rejected or accepted-limit closing).
--    The kinds are this CHECK's; db.py reads them with dbcore.check_values and holds no second list. A data migration
--    path is not a kind: the migration that carries a closing is emitted after it, so it does not exist when the gap is
--    closed. The kind is present exactly when the other three resolution cells are.
-- 2. THE STAMP'S HOUR AND MINUTE BY SHAPE: datetime() round-trips '2026-11-20 24:00' to the next day's midnight, so
--    162's round-trip test let hour 24 through. Hour 00-23 and minute 00-59 are refused otherwise here.
-- Not closed, recorded: a NUL inside the session or the pointer (char(0) ends a string in SQLite's text functions;
-- migrations 160 and 161 leave it open the same way and the CLI cannot pass one); a stamp in the future; the
-- not-before-created_at test on rows whose created_at is a date alone
-- (`select count(*) from gaps where length(created_at) = 10`).
-- A CLOSED gap with all four cells NULL stays accepted: the gaps closed before 162 are such rows, and the committed
-- data migrations that close gaps replay through this CHECK.

ALTER TABLE gaps ADD COLUMN resolution_kind TEXT
    CHECK (resolution_kind IS NULL OR resolution_kind IN ('commit', 'ledger', 'task', 'duplicate', 'reason'))
    CHECK ((resolution_kind IS NULL) = (resolution_ref IS NULL)
       AND (resolution_kind IS NULL) = (resolved_at IS NULL)
       AND (resolution_kind IS NULL) = (resolved_by_session IS NULL)
       AND (resolved_at IS NULL OR (substr(resolved_at, 12, 2) BETWEEN '00' AND '23'
                                    AND substr(resolved_at, 15, 2) BETWEEN '00' AND '59')));

PRAGMA user_version = 163;
