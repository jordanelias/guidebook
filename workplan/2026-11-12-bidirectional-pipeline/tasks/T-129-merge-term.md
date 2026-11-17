# T-129  Two terms judged one concept merge by a row, the survivor is derived, and a judgment that they are two is kept

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-129 |
| Title | Two terms judged one concept merge by a row, the survivor is derived, and a judgment that they are two is kept |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); a schema migration (one table, one view), two verbs, a writer change in `add-term`, one advisory check, tests |
| Executor | NOT FOR SONNET: Opus-class, executing `tasks/T-129-design.md` section A. The design is stated, but the sweep of every reader of a concept (section 5) needs a judgment per reader of whether it asks about a concept or about a record |
| Traces to | the owner's questions Q2 and Q4 of 2026-11-16 and the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (gaps G1, G2, G3); OD-03 and OD-18 (`grep -E '^OD-(03|18):' references/project-standards.md`); "retire in place then"; T-029 section 4 item 2 (which names a merge as the act for two terms that name one concept, while no verb merges terms) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-028, T-029 merged (T-028 gives a concept its forms by `form_id` and the screens this task makes read through the survivor; T-029 gives the term-relation table this task writes `distinct` rows into, with the kind and the retire-in-place columns its amendment of 2026-11-17 adds); `T-129-design.md` present (written 2026-11-17). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. The task rests on OD-03 and OD-29 (delegated, through T-028 and T-029). OD-68 (cross-language clashes, the owner's) is not a gate: the merge is judged per pair whatever the answer, and the answer changes only what the screens refuse (T-028).
- **Tests that must be red before you start:** `T129-01`, `T129-03`, `T129-04`, `T129-06` (section 6): no merge verb, no survivor, `--distinct-from` leaves only prose.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-129-merge-term "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-129" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

Two names for one concept become two concepts, and the evidence for one quantity splits between them: a determination rests on half its figures, and the book prints two near-identical topics. The write-time screens (`_name_holder`, `_near_terms`) stop a near duplicate when it is minted, but nothing joins two concepts found to be one afterwards: `merge-parameter` folds parameters, `rename-term` relabels, and no verb merges two terms. T-029 already says that two terms naming one concept are a dual home whose remedy is a merge (its section 4 item 2), and names `merge-parameter` and `rename-term` for it, neither of which merges terms. And when a session decides that two near names are two concepts (`add-term --distinct-from`), the judgment is kept only as words inside the new term's adjudication rationale, so no later pass can know the pair was judged.

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from sqlite_master where name in ('term_merges','v_term_survivor')\").fetchall());print([(t,f[3]) for (t,) in c.execute(\"select name from sqlite_master where type='table'\") for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if f[2]=='terms'])"
python3 scripts/db.py --help | tr ',{}' '\n\n\n' | grep -c -x -E 'merge-term|unmerge-term'
```

**Expected output today:** `[]` (no table, no view); the tables whose foreign keys point at `terms` (on 2026-11-17: `term_aliases`, `term_adjudications`, `base_parameters`, `parameter_declinations`; after T-029, its relation table too); `0` (no verb).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

Build section A of `workplan/2026-11-12-bidirectional-pipeline/tasks/T-129-design.md`, exactly:

1. **One schema migration:** the table `term_merges` and the view `v_term_survivor` (design A2, A3), the `candidate_reason` CHECK holding `R1`, `R2`, `R3`, `R4` (design B2 defines them; T-130 prints them), and every view the sweep of section 5 rewrites to read through the survivor, dropped and recreated in the same migration.
2. **One helper,** `dbcore.term_survivor(conn, term_id)`; nothing else follows `term_merges`.
3. **Two verbs in `scripts/db.py`:** `merge-term` and `unmerge-term`, with the refusals of design A4, each naming the next action. No `choices=` list: `--candidate-reason` is validated by `dbcore.check_declared` against the column's CHECK.
4. **Every writer that takes a term id resolves it and refuses a folded one, naming the survivor** (design A4, the set derived as it says), and `_name_holder` and `_near_terms` report survivors.
5. **`add-term --distinct-from` writes a `distinct` row** of T-029's table per named term, warranted by the new term's NAMES-NEW adjudication, in the same transaction (design A6).
6. **One advisory check,** `scripts/audit/term_merge_integrity.py`, registered in `governance/check-registry.yaml` as design A7 states, printing `EXAMINED:`.
7. **Test file** `scripts/tests/test_term_merges.py`, registered `test_term_merges` (design A8).
8. `governance/stage-map.yaml`: `term_merges: base` under `tables:`, with one dated history line naming T-129.
9. `skills/run-pipeline_SKILL.md`: one sentence where a term is minted or adjudicated: two terms found to be one concept are merged with `merge-term` (never by re-pointing rows); two found to be two are recorded with `--distinct-from` or T-029's `distinct`.

**What reads what this task adds or changes:** `v_term_survivor`: every writer that takes a term id, the two name screens, `v_term_names` (T-028), T-057's base coverage view, `term_merge_integrity`, and `consolidation-candidates` (T-130). `term_merges`: the view, the integrity check, T-130's proposer (a merged pair is never proposed). The `distinct` rows: T-130's proposer (a judged pair is not proposed again until the base grows under it) and `merge-term`'s refusal.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py`. Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). A view the migration rewrites is dropped and recreated in it; list them first (`select type, name from sqlite_master where sql like '%<table>%'`). The pull request contains no `scripts/migrations/data_*` file. After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and commit the regenerated `governance/context-map.yaml` (again after your last edit to `scripts/`).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `term_id`, `--term-id`, `canonical_en`, `term_aliases`, `_name_holder`, `_near_terms`, `--distinct-from`, `distinct_from`, `writable_tables`

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

**Callers already known** (found by this file's author; each is in scope): every view of design A5's second command (each is a caller: recreate it in the migration, and exercise it on the fixture, since several render 0 rows on the base); `scripts/audit/alias_provenance_audit.py` (reads forms per term); the parsers of the writers listed in design A4; `governance/context-map.yaml` (regenerated); `scripts/tests/test_scan_contract.py` and `scripts/tests/test_db_amend_writers.py` (they assert the capture set).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `schema_reference_audit test_db_integrity migration_reproducibility column_vocabulary_audit derived_not_curated_audit alias_provenance_audit identifier_floor_audit context_map_fresh test_db_amend_writers test_scan_contract skill_vocabulary_audit`. Run each as the registry runs it and keep the output:

```
CHECKS="schema_reference_audit test_db_integrity migration_reproducibility column_vocabulary_audit derived_not_curated_audit alias_provenance_audit identifier_floor_audit context_map_fresh test_db_amend_writers test_scan_contract skill_vocabulary_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_term_merges.py`, on its own scratch copy, with the cases of design A8 (`T129-01` to `T129-10`). Before: the file cannot run (no verb, no table). After: green, and `term_merge_integrity` passes with `EXAMINED:` equal to the merges the test left on its copy when pointed at it. Show `T129-09` red on a seeded `INSERT` that files a form under a folded term after the merge, then remove it.

**Writing the test.** Case ids carry this task's prefix (`T129-01`, …); confirm it is free first (`git grep -c '"T129-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: merge two terms by a judged row with a derived survivor, and keep a judgment that two near names are two concepts [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not re-point, UPDATE or copy any row of another table to the survivor (design A1): the merge is the row.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- a reader in the sweep of section 5 cannot be classed as asking about a concept or about a record without a judgment of meaning you cannot make from the code: report it;
- T-029's table lacks the kind `distinct` or the retire-in-place columns on your base (its amendment of 2026-11-17 not applied);
- the live database already holds a row that would make `merge-term` or a writer refusal fire on rows written before this task (report the rows; do not repair data in a tooling pull request);
- the owner has answered OD-68 in a form that changes what counts as one concept across languages: the answer governs and this file is corrected first.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
