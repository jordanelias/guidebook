# 2026-08-13 — Writers: a plan under "less code, more centralization"

**Owner instruction:** *"Plan out writers within the context of our existing infrastructure under
the maxim of less code, more centralization."*

> **REVISION 3 — owner rulings of 2026-08-13 recorded at §10-11: split by confidence, uniform
> sink, and a backend vetting surface showing the extract behind each determination.** The two
> rulings compose into a better design than the one offered to them; §10 says how.
>
> **REVISION 2, after an adversarial read-only review against three owner axes — long-term
> integrity, clean slate, and walking the pipeline in all directions with per-cell validation.**
> Revision 1's core idea survived; **two of its specific claims did not, and one of them was
> disqualifying.** What changed is listed at §8 rather than quietly absorbed. In particular:
> revision 1 said this plan **deletes** `ENUM_GUARDS` and proposes **no schema change**. Both are
> now reversed — the deletion was unsafe, and it is unsafe *because* the schema change was refused.

**The plan is still mostly subtraction.** The centralized writer already exists: `scripts/db.py`,
20 write functions, all one shape. What it lacks is not functions but a **sink** — it commits to
`data/guidebook.db` directly, which `CLAUDE.md` §4 forbids, so the whole layer is unusable against
the canonical database. The emitter exists. So does the glue, in a test harness.

| Piece | Where | Why not enough alone |
|---|---|---|
| The write layer | `scripts/db.py` | Commits straight to the canonical DB |
| The emitter | `scripts/emit_data_migration.py` | Takes **text** — someone must hand-write the SQL |
| The glue | `walk_harness.py:183` `emit_and_apply()` | Lives in a test harness; refuses to run outside a disposable tree |

---

## 1. A correction to the count this plan rests on

`workplan/2026-08-13-writerless-tables-analysis.md` and PR #99 said **eleven** tables need writers.
**Nine do.**

`search_coverage` and `search_languages` are **deliberately writerless** — `scripts/db.py:316-326`
raises `FrozenGridError` on either. They were frozen on 2026-08-06 as hand-kept state grids that
had drifted from the search log **in both directions**: 634 cells claimed SEARCHED with 15
corroborated by an execution, while 31 executions landed on cells the grid called NOT-RUN.
`workplan/search-coverage-completion-workplan.md` replaced them with `search_executions` plus
derived views. **Building writers for them would un-freeze a retirement.**

The analysis also called `search_languages` *"GATED — R11"*. Wrong: `research_batch_dod.py` reads
`search_executions`, not the grid. R11 is already satisfied by the log.

Both errors came from checking readers without checking whether a writer was *absent* or *removed
on purpose*. **Those look identical to a counter** — the same failure mode as the probe's own count.

---

## 2. Phase 0 — The one schema migration, and why it must come first

**Revision 1 claimed Phase 1 would let us delete `ENUM_GUARDS` (`emit_data_migration.py:66-108`)
because "every CHECK constraint on every column enforces itself" once parameters are bound against
a real schema. That claim is false, and it was checked and found false:**

```
evidence_sources.doi_resolution_outcome  →  TEXT          (no CHECK)
evidence_sources.url_resolution_outcome  →  TEXT          (no CHECK)
source_locators .doi_resolution_outcome  →  TEXT          (no CHECK)
source_locators .url_resolution_outcome  →  TEXT          (no CHECK)
evidence_sources CHECK'd columns: citation_mining_status, data_capture_status,
    processing_blocked_reason, scope, verification_closure_reason,
    verification_disposition, verification_method     ← neither outcome column
grep -rn 'resolution_outcome' schemas/                →  no matches
```

The emitter's own comment says so plainly (`emit_data_migration.py:55-56`): these vocabularies are
*"enforced by an AUDIT rather than by a table CHECK, so SQLite accepts a bad value silently."*
Binding parameters against the real schema therefore enforces **nothing** for exactly these two
columns. Deleting the guards would have regressed to post-hoc detection by
`test_db_integrity.py` [B03]/[B04] — **the precise mode whose documented failure created the guard**
(the same wrong value written in two consecutive batches on 2026-07-25, after the lesson had been
recorded in prose three times).

**So the constraint gets built rather than assumed.** One schema migration, before Phase 1:

- `CHECK` on `doi_resolution_outcome` ∈ {RESOLVED, NO-MATCH, REVERTED} and
  `url_resolution_outcome` ∈ its eleven values, on **both** `evidence_sources` and
  `source_locators`.
- `UNIQUE` on `evidence_sources.doi` where non-null. There is **no unique index on `doi` today** —
  only the `ref_id` autoindex and `idx_evidence_sources_standing`. R9's duplicate-DOI pre-check
  (`db.py:1648-1668`) is therefore a *read*, not a constraint, and two concurrent sessions defeat it
  (§3).

**This is cheap only now.** SQLite has no `ADD CONSTRAINT`; adding a CHECK means rebuilding the
table. `evidence_sources` and `source_value_extractions` are at **0 rows** today, so the rebuild is
free. Every row admitted from here makes it more expensive. **Revision 1's "no schema change
proposed" was not conservatism — it was the thing that made the deletion unsafe.**

Only after this migration lands does the `ENUM_GUARDS` deletion become true rather than aspirational.

---

## 3. Phase 1 — Redirect the sink. One function. No new writers.

Every `db.py` write is shaped:

```python
with connect(dry_run) as conn:
    conn.execute(f"INSERT INTO gaps ({cols}) VALUES ({ph})", list(row.values()))
```

`connect()` (`db.py:55-72`) opens the canonical DB and commits. Change **that one context manager**:
open a scratch copy, record each `(sql, params)` pair, and on clean exit emit a migration through
the sanctioned two-step instead of committing. Reads inside the function still work; every FK,
CHECK and UNIQUE in the real schema validates the write before it is emitted; a failed write emits
nothing.

**All 20 existing writers become legitimate against the canonical database for the first time, and
not one is rewritten.** `dry_run` keeps its meaning: emit nothing.

### 3a. The design problem revision 1 got wrong: this is time-of-check/time-of-use

Revision 1 filed snapshot drift as "Risk 1" and said the reproducibility gate would catch it.
**Both halves were wrong**, and the real surface is worse:

- **ID allocation and dedup read the snapshot, not the canonical.** `next_gap_id`
  (`db.py:149-156`), `next_con_id` (`:110-117`) and the R9 duplicate-DOI check (`:1648-1668`) all
  validate against whatever was copied. Two concurrent sessions both compute `GAP-042` and both
  pass. Because `gap_id` is a PK, the second migration fails **at apply, inside an
  already-committed immutable file** — which breaks every future rebuild and cannot be amended, only
  compensated. For `doi` it is worse: with no UNIQUE index (§2), the duplicate **applies cleanly and
  silently**, defeating R9 by way of the machinery built to serve it.
- **`lastrowid` drift across a junction.** `log_search` (`db.py:394-417`) takes
  `exec_id = cur.lastrowid` from `search_executions` and writes it into `search_admissions` in the
  same block. Rendered as a literal from the scratch's autoincrement and replayed against a
  canonical that moved, the junction row dangles.
- **The blocking gate does not cover either.** `migration_reproducibility.py:56-62` compares
  `PRAGMA user_version` plus `COUNT(*)` on six tables, committed against rebuilt. A *bad but
  applicable* migration reproduces identically on both sides and the gate stays green. A
  *non-applicable* one does not produce "a mystery one commit later" — it produces a permanently red
  rebuild inside an immutable file.
- **Multi-block operations are not atomic.** `add-source --slug` (`db.py:1346-1349`) is two
  `connect()` blocks — `insert_evidence_source` then `insert_source_slug_link` — so it is two
  migrations. "Emit nothing on exception" holds *per block*: block 1 applied plus block 2 failed is
  an immutable half-write.

**Therefore Phase 1 is not "copy, record, emit". It is:**

1. **Snapshot atomically**, inheriting the probe's mechanism (`probe_pipeline.py:40-44`) rather than
   a naive `shutil.copy` — `connect()` sets `PRAGMA journal_mode=WAL` (`db.py:61`), so a copy that
   ignores the `-wal` sidecar is a copy of the wrong database, and a read helper against canonical
   dirties the committed blob's header.
2. **Re-validate at apply time, not only at snapshot time.** Immediately before emit, replay the
   recorded parameters against a *fresh* copy of canonical. If the canonical moved underneath —
   an id taken, a DOI now present — fail loudly and emit nothing, rather than emitting a file that
   will break replay forever.
3. **Serialize the writer, or allocate ids from the canonical at emit time.** A single-writer
   discipline is the smaller change; id-at-emit is the more robust one. This is a real decision and
   the plan does not pretend otherwise.
4. **Give multi-block operations one transaction**, or state explicitly that they emit N migrations
   and provide the compensating path.

That is more than revision 1 costed. The honest estimate is **not "120 lines net"** — the re-validate
step and the snapshot mechanism are the bulk of it, and `emit_and_apply()` cannot simply be moved:
it is coupled to the harness's `TREE` global, its transcript writer and its `run()` wrapper
(`walk_harness.py:30-49, 183-221`). Treat it as a rewrite that the harness then imports.

---

## 4. Phase 2 — Nine functions, one shape, no new files

Each missing table gets one function in the shape used twenty times already, plus one `add_parser`
line. **No new module, no new abstraction.**

| # | Table | Stage | Model | Notes |
|---|---|---|---|---|
| 1 | `search_candidates` | research | — | **Gated (R7)** |
| 2 | `economics_entries` | research | `schemas/economics.py` | **Gated (R12)** |
| 3 | `source_value_extractions` | extraction | `schemas/source_value_extraction.py` | **Blocked on M4 — see §5** |
| 4 | `extraction_population_links` | extraction | `schemas/population_links.py` | R13; blocked with 3 |
| 5 | `spec_value_probes` | probing | `schemas/directness.py` et al. | Named in the PI |
| 6 | `probe_population_links` | probing | `schemas/population_links.py` | R13 |
| 7 | `reasoning_doc_citations` | verification | `schemas/reasoning_doc_citation.py` | 34 cols incl. locator scheme |
| 8 | `citation_population_links` | verification | `schemas/population_links.py` | R13 |
| 9 | `item_bpc_links` · `item_population_elaborations` | linkage | — | Render path; smallest, last |

Where a Pydantic model exists, validate through it — duplicating its rules in a `_validate_cols`
whitelist is the second copy that stops covering the first.

---

## 5. Sequencing against M4, and the two tables this plan does not write

Revision 1 said "no schema change proposed" and never mentioned the junction. That was not a
position; it was an omission. Stating it now:

**`specification_extraction_links` must land before Phase 2 items 3–4.** The probe's central
backward-walk finding is verbatim (`audits/2026-08-12c-pipeline-probe-log.md:12147`): *"0 rows — …
BROKEN JOINT: no table links specifications to source_value_extractions; the join must be improvised
on (ref_id, item_code) and item_code is nullable."* `workplan/2026-08-12-resolution-plan.md` §M4
schedules the junction among the **now-or-never** reshapes — now-or-never precisely because SQLite
has no `ADD CONSTRAINT` and both tables are empty **today**. Phase 2 items 3–4 write into exactly
the tables M4 wants to rebuild while empty. **Writers landing first either close that free window or
force copy-rebuild migrations later.** So: items 1–2 may proceed independently; items 3–4 wait on
M4.

**No writer for `specifications` is proposed here, and that is a gap, not a scope line.** It is the
table every walk terminates in. `assess_cell.py` is the only engine that computes a determination
and it refuses the canonical DB by design (`:487-492`). Who legitimately writes a determination is
an **owner question** (§6), not a tooling one — but a write path for the pipeline that cannot write
a determination is not finished, and revision 1 implied otherwise by listing nine tables and calling
that the set.

---

## 6. Phase 3 — What gets deleted, and one thing that must not be

| Delete | Because |
|---|---|
| `ENUM_GUARDS` + `check_enum_guards()` (~50 lines) | **Only after Phase 0 lands.** Until the CHECKs exist, this is the sole point-of-write guard on those vocabularies |
| `db.py`'s `_validate_cols` whitelists where a Pydantic model covers the table | Two vocabularies for one table is how they drift |
| **`assess_cell.py`'s `next_gap_id` re-implementation only** (`:426-429`, `f"GAP-{mx + 1}"` → `GAP-1`, against `^GAP-\d{3,4}$`; `db.py:156` has the correct zero-padded one) | The bug is real. **But revision 1 said "stops carrying its own write path", and that is wrong.** `assess_cell.py`'s separate path is a deliberate **owner-ratification boundary** — it emits a replay artifact headed *"Replayable onto the canonical DB ONLY after owner ratification"* (`:498-501`). Routing it through an auto-applying sink would push DG-NON-adjacent synthesis writes to canonical with no owner step. It is also one of `db_path_env_audit.py`'s two documented exemptions (`CLAUDE.md` §7). **Scope the deletion to the id allocator; the refusal stays** |

---

## 7. What this plan does **not** claim

- **It does not give on-demand, any-time, both-directions cell validation.** Phase 1 validates a row
  *at the instant it is written*. That is a different capability from taking one
  `(item × population)` specification, one extraction or one citation and re-deriving its standing
  on demand. Nothing here provides the latter, and **the backward direction is impossible for any
  tooling until §5's junction exists.** The read-side views (`v_item_provenance`, `v_source_reach`,
  `v_best_practice`) survive untouched — but by accident of the no-schema-change stance, not by
  design. Naming this as a separate, unbuilt capability rather than letting "validated" cover both.
- **It does not fix the four tables the probe cannot see** — `source_value_extractions`,
  `evidence_population_match`, `source_slug_links`, `case_studies` sit at 0 rows and were never
  flagged, because the probe detects write *statements*, not write *paths*.
- **It does not make the probe go green**, and should not until Phase 2 lands.

---

## 8. What the review overturned

| Revision 1 said | Corrected to |
|---|---|
| Deleting `ENUM_GUARDS` is safe — "superseded by real constraints on the scratch copy" | **False.** Neither column has a CHECK on either table, and no Pydantic model covers them. The deletion is gated behind a new Phase 0 that builds the constraints |
| "It proposes no schema change" | **Reversed.** One migration is required *first*, and it is cheap only while the tables are empty |
| Snapshot drift is "Risk 1", mitigated by the reproducibility gate | **The gate covers neither branch.** Promoted from a risk to a design requirement: apply-time re-validation, atomic snapshot, and a writer-serialization decision (§3a) |
| `assess_cell.py` "stops carrying its own write path" | **Scoped to the id allocator.** Its canonical-refusal is an owner-ratification boundary, not duplication |
| `emit_and_apply()` is "moved (not copied)"; "120 lines net" | Understated. It is coupled to the harness's globals; treat as a rewrite the harness imports |
| Nine tables is the set | Nine plus **`specifications`**, whose writer is an owner question and is not proposed here |

**What survived unchanged:** the diagnosis that the centralization already exists and lacks only a
sink; the 11→9 frozen-grid correction; that Phase 1 legitimizes twenty writers without rewriting
one; and that the existing write layer already enforces R9, R8 and R13 at the point of writing, so
the contract enforcement this inherits is real rather than assumed.

---

## 9. Sequence

0. **Phase 0** — the CHECK and UNIQUE migration, while the tables are empty.
1. **Phase 1** — the sink, with apply-time re-validation, the atomic snapshot, and the
   serialization decision made explicitly. Exercised on `insert_gap` first. Round-trip verified —
   emit, apply, rebuild, compare — not assumed.
2. **Phase 3 deletions**, once Phase 0 and 1 have both landed.
3. **Phase 2 items 1–2** — the gated tables. `research_batch_dod.py` is the acceptance test.
4. **M4's junction**, then **Phase 2 items 3–9** in stage order.

---

## 10. Owner rulings, 2026-08-13 — and how they compose

**Ruling 1 — split by confidence.** A session may freely record `pending`, `provisional` and
`not_applicable`. A **`stated`** determination — the confident claim, the guidebook's own voice —
requires owner ratification.

**Ruling 2 — uniform.** The sink behaves the same for every stage: emit and apply. No approval
queue, no out-tray, no per-stage mode.

### These compose better than the framing I offered

I said that if determinations needed sign-off, ruling 2 would answer itself — the machinery would
have to hold a change back for that one stage. **Taken together the rulings say something better:
the gate is not a held-back change, it is a refused one.**

Uniform apply forces the confidence split *out of the workflow and into the schema*. A session
cannot write a `stated` determination because a **constraint refuses it**, not because a slip is
waiting in a queue for attention. That is a promotion up this repo's own enforcement spectrum — a
constraint cannot be un-run, cannot examine nothing, and cannot be advisory — and it is **less**
code than a two-mode sink, not more.

Mechanism: a trigger on `specifications` that refuses `state='stated'` unless a matching
ratification row exists. SQLite `CHECK` cannot reference another table; a trigger can. This belongs
with the resolution plan's Part I, which already promotes invariants from prose into DDL.

**Consequence for Phase 0:** the ratification record and its trigger join the schema migration in
§2. Still cheap — `specifications` is at 0 rows.

### Ruling 1's second half: the vetting surface

*"Show text extracts or screenshots from the source where the determination is recorded, on a
backend version of the page, so I can easily vet the determinations."*

**Most of this exists.** `tools/spec-curation-vetting-surface.html` (40 KB) is regenerated from the
database by `tools/regenerate_vetting_surface.py`, lives in `tools/` rather than `site/` — so it is
already backend, not public — and already renders per-source extractions, synthesis-verified values,
selection walks and evidence spread. It is the right surface. Three things are missing, and they are
specific:

| Gap | Status | Work |
|---|---|---|
| **The verbatim extract is stored but not shown.** `source_value_extractions.claim_text` and `reasoning_doc_citations.claim_text` exist, with a full locator scheme beside them (`loc_division` … `loc_subclause`). The generator renders **zero** occurrences of `claim_text` — it shows values, not the words they came from | Data modelled, not rendered | Small. Render `claim_text` + locator next to each value |
| **The surface does not show the determination at all.** Its queries read `evidence_sources`, `items`, `populations`, `source_slug_links` and the three population junctions — **not `specifications`**. It shows the evidence, not what the evidence concluded | Blocked | Needs §5's `specification_extraction_links`. **This promotes M4 from "do it while the tables are empty" to a hard prerequisite of the ratification workflow** — you cannot vet a determination against its sources while nothing joins them |
| **Screenshots have no home anywhere in the schema.** Checked every table: no column matching screenshot / image / snapshot / scan / attachment / excerpt. Nothing | Not modelled | New. See below |

**On screenshots, one decision made and one concern raised.**

*Decided, as routine engineering:* images live as files under a versioned directory with a path
column referencing them — **not** as blobs in the database. The database is committed as a binary
and compared byte-for-byte by the reproducibility gate; page images would bloat it by orders of
magnitude and make every comparison slower for no gain.

*Raised, not decided:* a large share of the sources this project must vet are **paywalled
standards** — BS, ISO, CSA, national codes. Storing page images of those in the repository is a
copyright question, not a technical one, and the repository is intended to become public. A
**locator plus verbatim short extract** carries the same vetting power with far less exposure: it
tells you exactly where to look and what it says, which is what vetting needs. I would suggest
screenshots be reserved for sources that are freely licensed or for figures that cannot be conveyed
as text, with the locator-plus-extract path as the default. **Your call — I am flagging it, not
narrowing the request.** Both routes are built the same way.

---

## 11. Sequence, as ruled

0. **Phase 0** — one schema migration, while every affected table is empty: the two CHECK
   vocabularies, the `UNIQUE` on `doi`, **and** the ratification record plus the `stated` trigger.
1. **Phase 1** — the uniform sink, with apply-time re-validation, atomic snapshot and the
   serialization decision made explicitly. Round-trip verified, not assumed.
2. **Phase 3 deletions**, once Phase 0 and 1 have landed.
3. **Phase 2 items 1–2** — the gated research tables.
4. **M4's `specification_extraction_links`** — now a prerequisite of vetting, not a nicety.
5. **Phase 2 items 3–9**, and the vetting-surface work: render `claim_text` and the locator, then
   add the determination and its backward walk once the junction exists.

Still open, and narrowed to one question: **the screenshot scope above.** Everything else is ruled.
