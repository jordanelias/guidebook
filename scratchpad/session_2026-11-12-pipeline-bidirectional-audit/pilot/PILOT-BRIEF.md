# Pilot brief (every pilot executor reads this first, then its one task file)

Written 2026-11-13 by the coordinating session from `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` §4 ("The brief every pilot executor gets") and the R2 findings. A pilot tests the TASK FILE, not the product: its output is a report on whether the file can be followed to a green result, and a patch. A pilot never merges, never pushes, never opens a pull request and never writes the canonical database.

## What you follow
Only `/home/user/guidebook/CLAUDE.md` and your one task file. Do not read other task files, the audit folders or the ledger unless the task file tells you to. If the task file is wrong, stop and report the defect; do not work around it silently (a worked-around defect is a defect that is still in the file).

## The base is NOT origin/main
Pull request 220 (the plan's latest edits) is unmerged and the local `main` ref is stale, so in a clone `origin/main` is old. **For every command in your task file that uses `$BASE`, set it to the branch tip, exactly:** `BASE=origin/claude/peaceful-noether-kvf3sf`. Do not run the task file's own BASE line; it would choose a stale `main`. Say in your report that you overrode it and why.

## Set-up (replace T-nnn by your task's number, lower-case in branch names)
```
SCR=/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad
OUT=/home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot       # report and patch go here, and nowhere else inside /home/user/guidebook
BASE=origin/claude/peaceful-noether-kvf3sf
sha256sum /home/user/guidebook/data/guidebook.db        # record; it must be identical when you finish
rm -rf "$SCR/pilot/T-nnn" && mkdir -p "$SCR/pilot" && git clone -q /home/user/guidebook "$SCR/pilot/T-nnn" && cd "$SCR/pilot/T-nnn" && git switch -q -c pilot-T-nnn "$BASE"
bash .claude/hooks/ensure-deps.sh; python3 -c "import pydantic, jsonschema, yaml"     # a red check without pydantic proves nothing
```
Every later command runs inside `$SCR/pilot/T-nnn` (the clone). Shell variables do NOT survive between tool calls in this harness: begin every command block with the `SCR=`, `OUT=`, `BASE=` lines and `cd "$SCR/pilot/T-nnn"`. The task file's own `export SCRATCH=...` line is fine (it makes a folder under `$TMPDIR`; keep it).

**Stacked pilots.** If your task is stacked on predecessors, apply each predecessor's patch in the order the coordinator gave you: `git am "$OUT/<pred>.patch"` (use `git am --3way` if a plain apply fails and say so), then run `python3 scripts/migrate_db.py` in the clone so the clone's own database carries their schema. Migration numbers in a stack are pilot-local: if two predecessors took the same number, renumber the later one in the clone and say so; the real execution derives its number again. Never touch `/home/user/guidebook/data/guidebook.db`: work on the clone's copy and on `$SCRATCH` copies, and pass `GUIDEBOOK_DB_PATH` INLINE on every `db.py` write call (the harness resets env between shells).

## Pilot mode (this overrides the task file where they differ)
- Do NOT run `/session-open`; do not touch `scratchpad/CURRENT`; stay on the pilot branch (the file's `git switch -c task/...` line is for real execution only).
- Follow the file's sections in order through section 7 (commit, locally, in the clone). A commit message needs no trailers in a pilot. Stop there: no push, no pull request, no `/adversarial`, no `/batch-done`, no `unsubscribe`.
- Run the gate ONCE, when every edit is made and before the commit: `scripts/preflight.sh --base "$BASE" --explain` (the file's section 6 step 4). Read three things: the `RESULT` line, any check under NOTHING-IN-SCOPE, any blocking FAIL. Never `run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Run each check the task file names, as the registry runs it, before and after, and read its `EXAMINED:` line. A check with no `EXAMINED:` line or `EXAMINED: 0` examined nothing: say so.
- **Failing cases are compared with the R2 baseline.** `/home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/baseline-red-on-main.txt` lists the cases red on the untouched base (test_scan_contract G01 and G02; validate_schema_cross_check; research_dod R12; retired_vocabulary; skill_vocabulary_audit; doctrine_recheck). A case in that file is not your change's. Note: `doctrine_recheck` is at `scripts/doctrine_recheck.py` (the registry runs it with `--cross-ref`), not `scripts/audit/`.
- Case ids you write are prefixed with the task number and checked free first; probes are chosen by query, never typed; a new test must be shown red on the unchanged code (or on a seeded defect you then remove).
- The sweep: the file's exclusion list and its "caller, not mention" definition. Stop only on a caller you cannot repair within the file's section 4.
- If a command in the file prints something other than what the file says it will, that is a finding: record it (the command, what it printed, what the file said), and decide whether it is a stop condition under the file's section 9.

## What you save (the deliverables)
1. `$OUT/T-nnn-report.md`, ending with a section titled exactly **Task-file defects**. The report states: the base commit; whether each of the following held: (1) you followed only CLAUDE.md and the task file, (2) the evidence command printed what the file says (or the difference), (3) red before and green after (or a stop on a task-file defect, and if you stopped, what a corrected file would need), (4) the gate ran once and every named check's `EXAMINED:` was read (give each), (5) patch and report saved; the check-by-check before/after table; the sweep result; the code-size line; every place the file's instructions were wrong, unclear, ambiguous, missing a step, or contradicted by the repository, each with the command and the observed output. Do not soften: a defect that cost you more than a few minutes is the finding this pilot exists for.
2. `$OUT/T-nnn.patch`: `git -C "$SCR/pilot/T-nnn" format-patch -1 --stdout > "$OUT/T-nnn.patch"` (if you made one commit; if you stopped before a green state, save the diff of your working tree instead and say so).
3. Nothing else inside `/home/user/guidebook`. Do not commit there.

## Reply
Return only: the task id; PILOTED or STOPPED (and why, in one sentence); the sha256 of the canonical database before and after (must be equal); red-before/green-after in one line; the count of task-file defects and the three worst, in one line each; the two file paths.
