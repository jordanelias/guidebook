**VERDICT: about 4.24B tokens went into 17 harness sessions and 31 merged PRs. At least 32% of the orchestrator's tokens (1.12B of 3.51B) paid for turns that produced nothing: PR/CI wake-ups that only confirmed "still green" (637M) and stop-hook commit/push cycles for transcript-only changes (396M). Both are side effects of the harness and the PR workflow, not of the research. The largest structural multiplier is context: 51% of orchestrator tokens were spent in calls whose context was already above 500k.**

Scope and method. Read-only. All figures come from `transcripts/harness_*/{main.jsonl,subagents/*.jsonl}`, with API calls deduplicated by `message.id`. The current audit session `harness_37f845b8` is excluded. No check suite was run: every suite figure below comes from outputs the sessions themselves recorded.
Scripts are in this scratchpad. Run each one from `/home/user/guidebook` as `python3 <scratchpad>/<script>`. Outputs are saved next to them as `*.out`.

| Script | Computes |
|---|---|
| `audit_tokens.py` → `audit_tokens.out`, `audit_tokens.json`, `pr_info.json` | Per-session tokens, merged-PR mapping, episodes, waste classes (a) to (g), tools |
| `audit_rank.py` → `audit_rank.out` | Exclusive per-call waste attribution; stop-hook triggers before and after the fix |
| `audit_suites.py` → `audit_suites.out` | Suite runs by mode, their cost, reruns with no change in between, never-red and always-red checks |
| `audit_prtail.py` → `audit_prtail.out` | Tokens spent after each session's first `create_pull_request` |
| `audit_ctxcurve.py` → `audit_ctxcurve.out` | Context growth curve and compaction events |
| `audit_subagents.py` → `audit_subagents.out` | Subagent brief overlap and whether each subagent delivered its report |
| `audit_batches.py` → `audit_batches.out` | Research-batch sessions: tokens per search and per DB row |
| `audit_auditscripts.py` → `audit_auditscripts.out` | Which `scripts/audit/*.py` were run directly |
| `skill_staleness.py` | SKILL.md references to the deleted item layer |

Definitions:
- **"Tokens"** = input + cache_read + cache_write + output, per API call.
- **Cost of a tool use** = the tokens of the API call that issued it ÷ the number of tool uses in that call. Every extra tool round trip re-reads the whole context.
- **"Carry"** = the result's characters ÷ 4 × the number of later calls before the next compaction. This is what a result costs by being re-read at cache rate.
- **Merged-PR lines** come from `git diff --numstat M^1 M` on each merge commit. They exclude `transcripts/`, `scratchpad/` and generated `site/ parts/ audits/ tools/ *.html context-map`.

---

## 1. Token efficiency

### Totals

The following all come from `audit_tokens.py`, in the "PER-SESSION TABLE" TOTAL row and the lines that follow it:

- **4,240M tokens** in total: 3,509M in main transcripts and 732M in subagents.
- **6.57M output tokens.**
- Cache reads are **98.6%** of all tokens; output is 0.15%.
- Cache reads per output token: **636** overall, ranging from 266 (357827c3) to 1,568 (e124fa82).
- **51.3%** of orchestrator tokens were spent in calls with context above 500k.

The same script's "CONTEXT ECONOMICS" section gives:
- **Context floor.** The base context is 73–86k tokens per call (system prompt, tools, CLAUDE.md, SessionStart contract). Across 8,907 main calls that is 712M, about 20% of main tokens. CLAUDE.md alone is 34,607 bytes (`wc -c CLAUDE.md`, up from 26,747 on 2026-09-01), about 77M.
- **Context above 250k:** 1,475M, summed over calls as max(0, ctx − 250k).
- **Context above 500k:** 386M.

### Context growth

From `audit_ctxcurve.py`:
- Context grows by a median of 0.4–1.3k tokens per call.
- Every long session crosses 250k by about call 57–119, 500k by call 195–307, and 700k by call 316–495.
- There were **10 compactions**, all automatic, all at a preTokens value of 784–786k.
  - 292c6e38: 2
  - 556a3270: 2
  - 6a6f63cd: 2
  - 3ff1e851: 1
  - 616bcdf9: 1
  - 94859b50: 1
  - ca1ae452: 1
- **2,826 calls ran above 500k and 799 above 700k.** No session ever compacted or restarted by choice. 6a6f63cd spans 7.3 days and two research batches in one context.

### Per-session table

Source: `audit_tokens.py`, "PER-SESSION TABLE". The housekeeping share comes from `audit_rank.py`, "PER SESSION".

| session | hours | main/sub calls | tokens (main/sub) | output | ctxmax | >500k / >700k calls | compactions | merged PRs | substantive lines | tokens/PR | housekeeping-only share of main |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 292c6e38 | 29.6 | 1594/1189 | **946M** (753/193) | 787k | 784k | 805/323 | 2 | 129,130,131 | 6,963 | 315M | **511M (68%)** |
| 556a3270 | 7.6 | 1060/999 | **607M** (441/166) | 1017k | 784k | 374/110 | 2 | 136 | 7,788 | 607M | 35M (8%) |
| 6a6f63cd | 175.7 | 1215/702 | **605M** (503/102) | 938k | 779k | 456/111 | 2 | 126,127,128 | 17,322 | 202M | 137M (27%) |
| 94859b50 | 11.3 | 808/334 | **373M** (329/45) | 623k | 780k | 251/62 | 1 | 134,135 | 3,309 | 187M | 84M (26%) |
| 3ff1e851 | 19.2 | 695/163 | 281M | 421k | 781k | 222/68 | 1 | 146,147,149,150 | 1,638 | 70M | 72M (27%) |
| 616bcdf9 | 3.2 | 512/262 | 234M | 473k | 783k | 152/45 | 1 | 152,153 | 2,689 | 117M | 27M (13%) |
| ca1ae452 | 3.6 | 432/222 | 211M | 411k | 784k | 177/57 | 1 | 155 | 4,044 | 211M | 23M (13%) |
| cb2e5827 | 2.7 | 440/0 | 183M | 383k | 725k | 159/23 | 0 | 143,144 | 2,345 | 91M | 14M (8%) |
| c73c246b | 12.3 | 355/380 | 166M | 260k | 665k | 74/0 | 0 | 141,142 | 916 | 83M | 38M (31%) |
| e63bfb2e | 6.6 | 265/158 | 118M | 254k | 620k | 70/0 | 0 | 156,157 | 1,080 | 59M | 25M (25%) |
| e124fa82 | 1.3 | 240/465 | 116M | 73k | 248k | 0/0 | 0 | 137 | 1,564 | 116M | 40M (87%) |
| fbab52c8 | 3.7 | 294/146 | 114M | 283k | 601k | 51/0 | 0 | 145 | 756 | 114M | 13M (13%) |
| 1dc553b7 | 2.3 | 353/27 | 108M | 155k | 427k | 0/0 | 0 | 138,139 | 1,846 | 54M | 87M (82%) |
| 2aa77402 | 2.3 | 293/0 | 103M | 250k | 570k | 35/0 | 0 | 140 | 941 | 103M | 12M (12%) |
| **0e701d1b** | **0.6** | 166/12 | **42M** | 131k | 358k | 0/0 | 0 | 154 | 848 | **42M** | **0** |
| 357827c3 | 0.4 | 121/0 | 21M | 79k | 252k | 0/0 | 0 | 132,133 | 465 | 11M | 3M (14%) |
| d490f3ed | 0.2 | 64/6 | 11M | 34k | 231k | 0/0 | 0 | 151 | 0 | 11M | 2M (18%) |
| **TOTAL** | | 8907/5065 | **4,240M** | 6.57M | | 2826/799 | 10 | 31 | **54,514** | **137M** | **1,123M (32%)** |

**Tokens per merged PR:** 137M on average (4,240M ÷ 31). That is **78M per 1,000 substantive lines**. Five of the 31 PRs (#129, #135, #149, #150, #151) carry 0–12 substantive lines each: they are transcript or log-only. Source: `pr_info.json`, `sub` field.

### The four largest sessions compared with what they delivered

Source: the "PRs per session" section of `audit_tokens.py`, which reports the diff split and the net DB rows from each merge's before/after row counts.

The four sessions together account for 2,531M tokens (60% of the total) and 35,382 substantive lines (65% of the total).

- **292c6e38 (946M).** Merged #129 (12 substantive lines), #130 (1,004) and #131 (5,947). Net DB rows: 2, both `data_migrations`. Of 20,946 diff lines in #131, 14,708 are transcripts. **68% of its main tokens were housekeeping-only turns**: 234 of 244 notification wakes and 91 of 236 stop-hook cycles did nothing else. This is the worst-value session by a wide margin: 136M per 1,000 substantive lines, and no research content.
- **556a3270 (607M).** #136: 7,788 substantive lines, including batches 06–07 and the re-key (base_icf +72, population_icf_links +61, and negative deltas elsewhere). It also had the largest subagent spend: 166M across 15 background general-purpose agents.
- **6a6f63cd (605M).** #126–128: 17,322 substantive lines, including the item-layer deletion (items −93, item_taxonomy_links −540) and batches 04–05. This is the best tokens-per-line of the four (35M per 1,000 lines), although 137M of it was housekeeping.
- **94859b50 (373M).** #134–135: 3,309 lines and 51 net rows. 113M per 1,000 lines. 26% housekeeping.

### PRs are opened early, so almost all work happens under a live PR subscription

From `audit_prtail.py`:
- In 15 of 17 sessions, the first `create_pull_request` comes within the first 19–73 calls. After that point, 66–99% of the session's tokens are spent with the PR subscribed. Across all sessions that is 3,303M of 3,509M.
- **0e701d1b is the exception.** It opened its PR at call 163 of 166.

---

## 2. Waste classes, ranked by tokens

Classes 1–2 and 5–6 are exclusive per-call attributions from `audit_rank.py`. An episode counts as housekeeping-only when every tool call in it is one of: git status/add/commit (log messages)/push/fetch/log/diff, `preserve_transcripts.py`, `ReadNotifications`, `pull_request_read`, `actions_*`, `send_later`, `ToolSearch`, or text only. Classes 3, 4 and 7 are measured differently, as the table notes, and can overlap.

| # | Class | Tokens | Share | Method and source |
|---|---|---|---|---|
| 1 | **Notification wakes that only polled** | **637M** | 15.0% of all, 18.2% of main | 616 of 685 wake episodes, 1,493 calls. `audit_rank.py` class 1 |
| 2 | **Stop-hook commit/push cycles, housekeeping only** | **396M** | 9.3% of all | 451 of 616 stop-hook episodes, 904 calls. `audit_rank.py` class 2 |
| 3 | Long-context premium (structural; overlaps every other class) | 1,475M above 250k, 386M above 500k | 35% of all | Σ max(0, ctx − threshold). `audit_tokens.py`, "CONTEXT ECONOMICS" |
| 4 | Suite reruns with no mutating call since the last identical invocation | 95M | 2.2% | 546 of 3,107 suite runs. Issuing share + output carry, main and subagents. `audit_suites.py` |
| 5 | PR/CI polling inside episodes that also did real work | 69M | 1.6% | 211 tool uses. `audit_rank.py` class 5 |
| 6 | Identical non-suite Bash reruns with no change in between | 20M | 0.5% | 64 reruns. `audit_rank.py` class 4. The looser exact-string count, without the no-change condition, is 454 reruns / 193M |
| 7 | Tool results larger than 20KB (carry) | 60M | 1.4% | 41 results. Carry of all results is 692M. `audit_tokens.py`, "(d)" |
| 8 | Orient/preamble before the first write | 62M, not waste | 1.5% | `audit_tokens.py`, "(g)" |
| 9 | Duplicated or discarded subagents | 14M | 0.3% | `audit_subagents.py` |
| 10 | Re-reading the same file range | ~0.1M | ~0 | 1 exact repeat. `audit_tokens.py`, "(e)" |

Detail for each class:

**(1) ReadNotifications.** Source: `audit_tokens.py`, section "(a)".
- 683 calls, of which only 2 returned no notification.
- Of 730 relayed events:
  - 638 `check_suite.completed`
  - 54 `subscription.created`
  - 26 `check_run.completed`
  - 12 `pull_request.closed`
- 52 wakes were self-scheduled check-ins, out of 67 `send_later` calls.
- In the looping sessions the median gap between reads was **1.0–1.7 minutes** (1dc553b7, 292c6e38, 6a6f63cd, e124fa82, c73c246b, 3ff1e851).
- **90% of wakes (616/685) led to no action.**
- The `subscription.created` payload is about 19KB of instructions. Notification bodies carry 104M in total (`carry by producer`).

**(2) Stop-hook loop.** Sources: `audit_tokens.py` "(b)"; `audit_rank.py` last line; `git_metrics.txt`.
- **617 "Stop hook feedback" prompts: 592 before `scripts/fix_stop_hook_loop.sh` landed (2026-09-18 16:37Z) and 24 after.**
- 423 `preserve_transcripts.py` calls, costing 167M as issuing share (overlaps class 2).
- 755 `git commit` commands; 291 of the 448 commits on merged branches touch only transcripts or scratchpad (`git_metrics.txt`).
- The loop in 292c6e38 committed about every 80 seconds, with messages like "provenance: transcript refresh".
- The owner's complaint "God damn it you did the stupid fucking loop" (c73c246b, 2026-09-17T02:42Z) came before the fix.
- **The fix script's own header estimates about 150–200k tokens for one session's loop. The measured cost across sessions is 396M in housekeeping-only turns alone, or 802M including all stop-hook-triggered episodes.** The script under-states the cost because each cycle re-reads a context of about 400k, not just the output tokens.
- Classes 1 and 2 feed each other: a stop-hook commit is pushed, the push triggers CI, CI sends `check_suite.completed`, the wake appends to the transcript, and the stop hook fires again.

**(3) and (4) Suites.** The owner's additional request is answered in §2a below.

**(5) Large results.** Source: `audit_tokens.py` "(d)", `carry by producer`.
- The largest carries come from inline `python3 -` scripts (115M), shell reads (133M), `ReadNotifications` (104M), `db.py` (60M) and `pull_request_read` (55M).
- Among results larger than 20KB, the top producers are `ReadNotifications` (18 results, 21.9M), `sed` of large files (9 results, 13M) and PubMed/Consensus payloads (7.8M).

**(6) Re-reads.**
- Exact same-range re-reads are negligible (1 case).
- Instead, `scripts/db.py` is sliced piecemeal 4–21 times per session: 21 times in 556a3270 and 11 each in 616bcdf9 and 6a6f63cd.
- `assess_cell.py` was read 18 times in 556a3270.
- Source: `audit_tokens.py` "(e)", "top files read ≥4x".

**(7) Subagents.** Sources: `audit_subagents.py`, `audit_tokens.py` "(f)".
- 116 subagents, 732M tokens.
- 115 delivered a report. The one that did not was a 6a6f63cd antagonist (7.4M).
- 1 exact re-launch: 616bcdf9, brief overlap (Jaccard) 1.0, 6.9M.
- No other brief pairs overlap above 0.25.
- **Duplicated work was not the issue. Volume was.**
  - Adversarial-loop roles (antagonist 166M, agonist 76M, adversarial 28M, tracer 23M, steelman 11M) total **about 300M**.
  - 292c6e38 ran 8 antagonist/adversarial rounds in sequence (193M in subagents).
  - 556a3270 ran 15 background agents (166M).

**(8) Preamble.** Source: `audit_tokens.py` "(g)".
- The first productive write came at call 9–45: 0.8–6.5M tokens and 2–15 minutes, about 1–6% of each session.
- In batch sessions, the first research retrieval came at call 23–26, 5–9 minutes in.
- 3ff1e851 was the exception: first retrieval at call 120 (23M tokens, 33 minutes), because it did a content review first.
- **Preamble is not a material waste class.**

## 2a. Check suites (owner request)

Source: `audit_suites.py`. Tokens are the issuing share plus output carry. "No change" means that between two identical suite invocations there was no Edit/Write, no `sed -i`/redirect/mv/cp/rm, no git merge/pull/fetch, no migrate/emit/regenerate/context_map, no `db.py` write, and no inline Python containing write keywords.

| Suite / mode | Runs | Issuing tokens | Output carry | Reruns with no change | Tokens of those reruns |
|---|---|---|---|---|---|
| direct `scripts/audit/*.py` (not DoD) | 1,173 | 189M | 26M | 281 | 46M |
| `test_db_integrity.py` | 498 | 100M | 10M | 104 | 20M |
| `research_batch_dod --session` | 343 | 64M | 14M | 64 | 12M |
| other `scripts/tests/test_*.py`, pytest | 302 | 57M | 10M | 42 | 9M |
| `run_checks --changed-from` | 248 | 75M | 12M | 7 | 1.5M |
| `run_checks --selftest` | 155 | 34M | 4M | 0 | 0 |
| `run_checks` (bare, `--explain`, etc.) | 139 | 16M | 4M | 35 | 5M |
| `run_checks --all` | 76 | 23M | 3M | 2 | 0.4M |
| `preflight.sh` | 63 | 12M | 2M | 2 | 0.2M |
| `run_checks --list` | 45 | 5M | 4M | 7 | 0.8M |
| `run_checks --battery` | 22 | 6M | 0.4M | 0 | 0 |
| `research_batch_dod --selftest` / `--all` | 32 / 8 | 4M / 1M | ~1M | 2 | 0.2M |
| `run_checks --kinds` | 3 | 0.5M | 0 | 0 | 0 |
| **Total** | **3,107** | **584M (13.8%)** | **90M** | **546** | **95M** |

Notes on usage:
- The stop hook also ran `research_batch_dod.py --all` automatically **1,407 times**, injecting 2.64M characters of hook output. This is not counted above.
- `--all` was used 76 times, against 248 runs of the scoped gate. The heaviest `--all` users were 94859b50 (27), 292c6e38 (21) and 2aa77402 (9).
- The most-run direct audit scripts (`audit_auditscripts.py`):
  - `research_batch_dod`: 383
  - `extraction_relations_integrity`: 103
  - `research_protocol_audit`: 97
  - `retired_vocabulary_audit`: 95
  - `validate_pydantic_schemas`: 84
  - `adherence_log_audit`: 78

**Never red.** These are candidates for having no merit: 29 of the 76 registered checks, observed across every recorded `[PASS|FAIL|NONE]` line and summary line. Caveat: CI job logs are almost absent from the transcripts (0 `::error::` lines captured), and many local outputs were cut with `| tail`. "Never red here" therefore means never red locally.
- **Blocking checks that never went red:**
  - `judgment_handoff_shape` (89 observations, all PASS)
  - `research_contract_baseline_ratchet` (26)
  - `research_contract_sync` (17)
  - `check_yaml`, `check_utf8_md`, `claude_md_spine`, `validate_bpc` (11–13 each)
  - `schema_reference_audit`, `decision_capture`, `doctrine_recheck`, `validate_cross_refs`, `alias_provenance_audit`, `audit_adversarial_use`, `validate_axes`, `validate_jurisdiction`, `jurisdiction_db_vocabulary` (1–10 each)
- **Blocking checks that were almost always vacuous:**
  - `attestation_presence` (4 PASS / 94 NONE)
  - `attestation_schema` (4 / 95)
  - `source_slug_links_duplicates` (8 / 22)
- **Advisory checks that never went red:** `render_audit_browser` (78), `test_record_command_session` (27), `graph_audit` (22), `gap_mining_audit` (18), `claims_docket`, `matrix_consistency`, `readonly_db_open_audit`, `validate_population`, `audit_evidence_metadata`.
- **Advisory checks that were only ever NOTHING-IN-SCOPE:** `medical_lens_integrity` (126), `pmp_audit` (161), `population_integrity_audit` (160), `reasoning_doc_citations_audit` (161).
- **Never observed at all:** `claude_skills_loadable`.

**The opposite failure: always red.** These checks cannot discriminate either, and rule 6 says they teach the reader to ignore them. Eleven advisory checks were red in 100–328 observations with 0–12 passes:

| Check | Pass | Fail |
|---|---|---|
| `site_pages_fresh` | 0 | 328 |
| `retired_vocabulary` | 0 | 314 |
| `test_verification_pipeline` | 0 | 302 |
| `validate_pydantic_schemas` | 0 | 288 |
| `metadata_integrity_audit` | 0 | 206 |
| `validate_reasoning` | 0 | 191 |
| `source_locators_integrity` | 0 | 169 |
| `research_protocol_audit` | 12 | 135 |
| `author_fidelity` | 7 | 115 |
| `validate_schema_cross_check` | 5 | 101 |
| `context_map_fresh` | 45 | 120 |

**`test_db_integrity`:** 79 test ids observed, **52 never failed**. The 27 that failed at least once include K02 (×12), C04 (×8) and K01 (×7). Of the 62 ids declared literally in the current source, 38 were never observed failing.

**`research_batch_dod`:** every rule R1–R15 failed at least once. The most frequent were R9a (30 fails / 40 passes), R9b (24/43) and R1 (21/31).

---

## 3. Tool, skill and agent choice

Source: `audit_tokens.py` "TOOLS" and "(f)"; `skill_staleness.py`.

**Skills.**
- 10 `Skill` calls in 17 sessions:
  - `orient`: 5
  - `artifact-design`: 2
  - `artifact-diagramming`: 1
  - `citation-miner`: 1
  - `session-open`: 1
- 41 project skills are linked in `.claude/skills/`, plus 4 commands.
- **Before 2026-09-18 05:59 (commit ce39a07), no project skill could be loaded by the harness.** Sessions read `skills/*_SKILL.md` through `sed` instead; for example, 556a3270 read `skills/functional-deficit-auditor_SKILL.md` 5 times.
- The research batches never invoked `multilingual-research`, `gap-driven-mining` or `citation-verifier`. `citation-miner` was invoked once (616bcdf9).

**Stale skills** (`skill_staleness.py`: `item_code` references and item-layer `db.py` subcommands, against `items` = 0 rows and `item_audit_runs` = 0 rows):

| Skill | `item_code` refs | Item-layer subcommands |
|---|---|---|
| `item-audit-pipeline` | 30 | `add-audit-run`, `audit-runs`, `items`, `update-audit-run` |
| `audit-consolidator` | 14 | `update-audit-run` |
| `functional-deficit-auditor` | 9 | `items` |
| `economics-auditor` | 6 | — |
| `connection-discovery` | 3 | — (also 13 `[A-Z]-NN` item codes) |
| `cross-population-conflict-mapper` | 3 | — |
| `evidence-auditor` | 3 | — |
| `question-author` | 3 | — |
| `content-gap-analyzer` | 1 | — |

`item-consolidation-analyzer` is item-layer by definition. The harness's skill list still advertises all of these.

**Agent `subagent_type`.**
- 102 `Agent` calls:
  - general-purpose: 69
  - Explore: 14
  - antagonist (project agent): 7
  - Plan: 6
  - db-census (project agent): 5
  - claude-code-guide: 1
- **The `repo-sweep` project agent was never used.**
- 23 subagents carried an antagonist role, but only 7 used the `antagonist` agent. 292c6e38 ran its antagonists as `Explore` agents, and 556a3270 and 6a6f63cd ran theirs as general-purpose.
- `db-census` (Haiku) cost 0.1–0.3M per use and was the cheapest subagent in the corpus.

**Bash for reads.**
- Main transcripts: 12,422 Bash calls, of which about 1,215 are leading `cat/head/sed -n/grep/ls/find`.
- Read, Grep and Glob were used 10 times in the main transcripts and about 400 times in subagents.
- Every session sliced files with `sed -n`. Shell-read results carry 133M.

**Research tools.**
- MCP: PubMed about 50 calls (search 29, metadata 18, full text 2, related 1), Consensus 17, Scholar Gateway 5.
- Web: WebSearch 53, WebFetch 74.
- `retrieval_log.py` through Bash: 288 calls. Direct scholarly `curl`: 26.
- Research retrieval goes mainly through `retrieval_log.py`, which CLAUDE.md §5(c) requires because it persists payloads. MCP use is sparse and concentrated in 6a6f63cd (PubMed 37, Consensus 12) and 3ff1e851.
- Sessions 2aa77402, cb2e5827 and fbab52c8 used WebSearch or WebFetch only.
- Large Consensus and PubMed payloads carry 5.8M and 4.6M respectively.

---

## 4. The most and least efficient research batches

Source: `audit_batches.py`; the rows are net DB deltas of each session's merged PRs.

| Session | Batch | Tokens | Calls | Searches logged | Net rows | Tokens per search | Tokens per row |
|---|---|---|---|---|---|---|---|
| **0e701d1b** | 18 | **42M** | 166 | 10 | 35 | **4.2M** | 1.20M |
| fbab52c8 | 13–14 | 114M | 294 | 6 | 105 | 19.1M | 1.09M |
| cb2e5827 | ~10–12 | 183M | 440 | 11 | 145 | 16.6M | 1.26M |
| e124fa82 | 08 | 116M | 240 | 4 | 93 | 29.1M | 1.25M |
| 616bcdf9 | 16–17 | 234M | 512 | 12 | 124 | 19.5M | 1.89M |
| 3ff1e851 | 15 + review | 281M | 695 | 6 | 138 | 46.8M | 2.04M |
| 2aa77402 | 09 | 103M | 293 | 10 | 48 | 10.3M | 2.15M |
| **ca1ae452** | 19 | **211M** | 432 | 4 | 35 | **52.7M** | **6.03M** |

Per row written, 0e701d1b is about average. **Its advantage is entirely in the waste it avoided.** Compared with the least efficient batch, ca1ae452 (batch 19):

1. **When the PR was opened.** 0e701d1b opened its PR at call 163 of 166. It received 0 notifications and spent 0 tokens on housekeeping. ca1ae452 opened its PR at call 171 of 432. It then spent 97 calls (62M) on notification-woken turns and 53 calls (31M) on stop-hook turns, and 133M of its 183M main tokens came after the PR was opened. (`audit_prtail.py`; `audit_tokens.py` episodes)
2. **Context size.** 0e701d1b peaked at 358k with a mean of 249k and never compacted. ca1ae452 reached 784k, compacted once at call 373, had a mean context of 422k, and made 177 calls above 500k. (`audit_ctxcurve.py`, `audit_tokens.py`)
3. **Subagents.** 0e701d1b used one Haiku `db-census` agent (0.3M). ca1ae452 used 7 subagents (28M). 616bcdf9 used 12 (31M), including 5 antagonists, plus 148 calls (46M) spent handling their messages.
4. **Verification churn.** 0e701d1b ran 3 `test_db_integrity` and 4 `--changed-from` runs. ca1ae452 ran 33 and 23. 616bcdf9 ran `test_db_integrity` 104 times. (`audit_suites.py`, per session)
5. **Scope.** 0e701d1b ran 10 searches in 37 minutes from one instruction ("Orient then perform batch 18") and the `/orient` command. Batch 19 worked on pre-1990 scanned sources (`page_image.py` ×15; inline Python carry 13M) and logged only 4 searches.
6. **Timing.** 0e701d1b ran after the stop-hook fix landed and triggered it 0 times. ca1ae452 still triggered it 7 times; the fix lives in `~/.claude` and has to be re-applied in each container.

---

## 5. Systemic causes (six)

1. **PR-first workflow plus a CI wake on every push.** Every session opens a PR early, typically by call 19–73, and subscribes to it. Every push then produces a `check_suite.completed` wake that re-reads 300–780k of context to learn that CI is green, and `send_later` adds self check-ins on top. This produced 616 no-op wakes costing 637M. **Fix:** open the PR once, at the end (as 0e701d1b did), or do not subscribe until the work is done.
2. **Tracked files that grow every turn, plus a git-clean stop hook, make an unsatisfiable loop.** `transcripts/*.jsonl` and `scratchpad/*/commands.jsonl` grow on every turn, so the tree is never clean. Result: 617 stop-hook prompts, 396M in housekeeping turns, and 291 log-only commits on merged branches. Each of those commits re-arms cause 1. The fix is per-container, lives in `~/.claude`, and still let 24 prompts through after it landed. Its own cost estimate is too low by about three orders of magnitude.
3. **No context hygiene.** Sessions run until automatic compaction at about 784k, and one harness session spans days and several project sessions. 51% of orchestrator tokens were spent above 500k context, and 35% of all tokens are context beyond 250k. A base of about 80k per call (CLAUDE.md alone is 34.6KB) adds 712M as a floor. **Fix:** end or hand off a session per batch or PR.
4. **Verifying by re-running gates that cannot tell good from bad.** There were 3,107 suite runs (584M issuing, 90M carry), including 546 reruns with no change in between (95M), plus 1,407 automatic DoD runs from the stop hook. 29 registered checks never went red locally, 4 were only ever vacuous, and 11 advisory checks were red nearly every time. None of those 44 checks changes a decision.
5. **Open-ended status and "are we ready" prompts that turned into multi-day infrastructure rework.** "present current state…", "Can we perform research finally?" and "orient… prepare to conduct research" led to 292c6e38, 556a3270 and 94859b50: 1.93B tokens and 215 net DB rows, most of them 556a3270's re-key rows. 292c6e38 alone spent 946M for 2 migration-ledger rows and was 68% housekeeping.
6. **Project scaffolding bypassed or stale.**
   - Skills could not be loaded until 2026-09-18 and were invoked 10 times after that.
   - 9 skills still target the deleted item layer.
   - Project subagents were underused: `repo-sweep` 0 times, `antagonist` 7 of 23 antagonist runs. Adversarial work was instead done by general-purpose Opus/Fable agents, about 300M in adversarial-loop roles.
   - Every read went through Bash `sed` slices of large files (`db.py` sliced up to 21 times in one session).
