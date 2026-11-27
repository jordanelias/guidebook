# T-123  Each parameter with figures gets an accessibility direction read from an admitted source, or a gap saying none states one

> **NOT FOR SONNET** — Opus-class or above; which way is better for a disabled person is a judgment read from a source's own words, and the adversarial pass is owed. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: finding A4.2 of the adversarial pass on the remediation plan (`scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/AUDIT-FINDINGS.md`), re-verified 2026-11-14. Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the repair writer of the adversarial pass. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-123 |
| Title | Each parameter with figures gets an accessibility direction read from an admitted source, or a gap saying none states one |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | the contract criterion `base-direction-from-source` (`grep -n -A8 'id: base-direction-from-source' governance/pipeline-contract.yaml`); the owner's direction entry (`grep -n -F 'the minimum in some contexts may be the highest allowable number' references/project-standards.md`); `OPEN-ITEMS-PLAN.md`, which named parameters 5 and 9 and held no task |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none (the writer, `db.py set-parameter-direction`, exists and refuses a direction with no source or a source with no row for the parameter: `python3 scripts/db.py set-parameter-direction --help`).
- **Owner decisions:** none. The rulings it applies: a direction is read from an admitted source, never hand-set (the 2026-10-30 rulings, ACTION (6), quoted in the contract criterion above); the figures run in the parameter's accessibility direction, and a parameter with no recorded direction gets no minimum or maximum, only its identified values (the owner's direction entry).
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** the evidence query of section 3 prints at least one parameter.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-123-parameter-directions-from-sources "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-123" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db"
```
- Shell variables do not survive between tool calls: set `BASE`, `STEM` and `SCRATCH` again at the start of every block. **Real execution:** `/session-open`, then `/orient`. **Pilot:** skip `/session-open`, work on the scratch copy only, stop before the write path.
- Every write goes to the scratch copy, inline: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Land the rows only by the write path of CLAUDE.md §4, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```

## 3. The problem, in the guidebook's terms

The most accommodating value, the minimum and the maximum are all read in the parameter's accessibility direction; with no direction the engine states no value (`grep -n -A4 'if direction is None:' scripts/assess/assess_cell.py`). Most parameters that hold figures have no direction recorded, so the first live determinations (T-110) could state a value for very few of them, and nothing in the plan records the rest.

**Evidence command** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print('no direction, with figures:',c.execute('select p.parameter_id, t.canonical_en, count(x.extraction_id) from base_parameters p join terms t using(term_id) join source_value_extractions x on x.parameter_id=p.parameter_id where p.accessibility_direction is null group by 1,2 order by 1').fetchall());print('direction, no source:',c.execute('select parameter_id, accessibility_direction from base_parameters where accessibility_direction is not null and direction_ref_id is null').fetchall())"
```

**Output on 2026-11-14:** six parameters without a direction that hold figures (ids 4, 5, 6, 8, 9 and 11 printed, each with its count), and parameters 3 and 12 with `lower_is_better` and no source (history, recorded before `direction_ref_id` existed). If the output differs, the ground has moved: stop (section 9).

## 4. The change

1. **For each parameter the first list prints**, read the held sources that carry its figures (`select x.extraction_id, x.ref_id, e.tier, x.claim_text from source_value_extractions x join evidence_sources e using(ref_id) where x.parameter_id = ?`) and, where a source **states** which way is better for a disabled person (in its own words: a floor framed as a minimum, a ceiling framed as a maximum the user needs not exceeded, or a sentence saying more or less is easier), record it with `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py set-parameter-direction --parameter-id <id> --direction <from --help> --rationale "<why, for a disabled person, in the source's terms>" --ref-id <the source> --session "$STEM"`. The source must hold an extraction for the parameter (the writer refuses otherwise). Choose `contested` only where held sources state opposite directions for different groups (DR-2026-07-21 section 5), and name both.
2. **Where no held source states a direction**, record nothing in `base_parameters` (NULL stays) and write a gap through `db.py add-gap` naming the parameter and the missing direction, in a category from the live CHECK (`dbcore.schema_choices("gaps", "category")`; choose with a cited precedent use, as T-068 item 6 does). Never infer a direction from the parameter's name, its unit, the code stratum's habit or the values' spread (rule 8).
3. **Parameters 3 and 12** (a direction with no source): if the writer accepts a call on a parameter that already has a direction, record the source the direction is read from; if it refuses, leave them as history and list them. Do not change a direction a source does not support.
4. List in the pull request, per parameter: the direction and the source's words, or the gap and the search that found none.

**What reads what this task adds or changes:** the engine (`determine`, `_compose_headline`), T-059's selection, T-124's four figures, render, and T-110. **What wrong thing reaches the guidebook without it:** the first determinations state no value for most parameters that have evidence, and nothing says why.

**Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number, and never edit the file it writes. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a): `git grep -n -i -E 'parameters? (5|9)\b.*direction|no direction' -- governance architecture references skills ':!references/project-standards.md' ':!references/search-log'`; correct a sentence your rows make false, or stop if that is not research.

## 6. Verification

**Red before, green after.** The first list of section 3 prints, after the migration is applied, only parameters that carry an open gap this batch wrote; every direction recorded has a `direction_ref_id`. `research_batch_dod.py --session "$STEM"` prints non-zero `EXAMINED:` lines.

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Confirm the stem is the one stored on your rows: `select count(*) from base_parameters where updated_by_session=?` and the same on `gaps` with `created_by_session`, both above 0 together.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: parameter directions read from sources [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: per parameter, the direction with its source's words, or the gap; the gates with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not set a direction no admitted source states; do not hand-write SQL; do not write `data/guidebook.db` except through the write path.
- Do not put tooling in this pull request (CLAUDE.md rule 10); a writer gap found is filed and left.
- Do not author a specification row; do not decide doctrine. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the evidence output differs; a direction would need a guess; held sources state opposite directions and `contested` would hide a group; the writer refuses in a way its help does not explain; a gate green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a compensating migration through the same verbs, never an edit to the file.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
