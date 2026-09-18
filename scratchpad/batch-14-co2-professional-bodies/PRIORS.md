# Batch 14 — finishing the Co-2 pass: WFOT, CAOT, Occupational Therapy Australia

**Session:** `session_2026-09-18-research-batch-14-co2-professional-bodies`
**Parameter:** 3 (TERM-001, ramp gradient) · **Slug:** `accessible-circulation-geometry`
**Written BEFORE any query is run.** R8 / DR-2026-05-09.

## Why this batch exists, in one sentence from my own record

Batch 13's attestation, `independent_reviewer_counterclaim`:

> The honest position is that R1 remains partly unrun after a batch named for it, and the next batch
> should start with WFOT, CAOT and Occupational Therapy Australia before anything else.

This is that batch. It is not a new idea; it is a commitment being kept.

## The state, derived not remembered

```
select jurisdiction, count(*) from search_executions
where target_evidence_type='co2' group by jurisdiction
  ->  AU 1 · GB 1 · UK 1 · US 2      (5 total, 0 admissions)
select count(*) from evidence_sources where evidence_type='co2'   ->  0
```

**No INT search and no CA search has ever been run.** WFOT is the international federation; CAOT is a
national college. Both are squarely what `governance/tier-system.md` means by Co-2, and neither has
been looked at. The single AU search went to state equipment programmes, not to the professional body.

*Noted in passing and not fixed here:* the jurisdiction column carries both `GB` and `UK` for the
same place — batch 09 wrote `UK`, batch 13 wrote `GB`, and `evidence_sources` uses `GB`
(REF-00992). A vocabulary with two spellings for one jurisdiction will eventually scope a gate to
half its subject. Recorded as an observation, not actioned, because it is not this batch's question.

## The prior, stated so it can be wrong

**I expect all three to return well-formed zeroes on a stated gradient**, and I expect the batch to
end with Co-2 still unadmitted. Reasons, descending confidence:

1. **A federation publishes position statements, not dimensions.** WFOT's published output is
   occupational-justice and professional-scope material. A ramp gradient is a building-code fact and
   sits outside what an international federation asserts.
2. **CAOT will defer to the National Building Code of Canada** if it addresses gradient at all. If it
   does state a figure, the 2026-09-13 ruling puts value-restating material in the regulatory
   stratum, so it would be T4-T5 and would NOT anchor as Co-2 — the same call made on REF-00996 and
   REF-00997.
3. **Occupational Therapy Australia is the most likely of the three to state something**, because
   Australia has an unusually developed OT home-modification practice literature, and because batch
   13 already found two state programmes writing prescriber guidance. But for exactly that reason I
   expect OTA to point at AS 1428.1 rather than carry its own number.

**Falsifier, unchanged from batch 13:** a professional body stating a maximum gradient with its own
clinical warrant — a rationale, a cited study, or a consensus process — rather than a cross-reference
to a code. That would be the corpus's first Co-2 admission and would change the cell's tier basis.

**Confidence: medium-low on the specifics, high on the shape.** I have been wrong once already in
this pair of batches about what had been searched; I have not been wrong yet about what OT bodies
publish, and batch 09's RCOT zero and batch 13's delegation chain both point the same way.

## What would make this batch a failure rather than a zero

Not "no Co-2 admitted". That is the likely honest outcome. It fails if:

- a body is declared searched on a single query against its website, when its guidance lives in a
  members' area or a journal (that is batch 09's AOTA situation, and R10 says a block is not a
  terminal answer); or
- a zero is logged without R14's diagnosis — query-shape failure vs wrong index vs genuine absence; or
- something is admitted at Co-2 because this batch wants a Co-2 source. **The tier call must go
  against the batch's interest if the evidence says so**, as it did in batch 13.

## What this batch does NOT do

- It does not re-probe RCOT or AOTA. Batch 09 did both; batch 13 re-probed both and learned nothing
  new. A third pass would be duplication dressed as diligence.
- It does not recompute the determination unless an admission changes the governing or direction set.
