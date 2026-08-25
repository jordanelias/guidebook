# The pipeline, and every table derived to its stage

**The pipeline** — owner ruling 2026-08-25, superseding the 2026-08-24 list:

> **`research → evidence collection → judgment → synthesis → render`**

**Substrate is not a stage.** The vocabularies and registries are the layer all five stages point
*into*. Rule 5 — never write the same fact into a second table; point, don't copy — is unusable
without knowing which stage a table belongs to, which is why this map is a stopper rather than
orientation.

**Derived, not read.** `CLAUDE.md` requires it: *"Derive the table-to-stage assignment; do not read
one out of a document. The six-bucket assignment in the 2026-08-24 stage-discipline audit is
agent-authored, predates this ruling, and must be re-derived."* The test applied to each of the 66
tables is one question: **whose own work does this record?** Not what it keys on, and not who reads
it — a table read by four stages still belongs to the one that *writes* it.

Counts are live at 2026-08-25.

---

## RESEARCH — 10 tables
*What was searched, screened and mined, plus the clue store.*

| Table | Rows | What it means for the book |
|---|---:|---|
| `search_executions` | 28 | **Every query, verbatim, before screening.** The project's claim to have looked. A zero-yield row is a completed unit of work — it is how the book can say "we looked and found nothing" rather than staying silent about a gap. |
| `search_candidates` | 60 | Screened but unresolved leads. A staged description is a **hypothesis** (R15) — it must be re-described from the source on resolution, or a guess hardens into fact. 55 of 60 sit `PENDING-VERIFICATION`. |
| `search_coverage` | 0 | Per-slug jurisdiction coverage. Empty means no slug can yet say which jurisdictions it has and has not searched. |
| `search_languages` | 0 | Per-slug language coverage. The multilingual claim (R5: non-English peer-reviewed work is academic, not grey) has no record behind it. |
| `citation_mining` | 10 | Backward and forward mining per anchor (R2). Its `connections_produced` holds the harvested DOIs — **and nothing promotes them into the clue store**, so the yield is stranded. |
| `gap_mining` | 0 | Gap-driven mining attempts. |
| `gaps` | 5 | Open questions the book cannot yet answer. **A gap is a first-class finding**, not a to-do: "no Tier-1 quantified threshold exists for autistic users" is a publishable result. |
| `source_locators` | 875 | **The clue store** — "a lead index of identifiers, not evidence". The largest table in the pipeline and the batch's intended driver. |
| `reference_stubs` | 0 | |
| `jurisdictional_values` | 109 | **Contested assignment — see §Judgement calls.** Code/standard leads: which document to go and get, never what it says (REFERENCE-ONLY ruling, 2026-08-12). `value_text` and `value_numeric` are 0 non-null of 109, by ruling. |

## EVIDENCE COLLECTION — 10 tables
*What was admitted, its identity, verification and extraction.*

| Table | Rows | What it means for the book |
|---|---:|---|
| `evidence_sources` | 10 | **The admitted corpus.** Every claim in the book must trace here. 10 rows, all on one non-mobility slug. |
| `evidence_source_authors` | 37 | Authors, derived rather than stored beside the source (migration 063). **This is where the 2026-08-19 fabrication happened** — invented co-authors, including deletion of autistic community co-authors from a Co-1 paper whose warrant *is* their co-authorship. |
| `source_slug_links` | 10 | Which topic a source was admitted under. |
| `search_admissions` | 10 | **The admission edge** — which query produced which source. Without it, a source has no provenance chain back to the act of looking. |
| `evidence_population_match` | 25 | R13 grading: population-of-study vs population-served. **No match row = silently claiming they are the same.** Deliberately allows two rows per (ref, population) so a dissenting grade lands as a contest. |
| `source_value_extractions` | 0 | **The join between "we found a paper" and "the paper says 1200 mm".** Zero writers. This is where the walk severs. |
| `extraction_population_links` | 0 | |
| `supersession_check` | 0 | Is this anchor still the current best? Records **literature currency**, not judgment staleness. |
| `url_verification_runs` | 0 | R10 re-retrieval evidence. |
| `external_root_registry` | 0 | Root identity for independence counting. Unregistered roots silently under-count convergence. |

## JUDGMENT — 7 tables
*Determination. Writes `specifications`.*

| Table | Rows | What it means for the book |
|---|---:|---|
| `specifications` | 0 | **The determination** — the book's actual answer to a question. Currently keyed `UNIQUE(item_code, population_code)`; that grain is under challenge (see `GRAIN-QUESTION.md`). No CLI writer exists. |
| `specification_source_links` | 0 | Which sources govern a determination. **Without it a determination renders with no visible sources** — an assertion, not evidence. |
| `convergence_assessment` | 0 | Whether independent evidence streams agree. Doctrine requires counting **independent values**, never documents. |
| `spec_value_probes` | 0 | Progressive-measurement probes — walking a value to its empirical ceiling. |
| `probe_population_links` | 0 | |
| `conflicts` | 0 | **Where two populations' needs are incompatible in the same space.** For a mobility batch this is the central table: ramp gradient is an opposed demand. |
| `item_audit_runs` | 0 | |

## SYNTHESIS — 6 tables
*Weighing, convergence, cross-slug findings.*

| Table | Rows | What it means for the book |
|---|---:|---|
| `bpc_metadata` | 0 | Best-practice synthesis per slug. **Opus-floor authored** — and that floor has no mechanical enforcement anywhere. |
| `item_bpc_links` | 0 | |
| `connections` | 0 | **Cross-item interactions** — "when writing X, also consider Y". This is where the book stops being a list and becomes a thinking tool. `opus_reviewed` on it is hardcoded 0 and never read. |
| `connection_targets` | 0 | |
| `reasoning_doc_citations` | 0 | Claim-level verification of a reasoning document's prose against the corpus. **Empty, while the one real reasoning doc cites 8 unadmitted leads.** |
| `citation_population_links` | 0 | |

## RENDER — 10 tables
*Book surfaces and the content tables behind them.*

| Table | Rows | What it means for the book |
|---|---:|---|
| `rooms` | 17 | Room-type surfaces — how a reader actually enters the book ("I am designing a bathroom"). |
| `room_items` | 0 | Which provisions belong to which room. **Empty, so no room page can list its provisions.** |
| `case_studies` + `_outcomes`, `_populations`, `_specs`, `_strategies` | 0 | Part-12 built examples. R12 routes case studies here rather than leaving them in prose. |
| `economics_entries` + `_populations`, `_specs` | 0 | Part-13 cost/benefit. The advocacy delta — what an architect shows a client. |

## SUBSTRATE — 23 tables
*Not a stage. The layer all five stages point into.*

**Vocabularies:** `items` 93 · `populations` 23 · `slugs` 106 · `terms` 88 · `term_aliases` 2382 ·
`access_needs` 17 · `axes` 17 (→ `icf_demands`) · `access_duration` 3 · `access_stakes` 3 ·
`life_stage_modifiers` 2 · `weighting_profile` 5 · `situations` 0

**Crossing maps** *(the three `*_axis_*` names below are physical only, pending the §R8 rename to `*_demand_*`)*: `access_need_icf` 43 · `access_need_axis_map` 21 · `item_axis_links` 158 ·
`population_axis_map` 53 · `item_population_links` 372 · `item_population_elaborations` 0 ·
`term_item_links` 147 · `lang_jur_map` 70

**Registries of the project's own acts:** `decisions` 166 · `data_migrations` 352 · `pipeline_runs` 1

*`term_aliases` at 2,382 rows is the largest table in the repository — the multilingual apparatus
is by far the most built thing here, and it serves a corpus of 10 sources.*

---

## Judgement calls, declared rather than hidden

Three assignments are arguable. Recording them so the next reader can overturn them:

1. **`jurisdictional_values` → research, not render.** It keys on `item_code`, which reads as
   render, and my own earlier census put it there. But by the test — *whose work does it record?* —
   it is a **lead index**: which code document to go and get, with every value column null by
   ruling. That is functionally identical to `source_locators`, which is uncontroversially research.
   Its `item_code` key is not evidence of render membership; it is an instance of the grain problem
   in `GRAIN-QUESTION.md`.
2. **`weighting_profile` → substrate, not synthesis.** It is a registry of profiles that synthesis
   *reads*. A table read by a stage belongs to the stage that *writes* it.
3. **`supersession_check` → evidence collection, not synthesis.** Its CHECK vocabulary
   (`current_best`, `superseded_by`, `refined_by`) is about a **source's** standing in the
   literature, not about a synthesis's staleness. This corrects an assignment I got wrong earlier
   today.

## What the shape shows

| Stage | Tables | Rows |
|---|---:|---:|
| research | 10 | 1,087 |
| evidence collection | 10 | 82 |
| **judgment** | **7** | **0** |
| **synthesis** | **6** | **0** |
| render | 10 | 17 |
| substrate | 23 | 3,861 |

**Thirteen tables across judgment and synthesis, all empty.** The apparatus for deciding and
weighing is fully specified and has never once been used. And the substrate outweighs the entire
pipeline by three to one — the project has built the vocabularies to describe the book far ahead of
the evidence to fill it.

## One thing the derivation surfaced, bearing directly on the grain question

`source_value_extractions` — the evidence stage's last table — carries **all four** of
`ref_id`, `slug`, `population_code`, `item_code`.

`specifications` — the judgment stage's output — carries **two**, and makes them a `UNIQUE` key.

So the extraction layer is *already* multimodal in exactly the way the owner describes, and the
determination layer narrows to `(item × population)` at the moment of judgment. **The grain
collapses one stage downstream of where the evidence supports it.** Whatever replaces the current
key, the extraction table shows the wider frame is already expressible in this schema.
