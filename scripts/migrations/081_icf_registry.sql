-- 081_icf_registry.sql
--
-- THE ICF LENS COMES TO HOLD REAL ICF CODES.
--
-- OWNER RULING 2026-09-13, answering the fork opened by the same day's ruling that
-- `AX-` may never denote an ICF code anywhere: "Keep the ICF lens, give it real ICF
-- codes." Four columns literally named `icf_code` -- on `specifications`,
-- `source_value_extractions`, `item_taxonomy_links` and `icf_medical_map` -- carried a
-- real FK into `axes(axis_code)`, whose 17 values all begin `AX-`. So the column called
-- `icf_code` resolved to a coined functional-demand code, in the schema, four times over.
-- This migration re-points all four at a registry of actual ICF codes.
--
-- AND IT COSTS NO DATA MIGRATION, which is worth stating because the estimate put to the
-- owner said otherwise. All four columns hold ZERO rows: the 2026-09-13 circulation clear
-- emptied `specifications` and `source_value_extractions`, `item_taxonomy_links` has been
-- unwritable since its `item_code` FK reached into the emptied `items`, and
-- `icf_medical_map` has never been written. Re-keying an empty column is a schema change
-- and nothing more. The correction is recorded rather than quietly enjoyed.
--
-- WHAT THIS DOES NOT TOUCH. `axes` keeps its 17 rows and so do `population_axis_map` (53)
-- and `access_need_axis_map` (21). The 2026-08-25 RULE refuses folding the demand layer
-- into `access_needs` on a b/d-versus-e argument that this migration leaves intact: the
-- ICF lens now holds b and d codes directly, `access_needs` keeps its e-anchors, and the
-- demand layer is no longer a LENS. What becomes of it -- and whether the ratified
-- `axes` -> `icf_demands` rename should still run, given that it would put `AX-` codes
-- inside a table whose name begins "icf" and so recreate the ruled state -- is an open
-- question recorded in `references/project-standards.md`, not decided here.
--
-- ============================================================================
-- THE REGISTRY
-- ============================================================================
--
-- SEEDED ONLY FROM CODES THIS REPOSITORY ALREADY HOLDS, never from a remembered
-- classification: every row below comes from `access_need_icf`, `population_icf_links`,
-- or an `axes` anchor column, and `notes` records which.
--
-- TITLES ARE THE PART THAT CANNOT BE INVENTED, and this is CLAUDE.md 5(c) applied before
-- the fact rather than after. On 2026-08-19 five sources were stored with invented
-- co-authors and six gates passed them, because each asked whether a field was POPULATED
-- and never whether it was TRUE. An ICF title typed from memory is the same act. So a
-- title is written only where a document in this repository states it -- the
-- functional-deficit-auditor skill's own ICF activity table, and `access_need_icf.note`
-- -- and `title_source` names that document. The rest are NULL, which is the honest
-- state and is logged as a finding below rather than filled in.
--
-- The CHECK is what keeps it honest: a title may not exist without a source.
--
-- RANGES ARE FIRST-CLASS, because the corpus states them. `d310-d329` is one row, not
-- twenty: migration 080 kept ranges verbatim on the reasoning that expanding one would
-- invent the intermediate codes no source named, and the same reasoning governs here.

CREATE TABLE base_icf (
    icf_code      TEXT PRIMARY KEY,
    -- b body function / d activity & participation / e environmental factors /
    -- s body structures. The vocabulary is READ from `access_need_icf.icf_type`'s own
    -- CHECK, which has carried these four since 2026-07-23 -- not a new list.
    component     TEXT NOT NULL CHECK (component IN ('b', 'd', 'e', 's')),
    is_range      INTEGER NOT NULL DEFAULT 0 CHECK (is_range IN (0, 1)),
    title         TEXT,
    -- WHERE THE TITLE CAME FROM. NULL title means nobody here has stated it; a title with
    -- no source would be a title from memory, which is the one thing this column exists
    -- to make impossible.
    title_source  TEXT,
    notes         TEXT,
    created_at    TEXT NOT NULL,
    created_by_session TEXT NOT NULL,
    CHECK (title IS NULL OR title_source IS NOT NULL),
    CHECK (icf_code GLOB '[bdes][0-9][0-9][0-9]*')
);

INSERT INTO base_icf (icf_code, component, is_range, title, title_source,
                      notes, created_at, created_by_session)
VALUES
    ('b114', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b117', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b130', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b140', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b144', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b152', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b156', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b164', 'b', 0, 'higher-level cognitive functions: time management, planning & sequencing (verified WHO/ICF 2026-07-23). Rationale (owner 2026-07-23): brain fog impairs organizing time and retaining the sequence of actions, so tasks run slower as people work to hold onto intent -> the environment must impose no time pressure. No axis carries it.', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b167', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b210', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b230', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b235', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b240', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b280', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b320', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b330', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b435', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b440', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b455', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b525', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b550', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b620', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b710', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b730', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b765', 'b', 0, 'involuntary movement functions: tremor, dystonia, chorea, dyskinesia (excl. b760 voluntary control, b770 gait); verified WHO/ICF 2026-07-23. No axis carries it.', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('b770', 'b', 0, NULL, NULL, 'seeded from axes.icf_b_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d115', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d160', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d166', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d175', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d230', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d240', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d310', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d310–d329', 'd', 1, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d315', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d330', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d330–d349', 'd', 1, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d335', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d350', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d410', 'd', 0, 'Changing basic body position', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d415', 'd', 0, NULL, NULL, 'seeded from axes.icf_d_anchors', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d420', 'd', 0, 'Transferring oneself', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d440', 'd', 0, 'Fine hand use', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d445', 'd', 0, 'Hand and arm use', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d450', 'd', 0, 'Walking', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d455', 'd', 0, 'Moving around', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d460', 'd', 0, 'Moving around in different locations', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d465', 'd', 0, 'Moving around using equipment', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d470', 'd', 0, 'Using transportation', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d510', 'd', 0, 'Washing oneself', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from access_need_icf, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d520', 'd', 0, 'Caring for body parts', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d530', 'd', 0, 'Toileting', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d540', 'd', 0, 'Dressing', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from access_need_icf, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d550', 'd', 0, 'Eating', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d570', 'd', 0, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d620', 'd', 0, 'Acquisition of goods/services', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d630', 'd', 0, 'Preparing meals', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d640', 'd', 0, 'Doing housework', 'skills/functional-deficit-auditor_SKILL.md', 'seeded from axes.icf_d_anchors, population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d710–d729', 'd', 1, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d910', 'd', 0, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d910–d920', 'd', 1, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('d920', 'd', 0, NULL, NULL, 'seeded from population_icf_links', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e115', 'e', 0, 'products for daily living', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e120', 'e', 0, 'mobility products & technology', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e125', 'e', 0, 'products & technology for communication', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e1251', 'e', 0, 'assistive products & technology for communication (sub-code of e125); verified WHO/ICF 2026-07-23', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e150', 'e', 0, 'building design (public)', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e155', 'e', 0, 'building design (private)', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e240', 'e', 0, 'Light', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e250', 'e', 0, 'Sound', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e260', 'e', 0, 'Air quality', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake'),
    ('e340', 'e', 0, 'personal-care providers / SSPs', 'access_need_icf.note', 'seeded from access_need_icf', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake');

-- ============================================================================
-- RE-POINTING THE FOUR LENS COLUMNS, AND FK'ING THE TWO THAT ALREADY HELD REAL CODES
-- ============================================================================
--
-- SQLite cannot ALTER a foreign key, so each table is rebuilt. Every CREATE below is the
-- LIVE DDL with one substitution applied -- `REFERENCES axes(axis_code)` becomes
-- `REFERENCES base_icf(icf_code)`, or a REFERENCES clause is added where there was none
-- -- generated rather than retyped, because a hand-copied table definition is how a
-- rebuild silently drops a constraint nobody notices for a month.
--
-- THE VIEWS COME DOWN FIRST, and migration 076 is why. SQLite reparses the whole schema
-- on ALTER TABLE ... RENAME and refuses if any view is left unresolvable, so a rebuild
-- with a dependent view still standing fails partway. All of them are recreated verbatim
-- at the end, from their own stored SQL.
--
-- AND THE NEW TABLE IS BUILT UNDER A TEMPORARY NAME, NEVER THE OLD ONE RENAMED ASIDE.
-- The first cut of this migration did `ALTER TABLE specifications RENAME TO _081_old_...`
-- and it was WRONG in a way `PRAGMA foreign_key_check` reported as clean: since SQLite
-- 3.25, RENAME rewrites every reference to the renamed table, so four CHILD tables
-- (`specification_source_links`, `specification_extraction_links`,
-- `extraction_relations`, `extraction_population_links`) had their foreign keys silently
-- re-pointed at `_081_old_*` -- which the migration then dropped. The check passed
-- because all four hold zero rows, and a foreign key is resolved at INSERT time, not at
-- migration time. It would have failed on the first row anyone wrote. CLAUDE.md rule 4's
-- "treat a 0-row object as unproven, not clean", live, inside the repair for another
-- ruling. Caught by diffing the rehearsed schema against the canonical one object by
-- object -- which is the step, not the luck.
--
-- The recipe below is migration 076's and has no such hazard: build `_081_new_x`, copy
-- into it, DROP `x`, then rename `_081_new_x` to `x`. Nothing ever references the
-- temporary name, so the rewrite has nothing to corrupt, and every child keeps saying
-- `x` -- which resolves again the moment the rename lands.
--
-- `access_need_icf` (43 rows) and `population_icf_links` (61 rows) already held real ICF
-- codes and pointed at nothing. They get the FK too -- otherwise `base_icf` would be a
-- THIRD home for ICF codes rather than the one home, which is the whole point (rule 5).
-- Every value in both is in the seed above by construction: the seed was built from them.

-- THE AUTOINCREMENT FLOORS ARE CARRIED ACROSS THE REBUILD, and this paragraph exists
-- because the first cut of this migration did not carry them and `identifier_floor_audit`
-- went red on the canonical database.
--
-- `sqlite_sequence` holds one row per AUTOINCREMENT table recording the highest id ever
-- issued, and DROP TABLE takes that row with it. Three of the six tables rebuilt below are
-- AUTOINCREMENT -- `specifications`, `source_value_extractions`, `population_icf_links` --
-- and two of them hold zero rows, so the rebuild silently reset their floors to 0 and the
-- next determination written would have reused `specification_id` 1 and 2. Migration 076
-- exists precisely to stop that: identifiers are never reissued, because a reused id makes
-- the session record, the attestation and the retrieval log all point at a different row.
--
-- The floors are captured before the rebuild and restored as a MAXIMUM afterwards -- never
-- an overwrite, so a floor that somehow rose during the rebuild is not walked back. Every
-- value is READ from the live sequence rather than named here (rule 8): a hard-coded floor
-- is the same defect one layer up.
CREATE TEMP TABLE _081_seq AS SELECT name, seq FROM sqlite_sequence;

DROP VIEW IF EXISTS "v_root_id_conflicts";
DROP VIEW IF EXISTS "v_derived_figure_check";
DROP VIEW IF EXISTS "v_pending";
DROP VIEW IF EXISTS "v_divergence";
DROP VIEW IF EXISTS "v_best_practice";
DROP VIEW IF EXISTS "v_code_floor_only";
DROP VIEW IF EXISTS "v_source_reach_all";
DROP VIEW IF EXISTS "v_item_provenance";
DROP VIEW IF EXISTS "v_unregistered_roots";
DROP VIEW IF EXISTS "v_value_independence";
DROP VIEW IF EXISTS "v_determination_provenance";

-- specifications: re-pointed from axes(axis_code).
CREATE TABLE "_081_new_specifications" (
    -- AUTOINCREMENT (076): never reissue a specification_id. See the header.
    specification_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,
    -- which is why no determination could be written at all.
    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is
    -- retired in favour of these. NULL in a lens means "this determination is not
    -- stated in that lens", which is legitimate; stating several at once is the ideal.
    identity_code                   TEXT REFERENCES populations(population_code),
    icf_code                        TEXT REFERENCES base_icf(icf_code),
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
    updated_by_session              TEXT, value_note TEXT, functional_basis TEXT, derivation_rationale TEXT, cultural_claim_anchor TEXT
    CHECK (cultural_claim_anchor IS NULL OR json_valid(cultural_claim_anchor)), derivation_paths TEXT
    CHECK (derivation_paths IS NULL
        OR (derivation_paths = 'dual')
        OR (derivation_paths = 'function_only' AND derivation_rationale IS NOT NULL)
        OR (derivation_paths = 'population_only'
            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL))),
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);
INSERT INTO "_081_new_specifications" ("specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths") SELECT "specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths" FROM "specifications";
DROP TABLE "specifications";
ALTER TABLE "_081_new_specifications" RENAME TO "specifications";
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
);

-- source_value_extractions: re-pointed from axes(axis_code).
CREATE TABLE "_081_new_source_value_extractions" (
  extraction_id          INTEGER PRIMARY KEY AUTOINCREMENT,

  -- THE HAND-OFF KEY (D-0168; pinned by the blocking judgment_handoff_shape check):
  -- NOT NULL, a real FK at the evidence item, and NO UNIQUE index over it anywhere.
  ref_id                 TEXT NOT NULL REFERENCES evidence_sources(ref_id),

  -- The slug this extraction was MINED UNDER. Not a copy of source_slug_links: that
  -- junction says the source is admitted to the slug; this says the reading happened
  -- there. `evidence_sources` has no slug column, so there is nothing to point at.
  slug                   TEXT NOT NULL REFERENCES slugs(slug),

  -- THE SUBJECT (owner 2026-08-26), now mandatory. Was nullable with `parameter` /
  -- `parameter_canonical` beside it; a NOT NULL free-text parameter NAME sitting next to
  -- a mandatory pointer at the registry that holds that same name is the dual home rule 5
  -- forbids. The name is reached: base_parameters.term_id -> terms.canonical_en.
  --
  -- AND THE VERBATIM PHRASE IS NOT LOST WITH IT. `parameter` was documented (schemas/
  -- source_value_extraction.py) as "the SOURCE's own phrase for what it measures,
  -- verbatim and unjudged (R11/D-0173)". That fact already has a purpose-built home with
  -- a live writer and 33 live rows: `observed_terms.surface_form`, whose own DDL comment
  -- reads "The phrase EXACTLY as the source writes it. Not normalised, not translated,
  -- not mapped. R11 forbids back-translation and this is where that starts" -- keyed
  -- UNIQUE (ref_id, surface_form, language), with `locator` and `context_quote`, written
  -- by `db.py observe-term` and adjudicated by `adjudicate-term` (migration 068, D-0173).
  -- CLAUDE.md §6 orders exactly that split: "harvest concepts at evidence (db.py
  -- observe-term, verbatim and unjudged), adjudicate at judgment." `parameter` was the
  -- duplicate, and an UNREALISED one -- 0 rows, no writer, ever. Clause-level verbatim
  -- survives here in `claim_text` ("exact source phrasing") plus `source_section` and the
  -- 16 `loc_*` columns.
  --
  -- KNOWN RESIDUAL, stated rather than papered over: an extraction cannot say WHICH of
  -- its source's observations it was read from. Closing that is an `observation_id`
  -- pointer, and it is NOT added here because nothing would read it -- "an unread field,
  -- an uncalled script and an unregistered check are the same defect" (CLAUDE.md §8). Add
  -- it in the change that gives it a reader.
  parameter_id           INTEGER NOT NULL REFERENCES base_parameters(parameter_id),

  -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). Real typed FKs, one per
  -- lens, nothing polymorphic. They replace `population_code` (retired by that ruling's
  -- own ACTION) and `population_label`, the free-text companion that had no registry at
  -- all -- retiring the typed column while keeping the untyped one beside it would keep
  -- the exact defect the ruling was issued against.
  --
  -- `base_taxonomy_medical` holds 0 rows today, so a NON-NULL medical_code is
  -- unwritable until it is seeded. That is the CLAUDE.md §4 trap, and it is harmless in
  -- this shape precisely because the column is nullable and the CHECK is "at least one":
  -- the table stays writable through any of the other three. `specifications` carries the
  -- identical arrangement from 071.
  identity_code          TEXT REFERENCES populations(population_code),
  icf_code               TEXT REFERENCES base_icf(icf_code),
  needs_code             TEXT REFERENCES access_needs(need_code),
  medical_code           TEXT REFERENCES base_taxonomy_medical(medical_code),

  jurisdiction           TEXT,
  setting                TEXT,

  claim_type             TEXT NOT NULL
                           CHECK (claim_type IN ('numerical','range','qualitative','framework','absent')),
  claimed_value          TEXT,
  claimed_unit           TEXT,
  claim_text             TEXT,
  source_section         TEXT,

  -- Value genealogy / independence substrate (DR-2026-07-13 H1), carried across
  -- unchanged. v_value_independence counts distinct roots over these.
  root_id                TEXT,
  root_type              TEXT
                           CHECK (root_type IN (
                             'measurement_primary', 'participatory_finding',
                             'committee_assertion', 'derived_calculation', 'untraced')),
  root_ref_id            TEXT REFERENCES evidence_sources(ref_id),
  echo_of                TEXT,
  measurement_paradigm   TEXT
                           CHECK (measurement_paradigm IN (
                             'swept_path_dynamic', 'static_turning_circle', 'static_clearance',
                             'anthropometric_percentile', 'instrumented_physical_measurement',
                             'route_metric', 'field_observation', 'participatory_spatial',
                             'stated_unmeasured')),
  device_class           TEXT
                           CHECK (device_class IN (
                             'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter',
                             'bariatric_manual', 'bariatric_power', 'walker_rollator',
                             'mixed', 'not_device_scoped')),
  root_population_note   TEXT,
  root_classification_basis TEXT,
  contested              INTEGER NOT NULL DEFAULT 0
                           CHECK (contested IN (0, 1)),
  file_anchor            TEXT,

  -- Pinpoint locator hierarchy (migration 053), carried across unchanged. These are the
  -- clause-level address that makes D-0168's 1:N fan-out legible: NBC 3.8's many clauses
  -- are many rows, and these columns are what tells them apart.
  locator_scheme         TEXT,
  loc_division           TEXT,
  loc_part               TEXT,
  loc_section            TEXT,
  loc_subsection         TEXT,
  loc_paragraph          TEXT,
  loc_clause             TEXT,
  loc_subclause          TEXT,
  loc_division_end       TEXT,
  loc_part_end           TEXT,
  loc_section_end        TEXT,
  loc_subsection_end     TEXT,
  loc_paragraph_end      TEXT,
  loc_clause_end         TEXT,
  loc_subclause_end      TEXT,
  loc_note               TEXT,

  extraction_method      TEXT NOT NULL
                           CHECK (extraction_method IN ('skim','full-read','re-read','auto-mined')),
  extraction_status      TEXT NOT NULL DEFAULT 'preliminary'
                           CHECK (extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')),
  promoted_to_rdc_id     TEXT REFERENCES reasoning_doc_citations(citation_id),
  notes                  TEXT,

  created_at             TEXT NOT NULL,
  created_by_session     TEXT,
  updated_at             TEXT NOT NULL,
  updated_by_session     TEXT, figure_role TEXT
  CHECK (figure_role IS NULL OR figure_role IN ('claim', 'finding', 'condition', 'derived')), comparator TEXT
  CHECK (comparator IS NULL OR comparator IN ('=', '<', '<=', '>', '>=', 'between', 'approx')),

  -- Carried across verbatim: if claim_type='absent', claimed_value must be NULL; if it
  -- is anything else, claimed_value must be present. `db.py add-extraction` refuses both
  -- violations in words BEFORE the INSERT, so an operator gets a sentence rather than
  -- "CHECK constraint failed".
  CHECK (
    (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)
  ),

  -- D-0182, mechanised. Absence in a lens is fine; absence in ALL of them is not.
  -- Identical in form to specifications' and item_taxonomy_links' own CHECK.
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);
INSERT INTO "_081_new_source_value_extractions" ("extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator") SELECT "extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator" FROM "source_value_extractions";
DROP TABLE "source_value_extractions";
ALTER TABLE "_081_new_source_value_extractions" RENAME TO "source_value_extractions";
CREATE INDEX idx_sve_ref    ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status ON source_value_extractions(extraction_status);
CREATE INDEX ix_sve_locator ON source_value_extractions(loc_section, loc_clause);
CREATE INDEX idx_sve_slug_param ON source_value_extractions(slug, parameter_id);
CREATE INDEX idx_sve_param_ref ON source_value_extractions(parameter_id, ref_id);

-- item_taxonomy_links: re-pointed from axes(axis_code).
CREATE TABLE "_081_new_item_taxonomy_links" (
  item_code           TEXT NOT NULL,

  -- The four lenses (D-0170). NULL means "this fact is not stated in that lens",
  -- which is legitimate; a row stating several lenses at once is the ideal.
  identity_code       TEXT REFERENCES populations(population_code),
  icf_code            TEXT REFERENCES base_icf(icf_code),
  needs_code          TEXT REFERENCES access_needs(need_code),
  medical_code        TEXT REFERENCES base_taxonomy_medical(medical_code),

  subtype             TEXT NOT NULL DEFAULT '',  -- '' = no subtype, so it indexes

  -- From item_population_links. NULL = not adjudicated (see header).
  applicability       TEXT CHECK(applicability IN (
                        'applies', 'applies_strictly', 'applies_loosely',
                        'context_dependent', 'does_not_apply'
                      )),
  rationale_ref       TEXT REFERENCES decisions(decision_id),

  -- From item_axis_links. Kept under their own names; not merged into applicability.
  mechanism_note      TEXT,
  strength_band       TEXT CHECK(strength_band IN ('full','partial','weak')),
  -- CHECK text preserved VERBATIM from item_axis_links, `OR ... IS NULL` tail and
  -- all. A CHECK passes on NULL anyway, so the tail is redundant -- but
  -- rename_insurance.py compares CHECK TEXT, and paraphrasing a constraint it is
  -- meant to prove survived is how an instrument gets taught to accept drift.
  use_mode            TEXT CHECK(use_mode IN ('independent','assisted','collective')
                                 OR use_mode IS NULL),
  source              TEXT,

  created_at          TEXT,
  created_by_session  TEXT,

  FOREIGN KEY (item_code) REFERENCES items(item_code) ON DELETE CASCADE,

  -- The owner's rule, mechanised: absence in a lens is fine, absence in ALL of them
  -- is not. COALESCE is the whole constraint — "at least one", never "exactly one".
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);
INSERT INTO "_081_new_item_taxonomy_links" ("item_code", "identity_code", "icf_code", "needs_code", "medical_code", "subtype", "applicability", "rationale_ref", "mechanism_note", "strength_band", "use_mode", "source", "created_at", "created_by_session") SELECT "item_code", "identity_code", "icf_code", "needs_code", "medical_code", "subtype", "applicability", "rationale_ref", "mechanism_note", "strength_band", "use_mode", "source", "created_at", "created_by_session" FROM "item_taxonomy_links";
DROP TABLE "item_taxonomy_links";
ALTER TABLE "_081_new_item_taxonomy_links" RENAME TO "item_taxonomy_links";
CREATE UNIQUE INDEX idx_itl_row_identity ON item_taxonomy_links(
  item_code, subtype,
  COALESCE(identity_code,''), COALESCE(icf_code,''),
  COALESCE(needs_code,''),    COALESCE(medical_code,'')
);
CREATE INDEX idx_itl_item     ON item_taxonomy_links(item_code);
CREATE INDEX idx_itl_identity_lens ON item_taxonomy_links(identity_code);
CREATE INDEX idx_itl_icf_lens      ON item_taxonomy_links(icf_code);
CREATE INDEX idx_itl_needs_lens    ON item_taxonomy_links(needs_code);
CREATE INDEX idx_itl_medical_lens  ON item_taxonomy_links(medical_code);

-- icf_medical_map: re-pointed from axes(axis_code).
CREATE TABLE "_081_new_icf_medical_map" (
  icf_code           TEXT NOT NULL REFERENCES base_icf(icf_code),
  medical_code       TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  role               TEXT NOT NULL CHECK (role IN ('PRIMARY','SECONDARY','SITUATIONAL')),
  mapping_confidence TEXT NOT NULL
                       CHECK (mapping_confidence IN ('high_predictive','moderate','low','minimal')),
  note               TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (icf_code, medical_code)
);
INSERT INTO "_081_new_icf_medical_map" ("icf_code", "medical_code", "role", "mapping_confidence", "note", "created_at", "created_by_session") SELECT "icf_code", "medical_code", "role", "mapping_confidence", "note", "created_at", "created_by_session" FROM "icf_medical_map";
DROP TABLE "icf_medical_map";
ALTER TABLE "_081_new_icf_medical_map" RENAME TO "icf_medical_map";

-- access_need_icf: FK added where there was none.
CREATE TABLE "_081_new_access_need_icf" (
  need_code   TEXT NOT NULL REFERENCES access_needs(need_code),
  icf_code    TEXT NOT NULL REFERENCES base_icf(icf_code),                       -- 'e250','b765','d510' …
  icf_type    TEXT NOT NULL CHECK (icf_type IN ('b','d','e','s')),
  confidence  TEXT NOT NULL CHECK (confidence IN ('confirmed','proposed')),
  note        TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (need_code, icf_code)
);
INSERT INTO "_081_new_access_need_icf" ("need_code", "icf_code", "icf_type", "confidence", "note", "created_at", "created_by_session") SELECT "need_code", "icf_code", "icf_type", "confidence", "note", "created_at", "created_by_session" FROM "access_need_icf";
DROP TABLE "access_need_icf";
ALTER TABLE "_081_new_access_need_icf" RENAME TO "access_need_icf";

-- population_icf_links: FK added where there was none.
CREATE TABLE "_081_new_population_icf_links" (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    population_code     TEXT NOT NULL REFERENCES populations(population_code),
    icf_code            TEXT NOT NULL REFERENCES base_icf(icf_code),
    mechanism           TEXT NOT NULL,
    mapping_confidence  TEXT NOT NULL
                        CHECK (mapping_confidence IN ('high_predictive',
                                                      'moderate_contextual',
                                                      'low_indicative')),
    -- WHERE THIS ROW CAME FROM. A mapping with no provenance is the skill prose again,
    -- in a table. 'fda-skill-2026-09-13' is the promotion of the audited markdown; a
    -- later row derived from a study names its ref_id.
    provenance          TEXT NOT NULL,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    -- One row per (population, code, mechanism): the same population may reach one ICF
    -- code by two different mechanisms (SCI is "biomechanical + autonomic"), and both are
    -- real. Collapsing them would lose the distinction the mechanism column exists for.
    UNIQUE (population_code, icf_code, mechanism)
);
INSERT INTO "_081_new_population_icf_links" ("link_id", "population_code", "icf_code", "mechanism", "mapping_confidence", "provenance", "notes", "created_at", "created_by_session") SELECT "link_id", "population_code", "icf_code", "mechanism", "mapping_confidence", "provenance", "notes", "created_at", "created_by_session" FROM "population_icf_links";
DROP TABLE "population_icf_links";
ALTER TABLE "_081_new_population_icf_links" RENAME TO "population_icf_links";
CREATE INDEX idx_picf_icf ON population_icf_links(icf_code);

-- The floors, restored. INSERT covers a sequence row the rebuild dropped entirely;
-- UPDATE ... MAX covers one that survived at a lower value.
INSERT INTO sqlite_sequence (name, seq)
  SELECT s.name, s.seq FROM _081_seq s
   WHERE s.name NOT IN (SELECT name FROM sqlite_sequence);
UPDATE sqlite_sequence SET seq = MAX(seq,
        (SELECT s.seq FROM _081_seq s WHERE s.name = sqlite_sequence.name))
  WHERE name IN (SELECT name FROM _081_seq);
DROP TABLE _081_seq;

-- The views, recreated verbatim from their own stored SQL.
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
CREATE VIEW v_derived_figure_check AS
SELECT
    d.extraction_id                                              AS derived_id,
    CAST(d.claimed_value AS REAL)                                 AS stored,
    CAST(b.claimed_value AS REAL)                                 AS base_value,
    CAST(e.claimed_value AS REAL)                                 AS delta_value,
    CAST(b.claimed_value AS REAL) + CAST(e.claimed_value AS REAL) AS recomputed
FROM source_value_extractions d
JOIN extraction_relations rb
  ON rb.from_extraction_id = d.extraction_id
 AND rb.relation = 'derived_from'
 AND rb.input_role = 'base'
JOIN source_value_extractions b ON b.extraction_id = rb.to_extraction_id
JOIN extraction_relations rd
  ON rd.from_extraction_id = d.extraction_id
 AND rd.relation = 'derived_from'
 AND rd.input_role = 'delta'
JOIN source_value_extractions e ON e.extraction_id = rd.to_extraction_id
WHERE d.figure_role = 'derived'
  AND d.claimed_value GLOB '*[0-9]*' AND d.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND b.claimed_value GLOB '*[0-9]*' AND b.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND e.claimed_value GLOB '*[0-9]*' AND e.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND d.claimed_unit = b.claimed_unit
  AND d.claimed_unit = e.claimed_unit;
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
CREATE VIEW v_determination_provenance AS
SELECT s.specification_id,
       s.parameter_id,
       t.canonical_en                AS parameter_name,
       s.state,
       COALESCE(s.identity_code, s.icf_code, s.needs_code, s.medical_code) AS lens,
       l.role,
       l.exclusion_reason,
       x.extraction_id,
       x.figure_role,
       x.comparator,
       x.claimed_value,
       x.claimed_unit,
       x.claim_text,
       x.ref_id,
       e.tier,
       e.evidence_type,
       e.verification_status
  FROM specifications s
  JOIN specification_extraction_links l ON l.specification_id = s.specification_id
  JOIN source_value_extractions       x ON x.extraction_id    = l.extraction_id
  JOIN base_parameters                p ON p.parameter_id     = s.parameter_id
  JOIN terms                          t ON t.term_id          = p.term_id
  LEFT JOIN evidence_sources          e ON e.ref_id           = x.ref_id;

-- The 43 codes nobody here has named, logged rather than invented.
INSERT INTO gaps (gap_id, category, priority, status, skill, section, description,
                  created_at, created_by_session, updated_at, updated_by_session,
                  mining_addressability)
VALUES ('GAP-ICF-TITLES', 'ST', 'P2', 'OPEN', NULL, 'base_icf.title',
        'base_icf holds 72 ICF codes of which 29 carry a title stated by a document in this repository (the functional-deficit-auditor skill''s ICF activity table, and access_need_icf.note). The other 43 have title NULL because nothing here states them, and CLAUDE.md 5(c) forbids supplying them from memory -- that is the exact act that put invented co-authors on five sources through six green gates on 2026-08-19. Untitled: b114, b117, b130, b140, b144, b152, b156, b167, b210, b230, b235, b240, b280, b320, b330, b435, b440, b455, b525, b550, b620, b710, b730, b770, d115, d160, d166, d175, d230, d240, d310, d310–d329, d315, d330, d330–d349, d335, d350, d415, d570, d710–d729, d910, d910–d920, d920. CLAUDE.md section 6 requires working from ICF codes AND NAMES, so this is a real gap on the lens the owner ruled to keep. Remedy: retrieve the titles from the WHO ICF browser, persist the payload under retrieval-log/, and write them with db.py set-icf-title --title-source naming that payload -- the same bytes-not-memory path add-medical --icd11-payload uses for ICD-11.', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake', '2026-09-13 07:00', 'session_2026-09-13-derivation-handshake', 'NOT-ADDRESSABLE');

PRAGMA user_version = 81;
