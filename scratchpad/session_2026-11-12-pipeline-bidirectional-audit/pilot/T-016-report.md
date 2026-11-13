# T-016 pilot report (stage P2, stacked on the T-008 re-pilot)

Pilot, not a real execution: no `/session-open`, no `scratchpad/CURRENT`, no push, no pull request. Executor: Sonnet-class.

## Result

PILOTED, with defects. A green result was reached (red before, green after, gate PASS), but only after working around or interpreting nine defects in the file; the test plan (test file, ids, N11, M1, M5, M6) could not be followed as written.

- **Base commit.** `b331dc6` (`origin/claude/peaceful-noether-kvf3sf`), plus the T-008 re-pilot commit `0cab9ac` (stack).
- **My commit.** `76c323b`, patch at `$OUT/T-016.patch` (made with `git format-patch -1 --binary --stdout`, my commit only; checked: it applies with `git am` on a fresh clone of the stack).
- **Canonical database.** sha256 `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` before and after (equal). The task has no migration.
- **BASE override.** I did not run the file's BASE line (twice: set-up block and section 6 step 4); I used `BASE=origin/claude/peaceful-noether-kvf3sf` as the brief says, because the file's line names a branch (`ccr-408aaa9b-z3e4s0`) that is not the tip.

### The stack

- `git am "$OUT/T-008-repilot.patch"` WORKED on the first try. The `--binary`-less stub fallback was not needed. The patch's database hunk applied as a real blob: `PRAGMA user_version` was already 126 and `source_value_extractions.value_as_written` existed.
- `python3 scripts/migrate_db.py` ran anyway: `Schema at version 126; 0 data migration(s) applied.` `git status` stayed clean afterwards.
- **T-016's evidence command is unchanged by the stack.** `grep -rn 'def parse_bound' scripts` printed `scripts/assess/assess_cell.py:624:def parse_bound(...)`; the `sed` printed the T-1a paragraph with its done-when, as section 3 says.
- The stack matters for T-016 in three places, all real: `dbcore.QUANTITY_CLAIM_TYPES` (used, not retyped), `db._require_claimed_number` (runs BEFORE the new refusals, so the "no digit" branch of `figure_refusal` is reachable only with `--verbatim-exempt`), and `value_as_written` (used by test N8).

## The five things the brief asks

1. **Followed only CLAUDE.md and the task file?** No, and it could not be done. Section 4 item 1 says "Execute T-1a as written in `workplan/2026-10-23-pipeline-resolution-workplan.md` and the report section it cites (`scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`, T-1 steps 1 to 7)". The steps, the code sketches, the tests N1 to N11 and the mutations M1 to M5 exist only in that 160 kB report. I read the report's T-1 section, its common protocol (P-1 to P-10) and its §6.2 harness. I did not read other task files, the audit folders or the ledger.
2. **Evidence command printed what the file says?** Yes (see above). The stack did not change it.
3. **Red before, green after?** Yes. `T016-N1` to `N6`, `N9`, all red on the unchanged code; the controls green on both; `build_graph.py --check` 109 failures before and after (identical output).
4. **Gate ran once, every named check's `EXAMINED:` read?** Yes. Table below. Two named checks print no `EXAMINED:` line.
5. **Patch and report saved?** Yes.

## Check-by-check, before and after

Each check was run as the registry runs it (`cmd` read from `governance/check-registry.yaml`), on the stack before my edits and after them.

| Check | Before | After | Note |
|---|---|---|---|
| `test_assess_cell_pilot` | rc=0, no `EXAMINED:` line; 145 `PASS:` lines | rc=0, no `EXAMINED:` line; 151 `PASS:` lines | the file says each check shows `EXAMINED:`; this one never prints it. +6 cases are mine (`dbcore.bound_on_scale` table). Examined something (PASS lines), not by its own count |
| `extraction_relations_integrity` | `EXAMINED: 271`, `VERDICT: CLEAN` | `EXAMINED: 271`, `VERDICT: CLEAN` | 0 `v_derived_figure_check` rows: the view examines nothing in the live data, so this check cannot go red on my derived-arithmetic change; the tests do that |
| `test_run_pipeline_refusals` | `EXAMINED: 215 cases`, pass | `EXAMINED: 233 cases`, pass | +18 cases, all `T016-*` |
| `test_scan_contract` | `EXAMINED: 119`, 117/119, G01 and G02 red | identical | baseline-red (G01, G02), not mine; the failing-line diff is empty |
| `test_db_amend_writers` | `EXAMINED: 161`, 161/161 | identical | no case added here (see defect 4) |
| `test_author_presence` | rc=0, `EXAMINED 3` etc. per case | identical | |
| `test_search_log_completeness` | `EXAMINED: 23`, 23/23 | identical | |
| `test_validate_evidence_state_2_4` | rc=0, no `EXAMINED:` line; 12 `[PASS]` | identical | prints `ALL PASS (0 failed)` only |
| `claude_md_spine` | `EXAMINED: 7` | identical | |
| `research_contract_sync` | `EXAMINED: 79` | identical | |

In every row the failing-line diff (`diff <(grep ... before) <(grep ... after)`) is empty.

### Other done-when lines

- `grep -rn "def parse_bound" scripts`: empty after (one line before).
- `fixtures_g1_g13.py` (extracted from the report, run with `python3 -I`): 13 lines, **byte-identical** before and after (`cmp`).
- `notation_probe.py` (its import changed to `from dbcore import bound_on_scale`, as its own comment says): identical output before and after (`1:12` gives 8.3333, `12:1` gives 1200.0, `1/12` gives 0.0833, `8.33%` gives None: the engine still reads them as before; the writer now refuses them).
- `build_graph.py --check`: 109 failures before, 109 after, `diff` of the two outputs empty. The file's "pilots counted 109" is exact.
- Mutations (own harness, `(name, path, old, new, case)`, each edit applied once to the tree, `test_run_pipeline_refusals.py` run, file restored; 7 mutations, about 40 s each):

| Mutation | Result |
|---|---|
| M1 `unit_refusal`: `VALUE_BEARING.search(u)` replaced by `False` | KILLED by `T016-N4b` (NOT by N4: see defect 6) |
| M2 comparator refusal condition replaced by `False` | KILLED by `T016-N6` |
| M3 `figure_refusal` returns `None` at once | KILLED by `T016-N1`, `N2`, `N3`, `N5` |
| M4 derived tolerance `> 1e-9` to `> 1e9` | KILLED by `T016-N9` and `T016-N11` |
| M5' slash-ratio screen off (replaces the file's M5, which targets the numeral gloss) | KILLED by `T016-N2` |
| M6' inverted-ratio screen off | KILLED by `T016-N3` |
| M7' `relate_extraction` derived check off | KILLED by `T016-N11b` |

The file's acceptance asks for "KILLED six times"; with the gloss (M5) and OR-3 (M6) out of scope, the achievable count from the file's own list is four; I made three more.

## What I changed (section 4 steps 1 to 5, 7; step 6 skipped as ordered; 8 to 10 not done, gated on OR-3, OR-10, OR-11a)

- `scripts/dbcore.py`: the notation block moved in (from `NOTATION_FAMILIES` to `bound_on_scale`), `from fractions import Fraction` added, `bound_on_scale`'s docstring rewritten to carry what `parse_bound`'s said; `VALUE_BEARING`, `unit_refusal`, `figure_refusal` added.
- `scripts/assess/assess_cell.py`: block and `parse_bound` deleted, names imported back from `dbcore`; the now-unused `from fractions import Fraction` and its comment removed; one comment names `dbcore.bound_on_scale`.
- `scripts/db.py`: `_VALUE_BEARING = dbcore.VALUE_BEARING`; the unit/figure/comparator refusals after the `_SVE_VOCAB_COLUMNS` loop; `_refuse_derived_mismatch` called in `insert_extraction` (after the edge loop) and in `relate_extraction`; the duplicate comparison in `derive_extraction` deleted (the string "extract the base figure first with add-extraction" kept; `machines.yaml:230` still matches).
- Callers fixed: `scripts/tests/test_assess_cell_pilot.py` (patches `dbcore.NOTATION_FAMILIES`; +6 cases), `scripts/tests/test_run_pipeline_refusals.py` (`extraction()` fixture gains `comparator: "="`; new Section T016, 18 cases), `scripts/audit/extraction_relations_integrity.py` (a comment quoting the deleted arithmetic), `skills/run-pipeline_SKILL.md` (the sentence listing what the writer refuses).
- No registry change, no migration, no new verb, table or check. `governance/context-map.yaml` not regenerated (no schema change).

### Code size

`git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`): **8 files changed, 620 insertions, 239 deletions**. That figure includes the T-008 stack (the branch left `$BASE` before T-008's commit). Mine alone (`git diff --cached --shortstat HEAD -- ...`): **7 files changed, 364 insertions, 201 deletions**; without `scripts/tests`: **5 files, 252 insertions, 199 deletions**, net **+53**, inside the file's "+45..95". What reads the additions: `insert_extraction` (via `add-extraction`), `relate_extraction`, `derive_extraction`, the engine (re-imported names). Deleted: `parse_bound` (about 50 lines), the duplicate arithmetic in `derive_extraction`, the engine-local copy of the notation block (moved, not duplicated).

## Sweep

Names swept as the file lists them (`parse_bound`, `NOTATION_FAMILIES`, `derive_extraction`, `numeral-gloss`), with the four commands per name (tree, `sqlite_master`, registry, prose):

- `parse_bound`: three comment/docstring mentions in `assess_cell.py` (two went with the block, one reworded), the `def`. `sqlite_master`: `[]`. Registry: `[]`. Prose: none.
- `NOTATION_FAMILIES`: `assess_cell.py` (now an import) and `test_assess_cell_pilot.py` (a caller: patches the dict; repointed to `dbcore`). `[]`, `[]`, none.
- `derive_extraction`: `db.py` (def and dispatch), the comment in `extraction_relations_integrity.py` (a caller by truth: it quotes the deleted `abs(cn - (bn + dn)) > 1e-9`; reworded), `machines.yaml:230` (needle kept, a mention). `[]`, `[]`.
- `numeral-gloss`: no hit anywhere (as expected).

**Names the file's sweep list misses, which I swept as well** (these found the real callers): `insert_extraction` / `add-extraction` (found `test_run_pipeline_refusals.py`'s `extraction()` fixture, `skills/run-pipeline_SKILL.md` line 183-ish, `test_scan_contract.py`'s `claim()` which already passes a comparator), `bound_on_scale`, `to_canonical`, `from_canonical`, `notation_family`, `_VALUE_BEARING` (importers: `scripts/audit/medical_lens_integrity.py`, `scripts/tests/test_scan_contract.py`; alias keeps them working), `v_derived_figure_check`. `sqlite_master` for `v_derived_figure_check` and `derive_extraction`: the view's own definition only.

`build_graph.py --check`: 109 failures before and after, outputs identical (no verb, table or refusal-text name was removed; the text of refusals changed only by addition).

## Gate (once, before the commit)

`scripts/preflight.sh --base origin/claude/peaceful-noether-kvf3sf --explain`, background, about 2 minutes:

- `SELFTEST: PASS`. `RESULT: PASS — 60 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)`. `PREFLIGHT: PASS`.
- **NOTHING-IN-SCOPE (4):** `extraction_follow_up_audit`, `citation_mining_session`, `adversarial_pass_recorded`, `medical_lens_integrity`. None reads what this task changes; stated, not passed. (`adversarial_pass_recorded` and `citation_mining_session` are session-scoped and a pilot has no session.)
- **Blocking FAIL:** none.
- **The 11 advisory failures**: `test_scan_contract`, `validate_schema_cross_check`, `research_dod`, `retired_vocabulary`, `skill_vocabulary_audit` are in the R2 baseline (`skill_vocabulary_audit` reports 76 tokens in 18 files, the same as the baseline; the line naming `skills/run-pipeline_SKILL.md: CO1-NOT-APPLICABLE` pre-exists). **Six more are not in the R2 baseline file but are red on the unchanged stack too**: I re-ran `scan_debt`, `verified_scan_integrity`, `search_log_completeness`, `research_protocol_audit`, `metadata_integrity_audit` with my changes stashed and the output was byte-identical (`verified_scan_integrity`: 140 pairs across 212 rows; `metadata_integrity_audit`: 20 rows). `search_log_completeness` fails in the gate (4 WebSearch ledger lines, scoped to this working session by the hook) and passes standalone with `EXAMINED: 0`; it is a pilot artefact. The baseline file is incomplete (finding for the brief, not the task file).
- **`research_tooling_separation`** FAILs in the gate (it reads `origin/main`). By hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` printed `EXAMINED: 12`, `VERDICT: PASS`. Not mine. The path list it printed includes T-008's `retrieval_log.py`, i.e. the stack.
- Canonical database sha unchanged.

## Task-file defects

Ordered worst first. "Cost" is my estimate.

1. **The file is not self-contained and its own conflicting protocol comes with it** (cost: about 30 minutes of reading, the largest single item). Section 4 item 1 delegates the whole change to a 160 kB report plus a 2026-10-23 workplan; the file says "beyond it this file is self-contained". The delegated report carries a different branch/CURRENT/commit/attribution protocol (P-1 to P-10: `git switch -c claude/<slug> origin/main`, `scratchpad/CURRENT`, Opus attribution, `unsubscribe_pr_activity`, the old `--changed-from origin/main` gate) which contradicts section 2, 6 and 7 of this file; an executor has to know to ignore P-1 to P-10 and use only the T-1 steps. A corrected file would inline steps 1 to 5 and 7 (with the fixes below), or say "ignore the report's section 3.0".

2. **`derive-extraction` cannot succeed, so test N11 and the "control" for N10 cannot be run as the report writes them** (cost: about 20 minutes to find, then a test shim). Command: `db.derive_extraction(ref_id=..., parameter_id=..., base=..., delta=..., claim_text=..., claimed_value='14.75', comparator='=', ...)` on a fixture with a quotable derived sentence. Observed: `R3: this row states a value with no locator -- no --source-section, none of --loc-division ...`; the verb passes no `source_section` or `loc_*` and has no flag for them, so every numerical derived row it builds is refused at the R3 locator gate (every tier since 2026-11-06) before the new arithmetic check is reached. Also a derived row's `claim_text` must be a byte-quote that contains the derived number (`_require_verbatim` then `_require_claimed_number`), which an "analyst's computation statement" cannot be. So the file's N11 ("`derive_extraction` with a mismatched `--claimed-value` still refused, now by the shared check") is true only by the R3 refusal. My test wraps `db.insert_extraction` with a locator for that one block (`SHIM`) so the shared check is what fires. This is a pre-existing defect of the verb (not mine, not in section 4 to fix); the file should say N11 needs the shim or be dropped, and the owner should know the verb is dead. Adding `--source-section` to it would be "a flag section 4 does not name".

3. **The sketch in section 3 of the report (`figure_refusal`) raises on a range** (cost: 5 minutes, found by running it on the probe's `1:6 to 1:14`). `rise, run = (Fraction(x) for x in v.split(":", 1))` with `v = '1:6 to 1:14'` is `Fraction('6 to 1')`, a `ValueError`. The file's claim that the sketch "was run on the N1 to N8 inputs and the controls" did not include a range. I split the value on ` to ` and tested each part. Also the sketch's last no-digit message still names `--numeral-gloss` (the file says so in item 3).

4. **The test location is wrong for the fixtures it needs, and the ids collide** (cost: 20 minutes). The report puts "Section N (notation, T-1)" cases in `scripts/tests/test_db_amend_writers.py`. That file already has ids `N01` to `N05` (a log-search section) and no helper that makes a VERIFIED source with a covering reading and a quote that is in the retrieval-log bytes; `run_cli`/`q` exist there, `new_source`/`held_text`/`hand_scan`/`extraction()` exist in `test_run_pipeline_refusals.py`, which is where T-008 put its cases. I wrote Section T016 in `test_run_pipeline_refusals.py`. Section 6's "prefix `T016-` and confirm free" is the right instruction; the report's table (N1 to N12, in `test_db_amend_writers.py`) contradicts it. The file should name the test file and the fixtures.

5. **"Every live numerical claim already carries a comparator (C23), so no existing writer route breaks" is false, and the sweep did not find the route it breaks** (cost: 10 minutes). Command from the report: `SELECT COUNT(*) FROM source_value_extractions WHERE figure_role='claim' AND claim_type='numerical' AND comparator IS NULL` now prints 2 (with `figure_role IN ('claim','derived')`: 2), not 0. More important: the existing test fixture `extraction()` in `test_run_pipeline_refusals.py` writes `claim_type=numerical`, `figure_role=claim` with no comparator, so after step 5 five cases went red (`V04`, `X02`, `L02`, `L03`, `T008-36`) and the run crashed with an uncaught `Refusal` at `T008-37`. The file's sweep names (`parse_bound`, `NOTATION_FAMILIES`, `derive_extraction`, `numeral-gloss`) cannot find this; the sweep needs `insert_extraction` / `add-extraction` (and `derive-extraction`, which now also needs `--comparator`, an optional flag today).

6. **Mutation M1 and the acceptance "KILLED six times" cannot be met as written** (cost: 15 minutes). M1 ("`if VALUE_BEARING.search(unit)` to `if False`" turns N4 red): N4's unit also contains `where`, so the second screen condition refuses it and M1 SURVIVES. I added cases that exercise each condition alone (`'rise:run ratio max'`, `'rise:run ratio unless steep'`, `'ratio (new build)'`); then M1 is KILLED by `T016-N4b`. M5 (the numeral-gloss refusal) and M6 (OR-3's digit identity) target steps the file itself removes or does not execute, so only M1 to M4 exist; "six" in the acceptance cannot be reached.

7. **Test N8 as restated needs the quote of a row that cannot be reused as written** (cost: 10 minutes). Row 80's `claimed_unit` is a prose sentence (the Finnish "spelled-out cardinal" note) and its `claimed_value` is `'viisi prosenttia'`; its quote is not in the fixture's retrieval log, so the case needs `held_text(ref, quote)` on a fixture source. I derived the row by query (a quantity-type claim whose `claimed_value` has no digit, first by id) and wrote the quote into a fixture text. The case is also a duplicate of T-008's own `T008-36`/`T008-37`; the file does not say so. Say: reuse T-008's, or state the fixture.

8. **Counts in the file moved** (cost: 5 minutes of checking, no harm). Step 4: "27 of the 33 distinct `claimed_unit` values (33 of 101 rows)": now 27 of **38** distinct, 33 of **214** rows (the refused-unit count 27 and row count 33 still match; the totals do not). Step 4: "`grep -n "_VALUE_BEARING" scripts/db.py` lists its five uses": 8 lines, 15 occurrences, plus two importers (`scripts/audit/medical_lens_integrity.py`, `scripts/tests/test_scan_contract.py`). Report step 7 and the file's section 6: `test_scan_contract` "failed two cases" is right. Section 6 step 1: "Each line shows the check's subject (`EXAMINED:`)" is wrong for `test_assess_cell_pilot` and `test_validate_evidence_state_2_4`, which never print one.

9. **Smaller instruction defects.**
   - Report step 1 says paste the block "after `ENGINE_EXTRACTION_COLUMNS`"; T-008 put `QUANTITY_CLAIM_TYPES` after it and `figure_refusal` uses that constant, so the block must go after `QUANTITY_CLAIM_TYPES`. Step 1 also says nothing about the moved `bound_on_scale` docstring (it references the deleted `parse_bound` and says it "is left exactly as it was"; it had to be rewritten) or about the `from fractions import Fraction` import and its comment, which become unused in `assess_cell.py`.
   - The step 7 snippet (`bad["recomputed"]`) needs `conn.row_factory = sqlite3.Row`, which `dbcore.connect` sets; fine. But the new shared check narrows behaviour for unit-converted derived rows: the old `derive_extraction` comparison ran on raw numbers whatever the units, the view joins on equal units and plain numerals only, so a converted-unit mismatch is no longer refused (the integrity check reports such rows as UNCHECKED). The file does not say so.
   - Step 2 (compare against T-014's stress harness "before and after") names a task file I may not read and which is not defined here; I used the report's own §6.2 pieces I could extract (`fixtures_g1_g13.py`, `notation_probe.py`; the `regress_2026-10-22.sh` stages 1, 2, 5, 6, 7 not run, `render_attempt.py` is not in the repository). The expected-difference ("`guards.unit-in-prose` now refused") has no matching step in anything I could run.
   - Section 6 step 4: the code-size and gate instructions use the merge-base with `$BASE`, which in a stack includes the predecessor (620/239 against my 364/201). A stacked file should say to diff against the predecessor commit.
   - `figure_refusal`'s `--value-as-written` branch is unreachable for anything but `--verbatim-exempt` rows, because T-008's `_require_claimed_number` refuses a value without a number first; the file should say which path the test uses to reach it (I saw its message only in a shell probe of `dbcore.figure_refusal`, and no `T016-*` case reaches it).

## Stop conditions

None of section 9 fired as a hard stop. Judged and passed: item "any other step of T-1a depends on the numeral gloss" (it does not: only step 3's message string and test N8); defect 2 (`derive-extraction` dead) is a pre-existing fact about a verb, not a caller I could not repair. If the owner reads defect 2 as "the workplan text and the code disagree about what exists", the right call is a stop, and the task file should be corrected before a real execution.
