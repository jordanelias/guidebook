# PR #134 — orientation, then research preparation

Branch `claude/repository-orientation-9380wp`. **Created as `branch-repository-orientation-9380wp`
because no PR existed yet** (`scratchpad/README.md`: *"You do not know `<n>` until the PR exists…
name it for the branch and rename with `git mv` once the number is known"*), and `git mv`d here
with `scratchpad/CURRENT` updated in the same commit once #134 came back. The number was never
guessed.

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
- `BATCH-06-PLAN.md` — the fifteen legs, each with its `--prior-expectation` written before the
  search ran, per R8.
- `ORDER-OF-WORK.md` — the read-only ordering pass and its instructions. Its lines 97–100 said the
  medical lens was deferred; that was withdrawn under D-0188 and is struck in place.
- `ADJUDICATION.md` — the adjudicator's report, verbatim, under owner delegation D-0188. Three
  records cite it in `decision_artifacts`, one of them immutable.
- `ICD11-CORRESPONDENCE.md` — how ICD-11 grain maps onto the four lenses, and why block level.
- `ICD11-VERIFIED.md` — the retrieval that dissolved the verification block, and the correction to
  the claim that there was one.
- `MEDICAL-LENS-LICENSING-STOP.md` — superseded in place; kept because the ruling that superseded
  it is only legible beside what it overruled.
- `HANDOFF.md` — the next single action, what is owed, and the four owner-gated questions.
