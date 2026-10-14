-- 106_views_filter_retired.sql
-- SCHEMA migration -- the views that read base_parameters filter its lifecycle column, and
-- two source views filter supersession where that is safe. Plan step 0.3
-- (workplan/2026-10-12-simplification-workplan.md), LED-171: "No row is retired in place
-- until every reader that could surface it filters on status."
--
-- WHAT THIS DOES AND DOES NOT CLAIM. LED-171 speaks of EVERY reader. This migration changes
-- VIEWS, and only the ones named below. Readers that are not views (audit_evidence_metadata,
-- metadata_integrity_audit, research_batch_dod R2/R4/R13, db.py get_unmined,
-- validate_parameters, the render and scheduled-writer scripts that 1.1 and 1.5 delete) still
-- surface a retired parameter or a superseded source; so do four source views left alone
-- below. LED-171 is therefore NOT fully met by this change. The probe P-H
-- (workplan/pipeline-state-graph/build_graph.py) reads view SQL only and reports the four.
--
-- WHY NOW. Migration 104 gave base_parameters its first writers of 'retired' and 'merged'
-- (db.py retire-parameter, merge-parameter). Both refuse while a LIVE determination or an
-- open gate stands on the parameter (checked on a scratch copy), and assess_cell refuses to
-- determine an inactive one. v_value_independence already filters (104).
--
-- WHAT CHANGES. Each view is recreated verbatim from its stored SQL plus the predicate(s)
-- named; a predicate on the nullable side of a LEFT JOIN is in the ON clause so it deletes
-- no row from the listing.
--   v_code_floor_only          bp.status = 'active'
--   v_determination_provenance p.status = 'active'
--   v_item_provenance          bp.status = 'active'; es.superseded_by_ref_id IS NULL
--   v_source_reach_all         bp.status = 'active'; es.superseded_by_ref_id IS NULL (WHERE)
--   v_unregistered_roots       p.status = 'active', in both halves
-- Where the predicate removes a parameter from a view of LIVE specifications it states an
-- invariant the verbs already enforce and changes no row. The source predicate in
-- v_item_provenance is the same kind: supersede-source refuses while a live determination
-- rests on the source through specification_source_links (dbcore.determinations_resting_on).
-- v_source_reach_all lists SOURCES, so a tombstone is the wrong subject and is dropped (its
-- rows are junction rows: 83 to 82 rows, 53 to 52 sources). v_unregistered_roots lists
-- extraction defects and is filtered by parameter status: a retired parameter's extractions
-- stay as history (db.py retire-parameter), so their root defects stop being reported. That
-- is a judgment, not a derivation; recreating the view without the predicate reverses it.
--
-- WHAT DOES NOT CHANGE, AND WHY.
--   v_convergence_sources, v_evidence_authors, v_source_admission, and the source side of
--   v_determination_provenance still show a superseded source.
--   * v_determination_provenance: supersede-source does NOT refuse a source linked to a live
--     determination only through specification_extraction_links (determinations_resting_on
--     consults two junctions, not that one; reproduced on a scratch copy). Filtering the
--     LEFT JOIN there would blank the tier and evidence type of a live determination's
--     source while leaving its ref_id: worse than showing the tombstone.
--   * v_convergence_sources: lists the participants of a RECORDED assessment; supersede-source
--     is allowed when no live determination rests on it, and hiding the participant then
--     contradicts convergence_sources (15 recorded, 14 shown).
--   * v_evidence_authors, v_source_admission: ref_id lookups that readers LEFT JOIN from
--     their own queries on evidence_sources, which do not filter supersession; on the one
--     tombstone today (REF-01019) filtering the lookups changes no audit outcome, but the
--     blocking test_db_integrity C03 reads v_evidence_authors and would go red on a
--     COMPLETE-quality tombstone. The filter belongs in those readers.
--   The fix for the first is in supersede-source's refusal, the rest is a decision about
--   what a recorded fact shows after supersession; both are outside this step (GAP-062).
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
