# T-010  `add-parameter` refuses a term that is not a design quantity (first step)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted on 2026-11-12** by a Sonnet-class executor in a scratch clone, from an earlier version of this file: the change worked (red before, green after), and the sweep found two callers the file had not named, one of them a test that the change turned red. Report and patch: `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-010-report.md`, `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-010.patch` (a record, not a file to apply). The callers, the next action in the refusal, the test ids and the derived probes are corrected here. The amendable `domain` field (item 3) was added after the pilot and **has not been piloted**.

## 1. Identity

| | |
|---|---|
| Task | T-010 |
| Title | `add-parameter` refuses a term that is not a design quantity (first step) |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-42a in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** none. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** AT-77 (first half) red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-010-add-parameter-domain-refusal "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-010" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

Any term can be promoted to a parameter in one command. A functional axis and a legal concept were promoted in the stress runs; each became a "parameter" that every held source now owes a reading for, and that the engine will determine as a pending cell with a gap for any group named.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
TERM=$(python3 -I -c "import sqlite3,os;c=sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True);print(c.execute(\"select t.term_id from terms t where t.domain='functional_axis' and t.term_id not in (select term_id from base_parameters) and t.term_id not in (select term_id from parameter_declinations where revoked_at is null) and t.canonical_en not glob '*[0-9]*' order by t.term_id limit 1\").fetchone()[0])"); echo "probe term: $TERM"; GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py add-parameter --term-id "$TERM" --notes 'TASK-FIXTURE' --session session_task-probe; echo rc=$?; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select domain, count(*) from terms group by 1 order by 2 desc\").fetchall())"; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select distinct t.domain from base_parameters p join terms t using(term_id)\").fetchall())"; python3 scripts/db.py amend-term --help | grep -- '--field'
```

**This command calls a verb that writes.** It is safe only because `GUIDEBOOK_DB_PATH="$SCRATCH/…"` is set inline on that call, which points the verb at the copy. Keep it on every `db.py` call you derive from this one; a call without it addresses the canonical database.

**Expected output today:** The derived term (the first functional-axis term that is neither a parameter nor declined) is promoted, `rc=0`. The domains in use; no live parameter is filed under `functional_axis`, `population`, `medical`, `methodology`, `legal` or `economics`. `amend-term` offers `definition` and `scope_note` only: no verb can correct a term's domain.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. `scripts/dbcore.py`: one named rule, `NON_QUANTITY_DOMAINS`, a frozenset of the domains under which lenses, methods and bodies of law are filed: `functional_axis`, `population`, `medical`, `methodology`, `legal`, `economics`. Its comment says three things: that this is a judged rule declared once (the owner's tenth statement of 2026-11-12 allows a rule held in one stated place; `grep -n -F "isn't hardcoding necessarily" references/project-standards.md`); the two queries that justify it and the date they were run (the evidence command's second and third); and that it stays when T-020 gives each parameter a quantity kind (the domain is a fact of the term, the kind a fact of the parameter; folded T-020, section 4 item 2; corrected 2026-11-13, when this file still said T-020 would delete it). Nothing else in the tree types those domain names for this purpose.
2. `scripts/db.py`, `insert_parameter` (`grep -n 'def insert_parameter' scripts/db.py`): read the term's `domain` with the term, and refuse when it is in the rule, before the declination test. Do not alter the text of the refusals already in the function: `workplan/pipeline-state-graph/machines.yaml` matches on three of them. The new message states the domain, prints the domains of the live parameters and the refused set (both read, not typed), says nothing was written, and **names the next action for both cases**: if the term is a lens, a method or a body of law, dispose of it truthfully with `db.py decline-parameter --term-id <id> --reason '<why it is not a design quantity>'`; if it is a quantity filed under the wrong domain, correct the domain with `db.py amend-term --term-id <id> --field domain --replacement <domain> --reason '<why>'` and promote it again. Update the `--term-id` help text of `add-parameter` to name the new refusal.
3. `scripts/db.py`, `_AMENDABLE_TERM_FIELDS` (`grep -n '_AMENDABLE_TERM_FIELDS' scripts/db.py`): add `domain`, so that the second next action exists. `terms.domain` has no CHECK, so there is no vocabulary to read: the guard is that the replacement is a domain at least one other term already carries (`select 1 from terms where domain=?`), and the refusal for anything else lists those domains by query. `amend-term` already demands and records `--reason`. Without this field the refusal of item 2 would send a mis-filed quantity nowhere, which is a dead end (REQ-103).
4. This needs no new vocabulary. The quantity kind (a parameter states its kind) is T-020's, which keeps this refusal beside it; do not build it here. A term with no domain is not refused.

**What reads what this task adds or changes:** `NON_QUANTITY_DOMAINS`: `insert_parameter`, the fixture filter in `scripts/tests/test_scan_contract.py`, the new tests; T-020 keeps it (its section 4 item 2) and its free-term probes read it. The amendable `domain` field: `amend-term`; through it `add-parameter`.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `insert_parameter`, `add-parameter`, `_AMENDABLE_TERM_FIELDS`, `amend-term`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `insert_parameter`: code and skills: `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_scan_contract.py`. Prose: `workplan/pipeline-state-graph/machines.yaml`.
- `add-parameter`: code and skills: `.claude/settings.json`, `scripts/assess/assess_cell.py`, `scripts/audit/research_batch_dod.py`, `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_scan_contract.py`, `scripts/validate_parameters.py`, `skills/run-pipeline_SKILL.md`. Prose: `CLAUDE.md`, `architecture/conformance-schema-findings.md`, `architecture/meta-scripts-spec.md`, `governance/research-contract.yaml`, `governance/stage-map.yaml`, `workplan/pipeline-state-graph/machines.yaml`.
- `_AMENDABLE_TERM_FIELDS`: code and skills: `scripts/db.py`. Prose: none.
- `amend-term`: code and skills: `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`. Prose: none.

**Callers already known** (found by this file's author or by a pilot; each is in scope):
- `scripts/tests/test_scan_contract.py` builds a list of free terms in id order (`grep -n 'FREE = ' scripts/tests/test_scan_contract.py`) and promotes one of them in case V03. In the pilot the one it picked was a methodology term, so **V03 turned red because of this change**. Fix the fixture: the free-term query also leaves out terms whose domain is in `dbcore.NON_QUANTITY_DOMAINS` (read the rule; do not retype it). After: the file fails only the cases it failed in the before-run.
- `scripts/audit/research_batch_dod.py` has a comment that says `add-parameter` has one exception to its promote-or-decline rule (`grep -n 'ONE EXCEPTION' scripts/audit/research_batch_dod.py`). Add the second: a term in a refused domain is disposed of by `decline-parameter`.
- `scripts/tests/test_db_amend_writers.py` calls `insert_parameter` and tests `amend-term`; it must pass before and after, and gains nothing unless it asserts the exact list of amendable fields (if it does, that assertion is a caller: update it).
- `skills/run-pipeline_SKILL.md` and `.claude/settings.json` mention the verb and state nothing about what it refuses: mentions. `workplan/pipeline-state-graph/machines.yaml`: its needles on `insert_parameter`'s existing refusals must still match (`python3 workplan/pipeline-state-graph/build_graph.py --check`).

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_scan_contract`, `test_db_amend_writers`, `research_dod_selftest`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_scan_contract test_db_amend_writers research_dod_selftest test_author_presence test_search_log_completeness test_assess_cell_pilot"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** Add a section to `scripts/tests/test_run_pipeline_refusals.py` next to the other `add-parameter` cases. Every probe is derived: for a refused domain, the first term of that domain that is not a parameter, not declined and carries no digit in its name; for the legitimate case, the same query on a domain that a live parameter has. Cases: the rule exists and each of its members is a domain some term carries (a member no term carries is stale); a functional-axis term and a legal term are refused, and the message names the domain, `decline-parameter` and `amend-term`; a term of a live parameter's domain is still promoted (dry run); no live parameter sits in a refused domain; `amend-term --field domain` to a domain no term carries is refused and lists the domains; to a domain another term carries it is accepted (dry run). Before: the first case is red (the rule is absent) and the rest are gated on it by the file's `feature(...)` probe. After: all green. Show that the refusal cases can fail: disable the refusal, see them red, restore it. At the command line on `$SCRATCH/t.db`: the evidence command now ends `REFUSING: …` and `rc=1` for the derived functional-axis term; the same for a derived legal term; a derived term of a live parameter's domain is promoted.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T010-01`, `T010-02`, …) and confirm the prefix is free first (`grep -c '"T010-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: refuse promoting lens, method and legal terms to parameters [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row (`specifications`, read through `v_best_practice`; CLAUDE.md §6's `best_practice_synthesis` names a table not in the schema: superseded in part by TERM-RESOLUTION-PLAN §2, 2026-11-14) or any synthesis prose. A Sonnet-class model is below that floor.
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
- A live parameter has one of the refused domains (the evidence query shows it): stop; the rule would orphan a real parameter.
- You are tempted to refuse an element such as a grab bar (filed under a room domain): that needs the quantity kind of T-020; leave it.
- A test asserts the exact text of an existing refusal in `insert_parameter` and you would have to change that text.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
