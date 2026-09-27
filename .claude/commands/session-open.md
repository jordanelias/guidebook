---
description: Open a session correctly — set CURRENT before the first Bash call, or the command log lands in someone else's record
argument-hint: "[short-slug, defaults to the branch name]"
---

Do this FIRST, before any other work. `scratchpad/CURRENT` moves at OPEN, and the
`PostToolUse` hook writes every Bash call to whatever it names. Leave it stale and
this session's commands append to a merged PR's record — measured twice in this
repository, most recently 2026-09-18.

**`CURRENT` holds the DB SESSION STEM** (`session_YYYY-MM-DD-<slug>`), not a bare
branch slug. Batches 11–15 wrote branch slugs and their rows were stamped
`session_2026-09-18-research-batch-15-...` — a mismatch that scopes any check reading
`CURRENT` (e.g. `adversarial_pass_recorded`, RC4) to zero rows while reporting green.

**THE FOLDER NAME AND `CURRENT`'S CONTENT MUST BE IDENTICAL, not just similar.**
`.claude/hooks/record-command.py` only honours `CURRENT` when
`scratchpad/<CURRENT's content>` is a real directory; otherwise it falls back to a
same-harness-sid guess that can misfile the whole command log into an unrelated past
session's folder (measured 2026-09-27, ~30 minutes of commands lost into a stale
directory after a session changed `CURRENT` to the stem without renaming its folder to
match). Create the folder AS the stem from the start — never a bare slug — so there is
no window where they disagree:

```
SLUG="${1:-$(git branch --show-current | sed 's|.*/||')}"
STEM="session_$(date -u +%Y-%m-%d)-${SLUG}"
mkdir -p "scratchpad/$STEM"
echo "$STEM" > scratchpad/CURRENT
cat scratchpad/CURRENT
```

Rename the folder with `git mv` once the PR number exists, per the trap CLAUDE.md
section 7 names — but leave `scratchpad/CURRENT`'s content as the DB stem; do not
rename it to match. The hook's fallback (matching a `session_`/`pr-`-prefixed folder
by this harness's own last-logged command) covers exactly this gap, so a rename that
keeps one of those two prefixes stays routed correctly with no direct-match window at
all. What breaks routing is changing `CURRENT` to a value that names NEITHER the
current folder NOR any `session_`/`pr-`-prefixed folder that exists — always know
which of the two you are changing, and if it is `CURRENT`, create or rename the
matching folder in the same breath.

**Record the session kind (RC6).** Say, in your first status update, whether this is a
**research session** (writes rows only — evidence, judgment, synthesis) or a **tooling
session** (schema, scripts, checks, governance prose — no research rows). This
determines whether `research_tooling_separation` should ever see both kinds of path in
one changeset from this session: it shouldn't, by construction, for either kind. A
session that finds it needs both mid-way is the RC6 trap (DR-2026-08-19 §12.2's AMENDED
callout): file the writer gap as a GAP and either leave the rows unwritten or write them
through verbs the CLI already has; the tooling fix ships in its own PR, merged to main
first, and the batch branch takes it with `git merge origin/main`.

Then confirm the previous session closed cleanly:

```
python3 scripts/preserve_transcripts.py --check
```

`--check` is red for the whole life of a live session by construction — the
orchestrator's own transcript is still growing. Read it for what is unpreserved
from BEFORE this session, not as a gate on this one.
