# 30 — Data tables (Layer 3 container shape)

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


56 tables, 23 views, 12 empty tables. Stage = `governance/stage-map.yaml` (JUDGED by the owner's sessions; `infrastructure` is not a stage).

## 30.1 Tables by stage

### base (18 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| access_duration | 3 | 4 | — |
| access_need_icf | 43 | 7 | icf_code→base_icf.icf_code; need_code→access_needs.need_code |
| access_needs | 17 | 9 | — |
| access_stakes | 3 | 4 | — |
| base_icf | 72 | 8 | — |
| base_parameters | 10 | 12 | direction_ref_id→evidence_sources.ref_id; merged_into→base_parameters.parameter_id; term_id→terms.term_id |
| base_taxonomy_identity | 23 | 9 | parent_code→base_taxonomy_identity.identity_code |
| base_taxonomy_medical | 0 | 9 | — |
| icf_medical_map | 0 | 7 | medical_code→base_taxonomy_medical.medical_code; icf_code→base_icf.icf_code |
| identity_icf_map | 61 | 9 | icf_code→base_icf.icf_code; identity_code→base_taxonomy_identity.identity_code |
| identity_medical_map | 0 | 6 | medical_code→base_taxonomy_medical.medical_code; identity_code→base_taxonomy_identity.identity_code |
| lang_jur_map | 70 | 7 | — |
| life_stage_modifiers | 2 | 5 | — |
| parameter_declinations | 1 | 7 | term_id→terms.term_id |
| rooms | 17 | 10 | — |
| slugs | 106 | 10 | merged_into→slugs.slug |
| term_aliases | 2382 | 11 | observation_id→observed_terms.observation_id; term_id→terms.term_id |
| terms | 94 | 12 | — |

### research (8 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| citation_mining | 38 | 13 | slug→slugs.slug |
| gap_mining | 0 | 12 | gap_id→gaps.gap_id |
| research_code_leads | 96 | 11 | — |
| search_admissions | 61 | 4 | ref_id→evidence_sources.ref_id; exec_id→search_executions.exec_id |
| search_candidates | 155 | 19 | resolved_ref_id→evidence_sources.ref_id; suggested_slug→slugs.slug; found_under_slug→slugs.slug; exec_id→search_executions.exec_id |
| search_execution_artefacts | 117 | 4 | exec_id→search_executions.exec_id |
| search_executions | 203 | 35 | medical_code→base_taxonomy_medical.medical_code; needs_code→access_needs.need_code; icf_code→base_icf.icf_code; identity_code→base_taxonomy_identity.identity_code; origin_pass_id→adversarial_passes.pass_id; mined_ref_id→evidence_sources.ref_id; parameter_id→base_parameters.parameter_id; slug→slugs.slug |
| source_locators | 893 | 23 | — |

### evidence (8 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| case_studies | 0 | 37 | slug→slugs.slug |
| economics_entries | 1 | 25 | ref_id→evidence_sources.ref_id |
| evidence_source_authors | 142 | 14 | ref_id→evidence_sources.ref_id |
| evidence_sources | 59 | 97 | — |
| external_root_registry | 0 | 8 | — |
| observed_terms | 96 | 11 | ref_id→evidence_sources.ref_id |
| source_scans | 18 | 16 | target_parameter_id→base_parameters.parameter_id; ref_id→evidence_sources.ref_id |
| source_slug_links | 71 | 8 | slug→slugs.slug; ref_id→evidence_sources.ref_id |

### judgment (5 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| evidence_population_match | 61 | 11 | gap_id→gaps.gap_id; ref_id→evidence_sources.ref_id |
| extraction_follow_ups | 0 | 9 | extraction_id→source_value_extractions.extraction_id |
| extraction_relations | 57 | 12 | to_extraction_id→source_value_extractions.extraction_id; from_extraction_id→source_value_extractions.extraction_id |
| source_value_extractions | 214 | 52 | promoted_to_rdc_id→reasoning_doc_citations.citation_id; root_ref_id→evidence_sources.ref_id; root_id→external_root_registry.root_id; medical_code→base_taxonomy_medical.medical_code; needs_code→access_needs.need_code; icf_code→base_icf.icf_code; identity_code→base_taxonomy_identity.identity_code; parameter_id→base_parameters.parameter_id; slug→slugs.slug; ref_id→evidence_sources.ref_id |
| term_adjudications | 90 | 9 | term_id→terms.term_id; observation_id→observed_terms.observation_id |

### synthesis (8 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| conflicts | 0 | 14 | parameter_id→base_parameters.parameter_id; gap_id→gaps.gap_id; pop_b→base_taxonomy_identity.identity_code; pop_a→base_taxonomy_identity.identity_code |
| connection_targets | 0 | 7 | extraction_id→source_value_extractions.extraction_id; identity_code→base_taxonomy_identity.identity_code; slug→slugs.slug; parameter_id→base_parameters.parameter_id; con_id→connections.con_id |
| connections | 0 | 12 | filed_in→slugs.slug |
| convergence_assessment | 5 | 13 | — |
| convergence_sources | 69 | 5 | ref_id→evidence_sources.ref_id; convergence_id→convergence_assessment.convergence_id |
| gaps | 110 | 16 | — |
| reasoning_doc_citations | 0 | 34 | source_ref_id→evidence_sources.ref_id; reasoning_doc_slug→slugs.slug |
| supersession_check | 0 | 18 | ref_id→evidence_sources.ref_id; slug→slugs.slug |

### specification (4 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| determination_gates | 1 | 13 | trigger_ref_id→evidence_sources.ref_id; identity_code→base_taxonomy_identity.identity_code; parameter_id→base_parameters.parameter_id |
| specification_extraction_links | 151 | 6 | extraction_id→source_value_extractions.extraction_id; specification_id→specifications.specification_id |
| specification_source_links | 38 | 5 | ref_id→evidence_sources.ref_id; specification_id→specifications.specification_id |
| specifications | 8 | 42 | superseded_by_specification_id→specifications.specification_id; gap_register_id→gaps.gap_id; convergence_id→convergence_assessment.convergence_id; medical_code→base_taxonomy_medical.medical_code; needs_code→access_needs.need_code; icf_code→base_icf.icf_code; identity_code→base_taxonomy_identity.identity_code; parameter_id→base_parameters.parameter_id |

### render (1 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| weighting_profile | 5 | 4 | — |

### infrastructure (4 tables)

| table | rows | cols | FK out (col→table.col) |
|---|---|---|---|
| adversarial_findings | 193 | 16 | pass_id→adversarial_passes.pass_id |
| adversarial_passes | 9 | 10 | — |
| data_migrations | 476 | 5 | — |
| decisions | 188 | 22 | — |

## 30.2 Views and the stages they span (a cross-stage view IS the pointer — CLAUDE.md §3)

| view | reads tables | stages spanned |
|---|---|---|
| v_best_practice | specifications | specification |
| v_code_floor_only | base_parameters, specifications, terms | base, specification |
| v_convergence_sources | convergence_assessment, convergence_sources, evidence_sources | evidence, synthesis |
| v_coverage_branch | search_executions | research |
| v_coverage_jurisdiction | search_executions | research |
| v_coverage_language | search_executions | research |
| v_coverage_lens | search_executions | research |
| v_coverage_priority | search_executions, slugs | base, research |
| v_derived_figure_check | extraction_relations, source_value_extractions | judgment |
| v_determination_provenance | base_parameters, evidence_sources, source_value_extractions, specification_extraction_links, specifications, terms | base, evidence, judgment, specification |
| v_divergence | convergence_assessment, specifications | specification, synthesis |
| v_evidence_authors | evidence_source_authors, evidence_sources | evidence |
| v_item_provenance | base_parameters, evidence_source_authors, evidence_sources, specification_source_links, specifications, terms | base, evidence, specification |
| v_open_determination_gates | determination_gates | specification |
| v_pending | gaps, specifications | specification, synthesis |
| v_registry_duplicate_descriptions | external_root_registry | evidence |
| v_research_scope | lang_jur_map | base |
| v_root_id_conflicts | source_value_extractions | judgment |
| v_scan_ledger | base_parameters, evidence_sources, source_scans, source_value_extractions | base, evidence, judgment |
| v_source_admission | evidence_sources, search_admissions, search_executions | evidence, research |
| v_source_reach_all | base_parameters, evidence_sources, source_slug_links, specification_source_links, specifications, terms | base, evidence, specification |
| v_unregistered_roots | base_parameters, external_root_registry, source_value_extractions, terms | base, evidence, judgment |
| v_value_independence | base_parameters, external_root_registry, source_value_extractions, terms | base, evidence, judgment |

## 30.3 Writable-set check (NOT NULL FK into an EMPTY table)

| table | column | → empty table |
|---|---|---|
| connection_targets | con_id | connections |
| icf_medical_map | medical_code | base_taxonomy_medical |
| identity_medical_map | medical_code | base_taxonomy_medical |

## 30.4 Full DDL (verbatim from sqlite_master)

### `access_duration` — base, 3 rows

```sql
CREATE TABLE access_duration (
  code TEXT PRIMARY KEY CHECK (code IN ('permanent','temporary','situational')),
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
)
```

### `access_need_icf` — base, 43 rows

```sql
CREATE TABLE "access_need_icf" (
  need_code   TEXT NOT NULL REFERENCES access_needs(need_code),
  icf_code    TEXT NOT NULL REFERENCES base_icf(icf_code),                       -- 'e250','b765','d510' …
  icf_type    TEXT NOT NULL CHECK (icf_type IN ('b','d','e','s')),
  confidence  TEXT NOT NULL CHECK (confidence IN ('confirmed','proposed')),
  notes        TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (need_code, icf_code)
)
```

### `access_needs` — base, 17 rows

```sql
CREATE TABLE access_needs (
  need_code       TEXT PRIMARY KEY,               -- 'A-NOSIGHT' …
  family          TEXT NOT NULL CHECK (family IN
                    ('perceiving','communicating','operating','pacing','environment_safety')),
  design_obligation TEXT NOT NULL,                 -- "the design must …"
  absorbs         TEXT,                            -- populations/situations it covers (prose, audit-side)
  typical_stakes  TEXT CHECK (typical_stakes IN ('safety-critical','exclusion','friction')),
  source_version  TEXT NOT NULL DEFAULT 'access-taxonomy v0.1',
  notes           TEXT,
  created_at      TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
)
```

### `access_stakes` — base, 3 rows

```sql
CREATE TABLE access_stakes (
  code TEXT PRIMARY KEY CHECK (code IN ('safety-critical','exclusion','friction')),
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
)
```

### `base_icf` — base, 72 rows

```sql
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
)
```

### `base_parameters` — base, 10 rows

```sql
CREATE TABLE "base_parameters" (
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
    updated_by_session  TEXT, direction_rationale TEXT, accessibility_direction TEXT
    CHECK (accessibility_direction IS NULL
        OR (accessibility_direction IN ('higher_is_better',
                                        'lower_is_better',
                                        'contested')
            AND direction_rationale IS NOT NULL)), direction_ref_id TEXT REFERENCES evidence_sources(ref_id),
    -- merged_into is meaningful only for a merged row, and required for one.
    CHECK ((status = 'merged' AND merged_into IS NOT NULL)
        OR (status <> 'merged' AND merged_into IS NULL))
)
```

### `base_taxonomy_identity` — base, 23 rows

```sql
CREATE TABLE "base_taxonomy_identity" (
  identity_code     TEXT PRIMARY KEY,
  display_name        TEXT NOT NULL,
  category            TEXT CHECK(category IN (
                        'mobility', 'sensory', 'cognitive', 'mental_health',
                        'pain_fatigue', 'neurological', 'developmental',
                        'general'
                      )),
  description         TEXT,
  parent_code         TEXT REFERENCES "base_taxonomy_identity"(identity_code),
  is_compound         INTEGER DEFAULT 0 CHECK(is_compound IN (0,1)),
  status              TEXT DEFAULT 'active' CHECK(status IN ('active', 'deprecated')),
  created_at          TEXT,
  updated_at          TEXT
)
```

### `base_taxonomy_medical` — base, 0 rows

```sql
CREATE TABLE base_taxonomy_medical (
  medical_code        TEXT PRIMARY KEY,
  display_name        TEXT NOT NULL,
  description         TEXT,
  status              TEXT NOT NULL DEFAULT 'active'
                        CHECK(status IN ('active','deprecated','superseded')),
  notes               TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT
, icd11_anchors TEXT, icd11_verified_at TEXT)
```

### `icf_medical_map` — base, 0 rows

```sql
CREATE TABLE "icf_medical_map" (
  icf_code           TEXT NOT NULL REFERENCES base_icf(icf_code),
  medical_code       TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  role               TEXT NOT NULL CHECK (role IN ('PRIMARY','SECONDARY','SITUATIONAL')),
  mapping_confidence TEXT NOT NULL
                       CHECK (mapping_confidence IN ('high_predictive','moderate','low','minimal')),
  notes               TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (icf_code, medical_code)
)
```

### `identity_icf_map` — base, 61 rows

```sql
CREATE TABLE "identity_icf_map" (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_code     TEXT NOT NULL REFERENCES "base_taxonomy_identity"(identity_code),
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
    UNIQUE (identity_code, icf_code, mechanism)
)
```

### `identity_medical_map` — base, 0 rows

```sql
CREATE TABLE identity_medical_map (
  identity_code      TEXT NOT NULL REFERENCES "base_taxonomy_identity"(identity_code),
  medical_code       TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  -- 'names'          -- same subject under a clinical name
  -- 'member_of'      -- the identity row is a ratified umbrella containing this diagnosis
  -- 'identity_first' -- the community does not describe itself by this diagnosis; the
  --                     crossing is navigation ONLY, and populations.display_name is what
  --                     renders. functional-taxonomy §3.3: identity profiles carry no ICD
  --                     anchor -- still true, because the anchor lives on the medical row.
  relationship       TEXT NOT NULL CHECK (relationship IN ('names','member_of','identity_first')),
  notes               TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (identity_code, medical_code)
)
```

### `lang_jur_map` — base, 70 rows

```sql
CREATE TABLE "lang_jur_map" (
    language            TEXT NOT NULL,
    jurisdiction        TEXT NOT NULL,
    role                TEXT NOT NULL
                        CHECK (role IN ('PRIMARY', 'SECONDARY')),
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT, scope_status TEXT
    CHECK (scope_status IS NULL OR scope_status IN ('in-scope', 'scoped-out')),
    PRIMARY KEY (language, jurisdiction)
)
```

### `life_stage_modifiers` — base, 2 rows

```sql
CREATE TABLE life_stage_modifiers (
  code TEXT PRIMARY KEY CHECK (code IN ('SEN','CHD')),
  label TEXT NOT NULL,
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
)
```

### `parameter_declinations` — base, 1 rows

```sql
CREATE TABLE parameter_declinations (
    term_id            TEXT PRIMARY KEY REFERENCES terms(term_id),
    reason             TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL
, revoked_at TEXT, revoked_by_session TEXT, revocation_reason TEXT
    CHECK ((revoked_at IS NULL AND revoked_by_session IS NULL AND revocation_reason IS NULL)
        OR (revoked_at IS NOT NULL AND revoked_by_session IS NOT NULL
            AND revocation_reason IS NOT NULL AND length(trim(revocation_reason)) > 0)))
```

### `rooms` — base, 17 rows

```sql
CREATE TABLE rooms (
  room_code           TEXT PRIMARY KEY,
  name                TEXT NOT NULL,
  category            TEXT,
  description         TEXT,
  status              TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active','draft','retired')),
  notes               TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT,
  updated_at          TEXT,
  updated_by_session  TEXT
)
```

### `slugs` — base, 106 rows

```sql
CREATE TABLE "slugs" (
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
)
```

### `term_aliases` — base, 2382 rows

```sql
CREATE TABLE term_aliases (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,
    language            TEXT NOT NULL DEFAULT 'EN',
    alias_type          TEXT NOT NULL
                        CHECK(alias_type IN (
                            'SYNONYM','TRANSLATION','NARROWER',
                            'BROADER','DEPRECATED','DOMAIN'
                        )),
    jurisdiction        TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL, observation_id INTEGER REFERENCES observed_terms(observation_id),
    PRIMARY KEY (term_id, alias, language)
)
```

### `terms` — base, 94 rows

```sql
CREATE TABLE terms (
    term_id             TEXT PRIMARY KEY,
    canonical_en        TEXT NOT NULL,
    definition          TEXT,
    domain              TEXT,
    scope_note          TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
, catalogue TEXT
    CHECK (catalogue IN ('references/standards-registry.md', 'references/tier456-verified-sources.json', 'references/co1-verified-sources.json', 'references/co2-verified-sources.json', '_archived/data/corpus-pre-reset-2026-08-06.db')), catalogue_entry_ref TEXT, catalogue_approval_ref TEXT
    CHECK ((catalogue IS NULL AND catalogue_entry_ref IS NULL AND catalogue_approval_ref IS NULL)
        OR (catalogue IS NOT NULL
            AND catalogue_entry_ref IS NOT NULL AND length(trim(catalogue_entry_ref)) > 0
            AND catalogue_approval_ref IS NOT NULL AND length(trim(catalogue_approval_ref)) > 0)))
```

### `citation_mining` — research, 38 rows

```sql
CREATE TABLE "citation_mining" (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    global_ref_id       TEXT,
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    -- WAS: TEXT NOT NULL DEFAULT '[]'. Relaxed so a retired writer can leave it NULL
    -- instead of taking the old default and being misread as "found nothing". See
    -- header. The writer that stops setting it is scripts/db.py:log_mining.
    connections_produced TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    deferred_reason     TEXT,
    PRIMARY KEY (slug, local_ref_id)
)
```

### `gap_mining` — research, 0 rows

```sql
CREATE TABLE gap_mining (
    gap_mining_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    gap_id               TEXT NOT NULL REFERENCES gaps(gap_id),

    -- Provenance
    created_at           TEXT NOT NULL,
    created_by_session TEXT NOT NULL,

    -- Search strategy record (replayable). JSON:
    --   {"strategies": [{"tool":"pubmed","query":"...","date_filter":"...",
    --                    "tier_filter":"...","connectors_used":["pubmed",...],
    --                    "candidates_returned":N}, ...]}
    search_strategy_record TEXT NOT NULL,
    candidates_returned    INTEGER NOT NULL DEFAULT 0,
    candidates_reviewed    INTEGER NOT NULL DEFAULT 0,

    -- Outcome enum
    outcome              TEXT NOT NULL CHECK(outcome IN (
        'closure_evidence_found',  -- enough to close the gap (rule #7 must fire)
        'partial_evidence_found',  -- some discoveries; gap stays OPEN with annotation
        'null_result',             -- searches ran clean, no relevant discoveries
        'gap_recategorized',       -- gap not mining-addressable after all
        'deferred'                 -- connectors unavailable / other blocker
    )),

    -- Discoveries: JSON array of evidence_sources.ref_id values written to
    -- evidence_sources + source_slug_links as part of THIS attempt.
    -- NULL or '[]' permitted for null_result / deferred / gap_recategorized.
    discoveries_logged   TEXT,

    -- Rule #10 gate: candidates returned but not yet verified are recorded
    -- as DOIs only, NOT INSERTed to evidence_sources. The next session may
    -- verify and promote them. Mirrors supersession_check.superseding_dois.
    candidate_dois       TEXT,  -- JSON array

    -- Method used. Composite is the cluster-search pattern (skills/
    -- supersession-audit_SKILL.md §3) — 3-6 queries per gap, evaluated
    -- as a single attempt rather than per-query.
    check_method         TEXT NOT NULL CHECK(check_method IN (
        'pubmed_cluster',
        'scholar_gateway_lived_experience',
        'cochrane_direct',
        'standards_body_direct',
        'multilingual_research',
        'composite'
    )),

    notes                TEXT,

    -- Integrity: closure_evidence_found must have at least one discovery
    CHECK (
        outcome != 'closure_evidence_found'
        OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]')
    ),

    -- Integrity: gap_recategorized must document why (>=20 chars)
    CHECK (
        outcome != 'gap_recategorized'
        OR (notes IS NOT NULL AND length(notes) >= 20)
    ),

    -- Integrity: deferred must document the blocker (>=10 chars)
    CHECK (
        outcome != 'deferred'
        OR (notes IS NOT NULL AND length(notes) >= 10)
    )
)
```

### `research_code_leads` — research, 96 rows

```sql
CREATE TABLE research_code_leads (
    lead_id             INTEGER PRIMARY KEY,

    -- The two facts that survived the REFERENCE-ONLY ruling. Both mandatory: a lead that
    -- cannot say which jurisdiction it belongs to is not retrievable, and that is the
    -- whole purpose of the row.
    jurisdiction        TEXT NOT NULL,
    standard_name       TEXT NOT NULL,

    -- The locator R3 asks of a code value: "clause/section/page". NULL until someone
    -- actually retrieves the document — which is the work this table exists to queue.
    clause              TEXT,

    status              TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                        CHECK (status IN ('REFERENCE-ONLY', 'RETRIEVED', 'SUPERSEDED')),

    recovered_from      TEXT,
    notes               TEXT,

    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,

    -- The dedup the old shape could not express: 109 rows were 83 leads because the same
    -- standard was restated per item. Keyed on the lead itself, that restatement is
    -- impossible rather than merely discouraged.
    UNIQUE (jurisdiction, standard_name)
)
```

### `search_admissions` — research, 61 rows

```sql
CREATE TABLE search_admissions (
  exec_id             INTEGER NOT NULL REFERENCES search_executions(exec_id),
  ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  created_at          TEXT,
  created_by_session  TEXT,
  PRIMARY KEY (exec_id, ref_id)
)
```

### `search_candidates` — research, 155 rows

```sql
CREATE TABLE "search_candidates" (
  candidate_id     INTEGER PRIMARY KEY,
  exec_id          INTEGER REFERENCES search_executions(exec_id),  -- which search surfaced it
  found_under_slug TEXT REFERENCES slugs(slug),  -- the slug being searched when it surfaced
  suggested_slug   TEXT REFERENCES slugs(slug),  -- best-fit slug; NULL = MISCELLANEOUS / undecided
  disposition      TEXT NOT NULL CHECK (disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED',
                      'EXHAUSTED')),
  title            TEXT NOT NULL,
  locator          TEXT,                 -- DOI / URL / PMID as retrieved
  locator_status   TEXT CHECK (locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')),
  tier_guess       INTEGER CHECK (tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6),
  harm_finding     INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),
  why_not_admitted TEXT,                 -- required in practice: metadata gap, unverified, etc.
  notes            TEXT,
  created_by_session          TEXT NOT NULL,
  created_at       TEXT NOT NULL
, resolved_ref_id TEXT REFERENCES evidence_sources(ref_id), surfaced_in TEXT, surfaced_quote TEXT, updated_at TEXT, updated_by_session TEXT) STRICT
```

### `search_execution_artefacts` — research, 117 rows

```sql
CREATE TABLE search_execution_artefacts (
  exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
  artefact           TEXT NOT NULL,   -- retrieval-log/<session stem>/<file>: a POINTER into Layer 4
  created_by_session TEXT NOT NULL,
  created_at         TEXT NOT NULL,
  PRIMARY KEY (exec_id, artefact)
) STRICT
```

### `search_executions` — research, 203 rows

```sql
CREATE TABLE "search_executions" (
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
  REFERENCES adversarial_passes(pass_id) CHECK (origin_pass_id IS NULL OR origin = 'adversarial-pass'), updated_at TEXT, updated_by_session TEXT, identity_code TEXT REFERENCES "base_taxonomy_identity"(identity_code), icf_code TEXT REFERENCES base_icf(icf_code), needs_code TEXT REFERENCES access_needs(need_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code), absence_class TEXT
  CHECK (absence_class IS NULL OR absence_class IN ('query_shape_failure', 'wrong_index', 'genuine_absence'))
  CHECK (absence_class IS NULL OR results_found = 0),        -- explicit ISO ts (deterministic under rebuild)
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids)),
  CHECK (COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL)   -- a search says what it is for (R43)
) STRICT
```

### `source_locators` — research, 893 rows

```sql
CREATE TABLE "source_locators" (
    ref_id                  TEXT PRIMARY KEY,
    doi                     TEXT,
    url                     TEXT,
    pmid                    TEXT,
    pmcid                   TEXT,
    isbn                    TEXT,
    issn                    TEXT,
    standard_number         TEXT,
    -- Mirrors evidence_sources.doi_resolution_outcome as migration 091 declared it. The two
    -- columns are one vocabulary and must not drift apart; dbcore.check_values() reads this
    -- CHECK, so db.py's argparse, --help and amend-source all arm themselves from here.
    doi_resolution_outcome  TEXT
                            CHECK (doi_resolution_outcome IS NULL
                                   OR doi_resolution_outcome IN
                                      ('RESOLVED', 'NO-MATCH', 'REVERTED')),
    url_resolution_outcome  TEXT
                            CHECK (url_resolution_outcome IS NULL
                                   OR url_resolution_outcome IN
                                      ('MATCHED', 'PARTIAL', 'NO-MATCH', 'DEAD-LINK', 'DEAD-DNS',
                                       'WAYBACK-MATCH', 'WAYBACK-PARTIAL', 'URL-NO-MATCH',
                                       'RESOLVED', 'DEAD', 'RESOLVED-PARTIAL')),
    url_last_fetched        TEXT,
    recovered_from          TEXT NOT NULL DEFAULT 'corpus-pre-reset-2026-08-06',
    authors                 TEXT,
    pub_year                TEXT,
    title                   TEXT,
    tier_claimed            TEXT,
    jurisdiction            TEXT,
    used_in_bpcs            TEXT,
    status                  TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                            CHECK (status IN ('REFERENCE-ONLY','PROMOTED',
                                              'SCREENED-OUT','RETIRED')),
    screened_reason         TEXT,
    created_by_session       TEXT,
    created_at               TEXT,
    notes                   TEXT,
    CHECK (doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL OR title IS NOT NULL),
    -- A screened-out lead states WHY. Structural, not a convention a writer may forget.
    CHECK (status <> 'SCREENED-OUT'
           OR (screened_reason IS NOT NULL AND TRIM(screened_reason) <> ''))
)
```

### `case_studies` — evidence, 0 rows

```sql
CREATE TABLE "case_studies" (
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
, design_intent TEXT, populations_served_note TEXT, outcome_data TEXT, conflict_documented TEXT, failure_notes TEXT, construction_cost TEXT, accessible_design_premium TEXT, funding_sources TEXT, operational_cost_change TEXT, remediation_cost TEXT, roi_data TEXT, financial_evidence_tier INTEGER, financial_data_quality TEXT, evidence_contribution TEXT, part13_status TEXT, sources TEXT) STRICT
```

### `economics_entries` — evidence, 1 rows

```sql
CREATE TABLE economics_entries (
  entry_id        TEXT PRIMARY KEY,            -- ECON-NNNN / HO-NNN / CP-NNN
  pillar          TEXT NOT NULL CHECK (pillar IN ('health','inaction','construction','market')),
  entry_type      TEXT NOT NULL CHECK (entry_type IN
                    ('cost_premium','retrofit_multiplier','grant_programme','health_outcome',
                     'market_value','housing_deficit','research_gap')),
  source          TEXT NOT NULL,               -- citation reference (REF-ID where available)
  ref_id          TEXT REFERENCES evidence_sources(ref_id),  -- structured link when admitted
  jurisdiction    TEXT,                        -- ISO code or 'MULTI'
  finding         TEXT NOT NULL,
  study_design    TEXT,
  sample          TEXT,
  value_numeric   REAL,
  value_unit      TEXT,                        -- '%','currency','ratio','years'
  currency        TEXT,                        -- ISO currency code
  bcr             TEXT,                        -- benefit-cost ratio
  evidence_tier   INTEGER CHECK (evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6),
  confidence      TEXT CHECK (confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW')),
  source_section  TEXT,                        -- clause/section/page for coded or statutory values
  quant_status    TEXT CHECK (quant_status IS NULL OR quant_status IN
                    ('VERIFIED-QUANT','UNVERIFIED-QUANT')),  -- CLAUDE.md §6 discipline
  year            INTEGER,
  journal         TEXT,
  status          TEXT NOT NULL DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL,
  created_by_session TEXT NOT NULL,
  updated_at      TEXT,
  updated_by_session TEXT
) STRICT
```

### `evidence_source_authors` — evidence, 142 rows

```sql
CREATE TABLE "evidence_source_authors" (
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
        created_by_session  TEXT, corporate_name_note TEXT,
        UNIQUE(ref_id, position, role)
    )
```

### `evidence_sources` — evidence, 59 rows

```sql
CREATE TABLE "evidence_sources" (
        ref_id                      TEXT PRIMARY KEY,
        source_type                 TEXT CHECK (source_type IS NULL OR source_type IN (
                                   'journal_article',
                                   'book',
                                   'book_chapter',
                                   'conference_paper',
                                   'thesis',
                                   'primary_research',
                                   'case_study',
                                   'standard',
                                   'guideline',
                                   'report',
                                   'grey',
                                   'internal',
                                   'letter',
                                   'editorial',
                                   'commentary',
                                   'other',
                                   'code'
                                 )),
        -- Author summary (denorm)
        author_count                INTEGER,
        author_count_is_complete    INTEGER DEFAULT 0,
        first_author_last           TEXT,
        first_author_first          TEXT,
        is_corporate_primary        INTEGER DEFAULT 0,
        author_display              TEXT,
        -- Date
        pub_year                    INTEGER,
        pub_year_note               TEXT,
        -- Title
        pub_title                   TEXT,
        pub_subtitle                TEXT,
        chapter_title               TEXT,
        original_title              TEXT,
        -- Language
        lang_detected               TEXT,
        lang_detection_method       TEXT,
        pub_title_en                TEXT,
        pub_subtitle_en             TEXT,
        chapter_title_en            TEXT,
        journal_name_en             TEXT,
        translation_method          TEXT,
        translation_reviewed        INTEGER DEFAULT 0,
        -- Journal
        journal_name                TEXT,
        journal_abbrev              TEXT,
        volume                      TEXT,
        issue                       TEXT,
        pages_start                 TEXT,
        pages_end                   TEXT,
        article_number              TEXT,
        -- Book/Report
        publisher                   TEXT,
        publisher_location          TEXT,
        edition                     TEXT,
        book_title                  TEXT,
        series                      TEXT,
        series_number               TEXT,
        report_number               TEXT,
        institution                 TEXT,
        -- Standard
        standard_number             TEXT,
        -- Identifiers
        doi                         TEXT,
        pmid                        TEXT,
        pmcid                       TEXT,
        isbn                        TEXT,
        issn                        TEXT,
        url                         TEXT,
        url_accessed                TEXT,
        handle                      TEXT,
        local_id                    TEXT,
        -- Evidence classification
        tier                        INTEGER,
        evidence_type               TEXT,
        jurisdiction                TEXT,
        co1_provenance              TEXT,
        co1_source_type             TEXT,
        synthesis_attribution_required INTEGER,
        -- Quality
        metadata_quality TEXT CHECK (metadata_quality IS NULL OR metadata_quality IN ('COMPLETE', 'AUTHOR-TITLE-ONLY', 'GREY', 'PMID-ONLY', 'NULL', 'COMPLETE-STATUTORY')),
        verification_status TEXT CHECK (verification_status IS NULL OR verification_status IN ('VERIFIED', 'UNVERIFIED')),
        doi_resolution_outcome TEXT CHECK (doi_resolution_outcome IS NULL OR doi_resolution_outcome IN ('RESOLVED', 'NO-MATCH', 'REVERTED')),
        bpc_shorthand               TEXT,
        bpc_note                    TEXT,
        grey_flag                   INTEGER DEFAULT 0,
        grey_reason                 TEXT,
        verification_note           TEXT,
        prior_expectation           TEXT,
        search_queries_used         TEXT,
        derivation_chain            TEXT,
        -- Notes / Audit
        notes                       TEXT,
        created_at                  TEXT,
        created_by_session          TEXT,
        updated_at                  TEXT,
        updated_by_session          TEXT
    , verified_by_tool TEXT, last_verified_at TEXT, verification_attempt_count INTEGER DEFAULT 0, superseded_by_ref_id TEXT, pages TEXT, pub_month INTEGER, language TEXT, subtype TEXT, citation_count INTEGER, url_resolution_outcome TEXT CHECK (url_resolution_outcome IS NULL OR url_resolution_outcome IN ('MATCHED', 'PARTIAL', 'NO-MATCH', 'DEAD-LINK', 'DEAD-DNS', 'WAYBACK-MATCH', 'WAYBACK-PARTIAL', 'URL-NO-MATCH', 'RESOLVED', 'DEAD', 'RESOLVED-PARTIAL')), url_last_fetched TEXT, url_match_similarity REAL, metadata_integrity_status TEXT, metadata_integrity_detail TEXT, code_currency_status TEXT, code_currency_verified_at TEXT, code_currency_verified_by_session TEXT, code_currency_notes TEXT, scope TEXT
  CHECK (scope IS NULL OR scope IN (
    'high_control', 'lower_control', 'national', 'international', 'intrinsic'
  )), data_capture_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (data_capture_status IN ('pending','captured','none-extractable','deferred')), citation_mining_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (citation_mining_status IN ('pending','mined','deferred','not-applicable')), processing_blocked_reason TEXT
  CHECK (processing_blocked_reason IS NULL OR processing_blocked_reason IN (
    'no-full-text',        -- full text could not be obtained
    'paywalled',           -- access blocked by paywall
    'no-doi',              -- no resolvable identifier for automated paths
    'not-indexed',         -- absent from the indexes the pipeline queries
    'language',            -- awaiting in-language reading capacity
    'no-quantified-claims',-- read; carries no extractable value
    'superseded',          -- superseded by another source
    'out-of-scope',        -- outside the corpus this project extracts from
    'tier-not-required'    -- tier does not oblige the work
  )), standard_number_note TEXT, author_display_note  TEXT, publisher_note       TEXT, verification_disposition TEXT
  CHECK (verification_disposition IS NULL
         OR verification_disposition IN ('OPEN','CLOSED')), verification_method TEXT
  CHECK (verification_method IS NULL OR verification_method IN (
    'direct-render',              -- the document was fetched and read
    'co1-attestation',            -- the attestation itself was obtained (DR 3.1)
    'corroborated-not-retrieved', -- >=2 independent retrievals agree; doc not obtained
    'citing-bibliography',        -- existence attested only by another work's references
    'tool'                        -- resolve_dois / verify_urls; verified_by_tool names which
  )), verification_closure_reason TEXT
  CHECK (verification_closure_reason IS NULL OR verification_closure_reason IN (
    'paywalled',
    'print-only',
    'access-denied-persistent',
    'withdrawn',
    'not-found-after-search',
    'disputed-existence'          -- owner ruling: there may be no resolution
  )))
```

### `external_root_registry` — evidence, 0 rows

```sql
CREATE TABLE external_root_registry (
    root_id             TEXT PRIMARY KEY,
    description         TEXT NOT NULL,
    root_type           TEXT
                          CHECK (root_type IN (
                              'measurement_primary', 'participatory_finding',
                              'committee_assertion', 'derived_calculation',
                              'untraced')),
    provenance          TEXT,
    root_population_note TEXT,
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT
)
```

### `observed_terms` — evidence, 96 rows

```sql
CREATE TABLE "observed_terms" (
    observation_id      INTEGER PRIMARY KEY,
    -- POINTER, not a copy. The source's bibliography stays in evidence_sources.
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    -- The phrase EXACTLY as the source writes it. Not normalised, not translated,
    -- not mapped. R11 forbids back-translation and this is where that starts.
    surface_form        TEXT NOT NULL,
    -- The language the phrase APPEARS IN, which need not be the source's language.
    language            TEXT NOT NULL DEFAULT 'EN',
    -- R3's locator discipline: where in the source it appears. Part of the sighting's
    -- key since migration 102 (ux_observed_terms_sighting below).
    locator             TEXT,
    -- Enough surrounding text that judgment can adjudicate without re-retrieving.
    context_quote       TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT
)
```

### `source_scans` — evidence, 18 rows

```sql
CREATE TABLE source_scans (
    -- AUTOINCREMENT, as 076 did for the other ids a record names: a scan_id is cited by
    -- session records and must never come to mean a different reading.
    scan_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id              TEXT    NOT NULL REFERENCES evidence_sources(ref_id),
    -- catalogue: every active parameter up to catalogue_version.
    -- targeted:  one parameter, target_parameter_id (a back-fill reading).
    mode                TEXT    NOT NULL CHECK (mode IN ('catalogue', 'targeted')),
    catalogue_version   INTEGER NOT NULL CHECK (catalogue_version >= 1),
    target_parameter_id INTEGER REFERENCES base_parameters(parameter_id),
    -- full: the whole document. partial: some pages of it. fragment: one page or clause
    -- of a larger instrument. abstract: an abstract or metadata record only.
    text_scope          TEXT    NOT NULL CHECK (text_scope IN
                                ('full', 'partial', 'fragment', 'abstract')),
    pages_read          INTEGER CHECK (pages_read IS NULL OR pages_read >= 0),
    pages_total         INTEGER CHECK (pages_total IS NULL OR pages_total >= 1),
    -- Which saved file was read, by checksum: the manifest's own sha256 of the bytes.
    file_sha256         TEXT    NOT NULL CHECK (length(file_sha256) = 64),
    -- Whether the open pass (quantities the catalogue lacks, plan section 3.4) was done
    -- in this reading.
    open_pass_done      INTEGER NOT NULL DEFAULT 0 CHECK (open_pass_done IN (0, 1)),
    -- full-read: the text was read against the list. pre-screen: only a script listed
    -- where catalogue terms occur -- weaker, and v_scan_ledger says which it was.
    method              TEXT    NOT NULL CHECK (method IN ('full-read', 'pre-screen')),
    notes               TEXT,
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    CHECK ((mode = 'targeted' AND target_parameter_id IS NOT NULL)
        OR (mode = 'catalogue' AND target_parameter_id IS NULL)),
    CHECK (pages_read IS NULL OR pages_total IS NULL OR pages_read <= pages_total),
    -- "full" over a paged text means every page; a reading of fewer pages is partial.
    CHECK (text_scope <> 'full' OR pages_read IS NULL OR pages_read = pages_total)
)
```

### `source_slug_links` — evidence, 71 rows

```sql
CREATE TABLE "source_slug_links" (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL, relevance_note TEXT,
    PRIMARY KEY (ref_id, slug)
)
```

### `evidence_population_match` — judgment, 61 rows

```sql
CREATE TABLE "evidence_population_match" (
    match_id            TEXT PRIMARY KEY,
    source_ref          TEXT NOT NULL,
    target_population   TEXT NOT NULL,
    study_population    TEXT,
    sample_size         INTEGER,
    match_grade         TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note       TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    gap_id              TEXT REFERENCES gaps(gap_id)
)
```

### `extraction_follow_ups` — judgment, 0 rows

```sql
CREATE TABLE extraction_follow_ups (
    follow_up_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    reason              TEXT    NOT NULL CHECK (reason IN ('read-outside-admitting-purpose')),
    warrant             TEXT    NOT NULL CHECK (length(trim(warrant)) > 0),
    raised_at           TEXT    NOT NULL,
    raised_by_session   TEXT    NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution          TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL AND resolution IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution IS NOT NULL AND length(trim(resolution)) > 0))
)
```

### `extraction_relations` — judgment, 57 rows

```sql
CREATE TABLE extraction_relations (
  relation_id         INTEGER PRIMARY KEY AUTOINCREMENT,

  -- THE FIGURE THIS EDGE QUALIFIES. NOT NULL and a real FK -- an edge naming no source
  -- row describes nothing. No UNIQUE index touches this column alone: one extraction may
  -- carry several comparator edges (a ramp slope is both condition_on a run-length limit
  -- AND audited_against a code's stated maximum), and collapsing that to one row per
  -- extraction would force a choice this table exists to avoid forcing.
  from_extraction_id  INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),

  -- WHAT KIND OF COMPARISON THIS EDGE IS. Eight values; the CHECK is the vocabulary
  -- (CLAUDE.md section 4) and this is only its meaning, one line each.
  --   tested_at        -- the source physically measured its subjects at/against this
  --                      referent -- REF-00973's four ramp slopes were each tested_at a
  --                      named gradient.
  --   audited_against  -- the source measured whether subjects could perform WITHIN a
  --                      referent's own stated limit, rather than measuring an
  --                      independent value -- REF-00971's "existing standards".
  --   confirms         -- an independent measurement agrees with the referent's value.
  --   insufficient     -- the source asserts the referent's value is NOT ENOUGH for the
  --                      population or task in question -- REF-00784's 10-100% figure.
  --   exceeds          -- the source asserts the referent's value is more than needed.
  --   delta_over       -- the source states an increment relative to a baseline rather
  --                      than an absolute figure -- REF-00976's "more than thirty
  --                      centimetres of enlargement over the surveyed stock".
  --   condition_on     -- this figure only holds given a second figure this project also
  --                      holds as a row -- a slope given its run-length limit.
  --   derived_from     -- this figure is computed from the referent, never read off a
  --                      source -- always paired with input_role below and always a row
  --                      referent, never a label; see the CHECK immediately following.
  relation            TEXT NOT NULL CHECK (relation IN (
                        'tested_at', 'audited_against', 'confirms', 'insufficient',
                        'exceeds', 'delta_over', 'condition_on', 'derived_from')),

  -- THE REFERENT, HALF A: a row this project already holds. Nullable -- see to_label.
  -- Self-joins to the same table this column sits on, which is why the identity CHECK
  -- below refuses an edge from a row to itself.
  to_extraction_id    INTEGER REFERENCES source_value_extractions(extraction_id),

  -- THE REFERENT, HALF B: prose naming what to_extraction_id would otherwise point at,
  -- for a referent this project has not captured as its own row -- a code clause never
  -- extracted on its own parameter, a source's private baseline sample, or a referent the
  -- source itself never names. Exactly one of this column and to_extraction_id is set on
  -- every row; the CHECK enforcing that sits with the rest below, not here, because it
  -- names both columns together.
  to_label            TEXT,

  -- WHAT SORT OF THING to_label NAMES, when it is set. Meaningless and left NULL when
  -- the referent is a row instead -- a row already carries this information in its own
  -- data.
  --   standard      -- a code, guideline or published standard's own stated figure.
  --   own_sample    -- the source's own baseline measurement of its own subjects or
  --                   stock, as in REF-00976's surveyed housing.
  --   prior_source  -- an earlier study or publication, distinct from a code and from the
  --                   citing source's own sample.
  --   unnamed       -- the source itself does not say what the referent is. See the
  --                   `stated` column: this value and 'unnamed' there always travel
  --                   together, by CHECK.
  to_kind             TEXT CHECK (to_kind IS NULL OR to_kind IN (
                        'standard', 'own_sample', 'prior_source', 'unnamed')),

  -- HOW EXPLICITLY THE SOURCE ITSELF NAMES THE REFERENT -- independent of whether this
  -- project could resolve it to a row. NOT NULL: every edge takes a position on this.
  --   named     -- the source identifies the referent by name (a code number, an author,
  --              a described sample).
  --   unnamed   -- the source gestures at a referent ("existing standards") without
  --              naming which one. Never a row referent -- see the CHECK below; naming
  --              nothing is not the same claim as naming a specific row.
  --   inferred  -- the source names no referent at all and this project supplied one from
  --              context (a code the jurisdiction and date make unambiguous). The
  --              weakest of the three and the one most likely to need revisiting.
  stated              TEXT NOT NULL CHECK (stated IN ('named', 'unnamed', 'inferred')),

  -- WHICH SIDE OF A DERIVATION this edge supplies. Meaningful only for relation =
  -- 'derived_from', enforced by CHECK -- every other relation leaves it NULL.
  --   base    -- the starting figure the derived value is computed from.
  --   delta   -- the increment added to (or subtracted from) the base.
  --   factor  -- a multiplier applied to the base, for a derivation `v_derived_figure_check`
  --            does not itself recompute -- that view covers base+delta only; a
  --            factor-based derivation is a known residual, not a silent gap, recorded
  --            here rather than built speculatively (CLAUDE.md section 8).
  input_role          TEXT CHECK (input_role IS NULL OR input_role IN ('base', 'delta', 'factor')),

  -- THE SOURCE'S OWN WORDS FOR THE COMPARISON, NOT NULL. Mirrors the verbatim discipline
  -- `observed_terms.context_quote` and `db.py add-extraction`'s required `--claim-text`
  -- already carry on this project's other judgment-stage rows: a comparator asserted with
  -- nothing of the source's own phrasing behind it is not a comparator this project has
  -- actually read.
  quote               TEXT NOT NULL,

  notes               TEXT,

  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,

  -- An edge cannot compare a figure to itself.
  CHECK (to_extraction_id IS NULL OR to_extraction_id <> from_extraction_id),

  -- The referent is named as a row or as a label; never as both at once and never as
  -- neither, or the edge would point at two things or at nothing.
  CHECK ((to_extraction_id IS NULL) <> (to_label IS NULL)),

  -- You cannot be conditioned by, or computed from, a figure that does not exist as a
  -- row: condition_on and derived_from both require a resolvable to_extraction_id.
  CHECK (relation NOT IN ('condition_on', 'derived_from') OR to_extraction_id IS NOT NULL),

  -- input_role names which side of a derivation this edge is, so it is meaningless
  -- outside relation = 'derived_from' and mandatory inside it.
  CHECK (
    (relation = 'derived_from' AND input_role IS NOT NULL)
    OR (relation <> 'derived_from' AND input_role IS NULL)
  ),

  -- An unnamed referent cannot simultaneously be one specific known row: if the source
  -- does not say what it is, this project cannot have resolved it to a row either.
  CHECK (stated <> 'unnamed' OR to_extraction_id IS NULL),

  -- Calling the referent's kind 'unnamed' is a claim about how the source stated it, so
  -- it must agree with the stated column rather than disagree with it.
  CHECK (to_kind IS NULL OR to_kind <> 'unnamed' OR stated = 'unnamed')
)
```

### `source_value_extractions` — judgment, 214 rows

```sql
CREATE TABLE "source_value_extractions" (
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
  identity_code          TEXT REFERENCES "base_taxonomy_identity"(identity_code),
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
  CHECK (harm_finding = 0 OR figure_role = 'finding'),

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
)
```

### `term_adjudications` — judgment, 90 rows

```sql
CREATE TABLE term_adjudications (
    adjudication_id     INTEGER PRIMARY KEY,
    observation_id      INTEGER NOT NULL REFERENCES observed_terms(observation_id),
    -- OUTCOMES, documented HERE and not inside the CHECK. dbcore.check_values() reads
    -- this constraint's own value list to build the CLI's refusal, and an inline
    -- comment between the quoted values defeats its parser -- measured 2026-09-03,
    -- when a first cut of this migration carried the descriptions inside the IN(...)
    -- and every legitimate outcome was refused with a mangled vocabulary. The whole
    -- reason vocabularies come from the schema rather than a list in the code
    -- (CLAUDE.md §4) is defeated by punctuation the parser cannot see past.
    --
    --   NAMES-EXISTING  names a term we already hold
    --   NAMES-NEW       names a concept new to the vocabulary
    --   NOT-OURS        a real phrase, but not one of our concepts
    --   DEFERRED        cannot be settled on this source alone
    outcome             TEXT NOT NULL CHECK (outcome IN
                            ('NAMES-EXISTING','NAMES-NEW','NOT-OURS','DEFERRED')),
    term_id             TEXT REFERENCES terms(term_id),
    -- NOT NULL: an adjudication that does not say why cannot be contested, and the
    -- whole point of splitting observation from judgment is that the judgement is
    -- inspectable.
    rationale           TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    -- The outcome and the pointer must agree. An outcome that names a term must name
    -- one; an outcome that declines must not.
    CHECK (
        (outcome IN ('NAMES-EXISTING','NAMES-NEW') AND term_id IS NOT NULL)
     OR (outcome IN ('NOT-OURS','DEFERRED')        AND term_id IS NULL)
    )
)
```

### `conflicts` — synthesis, 0 rows

```sql
CREATE TABLE conflicts (
    conflict_id         TEXT PRIMARY KEY,
    domain              TEXT NOT NULL,
    pop_a               TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    pop_b               TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
                        )),
    resolution          TEXT,
    evidence            TEXT,
    gap_id              TEXT REFERENCES gaps(gap_id),
    source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL, parameter_id INTEGER REFERENCES base_parameters(parameter_id),
    CHECK (pop_a < pop_b)
)
```

### `connection_targets` — synthesis, 0 rows

```sql
CREATE TABLE connection_targets (
    target_id      INTEGER PRIMARY KEY,   -- a declared key: emit_batch_sql refuses to diff a table on implicit rowids
    con_id         TEXT NOT NULL REFERENCES connections(con_id),
    parameter_id   INTEGER REFERENCES base_parameters(parameter_id),
    slug           TEXT    REFERENCES slugs(slug),
    identity_code  TEXT    REFERENCES base_taxonomy_identity(identity_code),
    extraction_id  INTEGER REFERENCES source_value_extractions(extraction_id),
    methodology    TEXT,
    CHECK ((parameter_id IS NOT NULL) + (slug IS NOT NULL) + (identity_code IS NOT NULL)
           + (extraction_id IS NOT NULL) + (methodology IS NOT NULL) = 1),
    UNIQUE (con_id, parameter_id),
    UNIQUE (con_id, slug),
    UNIQUE (con_id, identity_code),
    UNIQUE (con_id, extraction_id),
    UNIQUE (con_id, methodology)
)
```

### `connections` — synthesis, 0 rows

```sql
CREATE TABLE connections (
    con_id              TEXT PRIMARY KEY,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )),
    confidence          TEXT NOT NULL
                        CHECK(confidence IN ('HIGH','MODERATE')),
    connection_type     TEXT
                        CHECK(connection_type IN (
                            'CROSS-POPULATION','CROSS-PARAMETER',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )),
    filed_in            TEXT NOT NULL REFERENCES slugs(slug),
    description         TEXT,
    source_skill        TEXT,
    opus_reviewed       INTEGER NOT NULL DEFAULT 0 CHECK(opus_reviewed IN (0,1)),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
)
```

### `convergence_assessment` — synthesis, 5 rows

```sql
CREATE TABLE convergence_assessment (
    convergence_id          INTEGER PRIMARY KEY,
    status                  TEXT NOT NULL
                            CHECK (status IN ('convergent', 'divergent',
                                              'single_axis', 'pending_assessment')),
    clinical_sources        TEXT,   -- JSON array of REF-IDs (Tier 1-3)
    co1_sources             TEXT,   -- JSON array of REF-IDs (Co-1)
    co2_sources             TEXT,   -- JSON array of REF-IDs (Co-2)
    down_weighted_sources   TEXT,   -- JSON array — directness DOWN-WEIGHTED (§1.7)
    discounted_sources      TEXT,   -- JSON array — directness DISCOUNTED/NON-ANCHORING
    rationale               TEXT,   -- required for divergent + single_axis (model)
    synthesis_approach      TEXT,   -- required for divergent (model)
    created_at              TEXT,
    created_by_session      TEXT,
    updated_at              TEXT,
    updated_by_session      TEXT
)
```

### `convergence_sources` — synthesis, 69 rows

```sql
CREATE TABLE convergence_sources (
    convergence_id  INTEGER NOT NULL
                    REFERENCES convergence_assessment(convergence_id),
    ref_id          TEXT    NOT NULL
                    REFERENCES evidence_sources(ref_id),
    -- The weighing is a property of the pairing, so it lives here. Vocabulary in the
    -- column's own CHECK, read by dbcore.check_values() rather than retyped by a caller.
    role            TEXT    NOT NULL
                    CHECK (role IN ('clinical', 'co1', 'co2',
                                    'down_weighted', 'discounted')),
    created_at          TEXT,
    created_by_session  TEXT,
    PRIMARY KEY (convergence_id, ref_id, role)
)
```

### `gaps` — synthesis, 110 rows

```sql
CREATE TABLE "gaps" (
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
    )))
```

### `reasoning_doc_citations` — synthesis, 0 rows

```sql
CREATE TABLE "reasoning_doc_citations" (
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
    created_by_session  TEXT NOT NULL,
    paywall_purchase_candidate INTEGER NOT NULL DEFAULT 0 CHECK(paywall_purchase_candidate IN (0,1)),
    notes                TEXT, setting TEXT, locator_scheme     TEXT, loc_division       TEXT, loc_part           TEXT, loc_section        TEXT, loc_subsection     TEXT, loc_paragraph      TEXT, loc_clause         TEXT, loc_subclause      TEXT, loc_division_end   TEXT, loc_part_end       TEXT, loc_section_end    TEXT, loc_subsection_end TEXT, loc_paragraph_end  TEXT, loc_clause_end     TEXT, loc_subclause_end  TEXT, loc_note           TEXT,
    CHECK (
      (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT NULL) OR
      (claim_type IN ('qualitative','definitional') AND claim_text IS NOT NULL AND claim_match IS NOT NULL)
    )
)
```

### `supersession_check` — synthesis, 0 rows

```sql
CREATE TABLE "supersession_check" (
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
    created_at           TEXT NOT NULL,
    created_by_session   TEXT NOT NULL,
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
)
```

### `determination_gates` — specification, 1 rows

```sql
CREATE TABLE determination_gates (
    gate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id        INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- The lens the finding applies to, NULL meaning every lens on this parameter. Not an
    -- FK set like specifications' four, because a gate is raised against a parameter by an
    -- audit that may not know which cells exist yet.
    identity_code       TEXT REFERENCES "base_taxonomy_identity"(identity_code),
    verdict             TEXT NOT NULL
                        CHECK (verdict IN ('UNLINKED', 'MISLINKED',
                                           'UNDER-CONSERVATIVE', 'CONTRADICTS')),
    -- The ladder-inversion guard: how strong the thing raising the gate actually is.
    trigger_ref_id      TEXT REFERENCES evidence_sources(ref_id),
    trigger_tier        INTEGER NOT NULL CHECK (trigger_tier BETWEEN 1 AND 6),
    trigger_evidence_type TEXT NOT NULL,
    detail              TEXT NOT NULL,
    raised_at           TEXT NOT NULL,
    raised_by_session   TEXT NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution_rationale TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL
            AND resolution_rationale IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution_rationale IS NOT NULL))
)
```

### `specification_extraction_links` — specification, 151 rows

```sql
CREATE TABLE specification_extraction_links (
    specification_id    INTEGER NOT NULL
                        REFERENCES specifications(specification_id),
    extraction_id       INTEGER NOT NULL
                        REFERENCES source_value_extractions(extraction_id),
    role                TEXT NOT NULL
                        CHECK (role IN ('governing', 'conditioning', 'excluded')),
    -- Why this row did not govern. Free text by design: the reasons are the engine's
    -- own vocabulary (tier non-anchoring, figure_role, superseded source) and pinning
    -- them to a CHECK here would be a second home for rules that live in assess_cell.
    exclusion_reason    TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (specification_id, extraction_id),
    -- A reason is required for an exclusion and meaningless otherwise.
    CHECK ((role =  'excluded' AND exclusion_reason IS NOT NULL)
        OR (role <> 'excluded' AND exclusion_reason IS NULL))
)
```

### `specification_source_links` — specification, 38 rows

```sql
CREATE TABLE "specification_source_links" (
  specification_id             INTEGER NOT NULL REFERENCES "specifications"(specification_id),
  ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  role                TEXT NOT NULL DEFAULT 'governing'
                        CHECK (role IN ('governing')),
  created_at          TEXT,
  created_by_session  TEXT,
  PRIMARY KEY (specification_id, ref_id)
)
```

### `specifications` — specification, 8 rows

```sql
CREATE TABLE "specifications" (
    -- AUTOINCREMENT (076): never reissue a specification_id. See the header.
    specification_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,
    -- which is why no determination could be written at all.
    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is
    -- retired in favour of these. NULL in a lens means "this determination is not
    -- stated in that lens", which is legitimate; stating several at once is the ideal.
    identity_code                   TEXT REFERENCES "base_taxonomy_identity"(identity_code),
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
            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL))), retired_at TEXT, retired_by_session TEXT, retirement_reason TEXT, superseded_by_specification_id INTEGER
    REFERENCES specifications(specification_id), rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0
  CHECK (rests_on_proxy_inference IN (0, 1)), value_notations TEXT, marker TEXT
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker = '○')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL)),
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
)
```

### `weighting_profile` — render, 5 rows

```sql
CREATE TABLE weighting_profile (
    audience        TEXT NOT NULL,
    use_pattern     TEXT NOT NULL,
    tier_weights    TEXT NOT NULL CHECK (json_valid(tier_weights)),
    notes           TEXT,
    PRIMARY KEY (audience, use_pattern)
)
```

### `adversarial_findings` — infrastructure, 193 rows

```sql
CREATE TABLE "adversarial_findings" (
  finding_id      INTEGER PRIMARY KEY,
  pass_id         INTEGER NOT NULL REFERENCES adversarial_passes(pass_id),
  lens            TEXT NOT NULL CHECK (lens IN (
                    'L1-existence','L2-fidelity','L3-independence','L4-tier','L5-population',
                    'L6-contrary','L7-recognition','L8-query-shape',
                    'S1-harm-reached-row','S2-mismatch-note-vs-payload','S3-containment',
                    'S4-sequence')),
  subject_table   TEXT,                -- loose pointer to the row attacked; never a copy of it,
                                       -- and never FK-enforced -- see header, "not Layer 1"
  subject_key     TEXT,
  claim_attacked  TEXT NOT NULL,
  method          TEXT NOT NULL,
  artefact        TEXT,                -- what the claim was attacked WITH (DR-2026-09-11 clause 2)
  verdict         TEXT NOT NULL CHECK (verdict IN
                    ('SUSTAINED','SURVIVED','NOT-ATTACKED','WITHHELD-FOR-OWNER')),
  severity        TEXT CHECK (severity IS NULL OR severity IN ('CRITICAL','HIGH','MEDIUM','LOW')),
                                       -- required iff verdict='SUSTAINED' (RULE ACTION 2)
  disposition     TEXT CHECK (disposition IS NULL OR disposition IN
                    ('REPAIRED','REJECTED','PROVISIONAL-DISPUTED','OWNER-RULED')),
  disposition_ref TEXT,                -- a data migration path; a quote-anchored ledger pointer; or the reason
  disposed_by_session TEXT,            -- NULL until disposed; set once, never overwritten (writer-enforced)
  disposed_at     TEXT,
  created_by_session TEXT NOT NULL,
  created_at      TEXT NOT NULL,
  -- The SUSTAINED<->severity pairing is a schema CHECK, not only a Python refusal, on
  -- the same precedent as `reviewer_transcript <> author_transcript` above: an invariant
  -- worth enforcing in a writer is worth enforcing for every future writer and every
  -- data migration that ever touches this table, not just the one call path that exists
  -- today. (severity IS NOT NULL) is 0/1 in SQLite, so this compares cleanly with the
  -- 0/1 of (verdict = 'SUSTAINED').
  CHECK ((verdict = 'SUSTAINED') = (severity IS NOT NULL))
) STRICT
```

### `adversarial_passes` — infrastructure, 9 rows

```sql
CREATE TABLE adversarial_passes (
  pass_id             INTEGER PRIMARY KEY,
  subject_session     TEXT NOT NULL,   -- bare stem of the batch attacked; writer strips a trailing .md
  subject_commit      TEXT NOT NULL,   -- the sha the reviewer read
  reviewer_transcript TEXT NOT NULL,   -- tracked path under transcripts/
  reviewer_models     TEXT NOT NULL CHECK (json_valid(reviewer_models) AND json_type(reviewer_models) = 'array'),
                                       -- DERIVED by the writer from the transcript; never typed
  author_transcript   TEXT NOT NULL,
  author_models       TEXT NOT NULL CHECK (json_valid(author_models) AND json_type(author_models) = 'array'),
  closed_at           TEXT,
  created_by_session  TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  CHECK (reviewer_transcript <> author_transcript)   -- a self-administered pass is not a pass
) STRICT
```

### `data_migrations` — infrastructure, 476 rows

```sql
CREATE TABLE data_migrations (
    migration_id        TEXT PRIMARY KEY,        -- e.g. "data_20260511053900_2026-05-11g-citation-mining"
    applied_at          TEXT NOT NULL,           -- ISO 8601 UTC
    content_sha         TEXT NOT NULL,           -- SHA-256 hex of the migration file body when applied
    applied_by_session  TEXT,                    -- which session ran the runner; NULL for batch reconstructions
    notes               TEXT
)
```

### `decisions` — infrastructure, 188 rows

```sql
CREATE TABLE "decisions" (
    decision_id         TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )),
    delegation          TEXT NOT NULL
                        CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')),
    delegation_rationale TEXT,
    summary             TEXT NOT NULL,
    outcome             TEXT NOT NULL,
    rationale           TEXT NOT NULL,
    decision_date       TEXT NOT NULL,
    decided_by          TEXT NOT NULL,
    model_routing       TEXT NOT NULL,
    effort_level        INTEGER NOT NULL,
    status              TEXT NOT NULL DEFAULT 'ACTIVE'
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
                        )),
    review_status       TEXT NOT NULL,
    supersedes          TEXT NOT NULL DEFAULT '[]',
    predecessors        TEXT NOT NULL DEFAULT '[]',
    decision_artifacts  TEXT NOT NULL DEFAULT '[]',
    alternatives_considered TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
)
```

### Views (verbatim)

#### `v_best_practice`

```sql
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND retired_at IS NULL
```

#### `v_code_floor_only`

```sql
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, t.canonical_en AS parameter_name
    FROM "specifications" ecs
    JOIN base_parameters bp ON bp.parameter_id = ecs.parameter_id
                            AND bp.status = 'active'
    JOIN terms t            ON t.term_id       = bp.term_id
    WHERE ecs.code_floor_only = 1
      AND ecs.retired_at IS NULL
```

#### `v_convergence_sources`

```sql
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
```

#### `v_coverage_branch`

```sql
CREATE VIEW v_coverage_branch AS
SELECT slug, jurisdiction, target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5
```

#### `v_coverage_jurisdiction`

```sql
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, jurisdiction
```

#### `v_coverage_language`

```sql
CREATE VIEW v_coverage_language AS
SELECT slug, language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, language
```

#### `v_coverage_lens`

```sql
CREATE VIEW v_coverage_lens AS
SELECT slug, parameter_id, jurisdiction, language, identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions GROUP BY 1, 2, 3, 4, 5, 6, 7, 8
```

#### `v_coverage_priority`

```sql
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
      WHERE se.slug = s.slug
        AND se.jurisdiction = ljm.jurisdiction
        AND UPPER(se.language) = ljm.language
  )
```

#### `v_derived_figure_check`

```sql
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
  AND d.claimed_unit = e.claimed_unit
```

#### `v_determination_provenance`

```sql
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
 WHERE s.retired_at IS NULL
```

#### `v_divergence`

```sql
CREATE VIEW v_divergence AS
    SELECT ecs.*, ca.status AS convergence_status, ca.rationale AS convergence_rationale,
           ca.synthesis_approach AS convergence_synthesis_approach
    FROM "specifications" ecs
    JOIN convergence_assessment ca ON ca.convergence_id = ecs.convergence_id
    WHERE ca.status = 'divergent'
      AND ecs.retired_at IS NULL
```

#### `v_evidence_authors`

```sql
CREATE VIEW v_evidence_authors AS
SELECT
  e.ref_id                                                                   AS ref_id,
  (SELECT COUNT(*) FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id)                                              AS author_count,
  (SELECT CASE WHEN a.is_corporate = 1 THEN a.corporate_name ELSE a.last_name END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS first_author_last,
  (SELECT CASE WHEN a.is_corporate = 1 THEN NULL ELSE a.first_name END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS first_author_first,
  (SELECT CASE WHEN a.is_corporate = 1 THEN 1 ELSE 0 END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS is_corporate_primary,
  (SELECT group_concat(
            CASE WHEN a.is_corporate = 1 THEN COALESCE(a.corporate_name, '')
                 ELSE TRIM(COALESCE(a.last_name, '') || ' ' ||
                           substr(COALESCE(a.first_name, ''), 1, 1)) END,
            '; ' ORDER BY a.position)
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id)                                              AS author_display
FROM evidence_sources e
```

#### `v_item_provenance`

```sql
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
  AND bp.status = 'active'
```

#### `v_open_determination_gates`

```sql
CREATE VIEW v_open_determination_gates AS
SELECT g.gate_id, g.parameter_id, g.identity_code, g.verdict,
       g.trigger_ref_id, g.trigger_tier, g.trigger_evidence_type, g.detail,
       g.raised_at, g.raised_by_session
  FROM determination_gates g
 WHERE g.resolved_at IS NULL
```

#### `v_pending`

```sql
CREATE VIEW v_pending AS
    SELECT ecs.*, g.description AS gap_description, g.category AS gap_category,
           g.priority AS gap_priority
    FROM "specifications" ecs
    JOIN gaps g ON g.gap_id = ecs.gap_register_id
    WHERE ecs.state = 'pending'
      AND ecs.retired_at IS NULL
```

#### `v_registry_duplicate_descriptions`

```sql
CREATE VIEW v_registry_duplicate_descriptions AS
    SELECT LOWER(TRIM(description)) AS normalised_description,
           COUNT(*) AS stub_count,
           GROUP_CONCAT(root_id, ', ') AS root_ids
    FROM external_root_registry
    GROUP BY LOWER(TRIM(description))
    HAVING COUNT(*) > 1
```

#### `v_research_scope`

```sql
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
 WHERE COALESCE(scope_status, 'in-scope') <> 'scoped-out'
```

#### `v_root_id_conflicts`

```sql
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
    GROUP BY root_id HAVING COUNT(DISTINCT root_ref_id) > 1
```

#### `v_scan_ledger`

```sql
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
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id
```

#### `v_source_admission`

```sql
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
JOIN search_executions se ON se.exec_id = sa.exec_id
```

#### `v_source_reach_all`

```sql
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
WHERE es.superseded_by_ref_id IS NULL
```

#### `v_unregistered_roots`

```sql
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
      AND sve.root_type NOT IN ('untraced', 'derived_calculation')
```

#### `v_value_independence`

```sql
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
    GROUP BY sve.parameter_id, t.canonical_en
```
