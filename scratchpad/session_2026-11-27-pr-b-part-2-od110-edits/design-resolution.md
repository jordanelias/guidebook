# Resolution of the antagonist's verdict on the T-117 / T-056 item 3a design

Coordinator's file, 2026-11-27. Inputs: `design-t117-t056.md` (agonist), `antagonist-t117-t056.md` (blind antagonist). Where this file and the design differ, **this file governs**. Nothing here decides an owner question; each item names the ruling it rests on. The antagonist's evidence commands are in its file; re-run them, do not trust them.

## Decisions

| # | Claim | Decision | Basis |
|---|---|---|---|
| 1 | Claim 6, engine reads the retrieval log | **Dropped.** The engine reads no log. A non-VERIFIED source that states the shown value refuses the cell, naming OD-99 (Q1) and OD-100. The "could not be retrieved" test (OD-99 Q2 (b)) lives in C10 only, as OD-99's interim text has it. | `retrieval_log.LOG_ROOT` is cwd-relative, so an engine reading it changes who governs and `derivation_sha`; that is eligibility, which OD-110 defers; T-117 section 8 forbids more than the marker. |
| 2 | Claim 2, refusal text | The refusal names every open question that blocks the cell (OD-92 and OD-99 for 3 x MOB), not the first. | Antagonist M6. |
| 3 | Claim 5, refuse unretrieved T1 to T3 | **Dropped.** | No live subject, duplicates C10, mis-cites OD-99 Q2; OD-95 reads "do nothing now". |
| 4 | Claim 7, rso flip | Kept, and `tier_basis` moves with it so the stored text no longer says `regulatory_stratum_only` where rso is 0. | Antagonist M5. |
| 5 | Claim 9, `directness.py` comment | **Dropped** (no edit to the comment). `design_scale` from the key is kept; the two meanings of `universal` (`directness.py`, `matrix_consistency.py`) are listed as a caller finding in the PR body, not edited. | Antagonist M2. |
| 6 | Claim 10, mixed marks on a cell with no value | Status quo (R7's floor mean) for a cell that shows no value. The refusal on a mix of the warning marker and circles is **not built**: it waits on OD-92. A cell that shows a value and has a non-VERIFIED stating source is refused per decision 1. | OD-92 words are "stating sources"; antagonist M3. |
| 7 | Claim 11, `own()` | `own()` is lifted out of `determine` so a test can call it, and it uses `_verified`, not a literal `"VERIFIED"`. | Rule 8 (one home); antagonist M8. |
| 8 | Claim 12, T-117 task file | **First commit of the PR**: edit T-117 item 4 (remove PROXY and `rests_on_proxy_inference` as thin causes and the `population_match` parent extension: OD-98), item 4a and T117-07 (OD-99's interim text replaces "triangle passes C10"), item 5 (an `AFTER_DATA` marker is not required), tests T117-03 (grey half), -04, -06, -08 (PROXY-thin: goes), -09, -11(d) as the antagonist's section 2.2 and the design's claim 12 list them. Every edit is recorded in the PR body under "Task-file defects". | Ledger entry "Delegated resolutions 2026-11-27", ACTION (1): task-file edits before acting. |
| 9 | Richness trap (M4) | A test must have a cell that is not below section 2.3 richness, or it cannot go red; the implementer picks a fixture on a scratch copy and states how it was built. A test whose red state cannot be shown on HEAD is not written. | CLAUDE.md section 5(a). |
| 10 | One PR for two tasks (M7) | **Kept, stated.** The owner asked for T-056 item 3a alongside. Both change `determine` and share one `RULE_VERSION` bump. The PR body says it departs from "one task, one pull request" and leaves T-056 open for items 1 to 3 and 5. | Owner's "yes" of 2026-11-27 to T-056 item 3a alongside. |
| 11 | `governance/tier-system.md` line 81 | Not edited (T-117 item 6 forbids governance edits). Listed for T-120 in the PR body. | Antagonist: stale, not false. |

## Built, waiting, out

- **Build now:** `band()` to the ruled table; the warning marker with no ordinal; `floor_mean` over circles only; delete the rso override; marker from the stating rows (OD-59) with the refusal of decision 1; the `specifications.marker` CHECK rebuild (number and object list derived from `sqlite_master`); C10 per OD-99's interim text; `design_scale` from the key (T-056 item 3a); the task-file edits of decision 8.
- **Waits for the owner:** OD-92 (mixed stating markers), OD-99 Q1 and Q2 (which marker a retrieved-but-UNVERIFIED source carries, and how "could not be retrieved" is shown), OD-95, OD-100, Q3 (PROXY-thin).
- **Out of this PR:** the T-059 selection slice and eligibility union (OD-101, OD-110); any engine read of the retrieval log; the `worse_at` harm record (OD-102); the `tier-system.md` edit.
