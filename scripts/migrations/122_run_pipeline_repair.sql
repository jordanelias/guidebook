-- 122_run_pipeline_repair.sql
-- SCHEMA migration -- four typed facts that the run-pipeline skill states and no column held, found by two
-- operator walk-throughs of the skill on 2026-11-06 (scratchpad run-pipeline-defect-collation.md, adjudicated in
-- run-pipeline-adjudication.md). Owner, 2026-11-06: "add a column where a convention would otherwise carry a fact";
-- "one value in each cell and each fact in the cell that names it".
--
-- 1. base_parameters.direction_ref_id -- WHICH ADMITTED SOURCE the accessibility direction was read from. Ledger
--    2026-10-30 ACTION (6): a direction is "recorded from an admitted source and not hand-set". The writer
--    (db.py set-parameter-direction) refuses a direction with no source; the column is nullable because two live
--    rows predate the rule (re-derive: SELECT parameter_id FROM base_parameters WHERE accessibility_direction IS
--    NOT NULL AND direction_ref_id IS NULL). Reader: scripts/assess/assess_cell.py's report.
-- 2. conflicts.parameter_id -- the conflict mapper says "keyed on the parameter" and the table had only a free-text
--    domain label. Reader: db.py conflicts --parameter-id. The dedup index moves from the prose label to the key.
-- 3. lang_jur_map.scope_status -- which (language, jurisdiction) rows the research scope covers (ledger 2026-10-30
--    item 7: P1+P2+P3 in scope; Arabic, Bengali, Hindi, Swahili scoped out). Until now the scope lived only in a
--    workplan file and `db.py coverage` counted every map row as required. NULL = not yet recorded; the fill is a
--    data migration after the owner settles which map rows the declared jurisdiction vocabulary admits (the map
--    names jurisdictions schemas/enums.JurisdictionCode does not; derive: compare the two). Reader: db.py coverage.
-- 4. v_scan_ledger gains BLOCKED: a source whose processing_blocked_reason is set (no full text, paywalled, ...)
--    can never be read, so it is not NOT-READ debt. scan_debt.py prints it apart. Reader: scan_debt.py.
-- 5. connections.confidence loses SPECULATIVE. The connection-discovery skill rules "SPECULATIVE is a CR gap, never
--    a connection"; a writer refusing a value the CHECK admits would be a second vocabulary (rule 8), so the CHECK
--    is the one home. Both tables hold no row and no data migration inserts into them (derive:
--    grep -l "INSERT INTO connections" scripts/migrations/data_*.sql); the guard below aborts if a row exists.

ALTER TABLE base_parameters ADD COLUMN direction_ref_id TEXT REFERENCES evidence_sources(ref_id);

ALTER TABLE conflicts ADD COLUMN parameter_id INTEGER REFERENCES base_parameters(parameter_id);
DROP INDEX IF EXISTS idx_conflicts_dedup;
CREATE UNIQUE INDEX idx_conflicts_dedup ON conflicts(parameter_id, pop_a, pop_b);

ALTER TABLE lang_jur_map ADD COLUMN scope_status TEXT
    CHECK (scope_status IS NULL OR scope_status IN ('in-scope', 'scoped-out'));

CREATE TABLE _connections_must_be_empty (n INTEGER NOT NULL CHECK (n = 0));
INSERT INTO _connections_must_be_empty SELECT COUNT(*) FROM connections;
INSERT INTO _connections_must_be_empty SELECT COUNT(*) FROM connection_targets;
DROP TABLE _connections_must_be_empty;

DROP TABLE connection_targets;
DROP TABLE connections;
CREATE TABLE connections (
    con_id              TEXT PRIMARY KEY,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )),
    confidence          TEXT NOT NULL
                        CHECK(confidence IN ('HIGH','MODERATE')),
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
CREATE TABLE connection_targets (
    target_id      INTEGER PRIMARY KEY,   -- a declared key: emit_batch_sql refuses to diff a table on implicit rowids
    con_id         TEXT NOT NULL REFERENCES connections(con_id),
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
CREATE INDEX idx_conn_status     ON connections(status);
CREATE INDEX idx_conn_confidence ON connections(confidence);
CREATE INDEX idx_conn_filed_in   ON connections(filed_in);
CREATE INDEX idx_ct_parameter    ON connection_targets(parameter_id);
CREATE INDEX idx_ct_slug         ON connection_targets(slug);
CREATE INDEX idx_ct_identity     ON connection_targets(identity_code);
CREATE INDEX idx_ct_extraction   ON connection_targets(extraction_id);

DROP VIEW v_scan_ledger;
CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a non-absent extraction exists for the pair (any figure_role).
--   2 STATED-ABSENT      only claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 BLOCKED            the source carries a processing_blocked_reason (no full text,
--                        paywalled, ...): nothing of it can be read, so the pair is not
--                        reading debt until the block clears (migration 122).
--   4 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   5 READ-PARTIAL       only partial / fragment / abstract readings cover it.
--   6 NOT-READ           no reading covers it.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >=
-- parameter_id (the parameter existed when the reading was made), or targeted at that
-- parameter. Rows 1 and 2 win over readings because a row written is stronger evidence
-- than a reading recorded; 4 wins over 5 because a full reading supersedes a partial
-- one of the same source.
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id, e.processing_blocked_reason
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id, pr.processing_blocked_reason,
           (SELECT s.scan_id FROM source_scans s
             WHERE s.ref_id = pr.ref_id
               AND ((s.mode = 'catalogue' AND s.catalogue_version >= pr.parameter_id)
                 OR (s.mode = 'targeted' AND s.target_parameter_id = pr.parameter_id))
             ORDER BY (s.text_scope = 'full') DESC, (s.method = 'full-read') DESC,
                      s.scan_id DESC
             LIMIT 1) AS scan_id
      FROM pairs pr
)
SELECT b.ref_id,
       b.parameter_id,
       CASE
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent') THEN 'STATED-ABSENT'
         WHEN b.processing_blocked_reason IS NOT NULL THEN 'BLOCKED'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

PRAGMA user_version = 122;
