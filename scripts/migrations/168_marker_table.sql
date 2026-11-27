-- 168_marker_table.sql
-- SCHEMA migration -- one rebuild of specifications, for the marker table (T-117; owner answers 2026-11-14,
-- fourteenth set "od57 yes" and fifteenth set "triangle for all", OD-64; "Owner answer 2026-11-14 (last) -- a cell
-- resting on tier 4 only takes the half circle").
--
--   marker CHECK  ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○')
--             ->  ('●','◐','○','⚠') AND (regulatory_stratum_only = 0 OR marker <> '●')
--   The warning marker (U+26A0 alone, never with U+FE0F) stands in place of a circle; a regulation-only row may now
--   show its tier's circle (◐ for T4) but never the full circle. The CHECK only widens: every row valid before is valid
--   after. The live-row CHECK (a live stated or provisional row has a marker) and the lens CHECK are unchanged.
--
-- SQLite cannot alter a column CHECK (migration 116 added this one with ADD COLUMN), so the table is rebuilt by
-- migration 114's recipe, GENERATED from the live DDL with the one substitution above, never retyped: build under a
-- temporary name, copy by column name, DROP the old, RENAME the new (so the inbound keys of specification_source_links,
-- specification_extraction_links and the table's own superseded_by_specification_id keep naming specifications; derived
-- with PRAGMA foreign_key_list over every table), recreate the indexes and the trigger, then the views from their own
-- stored SQL, verbatim. The views are the transitive closure over sqlite_master of views whose SQL names the table
-- (word-boundary match, iterated to a fixpoint), dropped first because SQLite refuses a rename while a view is
-- unresolvable. The table is AUTOINCREMENT: its sqlite_sequence floor is captured first and restored as a maximum.
--
-- NO AFTER_DATA LINE. The last committed data migration that writes specifications
-- (for f in scripts/migrations/data_*.sql; do grep -qiE '(INSERT INTO|UPDATE|DELETE FROM) +"?specifications\b' $f && basename $f; done | sort | tail -1)
-- precedes the last existing cutoff (grep -h '^-- AFTER_DATA:' scripts/migrations/*.sql | sort -u | tail -1), which
-- migrations from 146 on already replay after; so its rows exist when this rebuild runs and are copied. No column is
-- renamed or dropped, and the CHECK only widens, so no later data migration can fail against it.

CREATE TEMP TABLE _168_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'specifications';

DROP VIEW "v_determination_provenance";
DROP VIEW "v_gap_subject";
DROP VIEW "v_best_practice";
DROP VIEW "v_source_reach_all";
DROP VIEW "v_item_provenance";
DROP VIEW "v_pending";
DROP VIEW "v_divergence";

CREATE TABLE "_168_new_specifications" (
    -- AUTOINCREMENT (076): never reissue a specification_id. See the header.
    specification_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,
    -- which is why no determination could be written at all.
    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- THE THREE LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is
    -- retired in favour of these. NULL in a lens means "this determination is not
    -- stated in that lens", which is legitimate; stating several at once is the ideal.
    identity_code                   TEXT REFERENCES "base_taxonomy_identity"(identity_code),
    icf_code                        TEXT REFERENCES base_icf(icf_code),
    needs_code                      TEXT REFERENCES access_needs(need_code),
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
            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL))), retired_at TEXT, retired_by_session TEXT, retirement_reason TEXT, superseded_by_specification_id INTEGER
    REFERENCES specifications(specification_id), rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0
  CHECK (rests_on_proxy_inference IN (0, 1)), value_notations TEXT, marker TEXT
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○', '⚠')
                            AND (regulatory_stratum_only = 0 OR marker <> '●')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL)),
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code) IS NOT NULL)
);

INSERT INTO "_168_new_specifications" ("specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths", "retired_at", "retired_by_session", "retirement_reason", "superseded_by_specification_id", "rests_on_proxy_inference", "value_notations", "marker")
  SELECT "specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths", "retired_at", "retired_by_session", "retirement_reason", "superseded_by_specification_id", "rests_on_proxy_inference", "value_notations", "marker" FROM "specifications";

DROP TABLE "specifications";
ALTER TABLE "_168_new_specifications" RENAME TO "specifications";

CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, '')
) WHERE retired_at IS NULL;
CREATE INDEX idx_spec_retired ON specifications(retired_at);
CREATE TRIGGER trg_spec_retire_needs_reason
BEFORE UPDATE OF retired_at ON specifications
WHEN NEW.retired_at IS NOT NULL
 AND (NEW.retirement_reason IS NULL OR TRIM(NEW.retirement_reason) = '')
BEGIN
    SELECT RAISE(ABORT, 'a retired specification must carry a retirement_reason -- retiring a determination without recording why discards the judgement it cost');
END;

CREATE VIEW v_divergence AS
    SELECT ecs.*, ca.status AS convergence_status, ca.rationale AS convergence_rationale,
           ca.synthesis_approach AS convergence_synthesis_approach
    FROM "specifications" ecs
    JOIN convergence_assessment ca ON ca.convergence_id = ecs.convergence_id
    WHERE ca.status = 'divergent'
      AND ecs.retired_at IS NULL;
CREATE VIEW v_pending AS
    SELECT ecs.*, g.description AS gap_description, g.category AS gap_category,
           g.priority AS gap_priority
    FROM "specifications" ecs
    JOIN gaps g ON g.gap_id = ecs.gap_register_id
    WHERE ecs.state = 'pending'
      AND ecs.retired_at IS NULL;
CREATE VIEW v_item_provenance AS
SELECT
    bp.parameter_id,
    t.canonical_en              AS parameter_name,
    t.domain                    AS parameter_domain,
    ecs.specification_id,
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code) AS lens_code,
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
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code) AS lens_code,
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
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND retired_at IS NULL;
CREATE VIEW v_gap_subject AS
    SELECT g.gap_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code,
           g.jurisdiction, g.language, 'gaps' AS subject_home, NULL AS specification_id
      FROM gaps g
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code,
                    g.jurisdiction, g.language) IS NOT NULL
    UNION ALL
    SELECT g.gap_id, s.parameter_id, s.identity_code, s.icf_code, s.needs_code,
           NULL, NULL, 'specifications', s.specification_id
      FROM gaps g
      JOIN specifications s
        ON s.specification_id = (SELECT MAX(x.specification_id) FROM specifications x
                                  WHERE x.gap_register_id = g.gap_id)
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code,
                    g.jurisdiction, g.language) IS NULL
    UNION ALL
    SELECT g.gap_id, NULL, NULL, NULL, NULL, NULL, NULL, 'none', NULL
      FROM gaps g
     WHERE COALESCE(g.parameter_id, g.identity_code, g.icf_code, g.needs_code,
                    g.jurisdiction, g.language) IS NULL
       AND NOT EXISTS (SELECT 1 FROM specifications x WHERE x.gap_register_id = g.gap_id);
CREATE VIEW v_determination_provenance AS
SELECT s.specification_id,
       s.parameter_id,
       t.canonical_en                AS parameter_name,
       s.state,
       COALESCE(s.identity_code, s.icf_code, s.needs_code) AS lens,
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

INSERT INTO sqlite_sequence (name, seq)
  SELECT s.name, s.seq FROM _168_seq s
   WHERE s.name NOT IN (SELECT name FROM sqlite_sequence);
UPDATE sqlite_sequence SET seq = MAX(seq,
        (SELECT s.seq FROM _168_seq s WHERE s.name = sqlite_sequence.name))
  WHERE name IN (SELECT name FROM _168_seq);
DROP TABLE _168_seq;

PRAGMA user_version = 168;
