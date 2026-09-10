# Road to batch 06 — the walk, and what blocks a believable determination

An executed walk of base → research → evidence → judgment → specification on a scratch
copy (`sha256` verified identical to canonical before starting; canonical never opened
read-write). The plan below is triaged by ONE question: does it block the walk?

## THE HEADLINE

**The pipeline runs end to end today. Nothing mechanical stops a batch.** Steps 1–6 all
completed on the scratch: a parameter minted (`TERM-089` → `parameter_id 1`), a source
admitted with `scope` recorded, terms observed and adjudicated, the engine emitted a
determination, `emit_batch_sql` → `emit_data_migration` → `migrate_db` replayed it
cleanly with `PRAGMA foreign_key_check` empty, and **`research_batch_dod.py --session`
returned `COMPLIANT`, 18 rules PASS.**

## WHAT STOPS A *BELIEVABLE* BATCH

**The specification the engine emits is about the SLUG, not the parameter.**
`assess_cell.gather_sources(conn, slug)` (`:178`). `parameter_id` is used only in the
docstring, `sha()`, `determine()`'s signature, the report dict and `validate_parameter()`
— it never gathers evidence. So `param 1 × MOB → stated basis=T1+CO1+T2` was anchored on
all 10 sources linked to the slug, **8 of which the engine's own report flags
`tier_inconsistent`**, and every one of the 10 DOWN-WEIGHTED.

The cause is one table: **`db.py` contains zero references to `source_value_extractions`**
(only `dbcore.py:504`'s `WRITABLE_TABLES` entry). With no extraction writer there is no
parameter→evidence edge, so the engine has nothing to gather by but the slug. The
re-key was cosmetic at the point where it decides.

## BLOCKING, in dependency order

**B1 — the research contract tells every session the key is still open.**
`governance/research-contract.yaml:119`: *"What a cell keys on is an open owner
decision"* — false since migration 071. Every session reads this in the SessionStart
hook, so a session never reaches step 1. The file is hash-pinned by the blocking
`research_contract_sync`, so the line and `research_contract_hook.py --write` must land
in the SAME commit.

**B2 — no runbook for the walk exists.** The walk had to be assembled from `--help`.
`DR-2026-08-19 §12.1` is stale: step 4 says "No CLI; scratch SQL" (`add-candidate`
exists), step 7 orders a hand-SQL companion UPDATE (`add-source` now takes those flags),
and no step mentions `observe-term`, `add-term`, `add-parameter`, `adjudicate-term` or
the engine. `grep -ln "add-parameter\|observe-term\|adjudicate-term" skills/*.md` returns
nothing. Two hazards must be written down: **discard the engine's `--emit-sql` file when
the engine ran on the session scratch** (`emit_batch_sql` captures those rows, and
replaying both collides on `convergence_assessment.convergence_id`), and **regenerate
derived outputs before the gate**. Also: `db.py next-id` offers only
`{connections,gaps,terms,conflicts}` and the refusal sends you to a Python function — add
`next-id ref`.

**B3 — the cron's wake condition is reachable by a batch.** `verify_urls.py:447-470`
writes `url_verification_runs` (NOT in `EXEMPT_TABLES`) only for a source with
`url<>'' AND verification_status IS NULL`. Today the pool is empty and `git log` shows no
url-verification commit has ever landed — but `add-source` accepts a NULL status
(`db.py:2384` branches only on `VERIFIED`), and R10 examines VERIFIED rows only. One such
admission and the 15th 06:00 UTC fire pushes a blob to main, reddening
`migration_reproducibility` for every open DB PR. Fix the DoD predicate, not the cron —
the cron is owner decision #5.

**B4 — the extraction writer and the engine's subject.** Migration 073: give
`source_value_extractions` `parameter_id NOT NULL`, retire `item_code`/`population_code`
(0 rows, no data migration ever INSERTed — droppable) for the four lens columns under
D-0182's CHECK; `db.py add-extraction`; and `gather_sources` joins on
`(ref_id, parameter_id)` rather than slug. Value directness stays `NOT_ASSESSED` — no
grading rule is invented.

**B5 — the engine anchors `stated` on tiers it reports underivable.** Two halves: make a
`tier_consistent == False` source non-anchoring; and re-derive `scope` for the 8 canonical
sources from the retrieval-log payloads via `amend-source --field scope`, which refuses
any scope contradicting the stored tier.

**B6 — two specification-stage skills teach the retired key.**
`specification-curator_SKILL.md:70-72` and `item-specification-writer_SKILL.md:91`. A
session at the last stage writes a row the table refuses.

**B7 — process:** `regenerate_derived.sh` after `migrate_db.py`, before the gate. Both
freshness gates go red after every batch migration otherwise.

## DELIBERATELY WAITING

G2/G3/G6 promotion (Q4) — the engine's copy is the one in use. `check_rendered_docs`,
`population_page`, `spec_page`, `pilot_renderings` — render stage, not on the walk, and
`regenerate_derived.sh` does not call them. `base-parameter-vocabulary` pointing at
`validate_items` — advisory, cannot block. The `check_values` third-form conflation and
the stale `no_floor` exemptions — every refusal on the walk fired correctly. **No
re-determination path** (`idx_spec_row_identity` refuses a second run) — batch 06 is the
first determination of any cell; batch 07 needs a supersede design.

## STOP CONDITIONS — owner, not agent

1. Decision #5, the verify-urls cron. Do not edit it.
2. A source's study design contradicting its stored tier during the scope re-derivation —
   tier is an adjudicated judgment; changing it is content.
3. A ruling on `source_value_extractions` shape found in `sessions/` that this plan did
   not cite — record the supersession first.
4. Any step needing a value-directness grading rule. None exists. Do not invent one.
5. Batch 06's subject: continuing `accessible-circulation-geometry` needs no decision; a
   new slug is content and does.
6. After B4, any `stated` cell whose governing set includes a source with no extraction
   for that parameter — do not merge the migration.
