# DR-2026-08-14 — One ratified status vocabulary for decisions and conflicts

**Status:** OPERATIVE — 2026-08-14 (implemented 2026-08-15 by schema migration 058).

> **CORRECTED 2026-08-15, on a re-derivation of this record's own claims.** Two statements below
> were wrong when first written, and both are corrected in place with the error named rather than
> quietly amended:
>
> 1. **`decisions.supersedes` does not carry the successor relation on "all 160 rows".** It is `'[]'`
>    on **all 162 rows** — nothing has ever been written to it. The original check tested
>    `supersedes != ''`, and `'[]'` is a non-empty *string*: it measured string emptiness and
>    reported array population. This **weakens the stated grounds for retiring `SUPERSEDED`** (§3).
> 2. **The Mode-S vocabulary retirement is dated 2026-07-13, not 2026-07-21**, and its authority is
>    Item V of `RATIFICATION-PACKAGE-2026-07-12`, ratified in full by owner directive
>    (`RATIFICATION-RECORD-2026-07-13` A5). The corrected fact is worse than the original claim, not
>    better — see §3.
**Decision by:** Owner ruling 2026-08-14, given in five parts across two messages.
**Category:** D-SCHEMA (enum birth and retirement — Change-Order gated).
**Delegation:** DG-NON — owner-originated and owner-worded; captured here, not proposed.
**Amends:** `data/guidebook.db` (`decisions.status`, `conflicts.status` CHECK constraints),
`schemas/enums.py`, `schemas/conflict.py`, `scripts/db.py`, `scripts/validate_conflict.py`,
`scripts/validate_conflicts.py`, `scripts/audit_consolidator.py`,
`governance/retired-vocabulary.yaml`, `skills/cross-population-conflict-mapper_SKILL.md`,
five conflict matrices, three architecture documents.

---

## 1. The decision

Eight words, one list, both tables:

| Word | Means |
|---|---|
| `ACTIVE` | live; not yet closed or resolved |
| `PROPOSED` | put forward, not yet in force |
| `DEFERRED` | deliberately not addressed this pass |
| `RESOLVED-EVIDENCE` | resolved by direct evidence |
| `RESOLVED-CONSENSUS` | resolved by claims directly derived from direct evidence |
| `UNRESOLVED` | worked, and does not resolve at this scale |
| `CLOSED` | finished without an evidence resolution |
| `RETIRED` | removed from force without a successor |

The owner's words, verbatim, because three of the five parts carry reasoning that the word list
alone does not:

> "ADOPT RETIRED, DROP WITHDRAWN"
>
> "PROPOSED = PROVISIONAL FOR ME IN THIS PROJECT"
>
> "RESOLVED-EVIDENCE AND RESOLVED-CONSENSUS ARE ONLY TO BE USED FOR DIRECT EVIDENCE OR CLAIMS
> DIRECTLY DERIVED FROM THEM. OTHERWISE 'CLOSED' FOR ITEMS LIKE FINISHED INFRASTRUCTURE ITEMS"
>
> "DEFERRED IS DIFFERENT THAN OPEN BECAUSE IT ALLOWS US TO TELL (AND POSSIBLY WITH A COUNTER) HOW
> MANY TIMES WE HAVE CHOSEN TO NOT ADDRESS IT"
>
> "THEN REPLACE 'OPEN' WITH 'ACTIVE'. ONLY ONE SURVIVES"

**The reservation is the substantive half.** `RESOLVED-EVIDENCE` and `RESOLVED-CONSENSUS` are not
general-purpose "done" markers. They assert an evidentiary basis, and the ruling restricts them to
direct evidence or claims directly derived from it. Anything else that finishes — infrastructure
built, question withdrawn, work overtaken — is `CLOSED`. This keeps the two resolved words meaning
what the tier system says they mean rather than degrading into administrative closure, which is
exactly how an evidence vocabulary rots.

**`DEFERRED` is a measurement, not a mood.** It is distinct from `ACTIVE` because it records that a
choice was made not to act. The owner raised a counter for how many times something has been passed
over; that column is **not built here** — see §5.

## 2. What was broken

Two layers policed these fields and disagreed.

| Field | Database accepted | Python accepted |
|---|---|---|
| `decisions.status` | ACTIVE, SUPERSEDED, **WITHDRAWN**, PROPOSED, PROVISIONAL | PROPOSED, PROVISIONAL, ACTIVE, SUPERSEDED, **RETIRED** |
| `conflicts.status` | RESOLVED-EVIDENCE, RESOLVED-CONSENSUS, **RESOLUTION-PROPOSED, UNRESOLVED, MODE-S-ONLY** | RESOLVED-EVIDENCE, RESOLVED-CONSENSUS, **UNRESOLVABLE-MODE-S, DEFERRED, OPEN** |

Which word was legal depended on whether the write went through Python or SQL. On conflicts the two
sets shared two words of five. No row used any contested value, so nothing had failed yet — the
divergence was waiting for the first real write, and the corpus will never be this small again.

## 3. Retirements, and what happened to the meaning each carried

| Retired | Becomes | Note |
|---|---|---|
| `WITHDRAWN` | `RETIRED` | Owner ruling 1. 0 rows. |
| `PROVISIONAL` | `PROPOSED` | Owner ruling 2. 1 row — D-0139, remapped by migration 058. |
| `OPEN` | `ACTIVE` | Owner ruling 5. File layer only. |
| `SUPERSEDED` | `CLOSED` | **Not named in the ruling.** See below. |
| `RESOLUTION-PROPOSED` | `PROPOSED` | Direct synonym; no meaning moves. |
| `MODE-S-ONLY` | `UNRESOLVED` | **Not a pure rename.** See below. |
| `UNRESOLVABLE-MODE-S` | `UNRESOLVED` | The file layer's spelling of the same state. |

**`SUPERSEDED` was retired on a reading, not on an instruction — and one leg of that reading was
false.** The ruling did not name the word. It was put back to the owner before implementation and
implemented in the same turn on two grounds: that zero rows used the status, and that the relation it
encoded was already carried by `decisions.supersedes`.

**The first ground holds. The second does not.** `supersedes` is `'[]'` on all 162 rows — the column
has never been written to. What *is* populated is its inverse, `predecessors`, on **51 rows**. So the
successor relation is recorded in this table, but by the backward pointer, and the column I cited as
the status word's replacement is empty everywhere.

The corrected position: retiring `SUPERSEDED` costs nothing today (no row used it, and the relation
is recoverable from `predecessors`), but the claim that a populated pointer already did the job was
wrong. **Reversal remains one line in the CHECK and one in the enum**, and this is the item in this
DR most worth the owner overturning, because it is the only one the owner did not word.

**`MODE-S-ONLY` carried information that `UNRESOLVED` alone does not.** It meant *irreconcilable at
population scale, requires individual co-design* — not merely *unresolved*. Collapsing the two words
without moving that meaning would have destroyed a distinction the conflict matrices depend on. The
distinction now lives where it belongs: the status says the conflict does not resolve at this scale,
and `mode_s_trigger` / `unresolvable_residual` name the Person-Mode handoff. The five swept matrices
say it in words beside the status rather than losing it. `schemas/conflict.py`'s validator, which
required `mode_s_trigger` whenever the status was `UNRESOLVABLE-MODE-S`, now keys on `UNRESOLVED` —
the rule is unchanged, only the word it watches.

**This word's survival is a sharper finding than "it outlived a sweep", and the re-derivation is what
sharpened it.** The authority is **Item V of `RATIFICATION-PACKAGE-2026-07-12`**, ratified *in full*
by owner directive on **2026-07-13** (`RATIFICATION-RECORD-2026-07-13`, A5: "G1–G8, Item V, Item R,
in full"). Item V does not merely deprecate "Mode P/S" in prose. It names the work in its own words:

> vocabulary normalization: Universal/Population/Person Mode as sole design-scale names; "Tier N"
> reserved for evidence; "Mode P/S" deprecated (96 files; **one real data migration:
> `conflicts.status` CHECK**).

So the ratified decision **enumerated the single migration it required, and that migration was never
run** — for a month, until migration 058 finally changed that CHECK, by a different route than Item V
anticipated (collapsing to `UNRESOLVED` rather than coining a Person-Mode spelling, per the
2026-08-14 ruling).

That is this repo's characteristic defect in its most literal form: not a sweep that missed a file,
but a ratified decision that *listed* its one migration and did not execute it. It is the reason the
sweep here was run to completion before the migration was committed rather than after.

## 4. One shared list rather than per-field subsets

The ruling names a flat set of words for the project, not two lists. Both tables therefore accept
all eight.

The alternative — a narrower per-field subset, so that a decision could not be marked
`RESOLVED-EVIDENCE` — was rejected on reversibility. A superset can be narrowed by a forward
migration once usage shows which words a field never legitimately takes. A too-narrow CHECK refuses
a legitimate write the first time someone makes one, and refusal at the database is the expensive
kind of wrong. Precision here should come from usage evidence, which does not exist yet on a table
with zero rows.

## 5. Deliberately not built

**The deferral counter.** The owner raised it as a possibility ("and possibly with a counter"), and
it was offered as part of this work; the offer was not taken up, so no column was added. When it is
wanted it is a small forward migration — `defer_count` plus a last-deferred date, incremented on
transition into `DEFERRED`. Building it unasked would have been a schema decision made by the
implementer.

**The `mode_s_trigger` field name.** Still retired vocabulary. Renaming a schema field is a
structural change with its own caller sweep and its own Change-Order; the ruling was about status
values. Recorded here so it is visibly filed rather than missed.

## 6. Enforcement

- **Database:** `CHECK(status IN (…))` on both tables, migration 058. Verified in both directions:
  all eight ratified words accepted, all four retired decision words refused.
- **Python:** `schemas.enums.DecisionStatus` and `schemas.conflict.RATIFIED_STATUSES`, mirrored in
  `scripts/db.py`, `scripts/validate_conflict.py` and `scripts/validate_conflicts.py`.
- **Text:** `governance/retired-vocabulary.yaml` RV-022/023/024 for the three mechanically-matchable
  spellings, all at zero occurrences after the sweep. `WITHDRAWN`, `PROVISIONAL`, `SUPERSEDED` and
  `OPEN` are recorded in `deferred:` with their reason: each is load-bearing under a *different*
  live vocabulary nobody retired — `StandardStatus`, `cost_data_quality`, the whole supersession
  model, and `verification_disposition`'s literal `OPEN|CLOSED`. A literal match on any of the four
  would fire on hundreds of correct lines and train readers to ignore the check. The CHECK
  constraints enforce all four anyway, at the database rather than by grep.

## 7. Replay ordering — recorded because it constrains any future enum change

`migrate_db.py` applies **all** schema migrations before **any** data migration. D-0139's
`PROVISIONAL` value arrives inside the 057 baseline, i.e. in the schema phase, so it is already
present when 058 runs. A paired data migration could not have fixed it: that replays *after* the new
CHECK exists, by which point the rebuild has already failed. The value is therefore remapped inline
in the table copy.

Migrations 055 and 025 record the same collision from the other side. 025 resolved it by withdrawing
a same-day migration; 055 by moving DDL into the data phase. Neither was available here, and neither
was needed, because the offending value originates in the schema phase.

The remap is narrow on purpose. `WITHDRAWN` and `SUPERSEDED` were verified at zero rows, so no `CASE`
arm exists for them: if either ever appears in replay the copy fails loudly rather than silently
rewriting a value nobody ratified.

## 8. Verification

- Rebuild from migration history reproduces exactly — shallow and `--deep` both PASS.
- 18 views execute; zero row-count drift across 67 tables; `integrity_check` ok; no FK violations.
- `test_db_integrity` 72/72 — including L01, which caught this session's own dual-store divergence
  (the DB moved D-0139 while the YAML still said `PROVISIONAL`) and was reconciled toward the DB per
  `CLAUDE.md` §9-5.
- `validate_schema` 20/20.
- `run_checks.py --all`: 43 green, 16 nothing-in-scope, 6 advisory failures, 0 blocking — identical
  to a clean baseline of `origin/main`, same six names. Failure-neutral in both directions.
- `validate_conflict.py`'s 11 errors are the pre-existing unknown-population-code backlog
  (`references/tooling-register.md` §8, standing item 8), unchanged at 11 errors / 14 warnings.
