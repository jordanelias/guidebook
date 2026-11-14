# T-127  Give every stored code value its lens by contextual judgment, with its warrant (the one-time backfill)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the owner's instruction of 2026-11-14 (sixteenth set) and the statements that follow it (`grep -n -F "Owner instruction 2026-11-14 (sixteenth set)" references/project-standards.md`; `grep -n -F "(sixteenth set, later" references/project-standards.md`); the writer is T-126; with it this resolves `OPEN-ITEMS-PLAN.md` OI-72. Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the integrator of the sixteenth set. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-127 |
| Title | Give every stored code value its lens by contextual judgment, with its warrant (the one-time backfill) |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (Opus-class: a lens is judged from the clause and its context) |
| Traces to | OD-65; the sixteenth set and its four later statements (the moment of recording; mounting height; clearance height; any clearance); OD-31; OI-72 |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it). Every command uses `$BASE`.
- **Tasks that must be merged to the integration base first:** T-126 merged (the `context` warrant and `basis_reason`, and the recording guidance this batch applies to rows already stored). Check: `git log "$BASE" --format=%s | grep -c -E 'task/t-126-code-value-lens-at-recording|^T-126:|execute workplan T-126'` prints at least 1.
- **Owner decisions:** none as a gate. OD-65 is answered; the sixteenth set asks for this assignment. **OD-47 stays open**; a clause it concerns takes T-126's default derived from OD-31 (section 4 item 3), recorded as a default and replaced link by link if the owner answers otherwise.
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** the first evidence command of section 3 prints a count above 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-127-backfill-code-value-lenses "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-127" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: set `BASE`, `STEM` and `SCRATCH` again at the head of every block. **Real execution:** `/session-open`, then `/orient`; follow `skills/run-pipeline_SKILL.md` (the paragraph T-126 added). **Pilot:** no `/session-open`, scratch copy only, stop before the write path.
- Work only on the scratch copy: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Land the rows only by the write path:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another merged after you copied the database, `emit_batch_sql.py` refuses; start again from the new base.

## 3. The problem, in the guidebook's terms

The owner ruled that every code value carries a lens, assigned by contextual judgment when its row is recorded (OD-65; the sixteenth set). T-126 makes that true for rows recorded from now on. The code values already stored were recorded before it: every one carries only the `carried` links migration 131 moved from the retired columns, which have no judged warrant, and some carry `ALL`, which OD-31 removes from the identity lens. Until each is given its judged lens, the determination compares them under a lens no one judged.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select count(distinct x.extraction_id) from source_value_extractions x join evidence_sources e using(ref_id) where e.tier between 4 and 6 and not exists (select 1 from v_live_lens_links l where l.extraction_id=x.extraction_id and l.basis<>'carried')\").fetchone())"
python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select e.tier, sum(k.identity_code='ALL'), count(*) from v_live_lens_links k join source_value_extractions x using(extraction_id) join evidence_sources e using(ref_id) where e.tier between 4 and 6 group by 1\").fetchall())"
```

**Output on 2026-11-14:** the first printed `(144,)` (code values with no judged link); the second, the `carried` links per code tier and how many are `ALL`. If the first prints 0, the ground has moved: stop.

## 4. The change

1. **For each code value the first command lists**, read what the recording session would have had in front of it: the verified clause (`claim_text`) and its heading (`source_section`), the source's scope, application or purpose clause (re-open the saved file: `scripts/research/retrieval_log.py`), the figure's `setting` (or T-091's typed circumstance if merged by then: building type or use, interior or exterior), and the jurisdiction (it locates the code; it gives no lens).
2. **Judge its lens as T-126's guidance teaches**, one link per code, with `db.py add-lens-link`: `named_in_text` where the clause names the users, function or need; `heading` where its heading names the group (OD-31); otherwise `context`, `--basis-text` the source's words that state the context, `--basis-reason` the judgment. **The owner's worked defaults:** a mounting height, or any clearance (height, width, depth, clear floor or turning space, knee and toe clearance), takes the wheelchair-user lens with reason `typically concerns wheelchair users`, its codes derived by the commands in T-126 section 4 item 4, unless the clause names another group (an overhead or protruding-object clearance for people who are blind or have low vision takes that group).
3. **A clause whose context names no group and no default applies** (OD-47's case): T-126's default, no identity link and the ICF and access-need links of the function the clause serves, by `context`, the reason saying it is the default derived from OD-31 pending OD-47. Every code value receives a lens (OD-65); none is parked. List these rows in the pull request with their clause, so an answer to OD-47 can find them (`select link_id from v_live_lens_links where basis='context' and basis_reason like '%OD-47%'`, if the reason names it).
4. **Then retire the `carried` links** of the row with `retire-lens-link`, reason "replaced by the judged link(s) <ids>, T-127" (the verb refuses to retire a figure's last live link, so the judged links come first). **Except `ALL` links:** they stay for T-115, which retires them and then `ALL` itself (step 3 there); this batch does not retire the identity.
5. **Determinations:** a live specification resting on a figure whose lens changes is stale by its `derivation_sha`; it is re-derived by the engine in a later batch, never edited here. List them by command in the pull request: `select distinct specification_id from specification_extraction_links where extraction_id in (<the changed ids>)`.

**What reads what this task adds:** the engine's gather (T-019, through `v_live_lens_links`), and so T-059's selection and T-110's first determinations; T-115, which then retires only the `ALL` links; render. **Data migration.** Through `scripts/emit_data_migration.py`, which names the file; never type a migration name or number. No schema migration.

## 5. Caller sweep

A research task renames nothing; sweep only prose that restates a fact your rows change (rule 7a): `git grep -n -E 'carried' -- governance architecture references skills ':(exclude)references/project-standards.md'`, and correct a sentence the rows make false (or stop, if correcting it is not research). Report whether any live row still holds `carried` outside `ALL`; if none, say that `carried` can leave the CHECK after T-115 (a later tooling task, not this one).

## 6. Verification

**Red before, green after.** Before: the first command of section 3 prints a count above 0. After, on the migrated database: it prints `(0,)`; every new link has a basis other than `carried` and a non-blank `basis_text` (and `basis_reason` for `context`); every `carried` link left is an `ALL` link; the pull request lists each row with its basis, words and reason, and names the mounting-height and clearance rows that took the default (`select k.extraction_id, k.basis_text from v_live_lens_links k where k.basis='context' and k.basis_reason='typically concerns wheelchair users'`).

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Confirm the stem is the one on your rows: `python3 -I -c "import sqlite3,sys;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select count(*) from extraction_lens_links where created_by_session=? or retired_by_session=?',(sys.argv[1],sys.argv[1])).fetchone())" "$STEM"` is above 0.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: every stored code value given its lens by context, with its warrant [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the rows, their bases and reasons; the defaults applied; the OD-47 rows; the stale determinations listed>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not put tooling in this pull request: no schema migration, no new verb, no edit under `scripts/`, `schemas/`, `.github/` or `skills/` (rule 10).
- Do not write a lens without a warrant the source holds; do not use `named_in_text` for a judged lens; do not use `ALL`; do not retire an `ALL` link (T-115's) or the identity.
- Do not apply the worked defaults as a rule over the clause: where the clause names another group, that group is the lens.
- Do not write `data/guidebook.db` directly or hand-write SQL against a table a verb reaches. Do not re-key, move or edit a figure. Do not author a specification row.
- Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: T-126 is not merged; the evidence output differs; a clause cannot be re-read from a held artefact (its context would be guessed: report the row, do not link it); a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a data migration is append-only; correct a wrong link with a compensating batch (`add-lens-link`, then `retire-lens-link` with its reason), never by editing the file.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `db.py record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
