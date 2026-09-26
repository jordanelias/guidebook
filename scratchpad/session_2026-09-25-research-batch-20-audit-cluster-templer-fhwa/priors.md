# Batch 20 — PRE-REGISTERED PRIORS

Written BEFORE any database query, any search, any retrieval, or any render in this
batch. R8 / DR-2026-05-09: a prior recorded after seeing results is a rationalisation.

**What I already know, stated so it is not mistaken for prediction.** The runbook I was
handed (2026-09-25, drafted by a read-only investigation against origin/main @ cf35d441)
already asserts: that Templer FHWA-RD-79-3 carries a "Table 20, Ramp Gradient
Recommendations" over 1:8/1:10/1:12/1:16; that NBS IR 78-1554 uses "ramp" only
incidentally; and that candidates 123/124 are open-access audits reporting harm. Batch 19
§0 R1 independently records the Table 20 fact. Priors below that restate those claims
are not predictions and are marked **[KNOWN]**; the confidence on them is a confidence
that the runbook is right, not a forecast of the world.

---

## P0 — The pointer repair exposes nothing hidden in batch 19

`sessions/LATEST-RESEARCH` names batch 18. Re-pointing it to batch 19 re-scopes four
gates. **Prediction: `research_batch_dod --session` against batch 19 is COMPLIANT and
every rule examines > 0 subjects. p = 0.75.** Batch 19 §11/§14 record 19/19, but its
rows were amended after that run by code-review repairs, and the gates themselves have
moved since (PR #158). **Falsified if** any rule is red or any PASS examined 0. If red,
I stop and report (runbook step 2) — I do not proceed on top of it.

## P1 — The accessibility-audit cluster (candidates 123 Garg, 124 Pinto)

- **P1a — each reports a ramp-gradient COMPLIANCE figure (a count or proportion of
  audited facilities meeting a code gradient), not a gradient derived from users.**
  Garg p = 0.7; Pinto p = 0.55 (a national primary-care audit may report "ramp
  present/adequate" as a binary item without a gradient at all).
- **P1b — neither derives or tests a gradient THRESHOLD from user outcomes.** p = 0.9.
  An audit applies a yardstick; it does not measure what the yardstick should be.
- **P1c — the yardstick each uses is its national code** (India: Harmonised Guidelines /
  RPwD rules, 1:12; Brazil: ABNT NBR 9050, 8.33 % = 1:12). p = 0.65 for each.
- **P1d — neither carries a Co-1 warrant** (disabled people as co-producers evidenced in
  the bytes). p = 0.8. If one does, it is tiered Co-1 and the R1 leg is satisfied by
  the source, not only by the query.
- **P1e — tier: neither lands at T1.** A cross-sectional compliance audit is not a
  controlled study of the parameter. p = 0.8. I will assign from
  `governance/tier-system.md` against the retrieved text, not from the title screen's
  `tier_guess`, and I commit now to recording it if the tier-system text forces a tier
  I did not predict.
- **P1f — population-of-study grading (R13): both are PROXY or PARTIAL for MOB**, because
  the unit of study is the building, not a population of wheelchair users. p = 0.85.

## P2 — Templer et al., FHWA-RD-79-3 Vol. 3 (candidate 125)

- **P2a [KNOWN] — Table 20 exists and covers 1:8, 1:10, 1:12, 1:16.** p = 0.95.
- **P2b — Table 20 does NOT endorse 1:12 as acceptable without qualification for
  unassisted manual wheelchair users in ascent.** p = 0.6. The period literature
  (REF-01005's 1:12 "measured and found wanting") points that way; I have not seen
  Templer's table.
- **P2c — the rating instrument is a subjective rating scale by the subjects, not a
  physiological measure.** p = 0.55.
- **P2d — the Walter description is second-hand and gives Walter's gradient
  recommendation as a ratio.** p = 0.6. I make no prediction of the value.
- **P2e — the IA scan has a usable text layer (OCR) but Table 20 is legible only on the
  rendered page, not in the djvu text.** p = 0.5. Either way, the page is rendered and
  looked at before any extraction is written (batch 19 R2 lesson).
- **P2f — the report's sample includes older people or ambulant disabled people as
  well as wheelchair users**, i.e. it is not a young-trained-user sample of the Elmer
  kind. p = 0.75.

## P3 — NBS IR 78-1554 (candidate 117)

- **P3a [KNOWN] — no rampway recommendation.** p = 0.9. Falsified by any passage
  recommending a ramp gradient or ramp design value.
- **P3b — the text layer is readable by pymupdf/pypdf** (NIST legacy scans are usually
  OCR'd). p = 0.7. If not, pages are rendered and read.

## P4 — Footnote c on REF-01005 Table 13 (page index 56)

- **P4a — the rendered page shows the footnote marker `c` on the 1:8 and 1:10 rows only.**
  p = 0.8. Batch 19 §3 held this as a reading; §0 R5 later says it was "independently
  confirmed on the rendered page", which conflicts with the runbook's statement that the
  page was never rendered. **Checking which of those is true is part of this step.**
- **P4b — the footnote text names "Walters, 1971" (with the s) and Templer.** p = 0.8.

## P5 — GAP-033, term adjudication (never run)

- **P5a — running the verb surfaces a writer or vocabulary defect before it runs
  cleanly.** p = 0.5 (batch 19 P5 put this at 0.6 and never tested it; I lower it
  because the verbs have been exercised by tests since).
- **P5b — the modal outcome across the backlog is NAMES-EXISTING or DEFERRED, not
  NOT-OURS.** p = 0.6. Observed terms were harvested from on-topic sources, so most
  should name something in the existing vocabularies or be genuinely undecidable
  without owner doctrine.
- **P5c — at least one observation warrants NAMES-NEW.** p = 0.4.

## P6 — The determination does not move

**Parameter 3 × MOB stays UNDETERMINED; determination gate 1 stays unresolved;
`specifications` gains no live row. p = 0.97.** The blocker is REF-01002, which the owner
ruling of 2026-09-25 retires from active work; everything admitted this batch is either
pre-1990 historical grounding (T3 per the 2026-09-18 ruling) or a compliance audit that
tests no threshold. **Falsified if** a live determination is written — which would mean
I forced a cell, and is to be checked as a defect before anything else.

## P7 — The Co-1 / T2 leg (R1), run first

- **P7a — a Co-1-targeted query for participatory / DPO-led accessibility audits that
  record ramp gradients returns at least one on-topic source not already in the corpus.**
  p = 0.4. REF-01006 (batch 19) is one such; the question is whether a second is
  reachable.
- **P7b — a T2-targeted query (systematic/scoping review of built-environment
  accessibility audits) returns at least one review that tabulates ramp-gradient
  compliance across studies.** p = 0.35.
- Per-query priors are logged verbatim with each query via `--prior-expectation`,
  before it fires.

## P8 — The exhausted three (REF-01002, candidates 109, 110)

**No retrieval is attempted** (owner ruling 2026-09-25: *"if we can't access something from
anywhere then we have to give up on it for now."*). Prediction that I will find a route
not already recorded as failed: p = 0.05 — and I will not go looking for one; a route is
tried only if one presents itself without a search.
