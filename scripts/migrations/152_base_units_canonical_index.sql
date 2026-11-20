-- 152_base_units_canonical_index.sql
-- SCHEMA migration (T-030 repair; no data). Compensates migration 149 (committed, not edited): its unique index on the
-- canonical unit of a kind tested the literal `1/1`, so a row stored as `2/2` (factor one, unreduced) became a second
-- canonical unit of its kind, and `dbcore.canonical_unit` (which reads the factor as a Fraction) then had two to choose
-- from. The index now says what it means: the factor is one when numerator = denominator.
-- WHAT READS IT. dbcore.canonical_unit and every reader of base_units through dbcore.load_units (unchanged).

DROP INDEX ux_base_units_canonical;
CREATE UNIQUE INDEX ux_base_units_canonical ON base_units(kind_id) WHERE factor_numerator = factor_denominator;

PRAGMA user_version = 152;
