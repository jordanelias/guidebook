---
description: Open a session correctly — set CURRENT before the first Bash call, or the command log lands in someone else's record
argument-hint: "[short-slug, defaults to the branch name]"
---

Do this FIRST, before any other work. `scratchpad/CURRENT` moves at OPEN, and the
`PostToolUse` hook writes every Bash call to whatever it names. Leave it stale and
this session's commands append to a merged PR's record — measured twice in this
repository, most recently 2026-09-18.

```
SLUG="${1:-$(git branch --show-current | sed 's|.*/||')}"
mkdir -p "scratchpad/$SLUG"
echo "$SLUG" > scratchpad/CURRENT
cat scratchpad/CURRENT
```

Name the folder for the BRANCH, never for a guessed PR number. Rename it with
`git mv` once the PR number exists.

Then confirm the previous session closed cleanly:

```
python3 scripts/preserve_transcripts.py --check
```

`--check` is red for the whole life of a live session by construction — the
orchestrator's own transcript is still growing. Read it for what is unpreserved
from BEFORE this session, not as a gate on this one.
