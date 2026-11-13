# T-014  Keep the stress scripts as a characterisation harness and their probes as tests

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13 (dry pilot; behaviour preservation not shown, see the report): report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-014-report.md`, patch `.../T-014.patch`; defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-014 |
| Title | Keep the stress scripts as a characterisation harness and their probes as tests |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | retention (stress/RETAINED.md) in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is whichever remote branch carries the newest commit to `workplan/2026-11-12-bidirectional-pipeline/`. The `BASE=` line of the set-up block derives it (it names no branch, so a renamed or deleted workplan branch cannot make it fall silently to a stale `origin/main`; the pilot of 2026-11-13 met exactly that with the earlier line). Every command in this file uses `$BASE`, never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change. If the line prints an empty `BASE=`, stop (section 9).
- **Tasks that must be merged to the integration base first:** none. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none. This task rests on rulings already in the ledger or on no ruling at all.
- **Tests that must be red (or green) before you start:** none (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-014-stress-harness-and-probes "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-014" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

Three rounds of stress scripts found defects no check finds, and they are the only way to show that a refactor preserves behaviour. Left in a scratchpad with their known faults they will not be run again, and the next change to the writers is unproven.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
ls scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/*.py; A=scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-stress-audit.md; sed -n '/^## 4\./,/^## 5\./p' "$A" | head -20; sed -n '/^### 7\.4/,/^## 8\./p' "$A"
grep -n 'list(new)\[:5\]' scripts/migrate_db.py
```

**Expected output today:** Five scripts (`lang_probe.py`, `run_logged.py`, `stress_run.py`, `stress_run2.py`, `stress_run3.py`); the audit's section 4 table (W-1 to W-11) and its §7.4 paragraph (the reused clone, the guard probes without a locator, `raise-determination-gate` without its trigger, the merge probe on a parameter with an open gate); and two lines of `scripts/migrate_db.py`, both inside `_apply_atomically`, that print the first five items of a set (the source of the one difference two repaired runs still show; section 4 item 3).

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

`ST` below is `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress`. A probe that is refused for a reason other than the one it was written to test proves nothing, so every repair below aims each probe at the refusal (or acceptance) it names. Locate code by symbol, never by line number.

1. Fix the scripts where they are (`$ST/`):
   - a. **Reused clone.** Before each write-path clone, `shutil.rmtree(clone, ignore_errors=True)`, then clone unconditionally (drop the `if not clone.exists():` guard): in `stress_run3.py` `part_real`, and in `stress_run.py` `writepath_replay` and the cross-topic block of `main`. A reused clone keeps the previous run's migration, so the second run's rebuild fails (audit B-69).
   - b. **Locator on the quote probes.** In `stress_run3.py` `part_guards`, add `*loc_args(R.db)` to all **three** quote-variant `add-extraction` calls (`quote-extra-space`, `quote-homoglyph`, `quote-truncated`; the audit says two). With a locator, `quote-homoglyph` is still refused, now for a legitimate reason (no persisted retrieval artefact holds the altered quote); record that, it is the probe's answer.
   - c. **Probes that duplicate the anchor extraction.** The anchor (`anchor()`, the first extraction on `REF`) carries one lens; an `add-extraction` that repeats it under the same lens is refused as a byte-identical copy before any guard runs (the pilot saw this on `guards.control-exact`, `real.add-extraction.<that lens>` and `reentry.add-extraction`). Chosen (pilot 2026-11-13): (i) the guard cases (both loops of `part_guards`) take a lens derived by query, not typed: the first `identity_code` of `base_taxonomy_identity` with `status='active'`, `order by identity_code`, for which no `source_value_extractions` row exists with the anchor's `ref_id` and `parameter_id`; (ii) in `part_real`'s lens loop and in `part_reentry`, `add_ext` is skipped, with an `R.note(...)` saying the anchor already carries that cell, for any lens on which such a row already exists. The pilot typed `SCI` instead; rule 8 forbids typing a code the database can derive. Reason for skipping rather than re-aiming the real and reentry probes: the cell they meant to fill is already filled by the anchor, so the step adds nothing but a wrong-reason refusal.
   - d. **`raise-determination-gate`.** In `part_reentry`, append `--trigger-ref-id REF` (the held source) to the arguments `build_args` returns for that verb. Chosen (pilot 2026-11-13): the pointer, not `--trigger-tier` plus `--trigger-evidence-type`. `db.py` reads the tier and evidence type from the source and refuses them typed alongside it (rule 5); without a pointer it requires both typed. The audit's "omits `--trigger-evidence-type`" is half the refusal: the refusal text names both flags.
   - e. **Merge probe.** In `part_lifecycle`, replace `build_args("merge-parameter", …)` with explicit arguments: `merge-parameter --from <new> --into <into> --reason "STRESS-FIXTURE: change of grain" --session S`, where `<new>` is the parameter the part just defined and `<into>` is `select parameter_id from base_parameters p where status='active' and parameter_id<>:new and not exists (select 1 from determination_gates g where g.parameter_id=p.parameter_id and g.resolved_at is null) order by parameter_id limit 1`. `build_args` cannot do this: its `value_for` maps `--from` to an extraction id and fills `--reason` with `1`.
   - f. **Retire probe.** The following `retire-parameter` targets `<into>`, not `<new>`: once the merge succeeds, `<new>` is refused as already merged, which is a wrong-reason refusal for a probe named "retire a parameter with no open gate".
   - g. **`lang_probe.py`.** Drop `dbcore.normalise_quote_text` (loader entry, docstring line, per-string loop and collision keys): it collapses whitespace only and is not a copy of `retrieval_log.normalise_quote` (audit W-5).
   - h. **The two SQL probes in `stress_run.py`.** In `pass2_backward` (`backward.extraction-funnel`), the failing predicate is `sc.locator=l.locator` (`source_locators` has no `locator` column; it already joins on `ref_id`). Chosen (pilot 2026-11-13): join `search_candidates` by its pointer to the admitted source, `sc.resolved_ref_id=s.ref_id`. In `pass5_adversarial` (`adversarial.post-retire-state`), read `status` from `base_parameters`, not `retired_at`.
   - i. **Defaults that destroy evidence or break section 8.** In `stress_run.py` and `stress_run3.py`, make `--out` required (`required=True`, no default): the defaults are `results/` and `results3/` beside the scripts, `Run.__init__` empties each `log.jsonl` it opens, and `RETAINED.md` keeps those logs. In `stress_run3.py`, drop `batteries` from the default `--parts` (it runs `run_checks.py --battery <b> --all` ten times; section 8 forbids `--all`); the part stays callable by name.
   - j. **The repository root and the scratch root.** Chosen (pilot 2026-11-13): derive, do not parameterise. In `stress_run.py` (which `stress_run3.py` imports): `REPO = Path(__file__).resolve().parents[3]` (the scripts live inside the checkout they test, so their location is the fact; a parameter could name a tree other than the one whose code is running, and a hard-coded `/home/user/guidebook` made the 2026-11-13 pilot drive the working repository's code from a clone), and `SCRATCH = Path(tempfile.gettempdir()) / "guidebook-stress"` (it was another session's scratchpad directory). **The write-path steps clone `REPO`'s committed `HEAD`:** an edit under `scripts/` that is not committed is absent from the clone, so commit it before any run whose write-path steps must see it (section 6 step 2 does this).
2. Add ONE small script beside them, `stress_diff.py`: `python3 -I $ST/stress_diff.py <folder-A> <folder-B>`. Each folder holds `<part>/log.jsonl`. It:
   - matches steps on (part folder, tag with its running counter `.NNN.` removed, occurrence number of that name within the part); the counter shifts when a step is skipped, so matching on the raw tag reports phantom differences;
   - compares exactly `argv`, `rc`, `stdout`, `stderr`, `changed`. `expect` is not compared (it is prose written before the run), and `at`, `seconds`, `canonical_sha256` never are;
   - removes, before comparing, exactly three things: absolute paths under `/tmp/` or `tempfile.gettempdir()`; date-times `YYYY-MM-DD HH:MM[:SS]` (with a space or `T`; these are the `created_at` values and `--stamp` echoes, which is what "session stamps" meant: the session ids themselves are constant per part); 14-digit migration stamps (`20` followed by twelve digits). It has no option to remove anything else (section 9: a difference is reported, never normalised away);
   - prints `DIFF <part> <step> [<field>]` with a few lines of unified diff for each differing field, `DIFF <part> <step>: present only in A|B` for an unmatched step, then `EXAMINED: <steps> step(s) in <parts> part(s); differing fields: <n>`; exits 0 when `n` is 0, else 1.
   It lives in the scratchpad folder, not under `scripts/`: it reads nothing in the book. This is the before/after proof every refactor task cites.
3. **The one nondeterminism the repaired harness still shows is in `scripts/migrate_db.py`.** In `_apply_atomically`, both the ERROR branch and the WARNING branch print `list(new)[:5]`, the first five of a `set` of `PRAGMA foreign_key_check` tuples, so which five appear depends on hash order (and `-I` ignores `PYTHONHASHSEED`, so it cannot be pinned from outside). Two unchanged runs of the repaired harness differ in `real.migrate-rebuild [stderr]` for that reason alone (pilot run4 against run5). Chosen (pilot 2026-11-13): replace both with `sorted(new, key=repr)[:5]`. Sort at the source rather than declare the line noise in `stress_diff.py`: it is one expression at each of two sites, it makes `migrate_db.py`'s output reproducible for every reader (CI logs, the message `migration_reproducibility.py` relays), and an exemption in the diff would hide a real change in which violations are printed. `key=repr` because a `foreign_key_check` row can carry a NULL rowid (a WITHOUT ROWID table), and `repr` keeps the order total. The return value (`new`, a set), the counts printed and every exit code are unchanged. This is the only change under `scripts/`; it is Layer 0 tooling, so it belongs in this tooling pull request (rule 10).
4. Move nothing into `scripts/tests/` here. The probes that become permanent tests are written by the tasks whose defect they prove (T-008, T-009, T-010, T-011, T-006, T-007) so that each is red before its fix.

**What reads what this task adds or changes:** every later task that claims to preserve behaviour reads `stress_diff.py`'s output on two harness runs; every reader of `migrate_db.py`'s stderr reads the sorted examples.

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count; it shows only the `migrate_db.py` change, since the rest is under `scratchpad/`), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `stress_run`, `lang_probe`, `_apply_atomically`, `FK violations`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base (pilots counted 109 failures, so 109 is the base state, not yours); only a number above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `stress_run`: no file. The name does not exist yet, or lives only in the excluded paths.
- `lang_probe`: no file. The name does not exist yet, or lives only in the excluded paths.
- `_apply_atomically` (added 2026-11-13, re-run 2026-11-13): `scripts/migrate_db.py` only (the function, its callers in the same file and its `--selftest` cases). The callers use the returned set, which does not change; the selftest is run before and after (section 6 step 1).
- `FK violations` (added 2026-11-13): code, `scripts/migrate_db.py` only; prose, `references/audits/ecosystem-audit-2026-05-10.md` and `references/audits/ecosystem-resolution-summary.md` (mentions: neither states which examples are printed). `scripts/audit/migration_reproducibility.py` relays `migrate_db.py --rebuild`'s output in its message without parsing it: a mention.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** The only file under `scripts/` this task changes is `scripts/migrate_db.py`; the registered checks that run it are `migration_reproducibility` (blocking) and `migration_reproducibility_deep` (advisory), and its own `--selftest` is unregistered. (An earlier version of this file named seven `db.py` and engine tests here; the pilot showed none of them reads anything this task changes, so their before/after equality proved nothing, and they are dropped.) `migration_reproducibility.py` reuses a cached rebuild keyed on the migration files only, so a change to `migrate_db.py` itself would not be exercised: delete the cache before each run. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="migration_reproducibility migration_reproducibility_deep"
rm -f "$(python3 -c 'import tempfile;print(tempfile.gettempdir())')"/guidebook-repro-*.db
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
python3 scripts/migrate_db.py --selftest > "$SCRATCH/before-migrate_db-selftest.txt" 2>&1; echo "selftest rc=$? | $(grep RESULTS "$SCRATCH/before-migrate_db-selftest.txt")"
```

Each line shows the check's subject (`EXAMINED:` or, for the selftest, `RESULTS:`). A check that is red here was red before you touched anything: record it and carry on. A check that prints neither line, or `EXAMINED: 0`, examined nothing: say so in the pull request. These run full rebuilds and take minutes: run the loop in the background with a long timeout.

**The red test for section 4 item 3, also before any edit.** Rebuild twice from the unchanged tree and compare the stderr:

```
for i in 1 2; do GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 -I scripts/migrate_db.py --rebuild "$SCRATCH/rb$i.db" > /dev/null 2> "$SCRATCH/rb$i.err"; done
grep -c 'FK violations' "$SCRATCH/rb1.err"; diff "$SCRATCH/rb1.err" "$SCRATCH/rb2.err" > /dev/null; echo "differ=$?"
```

Red is `differ=1` with a non-zero `FK violations` count (the five example tuples differ). If `differ=0`, run the pair once more; if it is still 0, or the count is 0 (the warning no longer fires, so nothing exercises the print), the red cannot be shown: stop (section 9). Remove `$SCRATCH/rb*.db` afterwards. Section 4's repairs to the scratchpad scripts are not covered by this test; their red and green are step 2.

**Step 2: red before, green after, for the harness.** Every block begins with the `BASE` and `SCRATCH` lines of section 2 and these two:

```
ST=scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress
P=probes,real,guards,batches,lifecycle,reentry          # never batteries (section 8); always --out under $SCRATCH (the defaults overwrite retained logs)
```

Each harness run takes about a minute; `stress_run.py` takes longer. Run them in the background with a long timeout and read the files when they end; do not re-run a run because a call timed out. After each run, its last line must read `UNCHANGED` (the canonical database did not move).

1. **Write `stress_diff.py` first** (section 4 item 2); it changes nothing the runs read.
2. **Characterise the unrepaired scripts (A).** Remove the clone an earlier session may have left, then run twice:
   `O=$(python3 -I -c "import sys;sys.path.insert(0,'$ST');import stress_run;print(stress_run.SCRATCH)"); rm -rf "$O/real/clone"`
   `python3 -I $ST/stress_run3.py --out "$SCRATCH/A1" --parts $P; python3 -I $ST/stress_run3.py --out "$SCRATCH/A2" --parts $P`
   `python3 -I $ST/stress_diff.py "$SCRATCH/A1" "$SCRATCH/A2"`: red, as expected and **not** a stop: the differing fields are all `real.*` (A2 reuses A1's clone: `real.clone` present only in A1, `real.migrate-rebuild` rc 0 then 1). This is the red of item 1a.
3. **Apply section 4 item 1** (all of a to j). Then give the `batches` part its subject and exercise the two SQL probes of item 1h, which only `stress_run.py` runs:
   `python3 -I $ST/stress_run.py --topics acoustics,reach --out "$SCRATCH/R1"` (background; several minutes)
   `grep -c OperationalError "$SCRATCH"/R1/*/log.jsonl` prints 0 for every file. Without this run, `batches` logs only `batches.skip` and examines nothing.
4. **Repaired scripts, unchanged `migrate_db.py` (B).** `python3 -I $ST/stress_run3.py --out "$SCRATCH/B1" --parts $P` and the same to `B2`; `python3 -I $ST/stress_diff.py "$SCRATCH/B1" "$SCRATCH/B2"` prints exactly one differing field, `real.migrate-rebuild [stderr]` (the red of item 3, through the harness). Any other differing field: stop (section 9).
5. **Apply section 4 item 3, then commit it alone** (the write-path clone reads committed `HEAD`; section 4 item 1j): `git add scripts/migrate_db.py && git commit -m "governance: print migrate_db FK-violation examples in sorted order [$(date -u '+%Y-%m-%d %H:%M')]" -m "<attribution trailers>"`. Re-run the rebuild pair above: `differ=0` (green).
6. **Green (C).** `python3 -I $ST/stress_run3.py --out "$SCRATCH/C1" --parts $P` and the same to `C2`; `python3 -I $ST/stress_diff.py "$SCRATCH/C1" "$SCRATCH/C2"` prints `differing fields: 0` and exits 0. Any differing field is a section 9 stop.
7. **What the repairs changed.** `python3 -I $ST/stress_diff.py "$SCRATCH/A1" "$SCRATCH/C1"`: every step whose `rc` differs, and every step present in only one folder, must be one that section 4 item 1 repaired, added (the `batches` steps, now with a subject) or skipped (the duplicate-lens `add-extraction` steps of item 1c). List them in the pull request; any other `rc` change is a section 9 stop.
8. **The diff can fail.** `cp -r "$SCRATCH/C1" "$SCRATCH/S"`; with Python, change the `rc` (or `stdout`) of one step in `$SCRATCH/S/guards/log.jsonl`; `stress_diff.py` on `C1` and `S` names that step and exits 1. Restore it, change only that step's `expect`: exit 0 (by design, `expect` is not compared). `C1` against itself: exit 0.

**Writing the test.** This task writes no test file: its red tests are the rebuild pair of step 1 and the runs of step 2. Never type into a script or probe an id, a code or a count the database can derive: choose every probe by query (section 4 item 1c and 1e show the queries). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason: in C1, `guards.control-exact` must be `rc 0`; if it is refused, read why and stop if the derived lens is refused for a reason of its own (section 9).

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same block (cache deletion, loop and selftest) with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes longer than two minutes** (pilots measured over 2 in a clone). Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots: 737 paths against 6). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.
- **What the gate can and cannot see here.** It classifies the `scratchpad/` files as unclassified documentation (the pilot's gate, which saw only those, selected seven checks, none reading the change, and passed). It selects checks for `scripts/migrate_db.py`. The behaviour of the harness repairs is proved by step 2, not by the gate: say so in the pull request.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean. This task has two commits: the `migrate_db.py` change was committed alone in section 6 step 2.5 (the harness's clone must see it); this one carries the scratchpad repairs and `stress_diff.py`.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: repair stress scripts and add a normalised log diff for behaviour-preservation proofs [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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
- Do not run the `batteries` part of `stress_run3.py` (it runs `run_checks.py --all`), and never run a stress script without `--out` under `$SCRATCH`.
- Do not leave the stress scratch behind: when step 2 and the comparisons are done, `rm -rf "$(python3 -c 'import tempfile;print(tempfile.gettempdir())')/guidebook-stress"` (its clones and scratch databases hold `STRESS-FIXTURE` rows). Keep `$SCRATCH` until the pull request is written; it holds the evidence.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- the set-up's `BASE=` line prints an empty value;
- in section 6 step 2, B1 and B2 differ in any field other than `real.migrate-rebuild [stderr]`, or C1 and C2 differ in any field, or A1 and C1 differ in an `rc` that section 4 item 1 does not account for: report the field; do not hide it by normalising more (`stress_diff.py` has no option to). A1 and A2 differing in `real.*` is the expected red, not a stop.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
