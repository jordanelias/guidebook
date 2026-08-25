# Smoke-test protocol — 2026-08-25

Shared rules for every smoke-test agent. Written before the run so the logs are comparable.

## Subject of the eventual real batch (the smoke test must be shaped to it)

- **Items:** mobility — corridor clear width (`E-08`), door thresholds (`E-11`, `G-04`),
  sloped surfaces / ramp gradient (`E-03`), flooring materials (`B-08`, `C-03`, `C-05`, `C-06`,
  `A-05`), handrails (**no item exists — verify**), lift (`E-01`), parking (`E-04`).
- **Jurisdictions:** bucket 1 = UN · ISO · Canada · USA · UK · Germany · Norway · Sweden · Japan ·
  Australia; bucket 2 = EU · Singapore · New Zealand · Ireland · France · Spain · Portugal ·
  Finland · Netherlands · South Korea
  (`workplan/2026-08-18-research-frame-proposal.md:420-424`).
- **Driver:** the clue store, `source_locators` (875 rows) — "a lead index of identifiers, not
  evidence" (CLAUDE.md §4).

## Hard prohibitions

1. **Never write `data/guidebook.db`.** Open it read-only only. Record its sha256 at start and end
   of your run; both must equal `30a10669...`. Every write goes to your own scratch copy.
2. **Never commit, never push, never `git checkout`/`restore`/`stash`.** Other agents share this
   worktree.
3. **Never edit a tracked file** except your own log under
   `scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/logs/`. If a step you are testing
   would mutate tracked files (generators, formatters), redirect its output to your scratch
   directory, or run it, capture `git status`/`git diff --stat`, and immediately restore the file
   **by rewriting it from `git show HEAD:<path>`** — never a bulk `git checkout`.
4. **Admit no evidence anywhere.** External research tools get at most 1–2 reachability probes
   each. Record the response shape; do not mine a corpus.
5. **`ls`/Glob before believing "no matches".** `.ignore` hides `_archived/`, `audits/`,
   `sessions/`, `references/search-log/`, `versions/`, `workplan/_superseded/` from ripgrep and
   Grep. Use `grep -r` / `git grep` for those paths.

## What every log entry must carry

One entry per invocation, in your log file, in this shape:

```
### <ordinal>. <what was invoked>
INVOKED   : <exact command / skill file / tool name>
STAGE     : research | evidence-collection | judgment | synthesis | render | substrate
EXIT      : <code>   RUNTIME: <s>
READS     : <files:line-ranges, tables/columns, pointers, env vars>
WRITES    : <files:line, table.column cells with rowids/keys, or NONE>
EXAMINED  : <n subjects, per CLAUDE.md §2(a)> or NOTHING-IN-SCOPE
OUTPUT    : <verbatim head/tail, trimmed to what carries the finding>
FINDING   : PASS | FAIL | VACUOUS | ABSENT (does not exist) | BLOCKED (<why>)
LOCATION  : <file:line> or <table.column @ key> for every defect named
NOTE      : <one or two lines: what this means for the mobility batch>
```

`EXAMINED` is not optional: a gate that passes having examined nothing is failure mode (a) in
CLAUDE.md §2 and has been produced four times here. **When a check passes, prove it had a subject.**

## Absent things are first-class results

You are explicitly asked to attempt work the repository may not have built — backward and forward
citation mining, comparative analysis across judgments and syntheses, and so on. When a capability
does not exist, do not simulate it. Record `FINDING: ABSENT`, name the nearest existing surface
(script, skill, table, view), name what would have to exist, and say which pipeline stage is left
unenforced. An honest ABSENT is worth more than a green improvisation.

## Scratch database

Yours is at `$SMOKE/<your-id>.db` where
`SMOKE=/tmp/claude-0/-home-user-guidebook/982e23dc-1318-5999-92af-f35647743666/scratchpad/smoke`.
Point `GUIDEBOOK_DB_PATH` at it **inline on every call** — the harness resets env between shells:

```
GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db python3 scripts/db.py <subcommand> ...
```

Every write-time refusal is a **result**, not an obstacle. Log the refusal text verbatim; that is
the thing under test.
