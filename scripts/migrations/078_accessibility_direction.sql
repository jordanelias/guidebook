-- 078_accessibility_direction.sql
--
-- BEST-FOR-THE-USER, NOT LARGEST-NUMBER. The metadata the ratified most-accommodating
-- rule needs, and has been waiting on since 2026-07-21.
--
-- THE RULE ALREADY EXISTS AND THE ENGINE COULD NOT OBEY IT.
-- `governance/evidence-architecture.md` (owner directive 2026-07-21, Option A):
--
--     Where jurisdictions' code floors differ on a parameter, the determination anchors on
--     the MOST ACCOMMODATING available value, read per the parameter's accessibility
--     direction -- best-for-the-user, not largest-number: the widest minimum corridor, but
--     the LOWEST maximum threshold height and the GENTLEST maximum ramp slope.
--
-- and its execution DR (DR-2026-07-21 section 5) adds the safeguard:
--
--     Where a parameter's accessibility direction is population-CONTESTED -- flush
--     thresholds aid wheeled mobility but remove the tactile cues cane users rely on;
--     heavy acoustic absorption aids hearing-aid users but degrades echolocation; brighter
--     light aids low vision but harms photosensitive users -- most-accommodating selection
--     is inapplicable: no single value is anchored, the conflict is recorded, and the
--     spread is rendered with each population's direction stated.
--
-- Both bullets carry an inline [ENGINE-LAG -> DR-2026-07-21 section 5] marker, and that DR
-- says markers "are removed only by the follow-up that lands the behavior". This migration
-- is the schema half of that follow-up: it adds the per-parameter direction the rule reads.
-- Without it a determination cannot compose a value at all, which is why every
-- `specifications.value_min/value_max/value_unit` written since the 057 baseline has been
-- NULL -- the engine passes literal None into those three slots because it has no rule it
-- could apply.
--
-- WHY THE DIRECTION IS A PROPERTY OF THE PARAMETER, not of the determination or the source.
-- "More is better" is true of corridor width whoever measured it and whichever jurisdiction
-- states it; it is a fact about what the parameter MEANS for a disabled person. Putting it
-- on the determination would copy it per cell (rule 5), and putting it on the source would
-- make the same parameter change direction between studies.
--
-- CONTESTED IS A FIRST-CLASS VALUE, NOT AN ABSENCE. It says the direction was examined and
-- found to depend on which disabled people you ask -- which is the case the safeguard exists
-- for, and the case where anchoring one number would silently pick a winner between two
-- populations. NULL says something different and weaker: nobody has decided yet. The engine
-- must treat the two differently and say which it met, so they cannot share a representation.
--
-- THE RATIONALE IS REQUIRED BY THE SCHEMA, not by the writer alone (CLAUDE.md rule 8: where
-- judgment is required, the script asks for it and records the answer AND ITS WARRANT). A
-- direction with no stated reason is an assertion about disabled people's needs with nothing
-- behind it. SQLite cannot add a table-level CHECK by ALTER TABLE, but a column-level CHECK
-- may reference a sibling column, which is what the constraint below does -- verified against
-- sqlite 3.45.1 before writing, rather than assumed.

ALTER TABLE base_parameters ADD COLUMN direction_rationale TEXT;

ALTER TABLE base_parameters ADD COLUMN accessibility_direction TEXT
    CHECK (accessibility_direction IS NULL
        OR (accessibility_direction IN ('higher_is_better',
                                        'lower_is_better',
                                        'contested')
            AND direction_rationale IS NOT NULL));

PRAGMA user_version = 78;
