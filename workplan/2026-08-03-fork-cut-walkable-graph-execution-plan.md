# Fork cut: a walkable graph from topic to render

**Date:** 2026-08-03 · **Status:** PROPOSED · **Extends:** `workplan/2026-08-02-architecture-decision-and-execution-plan.md`
(does not supersede it) · **Owner gates:** ⚑1 fork trajectory (DG-NON), ⚑2 two-tier reproducibility
(amends DR-2026-05-28), ⚑3 committed-vs-generated policy

> **This plan does not open a new register.** Every item below either executes an existing
> workstream from the 2026-08-02 plan (W4.3, W5.3, N1, N7) or adds the two edge objects that plan
> does not cover. Where an item is already someone else's workstream, it is cited, not restated.
> Per CLAUDE.md §9 guardrail 3.

**How this was produced.** A review of commit `aaf8f1b` (Opus 5), an adversarial factuality audit of
that review against the live repo (Fable 5, 15 claims, read-only), then this plan. The audit
**refuted four of the review's claims and found a defect the review missed entirely**; those
corrections are recorded in §1 rather than quietly folded in.

---

## 0. The goal, and the one number that measures it

The 2026-08-02 plan states the goal as walking a published best practice *backwards*. This plan
takes the same graph in the forward direction, because that is where the fork has to cut:

> **From a research topic, through every intermediate step, to a rendered page — and back — with no
> hop resolved by filename convention, prose, or an unindexed JSON string.**

**The measuring number: rendered pages that cite the sources justifying them.**

| | |
|---|---|
| Rendered spec pages | **87** |
| …that name a single source | **0** → **1** (E-08, 2026-08-03) |

Zero at the time of writing. Not one published page showed its evidence. This is not a content gap — `E-08 × DEAF` is a
`stated` cell holding seven governing refs today — it is that `scripts/generate/spec_page.py:69-73`
selects nine cell columns and **not `governing_refs`**. The data reaches the renderer's doorstep and
is dropped there. Verified: `grep -c 'REF-' site/specs/*.html` returns 0 for every file.

That single omission is the cheapest high-value fix in this plan, and it is what the fork must not
inherit.

---

## 1. Corrections to the review that preceded this plan

Recorded per the house convention of correcting rather than rewriting.

- **[CORRECTED] The regeneration trigger is not broken.** The review claimed
  `regenerate-derived.yml` triggers on file paths rather than `user_version`, so schema-only
  migrations leave derived surfaces stale. False. Its `paths:` filter includes `data/guidebook.db`
  (line 34), and every schema migration commits the DB binary alongside it — the blocking
  `user_version` invariant compels that. Migrations 041–043 landed on a branch; the workflow runs
  `branches: [main]`; PR #78 merged and the trigger fired. **`aaf8f1b` *is* the mechanism working.**
  The staleness was branch-side latency that self-healed. No trigger fix is needed, and §4 removes
  the staleness class entirely by other means.

- **[CORRECTED] All three `item_bpc_links` point at retracted BPCs, not two.** The review read
  status from the links' `rationale` prose (written 2026-07-13). Status lives in
  `bpc_metadata.evidence_state`. All three — including `A-18 → room-acoustic-performance`, whose
  rationale says nothing about retraction — are `RETRACTED-PRE-REHAB` today. Trusting stale prose
  over the queryable column is precisely the failure CLAUDE.md §9 guardrail 1 names.

- **[CORRECTED] There are two `primary` links, not one.** `A-18 → room-acoustic-performance` and
  `F-07 → ms-thermal-temperature-conflict-resolution`. F-07 has a rendered page; A-18 does not.

- **[CORRECTED] "845 cells lost" was the right arithmetic under a methodology that both over- and
  under-counts.** Under-counts divergence: a further **334 cells differ with both sides non-empty**
  (`verification_attempt_count` 61, `verification_note` 57, `last_verified_at` 52, …), equally
  unreproducible — true committed-only information is ~1,179 cells plus 353 `evidence_source_authors`
  rows. Over-counts severity: every one of those columns is machine enrichment (`subtype`,
  `citation_count`, `pages`, `issn`, `publisher`, …) — the write-set of `resolve_dois.py` /
  `verify_urls.py`. "Would be lost on a clean fork" means "would be re-fetched by one job run",
  not "hand-authored synthesis destroyed". This distinction is the whole basis of §5.

- **[CORRECTED] Recommending that the weekly jobs emit migrations re-litigates a closed owner
  decision.** DR-2026-05-28 considered exactly that (option 3b) and adopted 3a. §5 argues the
  boundary was drawn around the wrong object, which is a different claim and a different remedy.

- **[MISSED] The final provenance hop is broken, not merely undriven** — §0 above. The review
  worried about six unrendered pages while all 87 rendered ones fail the project's own citation
  discipline.

- **[MISSED] `governing_refs` is a JSON TEXT array, not an edge.** The one place the cell→source
  relationship exists, it is unindexed, FK-less, and unwalkable from the source side without
  `json_each`. This is the structural root of the provenance problem. Already scoped as **W5.3** in
  the 2026-08-02 plan; this plan raises its priority (§7).

- **[NOTED] Three findings were re-discoveries, not novel catches.** The six-invariant gate
  blindness, the incomplete exemption list, and the `changed_files`-is-an-integer bug are all
  already documented in `governance/check-registry.yaml` and CLAUDE.md.

**What survived unchanged:** the vetting-surface display regression (§2), the missing build driver,
the reproducibility divergence and its cause, the shadow stores, and the Pydantic non-mirror —
including that no CI check enforces it, contrary to CLAUDE.md §4's claim that drift is "CI-caught".

---

## 2. The ten hops, and the two that have no edge object

| # | Hop | Edge today | Verdict |
|---|---|---|---|
| 1 | Topic → slug | `slugs` (106) | OK |
| 2 | Slug → search execution | `search_executions.slug` (84) | OK, thin |
| 3 | Slug → source | `source_slug_links` (1,013) | **Healthiest edge in the repo** |
| 4 | Source → extracted value | `source_value_extractions` (8) | Schema OK; population gap. Missing `item_code` — see 2026-08-02 §4.0 [CORRECTED] |
| 5 | Slug → BPC doc | `slugs.bpc_path` + `bpc_metadata` | OK; 22 slugs docless, 1 doc rowless |
| 6 | BPC → reasoning doc | **filename convention only** | HALF-EDGE |
| 7 | Slug → item | `item_bpc_links` (3 rows) + legacy `items.bpc_source_slug` string | Populated at 3%; legacy string is single-valued and cannot express multi-slug items |
| 8 | Item × population → cell | `evidence_cell_state` (15) | OK, sparse |
| 9 | Cell → governing sources | **JSON TEXT array** | **NO EDGE OBJECT** — W5.3 |
| 10 | Cell/item → rendered page | **nothing** | **NO EDGE OBJECT** |

**Two new objects close the walk:**

**`cell_source_links(cell_id, ref_id, role)`** — normalizes hop 9. One migration, no judgment calls:

```sql
INSERT INTO cell_source_links (cell_id, ref_id, role)
SELECT cell_id, je.value, 'governing'
FROM evidence_cell_state, json_each(governing_refs) je;
```

`json1` is available (SQLite 3.45.1). FK both sides; `governing_refs` frozen then dropped. This is
**W5.3**, already scoped — this plan supplies the migration shape and raises its rank.

**`render_manifest(page_path, item_code, generator, generator_version, db_content_hash, rendered_at, inputs_json)`**
— hop 10, entirely new. Written by the build driver; `inputs_json` (json1) enumerates the cell_ids,
ref_ids and jurisdictional_value ids consumed. This makes a *page* a first-class node and doubles as
the render-freshness receipt (§4). It also gives hop 10 the provenance anchor that finding **N7**
demands of seven other tables.

Hop 6 gets `bpc_metadata.reasoning_doc_path` — a column, not a convention. Convention-coupling is
what produced the `sessions/LATEST` defect; the same pattern is latent here.

---

## 3. Where the SQLite/JSON boundary sits

> **If it is a node or an edge, it is a row. If it is a payload *about* a row, it is JSON. If it is
> prose a human authors, it is a file — and the file has a row pointing at it.**

- **SQLite:** every table in §2, the two new edge tables, and the two shadow stores brought home —
  `data/decisions/decision_register.yaml` (156 entries) into the empty `decisions` table, and
  `references/case-study-compendium.md` (26 entries) into `case_studies` (0 rows, despite migrations
  037 *and* 038 shaping and reconciling its schema). CLAUDE.md guardrail 5 says the DB wins store
  conflicts; today the DB side is the empty one, which is backwards.
- **JSON as json1 columns:** `render_manifest.inputs_json`; raw Crossref/PubMed responses in the
  enrichment tier (§5), so every enriched value names the response that produced it.
- **JSON as files:** `attestations/*.json` stay files — schema-validated documents bound to commits,
  not graph data.
- **Files with rows:** BPC docs, reasoning docs, governance prose. `slugs.bpc_path` already does this
  correctly; extend the pattern, don't invent a second one.

---

## 4. Derived artifacts: stop committing them ⚑3

Today `site/`, `parts/`, the vetting surface and two dashboards are generated **and committed**, with
a bot pushing regenerations to main. That loop produced `aaf8f1b`, the branch-side staleness window,
and 35 revisions of a **462 KB single-line** JSON blob — single-line defeats git's line-based delta
compression, so each revision is near-full-size in history.

**Fork policy.** Committed: the DB, migrations, schemas, governance, BPC/reasoning docs, the
generators. **Nothing generated.** All derived surfaces build in CI and publish as an artifact.

This dissolves the staleness class rather than patching it: there is no committed derived copy left
*to be* stale, and §1's trigger question stops mattering. The PR gate inverts from "committed copy
matches a fresh regeneration" (two sources of truth) to "the build succeeds and
`render_manifest.db_content_hash` matches the PR's DB" (one source of truth, plus a receipt).

**The build driver** — `scripts/generate/build_site.py`, ~20 lines — iterates
`SELECT item_code FROM items`, calls `spec_page.generate()`, then populations and rooms, writes
`render_manifest`, and fails on any item that errors. It does not exist today in any form: no
Makefile, no workflow reference, and `scripts/regenerate_derived.sh` calls only the three `tools/`
generators.

---

## 5. Reproducibility with weekly enrichment: two tiers ⚑2

**The measured position.** A rebuild diverges from the committed DB in 9 of 64 tables, 7 non-exempt.
But four of those seven (`bpc_metadata`, `gaps`, `slugs`, `source_slug_links`) differ *only* in
timestamp re-stamping, and `data_migrations` only in a `notes` marker. **Substantive non-exempt
divergence is two tables: `evidence_sources` and `url_verification_runs`** — both written weekly by
`resolve_dois.py:576` / `verify_urls.py:243,412`, both committed back to main by their workflows
(`resolve-dois.yml:111-149`), neither on DR-2026-05-28's exemption list.

**Neither existing model is right.**

*Migrations-only for enrichment* (option 3b, declined) fossilizes dated observations as canon. A
migration asserts "this is canonically true of the guidebook"; an enrichment row asserts "this is
what Crossref said on date T". Replaying a 2026 `citation_count` in 2030 reproduces the bytes while
falsifying the claim. It would also accrete ~50 files/year of transient network results and fight the
workflows' race-abort path.

*Table-scoped exemption* (option 3a, adopted) draws the boundary around the wrong object. The real
boundary is **column-scoped** — which is why the two-table list was incomplete the day it was
written, the jobs' primary write target being `evidence_sources` itself, and why §1's ~1,179 orphaned
cells exist at all.

**Proposed: tier the data, not the tables.**

- **Canonical tier** — migration-controlled, fully rebuild-reproducible. `evidence_sources` slimmed
  to human-judged fields (identity, tier, evidence_type, jurisdiction, Co-1 fields, the `_note`
  overflows) plus every link/cell/extraction table.
- **Enrichment tier** — `source_enrichment(ref_id, field, value, fetched_at, tool, raw_response_json)`,
  written by the weekly jobs, joined by `url_verification_runs` / `pipeline_runs` /
  `evidence_source_authors`. Outside the reproducibility contract **as a tier**, so it never needs
  another DR to add a table. Reads coalesce canonical over enrichment through a view.
- **Timestamps** — extend `emit_data_migration.py`'s lint to refuse INSERTs omitting `created_at`,
  adopting migration 030's own tail-normalization discipline universally. `DEFAULT (datetime('now'))`
  appears in migrations 030–033, 039, 042 and makes byte-exact rebuild impossible today.

**Then, and only then, `migration_reproducibility_deep` can go blocking.** Enabling deep comparison
now would paint main permanently red — which is exactly why the registry keeps it advisory. Order
matters: tier split → timestamp discipline → promote the gate. The reverse order deadlocks the repo.

This preserves DR-2026-05-28's insight (job-owned data is a different kind of thing) and fixes its
implementation. **It amends a ratified DR and is owner-gated.**

---

## 6. Minimum viable walk: prove it on E-08 × DEAF before scaling

Verified complete at every hop in today's data: slug `deaf-spatial-design` → 7 `source_slug_links`
(REF-00338/339/342/343/344/345/347) → `evidence_cell_state` E-08 × DEAF, state `stated`, those same
7 refs in `governing_refs` → item E-08 → `site/specs/e-08.html`, which already renders and cites
nothing.

1. `cell_source_links` migration (W5.3) — the `json_each` insert above.
2. `spec_page.py` renders governing refs with citation strings and evidence markers from
   `evidence_sources`. **The measuring number moves off zero here.**
3. `build_site.py` + `render_manifest`.
4. Demonstrate both directions: `v_page_provenance` for `e-08.html`, and `v_source_reach` for
   REF-00338 — which also links `manoeuvring-footprint-vs-turning-radius-methodology`, so the
   multi-slug fan-out is exercised, not assumed.

**Second case: A-18.** It exercises the driver on an item with a primary BPC link and no existing
page, and forces the retracted-BPC question — all three `item_bpc_links` targets are
`RETRACTED-PRE-REHAB`, so the page must say so rather than render a confident specification over a
retracted synthesis.

**Views, not materialization.** The chain is a fixed shallow DAG (≤6 joins) over 863 sources and 15
cells; nothing here needs materializing for performance. Materialize the *canonical edge*
(`cell_source_links` — asserted by a human synthesis act, must be FK-checkable); compose the walk in
views. Recursion is needed in exactly one place: `populations.parent_code` ancestry.

---

## 7. Sequencing

### 7.0 Status, and six corrections to this plan's own ordering **[REVISED 2026-08-03, same day]**

An adversarial pass over §7 as written found the ordering wrong in six places. Recorded here
rather than silently rewritten, per the convention of the plan this one extends.

| Item | Status |
|---|---|
| **F2a/F2b** `cell_source_links` + backfill | **DONE** — migration 044 + data migration. 63 rows / 14 cells, junction and JSON agree exactly both directions, 0 FK violations. Rebuilds byte-identically. |
| **F9** vetting-surface note render | **DONE** — all 7 affected entries show their caveat again; C07 still passes. |
| **F6-core** spec pages cite their sources | **DONE** — E-08 renders 7 governing sources. **The measuring number is 1, not 0.** |
| F2-drop, F3a, F5, F6-infra, F7, N1-schema | open |
| F1 (⚑2), F4 (⚑3), F8 | owner-gated, not started |

1. **[CORRECTED] F6 was on the wrong side of the fork line.** §0 calls the citation fix the
   cheapest high-value change in this plan; §7 then parked it behind a fork gated by ⚑1/DG-NON,
   which the owner may decline — so under the original ordering the measuring number would have
   stayed at zero indefinitely. Split: **F6-core** (the render fix) is fork-independent and
   executes now; **F6-infra** (`build_site.py` + `render_manifest`) waits behind ⚑3.
2. **[CORRECTED] F2 never depended on F1.** The table implied it queued behind an owner ruling.
   `cell_source_links` is orthogonal to the `evidence_sources` tier split. Owner-gate latency
   should not sit in front of an ungated mechanical migration.
3. **[CORRECTED] "Freeze then drop" understated the sweep.** `governing_refs` has **nine** live
   code consumers — `validate_evidence_state.py`, `test_db_integrity.py`, `assess_cell.py`,
   `adjudication_integrity.py`, `check_rendered_docs.py`, `validate_verification_consistency.py`,
   `pilot_renderings.py`, `pipeline_completeness.py`, one test — plus `v_best_practice`
   (`SELECT *`). §2 named four. The drop is its own item, not a sub-step of F2, and until it
   lands a consistency check should hold junction ⊇ JSON.
4. **[CORRECTED] F3's blast radius was understated the same way.**
   `data/decisions/decision_register.yaml` is read by at least five live scripts including the
   **blocking** `decision_capture.py`. Retiring it to a stub without repointing them breaks the
   governance battery. Split: **F3a** import-to-DB; **F3b** retirement, after the sweep.
5. **[CORRECTED] F9 at position nine was indefensible** — minutes of work restoring the exact
   information whose loss prompted this review. It ships with the first session touching a
   generator, which is what happened.
6. **[CORRECTED] F5 is not a cut-blocker.** Nothing about the fork's shape depends on it;
   treating it as one adds schedule risk for no definitional gain.

### 7.1 The sequence as revised

**Before the fork is cut** — these define the fork; several are owner-gated.

| | Item | Gate |
|---|---|---|
| F1 | Ruling on the two-tier reproducibility model (§5); determines the `evidence_sources` split and therefore all subsequent migration numbering | ⚑2 owner |
| F2 | `cell_source_links` migration + freeze `governing_refs` (**W5.3**) | none |
| F3 | Import shadow stores: 156 decisions, 26 case studies; retire file copies to redirect stubs (guardrail 2) | ⚑ file retirement |
| F4 | Committed-vs-generated policy (§4); delete generated outputs from the fork's initial tree | ⚑3 owner |
| F5 | Regenerate `schemas/*.py` from `sqlite_master`, or declare the models a deliberate subset — and add the check that actually compares them. Do not carry a fiction into the fork | none |

**After the fork** — mechanical, no governance weight.

| | Item |
|---|---|
| F6 | `build_site.py` + `render_manifest` + **the `governing_refs` render fix** (§0) |
| F7 | `v_page_provenance` / `v_source_reach` + the population-ancestry CTE |
| F8 | Point the weekly jobs at the enrichment tier; first run repopulates §1's ~1,179 cells by re-fetch |
| F9 | Vetting-surface display fix: `COALESCE(author_display, author_display_note)` at `regenerate_vetting_surface.py:564,576` — **display-side only**. Restoring prose to `author_display` would re-trip `test_db_integrity.py:305-335` check C07, which names this surface as the reason placeholder prose in value columns is a defect |
| F10 | Content: populate `item_bpc_links`, retire `items.bpc_source_slug`, extractions, cells — at its own pace, against a schema that is finally ready |

**F5 note.** Hand-mirroring 94 columns into Pydantic recreates the drift with more surface area.
Generate from `PRAGMA table_info` or scope the model honestly. `schemas/evidence_source.py` has 17
fields, different names (`authors`/`year` vs `author_display`/`pub_year`), two fields with no DB
column at all, and a docstring claiming 531 records against 863.

---

## 8. What this plan does not decide

- Whether to fork at all (⚑1, DG-NON trajectory — owner only).
- ~~N1 and N3 remain ahead of this work in the 2026-08-02 priority order. A third of the corpus
  being unprovenanced outranks making the render hop walkable — this plan does not jump that queue,
  it queues behind it.~~ **[CORRECTED 2026-08-03]** This sentence was written as scope discipline
  and was wrong in its premise. §8's concern is the *honesty of rendered output*: that a page
  citing its sources while silently presenting unprovenanced code values would look sourced and
  hide the unsourced third. Verified against the actual generator — `spec_page.py` contains **zero**
  references to `jurisdictional_values` or any jurisdiction column, and **zero of 87** rendered
  pages mention jurisdiction or a code value. The feared page cannot currently exist. Meanwhile the
  render hop's real honesty failure was the opposite one: 87 confident pages citing nothing.

  N1 keeps its rank as the top **content-effort** item (109 values, no `ref_id`, 26/26 phantom
  `spec_id`, and T4–T6 is 314 of 863 sources) and its backfill proceeds as the priority workstream.
  It does not gate two disjoint one-session structural fixes that touch different tables and
  different files.

  **§8's substance is better served as an invariant than as a queue position**, and is hereby
  restated as one: *a regulatory-floor value renders only from a `jurisdictional_values` row
  carrying a non-null `ref_id`.* Today that is trivially satisfied because no floors render at all.
  The moment a floors section is added to the page template, the rule — not a remembered priority
  ordering — prevents the false-confidence page. Queue positions evaporate the day they are
  forgotten; invariants do not.
- Whether the 22 docless slugs and 62 retracted BPCs are rehabilitated before or after the cut. That
  is content sequencing, and it belongs to the BPC rewrite workplan.
