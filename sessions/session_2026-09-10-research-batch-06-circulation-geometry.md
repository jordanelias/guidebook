# Batch 06 — ramp gradient (TERM-001) × MOB

> **THIS RECORD WAS RECONSTRUCTED ON 2026-09-13 BY A LATER SESSION**
> (`session_2026-09-13-research-batch-07-corridor-width`), from the committed artefacts only —
> the database rows created under this session id, its migrations, its retrieval-log manifest and
> `scratchpad/pr-134-repository-orientation/HANDOFF.md`. Batch 06 closed without executing runbook
> step 8: no session record, no attestation, and both pointer files were left naming batch 05.
> **Nothing here is recalled; every figure was derived from `data/guidebook.db` after the fact.**
> Where the artefacts do not establish something, this record says so rather than filling it in.

**Session id:** `session_2026-09-10-research-batch-06-circulation-geometry`
**Cell:** `parameter_id 1` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry`
**Outcome:** `specification_id 1` — **`stated`**, `tier_basis T1`, `derivation_sha 75c34f1d82b5…`,
governed by REF-00973, REF-00974, REF-00979, REF-00980. `value_min/max/unit` NULL.

## Derived figures

| | |
|---|---|
| searches logged | 3 |
| sources admitted | 2 (REF-00979 Chow 2009, REF-00980 Sanford 1997 — both Tier 1) |
| slug-linked Tier 1–2 sources | 2 |
| candidates staged | 2 |
| concept observations | 6 |
| population matches | 3 |
| citation-mining passes | 2 |
| extractions on parameter 1 | 4 |
| parameters minted | 1 |
| determinations | 1 |

## Why this record exists now

`sessions/LATEST-RESEARCH` feeds the **blocking** `citation_mining_session` gate, and
`test_db_integrity`'s **L04** fails when that pointer names a session holding zero slug-linked
Tier 1–2 sources — because then the gate examines nothing and passes. Batch 07 admitted only Tier 3
sources, so pointing the mining gate at batch 07 would have hollowed it out. Batch 06 is the newest
session actually inside that gate's scope, and it had no record for the pointer to name.

So this is not tidiness: **batch 06's two Tier 1 admissions had never been audited by any
session-scoped check**, because the pointer stayed on batch 05 from 2026-09-02 until today.

## What the artefacts establish, and what they do not

The determination and its inputs are fully recorded in the database and in
`scripts/migrations/data_20260911*.sql`. The reasoning that produced them is recorded in
`scratchpad/pr-134-repository-orientation/HANDOFF.md`, which is committed and which this record does
not restate.

**What the attestation beside this file does and does not cover.** An attestation is a first-person
statement about how a session conducted itself — its deviations, its bias direction, the counterclaim
an independent reviewer would make. A later session cannot make those statements on batch 06's
behalf. So `attestations/sessions_session_2026-09-10-research-batch-06-circulation-geometry.json`
attests **the reconstruction**, which is the 2026-09-13 session's own act, and explicitly does not
attest batch 06's conduct. Batch 06's `adversarial-review` posture is not assessed here and cannot be
recovered from the artefacts.

## One correction the later session made to batch 06's data

REF-00784, which batch 06 declared its Tier 1 anchor, was demoted to Tier 3 on 2026-09-12 by owner
ruling after its abstract was retrieved for the first time and found to state "Case series" with a
sample of convenience. It does not govern `specification_id 1`, so the determination is unaffected.
Recorded here because batch 06's own record would otherwise describe an anchor that no longer stands.
