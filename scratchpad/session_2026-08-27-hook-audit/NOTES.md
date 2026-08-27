# Session note — hook audit (2026-08-27)

Question put to the session: "is this doing anything" — read as the harness-injected
research contract banner and, by extension, the hook battery in `.claude/settings.json`.

## Measured

| Hook | Result |
|---|---|
| `SessionStart` — contract banner | Working. `scripts/generate/research_contract_hook.py --check`: 51 contract lines, 15 rule ids, hook text matches `governance/research-contract.yaml`. |
| `SessionStart` — `ensure-deps.sh` | Working. `pydantic 2.13.4` + `jsonschema` present. |
| `Stop` — research DoD gate | Working. Hook body run verbatim: exit 0, COMPLIANT, R1–R15 PASS, R11 856 (baseline 856) inherited debt. |
| `PostToolUse` — `record-command.py` | **Misfiling.** See below. |

## The defect

Every Bash call of this session was appended to
`scratchpad/session_2026-08-24-pointer-discipline/commands.jsonl` — a directory three
days stale. The file was untracked and carried only this session's id
(`8c91e4a4-…`), eight lines, all stamped `2026-08-27T03:48`. Nothing from the 08-24
session was in it. Moved to this directory before committing, so the misfile is not
written into the permanent record.

Mechanism, `.claude/hooks/record-command.py:112-114`: the function anchors on
`session_id` once some log carries one, but on a session's FIRST command no log does,
so it falls through to `openp[-1]` — the newest `scratchpad/session_*` with no
`sessions/<stem>.md` behind it. Derived live, two dirs are open:

    OPEN  session_2026-08-21-reasoning-doc-digestion
    OPEN  session_2026-08-24-pointer-discipline

so `openp[-1]` is 08-24, and the first command anchors there for the whole session.

This is the defect the function's own docstring says it fixed — the docstring names
`session_2026-08-24-pointer-discipline` as the wrong answer the *previous*
(`sessions/LATEST`) implementation returned. Swapping the LATEST pointer for the
open-dir derivation reaches the same stale dir by a different door, because **"open"
and "current" are not the same thing when close-out is skipped**. Both the pointer
and its replacement are guesses at a fact the hook is already holding.

## Candidate fixes (not applied — awaiting owner decision)

1. **Narrow.** Close out the two stale sessions; `openp` empties and the fallback
   returns `""` rather than a wrong directory. Leaves the guess in place — it breaks
   again the next time a session is not closed out.
2. **Real.** The hook has `session_id` on the first call. Mint a directory from it
   instead of selecting an existing one. Removes the guess rather than re-tuning it,
   and is the shape rule 5 asks for: the session id is the fact, not a pointer to it.

---

## A second defect in the same hook, found 2026-08-27 05:12

**`record-command.py` attributes SUBAGENT commands to the parent session.**

While four Fable 5 auditors ran as subagents, the working tree kept dirtying on turns where the
parent session made no Bash call at all. Measured against
`scratchpad/session_2026-08-27-hook-audit/commands.jsonl`:

```
session_ids appearing in the log:
  8c91e4a4-984d-529f-ae03-ef6bae67b9a6  ×147     ← one id, every line

last recorded command: 2026-08-27T04:22:03Z
  mkdir -p /home/user/guidebook/scratchpad/session_2026-08-27-hook-audit/audits
```

That `mkdir` was run by an **auditor**, not by this session. Every one of the four subagents' Bash
calls lands in the parent's log under the parent's `session_id`, indistinguishable from the parent's
own work.

**Why this matters beyond the noise.** The command log is a provenance record — it is what the
2026-08-25 session built the derivation for, and what CLAUDE.md rule 6 requires committed so the
session has a review surface. A log that cannot say *who ran a command* is the same class of defect
as the misfiling above: the record exists, and it attributes wrongly. The 2026-08-27 nomenclature
session specifically valued its adversarial pass because *"four Fable 5 auditors, read-only, one lens
each, each writing its own report"* **repaired** a provenance weakness where auditors could not write
and their findings were transcribed by hand. This hook quietly re-introduces that weakness one layer
down: the reports are the auditors' own, but the command trail behind them is not.

**Practical effect on the session loop.** The parent's tree dirties whenever any subagent runs
anything, so the stop-hook git check fires on turns where the parent did nothing — a commit treadmill
with no fixed point while subagents are alive.

**Fix, and it composes with T-0.3.** The hook already receives a `session_id`; the defect is that a
subagent's id is not it. Two parts:
1. Record the *invoking agent's* id, not the root session's, and write a distinguishing field
   (`agent_id`, or `is_subagent`) on every line.
2. Once T-0.3 mints the directory from `session_id`, a subagent's commands either land in their own
   file or carry the discriminator — either is honest; the current merge is not.

Neither is applied here. Recorded for the same reason as the first defect: the record should say what
was measured, not what was tidied.
