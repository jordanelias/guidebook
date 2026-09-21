-- 095_drop_amendments_no_reader.sql
--
-- REMOVING A TABLE ADDED ONE DAY EARLIER, BECAUSE NOTHING READS IT.
--
-- Migration 094 created `amendments` to replace amendment trails written as appended
-- prose. The diagnosis was right and the remedy was not, for three reasons a read-only
-- review established on 2026-09-21 and which are verified again here:
--
-- 1. NO READER. CLAUDE.md §8: "Nothing is added without naming what reads it. An unread
--    field, an uncalled script and an unregistered check are the same defect." 094 named
--    none. No view, trigger, test, audit or dashboard queries this table; `amend-source`
--    writes it and nothing looks.
--
-- 2. ONE WRITER OF AT LEAST EIGHT. `correct_source`, `amend_extraction`, `amend_search`,
--    `reattribute_candidate`, `set-locator-status`, `amend_gap` and `close_gap` all still
--    record corrections as prose or as a returned dict that is printed and dropped. A
--    register fed by one of eight paths does not read as partial -- it reads as complete,
--    and is wrong by omission from its first row. That is worse than no register, and the
--    hazard lands on the first amend-source call of the next research batch.
--
-- 3. ITS SOLE WRITER VIOLATED RULE 5 ON CONTACT. 094's own header says "NOT A SECOND HOME
--    ... that column keeps only the warrant". The writer then INSERTed `reason` into
--    `amendments.reason` AND appended it to `metadata_integrity_detail`, so the warrant
--    had two homes -- and the PROSE one is the copy `metadata_integrity_audit.py` reads.
--    The structured copy was the unread one. A migration written to end rule-5 violations
--    shipped one in its only writer.
--
-- DROPPABLE UNDER RULE 3. The column-can-never-be-dropped clause binds a column a
-- committed data migration INSERTs; nothing INSERTs this table (verified: zero matches for
-- `INSERT INTO "amendments"` across scripts/migrations/data_*.sql), and it holds 0 rows, so
-- no immutable record names it and no rebuild reproduces anything that is lost here.
-- §8: "Code, checks, scripts, dead tables and views: delete them. No owner gate. You need
-- evidence -- unreferenced, vacuous after a real batch, or superseded -- not permission."
--
-- WHAT WOULD JUSTIFY RE-CREATING IT, recorded so the next session inherits the finding
-- rather than the absence. The register needs a reader that is book-facing, and there is a
-- real one: a check that a live determination whose governing source had its `tier`,
-- `scope` or `verification_status` amended AFTER the determination's stamp is stale. That
-- cannot be built from `updated_at`, which records that a row changed but not WHICH FIELD;
-- it needs exactly (table, row, field, was, now, when) -- this table's shape. It is
-- book-facing because a ● marker computed under a tier since corrected is a claim the
-- guidebook makes and can no longer support. Build the reader first, then the register,
-- and wire every amending path at once rather than one.
--
-- The 83-odd existing prose trails are untouched, as 094 left them: recovering
-- (field, was, now) from a hand-written sentence is per-row judgment, and a regex right
-- most of the time would manufacture an authoritative-looking record that is wrong in the
-- rest. (094's header also quoted "83 rows across ten columns ... roughly 112,000
-- characters" as measured figures; none of the three reproduces. Derive them, never quote
-- them -- rule 7a, inside the migration whose purpose was structuring corrections.)
--
-- AFTER_DATA: 20260920060857

DROP INDEX IF EXISTS idx_amendments_target;
DROP INDEX IF EXISTS idx_amendments_session;
DROP INDEX IF EXISTS idx_amendments_field;
DROP TABLE IF EXISTS amendments;

PRAGMA user_version = 95;
