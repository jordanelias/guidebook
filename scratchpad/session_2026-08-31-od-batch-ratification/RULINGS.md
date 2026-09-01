# Owner rulings, 2026-08-31 — the OD batch

Captured at the moment of contact, before any propagation (CLAUDE.md rule 0: record the
supersession; rule 6: the scratchpad is the review surface and is committed, not held in context).

Context: PR #123 merged; `scripts/migrate_db.py` permitted. The ratified operative instrument
`DR-2026-08-19` §3 step 4a names this batch **"THE NEXT ACT, and it is the owner's, not a
session's"**, and states *"Nothing in step 5 can be authored until OD-A, OD-B and OD-C are
answered."* All seven put to the owner and answered in one sitting.

| # | Question | RULING |
|---|---|---|
| OD-A | Are the 372 `item_population_links` substrate or scaffolding? | **Substrate, PROVISIONALLY** — with a standing requirement that any edge a determination RELIES ON is re-derived and given a `rationale_ref` in that determination's own migration. |
| OD-B | Do deaf and hard-of-hearing people belong on `room-acoustic-performance`? | **YES — add DEAF and COM.** |
| OD-C | A-18's applicability set | **DEAF, AUT, NDV, DEM** — the reasoning doc's four minus `general`. |
| OD-D | REF-00965 / REF-00968, Co-1 → T3? | **NOT re-graded** (needs full texts this environment cannot reach). **RULE: a Co-1 tier with `co1_provenance` NULL is `unwarranted-pending`** — mechanical, a check can enforce it. |
| OD-E | REF-00967, T1 → T3? | **RE-GRADE to T3.** n=27 single-centre EEG carrying no RT60/NRC/STC/NC value. |
| OD-F | The adversarial-subject waiver | **RATIFY ONCE, NARROWLY**, as an owner-commissioned review, and record it. |
| OD-G | DR §12.1 Step 10's `jurisdictional_values` clause | **STRIKE IT**, and record the 2026-08-12 REFERENCE-ONLY ruling *in the DB* as a row-level note. |

## What each ruling costs, mechanically

- **OD-A** is not free. "Provisionally" creates a standing obligation on every future determination
  migration. It needs an enforcing check, or it decays into "substrate, unconditionally" by
  inattention — the §1 ratchet in reverse.
- **OD-B** adds `DEAF` and `COM` links to A-18 and A-03/A-06/A-07, each carrying a `rationale_ref`
  per OD-A. That is the FIRST use of the OD-A obligation and its proof of shape.
- **OD-C** fixes A-18's population set at four and unblocks its 12 staged standards leads.
- **OD-D** is the only ruling that adds VOCABULARY: `unwarranted-pending` must exist somewhere a
  check can read. It is a tier-warrant state, not a tier.
- **OD-E** is a single-row UPDATE plus its compensating record.
- **OD-F** is a record-only act.
- **OD-G** edits a ratified DR's runbook AND writes a note into the DB.

## Interaction with the parked rename (065)

**OD-A rules on `item_population_links`, which migration 065 folds into
`base_item_taxonomy_links` together with `item_axis_links`.** 065 is parked and inert, so there is
no conflict today — but the fold must carry `rationale_ref` forward, and 065 currently DROPS it
("0 of 372 populated"). That drop was justified by the column being empty; OD-A makes it the
column where the debt gets paid. **The 065 generator must be corrected before it lands.** Recorded
here so it is not rediscovered later.
