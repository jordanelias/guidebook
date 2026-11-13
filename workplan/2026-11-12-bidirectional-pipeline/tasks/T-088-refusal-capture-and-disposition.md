# T-088  A writer's refusal is kept, and every refusal a batch met is disposed

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the owner's five statements of 2026-11-13 on what the pipeline cannot execute (`grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`, statements 1 to 5), the adjudication's Q10 and proposal P6 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-088 |
| Title | A writer's refusal is kept, and every refusal a batch met is disposed |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 0-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | the owner's statements 1 to 5 of 2026-11-13 (eleventh set); ADJUDICATION Q10, P6; T-089 (the reader across sessions, which reads what this task writes) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. The register reading of the owner's first statement is the one the rules support (ADJUDICATION Q10: rules 3 and 10 and CLAUDE.md §4 leave two lawful acts when a writer refuses, write through an existing verb or park). The other reading, an agent writing the canonical row by hand, is the open owner question OD-54 (the adjudication's AQ-8), and **nothing in this task builds it**: so OD-54 holds no part of this task.
- **Tests that must be red before you start:** `T088-01` (section 6): a refused call leaves no line anywhere.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-088-refusal-capture-and-disposition "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-088" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

When a writer refuses, the sentence that says why is the only record of what the batch tried to hold and could not. It is printed once and lost: the session's command log keeps the command and a hash of what was printed, not the words, and its exit code is not reliable. So a determination can omit a figure, or an inadequacy statement, that its source held, and nothing shows that the batch met it and what became of it. The owner asked for a register of what the pipeline cannot execute, "so we aren't losing content" and "that way we aren't held up" (statements 1 and 2).

**Evidence commands** (read-only):

```
python3 -c "import json;print(sorted(json.loads(open('scratchpad/session_2026-11-13-edmonton-checklist-pass/commands.jsonl').readline())))"
grep -n 'MEASURED CORRECTION' .claude/hooks/record-command.py
grep -n 'except Refusal as exc' scripts/db.py scripts/assess/assess_cell.py
grep -n '^class Refusal' scripts/dbcore.py scripts/assess/assess_cell.py
git grep -n -F 'refusals.jsonl' -- scripts .claude skills governance | head -3
```

**Output on 2026-11-13:** the log's keys are `bytes, command, cwd, exit, interrupted, is_error, response_keys, session_id, stderr_bytes, stderr_sha256, stdout_sha256, tool, ts` (no output text); the hook's own comment records that `exit` is not reliable; one catch point in each of `scripts/db.py` and `scripts/assess/assess_cell.py`, each `sys.exit(f"REFUSING: {exc}")`; two `Refusal` classes (`scripts/dbcore.py` and the engine's own, kept apart on purpose: read the engine's class docstring); no `refusals.jsonl` anywhere. If a capture already exists, the defect is fixed: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. **Do nothing** fails: the sentence is gone and the retry history with it. **A convention alone** (list what you met in `/batch-done`) fails the same way: the operator cannot list a sentence nobody kept. **Reuse:** the register of what is owed is the `gaps` table (`add-gap`; T-013's typed subject columns); the replay command is the refused argv itself, so no payload column or table is added. **Smallest code:** the capture, and one small reader of one session.

1. **Capture, one home: `dbcore.record_refusal(script, argv, sentence)`.** Called at the two catch points, before `sys.exit`: in `scripts/db.py`, `dbcore.record_refusal("scripts/db.py", sys.argv[1:], str(exc))`; in `scripts/assess/assess_cell.py` the same with `"scripts/assess/assess_cell.py"` (the engine already imports `dbcore`: `grep -n '^import dbcore' scripts/assess/assess_cell.py`). The function, stdlib only like the rest of `dbcore`:
   - reads the session stem from `REPO_ROOT / "scratchpad/CURRENT"`; returns, writing nothing, when that file is missing, or `REPO_ROOT / "scratchpad" / <stem>` is not a directory (CLAUDE.md §7: the folder must be named identically to `CURRENT`'s content);
   - reads the value after `--session` in `argv` (bare, with a trailing `.md` removed); returns, writing nothing, unless it equals the stem;
   - appends one JSON line to `scratchpad/<stem>/refusals.jsonl`: `ts` (`dbcore.now()`), `session`, `script`, `verb` (`argv[0]` for `scripts/db.py`; the script's own name for the engine), `argv`, `sentence`, and `db` (`str(dbcore.db_path())`, or the engine's `--db` value: which database refused);
   - never raises: an `OSError` writing the line is swallowed, so the refusal's exit and message are unchanged.
   **Chosen (authoring 2026-11-13): capture only a call whose `--session` is the running session.** Rejected: capture every refusal (the tests call `db.py` as a subprocess and refuse on purpose under `--session session_fixture` and the like, `grep -n 'def cli' -A3 scripts/tests/test_run_pipeline_refusals.py`; their refusals would fill the running session's record with fixtures); an environment switch to turn capture off (every test and probe must remember it, and one that forgets floods the record). A probe run under `session_probe` is deliberately not captured: it is not the batch's content.
   **Chosen: the line holds only what was said and done.** The derived fields (the stage the verb writes to, the tables it touches, the rule ids the sentence cites, a signature that clusters recurring refusals) are computed by the reader, T-089, from these fields and the live repository. Rejected: storing them in the line, as first proposed. `dbcore` is stdlib only and cannot read `governance/stage-map.yaml`; and a derived value stored beside its input drifts when the derivation improves (rule 5, rule 8): a signature normalised one way in October and another in December splits one class in two.
2. **A reader of one session, and the disposition: `scripts/audit/refusal_register.py`.** Stdlib only. Two subcommands:
   - `list [--session S]` (default: `scratchpad/CURRENT`): reads `scratchpad/<S>/refusals.jsonl` and prints, per refusal, its `ts`, `verb`, the sentence's first 160 characters and its disposition or `UNDISPOSED`; then `EXAMINED: <n> refusal(s)`; exits 1 when any is undisposed, 0 otherwise (also 0 with `EXAMINED: 0` when the file does not exist: say "no refusal captured").
   - `dispose --session S --ts T --as retried|parked|waived [--gap-id G] [--reason R]`: appends a line `{"kind": "disposition", "refusal_ts": T, "as": ..., "gap_id": ..., "reason": ..., "ts": now}` to the same file. Refuses (`REFUSING:` and exit 1): a `T` no refusal line of the file carries; `parked` without `--gap-id`, or with a gap id absent from the `gaps` table of the database the refusal line names (`db`), or, if that file is gone, of `data/guidebook.db`; `waived` without `--reason`; a second disposition of the same refusal.
   **Chosen:** the three dispositions are declared once, as a constant in this script, and read from there by `list` and `dispose` (the owner's 2026-11-12 line: a rule declared once in a stated place is not hard-coding, `grep -n -F "isn't hardcoding necessarily" references/project-standards.md`). Rejected: a table with a CHECK (a disposition is a fact about a session's record, held beside it in the committed scratchpad, rule 6; no other table reads it).
3. **The Layer 0 rule, in `/batch-done`.** In `.claude/commands/batch-done.md`, after the three gate lines, add:
   ```
   python3 scripts/audit/refusal_register.py list --session "$(cat scratchpad/CURRENT)"
   ```
   and the sentence: "Every writer refusal this batch met is disposed before the batch is done: **retried** (the writer was right; the corrected call succeeded), **parked** (its content waits: file a gap with `db.py add-gap`, typed by its subject, and keep the refused argv, which is the replay command), or **waived** (with a reason). An undisposed refusal is a batch that is not done."
4. **The Layer 2 protocol, in the skill.** In `skills/run-pipeline_SKILL.md`, section "Resume and exceptions", add one paragraph: "**When a writer refuses** (Layer 2 protocol; the capture is Layer 1, the `/batch-done` rule Layer 0): acknowledge (correct the call and write the row, if the refusal was right), or refuse-and-park (keep the refused argv, file a gap naming what is held back, and go on: the batch is not held up), then replay (the parked content is written through the sanctioned writer in a later research pull request, after the tooling pull request that closes the gap has merged, rule 10). Never write the row by hand: the content waits in the register, not in the database (`CLAUDE.md` rules 3 and 10; OD-54 is open). `refusal_register.py list` shows what the batch met."
5. **Not built here:** the reader across sessions, its classes and its cues (T-089); a registered check (review is the gate until it proves insufficient: ADJUDICATION Q10's Layer 0 note); any path that writes a canonical row by hand (OD-54).

**What reads what this task adds:** `/batch-done` (the `list` line); the research batch's pull request (the disposition list); T-089 (every committed `refusals.jsonl`). **What wrong thing reaches the guidebook without it:** a determination that omits a figure or an inadequacy statement its source held, with no record that it was met. **What it makes deletable:** nothing.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

### 4a. Design: the refusal register (owner statements 1 to 5, 2026-11-13)

*This subsection is the design both T-088 and T-089 build to. It decides no doctrine.*

- **Layers** (CLAUDE.md §3). **Layer 1, the carrier:** `dbcore.record_refusal`, one home for every writer, and the line's shape. **Layer 2, per-stage triage:** each stage meets the refusals its writers make, and the protocol is the same at every stage: *acknowledge* (the row is written), *refuse-and-park* (the sentence and argv are kept, a gap is filed, the batch goes on), *replay* (through the sanctioned writer, in a research pull request after the tooling merges). Which checks and which skill section a refusal at a stage cues is derived by T-089, not listed. **Layer 0, the gate:** `/batch-done`'s rule that every refusal met is disposed; a registered check only if review proves insufficient. **Layer 3:** the parked content and the rows the replay writes. This is a Layer 2 protocol on a Layer 1 carrier under a Layer 0 gate, not a new stage-pair contract: the stage-pair checks (`judgment_handoff_shape`, `derivation_handshake_integrity`) test rows already written, and a refusal happens at a writer, inside a stage.
- **The five failure classes** (the adjudication's; recorded on the disposition and the gap, never as a second vocabulary). (1) *A policy refusal that was right:* disposition `retried`, no gap. (2) *A missing verb or field:* `parked`; a gap, category `SW` (the category the register already uses for writer gaps: `select category, count(*) from gaps group by 1`), replayed after the tooling pull request. (3) *A tool defect:* `parked`; a gap, category `SW`. (4) *An environment block* (a publisher 403, a lost connection): not a writer refusal, so it is not captured here; its homes exist (`--processing-blocked-reason`, and the deferred acts of T-079). (5) *A data conflict:* the writers already accept a contest row or a follow-up, so it is `retried` through those verbs, or `waived` with the reason. Classes (2) and (3) share `SW`; the gap's description says which. **Chosen:** no new gap category. Rejected: a failure-class column (the owner asked that refusals be "dynamically typed/categorized", statement 4; T-089 derives the class of a refusal from its sentence's signature and its disposition, and a typed column would be a second, curated vocabulary).
- **The replay rule.** Parked content is replayed through the sanctioned writer in a research pull request after the tooling that closes its gap has merged (rule 10). The refused argv is the replay command; the replay session runs it as written, or as the closing tooling's new verb requires, and closes the gap.
- **The line the owner's first statement leaves open.** "alongside having an agent fix it by hand with correct context" is read as: the agent records the intended row (the argv), its refusal and a proposed amendment in the register. A canonical row written by hand is **not** part of T-088 or T-089; it is OD-54 (the adjudication's AQ-8), open.
- **The cue** (statement 5: "a cue to run a script/double check a protocol or skill/etc to ensure that the digest was actually performed correctly"): T-089 prints, for each refusal a batch met, the registered checks and the skill section of the refused verb's stage, derived from the repository; `/batch-done` re-runs those checks and re-reads that section before the batch is called done.

## 5. Caller sweep

Names to sweep: `except Refusal as exc`, `REFUSING:`, `record_refusal`, `batch-done`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: a test that asserts a refusal's stderr or exit (the capture must leave both unchanged: such a test going red has found a changed exit); a skill or command sentence that says how a refusal is handled, or that a refusal leaves no record; a registry entry. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/` except `workplan/pipeline-state-graph/machines.yaml`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_assess_cell_pilot claude_skills_loadable skill_vocabulary_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Record what is red before (`skill_vocabulary_audit` was red on 2026-11-12) and carry on.

**Step 2: red before, green after** (cases `T088-01`… in `scripts/tests/test_run_pipeline_refusals.py`; prefix free: `git grep -c 'T088-' scripts/tests/`). The tests never touch the real `scratchpad/CURRENT`: they call `dbcore.record_refusal` in-process with `dbcore.REPO_ROOT` pointed at a temporary directory that holds its own `scratchpad/CURRENT` and session folder (patch the module attribute for the call and restore it).
- `T088-01` a refusal whose argv carries `--session <the temp stem>` appends exactly one line with the six fields and `db`; red before (no function: assert the attribute exists, so an absent function cannot pass).
- `T088-02` a refusal under another session, with no `--session`, with `CURRENT` missing, and with the folder named differently from `CURRENT`, appends nothing.
- `T088-03` an unwritable session folder (`chmod` it read-only on the temp tree): the function returns without raising.
- `T088-04` through the CLI: `db.py` refused under `--session session_fixture` (choose the refusal by an existing case of the file) exits 1 with the same `REFUSING:` text as before, and the real session folder's `refusals.jsonl` (if any) does not change size.
- `T088-05` `refusal_register.py`: on the temp tree, `list` exits 1 with one `UNDISPOSED`; `dispose --as parked` without `--gap-id` refuses, with a gap id that is not a row refuses (the id built by query to be absent), with a real gap id (built on a scratch copy by `add-gap`, labelled `TASK-FIXTURE`) succeeds; `list` then exits 0; a second `dispose` of the same refusal refuses.
- Seeded defect: drop the session-equality test in `record_refusal`; `T088-02` goes red; restore.

**Fixtures** go to a copy or a temporary tree, are labelled `TASK-FIXTURE`, and never reach `data/guidebook.db` or the real scratchpad.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail; `test_run_pipeline_refusals`'s `EXAMINED:` grows only by the T088 cases.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: keep each writer refusal and dispose of every refusal a batch met [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's statements it answers; evidence before and after; the capture rule and why; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not change a refusal's text, its exit code or what it writes (nothing).
- Do not capture output other than the refusal sentence; do not capture a call whose `--session` is not the running session.
- Do not add a gap category, a table or a column; do not register a check.
- Do not build any path that writes a canonical row by hand (OD-54).
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: a capture of refusal sentences already exists; a refusal's exit or message changes; a test that refuses on purpose writes a line into the real session folder; the engine cannot import `dbcore` (its import roster changed); a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request; the captured lines in committed scratchpads stay as records.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
