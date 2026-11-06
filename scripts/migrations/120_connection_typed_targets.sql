-- 120_connection_typed_targets.sql  (replaces the earlier 120_connection_parameter_targets draft)
-- SCHEMA migration -- a connection points at what it connects by KEY, one kind per column, and the connection
-- type loses the deleted layer's name.
--
-- WHY. connection_targets.target was one TEXT cell holding whatever spelling a session chose: a slug, an
-- identity-lens code, a parameter, an extraction, a methodology, sometimes with a prefix ("item:E-08",
-- "population:MOB") that the reader had to parse to learn what kind of thing the cell held. That is data stored
-- in the wrong cell: the cell's meaning depended on a convention, nothing could join it, and a renamed or merged
-- parameter silently orphaned it. Owner, 2026-11-06: "we do NOT want to have data joined in cells ... or have data
-- stored in the wrong cell"; "more columns = more specificity = more flexibility".
--
-- Each target row now carries EXACTLY ONE of: parameter_id (base_parameters), slug (slugs), identity_code
-- (base_taxonomy_identity), extraction_id (source_value_extractions), or methodology (free text: the one kind with
-- no table of its own). Four are real foreign keys, so a dangling target cannot be written. READERS: the dedup
-- join in connection-discovery, `db.py connections`, and the render's cross-links between parameters.
--
-- connections.filed_in becomes a foreign key into slugs: it was already, by every writer's account, a topic slug,
-- typed as free text. connection_type 'CROSS-ITEM' becomes 'CROSS-PARAMETER' (the same relation, named for what
-- it now joins). The table holds no row when this is written (re-derive: SELECT COUNT(*) FROM connections), no
-- data migration writes either table (grep), and the old free-text targets cannot be mapped to a kind without
-- judgment, so none is copied. The guard below makes that loud: if an old target row exists its CHECK fails and
-- the migration aborts, instead of dropping targets silently.
--
-- Both tables are rebuilt (a CHECK or FK cannot be altered in place). connection_targets is the only table that
-- references connections (re-derive: PRAGMA foreign_key_list over every table). The indexes are recreated.

CREATE TABLE _old_targets_must_be_empty (n INTEGER NOT NULL CHECK (n = 0));
INSERT INTO _old_targets_must_be_empty SELECT COUNT(*) FROM connection_targets;
DROP TABLE _old_targets_must_be_empty;

CREATE TABLE connections_new (
    con_id              TEXT PRIMARY KEY,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )),
    confidence          TEXT NOT NULL
                        CHECK(confidence IN ('HIGH','MODERATE','SPECULATIVE')),
    connection_type     TEXT
                        CHECK(connection_type IN (
                            'CROSS-POPULATION','CROSS-PARAMETER',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )),
    filed_in            TEXT NOT NULL REFERENCES slugs(slug),
    description         TEXT,
    source_skill        TEXT,
    opus_reviewed       INTEGER NOT NULL DEFAULT 0 CHECK(opus_reviewed IN (0,1)),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

INSERT INTO connections_new
  SELECT con_id, status, confidence,
         CASE connection_type WHEN 'CROSS-ITEM' THEN 'CROSS-PARAMETER' ELSE connection_type END,
         filed_in, description, source_skill, opus_reviewed,
         created_at, created_by_session, updated_at, updated_by_session
  FROM connections;

CREATE TABLE connection_targets_new (
    target_id      INTEGER PRIMARY KEY,   -- a declared key: emit_batch_sql refuses to diff a table on implicit rowids
    con_id         TEXT NOT NULL REFERENCES connections_new(con_id),
    parameter_id   INTEGER REFERENCES base_parameters(parameter_id),
    slug           TEXT    REFERENCES slugs(slug),
    identity_code  TEXT    REFERENCES base_taxonomy_identity(identity_code),
    extraction_id  INTEGER REFERENCES source_value_extractions(extraction_id),
    methodology    TEXT,
    CHECK ((parameter_id IS NOT NULL) + (slug IS NOT NULL) + (identity_code IS NOT NULL)
           + (extraction_id IS NOT NULL) + (methodology IS NOT NULL) = 1),
    UNIQUE (con_id, parameter_id),
    UNIQUE (con_id, slug),
    UNIQUE (con_id, identity_code),
    UNIQUE (con_id, extraction_id),
    UNIQUE (con_id, methodology)
);

DROP TABLE connection_targets;
DROP TABLE connections;
ALTER TABLE connections_new RENAME TO connections;
ALTER TABLE connection_targets_new RENAME TO connection_targets;

CREATE INDEX idx_conn_status     ON connections(status);
CREATE INDEX idx_conn_confidence ON connections(confidence);
CREATE INDEX idx_conn_filed_in   ON connections(filed_in);
CREATE INDEX idx_ct_parameter    ON connection_targets(parameter_id);
CREATE INDEX idx_ct_slug         ON connection_targets(slug);
CREATE INDEX idx_ct_identity     ON connection_targets(identity_code);
CREATE INDEX idx_ct_extraction   ON connection_targets(extraction_id);

PRAGMA user_version = 120;
