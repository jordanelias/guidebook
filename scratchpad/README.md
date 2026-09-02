# scratchpad/ — one folder per PR, named for it

**Owner directive 2026-09-02: name the folder for the PR concerned.**

    scratchpad/pr-<number>-<short-slug>/
    scratchpad/CURRENT            <- names the folder the command-log hook writes to

`pr-127-research-batch-05-circulation-icf/` is the shape. The PR number comes first so
the folder sorts and greps by the thing a reviewer actually has in hand.

## `CURRENT` is not decoration — it is what makes the command log land in the right place

`.claude/hooks/record-command.py` appends one JSON line per Bash call to
`<the current folder>/commands.jsonl`. **It reads `scratchpad/CURRENT` first**, and only
falls back to inference if that file is missing or names no real directory.

**So a new batch sets `CURRENT` when it creates its folder, before running anything.**

```sh
mkdir -p scratchpad/pr-128-<slug>
printf 'pr-128-<slug>' > scratchpad/CURRENT
```

Forget it, and the hook infers — which is how, on 2026-09-02, **all 969 lines of three
project sessions ended up in one directory** while the newest batch had no command log at
all. The hook's own docstring called the harness session id "the anchor"; it is not. That
id identifies the *harness* session, and one harness session spans as many project
sessions as the container survives. So the hook matched the first directory it ever wrote
to and returned it forever, locking onto its own first mistake — which is why the
misfiling was total rather than partial (D05-004).

`CURRENT` moves at **open**. That is the whole point, and it is the opposite of
`sessions/LATEST` and `sessions/LATEST-RESEARCH`, which CLAUDE.md §7 warns both move at
**close** and therefore name the PREVIOUS session for the entire life of the current one.

## The folder name is not the session id

They are different things and only one of them is renameable.

The **session id** — `session_2026-09-02-research-batch-05-circulation-icf` — is written
into committed data migrations, into `created_by_session` on every row it wrote, into
`sessions/LATEST`, and into the gate scopes. It is immutable in practice. The **folder** is
just where the working files live, and it is named for the PR.

One PR can hold more than one session. `pr-126-...` holds batch 04 *and* the repairs
session that followed it, because both landed in PR #126.

## Older folders keep their `session_*` names, deliberately

Fourteen directories predate this convention. Their PRs are merged, their references are
settled, and renaming them would be churn against frozen records for no reader's benefit.
The hook matches **both** prefixes. Do not "finish the job" by renaming them.

## Frozen records inside these folders were NOT rewritten by the rename

Agent briefs, tracer logs, audit logs and provenance logs still say
`scratchpad/session_2026-09-0X-.../`, because that is where those files were when those
agents wrote about them. They are records of what was true on their date. If you are
following a path out of one of those and it does not exist, this rename is why — the
`session_` stem maps to the `pr-` folder holding the same slug.

## What belongs here

Working files that are a review surface: frames, agent briefs and findings, defect
registers, audit logs, command logs. **Commit them at every natural break, not at session
end** (CLAUDE.md rule 6) — a scratchpad that lives only in context is not a review surface,
and compaction, session end and container reclamation all take it.

Agent *transcripts* are not here: they go to `transcripts/` via
`scripts/preserve_transcripts.py`. See `transcripts/README.md`.
