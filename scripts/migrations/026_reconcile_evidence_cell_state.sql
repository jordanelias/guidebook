-- 026_reconcile_evidence_cell_state.sql
-- Schema migration: reconcile migration 024's evidence_cell_state (item_code x
-- population_code identity, directness-aware convergence_assessment table)
-- with the provenance/reproducibility design proposed in
-- workplan/best-practices-assessment-system.md §4 (slug x population x
-- jurisdiction, governing_refs/derivation_sha/rule_version), per
-- decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md.
-- STATUS: that DR is PROPOSED, pending owner ratification -- this migration
-- implements the DR's recommendation so it can be reviewed and tested, but is
-- not itself a claim that the reconciliation has been owner-approved.
--
-- RECONCILIATION:
--   * KEEPS 024's cell identity (item_code, population_code) -- no canonical
--     `specification`/`slug` table exists in the migration-built DB; item_code
--     remains the FK-valid parameter key (see 024's own header note).
--   * KEEPS 024's convergence_assessment table and FK unchanged -- richer and
--     directness-aware (down_weighted_sources/discounted_sources per DR-2026-05-29
--     §1.7); NOT regressed to the proposal's flatter `convergence` enum.
--   * ADDS a `jurisdiction` column, TEXT NOT NULL DEFAULT '' (empty string, not
--     NULL, means jurisdiction-agnostic -- SQLite does not treat NULL as equal
--     to itself in a UNIQUE constraint, so a nullable column here would
--     silently allow duplicate agnostic rows for the same cell).
--   * ADDS the proposal's provenance/reproducibility columns the existing table
--     lacks: tier_basis, governing_refs, rule_version, derivation_sha,
--     code_floor_only, value_range, falsification_condition, confidence_bucket
--     (kept alongside, not instead of, the existing confidence_dimensions_*
--     fields already relied on by scripts/validate_evidence_state.py).
--   * ADDS weighting_profile and four derived views exactly as proposed,
--     adjusted to the gaps table's real columns (description/category/priority)
--     and to the merged schema's convergence_assessment join.
--
-- Both evidence_cell_state and convergence_assessment have 0 rows (confirmed
-- at authoring time), so this is a schema-only rebuild with nothing to migrate
-- forward via INSERT...SELECT beyond a straight copy. The runner sets
-- PRAGMA user_version to 26 after applying.

BEGIN;

CREATE TABLE evidence_cell_state_new (
    cell_id                        INTEGER PRIMARY KEY,
    item_code                      TEXT NOT NULL REFERENCES items(item_code),
    population_code                TEXT NOT NULL REFERENCES populations(population_code),
    jurisdiction                   TEXT NOT NULL DEFAULT '',   -- '' = jurisdiction-agnostic
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
    -- queryable confidence summary (new; from best-practices-assessment-system.md §4)
    confidence_bucket              TEXT CHECK (confidence_bucket IS NULL
                                              OR confidence_bucket IN ('high', 'medium', 'low')),
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
    value_range                    TEXT,    -- within-population range (doctrine #1)
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
    UNIQUE (item_code, population_code, jurisdiction)
);

INSERT INTO evidence_cell_state_new (
    cell_id, item_code, population_code, jurisdiction, state, design_scale,
    convergence_id, confidence_dimensions_present, confidence_dimensions_absent,
    confidence_synthesis_basis, gap_register_id, not_applicable_rationale,
    has_unverified_sources, all_sources_disqualified,
    created_at, created_by_session, updated_at, updated_by_session
)
SELECT
    cell_id, item_code, population_code, '', state, design_scale,
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
CREATE INDEX idx_cell_state_jur   ON evidence_cell_state(jurisdiction);

-- weighting_profile (new; best-practices-assessment-system.md §5, unchanged design)
CREATE TABLE weighting_profile (
    audience        TEXT NOT NULL,
    use_pattern     TEXT NOT NULL,
    tier_weights    TEXT NOT NULL CHECK (json_valid(tier_weights)),
    notes           TEXT,
    PRIMARY KEY (audience, use_pattern)
);

-- Derived views (best-practices-assessment-system.md §4 -- "the transparent
-- surfaces, never drift"). Adjusted to the real gaps/convergence_assessment
-- columns rather than the sketch's assumed shape.
CREATE VIEW v_best_practice AS
    SELECT * FROM evidence_cell_state WHERE state IN ('stated', 'provisional');

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

CREATE VIEW v_code_floor_only AS
    SELECT * FROM evidence_cell_state WHERE code_floor_only = 1;

COMMIT;
