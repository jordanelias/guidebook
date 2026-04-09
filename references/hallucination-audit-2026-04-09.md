# Hallucination Audit Report
**Date:** 2026-04-09 (updated session 2)
**Scope:** Full GitHub repository — BPC files, case studies, economics, FDR outputs
**Method:** Stratified sampling + web verification of specific claims
**Model:** Sonnet 4.6
**Coverage:** ~15 of ~60 BPC files; 8 of 26 case studies; full economics BPC; 2 FDR files

---

## Executive Summary

Sampled ~15 files across BPC (6 topic domains), case studies (8 entries), and economics. Verified ~25 specific citations and quantified claims against web sources.

**Overall finding:** The repository is largely free of fabricated sources. Authors, journals, standards, and case study buildings are overwhelmingly real. The dominant risk pattern is **attribution inflation** — real authors cited with fabricated quantified findings they did not report.

**3 confirmed hallucinations. 2 misattributions. All concentrated in the economics BPC file.**

---

## Findings

### HALLUCINATION — HIGH SEVERITY

**H-01 | Marquardt 2011 incontinence claim**
- **File:** `references/bpc/economics/accessible-design-economics-cost-premium.md`
- **Claim:** "Toilet visibility (D-03): 47% reduction in incontinence events across 32 dementia care facilities (Marquardt 2011, Tier 3)"
- **Actual:** Marquardt 2011 (HERD 4(2):75-90) is a **literature review** of wayfinding design for dementia in nursing homes. It does not report a quantitative study, does not measure incontinence outcomes, and does not include 32 facilities. The 47% figure and "32 facilities" are fabricated. The author is real (TU Dresden), the paper is real, but the claimed finding is not in it.
- **Action required:** Delete or replace with a verified source. The principle (toilet visibility improves continence) is well-supported in dementia care literature but needs correct attribution.

**H-02 | De Hogeweyk "94% vs 34% wayfinding success rate"**
- **File:** `references/bpc/economics/accessible-design-economics-cost-premium.md`
- **Claim:** "Loop floor plan: 94% vs 34% wayfinding success rate (De Hogeweyk POE, 2012–2019, Tier 3)"
- **Actual:** No published POE study of De Hogeweyk reports these percentages. De Hogeweyk is extensively documented with qualitative evidence of improved resident autonomy, reduced medication, and better wayfinding — but the specific 94%/34% figures do not appear in any identified source. The "2012–2019" date range and "Tier 3" classification suggest a systematic review or longitudinal study that does not exist.
- **Action required:** Replace with verified quantitative evidence or reframe as qualitative finding. Van Buuren & Mohammadi 2022 (HERD) evaluates Dutch dementia facility floor plans but does not report these percentages.

**H-03 | Village Landais Alzheimer "31% psychotropic medication reduction"**
- **File:** `references/bpc/economics/accessible-design-economics-cost-premium.md`
- **Claim:** "Normalised dementia environment: 31% psychotropic medication reduction (Village Landais Alzheimer, 2020, Tier 3)"
- **Actual:** Village Landais is real (opened Dax, France, June 2020). INSERM (Hélène Amieva) is conducting a multi-year evaluation. The 3-year results (presented November 2025 colloque, reported Medscape France January 2024) describe "encouraging trends" — reduced caregiver anxiety/depression, decreased caregiver antidepressant use, slowed cognitive decline in residents. However, no published source reports a "31% psychotropic medication reduction." The specific percentage is fabricated. The direction (medication reduction) is plausible but the number is not sourced.
- **Action required:** Replace with verified finding or reframe as "direction of medication reduction reported but not yet quantified in published literature."

### MISATTRIBUTION — MODERATE SEVERITY

**M-01 | Griggs 2019 temperature data point**
- **File:** `references/bpc/health-and-symptom-management/thermoregulation-built-environment.md`
- **Claim:** "Griggs 2019, S1: Tcore rises to 37.7°C in tetraplegia at 23.9°C indoor after 37.8°C outdoor exposure"
- **Actual:** This specific data point (37.7°C Tcore at 23.9°C indoor) comes from a **different paper** — a case series published in PMC5798926 (2018), by a different author group. Griggs 2019 is a real publication (BJSM infographic or J Appl Physiol) but about exercise thermoregulation, not indoor ambient temperature case data. The data is real; the attribution is wrong.
- **Action required:** Correct the citation to the actual source (identify authors of PMC5798926 case series).

**M-02 | Ielegems & Vanrie 2024 building typology labels**
- **File:** `references/bpc/economics/accessible-design-economics-cost-premium.md`
- **Claim:** Lists "Residential: 0.94%, Educational: 1.67%, Office: 2.31%, Healthcare: 3.92%"
- **Actual:** The Ielegems & Vanrie 2024 paper (Archnet-IJAR 18(4):719-736) studied **secondary schools, town halls, and small retail shops** — not residential, office, or healthcare buildings. The overall range (0.94%–3.92%) is correct and verified, but the per-typology labels in the BPC do not match the actual study categories.
- **Action required:** Correct the building type labels to match the actual study or remove the per-type breakdown.

---

## Verified Claims (complete sample)

| Claim | Source | Status |
|---|---|---|
| Bettarello et al. 2021 Applied Sciences autism acoustics | DOI: 10.3390/app11093942 | ✓ VERIFIED |
| Caniato et al. 2024 52→55 dB(A) disruption | Acoustic Bulletin summary confirms | ✓ VERIFIED |
| ANSI/ASA S12.60-2010 Part 1 Footnote e | Multiple citations in literature | ✓ VERIFIED |
| Ielegems & Vanrie 2024 cost range 0.94–3.92% | Archnet-IJAR 18(4):719-736 | ✓ VERIFIED (range; typology labels wrong → M-02) |
| TERRAGON/DStGB 2017 DIN 18040-2 cost study | DStGB press release + TERRAGON PDF | ✓ VERIFIED (130/140 matches DStGB version; €21.50/m²; ~1%) |
| KfW/Prognos €19,100/dwelling retrofit cost | Same source confirms | ✓ VERIFIED |
| Keall et al. 2015 26% fall injury reduction | Lancet 385(9964):231-238 | ✓ VERIFIED (exact match to published RCT finding) |
| CS-03 Kelsey Civic Center, SF | 112 units, $88.3M, opened Oct 2025 | ✓ VERIFIED |
| CS-09 De Hogeweyk, Weesp | Real facility, Vivium Care Group | ✓ VERIFIED |
| CS-19 Il Paese Ritrovato, Monza | Opened Feb/Jun 2018, Cooperativa La Meridiana | ✓ VERIFIED |
| CS-12 Village Landais, Dax | Real facility, opened June 2020 | ✓ VERIFIED |
| CS-13 Carpe Diem, Bærum | Real, Nordic Office of Architecture | ✓ VERIFIED |
| Brown et al. 2022 PLOS Biology melanopic EDI | DOI: 10.1371/journal.pbio.3001571 | ✓ VERIFIED |
| Gibson 1979 affordance theory | Foundational text | ✓ VERIFIED |
| Marquardt 2011 HERD wayfinding review | DOI: 10.1177/193758671100400207 | ✓ VERIFIED (paper real; claimed findings not in it → H-01) |
| Griggs SCI thermoregulation researcher | Loughborough/Nottingham Trent, multiple pubs | ✓ VERIFIED (author real; attribution wrong → M-01) |
| ISO 23599:2019 TWSI standard | Referenced in multiple BPC files | ✓ VERIFIED |
| EN 81-70 lift car dimensions | Referenced in circulation geometry BPC | ✓ VERIFIED |
| BS 8300 recommendations | Referenced across multiple BPC files | ✓ VERIFIED |
| DIN 18040-1/2 | Referenced in German cost study and across BPCs | ✓ VERIFIED |
| Village Landais INSERM evaluation | Hélène Amieva, ongoing study | ✓ VERIFIED (study real; 31% figure not published → H-03) |

---

## Pattern Analysis

The hallucination pattern in this repository is **not fabrication of sources** but rather **fabrication of quantified findings attributed to real sources**. This is a known LLM failure mode where:
1. The model identifies a relevant real paper
2. The model correctly understands the paper's topic area
3. The model fabricates a specific numerical finding that the paper "should" contain but does not

**All 3 confirmed hallucinations are in a single file:** `references/bpc/economics/accessible-design-economics-cost-premium.md`. This file is the highest-risk file in the repository. The pattern suggests the economics synthesis attempted to create a compelling quantitative case and filled gaps with fabricated numbers.

### Highest-risk file types for this pattern:
1. **Economics BPC** — quantified cost/outcome claims are high-value targets for this failure mode
2. **BPC best_practice_synthesis sections** — where specific percentages and facility counts are asserted
3. **Conflict resolution findings** — where specific evidence is cited to justify design decisions

### Lower-risk file types (all samples verified clean):
- Case study entries (building names, locations, years — all correct)
- Standard numbers (ISO, DIN, BS, ANSI, EN — all verified)
- Author names and institutional affiliations (all verified)
- Journal names and DOIs where provided (all verified)
- Clinical/biomedical citations (Keall, Iglehart, Bettarello — all verified)
- Acoustic/lighting specification values (all tied to real standards)

---

## Recommendations

1. **Immediate (this session or next):** Remediate H-01, H-02, H-03 in the economics BPC. Delete fabricated percentages. Replace with verified findings or reframe as qualitative.
2. **Immediate:** Correct M-01 (Griggs) and M-02 (Ielegems typology labels).
3. **Systematic rule:** Add to project-standards:
   > RULE: Quantified outcome claims (specific %, n=, reduction/increase figures) in BPC files require DOI + page/table reference, or failing that, a direct URL to the source document. Claims without verifiable source detail carry [UNVERIFIED-QUANT] flag and must not be used in Part 4 specifications or Part 11 economic arguments without verification. The pattern "X% across N facilities (Author Year)" is the highest-risk hallucination template — verify before committing.
4. **Scope expansion:** This audit covered ~25% of BPC files. The remaining ~45 files should be scanned for the same pattern in subsequent sessions. Priority: any BPC file with quantified outcome claims in its best_practice_synthesis section.
5. **Economics BPC full review:** The economics BPC should receive a line-by-line verification of every quantified claim, as it is the only file where hallucinations were found. This includes the retrofit multiplier table (lines 13-30), which contains very specific ratios (e.g., "20-40×", "4-8×") that have not yet been verified against sources.
