-- 076_never_reuse_identifiers.sql
--
-- AN IDENTIFIER IS NEVER REUSED, AND DELETING ITS ROWS IS NOT WHAT MAKES IT FREE.
--
-- The 2026-09-13 corpus clear (data_20260913040739) deleted every circulation row on
-- the owner's ruling. That was correct. What it did NOT do -- and what nobody noticed
-- until an adversarial pass -- is that emptying a table hands its identifiers back to
-- the next writer:
--
--   * `ref_id`   is computed as MAX+1 over every table holding one (dbcore.ref_id_high_water),
--                so the mark fell 982 -> 970 and the next mint was REF-00971, an id the
--                batch-07 session record, its attestation, the retrieval-log manifests and
--                PR #136 all attribute to a specific scooter-manoeuvring study. Sealed by
--                the data migration that accompanies this one, which retains the thirteen
--                retired refs as RETIRED rows in `source_locators`.
--
--   * `parameter_id` and `specification_id` are plain `INTEGER PRIMARY KEY`, i.e. rowid
--                aliases, and SQLite assigns MAX(rowid)+1. Emptying the table restarts them
--                at 1. There is no high-water function to blame here and nothing to grep:
--                the next `add-parameter` silently re-mints `parameter_id 1`, and the next
--                determination re-mints `specification_id 1`, while eleven data migrations,
--                two session records and their attestations on disk still name the old ones.
--
-- This migration closes the second and third cases the way SQLite provides for: AUTOINCREMENT,
-- which allocates from `sqlite_sequence` and is defined never to reuse a value even after the
-- table is emptied. The sequences are seeded to the pre-clear maxima (both 2, read from the
-- blob at 91478d4^), so the first parameter of the re-run is 3 and the first determination is 3.
--
-- WHY NOT A TOMBSTONE ROW, which is how the ref_id case is handled and would also hold the
-- floor: `base_parameters` could carry one honestly -- its `status` CHECK already admits
-- 'retired'. `specifications` could not: every column that makes a determination meaningful is
-- NOT NULL or CHECK-constrained (`parameter_id`, `state`, and D-0182's "at least one lens"),
-- so a tombstone there would have to be a fabricated determination. A fake row in the table
-- that holds the project's answers is a worse object than a sequence counter.
--
-- SO THIS IS TWO MECHANISMS ACROSS THREE KEYS -- tombstones for `ref_id`, AUTOINCREMENT for the
-- two integer keys -- and that is worth stating rather than dressing up as one rule. Both are
-- FLOORS: they repair identity after a delete has already destroyed it. The single rule that
-- would make both unnecessary is `retire in place, never hard-delete`, for which the mechanism is
-- already half-built (`evidence_sources.superseded_by_ref_id`, `base_parameters.status = 'retired'`,
-- `source_locators.status = 'RETIRED'`). Under that rule the high-water holds because the rows
-- never leave, and `assess_cell`'s re-determination refusal could key on NOT RETIRED rather than
-- NOT EXISTS, which is the supersede design the engine currently refuses to invent for itself.
-- That is a doctrine change and an owner decision, so it is named here and not smuggled in.
-- AUTOINCREMENT is compatible with it either way: belt and braces, not a competing answer.
--
-- THE REBUILD IS SAFE AT ANY ROW COUNT. `scripts/migrate_db.py` hoists
-- `PRAGMA foreign_keys = OFF` into autocommit around the whole file and restores it after, so
-- the inbound references -- `specifications.parameter_id`, `source_value_extractions.parameter_id`,
-- `specification_source_links.specification_id` -- survive the rebuild: SQLite resolves foreign
-- keys by NAME at statement time, so a table recreated under the same name keeps them valid.
-- Migration 071 rebuilt `specifications` by exactly this route.

-- EIGHT VIEWS ARE CALLERS OF THESE TABLES AND MUST BE SWEPT WITH THEM (CLAUDE.md rule 4,
-- "A VIEW IS A CALLER"). SQLite reparses the whole schema on ALTER TABLE ... RENAME and
-- refuses if any view is then unresolvable, so the rebuild below fails outright with
-- `error in view v_code_floor_only: no such table: main.base_parameters` unless the views
-- are dropped first. Caught by rehearsal, not by reading. They are recreated verbatim at
-- the foot of this file from the live schema -- not retyped -- so the rebuild changes the
-- two tables' key allocation and nothing else about what any reader sees.

DROP VIEW v_pending;
DROP VIEW v_divergence;
DROP VIEW v_best_practice;
DROP VIEW v_code_floor_only;
DROP VIEW v_source_reach_all;
DROP VIEW v_item_provenance;
DROP VIEW v_unregistered_roots;
DROP VIEW v_value_independence;

-- A COPYING REBUILD, NOT A DROP/CREATE, and the difference is not academic. The first
-- cut of this file dropped both tables and guarded that with
-- `SELECT RAISE(ABORT, ...) WHERE (SELECT COUNT(*) ...) <> 0`. Two things were wrong.
-- SQLite's RAISE() is valid ONLY inside a trigger body, so the guard was a syntax error
-- that the rehearsal caught and a reader would have believed -- an assertion that cannot
-- fire is worse than none. And a migration that is correct only on an empty table is a
-- migration that can only ever be run today: a rebuild from migration history, or a
-- restore, or a replay on any database where these rows exist, would have hit the guard
-- or silently discarded data. This form copies whatever is there and is correct at 0 rows
-- or 10,000, so no guard is needed.
CREATE TABLE base_parameters_new (
    -- AUTOINCREMENT (076): never reissue a parameter_id. Eleven data migrations on disk
    -- name parameter_id 1 and 2; those ids mean `ramp gradient` and `corridor width` and
    -- must not come to mean anything else.
    parameter_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    -- UNIQUE: one parameter per term. A second row for the same term is the dual home
    -- rule 5 forbids; `add-term` already refuses a duplicate canonical_en upstream.
    term_id             TEXT    NOT NULL UNIQUE REFERENCES terms(term_id),
    status              TEXT    NOT NULL DEFAULT 'active'
                                CHECK (status IN ('active', 'merged', 'retired')),
    merged_into         INTEGER REFERENCES base_parameters(parameter_id),
    notes               TEXT,
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    -- merged_into is meaningful only for a merged row, and required for one.
    CHECK ((status = 'merged' AND merged_into IS NOT NULL)
        OR (status <> 'merged' AND merged_into IS NULL))
);

INSERT INTO base_parameters_new
    (parameter_id, term_id, status, merged_into, notes,
     created_at, created_by_session, updated_at, updated_by_session)
SELECT parameter_id, term_id, status, merged_into, notes,
       created_at, created_by_session, updated_at, updated_by_session
  FROM base_parameters;
DROP TABLE base_parameters;
ALTER TABLE base_parameters_new RENAME TO base_parameters;

CREATE TABLE specifications_new (
    -- AUTOINCREMENT (076): never reissue a specification_id. See the header.
    specification_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,
    -- which is why no determination could be written at all.
    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is
    -- retired in favour of these. NULL in a lens means "this determination is not
    -- stated in that lens", which is legitimate; stating several at once is the ideal.
    identity_code                   TEXT REFERENCES populations(population_code),
    icf_code                        TEXT REFERENCES axes(axis_code),
    needs_code                      TEXT REFERENCES access_needs(need_code),
    medical_code                    TEXT REFERENCES base_taxonomy_medical(medical_code),
    state                           TEXT NOT NULL
                                    CHECK (state IN ('stated', 'provisional',
                                                     'pending', 'not_applicable')),
    design_scale                    TEXT
                                    CHECK (design_scale IN ('universal', 'population', 'person')),
    convergence_id                  INTEGER REFERENCES convergence_assessment(convergence_id),
    confidence_dimensions_present   TEXT,   -- JSON array
    confidence_dimensions_absent    TEXT,   -- JSON array
    confidence_synthesis_basis      TEXT,
    gap_register_id                 TEXT REFERENCES gaps(gap_id),
    not_applicable_rationale        TEXT,
    tier_basis                      TEXT,
    governing_refs                  TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs)),
    rule_version                    TEXT,
    derivation_sha                  TEXT,
    code_floor_only                 INTEGER NOT NULL DEFAULT 0
                                    CHECK (code_floor_only IN (0, 1)),
    value_min                       REAL,
    value_max                       REAL,
    value_unit                      TEXT,
    falsification_condition         TEXT,
    has_unverified_sources          INTEGER NOT NULL DEFAULT 0
                                    CHECK (has_unverified_sources IN (0, 1)),
    all_sources_disqualified        INTEGER NOT NULL DEFAULT 0
                                    CHECK (all_sources_disqualified IN (0, 1)),
    regulatory_stratum_only         INTEGER NOT NULL DEFAULT 0
                                    CHECK (regulatory_stratum_only IN (0, 1)),
    created_at                      TEXT,
    created_by_session              TEXT,
    updated_at                      TEXT,
    updated_by_session              TEXT,
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);

INSERT INTO specifications_new
SELECT specification_id, parameter_id, identity_code, icf_code, needs_code, medical_code,
       state, design_scale, convergence_id, confidence_dimensions_present,
       confidence_dimensions_absent, confidence_synthesis_basis, gap_register_id,
       not_applicable_rationale, tier_basis, governing_refs, rule_version, derivation_sha,
       code_floor_only, value_min, value_max, value_unit, falsification_condition,
       has_unverified_sources, all_sources_disqualified, regulatory_stratum_only,
       created_at, created_by_session, updated_at, updated_by_session
  FROM specifications;
DROP TABLE specifications;
ALTER TABLE specifications_new RENAME TO specifications;

-- Recreated verbatim from the pre-076 schema. THE CELL'S IDENTITY, and the reason
-- `assess_cell` refuses a second determination of the same cell. The rebuild dropped it
-- with the old table, so it is recreated here rather than assumed to have survived.
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
);

-- Seed the sequences to the pre-clear maxima so the re-run starts at 3, not 1.
-- `sqlite_sequence` rows are normally created lazily on first insert; writing them
-- ahead of time is the documented way to set a starting point, and SQLite reads
-- seq+1 as the next value. Both maxima were 2, read from data/guidebook.db at 91478d4^
-- (the commit before the clear) rather than typed from memory.
DELETE FROM sqlite_sequence WHERE name IN ('base_parameters', 'specifications');
INSERT INTO sqlite_sequence (name, seq) VALUES ('base_parameters', 2), ('specifications', 2);

-- The eight views, recreated verbatim from the pre-076 schema.
CREATE VIEW v_pending AS
    SELECT ecs.*, g.description AS gap_description, g.category AS gap_category,
           g.priority AS gap_priority
    FROM "specifications" ecs
    JOIN gaps g ON g.gap_id = ecs.gap_register_id
    WHERE ecs.state = 'pending';

CREATE VIEW v_divergence AS
    SELECT ecs.*, ca.status AS convergence_status, ca.rationale AS convergence_rationale,
           ca.synthesis_approach AS convergence_synthesis_approach
    FROM "specifications" ecs
    JOIN convergence_assessment ca ON ca.convergence_id = ecs.convergence_id
    WHERE ca.status = 'divergent';

CREATE VIEW v_best_practice AS
    SELECT *,
           CASE
               WHEN regulatory_stratum_only = 1 THEN 'weak'
               ELSE 'anchored'
           END AS strength_band
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0;

CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1;

CREATE VIEW v_source_reach_all AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.verification_status,
    CASE WHEN ecs.specification_id IS NULL THEN 0 ELSE 1 END AS reaches,
    ecs.specification_id,
    ecs.parameter_id,
    t.canonical_en              AS parameter_name,
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code, ecs.medical_code) AS lens_code,
    ecs.state                   AS cell_state,
    (SELECT GROUP_CONCAT(ssl.slug, '; ')
       FROM source_slug_links ssl
      WHERE ssl.ref_id = es.ref_id)  AS admitted_under_slugs
FROM evidence_sources es
LEFT JOIN "specification_source_links" csl ON csl.ref_id = es.ref_id
LEFT JOIN "specifications" ecs ON ecs.specification_id = csl.specification_id
LEFT JOIN base_parameters bp   ON bp.parameter_id = ecs.parameter_id
LEFT JOIN terms t              ON t.term_id       = bp.term_id;

CREATE VIEW v_item_provenance AS
SELECT
    bp.parameter_id,
    t.canonical_en              AS parameter_name,
    t.domain                    AS parameter_domain,
    ecs.specification_id,
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code, ecs.medical_code) AS lens_code,
    ecs.state                   AS cell_state,
    ecs.tier_basis,
    ecs.regulatory_stratum_only,
    csl.role                    AS source_role,
    es.ref_id,
    es.pub_title,
    -- POINTER, NOT COPY (migration 063). Was `es.author_display`, a writer-retired
    -- tombstone reading NULL. The authors have one home, evidence_source_authors, and
    -- v_evidence_authors renders it.
    va.author_display,
    es.pub_year,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.jurisdiction
FROM base_parameters bp
JOIN terms t                            ON t.term_id           = bp.term_id
JOIN "specifications" ecs               ON ecs.parameter_id    = bp.parameter_id
JOIN "specification_source_links" csl   ON csl.specification_id = ecs.specification_id
JOIN evidence_sources es                ON es.ref_id           = csl.ref_id
LEFT JOIN v_evidence_authors va         ON va.ref_id           = es.ref_id;

CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id);

CREATE VIEW v_value_independence AS
    SELECT sve.parameter_id,
           t.canonical_en AS parameter_label,
           COUNT(DISTINCT COALESCE(sve.root_ref_id, sve.root_id)) AS independent_root_count
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_type IN ('measurement_primary', 'participatory_finding',
                            'derived_calculation')
      AND (sve.root_ref_id IS NOT NULL
           OR sve.root_id IN (SELECT root_id FROM external_root_registry))
    GROUP BY sve.parameter_id, t.canonical_en;

PRAGMA user_version = 76;
