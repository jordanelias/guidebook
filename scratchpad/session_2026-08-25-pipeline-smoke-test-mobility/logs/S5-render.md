# S5 — RENDER STAGE smoke test log
2026-08-25

Baseline `git status --short` (pre-existing, NOT mine):
```
 M scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl
 M sessions/LATEST
?? scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/
?? sessions/session_2026-08-25-pipeline-smoke-test-mobility.md
```
`git stash list`: empty.
DB sha256 at start: `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf` (matches PROTOCOL expected `30a10669...`).
Scratch DB: `$SMOKE/s5-render.db` (copy of canonical, same sha256 at copy time).

