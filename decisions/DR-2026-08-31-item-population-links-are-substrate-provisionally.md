# DR-2026-08-31-item-population-links-are-substrate-provisionally — OD-A: item_population_links are SUBSTRATE, provisionally -- any edge a determination relies on must be re-derived and carry a rationale_ref in that determination's own migration.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0175` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-31 22:14 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-31. Unblocks every determination. The alternative readings were
substrate-unconditionally (rejected: writes the debt off) and scaffolding (rejected: makes no
cell determinable anywhere).

## Rationale

Measured 2026-08-31 against the live schema: item_population_links holds 372 rows and
rationale_ref is NULL in ALL 372; 358 of them were written by one session,
session_2026-05-11-items-population-normalization, with 9 from session_2026-07-24-e08-inclusion-
repair and 5 from session_2026-07-13-contradiction-sweep-f07-recovery. So the concern is real
and concentrated, not diffuse. 'Provisionally' converts 372 silent assertions into a debt paid
where it is used rather than all at once or never. This is the ruling the instrument blocks step
5 behind, and it is F-5 in the 2026-08-22 agonist-antagonist plan.

## Alternatives considered

- Substrate unconditionally -- rejected: the 2026-05-11 session's assertions would never be
  examined and the debt is written off rather than paid.
- Scaffolding, quarantined under D-1 -- rejected: it makes NO cell determinable anywhere until all
  372 are re-derived, which stops determination work entirely.

## Notes, and what remains owed

THE OBLIGATION NEEDS AN ENFORCER OR IT DECAYS. 'Provisionally' is a standing requirement on
every future determination migration; with nothing reading it, it becomes 'substrate
unconditionally' by inattention -- CLAUDE.md §1's ratchet running the other way. A check is owed
that fails a determination migration citing an item_population_links edge whose rationale_ref is
still NULL. NOT built in this batch: the first such migration does not exist yet, so the check
would be vacuous today (§2a), and its subject arrives with OD-B's links. INTERACTION WITH THE
PARKED RENAME: migration 065 folds item_population_links into base_item_taxonomy_links and DROPS
rationale_ref, justified by it being 0 of 372 populated. OD-A makes that column the place the
debt is paid. The 065 generator must be corrected before it lands.

## Delegation

Owner ruling. Population applicability, work-product inclusion and evidence-tier definitions are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable. The operative instrument DR-2026-08-19 §3 step 4a names
this batch "THE NEXT ACT, and it is the owner's, not a session's".

## Artifacts

- `workplan/2026-08-22-agonist-antagonist-execution-plan.md §2 OD-A`
