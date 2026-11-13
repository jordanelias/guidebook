# T-013  A gap says what it is a gap in, and a search says which gap caused it

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-013-report.md`, patch `.../T-013.patch`; defects folded. Expect to find a defect in this file all the same, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-013 |
| Title | A gap says what it is a gap in, and a search says which gap caused it |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-12 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** none. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** AT-73 red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-013-typed-gaps "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-013" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

A gap names its parameter and group only in a sentence. The book cannot list its stated gaps for a parameter or a group, and a search run to close a gap cannot say so, so the backward step from a pending cell to research leaves no trail.

**Evidence command** (run from the repository root; it reads the canonical database read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from pragma_table_info('gaps')\").fetchall())"; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from pragma_table_info('search_executions') where name='gap_id'\").fetchall())"
```

**Expected output today:** `gaps` has no `parameter_id`, lens, `jurisdiction` or `language` column; the second query returns 0. `search_executions` already has `parameter_id`, `jurisdiction`, `language` and the four lens columns (`python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[0] for r in c.execute(\"select name from pragma_table_info('search_executions')\")])"`): only `gap_id` is missing there, and nothing else is added to it.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Schema migration: add to `gaps` the nullable columns `parameter_id` (FK `base_parameters`), `identity_code`, `icf_code`, `needs_code`, `medical_code` (FKs to the four lens registries, named exactly as on `specifications`), `jurisdiction`, `language`; add to `search_executions` a nullable `gap_id` (FK `gaps`). Nullable because existing rows have none; do not back-fill them. `search_executions` already holds `parameter_id`, `jurisdiction`, `language` and the four lens columns (section 3): add only `gap_id` there. **Chosen (pilot 2026-11-13):** eight `ALTER TABLE ... ADD COLUMN` statements and no table rebuild, copying each `REFERENCES` clause from the same column on `search_executions` (`select sql from sqlite_master where name='search_executions'`); `jurisdiction` and `language` take no FK, as on `search_executions`. `search_executions` is `STRICT`, so its new column must be typed: `gap_id TEXT REFERENCES gaps(gap_id)` (`gaps.gap_id` is `TEXT`).
2. `scripts/assess/assess_cell.py`, where it writes the gap for a pending cell (`grep -n 'INSERT INTO gaps' scripts/assess/assess_cell.py`): fill `parameter_id` and the four lens columns from the cell (`parameter_id` and the `lens` dict already in scope there); the engine has no jurisdiction or language for a cell, so those two stay NULL. `scripts/db.py add-gap` and `log-search`: accept the matching optional arguments. **Chosen (pilot 2026-11-13):** `add-gap` takes `--parameter`, `--identity`, `--icf`, `--needs`, `--medical`, `--jurisdiction`, `--language`, the same flag names `log-search` already uses for the same columns (`grep -n 'p_ls.add_argument' scripts/db.py`), and `log-search` takes `--gap-id`. Each value is refused, by name and before any row is written, the way `log_search` already refuses its own: the FK columns with `dbcore.fk_declared` (it reads `PRAGMA foreign_key_list`, so no list of codes is restated), `--jurisdiction` with `dbcore.check_jurisdiction`, `--language` against `dbcore.live_vocab(conn, "lang_jur_map", "language")`, and `--gap-id` with `dbcore.fk_declared` on `search_executions.gap_id`. No `choices=` list (CLAUDE.md rule 8).
3. Delete nothing. `gap_mining`, its verbs and its audit stay (they have callers; T-040).

**What reads what this task adds or changes:** The engine (writes); `db.py gaps`, `coverage`; a future render Gaps element; T-034.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). **This task needs no table rebuild:** all eight columns are nullable, with no CHECK, so `ALTER TABLE ... ADD COLUMN ... REFERENCES ...` adds each in place (a NULL default beside a `REFERENCES` clause is legal; `scripts/migrations/125_alias_observation_pointer.sql` is a precedent). Do not write a create, copy, drop, rename rebuild of `gaps` or `search_executions`. Still list the views and indexes that name each table (`select type, name from sqlite_master where sql like '%<table>%'`) and confirm none takes a bare `SELECT *` or `<table>.*` from it (a `COUNT(*)` is not that; on 2026-11-12 the views were `v_pending` on `gaps` and the `v_coverage_*` views and `v_source_admission` on `search_executions`, all naming their columns); ADD COLUMN leaves them as they are. The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `INTO gaps`, `FROM gaps`, `add-gap`, `gap_register_id`, `INTO search_executions`, `log-search`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `INTO gaps`: code and skills: `scripts/assess/assess_cell.py`, `scripts/db.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_validate_evidence_state_2_4.py`. Prose: `architecture/sqlite-data-layer.md`, `governance/stage-map.yaml`, `workplan/pipeline-state-graph/machines.yaml`.
- `FROM gaps`: code and skills: `scripts/assess/assess_cell.py`, `scripts/audit/gap_mining_audit.py`, `scripts/audit/research_protocol_audit.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/bootstrap.sh`, `scripts/db.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/validate_evidence_state.py`. Prose: `architecture/sqlite-data-layer.md`, `governance/stage-map.yaml`.
- `add-gap`: code and skills: `scripts/db.py`, `scripts/dbcore.py`, `scripts/tests/test_run_pipeline_refusals.py`, `skills/connection-discovery_SKILL.md`, `skills/content-gap-analyzer_SKILL.md`, `skills/cross-population-conflict-mapper_SKILL.md`, `skills/evidence-auditor_SKILL.md`, `skills/find-and-replace_SKILL.md`, `skills/gap-driven-mining_SKILL.md`, `skills/research-log-manager_SKILL.md`, `skills/run-pipeline_SKILL.md`, `skills/toc-editor_SKILL.md`. Prose: `governance/migration-based-writes-adopted-2026-05-11.md`, `references/audits/bpc-audit-pass0-2026-05-10.md`, `references/audits/bpc-audit-pass2-2026-05-10.md`, `workplan/pipeline-state-graph/machines.yaml`.
- `gap_register_id`: code and skills: `schemas/evidence_state.py`, `scripts/assess/assess_cell.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_validate_evidence_state_2_4.py`, `scripts/validate_evidence_state.py`. Prose: `governance/context-map.yaml`.
- `INTO search_executions`: code and skills: `scripts/audit/research_batch_dod.py`, `scripts/db.py`. Prose: none.
- `log-search`: code and skills: `.claude/commands/batch-done.md`, `.claude/settings.json`, `scripts/audit/derived_not_curated_audit.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/research_protocol_audit.py`, `scripts/audit/search_log_completeness.py`, `scripts/db.py`, `scripts/research/retrieval_log.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_search_log_completeness.py`, `skills/adversarial-research_SKILL.md`, `skills/citation-miner_SKILL.md`, `skills/research-log-manager_SKILL.md` and others (the command lists them all). Prose: `governance/check-registry.yaml`, `governance/research-contract.yaml`.

- **Callers no name above finds** (pilot 2026-11-13): `governance/context-map.yaml`, generated from the schema, goes stale with the migration and is regenerated (section 4); `scripts/audit/jurisdiction_db_vocabulary.py` (blocking) reads every table that has a `jurisdiction` column, so `gaps` enters its subject: run it before and after (section 6); the assessment engine's `--report-json` carries `gap_register_id`, which is how step 2 of section 6 finds the gap it wrote.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`, `test_validate_evidence_state_2_4`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`, `test_evidence_cell_state_2_3` (it writes `INTO gaps` and reads `gap_register_id`, section 5), `jurisdiction_db_vocabulary` (blocking; `gaps` enters its subject, section 5). Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness test_assess_cell_pilot test_validate_evidence_state_2_4 migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit test_evidence_cell_state_2_3 jurisdiction_db_vocabulary"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT|ALL PASS|PASS: all|FAILURES' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints `EXAMINED: 0` examined nothing: say so in the pull request. **Three tests print no `EXAMINED:` line by design** (pilot 2026-11-13): `test_assess_cell_pilot` ends `PASS: all pilot-engine branch tests`, and `test_validate_evidence_state_2_4` and `test_evidence_cell_state_2_3` end `ALL PASS (0 failed)` or `FAILURES: …`; record that summary line as their result and say in the pull request that they print no count. `test_author_presence` prints `EXAMINED` inside its assertion labels as well: its subject is the **last** `EXAMINED:` line (`grep '^EXAMINED:' "$SCRATCH/before-test_author_presence.txt" | tail -1`).

**Step 2: red before, green after.** Before: the evidence command of section 3 shows no such columns (red). After the migration is applied to your clone and the code is changed, run this probe on a copy. Parameter 7 and slug `accessible-circulation-geometry` are probes read on 2026-11-13 (an active parameter with no row in `specifications`, so the engine writes a pending cell and its gap); the expected values are read from the engine's own report, not typed:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-013"
cp data/guidebook.db "$SCRATCH/g.db" && python3 scripts/assess/assess_cell.py --db "$SCRATCH/g.db" --emit-sql "$SCRATCH/g.sql" --parameter-id 7 --slug accessible-circulation-geometry --identity ALL --session session_task-probe --stamp '2026-01-01 00:00' --report-json "$SCRATCH/g.json"
python3 -I -c "
import json,sqlite3,sys
r=json.load(open(sys.argv[1]))[0]; l=r['lens']; c=sqlite3.connect(sys.argv[2])
assert r['state']=='pending' and r['gap_register_id'], ('probe is not a pending cell: stop (section 9)', r['state'])
got=c.execute('select parameter_id,identity_code,icf_code,needs_code,medical_code from gaps where gap_id=?',(r['gap_register_id'],)).fetchone()
want=(r['parameter_id'],l['identity_code'],l['icf_code'],l['needs_code'],l['medical_code'])
print(r['gap_register_id'],got,want,'GREEN' if got==want else 'RED')" "$SCRATCH/g.json" "$SCRATCH/g.db"
GAP=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))[0]['gap_register_id'])" "$SCRATCH/g.json")
GUIDEBOOK_DB_PATH="$SCRATCH/g.db" python3 scripts/db.py log-search --parameter 7 --language EN --query-text 'TASK-FIXTURE probe' --engine manual --depth-method scoping --prior-expectation 'TASK-FIXTURE: none expected' --session session_task-probe --gap-id "$GAP"
python3 -I -c "import sqlite3,sys;print(sqlite3.connect(sys.argv[1]).execute('select exec_id,gap_id from search_executions order by exec_id desc limit 1').fetchone())" "$SCRATCH/g.db"   # GREEN: gap_id equals $GAP
GUIDEBOOK_DB_PATH="$SCRATCH/g.db" python3 scripts/db.py log-search --parameter 7 --language EN --query-text 'TASK-FIXTURE probe' --engine manual --depth-method scoping --prior-expectation 'TASK-FIXTURE: none expected' --session session_task-probe --gap-id "GAP-NO-SUCH-$GAP" --dry-run   # must be refused, naming the gap id
```

If the first assertion fails (the cell is no longer pending, or `assess_cell.py` refuses), the probe has moved: choose another active parameter with no `specifications` row by query, and say so. The probe's `--dry-run` refusal and the stored `gap_id` are restated as test cases below; the probe alone is not the test.

**Writing the test.** Put the new cases in `scripts/tests/test_run_pipeline_refusals.py` (chosen, pilot 2026-11-13: it already exercises `add-gap`, `log-search` and the engine through `assess()`, `cli()` and `scratch()`). At least: the engine's pending gap carries the cell's `parameter_id` and lenses; `add-gap` stores each new flag and refuses an unknown parameter, lens code, jurisdiction and language by name with no row written; `log-search --gap-id` stores a held gap id and refuses an unheld one with no row written. Two traps in that file (pilot): (a) earlier cases (E01, E05, E06, E11, E12) have already determined cells on the shared copy with the helper's default lens (`IDENT`, `ICF`), so an engine case using that lens is refused "already determined": give your case a lens no earlier case writes, chosen by query (for example add a `needs_code` from `access_needs`); (b) `far()` assumes a numeric id, and the highest `gap_id` in string order is non-numeric (for example `GAP-ICF-TITLES`), so take an unheld gap id from `db.next_gap_id()` (numeric ordering), never `far()` over `MAX(gap_id)`. Take case ids that cannot collide: prefix them with this task's number (`T013-01`, `T013-02`, …) and confirm the prefix is free first (`grep -c '"T013-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: type the gap subject and link searches to the gap that caused them [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author `best_practice_synthesis` or any synthesis prose. A Sonnet-class model is below that floor.
- Do not treat any `[A-Z]-NN` code (old item codes met in `references/`, `working/`) as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, determinations) in a tooling pull request, or tooling in a research one (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller:** a test fixture, a comment, a skill sentence or a help string that the sweep of section 5 shows is made false or red by your change is in scope, is fixed in this pull request, and is listed there.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- a view or check that names `gaps` or `search_executions` (section 4 lists the views) breaks after the migration: stop; the ADD COLUMN migration of section 4 should leave every one as it was, and a rebuild is not the fix.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
