# T-134  The state-graph instrument finds an atom by its quote, not its line number, and draws the ruled returns

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-134 |
| Title | The state-graph instrument finds an atom by its quote, not its line number, and draws the ruled returns |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); the instrument under `workplan/pipeline-state-graph/` and its contract extractor; no schema |
| Executor | Sonnet-class |
| Traces to | the owner's statements O7 and O8 of 2026-10-12 (walkability; "handshake ALL directions"); the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G11, G13); the sweep list of the stacked batch, T-022 item 5 (`scratchpad/session_2026-11-16-remediation-batch-1-tooling-stack/sweep-list.md`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-022 merged (it writes the ruled returns, `re_entry`, into `governance/pipeline-contract.yaml`). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none.
- **Tests that must be red before you start:** `T134-01`, `T134-02` (section 6).
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-134-state-graph-quotes-and-returns "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-134" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

The instrument that shows whether the pipeline can be walked in every direction is red on the base with about a hundred failures, and nearly all of them are not about the pipeline: an atom cites the line of a governance file it quotes, and the check fails when the quote has moved more than a few lines (the evidence command groups them). A line number typed into a file is a number that goes stale with nothing wrong (CLAUDE.md rule 7a), and an instrument red by construction teaches its reader to ignore it (rule 6). Every task file now tells its executor to diff the failure lines before and after, which works, but the real pipeline failures are lost among the drift. And the returns the owner ruled (re-entry from a later stage to an earlier one) are in the contract since T-022, but the extractor draws stages and criteria only, so the graph shows a one-way pipeline.

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 workplan/pipeline-state-graph/build_graph.py --check 2>&1 | grep FAIL | sed -E 's/FAIL +[A-Z0-9]+-[0-9]+: //; s/cited line [0-9]+/cited line N/; s/: .*$//' | sort | uniq -c
grep -c -i 're_entry' scripts/audit/graph/extract_contract.py
```

**Expected output today:** most failure lines are `quote found in <file> but not near cited line N`, grouped by file (the ledger holds most), and a few `QUOTE NOT FOUND`; `0` (the extractor never reads `re_entry`).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Quote first, line second.** In `workplan/pipeline-state-graph/build_graph.py` (the check that prints `not near cited line`, `grep -n 'not near cited line' workplan/pipeline-state-graph/build_graph.py`) and in `workplan/pipeline-state-graph/verify_atoms.py` if it holds the same rule: an atom passes when its quote is found **exactly once** in the cited file; the cited line is then informational and a quote found far from it prints a `MOVED <id>: cited line A, found at line B` line that does not fail. A quote found more than once fails unless one hit is within the present tolerance of the cited line (the line disambiguates). A quote not found still fails. Nothing else in the checker changes.
2. **The returns drawn.** `scripts/audit/graph/extract_contract.py` reads each stage's `re_entry` entries (their stage, their target stage, their carrier column) and emits one edge per entry, of a kind that says it is a ruled return; the builder renders it in `STATE-GRAPH.md` and `graph.json` (regenerate both: they are derived files, written by the builder). `workplan/pipeline-state-graph/walkability.py` is not changed: whether a cross-stage table counts as a member of each stage it carries stays as T-051 left it (the adjudication, G11: no table records the stage that raised a gap until a reader needs it).
3. **Remove the instruction it makes stale.** Task files that tell an executor to append a contract key at the end because atoms cite lines (T-049 item 4, T-130 item 2) stay true and need nothing; the sentence in `workplan/pipeline-state-graph/README.md` that describes the line check, if any, is corrected.

**What reads what this task adds or changes:** every task file's before-and-after `build_graph.py --check` (its failures are now pipeline facts and real missing quotes); the owner's walkability reading (`WALKABILITY.md`, `STATE-GRAPH.md`); `MOVED` lines: whoever re-quotes atoms (T-120).

**No schema migration.** This task changes no table; the pull request contains no file under `scripts/migrations/`.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `not near cited line`, `re_entry`, `extract_contract`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you change; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention*. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`; `machines.yaml` there is hand-written and is swept); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference; it is red on the base, so only a failure line your change adds is yours. An object that returns 0 rows is unproven, not clean.

**Callers already known** (found by this file's author; each is in scope): `scripts/audit/graph/extract_contract.py` is also read by `graph_audit` (`python3 -c "import yaml;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if 'graph' in str(c.get('cmd'))])"`): run it before and after; the hand-written atoms (`workplan/pipeline-state-graph/atoms/*.jsonl`) are data and are not edited by this task (T-120 re-quotes the ones its doctrine edits move).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `graph_audit test_graph_audit pipeline_contract_audit test_pipeline_contract`. Run each as the registry runs it and keep the output:

```
CHECKS="graph_audit test_graph_audit pipeline_contract_audit test_pipeline_contract"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_state_graph_instrument.py`, registered `test_state_graph_instrument` (`battery: tests`, `kinds: [tooling]`, `level: advisory`, `basis: hygiene`, `no_floor: selftest — …`). `T134-01`: on a temporary copy of a cited file with three blank lines inserted above a quoted line, the atom passes and a `MOVED` line is printed; with the quote's text changed, it fails. `T134-02`: the extractor emits one return edge per `re_entry` entry of the committed contract (count them from the contract, never type it). `T134-03`: a quote that occurs twice in the file, neither near the cited line, fails. Also: `build_graph.py --check` after the change prints no `not near cited line` failure, and every remaining failure line was in the before-run (`diff` them).

**Writing the test.** Case ids carry this task's prefix (`T134-01`, …); confirm it is free first (`git grep -c '"T134-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`; compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before.

**Step 4: the gate, once**, when every edit is made, before the commit, in the background with a long timeout:

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`. A FAIL on a check that was red on the base is not yours: run its `cmd` once on the base in a worktree and give both lines.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: the state-graph instrument finds an atom by its quote and draws the ruled returns [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, from `date -u`.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row or any synthesis prose.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, merges, determinations) in this pull request (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb, flag or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller** the sweep of section 5 finds.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not edit an atom's quote or line to make it pass (T-120 owns the atoms' text).

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- `re_entry` is not in `governance/pipeline-contract.yaml` on your base (T-022 not merged);
- a failure line that was not a line-drift failure disappears after your change (you weakened the quote check).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
