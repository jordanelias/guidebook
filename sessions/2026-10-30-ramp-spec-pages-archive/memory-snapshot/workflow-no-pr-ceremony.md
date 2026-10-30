---
name: workflow-no-pr-ceremony
description: "Guidebook repo: PRs/branches are not forbidden; the user only dislikes Claude pinging GitHub for merges incessantly for no reason."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d8ad22dd-b407-4f8b-b198-5ff102840966
  modified: 2026-10-30T04:27:32.686Z
---

On `C:\Github\guidebook`, the user does NOT object to branches or PRs as such. Corrected 2026-10-30: "no-PR workflow is incorrect -- I just don't want Claude to be pinging GitHub for merges incessantly for no reason." The earlier reading ("solo repo, skip branches/PRs") was too broad.

**Why:** The annoyance is noisy, needless GitHub activity (repeated merge/PR prompts), not the existence of PRs. The remote evidently does use PRs (origin/main has merged PRs such as #204 from cloud sessions), so main is not a private solo line.

**How to apply:** Don't open PRs, push, or prompt for merges unless there is a reason (the user asks, or work must reach the remote). When work does need to reach GitHub, do it once and deliberately, not repeatedly. Still commit/push only when the user asks. Before pushing, fetch and check divergence from origin/main. Relates to [[project-end-goal]].
