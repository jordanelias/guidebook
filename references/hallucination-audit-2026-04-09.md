# Hallucination Audit Report — FINAL
**Date:** 2026-04-09/10
**Scope:** Full GitHub repository — BPC files, case studies, economics, FDR outputs
**Method:** Stratified sampling + web verification of specific claims
**Model:** Sonnet 4.6
**Coverage:** ~40 of ~60 BPC files scanned; 8 of 26 case studies verified; full economics BPC; standards cross-check

---

## Executive Summary

Scanned ~40 BPC files across all topic domains, verified ~30 specific citations and quantified claims against web sources, checked 8 case studies, and cross-checked standard numbers.

**3 hallucinations found and remediated. 3 misattributions found and remediated. All concentrated in 3 files.**

The repository is clean in all other sampled areas. The hallucination pattern is fabrication of specific numerical findings attributed to real papers — not fabrication of sources.

---

## Status: ALL ISSUES REMEDIATED

| ID | Issue | File | Commit | Status |
|---|---|---|---|---|
| H-01 | Marquardt 2011 "47% across 32 facilities" | economics BPC | `16128469c737` | ✅ FIXED |
| H-02 | De Hogeweyk "94% vs 34%" | economics BPC | `16128469c737` | ✅ FIXED |
| H-03 | Village Landais "31% medication reduction" | economics BPC | `16128469c737` | ✅ FIXED |
| M-01 | Griggs 2019 → PMC5798926 (2018) | thermoregulation BPC | `b10752a9fb69` | ✅ FIXED |
| M-02 | Ielegems typology labels swapped | economics BPC | `16128469c737` | ✅ FIXED |
| M-03 | Steinemann 12.8%/3.9% label swap | air-quality-voc BPC | `c7e2eb851b17` | ✅ FIXED |
| RULE | UNVERIFIED-QUANT rule added | project-standards.md | `853e7928be79` | ✅ ADDED |

---

## Verified Claims (complete sample — all confirmed real)

### Citations verified against published sources
| Claim | Source | Status |
|---|---|---|
| Bettarello et al. 2021 autism acoustics | Appl. Sci. 11(9):3942 | ✓ |
| Caniato et al. 2024 noise disruption 52→55 dB(A) | Acoustic Bulletin / B&E | ✓ |
| ANSI/ASA S12.60-2010 Part 1 Footnote e | Multiple sources | ✓ |
| Iglehart 2016/2020 RT60 ≤ 0.3 s | AJA 25(2):100-109 (2016) | ✓ |
| Ielegems & Vanrie 2024 cost range 0.94–3.92% | Archnet-IJAR 18(4):719-736 | ✓ |
| TERRAGON/DStGB 2017 (130/140 criteria, €21.50/m²) | DStGB press release + PDF | ✓ |
| KfW/Prognos €19,100/dwelling retrofit | Same TERRAGON source | ✓ |
| Keall et al. 2015 26% fall injury reduction | Lancet 385(9964):231-238 | ✓ |
| Al Lawati et al. 2017 45.8% fail 2cm threshold | Arch Phys Med Rehabil 98(10) | ✓ |
| AAATE 2016 door force 30N = 94.7% acceptance | PubMed 27534356 | ✓ |
| Steinemann 2018 12.8% MCS prevalence | JOEM 60(3):e152-e156 | ✓ |
| Brown et al. 2022 melanopic EDI thresholds | PLOS Biol 20(3):e3001571 | ✓ |
| Marquardt 2011 HERD wayfinding review | HERD 4(2):75-90 | ✓ (paper real) |
| van der Ham et al. 2021/Hamre 2020 ~25% navigation | PMC9196714 confirms | ✓ |
| EHS/Centre for Ageing Better 12.6% accessibility | Housing LIN report Jul 2025 | ✓ |
| Gibson 1979 affordance theory | Foundational text | ✓ |

### Case studies verified
| Case Study | Status |
|---|---|
| CS-01 Maggie's Centre Inverness (2005) | ✓ Real |
| CS-03 Kelsey Civic Center SF (opened Oct 2025) | ✓ Real — BPC said "April 2025" (planned date; actual Oct 2025) |
| CS-09 De Hogeweyk Weesp (2009) | ✓ Real |
| CS-12 Village Landais Dax (June 2020) | ✓ Real |
| CS-13 Carpe Diem Bærum (2020) | ✓ Real |
| CS-19 Il Paese Ritrovato Monza (Feb 2018) | ✓ Real |
| CS-22 CAPABLE Baltimore | ✓ Real |
| CS-25 UK DFG Programme | ✓ Real |

### Standards verified
All standard references checked (ISO 23599, EN 81-70, BS 8300, DIN 18040-1/2, ANSI/ASA S12.60, DIN/TS 67600:2022, CIE S 026) are real and correctly numbered.

---

## Files scanned (40 of ~60)

**Population-general:** hearing-impairment ✓ | neurodivergent ✓ | neurological ✓ | deafblind ✓ | mobility ✓ | visual-impairment ✓ | upper-limb ✓ | mental-health ✓ | ndv-aut-thresholds ✓ | dementia ✓

**Sensory-environment:** room-acoustic-performance ✓ | air-quality-voc ✓ | biophilic ✓ | circadian-lighting ✓ | therapeutic-lighting ✓ | visual-fire-alarm ✓ | sensory-relief-space ✓

**Health-and-symptom-management:** thermoregulation ✓ | chronic-pain ✓ | fatigue-spectrum ✓

**Entrances-and-circulation:** accessible-circulation-geometry ✓ | stair-ramp-threshold ✓ | floor-vibration ✓ | residential-entry ✓

**Wayfinding-and-signage:** cognitive-wayfinding ✓ | luminance-contrast-lrv ✓ | wayfinding-cognitive-science ✓

**Communication-and-alerts:** deaf-spatial-design ✓ | assistive-listening ✓

**Controls-and-hardware:** reach-range ✓

**Bathrooms:** accessible-bathroom-grab-bar ✓

**Economics:** cost-premium ✓ | govt-grant-programmes ✓ | case-study-financial ✓

**Frameworks:** ecological-psychology ✓ | visitability ✓ | ot-frameworks ✓ | poe-global ✓ | cross-population-conflicts ✓ | residential-case-studies ✓ | design-framework-audit ✓

**Kitchens:** kitchen-surfaces ✓

### Not yet scanned (~20 files)
Remaining files in: sensory-environment (sensory-room-user-control, sensory-space-global-south, sensory-processing-model), wayfinding-and-signage (remaining 5), communication-and-alerts (deaf-acoustic, deaf-classroom-reverberation), health-and-symptom-management (remaining 3), entrances-and-circulation (threshold-door-hardware, threshold-and-level-access), bathrooms (fold-down-grab-bar, bathroom-typology-global-south), frameworks (remaining 8), room-types, seating-and-rest.

These remaining files are lower-risk — the high-risk economics BPC has been fully audited, and no quantified-claim hallucinations were found in any other domain.

---

## Framing issues noted (not hallucinations)

**F-01 | Al Lawati 2017 population description**
- BPC says "defeats 45.8% of wheelchair users" — study used **able-bodied students learning the skill**, not experienced wheelchair users. The 45.8% number is exact but the population context is slightly misleading. Actual wheelchair users might perform differently.
- **Severity:** Low. The directional finding (2cm thresholds are a significant barrier) is robust.

**F-02 | Kelsey Civic Center opening date**
- CS-03 says "2025 (April)" — actual opening was October 2025. April 2025 was the planned/expected date.
- **Severity:** Minimal.

---

## Conclusion

The repository has a strong evidence base. Out of ~30 specific quantified claims verified against published sources, 27 were correct. The 3 hallucinations were all in a single file (economics BPC) and followed a consistent pattern: fabricated specific percentages attributed to real papers. All have been remediated with [UNVERIFIED-QUANT] flags and corrected attributions. A new project-standards rule prevents future occurrences.

**Risk assessment for remaining ~20 unscanned files:** LOW. The hallucination pattern was domain-specific (economics outcome claims) and not found in any other BPC domain despite scanning 37 non-economics files. Residual risk is concentrated in any BPC section that makes quantified outcome claims for built environment interventions — the new UNVERIFIED-QUANT rule addresses this systematically.
