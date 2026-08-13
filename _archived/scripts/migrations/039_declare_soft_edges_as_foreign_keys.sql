-- 039_declare_soft_edges_as_foreign_keys.sql
-- SCHEMA migration — turn 12 undeclared id columns into declared foreign keys.
--
-- Rationale (workplan/2026-08-02-architecture-decision-and-execution-plan.md W5.1):
-- a declared foreign key is intent and enforcement in one object, checked by
-- SQLite on every write, at zero maintenance cost. These 12 columns already
-- behaved as foreign keys; nothing declared them, so nothing enforced them.
--
-- Every column below was verified to have ZERO orphans before this migration
-- was written. No backfill is required and no row is modified.
--
-- DDL provenance: each CREATE TABLE below was DERIVED from sqlite_master at
-- generation time, not hand-transcribed. The only edit is the injected
-- REFERENCES clause. This is deliberate — hand-copying an 88-column
-- definition is how a rebuild silently changes a type, default, or CHECK.
--
-- DEFERRED, and why: evidence_sources.superseded_by_ref_id (44 non-null
-- values, 0 orphans) is NOT included. evidence_sources has 88 columns and 9
-- inbound foreign keys; rebuilding the project's hub table to protect 44
-- values is a bad trade. It is covered instead by a registry check asserting
-- the column resolves. Revisit if that table is ever rebuilt for another
-- reason.
--
-- Data migrations run with PRAGMA foreign_keys=OFF (scripts/migrate_db.py:164),
-- so these declarations cannot break a rebuild on intermediate states. They
-- bind live writes (scripts/db.py sets foreign_keys=ON) and are verified in
-- bulk by PRAGMA foreign_key_check.
--
-- Forward-only; user_version -> 39.

PRAGMA foreign_keys = OFF;

-- Dependent views are dropped and recreated verbatim below.
DROP VIEW IF EXISTS v_coverage_priority;
DROP VIEW IF EXISTS v_pmp_latest_walk;
DROP VIEW IF EXISTS v_root_id_conflicts;
DROP VIEW IF EXISTS v_unregistered_roots;
DROP VIEW IF EXISTS v_value_independence;

-- ---- evidence_source_authors: +ref_id (1478 rows, 3 index(es), 0 view(s)) ----
CREATE TABLE _new_evidence_source_authors (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
        position            INTEGER NOT NULL,
        last_name           TEXT,
        first_name          TEXT,
        suffix              TEXT,
        orcid               TEXT,
        is_corporate        INTEGER NOT NULL DEFAULT 0,
        corporate_name      TEXT,
        corporate_name_en   TEXT,
        role                TEXT NOT NULL DEFAULT 'author',
        created_at          TEXT,
        created_by_session  TEXT,
        UNIQUE(ref_id, position, role)
    );
INSERT INTO _new_evidence_source_authors ("id", "ref_id", "position", "last_name", "first_name", "suffix", "orcid", "is_corporate", "corporate_name", "corporate_name_en", "role", "created_at", "created_by_session") SELECT "id", "ref_id", "position", "last_name", "first_name", "suffix", "orcid", "is_corporate", "corporate_name", "corporate_name_en", "role", "created_at", "created_by_session" FROM evidence_source_authors;
DROP TABLE evidence_source_authors;
ALTER TABLE _new_evidence_source_authors RENAME TO evidence_source_authors;
CREATE INDEX idx_esa_ref_id ON evidence_source_authors(ref_id);
CREATE INDEX idx_esa_last   ON evidence_source_authors(last_name);
CREATE INDEX idx_esa_corp   ON evidence_source_authors(corporate_name);

-- ---- source_value_extractions: +slug (8 rows, 3 index(es), 3 view(s)) ----
CREATE TABLE _new_source_value_extractions (
  extraction_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_id                 TEXT NOT NULL,
  slug                   TEXT NOT NULL REFERENCES slugs(slug),
  parameter              TEXT NOT NULL,
  parameter_canonical    TEXT,
  population_code        TEXT,
  population_label       TEXT,
  jurisdiction           TEXT,
  claim_type             TEXT NOT NULL
                           CHECK (claim_type IN ('numerical','range','qualitative','framework','absent')),
  claimed_value          TEXT,
  claimed_unit           TEXT,
  claim_text             TEXT,
  source_section         TEXT,
  extraction_method      TEXT NOT NULL
                           CHECK (extraction_method IN ('skim','full-read','re-read','auto-mined')),
  extraction_status      TEXT NOT NULL DEFAULT 'preliminary'
                           CHECK (extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')),
  promoted_to_rdc_id     TEXT,
  notes                  TEXT,
  created_at             TEXT NOT NULL,
  created_by_session     TEXT,
  updated_at             TEXT NOT NULL,
  updated_by_session     TEXT, setting TEXT, root_id TEXT, root_type TEXT
        CHECK (root_type IN (
            'measurement_primary', 'participatory_finding',
            'committee_assertion', 'derived_calculation', 'untraced')), root_ref_id TEXT REFERENCES evidence_sources(ref_id), echo_of TEXT, measurement_paradigm TEXT
        CHECK (measurement_paradigm IN (
            'swept_path_dynamic', 'static_turning_circle', 'static_clearance',
            'anthropometric_percentile', 'instrumented_physical_measurement',
            'route_metric', 'field_observation', 'participatory_spatial',
            'stated_unmeasured')), device_class TEXT
        CHECK (device_class IN (
            'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter',
            'bariatric_manual', 'bariatric_power', 'walker_rollator',
            'mixed', 'not_device_scoped')), root_population_note TEXT, file_anchor TEXT, root_classification_basis TEXT, contested INTEGER NOT NULL DEFAULT 0
        CHECK (contested IN (0, 1)),

  FOREIGN KEY (ref_id) REFERENCES evidence_sources(ref_id),
  FOREIGN KEY (population_code) REFERENCES populations(population_code),
  FOREIGN KEY (promoted_to_rdc_id) REFERENCES reasoning_doc_citations(citation_id),

  -- Soft consistency: if claim_type='absent', claimed_value must be NULL
  --                  if claim_type!='absent', claimed_value must NOT be NULL
  CHECK (
    (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)
  )
);
INSERT INTO _new_source_value_extractions ("extraction_id", "ref_id", "slug", "parameter", "parameter_canonical", "population_code", "population_label", "jurisdiction", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "setting", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "file_anchor", "root_classification_basis", "contested") SELECT "extraction_id", "ref_id", "slug", "parameter", "parameter_canonical", "population_code", "population_label", "jurisdiction", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "setting", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "file_anchor", "root_classification_basis", "contested" FROM source_value_extractions;
DROP TABLE source_value_extractions;
ALTER TABLE _new_source_value_extractions RENAME TO source_value_extractions;
CREATE INDEX idx_sve_slug_param ON source_value_extractions(slug, parameter_canonical);
CREATE INDEX idx_sve_ref        ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status     ON source_value_extractions(extraction_status);

-- ---- spec_value_probes: +slug (31 rows, 4 index(es), 1 view(s)) ----
CREATE TABLE _new_spec_value_probes (
    probe_id            TEXT PRIMARY KEY,
    walk_id             TEXT NOT NULL,
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    spec_value_origin   REAL NOT NULL,
    spec_unit           TEXT NOT NULL,
    direction           TEXT NOT NULL CHECK (direction IN ('up','down')),
    population          TEXT NOT NULL,
    claim_type          TEXT NOT NULL
                        CHECK (claim_type IN (
                            'minimum','maximum','target','range_low','range_high'
                        )),
    step_index          INTEGER NOT NULL,
    phase               TEXT NOT NULL
                        CHECK (phase IN (
                            'outer-pass-1st','outer-pass-2nd','outer-stop',
                            'refinement-pass-1st','refinement-pass-2nd','refinement-stop',
                            'final'
                        )),
    step_value          REAL NOT NULL,
    step_value_unit     TEXT NOT NULL,
    search_query        TEXT,
    search_query_alt    TEXT,
    passes_strict       INTEGER CHECK (passes_strict IN (0,1)),
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
, setting TEXT);
INSERT INTO _new_spec_value_probes ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "search_query", "search_query_alt", "passes_strict", "ref_id", "notes", "created_at", "created_by_session", "setting") SELECT "probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "search_query", "search_query_alt", "passes_strict", "ref_id", "notes", "created_at", "created_by_session", "setting" FROM spec_value_probes;
DROP TABLE spec_value_probes;
ALTER TABLE _new_spec_value_probes RENAME TO spec_value_probes;
CREATE INDEX idx_svp_slug_item  ON spec_value_probes(slug, item_code);
CREATE INDEX idx_svp_walk       ON spec_value_probes(walk_id, step_index);
CREATE INDEX idx_svp_item_phase ON spec_value_probes(item_code, phase);
CREATE INDEX idx_svp_ref        ON spec_value_probes(ref_id);

-- ---- supersession_check: +slug (134 rows, 4 index(es), 0 view(s)) ----
CREATE TABLE _new_supersession_check (
    check_id            TEXT PRIMARY KEY,
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    anchor_tier         INTEGER NOT NULL CHECK(anchor_tier BETWEEN 1 AND 6),
    anchor_evidence_type TEXT NOT NULL,  -- co1, co2, clinical, sr_meta, standard_eb, national_fw, code, grey

    -- The outcome of the supersession search
    outcome             TEXT NOT NULL CHECK(outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )),

    -- Outcome details
    superseding_ref_ids  TEXT,  -- JSON array of ref_ids for superseded_by / refined_by / divergent
    superseding_dois     TEXT,  -- JSON array of DOIs for not-yet-INSERTed candidates (rule #10 gate)
    refinement_dimension TEXT,  -- For refined_by: which parameter/population/outcome dimension was refined
    divergence_notes     TEXT,  -- For divergent_no_supersession: prose summary of the divergence

    -- Search strategy record (so the check is replayable)
    search_strategy_record TEXT NOT NULL,  -- JSON: {tool, query, date_filter, tier_filter, candidates_returned, candidates_reviewed}
    candidates_returned  INTEGER NOT NULL DEFAULT 0,
    candidates_reviewed  INTEGER NOT NULL DEFAULT 0,

    -- Audit fields
    checked_at           TEXT NOT NULL,
    checked_by_session   TEXT NOT NULL,
    check_method         TEXT NOT NULL CHECK(check_method IN (
        'pubmed_search', 'scholar_gateway', 'cochrane_direct',
        'standards_body_direct', 'multilingual_research',
        'composite'
    )),
    notes                TEXT,

    -- Integrity constraints
    CHECK (
        -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')
    ),
    CHECK (
        -- refined_by must name the refinement dimension
        outcome != 'refined_by' OR refinement_dimension IS NOT NULL
    ),
    CHECK (
        -- divergent_no_supersession must include divergence notes
        outcome != 'divergent_no_supersession' OR divergence_notes IS NOT NULL
    ),
    CHECK (
        -- co1_addition_logged only valid for Co-1 sources
        outcome != 'co1_addition_logged' OR anchor_evidence_type = 'co1'
    )
);
INSERT INTO _new_supersession_check ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "superseding_ref_ids", "superseding_dois", "refinement_dimension", "divergence_notes", "search_strategy_record", "candidates_returned", "candidates_reviewed", "checked_at", "checked_by_session", "check_method", "notes") SELECT "check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "superseding_ref_ids", "superseding_dois", "refinement_dimension", "divergence_notes", "search_strategy_record", "candidates_returned", "candidates_reviewed", "checked_at", "checked_by_session", "check_method", "notes" FROM supersession_check;
DROP TABLE supersession_check;
ALTER TABLE _new_supersession_check RENAME TO supersession_check;
CREATE INDEX idx_supersession_check_slug ON supersession_check(slug);
CREATE INDEX idx_supersession_check_ref ON supersession_check(ref_id);
CREATE INDEX idx_supersession_check_outcome ON supersession_check(outcome);
CREATE INDEX idx_supersession_check_checked_at ON supersession_check(checked_at);

-- ---- search_candidates: +found_under_slug, suggested_slug (18 rows, 2 index(es), 0 view(s)) ----
CREATE TABLE _new_search_candidates (
  candidate_id     INTEGER PRIMARY KEY,
  exec_id          INTEGER REFERENCES search_executions(exec_id),  -- which search surfaced it
  found_under_slug TEXT NOT NULL REFERENCES slugs(slug),  -- the slug being searched when it surfaced
  suggested_slug   TEXT REFERENCES slugs(slug),  -- best-fit slug; NULL = MISCELLANEOUS / undecided
  disposition      TEXT NOT NULL CHECK (disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED')),
  title            TEXT NOT NULL,
  locator          TEXT,                 -- DOI / URL / PMID as retrieved
  locator_status   TEXT CHECK (locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')),
  tier_guess       INTEGER CHECK (tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6),
  harm_finding     INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),
  why_not_admitted TEXT,                 -- required in practice: metadata gap, unverified, etc.
  notes            TEXT,
  session          TEXT NOT NULL,
  created_at       TEXT NOT NULL
) STRICT;
INSERT INTO _new_search_candidates ("candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "session", "created_at") SELECT "candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "session", "created_at" FROM search_candidates;
DROP TABLE search_candidates;
ALTER TABLE _new_search_candidates RENAME TO search_candidates;
CREATE INDEX ix_sc_suggested ON search_candidates(suggested_slug, disposition);
CREATE INDEX ix_sc_harm ON search_candidates(harm_finding);

-- ---- reasoning_doc_citations: +reasoning_doc_slug (14 rows, 4 index(es), 0 view(s)) ----
CREATE TABLE _new_reasoning_doc_citations (
    citation_id          TEXT PRIMARY KEY,
    reasoning_doc_slug   TEXT NOT NULL REFERENCES slugs(slug),
    parameter            TEXT NOT NULL,
    jurisdiction         TEXT,
    population           TEXT,
    claim_type           TEXT NOT NULL CHECK(claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )),
    claimed_value        TEXT,
    claimed_unit         TEXT,
    claim_text           TEXT,
    source_ref_id        TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    source_section       TEXT,
    value_match          TEXT CHECK(value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )),
    claim_match          TEXT CHECK(claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )),
    verified_at          TEXT NOT NULL,
    verified_by_session  TEXT NOT NULL,
    paywall_purchase_candidate INTEGER NOT NULL DEFAULT 0 CHECK(paywall_purchase_candidate IN (0,1)),
    notes                TEXT, setting TEXT,
    CHECK (
      (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT NULL) OR
      (claim_type IN ('qualitative','definitional') AND claim_text IS NOT NULL AND claim_match IS NOT NULL)
    )
);
INSERT INTO _new_reasoning_doc_citations ("citation_id", "reasoning_doc_slug", "parameter", "jurisdiction", "population", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_ref_id", "source_section", "value_match", "claim_match", "verified_at", "verified_by_session", "paywall_purchase_candidate", "notes", "setting") SELECT "citation_id", "reasoning_doc_slug", "parameter", "jurisdiction", "population", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_ref_id", "source_section", "value_match", "claim_match", "verified_at", "verified_by_session", "paywall_purchase_candidate", "notes", "setting" FROM reasoning_doc_citations;
DROP TABLE reasoning_doc_citations;
ALTER TABLE _new_reasoning_doc_citations RENAME TO reasoning_doc_citations;
CREATE INDEX idx_rdc_slug_param  ON reasoning_doc_citations(reasoning_doc_slug, parameter);
CREATE INDEX idx_rdc_ref         ON reasoning_doc_citations(source_ref_id);
CREATE INDEX idx_rdc_claim_type  ON reasoning_doc_citations(claim_type);
CREATE INDEX idx_rdc_paywall     ON reasoning_doc_citations(paywall_purchase_candidate) WHERE paywall_purchase_candidate = 1;

-- ---- term_item_links: +item_code (147 rows, 1 index(es), 0 view(s)) ----
CREATE TABLE _new_term_item_links (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    population          TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, item_code)
);
INSERT INTO _new_term_item_links ("term_id", "item_code", "population", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session") SELECT "term_id", "item_code", "population", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session" FROM term_item_links;
DROP TABLE term_item_links;
ALTER TABLE _new_term_item_links RENAME TO term_item_links;
CREATE INDEX idx_til_item    ON term_item_links(item_code);

-- ---- item_axis_links: +item_code (158 rows, 0 index(es), 0 view(s)) ----
CREATE TABLE _new_item_axis_links (
  item_code        TEXT NOT NULL REFERENCES items(item_code),
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  mechanism_note   TEXT,
  strength_band    TEXT CHECK (strength_band IN ('full','partial','weak')),
  use_mode         TEXT CHECK (use_mode IN ('independent','assisted','collective') OR use_mode IS NULL),
  source           TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (item_code, axis_code)
);
INSERT INTO _new_item_axis_links ("item_code", "axis_code", "mechanism_note", "strength_band", "use_mode", "source", "created_at", "created_by_session") SELECT "item_code", "axis_code", "mechanism_note", "strength_band", "use_mode", "source", "created_at", "created_by_session" FROM item_axis_links;
DROP TABLE item_axis_links;
ALTER TABLE _new_item_axis_links RENAME TO item_axis_links;

-- ---- population_axis_map: +population_code (53 rows, 0 index(es), 0 view(s)) ----
CREATE TABLE _new_population_axis_map (
  population_code  TEXT NOT NULL REFERENCES populations(population_code),
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  role             TEXT NOT NULL CHECK (role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL')),
  note             TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (population_code, axis_code)
);
INSERT INTO _new_population_axis_map ("population_code", "axis_code", "role", "note", "created_at", "created_by_session") SELECT "population_code", "axis_code", "role", "note", "created_at", "created_by_session" FROM population_axis_map;
DROP TABLE population_axis_map;
ALTER TABLE _new_population_axis_map RENAME TO population_axis_map;

-- ---- slugs: +merged_into (106 rows, 0 index(es), 1 view(s)) ----
CREATE TABLE _new_slugs (
    slug                TEXT PRIMARY KEY,
    topic_directory     TEXT NOT NULL,
    sl_path             TEXT NOT NULL,
    bpc_path            TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','MERGED','STUB','PROVISIONAL'
                        )),
    merged_into         TEXT REFERENCES slugs(slug),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
, serves_axes TEXT);
INSERT INTO _new_slugs ("slug", "topic_directory", "sl_path", "bpc_path", "status", "merged_into", "created_at", "created_by_session", "updated_at", "updated_by_session", "serves_axes") SELECT "slug", "topic_directory", "sl_path", "bpc_path", "status", "merged_into", "created_at", "created_by_session", "updated_at", "updated_by_session", "serves_axes" FROM slugs;
DROP TABLE slugs;
ALTER TABLE _new_slugs RENAME TO slugs;

-- ---- case_studies: +slug (0 rows, 2 index(es), 0 view(s)) ----
CREATE TABLE _new_case_studies (
  case_study_id   TEXT PRIMARY KEY,            -- CS-NNNN (validator-enforced in the model)
  slug            TEXT NOT NULL REFERENCES slugs(slug),
  title           TEXT NOT NULL,
  building_type   TEXT NOT NULL,
  location        TEXT NOT NULL,
  architect       TEXT,
  year            INTEGER,
  setting         TEXT,
  population_description TEXT,
  evidence_quality_tier  INTEGER CHECK (evidence_quality_tier IS NULL
                                        OR evidence_quality_tier BETWEEN 1 AND 3),
  cost_data       TEXT,
  cost_data_quality TEXT CHECK (cost_data_quality IS NULL OR cost_data_quality IN
                     ('VERIFIED','PROVISIONAL','GREY')),
  part_section    TEXT,                        -- e.g. §12.01
  limitations     TEXT,                        -- REQUIRED in practice: what this case cannot show
  harm_finding    INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),  -- failure/inadequacy case
  status          TEXT NOT NULL DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL,
  created_by_session TEXT NOT NULL,
  updated_at      TEXT,
  updated_by_session TEXT
, design_intent TEXT, populations_served_note TEXT, outcome_data TEXT, conflict_documented TEXT, failure_notes TEXT, construction_cost TEXT, accessible_design_premium TEXT, funding_sources TEXT, operational_cost_change TEXT, remediation_cost TEXT, roi_data TEXT, financial_evidence_tier INTEGER, financial_data_quality TEXT, evidence_contribution TEXT, part13_status TEXT, sources TEXT) STRICT;
INSERT INTO _new_case_studies ("case_study_id", "slug", "title", "building_type", "location", "architect", "year", "setting", "population_description", "evidence_quality_tier", "cost_data", "cost_data_quality", "part_section", "limitations", "harm_finding", "status", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "design_intent", "populations_served_note", "outcome_data", "conflict_documented", "failure_notes", "construction_cost", "accessible_design_premium", "funding_sources", "operational_cost_change", "remediation_cost", "roi_data", "financial_evidence_tier", "financial_data_quality", "evidence_contribution", "part13_status", "sources") SELECT "case_study_id", "slug", "title", "building_type", "location", "architect", "year", "setting", "population_description", "evidence_quality_tier", "cost_data", "cost_data_quality", "part_section", "limitations", "harm_finding", "status", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "design_intent", "populations_served_note", "outcome_data", "conflict_documented", "failure_notes", "construction_cost", "accessible_design_premium", "funding_sources", "operational_cost_change", "remediation_cost", "roi_data", "financial_evidence_tier", "financial_data_quality", "evidence_contribution", "part13_status", "sources" FROM case_studies;
DROP TABLE case_studies;
ALTER TABLE _new_case_studies RENAME TO case_studies;
CREATE INDEX ix_cs_slug ON case_studies(slug);
CREATE INDEX ix_cs_harm ON case_studies(harm_finding);

-- Recreate views (verbatim from sqlite_master).
CREATE VIEW v_coverage_priority AS
SELECT
    s.slug,
    ljm.jurisdiction,
    ljm.language,
    ljm.role,
    ( (CASE ljm.role WHEN 'PRIMARY' THEN 3 ELSE 1 END)
      + (CASE WHEN (SELECT COUNT(*) FROM search_executions se2
                    WHERE se2.slug = s.slug AND se2.deferred_reason IS NULL) = 0
              THEN 2 ELSE 0 END)
    ) AS priority_score,
    (SELECT COUNT(*) FROM search_executions se3
     WHERE se3.slug = s.slug AND se3.deferred_reason IS NULL) AS slug_searches
FROM slugs s
JOIN lang_jur_map ljm            -- CROSS JOIN: every in-scope slug x every required (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      WHERE se.slug = s.slug
        AND se.jurisdiction = ljm.jurisdiction
        AND se.language = ljm.language
  );

CREATE VIEW v_pmp_latest_walk AS
SELECT
    item_code,
    slug,
    walk_id,
    MAX(created_at) AS walk_completed_at,
    SUM(CASE WHEN phase IN (
            'outer-pass-1st','outer-pass-2nd',
            'refinement-pass-1st','refinement-pass-2nd'
        ) THEN 1 ELSE 0 END) AS supported_steps,
    SUM(CASE WHEN phase IN (
            'outer-stop','refinement-stop'
        ) THEN 1 ELSE 0 END) AS terminator_steps
FROM spec_value_probes
GROUP BY item_code, slug, walk_id;

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

CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id, sve.slug, sve.parameter, sve.root_id
    FROM source_value_extractions sve
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id);

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

PRAGMA foreign_keys = ON;

