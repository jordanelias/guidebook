# T-017  The prior workplan's T-2: conditions become branches

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-017-report.md`, patch `.../T-017.patch` (stacked on the T-008 and T-016 pilots); defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-017 |
| Title | The prior workplan's T-2: conditions become branches |
| Wave | 1 (chain) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | prior workplan T-2 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-016 merged (it in turn needs T-008 and T-014; section 6 runs T-014's stress harness and its `stress_diff.py`). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** the cases of section 6 step 2a marked red are red on the unchanged code (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-017-wp-t2-conditions "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-017" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

A value that holds only under a condition (a short rise, an alteration) is composed into the headline as if it held everywhere. The owner ruled that such claims are shown as branches beside a headline taken only from unconditioned claims, and that the headline is empty when every claim is conditioned (OR-2: `grep -n -F 'Branches, and an empty headline' references/project-standards.md`).

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only):

```
sed -n '/\*\*T-2 Conditions/,/Code +35/p' workplan/2026-10-23-pipeline-resolution-workplan.md
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print("condition_on edges:", c.execute("SELECT COUNT(*) FROM extraction_relations WHERE relation='condition_on'").fetchone()[0])
# C20's second query: edges FROM a value-supplying, non-skimmed row (a row that can govern), and their parameters
print("from governable rows (count, parameters):", c.execute(
    "SELECT COUNT(*), GROUP_CONCAT(DISTINCT x.parameter_id) FROM extraction_relations r JOIN source_value_extractions x "
    "ON x.extraction_id=r.from_extraction_id WHERE r.relation='condition_on' AND x.figure_role IN ('claim','derived') "
    "AND x.extraction_method <> 'skim'").fetchone())
for row in c.execute("SELECT a.figure_role, a.extraction_method, b.figure_role, COUNT(*) FROM extraction_relations r "
                     "JOIN source_value_extractions a ON a.extraction_id=r.from_extraction_id JOIN source_value_extractions b "
                     "ON b.extraction_id=r.to_extraction_id WHERE r.relation='condition_on' GROUP BY 1,2,3"):
    print("  from", row[0], row[1], "-> to", row[2], ":", row[3])
PY
```

**Expected output today:** the workplan paragraph for T-2; a non-zero count of `condition_on` edges; a **non-zero** count of edges from governable rows, all on one parameter on 2026-11-13 (parameter 12, whose run-length claims point at gradient rows of parameter 3); and the direction breakdown, in which edges run both from condition rows to claims (the relaxation shape) and from claims to condition rows (the conditioned-claim shape this task acts on).

**The 2026-10-22 report's premise is stale, and that is not a stop.** The report (section 4) and the prior workplan's done-when say "no governing row has an outgoing `condition_on` edge today … C20's governing-edge query must print `0` before and after" and "7 of the 10 live edges run the other way" (its A-11). Later research added claim rows with edges in the conditioned direction, so the second count is no longer 0 and this task **does** change what the engine says about a live parameter: its governing rows with an outgoing edge leave the headline and become branches. Section 6 step 2c states the expected before and after.

If the output differs from the above in any other way, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-13; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

**This section is the whole change; you do not need to open anything else to execute it.** It was extracted from T-2 in `workplan/2026-10-23-pipeline-resolution-workplan.md` and from the T-2 section of `scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md` (its steps 1 to 3, tests B1 to B6, mutations M7 and M8, Appendix C's C20, C32 and C36, section 6.2's regression suite and section 7.1's K-11), with the pilot's corrections. If you do open that report, these parts of it **do not apply** and this file overrides them: its common protocol (§3.0, P-1 to P-10: a branch `claude/<pr-slug>` from `origin/main`, writing `scratchpad/CURRENT` and running `preserve_transcripts.py` in a pilot, the gate as `preflight.sh` plus a separate `run_checks.py --changed-from origin/main` and `--selftest`, a mutation harness under `scratchpad/$STEM/`, its net-negative statement and stock exception text (CLAUDE.md §8 has no net-negative requirement), its commit subject, its second "session command log" commit, the attribution lines and session link it prints, and its pull-request steps; sections 2, 4 (code size), 6, 7 and 11 here govern those); its T-2 acceptance line "C20's governing-edge query prints 0" and the claim behind it (section 3); its OR-2 "strictest branch" alternative (the owner chose the empty headline); its instruction to extend `synth_db` with an `edges=()` argument (the tests below build the table per case); its test-section name "B (T-2)" in `scripts/tests/test_db_amend_writers.py` (that file has no such section); its B4 (it cannot go red on its value: section 6); its sentence that `derivation_sha` does not move (it moves, item 2); its `regress_2026-10-22.sh` as printed (it passes `--slug stress-test`, which the engine now refuses: "no such slug"; section 6 step 2c replaces stages 1 and 2, and T-014's harness replaces stage 7); and its size estimate. Locate code by symbol, never by line number.

1. **The partition, in `scripts/assess/assess_cell.py`.** Rename the existing `def compose_value(conn, links, direction):` to `def _compose_headline(conn, links, direction):`, leaving its body and its long docstring exactly as they are, and insert directly above it this new `compose_value`, which is now the only caller of `_compose_headline` (`git grep -n 'compose_value(' -- scripts` shows the one call in `determine`, which keeps its name):
   ```python
   def compose_value(conn, links, direction):
       """The determination's value from its HEADLINE claims; conditioned claims are branches (OR-2).

       A governing claim with an outgoing `condition_on` edge holds only under that condition
       (migration 075: "this figure only holds given a second figure"), so it is a branch beside the
       headline, never part of it (owner, OR-2: "Branches, and an empty headline when all are
       conditioned"). The edge points FROM the conditioned claim: an edge ARRIVING at a row conditions
       nothing (the relaxation rows point at the general claim they relax; reading them the other way
       would push the general claims out of the headline). Link roles are unchanged, so a conditioned
       row stays `governing`. Every note returned, a decline included, says how many claims are
       branches: a decline computed over the headline alone is otherwise read as a statement about
       every governing claim. Returns what `_compose_headline` returns."""
       gov = {l["extraction_id"] for l in links if l["role"] == "governing"}
       conditioned = set()
       if gov and _table_exists(conn, "extraction_relations"):
           conditioned = {r[0] for r in conn.execute(
               "SELECT from_extraction_id FROM extraction_relations WHERE relation = 'condition_on'")} & gov
       headline = [l for l in links
                   if not (l["role"] == "governing" and l["extraction_id"] in conditioned)]
       if conditioned and not any(l["role"] == "governing" for l in headline):
           return None, None, None, (f"piecewise only: all {len(conditioned)} governing claim(s) are "
                                     f"conditioned (condition_on); the branches are the answer"), None
       vmin, vmax, unit, note, notations = _compose_headline(conn, headline, direction)
       if conditioned:
           note = ((note + "; ") if note else "") + (
               f"{len(conditioned)} conditioned claim(s) are branches, not the headline")
       return vmin, vmax, unit, note, notations
   ```
   Chosen (fold 2026-11-13, pilot defect 8): the branch count is appended on **every** return path, the declines included. The report's sketch appended it only on the composed path, so on the live data the parameter whose claims are conditioned kept a note saying "governing claims are stated in different units" with no word that most of its governing claims had been set aside. A wrapper does this in one place instead of at each of `_compose_headline`'s returns. `_compose_headline`'s docstring sentence "Returns (value_min, value_max, value_unit, note)" undercounts its own five-tuple; correct it to name the fifth element (`notations`) while you are there.
2. **`RULE_VERSION`: a label bump, derived.** The partition changes what the engine answers for the same links, so the label changes. Derive the next label at branch time, and again after any `git merge "$BASE"` (section 11 item 5); never type it from this file:
   ```
   git fetch origin
   python3 -I - "$BASE" <<'PY'
   import re, subprocess, sqlite3, sys
   git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
   others = git("log", "--remotes", "--not", "HEAD", "-p", "-G^RULE_VERSION = ", "--", "scripts/assess/assess_cell.py")
   on_base = git("show", f"{sys.argv[1]}:scripts/assess/assess_cell.py")
   stored = " ".join(v or "" for (v,) in sqlite3.connect("file:data/guidebook.db?mode=ro", uri=True).execute(
       "SELECT DISTINCT rule_version FROM specifications"))
   used = {int(n) for n in re.findall(r'RULE_VERSION = "pilot-(\d+)"', others + on_base) + re.findall(r"pilot-(\d+)", stored)}
   print("on $BASE:", re.search(r'^RULE_VERSION = "([^"]+)"', on_base, re.M).group(1), "| next: pilot-%d" % (max(used) + 1))
   PY
   ```
   It takes the next number above every label it can see: the one on `$BASE` (which includes T-008's and T-016's bumps once they are merged), any label assigned on a fetched remote branch that your branch does not contain (so a bump another execution pushed first is seen before it merges), and every label stamped on a stored determination. Your own branch's bump is excluded (it is in `HEAD`), so re-running it after you set the label, or after a `git merge "$BASE"`, prints the same next label unless someone else has taken it; if it then prints a different one, set that one. On 2026-11-13 it printed `on $BASE: pilot-4 | next: pilot-5`; the pilot used `pilot-5` only because neither stacked pilot had bumped. Set `RULE_VERSION` to the printed next label and put this above the existing comment block: `# <next label> (T-017, prior workplan T-2): conditioned governing claims are branches, not the headline (OR-2). Payload format unchanged; K01/K02 read this label as a link-set version.` Leave `LEGACY_SHA_VERSIONS = ("pilot-2",)` in the integrity test as it is: its own comment says a bump that leaves the payload alone needs no edit there.
   - **Consequence: every `derivation_sha` moves.** The label is in the sha payload (`grep -n '"::" + RULE_VERSION' scripts/assess/assess_cell.py`), so the same cell determined before and after this change carries a different sha even where its value, note, state and marker are identical. These readers must not treat that as a defect: the stress harness diff (section 6 step 2e), the every-parameter comparison (step 2c), the emitted SQL of any engine run, and any later pull request that compares shas across this bump. These are unaffected and must stay green: K01 and K02 in the integrity test (each row is verified against its **own** stored `rule_version`); C35's determinism (two runs of the same code). `stale_determinations` (read by `derivation_handshake_integrity`) compares only live rows stamped with the current label, so rows stamped with the old label leave its subject: none is live on the canonical database (`SELECT COUNT(*) FROM specifications WHERE retired_at IS NULL`), and a live one would be re-determined by retire-and-run, never re-labelled.
3. **The refusal, in `scripts/db.py` `_write_relation_edge`.** Inside the `if has_row:` block, directly after the two lines `if relation == "confirms":` / `_refuse_live_confirmation(conn, context, to_extraction)`, at the same indentation as that `if` (a `condition_on` must have a row referent, so the guard belongs where the row is known):
   ```python
           if relation == "condition_on" and dbcore.live_determinations_linked(
                   conn, from_id, governing_only=True):
               raise Refusal(
                   f"{context}: extraction {from_id} governs a live determination; a condition_on edge "
                   f"from it would move it out of that headline without re-deciding it. Retire the "
                   f"specification first (db.py retire-specification), add the edge, re-determine. "
                   f"Nothing was written.")
   ```
   An edge **to** a governing row from a condition row (the relaxation shape) is not refused: it changes what a render shows, never the stored answer. The refusal is reached by `relate-extraction`, `add-extraction --relation` and `derive-extraction` (all through `_write_relation_edge`); for the last two the new row cannot yet govern anything, so only `relate-extraction` can trip it.
4. **Tests**, in `scripts/tests/test_assess_cell_pilot.py` (T017-B1, B2, B3, B3b, B4, B7) and `scripts/tests/test_db_amend_writers.py` (T017-B5, B6): the full cases and their code are in section 6 step 2a.

**What reads what this task adds or changes:** `determine()` (the engine) reads `compose_value`; `relate-extraction` reads the new refusal; the render of the branches (a later task) reads the edges, not anything stored here. Nothing is replaced or made deletable.

**Code size.** Report in the pull request the output of the command below (run it after `git add` and before the commit, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. It measures from the point where your branch left `$BASE`, unless T-016's commit is on your branch but not in `$BASE` (a stacked run, as in the pilot, where the merge-base also counted T-008's and T-016's work); it then measures from T-016's commit, so only this task is counted:

```
T016=$(git log -1 --format=%H --fixed-strings --grep="governance: execute workplan T-1a reading" HEAD); FROM=$(git merge-base HEAD "$BASE")
[ -n "$T016" ] && ! git merge-base --is-ancestor "$T016" "$BASE" && FROM="$T016"
git diff --cached --shortstat "$FROM" -- scripts schemas .github skills ':!scripts/migrations'
git diff --cached --shortstat "$FROM" -- scripts schemas .github skills ':!scripts/migrations' ':!scripts/tests'   # non-test code alone
```

## 5. Caller sweep

Names to sweep: `condition_on`, `RULE_VERSION`, `compose_value`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records; T-014's harness under `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/` is run in section 6, not edited: it passes no argument this task changes).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. This task adds a refusal, so run it. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours (the pilot saw the same count and identical sorted output). An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-13, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `condition_on`: code and skills: `scripts/audit/extraction_relations_integrity.py` (reads the edges to find orphan conditions: a mention, its verdict is run in section 6), `scripts/db.py` (yours), `skills/connection-discovery_SKILL.md` and `skills/run-pipeline_SKILL.md` (describe filing the edge; still true: mentions). After T-016 merges, also `scripts/dbcore.py` (`unit_refusal`'s sentence telling the writer to put a condition in its own row) and `scripts/tests/test_run_pipeline_refusals.py` (T-016's cases): both mentions. Views, triggers, indexes: the table `extraction_relations` only. Registry: none. Prose: `governance/pipeline-contract.yaml` (mentions; one sentence there says the relations "have no writer yet", which has been false since the writer existed: not this task's, leave it).
- `RULE_VERSION`: `scripts/assess/assess_cell.py` (yours), `scripts/tests/test_assess_cell_pilot.py` (imports it; a caller that needs no edit), `scripts/tests/test_db_integrity.py` (a comment that a payload-preserving bump needs no edit there: a mention). Prose: none.
- `compose_value`: `scripts/assess/assess_cell.py` (the call in `determine` and three comments that name it: still true) and `governance/evidence-architecture.md` (names `assess_cell.compose_value()` as where most-accommodating selection landed; still true, the selection now sits in `_compose_headline` behind it: a mention).

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_assess_cell_pilot`, `test_run_pipeline_refusals`, `test_scan_contract`, `test_validate_evidence_state_2_4`, `test_db_amend_writers` (this task adds cases to it), `test_db_integrity` (K01 and K02 read the rule-version label), `extraction_relations_integrity` (reads the `condition_on` edges). Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_assess_cell_pilot test_run_pipeline_refusals test_scan_contract test_validate_evidence_state_2_4 test_db_amend_writers test_db_integrity extraction_relations_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`), except two that never print one: `test_assess_cell_pilot` (count its `PASS:` lines: `grep -c '^ *PASS:' "$SCRATCH/before-test_assess_cell_pilot.txt"`) and `test_validate_evidence_state_2_4` (it prints `ALL PASS (0 failed)` and `[PASS]` lines); report those counts as their subject. A check that is red here was red before you touched anything (on 2026-11-13 `test_scan_contract` failed two cases, G01 and G02): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. Also run `python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/before-graph.txt" 2>&1` (section 5).

**Step 2: red before, green after.** Done when every item below is run and shown in the pull request. Begin each block with the `BASE=` and `export SCRATCH=` lines, and `ST=scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress`.

*2a. The tests, written before the change and run on the unchanged code.* Confirm the prefix is free: `grep -c '"T017-' scripts/tests/test_assess_cell_pilot.py scripts/tests/test_db_amend_writers.py` prints 0 for both. The ids keep the report's B-numbers behind the task prefix; B3b and B7 are the pilot's and this fold's additions.

In `scripts/tests/test_assess_cell_pilot.py`, inside `main()`, directly after the `expect("COMPOSE: a claim stating no number is REPORTED, not silently dropped", …)` call. The fixtures use tier-1 clinical sources: with two tier-6 rows the cell is `pending` and every value is `None`, so a case would fail on both the unchanged and the changed engine (the pilot hit this). Each fixture table is built per case; `synth_db` is not changed.
```python
    # T-017 (OR-2): a governing claim with an outgoing `condition_on` edge is a branch, never the
    # headline. Each row is (value, unit, comparator, conditioned?); a conditioned row gets an edge to
    # a `condition` row of ANOTHER parameter, the shape the live edges have. `reverse` points the edge
    # the other way, the relaxation shape: an edge arriving at a row conditions nothing.
    # Tier 1 clinical, so a single source can state the cell (two tier-6 rows leave it pending).
    def _t017_cell(rows, direction="lower_is_better", reverse=False):
        c = synth_db([{"tier": 1, "evidence_type": "clinical", "claimed_value": v,
                       "claimed_unit": u, "comparator": k} for v, u, k, _c in rows],
                     direction=direction)
        c.executescript("CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY "
                        "AUTOINCREMENT, from_extraction_id INT, relation TEXT, "
                        "to_extraction_id INT, to_label TEXT, input_role TEXT)")
        for v, _u, _k, cond in rows:
            if not cond:
                continue
            gid, ref = c.execute("SELECT extraction_id, ref_id FROM source_value_extractions "
                                 "WHERE claimed_value = ?", (v,)).fetchone()
            cid = c.execute("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
                            "claim_type, claimed_value, claimed_unit, figure_role, comparator) "
                            "VALUES (?, 'syn-slug', 2, 'numerical', '0.5', 'm', 'condition', '>')",
                            (ref,)).lastrowid
            c.execute("INSERT INTO extraction_relations (from_extraction_id, relation, "
                      "to_extraction_id) VALUES (?, 'condition_on', ?)",
                      (cid, gid) if reverse else (gid, cid))
        return determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "t017")
```
Then one `expect(...)` per row of this table, with the detail string showing `value_min`/`value_max` and `value_note` (`R = "rise:run ratio"`; each row value is distinct, because the helper finds a row by its value):

| id | rows (value, unit, comparator, conditioned) | direction | expect after the change | on unchanged code |
|---|---|---|---|---|
| T017-B1 | `("1:12", R, "<=", False)`, `("1:20", R, "<=", True)` | lower | `value_max` equals `100/12` (within 1e-9); note contains `1 conditioned claim(s)` | red (`5.0`, the conditioned 1:20) |
| T017-B2 | `("1:6"…)`, `("1:10"…)`, `("1:12"…)`, `("1:16"…)`, `("1:20"…)`, each `R, "<=", True` | lower | `value_max is None`; note starts with `piecewise only` | red (`5.0`) |
| T017-B3 | B1's rows, neither conditioned (control) | lower | `value_max == 5.0`; `conditioned` not in the note | green |
| T017-B3b | B1's rows with `reverse=True` (the relaxation shape, report K-11) | lower | `value_max == 5.0`; `conditioned` not in the note | green (red under M10) |
| T017-B4 | `("1200", "mm", ">=", False)`, `("1500", "mm", ">=", True)` | `higher_is_better` | `value_min == 1200.0`; note contains `1 conditioned claim(s)` | red (`1500.0`) |
| T017-B7 | `("600", "cm", "<=", False)`, `("9", "m", "<=", False)`, `("10", "m", "<=", True)` | lower | `value_max is None`; note contains both `different units` and `1 conditioned claim(s)` | red (no branch count) |

**Why B4 is not the report's B4.** The report's B4 (`1:15` unconditioned plus a conditioned `1:12`, expect `100/15`) cannot go red on its value: under `lower_is_better` the lowest ceiling is `1:15` with or without the edge, so only its note distinguishes the two engines. This B4 is a probe whose **value** differs (the conditioned claim is the one the most-accommodating rule would pick, under the other direction), and B7 is the note-only probe, on a decline path, stated as such.

In `scripts/tests/test_db_amend_writers.py`, in the section whose cases are numbered `G01` to `G10` (it already holds a live determination's governing row `GOV_X`, and the `unretire`/`reretire`, `linked`, `refusal`, `counts` and `q` helpers), directly after the `record("G10", …)` call. Every row is chosen by query. The accepted edge must pass the verbatim floor, so it borrows the quote of a `condition_on` edge a condition row already carries:
```python
        # T-017: a condition_on edge FROM a governing row would move it out of its live headline
        # (assess_cell.compose_value), so it is refused like a regrade; the relaxation shape, an
        # edge from a condition row TO a governing one, changes what a render shows and not the
        # stored answer, so it is not. Rows are chosen by query; the target is any condition row.
        cond = q("SELECT extraction_id FROM source_value_extractions WHERE figure_role='condition' "
                 "ORDER BY 1")
        COND_TO = next((c for (c,) in cond if c != GOV_X), None)
        COND_FROM, COND_QUOTE = next(((c, qt) for c, qt in q(
            "SELECT r.from_extraction_id, r.quote FROM extraction_relations r JOIN "
            "source_value_extractions x ON x.extraction_id = r.from_extraction_id WHERE "
            "r.relation='condition_on' AND x.figure_role='condition' AND r.quote IS NOT NULL "
            "ORDER BY 1") if linked(c, governing_only=True) == [] and c != GOV_X), (None, None))
        cedge = dict(stated="named", quote="fixture quote", dry_run=True,
                     cross_source_reason="fixture: the target is chosen by query, not by source")
        n_rel = counts("extraction_relations")
        msg_c5 = refusal(db.relate_extraction, GOV_X, "condition_on", S,
                         **dict(cedge, to_extraction=COND_TO)) if COND_TO else None
        record("T017-B5", "relate-extraction refuses a condition_on edge FROM a governing row of a "
               "live determination, naming it and retire-specification, and writes nothing",
               COND_TO is not None and msg_c5 and "governs a live determination" in msg_c5
               and "retire-specification" in msg_c5 and counts("extraction_relations") == n_rel,
               f"to={COND_TO} {msg_c5!r}")
        got_c6 = None
        if COND_FROM:
            try:
                got_c6 = db.relate_extraction(COND_FROM, "condition_on", S,
                                              **dict(cedge, to_extraction=GOV_X, quote=COND_QUOTE))
            except Refusal as exc:
                got_c6 = str(exc)
        record("T017-B6", "...but the same edge from a condition row to that governing row is accepted",
               COND_FROM is not None and isinstance(got_c6, dict), f"from={COND_FROM} {got_c6!r}")
```
On the unchanged code T017-B5 is red (the edge is accepted) and T017-B6 green; after the change both are green. If either query returns no row, the case fails with `None` in its detail: that is a missing fixture, not a pass; stop (section 9).

Run both files on the unchanged code and keep the output: the cases marked red are red, the others green. Then make the change and run them again: every case green.

*2b. The mutations.* Each must be KILLED. Write a harness to `$SCRATCH/t017-mutations.py` (not in the repository): a list of `(name, path, old, new, test)`; for each, read the file, `assert text.count(old) == 1` (if not, lengthen `old` with its neighbouring text), write the edit, run `python3 <test>` from the repository root, print `KILLED` when the exit code is not 0 and `SURVIVED` otherwise, and restore the file in a `finally`.

| id | path | old → new | test | killed by (pilot-checked 2026-11-13) |
|---|---|---|---|---|
| M7 | `scripts/assess/assess_cell.py` | `and l["extraction_id"] in conditioned)]` → `and False)]` | `scripts/tests/test_assess_cell_pilot.py` | T017-B1, B2, B4 |
| M8 | `scripts/db.py` | `if relation == "condition_on" and dbcore.live_determinations_linked(` → `if False and dbcore.live_determinations_linked(` | `scripts/tests/test_db_amend_writers.py` | T017-B5 |
| M9 | `scripts/assess/assess_cell.py` | `    if conditioned:\n` → `    if False:\n` | `scripts/tests/test_assess_cell_pilot.py` | T017-B1, B4, B7 |
| M10 | `scripts/assess/assess_cell.py` | `"SELECT from_extraction_id FROM extraction_relations WHERE relation = 'condition_on'"` → the same with `to_extraction_id` | `scripts/tests/test_assess_cell_pilot.py` | T017-B3b (and B1, B2, B4, B7) |

The harness prints KILLED four times. M10 is the reading the report's K-11 warns against (taking the relaxation edges as "this claim is conditioned").

*2c. The live data, every parameter, before and after.* This replaces stages 1 and 2 of the report's `regress_2026-10-22.sh` (whose `--slug stress-test` the engine now refuses). The slug and the lens are derived by query, never typed. Save this as `$SCRATCH/cells.sh` and run `SCRATCH="$SCRATCH" bash "$SCRATCH/cells.sh" before` on the unchanged code, then `… after` after the change; each writes only to a fresh copy under `$SCRATCH`:
```
T="$SCRATCH/cells-$1"; rm -rf "$T"; mkdir -p "$T"; cp data/guidebook.db "$T/c.db"
read SLUG LENS < <(python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('SELECT slug FROM source_value_extractions WHERE slug IN (SELECT slug FROM slugs) GROUP BY slug ORDER BY COUNT(*) DESC, slug LIMIT 1').fetchone()[0], c.execute('SELECT identity_code FROM source_value_extractions WHERE identity_code IS NOT NULL GROUP BY 1 ORDER BY COUNT(*) DESC, 1 LIMIT 1').fetchone()[0])")
for p in $(python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(' '.join(str(r[0]) for r in c.execute(\"SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1\")))"); do
  GUIDEBOOK_DB_PATH="$T/c.db" python3 scripts/assess/assess_cell.py --db "$T/c.db" --emit-sql "$T/p$p.sql" --parameter-id "$p" --slug "$SLUG" --identity "$LENS" --session session_2026-11-13-t017-cells --stamp '2026-11-13 00:00:00' > "$T/p$p.log" 2>&1 || echo "p$p rc=$?"; done
python3 -I -c "
import sqlite3,sys;c=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True)
for r in c.execute('SELECT parameter_id,state,marker,value_min,value_max,value_unit,value_note FROM specifications WHERE retired_at IS NULL ORDER BY 1'): print(r)
print('BRANCHES', c.execute(\"SELECT s.parameter_id, COUNT(DISTINCT l.extraction_id) FROM specifications s JOIN specification_extraction_links l USING(specification_id) WHERE s.retired_at IS NULL AND l.role='governing' AND EXISTS (SELECT 1 FROM extraction_relations r WHERE r.from_extraction_id=l.extraction_id AND r.relation='condition_on') GROUP BY 1\").fetchall())
" "$T/c.db" > "$SCRATCH/cells-$1.txt"; wc -l < "$SCRATCH/cells-$1.txt"
```
Then `diff "$SCRATCH/cells-before.txt" "$SCRATCH/cells-after.txt"`. No `rc=` line may print in either run. The `BRANCHES` line lists each parameter with governing rows that carry an outgoing edge, and how many; the link roles do not change, so it is identical in both files. Expected (pilot and fold, 2026-11-13, measured on the code before T-016; the notes' other text may differ after T-016):
- **Every parameter the `BRANCHES` line lists:** its `value_note` gains `; N conditioned claim(s) are branches, not the headline` with N its `BRANCHES` count, or becomes `piecewise only: …` if N is all its governing rows. Its value moves only if its unconditioned governing rows compose differently from the whole set. On 2026-11-13 that was parameter 12 alone: its headline rows are still stated in different units (`cm`, `m`, `mm`), so it still declines, its value stays NULL, and only its note changes.
- **Every other parameter:** the line is byte-identical. On 2026-11-13 parameter 3 still read `max 5.0` in `%` (its governing rows carry no outgoing edge; its conditioned rows are linked `conditioning`, not `governing`), and the others stayed `pending`.
- **Nothing anywhere:** `state` and `marker` do not change (they read the links, which this task does not change).

*2d. The engine fixtures (report C32).* Extract the fixture script from the report into `$SCRATCH` (not the repository) and run it before and after:
```
R=scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md
awk -v h="# fixtures_g1_g13.py" 'index($0,h)==1{p=1} p&&/^```/{exit} p' "$R" > "$SCRATCH/fixtures_g1_g13.py"
python3 -I "$SCRATCH/fixtures_g1_g13.py" "$PWD" > "$SCRATCH/fixtures-before.txt" 2>&1; wc -l < "$SCRATCH/fixtures-before.txt"
```
After the change, the same to `fixtures-after.txt`, then `cmp` the two: identical (its fixtures build no `extraction_relations` table, and its output holds no label or sha; the pilot saw 13 identical lines).

*2e. The stress harness of T-014 (merged before this task).* `$ST/stress_run3.py` is the harness and `$ST/stress_diff.py` compares two of its runs (T-014 section 4 items 1 and 2: it matches steps by part and tag, compares `argv`, `rc`, `stdout`, `stderr` and `changed`, and exits 1 when any field differs). T-014's own A/B/C runs characterise the harness itself (A unrepaired, B repaired, C after its `migrate_db.py` fix); this task uses only its last form, the one every later task uses: one run on the unchanged code and one after, compared. Use the two parts that run the engine and `relate-extraction`, `real` and `reentry`:
```
python3 -I $ST/stress_run3.py --out "$SCRATCH/H-before" --parts real,reentry      # unchanged code; background, long timeout; last line UNCHANGED
python3 -I $ST/stress_run3.py --out "$SCRATCH/H-after"  --parts real,reentry      # after the change
python3 -I $ST/stress_diff.py "$SCRATCH/H-before" "$SCRATCH/H-after"
```
This task has no migration, so the write-path clone's committed `HEAD` (T-014 item 1j) does not affect what is compared: no commit is needed before the after-run. The diff is expected to exit 1. Every differing field must be explained by one of these, and listed in the pull request with which one: (a) the rule-version label or a `derivation_sha` (item 2's consequence), in the `real.assess.*` and `reentry.assess-*` steps or in a step that prints a determination row; (b) a `value_note` or value change on a cell where a governing row carries an outgoing `condition_on` edge in that part's scratch database (`real.relate-extraction` files such an edge before `real.assess.*` runs, and no determination is live at that point, so that step is accepted in both runs). A differing `rc` on any step, or a field explained by neither, is a stop (section 9).

*2f. The rest.* The section 3 evidence command prints the same counts before and after (this task changes no row). `python3 scripts/audit/extraction_relations_integrity.py` prints `VERDICT: CLEAN`. `build_graph.py --check` after, compared with `$SCRATCH/before-graph.txt` as section 5 says.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T017-B1`, `T017-B2`, …) and confirm the prefix is free first (`grep -c '"T017-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (step 2a's B5 and B6 do). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason (B6 borrows a stored quote for exactly that reason: without it the persisted-artefact quote refusal stops it). Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove (B3 and B3b are controls; M10 is B3b's seeded defect).

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number (or, for the two checks named in step 1, the `PASS:` count) may only change by the cases you added (six in `test_assess_cell_pilot`, two in `test_db_amend_writers`).

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on. An advisory FAIL in the gate that is not in your before-run and reads nothing this diff touches (the pilot saw several, for example `search_log_completeness` citing other sessions' logs): run it once on `$BASE` untouched (`git stash`, run, `git stash pop`) and report both results.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: execute workplan T-2 conditions [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- Do not type the new `RULE_VERSION` label from this file or the pilot's patch; derive it (section 4 item 2). Do not add a label to `LEGACY_SHA_VERSIONS`.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not print the T-2 paragraph, or prints 0 `condition_on` edges (the relation or its rows have moved). **Not a stop:** a non-zero count of edges from governable rows, which contradicts the report's "0" and is today's expected output (section 3);
- the red test is not red before the change, or is not green after it, after one honest attempt; or a B5/B6 fixture query returns no row;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- The code and section 4 disagree about what exists (a symbol it locates is missing, appears twice, or does something other than section 4 says): stop and report; do not reinterpret the plan.
- The label derivation of section 4 item 2 fails (for example `$BASE` has no `RULE_VERSION = "pilot-N"` line: the label scheme has changed, and choosing a new one is not this task's).
- In section 6 step 2c: a parameter's line changes that the `BRANCHES` line does not list, a `state` or `marker` changes anywhere, the `BRANCHES` line differs between the two runs, or an `rc=` line prints. In step 2d: the fixture output differs. In step 2e: a differing field that neither explanation covers, or any differing `rc`.
- A mutation of section 6 step 2b survives after one honest attempt to make its case reach the code it targets.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; the derived `RULE_VERSION` label and the statement that every `derivation_sha` moves with it; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase), re-derive the `RULE_VERSION` label (section 4 item 2) and, if you carry a schema migration, derive its number again by the rule in section 4.
