-- 052_extraction_item_edge.sql
-- SCHEMA migration — hop 4 gets its edge object, and a reader in the same commit.
--
-- THE PROBLEM THIS SOLVES
-- Plan §2 hop 4 is source → extracted value. The table exists and is populated,
-- but nothing on it says which design parameter the extracted value describes.
-- The 2026-08-02 plan (§4.0) names the consequence: extraction → specification
-- "resolves by text-matching `parameter`, the one fuzzy hop in an otherwise
-- typed chain."
--
-- Text-matching does not resolve it. All 8 rows carry parameter='RT60', and
-- there are TWO RT60 items: A-18 "RT60 in Occupied Learning and Listening
-- Spaces" and A-10b "RT60 for Hydrotherapy and Pool Environments". The slug
-- does not resolve it either -- 13 items carry
-- bpc_source_slug='room-acoustic-performance'. The reasoning doc anticipated
-- exactly this at line 82: context-keyed items ("RT60-classroom vs
-- RT60-hydrotherapy") are the operative pattern for context differentiation.
-- So the parameter name is ambiguous by design, and the edge has to be typed.
--
-- A COLUMN, NOT A JUNCTION
-- 044 and 050 both added junctions, so the default here would be a third. It
-- would be wrong. Those two normalised JSON arrays that ALREADY expressed
-- many-to-many data. Nothing in these 8 rows expresses a two-item extraction,
-- and the grain forbids it: an extraction row is one claim, from one source
-- section, at one scope -- `claim_text`, `source_section` and
-- `root_population_note` all scope it. REF-00563 already appears twice
-- (extraction 2, footnote-e 0.3 s; extraction 4, main-body 0.6 s) because those
-- are two claims. A source reaching two items is row multiplication, not an
-- edge set, and it does not corrupt independence scoring because independence
-- counts at `root_id` grain -- extraction 1's own basis text says it: "both
-- DEAF rows root here so the line counts once."
--
-- The cautionary precedent is in this table's own family:
-- `extraction_population_links`, a junction hanging off `extraction_id`, has
-- ZERO rows. That is the 043 shape -- a container for a cardinality that never
-- arrived. `spec_value_probes`, the next link in the same chain, types its item
-- as a scalar `item_code TEXT NOT NULL REFERENCES items(item_code)`. This
-- column extends that pattern one hop upstream. If a genuinely two-item single
-- claim ever appears, the answer is two rows sharing a root_id, not a schema
-- change.
--
-- NULLABLE, DELIBERATELY
-- NOT NULL would force an item to be invented for every future capture whose
-- item is not yet established -- the schema equivalent of minting an exec_id for
-- an unlogged search, which migration 050 refused. NULL here means "the item was
-- not established at extraction", and that is a fact worth being able to state.
-- The case is live rather than theoretical: the 19 capture-pending sources on
-- `energy-conservation-rest-points-seating` will land NULL, because that slug
-- has NO item at all -- zero `items.bpc_source_slug` matches and zero
-- `item_bpc_links` rows. (This corrects the reason given for promoting this
-- rung: see the plan's §7.2. The 19 do not need this edge on arrival. The 8
-- existing rows need it now, and step 9 is about to make the backfill harder --
-- see below.)
--
-- FK IS SAFE
-- Every existing item_code column in the DB was orphan-scanned before declaring
-- this one: `term_item_links` 0/147, `item_axis_links` 0/158,
-- `spec_value_probes` 0/31, `evidence_cell_state` 0/15, `item_audit_runs` 0/87.
-- The "26/26 phantom" the plan warns about is `jurisdictional_values.spec_id`,
-- keys of a table that does not exist -- a different column family, and an
-- argument FOR declaring the FK at birth rather than against.
--
-- WHY BEFORE STEP 9, NOT AFTER
-- The backfill's witnesses are unambiguous only while A-10b has nothing: no
-- `item_bpc_links` row, no cell, no probe (all verified zero). Step 9's
-- `item_bpc_links` backfill is expected to give A-10b its parameter link, at
-- which point "the slug's item for this parameter" stops resolving uniquely.
-- The window is the argument for this ordering, and it is the one the ladder
-- did not state.
--
-- TIMESTAMPS
-- No DEFAULT (datetime('now')) -- 044's rule. The data migration that follows
-- sets updated_at explicitly.
--
-- Forward-only; user_version -> 52.

ALTER TABLE source_value_extractions ADD COLUMN item_code TEXT
  REFERENCES items(item_code);

CREATE INDEX IF NOT EXISTS idx_sve_item ON source_value_extractions(item_code);

-- ── The reader, shipped with the edge ──────────────────────────────────────
-- Migration 051 exists because 050 shipped a junction with no query path and
-- called the reverse walk "the point" while providing no way to walk it. That
-- lesson is one migration old; this is the query the edge is for.
--
-- `assess_cell.py` degrades three separate assessments to NOT_ASSESSED /
-- pending_assessment citing this table (lines 194, 252-255, 319-326). Its
-- value-convergence branch needs exactly this shape: for one item, every
-- extracted value with its claim type, status, root classification and whether
-- it is contested. The view does not decide convergence -- deciding is
-- synthesis, and synthesis is Opus-floored. It supplies the input.
CREATE VIEW IF NOT EXISTS v_item_extractions AS
SELECT
    i.item_code,
    i.name                      AS item_name,
    i.category                  AS item_category,
    sve.extraction_id,
    sve.slug,
    sve.parameter,
    sve.parameter_canonical,
    sve.population_code,
    sve.jurisdiction,
    sve.claim_type,
    sve.claimed_value,
    sve.claimed_unit,
    sve.extraction_status,
    sve.extraction_method,
    sve.root_id,
    sve.root_type,
    sve.root_ref_id,
    sve.contested,
    sve.ref_id,
    es.tier                     AS source_tier,
    es.verification_status,
    sve.promoted_to_rdc_id
FROM items i
JOIN source_value_extractions sve ON sve.item_code = i.item_code
LEFT JOIN evidence_sources es     ON es.ref_id     = sve.ref_id;
