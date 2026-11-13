# T-012  Follow-up reasons for a skimmed figure and an absence finding

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-012-report.md`, patch `.../T-012.patch`; defects folded. Expect to find a defect in this file still, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-012 |
| Title | Follow-up reasons for a skimmed figure and an absence finding |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-13 (two values) in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** none. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** the red test of section 6 step 2: the reason vocabulary has one value, so an absence finding's owed tested value cannot be recorded (AT-11's recording half). AT-08's skimmed half is already green and stays so: the engine names each skimmed finding as owing a dedicated reading (`git grep -n "owes a dedicated reading" -- scripts/assess/assess_cell.py scripts/tests/test_assess_cell_pilot.py`), and this task adds nothing for it (section 4, item 1). AT-11's pointer half (an absence finding pointing at the code figure it tested) is an `extraction_relations` row with `relation = 'tested_at'`, which exists already and is not this task's. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi; echo "BASE=$BASE"
git switch -c task/t-012-follow-up-reasons "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-012" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The owner ruled that a skimmed finding cues a dedicated reading and that a study reporting no change sends work back to find the values it tested. The first debt is already recorded, by `extraction_method = 'skim'`, and the engine names it (section 4, item 1). The second cannot be recorded: a no-change finding whose tested value is still unknown has no carrier, so the work owed on it is forgotten and the finding is later treated as read.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3,re;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(' '.join(re.search(r'reason\s+TEXT[^\n]*', c.execute(\"select sql from sqlite_master where name='extraction_follow_ups'\").fetchone()[0]).group(0).split()))"
```

**Expected output today:** exactly one line, `reason TEXT NOT NULL CHECK (reason IN ('read-outside-admitting-purpose')),` (the command collapses the stored runs of spaces, so the line compares as written): the vocabulary has one value.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. A schema migration that rebuilds `extraction_follow_ups` with the CHECK widened by **one** value: `absence-needs-tested-value` (a finding with `claim_type = 'absent'` that reports no change, whose tested value backward citation mining and context are still to find; REQ-039). Add no other value. No value is named for `provisional`: the owner answered OD-10 on 2026-11-12 (`grep -n -F "OD-10: provisional means strength of evidence" references/project-standards.md`): `provisional` is the cell's computed strength, and a re-read owed is a reading's own status (`extraction_status = 'preliminary'`, or a follow-up on the reading). A reader's question is OD-21's open gate (T-021), not a follow-up value.
   **Chosen (pilot 2026-11-13): no `skimmed-needs-full-read` value.** The debt it would record is already held in the cell that names it: `source_value_extractions.extraction_method = 'skim'` (`dbcore.NOT_PUBLISHABLE_METHODS`). The engine reads that column, leaves the figure out and names it as owing a dedicated reading with the command that records one (`scan_command` in `scripts/assess/assess_cell.py`; the owner's ACTION (1) of 2026-10-21, `grep -n -F "report a skimmed one as owing a dedicated reading" references/project-standards.md`), and the debt closes when the reading is recorded and `db.py amend-extraction` changes `extraction_method`. A follow-up row with that reason would be a second home of the same fact (CLAUDE.md rules 5 and 8), would stay open after the column was amended, and would contradict migration 105's own design ("Skimmed figures need no follow-up row: the typed column extraction_method = 'skim' already says it"). An absence finding is different: `claim_type = 'absent'` also covers rows with no stated value for other reasons (a checklist question, a qualitative requirement), so "this one owes a tested value" is a judgement with a warrant, which is what a follow-up row records. The pilot added both values (its patch, `T-012.patch`, is not to be applied as it stands).
2. `scripts/db.py raise-follow-up`: nothing to change. Its `--reason` choices are read from the CHECK (`dbcore.schema_choices("extraction_follow_ups", "reason")`) and the writer checks the value with `dbcore.check_declared` (pilot 2026-11-13; `grep -n 'schema_choices("extraction_follow_ups"' scripts/db.py`).
3. `scripts/audit/extraction_follow_up_audit.py`: nothing to change. It prints each row's `reason` and names none (pilot 2026-11-13; `grep -c -F "read-outside-admitting-purpose" scripts/audit/extraction_follow_up_audit.py` prints 0).
4. One test case in `scripts/tests/test_scan_contract.py` for the new value and one for the choice in item 1 (section 6).

**What reads what this task adds or changes:** `raise-follow-up` (its choices), `resolve-follow-up`, `extraction_follow_up_audit` (lists open follow-ups; fails a live determination governed by an extraction under one). **The engine does not read `extraction_follow_ups`** (`git grep -n -i -e follow_up -e follow-up -- scripts/assess` prints nothing): it leaves out a figure by `extraction_method`, not by a follow-up, so there is nothing in it to check or change. (The improvement programme's IMP-13 says otherwise; it is wrong on this point.)

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**This migration, specifically** (a CHECK change, so create, copy, drop, rename):
- The name list command gives the table and one index, `ux_extraction_follow_ups_open`, and no view or trigger (pilot 2026-11-13); recreate the index exactly as migration 105 declares it.
- **No `-- AFTER_DATA:` marker.** No committed data migration names the table: `git grep -l extraction_follow_ups -- 'scripts/migrations/data_*'` prints nothing (if it prints a file, stop: section 9).
- **The table is `AUTOINCREMENT`, and `DROP TABLE` deletes its `sqlite_sequence` row**, so an identifier could be reissued. Capture the floor first and restore it as a maximum afterwards, as migration 114 does (`grep -n "_114_seq" scripts/migrations/114_extraction_slug_and_root.sql`): `CREATE TEMP TABLE _NNN_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'extraction_follow_ups';` before the drop; after the rename, insert the captured row if `sqlite_sequence` has none for the table, then `UPDATE sqlite_sequence SET seq = MAX(seq, (SELECT COALESCE(MAX(seq), 0) FROM _NNN_seq)) WHERE name = 'extraction_follow_ups';` and drop the temp table. The table holds 0 rows today, so the copy moves nothing in the real database: prove the copy and the floor on a seeded scratch copy (insert three `TASK-FIXTURE` follow-ups, delete one, apply the migration's SQL, confirm the two ids survive and `sqlite_sequence` still reads the old maximum).
- Copy by column name, not `SELECT *`. The header states that it supersedes migration 105's sentence "THE REASON VOCABULARY HAS ONE VALUE, deliberately" (105 is immutable and is not edited) and that 105's sentence on skimmed figures still holds (item 1).
- The commit carries the migrated `data/guidebook.db` and the regenerated `governance/context-map.yaml` (its `schema_version` and `db_fingerprint` lines change).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `extraction_follow_ups`, `read-outside-admitting-purpose`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base (pilots counted 109 failures, so 109 is the base state, not yours); only a number above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `extraction_follow_ups`: code and skills: `scripts/audit/extraction_follow_up_audit.py`, `scripts/db.py`, `scripts/tests/test_scan_contract.py`, `skills/run-pipeline_SKILL.md` (two lines; the pilot judged both mentions: the vocabulary is stated as the column's CHECK, which stays true). Views, triggers, indexes: the table and `ux_extraction_follow_ups_open`. Registry: none. Prose: `governance/context-map.yaml`, `governance/owner-browser.yaml`, `governance/stage-map.yaml`. Of these, `governance/context-map.yaml` is a **caller**: it is generated, and its header (`schema_version`, `db_fingerprint`) goes stale with any migration, which `context_map_fresh` reports; repair it by regenerating (section 4), never by hand. The other two are mentions (pilot 2026-11-13).
- `read-outside-admitting-purpose`: code and skills: `scripts/tests/test_scan_contract.py` (fixtures, still true: mentions). Prose: none.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`, `test_validate_evidence_state_2_4`, `extraction_follow_up_audit`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness test_assess_cell_pilot test_validate_evidence_state_2_4 extraction_follow_up_audit migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *(EXAMINED:|RESULTS|FAILED|VERDICT|ALL PASS|FAILURES|PASS: all|FAIL: )' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). The pattern is anchored at the start of a line: `test_author_presence` names `EXAMINED` inside its case titles, and an unanchored pattern fills the 200 characters with those and hides its summary `EXAMINED: … assertion(s)` line. A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. Two exceptions print no `EXAMINED:` line by design and are read by their case count instead: `test_assess_cell_pilot` (`grep -cE '^ +(PASS|FAIL): ' "$SCRATCH/before-test_assess_cell_pilot.txt"`, ending `PASS: all pilot-engine branch tests`) and `test_validate_evidence_state_2_4` (`grep -cE '^ +\[(PASS|FAIL)\] ' "$SCRATCH/before-test_validate_evidence_state_2_4.txt"`, ending `ALL PASS  (0 failed)`); report those counts as their subject. `extraction_follow_up_audit` prints `EXAMINED: 0` today (no follow-up raised, no live determination): it is vacuous before and after, and the new test case, not the audit, is what proves this change (pilot 2026-11-13).

**Step 2: red before, green after.** The probe is an absence finding chosen by query, never a typed id:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-012"
EID=$(python3 -I -c "import sqlite3;c=sqlite3.connect('file:$SCRATCH/t.db?mode=ro',uri=True);print(c.execute(\"select min(extraction_id) from source_value_extractions where claim_type='absent'\").fetchone()[0])"); echo "EID=$EID"
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py raise-follow-up --extraction-id "$EID" --reason absence-needs-tested-value --warrant 'TASK-FIXTURE' --session session_task-probe; echo "rc=$?"
```

Do not pipe the `db.py` call, or `rc=` reports the pipe. **Before:** `rc=2` and argparse's `invalid choice: 'absence-needs-tested-value' (choose from 'read-outside-admitting-purpose')` on stderr. That is the expected refusal: the `--reason` choices are read from the CHECK, so argparse refuses before the writer's own `Refusal` is reached; it is a usage error, not a `Refusal:` message, and that difference is not a defect. **After** (on a fresh copy of the migrated database, `cp data/guidebook.db "$SCRATCH/t2.db"` once the migration is applied, and `GUIDEBOOK_DB_PATH="$SCRATCH/t2.db"` on both calls): `rc=0` with a `follow_up_id`, and `db.py resolve-follow-up --follow-up-id <that id> --resolution 'TASK-FIXTURE' --session session_task-probe` closes it (`rc=0`). The same call with `--reason skimmed-needs-full-read` is refused before and after (section 4, item 1).

**The cases to add** to `scripts/tests/test_scan_contract.py`, after U08, reusing its `raise_fu`, `resolve_fu`, `refusal`, `attempt` and `record` helpers (the file copies `data/guidebook.db`, so the cases are red until the migration is applied to your working copy of it):
- `T012-01`: `raise_follow_up` with `absence-needs-tested-value` on the fixture extraction the U cases use (`E_FULL`, which the test writes itself; the writer does not read `claim_type`, and this task adds no refusal that would) writes an open follow-up; a second open one with the same reason is refused (`already has open`); `resolve_follow_up` closes it. Red before the migration, green after.
- `T012-02`, the red test for item 1's choice: `raise_follow_up` with `skimmed-needs-full-read` on the fixture's skimmed extraction (`E_ONLY_SKIM`) is refused with `CHECK`. It is green before and after the change, so show it can fail on a seeded defect. The test always copies `<repository>/data/guidebook.db` (it sets `GUIDEBOOK_DB_PATH` itself), so seed a scratch worktree, never the canonical file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-012"
git worktree add --detach "$SCRATCH/seed" HEAD && cp scripts/tests/test_scan_contract.py "$SCRATCH/seed/scripts/tests/" && cp "$SCRATCH/t.db" "$SCRATCH/seed/data/guidebook.db"
sed "s/'absence-needs-tested-value'/'absence-needs-tested-value', 'skimmed-needs-full-read'/" scripts/migrations/NNN_<slug>.sql > "$SCRATCH/seeded.sql"   # your migration, CHECK widened by the rejected value
python3 -I -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1]);c.executescript(open(sys.argv[2]).read());c.close()" "$SCRATCH/seed/data/guidebook.db" "$SCRATCH/seeded.sql"
(cd "$SCRATCH/seed" && python3 scripts/tests/test_scan_contract.py) | grep -F 'T012-02'   # must show ✗
git worktree remove --force "$SCRATCH/seed"
```

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T012-01`, `T012-02`, …) and confirm the prefix is free first (`grep -c '"T012-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `for c in $CHECKS; do echo "== $c"; diff <(grep -E '\[✗\]|\[FAIL\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|\[FAIL\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt"); done` (begin the block with the `SCRATCH` and `CHECKS` lines; `\[FAIL\]` is `test_validate_evidence_state_2_4`'s form). No failing case may appear that was not failing before; the `EXAMINED:` number (or, for the two tests above, the case count) may only change by the cases you added: `test_scan_contract` by two.

**Step 4: the gate, once.**

```
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes longer than two minutes** (pilots measured over 2 in a clone). Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots: 737 paths against 6). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.
- **An advisory FAIL in `gate.txt` on a check that is not in the before-run list** must be shown to be the base's, not yours, by running that check's registry `cmd` once on an unchanged worktree of the base and comparing (the pilot met several, all pre-existing: `scan_debt`, `verified_scan_integrity`, `research_protocol_audit`, `metadata_integrity_audit`, `validate_schema_cross_check`, `retired_vocabulary`, `research_dod`, `skill_vocabulary_audit`, `search_log_completeness`; re-derive, do not trust the list):

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-012"
if git rev-parse -q --verify origin/ccr-408aaa9b-z3e4s0 >/dev/null && ! git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline; then BASE=origin/ccr-408aaa9b-z3e4s0; else BASE=origin/main; fi
git worktree add --detach "$SCRATCH/base" "$(git merge-base HEAD "$BASE")"
c=<check id>; cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c)
(cd "$SCRATCH/base" && $cmd) > "$SCRATCH/base-$c.txt" 2>&1; echo "base rc=$?"; $cmd > "$SCRATCH/mine-$c.txt" 2>&1; echo "mine rc=$?"; diff "$SCRATCH/base-$c.txt" "$SCRATCH/mine-$c.txt" | head -20
git worktree remove --force "$SCRATCH/base"                 # when every such check is compared
```
  Same rc and the same failing lines: not yours; name it in the pull request. `search_log_completeness` can fail in the gate on WebSearch ledger lines of the running session and pass standalone (pilot 2026-11-13): that is the session's own search log, not this diff.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: widen extraction follow-up reasons for an absence finding [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- an owner entry later than 2026-11-12 asks for a follow-up row on a skimmed figure (`grep -n -F -e "skimmed-needs-full-read" -e "skimmed figure" references/project-standards.md`, read every hit dated after 2026-11-12): that ruling supersedes section 4 item 1's choice (CLAUDE.md rule 0), and adding the value is then the owner's word to carry out, not a design to re-argue;
- `git grep -l extraction_follow_ups -- 'scripts/migrations/data_*'` prints a file (the migration would then need an `AFTER_DATA` marker this file does not specify).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
