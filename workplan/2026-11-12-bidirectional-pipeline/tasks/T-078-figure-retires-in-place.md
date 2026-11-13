# T-078  A figure retires in place

> **NOT FOR SONNET** — Opus-class or the Fable implementation agent. Section 4 item 3 asks, for every reader of `source_value_extractions`, whether a retired figure belongs in what it shows (a history view should keep it, a gather must drop it); that is a judgment per reader, not a mechanical edit. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting for an Opus-class session.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 (AT-18), probe in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/R2-probes.md` (section AT-18). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13; the R2 probe was re-run on that day's HEAD. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-078 |
| Title | A figure retires in place |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | AT-18 ("Retiring a source, a figure, a parameter and a determination leaves each row present with a status", `grep -n 'AT-18' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`); REQ-018; the owner's ruling "retire in place then" (`grep -n -F 'retire in place then' references/project-standards.md`) and its execution condition (`grep -n -F 'No row is retired in place until every reader' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none. (T-018's `extraction_lens_links` and `v_live_lens_links`, and T-019's gather in `assess_cell.py`, which this task reads, are merged on 2026-11-13: `git log "$BASE" --oneline | grep -F 'task/t-019-lens-gather'`.) T-050 retires admission edges and connections with the same column shape; if it merged first, reuse its writer helper rather than writing a second one, and say so.
- **Owner decisions:** none in the register. The ruling is the owner's ("retire in place then", 2026-09-16), covering "DATA ROWS AND IDENTIFIERS"; a figure is a data row. Its execution condition binds this task: no figure is retired until every reader that could surface it filters on status. One related owner question is open and this task does not wait for it: OI-55 (7), whether `add-lens-link` and `retire-lens-link` refuse while a live determination uses the figure. This task makes `retire-extraction` refuse in that case (section 4, item 2, Chosen); if the owner answers OI-55 (7) the other way, the same answer applies here and is a one-condition change.
- **Tests that must be red before you start:** AT-18 for the figure, restated in section 6.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-078-figure-retires-in-place "$BASE"    # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-078" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A figure read from a source can turn out wrong (misread, superseded by a correction, filed against the wrong parameter). Sources, parameters and determinations each have a retire-in-place path; a figure has none, so the only way to withdraw one is a hard delete, which loses the fact that the figure was once claimed and which determinations it fed. That has happened: a data migration deleted figures outright (`git grep -l -i -E 'DELETE FROM "?source_value_extractions' -- scripts/migrations`; on 2026-11-13 it names `data_20260913040739_2026-09-13-clear-circulation-corpus.sql`), and the gap in `extraction_id` shows it.

**Evidence commands** (read-only):

```
grep -n -E '"retire-[a-z-]+"|"supersede-source"' scripts/db.py | grep add_parser
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(source_value_extractions)') if 'retir' in r[1] or 'status' in r[1]]);print(c.execute(\"select (select seq from sqlite_sequence where name='source_value_extractions'), count(*), max(extraction_id) from source_value_extractions\").fetchone());print(c.execute('select count(*) from specifications where retired_at is null').fetchone())"
python3 -I -c "import sys;sys.path.insert(0,'scripts');import dbcore,sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(sorted(dbcore.deletable_tables(c)))"
```

**Output on 2026-11-13:** the `add_parser` lines name `retire-specification`, `retire-parameter`, `retire-lens-link` and `supersede-source`, and no figure verb; the only status-like column is `extraction_status` (review state: `preliminary`, `reviewed`, `verified`, `contradicted`, `absent-confirmed`, not retirement); `(227, 214, 227)` (sequence, rows, max id: ids were used and are gone); `(0,)` live determinations; `source_value_extractions` is not in `deletable_tables` (the sanctioned path already refuses a delete, so the defect is the missing retire path, not a missing refusal).

**The other half of AT-18 is not this task's.** "The next identifier issued is higher than any ever used" holds for `extraction_id`, `parameter_id` and `specification_id` (AUTOINCREMENT). For `ref_id`, a hard delete of the highest source makes `dbcore.next_ref_id` fall back, but the sanctioned path refuses the delete (`emit_batch_sql.py` refuses rows missing from the scratch, and `evidence_sources` is not in `deletable_tables`) and the blocking `identifier_floor_audit` goes red on it (probe on a scratch copy, 2026-11-13: `VERDICT: FAIL … ref_id floor REGRESSED`). That half is guarded; no task.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Schema migration: three nullable columns on `source_value_extractions`**: `retired_at TEXT`, `retired_by_session TEXT`, `retirement_reason TEXT`, added with `ALTER TABLE … ADD COLUMN` (the shape `specifications`, `extraction_lens_links` and T-050's tables use: `PRAGMA table_info(extraction_lens_links)`). Two triggers, in the shape of `trg_spec_retire_needs_reason` (`grep -n -A7 'CREATE TRIGGER trg_spec_retire_needs_reason' scripts/migrations/083_specification_retire_in_place.sql`): one refuses `retired_at` set without a non-blank `retirement_reason` and `retired_by_session`; one refuses clearing `retired_at` once set (no un-retiring: a wrong retirement is answered by a new figure). **Chosen (authoring 2026-11-13):** columns plus triggers, not a status value in `extraction_status` (that column says how far a figure has been reviewed; retirement is a different fact, and one cell holds one fact: CLAUDE.md §4, owner 2026-11-06), and not a create-copy-drop-rename with a CHECK (the table carries views and an inbound pointer from every judgment table; the triggers refuse every writer and cost no rebuild).
2. **`db.py retire-extraction --extraction-id N --reason TEXT --session S`**, writing the three columns in one UPDATE. Refuses: an unknown id; a figure already retired; a blank reason; **a figure linked from a LIVE determination** (`specification_extraction_links` joined to `specifications` with `retired_at IS NULL`), naming each determination and the next act (`retire-specification` first, then re-run), in the shape of `_refuse_live_work` (`grep -n 'def _refuse_live_work' -A25 scripts/db.py`). **Chosen (authoring 2026-11-13):** refuse while a live determination uses the figure, as `retire-parameter` does for its parameter; rejected: retiring and letting the stale-determination check report it (a determination would then cite a withdrawn figure until someone re-runs). No live determination exists today (evidence), so the refusal changes no present act. `amend-extraction` and `relate-extraction` refuse a retired figure (one guard each, the message naming `retire-extraction`'s history).
   **Lens links and relations are not touched by the verb.** `v_live_lens_links` is rebuilt to exclude links whose figure is retired (one view; every reader of it inherits the filter). `extraction_relations` rows stay as history; readers that walk an edge into a retired figure drop it (item 3). **Chosen (authoring 2026-11-13):** filter by pointer, not by retiring the link rows too: retiring the links would write the same fact (the figure is withdrawn) into a second table, which rule 5 forbids.
3. **Every reader that could surface a figure filters on `retired_at IS NULL`, or says in a comment why it keeps history** (the ruling's execution condition). Derive the readers, do not trust a list: the views (`select name from sqlite_master where type='view' and sql like '%source_value_extractions%'`; on 2026-11-13: `v_derived_figure_check`, `v_determination_provenance`, `v_root_id_conflicts`, `v_scan_ledger`, `v_unregistered_roots`, `v_value_independence`) and the code (`git grep -l -F 'source_value_extractions' -- scripts ':(exclude)scripts/migrations' ':(exclude)scripts/tests'`; on 2026-11-13 eleven files, including `assess/assess_cell.py`, `db.py`, `dbcore.py`, `audit/research_batch_dod.py`, `audit/verified_scan_integrity.py`, `audit/adjudication_integrity.py`). For each, decide and record in the pull request one of: **filters** (a gather, a count of what is live, a ledger status, a coverage figure, the engine's `count_extractions` and every `gather_*` that `_lens_clause` serves); **keeps history, says so** (a provenance view of a retired determination, an audit whose subject is every row ever written). `v_scan_ledger`'s EXTRACTED and STATED-ABSENT statuses must not be earned by a retired figure (a pair whose only figure is retired goes back to its reading status). `test_db_integrity` K02 ("every figure of the parameter is accounted for") counts live figures only.
4. **No figure is retired by this task.** The pull request adds the path and the filters; it contains no `scripts/migrations/data_*` file.

**Schema migration (this task has one).** Never type a migration number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, in `scripts/migrations/NNN_figure_retire_in_place.sql`, ending with `PRAGMA user_version` set to the same number. A view is changed by `DROP VIEW` then `CREATE VIEW` in the same migration. Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). Run `python3 scripts/audit/joined_cells_census.py` before and after (no new candidate). After the migration, run `python3 scripts/generate/context_map.py` and include its output.

**What reads what this task adds:** the engine's gather and `count_extractions` (a retired figure stops feeding a determination); `v_scan_ledger` and every coverage reader; T-005's retired-row fixture (AT-19), which gains a retired figure as a kind once this merges (the coordinator updates T-005); a research session that finds a wrong figure. **What it makes deletable:** nothing today; it removes the reason a future session would hard-delete a figure.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `source_value_extractions`, `v_live_lens_links`, `amend-extraction`, `relate-extraction`, `extraction_id`, `count_extractions`, `_lens_clause`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code or a view that reads figures and would surface a retired one; a test that counts figures or builds a `source_value_extractions` fixture from the live DDL (a fixture built from the DDL gains three columns; one that inserts by position breaks); a registry entry; a skill or governance sentence that says a figure is withdrawn by deletion or cannot be withdrawn. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds a verb: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (its failure count on the base is the base state; only a count above your before-run is yours). `skills/run-pipeline_SKILL.md` names the judgment verbs: add `retire-extraction` where it lists how a figure is corrected, if it lists that.

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_assess_cell_pilot test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_db_integrity verified_scan_integrity schema_reference_audit migration_reproducibility"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
If a name in `CHECKS` is not a registry id on the day (`python3 scripts/run_checks.py --list | grep <name>`), drop it and say so. Checks red here (on 2026-11-13: `test_scan_contract` G01/G02, `verified_scan_integrity`) were red before you: record and carry on. `test_assess_cell_pilot` prints no `EXAMINED:` line unless T-075 has merged: count its `PASS:` lines.

**Step 2: red before, green after** (cases `T078-01`…, prefix free: `git grep -c 'T078-' scripts/tests/`):
- `T078-01` AT-18 for a figure: on a scratch copy, pick a figure by query (one not linked from any live determination: `select extraction_id from source_value_extractions where extraction_id not in (select l.extraction_id from specification_extraction_links l join specifications s using(specification_id) where s.retired_at is null) order by 1 limit 1`); `retire-extraction` it; the row count is unchanged, `retired_at`, `retired_by_session` and `retirement_reason` are set. Red before (no verb: argparse error; assert stderr starts `REFUSING:` or the verb is unknown, so an absent verb cannot pass).
- `T078-02` refusals: blank reason; unknown id (`select coalesce(max(extraction_id),0)+1 …`); already retired; un-retire by raw UPDATE refused by the trigger.
- `T078-03` a live determination links the figure: build one on the scratch copy through the engine (or a raw insert into `specifications` and `specification_extraction_links` labelled `TASK-FIXTURE`) and show the refusal names it.
- `T078-04` the readers: after retiring a figure, the engine's gather for its parameter and lens no longer counts it (`count_extractions` falls by one), `v_live_lens_links` no longer lists its links, and `v_scan_ledger` gives its pair the reading status it would have had with no figure. Seeded defect: remove the filter from one `gather_*` on a copy of the code; the case goes red; restore.
- `T078-05` `amend-extraction` on a retired figure is refused.

**Fixtures** go to a copy, are labelled `TASK-FIXTURE`, and never reach `data/guidebook.db`.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail; an `EXAMINED:` number may change only by cases you added or by retired figures you created on a copy (none on the canonical database).

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` changes only by the migration, and the rebuild reproduces it.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: a figure retires in place (AT-18) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: evidence before and after; the reader table (filters / keeps history, why); callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not retire, delete or amend any figure on the canonical database.
- Do not put retirement into `extraction_status`, a note, or any second table.
- Do not drop a reader's history view to make it filter; a history view says it keeps retired rows.
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.
- Do not type an id or a count into a test; derive it.

## 9. Stop conditions

Stop and report when: the evidence output differs from section 3; a reader cannot be made to filter without changing what a live check asserts; the owner has answered OI-55 (7) in a form that contradicts item 2's refusal (apply the answer only if it is in the ledger in the owner's words); a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a compensating migration in a new pull request; committed migrations are never edited.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (ask the critic to attack the reader table first); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push. One pull request merges at a time; re-derive the migration number after `git merge "$BASE"` if another merged first.
