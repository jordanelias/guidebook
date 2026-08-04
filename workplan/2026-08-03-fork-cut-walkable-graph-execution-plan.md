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
| …that name a single source | **0** → **11 of 93** (2026-08-04) |

Zero at the time of writing. Not one published page showed its evidence.
**[CORRECTED 2026-08-04]** An intermediate revision of this line read "0 → 1 (E-08)". That
undercounted: `g-03.html` was also regenerated the same evening and cites 4 refs, so the true
progression was 0 → 2 → 11. 11 of 93 is now every item that has a cell; the remaining ceiling is
content, not code. This is not a content gap — `E-08 × DEAF` is a
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

**Hop 10 — `render_manifest`, proposed here and since ABANDONED.** This plan proposed a table
recording each page build. It was created (migration 045) and dropped (046) on 2026-08-04 once the
owner stated the target architecture is dynamic rendering, under which there is no per-page build
event to record. Left in place as the proposal it was, rather than edited to look prescient.

What closed hop 10 instead: `v_item_provenance` and `v_source_reach` (migration 047), keyed on
`item_code` rather than page path, so they survive a page becoming a route; and
`scripts/generate/build_site.py`, which proves page↔DB correspondence by re-rendering rather than
by consulting a stored receipt.

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
- **JSON as json1 columns:** raw Crossref/PubMed responses in the enrichment tier (§5), so every
  enriched value names the response that produced it.
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
generators. **Nothing generated.**

**[CORRECTED 2026-08-04 — owner directive: "Do not rely on artifacts for rendering the site."]**
This section previously said derived surfaces would "build in CI and publish as an artifact". That
was wrong, and the objection is sound: a CI artifact expires, is not addressable, and cannot be
browsed or diffed. Making the site depend on one trades a stale committed copy for a *vanishing*
one, which is worse — the repo would no longer contain the means of knowing what was published.

The correct property is not "where the bytes are parked" but **regenerability**: the DB plus the
generators, both committed, must reproduce the site deterministically at any time, and
it must be possible to prove that a given render corresponds to a given DB state. Under that
property, ⚑3's real choice is between **committing the generated output** and **regenerating it on
demand from committed inputs** — and an ephemeral artifact is not an answer to either.

**[SUPERSEDED the same day, by the next owner directive.]** The paragraph above originally
concluded that this makes `render_manifest` *more* load-bearing. Then the owner stated the target
architecture — "the entire pipeline is dynamic rendering on site" — under which there is no
per-page build event to attest. `render_manifest` was created (migration 045) and dropped
(migration 046) within hours; see 046's header for the full reasoning, including that it repeated
migration 043's speculative-schema mistake.

What actually carries provenance is `v_item_provenance` and `v_source_reach` (migration 047),
which key on `item_code` rather than on a page path and therefore stay correct when a page stops
being a file and becomes a route. And under current practice the DB, the generators and the pages
are committed *atomically*, so the commit itself already answers "what did this page rest on".

This dissolves the staleness class rather than patching it: there is no committed derived copy left
*to be* stale, and §1's trigger question stops mattering. The PR gate inverts from "committed copy
matches a fresh regeneration" (two sources of truth) to "the pages on disk match a fresh render
from the committed DB" (one source of truth). `build_site.py --check` implements exactly that;
registering it in `governance/check-registry.yaml` is what makes it run.

**The build driver** — `scripts/generate/build_site.py`. **[BUILT 2026-08-04.]** Iterates
`SELECT item_code FROM items`, calls `spec_page`, and fails on any item that errors. It writes no
state: `--check` answers staleness by comparing what is on disk against a fresh render, which needs
no manifest and survives the move to dynamic rendering.

Two limits to state rather than let the name imply otherwise: it currently builds **`site/specs/`
only** — `site/populations/` (11 files) and `site/rooms/` (17 files) have generators that it does
not drive — and `--check` does not yet detect an orphan file whose item has been deleted from
`items`.

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
3. `build_site.py` (no manifest — see §2).
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
   executes now; **F6-infra** (`build_site.py`) was thought to wait behind ⚑3 and does not — building
the driver is correct under either answer, and only "delete `site/` from the tree" is gated. Built
2026-08-04.
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
| F6 | **DONE 2026-08-04** — `build_site.py`, the `governing_refs` render fix, and BPC `evidence_state` on every page. No manifest (§2). |
| F7 | `v_page_provenance` / `v_source_reach` + the population-ancestry CTE |
| F8 | Point the weekly jobs at the enrichment tier; first run repopulates §1's ~1,179 cells by re-fetch |
| F9 | Vetting-surface display fix: `COALESCE(author_display, author_display_note)` at `regenerate_vetting_surface.py:564,576` — **display-side only**. Restoring prose to `author_display` would re-trip `test_db_integrity.py:305-335` check C07, which names this surface as the reason placeholder prose in value columns is a defect |
| F10 | Content: populate `item_bpc_links`, retire `items.bpc_source_slug`, extractions, cells — at its own pace, against a schema that is finally ready |

**F5 note.** Hand-mirroring 94 columns into Pydantic recreates the drift with more surface area.
Generate from `PRAGMA table_info` or scope the model honestly. `schemas/evidence_source.py` has 17
fields, different names (`authors`/`year` vs `author_display`/`pub_year`), two fields with no DB
column at all, and a docstring claiming 531 records against 863.

### 7.2 The table-by-table ladder **[ADDED 2026-08-04]**

§7.1 sequences the *fork*. This ladder sequences the *walk* — one table at a time, in the order
the graph is traversed, so that at every rung the chain from a research question to a rendered
page has one fewer JSON array standing in for an edge. It was worked out granularly and is
recorded here because a plan that lives only in a conversation is not a plan.

| Step | Table / hop | State |
|---|---|---|
| 1 | Verification standing — `evidence_sources` columns (D-0157) | **DONE 2026-08-04** — migrations 049 + remap; PR #82 |
| 2 | ~~Hop 3~~ **Hop 2b — `search_admissions`** (search execution → admitted source) | **DONE 2026-08-04** — migrations 050 + 051; see below |
| 3 | ~~`search_candidates.admitted_ref_id`~~ **deferred** — see the reordering note | deferred |
| 4 | **`source_value_extractions.item_code` — extraction → item** — *promoted to next* | next |
| 5 | `bpc_metadata.reasoning_doc_path` — synthesis doc as a column, not a filename convention | pending |
| 6 | Close the DISPUTED seven against `audits/anchor-correctness-sweep-2026-07-20.md` | pending |
| 7 | N1 — `jurisdictional_values.ref_id` (the regulatory-floor invariant in §8) | pending |
| 8 | Drop `governing_refs` after the nine-caller sweep (F2c) | pending |
| 9 | `item_bpc_links` backfill (~84 rows); retire `items.bpc_source_slug` | pending |
| 10 | Render completion — `room_page.py` `FROM room`→`rooms`, drive populations/rooms, promote `site_pages_fresh` to blocking | pending |

**Step 2 outcome, stated honestly.** The junction is correct and complete: 39 edges over 29 of
84 executions, zero orphans, parity with the JSON held in both directions plus a third check
against `results_admitted` (`test_db_integrity` H03/H04/H05, and H01/H02 which finally supply
the consistency check migration 044's header called for and never got). A rebuild from migration
history reproduces `search_admissions` and `cell_source_links` row-for-row.

**[CORRECTED 2026-08-04, same day — four claims this step made that the DB does not support.]**
An adversarial review challenged the step's own framing; each correction below was re-derived
against the live database before being written here. The commit and migration 050 stand as
written — the 045→046 precedent is to record a mistake forward, not to edit history so it reads
as prescient. Migration 051's header carries the two that belong to a migration.

1. **"Hop 3" is the wrong label.** §2's hop 3 is *slug → source* via `source_slug_links` (1,013
   rows, the healthiest edge in the repo) — already a junction, and untouched by this step. The
   edge normalised here is *search execution → admitted source*, which appears nowhere in §2's
   ten-hop table. It is a refinement of hop 2 and strictly finer than hop 3: hop 3 says the
   source belongs to this topic; this says *which logged search found it*. Relabelled **hop 2b**
   in the ladder above.
2. **"The last JSON-array-as-edge on the path" is false.**
   `citation_mining.connections_produced` is still one, and citation mining is a discovery
   channel just as a logged search is. It is also a far worse one, and the difference matters
   because it changes what fixing it costs. Of its 183 rows, 25 carry a non-empty value —
   **13 of those hold a bare integer** (a count, in a column whose other rows hold a list). Of
   the 81 array entries, **15** are global `REF-#####` ids, **50** are slug-scoped
   `local_ref_id` values resolvable only through `source_slug_links(slug, local_ref_id)`, and
   **3 resolve to nothing at all** (`CCD-12` under `accessible-design-economics-cost-premium`;
   `MHB-35` and `MHB-36` under `sensory-space-global-south`). Three vocabularies and two
   cardinalities in one column. It cannot be foreign-keyed until a decision says what the column
   means, and those three unresolvable ids are a data finding owed a look on their own.
   `convergence_assessment`'s five REF-array columns are the same question one hop later.
3. **"Rebuild byte-identical" overstated the scope.** The two junctions reproduce exactly; the
   *file* does not, and never has — ten tables diverge under rebuild for the pre-existing reasons
   §5 documents, none of them caused by this step. The claim was true of the rows and false as
   the sentence read.
4. **The junction shipped with no reader.** 050's header names the reverse walk twice as "the
   point" and builds an index for it, then shipped no query that performs it. Fixed by migration
   051 (`v_source_admission`) — the missing half of 047: `v_source_reach` walks a source forward
   to the pages it justifies, `v_source_admission` walks it back to the search that admitted it,
   with the verbatim query text.

What it does **not** yet do is close the walk. The 39 admitted refs and the 57 refs that govern
a cell are **disjoint sets — zero overlap**. Hop 3 is a real edge on a limb that does not yet
reach hop 9. Nineteen of the 39 belong to one slug
(`energy-conservation-rest-points-seating`), whose cells are not determined. So the honest claim
for this step is "the last JSON-array-as-edge on the path is now a foreign key", not "you can
now walk from a search to a page" — you cannot, for any source, and no amount of schema work
will change that. Only determining cells from searched-and-admitted sources will.

The 824 pre-substrate sources get no admission row at all, and that absence is load-bearing: a
source with no edge means *which search found this was never logged*, not *no search found it*.
Minting an exec_id to make the table look full would fabricate a search — the failure R8 and R14
of the research contract exist to prevent.

**Reordering: step 3 deferred, step 4 promoted. [2026-08-04]** Chasing the disjointness finding
into the data changed which rung is next.

`energy-conservation-rest-points-seating` — 19 of the 39 admitted sources, the most-researched
slug on the substrate — was profiled end to end. Every one of the 19 is `VERIFIED` + `CLOSED`, so
**Phase B is clean and the B-before-E gate is open**. Downstream of that, nothing exists: no
`bpc_metadata` row, no `source_value_extractions` row, no `item_bpc_links` row, no cell. All 19
carry `data_capture_status = 'pending'`. The slug is simultaneously the best-researched and the
least-connected in the repo, and the gap is not a missing edge object — it is that capture,
extraction and synthesis never ran.

Two consequences for sequencing:

- **Step 3 is deferred.** `search_candidates` holds 18 rows, 4 of them `ADMITTED`. Adding
  `admitted_ref_id` would wire four rows onto the limb that just received its edge object, while
  rejections already have a home in `why_not_admitted`. More schema on a structurally complete
  but content-dead limb is precisely the "inventing work" pattern to avoid.
- **Step 4 is promoted.** `source_value_extractions` has 8 rows and **no `item_code` at all** —
  hop 4 is a missing edge object, not a mis-shaped one, and it is the edge the 19 pending
  captures will need the moment capture runs. Building it before the rows exist is the one
  ordering where schema-first is right: the alternative is capturing values into a table that
  cannot say which parameter they describe.

One further constraint the profile surfaced, which bounds what closing the walk can even claim:
**18 of the 19 are tier 3**, one is Co-1 (`REF-00950`) and one T5. Under `governance/tier-system.md`
a T3-only basis never reaches `stated`. So a cell determined from this slug's corpus reaches
`provisional` unless the Co-1 source anchors it as co-primary under CRPD Art. 4.3. Worth knowing
before anyone treats "19 admitted sources" as a finished evidence base.

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
