# T-016  The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses prose units)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-016-report.md`, patch `.../T-016.patch` (stacked on the T-008 re-pilot); defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-016 |
| Title | The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses prose units) |
| Wave | 1 (chain, first) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | prior workplan T-1a in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-008 and T-014 merged (T-008 changes the same writer, built what replaces this task's numeral gloss and declared `dbcore.QUANTITY_CLAIM_TYPES`; T-014 makes the stress harness that section 6 runs before and after). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** T-1a's done-when unmet: `grep -rn "def parse_bound" scripts` returns a line. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-016-wp-t1a-reading "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-016" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The writer accepts a unit cell holding prose and a figure it cannot read, so most governing claims of a parameter are left out of its value without anyone being told. This task is also the first link of the chain to the lens fix.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
grep -rn 'def parse_bound' scripts; sed -n '/\*\*T-1a Reading/,/Code +45/p' workplan/2026-10-23-pipeline-resolution-workplan.md
```

**Expected output today:** `scripts/assess/assess_cell.py` defines `parse_bound`; the workplan paragraph for T-1a with its done-when.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

**This section is the whole change; you do not need to open anything else to execute it.** It was extracted from T-1a in `workplan/2026-10-23-pipeline-resolution-workplan.md` and from the T-1 section of `scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md` (steps 1 to 5 and 7), with the pilot's corrections. If you do open that report, these parts of it **do not apply** and this file overrides them: its common protocol (§3.0, P-1 to P-10: a branch from `origin/main`, writing `scratchpad/CURRENT`, the attribution lines and session link it prints, its pull-request steps, the gate `run_checks.py --changed-from origin/main`, a mutation harness under `scratchpad/$STEM/`; sections 2, 6, 7 and 11 here govern those); T-1 steps 6 (the numeral gloss: see below), 8 (OR-3), 9 (OR-10) and 10 (OR-11a), which this task does not execute; its test location (`scripts/tests/test_db_amend_writers.py`, whose ids `N01` to `N05` already exist and which lacks the fixtures these cases need), its test rows N8, N8b and N12, its mutations M5 and M6, its "KILLED six times", its "`build_graph.py --check` reports 0 failures" (section 5 says how to read that check), the counts in its step 4, and its sentence "every live numerical claim already carries a comparator" (false: see item 5).

**The numeral gloss is not built** (owner ruling of 2026-11-12, CLAUDE.md rule 0): a number written in words is entered as a numeral and unit, with the source's wording in a column of its own (`grep -n -F "just translate these into numbers/units" references/project-standards.md`). T-008 built that (`--value-as-written`, column `value_as_written`). Add no `--numeral-gloss` argument and write no `NUMERAL-GLOSS:` text into `notes` (a marker in a note is two facts in one cell, which the owner's schema ruling of 2026-11-06 forbids). Where the claim types `numerical` and `range` are meant, read `dbcore.QUANTITY_CLAIM_TYPES` (declared by T-008); never type the pair again. Locate code by symbol, never by line number.

1. **Move the notation code to `scripts/dbcore.py`** (stdlib only).
   - In `scripts/assess/assess_cell.py`, cut from the comment line `#: NOTATIONS OF ONE QUANTITY` through the end of `def bound_on_scale` (`grep -n "NOTATIONS OF ONE QUANTITY\|^def bound_on_scale\|^def parse_bound" scripts/assess/assess_cell.py`). The block holds `NOTATION_FAMILIES`, `_CONVERTIBLE`, `_RATIO_RE`, `notation_family`, `to_canonical`, `from_canonical` and `bound_on_scale`; `parse_bound`, which follows it, is deleted, not moved (item 2).
   - Paste it into `scripts/dbcore.py` directly after `QUANTITY_CLAIM_TYPES` (`grep -n '^QUANTITY_CLAIM_TYPES' scripts/dbcore.py`), not after `ENGINE_EXTRACTION_COLUMNS`: item 4 uses that constant. Add `from fractions import Fraction` to dbcore's imports (`re` is already there).
   - `bound_on_scale`'s docstring names `parse_bound` and says it "is left exactly as it was": rewrite those sentences so the docstring states, itself, what `parse_bound`'s said and is still true (the comparator IS the bound; a bare number is read as a point, so a ceiling stored without `<=` contributes a floor as well).
   - In `assess_cell.py`, import the names back where the block was, so the engine's names stay valid for its importers:
     ```python
     # The notation arithmetic lives in dbcore, so the writer that refuses an unreadable figure and the
     # engine that reads it are one definition. Names are imported back so the engine's names stay valid.
     from dbcore import (NOTATION_FAMILIES, _CONVERTIBLE, notation_family,  # noqa: E402,F401 -- one home (T-016)
                         to_canonical, from_canonical, bound_on_scale)
     ```
   - Then `grep -n 'Fraction' scripts/assess/assess_cell.py`: if only comments remain, delete `from fractions import Fraction` and the three-line `# EXACT, NEVER FLOAT` comment above it.
   - In `scripts/tests/test_assess_cell_pilot.py`, the block that patches `_ac.NOTATION_FAMILIES["gradient"]` imports `dbcore as _ac` instead of `assess_cell as _ac` (the dict is shared, so both pass; the test names the home).
2. **Delete `parse_bound`** (dead: `git grep -n 'parse_bound(' -- scripts schemas skills .claude` prints only its own `def`). In `compose_value`'s comment "`parse_bound`'s own docstring says the comparator IS the bound", write `dbcore.bound_on_scale` for `parse_bound`. Ledger lines that name it stay (append-only).
3. **`dbcore.VALUE_BEARING` and `dbcore.unit_refusal`.** Move the regex `_VALUE_BEARING` out of `scripts/db.py` into dbcore and leave the alias `_VALUE_BEARING = dbcore.VALUE_BEARING` in `db.py`, so its importers keep working (`git grep -n '_VALUE_BEARING\b' -- scripts`: `scripts/audit/medical_lens_integrity.py` and `scripts/tests/test_scan_contract.py` read `db._VALUE_BEARING`). In dbcore, after the notation block:
   ```python
   #: A name or a unit may not state its own answer: digits, comparator symbols, min/max words. Moved here
   #: from `db.py` (which keeps `_VALUE_BEARING = dbcore.VALUE_BEARING`): one definition for both screens.
   VALUE_BEARING = re.compile(r"[0-9≥≤<>=]|\b(min|max|minimum|maximum)\b", re.I)


   def unit_refusal(unit):
       """The sentence that refuses a `claimed_unit` that is not a bare scale, else None. `dB(A)` passes."""
       u = (unit or "").strip()
       if not u:
           return None
       if (VALUE_BEARING.search(u) or re.search(r"[;,]|\b(where|if|unless|except|only|when)\b", u, re.I)
               or ("(" in u and not re.fullmatch(r"[A-Za-z]+\([A-Z]\)", u))):
           return ("a unit names the scale only. Put a condition in its own row (`add-extraction "
                   "--figure-role condition` on the parameter it measures) joined by `--relation "
                   "condition_on`; put applicability (new build, alteration, building type) in "
                   "`--setting`; put commentary in `--notes`")
       return None
   ```
   Copy the regex from `db.py` as it stands on `$BASE` if it differs from the line above; the alias must leave behaviour unchanged.
4. **`dbcore.figure_refusal`.** After `unit_refusal`:
   ```python
   def figure_refusal(value, unit, comparator, claim_type):
       """The sentence that refuses a quantity figure the engine cannot read, else None.

       None when `claim_type` is not in `QUANTITY_CLAIM_TYPES`. Otherwise None only when `bound_on_scale`
       reads the figure AND it is neither a slash ratio in a gradient unit (`bound_on_scale` reads `1/12`
       as 0.083 %, so that is tested first) nor an inverted gradient ratio (`12:1`, in either end of a range).
       """
       if claim_type not in QUANTITY_CLAIM_TYPES:
           return None
       v, u = (value or "").strip(), (unit or "").strip()
       if "/" in v and notation_family(u):
           return "write a gradient ratio as rise:run (1:12), not 1/12, which reads as 0.083 %"
       if bound_on_scale(v, u, comparator, claim_type) is None:
           if re.search(r"\d\s*%", v):
               return f"write the number ({v.replace('%', '').strip()}) and put % in --claimed-unit"
           if re.search(r"\d\s+in\s+\d", v):
               return "write '1 in 12' as 1:12 with --claimed-unit 'rise:run ratio'"
           if re.search(r"\d,\d", v):
               return "write a decimal comma as a point (30,0 -> 30.0); the digits stay the same"
           if ":" in v and not notation_family(u):
               return ("a ratio needs the unit 'rise:run ratio' -- if, and only if, the source measures "
                       "rise over HORIZONTAL run; rise over slope length is a different unit")
           if claim_type == "range":
               return "write a range as 'a to b' (e.g. '0 to 4.8')"
           if not re.search(r"\d", v):
               return ("a number written in words is entered as a numeral and unit, with the source's "
                       "wording in --value-as-written")
           return f"{v!r} with unit {u!r} cannot be placed on any scale"
       if notation_family(u):
           for part in re.split(r"\s+to\s+", v):
               if ":" in part:
                   rise, run = (Fraction(x) for x in part.split(":", 1))
                   if rise > run:
                       return ("an inverted ratio (rise larger than run): write 1:12, and record the "
                               "source's order in --notes")
       return None
   ```
   Chosen (pilot 2026-11-13): the inverted-ratio test splits a range on ` to ` and tests each end. The report's sketch split the whole value on the first colon, so the live range `1:6 to 1:14` (`SELECT extraction_id FROM source_value_extractions WHERE claimed_value LIKE '%:% to %:%'`) raised `ValueError` (`Fraction('6 to 1:14')`) inside the writer; section 6 has the case that goes red on that sketch. The no-digit branch is reached only by a `--verbatim-exempt` row: on any other row T-008's number check in `_require_verbatim` refuses a value with no numeral first, so this branch is tested by a direct call (section 6, `T016-N8`).
5. **Wire the refusals into `db.insert_extraction`**, directly after the `for col in _SVE_VOCAB_COLUMNS:` loop:
   ```python
   # --- the figure must be readable (T-016) ----------------------------------
   # A unit that is a sentence and a value the engine cannot place on a scale are both left OUT of a
   # determination's value without anyone being told; refuse them here, with the fix.
   for _why in (dbcore.unit_refusal(row.get("claimed_unit")),
                dbcore.figure_refusal(value, row.get("claimed_unit"), row.get("comparator"), claim_type)):
       if _why:
           raise Refusal(f"add-extraction: {_why}. Nothing was written.")
   if figure_role in ("claim", "derived") and claim_type == "numerical" and not row.get("comparator"):
       raise Refusal("add-extraction: a value-supplying numerical row needs --comparator ('=' for a "
                     "point); a bare number is read as a point and adds a floor as well as a ceiling. "
                     "Nothing was written.")
   ```
   These run after the quote, locator (R3) and T-008 number checks, which are unchanged. **Stored rows are history and are not touched:** two live value-supplying numerical rows carry no comparator (`SELECT extraction_id, claimed_value, claimed_unit FROM source_value_extractions WHERE figure_role IN ('claim','derived') AND claim_type='numerical' AND comparator IS NULL`), and the unit screen refuses some live units (run `dbcore.unit_refusal` over `SELECT claimed_unit, COUNT(*) FROM source_value_extractions GROUP BY 1` on a copy). The new refusals apply when a row is written; no stored row is re-valued, and the engine still reads those rows as before. Do not amend them here: that is research data (rule 10). List the two ids in the pull request as the research follow-up (`comparator` is already in `_AMENDABLE_SVE_FIELDS`, so `amend-extraction` can set it).
6. **One home for derived arithmetic.** Chosen (pilot 2026-11-13): one helper in `scripts/db.py`, beside `_refuse_live_confirmation`:
   ```python
   def _refuse_derived_mismatch(conn, extraction_id: int, context: str):
       """Refuse a derived figure that disagrees with its own base + delta: the ONE home of that arithmetic.
       Reads `v_derived_figure_check` inside the caller's transaction, so the raise rolls back the row and its
       edges. Tolerance: `extraction_relations_integrity`'s EPSILON, which reads the same view afterwards. The
       view joins on equal units and plain numerals, so a converted row is not compared (its
       `--conversion-note` is its only record)."""
       bad = conn.execute("SELECT stored, recomputed FROM v_derived_figure_check WHERE derived_id = ?",
                          (extraction_id,)).fetchone()
       if bad and abs(bad["recomputed"] - bad["stored"]) > 1e-9:
           raise Refusal(f"{context}: derived figure {bad['stored']} disagrees with its own base + delta "
                         f"({bad['recomputed']}). A derived figure that contradicts its inputs is the "
                         f"defect this check exists to stop. Nothing was written.")
   ```
   - In `insert_extraction`, after the loop that writes the relation edges and before the `return`: `if figure_role == "derived": _refuse_derived_mismatch(conn, extraction_id, "add-extraction")`.
   - In `relate_extraction`, after `_write_relation_edge(...)` inside the same `with`: `if row["figure_role"] == "derived" and relation == "derived_from": _refuse_derived_mismatch(conn, from_extraction, "relate-extraction")`.
   - In `derive_extraction`, delete the `if claimed_value is not None:` block that compares `abs(cn - (bn + dn)) > 1e-9` and raises; keep the computation (`if claimed_value is None and bn is not None and dn is not None: claimed_value = _fmt_num(bn + dn)`, `elif claimed_value is None: raise Refusal(...)`), with a one-line comment that a supplied value is compared by `_refuse_derived_mismatch`. Keep the string "extract the base figure first with add-extraction" (`workplan/pipeline-state-graph/machines.yaml` uses it as a needle).
   - A unit-converted derived row is no longer compared at write. That is not a weakened refusal: the deleted block compared raw numbers across units, so it refused a correct conversion (base and delta in m, stored in mm), and the integrity check already reports such rows as `UNCHECKED`. Say so in the pull request.
7. **Known pre-existing defect, recorded and not fixed here: `derive-extraction` cannot write a row.** It passes no `source_section`, no `loc_*` column and no `notes` to `insert_extraction`, and has no flag for any of them, so every row it builds is refused by R3's locator refusal ("R3: this row states a value with no locator"), which has applied to every tier since 2026-11-06 (`git log --format='%h %ad %s' --date=short -S'EVERY TIER NEEDS A LOCATOR' -- scripts/db.py | tail -1`). No derived row exists (`SELECT COUNT(*) FROM source_value_extractions WHERE figure_role='derived'`). Chosen (pilot 2026-11-13): this task does not repair it. A repair is a new locator interface on the verb (`--source-section`, and from tier 4 the `loc_*` hierarchy with `--locator-scheme`), which is not part of T-1a and touches a parser T-018 also changes; it is filed as its own task. Consequence for this task: after item 6 a mismatched `--claimed-value` on `derive-extraction` is still refused, but by R3, before the arithmetic is reached. The test reaches the shared check through the verb with a stated shim and also asserts the R3 refusal, so the case turns red the day the verb is repaired (section 6, `T016-N11` to `N11c`). Say so in the pull request.
8. **Callers repaired in this pull request** (section 5 finds them; each is listed in the pull request):
   - `scripts/tests/test_run_pipeline_refusals.py`: the fixture `extraction()` writes a `numerical` `claim` row with no comparator; add `"comparator": "="` to its base dict. Without it, five existing cases (`V04`, `X02`, `L02`, `L03`, and T-008's case that writes the Finnish sentence) go red after item 5 and the next T-008 case ends the run with an uncaught `Refusal` (pilot 2026-11-13).
   - `scripts/tests/test_assess_cell_pilot.py`: item 1's import.
   - `scripts/audit/extraction_relations_integrity.py`: the comment headed "TOLERANCE MATCHES THE WRITER'S" quotes the deleted `derive_extraction` comparison; reword it to name `db.py _refuse_derived_mismatch` (add-extraction, relate-extraction, derive-extraction) and `abs(recomputed - stored) > 1e-9`.
   - `skills/run-pipeline_SKILL.md`: in the `add-extraction` bullet, after "value and unit", add "`--comparator` for a numerical figure (`=` for a point)", and append to its "**The writer refuses:**" list: a `--claimed-unit` that is a sentence rather than a scale (the condition is its own row, `--relation condition_on`; applicability is `--setting`); a quantity figure the engine cannot place on a scale (`8.33%`, `1/12`, `12:1`, `1 in 12`, a decimal comma; the refusal names the fix); a value-supplying numerical row with no `--comparator`; a `derived` figure that disagrees with its own base + delta. `python3 scripts/audit/skill_vocabulary_audit.py` must be no worse after.
   - The stress harness of T-014, `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/stress_run3.py` (a live harness since T-014, so a caller despite its path): its `add_ext` and its quote-variant `add-extraction` call pass no `--comparator`, so after item 5 every probe that was accepted would be refused for the comparator, the wrong reason. Make `anchor()` select `comparator` as an eighth column, unpack it in `add_ext`, and pass `*(("--comparator", c) if c else ())` with `c` the anchor row's own comparator in both places. Do this **before** the harness's before-run (section 6), so the two runs differ only by the writer.

**What reads what this task adds or changes:** `add-extraction` and `derive-extraction` (through `insert_extraction`), `relate-extraction`, the engine (`assess_cell.py`, which imports the notation names back), `medical_lens_integrity.py` and `test_scan_contract.py` (through the `_VALUE_BEARING` alias). `amend-extraction` is not changed. It deletes code (`parse_bound`, the duplicate arithmetic in `derive_extraction`, the engine's own copy of the notation block, now moved): the code-size line must show it.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `parse_bound`, `NOTATION_FAMILIES`, `derive_extraction`, `numeral-gloss`, `insert_extraction`, `add-extraction`, `derive-extraction`, `_VALUE_BEARING`, `bound_on_scale`, `to_canonical`, `from_canonical`, `notation_family`, `_CONVERTIBLE`, `v_derived_figure_check`. The first four alone miss every caller the pilot found: a new refusal in `insert_extraction` changes the truth of everything that writes through it.

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

**One exception to the exclusions:** `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/` is not a frozen record once T-014 has merged; it is the live harness section 6 runs. Sweep its scripts too: `git grep -n -F -e 'add-extraction' -- 'scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/*.py'`. On 2026-11-13: `stress_run3.py` (`add_ext` and the quote-variant call: callers, section 4 item 8); `stress_run.py` (three probes written to be refused by a check that runs before the new ones: mentions) and `stress_run2.py` (one step; not part of the harness section 6 runs: a mention).

**Hits when this file was written** (2026-11-12 for the first four names, 2026-11-13 for the rest, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `parse_bound`: code and skills: `scripts/assess/assess_cell.py`. Prose: none.
- `NOTATION_FAMILIES`: code and skills: `scripts/assess/assess_cell.py`, `scripts/tests/test_assess_cell_pilot.py` (a caller: it patches the dict; section 4 item 1). Prose: none.
- `derive_extraction`: code and skills: `scripts/audit/extraction_relations_integrity.py` (a caller by truth: a comment quotes the deleted comparison; section 4 item 8), `scripts/db.py`. Prose: `workplan/pipeline-state-graph/machines.yaml` (a needle; kept, a mention).
- `numeral-gloss`: no file. The name does not exist yet, or lives only in the excluded paths.
- `insert_extraction`: code: `scripts/db.py`, `scripts/tests/test_db_amend_writers.py` (no numerical write without a comparator; a mention: the pilot saw it unchanged), `scripts/tests/test_run_pipeline_refusals.py` (a caller: the `extraction()` fixture; section 4 item 8), `scripts/tests/test_scan_contract.py` (its `claim()` already passes a comparator; a mention). Prose: `workplan/pipeline-state-graph/machines.yaml`.
- `add-extraction`: code and skills: `.claude/settings.json`, `scripts/assess/assess_cell.py`, `scripts/audit/observation_verbatim_audit.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/verified_scan_integrity.py`, `scripts/db.py`, the three test files above, `skills/gap-driven-mining_SKILL.md`, `skills/run-pipeline_SKILL.md` (a caller: it lists what the writer refuses; section 4 item 8). Prose: `governance/check-registry.yaml`, `governance/pipeline-contract.yaml`, `governance/pipeline-operations.md`, `governance/research-contract.yaml`, `workplan/pipeline-state-graph/machines.yaml`. A sentence that lists what `add-extraction` requires or refuses is a caller; a sentence that only names the verb is a mention. Harness: `stress_run3.py` (a caller; section 4 item 8).
- `derive-extraction`: code and skills: `scripts/audit/extraction_relations_integrity.py`, `scripts/db.py`, `skills/connection-discovery_SKILL.md`, `skills/run-pipeline_SKILL.md`. Prose: `governance/check-registry.yaml`, `workplan/pipeline-state-graph/machines.yaml`. The skill sentences that offer the verb for computed figures were already false before this task (section 4 item 7); they are mentions here and belong to the task that repairs the verb.
- `_VALUE_BEARING`: code: `scripts/audit/medical_lens_integrity.py`, `scripts/tests/test_scan_contract.py` (both read `db._VALUE_BEARING`; the alias keeps them), `scripts/audit/research_batch_dod.py` (comment), `scripts/tests/test_run_pipeline_refusals.py` and `scripts/validate_parameters.py` (they read `_VALUE_BEARING_NAME`, which stays in `db.py`). Prose: none.
- `bound_on_scale`, `notation_family`, `_CONVERTIBLE`: `scripts/assess/assess_cell.py` only. `to_canonical`: also `scripts/tests/test_assess_cell_pilot.py`. `from_canonical`: also `scripts/audit/graph/build.py`, whose hit is `_assert_distinct_from_canonical`, a different name (a mention). Prose: none.
- `v_derived_figure_check`: code: `scripts/audit/extraction_relations_integrity.py`, `scripts/db.py`. Prose: `governance/context-map.yaml`, `governance/pipeline-contract.yaml` (mentions). `sqlite_master`: the view's own definition.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_assess_cell_pilot`, `extraction_relations_integrity`, `test_run_pipeline_refusals`, `test_scan_contract`, `test_db_amend_writers`, `test_author_presence`, `test_search_log_completeness`, `test_validate_evidence_state_2_4`, `claude_md_spine`, `research_contract_sync`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_assess_cell_pilot extraction_relations_integrity test_run_pipeline_refusals test_scan_contract test_db_amend_writers test_author_presence test_search_log_completeness test_validate_evidence_state_2_4 claude_md_spine research_contract_sync"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`), except two that never print one: `test_assess_cell_pilot` (count its `PASS:` lines: `grep -c '^ *PASS:' "$SCRATCH/before-test_assess_cell_pilot.txt"`) and `test_validate_evidence_state_2_4` (it prints `ALL PASS (0 failed)` and `[PASS]` lines); report those counts as their subject. `extraction_relations_integrity` examines rows but no derived row exists (`SELECT COUNT(*) FROM v_derived_figure_check`), so it cannot go red on section 4 item 6: the tests do that. A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** Done when every item below is run and shown in the pull request. Begin each block with the `BASE=` and `export SCRATCH=` lines, and `ST=scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress`.

*2a. The engine's reader, before any edit.* Two probe scripts from the 2026-10-22 report record what the engine reads; the move must not change a byte of their output. Extract them into `$SCRATCH` (not the repository) and run them:
```
R=scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md
for f in fixtures_g1_g13 notation_probe; do awk -v h="# $f.py" 'index($0,h)==1{p=1} p&&/^```/{exit} p' "$R" > "$SCRATCH/$f.py"; python3 -I "$SCRATCH/$f.py" "$PWD" > "$SCRATCH/$f-before.txt" 2>&1; wc -l < "$SCRATCH/$f-before.txt"; done
```
Each prints a non-zero line count (13 and 15 on 2026-11-13). Do not edit either script: `notation_probe.py` imports `bound_on_scale` from `assess_cell`, which still exports it after section 4 item 1. After the change, the same loop with `-after` and `cmp "$SCRATCH/$f-before.txt" "$SCRATCH/$f-after.txt"` for each: identical.

*2b. The stress harness, before.* Make the `stress_run3.py` repair of section 4 item 8 first (it changes the probes' arguments, so it must be in both runs), then, on the unchanged writer: `python3 -I $ST/stress_run3.py --out "$SCRATCH/H-before" --parts guards` (about a minute; its last line must read `UNCHANGED`). Read `guards.control-exact` in `$SCRATCH/H-before/guards/log.jsonl`: rc 0. After the change, the same to `$SCRATCH/H-after`, then `python3 -I $ST/stress_diff.py "$SCRATCH/H-before" "$SCRATCH/H-after"`. Expected: `guards.unit-in-prose` differs (accepted before, refused after by the unit screen) and `guards.control-exact` does not. Any other differing step must print one of section 4's refusal sentences (unit, figure, comparator) on an input that refusal is meant for (for example `guards.fullwidth-digits`, if T-008 accepted it: a full-width colon is not a ratio the engine reads); list each in the pull request. Any other difference is a stop (section 9).

*2c. The tests, written before the change and run on the unchanged writer.* Chosen (pilot 2026-11-13): the cases go in `scripts/tests/test_run_pipeline_refusals.py`, as a new section at the end before `finish()`, headed `print("Section T016: ...")`, not in `test_db_amend_writers.py` (whose `N01` to `N05` collide and which has no verified-source fixture). Confirm the prefix is free: `grep -c '"T016-' scripts/tests/test_run_pipeline_refusals.py` prints 0. Use the file's own helpers: inside `with scratch() as c:`, `ref = new_source(verified=True)`, `held_text(ref, "\n".join(sentences))`, `hand_scan(c, ref, "full")`, `pid = P_ACTIVE[0]`; build each row with `extraction(ref, pid, claim_text=<its sentence>, claimed_value=..., claimed_unit=..., comparator=...)`; call `refusal(db.insert_extraction, row, session=S, dry_run=True, relations=[])` for a refusal (its text, or None) and `ok(...)` for an acceptance (`(result, error)`); `record(tid, name, passed, details)`. Make the `extraction()` fixture change of section 4 item 8 in the same edit. The fixture sentences are test text, written in the case, one per case, each holding the figure it claims (for example "A ramp gradient of 8.33% is the greatest permitted.", "The fall is 1/12 over the run.", "A slope of 12:1 is shown on the drawing.", "Ramps are to be not steeper than 1:12 along the run.", "Where the height difference is at most 0.05 m a ramp is to be not steeper than 1:12.", "The surface is to be slip-resistant when wet.", "The first flight rises 5.5 percent.", "The second flight rises 9.25 percent.", "The combined rise is 14.75 percent.", "The combined rise is 99 percent.").

| id | call | input (value / unit / comparator) | expected after the change | on unchanged code |
|---|---|---|---|---|
| T016-N1 | `insert_extraction`, dry run | `8.33%` / `%` / `<=` | refused; text contains `put % in --claimed-unit` | red (accepted) |
| T016-N2 | same | `1/12` / `rise:run ratio` / `<=` | refused; `not 1/12` | red |
| T016-N3 | same | `12:1` / `rise:run ratio` / `<=` | refused; `inverted` | red |
| T016-N3b | `ok(lambda: dbcore.figure_refusal(...))` | `1:6 to 14:1` / `rise:run ratio` / `between`, claim type `range` | the returned text contains `inverted` | red (no function) |
| T016-N4 | `insert_extraction`, dry run | `1:12` / `rise:run ratio (maximum) where the height difference is <= 0.05 m` / `<=` | refused; `condition_on` | red |
| T016-N4b | same | `1:12` / `rise:run ratio max` / `<=` (the value-bearing screen alone) | refused; `condition_on` | red |
| T016-N4c | same | `1:12` / `rise:run ratio unless steep` / `<=` (the condition words alone) | refused; `condition_on` | red |
| T016-N4e | same | `1:12` / `ratio (new build)` / `<=` (the parenthesis rule alone) | refused; `condition_on` | red |
| T016-N5 | same | `1:12` / `ratio` / `<=` | refused; `rise:run ratio` | red |
| T016-N6 | same | `1:12` / `rise:run ratio` / none | refused; `--comparator` | red |
| T016-N7 | same, `ok` | `1:12` / `rise:run ratio` / `<=` | accepted (control) | green |
| T016-N7b | same, `ok` | a `qualitative` claim, value `slip-resistant`, unit None, comparator None | accepted (control) | green |
| T016-N7c | `ok(lambda: dbcore.figure_refusal(...))` | `1:6 to 1:14` / `rise:run ratio` / `between`, `range` | returns None with no exception (the report's sketch raised `ValueError` here) | red (no function) |
| T016-N8 | `ok(lambda: dbcore.figure_refusal(...))` | the `claimed_value` of the first quantity-type row whose value has no digit, derived by query (`SELECT claimed_value FROM source_value_extractions WHERE claim_type IN (SELECT value FROM json_each(?)) AND claimed_value NOT GLOB '*[0-9]*' ORDER BY extraction_id LIMIT 1` with `json.dumps(list(dbcore.QUANTITY_CLAIM_TYPES))`) / `%` / `<=` / `numerical` | the returned text contains `--value-as-written`; `skip(...)` if the query returns no row | red (no function) |
| T016-N9 | `insert_extraction`, written (not dry run) | base `5.5` and delta `9.25` (`%`, `=`) written first through `insert_extraction`; then a `derived` row `99` / `%` / `=` with `relations=` two `derived_from` edges (`input_role` `base` and `delta`, `stated` `named`, each edge's `quote` its target's sentence) | refused; `disagrees`; the counts of `source_value_extractions` and `extraction_relations` on the scratch copy are unchanged | red (accepted) |
| T016-N10 | same, dry run, `ok` | the same derived row with `14.75` | accepted (control) | green |
| T016-N11 | `db.derive_extraction` through a SHIM | base and delta of N9, `claimed_value="99"`, `comparator="="`, `claim_text` the "99" sentence, `identity=IDENT` | refused; text contains `disagrees with its own base + delta`; counts unchanged | red (the old check's text differs) |
| T016-N11a | same SHIM, `ok` | the same with no `claimed_value` and the "14.75" sentence | accepted; the stored `claimed_value` is `14.75` | green |
| T016-N11c | `db.derive_extraction`, no shim | the N11a call | refused; text starts with `R3:` (the known defect of section 4 item 7; this case goes red when the verb is repaired, and that repair removes the shim) | green |
| T016-N11b | `db.relate_extraction` | a `derived` row `99` written with its `base` edge only, then `relate_extraction(row, "derived_from", S, to_extraction=delta, stated="named", quote=<delta sentence>, input_role="delta")` | refused; `disagrees`; counts unchanged | red (accepted) |

The SHIM, stated in a comment beside it: `derive_extraction` passes no locator (section 4 item 7), so for N11 and N11a only, replace `db.insert_extraction` with a wrapper that adds `"source_section": "section 3"` to the row, and restore it straight after (`_insert = db.insert_extraction; db.insert_extraction = lambda data, *a, **k: _insert({**data, "source_section": "section 3"}, *a, **k)`, then `db.insert_extraction = _insert`, in a `try`/`finally`).

In `scripts/tests/test_assess_cell_pilot.py`, after the block that patches `NOTATION_FAMILIES`, assert `dbcore.bound_on_scale` exactly, with `expect(...)`: `("1:12", "rise:run ratio", "<=", "numerical")` gives `(None, Fraction(25, 3))`; `("8.33", "%", "<=", "numerical")` gives `(None, Fraction("8.33"))`; `("1:20", "rise:run ratio", ">=", "numerical")` gives `(Fraction(5), None)`; `("0 to 4.8", "%", "between", "range")` gives `(Fraction(0), Fraction("4.8"))`; `("1/12", "rise:run ratio", "<=", "numerical")` gives `(None, Fraction(1, 12))` (the reader still reads it; the writer refuses it); `("8.33%", "%", "<=", "numerical")` gives `None`. Red on unchanged code (no `dbcore.bound_on_scale`).

Run both files on the unchanged writer: the cases marked red above are red and the controls green. Then make the change and run them again: every case green, and T-008's cases (among them the two that write the Finnish sentence) still green.

*2d. The mutations.* Each must be KILLED. Write a harness to `$SCRATCH/t016-mutations.py` (not in the repository): a list of `(name, path, old, new, test)`; for each, read the file, `assert text.count(old) == 1` (if not, lengthen `old` with its neighbouring text), write the edit, run `python3 <test>` from the repository root, print `KILLED` when the exit code is not 0 and `SURVIVED` otherwise, and restore the file in a `finally`. The test for every row is `scripts/tests/test_run_pipeline_refusals.py` (about 40 s a run).

| id | path | old → new | killed by |
|---|---|---|---|
| M1 | `scripts/dbcore.py` | `if (VALUE_BEARING.search(u) or` → `if (False or` | T016-N4b |
| M2 | `scripts/db.py` | `and not row.get("comparator"):` → `and False:` | T016-N6 |
| M3 | `scripts/dbcore.py` | in `figure_refusal`, `if claim_type not in QUANTITY_CLAIM_TYPES:` → `if True:` | T016-N1, N2, N3, N5 |
| M4 | `scripts/db.py` | in `_refuse_derived_mismatch`, `> 1e-9:` → `> 1e9:` | T016-N9, N11 |
| M5 | `scripts/dbcore.py` | `if "/" in v and notation_family(u):` → `if False:` | T016-N2 |
| M6 | `scripts/dbcore.py` | `if rise > run:` → `if False:` | T016-N3, N3b |
| M7 | `scripts/db.py` | `_refuse_derived_mismatch(conn, from_extraction, "relate-extraction")` → `pass` | T016-N11b |
| M8 | `scripts/dbcore.py` | `for part in re.split(r"\s+to\s+", v):` → `for part in [v]:` | T016-N7c |

The harness prints KILLED eight times. (The report's M5 and M6 targeted the numeral gloss and OR-3, which this task does not build; its M1 survived on N4, whose unit trips all three screens at once, which is why N4b, N4c and N4e test one screen each.)

*2e. The rest.* `grep -rn "def parse_bound" scripts` prints nothing. `python3 scripts/audit/extraction_relations_integrity.py` prints `VERDICT: CLEAN` (see step 1 on what it cannot see). `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after, compared as section 5 says (the pilot saw identical output).

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T016-01`, `T016-02`, …) and confirm the prefix is free first (`grep -c '"T016-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

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

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: execute workplan T-1a reading [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- The code and section 4 disagree about what exists (a symbol it locates is missing, appears twice, or does something other than section 4 says): stop and report; do not reinterpret the plan. **Not a stop:** `derive-extraction` refused by R3's locator refusal. That is the known pre-existing defect of section 4 item 7, and the test of section 6 (`T016-N11c`) asserts it.
- In section 6 step 2b, `guards.control-exact` is refused in the before-run, or the after-run differs in a step section 6 does not account for.
- A mutation of section 6 step 2d survives after one honest attempt to make its case reach the code it targets.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
