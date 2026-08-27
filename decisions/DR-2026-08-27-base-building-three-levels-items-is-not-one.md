# DR-2026-08-27 — base_building holds three levels -- building type, room type, construction element -- and `items` is none of them

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0171` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-27. The 2026-08-26 ruling that `items` is the Part-4 render
rollup therefore stands unamended.

## Rationale

The owner: "Building types (eg residential, commercial), room types (eg kitchen, entry,
bathroom), construction elements (eg door, door handle, window, floor) are what I wanted for
that table." Measured: only the middle level exists (rooms, 17 rows -- R-KIT, R-ENT, R-BA);
building types and construction elements have no table. items (93) holds design provisions ABOUT
elements, e.g. A-03 "Acoustic Door (STC >=35) at All Sensitive Space Boundaries". This explains
a defect already on the record: 42 of 93 item names carry a determination in the label because
items conflates the element (door), the parameter (STC) and the determination (>=35), with no
element table and no parameter registry to hold them apart. The proposed vocabulary check treats
the symptom; the three-level split removes the cause.

## Alternatives considered

- Rename items into base_building -- rejected on measurement: items holds provisions, not
elements.
- Three separate tables -- weighed against one self-referential table, because the owner said
"that table" and separately ruled parent columns; a parent across three tables is polymorphic,
which SQLite cannot key. Shape recorded as open in the agonist-antagonist pass.

## Notes, and what remains owed

items.category holds 10 distinct bare letters A-K with no category-name table anywhere -- the
same collapse a second time.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
- `scratchpad/session_2026-08-27-rename-execution/AGONIST-ANTAGONIST.md`
