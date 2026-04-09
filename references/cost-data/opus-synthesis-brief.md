# Opus Synthesis Brief — Construction Cost Economics
<!-- Prepared: 2026-04-09 23:00 | Prepared by: Sonnet 4.6 | For: Opus 4.6 session -->
<!-- Standing rule 6: Sonnet never determines best practice. This brief presents assembled evidence for Opus synthesis. -->

## Task

Three synthesis items requiring Opus-level judgment:

### 1. Economic Argument Framing for Parts 1 and 10

**Evidence assembled (read `references/cost-data/` before synthesising):**

The cross-jurisdictional evidence converges on a central finding: accessibility costs virtually nothing at design stage but is 2×–15× more expensive to retrofit. Specifically:

- **DE (TERRAGON/DStGB 2017, E-3/E-4):** 138/148 DIN 18040-2 criteria produce zero cost. Full compliance = 0.54%–1.26% of construction cost. Retrofit avg = €19,100/apartment (KfW/Prognos). Retrofit is 12× more expensive.
- **BE (Ielegems & Vanrie 2024, E-1):** 0.94%–3.92% new-build; 2.24%–14.9% renovation. Avg 1.19% for large projects. Peer-reviewed, 12 case studies.
- **US (ADA National Network 2025, E-6; HUD/Woodstock 2020, E-2):** <1% new-build. Chicago HomeMod avg $12,200–$15,150/unit retrofit. Cost-benefit positive: only 2.5%–4.6% of participants deferring assisted-living for 5 years breaks even for government.
- **CA (RHFAC/HCMA 2024, E-6):** ~1% or zero.
- **SE (Lund University, E-1):** Not significant.
- **NL (EIB 2020, E-3; EU research via NEN, E-6):** 1–1.4%. Specific items (lift, balcony): €4,000/apartment.
- **DK (NCC, E-4):** "Does not have to cost extra if thought into the project from start."
- **FR (FFB, E-7):** 2–5% — CONTESTED by disability organisations; commercial interest source.
- **NO (Husbanken, E-2):** 92% of housing stock fails basic accessibility.
- **JP (Kaigo Hoken, E-2):** Government subsidises 90% of ¥200K modification cost.
- **KR:** BF certification mandatory for public buildings since 2015.

**Synthesis questions for Opus:**
1. What is the best-practice framing for the guidebook's economic argument? The evidence supports "design-stage inclusion is near-zero cost; retrofit is the expensive path" — but how should this be articulated in Part 1 (foundations) vs Part 10 (adaptable readiness)?
2. Should the guidebook cite specific cost percentages, or present the evidence pattern without headline numbers? The German 0.54%–1.26% figure is the most granular and defensible, but jurisdiction-specific.
3. How should the contested French FFB figure (2–5%) be handled? It is the only outlier and comes from a source with commercial interest.

### 2. Cost Data Architecture

**Question:** Should per-item retrofit costs live in:
- (a) Part 4 `Retrofit cost note:` fields (already scaffolded — see A-01 example)
- (b) A standalone economics section/appendix
- (c) Both, with cross-reference

Part 4 already has `Retrofit cost note:` architecture (A-01 has one: "Retrofit penalty: LOW — PLANNING"). The E-7 consumer cost data assembled in `bottom-up-construction-costs.md` maps to Part 4 items (E-01, E-03, G-03, G-04, H-01, I-04, etc.). But economics-researcher scope says "Product pricing or equipment market data" is out of scope.

**Tension:** The Part 4 retrofit cost notes serve architects estimating project cost. The economics section serves the investment-case argument. These are different audiences with different needs from the same data.

### 3. HUD Cost-Benefit Methodology Integration

The HUD/Woodstock (2020) study demonstrates a methodology for comparing modification costs against avoided costs (assisted-living deferral, reduced personal care, reduced emergency services). The finding that only 2.5%–4.6% of participants deferring assisted-living for 5 years is sufficient to break even is powerful.

**Question:** Can/should the guidebook's three-tier hierarchy be mapped to a cost-benefit framework? E.g.:
- Tier 0 (Universal/Code): Near-zero marginal cost at design stage → infinite ROI
- Tier 1 (Population-Informed): Low-moderate cost → high ROI via falls prevention, independent living
- Tier 2 (Person-Specific/OT): Variable cost → cost offset by avoided institutional care

This would give practitioners an economic justification for each tier, beyond the equity/rights argument.

## Source Files

Load before synthesis:
- `references/cost-data/bottom-up-construction-costs.md`
- `references/cost-data/multilingual-construction-costs.md`
- `references/economics-sources.md`
- `references/bpc/economics/construction-cost-data.md`

## Citation Mining Targets (from Ielegems 2024 bibliography)

These studies were identified but not yet accessed. Priority for retrieval:

| Citation | Why priority |
|---|---|
| Steinfeld, E. (2005). Education for All: The cost of accessibility. World Bank EdNotes. | Seminal; schools context; cost control guidelines |
| Société Logique (2015). Study of the Cost of Including Accessibility Features in Newly-Constructed Modest Houses. CMHC. | Canadian residential; CMHC = E-2/E-3 tier |
| Terashima, M. & Clark, K. (2021). Measuring economic benefits of accessible spaces. JADA, 11(2), 195–231. | Systematic review of economic evidence |
| Fuglerud, K.S., Halbach, T. & Tjøstheim, I. (2015). Cost-benefit analysis of universal design. NR Report 1032. | Norwegian cost-benefit; Norsk Regnesentral |
| Jones, P. (2011). [specific building aspect UD cost study — title not retrieved] | Cited by Ielegems as single-aspect cost analysis |

## Jurisdiction Coverage Summary

| Status | Count | Jurisdictions |
|---|---|---|
| SEARCHED | 13 | US, UK, AU, DE, FR, SE, NO, JP, CA, BE, NL, KR, EU |
| NOT-RUN | 33 | CH, DK (partial), FI, NZ, SG, IE, IT, ES, BR, CN + all Tier A/B |

Languages searched: EN, DE, FR, SV, NO, JA, NL, KO, DA (partial) = 9/19
