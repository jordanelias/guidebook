# T-143  An angle in degrees converts to the gradient by its tangent, ordered exactly and shown on the safe side

_One task of a stacked pull request (`grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index and register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, item 32 and section 4 item 11, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number here was read on 2026-11-19 and is given with the command that produces it: re-run it; do not trust the number. Canadian English._

**Pilot status.** Not piloted. Authored 2026-11-19 by an Opus-class task author. **The adjudication deferred the build of this rule to T-059's comparison step; the datum that settles when it is built is not in hand on 2026-11-19 (section 3), so this task's first step stops today.** Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-143 |
| Title | An angle in degrees converts to the gradient by its tangent, ordered exactly and shown on the safe side |
| Wave | 1 (chain): the last prerequisite of T-059, built with it |
| Layer (CLAUDE.md §3) | 1 (a cell on `base_units`) and 2 (the converter, the engine's ordering, `add-unit`) |
| Kind | **TOOLING** (CLAUDE.md rule 10). The `degrees` row itself is research, landed by `add-unit` in its own pull request |
| Executor | NOT FOR SONNET: Opus-class. The task writes a conversion rule, an exact ordering that must never fall back on a float tolerance, and the meaning of four refusals |
| Traces to | the adjudication's item 32 (with items 31, 35, 36); OD-24 ("gradient (ratio, percentage or degrees as notations)", `grep -n -E '^OD-24:' references/project-standards.md`); OD-22 ("round a minimum up and a maximum down", `grep -n -E '^OD-22:' references/project-standards.md`); the sweep list `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md`, T-030 item 2 |

## 2. Preconditions

- **The integration base**, as T-142's section 2 states it (`origin/main` once the workplan merges; on a stacked batch a task is met if its commit is on `HEAD` or `origin/main`).
- **Tasks that must be merged first, and the order of this one.** The adjudication: "`degrees` … (b) adopted as the rule, DEFERRED in build to T-059's comparison step", with the follow-on "a cell on `base_units` naming the conversion, inside the T-059 prerequisites". So this task runs **immediately before T-059**, after every other prerequisite of T-059, and T-059 then orders values through what this task builds:
  - every task T-059's section 2 names as merged first (T-016, T-019, T-120, T-126, T-127, T-128; read them from its file, `grep -n -F "Tasks that must be merged to the integration base first" workplan/2026-11-12-bidirectional-pipeline/tasks/T-059-wp-t4-agreement.md`), and T-059 itself **not** merged;
  - T-137 (`tasks/T-137-units-and-kinds-as-data.md`, the adjudication's section 4 item 3: `add-unit` with a warrant, item 31; exact bounds on `specifications`, item 35). Its own file says a non-linear unit "cannot pass the factor test and stays standing alone: that is DEFERRED to T-059, not built here" (`grep -n -F "DEFERRED to T-059" workplan/2026-11-12-bidirectional-pipeline/tasks/T-137-units-and-kinds-as-data.md`); this task is that deferral. Without `add-unit` no tangent row can be added by data; without exact bounds a bound stated in degrees would be stored as a float.
- **Owner decisions and delegated resolutions, through the ledger's gate** (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`); any CLOSED line is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-22 OD-24 OD-42; do gate $n; done
```
  On 2026-11-19: `OD-22 OPEN (delegated; not required)`, `OD-24 OPEN (delegated; not required)`, `OD-42 OPEN (delegated; confirmed with corrections applied)`. OD-24 makes degrees a notation of the gradient kind; OD-22 fixes the safe side; OD-42 keeps a change within one system exact (not reached: degrees and percent carry no measuring system). The design items 31 to 36 are ratified by reference to the adjudication (the ratification entry, "the design questions numbered 12 to 91 … are ratified by reference").
- **Tests that must be red before you start:** `T143-01` to `T143-09` (section 6).
- **Set-up** (the stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1):
```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
# stacked batch: stay on the batch's branch (no git switch -c); single task: git switch -c task/t-143-degrees-rule "$BASE"
BASE_PRE=$(git rev-parse HEAD); echo "BASE_PRE=$BASE_PRE"  # every DIFF below uses $BASE_PRE on a stacked batch
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-143" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Begin every later block with the `W=…; BASE=…` line, `BASE_PRE=<the sha you recorded>` and `export SCRATCH=…`. Probes run on `$SCRATCH` with `--session session_task-probe`; never edit or delete `scratchpad/<session>/refusals.jsonl`. **Pilot:** stop after section 7.

## 3. The problem, in the guidebook's terms, and the datum the deferral waits on

A source that states a ramp's slope as an angle ("not more than 4.8°") and one that states it as a percentage describe one quantity (OD-24), yet the engine cannot compare them: `degrees` has no row of `base_units`, so a degrees figure stands alone, and a cell holding both is refused as "different units". A linear factor cannot hold it: the percentage is 100·tan(θ), not a rescaling of θ (`grep -n -F "ARCTANGENT of the gradient" scripts/dbcore.py`). Today's refusal composes nothing wrongly; what reaches the guidebook is a ramp cell that shows its figures but cannot say which is the most accommodating, so the selection T-059 builds would pass over an angle figure.

**The datum (run this first, read-only; it is the task's step 0):**
```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*), group_concat(extraction_id), group_concat(distinct parameter_id) from source_value_extractions where claimed_unit='degrees' and retired_at is null\").fetchone(), c.execute(\"select count(*) from base_units where unit='degrees'\").fetchone(), [r[1] for r in c.execute('pragma table_info(base_units)') if r[1] in ('conversion','warrant_quote')])"; grep -c '"add-unit"' scripts/db.py
for t in T-120 T-127 T-128 T-059; do echo "$t $(git log origin/main HEAD --format=%s | grep -c -F "$t")"; done
```
**Output on 2026-11-19:** `(4, '11,12,46,47', '3') (0,) []`, then `0`, then `T-120 0`, `T-127 1`, `T-128 0`, `T-059 1` (the two hits are the commits that authored those task files, `8323f1f9` and `4978132c`; read them with `git log origin/main HEAD --format='%h %s' | grep -E 'T-127|T-059'`; neither is an execution). Read: the live subject exists (four live figures in degrees, all on one parameter; the adjudication's own query, `select extraction_id, parameter_id from source_value_extractions where claimed_unit='degrees' and retired_at is null`, returns the same four rows), `degrees` has no row, `add-unit` does not exist, and T-059's prerequisites T-120, T-127 and T-128 are not executed. **So the datum is not in hand on 2026-11-19: stop at step 0 and report.**

**Step 0, the rule for stopping.** Go on only when all of these hold; otherwise stop, change nothing, and report what printed: (i) the live subject count is above 0 (if it is 0, there is nothing to convert: report "do nothing", CLAUDE.md §8); (ii) `add-unit` exists and `specifications` holds exact bounds (the item-3 task's own after-test); (iii) every other prerequisite of T-059 is met by T-059's own section 2 check, and T-059 is not merged; (iv) the coordinator confirms T-059 is the next task of the stack. The ids above are probes read on 2026-11-19; a test never types them.

## 4. The change

Order of preference (CLAUDE.md §8): do nothing; change a rule; reuse; delete the cause; only then add the smallest code. "Do nothing" leaves T-059 unable to compare an angle with a percentage, which the adjudication rejected as option (a).

1. **One cell on `base_units`: `conversion TEXT NOT NULL DEFAULT 'linear' CHECK (conversion IN ('linear','tangent_degrees'))`**, by `ALTER TABLE … ADD COLUMN`, with `CHECK (conversion = 'linear' OR (figure_form = 'number' AND system IS NULL AND factor_numerator = 1 AND factor_denominator = 1))`. The vocabulary is the column's CHECK, read by `dbcore.check_values` (rule 8). A `tangent_degrees` row means: the figure is an angle θ in degrees, and its value on the kind's canonical scale is tan(θ) multiplied by the factor of the kind's ratio-form unit (`dbcore.ratio_unit(conn, kind)`), because tan(θ) is rise over run and that row already holds what one unit of rise over run is on the canonical scale (`rise:run ratio`, factor 100 for the gradient kind: `select unit, factor_numerator, factor_denominator from base_units where figure_form='ratio'`). So the tangent row carries no factor of its own (1/1), and one fact has one home (rule 5). Recreate `ux_base_units_canonical` from its current text in `sqlite_master` with `AND conversion = 'linear'` added to its `WHERE`, so a tangent row's 1/1 is never read as the kind's canonical unit. If SQLite refuses the cross-column CHECK in `ADD COLUMN` on the scratch copy, the DDL keeps the vocabulary CHECK only, the rest goes into `add-unit`'s refusals (item 4), and the pull request says so.
2. **The converter, in `scripts/dbcore.py`, beside `to_canonical` and `from_canonical`** (unit arithmetic's one home):
   a. `UnitRow` gains `conversion`; `load_units`, `kind_members` and `canonical_unit` read it; `canonical_unit` and `_ratio_member` consider linear rows only.
   b. **Exact values.** For rational θ in degrees, tan(θ) is rational only when tan(θ) is 0, 1 or −1 (if tan θ = q is rational, cos 2θ = (1−q²)/(1+q²) is rational, so by Niven's theorem cos 2θ ∈ {0, ±½, ±1}, and only q ∈ {0, ±1} is rational). On (−90°, 90°) that is θ ∈ {−45, 0, 45}. At those angles `to_canonical` returns the exact Fraction (0 or ± the ratio factor). At any other angle it raises a named error saying the value is not exact on the canonical scale and naming the two functions below; it never returns a float.
   c. **`figure_cmp(conn, (raw_a, unit_a), (raw_b, unit_b))`** returns −1, 0 or 1 for two figures of one kind, exactly. Two linear figures compare as Fractions, as today. Where a tangent figure is involved and both are exact by (b), compare the Fractions. Otherwise the two are never equal (by (b)), and the order is decided by an enclosure of tan(θ) (or of atan) computed with `decimal` at a working precision whose error is bounded in the code, doubling the precision until the enclosure lies wholly on one side of the other figure. **No tolerance constant**: a fixed epsilon would be a typed number deciding an order the arithmetic can decide (rule 7a). tan is increasing on (−90°, 90°), so the order of angles is the order of gradients.
   d. **`shown_conversion(conn, raw, from_unit, to_unit, bound)`** returns `(text, exact, mark)` for a figure stated in one unit and shown in another of its kind, where either is a tangent unit. Exact cases (b) are shown exactly, marked `MARK_CONVERTED`. Otherwise the text is cut from the enclosure to `SHOWN_DIGITS` significant digits on the safe side (OD-22): a `min` upward and a `max` downward in a unit that rises with steepness (percent, degrees); for the ratio-form target (`1:n`, whose `n` falls as steepness rises) a `min`'s run is cut downward and a `max`'s upward; the cut point is decided by the enclosure, widening the precision until it does not straddle it; `exact` False; mark `MARK_CONVERTED`. Where the two cut bounds of one figure would cross (a range narrower than the cut), the digits are extended until they do not cross, never shown inverted (item 36's purpose; no new mark). A floor and a ceiling that coincide follow T-030's existing rule, two claims and never a point (`grep -n -F "merely coincide are two claims" scripts/assess/assess_cell.py`; its case is `T030-16`).
   e. **`figure_refusal`** (`grep -n "def figure_refusal" scripts/dbcore.py`) refuses a figure in a tangent unit whose angle is not strictly between −90 and 90, naming the next act: the figure is not the angle of a slope; record it in the unit the source states. No other figure refusal changes.
3. **The engine** (`scripts/assess/assess_cell.py`: the compose step that reads `unit_kind`, `bound_on_scale` and `from_canonical`, `grep -n "COMPOSE ACROSS UNITS OF ONE KIND" scripts/assess/assess_cell.py`) orders governing bounds through `figure_cmp` whenever a tangent unit is among them, so a cell with degrees and percent figures composes; every other notation of the kind is shown by `shown_conversion` or `from_canonical`, marked as derived.
   **Storage: an open point this file does not settle, and the coordinator confirms before execution.** T-137 (the item-3 task, `tasks/T-137-units-and-kinds-as-data.md` section 4 item 3) stores `value_min` and `value_max` as exact Fraction text on the kind's canonical scale under one `value_unit`. A bound governed by a tangent figure at any angle other than −45°, 0° or 45° has no exact value on that scale (item 2b), so T-137's form cannot hold it. *This file's reading, which needs the coordinator's confirmation:* when a governing bound is such a figure, `value_unit` is the tangent unit and each bound is stored as the exact figure in it, provided the other bound is stated in that unit, is one of the exact cases, or is absent; when the two bounds are governed by figures in two notations that cannot both be exact in one unit, both stay NULL, the note names the two notations, and the governing figures and their converted notations are shown (no value is invented and no float is stored). The alternative, a unit per bound, is a column this file does not name. If the coordinator does not confirm the reading, stop before item 3 (section 9). Cells with linear units only produce byte-identical output (`T143-08`). T-059's selection, built next, orders through `figure_cmp` and adds no second comparison: T-059's file needs a line naming this task as a prerequisite and that rule; that edit is the coordinator's.
4. **`add-unit --conversion`** (the verb T-137 adds; its factor test, "the quote … must hold one figure in the new unit and one in a unit of the same kind already held whose canonical values are equal under the given factor", cannot hold for a tangent row and is replaced for `tangent_degrees` by the test below), with choices from the CHECK (`dbcore.schema_choices("base_units", "conversion")`), default `linear`. Refusals, each in words before a constraint would raise: `tangent_degrees` with a factor given (it has none of its own: item 1); `tangent_degrees` for a kind with no ratio-form unit (naming that the kind's ratio unit must be added first); `tangent_degrees` with `--figure-form ratio` or a `--system`. The warrant cells are T-137's (the words and the locator); for a `tangent_degrees` row the quote must hold one figure in the new unit and one in the kind's ratio-form or canonical unit whose values agree under this rule exactly, which only the exact cases of item 2b can (a quote stating `45°` beside `100 %` or `1:1`); name which half was missing. No length or tolerance is typed.
5. **No row is written by this task.** The `degrees` row lands by `add-unit --conversion tangent_degrees` in a research pull request (rule 10), after which the four live figures of section 3 compose with the parameter's percentage figures.

**What reads what this task adds:** `conversion` is read by `load_units` and so by every converter and the engine; `figure_cmp` by the engine's compose step now and T-059's selection next; `shown_conversion` by the engine's notation record and render (T-037); the `figure_refusal` branch by `add-extraction`. **Without them, what reaches the guidebook:** an angle figure that can never be weighed against a percentage, so the most accommodating gradient of a ramp cell is chosen from the percentage figures alone, or, if a linear row were added for degrees by analogy, 5° read as 5 % (the defect `scripts/tests/test_assess_cell_pilot.py` records: `grep -n "arctangent" scripts/tests/test_assess_cell_pilot.py`).

**Schema migration (this task has one).** Derive its number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; it ends by setting `PRAGMA user_version` to the same. Run `python3 scripts/audit/joined_cells_census.py` before and after (no new candidate). Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep`. No `scripts/migrations/data_*` file. Then `python3 scripts/generate/context_map.py`.

**Code size.** `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`; name what reads each addition.

## 5. Caller sweep

Names to sweep: `load_units`, `UnitRow`, `to_canonical`, `from_canonical`, `bound_on_scale`, `canonical_unit`, `kind_members`, `ratio_unit`, `figure_refusal`, `base_units`, `ux_base_units_canonical`, `degrees`, `add-unit`.

**What a caller is**, and what the sweep leaves out, as T-135's section 5 states them (`sed -n '/^## 5. Caller sweep/,/^## 6/p' workplan/2026-11-12-bidirectional-pipeline/tasks/T-135-domain-vocabulary.md`). Per name:
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after; report only lines your change adds.

**Callers found 2026-11-19** (`git grep -l -E "load_units|to_canonical|from_canonical|UnitRow|kind_members|canonical_unit" -- scripts ':(exclude)scripts/migrations'`; re-run): `scripts/dbcore.py`; `scripts/assess/assess_cell.py` (the compose step and its comment "millimetres and degrees are different kinds of quantity": millimetres and degrees stay different kinds, the comment's example stays true, reword it if it implies degrees has no row); `scripts/tests/test_assess_cell_pilot.py` (the case "`degrees` has no row, so it is never read as a unit of the gradient kind" reads the canonical table through `synth_db`: rewrite it to hold on any data, that a `degrees` row is read as a gradient notation only through `tangent_degrees` and never as a linear factor, since a research row will land later; the mm-against-degrees "different units" case stays and stays green, the kinds differ); `scripts/audit/graph/build.py` (a name match on `_assert_distinct_from_canonical`: a mention). The schema objects naming `base_units`: the table and `ux_base_units_canonical` (`select type, name from sqlite_master where sql like '%base_units%'`). `degrees` also appears in `scripts/dbcore.py`'s comment on the unit table (reword: degrees now has a rule, as data). No registry entry names any of them.

## 6. Verification

**Step 1, before any edit:** set `CHECKS="test_assess_cell_pilot test_run_pipeline_refusals test_db_amend_writers test_scan_contract migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit context_map_fresh derived_not_curated_audit"` (each a registered id on 2026-11-19), then run the `for c in $CHECKS` line of T-135's step 1 (`grep -n -F 'for c in $CHECKS' workplan/2026-11-12-bidirectional-pipeline/tasks/T-135-domain-vocabulary.md`), writing `before-<check>.txt`. A check red here was red before you; one with no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** Cases in `scripts/tests/test_assess_cell_pilot.py` (registered), prefix `T143-` (confirm free: `git grep -c '"T143-' -- scripts/tests` prints nothing). A `tangent_degrees` row is added on the test's own copy (`synth_db`) through the writer, labelled `TASK-FIXTURE`; the kind and its ratio unit are chosen by query (`select kind_id from base_units where figure_form='ratio'`), never typed. Each case is red today and must also go red on its named **seeded defect**, shown and then removed (restore byte for byte; `cmp`):
- `T143-01` exact angles: 45° is exactly the ratio factor and 0° is 0 on the canonical scale; `to_canonical` of 30° raises the named error and returns no float. Defect: return `Fraction(math.tan(...))`.
- `T143-02` order: 4.8° against 8.4 % and against 8.3 % (tan 4.8° × 100 lies between them; the expected signs are computed in the test from `decimal` at a precision the test states, not typed), and 45° against 100 % compares equal. Defect: compare with a float and an epsilon.
- `T143-03` order is never decided by a tolerance: two figures closer than any fixed epsilon you can name (an angle and the percentage cut from its own enclosure at a high precision) are ordered correctly. Defect: a fixed precision with no widening.
- `T143-04` shown on the safe side: a maximum of 4.8° shown in percent is not above 100·tan 4.8°, a minimum not below; a maximum shown as `1:n` has `n` not below the true run. Defect: round to the nearest.
- `T143-05` a narrow range whose two cut bounds would cross is shown with more digits, never inverted. Defect: no extension.
- `T143-06` the engine composes a cell holding a degrees floor or ceiling and a percent figure into one interval with its notations marked converted, where the unchanged code wrote "different units". Defect: the engine's compose step reverted to `to_canonical` only.
- `T143-07` refusals: `add-unit --conversion tangent_degrees` with a factor, for a kind with no ratio unit, with a figure form `ratio`, each refused naming the next act; `add-extraction` of 90° and of −95° in the tangent unit refused. Defect: each branch removed in turn.
- `T143-08` a cell with linear units only gives byte-identical `value_notations` and bounds before and after (all live cells of the copy, chosen by query). Defect: `figure_cmp` used with a float for linear units.
- `T143-09` the canonical-unit index ignores a tangent row (a tangent 1/1 row beside the kind's canonical unit is accepted; a second linear 1/1 row is still refused). Defect: the index without `conversion = 'linear'`.

**Step 3, after:** the same loop with `after-`; compare failing lines check by check (T-135's step 3 command). No new failing case.

**Step 4: the gate, once**, in the background with a long timeout, waiting with an until-loop on its output file: `scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"`.

## 7. Commit

After the gate is clean: `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'`; `git commit -m "governance: convert an angle in degrees to the gradient by its tangent, ordered exactly [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: changes, the step-0 datum as printed, evidence before and after, callers and what was done to each>" -m "<the trailers your session gives>"`.

## 8. What you must NOT do

- Do not start past step 0 while the datum is not in hand. Do not write `data/guidebook.db` except through `migrate_db.py`; do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`.
- Do not add the `degrees` row, or any unit row, here (rule 10); do not give a tangent row a factor (rule 5).
- Do not store, return or format a float for a converted figure; do not decide an order or a cut with a tolerance constant.
- Do not change how linear units convert, round or display; do not touch T-059's selection rule.
- Do not add a mark, a conversion kind, a verb or a column section 4 does not name. Fixing a caller the sweep finds is in scope.
- Do not weaken a refusal or relax a CHECK; do not hand-type a count; do not type a unit spelling or an id into a test.
- Do not push, open a pull request, or subscribe to pull-request activity on a stacked batch.

## 9. Stop conditions

Stop, change nothing further, and report when: step 0's datum is not in hand (the expected state on 2026-11-19); a precondition is unmet or the gate prints CLOSED; the live subject differs from the adjudication's query in kind (a degrees figure on a parameter whose kind is not the gradient: `select parameter_id, quantity_kind from base_parameters where parameter_id in (<the parameters step 0 printed>)`, NULL on 2026-11-19, which does not stop); the coordinator does not confirm item 3's storage reading; a case is not red before, not green after one honest attempt, or survives its seeded defect; a check green before is red after; the rebuild does not reproduce the database; T-059 is merged before this task (its comparison would then need this rule wired into its own code, which this file does not describe); you would have to guess a value, a unit spelling or the owner's intent.

## 10. Rollback

Before merge: drop the commit from the stack by the coordinator's choice. After merge: a compensating migration in a new pull request (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Stacked batch: the coordinator runs `/adversarial` on the commit and `/batch-done`, and opens the one pull request last; ask the critic to attack item 2c (an order decided with no tolerance) and item 2d's safe side for the ratio form first. Single task: `/adversarial` once, `/batch-done`, push, open the pull request last, call `unsubscribe_pr_activity` immediately, push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
