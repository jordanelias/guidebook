# Batch 19 — PRE-REGISTERED PRIORS

Written BEFORE any screen was run, any retrieval fired, or any result seen.
R8 / DR-2026-05-09: a prior recorded after seeing results is a rationalisation.

Assignment: batch 18 §9 items 1–4, taken in that order.

---

## P1 — REF-01005 backward mining yield

**Instrument, chosen before the run:** `slope-strict` v1 is the PRIMARY screen.
`slope-strict-plus-motion` v1 is secondary. **`slope-loose` is pre-emptively
disqualified as a relevance measure on this anchor** and the reason is stated now,
not after: REF-01005 is titled *Accessible Buildings for People with Walking and
Reaching Limitations*, so its bibliography is an ACCESSIBILITY bibliography, and
`slope-loose` carries the bare stem `accessib`. On this anchor that screen measures
"cites accessibility papers", which is trivially true and tells us nothing about
slope. It will be reported for comparability with pre-2026-09-18 numbers and for
no other purpose.

**Predictions:**

- **P1a — bibliography size ≥ 60 references.** A 170-page federal research report,
  one of a six-report series, commissioned to revise ANSI A117. Confidence: 0.75.
- **P1b — `slope-strict` yield is between 3 and 12 references**, i.e. a small
  fraction of a large list. The volume spans doors, reach ranges, corridors and
  controls; ramps are one chapter. Confidence: 0.6. **Falsified if the yield is 0
  or ≥ 20.**
- **P1c — `slope-loose` yield is at least 3× the `slope-strict` yield**, for the
  structural reason given above rather than because the references are relevant.
  Confidence: 0.7. This is a prediction about the INSTRUMENT, not the literature.
- **P1d — the bibliography contains BOTH Templer and Walter as discrete entries.**
  Table 13 footnote c names them. Confidence: 0.8. If absent, the footnote cites
  work not in the reference list, which is itself a finding.

**The OCR caveat, stated in advance:** the PDF text layer is known OCR-damaged.
Any yield is therefore a FLOOR, not a count — a reference whose title is mangled
below the screen's terms is a false negative. A zero on `slope-strict` here would
be weak evidence of absence, and I commit now to reporting it that way.

## P2 — Walter 1971 via Jisc Library Hub Discover

Candidate 109. Target: *Four architectural movement studies for the wheelchair and
ambulant disabled. Part 3 — Ramp gradients* (1971).

- **P2a — Jisc returns a CATALOGUE RECORD: probability 0.65.** Jisc Library Hub
  Discover aggregates UK research-library catalogues and this is a UK institutional
  report, which is exactly its stratum.
- **P2b — Jisc returns FULL TEXT: probability 0.10.** It is a discovery service over
  catalogues, not a full-text repository. **The realistic success here is locator
  verification plus named holding libraries, and I am pre-committing to counting
  that as a success rather than moving the goalposts to full text afterwards.**
- **P2c — if a record is found, its author is NOT the name batch 17 first staged.**
  Candidate 109's note already records that the staged description was wrong on the
  author and was corrected on resolution. Confidence: 0.7 that the corrected
  attribution holds up against an authoritative catalogue.

## P3 — Templer 1977 via ERIC, NTIS, TRID

Candidate 115. **Which Templer item is load-bearing is UNRESOLVED and will not be
guessed** (batch 18 §9 item 3, carried forward verbatim).

- **P3a — TRID holds a Templer 1977 record: probability 0.5.** Templer published on
  stairs and ramps in the transportation-research stratum.
- **P3b — ERIC holds it: probability 0.2.** ERIC is an education index; it held
  REF-01005 because HUD deposited it there, which was a deposit fact, not coverage.
- **P3c — NTIS holds it: probability 0.3**, conditional on it having been a federal
  technical report.
- **P3d — at least one of the three returns SOMETHING: probability 0.7.**
- **P3e — MORE THAN ONE distinct Templer 1977 item exists and disambiguation is
  required: probability 0.4.** If so, the batch records the ambiguity and does not
  resolve it by picking the likeliest.

## P4 — Does this batch move the determination? NO.

**Predicted: parameter 3 × MOB stays UNDETERMINED, determination gate 1 stays OPEN,
`specifications` gains no live row. Probability 0.95.**

The reasoning, recorded so the prediction is falsifiable rather than vague: the
blocker is C10 over REF-01002's UNVERIFIED status, and nothing in this assignment
touches REF-01002. Further, Walter 1971 and Templer 1977 are both pre-1990, so the
owner ruling of 2026-09-18 places them as HISTORICAL GROUNDING at T3 — they cannot
anchor a present-day building parameter however strong their methods. **Retrieving
both in full would still leave the cell undetermined.** That is not a failure of
this batch; it is the batch's expected outcome, and banking a null here as
disappointment would misread it.

**Falsified if** a live determination is written this batch. If that happens, I
have either found a current anchor I did not predict, or I have forced a cell the
gates should have refused — and the second is the likelier reading, to be checked
before celebrating.

## P5 — GAP-033 (term adjudication), if capacity remains

`term_adjudications` is empty while `observed_terms` is not. Batch 18 named this
owed and did not attempt it. **Prediction: attempting it will surface a WRITER or
VOCABULARY defect rather than running cleanly, probability 0.6** — every other
never-run verb in this repository has (`reattribute-candidate`, `--verbatim-exempt`,
`add-source` report fields). Stated in advance so a discovered defect counts as a
prediction rather than as an incident.
