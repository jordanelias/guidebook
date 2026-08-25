# The command-log hook misfiles again — third iteration of one bug

**Found by observation, 2026-08-25 22:27Z**, minutes after PR #119 merged. Not sought; the hook
filed this session's commands into a different session's directory and `git status` showed it.

## Measured

```
scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/commands.jsonl
    822 lines, 0 carrying session_id        <- this session's real log, old schema

scratchpad/session_2026-08-25-rulings-incorporation-and-pipeline-sweep/commands.jsonl
    30 lines, 4 carrying 982e23dc-…         <- MY commands, in ANOTHER session's directory
    last line ts 2026-08-25T22:27:22Z, session_id 982e23dc-…
```

## Mechanism

`open_session()` in `.claude/hooks/record-command.py`:

1. **Fast path** — match `session_id` against the *last line* of each log. My session's own log has
   **822 lines and zero `session_id` fields** (written under the pre-#119 schema), so it can never
   match. The fast path cannot bootstrap: the very first call of any session has no line to match.
2. **Fallback** — `openp = [n for n in pads if not (root/"sessions"/f"{n}.md").exists()]`, then
   `openp[-1]`. **A session is treated as closed the moment its record file exists.** This session
   wrote `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` at close-out — correct
   practice — so it is classified closed while still running. The newest dir *without* a record is
   `session_2026-08-25-rulings-incorporation-and-pipeline-sweep`, so my commands go there.
3. **Self-reinforcing.** That log now ends with my `session_id`, so the fast path matches it on
   every subsequent call and **pins** the misfile permanently.

## Why this is the same bug a third time

| Version | Derivation | Failure |
|---|---|---|
| ≤2026-08-23 | `.claude/session` | pointer moved at close-out → named the previous session |
| 2026-08-23 | `sessions/LATEST` | pointer moved at close-out → named the previous session |
| 2026-08-25 (#119) | "no record file ⇒ open" | **record written before close ⇒ named another session** |

#119 diagnosed the first two correctly and precisely — *"swapping which stale pointer you read
changed nothing"* — and its own docstring warns *"the wrong version is the plausible one and will be
reached for again."* The third version stopped reading a pointer and started inferring from a file's
existence, which is the same move: a proxy that answers a *different* question. "Does a session
record exist?" is not "is this session over." `CLAUDE.md` rule 6 actively encourages writing the
record early — *"commit the scratchpad at every natural break, not at session end"* — so the
heuristic misfires precisely on sessions that follow the rule.

## Proposed fix — minimal, and it makes the wrong answer loud

1. **Search all lines, not just the last**, for a log already carrying this `session_id`. Cheap
   enough with a bounded tail read, and survives interleaving.
2. **Never guess another session's directory.** When no log carries this `session_id`, write to
   `scratchpad/session-<harness-sid>/` — a visibly foreign name. #119's docstring already states the
   principle (*"a wrong answer must be loud"*); the `openp[-1]` fallback violates it by producing a
   plausible-looking wrong answer, which is exactly how the previous two hid.
3. **Drop record-existence as the openness test.** It is a proxy for a fact nothing records.

Not applied here: this is `main`'s code, merged minutes ago, and #119 reasoned its design out at
length. The finding is reported rather than patched.
