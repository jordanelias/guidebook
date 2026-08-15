# DR-2026-08-15 — `SUPERSEDED` is retained as a status value

**Status:** OPERATIVE — 2026-08-15.
**Decision by:** Owner ruling 2026-08-15 — "yes we keep superseded".
**Category:** D-SCHEMA (enum membership — Change-Order gated).
**Delegation:** DG-NON — owner-originated; this record captures it.
**Amends:** `DR-2026-08-14-status-vocabulary-ratification` (D-0161).
**Implemented by:** schema migration `060_restore_superseded_status.sql`.

---

## 1. The decision

`SUPERSEDED` is a live status value on both `decisions.status` and `conflicts.status`. **The ratified
vocabulary is nine words, not eight:**

`ACTIVE` · `PROPOSED` · `DEFERRED` · `RESOLVED-EVIDENCE` · `RESOLVED-CONSENSUS` · `UNRESOLVED` ·
`CLOSED` · `RETIRED` · `SUPERSEDED`

## 2. What this reverses, and why the reversal is right on the merits

Migration 058 retired `SUPERSEDED`. **The owner's 2026-08-14 ruling did not ask for that.** The
ruling named eight words and said nothing about this one; I inferred the retirement, flagged the
inference in writing, and implemented it in the same turn.

The inference rested on two grounds. The first — no row has ever used the status — is true. The
second was **false**: I wrote that `decisions.supersedes` already carried the successor relation on
every row. It is `'[]'` on all 162 rows and has never been written to. The check that produced the
claim tested `supersedes != ''`, and `'[]'` is a non-empty *string*, so it counted 162 strings and I
reported 160 populated arrays. What *is* populated is the inverse column, `predecessors`, on 51 rows.

**The word earns its place on the merits, not merely because the owner said so.** `SUPERSEDED` and
`RETIRED` are not synonyms:

| Word | Says |
|---|---|
| `SUPERSEDED` | replaced, and a successor exists |
| `RETIRED` | removed, and no successor exists |
| `CLOSED` | finished, without an evidence resolution |

Collapsing `SUPERSEDED` into `CLOSED` would make *"was this replaced, and by what?"* unanswerable
from the status. With `supersedes` empty on every row, the status word was carrying that signal
alone — so the retirement would have deleted the last remaining carrier of the fact, not a redundant
second copy of it. My own false premise was the thing that made the retirement look safe.

## 3. Scope of the change

Widening a CHECK cannot invalidate an existing row, and zero rows carry `SUPERSEDED`, so **migration
060 makes no data change** — unlike 058, the table copy is a straight `SELECT *` with no inline
remap. Nine call sites were swept back: both CHECK constraints, `schemas/enums.py`,
`schemas/conflict.py`, `scripts/db.py`, `scripts/validate_conflict.py`,
`scripts/validate_conflicts.py`, the conflict-mapper skill, and the DDL reference in
`architecture/sqlite-data-layer.md`.

`governance/retired-vocabulary.yaml` no longer lists `SUPERSEDED` among the deferred retirements. Its
entry there had been correct for a different reason — the word is load-bearing across the whole
supersession model (`time-model.md` §4, `SupersedenceType`, `StandardStatus`, and every DR that
supersedes another) — and that reasoning is now moot rather than wrong: the word is not retired in
any sense.

## 4. What this says about the process, kept rather than tidied

The defect was not the inference. Flagging a reading and asking is legitimate; I did flag it. The
defect was **acting on it in the same turn**, on a premise I had measured wrongly, in a decision the
owner had just worded precisely — and then carrying that premise into a DR, an attestation, two
register stores, five commit messages and a PR description, all of which went green.

**No gate caught it.** Every mechanical claim was verified and every claim about *why* went
unchecked, because the gates read schemas and constraints, not reasoning. It surfaced only when the
owner asked for a re-derivation, one instruction after the fact.

The operative lesson for the remaining decision groups: **an inference that extends an owner ruling
gets held for the next exchange, not shipped alongside it** — even when it looks free, and
especially when the thing making it look free is a number I measured myself.
