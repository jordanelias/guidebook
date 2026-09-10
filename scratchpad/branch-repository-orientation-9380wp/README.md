# branch `claude/repository-orientation-9380wp` — orientation, then research preparation

**Named for the branch, not a PR number, because no PR existed when the folder was created**
(`scratchpad/README.md`: *"You do not know `<n>` until the PR exists… name it for the branch and
rename with `git mv` once the number is known"*). `git mv` it to `pr-<n>-repository-orientation`
and update `scratchpad/CURRENT` in the same commit once the number comes back.

## Why this folder exists at all, on its first commit

`scratchpad/CURRENT` read `pr-133-db-refusal-sweep` when this session opened, and PR #133 had
already merged (`bd59fd4`). That is exactly the staleness `CLAUDE.md` §7 warns about — *"the folder
it names is then a merged PR's, and your command log appends to someone else's record until you
move it."* 29 lines of this session had already landed in #133's `commands.jsonl` before the move.
They were split back out **by `session_id`**, not by line count, and #133's file was restored to
byte-identical with `HEAD`. Same repair as commit `7660be0` made at #132's merge.

## Contents

- `commands.jsonl` — the Bash hook's log for this session.
- `ORIENTATION.md` — the derived state of the repository and what a batch 06 needs. Everything in
  it is derived from the live repository at the stated timestamp; nothing is quoted from prose.
