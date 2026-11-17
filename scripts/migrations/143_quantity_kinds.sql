-- 143_quantity_kinds.sql
-- SCHEMA migration (T-020; no data rows beyond the six-kind seed of the vocabulary table). A parameter states what
-- kind of quantity it is, and on what evidence anyone judged that it is one.
--
-- WHY. An element such as a grab bar can be promoted to a parameter: it then owes a reading from every source and is
-- determined as a cell, though it measures nothing, and nothing on the row says what it measures. Whether a term names
-- an element or a quantity cannot be computed from the term; it is a judgment (CLAUDE.md rule 8), so the writer asks
-- for it, constrained to the live vocabulary, and records the answer and its warrant in named columns. OD-24 (delegated
-- resolution 2026-11-12 in references/project-standards.md): a parameter states a quantity kind from a table of kinds
-- held as rows and extended by data with a warrant, not a CHECK list.
--
-- WHAT. base_quantity_kinds: one row per kind, its definition, and the dated ledger heading that admitted it (the
-- pointer terms.catalogue_approval_ref uses). Two nullable columns on base_parameters: the kind, and the observation
-- (observed_terms) whose verbatim quote states a value of the quantity, which is the warrant, a pointer and not a copy.
-- Nullable because the live parameters take their kind in a research pull request (T-109); db.py add-parameter
-- enforces both for every new row. A CHECK naming both columns is not added: the writer holds it.
--
-- SEED. Exactly the kinds OD-24 lists, each admitted by that entry. Ratio, percentage and degrees are notations of
-- gradient (T-030's), not kinds. created_at is the date of writing.
--
-- WHAT READS IT. db.py add-parameter (reads base_quantity_kinds and observed_terms), db.py add-quantity-kind (writes).

CREATE TABLE base_quantity_kinds (
    kind_id             TEXT PRIMARY KEY CHECK (length(trim(kind_id)) > 0),
    definition          TEXT NOT NULL CHECK (length(trim(definition)) > 0),
    approval_ref        TEXT NOT NULL CHECK (length(trim(approval_ref)) > 0),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT
);

INSERT INTO base_quantity_kinds (kind_id, definition, approval_ref, created_at, created_by_session) VALUES
 ('length', 'A distance measured along a straight line between two points of a room, a route or a fitting.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143'),
 ('gradient', 'The rise of a surface over its run; a ratio, a percentage and an angle in degrees are notations of this one kind, not kinds of their own.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143'),
 ('force', 'A push, pull or turn that a person must apply to operate or move something.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143'),
 ('time', 'A duration, such as how long a sound takes to decay or a door stays open.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143'),
 ('luminous_reflectance', 'The share of incident light a surface reflects (light reflectance value, LRV), and the contrast between two surfaces stated as the difference of their LRVs on that same scale.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143'),
 ('colour_temperature', 'The correlated colour temperature of a white light source, on the warm-to-cool scale.',
  'Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds', '2026-11-16 00:00', 'migration_143');

ALTER TABLE base_parameters ADD COLUMN quantity_kind TEXT REFERENCES base_quantity_kinds(kind_id);
ALTER TABLE base_parameters ADD COLUMN quantity_kind_observation_id INTEGER REFERENCES observed_terms(observation_id);

PRAGMA user_version = 143;
