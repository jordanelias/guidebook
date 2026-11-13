# T-059  The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragility note)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-059 |
| Title | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragility note) |
| Wave | 1 (chain, after T-019) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Opus-class (**NOT FOR SONNET**: step 2 has an open design point, section 4 item 4) |
| Traces to | prior workplan T-4 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md`; the report's T-4 (`scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`, `grep -n '^### T-4 agreement' <that file>`); the owner's OR-4, OR-6 and OR-6b (`grep -n -E '^OR-4:' references/project-standards.md` and `grep -n -E '^OR-6b:' references/project-standards.md`) and OR-6c (tenth set, `grep -n -F 'OR-6c — how far' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-016 and T-019 merged (the prior workplan's reading step 1a and its lens step 3; this task lands after the lens step to keep one `RULE_VERSION` sequence). Check by running those tasks' own after-tests (their section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none in the register. The rulings this task rests on are in the ledger: OR-4 ("Yes, the most accommodating value wins"), OR-6 (stated and divergent, with a synthesis approach), OR-6b ("No, the spread is printed in the note") and OR-6c (tenth set, 2026-11-13). **Step 3 of the report (the Co-1 boundary) is not in this task**: OR-5b's test of soundness has three open edges (ledger, tenth set, "What it does not decide"), and no code is written on a guess (section 9). It becomes its own task when the owner has answered them.
- **Tests that must be red (or green) before you start:** the report's G1, G2, G3, G8, G12 and G13 assertions and its F-tests not yet passing (G4 is Co-1 and belongs to the held step) (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi; echo "BASE=$BASE"
git switch -c task/t-059-wp-t2-conditions "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-059" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The prior workplan's T-4 has no task of its own anywhere else: its three steps that the owner has ruled are exclusion causes that name the true reason, anchoring claims that cannot all hold recorded as `divergent`, and a note that says how many rows set the selected bound. Today an excluded value row carries one constant sentence whatever the cause, a divergence between anchoring tiers is not detected, and the note does not say how fragile the selected bound is.

The owner's rulings fix the behaviour: the most accommodating value wins whatever anchoring tier stated it (OR-4); anchoring claims that cannot all hold are recorded `divergent`, stay `stated`, and are not written without a synthesis approach (OR-6; evidence-methodology §3.3); floors that differ but can all be met are not divergent and the spread is printed in the note (OR-6b); and for claims that cannot all hold, the approach for a T1 figure against a T2 figure is the owner's own: the T1 figure is stated and the T2 dispute is noted in the item's discussion. The tenth set (2026-11-13) extends that to **any divergence between different tiers**, with **Co-1 and T1 counted as one rank**: so a divergence between ranks is resolved by the higher rank stating the value and the lower rank's dispute being noted, and a divergence between two sources of the same rank (Co-1 against T1 included) waits for a synthesis approach written by an Opus-class session.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
sed -n '/^### T-4 agreement/,/^### T-5/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md; sed -n '/\*\*T-4 Agreement/,/Code +85/p' workplan/2026-10-23-pipeline-resolution-workplan.md; grep -n -E 'def determine|def compose_value|def gather_extraction_links|def stale_determinations' scripts/assess/assess_cell.py
```

**Expected output today:** the report's T-4 section (steps 1 to 4) and the workplan's T-4 paragraph; four `def` lines, with `determine(conn, parameter_id, lens, slug, note)` taking no `synthesis_approach` parameter.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Execute steps **1, 2 and 4** of the report's T-4 (exclusion causes; divergence; the fragility note) as written in `workplan/2026-10-23-pipeline-resolution-workplan.md` and the report section it cites, with the report's G1, G2, G3, G8, G12 and G13 assertions, the F-tests (every governing value × 1.1 and × 0.9, each comparator flipped, expectations written beside each case; the factor lives only in the test, rule 7a) and the mutation tests it names for these steps (M13 to M16), **except for the points below**, where a later owner statement governs (CLAUDE.md rule 0).
2. **Step 3 (the Co-1 dimensional boundary) is not done here.** The report's step 3 removes every Co-1 row from the numeric bound; the owner's OR-5 ruling lets a Co-1 figure set a value insofar as its source is academically sound, so the step as written would erase what the ruling allows (CLAUDE.md §6: erasing the people who produced the work while claiming the tier is the worst failure available here). Leave `compose_value`'s treatment of Co-1 rows as it is, and say so in the pull request. Do not delete the sentence in `references/methodology-evidence-hierarchy-mapping.md` §6.4 either: that edit belongs with the step it describes.
3. **OR-6b = no, as written** (the spread of the passed-over bounds is printed in the note). **OR-4 = yes: no change** to the selection rule beyond the extension the report names.
4. **Step 2 has one open design point, which you settle first and record in the pull request body before you write code (this is why the task is not for Sonnet).** The report's step 2 refuses every divergence until `--synthesis-approach-file` supplies an approach written by an Opus-class session. The owner's rulings make the approach for a divergence between **different ranks** a rule, not a text: the higher rank states the value, the lower rank's dispute is noted. Decide, and record with your reasons, how that rule-supplied approach is held without writing a second home for a fact (rule 5): the options are (a) a typed approach kind on `convergence_assessment` (a value from a CHECK: `higher_rank_states` or `written`) with the written text only for `written`; (b) the existing `synthesis_approach` text holding the rule's name. A typed kind is preferred by the 2026-11-06 schema-shape statement (a prefix that says what the rest of a cell means is data joined in a cell); if you choose it, it is a schema migration and section 6 changes accordingly. The engine writes **no prose approach of its own** (the report's K-5): for same-rank divergences it refuses, as the report says. Rank is derived from the tier ladder with Co-1 and T1 equal (`governance/tier-system.md`; derive it, never list it: rule 8).
5. Code deleted or replaced: the report's step 2 retires the old "INCOHERENT INTERVAL … comparator" sentence for the multi-source case; the code-size line must show whatever else goes.

**What reads what this task adds or changes:** `determine`, `compose_value`, `gather_extraction_links`, `stale_determinations`, `main` in `scripts/assess/assess_cell.py`; render's note lines later (T-037).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `divergent`, `synthesis_approach`, `convergence_assessment`

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

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `divergent`, `synthesis_approach`, `convergence_assessment`: code and skills (re-derive; the Names line above, run with `-l`): `scripts/assess/assess_cell.py`, `scripts/audit/adjudication_integrity.py`. Prose: `governance/stage-map.yaml`, `governance/pipeline-operations.md`, `governance/owner-browser.yaml`.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_assess_cell_pilot`, `test_evidence_cell_state_2_3`, `test_validate_evidence_state_2_4`, `test_scan_contract`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_assess_cell_pilot test_evidence_cell_state_2_3 test_validate_evidence_state_2_4 test_scan_contract"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** The report's G1, G2, G3, G8, G12 and G13 assertions and the F-tests of its section 6.1, each run and shown; M13 to M16 each killed; `fixtures_g1_g13.py` output differs only where steps 1, 2 and 4 intend it; the stress harness diff shows only intended changes. A divergence across ranks (T1 against T2, Co-1 against T2) is stated at the higher rank and the dispute is noted; a divergence at one rank (T1 against T1, Co-1 against T1) is refused without an approach written by an Opus-class session.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T059-01`, `T059-02`, …) and confirm the prefix is free first (`grep -c '"T059-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: execute workplan T-4 agreement (steps 1, 2, 4) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- the Co-1 treatment in `compose_value` would have to change to make a test pass (that is the held step 3: stop, do not edit it);
- the typed approach kind of section 4 item 4 cannot be derived from the tier ladder without a list kept beside it (rule 8);

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
