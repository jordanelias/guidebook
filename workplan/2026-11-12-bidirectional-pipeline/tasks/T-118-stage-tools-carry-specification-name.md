# T-118  The specification stage's tools carry the stage's name (deferred)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` section 4, TT-7 (folded 2026-11-14; where that plan and this file differ, that plan governs, and the ledger governs both). Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the fold of the term-resolution plan (its TT-7, which named this number). **Deferred by its dependencies**, as the plan recommends: it renames objects that T-021, T-059, T-068 and T-117 edit first. The owner has ruled the naming rule but not when to apply it. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-118 |
| Title | The specification stage's tools carry the stage's name (deferred) |
| Wave | 6 (deferred: last of the term-resolution work) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class (a mechanical rename with a caller sweep; every name is derived) |
| Traces to | TERM-RESOLUTION-PLAN §4 TT-7, §1 U9; the ledger: `grep -n -F "Owner statement 2026-11-14 (last) — a stage's tools carry the stage's own name" references/project-standards.md` and `grep -n -F "Owner statement 2026-11-14 (last) — what \"determination\" means" references/project-standards.md` |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-021, T-059, T-068 and T-117 merged. T-021 widens `determination_gates` and its verb, T-059 and T-068 edit `determine` and the views over it, T-117 rebuilds `specifications`; renaming first would make each of them stale (TERM-RESOLUTION-PLAN §4: "Recommend deferring until T-068, T-059 and T-117 have landed (same files)"; T-021 added by the fold for the same reason). Check by running, for each: `git log "$BASE" --merges --format=%s | grep -c -F 'task/t-0NN-…'` with that task's file stem (lower case).
- **Owner decisions:** none in the register. The rule is the owner's ("the pipeline stage tools should match the actual name of the stage"); the defaults the term-resolution plan reads from "whatever doesn't matter" apply and are not registered: **no aliases** after the rename, the stage stays **specification**, the act is "states the ideal and grades its evidence" (resolved by default, ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`). `v_best_practice` keeps its name unless the owner answers OD-62 otherwise (OD-62 is optional and holds nothing; if it is answered "rename", stop and report, since that widens this task).
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T118-01` (section 6).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-118-stage-tools-carry-specification-name "$BASE"         # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-118" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

Internal names only: no wrong thing reaches the guidebook without this task (TERM-RESOLUTION-PLAN §4). A reader of the schema meets a second word for the specification stage's product ("determination") beside the stage's own, which the owner ruled against.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where name like '%determination%'\").fetchall())"
git grep -n -E 'def (determinations_resting_on|live_determinations_linked|raise_determination_gate|resolve_determination_gate|stale_determinations)\b' -- scripts
python3 -c "import yaml;t=yaml.safe_load(open('governance/stage-map.yaml'))['tables'];print({k:v for k,v in t.items() if 'determination' in k or 'population_match' in k})"
git grep -l -i -E 'determination_gates|v_determination_provenance|determinations_resting_on|v_open_determination_gates' -- ':!scripts/migrations/data_*' ':!scratchpad' ':!transcripts' | wc -l
```

**Output on 2026-11-14:** the table `determination_gates` and the views `v_open_determination_gates` and `v_determination_provenance`; the five functions; the stage map puts `determination_gates` in specification and `evidence_population_match` in judgment, and holds no views (so a view's stage is unjudged by it); the caller count (re-run it; the plan measured it, do not trust a figure). If the output differs, the ground has moved: stop (section 9).

## 4. The change

1. **Derive the rename set, do not type it.** From `governance/stage-map.yaml`: every table assigned to `specification` whose name carries another stage's word or "determination"; from `sqlite_master`: every view whose name carries "determination" and that reads only specification-stage tables (plus base); from `scripts/`: every function or verb whose name carries "determination" and that reads or writes those objects. Print the set with the derivation before any edit. **`evidence_population_match`** (judgment) carries "evidence", another stage's word: it is in the set the derivation prints; rename it only if the derivation shows it belongs to judgment and the new name is `judgment_population_match` or similar carrying the stage id (state the choice and the warrant in the pull request).
2. **One schema migration** renaming the tables and views (`ALTER TABLE … RENAME TO`; views dropped and recreated under the new names, with every view and trigger that names an old object recreated, derived from `sqlite_master`), the next number by `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` plus one, ending with `PRAGMA user_version`. **No aliases** (no compatibility view under the old name). A column a committed data migration INSERTs keeps working: grep `scripts/migrations/data_*` for each old name first; a data migration that names an old table is immutable, so the rebuild must replay it before the rename (an `-- AFTER_DATA:` marker; `grep -n 'AFTER_DATA' scripts/migrate_db.py`).
3. **The callers, swept** (CLAUDE.md rule 4: a view is a caller, so is a skill, so is the check registry): code, tests, `db.py` verbs and their help, skills, `.claude/commands`, `governance/check-registry.yaml` (`cmd` and `basis`), `governance/stage-map.yaml`, `governance/context-map.yaml` (regenerate it), `workplan/pipeline-state-graph/machines.yaml`, and live governance prose. Frozen workplan prose and `references/project-standards.md` are left. Verbs renamed: `raise-determination-gate` and `resolve-determination-gate` take the stage's name; no old verb is kept.
4. **Prove it.** `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"`; `python3 scripts/audit/migration_reproducibility.py --deep`; `python3 scripts/run_checks.py --selftest` (the registry's basis refs fail there on a rename: CLAUDE.md §1); `schema_reference_audit`; the UNWRITABLE derivation.

**Chosen (authoring 2026-11-14):** one migration and one sweep, after the files that edit these objects have landed (rule 8; the owner's minimise-code ruling). Rejected: renaming now with aliases (the owner's default is no aliases).

**What reads what this task changes:** every caller the sweep lists. **What wrong thing reaches the guidebook without it:** none (internal names). **What it makes deletable:** nothing; it renames.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: every old name item 1 prints, and `determination` as a whole word in `scripts/` and `skills/` (a prose use of the word for the act stays: the owner's definition says the word stands; only object names change).
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="schema_reference_audit test_assess_cell_pilot test_scan_contract test_db_integrity derivation_handshake_integrity"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
**Step 2: red before, green after.** `T118-01`: item 1's derivation prints an empty set after the change and a non-empty one before; every caller listed in section 3's last command resolves to a new name or is frozen prose. Seeded defect: leave one view under its old name; `schema_reference_audit` or the selftest goes red; restore.
**Step 3: after-run**, as step 1 with `after-`; nothing new may fail; each check's `EXAMINED:` subject unchanged.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/run_checks.py --selftest
```

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: specification-stage objects carry the stage's name [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the derived rename set; the migration; every caller and what was done; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before every dependency has merged. Do not keep an alias. Do not rename `v_best_practice` unless the owner answers OD-62 "rename" (then stop and report first).
- Do not change behaviour: a rename only. Do not edit frozen prose or the ledger.
- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: a dependency is not merged; the derivation of item 1 needs a list kept beside the stage map (rule 8); a committed data migration names an old object and the rebuild cannot replay it before the rename; the selftest or `schema_reference_audit` is red after; the rebuild does not reproduce the database; OD-62 is answered "rename".

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request, with a compensating migration (CLAUDE.md rule 3).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
