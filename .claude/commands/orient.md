---
description: Orient in the repository from live state before starting work — derived, never quoted
---

Orient yourself here before doing anything else. **Derive every figure below; do
not quote one from a document, this file included** (CLAUDE.md rule 7a).

Run these, and read what they say rather than what you expect:

```
bash .claude/hooks/ensure-deps.sh          # a fresh container has no pydantic
cat scratchpad/CURRENT                     # the session running NOW
python3 scripts/run_checks.py --list       # registry + quarantine
```

Then establish live state with `db-census` (Haiku — do not spend Opus on counts):

- row counts per table, and which tables are EMPTY
- which tables are UNWRITABLE through a NOT NULL FK into an emptied table
- `PRAGMA user_version`

Read, in this order, and only these:

1. `decisions/DR-2026-08-19-research-restart-operative-instrument.md` — what to do now
2. the tail of `references/project-standards.md` — the latest owner rulings, which
   supersede every ratified record they touch on contact (rule 0)

**Two traps that make a confident answer wrong.** `.ignore` hides `sessions/`,
`_archived/`, `audits/`, `versions/` and `tools/*.html` from ripgrep and the Grep
tool, and owner rulings live overwhelmingly in `sessions/` — use `grep -r` or
`git grep`, and never report a ruling absent from a search that could not have
seen it. `sessions/LATEST` and `LATEST-RESEARCH` move at CLOSE, so both name the
PREVIOUS session all session long.

Report: what state the pipeline is in, what the live blockers are, and the single
next action. State assumptions inline. Do not produce a plan document unless I
ask for one.
