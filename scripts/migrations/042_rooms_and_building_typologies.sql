-- 042_rooms_and_building_typologies.sql
-- SCHEMA migration — give stage 12's catalogue the tables it never had.
--
-- Stage 12 of the pipeline is "a catalogue of specifications / rooms / buildings /
-- case studies". Three of those four have tables:
--   specifications  items (93) + item_population_links (372)
--   case studies    case_studies + 4 child tables, all FK'd (0 rows — empty, not missing)
--   economics       economics_entries + 2 child tables (5 rows — thin, not missing)
-- Rooms and building typologies had NOTHING. This is the only structural break
-- in stages 1-12.
--
-- The absence is not theoretical. scripts/generate/room_page.py has been written
-- against five tables that have never existed (room, room_item,
-- room_item_population, room_conflict, room_dar_provision) and crashes on
-- 'no such table: room' — while site/rooms/ holds 17 rendered pages whose room
-- vocabulary exists only inside their own HTML titles. The catalogue layer has
-- been carried in generated output rather than in the database it is supposed to
-- derive from, which inverts the repo's own rule that the DB is canonical.
--
-- Codes follow the R-XXX convention already used in those 17 pages, so nothing
-- has to be renamed and the existing pages can be regenerated from the table.
--
-- Rooms sit PARALLEL to specifications: rooms is to items what a place is to a
-- design parameter, and room_items is the one genuinely new relationship -- a
-- room is an assembly of specifications. Nothing else is added on speculation.
-- A first draft also created room_populations and typology_rooms; both were
-- dropped before commit. A room's population demands are reachable through its
-- items' existing population links, and a typology-to-room junction is premature
-- while building_typologies has no rows. Add either when there is data that
-- cannot be expressed without it.
--
-- Forward-only; user_version -> 42.

CREATE TABLE IF NOT EXISTS rooms (
  room_code           TEXT PRIMARY KEY,
  name                TEXT NOT NULL,
  category            TEXT,
  description         TEXT,
  status              TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active','draft','retired')),
  notes               TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT,
  updated_at          TEXT,
  updated_by_session  TEXT
);

-- Building typologies: the setting a room sits in. case_studies.building_type
-- already records this as free text per case study; this gives that axis a
-- vocabulary to point at rather than restating it per row.
CREATE TABLE IF NOT EXISTS building_typologies (
  typology_code       TEXT PRIMARY KEY,
  name                TEXT NOT NULL,
  description         TEXT,
  status              TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active','draft','retired')),
  notes               TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT,
  updated_at          TEXT,
  updated_by_session  TEXT
);

-- Which specifications apply in which room, and how strongly.
CREATE TABLE IF NOT EXISTS room_items (
  room_code           TEXT NOT NULL REFERENCES rooms(room_code),
  item_code           TEXT NOT NULL REFERENCES items(item_code),
  applicability       TEXT NOT NULL DEFAULT 'applies'
                        CHECK (applicability IN ('applies','conditional','not-applicable')),
  applicability_note  TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT,
  PRIMARY KEY (room_code, item_code)
);

CREATE INDEX IF NOT EXISTS idx_room_items_item ON room_items(item_code);
