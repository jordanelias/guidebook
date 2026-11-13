# T-061  `amend-extraction` reformats a figure's value, unit or empty setting in place (the prior workplan's T-1b step 8)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, OI-52) against `HEAD` after T-016, T-017, T-018 and T-019 merged. The rule of section 4 was prototyped on a scratch copy by monkeypatching `db.amend_extraction` (not committed): it accepted every reformat section 6 expects to pass and refused every one it expects to refuse. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-061 |
| Title | `amend-extraction` reformats a figure's value, unit or empty setting in place (the prior workplan's T-1b step 8) |
| Wave | 1 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | prior workplan T-1b step 8 (`grep -n -F '**T-1b Optional reading steps**' workplan/2026-10-23-pipeline-resolution-workplan.md`); OI-52 in `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`; the owner's OR-3 (`grep -n -F 'OR-3: "Yes, reformat in place"' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-008, T-016 merged (T-008 built `_require_stated_numbers` and `value_as_written`, which this task calls; T-016 built `dbcore.unit_refusal` and `dbcore.figure_refusal`, which it calls). Both were merged on 2026-11-13. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. OR-3 is answered (2026-10-29): `grep -n -F 'OR-3: "Yes, reformat in place"' references/project-standards.md`, and the entry's reading, `grep -n -F 'Reformatting a figure' references/project-standards.md`: "Reformatting a figure's value, unit or empty setting in place, with the same digits and quote and the old text kept in notes, narrows D-0168's \"a wrong claimed_value ... is a SECOND ROW\" for reformatting only". One related question is open, registered as OD-41, and its branch is **not** built here (section 4, "Not built here": the held-out branch rests on OD-41).
- **Tests that must be red (or green) before you start:** the cases of section 6 step 2a marked red are red on the unchanged code.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-061-amend-extraction-reformat "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-061" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

Most governing claims of ramp gradient hold their condition in the unit cell (`% longitudinal gradient (maximum) where the rise is <= 0.6 m …`) or a percent sign in the value (`6%`), so the engine cannot place them on a scale and they are left out of the value. T-016 made the writer refuse those shapes for every new row; the stored rows are history, and the only way to bring one into line without inventing a figure is to reformat it in place, which the owner allowed (OR-3). `amend-extraction` still refuses `claimed_value`, `claimed_unit` and `setting` outright, so the research repair (T-108) has no verb.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it works on the scratch copy, dry run):

```
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py amend-extraction --extraction-id 1 --field claimed_unit --value '%' --reason probe --session session_probe --dry-run 2>&1 | tail -1
python3 -I - <<'PY'
import sqlite3, sys, collections
sys.path.insert(0, 'scripts'); import dbcore
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True); c.row_factory = sqlite3.Row
cls = collections.defaultdict(list)
for r in c.execute("SELECT * FROM source_value_extractions ORDER BY extraction_id"):
    if dbcore.unit_refusal(r['claimed_unit']): cls['unit'].append(r['extraction_id'])
    if dbcore.figure_refusal(r['claimed_value'], r['claimed_unit'], r['comparator'], r['claim_type']): cls['figure'].append(r['extraction_id'])
    if dbcore.comparator_refusal(r['figure_role'], r['claim_type'], r['comparator']): cls['comparator'].append(r['extraction_id'])
for k, v in sorted(cls.items()): print(k, len(v), v)
print('any', len(set().union(*cls.values())))
PY
```

**Expected output today:** the first line is argparse's `argument --field: invalid choice: 'claimed_unit' (choose from …)` (the list does not hold `claimed_unit`, `claimed_value` or `setting`). The census prints three lines, `comparator`, `figure` and `unit`, each with a non-zero count and its ids, and an `any` line: the stored rows T-016's screens would refuse today. On 2026-11-13 the `comparator` line listed 189 and 190 (`comparator` is already amendable), and every id on the `unit` line was also on the `figure` line or was a prose-unit row whose figure reads.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-13; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves the stored prose-unit rows unreadable for good (the only other path, a second row, would hold the same figure twice from one source and quote, which the engine counts twice); the ruling is the rule change; this is the smallest code that applies it, and it reuses T-008's and T-016's screens instead of writing new ones. Locate code by symbol, never by line number.

1. **The fields, in `scripts/db.py`.** Add `"claimed_value"`, `"claimed_unit"` and `"setting"` to `_AMENDABLE_SVE_FIELDS`. Above it, under the comment paragraph that begins `# jurisdiction ADDED 2026-11-13 (T-024)`, add:
   ```python
   # claimed_value, claimed_unit and setting ADDED by T-061 (prior workplan T-1b step 8). Owner, OR-3 (2026-10-29):
   # "Yes, reformat in place" -- a figure's value, unit or EMPTY setting is reformatted in place, with the same
   # numbers and quote, the old text kept in notes (amend_extraction's marker), narrowing D-0168 for reformatting
   # only. `_refuse_unless_reformat` is the whole of what "reformat" means; a different figure is still a second row.
   ```
   The paragraph that opens the comment block says `# Only these two, ever.`: it has been false since 2026-09-18. Replace that first sentence with `# Only these.` and leave the rest of that paragraph as it is.
2. **The rule, in `scripts/db.py`, directly above `def amend_extraction`:**
   ```python
   def _figure_numbers(text):
       """The numbers a figure states, in order, each as its set of readings (`retrieval_log.number_tokens`, the reader
       T-008's number rule uses); a ratio gives its two operands. `1:20` -> [{1}, {20}]; `30,0` -> [{30.0}];
       `30,000` -> [{30000, 30.000}] (a lone group of three after a comma is ambiguous)."""
       out = []
       for kind, readings, _whole in _retrieval_log().number_tokens(text or ""):
           if kind == "ratio":
               out += [{r[0] for r in readings}, {r[1] for r in readings}]
           else:
               out.append(set(readings))
       return out


   def _refuse_unless_reformat(row, field, value):
       """OR-3 (owner 2026-10-29, "Yes, reformat in place"): what a reformat of a stored figure is. Anything else is a
       second row and a contest (D-0168). Called by `amend_extraction` for a changed claimed_value, claimed_unit or
       setting; the old text is kept in notes by its marker.

         setting        only when the row's setting is empty.
         claimed_value  a quantity claim (`dbcore.QUANTITY_CLAIM_TYPES`) only; the new value states the same numbers
                        in the same order, each one of the old number's readings (so `6%` -> `6`, `30,0` -> `30.0`,
                        `0-4.8` -> `0 to 4.8`, `1 in 12` -> `1:12`; never `1:20` -> `1:2.0` or `6` -> `60`); then
                        T-008's number rule against the row's own quote, and the figure must read under the row's unit.
         claimed_unit   `dbcore.unit_refusal`; the new unit stands, on word boundaries, in the old cell (a reformat
                        drops words, it does not name a unit the row did not, so `mm (clear)` -> `m` is refused); then
                        the row's value must read under the new unit.

       KNOWN AND ACCEPTED: a stored value that is ambiguous (`30,000`) cannot be reformatted in place, because T-008's
       rule refuses an ambiguous claimed token and asks for the source's wording, which cannot be set while the stored
       value is ambiguous. Such a row is a second row with --value-as-written. None is stored (section 3's census)."""
       ctx = f"amend-extraction --field {field}: extraction {row['extraction_id']}"
       if field == "setting":
           if (row["setting"] or "").strip():
               raise Refusal(f"{ctx} already states setting {row['setting']!r}. Only an EMPTY setting is filled in "
                             f"place (OR-3); a different applicability is a second row (db.py add-extraction). "
                             f"Nothing was written.")
           return
       if field == "claimed_value":
           if row["claim_type"] not in dbcore.QUANTITY_CLAIM_TYPES:
               raise Refusal(f"{ctx} is a {row['claim_type']!r} claim, not a quantity: a reformat keeps a figure's "
                             f"numbers, and a changed qualitative value is a second row (D-0168). Nothing was written.")
           old, new = _figure_numbers(row["claimed_value"]), _figure_numbers(value)
           if len(old) != len(new) or not all(len(n) == 1 and n <= o for n, o in zip(new, old)):
               raise Refusal(f"{ctx}: {value!r} does not state the same numbers, in the same order, as "
                             f"{row['claimed_value']!r}. A reformat keeps the numbers (OR-3); a different figure is a "
                             f"second row and a contest (D-0168), and a figure the row holds in words is a second row "
                             f"with --value-as-written. Nothing was written.")
           _require_stated_numbers(row["claim_text"] or "", value, row["claim_type"], row["value_as_written"],
                                   "--claimed-value", "amend-extraction")
           figure, unit = value, row["claimed_unit"]
       else:
           why = dbcore.unit_refusal(value)
           if why:
               raise Refusal(f"{ctx}: {why}. Nothing was written.")
           if not _as_whole_words(value, row["claimed_unit"]):
               raise Refusal(f"{ctx}: {value!r} is not, on word boundaries, in the row's unit cell "
                             f"{row['claimed_unit']!r}. A reformat drops words from the cell; naming a unit the row "
                             f"did not is a new reading, a second row (D-0168). Nothing was written.")
           figure, unit = row["claimed_value"], value
       why = dbcore.figure_refusal(figure, unit, row["comparator"], row["claim_type"])
       if why:
           raise Refusal(f"{ctx}: the figure would still not be readable: {why}. When both the value and the unit "
                         f"need reformatting, reformat claimed_value first. Nothing was written.")
   ```
   `_retrieval_log`, `_require_stated_numbers` and `_as_whole_words` already exist in `scripts/db.py` (`grep -n -E 'def (_retrieval_log|_require_stated_numbers|_as_whole_words)\(' scripts/db.py` prints three lines); reuse them, do not copy them.
3. **The call, in `amend_extraction`.** Directly after the `if old == value:` block (the one that ends `return {"extraction_id": extraction_id, "field": field, "changed": False, …}`) and before the comment that begins `# A CHANGE of a column the engine reads`, insert:
   ```python
           if field in ("claimed_value", "claimed_unit", "setting"):
               _refuse_unless_reformat(row, field, value)
   ```
   Chosen (authoring 2026-11-13): after the "already this value" path, so re-confirming a stored setting with a reason is still recorded, not refused; rejected: before it, which would refuse "I checked, and it was already right" for a filled setting. The live-determination refusal that follows already covers `claimed_value` and `claimed_unit`, because both are in `dbcore.ENGINE_EXTRACTION_COLUMNS` (test T061-13 holds that). `setting` is not an engine column and is not refused by it.
4. **The first refusal and the help.** In `amend_extraction`, the refusal for a field not in `_AMENDABLE_SVE_FIELDS` currently says `a wrong claimed_value or claim_text is a SECOND ROW and a contest (D-0168), not an overwrite.` (the sentence spans three adjacent f-string literals; `grep -n -F 'claimed_value or claim_text is a SECOND ROW' scripts/db.py` finds the middle one) Make it say `a wrong claim_text, or a claimed_value with different numbers, is a SECOND ROW and a contest (D-0168), not an overwrite; a reformat with the same numbers is amended here (OR-3).` In the `amend-extraction` parser, the `--field` help says `ONLY these fields. A wrong claimed_value or claim_text is a SECOND ROW and a contest (D-0168), not an overwrite.`: make it `ONLY these fields. claimed_value, claimed_unit and setting take a reformat only (same numbers; a unit already in the cell; an empty setting; OR-3). A different figure is a SECOND ROW and a contest (D-0168).` The docstring of `amend_extraction` gains one sentence: `claimed_value, claimed_unit and setting take only a reformat (OR-3, _refuse_unless_reformat).`
5. **Tests**, in `scripts/tests/test_run_pipeline_refusals.py`: section 6 step 2a.

**Not built here (held on an owner question, OQ-B of this task's hand-back).** Rows whose unit is the bare word `ratio` and whose figure is written `1:20` (`SELECT extraction_id FROM source_value_extractions WHERE claimed_unit='ratio'`) are refused by item 2: `rise:run ratio` names a horizontal run that the cell does not, so it is a new reading under this rule. Whether that change is a reformat is the owner's reading of OR-3, not this task's. If the owner rules it a reformat, the follow-up is one branch in `_refuse_unless_reformat`: accept a new unit that is a member of `dbcore.NOTATION_FAMILIES` when the old unit stands, on word boundaries, in the new one and the stored figure reads under it (`dbcore.figure_refusal` is None). Do not build it here.

**What reads what this task adds or changes:** `db.py amend-extraction` (the CLI and the Python API) reads `_refuse_unless_reformat`; T-108 (research, moves conditions out of the unit cell) is the first caller and cannot run without it; the engine reads the reformatted rows (`assess_cell` through `dbcore.bound_on_scale`). Nothing is replaced or made deletable. No `RULE_VERSION` change: the engine's code does not change, and a reformatted row moves only the `derivation_sha` of a cell determined after it, which re-determination handles.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `_AMENDABLE_SVE_FIELDS`, `amend_extraction`, `amend-extraction`, `SECOND ROW`, `second row`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records); `decisions/` (D-0168's record: marking it is the prior workplan's H-0, which needs an attestation, CLAUDE.md rule 2, and is not this task's).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. This task changes the text of a refusal, so run it. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-13, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `workplan/pipeline-state-graph/machines.yaml`, transition `M04.t2` (`grep -n 'id: M04.t2' -A6 workplan/pipeline-state-graph/machines.yaml`): **a caller.** Its `to:` line lists the amendable fields and ends `value_as_written only)`; its guard says `a changed claimed_value or claim_text is NOT amendable: it is a second row and a contest (D-0168)`. Make the list name every field of `_AMENDABLE_SVE_FIELDS` after your change (it also lacks `jurisdiction`, which T-024 added: the same line, so fix it here and say so), and the guard `a changed claim_text, or a claimed_value with different numbers, is NOT amendable: it is a second row and a contest (D-0168); a reformat is (OR-3)`. Its needle `_AMENDABLE_SVE_FIELDS = frozenset` must still match.
- `skills/run-pipeline_SKILL.md`: **a caller.** It names what `amend-extraction` does for `verified` and `figure_role` and says nothing of a reformat; after the sentence that ends `a `derived` figure that disagrees with its own base + delta (`add-extraction`, `relate-extraction`, `amend-extraction`).`, add one sentence: `A stored figure whose value or unit the writer would now refuse is reformatted in place with `amend-extraction --field claimed_value` (same numbers) and then `--field claimed_unit` (a unit already in the cell), and an empty setting filled with `--field setting` (OR-3); a different figure is a second row.` Then run `python3 scripts/audit/skill_vocabulary_audit.py`: no worse than before.
- `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_db_integrity.py`: call `amend_extraction` or name the verb; run before and after (section 6).
- `scripts/assess/assess_cell.py`, `scripts/audit/extraction_relations_integrity.py`, `scripts/audit/verified_scan_integrity.py`, `scripts/dbcore.py`: name the verb in a message or comment that stays true (mentions).
- `governance/pipeline-contract.yaml` (names the verb as a writer: a mention); `governance/owner-browser.yaml` (OR-3's prompt quotes D-0168: a mention, the prompt is the question that was answered).
- `sqlite_master` and the registry: none for these names.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals` (this task adds cases to it), `test_db_amend_writers`, `test_db_integrity`, `test_scan_contract`, `extraction_relations_integrity`, `verified_scan_integrity`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers test_db_integrity test_scan_contract extraction_relations_integrity verified_scan_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (`verified_scan_integrity` is red on the base while legacy rows stand; on 2026-11-13 `test_run_pipeline_refusals` failed X02 and X03, whose fixture source now holds a decodable text, and on 2026-11-12 `test_scan_contract` failed G01 and G02): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. Also run `python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/before-graph.txt" 2>&1` (section 5).

**Step 2: red before, green after.**

*2a. The tests, written before the change and run on the unchanged code.* Confirm the prefix is free: `grep -c '"T061-' scripts/tests/test_run_pipeline_refusals.py` prints 0. Add one section at the end of `scripts/tests/test_run_pipeline_refusals.py`, directly before the final `finish()` call, headed `print("Section T061: amend-extraction reformats in place (OR-3)")`. Build the fixture with the file's own helpers, inside `with scratch() as c:` (every row is written on that copy; the HAND updates are labelled HAND, as the file's other hand-built states are):

```python
    # T-061 (OR-3): a stored figure is reformatted in place, same numbers and quote, or not at all.
    # The rows are written VALID through the writer, then put into the history shape the writer now
    # refuses by HAND (that shape can no longer be written), then reformatted back through the verb.
    T61 = {"pct":   "The longitudinal gradient is not to exceed 6% where the rise is at most 0.6 m.",
           "ratio": "Every ramp in the survey had a slope of 1:20 over its full length.",
           "comma": "Somente 30,0 % dos predios possuem inclinacao maxima.",
           "range": "The inclination varied between 0 to 4.8 degrees across the trials.",
           "mm":    "The clear width of the passage is to be 1200 mm at least.",
           "qual":  "The surface is to be firm, stable and slip resistant.",
           "words": "A rise of 1:12 is the most that is allowed on a short ramp."}
    ref = new_source(verified=True)
    held_text(ref, "\n".join(T61.values()))
    hand_scan(c, ref, "full")
    P = P_ACTIVE[0]

    def put_row(key, value, unit, cmp_="<=", ctype="numerical", role="claim"):
        return db.insert_extraction(extraction(ref, P, claim_text=T61[key], claimed_value=value,
                                               claimed_unit=unit, comparator=cmp_, claim_type=ctype,
                                               figure_role=role), session=S, dry_run=False,
                                    relations=[])["extraction_id"]

    def row(xid):
        return c.execute("SELECT * FROM source_value_extractions WHERE extraction_id=?", (xid,)).fetchone()
```
Then write the rows (`A = put_row("pct", "6", "%")`, `B = put_row("ratio", "1:20", "rise:run ratio")`, `C = put_row("comma", "30.0", "%", "=", role="finding")`, `D = put_row("range", "0 to 4.8", "degrees", "between", "range", "condition")`, `E = put_row("mm", "1200", "mm", ">=")`, `F = put_row("qual", "firm", None, None, "qualitative", "finding")`, `G = put_row("words", "1:12", "rise:run ratio")`), and put each into its history shape by HAND (`hand("UPDATE source_value_extractions SET claimed_value=?, claimed_unit=? WHERE extraction_id=?", v, u, xid)`): A `6%` / `% longitudinal gradient (maximum) where the rise is at most 0.6 m`; B `1:20` / `rise:run ratio (preferred maximum)`; C `30,0` / `%`; D `0-4.8` / `degrees`; E `1200` / `mm (clear, between handrails)`; F unchanged; G `one in twelve` / `rise:run ratio`. Each sentence is distinct, so no row is a byte-identical copy of another (the writer refuses one, case L03). If a `put_row` call is refused, its message names the missing fixture field: add it to the call (never weaken a refusal), and say so in the pull request. Then one `record(...)` per row of this table; `amend(x, f, v)` stands for `db.amend_extraction(x, f, v, "T061 fixture", session=S, dry_run=False)` through `ok(...)` (accepted) or `refusal(...)` (refused); every refused case also asserts that `row(x)[f]` is unchanged:

| id | call | expect after the change | on unchanged code |
|---|---|---|---|
| T061-01 | `amend(A, "claimed_value", "6")` | accepted; `row(A)["claimed_value"] == "6"`; its `notes` contain `claimed_value SET 6% -> 6` | red (field refused) |
| T061-02 | then `amend(A, "claimed_unit", "%")` | accepted; `dbcore.unit_refusal(row(A)["claimed_unit"])` and `dbcore.figure_refusal(...)` over the row are both None; `notes` keep the old unit text | red |
| T061-03 | `amend(A, "claimed_value", "60")` | refused; text contains `same numbers` | red (the refusal names the field, not the numbers) |
| T061-04 | `amend(B, "claimed_value", "1:2.0")` | refused; `same numbers` (a decimal point moved) | red |
| T061-05 | `amend(E, "claimed_unit", "m")` | refused; text contains `word boundaries` (`m` is not a word of `mm (clear …)`: a rescale) | red |
| T061-06 | `amend(B, "claimed_unit", "ratio")` | refused; text contains `still not be readable` (`ratio` is a word of the cell, but `1:20` does not read under it) | red |
| T061-07 | `amend(B, "claimed_unit", "rise:run ratio")` | accepted; figure reads | red |
| T061-08 | `amend(D, "claimed_value", "0 to 4.8")` | accepted | red |
| T061-09 | `amend(C, "claimed_value", "30.0")` | accepted | red |
| T061-10 | `amend(A, "setting", "new buildings")` | accepted (the setting was empty) | red |
| T061-11 | `amend(A, "setting", "existing buildings")` | refused; `already states setting` | red |
| T061-11b | `amend(A, "setting", "new buildings")` again | accepted with `changed` False (the "already this value" path records the reason) | red |
| T061-12 | `amend(F, "claimed_value", "rough")` | refused; `not a quantity` | red |
| T061-13 | no call: `{"claimed_value", "claimed_unit"} <= set(dbcore.ENGINE_EXTRACTION_COLUMNS) and {"claimed_value", "claimed_unit", "setting"} <= db._AMENDABLE_SVE_FIELDS` | true (the live-determination refusal covers the two engine columns) | red (not amendable) |
| T061-14 | `amend(G, "claimed_value", "1:12")` | refused; `same numbers` (a figure held in words is a second row with `--value-as-written`, T-111's shape) | red |

Run the file on the unchanged code and keep the output: every T061 case red. Make the change and run it again: every T061 case green, and no case of the file that was green before is red.

*2b. The mutations.* Each must be KILLED. Write a harness to `$SCRATCH/t061-mutations.py` (not in the repository): a list of `(name, path, old, new, test)`; for each, read the file, `assert text.count(old) == 1` (if not, lengthen `old` with its neighbouring text), write the edit, run `python3 <test>` from the repository root, print `KILLED` when the exit code is not 0 and `SURVIVED` otherwise, and restore the file in a `finally`. All six use `scripts/db.py` and `scripts/tests/test_run_pipeline_refusals.py`:

| id | old → new | killed by |
|---|---|---|
| M1 | `            _refuse_unless_reformat(row, field, value)` → `            pass` | T061-03, 04, 05, 11, 12 |
| M2 | `all(len(n) == 1 and n <= o for n, o in zip(new, old))` → `True` | T061-03, 04 |
| M3 | `if not _as_whole_words(value, row["claimed_unit"]):` → `if False:` | T061-05 |
| M4 | `        if (row["setting"] or "").strip():` → `        if False:` | T061-11 |
| M5 | `    why = dbcore.figure_refusal(figure, unit, row["comparator"], row["claim_type"])` → `    why = None` | T061-06 |
| M6 | `if row["claim_type"] not in dbcore.QUANTITY_CLAIM_TYPES:` → `if False:` | T061-12 |

*2c. The live rows, by report only (no row is changed).* On `$SCRATCH/t.db`, dry run, the reformats T-108 will make: for every id on section 3's census `unit` or `figure` line, call `db.amend_extraction(<id>, "claimed_value", <the value with a `%` removed, a comma between digits made a point, and `a-b` made `a to b`>, "probe", session="session_probe", dry_run=True)` when that differs from the stored value, then the same for `claimed_unit` with the cell's leading `%` or `rise:run ratio` when the cell starts with one; print each id, field and `ACCEPTED`/`REFUSED` with the refusal's first 80 characters. Expected (prototype, 2026-11-13): every prose-unit row reformats except the one whose value is written in words (extraction 80: T-111 files its numeral as a second row), and every bare-`ratio` row's unit is refused (section 4, "Not built here"). Report the list in the pull request as what T-108 can and cannot do with this verb.

*2d. The rest.* `python3 scripts/audit/extraction_relations_integrity.py`: no worse than before. `build_graph.py --check` after, compared with `$SCRATCH/before-graph.txt` (section 5).

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T061-01`, `T061-02`, …) and confirm the prefix is free first. Never type into a test an id, a code or a count the database can derive: choose every probe by query or build it on the test's own scratch copy, as above. A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason (T061-01 and 07 are those: the fixture rows were written valid first). Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove (the mutations are those).

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added (`test_run_pipeline_refusals` grows by the T061 cases; the others do not change).

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched. Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: amend-extraction reformats value, unit and empty setting in place (OR-3) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it. This task has no migration.
- Do not reformat any stored row: that is research (T-108), rule 10. Section 6 step 2c is a dry run on a copy.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not build the branch section 4 says is held (a unit the cell does not name). Do not make `claim_text` amendable.
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
- `sha256sum data/guidebook.db` changes;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- The code and section 4 disagree about what exists (a symbol it locates is missing, appears twice, or does something other than section 4 says; for example `retrieval_log.number_tokens` no longer returns `(kind, readings, whole)` triples): stop and report; do not reinterpret the plan.
- A mutation of section 6 step 2b survives after one honest attempt to make its case reach the code it targets.
- Section 6 step 2c shows a prose-unit row of T-108's scope refused for a reason this file does not name.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; step 2c's list; what was not verified. End the body with the pull-request attribution line your session instructions give, and a heading "Task-file defects" (REMEDIATION-WORKPLAN section 2 item 5a).
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase).
