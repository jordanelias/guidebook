-- 121_conflicts_typed.sql
-- SCHEMA migration -- a conflict names its two populations by KEY, and the retired item column and the dedup index
-- that depended on it go.
--
-- WHY. conflicts.pop_a and pop_b were free text. The cross-population-conflict-mapper skill filed codes
-- (`VIS`, `DBL`, `OFS`) that base_taxonomy_identity, the identity lens every determination is keyed on, does not
-- hold; insert_conflict checked only that pop_a sorts before pop_b. Owner, 2026-11-06: "we do NOT want ... data
-- stored in the wrong cell"; "more columns = more specificity". Each is now a foreign key into
-- base_taxonomy_identity(identity_code), gap_id a foreign key into gaps, and pop_a < pop_b a CHECK rather than a
-- writer-only convention.
--
-- item_code is dropped: the item layer is deleted (CLAUDE.md section 7), add-conflict has refused the column
-- since the layer went, and no row can carry it. The unique index idx_conflicts_dedup was keyed on
-- (item_code, domain, pop_a, pop_b); with item_code always NULL, and SQLite treating NULLs as distinct, it
-- deduplicated nothing. It is replaced by a unique index on (domain, pop_a, pop_b), which does.
--
-- READERS: `db.py conflicts` and `add-conflict`/`update-conflict`; the conflict mapper's matrix; the render's
-- population-conflict statement. The table holds no row when this is written (re-derive: SELECT COUNT(*) FROM
-- conflicts); the guard below aborts the migration if one exists, rather than dropping it.

CREATE TABLE _conflicts_must_be_empty (n INTEGER NOT NULL CHECK (n = 0));
INSERT INTO _conflicts_must_be_empty SELECT COUNT(*) FROM conflicts;
DROP TABLE _conflicts_must_be_empty;

DROP TABLE conflicts;
CREATE TABLE conflicts (
    conflict_id         TEXT PRIMARY KEY,
    domain              TEXT NOT NULL,
    pop_a               TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    pop_b               TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
                        )),
    resolution          TEXT,
    evidence            TEXT,
    gap_id              TEXT REFERENCES gaps(gap_id),
    source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    CHECK (pop_a < pop_b)
);

CREATE UNIQUE INDEX idx_conflicts_dedup  ON conflicts(domain, pop_a, pop_b);
CREATE INDEX idx_conflicts_status ON conflicts(status);

PRAGMA user_version = 121;
