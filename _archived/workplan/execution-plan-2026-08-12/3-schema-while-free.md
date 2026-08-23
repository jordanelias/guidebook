# Wave 3 — Free today, expensive after the first content batch

**Read `00-holistic-execution-plan.md` first.** **Preconditions: L1 exists; Wave 1 has landed.**

Every table this wave changes is empty today. **But empty is not neutral** — W1.4 exists because
the reset moved a counter to a value its own schema forbids and broke the only determination
writer, invisibly.

**Schema state:** `PRAGMA user_version = 53`; highest migration on disk is
`scripts/migrations/053_locator_hierarchy.sql` (ends `PRAGMA user_version = 53;` at `:122`).
**Next free number is 054.** All numbers below are proposals — re-derive at execution.

**Every schema migration is forward-only, bumps `user_version`, and must be mirrored in
`schemas/*.py` in the same commit.** Drift is a CI-caught bug.

**Target order:** `source_value_extractions` → `evidence_population_match` →
`reasoning_doc_citations`. Stages 8 and 9 each read all three.

**Proposed numbering:** 054 = W3.9 · 055 = W3.2 · 056 = W3.3 · 057 = W3.4 · 058 = W3.1.

**The grid, for scale:** 93 items × 23 populations = 2,139 potential cells; 372 pairs asserted
applicable; **0 determined**.

---

## W3.9 — One locator representation. **Candidate B. Do this first (054).**

### Objective
Unify the locator block by **definition** rather than by table, add the scheme registry, and
guard the three physical blocks against drift.

### Re-derived
All three tables carry the identical 16-column block in identical order — `locator_scheme` plus
15 `loc_*` columns: `loc_division, loc_part, loc_section, loc_subsection, loc_paragraph,
loc_clause, loc_subclause`, their seven `_end` twins, and `loc_note`. Totals:
`jurisdictional_values` 16/32 · `source_value_extractions` 16/49 · `reasoning_doc_citations`
16/34. **The Pydantic side is triplicated verbatim too** — `jurisdictional_value.py:60-75`,
`source_value_extraction.py:108-123`, `reasoning_doc_citation.py:109-124`.

**Two facts the plan does not state:**
1. **Migration 053 enumerates zero scheme families.** `locator_scheme` is bare TEXT — no CHECK,
   no registry.
2. **Zero adoption in the only table with rows.** `SELECT DISTINCT locator_scheme FROM
   jurisdictional_values` → one row, `NULL`, ×109. Locators live in free-text `source_section`
   (`A.1`–`A.20`) and packed `standard_name`.

The "~24 families" figure is the **2026-08-09 document's own count**
(`2026-08-09-locator-hierarchy-and-enforcement-probes.md:51-55` — twelve leading-token families
cover 97 of 109 rows: DIN 19 · AS/NZS 16 · ADA 15 · BS 15 · …; edition-splitting gives *"roughly
24"*; its C5 correction at `:399` records "twelve" as the refuted claim). **Size the registry
from that enumeration.** A registry sized for 12 fails closed on real input.

### Why Candidate A fails
A `locators` table keyed `(owner_kind, owner_id)` has a **polymorphic `owner_id`, so it cannot
be constrained by a foreign key** — the identical construction the §2.1 retraction refused. It
also forfeits three addable `locator_scheme` FKs. The `v_locators` view below has exactly that
polymorphic shape, which is fine for a *view* and fatal for a *table*.

### Migration `054_locator_schemes.sql`

```sql
-- 054_locator_schemes.sql
-- W3.9 Candidate B: the scheme registry + enforcement. The three loc_* blocks
-- stay physically in place (identical meaning is NOT assumed from identical
-- shape — the W7 fold test); their DEFINITION is unified in schemas/ and
-- guarded by scripts/audit/locator_block_identity.py.
CREATE TABLE locator_schemes (
    scheme              TEXT PRIMARY KEY,   -- 'ada-2010', 'iso', 'din', 'bs', 'as-nzs', 'tek17', …
    family_label        TEXT NOT NULL,
    top_level           TEXT NOT NULL CHECK (top_level IN
                          ('division','part','section','subsection',
                           'paragraph','clause','subclause')),
    render_sigil        TEXT,               -- '§' / 'clause ' / 'Art. '
    render_example      TEXT,               -- '§404.2.5' / 'clause 12.3' / '12-6(2)'
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT
);

-- FK enforcement WITHOUT rebuilding three tables (SQLite cannot ADD CONSTRAINT
-- to an existing column): BEFORE-triggers, one pair per table.
CREATE TRIGGER trg_jv_locator_scheme_ins BEFORE INSERT ON jurisdictional_values
WHEN NEW.locator_scheme IS NOT NULL
     AND NOT EXISTS (SELECT 1 FROM locator_schemes s WHERE s.scheme = NEW.locator_scheme)
BEGIN SELECT RAISE(ABORT, 'unknown locator_scheme (register it in locator_schemes first)'); END;
CREATE TRIGGER trg_jv_locator_scheme_upd BEFORE UPDATE OF locator_scheme ON jurisdictional_values
WHEN NEW.locator_scheme IS NOT NULL
     AND NOT EXISTS (SELECT 1 FROM locator_schemes s WHERE s.scheme = NEW.locator_scheme)
BEGIN SELECT RAISE(ABORT, 'unknown locator_scheme (register it in locator_schemes first)'); END;
-- identical _ins/_upd pairs for source_value_extractions (trg_sve_locator_scheme_*)
-- and reasoning_doc_citations (trg_rdc_locator_scheme_*); six triggers total.

CREATE VIEW v_locators AS
SELECT 'jurisdictional_values' AS owner_table, CAST(jv_id AS TEXT) AS owner_pk,
       item_code, NULL AS ref_id, locator_scheme,
       loc_division, loc_part, loc_section, loc_subsection, loc_paragraph,
       loc_clause, loc_subclause, loc_division_end, loc_part_end,
       loc_section_end, loc_subsection_end, loc_paragraph_end,
       loc_clause_end, loc_subclause_end, loc_note
  FROM jurisdictional_values
UNION ALL
SELECT 'source_value_extractions', CAST(extraction_id AS TEXT),
       item_code, ref_id, locator_scheme, /* …same 15… */
       loc_division, loc_part, loc_section, loc_subsection, loc_paragraph,
       loc_clause, loc_subclause, loc_division_end, loc_part_end,
       loc_section_end, loc_subsection_end, loc_paragraph_end,
       loc_clause_end, loc_subclause_end, loc_note
  FROM source_value_extractions
UNION ALL
SELECT 'reasoning_doc_citations', CAST(citation_id AS TEXT),
       NULL, source_ref_id, locator_scheme, /* …same 15… */
       loc_division, loc_part, loc_section, loc_subsection, loc_paragraph,
       loc_clause, loc_subclause, loc_division_end, loc_part_end,
       loc_section_end, loc_subsection_end, loc_paragraph_end,
       loc_clause_end, loc_subclause_end, loc_note
  FROM reasoning_doc_citations;

PRAGMA user_version = 54;
```

### Then
1. **New `schemas/locator.py`** with a `LocatorBlock(BaseModel)` carrying the 16 optional fields;
   **delete** the block from the three models and inherit it. Add a `LocatorScheme` model.
   Register both in `validate_pydantic_schemas`' model→table map (`:84` area).
2. **New `scripts/audit/locator_block_identity.py`**: `PRAGMA table_info` on all three; extract
   the contiguous block from `locator_scheme` to `loc_note`; assert name + order + declared-type
   identity across the three **and** against `LocatorBlock.model_fields` order. Register
   advisory in the `schema` battery, printing `EXAMINED: 3 tables / 48 columns`.
3. **Seed migration** (data migration) for the ~24 scheme rows.

### Net
**−0 columns, +1 table, +1 view; 6 definitional copies (3 DDL + 3 Pydantic) → 1.** This revises
the plan's "−32 columns" and is the correct accounting.

### Verification
Rebuild reproduces; a scratch insert with `locator_scheme='not-a-scheme'` ABORTs in all three
tables; `SELECT COUNT(*) FROM v_locators` = 109, all with NULL locators — honestly.

### Risk
**Unifying a representation no row uses is cheap, but must not be mistaken for the judgment work
migration 053's own header defers** (`:44-58`: the `/`-splitting of 21 multi-doc rows with three
named false positives, and the re-key of `UNIQUE (item_code, jurisdiction, standard_name)`).
Those stay owner-gated (W9.3 items 6 and 8).

---

## W3.2 — Split `evidence_population_match.target_population` (055)

### The archived evidence — **reachable, and both claims verified**

The archived DB at `4fc6304` is readable locally via `git cat-file blob 4fc6304:data/guidebook.db`
piped into `sqlite3.Connection.deserialize()`. **Practical note: the blob's header carries WAL
format bytes — flip bytes 18/19 from 2→1 in the in-memory copy or `deserialize` fails with
"unable to open database file".**

- **64 rows** in archived `evidence_population_match` — **confirmed**.
- **30 distinct** `target_population` values — **confirmed**.
- **22 of 30 are prose**, not parseable as codes, including the plan's exemplar
  `'Hardware operating force threshold for UPL/PAIN populations including RA'` — **confirmed**.
  That value is **not even a population**, and must classify to note-only with a NULL code.

**Do not import the rows.** FK to an empty `evidence_sources`, and `DR-2026-08-06 §4.1`:
*"Research resuming does not restore these rows."* The 30 values become a `(code, note)`
worksheet committed as a DR appendix — 8 map to bare codes (`ALL`, `AUT`, `BLIND`, `COM`, `DEM`,
`MOB`, `NDV`, `VES`); 22 need judgment.

### The DDL is richer than every prior document records
The live table also carries a legacy un-FK'd **`source_ref TEXT NOT NULL`** beside `ref_id`, plus
`gap_id` and `mismatch_note`, and `match_id` is **TEXT**, not an integer PK. The rebuild must
decide `source_ref`'s fate — **recommend drop**, after sweeping `rg -n "source_ref\b"`.

### Migration `055_population_match_split.sql`
Rebuild (0 rows, so free): new table with `target_population_code TEXT REFERENCES
populations(population_code)` (nullable) and `target_population_note TEXT NOT NULL` (R13 needs
richness on the served side), `ref_id NOT NULL REFERENCES evidence_sources(ref_id)`, `match_grade`
CHECK on EXACT/PARTIAL/PROXY/MISMATCH, `gap_id` FK; `INSERT … SELECT` (0 rows, kept for form);
`DROP`; `RENAME`; `PRAGMA user_version = 55;`

### Two consequences
1. **No Pydantic model exists for this table** — `schemas/` has no `evidence_population_match.py`
   (only doc-references in `population_links.py:10` and `directness.py:21,89,102`). Either add
   one or record the absence in the ledger; do not leave it implicit.
2. **The consumer must change.** `assess_cell.py:168-183` (`population_match()`) matches
   `\b{population}\b` against free text. Post-split it reads `target_population_code = ?` first,
   falling back to the note only with a logged NOT_ASSESSED-style flag — the same G2 conservatism,
   now keyed.

### Verification
Inserting `target_population_code='NOT-A-REAL-POPULATION'` into a scratch copy now **fails the
FK** — closing the probe class the trial demonstrated.

### Risk
FK enforcement depends on `PRAGMA foreign_keys` at the connection. **W3.2's guarantees are only
as good as Wave 1's fix.**

---

## W3.3 — Doctrine binding on `specifications` (056)

**Leg 4 of DR-2026-08-06's four-leg promise. Legs 1–3 have columns (`rule_version`,
`derivation_sha`, `governing_refs`); leg 4 has nothing** — there is no doctrine-SHA column
anywhere in the cell's 27 columns.

```sql
-- 056_cell_doctrine_binding.sql
ALTER TABLE specifications ADD COLUMN doctrine_sha TEXT
  CHECK (doctrine_sha IS NULL OR (
    length(doctrine_sha) = 7 AND NOT doctrine_sha GLOB '*[^0-9a-f]*'));
PRAGMA user_version = 56;
```

Mirror in `schemas/evidence_state.py` reusing `attestation.schema.json:14`'s pattern verbatim.
Stamp in `assess_cell.py`: a `DOCTRINE_SHA` constant derived at run time via
`git rev-parse HEAD:governance/mission-and-epistemics.md`, with a `--doctrine-sha` override for
fixtures; add to `cols` (`:563-569`) and `vals` (`:550-562`), **widening the placeholder count at
`:571` from 26 to 27.**

**Choose this over widening `attestation.schema.json`** — that file is CODEOWNERS-protected and
the change alters attestation semantics repo-wide.

**Note:** GLOB is case-sensitive, so uppercase hex fails. Intended (git emits lowercase), but say
so. And a doctrine amendment mid-batch produces mixed SHAs across cells — **that is the feature**;
staleness becomes queryable.

---

## W3.4 — `co1 ⇒ tier=1` enforced in the database (057)

### Pre-flight, run against the archived DB
`SELECT COUNT(*) FROM evidence_sources WHERE evidence_type='co1' AND tier<>1` → **0**, across 29
co1 rows. **No historical data would ever have violated it.**

### Take the trigger, not the rebuild
`evidence_sources` is **97 columns with 7 embedded CHECKs**. A rebuild reproducing 97 columns
byte-for-byte is the highest-risk edit available for a guarantee a six-line trigger provides
identically.

```sql
-- 057_co1_tier_guard.sql
CREATE TRIGGER trg_es_co1_tier_ins BEFORE INSERT ON evidence_sources
WHEN NEW.evidence_type = 'co1' AND (NEW.tier IS NULL OR NEW.tier <> 1)
BEGIN SELECT RAISE(ABORT,
  'co1 sources must be tier=1 (co-primary; tier-system.md §1, T-03)'); END;

CREATE TRIGGER trg_es_co1_tier_upd BEFORE UPDATE OF evidence_type, tier ON evidence_sources
WHEN NEW.evidence_type = 'co1' AND (NEW.tier IS NULL OR NEW.tier <> 1)
BEGIN SELECT RAISE(ABORT,
  'co1 sources must be tier=1 (co-primary; tier-system.md §1, T-03)'); END;

PRAGMA user_version = 57;
```

### Two things to record, not fix here
1. **The dormant validator.** `scripts/validate_evidence_state.py:76-121`
   (`validate_source_co1_fields`) scans `data/sources/*.yaml`, **which does not exist**, and its
   own comment at `:97-102` admits **two dormant bugs** — an undefined `r` NameError on the
   UNVERIFIED path, and two D-0157-retired status values that can no longer occur. Its repair or
   retirement is a separate ledgered act.
2. **The boundary.** This guard does **not** close the trial's `tier=99` /
   `evidence_type='not-a-real-evidence-type'` hole. `evidence_sources` has 7 CHECKs and **none on
   `tier` or `evidence_type`**. Full enum CHECKs are a D-SCHEMA enum decision with four rival
   vocabularies (`tooling-register.md` §4.1) — **raise it, do not smuggle it in.**

---

## W3.1 — Implement the derived-value triangle (058)

**Gated on D-B.** Enum addition is D-SCHEMA (Change-Order gated).

1. Doctrine: extend `governance/tier-system.md` §5 after `:73` — ▲ derived/full · ◭ derived/partial
   · △ derived/weak; shape = derivation, fill = strength per D-B; cross-reference §8's band table.
2. Migration `058_derived_value_marker.sql`: add `synthesis_method_indicator TEXT CHECK (… IN
   ('direct','inferred','consensus'))` and `inference_basis TEXT` to `specifications`, plus
   **BEFORE INSERT/UPDATE triggers enforcing that `inferred` requires a non-empty
   `inference_basis`** (SQLite cannot add a table-level CHECK).
   **The column name is load-bearing** — `synthesis_method` is reserved by
   `armature_v4_resolutions.md:104` for a different vocabulary. Put that in the migration comment.
3. Mirror in `schemas/evidence_state.py` with a `field_validator` and a `model_validator` for the
   pairing. **Record, do not silently fix, the pre-existing drift:** the model already lacks
   `value_min/value_max/value_unit`, `tier_basis` and `governing_refs`, which
   `validate_pydantic_schemas` counts.
4. Renderer: emit the marker at **cell** level from `v_best_practice.strength_band` (live:
   `'weak'` iff `regulatory_stratum_only=1`, else `'anchored'`) × the indicator.
   **Do not reuse the mockup's `sym-warn` ▲ class** (D-B's collision finding).

**Risk:** `armature_v4_resolutions.md:110` attaches the vocabulary to *Specification*, which has
no canonical table (`evidence_state.py:18-21` keys the cell on `items.item_code` precisely because
the spec layer is legacy-only). **The DR must state that the cell is the carrying surface until a
spec layer exists.**

---

## W3.5 — `assess_cell.py` must write `specification_source_links`

**Insertion point re-verified exactly as the plan states: after `:573`, before `:575`.**
`:570-573` is the cell INSERT and its `sql_lines.append`; `:575` begins `report.append`. Both
`specification_id` and `det["governing_refs"]` are in scope between them.

```python
        # W3.5: the junction IS the readable edge (spec_page.py reads it, never
        # the JSON). role='governing' is the only value the DDL CHECK admits.
        for ref in det["governing_refs"]:
            csl = (specification_id, ref, "governing", STAMP, SESSION)
            conn.execute(
                "INSERT INTO specification_source_links "
                "(specification_id, ref_id, role, created_at, created_by_session) "
                "VALUES (?,?,?,?,?)", csl)
            sql_lines.append(
                "INSERT INTO specification_source_links "
                "(specification_id, ref_id, role, created_at, created_by_session) VALUES ("
                + ", ".join(q(v) for v in csl) + ");")
```

**DDL constraint confirmed:** `role TEXT NOT NULL DEFAULT 'governing' CHECK (role IN
('governing'))`, PK `(specification_id, ref_id)`. `det["governing_refs"]` is distinct by construction
(built by `sorted(...)` at `:314`/`:358`/`:378`) — assert uniqueness anyway.

**One decision to record:** `supporting_refs` (`:321`) cannot junction — the CHECK admits only
`'governing'`. Record that as deliberate, not overlooked.

**Why it matters:** the trial's first determination carried 7 governing refs and 0 junction rows,
so `spec_page.py:217-223` rendered *"records no governing sources … treat it as unevidenced."*
**The honesty mechanism misreports.**

---

## W3.6 — Render the value, the marker band, and the gap link

**Gated on W3.1 and D-A.** The gap-link half is ungated and overlaps W5.7 — cross-reference the
ledger entries rather than fixing half of it in each wave.

`spec_page.py:73-77` selects exactly `specification_id, population_code, state, tier_basis,
code_floor_only, falsification_condition, regulatory_stratum_only, confidence_synthesis_basis,
has_unverified_sources, all_sources_disqualified` — **omitting `value_min`, `value_max`,
`value_unit` and `gap_register_id`.**

**The per-source marker absence is deliberate and doctrinally argued** — `citation()`'s docstring
at `:131-139`: *a marker qualifies a claim sentence, not a source.* Leave it. The marker belongs
on the cell row.

**One addition beyond the plan:** when `value_min`/`value_max` are present and `value_unit` is
NULL, render a **loud defect marker, not a bare number** — W0.3's NULL-unit lesson applied at the
render layer.

**Correction to the phase-map:** its render section says *"the value (no column exists for it)"*.
The columns exist; the SELECT omits them. The plan's W3.6 states it correctly.

---

## W3.7 — Populate `access_needs.typical_stakes`

**Owner review mandatory.** These are sixteen judgment acts, and Appendix D calls them the item
most likely to change under review.

**Verified:** 17 rows, `typical_stakes` NULL on **16**; only `A-TRIGGER` graded
(`safety-critical`). `access_stakes` holds exactly three: `safety-critical` ("Harm if
violated."), `exclusion` ("Locks people out."), `friction` ("Degrades the experience.").
**A-SIZE and A-REACH — the two that reach corridor width — are both NULL.**

### The sixteen proposals — for owner ruling, not determinations

| need_code | proposed | contestable alternate |
|---|---|---|
| A-NOSIGHT | exclusion | — |
| A-NOSOUND | exclusion | safety-critical (alarms) |
| A-TACTILE | exclusion | — |
| A-STABLE | safety-critical (falls) | — |
| A-NOSPEECH | exclusion | — |
| A-PLAIN | exclusion | friction |
| A-REACH | exclusion | safety-critical (egress) |
| A-PRECISION | friction | exclusion |
| A-AT | exclusion | possibly out of built-env scope |
| A-SELFCARE | exclusion | safety-critical (dignity/harm) |
| A-LOWLOAD | friction | — |
| A-TIME | exclusion | friction |
| A-EFFORT | exclusion | — |
| A-STIMULUS | friction | safety-critical (migraine/PTSD harm) |
| A-CALM | friction | — |
| A-SIZE | exclusion | safety-critical (weight-rating failure = harm) |

**Data migration, never schema**, sixteen guarded statements:
```sql
UPDATE access_needs SET typical_stakes='exclusion'
 WHERE need_code='A-REACH' AND typical_stakes IS NULL;
```
The `IS NULL` guard makes re-application a no-op — the W5.1 idempotence pattern.

**Two gaps to record:** there is **no FK** from `typical_stakes` to `access_stakes` (a W3.4-class
trigger candidate), and **no Pydantic model exists for `access_needs`**.

**Risk:** single-value grading flattens context — A-STIMULUS is friction in an office and
safety-critical for PTSD triggers. Keep the column single-valued and the nuance in `notes`, per
the existing A-TRIGGER pattern.

---

## W3.8 — The six stage-7 outputs: writer or declaration

**Writer sweep re-run: `spec_value_probes`, `item_bpc_links`, `extraction_population_links`,
`case_studies`, `economics_entries`, `specification_source_links` — zero writers, all six.**
(`specification_source_links` is discharged by W3.5.)

**The urgency is a contract conflict:** `governance/research-contract.yaml:186-193` (R12)
instructs sessions to route *"Case studies → case_studies. Economics → economics_entries"* — and
**no tool can write either.** *(The plan's correction is confirmed: the contract is R1–**R15**,
stated at `:1`, with R15 at `:215`.)*

Add a criterion to `pipeline-contract.yaml` declaring the five hand-authored, and per-table:

- `spec_value_probes` → **the writer is the PMP harness. Wire it (W9.5), don't declare it.**
- `item_bpc_links` → a backfill writer from `items.bpc_source_slug` is nearly free; the
  duplication is live (87 pointers, 0 keyed rows).
- The other three → declare hand-authored now, revisit post-D-A.

**Risk:** declaring `economics_entries` hand-authored without amending R12's wording leaves the
contract instructing an impossible act.

---

## Re-derivation notes

| Claim | Status | Evidence |
|---|---|---|
| Three identical 16-column locator blocks | **CONFIRMED** | 16/32, 16/49, 16/34; Pydantic triplicated too |
| Locator families in migration 053 | **REVISED — zero enumerated** | bare TEXT, no CHECK |
| Locator adoption in data | **NEW — zero of 109** | all `locator_scheme` NULL |
| "~24 families" | **CONFIRMED as sourced** | the 2026-08-09 doc's own count, `:51-55`, `:399` |
| W3.2: 64 archived rows, 30 distinct, 22 prose | **CONFIRMED** | archived DB read in-memory |
| `evidence_population_match` DDL | **REVISED** | also carries `source_ref`, `gap_id`, `mismatch_note`; `match_id` is TEXT |
| co1 rows with tier≠1 in the archive | **CONFIRMED — zero** | 29 co1 rows, all tier 1 |
| `validate_source_co1_fields` scans a non-existent path and admits two bugs | **CONFIRMED** | `:76-121`, comment `:97-102` |
| W3.5 insertion point "after 573, before 575" | **CONFIRMED exactly** | — |
| `specification_source_links.role` CHECK admits only `'governing'` | **CONFIRMED** | so `supporting_refs` cannot junction |
| W3.6's four omissions | **CONFIRMED** | `spec_page.py:73-77` |
| 16 of 17 `typical_stakes` NULL; three ratified values | **CONFIRMED** | full dump |
| Six stage-7 outputs have no writer | **CONFIRMED** | writer sweep |
| Research contract is R1–R15 | **CONFIRMED** | `research-contract.yaml:1`, R15 at `:215` |
