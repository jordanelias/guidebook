# DR-2026-08-27 — The evidence item is the SOURCE; the judgment item is the extracted, tiered, categorised value. Evidence to judgment is 1:N

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0168` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-27, adopting item #2 of the architecture note.
source_value_extractions re-assigns from evidence to judgment.

## Rationale

The owner: "one evidence source may provide many rows of judgment (eg a code document like
Canada's NBC 3.8)", and judgment "determines category of judgment item, derives
value/process/figure/goal for it". So the value is derived at judgment, not evidence, and the
evidence row is the source record. This moots three findings the adversarial passes had raised
as blockers: A3-F3 (the lead key put a per-source fact on a per-extraction row), A3-F18 (the
population-match grain conflict), and my own rejection of the 25-grades-over-10-sources
measurement as the wrong edge -- it was always the right edge. judgment_items is not a new table
needing a designed column set; it inherits the extraction table.

## Alternatives considered

- 1:1 with UNIQUE(evidence_item_id) -- rejected by the owner's own worked example, a code
document yielding many clause-level judgments.
- Keep extraction in evidence collection -- rejected: it puts the tier verdict and the derived
value in a stage the owner defines as a cursory scan.

## Notes, and what remains owed

Owed and not free: the tier verdict is a judgment output but `tier` is a column on
evidence_sources. Measured 2026-08-27: 40 Python files name evidence_sources, 78 Python lines
name a tier field, 26 skills teach tier. Writer-retire, reader-retire, NULL forward. Queued, not
done.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
- `references/owner-notes/2026-08-27-architecture-note.md`
