# Working notes — research batch 02, room-acoustic-performance

Kept per owner directive 2026-08-22: *"keep your scratch ... so that we can trace how it interacts
with all of our machinery and conversely we can see how much of our machinery isn't being used."*

This file is the human-readable trace. Two machine-derived companions sit beside it:
`commands.jsonl` (PostToolUse hook, every Bash call) and `machinery-trace.md` (generated at close:
what the batch touched, and what stayed idle).

## Step order actually followed (DR-2026-08-19 §12.1)

| Step | What ran | Outcome |
|---|---|---|
| 0 pre-state | `sha256sum`; `research_batch_dod.py --selftest`; `--session <S>`; | sha `abc71e24…`; selftest PASS 15/15; DoD exit 1 with **exactly one** failure, R1 — the runbook's predicted signature for an empty session |
| 1 scratch | `cp data/guidebook.db $SCRATCH/batch02.db` | canonical untouched from here to step 11 |
| 2 frame | `db.py coverage`; SQL over `items`/`item_population_links`/`search_executions`/`terms` | 10 served populations; **DEAF absent**; 9 prior executions read, none deleted (R8) |
| 3 log | 6 literature queries + 1 stash lookup, all logged **before** screening | exec 10–16 |
| 4 screen | top-10 of each read; 65 screened total | candidates staged at R7 floor |
| 5 R9 pre-check | hand SQL against **both** `evidence_sources` and `source_locators` | 3 held leads → reuse; 2 unheld → mint from REF-00969 |
| 6 R10 re-retrieve | `retrieval_log.fetch` → Crossref, payloads persisted | 5 resolved; 1 transient TLS failure recorded, ladder retry succeeded |
| 7 admit | `db.py add-source` ×5 + mandatory companion UPDATE | all 5 `doi_resolution_outcome='RESOLVED'` |
| 8 grade | 13 `evidence_population_match` rows | 1 EXACT · 4 PARTIAL · 2 PROXY · 6 MISMATCH |
| 9 mine | R2 floor = admissions//4, min 1 | see below |
| 10 route | R12 — **no** `jurisdictional_values` write (2026-08-12 ruling; DR §12.1 Step 10 carries an interim STOP) | — |
| 11 gate/emit/apply | DoD on scratch → `emit_batch_sql` → `emit_data_migration` → `migrate_db` | — |

## Decisions taken inside the batch, and why

- **REF-00969 tiered DOWN, deliberately.** Same team and cohort as REF-00965, which carries `co1`/T1.
  OD-D disputes exactly that lineage's co-production warrant, so admitting a sibling at Co-1 would
  compound a disputed grade. Graded `clinical`/`lower_control` → T3. Re-grade **up** if OD-D sustains.
- **REF-00561 attributed to exec 16, not exec 13.** It did not appear in the top results of any of
  the six literature queries. It reached admission through the stash lookup, prompted by a
  hand-written adjudication. Attributing it to the AUT query would have been tidier and false.
- **MB2-004 / MB2-007 capped at PROXY.** The strongest Tier-1 evidence on this parameter studies
  deaf and hard-of-hearing *children*, and DEAF carries **zero** `item_population_links` on this
  slug. A Tier-1 study with a hard number is still PROXY when its population is not the one served.
- **My own error, caught before it reached a field.** I wrote in exec 14's note that Iglehart's
  second paper was 2019, inferring from the DOI slug `2019_AJA-19-0010`. The payload says **2020**.
  The reasoning doc was right and I was wrong. Corrected in the row before any admission was written.

## What this batch did NOT do

- No `specifications` row. D-0165 defers the population-taxonomy question, so no cell on this slug is
  authorable; that is act 5 and it remains blocked.
- No `jurisdictional_values` write, by ruling.
- No full texts read. Every value attributed to a source in prose is `[UNVERIFIED-QUANT]`; **no
  numeric value was written into any value column.**
- No Italian-language sweep. Exec 15 was posed in Italian and the engine answered semantically in
  English; that is a topic search, not language coverage, and the row says so.
