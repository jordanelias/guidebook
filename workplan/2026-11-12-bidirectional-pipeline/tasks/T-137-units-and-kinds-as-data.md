# T-137  A unit is added by data with its warrant, a kind's quote states a value in a unit of that kind, and a determination's bounds are stored exactly

_One task of a stacked pull request (owner instruction of 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Why this task exists, and the options it chose between: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, items 31, 41, 35 and 33 (section 3) and section 4 item 3, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number in this file was read on 2026-11-19 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-19 by an Opus-class task author from the ratified third adjudication; its evidence commands were run read-only on 2026-11-19 against branch `ccr-cc893571-i4lug4` at `a6c478e0` (schema version 159) and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-137 |
| Title | A unit is added by data with its warrant, a kind's quote states a value in a unit of that kind, and a determination's bounds are stored exactly |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10); one schema migration (`base_units` warrant cells; `specifications` rebuilt with exact bounds), one verb (`db.py add-unit`), one shared figure reader in `scripts/dbcore.py`, the engine's bound output, a dated amendment line in `tasks/T-132-drift-detectors-bind.md` |
| Executor | NOT FOR SONNET: Opus-class. The task writes the shape of a unit's warrant, the meaning of the refusal that a quote states the factor, and the stored form of a determination's bounds |
| Traces to | OD-24 (delegated: kinds "extended by data with a warrant"; `grep -n -F "OD-24:" references/project-standards.md`); OD-22 (delegated: a minimum never shown below the source, a maximum never above); OD-71 (owner, the warrant's shape); the owner's "pipeline must not have hard coded behaviours" (2026-11-12 (seventh)) and "you have to compute it" (2026-09-09, evening); T-030 sweep items 1, 3 and 7 and T-020's digit test (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` lines 49, 51, 63; `scratchpad/session_2026-11-16-remediation-batch-1-tooling-stack/sweep-list.md` line 10) |

## 2. Preconditions

- **The integration base.** On this stacked batch the earlier tasks are commits on the batch's branch (`ccr-cc893571-i4lug4`); a task named below is merged if its commit is on `HEAD` or on `origin/main`. The set-up block sets `$BASE` (preconditions only) and records `BASE_PRE` (every diff, gate and count).
- **Tasks that must be merged to the integration base first:** T-030 and T-083, with their repairs. Check by subject: `git log --oneline HEAD | grep -F -e "hold units and conversions as data" -e "repair T-030 after the adversarial pass" -e "repair T-083 after the adversarial pass"` prints three lines. If T-136 is also on the branch, derive your migration number after it (section 4).
- **Owner decisions:** OD-71, answered by the owner.
- **Delegated resolutions this task rests on:** OD-22 and OD-24, each read only through the gate of the convention of 2026-11-12 (`grep -n -F "## Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you commit; anything but OPEN is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-71 OD-22 OD-24; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19 — the third adjudication" references/project-standards.md
```
  Printed on 2026-11-19: `OD-71 OPEN (owner)`, `OD-22 OPEN (delegated; not required)`, `OD-24 OPEN (delegated; not required)`, `1`. Items 31, 41, 35 and 33 carry no OD number; they are ratified by reference (the last line must print `1`). If a later entry narrows the ratification ("the breadth of 'all' is the first to confirm", its ACTION (3)), stop.
- **Tests that must be red before you start:** `T137-01`, `T137-05`, `T137-07` (section 6).
- **Set-up** (stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1):

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
git rev-parse HEAD > "$SCRATCH/base_pre"; sha256sum data/guidebook.db | tee "$SCRATCH/db.sha"   # no git switch -c: stay on the batch's branch
```
- **Shell variables do not survive between tool calls.** Begin every later block with the `export SCRATCH=…` line and `BASE_PRE=$(cat "$SCRATCH/base_pre")`; pass `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline on every probe, under `--session session_task-probe` (never the running session; never delete `refusals.jsonl`). `/session-open` and `scratchpad/CURRENT` are the coordinator's.

## 3. The problem, in the guidebook's terms

A determination states a figure for disabled people in the units the sources used, converted exactly between them. Three things in that chain are not yet data the pipeline can extend or trust. **A unit can enter only by a hand-written migration** (`base_units` has no writer and no warrant), so a source stating a force in newtons or a luminance in lux has no route in: a hard-coded behaviour (owner, 2026-11-12 (seventh)), and four of the six quantity kinds hold no unit at all. **A quantity kind is warranted by any quote holding a digit**, so "Class 1" or a year warrants "length". And **a determination's bounds are stored as floating-point numbers**: the engine computes them exactly (as fractions) and then writes `float(...)`, so the stored figure is not the figure the sources support (1:12 is stored as 8.333…, not 100/12). A fourth defect, that a determination written under an older rule version reads current, belongs to T-132 (section 4, item 4).

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

**Printed on 2026-11-19:** `False` and the ten columns `unit, kind_id, factor_numerator, factor_denominator, figure_form, system, created_at, created_by_session, updated_at, updated_by_session` (no writer, no warrant); `[('colour_temperature', 0), ('force', 0), ('gradient', 2), ('length', 5), ('luminous_reflectance', 0), ('time', 0)]`; `[('value_min', 'REAL'), ('value_max', 'REAL')] (8, 0, 0, 5) [('real', 5.0)]` (eight determinations, none live, five retired ones holding the bound 5.0); `(0,)` (no parameter holds a kind quote, so tightening the quote test re-judges nothing stored); fixture INSERTs only in `scripts/tests/test_assess_cell_pilot.py` (3) and `scripts/tests/test_run_pipeline_refusals.py` (2); then one line each at `7825:` of `db.py`, `991:` and `1852:` of `assess_cell.py`. This agrees with the adjudication (items 31, 35, 41; it gave no count for item 31, and item 34's broader count is research, not this task).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Every refusal names the next act and writes nothing. Do the items in this order: item 2 reads the figures item 1's reader finds.

**One schema migration** (number derived at execution: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; `scripts/migrations/NNN_units_warrant_and_exact_bounds.sql`, ending with `PRAGMA user_version = NNN`).

1. **`add-unit`, by data, with a warrant (item 31).**
   - **Schema.** `base_units` gains `quote` (the defining standard's words, verbatim), `source_url`, `source_page`, `source_clause`, `source_line`, and `ref_id` (provenance only, no foreign key: OD-71), spelled and checked as `base_parameters`' `quantity_kind_*` cells are (migration 156's whitespace and zero-width set). CHECK: the warrant cells all present (quote, URL, a page or a clause; line optional) or all absent. The seven rows migration 149 seeded (`select unit from base_units where created_by_session='migration_149'`) carry no warrant and stay as they are: their factors are pinned to their definitions by T030-13; do not invent a locator for them.
   - **The shared figure reader.** One helper in `scripts/dbcore.py`, beside `load_units`, that lists the figures a text states in units of a given kind: a numeral (`\d+(?:\.\d+)?`, the shape `to_canonical` and `_RATIO_RE` already read) followed, after optional whitespace, by a unit's own text on a word boundary for a `figure_form = 'number'` row, or a ratio `a:b` for a kind holding a `figure_form = 'ratio'` row; each figure returned as its exact value on the kind's canonical scale (`to_canonical`). Units come from `load_units`; no unit, kind or notation is typed. It takes an optional candidate row (unit, factor, form) so `add-unit` can read a unit not yet held. Known limit, stated in its docstring and not patched: a numeral written with a decimal comma (`25,4`) is not read, and `1 in 12` reads as one inch (the unit `in` is an English word); the refusal text names both.
   - **`db.py add-unit`** (`--unit`, `--kind-id`, `--factor-numerator`, `--factor-denominator`, `--figure-form`, `--system`, `--quote`, `--source-url`, `--source-page` or `--source-clause`, `--source-line`, `--ref-id`, `--session`, `--dry-run`; check every flag name against `dbcore._SECRET_WORDS` first, and stop if one clashes). Refuses, in this order: a blank session; a unit text that is blank, untrimmed, or refused by `dbcore.unit_refusal`; a unit already held (no overwrite: a factor changed under stored figures changes what they mean; name the held row); a kind that is not a row of `base_quantity_kinds` (name `add-quantity-kind`); a factor that is not two positive integers in lowest terms (one factor, one spelling: the canonical index tests numerator = denominator); a `--figure-form` or `--system` outside its CHECK (`dbcore.check_declared`); a first unit of a kind whose factor is not 1 (`dbcore.canonical_unit` would otherwise raise for the kind); a second factor-1 unit of a kind (name the held one; the unique index is the backstop); a missing or partial warrant, a zero-width character, a malformed URL (`_check_base_locator`); and **a quote that does not state the factor**: it must hold one figure in the new unit and one in a unit of the same kind already held whose canonical values are equal under the given factor, exactly (Fraction); for a kind's first unit, a figure in the new unit alone. So `1 in = 25.4 mm` warrants `in` at 127/5 and `25 mm` does not; `1:20 (5 %)` warrants a ratio unit at 100. Name which half was missing.
   - It writes one row with the stamp. `base_units` then enters `dbcore.writable_tables` by derivation (its INSERT literal), and `emit_batch_sql.py` captures it: show both, never edit a list. A non-linear unit (`degrees`, item 32) cannot pass the factor test and stays standing alone: that is DEFERRED to T-059, not built here.
2. **The kind's quote states a value in a unit of that kind (item 41).** In `_kind_refusal` (one home for `add-parameter` and `set-parameter-kind`), the digit test is replaced by the shared reader: the quote must hold at least one figure in a unit of the declared kind. A kind with no unit is refused naming `add-unit` (today four kinds, by the command of section 3: say so in the pull request, since T-109's research rows for those kinds now need `add-unit` first). No live row is re-judged (section 3 printed `(0,)`).
3. **Exact bounds on `specifications` (item 35).** Rebuild `specifications` (create, copy, drop, rename; model on `scripts/migrations/138_drop_medical_lens.sql`, the last rebuild) with `value_min` and `value_max` declared `TEXT`, each NULL or the text `str(fractions.Fraction(…))` prints (an integer, or numerator/denominator in lowest terms with a positive denominator). The CHECK holds the character shape (`typeof = 'text'`, digits with an optional leading `-` and at most one `/`, no `.`); the writer holds lowest terms, and a test round-trips every stored cell through `Fraction`. The copy converts a stored REAL only when it is integral (`value_max = CAST(value_max AS INTEGER)`), as `CAST(CAST(… AS INTEGER) AS TEXT)`; a guard (the `_156_guard` pattern of migration 156) aborts the migration if any stored bound is not integral, because the exact figure of a float cannot be recovered from it and inventing one is a fabricated value. Every view, index, trigger and child foreign key naming the table is recreated (`select type, name from sqlite_master where sql like '%specifications%'`: on 2026-11-19 eight views, two indexes, one trigger, three child tables; four views select `s.*`, so their column types change with the table: read each reader of them). The engine (`scripts/assess/assess_cell.py`, `_compose_headline`'s return) yields `str(vmin)` and `str(vmax)` for a Fraction instead of `float(...)`, and `STORED_ANSWER`'s comparison in `stale_determinations` then compares text with text; read every other reader of the two columns (`git grep -n -E "value_min|value_max" -- scripts schemas skills ':(exclude)scripts/migrations'`). Bump `RULE_VERSION` by the engine's own contract in its comment ("same evidence + same rule_version => same answer"): the stored answer changes form for any bound that is not an integer, so give the new label and say so in its comment; the sha payload is unchanged unless you change it (then K01's version sets in `test_db_integrity.py` need the label, as their comments say). Show that the replay plan orders the migration after every data migration (several INSERT these columns: `grep -l -E "value_min|value_max" scripts/migrations/data_*`), with `python3 -c "import sys;sys.path.insert(0,'scripts');import migrate_db as m;p=m.build_plan();print(p[-1][:2], [s[:2] for s in p if s[0]=='data'][-1])"` (the last step is your schema migration; rule 5).
4. **A rule-version change reads stale (item 33): into T-132, not here.** Append to `workplan/2026-11-12-bidirectional-pipeline/tasks/T-132-drift-detectors-bind.md`, after its last line, this dated line and nothing else:

   > **Amended 2026-11-19 (third adjudication item 33, ratified 2026-11-19; "you have to compute it", owner 2026-09-09 (evening)):** `stale_determinations` in `scripts/assess/assess_cell.py` filters `rule_version = RULE_VERSION`, so a live determination written under an earlier rule reads current. This task also changes it to report such a determination as stale, with `rule_version` among its differing fields, rather than skip it (a cache of a rule no longer in force is not the computation); the Kind line's "no code path" is superseded by this one change. Add a red-then-green case: on a scratch copy, a live determination stamped with an earlier label is reported. The ratchet of item 1 is read after this change.

   Do not change `stale_determinations`' filter in this task.

**What reads what this task adds:** `add-unit` rows: `dbcore.load_units` and every conversion (`to_canonical`, `from_canonical`, the engine's composition, `figure_refusal`), `emit_batch_sql.py`, T-047 (the add-by-data test, adjudication item 31), the research batch that places the units of item 34. The warrant cells: the owner browser, and the next reader who asks why a factor holds. The shared reader: `add-unit` and `_kind_refusal`. Exact bounds: `stale_determinations`, the views selecting `s.*` (`v_best_practice`, `v_divergence`, `v_pending`, `v_code_floor_only`) and render through them. **Without this task**, a unit a source uses cannot enter without hand SQL; a kind can rest on a clause number; and the book states a bound no source stated.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`); for anything added name what reads it and what it replaces (the digit test, `float(...)`).

**Migration discipline.** `python3 scripts/audit/joined_cells_census.py` before and after (keep both; an empty new column proves nothing). Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). No `data_*` file. Then `python3 scripts/generate/context_map.py`, and include `governance/context-map.yaml`.

## 5. Caller sweep

Names to sweep: `base_units`, `load_units`, `_kind_refusal`, `holds no digit`, `quantity_kind_quote`, `add-quantity-kind`, `value_min`, `value_max`, `STORED_ANSWER`, `RULE_VERSION`, `specifications` (views and child tables only).

A caller is a hit whose behaviour or truth changes (code, a test exercising it, a view, index or trigger, a registry entry, a skill or governance sentence stating it); a hit that stays true is a mention. **Fixing a caller is in scope** (rule 4). Left out: `workplan/` except `machines.yaml` and the T-132 line above, the ledger, `scripts/migrations/`, and the frozen records.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
A new verb and new refusal texts: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference.

**Callers found on 2026-11-19** (each in scope; re-run): `scripts/db.py` (`_kind_refusal`, `_KIND_WARRANT`'s help text "they must hold a digit", the parser and dispatch of the new verb); `scripts/dbcore.py` (the comment block above `SHOWN_STEPS` saying units enter "by migration", `canonical_unit`'s NotImplementedError text "add the kind's canonical unit (factor 1) by migration": both now name `add-unit`); `scripts/assess/assess_cell.py` (`_compose_headline`'s return, `STORED_ANSWER`, `RULE_VERSION` and its comment, the docstring at the `value_min` write); tests: `scripts/tests/test_assess_cell_pilot.py` (two positional `INSERT INTO base_units VALUES (…)` fixtures that break when columns are added, and the cases asserting float bounds), `scripts/tests/test_run_pipeline_refusals.py` (the T-020 digit cases and two `base_units` fixtures), `scripts/tests/test_db_amend_writers.py` (T-083 cases passing a kind quote: their quotes must now state a unit of the kind, chosen by query), `scripts/tests/test_db_integrity.py` (K01's version sets, only if the sha payload changes); `schemas/base.py` (`ConditionValue.value_min: Optional[float]`: read it; a mention unless it models a specification row); skills `skills/run-pipeline_SKILL.md` (the quantity-kind sentence; any sentence on units entering by migration); `governance/context-map.yaml` (regenerated); task prose in `workplan/` is not swept, except the T-132 line.

## 6. Verification

**Step 1, before any edit: the before-run.** Checks that read what this task touches: `test_assess_cell_pilot test_run_pipeline_refusals test_db_amend_writers test_db_integrity derivation_handshake_integrity derived_not_curated_audit column_vocabulary_audit schema_reference_audit migration_reproducibility context_map_fresh`.

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137"
CHECKS="test_assess_cell_pilot test_run_pipeline_refusals test_db_amend_writers test_db_integrity derivation_handshake_integrity derived_not_curated_audit column_vocabulary_audit schema_reference_audit migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it. No `EXAMINED:` line, or `EXAMINED: 0`, means it examined nothing: say so (`derivation_handshake_integrity` examines no live determination today).

**Step 2: red before, green after.** Case ids `T137-NN` (`git grep -c '"T137-' -- scripts/tests` printed nothing on 2026-11-19), in `scripts/tests/test_run_pipeline_refusals.py` beside the T-020 and T-030 cases, or in `scripts/tests/test_assess_cell_pilot.py` for the engine cases. Probes by query or built on the test's own scratch copy labelled `TASK-FIXTURE`; never a typed unit spelling, kind id, factor or count the database can derive, except a fixture you build. Show each case red on a seeded defect you then remove (restore byte for byte; `cmp`).

| Case | Red before (or the seeded defect) | Green after |
|---|---|---|
| T137-01 | `add-unit` is not a verb; `base_units` is not in `dbcore.writable_tables` | a fixture unit of a fixture kind is written with its warrant; the table is in the derived capture set and `emit_batch_sql.py` captures the row on a scratch copy |
| T137-02 | seeded: remove each refusal in turn | each refusal of item 1 fires on its probe and writes nothing (row count and table hash unchanged) |
| T137-03 | seeded: compare without exactness (float) | a quote whose second figure differs from the factor by less than any float tolerance is refused; the exact statement passes; a ratio-form statement passes for a ratio unit |
| T137-04 | seeded: drop the warrant CHECK on a scratch rebuild | a raw INSERT of a partial warrant is refused; the seeded rows (no warrant) pass |
| T137-05 | `add-parameter` with a kind quote "Class 1" (a digit, no unit) succeeds | refused, naming the units of the kind (read from `base_units`); a quote stating a figure in a unit of another kind is refused; one in a unit of the kind passes; a kind with no unit is refused naming `add-unit` |
| T137-06 | seeded: let the reader match a unit inside a word | `120 mmHg` is not read as mm (word boundary), `1200 mm` is |
| T137-07 | the engine writes a REAL bound; `typeof(value_max)` is `real` | a determination computed on a scratch copy stores text that round-trips through `Fraction` to the engine's exact value (choose a parameter whose figures give a non-terminating bound by query, or build one) |
| T137-08 | seeded: drop the guard | on a scratch copy holding a non-integral REAL bound the migration aborts; on the canonical copy it converts the stored 5.0 to `5` and `--rebuild` reproduces the database |
| T137-09 | seeded: append nothing to T-132 | `grep -c -F "Amended 2026-11-19 (third adjudication item 33" workplan/2026-11-12-bidirectional-pipeline/tasks/T-132-drift-detectors-bind.md` prints 1, and `stale_determinations` is unchanged (`git diff "$BASE_PRE" -- scripts/assess/assess_cell.py` shows no change inside it beyond the text comparison) |

**Step 3, after the change: the after-run.** The same loop with `after-`; compare check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; a case that asserted a float bound or the digit test is a caller updated to the ruled behaviour, named in the commit body.

**Step 4: the gate, once**, when every edit is made, in the background with a long timeout, waiting with an until-loop on its output file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-137"; BASE_PRE=$(cat "$SCRATCH/base_pre")
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass), any blocking `FAIL`; a FAIL red on the base is not yours (run its `cmd` once on `$BASE_PRE` in a worktree and give both lines).

## 7. Commit

After the gate is clean, staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status`):
```
git commit -m "governance: units enter by data with a warrant, a kind's quote states a value in its unit, and bounds are stored exactly [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, each caller and what was done, the RULE_VERSION label and why>" -m "<the attribution trailers your session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`; do not add a unit row in the migration (units enter through `add-unit` from now on; placing the units of item 34 is research, rule 10).
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`; do not push, open a pull request, subscribe, run `/adversarial` or `/batch-done`.
- Do not type a list of units, kinds, notations, unit words or a float tolerance into code (rule 8); do not build a non-linear conversion (`degrees` is T-059's).
- Do not invent a warrant for the seeded rows, or an exact value for a non-integral stored float.
- Do not change `stale_determinations`' filter (T-132's, by the amendment line), the shown rounding (`SHOWN_STEPS`, OD-22), or `value_notations`.
- Do not add a table, column, flag or verb that section 4 does not name; list any helper you add. Fixing a caller is in scope.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level. The digit test is replaced by a stricter one, not removed.
- Do not hand-type a count into any file or message.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, saw and expected) when:
- a precondition of section 2 is not met, or the gate prints anything but OPEN, or a later ledger entry narrows the ratification;
- an evidence command of section 3 prints otherwise (in particular: a live determination exists, a stored bound is not integral, or a parameter already holds a kind quote that the new test would refuse);
- a flag name of `add-unit` clashes with `dbcore._SECRET_WORDS`;
- a red test is not red before or not green after one honest attempt;
- the sweep finds a caller you cannot repair without adding something section 4 does not name;
- a check green in the before-run is red after, other than a case asserting the digit test or a float bound;
- `migrate_db.py --rebuild` does not reproduce the database, or the replay plan does not order your migration after every data migration;
- you would have to guess a value, a unit's factor, a locator or an owner's intent.

## 10. Rollback

Before merge: the coordinator drops the commit from the stack. After merge: `git revert` in a new pull request. A committed migration is never edited: fix forward with a compensating migration (rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

On this stack the coordinator runs `/adversarial` on your commit and sends any repair; `/batch-done`, the push, the one pull request and the immediate `unsubscribe_pr_activity` are the coordinator's. Report per `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 3, with a heading "Task-file defects".
