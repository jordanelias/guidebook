# T-132  The drift detectors bind once their subject exists (a stale stored determination, a write to a folded term), and the prose about a deleted cron is corrected

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-132 |
| Title | The drift detectors bind once their subject exists (a stale stored determination, a write to a folded term), and the prose about a deleted cron is corrected |
| Wave | 6 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); a registry level, two docstrings and one contract hook sentence; no schema, no code path |
| Executor | Sonnet-class |
| Traces to | the owner's question Q4 of 2026-11-16 ("how does the pipeline handle propagation in all directions whenever there is a change made to a row"); the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G7, G8, G10); `scripts/audit/derivation_handshake_integrity.py` docstring item 6 and its ratchet paragraph |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-110, T-131 merged (T-110 writes the first live determinations and T-131 the first term merges: before them each check is vacuous, and a blocking check over nothing is a defect `run_checks.py` already reports). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none.
- **Tests that must be red before you start:** `T132-01` (section 6): the registry holds `derivation_handshake_integrity` and `term_merge_integrity` at `advisory` while their subjects exist.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-132-drift-detectors-bind "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-132" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

A determination is a stored answer over inputs that `derivation_sha` does not hash (a source's verification and tier, a row's grading and comparator, a `confirms` edge). The project's detector for a stored answer the engine would no longer give is a recompute (`assess_cell.stale_determinations`, run by `derivation_handshake_integrity`), which catches every input the engine reads, by whatever route it moved. It is advisory, and its own docstring says to ratchet it to blocking with the first live determination; no task does that, and rule 10 forbids doing it in T-110's research pull request. So once determinations exist, the book can show a ● over a source since demoted with nothing red. Separately, three sentences still name a scheduled verification cron as a route that bypasses the writers; it was deleted on 2026-10-14 (`grep -n -F 'The scheduled cron that polled this pool was deleted' scripts/audit/research_batch_dod.py`), so the prose callers state a fact that is false (CLAUDE.md rule 7a, the third shape).

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 -c "import yaml;print([(c['id'],c['level'],c.get('min_items')) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if c['id']=='derivation_handshake_integrity'])"
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from specifications where retired_at is null').fetchone())"
grep -n -i 'cron' scripts/audit/derivation_handshake_integrity.py scripts/assess/assess_cell.py governance/research-contract.yaml
```

**Expected output today:** `advisory` with `min_items` 1; on 2026-11-17 no live determination (this task runs only after T-110, so on its base the count is above 0); one line naming the cron in each of the three files.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **The ratchets.** In `governance/check-registry.yaml`, `derivation_handshake_integrity` moves to `level: blocking` (its `min_items: 1` stays; determinations are retired, never deleted, so the floor holds), and `term_merge_integrity` (T-129) moves to `level: blocking` with `min_items: 1` (a merge is retired, never deleted). Before each edit, run the check on the base: it must pass with `EXAMINED:` above 0; if `derivation_handshake_integrity` fails, the failing determinations are stale and are retired and re-determined in a research pull request first, and if `term_merge_integrity` fails, a row was written to a folded term by a route that skipped the writers (stop, section 9, either way).
2. **The prose callers.** Correct the sentence about the cron in the docstring of `scripts/audit/derivation_handshake_integrity.py` (item 6) and in `scripts/assess/assess_cell.py` (the docstring of `stale_determinations`), and the hook text in `governance/research-contract.yaml` that says the cron "pushes a DB blob to main": each names only routes that exist (a data migration; a route not yet thought of). Keep the research contract's rule (never leave `verification_status` NULL) and its reason; drop only the cron. **`governance/research-contract.yaml` is injected by a hook:** after the edit, run the check that compares it (`python3 -c "import yaml;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if 'research_contract' in c['id']])"` names it) and regenerate what it says to regenerate.
3. Nothing else: the sha is not extended (the adjudication, G8: a second definition of the engine's inputs, beside the engine itself, would drift from it), and no trigger is added (G7).

**What reads what this task adds or changes:** the gate (`scripts/preflight.sh`, CI) on every diff that changes data, schema or governance (the check's `kinds`); the three corrected sentences: the next reader of each file.

**No schema migration.** This task changes no table; the pull request contains no file under `scripts/migrations/`.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `derivation_handshake_integrity`, `term_merge_integrity`, `cron`, `stale_determinations`

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

**Callers already known** (found by this file's author; each is in scope): `governance/research-contract.yaml` (injected by the `SessionStart` hook: `research_contract_sync` compares it; never insert a hook, CLAUDE.md §7); `scripts/run_checks.py --selftest` (a level change is a registry change).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `derivation_handshake_integrity term_merge_integrity test_db_integrity research_contract_sync`. Run each as the registry runs it and keep the output:

```
CHECKS="derivation_handshake_integrity term_merge_integrity test_db_integrity research_contract_sync"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_drift_detector_level.py`, registered `test_drift_detector_level` (`battery: tests`, `kinds: [governance]`, `level: advisory`, `basis: hygiene`, `no_floor: selftest — …`), with `T132-01`: when the database holds a live determination (derive: `select count(*) from specifications where retired_at is null`), `derivation_handshake_integrity` is `blocking` in the registry, and when it holds a live term merge (`select count(*) from term_merges where retired_at is null`), so is `term_merge_integrity`; `T132-02`: no file under `scripts/`, `schemas/` or `governance/` names a scheduled verification cron as a live route (`git grep -i -E 'verification cron|url-verification cron'` outside `scripts/migrations/` and the sentence of `research_batch_dod.py` that records its deletion). Before: both red on T-110's base. After: green. Run `python3 scripts/run_checks.py --selftest` after the registry edit.

**Writing the test.** Case ids carry this task's prefix (`T132-01`, …); confirm it is free first (`git grep -c '"T132-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: the drift detectors bind once their subject exists, and the deleted cron leaves the prose [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not extend `derivation_sha` or add a trigger (section 4 item 3).

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- `derivation_handshake_integrity` fails on the base (a stored determination is stale): the remedy is research (retire and re-determine), not this pull request;
- no live determination or no live term merge exists on your base (T-110 or T-131 not merged, or their rows retired): a blocking check over nothing is a defect; stop.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
