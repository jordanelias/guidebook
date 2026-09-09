-- 072_repair_the_views_071_broke.sql
-- SCHEMA migration — the sweep migration 071 owed and did not pay.
--
-- Migration 071 dropped specifications.item_code and .population_code. Three views still
-- selected them and have been erroring ever since:
--
--   v_code_floor_only   no such column: ecs.item_code
--   v_source_reach_all  no such column: ecs.item_code
--   v_item_provenance   no such column: ecs.population_code
--
-- WHY THE CHECKS DID NOT CATCH IT, which is the part worth recording. Every one of these
-- views resolves over tables holding 0 rows, and no registered check SELECTs from them.
-- So `run_checks.py --all` was PASS, 50 green, 0 blocking, over three broken objects.
-- CLAUDE.md rule 4 states the rule this violates in as many words -- "treat a 0-row
-- object as unproven, not clean" -- and names v_item_provenance BY NAME as the view
-- migration 063 missed and 064 existed to repair. 071 repeated 063's mistake on the same
-- view. The instrument that found it is not a check: it is a probe that SELECTs from
-- every view in sqlite_master and reports the ones that raise.
--
-- THESE ARE CROSS-STAGE VIEWS, so repair is not optional and deletion is not on the
-- table. CLAUDE.md §3: a view joining two stages on the shared reference id is what
-- "point" MEANS in SQL, which makes it the most protected object in the schema --
-- deleting one forces the next reader back to copying, the defect rule 5 exists to stop.
--
-- NAMES ARE KEPT. `v_item_provenance` now walks parameters, not items, so its name is
-- inaccurate. Renaming it is a separate act with its own caller sweep (schema_reference_
-- audit, pipeline-contract.yaml, context-map.yaml all name it), and doing it inside a
-- repair would mix a fix with a rename -- which is how 063 went wrong. Recorded, not done.

-- ---------------------------------------------------------------------------
DROP VIEW IF EXISTS v_code_floor_only;
-- The jurisdictional_values join is GONE, not re-keyed: it joined on item_code, and
-- jurisdictional_values is still keyed on the deleted item layer (its own item_code is
-- NOT NULL into an emptied `items`, so the table is unwritable and holds 0 rows). There
-- is no parameter->jurisdiction edge to join through yet. Enriching a code-floor cell
-- with its standard is real and owed; inventing a join that cannot resolve is not.
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1;

-- ---------------------------------------------------------------------------
DROP VIEW IF EXISTS v_source_reach_all;
-- Evidence -> specification reach. Still crosses stages on the shared reference id;
-- the cell's identity is now parameter x lens rather than item x population.
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

-- ---------------------------------------------------------------------------
DROP VIEW IF EXISTS v_item_provenance;
-- Walks base_parameters where it walked items. The author pointer from migration 063 is
-- preserved verbatim -- that repair is still live and must not be undone by this one.
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

PRAGMA user_version = 72;
