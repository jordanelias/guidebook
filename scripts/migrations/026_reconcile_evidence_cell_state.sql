-- 026_reconcile_evidence_cell_state.sql
-- Schema migration: reconcile migration 024's evidence_cell_state (item_code x
-- population_code identity, directness-aware convergence_assessment table)
-- with the provenance/reproducibility design proposed in
-- workplan/best-practices-assessment-system.md §4 (governing_refs/
-- derivation_sha/rule_version), per
-- decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md (v2,
-- revised after adversarial review -- see that DR's "Revision history").
-- STATUS: that DR is PROPOSED, pending owner ratification -- this migration
-- implements the DR's recommendation so it can be reviewed and tested, but is
-- not itself a claim that the reconciliation has been owner-approved.
--
-- RECONCILIATION (v2 -- corrects the v1 draft's jurisdiction-in-key error):
--   * KEEPS 024's cell identity (item_code, population_code) -- no canonical
--     `specification` table exists in the migration-built DB; item_code
--     remains the FK-valid parameter key. item_bpc_links (migration 013,
--     meant to succeed the single-string bpc_source_slug for items with
--     multiple governing BPCs) is only 1/92 populated, so slug-based identity
--     would be a strictly worse join today, not just an unavailable one.
--   * KEEPS 024's convergence_assessment table and FK unchanged -- richer and
--     directness-aware; NOT regressed to a flat `convergence` enum.
--   * DOES NOT add jurisdiction to this table at all (v1 draft added it to the
--     UNIQUE key; adversarial review + tier-system.md's own corridor-width
--     doctrine established that conflates "best practice" (jurisdiction-
--     agnostic by definition) with "code floor" (inherently jurisdiction-
--     specific) -- exactly the failure mode tier-system.md names). Jurisdiction-
--     specific code values get their own table, see jurisdictional_values below.
--   * ADDS the provenance/reproducibility columns the existing table lacks:
--     tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only,
--     falsification_condition. Does NOT add a `confidence_bucket` column (v1
--     draft added one; no derivation rule from confidence_dimensions_present/
--     absent exists anywhere in the repo, and an undefined, unenforced mapping
--     between two representations of the same fact is a driftable redundant
--     field -- deferred until a real derivation rule and consistency check
--     exist to back it).
--   * REPLACES the v1 draft's unstructured `value_range TEXT` with
--     `value_min REAL, value_max REAL, value_unit TEXT` -- structured to match
--     the convention data/jurisdictional_values/*.yaml already uses
--     (value_numeric/unit), so a code-floor-vs-best-practice delta is a plain
--     numeric comparison, not string parsing.
--   * ADDS `jurisdictional_values` (new; loads data/jurisdictional_values/
--     *.yaml, currently uncommitted to the DB, in the companion data
--     migration data_20260712150000_jurisdictional-values-backfill.sql).
--   * FIXES v_best_practice (present in the v1 draft without this filter) to
--     exclude code_floor_only=1 rows -- per best-practices-assessment-system.md
--     §3's own hard rule, a Tier-6-only cell is provisional/code-floor-only,
--     never a best-practice determination, and the "transparent surface, never
--     drift" view must not surface it as one.
--   * ADDS v_code_floor_only as a join against jurisdictional_values so the
--     code-floor-delta surface promised in best-practices-assessment-system.md
--     §4 Phase 4 is actually computable from structured columns.
--
-- evidence_cell_state and convergence_assessment both have 0 rows (confirmed
-- at authoring time); this is a schema-only rebuild via create-copy-drop-rename
-- (SQLite cannot alter a UNIQUE constraint in place), matching the pattern
-- migration 025 used. The runner sets PRAGMA user_version to 26 after applying.

BEGIN;

CREATE TABLE evidence_cell_state_new (
    cell_id                        INTEGER PRIMARY KEY,
    item_code                      TEXT NOT NULL REFERENCES items(item_code),
    population_code                TEXT NOT NULL REFERENCES populations(population_code),
    state                          TEXT NOT NULL
                                   CHECK (state IN ('stated', 'provisional',
                                                    'pending', 'not_applicable')),
    design_scale                   TEXT
                                   CHECK (design_scale IN ('universal', 'population', 'person')),
    convergence_id                 INTEGER REFERENCES convergence_assessment(convergence_id),
    -- provisional confidence flag (§2.3, unchanged from migration 024)
    confidence_dimensions_present   TEXT,   -- JSON array
    confidence_dimensions_absent    TEXT,   -- JSON array
    confidence_synthesis_basis      TEXT,
    -- pending gap link (§2.4, unchanged)
    gap_register_id                TEXT REFERENCES gaps(gap_id),
    -- not_applicable rationale (§2.5, unchanged)
    not_applicable_rationale        TEXT,
    -- provenance / reproducibility (new)
    tier_basis                     TEXT,    -- e.g. 'T1+CO1' / 'T3' / 'T6-only'
    governing_refs                 TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs)),
    rule_version                   TEXT,    -- determination-algorithm version that produced this row
    derivation_sha                 TEXT,    -- hash of (sorted governing_refs + rule_version); staleness check
    code_floor_only                INTEGER NOT NULL DEFAULT 0
                                   CHECK (code_floor_only IN (0, 1)),
    -- within-population evidence-anchored range (doctrine #1), structured
    value_min                      REAL,
    value_max                      REAL,
    value_unit                     TEXT,
    falsification_condition        TEXT,    -- what evidence would overturn this (doctrine #6)
    -- source-quality flags (unchanged)
    has_unverified_sources          INTEGER NOT NULL DEFAULT 0
                                    CHECK (has_unverified_sources IN (0, 1)),
    all_sources_disqualified        INTEGER NOT NULL DEFAULT 0
                                    CHECK (all_sources_disqualified IN (0, 1)),
    created_at                     TEXT,
    created_by_session              TEXT,
    updated_at                      TEXT,
    updated_by_session               TEXT,
    UNIQUE (item_code, population_code)
);

INSERT INTO evidence_cell_state_new (
    cell_id, item_code, population_code, state, design_scale,
    convergence_id, confidence_dimensions_present, confidence_dimensions_absent,
    confidence_synthesis_basis, gap_register_id, not_applicable_rationale,
    has_unverified_sources, all_sources_disqualified,
    created_at, created_by_session, updated_at, updated_by_session
)
SELECT
    cell_id, item_code, population_code, state, design_scale,
    convergence_id, confidence_dimensions_present, confidence_dimensions_absent,
    confidence_synthesis_basis, gap_register_id, not_applicable_rationale,
    has_unverified_sources, all_sources_disqualified,
    created_at, created_by_session, updated_at, updated_by_session
FROM evidence_cell_state;

DROP TABLE evidence_cell_state;
ALTER TABLE evidence_cell_state_new RENAME TO evidence_cell_state;

CREATE INDEX idx_cell_state_item  ON evidence_cell_state(item_code);
CREATE INDEX idx_cell_state_pop   ON evidence_cell_state(population_code);
CREATE INDEX idx_cell_state_state ON evidence_cell_state(state);

-- weighting_profile (new; best-practices-assessment-system.md §5, unchanged design)
CREATE TABLE weighting_profile (
    audience        TEXT NOT NULL,
    use_pattern     TEXT NOT NULL,
    tier_weights    TEXT NOT NULL CHECK (json_valid(tier_weights)),
    notes           TEXT,
    PRIMARY KEY (audience, use_pattern)
);

-- Jurisdiction-specific code-floor values (new). Normalizes
-- data/jurisdictional_values/*.yaml (109 records across 20 files, currently
-- not loaded into the DB at all) into a real table, kept deliberately SEPARATE
-- from evidence_cell_state so a jurisdiction-specific regulatory minimum can
-- never be mistaken for -- or silently join into a view alongside -- a
-- jurisdiction-agnostic best-practice determination.
CREATE TABLE jurisdictional_values (
    jv_id               INTEGER PRIMARY KEY,
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    jurisdiction         TEXT NOT NULL,
    spec_id              TEXT,    -- informational only (e.g. 'SPEC-0050'); no
                                  -- specification table exists to FK against
    standard_name        TEXT,
    value_text           TEXT,
    value_numeric         REAL,
    unit                 TEXT,
    is_code_minimum       INTEGER CHECK (is_code_minimum IS NULL OR is_code_minimum IN (0, 1)),
    evidence_tier         INTEGER NOT NULL DEFAULT 6,   -- code/regulatory values are Tier 6 by definition
    source_section        TEXT,
    notes                TEXT,
    created_at            TEXT,
    created_by_session     TEXT,
    updated_at            TEXT,
    updated_by_session      TEXT,
    UNIQUE (item_code, jurisdiction, standard_name)
);

CREATE INDEX idx_jur_values_item ON jurisdictional_values(item_code);
CREATE INDEX idx_jur_values_jur  ON jurisdictional_values(jurisdiction);

-- Derived views (best-practices-assessment-system.md §4 -- "the transparent
-- surfaces, never drift"). v_best_practice EXCLUDES code_floor_only=1 (fixed
-- from the v1 draft, which omitted this filter and would have surfaced
-- Tier-6-only code-floor rows as "best practice" -- the exact conflation
-- tier-system.md's corridor-width example names as the failure mode this
-- schema exists to prevent).
CREATE VIEW v_best_practice AS
    SELECT * FROM evidence_cell_state
    WHERE state IN ('stated', 'provisional') AND code_floor_only = 0;

CREATE VIEW v_pending AS
    SELECT ecs.*, g.description AS gap_description, g.category AS gap_category,
           g.priority AS gap_priority
    FROM evidence_cell_state ecs
    JOIN gaps g ON g.gap_id = ecs.gap_register_id
    WHERE ecs.state = 'pending';

CREATE VIEW v_divergence AS
    SELECT ecs.*, ca.status AS convergence_status, ca.rationale AS convergence_rationale,
           ca.synthesis_approach AS convergence_synthesis_approach
    FROM evidence_cell_state ecs
    JOIN convergence_assessment ca ON ca.convergence_id = ecs.convergence_id
    WHERE ca.status = 'divergent';

-- Joins against jurisdictional_values (not just a self-filter) so the
-- code-floor-delta surface promised in best-practices-assessment-system.md
-- §4 Phase 4 is actually computable: code_value/code_unit alongside the
-- cell's own value_min/value_max/value_unit.
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, jv.jurisdiction, jv.standard_name,
           jv.value_numeric AS code_value, jv.unit AS code_unit
    FROM evidence_cell_state ecs
    LEFT JOIN jurisdictional_values jv ON jv.item_code = ecs.item_code
    WHERE ecs.code_floor_only = 1;

COMMIT;
