-- 131_extraction_lens_links.sql
-- SCHEMA migration -- the lens link table for figures (OR-1c, owner 2026-11-06: "link table unless that is more
-- prone to errors"; the 2026-08-28 clause "Never a population_* link table" is superseded for a figure's lens
-- codes by OD-39, owner 2026-11-12). Design: workplan/2026-11-12-bidirectional-pipeline/tasks/T-018-design.md.
--
--   1. CREATE extraction_lens_links: one row per (figure, lens code); four typed FK lens columns, exactly one
--      per row; a typed warrant (basis, basis_text); retire-in-place columns (OD-29). One LIVE link per
--      (figure, code) by a partial unique index. v_live_lens_links is the one read surface.
--   2. CARRY every non-NULL lens value of source_value_extractions into the table as a `carried` link,
--      stamped with the figure's own created_*/updated_* (the lens was asserted when the figure was written).
--   3. REBUILD source_value_extractions with the four lens columns copied as NULL and the D-0182 "at least one"
--      CHECK inverted to "all NULL". Not dropped: committed data migrations INSERT these columns.
--      Generated from the live DDL (migration 114's recipe), not retyped: build under a temporary name, copy
--      by column name, DROP the old, RENAME the new (so the inbound keys from extraction_relations,
--      specification_extraction_links, connection_targets and extraction_follow_ups keep their target),
--      recreate the indexes, then the views from their own stored SQL, verbatim. The views come down first
--      because SQLite refuses a rename while a view is unresolvable: v_root_id_conflicts, v_derived_figure_check, v_value_independence, v_determination_provenance, v_unregistered_roots, v_scan_ledger.
--      None of those views reads the four lens columns of the figure.
--      A carried link takes the figure's own created_by_session (NOT NULL here). The check that no figure lacks one:
--      select count(*) from source_value_extractions where created_by_session is null   -- must print 0 before this runs
--
-- The table is AUTOINCREMENT. DROP TABLE takes its sqlite_sequence row, so the floor is captured first and
-- restored as a maximum afterwards (migration 076: an identifier is never reissued).
--
-- ORDER: the carry and the rebuild read every figure once, after every committed data migration has written
-- theirs; without this marker the rebuild would carry from an empty table and then replay the data migrations
-- into the columns, which the inverted CHECK refuses. A data migration captured before this one and merged
-- after it that INSERTs a lens column is refused by that CHECK and must be captured again through
-- add-extraction / add-lens-link.
-- AFTER_DATA: 20261106053823

CREATE TABLE extraction_lens_links (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    -- THE FOUR LENSES, typed, one per row (2026-08-28 shape; "never two lenses in one row").
    identity_code       TEXT REFERENCES base_taxonomy_identity(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    medical_code        TEXT REFERENCES base_taxonomy_medical(medical_code),
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
         + (needs_code IS NOT NULL) + (medical_code IS NOT NULL) = 1),
    CHECK ((basis = 'carried') = (basis_text IS NULL)),
    CHECK (basis_text IS NULL OR length(trim(basis_text)) > 0),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL)
       AND (retired_at IS NULL) = (retirement_reason IS NULL))
);
-- One LIVE link per (figure, code). A retired link may repeat a live one (history).
CREATE UNIQUE INDEX ux_extraction_lens_live ON extraction_lens_links
    (extraction_id, COALESCE(identity_code, ''), COALESCE(icf_code, ''),
     COALESCE(needs_code, ''), COALESCE(medical_code, ''))
    WHERE retired_at IS NULL;
CREATE INDEX ix_ell_extraction ON extraction_lens_links(extraction_id);
CREATE INDEX ix_ell_identity   ON extraction_lens_links(identity_code) WHERE retired_at IS NULL;
CREATE INDEX ix_ell_icf        ON extraction_lens_links(icf_code)      WHERE retired_at IS NULL;
CREATE INDEX ix_ell_needs      ON extraction_lens_links(needs_code)    WHERE retired_at IS NULL;

-- THE CARRY: one `carried` link per non-NULL lens value of every figure.
INSERT INTO extraction_lens_links (extraction_id, identity_code, basis, created_at, created_by_session, updated_at, updated_by_session)
  SELECT extraction_id, identity_code, 'carried', created_at, created_by_session,
         COALESCE(updated_at, created_at), COALESCE(updated_by_session, created_by_session)
    FROM source_value_extractions WHERE identity_code IS NOT NULL;
INSERT INTO extraction_lens_links (extraction_id, icf_code, basis, created_at, created_by_session, updated_at, updated_by_session)
  SELECT extraction_id, icf_code, 'carried', created_at, created_by_session,
         COALESCE(updated_at, created_at), COALESCE(updated_by_session, created_by_session)
    FROM source_value_extractions WHERE icf_code IS NOT NULL;
INSERT INTO extraction_lens_links (extraction_id, needs_code, basis, created_at, created_by_session, updated_at, updated_by_session)
  SELECT extraction_id, needs_code, 'carried', created_at, created_by_session,
         COALESCE(updated_at, created_at), COALESCE(updated_by_session, created_by_session)
    FROM source_value_extractions WHERE needs_code IS NOT NULL;
INSERT INTO extraction_lens_links (extraction_id, medical_code, basis, created_at, created_by_session, updated_at, updated_by_session)
  SELECT extraction_id, medical_code, 'carried', created_at, created_by_session,
         COALESCE(updated_at, created_at), COALESCE(updated_by_session, created_by_session)
    FROM source_value_extractions WHERE medical_code IS NOT NULL;

CREATE TEMP TABLE _131_seq AS SELECT name, seq FROM sqlite_sequence;

DROP VIEW "v_root_id_conflicts";
DROP VIEW "v_derived_figure_check";
DROP VIEW "v_value_independence";
DROP VIEW "v_determination_provenance";
DROP VIEW "v_unregistered_roots";
DROP VIEW "v_scan_ledger";

CREATE TABLE "_131_new_source_value_extractions" (
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

  -- THE FOUR LENSES: HISTORY since migration 131 (OR-1c). A figure's lens is a set of rows in
  -- extraction_lens_links, read through v_live_lens_links; these four columns are held NULL by the CHECK
  -- at the foot of this table and are never written again. They are kept because committed data
  -- migrations INSERT them (CLAUDE.md rule 5: a column a committed data migration INSERTs can never be
  -- dropped). Until 131 they were real typed FKs, one per lens (owner 2026-08-28, replacing
  -- `population_code` and the free-text `population_label`), under D-0182's "at least one" CHECK.
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
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NULL)
);
INSERT INTO "_131_new_source_value_extractions" ("extraction_id", "ref_id", "slug", "parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator", "harm_finding", "value_as_written")
  SELECT "extraction_id", "ref_id", "slug", "parameter_id", NULL, NULL, NULL, NULL, "jurisdiction", "setting", "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section", "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm", "device_class", "root_population_note", "root_classification_basis", "contested", "file_anchor", "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end", "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note", "extraction_method", "extraction_status", "promoted_to_rdc_id", "notes", "created_at", "created_by_session", "updated_at", "updated_by_session", "figure_role", "comparator", "harm_finding", "value_as_written"
  FROM "source_value_extractions";
DROP TABLE "source_value_extractions";
ALTER TABLE "_131_new_source_value_extractions" RENAME TO "source_value_extractions";
CREATE INDEX idx_sve_ref    ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status ON source_value_extractions(extraction_status);
CREATE INDEX ix_sve_locator ON source_value_extractions(loc_section, loc_clause);
CREATE INDEX idx_sve_param_ref ON source_value_extractions(parameter_id, ref_id);

INSERT INTO sqlite_sequence (name, seq)
  SELECT s.name, s.seq FROM _131_seq s
   WHERE s.name NOT IN (SELECT name FROM sqlite_sequence);
UPDATE sqlite_sequence SET seq = MAX(seq,
        (SELECT s.seq FROM _131_seq s WHERE s.name = sqlite_sequence.name))
  WHERE name IN (SELECT name FROM _131_seq);
DROP TABLE _131_seq;

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

-- The one read surface for a figure's lens (OD-29: every reader filters on the retired mark first).
CREATE VIEW v_live_lens_links AS
SELECT link_id, extraction_id, identity_code, icf_code, needs_code, medical_code,
       basis, basis_text, created_at, created_by_session
  FROM extraction_lens_links
 WHERE retired_at IS NULL;

PRAGMA user_version = 131;
