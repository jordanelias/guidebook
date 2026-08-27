# Nomenclature — stages, tables, keys, and what crosses a boundary

**A proposal, and nothing here is executed.** No table is renamed, no migration is written, no
caller is swept. The §R8 precedent sets the bar: renaming **four** tables is already owner-gated,
scoped at 312 tracked files, and forbidden to attempt piecemeal. This document covers **66**.
It exists so the rename can be ruled on once, as a grammar, instead of table by table forever.

Every figure below is measured against `data/guidebook.db` at `user_version` 64, 2026-08-27.

---

## 0. Three name-spaces that have to agree, and currently do not

| | lives in | who derives it |
|---|---|---|
| **stage names** | `governance/pipeline-contract.yaml` `stages[].id` | `stage_label()` derives the display form |
| **table names** | the schema itself | nothing — each was named by whoever wrote its migration |
| **key names** | column names | nothing |

The stage layer has a one-home rule and a derivation. The other two have neither, which is the
whole complaint: **a table's name does not tell you its stage, and its column names do not tell you
which stage's key they point at.**

---

## PART A — Stage names

### A.1 The five ids, and the one-home rule that already governs them

`governance/pipeline-contract.yaml` is the single home. `tools/pipeline_completeness.py:37`:

```python
STAGES = ["research", "evidence-collection", "judgment", "synthesis", "render"]

def stage_label(stage_id: str) -> str:      # :42-43
    return stage_id.replace("-", " ")
```

| contract id | display label | derived how |
|---|---|---|
| `research` | research | identity |
| `evidence-collection` | evidence collection | hyphen → space |
| `judgment` | judgment | identity |
| `synthesis` | synthesis | identity |
| `render` | render | identity |

**Substrate is not in that list and must not be added to it.** It is the layer all five point into.

### A.2 The proposed table prefix — derived, not a second vocabulary

An abbreviation table (`research → res_`) would be a **second home for the stage name**, which is
the defect rule 5 exists to stop. So the prefix must be *computed* from the id, exactly as the
display label is:

```python
def stage_prefix(stage_id: str) -> str:     # the proposal — one line, one home
    return stage_id[:3] + "_"
```

| stage id | prefix | collision check |
|---|---|---|
| `research` | `res_` | — |
| `evidence-collection` | `evi_` | — |
| `judgment` | `jud_` | — |
| `synthesis` | `syn_` | — |
| `render` | `ren_` | — |

All five distinct at three characters. **Substrate takes no prefix**, and the absence is the signal:
*no prefix means not a stage — the layer everything points into.* That is also the cheap answer,
because it leaves `items`, `populations`, `slugs` and `terms` — the four most-referenced names in
the repository — untouched.

---

## PART B — Key names, and what actually crosses a boundary

### B.1 Only seven columns in the whole schema are pointed at from another stage

41 foreign keys cross a stage boundary; 39 stay inside one. Every one of the 41 lands on one of
these seven columns:

| target | stage | inbound cross-stage FKs | who points at it |
|---|---|---:|---|
| `slugs.slug` | substrate | **14** | research 6 · evidence 3 · judgment 1 · synthesis 3 · render 1 |
| `items.item_code` | substrate | **10** | research 1 · evidence 1 · judgment 4 · synthesis 1 · render 3 |
| `populations.population_code` | substrate | **7** | evidence 2 · judgment 2 · synthesis 1 · render 2 |
| `evidence_sources.ref_id` | evidence | **6** | research 1 · judgment 2 · synthesis 1 · render 1 · substrate 1 |
| `gaps.gap_id` | research | **2** | evidence 1 · judgment 1 |
| `search_executions.exec_id` | research | **1** | evidence 1 |
| `reasoning_doc_citations.citation_id` | synthesis | **1** | evidence 1 |

**That is the entire cross-stage surface.** Everything else a stage knows about another stage, it
reaches through one of these seven columns — or, as §B.4 shows, through a string with no key at all.

### B.2 Nothing points into judgment, and nothing points into render

Zero cross-stage foreign keys target a judgment or a render table. `specifications.specification_id`
is referenced by exactly one thing, `specification_source_links`, in its own stage.

That is *correct* under rule 5 — later stages reach back, earlier stages do not reach forward — and
it means the pipeline's keys almost all flow **backwards**. Three exceptions run the other way and
are worth naming, because each is a promotion edge someone will want to delete as redundant:

| pointer | direction | what it is |
|---|---|---|
| `citation_mining.global_ref_id → evidence_sources.ref_id` | research → evidence | a mined lead that got admitted |
| `source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations.citation_id` | evidence → synthesis | an extraction that became a cited claim |
| `item_population_elaborations.evidence_ref_id → evidence_sources.ref_id` | **substrate → evidence** | substrate citing a stage, which inverts the model |

### B.3 The `REF-` namespace is two tables sharing one id space with no key between them

| | rows | |
|---|---:|---|
| `source_locators.ref_id` (research) | 875 | the clue store |
| `evidence_sources.ref_id` (evidence) | 10 | the admitted corpus |
| present in **both** | **4** | |
| only in `source_locators` | 871 | |
| only in `evidence_sources` | **6** | |

There is **no foreign key in either direction**. `dbcore.next_ref_id()` mints from the union
high-water mark, so the id space is shared — but **`REF-00325` does not tell you which stage it
lives in**, and six admitted sources have no clue-store row at all.

**Eleven ids do not even match the format.** `source_locators` holds `REF-VERIFIED-001` …
`REF-VERIFIED-012`, which sort *above* every numbered id — `max(ref_id)` returns
`REF-VERIFIED-012`, not `REF-00964`. Any high-water mark computed with `MAX()` on text is wrong
today. (`dbcore.next_ref_id()` is the sanctioned computation; hand-rolled `MAX()` is the trap.)

### B.4 Seven column names for one referent, three of them lying

| column | non-null | FK? | what it actually holds |
|---|---:|---|---|
| `evidence_sources.ref_id` | 10 | (is the target) | `REF-00325` |
| `citation_mining.global_ref_id` | 10 | **yes** | `REF-00965` |
| `reasoning_doc_citations.source_ref_id` | 0 | **yes** | a ref_id |
| `source_value_extractions.root_ref_id` | 0 | **yes** | a ref_id |
| `item_population_elaborations.evidence_ref_id` | 0 | **yes** | a ref_id |
| `evidence_sources.superseded_by_ref_id` | 0 | **no** | a ref_id, unenforced |
| `citation_mining.local_ref_id` | 10 | no | **`RAP-01` — not a ref_id at all** |
| `source_slug_links.local_ref_id` | 10 | no | **`RAP-04` — not a ref_id at all** |
| `supersession_check.local_ref_id` | 0 | no | **not a ref_id at all** |

`local_ref_id` reads as "a ref_id, locally scoped". It is a **within-document citation label**. Three
tables carry it; none of them means a `REF-`.

### B.5 Soft references — a column named for another stage's key, with no key

| stage | column | should point at |
|---|---|---|
| judgment | `conflicts.pop_a`, `conflicts.pop_b` | `populations.population_code` — **unconstrained** |
| judgment | `conflicts.gap_id` | `gaps.gap_id` — unconstrained, while `specifications.gap_register_id` *is* keyed |
| research | `source_locators.ref_id` | not keyed to `evidence_sources` (§B.3) |
| research | `reference_stubs.ref_id` | same |
| research | `source_locators.used_in_bpcs` | a packed reference into **synthesis** |
| substrate | `slugs.serves_axes`, `situations.attaches_axes` | packed lists of demand codes |
| 9 tables | `jurisdiction` | no table exists — the vocabulary is an **inert enum** in `schemas/enums.py` |

`conflicts` is the table a mobility batch needs most — ramp gradient is the opposed demand between
ambulant and wheeled movement — and its two population columns are free text.

### B.6 Key *kind* is inconsistent: stable code vs. surrogate integer

| minted as a stable text code | minted as a bare integer |
|---|---|
| `ref_id` `REF-00325` · `item_code` `A-01` · `population_code` `AUT` · `slug` · `term_id` `TERM-001` · `room_code` `R-BA` · `gap_id` `GAP-B01-001` · `match_id` `MB1-001` · `decision_id` `D-0001` | `search_executions.exec_id` `19` · `search_candidates.candidate_id` `1` · `jurisdictional_values.jv_id` `4` · `specifications.specification_id` · `convergence_assessment.convergence_id` · `source_value_extractions.extraction_id` |

**The admission edge hangs on an integer.** `search_admissions` is the provenance chain from a
source back to the act of looking, and its key is `(exec_id, ref_id)` — half stable code, half
rowid. So does the judgment stage's whole output: `specification_id` is `INTEGER PRIMARY KEY`.

---

## PART C — The nine naming faults, each measured

1. **No name carries its stage.** 0 of 66 tables are prefixed. Rule 5 is unusable without knowing a
   table's stage, and CLAUDE.md makes deriving the stage map a *stopper*. The name is where that
   derivation should already be.
2. **"Locator" means two opposite things in one schema.** `source_locators` holds `doi, url, pmid,
   pmcid, isbn, issn, standard_number` — **bibliographic identifiers**. Meanwhile R3 defines a
   locator as a within-document pointer (*"clause/section/page"*), which is what
   `source_value_extractions`' sixteen `loc_*` columns hold (`loc_division` … `loc_subclause_end`).
   The table named `_locators` holds the sense it is not.
3. **`jurisdictional_values` holds no values.** 109 rows; `value_text` and `value_numeric` are
   **0 non-null**, by the REFERENCE-ONLY ruling of 2026-08-12. It is a lead index. The name states
   the opposite of the ruling.
4. **`bpc_metadata` is not metadata.** It *is* the best-practice synthesis — the stage's output —
   not data about it. `BPC` is also an unexpanded acronym appearing in a table name, a column
   (`items.bpc_source_slug`, `source_locators.used_in_bpcs`) and a junction (`item_bpc_links`).
5. **Two tables named `*_specs` do not reference specifications.** `case_study_specs.item_code →
   items.item_code` and `economics_entry_specs.item_code → items.item_code`. Both are named for the
   judgment object and keyed on the render rollup.
6. **Three suffixes for one relation kind.** `_links` ×9, `_map` ×3, and bare-noun junctions
   (`connection_targets`, `room_items`, `case_study_populations`, `case_study_specs`,
   `economics_entry_populations`, `economics_entry_specs`, `search_admissions`). All are the same
   thing: a primary key composed of references to two other things. (`term_aliases` looks like a
   fourth form and is not — see §D.)
7. **Head noun is plural in 52 tables and singular in 14** — `access_duration`, `access_need_icf`,
   `bpc_metadata`, `citation_mining`, `convergence_assessment`, `evidence_population_match`,
   `external_root_registry`, `gap_mining`, `lang_jur_map`, `search_coverage`, `supersession_check`,
   `weighting_profile`, and the two `*_axis_map`s.
8. **The activity is named, not the row.** `citation_mining`, `gap_mining`, `supersession_check`
   name a *process*; one row is a *run of it*. Compare `url_verification_runs`, `item_audit_runs`,
   `pipeline_runs`, which get this right.
9. **Retired vocabulary is still in four table names and six columns** — `axes`, `item_axis_links`,
   `population_axis_map`, `access_need_axis_map`; `axis_code` ×4, `slugs.serves_axes`,
   `situations.attaches_axes`. Already ruled (P0.6): rename, then register.

---

## PART D — The proposed grammar

> **`<stage-prefix>` `<subject>` `<kind-suffix>`**, head noun always plural.

**Prefix** — `stage_id[:3] + "_"`, derived (§A.2). No prefix = substrate.

*The junction test is deliberately written against key columns rather than payload, because the
payload test fails on real tables. `term_aliases` has PK `(term_id, alias, language)` and looks
composite, but `alias` **is** the payload — the row is the alias — so it is a record, not a
junction, and keeps its name.*

**Kind suffix** — a closed set of three, each decided by a test against the schema itself, not by
taste:

| kind | test | suffix | example |
|---|---|---|---|
| **registry** | PK is a code this table mints, and other tables FK to it | *(none)* | `items`, `populations` |
| **junction** | PK is a composite of ≥2 columns that each identify *another thing* — a foreign key, or an external vocabulary with no table (`jurisdiction`, `language`, `icf_code`) | `_links` | `evi_slug_links` |
| **record** | anything else — one row is a thing that happened or was decided | plural noun naming what one row **is** | `res_searches`, `jud_specifications` |

A fourth is worth declaring because it is already used correctly four times and would otherwise get
collapsed into "record": **`_runs`** for a record of an act performed, carrying a timestamp and an
outcome (`url_verification_runs`, `item_audit_runs`, `pipeline_runs`, and — after fault 8 —
`res_mining_runs`, `evi_supersession_runs`).

---

## PART E — The full reconciliation, all 66 tables

Rows marked **†** are where the *name* is wrong, not merely unprefixed — those are the ones worth
arguing about. Everything else is a mechanical prefix.

### RESEARCH → `res_` (10 tables, 1,087 rows)

| current | rows | one row is | proposed | why |
|---|---:|---|---|---|
| `search_executions` | 28 | one query, verbatim, pre-screening | `res_searches` | the row is a search, not an "execution" |
| `search_candidates` | 60 | a screened but unresolved lead | `res_candidates` | prefix only |
| `search_coverage` | 0 | slug × jurisdiction covered | `res_coverage_links` † | it is a junction; singular head |
| `search_languages` | 0 | slug × language covered | `res_language_links` † | same |
| `citation_mining` | 10 | one backward/forward pass | `res_mining_runs` † | fault 8 |
| `gap_mining` | 0 | one gap-driven pass | `res_gap_mining_runs` † | fault 8 |
| `gaps` | 5 | an open question the book cannot answer | `res_gaps` | prefix only |
| `source_locators` | 875 | **a lead: identifiers for a document to go and get** | `res_leads` † | fault 2 — it holds identifiers, not locators |
| `reference_stubs` | 0 | ? | `res_stubs` † | 0 rows, no writer — **delete candidate, not rename** |
| `jurisdictional_values` | 109 | which code document to go and get | `res_code_leads` † | fault 3 — it holds no values |

### EVIDENCE COLLECTION → `evi_` (10 tables, 92 rows)

| current | rows | one row is | proposed | why |
|---|---:|---|---|---|
| `evidence_sources` | 10 | an admitted source | `evi_sources` | prefix absorbs `evidence_` |
| `evidence_source_authors` | 37 | one author position on a source | `evi_source_authors` | prefix only |
| `source_slug_links` | 10 | source × topic admitted under | `evi_slug_links` | prefix only |
| `search_admissions` | 10 | **the admission edge**: query × source | `evi_admission_links` † | fault 6 — it is a junction |
| `evidence_population_match` | 25 | an R13 grade of study-vs-served | `evi_population_grades` † | it is a grade; deliberately non-unique, so plural matters |
| `source_value_extractions` | 0 | **"the paper says 1200 mm"** | `evi_extractions` † | `source_` is redundant under the prefix |
| `extraction_population_links` | 0 | extraction × population | `evi_extraction_population_links` | prefix only |
| `supersession_check` | 0 | one currency check on a source | `evi_supersession_runs` † | fault 8 |
| `url_verification_runs` | 0 | one R10 re-retrieval | `evi_url_verification_runs` | already correct |
| `external_root_registry` | 0 | an independent evidence root | `evi_roots` † | fault 7; "external registry" describes the file cabinet, not the row |

### JUDGMENT → `jud_` (7 tables, 0 rows)

| current | rows | one row is | proposed | why |
|---|---:|---|---|---|
| `specifications` | 0 | **the determination — the book's answer** | `jud_specifications` | name is owner-directed (2026-08-12); prefix only |
| `specification_source_links` | 0 | determination × governing source | `jud_source_links` | prefix absorbs `specification_` |
| `convergence_assessment` | 0 | whether independent streams agree | `jud_convergence_assessments` † | fault 7 |
| `spec_value_probes` | 0 | a progressive-measurement probe | `jud_value_probes` | prefix absorbs `spec_` |
| `probe_population_links` | 0 | probe × population | `jud_probe_population_links` | prefix only |
| `conflicts` | 0 | **two populations' needs incompatible in one space** | `jud_conflicts` | prefix only — but see §B.5, `pop_a`/`pop_b` need keys |
| `item_audit_runs` | 0 | one audit pass over an item | `jud_audit_runs` | prefix absorbs `item_` |

### SYNTHESIS → `syn_` (6 tables, 0 rows)

| current | rows | one row is | proposed | why |
|---|---:|---|---|---|
| `bpc_metadata` | 0 | **the best-practice synthesis for a slug** | `syn_best_practice` † | fault 4 — it is the synthesis, not metadata |
| `item_bpc_links` | 0 | synthesis × item | `syn_item_links` † | drops the acronym |
| `connections` | 0 | **"when writing X, also consider Y"** | `syn_connections` | prefix only |
| `connection_targets` | 0 | connection × target | `syn_connection_links` † | fault 6 |
| `reasoning_doc_citations` | 0 | a claim in a reasoning doc, verified | `syn_citations` | prefix absorbs the rest |
| `citation_population_links` | 0 | citation × population | `syn_citation_population_links` | prefix only |

### RENDER → `ren_` (10 tables, 17 rows)

| current | rows | one row is | proposed | why |
|---|---:|---|---|---|
| `rooms` | 17 | a room-type surface | `ren_rooms` | prefix only |
| `room_items` | 0 | room × provision | `ren_room_item_links` † | fault 6 |
| `case_studies` | 0 | a Part-12 built example | `ren_case_studies` | prefix only |
| `case_study_outcomes` | 0 | a measured outcome | `ren_case_study_outcomes` | prefix only |
| `case_study_populations` | 0 | case study × population | `ren_case_study_population_links` † | fault 6 |
| `case_study_specs` | 0 | case study × **item** | `ren_case_study_item_links` † | **fault 5 — the name says spec, the key says item** |
| `case_study_strategies` | 0 | a strategy used | `ren_case_study_strategies` | prefix only |
| `economics_entries` | 0 | a Part-13 cost/benefit entry | `ren_economics_entries` | prefix only |
| `economics_entry_populations` | 0 | entry × population | `ren_economics_population_links` † | fault 6 |
| `economics_entry_specs` | 0 | entry × **item** | `ren_economics_item_links` † | **fault 5** |

### SUBSTRATE → no prefix (23 tables, 3,861 rows)

| current | rows | proposed | why |
|---|---:|---|---|
| `items` | 93 | **see §F.1 — its stage is in question** | the 2026-08-26 ruling makes it a render rollup |
| `populations` | 23 | unchanged | registry |
| `slugs` | 106 | unchanged | registry |
| `terms` | 88 | unchanged | registry |
| `term_aliases` | 2382 | unchanged | *proposed as `term_alias_links` on a first pass and withdrawn* — `alias` is the payload, so it is a record, not a junction |
| `access_needs` | 17 | unchanged | registry |
| `axes` | 17 | `icf_demands` † | **already ruled — P0.6** |
| `access_duration` | 3 | `access_durations` † | fault 7 |
| `access_stakes` | 3 | unchanged | registry |
| `life_stage_modifiers` | 2 | unchanged | registry |
| `weighting_profile` | 5 | `weighting_profiles` † | fault 7 |
| `situations` | 0 | unchanged (0 rows — delete candidate) | |
| `access_need_icf` | 43 | `access_need_icf_links` † | faults 6, 7 |
| `access_need_axis_map` | 21 | `access_need_demand_links` † | **P0.6** + fault 6 |
| `item_axis_links` | 158 | `item_demand_links` † | **P0.6** |
| `population_axis_map` | 53 | `population_demand_links` † | **P0.6** + fault 6 |
| `item_population_links` | 372 | unchanged | already correct |
| `item_population_elaborations` | 0 | unchanged | but see §B.2 — it points *into* evidence |
| `term_item_links` | 147 | unchanged | already correct |
| `lang_jur_map` | 70 | `language_jurisdiction_links` † | faults 6, 7, and two abbreviations |
| `decisions` | 166 | unchanged | see §F.3 |
| `data_migrations` | 352 | unchanged | see §F.3 |
| `pipeline_runs` | 1 | unchanged | see §F.3 |

**Count**, derived from this table rather than asserted
(`grep '^| \`' | grep -c '†'`): 66 tables · **30 carry a name fault** (†) · **36 are prefix-only**.

---

## PART F — What this does NOT decide

### F.1 `items` may not be substrate any more
The derived stage map (2026-08-25) puts `items` in substrate as a vocabulary. The owner ruling of
**2026-08-26** makes it *"the Part-4 render rollup … **derived from** specifications rather than
keyed by them."* Under the derivation test — *whose own work does this record?* — a table derived
from judgment output is **render**, not substrate. If that reading holds, `items` becomes
`ren_items` and the cross-stage map changes underneath everything above: **all 10 foreign keys
targeting `items.item_code` are re-classified**, and 3 of them —
`ren_room_item_links`, `ren_case_study_item_links`, `ren_economics_item_links` — stop being
cross-stage at all, because both ends land in render. The remaining 7, including four from judgment,
become judgment→render and evidence→render edges, which are **forward** pointers of the kind §B.2
finds are otherwise almost absent. That is the single highest-consequence open question here, and it
is the owner's.

### F.2 The entity model's arrow runs backwards from the ruled pipeline
`governance/conceptual-model.md:90`: *"ENT-02 → ENT-03 → ENT-01 … Sources feed into BPC entries.
**BPC synthesis produces specifications.**"* That is evidence → **synthesis** → judgment. The ruled
pipeline is evidence → **judgment** → synthesis. The model predates the ruling and one of them has
to be corrected; a rename executed against the wrong one bakes the contradiction into 66 names.

### F.3 Three tables are not in any stage and not really substrate either
`decisions` (166), `data_migrations` (352), `pipeline_runs` (1) record **the project's own acts**,
not the book's content. They are filed under substrate for want of anywhere else. A `meta_` prefix
is arguable; so is leaving them alone. Not decided here.

### F.4 Key *kind* is out of scope and shouldn't be
Renaming `search_executions` to `res_searches` does not fix `exec_id` being a rowid (§B.6). A rename
migration is the cheapest moment this project will ever have to also make the judgment stage's key a
stable code — `specifications` holds **0 rows**. After the first determination, it is re-reasoning.

---

## PART G — What it would cost, and the one thing that makes it cheap

**Now is the cheapest it will ever be.** 13 of the 66 tables — all of judgment and all of synthesis —
hold **zero rows**, and every render table but `rooms` holds zero. A rename there is DDL only.

**The sweep is the cost, not the SQL.** CLAUDE.md §0.4: a rename is not done until callers are
swept, **a view is a caller, and so is a skill**. Migration 064 exists because 063 swept eight Python
readers and six skills and missed `v_item_provenance`. For this rename the caller set is:

- **18 views** — 7 of them cross-stage (§H below), each one a pointer rule 5 protects
- every `scripts/db.py` subcommand, `dbcore`, and the Pydantic models in `schemas/`
- `governance/check-registry.yaml`, which encodes stage-qualified `basis:` references and broke the
  `--selftest` on the last stage rename
- the skills, which teach table names in prose
- **`scripts/migrations/data_*`** — a column a committed data migration INSERTs can never simply be
  dropped, and the same replay-order trap that cost migration 062 applies to a table rename

**Do it as one migration or not at all.** §R8 item 3's bar on piecemeal execution applies with much
more force at 66 tables than at 4.

---

## PART H — Appendix: the seven cross-stage views

CLAUDE.md names four. Re-derived 2026-08-27 against the stage map, resolving nested views and
quoted table names, there are **seven** — and one of CLAUDE.md's four is not among them:

| view | spans | reads |
|---|---|---|
| `v_source_admission` | evidence + research | `evidence_sources`, `search_admissions`, `search_executions` |
| `v_item_provenance` | evidence + judgment + substrate | + `specifications`, `specification_source_links`, `items` |
| `v_source_reach_all` | evidence + judgment + substrate | + `specifications`, `specification_source_links`, `items` |
| `v_code_floor_only` | **judgment + research** | `specifications`, `jurisdictional_values` |
| `v_pending` | **judgment + research** | `specifications`, `gaps` |
| `v_item_extractions` | **evidence + substrate** | `source_value_extractions`, `evidence_sources`, `items` |
| `v_coverage_priority` | **research + substrate** | `search_executions`, `slugs`, `lang_jur_map` |

**`v_divergence` is not cross-stage.** CLAUDE.md records it as *judgment ← synthesis*; it reads
`specifications` and `convergence_assessment`, and the derived map puts **both in judgment**. The
CLAUDE.md list predates the re-derivation that file itself mandates.

This matters beyond bookkeeping: CLAUDE.md protects cross-stage views from deletion because *a
cross-stage view **is** the pointer*. **Four more views are protected than CLAUDE.md currently
names.**
