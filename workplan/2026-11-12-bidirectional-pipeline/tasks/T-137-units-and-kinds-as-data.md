# T-137  A unit is added by data with its warrant, a kind's quote states a value in a unit of that kind, and a determination's bounds are stored exactly

_One task of a stacked pull request (owner instruction of 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). The ratification entry of 2026-11-19 says "each its own pull request" in its ACTION (2); those are the recorder's words, the owner's instruction of 2026-11-15 is stacked, and the stack stands. Read `CLAUDE.md` first; beyond it this file is self-contained. Why, and the options weighed: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, items 31, 41, 35 and 33 (section 3) and section 4 item 3, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number was read on 2026-11-19 with the command that produces it: re-run it._

**Pilot status.** Not piloted. Authored 2026-11-19 from the ratified adjudication; evidence run read-only at `a6c478e0` (schema 159). Expect a defect in this file; report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-137 |
| Title | A unit is added by data with its warrant, a kind's quote states a value in a unit of that kind, and a determination's bounds are stored exactly |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (rule 10); one schema migration (units keyed by id with their spellings and warrants; exact bounds), two verbs (`add-unit`, `add-unit-spelling`), a figure reader, the engine's bound output, a dated line in T-132 |
| Executor | NOT FOR SONNET: Opus-class: a unit's warrant, the factor refusal, the numeral reader, the stored form of bounds |
| Traces to | OD-24 (delegated: kinds "extended by data with a warrant"); OD-22 (delegated); OD-71 (owner); "pipeline must not have hard coded behaviours" (2026-11-12 (seventh)); "you have to compute it" (2026-09-09, evening); T-030 sweep items 1, 3 and 7 and T-020's digit test (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` lines 49, 51, 63; `scratchpad/session_2026-11-16-remediation-batch-1-tooling-stack/sweep-list.md` line 10) |

## 2. Preconditions

- **The integration base.** A task named below is merged if its commit is on `HEAD` (the batch's branch) or on `origin/main`. `$BASE` serves preconditions only; `BASE_PRE` every diff, gate and count.
- **Tasks that must be merged to the integration base first:** T-030 and T-083, with their repairs. Check by subject: `git log --oneline HEAD | grep -F -e "hold units and conversions as data" -e "repair T-030 after the adversarial pass" -e "repair T-083 after the adversarial pass"` prints three lines. Derive your migration number after any other on the branch.
- **Owner decisions:** OD-71, answered by the owner.
- **Delegated resolutions this task rests on:** OD-22 and OD-24, read through the gate of the convention of 2026-11-12, before you start and before you commit; anything but OPEN is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-71 OD-22 OD-24; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19 — the third adjudication" references/project-standards.md
```
  Printed on 2026-11-19: `OD-71 OPEN (owner)`, `OD-22 OPEN (delegated; not required)`, `OD-24 OPEN (delegated; not required)`, `1`. Items 31, 41, 35 and 33 carry no OD number; they are ratified by reference (the last line must print `1`). If a later entry narrows "Ratify all", stop.
- **Tests that must be red before you start:** `T137-01`, `T137-07`, `T137-10` (section 6).
- **Set-up** (stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1):

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
git rev-parse HEAD > "$SCRATCH/base_pre"; sha256sum data/guidebook.db | tee "$SCRATCH/db.sha"   # no git switch -c: stay on the batch's branch
```
- **Shell variables do not survive between calls:** begin each block with the `export SCRATCH=…` line and `BASE_PRE=$(cat "$SCRATCH/base_pre")`; probe with `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline and `--session session_task-probe`; never delete `refusals.jsonl`. `/session-open` is the coordinator's.

## 3. The problem, in the guidebook's terms

A determination states a figure in the units its sources used, converted exactly. **A unit enters only by a hand-written migration** (`base_units` has no writer and no warrant), keyed by one spelling, so neither a unit in newtons nor `мм` or `毫米` beside `mm` has a route: a hard-coded behaviour (owner, 2026-11-12 (seventh)); four of six kinds hold no unit. **A kind is warranted by any quote holding a digit**, so "Class 1" warrants "length". **Bounds are stored as floats**: the engine computes Fractions and writes `float(...)` (1:12 is stored as 8.333…, not `25/3`, `str(Fraction(100, 12))`). That a determination of an older rule version reads current belongs to T-132 (item 4).

**Evidence commands** (read-only):

```
python3 -I -c "
import sqlite3,sys;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('base_units' in dbcore.writable_tables(c), [r[1] for r in c.execute('pragma table_info(base_units)')])
print(c.execute('select k.kind_id, count(u.unit) from base_quantity_kinds k left join base_units u on u.kind_id=k.kind_id group by 1 order by 1').fetchall())
print([(r[1],r[2]) for r in c.execute('pragma table_info(specifications)') if r[1] in ('value_min','value_max')], c.execute('select count(*), sum(retired_at is null), count(value_min), count(value_max) from specifications').fetchone(), c.execute('select distinct typeof(value_max), value_max from specifications where value_max is not null').fetchall())
print(c.execute('select count(*) from base_parameters where quantity_kind_quote is not null').fetchone())"
git grep -n "INSERT INTO base_units" -- scripts ':(exclude)scripts/migrations' | cut -d: -f1 | sort | uniq -c
grep -n -F "holds no digit" scripts/db.py | cut -c1-12; grep -n -F "float(vmin) if vmin" scripts/assess/assess_cell.py | cut -c1-12; grep -n -F "AND rule_version = ?" scripts/assess/assess_cell.py | cut -c1-12
```

**Printed on 2026-11-19:** `False` and ten columns with no warrant cell; `[('colour_temperature', 0), ('force', 0), ('gradient', 2), ('length', 5), ('luminous_reflectance', 0), ('time', 0)]`; `[('value_min', 'REAL'), ('value_max', 'REAL')] (8, 0, 0, 5) [('real', 5.0)]` (none live; five retired rows hold 5.0); `(0,)` (no stored kind quote to re-judge); fixture INSERTs in two test files only; one line each at `7825:` of `db.py`, `991:` and `1852:` of `assess_cell.py`. This agrees with the adjudication.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, CLAUDE.md §8: do nothing; change a convention; reuse; delete the cause; only then add the smallest code. Every refusal names the next act. Do the items in order.

**One schema migration** (number derived at execution: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; `scripts/migrations/NNN_units_warrant_and_exact_bounds.sql`, ending with `PRAGMA user_version = NNN`).

1. **Units and their spellings, by data, with a warrant (item 31).**
   - **Schema (the same migration; it compensates 149's table keyed by one spelling).** `base_units` is rebuilt as the unit: `unit_id INTEGER PRIMARY KEY AUTOINCREMENT`, `kind_id`, the factor, `figure_form`, `system`, and the warrant cells `quote` (the defining standard's words, verbatim), `source_url`, `source_page`, `source_clause`, `source_line`, `ref_id` (provenance only, no foreign key: OD-71), checked as the `quantity_kind_*` cells are (156's whitespace set), all present or all absent. `ux_base_units_canonical` stays: one factor-1 unit per kind. A new base table `base_unit_spellings` holds each written form of a unit, one per row: `spelling`, `unit_id` (foreign key), its own warrant cells with `judge` and `reason`, all present or all absent, the stamp; unique on (`spelling`, `unit_id`). A unit's first spelling carries no warrant of its own: the unit row's warrant is its one home (rule 5); a later spelling carries the judgment that it denotes the unit. So `мм`, `millimetres` and `毫米` are spellings of the one canonical length unit, never second factor-1 units, and `%` may spell a gradient unit and a luminous-reflectance unit at once (two units, two kinds, one spelling). The copy writes each seeded row's text as its unit's first spelling, with no warrant (factors pinned by T030-13; invent no locator). Add `base_unit_spellings: base` to `governance/stage-map.yaml`. No object referenced `base_units` on 2026-11-19 (`select name from sqlite_master where sql like '%REFERENCES base_units%'`).
   - **What reads a spelling:** `dbcore.load_units` (rewritten to join spellings to units), every converter through it, the engine's composition and the figure reader below. A `claimed_unit` is matched against every spelling. A spelling that names units of one kind resolves; one that names units of several kinds resolves by the parameter's `quantity_kind` where the caller has it, and otherwise stands alone, with the ambiguity said in the note or the refusal (never a guess, never the first row). No spelling is ambiguous today, so stored answers do not move; prove it (T137-10).
   - **The shared figure reader** (one helper in `scripts/dbcore.py`, beside `load_units`): the figures a text states in units of a given kind. **Numerals:** a run of Unicode decimal digits of any script (category `Nd`, fullwidth included, valued with `unicodedata.decimal`), after NFKC normalisation. A numeral holding a comma, or a separator followed by exactly three digits (`1,200`, `1.200`, `25,4`, `1 000`), is **ambiguous** (decimal or grouping): it counts as a figure for a presence test, and it is never valued: a test that needs the value refuses it, naming the numeral and the next act (quote a statement whose numeral is unambiguous). Nothing is ever read as one reading of an ambiguous numeral. **Unit after the numeral** (optional whitespace between): a spelling holding a wide character (Unicode East Asian Width `W` or `F`) is matched as a substring; any other spelling must not be followed by a narrow letter (a character of category `L*` whose width is not `W` or `F`), so `1200 mm` and `幅は1200mm以上` are read and `120 mmHg` is not. A ratio `a:b` (the shape `_RATIO_RE` reads) counts for a kind holding a `figure_form = 'ratio'` unit. Kinds, units and spellings come from the rows; no script, language or unit is typed; reuse T-136's containment helper if it is on the branch. **Not read, stated in the docstring:** numerals written in words (`viisi prosenttia`), fractions in words (`12분의 1`, `8分の１`), a slash fraction with no unit (`1/12`), `1 in 12` (read as one inch: the spelling `in` is an English word).
   - **`db.py add-unit`** (`--kind-id`, `--spelling`, `--factor-numerator`, `--factor-denominator`, `--figure-form`, `--system`, `--quote`, `--source-url`, `--source-page` or `--source-clause`, `--source-line`, `--ref-id`, `--session`, `--dry-run`; check every flag name against `dbcore._SECRET_WORDS` first and stop on a clash) writes a unit and its first spelling; its warrant is the defining standard's words, so it takes no judge. Refuses, in order: a blank session; a spelling refused by `dbcore.unit_refusal` or blank; a spelling already spelling a unit of this kind (name it: one written form, one factor, per kind); an unknown kind (name `add-quantity-kind`); a factor that is not two positive integers in lowest terms; a `--figure-form` or `--system` outside its CHECK (`dbcore.check_declared`); a kind's first unit whose factor is not 1, and a second factor-1 unit of a kind (name `add-unit-spelling` for another spelling of it); a missing or partial warrant, a zero-width character, a malformed URL (`_check_base_locator`); a quote with no digit (T-020's floor, digits of any script); and **a quote that does not state the factor**: it holds a valued figure in the new spelling and a valued figure in a held spelling of the same kind whose canonical values are equal under the factor, exactly (Fraction), or, for a kind's first unit, a figure in the new spelling. So `1 in = 25.4 mm` warrants 127/5, `1 in = 25 mm` does not, and `1 in = 25,4 mm` is refused as ambiguous, never read as 4 mm. Name which half was missing.
   - **`db.py add-unit-spelling`** (`--unit-id`, `--spelling`, the warrant flags, `--judge`, `--reason`, `--session`, `--dry-run`) records another written form of a held unit. That two forms denote one unit is a judgment (rule 8: the script asks for it and records the judge and the reason). Refuses: an unknown unit; a spelling refused by `unit_refusal`; one already spelling this unit, or a unit of this unit's kind with another factor; a missing or partial warrant; a quote that does not hold the spelling (script-derived containment, as the reader's unit match). It asks no numeral, so a spelling in any script, written beside numerals in words, has a route.
   - `base_units` and `base_unit_spellings` then enter `dbcore.writable_tables` by derivation and `emit_batch_sql.py` captures them: show both, never edit a list. `degrees` (item 32) cannot pass the factor test and stays standing alone (T-143's).
2. **The kind's quote states a value in a unit of that kind (item 41).** In `_kind_refusal` (one home for `add-parameter` and `set-parameter-kind`), the quote must hold a digit (T-020, kept) **and** at least one figure, valued or ambiguous, in a recorded spelling of a unit of the declared kind. A kind with no unit is refused naming `add-unit`. **Before building this item**, run the reader over every live figure's `claim_text` whose text holds a digit and that the parameter's kind could govern (`select x.extraction_id, x.claim_text from source_value_extractions x where x.retired_at is null`, digits by `unicodedata`), and list each the digit test accepts and the reader reads no figure in, with its script (by `unicodedata.east_asian_width` and category, never a language list). The critic found such figures in Korean, Japanese and Finnish sources on 2026-11-19 (live digit-bearing figures holding a wide character: count with that query and `east_asian_width`). **If any such figure exists, do not build item 2** (stop condition): the adjudication gives the kind quote no judged route (item 41: "a number followed by a unit of the declared kind, read from `base_units`"), and building it would leave a non-English source no way to warrant a kind. Commit items 1, 3 and 4, report the list and open point O-1; the digit test stays.
3. **Exact bounds on `specifications` (item 35).** Rebuild `specifications` (create, copy, drop, rename; model on `scripts/migrations/138_drop_medical_lens.sql`, the last rebuild) with `value_min` and `value_max` declared `TEXT`, each NULL or the text `str(fractions.Fraction(…))` prints (an integer, or numerator/denominator in lowest terms with a positive denominator). The CHECK holds the character shape (`typeof = 'text'`, digits with an optional leading `-` and at most one `/`, no `.`) of the bound **in the row's `value_unit`**; the writer holds lowest terms, and a test round-trips every stored cell through `Fraction`. A bound with no exact rational value (one governed by a tangent figure, T-143 item 2b) cannot be held by this form: T-143 changes or extends this CHECK by its own migration, and this task adds nothing for it (dated line in T-143, item 5 below). The copy converts a stored REAL only when it is integral (`value_max = CAST(value_max AS INTEGER)`), as `CAST(CAST(… AS INTEGER) AS TEXT)`; a guard (the `_156_guard` pattern of migration 156) aborts the migration if any stored bound is not integral, because the exact figure of a float cannot be recovered from it and inventing one is a fabricated value. Recreate every view, index, trigger and child key naming the table (`select type, name from sqlite_master where sql like '%specifications%'`); four views select `s.*`: read their readers. The engine (`scripts/assess/assess_cell.py`, `_compose_headline`'s return) yields `str(vmin)` and `str(vmax)` for a Fraction instead of `float(...)`, and `STORED_ANSWER`'s comparison in `stale_determinations` then compares text with text; read every other reader of the two columns (`git grep -n -E "value_min|value_max" -- scripts schemas skills ':(exclude)scripts/migrations'`). Bump `RULE_VERSION` by the engine's contract in its comment (the stored answer changes form for a non-integral bound); if the sha payload changes, K01's version sets in `test_db_integrity.py` take the label. Show that the replay plan orders the migration after every data migration (several INSERT these columns: `grep -l -E "value_min|value_max" scripts/migrations/data_*`), with `python3 -c "import sys;sys.path.insert(0,'scripts');import migrate_db as m;p=m.build_plan();print(p[-1][:2], [s[:2] for s in p if s[0]=='data'][-1])"` (the last step is your schema migration; rule 5).
4. **A rule-version change reads stale (item 33): into T-132, not here.** Append to `workplan/2026-11-12-bidirectional-pipeline/tasks/T-132-drift-detectors-bind.md`, after its last line, this dated line and nothing else:

   > **Amended 2026-11-19 (third adjudication item 33, ratified 2026-11-19; "you have to compute it", owner 2026-09-09 (evening)):** `stale_determinations` in `scripts/assess/assess_cell.py` filters `rule_version = RULE_VERSION`, so a live determination written under an earlier rule reads current. This task also changes it to report such a determination as stale, with `rule_version` among its differing fields, rather than skip it (a cache of a rule no longer in force is not the computation); the Kind line's "no code path" is superseded by this one change. Add a red-then-green case: on a scratch copy, a live determination stamped with an earlier label is reported. The ratchet of item 1 is read after this change.

   Do not change `stale_determinations`' filter in this task.
5. **Reconciled with T-143.** The repair of 2026-11-19 appended a dated line to `tasks/T-143-degrees-rule.md` saying that T-143 changes or extends item 3's CHECK by its own migration (`grep -c -F "Amended 2026-11-19 (repair of T-137" workplan/2026-11-12-bidirectional-pipeline/tasks/T-143-degrees-rule.md` prints 1). Add nothing for it.

**What reads it:** units and spellings: `load_units`, every converter, the engine, `emit_batch_sql.py`, T-047, item 34's research. Warrants: the owner browser. The reader: `add-unit`, `_kind_refusal`. Exact bounds: `stale_determinations`, the four `s.*` views, render. **Without it**, a unit a source writes in any script cannot enter without hand SQL; a kind can rest on a clause number; the book states a bound no source stated.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), naming what each addition reads and replaces.

**Migration discipline.** `joined_cells_census.py` before and after; apply only with `migrate_db.py`; prove with `migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `migration_reproducibility.py --deep` (PASS); no `data_*` file; regenerate `governance/context-map.yaml` (`scripts/generate/context_map.py`).

## 5. Caller sweep

Names to sweep: `base_units`, `load_units`, `unit_kind`, `kind_members`, `canonical_unit`, `UnitRow`, `_kind_refusal`, `holds no digit`, `quantity_kind_quote`, `add-quantity-kind`, `value_min`, `value_max`, `STORED_ANSWER`, `RULE_VERSION`, `specifications` (views and child tables only).

A caller is a hit whose behaviour or truth changes; a hit that stays true is a mention. **Fixing a caller is in scope** (rule 4). Left out: `workplan/` except `machines.yaml`, the ledger, `scripts/migrations/`, the frozen records.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
New verbs: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after; report the difference.

**Callers found on 2026-11-19** (re-run): `scripts/db.py` (`_kind_refusal`, `_KIND_WARRANT`'s help, the new verbs); `scripts/dbcore.py` (`load_units` and its callers; two sentences saying units enter "by migration"); `scripts/assess/assess_cell.py` (`_compose_headline`'s return, `STORED_ANSWER`, `RULE_VERSION`); tests `test_assess_cell_pilot.py` (old-shape `base_units` fixtures, float-bound cases), `test_run_pipeline_refusals.py` (T-020 cases, two fixtures), `test_db_amend_writers.py` (T-083 kind quotes, if item 2 is built), `test_db_integrity.py` (only if the sha payload changes); `schemas/base.py` (`ConditionValue`, likely a mention); `governance/stage-map.yaml`; `skills/run-pipeline_SKILL.md`; `governance/context-map.yaml` (regenerated).

## 6. Verification

**Step 1, before any edit: the before-run.** Checks that read what this task touches: `test_assess_cell_pilot test_run_pipeline_refusals test_db_amend_writers test_db_integrity derivation_handshake_integrity derived_not_curated_audit column_vocabulary_audit schema_reference_audit migration_reproducibility context_map_fresh`.

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137"
CHECKS="test_assess_cell_pilot test_run_pipeline_refusals test_db_amend_writers test_db_integrity derivation_handshake_integrity derived_not_curated_audit column_vocabulary_audit schema_reference_audit migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Record any check red here; no `EXAMINED:` line, or `EXAMINED: 0`, means it examined nothing: say so.

**Step 2: red before, green after.** Case ids `T137-NN` (`git grep -c '"T137-' -- scripts/tests` printed nothing on 2026-11-19), in `scripts/tests/test_run_pipeline_refusals.py` beside the T-020 and T-030 cases, or in `scripts/tests/test_assess_cell_pilot.py` for the engine cases. Probes by query or on the test's own copy labelled `TASK-FIXTURE`; type nothing the database can derive. Show each case red on a seeded defect you then remove (`cmp`).

| Case | Red before (or the seeded defect) | Green after |
|---|---|---|
| T137-01 | `add-unit` and `add-unit-spelling` are not verbs; `base_units` is not in `dbcore.writable_tables` | a fixture unit and a second spelling are written with their warrants; both tables are in the derived capture set and `emit_batch_sql.py` captures them |
| T137-02 | seeded: remove each refusal in turn | each refusal of item 1 fires and writes nothing (table hash unchanged) |
| T137-03 | seeded: compare without exactness (float) | a quote whose second figure differs from the factor by less than any float tolerance is refused; the exact statement passes; a ratio-form statement passes for a ratio unit |
| T137-04 | seeded: drop the warrant CHECK on a scratch rebuild | a raw INSERT of a partial warrant is refused; the seeded rows (no warrant) pass |
| T137-05 (only if item 2 is built) | `add-parameter` with a kind quote "Class 1" (a digit, no unit) succeeds | refused, naming the units of the kind (read from `base_units`); a quote stating a figure in a unit of another kind is refused; one in a unit of the kind passes; a kind with no unit is refused naming `add-unit` |
| T137-06 | seeded in turn: `\w` boundaries; ASCII digits only; read `,` as a decimal; read `,` as grouping | `120 mmHg` is not read as mm; `幅は1200mm以上` and fullwidth digits are read; `1,200 mm`, `1.200 mm`, `25,4 mm` are figures but never valued (an exact test refuses them by name); live non-Latin claim texts chosen by `unicodedata`, never a typed language |
| T137-10 | `мм` cannot be added at factor 1 beside `mm` (canonical index), nor `%` for a second kind (primary key) | `add-unit-spelling` records `мм` for the canonical length unit; `add-unit` records a `%` unit of another fixture kind; a spelling naming units of two kinds resolves by the parameter's kind and otherwise stands alone, said; on the canonical copy every unit and every stored answer reads as before (compare `load_units` and `stale_determinations` before and after) |
| T137-07 | the engine writes a REAL bound; `typeof(value_max)` is `real` | a determination computed on a scratch copy stores text that round-trips through `Fraction` to the engine's exact value (choose a parameter whose figures give a non-terminating bound by query, or build one) |
| T137-08 | seeded: drop the guard | on a scratch copy holding a non-integral REAL bound the migration aborts; on the canonical copy it converts the stored 5.0 to `5` and `--rebuild` reproduces the database |
| T137-09 | seeded: append nothing to T-132 | the T-132 line is present once (`grep -c -F "Amended 2026-11-19 (third adjudication item 33"` on that file); `stale_determinations`' filter is unchanged |

**Step 3: the after-run.** The same loop with `after-`; diff the failing lines check by check (`grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL'`). No new failing case, except one asserting a float bound, updated and named.

**Step 4: the gate, once**, when every edit is made, in the background with a long timeout, waiting with an until-loop on its output file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137"; BASE_PRE=$(cat "$SCRATCH/base_pre")
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass), any blocking `FAIL` (one red on `$BASE_PRE` too is not yours: give both lines).

## 7. Commit

After the gate is clean, staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status`):
```
git commit -m "governance: units enter by data with a warrant, a kind's quote states a value in its unit, and bounds are stored exactly [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, each caller and what was done, the RULE_VERSION label and why>" -m "<the attribution trailers your session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`; do not add a unit row in the migration (units enter through `add-unit` from now on; placing the units of item 34 is research, rule 10).
- Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`; do not push, open a pull request, subscribe, or run `/adversarial` or `/batch-done`.
- Do not type a list of units, kinds, scripts, languages, number words or a float tolerance (rule 8); do not value an ambiguous numeral; do not build a non-linear conversion (T-143's).
- Do not invent a warrant for the seeded rows, or an exact value for a non-integral stored float.
- Do not change `stale_determinations`' filter (T-132's), `SHOWN_STEPS` (OD-22) or `value_notations`.
- Add no table, column, flag or verb section 4 does not name; list any helper; hand-type no count. Fixing a caller is in scope.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level. The digit test stays, with item 2's test added to it.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, saw and expected) when:
- a precondition of section 2 is not met, or the gate prints anything but OPEN, or a later ledger entry narrows the ratification;
- an evidence command of section 3 prints otherwise (in particular: a live determination exists, a stored bound is not integral, or a parameter already holds a kind quote that the new test would refuse);
- a flag name of `add-unit` clashes with `dbcore._SECRET_WORDS`;
- a red test is not red before or not green after one honest attempt;
- the sweep finds a caller you cannot repair without adding something section 4 does not name;
- a check green in the before-run is red after, other than a case asserting the digit test or a float bound;
- `migrate_db.py --rebuild` does not reproduce the database, or the replay plan does not order your migration after every data migration;
- the list of item 2's pre-build run is not empty: build no item 2 (section 4);
- a spelling is found to name units of two kinds today, or a stored answer moves under the new `load_units`;
- you would have to guess a value, a unit's factor, a locator or an owner's intent.

**Open points for the owner (carried in the report).** O-1: a kind quote whose value is written in words or as a fraction in words (`12분의 1`, `8分の１`, `viisi prosenttia`) has no deterministic reading and the adjudication gives no judged route; until the owner gives one, item 2 is not built where such figures exist. O-2: a unit whose defining statement gives its factor only in words, or only with an ambiguous numeral, has no route through `add-unit` (item 31 asks for "the exact fraction its defining standard states"); is a judged factor wanted?

## 10. Rollback

Before merge the coordinator drops the commit; after merge, `git revert` in a new pull request. A committed migration is never edited: fix forward (rule 3).

## 11. Adversarial pass and pull request

The coordinator runs `/adversarial`, `/batch-done`, the push and the pull request. Report per `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 3, with a heading "Task-file defects".
