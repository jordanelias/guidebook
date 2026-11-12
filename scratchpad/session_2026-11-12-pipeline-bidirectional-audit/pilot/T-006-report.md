# T-006 pilot report: `delete-connection` refuses an id that is not a row

## Verdict

**Did the task file suffice: YES, with small defects (none blocked completion).** Every executable step ran as written, the red test was red before and green after, the gate passed, the canonical database did not move. Clone: `/tmp/claude-0/pilot/T-006`, branch `pilot-T-006`, commit `722d1ed` (not pushed, no PR, no adversarial pass).

Headline: before, `delete-connection --con-id CON-9999` printed `{"deleted": "CON-9999", "dry_run": false}` and exited 0; after, it prints `REFUSING: delete-connection: CON-9999 is not a connection. Nothing was written.` and exits 1. Deleting a real connection still works.

## BEFORE and AFTER, verbatim

Evidence command (task section 3), BEFORE (matches "Expected output today"):
```
{
  "deleted": "CON-9999",
  "dry_run": false
}
rc=0
```
Same command, AFTER:
```
REFUSING: delete-connection: CON-9999 is not a connection. Nothing was written.
rc=1
```

Red test (`python3 scripts/tests/test_run_pipeline_refusals.py`, two cases added after N09: N10 refusal, N11 a live connection still deletes with its targets). BEFORE the change, N11 passed (as it should) and N10 was red:
```
  [✓] N09: a CHECK status on a live connection is accepted
  [✗] N10: delete-connection refuses an unknown con_id
  [✓] N11: delete-connection still deletes a connection that exists, with its targets
EXAMINED: 177 cases
FAILED: 1
rc=1
```
AFTER:
```
  [✓] N10: delete-connection refuses an unknown con_id
  [✓] N11: delete-connection still deletes a connection that exists, with its targets
EXAMINED: 177 cases
PASS: all 177 cases
rc=0
```

End-to-end on the scratch copy (the live table is empty, so I made a fixture with the CLI, `--description "TASK-FIXTURE"`): `add-connection ... --parameter 3 --parameter 4` returned `CON-0001`. Then a mistyped id, the very defect:
```
$ delete-connection --con-id CON-001 ...      (typo for CON-0001)
REFUSING: delete-connection: CON-001 is not a connection. Nothing was written.   rc=1
$ delete-connection --con-id CON-0001 ...
{ "deleted": "CON-0001", "dry_run": false }  rc=0
connections=0, connection_targets=0 afterwards (it had 1 and 2)
```
`sha256sum data/guidebook.db` before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` (unchanged).

## Gate

Run: `scripts/preflight.sh --base HEAD~1 --explain` (see defect D1 for why not `origin/main`). Selftest ran inside preflight: `SELFTEST: PASS`. Work kind classified: tooling; 24 of 75 checks selected. `RESULT: PASS — 22 check(s) green, 2 advisory failure(s)`; `PREFLIGHT: PASS`.
- Touched checks and their subjects: `test_run_pipeline_refusals` PASS, `EXAMINED: 177 cases`; `test_db_amend_writers` PASS, examined 161; `readonly_db_open_audit`, `db_path_env_audit` PASS; `context_map_fresh` PASS. No touched check was NOTHING-IN-SCOPE or EXAMINED: 0.
- Two advisory failures: `test_scan_contract` (G01, G02) is red on untouched HEAD~1 too (I ran it in a throwaway worktree: same 117/119). `retired_vocabulary` (113 occurrences) I did not re-run on the base; it names no line of `scripts/db.py` or the test file in the output I read, so I treat it as unrelated but flag it as unverified.

## What the change did to the pipeline's behaviour

`delete_connection` in `scripts/db.py` now looks the id up with `dbcore.exists(conn, "connections", "con_id", con_id)` before the two DELETEs, and raises `Refusal` (house wording, copied from `update-connection`) when no row exists. Before, a session that mistyped `CON-0001` as `CON-001` ran two DELETEs matching zero rows, was told `{"deleted": "CON-001"}`, and believed the wrong link gone while the real one stayed and could still reach the discussion a reader sees. Now the same typo exits non-zero with a message that names the id and says nothing was written; an existing id deletes its connection and its targets exactly as before. Only the printed result and exit code change for a missing id; no data path changes. Two added lines in `delete_connection`, no new verb, column, check or script.

## Diff stat

`git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'` in the clone: `29 files changed, 4375 insertions(+), 1018 deletions(-)` — this is NOT the task's diff (see D1). The task's own diff, `git diff --shortstat HEAD~1 -- scripts schemas .github skills ':!scripts/migrations'`: `2 files changed, 10 insertions(+)` (2 in `scripts/db.py`, 8 in `scripts/tests/test_run_pipeline_refusals.py`). Reads the new code: sessions acting on the printed result; replaces/makes deletable: nothing.

## Caller sweep (section 5), result

Names `delete_connection`, `delete-connection`: tree hits are `scripts/db.py` (definition, parser, dispatch), my two tests, plus prose/generated files only: `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md` (generated, list the verb), `workplan/workplan-item-audit-pipeline-co0009.md`, the ledger and `REMEDIATION-WORKPLAN.md` / T-032 / T-006 itself (OD-29, retire-in-place). `sqlite_master` (views, triggers, indexes): `[]` for both names (0 rows, unproven but there is nothing a view could reference: the verb is a Python function). Skills/.claude: `[]`. Check registry: `[]`. None of the prose restates the old success-on-missing-id behaviour, so nothing was fixed in this change.

## Task-file defects and ambiguities

- **D1 (section 2 set-up, section 6, section 11): the base ref.** The file says to branch from and gate against `origin/main`. In a clone of this repository, `origin/main` is 106 commits behind the branch that carries the workplan (`origin/ccr-408aaa9b-z3e4s0`, the clone's `HEAD`); it lacks the workplan itself. `--shortstat origin/main` therefore reports 29 files of unrelated change, and `preflight.sh` (default base `origin/main`) would have classified a 686-file diff. I used `--base HEAD~1` after committing. Fix: say which ref is the integration base, or say "gate against the commit your branch starts from".
- **D2 (section 6): the gate is run before the commit in the file's order (sections 6 then 7), but a diff-scoped gate against a base needs the diff; against `origin/main` uncommitted changes are included, against `HEAD~1` they are not.** Say whether to commit first.
- **D3 (section 6, "Add both cases to ... whichever already tests connection verbs"):** `grep -n connection scripts/tests/*.py` offers two files; only `test_run_pipeline_refusals.py` has the unknown-id refusal sibling (N08) and the fixture machinery. Unambiguous in practice but the choice was mine. The file also does not say how the positive case may be built: the live `connections` table is empty, `NEXT_CON` is created by N05 on the main test copy and must not be deleted there (later sections might read it), so the positive case needs the `scratch()` copy. A sentence would save a Sonnet executor a read of ~200 lines of harness.
- **D4 (section 6, "create one on the scratch copy with `add-connection`"):** no command given; `add-connection` requires `--confidence --connection-type --filed-in --description --source-skill`, two or more targets, a valid slug and parameter ids. I derived `--filed-in aac-speech-production-environments`, `--parameter 3 --parameter 4` from the database. Supply a worked invocation or say "derive a slug and two parameter ids from the scratch copy". Also the minted id is `CON-0001` (four digits), while a hand-typed example `CON-001` is itself a wrong id.
- **D5 (section 5, sweep command):** the prose sweep includes `workplan`, which matches the task files, the ledger, the generated `graph.json`/`STATE-GRAPH.md` and old workplans, so the "tree" and "prose" blocks print ~50 lines of noise; section 9 says "stop if the sweep finds a caller this file does not mention", which these hits technically are. I judged them references, not callers, and continued. State explicitly that hits in `workplan/` and generated state-graph files are not callers, or exclude them.
- **D6 (section 2, set-up):** `git switch -c task/t-006-... origin/main` conflicts with the pilot instruction to be on `pilot-T-006`; not a defect for real use. `/session-open` is demanded before the first command; not run in the pilot (no `scratchpad/CURRENT` change in the clone); the clone's existing `CURRENT` names the audit session, so a real executor would have to create a new session folder first.
- **D7 (section 3, "reads the canonical database read-only or works on a copy"):** the delete verb is a write; the evidence command is only safe because `GUIDEBOOK_DB_PATH` is set inline to the copy. The file does say so in section 2; a reminder next to the command would help.
- **D8 (section 4):** says "exactly as `update-connection` already does", which is `update_connection_status`; the function name is not given, and the CLI verb name in the message (`update-connection:` vs the new `delete-connection:`) must be changed by hand. Worked, but name the function.
- **D9 (section 6, proof of examining):** the file lists `EXAMINED:` as the evidence but does not name the check to read (`test_run_pipeline_refusals`); I found it in the `--explain` list. Also the "standing advisory failures" reference (`hs-stress-audit.md` row B-82) was not opened; I verified `test_scan_contract` against base myself.
- **Observation, not a defect:** the verb the task hardens hard-deletes data, which the ledger says contradicts the owner's retire-in-place ruling; section 9 correctly fences that off (T-032 / OD-29).

## Commands run (clone `/tmp/claude-0/pilot/T-006`; scratch `/tmp/claude-0/pilot/guidebook-t-006`)

```
mkdir -p /tmp/claude-0/pilot; git clone --quiet /home/user/guidebook /tmp/claude-0/pilot/T-006; git checkout -q -b pilot-T-006
bash .claude/hooks/ensure-deps.sh; python3 -c "import pydantic, jsonschema"       # deps ok
sha256sum data/guidebook.db; cp data/guidebook.db $SCRATCH/t.db
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py delete-connection --con-id CON-9999 --session session_task-probe   # BEFORE
python3 scripts/tests/test_run_pipeline_refusals.py        # red (after adding N10, N11), then green after the fix
GUIDEBOOK_DB_PATH=... python3 scripts/db.py add-connection ... ; delete-connection (CON-9999, CON-001, CON-0001)
git grep / sqlite_master / skills / registry / prose sweeps for both names (section 5)
git add -A . ':!transcripts' ':!*commands.jsonl'; git commit (prescribed subject, timestamp 2026-11-12 05:41, trailers as given in session)
scripts/preflight.sh --base HEAD~1 --explain
git worktree add ../T-006-base HEAD~1; python3 scripts/tests/test_scan_contract.py   # base comparison, then removed
git diff --shortstat ...; sha256sum data/guidebook.db
```
`run_checks.py --selftest` was not run separately: nothing is renamed (preflight ran it once anyway: PASS).

Patch: `/home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-006.patch`.
