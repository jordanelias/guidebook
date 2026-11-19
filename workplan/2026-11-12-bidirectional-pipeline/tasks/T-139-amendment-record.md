# T-139  What a row said before an amendment is held in a typed record, not in a sentence appended to a note

_One task of a stacked pull request (owner instruction 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Authority: the ratified adjudication `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md` (section 4 item 6; section 3 item 55, with items 24 and 54 where they touch it) and `OPEN-ITEMS-PLAN.md` OI-78. Every figure here was read on 2026-11-19, read-only, and is given with the command that produces it: re-run it; do not trust the figure._

**Pilot status.** Not piloted. Authored 2026-11-19 by an Opus-class task author on the owner's instruction "Author the tooling tasks in order". Expect a defect in this file; report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-139 |
| Title | What a row said before an amendment is held in a typed record, not in a sentence appended to a note |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10); one schema migration (a new cross-stage table), one `dbcore` helper, the amending writers, one read verb, two readers |
| Executor | NOT FOR SONNET: Opus-class. The task decides, for each amending verb, which cells are an overwrite to record and which are the verb's own appended content, and writes the coverage rule that keeps a partial register from reading as complete (the defect that dropped the last one, migration 095) |
| Traces to | adjudication 3 item 55 ("one typed amendment record for every `amend-*` verb (row, column, old value, new value, judge, reason, time); the merge's `MERGED` note (OI-78) moves to T-129's merge-row shape"); the owner's schema-shape statement of 2026-11-06 ("we do NOT want to have data joined in cells … or have data stored in the wrong cell"; `grep -n -F "data stored in the wrong cell" references/project-standards.md`); OI-78 (`sed -n 147p workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`); `scripts/migrations/095_drop_amendments_no_reader.sql` (why the first register was dropped, and what would justify one) |

## 2. Preconditions

- **The integration base and set-up: the stacked-branch convention** (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1, or the brief the coordinator names). Stay on the branch you are given; no `git switch -c`; no `/session-open` (the coordinator has run it). Every diff, the gate's `--base` and the code-size line use `$BASE_PRE`.
- **Order (ledger "Owner ratification 2026-11-19", ACTION (2), "in its order").** Sixth of section 4: after T-136, T-137, T-138 and T-135, each a commit on HEAD proven by its own after-test (its section 6). T-138 matters most: it adds to `merge-parameter` the refusal of two differing quantity kinds (item 24), which this task must keep. T-027 and T-059 come after this task.
- **Decisions this task rests on.** Item 55 and OI-78 carry no OD number; item 55 is ratified by reference in the ledger entry "Owner ratification 2026-11-19" (the design questions numbered 12 to 91 "are ratified by reference"; its ACTION (3) keeps the breadth of "all" an [ASSUMPTION] until the owner confirms it). Check the entry, and stop if a later line withdraws its CHECK lines or names item 55:
```
grep -c -F "## Owner ratification 2026-11-19" references/project-standards.md      # printed 1 on 2026-11-19
awk '/^## Owner ratification 2026-11-19/{f=1} f' references/project-standards.md | grep -n -i "withdraw" | head   # printed nothing on 2026-11-19
```
  OD-54 ("into the register, replayed through the writer") is read for the capture rule; by the convention of 2026-11-12 (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-54; do gate $n; done
```
  Printed 2026-11-19: `OD-54 OPEN (delegated; confirmed)`.
- **Tests that must be red before you start:** `T139-01`, `T139-02`, `T139-03`, `T139-05` (section 6).
- **Set-up.**
```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin; BASE_PRE=$(git rev-parse HEAD); echo "BASE_PRE=$BASE_PRE"
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-139" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin each block with the `export SCRATCH=…` line and `BASE_PRE` as recorded. Every probe and fixture passes `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline and `--session session_task-probe`; never delete or edit a `refusals.jsonl`.

## 3. The problem, in the guidebook's terms

When a session corrects a cell (a source's tier or scope, a figure's unit, a term's domain, a population match's grade), the value it replaces survives only as a sentence appended to a note: `|| AMENDED <date> by <session>: domain was: '…'` in `terms.scope_note`, `Replaced text was: …` in `evidence_sources.metadata_integrity_detail`, `|| <date> claimed_unit SET … -> … (reason)` in `source_value_extractions.notes`, `REGRADED A -> B` in `evidence_population_match.mismatch_note`, or a `was`/`now` dict printed by `correct-source` and dropped. `merge-parameter` re-points every row of a folded parameter and appends a `MERGED` line to each one's `notes`, so a moved figure says which parameter its writer named only in prose (OI-78). No gate can see a correction, "what did this batch change" cannot be asked, and a figure or tier the book shows cannot be traced to what it said before. The owner's statement of 2026-11-06 names this shape: "data stored in the wrong cell".

**Why the first register failed, and what this one must do instead** (`sed -n 1,50p scripts/migrations/095_drop_amendments_no_reader.sql`): (1) it had no reader; (2) one writer of at least eight fed it, so it read as complete and was wrong by omission; (3) its writer put the reason in both the table and the prose. This task names its readers (section 4), wires every amending verb at once and states its coverage from the code, and writes no prose trailer beside a row.

**Evidence command** (read-only):
```
grep -c "append_dated_note(" scripts/db.py
grep -n -F -e "Replaced text was" -e "domain was:" -e '"REGRADED"' -e '"MERGED"' -e "SET {old_disp} -> {value}" scripts/db.py | cut -c1-90
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from sqlite_master where name like '%amendment%'\").fetchall(), c.execute(\"select count(*) from base_parameters where status='merged'\").fetchone())"
grep -oE 'add_parser\("(amend-[a-z-]+|correct-source|merge-parameter)"' scripts/db.py | sort -u | tr '\n' ' '
```
**Printed 2026-11-19:** `14`; the trailer lines of `amend_population_match`, `amend_term`, `amend_source`, `merge_parameter` (twice) and `amend_extraction`, plus one line comparing a SLUG's status with `"MERGED"` (a mention: slugs are not parameters); `[] (0,)` (no amendment table; no parameter merge has been run); the nine verbs `amend-extraction amend-gap amend-identity amend-population-match amend-search amend-source amend-term correct-source merge-parameter`. If any differs, stop (section 9).

## 4. The change

Order of preference (CLAUDE.md §8): do nothing; a rule; reuse; delete the cause; the smallest code. Doing nothing leaves the shape the owner ruled against; a rule cannot type a cell; nothing reusable exists (095 dropped the table). So:

1. **One table, `row_amendments`** (schema migration; derive its number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one): `amendment_id INTEGER PRIMARY KEY AUTOINCREMENT`; `table_name`, `row_key`, `column_name`, each `TEXT NOT NULL` with a non-blank CHECK; `value_was` and `value_now` **declared without a type**, so a value keeps its storage class (an INTEGER stays an INTEGER; one value per cell: a single column's single value, never a list); `verb TEXT NOT NULL` (non-blank; no CHECK listing verbs: coverage is derived from the code, item 4); `reason TEXT NOT NULL` (non-blank); `amended_at`, `amended_by_session` `NOT NULL`. A CHECK that `value_was IS NOT value_now`. One index on `(table_name, row_key)`. No foreign key (the amended rows are keyed on TEXT and INTEGER across many tables: 094's own argument, kept). `governance/stage-map.yaml`: `row_amendments: cross-stage` (it records amendments of every stage; adjudication item 70: walkable as an intermediate, counted in no stage). The migration inserts nothing: the existing prose trailers are NOT parsed into rows (095: a regex right most of the time manufactures an authoritative record that is wrong in the rest).
2. **One helper, `dbcore.record_amendment(conn, table, row_key, column, was, now, verb, reason, session, stamp)`.** Refuses (a `Refusal`, naming the defect): a table not in the live schema; a column not in that table; a table whose primary key is not one column (derived by `PRAGMA table_info`; one `row_key` cell must name the row); `was == now` (no change is not an amendment); a blank reason or session. **The judge is the session that ran the verb** (adjudication item 40: "The session stamp is the verifiable part"; no verb takes a `--judge` today, and a required one on nine verbs would be a sweep of every skill that calls them). If you read "judge" in item 55 as a named person or model, stop and ask (section 9): do not add a column on your own reading.
3. **Every amending verb calls it, in the same transaction as its UPDATE, once per changed column, and stops writing the prose trailer for that change** (rule 5: the reason has one home). Located by symbol, never by line:
   - `amend_source`: one row per column it changes (the field; `tier` when re-derived; each column a re-type moves); the `metadata_integrity_detail` segment it appends is no longer written; `metadata_integrity_status` still moves to `CORRECTED` (or stays, for a currency statement), because `metadata_integrity_audit.py` keys on it;
   - `correct_source`: one row per bibliographic field it changes (`was`, `now` from the payload). The author rows it replaces are **excluded, with the reason in the code**: they are rows of `evidence_source_authors` keyed on two columns, replaced wholesale from a logged payload that `--verify-authors` re-reads; the payload is their record;
   - `amend_extraction`: one row for the field; the `notes` marker is no longer appended, and the "already this value" note (a check recorded as a check, not an overwrite) stays as it is;
   - `amend_term`: one row for `definition`, `domain` or `scope_note`; no `AMENDED` trailer; the no-op test keeps reading old trailers so a stored body still compares;
   - `amend_population_match`: one row for `match_grade`; no `REGRADED` line in `mismatch_note` (the table has no `updated_*` columns: the amendment row carries the stamp);
   - `amend_identity`: one row per changed column; the approving ledger heading is its `--approval-ref`, which the verb already checks; it goes into `reason` as `<reason> (approved: <heading>)`. [If T-141 item 75 has given `base_taxonomy_identity` an approval column first, write the heading there instead and keep `reason` the reason alone.]
   - `amend_search` and `amend_gap`: one row per cell a `--set-*` or `--clear-*` flag overwrites; their `--note` text is the verb's own appended content (R15: "the guess left legible beside the correction") and stays as it is;
   - `merge_parameter`, item 5.
4. **Coverage is derived, never listed.** A constant `_AMENDMENT_EXEMPT` in `db.py` maps each function that executes an `UPDATE … SET` on a non-stamp column of an existing row, and does NOT call `record_amendment`, to the reason it is not an amendment (a retirement with its own three columns; a status move with its own stamp columns; a write-once cell; a stamp). Derive its initial content by an AST scan of `scripts/db.py` (and the engine's write path in `scripts/assess/assess_cell.py`); no amending verb of item 3 may be in it. The read verb of item 6 prints the covering verbs, derived by the same scan (the callers of `record_amendment`), so the register never reads as complete for a path it does not cover. This is the burden-of-proof shape `dbcore.writable_tables` uses (CLAUDE.md rule 8).
5. **`merge-parameter` (OI-78; adjudication items 24 and 55).** Reading, recorded so the reviewer can contest it: OI-78's own resolution column allows "a recorded decision that it keeps the re-point, with the reason", and T-129-design A7 places the change of shape "when T-059's gather is rewritten". This task therefore: (a) **keeps the re-point until T-059**, with the reason in the docstring: the engine gathers figures by `parameter_id` (`grep -n 'def gather_sources' scripts/assess/assess_cell.py`) and the views that answer about a parameter (`select name from sqlite_master where type='view' and sql like '%parameter_id%'`) read it too; a merge row without them would split a parameter's figures with nothing red; (b) **records every moved row** as one `row_amendments` row (`column_name` the foreign-key column, `value_was` the folded id, `value_now` the survivor, `verb` `merge-parameter`, the merge's reason), and the folded parameter's own `status` and `merged_into` the same way: the folded row with `status = 'merged'` and `merged_into` IS the merge record (one home; no `parameter_merges` table is added); (c) **writes no `MERGED` line** into any `notes`; (d) **keeps every refusal** it has, including T-138's differing-kinds refusal, except the refusal "the table has no notes column to record the move on", whose reason is gone (the move is recorded for any table): say so in the commit, with the case that shows the move recorded on such a table.
   **Plan edit (no code), made by you in this pull request:** append to `workplan/2026-11-12-bidirectional-pipeline/tasks/T-059-wp-t4-agreement.md` a dated line: "**Amended 2026-<date> (T-139; adjudication 3 item 55, OI-78):** when this task rewrites the gather, it also gives the parameter merge T-129's shape: no re-point, a survivor derived from `base_parameters.merged_into` (one view), the gather and every reader that answers about a parameter reading the survivor's class; `row_amendments` keeps the history of any re-point made before. Until then `merge-parameter` re-points and records each move in `row_amendments`."
6. **The readers this task adds (CLAUDE.md §8: nothing without naming what reads it).**
   - `db.py amendments [--table T] [--row-key K] [--session S]`: read-only, newest first, one line per row; its first line names the covering verbs (item 4). Read by the adversarial pass (`/adversarial`, "what did this batch change") and by any session asking what a cell said before.
   - `scripts/audit/metadata_integrity_audit.py`: where it prints a source's `metadata_integrity_detail`, it also prints the source's latest `row_amendments` reason, so an amendment made after this task (which no longer writes the detail) is still shown.
   - `scripts/research/emit_batch_sql.py` captures the table by derivation (`dbcore.writable_tables`), so an amendment replays (OD-54).
7. **What wrong thing reaches the guidebook without it:** a corrected tier, scope, unit, grade or domain whose prior value and reason live in prose no gate reads, so a figure, a marker or a term the book shows cannot be traced to what it was before or who changed it; and a merged parameter's figures that say which parameter their writer named only in a note. **Code it makes deletable:** five trailer-composing branches and the merge's notes-column refusal.
8. **Item 54 (no change here):** a notation-family member added later is a warranted data act (T-030), so its widening of the reformat is warranted; this task only records each reformat as a typed row.

**Schema migration.** As T-050 section 4 states it: `joined_cells_census.py` before and after (no new candidate; it examines no column of an empty table, so also run it on a scratch copy after a fixture amendment); apply only with `python3 scripts/migrate_db.py`; `migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` exit 0; `migration_reproducibility.py --deep` PASS; regenerate `governance/context-map.yaml`. No `scripts/migrations/data_*` file.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), naming what reads each addition and what it replaces.

## 5. Caller sweep

Names to sweep: `append_dated_note`, `Replaced text was`, `domain was:`, `REGRADED`, `MERGED`, `_TERM_TRAILER`, `metadata_integrity_detail`, `mismatch_note`, `_MERGE_KEEPS_HISTORY`, `merge-parameter`, `row_amendments`.

**What a caller is**, and what the sweep leaves out: as T-050 section 5 states them (code, tests, views, registry, skills, `.claude/`, governance prose and `machines.yaml` needles are swept; `workplan/` other than `machines.yaml`, the ledger, committed migrations and frozen records are not).

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after (a new verb and table); only a failure line your change adds is yours.

**Callers known on 2026-11-19:** `scripts/db.py` (the nine verbs; the `amend-source` help string that says the detail keeps "the replaced text": `grep -n "metadata_integrity_detail with the replaced text" scripts/db.py`; `amend-extraction`'s `--reason` help that says it is appended to notes); `scripts/dbcore.py` (`append_dated_note`, which stays for the non-amending verbs: `resolve-candidate`, `link-admission`, `retire-parameter`, `annotate-parameter`, `supersede-source`, the code-lead verbs); `scripts/audit/metadata_integrity_audit.py`; the tests that assert a trailer (`git grep -l -E "REGRADED|Replaced text was|MERGED|domain was|SET .* -> " -- scripts/tests` printed `test_db_amend_writers.py`, `test_db_integrity.py`, `test_run_pipeline_refusals.py`, `test_scan_contract.py`): each assertion of a trailer is rewritten to assert the amendment row, and each rewrite is listed in the pull request; `workplan/pipeline-state-graph/machines.yaml` (a needle on a trailer string, if any: `grep -n -E "REGRADED|MERGED|Replaced text" workplan/pipeline-state-graph/machines.yaml`); `skills/evidence-metadata-rehabilitation_SKILL.md` writes `metadata_integrity_detail` for verification (a different writer: a mention unless it states amend-source's segment).

## 6. Verification

**Step 1, the before-run, before any edit:** `test_db_amend_writers test_run_pipeline_refusals test_db_integrity test_scan_contract metadata_integrity_audit emit_batch_sql_selftest derived_not_curated_audit schema_reference_audit migration_reproducibility context_map_fresh`, each run as the registry runs it (the loop of T-050 section 6 step 1), output kept in `$SCRATCH/before-<id>.txt`. A check red here was red before you: record it. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2, red before and green after.** A new file `scripts/tests/test_row_amendments.py`, registered `test_row_amendments` (`battery: tests`, `kinds: [tooling, data]`, `level: advisory`, `basis: hygiene`, a `no_floor:` that says its subject is its own fixtures). Confirm the prefix is free (`git grep -c '"T139-' -- scripts/tests` prints nothing; it printed nothing on 2026-11-19). Every case runs on a scratch copy built inside the test (`TASK-FIXTURE`), every probe row chosen by query, never typed. Each case is shown red on the unchanged code or on the named seeded defect, which you then remove (`cmp` the file against its saved copy):

- `T139-01` the helper: one legitimate row written; each refusal of item 2 by its own sub-case (unknown table, unknown column, a two-column-key table derived by query, `was == now`, blank reason). Red before (no helper). Seeded defect per refusal: delete its line.
- `T139-02` the verbs, one sub-case each for `amend-extraction`, `amend-gap --set-…`, `amend-identity`, `amend-population-match`, `amend-search --set-…`, `amend-source`, `amend-term`, `correct-source` (a source with a logged payload, chosen by query; `SKIPPED-NO-FIXTURE` if none, said in the pull request): after the call, exactly one `row_amendments` row per changed column with the right `was`, `now`, `verb`, `reason` and session, and the trailer column's text unchanged. Seeded defect: remove the helper call from one verb, and its sub-case goes red.
- `T139-03` coverage: on a temporary copy of `scripts/db.py`, a new function with an `UPDATE … SET` of a non-stamp column, neither calling the helper nor exempted, makes the scan fail naming it; an exemption with a blank reason fails; an amending verb of item 3 placed in `_AMENDMENT_EXEMPT` fails. Red before (no scan).
- `T139-04` the merge: two fixture parameters built on the copy (of one quantity kind, so T-138's refusal does not fire; a sub-case shows that refusal still fires for two kinds): every moved row gets one amendment row (`value_was` the folded id, `value_now` the survivor), the folded parameter's `status` and `merged_into` get theirs, and no `notes` cell of any moved row changes. A moved row in a table with no `notes` column is recorded (the refusal is gone, the trace is not). Seeded defect: restore the `MERGED` append, and the `notes` assertion goes red.
- `T139-05` the read verb: `db.py amendments --table T --row-key K` lists the rows of T-139-02's fixture newest first, and its first line names exactly the verbs the scan derives. Red before (no verb).
- `T139-06` the audit: `metadata_integrity_audit.py` run against the copy after an `amend-source` prints that amendment's reason for the source. Seeded defect: remove the added read.
- `T139-07` capture and replay: `emit_batch_sql.py --scratch` on the copy after one amendment emits an INSERT into `row_amendments`, and replaying it onto a fresh copy of the base yields the same row.
- `T139-08` storage class: an INTEGER `value_was` and a REAL `value_now` keep `typeof()` `integer` and `real`; a seeded defect that declares the columns `TEXT` turns both to `text`.

Also on the copy, after a fixture amendment: `joined_cells_census.py` (the new table adds no candidate) and `derived_not_curated_audit.py` (no new finding; `_AMENDMENT_EXEMPT` is an exclusion with reasons, not a curated vocabulary: if the audit flags it, report it, do not silence it).

**Step 3, the after-run:** the same loop with `after-`; compare failure lines check by check; no failing case may appear that was not failing before.

**Step 4, the gate, once**, in the background with a long timeout, waiting on its output file:
```
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass: say so) and any blocking `FAIL`. `research_tooling_separation`: run it once by hand with `--base "$BASE_PRE"`.

## 7. Commit

After the gate is clean: `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status` shows only your files), then `git commit -m "governance: what a row said before an amendment is held in a typed record [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the change, the evidence before and after, each caller and what was done to it, the merge reading of section 4 item 5>" -m "<the two trailer lines your session instructions give>"`.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly; only `scripts/migrate_db.py` changes it. Do not run `run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not parse any existing prose trailer into a row, and do not delete or rewrite an existing trailer.
- Do not add a `--judge` flag, a verb CHECK, a `parameter_merges` table, a survivor view, or a change to the engine's gather (T-059's, by the plan edit of item 5).
- Do not put the reason in both the record and a note. Do not weaken any refusal of `merge-parameter` other than the one item 5 (d) names, and do not drop T-138's.
- Do not hand-type a count, an id or a code into a file, a test or a message; write the command. No research rows (rule 10). Do not push, open a pull request, or subscribe to anything.
- Do not decide doctrine; do not author a specification row.

## 9. Stop conditions

Stop, change nothing further, and report what you ran, saw and expected, when:
- a precondition of section 2 is not met, or the ratification entry is withdrawn as to item 55;
- the evidence command of section 3 prints otherwise;
- a red test is not red before or not green after, after one honest attempt;
- a caller cannot be repaired without adding what section 4 does not name;
- a check green in the before-run is red after;
- an amending verb changes a table whose key is two columns (other than `correct-source`'s author rows): the record cannot name the row in one cell, and the shape is a decision;
- you read "judge" in item 55 as something other than the session (item 2);
- the scan of item 4 finds an overwrite path you cannot classify as an amendment or an exemption with a reason.

## 10. Rollback

Before merge: drop the commit from the stack on the coordinator's instruction; nothing else changed. After merge: `git revert` in a new pull request. A committed migration is never edited: fix forward (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass

On a stacked batch the coordinator runs the adversarial pass on your commit and any repair; do not run `/adversarial` or `/batch-done`, push, or open a pull request yourself. The critic should attack, at least: a verb whose overwrite writes no row (run each verb, not the scan alone); a reason written twice; a row whose `row_key` does not resolve to the amended row; and the merge reading of section 4 item 5.
