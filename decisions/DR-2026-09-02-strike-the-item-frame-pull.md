# DR-2026-09-02-strike-the-item-frame-pull — Strike DR-2026-08-19 §12.1 step 2's item-frame query; replace it with an ICF-first frame pull.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0187` · category `D-DOCT` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-02 19:16 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-09-02.

## Rationale

The instrument contradicted itself at the point it was most trusted. §1.4 rule 1 says a slug is authored from the ICF/access-need frame first and the item list consulted for coverage 'never to supply one'; rule 2 says 'No value crosses' from an item name into a search_executions or search_candidates row. §12.1 step 2 ordered the frame pulled from items. A session obeying the runbook therefore broke the quarantine, and on 2026-09-01 one did: FRAME.md was derived from items and the item values '22 N' and 'PTV >=36' reached agonist queries. The step is also inert three times over -- items is empty, and item_axis_links and item_population_links were dropped by migration 065.

## Alternatives considered

- Amend §1.4 instead so the item frame becomes lawful -- rejected: §1.4 is the quarantine, and the measured harm ran the other way.
- Leave both and rely on sessions to notice -- rejected: one did not, which is why this exists.

## Notes, and what remains owed

Struck in place with the original text preserved, per the D-0181 precedent that editing a ratified DR's runbook is done under explicit owner ruling with the struck text kept in the record. THE REPLACEMENT STATES TWO GAPS RATHER THAN PAPERING OVER THEM, both created by the 2026-09-01 retraction and neither repaired: term_item_links was the only route from terms and term_aliases (88 and 2,382 rows) to a research subject and is now empty, so R11's terms_used has no slug route; and slugs.serves_axes is populated on 1 of 106 rows, so the cross-product the step pulls is generic rather than slug-specific. A runbook step that cannot execute is the defect this strike removes, so the step says only what is actually reachable.

## Delegation

Owner ruling amending a RATIFIED Decision Record. CLAUDE.md rule 0: a live owner statement supersedes every prior ratified record it touches, on contact.

## Artifacts

- `decisions/DR-2026-09-02-strike-the-item-frame-pull.md`
- `decisions/DR-2026-08-19-research-restart-operative-instrument.md`
