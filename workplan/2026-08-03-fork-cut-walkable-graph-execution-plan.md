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
| 4 | **`source_value_extractions.item_code` — extraction → item** *(promoted over step 3)* | **DONE 2026-08-04** — migration 052 + backfill; see the step-4 note |
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

   **[CORRECTED, same session — the "3 unresolvable" were my error, not the data's.]** I looked
   those three up scoped to the mining row's own slug. Resolved globally, **all three exist**:
   `CCD-12` → `REF-00843` (slug `construction-cost-data`), `MHB-35` → `REF-00845` and
   `MHB-36` → `REF-00847` (slug `mental-health-built-environment`). They are **cross-slug
   spillover**: the `SSG-15` mining row's own note says it "filtered to 6 relevant new
   discoveries", two of which belong to another slug — and spillover routing is what
   `DR-2026-07-24-search-executions-substrate` describes as intended behaviour, not breakage.
   Resolved correctly the tally is **15 global `REF-` ids · 50 same-slug locals · 3 cross-slug
   locals · 0 unresolvable.**

   The obstacle survives, but it is a different one, and stating it right matters more than the
   count. `connections_produced` entries carry **no slug scope**, and `local_ref_id` is **not
   globally unique** — 30 values are shared by more than one slug (the bare-numeric `01`–`05`
   series, 4–5 slugs each). An entry is therefore resolvable only by knowing which slug it
   belongs to, and the column does not say; a global lookup happens to be unambiguous for the
   prefixed ids and ambiguous for the bare-numeric ones. *That* is why it cannot be
   foreign-keyed without a decision — not a dangling id. The bare-integer rows (13 of 25) remain
   a separate defect, and the "3 dangling ids" line above is left standing as written so the
   error is visible rather than tidied away.
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

  **[CORRECTED 2026-08-04 — the second sentence of that justification is false.]** An
  adversarial design review attacked it and the attack lands. `energy-conservation-rest-points-seating`
  has **no item at all**: zero `items.bpc_source_slug` matches and zero `item_bpc_links` rows
  (verified). When capture runs, all 19 land `item_code = NULL` and cannot use this edge until
  an item is created and linked — itself a governed act belonging to step 9. Building an edge
  for traffic that cannot use it is the 043/045 mistake with a better story, and that is what
  the sentence above argued for. The 19-pending observation survives only as the argument for
  the column being **nullable**, not for building it.

  The rung is still right, on three feet that hold:

  1. **It removes a demonstrable false positive, today.** Without `item_code`, joining a cell's
     governing sources to their extractions on `ref_id` alone attributes **four** RT60-in-seconds
     extractions to cells 9012 (`A-02`, acoustic ceiling panels, NRC ≥0.85) and 9013 (`A-08`,
     HVAC noise, NC-25) — parameters measured in different units entirely. With the item match
     those correctly drop to zero and only the two genuine `A-18` cells remain. That is not a
     hypothetical drift; it is a wrong answer the schema was returning.
  2. **The readers exist and are starving.** `scripts/assess/assess_cell.py` degrades three
     separate assessments to `NOT_ASSESSED` / `pending_assessment` citing this table, and
     `pilot_renderings.py` emitted "source_value_extractions empty" into published output for
     all fifteen pilot cells — false for two of them.
  3. **A closing window.** The backfill's witnesses resolve unambiguously only while `A-10b`
     has nothing — no `item_bpc_links` row, no cell, no probe (all verified zero). Step 9's
     `item_bpc_links` backfill is expected to give it a parameter link, after which "the slug's
     item for this parameter" stops resolving uniquely. Hop 4 before hop 7 is the only order in
     which this backfill is cheap and clean.

**Step 4 outcome. [2026-08-04]** Migration 052 adds `item_code` (nullable, FK to `items`) plus
`v_item_extractions` — the reader shipped *with* the edge this time, 051's lesson being one
migration old. A column rather than a junction: an extraction row is one claim at one scope, and
a source reaching two items is row multiplication, not an edge set (`REF-00563` already appears
twice for exactly that reason). The cautionary precedent is in the table's own family —
`extraction_population_links`, a junction hanging off `extraction_id`, has **zero rows**.

All 8 rows backfill to `A-18`, but they are not all known the same way, and the migration records
three witness classes rather than flattening them:

| Class | Rows | Witness |
|---|---|---|
| **W1** typed key on the row | 1 | `root_classification_basis` names `PMP-A18-001-F`; that probe carries `item_code='A-18'` in a NOT NULL FK column |
| **W2** typed join, one hop | 2, 3 | row 2 shares row 1's `root_id`/`root_ref_id`; row 3 is governed by exactly one cell, 9011 = (`A-18`, `AUT`) |
| **W3** row-supplied locator, dereferenced | 4–8 | each row's own `file_anchor` points into the A-18 reasoning doc's Step-3 table; the document's subject item is established at its line 92; each claimed value matches its anchored row |

W3 is the one worth defending. The D-0157 standard is "a value is written only where the row
itself supplies it", and rows 4–8 supply a **locator**, not a value. Dereferencing a locator the
row provides is verification; inferring from a table the row never mentions is what
`data_20260804164915` had to revert. One dereference step is required and is stated in the
migration rather than hidden. What was **not** used as a witness: "the slug's primary
`item_bpc_links` row + `parameter='RT60'`" — it resolves uniquely today only because `A-10b` has
no link yet, and a witness with an expiry date is not a witness.

Two standing checks were added with the edge: `J01` (an extraction's item belongs to its slug) and
`J02` (an extraction agrees with the PMP probe its own basis text names). Both fault-injected.

**[CORRECTED, same day — four findings from the steelman review of this step.]**

1. **`J01` and `J02` did not hold the judgment they were written to hold.** The review proved it
   by injection: setting extraction 6 to `A-10b` passes both. `A-10b` shares
   `bpc_source_slug='room-acoustic-performance'`, so `J01`'s second branch admits it, and row 6
   names no probe, so `J02` never reaches it. **The realistic error was never cross-slug — it was
   the other RT60 item, same slug**, which is precisely the ambiguity the column exists to
   resolve. `J03` now pins the eight adjudicated assignments by id, and fires on exactly that
   fault. It is a snapshot check on purpose: the adjudication is not mechanizable, but it is
   pinnable, and a legitimate change to the set has to move this check in the same commit.
2. **One supporting claim in the backfill migration is false.** It closes W3 with "every one of
   these five rows is scoped to classrooms, teaching spaces or learning spaces in its own
   claim_text." Row 6 is not: *"DIN 18041:2016 volume-dependent target curve yields RT60
   typically 0.4–0.8 s for small-to-medium rooms by use type"* — no scope word, and DIN 18041's
   room-group scheme reaches sport and swimming halls, so `A-10b` is not excluded on claim text
   alone. Rows 4, 5, 7 and 8 do carry the wording. The migration is immutable and stands; the
   exclusion for row 6 rests on the other two legs, below.
3. **W3's warrant was argued from the weaker of two available grounds.** "The row supplies a
   locator, so dereferencing it is verification" is a *disclosed extension* of the D-0157 rule,
   not a straight application of it — stated here rather than left as an implied continuity.
   The stronger ground was on the rows and went unused: rows **6, 7 and 8 record in their own
   `root_classification_basis` that the value came "from pilot step-3"**. The A-18 doc's Step-3
   table is not external corroboration for those rows — it is their recorded provenance. Note
   the inversion: row 6 has the weakest claim_text and the strongest warrant.
4. **The pilot-rendering description below was wrong about the artifact.** It said the generator
   "emitted `source_value_extractions empty` for all fifteen pilot cells — false for two." The
   committed `working/pilot/pilot-renderings.html` contains **7 cells and the sentence 7 times**,
   generated when only 9001–9007 existed; none of those seven has extractions. The 15-cell
   description applies to a fresh run that cannot execute. The committed file's falsehood is real
   but different: a table-level "empty" claim repeated 7 times that the table's 8 rows falsify —
   and it labels the B-10 cell **`B-10×NEU`**, a population code that appears nowhere in
   `evidence_cell_state` (the row is `B-10×BRAIN`).

*Checked and refuted:* the review also suggested `tools/pipeline-completeness-dashboard.html`
had been hand-patched rather than regenerated. Re-running `tools/pipeline_completeness.py`
produces no diff, so it was generated.

**Pilot-rendering repair — DONE 2026-08-04, immediately after.** `_sha_label()` makes the tuple
line NULL-tolerant and the generator runs for the first time since the second batch of cells was
added. Regenerating replaces a document frozen at the 7-cell era with the live 15, and that one
act clears three standing falsehoods in published output: the table-level
`"source_value_extractions empty"` claim (7 occurrences → 0), the `B-10×NEU` ghost cell (6 → 0;
the row is `B-10×BRAIN`), and the eight determinations whose `derivation_sha` now reads
**"not recorded"** instead of crashing the render. Whether those eight *should* carry a sha is a
data question left open on purpose — a derivation hash is a claim about how a determination was
computed, and minting one to make the render tidy would fabricate that claim.

`register_integrity_check.py` **passes on the regenerated document**, DB cross-check on, and its
`--selftest` still fires all seven tamper cases against it — so the pass is the checker working,
not the checker asleep. Its quarantine (ENGINE-LAG on I3's repealed absolute form) did not bite
here; no cell in this set triggers the weak-band path. One wart left standing and recorded in
the code: `data-sha` emits the Python repr `'None'` for a NULL, because the checker cross-checks
against `str(row['sha'])`. Fixing it means moving the checker in lockstep, and bundling a second
change into a quarantined check is how you get one nobody can reason about.

**Two pre-existing defects surfaced while sweeping callers, neither fixed here.**
`scripts/generate/pilot_renderings.py` **cannot run at all** — it crashes on
`derivation_sha[:16]` because **8 of 15 cells (9008–9015) have `derivation_sha` NULL**. Confirmed
pre-existing by running the committed version. So the false "source_value_extractions empty"
sentence is corrected *in the generator source* but still stands in the committed
`working/pilot/pilot-renderings.html`, which cannot be regenerated until the generator or the
data is fixed. `register_integrity_check.py` separately reports the committed HTML renders a
`B-10×NEU` cell that no longer exists in `evidence_cell_state`. Both belong to a pilot-rendering
repair, not to hop 4.

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
