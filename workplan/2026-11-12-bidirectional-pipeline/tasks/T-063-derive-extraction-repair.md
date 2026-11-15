# T-063  `derive-extraction` can write a derived figure honestly

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class) from OI-56's item "`derive-extraction` cannot write a row" and the three blockers T-016 recorded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-063 |
| Title | `derive-extraction` can write a derived figure honestly |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class: the question in section 2 (OD-40, what a derived figure's quote is) is resolved under delegation and read through its gate, so the executor chooses nothing about it |
| Traces to | OI-56 (`grep -n -F 'derive-extraction` cannot write a row' workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`); T-016 section 4 item 7 and its tests T016-N11c, N11d, N11e; the `derive_extraction` docstring's "KNOWN DEFECT" paragraph (`grep -n -F 'KNOWN DEFECT, recorded by T-016' scripts/db.py`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-016, T-018 merged (T-016 made `_refuse_derived_mismatch` the one home of the arithmetic and recorded the three blockers; T-018 changed the lens flags this verb shares with `add-extraction`). Both were merged on 2026-11-13. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. The one decision this task needed (this file's OQ-A, registered as OD-40: what a derived figure carries as its quote and its locator) is resolved under delegation (next bullet); its question and options are in `REMEDIATION-WORKPLAN.md` §8.
- **Delegated resolutions this task rests on.** OD-40: a derived figure has no quote or locator of its own; both are its inputs', reached through its two `derived_from` edges, each carrying its input's verified quote; the writer refuses a derived row whose inputs lack a quote or a locator, and still checks the arithmetic; a figure that a source states in words is a claim row, never a derived one. A resolution by an Opus-class model under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13 (ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-40" references/project-standards.md`): not the owner's words, reversible by the owner, checked by a second, independent Opus-class instance and confirmed with corrections applied, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-40; do gate $n; done
```
- **Tests that must be red (or green) before you start:** T016-N11c, N11d and N11e are green on the unchanged code (they assert the three blockers); this task turns them, as section 6 says.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-063-derive-extraction-repair "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-063" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command, and create the branch as shown. **Pilot or dry run:** do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

The owner expects the specifications pass to be "adjudicating, deriving and synthesizing across rows of related evidence" (OR-14: `grep -n -F 'This derivation is what I expect the specifications pass' references/project-standards.md`). The one verb that records a derived figure, with the edges that let a check recompute it, cannot write a row, so a computed figure today can only be typed into prose, where nothing recomputes it. Three blockers stand in front of `insert_extraction`, each reached once the one before is cleared: (1) the verb passes no locator, so R3 refuses every row; (2) a value-supplying numerical row needs a comparator and the verb has no default, though the comparator of a sum is arithmetic on its inputs' (rule 8: derive it, never ask for it); (3) its quote is the analyst's sentence, which the saved-bytes check refuses. A fourth defect sits behind them: `--conversion-note`, which the verb's own refusal calls "the only record of the arithmetic" for a unit-converted figure, is accepted and never stored (`grep -n 'conversion_note' scripts/db.py`: it appears in the signature, the refusal and the parser, and in no `data` key).

**Evidence command** (run from the repository root; it reads the code and the canonical database read-only):

```
python3 scripts/tests/test_run_pipeline_refusals.py 2>&1 | grep -E 'T016-N11[cde]'
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from source_value_extractions where figure_role='derived'\").fetchone())"
python3 - <<'PY'
import ast, pathlib
src = pathlib.Path('scripts/db.py').read_text(); fn = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == 'derive_extraction')
body = ast.get_source_segment(src, fn); data = body[body.index('data = {'):body.index('}', body.index('data = {'))]
print('conversion_note stored:', 'conversion_note' in data, '| comparator from inputs:', 'base_row["comparator"]' in body)
PY
```

**Expected output today:** three `[✓]` lines, T016-N11c, N11d and N11e (the blockers, asserted); `(0,)`; `conversion_note stored: False | comparator from inputs: False`.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves a verb that "looks implemented" and refuses everything, the shape its own comment calls worse than a missing verb. Locate code by symbol, never by line number.

**Items 1 to 4 build OD-40 as resolved under delegation (answer (a), as corrected by its independent check; section 2).**

1. **The comparator is derived, never asked for.** In `scripts/db.py`, directly above `def derive_extraction`:
   ```python
   def _derived_comparator(base_cmp, delta_cmp):
       """The comparator of base + delta, by interval arithmetic: a point delta ('=') keeps the base's bound; a delta
       bounded the same way as the base keeps that bound; anything else (a range, 'approx', opposite or mixed bounds,
       a base with no comparator) bounds nothing, and None is returned."""
       if delta_cmp == "=" and base_cmp in ("=", ">=", ">", "<=", "<"):
           return base_cmp
       if delta_cmp == base_cmp and base_cmp in (">=", ">", "<=", "<"):
           return base_cmp
       return None
   ```
   In `derive_extraction`, read `comparator` with the base and delta rows (add it to both `SELECT`s), set `comparator = _derived_comparator(base_row["comparator"], delta_row["comparator"])`, and refuse when it is None: `f"derive-extraction: the sum of base {base} ({base_row['comparator'] or 'no comparator'}) and delta {delta} ({delta_row['comparator'] or 'no comparator'}) is not a bound. A point delta ('=') moves the base's bound; two bounds of the same kind add. Set a missing comparator with amend-extraction --field comparator. Nothing was written."` Delete the `comparator` parameter from the signature, the `--comparator` argument from the `derive-extraction` parser and from its dispatch call. Chosen (authoring 2026-11-13): derived and not checked against a supplied value, because a flag that can only agree or disagree with arithmetic is rule 8's anti-pattern in one line; rejected: keeping `--comparator` and refusing a disagreeing one.
2. **One unit, or no derivation.** Delete `--claimed-unit` and `--conversion-note` (signature, parser, dispatch) and the refusal that asks for them; refuse instead when `base_row["claimed_unit"] != delta_row["claimed_unit"]`: `f"derive-extraction: base {base} is stated in {base_unit!r} and delta {delta} in {delta_unit!r}. This verb adds figures stated in one unit; a converted figure is not recomputed by any check (v_derived_figure_check joins on equal units). Nothing was written."`, and store the inputs' unit. Chosen (authoring 2026-11-13): delete the cause. The note was never stored, the integrity check names unit-converted derived rows as "the derived figures MOST likely to be wrong" and cannot see them (`grep -n -F 'MOST likely to be wrong' scripts/audit/extraction_relations_integrity.py`), and T-030 makes exact conversions data a later change can read; rejected: storing the note in `notes` (a prefix that says what the rest of the cell means, the joined-cell shape of the owner's 2026-11-06 ruling, CLAUDE.md §4) or a new column nothing would read.
3. **The quote and the locator** (`insert_extraction`, which `derive_extraction` calls). Read `figure_role = row.get("figure_role")` before the verbatim floor (it is read further down today; reading it earlier changes nothing else).
   - **Under (a), as resolved:**
     - The verbatim floor (the refusal that begins `--claim-text is required and must not be blank`) and the `_require_verbatim` call apply unless `figure_role == "derived"`. A derived row stores no quote: a `claim_text` given for one is refused, because a figure a source states in words is a claim row, never a derived one (OD-40 as corrected).
     - R3: for a derived row with no locator of its own, instead of the two `R3:` refusals, require that every `derived_from` edge in `relations` points at a row with a locator: `source_section`, any `loc_*` level, or `[UNVERIFIED-QUANT]` in its `notes`. Refuse naming the input that has none: `f"R3: derived figure's input {to_id} has no locator, so the derived figure cannot be found again. Nothing written."` Require at least the `base` edge in the same call (the amend path already requires one: `grep -n -F "figure_role='derived' requires at" scripts/db.py`).
     - In `derive_extraction`: `--claim-text` is no longer taken (signature, parser, dispatch): a derived figure has no quote of its own; its words are its inputs' (`grep -n -F "OD-40: a derived figure has no quote" references/project-standards.md`). `claim_text` is None.
     - **The derived row's own `ref_id`** is NOT NULL (`PRAGMA table_info(source_value_extractions)`), so a figure derived from two sources names one of them. Say, in the verb's help and docstring, that this `ref_id` is a pointer to the base input (as `root_ref_id` already is) and not an attribution of the derived figure to that source; or refuse inputs from two sources until it is said (the independent check of OD-40, its section (5)).
     - The lens warrant: `named_in_text` already accepts a word found in a file saved for the source, and `heading` needs a `source_section` a derived row does not carry, so it is refused by the existing rule; leave both. Say so in the pull request.
4. **The docstring and the comments.** Replace the `derive_extraction` docstring's "KNOWN DEFECT, recorded by T-016 and NOT repaired here" paragraph with one sentence naming this task, the answer and what the verb now derives (comparator, unit). In the edge comment block that begins `# EACH EDGE CARRIES ITS OWN TARGET'S QUOTE`, keep the paragraph; correct `a derived row's claim_text is by its nature the analyst's computation statement` to say what the answer made it.

**What reads what this task adds or changes:** `db.py derive-extraction` (the CLI and the Python API); `v_derived_figure_check` and `extraction_relations_integrity` read the rows it writes; the engine reads a derived row as a value-supplying figure (`dbcore.VALUE_SUPPLYING_ROLES`). It deletes `--comparator`, `--claimed-unit` and `--conversion-note` from the verb and the refusal that asked for them.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `derive_extraction`, `derive-extraction`, `conversion-note`, `conversion_note`, `_refuse_derived_mismatch`, `v_derived_figure_check`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4).

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `graph.json` and `STATE-GRAPH.md`; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md`; `scripts/migrations/`; `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/`.

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task removes flags and changes refusals: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after (red on the base; only a count above your before-run is yours).

**Hits when this file was written** (2026-11-13):

- `scripts/tests/test_run_pipeline_refusals.py`: **callers.** T016-N11 and N11a call the verb through a SHIM that adds a locator, and pass `comparator="="`; N11c, N11d and N11e assert the three blockers. After the change: remove the SHIM; N11 (a wrong `--claimed-value`, refused by the shared check) and N11a (computed 14.75, accepted) call the verb directly with no `comparator`; N11c, N11d and N11e are rewritten as section 6 step 2a says.
- `scripts/audit/extraction_relations_integrity.py`: **a caller.** The comment that names `derive-extraction --claimed-unit --conversion-note` as the writer of unit-converted rows: say that the verb no longer writes them (this task) and that such a row can still arrive through `add-extraction` with `derived_from` edges, which the view still cannot see; the check's logic is unchanged.
- `governance/check-registry.yaml`: a comment says `relate-extraction and derive-extraction still expose no flag of their own` for `--verbatim-exempt`: still true (a mention).
- `skills/run-pipeline_SKILL.md` and `skills/connection-discovery_SKILL.md`: offer `derive-extraction` for computed figures (false until now; true after, a mention), and must not name `--conversion-note` or `--comparator` for it (if either does, correct it). Add to `run-pipeline_SKILL.md`, after `` `derive-extraction` for computed figures ``: `(the comparator and the unit are its inputs'; a derived figure has no quote or locator of its own: its words and its place are its inputs', reached through its `derived_from` edges)`. Run `python3 scripts/audit/skill_vocabulary_audit.py`: no worse.
- `workplan/pipeline-state-graph/machines.yaml`, `M04.t3`: its needle `extract the base figure first with add-extraction` must still match (keep that string in the verb's refusal). Its guard stays true.
- `governance/pipeline-contract.yaml`: names the verb as a writer (a mention).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_run_pipeline_refusals`, `test_db_amend_writers`, `extraction_relations_integrity`. Run each as the registry runs it and keep the output:

```
CHECKS="test_run_pipeline_refusals test_db_amend_writers extraction_relations_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything (on 2026-11-13 `test_run_pipeline_refusals` failed X02 and X03, whose fixture source now holds a decodable text): record it and carry on.

**Step 2: red before, green after.**

*2a. The tests* (answer (a), as resolved under delegation). In `scripts/tests/test_run_pipeline_refusals.py`, in the T016 derived block (base `5.5`, delta `9.25`, both `%` and `=`, written for real on the scratch copy), confirm `grep -c '"T063-' scripts/tests/test_run_pipeline_refusals.py` prints 0, then:

| id | call (no SHIM) | expect after the change | on unchanged code |
|---|---|---|---|
| T016-N11c (rewritten) | `db.derive_extraction(ref_id=t16, parameter_id=pid, base=base_id, delta=delta_id, session=S, identity=IDENT, **lens_of(T16["good"]))` with no `claim_text` (the warrant word is found in the source's saved text, which `named_in_text` accepts), written for real | accepted; the row's `claimed_value` reads `14.75`, `comparator` `=`, `claimed_unit` `%`, `figure_role` `derived`; two `derived_from` edges; `v_derived_figure_check` has a row for it with `stored == recomputed` | red (R3) |
| T063-01 | delta re-pointed at a written `>=` row (`numbered("delta", "9.25", comparator=">=")` under a new sentence) and base `=` | refused; `is not a bound` | red (R3 first) |
| T063-02 | base `>=` 5.5 and delta `=` 9.25 | accepted; stored comparator `>=` | red |
| T063-03 | delta written in `mm`, base in `%` | refused; `stated in` both units, nothing written | red (the old refusal asks for `--conversion-note`) |
| T063-04 | a base with no locator: HAND `UPDATE … SET source_section=NULL, loc_section=NULL` on a copy of the base row | refused; `R3: derived figure's input` | red |
| T063-05 | `inspect.signature(db.derive_extraction)` | has no `comparator`, `claimed_unit` or `conversion_note` parameter | red |
| T016-N11d, N11e | delete both (their blockers are gone); say so in the pull request | — | — |

*2b. The mutations* (harness in `$SCRATCH/t063-mutations.py`, the shape T-017 section 6 step 2b describes): M1, in `_derived_comparator`, `if delta_cmp == "=" and` → `if True and` → T063-01 KILLED; M2, delete the unit-equality refusal → T063-03 KILLED; M3, make the input-locator check a no-op → T063-04 KILLED.

*2c. The rest.* `python3 scripts/audit/extraction_relations_integrity.py` on the canonical database: unchanged (no derived row exists). `build_graph.py --check` after, compared with before.

**Writing the test.** Case ids `T063-01`, …, confirmed free. Never type into a test an id the database can derive. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-`. Compare: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number changes only by the cases added and deleted.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run it once, in the background, when every edit is made; never `--all`; read the `RESULT` line, any `NOTHING-IN-SCOPE`, any blocking `FAIL`. `research_tooling_separation` reads `origin/main`: run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and treat a gate FAIL that disappears with `--base` as not yours. A check already red before your change tells you nothing about your diff: name it with its before and after lines.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: derive-extraction writes a derived figure (comparator and unit from its inputs) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the delegated resolution of OD-40 and its ledger lines (the resolution, its status and its check), what changed, the evidence before and after, the callers and what was done to each>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start while section 2's gate prints CLOSED for OD-40, and do not implement an answer other than the one recorded (a delegated resolution, never the owner's words).
- Do not write `data/guidebook.db` directly. This task has no migration and writes no derived row outside a test's scratch copy.
- Do not weaken the verbatim floor or R3 for any row other than a `derived` one, and not beyond what the recorded answer says.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine. Do not author synthesis prose.
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it.
- Do not add a table, column, check, verb or script that section 4 does not name. Fixing a caller the sweep finds is in scope.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- section 2's gate prints CLOSED for OD-40 (the owner has reversed it, a correction has withdrawn it, or its independent check is not recorded), or the recorded resolution adds a condition this file does not cover;
- a precondition in section 2 is not met;
- the evidence command in section 3 does not give today's expected output;
- the red test is not red before the change, or is not green after it, after one honest attempt;
- a derived row is written on the scratch copy whose `v_derived_figure_check` row disagrees, or that the view does not list;
- the sweep finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run;
- `sha256sum data/guidebook.db` changes;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request. Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff. One pass.
2. Run `/batch-done`.
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the delegated resolution of OD-40 and its ledger lines; the problem; the evidence before and after; each caller and what was done to it; each check's `EXAMINED:` line before and after; the code-size line; what was not verified; a heading "Task-file defects". End with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it. The final push is never `[skip ci]`.
5. One pull request merges at a time; take a merged predecessor with `git merge "$BASE"` (never rebase).
