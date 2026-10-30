---
name: workflow-rate-limit-lesson
description: "On this account, heavy/concurrent multi-agent workflows trip server-side rate-limiting and spend caps; serialize, keep lean, and have a direct-synthesis fallback."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d8ad22dd-b407-4f8b-b198-5ff102840966
---

Multi-agent Workflow runs on this account repeatedly failed at the synthesis stage. Causes observed (2026-06-22): (1) running 3 heavy workflows concurrently caused "Server is temporarily limiting requests (not your usage limit)" throttling; (2) a single shape-audit run (65 agents, 1.26M subagent tokens) exhausted the **monthly spend cap**; (3) even after a usage reset, a lean solo re-run still got rate-limited at the end after doing real work (320K tokens, 92 tool uses) — the throttle is intermittent but persistent for big fan-outs.

**Why:** The deliverable kept not reaching disk because the *synthesis* agent (the last call) got rate-limited, wasting the upstream map/verify work.

**How to apply:** (1) NEVER run multiple heavy workflows concurrently — serialize, one at a time. (2) Keep fan-out lean (e.g., verify only critical+high findings, not every finding). (3) For the synthesis/last-mile step, prefer authoring it DIRECTLY in the main loop from the structured findings rather than a final synthesis agent that can get throttled — the main loop kept working when subagents were capped. (4) If a run dies at synthesis, author the report yourself from session-verified findings (done for `audits/project-shape-audit-2026-06-22.md`). Relates to [[project-end-goal]].

**Addendum 2026-10-29 (ramp-slope stress test):** Consensus `search` also throttles — 2 of 3 parallel calls returned "Rate limit exceeded" even at the documented batch size of 3; run Consensus queries one at a time. Windows tooling: use `python -X utf8` (note `-I` ignores PYTHONUTF8) or item names containing "≤" crash on cp1252 stdout. `scripts/resolve_dois.py` has no argparse — never call it with `--help`; it runs live.
