# Session 2026-08-23 — Research batch 03: forward citation mining

**Written after the fact, 2026-08-23, and that is itself a defect.** The batch's migration was
emitted, applied and merged before this record existed, and `sessions/LATEST-RESEARCH` still pointed
at batch 02 while batch-03 rows in the DB cited a session id with no file behind it. A read-only
adjudication caught it and graded it HIGH. Every prior batch carried a record and an attestation at
the time of the write; this one did not, and the reason is that the session was mid-way through
unrelated repair work and treated the batch as a step inside it rather than as a batch.

---

## 1. What this batch did

**R2 requires backward AND forward mining. Forward had never been run — not once, on any anchor.**
All seven `citation_mining` rows read `backward=1, forward=0` with `connections_produced` empty, and
three further sources had no mining row at all.

| | |
|---|---|
| `search_executions` written **by this batch** | **10** |
| Zero-yield searches kept (R8) | **3** |
| `search_candidates` staged | 16, of which **2 withdrawn by me on review** |
| `citation_mining` rows now carrying `forward=1` | **10 of 10** |
| Sources admitted | **0** |
| Forward citations that existed and had never been looked at | **219** |

**A figure I got wrong and am correcting here:** I described this batch as writing *28*
`search_executions`. That is the whole-table count including batches 01 and 02. **This batch wrote
10.**

## 2. Retrieval, and a zero that is not an absence

OpenAlex resolved all ten anchors, then exhausted its request budget mid-run. **Those zeros are not
logged as zero-yield searches.** Under R14 a zero is evidence of absence only if the query was
well-formed, and a rate limit is an infrastructure failure, not a finding. R10 says a publisher block
is not a terminal answer, so the mine was re-run through Semantic Scholar.

Where S2 returned 0 while OpenAlex reported a non-zero `cited_by_count` for the same DOI, the search
row says so explicitly: **an indexing fact about S2 coverage, not an evidence fact** (R5). Three
searches are genuine well-formed zeros — the anchor resolved and both indexes agree — and they are
kept, because a zero-yield search is a completed unit of work (R8).

## 3. The DoD gate says NON-COMPLIANT, and the waiver is here

`research_batch_dod.py --session session_2026-08-23-research-batch-03-forward-mining` fails four
rules. **The gate is right and the batch still stands. Reasoned waiver, per the gate's own footer:**

| Rule | Why it fails | Waiver |
|---|---|---|
| **R9a / R9b** | This batch admitted nothing, so the stash cross-check and the collision check have no subject and correctly report NOTHING IN SCOPE | **Structural, not a defect in the batch.** I hardened these rules the same morning so a bare PASS could not stand on an empty subject. That hardening was right for admitting batches and created a state a *mining* batch can never clear. **The gate has no posture for non-admitting work** — recorded as the fix, not waived away. |
| **R4** | Demands population linkage from searches that admitted nothing | Same shape: no empty posture. |
| **R1** | Co-1 pass not evidenced | **Avoidable, and my error.** A `CO1-NOT-APPLICABLE` channel exists in `findings_note` and this batch did not use it. Forward mining from mixed anchors has no Co-1 targeting step; it inherits the lens of what it mines. |

**This is the honest reading: a mining-only batch cannot currently be compliant.** Patching it with a
waiver every time would be ceremony. The fix belongs in the gate.

## 4. Two candidates I withdrew

- **#55** — already admitted as **REF-00965**. My screen deduped against `search_candidates` only,
  not against `evidence_sources` or `source_locators`. **That is the R9 pre-check I had fixed in the
  DoD gate that same morning, omitted at the staging step.** Kept as MISCELLANEOUS rather than
  deleted: a withdrawn candidate is a record of the error.
- **#60** — concert-hall violin acoustics. Off-slug; REHOME. My keyword screen matched "acoustic"
  plus a Co-1 pattern and let it through.

**Nothing was admitted.** Every staged row records in its own `why_not_admitted` that the keyword
screen is a **hypothesis** (R15) and that the population tags are regex hits, not graded claims — the
`MH` pattern in particular fires on "wellbeing"/"stress" inside autism papers.

## 5. What this did and did not move

`evidence_sources` 10 → 10. `specifications` 0 → 0. Five gaps OPEN at open and close. **What moved is
that R2's forward debt is discharged and 180 distinct citing works are now visible where none were.**
Ten of them touch the open gaps (DEM, MH, BRAIN) and twelve carry a Co-1 signal — none yet verified.

## 6. The pointer this batch cannot hold, and it is a third instance

`sessions/LATEST-RESEARCH` was advanced to this session and then **reverted to batch 02**, because
advancing it makes a BLOCKING gate vacuous. `test_db_integrity` L04, verbatim:

> *"pointer names 'session_2026-08-23-research-batch-03-forward-mining.md', which holds 0
> slug-linked Tier 1-2 source(s)… With 0 subjects that BLOCKING gate examines nothing and passes."*

The pointer carries two jobs that this batch pulls apart: *"the most recent session that did
research"* and *"the subject for the citation-mining gate"*. Batch 03 satisfies the first and cannot
satisfy the second, because the gate's subject is admitted sources and this batch admitted none.
**`LATEST` advances to this session; `LATEST-RESEARCH` stays on batch 02**, which still has real
subjects, so the blocking gate keeps examining something.

**This is the third gate today that assumes a research session admits sources** — after the DoD
contract (§3) and the R9a/R9b subject checks. That is no longer three coincidences. The apparatus
has one model of a research session, and mining does not fit it.

**Next:** resolve the staged candidates under R10/R15, and give the DoD gate — and this pointer — a
posture for non-admitting work before the next mining pass runs.
