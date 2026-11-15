# T-055  Tooling for the mobility family: the devices it needs, and a parent's determination that gathers its children

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-055-report.md`, patch `.../T-055.patch` (stacked on the T-008, T-016, T-017, T-018 and T-019 pilots); defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-055 |
| Title | Tooling for the mobility family: the devices it needs, and a parent's determination that gathers its children |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OD-14 (owner, 2026-11-12, third set: decompose `MOB` by device); the owner's statement of 2026-11-12 (second) on unifying at an abstract vantage; T-102's design |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-019 merged (it carries T-018's link table, `v_live_lens_links`, and the engine's `_lens_clause`, which this task widens); and the design `T-102-design.md` present (it names the `device_class` values and the children; this task builds only what it names). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Not a precondition of its own: the stress harness.** An earlier version of section 6 asked for "the stress harness of T-014" without naming it here. That harness is in `$BASE` anyway (T-019 needs T-016, which needs it), but this task does not run it: its write-path steps clone the committed `HEAD` (T-014 section 4 item 1j), and this task commits only after the gate. The claim the harness would have guarded, that no existing cell changes, is proved more directly by section 6 step 2c, which determines every live identity cell on the unchanged code and on yours and compares them byte for byte.
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words.
  - **OD-14** — answered by the owner, 2026-11-12 (third set): MOB decomposed by device (`grep -n -F "OD-14: MOB is decomposed by device" references/project-standards.md`). Check: `grep -F "OD-14 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`.
- **Tests that must be red (or green) before you start:** `device_class` has no value for a prosthesis, crutches or a cane, and the engine does not read `parent_code` (section 3). T-019's live cases T019-13, T019-14 and T019-15 in `scripts/tests/test_assess_cell_pilot.py` are green: they assume a cell depends only on the figures carrying its own code, which stays true only while no code has a child, so they go red the day T-102 mints one. This task repairs them (section 4 item 4).
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-055-mobility-family-tooling "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-055" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The owner decomposed `MOB` by device. Wheelchair drive is already a typed descriptor (`device_class`), but the column cannot say "prosthesis", "crutches" or "cane", so a figure about those users would carry its device in prose or as an identity code (a second home, rule 5). And a determination at the parent `MOB` gathers only figures tagged `MOB`, so the family's commonality is lost.

**Evidence command** (read-only):

```
python3 -I -c "import sys,sqlite3;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(sorted(dbcore.check_values(c,'source_value_extractions','device_class')))"
grep -c parent_code scripts/assess/assess_cell.py
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from base_taxonomy_identity where parent_code is not null').fetchone()[0])"
```

**Expected output today:** a list of the chair, walker, scooter, `mixed` and `not_device_scoped` values with none of `lower_limb_prosthesis`, `crutches`, `cane` (the vocabulary is read from the column's own CHECK, the way the writers read it); `0`; `0` (no code has a parent yet, which section 4 item 5 relies on). If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

Locate code by symbol, never by line number. The pilot's patch (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-055.patch`) built every item below and may be read as a worked example; it was made on a stack, so derive its numbers again and never apply it.

1. **Schema migration: widen the `device_class` CHECK on `source_value_extractions`** by exactly the values `T-102-design.md` section 4 names: `lower_limb_prosthesis`, `crutches`, `cane` (the design keeps no upper-limb prosthesis value). Keep every existing value. If the design asks for the vocabulary as a table rather than a CHECK (the owner's "no hard-coded behaviours"), stop and report: that is a larger change to propose, not to improvise.
   - **Number.** Never type it: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one, zero-padded; file `scripts/migrations/NNN_device_class_mobility_values.sql`, ending `PRAGMA user_version = NNN;`.
   - **Shape.** SQLite cannot change a CHECK in place, so the table is rebuilt. Follow `scripts/migrations/114_extraction_slug_and_root.sql` step for step, and T-018's own rebuild of the same table (`ls scripts/migrations/*_extraction_lens_links.sql`) as the newest model: capture `sqlite_sequence` into a temporary table (the table is AUTOINCREMENT and `DROP TABLE` takes its row); drop every view whose SQL names the table, a view that reads another listed view before the one it reads; create `_NNN_new_source_value_extractions`; copy by column name (`INSERT INTO … (<every column>) SELECT <same> FROM source_value_extractions`); drop the old table; rename the new one (the foreign keys of other tables into it name it by text, so they resolve to the rebuilt table and are not rebuilt); recreate every index from its stored SQL; restore the sequence floor as 114 does; recreate every view from its stored SQL, verbatim. List the objects at execution: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where sql like '%source_value_extractions%' and name<>'source_value_extractions'\").fetchall())"`.
   - **Generate the file from `sqlite_master`; do not hand-type the table.** Read the `CREATE TABLE`, index and view SQL with Python from a scratch copy of `$BASE`'s database and write them out, with one substitution: the `device_class IN (…)` list gains the three values. Every other column, CHECK, default and comment is carried as it stands, T-018's CHECK holding the four retired lens columns NULL among them. Prove the substitution is the only change: `diff` the stored `CREATE TABLE` text against your new one (with the temporary name put back) prints only the line or lines of that list. Say in the migration's header that it was generated, from what, and that it widens a CHECK for OD-14 and `T-102-design.md` section 4.
   - **No `AFTER_DATA` marker.** T-018's migration carries one, and `scripts/migrate_db.py` makes "this migration, and every migration numbered after it" wait for the data it names (`grep -n -A4 'AFTER_DATA: YYYYMMDDHHMMSS' scripts/migrate_db.py`, in `build_plan`'s docstring), so this rebuild already runs after the data on a rebuild. It copies rows and widens a CHECK, so it needs no marker of its own.
   - **Apply and prove.** Apply it only with `python3 scripts/migrate_db.py`. Then: `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` exits 0; `python3 scripts/audit/migration_reproducibility.py --deep` passes; every row of `source_value_extractions` and of `extraction_lens_links` is identical before and after, every column compared (keep `cp data/guidebook.db "$SCRATCH/pre.db"` before you apply it, and compare with `ATTACH`); the `sqlite_sequence` value of the table is unchanged; the set of tables, indexes and views is unchanged and each view's SQL is byte-identical; `PRAGMA foreign_key_check` prints nothing and `PRAGMA integrity_check` prints `ok`. Run `python3 scripts/audit/joined_cells_census.py` before and after (CLAUDE.md §4); the candidate count must not change.
   - **Regenerate the context map** after the migration and the engine change (item 2), and before the gate: `python3 scripts/generate/context_map.py`, then `python3 scripts/generate/context_map.py --check` (exit 0). The migration moves `schema_version` and the fingerprint in `governance/context-map.yaml`, and the test fixture of item 3 adds `base_taxonomy_identity` to that test's writer list; `context_map_fresh` is red until you do.
   - **`amend-extraction`.** Add `device_class` to `_AMENDABLE_SVE_FIELDS` in `scripts/db.py`, with a dated comment saying why (T-102 records a figure's stated device on a row already written; the engine does not read the column). The existing `--reason` requirement and the column's own CHECK (through `dbcore.check_values`) are its gates; add no code for them. The `--field` choices are derived from that set, so `add-extraction`'s and `amend-extraction`'s help gain the values with no edit; two help strings of `amend-extraction` are already false and become more so (`grep -n -e 'figure_role or comparator' -e 'ONLY these two' scripts/db.py`): correct them to name "the amendable fields (`--field`)".
2. **The engine's gather: change only `_lens_clause`** in `scripts/assess/assess_cell.py` (the function T-019 added). Every gather, `count_extractions` and `gather_extraction_links`'s in-lens set already go through it (`grep -n '_lens_clause(' scripts/assess/assess_cell.py`), so one edit reaches them all, including OD-08's absent-cell refusal: a parent with no figure of its own but with its children's figures has a cell. A determination keyed on an identity code gathers figures with a live link to that code **or to any code whose `parent_code` chain reaches it**, derived from `base_taxonomy_identity` on every call, never a list. A child's determination gathers only the child and its own descendants. The other three lenses are unchanged (only the identity lens has a hierarchy). Write it exactly in this form, beside `_lens_clause`:
   ```python
   # The identity lens is the one lens with a hierarchy (base_taxonomy_identity.parent_code): a cell keyed on a code
   # gathers the figures linked to that code or to any code whose parent_code chain reaches it (T-055). Derived from
   # the registry on every gather, never a list. UNION, not UNION ALL, so a cycle ends.
   _IDENTITY_FAMILY = ("(WITH RECURSIVE family AS (SELECT ? AS code UNION SELECT i.identity_code "
                       "FROM base_taxonomy_identity i JOIN family f ON i.parent_code = f.code) "
                       "SELECT code FROM family)")
   ```
   and in `_lens_clause`, for `c == "identity_code"`, put `k.identity_code IN {_IDENTITY_FAMILY}` where the other lenses keep `k.{c} = ?` (the one parameter is still `lens[c]`). Two things about this form are required, not style:
   - **No column list on the CTE.** `T-018-design.md` section 4 sketches `WITH RECURSIVE family(code) AS (…)`. The blocking `schema_reference_audit` recognises a CTE name only by `WITH [RECURSIVE] <name> AS` (`grep -n 'RECURSIVE' scripts/audit/schema_reference_audit.py`), so with a column list it reads `family` as a table the schema lacks: `MISSING: family`, `RESULT: FAIL` (pilot, 2026-11-13). The form above names the column inside (`SELECT ? AS code`) and passes.
   - **A parenthesised subquery inside the `IN`, not a top-level `WITH`.** The engine splices `_lens_clause`'s text into the `WHERE` of five different `SELECT`s, so there is no statement head to put a `WITH` on.
   **A figure is gathered once** [2026-11-12, OI-13 fold]: the children are not mutually exclusive (a figure may carry `WHEEL` and `WALKAID` links), so the family predicate stays inside the per-figure `EXISTS`, never a join on the links, and no count downstream (governing figures, sources, convergence roots) multiplies by the number of links. Update the docstring of `_lens_clause` to say so. In `gather_extraction_links`, the `excluded` reason becomes "… carries every code the cell states (an identity code counts through its `parent_code` chain); …": keep its prefix `not stated in this cell's lens (` exactly, because T-019's cases match it. (`SCI` is retired to `WHEEL` and `LMB` becomes `UPL`, outside the family, by T-102 and T-116; neither changes this task. The ninth set replaced the child `PROSTH` by `LLD`, people with lower-limb differences, defined by the condition: `lower_limb_prosthesis` stays a `device_class` value, a descriptor of the device a figure concerns, and is still added here; it is not a second home of `LLD`, `T-102-design.md` §0. Whether a parameter may be determined at `MOB` at all, the design-equivalence test, is T-110's; the engine does not enforce it and this task does not add it.)
3. **The engine's fixture, `synth_db` in `scripts/tests/test_assess_cell_pilot.py`** (a caller: once the identity lens reads `base_taxonomy_identity`, every synthetic determination keyed on an identity raises `no such table`). T-019 rewrote `synth_db` onto link rows (its item 8) and merges first; edit its version. Add to the fixture schema, unconditionally, `CREATE TABLE base_taxonomy_identity (identity_code TEXT PRIMARY KEY, parent_code TEXT REFERENCES base_taxonomy_identity(identity_code))`, and a keyword `family=()` of `(child, parent)` pairs that inserts both codes and sets the child's `parent_code`. Empty by default, so every code is a root and every existing case keeps its meaning. This fixture table is named here; section 8's "do not add a table" does not forbid it.
4. **T-019's live cases, made family-aware** (same file; a caller: green today, red the day T-102 mints a child). T019-13 compares the figures a cell reaches with those carrying the cell's own code; T019-14 does the same for the other group's cell; T019-15 picks a registry identity that no figure of a parameter carries and expects the refusal, but a parent whose children carry figures is not refused. In each, replace "carries the code" by "carries the code or one of its descendants' codes", with the family computed **in Python** from `SELECT identity_code, parent_code FROM base_taxonomy_identity` (independent of the engine's SQL, so a defect in `_IDENTITY_FAMILY` cannot hide itself, and no SQL CTE for the audit to misread); for T019-15, choose a code none of whose family carries a figure of the parameter. Today every family is one code, so the three cases are unchanged in effect; say so in the pull request.
5. **`RULE_VERSION` is not bumped.** In this engine the label names a change in what the engine answers for the same inputs (folded T-017 section 4 item 2: "The partition changes what the engine answers for the same links, so the label changes"). Here: (a) on the registry this task merges into, no code has a parent (section 3's third line prints `0`), so every cell gathers exactly the figures it gathered before, and section 6 step 2c proves it by an identical `derivation_sha` for every live identity cell (identical shas need an unchanged label); (b) once T-102 gives `MOB` children, a parent's cell gathers more figures, and the figures and their roles are themselves in the sha payload (`grep -n 'def link_payload' scripts/assess/assess_cell.py`), so the sha moves with no label; (c) `stale_determinations` examines only live rows stamped with the current label, so a bump would take every earlier live determination out of its subject, which are exactly the rows a new child could make stale. So do not run T-017's derivation command and do not touch `LEGACY_SHA_VERSIONS` or `COALESCE_LENS_SHA_VERSIONS`. If step 2c shows any difference, the premise of (a) is false: stop (section 9).
6. **Grades are not inherited, in either direction; leave `population_match` as it is.** The owner's ruling of 2026-08-25 (`grep -n -F 'Not fanned out, ever' references/project-standards.md`; quoted in `T-102-design.md` section 6): "`evidence_population_match.study_population` is free text describing *the study's own* participants. A grade is a fact about a paper." `population_match` attributes a grade to a cell only when its `target_population` names the cell's own code. So when a parent's cell gathers a child's figure, that source has no grade there unless a row names the parent: its `population_directness` is `NOT_ASSESSED` (G2) and its consolidation is capped accordingly. Likewise a child's cell does not take a parent-level grade. A `MOB` determination will therefore read weaker than its children's on the same figures. That is the ruling applied, not a defect: do not widen `population_match` to the family, and say so in the pull request. Case T055-08 (section 6) holds it.
7. **Callers in prose and help:** `skills/run-pipeline_SKILL.md`, the sentence T-019 wrote ("a figure reaches a cell only through the live lens links written on it … every lens the cell states must be among them"): add that an identity code counts through `parent_code` (a parent's cell gathers its descendants' figures, once each; a child's cell only its own). The `amend-extraction` help strings of item 1.

**What reads what this task adds or changes:** `add-extraction` and `amend-extraction` read the `device_class` CHECK; every gather of the engine reads `_IDENTITY_FAMILY` through `_lens_clause`; `_lens_clause` reads `base_taxonomy_identity.parent_code`; the `synth_db` fixture's `base_taxonomy_identity` is read by `_lens_clause` in the tests; T-102 (rows, `amend-extraction --field device_class`) and T-110 (parent determinations). Nothing becomes deletable.

**Flag names, for any test or command that writes a figure or a link.** As folded T-018 defines them: `add-extraction` and `derive-extraction` take the warrant as `--lens-basis` and `--lens-basis-text` (Python payload keys `lens_basis` and `lens_basis_text`); `add-lens-link` takes `--basis` and `--basis-text`, the names `T-102-design.md` section 9 also uses. Reuse the payload builder or CLI helper T-018 left in the test file you edit; do not write a lens column on a figure (T-018's CHECK refuses it).

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`, so new files count) and, for anything added, what reads it. In a pilot stacked on other pilots' patches the merge-base also counts the predecessors' work: measure your own commit with `HEAD~1` in place of the merge-base, and say so.

## 5. Caller sweep

Names to sweep: `device_class`, `parent_code`, `_lens_clause`, `_AMENDABLE_SVE_FIELDS`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean. This task changes an exclusion reason and no refusal; the pilot ran it anyway and saw the same failure count before and after.

**The name sweep misses the callers that matter most here, because the behaviour changes and the names do not.** Also:
1. **Grep for the behaviour:** `git grep -n -i -E 'only through the live lens links|every lens the cell states|carries (its|the cell.s) (identity )?code' -- skills governance architecture .claude scripts CLAUDE.md ':(exclude)scripts/migrations'`. Judge each hit by the definition above.
2. **Run every registered check that reads what you change**, before and after (section 6 step 1 derives the list). A check that goes red after the change is a caller even when no name in it changed.
3. **Regenerate the context map** (section 4 item 1) and confirm `context_map.py --check` exits 0.

**Hits when this file was written** (pilot, 2026-11-13, on the stacked branch; re-run the commands, a new file in your output is a hit to judge):
- `device_class`: `scripts/db.py` (the `add-extraction` choices, already derived from the CHECK; `_SVE_VOCAB_COLUMNS`; the insert column list: mentions); `skills/connection-discovery_SKILL.md` and `skills/run-pipeline_SKILL.md` (list it among vocabularies: mentions); views, triggers, indexes: the table only; registry: none; prose: `governance/evidence-architecture.md` and `references/methodology/value-genealogy-worked-example-corridor-width.md` (mentions; the pilot's stack also showed `architecture/schema-spec.md` and `governance/context-map.yaml`, which the workplan branch did not on the same day: judge whatever your tree prints; the context map is regenerated, never edited).
- `parent_code`: `scripts/audit/graph/*.py` and `scripts/audit/graph_audit.py` (they read it for a cycle check, which `_IDENTITY_FAMILY`'s `UNION` does not need: mentions); `architecture/schema-spec.md` (an older `population` table's sketch: a mention).
- `_lens_clause`: `scripts/assess/assess_cell.py` (yours). Its behavioural callers: `scripts/tests/test_assess_cell_pilot.py` (`synth_db`, item 3; T019-13 to T019-15, item 4); `skills/run-pipeline_SKILL.md` (item 7); the `excluded` reason (item 2).
- `_AMENDABLE_SVE_FIELDS`: `scripts/db.py` (yours; the two help strings of item 1 are callers).
- Run before and after with no edit expected: `scripts/tests/test_scan_contract.py` (calls the gathers with a lens), `scripts/tests/test_run_pipeline_refusals.py` (runs the engine as a CLI), `scripts/tests/test_db_amend_writers.py` (your amend cases go here).

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `schema_reference_audit` (blocking; it reads the engine's SQL, section 4 item 2), `migration_reproducibility`, `test_db_integrity`, `context_map_fresh` (red after any migration until the map is regenerated), `test_assess_cell_pilot`, `test_db_amend_writers`, `test_run_pipeline_refusals`, `test_scan_contract`, `test_validate_evidence_state_2_4`, `derivation_handshake_integrity`, `derived_not_curated_audit` (blocking; it scans the engine and `db.py`). The list is typed, so derive the rest as well; this prints every registered check whose `cmd` names a file that names the engine, `amend-extraction` or `device_class`:
```
python3 -I -c "import yaml,subprocess;h=set(subprocess.run(['git','grep','-l','-E','assess_cell|amend-extraction|device_class','--','scripts',':(exclude)scripts/migrations'],capture_output=True,text=True).stdout.split());print(sorted((c['id'],c.get('level')) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if any(f in ' '.join(map(str,c.get('cmd') or [])) for f in h)))"
```
On 2026-11-13 it also printed `db_path_env_audit`, `extraction_follow_up_audit`, `medical_lens_integrity` and `verified_scan_integrity`: their scripts name these files in a path table or a message and do not call them, so they are mentions (the gate runs them). Add any other id it prints to `CHECKS`, or name it in the pull request as a mention with the reason. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="schema_reference_audit migration_reproducibility test_db_integrity context_map_fresh test_assess_cell_pilot test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_validate_evidence_state_2_4 derivation_handshake_integrity derived_not_curated_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. `test_assess_cell_pilot` and `test_validate_evidence_state_2_4` print no whole-run `EXAMINED:` line: report each as "no EXAMINED line", count its `PASS:` lines (`grep -c '^ *PASS:' "$SCRATCH/before-test_assess_cell_pilot.txt"`), and compare failing lines as for the rest. Ten cases of `test_db_integrity` examine nothing on the canonical database, K01 and K02 among them (no live determination): no registered check proves that the gather leaves a stored determination alone, which is why step 2c exists.

**Step 2: red before, green after.** Write the cases first, run them on the unchanged code (red), then make the change (green). Keep both outputs for the pull request.

*2a. The engine, in `scripts/tests/test_assess_cell_pilot.py`* (on `synth_db` with `family=`, section 4 item 3, unless marked live; the codes are fixture labels):

| Case | Fixture | Expect after | Before |
|---|---|---|---|
| T055-01 | a family `WHEEL` and `WALKAID` under `MOB`, and a grandchild under `WALKAID`; one figure linked to each of the four codes | the `MOB` cell's governing refs are all four sources | red |
| T055-02 | same | the `WALKAID` cell gathers only `WALKAID`'s and the grandchild's; the `WHEEL` cell only `WHEEL`'s (never the parent's, never a sibling's) | red |
| T055-03 | same figures, no `family` | the `MOB` cell gathers only the `MOB` figure (a code with no children is a root) | green (a guard) |
| T055-04 (OI-13) | **one** figure linked to `WHEEL` and `WALKAID`, plus a `MOB` figure | the `MOB` cell's governing-figure count equals the number of distinct extraction ids, and equals `n_extractions`; `n_sources` counts each source once | red; and red on a seeded defect: the family predicate written as a join on the links (the pilot's seeded join gave more governing rows than distinct ids), then removed |
| T055-05 (OD-08) | only a `WHEEL` figure, `WHEEL` under `MOB` | the `MOB` cell is not refused: the `WHEEL` figure governs it | red (refused "has no row") |
| T055-06 | as T055-05, the `WHEEL` link retired on the fixture's own table | the `MOB` cell is refused: a retired link carries nothing to the parent | green (a guard) |
| T055-07 (live copy) | a copy of the canonical database in a temporary directory, never the canonical file: two identity codes that live links carry on one parameter, chosen by query, the second carried by some figure that does not carry the first; on the copy, the second's `parent_code` set to the first | the first's cell reaches the union of both codes' figures; the second's reaches only its own; neither set empty | red |
| T055-08 (2026-08-25, "Not fanned out, ever") | as T055-05, with one `evidence_population_match` row on the `WHEEL` figure's source whose `target_population` is `WHEEL` and whose grade maps to a directness other than `NOT_ASSESSED` (take the value from `population_directness_from_match_grade`'s own mapping); and a second source, linked `WHEEL`, graded only against `MOB` | in the `MOB` cell, the first source's record has `population_directness == "NOT_ASSESSED"`; in the `WHEEL` cell it does not (the control, so the case can fail); in the `WHEEL` cell the second source's is `NOT_ASSESSED` | red (the `MOB` cell does not gather the source, so its record is absent); and red on a seeded defect: `population_match` widened to the family, then removed |

T055-07 needs a raw `UPDATE` of `parent_code` on the copy: that is a fixture write on a throwaway copy (section 8 forbids writing only `data/guidebook.db`), and the copy is the only way to seed a child before T-025 or T-102 writes one. Print the file's `SKIPPED-NO-FIXTURE` line if no parameter carries two identity codes. T019-13 to T019-15 are repaired as section 4 item 4 says; after the change they stay green.

*2b. The writers, in `scripts/tests/test_db_amend_writers.py`.* Number these on from the engine file's cases (`T055-11` onwards), so an id names one case. On the test's scratch copy, with figures written through the CLI (`add-extraction` with `--lens-basis` and `--lens-basis-text`, through the helper T-018 left in the file): `add-extraction --device-class <v>` stores each of the three new values (red before); an unknown value is refused and nothing is written (green before: argparse's derived choices; a guard); `amend-extraction --field device_class --value <v> --reason <words>` records a device on a row whose `device_class` is NULL, with the reason in `notes` (red before); it refuses a value outside the CHECK and a blank `--reason`, and the row keeps its value (red before: the field is not amendable); `dbcore.check_values(conn, "source_value_extractions", "device_class")` holds the three new values and every value it held before (red before). To get a NULL `device_class` on a written row, `UPDATE` the test's own copy, as a fixture.

*2c. Every live cell, before and after: nothing changes today.* The gather now reads the registry, and section 4 item 5 rests on the fact that no live cell changes while no code has a child. Prove it: determine every distinct (parameter, identity code) pair the live links carry, on the unchanged code and database (a worktree of the base) and on yours (after the migration), read-only, and compare:
```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-055"
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
git worktree add --detach "$SCRATCH/cells-wt" "$(git merge-base HEAD "$BASE")"
cells(){ python3 -I - "$1" > "$2" 2>&1 <<'PY'
import os, sqlite3, sys
root = sys.argv[1]; sys.path[:0] = [root, os.path.join(root, "scripts", "assess")]
from assess_cell import determine, Refusal, STORED_ANSWER
c = sqlite3.connect(f"file:{root}/data/guidebook.db?mode=ro", uri=True)
pairs = c.execute("SELECT DISTINCT x.parameter_id, l.identity_code FROM source_value_extractions x JOIN v_live_lens_links l "
                  "USING (extraction_id) WHERE l.identity_code IS NOT NULL ORDER BY 1, 2").fetchall()
print("EXAMINED:", len(pairs), "cells")
for pid, code in pairs:
    try:
        d = determine(c, pid, {"identity_code": code}, "", "t055-cells")
        print(pid, code, [d[k] for k in STORED_ANSWER], sorted((l["role"], l["extraction_id"]) for l in d["links"]))
    except Refusal as e:
        print(pid, code, "REFUSED", e)
PY
}
cells "$SCRATCH/cells-wt" "$SCRATCH/cells-before.txt"; cells "$PWD" "$SCRATCH/cells-after.txt"
head -1 "$SCRATCH/cells-before.txt"; diff "$SCRATCH/cells-before.txt" "$SCRATCH/cells-after.txt" && echo IDENTICAL
git worktree remove --force "$SCRATCH/cells-wt"
```
Expected: a non-zero `EXAMINED:` line and `IDENTICAL` (the stored answer, `derivation_sha` included, and every link role of every cell). Any difference is a stop (section 9): it means a code has a child already, or the change reaches beyond the identity lens.

*2d. The migration's proof* is in section 4 item 1 ("Apply and prove"); its outputs go in the pull request.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T055-01`, `T055-02`, …) and confirm the prefix is free first (`grep -c '"T055-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added (and `schema_reference_audit`'s by the SQL strings you added). `context_map_fresh` is green after you regenerate the map (section 4 item 1). The existing cases whose text changes are T019-13 to T019-15 (section 4 item 4); name them in the pull request.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards. Regenerate the context map (section 4 item 1) **before** the gate, so it is not the file you change afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **In a pilot stacked on other pilots' patches** (the predecessors applied as commits on your branch, not merged into `$BASE`), `--base "$BASE"` gates the predecessors' work too: run the gate with `--base HEAD` (the stack head, before your commit) and say so in the report.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.
- **An advisory FAIL in `gate.txt` on a check that is not in the before-run list** has no before-line to compare, and inference ("the diff touches no scan data") is not a measurement. Run that check's registry `cmd` once on an unchanged worktree of the base and compare (the pilot met `scan_debt`, `verified_scan_integrity`, `search_log_completeness`, `research_protocol_audit` and `metadata_integrity_audit` this way, none in the R2 baseline, and did not measure them; other pilots found the four besides `search_log_completeness` red on a pristine base; re-derive, do not trust the list):

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-055"
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
git worktree add --detach "$SCRATCH/base" "$(git merge-base HEAD "$BASE")"
c=<check id>; cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c)
(cd "$SCRATCH/base" && $cmd) > "$SCRATCH/base-$c.txt" 2>&1; echo "base rc=$?"; $cmd > "$SCRATCH/mine-$c.txt" 2>&1; echo "mine rc=$?"; diff "$SCRATCH/base-$c.txt" "$SCRATCH/mine-$c.txt" | head -20
git worktree remove --force "$SCRATCH/base"                 # when every such check is compared
```
  Same rc and the same failing lines: not yours; name it in the pull request with both results. Green on the base and red on yours: yours; fix it, re-run the gate once more, and say in the pull request that it ran twice and why. `search_log_completeness` can fail in the gate on WebSearch ledger lines of the running session and pass standalone (pilots, 2026-11-13): that is the session's own search log, not this diff; report both results.

**The canonical database:** it changes only by `scripts/migrate_db.py` applying your migration; record its `sha256sum` after that and say in the pull request that the rebuild reproduces it (section 4 item 1).

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: device values and a parent-gathering determination for the mobility family [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row (`specifications`, read through `v_best_practice`; CLAUDE.md §6's `best_practice_synthesis` names a table not in the schema: superseded in part by TERM-RESOLUTION-PLAN §2, 2026-11-14) or any synthesis prose. A Sonnet-class model is below that floor.
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
- the every-cell comparison of section 6 step 2c prints any difference, or `EXAMINED: 0` (the no-bump reasoning of section 4 item 5 then does not hold, and the label is not yours to re-decide);
- the generated migration differs from the stored `CREATE TABLE` text in more than the `device_class` list (section 4 item 1), or any row, sequence value, object or view text differs after it is applied;
- `schema_reference_audit` reports `MISSING: family` (the CTE was written with a column list, or outside the `IN`: correct it to section 4 item 2's form; a stop only if that form also fails);
- you find yourself widening `population_match` to the family, or a test that expects a parent's cell to carry a child's grade: the 2026-08-25 ruling forbids it (section 4 item 6).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it (the `synth_db` fixture, T019-13 to T019-15, the `excluded` reason, the skill sentence, the help strings, the context map); each check you ran with its `EXAMINED:` line, before and after; the red-before output of section 6 step 2 and the seeded defects of T055-04 and T055-08; the migration's proof (section 4 item 1); the every-cell comparison of step 2c; the statement that `RULE_VERSION` is not bumped, with the three reasons of section 4 item 5; the grade consequence of section 4 item 6 (a parent's determination does not inherit a child's grade, so it reads weaker); the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
