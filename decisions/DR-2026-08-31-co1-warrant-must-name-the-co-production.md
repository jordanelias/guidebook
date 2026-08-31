# DR-2026-08-31-co1-warrant-must-name-the-co-production — OD-D: a Co-1 tier is unwarranted-pending unless co1_provenance NAMES the co-production. 'published_corpus' is not a co-production warrant.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0178` · category `D-METH` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-31 22:14 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-31, RE-PUT after measurement refuted the question's own premise.

## Rationale

The question as tabled in the 2026-08-22 plan asserted co1_source_type and co1_provenance were
NULL on all three Co-1 sources. Measured 2026-08-31, that is FALSE: REF-00965, REF-00966 and
REF-00968 all carry co1_source_type='peer_reviewed_literature' and
co1_provenance='published_corpus'. The ruled NULL test would therefore have fired on ZERO rows
-- a gate that examined nothing (CLAUDE.md §2a), on the only slug in the project that holds
evidence. The re-put ruling fixes the substance rather than the field's nullity:
'published_corpus' states where a source was PUBLISHED, not that disabled people CO-PRODUCED it,
and co-production is the entire Co-1 warrant under CRPD Art 4.3. CLAUDE.md §6: 'when you cite
lived-experience work, the disabled people who produced it are part of the evidence, not
metadata.'

## Alternatives considered

- Keep the NULL test as first ruled -- rejected on measurement: it examines nothing here.
- Defer entirely pending full texts -- weighed; nothing blocks on it, but it leaves Co-1
  unenforced on the one slug that uses it.

## Notes, and what remains owed

CONSEQUENCE, STATED BECAUSE IT IS UNCOMFORTABLE: all three Co-1 sources are unwarranted-pending
under this rule TODAY, including REF-00966 -- which the 2026-08-22 plan says DOES state a
participatory method and DOES carry autistic community co-authors. So REF-00966's RECORD is
wrong, not its tier: the fix is to correct co1_provenance upward from the retrieved payload, not
to drop the tier. REF-00965 and REF-00968 remain referred, needing full texts this environment
cannot reach. ALSO MEASURED: evidence_sources.tier has NO CHECK constraint, so tier is not
machine-enforced at all and dbcore.check_values returns an empty set for it -- an enforcing
check for this rule cannot lean on the column's own vocabulary.

## Delegation

Owner ruling. Population applicability, work-product inclusion and evidence-tier definitions are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable. The operative instrument DR-2026-08-19 §3 step 4a names
this batch "THE NEXT ACT, and it is the owner's, not a session's".

## Artifacts

- `workplan/2026-08-22-agonist-antagonist-execution-plan.md §2 OD-D`
- `governance/tier-system.md`
