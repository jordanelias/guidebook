# D-0139 Amendment 2 — Website Entity Tables
**Created:** 2026-05-04 07:30 UTC
**Amends:** `architecture/schema-spec.md`
**Authority:** B3.2 (workplan-co0007-v4.md) + navigation-modes.md
**Decision category:** D-SCHEMA / DG-REVIEW
**Status:** ACTIVE

---

## 1. Summary

This amendment adds three new entity tables (doctrine, room, specialist) and their join tables. These entities serve the `/foundations/`, `/rooms/`, and `/specialists/` URL families defined in navigation-modes.md §3.

---

## 2. Table: `doctrine`

```sql
CREATE TABLE doctrine (
  doctrine_id      TEXT PRIMARY KEY,           -- DOC-NNNN
  slug             TEXT NOT NULL UNIQUE,        -- URL slug
  title            TEXT NOT NULL,
  doctrine_group   TEXT NOT NULL CHECK (doctrine_group IN ('core','evidence','ethics','frameworks')),
  statement        TEXT NOT NULL,               -- Authoritative prose
  implications     TEXT,                        -- Implications for practice
  body_md          TEXT,                        -- Full prose (markdown)
  part_section     TEXT,                        -- §1.x reference
  status           TEXT CHECK (status IN ('active','superseded')) DEFAULT 'active',
  notes            TEXT,
  created_at       TEXT NOT NULL,
  modified_at      TEXT NOT NULL
);

CREATE INDEX idx_doctrine_group (doctrine_group);
CREATE INDEX idx_doctrine_slug (slug);
```

### Join table: `doctrine_specification`

```sql
CREATE TABLE doctrine_specification (
  doctrine_id      TEXT NOT NULL,
  item_code        TEXT NOT NULL,
  PRIMARY KEY (doctrine_id, item_code),
  FOREIGN KEY (doctrine_id) REFERENCES doctrine(doctrine_id),
  FOREIGN KEY (item_code) REFERENCES specification(item_code)
);
```

---

## 3. Table: `room`

```sql
CREATE TABLE room (
  room_id          TEXT PRIMARY KEY,           -- R-ENT, R-BA, etc.
  room_label       TEXT NOT NULL,
  building_type    TEXT NOT NULL CHECK (building_type IN ('residential','non-residential')),
  part_source      INTEGER NOT NULL CHECK (part_source IN (6, 7)),
  section          TEXT,                        -- §6.1, §7.3, etc.
  criticality_note TEXT,
  evidence_density TEXT,                        -- ■ / ▓ / ░ / ·
  status           TEXT CHECK (status IN ('active','draft','retired')) DEFAULT 'active',
  notes            TEXT,
  created_at       TEXT NOT NULL,
  modified_at      TEXT NOT NULL
);

CREATE INDEX idx_room_building_type (building_type);
CREATE INDEX idx_room_part (part_source);
```

### Join table: `room_item`

```sql
CREATE TABLE room_item (
  room_id          TEXT NOT NULL,
  item_code        TEXT NOT NULL,
  design_stage     TEXT,                        -- SD, DD, CD, RFO
  must_appear_on   TEXT,                        -- Drawing reference
  notes            TEXT,
  PRIMARY KEY (room_id, item_code),
  FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE INDEX idx_room_item_stage (design_stage);
```

### Join table: `room_item_population`

```sql
CREATE TABLE room_item_population (
  room_id          TEXT NOT NULL,
  item_code        TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  applicability    TEXT CHECK (applicability IN ('primary','secondary')),
  PRIMARY KEY (room_id, item_code, population_code),
  FOREIGN KEY (room_id, item_code) REFERENCES room_item(room_id, item_code),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
```

### Table: `room_dar_provision`

```sql
CREATE TABLE room_dar_provision (
  provision_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id          TEXT NOT NULL,
  description      TEXT NOT NULL,
  construction_stage TEXT,
  drawing_reference TEXT,
  notes            TEXT,
  FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE INDEX idx_room_dar_room (room_id);
```

### Table: `room_conflict`

```sql
CREATE TABLE room_conflict (
  conflict_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id          TEXT NOT NULL,
  description      TEXT NOT NULL,
  resolution       TEXT,
  conflict_domain  TEXT,                        -- Links to conflict entity
  FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE INDEX idx_room_conflict_room (room_id);
```

---

## 4. Table: `specialist`

```sql
CREATE TABLE specialist (
  specialist_id    TEXT PRIMARY KEY,           -- SPEC-ROLE-NN
  role             TEXT NOT NULL UNIQUE,        -- OT, dementia-design, etc.
  role_label       TEXT NOT NULL,               -- Human-readable
  part_section     TEXT,                        -- §9.x reference
  role_description TEXT NOT NULL,
  assessment_format TEXT,
  co_design_notes  TEXT,
  guidebook_relationship TEXT,
  status           TEXT CHECK (status IN ('active','retired')) DEFAULT 'active',
  notes            TEXT,
  created_at       TEXT NOT NULL,
  modified_at      TEXT NOT NULL
);
```

### Table: `specialist_trigger`

```sql
CREATE TABLE specialist_trigger (
  trigger_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  specialist_id    TEXT NOT NULL,
  trigger_text     TEXT NOT NULL,
  FOREIGN KEY (specialist_id) REFERENCES specialist(specialist_id)
);

CREATE INDEX idx_specialist_trigger (specialist_id);
```

### Table: `specialist_stage_scope`

```sql
CREATE TABLE specialist_stage_scope (
  scope_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  specialist_id    TEXT NOT NULL,
  stage            TEXT NOT NULL,               -- SD, DD, CD, RFO
  scope_text       TEXT NOT NULL,
  FOREIGN KEY (specialist_id) REFERENCES specialist(specialist_id)
);

CREATE INDEX idx_specialist_stage (specialist_id, stage);
```

### Join table: `specialist_specification`

```sql
CREATE TABLE specialist_specification (
  specialist_id    TEXT NOT NULL,
  item_code        TEXT NOT NULL,
  PRIMARY KEY (specialist_id, item_code),
  FOREIGN KEY (specialist_id) REFERENCES specialist(specialist_id)
);
```

### Join table: `specialist_population`

```sql
CREATE TABLE specialist_population (
  specialist_id    TEXT NOT NULL,
  population_code  TEXT NOT NULL,
  PRIMARY KEY (specialist_id, population_code),
  FOREIGN KEY (specialist_id) REFERENCES specialist(specialist_id),
  FOREIGN KEY (population_code) REFERENCES population(code)
);
```

---

## 5. D-SCHEMA records

| ID | Entity | Decision | Delegation |
|---|---|---|---|
| D-SCHEMA-019 | doctrine | New entity table + doctrine_specification join | DG-REVIEW |
| D-SCHEMA-020 | room | New entity table + 4 sub-tables (room_item, room_item_population, room_dar_provision, room_conflict) | DG-REVIEW |
| D-SCHEMA-021 | specialist | New entity table + 3 sub-tables (specialist_trigger, specialist_stage_scope, specialist_specification) + specialist_population join | DG-REVIEW |

---

## 6. Change log

| Date | Change |
|---|---|
| 2026-05-04 07:30 | D-0139 Amendment 2 issued. 3 entity tables, 8 sub/join tables. |
