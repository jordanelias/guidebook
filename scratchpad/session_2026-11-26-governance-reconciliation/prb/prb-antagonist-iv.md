# PR B piece IV: antagonist review of the implementation (amend-search --set-deferred-reason)

Subject: the uncommitted diff `git diff -- scripts skills workplan` (5 files, +153/-17). HEAD moved from 807e7c8c to 0518b92a during this review. That commit touched only the ledger and the scratchpad (`git diff --stat 807e7c8c 0518b92a -- scripts skills workplan governance` is empty), so the red/green results hold. Canonical sha256 3d419efb…edb9 at the start and at the end. Every write went to copies under scratchpad/aiv/. One process error: a test-output file (green.txt) landed in the repo root because of a cwd slip. I moved it out at once, and `git status` shows only the five files under review plus logs.

## Table

| # | Attack | Result | Evidence |
|---|---|---|---|
| 1a | New tests RED on unmodified code | HELD | `git archive HEAD` plus the new test file only: `FAILED: 4`, rc=1. T081A-01/02 show "feature absent". T081A-03 fails on the real defect: `(None, 'absence_class after the call:', 'genuine_absence')`. T081A-04 fails with `rc 2 … unrecognized arguments: --set-deferred-reason`. |
| 1b | GREEN with the change, whole file | HELD | Working tree: `PASS: all 604 cases`, rc=0, SKIPPED-NO-FIXTURE 1 (T054-02, also skipped on HEAD). The ✓/✗ lines of the two runs differ only in T081A-01..04. |
| 2a | Blank, whitespace, tab/newline reason | HELD | Each gives rc=1 "a blank --set-deferred-reason states no cause … Nothing was written." The file is byte-identical. |
| 2b | results_found>0 (exec 1) | HELD | rc=1 "results_found=20, search_admissions none: this search ran …". Byte-identical. |
| 2c | Admission edge with results_found=0 (HAND), live or retired | HELD | rc=1 "search_admissions ['REF-00139'] …". Byte-identical. |
| 2d | results_admitted=2 and admitted_ref_ids set, no edge (HAND) | BROKEN (LOW) | rc=0 and `deferred_reason='HTTP 429'` written. See D5. |
| 2e | Already deferred (exec 9) | HELD | rc=1 "write-once". Byte-identical. |
| 2f | Classed row (26, classed by the sanctioned writer, then deferred) | HELD | rc=1 "absence_class is 'wrong_index' …". Byte-identical. |
| 2g | Both flags in one call | HELD | rc=1 "cannot assert both". Byte-identical. |
| 2h | Non-existent exec 999999 | HELD | rc=1 "no such search execution." |
| 2i | Converse refusal on deferred exec 9 | HELD | rc=1 "cannot assert both". Byte-identical. |
| 2j | deferred_reason='' (HAND) | BROKEN (LOW) | `--set-absence-class` gives rc=0 and the row becomes `('genuine_absence', '')`. `--set-deferred-reason` overwrites ''. See D6. |
| 2k | --clear-target with a refused deferral; a valid deferral with a refused --set-harm-finding; --dry-run | HELD | Every refused call is byte-identical, which proves the rollback after earlier UPDATEs. --dry-run is byte-identical. |
| 3a | Capture: emit_batch_sql | HELD | Four deferrals on a scratch copy give "0 insert(s), 4 update(s), 0 delete(s)", each `WHERE "exec_id" = 87/133/138/191`. |
| 3b | writable_tables | HELD | `'search_executions' in dbcore.writable_tables(c)` gives True. No derived list needs a change. |
| 3c | research-contract.yaml untouched; research_contract_sync | HELD | rc=0, "EXAMINED: 79 contract line(s)" on both HEAD and the working tree. |
| 3d | Other checks reading db.py and skills (run by hand) | HELD | derived_not_curated, schema_reference (2234→2246 refs, rc 0), skill_vocabulary (rc 1, identical), retired_vocabulary (rc 1, identical), pipeline_contract, claude_skills_loadable, context_map, research_dod_selftest, test_db_amend_writers (381/381), test_scan_contract (233/237, same 4 failures as HEAD) and build_graph --check all give identical summaries on HEAD and the working tree. |
| 4 | Callers (rule 4) | PARTIAL | See D3, D4 and D7b. citation-miner:120 concerns log-mining (`citation_mining.deferred_reason`), a different column, so leaving it is correct. |
| 5 | Quality and prose | PARTIAL | See D1, D2, D8 and D9. The code is minimal for what it does, with no dead code. |
| 6 | Solves the owner's problem | HELD (for the four) | cell_status(3) examined_empty goes from `[87,133,138,191]` to `[]`, deferred_searches `[87,133,138,191]`, owed.pairs_in_scope `[]` → `[]`. coverage: searches_outside_scope 68→67, searches_deferred_with_reason 0→4, pairs/jurisdictions/languages searched unchanged at 19/23/12. v_coverage_* row counts unchanged. After the change, zero-result rows still in examined_empty are `[29, 81, 82, 84, 85]` (81: see D12). |

## Defects, worst first

**D1 MEDIUM: the T-081 §2 precondition check states a wrong count.**
- Text: "`python3 scripts/db.py amend-search --help | grep -c set-deferred-reason` prints 1".
- Reproduction: `for c in 60 80 250; do COLUMNS=$c python3 scripts/db.py amend-search --help | grep -c set-deferred-reason; done` prints `2 2 2`. The usage line and the option line both match.
- Effect: §9 says "Stop … when a precondition is unmet", so a correct executor stops after the flag has merged.
- This is the only guard on the dependency. The plan generator (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` l.77-88) reads only `T-\d+` from that bullet, so REMEDIATION-PLAN.md shows T-081 with no dependency on the flag.
- It is also a typed result in place of the command (rule 7a), written into a file whose header says every number was read on 66a5ba8a.

**D2 MEDIUM: T-081 §9's stop condition can no longer fire for a deferral.**
- Text: "refuses for a reason other than a value, an already-classed row or (for a deferral) the states its refusal names".
- Every deferral refusal names a state, so this clause matches every possible deferral refusal.
- §3 fixes the four rows as zero-result, unclassed, undeferred and unadmitted. Any refusal on them therefore means the ground has moved, which is exactly what §9 exists to stop on.

**D3 MEDIUM: the new refusal cites R6 for words R6 does not contain, and the "deliberately" prose is left stale.**
- Refusal text: "deferred_reason means not run, never a findings channel (R6)". R6's hook reads "deferred_reason means DELIBERATELY NOT SEARCHED" (`governance/research-contract.yaml:155`). The quoted words are DR-2026-08-19's (l.1039).
- Left stale, now reachable by a second writer:
  - R6's hook, which is injected every session and held by the blocking sync;
  - the research_batch_dod.py:546 message;
  - db.py:3308 (`log-search --deferred-reason` help: "a search DELIBERATELY not run");
  - db.py:886;
  - the DDL comment "deliberate no-search".
- OD-45's plan changes ask T-081's PR for a sentence on "deliberate" (`DELEGATED-RESOLUTIONS-2.md:178`). The edited T-081 file does not carry that instruction.
- The implementer knew and deferred; no gate sees it.

**D4 LOW: a prose caller describing this diff is already incomplete.**
- `references/project-standards.md:9012` (committed in 0518b92a during this review) says T-081 "(sections 2, 4 and 8) edited".
- The diff edits sections 2, 4, 6, 8 and 9.

**D5 LOW: the admission refusal reads only search_admissions edges.**
- Reproduction (HAND): `UPDATE search_executions SET results_admitted=2, admitted_ref_ids='["REF-00001"]' WHERE exec_id=87`, then `amend-search --exec-id 87 --append-note x --set-deferred-reason "HTTP 429"`. Result: rc 0, written.
- The help says "refused when the search found or admitted anything".
- cell_status reads `results_admitted` for held and examined_empty.
- Live: 7 rows have results_admitted>0 and no edge. All have results_found>0, so the hole is unreachable today.

**D6 LOW: the implementation tests truthiness where readers test NULL.**
- amend_search treats `deferred_reason` by truthiness; every SQL reader uses `IS [NOT] NULL`.
- On a row with `''`, the converse refusal does not fire (the row ends up both classed and, to the views, deferred), and write-once is bypassed.
- The state is HAND-only: log_search folds '' to None.

**D7 MEDIUM (pre-existing in T-081, next to the edited §6): T-081's gates examine none of the rows it amends.**
- research_batch_dod scopes by `created_by_session` (l.318). The amended rows were created by earlier sessions.
- T-081's "Confirm the gates examined this batch" counts `updated_by_session`, which is a different subject from the gate's.

**D7b LOW: the R14 DoD message names only the absence-class route.**
- research_batch_dod.py:1227-1230 names only `--absence-class` and `amend-search --set-absence-class`.
- For a row whose request returned no list, the correct route is now `--set-deferred-reason`, and the message does not name it.

**D8 LOW: a clause in run-pipeline_SKILL.md now attaches to the wrong sentence.**
- In run-pipeline_SKILL.md:137-141, "; the batch gate reads the column" now hangs off the deferral sentence, so it is ambiguous which column is meant.

**D9 LOW: a wrong deferral has no path.**
- The flag is write-once with no clear. The converse message says "pass the one that is true" and gives no route when the stored deferral is the wrong one.
- T-081 §10 says "corrected forward through the same verbs", but no verb exists.

**D10 LOW: the flag can reach very few rows (§8).**
- After T-080, log-search cannot write an unclassed, undeferred zero row, and the flag refuses classed rows.
- After T-081 it can reach only rows that T-081 leaves unclassed.
- A retrieval failure found later on a classed row (the likely future case) has no CLI path.

**D11 LOW: the test re-derives the search-to-parameter mapping by hand.**
- `_ZERO81` computes `COALESCE(parameter_id, MIN extraction parameter for slug)` instead of reading cell_status, which is a second home for that mapping.
- If the two diverge, T081A-01 goes red for a fixture reason, not a defect.

**D12 (for the owner or coordinator, not a diff defect).**
- Exec 81's note records an HTTP 200 Cloudflare interstitial ("Just a moment..."). That is a "bot challenge", which OD-45's resolution names verbatim.
- The review's correction (`DELEGATED-RESOLUTIONS-2-REVIEW.md:166`) left 81 to T-081's own judgment.
- 81 stays in examined_empty for parameter 3.

## Omissions
- run_checks `--changed-from` classifies this diff as tooling only. derived_not_curated_audit, schema_reference_audit, skill_vocabulary_audit and claude_skills_loadable, which read db.py and skills/, are not selected; I ran them by hand. This selection gap predates the diff.
- skill_vocabulary_audit prints EXAMINED 568 both before and after, although two skills gained tokens. [UNVERIFIED] whether it read the new tokens.
- No mutation runs by the implementer. I did not run mutations either. By analysis each T081A-02 case's refusal is the only barrier to a write, except that "both" depends only on the absence-class block's check.

## Verdict
READY TO COMMIT AS IS: no.
- The code in scripts/db.py and the tests hold under every attack that a sanctioned writer can reach.
- The commit is not ready while T-081 carries D1 (a precondition that stops a correct executor) and D2 (a vacuous stop condition).
- D3's R6 misattribution and the stale "deliberate" prose must at least be stated in the PR body.

## Summary
The tests are honestly red-first: 4 fail on HEAD, and T081A-03 fails on the real defect (`genuine_absence` written on a deferred row). With the change, all 604 pass. Every reachable refusal leaves the database byte-identical, including refusals after an earlier setter's UPDATE in the same call. emit_batch_sql captures 4 UPDATEs. The research contract is untouched and its sync check passes. Every other check I ran gives the same result on HEAD and the working tree. The four rows leave examined_empty, and the coverage counters move only where they should. The prose is weaker:
- T-081's new precondition check prints 2, not 1.
- Its edited stop condition can no longer fire for a deferral.
- The new refusal attributes DR-2026-08-19's words to R6, while R6 and four other prose callers still say "deliberately".
- Two hand-built states slip past the refusals: `results_admitted` without an edge, and `''`.
