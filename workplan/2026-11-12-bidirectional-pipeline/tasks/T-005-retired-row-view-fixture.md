# T-005  A seeded test that a retired determination is surfaced by no determination view

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

## 1. Identity

| | |
|---|---|
| Task | T-005 |
| Title | A seeded test that a retired determination is surfaced by no determination view |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-10 (second fixture) in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **Tasks that must be merged to `main` first:** none. Check with `git log origin/main --oneline | grep -i -E "<the commit subject of that task>"`, or by running that task's own after-test.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** AT-55 (second half): no such test exists (`grep -rn "v_best_practice" scripts/tests` returns a fixture stub only). (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin main && git switch -c task/t-005-retired-row-view-fixture origin/main  # never commit on main
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-005" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
Shell variables do not survive from one tool call to the next in this harness. Begin every later command block with the same `export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-005"` line (the path is fixed, so repeating it is safe), and pass `GUIDEBOOK_DB_PATH` inline on each call as shown. Open the session with `/session-open` before the first command, so the command log lands in this task's own folder (CLAUDE.md §7).

## 3. The problem, in the guidebook's terms

The owner ruled retire-in-place on the condition that every reader filters retired rows. No test would notice a view that started to show a retired determination, and a retired value would then reach a page.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
grep -rn -E 'v_best_practice|v_pending|v_determination_provenance' scripts/tests | cut -c1-120; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(v,'retired_at' in c.execute('select sql from sqlite_master where name=?',(v,)).fetchone()[0]) for v in ('v_best_practice','v_determination_provenance','v_item_provenance','v_pending','v_divergence','v_code_floor_only')])"
```

**Expected output today:** One stub line in a test file; every view names `retired_at` (True).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Add a test to `scripts/tests/test_assess_cell_pilot.py` (reuse its fixture builders; do not add a file unless that one cannot hold it): build a determination, assert the six determination views return it where they should, retire it with `UPDATE specifications SET retired_at=…` on the fixture connection, assert each view returns no row for it.
2. Print `EXAMINED: <number of view assertions>` only if the file's existing convention does; otherwise follow the file.

**What reads what this task adds or changes:** The `tests` battery (`test_assess_cell_pilot` is registered).

**Code size.** Report in the pull request the output of `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`, and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Run each for every name listed, and record the output in the pull request description. A view is a caller; so is a skill; so is the check registry; so is prose (CLAUDE.md rule 4).

Names: `v_best_practice`, `v_pending`, `v_divergence`, `v_code_floor_only`, `v_item_provenance`, `v_determination_provenance`

```
N='<name>'
git grep -n -e "$N" -- . ':(exclude)transcripts' ':(exclude)scratchpad'          # the tree; git grep sees the paths .ignore hides
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
git grep -n -e "$N" -- skills .claude                                              # skills, agents, commands, hooks
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -e "$N" -- governance references architecture CLAUDE.md workplan        # prose that restates it
```
A hit in a view, a skill, the registry or prose is fixed in this same pull request, or the task stops and reports it. An object that returns 0 rows is unproven, not clean.

## 6. Verification

**Red before, green after.** This test is green on `main` (the views filter). Its redness is shown by mutation, once, and not committed: in a scratch copy of the database recreate one view without its `retired_at` filter and show the new assertion fails; record the output in the pull request. After: `python3 scripts/tests/test_assess_cell_pilot.py` prints its PASS line.

**Fixtures.** Anything a test or probe writes goes to a copy (`$SCRATCH`), is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`. A new test must be able to fail: show it red on the unchanged code (or on a seeded defect) before you show it green.

**The gate, once, when the diff is ready:**

```
scripts/preflight.sh                                                   # once, when the diff is ready
python3 scripts/run_checks.py --changed-from origin/main --explain     # once; never --all
python3 scripts/run_checks.py --selftest                               # after any rename, new check or registry edit
```
**Proof that each gate examined something.** In the `--explain` output find every check this task touches and read its `EXAMINED: <n>` line. A check listed under `NOTHING-IN-SCOPE`, or printing `EXAMINED: 0`, has not passed: say so in the pull request and treat it as not verified. A check that is red on untouched `origin/main` tells you nothing about your diff; name it and move on (the standing advisory failures on `main` are listed in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-stress-audit.md` row B-82).

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: add seeded test that determination views hide retired rows [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the sweep result>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- Do not hand-type a count into any file or message; write the command that computes it.
- Do not add a table, column, check, verb or script that this file does not name. If one seems needed, stop and report.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the caller sweep finds a caller this file does not mention;
- a blocking check goes red that was green on `origin/main`;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- The fixture builders cannot create the views (they use a reduced schema): report it; do not copy the schema into the test.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, when the diff-scoped gate is clean. Title = the commit subject. Body: the problem, the evidence before and after, the sweep output, the checks with their `EXAMINED:` lines, what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge origin/main` (never rebase) and, if you carry a schema migration, renumber it by the rule above.
