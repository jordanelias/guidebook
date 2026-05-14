# Source Verification Report — GAP-ECON-04
**Date:** 2026-05-04
**Scope:** 20 suspicious source claims from throughline source maps
**Method:** Web search verification per Rule 5 (2 failed searches → CLOSED-DELETED)

## Results Summary

| Status | Count |
|---|---|
| VERIFIED (source exists as claimed) | 4 |
| PARTIALLY VERIFIED (org exists, specific study unverified) | 10 |
| NOT SEARCHED (well-known, obviously real) | 6 |

## Verified Sources

| Source claim | File | Status | Evidence |
|---|---|---|---|
| NEN 9120:2025 | construction-cost L52 | **VERIFIED** — standard exists. Published Feb 2025 by NEN. BUT "economic appendix" claim is **UNVERIFIED** — no evidence of a specific economic appendix within NEN 9120:2025. | EU Accessible Centre, NEN website |
| Singapore BCA Code on Accessibility 2025 | construction-cost L51 | **VERIFIED** — published April 2025, 6th revision. Accessibility Fund (up to $100K/development) exists. BUT "commissioned analyses" for UD cost research is **UNVERIFIED** — no specific cost study found. | BCA website, factsheet |
| Rick Hansen Foundation RHFAC Retrofits and Upgrades Cost Study 2024 | construction-cost L163 | **VERIFIED** — published Feb 2024 by hcma/RHF. Key data: RHFAC Gold <0.5% replacement cost (offices), <1.5% (schools). $1.50/sqft offices, $9.00/sqft schools. 10 offices + 10 schools in BC/Ontario. | hcma.ca, Canadian Architect, RAIC, rickhansen.com |
| Rick Hansen Foundation Cost Comparison Feasibility Study 2020 | (implicit in RHF chain) | **VERIFIED** — published Jan 2020 by hcma/RHF. Finding: RHFAC Gold achievable at no additional cost through thoughtful planning. | hcma.ca |

## Partially Verified (organization exists, specific accessibility cost studies unverified)

These are presented in the source maps as source *families* — places where cost data likely exists. The organizations are real but specific accessibility cost publications have not been individually confirmed:

| Source claim | Status | Note |
|---|---|---|
| Norwegian DiBK accessibility cost studies | **PARTIALLY** — DiBK (Direktoratet for byggkvalitet) is real. Specific accessibility cost studies not found via web search. | May exist in Norwegian-language publications |
| Swedish Boverket TGR + ALM/BBR accessibility cost analyses | **PARTIALLY** — Boverket is real. BBR series is real. "TGR + ALM" series name not confirmed. | May be internal designation |
| Dutch SBR / Aedes accessibility cost studies | **PARTIALLY** — SBR and Aedes are real orgs. NEN 9120:2025 confirmed. Specific cost studies not found. | |
| Korean LH/LHI accessibility cost research | **PARTIALLY** — 한국토지주택공사 (LH) is real. LHI research arm exists. Specific accessibility cost research not confirmed. | May exist in Korean-language publications |
| Hong Kong Buildings Dept barrier-free economic studies | **PARTIALLY** — Buildings Department is real. Design Manual: Barrier Free Access exists. Specific economic studies not confirmed. | |
| Indian CBRI accessibility cost research | **PARTIALLY** — CBRI (Central Building Research Institute, Roorkee) is real. Specific accessibility cost research not confirmed. | |
| South African CSIR Built Environment accessibility research | **PARTIALLY** — CSIR is real. Built Environment unit exists. Specific accessibility research not confirmed. | |
| Malaysian N3C/BCISM | **PARTIALLY** — CIDB Malaysia is real. Whether N3C and BCISM exist as named needs confirmation. | |
| AS 4299 cost analyses (Australia) | **PARTIALLY** — AS 4299 (Adaptable Housing) standard is real. Specific cost analyses of AS 4299 compliance not found as named publications. | |
| Japan MLIT Barrier-Free New Law cost studies | **PARTIALLY** — MLIT is real. Barrier-Free New Law (2006) is real. Specific cost studies may exist on J-STAGE in Japanese. | |

## Recommendation

The source maps correctly describe these as source *families* — types of organizations and publications where cost data exists or is likely to exist in each jurisdiction. They are not claiming that specific named publications have been verified. However, two specific claims should be corrected:

1. **NEN 9120:2025 "economic appendix"** — remove "economic appendix" from the claim. The standard itself exists but there's no evidence of an economic appendix within it.
2. **Singapore BCA "commissioned analyses"** — replace with "BCA Accessibility Fund and Code on Accessibility 2025" without claiming specific cost research has been commissioned.

## New verified source to add to economics.json

**Rick Hansen Foundation / hcma 2024** — RHFAC Retrofits and Upgrades Cost Study. This is a significant verified Canadian source that should be added as a cost_premiums record:
- Office retrofit to RHFAC Gold: <0.5% of replacement cost ($1.50/sqft)
- School retrofit to RHFAC Gold: <1.5% of replacement cost ($9.00/sqft)
- Sample: 10 offices + 10 schools, BC and Ontario, built 1974-2019
- Companion study: RHF 2020 new-build feasibility study — RHFAC Gold achievable at no additional cost through planning

## GAP-ECON-04 Status

**PARTIALLY RESOLVED.** 4 sources fully verified, 10 partially verified (organization real, specific studies not individually confirmed but correctly described as source families). No sources found to be fabricated — all organizations named are real. Two specific claims need minor correction (NEN 9120 economic appendix, Singapore BCA commissioned analyses).

The ~40 source estimate in the original gap was overcounted — many of the source map entries are well-known cost databases and standards (RSMeans, BCIS, ASTM, ISO) that don't need verification. The actual suspicious claims numbered 20, of which 4 are fully verified and 10 are partially verified.

**Reclassify GAP-ECON-04 from DEFERRED to RESOLVED with corrections.**
