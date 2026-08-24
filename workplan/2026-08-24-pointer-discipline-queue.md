# Pointer-discipline migration queue — PD-0 … PD-8

**Written 2026-08-24, after the owner asked where the queue had been merged and a new session
could not find it. It had never been merged anywhere.** It existed only in one conversation,
produced by a Fable 5 read-only audit, and three of its items shipped to `main` citing labels —
`M3`, `M5` — that no file in this repository defined. `scripts/migrations/data_20260824173108`
opens *"M3: retire admitted_ref_ids"* and `governance/retired-vocabulary.yaml:97` says *"the M5
author sweep"*: two orphan labels pointing at nothing a reader could reach.

> This is the failure `DR-2026-08-24-scaffolding-is-phase-specific` §0 already recorded, one
> level down: **"A ruling not in the repository cannot bind a session that did not witness it."**
> There it was owner rulings. Here it was my own execution plan, and I compounded it by
> reporting the remaining set to the owner as *"M4, M6, M7, M8"* — **four items, when six
> remain.** PD-1 and PD-2 were never done and I had stopped mentioning them.

**Primary source:** `scratchpad/session_2026-08-24-pointer-discipline/fable-stage-discipline-audit-2026-08-24.txt`
— the audit, recovered verbatim from the session transcript and committed alongside this. Read it
for the reasoning. Read this file for status: **every figure below was re-measured against the live
DB on 2026-08-24**, and several of the audit's counts are stale.

---

## Why the labels changed: `M<n>` → `PD-<n>`

`M<n>` was ambiguous the day it was coined, in two directions at once:

| Collision | Where |
|---|---|
| **`M4(2)` / `M4(3)`** = UK Building Regulations Approved Document M, Volume 4 | live evidence-corpus term across `references/`, `_archived/parts/`, and a committed migration's `metadata_integrity_detail` |
| **`M1`–`M7`** = "mission throughlines" | `workplan/_superseded/workplan-co0007-synthesis.md`, `co0007-synthesis-workplan-2.md` |
| **`M1`–`M5`** = adversarial-review findings | `workplan/2026-08-12-commit-91-adversarial-review.md` |

A session grepping `M4` gets Building Regs, not this queue. `PD-` (pointer discipline) collides
with nothing. **The old labels are kept as aliases below** so the two shipped references resolve;
do not rewrite the migration header or the YAML comment — both are append-only records.

---

## The rule the whole queue executes

`DR-2026-08-24-scaffolding-is-phase-specific` §2.1, owner's words, general form:

> *"It is better to have a table cell point to another table cell than to rewrite."*
> **Never write the same fact into a second table.**

And the constraint that shapes every item, learned the hard way in migration 062:

> **A column a committed data migration INSERTs can never be physically dropped.** Migrations are
> append-only and replay from the baseline, so a DROP that replays before the INSERT naming it
> breaks `migration_reproducibility`. Such columns are **writer-retired, reader-retired, and
> NULLed forward** — they stay as tombstones. Before proposing any drop, grep
> `scripts/migrations/data_*` for the column name. That grep is the gate.

---

## Status — re-measured against the live DB, 2026-08-24

| ID | Alias | What | Status | Landed as |
|---|---|---|---|---|
| **PD-0** | M0 | Repoint citation-mining readers to the reference ID | **DONE** | `0262c4f` |
| **PD-1** | M1 | `citation_mining` DOI case-drift + divergent `local_ref_id` | **OPEN** — still valid, now cosmetic | — |
| **PD-2** | M2 | Retire `citation_mining.doi` | **OPEN** — scope reduced | — |
| **PD-3** | M3 | Single-home the admission fact | **DONE** | `70e6188` |
| **PD-4** | M4 | `evidence_population_match` FK hygiene | **OPEN** — low value, drop already ruled out | — |
| **PD-5** | M5 | Authors are rows, not five copies | **DONE** | `06535b4`, `52bd052`, + migration 064 |
| **PD-6** | M6 | NULL `evidence_sources.search_queries_used` | **OPEN** — still valid | — |
| **PD-7** | M7 | Shape cleanup, 0-row tables only | **OPEN** — still valid | — |
| **PD-8** | M8 | `items.bpc_source_slug` / `item_bpc_links` rule | **OPEN** — a decision to record, no migration | — |

---

## The open items, with today's measurements

### PD-1 — `citation_mining` identifier drift  ·  OPEN, downgraded to cosmetic

Measured today: **2 rows** whose `cm.doi` differs from `evidence_sources.doi` **by letter case
only** (0 disagree on substance), and **3 rows** whose `local_ref_id` diverges —
`RAP-F61/F69/F70` in `citation_mining` against `RAP-06/09/10` in `source_slug_links`, for the
same three sources.

**PD-0 already removed the harm.** Those three divergences were what made `get_unmined_sources()`
report three fully-mined sources as unmined; the joins now key on `global_ref_id`, and the
acceptance test passes — the three no longer appear. What remains is a cosmetic disagreement
between two labels, load-bearing for nothing.

**Decide, don't drift:** either `UPDATE` the three `citation_mining` rows to the
`source_slug_links` labels, or record that `citation_mining.local_ref_id` is a session-local
annotation and non-joinable. Either is defensible; leaving two undocumented answers is not.
Folding the DOI half into PD-2 is cheaper than repairing it here.

### PD-2 — retire `citation_mining.doi`  ·  OPEN, scope reduced from the audit

Measured today: **10 of 10 rows populated** — *not* the 7 the audit and
`references/project-standards.md` both record. **No live code reads it.** Every `git grep` hit is
prose in `project-standards.md` describing the defect, not a caller.

So this is no longer a rebuild. It is: writer-retire (nothing writes it — `db.py`'s `--doi` flag
went with PD-0), then a data migration NULLing 10 rows. **The physical drop is impossible** —
committed data migrations INSERT the column.

> **`references/project-standards.md` instructs the impossible version**, at line ~787:
> *"Order of repair, cheapest first: drop `citation_mining.doi`"*. Followed literally that
> breaks `migration_reproducibility`, which is the trap migration 062 already sprang. A dated
> correction is appended to that file rather than rewriting it — it is the append-only operative
> ledger.

### PD-4 — `evidence_population_match` FK hygiene  ·  OPEN, low value

Measured today: 25 rows, **0 drifted** (`source_ref` equals `ref_id` on every row), **0 NULL**.

The audit reached its own verdict here and it still holds: *"defer the physical drop; ship only
the FK-hygiene."* The drop is blocked — committed migrations INSERT `source_ref`. What is left is
adding `target_population → populations` as a real FK and marking `source_ref` deprecated-for-
readers. **No drift exists to fix**, so this is the lowest-value item in the queue; schedule it
last or fold it into PD-7.

### PD-6 — `evidence_sources.search_queries_used`  ·  OPEN, valid

Measured today: **10 of 10 rows populated** with copied query text; `v_source_admission` holds
**10 rows** to point at instead. The audit's sharpest observation stands — some of those rows
literally contain the prose *"see search_executions exec 10-15 for this batch"*: **the data is
asking to be a join.**

Data migration NULLing 10 rows, after redirecting readers to `v_source_admission.query_text`.
Falsified by: a session needing the query for a ref and the view not returning it.

### PD-7 — shape cleanup, 0-row tables only  ·  OPEN, valid

Re-verified empty today, so all still free to reshape: `bpc_metadata`, `conflicts`,
`spec_value_probes`, `reasoning_doc_citations`, `specifications`, `economics_entries`,
`situations`, `case_studies` — **0 rows each**.

`jurisdictional_values` holds **109 rows** and is the exception the audit already flagged: it
arrives via data migrations, so check which columns those INSERT before touching it.

One file, pure DDL. Free today and expensive the moment any of these takes a first row —
`specifications.governing_refs` above all, which becomes a migration over live determinations.
**Gate each table with the `scripts/migrations/data_*` grep before including it.**

### PD-8 — `items.bpc_source_slug` / `item_bpc_links`  ·  OPEN, no migration

Measured today: **87 items** carry `bpc_source_slug`; `item_bpc_links` holds **0 rows**. Two homes
for one fact, one populated.

Record in the decision register: the column is authoritative for the primary link; the junction is
reserved; migrate-and-drop only when a non-primary link is first needed. Building the junction now
would create a pointer nothing dereferences, which the audit rightly calls worse than the copy.

---

## What the audit says NOT to do

Carried forward because each has a reason that outlives the queue:

1. **Do not touch `source_locators` ↔ `evidence_sources` duplication.** Owner-exempt clue store —
   *"the clues table is a historical artifact… We do not care about information in the clues table
   being duplicated."* Its case-drifted DOIs are allowed to be wrong-ish.
2. **Do not drop `reference_stubs`.** The empty tombstone is load-bearing for replay;
   `data_20260823223839` writes into it. 062 tried the tidy version and failed the gate.
3. **Do not physically drop any column a committed data migration INSERTs.** See the constraint above.
4. **Do not convert frozen snapshots** — `search_candidates`, `gap_mining.candidate_dois`,
   `supersession_check.superseding_dois`, `retrieval-log/`. A pointer to a row that may never exist
   is worse than the copy.
5. **Do not add parity checks or triggers to police the remaining copies.** CLAUDE.md §1 — apparatus
   carries the burden of proof, and a parity check makes a dual home *survivable*, therefore
   permanent. The discipline is fewer homes, not better-guarded homes.
6. **Do not execute the `axes` retirement inside this series.** Real duplication, but an owner-ruling
   execution with 232+ live crossing rows; mixing it into plumbing hides a doctrinal change.
7. **Do not build junctions for `convergence_assessment`'s JSON arrays yet.** Zero rows, zero readers,
   defensible frozen-assessment semantics.

---

## What PD-5 cost, recorded so the next sweep is wider

PD-5 was the largest item and it **missed a caller**. Migration 063 redirected eight Python readers
and six skills; migration 064 exists because it did not redirect `v_item_provenance`, which the
audit named *first* in its own instruction for that item.

**It was invisible to the completeness proof.** That proof was a byte-exact diff of every
regenerated output — sound for what it covered, and blind here: `specifications` holds 0 rows, so
the view returns 0 rows, so it appears in no rendered output and in no check's subject. **An empty
scope hid a real defect from a byte-exact render diff.** The same session's instrumentation work
found 26 checks passing over empty scopes; this is that shape one layer down.

**Carry forward:** a render diff is not a sweep. Grep the retired names across
`sqlite_master` as well as the tree, and treat a 0-row object as unproven rather than clean.
