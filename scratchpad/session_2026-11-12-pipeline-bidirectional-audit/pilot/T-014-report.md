# T-014 pilot report (dry pilot, Sonnet-class executor)

Task: T-014 Keep the stress scripts as a characterisation harness and their probes as tests. Stage P0, stacked on nothing. Mode: **pilot** (scratch clone, no push, no PR, no /session-open, no /adversarial, no /batch-done).

Base commit: `origin/claude/peaceful-noether-kvf3sf` = d0952279b (clone HEAD at start d095227). I **overrode the task file's BASE line** as the brief says: in the clone `origin/ccr-408aaa9b-z3e4s0` does not exist (`git rev-parse -q --verify` prints nothing), and `git diff --quiet origin/main origin/claude/peaceful-noether-kvf3sf -- workplan/...` exits 1, so the file's own line would have picked the stale `origin/main`.
Canonical database sha256 before and after (both `/home/user/guidebook/data/guidebook.db` and the clone's): `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`, equal.
Result: **PILOTED, with two points where a real executor would have to stop under section 9** (defects 1 and 2 below). I went on to a green gate and a commit, and say so.

## Did the five things hold

1. Followed only CLAUDE.md and the task file (plus the files the task file names: `stress/*.py`, `audit/hs-stress-audit.md` section 4/7.4 to learn which probes it means, `stress/RETAINED.md`, and the brief). Yes. I did read `audit/hs-stress-audit.md` beyond the evidence command's `sed` range (B-75, B-79, 7.4) because section 4 item 1 names the faults only by short phrase; that was needed.
2. Evidence command printed what the file says: **mostly**. `ls` printed five scripts (lang_probe, run_logged, stress_run, stress_run2, stress_run3). The `sed` printed section 4 of the audit with W-1 to W-11; it does **not** print "section 7.4" (that is a different part of the audit file), although the file says the output lists "W-1 to W-11 and section 7.4".
3. Red before, green after: **partly**. The two unchanged runs are not equal (red), but not for the reason the file anticipates, and after the repairs the two runs are *still* not equal (one field), so "prints no differing step" never became true. Details in defects 1 and 2. Per-fault red/green is real and shown (table below).
4. Gate ran once; each named check's `EXAMINED:` read. Yes (table). Gate result PASS, but vacuous for this change (defect 9).
5. Patch and report saved. Yes.

## Evidence of red and green

Unchanged tree, `stress_run3.py --parts probes,real,guards,batches,lifecycle,reentry` (not `batteries`, defect 8), `--out` a scratch folder (defect 7), run twice (run1, run2), compared with the new `stress_diff.py`:

- run1 vs run2 (unchanged): 6 differing fields, all in `real`: `real.clone` is skipped in run 2 because the clone from run 1 exists (`if not clone.exists()`), `emit-data-migration` then writes a second migration into the reused clone and `migrate-rebuild` fails: rc 0 -> rc 1, "Applying 69 schema migration(s) and 158 data migration(s)" -> "... 159 ..." with no "Rebuilt successfully", and `migration-reproducibility-deep` rc 0 -> rc 1. This is the audit's B-69 reproduced.
- Repairs applied (below), then run4 vs run5 (repaired, both fresh): **1 differing field**: `real.migrate-rebuild [stderr]`. The advisory line "158 FK violations after 081_icf_registry.sql" is followed by five example tuples that differ between runs (`('item_taxonomy_links', 419, ...)` vs `('item_taxonomy_links', 436, ...)`). Cause read in `scripts/migrate_db.py` line 192 region: the examples are `list(new)[:5]` of a `set` of tuples, so which five are printed depends on hash order. I did not normalise it (section 9: "do not hide it by normalising more").
- Seeded-difference test (`stress_diff.py` on a copy of run4): changing an `expect` string prints **nothing** (exit 0, correct: `expect` is not a compared field); changing one `stdout` prints `DIFF guards guards.guards.control-exact [stdout]` and exits 1; a folder against itself exits 0. So the section 6 instruction "change one expectation string ... and diff again" cannot show a difference (defect 3).
- Original (run1) vs repaired (run4): the `rc` field differs in exactly the five steps repaired in the scripts: `guards.control-exact`, `guards.quote-extra-space`, `guards.quote-truncated`, `lifecycle.merge-parameter`, `reentry.raise-determination-gate`. (43 differing fields in all; the rest are the new outputs those steps now produce and the retire probe's new target.)

## Script repairs made (patch: `T-014.patch`, one commit, four files, all under `scratchpad/.../stress/`)

| Section 4.1 item | Done | Observed after |
|---|---|---|
| delete the reused clone before each write-path replay | `shutil.rmtree(clone)` before the clone in `stress_run3.py` (real) and twice in `stress_run.py` (writepath_replay, crosstopic) | run4 and run5 both reach `migrate-rebuild` rc 0 and `reproducibility-deep` rc 0 |
| locator on the two guard probes | `*loc_args(R.db)` added to the quote-variant calls (all three, not two) | extra-space and truncated now reach the guard: rc 0 (accepted) where before rc 1 "needs a locator" |
| `--trigger-evidence-type` on raise-determination-gate | added, **and `--trigger-tier`** (defect 5a); both read from a held source row, not typed | gate 2 raised, rc 0 |
| merge probe at a parameter with no open gate | explicit args; target chosen by query (active, no open gate) | merge rc 0 (parameter 13 into 4) |
| drop `dbcore.normalise_quote_text` from `lang_probe.py` | removed from loader, docstring, loop and collision keys | probes part rc 0, output keys `collisions_rl.normalise_quote`, no loader errors |
| two failing SQL probes | `stress_run.py`: `sc.locator=l.locator` -> `sc.resolved_ref_id=s.ref_id`; `retired_at` -> `status` in the post-retire query | `stress_run.py --topics cost` (killed by my 100 s timeout after the write-path steps): funnel returns 11 rows, post-retire returns `[122, "active"]`, 0 `OperationalError` in its log |

Not in section 4.1, needed, done: `GUARD_LENS = "SCI"` for every guard case (defect 5b); retire probe retargeted (defect 5c).
Added: `stress_diff.py` (66 lines): reads `<part>/log.jsonl` in two folders, matches steps on (part, tag without its running counter, repeat number), compares argv/rc/stdout/stderr/changed, removes absolute `/tmp` paths, date-times, 14-digit migration stamps (and never compares `at`, `seconds`, `canonical_sha256`), prints `EXAMINED: <steps> ...`, exit 1 on any difference.

## Check-by-check, before and after (registry `cmd`, run as the registry runs it)

| Check | rc before / after | EXAMINED line (before = after) | failing cases before = after |
|---|---|---|---|
| test_run_pipeline_refusals | 0 / 0 | `EXAMINED: 175 cases` | none |
| test_db_amend_writers | 0 / 0 | `EXAMINED: 161 assertion(s)` | none |
| test_scan_contract | 1 / 1 | `EXAMINED: 119 assertion(s)`, 117/119 | G01, G02 (the R2 baseline, not this change's) |
| test_author_presence | 0 / 0 | `EXAMINED: 13 assertion(s)` | none |
| test_search_log_completeness | 0 / 0 | `EXAMINED: 23 assertion(s)` | none |
| test_assess_cell_pilot | 0 / 0 | **no `EXAMINED:` line**; only `PASS: all pilot-engine branch tests` (counts nothing) | none |
| observation_verbatim_audit | 0 / 0 | `EXAMINED: 96` | none |

The failing-case diff (`diff <(grep ...before) <(grep ...after)`) is empty for all seven. None of the seven reads anything this task touches (defect 9), so equality here is expected and proves nothing about the change.

Gate (`scripts/preflight.sh --base "$BASE" --explain`, run once, before the commit): selftest PASS; `RESULT: PASS - 6 check(s) green, 1 advisory failure(s)`; the one failure is `retired_vocabulary` (advisory, in the R2 baseline: `EXAMINED: 27 register entr(ies) + 1 dead exemption(s)`, 126 occurrences); `PREFLIGHT: PASS`. No `NOTHING-IN-SCOPE` heading and no blocking FAIL. But the run selected 7 of 75 checks (`check_utf8_md`, `check_json`, `check_yaml`, `validate_cross_refs`, `retired_vocabulary`, `research_contract_baseline_ratchet`, `research_dod_selftest`) because the four changed files are "unclassified ... docs-only": it examined nothing of what the change does.

## Sweep

Names `stress_run`, `lang_probe`, with the file's exclusion list: all four commands give no hit (code/tests/skills/agents/hooks/workflows; `sqlite_master`, an empty list; check registry, an empty list; governance/architecture/CLAUDE.md/references/machines.yaml). Matches the file's "no file". No caller; nothing to repair. I also swept `stress_diff` mentally by the same rule: new name, no hit possible.

## Code-size line

`git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`: **empty** (nothing under those paths changed; the whole change is under `scratchpad/`). Whole commit: 4 files, 92 insertions, 19 deletions. The file asks the PR to "name what reads" each addition; `stress_diff.py` is read by nothing in the repository, only by the later refactor tasks' executors by instruction.

## What a dry pilot cannot show (the coordinator's question)

Things the file assumes that a clone-based dry pilot cannot demonstrate, or demonstrates differently:
- **The scripts act on `/home/user/guidebook`, not on the clone.** `REPO = Path("/home/user/guidebook")` is hard-coded in `stress_run.py`; every `db.py`, `assess_cell.py`, `run_checks.py` call and every `git clone` for the write-path replay uses it. In my pilot the "unchanged" and "repaired" runs therefore exercised the working repository's code (whatever it had checked out), with the *clone's* script text driving it. In a real execution those are the same tree, so the before/after proof works; in a pilot it cannot prove behaviour preservation of a code change, only the harness's own mechanics. Also the write-path replay clones the working tree's committed HEAD (uncommitted refactor edits are not in it) - the file should tell a refactor task to commit before the after-run.
- **`SCRATCH` is another session's directory** (`.../4a95df3b-.../scratchpad/stress-run`), created on demand; the file's `export SCRATCH=...` is not read by the scripts. Two runs share it, which is the cause of the clone-reuse fault. A real execution has the same behaviour; only a pilot makes it visible.
- **Section 11 (adversarial pass, `/batch-done`, PR body, `unsubscribe`)** and `/session-open` are real-execution steps not run. The PR body wants an "EXAMINED before and after" for each check, and the code-size line; the latter is empty here.
- The step 2 proof (no differing step across runs) is the part the whole task rests on, and it is the part that failed (defect 2). A real executor would have hit the section 9 stop here.

## Task-file defects

1. **Section 6 step 2 is unachievable as ordered, and trips section 9.** It says to run `stress_run3.py` twice "on the unchanged tree" and expects no differing step. The unchanged tree contains the clone-reuse fault that section 4.1 repairs, so run 2 differs from run 1 (`real.migrate-rebuild` rc 0 -> 1, `reproducibility-deep` rc 0 -> 1; command: `stress_diff.py run1 run2`). Section 9's last bullet says to stop and not normalise more. Either the order is wrong (repair first, then prove determinism) or the expectation is wrong. I took the first reading.
2. **After repair the two runs still differ, in a field the file forbids hiding.** `real.migrate-rebuild [stderr]`: five example FK-violation tuples are `list(set)[:5]` in `scripts/migrate_db.py` (~line 175/192), so the output depends on hash order; observed run4 vs run5. The file gives no way to a green baseline: it needs a decision (sort the examples in `migrate_db.py`, which is a scripts change section 4 does not name, or declare that line noise in `stress_diff.py`). This is the finding that matters most: a before/after harness that is never equal to itself proves nothing for the refactor tasks that cite it.
3. **"Change one expectation string in a copy of a result log and diff again" cannot show a difference.** Section 4.2 lists the compared fields as argv, rc, stdout, stderr, changed; `expect` is not one. Observed: exit 0, "differing fields: 0". The seeded change must be to `stdout` or `rc`.
4. **No rule for matching steps between two runs.** Tags carry a running counter (`real.026.real.clone`) that shifts when a step is skipped, so the naive match reports eleven phantom differences. The file lists what to normalise but not this; I strip the counter and number repeats. Ambiguous too: "session stamps" (the session ids are constants per topic; what varies is date-times such as `created_at` and `--stamp` echoes).
5. **The repair list (section 4.1) is incomplete or wrong in four places:**
   a. `raise-determination-gate` needs `--trigger-tier` as well as `--trigger-evidence-type` (the refusal text: "must state --trigger-tier and --trigger-evidence-type").
   b. The guard `control-exact` probe is refused as "extraction 119 already carries this exact row (... same lenses ...)" before any guard runs; the control proves nothing. Not listed. I moved the guard cases to lens SCI (a choice the file should make).
   c. The merge probe's arguments come from `value_for`, which maps the flag `--from` to an *extraction id* and fills `--reason` with `1` (observed argv: `merge-parameter --from 11 --into 3 --reason 1`), so "point it at a parameter with no open gate" is not enough; explicit arguments were needed. Once the merge succeeds, the following `retire-parameter` on the merged parameter is refused ("already merged into 4"), another wrong-reason refusal; I retargeted it to the `into` parameter.
   d. "the two guard probes" are three: the homoglyph probe also lacks a locator; with one it is still refused, now for a different, legitimate reason (no retrievable payload to verify the quote against). And `real.add-extraction.MOB` and `reentry.add-extraction` are refused as byte-identical duplicates of extraction 119 (same shape as 5b); I left them and note them.
6. **The SQL-probe repair text does not match the failure.** "`source_locators` joins on `ref_id`": the query already joins `source_locators` on `ref_id`; the failing predicate is `sc.locator=l.locator`. The file does not say what to join `search_candidates` on; I chose `sc.resolved_ref_id=s.ref_id` (a judgment). Also both SQL probes live in `stress_run.py` (passes 2 and 5), which `stress_run3.py` does not run, so the section 6 verification (two runs of `stress_run3.py`) never exercises them; I had to run `stress_run.py --topics cost` and it exceeds 100 s.
7. **Default `--out` destroys the retained evidence.** `stress_run3.py` defaults `--out` to `results3` beside the scripts and `Run.__init__` does `self.log.write_text("")`; the file says nothing about passing `--out`. (Read from the code; I always passed `--out`.) Likewise `RETAINED.md` section 5 says to keep `results3/*/log.jsonl`.
8. **The default parts include `batteries`, which runs `run_checks.py --battery <b> --all` ten times (timeout 1500 s each)**, against section 8 ("Do not run `scripts/run_checks.py --all`") and the brief. The file never says which `--parts` to use. Also `batches` silently "passes": it logs `batches.skip` with rc 0 when the round-1 scratch databases (`acoustics/topic.db`, `reach/topic.db`) do not exist, which is the case in any fresh environment; the file doesn't say that stress_run.py must be run first or that this part is vacuous. Without `batteries` a run takes about one minute; I ran `--parts probes,real,guards,batches,lifecycle,reentry`.
9. **Section 6's checks and the gate do not read what this task changes.** "These registered checks read what this task touches" is false: the change is only under `scratchpad/`, which `run_checks.py` classifies "unclassified ... docs-only"; the gate selected 7 of 75 checks, none of the seven named, and passes. Before/after equality of the seven is guaranteed and says nothing. The real test of this task is the stress diff (defects 1-3).
10. `test_assess_cell_pilot` prints no `EXAMINED:` line (only `PASS: all pilot-engine branch tests`), yet section 6 says each line shows the subject and an absent line means "examined nothing". The file should name it as an exception or say how to count its cases.
11. Section 2's BASE line and its fallback: the named branch `origin/ccr-408aaa9b-z3e4s0` is absent from a clone of the working repository, so the line silently falls to `origin/main`, which lacks the workplan (the brief's override fixed it). The file also repeats the BASE line in section 6 step 4, so a stale choice recurs.
12. Minor: the file says `STRESS-FIXTURE`-style fixtures must not reach `data/guidebook.db`, but does not say that the stress scripts leave `/tmp/claude-0/-home-user-guidebook/4a95df3b-.../scratchpad/stress-run/` populated (clones, scratch databases) outside any task folder; section 8's list does not mention cleanup. The `stress_run.py` run was cut at my 100 s timeout, leaving its scratch half-written.

Stop-condition judgement: defects 1 and 2 are literal section 9 stops ("the two unchanged runs differ after normalisation: report the field"). I reported them and continued, because the cause of 1 is the very fault section 4.1 repairs and the cause of 2 is outside the file's authority. A real execution should not continue past 2 without a ruling.

Files: `/home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-014-report.md`, `/home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-014.patch`. Clone: `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/pilot/T-014` (commit 8295ae6). Run folders: `/tmp/guidebook-t-014/run1` to `run5`, `seed`, `r1`.
