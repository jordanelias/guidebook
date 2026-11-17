# T-130  The consolidation sweep: candidate pairs proposed from the live base, judged, and stopped by a bound held in the contract

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-130 |
| Title | The consolidation sweep: candidate pairs proposed from the live base, judged, and stopped by a bound held in the contract |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); one read verb, one contract key and its model field, the batch command and skill text, tests |
| Executor | Sonnet-class, executing `tasks/T-129-design.md` section B (the proposer's four reasons, the re-proposal rule, the bound and the loop are stated there in full). The judging of candidates is T-131's, not this task's |
| Traces to | the owner's question Q2 of 2026-11-16 ("an iterative loop with limited repetitions to ensure exit … so we don't end up with duplicates or near identical topics") and Q3 ("systematically perform new passes over already-recorded rows … if the base gets extended"); the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (gaps G1, G3, G4); E4 (`grep -n -E '^\| E4 ' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-129, T-049 merged (T-129 gives the survivor view, the merge rows and the `distinct` rows the proposer reads; T-049 gives `v_translations_current`, which reason R4 reads); `T-129-design.md` present. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. Reason R4 reads only translations reviewed under OD-30 (delegated, through T-049). OD-68 is not a gate (design D (3)).
- **Tests that must be red before you start:** `T130-01` to `T130-07` (section 6): the verb does not exist and the contract has no `consolidation:` key.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-130-consolidation-sweep "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-130" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

The write-time screens catch a near duplicate only at the moment a name is minted, only within a language, and never through a model-generated seed (E4). A form promoted later (T-069), attested later (T-107) or translated later (T-112) can show that two held concepts are one, and nothing proposes the pair again. Some pairs already exist: one form held by two concepts in one language (the evidence command lists them; some are search seeds, some unrecorded aliases, and at least one names two different quantities, which is a homonym a judge must record as two, not merge). The owner asked for a loop that consolidates topics across languages and synonyms, with limited repetitions, so that duplicates do not accumulate.

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select upper(language), lower(alias), group_concat(distinct term_id), group_concat(distinct attestation) from term_aliases where alias_type not in ('NARROWER','BROADER') group by 1,2 having count(distinct term_id)>1\").fetchall())"
python3 -c "import yaml;print('consolidation' in yaml.safe_load(open('governance/pipeline-contract.yaml')))"
python3 scripts/db.py consolidation-candidates 2>&1 | tail -1 | cut -c1-80
```

**Expected output today:** a non-empty list of (language, form, terms, attestation) rows: forms held by more than one concept in one language (count them, never quote the count); `False`; `invalid choice: 'consolidation-candidates'`.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

Build section B of `workplan/2026-11-12-bidirectional-pipeline/tasks/T-129-design.md`, exactly:

1. **`db.py consolidation-candidates [--pass N] [--language L]`,** read-only (it opens the database `mode=ro`), with the four reasons of design B2, the re-proposal rule of B3, the output and exit code of B1, and the `owner` mark of B5 for a pair touching `dbcore.NON_QUANTITY_DOMAINS`. It reuses `_name_tokens` and the near rule of `_near_terms` (one function for the near rule, called by both: if `_near_terms` holds it inline, lift it into one helper both call; write no second copy). The function behind the verb takes a keyword `contract_path` (default: the committed contract) that the CLI does not expose.
2. **The bound, held once:** `governance/pipeline-contract.yaml` gains `consolidation:` with `max_passes: 3`, **appended at the end of the file** (the atoms of `workplan/pipeline-state-graph/atoms/` cite the file's lines by number until T-134 merges; confirm the end is clear with `grep -rhoE 'pipeline-contract\.yaml:[0-9]+' workplan/pipeline-state-graph/atoms | cut -d: -f2 | sort -n | tail -1` below `wc -l < governance/pipeline-contract.yaml`); `schemas/pipeline_contract.py` gains the optional model (`extra="forbid"`, one field `max_passes: int` with `ge=1`). No number appears in the verb's code.
3. **The loop, written where it is read:** `.claude/commands/batch-done.md`'s COVERAGE section prints `python3 scripts/db.py consolidation-candidates` (printed, not failed, as the section's other reads), and `skills/run-pipeline_SKILL.md` states the loop of design B4 and the verdicts of B5 in plain text (the contract rule in plain text, never in backticks: the key path is not a name `skill_vocabulary_audit` can resolve).
4. **Test file** `scripts/tests/test_consolidation_candidates.py`, registered `test_consolidation_candidates` (`battery: tests`, `kinds: [tooling, schema]`, `level: advisory`, `basis: hygiene`, `no_floor: selftest — …`), with the cases of design B7.

**What reads what this task adds or changes:** the verb's output: the session judging candidates (T-131 and every later batch, through the skill), the owner (the batch's pull request, through `/batch-done`). The contract key: the verb, and `pipeline_contract_audit` (it loads the contract). `contract_path`: the test only.

**No schema migration.** This task changes no table; the pull request contains no file under `scripts/migrations/`.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `pipeline-contract.yaml`, `_near_terms`, `_name_tokens`, `NON_QUANTITY_DOMAINS`, `batch-done`, `COVERAGE`

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

**Callers already known** (found by this file's author; each is in scope): `schemas/pipeline_contract.py` forbids unknown keys, so the contract key and the model field land together, and `scripts/audit/pipeline_contract_audit.py` and `scripts/tests/test_pipeline_contract.py` must pass before and after; the atoms of `workplan/pipeline-state-graph/atoms/*.jsonl` (they cite contract lines by number: append at the end); `skills/run-pipeline_SKILL.md` and `.claude/commands/batch-done.md` (the two sentences of item 3).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `pipeline_contract_audit test_pipeline_contract derived_not_curated_audit skill_vocabulary_audit context_map_fresh test_term_merges`. Run each as the registry runs it and keep the output:

```
CHECKS="pipeline_contract_audit test_pipeline_contract derived_not_curated_audit skill_vocabulary_audit context_map_fresh test_term_merges"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_consolidation_candidates.py`, on its own scratch copy, with the cases of design B7 (`T130-01` to `T130-10`); every fixture built by query (a term with an attested form in a language, a second term to share or near it), labelled `TASK-FIXTURE`. Before: the file cannot run. After: green. Also, on the live database, `python3 scripts/db.py consolidation-candidates` lists at least the pairs the evidence command's attested rows imply (derive the expectation from that query, never type it), and `build_graph.py --check` prints exactly the before-run's failure lines (`diff` them: a new `not near cited line` for the contract means the key was not appended at the end).

**Writing the test.** Case ids carry this task's prefix (`T130-01`, …); confirm it is free first (`git grep -c '"T130-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: propose consolidation candidates from the live base, with the pass bound held once in the contract [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not write a merge, a relation or a `distinct` row (that is T-131's research, CLAUDE.md rule 10); do not register a check that fails while candidates exist (design C, F).

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- the contract model cannot take a new top-level key without changing how existing keys validate;
- `v_translations_current` or a `status` of `reviewed` is not on your base (T-049 not merged): do not build R4 against another column;
- a reason would need a vocabulary the schema does not hold (the reason codes are `term_merges.candidate_reason`'s CHECK, from T-129).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
