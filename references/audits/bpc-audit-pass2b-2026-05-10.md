# BPC Audit Pass 2B — Citation Verification Results
**Date:** 2026-05-10
**Session:** bpc-audit-2026-05-10 (continuation)
**Protocol:** research-log-manager CHECK/LOG per standing rule #4

---

## Summary

5 citation verification items completed. 1 fully verified, 1 verified with citation-precision note, 2 partially verified, 1 fabrication pattern confirmed.

| # | Claim | Verdict | GAP action |
|---|---|---|---|
| 2B.1 | Steinfeld 2010, n=500 | VERIFIED (citation-precision note) | GAP-266 updated |
| 2B.2 | van der Schaaf 2013, n=23,868/199 wards | VERIFIED | None needed |
| 2B.3 | Faerden 2022, d=2.0 patient support | PARTIALLY VERIFIED | GAP-279 filed |
| 2B.4 | Weltens 2023, OR 5.36 | AUTHOR VERIFIED, STAT NOT CONFIRMED | GAP-280 filed |
| 2B.5 | Avandell NJ 60% revenue premium | FABRICATION PATTERN | GAP-278 updated |

---

## 2B.1 — Steinfeld et al. 2010, n=500

**Claim in mob_pg.md:** "Steinfeld et al. 2010, n=500" as Tier 1 anchor for wheelchair turning space.

**Finding:** Reference exists. Two 2010 publications from the same IDeA Center research program:
- Steinfeld et al. 2010a: "Anthropometry and Standards for Wheeled Mobility: An International Comparison." *Assistive Technology* 22(1), 51–67. (Journal article, international comparison.)
- Steinfeld et al. 2010b: "Final Report: Anthropometry of Wheeled Mobility Project." IDeA Center, for U.S. Access Board. (Final report.)

**Sample size:** Actual enrolled = 495 (not 500). 339 completed turning maneuver independently. "500" is the rounded figure used in secondary citations (ICC/ANSI code proposals, RESNA 2018 conference papers). Defensible approximation.

**Turning data:** The 2010b-derived Design Resource #21 reports **360° turn** data (95th percentile: 2108mm manual+power, 2489mm scooters). The **2400mm 180° turn** figure cited in the BPC traces to the earlier Steinfeld 2006 RESNA paper (IDEA + BS8300 entire-sample, enclosed bay). The BPC should cite both studies or clarify which yields which figure.

**Verdict:** VERIFIED with citation-precision note. The Tier 1 anchor for the research program holds. The specific 2400mm 180° figure needs correct attribution to the 2006 paper.

---

## 2B.2 — van der Schaaf 2013, n=23,868 across 199 wards

**Claim in MH BPC:** van der Schaaf 2013 as Tier 1 anchor for private-space → reduced seclusion.

**Finding:** van der Schaaf, P.S., Dusseldorp, E., Keuning, F.M., Janssen, W.A., & Noorthoorn, E.O. (2013). "Impact of the physical environment of psychiatric wards on the use of seclusion." *British Journal of Psychiatry*, 202(2), 142–149. PMID 23307922.

**Sample sizes:** Exact match. n=199 wards, n=23,868 admissions, n=14,834 patients, 12-month period, 77 hospitals in the Netherlands. Multilevel regression analysis.

**Findings:** Private spaces and comfort reduced seclusion risk. Overcrowding, limited outdoor space, and special safety features increased seclusion risk. Study uses seclusion as proxy for aggression.

**Verdict:** VERIFIED. Citation is real, sample sizes exact-match, methodology (multilevel regression) is appropriate for the claims made.

---

## 2B.3 — Faerden 2022, Cohen's d = 2.0 patient support

**Claim in MH BPC:** "Faerden 2022, Cohen's d = 2.0 patient support" described as Tier 1 patient-control RCT.

**Finding:** Faerden, A. et al. (2022/2023). "Environmental Transformations Enhancing Dignity in an Acute Psychiatric Ward: Outcome of a User-Driven Service Design Project." *HERD* 16(2):55–72. DOI: 10.1177/19375867221136558. PMID 36567605. CC-BY 4.0.

**Study design MISCHARACTERIZED:**
- BPC says: "patient-control RCT"
- Actual: pre-post quasi-experimental design with control group
- NOT randomized
- Effect evaluated by **nursing staff questionnaire**, not patient-reported outcomes
- Measured staff perception of whether environment "supports the needs of patients in their situation"

**Effect size:** Paper confirms use of Cohen's d (d ≤ 0.2 small, d ≤ 0.5 medium, d ≤ 0.8 large). The specific d=2.0 value cannot be confirmed from accessible search results. d=2.0 would be 2.5× Cohen's "large" threshold — exceptionally high. Plausible for a staff-rated obvious environmental change (before: prison-like → after: refurbished with nature, privacy) but needs primary-source confirmation.

**Verdict:** PARTIALLY VERIFIED. Paper exists, is real, uses Cohen's d. Two flags: (1) study design miscategorized as RCT (it's quasi-experimental), (2) d=2.0 unconfirmed. GAP-279 filed.

---

## 2B.4 — Weltens 2023, OR 5.36 overcrowding→aggression

**Claim in MH BPC:** "Weltens 2023, OR 5.36 overcrowding→aggression" as Tier 1 evidence.

**Finding:** Two Weltens papers identified:
1. Weltens et al. (2021). "Aggression on the psychiatric ward: Prevalence and risk factors. A systematic review." *PLoS One* 16(10):e0258346. PMID 34624057. **Accessible, open access.**
2. Weltens et al. (2023). "Staff and ward factors associated with aggression development on an acute closed psychiatric ward: an experience sampling method study." *BMJ Open* 13(2):e067943. PMID 36806071.

**OR values in accessible 2021 review:** Graduated overcrowding ORs: 1.30 (5% surplus), 2.08 (5–10% surplus), 2.15 (>10% surplus). **None is 5.36.**

**2023 ESM study:** Full results inaccessible via search. OR 5.36 may be in this paper but cannot be confirmed.

**Verdict:** Author verified, exact statistic not confirmed. GAP-280 filed. The MH BPC should clarify which Weltens paper contains the OR 5.36. If not confirmable, downgrade to the documented ORs from the 2021 review.

---

## 2B.5 — Avandell NJ $12,000/month vs US ~$7,500/month → 60% premium

**Claim in accessibility-feature-market-value-uplift-framing.md:** "Avandell NJ: $12,000/month vs US memory-care average ~$7,500/month → 60% revenue premium"

**Finding — FABRICATION PATTERN CONFIRMED:**

| Component | Status |
|---|---|
| $12,000/month | PARTIAL — projected cost from Larry Carlson (UMC CEO) interview in Rethinking65, Apr 2023. Avandell has NOT opened. This is a projected price. |
| "US memory-care average ~$7,500/month" | **WRONG LABEL.** ~$7,500 approximates the NJ state average. Sources: NJ median $6,289 (MemoryCare.com), NJ median $7,000 (A Place for Mom), NJ range $6,500–$7,500 (MemoryCareFacilities.net). **US national** average is ~$5,650 (CareAvailability). |
| "60% revenue premium" | Arithmetic correct ($12,000 / $7,500 = 1.6). But denominator is NJ state avg mislabeled as US avg. Against actual US avg ($5,650), premium would be ~112%. |
| Source attribution | No academic or industry-standard source. CEO interview + mislabeled comparator. |

**Pattern match:** Identical to RULE 2026-04-09 findings — real numbers, wrong labels, creating a plausible but misleading calculation. The economics BPC was previously caught with 3 fabricated quantified findings. This is a 4th instance.

**Verdict:** FABRICATION PATTERN. GAP-278 updated with verification details.

---

## Methodology note

Each item was searched via web_search (2+ queries per item). Primary sources were retrieved where accessible. PubMed full-text access was unavailable for the PMC-hosted papers (reCAPTCHA blocking).

For items where exact statistics could not be confirmed (2B.3, 2B.4), the author and study existence were verified but the specific quantitative claim remains tagged `[UNVERIFIED-QUANT]`.

The adversarial research protocol's detection question was applied: "Does the cited evidence specifically validate THE SPECIFIC CLAIM, or does it just speak to the topic?" Results:
- 2B.1: evidence validates the research program, not the specific 2400mm figure (that's a different paper)
- 2B.3: study validates environmental design → dignity improvement, but NOT via the methodology the BPC claims (not RCT, not patient-reported)
- 2B.5: numbers are real but labels are wrong — the topic (memory care pricing) is real, the specific claim (60% vs US average) is fabricated via mislabeling
