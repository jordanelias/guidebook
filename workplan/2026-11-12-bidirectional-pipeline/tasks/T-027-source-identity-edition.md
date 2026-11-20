# T-027  The source's own title, edition and currency can be written

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-027 |
| Title | The source's own title, edition and currency can be written |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) _[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19): now with one schema migration, an `evidence_sources` rebuild (section 12.3).]_ |
| Executor | Sonnet-class _[Amended 2026-11-19, because it is now false: NOT FOR SONNET: Opus-class. The task writes the shape of a judged bibliographic warrant and the refusals that keep it from being a substring match; the first attempt (`c9c84466`, reverted by `d6c19cbd`) fabricated editions for want of exactly that.]_ |
| Traces to | IMP-25 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md`; _added 2026-11-19:_ `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md` section 3 items 30, 76 and 77, section 4 item 7; CLAUDE.md §5(c) ("Never write a bibliographic field from memory when a payload is in hand") and rule 8 ("demanding the evidence for it, and recording the answer and its warrant in named columns"); the T-027 sections of `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` and `scratchpad/session_2026-11-15-remediation-stack/sweep-list.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** none. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`. _[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19, ACTION (2), "in its order"): T-139 (the amendment record) first, so that replacing a stated edition or original title writes its typed amendment row, and T-135 before it by the same order. Check by T-139's after-test `T139-01`.]_
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all. _[Amended 2026-11-19: it now rests on adjudication items 30 and 76, which carry no OD number and are ratified by reference in the ledger entry "Owner ratification 2026-11-19"; section 12.1 says how to check that they still stand.]_
- **Tests that must be red (or green) before you start:** AT-03 red. _[Amended 2026-11-19: `T027-10` to `T027-13` of section 12.4 red.]_ (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-027-source-identity-edition "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-027" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

A non-English source's original title, a standard's edition and whether it is still in force have columns and no writer. A superseded edition can be cited as current.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select sum(original_title is not null), sum(edition is not null), sum(code_currency_status is not null) from evidence_sources\").fetchall())"
```

**Expected output today:** All three are 0 or NULL. _[Re-run 2026-11-19 read-only: `[(0, 0, 0)]`. Still true, but section 3's premise is only partly stale: `code_currency_status` and `code_currency_notes` are writable by `amend-source` (first stack), and `original_title` by `correct-source` for a source with a DOI; `edition` and a DOI-less source's `original_title` have no writer. Section 12.2 gives the commands.]_

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. `amend-source` / `correct-source`: accept the existing columns `original_title`, `edition`, `code_currency_status` and its three companions, with the provenance rule the verb already applies to its other fields. `v_evidence_authors`: show the full given name where the name has no initials convention (a schema migration recreating the view).

_[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19). Item 1 is false in three places and is NOT to be executed: (a) "the provenance rule the verb already applies" is what the reverted `c9c84466` applied (a quote found anywhere in a saved file, the value any substring of it), which wrote another standard's edition, a page marker and `5 edition` from "2015 edition"; the rule that governs is the judged, warranted value of section 12.3 (adjudication item 30). (b) `code_currency_status` is already writable; what remains is a CHECK in the same rebuild (item 76). (c) The `v_evidence_authors` part is resolved by adjudication item 77 (no initials flag; the given name shown as stored, held to the logged payload by `--verify-authors`; a view edit only) and is executed by T-141 item 77, not here; it is no longer a GAP of this task.]_

**What reads what this task adds or changes:** A future evidence list; `jurisdiction-tracker`.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `original_title`, `code_currency_status`, `v_evidence_authors`

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

- `original_title`: code and skills: `scripts/research/retrieval_log.py`. Prose: `references/audits/evidence-sources-schema-redesign-methodology.md`, `references/audits/migration-review-2026-05-11.csv`.
- `code_currency_status`: code and skills: none. Prose: `governance/tier-system.md`.
- `v_evidence_authors`: code and skills: `schemas/evidence_source.py`, `scripts/audit/citation_mining_completeness.py`, `scripts/audit/source_slug_links_duplicates.py`, `scripts/audit_evidence_metadata.py`, `scripts/db.py`, `scripts/tests/test_db_integrity.py`, `skills/bibliography-compiler_SKILL.md`, `skills/citation-miner_SKILL.md`, `skills/evidence-metadata-rehabilitation_SKILL.md`. Prose: `architecture/meta-scripts-spec.md`, `governance/context-map.yaml`.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** On a scratch copy the fields can be set through the verb and are refused without their warrant. _[Amended 2026-11-19: replaced by section 12.4's named cases; the before-run list of step 1 gains `test_db_integrity metadata_integrity_audit emit_batch_sql_selftest column_vocabulary_audit derived_not_curated_audit migration_reproducibility schema_reference_audit context_map_fresh`.]_

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T027-01`, `T027-02`, …) and confirm the prefix is free first (`grep -c '"T027-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
- **`research_tooling_separation` reads `origin/main`, not `$BASE`, until T-075 (`@BASE@`) is merged** (the registered `cmd` then takes `--base`, and CI still reads `origin/main` until its classify job hands the base on), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: let source identity, edition and currency be written [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.

## 12. Amended 2026-11-19 (ledger: Owner ratification 2026-11-19) — what now governs

_Written 2026-11-19 by an Opus-class task author on the owner's instruction "Author the tooling tasks in order" (the ratified adjudication `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, section 4 item 7; section 3 items 30, 76, 77 and 88). Every figure was read on 2026-11-19 read-only and is given with its command: re-run it. Where this section and sections 1 to 11 disagree, this section governs; where it is silent, sections 5, 7, 8, 10 and 11 stand, and section 6 steps 1, 3 and 4 stand with the check list amended there._

### 12.1 What happened, the gate and the set-up

**The first attempt and why it was reverted.** `c9c84466` let `amend-source --field edition` write a DOI-less source's edition when `--replacement` occurred inside an `--edition-quote` found in a file saved for that source; `d6c19cbd` reverted it after the critic wrote, through it: `2003 Edition` onto the 2010 ADA Standards from its referenced-standards list; a one-character value from a one-character quote; punctuation-only values (they normalise to empty, and empty is in everything); `5 edition` from "2015 edition"; an amendment year; a page-marker number; a semicolon list stored as typed; a first statement ledgered as CORRECTED (`git show c9c84466 d6c19cbd`; the T-027 section of the 2026-11-18 sweep list). Every one is a machine-only rule standing in for a judgment (adjudication item 30).

**The gate.** Items 30, 76 and 77 carry no OD number; they are ratified by reference in "Owner ratification 2026-11-19" ("the design questions numbered 12 to 91 that carry no OD number are ratified by reference"; its ACTION (3) keeps the breadth of "all" an [ASSUMPTION] until the owner confirms it). Check the entry stands, and stop if a later ledger line withdraws its CHECK lines or names item 30 or 76:
```
grep -c -F "## Owner ratification 2026-11-19" references/project-standards.md      # printed 1 on 2026-11-19
awk '/^## Owner ratification 2026-11-19/{f=1} f' references/project-standards.md | grep -n -i "withdraw" | head   # printed nothing on 2026-11-19
```
No OD gate applies (no register decision is rested on). **Order:** seventh of section 4, after T-139.

**Set-up (the stacked-branch convention of `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1, or the brief the coordinator names).** Stay on the given branch; no `git switch -c`; no `/session-open`; diffs and the gate use `$BASE_PRE`:
```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin; BASE_PRE=$(git rev-parse HEAD); echo "BASE_PRE=$BASE_PRE"
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-027" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
Probes and fixtures: `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline, `--session session_task-probe`; a test that needs a saved file builds its own retrieval-log fixture under a temporary `GUIDEBOOK_RETRIEVAL_LOG` (`TASK-FIXTURE`), never under `retrieval-log/`.

### 12.2 The problem, re-measured (read-only)

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select sum(doi is null), count(*), sum(edition is not null), sum(original_title is not null), sum(code_currency_status is not null) from evidence_sources').fetchone())"
python3 -I -c "import sys;sys.path.insert(0,'scripts');import dbcore;print(dbcore.code_currency_vocabulary())"
grep -n -F 'code_currency_status' governance/tier-system.md | head -2
```
Printed 2026-11-19: `(39, 59, 0, 0, 0)` (39 of 59 sources have no DOI, so `correct-source` can never reach them; nothing is stated yet); the four values parsed from the governance sentence; the sentence at line 57. `code_currency_status` carries no CHECK (`dbcore.check_values` returns an empty set for it), so a reworded sentence makes every currency write refuse and the T027-03 case skip (S15 sweep list, T-027 item (f)). If any figure differs, stop.

### 12.3 The change (replaces section 4 item 1)

1. **One schema migration rebuilds `evidence_sources`** (create, copy, drop, rename; `PRAGMA foreign_keys=OFF`, `foreign_key_check` empty after; recreate every index and view that names it: `select type, name from sqlite_master where sql like '%evidence_sources%'`; the tables that hold a foreign key into it, seventeen on 2026-11-19: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(sorted({t for (t,) in c.execute(\"select name from sqlite_master where type='table'\") for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if f[2]=='evidence_sources'}))"`; T-136 may have removed `base_parameters` from that list). Every existing row and column is copied unchanged. The rebuild adds:
   - **(item 76)** `CHECK (code_currency_status IS NULL OR code_currency_status IN (…))`, the members copied ONCE into the migration from `dbcore.code_currency_vocabulary()` as it reads at execution (the ratified sentence of `governance/tier-system.md`); the migration is then the machine's one home. `dbcore.code_currency_vocabulary` becomes a reader of the CHECK (`dbcore.check_values(conn, 'evidence_sources', 'code_currency_status')`), taking a connection; its callers pass one. The governance sentence is ratified doctrine and stays as written (it is not a second machine home; no parity check is added: rule 5).
   - **(item 30) a warrant column set per field, for `edition` and for `original_title`** (F below): `F_words` (the source's own words that state the value, verbatim), `F_part` with `CHECK (F_part IN ('front_matter', 'imprint'))` (where in the document the words stand: its title page or front matter, or its imprint or colophon), `F_page` (the page or place in the file), `F_file_sha256` (the `sha256` of the retrieval-log manifest line of the file the words were read in; CHECK: 64 lower-case hex), `F_judge`, `F_reason`, `F_judged_at`, `F_judged_by_session`. CHECKs: the eight are all set (each non-blank) or all NULL; when they are set, F is set; and `F IS NULL OR F_words IS NOT NULL OR doi IS NOT NULL` (a DOI-less source's value always carries its warrant; a DOI source's value from `correct-source` is warranted by its logged payload, as today).
2. **One verb, `db.py record-source-identity --ref-id R --field edition|original_title --value V --words W --part front_matter|imprint --page P --file-sha256 S --judge NAME --reason TXT --session S [--dry-run]`.** `--field`'s choices are DERIVED from the schema (the fields that carry a `_words` column), `--part`'s from the CHECK. It refuses, each refusal naming the next action and saying `Nothing was written.`:
   - an unknown source; a blank session, judge, page or reason, or a reason with no letter;
   - a source with a DOI whose logged payload states the field (names `correct-source --field F`); a DOI source with no logged payload (names re-retrieval, R10: the payload is the stronger warrant); a DOI source whose payload states nothing for the field is accepted (no dead end);
   - `--file-sha256` that is not the `sha256` of a manifest line whose `ref_id` is this source (`retrieval_log` reads the manifests; one helper, no second parser), or whose saved file (or a file whose `derived_from` names that line) is not on disk (names re-retrieval);
   - `--words` not found, under `retrieval_log.normalise_quote`, in that file (not merely in any file saved for the source: the reverted attempt's scope);
   - a `--value` that normalises to empty (`normalise_quote` yields nothing: punctuation, dashes, spaces);
   - a `--value` whose normalised tokens are not a contiguous run of WHOLE tokens of the normalised `--words` (`5 edition` from `2015 edition` is refused; `2015 edition` is not); no length threshold is added (adjudication item 30: the whole-token and non-empty tests do the work);
   - a `--value` that does not occur in `--words` as written, whitespace collapsed: the stored value is the source's own spelling, never the operator's;
   - a value equal to the stored one with the same warrant (no-op, `changed: false`).
   On success it writes F and its eight warrant cells in one UPDATE. A first statement (F was NULL) is recorded by those cells alone; a replacement of a stated F writes one row of T-139's amendment record (`was`, `now`, `reason`) for F, and none for the warrant cells, which are the record of the new judgment. It writes nothing to `metadata_integrity_detail` and does not move `metadata_integrity_status` (a first statement is not a correction).
3. **`amend-source` is not widened.** `edition` and `original_title` stay out of `_AMENDABLE`, which stays disjoint from `_CORRECTABLE` (`test_db_integrity` M03); `amend-source --field edition` keeps refusing, and its message now names `record-source-identity` for a DOI-less source.
4. **What the machine cannot check, stated.** Whether the words are the source's OWN statement of its edition (and not a cited standard's edition in a referenced-standards list) is the judge's: it is recorded in `F_part`, `F_page`, `F_judge` and `F_reason`, contestable, and read by the adversarial pass. No rule pretends to decide it (rule 8: "the script asks for it … and records the answer and its warrant in named columns").
5. **Not here:** the `v_evidence_authors` given name (adjudication item 77, a view edit) is T-141 item 77.

**What reads what this task adds:** `bibliography-compiler` (`skills/bibliography-compiler_SKILL.md`) and `citation-miner` read `evidence_sources` bibliographic columns (an edition and an original title reach the reference list); `retrieval_log.py --verify-authors` reads `original_title` among `_TITLE_COLS`; `jurisdiction-tracker` and `amend-source` read `code_currency_status` through the CHECK; `metadata_integrity_audit.py` reads the source row. The warrant cells are read by the adversarial pass and by `record-source-identity` itself (its no-op test). **What wrong thing reaches the guidebook without it:** a standard cited under an edition it does not state, or a non-English source with no title of its own; with the reverted rule, an edition the source never stated. **Code it makes deletable:** the parse of `governance/tier-system.md` in `dbcore.code_currency_vocabulary`.

### 12.4 Verification

The before-run (section 6 step 1, list amended). New cases in `scripts/tests/test_run_pipeline_refusals.py` (where T027-01 to T027-07 live; `T027-08` and `T027-09` were taken by the reverted commit and are not reused), on a scratch copy and a temporary retrieval log built by the test, every probe source chosen by query (a DOI-less source; for 12.3 item 2's payload refusal a DOI source whose logged payload states `original-title`, derived by reading the manifests). Confirm the free ids first (`git grep -n '"T027-1' -- scripts/tests` prints nothing; printed nothing on 2026-11-19). Each case red on the unchanged code or on a named seeded defect, then restored (`cmp`):

- `T027-10` a DOI-less source's edition is written with its full warrant; the stored value is the run as the words spell it; no amendment row and no `metadata_integrity_detail` change on a first statement. Red before (no verb).
- `T027-11` the whole-token rule: `5 edition` from words `2015 edition` refused; `2015 edition` from the same words accepted; a value inside a longer token refused. Seeded defect: replace the token test by `phrase_in_quote` and the first probe passes.
- `T027-12` a value that normalises to empty (derived: a string of the punctuation `normalise_quote` drops) refused; blank words, judge, page refused; a letterless reason refused. One sub-case per refusal, each red when its line is removed.
- `T027-13` the file: a `--file-sha256` of another source's manifest line refused; words present in another file saved for THIS source but not in the named file refused; a manifest line whose file is absent refused.
- `T027-14` a DOI source whose payload states the field refused naming `correct-source`; a DOI source whose payload states nothing accepted.
- `T027-15` replacing a stated edition writes one T-139 amendment row (`was`, `now`, `reason`) and replaces the eight warrant cells; the same value and warrant again is `changed: false`.
- `T027-16` the schema: on the copy, a raw UPDATE setting `edition` on a DOI-less source with no warrant raises; a warrant set partly raises; `F_part` outside its CHECK raises; a `code_currency_status` outside the CHECK raises.
- `T027-17` the currency vocabulary is the CHECK's: `dbcore.code_currency_vocabulary(conn)` equals `dbcore.check_values(...)`; with `governance/tier-system.md` read from a temporary copy whose enum sentence is reworded, `amend-source --field code_currency_status` still accepts a member. Red before (the parse fails closed and refuses).
- `T027-18` the rebuild loses nothing: every row of `evidence_sources` (each pre-existing column) and of the seventeen referencing tables is identical before and after on the copy; every recreated view's `sql` is identical to its pre-migration text.
- Rewrite `T027-03` and `T027-05` only where they read the governance sentence or assert `edition` is payload-only; say so in the pull request. `T027-06` stays.

Also, before and after: `joined_cells_census.py` (no new candidate), `migrate_db.py --rebuild` (exit 0), `migration_reproducibility.py --deep` (PASS), `build_graph.py --check` (no failure line added).

**Caller sweep (section 5, names widened):** `original_title`, `edition`, `code_currency_status`, `code_currency_vocabulary`, `_CORRECTABLE`, `PAYLOAD_FIELDS`, `edition-quote`, `record-source-identity`. Known on 2026-11-19 (section 5's commands): `scripts/db.py`, `scripts/dbcore.py`, `scripts/research/retrieval_log.py`, `scripts/tests/test_run_pipeline_refusals.py`; prose `governance/tier-system.md` (the enum sentence: a mention once the CHECK holds the same members; it states doctrine, not a mechanism) and two frozen `references/audits/` files (mentions). Every view and index of `evidence_sources` is a caller of the rebuild. `skills/bibliography-compiler_SKILL.md` and `skills/jurisdiction-tracker_SKILL.md`: read for a sentence describing how an edition or currency is written; correct one that the change makes false.

### 12.5 What you must NOT do (in addition to section 8)

- Do not accept a value the words do not hold as a whole-token run, and do not add a length threshold, a list of edition words, or any rule that claims to recognise a front matter mechanically.
- Do not backfill an edition or an original title for any source (research, rule 10), and do not change the `v_evidence_authors` view (T-141 item 77).
- Do not edit `governance/tier-system.md`.

### 12.6 Stop conditions (in addition to section 9)

- 12.2 prints other figures, or the governance sentence yields a set other than the one the migration would copy;
- a live `code_currency_status` value lies outside the vocabulary (none today: all NULL);
- T-139 is not on HEAD (its amendment record is what a replacement writes);
- a referencing table or view cannot be recreated identically by the rebuild;
- the ratification entry is withdrawn as to item 30 or 76.

### 12.7 Corrections 2026-11-19, after the adversarial review of this amendment (the lines above stay as written; where they disagree, these govern)

**Correction 1 (12.3 item 2, the location and the run; HIGH).** The whole-token test as written cannot be built and does not close the counterexamples: `retrieval_log.normalise_quote('2015 edition')` returns `'2015edition'` (no tokens), and `python3 -I -c "import sys;sys.path.insert(0,'scripts/research');import retrieval_log as R;print(R.phrase_in_quote('5 edition','2015 edition'))"` printed `True` on 2026-11-19, so `--words '5 edition'` would be "found" in a file saying "2015 edition". Replace both tests by ONE boundary rule, one helper in `scripts/research/retrieval_log.py` beside `normalise_quote` (the one home for "a run found at boundaries"), applied twice: the value in the words, and the words in the file.
- **The texts compared.** Each is NFKC-normalised, case-folded and whitespace-collapsed, never made spaceless. The file's text is the saved artefact's text with every `retrieval_log.PAGE_MARKER` line removed and the page of each remaining line recorded from those markers.
- **The boundary, derived from the Unicode database, the same for every script.** A run of `t` is at boundaries when each of its two ends is the start or end of `t` or touches a character whose `unicodedata.category` begins `Z` (space), `P` (punctuation, brackets included) or `S` (symbol), or is `Cc`. No language or script list is typed; no word segmenter is used (adjudication item 58 declined one).
- **What that gives, by script.** Latin and other spaced scripts (Cyrillic, Greek): `5 edition` is not at boundaries in `2015 edition`; `2015 edition` is. Korean, written with spaces: `제3판` is at boundaries in `제3판 발행`, not in `제3판의` (a particle attached: refused, residual). **Scripts written without spaces (Japanese, Chinese; also Thai, Lao, Khmer, Myanmar): a value must be a whole punctuation- or bracket-delimited segment.** For REF-00990's title (`select pub_title from evidence_sources where ref_id='REF-00990'`), `平成十八年政令第三百七十九号` (the bracketed segment) is at boundaries and `十八年…` cut from `平成十八年…` is not. **OPEN POINT and stop condition:** a value shorter than a punctuation-delimited segment in a script written without spaces (an edition such as `第3版` inside `改訂第3版発行`) cannot be recorded by this rule; segmenting it would invent a rule (a dictionary or a script-change heuristic). The executor builds the conservative rule, and reports each such value met as refused, for the owner or coordinator to rule. T-136's containment helper (`grep -n -i "Containment, one helper" workplan/2026-11-12-bidirectional-pipeline/tasks/T-136-base-grounding-absorbed.md`) answers a different question (does a quote CONTAIN a form, substring for wide scripts) and is not reused for a boundary: say so in the docstring of both.
- **Further refusals, each derived:** a value or words matching `PAGE_MARKER` (a page marker is the retrieval log's, not the source's); a value holding a character whose `unicodedata.name` contains `SEMICOLON`, or of category `Zl`, `Zp` or `Cc` (two values in one cell); a value that is the whole of the words (**the author's reading, for confirmation:** the words state the value, so they hold at least one boundary-delimited segment besides it; this refuses a one-character quote with a one-character value and adds no length threshold).
- **The locator, stated and tested.** When the file carries page markers, the words must be found on the page `F_page` names (refused otherwise, naming the page they are on); when it carries none, `F_page` is recorded as stated and the refusal says the page could not be checked. Whether that page is the source's front matter or imprint, rather than a referenced-standards list, stays the judge's (`F_part`, `F_judge`, `F_reason`): the machine cannot read a page's role, and no rule pretends to.

**Correction 2 (12.4, the tests named for every counterexample of the first critic).** Each on a temporary retrieval log, each red on its seeded defect:
- `T027-20` another standard's edition from a referenced-standards list: the words sit on a page other than the stated `F_page`: refused; stated at their true page with `F_part` `front_matter`, accepted and the record shows the page and the part (the residual, recorded for the adversarial pass; seeded defect: drop the page check).
- `T027-21` a one-character quote and value: refused (the words are the value alone).
- `T027-22` a punctuation-only value: refused (empty once `P`, `S`, `Z` are set aside).
- `T027-23` `5 edition`: refused as a value of words `2015 edition`, and refused as words located in a file saying `2015 edition` (seeded defect: restore `phrase_in_quote`, and both pass).
- `T027-24` the amendment year: a year that is a whole segment of the words passes the machine; the case asserts the judge, part and page are required and stored (the residual is the judge's; seeded defect: make `--judge` optional).
- `T027-25` a page marker: value `27` with words `[PDF page 27 of 79]` refused; a page-marker number cannot be located in the file (markers are removed).
- `T027-26` a semicolon list: `2010; 2015` refused.
- `T027-27` scripts: Latin (above); Japanese (REF-00990's bracketed segment accepted, `十八年` refused); Korean (`제3판` accepted from `제3판 발행`, refused from `제3판의`); a spaced non-Latin script (Russian `3-е издание`: `издание` accepted, `здание` refused).

**Correction 3 (12.3, `correct-source` and the warrant cells).** A payload write by `correct-source` to `edition` or `original_title` clears that field's eight warrant cells in the same UPDATE (the payload is then the warrant) and writes T-139's amendment row (with its `--judge`); otherwise `original_title_words` would describe a value no longer stored, and the CHECK would pass. `T027-28`: a judged value replaced by `correct-source` leaves the cells NULL (seeded defect: skip the clearing, and the case fails).

**Correction 4 (T-139's coverage).** `record-source-identity` calls `dbcore.record_amendment` when it replaces a stated value and writes nothing to `row_amendments` for a first statement; it is a covered verb, not an entry of `_AMENDMENT_EXEMPT`.

**Correction 5 (rule 7a).** "seventeen referencing tables" in 12.3 item 1 and `T027-18` is a typed count that T-136 (ordered earlier, it drops `base_parameters.direction_ref_id`'s key) makes stale: `T027-18` compares the tables the command of 12.3 item 1 lists at execution, never a number.
