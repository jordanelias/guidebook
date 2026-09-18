# Batch 13 — Co-2 (OT professional-body CPGs) on ramp gradient

**Session:** `session_2026-09-18-research-batch-13-co2-occupational-therapy`
**Parameter:** 3 (TERM-001, ramp gradient), `accessibility_direction = lower_is_better`
**Written BEFORE any query is run.** R8 / DR-2026-05-09: a prior recorded after seeing results is a
rationalisation, not a prior.

## Why this batch is Co-2 and not something else

Derived from the live DB, not remembered — `select evidence_type, co1_source_type from evidence_sources`
over 14 rows returns T1, T2, T4, T5, T6 and Co-1, and **no Co-2 at all**. R1 of the research contract
makes the Co-1 / T2 / Co-2 pass first with no exceptions, and `governance/tier-system.md` puts Co-2
(OT professional-body CPGs) in the anchoring stratum. Twelve batches have run without one. That is
the gap, and it is a gap in the *searching*, unlike the four Co-1 zeroes batch 12 recorded, which
were gaps in the evidence base.

## The prior, stated so it can be wrong

**I expect the Co-2 pass to return few or no stated gradient figures, and I expect it to be a
well-formed zero rather than a thin yield.** Three reasons, in descending confidence:

1. **OT professional guidance is about the assessment, not the dimension.** The body of work an OT
   professional body publishes on housing adaptation is predominantly process: who assesses, when,
   against what functional criteria, and how quickly. RCOT's *Adaptations without delay* is the
   archetype — a framework about delay and referral, not a table of slopes.
2. **Where an OT CPG does state a gradient, I expect it to RESTATE A NATIONAL CODE.** If that is
   what I find, the 2026-09-13 ruling puts value-restating material in the regulatory stratum, so it
   would be tiered T4-T5 and would **not** anchor as Co-2 — the same call batch 12 made on
   REF-00996. A Co-2 admission requires the professional body to be reasoning from its own
   discipline's evidence, not quoting the building regulator.
3. **The four Co-1 zeroes point the same way.** Disabled people's organisations published on whether
   access exists; regulators published the number. OT bodies sit closer to the regulator than to the
   DPO on dimensional questions, but their published output sits closer to the DPO.

**Falsifier:** an OT professional body stating a maximum gradient *with its own warrant* — a
clinical rationale, a cited study, or a consensus process — rather than a cross-reference to a code.
If that exists, my prior is wrong and the cell gains its first anchoring-tier value-supplying source.

**Confidence: medium.** I have not searched this literature in this project before, and batch 11's
IPC result (a sports federation stating 1:20 with a best-practice rationale) is a live precedent for
a non-regulator body stating a figure on its own authority.

## What I will NOT do

- Not down-tier non-English OT guidance for non-indexation (R5).
- Not let a zero-yield pass go unlogged or back-filled (R8). Four well-formed zeroes are batch 12's
  actual finding; a fifth would be a result, not a failure.
- Not recompute the determination unless an admission actually changes the governing or direction
  set. Spec 5 is live and `provisional`; it stays until evidence moves it.

## Targets, in order

| # | Body | Jurisdiction | Why |
|---|---|---|---|
| 1 | RCOT (Royal College of Occupational Therapists) | GB | Largest published housing-adaptation corpus |
| 2 | AOTA (American OT Association) | US | Practice guidelines incl. home modification |
| 3 | CAOT | CA | Home-modification position statements |
| 4 | OT Australia / WFOT | AU / INT | Consensus statements |

Query shapes will be logged verbatim with `db.py log-search --prior-expectation` before screening,
per R8, and R14 applies to every zero: query-shape failure vs wrong index vs genuine absence.
