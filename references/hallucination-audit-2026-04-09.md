# Hallucination Audit Report
**Date:** 2026-04-09
**Scope:** Full GitHub repository — BPC files, case studies, economics, FDR outputs
**Method:** Stratified sampling + web verification of specific claims
**Model:** Sonnet 4.6

---

## Executive Summary

Sampled ~15 files across BPC (6 topic domains), case studies (8 entries), and economics. Verified ~20 specific citations and quantified claims against web sources.

**Overall finding:** The repository is largely free of fabricated sources. Authors, journals, standards, and case study buildings are overwhelmingly real. The dominant risk pattern is **attribution inflation** — real authors cited with fabricated quantified findings they did not report.

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

### UNVERIFIED — LOW SEVERITY (flagged for follow-up)

**U-01 | Village Landais Alzheimer "31% psychotropic medication reduction"**
- **File:** `references/bpc/economics/accessible-design-economics-cost-premium.md`
- **Claim:** "Normalised dementia environment: 31% psychotropic medication reduction (Village Landais Alzheimer, 2020, Tier 3)"
- **Status:** Not verified in this session. Village Landais is a real facility (opened Dax, France, June 2020). Medication reduction is plausible (consistent with De Hogeweyk and Il Paese Ritrovato qualitative reports). The 31% figure needs source verification.

**U-02 | Iglehart year attribution**
- **File:** `references/bpc/sensory-environment/room-acoustic-performance.md`
- **Claim:** "Iglehart, 2020, AJA" for RT60 ≤ 0.3 s classroom finding with cochlear implants
- **Status:** The CI-specific finding (0.3 s RT60 benefit) is from Iglehart **2016** (AJA 25(2):100-109). Iglehart 2020 (AJA) extends the work to hearing aids. Both papers are real and support the claim. Minor year discrepancy — the 2016 paper is the primary CI source.

---

## Verified Claims (sample — all confirmed real)

| Claim | Source | Status |
|---|---|---|
| Bettarello et al. 2021 Applied Sciences autism acoustics | DOI: 10.3390/app11093942 | ✓ VERIFIED |
| Caniato et al. 2024 52→55 dB(A) disruption | Acoustic Bulletin summary confirms | ✓ VERIFIED |
| ANSI/ASA S12.60-2010 Part 1 Footnote e | Multiple citations in literature | ✓ VERIFIED |
| Ielegems & Vanrie 2024 cost range 0.94–3.92% | Archnet-IJAR 18(4):719-736 | ✓ VERIFIED (range; typology labels wrong) |
| CS-03 Kelsey Civic Center, SF | 112 units, $88.3M, opened Oct 2025 | ✓ VERIFIED |
| CS-09 De Hogeweyk, Weesp | Real facility, Vivium Care Group | ✓ VERIFIED |
| CS-19 Il Paese Ritrovato, Monza | Opened Feb/Jun 2018, Cooperativa La Meridiana | ✓ VERIFIED |
| CS-12 Village Landais, Dax | Real facility, opened June 2020 | ✓ VERIFIED |
| CS-13 Carpe Diem, Bærum | Real, Nordic Office of Architecture | ✓ VERIFIED |
| Brown et al. 2022 PLOS Biology melanopic EDI | DOI: 10.1371/journal.pbio.3001571 | ✓ VERIFIED |
| Gibson 1979 affordance theory | Foundational text | ✓ VERIFIED |
| Marquardt 2011 HERD wayfinding review | DOI: 10.1177/193758671100400207 | ✓ VERIFIED (paper real; claimed findings not in it) |
| Griggs SCI thermoregulation researcher | Loughborough/Nottingham Trent, multiple pubs | ✓ VERIFIED (author real; attribution wrong) |

---

## Pattern Analysis

The hallucination pattern in this repository is **not fabrication of sources** but rather **fabrication of quantified findings attributed to real sources**. This is a known LLM failure mode where:
1. The model identifies a relevant real paper
2. The model correctly understands the paper's topic area
3. The model fabricates a specific numerical finding that the paper "should" contain but does not

This is harder to detect than pure source fabrication because the citation trail looks legitimate until the specific claim is checked against the actual paper.

### Highest-risk file types for this pattern:
1. **Economics BPC** — quantified cost/outcome claims are high-value targets for this failure mode
2. **BPC best_practice_synthesis sections** — where specific percentages and facility counts are asserted
3. **Conflict resolution findings** — where specific evidence is cited to justify design decisions

### Lower-risk file types:
- Case study entries (building names, locations, years are verifiable and were correct)
- Standard numbers (ISO, DIN, BS, ANSI — all verified as real)
- Author names and institutional affiliations (all verified)
- Journal names and DOIs where provided (all verified)

---

## Recommendations

1. **Immediate:** Remediate H-01 and H-02 in the economics BPC. These are specific false claims with fabricated numbers.
2. **Immediate:** Correct M-01 and M-02 attributions.
3. **Systematic:** Any BPC claim with a specific percentage + facility count + single author citation should be verified before publication. This pattern (e.g., "X% across N facilities (Author Year)") is the highest-risk template for this hallucination type.
4. **Process:** Add a project-standards rule: "Quantified outcome claims (%, n=, reduction/increase) require DOI or direct page reference. Claims without these markers carry [UNVERIFIED-QUANT] flag."
5. **Scope expansion:** This audit sampled ~15 of ~60 BPC files. A full audit of all quantified claims across all BPC files would require ~4 additional sessions at this verification depth.
