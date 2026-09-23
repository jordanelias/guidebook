# Protocol-conformance audit — PRs #116–#157 (merged 2026-08-24 … 2026-09-21)

**VERDICT: PARTIAL CONFORMANCE.** The letter of the protocol mostly held: every PR merged with the final head green or explicitly waived, every synthesis-path PR carried an attestation, every research batch from 05 onward ran the DoD gate to COMPLIANT, and R10 is clean. What failed is concentrated in four places. (1) The **append-only search log was deleted and its ids reissued**, and the DoD R8 gate cannot see that. (2) **R2 forward mining was never run** on most T1–T2 anchors, and the R2 gate passes regardless. (3) The **adversarial pass that DR-2026-08-19 §7 binds to data diffs** is missing from five DB-touching PRs. (4) **GitHub-side review is empty**: no reviews, no review threads and no approvals check on any of the 42 PRs, merges were not gated on CI, and 8 PRs merged while CI was still running on the final head.

Scope and method: this was a read-only pass. Following the owner instruction received mid-task, no check suites were run after it arrived. Evidence comes from GitHub REST (via proxy), `git log`, the read-only DB (`PRAGMA user_version` = 95) and `transcripts/harness_*/main.jsonl`. Helper scripts and raw data are in this scratchpad: `gh_fetch.py` → `gh/prs.json`, `order.py`, `dod.py`. Transcripts start at **2026-09-01T20:12**, so **#116–#125 have no transcript** and every transcript-based claim for them is [GAP].

---

## 1. Findings, worst first

### F1 — CRITICAL — The R8 append-only search log was deleted, its identifiers were reissued, and the gate is blind to it (#136, then #137/#140/#143)
- `data_20260913040739_2026-09-13-clear-circulation-corpus.sql:107` runs `DELETE FROM search_executions WHERE slug = 'accessible-circulation-geometry'`. This is the owner-ruled corpus clear, merged in #136.
- `search_executions.exec_id` has no AUTOINCREMENT, so batches 08–10 **reused exec_id 29–48**, the ids that batches 05–07 had held.
  - Live data: `select created_by_session,min(exec_id),max(exec_id) from search_executions group by 1` shows batch 08 at 29–32, 09 at 33–42, 10 at 43–46.
  - Deleted data: the batch 05 migration inserted 29–43 and the batch 07 migration inserted 47–48. Derived by regex over `scripts/migrations/data_*batch-0[5-7]*.sql`, `INSERT INTO search_executions (...) VALUES (<id>`.
- **Permanent records now point at the wrong rows.** `sessions/session_2026-09-02-research-batch-05-circulation-icf.md:85` ("exec 34 logged a…") and `sessions/session_2026-09-13-research-batch-07-corridor-width.md:39,91` ("exec 47", "exec 44") now resolve to batch-09 and batch-10 rows.
- **The DoD R8 check is defeated by construction.** It detects deletion as `max(exec_id) > COUNT(*)` (`scripts/audit/research_batch_dod.py:455-463`). Reissue fills the gap, so max = count = 91 (`select max(exec_id),count(*) from search_executions`), and R8 reports "no deleted rows".
- **The repair sweep missed this key.** 6cd99a1 ("an identifier is never reissued", 2026-09-13) fixed reissue for `base_parameters` and `specifications` only. `_INT_KEYS` in `scripts/audit/identifier_floor_audit.py:62-69` covers only those two tables, and `sqlite_sequence` has no `search_executions` entry (`select * from sqlite_sequence`).
- No record acknowledges this (`git grep -iE 'exec_id.{0,40}(reuse|recycl)'` returns 0 hits).
- Rule 0 does license the deletion: the owner ruled the rows untrusted. What rule 0 does not license is recording the clear as "compensating, append-only" (migration header, lines 16–19) while the identity guarantee R8 depends on was lost.
- Rules and clauses: R8 ("Never delete or backfill"), CLAUDE.md rule 4 (a key is a caller), rule 8.
- `search_candidates.candidate_id` may have the same problem [UNVERIFIED].

### F2 — HIGH — R2 forward mining is absent on 7 of 12 T1–T2 anchors, yet they are recorded as `mined` (#137, #152, #155)
- Command: `select count(*) from citation_mining cm join evidence_sources es on es.ref_id=cm.global_ref_id where es.tier<=2 and cm.forward=0 and cm.deferred_reason is null` returns **7**, out of **12** T1–T2 sources (`select count(*) from evidence_sources where tier<=2`).
- The seven: REF-00983, 00984, 00985, 00986 (batch 08); REF-00979, 00980 (batch 16); REF-01006 (batch 19). All seven carry `citation_mining_status='mined'`.
- R2 requires "backward AND forward". The owner ruling in GAP-022 says "deferred is okay so long as it runs eventually", but these rows are not deferred either; the forward direction was simply never logged.
- The gate counts presence of a mining row, not direction (`research_batch_dod.py:~331`). daac431's own comment says so: "It counts PRESENCE, which is the defect."

### F3 — HIGH — The DR §7 adversarial pass is missing on data-bearing PRs (#140, #143, #144, #146/#147, #154)
- DR-2026-08-19 §7 binds adversarial review to data and synthesis diffs, exhaustive on every `stated` determination.
- Method: I listed the subagent roles per session (`ls transcripts/harness_<id>/subagents`) and read each subagent's first prompt.
- **No antagonist or critic** ran in these sessions:
  - `2aa77402` (#140, batch 09) has 0 subagents.
  - `cb2e5827` (#143/#144, batches 10–12) has 0 subagents.
  - `0e701d1b` (#154, batch 18) ran only a db-census subagent.
  - `3ff1e851` (#146/#147, batch 15) ran only /code-review and /simplify quality agents. Those look at code, not claims.
- The pass works when it runs. In #153 it found the batch-17 retraction was itself unvalidated. In #155 (`ca1ae452`, 1 antagonist) it refuted two headline findings before merge.
- No gate checks for the pass. The blocking gate `audit_adversarial_use` checks a misuse-vector catalogue (`scripts/audit_adversarial_use.py:3-12`), not session review. The optional `adversarial_findings` table does not exist (`select name from sqlite_master where name like '%adversar%'` returns nothing).

### F4 — HIGH — GitHub-side review and merge gating are absent (all 42 PRs)
- **Reviews:** 0 GitHub reviews, 0 review threads, 0 review comments on every PR. Sources: `GET /pulls/{n}/reviews`, `/pulls/{n}/ccr/review_threads`, `/pulls/{n}/comments` → `gh/threads.json` is empty.
- **No "Claude Approvals" check** on any final head. Every check run's app slug is `github-actions` (`gh/prs.json`, field `checks[].app`).
- **No merge gating.** The `main` ruleset (id 19136391) has `enforcement: disabled` and only `deletion` and `non_fast_forward` rules (`GET /rulesets/19136391`).
- **8 PRs merged before CI finished on the final head:** #117, #130, #132, #138, #141, #146, #147, #155. The command filtered check-suite `max(completed_at) > merged_at` using `commits/{sha}/check-runs?filter=all`.
  - Seven of those heads were `session command log` commits (`git log -1 --format=%s <sha>`).
  - **#146's head 0b3b7f0 was substantive** (+422 lines: "admit BE ES HR IT INT; the enum can now gate the corpus"). It merged 44 s after the suite started and went green only afterwards.
- **2 PRs merged with a failing check:** #149 and #151 (`Classify change` = failure, 1–2 s runtime). The agent documented this as runner allocation in PR comments and left it red. #150 comment: "Standing down; no re-run".
- **Merge actors:** in-session agents merged at least #134, via `mcp__github__merge_pull_request` in `94859b50` after an owner "commit push merge" with CI green. Every PR shows `merged_by=jordanelias` because the token is shared, so the owner-vs-agent split for the other PRs is [UNVERIFIED].

### F5 — MEDIUM — R8 "log every query before screening" was met by pre-committed priors files, not by the log itself (#146, #152)
- **Batch 15** (`3ff1e851`):
  - PubMed, Consensus and Scholar searches ran 03:56:06–03:57:23 and were screened at 03:56:30.
  - They were logged as exec 60–63 at 04:03 (`select exec_id,created_at from search_executions where exec_id between 60 and 63`).
  - Mitigation: priors were committed first in dea4f1c at 03:55:58 (author = committer date), and the logged priors quote that file.
- **Batch 16:** priors were committed in 589577b at 19:50:11, the first search ran at 19:50:14, and the log was written at 19:54.
- On balance, the prior preceded the result but the verbatim log did not precede screening.
- **Batch 05** (#127): the 15 search INSERTs carry **no `prior_expectation` column** at all. Derived by parsing `data_20260902220357_*.sql`. The `log-search` refusal only landed on 2026-09-03 (`research_protocol_audit.py:128`). Those rows were deleted on 2026-09-13.
- **Batches 08–14 and 17–19 conform:** either log-search ran before any search call (`order.py` sequence), or priors were committed first (4f053bc, e4c1caf, c627055, 50c9b53, 3db5769, 6893397).
- The gate itself checks only that a prior exists (db.py:641), not when it was written.

### F6 — MEDIUM — The R1 "Co-1/T2/Co-2 FIRST" order was inverted in three batches, and across the programme
- Per-batch order, from `select target_evidence_type from search_executions where created_by_session=? order by exec_id`:
  - Batch 10 (#143): code, code, code, then co1.
  - Batch 18 (#154): grey ×6, clinical ×2, then co1 at position 9 of 10.
  - Batch 19 (#155): grey ×3, then co1 last.
- At programme level, the T4–T6 stratum was searched (batches 10–11, 2026-09-17) before the Co-2 pass (batches 13–14) and the T2 pass (batch 15, 2026-09-18).
- The DoD R1 check only asks whether any co1/co2 search exists (`research_batch_dod.py:292-317`), so it cannot see order.

### F7 — MEDIUM — Rule 6 transcript gaps
- **No transcript at all** for:
  - #116–#125: transcripts begin 2026-09-01.
  - #148 (`claude/claude-use-evaluation-b0cd3t`): no harness directory maps to that branch (tx_metrics branch list).
- **Batch 08 execution is unpreserved.** `harness_e124fa82/main.jsonl` ends at 04:12:46, but batch 08 was committed from 05:16 onwards (d5f6405 "research: batch 08…" at 05:16, 0ac6ef4 at 06:06). `grep -l research-batch-08-ramp-gradient` does not match `e124fa82`.
- **Subagent transcripts are complete** where sessions exist: subagent file counts equal the `subs=` counts in all 17 sessions.

### F8 — MEDIUM — Stop-hook churn: the protocol consumed the work
- In this window, **246 of 457** non-merge commits on main are `session command log` (`git log --since=2026-08-23 --until=2026-09-22 --no-merges --format=%s origin/main | grep -c 'session command log'`, against `| wc -l`).
- In PRs, git_metrics counts 291 log-only commits out of 448.
- **Session `292c6e38`:** 241 stop-hook messages, 184 log-pushes and 64 "Churn only / Green on" acknowledgements. **Session `e124fa82`:** 45 stop-hook messages, 45 log-pushes and 39 acknowledgements. Counted by `order`-style JSON parse; the script is inline in this audit's Bash history.
- Four PRs were opened only to carry transcripts after a merge: **#129, #135, #149 (25/25 commits log-only), #150.**
- The loop also made merges race the head (see F4).
- The fix (`scripts/fix_stop_hook_loop.sh`, 00edd89) landed on **2026-09-18**, after most of the window.

### F9 — MEDIUM — PR watching was done by polling on top of subscriptions
- Across 17 sessions (excluding this one): **683** `ReadNotifications` and **67** `send_later` calls, from a JSON parse of `tool_use` blocks.
- `292c6e38` alone made 244 `ReadNotifications` and 22 `send_later` calls while holding 3 `subscribe_pr_activity` subscriptions.
- Which PR-watching protocol text governs this is [UNVERIFIED]; CLAUDE.md does not define one. So this is an efficiency finding, not a rule breach.

### F10 — LOW/MEDIUM — Skills: required by protocol but not invoked
- **Skill tool calls: 10 in total across 17 sessions,** none of them before #148 merged on 2026-09-18. #148 records "47 skills the harness could not load", so before that date invocation was **impossible**, not skipped.
- After #148:
  - `orient` ×5, `session-open` ×1, `citation-miner` ×1 (batch 16/17).
  - `batch-done` ×0, but its content (DoD `--session`, then `--all`) was run by hand in every batch session.
  - `adversarial` ×0, though antagonist agents were launched directly in `616bcdf9`, `ca1ae452` and `e63bfb2e`, which is equivalent to its step 1.
  - `multilingual-research` ×0, although its trigger ("research") matches every batch. Its CHECK and LOG tables are empty: `select count(*) from search_languages` → 0 and `from search_coverage` → 0.
- The skill text is partly stale (GitHub checkpointing, 14-language counts). In practice, the SessionStart contract plus the DoD gate replaced it. That replacement is unrecorded [GAP: no ruling found retiring the skill's CHECK/LOG].

### F11 — LOW — Rule 1 commit format
- **7** commits on main lack the timestamp: 1 in #152 and 6 in #153, all "batch 17…". Command: `git log --since=2026-08-23 --until=2026-09-22 --no-merges --format=%s origin/main | grep -vE '\[[0-9]{4}-..-.. ..:..\]$' | grep -vE '^(source-verification|Merge )' | wc -l`.
- These landed because `check_commit_msg.py` is skipped on every PR (42/42 `skipped`) and on push checks only `fetch-depth: 2` (`ci.yml:253-266`).
- **39 of 446** stamped commits carry a stamp more than 5 minutes from their committer date. Example: dea4f1c is stamped 04:02 but was committed at 03:55. Some of these may be amends or merges [UNVERIFIED].

### F12 — LOW — Rule 0: breaches occurred and were self-caught
- `sessions/session_2026-08-27-nomenclature-reconciliation.md:64`: an owner 1:1 ruling was weighed against DR §7 (#121–#123 window).
- ab74930 ("rule 0 in the other direction"): agent design was recorded under an owner-ruling banner.
- CLAUDE.md §6 records the 2026-08-26 subject ruling as having been declared "open" until 2026-09-09.
- After the 09-09 CLAUDE.md rework, rulings were recorded on contact. Examples: #152 "Owner ruling recorded on contact"; batch 15 exec 64 "ADDED MID-BATCH ON AN OWNER DIRECTIVE"; the project-standards 2026-09-13 weighted-average ruling explicitly withdraws the session's own recommendation.

### F13 — LOW — Rule 7a: hand-typed counts after the rule landed (33c870e, 2026-09-16)
- `governance/stage-map.yaml:14` (238e8eb, 2026-09-17) states "depth 0 holds 26 tables", "17 of 89 objects" with no command beside them.
- #155's body self-corrected a typed "19/19".
- CLAUDE.md itself still states "~579KB" (§7) and "nine defects" (§2).
- The sample was `git log -p` over `CLAUDE.md governance/ references/ architecture/` since 2026-09-16T12:00, grepping `\b[2-9]\d*\s+(rows|checks|tables|sources…)`. It is not exhaustive.

### Items that conform (checked)
- **Rule 2:** every PR with a synthesis-path change carries at least 1 attestation (git_metrics: no row has synth=True with attest=0).
- **R10:** 0 URL-bearing sources have a NULL `verification_status` (`select count(*) from evidence_sources where url<>'' and verification_status is null` → 0). 26 are VERIFIED and 1 UNVERIFIED.
- **R13:** every T1–T3 source has a population-match row. The 4 without one are T5/T6 (REF-00988, 00990, 00991, 00992), which the gate exempts; the hook text says "every admission" [minor text/gate mismatch].
- **DoD before "done":** the last DoD run before merge was COMPLIANT for batches 05–19 (`dod.py`). Batch 04's only transcripted run was NON-COMPLIANT (3 rules, 2026-09-01T20:15) [GAP: batch 04 was executed pre-transcript].
- **CI:** mid-PR red on #145 (L04) was fixed before merge (e17f829).

---

## 2. Per-PR conformance (one line each)

Key:
- **CI** = final-head outcome. **Early** = merged before CI finished on the final head.
- **Rev** = GitHub reviews. They are 0 on every PR and omitted from the lines below.
- **Tx** = transcript preserved.
- **Branch** = number of PRs merged from that branch within the window.

| PR | Branch | Kind | CI | Tx | Deviations |
|---|---|---|---|---|---|
| #116 | pointer-discipline (2) | governance/schema | green | [GAP] | no Generated line in PR body |
| #117 | provenance-walk (1) | governance | green, **early** (log head) | [GAP] | — |
| #118 | smoke-test (3) | governance | green | [GAP] | — |
| #119 | pointer-discipline (2) | DB | green | [GAP] | — |
| #120 | smoke-test (3) | governance | green | [GAP] | — |
| #121 | smoke-test (3) | governance | green | [GAP] | rule-0 breach recorded 08-27 (self-caught) |
| #122 | fable-5 (2) | governance | green | [GAP] | — |
| #123 | fable-5 (2) | DB | green | [GAP] | rename not applied at merge per own comment |
| #124 | od-batch (1) | DB | green | [GAP] | — |
| #125 | od-b-links (1) | DB | green | [GAP] | — |
| #126 | circulation (3) | batch 04 + item-layer deletion | green | partial | batch-04 DoD NON-COMPLIANT at 09-01T20:15; data later cleared |
| #127 | circulation (3) | batch 05 | green | yes | 15 queries with no prior column (F5); rows deleted 09-13 |
| #128 | circulation (3) | governance/DB | green | yes | DB conflict from scheduled cron (rule 3 trap) |
| #129 | project-status (3) | log-only follow-up | green | yes | transcript-only PR |
| #130 | project-status (3) | governance | green, **early** | yes | — |
| #131 | project-status (3) | DB (213 commits) | green | yes | — |
| #132 | pr-131-verif (2) | code | green, **early** | yes | — |
| #133 | pr-131-verif (2) | code | green | yes | — |
| #134 | orientation (2) | batch 06 | green | yes | agent-merged on owner instruction, CI green |
| #135 | orientation (2) | log-only follow-up | green | yes | — |
| #136 | research-capability (1) | batch 07 + corpus clear | green | yes | **F1** search-log delete |
| #137 | research-safety (1) | batch 08 | green | **partial** | F1 id reuse; F2 (4 anchors); batch execution untranscripted (F7); REF-00987 has no search_admission |
| #138 | infra-state (2) | governance | green, **early** | yes | — |
| #139 | infra-state (2) | governance (rule 7a) | green | yes | — |
| #140 | pensive-bardeen (1) | batch 09 | green | yes | **no adversarial** (F3) |
| #141 | batch-10-prep (2) | prep | green, **early** | yes | — |
| #142 | batch-10-prep (2) | DB | green | yes | — |
| #143 | research-prep (2) | batch 10 | green | yes | no adversarial; R1 order code-before-co1 |
| #144 | research-prep (2) | batches 11–12 | green | yes | no adversarial |
| #145 | pr-144-review (1) | batches 13–14 | green (red mid-PR, fixed) | yes | code review only |
| #146 | batch-13 (4) | batch 15 | green, **early on substantive head** | yes | F5 log-after-screen; no adversarial |
| #147 | batch-13 (4) | GAP-010 | green, **early** | yes | — |
| #148 | claude-use-eval (1) | governance (skills loadable) | green | **no** | transcript missing |
| #149 | batch-13 (4) | log-only | **RED** (Classify) | yes | merged red |
| #150 | batch-13 (4) | log-only | green | yes | Classify red on earlier head, left |
| #151 | status-update (1) | log-only | **RED** (Classify) | yes | merged red |
| #152 | batch-protocol (2) | batch 16 | green | yes | 1 bad commit; F2 (2 anchors) |
| #153 | batch-protocol (2) | batch 17 | green | yes | 6 bad commits |
| #154 | batch-18 (1) | batch 18 | green | yes | **no adversarial**; R1 grey-first |
| #155 | next-batch (1) | batch 19 | green, **early** (log head) | yes | R1 co1-last; F2 (1 anchor) |
| #156 | data-table (2) | DB/render | green | yes | — |
| #157 | data-table (2) | schema | green | yes | — |

Branch stacking: 42 PRs came from 24 branches. `claude/batch-13-content-review-kpz7u8` alone produced 4 (#146, #147, #149, #150), and two of those carry only transcripts.

---

## 3. Merits of the gates the PRs ran against (CLAUDE.md §8 test)

This section is judged from the registry, git history, CI results and transcripts only; no gates were re-run. The registry holds 76 checks: `python3 -c "import yaml;print(len(yaml.safe_load(open('governance/check-registry.yaml'))['checks']))"`.

| Gate (level) | What wrong thing it keeps out of the book | Caught a real defect? | Weakness |
|---|---|---|---|
| **research_dod_session / research_dod** (blocking / advisory) | Non-compliant evidence entering the corpus | **Yes.** 7e9b9c8: batch 06 "DoD gate found five unmet rules" | Vacuous on four axes: R8 is blind to id reissue (F1); R2 counts presence, not direction (F2); R1 ignores order (F6); R8 checks prior presence, not timing (F5). Probes in `2aa77402` show it now fails on an empty session rather than passing green. |
| **author_fidelity** (advisory) | Fabricated or altered bibliographic fields (§5c, the worst failure class) | **Yes.** f6e9d4b: two batch-18 claims retracted (HathiTrust 403; Google Books 429 recorded as "0") | **Advisory**, although it guards the most book-relevant failure. Should be blocking. |
| **migration_reproducibility** (blocking) | A DB that a rebuild cannot reproduce | Partial | Counts only. 399ab2d shows a double-inserted batch would pass green. The deep variant is advisory. |
| **identifier_floor_audit** (blocking) | Reissued ids turning records into false pointers | **Yes.** 6cd99a1 | Scope is 2 keys; misses `exec_id` (F1). |
| **test_db_integrity** (blocking) | Integrity/content defects | Mixed | L04 fired by **calendar** rather than by defect (e17f829): green by coincidence for batches 11–12, red on a date change in #145. Red-by-construction class. |
| **attestation_presence / attestation_schema** (blocking) | Synthesis without a signed record | Now yes | Until 5cdbe6f (09-11) it examined only HEAD~1, i.e. was blocking and vacuous. It still does not read the free text. |
| **column_vocabulary_audit, derived_not_curated_audit** (blocking) | Vocabulary drift | Yes, for vocabularies | 65de740: battery was **green while `log-search` could not write a row**. No check exercises the writers. |
| **source_locators_integrity** (advisory) | Misattributed DOIs in the clue store (feeds R9 dedup) | **Yes.** It detected the offset-DOI corruption on 09-11 (5cdbe6f); batch 15 hit it live (REF-00037, `3ff1e851` 04:01) | Advisory, and no writer exists to repair it, so a known corruption has persisted for over 10 days [UNVERIFIED post-09-18 repair]. |
| **claude_md_spine** (blocking) | — (apparatus only) | No evidence | Fails the §8 test: guards CLAUDE.md prose, not the book. |
| **research_contract_sync** (blocking) | Hook/contract drift | 611a975 (fixes found by an antagonist, not by the gate) | Red by a hard-coded index if a SessionStart hook is inserted (CLAUDE.md §7 trap). |
| **Commit message format** (CI job) | — (apparatus only) | No | **Skipped on 42/42 PRs**; on push only checks depth 2. 7 bad commits reached main. Vacuous. |
| **Classify change** (CI job) | Routes batteries | — | Failed on runner allocation (#149, #151); a red that means nothing about the diff. |
| **render *_fresh** (2 blocking, 5 advisory) | Stale published dashboards | [UNVERIFIED] | Red by construction on every data change; the regenerate-derived bot commits to main (e.g. ec199ee, ed08027). |
| **Tests battery** (9 advisory) | Regression in audit scripts | 8055618/1e5645c referenced them | All advisory. `test_verification_pipeline` still asserts cleared-corpus floors (CLAUDE.md rule 7a). |
| **audit_adversarial_use** (blocking) | Misuse-vector review on release | No evidence in window | Unrelated to the session adversarial pass that DR §7 requires; there is nothing to examine pre-release. |

Net assessment:
- The gates that caught real defects are the DoD, author_fidelity, identifier_floor, source_locators and attestation gates. Two of those five are advisory.
- The blocking set also includes gates that are apparatus-only (claude_md_spine) or vacuous (commit-msg).
- No gate checks the four places where this audit found the protocol failing: search-log identity, forward mining, R1 order, and adversarial-pass presence.

---

## 4. Systemic causes (≤6)
1. **Gates check that a thing exists, not that it happened correctly.** R2 checks a mining row exists, not its direction. R8 checks a prior exists, not when it was written. R1 checks a co1 search exists, not the order. Attestation checks the file exists, not what it says. This is CLAUDE.md §5(a) recurring inside the DoD itself.
2. **Deletion by owner ruling was treated as a compensating migration without a full identity sweep.** Rule 4's "a key is a caller" was applied to two tables and not the log R8 protects.
3. **The adversarial pass is manual and unrecorded.** No table, no gate and no command invocation (`adversarial` ×0) exist for it, so it ran where the session happened to think of it. It was reliably absent in single-agent batch sessions.
4. **The stop hook's "clean tree" rule produced hundreds of log-only commits and pushes.** Those racing pushes decoupled merges from CI on the head, and no branch ruleset enforces checks.
5. **Skills were unloadable until 2026-09-18,** so the protocol lived in the SessionStart contract and CLAUDE.md. Skills such as multilingual-research, with its CHECK/LOG steps, were silently superseded rather than retired.
6. **GitHub carries no independent review.** Review happened in-session only (antagonists and code-review agents), leaving no thread, approval or check a later reader can audit.
