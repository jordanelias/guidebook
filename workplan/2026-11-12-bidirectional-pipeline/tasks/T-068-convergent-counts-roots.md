# T-068  A cell is convergent only on two or more independent roots

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B). **HELD: step 3 of section 4, and therefore the whole pull request, waits on owner question Q-T068 (section 2).** Its evidence commands were run on 2026-11-13 and printed what section 3 states; the shared view of item 1 was built on a scratch copy and reproduced `v_value_independence` exactly. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-068 |
| Title | A cell is convergent only on two or more independent roots |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: the engine edit is placed in code that T-059 writes and this file cannot quote, and it is held on an owner question |
| Traces to | prior workplan T-8 step 2 (`sed -n '/\*\*T-8 Roots/,/Code +60/p' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report: `sed -n '/^### T-8 roots/,/^### 3.9/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); DR-2026-07-13 H1, "precedent counts documents; evidence counts roots" (`grep -n -F 'precedent counts documents; evidence counts roots' governance/evidence-architecture.md`); the contract criterion `convergence-independence` (`grep -n -A3 'id: convergence-independence' governance/pipeline-contract.yaml`); OI-52 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`.
- **Tasks that must be merged to the integration base first:** T-059 merged (it computes whether the anchoring bounds can all hold and records `divergent` when they cannot; this task acts only on the cells where they can). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F 'task/t-059'`.
- **Owner decisions:** OD-43 (registered 2026-11-13, not yet asked; this file's Q-T068). **One owner question, raised by this authoring and not yet asked, holds step 3 and so the whole task** (until a ledger line in the owner's words answers it, do not start):
  - **Q-T068: when may the engine call a cell `convergent`?** Today it never does: with two or more evidence axes it writes `pending_assessment`, because no rule "exists for grading agreement between extracted values" (`grep -n -F 'exists for grading agreement between extracted values' scripts/assess/assess_cell.py`). The ratified definition is "Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range" (`grep -n -F 'agree on the parameter value or range' governance/evidence-methodology.md`). After T-059 the engine knows whether the anchoring claims can all hold (OR-6, OR-6b). The options: **(a)** two or more axes, anchoring claims that can all hold, and two or more independent roots among the governing figures: `convergent` (the 2026-10-22 report's T-8 step 2, its source for this option); otherwise `pending_assessment`; **(b)** as (a) but only when the axes state the same bound, so differing floors that can all be met stay `pending_assessment`; **(c)** the engine never writes `convergent`; an Opus-class synthesis session grades it, and the root condition is checked by the validator only. The rulings it rests on: OR-6b (`grep -n -F 'OR-6b: "No, the spread is printed in the note"' references/project-standards.md`) settles that differing satisfiable floors are not `divergent`, and says nothing of `convergent`; the H1 doctrine settles that roots, not documents, are counted. Under (c), section 4 item 3 is dropped, items 1, 2 and 4 stand, and the coordinator must say so in this file before it is executed.
- **Tests that must be red before you start:** T068-01 and T068-02 (section 6), on the unchanged code.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-068-convergent-counts-roots "$BASE"
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-068" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` and `export SCRATCH=…` lines.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, no `scratchpad/CURRENT`, stay on the branch you were given, stop after section 7.

## 3. The problem, in the guidebook's terms

Twenty-four codes repeating one figure are one fact about transmission, not twenty-four facts about disabled people (`governance/evidence-architecture.md` §4.5). A cell called `convergent` is rendered as "Tier 1 OT evidence and Co-1 sources converge on [claim]" (`grep -n -F '| `convergent` | Co-1-C |' governance/evidence-methodology.md`). If two sources that rest on one measurement are counted as two, that sentence launders one root into a convergence. The root registry and `v_value_independence` exist to stop this, but nothing ties a `convergent` status to the root count: the engine does not write `convergent` today, the validator checks only axes (`grep -n -F "status 'convergent' requires ≥2 evidence axes" scripts/validate_evidence_state.py`), and the prior workplan's T-8 condition is in no task (T-048 builds the registry's writer only: `grep -c -i 'distinct' workplan/2026-11-12-bidirectional-pipeline/tasks/T-048-root-registry-writer.md` prints 0).

**Evidence command** (read-only):

```
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print("convergence statuses:", c.execute("select status, count(*) from convergence_assessment group by 1").fetchall())
print("v_value_independence:", c.execute("select * from v_value_independence").fetchall())
print("roots of value-supplying rows:", c.execute("select x.parameter_id, count(distinct coalesce(x.root_ref_id, x.root_id)) from source_value_extractions x join base_parameters p using(parameter_id) where p.status='active' and x.figure_role in ('claim','derived') and x.root_type in ('measurement_primary','participatory_finding','derived_calculation') and (x.root_ref_id is not null or x.root_id in (select root_id from external_root_registry)) group by 1").fetchall())
PY
grep -n -E "conv_status = \"pending_assessment\"|status=\(\"pending_assessment\"" scripts/assess/assess_cell.py
grep -n -F "status 'convergent' requires" scripts/validate_evidence_state.py
```

**Expected output today** (2026-11-13): only `pending_assessment` rows (5); `v_value_independence` lists parameter 3 (14 roots); the value-supplying rows of parameter 3 carry far fewer distinct roots (3); two `pending_assessment` assignments in the engine; the validator's axes line. The gap between 14 and 3 is reported, not changed, by this task: the aggregate view counts the roots of condition and finding rows too (section 4, item 1, last bullet).

## 4. The change

Order of preference, from CLAUDE.md §8. **Chosen (authoring 2026-11-13): the condition is built with its only writer, not ahead of it.** Rejected: a validator rule alone, built now. Nothing writes `convergent` (section 3), so such a rule would examine no row on the live data and could only be shown red on a seeded row: an apparatus with no subject (CLAUDE.md §5(a)). The condition becomes load-bearing at the moment the engine may write the status, which is item 3, so items 1 to 4 ship together.

1. **One predicate, two readers: a row-level view, and the aggregate redefined over it.** Schema migration `scripts/migrations/NNN_value_independence_rows.sql` (number derived as below). **Chosen: this definition**, which on the scratch copy of 2026-11-13 left `v_value_independence` byte-identical (`[(3, 'ramp gradient', 14)]` before and after):
   ```sql
   DROP VIEW v_value_independence;
   -- v_value_independence_rows: one row per extraction whose root counts toward independence (DR-2026-07-13 H1):
   -- a measured, participatory or derived root, held in the corpus (root_ref_id) or registered (root_id). The ONE
   -- home of that predicate; read by v_value_independence and by assess_cell.determine (convergent needs >= 2).
   CREATE VIEW v_value_independence_rows AS
   SELECT sve.extraction_id, sve.parameter_id, sve.ref_id,
          COALESCE(sve.root_ref_id, sve.root_id) AS root, sve.root_type
     FROM source_value_extractions sve
     JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    WHERE sve.root_type IN ('measurement_primary', 'participatory_finding', 'derived_calculation')
      AND (sve.root_ref_id IS NOT NULL
           OR sve.root_id IN (SELECT root_id FROM external_root_registry))
      AND p.status = 'active';
   CREATE VIEW v_value_independence AS
   SELECT r.parameter_id, t.canonical_en AS parameter_label,
          COUNT(DISTINCT r.root) AS independent_root_count
     FROM v_value_independence_rows r
     JOIN base_parameters p ON p.parameter_id = r.parameter_id
     JOIN terms t ON t.term_id = p.term_id
    GROUP BY r.parameter_id, t.canonical_en;
   ```
   Before writing it, compare the live definition (`select sql from sqlite_master where name='v_value_independence'`) with the `WHERE` above; if they differ, stop (section 9).
   - The aggregate is not narrowed to value-supplying rows here: that changes what a reader of the aggregate is told and is not this task's. It is reported in the pull request with section 3's two figures.
2. **The validator agrees with the engine.** In `scripts/validate_evidence_state.py` `validate_convergence_db`, in the `elif status == "convergent":` branch, after the axes check: count `SELECT COUNT(DISTINCT r.root) FROM v_value_independence_rows r JOIN specification_extraction_links l ON l.extraction_id = r.extraction_id JOIN specifications s ON s.specification_id = l.specification_id WHERE s.convergence_id = ? AND s.retired_at IS NULL AND l.role = 'governing'`; fewer than two appends `f"{tag}: status 'convergent' requires >=2 independent roots among its governing figures, found {n}"`. A convergence row that no live specification points at is skipped and counted in a printed line, not passed silently. Read the link table's and the role's names from the live schema first (`PRAGMA table_info(specification_extraction_links)`); T-018 and T-019 may have changed them.
3. **HELD on Q-T068. The engine.** In `scripts/assess/assess_cell.py` `determine`, anchored branch, where T-059 has decided the anchoring claims can all hold and two or more axes are present: count the distinct roots of the governing figures through item 1's view (`SELECT COUNT(DISTINCT root) FROM v_value_independence_rows WHERE extraction_id IN (<the governing extraction ids>)`, the ids being the links `gather_extraction_links` marks `governing`). Under answer (a): two or more gives `convergent`, with a rationale that names the count; fewer keeps `pending_assessment`, with a rationale that says "fewer than two independent roots among the governing figures (n)". Under (b): as (a), adding the same-bound condition. Under (c): skip this item. The proxy branch (findings supplying direction) is untouched: it never writes `convergent`. The engine writes no synthesis prose (the report's K-5).
4. **`RULE_VERSION`: a derived label bump** (item 3 changes what the engine answers for the same links). Derive it exactly as T-017 section 4 item 2 does (its script reads every label on `$BASE`, on fetched remote branches and on stored determinations, and prints the next one); never type it from this file. Every `derivation_sha` moves with it.

**Schema migration (this task has one).** Never type a migration number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` plus one, zero-padded, ending with `PRAGMA user_version` set to it. Recreate every view that names `v_value_independence` (`select type, name from sqlite_master where sql like '%v_value_independence%'`). Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` and `python3 scripts/audit/migration_reproducibility.py --deep`. Then `python3 scripts/generate/context_map.py`, output included.

**What reads what this task adds or changes:** `determine` and `validate_convergence_db` read `v_value_independence_rows`; `v_value_independence`'s readers (`scripts/tests/test_scan_contract.py` Q9, `skills/run-pipeline_SKILL.md`) see the same rows; the render's Co-1-C sentence reads the status (T-037).

**What wrong thing reaches the guidebook without it:** a page that says sources "converge" on a figure that rests on one measurement repeated.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `v_value_independence`, `convergent`, `pending_assessment`, `RULE_VERSION`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed (for example a sentence saying the engine never writes `convergent`, or that convergence counts axes only). A hit that stays true is a *mention*. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4).

**What the sweep leaves out, and why.** `workplan/` (except the hand-written `workplan/pipeline-state-graph/machines.yaml`), `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds a view, so run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (only a count above your before-run is yours).

**Hits when this file was written** (2026-11-13): `v_value_independence`: `scripts/assess/assess_cell.py` (a comment), `scripts/db.py` (two comments), `scripts/tests/test_scan_contract.py` (Q9 reads it: run before and after), `skills/run-pipeline_SKILL.md` (a mention), `governance/evidence-architecture.md` §4.5 and `governance/pipeline-contract.yaml` `convergence-independence` (mentions: both already say roots are counted). `convergent`: `scripts/assess/assess_cell.py` (the comments at both `pending_assessment` assignments say the engine never claims `convergent`: callers under answers (a) and (b), edited to say when it does), `scripts/validate_evidence_state.py` (item 2). Re-derive `pending_assessment` and `RULE_VERSION`.

## 6. Verification

**Step 1, the before-run.** Checks that read what this task touches: `validate_evidence_state`, `test_validate_evidence_state_2_4`, `test_evidence_cell_state_2_3`, `test_assess_cell_pilot`, `test_scan_contract`, `test_db_integrity`. Run each as the registry runs it:
```
CHECKS="validate_evidence_state test_validate_evidence_state_2_4 test_evidence_cell_state_2_3 test_assess_cell_pilot test_scan_contract test_db_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
`test_assess_cell_pilot` and `test_validate_evidence_state_2_4` print no `EXAMINED:` line: count `PASS:` lines (`grep -c '^ *PASS:'`) and report that as their subject.

**Step 2, red before, green after.** Prefix `T068-`; confirm it is free in each file (`grep -c '"T068-' <file>` prints 0). Fixtures are built per case in `scripts/tests/test_assess_cell_pilot.py` the way T-017's `_t017_cell` builds them (tier 1 clinical for one axis, a verified Co-1 for the second, so two axes are present), with `root_type`, `root_ref_id` set on each row:

| id | rows | expect after | on unchanged code |
|---|---|---|---|
| T068-01 | two axes; bounds that can all hold; both governing rows rooted to the same `root_ref_id` | `pending_assessment`; rationale names fewer than two roots | red (no root wording) |
| T068-02 | as 01 but two distinct roots | `convergent` (answer a or b) | red (`pending_assessment`) |
| T068-03 | two distinct roots; bounds that cannot all hold | `divergent` as T-059 decides; unchanged by this task | green (control) |
| T068-04 | two distinct roots, but one is `committee_assertion` | `pending_assessment` (one root counts) | red under 02's mutation below |
| T068-05 | in `scripts/tests/test_validate_evidence_state_2_4.py`: a convergence row with status `convergent` and a live specification whose governing figures share one root | the validator reports the roots error | red (only axes are checked) |

**Mutations** (harness in `$SCRATCH`, as T-017 step 2b builds one): M23, the root-count comparison made always true, killed by T068-01; the view's `root_type IN (...)` widened to include `committee_assertion`, killed by T068-04; the validator's root branch disabled, killed by T068-05. Each prints KILLED.

**Live data, before and after.** Run every active parameter through the engine on a copy before and after, as T-017 section 6 step 2c does (save its `cells.sh` from that file). Under answer (a) or (b), a line may change only where the cell had two or more axes and claims that can all hold; every such change is listed in the pull request with its root count. Nothing changes under (c).

**Step 3, the after-run**: the same loop with `after-`, compared failing line by failing line. **Step 4, the gate, once**: `scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1` (background, long timeout), then `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: convergent needs two independent roots, counted from one view [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start while Q-T068 has no answer in the owner's words in the ledger.
- Do not write `data/guidebook.db` directly; only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not let the engine write synthesis prose or a synthesis approach (K-5), and do not touch Co-1 handling (T-059's held step 3).
- Do not narrow `v_value_independence` to value-supplying rows; report the gap instead.
- Do not type the new `RULE_VERSION` label; derive it. Do not hand-type a count or an id into a file, message or test.
- Do not add a table, column, check, verb or script that section 4 does not name. A caller the sweep finds is fixed here.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level.
- Do not put research rows in this pull request. Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: Q-T068 is unanswered or answered in another form; T-059 is not merged, or after it the engine has no single place where "the anchoring claims can all hold" is known; the live `v_value_independence` predicate differs from item 1's; a red test is not red before or green after; a mutation survives; a line changes in the live-data comparison that item 3 does not explain, or any `state` or `marker` changes; the rebuild does not reproduce the database; you would have to guess a value, a name or an owner's intent.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request, with a compensating migration for the views (CLAUDE.md rule 3).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base, with the derived label, the statement that every `derivation_sha` moves, section 3's two root figures, and each check's subject before and after; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change. One pull request merges at a time; after `git merge "$BASE"` re-derive the label and the migration number.
