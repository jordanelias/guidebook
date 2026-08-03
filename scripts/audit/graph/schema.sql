-- audit_graph.db — schema for the vectorized structural audit tool.
--
-- This database is a DERIVED, read-only build artifact rebuilt deterministically
-- from the repository by scripts/audit/graph/build.py. It is NOT migration-tracked,
-- NOT committed (see .gitignore), and never competes with data/guidebook.db.
-- It models the whole repository as a typed node/edge graph plus a findings ledger.

CREATE TABLE nodes (
    node_id   TEXT PRIMARY KEY,   -- "<kind>:<key>", e.g. "source:REF-00157", "db_table:items"
    kind      TEXT NOT NULL,      -- item|source|population|connection|gap|slug|term|conflict|
                                  -- decision|db_table|db_row|file|symbol|content|pydantic_model|
                                  -- skill|governance_rule|migration|stage|identifier
    key       TEXT NOT NULL,      -- natural key within kind
    subtype   TEXT,               -- e.g. table name for db_row; 'function'/'class' for symbol
    path      TEXT,               -- source file path when applicable
    label     TEXT,               -- short human label
    attrs     TEXT                -- JSON blob of extra attributes (state columns, counts, ...)
);
CREATE INDEX idx_nodes_kind ON nodes(kind);
CREATE INDEX idx_nodes_key  ON nodes(key);

CREATE TABLE edges (
    edge_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    src       TEXT NOT NULL,      -- node_id (source of the relationship)
    dst       TEXT NOT NULL,      -- node_id (may reference a non-existent node = dangling)
    etype     TEXT NOT NULL,      -- fk|junction|citation|ref|import|table_ref|prose_schema|
                                  -- membership|stage|migration_seq|model_table|self_ref
    src_path  TEXT,               -- where the edge was observed (file path)
    src_line  INTEGER,
    resolved  INTEGER NOT NULL DEFAULT 1,  -- 1 if dst node exists; 0 if dangling (set by resolve pass)
    attrs     TEXT
);
CREATE INDEX idx_edges_src   ON edges(src);
CREATE INDEX idx_edges_dst   ON edges(dst);
CREATE INDEX idx_edges_etype ON edges(etype);
CREATE INDEX idx_edges_resolved ON edges(resolved);

CREATE TABLE findings (
    finding_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    check_id    TEXT NOT NULL,    -- e.g. "orphan.uncited_source"
    severity    TEXT NOT NULL CHECK (severity IN ('ERROR','WARN','INFO')),
    node_id     TEXT,             -- subject node, when applicable
    message     TEXT NOT NULL,
    known_debt  TEXT,             -- known-debt entry id if suppressed (NULL = live finding)
    attrs       TEXT
);
CREATE INDEX idx_findings_check ON findings(check_id);
CREATE INDEX idx_findings_sev   ON findings(severity);
CREATE INDEX idx_findings_debt  ON findings(known_debt);

CREATE TABLE build_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
