# DR-2026-09-11 — Adjudication is delegated for a named set of items, and the medical lens gets filled out

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that a
live owner statement supersedes every prior ratified record it touches **on contact**. This record
exists so the ruling is citable by the machine and findable by a reader, not to confer validity it
already has.

**Register row:** `D-0188` · category `D-DOCT` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-11 01:20 · `data/decisions/decision_register.yaml`

> **This file is HAND-WRITTEN, and the header other DR files carry is wrong.** Those files say
> *"This file is GENERATED from its register row"* and **no generator exists** — commit `06ceda8`
> hand-wrote eight of them beside the register edit. C9 lives in `scripts/decision_capture.py`, not
> in `run_checks.py --selftest`, and it checks only that each DR file is cited by *some* register
> row, never its content. So a decision costs three hand-maintained homes: the register row, this
> file, and the `decisions` table row. That is a rule-5 dual home the project already carries. It is
> named here rather than discovered again.

## Outcome

ADOPTED by owner ruling 2026-09-11. Adjudication of the escalated item set is delegated; the owner
takes an overseer posture; the medical-lens taxonomy is filled out.

## Rationale

The owner, verbatim: *"Fable 5.1 to adjudicate and resolve all items that are presented to me. Opus
to execute in agonist-antagonist method. Ensure that medical gets filled out."*

**Clause 1** supersedes the Delegation clauses of D-0170, D-0169 and D-0182, and
`governance/decision-protocol.md` §2.4 items 2–3, **as applied to the enumerated items and no
further**. The DG-NON list is not amended generally. The owner named a queue, not a class.

**Clause 2** sets the execution method: agonist builds, antagonist attacks the specific claim, and a
task is done when the antagonist reports what it attacked the claim *with*.

**Clause 3 enforces D-0170 rather than deciding anything.** D-0170 adopted the medical lens on
2026-08-27. The session had escalated it as open anyway. The escalation is withdrawn, and the reason
it happened is recorded in `references/project-standards.md`: an empty table was read as an open
question instead of as a ratified ruling awaiting execution.

## Alternatives considered

- Read the delegation as reaching the DG-NON class generally — rejected: the owner named items
  presented to them, and widening it would be an agent enlarging its own authority.
- Decline the delegation as inconsistent with D-0170's non-delegable clause — rejected by rule 0:
  that clause is precisely what the ruling changes, and a ratified record is never an argument
  against the ruling that changes it.

## Consequence recorded, because it would otherwise be found the hard way

D-0170's stated mechanism for lens-switching — *"a medical taxonomy needs the same crossings into the
other three or the lens cannot switch"* — was superseded on 2026-09-01 by D-0184, which made the lens
a **column**: render is `WHERE medical_code = ?`. The crossings remain required as the authoring aid
and the coverage measure, not as the render path. **A session citing D-0170 alone would build the
wrong thing while correctly citing a ratified DR.**

## Artifacts

- `references/project-standards.md` (entry dated 2026-09-11)
- `scratchpad/pr-134-repository-orientation/ADJUDICATION.md`
