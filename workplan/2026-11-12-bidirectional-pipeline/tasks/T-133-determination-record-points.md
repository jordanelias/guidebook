# T-133  A determination's record points at the map rows it read, and a gate weighs its trigger at the source's tier today

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-133 |
| Title | A determination's record points at the map rows it read, and a gate weighs its trigger at the source's tier today |
| Wave | 6 |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); a schema migration (one junction table, one view recreated), the engine's writer of one record, two readers, tests |
| Executor | Sonnet-class (the design is stated below; stop if T-059, T-068 or T-124 left the engine's writer in another shape) |
| Traces to | the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G9); CLAUDE.md rule 5 ("A parity check is not a fix"); `scripts/audit/derivation_handshake_integrity.py` docstring items 4 and 5; the 2026-11-06 schema-shape statement (CLAUDE.md §4) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-124 merged (the last task before the first determinations that changes what the engine writes on a determination; through it T-059 and T-068). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none.
- **Tests that must be red before you start:** `T133-01`, `T133-03` (section 6).
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-133-determination-record-points "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-133" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

Two facts a determination depends on are kept as copies, each with a check that the copy still matches (CLAUDE.md rule 5: "a parity check is not a fix — it makes a dual home survivable, therefore permanent"). (1) `specifications.functional_basis` is a JSON copy of four columns of the `identity_icf_map` rows the engine read for the cell's function path (`grep -n -A8 'the function path: the promoted' scripts/assess/assess_cell.py`); the map rows retire in place (`retired_at`), so a pointer to them keeps the history the copy keeps, without a second home and without JSON in a cell. (2) `determination_gates.trigger_tier` is the tier of the gate's source copied when the gate was raised (the writer reads it from the source: `grep -n -F 'they are read from it' scripts/db.py`), and the engine's ladder-inversion guard reads the copy, so a source re-tiered since decides nothing: a grey trigger can come to pin a T1-anchored cell. `derivation_handshake_integrity` items 4 and 5 police both copies. This is the cheapest moment: no determination is live, and the first ones (T-110) follow.

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print('g.trigger_tier' in c.execute(\"select sql from sqlite_master where name='v_open_determination_gates'\").fetchone()[0]);print(c.execute('select count(*), count(functional_basis), sum(retired_at is null) from specifications').fetchone());print(c.execute(\"select name from sqlite_master where name='specification_map_links'\").fetchall())"
```

**Expected output today:** `True` (the view passes the stored tier through); every stored determination carries a `functional_basis` copy and none is live; `[]`.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **The gate's tier, read through its pointer.** Recreate `v_open_determination_gates` so that, for a gate with a `trigger_ref_id`, `trigger_tier` and `trigger_evidence_type` are the source's own (`LEFT JOIN evidence_sources e ON e.ref_id = g.trigger_ref_id`, `COALESCE(e.tier, g.trigger_tier)`, `COALESCE(e.evidence_type, g.trigger_evidence_type)`), and for a gate without one, the stated values. The view keeps its column names, so `_open_gates` in `scripts/assess/assess_cell.py` is unchanged. The stored columns stay (the table's CHECK requires them for a non-QUESTION gate, and committed migrations insert them: `git grep -l trigger_tier -- scripts/migrations`); they now record the tier stated when the gate was raised, and the view's DDL comment says so in one sentence. Delete item 5 of `derivation_handshake_integrity` (the parity check over the copy) and its test case, because nothing decides on the copy.
2. **The function path, by pointer.** One junction table, `specification_map_links (specification_id INTEGER NOT NULL REFERENCES specifications(specification_id), link_id INTEGER NOT NULL REFERENCES identity_icf_map(link_id), PRIMARY KEY (specification_id, link_id))`. The engine's writer, where it writes a determination, writes one row per `identity_icf_map` row its function path read (the `link_id`s of the query that today builds the JSON) and stops writing `functional_basis` (NULL forward: committed data migrations insert the column, `git grep -l functional_basis -- scripts/migrations`, so it is never dropped before them, CLAUDE.md rule 5). The engine's own `functional_basis` value inside the run (the returned tuple) may stay as it is for the derivation; only the stored copy goes. Readers switch to the junction joined to `identity_icf_map`: `derivation_handshake_integrity` item 4 becomes "a live determination claiming a function path has at least one junction row" (no parity), and `test_assess_cell_pilot` H3 reads the junction. A retired determination keeps its JSON as history.
3. `governance/stage-map.yaml`: `specification_map_links: specification`, with one dated history line naming T-133; `governance/evidence-architecture.md`'s sentence that every determination records `functional_basis` is corrected to name the junction (a prose caller).

**What reads what this task adds or changes:** the first determinations, which now wait for this task (T-110, its section 2 amended 2026-11-17); the engine's gate guard (through the view); `derivation_handshake_integrity` and `test_assess_cell_pilot` (the junction); `v_determination_provenance` if the sweep shows it reads `functional_basis` (then it reads the junction). `specification_map_links` spans two stages (specification to base), so it is a pointer row, not a copy.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py`. Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). A view the migration rewrites is dropped and recreated in it; list them first (`select type, name from sqlite_master where sql like '%<table>%'`). The pull request contains no `scripts/migrations/data_*` file. After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and commit the regenerated `governance/context-map.yaml` (again after your last edit to `scripts/`).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `functional_basis`, `trigger_tier`, `trigger_evidence_type`, `v_open_determination_gates`, `identity_icf_map`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you change; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention*. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`; `machines.yaml` there is hand-written and is swept); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference; it is red on the base, so only a failure line your change adds is yours. An object that returns 0 rows is unproven, not clean.

**Callers already known** (found by this file's author; each is in scope): `scripts/assess/assess_cell.py` (the writer and `_open_gates`); `scripts/audit/derivation_handshake_integrity.py` (items 4 and 5); `scripts/tests/test_assess_cell_pilot.py` (H3); `scripts/tests/test_db_integrity.py` (K01 and K02 recompute the sha: confirm the sha payload does not include `functional_basis`, `grep -n 'def sha' -A30 scripts/assess/assess_cell.py`, so `RULE_VERSION` need not move; if it does include it, stop); `governance/evidence-architecture.md`; `governance/pipeline-contract.yaml`'s `derivation-handshake` criterion (quoted by atom PIP-05).

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `derivation_handshake_integrity test_assess_cell_pilot test_db_integrity schema_reference_audit migration_reproducibility column_vocabulary_audit context_map_fresh`. Run each as the registry runs it and keep the output:

```
CHECKS="derivation_handshake_integrity test_assess_cell_pilot test_db_integrity schema_reference_audit migration_reproducibility column_vocabulary_audit context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_determination_record_points.py`, registered `test_determination_record_points` (`battery: tests`, `kinds: [tooling, schema]`, `level: advisory`, `basis: hygiene`, `no_floor: selftest — …`), on a scratch copy. `T133-01`: raise a gate citing a source (chosen by query) on a fixture parameter, then change that source's tier on the copy (an `UPDATE` on the copy, as a data migration could): the view, and the engine's gate list for a cell anchored between the two tiers, follow the source's tier today, not the stored one. `T133-02`: a gate with no source keeps its stated tier. `T133-03`: determine a fixture cell whose identity has map rows: one junction row per map row read, `functional_basis` NULL, and retiring one map row afterwards leaves the junction row pointing at a row whose `retired_at` is set (history kept). `T133-04`: `derivation_handshake_integrity` has no parity item left over either copy (`grep -c 'stored trigger is' scripts/audit/derivation_handshake_integrity.py` prints 0). Before: `T133-01` and `T133-03` red. After: green.

**Writing the test.** Case ids carry this task's prefix (`T133-01`, …); confirm it is free first (`git grep -c '"T133-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`; compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before.

**Step 4: the gate, once**, when every edit is made, before the commit, in the background with a long timeout:

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`. A FAIL on a check that was red on the base is not yours: run its `cmd` once on the base in a worktree and give both lines.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: a determination points at the map rows it read and a gate weighs its source's tier today; two parity checks deleted [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, from `date -u`.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row or any synthesis prose.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, merges, determinations) in this pull request (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb, flag or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller** the sweep of section 5 finds.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not drop `functional_basis` or `trigger_tier` (committed data migrations insert them).

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- the engine's writer, after T-059, T-068 and T-124, no longer builds the function path from `identity_icf_map` in one query, or the sha payload hashes `functional_basis`;
- a live determination exists on your base (T-110 ran first): its JSON would be a live second home; stop and report.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
