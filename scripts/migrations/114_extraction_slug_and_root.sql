-- 114_extraction_slug_and_root.sql
-- SCHEMA migration -- one rebuild of source_value_extractions, for two rulings (plan Phase 3 judgment).
--
--   slug     NOT NULL REFERENCES slugs(slug)  ->  nullable, and no writer sets it any more (RULINGS R37).
--            The scan contract (LED-195, LED-196, LED-201) says a slug guides what is SEARCHED, not what is read:
--            a source is read for every parameter whatever slug admitted it. Existing rows keep the slug they were
--            mined under, as history; source_slug_links stays the admission record.
--   root_id  TEXT  ->  TEXT REFERENCES external_root_registry(root_id)  (RULINGS R24).
--            root_id is registry-only; an in-corpus root is named by root_ref_id, which is how the two columns
--            already divide. No committed row carries a root_id, so the new key constrains nothing that exists.
--   idx_sve_slug_param (slug, parameter_id) is not recreated: nothing reads this table by slug, and a column that
--            is NULL from now on indexes nothing. The other four indexes are recreated verbatim.
--
-- SQLite cannot drop a NOT NULL or add a key, so the table is rebuilt by migration 081's recipe, GENERATED from the live
-- DDL with the two substitutions above rather than retyped: build under a temporary name, copy by column name, DROP the
-- old, RENAME the new (so the inbound keys from extraction_relations, specification_extraction_links and
-- extraction_follow_ups keep naming source_value_extractions), recreate the indexes, then the views from their own stored
-- SQL, verbatim. The views come down first because SQLite refuses a rename while a view is unresolvable:
-- v_root_id_conflicts, v_derived_figure_check, v_scan_ledger, v_value_independence, v_determination_provenance, v_unregistered_roots.
--
-- The table is AUTOINCREMENT. DROP TABLE takes its sqlite_sequence row, so the floor is captured first and restored as a
-- maximum afterwards (migration 076: an identifier is never reissued).
--
-- ORDER: the rebuild copies every row once, after every committed data migration has written theirs.
-- AFTER_DATA: 20261016003719

CREATE TEMP TABLE _114_seq AS SELECT name, seq FROM sqlite_sequence;

DROP VIEW "v_root_id_conflicts";
DROP VIEW "v_derived_figure_check";
DROP VIEW "v_scan_ledger";
DROP VIEW "v_value_independence";
DROP VIEW "v_determination_provenance";
DROP VIEW "v_unregistered_roots";

CREATE TABLE "_114_new_source_value_extractions" (
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
INSERT INTO "_114_new_source_value_extractions" ("extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator")
  SELECT "extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator" FROM "source_value_extractions";
DROP TABLE "source_value_extractions";
ALTER TABLE "_114_new_source_value_extractions" RENAME TO "source_value_extractions";
CREATE INDEX idx_sve_ref    ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status ON source_value_extractions(extraction_status);
CREATE INDEX ix_sve_locator ON source_value_extractions(loc_section, loc_clause);
CREATE INDEX idx_sve_param_ref ON source_value_extractions(parameter_id, ref_id);

INSERT INTO sqlite_sequence (name, seq)
  SELECT s.name, s.seq FROM _114_seq s
   WHERE s.name NOT IN (SELECT name FROM sqlite_sequence);
UPDATE sqlite_sequence SET seq = MAX(seq,
        (SELECT s.seq FROM _114_seq s WHERE s.name = sqlite_sequence.name))
  WHERE name IN (SELECT name FROM _114_seq);
DROP TABLE _114_seq;

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
--   4 READ-PARTIAL       only partial / fragment / abstract readings cover it.
--   5 NOT-READ           no reading covers it.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >=
-- parameter_id (the parameter existed when the reading was made), or targeted at that
-- parameter. Rows 1 and 2 win over readings because a row written is stronger evidence
-- than a reading recorded; 3 wins over 4 because a full reading supersedes a partial
-- one of the same source.
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id,
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
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

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

PRAGMA user_version = 114;
