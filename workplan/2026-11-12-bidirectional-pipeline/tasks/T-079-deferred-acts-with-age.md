# T-079  A deferred reading is recorded, and every deferred act lists with its age from one view

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 (AT-17), probe in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/R2-probes.md` (section AT-17). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13; the R2 probe was re-run on that day's HEAD. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-079 |
| Title | A deferred reading is recorded, and every deferred act lists with its age from one view |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | AT-17 ("The set of deferred acts (mining, searches, readings) older than a stated age can be listed by one query", `grep -n 'AT-17' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`); REQ-036; the owner's "deferred is okay so long as it runs eventually" (`grep -n -F 'deferred is okay so long as it runs eventually' references/project-standards.md`) and the ledger's own finding beneath it that "nothing in this repository enforces it or even measures it" |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. The ruling is the owner's (2026-09-18): a deferral is legitimate "so long as it runs eventually", and for mining "the execution signal already exists and it is `evidence_sources.citation_mining_status`" (`grep -n -F 'The execution signal already exists' references/project-standards.md`). Extending the record to readings is AT-17's reading of REQ-036 ("by extension every owed act"); it adds no doctrine: a deferred reading is still owed, and the scan ledger still lists the pair as unread.
- **Tests that must be red before you start:** AT-17, restated in section 6.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-079-deferred-acts-with-age "$BASE"              # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-079" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A deferred act is a promise to go back: a search not run, a source not mined, a source not read. The owner allows deferral on the condition that the act eventually runs. Searches and mining record their deferrals with a date; a reading has no deferred state at all, so "we chose not to read this yet" cannot be told from "nobody has looked", and no query lists all three with their age. A deferral that is never discharged is indistinguishable from one taken last week.

**Evidence commands** (read-only):

```
python3 - <<'PY'
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('search deferrals', c.execute("select count(*) from search_executions where deferred_reason is not null").fetchone()[0])
print('mining deferrals standing', c.execute("select count(*) from citation_mining cm join evidence_sources e on e.ref_id=coalesce(cm.global_ref_id,cm.local_ref_id) where cm.deferred_reason is not null and e.citation_mining_status='deferred'").fetchone()[0])
print('source_scans columns with defer/status', [r[1] for r in c.execute('pragma table_info(source_scans)') if 'defer' in r[1] or 'status' in r[1]])
print('v_scan_ledger columns', [r[1] for r in c.execute('pragma table_info(v_scan_ledger)')])
print('ledger statuses', c.execute('select status,count(*) from v_scan_ledger group by 1').fetchall())
print('views over deferrals', [r[0] for r in c.execute("select name from sqlite_master where type='view' and name like '%defer%'")])
PY
```

**Output on 2026-11-13:** `search deferrals 1`; `mining deferrals standing 13`; `source_scans columns with defer/status []`; `v_scan_ledger columns ['ref_id', 'parameter_id', 'status', 'scan_id', 'text_scope', 'method']` (no date); statuses `EXTRACTED`, `NOT-READ`, `READ-NOTHING-FOUND`, `READ-PARTIAL`, `STATED-ABSENT` (no deferred one); `views over deferrals []`. A union over searches and mining with an age filter runs today (the R2 probe's), but a reading cannot enter it.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Schema migration: a table `reading_deferrals`** (`deferral_id INTEGER PRIMARY KEY AUTOINCREMENT`, `ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id)`, `parameter_id INTEGER REFERENCES base_parameters(parameter_id)` (NULL: the whole-source catalogue reading), `reason TEXT NOT NULL CHECK (trim(reason) <> '')`, `created_at TEXT NOT NULL`, `created_by_session TEXT NOT NULL`). Add it to `governance/stage-map.yaml` as `evidence` (beside `source_scans`, which the map puts there: `grep -n 'source_scans' governance/stage-map.yaml`).
   **Chosen (authoring 2026-11-13):** a table of its own. Rejected: (a) a row in `source_scans` (its `file_sha256 NOT NULL` and `text_scope` describe a reading that happened; a deferral is the opposite fact); (b) `evidence_sources.data_capture_status = 'deferred'` (per source only, no date and no reason, and a column a data migration INSERTs, CLAUDE.md rule 5); (c) a new `v_scan_ledger` status (the pair stays owed until it is read, and the gates that read the ledger's statuses would change meaning). The deferral is **discharged by derivation, never by a write**: a `full` reading in `source_scans` that covers the pair (catalogue mode with `catalogue_version >= parameter_id`, or targeted at it; for a NULL parameter, any full catalogue reading of the source) and is dated after the deferral.
2. **`db.py defer-reading --ref-id R [--parameter P] --reason TEXT --session S`.** Refuses: a source that does not exist or is superseded (`superseded_by_ref_id IS NOT NULL`: the replacement is what is owed); a parameter that is not active; a blank reason; a pair a full reading already covers (nothing is owed); a pair that already has an undischarged deferral. Reuse the existing helpers for each (`_parameter_row`, `dbcore.require_reason`, the source lookups `record-scan` uses, including its tombstone refusal `_refuse_tombstone`: `grep -n 'def record_scan' -A60 scripts/db.py`).
3. **A view `v_deferred_acts`** with columns `kind` (`search`, `mining`, `reading`, `adjudication`), `subject` (the exec id; the mined `ref_id` and slug; the `ref_id` and parameter; the observation id, its `ref_id` and surface form), `reason`, `deferred_at`, `created_by_session`, listing **only standing deferrals**:
   - searches: `search_executions` with `deferred_reason IS NOT NULL`, dated `created_at`. A deferred search has no discharge pointer today (a search later run is a new row that names nothing it discharges), so every search deferral lists; say so in the view's header comment.
   - mining: `citation_mining` rows with `deferred_reason IS NOT NULL` whose source's `citation_mining_status` is still `deferred` (the owner's home for the execution signal), dated `citation_mining.created_at`.
   - readings: `reading_deferrals` with no discharging reading (item 1).
   - **adjudications** (kind `adjudication`; added 2026-11-13 by the fold of the Edmonton case study, ADJUDICATION P3 and R4): every observation whose **latest** adjudication (`max(adjudication_id)` per `observation_id`, the rule T-069 and T-074 select by) has outcome `DEFERRED`; `subject` is the observation id with its source (`observed_terms.ref_id`) and surface form, `reason` the adjudication's `rationale`, `deferred_at` the adjudication's `created_at`, `created_by_session` its session. It is discharged by derivation, never by a write: a later adjudication of the same observation with another outcome makes it no longer the latest, so the row leaves the view. The outcome is matched as the literal of the column's own CHECK; confirm it is still one of `dbcore.check_values(conn, 'term_adjudications', 'outcome')` in a test (`T079-05`), so a renamed outcome turns the test red rather than emptying the arm.
     **Chosen (fold 2026-11-13):** a fourth arm of the same view. Rejected: a table or queue of candidates (the deferred adjudications are already rows; what was missing is one read, ADJUDICATION Q3), and a separate view (one owner sentence, "deferred is okay so long as it runs eventually", governs all four kinds).
   **Chosen (authoring 2026-11-13):** the date is when the obligation was first recorded (`created_at`), not when the row was last written (`updated_at`): a re-deferral that reset the clock would hide an old obligation, the failure the 2026-09-18 entry names. The age query AT-17 asks for is then `select * from v_deferred_acts where deferred_at < datetime('now', '-<N> days')`; no age threshold is stored or typed anywhere (rule 7a). The view reads three stages beyond base (research for searches and mining, evidence for sources and readings): it is a cross-stage pointer view (CLAUDE.md §3); name the stages in its header comment.
4. **Nothing reads the view as a gate in this task.** It is the measure the 2026-09-18 entry says is missing; a check that fails on an aged deferral would need an age the owner has not set (section 9 of this file names that as an owner question, not this task's).
5. **The skill's resume list** (`grep -n 'Resume from live state' -A6 skills/run-pipeline_SKILL.md`) names unadjudicated observations and leftover `NAMES-NEW` terms, not deferred adjudications: add "deferred acts, with their age (`select * from v_deferred_acts order by deferred_at`), including observations whose latest adjudication is `DEFERRED`". It is a prose caller of the new arm.

**Schema migration (this task has one).** Never type a migration number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, in `scripts/migrations/NNN_reading_deferrals.sql`, ending with `PRAGMA user_version` set to the same number. Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). Run `python3 scripts/audit/joined_cells_census.py` before and after (no new candidate). A new table must be writable by the capture path: confirm `reading_deferrals` appears in `dbcore.writable_tables(conn)` on the migrated copy (it is derived from the INSERTs in `db.py`; `python3 -I -c "import sys;sys.path.insert(0,'scripts');import dbcore,sqlite3;print('reading_deferrals' in dbcore.writable_tables(sqlite3.connect('$SCRATCH/t.db')))"` after applying the migration to the copy). After the migration, run `python3 scripts/generate/context_map.py` and include its output.

**What reads what this task adds:** a session or the owner asking which promises are outstanding and how old; for the `adjudication` arm, `/batch-done` (T-090's read (3) lists a batch's deferred observations; this arm gives them their age across batches), the skill's resume list (item 5 below) and T-072 (whose section 4 item 6 takes the leftover terms; a deferred observation from any source is now visible to it); `/orient` may read the view later (not changed here); the R6 rule of `research_dod` (deferral is not a findings channel) is unaffected. **What it makes deletable:** the hand-written union a reader would otherwise write each time.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `deferred_reason`, `citation_mining_status`, `source_scans`, `v_scan_ledger`, `writable_tables`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task (code, a test, a view, a registry entry, a skill or governance sentence that says a reading cannot be deferred, or that lists the deferral homes). A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds a verb, a table and a view: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (only a failure count above the before-run is yours). `skills/run-pipeline_SKILL.md` describes the reading step: add one sentence naming `defer-reading` where it says what to do with a source that cannot be read now, if it says that.

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_db_amend_writers test_scan_contract scan_debt research_dod schema_reference_audit migration_reproducibility"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Red here on 2026-11-13: `test_scan_contract` (G01, G02), `scan_debt`, `research_dod` (R12): record and carry on.

**Step 2: red before, green after** (cases `T079-01`… in `scripts/tests/test_db_amend_writers.py`; prefix free: `git grep -c 'T079-' scripts/tests/`):
- `T079-01` AT-17: on a scratch copy, defer one reading through the verb (a source and an active parameter chosen by query, a pair whose ledger status is `NOT-READ`: `select ref_id, parameter_id from v_scan_ledger where status='NOT-READ' order by 1,2 limit 1`); then `select kind, count(*) from v_deferred_acts group by kind` returns all three kinds, and the age query with a window that excludes today returns the older search and mining rows and not the new reading. Red before (no table, no verb, no view; assert stderr starts `REFUSING:` or the verb is unknown).
- `T079-02` refusals: blank reason; superseded source; inactive parameter; a pair already covered by a full reading (build one with `db.py record-scan` on the copy); a second undischarged deferral of the same pair.
- `T079-03` discharge: record a full catalogue reading of the deferred source on the copy (`db.py record-scan`, `TASK-FIXTURE` notes) and the deferral leaves the view; a `partial` reading does not discharge it.
- `T079-04` mining: on the copy, discharge one standing mining deferral with `log-mining --discharge-deferral` and it leaves the view.
- `T079-05` the adjudication arm (fold 2026-11-13): on a copy, an observation chosen by query whose latest adjudication is `DEFERRED` (`with l as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select observation_id from l where outcome='DEFERRED' order by 1 limit 1`; if none, adjudicate one `DEFERRED` on the copy, `TASK-FIXTURE`) lists with kind `adjudication`, its rationale and date; after `adjudicate-term` gives it another outcome on the copy, it leaves the view; an observation with an older `DEFERRED` and a newer `NAMES-EXISTING` never lists; `'DEFERRED'` is in `dbcore.check_values(conn, 'term_adjudications', 'outcome')`. On 2026-11-13 the canonical database held observations of each kind (`select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join (<the with clause above, as l>) l using(observation_id) group by 1`).
- Seeded defect: on a copy of the migration, drop the discharge clause of the reading arm; `T079-03` goes red; restore. And select the adjudication arm by any `DEFERRED` row rather than the latest; `T079-05`'s older-then-newer case goes red; restore.

**Fixtures** go to a copy, are labelled `TASK-FIXTURE`, and never reach `data/guidebook.db`.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` changes only by the migration, and the rebuild reproduces it.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: record a deferred reading and list every deferred act with its age (AT-17) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not defer any reading on the canonical database; the pull request carries no data.
- Do not add a status to `v_scan_ledger`, a column to `source_scans`, or use `data_capture_status`.
- Do not type an age threshold anywhere, or add a check that fails on age.
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the evidence output differs from section 3; `dbcore.writable_tables` does not capture the new table; a mining deferral's discharge cannot be read from `citation_mining_status` alone (report what `log_mining` writes); a check green before is red after; the rebuild does not reproduce the database. **Not this task's, for the owner:** what age makes a standing deferral a defect (a gate on the view needs that number in the owner's words).

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a compensating migration in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push. Re-derive the migration number after `git merge "$BASE"` if another merged first.
