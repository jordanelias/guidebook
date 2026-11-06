# Audit trail: stress test of skills/run-pipeline_SKILL.md, and the cache/tmp cleanup

Written by the session as it acted, on the owner's instructions of 2026-11-06 ("stress test the skill", "all directions", "remove stale files from cache", "or tmp", "log all steps for audit trail", "including all failures").
Machine record of every shell call in this session, failures included: `scratchpad/session_2026-11-06-pipeline-batch/commands.jsonl` and `transcripts/harness_a45ca7d3/` (the main transcript and each subagent's). This file is the human-readable account; entries are appended and never edited, corrections are new entries.


## Part 1. Cleanup of stale cache and tmp files

Decision rule: delete only files this session created or that the tooling regenerates, and only when nothing running or still owed reads them. KEPT, with reasons, are listed at the end of this part.

| # | time | action | target | detail | outcome |
|---|---|---|---|---|---|
| 1 | 2026-11-06 09:19:54 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/rebuilt.db` | scratch leftover from this session; 5115904 bytes; sha256 aec024b98ad88898 | OK |
| 2 | 2026-11-06 09:19:54 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/rebuilt2.db` | scratch leftover from this session; 5115904 bytes; sha256 ec5170e54f167c22 | OK |
| 3 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/rebuilt3.db` | scratch leftover from this session; 5115904 bytes; sha256 792a7a21d5fd9785 | OK |
| 4 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/a.txt` | scratch leftover from this session; 980 bytes; sha256 8501895d2d6e60ad | OK |
| 5 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/b.txt` | scratch leftover from this session; 980 bytes; sha256 8501895d2d6e60ad | OK |
| 6 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/run_checks.txt` | scratch leftover from this session; 19536 bytes; sha256 8f9dd0df9e8a7365 | OK |
| 7 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/decisions_update.sql` | scratch leftover from this session; 1007 bytes; sha256 41cb494d2c901adc | OK |
| 8 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/x.db` | tmp copy of a rebuilt DB; 5115904 bytes; sha256 792a7a21d5fd9785 | OK |
| 9 | 2026-11-06 09:19:55 UTC | delete file | `/tmp/claude-0/moved.jsonl` | seven command-log lines already appended to the session log; 8645 bytes; sha256 f9755cbbf6cb2b10 | OK |
| 10 | 2026-11-06 09:19:55 UTC | list ignored paths | `git status --short --ignored` | rc=0 | OK |
| 11 | 2026-11-06 09:19:55 UTC | delete generated file | `data/audit_graph.db` | ignored artefact the graph audit rebuilds; 2879488 bytes; sha256 241372818796336c | OK |
| 12 | 2026-11-06 09:19:55 UTC | delete cache dir | `schemas/__pycache__/` | 11 file(s), 114540 bytes; python regenerates it | OK |
| 13 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/__pycache__/` | 5 file(s), 713134 bytes; python regenerates it | OK |
| 14 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/assess/__pycache__/` | 1 file(s), 114597 bytes; python regenerates it | OK |
| 15 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/audit/__pycache__/` | 2 file(s), 41349 bytes; python regenerates it | OK |
| 16 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/audit/graph/__pycache__/` | 7 file(s), 49939 bytes; python regenerates it | OK |
| 17 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/ci_helpers/__pycache__/` | 2 file(s), 4837 bytes; python regenerates it | OK |
| 18 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/research/__pycache__/` | 2 file(s), 149232 bytes; python regenerates it | OK |
| 19 | 2026-11-06 09:19:55 UTC | delete cache dir | `scripts/tests/__pycache__/` | 1 file(s), 8745 bytes; python regenerates it | OK |
| 20 | 2026-11-06 09:19:55 UTC | git worktree prune | `git worktree prune -v` | rc=0; nothing to prune | OK |
| 21 | 2026-11-06 09:19:55 UTC | regenerate | `/tmp/claude-0/-home-user-guidebook/a45ca7d3-e506-5935-9bfc-36628e89637d/scratchpad/pipeline-stages.md` | stale (written before migrations 117 to 121); old sha256 9eb6ad46feba1cb3, new sha256 3cc7a500b6876960; tables, counts and verb-to-table mapping are re-derived, its hand-written prose bullets are NOT refreshed | OK |

KEPT (not stale, or still owed):
- `decisions_update.keep.sql`: the SQL for the data-only follow-up PR that marks decisions D-0058 and D-0065 SUPERSEDED.
- `gen_stages.py`, `pipeline-stages.md`: the stage reference the owner asked for (regenerated above).
- `stress/` and `stress2/`: the two stress testers' scratch directories, in use.
- `tasks/`: harness task output, harness-managed.
- `cleanup_with_audit.py`: this script.


## Part 2. Stress-test runs

| # | time | run | outcome |
|---|---|---|---|
| 22 | (launch time not captured at the time; see the main transcript) | Walk-through 1: `from-evidence` stages 3 to 7 plus exception drills, a fresh general-purpose agent following only the skill, on a scratch copy of the database | launched in the background |
| 23 | 2026-11-06 09:21:55 UTC | Walk-through 1 | **FAILED, terminated early by the platform, not by the skill.** Error text, verbatim: "Agent terminated early due to an API error: API Error: Sonnet 5.5's safeguards flagged this message (https://www.anthropic.com/legal/aup). This sometimes happens with safe, normal conversations. Claude Code can't respond to this message with Sonnet 5.5. Try rephrasing the request in a new session or change your model. Details: `[reasoning_extraction]`. Request ID: req_011CgmRqFqNQy3MCa131eJsR (error type invalid_request)". Its only recorded output before stopping: "I'll start by reading the skill and running the dependency hook." No step log was written, so this walk-through produced **no results**: the `from-evidence` variant, its exception drills (a to g) and the closing-gates check are UNTESTED. The session did not redo the agent's work itself, per the notification. |
| 24 | 2026-11-06 09:26:01 UTC | Walk-through 1, RETRY | Relaunched on the owner's instruction ("why would sonnet fail? try again"). Same brief and same model as the failed run, unchanged except that it now requires a step log at the tester's scratch directory (`stress/steplog.md`). The cause of the entry-23 failure is unknown: the platform error names a safeguard flag (`[reasoning_extraction]`) on the agent's message and nothing else, and the brief was not altered to get past it. Outcome: pending. |
