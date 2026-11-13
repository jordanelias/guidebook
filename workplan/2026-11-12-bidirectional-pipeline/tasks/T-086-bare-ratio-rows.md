# T-086  The stored gradients whose unit says only `ratio`

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` (`### OD-41`). Carved out of T-108 on 2026-11-13 so that OD-41 holds only these rows and not the rest of T-108 (`tasks/T-108-unit-condition-repair.md`, its "Owner decisions" bullet). Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-57, item (13), and T-061 section 4, "Not built here" (`grep -n -F 'Not built here' workplan/2026-11-12-bidirectional-pipeline/tasks/T-061-amend-extraction-reformat.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class plan integrator). Its evidence command was run on a scratch copy and printed what section 3 states; no row was written. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-086 |
| Title | The stored gradients whose unit says only `ratio` |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (Opus-class): under either answer each row is re-read against its source to confirm the figure is a rise over a horizontal run, a judgment on the text, not a mechanical step |
| Traces to | OD-41; OI-57 item (13); the prior workplan's D-1 (`grep -n -F 'D-1' workplan/2026-10-23-pipeline-resolution-workplan.md`); OR-3 (`grep -n -F 'OR-3: "Yes, reformat in place"' references/project-standards.md`); D-0168 as OR-3 narrows it (`grep -n -F 'Reformatting a figure' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-061 merged (its `_refuse_unless_reformat` is the verb under answer (a), and the screens it reuses are what answer (b)'s rows must pass). T-093 merged under answer (a): the one-branch follow-up to T-061 that T-061 names and does not build (accept a new unit that is a member of `dbcore.NOTATION_FAMILIES` when the old unit stands, on word boundaries, in the new one and the stored figure reads under it), authored 2026-11-13 as `tasks/T-093-ratio-unit-reformat-branch.md` and held on OD-41. The plan's generator reads T-093 here as a hard dependency under both answers; under answer (b) T-093 is declined, and the coordinator who folds the answer deletes `T-093` from this bullet in the same edit. Check by running: `GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py amend-extraction --extraction-id "$(python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select min(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone()[0])")" --field claimed_unit --value 'rise:run ratio' --reason probe --session session_probe --dry-run 2>&1 | tail -1`: under (a) it must not be refused; under (b) it is refused and that is expected.
- **Owner decisions:** OD-41 (OPEN, registered 2026-11-13, not yet asked): is changing the unit `ratio` to `rise:run ratio` on the stored rows a reformat (OR-3) or a new reading (a second row, D-0168)? Read the answer by `grep -n -F "OD-41" references/project-standards.md | tail -3`; do the part of section 4 that the answer names, and nothing of the other.
- **Open owner question bearing on part of this task (not its gate):** OQ-T086, registered 2026-11-13 as OD-55: under OD-41 (b), is the stored bare-`ratio` row retired in place under T-078 once its second reading is written, or are both rows left? Section 4 item 2 writes the second rows and retires nothing until it is answered (`grep -F "OD-55 STATUS:" references/project-standards.md | tail -1`). Under (a) it does not arise.
- **Tests that must be red (or green) before you start:** the after-test of section 6 is red (it prints the ids).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-086-bare-ratio-rows "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-086" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
```
- **Shell variables do not survive from one tool call to the next in this harness.** Write the stem down once and begin every later command block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** open with `/session-open`, then `/orient`. Follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run** (a scratch clone): skip `/session-open`, stay on the branch you were given, do the work on the scratch copy only, and stop before the write path below.
- Work only on the scratch copy and point every call at it inline: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`.
- Land the rows only by the write path, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another research batch merged after you copied the database, `emit_batch_sql.py` refuses ("copied from a different base"). Do not force it; start again from the new base.

## 3. The problem, in the guidebook's terms

Some stored ramp-gradient figures are written `1:12` with the unit cell holding only `ratio`. The engine reads an `a:b` figure only under `rise:run ratio` (rise over horizontal run: a gradient), so it leaves these out of the value and lists them in the cell's note as "no parsable numeric bound". `ratio` alone does not say which run is meant, and whether filling that in is a reformat of the stored row or a new reading of the source is the owner's question OD-41.

**Evidence command** (on a scratch copy, read-only):

```
cp data/guidebook.db "$SCRATCH/r.db"
python3 -I - "$SCRATCH/r.db" <<'PY'
import sqlite3, sys
sys.path.insert(0, 'scripts'); import dbcore
c = sqlite3.connect(f'file:{sys.argv[1]}?mode=ro', uri=True); c.row_factory = sqlite3.Row
rows = c.execute("SELECT * FROM source_value_extractions WHERE claimed_unit='ratio' ORDER BY extraction_id").fetchall()
print('bare ratio rows', [r['extraction_id'] for r in rows])
print('values', sorted({r['claimed_value'] for r in rows}), '| all a:b:', all(':' in (r['claimed_value'] or '') for r in rows))
print('sources', sorted({r['ref_id'] for r in rows}), '| parameters', sorted({r['parameter_id'] for r in rows}))
print('role/type/comparator', sorted({(r['figure_role'], r['claim_type'], r['comparator']) for r in rows}, key=str), '| status', sorted({r['extraction_status'] for r in rows}))
print('engine refuses the figure today:', sum(dbcore.figure_refusal(r['claimed_value'], r['claimed_unit'], r['comparator'], r['claim_type']) is not None for r in rows), 'of', len(rows))
print('under rise:run ratio it would read:', sum(dbcore.figure_refusal(r['claimed_value'], 'rise:run ratio', r['comparator'], r['claim_type']) is None for r in rows), 'of', len(rows))
print('live determinations on those parameters:', c.execute("select count(*) from specifications where retired_at is null and parameter_id in (select parameter_id from source_value_extractions where claimed_unit='ratio')").fetchone()[0])
PY
rm -f "$SCRATCH/r.db"
```

**Expected output today** (2026-11-13): a list of ids, all on one parameter (3, ramp gradient) and from three sources; every value is `a:b`; roles `claim` and `finding`, comparators `<=`, `=` and none, status `reviewed` or `verified`; the engine refuses every one today and would read every one under `rise:run ratio`; no live determination on the parameter. The query is T-061's (`SELECT extraction_id FROM source_value_extractions WHERE claimed_unit='ratio'`, its section 4, "Not built here"). The ids are not the contiguous range the prior D-1 table named: derive them, never copy them.

If the output differs, the ground has moved: stop (section 9). Where a later command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves these figures out of every ramp-gradient cell. No code: under either answer the verbs exist once the preconditions hold.

0. **Under either answer, first read each row against its source.** For each id of section 3, read the row's `claim_text` and `source_section` against the source's saved text (`python3 scripts/research/retrieval_log.py` and the source's held artefacts: `artefacts_for_source(<ref_id>)`), and confirm that the figure is a rise over a **horizontal** run, the meaning `rise:run ratio` names. A row whose source does not say, or says the run is along the slope, is left as it is and listed in the pull request with the sentence that shows it (section 9). **Chosen (authoring 2026-11-13):** this reading is the task's, under both answers. Rejected: assuming every `1:n` ramp figure is rise over horizontal run (most are, but the unit is the only place the meaning is stated; a wrong unit would let the engine compose a figure on the wrong scale).
1. **Under answer (a), a reformat (OR-3).** For each confirmed row: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py amend-extraction --extraction-id <id> --field claimed_unit --value 'rise:run ratio' --reason "OD-41 (a): the stored ratio is rise over horizontal run (<the source's words, quoted>)" --session "$STEM"`. The value, quote and locator do not change; the writer keeps the old unit in notes by its own marker. Nothing else is written.
2. **Under answer (b), a new reading (D-0168).** For each confirmed row: one new row through `db.py add-extraction`, carrying the stored row's `ref_id`, `parameter_id`, `claim_text`, locator fields, `comparator`, `figure_role`, `claim_type`, lens columns and `claimed_value` unchanged, with `claimed_unit` `rise:run ratio`; an `extraction_status` the writer accepts for it (a `verified` row needs a full-scope reading covering the parameter, OR-11a: otherwise `reviewed`, as the stored row is). The stored row is not changed. **Owner question raised here (OQ-T086, registered as OD-55):** under (b) the stored row stays and stays unreadable, so the engine reads one figure per pair, but its value note's count of governing claims counts both rows. Whether the stored row is to be retired in place (T-078 builds that verb) is not answered by OD-41's option (b) as registered; if the owner's answer does not say, ask, and do not retire anything here.
3. **Neither answer reaches another row.** Rows whose unit cell holds a sentence or a condition are T-108's; extraction 80's spelled-out figure is T-111's.

**What reads what this task changes:** the engine (`assess_cell` through `dbcore.bound_on_scale` and `dbcore.figure_refusal`), which then reads these figures into parameter 3's cells; T-110 (the first live determinations), downstream. **Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number, and never edit the file it writes. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a). For each row id or value you change, search the reading surface and the governance prose, and correct a sentence your rows make false (or stop, if correcting it is not research):

```
V='<the id, code or value you changed>'
git grep -n -F -e "$V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

Structures this task touches, for orientation: `source_value_extractions.claimed_unit` (answer (a)), new `source_value_extractions` rows (answer (b)). The ledger, `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**The after-test, by answer** (run on `$SCRATCH/t.db` before the work, on `$SCRATCH/s.db` after it, then on the canonical database after the migration):
- (a): `python3 -I -c "import sqlite3,sys;print(sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True).execute(\"select group_concat(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone()[0])" <db>` prints `None`, or only the ids section 4 item 0 left with a reason. **Red before:** it prints section 3's ids.
- (b): `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True);print(c.execute(\"select o.extraction_id, count(n.extraction_id) from source_value_extractions o left join source_value_extractions n on n.ref_id=o.ref_id and n.parameter_id=o.parameter_id and n.claim_text=o.claim_text and n.claimed_value=o.claimed_value and n.claimed_unit='rise:run ratio' where o.claimed_unit='ratio' group by 1 having count(n.extraction_id)<>1\").fetchall())" <db>` prints `[]`, or only the ids left with a reason (each stored row has exactly one new reading). **Red before:** it prints every id with count 0.
- **Seeded defect, on `$SCRATCH/t.db` only:** (a) try `amend-extraction --field claimed_value` on one of the rows with a changed digit (`1:20` to `1:2.0`, chosen by query): the writer must refuse (OR-3 keeps the numbers); (b) write the same new reading twice for one row: the second write is refused as a duplicate, or, if it is not, the (b) after-test prints that id with count 2. Report which.
- **The engine, before and after:** `python3 scripts/assess/assess_cell.py --db "$SCRATCH/e.db" --emit-sql "$SCRATCH/e.sql" --parameter-id 3 --slug accessible-circulation-geometry --identity MOB --session session_task-probe --stamp '2026-01-01 00:00' --report-json "$SCRATCH/e.json"` on a fresh copy of `t.db` (before) and of `s.db` (after); quote both reports' `value_note` in the pull request. After, no section 3 id is among the claims with "no parsable numeric bound" except one left with a reason (and, under (b), the stored row of each pair, per OQ-T086).

**Fixtures.** Probes run on `$SCRATCH/t.db`; the batch's own rows are written on `$SCRATCH/s.db` and reach `data/guidebook.db` only through the write path of section 2.

**The gates, once each:**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8   # the research gate
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- Run each once, after the migration is applied and before the commit. Confirm the stem is the one stored on your rows: `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from source_value_extractions where created_by_session=? or updated_by_session=?',(sys.argv[1],sys.argv[1])).fetchone())" "$STEM"` is above 0. `migration_reproducibility` compares row counts only, so an UPDATE (answer (a)) is invisible to it: also run `python3 scripts/audit/migration_reproducibility.py --deep`.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: the stored ramp gradients whose unit says only ratio, under OD-41 [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: OD-41's answer and its ledger line; the rows, each with the source sentence that shows a horizontal run; rows left and why; the engine's value_note before and after>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before OD-41 is answered, and do not do the other answer's part.
- Do not change a digit, a quote or a locator. Do not retire, supersede or delete a stored row (OQ-T086).
- Do not build the follow-up branch of T-061 here (tooling, rule 10).
- Do not write `data/guidebook.db` directly; do not hand-write SQL against a table a `db.py` verb can reach.
- Do not decide doctrine; do not treat any `[A-Z]-NN` code as a container. Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.
- Do not hand-type a count into any file or message; write the command that computes it.

## 9. Stop conditions

Stop, change nothing further, and report when: OD-41 is unanswered, or answered in a form neither (a) nor (b) describes; under (a), the precondition's dry run is refused (the follow-up branch is not merged); under (b), the owner's answer does not say what becomes of the stored row and the engine's report counts both (OQ-T086: ask); section 3's command prints a row that is not `a:b`, or a parameter other than one, or a live determination; a row's source does not show a horizontal run (leave it, list it with the sentence); a check green in the before-run is red after; the rebuild does not reproduce the database; you would have to guess a value, a unit or the owner's intent.

## 10. Rollback

Before the migration is applied: delete the scratch copy; nothing has changed. After it is committed: a data migration is append-only and immutable; correct a wrong row with a compensating migration written through the same verbs, never by editing or deleting the file.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7. `/adversarial` once on the finished diff (for a research task the pass is recorded with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
