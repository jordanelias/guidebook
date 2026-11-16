-- 138_drop_medical_lens.sql
-- SCHEMA migration, GENERATED from sqlite_master of the schema-137 database. Owner instruction 2026-11-16, quoted in
-- references/project-standards.md ("Owner instruction 2026-11-16 -- the medical taxonomy, the medical maps and the
-- medical codes are deleted"): the medical lens is removed. Dropped: base_taxonomy_medical, identity_medical_map and
-- icf_medical_map (no row in any of them), and the medical_code column of gaps, specifications, search_executions, extraction_lens_links, determination_gates, source_value_extractions (NULL on every row of
-- every one of them). Tooling; no research row, no row changed or lost.
--
-- SQLite cannot drop a column that carries a foreign key, a CHECK or an index, so each of the six tables is rebuilt as
-- 114, 131 and 136 rebuilt theirs: the sequence floor of an AUTOINCREMENT table is captured (DROP TABLE takes its
-- row), every view that names a rebuilt or dropped table (and every view that names such a view) is dropped, each new
-- table is created, filled by column name, the old one dropped and the new one renamed, its indexes and trigger are
-- recreated, the floors are restored and the views are recreated from their stored text. The only edits to any stored
-- text are the medical-lens ones: the column, the term in the three CHECKs and the two unique indexes that carried it,
-- and the term in the six views that selected it. The foreign keys of other tables into a rebuilt table name it by
-- text and resolve to the new table.
CREATE TEMP TABLE _138_seq AS SELECT name, seq FROM sqlite_sequence;

DROP VIEW "v_coverage_priority";
DROP VIEW "v_scan_ledger";
DROP VIEW "v_unregistered_roots";
DROP VIEW "v_determination_provenance";
DROP VIEW "v_value_independence";
DROP VIEW "v_derived_figure_check";
DROP VIEW "v_root_id_conflicts";
DROP VIEW "v_open_determination_gates";
DROP VIEW "v_coverage_lens";
DROP VIEW "v_coverage_language";
DROP VIEW "v_live_lens_links";
DROP VIEW "v_coverage_branch";
DROP VIEW "v_coverage_jurisdiction";
DROP VIEW "v_gap_subject";
DROP VIEW "v_research_scope";
DROP VIEW "v_best_practice";
DROP VIEW "v_source_admission";
DROP VIEW "v_source_reach_all";
DROP VIEW "v_item_provenance";
DROP VIEW "v_code_floor_only";
DROP VIEW "v_pending";
DROP VIEW "v_divergence";

CREATE TABLE "_138_new_gaps" (
    gap_id              TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG',
                            'CI','DEC','CONF','AUDT'
                        )),
    priority            TEXT NOT NULL CHECK(priority IN ('P1','P2','P3')),
    status              TEXT NOT NULL
                        CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%'),
    skill               TEXT,
    section             TEXT,
    description         TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
, falsification_condition TEXT, confidence_interval TEXT, shift_conditions TEXT, named_dissenter TEXT, mining_addressability TEXT
    CHECK(mining_addressability IS NULL OR mining_addressability IN (
        'ADDRESSABLE',
        'NOT-ADDRESSABLE',
        'TRIAGE-NEEDED'
    )), parameter_id INTEGER REFERENCES base_parameters(parameter_id), identity_code TEXT REFERENCES "base_taxonomy_identity"(identity_code), icf_code TEXT REFERENCES base_icf(icf_code), needs_code TEXT REFERENCES access_needs(need_code), jurisdiction TEXT, language TEXT);

INSERT INTO "_138_new_gaps" ("gap_id", "category", "priority", "status", "skill", "section", "description", "created_at", "created_by_session", "updated_at", "updated_by_session", "falsification_condition", "confidence_interval", "shift_conditions", "named_dissenter", "mining_addressability", "parameter_id", "identity_code", "icf_code", "needs_code", "jurisdiction", "language") SELECT "gap_id", "category", "priority", "status", "skill", "section", "description", "created_at", "created_by_session", "updated_at", "updated_by_session", "falsification_condition", "confidence_interval", "shift_conditions", "named_dissenter", "mining_addressability", "parameter_id", "identity_code", "icf_code", "needs_code", "jurisdiction", "language" FROM "gaps";
DROP TABLE "gaps";
ALTER TABLE "_138_new_gaps" RENAME TO "gaps";
CREATE INDEX idx_gap_priority_status ON gaps(priority, status);
CREATE INDEX idx_gaps_mining_addressability ON gaps(mining_addressability);

CREATE TABLE "_138_new_specifications" (
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
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker = '○')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL)),
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code) IS NOT NULL)
);

INSERT INTO "_138_new_specifications" ("specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths", "retired_at", "retired_by_session", "retirement_reason", "superseded_by_specification_id", "rests_on_proxy_inference", "value_notations", "marker") SELECT "specification_id", "parameter_id", "identity_code", "icf_code", "needs_code", "state", "design_scale", "convergence_id", "confidence_dimensions_present", "confidence_dimensions_absent", "confidence_synthesis_basis", "gap_register_id", "not_applicable_rationale", "tier_basis", "governing_refs", "rule_version", "derivation_sha", "code_floor_only", "value_min", "value_max", "value_unit", "falsification_condition", "has_unverified_sources", "all_sources_disqualified", "regulatory_stratum_only", "created_at", "created_by_session", "updated_at", "updated_by_session", "value_note", "functional_basis", "derivation_rationale", "cultural_claim_anchor", "derivation_paths", "retired_at", "retired_by_session", "retirement_reason", "superseded_by_specification_id", "rests_on_proxy_inference", "value_notations", "marker" FROM "specifications";
DROP TABLE "specifications";
ALTER TABLE "_138_new_specifications" RENAME TO "specifications";
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

CREATE TABLE "_138_new_search_executions" (
  exec_id              INTEGER PRIMARY KEY,
  slug                 TEXT REFERENCES slugs(slug),   -- NULL when the search is for a parameter or mines a source (R43)
  parameter_id         INTEGER REFERENCES base_parameters(parameter_id),   -- the parameter a slug-less search was FOR (R43)
  jurisdiction         TEXT,                 -- NULL = jurisdiction-agnostic search
  language             TEXT NOT NULL,        -- ISO; one of the 19 research languages
  -- hierarchy branch the search TARGETED (diffable against what was FOUND):
  target_tier          INTEGER CHECK (target_tier IS NULL OR target_tier BETWEEN 1 AND 6),
  target_evidence_type TEXT CHECK (target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  target_scope         TEXT CHECK (target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')),
  -- the verbatim, replayable query:
  query_text           TEXT NOT NULL,
  terms_used           TEXT,                 -- JSON array of term ids
  engine               TEXT NOT NULL,        -- pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
  -- depth as real method, not booleans:
  depth_method         TEXT NOT NULL CHECK (depth_method IN ('scoping','systematic')),
  mining_direction     TEXT CHECK (mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')),
  -- yield:
  results_found        INTEGER NOT NULL DEFAULT 0,
  results_screened     INTEGER NOT NULL DEFAULT 0,
  results_admitted     INTEGER NOT NULL DEFAULT 0,
  saturation_signal    TEXT CHECK (saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')),
  admitted_ref_ids     TEXT,                 -- JSON array of evidence_sources.ref_id
  deferred_reason      TEXT,                 -- non-NULL => deliberate no-search for this cell
  backfill             INTEGER NOT NULL DEFAULT 0 CHECK (backfill IN (0,1)),
  created_by_session              TEXT NOT NULL,
  created_at          TEXT NOT NULL, findings_note TEXT, harm_finding INTEGER NOT NULL DEFAULT 0, prior_expectation TEXT, origin TEXT NOT NULL DEFAULT 'planned'
  CHECK (origin IN ('planned','incidental','adversarial-pass','owner-supplied','lead-index')), mined_ref_id TEXT REFERENCES evidence_sources(ref_id), origin_pass_id INTEGER
  REFERENCES adversarial_passes(pass_id) CHECK (origin_pass_id IS NULL OR origin = 'adversarial-pass'), updated_at TEXT, updated_by_session TEXT, identity_code TEXT REFERENCES "base_taxonomy_identity"(identity_code), icf_code TEXT REFERENCES base_icf(icf_code), needs_code TEXT REFERENCES access_needs(need_code), absence_class TEXT
  CHECK (absence_class IS NULL OR absence_class IN ('query_shape_failure', 'wrong_index', 'genuine_absence'))
  CHECK (absence_class IS NULL OR results_found = 0), gap_id TEXT REFERENCES gaps(gap_id),        -- explicit ISO ts (deterministic under rebuild)
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids)),
  CHECK (COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL)   -- a search says what it is for (R43)
) STRICT;

INSERT INTO "_138_new_search_executions" ("exec_id", "slug", "parameter_id", "jurisdiction", "language", "target_tier", "target_evidence_type", "target_scope", "query_text", "terms_used", "engine", "depth_method", "mining_direction", "results_found", "results_screened", "results_admitted", "saturation_signal", "admitted_ref_ids", "deferred_reason", "backfill", "created_by_session", "created_at", "findings_note", "harm_finding", "prior_expectation", "origin", "mined_ref_id", "origin_pass_id", "updated_at", "updated_by_session", "identity_code", "icf_code", "needs_code", "absence_class", "gap_id") SELECT "exec_id", "slug", "parameter_id", "jurisdiction", "language", "target_tier", "target_evidence_type", "target_scope", "query_text", "terms_used", "engine", "depth_method", "mining_direction", "results_found", "results_screened", "results_admitted", "saturation_signal", "admitted_ref_ids", "deferred_reason", "backfill", "created_by_session", "created_at", "findings_note", "harm_finding", "prior_expectation", "origin", "mined_ref_id", "origin_pass_id", "updated_at", "updated_by_session", "identity_code", "icf_code", "needs_code", "absence_class", "gap_id" FROM "search_executions";
DROP TABLE "search_executions";
ALTER TABLE "_138_new_search_executions" RENAME TO "search_executions";
CREATE INDEX ix_se_cell   ON search_executions(slug, jurisdiction, language);
CREATE INDEX ix_se_branch ON search_executions(target_tier, target_evidence_type, target_scope);

CREATE TABLE "_138_new_extraction_lens_links" (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    -- THE THREE LENSES, typed, one per row (2026-08-28 shape; "never two lenses in one row").
    identity_code       TEXT REFERENCES base_taxonomy_identity(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    -- THE WARRANT (rule 8: a judgment records its answer and its evidence in named columns).
    --   named_in_text       the figure's own words name the users / function / need (D-2)
    --   heading             the provision names no one; its heading names the group (OD-31)
    --   study_participants  a study's own participants are this group (2026-08-25 grade rule)
    --   carried             moved by migration 131 from the retired column; no judged warrant yet
    basis               TEXT NOT NULL CHECK (basis IN
                            ('named_in_text', 'heading', 'study_participants', 'carried')),
    basis_text          TEXT,          -- the exact words that warrant the link
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL)
         + (needs_code IS NOT NULL) = 1),
    CHECK ((basis = 'carried') = (basis_text IS NULL)),
    CHECK (basis_text IS NULL OR length(trim(basis_text)) > 0),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL)
       AND (retired_at IS NULL) = (retirement_reason IS NULL))
);

INSERT INTO "_138_new_extraction_lens_links" ("link_id", "extraction_id", "identity_code", "icf_code", "needs_code", "basis", "basis_text", "retired_at", "retired_by_session", "retirement_reason", "created_at", "created_by_session", "updated_at", "updated_by_session") SELECT "link_id", "extraction_id", "identity_code", "icf_code", "needs_code", "basis", "basis_text", "retired_at", "retired_by_session", "retirement_reason", "created_at", "created_by_session", "updated_at", "updated_by_session" FROM "extraction_lens_links";
DROP TABLE "extraction_lens_links";
ALTER TABLE "_138_new_extraction_lens_links" RENAME TO "extraction_lens_links";
CREATE UNIQUE INDEX ux_extraction_lens_live ON extraction_lens_links
    (extraction_id, COALESCE(identity_code, ''), COALESCE(icf_code, ''),
     COALESCE(needs_code, ''))
    WHERE retired_at IS NULL;
CREATE INDEX ix_ell_extraction ON extraction_lens_links(extraction_id);
CREATE INDEX ix_ell_identity   ON extraction_lens_links(identity_code) WHERE retired_at IS NULL;
CREATE INDEX ix_ell_icf        ON extraction_lens_links(icf_code)      WHERE retired_at IS NULL;
CREATE INDEX ix_ell_needs      ON extraction_lens_links(needs_code)    WHERE retired_at IS NULL;

CREATE TABLE "_138_new_determination_gates" (
    gate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id        INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- The lens the finding applies to, NULL meaning every lens on this parameter. Not an FK set like
    -- specifications' four, because a gate is raised against a parameter by an audit that may not know which cells
    -- exist yet. A gate is skipped for a cell only when the cell carries a DIFFERENT code in a lens the gate names; a lens the cell does not carry never skips it (the rule the identity column always had).
    identity_code       TEXT REFERENCES "base_taxonomy_identity"(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    verdict             TEXT NOT NULL
                        CHECK (verdict IN ('UNLINKED', 'MISLINKED',
                                           'UNDER-CONSERVATIVE', 'CONTRADICTS', 'QUESTION')),
    -- The ladder-inversion guard: how strong the thing raising the gate actually is. A QUESTION has no such
    -- thing and carries NULL in all three trigger columns; every other verdict states them.
    trigger_ref_id      TEXT REFERENCES evidence_sources(ref_id),
    trigger_tier        INTEGER CHECK (trigger_tier BETWEEN 1 AND 6),
    trigger_evidence_type TEXT,
    detail              TEXT NOT NULL,
    raised_at           TEXT NOT NULL,
    raised_by_session   TEXT NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution_rationale TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL
            AND resolution_rationale IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution_rationale IS NOT NULL)),
    CHECK ((verdict = 'QUESTION'
            AND trigger_tier IS NULL AND trigger_evidence_type IS NULL AND trigger_ref_id IS NULL)
        OR (verdict <> 'QUESTION'
            AND trigger_tier IS NOT NULL AND trigger_evidence_type IS NOT NULL))
);

INSERT INTO "_138_new_determination_gates" ("gate_id", "parameter_id", "identity_code", "icf_code", "needs_code", "verdict", "trigger_ref_id", "trigger_tier", "trigger_evidence_type", "detail", "raised_at", "raised_by_session", "resolved_at", "resolved_by_session", "resolution_rationale") SELECT "gate_id", "parameter_id", "identity_code", "icf_code", "needs_code", "verdict", "trigger_ref_id", "trigger_tier", "trigger_evidence_type", "detail", "raised_at", "raised_by_session", "resolved_at", "resolved_by_session", "resolution_rationale" FROM "determination_gates";
DROP TABLE "determination_gates";
ALTER TABLE "_138_new_determination_gates" RENAME TO "determination_gates";
CREATE INDEX idx_gates_open ON determination_gates(parameter_id, resolved_at);

CREATE TABLE "_138_new_source_value_extractions" (
  extraction_id          INTEGER PRIMARY KEY AUTOINCREMENT,

  -- THE HAND-OFF KEY (D-0168; pinned by the blocking judgment_handoff_shape check):
  -- NOT NULL, a real FK at the evidence item, and NO UNIQUE index over it anywhere.
  ref_id                 TEXT NOT NULL REFERENCES evidence_sources(ref_id),

  -- The slug this extraction was mined under: HISTORY. No writer sets it after migration 114 (the scan
  -- contract, LED-195: a slug guides what is searched, not what is read from a source), so it is NULL on every
  -- later row. The admission record is source_slug_links.
  slug                   TEXT REFERENCES slugs(slug),

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

  -- THE THREE LENSES: HISTORY since migration 131 (OR-1c). A figure's lens is a set of rows in
  -- extraction_lens_links, read through v_live_lens_links; these four columns are held NULL by the CHECK
  -- at the foot of this table and are never written again. They are kept because committed data
  -- migrations INSERT them (CLAUDE.md rule 5: a column a committed data migration INSERTs can never be
  -- dropped). Until 131 they were real typed FKs, one per lens (owner 2026-08-28, replacing
  -- `population_code` and the free-text `population_label`), under D-0182's "at least one" CHECK.
  identity_code          TEXT REFERENCES "base_taxonomy_identity"(identity_code),
  icf_code               TEXT REFERENCES base_icf(icf_code),
  needs_code             TEXT REFERENCES access_needs(need_code),

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
  root_id                TEXT REFERENCES external_root_registry(root_id),   -- registry-only (R24); an in-corpus root is root_ref_id
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
                             'lower_limb_prosthesis', 'crutches', 'cane',
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
  CHECK (comparator IS NULL OR comparator IN ('=', '<', '<=', '>', '>=', 'between', 'approx')), harm_finding INTEGER NOT NULL DEFAULT 0
  CHECK (harm_finding IN (0, 1))
  CHECK (harm_finding = 0 OR figure_role = 'finding'), value_as_written TEXT CHECK (value_as_written IS NULL OR length(trim(value_as_written)) > 0),

  -- Carried across verbatim: if claim_type='absent', claimed_value must be NULL; if it
  -- is anything else, claimed_value must be present. `db.py add-extraction` refuses both
  -- violations in words BEFORE the INSERT, so an operator gets a sentence rather than
  -- "CHECK constraint failed".
  CHECK (
    (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)
  ),

  -- HISTORY, retired by migration 131: a figure's lens lives in extraction_lens_links (OR-1c,
  -- owner 2026-11-06). The four columns are kept because committed data migrations INSERT them (rule 5:
  -- a column a committed data migration INSERTs can never be dropped) and are held NULL here; never
  -- written again. D-0182 (a link must be tied to at least one lens) moved to the writers and to the
  -- blocking test_db_integrity case that reads v_live_lens_links.
  CHECK (COALESCE(identity_code, icf_code, needs_code) IS NULL)
);

INSERT INTO "_138_new_source_value_extractions" ("extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator", "harm_finding", "value_as_written") SELECT "extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator", "harm_finding", "value_as_written" FROM "source_value_extractions";
DROP TABLE "source_value_extractions";
ALTER TABLE "_138_new_source_value_extractions" RENAME TO "source_value_extractions";
CREATE INDEX idx_sve_ref    ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status ON source_value_extractions(extraction_status);
CREATE INDEX ix_sve_locator ON source_value_extractions(loc_section, loc_clause);
CREATE INDEX idx_sve_param_ref ON source_value_extractions(parameter_id, ref_id);

DROP TABLE "base_taxonomy_medical";
DROP TABLE "identity_medical_map";
DROP TABLE "icf_medical_map";

DELETE FROM sqlite_sequence WHERE name IN ('determination_gates', 'extraction_lens_links', 'source_value_extractions', 'specifications');
INSERT INTO sqlite_sequence (name, seq) SELECT name, seq FROM _138_seq WHERE name IN ('determination_gates', 'extraction_lens_links', 'source_value_extractions', 'specifications');
DROP TABLE _138_seq;

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

CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
                            AND bp.status = 'active'
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1
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

CREATE VIEW v_source_admission AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.verification_disposition,
    se.exec_id,
    se.slug                     AS admitted_under_slug,
    se.query_text,
    se.engine,
    se.language,
    se.jurisdiction             AS search_jurisdiction,
    se.depth_method,
    se.mining_direction,
    se.target_tier,
    se.backfill                 AS search_was_backfilled,
    se.created_by_session                  AS admitting_session,
    se.created_at              AS admitted_at,
    -- The research-stage prior, reached by pointer rather than copied onto the
    -- evidence row. This is what makes CHECK 7 answerable.
    se.prior_expectation
FROM evidence_sources es
JOIN search_admissions sa ON sa.ref_id  = es.ref_id
JOIN search_executions se ON se.exec_id = sa.exec_id;

CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND retired_at IS NULL;

CREATE VIEW v_research_scope AS
-- v_research_scope: the (language, jurisdiction) pairs the research scope OWES a search for.
--
-- The ONE home of "what is owed": every lang_jur_map row not recorded `scoped-out`. A NULL scope_status is owed --
-- an unrecorded scope never shrinks the requirement (on 2026-11-06 marking four languages `scoped-out` left every
-- other row NULL, and `coverage` read required 0/0, complete true). The fill of scope_status is a data migration
-- after owner question 5; until then the requirement is the whole map, less what is recorded `scoped-out`.
-- Readers: v_coverage_priority, `db.py coverage`.
SELECT language, jurisdiction, role
  FROM lang_jur_map
 WHERE COALESCE(scope_status, 'in-scope') <> 'scoped-out';

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

CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
WHERE deferred_reason IS NULL
GROUP BY 1, 2;

CREATE VIEW v_coverage_branch AS
SELECT slug, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction,
       target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5;

CREATE VIEW v_live_lens_links AS
SELECT link_id, extraction_id, identity_code, icf_code, needs_code,
       basis, basis_text, created_at, created_by_session
  FROM extraction_lens_links
 WHERE retired_at IS NULL;

CREATE VIEW v_coverage_language AS
SELECT slug, UPPER(language) AS language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, UPPER(language);

CREATE VIEW v_coverage_lens AS
SELECT slug, parameter_id, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction, UPPER(language) AS language,
       identity_code, icf_code, needs_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
GROUP BY 1, 2, 3, 4, 5, 6, 7;

CREATE VIEW v_open_determination_gates AS
SELECT g.gate_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.verdict,
       g.trigger_ref_id, g.trigger_tier, g.trigger_evidence_type, g.detail,
       g.raised_at, g.raised_by_session
  FROM determination_gates g
 WHERE g.resolved_at IS NULL;

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
      -- 104: active parameters only; a retired parameter's extractions are history.
      AND p.status = 'active'
    GROUP BY sve.parameter_id, t.canonical_en;

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

CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a non-absent extraction exists for the pair (any figure_role).
--   2 STATED-ABSENT      only claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   4 BLOCKED            no full reading covers the pair AND the source carries an obstacle
--                        processing_blocked_reason (below): the full text could not be
--                        obtained or read, so the pair is not reading debt until a full
--                        reading is recorded. Any partial / fragment / abstract reading of
--                        the pair is still named in scan_id / text_scope / method.
--   5 READ-PARTIAL       only partial / fragment / abstract readings cover it, and no
--                        obstacle stands: the full text is obtainable and unread -- debt.
--   6 NOT-READ           no reading covers it.
-- WHY THIS ORDER (it is derived from what each fact proves; 122 ranked BLOCKED above every
-- reading and 123 below every reading, both guesses): a FULL reading proves the obstacle
-- gone, since the whole text was read, so 3 outranks 4. A partial, fragment or abstract
-- reading proves nothing about the full text, so under a standing obstacle 4 outranks 5.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >= parameter_id
-- (the parameter existed when the reading was made), or targeted at that parameter. Rows 1
-- and 2 win over readings because a row written is stronger evidence than a reading
-- recorded; 3 wins over the rest because a full reading supersedes a partial one.
--
-- THE BLOCKED CASE BELOW IS THE ONE HOME of "the text could not be obtained or read", and
-- this header is the ONE HOME of the classification of every processing_blocked_reason
-- value (evidence_sources CHECK, migration 091); each value appears here as a bare token
-- under exactly one head, and a test derives the CHECK and fails on a value this header
-- does not name. The writers and gates read this view's status, never the column. NOTHING
-- CLEARS THE COLUMN: it is the retrieval record and stays as history; the ledger alone says
-- whether a pair is still blocked.
--   obstacle to the text (BLOCKED, above):  no-full-text, paywalled, language.
--   copy of a typed fact (not an obstacle; the writers refuse it by pointer -- the judgement
--     lives in db.py _BLOCK_REASON_COPIES): no-quantified-claims -> a recorded full reading;
--     superseded -> superseded_by_ref_id.
--   pending owner question 8 of the round-3 adjudication, treated as NULL (the source owes
--     its reading): out-of-scope, tier-not-required (they say no text was unobtainable);
--     no-doi, not-indexed (migration 091's comments describe discovery -- "no resolvable
--     identifier for automated paths", "absent from the indexes the pipeline queries" --
--     not an obstacle to a text in hand, and a URL-only report admitted without a DOI can
--     be read).
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id, e.processing_blocked_reason
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id, pr.processing_blocked_reason,
           (SELECT s.scan_id FROM source_scans s
             WHERE s.ref_id = pr.ref_id
               AND ((s.mode = 'catalogue' AND s.catalogue_version >= pr.parameter_id)
                 OR (s.mode = 'targeted' AND s.target_parameter_id = pr.parameter_id))
             ORDER BY (s.text_scope = 'full') DESC, (s.method = 'full-read') DESC,
                      s.scan_id DESC
             LIMIT 1) AS scan_id
      FROM pairs pr
)
SELECT b.ref_id,
       b.parameter_id,
       CASE
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent') THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN b.processing_blocked_reason IN
              ('no-full-text', 'paywalled', 'language') THEN 'BLOCKED'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

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
JOIN v_research_scope ljm        -- CROSS JOIN: every in-scope slug x every owed (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
      WHERE se.slug = s.slug
        AND se.deferred_reason IS NULL
        AND COALESCE(b.parent_code, se.jurisdiction) = ljm.jurisdiction
        AND UPPER(se.language) = ljm.language
  );

PRAGMA user_version = 138;
