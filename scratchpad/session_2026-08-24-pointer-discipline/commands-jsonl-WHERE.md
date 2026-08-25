# Where this session's `commands.jsonl` actually is

**There is no `commands.jsonl` in this directory, and its absence is a defect in the
recorder, not in the session.** `.claude/hooks/record-command.py` derived the session
stem from `sessions/LATEST` — a pointer moved by the CLOSE-OUT ritual, so for the whole
life of a session it names the PREVIOUS one. Every Bash call this session made was
appended to:

    scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl

Measured 2026-08-25, that file holds three sessions' logs and is named after the earliest:

| dated | lines | actually belongs to |
|---|---|---|
| 2026-08-23 | 5 | `session_2026-08-23-research-batch-03-forward-mining` |
| 2026-08-24 | 405 | `session_2026-08-24-pointer-discipline` |
| 2026-08-25 | 274 | `session_2026-08-25-rulings-incorporation-and-pipeline-sweep` |

**The lines are NOT split back out, deliberately.** The day column above is a description,
not a boundary: the 08-24 session ran straight through midnight UTC — lines 405–411 are one
continuous run from 23:56:44Z to 00:00:09Z — so carving by date would cut a session in half
and assign six of its commands to a session that had not started. Re-attributing a frozen
log by inference is how a provenance record becomes a guess. This is a POINTER to where the
lines are, which is what rule 5 asks for; the log stays where it was written.

Fixed forward 2026-08-25: the hook now DERIVES the open session (a scratchpad session
directory with no `sessions/<stem>.md` behind it is open; the newest such is current) and
files under the harness session id — a visibly foreign name — when it cannot tell. See
`open_session()` in `.claude/hooks/record-command.py`.
