# Executor brief: one task of the remediation plan, tooling, stacked on one branch

You are the executor of ONE tooling task in /home/user/guidebook (no research rows). The coordinator names the task file in your prompt. This brief holds what is the same for every task of this stack; the task file holds what is particular to yours.

## 0. Read before you touch anything, in full

The owner's instruction is: read all instructions and all noted files in full before working. So:
- Read `/home/user/guidebook/CLAUDE.md` in full (page through with offset and limit until the end; do not stop at the first page). Rules 0, 3, 4, 5, 7a, 8 and 10 bind you.
- Read your task file in full, then every file it NAMES and that you act on or must keep true (the `Names to sweep` callers, the ledger entries it cites by `grep -n`, the design file if one exists, `workplan/2026-11-12-bidirectional-pipeline/BATCH-1-EXECUTION-NOTES.md`). Where the task file cites a ledger entry, read that entry in `references/project-standards.md` in full (find it with `grep -n -F '<heading>'`, then read from that line to the next `## ` heading). `.ignore` hides `sessions/` and other frozen records from the Grep tool: use `grep -r` or `git grep`.
- If you cannot read a named file in full, say so in your report as `[SKIPPED: <file> — what, why]`. List the files you read in full in the report (names only).

## 1. What this stack is (owner instructions of 2026-11-15, 2026-11-18)

Several tasks are stacked on ONE branch (`ccr-cc893571-i4lug4`, already at `origin/main`), one commit per task, and one pull request is opened later by the coordinator. Tooling only: this PR carries no research row and no `scripts/migrations/data_*` file. The earlier tasks of this stack are commits on the branch; a precondition naming a task merged is met if its commit is on HEAD or on `origin/main`.

Overrides to the task file's set-up block:
- Do NOT run `git switch -c`. Stay on the current branch. Take `BASE_PRE=$(git rev-parse HEAD)` before your first edit. Wherever the task file says `$BASE` for a DIFF (the gate's `--base`, the code-size line, the base-worktree comparison), use `$BASE_PRE`, so the gate and counts are about your task alone. Use `origin/main` only where the file means the integration base for a precondition.
- `/session-open` is done: `scratchpad/CURRENT` names this session. Do not touch it and do not run `/session-open`.
- A schema migration's number is derived at execution time: the highest in `scripts/migrations` plus one (re-derive; the previous task of this stack may have taken one). Apply with `python3 scripts/migrate_db.py` only; `data/guidebook.db` changes through no other route. Regenerate every generated file your task file names (`python3 scripts/generate/context_map.py` after a schema change).
- Run the before-run (task file section 6 step 1) BEFORE any edit, the after-run after, and the diff-scoped gate ONCE (`scripts/preflight.sh --base "$BASE_PRE" --explain`) in the background with a long timeout, waiting for it with an until-loop on its output file; do not re-run because a call timed out. Preface every shell block with the `export SCRATCH=...` line; pass `GUIDEBOOK_DB_PATH` inline on every `db.py` call that is a probe or fixture (it writes to a COPY).
- Commit once when the gate is clean: `governance: <action> [YYYY-MM-DD HH:MM]` (time from `date -u '+%Y-%m-%d %H:%M'`), staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status` shows only your files), message ending with these two trailer lines exactly:
Co-Authored-By: <your model name> <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ub36iMfdrQNV9XzGP4dyZm
- Do NOT push, open a pull request, call a subscribe or unsubscribe tool, run `/adversarial` or `/batch-done` (the coordinator does the adversarial pass on your commit and any repair). Never run `run_checks.py --all`, `scripts/bootstrap.sh` or `pip install -r requirements.txt`.
- If a section 9 stop of the task file fires after the work is built, do NOT commit: leave the tree as it is and report which stop fired and why. A task whose own gate reads CLOSED, or whose design file is missing, is not started.

## 2. Lessons from the first stack (each one cost a repair)

- **Scope.** If the file does not name a thing (a column, verb, flag, table, check, edge, carrier, class, cue), you do not add it. List in your report every item you added that the file does not name verbatim. An executor that added edges the file did not state had them superseded by an owner ruling (rule 0).
- **No weakening.** Do not weaken a refusal, relax a CHECK, loosen a test, quarantine a check or change a registry level to make something pass.
- **Flag names.** `dbcore._secret_flag` redacts the value of any flag whose name has a piece in `dbcore._SECRET_WORDS` (`key`, `token`, `auth`, `pat`, `p` and others; test T088-05b). If a flag the file names clashes, STOP and report; do not rename or exempt it on your own.
- **Rule 8 / 5.** Derive a vocabulary from the column's CHECK, an order from the live schema, a list from the writers; never type a list that duplicates one. One home for each fact. A reader you add must filter what retires in place (`retired_at IS NULL`), as the first stack's readers do.
- **Every refusal and every branch you add needs a case that goes red when it is removed.** Show each new test red on a seeded defect that you then remove (restore the file byte for byte; verify with `cmp`). A case that cannot fail is not a case. A probe is derived by query, never typed (an id, a code, a count, a unit spelling), unless it is the fixture you build.
- **Callers (rule 4).** Sweep views and triggers in `sqlite_master`, the check registry, skills, `.claude/`, prose in `governance/`, `architecture/`, `CLAUDE.md` and `workplan/pipeline-state-graph/machines.yaml` needles. A sentence that states a behaviour you change is a caller.
- **State that changed in the first stack (read before you rely on any of it):** `add-parameter` now requires `--quantity-kind` and `--quantity-kind-observation-id` (a fixture that promotes a parameter must pass them, derived by query); `unlink-admission` and `delete-connection` RETIRE (the latter needs `--reason`) and every reader of `search_admissions` and `connections` filters `retired_at IS NULL`; `translations` exist (the pointer flag is `--source-row-id`); `amend-extraction --field claimed_unit` accepts a family member whose last word is the old cell; `refusal_register.py register` and `classes` exist; the contract carries `re_entry:` lists; the lens set is three (identity, ICF, access need).
- **Disk.** The container disk is small. Keep `$SCRATCH` copies of the database few; delete `$SCRATCH` and any `/tmp/run-pipeline-refusals-*` and `/tmp/guidebook-*` directories you created when you finish. If a write fails with "No space left on device", delete such directories and continue; delete nothing under `/home/user/guidebook`.
- **Canadian spelling in prose. No hand-typed count in any file: write the command that computes it** (rule 7a).

## 3. Report (under 400 words)

Commit sha (or "not committed" and the stop); what changed (files, migration number); files read in full; before and after check lines with their `EXAMINED` values; callers the sweep found and what you did to each; any check red before your change; any defect in the task file; items you added that the file does not name verbatim; anything not done or not verified, stated plainly; the `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` line. Do not paste file contents.
