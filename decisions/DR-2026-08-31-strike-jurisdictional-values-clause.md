# DR-2026-08-31-strike-jurisdictional-values-clause — OD-G: strike DR §12.1 Step 10's jurisdictional_values clause, and record the 2026-08-12 REFERENCE-ONLY ruling in the DB as a row-level note.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0181` · category `D-OP` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-31 22:14 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-31.

## Rationale

The runbook currently instructs the next research batch to write jurisdictional_values, which a
2026-08-12 ruling made REFERENCE-ONLY -- so the runbook walks the next batch into a forbidden
write. That is F-8. The ruling itself lives only in a YAML header comment, which is precisely
the class CLAUDE.md rule 4b names: a ruling that is in the repository, in a file, and still
fails to bind because the next session's search does not reach it. Putting it in the DB as a
row-level note also stops an emptied-by-ruling table from looking like an empty-for-want-of-data
one -- a distinction no gate can currently make.

## Alternatives considered

- Strike the clause only -- fixes the trap but leaves the ruling in a YAML comment where grep will
  not find it.
- Keep the clause and reverse the REFERENCE-ONLY ruling -- reverses a 2026-08-12 content ruling,
  which needs its own reasoning rather than being decided as runbook housekeeping.

## Notes, and what remains owed

jurisdictional_values holds 109 rows and is renamed research_code_leads by the parked migration
065; the note must survive that rename. Editing a RATIFIED DR's runbook is itself unusual and is
done here under an explicit owner ruling, with the struck text preserved in the DR record rather
than deleted.

## Delegation

Owner ruling. Population applicability, work-product inclusion and evidence-tier definitions are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable. The operative instrument DR-2026-08-19 §3 step 4a names
this batch "THE NEXT ACT, and it is the owner's, not a session's".

## Artifacts

- `workplan/2026-08-22-agonist-antagonist-execution-plan.md §2 OD-G`
