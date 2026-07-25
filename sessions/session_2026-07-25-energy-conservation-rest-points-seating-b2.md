# Session — energy-conservation-rest-points-seating, batch 2

**Date:** 2026-07-25
**Slug:** `energy-conservation-rest-points-seating` (STUB, `seating-and-rest`)
**Axis:** `AX-STA` Sustained-exertion demand; secondary `AX-PAI`, `AX-AMB`, `AX-BAL`
**Doctrine SHA:** `0f2f525`
**Predecessor:** batch 1 (merged as PR #71)
**DoD gate:** COMPLIANT, 15/15

---

## 1. Objective and result

Batch 1 left three things: six staged candidates, an untested single-research-group dependency
(**GAP-306**), and an interval figure with no primary basis (**GAP-304**). Batch 2 targeted the
first two.

**7 sources admitted** (REF-00953–00959). **GAP-306 closed.** GAP-304 sharpened and left open.
Three new gaps registered, one of them a P1 harm finding.

## 2. GAP-306 — independence tested, and the gap does not hold

Three of batch 1's four primary sources shared authors and institution (Jyväskylä), so the
resting-places finding could have been one group's result echoed.

**Method chosen deliberately.** A forward citation walk from a Finnish-cluster paper tends to
return the same cluster — it would have manufactured the appearance of corroboration. Instead the
independence question was attacked with a well-formed topical query designed to surface *other*
groups. (Three concepts returned 19 usable records; batch 1's seven- and eight-concept AND-chains
had returned zero. The query-shape lesson from batch 1 paid off directly.)

**Five groups, six countries, five distinct methods** — none Finnish, none sharing authors:

| Source | Country | Method | Why it counts as independent |
|---|---|---|---|
| REF-00955 | CA | GPS routes + GIS, n=25 | Measures *recorded* walking, not recalled barriers |
| REF-00956 | CZ (+LV) | Survey n=525, ordinal regression | Distributional: rural provision substantially worse |
| REF-00957 | FR | Spatial accessibility model | Benches are 1 of only **4** model variables |
| REF-00958 | HK | Qualitative n=38 | Non-Western setting; benches surface unprompted |
| REF-00959 | US | n=3,677, validated instrument | Benches **survived empirical item selection** |

The methods fail in different directions, so agreement across them is worth more than five
repetitions of one design. Recorded confidence **80–90%** — and scoped explicitly: that is
confidence the association is not a single-group artefact, **not** a claim about effect
magnitude, which none of these sources was designed to estimate.

## 3. GAP-304 — sharpened, not closed, and now more uncomfortable

Six further sources were read, including a **participatory national framework** where disabled
street users were consulted directly (REF-00954) and a **validated instrument at n=3,677**
(REF-00959). **Not one states a spacing figure.** REF-00954 says only "at regular intervals where
possible"; REF-00959 records bench *presence*.

So: bench **presence** is now independently and repeatedly associated with walking outcomes,
while the **interval** is unmeasured by anyone located so far. The 50 m figure is not merely
under-evidenced — the entire literature supporting rest provision is silent on spacing.

## 4. The seat-height conflict resolved — and the independence check run in both directions

Batch 1 could only report Co-1 (REF-00950: 380/480/580 mm) asserting against a T5 standard
(REF-00949: single 470–480 mm band). REF-00953 supplies the primary evidence, and it is
**independent** — Australian aged-care research that never cites the UK guidance:

- Audited 410–505 mm (facilities) and 423–510 mm (suppliers); **none** fits a 5th-percentile
  older Australian female (popliteal height 330 mm vs mean 379 mm).
- Names the mechanism the standard misses: *"The disparity between seat height required for STS
  and seat height required for comfort while seated."* One number cannot satisfy both.
- Recommends variety, not a midpoint: *"a range of chairs of different heights in each space."*

**This is the methodological point of the batch.** In batch 1, a Co-1 source agreeing with a
standard was *not* corroboration — it cited that standard. Here, a Co-1 source agreeing with
primary research *is* corroboration — they are independent and arrived by different routes. The
independence check has to run in both directions, or it is just scepticism aimed at conclusions
we happen to dislike.

**Armrests:** REF-00949 says they *"are helpful for some."* REF-00953 observed them *"used 100% of
the time regardless of the resident's level of mobility"*, with 90% of transfers needing more than
one attempt. REF-00954 converges independently. The standard is too permissive.

## 5. R7 — new harm finding (GAP-307, P1)

Single-height seating is an equity harm and the standard encodes it. REF-00953: *"shorter
residents are being disadvantaged compared with taller ones, suffering discomfort and possible
musculoskeletal damage while sitting and being put at risk of deep venous thrombosis (DVT) due to
the seating design."* Women are 69% of permanent aged care in Australia and likelier to be
shorter, so **the harm is gendered**. The UK 470–480 mm band sits inside the excluding range.

## 6. New parameter with no specification anywhere (GAP-308)

REF-00954 records disabled street users requiring seating *"positioned so that it is possible to
see from a distance i.e. to allow journey planning"* and *"clearly signposted … to know when to
anticipate potential for breaks."* Neither REF-00949 nor REF-00950 specifies visibility, sightline
or signage. A bench that cannot be seen in advance does not inform the decision of whether the
journey is attemptable — which is the decision this demand actually turns on.

## 7. What batch 2 did NOT achieve — stated plainly

**Zero new Co-1 sources.** The R1 pass ran first and came back empty **because of access, not
absence**. Transport for All returned HTTP 403 on all three routes tried (highlights PDF, full
PDF, HTML news page); Ulahannan returned 403 from ScienceDirect with no DOI available. Neither was
admitted on secondary description — a web-search summary calling an organisation disabled-led is
not the source speaking, and batch 1 set the standard of verifying that from the organisation's
own material. Registered as **GAP-309**. This matters disproportionately: **the slug still holds
only one Co-1 source.**

Also not done: non-EN remains deferred (no `term_aliases` yet — deferral, not absence); Gant 1997
and Access Association were not attempted this batch.

## 8. Errors made and corrected before commit

- **`NOT-APPLICABLE` in `doi_resolution_outcome` again** — the same vocabulary error I made and
  fixed in batch 1, repeated on the one new source without a DOI. Caught by diffing integrity
  against the pre-batch DB (25/35 vs 26/35). The lesson from batch 1 was recorded in prose but not
  mechanised, which is exactly the failure mode `.claude/settings.json` was built to address.
- **Closed a research gap without its protocol fields** — `research_protocol_audit` CHECK 1
  requires `confidence_interval`, `shift_conditions` and `named_dissenter`, not just a
  falsification condition. Fair rule: closing a gap should record what would reopen it.
- **Narrative confidence interval** — CHECK 4 wants the corpus convention (a numerical percentage
  range, or `NOT-RESEARCHED`). Converted to `80-90%` with the reasoning folded into
  `shift_conditions` rather than deleted.

All three fixed at source in the uncommitted migration and the DB rebuilt, so none enters history.

## 9. Gate results

| Check | Result |
|---|---|
| `research_batch_dod --session` | **COMPLIANT 15/15** (first run) |
| `research_batch_dod --all` | COMPLIANT |
| Migration reproducibility (7 invariants) | PASS |
| `test_db_integrity.py` | 26/35 — **equal to pre-batch baseline** |
| `research_protocol_audit` | 2138 — **equal to baseline, no net new debt** |
| `validate_bpc.py` / `validate_cross_refs.py` | 102/102 · 0 issues |

## 10. Batch 3 queue

1. **REF-00953 backward leads** — Christenson (380–457 mm variety), Holden & Fernie (armrest
   730 mm floor / 250 mm seat / 120 mm width), Kothiyal & Tettey (376 mm depth), the Australian
   Standard for fixed-height chairs. Likeliest route to a primary derivation of the dimensions.
2. **GAP-309** — retrieve the two blocked Co-1 sources by another route (Crossref for a DOI, then
   retry). The Co-1 base is the slug's thinnest point.
3. **Transport Scotland parent report** — the appendix omits the interval; the parent may not.
4. **`term_aliases`** to unblock non-EN.
