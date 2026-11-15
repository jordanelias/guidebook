# T-080  A zero-result search states its cause when it is logged

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 (AT-16), probe in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/R2-probes.md` (section AT-16). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13; the R2 probe was re-run on that day's HEAD. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-080 |
| Title | A zero-result search states its cause when it is logged |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class: OD-45 is resolved under delegation and read through section 2's gate, so every step is mechanical from this file |
| Traces to | AT-16 ("A zero-result search is stored, cannot be deleted through the sanctioned path, and states which of three causes applies", `grep -n 'AT-16' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`); REQ-048 and REQ-021; contract rule R14 (`grep -n -A8 'id: R14' governance/research-contract.yaml`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. The one question this task needed (registered as OD-45: is a logged search whose request never returned a result list a zero-result search, and under which cause, or a search not run?) is resolved under delegation (next bullet). What it rests on: R14 (`grep -n -A8 'id: R14' governance/research-contract.yaml`); the operative instrument's "`deferred_reason` is for searches *not run*, never a findings channel" (`grep -n -F 'is for searches *not run*' decisions/DR-2026-08-19-research-restart-operative-instrument.md`); and the notes of the live zero-result searches (section 3's command prints them). The step it governs is section 4 item 2.
- **Delegated resolutions this task rests on.** OD-45: a search not run, deferred (option (c)). A logged search whose request returned no result list (a 403 or bot challenge, a 429, a connection reset, a stub page) was not run: it is recorded with `deferred_reason` naming the failure, carries no absence class, and is owed a re-run; a zero-result search is read as a finding only where `deferred_reason` is NULL. A resolution by an Opus-class model under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13 (ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-45" references/project-standards.md`): not the owner's words, reversible by the owner, checked by a second, independent Opus-class instance and confirmed with corrections applied, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-45; do gate $n; done
```
- **Tests that must be red before you start:** AT-16's third clause, restated in section 6. (Its first two clauses are green on 2026-11-13: the rows are stored; `search_executions` is not in `dbcore.deletable_tables` and `emit_batch_sql.py` refuses a deleted row.)
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-080-zero-result-search-states-its-cause "$BASE"          # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-080" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

An empty search result is evidence that nothing exists only if the query was well formed and the index was the right one. The project records zero-result searches and keeps them, and has a typed column for the cause (`absence_class`), but the writer lets a search that found nothing be logged with no cause, and no live zero-result search carries one in the column. A reader therefore cannot tell "nothing exists" from "we asked badly" or "the catalogue does not hold this kind of work" without reading free text.

**Evidence commands** (on the scratch copy for the write probe):

```
python3 - <<'PY'
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('zero-result rows, with class, deferred, with note:', c.execute("select count(*), sum(absence_class is not null), sum(deferred_reason is not null), sum(coalesce(findings_note,'')<>'') from search_executions where results_found=0").fetchone())
for r in c.execute("select exec_id, engine, substr(findings_note,1,90) from search_executions where results_found=0 and deferred_reason is null order by exec_id"): print(r)
PY
P=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select min(parameter_id) from base_parameters where status='active'\").fetchone()[0])")
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py log-search --parameter "$P" --language en --query-text "TASK-FIXTURE zero probe" --engine pubmed --depth-method scoping --results-found 0 --prior-expectation "TASK-FIXTURE expect none" --session session_task-probe > "$SCRATCH/probe.txt" 2>&1; echo "log-search rc=$?"
python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select results_found, absence_class from search_executions where query_text='TASK-FIXTURE zero probe'\").fetchall())"
grep -n 'Omit until judged' scripts/db.py
```

**Output on 2026-11-13:** `(13, 0, 1, 12)`; twelve rows listed (exec ids 26, 27, 28, 29, 81, 82, 84, 85, 87, 133, 138, 191), of which 81, 87, 133, 138 and 191 describe a request that did not return a result list; `log-search rc=0`; `[(0, None)]` (a zero-result search with no cause is written); the help text of `--absence-class` says "Omit until judged; set later with amend-search --set-absence-class".

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **`log-search` refuses a zero-result search with no cause.** In `log_search` (`grep -n 'def log_search' scripts/db.py`), beside the existing refusal of a cause on a non-zero search (`grep -n 'search that found nothing can be classed as an absence' scripts/db.py`), refuse `results_found == 0` with `absence_class` None and `deferred_reason` None, naming the values read from the column's CHECK (`dbcore.schema_choices("search_executions", "absence_class")`, never typed) and the next act. A backfilled search (`--backfill 1`) is not exempt. Correct the `--absence-class` help text ("Omit until judged" becomes "Required when --results-found is 0"). **Chosen (authoring 2026-11-13):** refuse at write, as R14's "while-searching" phase places the rule and AT-16 states it; rejected: a check that reports bare rows after the fact (R14 in `research_dod` already does that and accepts a free-text note, so it cannot close AT-16's "states which of three"). Rejected also: exempting backfill (the rule is about the row, not about when it was logged; a backfill whose cause is unknown is not logged until it is).
2. **Apply OD-45 as resolved under delegation, option (c): a deferral.** The refusal's message says that a request that returned no result list is logged with `--deferred-reason` (it was not run) and not as a zero-result search. Then name, in the pull request, every reader that counts zero-yield searches, and make each exclude `deferred_reason IS NOT NULL` first, or a search not run reads as a null result (`results_found` is NOT NULL, so a deferred row still stores `0`): find them with `git grep -n -E "results_found *(=|==) *0" -- scripts skills governance ':!scripts/migrations'`, and list each with whether it already excludes deferrals. The column's own comment (`deferred_reason TEXT, -- non-NULL => deliberate no-search for this cell`) calls a deferral "deliberate"; a blocked request is a search not run, not a choice: say so in the pull request (the comment lives in the table's DDL).
3. **Live rows are not touched here.** Classifying the existing zero-result searches is judgment on research rows: T-081 (a RESEARCH task, after this one).

**Schema migration:** none (option (c) adds no cause to the column's CHECK). The pull request contains no `scripts/migrations/` file.

**What reads what this task changes:** every research session's `log-search` call (on 2026-11-13 `git grep -l 'log-search' -- skills` names `adversarial-research`, `citation-miner`, `gap-driven-mining`, `research-log-manager` and `run-pipeline`; re-derive); R14 in `research_dod`.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `log-search`, `log_search`, `--results-found`, `absence_class`, `absence-class`, `Omit until judged`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: a test, fixture or script that logs a zero-result search without a cause (it now fails for the new reason; repoint it to carry a cause, or to test the refusal); a skill or command that tells a session to log an empty result and judge it later; a registry entry. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`, `references/search-log/` (records of past searches).

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
The refusal text changes: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference. Known callers to read on the day: `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_search_log_completeness.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/audit/research_batch_dod.py` (its selftest logs searches), and every skill that tells a session how to log a search (`git grep -l 'log-search' -- skills`).

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_run_pipeline_refusals test_search_log_completeness test_db_amend_writers research_dod_selftest research_dod search_log_completeness"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])).replace('@SESSION@',''))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
`search_log_completeness` takes a session; with none it may refuse or examine nothing: record what it printed. `research_dod` is red on the base (R12): record and carry on.

**Step 2: red before, green after** (cases `T080-01`…; prefix free: `git grep -c 'T080-' scripts/tests/`):
- `T080-01` AT-16 third clause: `log-search --results-found 0` with no `--absence-class` and no `--deferred-reason` is refused (stderr starts `REFUSING:` and names the values read from the CHECK); no row is written (count before and after on the copy). Red before (section 3's probe: rc 0, row written).
- `T080-02` the same with `--absence-class` set to the first value of `dbcore.schema_choices("search_executions", "absence_class")` is accepted.
- `T080-03` the same with `--deferred-reason` is accepted (a search not run).
- `T080-04` `--backfill 1` with no cause is refused.
- Seeded defect: comment out the new refusal; `T080-01` goes red; restore.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail; a fixture repointed by the sweep is listed.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` must not move (option (c) brings no migration).

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: a zero-result search states its cause when logged (AT-16) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the delegated resolution of OD-45 and its ledger lines (the resolution, its status and its check); evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not classify or amend any live search (that is T-081).
- Do not type the cause vocabulary into code; read it from the CHECK.
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: section 2's gate prints CLOSED for OD-45 (the owner has reversed it, a correction has withdrawn it, or its independent check is not recorded), or the recorded resolution adds a condition this file does not cover; the evidence output differs from section 3; a research skill's instructions cannot be kept true without a doctrine change; a check green before is red after; a migration would be needed (option (c) needs none).

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert` in a new pull request (no migration to compensate under option (c)).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
