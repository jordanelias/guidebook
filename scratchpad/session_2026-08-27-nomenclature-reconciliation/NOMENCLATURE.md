# Nomenclature — six stages, the `-item` spine, and the keys that were never there

**Rewritten 2026-08-27** after two owner rulings landed mid-audit and changed the frame:

1. **The pipeline is SIX stages** — *"you research slugs, evidence research, judge evidence,
   synthesize judgments, specify syntheses, and render specifications."* `specification` is a stage
   again, after synthesis. Supersedes the five-stage list of 2026-08-25.
2. **Every stage's hand-off object is `<stage>_items`** — *"we don't need to iterate different words
   for item. we just append '-item'."* And the rename **creates the hand-off keys**, which do not
   exist today.

Both are in `references/project-standards.md`, 2026-08-27, with their quoted wording. The first
supersedes *"`specifications` is a TABLE, not a stage"*; the second supersedes this document's own
first pass, which coined a distinct noun per table (`res_leads`, `evi_extractions`,
`syn_best_practice`). Those are struck.

**Still a proposal. Nothing is renamed, no migration is written, no caller is swept.** Every figure
is measured against `data/guidebook.db` at `user_version` 64.

---

## PART A — The six stages, and the prefix

| # | stage id | prefix | consumes | produces |
|---|---|---|---|---|
| 1 | `research` | `res_` | slugs | **research-items** — a lead: what to go and get |
| 2 | `evidence-collection` | `evi_` | research-items | **evidence-items** — *"the paper says 1200 mm"* |
| 3 | `judgment` | `jud_` | evidence-items | **judgment-items** — is that extraction sound, and how does it weigh |
| 4 | `synthesis` | `syn_` | judgment-items | **synthesis-items** — what the judgments say together |
| 5 | `specification` | `spe_` | synthesis-items | **specification-items** — *therefore: 1200 mm, marked ●* |
| 6 | `render` | `ren_` | specification-items | **render-items** — the surface a reader opens |

**The prefix is derived, not a second vocabulary.** An abbreviation table (`research → res_`) would
be a second home for the stage name — the defect rule 5 exists to stop. So it is computed, exactly as
the display label already is:

```python
def stage_label(stage_id):  return stage_id.replace("-", " ")   # existing, :42
def stage_prefix(stage_id): return stage_id[:3] + "_"           # proposed
```

`res evi jud syn spe ren` — six distinct codes at three characters. **Substrate takes no prefix, and
the absence is the signal:** no prefix means not a stage.

---

## PART B — The spine that is not there

**This is the finding, and it is bigger than the naming.**

Not one foreign key in the schema lands on any stage's hand-off object:

| stage output | inbound FKs | of those, cross-stage |
|---|---:|---:|
| `source_locators` — the lead | **0** | **0** |
| `source_value_extractions` — the extracted value | 1 | **0** |
| `specifications` — the determination | 1 | **0** |
| `bpc_metadata` — the synthesis | **0** | **0** |

The two that have one inbound key have it from inside their own stage
(`extraction_population_links`, `specification_source_links`). **All 41 cross-stage foreign keys
point at substrate vocabularies — `slug` 14, `item_code` 10, `population_code` 7 — or at
`evidence_sources` (6), or sideways. None of them is a hand-off.**

So each stage is joined to the next through a **shared topic label**, not through the thing the
previous stage produced. That is why the pipeline does not walk. The row counts say it is empty
downstream; this says it was never connected.

Two more of the same class:

- **`item_bpc_links` does not reference `bpc_metadata`.** It is named for the synthesis and keys
  `slug` + `item_code`. The synthesis↔item junction never touches the synthesis table.
- **`spec_value_probes` reaches past the extraction to the paper** — `ref_id → evidence_sources`,
  plus `item_code` and `slug`. It never sees `source_value_extractions`.

### What the rename creates — and why the shape flips halfway

Owner ruling: the rename lands the spine, not a follow-up migration. And the owner's cardinality,
stated the same day, decides its shape:

> *"research produces many rows of evidence from one slug. each row of evidence provides one row for
> judgment. one-to-many rows of judgment provide one row for syntheses. one-to-many rows of syntheses
> provide one row for specifications."*

**The pipeline fans OUT through research → evidence → judgment, then fans IN through synthesis →
specification → render.** The evidence multiplies until judgment, then narrows to one answer. The
pivot is between judgment and synthesis — and a hand-off *column* can only express the fan-out half,
so the key changes kind exactly there.

| hand-off | cardinality | shape |
|---|---|---|
| research → evidence | **1:N** — one lead states many parameters | `evi_items.research_item_id` **NOT NULL** |
| evidence → judgment | **1:N** — normally 1:1; see dissent | `jud_items.evidence_item_id` **NOT NULL**, deliberately **not UNIQUE** |
| judgment → synthesis | **N:1** | junction `syn_judgment_links`, both sides NOT NULL, **≥1 per synthesis** |
| synthesis → specification | **N:1** | junction `spe_synthesis_links`, ≥1 per specification |
| specification → render | **N:1** | junction |

**A junction, not a back-pointer.** A nullable `jud_items.synthesis_item_id` filled in later would
lose the NOT NULL guarantee, forbid one judgment feeding two syntheses, and require a **write into a
completed stage** — the thing rule 5 exists to stop. The junction is written by the *downstream*
stage as it creates its own item: *"this synthesis drew on these judgments."* Every stage still
writes only its own tables.

**The evidence → judgment hand-off must not be constrained to 1:1.** `add-population-match`
deliberately omits uniqueness on (ref_id, population) so a dissenting adversarial grade lands as a
second row and divergent grades read as a contest (`DR-2026-08-19` §7). Verified 2026-08-27:
`evidence_population_match` carries no UNIQUE beyond `match_id`; 25 rows across 10 sources. **A
`UNIQUE(evidence_item_id)` on `jud_items` would silently abolish the contest.**

**The schema already half-encodes this.** `bpc_metadata`'s PK is `slug` — one synthesis per topic,
the fan-in. `source_value_extractions` has no UNIQUE on `(ref_id, parameter)` — one paper may state
many parameters, the fan-out. Both cardinalities were already there; only the keys joining them were
missing.

**The window is open and closes on first write.** Judgment, synthesis and specification hold **0
rows** between them; every render table but `rooms` holds 0. A NOT NULL key added now is DDL. Added
after the first determination, it is re-reasoning every row.

### One item table does not exist, and one is not a table at all

| stage | current occupant of `<stage>_items` |
|---|---|
| research | `source_locators` — 875 rows |
| evidence-collection | `source_value_extractions` — 0 rows, **and no writer** |
| **judgment** | **none. `judgment_items` is a NEW table** |
| synthesis | `bpc_metadata` — 0 rows |
| specification | `specifications` — 0 rows |
| **render** | **none as a row** — render surfaces are files under `site/` and `parts/` |

That `judgment_items` is missing is consistent with the sever already on the record: nothing writes
`source_value_extractions`, **and nothing consumes it either**. `judgment_items` is its consumer, and
its absence is why the extraction table could sit specified-in-fourteen-places and unwritten for
seven weeks without anything noticing.

---

## PART C — What crosses a boundary today

41 foreign keys cross a stage boundary; 39 stay inside one. All 41 land on seven columns.

| target | stage | inbound | who points at it |
|---|---|---:|---|
| `slugs.slug` | substrate | **14** | res 6 · evi 3 · jud 1 · syn 3 · ren 1 |
| `items.item_code` | substrate | **10** | res 1 · evi 1 · jud 4 · syn 1 · ren 3 |
| `populations.population_code` | substrate | **7** | evi 2 · jud 2 · syn 1 · ren 2 |
| `evidence_sources.ref_id` | evidence | **6** | res 1 · jud 2 · syn 1 · ren 1 · sub 1 |
| `gaps.gap_id` | research | **2** | evi 1 · jud 1 |
| `search_executions.exec_id` | research | **1** | evi 1 |
| `reasoning_doc_citations.citation_id` | synthesis | **1** | evi 1 |

*(Stage attributions above are from the five-stage map and are re-derived per Part E under the six.)*

### C.1 The `REF-` namespace is two tables sharing one id space with no key between them

875 clue-store rows · 10 admitted · **4 in both** · **6 admitted with no clue-store row** · no foreign
key in either direction. So `REF-00325` does not tell you which stage it lives in — and under the
`-item` ruling, that is precisely what `evidence_items.research_item_id` fixes.

**Eleven ids do not match the format.** `source_locators` holds `REF-VERIFIED-001` … `-012`, which
sort *above* every numbered id, so `MAX(ref_id)` returns `REF-VERIFIED-012`. Any hand-rolled
high-water mark is wrong today; `dbcore.next_ref_id()` is the sanctioned computation.

### C.2 Seven column names for one referent, three of them lying

`ref_id` · `global_ref_id` · `source_ref_id` · `root_ref_id` · `evidence_ref_id` ·
`superseded_by_ref_id` — and **`local_ref_id`**, on three tables, which holds `RAP-01`: a
within-document citation label, not a `REF-` at all.

### C.3 Soft references — named for a key, carrying no key

- **`conflicts.pop_a` / `pop_b`** — free text where a population code belongs. This is the table a
  mobility batch needs most: ramp gradient is the opposed demand between ambulant and wheeled
  movement.
- `conflicts.gap_id` — unkeyed, while `specifications.gap_register_id` is keyed.
- `source_locators.ref_id`, `reference_stubs.ref_id` — unkeyed to `evidence_sources`.
- `source_locators.used_in_bpcs` — a packed reference into synthesis.
- `slugs.serves_axes`, `situations.attaches_axes` — packed lists of demand codes.
- `jurisdiction`, on **9 tables** — no table exists; the vocabulary is an inert enum in
  `schemas/enums.py`.

### C.4 Key kind is inconsistent

Stable text codes (`REF-00325`, `A-01`, `AUT`, `GAP-B01-001`) against bare surrogate integers
(`exec_id`, `candidate_id`, `jv_id`, `specification_id`, `convergence_id`, `extraction_id`).
**The admission edge hangs on an integer** — `search_admissions` keys `(exec_id, ref_id)`, half
stable code and half rowid — and so does the entire output of the judgment stage.

---

## PART D — The grammar

> **`<stage-prefix>` `<subject>` `<kind-suffix>`**, head noun always plural.

**The hand-off object is `<prefix>_items`. Full stop.** Owner ruling: one word, appended; do not coin
a distinct noun for it. Satellite tables inside a stage keep descriptive names, because they are not
the hand-off and nothing outside the stage keys to them.

**Kind suffix** — a closed set, each decided by a test against the schema rather than by taste:

| kind | test | suffix |
|---|---|---|
| **hand-off item** | the object the next stage consumes | `_items` |
| **registry** | PK is a code this table mints, and other tables key to it | *(none)* |
| **junction** | PK composed of ≥2 columns that each identify another thing — an FK, or an external vocabulary with no table | `_links` |
| **run** | a record of an act performed, carrying a timestamp and an outcome | `_runs` |
| **record** | anything else — one row is a thing that happened or was decided | plural noun naming what one row *is* |

*The junction test is written against key columns, not payload, because the payload test fails on
real tables: `term_aliases` has PK `(term_id, alias, language)` and looks composite, but `alias`
**is** the payload, so it is a record and keeps its name.*

---

## PART E — The 66 tables under six stages

**Rows marked ‡ change STAGE, not just name** — those are the ones the six-stage ruling moves, and
each is a first-pass derivation owed confirmation. Rows marked † carry a name fault beyond the
prefix.

### 1 · RESEARCH — `res_`

| current | rows | proposed | note |
|---|---:|---|---|
| `source_locators` | 875 | **`res_items`** † | the hand-off object. "Locator" is wrong twice over — it holds `doi, url, pmid, isbn`, while R3 defines a locator as a within-document pointer, which is what `source_value_extractions`' sixteen `loc_*` columns hold |
| `jurisdictional_values` | 109 | `res_code_leads` † | 109 rows, **0 non-null** in `value_text` and `value_numeric` by the 2026-08-12 REFERENCE-ONLY ruling — the name states the opposite of the ruling |
| `search_candidates` | 60 | `res_candidates` | |
| `search_executions` | 28 | `res_searches` † | the row is a search, not an "execution" |
| `citation_mining` | 10 | `res_mining_runs` † | names the activity, not the row |
| `gaps` | 5 | `res_gaps` | |
| `search_coverage` | 0 | `res_coverage_links` † | it is a junction |
| `search_languages` | 0 | `res_language_links` † | junction |
| `gap_mining` | 0 | `res_gap_mining_runs` † | activity, not row |
| `reference_stubs` | 0 | *delete candidate* † | 0 rows, no writer |

### 2 · EVIDENCE COLLECTION — `evi_`

| current | rows | proposed | note |
|---|---:|---|---|
| `source_value_extractions` | 0 | **`evi_items`** † | the hand-off object — and the sever. Gains `research_item_id NOT NULL` |
| `evidence_source_authors` | 37 | `evi_source_authors` | where the 2026-08-19 fabrication happened |
| `evidence_sources` | 10 | `evi_sources` | the admitted corpus — a satellite, not the hand-off |
| `source_slug_links` | 10 | `evi_slug_links` | |
| `search_admissions` | 10 | `evi_admission_links` † | junction named as a plural noun |
| `extraction_population_links` | 0 | `evi_item_population_links` | follows the item rename |
| `supersession_check` | 0 | `evi_supersession_runs` † | activity, not row |
| `url_verification_runs` | 0 | `evi_url_verification_runs` | already correct |
| `external_root_registry` | 0 | `evi_roots` † | "registry" names the cabinet, not the row |
| `evidence_population_match` | 25 | `jud_population_grades` ‡† | **moves to judgment** — a grade of study-vs-served is a judgment about an admission, not part of collecting it |

### 3 · JUDGMENT — `jud_`

| current | rows | proposed | note |
|---|---:|---|---|
| *(none)* | — | **`jud_items`** ‡ | **NEW TABLE.** Per-extraction determination of soundness and weight. Gains `evidence_item_id NOT NULL`. Column set is owed a design |
| `evidence_population_match` | 25 | `jud_population_grades` ‡ | in from evidence |
| `item_audit_runs` | 0 | `jud_audit_runs` | |
| `conflicts` | 0 | `syn_conflicts` ‡ | **moves to synthesis** — an opposed demand between two populations is a cross-cutting finding, arguable |
| `convergence_assessment` | 0 | `syn_convergence` ‡† | **moves to synthesis** — counting independent roots across extractions is weighing, which is what synthesis now names |
| `specifications` | 0 | `spe_items` ‡ | **moves to specification** |
| `specification_source_links` | 0 | `spe_source_links` ‡ | follows it |
| `spec_value_probes` | 0 | `spe_value_probes` ‡ | **moves to specification** — a probe walks a value to its ceiling, which produces the number |
| `probe_population_links` | 0 | `spe_probe_population_links` ‡ | follows it |

### 4 · SYNTHESIS — `syn_`

| current | rows | proposed | note |
|---|---:|---|---|
| `bpc_metadata` | 0 | **`syn_items`** † | the hand-off object. It is not metadata — it *is* the synthesis. Gains `judgment_item_id NOT NULL` |
| `item_bpc_links` | 0 | `syn_item_links` † | **and it must be re-keyed** — today it references `slugs` and `items`, never `bpc_metadata` |
| `connections` | 0 | `syn_connections` | |
| `connection_targets` | 0 | `syn_connection_links` † | junction |
| `reasoning_doc_citations` | 0 | `syn_citations` | |
| `citation_population_links` | 0 | `syn_citation_population_links` | |
| *in from judgment* | | `syn_conflicts`, `syn_convergence` ‡ | |

### 5 · SPECIFICATION — `spe_`  *(a stage again, 2026-08-27)*

| current | rows | proposed | note |
|---|---:|---|---|
| `specifications` | 0 | **`spe_items`** ‡ | the determination. Keys on the canonical parameter (2026-08-26); gains `synthesis_item_id NOT NULL`; `item_code` and `population_code` leave the identity |
| `specification_source_links` | 0 | `spe_source_links` ‡ | |
| `spec_value_probes` | 0 | `spe_value_probes` ‡ | |
| `probe_population_links` | 0 | `spe_probe_population_links` ‡ | |

### 6 · RENDER — `ren_`

| current | rows | proposed | note |
|---|---:|---|---|
| *(none as a row)* | — | **`ren_items`** | render surfaces are files under `site/` and `parts/`. Whether they gain a row is open — see F.2 |
| `rooms` | 17 | `ren_rooms` | |
| `room_items` | 0 | `ren_room_links` † | junction; and `_items` now means something specific, so it may not stay in this name |
| `case_studies` | 0 | `ren_case_studies` | |
| `case_study_outcomes` | 0 | `ren_case_study_outcomes` | |
| `case_study_populations` | 0 | `ren_case_study_population_links` † | junction |
| `case_study_specs` | 0 | `ren_case_study_links` † | **named for the specification, foreign-keyed to `items`** |
| `case_study_strategies` | 0 | `ren_case_study_strategies` | |
| `economics_entries` | 0 | `ren_economics_entries` | |
| `economics_entry_populations` | 0 | `ren_economics_population_links` † | junction |
| `economics_entry_specs` | 0 | `ren_economics_links` † | **same fault** |

### SUBSTRATE — no prefix

`items` **is retired outright** — the word was the ambiguity, and its rollup role is now served by
whatever `ren_items` becomes. The 10 foreign keys targeting `items.item_code` are re-pointed or
dropped in the same migration.

| current | rows | proposed |
|---|---:|---|
| `term_aliases` | 2382 | unchanged — *proposed as `term_alias_links` on a first pass and withdrawn: `alias` is the payload* |
| `item_population_links` | 372 | re-pointed once `items` retires |
| `data_migrations` | 352 | unchanged — see F.3 |
| `decisions` | 166 | unchanged — see F.3 |
| `item_axis_links` | 158 | `item_demand_links` † — **already ruled, P0.6** |
| `term_item_links` | 147 | re-pointed once `items` retires |
| `slugs` | 106 | unchanged |
| `items` | 93 | **retired** ‡† |
| `terms` | 88 | unchanged |
| `lang_jur_map` | 70 | `language_jurisdiction_links` † |
| `population_axis_map` | 53 | `population_demand_links` † — **P0.6** |
| `access_need_icf` | 43 | `access_need_icf_links` † |
| `populations` | 23 | unchanged |
| `access_need_axis_map` | 21 | `access_need_demand_links` † — **P0.6** |
| `axes` | 17 | `icf_demands` † — **already ruled, P0.6** |
| `access_needs` | 17 | unchanged |
| `weighting_profile` | 5 | `weighting_profiles` † |
| `access_duration` | 3 | `access_durations` † |
| `access_stakes` | 3 | unchanged |
| `life_stage_modifiers` | 2 | unchanged |
| `pipeline_runs` | 1 | unchanged — see F.3 |
| `item_population_elaborations` | 0 | re-pointed; note it points *into* evidence, inverting the substrate model |
| `situations` | 0 | unchanged — 0 rows, delete candidate |

---

## PART F — Open

**F.1 — `judgment_items` needs a column set.** It is the only genuinely new table, and nothing in the
schema prefigures it. Minimum: `evidence_item_id NOT NULL`, a soundness determination, a weight or
tier basis, and the population-match grade moving in from `evidence_population_match`. Owed a design
before the migration.

**F.2 — `render_items` may not be a table.** Render surfaces are files. Either render's hand-off is
the file path (and `ren_items` is a manifest row per published surface), or render is the one stage
whose item lives outside the database. Both are defensible; neither is decided.

**F.3 — Three tables are in no stage and not really substrate.** `decisions` (166),
`data_migrations` (352), `pipeline_runs` (1) record **the project's own acts**, not the book's
content. A `meta_` prefix is arguable; so is leaving them.

**F.4 — Key kind.** Renaming does not fix `exec_id` and `specification_id` being rowids. The rename
migration is the cheapest moment this project will ever have to make them stable codes.

**CLOSED by the six-stage ruling:** the contradiction between the ruled pipeline and
`conceptual-model.md:90` (*"BPC synthesis produces specifications"*). The entity model was right and
the five-stage list was the anomaly.

---

## PART G — Cost

**Now is the cheapest it will ever be.** Judgment, synthesis and specification hold 0 rows between
them; every render table but `rooms` holds 0. The renames and the NOT NULL hand-off keys are DDL.

**The sweep is the cost, not the SQL.** A rename is not done until the callers are swept, and *a view
is a caller, and so is a skill*. Migration 064 exists because 063 swept eight Python readers and six
skills and missed one view. The caller set here:

- **18 views**, 7 of them cross-stage — each one a pointer rule 5 protects
- every `db.py` subcommand, `dbcore`, and the Pydantic models in `schemas/`
- `governance/pipeline-contract.yaml` — which needs a **`specification` stage** added with entry
  conditions and criteria before anything else can reference it
- `tools/pipeline_completeness.py`'s `STAGES`, and the blocking `pipeline_completeness_fresh` gate
- `governance/check-registry.yaml`'s stage-qualified `basis:` references — the exact surface that
  broke `--selftest` on the last stage rename
- the skills, which teach table names in prose
- `scripts/migrations/data_*` — a column a committed data migration INSERTs can never simply be
  dropped, and migration 062's replay-order trap applies to a table rename

**One migration, or not at all.** The bar on piecemeal execution applies with far more force at
sixty-six tables and a new stage than at four tables.

---

## PART H — Appendix: the seven cross-stage views

CLAUDE.md named four. Re-derived 2026-08-27, resolving nested views and quoted table names, there are
**seven** — and one of the four is not among them:

| view | reads |
|---|---|
| `v_source_admission` | evidence_sources, search_admissions, search_executions |
| `v_item_provenance` | + specifications, specification_source_links, items |
| `v_source_reach_all` | + specifications, specification_source_links, items |
| `v_code_floor_only` | specifications, jurisdictional_values — **not in the old list** |
| `v_pending` | specifications, gaps — **not in the old list** |
| `v_item_extractions` | source_value_extractions, evidence_sources, items — **not in the old list** |
| `v_coverage_priority` | search_executions, slugs, lang_jur_map — **not in the old list** |

**`v_divergence` is not cross-stage under the five-stage map** — it reads `specifications` and
`convergence_assessment`, which that map put both in judgment. **Under the six-stage ruling it
becomes cross-stage again**, since `specifications` moves to specification and
`convergence_assessment` to synthesis. The old list reached the right answer by the wrong route, and
this is worth stating plainly rather than quietly banking: *my correction of it was right about the
five-stage map and is overtaken by the ruling that landed hours later.*

This matters beyond bookkeeping: CLAUDE.md protects cross-stage views from deletion because **a
cross-stage view is the pointer**. Under six stages the protected set grows again, and every span
above is owed a re-derivation.

---

## PART I — If we rebuilt from scratch

**Short answer: a new baseline migration, exactly the way `057_baseline_2026-08-12.sql` was made.
Not a hand-built database, and not sixty-six renames.**

### I.1 The mechanism exists and is proven

`scripts/migrations/057_baseline_2026-08-12.sql` is a **full baseline** — complete schema *and* data
in one file, superseding every earlier migration, with the superseded files frozen at
`_archived/scripts/migrations/` (**359 files** live there today; the path is real and the precedent
is closed). `scripts/migrate_db.py --rebuild` replays from a baseline forward, and the blocking
`migration_reproducibility` gate proves the committed database still reproduces. Nothing new has to
be invented.

### I.2 Why a baseline, and not sixty-six renames — in 057's own words

The baseline's header states its reasons, and they are **the same reasons, at sixty-six times the
scale**:

> *"Immutable data migrations pinned RETIRED NAMES forever. Renaming `evidence_cell_state` to
> `specifications` collided with **19 of them** and needed a new ordering mechanism (AFTER_DATA,
> schema 056) purely to work around replay."*

**One table rename collided with nineteen data migrations and required a new mechanism.** There are
**33** data migrations live today, and this proposal renames 66 tables, moves 6 between stages,
creates 5, and retires `items` outright.

And there is a hard technical reason on top of the historical one: **SQLite cannot ALTER a
constraint.** Adding `NOT NULL` and a foreign key to an existing table means create-new → copy →
drop-old → rename. *The incremental path is already a rebuild — done sixty-six times, with
sixty-six chances to miss a caller.* Migration 064 exists because 063 missed exactly one.

One baseline is one DDL file, one data load, and **one caller sweep**.

### I.3 What actually has to move

| stage | rows | at rebuild |
|---|---:|---|
| substrate | 4,122 | carried — vocabularies and crossing maps |
| research | 1,087 | carried — the clue store is 875 of it |
| evidence collection | 92 | carried |
| render | 17 | carried — all of it is `rooms` |
| **judgment** | **0** | **clean-sheet CREATE** |
| **synthesis** | **0** | **clean-sheet CREATE** |
| **specification** | **0** | **clean-sheet CREATE** |
| **total** | **5,318** | |

**That is the whole argument.** The half of the pipeline being redesigned — the three stages whose
grain, keys and names are all changing — contains **no data at all**. There is nothing to migrate
there, only something to build correctly the first time. The 5,318 rows that do exist are 78%
substrate vocabulary, which is the most stable and least contested part of the schema.

### I.4 The order of operations

1. **DDL for all six stages plus substrate**, in dependency order, with the hand-off keys declared
   at creation: two `NOT NULL` columns and three junctions (Part B).
2. **Substrate data first** — everything points into it, so it must exist before any stage row.
   This is where the pending vocabulary changes land (I.5).
3. **Research data** — 1,087 rows, the clue store the batch will drive from.
4. **Evidence data** — 92 rows.
5. **Render data** — 17 rows of `rooms`.
6. **Nothing downstream.** Judgment, synthesis and specification are created empty.
7. The hand-off keys are then **satisfiable by construction**: `evi_items.research_item_id NOT NULL`
   costs nothing because there are 875 leads and 0 extractions, and the three junctions have no rows
   to reconcile because their upstream stages are empty.

### I.5 What must be resolved *in* the baseline, not after it

Each of these is currently a pending change that would otherwise need its own migration and its own
caller sweep. A rebuild absorbs all of them at no extra cost:

| | measured | disposition |
|---|---:|---|
| `MOB` links to fan out to `AMB` / `WHEEL` | 31 → 62 | already ruled, 2026-08-26 |
| cells carrying `AX-` values | 288 | needs the re-mint decision first (§R8 scoping) |
| the `axis` → `demand` rename | 4 tables, 6 columns | already ruled, P0.6 |
| admitted sources with **no clue-store row** | **6** | a provenance hole — resolve or record as legacy |
| malformed `REF-VERIFIED-NNN` ids | **11** | they sort above every numbered id and break `MAX()` |
| surrogate integer keys (`exec_id`, `specification_id`, `extraction_id`, …) | 6 columns | the cheapest moment to make them stable codes (F.4) |
| retired population codes | **0 in the database** | live only in 12 skill files — a prose sweep, not a data one |

### I.6 What a rebuild must not do

- **Do not hand-build the database.** Rule 3 is absolute: migrations only, `emit_data_migration.py`
  → `migrate_db.py`, CI rebuilds and compares. A baseline is a migration; a hand-edited `.db` is not.
- **Do not lose the ledger.** `data_migrations` holds **352 rows** recording the project's own acts.
  057 collapsed the *files* and kept the record; do the same.
- **Do not delete the superseded migrations.** Freeze them at `_archived/scripts/migrations/`, which
  already holds 359 and carries a README explaining what they were.
- **Do not skip the caller sweep because the DDL is clean.** A view is a caller, and so is a skill.
  The sweep is the cost of this change; the SQL is the cheap part.
- **Do not do it before the open questions in Part F are answered** — `judgment_items` has no column
  set, `render_items` may not be a table, and the `AX-` re-mint decision gates the substrate load.

### I.7 The window

Every item in I.4 and I.5 is DDL today and re-reasoning tomorrow. The moment the first determination
is written — one row in `specifications` — the grain change, the key change, the hand-off keys and
the population fan-out all stop being schema edits and become re-derivations of reasoned content.
**The pipeline being empty is not only the problem; right now it is also the opportunity.**

---

## PART J — Re-entrancy is a column, not a table

Three owner questions, 2026-08-27, which turn out to be one question.

### J.1 Citation mining — yes, a mined DOI is just a research-item

> *"if we were to do citation mining, whether it be forwards or backwards, wouldn't that just require
> us to have them processed through research? we would just have a column that notes where they came
> from, right?"*

**Yes, and the schema is already 80% of the way there without anyone having noticed.**
`search_executions` already carries `jurisdiction`, `language` **and `mining_direction`** among its
23 columns. A mining pass *is* a search with a different origin. And a mined DOI is a lead — the same
row-kind as every other lead.

So: `res_items` gains `origin` (`searched` · `mined-backward` · `mined-forward` · `gap-driven` ·
`code-register` · `hand-entered`) and `parent_item_id`, a **self-referential** nullable FK naming the
lead whose source cited this one. The citation graph then walks inside research, which is what mining
is. A root lead has a null parent; a depth-3 mined lead has a chain of three.

**This closes a live defect rather than adding one.** `citation_mining.connections_produced` holds
harvested DOIs and **nothing promotes them into the clue store** — measured earlier, 138 distinct
DOIs harvested and 4 reached `source_locators`; a separate OpenAlex pass found 272 mobility DOIs of
which 256 are in neither store. Under the origin-column model there *is* no promotion step, because
a mined DOI arrives as a research-item. The stranded-yield bug is a consequence of modelling mining
as a table instead of as a provenance.

**And `source_locators` has no origin column today.** Its nearest thing is `recovered_from`, which is
about URL recovery, not discovery. **875 leads and no record of where any of them came from.**

### J.2 Cross-synthesis comparison — yes, same table, new id, provenance columns

> *"if we were to do cross-referential comparisons between syntheses, wouldn't we just run a similar
> synthesis logic and append it to our table, and just have columns that state where it came from and
> assign a new reference ID?"*

**Yes.** A synthesis-of-syntheses is still a synthesis-item: same row-kind, same table, its own id.
What changes is only what it drew on. So `syn_items` gains a `kind` (`primary` from judgments ·
`comparative` from other syntheses) and a second fan-in junction beside the first:

```
syn_judgment_links(synthesis_item_id, judgment_item_id)          -- primary
syn_synthesis_links(synthesis_item_id, source_synthesis_item_id) -- comparative, self-referential
```

Same shape as the hand-off junctions in Part B, and for the same reason: the fan is N:1, so the
pointer is a junction written by the downstream item.

**This is already ratified doctrine, not a new idea.** `governance/pipeline-map.yaml:78` established
2026-08-21: *"these are LAYERS a walk **re-enters**, not phases it passes through. A sequencer must
be re-entrant."* Its `loops:` block at `:160` even names this exact case — *"citation_mining
re-enters admission from an already-admitted source"*. The doctrine was written; the schema never
implemented it, and built tables where it needed columns.

**It also raises a question about `connections`.** *"When writing X, also consider Y"* is a
cross-cutting finding drawn from more than one synthesis — which is precisely a comparative
synthesis-item. Whether `connections` + `connection_targets` survive as their own tables, or become
`syn_items` with `kind='connection'` and their targets in `syn_synthesis_links`, is now an open
question rather than a settled one. Both hold **0 rows**.

### J.3 So why are there sixty-six tables?

> *"in other words, I am really questioning why we have so many tables"*

Because the schema grew **one table per activity and one per attachment**, instead of one per
*kind of row*. Measured 2026-08-27:

| | tables | rows | what they all are |
|---|---:|---:|---|
| **A lead, under four names** | **4** | 1,044 | `source_locators` 875 · `jurisdictional_values` 109 · `search_candidates` 60 · `reference_stubs` 0 — every one is *"a document we might admit, and why we think so"* |
| **An act performed, under four naming conventions** | **7** | 39 | `search_executions` · `citation_mining` · `gap_mining` · `supersession_check` · `url_verification_runs` · `item_audit_runs` · `pipeline_runs` |
| **"X applies to population P"** | **6** | 372 | `item_population_links` 372 · `extraction_population_links` · `probe_population_links` · `citation_population_links` · `case_study_populations` · `economics_entry_populations` — five of the six are empty |

**Seventeen tables doing three things.** And on top of that:

**33 of the 66 tables hold zero rows.** Half the schema has never been used once. That is not
principally a naming problem — it is `CLAUDE.md` §1's burden of proof unpaid: *before adding a table,
state what wrong thing reaches the guidebook if it does not exist.* Thirty-three times, that question
was not asked, or was answered speculatively.

**Two tables are outright derivable and should be deleted, not renamed.** `search_coverage`
(slug × jurisdiction) and `search_languages` (slug × language) restate what `search_executions`
already records — it carries `slug`, `jurisdiction` and `language` on every row. Both hold 0 rows.
**A second home for a fact another table already states is rule 5's exact prohibition**, and here the
first home is more precise, because it is per-query rather than per-slug.

**And one becomes redundant under the `-item` spine.** `search_admissions` is the query→source edge;
once `evi_items.research_item_id` names the lead and the lead names its search, the edge is a join,
not a table.

### J.4 The rule this yields

> **A new table is warranted only when the ROW-KIND is new. A new provenance is a COLUMN. A new
> relationship is a junction. A new activity is a `kind` value on an existing runs table.**

Applied to the three questions: mining yield is a column (`origin`), a comparative synthesis is a
column (`kind`) plus a junction, and the reason there are sixty-six tables is that neither rule was
in force when they were written.

**What that does not license.** Collapsing the six population junctions into one polymorphic
`(stage, item_id, population_code)` table would trade six enforced foreign keys for zero — SQLite
cannot key a polymorphic column. **The uniform name does most of the work without that cost:**
`<prefix>_population_links` on every stage is six tables, but six *predictable* ones, and a reader
who knows the rule never has to look any of them up. Count is not the metric; **derivability is.**
