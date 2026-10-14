-- 106_views_filter_retired.sql
-- SCHEMA migration -- every view that LISTS parameters, determinations or sources filters
-- on the lifecycle column its table carries. Plan step 0.3
-- (workplan/2026-10-12-simplification-workplan.md), LED-171: "No row is retired in place
-- until every reader that could surface it filters on status."
--
-- WHY NOW. Migration 104 gave base_parameters its first writers of 'retired' and 'merged'
-- (db.py retire-parameter, merge-parameter), and db.py supersede-source has written
-- evidence_sources.superseded_by_ref_id since 2026-10-01 with its own docstring naming the
-- views as a KNOWN GAP "in its own migration". This is that migration. v_value_independence
-- already filters (104).
--
-- WHAT CHANGES, view by view. Each is recreated verbatim from its stored SQL plus the
-- predicate(s) named; a predicate that sits on the nullable side of a LEFT JOIN is in the
-- ON clause so the row it would hide is not deleted from the listing.
--   v_code_floor_only          bp.status = 'active'
--   v_convergence_sources      es.superseded_by_ref_id IS NULL
--   v_determination_provenance p.status = 'active'; e.superseded_by_ref_id IS NULL
--   v_item_provenance          bp.status = 'active'; es.superseded_by_ref_id IS NULL
--   v_source_reach_all         bp.status = 'active'; es.superseded_by_ref_id IS NULL (WHERE)
--   v_unregistered_roots       p.status = 'active', in both halves
-- The determination views read LIVE specifications only, and neither retire-parameter,
-- merge-parameter nor supersede-source permits a live determination on the row it changes
-- (assess_cell also refuses an inactive parameter), so there the predicate states the
-- invariant and changes no row. The live data agrees: every parameter is active, and the
-- one superseded source appears in none of these views except v_source_reach_all, which
-- loses exactly that row (83 to 82).
--
-- WHAT DOES NOT CHANGE, AND WHY. v_evidence_authors and v_source_admission still show a
-- superseded source. They are lookups keyed on ref_id, and every reader of them
-- (code_currency_audit, citation_mining_completeness [blocking], source_slug_links_duplicates,
-- audit_evidence_metadata, research_protocol_audit) LEFT JOINs them from a query on
-- evidence_sources that does not itself filter supersession. Filtering the lookup would make
-- those audits report the tombstone as authorless or never admitted; the filter belongs in
-- those readers' own queries, a separate change that moves audit populations.
-- build_graph.py probe P-H names the two as judged exemptions.
--
-- NO TABLE IS CHANGED: no AFTER_DATA marker is needed (no backfill, no rebuild).

DROP VIEW v_code_floor_only;
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
                            AND bp.status = 'active'
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1
      AND ecs.retired_at IS NULL;

DROP VIEW v_convergence_sources;
CREATE VIEW v_convergence_sources AS
SELECT cs.convergence_id,
       ca.status            AS convergence_status,
       cs.role,
       cs.ref_id,
       es.tier,
       es.evidence_type,
       es.verification_status
  FROM convergence_sources cs
  JOIN convergence_assessment ca ON ca.convergence_id = cs.convergence_id
  JOIN evidence_sources es       ON es.ref_id         = cs.ref_id
                                AND es.superseded_by_ref_id IS NULL;

DROP VIEW v_determination_provenance;
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
                                       AND p.status             = 'active'
  JOIN terms                          t ON t.term_id          = p.term_id
  LEFT JOIN evidence_sources          e ON e.ref_id           = x.ref_id
                                       AND e.superseded_by_ref_id IS NULL
 WHERE s.retired_at IS NULL;

DROP VIEW v_item_provenance;
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
                                        AND es.superseded_by_ref_id IS NULL
LEFT JOIN v_evidence_authors va         ON va.ref_id           = es.ref_id
WHERE ecs.retired_at IS NULL
  AND bp.status = 'active';

DROP VIEW v_source_reach_all;
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
-- THE PREDICATE IS IN THE JOIN, NOT A WHERE. See the header: a WHERE would delete the
-- source from this audit instead of showing that it now reaches nothing.
LEFT JOIN "specifications" ecs ON ecs.specification_id = csl.specification_id
                              AND ecs.retired_at IS NULL
LEFT JOIN base_parameters bp   ON bp.parameter_id = ecs.parameter_id
                              AND bp.status       = 'active'
LEFT JOIN terms t              ON t.term_id       = bp.term_id
-- A TOMBSTONE IS NOT A SOURCE TO REACH WITH. Unlike the specification predicate above,
-- this one belongs in a WHERE: the superseded row is deleted from the audit on purpose,
-- because `by` carries its work (supersede-source).
WHERE es.superseded_by_ref_id IS NULL;

DROP VIEW v_unregistered_roots;
CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'unregistered' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
                           AND p.status = 'active'
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id)

    UNION ALL

    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'rootless' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
                           AND p.status = 'active'
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NULL
      AND sve.root_ref_id IS NULL
      AND sve.root_type IS NOT NULL
      AND sve.root_type NOT IN ('untraced', 'derived_calculation');

PRAGMA user_version = 106;
