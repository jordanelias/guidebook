# 2026-08-12 — What is actually in every table, phase by phase

**Status:** OBSERVATIONAL. Nothing here is a proposal and nothing here is evidence.

**CONTENT VALIDITY:** NOT CONTENT — STRUCTURAL INVENTORY, NOT ADMISSIBLE AS EVIDENCE. Every
value reproduced below was read out of the committed database to describe *the state of the
machine*, not to establish a fact about the built environment. No DOI was pre-checked, no
locator re-retrieved, no figure independently verified (R3, R9, R10 unsatisfied by
construction). **Nothing here may be mined, promoted, cited, or treated as a starting point for
a determination.**

**Derived from:** `data/guidebook.db` at `PRAGMA user_version = 53`, read read-only at commit
`fd4c09d` (the PR #95 merge). Every row count, column count and distribution below was measured
by query, not read off a design document. Where this file disagrees with prose elsewhere in the
repository, re-run the query — per `CLAUDE.md`, the DB is canonical and prose counts are stale
everywhere.

**Phase numbering** follows `workplan/2026-08-12-pipeline-phase-state-map.md` (phases 1–12),
which is the corridor-walk trial's own numbering. The twelve-stage numbering used in
`workplan/2026-08-11-per-stage-table-anatomy.md` is the same spine.

---

## 0. The shape of it, in one screen

| | |
|---|---|
| Tables | **67** (66 + `sqlite_sequence`) |
| Views | **18** |
| Tables holding at least one row | **27** (28 with `sqlite_sequence`) |
| Tables holding **zero** rows | **39** |
| Schema version | `user_version = 53` |
| Rows in the whole database | **4,245** |

**The single most important fact about the current data is where the rows are.** Of 4,245 rows,
**3,894 (91.7%) are vocabulary and terminology** — `term_aliases` alone is 2,382. A further 314
are the migration ledger and 157 the decision register. The **entire evidence pipeline —
phases 3 through 10 — holds zero rows in every table.**

```
  PHASE 1   items 93 · populations 23 · slugs 106 · links 372/158     POPULATED
  PHASE 2   bpc_metadata                                          0   EMPTY
  PHASE 3   search_executions                                     0   EMPTY
  PHASE 4   search_admissions                                     0   EMPTY
  PHASE 5   evidence_sources                                      0   EMPTY  ◀── the corpus
  PHASE 6   citation_mining                                       0   EMPTY
  PHASE 7   source_value_extractions                              0   EMPTY
  PHASE 8   evidence_population_match                             0   EMPTY
  PHASE 9   specifications                                   0   EMPTY  ◀── the product
  PHASE 10  reasoning_doc_citations                               0   EMPTY
  PHASE 11  pipeline_runs 6 · url_verification_runs 5             residue of a corpus that no longer exists
  PHASE 12  (reads only)
  ASIDE     jurisdictional_values                               109   the one populated evidence-shaped table
```

This is the expected post-reset state, not a fault: `DR-2026-08-06-clean-room-evidence-reset.md`
cleared the corpus deliberately and preserved the frame. What this inventory adds is **precision
about what "the frame" turned out to contain** — including three things it should not.

---

## Phase 1 — Topic and taxonomy creation

*The skeleton. This is where nearly all the live data is.*

### `items` — 93 rows, 15 columns

The design-parameter vocabulary. `item_code` is the key every downstream table joins on
(14 inbound foreign keys); `name` is free text and is **not** a key.

| Category | Rows | Domain |
|---|---|---|
| A | 19 | acoustics |
| B | 12 | lighting |
| C | 6 | colour, contrast, LRV |
| D | 11 | layout, wayfinding, cognitive legibility |
| E | 14 | circulation, entry, vertical access |
| F | 8 | sensory gradient, air quality, thermal |
| G | 9 | seating, bathrooms, work surfaces |
| H | 5 | controls |
| I | 4 | hardware, kitchen, bathroom operation |
| K | 5 | DeafBlind provision, thermoregulation |

All 93 are `status = 'active'`. Category **J is deliberately absent** (struck by convention).
Numbering is not contiguous: `A-10b` exists, `E-14` does not.

**What the names carry, which is the finding.** Measured directly:

- **28 of 93 names contain a numeric determination** — independently re-derived and matching the
  owner ruling in §0.1 of `workplan/2026-08-12-resolution-plan.md`. Full list at Appendix A.
- **62 of 93 names carry a parenthetical clause**, most of which are scope or condition
  statements (`(Where Full Passenger Lift Not Achievable)`, `(Where VIS Navigation Maintained)`).
- **`bpc_source_slug` is populated on 87 of 93**; six items point at no slug: `A-13`, `A-15`,
  `B-08`, `G-02`, `G-07`, `F-07`. It is a denormalised text pointer duplicating what
  `item_bpc_links` exists to hold — and `item_bpc_links` has **0 rows**, so the keyed
  representation of this fact does not exist anywhere.
- The 87 pointers resolve to only **27 distinct slugs of 106**.
- **`E-15`'s name is truncated mid-parenthetical**: `Changing Places Facility (Height-Adjustable
  Bench, Overhead` — an unclosed bracket, the only unbalanced name in the table. This is a data
  defect no document in `workplan/` currently records.

**PMP columns.** `pmp_delta_min`, `pmp_direction`, `pmp_last_walk_at`, `pmp_empirical_ceiling`,
`pmp_gap_signed` are populated on **4 items only** — `A-02`, `A-08`, `B-01`, `A-18` — all walked
in May 2026. The other 89 are NULL. `pmp_delta_min` is set on just two.

### `populations` — 23 rows, 9 columns

The disability-population vocabulary. Self-referencing `parent_code` — **every row has
`parent_code = NULL` and `is_compound = 0`**, so the hierarchy the column exists to express is
entirely flat in practice. All 23 are `active`.

Categories present: `developmental` (ADHD, AUT, ID, NDV), `sensory` (BLIND, DEAF, DEAFBLIND),
`neurological` (BRAIN, EPI, MOVE, MS, VES), `mobility` (LMB, MOB, SCI), `pain_fatigue` (COM,
PAIN), `cognitive` (DEM), `mental_health` (MH), `general` (ALL, BAR, LPA, TALL).

`ALL` is a scope marker, not a population.

### `slugs` — 106 rows, 11 columns

Research units. **80 ACTIVE · 23 STUB · 3 MERGED.** Spread over 13 topic directories, the
largest being `sensory-environment` (19) and `frameworks-and-methodology` (19).

**`serves_axes` is populated on 1 row of 106** — the axis-routing column is effectively unused.

### `item_population_links` — 372 rows, 7 columns

Which parameters apply to which populations. The densest real relation in the database.

- `applicability`: **366 `applies`**, 6 `context_dependent`.
- `subtype`: 363 empty string; 5 `with-mental-health-comorbidity`, 3
  `with-upper-limb-involvement`, 1 `with-post-concussion-presentation`.
- Coverage is very uneven: DEM 55, BLIND 43, COM 34, MOB 31, BRAIN 30, NDV 30, PAIN 29, SCI 26
  … down to ADHD 1, BAR 1, EPI 1, LPA 1, VES 1.
- **Three populations have zero links: `MOVE`, `ID`, `TALL`.** They exist in the vocabulary and
  are attached to no parameter at all.
- `rationale_ref` is an INTEGER pointing at nothing keyed.

### `item_axis_links` — 158 rows, 8 columns

Parameters against the 17 functional axes. `strength_band` is `full` (95), `partial` (55),
`weak` (8). `use_mode` is NULL on 149 of 158; where set it is `assisted` (9). `source` is a
free-text provenance note — 139 rows say `E3 harvest from item function + FDA audit-briefs`,
11 say `E3 adversarial fix`, and **one row carries a 300-character narrative** describing an
owner directive, a self-review, and two gap IDs (`GAP-300`/`GAP-301`) that no longer resolve.

### `item_bpc_links` — **0 rows**

The FK-valid item↔slug bridge. Empty. The trial wrote one row and the reset cleared it. The
same fact lives, un-keyed, in `items.bpc_source_slug` (87 rows).

---

## Phase 2 — Scope and question framing

### `bpc_metadata` — **0 rows**, 16 columns

Per-slug scope and closure flags: `pico_complete`, `search_complete`, `bpc_complete`,
`citation_mining_complete`, `supersession_check_complete`, `closure_definition_version`.

Two structural facts survive the emptiness:

- **`population` is `TEXT NOT NULL` with no foreign key** — singular and un-keyed, while the
  same concept is FK-constrained in four other tables. A slug covering thirteen populations can
  record one, and can record one that does not exist.
- The emptying of this table is what took `pre_rehab_banner_audit` from RED on 6 slugs to RED on
  68 without any check changing verdict — the DB-side invariants lost their subject.

---

## Phase 3 — Search execution

### `search_executions` — **0 rows**, 23 columns

The best-defended table in the schema and it holds nothing. `STRICT`, with real CHECK
constraints on `target_tier` (1–6), `target_evidence_type` (8-value enum), `target_scope`,
`depth_method` and `saturation_signal`; stores `query_text` verbatim so a stranger can replay
the search; carries `results_found` / `results_screened` / `results_admitted`, `findings_note`,
`deferred_reason`, `harm_finding` and `backfill`.

**The asymmetry to note while it is empty:** the *search* has a tier vocabulary enforced by
CHECK. The *source it admits* (phase 5) does not.

### `search_candidates` — **0 rows**, 14 columns

Off-slug and unadmitted material (R7's REHOME/MISC/PENDING dispositions). Empty.

### `search_coverage` — **0 rows** · `search_languages` — **0 rows**

Both are frozen grids: `scripts/db.py` raises `FrozenGridError` on any write. Live row count is
zero; the archived branch holds 4,960 and 1,558 respectively. Coverage's live mechanism is
`search_executions` plus the `v_coverage_*` views — which is why `v_coverage_priority` returns
7,210 rows (see §5).

---

## Phase 4 — Screening and admission

### `search_admissions` — **0 rows**, 4 columns

`(exec_id, ref_id)` composite key, both foreign. Empty.

The order this table implies is **not** the documented order: `ref_id REFERENCES
evidence_sources(ref_id)`, so admission cannot complete before the source row exists. The real
sequence is 4a → 5 → 4b.

---

## Phase 5 — Source verification

### `evidence_sources` — **0 rows**, **97 columns**

The corpus. The widest table in the schema; currently empty by the clean-room reset.

Column families: authorship (14), publication identity (21), identifiers — DOI/PMID/PMCID/ISBN/
ISSN/URL/handle (10), language and translation (11), classification (`tier`, `evidence_type`,
`jurisdiction`, `scope`, `co1_provenance`, `co1_source_type`), verification state (13 columns
across DOI resolution, URL resolution, metadata integrity, code currency), and processing state
(`data_capture_status`, `citation_mining_status`, `processing_blocked_reason`).

**Where the vocabularies stop being enforced.** CHECK constraints exist on `scope`,
`data_capture_status`, `citation_mining_status`, `processing_blocked_reason`,
`verification_disposition`, `verification_method`, `verification_closure_reason` — and there is
**no CHECK on `tier` and none on `evidence_type`**, the two columns the entire evidence doctrine
turns on. The trial demonstrated `tier = 99` and `evidence_type = 'not-a-real-evidence-type'`
both persisting.

### `evidence_source_authors` — **0 rows**, 14 columns

Exempt from the migration rule (DR-2026-05-28) — written by scheduled jobs. Empty. But
`sqlite_sequence` records its AUTOINCREMENT high-water mark at **1,273**: the reset removed the
rows and left the counter, which is the clearest single measure of how large the pre-reset
corpus was.

---

## Phase 6 — Citation mining

### `citation_mining` — **0 rows**, 13 columns · `gap_mining` — **0 rows**, 12 columns

`citation_mining` records backward/forward mining per `(slug, local_ref_id)`, with
`connections_produced` and `deferred_reason`.

**The un-keyed exit:** `connections_produced` is `TEXT NOT NULL` holding a JSON array of
connection ids with **no foreign key** to `connections`. It is the only link from mining into
the connection layer and it is a string. `connections` and `connection_targets` are themselves
**0 rows**.

### `supersession_check` — **0 rows**, 18 columns

Anchor-supersession checks with `search_strategy_record`, `candidates_returned/reviewed`,
`superseding_ref_ids`, `refinement_dimension`. Empty.

---

## Phase 7 — Value extraction

*The stage the resolution plan identifies as the hole: nine of the fourteen unwritable outputs
are here.*

### `source_value_extractions` — **0 rows**, **49 columns**

The most ambitious table in the schema, and a terminus: nothing downstream reads it.

- Claim: `claimed_value`, `claimed_unit`, `claim_type`, `claim_text`, `parameter`,
  `parameter_canonical`.
- **`measurement_paradigm`** — 9 values including `swept_path_dynamic`, `static_turning_circle`,
  `static_clearance`, `anthropometric_percentile`, `participatory_spatial`, `stated_unmeasured`.
- **`device_class`** — manual / power / scooter / bariatric / walker / mixed.
- Provenance: `root_id`, `root_type`, `root_ref_id`, `echo_of`, `contested`,
  `root_classification_basis`, `root_population_note`.
- **16 `loc_*` locator columns** from migration 053.
- Process: `extraction_method`, `extraction_status`, `promoted_to_rdc_id`.

`sqlite_sequence` records its high-water mark at **8** — the trial's nine extractions, minus
one, then cleared.

### The other stage-7 tables, all **0 rows**

| Table | Cols | Note |
|---|---|---|
| `spec_value_probes` | 21 | The Progressive Measurement Protocol's output. The protocol exists, is unrun and is unwired. |
| `extraction_population_links` | 5 | Junction; no writer. |
| `specification_source_links` | 5 | The junction three renderers read and `assess_cell.py` never writes. |
| `item_bpc_links` | 6 | (also phase 1) |
| `case_studies` | 37 | Plus `case_study_outcomes`, `_populations`, `_specs`, `_strategies` — all 0. |
| `economics_entries` | 25 | Plus `economics_entry_populations`, `_specs` — all 0. R12 instructs sessions to write this table and no tool can. |
| `probe_population_links` | 5 | Junction on `spec_value_probes`. |

---

## Phase 8 — Population matching and directness

### `evidence_population_match` — **0 rows**, 11 columns

`match_grade` ∈ EXACT / PARTIAL / PROXY / MISMATCH, with `study_population`, `sample_size`,
`mismatch_note`, and FKs to `evidence_sources` and `gaps`.

**The broken leg, visible in the DDL while empty:** `target_population` is `TEXT NOT NULL` with
**no foreign key**. Its consumer matches it with a regex. A malformed or umbrella value reads as
*absent* rather than *malformed* — it fails silently, in the direction of under-reporting.

---

## Phase 9 — Cell determination

### `specifications` — **0 rows**, 27 columns

The product of the entire pipeline: one row per `(item_code, population_code)`, UNIQUE on the
pair. **Zero determinations exist.**

Columns: `state` (stated/provisional/pending/not_applicable), `design_scale`, `tier_basis`,
`governing_refs` (JSON), `rule_version`, `derivation_sha`, `code_floor_only`,
`regulatory_stratum_only`, `has_unverified_sources`, `all_sources_disqualified`,
`falsification_condition`, `not_applicable_rationale`, `gap_register_id`, the three confidence
dimension columns — and **`value_min`, `value_max`, `value_unit`**.

Two facts about those last three: they are the only place a determined number could live, and
the only writer in the repository sets them to `None, None, None` unconditionally on every path.
There is **no column anywhere recording the doctrine SHA a judgement was made under** — leg 4 of
the reset DR's four-leg promise.

**The potential grid is 93 × 23 = 2,139 cells. 372 of those pairs are asserted applicable.
0 are determined.**

### `convergence_assessment` — **0 rows**, 13 columns · `gaps` — **0 rows**, 16 columns

`gaps` being empty is load-bearing: the gap-id allocator returns `GAP-1` on an empty table and
the schema requires `^GAP-\d{3,4}$`, so the determination engine aborts on its first write. The
empty table is what breaks the writer.

`gaps` carries `falsification_condition`, `confidence_interval`, `shift_conditions`,
`named_dissenter`, `mining_addressability` — the honesty apparatus, unpopulated.

---

## Phase 10 — Synthesis

### `reasoning_doc_citations` — **0 rows**, 34 columns

The only DB representation of the primary deliverable. Carries `claim_type`, `claimed_value`,
`claimed_unit`, `value_match`, `claim_match`, `paywall_purchase_candidate`, and the **same 16
`loc_*` locator columns** as `source_value_extractions` and `jurisdictional_values`.

### `citation_population_links` — **0 rows**, 5 columns

**The file chain and the DB chain never meet.** `references/bpc/` and
`references/bpc-reasoning/` hold markdown; neither validator opens the database. A reasoning doc
can name a BPC that does not exist, and no registered check reads a cell-state row as a
precondition for committing either.

---

## Phase 11 — Adversarial QA and audit

*The only phase-11/12 tables with rows — and their rows describe a corpus that no longer
exists.*

### `pipeline_runs` — 6 rows, 29 columns

DOI-resolution runs, all from **2026-05-12**, all `run_by_session = 'resolve-dois-action'`.
Five of six resolved nothing; one resolved 2. Their counters record the corpus as it then was:
`doi_before = 222–225`, `verified_before = 283–286`.

### `url_verification_runs` — 5 rows, 16 columns

URL-verification runs from **2026-05-13** and **2026-05-15**. Cumulative `verified_before` →
`verified_after` climbs 361 → 410 across the four working runs; 51 URLs verified, 4 dead.

**Both tables are historical residue.** They report activity against 400+ sources in a table
that now holds zero. `pipeline_runs` is on the migration-exempt list; `url_verification_runs`
is **not**, and is still written by the bi-weekly `verify-urls.yml` cron — which is why widening
the reproducibility gate without an exemption ruling first would manufacture a permanently-red
blocking check.

### `item_audit_runs` — **0 rows**, 12 columns

Per-item audit pipeline state. Empty.

---

## Phase 12 — Render

Writes files, not rows. Reads `items`, `item_population_links`, `item_bpc_links`,
`bpc_metadata`, `specifications`, `specification_source_links` — **five of those six are empty**,
so every generated page currently renders from `items` and `item_population_links` alone, behind
"not yet computed" banners.

---

## The evidence-shaped table that is not in any phase

### `jurisdictional_values` — 109 rows, 32 columns

**The only populated table holding anything resembling evidence**, and it is not written by any
pipeline stage — it was seeded by a one-shot importer and is shadowed by YAML files under
`data/jurisdictional_values/`.

| Measure | Value |
|---|---|
| Rows | 109 across **20 of 93 items** |
| Jurisdictions | 12 — DE 20, GB 20, US 20, AU 18, ISO 13, FR 5, NO 5, EU 4, CA/CH/JP/SG 1 each |
| `evidence_tier` | **6 on every row** |
| `is_code_minimum` | **1 on every row** |
| `value_numeric` populated | 75 of 109 |
| `unit` populated | 87 of 109 |
| **`value_numeric` set with `unit` NULL** | **8** |
| `locator_scheme` populated | **0 of 109** |
| any `loc_*` column populated | **0 of 109** |

Three findings follow directly from that table:

1. **The entire holding is regulatory stratum.** 109 rows, tier 6, code minimum, no exceptions.
   Under `governance/tier-system.md` this material is walled off from full-strength anchoring —
   so the one populated evidence table cannot, by doctrine, anchor a best-practice claim above
   the flagged weak band.
2. **Migration 053's locator hierarchy has zero adoption.** All 16 `loc_*` columns and
   `locator_scheme` are NULL on all 109 rows; locators live in the free-text `source_section`
   field instead (`A.1`–`A.20`). The hierarchy is unenforced *and* unused.
3. **The eight numeric-without-unit rows are the extractor-failure class**, and the detector
   built to catch value defects filters exactly those rows out. Enumerated:

| jv | item / juris | numeric | drawn from |
|---|---|---|---|
| 14 | E-07 / US | 0.42 | `Threshold: ≥0.42` (a real DCOF value; unit genuinely dimensionless) |
| 15 | E-07 / GB | 36.0 | `PTV ≥36 wet` (a real PTV value; dimensionless) |
| 16 | E-07 / DE | 9.0 | **`R9–R13`** — a slip-resistance *class ordinal* |
| 17 | E-07 / AU | 3.0 | **`P3–P5`** — a class ordinal |
| 96 | A-10 / US | 50.0 | `≥50 occupants` (a real trigger threshold) |
| 100 | A-10 / FR | 50.0 | `≥50 seats` (a real trigger threshold) |
| 106 | E-15 / GB | 2021.0 | **the year in `Building Regs 2021`**, on a row whose text states `Min Area: ≥12m²` |
| 107 | E-15 / US | 1.0 | **`Supplement 1 (2024)`** — an edition ordinal |

Four are genuinely dimensionless quantities; four are not quantities at all.

---

## Vocabulary and taxonomy tables outside the phase spine

| Table | Rows | What is in it |
|---|---|---|
| `terms` | 88 | Canonical terminology across 18 domains — `functional_axis` 17, `methodology` 13, `circulation` 11, `medical` 8. |
| `term_aliases` | **2,382** | The multilingual search vocabulary: **15 languages** (en 415, de 191, es 171, fr 170, fi 160, da/ko 157, zh 155, ja 150, nl 140, sv 134, no 132, it 121, pt 114, id 15). Types: SYNONYM 1,119 · TRANSLATION 996 · NARROWER 146 · BROADER 70 · DOMAIN 49 · DEPRECATED 2. **The single largest body of data in the database.** |
| `term_item_links` | 147 | 49 terms against 69 items. `population` NULL on all 147. |
| `axes` | 17 | The functional axes. `coverage_status`: ESTABLISHED 10, STUB 5, PARTIAL 2. Every row carries a `mechanism` and a `falsification_condition`. |
| `access_needs` | 17 | Four families — perceiving, operating, communicating, pacing, environment_safety. Every row carries a full `design_obligation` sentence. **`typical_stakes` is NULL on 16 of 17** — only `A-TRIGGER` is graded (`safety-critical`). |
| `access_stakes` | 3 | `safety-critical` / `exclusion` / `friction` — the vocabulary the 16 NULLs would draw on. |
| `access_duration` | 3 | `permanent` / `temporary` / `situational`. |
| `life_stage_modifiers` | 2 | `SEN`, `CHD` — explicitly orthogonal to populations. |
| `access_need_axis_map` | 21 | need↔axis: primary 10, spans 6, partial 5. |
| `access_need_icf` | 43 | ICF anchors — 38 `e` (environmental), 3 `d`, 2 `b`; all `confirmed`. |
| `population_axis_map` | 53 | population↔axis: SECONDARY 27, PRIMARY 17, ALIAS 7, SITUATIONAL 2. |
| `population_reclass` | 29 | A **proposal table**, not a live taxonomy. **14 of its 29 `population_code` values do not exist in `populations`** (CFS, CHD, DBL, EXH, LCOV, MCAS, NEU, OAD, OFS, PCS, POTS, SENS, UPL, VIS) — it has no FK, and it is where the axis-alias and split proposals live. |
| `lang_jur_map` | 70 | language↔jurisdiction: 50 PRIMARY, 20 SECONDARY. **This is the closest thing to the two frame vocabularies (languages, jurisdictions) the reset DR requires and neither of which has a canonical table.** |
| `rooms` | 17 | Room typology R-ASM…R-WC, all active, `category` NULL on all 17. **Not named in the reset DR's frame enumeration** — off-frame. |
| `room_items` | **0** | The junction that would make `rooms` useful. Empty, so `rooms` connects to nothing. |

---

## Governance, operations and off-frame tables

| Table | Rows | What is in it |
|---|---|---|
| `decisions` | **157** | The governance decision register, imported from YAML on 2026-08-04. D-DOCT 43 · D-METH 55 · D-OP 32 · D-SCHEMA 22 · D-PRES 5. Delegation: **DG-NON 115**, DG-REVIEW 32, DG-AUTO 10. Status: ACTIVE 155, PROPOSED 1, PROVISIONAL 1. Dates 2026-03-15 → 2026-08-04. **Still dual-stored** — four scripts read the YAML. |
| `data_migrations` | **314** | The migration ledger, 2026-05-11 → 2026-08-06, across 15 sessions. The 15 most recent all carry `notes = 'rebuilt by runner'` and share one `applied_at`, because the ledger is regenerated on rebuild. |
| `db_meta` | 2 | `created_at = 2026-05-08 03:41`, `project = jordanelias/guidebook`. The retired `schema_version` key is gone; `PRAGMA user_version` is the only version marker. |
| `sqlite_sequence` | 3 | AUTOINCREMENT high-water marks that **survived the reset**: `evidence_source_authors` **1,273**, `source_value_extractions` 8, `item_population_elaborations` 7. The best available fossil record of the pre-reset corpus. |
| `weighting_profile` | 5 | Audience × use-pattern render weightings — designer, disabled_person ×2, policymaker, ot. Each carries a JSON `tier_weights` foreground list. **No code reads this table**, while `governance/evidence-architecture.md` I3 binds renders "under any weighting profile". |
| `item_population_elaborations` | **3** | Manual-vs-power wheelchair and upper-limb variants for E-12, G-08, G-09. Columns `variant_distinction`, `spec_variant_a`, `spec_variant_b` hold **prose specifications** — this is synthesis output, the exact class the clean-room reset existed to clear, and it survived. `evidence_ref_id` is NULL on all three. |
| `situations` | **0** | The native Co-1 entity — lived-experience accounts with `account_language`, `translation_ref`, `co1_status`. Empty live *and* archived. Named in five governance documents. |
| `external_root_registry` | **0** | Root-provenance registry. Empty live and archived. |
| `conflicts` | **0** | Population-vs-population conflict register (`pop_a`, `pop_b`, `resolution`, `gap_id`). Empty. |

---

## The 18 views

Seventeen return **0 rows**, because they sit on empty tables. One does not:

- **`v_coverage_priority` — 7,210 rows.** It is a cross-product over the populated skeleton
  (slugs × jurisdictions or similar), so it produces a large prioritisation surface out of
  vocabulary alone. It has **no reader in the codebase.**
- `v_best_practice` (0) is the view supplying `strength_band` to the renderer.
- `v_value_independence` (0) is cited by the pipeline contract as its H1 mechanism.
- `v_root_id_conflicts` (0) queries `source_value_extractions` only.
- The remaining fourteen — `v_code_floor_only`, `v_coverage_branch`, `v_coverage_jurisdiction`,
  `v_coverage_language`, `v_divergence`, `v_item_extractions`, `v_item_provenance`, `v_pending`,
  `v_pmp_latest_walk`, `v_registry_duplicate_descriptions`, `v_source_admission`,
  `v_source_reach`, `v_source_reach_all`, `v_unregistered_roots` — all 0.

---

## What this inventory establishes

1. **The pipeline is empty from phase 2 to phase 10 inclusive.** Not thin — empty. Every
   statement about pipeline behaviour is currently a statement about code, not about data.
2. **The frame is not neutral scaffolding.** 28 item names carry determinations, 3 rows of
   `item_population_elaborations` carry prose specifications, and 109 `jurisdictional_values`
   rows carry code minima. **All three are answers, sitting in a layer the reset preserved on
   the understanding that it held only questions.**
3. **The one populated evidence table is entirely tier 6.** By the project's own tier doctrine
   it cannot anchor a full-strength claim, so the visible content and the admissible content do
   not overlap at all.
4. **Enforcement is inverted where it matters most.** The empty `search_executions` has CHECK
   constraints on every enum; the empty `evidence_sources` has none on `tier` or
   `evidence_type`; the empty `evidence_population_match` has no FK on the population it
   matches. The best-defended table holds nothing and the least-defended one is the corpus.
5. **Three counters outlived their rows** — `sqlite_sequence` at 1,273 authors, and the two
   operations tables reporting 410 verified URLs and 225 resolved DOIs against a corpus of zero.
6. **Two defects here are not recorded anywhere in `workplan/`:** `items.E-15`'s truncated name,
   and the total non-adoption of the `loc_*` locator hierarchy in the only table that has rows
   to put in it.

---

## Appendix A — The 28 item names carrying a numeric determination

Re-derived at `fd4c09d` by `SELECT item_code, name FROM items WHERE name REGEXP '\d'`.

`A-02` Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces ·
`A-03` Acoustic Door (STC ≥35) at All Sensitive Space Boundaries ·
`A-06` Fabric Wall Panels (NRC ≥0.70) at Acoustic Reflection Points ·
`A-08` HVAC Noise Control (NC-25 Maximum in Sensitive Spaces) ·
`A-10b` RT60 for Hydrotherapy and Pool Environments ·
`A-14` Double-Leaf Partition (STC ≥50) for Sensitive Adjacencies ·
`A-16` Sensory Room / Quiet Room Provision (≥8 m², one per floor or per 500 m² GFA) ·
`A-18` RT60 in Occupied Learning and Listening Spaces ·
`B-01` Circadian Lighting (≥150 EML Minimum at Eye Level in Daytime Spaces) ·
`B-04` Flicker-Free LED Luminaires (IEEE 1789-2015 Compliant) ·
`B-05` Gradual Lighting Transition Zones (≥5 m at All Major Illuminance Changes) ·
`B-06` Individual Dimming Control (≥300 Lux Range) ·
`B-08` Matte, Low-Reflectance Floor Finishes (≤30 Gloss Units) ·
`B-11` Warm Colour Temperature for Evening (≤2700 K After 19:00) ·
`C-04` LRV Contrast (≥30 at All Critical Junctions) ·
`D-11` Safe Accessible Garden (Loop Path, Secured Perimeter, Seating Every 20 m) ·
`E-01` Accessible Lift (1400×1100 mm Car, All Floors Served) ·
`E-03` Ramp Gradient (≤1:20 — MS Fatigue and Temporal Accessibility) ·
`E-04` Accessible Parking (3600 mm Width, Covered, Closest to Entry) ·
`E-05` Weather Protection at Entry (Covered Canopy Minimum 3000×2000 mm) ·
`E-07` Slip Resistance (PTV ≥36 Wet Throughout All Circulation and Entry) ·
`E-08` Corridor Clear Width (≥1200 mm Minimum on All Primary Routes) ·
`E-09` Tactile Walking Surface Indicators (ISO 23599:2019) ·
`F-04` Air Quality (MERV 13+ Filtration, Low-VOC Specification, Thermal Stability) ·
`G-05` Adjustable-Height Work Surfaces and Desks (650--870 mm AFF Range) ·
`G-06` Reception Counter (Accessible Height Section — 760--860 mm AFF) ·
`H-01` All Controls at Accessible Height (400--1100 mm AFF, One-Fist Operable) ·
`I-01` Hardware Throughout (Lever, D-Pull, One-Hand Operable, ≤22 N)

**Three are arguably citations rather than determinations** — `A-10b`/`A-18` (`RT60` is the name
of a metric), `B-04` (`IEEE 1789-2015` is a standard designation), `E-09` (`ISO 23599:2019`
likewise). The permitted-set question is open.

---

## Appendix B — Every table, its phase, and its row count

| Phase | Table | Rows | Cols |
|---|---|---|---|
| 1 | `items` | 93 | 15 |
| 1 | `populations` | 23 | 9 |
| 1 | `slugs` | 106 | 11 |
| 1 | `item_population_links` | 372 | 7 |
| 1 | `item_axis_links` | 158 | 8 |
| 1 | `item_bpc_links` | **0** | 6 |
| 2 | `bpc_metadata` | **0** | 16 |
| 3 | `search_executions` | **0** | 23 |
| 3 | `search_candidates` | **0** | 14 |
| 3 | `search_coverage` | **0** | 11 |
| 3 | `search_languages` | **0** | 9 |
| 4 | `search_admissions` | **0** | 4 |
| 5 | `evidence_sources` | **0** | 97 |
| 5 | `evidence_source_authors` | **0** | 14 |
| 5 | `source_slug_links` | **0** | 8 |
| 6 | `citation_mining` | **0** | 13 |
| 6 | `gap_mining` | **0** | 12 |
| 6 | `supersession_check` | **0** | 18 |
| 6 | `connections` | **0** | 13 |
| 6 | `connection_targets` | **0** | 2 |
| 7 | `source_value_extractions` | **0** | 49 |
| 7 | `extraction_population_links` | **0** | 5 |
| 7 | `spec_value_probes` | **0** | 21 |
| 7 | `probe_population_links` | **0** | 5 |
| 7 | `case_studies` | **0** | 37 |
| 7 | `case_study_outcomes` | **0** | 6 |
| 7 | `case_study_populations` | **0** | 2 |
| 7 | `case_study_specs` | **0** | 2 |
| 7 | `case_study_strategies` | **0** | 3 |
| 7 | `economics_entries` | **0** | 25 |
| 7 | `economics_entry_populations` | **0** | 2 |
| 7 | `economics_entry_specs` | **0** | 2 |
| 8 | `evidence_population_match` | **0** | 11 |
| 9 | `specifications` | **0** | 27 |
| 9 | `specification_source_links` | **0** | 5 |
| 9 | `convergence_assessment` | **0** | 13 |
| 9 | `gaps` | **0** | 16 |
| 10 | `reasoning_doc_citations` | **0** | 34 |
| 10 | `citation_population_links` | **0** | 5 |
| 11 | `pipeline_runs` | 6 | 29 |
| 11 | `url_verification_runs` | 5 | 16 |
| 11 | `item_audit_runs` | **0** | 12 |
| — | `jurisdictional_values` | 109 | 32 |
| — | `terms` | 88 | 9 |
| — | `term_aliases` | 2,382 | 10 |
| — | `term_item_links` | 147 | 8 |
| — | `axes` | 17 | 11 |
| — | `access_needs` | 17 | 9 |
| — | `access_stakes` | 3 | 4 |
| — | `access_duration` | 3 | 4 |
| — | `life_stage_modifiers` | 2 | 5 |
| — | `access_need_axis_map` | 21 | 6 |
| — | `access_need_icf` | 43 | 7 |
| — | `population_axis_map` | 53 | 6 |
| — | `population_reclass` | 29 | 13 |
| — | `lang_jur_map` | 70 | 6 |
| — | `rooms` | 17 | 10 |
| — | `room_items` | **0** | 6 |
| — | `item_population_elaborations` | 3 | 10 |
| — | `weighting_profile` | 5 | 4 |
| — | `conflicts` | **0** | 14 |
| — | `situations` | **0** | 12 |
| — | `external_root_registry` | **0** | 8 |
| — | `decisions` | 157 | 22 |
| — | `data_migrations` | 314 | 5 |
| — | `db_meta` | 2 | 2 |
| — | `sqlite_sequence` | 3 | 2 |

**67 tables · 4,245 rows · 27 populated · 39 empty.**

---

*Measured 2026-08-11 against `data/guidebook.db` at `user_version = 53`, commit `fd4c09d`, by
read-only query. Counts are volatile by construction — re-derive before acting on any row.*
