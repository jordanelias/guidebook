-- 025_drop_colonial_role.sql
-- Remove COLONIAL from lang_jur_map.role CHECK; reset the table to empty; withdraw the
-- erroneous Stage-4.3 population migration from the ledger.
-- Per owner decision DR-2026-06-11-remove-colonial-role. COLONIAL originated in workplan A.3
-- (line 218) but was never defined; A.3's only examples mark colonial-legacy English SECONDARY.
-- data_20260611224657 was a premature population (migration 023 deferred it pending role
-- definitions) whose COLONIAL rows contradicted A.3's examples; its file is deleted in the same
-- commit and its ledger row removed here so committed == rebuild. The CHECK cannot be tightened
-- while that migration's COLONIAL inserts remain in replay (CI rebuilds schema-before-data),
-- hence the withdrawal. Forward-only exception, scoped to a same-day migration nothing depends on.
-- Runner sets PRAGMA user_version to 25.
BEGIN;
CREATE TABLE lang_jur_map_new (
    language            TEXT NOT NULL,
    jurisdiction        TEXT NOT NULL,
    role                TEXT NOT NULL
                        CHECK (role IN ('PRIMARY', 'SECONDARY')),
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT,
    PRIMARY KEY (language, jurisdiction)
);
DROP TABLE lang_jur_map;
ALTER TABLE lang_jur_map_new RENAME TO lang_jur_map;
DELETE FROM data_migrations WHERE migration_id = 'data_20260611224657_2026-06-11-stage-4-3-gate-closure';
COMMIT;
