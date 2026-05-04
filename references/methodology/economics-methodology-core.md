# Economics Research Methodology — Core Framework
<!-- Partitioned: 2026-05-03 from economics-research-methodology.md v1.9 -->
<!-- This is the methodological infrastructure file. For throughline-specific content, see companion files. -->

**Status:** v2.0 — partitioned from monolithic v1.9
**Original:** `references/methodology/economics-research-methodology.md` (archived as `economics-research-methodology-v1.9-archived.md`)
**Companion files:**
- `throughline-health-outcomes.md` — Pillar 1: health-outcomes evidence and BCR data
- `throughline-cost-of-inaction.md` — Pillar 2: retrofit penalties, housing deficit, litigation, government programmes
- `throughline-construction-cost.md` — Pillar 3: new-build premium evidence, per-technique costs
- `throughline-market-value.md` — Pillar 4: V1-V5 vendor framework, §15 perceptual-value crossover, pricing mechanisms
- `economics-gaps-and-citations.md` — Consolidated gap register and research priorities

---

## 0. Voice Register Declaration

This document operates in **procedural-imperative voice**. Constructions such as "the methodology requires X" and "the researcher should locate the original publication" describe what this research methodology requires of its user. They are not Guidebook-as-authority claims about the world. Per project RULE 2026-04-29 14:04 (A4 voice-style), Guidebook prose categorical-authority constructions are voice failures; this document is methodology guidance for researchers, not specification voice for designers, and the procedural register is appropriate to its scope.

**When research conducted under this methodology produces findings that enter the Guidebook proper** (Part 11 specifications, BPC entries, etc.), the findings must be re-voiced into tier-located form per A4 §§8.1–8.3 before publication. Specifically:
- Tier 0 findings → "Code requires [value] per [standard]"
- Tier 1 findings → "[Evidence tier] evidence supports [value]" or "Best practice based on [N] jurisdictions and [tier] evidence is [value]"
- Tier 2 findings → "OT assessment determines position within [range] based on [functional parameter]"
- Co-1 findings → Pattern Co-1-A through Co-1-D per A5 voice-style §8.3

This declaration closes the audit C.5 finding (voice creep risk).

---

---

## 1. Project Context

The Guidebook for Accessible Built Environments has a documented economics-evidence failure mode. The 2026-04-09 hallucination audit identified three fabricated quantified findings in the economics-cost-premium BPC, all of pattern *"X% across N facilities (Author Year)"*. This is the highest-risk hallucination template in this domain. RULE 2026-04-09 governs quantified-outcome verification project-wide as a result.

The methodology in this document exists to:
- Direct economic research toward source families with verifiable provenance
- Distinguish economic-question types whose conflation produces invalid claims
- Anchor cross-jurisdictional research given construction cost variation of 3–5× across the project's scope
- Position evidence per the seven-tier hierarchy (Tier 1 OT clinical research → Co-1 lived experience → Tier 6 statutory codes)
- Provide methodology guidance ahead of the C-stage build of the `economics-researcher` Hybrid skill

This document does not specify economic figures. It directs research toward sources where such figures, properly verified, can be obtained. Per Core Doctrine (RULE 2026-04-26 19:25), the Guidebook is an advocacy project, not an authority; this methodology equips researchers to ask the right economic questions, not to accept inherited answers.

---


---

## 2. Cost Question Taxonomy

Twelve economic question types organised in two families. Each has a distinct evidence base. They are not interchangeable. Most failed economics arguments confuse them.

### 2.1 Project-economics questions (Q1–Q7)

**Q1 — First-cost premium per technique.** "What does it cost to install a roll-in shower vs a standard tub-shower?" Requires line-item BoQ comparison.

**Q2 — First-cost premium per system.** "What does an accessible-compliant restroom add to per-square-metre restroom cost?" Requires assembly-level cost data.

**Q3 — First-cost premium per building.** "What % does universal design add to total project cost?" Requires whole-building cost models. Highest hallucination risk in this domain.

**Q4 — Lifecycle cost (LCC).** "Over 50 years, what is the NPV cost of accessible vs non-accessible specification?" Requires LCC modelling per ASTM E917 / ISO 15686-5 / BS 8544 / AS-NZS 4536 with maintenance, replacement, energy, end-of-life.

**Q5 — Cost-effectiveness / cost-utility.** "Cost per fall avoided, cost per QALY, cost per accommodation event." Requires clinical or epidemiological outcome data joined to cost.

**Q6 — Cost-benefit / cost-of-inaction.** "Costs avoided + benefits gained vs cost incurred." Requires external benefit valuation: healthcare offsets, litigation avoidance, productivity, exclusion-cost.

**Q7 — Distributional analysis.** "Who bears the cost, who captures the benefit, with what time lag." Requires social CBA methods. Standard answer: *different parties* — and that is the methodologically honest framing for accessibility.

### 2.2 Vendor-side questions (V1–V5)

Relevant when arguing to a developer, builder, or investor whose economic relationship to the building ends at sale or stabilises at NOI. They are rationally indifferent to lifecycle benefits and healthcare offsets. Methodology must argue on their terms.

**V1 — Hedonic price premium at sale.** Does an accessible / aging-in-place unit sell for more?

**V2 — Days-on-market / velocity.** Does it sell faster?

**V3 — Buyer pool expansion.** How many more qualified buyers can bid?

**V4 — Financing premium / eligibility.** Does the unit, or its buyers, qualify for preferential mortgage products, grants, subsidies, or tax treatments?

**V5 — Warranty / defect / litigation exposure during the responsible period.**

A serious vendor argument addresses V1 + V2 + V3 minimum. V4 and V5 are reinforcement. Q5 / Q6 (healthcare offsets, societal benefits) are not vendor arguments — naming them weakens the pitch to a vendor audience because the vendor doesn't capture those benefits.

---


**Source maps for each question type are in the throughline files:**
- Q1-Q4 first-cost sources → `throughline-construction-cost.md`
- Q5 cost-effectiveness sources → `throughline-health-outcomes.md`
- Q6 cost-benefit sources → split: healthcare downstream in `throughline-health-outcomes.md`; litigation, retrofit-later, ESG in `throughline-cost-of-inaction.md`
- Q7 distributional analysis → `throughline-cost-of-inaction.md`
- V1-V3 hedonic/DOM/buyer-pool → `throughline-market-value.md`
- V4 financing → `throughline-cost-of-inaction.md`
- V5 warranty/litigation → `throughline-cost-of-inaction.md`

---

## 3. Project-Stage Map

Cost questions are stage-specific. The AACE International cost-estimate classification (Class 1 highest precision through Class 5 lowest) provides the precision standard. RIBA Plan of Work and AIA stages harmonise to this map.

| Stage | Dominant cost questions | Required precision |
|---|---|---|
| Strategic / pre-feasibility | Q6, Q7 | Order of magnitude (Class 5) |
| Programming / brief | Q3, Q6 | Building-type benchmarks (Class 4) |
| Concept / Schematic | Q3, partial Q2 | ±20% (Class 4) |
| Design Development | Q2, Q4 | ±10–15% (Class 3) |
| Construction Documents / Tech Design | Q1, Q2 | ±5–10% (Class 2) |
| Tender / Procurement | Q1 | ±3–5% (Class 1; bid-validated) |
| Construction | Q1 (change orders) | Actual costs |
| Commissioning / RFO | Q4, Q5 (baseline) | Actuals + projection |
| Operation / POE | Q4, Q5, Q6 | Time-series actuals |
| Retrofit / Renovation | Q1–Q3 + retrofit-premium adjustment | Stage 2–6 with adjustment factors |
| End-of-life / repurpose | Q4 (residual) | Demolition + salvage values |

The methodology yields the testable claim Part 11 is positioned to make: *which class of cost question can be answered defensibly at which stage, and which require deferred analysis.* Per Core Doctrine, the Guidebook teaches the reader to ask "what cost question are we asking right now?" before reaching for a number.

---


---

## 6. Layered Search Methodology (geography-neutral)

Six search layers applied to all the source maps above.

### 6.1 Source-typed search (replaces keyword-typed search)

Reason about which type of source produces the figure required, then go to that source family. Different economic claims live in radically different source families. Keyword search blurs them, surfacing trade-association marketing figures next to peer-reviewed cost-effectiveness studies with no signal of evidence tier.

### 6.2 Citation-graph mining

The project's canonical `citation-miner` approach applied to economics seeds:
- Forward citation harvesting in Web of Science / Scopus / Dimensions from seed papers
- Backward citation mining of well-conducted systematic reviews (SR reference list is curated)
- Co-citation analysis (papers frequently cited together share methodology pedigree more reliably than papers sharing keywords)
- Author network expansion (productive economists in this niche are few across all jurisdictions; once identified, CV-tracking surfaces working papers and conference talks 12–24 months ahead of journal publication)

### 6.3 Classification-coded search

The lever that makes specialised databases precise. Equivalents across the project's source families:

- **JEL codes** (EconLit, RePEc, NBER, IZA): I10–I18 health, I31 welfare, J14 disability + employment, R21 housing demand, R31 housing markets, H51 government health expenditure, H75 social services, I38 welfare programmes
- **MeSH terms** (PubMed): Architectural Accessibility; Universal Design; Aging; Cost-Benefit Analysis; Health Care Costs
- **SSRN topic codes** + **OECD Statistics codes** + **Scopus subject area filters** (most relevant: 3306 Development; 3320 Political Science; 2904 Sociology; 2719 Health Policy)
- **CSI MasterFormat** (US/CA/MX): for cost-data publishers
- **NRM2 element / Uniclass** (UK/international): for cost-data publishers
- **DIN 276 / STLB-Bau** (Germany): for cost-data publishers
- **Omniclass** (international): for BIM-integrated cost data

Classification-coded search returns roughly 3 orders of magnitude less noise than keyword-only search.

### 6.4 Grey literature systematic search

Where most data on this topic actually lives. Without this layer the project's economics evidence base will be thin regardless of how well the journal search runs.

- World Bank eLibrary
- Asian Development Bank eLibrary
- African Development Bank publications
- Inter-American Development Bank publications
- EU JRC technical reports
- EU member-state housing/construction research institutes: UK PD&R-equivalent (DLUHC); CMHC (Canada); HUD User PD&R (US); AHURI (Australia); BBSR (Germany); BBR (Sweden); DiBK + Husbanken (Norway); BPIE (EU buildings — energy-focused, accessibility intersection only); INSEE methods and CSTB technical research (France); IPEA — Instituto de Pesquisa Econômica Aplicada (Brazil)
- OECD Working Papers (Health, Social Affairs, Urban directorates)
- IMF Working Papers (aging + long-term care fiscal projections)
- NBER / IZA / CEP / EconStor (Germany) / RIETI (Japan) / Productivity Commission (AU) / RIETM (Korea) / IDE-JETRO (Asia) working papers
- WHO regional offices — disability-related operational data
- National disability council reports: NCD (US), EDF (EU), DPI International, COTA (AU), DPO networks per jurisdiction
- State audit office reports: NAO (UK), GAO (US), ANAO (AU), OAG (Canada), Bundesrechnungshof (DE), Cour des comptes (FR), Rigsrevisionen (DK), Riksrevisjonen (NO), Riksrevisionen (SE), Algemene Rekenkamer (NL) — repeatedly evaluate accessibility programmes and produce cost data unavailable elsewhere
- POE reports (post-occupancy evaluation; particularly from healthcare estates: NHS Estates Returns UK; Australasian Health Facility Guidelines POE; Canadian Standards Association case studies; HBN-equivalent in EU)

### 6.5 Specialised databases

- EconLit (EBSCO; field-restricted JEL searching)
- NBER Working Papers (free; full-text)
- RePEc / IDEAS (free; massive aggregated archive)
- SSRN (preprints across economics, finance, law)
- EconStor (Germany; free; includes IZA, ZEW, Kiel, RWI working papers)
- HAL-SHS (France; free; humanities and social sciences open archive)
- CEEOL (Central / Eastern European economics — fills jurisdictional gap)
- AJOL (Africa) — flagged in project standards as Global South source
- J-STAGE (Japan) — flagged in project standards
- LILACS (Latin America / Caribbean)
- Scielo (Latin America / Caribbean / Iberia)
- KCI (Korea)
- AiritiLibrary (Taiwan)
- CNKI (China; partial open access; partial subscription)
- Cochrane Library + CRD York DARE/NHS EED archive + Tufts CEA Registry
- WHO IRIS institutional repository

### 6.6 Government statistical microdata (derive, don't cite)

Higher-leverage than searching for someone else's published statistic. Compute the project-fit number from public microdata.

- Each jurisdiction's national household survey microdata (per §5.3)
- Each jurisdiction's housing condition survey
- Each jurisdiction's health interview survey
- OECD-coordinated cross-jurisdictional microdata: SHARE — Survey of Health, Ageing and Retirement in Europe (28 countries); HRS-style longitudinal cohorts globally — UKHLS UK; HILDA AU; SOEP DE; KLOSA Korea; CHARLS China; LASI India; CRELES Costa Rica; SAGE WHO multi-country; HRS US; ELSA UK; ELSI Brazil
- LISS Panel (Netherlands)
- CADTH multi-jurisdictional cost-effectiveness microdata pools

For population-prevalence-weighted economic exposure calculations, microdata is the only honest route — published cross-tabs almost never align to the cell required.

### 6.7 Business and corporate-disclosure data

Underexploited on this topic across all jurisdictions.

- Securities regulators' full-text disclosure search: SEC EDGAR (US); SEDAR+ (Canada); Companies House (UK); ASX (AU); EDINET (JP); BaFin (DE); AMF (FR); CONSOB (IT); CNMV (ES); FSC (KR); FSC + SGX (SG); CVM (BR); HKEX (HK)
- Risk-factor disclosures in annual reports of public REITs, healthcare facility operators, retail operators — quantify accessibility-related capex and litigation exposure
- Bloomberg / Capital IQ / FactSet / Refinitiv (multi-jurisdictional commercial)
- PitchBook / Crunchbase / Tracxn / Crunchbase Asia (private market data)
- OpenCorporates (global corporate registry data)
- ESG disclosure databases per jurisdiction (BRSR India; CSRD-compliant filings EU)

Corporate disclosures contain economic data unavailable elsewhere, especially for retrofit capex magnitudes in built-up portfolios.

---

## 7. Validation Methodology (the critical layer)

The project's economics evidence has a documented failure mode (RULE 2026-04-09). A retrieval methodology that does not include the validation chain reproduces the failure.

For every quantified economic finding to make it into Part 11 or any specification:

1. **Original publication located** via DOI or stable URL — not citation databases, the actual source
2. **Specific number located** on specific page or in specific table of that source
3. **Methodology section cross-checked** — did the cited paper actually compute this number, or is it restating someone else's figure (in which case repeat from step 1 against the original)
4. **Six metadata fields captured:** population, sample, time period, geography, currency, base year. Without all six the figure is uninterpretable and cannot be cross-applied
5. **Two-strike rule:** if 2 independent search attempts fail to verify the specific number, the figure is CLOSED-DELETED per Standing Rule 5; do not preserve as [UNVERIFIED]

For derived/comparative claims: distinguish original calculation (document the math + source data) from cited calculation (locate their methodology); explicit currency conversion with documented base year + index source.

**Cross-jurisdiction transfer warning embedded in methodology:** construction cost varies 3–5× across the project's 24 jurisdictions. A figure derived in one jurisdiction does not transfer without local labour-cost adjustment. The methodology must enforce this — never extract a percentage figure from one jurisdiction and apply it to another without documented adjustment via a recognised cost index source (Compass International Yearbook, Arcadis ICC, Linesight Global, Turner & Townsend ICMS, or per-jurisdiction national construction cost index).

---


---

## 11. Methodological Hazards

Eight that the literature gets wrong often enough that the methodology must address them.

**11.1 Externalised benefits (Q6).** Q6 benefits accrue to insurers, governments, employers, and excluded users — not to the building owner who pays Q1/Q3 cost. Standard ROI calculations (which assume costs and benefits accrue to the same party) misrepresent this. Distributional accounting (Q7) is the methodologically honest framing.

**11.2 Threshold effects.** Accessibility is often discrete, not continuous. A doorway is either passable for a power wheelchair or not. Standard CBA assumes continuous cost-benefit functions. Real-options or threshold-CBA methods apply.

**11.3 Population uncertainty + induced demand.** Disability prevalence in a building's user population is unobservable at design stage and changes after the building exists (accessibility creates its own demand — users self-select). Static demographic projections undercount benefit.

**11.4 Time horizon and discount rate.** Benefits accrue over building life (40–100 years). Discount rate selection (3% Treasury vs 7% OMB vs 1.5% green-book social-time-preference vs HM Treasury Green Book stepped rate) changes NPV by factor of 5–10. Specify rate + justification per ASTM E917 / ISO 15686-5.

**11.5 Population heterogeneity inside a code (Core Doctrine alignment).** Per project doctrine 2026-04-24, populations are not uniform. Cost-effectiveness calculated for "wheelchair users" averages across radically different functional profiles. Q5 figures applied to specific persons require Tier-2 OT methodology, not population averages.

**11.6 Speculative demand vs realised demand.** Surveys consistently show >90% aging-in-place preference across developed-economy jurisdictions; realised aging-in-place behaviour is lower because of caregiver availability, financial capacity, and dwelling suitability. The gap between stated preference and realised behaviour is the *opportunity* for accessible-housing development — the unmet demand is real — but a vendor argument that conflates the two over-claims. Honest methodology distinguishes "stated preference" from "realised demand" and uses the gap as the argument, not the headline.

**11.7 Adverse-selection signalling.** A unit marketed as "accessible" can be perceived by some buyers as signalling old age, infirmity, or institutional aesthetic. Universal design's literature addresses this directly: the design-quality argument is that good universal design is invisible. Marketing follows: don't sell "accessibility features"; sell "a home that works at every life stage" or "future-proofed living" (Lifetime Homes UK communications research; AU Livable Housing marketing studies; Steinfeld 2012).

**11.8 Cohort vs period demand.** Demographic projections give cohort demand (boomers ageing). Period demand (current market conditions, immigration patterns, household formation) can diverge. A 2026 launch faces 2026 buyer-pool composition, not 2043's. Current period-demand argument is strong across most project jurisdictions (immigrant household formation; multi-generational households growing; aging cohort already large) but the methodology must acknowledge the distinction.

These connect to existing project rules: doctrine on population non-uniformity (RULE 2026-04-24); methodological pluralism via four-framework rule (RULE 2026-04-09); evidence hierarchy with Co-1 lived experience as co-primary (foundational); designed-in Tier 1/Tier 2 bridge for ranges (foundational).

---


---

## 13. Connection to Existing Project Artifacts

This methodology connects to:
- **GAP-079** (Part 4 + matrices GRADE ratings) — economics evidence GRADE assessment is part of the broader Part 4 evidence pipeline
- **The 2026-04-09 hallucination audit** — three fabricated economics findings caught; informed RULE 2026-04-09
- **The Village Landais 31% [STRUCK] claim** (session_2026-05-01-audit-remediation §5) — canonical example of why this methodology matters; a keyword search returned the figure through citation chains, but methodology search (locate INSERM original report → check methodology section → check effect-size table) reveals 31% is not in source
- **economics-researcher skill** — dormant; Hybrid; Sonnet 4.6; To-build at C-stage. This document is its scaffolding.
- **Part 11 The Economics of Accessible Construction** — destination for figures retrieved using this methodology
- **24-jurisdiction registry** (governance/jurisdiction-philosophy.md) — every source family in this document indexes against the 24

---

## 14. Decision Path Forward

This methodology document is DRAFT pre-canonical. To move toward canonical adoption:

1. **Project-owner review** — geographic balance, source-family completeness, voice consistency with project standards
2. **D-METH/DG-REVIEW Decision record** authored per A12 protocol, capturing rationale + scope + delegation
3. **CS8 cross-stage activation** — paired Decision record establishes methodology authority
4. **Cross-reference to project-standards.md** — if methodology becomes canonical, a RULE entry references this document
5. **Build of `economics-researcher` skill at C-stage** — validator (`economics_researcher_validate.py`) checks methodology compliance on outputs

Pre-canonical, this document serves as research methodology guidance only. Specifications derived from research using this methodology must independently meet RULE 2026-04-09 (verification) and Standing Rule 5 (two-strike).

---


---

## Changelog

**v2.0 — 2026-05-03** — Partitioned from monolithic v1.9 (1,624 lines) into six throughline-organized files. No content removed; all content redistributed with cross-references. Original archived.

**v1.0-v1.9 changelog** — See `economics-research-methodology-v1.9-archived.md` for full version history.
