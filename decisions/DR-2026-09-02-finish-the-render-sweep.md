# DR-2026-09-02-finish-the-render-sweep — Finish the render sweep: archive the site surfaces that publish the deleted item layer.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0186` · category `D-OP` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-02 19:15 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-09-02, choosing option B of two put to the owner.

## Rationale

The 2026-09-01 retraction deleted site/specs and stopped, leaving site/populations publishing 172 links across 79 item codes and both index pages pointing into a directory that no longer existed. No gate caught it because validate_cross_refs treats site/ as REFERENCE_ONLY. DR-2026-08-19 §1.2 had predicted exactly this: 'archiving the items rows quarantines none of this -- a researcher who greps the repository for their slug will meet the old answer before they have logged their first search.' Leaving the surface half-swept was the one disposition ruled out: neither frozen nor swept, just broken.

## Alternatives considered

- Treat site/ as a frozen reference surface and restore site/specs -- rejected by the owner: it keeps publishing determinations the data no longer holds.
- Leave the state as it was -- ruled out before the choice was put: half a rendered surface is not a disposition.

## Notes, and what remains owed

CORRECTS AN EARLIER SESSION ERROR. The 93 spec pages were deleted outright on 2026-09-01. CLAUDE.md §1 holds that git history is the archive for CODE and _archived/ is the right home for retired CONTENT; rendered pages are content. They are restored to _archived/site/specs/, which also makes the archived index.html's relative links resolve, and root index.html's six links are repointed there. UNEXPLAINED, STATED RATHER THAN TIDIED: two pages, [cross-cutting].html and [unassigned].html, arrived in the restore set. They are real rendered pages appearing nowhere in git history -- 93 were deleted and 93 existed at befaa29^. Kept because they are content, but the mechanism by which they entered the set was not reconstructed and no mechanism was invented. OWED: root index.html still states the determination 'Corridor Clear Width (>=1200 mm Minimum on All Primary Routes)' as fact on its front page. Rewriting the landing page's framing is mission-level content and was not done here.

## Delegation

Owner ruling. What the project publishes is work-product inclusion, DG-NON under governance/decision-protocol.md.

## Artifacts

- `decisions/DR-2026-09-02-finish-the-render-sweep.md`
- `_archived/site/`
