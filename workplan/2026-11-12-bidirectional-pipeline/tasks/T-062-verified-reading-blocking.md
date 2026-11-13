# T-062  A `verified` figure with no full reading is refused at rest, not only at write (the prior workplan's T-1b step 10, finished)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, OI-52). Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-062 |
| Title | A `verified` figure with no full reading is refused at rest, not only at write (the prior workplan's T-1b step 10, finished) |
| Wave | 5 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | prior workplan T-1b step 10 (`grep -n -F '**T-1b Optional reading steps**' workplan/2026-10-23-pipeline-resolution-workplan.md`) and D-3's "re-grades `verified` only on a full scan if OR-11a"; OI-52; the owner's OR-11a (`grep -n -F 'OR-11a: "Yes, require a full-scope scan"' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-105 merged (it reads the held sources in full and records the readings; the re-grade of the `verified` rows no full reading covers belongs to it, the prior workplan's D-3). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. OR-11a is answered (2026-10-29); the entry's reading: `grep -n -F 'an extraction marked `verified` requires a recorded full-scope' references/project-standards.md`, and its ACTION (8): `grep -n -F '(8) Require a full-scope scan for' references/project-standards.md`.
- **The data must already be clean for the one class this task makes blocking.** On `$BASE`, `python3 scripts/audit/verified_scan_integrity.py | grep -E '^  VERIFIED-WITHOUT-FULL-READING:'` prints `0 row(s)`. If it prints more, the research repair has not landed: stop (section 9); do not re-grade a row here (rule 10).
- **Tests that must be red (or green) before you start:** the cases of section 6 step 2a marked red are red on the unchanged code.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-062-verified-reading-blocking "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-062" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

OR-11a is half built. Since 2026-11-06 `add-extraction` and `amend-extraction` refuse `extraction_status='verified'` without a full-scope reading that covers the row's parameter (`git log --format='%h %ad %s' --date=short -S'_require_full_scan_for_verified' -- scripts/db.py | tail -1`; tests V01 to V06 in `scripts/tests/test_run_pipeline_refusals.py`). The corpus-wide reader, `verified_scan_integrity`, is advisory, and its own registry note says it stays advisory "until those rows are re-graded in a data PR, then blocking". It cannot become blocking as a whole: two of its three classes (a row on an unverified source, a row no reading covers) wait on other work, one of them on an extraction retire path that does not exist (OI-56, AT-18). So once the `verified` class is clean, nothing stops a data migration that bypasses the writer (the hand-SQL shape CLAUDE.md rule 10 records) from marking a figure `verified` that no one read in full, and the render prints the status of each row (OR-11a's entry: "the renderer prints the status of each row"), so the reader is told a figure was verified when it was not.

**Evidence command** (run from the repository root; it reads the canonical database read-only):

```
python3 scripts/audit/verified_scan_integrity.py | grep -E '^EXAMINED|^  [A-Z-]+: |^(PASS|FAIL)'
python3 scripts/audit/verified_scan_integrity.py --class VERIFIED-WITHOUT-FULL-READING 2>&1 | tail -1
python3 -c "import yaml;print([(c['id'],c['level']) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if 'verified_scan_integrity' in ' '.join(c['cmd'])])"
```

**Expected output today (on this task's base, after T-105):** `EXAMINED:` above 0; `VERIFIED-WITHOUT-FULL-READING: 0 row(s)` (the precondition) and the two other classes as they stand; the second line is argparse's `unrecognized arguments: --class …` (the script takes no argument); the registry line lists one entry, `verified_scan_integrity`, `advisory`. On 2026-11-13, before T-105, the first class was not empty: that is why this task waits.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves OR-11a's at-rest half advisory for as long as the other two classes stand, which has no end date. Reuse: one argument on the existing script and a second registry entry, the shape `migration_reproducibility --deep` and `provenance_artefact_audit --mode` already use (`python3 -c "import yaml;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if len(c['cmd'])>2])"`). No new script.

1. **`scripts/audit/verified_scan_integrity.py`: one optional argument.** Move the `classes` tuple out of `main()` to module level, unchanged, as `CLASSES`. Add `argparse` with one option, `--class`, `dest="only"`, `choices=[name for name, _col, _remedy in CLASSES]` (derived from the tuple, never retyped), default None. When given, `main()` evaluates and prints that class alone; `EXAMINED:` is still the number of live extraction rows (the subject is unchanged), `PASS`/`FAIL` speak of that class only, and the exit code is 0 when it is empty, 1 otherwise. Without it, the output is byte-identical to today's (section 6 step 2b proves it). Add to the docstring's `Usage:` line `[--class NAME]` and one sentence: `--class VERIFIED-WITHOUT-FULL-READING is the blocking form (registry id verified_status_full_reading, T-062): OR-11a's at-rest half, held while the other two classes wait on other work.`
2. **`governance/check-registry.yaml`: a second entry**, directly after `verified_scan_integrity`, copying its `battery`, `kinds`, `basis`, `cost` and `min_items`:
   ```yaml
   - id: verified_status_full_reading
     cmd:
     - python3
     - scripts/audit/verified_scan_integrity.py
     - --class
     - VERIFIED-WITHOUT-FULL-READING
     battery: db_integrity
     kinds:
     - data
     - schema
     level: blocking
     basis: judgment/verified-reading
     cost: fast
     min_items: 1
     note: 'T-062 (OR-11a, owner 2026-10-29, ACTION (8)). The one class of verified_scan_integrity
       that is OR-11a itself: a row marked verified that no full-scope source_scans reading covering
       its parameter supports. BLOCKING because the writers refuse that state since 2026-11-06 and
       the legacy rows were re-graded or read in full (T-105), so a new one can only come from a path
       that bypassed the writer. EXAMINED prints the live extraction count (derive: run it). Its
       reader is the render, which prints each figure''s status (OR-11a), and the adversarial pass.'
   ```
   In the note of `verified_scan_integrity`, replace the sentence that begins `Advisory until those rows are re-graded in a data PR, then blocking.` with `Advisory while its SOURCE-NOT-VERIFIED and NO-COVERING-READING classes stand; its VERIFIED-WITHOUT-FULL-READING class is blocking as verified_status_full_reading (T-062).`
3. **The generated context map.** `python3 scripts/generate/context_map.py`, and include its output in the change: a new registry entry makes `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise. Then `python3 scripts/generate/context_map.py --check` exits 0.
4. **The contract sentence.** `governance/pipeline-contract.yaml`, criterion `verified-reading`, says `the corpus-wide reader is the check below, red while rows written before the writer refused the state stand (derive: run it).` Make it `the corpus-wide reader is the check below (its verified class is blocking as verified_status_full_reading), red while rows written before the writer refused the other two states stand (derive: run it).` Leave its `check:` line as it is.

**What reads what this task adds or changes:** `run_checks.py` reads the registry entry (battery `db_integrity`, CI); the render reads the status this keeps true (T-037; OR-11a's "the renderer prints the status of each row"). Nothing is replaced or made deletable.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `verified_scan_integrity`, `VERIFIED-WITHOUT-FULL-READING`, `verified-reading`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
This task adds a registry entry: run `python3 scripts/run_checks.py --selftest` after the change (CLAUDE.md §1: the registry's `basis` refs are checked there, and `--changed-from` does not run it), and `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after (it is red on the base; only a count above your before-run is yours).

**Hits when this file was written** (2026-11-13):

- `scripts/tests/test_run_pipeline_refusals.py`: the case E04 and its helper `integrity(db_path)` run the script with no argument (a caller: E04 must stay green, which proves the no-argument output did not change); this task adds its own cases beside it.
- `skills/run-pipeline_SKILL.md`: two sentences name the script and its classes (still true: mentions). If either says the check is advisory as a whole, add `(its verified class is blocking, T-062)`.
- `governance/check-registry.yaml` (yours), `governance/context-map.yaml` (generated, regenerated in item 3), `governance/pipeline-contract.yaml` (item 4).

Every test file in that list is run before and after the change (section 6).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `verified_scan_integrity`, `context_map_fresh`. Run each as the registry runs it and keep the output:

```
CHECKS="test_run_pipeline_refusals verified_scan_integrity context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT|PASS|FAIL' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
python3 scripts/audit/verified_scan_integrity.py > "$SCRATCH/before-noarg.txt" 2>&1; echo "rc=$?"
```

A check that is red here was red before you touched anything (`verified_scan_integrity` is red while its other two classes stand): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.**

*2a. The tests.* Confirm the prefix is free: `grep -c '"T062-' scripts/tests/test_run_pipeline_refusals.py` prints 0. Give the file's `integrity(db_path)` helper an optional second parameter `args=()`, appended to the subprocess argument list (E04 calls it without one, so it is unchanged). Add, directly after E04's `record(...)`, inside `with scratch() as c:`:

```python
    # T-062: the verified class alone, the blocking form. A HAND-made verified row over an abstract-only
    # reading is the state only a path that bypasses the writer can leave; the check must go red on it.
    ref = new_source(verified=True)
    hand_scan(c, ref, "abstract")
    xid = c.execute("INSERT INTO source_value_extractions (ref_id, parameter_id, claim_type, claimed_value, "
                    "claimed_unit, claim_text, extraction_method, extraction_status, figure_role, comparator, "
                    "created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (ref, P_ACTIVE[0], "numerical", "1200", "mm", "TASK-FIXTURE T062", "full-read",
                     "verified", "claim", "=", "t", "t")).lastrowid
    c.commit()                                         # HAND: a state the writer refuses
    rc_c, ex_c, got_c = integrity(os.environ["GUIDEBOOK_DB_PATH"], ("--class", "VERIFIED-WITHOUT-FULL-READING"))
```
If that INSERT is refused by a CHECK or NOT NULL column, add the column the message names with a value from its own CHECK (`dbcore.check_values`), never by weakening anything, and say so in the pull request. Then:

| id | assertion | after the change | on unchanged code |
|---|---|---|---|
| T062-01 | `rc_c == 1` and `got_c["VERIFIED-WITHOUT-FULL-READING"][0] >= 1` and `ref in got_c["VERIFIED-WITHOUT-FULL-READING"][1]` | green | red (argparse exits 2) |
| T062-02 | the other two classes are not printed: `got_c["SOURCE-NOT-VERIFIED"] == (0, set())` and `got_c["NO-COVERING-READING"] == (0, set())` (the helper's defaults when a class line is absent) | green | red |
| T062-03 | `ex_c` equals E04's `ex` plus the rows the scratch copy added (`c.execute("SELECT COUNT(*) FROM source_value_extractions x JOIN evidence_sources e USING (ref_id) JOIN base_parameters p USING (parameter_id) WHERE e.superseded_by_ref_id IS NULL AND p.status='active'").fetchone()[0]`): the subject is every live row, not the class | green | red |
| T062-04 | after HAND `UPDATE source_value_extractions SET extraction_status='preliminary' WHERE extraction_id=?` (xid) and `c.commit()`, the same call returns `rc == 0`: the class was empty on the base (the precondition), so removing the fixture's one row empties it (the control: the check is not red by construction) | green | red |
| T062-05 | `python3 -c "import yaml;…"` over the registry: an entry whose `cmd` ends with `--class`, `VERIFIED-WITHOUT-FULL-READING` has `level: blocking` and `basis: judgment/verified-reading` | green | red (no entry) |

*2b. The no-argument output is unchanged.* After the change: `python3 scripts/audit/verified_scan_integrity.py > "$SCRATCH/after-noarg.txt" 2>&1; echo "rc=$?"; cmp "$SCRATCH/before-noarg.txt" "$SCRATCH/after-noarg.txt"`: identical, and the same `rc`.

*2c. The mutations.* Each must be KILLED (harness in `$SCRATCH/t062-mutations.py`, the shape T-017 section 6 step 2b describes: assert the old text occurs once, edit, run `python3 scripts/tests/test_run_pipeline_refusals.py`, restore in `finally`): M1, in the script, make the class filter a no-op (evaluate every class even when `--class` is given) → T062-02; M2, in the registry entry, `level: blocking` → `level: advisory` → T062-05.

**Writing the test.** Take case ids that cannot collide (`T062-01`, …). Never type into a test an id, a code or a count the database can derive. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`, plus the new entry: `python3 scripts/audit/verified_scan_integrity.py --class VERIFIED-WITHOUT-FULL-READING; echo rc=$?` prints `EXAMINED:` above 0 and `rc=0` on the canonical database. Compare check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; `test_run_pipeline_refusals`' `EXAMINED:` grows by the T062 cases only. `python3 scripts/run_checks.py --selftest` passes.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** Do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** In `gate.txt` read the `RESULT` line, any check under `NOTHING-IN-SCOPE` (it has not passed: say so), and any blocking `FAIL`. `verified_status_full_reading` is new and blocking: it must pass.
- **The gate takes several minutes.** Run it in the background with a long timeout.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`.** Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** tells you nothing about your diff: name it in the pull request with its before and after lines.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: verified needs a full reading, blocking at rest (OR-11a) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. This task has no migration. The HAND rows of section 6 are written on the test's scratch copy only.
- Do not re-grade, re-read or amend any stored row (that is T-105, research; rule 10). If the precondition fails, stop.
- Do not make `verified_scan_integrity` as a whole blocking, and do not quarantine or relax it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine. Do not author synthesis prose.
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it.
- Do not add a table, column, check, verb or script that section 4 does not name. Fixing a caller the sweep finds is in scope.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met: in particular `VERIFIED-WITHOUT-FULL-READING` is not `0 row(s)` on `$BASE` (report the rows the script prints and that T-105, as the prior workplan's D-3, has not re-graded them);
- the evidence command in section 3 does not give today's expected output;
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the no-argument output of the script differs before and after (step 2b);
- `run_checks.py --selftest` fails on the new entry;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- The code and section 4 disagree about what exists: stop and report; do not reinterpret the plan.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request. Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff. One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, do not poll, do not schedule a reminder. The final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase).
