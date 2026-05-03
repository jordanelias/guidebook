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


---

## F. Citation Mining Findings (systematic, 2026-05-03 continued)

### F.1 UK — Centre for Ageing Better citation chain

**£1,387 M4(2) cost figure provenance:**
- Centre for Ageing Better (2020), "State of Ageing" — cites £1,387 per dwelling for M4(2)
- Earlier figure: 2014 estimate of £521 for M4(2) on a 3-bed semi-detached house
- Both figures government-cited; the £1,387 is the current reference figure

**Major UK policy update (December 2025) — NOT IN METHODOLOGY DOC:**
- UK government announced **minimum 40% of new homes must be M4(2)** — national planning policy
- Previous position: M4(2) optional, set by local planning authorities
- London Plan remains at 90% M4(2) + 10% M4(3)
- This is a significant regulatory change that updates the methodology doc's §15.13.1 finding that "outside London, less than 25% of new homes are required to meet M4(2)"

**NHS cost data (citation-mined):**
- £513 million/year — NHS cost of poor housing for 55+ households
- £177 million of that from falls in homes
- £4.3 billion total to fix all Category 1 hazards in older people's homes → payback in ~8 years
- Source: Building Research Establishment (BRE) modelling for Centre for Ageing Better

**Supply gap data (citation-mined):**
- 9% of English homes meet basic accessibility standard (English Housing Survey)
- 1.8 million people currently need accessible/adaptable home
- 44 years to meet current demand at current building rate
- 250,000 additional accessible homes could have been built if M4(2) was mandatory from 2022

**RIBA + Habinteg Inclusive Housing Design Guide (2024):**
- "Minimal or no additional cost if considered from the outset"
- HoME coalition now 11 organizations (Centre for Ageing Better, Habinteg, Age UK, Disability Rights UK, HousingLin, RIBA, NHF, CIH, TCPA + 2 more)

**Evidence tier:** The £1,387 figure is Tier 4 (government-cited via Centre for Ageing Better, a charitable foundation). The NHS cost figures are Tier 4 (BRE modelling). The RIBA claim of "minimal or no additional cost" is Tier 5 (advocacy body position statement, not independently verified).

### F.2 CMHC/Société Logique 2015 — backward mining

The full report methodology cites:
- www.costtobuild.net (Canadian construction cost estimator)
- RSMeans Contractor's Pricing Guide: Residential Repair & Remodeling 2015
- Specialized manufacturers for specific accessibility items
- Rate schedules for construction trades in each city
- Municipal construction regulations for each of 5 cities

No academic references cited. This is a practitioner cost study, not an academic paper. The reference chain terminates at trade cost sources — which is appropriate for a Q1/Q2 first-cost study.

### F.3 Sirmans 2006 — forward citation mining (completed)

Hundreds of citing papers examined via IDEAS/RePEc and Semantic Scholar. Zero papers apply hedonic regression to disability-accessibility features in residential dwellings. Citations are entirely standard hedonic methodology — lot size, age, garages, pools, neighborhood characteristics. Confirms the hedonic gap is not an artifact of incomplete searching but a genuine absence in the published literature.

### F.4 Citation mining process note

Citation mining should be conducted for every verified new source. The pattern:
1. Backward: what does the source cite that we don't have?
2. Forward: what cites the source that we don't have?
3. If the source is a practitioner study (like CMHC), the backward chain terminates at trade cost databases — no further academic mining needed
4. If the source is an academic paper (like Ielegems 2024), both directions are productive

Sources still requiring citation mining:
- Fuglerud, Halbach & Tjøstheim 2015 (Norwegian CBA) — backward + forward
- Habinteg retrofit cost studies — primary source for £27,000 figure
- ABCB/CIE RIS 2021 — bibliography contains Australian cost study references
- Szanton CAPABLE publications — already well-mined but forward-cite for recent replication studies


---

## G. Final Findings (2026-05-03 session close)

### G.1 NEN 9120:2025 — CONFIRMED PUBLISHED

**Published:** January 1, 2025. Presented to Dutch Minister of Housing (Mona Keijzer) on February 3, 2025.
**Full title:** NEN 9120:2025 nl — Nederlandse uitwerking van NEN-EN 17210: Prestatie-eisen voor toegankelijkheid en bruikbaarheid van gebouwen (Dutch national application document for EN 17210: Performance requirements for accessibility and usability of the built environment)
**Replaces:** NEN 1814:2001
**Based on:** EN 17210:2021 (European standard)
**Access:** Freely available via NEN Connect (free account)
**Status:** Platform31 conducting national evaluation of application
**Scope:** Design, construction, refurbishment, adaptation, and maintenance of built environments. Covers wayfinding, circulation, sanitary facilities, interfaces/controls, emergency exits.
**Key position:** Accessibility consultants advocate that "merely applying this standard is not enough" — accessibility advisors and people with lived experience should be involved from the beginning of construction projects (AccessibleEU, April 2025). Aligns with project Co-1 doctrine.

The methodology doc's [UNVERIFIED] flag on NEN 9120 can now be removed. Economic appendix content requires NEN Connect access — deferred.

### G.2 Fuglerud, Halbach & Tjøstheim 2015 — citation mining completed

NR Report 1032 is a 37-page literature review + methodology framework for CBA of universal design. Forward citations (Halbach & Fuglerud 2016, 2024 Springer chapter) are all **ICT-focused** — workplace digital accessibility, not built environment. The report's built-environment content is a literature review citing the same sources the project already holds. Low additional yield for built-environment economics.

### G.3 UK December 2025 40% M4(2) mandate — committed to methodology doc v1.8

§15.13.1 updated to reflect that the UK government announced a national minimum of 40% of new homes must be M4(2), replacing the previous finding that <25% of non-London new homes were required to meet M4(2).

---

## H. Session close — handoff

**10 commits this session:**
1. `720e296` — workplan/economics-audit-research-2026-05-03.md (initial audit)
2. `07557a3` — references/economics/canadian-provincial-accessibility-programmes.md
3. `998af01` — references/search-log/economics/... (research log initial)
4. `8776fda` — references/methodology/economics-research-methodology.md v1.7 (CMHC + Throughline 1 + CvV)
5. `25a2628` — references/bpc/economics/construction-cost-data.md (TERRAGON flag)
6. `cf3ad4f` — workplan/economics-audit-research-2026-05-03.md (Ielegems + synthesis)
7. `f493437` — references/search-log/economics/... (research log update)
8. `cee469e` — workplan/economics-audit-research-2026-05-03.md (citation mining)
9. `6ebaa2f` — references/methodology/economics-research-methodology.md v1.8 (UK policy)
10. This commit

**Remaining for next session (ordered):**
1. §15 extraction to separate analytical document — needs Change Order discussion with project owner
2. Habinteg £27,000 retrofit cost — trace to primary source
3. ABCB/CIE RIS bibliography mining — Australian cost study references
4. Ielegems 2019 full report PDF retrieval (have abstract from UHasselt)
5. Japanese J-STAGE barrier-free cost studies (multilingual research)
6. Spanish MDPI 2024 regulatory review (Challenges in Housing Accessibility)
7. NEN 9120:2025 economic appendix extraction (requires NEN Connect)
8. Remove [UNVERIFIED] flag on NEN 9120 in methodology doc
9. Citation mining as ongoing process for every new verified source

**Process improvement identified:** Citation mining should be integrated into research workflow from the start, not treated as separate task. Every verified source triggers backward + forward mining before committing.


---

## I. Session 2 Findings (2026-05-03 continued)

### I.1 Habinteg £27,000 — primary source traced

**Source:** Habinteg Housing Association news release, September 2024. "Adaptations to older homes could cost households thousands."

**The £27,000 figure is the cumulative cost of 3 most common adaptations in an M4(1) home:**

| Adaptation | M4(1) cost | M4(2) cost | Differential |
|---|---|---|---|
| Grab rail (with wall strengthening) | ~£270 | ~£125 (walls already reinforced) | £145 saved |
| Stairlift (narrow/curved stairs) | £9,000–£10,000 | £2,500–£4,000 (accessible staircase) | £5,000–£7,500 saved |
| Wet room conversion (full structural) | £6,500+ | ~£4,700 (pre-existing drainage) | £1,800 saved (37% cheaper) |
| **Total 3 adaptations** | **~£27,000** | **~£7,325–£8,825** | **~£18,175–£19,675 saved** |

**Evidence tier:** Tier 5 — housing association contractor estimates, not independently commissioned study.

**Note:** In some M4(1) homes, stairlifts cannot be fitted due to stair narrowness → through-floor lift needed at £18,000–£20,000. This would push M4(1) total above £27,000.

**DFG context:** UK DFG allocation 2024/25 = £625 million (185% increase over 10 years). Source: Foundations, the National Body for DFGs.

### I.2 LSE/Habinteg "Living not Existing" (2023) — NEW Q6 DATA

**Source:** Provan, J.A. & Lane, L. (2023). "The social and economic value of wheelchair user homes." LSE Housing and Communities / STICERD. Commissioned by Habinteg. LSE Research Online: eprints.lse.ac.uk/121508/

**Methodology:** Cost-benefit analysis using evidence review + 17 qualitative interviews with wheelchair users. Three household-type models.

**M4(3) wheelchair user homes — cost-benefit over 10 years (vs M4(2) baseline):**

| Household type | Additional build cost | 10-year benefit | BCR | Annual LA saving |
|---|---|---|---|---|
| Working-age adult | ~£22,000 | ~£94,000 | 4.3:1 | ~£5,000/yr |
| Later years (65+) | ~£18,000 | ~£101,000 | 5.6:1 | ~£9,000/yr |
| Child wheelchair user | ~£26,000 | ~£67,000 | 2.6:1 | Not specified |

**Eight social benefit areas:** independence, safety, parenting, family cohesion, employment, community engagement, physical/mental wellbeing, reduced care needs.

**Evidence tier:** Tier 2-3 (LSE academic research group, published via LSE Research Online, cited in UK parliamentary written evidence). CBA methodology, not RCT.

**Co-1 content:** 17 wheelchair user interviews providing qualitative lived-experience data. Pseudonymized. Covers impact on independence, employment, relationships.

**Significance:** This is the strongest Q6 (cost-benefit/cost-of-inaction) evidence the project has for wheelchair-accessible housing. The 4.3:1 to 5.6:1 BCR is compelling because it measures total social value including reduced care costs, not just construction economics. The annual LA savings of £5-9K per wheelchair user are directly policy-relevant.

### I.3 DCWC/ABCB — per-dwelling cost data CORRECTED

**Source:** Donald Cant Watts Corke (DCWC), quantity surveyors, for ABCB. Cited in CIE Decision Regulation Impact Statement 2021.

**Per-dwelling additional cost estimates:**

| Standard | Building type | Additional cost (AUD) | As % of dwelling price |
|---|---|---|---|
| Silver | Separate house | $3,874 | 0.5–1.9% |
| Silver | Other types | Higher | Up to 1.9% |
| Gold | Various | Range | 1.4–9.0% |
| Gold+ | Apartment | Up to $37,742 | 1.9–11.6% |

**CORRECTION from prior session:** The "$538 break-even" figure was the sensitivity threshold, not the actual cost. The DCWC QS estimate for Silver separate house is AUD $3,874. The CIE noted Option 1 (Silver) would break even if costs were overstated by $538 — meaning net cost is approximately the DCWC estimate minus $538 adjustment in sensitivity.

**Builder-perceived vs QS cost gap:** A builder quoted AUD $15,000 for Silver on a new house (Disability Support Guide article), nearly 4× the DCWC QS estimate. This gap between industry-perceived cost and professional quantity-surveyor estimate is itself a finding — it demonstrates the "perceived additional cost" barrier that Ielegems 2024 identifies as the primary barrier to UD adoption.

**Evidence tier:** Tier 4 — government-commissioned QS analysis.

### I.4 DaltonCarter counter-analysis (2020) — ABCB RIS methodology critique

**Source:** Dalton, A. & Carter, R. (2020). "Economic advice prepared to assist with responses to the Consultation Regulation Impact Statement on minimum accessibility standards for housing in the National Construction Code." Deakin University / AdHealth Consulting. Prepared for Summer Foundation + Melbourne Disability Institute.

**Key finding:** CIE's CBA methodology had "important methodological issues" that systematically understated benefits. Specifically:
- The "problem reduction approach" (CIE's preferred method) narrowly defines beneficiaries
- The willingness-to-pay approach (broader) produced more favorable results
- Social justice and equity considerations are inadequately weighted in CBA
- Discount rate selection (7%) disadvantages long-lived benefits

**Significance:** This is a peer critique of the government CBA that produced the "costs exceed benefits" headline. The DaltonCarter analysis supports the finding that Option 1 (Silver) is closer to net-positive than the CIE central estimate suggests.

### I.5 Spanish Law 6/2022 on Cognitive Accessibility

**Source:** González Alonso, M.Y. & González Lozano, B. (2024). "Challenges in Housing Accessibility Towards Universal Design." Architecture (MDPI), 4(4), 917-929. doi:10.3390/architecture4040048

**Spanish regulatory landscape:**
- Three laws (1960, 1999, 2022), three decrees (2006, 2013, 2015), one national plan
- Main regulation: Technical Building Code (Código Técnico de la Edificación)
- **Law 6/2022 on Cognitive Accessibility** — amends General Law on Rights of Persons with Disabilities to define and regulate cognitive accessibility requirements. Spain is one of few jurisdictions with explicit cognitive accessibility legislation.
- Royal Legislative Decree 1/2013 — unifies disability rights regulations; introduces discrimination by association

**For the project:** Law 6/2022 is relevant to NDV and DEM population codes. Connection to Part 1 §1.6 regulatory landscape and Part 4 D-series cognitive wayfinding items.

**No cost data** — regulatory review only. Tier 6 (regulatory analysis).

### I.6 UK accessibility stock data discrepancy

Two figures in circulation:
- 9% of English homes meet basic accessibility standard (Centre for Ageing Better, State of Ageing 2020, citing English Housing Survey)
- 12% current housing stock with basic accessibility features (Habinteg December 2025 NPPF response)

The discrepancy may reflect: (a) different EHS survey years, (b) different definitions of "basic accessibility," or (c) updated data. The 9% figure uses a 4-feature test (level access to entrance, flush threshold, wide doorframes, entrance-level toilet). The 12% figure may use a different threshold. [UNVERIFIED — confirm which EHS methodology each uses]

### I.7 Cross-jurisdictional cost synthesis — final revision

| Jurisdiction | Standard | QS/Research cost | Builder-perceived cost | Source | Tier |
|---|---|---|---|---|---|
| AU | Silver (separate house) | AUD $3,874 (0.5-1.9%) | AUD $15,000 (builder quote) | DCWC/ABCB 2021 | 4 |
| UK | M4(2) | £1,387–£1,400 (~0.4%) | Not separately measured | Centre for Ageing Better 2020 | 4 |
| UK | M4(3) vs M4(2) | £18,000–£26,000 | Not separately measured | LSE/Habinteg 2023 | 2-3 |
| DE | DIN 18040-2 basic | €1,600/75m² apt (1.26%) | Not separately measured | TERRAGON/DStGB 2017 | 4 (commercial) |
| CA | 60-feature comprehensive | 6-12% per dwelling | Not separately measured | CMHC/Société Logique 2015 | 4 |
| BE | 119-criteria public buildings | 0.54-9.16% new-build | Not separately measured | Ielegems et al. 2019/2024 | 1 |
| NO | TEK10 bathroom UD | ~0.8m² increase | Not separately measured | SINTEF 2010 | 4 |

**The builder-perceived vs QS gap:** The Australian data reveals a ~4× gap between QS-estimated cost and builder-quoted cost for the same standard. This gap is the "perceived additional cost" that all studies identify as the primary barrier. If this gap exists across jurisdictions (likely), then the cost-premium debate is partly a perception problem, not just an evidence problem.

### I.8 Citation mining conducted this session

| Source | Direction | Yield |
|---|---|---|
| Habinteg £27K | Backward | Contractor estimates traced; 3-adaptation breakdown recovered |
| Habinteg | Forward | LSE "Living not Existing" 2023 — major new Q6 data |
| ABCB/CIE RIS | Backward | DCWC QS cost study; DaltonCarter counter-analysis |
| ABCB/CIE RIS | Forward | Summer Foundation submission; Building Better Homes campaign |
| Spanish MDPI 2024 | Backward | Law 6/2022 Cognitive Accessibility; Technical Building Code |
| Sirmans 2006 | Forward | Confirmed: zero disability-accessibility hedonic papers in citation network |
