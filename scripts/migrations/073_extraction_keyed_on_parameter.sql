-- 073_extraction_keyed_on_parameter.sql
-- SCHEMA migration — the JUDGMENT hand-off gets the same subject and the same lenses
-- the determination got in 071. Nothing here is new doctrine; all of it is owed sweep.
--
-- WHAT 071 LEFT HALF-DONE. 071 gave `specifications` `parameter_id NOT NULL` and the four
-- lens columns, and gave `source_value_extractions` a NULLABLE `parameter_id` with this
-- reason, quoted from its own §2 comment:
--
--     "NULLABLE on purpose: an extraction is written when the value is read out of the
--      source, and the parameter is adjudicated afterwards. NULL means 'not yet
--      adjudicated' ... parameter_canonical stays for now and is writer-retired rather
--      than dropped"
--
-- That window closes here, and it closes for a reason 071 could not have acted on: there
-- has never BEEN a writer. Measured 2026-09-10 -- `grep -c source_value_extractions
-- scripts/db.py` returns 0, and no committed data migration INSERTs into the table
-- (`grep -lE 'INSERT[[:space:]]+INTO[[:space:]]+"?source_value_extractions"?'
-- scripts/migrations/*.sql` -> no matches; the one migration naming the table names it
-- inside a `decisions` INSERT). So "written before adjudication" describes an act nobody
-- can perform. `db.py add-extraction` ships in this same change and requires the
-- parameter, so the row and its subject are minted together.
--
-- THREE RULINGS EXECUTED HERE, none of them new:
--
--   2026-08-27, D-0168 (decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-
--     extraction.md) -- "The evidence item is the SOURCE; the judgment item is the
--     extracted, tiered, categorised value. Evidence to judgment is 1:N." This table is
--     at JUDGMENT. `parameter_id` is therefore judgment's OWN key, not a judgment fact
--     smuggled into evidence -- which is what makes NOT NULL stage-correct rather than
--     premature.
--
--   2026-08-26 (references/project-standards.md, `grep -n 'judgment object is the'`)
--     "The judgment object is the canonical parameter." Its ACTION (2) ordered a
--     canonical-parameter vocabulary whose "home is the schema's own CHECK or a registry
--     table"; 071 built the registry table. See the ACTION (3) note below -- it is the
--     one clause of that ruling this migration does not obey literally, and why.
--
--   2026-08-28, as relaxed by D-0182 (2026-09-01)
--     The four lens columns. That ruling names this table by name in its own evidence:
--     "11 tables can express identity, 3 icf, 2 needs, 0 medical. Every attachment point
--     except `items` is identity-only -- `specifications`, `source_value_extractions`,
--     ..." and its CONDITION is "any session ... attaching a determination, EXTRACTION,
--     case study or economics entry to a group of disabled people". ACTION: "Four lens
--     columns, one CHECK, real FKs. Never a `population_*` link table. `population_code`
--     is retired in favour of the four." D-0182 relaxed "exactly one" to AT LEAST ONE --
--     COALESCE(...) IS NOT NULL -- which is the form 065 and 071 both carry.
--
-- A FOURTH STANDING RULING TOUCHES THIS TABLE AND IS *NOT* EXECUTED HERE. Recorded,
-- because the silence is the defect -- CLAUDE.md §6 carries this exact failure mode as
-- its own proof paragraph: a ruling can be in the repository, in the file §9 sends you
-- to, and still fail to bind because the search stopped at the first answer it found.
-- Three rulings were cited above; this one was not, and this migration recreates the
-- very table it names.
--
--   2026-08-27, owner ruling (references/project-standards.md, `grep -n "hand-off object
--   is named"`): "Every stage's hand-off object is named `<stage>_items`, and the
--   hand-off is a NOT NULL foreign key", quoted from the owner in two parts -- "just
--   call them whatever their stage is and add -item" and "we don't need to iterate
--   different words for item -- we just append '-item'". Its ACTION (2): "The five
--   hand-off keys land in the same migration as the rename -- not a follow-up." The
--   owner selected "the rename creates the spine" OVER deferring it to a second
--   migration, in as many words. This table is the JUDGMENT hand-off object (D-0168),
--   so under that ruling its name is `judgment_items`.
--
-- WHY THE RENAME IS NOT EXECUTED HERE, stated as a cost rather than as a reason to
-- forget it. D-0168, ratification item 2, records that `judgment_items` needs "no new
-- table and no new key" -- the key already exists, the shape is already right, and
-- `scripts/audit/judgment_handoff_shape.py` (BLOCKING) already pins it. So what is left
-- IS the rename, and a rename is not done until the callers are swept (rule 4: a VIEW
-- is a caller, so is a skill, so is the check registry).
--
-- MEASURED 2026-09-10, so the next session inherits a number rather than an impression:
--   * 26 live executable/config callers name `source_value_extractions` by string
--     (`git grep -l source_value_extractions -- '*.py' '*.sh' '*.yaml' '*.yml' '*.sql'`,
--     minus `_archived/` and `scratchpad/`); 17 of them are Python.
--   * 5 schema objects: the three views this migration re-derives, the
--     `extraction_population_links` junction whose FK names the table, and five indexes
--     carrying the `sve` stem.
--   * `judgment_handoff_shape.py:31` says it in its own source: `TABLE =
--     "source_value_extractions"  # the judgment item; a rename must sweep this`, and
--     its FAIL branch for a missing table says the same again.
--   * `dbcore.WRITABLE_TABLES` and therefore `emit_batch_sql.py` -- the capture path
--     that has now been blind to a live table FIVE separate times, each recorded in
--     that list's own comments.
--   * Prose callers, which no gate covers at all.
-- A rename touching that surface belongs in a migration whose ONLY job is the rename,
-- with the other four stages' hand-off objects, because the ruling's own ACTION (2)
-- says the five keys land together. Doing one-fifth of it inside a re-key would leave
-- the spine half-named -- the same "deleting one of five is worse than deleting none"
-- reasoning this migration already applies to `extraction_population_links` below.
--
-- WHAT IS OWED, precisely: `source_value_extractions` -> `judgment_items`, alongside
-- `source_locators` -> `research_items`, `bpc_metadata` -> `synthesis_items`,
-- `specifications` -> `specification_items`, and the junctions for the fan-in half.
-- Under rule 0 this ruling is not weakened by having gone unexecuted; it is owed.
--
-- ONE RULING CLAUSE SATISFIED IN SUBSTANCE RATHER THAN IN LETTER, recorded rather than
-- silently resolved. The 2026-08-26 ACTION (3) reads: "`add-extraction` (P1.2) must
-- REQUIRE `parameter_canonical`, not accept the column's nullability, or extractions
-- become unjoinable to the determinations they exist to support." The clause states its
-- own purpose -- joinability -- and names `parameter_canonical` because on 2026-08-26 no
-- registry existed to point at; the SAME ruling's ACTION (2) ordered one built, and 071
-- built it. This migration requires the key and the key is `parameter_id`. Requiring
-- `parameter_canonical` AS WELL would put the parameter's name in a second home: it lives
-- in `terms.canonical_en`, reached by pointer through `base_parameters.term_id`, and
-- rule 5 forbids the copy. The clause is discharged, not defied.
--
-- THIS MIGRATION PUTS THE TABLE INTO THE UNWRITABLE SET, AND THAT IS THE POINT. Say it
-- out loud, because CLAUDE.md §4's probe now prints a line it did not print before:
--
--     UNWRITABLE  source_value_extractions.parameter_id -> empty table
--
-- `parameter_id` is NOT NULL into `base_parameters`, which holds 0 rows, so a bare
-- INSERT dies with `FOREIGN KEY constraint failed` -- at INSERT, never at migration
-- time. That is the exact trap §4 names: "the schema looks healthy, a rebuild
-- reproduces it exactly, and every gate stays green over a table that cannot accept a
-- row", and `specifications` and `item_taxonomy_links` are already in it.
--
-- WHY IT IS THE GOOD VERSION OF THAT STATE, and the difference is the whole of it. The
-- other two are unwritable AND SILENT: they refuse with SQLite's sentence, which names
-- neither the cause nor the fix. This table ships its writer in the same change, and
-- `db.py add-extraction` refuses EARLY and BY NAME -- it counts `base_parameters`
-- before touching anything and says "Mint the subject first, from an adjudicated
-- term: db.py add-parameter --term-id TERM-NNN". Verified 2026-09-10 against a scratch
-- copy: minting a parameter first makes the table accept rows immediately. The state
-- is a precondition an operator is told how to satisfy, not a wall.
--
-- WHAT CHANGED, exactly: a writable-but-writerless table became a writer-having-but-
-- FK-blocked one. Both readings of "0 rows" were wrong before and are wrong now --
-- rule 4's "treat a 0-row object as unproven, not clean". Derive the live unwritable
-- set with §4's probe before planning any write; never quote this comment for it.
--
-- WHY THE TABLE CAN BE DROPPED AND RECREATED. It holds 0 rows and NO committed migration
-- INSERTs into it (measured above), so a replay reaches this point with the table empty
-- and nothing downstream to strand. Rule 5's "a column a committed data migration INSERTs
-- can never be dropped" does not bite, because nothing was ever inserted. This is exactly
-- 071's warrant for dropping and recreating `specifications`, re-measured for this table.
--
-- WHAT IS NOT TOUCHED, AND WHY, so a reader does not read silence as oversight:
--
--   `slug`. `evidence_sources` has no slug column; `source_slug_links` is the junction.
--   "This extraction was mined under this slug" is a fact OF THE EXTRACTION -- one source
--   admitted under two slugs can be mined for a different parameter under each -- not a
--   copy of the junction. It stays, NOT NULL, with its FK.
--
--   NO UNIQUE INDEX, ANYWHERE ON THIS TABLE. Deliberate and ruled. D-0168: "one evidence
--   source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)".
--   `scripts/audit/judgment_handoff_shape.py` (BLOCKING) fails if any UNIQUE index appears
--   here. 071 put `idx_spec_row_identity` -- a UNIQUE row-identity index -- on
--   `specifications`; copying that pattern onto this table would collapse the ruled 1:N
--   fan-out and abolish the DR-2026-08-19 §7 dissent contest, where a divergent
--   adversarial grade lands as a second row and the divergence reads as a contest. The
--   two tables are deliberately shaped differently and this comment is why.
--
--   `extraction_population_links` (0 rows). The 2026-08-28 ruling lists it among "five
--   splinter tables [that] are DELETED, not renamed" -- with `probe_population_links`,
--   `citation_population_links`, `case_study_populations`, `economics_entry_populations`.
--   That deletion is still owed and is NOT executed here: deleting one of five is worse
--   than deleting none, because it hides the four that remain, and each has its own
--   callers (schemas/population_links.py, validate_pydantic_schemas' MODEL_TABLE_MAP,
--   population_integrity_audit.py, regenerate_vetting_surface.py). Its FK names
--   `source_value_extractions(extraction_id)`, which this migration preserves, so the
--   drop/recreate leaves it exactly as dead as it was.

-- ---------------------------------------------------------------------------
-- 1. Views first. A VIEW IS A CALLER (rule 4) and three of the four read a column
--    this migration retires; SQLite would let them rot silently otherwise.
-- ---------------------------------------------------------------------------

-- v_item_extractions: DELETED.
--
-- CLAUDE.md §3 requires the stage question to be ASKED BEFORE a view is deleted, because
-- "a cross-stage view IS the pointer ... deleting it forces the next reader back to
-- copying". Asked and answered:
--
--   WHICH STAGES DOES IT SPAN? Three. `items` is RENDER -- owner 2026-08-26 demoted it
--   "from identity to rollup ... the Part-4 render aggregate ... derived FROM
--   specifications rather than keyed by them". `source_value_extractions` is JUDGMENT
--   (D-0168). `evidence_sources` is EVIDENCE. So render + judgment + evidence.
--
--   THEN WHY IS DELETING IT NOT THE PROHIBITED ACT? Because the prohibition protects a
--   pointer that a reader would otherwise have to re-copy, and this view's pointer is the
--   edge the ruling itself deleted. It joins `sve.item_code = i.item_code` -- the hop-4
--   item edge -- and the 2026-08-26 ACTION (5) says "`items` survives as the Part-4
--   rollup only -- no new writer keys anything on `item_code` at the judgment stage".
--   The rollup's route is now items <- specifications <- base_parameters, DERIVED, not
--   joined through extractions. A reader deprived of this view is not pushed toward
--   copying; they are pushed toward the route the ruling installed.
--
--   AND NO REPLACEMENT IS BUILT. A `v_parameter_extractions` would have zero readers on
--   the day it shipped -- `v_item_extractions` has none today either (swept 2026-09-10:
--   no executable caller SELECTs from it; the only hits are the GENERATED
--   governance/context-map.yaml inventory, prose in project-standards.md and two
--   workplans, and its own definition in the 057 baseline). CLAUDE.md §8: "Nothing is
--   added without naming what reads it." Build it when something reads it.
DROP VIEW IF EXISTS v_item_extractions;

-- v_unregistered_roots: re-derived. It selected `sve.parameter`, the free-text column
-- this migration retires. The label now comes BY POINTER from `terms` -- which is rule 5
-- applied to the view, not merely to the table: the diagnostic keeps its human-readable
-- parameter name without any table copying it.
DROP VIEW IF EXISTS v_unregistered_roots;
CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id);

-- v_value_independence: re-derived a second time, for the second half of 2026-08-26
-- ACTION (4). 071 took `population_code` out of its grain and left
-- `COALESCE(parameter_canonical, parameter)` as the label, saying so in its own comment:
-- the text columns "remain as the fallback label while extractions are still being
-- adjudicated (parameter_id NULL)". `parameter_id` is NOT NULL from this migration on, so
-- the fallback has nothing left to fall back FROM, and the JOIN cannot drop a row.
-- Swept again 2026-09-10: still no executable caller SELECTs from this view -- only the
-- baseline that defines it, prose in evidence-architecture.md and the pipeline contract.
DROP VIEW IF EXISTS v_value_independence;
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
    GROUP BY sve.parameter_id, t.canonical_en;

-- v_root_id_conflicts: SWEPT, UNCHANGED, and that is a finding not an omission. It reads
-- `root_ref_id` and `root_id` only -- neither is retired here -- so it is re-verified
-- rather than re-derived. Rule 4's "treat a 0-row object as unproven, not clean" is
-- discharged by the post-migration probe in this session's report, which re-executes
-- every surviving view against the rebuilt schema rather than trusting that it parses.

-- ---------------------------------------------------------------------------
-- 2. The judgment item, re-keyed.
-- ---------------------------------------------------------------------------
DROP TABLE source_value_extractions;

CREATE TABLE source_value_extractions (
  extraction_id          INTEGER PRIMARY KEY AUTOINCREMENT,

  -- THE HAND-OFF KEY (D-0168; pinned by the blocking judgment_handoff_shape check):
  -- NOT NULL, a real FK at the evidence item, and NO UNIQUE index over it anywhere.
  ref_id                 TEXT NOT NULL REFERENCES evidence_sources(ref_id),

  -- The slug this extraction was MINED UNDER. Not a copy of source_slug_links: that
  -- junction says the source is admitted to the slug; this says the reading happened
  -- there. `evidence_sources` has no slug column, so there is nothing to point at.
  slug                   TEXT NOT NULL REFERENCES slugs(slug),

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
  -- duplicate, and an UNREALISED one -- 0 rows, no writer, ever.
  --
  -- WHAT GUARANTEES CLAUSE-LEVEL VERBATIM ON THIS ROW, AND WHAT DOES NOT. An earlier
  -- draft of this comment said verbatim "survives here in `claim_text` plus
  -- `source_section` and the 16 `loc_*` columns" -- which overclaimed, because EVERY
  -- one of those columns is NULLABLE and this migration cannot make them otherwise
  -- without a NOT NULL default nobody can supply. Reproduced 2026-09-10: a happy-path
  -- row came out with claim_text NULL, source_section NULL, no loc_*, notes NULL --
  -- ZERO verbatim, where before this migration `parameter` was NOT NULL and every row
  -- carried at least the source's own phrase for what it measures.
  --
  -- THE GUARANTEE IS THE WRITER'S, NOT THE SCHEMA'S, and it is stated that way on
  -- purpose. `db.py add-extraction` makes `--claim-text` REQUIRED and refuses a blank,
  -- so every row this project writes carries the source's own words at clause grain.
  -- The table itself does not enforce it: a row inserted by any other path can still
  -- carry none. Tightening the column is a compensating migration, and it is worth
  -- doing the first time a second writer exists -- not before, when the CLI is the
  -- only writer and the refusal is where an operator can actually read it.
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
  icf_code               TEXT REFERENCES axes(axis_code),
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
  root_id                TEXT,
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
  updated_by_session     TEXT,

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

-- ---------------------------------------------------------------------------
-- 3. Indexes. Every CHECK vocabulary above is written in the `col IN (...)` form that
--    dbcore.check_values() parses, so the CLI's refusals read the schema rather than a
--    list in code (CLAUDE.md §4). Verified for all six vocabularies after this migration.
-- ---------------------------------------------------------------------------

-- Carried across from the dropped table, unchanged in key and name.
CREATE INDEX idx_sve_ref    ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status ON source_value_extractions(extraction_status);
CREATE INDEX ix_sve_locator ON source_value_extractions(loc_section, loc_clause);

-- idx_sve_item IS NOT RECREATED. It indexed `item_code`, which is retired here.
-- Recorded rather than left to inference.

-- idx_sve_slug_param, re-derived onto the new key. It was (slug, parameter_canonical);
-- the second column is retired, so the index follows the key rather than dying with it.
-- READER: tools/regenerate_vetting_surface.py, which selects extractions `WHERE slug = ?`,
-- and v_unregistered_roots, which reports per (slug, parameter).
CREATE INDEX idx_sve_slug_param ON source_value_extractions(slug, parameter_id);

-- NEW, and named for what reads it: assess_cell.gather_sources(), re-written in this same
-- change to gather the sources holding an extraction FOR THIS PARAMETER -- an equality on
-- parameter_id joined to evidence_sources on ref_id. parameter_id leads because it is the
-- equality predicate; ref_id follows so the join key is covered.
--
-- EXPLICITLY NOT UNIQUE. `UNIQUE (ref_id, parameter_id)` is the natural-looking mistake
-- here and it is forbidden: D-0168 rules one source may yield MANY judgment rows for one
-- parameter (NBC 3.8's clauses), and DR-2026-08-19 §7 preserves a dissent contest in which
-- a divergent adversarial grade lands as a second row. judgment_handoff_shape.py fails on
-- any UNIQUE index on this table.
CREATE INDEX idx_sve_param_ref ON source_value_extractions(parameter_id, ref_id);

PRAGMA user_version = 73;
