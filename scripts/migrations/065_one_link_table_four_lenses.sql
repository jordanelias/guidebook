-- 065_one_link_table_four_lenses.sql
-- SCHEMA migration — one item×taxonomy link table, four lenses, one row per fact.
--
-- WHAT THE OWNER ASKED FOR, 2026-09-01, in their own words:
--     "a dynamically rendering website with a multimodal lens and filters so that we
--      can have specifications that are presented according to which lens the user
--      chooses and what filters they have selected"
-- with three constraints given in the same exchange: taxonomies ABSTRACTED so
-- downstream tables reference them dynamically; absence in a lens is OK; but a link
-- MUST tie to at least one, and IDEALLY ties into many.
--
-- WHY A WIDE ROW AND NOT A TRAVERSAL. The alternative — store the fact in one lens and
-- cross to the others at render through population_axis_map / access_need_axis_map — is
-- what the schema is shaped for today, and it was measured on 2026-09-01
-- (scratchpad/session_2026-09-01-lens-architecture/LENS-ARCHITECTURE.md):
--
--   * The crossings are INCOMPLETE. identity→ICF covers 20 of 23 (ALL, ID, MOVE have no
--     row); ICF→identity 16 of 17 (AX-COG-L); needs→ICF 15 of 17 (A-AT, A-TIME);
--     ICF→needs 15 of 17 (AX-PAI, AX-THR); identity↔needs has NO direct map at all.
--     Every gap is a silently empty page, not a "no results" page.
--   * Traversal MANUFACTURES INFERENCE and changes the answer. Asking the identity lens
--     for DEAF returns 20 items. Asking the ICF lens for AX-AUD — the axis DEAF crosses
--     to — returns 38 rows, because DEAFBLIND also crosses to AX-AUD. Only the first is
--     a recorded fact; the second is produced by a JOIN. D-0174 reserves applicability
--     to synthesis, so a render layer that crosses is adjudicating in the one place
--     nothing reviews and no attestation covers.
--
-- So the lens becomes a COLUMN CHOICE. `WHERE identity_code=?` / `WHERE icf_code=?` /
-- `WHERE needs_code=?` / `WHERE medical_code=?` — one query shape, four lenses, no
-- UNION anywhere. A UNION is only forced when the taxonomies live in separate link
-- tables, which is the state this migration ends.
--
-- WHAT IT FOLDS, AND WHY THAT IS THE POINT. The ICF lens already had a SECOND HOME:
-- `item_axis_links`, 158 rows, measured today. Two link tables for one relationship is
-- rule 5's dual home, and it is why the render layer could not ask a lens-neutral
-- question. 372 + 158 = 530 rows land in one table. Nothing is merged semantically:
-- every column of both tables survives under its own name, because merging
-- `strength_band` into `applicability` would be a doctrinal judgement and this is a
-- schema migration.
--
-- APPLICABILITY BECOMES NULLABLE, DELIBERATELY. It was NOT NULL DEFAULT 'applies' on
-- item_population_links. The 158 axis rows never carried it, and defaulting them to
-- 'applies' would assert an applicability judgement that nobody made — the exact
-- inference D-0174 reserves to synthesis. NULL now means "not adjudicated". The CHECK
-- keeps all five values verbatim so dbcore.check_values() still reads the vocabulary
-- (a CHECK passes on NULL, so no `OR ... IS NULL` clause is needed or wanted).
--
-- THE AT-LEAST-ONE RULE IS A TABLE-LEVEL CHECK, and it has to be written now rather
-- than added later: SQLite's ALTER TABLE ADD COLUMN can carry a REFERENCES clause but
-- cannot add a table-level CHECK, so a medical_code bolted on afterwards would sit
-- outside the constraint and a medical-only row would be refused. Hence
-- base_taxonomy_medical is created here — D-0170 (ADOPTED, owner ruling 2026-08-27)
-- names it as one of the four lenses and it has never existed. It is created EMPTY:
-- populating a disability vocabulary is content, DG-NON, and the owner's alone.
--
-- rationale_ref BECOMES A TYPED POINTER. OD-A (D-0175, 2026-08-31) rules these links
-- substrate PROVISIONALLY: any edge a determination relies on must be re-derived and
-- carry a rationale_ref in that determination's own migration. Measured, that duty was
-- unenforceable — rationale_ref was an unconstrained INTEGER with no foreign key, so it
-- pointed at nothing and any integer satisfied it. Owner ruling 2026-09-01: it
-- references the decision that authorises the edge. It stays NULLABLE; the 530 existing
-- edges keep NULL, because OD-A's debt is paid where an edge is USED, not all at once.
--
-- WHY ONE MIGRATION AND NOT TWO. Rebuilding this table twice would sweep its callers
-- twice, which is the failure §0.4 describes. Every change that needs a rebuild — the
-- rationale_ref type change, the four lens foreign keys, the table-level CHECK, the
-- primary key — is made here, once.
--
-- EDITING AN UNAPPLIED MIGRATION. This file was committed on 2026-09-01 as
-- `065_rationale_ref_points_at_the_decision.sql` and has never run: PRAGMA user_version
-- is 64 and schema migrations leave no ledger row. Rule 3's immutability protects
-- APPLIED migrations from diverging from the database they built; there is no such
-- database here. Fixing forward instead would mean landing a shape the same session
-- already knows is wrong, then rebuilding to correct it.
--
-- WHAT IS PRESERVED, verified after by scripts/audit/rename_insurance.py rather than
-- assumed: 530 rows with every column value intact, the applicability vocabulary, the
-- items and populations foreign keys including ON DELETE CASCADE, and uniqueness of
-- (item_code, subtype, lens tuple). Neither table has an inbound foreign key, a view,
-- or a trigger — measured, not assumed.
--
-- WHAT CHANGES BEHAVIOURALLY, stated rather than buried: the 158 folded axis rows gain
-- ON DELETE CASCADE on item_code, which item_axis_links did not have. Deleting an item
-- is not a live operation here, and one cascade rule for one table beats two.

PRAGMA legacy_alter_table=OFF;

-- ---------------------------------------------------------------------------
-- The fourth lens. D-0170 named it; it has never existed.
-- ---------------------------------------------------------------------------
CREATE TABLE base_taxonomy_medical (
  medical_code        TEXT PRIMARY KEY,
  display_name        TEXT NOT NULL,
  description         TEXT,
  status              TEXT NOT NULL DEFAULT 'active'
                        CHECK(status IN ('active','deprecated','superseded')),
  notes               TEXT,
  created_at          TEXT DEFAULT (datetime('now')),
  created_by_session  TEXT
);

-- ---------------------------------------------------------------------------
-- One link table. Four nullable lens pointers, at least one required.
-- ---------------------------------------------------------------------------
CREATE TABLE item_taxonomy_links (
  item_code           TEXT NOT NULL,

  -- The four lenses (D-0170). NULL means "this fact is not stated in that lens",
  -- which is legitimate; a row stating several lenses at once is the ideal.
  identity_code       TEXT REFERENCES populations(population_code),
  icf_code            TEXT REFERENCES axes(axis_code),
  needs_code          TEXT REFERENCES access_needs(need_code),
  medical_code        TEXT REFERENCES base_taxonomy_medical(medical_code),

  subtype             TEXT NOT NULL DEFAULT '',  -- '' = no subtype, so it indexes

  -- From item_population_links. NULL = not adjudicated (see header).
  applicability       TEXT CHECK(applicability IN (
                        'applies', 'applies_strictly', 'applies_loosely',
                        'context_dependent', 'does_not_apply'
                      )),
  rationale_ref       TEXT REFERENCES decisions(decision_id),

  -- From item_axis_links. Kept under their own names; not merged into applicability.
  mechanism_note      TEXT,
  strength_band       TEXT CHECK(strength_band IN ('full','partial','weak')),
  -- CHECK text preserved VERBATIM from item_axis_links, `OR ... IS NULL` tail and
  -- all. A CHECK passes on NULL anyway, so the tail is redundant -- but
  -- rename_insurance.py compares CHECK TEXT, and paraphrasing a constraint it is
  -- meant to prove survived is how an instrument gets taught to accept drift.
  use_mode            TEXT CHECK(use_mode IN ('independent','assisted','collective')
                                 OR use_mode IS NULL),
  source              TEXT,

  created_at          TEXT,
  created_by_session  TEXT,

  FOREIGN KEY (item_code) REFERENCES items(item_code) ON DELETE CASCADE,

  -- The owner's rule, mechanised: absence in a lens is fine, absence in ALL of them
  -- is not. COALESCE is the whole constraint — "at least one", never "exactly one".
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);

-- Uniqueness has to be an expression index, not a PRIMARY KEY. The old PK was
-- (item_code, population_code, subtype); the lens columns are nullable now, and SQLite
-- treats NULLs as distinct in a UNIQUE index, so a plain unique constraint over them
-- would silently permit duplicates. COALESCE to '' makes the absent lenses comparable.
CREATE UNIQUE INDEX idx_itl_row_identity ON item_taxonomy_links(
  item_code, subtype,
  COALESCE(identity_code,''), COALESCE(icf_code,''),
  COALESCE(needs_code,''),    COALESCE(medical_code,'')
);

CREATE INDEX idx_itl_item     ON item_taxonomy_links(item_code);
CREATE INDEX idx_itl_identity_lens ON item_taxonomy_links(identity_code);
CREATE INDEX idx_itl_icf_lens      ON item_taxonomy_links(icf_code);
CREATE INDEX idx_itl_needs_lens    ON item_taxonomy_links(needs_code);
CREATE INDEX idx_itl_medical_lens  ON item_taxonomy_links(medical_code);

-- ---------------------------------------------------------------------------
-- Fold both sources in. CAST on rationale_ref is a formality: all 372 rows hold NULL.
-- ---------------------------------------------------------------------------
INSERT INTO item_taxonomy_links
  (item_code, identity_code, subtype, applicability, rationale_ref,
   created_at, created_by_session)
SELECT item_code, population_code, subtype, applicability,
       CAST(rationale_ref AS TEXT), created_at, created_by_session
FROM item_population_links;

INSERT INTO item_taxonomy_links
  (item_code, icf_code, mechanism_note, strength_band, use_mode, source,
   created_at, created_by_session)
SELECT item_code, axis_code, mechanism_note, strength_band, use_mode, source,
       created_at, created_by_session
FROM item_axis_links;

DROP TABLE item_population_links;
DROP TABLE item_axis_links;

PRAGMA user_version = 65;
