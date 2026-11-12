# T-049  A typed home for translations, attached by pointer and callable from any stage

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-049 |
| Title | A typed home for translations, attached by pointer and callable from any stage |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | REQ-104 (owner statements 2026-11-12, ninth and tenth); AT-107, AT-108, AT-109 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-008 merged (the fidelity rule uses its number reader). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Delegated resolutions this task rests on.** OD-30: any model may draft a translation; a translation is shown to a reader only once reviewed by an Opus-class instance other than its translator. Each is a resolution by an Opus-class model under the owner's delegation of 2026-11-12: not the owner's words, reversible by the owner, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-30; do gate $n; done
```
- **Tests that must be red (or green) before you start:** AT-107, AT-108 and AT-109 red: no table, no verb. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0); echo "BASE=$BASE"
git switch -c task/t-049-translation-home "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-049" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The pipeline holds quotations, terms, clauses and titles in many languages and has nowhere to put a translation of any of them. So text in different languages cannot be compared or discussed together, or a session translates in its head and the translation is lost, or, worse, an English paraphrase is written where the source's words should be and is later read as the source's. The owner asked that everything non-English be translated, "probably at synthesis or whatever we need".

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from sqlite_master where name like '%translat%'\").fetchall())"; python3 scripts/db.py --help | tr ',' '\n' | grep -c -i translat; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from source_value_extractions x join evidence_sources e using(ref_id) where upper(coalesce(e.lang_detected,'EN'))<>'EN'\").fetchall())"; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from term_aliases where alias_type='TRANSLATION'\").fetchall())"; grep -c -i 'translation' governance/pipeline-contract.yaml
```

**Expected output today:** `[]` and `0`: no table and no verb. A non-zero count of figures whose source is recorded in a language other than English (a lower bound: the language column is NULL or inconsistently cased on many sources until T-015). A large count of aliases typed `TRANSLATION`, which are a different thing (see item 6). `0`: the contract says nothing about translation.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **One table, `translations`, by schema migration.** A translation points at the cell it translates and never replaces or copies it. Columns: `translation_id` (integer key); the pointer `source_table`, `source_column`, `source_row_key` (the row's primary-key value as text); `source_sha256` (the hash of the cell's text when it was translated, so a later change to the original is seen; a hash is not a copy); `target_language`; `translated_text` (NULL only while requested); `status` with a CHECK (`requested`, `translated`, `reviewed`, `rejected`); `translator_kind` with a CHECK (`model`, `tool`, `person`) and `translator_name` (the model id, the tool and version, or the person), both required once `status` is past `requested`; `requested_at_stage` (the stage that asked); `due_stage` (NULL means the rule of item 4 decides; a value is an explicit override for this row); `reviewed_by_kind`, `reviewed_by_name`, `reviewed_at`, required exactly when `status` is `reviewed` or `rejected`; `superseded_by_translation_id` (a corrected translation is a new row; the old one is retired in place); and the four session and time columns every table carries. CHECKs hold those consistency rules. There is no column that says "this is a translation": the table is the mark, and a flag that is always true informs nobody.
2. **One view, `v_translations_current`:** rows that are `translated` or `reviewed` and not superseded. It is the only read surface. It never names `translated_text` as if it were a source column, and nothing joins it into a view under the name of the column it translates.
3. **Three verbs in `scripts/db.py`,** each refusing what it should. `request-translation` (pointer, `--target-language`, `--stage`): validates the pointer against the live schema (the table and column exist, by `sqlite_master` and `PRAGMA table_info`; the row exists by its primary key; the cell is text and not empty). It reads the cell itself and stores the hash; it never accepts the original retyped. It refuses a target language `lang_jur_map` does not hold, using the function `log-search` uses (`grep -n 'not a language lang_jur_map holds' scripts/db.py`), and a target equal to the source's recorded language where the pointed row leads to one. `record-translation` (a request id, or a pointer to create and fill in one call; `--text`, `--translator-kind`, `--translator-name`): applies the fidelity rule of item 5. `review-translation` (`--verdict reviewed|rejected`, the reviewer's kind and name, a reason on rejection). No list of translatable tables is typed anywhere: any text cell of any table can be pointed at. `--stage` is validated against the stage ids of `governance/pipeline-contract.yaml`.
4. **The default stage is a rule held once, not a literal in code.** `governance/pipeline-contract.yaml` gains one top-level key, `translation:` with `default_stage: synthesis` (the owner: "we can set a rule for synthesis to translate, which isn't hardcoding necessarily"). `schemas/pipeline_contract.py` gains the matching optional field and validates that the value is one of the contract's own stage ids. The verbs read it through one function: a request made without `--due-stage` falls due at the rule's stage, computed when it is read, never stored; one read-only verb, `translations --due-at <stage>`, lists what is due there. No stage name appears in the verbs' code. The target language has no default until OD-02 is answered: `--target-language` is required.
5. **Fidelity, checked at `record-translation`.** The original is kept by construction (it is never touched). The numbers must agree: with the number reader of T-008, every number the original cell states as a numeral must be stated in the translation, and every number the translation states must be stated in the original or, where the pointed cell is the `claim_text` of a figure, be a number of that row's verified `claimed_value` (this covers a number the source writes in words). A translation that adds, drops or changes a figure is refused. A translation of a cell whose hash no longer matches is refused: request it again.
6. **What this is not.** The aliases typed `TRANSLATION` in `term_aliases` are search forms generated in other languages; they stay where they are, flagged as search aids (T-026 types their attestation), and are neither moved here nor deleted. A translation row never becomes an alias or a term: a concept is minted only from an observed phrase, as now (no back-translation). A translation of an attested non-English form is an aid to discussion that points at the alias row. `value_as_written` on a figure (T-008) is the same idea at the grain of one cell: the source's wording is kept in a cell that names it, our reading is in a cell that names it as ours, the writer checks the wording against the verified bytes, and who made the reading is recorded. Do not build a second mechanism for numbers.
7. **One check, registered in `governance/check-registry.yaml`:** `scripts/audit/translation_pointer_audit.py`. For every current translation: the pointer resolves, the hash matches the cell today, the number rule of item 5 holds. It prints `EXAMINED: <n>`. What reaches the guidebook without it: a translation shown beside a quotation it no longer translates, because SQLite cannot hold a foreign key to "any cell". Declare it as the registry declares a check over a table that is empty by decision today (read two existing floorless entries and follow them). The captured set is derived from the writers: confirm `translations` enters it with `dbcore.writable_tables`.

8. **Review rule (OD-30, resolved under delegation).** A CHECK that a `reviewed` or `rejected` row's reviewer is not its translator (`reviewed_by_name <> translator_name`); `review-translation` refuses otherwise and its help says that a translation shown to a reader is reviewed by an Opus-class instance. The database cannot verify a model's class: it records the reviewer's name, and render shows only `reviewed` rows (T-037).
9. **One home for translations.** `evidence_sources` carries earlier, unused title-translation columns (`pub_title_en`, `pub_subtitle_en`, `chapter_title_en`, `journal_name_en`, `translation_method`, `translation_reviewed`; `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select translation_method, translation_reviewed, count(*), sum(pub_title_en is not null) from evidence_sources group by 1,2').fetchall())"`). After this task no writer writes them: a title's translation is a `translations` row pointing at the title cell. Sweep their writers and readers and retire them in order — writer, then reader, then NULL forward (CLAUDE.md rule 5); never drop a column a committed data migration INSERTs (`git grep -l -e pub_title_en -e translation_reviewed -- scripts/migrations` first).

**What reads what this task adds or changes:** `v_translations_current`: the synthesis discussion (T-032), the candidate finder (T-033), render (T-037), and a session comparing forms across languages (T-026, T-107). `translations --due-at`: `/run-pipeline` at each stage. The contract key: the verbs, and `pipeline_contract_audit`.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `pipeline-contract.yaml`, `lang_jur_map`, `writable_tables`, `TRANSLATION`, `stages:`, `pub_title_en`, `translation_method`, `translation_reviewed`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) and report its result. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `pipeline-contract.yaml`: code and skills: `schemas/pipeline_contract.py`, `scripts/audit/adversarial_pass_audit.py`, `scripts/audit/claude_md_spine.py`, `scripts/audit/graph/extract_contract.py`, `scripts/audit/pipeline_contract_audit.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/db.py`, `scripts/dbcore.py`, `scripts/generate/owner_browser_build.py`, `scripts/run_checks.py`, `scripts/tests/test_pipeline_contract.py`, `skills/run-pipeline_SKILL.md`. Prose: `CLAUDE.md`, `architecture/meta-scripts-spec.md`, `governance/check-registry.yaml`, `governance/stage-map.yaml`.
- `lang_jur_map`: code and skills: `schemas/enums.py`, `scripts/audit/alias_provenance_audit.py`, `scripts/audit/graph/known_debt.yaml`, `scripts/audit/graph/topology.py`, `scripts/audit/jurisdiction_db_vocabulary.py`, `scripts/db.py`, `scripts/dbcore.py`, `scripts/tests/test_run_pipeline_refusals.py`, `skills/run-pipeline_SKILL.md`. Prose: `governance/context-map.yaml`, `governance/functional-taxonomy.md`, `governance/held-tensions.md`, `governance/owner-browser.yaml`, `governance/stage-map.yaml`.
- `writable_tables`: code and skills: `scripts/db.py`, `scripts/dbcore.py`, `scripts/research/emit_batch_sql.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_scan_contract.py`. Prose: `CLAUDE.md`.
- `TRANSLATION`: code and skills: `scripts/audit/research_batch_dod.py`, `scripts/db.py`, `scripts/research/page_image.py`, `scripts/tests/test_scan_contract.py`. Prose: `architecture/sqlite-data-layer.md`, `references/audits/migration-review-2026-05-11.csv`, `references/bpc/health-and-symptom-management/thermoregulation-built-environment.md`.
- `stages:`: code and skills: `schemas/pipeline_contract.py`, `scripts/audit/claude_md_spine.py`, `scripts/audit/pipeline_contract_audit.py`. Prose: `CLAUDE.md`, `governance/conceptual-model.md`, `governance/pipeline-contract.yaml`, `references/bpc/ALL-FW.md`, `references/bpc/wayfinding-and-signage/wayfinding-cognitive-science-spatial-design.md`.

**Callers already known** (found by this file's author or by a pilot; each is in scope):
- `schemas/pipeline_contract.py` forbids unknown keys, so the contract key and the model field land together; `scripts/audit/pipeline_contract_audit.py` and `scripts/tests/test_pipeline_contract.py` load the contract and must pass before and after.
- `governance/context-map.yaml` is generated from the tree: a new table and script change it; regenerate with `python3 scripts/generate/context_map.py` if `context_map_fresh` says so.
- `governance/stage-map.yaml` assigns tables to stages: `translations` is a cross-stage table (it points into every stage). Add it as the file treats the gap register, and say so in the pull request; if the file has no such category, stop.
- `skills/run-pipeline_SKILL.md`: one sentence at the synthesis step (translations due there are listed by `db.py translations --due-at synthesis`) and one where a stage meets text it cannot read (request a translation; never paraphrase into a source column).

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `pipeline_contract_audit`, `test_pipeline_contract`, `test_run_pipeline_refusals`, `test_db_amend_writers`, `context_map_fresh`, `graph_audit`, `derived_not_curated_audit`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="pipeline_contract_audit test_pipeline_contract test_run_pipeline_refusals test_db_amend_writers context_map_fresh graph_audit derived_not_curated_audit test_scan_contract test_author_presence test_search_log_completeness test_assess_cell_pilot migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** A new test file under `scripts/tests/`, registered in the `tests` battery, working on its own scratch copy and deriving every probe. **AT-107** (put the string `AT-107` in the docstring): choose by query a figure whose source is recorded in a language other than English; from the stage `judgment`, request and record a translation of its `claim_text` into a language `lang_jur_map` holds, by the verbs alone. Assert: the original cell is byte-identical before and after; the row in `v_translations_current` joins back to that cell by its pointer; `requested_at_stage` is `judgment`; `git status --porcelain scripts schemas` is empty. **AT-108** (`AT-108` in the docstring): with the contract as committed, a request with no `--due-stage` is listed by `translations --due-at synthesis`; load a temporary copy of the contract in which `default_stage` is another stage id (through the loader's path argument: `grep -n 'def load' schemas/pipeline_contract.py`) and the same request is listed at that stage and not at synthesis, with no file under `scripts/` or `schemas/` changed. Assert also that no stage id is written as a literal in the three verbs: `git grep -n -w -e synthesis -- scripts/db.py` shows no line inside them. **AT-109** (`AT-109` in the docstring): a translation whose text changes a figure of the original is refused; one that drops a figure is refused; one that keeps every figure is accepted; a translation of a quote that spells its number in words, stating the numeral of the row's `claimed_value`, is accepted. Also: a pointer to a table, column or row that does not exist is refused; a retyped original is impossible (the verb takes no such argument); recording against a cell changed since the request is refused; `review-translation` requires the reviewer. Before: the file cannot run (no table, no verb). After: green, and `translation_pointer_audit` passes with `EXAMINED:` equal to the rows the test left on its copy when pointed at it.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T049-01`, `T049-02`, …) and confirm the prefix is free first (`grep -c '"T049-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: add a typed home for translations attached by pointer, with the default stage held as one rule [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- the delegation gate of section 2 prints CLOSED for a decision this task rests on (the owner has reversed it, a correction has withdrawn it, or its independent check is not recorded); a delegated resolution is never the owner's words;
- The contract model cannot take a new top-level key without changing how existing keys validate.
- A translation would have to be written into a column that holds a source's wording: never; stop.
- You find yourself choosing a target language or a reviewer class: that is OD-02 and OD-30.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
