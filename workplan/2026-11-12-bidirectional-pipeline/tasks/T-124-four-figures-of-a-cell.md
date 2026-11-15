# T-124  The four figures of a cell (minimum, mode, median, maximum), computed once at the specification stage in the parameter's accessibility direction

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: findings A3.13, A4.3 and A1.2 of the adversarial pass on the remediation plan (`scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/AUDIT-FINDINGS.md`), re-verified 2026-11-14: the owner named four figures, no task computed them, and the plan had left the mode's and the median's scope to render though the ledger leaves it to the owner. Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the repair writer of the adversarial pass. **Opened 2026-11-14 by the owner's answer to OD-63** (fifteenth set: "all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes"; `grep -n -F "Owner answers 2026-11-14 (fifteenth set)" references/project-standards.md`): the maximum, the mode and the median are taken over every identified value for the cell and its context; render shows the four figures only as a colour code on the surveyed jurisdictional code bodies (T-037). Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-124 |
| Title | The four figures of a cell (minimum, mode, median, maximum), computed once at the specification stage in the parameter's accessibility direction |
| Wave | 6 (after the term-resolution tooling) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: Opus-class. It applies five owner entries of 2026-11-14 in code, two of them with recorded readings, and is placed in code T-059 and T-068 write |
| Traces to | the owner's entries "the project holds four data points: minimum, mode, median, maximum", "the minimum is the code stratum's lowest value, or the lowest identified value where there is no code data", "the figures run in the parameter's accessibility direction; the minimum may be the highest number" and the transparency entry (`grep -n -E '^## Owner (statement|answer) 2026-11-14 .*(four data points|minimum is the code stratum|accessibility direction|radically transparent)' references/project-standards.md`); TERM-RESOLUTION-PLAN §1 U3, U4 |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-059 and T-068 merged (T-059 builds selection in the accessibility direction and the no-direction case this task reuses; T-068 builds the cluster step, with the tolerance in one home, which is the mode). Check by running, per task, `git log "$BASE" --format=%s | grep -c -E 'task/t-059-wp-t4-agreement|^T-059:|execute workplan T-059'` and the same with `t-068-convergent-counts-roots`/`T-068`, each printing at least 1.
- **Owner decisions:** OD-63 (over which values are the maximum, the mode and the median taken?), **answered by the owner 2026-11-14** (fifteenth set; ledger: `grep -n -F "Owner answers 2026-11-14 (fifteenth set)" references/project-standards.md`): "all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes", recorded as `OD-63: all identified values when synthesising and determining; the render shows the minimum, mode, median and maximum as a colour code on the surveyed jurisdictional code bodies` (`grep -E '^OD-63:' references/project-standards.md | tail -1`). **What this task builds from it:** the maximum, the mode and the median over every identified value for the cell and its context, every stratum (item 1); the minimum stays as the owner's earlier answer settled it. **What it leaves to render (T-037):** the colour code on the code bodies, and its non-colour carrier. Earlier status, kept as history: registered and referred to the owner 2026-11-14 (`grep -n -F "questions the adversarial pass on the remediation plan found" references/project-standards.md`). Run the gate before you start and again before you open the pull request; it must print `OD-63 OPEN (owner)`, else stop (section 9). The gate reads the status class only; the answer is the last `OD-NN:` line (`REMEDIATION-WORKPLAN.md` section 13, "What the gate reads"):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-63; do gate $n; done
```
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T124-01` to `T124-08` (section 6), on the unchanged code.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-124-four-figures-of-a-cell "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task never moves it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-124" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The owner said the guidebook shows four figures for a cell, "minimum, mode, median, maximum", read in the parameter's accessibility direction, the minimum from the code stratum unless there is no code data. Nothing computes them: the engine states one value (the selection), render (T-037) was told to show four figures nobody produces, and no test checks the minimum, so a minimum taken numerically, or across every stratum, would pass every gate.

**Evidence commands** (read-only):

```
git grep -n -i -E 'def .*(median|mode|minimum|maximum|figures)' -- scripts/assess/assess_cell.py scripts/dbcore.py
git grep -n -i -E 'median' -- scripts ':!scripts/migrations' | cut -c1-120
```

**Output on 2026-11-14:** no function computes the four figures; `median` appears in no engine code. If the output differs (a function now exists), the ground has moved: stop (section 9) and read it before writing a second.

## 4. The change

Order of preference, from CLAUDE.md §8: one function, derived at read, nothing stored.

1. **One function**, `cell_figures` in `scripts/assess/assess_cell.py` beside `compose_value`, over the cell's identified values (the governing and the shown extraction links the engine already gathers for the cell's lens), returning for each figure its value, its unit and the extraction rows that state it:
   - **Order first.** Every value is ordered by the parameter's `accessibility_direction` before any figure is taken (owner: "order the identified values by the parameter's accessibility direction before taking any of the four; never take the numerically smallest value as the minimum without that order"). A parameter whose direction is NULL or `contested` gets **no minimum and no maximum**, only the identified values (the owner's direction entry; the same refusal T-059 tests as `T059-H7`).
   - **Intervals.** A figure that is an interval contributes its bounds through `dbcore.bound_on_scale`, never a midpoint (the owner's ranges statements).
   - **Minimum** (settled by the owner): the least accommodating value the **code stratum** (T4 to T6) states for the cell; where the cell has no code value, the least accommodating identified value, **labelled as drawn from research**, never as a code floor. Under the direction, a ceiling-only code claim ("at most 38 N") is the minimum of a lower-is-better parameter, and a floor-only claim ("at least 1200") the minimum of a higher-is-better one (the owner's correction of the numeric reading). Where codes of several jurisdictions state different values, return the least accommodating with every source that states it; how a page presents the set is render's.
   - **Maximum, mode, median (OD-63, answered 2026-11-14):** over **every identified value for the cell and its context, every stratum** (T1 to T6, Co-1, Co-2), each in accommodation order and each with the rows that state it ("all values when synthesizing and making determinations"). The maximum is the most accommodating identified value, which may be a code value where no research value is more accommodating; it is not the selected best where the harm test replaced the most accommodating value (the selection is T-059's, its one home in this plan: `tasks/T-059-wp-t4-agreement.md` section 4 item 6), and the function returns both, never conflating them. The mode is the cluster T-068's cluster step finds holding the most sources (most common practice counts practice; the independent-roots count is returned beside it, as T-068 shows it beside every convergence; its tolerance read from its one home, never restated; a tie returns every tied cluster; a live cell whose mode differs when counted by roots is listed in the pull request, not decided); the median is the middle value in accommodation order (two middle values: both, never their mean).
   - **One value:** all four coincide and the function says so.
2. **Nothing is stored.** The figures are derived from rows already held (rule 5); the engine's report (`--report-json`) and render (T-037) read the function. If a reader needs them in SQL, that is a view in a later task, not a column here. **Where render reads them (OD-63):** render calls `cell_figures` for the cell (or reads the same four figures from the engine's `--report-json`, which calls it) and uses them as the colour code on the jurisdictional code bodies it lists from T-036's comparison view; it never re-computes a figure, and the figures it colours by are the ones this function takes over every identified value, not figures re-taken over the code bodies alone. The function therefore returns, with each figure, the rows that state it and each row's jurisdiction (through its source), so render can tell which code body carries which figure without a second computation.
3. **Tests** in `scripts/tests/test_assess_cell_pilot.py` (prefix free: `git grep -c 'T124-' scripts/tests/`; fixtures on the test's own scratch copy, as T-017's `_t017_cell` builds them).

**What reads what this task adds:** render (T-037: its cases `T037-F1` to `T037-F5` compare the page's colour code with this function), the engine's report, and T-122's criterion `spec-four-figures`. **What wrong thing reaches the guidebook without it:** a page with no minimum, mode, median or maximum, or one whose render code computes them on its own (a second home), numerically, or across the wrong stratum. **What it makes deletable:** nothing today; it prevents a second implementation in render.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `cell_figures`, `compose_value`, `bound_on_scale`. Prose that names the four figures (`git grep -n -i -E 'minimum, mode, median' -- governance architecture skills ':!references/project-standards.md'`) is read; a sentence that says how they are computed and differs is corrected or listed for T-120's owner.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="test_assess_cell_pilot test_evidence_cell_state_2_3"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
**Step 2: red before, green after** (each red on the unchanged code, which has no `cell_figures`):
- `T124-01` a lower-is-better cell whose only code value is a ceiling ("at most" a value) beside research values below it: minimum = the code ceiling, labelled code; maximum = the lowest research value.
- `T124-02` a cell with no code value: minimum = the least accommodating research value, labelled research.
- `T124-03` numeric against accommodation order: a lower-is-better cell; the numerically smallest value is the maximum, never the minimum.
- `T124-04` direction NULL: no minimum and no maximum; every value returned with its source.
- `T124-05` an interval ("1000 to 1200") beside points: both bounds enter the figures; no midpoint appears.
- `T124-06` a harm-test cell (T-059's `T059-H2` fixture): the maximum is the most accommodating value; the selected best is the value the source proposed; both are returned and differ.
- `T124-07` one value: all four coincide.
- `T124-08` (OD-63) the scope is every stratum: a higher-is-better cell with a T1 value above every code value: the maximum is the T1 value; the same cell with a T6 value above every research value and no source stating worse results: the maximum is the T6 value; the median and the mode are taken over the research and the code values together (a fixture where the research-only median differs from the all-values median asserts the all-values one); each figure's rows carry their jurisdiction.
- Seeded defects, each KILLED: the minimum taken over every stratum (T124-01); the order taken numerically (T124-03); the median as a mean of two (a two-middle fixture inside T124-05); the maximum, mode or median taken over research values only (T124-08).
**Step 3: after-run**, as step 1 with `after-`; nothing new may fail.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
`sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: the four figures of a cell, in accessibility direction (OD-63) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner entries and the OD-63 answer line; the function; the tests red before and green after; the seeded defects killed; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not build while the gate prints CLOSED for OD-63. Do not narrow the maximum, the mode or the median to a stratum (OD-63: every identified value). Do not build the colour code here: it is render's (T-037).
- Do not store a figure; do not change which value the cell states (T-059) or its marker (T-117); do not restate the tolerance or the selection rule (one home each).
- Do not take any figure in numeric order, or a minimum over every stratum when a code value exists. Do not average.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the gate prints CLOSED for OD-63, or a later `OD-63:` line in the ledger differs from the one section 2 quotes; a dependency is not merged; the evidence output differs; a row's jurisdiction cannot be reached through its source without a new column; a test green before is red after.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (it should attack the direction order and the minimum's stratum); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
