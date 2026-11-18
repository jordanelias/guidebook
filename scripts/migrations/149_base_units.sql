-- 149_base_units.sql
-- SCHEMA migration (T-030; no data rows beyond the seed of the unit table). Units, and the exact factor that relates
-- the units of one quantity kind, are rows.
--
-- WHY. The engine owned one hard-coded family (the gradient notations `%` and `rise:run ratio`), so a parameter whose
-- sources state the same length in millimetres, centimetres and metres declined to compose ("stated in different units"),
-- and a length family could be added only by editing the engine (GAP-072, GAP-094). OR-10 (owner, 2026-10-29): the engine
-- may compose across exact length units and present both. OD-24 (delegated resolution 2026-11-12): units belong to the
-- quantity kinds of T-020. OD-22 and OD-42 (delegated resolutions 2026-11-12 and 2026-11-13): a conversion between metric
-- prefixes is shown exactly; a conversion between inch-foot and metric is shown at the nearest quarter inch or 5 mm that
-- does not fall on the wrong side of the source's bound; the stored bound stays exact.
--
-- WHAT. base_units: one row per unit as a source writes it in claimed_unit, the kind it measures (a row of
-- base_quantity_kinds, T-020), and its factor as two integers, so the conversion is exact in Fraction and never a float:
-- one of this unit is factor_numerator / factor_denominator of the kind's CANONICAL unit. The canonical unit of a kind is
-- the one unit whose factor is 1 (the unique index below allows at most one; a kind with none cannot compose and the
-- reader says so). figure_form says how a figure of the unit is written: `number`, or `ratio` (written a:b, the figure
-- being a divided by b, so `1:12` under `rise:run ratio` is 100/12 percent). system says which measuring system a length
-- unit belongs to, because the shown figure is rounded to the owner's increment only when the shown unit's system is not
-- the system the source stated it in; NULL for a unit that has no such system. The increments themselves (5 mm; a quarter
-- inch) are the owner's ruling and live once, in dbcore.SHOWN_STEPS, beside the converter that applies them.
--
-- SEED. Every factor is a definition, not a measurement: the international inch is 25.4 mm exactly (1959) and the foot is
-- twelve inches, so 127/5 and 1524/5 millimetres. The two gradient notations are the pair NOTATION_FAMILIES held in
-- dbcore (owner ruling 2026-09-17, "Present both"); percent is canonical. `degrees` is NOT seeded: it is the arctangent
-- of the gradient, not a rescaling, so no exact factor relates it to percent. No force, time or other unit is seeded:
-- a unit is added when a parameter of its kind needs a conversion, by a migration (no verb writes this table).
--
-- WHAT READS IT. dbcore.load_units and the functions built on it (to_canonical, from_canonical, bound_on_scale,
-- figure_refusal), read by assess_cell.compose_value and by db.py add-extraction / amend-extraction (through figure_refusal
-- and the reformat rule).

CREATE TABLE base_units (
    unit                TEXT PRIMARY KEY CHECK (length(trim(unit)) > 0 AND unit = trim(unit)),
    kind_id             TEXT NOT NULL REFERENCES base_quantity_kinds(kind_id),
    factor_numerator    INTEGER NOT NULL CHECK (factor_numerator > 0),
    factor_denominator  INTEGER NOT NULL CHECK (factor_denominator > 0),
    figure_form         TEXT NOT NULL CHECK (figure_form IN ('number', 'ratio')),
    system              TEXT CHECK (system IS NULL OR system IN ('metric', 'inch-foot')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT
);

CREATE UNIQUE INDEX ux_base_units_canonical ON base_units(kind_id) WHERE factor_numerator = 1 AND factor_denominator = 1;

INSERT INTO base_units (unit, kind_id, factor_numerator, factor_denominator, figure_form, system, created_at, created_by_session) VALUES
 ('mm',             'length',   1,    1, 'number', 'metric',    '2026-11-18 00:00', 'migration_149'),
 ('cm',             'length',   10,   1, 'number', 'metric',    '2026-11-18 00:00', 'migration_149'),
 ('m',              'length',   1000, 1, 'number', 'metric',    '2026-11-18 00:00', 'migration_149'),
 ('in',             'length',   127,  5, 'number', 'inch-foot', '2026-11-18 00:00', 'migration_149'),
 ('ft',             'length',   1524, 5, 'number', 'inch-foot', '2026-11-18 00:00', 'migration_149'),
 ('%',              'gradient', 1,    1, 'number', NULL,        '2026-11-18 00:00', 'migration_149'),
 ('rise:run ratio', 'gradient', 100,  1, 'ratio',  NULL,        '2026-11-18 00:00', 'migration_149');

PRAGMA user_version = 149;
