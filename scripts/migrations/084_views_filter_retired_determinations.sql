-- 084_views_filter_retired_determinations.sql
--
-- ACTION ITEM 2 OF THE 2026-09-16 RULING: "no row is retired in place until every reader
-- that could surface it filters on status."
--
-- Migration 083 gave `specifications` its retirement columns and made the identity index
-- partial, but deliberately retired nothing, because a retired determination that still
-- renders is worse than the problem retirement solves. The 2026-09-13 corpus clear existed
-- to get untrusted rows OFF the reading surface; retire-in-place without this migration
-- would put them back on it while calling them retired.
--
-- Seven of twenty views read `specifications`. None filtered on any lifecycle predicate.
-- A few filter on `state`, which is a DIFFERENT question -- 083's own comment draws that
-- line: `state` is epistemic (how well the evidence supports the answer), retirement is
-- lifecycle (whether this is still the answer). A `stated` row that has been superseded is
-- still `stated`; it is simply no longer the cell's determination.
--
-- v_source_reach_all IS THE ONE THAT MUST NOT TAKE A WHERE CLAUSE, and the difference is
-- not cosmetic. It LEFT JOINs specifications to compute `reaches` -- 1 if a source reached
-- a determination, 0 if it reached none. A source whose ONLY determination is retired must
-- fall back to reaches=0, not vanish. `WHERE ecs.retired_at IS NULL` keeps unmatched rows
-- (NULL IS NULL), but DROPS that source entirely, silently shrinking the corpus-reach
-- audit exactly where it is most interesting. The predicate belongs in the JOIN.
--
-- v_item_provenance is the view CLAUDE.md rule 4 cites by name -- the one whose 0 rows let
-- migration 063 miss a caller. It is filtered here, never dropped: it spans evidence and
-- specification, and a cross-stage view IS the pointer rule 5 requires.

DROP VIEW IF EXISTS v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *,
           CASE
               WHEN regulatory_stratum_only = 1 THEN 'weak'
               ELSE 'anchored'
           END AS strength_band
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0
      AND retired_at IS NULL;

DROP VIEW IF EXISTS v_code_floor_only;
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1
      AND ecs.retired_at IS NULL;

DROP VIEW IF EXISTS v_divergence;
CREATE VIEW v_divergence AS
    SELECT ecs.*, ca.status AS convergence_status, ca.rationale AS convergence_rationale,
           ca.synthesis_approach AS convergence_synthesis_approach
    FROM "specifications" ecs
    JOIN convergence_assessment ca ON ca.convergence_id = ecs.convergence_id
    WHERE ca.status = 'divergent'
      AND ecs.retired_at IS NULL;

DROP VIEW IF EXISTS v_pending;
CREATE VIEW v_pending AS
    SELECT ecs.*, g.description AS gap_description, g.category AS gap_category,
           g.priority AS gap_priority
    FROM "specifications" ecs
    JOIN gaps g ON g.gap_id = ecs.gap_register_id
    WHERE ecs.state = 'pending'
      AND ecs.retired_at IS NULL;

DROP VIEW IF EXISTS v_determination_provenance;
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
  LEFT JOIN evidence_sources          e ON e.ref_id           = x.ref_id
 WHERE s.retired_at IS NULL;

DROP VIEW IF EXISTS v_item_provenance;
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
LEFT JOIN v_evidence_authors va         ON va.ref_id           = es.ref_id
WHERE ecs.retired_at IS NULL;

DROP VIEW IF EXISTS v_source_reach_all;
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
LEFT JOIN terms t              ON t.term_id       = bp.term_id;

PRAGMA user_version = 84;
