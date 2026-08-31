# DR-2026-08-27 — The pipeline is SEVEN stages and `base` is the first: Base, Research, Evidence, Judgment, Synthesis, Specification, Render

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0167` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-27. Ends the "substrate is not a stage" convention, which was
agent-coined on 2026-08-24 and used as canon for three days. Supersedes the five-stage list
(2026-08-25) and the six-stage list (2026-08-27 am).

## Rationale

The owner ruled base a stage because "it supplies the base information upon which research can
perform its task, and it doesn't belong under research because none of it IS research. it's the
first layer of information." Re-deriving both live figures under base-as-stage-1, using the R1
audit assignment: foreign keys go from 21/59 to 49/31 cross-stage/within, reclassifying 28 keys
and taking cross-stage from 26% to 61% of the schema's 80; cross-stage views go from 9 to 10 of
18. The long-quoted "43/37 on eight columns" matches neither convention and is void. Because a
cross-stage view IS the pointer, the protected set grows, and the view that joins it is
v_coverage_priority (base+research, 7,208 rows) -- the matrix view, which two successive plans
proposed deleting.

## Alternatives considered

- Keep substrate outside the stage set (the retired convention) -- rejected: the owner ruled
base supplies what research consumes, so it is a producing layer, and "substrate" was never
owner vocabulary.
- Fold base under research -- rejected by the owner in terms: none of base IS research.

## Notes, and what remains owed

Companion ruling recorded the same contact: a table is never a stage ("Slugs isn't a stage as
that word doesn't actually make sense for it"). Neither governance/pipeline-contract.yaml nor
tools/pipeline_completeness.py has been updated; both still enforce five stages. Propagation
owed.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
- `references/owner-notes/2026-08-27-architecture-note.md`
- `scratchpad/session_2026-08-27-hook-audit/audits/R1-stage-assignment.md`
