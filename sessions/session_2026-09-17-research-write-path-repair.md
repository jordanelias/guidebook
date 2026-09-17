# The research write path was broken by migration 085, under a green battery

**Session id:** `session_2026-09-17-research-write-path-repair`
**Branch:** `claude/research-preparation-joue00`
**Asked for:** orient, and prepare to perform research.

> **NO RESEARCH RAN IN THIS SESSION, AND NO ROW WAS WRITTEN TO THE CANONICAL DB.** Every probe
> wrote to a scratch copy. This record is about the repair that had to happen before batch 10
> could run at all.

## What was found

Batch 10 was already prepared and unrun — priors and query plan committed ahead of any query, the
session id uncontaminated. Checking whether that preparation still held mattered because migration
085 landed **after** it merged. It did not hold:

```
$ python3 scripts/db.py log-search --slug accessible-circulation-geometry ...
sqlite3.OperationalError: table search_executions has no column named session
```

`log-search` is the first command of every research batch and the only way R8 — *log EVERY query
verbatim before screening* — can be met. `add-candidate` was broken identically on
`search_candidates.session`, which Leg C needs for candidate 69. `add-audit-run` was broken by 085's
drop of `item_audit_runs.session`.

## Why every gate was green over it

085 renamed eight `*_by_session` columns and four `*_at` columns. Its caller sweep was **empirical,
not grepped** — it ran the full check battery against a rebuilt DB. That is a better sweep than grep
and it still could not see this, because **no check writes a search execution.** The battery, the
registry selftest, and `column_vocabulary_audit` — the check 085 itself built — were all green while
the research write path could not accept a row.

CLAUDE.md rule 4 says a rename is not done until the callers are swept, and names a view, a skill
and the registry as callers it has been caught missing. **A writer exercised by no check is the
fourth, and the one the empirical method is structurally blind to:** the battery sweeps readers,
because reading is what checks do.

## The discriminator, and why the fix is not to retype the names

Every writer that reached for `dbcore.stamp_for(conn, table, session)` survived the rename
untouched — `gap_mining`, `supersession_check`, `pipeline_runs`, `url_verification_runs`,
`source_locators`. `stamp_for` reads the live schema and fills only the audit columns that table
actually has. The two writers that broke are the only two that spelled the column name as a string
literal beside it.

That is rule 8 exactly: the schema is the one home of a column's name, and a literal is a second
home. So the repair is not to type `created_by_session` where `session` used to be — it is to stop
typing it.

| File | Change |
|---|---|
| `scripts/db.py` | `log-search` and `add-candidate` derive audit columns via `stamp_for`; `add-audit-run` drops the deleted key |
| `schemas/search_execution.py` | mirrors the rename (§7: schemas ↔ SQLite drift is a bug) |
| `scripts/audit/derived_not_curated_audit.py` | second mechanically decidable class for rule 8 |
| `governance/check-registry.yaml` | entry documents the class; a hand-typed "91" replaced by the command that computes it |

## The enforcement, and its falsification

`derived_not_curated_audit` is rule 8 mechanised and already blocking, so the class went there
rather than into new apparatus. **What wrong thing reaches the guidebook without it:** a batch whose
searches cannot be recorded — research invalid by the research contract's own terms, discovered only
after the retrieval work is spent.

Falsified by re-introducing **both** original defects, in both of their shapes — a dict literal and
a subscript store — and re-running:

```
* scripts/db.py:511  builds the row `row` with column(s) executed_at, session
                     that search_executions does not have
* scripts/db.py:5911 builds the row `row` with column(s) session
                     that search_candidates does not have
```

Clean on the repaired tree, examining 18 row dicts. Re-derive rather than trust that figure.

**A first cut was thrown away rather than tuned.** It judged any dict matching the table on a
majority of its keys and produced fifteen findings — every one an `_emit` result payload echoing
the row, not one a real defect. A check red by construction teaches its reader to ignore it, which
is rule 6's own argument, and a 15-to-0 false-positive rate is worse than no check. The version kept
reads the row variable the INSERT is actually handed.

**What it does not catch, stated so a green result is not over-read:** a row assembled in one
function and inserted in another. `add-audit-run` escaped it by exactly that shape, and was found by
*running* the writers against a scratch DB. That remains the only complete caller sweep, and this
check is a tripwire for the commonest shape rather than proof the callers are swept.

## What was corrected elsewhere

The batch-10 record asserted a pre-state sha (`fdbb8612…`) and that it "must be unchanged when the
batch begins". 085 moved the blob to `608626c7…` hours later, so a session trusting the string would
have read a legitimate migration as contamination. Struck in place with the stale value visible, and
the invariant replaced with one that is actually about this batch: **no row carries this session
id** — verified, 0 rows across `search_executions`, `evidence_sources`, `specifications` and
`search_candidates`.

## State of readiness for batch 10

Nothing in batch 10's frame, priors or query plan changes. Verified rather than assumed:

- `log-search` and `add-candidate` write correctly to a scratch copy, `created_by_session` and
  `created_at` populated.
- `research_batch_dod.py --selftest` 19/19; the batch-10 session id fires **exactly R1, R9a, R9b** —
  the uncontaminated-id signature.
- `run_checks.py --selftest` PASS; `--changed-from origin/main` PASS.
- `emit_batch_sql.py --selftest` 9/9; `migrate_db.py --selftest` 14/14.
- The `QUERY-PLAN.md` richness table re-derives identically: one T4 international, or one T5 from a
  jurisdiction other than DE, flips the cell; a single new statutory code does not.

## What this session did NOT do

It did not run batch 10. It did not admit a source, log a search against the canonical DB, or emit a
migration. The five advisory check failures on this branch (`validate_schema_cross_check`,
`validate_pydantic_schemas`, `retired_vocabulary`, `test_verification_pipeline`,
`source_locators_integrity`) are pre-existing and untouched here; `test_verification_pipeline` is
named in CLAUDE.md rule 7a as asserting a corpus floor an owner ruling deliberately cleared, and
`source_locators_integrity` states in its own output that its repair is blocked on a writer that
does not exist.
