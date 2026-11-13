# T-091  A figure's circumstance (building use, new or existing, interior or exterior) in typed cells

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the adjudication of the Edmonton digest, Q7, R1, R7 and proposal P8 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`); the owner's question Q7 "how do you handle a commercial versus residential versus public?" (`grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study. **Held on OD-49**: nothing in section 4 is built until the owner answers it, and what is built depends on the answer. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-091 |
| Title | A figure's circumstance (building use, new or existing, interior or exterior) in typed cells |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: the carrier's shape (columns or a link table, the key question, the vocabulary's home) is a design written by an Opus-class session from the owner's answer, as `T-018-design.md` was |
| Traces to | ADJUDICATION Q7, R1, R7, P8; the 2026-08-27 ruling that `base_building` is three levels (`grep -n -F 'base_building' references/project-standards.md \| head -2`); the 2026-11-06 schema-shape ruling, one value per cell (CLAUDE.md §4); OD-24's split test (`grep -n -F 'OD-24: flat and coarse' references/project-standards.md`); T-092 (the research task that re-tags the stored figures) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none; the design file `T-091-design.md` written first, after the owner's answer (section 4 item 1). T-017's branch partition and T-019's lens gather, which an answer (a1) builds on, are merged.
- **Owner decisions:** OD-49 (the adjudication's AQ-3; OPEN, registered 2026-11-13, not yet asked): (a) is building type a branch within one determination, part of what a determination is keyed on, or left in `setting`, and what is its vocabulary; (b) is the construction-element level a table of its own, or the element terms the catalogue already holds? Read the answer by `grep -F "OD-49 STATUS:" references/project-standards.md | tail -1`, then the answer line. Under (a3) "leave it in `setting`" this task is declined: the coordinator records the decline in the plan and T-092 with it.
- **Tests that must be red before you start:** section 3's first command prints parameters with more than one distinct `setting`, and `grep -n 'setting' scripts/assess/assess_cell.py` shows the engine reading none.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-091-typed-circumstance-carrier "$BASE"         # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-091" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A figure for a dwelling and a figure for a public building, for the same quantity and the same group, compose into one headline, because what kind of building, new or existing work, and interior or exterior are held together in one free-text cell, `setting`, which the engine never reads. The owner ruled in 2026-08-27 that building type is the first of three base levels; no figure points at it. OD-24 asks that clause variations be typed conditions, but a typed condition today is a `condition` row on a measured parameter, and building type is not a measured quantity, so it has no carrier.

**Evidence commands** (read-only, on `$SCRATCH/t.db`):

```
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True);print(c.execute('select parameter_id, count(distinct setting), sum(setting is null) from source_value_extractions group by 1').fetchall()); print(c.execute('select setting from source_value_extractions where parameter_id=9 and setting is not null limit 4').fetchall()); print(c.execute(\"select name from sqlite_master where name like '%building%' or name like '%room%'\").fetchall())" "$SCRATCH/t.db"
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/audit/joined_cells_census.py | grep -E 'source_value_extractions.setting|EXAMINED'
grep -n 'setting' scripts/assess/assess_cell.py
```

**Output on 2026-11-13:** every parameter with figures has several distinct `setting` values (parameter 3 also has many NULLs); door-width settings join construction status, building use and approach geometry in one cell (for example "new buildings; straight-on approach"); `rooms` is the only building-level object; the census flags `source_value_extractions.setting` as holding delimited values; the engine's only mention of the word is a docstring line about a rig setting, not the column. If a typed circumstance column or table already exists, stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8. **Do nothing** is the owner's option (a3): then this task is declined and nothing is built. Otherwise:

1. **Write `tasks/T-091-design.md` first** (an Opus-class session, from the owner's answer; the shape of `T-018-design.md`). It answers, against the live schema: which facets the answer types (building use; new or existing; interior or exterior; any other the answer names), each in its own column or link row (the 2026-11-06 schema-shape ruling: one value per cell, a foreign key where a table exists); where each facet's vocabulary lives (a base table with its rows added by data and a warrant, never a `choices=` list or a CHECK typed from examples: rule 8); under (a1) how the engine shows a branch per circumstance (T-017's branch partition is the model: `grep -n 'def conditioned_governing' scripts/assess/assess_cell.py`), and under (a2) how the determination's key widens (a change to the key ruled on 2026-08-26 and 2026-08-28, which the owner's answer then supersedes on contact: rule 0); under (b1) how the element level is derived from the element terms the catalogue holds (declined terms, the TERM-089 precedent), and under (b2) the `base_elements` table and which of the two homes points at the other; how `setting` is retired (writer-retire, reader-retire, NULL forward: rule 5's order, since committed data migrations INSERT it: `git grep -l -F '"setting"' -- 'scripts/migrations/data_*' | head -3`).
2. **Then build exactly what the design names**: the migration, the writer flags (`add-extraction` and `amend-extraction`), the engine's reading, the stage-map entry, and their refusals; `RULE_VERSION` derived and bumped if the engine changes.
3. **No row is re-tagged here** (T-092, research, rule 10).

**Chosen (authoring 2026-11-13):** one tooling task with a design file, held on the owner. Rejected: building a carrier now on the adjudication's option (a1) (the key of a determination and the base vocabulary are doctrine: CLAUDE.md §8 "jurisdiction, population taxonomy" and the 2026-08-26/28 rulings); a `condition` row standing for a building type (a condition row needs a measured value on a parameter, `extraction_relations` DDL: "this figure only holds given a second figure this project also holds as a row").

**What reads what this task adds:** the engine (the branch or the key); render (a determination shown per circumstance); T-092 (the re-tag); the coverage reads of T-090 if a facet is added to them. **What wrong thing reaches the guidebook without it:** a headline value that mixes dwelling and public-building figures, or new and existing work, for the same quantity and group. **What it makes deletable:** the free-text `setting` cell, once T-092 has re-tagged every figure.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `setting`, `--setting`, `rooms`, `base_building`.

**What a caller is.** A hit whose behaviour or truth changes with the carrier: a writer or reader of `setting`, a view that selects it, a skill sentence that says "applicability in `--setting`" (`grep -n -F 'applicability in `--setting`' skills/run-pipeline_SKILL.md`), a test. Left out: `workplan/` except `workplan/pipeline-state-graph/machines.yaml`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after.

## 6. Verification

Written by the design file (its after-tests, red before and green after, with a seeded defect for every new refusal), and at least: a figure whose circumstance is typed reaches only the branch (a1) or the determination (a2) of its circumstance, shown by the engine on a scratch copy with two `TASK-FIXTURE` figures of one parameter and lens that differ only in building use; `joined_cells_census.py` reports no new candidate; `migrate_db.py --rebuild` reproduces the database. The gate, once:
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: a figure's circumstance in typed cells, per OD-49 [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's answer and its ledger line; the design; evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before OD-49 is answered; do not build the part of another answer.
- Do not type a building-type vocabulary from examples into a CHECK or a `choices=` list; do not re-tag any stored figure (T-092).
- Do not drop `setting` (committed data migrations INSERT it; rule 5).
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: OD-49 is unanswered or answered in a form none of (a1), (a2), (a3), (b1), (b2) describes; a typed circumstance carrier already exists; the design needs a vocabulary the answer does not give; a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a compensating migration in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
