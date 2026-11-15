# T-018  The link table for several codes of one model on a figure

> **Design present.** The design this file waited for is committed beside it as `T-018-design.md` (2026-11-12): table `extraction_lens_links`, view `v_live_lens_links`, the four figure columns carried, NULLed and held NULL, two new verbs, the gather predicate T-019 builds. A Sonnet-class executor executes this file **exactly as that design specifies**; where this file and the design differ, the design governs. If the design leaves a column undecided, stop (section 9).

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-018-report.md`, patch `.../T-018.patch` (stacked on the T-008, T-016 and T-017 pilots); defects folded. If you find a further defect in this file, report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-018 |
| Title | The link table for several codes of one model on a figure |
| Wave | 1 (chain) |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class, executing `T-018-design.md` (see the note above) |
| Traces to | IMP-40 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-017 merged; `T-018-design.md` present. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** OD-39 — **answered by the owner, 2026-11-12 (fifth set):** "Yes, the 2026-11-06 ruling supersedes that clause" (`grep -n -F "OD-39: the 2026-11-06 link-table ruling supersedes" references/project-standards.md`): the 2026-08-28 clause "Never a `population_*` link table" is superseded, for a figure's lens codes, by the link-table ruling of 2026-11-06 (OR-1c). Check: `grep -F "OD-39 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`; any other value is a stop. Gate: `for n in OD-39; do gate $n; done` with the `gate` function of `REMEDIATION-WORKPLAN.md` §13. **How to read the gate's words.** `OPEN` means the decision is in force and you may proceed: `OPEN (owner)` is a decision the owner answered, which is what OD-39 is, so the expected line is `OD-39 OPEN (owner)`. `CLOSED` means stop. The ledger's OD-39 answer line ends "T-018 appends the SUPERSEDES/BY pair and builds extraction_lens_links"; that clause is stale. It was written before the fifth-set fold found that the audit cannot anchor such a pair on a target inside the ledger, and the ledger is append-only, so the line stays as written. Follow `T-018-design.md` section 5, step 6 (a prose entry, no machine pair), as section 4 item 2 below says.
- **Not a precondition: T-054.** T-054 (`tasks/T-054-identity-retires-to-need.md`) builds the identity successor and the `retire-identity` verb. T-018 does not wait for it, and T-054 does not wait for T-018: T-054's own dependency bullet reads "none", and T-102 waits for both. In this task, the writers refuse a `deprecated` identity code with a plain refusal that names no successor, because no successor column exists until T-054 adds one. T-054 extends that refusal to name the successor and counts live links in `retire-identity`. If T-054 has merged first (`git grep -n 'def retire_identity' scripts/db.py` prints a line), call its refusal helper instead of writing a second one (locate it by symbol). Then confirm on a scratch copy that `retire-identity` refuses a code that a live link carries and ignores a retired link. If it counts a retired link, stop (section 9): the defect is in T-054's derivation.
- **Tests that must be red (or green) before you start:** AT-32 red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-018-link-table "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-018" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

A figure that concerns two ICF codes, or two identity groups, must be written twice or lose one. The owner ruled a link table ("link table unless that is more prone to errors").

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
grep -n -F 'link table unless that is more prone to errors' references/project-standards.md; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select sum(identity_code is not null), sum(icf_code is not null), sum(needs_code is not null) from source_value_extractions\").fetchall())"
```

**Expected output today:** The ruling line; almost every figure carries an identity code only.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Build the table, the view and the migration exactly as `T-018-design.md` sections 2, 3 and 5 specify (`extraction_lens_links`, `v_live_lens_links`; the four lens columns on `source_value_extractions` carried into the table, NULLed, and held NULL by CHECK; the migration carries an `AFTER_DATA` marker). The ledger leaves the shape to this tooling pull request; it does not say the table must precede the lens fix: that order is the audit's, chosen so the gather is written once.
2. Writers, as the design's section 6 specifies: `add-extraction` and `derive-extraction` accept repeated lens arguments with `--lens-basis` and `--lens-basis-text` and write the links; two new verbs, `add-lens-link` and `retire-lens-link`. `amend-extraction` is **not** changed (the design corrects this file's earlier wording). The capture set includes the new table (it is derived: check `dbcore.writable_tables`). Record the supersession in the ledger as the design's section 5, step 6 now says (corrected 2026-11-12 after OD-39): **a prose entry, not a machine `SUPERSEDES:`/`BY:` pair**, because `supersession_backpointer_audit` cannot anchor a target that is itself in the ledger (the citation line is a second occurrence of the target quote, the quote already occurs twice under the audit's normalisation, and the marker it requires must sit beside the immutable 2026-08-28 paragraph); writing the pair would turn that check red. Run `python3 scripts/audit/supersession_backpointer_audit.py` before and after; its verdict must not change.
3. Repair the callers the design's section 9 lists, and add the integrity case and the tests of its section 10. The Python API takes the warrant as two payload keys, `lens_basis` and `lens_basis_text`, and each lens key takes one code or a list (design section 6, "The Python API"). Every test call site the design lists there is repaired through its payload builder.
4. **Emit a table's UPDATEs before its INSERTs in `scripts/research/emit_batch_sql.py`** (function `emit`, the line that appends `inserts + updates`; locate it by symbol). Today the emitter writes a table's new rows before its changed ones. So a batch in which `add-lens-link` replaces a carried link emits the judged link's INSERT while the carried link is still live, and applying the batch fails with `UNIQUE constraint failed: index 'ux_extraction_lens_live'` (pilot, 2026-11-13). This is the main write path of T-106, T-102 and T-115. Change only the order, to `updates + inserts`, and replace the comment above it with the reason. With the UPDATEs first, the rows already in the table reach their final form before any new row arrives, so every row present at each step is a row of the batch's end state, and every UNIQUE index, partial or not, holds at each step. The foreign keys need no ordering: `migrate_db.py` applies a migration with foreign keys off and checks them once at the end (`grep -n 'def _apply_atomically' scripts/migrate_db.py`). The same change makes a retired-and-redetermined `specifications` cell replayable, since it has the same partial-unique shape (`idx_spec_row_identity`). Do not instead make `add-lens-link` write the retirement first: the emitter diffs end states and never sees the order in which a verb wrote. Do not weaken `ux_extraction_lens_live`. The round-trip test is T018-08 (section 6 and design section 10).
5. **Place the new table in `governance/stage-map.yaml`:** one line, `extraction_lens_links: judgment`, in alphabetical order under `tables:`, with a dated comment in the file's own style saying who judged it and why. The reasons: a figure's lens codes are the crossing, which is judgment's output (CLAUDE.md §6); the table's parent row, `source_value_extractions`, is already `judgment`; and its other foreign keys point into `base`, which is not a stage, so the table crosses no stage. `build_graph.py --check` fails with "tables in the schema but not in stage-map" without this line, and the sweep's grep does not find it because the map does not name the lens columns.
6. **Repair every raw write of a lens column on a figure.** The all-NULL CHECK refuses any hand-written `INSERT INTO source_value_extractions` that names a lens column. The fixtures that do this are callers: `scripts/audit/research_batch_dod.py` (its `selftest` corpus is cloned from the live schema, and the registered **blocking** check `research_dod_selftest` dies with `IntegrityError: CHECK constraint failed` until the fixture is repaired) and `scripts/tests/test_scan_contract.py` (three INSERTs). Write each fixture figure without lens columns and add one `extraction_lens_links` row for it (basis `carried`, which needs no basis text, is the form a fixture standing for a pre-existing figure may take). Find them all with the raw-write sweep of section 5. A fixture that builds its own schema (`scripts/tests/test_assess_cell_pilot.py`) is a mention: its table is not the live one.

**What reads what this task adds or changes:** The engine's gather (T-019, then T-055's parent widening), `add-extraction`, the `retire-identity` live-row refusal (T-054), the lens re-tagging (T-106), the mobility split (T-102), the `ALL` re-tag (T-115). The emitter's order (item 4) is read by every research batch's data migration that changes and adds rows in one table, first those of T-106, T-102 and T-115. The stage-map line (item 5) is read by `build_graph.py --check`.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). **Before you apply it, keep the pre-migration database: `cp data/guidebook.db "$SCRATCH/pre.db"`.** The one-time carry assertion of section 6 reads it. Apply the migration only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). **The migration's `AFTER_DATA` timestamp is a hazard for data migrations captured elsewhere.** Once this migration is in, its all-NULL CHECK refuses any data migration that is replayed after it and INSERTs a lens column. That includes a research batch captured before this pull request merges but merged after it. Such a batch must be captured again through the new verbs once this one merges; say so in the pull request body. If a data migration merges into `$BASE` while you work, derive the `AFTER_DATA` timestamp again (design section 3, item 4), as well as the number (section 11, step 5). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name. (In a pilot stacked on other pilots' patches, that base also counts the predecessors' work: measure your own commit with `HEAD~1` in place of the merge-base.)

## 5. Caller sweep

Names to sweep: `identity_code`, `icf_code`, `needs_code`, `medical_code`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
**The raw-write sweep.** The CHECK this task inverts refuses a hand-written INSERT that names a lens column, and the name sweep above lists such a file without telling you which line writes. This line prints each raw INSERT into the figures table whose next four lines name a lens column. Each hit in a fixture cloned from the live schema is a caller (section 4, item 6):
```
git grep -n -A4 -E 'INSERT( OR [A-Z]+)? INTO "?source_value_extractions' -- scripts .claude skills ':(exclude)scripts/migrations' | grep -E 'INSERT|identity_code|icf_code|needs_code|medical_code'
```
On 2026-11-13 it printed `scripts/audit/research_batch_dod.py`, `scripts/tests/test_scan_contract.py` (callers), `scripts/tests/test_assess_cell_pilot.py` (its own fixture schema: a mention) and `scripts/db.py`'s own writer.

If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `identity_code`: code and skills: `schemas/evidence_state.py`, `scripts/assess/assess_cell.py`, `scripts/audit/derivation_handshake_integrity.py`, `scripts/audit/graph/extract_db.py`, `scripts/audit/graph_audit.py`, `scripts/audit/medical_lens_integrity.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/db.py`, `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py` and others (the command lists them all). Prose: `architecture/meta-scripts-spec.md`, `architecture/schema-spec.md`, `governance/context-map.yaml`, `governance/evidence-architecture.md`, `governance/owner-browser.yaml`, `governance/population-taxonomy.md`, `governance/retired-vocabulary.yaml`, `workplan/pipeline-state-graph/machines.yaml`.
- `icf_code`: code and skills: `schemas/evidence_state.py`, `scripts/assess/assess_cell.py`, `scripts/audit/derivation_handshake_integrity.py`, `scripts/audit/medical_lens_integrity.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/db.py`, `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/tests/test_validate_evidence_state_2_4.py`, `scripts/validate_evidence_state.py` and others (the command lists them all). Prose: `architecture/meta-scripts-spec.md`, `architecture/schema-spec.md`, `governance/context-map.yaml`, `governance/evidence-architecture.md`, `governance/functional-taxonomy.md`.
- `needs_code`: code and skills: `schemas/evidence_state.py`, `scripts/assess/assess_cell.py`, `scripts/audit/medical_lens_integrity.py`, `scripts/db.py`, `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_scan_contract.py`, `scripts/validate_evidence_state.py`, `scripts/validate_verification_consistency.py`. Prose: `architecture/meta-scripts-spec.md`, `architecture/schema-spec.md`, `governance/context-map.yaml`, `governance/evidence-architecture.md`.
- `medical_code`: code and skills: `schemas/evidence_state.py`, `scripts/assess/assess_cell.py`, `scripts/audit/medical_lens_integrity.py`, `scripts/db.py`, `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_scan_contract.py`, `scripts/validate_evidence_state.py`, `scripts/validate_verification_consistency.py`. Prose: `architecture/meta-scripts-spec.md`, `architecture/schema-spec.md`, `governance/context-map.yaml`, `governance/evidence-architecture.md`, `governance/pipeline-contract.yaml`.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`, `test_validate_evidence_state_2_4`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`, `research_dod_selftest` (blocking; it builds its corpus from the live schema and raw-INSERTs a figure with a lens column, so it crashes after the migration until its fixture is repaired, section 4 item 6). The list is typed, so derive the rest as well. This prints every registered check whose `cmd` names a file that the sweep of section 5 hits, or one of the two scripts this task edits besides the migration:
```
python3 -I -c "import yaml,subprocess;h=set(subprocess.run(['git','grep','-l','-E','identity_code|icf_code|needs_code|medical_code','--','scripts',':(exclude)scripts/migrations'],capture_output=True,text=True).stdout.split())|{'scripts/db.py','scripts/research/emit_batch_sql.py'};print(sorted((c['id'],c.get('level')) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if any(f in ' '.join(map(str,c.get('cmd') or [])) for f in h)))"
```
Add each id it prints that is missing from `CHECKS` to `CHECKS`, unless its `cmd` carries a placeholder such as `@SESSION@`, which only the gate fills. Or name it in the pull request as a mention, with the reason; for example, its script reads `specifications`' lens columns, not the figure's (design section 9, last row). Run each check as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness test_assess_cell_pilot test_validate_evidence_state_2_4 migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit research_dod_selftest"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. Three are known to print no whole-run line (pilot, 2026-11-13). `test_assess_cell_pilot` prints "PASS: all pilot-engine branch tests" and `test_validate_evidence_state_2_4` prints "ALL PASS (0 failed)"; `test_author_presence` prints only per-case `EXAMINED:` lines. Report each as "no EXAMINED line" before and after, and compare their failing lines as for the rest.

**Step 2: red before, green after.** AT-32 (first half): on a scratch copy a figure concerning two ICF codes is stored once with two links; before, the second code has nowhere to go. The cases, their probes and their expected red output today are in `T-018-design.md` section 10: T018-01 to T018-05, T018-07 and T018-08. AT-32's second half (a determination lists every model its governing figures carry) is T-019's. **A case must report red, not crash.** On the unchanged code there is no `--lens-basis`, no `v_live_lens_links` and no `add-lens-link`. Guard every read of the new table or view, so that the case records `[✗]` with the reason and the later cases still run. A case whose probe cannot exist on the unchanged schema records a failure; it does not print `SKIPPED-NO-FIXTURE`.

**The carry assertion (once, not a test file).** That every carried link matches the lens columns of the same figure before the migration is a property of this migration's single run. No pre-migration copy exists in the repository once the migration is committed, and the carried set rightly shrinks as later batches retire links. So it is not a committed case (the design's former T018-06). Run this once, straight after `migrate_db.py` applies the migration and before any other write, against the `pre.db` kept in section 4. Paste the command and its output into the pull request body:
```
python3 -I - "$SCRATCH/pre.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
c.execute("ATTACH ? AS p", (f"file:{sys.argv[1]}?mode=ro",))
L = ("identity_code", "icf_code", "needs_code", "medical_code")
pre = {(e, k, v) for k in L for e, v in c.execute(f"SELECT extraction_id, {k} FROM p.source_value_extractions WHERE {k} IS NOT NULL")}
car = {(e, k, v) for k in L for e, v in c.execute(f"SELECT extraction_id, {k} FROM extraction_lens_links WHERE basis='carried' AND {k} IS NOT NULL")}
stamp = c.execute("SELECT COUNT(*) FROM extraction_lens_links k JOIN p.source_value_extractions x USING (extraction_id) WHERE k.basis='carried' AND (k.created_at IS NOT x.created_at OR k.created_by_session IS NOT x.created_by_session)").fetchone()[0]
left = c.execute("SELECT COUNT(*) FROM source_value_extractions WHERE COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL").fetchone()[0]
print("EXAMINED:", len(pre), "| carried:", len(car), "| equal:", pre == car, "| stamp mismatches:", stamp, "| lens values left on figures:", left)
PY
```
Expected: a non-zero `EXAMINED`, `equal: True`, and `0` for both the stamp mismatches and the values left on figures. Any other output is a stop (section 9). The design's step 3 lets a figure whose `created_by_session` is NULL take the migration's stem; for such a figure the stamp line counts a mismatch. Name those figures in the pull request instead.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T018-01`, `T018-02`, …) and confirm the prefix is free first (`grep -c '"T018-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: add the lens link table for figures [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- The design file is missing or leaves a column undecided.
- the one-time carry assertion of section 6 prints anything other than the expected output, other than the stamp mismatches the design's NULL-session clause explains;
- T-054 has merged first and its `retire-identity` counts a retired link as live (section 2, "Not a precondition: T-054").

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the one-time carry assertion and its output (section 6); the note that a research batch captured before this merges, holding an INSERT of a lens column, must be captured again (section 4); the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4. If the merge brought a new `scripts/migrations/data_*.sql`, derive the `AFTER_DATA` timestamp again too, and repeat the rebuild and `--deep`. Repeat the carry assertion with the base's own database as `pre.db` (`git show "$BASE:data/guidebook.db" > "$SCRATCH/pre.db"`).
