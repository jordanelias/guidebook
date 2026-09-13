# Backfill plan — grading the 8 live extractions under migration 075

Derived 2026-09-13 **from the persisted payload bytes only**. Every quote below was located by
byte-search in `retrieval-log/`; the writer re-verifies each as a byte-substring before accepting it,
so nothing here rests on this file being right.

**Blocked until the writers land.** No `db.py` verb sets `figure_role` or writes an edge yet.

## The grading

| # | ref | role | comparator | edge | referent |
|---|---|---|---|---|---|
| 1 | REF-00973 | `condition` | — | **none** | — |
| 2 | REF-00974 | `finding` | — | none | — |
| 3 | REF-00980 | `condition` | — | `tested_at` | label, `standard`, **named** |
| 3b | REF-00980 **new row** | `finding` | — | `confirms` | same label |
| 3c | REF-00980 **new row**, new parameter *ramp run* | `condition` | `=` | `condition_on` → #3 | — |
| 4 | REF-00979 | `finding` | `between` | none | — |
| 4b | REF-00979 **new row**, *ramp run* | `condition` | `=` | `condition_on` → #4 | — |
| 5 | REF-00784 | `finding` | — | `insufficient` | label, `standard`, **named** |
| 6 | REF-00971 | `finding` | — | `insufficient` | label, `unnamed`, **unnamed** |
| 7 | REF-00976 | `finding` | — | none | — |
| 7b | REF-00976 **new row** | `claim` | `>` 30 cm | `delta_over` | label, `own_sample`, **named** |
| 8 | REF-00981 | `finding` | — | `audited_against` | label, `standard`, **named** |

## The quotes, verbatim from the payloads

- **#3 `tested_at`** → *"the range of ramp slopes allowed under the current ADA accessibility
  guidelines"* (`1e08f1f365d154a1.xml`). The tested slopes **are** the ADA range — which is why
  extraction 3's `1:8 to 1:20` is a rig setting, not a claim.
- **#3b `confirms`** → *"changes to the technical requirements for ramp slope and length cannot be
  recommended at this time"*. **This is the live case for the owner's 2026-09-13 upgrade ruling** — a
  T1 source confirming a code value as genuine best practice, which G1's traceability test alone
  would never have caught.
- **#3c run** → *"traversed a 30-foot ramp"*. 30 ft.
- **#4b run** → *"Each subject pushed up a wooden ramp (7.3m long)"*. 7.3 m.
- **#5 `insufficient`** → *"current Accessibility Guidelines for Buildings and Facilities
  specifications"*.
- **#6 `insufficient`** → *"existing standards"* — named by nobody. `to_kind='unnamed'`,
  `stated='unnamed'`. This is the live unstated-baseline case and becomes queryable.
- **#7b `delta_over`** → *"newly built residences in Japan"* (`d170cbf86507a07b.html`).
- **#8 `audited_against`** → *"The Americans with Disabilities Act (ADA) of 1990"*.

## Two things deliberately NOT written

**REF-00973 gets no ADA edge.** Its four tested slopes coincide with the ADA range, but its payload
contains no sentence naming ADA, a guideline or a standard — searched and confirmed empty. Writing
the edge would require `stated='inferred'`, and inferring a baseline to fill a gap is the shape the
whole `stated` column exists to prevent. The coincidence goes in `notes`, not in an edge.

**No derived row for REF-00976.** `delta_over` records "+30 cm over the surveyed stock", but the
stock's own width is not in the abstract, so the base figure does not exist as a row and
`derive-extraction` must refuse. That refusal is correct: a derived figure exists only when its base
does. The J-STAGE full text is the retrieval that would supply it.

## The K01 consequence, measured before it bites

`test_db_integrity`'s K01 hashes `n_extractions` **per parameter**. Rows 3b and 7b are new rows on
parameters 1 and 2, so both stored `derivation_sha` values stop verifying and K01 — blocking — goes
red. Rows 3c and 4b are on a NEW parameter (*ramp run*) and do not touch it. So the backfill either
ships with a compensating restamp migration recomputing both shas by K01's own payload formula, or
waits for the supersede path. K01's own remedy text says "re-run the engine and restamp", and the
engine refuses to re-determine — so restamp is the available route and the state does not change,
only the attestation.

## Vocabulary owed first

*ramp run* has no term. The ruled path is open: `observe-term` on REF-00980's "30-foot ramp" or
REF-00979's "7.3m long", then `add-term`, then `add-parameter`. *Landing length* has **no phrase in
any logged abstract** and cannot be minted honestly until a source using it is admitted — ADA 2010
§405 is the obvious candidate and is already staged as a lead.
