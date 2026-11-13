# T-067  Coverage per parameter and in-scope pair, reached through admissions

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B of the prior-workplan items). Its evidence commands were run on 2026-11-13 on a scratch copy and printed what section 3 states; its view was built and queried on that copy. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-067 |
| Title | Coverage per parameter and in-scope pair, reached through admissions |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | prior workplan T-6b step 5 (`sed -n '/\*\*T-6b Search terms/,/M21 KILLED/p' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report's step 5: `sed -n '/^5\. (OR-8 = yes) .v_coverage_parameter_via_admission/,/^6\. (OR-9/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); OR-8 (`grep -n -F 'OR-8: "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language."' references/project-standards.md`); OI-52 in `OPEN-ITEMS-PLAN.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** none (after T-050 if both are open: T-050 gives `search_admissions` a retirement, and this view must then read live admissions only; section 4 item 2 says how either order is handled). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F 'task/t-050'`.
- **Already on the base:** the jurisdiction roll-up through `base_jurisdictions.parent_code` (merged as #225: `git log "$BASE" --oneline | grep -F 'task/t-024-jurisdiction-registry'`).
- **Owner decisions:** none. This task rests on OR-8 (above) and on the owner's answer to OD-04 (`grep -n -F 'OD-04: scope = P1+P2+P3 as recorded' references/project-standards.md`), which makes the in-scope pairs of `v_research_scope` the bucket members OR-8 names. It decides no scope: it reads the scope wherever it stands.
- **Tests that must be red before you start:** T067-01 (no view returns one row per active parameter and owed pair). It is restated in full in section 6.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-067-coverage-per-parameter-via-admission "$BASE"   # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-067" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution** (a pull request intended): run `/session-open` before the first command, and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7. Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The owner ruled that research is exhausted per parameter and per bucket member, a bucket member being a jurisdiction together with its associated language (OR-8), and the run-pipeline skill states that rule (`grep -n -F 'Exhaustion is per parameter, per bucket member' skills/run-pipeline_SKILL.md`). Nothing computes it. `db.py coverage` reads per slug; `v_coverage_lens` groups by the parameter a search was logged with, and almost no search names one; the route by which a search actually reaches a parameter is the admission of a source that holds an extraction of that parameter, and no view follows it. So a session cannot see, for a parameter, which in-scope pairs have reached evidence, and a pair with nothing at all is invisible rather than shown empty. A table of that shape is how "every in-scope jurisdiction has been looked at for this parameter" gets claimed without being true.

**Evidence command** (read-only on the canonical database):

```
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print([r[0] for r in c.execute("select name from sqlite_master where type='view' and name like 'v\\_coverage%' escape '\\' order by 1")])
print("searches with / without a parameter:", c.execute("select count(parameter_id), count(*) - count(parameter_id) from search_executions").fetchone())
print("parameters reached through admissions:", c.execute("select count(distinct x.parameter_id) from search_admissions sa join source_value_extractions x on x.ref_id = sa.ref_id").fetchone()[0])
print("active parameters x owed pairs:", c.execute("select (select count(*) from base_parameters where status='active') * (select count(*) from v_research_scope)").fetchone()[0])
PY
grep -n -F 'Exhaustion is per parameter, per bucket member' skills/run-pipeline_SKILL.md
```

**Expected output today** (2026-11-13): the views `v_coverage_branch`, `v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_lens`, `v_coverage_priority` and no `v_coverage_parameter_via_admission`; a small number of searches with a parameter against a much larger number without (7 and 196 on 2026-11-13); a non-zero number of parameters reached through admissions (8); a non-zero product (700); and the skill's line.

**What of the prior T-6b is already done, and why only this view remains** (the authoring note the coordinator asked for; re-run each command):
- *The terms half* (`--term` deriving `terms_used` from the alias table) is T-026, merged as #226 (`git log "$BASE" --oneline | grep -F 'task/t-026-alias-attestation'`): `log-search --form-id` writes `search_execution_forms` by the form's key and refuses a form of another language (`grep -n -F 'search fires the forms of its own language' scripts/db.py`). The report's M21 (the no-alias refusal) has no counterpart because a search with no form is now simply a search with no form row.
- *The bucket table* (`jurisdiction_buckets`) is not built and must not be: OD-04's answer replaced buckets 1 and 2 with one scope, P1+P2+P3 (`grep -n -F 'This replaces buckets 1 and 2 of 2026-09-28' references/project-standards.md`), and the 2026-11-06 E11 answer made the `lang_jur_map` pairs of that scope the bucket members of OR-8 (`grep -n -F '| E11 |' references/project-standards.md`). That membership already has one home, `lang_jur_map.scope_status` read through `v_research_scope` (migrations 122 and 123; `grep -n 'Readers:' scripts/migrations/123_research_scope_and_ledger_precedence.sql`); T-025 builds `set-pair-scope` and T-101 records the scope on every pair. A second table of members would be a second home (rule 5). Bucket numbers are no longer read by any rule: OD-04 made the scope one set.
- *The redefinition of `v_coverage_priority` to buckets 1 and 2* is done by migration 123 (it reads `v_research_scope`).
- *T-057* (`tasks/T-057-base-coverage-view.md`) answers a different question: per concept and pair, whether a form of the concept is attested, searched for with none found, or not searched (the base's coverage of vocabulary). This task is per parameter and pair, through the evidence that searches admitted (research reaching judgment). Neither view answers the other's question; they share only `v_research_scope`.
- *Step 6* (a table of search indices) is not built: OR-9 "None yet".

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves the skill's rule with no reading; no existing view has the grain (section 3); so one view is added, and nothing else.

1. **Schema migration `scripts/migrations/NNN_coverage_parameter_via_admission.sql`** (number derived as below): one view, no table, no column, nothing stored. **Chosen (authoring 2026-11-13): this definition.**
   ```sql
   -- v_coverage_parameter_via_admission: one row per ACTIVE parameter and per pair the research scope owes
   -- (v_research_scope), saying how searches in that pair reached the parameter. Owner, OR-8 (2026-10-29):
   -- exhaustion is judged per parameter and per bucket member, a jurisdiction with its associated language.
   -- A pair with nothing is a row of zeros, never a missing row. No threshold and no "exhausted" flag: the
   -- reader judges from the counts (rule 8). Stages: research (search_executions, search_admissions) and
   -- judgment (source_value_extractions), joined on ref_id; base for the scope and the parameters.
   -- A search's jurisdiction rolls up to its country (OD-04; the roll-up of migration <T-024's number>).
   -- Readers: skills/run-pipeline_SKILL.md (Scope paragraph), skills/research-log-manager_SKILL.md (coverage).
   CREATE VIEW v_coverage_parameter_via_admission AS
   WITH searched AS (
     SELECT se.exec_id, se.parameter_id, UPPER(se.language) AS language,
            COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction
       FROM search_executions se
       LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
      WHERE se.deferred_reason IS NULL),
   reached AS (
     SELECT DISTINCT s.exec_id, s.language, s.jurisdiction, x.parameter_id, sa.ref_id
       FROM searched s
       JOIN search_admissions sa ON sa.exec_id = s.exec_id
       JOIN source_value_extractions x ON x.ref_id = sa.ref_id)
   SELECT p.parameter_id, v.language, v.jurisdiction, v.role,
          (SELECT COUNT(*) FROM searched s WHERE s.parameter_id = p.parameter_id
              AND s.language = v.language AND s.jurisdiction = v.jurisdiction) AS searches_naming_parameter,
          (SELECT COUNT(DISTINCT r.exec_id) FROM reached r WHERE r.parameter_id = p.parameter_id
              AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS searches_reaching_parameter,
          (SELECT COUNT(DISTINCT r.ref_id) FROM reached r WHERE r.parameter_id = p.parameter_id
              AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS sources_admitted
     FROM base_parameters p CROSS JOIN v_research_scope v
    WHERE p.status = 'active';
   ```
   Replace `<T-024's number>` with the migration that created `base_jurisdictions` (`grep -l 'CREATE TABLE base_jurisdictions' scripts/migrations/*.sql`). End the file by setting `PRAGMA user_version` to the migration's number.
   - **Chosen: the grain is active parameter × owed pair, built from the scope and not from the searches.** Rejected: the report's sketch (`GROUP BY` over searches that admitted something), which lists only pairs with a hit, so an untouched pair is absent and reads as nothing to do (CLAUDE.md §5(a), the failure the owner's 2026-09-28 rule was written against). Built on the scratch copy on 2026-11-13 it returned exactly one row per parameter and pair (700 rows, 700 distinct keys), 49 of them with an admitted source.
   - **Chosen: three counts side by side, not one.** `searches_naming_parameter` is the direct route (a search logged with `--parameter`), `searches_reaching_parameter` the route through an admitted source, `sources_admitted` the distinct sources reached. Rejected: adding the direct and indirect counts into one figure, which would hide which route did the reaching (the report notes the direct route already lives in `v_coverage_lens`; this view puts both beside the scope so one query answers the owner's question).
   - **Chosen: searches outside the scope are not shown.** A search whose rolled-up pair is not owed (30 admissions on 2026-11-13: `select count(*) from search_admissions sa join search_executions se using(exec_id) left join base_jurisdictions b on b.jurisdiction_code=se.jurisdiction where se.deferred_reason is null and not exists(select 1 from v_research_scope v where v.language=upper(se.language) and v.jurisdiction=coalesce(b.parent_code,se.jurisdiction))`) is already reported by `db.py coverage` as `searches_outside_scope`; this view answers what is owed.
   - **Chosen: no lens columns.** OR-8 names parameter and bucket member, not lens; `v_coverage_lens` keeps the lens grain.
2. **Live admissions only, whichever of this task and T-050 merges first.** Run `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(search_admissions)')])"`. If `retired_at` is listed (T-050 merged first), add `AND sa.retired_at IS NULL` to the `reached` join. If it is not, write the view as above and add one line to the pull request: "T-050 must add `AND sa.retired_at IS NULL` to `v_coverage_parameter_via_admission`" (T-050's own sweep of `search_admissions` finds the view in `sqlite_master` and its section 4 item 3 already requires every reader to filter).
3. **The readers, edited in the same pull request** (rule: nothing is added without naming what reads it):
   - `skills/run-pipeline_SKILL.md`, the Scope paragraph (`grep -n -F 'Exhaustion is per parameter, per bucket member' skills/run-pipeline_SKILL.md`): add one sentence after the paragraph's first sentence: "Read it per parameter from `v_coverage_parameter_via_admission` (one row per active parameter and owed pair; a pair of zeros is unsearched for that parameter)."
   - `skills/research-log-manager_SKILL.md`, the coverage quote (`grep -n -F 'Coverage is derived from the log' skills/research-log-manager_SKILL.md`): add `v_coverage_parameter_via_admission` to the list of views, with "(per parameter, through admissions)".
4. **Stage map.** `governance/stage-map.yaml` maps tables only (its header: "Views are absent from this file"), so no entry is added; the view's own comment names the stages it spans (CLAUDE.md §3). Run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after (section 5).
5. **Generated context map.** After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output: a new view makes `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (a view adds no candidate). Apply it only with `python3 scripts/migrate_db.py`. Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). The pull request contains no `scripts/migrations/data_*` file.

**What reads what this task adds or changes:** the two skill sentences of item 3 (the operator's per-parameter exhaustion reading, OR-8); T-050's sweep (item 2). Nothing is replaced or made deletable.

**What wrong thing reaches the guidebook without it:** a parameter's page says or implies that the in-scope jurisdictions were searched for it when some pairs were never reached, because no reading shows the pairs that reached nothing.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it.

## 5. Caller sweep

Names to sweep: `v_coverage_lens`, `v_research_scope`, `search_admissions`, `v_coverage_`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there. A sentence that says per-parameter coverage cannot be read, or names only per-slug readers as the way to judge exhaustion per parameter, is a caller.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds a view, so also run `python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/before-graph.txt" 2>&1` before the change and again after, and report the difference. It is red on the base: only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-13; re-run them, a new file in your output is a hit to judge):
- `v_coverage_lens`: `skills/research-log-manager_SKILL.md` (item 3: a caller you edit), `governance/context-map.yaml` (regenerated, item 5).
- `v_research_scope`: `scripts/db.py` (`get_coverage_completeness`: a mention, unchanged), `scripts/tests/test_run_pipeline_refusals.py` (W01, G02: they read the view; run before and after), `skills/run-pipeline_SKILL.md` (item 3), views `v_coverage_priority` (a mention).
- `search_admissions`: code that writes or audits admissions (`scripts/db.py`, `scripts/dbcore.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/research_protocol_audit.py`, `scripts/research/emit_batch_sql.py`, `scripts/tests/test_db_amend_writers.py`): mentions; this task changes no admission.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals` (W01 and G02 read `v_research_scope`; your new cases go here), `test_db_amend_writers` (reads `v_coverage_priority`), `test_scan_contract`. Run each as the registry runs it and keep the output:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check that is red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** In `scripts/tests/test_run_pipeline_refusals.py`, next to W01 and using that file's `scratch()`, `record()` and `skip()` helpers. Confirm the prefix is free first (`grep -c '"T067-' scripts/tests/test_run_pipeline_refusals.py` prints 0). Every probe is chosen by query; anything built is built on the test's scratch copy and labelled `TASK-FIXTURE`:

| id | what | after the change | on unchanged code |
|---|---|---|---|
| T067-01 | the grain: `count(*)` equals `count(*)` of `select distinct parameter_id, language, jurisdiction` of the view, and equals active parameters × rows of `v_research_scope` | equal | red (`no such table`) |
| T067-02 | an owed pair and an active parameter chosen by query with `sources_admitted = 0`; on the copy, add a non-deferred search in that pair that admits a source holding an extraction of that parameter (the source chosen by query) | that row's `sources_admitted` and `searches_reaching_parameter` become 1; every other row is unchanged (compare the whole view before and after the insert) | red |
| T067-03 | the same search with `deferred_reason` set | the row stays at 0 | red |
| T067-04 | the same search logged with a sub-national code whose parent is the pair's jurisdiction (admit one on the copy with `kind='sub-national'`, `parent_code` the pair's jurisdiction, if none is held) | counts toward the parent's row | red |
| T067-05 | the same search with the language in lower case | counts toward the upper-case pair | red |
| T067-06 | a pair recorded `scoped-out` on the copy | its rows leave the view | red |

**Seeded defects** (each must turn a case red; restore the file after): remove `WHERE se.deferred_reason IS NULL` (T067-03 red); replace `COALESCE(b.parent_code, se.jurisdiction)` with `se.jurisdiction` (T067-04 red); replace `UPPER(se.language)` with `se.language` (T067-05 red). Apply each to a copy of the migration's SQL executed on a scratch database, not to the committed file, and report KILLED for each.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- Run it once, when every edit is made, before the commit; do not run `run_checks.py` separately, and never `--all`. It takes several minutes: run it in the background with a long timeout.
- In `gate.txt` read the `RESULT` line, any check under `NOTHING-IN-SCOPE` (it has not passed: say so), and any blocking `FAIL`.
- `research_tooling_separation` reads `origin/main`, not `$BASE`: run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` once by hand and report that result; a gate FAIL that disappears with `--base` is not yours.

**The canonical database moves only by `scripts/migrate_db.py`**, and the rebuild reproduces it (section 4).

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: coverage per parameter and in-scope pair through admissions (OR-8) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not build `jurisdiction_buckets`, a bucket number, a list of in-scope codes, or an "exhausted" flag or threshold (section 3; rule 8).
- Do not decide doctrine (jurisdiction scope included). Do not record a scope on any pair: that is T-101's.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not put research rows in this pull request (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb or script that section 4 does not name. A caller the sweep shows is made false by your change is in scope and is fixed here.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met;
- the evidence command in section 3 does not give today's expected shape (a `v_coverage_parameter_via_admission` view already exists, `v_research_scope` is gone, or no parameter is reached through admissions);
- the red test is not red before the change, or is not green after it, after one honest attempt; or a seeded defect survives;
- the sweep finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- the rebuild does not reproduce the database;
- `v_research_scope` has changed its columns (the view reads `language`, `jurisdiction`, `role`): report, do not adapt;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request; the view is dropped by a compensating migration, never by editing this one (CLAUDE.md rule 3).

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff. One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; the T-050 line of section 4 item 2 if it applies; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and derive the migration number again.
