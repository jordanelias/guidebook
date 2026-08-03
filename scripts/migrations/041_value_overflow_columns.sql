-- 041_value_overflow_columns.sql
-- SCHEMA migration — give conflated value columns a paired prose overflow.
--
-- THE PROBLEM THIS SOLVES
-- A column must hold one domain. Several here hold two: a value AND the prose
-- qualifying it. Measured on evidence_sources today:
--   standard_number   332 non-null, of which ~139 are bibliographic descriptions
--                     rather than identifiers — and at least one row,
--                     'BS 6440:2011 (supersedes BS 6440:1999; confirmed November
--                     2016)', is a real identifier WITH a qualifier glued on.
--   author_display    6 rows holding '[Author pending — …]' instead of a name
--   publisher         4 rows holding '[Pending — likely HERD or …]', a hypothesis
--
-- WHY AN OVERFLOW AND NOT A CLEANUP
-- A first attempt tried to split these by heuristic (length > 60) and relocate
-- the prose into `notes`. It was wrong twice over. It mis-split one row of 139 —
-- no rule reliably separates 'BS 6440:2011' from its parenthetical — and `notes`
-- is a single dumping ground, so moving field-specific prose there just moves
-- the conflation somewhere less traceable.
--
-- A paired overflow removes the judgement from write time. The typed value goes
-- in the value column, everything qualifying it goes in <column>_note at the
-- same grain, and nothing has to be thrown away or guessed at. Where the writer
-- cannot tell which part is the value, the whole string goes to the overflow and
-- the value stays NULL — honestly empty, and visible to a check, rather than
-- holding prose that a gate will mistake for a value.
--
-- This is additive: no existing value is touched by this migration. The
-- de-conflation itself is a DATA migration, and it moves prose INTO these
-- columns rather than into notes.
--
-- Forward-only; user_version -> 41.

ALTER TABLE evidence_sources ADD COLUMN standard_number_note TEXT;
ALTER TABLE evidence_sources ADD COLUMN author_display_note  TEXT;
ALTER TABLE evidence_sources ADD COLUMN publisher_note       TEXT;

-- evidence_source_authors has no notes column of its own, so corporate_name
-- placeholders had nowhere to go except another table. Give it one at its own
-- grain (per author row, not per source).
ALTER TABLE evidence_source_authors ADD COLUMN corporate_name_note TEXT;
