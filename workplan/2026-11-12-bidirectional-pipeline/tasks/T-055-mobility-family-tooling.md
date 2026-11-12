# T-055  Tooling for the mobility family: the devices it needs, and a parent's determination that gathers its children

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Written in the last fold pass of 2026-11-12, from the owner's third set of answers. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-055 |
| Title | Tooling for the mobility family: the devices it needs, and a parent's determination that gathers its children |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OD-14 (owner, 2026-11-12, third set: decompose `MOB` by device); the owner's statement of 2026-11-12 (second) on unifying at an abstract vantage; T-102's design |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-019 merged; and the design `T-102-design.md` present (it names the `device_class` values and the children; this task builds only what it names). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words.
  - **OD-14** — answered by the owner, 2026-11-12 (third set): MOB decomposed by device (`grep -n -F "OD-14: MOB is decomposed by device" references/project-standards.md`). Check: `grep -F "OD-14 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`.
- **Tests that must be red (or green) before you start:** `device_class` has no value for a prosthesis, crutches or a cane, and the engine does not read `parent_code`.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi; echo "BASE=$BASE"
git switch -c task/t-055-mobility-family-tooling "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-055" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The owner decomposed `MOB` by device. Wheelchair drive is already a typed descriptor (`device_class`), but the column cannot say "prosthesis", "crutches" or "cane", so a figure about those users would carry its device in prose or as an identity code (a second home, rule 5). And a determination at the parent `MOB` gathers only figures tagged `MOB`, so the family's commonality is lost.

**Evidence command** (read-only):

```
python3 -I -c "import sqlite3,re;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);s=c.execute(\"select sql from sqlite_master where name='source_value_extractions'\").fetchone()[0];print(re.search(r'device_class[^,]*CHECK \\(device_class IN \\([^)]*\\)',s).group(0))"
grep -c parent_code scripts/assess/assess_cell.py
```

**Expected output today:** the chair and walker values only; `0`. If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Schema migration: widen the `device_class` CHECK on `source_value_extractions` by exactly the values `T-102-design.md` section 4 names: `lower_limb_prosthesis`, `crutches`, `cane` (the design keeps no upper-limb prosthesis value). Carry over every other CHECK verbatim from `sqlite_master` at execution, including T-018's CHECK that holds the four retired lens columns NULL (a widening that copies rows unchanged needs no `AFTER_DATA` marker; T-018's marker already orders it after the data T-018 reshaped). Add `device_class` to `amend-extraction`'s amendable fields (`_AMENDABLE_SVE_FIELDS` in `scripts/db.py`), with the existing `--reason` requirement and the column's own CHECK as its vocabulary, so a figure's stated device can be recorded on an existing row (`T-102-design.md` section 9). SQLite cannot change a CHECK in place: create, copy, drop, rename, and recreate every view and index naming the table. Keep every existing value. Derive the migration number; prove it by rebuild and `migration_reproducibility.py --deep`. If the design asks for the vocabulary as a table rather than a CHECK (the owner's "no hard-coded behaviours"), stop and report: that is a larger change to propose, not to improvise.
2. The engine's gather (`scripts/assess/assess_cell.py`, the identity predicate T-019 left): a determination keyed on a code gathers figures with a live link (`v_live_lens_links`) to that code **or to any code whose `parent_code` chain reaches it**, by the recursive `family` CTE of `T-018-design.md` section 4 on `base_taxonomy_identity`, never a list. A child's determination gathers only the child. **A figure is gathered once** [2026-11-12, OI-13 fold]: the children are not mutually exclusive (a figure may carry `WHEEL` and `WALKAID` links), so the family predicate stays inside the per-figure `EXISTS`, never a join on the links, and no count downstream (governing figures, sources, convergence roots) multiplies by the number of links. Nothing else in the engine changes. (`SCI` is retired to `WHEEL` and `LMB` becomes `UPL`, outside the family, by T-102 and T-116; neither changes this task. The ninth set replaced the child `PROSTH` by `LLD`, people with lower-limb differences, defined by the condition: `lower_limb_prosthesis` stays a `device_class` value, a descriptor of the device a figure concerns, and is still added here; it is not a second home of `LLD`, `T-102-design.md` §0.)

**What reads what this task adds or changes:** `add-extraction`, `amend-extraction` (the `device_class` values); the engine; T-102; T-110.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` and, for anything added, what reads it.

## 5. Caller sweep

Names to sweep: `device_class`, `parent_code`, the identity predicate of the engine

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) and report its result. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written:** not recorded (this file was written in the last fold pass of 2026-11-12, without running the sweep). Run the two `git grep` lines above with `-l` before you change anything; every file they print is a hit to judge as a caller or a mention.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `schema_reference_audit`, `migration_reproducibility`, `test_db_integrity`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="schema_reference_audit migration_reproducibility test_db_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** Before: the evidence command prints no prosthesis value and `0`. After, on a scratch copy: `add-extraction` accepts each new `device_class` value and refuses an unknown one; with a child code seeded under a parent by the test on its own scratch copy (never in the canonical database), a determination at the parent gathers the child's figure and one at the child does not gather the parent's. Added (OI-13): a fixture figure linked to two children of one parent is gathered once by the parent's determination (its governing-figure count equals the number of distinct extraction ids), red if the predicate is written as a join. Red on the unchanged code; the stress harness of T-014 shows no other change.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T055-01`, `T055-02`, …) and confirm the prefix is free first (`grep -c '"T055-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: device values and a parent-gathering determination for the mobility family [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author `best_practice_synthesis` or any synthesis prose. A Sonnet-class model is below that floor.
- Do not treat any `[A-Z]-NN` code (old item codes met in `references/`, `working/`) as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, determinations) in a tooling pull request, or tooling in a research one (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller:** a test fixture, a comment, a skill sentence or a help string that the sweep of section 5 shows is made false or red by your change is in scope, is fixed in this pull request, and is listed there.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
