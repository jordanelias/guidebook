# pr-143 — orientation, and the write path that was broken

**Branch:** `claude/research-preparation-joue00` · **PR** #143
**Session id:** `session_2026-09-17-research-write-path-repair`

## What this session was asked to do, and what it found instead

Orient, and prepare to perform research. Batch 10 was already prepared — `PRIORS.md` and
`QUERY-PLAN.md` committed before any query, the pre-state probe recorded, the session id
uncontaminated. Preparing to run it meant checking that preparation still held, because
migration 085 landed **after** it merged.

It did not hold. `scripts/db.py log-search` — the first command of every research batch, and the
only way R8 ("log EVERY query verbatim before screening") can be met — raised:

```
sqlite3.OperationalError: table search_executions has no column named session
```

`db.py add-candidate` was broken the same way (`search_candidates.session`), and `add-audit-run`
by the drop of `item_audit_runs.session`.

## Why every gate was green over it

Migration 085 renamed eight `*_by_session` columns and four `*_at` columns. Its caller sweep was
**empirical, not grepped** — it ran the full check battery against a rebuilt DB, which is a better
sweep than grep and still could not see this, because **no check writes a search execution.** The
battery, the registry selftest and `column_vocabulary_audit` (the check 085 itself built) were all
green while the research write path could not accept a row.

That is CLAUDE.md rule 4 ("a rename is not done until the callers are swept") meeting failure mode
(a) ("a gate that passes having examined nothing"). The reader-side callers were exercised by the
battery and swept correctly; the writer-side ones were not exercised by anything.

## The discriminator, and why it is the fix

Every writer that reached for `dbcore.stamp_for(conn, table, session)` survived the rename
untouched — it reads the live schema. `gap_mining`, `supersession_check`, `pipeline_runs`,
`url_verification_runs` and `source_locators` were all fine. The only two that broke are the only
two that spelled the column name as a string literal. That is rule 8 in miniature: the schema is
the one home of a column's name, and a literal beside it is a second home.

So the fix is not to retype the new names — it is to stop typing them.

## What changed

| File | Change |
|---|---|
| `scripts/db.py` | `log-search` and `add-candidate` derive their audit columns via `stamp_for`; `add-audit-run` drops the deleted `session` key |
| `schemas/search_execution.py` | mirrors the rename (§7: schemas ↔ SQLite drift is a bug) |
| `scripts/audit/derived_not_curated_audit.py` | second class: a writer naming a column its table does not have |
| `governance/check-registry.yaml` | entry documents the new class; a hand-typed "91" replaced by the command that computes it |

## The check is falsifiable, which is the only reason it is worth having

Proved by re-introducing **both** original defects and re-running:

```
* scripts/db.py:511  builds the row `row` with column(s) executed_at, session
                     that search_executions does not have
* scripts/db.py:5911 builds the row `row` with column(s) session
                     that search_candidates does not have
```

Clean on the repaired tree, examining 18 row dicts — not vacuous.

A first cut used a majority-of-keys heuristic and produced **fifteen findings, every one a result
dict and not one a real defect.** It was replaced rather than tuned: a check red by construction
teaches its reader to ignore it, which is rule 6's own argument. The version kept reads the row
variable the INSERT is actually handed, so an `_emit({...})` payload echoing the row is never
judged as a row.

**What it does not catch, so a green result is not over-read:** a row assembled in one function and
inserted in another. `add-audit-run` escaped it by exactly that shape and was found by *running*
the writers against a scratch DB. That remains the only complete caller sweep.

## State of readiness for batch 10

- Write path: `log-search` and `add-candidate` verified working against a scratch copy, rows landing
  with `created_by_session`/`created_at` populated.
- `research_batch_dod.py --selftest` 19/19; the batch-10 session id still fires **exactly R1, R9a,
  R9b** — the uncontaminated-id signature.
- `run_checks.py --selftest` PASS; `--changed-from origin/main` PASS.
- `emit_batch_sql.py --selftest` 9/9, `migrate_db.py --selftest` 14/14.
- The richness table in `QUERY-PLAN.md` re-derives **identically** — one T4 international or one T5
  from a jurisdiction other than DE flips the cell; a single new statutory code does not.
- **The canonical DB is untouched.** All probe writes went to scratch copies.

## The pre-state figure in the batch-10 record was stale

That record asserts `sha256sum data/guidebook.db` is `fdbb8612…` and "must be unchanged when the
batch begins". Migration 085 moved it to `608626c7…` hours later. A session trusting the recorded
string would have read a legitimate schema migration as contamination. Corrected in place, struck
clause left visible — the record's own instruction to re-derive rather than trust the string is what
saved it, and is the reason the instruction is written that way.

---

# Part 2 — batch 10 ran

With the write path repaired, the batch the repair existed for was executed. Four of fourteen
planned executions: Leg A rows 1–3 (JP, FR, GB) and Leg D row 11 (Co-1). Full record in
`sessions/session_2026-09-17-research-batch-10-ramp-gradient-threshold.md`, now closed.

## The result

**Row 1 falsified its own prior, which is the most valuable thing the batch produced.** The corpus
held `REF-00989`, a Co-1 source attributing three gradient figures to "the Barrier-Free Law". Two
are in Cabinet Order 379/2006. The third — 1/15 — occurs **zero times** in that Order; it is in
MLIT Ordinance 114/2006, the *voluntary* 誘導基準. So the corpus held a lived-experience assessment
of a legal figure that merged a mandatory instrument with an aspirational one. Nothing in Japanese
law requires 1/15.

**Row 3 broke the comparison the batch was heading toward.** AD M conditions gradient on the
*going* of a flight: 1:12 is UK-legal only for a 2 m going (166 mm rise). The US and Japanese 1:12
carry no length term in the same clause. Regulatory richness now clears on "3 T6 codes from 3
jurisdictions" — and the engine's own verdict says *value-level convergence unverified*, which row
3 gives positive reason to believe is false.

**The determination was retired, not recomputed.** Recomputing would publish a regulatory-floor
claim as though it answered what a wheelchair user can actually climb.

## Three more write-path defects, found by running it

Each was found by the batch hitting it, not by reading code:

1. **`add-source --slug` reported a link it never wrote** — gated on `--local-ref-id` while
   `_emit` announced `linked_slug` unconditionally. Now refuses.
2. **The verbatim guard could not read CJK numerals.** It checked that `claimed_value`'s Arabic
   digits appear in the quote; a Japanese statute writes 十二分の一. `--verbatim-exempt` was
   correctly refused because the text *did* verify, so there was no path at all — **every CJK
   statutory value was unfilable.** R5 says non-English work is not lesser; the guard made it
   unwritable. Now normalises CJK numerals, and still rejects fabricated figures.
3. **A refusal fired after its own INSERT**, leaving an orphan admission (`REF-09999`) that the
   DoD gate caught on R3 and R11-harvest. My own defect, introduced in fix 1 and moved to where
   argument checks belong.

The batch is captured as `replay-batch-10.sh` — rebuild from canonical, replay, diff. That is how
the orphan was proved gone rather than argued away.
