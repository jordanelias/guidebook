# T-081  Each stored zero-result search states its cause

> **NOT FOR SONNET, and HELD.** Opus-class: deciding from a search's own note whether an empty result was a malformed query, the wrong index or a genuine absence is a reading of research, not a mechanical step (several notes argue for one cause in words that fit another). Held until T-080 is merged. T-080's question (OD-45: whether a blocked, refused or cut-off request is a zero-result search, and under which cause) is resolved under delegation (2026-11-13, confirmed by its independent check) and read through section 2's gate. An executor that opens this file before then does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 (AT-16). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-081 |
| Title | Each stored zero-result search states its cause |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | AT-16, third clause ("states which of three causes applies"); REQ-048; contract rule R14 (`grep -n -A8 'id: R14' governance/research-contract.yaml`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-080 merged (it carries OD-45, as resolved under delegation, into the writer; option (c) adds no cause to the column's CHECK). Check: `git log "$BASE" --oneline | grep -F 'zero-result search states its cause'`.
- **Owner decisions:** none in the register. Also OI-55 (1), how a carry-only research batch (it searches nothing and admits nothing) is gated: this batch is one, and `research_dod_session` may be red on it by construction, exactly as for T-102 and T-111. Follow the coordinator's ruling on OI-55 (1) when it exists; until then, report the gate's lines and do not treat its red as this batch's defect.
- **Delegated resolutions this task rests on.** OD-45 (the question T-080 carries into the writer): a logged search whose request never returned a result list is a search not run, deferred, with no absence class, and owed a re-run (option (c)). A resolution by an Opus-class model under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13 (ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-45" references/project-standards.md`): not the owner's words, reversible by the owner, checked by a second, independent Opus-class instance and confirmed with corrections applied, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-45; do gate $n; done
```
- **Tests that must be red before you start:** AT-16's third clause on the stored rows: `select count(*) from search_executions where results_found=0 and deferred_reason is null and absence_class is null` is above 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-081-classify-zero-result-searches "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-classify-zero-results   # bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-081" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** `/session-open` (it sets `scratchpad/CURRENT` to the stem), then `/orient`. **Pilot:** skip `/session-open`, stay on the given branch, work on the scratch copy only, stop before the write path.
- Every call points at the scratch copy inline: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`.
- Rows land only by the write path, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "R14 cause on each stored zero-result search" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another research batch merged after you copied the database, `emit_batch_sql.py` refuses; start again from the new base.

## 3. The problem, in the guidebook's terms

Each stored search that found nothing says why only in free text, so "no evidence exists" cannot be read apart from "we asked badly" or "this catalogue does not hold such work" without reading the prose. The typed column exists and is empty on every such row.

**Evidence command** (read-only):

```
python3 - <<'PY'
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('values', [l for l in c.execute("select sql from sqlite_master where name='search_executions'").fetchone()[0].splitlines() if 'absence_class IN' in l])
for r in c.execute("select exec_id, engine, absence_class, findings_note from search_executions where results_found=0 and deferred_reason is null order by exec_id"): print(r[0], r[1], r[2], '|', (r[3] or '')[:240])
PY
```

**Output on 2026-11-13:** the CHECK lists `query_shape_failure`, `wrong_index`, `genuine_absence` (OD-45's option (c) adds none); twelve rows (exec ids 26, 27, 28, 29, 81, 82, 84, 85, 87, 133, 138, 191), `absence_class` None on each, each with a note.

If the output differs (other than a value T-080 added), the ground has moved: stop (section 9).

## 4. The change

1. **For each row the command prints, read its whole `findings_note` and its `query_text`, and decide its cause under R14 and OD-45 as resolved under delegation (section 2).** Write it with `db.py amend-search --exec-id N --set-absence-class <value> --append-note "<one sentence: which words of the note decide it>" --session "$STEM"`. The verb refuses a value outside the column's CHECK and a row already classed.
   - A note that names the cause in R14's own words decides it (for example a note that calls the zero "GENUINE WELL-FORMED" with the anchor resolved, or "ZERO FROM THIS INDEX, NOT ABSENCE" because another index holds citations).
   - A note that names one cause in words that describe another (a "genuine absence from this index" because the catalogue does not hold that kind of document reads as the wrong index) is decided by what the note says happened, and the appended sentence quotes those words.
   - A request that never returned a result list (blocked, quota, cut off: on 2026-11-13 exec ids 87, 133, 138 and 191 by their notes) is, under OD-45 as resolved, a search not run: a deferral owed a re-run, with nothing in this column. A search logged as run cannot become a deferral by amendment (`amend-search` has no deferred-reason flag: `python3 scripts/db.py amend-search --help`), so the row is not amended here: list it in the pull request as a deferral owed a re-run, with its reason in the note's words. Exec id 81 calls itself "an R14 query-shape failure of a kind R14 does not name": judge it on its own words, not as one of these.
2. **A row whose note does not let you decide** is not classed: list it in the pull request with the note's words and leave it. Do not guess a cause.
3. Nothing else changes: no new search, no deletion, no edit of `results_found` or of a note's existing text.

**Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task changes no code; the sweep is for prose that restates a fact the rows change (CLAUDE.md rule 7a):
```
V='<an exec id you classed>'
git grep -n -F -e "exec $V" -e "exec_id $V" -e "exec-id $V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
A sentence that says a stored zero-result search has no typed cause becomes false: correct it if it is research prose, or list it.

## 6. Verification

**Red before, green after.** Before: section 2's count is above 0. After, on the migrated database: every row the command printed carries a cause, except those listed under item 1 (c) or item 2 with their reason; `select absence_class, count(*) from search_executions where results_found=0 and deferred_reason is null group by 1` shows the distribution. `research_dod`'s R14 still passes (it accepts the column).

**The gates, once each, after the migration is applied and before the commit:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep    # an UPDATE is invisible to the row-count check
```
Confirm the gates examined this batch: `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from search_executions where updated_by_session=?',(sys.argv[1],)).fetchone())" "$STEM"` is above 0.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "research-log-manager: state the R14 cause on each stored zero-result search [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: each exec id, the cause, the words of its note that decide it; rows left and why>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before T-080 is merged and the delegated resolution is confirmed (the gate of section 2 prints OPEN).
- Do not class a row whose note does not decide it; do not delete or re-run a search; do not rewrite a note.
- No tooling in this pull request (rule 10). Do not write `data/guidebook.db` except by the write path. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: a precondition is unmet; the evidence differs from section 3; `amend-search` refuses for a reason other than a value or an already-classed row; a check green before is red after; the rebuild does not reproduce the database; you would have to guess a cause.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a data migration is immutable; a wrong cause is corrected forward through the same verbs (if `amend-search` refuses to re-class, file that as a writer gap with `db.py add-gap`).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (the pass is recorded with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
