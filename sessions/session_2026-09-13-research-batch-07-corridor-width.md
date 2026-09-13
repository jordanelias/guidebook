# Batch 07 — corridor width (TERM-002) × MOB

**Session id:** `session_2026-09-13-research-batch-07-corridor-width`
**Branch:** `claude/research-capability-status-fxoybg` · **PR** #136
**Cell:** `parameter_id 2` (TERM-002 `corridor width`) × identity lens `MOB`, slug
`accessible-circulation-geometry`
**Outcome:** `specification_id 2` — **`provisional`**, `tier_basis T3-only`,
`derivation_sha 62bfd45350c6…`, `value_min/max/unit` all NULL.

Every figure below was derived from `data/guidebook.db` after the migrations applied (rule 7).
Re-derive before relying on any of it.

## What the batch did

| | |
|---|---|
| searches logged | 2 (1 zero-yield, 30 results screened) |
| sources admitted | 2, with 2 `search_admissions` edges |
| candidates staged | 4 |
| concept observations | 3 |
| population matches | 2 |
| citation-mining passes | 2 |
| extractions on parameter 2 | 4 |
| parameters minted | 1 (promoted, not coined) |
| determinations | 1 |
| data migrations | 2 |

**The parameter was PROMOTED, not minted.** `TERM-002 corridor width` already existed, so step 1 ran
`add-parameter --term-id TERM-002` (provenance `base-vocabulary`) and the runbook's
`observe-term → add-term` path was deliberately skipped. Running it as written would have coined
"corridor clear width" beside TERM-002 — the same near-duplicate defect `ORDER-OF-WORK.md` caught
with `turning diameter` beside TERM-003.

## The Co-1 leg is a real zero, and the control is what proves it

0 hits with the co-production clause; **30** with the identical subject terms and the clause removed.
That is a fact about publication venue, not about query shape, which is the distinction R14 exists to
force. Co-1 on corridor width is not reachable through PubMed and has to be sought in DPO, housing and
design venues. Recorded as exec 47 with the finding in `findings_note`, and kept — R8 makes a
zero-yield search a completed unit of work.

## The substantive finding: nothing states a corridor width

**Not one retrieved source states an absolute corridor width.** All four extractions are `qualitative`
or `absent`:

- **REF-00784** (Koontz 2010) — minimum passageway width *is* its outcome measure, and its abstract
  reports no number. What it reports is that between 10% and 100% of users cannot manoeuvre in spaces
  meeting current Accessibility Guidelines.
- **REF-00971** (Dutta 2011) — no tested scooter completed all five configurations within the space
  existing standards allow. **Marked `contested = 1`**; see below.
- **REF-00976** (AIJ 2004) — states a required *enlargement* of more than 30 cm over surveyed Japanese
  housing stock. Deliberately **not** graded `numerical`: an increment is not a width, and
  `claimed_value` means the value claimed for the parameter.
- **REF-00981** (Dolbow & Figoni 2015) — `absent`, and the absence is the finding: an 82-item ADA
  compliance survey of ten facilities that names narrow passageways as a major obstacle and never
  reports a passageway dimension.

So the literature reachable from here measures the **inadequacy of dimensions** rather than the
dimensions. That is content for the guidebook, not only a gap in the corpus.

## What the adversarial pass changed

The antagonist ran read-only and independently, arming itself from the contract and the gate before
the batch ran. Two of its findings changed the filed rows:

1. **REF-00982's extraction was RETRACTED.** Its own abstract states the objective is to demonstrate a
   re-sampling method; doorway and clear-floor-space widths are the *illustration*. And `door width` is
   TERM-021, a separate live term, while `clear floor space` has no term at all. Filing it under
   TERM-002 because the abstract contains "clear … width" is the conflation TERM-002's own `scope_note`
   warns about for the Spanish alias `paso libre`. **The source stays admitted and slug-linked; only
   the parameter edge is withdrawn**, with the reasoning kept as candidate 81.
2. **REF-00971's extraction was marked `contested`.** Its harvested phrases are `turning diameter` and
   `turning 180° in a corridor`, and its sibling REF-00972 states a 1.5 m *turning circle* — so the
   pair's subject is arguably TERM-003. The row stays because one of the five configurations measured
   is explicitly a corridor; the contest is recorded in the row rather than argued away. REF-00972 was
   never extracted on this parameter for the same reason.

It also predicted the outcome before the engine ran — `provisional / T3-only` on an all-T3 governing
set — and warned that one extraction on the Co-1 survey or the T2 review would have flipped the cell
to `stated` on a source that states no width, because `gather_sources()` never reads `claim_type`.
Neither was extracted. That warning is the batch's most important unfixed finding and is recorded
below.

## Defects found by tripping them

**H05 — an admission count with no edges.** `db.py log-search` guarded invariant H05 with
`if ids and results_admitted and results_admitted != len(ids)`. Conditioning on `ids` meant a count
passed with **no** `--admitted-ref-id` at all was never checked. Tripped while logging this batch.
Measured against canonical: **8 of the 13** executions claiming admissions carry zero junction edges,
and one of them (exec 44) is batch 06, which the definition-of-done gate had passed COMPLIANT.
The junction is the only carrier — `admitted_ref_ids` is deliberately not written — so a count with no
edge claims an admission nothing can trace. **Closed**; the exact call that slipped through now
refuses, and the legitimate shapes were re-tested.

**exec 48's harm flag was down.** Raised through `amend-search --set-harm-finding`, which appends
rather than rewrites, with the three findings named: REF-00784's 10–100%, REF-00971's standards
failure, and staged candidate 79 (36% of occupants not evacuated when corridors are impeded).

## Owed, and stated rather than left to be discovered

- **Batch 06 was never closed.** No `sessions/` record, no attestation. `sessions/LATEST` and
  `LATEST-RESEARCH` named batch 05 until this session moved them to batch 07 — which means
  `citation_mining_session` and `author_fidelity`, both session-scoped, were auditing batch 05 the
  whole time, and moving the pointer past batch 06 means batch 06 never gets that audit at all.
- **The ICF and access-need lenses are not set on this cell.** Only `identity_code` is. The crossing is
  judgment's output under the 2026-08-27 ruling and the phrases are harvested and unadjudicated; zero
  links after judgment is a defect, and this cell currently has that shape.
- **The cell has no value, and nothing reads the columns that would hold one.**
  `specifications.value_min/max/unit` are written NULL by the engine and read by nothing. For this cell
  that is also *true* — no source states a width — but the two facts are independent and should not be
  allowed to excuse each other.
- **`gather_sources()` does not read `claim_type`.** An honestly-`absent` extraction makes its source a
  governing anchor. Harmless here because every governing source is T3-clinical; not harmless in
  general.
