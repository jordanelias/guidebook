-- 107_drop_item_layer_cluster.sql
-- SCHEMA migration -- the item layer is dropped from the schema (plan step 1.2; RULINGS R36).
--
-- THE OWNER'S REASON. The item layer was deleted from the database on 2026-09-01 because a
-- container named for its answer ("E-08 Corridor Clear Width (>=1200 mm Minimum on All Primary
-- Routes)") biases every finding filed into it (CLAUDE.md section 7; WRK-169, WRK-170). The
-- rows are gone; this removes the empty tables, the view and the foreign keys that still
-- pointed at them, so no writer can file into a container that no longer exists. WRK-170's
-- condition (the rows are archived) is met by _archived/data/corpus-pre-reset-2026-08-06.db and
-- the migration chain.
--
-- EVIDENCE (derived, 2026-10-14, before this migration; re-run rather than trust):
--   * every table below holds 0 rows:
--       select count(*) from <table>   -- each 0
--   * the only inbound foreign keys are from the tables below to `items`, and from `conflicts`
--     (also 0 rows) to `items`; `probe_population_links` points at `spec_value_probes`:
--       pragma foreign_key_list on every table
--   * the only view reading any of them is v_pmp_latest_walk (reads spec_value_probes); no trigger
--     reads any of them (sqlite_master).
--   * data migrations that write them:
--       grep -lE "(INSERT( OR [A-Z]+)? INTO|UPDATE|DELETE FROM) \"?<table>\"?[ (]" scripts/migrations/data_*.sql
--     finds only data_20260821185514 (jurisdictional_values) and data_20260901183203
--     (item_taxonomy_links). Both precede 095's AFTER_DATA marker (20260920060857), so the
--     runner replays them before this migration; no data migration after the marker names any
--     of these tables, so no marker is needed here.
--
-- WHAT IS DROPPED: items, item_audit_runs, item_bpc_links, item_taxonomy_links,
-- item_population_elaborations, term_item_links, room_items, case_study_specs,
-- economics_entry_specs, spec_value_probes, probe_population_links, jurisdictional_values, and
-- the view v_pmp_latest_walk.
--
-- WHAT IS REBUILT: `conflicts` (0 rows) keeps `item_code` as a plain column, without its
-- foreign key into `items`, by the 081 procedure (create the new table from the live DDL
-- changing only that line, copy, drop, rename, recreate the three indexes). The column and its
-- unique index stay: a writer still names an item code there, and dropping a column a writer
-- names is that writer's retirement, not this migration's (CLAUDE.md rule 5).

DROP VIEW v_pmp_latest_walk;
DROP TABLE probe_population_links;
DROP TABLE spec_value_probes;
DROP TABLE item_audit_runs;
DROP TABLE item_bpc_links;
DROP TABLE item_taxonomy_links;
DROP TABLE item_population_elaborations;
DROP TABLE term_item_links;
DROP TABLE room_items;
DROP TABLE case_study_specs;
DROP TABLE economics_entry_specs;
DROP TABLE jurisdictional_values;

CREATE TABLE "_107_new_conflicts" (
    conflict_id         TEXT PRIMARY KEY,
    item_code           TEXT,
    domain              TEXT NOT NULL,
    pop_a               TEXT NOT NULL,
    pop_b               TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
                        )),
    resolution          TEXT,
    evidence            TEXT,
    gap_id              TEXT,
    source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

INSERT INTO "_107_new_conflicts" SELECT * FROM "conflicts";
DROP TABLE "conflicts";
ALTER TABLE "_107_new_conflicts" RENAME TO "conflicts";
CREATE UNIQUE INDEX idx_conflicts_dedup  ON conflicts(item_code, domain, pop_a, pop_b);
CREATE INDEX idx_conflicts_status ON conflicts(status);
CREATE INDEX idx_conflicts_item   ON conflicts(item_code);

DROP TABLE items;

PRAGMA user_version = 107;
