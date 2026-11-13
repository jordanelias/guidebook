# T-075  The gate reports what each check examined, against the base it was given, and rebuilds when its inputs change

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source of the items: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 ("the registered-check and `--base` items are one small tooling task"), and the pilot reports in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/` (T-008-repilot D7 and D8, T-012 defect 3, T-013 defects 1 and 9, T-024 defects 6 and 12, T-026 defect 12, T-102 on `emit_batch_sql.py --selftest`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 from the pilots' findings; its evidence commands were run on 2026-11-13 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-075 |
| Title | The gate reports what each check examined, against the base it was given, and rebuilds when its inputs change |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-56 (registered-check and `--base` items; `NAME_TO_CODE`); CLAUDE.md §5 (a) "Every check must print `EXAMINED: <n>`"; rule 8 ("Never curate a fact the machine can compute") |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch (if its name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** none. Check by running section 3's evidence commands: they must print what section 3 says.
- **Owner decisions:** none. This task rests on CLAUDE.md §5 (a), rule 8 and §8 ("Adding a check means editing `governance/check-registry.yaml` — never a workflow"), and on no ruling that is still open.
- **Tests that must be red (or green) before you start:** none of the acceptance tests; the red cases are the ones section 6 writes.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-075-gate-reports-its-subject-and-base "$BASE"     # real execution only (see below for a pilot)
sha256sum data/guidebook.db                                # record it; this task has no migration, so it must not move
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-075" && mkdir -p "$SCRATCH"
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line.
- **Real execution:** run `/session-open` before the first command (CLAUDE.md §7), and create the branch as shown. **Pilot or dry run** (a scratch clone): do not run `/session-open`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

The gate is how a change to the writers that protect the book's rows is judged. Five things make it report less than it claims.

1. **Changeset-scoped checks diff against `origin/main`, not against the base the gate was given.** `preflight.sh --base "$BASE"` passes `--changed-from "$BASE"` to `run_checks.py`, but `run_checks.py` substitutes only `@SESSION@` into a registered `cmd` (`grep -n 'def expand' -A2 scripts/run_checks.py`), and the registered `cmd`s of the checks that take `--base` do not pass it. In every pilot `research_tooling_separation` FAILed on hundreds of paths the diff never touched and passed when run by hand with `--base`. The same holds for the four `attestation_*` checks (two of them blocking), which nobody had seen because no pilot touched a synthesis path.
2. **Registered checks print no `EXAMINED:` line**, so the vacuity guard and the stale-claim detector cannot see them (`run_checks.py`'s own selftest INFO line says so, and says "`--all` reports which", which nothing does: `grep -n "reports which" scripts/run_checks.py`). The pilots named three; the set is wider.
3. **`migration_reproducibility.py` keys its cached rebuild on the migration files only** (`grep -n 'def migrations_fingerprint' -A22 scripts/audit/migration_reproducibility.py`). The rebuild it caches is produced by `scripts/migrate_db.py`; a change to that script (how it orders, applies or checks migrations) reuses a rebuild made by the old script, and the blocking gate compares the committed database against a rebuild nobody re-made.
4. **Selftests that prove a writer or a gate can fire are not registered**, so CI never runs them (`emit_batch_sql.py --selftest` was named by the T-102 pilot; the set is wider).
5. **`validate_jurisdiction.py` carries `NAME_TO_CODE`, a hard-coded country-name list** beside `base_jurisdictions` (T-024 pilot defect 12). On the live inputs it is never consulted.

**Evidence commands** (run from the repository root; all read-only; none writes the database):

```
# (1) checks that accept --base and are not given it
python3 - <<'PY'
import yaml,re,os
for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks']:
    f=next((x for x in c['cmd'] if x.endswith('.py')),None)
    if f and os.path.exists(f) and re.search(r'add_argument\(\s*"--base"',open(f).read()) and '--base' not in c['cmd']:
        print(c['id'], c['level'], ' '.join(c['cmd']))
PY
# (2) registered checks whose script never prints EXAMINED
python3 - <<'PY'
import yaml,os
for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks']:
    f=next((x for x in c['cmd'] if x.endswith('.py') or x.endswith('.sh')),None)
    if f and os.path.exists(f) and 'EXAMINED' not in open(f).read(): print(c['id'], f)
PY
# (3) the fingerprint's inputs
grep -n 'def migrations_fingerprint' -A22 scripts/audit/migration_reproducibility.py | grep -n 'migrate_db\|listdir\|sqlite_version'
# (4) scripts with a --selftest that no registry entry runs with --selftest
python3 - <<'PY'
import yaml,subprocess
reg={(c['cmd'][1] if len(c['cmd'])>1 else '', '--selftest' in c['cmd']) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks']}
files=subprocess.run(['git','grep','-l','-E',r'add_argument\(\s*"--selftest"|"--selftest" in (_?sys\.argv)|== "--selftest"','--','scripts',':(exclude)scripts/migrations'],capture_output=True,text=True).stdout.split()
ci=open('.github/workflows/ci.yml').read()
for f in files:
    if (f,True) not in reg: print('SELFTEST NOT REGISTERED:', f, '(named in ci.yml)' if f.split('/')[-1] in ci else '')
PY
# (5) NAME_TO_CODE hits on the live inputs
python3 - 2>/dev/null <<'PY' | tail -1
import sys,io,contextlib; sys.argv=['validate_jurisdiction.py']; sys.path.insert(0,'scripts')
import validate_jurisdiction as v
class D(dict):
    hits=0
    def __contains__(s,k):
        r=dict.__contains__(s,k); D.hits+=r; return r
v.NAME_TO_CODE=D(v.NAME_TO_CODE)
with contextlib.redirect_stdout(io.StringIO()):
    try: v.main()
    except SystemExit: pass
print("NAME_TO_CODE hits:", D.hits)
PY
```

**Output on 2026-11-13** (commit `66a5ba8a`):
- (1) six lines: `claims_docket advisory … claims_docket.py check`, `attestation_presence blocking`, `attestation_schema blocking`, `attestation_evidence advisory`, `attestation_verdict informational`, `research_tooling_separation advisory`. (`claims_docket`'s `--base` may belong to its `generate` mode only; step 1 below says how to tell.)
- (2) eight lines: `validate_cross_refs`, `doctrine_recheck`, `test_graph_audit`, `test_pipeline_contract`, `test_assess_cell_pilot`, `test_evidence_cell_state_2_3`, `test_validate_evidence_state_2_4`, `test_directness_2_2`.
- (3) no line names `migrate_db` or `sqlite_version`; the fingerprint reads only the migrations directory.
- (4) twelve lines; three are named in `ci.yml` (`claims_docket.py`, `check_commit_msg.py`, `run_checks.py`); the other nine are `column_vocabulary_audit.py`, `migration_reproducibility.py`, `readonly_db_open_audit.py`, `retired_vocabulary_audit.py`, `dbcore.py`, `emit_data_migration.py`, `migrate_db.py`, `emit_batch_sql.py`, `validate_verification_consistency.py`. Each of those nine selftests printed PASS (rc 0) when run by hand on 2026-11-13; of the nine only `dbcore.py` and `column_vocabulary_audit.py` printed a line-anchored `EXAMINED:` line, so the other seven also get one under item 2's rule when they are registered (item 4).
- (5) `NAME_TO_CODE hits: 0`; `validate_jurisdiction.py` printed `PASS: 0 errors, 28 warnings` and `EXAMINED: 111` both with the dictionary and with it emptied (identical output).

If an output differs, the ground has moved: stop (section 9), unless the difference is only a smaller set (an item already fixed), which you report and skip.

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **`@BASE@`, substituted like `@SESSION@`.** In `scripts/run_checks.py`, `expand(cmd, session)` gains the base: every `@BASE@` in a registered `cmd` becomes the ref given to `--changed-from`, or `origin/main` when none was given (the default every such script already has, so a run without `--changed-from`, as CI's battery jobs make, behaves exactly as today). Thread the value from `main()` through `run_check(...)` to `expand(...)`. Then, for each check printed by evidence command (1), append `--base`, `@BASE@` to its registered `cmd` **only if the mode the registry invokes reads `--base`**: run `python3 <script> <the cmd's arguments> --base HEAD; echo rc=$?` and read the script's argparse (for `claims_docket.py check`, `python3 scripts/audit/claims_docket.py check --help`). If the invoked mode rejects or ignores `--base`, leave that entry and name it in the pull request.
   **Chosen (authoring 2026-11-13):** a placeholder substituted by the runner, rejected alternatives (a) writing a literal `--base origin/main` into the registry (it is the same defect: the gate's base is a run-time fact) and (b) having each script read an environment variable (a second convention beside `@SESSION@`, and invisible in the registry).
2. **Every registered check prints a line-anchored `EXAMINED: <n>`.** For each script of evidence command (2), print one `EXAMINED: <n>` line at the end of its run, where `<n>` is what it already counts: for a test file, the number of cases it ran (the `[PASS]`/`PASS:`/`[SKIP]` results it collected; a skipped case is not examined, so count only cases that asserted), following the shape `test_db_amend_writers.py` uses (`grep -n 'EXAMINED' scripts/tests/test_db_amend_writers.py`); for `validate_cross_refs.py`, the number of references it resolved; for `doctrine_recheck.py --cross-ref`, the number of `doctrinal_basis` references it checked. Do not change what any check asserts. A script that has no countable subject is reported in the pull request, not given a made-up count.
   Then make the runner say which run checks printed none: after the run, `run_checks.py` prints one line `NO-EXAMINED (<n>): <ids>` listing every check that ran and whose output matched neither `EXAMINED_RE` nor `NOTHING_IN_SCOPE_RE`, and prints nothing when the list is empty. It does not change any status or the exit code. Correct the selftest INFO sentence (`grep -n "reports which" scripts/run_checks.py`) to say the summary line names them.
   **Chosen (authoring 2026-11-13):** a summary line, not a FAIL. Rejected: failing a check that prints no count (the runner's own comment rejects that lever: "failing the registry for a script's output format would be the wrong lever", `grep -n "wrong lever" scripts/run_checks.py`); rejected also: a static grep of each script for the word `EXAMINED` (a comment satisfies it). After this task the line is empty on the base, so it is not red by construction (CLAUDE.md rule 6's warning).
3. **The rebuild cache keys on everything the rebuild runs.** In `migrations_fingerprint()` add to the digest the bytes of `scripts/migrate_db.py` (the script `rebuild()` runs, `grep -n 'migrate_db.py' scripts/audit/migration_reproducibility.py`) and `sqlite3.sqlite_version` (the engine that replays the SQL). Correct the two docstrings that say the migration files are the rebuild's "sole input" / "only input" (`grep -n 'sole input\|only input' scripts/audit/migration_reproducibility.py`). `migrate_db.py` imports no project module today (`grep -n '^import\|^from' scripts/migrate_db.py`); if it imports one on the day, add that file too and say so.
4. **Register the unregistered selftests** printed by evidence command (4), except those `ci.yml` already runs (leave the three named there; the workflow is not edited, CLAUDE.md §8). One registry entry per script, appended after the last entry of the same battery, in the shape of `research_dod_selftest` (`grep -n -A12 'id: research_dod_selftest' governance/check-registry.yaml`): id `<script stem>_selftest`; `cmd: [python3, <path>, --selftest]`; `battery` and `kinds` taken from the registered check that runs the same script without `--selftest` (for a script with no such entry, `battery: tests`, `kinds: [tooling]`); `level: advisory`; `basis: hygiene`; `cost: fast`; `no_floor: selftest — subject is its own fixtures, not a corpus; a floor would count the wrong thing` (the text the other selftest entries carry). A selftest that does not print `EXAMINED:` gets the line under item 2's rule in the same pull request.
   **Chosen (authoring 2026-11-13):** register the whole derived set, not only the one the pilot named: a list of one is the curated list rule 8 forbids. **Why each earns its place (CLAUDE.md §8, "state what wrong thing reaches the guidebook"):** `emit_batch_sql`, `emit_data_migration` and `migrate_db` are the write path every row of the book passes through; a regression there lands wrong rows in `data/guidebook.db` and the selftest is the only thing that exercises their refusals without a real batch. `dbcore` holds the vocabularies and refusals the writers share. The audits' selftests prove that the gate in front of a defect can go red ("a gate nobody has watched fire is not a gate", `grep -n 'watched' scripts/audit/migration_reproducibility.py`).
5. **Delete `NAME_TO_CODE`** and its one use in `resolve_jurisdiction` (`grep -n 'NAME_TO_CODE' scripts/validate_jurisdiction.py`). The vocabulary is `base_jurisdictions` (`dbcore.declared_jurisdictions()`); a full country name in an input is then reported as an unresolved code, which is what an undeclared value is. **Chosen (authoring 2026-11-13):** delete rather than derive. Deriving would need a name column on `base_jurisdictions` (a schema change and a naming decision) for a lookup that no live input uses (evidence (5)); CLAUDE.md §8: "delete the cause" comes before "add".

**What reads what this task adds or changes:** `preflight.sh` and CI (through `run_checks.py`) read the `@BASE@` substitution and the `NO-EXAMINED` line; `run_checks.py`'s vacuity guard and stale-claim detector read the new `EXAMINED:` lines; the `data` battery reads the fingerprint; CI's battery jobs run the new registry entries. **What it makes deletable:** the paragraph every task file of this plan carries about running `research_tooling_separation` by hand with `--base` (section 6, step 4, the fourth bullet); list it in the pull request for the coordinator (do not edit other task files).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it.

## 5. Caller sweep

Names to sweep: `expand(`, `run_check(`, `@SESSION@`, `migrations_fingerprint`, `NAME_TO_CODE`, `resolve_jurisdiction`, `reports which`, and each check id whose registry entry you change.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans; the task files' boilerplate is listed for the coordinator, not edited); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable); `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

**Known callers when this file was written** (re-derive): `governance/context-map.yaml` is generated from the registry and goes stale when a `cmd` changes: run `python3 scripts/generate/context_map.py` after the registry edit and include its output (every registry-touching pilot hit `context_map_fresh` otherwise). `scripts/audit/jurisdiction_db_vocabulary.py` describes `validate_jurisdiction.py` in prose (`grep -n 'validate_jurisdiction' scripts/audit/jurisdiction_db_vocabulary.py`): read it; it is a caller only if it states the name list.

## 6. Verification

**Step 1, before any edit: the before-run.** Run, as the registry runs them, every check whose entry or script you will change, plus `migration_reproducibility` and `validate_jurisdiction`; keep the output:

```
CHECKS="research_tooling_separation attestation_presence attestation_schema validate_cross_refs doctrine_recheck test_pipeline_contract test_assess_cell_pilot test_evidence_cell_state_2_3 test_validate_evidence_state_2_4 test_directness_2_2 migration_reproducibility validate_jurisdiction"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])).replace('@SESSION@',''))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
python3 scripts/tests/test_graph_audit.py > "$SCRATCH/before-test_graph_audit.txt" 2>&1; echo "test_graph_audit rc=$?"   # slow; run once before, once after
python3 scripts/run_checks.py --selftest > "$SCRATCH/before-selftest.txt" 2>&1; echo "selftest rc=$?"
```
On 2026-11-13 the eight scripts of evidence (2) printed no `EXAMINED:` line; that is the defect, not a precondition failure.

**Step 2: red before, green after.** Add cases to `run_checks.py --selftest` (next free C-number: `grep -o 'check("C[0-9]*' scripts/run_checks.py | sort -u` shows the highest) and to `migration_reproducibility.py --selftest`:
- `T075-01` `expand(["x","--base","@BASE@"], session, base="R")` returns `--base R`; with no base it returns `origin/main`. Red on the unchanged code (the placeholder is returned untouched).
- `T075-02` every registered `cmd` of a check whose script accepts `--base` in the invoked mode carries `@BASE@` (derive the set with evidence command (1)'s logic, so a new such check without it turns the case red). Seeded defect: remove `@BASE@` from one entry in a copy of the registry the case loads; the case goes red.
- `T075-03` the summary names a check that printed no count: feed the summary function one fake result whose output is `ok` and one whose output is `EXAMINED: 3`; only the first is listed. Red before (no such line).
- `T075-04` in `migration_reproducibility.py --selftest`: the fingerprint changes when the bytes of the rebuild script change. Make the script path an argument of `migrations_fingerprint` (default the real one) and call it on two temporary copies that differ by one byte; the two digests differ. Red on the unchanged code.
- `T075-05` (by hand, in the pull request) `python3 scripts/validate_jurisdiction.py` output is identical before and after the deletion (`diff "$SCRATCH/before-validate_jurisdiction.txt" "$SCRATCH/after-validate_jurisdiction.txt"` prints nothing); and a temporary copy of the standards registry holding one entry with `jurisdiction: Australia` (made under `$SCRATCH`, passed by the script's own path option if it has one; otherwise state not run) is reported unresolved after the change and resolved before it.
- For each script given an `EXAMINED:` line, show the line in the after-run with a non-zero number, and show it drop by one when you comment out one case (then restore it).

**Writing the test.** Case ids prefixed `T075-` (confirm free: `git grep -c 'T075-' scripts/` prints nothing). Never type a count the code can derive. A new case must be able to fail: show it red on the unchanged code or on a seeded defect that you then remove.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Compare check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before. Then run each new `*_selftest` registry entry once through `python3 scripts/run_checks.py --battery <its battery> --kinds tooling` only if it is cheap; otherwise run its `cmd` directly, and record each rc and `EXAMINED:` line.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST|NO-EXAMINED)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- Run it once, when every edit is made, in the background with a long timeout. This task is the one that makes `research_tooling_separation` read `$BASE`: in this run it must print `Changeset vs $BASE` (or the equivalent line naming your base), not `origin/main`. Quote that line in the pull request.
- Read the `RESULT` line, every check under `NOTHING-IN-SCOPE`, every blocking `FAIL`, and the new `NO-EXAMINED` line (it should name none of the checks this task fixed; any it names is reported).
- **The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: the gate reports each check's subject against its own base [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the five items; evidence before and after; callers found; the checks fixed with their EXAMINED lines; the entries whose --base mode was not applicable>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db`. This task has no migration.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not edit `.github/workflows/*` (a check is added in the registry, never in a workflow).
- Do not change what any check asserts, its `level`, its `min_items` or its `no_floor` reason, other than the `cmd` of item 1 and the new entries of item 4. Do not quarantine a check.
- Do not add a name column or any other schema change for jurisdictions (item 5 deletes; it does not derive).
- Do not hand-type a count; write the command.
- Do not edit another task file; list what item 1 makes stale for the coordinator.
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity.

## 9. Stop conditions

Stop, change nothing further, and report when:
- an evidence command prints a larger set than section 3 states, or a different kind of hit (a new hit is a new item to judge, not one to absorb silently);
- a newly registered selftest is red on the unchanged base (register nothing red: report it);
- a script of item 2 has no subject you can count without changing what it does;
- giving `--base` to an attestation check changes its verdict on `$BASE` itself in a way you cannot explain from the diff (the two blocking entries gate synthesis paths);
- a check green in the before-run is red in the after-run;
- `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request. Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff.
2. Run `/batch-done`.
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller and what was done; each check with its `EXAMINED:` line before and after; the code-size line; what was not verified; the list of task-file paragraphs made stale (item 1). End with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time; take a merged predecessor with `git merge "$BASE"` after `git fetch origin` (never rebase).
