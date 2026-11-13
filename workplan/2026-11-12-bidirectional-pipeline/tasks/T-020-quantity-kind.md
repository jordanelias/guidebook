# T-020  A parameter states what kind of quantity it is

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-020-report.md`, patch `.../T-020.patch` (stacked on the T-010 pilot patch); defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-020 |
| Title | A parameter states what kind of quantity it is |
| Wave | 1 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-42b, IMP-30a in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-010 merged. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. The decisions this task needed are resolved under delegation (next bullet); none is still the owner's.
- **Delegated resolutions this task rests on.** OD-24: parameters are flat and coarse; a parameter states a quantity kind from a table of kinds held as rows and extended by data with a warrant; a parameter need not belong to an element. Each is a resolution by an Opus-class model under the owner's delegation of 2026-11-12: not the owner's words, reversible by the owner, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-24; do gate $n; done
```
- **Tests that must be red (or green) before you start:** AT-77 (second half) red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-020-quantity-kind "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-020" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

An element such as a grab bar can be promoted to a parameter. It then owes a reading from every source and is determined as a cell, though it measures nothing. Nothing on the parameter's row says what it measures, or on what evidence anyone judged that it measures anything, so the promotion cannot be read or contested.

**What this task closes, and what it does not** (pilot 2026-11-13). Whether a term names an element or a quantity cannot be computed from the term; it is a judgment. CLAUDE.md rule 8: where judgment is required, the script asks for it, constrained to the live vocabulary, demands the evidence, and records the answer and its warrant in named columns. After this task `add-parameter` refuses a promotion that does not name a kind from the table and an observation of a source stating a value of the quantity; the answer, its warrant and the session that judged it sit on the row. A determined operator can still promote `grab bar` as a length by pointing at an observation; the promotion is then recorded with its warrant and contestable, not prevented. Refusing an element mechanically is out of scope (section 9).

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
TERM=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select term_id from terms where canonical_en='grab bar'\").fetchone()[0])"); echo "probe term: $TERM"; GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py add-parameter --term-id "$TERM" --notes TASK-FIXTURE --session session_task-probe; echo rc=$?
```

**This command calls a verb that writes.** It is safe only because `GUIDEBOOK_DB_PATH="$SCRATCH/…"` is set inline on that call, which points the verb at the copy. Keep it on every `db.py` call you derive from this one; a call without it addresses the canonical database.

**Expected output today:** rc=0: the term named `grab bar`, an element and not a quantity, becomes a parameter.

The pilot saw `probe term: TERM-008` and a new parameter with `"canonical_en": "grab bar"`, rc=0. The term's domain (`select domain from terms where term_id='TERM-008'`; `bathroom` on 2026-11-13) is not one T-010 refuses, so the output is the same with or without T-010 merged.

**Expected output after the change.** Apply your migration to the working clone first, then take a fresh copy, because the before-run wrote a parameter into the old one: `cp data/guidebook.db "$SCRATCH/t.db"`. Then:

```
TERM=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select term_id from terms where canonical_en='grab bar'\").fetchone()[0])")
OBS=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select observation_id from observed_terms where context_quote glob '*[0-9]*' order by observation_id limit 1\").fetchone()[0])")
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py add-parameter --term-id "$TERM" --notes TASK-FIXTURE --session session_task-probe; echo "a rc=$?"
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py add-parameter --term-id "$TERM" --quantity-kind length --notes TASK-FIXTURE --session session_task-probe; echo "b rc=$?"
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py add-parameter --term-id "$TERM" --quantity-kind length --quantity-kind-observation-id "$OBS" --notes TASK-FIXTURE --session session_task-probe; echo "c rc=$?"
```

- `a rc=1`: a `REFUSING:` line naming every `kind_id` of `base_quantity_kinds` and the verb that adds one; nothing written.
- `b rc=1`: a `REFUSING:` line naming `--quantity-kind-observation-id` and what the observation must show; nothing written.
- `c rc=0`: the parameter is written with `quantity_kind` = `length` and `quantity_kind_observation_id` = `$OBS`. This is the judgment recorded with its warrant, not prevented (the paragraph above). The two refusals and the warrant on the row are the change; `c` is not a defect of this task.

If the output before the change differs from "Expected output today", the ground has moved: stop (section 9). If `a`, `b` or `c` after the change differs, your change is not done. Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. Schema migration: a base table of quantity kinds (one row per kind: its id, a definition, the ledger entry that admitted it, and the four session and time columns), seeded with exactly the kinds of the delegated resolution of OD-24 (`grep -n -F "OD-24:" references/project-standards.md`: length; gradient, with ratio, percentage and degrees as notations; force; time; luminous reflectance and its contrast (LRV); colour temperature), and on `base_parameters` the kind and its warrant (item 1a). **Not a CHECK list:** one verb adds a kind and refuses without an approval pointer (the pattern `mint-term-from-catalogue` uses), so the add-by-data test (T-047) can add one with no code edit. Add no element column: the delegated answer is that a parameter need not belong to an element; elements reach parameters by term pointers (T-029).

   **Chosen (pilot 2026-11-13): the table, verbatim.** Name `base_quantity_kinds`; columns `kind_id TEXT PRIMARY KEY CHECK (length(trim(kind_id)) > 0)`, `definition TEXT NOT NULL CHECK (length(trim(definition)) > 0)`, `approval_ref TEXT NOT NULL CHECK (length(trim(approval_ref)) > 0)`, `created_at TEXT NOT NULL`, `created_by_session TEXT NOT NULL`, `updated_at TEXT`, `updated_by_session TEXT`. Reason: the four session and time columns copy the shape of `base_parameters` (created NOT NULL, updated nullable); `approval_ref` holds the dated `## ` heading of the ledger entry that admitted the kind, the value `terms.catalogue_approval_ref` holds for a catalogue term, checked by the same lookup (`dbcore.ledger_heading_count(heading) == 1`).

   **Chosen (pilot 2026-11-13): the six seed rows, verbatim.** Every row has `approval_ref` = `Delegated resolution 2026-11-12 — OD-24 how coarse a parameter is, and its quantity kinds` (the em dash is U+2014; confirm with `python3 -c "import sys;sys.path.insert(0,'scripts');import dbcore;print(dbcore.ledger_heading_count(sys.argv[1]))" "<that heading>"`, which must print 1), `created_by_session` = `migration_NNN` with NNN your derived migration number (the convention of `118_adversarial_lens_sequence.sql`), and `created_at` = `$(date -u '+%Y-%m-%d') 00:00` read when you write the file. `updated_*` NULL.

   | kind_id | definition |
   |---|---|
   | `length` | `A distance measured along a straight line between two points of a room, a route or a fitting.` |
   | `gradient` | `The rise of a surface over its run; a ratio, a percentage and an angle in degrees are notations of this one kind, not kinds of their own.` |
   | `force` | `A push, pull or turn that a person must apply to operate or move something.` |
   | `time` | `A duration, such as how long a sound takes to decay or a door stays open.` |
   | `luminous_reflectance` | `The share of incident light a surface reflects (light reflectance value, LRV), and the contrast between two surfaces stated as the difference of their LRVs on that same scale.` |
   | `colour_temperature` | `The correlated colour temperature of a white light source, on the warm-to-cool scale.` |

   Reasons. **"Luminous reflectance and its contrast (LRV)" is one kind, not two:** OD-24's resolution lists six entries separated by semicolons and says a kind is the physical dimension of the quantity (`workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md`, section OD-24); a contrast stated as an LRV difference lies on the LRV scale. A contrast that needs another scale is a new kind added by data with a warrant, not a decision for this task. **Ratio, percentage and degrees get no rows:** OD-24 calls them notations of gradient; notations and units within a kind are T-030's. The seed covers each live parameter and nothing beyond (OD-24: "seeded from what the live parameters need"): `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select p.parameter_id,t.canonical_en from base_parameters p join terms t using(term_id)').fetchall())"` (ramp gradient, gradient; corridor width, turning circle, door width, headroom clearance, ramp run length, length; operating force, force; reverberation time, time; LRV contrast, luminous_reflectance; colour temperature, colour_temperature, on 2026-11-13). Assigning those is T-109's, not yours. The definitions carry no digit (`add-quantity-kind` refuses one).

1a. **The kind is a judgment, so it carries its warrant** (CLAUDE.md rule 8). **Chosen (pilot 2026-11-13):** two nullable columns on `base_parameters`, added with `ALTER TABLE ... ADD COLUMN`: `quantity_kind TEXT REFERENCES base_quantity_kinds(kind_id)` and `quantity_kind_observation_id INTEGER REFERENCES observed_terms(observation_id)`. The warrant is a POINTER to an observation (`db.py observe-term`: a source's verbatim `context_quote`, its `ref_id` and `locator`, which `observe-term` today checks against the source's retrieved bytes or records an exemption for), not a copied quote and not free prose. Reason: rule 5 (point, do not copy: the source's words already have a home), rule 8 (the answer and its warrant in named columns; who judged is `created_by_session`), CLAUDE.md §5(c) (the warrant's text is checked where it is written, by `observe-term`, not retyped here), and the 2026-11-06 schema-shape statement (one value per cell). The pilot's design (an operator-chosen kind with no warrant) was rejected because it records an answer no one can check. **`add-parameter`** takes `--quantity-kind` and `--quantity-kind-observation-id`, both optional at parse time (no `required=True`, no `choices=`: argparse cannot read rows and would refuse without naming the kinds), and `insert_parameter` refuses, **after every refusal it has today, T-010's included, so each existing refusal's tests still see their own message**, in this order: (i) no kind or a kind not in the table, naming every `kind_id` read from the table and `db.py add-quantity-kind`; (ii) no observation id, or one that is not a row of `observed_terms`, naming the flag and `db.py observe-term`; (iii) an observation whose `context_quote` holds no digit (`any(ch.isdigit() for ch in quote)`, which reads non-Latin digits too), saying that a passage stating no value cannot show what the quantity is measured in. The writer does not require the observation to be adjudicated to the term (the docstring of `insert_parameter` records why that gate was rejected) and does not compare the observation's words with the term's name (R11: a source's phrase is not normalised). The result dict gains `quantity_kind` and `quantity_kind_observation_id`. A CHECK naming both columns is not added; the writer holds it, as the migration note below says.

   **`add-quantity-kind`** (function `insert_quantity_kind`; flags `--kind-id`, `--definition`, `--approval-ref`, `--session`, `--dry-run`): refuses a blank or ill-shaped id (anything not matching `^[a-z][a-z_]*$`, the seed's own shape), a definition holding a digit (a kind is not a value), an `--approval-ref` that is not exactly one `## ` heading of the ledger (`dbcore.ledger_heading_count`), and an existing `kind_id` (naming the row). It writes through `dbcore.stamp_for(conn, "base_quantity_kinds", session)`.
2. **Keep T-010's refusal.** `dbcore.NON_QUANTITY_DOMAINS`, the refusal in `insert_parameter` that reads it, the fixture filter in `scripts/tests/test_scan_contract.py`, the sentence in `scripts/audit/research_batch_dod.py` and T-010's cases AP1-AP5 (`scripts/tests/test_run_pipeline_refusals.py`, section A7b) stay. **Chosen (pilot 2026-11-13), reversing this file's earlier instruction to delete them:** the pilot showed that with the kind in place `TERM-041` (functional_axis) and `TERM-075` (legal), which T-010 refuses, become promotable under any kind, and section 8 forbids weakening a refusal. The kind does not replace the domain rule: the domain is a fact of the term's row and the kind a fact of the parameter's, two facts and not one fact in two homes, and even with a warrant a lens or legal term can be pointed at an observation that states a number. Keep the amendable `domain` field of `amend-term`. Whether the domain rule should later be derived rather than held as a constant is not this task's question.
3. The ten live parameters get their kind in a separate research pull request (T-109), not here: the column is nullable for existing rows until then, and `add-parameter` enforces it for new ones.
4. **The split test is a rule of judgment, not code:** two cases are two parameters only when they cannot be placed on one scale or their accessibility directions differ. State it in the help text of `add-parameter`'s `--quantity-kind` (one sentence); build no check for it.
5. **Stage map.** Add `base_quantity_kinds: base` to `tables:` in `governance/stage-map.yaml`, in alphabetical order after `base_parameters: base`. Without it `build_graph.py --check` gains one failure (`tables in the schema but not in stage-map: ['base_quantity_kinds']`).
6. **Callers to repair in this pull request** (the pilot found these; your sweep in section 5 must find them again): every `insert_parameter` call in `scripts/tests/test_scan_contract.py` and `scripts/tests/test_db_amend_writers.py`, and T-010's case AP4 (the legitimate promotion) in `test_run_pipeline_refusals.py`, pass a kind and an observation chosen by query; `scripts/tests/test_evidence_cell_state_2_3.py` adds `'base_quantity_kinds'` and `'observed_terms'` to its live-DDL name list (it runs with `foreign_keys=ON`, and an INSERT into a table whose FK parent table is missing fails `no such table`, even with the column NULL); every operator-facing message that prints `db.py add-parameter --term-id ...` (`git grep -n -F "add-parameter --term-id" -- scripts ':(exclude)scripts/migrations'`: in the pilot four in `db.py`, one in `scripts/assess/assess_cell.py`, one in `scripts/audit/research_batch_dod.py`) gains the two flags; `workplan/pipeline-state-graph/machines.yaml` transition `M03.t4` gains a guard line for the kind and its warrant and an `evidence` needle quoting the new refusal's text.

**What reads what this task adds or changes:** `add-parameter` reads `base_quantity_kinds` and `observed_terms`; `add-quantity-kind` is read by T-047 (add by data); T-030 (units reference kinds); the engine's composer; T-109 (assigns the live parameters their kind and warrant).

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (the last line is `EXAMINED: … candidate(s)`; a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py` (this is the one sanctioned way `data/guidebook.db` changes). Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0 and a last line `Rebuilt ... successfully`; on stderr it prints `WARNING ... FK violations after <migration>` with up to five tuples such as `('item_taxonomy_links', 396, 'base_icf', 4)` for historical migrations: that is legacy drift its foreign-key snapshot reports as advisory, and only a warning naming your migration, or a tuple naming `base_parameters`, `base_quantity_kinds` or `observed_terms`, is yours) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). SQLite cannot add a `NOT NULL` foreign key or change a CHECK in place: use create, copy, drop, rename inside the migration, and list every view and index that names the table (`select type, name from sqlite_master where sql like '%<table>%'`; they must be recreated). The pull request contains no `scripts/migrations/data_*` file. **After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and include its output in the change:** a new table or column makes the generated `governance/context-map.yaml` stale, and `context_map_fresh` fails otherwise (every schema pilot hit this). **If every change is a new nullable column, `ALTER TABLE ... ADD COLUMN` is enough** (a CHECK that names two columns goes in the writer, as the file says); use create, copy, drop, rename only for a change SQLite cannot make in place.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `insert_parameter`, `add-parameter`, `NON_QUANTITY_DOMAINS`, `quantity_kind`, `'base_parameters'` (with the single quotes: it finds code that names the table as a string, which is how a fixture lists tables to copy)

**Builders of a changed table's DDL** (pilot 2026-11-13: the name sweep missed one). A test that copies a table's live `CREATE` statement from `sqlite_master` into a scratch database breaks when that table gains a foreign key whose parent it does not also copy, and no name above need appear near the break. Find every builder of `base_parameters` (the one table whose DDL this task changes):

```
git grep -l -F "sqlite_master" -- scripts ':(exclude)scripts/migrations' | xargs grep -l -F "base_parameters"
```

Each test file it prints goes on the before/after list of section 6. Open each and look for a list of table names passed to `sqlite_master`: on 2026-11-13 `scripts/tests/test_evidence_cell_state_2_3.py` (runs with `foreign_keys=ON`; it failed `sqlite3.OperationalError: no such table: main.base_quantity_kinds` in the pilot, repaired as section 4 item 6 says) and `scripts/tests/test_validate_evidence_state_2_4.py` (inserts into `base_parameters` with foreign keys off; green in the pilot, still a caller to run).

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

- `insert_parameter`: code and skills: `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_scan_contract.py`. Prose: `workplan/pipeline-state-graph/machines.yaml`.
- `add-parameter`: code and skills: `.claude/settings.json`, `scripts/assess/assess_cell.py`, `scripts/audit/research_batch_dod.py`, `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_scan_contract.py`, `scripts/validate_parameters.py`, `skills/run-pipeline_SKILL.md`. Prose: `CLAUDE.md`, `architecture/conformance-schema-findings.md`, `architecture/meta-scripts-spec.md`, `governance/research-contract.yaml`, `governance/stage-map.yaml`, `workplan/pipeline-state-graph/machines.yaml`.
- `NON_QUANTITY_DOMAINS`: no file on 2026-11-12, because T-010 had not merged. Once it has: `scripts/dbcore.py`, `scripts/db.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/audit/research_batch_dod.py`. This task keeps every one of them (section 4 item 2); each is a mention, except AP4 in `test_run_pipeline_refusals.py`, which is a caller (section 4 item 6).
- `'base_parameters'`: `scripts/assess/assess_cell.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_validate_evidence_state_2_4.py` (2026-11-13).
- **Not a mention, though listed under prose above:** `workplan/pipeline-state-graph/machines.yaml` transition `M03.t4` states `add-parameter`'s guards and is a caller (section 4 item 6). `governance/stage-map.yaml` must gain the new table (section 4 item 5). In the pilot these were left as mentions: `CLAUDE.md`, `skills/run-pipeline_SKILL.md`, `.claude/settings.json`, `governance/research-contract.yaml`, `architecture/*`, `scripts/validate_parameters.py`; re-read each, since a sentence stating what `add-parameter` refuses is a caller.

**`build_graph.py --check`, before and after.** The pilot saw the same failure count before and after once the stage-map line was in; without it, one more (`tables in the schema but not in stage-map`). Any other new failure is yours.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `test_scan_contract`, `test_author_presence`, `test_search_log_completeness`, `test_assess_cell_pilot`, `test_validate_evidence_state_2_4`, `migration_reproducibility`, `schema_reference_audit`, `test_db_integrity`, `column_vocabulary_audit`, `test_evidence_cell_state_2_3` (added after the pilot: it builds `base_parameters` from the live DDL, section 5). Add any other registered test the builder sweep of section 5 prints. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_scan_contract test_author_presence test_search_log_completeness test_assess_cell_pilot test_validate_evidence_state_2_4 migration_reproducibility schema_reference_audit test_db_integrity column_vocabulary_audit test_evidence_cell_state_2_3"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** Before: the evidence command gives rc=0 (section 3). After: `a`, `b`, `c` of section 3, and the cases below green.

**Where the cases go.** `scripts/tests/test_run_pipeline_refusals.py`, in a new section printed as `Section A7c: add-parameter requires a quantity kind and its warrant (T-020)`, directly after T-010's section A7b (cases AP1-AP5, which stay). Use the file's own `feature`, `record` and `skip` helpers, as A7b does. Cases (pilot 2026-11-13, adjusted to the chosen design):

- `T020-01` feature probe: `base_quantity_kinds` exists and `db.insert_quantity_kind` exists. Red on the unchanged code; T020-02 to T020-08 are gated on it, as A7b's are on AP1.
- `T020-02` a free term (probe below) with no kind is refused, and the refusal names every `kind_id` read from the table, not typed into the test.
- `T020-03` the same term with a kind not in the table is refused.
- `T020-04` a kind from the table and no observation id is refused, naming `--quantity-kind-observation-id`; a non-existent observation id (`select coalesce(max(observation_id),0)+1 from observed_terms`) is refused.
- `T020-05` a kind and an observation whose `context_quote` holds no digit (derive it: `select observation_id from observed_terms where context_quote not glob '*[0-9]*' order by 1 limit 1`) is refused. If none exists, `SKIPPED-NO-FIXTURE`.
- `T020-06` a kind and an observation whose quote holds a digit (derived as in section 3) is accepted; the row carries both values and the session.
- `T020-07` **no refusal weakened:** the first unpromoted term of a refused domain (AP2's probe), given a full kind and warrant, is still refused with T-010's domain message.
- `T020-08` add by data: `insert_quantity_kind` refuses a missing or unresolvable `--approval-ref`, an ill-shaped id, a digit in the definition, and an existing id; with the OD-24 heading it writes a fixture kind (`kind_id` built in the test, e.g. `task_fixture_kind`); `add-parameter` then accepts a free term with that kind and a valid observation. The test edits no file and writes only to its own scratch copy: that is the proof that a kind is added with no code edit. (This replaces "with `git status --porcelain scripts schemas` empty", which cannot hold while your change is uncommitted.)

Can it fail: show T020-01 red on the unchanged code, then seed a defect (disable each new refusal in turn with `if False and ...`), show T020-02 to T020-05 red, and remove the seed. In the pilot `EXAMINED:` rose by the cases added and nothing else.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T020-01`, `T020-02`, …) and confirm the prefix is free first (`grep -c '"T020-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (the "free term": the first term that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, whose name carries no digit, comparator or min/max word, and whose domain is not in `dbcore.NON_QUANTITY_DOMAINS`, so no other refusal stops it). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit** (a second run only for the reason given in the next bullet). It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read four things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`; **and every advisory failure, one by one.** `RESULT: PASS` and `PREFLIGHT: PASS` do not mean your change broke nothing: in the pilot the gate passed with a test this change had turned red (`test_evidence_cell_state_2_3`) listed among the advisory failures. For each advisory failure that is not in your before-run, run its registered `cmd` in a worktree of the base and see whether it is red there too:

```
git worktree add "$SCRATCH/base-wt" "$(git merge-base HEAD "$BASE")"
c=<check id>; cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); (cd "$SCRATCH/base-wt" && $cmd > "$SCRATCH/base-$c.txt" 2>&1; echo "$c base rc=$?")
git worktree remove --force "$SCRATCH/base-wt"                # when done
```
Red on the base: not yours; name it with both results. Green on the base and red on yours: yours; fix it, then re-run the gate **once more** and say in the pull request that it ran twice and why. The pilot met these as red on a pristine base: `scan_debt`, `verified_scan_integrity`, `validate_schema_cross_check`, `research_protocol_audit`, `metadata_integrity_audit` (re-derive; do not trust the list).
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: require a quantity kind and its warrant when a parameter is defined [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- you are asked, or tempted, to make `add-parameter` refuse an element mechanically (a column classing terms as element or quantity, a list of element words, a name pattern, a rule comparing the observation's words with the term's). Which terms name elements is a vocabulary the owner has not set; section 3 states that this task records the judgment and does not prevent it;
- you are asked, or tempted, to delete T-010's domain refusal or its tests (section 4 item 2 keeps them).

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
