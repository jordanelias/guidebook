# `.claude/` — what lives here and why

The contract for this directory. It holds **harness wiring only**: things the
Claude Code runtime loads on its own, without an agent choosing to. Project
doctrine lives in `governance/`, process in `CLAUDE.md`, and the research
protocol in `skills/`.

**The organising principle, and it is this repository's own.** From
`.claude/settings.json`, on why the 2026-07-24 research run skipped Co-1,
citation mining, clause citation and combinatorial pairing while the rules for
all four sat documented:

> the rules did not fail; PROSE failed — an agent must choose to load it, and
> attention degrades as context fills.

So the test for putting something here is not "is this important?" It is: **does
this have to work when nobody remembers it?** If an agent must choose to read
it, it belongs in `governance/` or `skills/` and it is not enforcement.

---

## Layout

| Path | Loaded by the harness | Holds |
|---|---|---|
| `settings.json` | always | permissions and hooks |
| `hooks/` | fired by `settings.json` | the scripts hooks run |
| `agents/` | on `Agent` dispatch | subagent definitions, one per file |
| `commands/` | on `/<name>` | slash commands for repeated workflows |
| `skills/<name>/SKILL.md` | on `Skill` dispatch | **symlinks** into `skills/` |

Derive the inventory rather than trusting this table:

```
ls .claude/agents/ .claude/commands/
python3 scripts/sync_claude_skills.py --check
```

---

## `skills/` is the source of truth; `.claude/skills/` only points at it

The harness discovers skills at `.claude/skills/<name>/SKILL.md` and nowhere
else. This repository's 47 skills live at `skills/<name>_SKILL.md`, so until
2026-09-18 not one of them was loadable — they were found only when an agent
chose to read them, which is the failure mode above, reproduced 47 times.

`scripts/sync_claude_skills.py` links them. **Relative symlinks, never copies**:
CLAUDE.md rule 5, owner ruling 2026-08-24 — *"It is better to have a table cell
point to another table cell than to rewrite."* A generated copy of a skill body
is the same fact in a second home and drifts the first time either side is
edited; a parity check would only make the dual home survivable, therefore
permanent. A symlink has one home and cannot drift.

**The script never writes a `description`.** That field is what the harness
matches a task against, so a wrong one fires the skill on the wrong work — worse
than a missing one. Rule 8: where judgment is genuinely required the script asks
for it and never invents a value. Skills without one are reported by name and
left unlinked. Run the script to see which, and add the line to the source file:

```yaml
description: <when the harness should reach for this skill>
```

`claude_skills_loadable` (advisory) watches for drift. It is advisory because
skills still lack descriptions, so blocking would be red by construction — rule
6. Ratchet it to blocking once the script reports IN SYNC on a clean tree.

---

## `agents/` — match the model to the task, per subagent

The model belongs in the subagent's frontmatter, not in a sentence you have to
remember to type. Measured across the 12 preserved harness transcripts on
2026-09-18: Opus carried **74%** of all assistant turns and Haiku **0.16%**,
against ~12k recorded Bash calls that are overwhelmingly `cat`, `grep`, `ls` and
read-only `sqlite3` counts. There was no `agents/` directory at all, so the rule
existed only as prose. Re-derive before trusting those figures.

- **Mechanical work → Haiku.** `repo-sweep` (rule 4 caller sweeps), `db-census`
  (row counts, empty tables, unwritable FKs). Neither may adjudicate; both must
  show the command beside every figure.
- **Critique → a separate read-only definition.** `antagonist` runs on Fable with
  no write access and a prompt that attacks the claim. A model checking its own
  work is not a review.
- **Judgment, synthesis, writing → Opus.** `best_practice_synthesis` has an
  Opus floor that is doctrine, not preference.

A critic that can also write will fix what it finds and stop finding things.
Removing write access is the whole mechanism.

---

## `commands/` — for the prompt you have typed more than twice

Not for everything. A slash command earns its place when the same instruction
has been retyped across sessions and got shorter each time, losing a precondition
on every pass. `/orient`, `/session-open`, `/adversarial` and `/batch-done` are
each a prompt from this repository's own transcripts, written back out with the
preconditions restored.

`/session-open` exists because `scratchpad/CURRENT` moves at OPEN and the
`PostToolUse` hook writes every Bash call to whatever it names. Twice now a
session's commands have landed in a previous session's record.

---

## Hooks — and the one rule about writing them

Hooks are the only thing here that is genuinely enforcement. Two cautions this
repository paid for:

1. **Append `SessionStart` hooks, never insert at index 0.**
   `research_contract_hook.py` reads `SessionStart[0]["hooks"][0]["command"]` by
   hardcoded index; an insert turns the blocking `research_contract_sync` red
   with a diff that reads as contract drift.
2. **Never write a hook that demands a clean tree.** `transcripts/harness_*/main.jsonl`
   and `scratchpad/<session>/commands.jsonl` append on every turn by design, so
   the tree is dirty again the instant the hook is answered — unsatisfiable by
   construction, and the agent satisfying it commits and pushes in a loop. Scope
   the question instead:

   ```
   git diff --quiet -- :/ ':(exclude)transcripts/' ':(exclude)*commands.jsonl'
   ```

   `scripts/fix_stop_hook_loop.sh` patches the harness-side hook to read that
   exclusion from `git config stophook.ignorePath`. Run it once, locally.

A check that is red by construction teaches its reader to ignore it. That is the
most expensive failure available in this directory, because it discredits the
hooks that are working.
