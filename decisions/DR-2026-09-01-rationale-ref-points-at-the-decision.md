# DR-2026-09-01-rationale-ref-points-at-the-decision — rationale_ref points at the DECISION that authorises the edge -- decisions.decision_id, a typed foreign key.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0183` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-01 19:20 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-09-01.

## Rationale

D-0175 (OD-A) rules these links substrate provisionally: any edge a determination relies on must
be re-derived and carry a rationale_ref in that determination's own migration. Measured
2026-08-31, that obligation was unenforceable -- rationale_ref was an unconstrained INTEGER with
no foreign key, so it referenced nothing and ANY integer satisfied "carries a rationale_ref".
Asked what it should point at, the owner ruled: the decision that authorises it. That makes the
column TEXT REFERENCES decisions(decision_id), so a fabricated warrant is refused by the
database rather than by attention.

## Alternatives considered

- Point at evidence_sources.ref_id -- rejected by the ruling; an edge is authorised by a
  decision, and the evidence behind that decision is reached through it by pointer.
- Leave it untyped and enforce by check -- rejected: a check reads what a constraint could have
  refused, and every one of the 372 rows proved the column inert.

## Notes, and what remains owed

The column stays NULLABLE and all 530 existing rows keep NULL. OD-A's debt is paid where an edge
is USED, and making it NOT NULL would either forge 530 warrants or block the table entirely.
This also discharges the correction D-0175's own notes demanded: the parked 065 generator
DROPPED rationale_ref on the grounds that it was 0 of 372 populated, and OD-A makes it the
column where the debt is paid. It is kept.

## Delegation

Owner ruling. The lens taxonomy and how a reader browses the book are doctrine -- mission,
audience and population taxonomy sit in governance/decision-protocol.md's DG-NON class, and
CLAUDE.md rule 0 makes a live owner statement non-delegable and superseding on contact.

## Artifacts

- `scripts/migrations/065_one_link_table_four_lenses.sql`
