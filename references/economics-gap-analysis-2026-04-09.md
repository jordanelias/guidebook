# Economics Gap Analysis — Part 11 & Case Study Compendium
**Date:** 2026-04-09 18:03
**Model:** Sonnet 4.6
**Skill:** economics-researcher
**Status:** ANALYSIS COMPLETE — pending integration

---

## 1. Missing Intervention Categories in Cost Intelligence Tables (§11.4)

Part 11's cost tables cover 8 categories. The following intervention categories have **no cost table** despite being present in the Part 4 item library:

### 1A. Kitchen/Workspace Accessibility

| Technique | Part 4 Ref | NC Premium (est.) | Retrofit ×NC (est.) | Decision Stage | Source |
|---|---|---|---|---|---|
| Adjustable-height worktop (manual) | H-01 | 0.3–0.8% | 3–6× | Technical design | DIN 18040-2; NS 11001 |
| Adjustable-height worktop (electric) | H-01 | 0.5–1.2% | 2–4× | Technical design | NS 11001; SINTEF |
| Pull-out shelving / carousel units | H-01 | 0.2–0.5% | 2–3× | Technical design | Industry standard |
| Knee clearance under sink/hob (≥700mm) | H-01 | 0% | 4–8× | Schematic | DIN 18040-2 |
| Front-operated controls on appliances | H-01 | 0% (specification) | 1–1.5× | Technical design | NS 11001 |
| Side-opening oven at worktop height | H-01 | 0.1–0.2% | 1.5–2× | Technical design | Industry standard |

**System integrity note:** Kitchen accessibility is a system. Adjustable worktop without knee clearance is non-functional for seated users. Brief as integrated package.

### 1B. Bedroom Accessibility

| Technique | Part 4 Ref | NC Premium (est.) | Retrofit ×NC (est.) | Decision Stage | Source |
|---|---|---|---|---|---|
| Bed transfer space (≥1200mm one side) | — | 0% | 5–10× | Schematic | DIN 18040-2 |
| Ceiling hoist tracking blocking | Part 10 DAR | 0% (blocking only) | 20–40× | Construction | Part 10 §10.1; Habinteg 2010 |
| Ceiling hoist installation | Part 10 DAR | 0.3–0.8% | 3–6× | Technical design | CAN/ASC 2.8:2025 |
| Window sill height ≤600mm (seated viewing) | — | 0% | N/A | Schematic | DIN 18040-2 |
| Accessible wardrobe (pull-down rails) | H-01 | 0.1–0.3% | 1.5–2.5× | Technical design | Industry standard |

### 1C. Emergency Egress

| Technique | Part 4 Ref | NC Premium (est.) | Retrofit ×NC (est.) | Decision Stage | Source |
|---|---|---|---|---|---|
| Refuge of rescue / safe haven | — | 0.2–0.5% | 8–20× | Brief | BS 9999; DIN 18040-1 |
| Evacuation lift (fire-rated) | E-01/E-02 | 1–3% | 15–30× | Brief | BS 9999 |
| Visual/tactile fire alarm routing (corridors) | B-10 | 0.1–0.3% | 2–4× | Technical design | BS 5839; DIN VDE 0833 |
| Vibrating pillow alert (bedroom) | H-04 | 0.05–0.1% | 1.5–2× | Technical design | BS 8300-2 |

### 1D. Controls and Hardware

| Technique | Part 4 Ref | NC Premium (est.) | Retrofit ×NC (est.) | Decision Stage | Source |
|---|---|---|---|---|---|
| Lever handles throughout | E-03 | 0% | 1–1.5× | Technical design | DIN 18040-2; BS 8300 |
| Rocker light switches at 900–1100mm AFF | E-05 | 0% | 0.5–1× | Construction | DIN 18040-2 |
| Power outlets at 450–1200mm AFF | — | 0% | 1–2× | Construction | DIN 18040-2; NS 11001 |
| Accessible intercom with visual display | F-06 | 0.1–0.3% | 1.5–2.5× | Technical design | DIN 18040-2 |
| Delayed-action door closers | E-04 | 0.05–0.1% per door | 1.5–2× | Technical design | BS 8300 |

### 1E. Additional Individual Techniques Missing from Existing Tables

| Technique | Should Appear In | NC Premium | Retrofit ×NC | Decision Stage |
|---|---|---|---|---|
| Handrail continuity + profile (circular 40–45mm) | §11.4.1 Circulation | 0% | 2–4× | Technical design |
| Colour-contrasted stair nosings | §11.4.4 Visual | 0–0.1% | 1–1.5× | Construction |
| Fold-down shower seat | §11.4.2 Bathroom | 0.05–0.1% | 1.5–2.5× | Technical design |
| Adjustable-height basin/vanity | §11.4.2 Bathroom | 0.2–0.5% | 3–5× | Technical design |
| Accessible balcony/terrace threshold (≤20mm) | §11.4.1 or §11.4.8 | 0% | 3–6× | Schematic |
| Colour-coded zone boundaries (floor) | §11.4.5 Cognitive | 0% | 0.5–1× | Construction |

---

## 2. Missing Financial Methodologies

### 2A. Social Return on Investment (SROI)

**Current status in Part 11:** Not mentioned.
**Evidence available:** Foundations UK has applied SROI to DFG-funded home adaptations. CAPABLE programme (CS-22) has published cost modelling showing ~$10,000–$22,000 Medicare/Medicaid savings per $2,825 programme cost. LSE/Habinteg (CS-23) models 4:1 benefit-cost ratio for wheelchair user homes.
**Recommendation:** Add to §11.3 as a named methodology. Do not attempt to produce SROI calculations — that is specialist economist territory — but name the methodology and cite the existing applications.

### 2B. Quality-Adjusted Life Year (QALY)

**Current status in Part 11:** Not mentioned.
**Evidence available:** BATH-OUT-2 RCT (CS-24) uses SF-36 which maps to QALYs via standard health economics methodology. NICE (UK) uses QALY-based cost-effectiveness analysis for health interventions; home adaptations fall within this framework.
**Recommendation:** Note as available methodology in §11.3 or §11.10. Flag that QALY analysis of home adaptations is feasible but not yet published at scale.

### 2C. Avoided Institutional Care Cost

**Current status in Part 11:** Mentioned briefly (§11.3.2 lifecycle value; §11.8.1 Arg 4 dementia design case) but not quantified systematically.
**Evidence available:**
- De Hogeweyk (CS-09): cost per resident comparable to traditional nursing homes (~€5,000/month)
- Village Landais (CS-12): ~€82/day comparable to French nursing homes
- Il Paese Ritrovato (CS-19): ~€93/day comparable to Italian nursing homes
- CAPABLE (CS-22): hospitalisations reduced 0.43→0.23/year (p=0.03)
- LSE/Habinteg (CS-23): local authority savings £4,800–£9,200/year per wheelchair user household
- UK DFG review: residential care cost £39,520/year vs home care £13,200/year
**Recommendation:** Consolidate these figures into a new §11.3.5 or expand §11.3.2 with a dedicated avoided-care-cost table.

### 2D. Employment Participation Benefit

**Current status in Part 11:** Mentioned in §11.3.4 but not quantified.
**Evidence available:** OECD disability employment gap data across member countries. Disability employment rate typically 20–30 percentage points below general population.
**Recommendation:** Flag as important but unquantified in current evidence base. Note that accessible workplaces enable employment participation, but no study has isolated the economic return of specific built environment provisions on employment outcomes. [GAP]

### 2E. Tax Incentive Economic Value

**Current status in Part 11:** §11.8.1 Arg 6 mentions grant programmes but not tax incentives.
**Evidence available:**
- US ADA tax credits: Section 44 Disabled Access Credit (up to $5,000/year for small businesses); Section 190 Tax Deduction (up to $15,000/year)
- Australia NDIS SDA: funding $35K–$117K/year per participant (not a tax incentive but a direct subsidy)
- Canada HATC: Home Accessibility Tax Credit (15% of up to $20,000 in eligible expenses = max $3,000 credit)
- Germany: KfW 455-B grants (10–12.5% of costs, max €6,250); KfW 159 loans
**Recommendation:** Add a brief table of jurisdiction-specific financial incentives to §11.8.3. Flag all figures `[VERIFY ANNUALLY]`.

---

## 3. NFP/Foundation/Government Body Budget Register

### 3A. Government Programmes with Published Budgets

| Programme | Jurisdiction | Annual Budget | Type | Population | Key Figures | Data Quality | Source Date |
|---|---|---|---|---|---|---|---|
| UK Disabled Facilities Grant | UK (England) | £761M (2025-26); £723M (2026-27) | Capital grant — home adaptations | MOB/DEM/VIS/ALL | Max £30,000/application; ~60,000 adaptations/year; new formula from 2026-27 | VERIFIED | Feb 2026 |
| KfW 455-B + 159 | Germany | €50M grants (2026, restarted 8 Apr 2026); loans via 159 ongoing | Grant + loan — barrier reduction | ALL (existing housing) | 10–12.5% of costs (max €6,250 grant); up to €50,000 förderfähig; IWU: 2M+ dwellings needed by 2035 | VERIFIED | Apr 2026 |
| NDIS SDA | Australia | ~A$600M (FY25; ~1.2% of $46.2B NDIS total) | Annual participant housing funding | MOB/NEU/NDV/IntD (extreme functional impairment) | $35K–$117K/year per participant; ~25,500 participants; 4 design categories; ~$14B capital needed for 5,000 new dwellings by 2033; projected to triple by 2033 | VERIFIED | Mar 2026 |
| US HUD Section 811 | USA | $287M (FY2026 enacted) | Project-based rental assistance + capital advances | All disability (housing) | $30M increase from FY2025; Congress rejected block grant proposal | VERIFIED | Jan 2026 |
| Norwegian Husbanken adaptation grants | Norway | NOK 89M (2026 budget) for home adaptations | Grant — home adaptations for elderly | MOB/DEM (ageing) | 25% of costs, max NOK 75,000/household; plus low-interest loans | VERIFIED | Oct 2025 |
| Norwegian nursing home investment | Norway | NOK 3,365M (2026 commitment framework) | Investment grants — nursing home places | DEM/ALL | ~1,500 places | VERIFIED | Oct 2025 |
| CMHC / Build Canada Homes | Canada | $7.3B (2025-2031); $70B National Housing Strategy (10-year) | Loans, grants, contributions | ALL (affordable housing with accessibility embedded) | AHIF, RCFI active; BC RAHA: 2,089 adaptations completed; Budget 2025 proposes $2.4B reduction | VERIFIED | Dec 2025 |
| Canada HATC | Canada | Tax credit (not appropriation) | Tax credit — home accessibility | ALL | 15% of up to $20,000 eligible expenses (max $3,000 credit) | VERIFIED | Current |
| US ADA Tax Credits | USA | Tax credit (not appropriation) | Tax credits — business accessibility | ALL | Section 44: up to $5,000/year (small business); Section 190: up to $15,000/year deduction | VERIFIED | Current |

### 3B. Foundations and NFPs with Published Budgets/Grant Maxima

| Organisation | Jurisdiction | Annual Budget/Grant Scale | Type | Built Environment Focus | Key Figures | Data Quality |
|---|---|---|---|---|---|---|
| Rick Hansen Foundation | Canada | $11.7M programme spend (F2024) | Charity — accessibility certification, education, research | RHFAC building certification; "Quality in Built Environment" research (70 researchers, 14 universities) | 57% to accessibility; $400K to 8 BC municipalities for 24 buildings; 147 sites rated F2024 | VERIFIED (Charity Intelligence) |
| Fundación ONCE | Spain | 3% of ONCE lottery gross receipts (~€100M+ estimated total; ~1/3 to accessibility) | Foundation — disability inclusion | Universal accessibility in built environment; housing, transport, public spaces | Housing grants up to €200K (90% subsidy) or €300K (50% subsidy); wheelchair space supplement €20K each | VERIFIED (foundation website) |
| Aktion Mensch | Germany | Largest private disability funder in Germany (lottery-funded) | Foundation — inclusion projects | Barrier-free housing construction and conversion | Housing grants: up to €200K (90%, 2-8 persons) or €300K (50%); digital accessibility micro-grants up to €5K (100%) | VERIFIED (grant guidelines) |
| Foundations UK | UK | Government-funded body administering DFG support | National body — DFG and Home Improvement Agencies | DFG delivery support; policy research | Administers guidance for £761M DFG programme; publishes allocations data | VERIFIED |
| Habinteg | UK | Housing association + research | Housing association — wheelchair accessible housing | M4(3) wheelchair user homes; cost-benefit research | LSE/Habinteg CASEreport 147: £22K premium, 4:1 BCR, £94K benefit over 10 years | VERIFIED (published report) |
| Summer Foundation | Australia | Research + housing innovation | Foundation — disability housing | Individualised accessible apartments for complex disability | CS-16: Tier 1 evidence; −2.4 support hours/person/day documented | VERIFIED (peer-reviewed) |
| DOGA | Norway | Government-funded design agency | National design body | Inclusive design awards; co-creation methodology | DOGA Innovation Award for Inclusive Design (Carpe Diem CS-13 recipient 2024) | VERIFIED |
| Centre for Excellence in Universal Design | Ireland | Government-funded (NDA) | National UD centre | Built environment, ICT, products | Publishes UD guidance; Building for Everyone guidance series | VERIFIED |
| AccessibleEU | EU | EU-funded resource centre | EU accessibility centre | Built environment, digital, products | European Accessibility Act implementation support (entered force 28 Jun 2025) | VERIFIED |

### 3C. Programmes Not Yet in Part 11 Evidence Base

The following programmes represent new evidence sources that should be added to Part 11:

1. **NDIS SDA (Australia)** — Most comprehensive government-backed accessible housing investment programme globally. Four design categories (Improved Liveability, Fully Accessible, Robust, High Physical Support) directly parallel guidebook taxonomy. Published pricing $35K–$117K/year. Should be added to §11.8.3.

2. **Aktion Mensch housing grants (Germany)** — Published grant maxima for barrier-free housing construction/conversion provide German-jurisdiction cost benchmarks for §11.8.3.

3. **Norwegian Husbanken adaptation grants** — Published grant maxima (25%, max NOK 75,000) provide Norwegian-jurisdiction benchmark.

4. **AccessibleEU / European Accessibility Act** — Entered force 28 Jun 2025. Regulatory context for §11.8.3 EU jurisdictions.

---

## 4. Corrections Required to Existing Part 11 Content

### 4A. KfW Programme Status

**Current text (§11.8.3):** "KfW 455-B grant programme suspended January 2025 (oversubscribed); KfW 159 loan programme continues at reduced rate."

**Required update:** KfW 455-B restarted 8 April 2026 with €50M budget (down from €150M in 2024; ZVSHK requested €150M minimum). Conditions unchanged: 10% individual measures (max €2,500), 12.5% Altersgerechtes Haus standard (max €6,250). Budget expected to be exhausted within months. IWU study: 2M+ barrier-free dwellings needed by 2035.

### 4B. UK DFG Budget

**Current text (CS-25):** "£573M national budget 2023/24"
**Current Part 11 §11.8.1 Arg 6:** "UK DFG (£711m/year)"

**Required update:** 2025-26 total is £761M (including £50M in-year uplift announced Jan 2026). 2026-27 confirmed at £723M with new allocations formula. Max grant remains £30,000 but under review.

### 4C. Oslo Economics Entry (GAP-064)

Part 11 scaffold notes: "§11.6 Evidence Landscape: add Oslo Economics (2018) entry (GAP-064)."

The Oslo Economics (2018) Report 2018-36 entry already appears in §11.6.1 strong evidence table:
> "Universal design in schools — positive BCR (NOK 2.2 billion benefit) | Cost-benefit analysis of universally designed Norwegian primary school. Strongly positive benefit-cost ratio. | Oslo Economics (2018) Report 2018-36 [Norwegian]"

This appears to have been added but the scaffold comment not removed. Verify and remove scaffold comment.

---

## 5. Gap Register Items

### New gaps identified:

| ID | Priority | Topic | Detail |
|---|---|---|---|
| GAP-ECON-01 | P2 | Kitchen accessibility cost data | No published cost study isolates kitchen accessibility premium. §11.4 needs kitchen table. Estimate from DIN 18040-2 compliance data. |
| GAP-ECON-02 | P2 | Bedroom accessibility cost data | Ceiling hoist blocking cost in Part 10 but not cross-referenced in Part 11. Need integrated bedroom cost table. |
| GAP-ECON-03 | P2 | Emergency egress cost data | Refuge of rescue, evacuation lift costs not in Part 11. BS 9999 provides design requirements but not cost data. |
| GAP-ECON-04 | P3 | Employment participation economic benefit | No study isolates economic return of specific built environment provisions on employment outcomes. Flag in §11.10.2. |
| GAP-ECON-05 | P2 | SROI/QALY methodology section | Part 11 does not name these methodologies. Add to §11.3 with existing case study evidence. |
| GAP-ECON-06 | P1 | KfW budget correction | Programme restarted Apr 2026. Part 11 text requires update. |
| GAP-ECON-07 | P1 | UK DFG budget correction | £761M actual (2025-26) vs £573M cited in CS-25. |
| GAP-ECON-08 | P2 | NDIS SDA as new evidence source | Most comprehensive government-backed accessible housing programme. Not cited anywhere in guidebook. |
| GAP-ECON-09 | P3 | New-build non-dementia residential cost isolation | No case study provides isolated accessible design premium for this building type. Confirmed gap. |

---

## 6. Connection Candidates

| CON-ID | Type | Primary Target | Detail | Confidence |
|---|---|---|---|---|
| NEW | CROSS-REF | Part 10 §10.1 → Part 11 §11.4 | Ceiling hoist blocking cost data appears in Part 10 DAR table but not in Part 11 cost intelligence tables. Cross-reference needed. | HIGH |
| NEW | CROSS-REF | Part 11 §11.8.3 → CS-25 | UK DFG budget figures differ between Part 11 (£711M) and CS-25 (£573M). Reconcile to £761M (2025-26 actual). | HIGH |
| NEW | NEW-EVIDENCE | Part 11 §11.6.1 + §11.8.3 | NDIS SDA (Australia): ~A$600M/year, 4 design categories, $35K-$117K/year per participant. Strongest government-backed accessible housing programme globally. | HIGH |
| NEW | NEW-EVIDENCE | Part 11 §11.8.3 (Germany) | Aktion Mensch barrier-free housing grants: up to €200K (90%) or €300K (50%). Supplements KfW data for German jurisdiction. | MODERATE |
| NEW | NEW-EVIDENCE | Part 11 §11.8.3 (Norway) | Husbanken adaptation grants: 25% of costs, max NOK 75,000/household (2026). Supplements existing Norwegian evidence. | MODERATE |
