-- 028_value_genealogy_h1.sql
-- Per DR-2026-07-13-value-genealogy-and-derivation-handshake (ACCEPTED 2026-07-13,
-- ratification record decisions/RATIFICATION-RECORD-2026-07-13.md), item H1:
-- genealogy fields on the (empty) B6 source_value_extractions substrate, the
-- external-root registry that backs the anti-gaming root discipline, and the
-- v_value_independence discriminator view (best-practice-vs-consensus, computed
-- as independent traced roots per parameter x population).
--
-- SCOPE NOTE (workplan/next-steps-synthesis-2026-07-14.md, Phase 0c): H1 slice
-- only — the "columns before extraction row 1" prerequisite so the Phase-E
-- extraction pass is commissioned WITH genealogy from row one (DR §51: retrofit
-- is the expensive path). H3 (population_icf_links + FDA->population crosswalk)
-- and H4 (assess_cell derivation-path gates) land at their point of use.
--
-- ADVERSARIAL REVIEW (2026-07-14, independent pass; workplan/phase-e-execution-
-- log-2026-07-14.md): the v1 discriminator was inflatable three ways, all firing
-- on the first hand-authored extraction rows and invisible to an empty-table
-- rebuild. Fixes applied here:
--   * A/B: v_value_independence used a permissive filter that COUNTED
--     NULL-root_type rows (the default intermediate state of a fresh extraction)
--     and never consulted the registry audit. Replaced with a positive
--     root_type allow-list + a root-resolution clause (in-corpus ref OR
--     registered stub), so committee_assertion / untraced / unclassified /
--     unregistered-minted rows cannot score.
--   * C [HIGH]: two rows citing the SAME in-corpus source with DIFFERENT root_id
--     strings counted as two independent roots (the exact one-root-inflated-to-
--     many failure the DR exists to catch), and the registry audit was blind to
--     it. Discriminator now counts DISTINCT COALESCE(root_ref_id, root_id) — one
--     in-corpus source collapses to one root regardless of root_id string — and
--     a new v_root_id_conflicts view surfaces any ref<->id non-1:1. NOTE: this
--     hardens a gap in the RATIFIED DR discipline (a), which guaranteed a
--     root_id "resolves to" a root but never "one source => one id". Surfaced
--     for owner awareness; it exceeds the literal DR text to serve its intent.
--   * D: external_root_registry PRIMARY KEY dedups id STRINGS, not physical
--     roots (two stubs for one 1970s study). v_registry_duplicate_descriptions
--     surfaces exact-normalised-description dupes; near-duplicate stubs remain a
--     human-review discipline (no pure-SQL fuzzy match).
--   * E: grain caveats for consumers — a parameter split across canonicalised /
--     raw rows under-counts (safe direction); a pure-consensus value is ABSENT
--     from v_value_independence, not 0 (treat missing as zero independence).
--   * F: wrapped in a transaction so a mid-script failure rolls back cleanly
--     rather than half-migrating the table (precedent: migration 020).
--
-- The table is empty (0 rows), so the added CHECKs are satisfied vacuously and
-- no backfill is required. Apply ONLY through scripts/migrate_db.py (never a hand
-- ALTER of canonical) so the GAP-290 reproducibility invariant stays intact.

BEGIN;

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
-- OR a registered external-root stub here.
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
-- traced roots per (canonical parameter x population).
--   * root_type allow-list => committee_assertion, untraced and unclassified
--     (NULL) rows never score (precedent can never out-count evidence);
--   * resolution clause => a root_id must resolve to an in-corpus source or a
--     registered stub, so a minted/unregistered id cannot score;
--   * COUNT(DISTINCT COALESCE(root_ref_id, root_id)) => one in-corpus SOURCE is
--     one root however many root_id strings it was given (Finding C).
-- Consumer caveats (Finding E): a value absent here has zero independent roots
-- (treat missing as 0); population_code NULL rows share one bucket.
DROP VIEW IF EXISTS v_value_independence;
CREATE VIEW v_value_independence AS
    SELECT COALESCE(parameter_canonical, parameter) AS parameter,
           population_code,
           COUNT(DISTINCT COALESCE(root_ref_id, root_id)) AS independent_root_count
    FROM source_value_extractions
    WHERE root_type IN ('measurement_primary', 'participatory_finding',
                        'derived_calculation')
      AND (root_ref_id IS NOT NULL
           OR root_id IN (SELECT root_id FROM external_root_registry))
    GROUP BY COALESCE(parameter_canonical, parameter), population_code;

-- Registry-discipline audit: extraction rows whose root_id resolves to neither an
-- in-corpus source nor a registered external root (the "minted id" gaming signal).
-- The discriminator above already excludes these; this surfaces them for cleanup.
DROP VIEW IF EXISTS v_unregistered_roots;
CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id, sve.slug, sve.parameter, sve.root_id
    FROM source_value_extractions sve
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id);

-- Finding C audit: the one-root = one-id invariant among in-corpus rows. Any
-- in-corpus source carrying >1 root_id string, or any root_id spanning >1 source,
-- is a mis-classification that would have inflated independence pre-fix.
DROP VIEW IF EXISTS v_root_id_conflicts;
CREATE VIEW v_root_id_conflicts AS
    SELECT 'ref_id_has_multiple_root_ids' AS conflict_type,
           root_ref_id AS conflict_key,
           COUNT(DISTINCT root_id) AS distinct_count
    FROM source_value_extractions
    WHERE root_ref_id IS NOT NULL AND root_id IS NOT NULL
    GROUP BY root_ref_id HAVING COUNT(DISTINCT root_id) > 1
    UNION ALL
    SELECT 'root_id_spans_multiple_ref_ids' AS conflict_type,
           root_id AS conflict_key,
           COUNT(DISTINCT root_ref_id) AS distinct_count
    FROM source_value_extractions
    WHERE root_ref_id IS NOT NULL AND root_id IS NOT NULL
    GROUP BY root_id HAVING COUNT(DISTINCT root_ref_id) > 1;

-- Finding D audit: registry stubs that normalise to the same description (one
-- physical root registered twice). Near-duplicates (e.g. 'va1' vs 'va-1970')
-- remain a human-review discipline.
DROP VIEW IF EXISTS v_registry_duplicate_descriptions;
CREATE VIEW v_registry_duplicate_descriptions AS
    SELECT LOWER(TRIM(description)) AS normalised_description,
           COUNT(*) AS stub_count,
           GROUP_CONCAT(root_id, ', ') AS root_ids
    FROM external_root_registry
    GROUP BY LOWER(TRIM(description))
    HAVING COUNT(*) > 1;

COMMIT;
