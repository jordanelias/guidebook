# Execution brief (every real-execution agent reads this first, then its one task file)

Written 2026-11-13 by the coordinating session. A REAL execution builds one task for a pull request. It differs from a pilot in that the work is committed and pushed. It does NOT include the adversarial pass or opening the pull request: the coordinator runs the critic (a separate read-only agent, as `/adversarial` requires) and opens the PR. Merging is the owner's act; nobody here merges.

## What you follow
`/home/user/guidebook/CLAUDE.md` and your one task file (and the design file it names, if any). Follow the task file's sections in order. If a command prints something other than what the file says, or a step cannot be followed, apply the file's section 9: STOP and report it (with the command and the output). Do not work around a defect silently; a trivial mechanical correction (a typo in a path) may be made if you list it. The files were piloted and folded on 2026-11-13, so a stop is a finding.

## Where you work (a clone, never /home/user/guidebook's working tree)
The owner permitted pushes to task branches named `task/t-nnn-<slug>` (exactly the branch name your task file gives) and to no other branch. Stacked pull requests: your base is the previous task's branch, passed to you by the coordinator as STACK_BASE (a branch name, without `origin/`). Replace the task file's derived `BASE` line with `BASE=origin/$STACK_BASE`, everywhere the file uses `$BASE`, and say so in your report.
```
SCR=/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad
STACK_BASE=<given>      TASK_BRANCH=<given>      TNN=<e.g. t-014>
sha256sum /home/user/guidebook/data/guidebook.db        # record; the working repository's database must not change
rm -rf "$SCR/exec/$TNN" && mkdir -p "$SCR/exec" && git clone -q /home/user/guidebook "$SCR/exec/$TNN" && cd "$SCR/exec/$TNN"
git remote set-url origin https://github.com/jordanelias/guidebook
git fetch -q origin "$STACK_BASE" && BASE=origin/$STACK_BASE
git switch -q -c "$TASK_BRANCH" "$BASE"
bash .claude/hooks/ensure-deps.sh; python3 -c "import pydantic, jsonschema, yaml"
```
Shell variables do not survive between tool calls: start every command block with the `SCR=`, `STACK_BASE=`, `BASE=` lines and `cd "$SCR/exec/$TNN"`.

**Session folder.** The task file says `/session-open`; the command-log hook is bound to the main repository, so in a clone do only its file steps: `STEM="session_$(date -u +%Y-%m-%d)-<task-slug>"; mkdir -p "scratchpad/$STEM"; echo "$STEM" > scratchpad/CURRENT`. This is a TOOLING session (no research rows).

## Rules that bind you (from CLAUDE.md and the task file)
- The canonical database changes only through `scripts/migrate_db.py` (schema tasks commit the migrated `data/guidebook.db` in the clone, as the file says). Never write it with SQL or Python. `GUIDEBOOK_DB_PATH` inline on every `db.py` write call, on a scratch copy.
- The gate ONCE, when every edit is made and before the commit: `scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1`, in the background with a long timeout (it takes several minutes). Read RESULT, NOTHING-IN-SCOPE and any blocking FAIL. Never `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`.
- Run each check the file names, as the registry runs it, before and after, and read its `EXAMINED:` line (the file says which print none).
- Commit message: `governance: <action> [YYYY-MM-DD HH:MM]` (timestamp last, from `date -u '+%Y-%m-%d %H:%M'`), with the body the file asks for, ending with these two trailer lines exactly:
  `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01Ub36iQaXrsGs27PBykEgY7`
  Do not include `[skip ci]`.
- Add the append-only logs only as the file says (`':!transcripts' ':!*commands.jsonl'`).
- Push ONLY your task branch: `git push -u origin "$TASK_BRANCH"` (retry network errors up to 4 times with backoff). Never push to main, never to any other branch, never force-push, never rebase.
- Do NOT open a pull request, do NOT subscribe to PR activity, do NOT run `/adversarial` or `/batch-done` (the coordinator does). Do not schedule check-ins.
- Disk: do not make database copies beyond what the file asks; delete your scratch copies (under `$SCRATCH`) when done. Keep the clone.

## Report (reply with exactly this)
1. TASK, BRANCH, PUSHED sha (`git rev-parse HEAD`), STACK_BASE.
2. DONE or STOPPED (and why, in one sentence, with the command).
3. Canonical working-repository database sha256 before and after (equal) and, for a schema task, the clone's migration number and `PRAGMA user_version`.
4. Red before / green after, in the file's terms.
5. The gate: RESULT line, NOTHING-IN-SCOPE list, advisory failures, each marked "in baseline / not mine / mine and fixed".
6. The code-size line the file asks for, and what the added code reads and what wrong thing it prevents.
7. Deviations from the file, and defects you found in it (command, output, what was expected).
8. A paragraph for the pull-request body: the problem; evidence before and after; each caller the sweep found and what was done; each check with its `EXAMINED:`; what was not verified.
9. The path of the clone.
