# Economics Audit & Research Findings — 2026-05-03

**Session:** 2026-05-03
**Model:** Opus 4.6
**Task:** Audit of economics/financials work + new research to acquire additional data
**Status:** INTERIM — research continuing

---

## A. Audit of Economics Work (2026-05-02 commits)

### Documents examined
- `references/methodology/economics-research-methodology.md` (v1.0–v1.6, 178,947 chars)
- `references/bpc/economics/accessibility-feature-market-value-uplift-framing.md` (29,726 chars)
- `references/bpc/economics/accessible-design-economics-cost-premium.md` (10,133 chars)
- `references/bpc/economics/case-study-economics-financial-data.md` (8,864 chars)
- `references/bpc/economics/construction-cost-data.md` (4,297 chars)
- `references/bpc/economics/government-grant-programmes-home-adaptation.md` (6,698 chars)
- `references/economics/cost-intelligence-accessible-construction.md` (24,289 chars)
- `references/economics/cost-intelligence-supplement.md` (7,073 chars)
- `references/economics/bottom-up-cost-data-uk-au-2026.md` (6,332 chars)
- `parts/v10/part11.md` (66,175 chars)
- GAP-METH-ECON-01 through GAP-METH-ECON-07

### Positive findings
- A.1 Q1–Q7/V1–V5 cost taxonomy is a genuine methodological contribution
- A.2 v1.1 fabrication remediation caught and corrected 7+ fabricated source names — thorough
- A.3 GAP/CONFIDENCE/ASSUMPTION markers used throughout; self-awareness of limitations is good
- A.4 Case-study financial register honest: 5 VERIFIED / 4 PROVISIONAL / 17 GREY
- A.5 Government programme data well-sourced across 8 jurisdictions
- A.6 Voice register declaration (§0) appropriate — separates methodology from specification voice

### Concerns

#### B.1 [HIGH] Throughline 1 "Tier 1 by inheritance" overclaim
The methodology doc claims ~8 dimensionally-driven registry items inherit "Tier 1" evidence from Sirmans 2006. The logic chain skips the step where marginal value varies by use — the marginal value of 2.4m² of widened corridor is not equivalent to 2.4m² of additional living space. Hedonic coefficients are marginal and non-linear. Re-tier to Tier 2 (transferable inference) for most items; Tier 3 for items where floor-area-added is genuinely usable room space (G-04 wet room, accessible bedroom).

#### B.2 [HIGH] Cost vs. Value 61% ROI framing misleading
The UD bath ($42,183) returns 61% ROI vs midrange bath ($26,138) returning 80% ROI. The UD bath loses $16,451 at sale vs $5,228 for midrange — 3.15× more money lost. The "+12 pp YoY gain" is noted but the absolute ROI is lower than the alternative. Reframe to lead with absolute comparison, then note non-financial value.

#### B.3 [HIGH — CORRECTED BELOW] CMHC/Société Logique mischaracterized
See §B below. The "few hundred to few thousand dollars per unit" paraphrase in §15.13.3 is from a secondary source. The primary CMHC source reports 6-12% per dwelling.

#### B.4 [MEDIUM] German cost premium discrepancy
TERRAGON/DStGB 2017: 0.35-1.26% for DIN 18040-2 basic barrierefrei. bau.de 2026: 5-10% for full barrierefrei. Resolved: scope-dependent (see §B.2 below).

#### B.5 [MEDIUM] §15 scope creep — methodology document has become substantive analysis
§15 runs ~100,000+ chars and contains per-item ROI computations, price-tier segmentation, marketing strategy. Extract §15.10–§15.13 to separate analytical document.

#### B.6 [MEDIUM] Avandell 60% premium attribution weak
Compares single luxury NJ facility to national average. Multiple confounds (location, service level, facility age). Reword to acknowledge confounds.

#### B.7 [MEDIUM] TERRAGON commercial interest not flagged
TERRAGON is a developer of barrier-free housing (~2,000 units built). Study showing low costs has commercial interest. French FFB figure excluded for same reason but TERRAGON retained without equivalent caution. Critique from Ulrike Jocham ("Die Frau Nullschwelle") flags unsubstantiated claims regarding thresholds.

#### B.8 [LOW] Currency/base-year anchoring inconsistent across files
#### B.9 [LOW] Evidence-tier notation differs between files (E-1/E-2 vs Tier 1/Tier 2)

---

## B. New Research Findings

### B.1 CMHC/Société Logique — primary source data (CORRECTION)

**Source:** CMHC Research Bulletin, May 2016. "Cost of Accessibility Features in Newly-Constructed Modest Houses." CMHC Project Manager: Janet Kreda. Consultant: Société Logique. Five Canadian cities: Vancouver, Winnipeg, Toronto, Montréal, Halifax.

**Scope:** 60 accessibility features covering access to dwelling, building layout, garage, mobility inside house, kitchen and bathroom design, windows, controls, allowances for future lift, fire safety.

**Per-feature cost distribution:**
- 57% of features: $0-$99 or not applicable
- 18%: $100-$499
- 8%: $500-$999
- 17%: $1,000 or more

**Per-dwelling cost premium (% of standard construction cost):**

| Building type | Montréal | Toronto | Vancouver | Halifax | Winnipeg |
|---|---|---|---|---|---|
| Bungalow | 6% | 6% | 6% | 6% | 6% |
| Semi-detached | 12% | 12% | 11% | 12% | 12% |
| Detached | 10% | 10% | 9% | 10% | 10% |
| Townhouse | 7% | 7% | 6% | 7% | 7% |

**Floor area increases:**

| Building type | Standard (m²) | Modified (m²) | % increase |
|---|---|---|---|
| Bungalow | 136 | 136 | 0% |
| Semi-detached | 121 | 130 | 7% |
| Detached | 154 | 162 | 5% |
| Townhouse | 165 | 168 | 2% |
| Apartment | 81 | 81 | 0% |

**Critical note:** The methodology doc (§15.13.3) cites this study as finding "few hundred to few thousand dollars per unit" — that paraphrase is from the Community Housing Transformation Centre, not the primary source. The per-feature costs are indeed in that range, but the aggregate per-dwelling premium is 6-12%. This is a significant mischaracterization that must be corrected.

**Evidence tier:** Tier 4 — government-commissioned analysis (CMHC). Five cities, five building types, construction-sector-validated. Methodology: RSMeans Contractor's Pricing Guide 2015 + local construction-sector verification.

### B.2 German cost premium discrepancy — RESOLVED

**TERRAGON/DStGB 2017:**
- Analyzed 148 criteria of DIN 18040-2 (basic barrierefrei, NOT R-marked wheelchair-accessible)
- 138 criteria: zero additional cost (planning decisions only)
- Full compliance: 0.35-1.26% of pure construction costs (KG 300+400)
- €21.50/m² Wohnfläche for full compliance
- ~€1,600 per 75m² apartment
- Basis: exemplary 5-storey, 20-unit apartment building in Berlin (idealized project)
- Commercial interest: TERRAGON is a developer of barrier-free housing (~2,000 units)

**bau.de 2026 "5-10%":**
- Broader scope including R-marked wheelchair provisions (DIN 18040-2 (R))
- Likely includes soft costs not in KG 300+400
- Trade-press synthesis, not commissioned study

**CMHC/Société Logique 2015/2016:**
- 60 features including elevator preparation, fire refuges, spatial reconfiguration
- 6-12% per dwelling depending on building type
- Scope comparable to German R-marked provisions

**Reconciliation:** The variance is scope-dependent, not methodology-dependent.
- Basic visitability / Silver / M4(2) / DIN 18040-2 basic: 0.4-1.3% in multi-unit new construction
- Comprehensive accessibility with full provisions: 5-12%
- Both are valid figures for different standard levels

### B.3 Australian ABCB RIS — per-dwelling cost

**Source:** Centre for International Economics (CIE) for ABCB. Decision Regulation Impact Statement, 2021-2022. Option 1 = Silver standard (NCC 2022).

- Silver (Option 1): small net cost; would break even if cost estimates overstated by ~AUD $538 per dwelling
- Gold (Option 2) and Gold+ (Option 3): costs significantly outweigh benefits under all scenarios
- Under willingness-to-pay approach: Option 1 broadly breaks even
- Adoption: VIC, QLD, TAS, ACT, NT adopted; NSW, WA, SA initially refused

**Evidence tier:** Tier 4 — government-commissioned cost-benefit analysis.

### B.4 Norwegian SINTEF — confirmed

**Source:** Christoffersen, J. & Denizou, K. (2010). "Ikke så dyrt likevel. Konsekvenser av TEK 10 for arealbruk i småboliger." SINTEF Byggforsk. Commissioned by Husbanken.

- TEK10 accessibility requirements for bathrooms neither make bathrooms disproportionately large nor significantly more expensive
- Title translates: "Not so expensive after all"
- Ryhl & Frandsen found 0.8 m² average increase for universal design features
- TEK17 extended the TEK10 requirements

**Evidence tier:** Tier 4 — government-commissioned research (Husbanken/SINTEF).

### B.5 Ielegems & Vanrie — additional output identified

ResearchGate profile shows December 2024 output: "Eindrapport_Directe kosten en baten van Integrale toegankelijkheid voor publieke gebouwen" (Final report: Direct costs and benefits of Integral accessibility for public buildings). Dutch-language. Not yet retrieved — research target.

Confirmed reference list includes prior studies by Ielegems, Herssens & Vanrie (2019), "Drivers and Barriers for Universal Designing: A Survey on Architects' Perceptions," JAPR 36(3):181-197. Forward-citation from Ielegems 2024 identified: Enhancing universal design through co-design (Archnet-IJAR Feb 2026, Australian co-design study).

### B.6 Hedonic gap confirmed

No peer-reviewed hedonic regression isolating disability-accessibility features in residential property values surfaced across any jurisdiction searched (US, UK, CA, AU, DE, NO, NL, BE). The 54-paper 2018 systematic review (Eurostat-published, Chalmers University of Technology) confirms: "accessibility" in hedonic price models refers overwhelmingly to transport/location accessibility, not building-level disability features.

This is the single largest evidence gap across all 24 project jurisdictions. Methodologically tractable — UK Land Registry Price Paid Data is free and complete; a UK-first hedonic on M4(2) vs M4(1) properties is probably the lowest-barrier commissioned study.

### B.7 Canadian institutional landscape (new data)

**CSA/ASC B652:23 — Accessible Dwellings (January 2023):**
- First National Standard of Canada for accessible dwellings
- Funded by CMHC and Accessibility Standards Canada (ASC)
- Covers design, construction, and alteration of accessible homes
- Technical requirements include 1500mm turning circles, 850mm door openings, reinforced bathroom walls
- RHFAC v4.0 (Rick Hansen Foundation) aligning with B652:23 for multi-unit residential

**CMHC Housing Design Catalogue (2025-2026):**
- Standardized accessible-ready and enhanced-accessible designs
- Aligned with ASC 2.8 (Accessible-Ready Housing) and CSA/ASC B652:23
- Class B construction cost estimates included
- Regional designs across Canada incorporating local regulations
- Supports prefab and off-site construction methods

**CMHC MLI Select — Accessibility Bucket:**
- Multi-unit mortgage loan insurance with points-based scoring
- Accessibility points: accessible units + universal design features + accessible common areas
- Benefits: reduced insurance premiums, longer amortization (up to 40 years), better DCR
- Federal CMB expansion by $20B annually supporting capacity
- Accessibility is one of three equal pillars with energy efficiency and affordability

**Accessible Canada Act (2019):**
- Mandate: barrier-free Canada by 2040
- Accessibility Standards Canada (ASC) established as standards development organization
- Three new accessibility standards published February 2023 (B651, B651.2, B652)

### B.8 Cross-jurisdictional cost-premium synthesis (revised)

| Jurisdiction | Standard | Scope | Premium (new-build) | Source | Tier |
|---|---|---|---|---|---|
| DE | DIN 18040-2 basic | 148 criteria, multi-unit | 0.35-1.26% | TERRAGON/DStGB 2017 | 4 (commercial interest flagged) |
| UK | M4(2) | Lifetime Homes equivalent | ~£1,400/dwelling (~0.4%) | Centre for Ageing Better 2020 | 4 |
| AU | NCC 2022 Silver | 7 core elements | ~AUD $538 break-even | CIE/ABCB RIS 2021 | 4 |
| BE | UD public buildings | 12 case studies, 3 types | 0.94-3.92% new-build | Ielegems & Vanrie 2024 | 1 (peer-reviewed) |
| CA | 60-feature full access | Comprehensive residential | 6-12% | CMHC/Société Logique 2015 | 4 |
| DE | DIN 18040-2 (R) full | R-marked wheelchair | 5-10% | bau.de trade-press 2026 | 5 |
| NO | TEK10/TEK17 | Bathroom UD requirements | "Not so expensive" (~0.8 m²) | SINTEF Byggforsk 2010 | 4 |
| US | ADA compliance | Public accommodation | <1% | ADA National Network 2025 | 5 |

**The critical insight:** cost premium is a function of standard scope, not jurisdiction. Basic visitability/Silver in multi-unit new construction clusters at 0.4-1.3% across jurisdictions. Comprehensive 60-feature accessibility clusters at 5-12%. The meaningful comparison is scope-to-scope, not jurisdiction-to-jurisdiction.

---

## C. Research targets — next actions

1. **[IMMEDIATE] Correct CMHC mischaracterization** in economics-research-methodology.md §15.13.3
2. **[IMMEDIATE] Add TERRAGON commercial interest flag** alongside cost figures
3. **[NEXT SESSION] Ielegems 2024 backward citation mining** — retrieve reference list, forward-cite in Scopus
4. **[NEXT SESSION] Ielegems December 2024 Dutch-language report** — retrieve full text
5. **[NEXT SESSION] Canadian provincial programmes deep dive** — Ontario AODA cost data, BC building code accessibility, Quebec Société Logique ongoing work
6. **[NEXT SESSION] CMHC Housing Design Catalogue** — extract Class B cost estimates for accessible-ready vs standard designs
7. **[NEXT SESSION] Forward-cite Sirmans 2006** in Scopus for non-US hedonic literature
8. **[DEFERRED] Commission UK hedonic study** using Land Registry Price Paid Data — lowest-barrier study to close the gap

---

## D. Research log entries (for commit)

### SL: economics-audit-cost-premium-cross-jurisdiction
- **Slug:** economics-audit-cost-premium-cross-jurisdiction
- **Date:** 2026-05-03 19:44
- **Searches:** CMHC Société Logique 2015, TERRAGON DStGB 2017, ABCB NCC 2022 RIS, SINTEF TEK10 2010, Ielegems 2024, CSA B652, hedonic regression accessibility
- **Key finding:** Cost premium is scope-dependent (0.4-1.3% basic vs 5-12% comprehensive), not jurisdiction-dependent. CMHC study was mischaracterized in methodology doc. Hedonic gap confirmed across all jurisdictions.
- **Sources verified:** CMHC Research Bulletin May 2016 (primary); DStGB press release 6 April 2017; ABCB Decision RIS 2021; SINTEF/Husbanken 2010; regjeringen.no archived report
- **GAPs identified:** Hedonic regression on disability-accessibility features absent across all jurisdictions (confirmed); Ielegems Dec 2024 Dutch report not yet retrieved; CMHC Housing Design Catalogue Class B costs not yet extracted

---

**End of interim findings. Research continuing.**


---

## E. Additional Research Findings (2026-05-03 session continued)

### E.1 Ielegems, Vanrie & Herssens (2019) — Full Report Retrieved

**Source:** Ielegems, E., Vanrie, J., & Herssens, J. (2019). "Rapport: Directe Kosten en Baten van Integrale Toegankelijkheid voor Publieke Gebouwen in Vlaanderen." UHasselt Document Server. hdl.handle.net/1942/36702

**Note:** This is the full report underlying the Ielegems & Vanrie 2024 Archnet-IJAR journal article. The report predates the journal article and contains more detailed findings. The ResearchGate "Dec 2024" date appears to be the dataset upload date, not the report date.

**Methodology:** 12 case studies, 3 typologies (secondary schools, town halls, small retail shops), Limburg province (Belgium). 119 accessibility criteria — broader than wheelchair access, includes color contrast, wayfinding, acoustics. Three scenarios per case: (1) current state, (2) renovation to 100% integral accessibility, (3) new build at 100% integral accessibility. Research-by-Design methodology. Independent contractor cost estimation based on concrete case context.

**Cost findings by typology (new build vs renovation):**

| Typology | Scale (avg cost) | Renovation additional cost | New-build additional cost |
|---|---|---|---|
| Secondary schools | >€8M | 1.44–2.34% | **0.54–0.64%** |
| Town halls | ~€950K | 8.58–17.67% | **4.24–9.16%** |
| Small retail shops | ~€55K | 20.48–26.32% | **2.09–2.70%** |

**Critical insight — scale dependency:** The relative cost of accessibility is strongly scale-dependent. Large buildings (schools) approach negligible cost at <1%. Small buildings (retail) show 2-3% for new build and 20-26% for renovation. The scale dependency explains the wide range in the journal article (0.94-3.92%).

**Building element cost distribution:**
- Cheapest elements (together ~5% of total accessibility budget): electrical controls & lighting, interior floors, color contrast, signage, fixed interior furniture
- Most expensive elements: lifts and interior stairs/ramps
- "Circulation" element: expensive to renovate but minimal additional cost if designed from start

**Benefit analysis:** 15 of 16 examined building elements contain criteria that improve comfort for everyone (not just persons with disability). Quantifying population benefit proved difficult due to lack of regional demographic data.

**Evidence tier:** Tier 1 (peer-reviewed methodology — Research-by-Design with independent contractor verification, published through university document server, later published in Archnet-IJAR)

**Significance for project:** This is the most detailed European cost study on accessible construction, using broader criteria (119 vs TERRAGON's 148 but including sensory and cognitive provisions TERRAGON excludes). Confirms that new-build accessibility at large scale is near-negligible (<1%); renovation is 5-20× more expensive; and small-scale buildings face proportionally higher costs.

### E.2 Dutch NEN 9120 / RIGO Research data

From the Dutch government document (zoek.officielebekendmakingen.nl), RIGO Research (Netherlands) found:
- Accessible toilet addition: €3,000–€5,000
- Lift over 2 stories: additional investment (figure truncated in search result)
- Cost-benefit distribution is "skewed": benefits concentrate in large buildings with many visitors at relatively low cost, while costs are proportionally high in small buildings

NEN 9120:2025 (new Dutch accessibility standard) was under development as of late 2023, expected publication early 2024. This replaces/supplements NEN 1814. [UNVERIFIED — confirm current status of NEN 9120]

### E.3 Cross-jurisdictional cost synthesis — revised with Ielegems detail

The Ielegems data refines the cross-jurisdictional picture:

**Basic visitability / Silver / M4(2) — multi-unit new construction:**
- UK M4(2): ~£1,400/dwelling (~0.4%)
- DE DIN 18040-2 basic: 0.35-1.26% (TERRAGON, commercial interest flagged)
- AU NCC 2022 Silver: ~AUD $538 break-even
- BE large public buildings: 0.54-0.64% (Ielegems)
- NO TEK10: ~0.8m² increase, "not so expensive" (SINTEF)
- US public accommodation: <1% (ADA National Network, Tier 5)

**Comprehensive accessibility — new construction:**
- CA 60-feature residential: 6-12% (CMHC/Société Logique)
- DE DIN 18040-2 R-marked: 5-10% (bau.de trade-press)
- BE small retail (119 criteria): 2.09-2.70% (Ielegems)
- BE town halls (119 criteria): 4.24-9.16% (Ielegems)

**Renovation (always dramatically more expensive):**
- BE schools: 1.44-2.34% (low because large scale)
- BE town halls: 8.58-17.67%
- BE small retail: 20.48-26.32%
- DE retrofit: €19,100/dwelling avg (KfW/Prognos)
- UK retrofit vs designed-in: ~19× ratio (Habinteg)

**The two variables that drive cost:** (1) scope of standard (basic vs comprehensive) and (2) building scale (large vs small). Jurisdiction is a distant third factor.
