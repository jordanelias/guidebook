# DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many — A taxonomy link may be ABSENT from a lens, MUST tie to at least one, and IDEALLY ties into many.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0182` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-01 19:20 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-09-01.

## Rationale

Given in three messages during the lens-architecture investigation: "it is OKAY for a link to be
absent in a related taxonomy column", "but a link MUST be tied to at least one", "and ideally it
ties into many". Together they are a cardinality rule over the four lenses of D-0170, and they
settle a question the schema could not: whether a link row states ONE taxonomy or several. It
states as many as are known, and at least one. The owner's own example -- an evidence row
concerning ICF codes for assistive mobility devices that also concerns wheelchair identity and
also paraplegia medically -- is one fact, so it is one row. Measured 2026-09-01: the rule is
expressible in SQLite as a table-level CHECK (COALESCE(identity_code, icf_code, needs_code,
medical_code) IS NOT NULL), which admits the four-lens row, admits a single-lens row with three
NULLs, and refuses a row that states no lens at all. All three were tested against the live
shape before this was recorded.

## Alternatives considered

- Exactly one lens per row (CHECK (...) = 1) -- this was the parked design in the migration 065
  generator, and the ruling reverses it: it forbids the owner's own wheelchair example, which is
  one fact stating three lenses.
- No constraint at all -- rejected by the ruling's second clause; a link tied to no taxonomy is
  unreachable from every lens and renders nowhere.

## Notes, and what remains owed

The ideally-many clause is an AUTHORING aim, not a constraint, and is deliberately not
mechanised: a CHECK demanding two lenses would refuse the 372 identity-only rows that already
exist and every honest single-lens fact after them. What the crossing maps become is the aid to
it -- when an identity link is recorded they suggest the ICF and needs codes that probably
belong on the same row, for a human or a synthesis step to confirm. They stop being render
machinery.

## Delegation

Owner ruling. The lens taxonomy and how a reader browses the book are doctrine -- mission,
audience and population taxonomy sit in governance/decision-protocol.md's DG-NON class, and
CLAUDE.md rule 0 makes a live owner statement non-delegable and superseding on contact.

## Artifacts

- `scripts/migrations/065_one_link_table_four_lenses.sql`
- `scratchpad/session_2026-09-01-lens-architecture/LENS-ARCHITECTURE.md`
