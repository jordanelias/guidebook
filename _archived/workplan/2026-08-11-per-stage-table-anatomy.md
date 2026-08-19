# 2026-08-11 — What each pipeline stage needs from the database, and what each table is doing

**Status:** ANALYSIS. Nothing executed. Companion to
`workplan/2026-08-11-consolidated-review-and-plan.md`; this is the per-stage view its Part 6
consolidation assumed but never set out.
**Method:** the twelve stages from `2026-08-11-remediation-and-pipeline-anatomy.md` Part 2, crossed
with, for every table: row count, column count, **live writers** and **live readers** measured from
code (excluding `scripts/migrations/`, `scripts/convert/`, `scripts/migrate/`, `scripts/db/`,
`scripts/probes/`, `scripts/tests/`). Table purposes are **my reading of the schema**, not quoted
doctrine — only 24 of 67 tables carry a DDL comment, and most of those are column notes.
**Subject:** `d09f923`. 66 tables · 18 views.

---

## Part 0 — The shape of the answer

Two distinctions do all the work, and conflating them is why "39 tables are empty" has never been
an actionable statement.

**Distinction 1 — a table with no writer is one of two very different things.**

| | | Correct? |
|---|---|---|
| **Seeded vocabulary** | Loaded once by migration; no runtime writer is *supposed* to exist. `populations`, `terms`, `axes`, `slugs`, `lang_jur_map`, `access_*`, `item_axis_links` | **Yes — by design** |
| **Unwritable output** | The pipeline *reads* it, so some stage is meant to fill it, and **no code can** | **No — a hole** |

**13 tables are unwritable outputs**: `source_value_extractions`, `spec_value_probes`,
`reasoning_doc_citations`, `evidence_population_match`, `cell_source_links`, `item_bpc_links`,
`extraction_population_links`, `citation_population_links`, `probe_population_links`,
`search_candidates`, `search_coverage`, `search_languages`, `economics_entries`.

**Distinction 2 — the holes are not spread evenly. They cluster in stages 6–9.**

| Stage | Tables | Unwritable outputs | Verdict |
|---|---|---|---|
| 1 Topic & taxonomy | 20 | 0 | **runs** — the no-writer tables here are all seeded vocabulary |
| 2 Scope & framing | 16 | 2 | runs, degraded |
| 3 Search execution | 11 | 3 | **runs** — but coverage tracking cannot be written |
| 4 Screening & admission | 14 | 3 | **runs** — the admission path works |
| 5 Source verification | 10 | 1 | **runs** — the strongest stage |
| **6 Citation mining** | 10 | **2** | evidence enters, citations cannot be recorded |
| **7 Value extraction** | 21 | **9** | **the epicentre — nothing here can be written** |
| **8 Population matching** | 13 | **6** | the graded match has no writer |
| **9 Cell determination** | 16 | **4** | reads four tables nothing fills |
| 10 Synthesis | 8 | 3 | |
| 11 Adversarial QA | 11 | 2 | |
| 12 Render | 10 | 4 | renders from tables no stage filled |

**The pipeline can gather evidence and cannot turn it into a determination.** Stages 1–5 —
topic, scope, search, admission, verification — have writers and work. Stage 7 has **nine**
unwritable outputs of twenty-one tables. That is the same conclusion PR #93's resolution plan
reached from the other direction ("the pipeline determines a state, never a number"), arrived at
here by counting writers.

---

## Part 1 — Stage by stage

Role key: **SPINE** = carried across four or more stages · **VOCAB** = seeded reference data ·
**PRODUCES** = written by this stage · **READS** = consumed from an earlier stage ·
**⚠ NO WRITER** = read but unwritable.

### Stage 1 — Topic & taxonomy creation
*Establishes what may be researched: the research topics, the disability populations and functional
axes they are organised by, the languages and jurisdictions in scope.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `slugs` | 106 | **SPINE**, VOCAB | The research-topic register. Every downstream row hangs off a slug |
| `populations` | 23 | **SPINE**, VOCAB | Disability population codes, self-referencing for parent/child |
| `items` | 93 | **SPINE**, VOCAB | Design parameters `A-01…K-NN` — the other axis of the evidence grid |
| `axes` | 17 | VOCAB | Functional-demand axes; the non-erasing layer the work-from-axes rule requires |
| `access_needs` | 17 | VOCAB | "The design must…" statements — the obligation layer |
| `population_axis_map` · `access_need_axis_map` · `item_axis_links` | 53 · 21 · 158 | VOCAB | The three maps binding populations, needs and items onto axes |
| `item_population_links` | 372 | **SPINE**, VOCAB | Which populations each item serves — the grid's skeleton |
| `terms` · `term_aliases` · `term_item_links` | 88 · 2,382 · 147 | VOCAB | Multilingual terminology. `term_aliases` is the **largest table in the database** |
| `access_need_icf` | 43 | VOCAB | ICF crosswalk for access needs |
| `lang_jur_map` | 70 | VOCAB | Which languages to search for which jurisdiction |
| `access_duration` · `access_stakes` · `life_stage_modifiers` | 3 · 3 · 2 | VOCAB | Three tiny enumerations. **Fold candidate G3** — the first two are column-for-column identical |
| `population_reclass` | 29 | VOCAB | Retired population codes and what replaced them |
| `jurisdictional_values` | 109 | **SPINE** | Recorded code values. **The only populated quantitative table**, and the one carrying the five false values |
| `situations` | 0 | ⚠ | Designed, migrated, **never written in the project's history**. Cut candidate |

**Health: runs.** Every no-writer table here is seeded vocabulary, which is correct. This is the
stage the clean-room reset deliberately preserved — the frame, in the owner's words.

### Stage 2 — Scope & question framing
*Decides what question a topic is being asked, and against which items, rooms and populations.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `bpc_metadata` | 0 | PRODUCES | Per-slug completion flags: search done, mining done, BPC done. **PK is `slug` — a strict 1:1 extension of `slugs`. Fold candidate G1** |
| `item_bpc_links` | 0 | ⚠ NO WRITER | Which slugs answer which item. **The join that makes an item's evidence findable, and nothing writes it** |
| `item_population_elaborations` | 3 | ⚠ NO WRITER | Per-(item×population) narrative qualifications |
| `rooms` · `room_items` | 17 · 0 | ⚠ NO WRITER | Room typology and its item membership. The 142 room↔item pairs exist in an **archived seed script** |
| `weighting_profile` | 5 | ⚠ NO WRITER | Tier weights per audience/use-pattern. **Named by three stages, touched by no code** — the residual my phase-method test surfaced |
| `gaps` | 0 | PRODUCES | The gap register — what is known to be missing |

**Health: runs, degraded.** Framing can be recorded; the item↔slug join that makes it useful cannot.

### Stage 3 — Search execution
*Runs and logs searches across languages and jurisdictions.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `search_executions` | 0 | **SPINE**, PRODUCES | One row per query: terms, engine, results found/screened/admitted, saturation. **The provenance anchor — hop 5, the strongest hop on the backward walk** |
| `search_admissions` | 0 | PRODUCES | Junction (exec × ref) recording which search admitted which source |
| `search_candidates` | 0 | ⚠ NO WRITER | Things found but not admitted — REHOME/MISC/PENDING. **Contract rule R7 requires this and nothing can write it** |
| `search_coverage` · `search_languages` | 0 · 0 | ⚠ NO WRITER | Per-slug coverage by jurisdiction / by language. **Fold candidate G5** — same table, two axes |
| `citation_mining` · `gap_mining` | 0 | PRODUCES | Mining ledgers, per slug and per gap |

**Health: runs.** Searches can be logged and admissions recorded. **Coverage cannot be tracked**,
so "have we searched enough" has no queryable answer — which is what the four `v_coverage_*` views
were built to report, and three of them read tables with no writer.

### Stage 4 — Screening & admission
*Decides which found sources enter the corpus.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `evidence_sources` | 0 | **SPINE** (10 stages), PRODUCES | The source record. **97 columns — the widest table in the database** |
| `source_slug_links` | 0 | **SPINE**, PRODUCES | Which sources answer which topic, with a local ref id |
| `evidence_population_match` | 0 | ⚠ NO WRITER | **The population-served grade — R13's whole subject.** `target_population` has no FK; three scripts read it as three different types |
| `connections` | 0 | PRODUCES | Cross-item / cross-population connections |

**Health: runs.** The admission path is intact. The **grading** of who a source serves is not.

### Stage 5 — Source verification
*Confirms the source is real, retrievable, and correctly described.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `evidence_source_authors` | 0 | PRODUCES | Normalised authorship. **Migration-exempt** — written by scheduled jobs |
| `url_verification_runs` · `pipeline_runs` | 5 · 6 | PRODUCES | Scheduled-job ledgers, the only tables here with rows |
| `cell_source_links` | 0 | ⚠ NO WRITER | Which sources govern which determination — **hop 2 of the backward walk** |

**Health: the strongest stage.** One unwritable output of ten tables, and the two scheduled
verification channels demonstrably work.

### Stage 6 — Citation mining
*Mines confirmed anchors backward and forward for further sources.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `citation_mining` | 0 | PRODUCES | Per (slug × local ref): backward/forward done, DOI, connections produced. **Fold candidate G2 — same grain as `source_slug_links`, addressed by a different key** |
| `reasoning_doc_citations` | 0 | ⚠ NO WRITER | **The verified claim ledger** — parameter, jurisdiction, claimed value, source section, value/claim match |
| `citation_population_links` | 0 | ⚠ NO WRITER | Population attached to a citation |
| `connection_targets` | 0 | PRODUCES | What a connection points at — **un-keyed text**, not an FK |

**Health: broken outward.** Mining can be *logged*; what it *finds* cannot be recorded as a
verified claim.

### Stage 7 — Value extraction · **the epicentre**
*Turns a verified source into a specific quantity attached to a specific item and population.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `source_value_extractions` | 0 | ⚠ NO WRITER | **49 columns.** The extracted claim: parameter, claimed value and unit, claim type, root type and id, measurement paradigm, plus a 16-column locator block |
| `spec_value_probes` | 0 | ⚠ NO WRITER | Probe walks testing whether a spec value survives a search |
| `reasoning_doc_citations` | 0 | ⚠ NO WRITER | (as stage 6) |
| `evidence_population_match` · `extraction_population_links` | 0 | ⚠ NO WRITER | Who the value is for |
| `case_studies` (+`case_study_specs`) | 0 | ⚠ NO WRITER | 37 columns; a **56 KB, ~26-entry compendium exists in markdown** |
| `economics_entries` (+`economics_entry_specs`) | 0 | ⚠ NO WRITER | Cost/benefit entries. **Contract rule R12 instructs sessions to write here and no tool can** |
| `external_root_registry` | 0 | ⚠ NO WRITER | Root-claim provenance types. Never written in either database. Cut candidate |
| `item_bpc_links` · `cell_source_links` | 0 | ⚠ NO WRITER | (as stages 2 and 5) |
| `jurisdictional_values` | 109 | PRODUCES | The one thing here that **does** have a writer — and the table holding the five false values |

**Health: nine unwritable outputs of twenty-one tables.** This is where evidence becomes number,
and it is the least buildable stage in the pipeline. The 16-column locator block appears here
**three times over** (`source_value_extractions`, `reasoning_doc_citations`,
`jurisdictional_values`) — 48 columns for one concept.

### Stage 8 — Population matching & directness
*Grades how well the studied population matches the population served.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `evidence_population_match` | 0 | ⚠ NO WRITER | `match_grade`, `study_population`, `sample_size` — the R13 grade itself |
| `citation_/extraction_/probe_population_links` | 0 | ⚠ NO WRITER | Three structurally identical link tables, one per parent. **Correctly keyed — do not fold** (§1.3 of the consolidated review) |
| `convergence_assessment` | 0 | PRODUCES | Whether independent sources converge |
| `evidence_cell_state` | 0 | **SPINE**, PRODUCES | The per-cell determination |

**Health: six unwritable outputs of thirteen.** The doctrine's most distinctive commitment —
grading population-of-study against population-served — has **no writer at all**.

### Stage 9 — Cell determination
*Decides, for one item × population cell, what the best practice is and how well evidenced.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `evidence_cell_state` | 0 | **SPINE**, PRODUCES | 27 columns. State (`stated`/`provisional`/`pending`/`not_applicable`), governing refs, gap link. **`assess_cell.py` writes `value_min`/`value_max`/`value_unit` as `None`, unconditionally** |
| `conflicts` | 0 | PRODUCES | Cross-population conflicts at an item |
| `cell_source_links` · `source_value_extractions` · `evidence_population_match` · `item_bpc_links` | 0 | ⚠ NO WRITER | **The determination stage reads four tables nothing fills** |
| `weighting_profile` | 5 | ⚠ NO WRITER | Named here, read by nothing |

**Health: the stage runs and determines a *state*, never a *number*.** That is PR #93's D-A
ruling, visible here as three unconditional `None`s.

### Stage 10 — Synthesis
*Writes the reasoning document — the project's primary deliverable.*

| Table | Rows | Role |
|---|---|---|
| `evidence_cell_state` · `convergence_assessment` · `bpc_metadata` · `items` · `slugs` | | READS |
| `reasoning_doc_citations` · `spec_value_probes` · `item_bpc_links` | 0 | ⚠ NO WRITER |

**Health: reads three unwritable tables.** `references/bpc-reasoning/` holds **one** document.

### Stage 11 — Adversarial QA & audit
*Checks the determination against doctrine and against itself.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `item_audit_runs` | 0 | PRODUCES | Per-item audit ledger |
| `supersession_check` | 0 | PRODUCES | Whether a superseding standard exists |
| `pipeline_runs` | 6 | PRODUCES | Job ledger |

**Health: writable.** This stage has writers; it has nothing to audit.

### Stage 12 — Render
*Emits the pages.*

| Table | Rows | Role | What it is doing |
|---|---|---|---|
| `evidence_cell_state` · `items` · `populations` · `item_population_links` | | READS | The grid and its determinations |
| `rooms` · `room_items` | 17 · 0 | ⚠ NO WRITER | `room_page.py` queries **six tables that do not exist** |
| `weighting_profile` | 5 | ⚠ NO WRITER | Intended to weight the rendered view; read by nothing |

**Health: renders honest "not yet computed" banners**, which is the correct behaviour for an
empty corpus.

---

## Part 2 — What this view adds

**1. It separates two kinds of empty.** 39 empty tables is not one problem. **26 are empty because
the corpus was reset** and will fill when work resumes. **13 are empty because nothing can write
them** and would stay empty through any amount of research. Only the second set is a defect.

**2. It locates the break precisely.** Stages 1–5 work. Stage 7 has nine unwritable outputs.
The pipeline's failure is not diffuse — it is that **evidence cannot become a value**, and the two
stages after it inherit the hole.

**3. It explains why `jurisdictional_values` matters more than its size suggests.** It is the only
populated quantitative table and the only writable output in stage 7. Every determination made
before stage 7 is fixed will rest on it — which is why the five false values in it are the most
consequential data defect in the register, and why the quarantined detector that names them should
be wired first.

**4. It shows which folds are safe, per stage.** G1 (`bpc_metadata`→`slugs`) is stage 2 into stage
1; G2 (`citation_mining`→`source_slug_links`) is stage 6 into stage 4; G3 (the three tiny
vocabularies) is entirely within stage 1; G5 (the coverage pair) is entirely within stage 3. **No
proposed fold crosses a stage boundary in a way that merges two different grains** — which is the
check the two retracted folds failed.

**5. It gives the write-path work a target.** PR #93's Wave 1 fixes the migration mechanism.
This view says what to point it at: **the nine stage-7 outputs, in the order
`source_value_extractions` → `evidence_population_match` → `reasoning_doc_citations`**, because
stage 8 and stage 9 each read all three and nothing else unblocks them.

---

## Part 3 — Limits

- **Table purposes are my reading of the schema.** Only 24 of 67 tables carry a DDL comment and
  most are column notes. Where a purpose here contradicts `governance/conceptual-model.md`, that
  document wins.
- **Stage assignment comes from the anatomy document**, one prior session's work, validated at
  r = 0.73 against code reachability (§1.2 of the consolidated review) with two known residuals —
  `decisions` and `weighting_profile`. A table the anatomy omitted would be missing here.
- **"Live writer" is a static measure** — an `INSERT`/`UPDATE`/`DELETE` against the table name in
  non-legacy code. A writer reached only through dynamic SQL would be missed.
- **Health verdicts are mine**, derived from writer counts, not from executing each stage. The
  only stage anyone has actually walked end to end is the one PR #93's trial walked, and it broke
  four times.
