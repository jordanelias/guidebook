# T-026  A form says how it is attested, and a search says which forms it used

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-026-report.md`, patch `.../T-026.patch`; defects folded. Expect to find a defect in this file all the same, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-026 |
| Title | A form says how it is attested, and a search says which forms it used |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-22 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** none; but the one-page forms-home design `T-028-design.md` (written first under T-028 item 2, and committed beside the task files on 2026-11-12) must exist, because it names the one table that holds a form, and this task's attestation columns go on that table and nowhere else (the delegated resolution of OD-03 allows one forms home; the design names `term_aliases`, which already holds every form today: `PRAGMA table_info(term_aliases)`). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** AT-24 red, for the vocabulary query `_near_terms` and for the search join (section 6 step 2). AT-24's other half, the exact-name screen `_name_holder`, is T-028's (its case T028-05). AT-23 (the base coverage view) is not this task's: it is turned by T-057 (`workplan/2026-11-12-bidirectional-pipeline/tasks/T-057-base-coverage-view.md`, section 2); the improvement programme lists it against IMP-22, but nothing in this task builds it. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-026-alias-attestation "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-026" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

Nothing typed separates a term found in a national instrument from one a model generated. A search run on an invented word returns nothing, and that is recorded as an absent literature.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*), sum(observation_id is not null), sum(alias_type='TRANSLATION') from term_aliases\").fetchall());print('attestation' in [r[1] for r in c.execute('pragma table_info(term_aliases)')], [r[0] for r in c.execute(\"select name from sqlite_master where name='search_execution_forms'\")])"
```

**Expected output today:** first line, three numbers (aliases; aliases that point at an observation; `TRANSLATION` aliases): the third is not 0 and the second is far below the first (no alias, or almost none, points at an observation); second line exactly `False []` (no `attestation` column, no junction). The second line is the test of moved ground: if it prints anything else, part of this task is already done; stop.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

Every object below is named; section 8's "do not add what section 4 does not name" applies to anything else. Each "Chosen (pilot 2026-11-13)" closes a gap the pilot met; do not reopen it.

1. **Schema migration, one file**, on the table `T-028-design.md` names as the one forms home: **`term_aliases`** (design section 2; no new forms table). **Do not change the table's key:** the occurrence grain is T-028's rebuild.
   - **Header.** Name T-026, the design, OD-03. Carry the line `-- AFTER_DATA: <ts>`, with `<ts>` the output of `ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`. Why: `migrate_db.py --rebuild` runs schema migrations before the data migrations that follow the last marker (`grep -n 'def build_plan' -A30 scripts/migrate_db.py`), and data migrations write `term_aliases` (`grep -l term_aliases scripts/migrations/data_*.sql`); without the marker the rebuild fills `attestation` before those rows exist and `migration_reproducibility.py --deep` diverges. No comment in the migration carries a hand-typed count either (CLAUDE.md rule 7a).
   - **Columns, by `ALTER TABLE ... ADD COLUMN`**, exactly as the design's sections 3 and 4 name them: `attestation TEXT NOT NULL DEFAULT 'unrecorded' CHECK (attestation IN ('instrument','other_source','owner_supplied','model_seed','unrecorded'))` (the sixth statement's four kinds, `grep -n -F 'its attestation (instrument phrase with locator' references/project-standards.md`, plus `unrecorded`); then `source_url`, `source_page`, `source_line`, `source_clause` with the column CHECKs of the design's section 3. **The `DEFAULT` is required:** SQLite refuses `Cannot add a NOT NULL column with default value NULL` (measured). Its consequence: every writer that omits the column (`rename_term`'s insert of the former label, the selftest INSERT in `research_batch_dod.py`, the AL07 fixture in `test_scan_contract.py`) now writes `unrecorded`, which is true for each; leave them. **The two cross-column CHECKs of the design's section 3 go in DDL, on the last column added (`source_clause`)**: `ADD COLUMN` carries a CHECK that names other columns (measured: the violating insert gave `CHECK constraint failed`), so the writer is not the only guard.
   - **Fill, one UPDATE in the same migration**, from what each row already says, in `classify()`'s precedence, with `INSTR`, not `LIKE` (`LIKE` is case-insensitive; `classify()` is a case-sensitive `in`):
     ```
     UPDATE term_aliases SET attestation = CASE
         WHEN INSTR(COALESCE(notes,''), 'VERIFIED-GLOSSARY') > 0 THEN 'unrecorded'
         WHEN INSTR(COALESCE(notes,''), 'VERIFIED-CROSS')    > 0 THEN 'unrecorded'
         WHEN INSTR(COALESCE(notes,''), 'VERIFIED-NATIVE')   > 0 THEN 'unrecorded'
         WHEN observation_id IS NOT NULL                          THEN 'other_source'
         WHEN INSTR(COALESCE(notes,''), 'model-generated')   > 0 THEN 'model_seed'
         ELSE 'unrecorded' END;
     ```
     Never `instrument` by inference. The `VERIFIED-*` rows go to `unrecorded`, not `other_source`, because they carry no observation and no locator and the first cross-column CHECK would refuse them; this is the design's own conditional (section 4), and it is live: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from term_aliases where instr(notes,'VERIFIED-GLOSSARY')>0 or instr(notes,'VERIFIED-CROSS')>0\").fetchone())"` was not 0 on 2026-11-13. **List them in the pull request body for T-107** with `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);[print(r) for r in c.execute(\"select term_id, alias, language, notes from term_aliases where instr(notes,'VERIFIED-GLOSSARY')>0 or instr(notes,'VERIFIED-CROSS')>0 order by 1,2\")]"` (run on the canonical database, before the migration). The fill is an UPDATE: `migration_reproducibility` (row counts) cannot see it; only `--deep` can, which is why section 4's proof runs `--deep`.
   - **The junction: `search_execution_forms`.** Chosen (pilot 2026-11-13, corrected on review): it points at a form by the table's **present key**, with a real foreign key, not by `rowid`:
     ```
     CREATE TABLE search_execution_forms (
         exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
         term_id            TEXT NOT NULL,
         alias              TEXT NOT NULL,
         language           TEXT NOT NULL,
         created_at         TEXT NOT NULL,
         created_by_session TEXT NOT NULL,
         PRIMARY KEY (exec_id, term_id, alias, language),
         FOREIGN KEY (term_id, alias, language) REFERENCES term_aliases(term_id, alias, language)
     );
     ```
     Why not `rowid`, as the design's section 4 says: (i) SQLite cannot declare a foreign key on a rowid (measured: `foreign key mismatch`), so nothing but the writer would check the pointer; (ii) `term_aliases` has no `INTEGER PRIMARY KEY`, so its rowids are implicit, and the capture path does not carry them: `emit_batch_sql.py` diffs a table by its declared key and emits new rows in key order without a rowid (`grep -n 'implicit rowids' scripts/research/emit_batch_sql.py`), so two forms added in one batch can land in the canonical database with rowids other than the scratch copy's, and a junction row captured from the scratch copy would then point at the wrong form. (`migrate_db.py --rebuild` itself reproduced every rowid on 2026-11-13, measured by comparing `select rowid, term_id, alias, language from term_aliases` between the canonical and a rebuilt copy; the defect is the capture, not the rebuild.) The key is a pointer, not a copy (CLAUDE.md rule 5); it is the table's own primary key until T-028. **What T-028 does with it** (stated here so T-028 does not have to work it out): in the same migration that rebuilds `term_aliases`, T-028 rebuilds this junction to `(exec_id, form_id INTEGER NOT NULL REFERENCES term_aliases(form_id), created_at, created_by_session, PRIMARY KEY (exec_id, form_id))`, filled by `SELECT j.exec_id, a.rowid, j.created_at, j.created_by_session FROM search_execution_forms j JOIN term_aliases a USING (term_id, alias, language)` before the old `term_aliases` is dropped (one form per key until then, so the join is exact; the row count must not change). It must, because the key stops being unique at the occurrence grain and the foreign key would then answer `foreign key mismatch`. The writer's flag (`--form-id`, below) does not change.
2. **`add-alias`, three routes, exactly one per call** (`db.py add-alias --term-id T --alias-type X --session S` plus one of):
   - **Observation route** (today's): `--observation-id N`. Unchanged, except that it writes `attestation`: `other_source` by default (the fill rule: an admitted source used the phrase; whether it is an instrument is a judgment), or `instrument` when `--attestation instrument` is given. Never inferred.
   - **Base route** (seventh statement): `--alias "<text>" --language XX --jurisdiction YY --source-url URL (--source-page P | --source-clause C) [--source-line N] --attestation instrument|other_source`. Chosen (pilot 2026-11-13): the observation route reads the phrase, language and jurisdiction from the observation; the base route has none, so it names them, and `--language` is stored in `term_aliases`' own letter case (`_alias_language`). Refuses: a (language, jurisdiction) pair `lang_jur_map` does not hold, compared case-insensitively (the same refusal the design gives `add-term --first-form`, so the two base routes agree); no `--source-url`, or neither `--source-page` nor `--source-clause`; an `--attestation` outside `instrument|other_source`. The warrant is the locator (it names where the form is used) and the judge is `created_by_session`; no rationale column is added (see the design defect reported for T-028-design.md; do not put a rationale in `notes`).
   - **Seed route**: `--alias "<text>" --language XX [--jurisdiction YY] --seed owner_supplied|model_seed`. No locator: refuses `--source-*` and `--attestation` with `--seed`, and refuses `--seed instrument|other_source` (an attestation needs a locator). The language must be one `lang_jur_map` holds; a given jurisdiction must pair with it there.
   - **Promotion and no downgrade.** The key is still `(term_id, alias, language)`. A held row whose `attestation` is `model_seed`, `owner_supplied` or `unrecorded` is **promoted in place** by the observation or the base route (its `attestation` and pointer or locator are set; `jurisdiction` is set where it was NULL, and a held jurisdiction that differs from the one given is refused); no second row. A held row whose `attestation` is already `instrument` or `other_source` is **refused** by every route, the refusal saying that a second occurrence waits for T-028's occurrence grain (this keeps an `instrument` row from being re-attested as `other_source`). The seed route refuses any held row. Existing refusal texts stay: AL05 matches `already holds` and AL08 matches `attested by observation`.
   - New parameters of `add_alias` are keyword parameters with defaults: the tests call it positionally as `add_alias(term, observation, alias_type, session)`.
3. **`log-search`.** Gains `--form-id N` (repeatable): the `rowid` of a `term_aliases` row as read now (`form_id` after T-028, same flag). The writer looks the row up, refuses one that does not exist, and writes one `search_execution_forms` row per distinct form with that row's key. `--terms-used` is **refused for new rows**, the refusal naming `--form-id`; the column is kept and no existing row is converted. Chosen (pilot 2026-11-13): the JSON is not forms but term ids and free words (`python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select terms_used from search_executions where terms_used is not null limit 5').fetchall())"`; the research-log-manager skill tells operators to put words in it), so no word maps mechanically to a form; the query's words stay in `query_text`. This retires the writer of a column a committed migration fills (CLAUDE.md rule 5: writer-retire first; the column is not dropped).
4. **`_near_terms` reads `attestation`.** It compares labels (`terms.canonical_en`, as today) and the EN aliases whose `attestation IN ('instrument','other_source')` only. It never read `notes`; "read the column, not the note" means here "compare attested forms, not every alias". Per-language screening is T-028's. **This narrowing is licensed, and is not a weakened refusal under section 8:** E4 (`grep -n '^| E4 ' references/project-standards.md`) rules that model-generated and unrecorded aliases are "never vocabulary", and the design's section 8 says the screens read attested forms only. The refusal's text and its comparison of labels stay; what it stops comparing is search aids. E4's own words make a seed vocabulary only "when an instrument in its language is read"; the design counts `other_source` as attested too. That reading is the owner's, not yours: follow the design (it is no looser than today, when every alias is compared) and say in the pull request that the question is open. Until T-107 attests forms, the near-match refusal of `add-term` compares labels only (no row is attested after the fill); say so in the pull request.
5. **`alias_provenance_audit` reads `attestation` first.** Chosen (pilot 2026-11-13): `classify()` maps `instrument` and `other_source` to `SOURCE-ATTESTED`, `model_seed` to `MODEL-GENERATED`, `owner_supplied` to a new class `OWNER-SUPPLIED`; for `unrecorded` only, it falls back to today's notes markers (`VERIFIED-*`, `curated`, `repo shorthand`), so their report classes survive. The FAIL rule is unchanged: an `unrecorded` row with no marker created on or after `CUTOFF_SESSION_DATE` fails. Why: the fill maps the curated, repo-shorthand and `VERIFIED-*` rows to `unrecorded`, and they were created after the cutoff, so a column-only audit would turn a green audit red (count them: `python3 -I -c "import sqlite3,sys;sys.path.insert(0,'scripts/audit');import alias_provenance_audit as a,collections;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(collections.Counter(a.classify(n,o) for n,o,s in c.execute('select notes,observation_id,created_by_session from term_aliases') if a.session_date(s)>=a.CUTOFF_SESSION_DATE))"`). The fallback retires when T-107 re-attests those rows.
6. **Callers to edit** (found by the sweep of section 5; listed here so they are named): `skills/research-log-manager_SKILL.md` (its `log-search` example passes `--terms-used`; it becomes `--form-id`), `skills/run-pipeline_SKILL.md` (the `add-alias` sentence names the routes), `scripts/tests/test_scan_contract.py` (the AL07 fixture states `model_seed`; the new cases of section 6), and, for the new table, `governance/stage-map.yaml` and `governance/owner-browser.yaml` (where its sibling `search_admissions` is named) and the regenerated `governance/context-map.yaml`; and the R11 check of `scripts/audit/research_batch_dod.py` (found on review, missed by the pilot: `grep -n "R11 vocabulary provenance" -A8 scripts/audit/research_batch_dod.py`), which fails every alias a batch wrote with an empty `notes`. The base and seed routes write their provenance in typed columns, not in `notes` (the 2026-11-06 schema-shape statement), so R11 would fail every row they write; its predicate becomes "empty `notes` **and** `attestation = 'unrecorded'`". That is not a weakened refusal: a row with a typed attestation states its provenance in the cell that names it. Do not make the writers put a marker in `notes` to satisfy R11. Edit code only in `scripts/db.py`, `scripts/audit/alias_provenance_audit.py`, `scripts/audit/research_batch_dod.py` (R11 only) and the test file.

**What reads what this task adds or changes:** `add-alias`, `log-search`, `add-term` (through `_near_terms`), `alias_provenance_audit`, the `research-log-manager` and `run-pipeline` skills; later T-028 (its rebuild reads the columns and remaps the junction), T-107 (it re-attests the listed rows) and T-057 (its coverage view reads `attestation` and the junction). `multilingual-research` reaches `log-search` only through `research-log-manager` (`git grep -n -i -e alias -e terms -- skills/multilingual-research_SKILL.md` finds nothing this task changes).

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `term_aliases`, `terms_used`, `terms-used`, `alias_provenance`, `_near_terms`, `add-alias`, `log-search`

`terms-used` is the CLI spelling of `terms_used`; the underscore needle does not find it (the pilot's sweep missed `skills/research-log-manager_SKILL.md` for that reason). `add-alias` and `log-search` find every sentence that states the verbs' behaviour; most are mentions (a `log-search` sentence about priors or admissions stays true), and only a sentence about the terms a search used or the routes of `add-alias` is a caller.

**A new table has no name to sweep for.** Find where `search_execution_forms` must be registered by sweeping its sibling: `git grep -l -F search_admissions -- governance architecture skills .claude scripts ':(exclude)scripts/migrations'`. On 2026-11-13 the files that register a table (as distinct from code that reads `search_admissions`) were `governance/stage-map.yaml` (its stage), `governance/owner-browser.yaml` (its description) and `governance/context-map.yaml` (generated; regenerate it, never hand-edit). `dbcore.writable_tables` derives the capture set, so no list in code needs it.

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

- `term_aliases`: code and skills: `scripts/audit/alias_provenance_audit.py`, `scripts/audit/graph/extract_db.py`, `scripts/audit/jurisdiction_db_vocabulary.py`, `scripts/audit/research_batch_dod.py`, `scripts/db.py`, `scripts/tests/test_scan_contract.py`, `skills/run-pipeline_SKILL.md`. Prose: `architecture/sqlite-data-layer.md`, `governance/check-registry.yaml`, `governance/context-map.yaml`, `governance/functional-taxonomy.md`, `governance/held-tensions.md`, `governance/owner-browser.yaml`, `governance/stage-map.yaml`, `references/audits/cell-conflation-audit-2026-05-11.md`, `references/owner-notes/2026-08-27-architecture-note.md`.
- `terms_used`: code and skills: `scripts/db.py`. Prose: none.
- `terms-used` (added 2026-11-13): code and skills: `scripts/db.py`, `skills/research-log-manager_SKILL.md` (line 74 on 2026-11-13: the `log-search` example passes `--terms-used '["alias1","MeSH term","alias2"]'`; a caller, edited to `--form-id`).
- `alias_provenance`: code and skills: `scripts/audit/alias_provenance_audit.py`, `scripts/audit/research_batch_dod.py`, `scripts/db.py`, `scripts/tests/test_scan_contract.py`. Prose: `governance/check-registry.yaml`, `governance/context-map.yaml`, `governance/owner-browser.yaml`.
- `_near_terms`: `scripts/db.py` only (its one caller is `insert_term`).
- `add-alias`, `log-search`: run the commands; the pilot judged `skills/run-pipeline_SKILL.md` (the `add-alias` sentence) a caller, and `research_batch_dod.py` line 1342 (a selftest INSERT without `attestation`) a mention that still works because of the column's `DEFAULT`. The same file's R11 (`grep -n "R11 vocabulary provenance" scripts/audit/research_batch_dod.py`, a `notes`-is-empty count) is a caller the pilot missed; section 4 item 6 says how it changes. `scripts/audit/graph/extract_db.py` and `scripts/audit/jurisdiction_db_vocabulary.py` read `term_aliases` and are mentions. `check-registry.yaml` quotes the alias count as a hand-typed "today" figure; it stays true (no row is added) and is not this task's to fix.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `alias_provenance_audit`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`, `research_dod` (its R11 changes; the pilot found it red on the base for R12, which is not yours). Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness alias_provenance_audit migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit research_dod"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** AT-24 (its source text: "No alias marked as model-generated or unattested is used as vocabulary by any writer or view; each is usable only by a search that is flagged"), as far as this task turns it: (a) `_near_terms` returns no alias whose `attestation` is not `instrument` or `other_source`; (b) a search that fired such an alias is found by this join, which is the flag (derived, not stored): `select distinct f.exec_id from search_execution_forms f join term_aliases a using (term_id, alias, language) where a.attestation not in ('instrument','other_source')`. The `_name_holder` half is T-028's (T028-05).

**Where the cases go:** `scripts/tests/test_scan_contract.py` (it already holds the `add-alias` cases and builds a scratch copy); no existing test exercises `log-search`'s write path, so its cases go there too. Cases, at least (prefix `T026-`):

| Case | What | Red on the unchanged code because |
|---|---|---|
| T026-01 (AT-24 a) | **The seed is made by SQL on the test's scratch copy, never by the new writer**: if it were made by `add-alias --seed`, the unchanged code would write nothing and `_near_terms` would return `[]`, so the case would pass on the old code (the pilot's first version did exactly this). Recipe: choose two fixture words and show by query that `_name_tokens` of no label and no alias contains either (e.g. `taskfixturea`, `taskfixtureb`); choose a term by query; `INSERT` into `term_aliases` the two-word alias in EN for it with `alias_type 'SYNONYM'`, notes `model-generated TASK-FIXTURE`, a post-cutoff `created_by_session`, and `attestation = 'model_seed'` only if `PRAGMA table_info(term_aliases)` lists the column; then call `_near_terms(conn, "taskfixturea taskfixtureb taskfixturec")` (a superset: a two-token held name inside the new one is near). Assert the term is not returned. | the old `_near_terms` compares every EN alias and returns the term |
| T026-02 | positive control on the same copy: the same SQL insert with other fixture words and `attestation = 'instrument'`, `jurisdiction`, `source_url`, `source_clause` set; `_near_terms` **does** return that term. And a label still screens: a near match of an existing `canonical_en` (chosen by query) is still returned | (runs after the migration only; it proves the screen was narrowed, not switched off) |
| T026-03 (AT-24 b) | on a scratch copy, `log-search ... --form-id <the seed's rowid>`; the join of step 2 (b) returns that `exec_id` | `unrecognized arguments: --form-id` |
| T026-04 | `log-search --terms-used '[...]'` is refused, naming `--form-id`; `--form-id` naming no row is refused; nothing is written by either | the old writer accepts `--terms-used` |
| T026-05 | base route writes one row with the given locator and `attestation`; promotion of a SQL-made seed in place by the base route (one row, attestation set); a held `instrument` row is refused by the observation route (no downgrade) | `unrecognized arguments: --alias` (and the others) |
| T026-06 | the refusals of section 4 item 2: no locator; a pair `lang_jur_map` lacks (choose by query a language and a jurisdiction that never pair there); `--seed` with `--source-url`; `--seed instrument` | as T026-05 |
| T026-07 | `alias_provenance_audit` on a migrated scratch copy (`GUIDEBOOK_DB_PATH`), after an SQL insert of a post-cutoff row with `attestation = 'owner_supplied'` and NULL notes: exit 0, the row counted `OWNER-SUPPLIED` | the old `classify()` reads only `notes`, calls the row UNKNOWN and exits 1 |
| T026-08 | the same with `attestation = 'unrecorded'` and NULL notes: still exit 1 (the refusal is not weakened) | (green before and after; it guards the fallback) |
| T026-09 | `research_batch_dod.py` R11 scoped to a fixture session: a base-route row with empty `notes` passes; an `unrecorded` row with empty `notes` still fails | the old R11 fails the base-route row |

Show each red row red on the unchanged code (or, for a case that needs the migration, on the unchanged code over the migrated copy), and all green after.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T026-01`, `T026-02`, …) and confirm the prefix is free first (`grep -c '"T026-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: type alias attestation and the forms a search used [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass. Two changes of section 4 look like weakening and are not, for the reasons given there: `_near_terms` no longer compares seeds (item 4, licensed by E4), and R11 of `research_batch_dod.py` accepts a typed attestation in place of a note (item 6). Nothing else is narrowed.
- Do not point anything at `term_aliases` by `rowid` in a stored row: the capture path does not carry implicit rowids (section 4 item 1). `--form-id` takes a rowid as input only; what is stored is the key.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- `T-028-design.md` at execution names a different junction, a rationale column for the base route, or an owner ruling that an `other_source` form is not vocabulary (all three were reported against the design on 2026-11-13; see section 4 items 1, 2 and 4): follow the design as it then stands if it says exactly what to build, otherwise stop;
- the migration fails on a scratch copy (for example, a cross-column CHECK refuses a filled row), or `migration_reproducibility.py --deep` does not pass after it (check the `AFTER_DATA` line first).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
