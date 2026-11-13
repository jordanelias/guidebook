# T-028  A concept that is not an English string

> **NOT FOR SONNET** — the design is committed beside this file as `T-028-design.md` (2026-11-12): the one forms home is `term_aliases`, rebuilt to one row per occurrence; `canonical_en` stays as our label; `v_term_names` derives the label basis and the name shown. The delegated resolution of OD-03 keeps this task's NOT FOR SONNET status, because the change rewrites the semantics of every name screen: an Opus-class session executes the design exactly; where this file and the design differ, the design governs. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-028-report.md`, patch `.../T-028.patch` (stacked on the T-026 pilot); defects folded. Expect to find a defect in this file all the same, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-028 |
| Title | A concept that is not an English string |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | IMP-21 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-026 merged. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "governance: type alias attestation and the forms a search used"` (T-026's commit subject, its section 7). Then check that T-026's junction is in the form its folded file describes (section 4 item 1 there: keyed by `(term_id, alias, language)` with a real foreign key, no `form_id` column), because this task's migration remaps it by that key: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([tuple(r[2:5]) for r in c.execute('pragma foreign_key_list(search_execution_forms)')], [r[1] for r in c.execute('pragma table_info(search_execution_forms)')])"` must list `('term_aliases', 'term_id', 'term_id')`, `('term_aliases', 'alias', 'alias')`, `('term_aliases', 'language', 'language')` and a column list without `form_id`. Anything else (no table; a `form_id` column pointing at a `rowid`, which is the shape of the unfolded T-026 pilot patch) is a stop (section 9). In a stacked run (T-026 committed on your branch, not yet merged), run the same checks against `HEAD` and on your clone's migrated database.
- **Owner decisions:** OD-38 — **answered by the owner, 2026-11-12 (fifth set):** "First recorded, until a named judge picks; the pick is recorded with its reason" (`grep -n -F "OD-38: the first English name recorded is shown" references/project-standards.md`). It settles the design's tie-break (section 7, rule 2): where several English-language instruments name one concept differently, the first recorded is shown until a named judge picks one with `rename-term --from-form`, and the pick is recorded with its reason. Check: `grep -F "OD-38 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`; any other value is a stop. The other decisions this task needed are resolved under delegation (next bullet).
- **Delegated resolutions this task rests on.** OD-03: forms table; `canonical_en` kept as our English descriptive label, never a form; the name shown derived by E1. Each is a resolution by an Opus-class model under the owner's delegation of 2026-11-12: not the owner's words, reversible by the owner, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-03 OD-38; do gate $n; done
```
- **Tests that must be red (or green) before you start:** AT-25 red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-028-concept-identity "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-028" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

A concept first met in another language is named by an English gloss and searched for by it.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from terms where canonical_en glob '*[^ -~]*'\").fetchall())"
```

**Expected output today:** 0: no term has a non-ASCII name.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

Every object below is named; section 8's "do not add what section 4 does not name" applies to anything else. Each "Chosen (pilot 2026-11-13)" closes a gap the pilot met; do not reopen it.

1. Build `tasks/T-028-design.md` (committed 2026-11-12, revised 2026-11-13), to the delegated resolution of OD-03 (`workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md`, section OD-03): a concept's identity is `terms.term_id`; its names are rows of **one** forms table, **`term_aliases`** (no `term_forms` table is built: the design's section 2 says why), rebuilt by one schema migration to one row per occurrence keyed by `form_id`, with a unique occurrence index in place of the primary key and a nullable `usage_type` (design sections 3 and 10; the migration carries an `AFTER_DATA` marker, derived as the design's section 10 says even when it equals the marker T-026's migration already carries: harmless then, needed if a data migration lands between the two). `form_id` is assigned inside the migration from each row's `rowid` (the rebuild reproduces it: `migration_reproducibility.py --deep` is the proof); **no stored pointer reaches `term_aliases` by `rowid`**, before or after (`emit_batch_sql.py` does not carry implicit rowids: `grep -n 'implicit rowids' scripts/research/emit_batch_sql.py`). T-026's attestation and locator columns are on the same table (design section 4). `canonical_en` stays `NOT NULL` as our English descriptive label, never a form and never matched first (section 6). The label basis and the name shown are derived by one view, `v_term_names` (section 7): add no label-kind column and no display pointer; the stored, warranted choice is the label itself, set by `rename-term`.
   - **The junction.** Chosen (pilot 2026-11-13, corrected on review): in the same migration, and before the old `term_aliases` is dropped, `search_execution_forms` is rebuilt from T-026's key to `form_id`, **remapped by key**, as T-026's folded section 4 item 1 states: `(exec_id INTEGER NOT NULL REFERENCES search_executions(exec_id), form_id INTEGER NOT NULL REFERENCES term_aliases(form_id), created_at TEXT NOT NULL, created_by_session TEXT NOT NULL, PRIMARY KEY (exec_id, form_id))`, filled by `SELECT j.exec_id, a.form_id, j.created_at, j.created_by_session FROM search_execution_forms j JOIN _NNN_term_aliases a USING (term_id, alias, language)` (one row per key until this migration, so the join is exact; the junction's row count must not change). It must: at the occurrence grain the old key is no longer unique, and a foreign key on it answers `foreign key mismatch`. The probe of the schema-migration paragraph below lists the junction; it is a real caller, not a match on a comment. Prove the remap on a non-empty junction: on `$SCRATCH/t.db` before the migration, write one `TASK-FIXTURE` row with `log-search --form-id` (T-026's verb), apply the migration to that copy, and show the row's `form_id` reaches the same `(term_id, alias, language)`; a remap shown on an empty junction is unproven (CLAUDE.md rule 4).
   - **`attestation`'s DEFAULT.** Chosen (2026-11-13): the rebuilt column keeps T-026's `DEFAULT 'unrecorded'` (copy the definition from `sqlite_master`, design section 10 step 2). A writer that omits the column (`research_batch_dod.py`'s selftest INSERT, test fixtures) then records `unrecorded`, which is true of a row whose writer states no provenance; changing each of them would add code for no truer row.
   - **No `VACUUM`.** The rebuild leaves free pages and the database file grows; leave it. `VACUUM` may renumber the implicit rowids of every table without an `INTEGER PRIMARY KEY`.
2. Change every writer that screens or matches a name as the design's section 8 table says (as revised 2026-11-13), with these choices:
   - **The screens.** `_name_holder(conn, name, language, *, exclude_term)` returns every clash, none first: another term's label (compared only when `language` is EN) and another term's **attested** form (`attestation IN ('instrument','other_source')`) **in any language**, as today's screen compares aliases in any language; seeds (`model_seed`, `owner_supplied`, `unrecorded`) never clash and are returned as `seed_matches` (E4). `_near_terms(conn, name, language)` compares attested forms in `language`, and labels only when `language` is EN. Both keep comparing attested `NARROWER` and `BROADER` strings, as T-026's `_near_terms` does: they are not names of the concept (design section 5), but a new name equal or near to one is still worth the refusal, and dropping them is a narrowing no ruling licenses. Two narrowings are licensed and are not a weakened refusal under section 8: a seed is never vocabulary (E4: `grep -n '^| E4 ' references/project-standards.md`, already applied by T-026 to `_near_terms`); and a non-English name is neither matched against English labels nor near-matched against English forms (the eighth 2026-11-06 statement: `grep -n -F 'English is one column of the matrix' references/project-standards.md`; our label "is not asserted to be a form", and English is "not read first, matched first or ranked first"). **Not narrowed:** whether an identical string attested in one language for another concept clashes with a name in another language is an open owner question (section 9); until it is answered, the exact screen keeps comparing attested forms in every language.
   - **`add-term --from-observation`** writes the observation's surface form as the concept's first member row, **through the same function `add-alias`'s observation route uses** (its check that the quote contains the phrase and is in a file saved for the source, or carries `VERBATIM-EXEMPT`), so one value is written to one standard. Chosen (pilot 2026-11-13): `--attestation instrument|other_source` is optional and defaults to `other_source`, as T-026's observation route does; where that check fails, the term is still minted (as today) and its member row is written `unrecorded` with its `observation_id`, and the output says so and that `add-alias` promotes it once the quote is verified. The inside-the-phrase rule applies only when the observation's language is EN (design section 6).
   - **`add-term --first-form`**, the base route (design section 8), requires `--judge` and `--rationale` as well.
   - **`rename-term`** writes no alias row and gains `--from-form <form_id>`; under OD-38 **every** route (`--from-form`, `--from-observation`, `--ruling-quote`) requires `--judge <who picked>` and the existing `--reason`. Its screen is `_name_holder(conn, new, 'EN', exclude_term=term_id)`: the refusal of a name another term holds as an attested form is **kept** (the design's "label screen only" is withdrawn: no ruling licenses it), and only the two licensed narrowings above apply.
   - **`mint-term-from-catalogue`** screens as `rename-term` does (the design's "label screen only" withdrawn on the same ground); it writes no pick row (its warrant is the catalogue columns on `terms`).
   - **`add-alias`**: occurrences; `DOMAIN` refused, naming `--usage-type`; `--usage-type` written; duplicate occurrence refused in words, keeping the refusal texts the existing tests match (or, where the occurrence rule makes a case's premise false, the case is a caller: update it and list it). **`log-search --form-id`** takes and writes a `form_id` (the flag is unchanged; T-026's lookup by key becomes a lookup by `form_id`).
   - **One table, `term_label_picks`.** Chosen (pilot 2026-11-13, extended on review): the typed home of the judge and the reason, for every route that sets a label by judgment and has no other home for its warrant: each `rename-term` (all three routes) and `add-term --first-form` (whose `--rationale` is this row's `reason`: the base route writes no adjudication, since `term_adjudications.observation_id` is `NOT NULL`, and a judgment about the concept does not belong in a cell about one form). `add-term --from-observation` writes no pick row: its warrant is its `term_adjudications` row (rule 5). Columns: `pick_id INTEGER PRIMARY KEY`; `term_id TEXT NOT NULL REFERENCES terms(term_id)`; `former_label TEXT` (the label replaced; NULL only for a mint); exactly one warrant pointer, `form_id INTEGER REFERENCES term_aliases(form_id)` (`--from-form`, or the first form of a mint), `observation_id INTEGER REFERENCES observed_terms(observation_id)` or `ruling_quote TEXT`; `judge TEXT NOT NULL`; `reason TEXT NOT NULL`; the session and time columns `dbcore.stamp_for` fills. CHECKs: exactly one warrant pointer is set; `former_label IS NOT NULL OR form_id IS NOT NULL`. The route is derived from which pointer is set, never stored (rule 8); the new label is `terms.canonical_en`, never copied here. **`rename-term` writes no `AMENDED` trailer on `scope_note`** on any route: the former label lives once, in `former_label` (the owner's schema-shape statement of 2026-11-06, CLAUDE.md §4: a correction appended to a note is a fact in the wrong cell). Existing trailers are not rewritten. Register the table in `governance/stage-map.yaml` under `base` and describe it in `governance/owner-browser.yaml`, beside `terms`; regenerate `governance/context-map.yaml`.
   Legacy `alias_type` values are not rewritten (design section 5).
3. Repair the callers of the design's section 13 and of the sweep of section 5, and add the tests of the design's section 14 (T028-01 is AT-25).

**What reads what this task adds or changes:** Every writer that screens or matches a name; the coverage view of the base (T-057); render (the name shown, T-037); `log-search` (the junction). `term_label_picks` is read by the tests and by no other reader yet: it is the record OD-38 requires ("the pick is recorded with its reason"), and it replaces two homes of the former label (the `DEPRECATED` alias row and the `scope_note` trailer).

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**Code size.** Report in the pull request the output of the command below (run it after `git add` and before the commit, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. It measures from the point where your branch left `$BASE`, unless T-026's commit is on your branch but not in `$BASE` (a stacked run), where that point would count T-026 too; it then measures from T-026's commit, so only this task is counted:

```
T026=$(git log -1 --format=%H --fixed-strings --grep="governance: type alias attestation and the forms a search used" HEAD); FROM=$(git merge-base HEAD "$BASE")
[ -n "$T026" ] && ! git merge-base --is-ancestor "$T026" "$BASE" && FROM="$T026"
git diff --cached --shortstat "$FROM" -- scripts schemas .github skills ':!scripts/migrations'
```

## 5. Caller sweep

Names to sweep: `canonical_en`, `term_aliases`, `_name_holder`, `_near_terms`, `alias_type`, `insert_term`, `add-term`, `rename_term`, `rename-term`, `mint_term_from_catalogue`, `mint-term-from-catalogue`, `search_execution_forms`, `form-id`, `scope_note` (the design's section 13 lists the callers found by reading the code on 2026-11-12, corrected 2026-11-13)

The verb and function needles were added after the pilot: the five names alone missed callers of the changed writers, found only by chance (the pilot's defect 9). Callers the pilot found that way, re-check each: `workplan/pipeline-state-graph/machines.yaml` M03.t3, whose guard "a term can only be minted FROM an observation" the base route makes false (rewrite it); `scripts/tests/test_run_pipeline_refusals.py` T01 and T02 and the `fixture_term` helper of `scripts/tests/test_db_amend_writers.py` (they call `insert_term`; with `--attestation` optional they need no change unless the shared verification refuses their observation, and they must then be listed); `skills/run-pipeline_SKILL.md` (the `add-term` paragraph); `scripts/db.py` `log_search` and `skills/research-log-manager_SKILL.md` (the `--form-id` wording T-026 wrote: a key until now, a `form_id` after). `scope_note` finds the tests that assert the rename trailer (N07 in `scripts/tests/test_scan_contract.py`): they now assert the `term_label_picks` row and an unchanged `scope_note`. **A new table has no name to sweep for:** register `term_label_picks` where its sibling `terms` is registered (`grep -n -E '^  terms:' governance/stage-map.yaml governance/owner-browser.yaml`); without the stage-map entry `build_graph.py --check` gains a failure (`tables in the schema but not in stage-map`).

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

- `canonical_en`: code and skills: `scripts/audit/research_batch_dod.py`, `scripts/audit/scan_debt.py`, `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/validate_parameters.py`. Prose: `architecture/sqlite-data-layer.md`, `governance/owner-browser.yaml`, `governance/pipeline-contract.yaml`.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`, and the test files and audits that call or read what section 4 changes (`test_scan_contract`, `test_db_amend_writers`, `test_evidence_cell_state_2_3`, `test_run_pipeline_refusals`, `alias_provenance_audit`, `validate_parameters`, `jurisdiction_db_vocabulary`, `research_dod_selftest`, `scan_debt`). Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found. `test_evidence_cell_state_2_3` and `research_dod_selftest` print no `EXAMINED:` line (the pilot saw `ALL PASS (0 failed)` and `SELFTEST: PASS`); compare their result lines instead:

```
CHECKS="migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit test_scan_contract test_db_amend_writers test_evidence_cell_state_2_3 test_run_pipeline_refusals alias_provenance_audit validate_parameters jurisdiction_db_vocabulary research_dod_selftest scan_debt"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** AT-25: a concept can be stored whose first and only attested form is non-English, with an English label marked as descriptive and not counted as an attested English form. The cases, probes and expected red output today are `T-028-design.md` section 14 (T028-01 to T028-10). The red each case shows on the unchanged code is whatever stops it there (an unknown argument, an unexpected keyword, a refusal): the design states it loosely because which one appears depends on the order of arguments and on which new parameter the test passes first. What must hold is that the case is red before and green after, and that the red was observed.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T028-01`, `T028-02`, …) and confirm the prefix is free first (`grep -c '"T028-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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
git commit -m "governance: hold concept names as forms per the owner's answer [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass. Two narrowings of section 4 item 2 look like weakening and are not, for the rulings cited there: a seed never clashes or near-matches (E4), and a non-English name is not matched against English labels or near-matched against English forms (the eighth 2026-11-06 statement). Nothing else is narrowed: `rename-term` and `mint-term-from-catalogue` keep refusing a name another term holds as an attested form, and the exact screen keeps comparing attested forms in every language.
- Do not point anything at `term_aliases` by `rowid` in a stored row, and do not run `VACUUM` (section 4 item 1).

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
- `search_execution_forms` is not in the form T-026's folded file describes (section 2's check), or the remap of section 4 item 1 changes the junction's row count;
- a `translations` table exists (T-049) and holds a row pointing into `term_aliases` (`python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);t=c.execute(\"select 1 from sqlite_master where name='translations'\").fetchone();print(t and c.execute(\"select count(*) from translations where source_table='term_aliases'\").fetchone())"` prints neither `None` nor `(0,)`): such a pointer was made before `term_aliases` had a single-column key, and this task does not guess how it was encoded (design section 9);
- **the owner question on cross-language clashes** (open; not decided by this file or the design): does an identical string attested in one language for one concept clash with a name, label or form in another language for a different concept, or are such strings independent forms (and, if they clash, may an operator record the conflation with `--distinct-from` as for a same-language clash)? This file keeps today's reach (attested forms are compared in every language) and narrows only what E4 and the eighth statement license. Stop if any step, test or design sentence would require narrowing it further, or if the ledger records an owner answer that differs from the kept behaviour (`grep -n -i 'cross-language' references/project-standards.md`, which printed nothing on 2026-11-13): the answer governs, and the file must be corrected to it before work goes on;

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
