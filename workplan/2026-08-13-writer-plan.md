# 2026-08-13 — Writers: a plan under "less code, more centralization"

**Owner instruction:** *"Plan out writers within the context of our existing infrastructure under
the maxim of less code, more centralization."*

**The plan is subtraction, not addition.** The centralized writer already exists. It is
`scripts/db.py` — 1,889 lines, 20 write functions, all of one shape. What it lacks is not
functions; it is a **sink**. It commits to `data/guidebook.db` directly, which `CLAUDE.md` §4
forbids, so its entire write layer is unusable against the canonical database. The migration
emitter it should be feeding exists too, and so does the glue — in a test harness.

Three pieces, built separately, never joined:

| Piece | Where | What it does | Why it is not enough alone |
|---|---|---|---|
| The write layer | `scripts/db.py` | 20 functions writing 12 tables, every one shaped `with connect() as conn: conn.execute(sql, params)` | Commits straight to the canonical DB — the one thing the write discipline forbids |
| The emitter | `scripts/emit_data_migration.py` | Wraps SQL in a timestamped, transaction-bounded migration | Takes **text**. Someone must hand-write the SQL |
| The glue | `scripts/tests/walk_harness.py:183` `emit_and_apply()` | Runs emitter → `migrate_db.py`, the sanctioned two-step | Lives in a test harness and **refuses to run outside a disposable tree** |

Joining them is one change. Everything else in this plan follows from it.

---

## 1. First, a correction to my own count

`workplan/2026-08-13-writerless-tables-analysis.md` and PR #99 say **eleven** tables need writers.
**Two of the eleven must not get one**, and I did not check before writing that.

`search_coverage` and `search_languages` were **deliberately frozen on 2026-08-06**.
`scripts/db.py:316-326` raises `FrozenGridError` on any write, with a 37-line comment explaining
why: they were hand-kept state grids that drifted from the search log **in both directions** —
634 cells claimed SEARCHED with 15 corroborated by an execution, while 31 executions landed on
cells the grid called NOT-RUN. `workplan/search-coverage-completion-workplan.md` replaced them with
the `search_executions` log plus derived views (`v_coverage_jurisdiction`, `v_coverage_language`,
`v_coverage_branch`).

I also wrote that `search_languages` is *"GATED — R11"*, implying a tool is needed for the gate to
pass. **That is wrong on both counts.** `research_batch_dod.py` reads `search_executions`, not the
grid. The gate is already satisfied by the log.

**Building writers for those two would un-freeze a retirement and re-open the drift.** They are
correctly writerless, and the probe should keep reporting them — a table with no writer *by design*
looks identical to one with no writer *by omission*, which is exactly why the distinction has to be
written down rather than inferred from a count.

**Corrected: nine tables need a writer, not eleven.**

---

## 2. Phase 1 — Redirect the sink. One function. No new writers.

Today, every `db.py` write does this:

```python
with connect(dry_run) as conn:
    conn.execute(f"INSERT INTO gaps ({cols}) VALUES ({ph})", list(row.values()))
```

`connect()` (`db.py:55-72`) opens the canonical DB and commits. Change **that one context manager**
so a write can be *recorded and emitted* instead of committed:

- Open a **scratch copy** of the canonical DB, not the canonical file. Reads inside the function
  still work, `lastrowid` still works, and — critically — **every FK, CHECK and UNIQUE constraint
  in the real schema validates the write before it is emitted.**
- Record each `(sql, params)` pair as it executes.
- On clean exit, render the recorded pairs as literal SQL and hand them to
  `emit_data_migration.py`, then apply with `migrate_db.py`. That is `emit_and_apply()`, moved out
  of the test harness into `db.py` where production callers can reach it.
- On exception, emit nothing. A failed write leaves no migration.

**What this costs:** one rewritten context manager, one small recording proxy, and a function moved
(not copied) out of `walk_harness.py`. Call it 120 lines net, with a deletion on the other side.

**What this buys:** all 20 existing write functions become legitimate against the canonical
database for the first time — `insert_gap`, `insert_connection`, `insert_conflict`, `insert_item`,
`add-source`, `log_search`, `log_mining`, `update-bpc`, `insert_audit_run` and the rest. Not one of
them is rewritten. The `dry_run` flag they already accept keeps its meaning: emit nothing.

**This is the highest-leverage change available and it writes none of the nine tables.** It should
land and be exercised on its own, before any new table is touched.

### Why the scratch copy rather than emitting SQL blind

Because the alternative is what we have now. `emit_data_migration.py:66-108` carries `ENUM_GUARDS`
— fifty lines of **regex over SQL text**, scanning for `col='VALUE'` patterns, with a comment
recording that the same bad value was written twice in one day and that prose did not stop the
repeat. It guards **two columns**. It cannot guard more, because guessing a column's value from
positional INSERT text is not decidable by regex.

Bind the parameters and apply them to a real schema instead, and every CHECK constraint on every
column of every table enforces itself — for free, with no list to maintain. **That is the
centralization: not one more validator, but the one that already exists doing the work.**

---

## 3. Phase 2 — Nine functions, one shape, no new files

Each missing table gets one function following the shape already used twenty times:

```python
def insert_<table>(data: dict, session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols, ph = ", ".join(row), ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO <table> ({cols}) VALUES ({ph})", list(row.values()))
    return row["<pk>"]
```

Plus one `add_parser` line each on the existing CLI. **No new module, no new abstraction, no
per-stage emitter.** Ordered by what the gates already demand:

| # | Table | Stage | Pydantic model | Notes |
|---|---|---|---|---|
| 1 | `search_candidates` | research | — | **Gated (R7)**: off-slug material must land here, not in prose |
| 2 | `economics_entries` | research | `schemas/economics.py` | **Gated (R12)**: economic data must land here, not in prose |
| 3 | `source_value_extractions` | extraction | `schemas/source_value_extraction.py` | Not in the eleven — has a writer somewhere, still 0 rows. See §5 |
| 4 | `extraction_population_links` | extraction | `schemas/population_links.py` | R13 |
| 5 | `spec_value_probes` | probing | `schemas/directness.py` et al. | Named in the PI |
| 6 | `probe_population_links` | probing | `schemas/population_links.py` | R13 |
| 7 | `reasoning_doc_citations` | verification | `schemas/reasoning_doc_citation.py` | Named in the PI; 34 columns incl. a full locator scheme |
| 8 | `citation_population_links` | verification | `schemas/population_links.py` | R13 |
| 9 | `item_bpc_links` · `item_population_elaborations` | linkage | — | Render path; smallest, do last |

Six of the nine already have a Pydantic model. **Where one exists, validate through it** — the
model is the vocabulary, and duplicating its rules in a `_validate_cols` whitelist is the second
copy that stops covering the first. Where none exists, the table's own CHECK constraints do the
work via the scratch copy; a model can follow when the shape settles.

---

## 4. Phase 3 — What gets deleted

A plan that only adds has not centralized anything.

| Delete | Because |
|---|---|
| `ENUM_GUARDS` + `check_enum_guards()` (`emit_data_migration.py`, ~50 lines) | Superseded by real constraints on the scratch copy, for every column rather than two. **Keep the emitter's risky-pattern warnings** — those guard hand-written SQL, which stays legal |
| `emit_and_apply()` in `walk_harness.py` | Moved into `db.py`, not copied. The harness imports it |
| `db.py`'s `_validate_cols` whitelists, where a Pydantic model covers the same table | Two vocabularies for one table is how they drift |
| `scripts/assess/assess_cell.py`'s separate write path | It re-implemented `next_gap_id` and got the format wrong (`GAP-1` against `^GAP-\d{3,4}$`) while `db.py:149` already held the correct one. It should call the library, not carry a second one |

---

## 5. What this plan does **not** claim

- **It does not fix the four tables the probe cannot see.** `source_value_extractions`,
  `evidence_population_match`, `source_slug_links` and `case_studies` sit at 0 rows and were never
  flagged, because the probe detects write *statements*, not write *paths*. Phase 2 covers the
  first; the other three need the same audit this document did for the nine — **do not assume they
  are fine because a counter did not name them.**
- **It does not make the probe go green**, and should not. Until Phase 2 lands, the count is a true
  measurement of an absence. Silencing it would restore the mask the baseline removed.
- **It proposes no schema change.** Every table exists with its FKs; six have models. This is a
  tooling gap, not a modelling gap — and a plan that widened the schema first would be solving the
  wrong problem twice.

---

## 6. Risks, named

1. **The scratch copy must be a copy of the *committed* DB, and the emitted migration must apply
   cleanly to it afterwards.** If the two diverge, the reproducibility gate catches it — but as a
   mystery, one commit later. Phase 1 must therefore verify round-trip on its first run: emit,
   apply, rebuild, compare. Not "it should work."
2. **Recording `(sql, params)` and rendering literals is a serialisation boundary.** Byte values,
   NULLs and floats each have a wrong rendering that looks right. The renderer needs a test with
   those three cases before it carries a real write, and the test should tamper with it and watch
   it fail — a serialiser nobody has watched break is not verified.
3. **Every write becomes a migration, so migration count grows with research volume.** That is the
   design working, and the baseline mechanism now exists to compress it (D-0160). It is worth
   saying out loud that the freeze we just performed is the pressure valve for this plan.
4. **`db.py` is 1,889 lines and this makes it more central, not less.** The maxim says
   centralization, and I am taking it at its word — but the honest cost is that one file becomes
   more load-bearing. The mitigation is that it gains a sink and nine six-line functions, not
   nine subsystems.

---

## 7. Sequence

1. **Phase 1 alone**, exercised on an existing writer (`insert_gap` is the smallest), with the
   round-trip verification of risk 1 and the serialiser test of risk 2. Nothing new is writable
   yet; the twenty that exist become legitimate.
2. **Phase 2 items 1–2** — the two gated tables. `research_batch_dod.py` already states what a
   complete research batch must contain, so it is the acceptance test, not a new one to write.
3. **Phase 3 deletions**, once Phase 1 has carried a real write.
4. **Phase 2 items 3–9**, in stage order, as the pipeline reaches each.

Phases 1 and 3 are the "less code" half; phase 2 is nine six-line functions. **No new file is
proposed anywhere in this plan.**
