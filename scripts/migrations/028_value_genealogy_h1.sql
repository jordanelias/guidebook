-- 028_value_genealogy_h1.sql
-- Per DR-2026-07-13-value-genealogy-and-derivation-handshake (ACCEPTED 2026-07-13,
-- ratification record decisions/RATIFICATION-RECORD-2026-07-13.md), item H1:
-- genealogy fields on the (empty) B6 source_value_extractions substrate, the
-- external-root registry that backs the anti-gaming root discipline, and the
-- v_value_independence discriminator view (best-practice-vs-consensus, computed
-- as COUNT(DISTINCT root_id) per parameter x population, excluding committee
-- assertions and untraced rows).
--
-- SCOPE NOTE (workplan/next-steps-synthesis-2026-07-14.md, Phase 0c): this is
-- the H1 slice only — the "columns before extraction row 1" prerequisite so the
-- Phase-E extraction pass is commissioned WITH genealogy from row one (DR §51:
-- "retrofit would be the expensive path"). H3 (population_icf_links + the
-- FDA->population crosswalk) and H4 (assess_cell derivation-path gates) are
-- determination-time, downstream of extraction row 1, and land at their point of
-- use — not here. The table is empty (0 rows), so the added CHECKs are satisfied
-- vacuously and no backfill is required.

-- H1 genealogy columns on source_value_extractions.
-- (Added nullable; a CHECK on a nullable column passes on NULL, and ALTER ADD
--  COLUMN permits a REFERENCES clause when the default is NULL.)
ALTER TABLE source_value_extractions
    ADD COLUMN root_id TEXT;
ALTER TABLE source_value_extractions
    ADD COLUMN root_type TEXT
        CHECK (root_type IN (
            'measurement_primary', 'participatory_finding',
            'committee_assertion', 'derived_calculation', 'untraced'));
ALTER TABLE source_value_extractions
    ADD COLUMN root_ref_id TEXT REFERENCES evidence_sources(ref_id);
ALTER TABLE source_value_extractions
    ADD COLUMN echo_of TEXT;
ALTER TABLE source_value_extractions
    ADD COLUMN measurement_paradigm TEXT
        CHECK (measurement_paradigm IN (
            'swept_path_dynamic', 'static_turning_circle', 'static_clearance',
            'anthropometric_percentile', 'instrumented_physical_measurement',
            'route_metric', 'field_observation', 'participatory_spatial',
            'stated_unmeasured'));
ALTER TABLE source_value_extractions
    ADD COLUMN device_class TEXT
        CHECK (device_class IN (
            'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter',
            'bariatric_manual', 'bariatric_power', 'walker_rollator',
            'mixed', 'not_device_scoped'));
ALTER TABLE source_value_extractions
    ADD COLUMN root_population_note TEXT;
ALTER TABLE source_value_extractions
    ADD COLUMN file_anchor TEXT;
ALTER TABLE source_value_extractions
    ADD COLUMN root_classification_basis TEXT;
ALTER TABLE source_value_extractions
    ADD COLUMN contested INTEGER NOT NULL DEFAULT 0
        CHECK (contested IN (0, 1));

-- External-root registry: one row per out-of-corpus evidentiary root (e.g. the
-- 1970s VA/HUD anthropometric studies). The H1 anti-gaming discipline: a root_id
-- must resolve to EITHER an in-corpus evidence_sources.ref_id (via root_ref_id)
-- OR a registered external-root stub here, so two extractors cannot mint two ids
-- for one root and double the independence count.
CREATE TABLE IF NOT EXISTS external_root_registry (
    root_id             TEXT PRIMARY KEY,
    description         TEXT NOT NULL,
    root_type           TEXT
                          CHECK (root_type IN (
                              'measurement_primary', 'participatory_finding',
                              'committee_assertion', 'derived_calculation',
                              'untraced')),
    provenance          TEXT,
    root_population_note TEXT,
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT
);

-- The computable best-practice-vs-consensus discriminator (DR §H1): independent
-- traced roots per (canonical parameter x population). Untraced rows carry NULL
-- root_id and are excluded; committee_assertion rows are excluded so precedent
-- (counting documents) can never out-score evidence (counting roots).
DROP VIEW IF EXISTS v_value_independence;
CREATE VIEW v_value_independence AS
    SELECT COALESCE(parameter_canonical, parameter) AS parameter,
           population_code,
           COUNT(DISTINCT root_id) AS independent_root_count
    FROM source_value_extractions
    WHERE root_id IS NOT NULL
      AND (root_type IS NULL OR root_type <> 'committee_assertion')
    GROUP BY COALESCE(parameter_canonical, parameter), population_code;

-- Registry-discipline audit surface: extraction rows whose root_id resolves to
-- neither an in-corpus source nor a registered external root. Must stay empty;
-- a non-empty result is the "minted id" gaming signal the DR names.
DROP VIEW IF EXISTS v_unregistered_roots;
CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id, sve.slug, sve.parameter, sve.root_id
    FROM source_value_extractions sve
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id);
