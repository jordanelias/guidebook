# Per-query priors — written BEFORE each query fires (R8)

Batch-level priors are in `priors.md` (committed be427f35 before any query). These are the
per-query expectations for the Co-1 / T2 leg, which R1 requires to run before any other
tier's work in this batch. Each is committed before the query it describes is sent, and is
copied verbatim into `--prior-expectation` when the execution is logged.

**Why these two and not a repeat of batch 19's five.** Batch 19 (exec 91) searched Crossref
titles/abstracts for lived-experience ramp work, Europe PMC for wheelchair AND ramp AND
participatory terms, ERIC, and the exact phrase "Participatory accessibility audits". Its
admission (REF-01006) is a participatory audit that reports ramp gradient only inside a
table. The lesson batch 19 recorded is that **an audit's ramp data lives in the body, not the
title** (the slope-strict false negative). So the instrument here is Europe PMC's
**full-text** index, which searches the body of open-access articles, and the target is the
document type — the audit — rather than the topic word "ramp" in a title.

| # | Target | Engine | Query (verbatim) | Prior, before running |
|---|---|---|---|---|
| Q1 | Co-1: accessibility audits of real buildings that are disability-led or participatory AND record ramp gradient/slope in the body | Europe PMC REST `search`, resultType=lite, pageSize=100, full-text index | `("accessibility audit" OR "access audit") AND ramp AND (gradient OR slope) AND (participatory OR "disabled people's organisation" OR "disabled persons organisation" OR "organisation of persons with disabilities" OR "co-researchers" OR "peer researchers")` | hitCount between 10 and 120, p≈0.6 (full-text AND of five concepts is narrow but "participatory" is common). At least one on-topic result not already in the corpus that is BOTH co-produced with disabled people AND reports a measured ramp gradient: p≈0.35. REF-01006 itself should appear (it is PMC-deposited and matches every term) — p≈0.8; **if it does not, the query shape is suspect, not the literature (R14)**. Most hits will be health-facility audits in LMICs, same cluster as candidates 123/124, p≈0.6. |
| Q2 | T2: a systematic or scoping review that pools accessibility-audit findings on ramps across studies | Europe PMC REST `search`, resultType=lite, pageSize=100 | `("systematic review" OR "scoping review") AND ("accessibility audit" OR "physical accessibility" OR "architectural barriers") AND ramp AND (gradient OR slope OR incline)` | hitCount between 20 and 300, p≈0.6. At least one review whose own synthesis reports ramp-gradient compliance or a ramp-gradient outcome across included studies: p≈0.35. A review that is systematic (appraised, T2 sr_meta) rather than scoping (T3 per tier-system §2/§9): p≈0.4 conditional on one being found. Candidate 114 (a systematic review of manual wheelchair biomechanics over environmental barriers, already staged) may recur and must not be double-staged (R9). |

**Screening discipline.** Titles screened for all returned records on the first page; abstracts
fetched only for records a title does not rule out. Every staged candidate is R9-prechecked
against `evidence_sources.doi` and `search_candidates.locator` before staging. A result count is
read from the persisted payload's `hitCount`, never typed from the screen.

---

## Added after Q1 and Q2 returned, BEFORE Q1b fires

**Honest provenance:** Q1b was not in the original plan. Q1 returned hitCount 2 (predicted
10-120), one of them REF-01006 — so the query shape is sound (the known positive came back)
and the narrowness is real, but the exact phrase "accessibility audit"/"access audit" is the
likeliest single constraint doing the narrowing. Q1b relaxes that one term and nothing else,
so the difference between Q1 and Q1b isolates it (R14: query shape vs genuine absence).

| # | Target | Engine | Query (verbatim) | Prior, before running |
|---|---|---|---|---|
| Q1b | Co-1: same target as Q1, without the audit phrase | Europe PMC REST `search`, resultType=lite, pageSize=100 | `audit AND ramp AND (gradient OR slope) AND ("persons with disabilities" OR "people with disabilities" OR "disabled people") AND (participatory OR "user-led" OR "co-production" OR "co-researchers" OR "peer researchers" OR "disabled people's organisation" OR "organisation of persons with disabilities")` | hitCount 10-150, p≈0.6. At least one NEW co-produced audit that records a ramp gradient: p≈0.25 (lower than Q1's prior, because Q1 already found the one I expected to exist). If Q1b returns only REF-01006 plus off-topic hits, the Co-1 audit stratum on ramp gradient is genuinely thin in Europe PMC's OA full text — an INDEX-bounded absence, not a literature-wide one. |
