# Batch 15 priors — T2 synthesis, and the search for a stated value at an anchoring tier

**Session:** `session_2026-09-18-research-batch-15-t2-synthesis-threshold`
**Parameter:** 3 (TERM-001, ramp gradient) · **Slug:** `accessible-circulation-geometry`
**Committed BEFORE the first query is run.** R8: a prior recorded after seeing results is a
rationalisation, not a prior (DR-2026-05-09).

---

## 1. Why this batch, and a correction to the brief that proposed it

`workplan/2026-09-18-pipeline-content-review-and-walkability.md` §4 recommended T2 as "the untried
stratum" and — correctly — named the command to check before framing on it. **Run before writing
these priors, the check falsified the word "untried":**

```
select count(*) from search_executions where target_evidence_type='sr_meta'   ->  3
select count(*) from search_executions where target_tier=2                    ->  16
```

The vocabulary term is `sr_meta`, not `t2`, and T2 is **lightly worked, not untried**. Correcting my
own brief rather than inheriting its phrasing, because that is the exact three-step failure batch 13
recorded: a true scoped claim, a lossy restatement, and a reader who trusted the restatement.

**What survives the correction, and it is the whole warrant for this batch.** Exactly **one** T2
academic-database query has ever run against parameter 3 — exec 30:

> `(wheelchair propulsion) AND (ramp OR slope OR incline) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])`

One hit, admitted as REF-00984, which states no gradient. That query is a narrow PubMed AND-chain
gated on publication type — **the query shape R14 names first** when distinguishing a query-shape
failure from genuine absence. A single such query is not a worked stratum.

## 2. The question this batch is trying to answer

Specification 7 states its own falsification condition: *"Overturned if a source states a value for
this parameter at an anchoring tier."* The cell is `provisional` and `rests_on_proxy_inference = 1`
because all eight governing claims are T4–T6 regulatory, and the anchoring-tier evidence
(T1/Co-1/T2) supplies only **direction**, never a value.

**So the batch has one target: an anchoring-tier source that STATES a ramp gradient value or
threshold**, as opposed to measuring an effect across a range. That single admission is what lifts
parameter 3 off proxy inference. Everything else this batch finds is secondary.

## 3. Per-query priors — written before running, each independently falsifiable

**Q1 — PubMed, deliberately WITHOUT the publication-type gate.**
*Prior:* exec 30's single hit is an artefact of the `[Publication Type]` filter, not of the
literature. Removing the gate and broadening the concept terms will return **more than one** review-
shaped record. I expect **3–15 hits**, and I expect **none of them to state a gradient ceiling** —
the propulsion literature measures effects across ranges. FALSIFIED IF: a T2 record states a maximum
or recommended gradient.

**Q2 — PubMed, the threshold framing rather than the propulsion framing.**
*Prior:* searching for threshold/maximum/limit language rather than propulsion mechanics reaches a
different literature — rehabilitation engineering and accessibility standards research. I expect
**low yield (0–5)** and I expect any hit to be a *standards-development* paper that cites a code
value rather than deriving one, which would be T2 restating T6 and **not** an anchoring-tier stated
value. FALSIFIED IF: a study derives a threshold from its own data.

**Q3 — Consensus, semantic rather than boolean.**
*Prior:* a semantic engine will surface the dose-response literature already held (REF-00983/985/986)
and I expect **substantial overlap with the corpus** — which is a saturation signal, not a failure.
I expect **0 new admissions** and I will record overlap explicitly. FALSIFIED IF: it surfaces a
synthesis the PubMed queries structurally could not reach.

**Q4 — Scholar Gateway, semantic, cross-disciplinary.**
*Prior:* ramp-gradient thresholds may be studied outside rehabilitation medicine — in ergonomics,
transport, universal-design research — where PubMed does not index. I expect **the highest
probability of a genuinely new source of any query in this batch**, and also the highest risk of T3
grey. FALSIFIED IF: it returns only what PubMed already gave.

**Q5 — R2 forward/backward mining on REF-00984, the one T2 anchor held.**
*Prior:* REF-00984 (wheelchair skills tests systematic review, 2003) is old, and I expect its forward
citations to include **more recent syntheses** of wheelchair skills and environmental negotiation. I
expect **1–3 candidates worth staging** and **0–1 admissions**. FALSIFIED IF: the forward set is
empty, which would mean the anchor is a dead end rather than a seam.

## 4. Standing expectations for the batch as a whole

- **Most likely outcome, stated so it cannot be claimed as a success afterwards: ZERO admissions
  that state a value.** The regulatory stratum holds the values because *that is what codes do*;
  the research stratum measures effects. If that is what this batch finds, parameter 3 stays a proxy
  determination and **the null is the finding**, recorded as one.
- I expect to **stage more candidates than I admit**, and R15 says each staged description is a
  hypothesis to be re-described from the source on resolution, never left to harden.
- **R7:** failure, harm and inadequacy evidence is first-class. A synthesis finding that code-
  compliant gradients are inadequate is a result, not a by-product.
- **R11:** `observe-term` every concept phrase a source uses, in its own words, unjudged.
- **R13:** grade population-of-study against population-served on every admission — and the review
  found four ungraded sources, so this batch does not add a fifth.
- **R9/R10:** pre-check every DOI; re-retrieve every locator. No admission on a search snippet.
  Batch 13's Foundations falsification is the standing warning.
