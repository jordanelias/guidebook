-- 079_value_note.sql
--
-- WHY A DETERMINATION HAS NO VALUE, recorded in the determination.
--
-- Migration 078 let the engine compose a value most-accommodatingly. It also made the
-- engine DECLINE to compose one in four distinct situations, and until this column those
-- four were indistinguishable in the database -- all four are `value_min IS NULL`:
--
--   1. no governing claim states a number (every one is qualitative, or a ratio);
--   2. the governing claims are in different UNITS, so there is no common interval and
--      converting them would invent a figure no source stated;
--   3. no `accessibility_direction` is recorded for the parameter, so the
--      most-accommodating rule has nothing to read;
--   4. the direction is CONTESTED -- DR-2026-07-21 section 5: no single value is anchored,
--      the conflict is recorded, and the spread is rendered with each population's
--      direction stated.
--
-- The fourth is not a gap, it is a FINDING, and it is content-affecting: a contested
-- direction means flush thresholds aid wheeled mobility while removing the tactile cues
-- cane users rely on, and the render surface is required to show that conflict rather than
-- pick a winner. Collapsing it into the same NULL as "nobody has recorded a direction yet"
-- loses the one case the safeguard exists for.
--
-- This is the same defect shape as the one migration 077 closed one stage earlier: a
-- `pending` cell and an unexamined parameter both read as absence unless something records
-- which it was. The engine already computes this reason; it was being returned in the report
-- JSON, which is not persisted, and dropped on the way to the row.
--
-- NOT a vocabulary. The reasons are the engine's own sentences and naming them in a CHECK
-- would put the composition rules in two places (CLAUDE.md rule 5, and rule 8's "never
-- curate a fact the machine computes"). The column records what the engine said.

ALTER TABLE specifications ADD COLUMN value_note TEXT;

PRAGMA user_version = 79;
