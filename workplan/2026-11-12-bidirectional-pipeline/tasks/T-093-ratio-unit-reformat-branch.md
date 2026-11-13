# T-093  `amend-extraction` accepts `ratio` to `rise:run ratio` as a reformat, if the owner rules it one

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the follow-up `tasks/T-061-amend-extraction-reformat.md` names and does not build (`grep -n -F 'Not built here' workplan/2026-11-12-bidirectional-pipeline/tasks/T-061-amend-extraction-reformat.md`), and `tasks/T-086-bare-ratio-rows.md` section 2. Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study, finishing an open item of the previous integration (T-086 had no id for this branch). **Held on OD-41, and built only under its answer (a).** Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-093 |
| Title | `amend-extraction` accepts `ratio` to `rise:run ratio` as a reformat, if the owner rules it one |
| Wave | 1 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OD-41 option (a); T-061 section 4, "Not built here"; T-086 (the research task that amends the rows under (a)) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-061 merged (it adds `_refuse_unless_reformat`, which this task gives one more branch). Check by running: `git grep -n 'def _refuse_unless_reformat' -- scripts/db.py` prints one line.
- **Owner decisions:** OD-41 (OPEN, registered 2026-11-13, not yet asked): is changing the unit `ratio` to `rise:run ratio` on the stored rows a reformat (OR-3) or a new reading (a second row, D-0168)? Read it by `grep -F "OD-41 STATUS:" references/project-standards.md | tail -1` and the answer line `grep -n -F "OD-41:" references/project-standards.md | tail -1`. **Only under answer (a) is this task built.** Under (b) it is declined: stop at once (section 9), and the coordinator records the decline in the plan and removes T-093 from T-086's "Tasks that must be merged" bullet. The plan's generator cannot tell the two answers apart: it shows this task OWNER-held until OD-41 is answered by the owner and READY after either answer, so the answer line, not the generator, decides whether it is done.
- **Tests that must be red before you start:** `T093-01` (section 6): the dry run below is refused.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-093-ratio-unit-reformat-branch "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-093" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

Some stored ramp gradients read `1:12` under the bare unit `ratio`. The engine reads an `a:b` figure only under `rise:run ratio`, so they are left out of every ramp-gradient cell. T-061's reformat rule lets a unit lose words in place but never gain them, so `ratio` to `rise:run ratio` is refused as a new reading. If the owner rules that change a reformat, the rule needs one branch.

**Evidence commands** (on `$SCRATCH/t.db`, read-only; after T-061 has merged):

```
python3 -I -c "import sqlite3,sys;print(sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True).execute(\"select group_concat(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone())" "$SCRATCH/t.db"
grep -n 'NOTATION_FAMILIES = ' -A2 scripts/dbcore.py
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py amend-extraction --extraction-id "$(python3 -I -c "import sqlite3,sys;print(sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True).execute(\"select min(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone()[0])" "$SCRATCH/t.db")" --field claimed_unit --value 'rise:run ratio' --reason probe --session session_probe --dry-run 2>&1 | tail -1
```

**Output on 2026-11-13** (the first two only; T-061 is not merged, so the third could not be run): the ids `52,53,54,57,58,60,61,62,64,65,66`; `NOTATION_FAMILIES` holds one family, `gradient`, with `%` and `rise:run ratio`. After T-061, the third is expected to print a `REFUSING:` line saying `'rise:run ratio'` is not, on word boundaries, in the row's unit cell. If it is accepted, the branch exists: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing (the owner's answer (b) makes this the choice); otherwise one branch in the existing rule, no new function.

1. **In `_refuse_unless_reformat`, unit branch** (`scripts/db.py`): when the new unit does not stand in the old cell, accept it if and only if (i) the new unit is a member of one of `dbcore.NOTATION_FAMILIES`' tuples (read from the constant, never typed), (ii) the old cell, stripped, stands on word boundaries in the new unit (`_as_whole_words(row["claimed_unit"], value)`, the helper T-061 already calls the other way round), and (iii) the stored figure reads under the new unit (`dbcore.figure_refusal(...)` is None, the check that already follows). Otherwise the existing refusal stands, word for word.
2. **Its comment.** One sentence in the docstring's `claimed_unit` entry: "Or, under OD-41 (a), a family member of `dbcore.NOTATION_FAMILIES` that contains the old cell on word boundaries (`ratio` -> `rise:run ratio`), when the figure reads under it."
3. **Nothing else.** No other unit gains words; no row is amended here (T-086).

**Chosen (authoring 2026-11-13):** the condition is "a notation-family member that contains the old cell", as T-061 named it. Rejected: a pair list (`{'ratio': 'rise:run ratio'}`), a second home for what the notation families already declare (rule 8).

**What reads what this task adds:** `amend-extraction`; T-086 under (a). **What wrong thing reaches the guidebook without it (under (a)):** the bare-`ratio` gradients stay out of every ramp-gradient cell. **What it makes deletable:** nothing.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `_refuse_unless_reformat`, `NOTATION_FAMILIES`, `rise:run ratio`.

**What a caller is.** A hit whose behaviour or truth changes: a test of `_refuse_unless_reformat`'s unit branch (T-061's cases; one that asserts `ratio` to `rise:run ratio` is refused is now wrong under (a) and is changed, and the change listed); a skill or help sentence that says a unit cannot gain words. Left out: `workplan/` except `workplan/pipeline-state-graph/machines.yaml`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_run_pipeline_refusals test_db_amend_writers"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
**Step 2: red before, green after** (cases `T093-01`… in `scripts/tests/test_run_pipeline_refusals.py`; prefix free: `git grep -c 'T093-' scripts/tests/`; probes chosen by query):
- `T093-01` a bare-`ratio` row (the first by query) amended to `rise:run ratio` is accepted, the value and quote unchanged and the old unit in notes; red before.
- `T093-02` the same row to `mm` is still refused with T-061's message; a `%` row to `rise:run ratio` is refused (the old cell is not in the new unit); a row whose figure does not read under `rise:run ratio` (a bare number, built on the copy as `TASK-FIXTURE`) is refused.
- Seeded defect: drop condition (i); `T093-02`'s `mm` case still refuses but a fixture row under unit `ratio` amended to `ratio of widths` is accepted, so a test asserting its refusal goes red; restore.
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
git commit -m "governance: a bare ratio unit reformats to rise:run ratio (OD-41 (a)) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's answer and its ledger line; evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not build this under answer (b), or before OD-41 is answered.
- Do not type a unit pair; read the families. Do not change T-061's other refusals or their text.
- Do not amend any row (T-086). Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: OD-41 is unanswered, or answered (b) (then the task is declined: report so); T-061 is not merged; the dry run of section 3 is already accepted; a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
