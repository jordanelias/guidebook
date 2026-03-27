# Case Study Compendium
**File:** references/case-study-compendium.md
**Created:** 2026-03-27 (Session 4 — Phase 2A Operation 2)
**Status:** ACTIVE — populated progressively through Sessions 4, 7, 8
**Schema version:** v10.4

---

## Schema

Per-entry fields:
- `id` — CS-NN sequential
- `name` — Building/programme name
- `location` — City, country
- `year` — Completion or programme start
- `populations_served` — Population codes
- `design_intent` — Explicit multi-population / UD / single-pop
- `building_type` — Residential / healthcare / education / workplace / transport / mixed
- `outcome_data` — POE findings with source and tier
- `conflict_documented` — YES/NO; if yes, describe
- `failure_notes` — Failures, retrofits, complaints, litigation
- `construction_cost` — Total or per-m², currency, year; quality flag
- `accessible_design_premium` — % of project cost if isolated
- `funding_sources`
- `operational_cost_change`
- `remediation_cost`
- `roi_data`
- `financial_evidence_tier`
- `financial_data_quality` — VERIFIED / PROVISIONAL / GREY
- `evidence_contribution` — How this case study contributes to guidebook evidence base
- `part13_status` — IN (existing) / CANDIDATE / EXCLUDED
- `sources`

**Financial data quality flags:** VERIFIED = formally published peer-reviewed or audited source. PROVISIONAL = organisational report, planning application, press release with named source. GREY = undocumented estimate or unverifiable claim — include with explicit [GREY] marker.

---

## Existing Case Studies (§13.01–§13.14 in v9.0)

---

### CS-01 — Maggie's Centre Inverness

| Field | Data |
|---|---|
| id | CS-01 |
| name | Maggie's Highlands Cancer Caring Centre |
| location | Inverness, Highland, UK |
| year | 2005 |
| populations_served | NDV/MH · PAIN · OFS (cancer patients); ALL biophilic |
| design_intent | Therapeutic cancer care centre; evidence-based biophilic design |
| building_type | Healthcare (cancer support) |
| outcome_data | Network-level meta-synthesis (Liu et al. 2022, Building and Environment): biophilic design elements → "Welcoming-Relaxing" outcome dominant. Cancer patients: thermal comfort more important than standard design (chemotherapy cold sensitivity). [Tier 3] |
| conflict_documented | YES — thermal sensitivity (cancer/PAIN vs standard comfort range); resolved by user-controlled heating |
| failure_notes | None specific to Inverness; network-level: some centres receive criticism for aesthetics over function |
| construction_cost | Donation-funded; Inverness specific cost not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Charitable donations |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Biophilic/sensory design for PAIN/OFS/NDV/MH populations; thermal conflict documentation |
| part13_status | IN |
| sources | Liu et al. (2022) Building and Environment; Wikipedia (Maggie's Centres); PagePark Architects |

---

### CS-02 — Gallaudet DeafSpace Campus

| Field | Data |
|---|---|
| id | CS-02 |
| name | Gallaudet University DeafSpace Campus |
| location | Washington DC, USA |
| year | 2005 (guidelines); ongoing campus implementation |
| populations_served | DEAF (primary); MOB secondary (widened corridors, ramps) |
| design_intent | Deaf-culture-led campus design; 150+ guidelines |
| building_type | Education / campus |
| outcome_data | No standardised clinical POE. Community satisfaction documented through participatory design process. Campus described as "living laboratory" for DeafSpace principles. [Co-1] |
| conflict_documented | YES — DeafSpace rounded corners caused MOB collisions; corrected post-occupancy to glass corners. Wide corridors for signing: compatible with MOB. Ramps preferred over stairs: compatible with MOB. |
| failure_notes | SLCC (see CS-08): Bauman self-reports design concerns from using modern over organic Deaf paradigm. Rounded corners: post-occupancy correction required. |
| construction_cost | Not isolated |
| accessible_design_premium | Not isolated |
| funding_sources | University; federal government (Gallaudet is federally chartered) |
| operational_cost_change | Not documented |
| remediation_cost | Not documented (glass corner modification cost not isolated) |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Paradigm cross-population design for DEAF with self-documented failure cases; highest Co-1 evidence base for any single disability population |
| part13_status | IN |
| sources | Gallaudet DeafSpace Guidelines Vol 1 (2010); Bauman 2015 TedxGallaudet; Studio27 Architecture; NEA blog 2018; ASLA Dirt 2019 |

---

### CS-03 — The Kelsey Civic Center

| Field | Data |
|---|---|
| id | CS-03 |
| name | The Kelsey Civic Center |
| location | San Francisco, CA, USA |
| year | 2025 (April) |
| populations_served | MOB · VIS · DEAF · NEU · NDV · OFS · IntD — spectrum-wide disability-forward |
| design_intent | Explicit multi-disability affordable housing; disability-forward design |
| building_type | Residential (affordable housing, 112 units) |
| outcome_data | Too early for systematic POE (opened April 2025). Resident testimonials document independence and community belonging. Inclusion Concierge programme operational. [PROVISIONAL] |
| conflict_documented | Not formally documented; co-design process addressed multi-population tensions. Design described as "reframing access from code compliance to creativity." |
| failure_notes | None documented (too early) |
| construction_cost | $88.3M total (112 units, San Francisco 2025) [VERIFIED] |
| accessible_design_premium | Not isolated |
| funding_sources | HUD Section 811; California AHSC; SF Mayor's Office of Housing; JPMorgan Chase; Golden Gate Regional Center; Harry & Jeanette Weinberg Foundation; FHLBank SF ($1.6M AHP grant) |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | Tier 5 (official development documentation) |
| financial_data_quality | VERIFIED |
| evidence_contribution | Most ambitious contemporary cross-population disability-forward housing; produced Inclusive Design Standards (published); first SF housing lottery to preference HCBS users; national model |
| part13_status | IN |
| sources | thekelsey.org; WRNS Studio; Housing Trust Silicon Valley 2026; Urban Institute; FHLBank SF |

---

### CS-04 — DSDC Iris Murdoch Building

| Field | Data |
|---|---|
| id | CS-04 |
| name | Iris Murdoch Building, DSDC, University of Stirling |
| location | Stirling, Scotland, UK |
| year | 2006 (approx.) |
| populations_served | DEM (demonstration environment); staff (neurotypical workplace) |
| design_intent | Dual function: dementia-exemplar design + academic workplace |
| building_type | Education / workplace (academic research centre) |
| outcome_data | POE conducted internally; published Design Studies 2006. Staff concerns about open plan addressed through user involvement. Building demonstrates dementia-friendly design is compatible with workplace function. [Tier 2 — design study] |
| conflict_documented | YES — DEM wayfinding principles (colour-coded routes, orientation cues) vs open-plan academic office requirements. Resolved: dementia-friendly cues integrated without compromising open plan. |
| failure_notes | None significant; minor: garden requires annual pressure-washing due to north-facing aspect |
| construction_cost | Not documented [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | University of Stirling; charitable |
| operational_cost_change | Not documented |
| remediation_cost | Annual garden maintenance above standard (noted) |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Only published POE of a dementia-friendly workplace environment; demonstrates cross-population compatibility of DEM design with neurotypical workplace use |
| part13_status | IN |
| sources | Design Studies 2006; Scottish Forestry case study; dementia.stir.ac.uk |

---

### CS-05 — AtkinsRéalis HQ

| Field | Data |
|---|---|
| id | CS-05 |
| name | AtkinsRéalis HQ (formerly SNC-Lavalin) |
| location | [Location not confirmed in search results] |
| year | [Year not confirmed] |
| populations_served | [Not confirmed — likely ALL workplace UD] |
| design_intent | [Not confirmed] |
| building_type | Workplace |
| outcome_data | [Not found — requires targeted search in Session 7] |
| conflict_documented | [Not found] |
| failure_notes | [Not found] |
| construction_cost | [Not found] [GREY] |
| accessible_design_premium | [Not found] |
| funding_sources | Private (engineering consultancy) |
| operational_cost_change | [Not found] |
| remediation_cost | [Not found] |
| roi_data | [Not found] |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | [To be determined — Session 7] |
| part13_status | IN |
| sources | [Search required — flag for Session 7] |
| notes | RESEARCH REQUIRED — No substantive data found in Session 4 pass. AtkinsRéalis is a global engineering firm. This may be an internal accessible workplace programme rather than a published case study. Escalate to Session 7 targeted search. |

---

### CS-06 — Lyngby-Taarbæk School

| Field | Data |
|---|---|
| id | CS-06 |
| name | Lyngby-Taarbæk School |
| location | Lyngby-Taarbæk, Denmark |
| year | [Not confirmed] |
| populations_served | NDV/AUT · NDV/ADHD · ALL (inclusive school design) |
| design_intent | Inclusive school environment; neurodivergent-informed design |
| building_type | Education (K-12) |
| outcome_data | [Not found in Session 4 — requires Danish-language targeted search in Session 5/6] |
| conflict_documented | [Not found] |
| failure_notes | [Not found] |
| construction_cost | [Not found] [GREY] |
| accessible_design_premium | [Not found] |
| funding_sources | Municipal / Danish government |
| operational_cost_change | [Not found] |
| remediation_cost | [Not found] |
| roi_data | [Not found] |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | [To be determined] |
| part13_status | IN |
| sources | [Search required — flag for Session 5/6 Danish language pass] |

---

### CS-07 — Singapore HDB Universal Design Flats

| Field | Data |
|---|---|
| id | CS-07 |
| name | Singapore HDB Universal Design Programme (SkyVille @ Dawson exemplar) |
| location | Singapore |
| year | 2006 (programme); SkyVille 2016 |
| populations_served | MOB · DEM (ageing) · ALL (UD) |
| design_intent | National UD programme for public housing; SkyVille @ Dawson as flagship |
| building_type | Residential (public housing, large-scale) |
| outcome_data | BCA UD Mark Platinum 2016 for SkyVille. Programme-level: UD Mark scheme operational since 2006. No clinical POE published. [Tier 5 — award recognition] |
| conflict_documented | None documented |
| failure_notes | None documented |
| construction_cost | Not isolated from total development [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Singapore government (HDB) |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Largest-scale national UD residential programme in scope; framework evidence for Part 13 methodology note on programme-level vs building-level evidence |
| part13_status | IN |
| sources | BCA Singapore; Houzz Singapore; BCA Universal Design Index |

---

### CS-08 — Gallaudet SLCC

| Field | Data |
|---|---|
| id | CS-08 |
| name | Sorenson Language and Communication Center (SLCC), Gallaudet University |
| location | Washington DC, USA |
| year | 2008 |
| populations_served | DEAF (primary) |
| design_intent | First purpose-built DeafSpace building |
| building_type | Education (academic/communication centre) |
| outcome_data | Architect self-report (Bauman 2015): design concerns attributed to using modern paradigm over organic Deaf paradigm. Described as learning exercise that informed subsequent DeafSpace guidelines. [Co-1 — architect self-report] |
| conflict_documented | YES (design deficiency) — SLCC used modern architectural paradigm rather than organic DeafSpace principles; Bauman identified this as a design limitation post-occupancy. |
| failure_notes | Post-occupancy critique from architect: SLCC did not fully achieve DeafSpace intent due to paradigm choice. Interior reportedly not achieving full visual connectivity as designed. |
| construction_cost | Not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Gallaudet University; federal government |
| operational_cost_change | Not documented |
| remediation_cost | Not documented |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | First-ever purpose-built DeafSpace building; architect-documented failure case; demonstrates importance of paradigm fidelity in disability-led design |
| part13_status | IN |
| sources | Bauman 2015 TedxGallaudet; SmithGroup (architect); Saint Mary's University DeafSpace library guide |

---

### CS-09 — De Hogeweyk

| Field | Data |
|---|---|
| id | CS-09 |
| name | De Hogeweyk (Hogewey Dementia Village) |
| location | Weesp, Netherlands |
| year | 2009 |
| populations_served | DEM (severe; single-population) |
| design_intent | Normalised small-scale living for people with severe dementia; deinstitutionalise, transform, normalise |
| building_type | Residential (care facility; 23 apartments, 152 residents) |
| outcome_data | Cambridge International Psychogeriatrics 2020: antipsychotic medication reduced from ~50% to ~12% (2019). Residents more active vs traditional nursing homes. LIMITATION: No RCT; no standardised clinical instruments for cognition/function confirmed. [Tier 3 — systematic literature review finding] |
| conflict_documented | NO cross-population conflict (single DEM population). Freedom vs safety tension: resolved by gated open village. |
| failure_notes | Critical voices: described as "Truman Show" (deceptive environment). Addressed by Hogeweyk team. |
| construction_cost | €19.3M total (4 acres; 2009). €17.8M Dutch government, €1.5M local. ~€5,000/resident/month [PROVISIONAL] |
| accessible_design_premium | Not isolated |
| funding_sources | Dutch government (€17.8M); local organisations (€1.5M) |
| operational_cost_change | Cost per resident comparable to traditional nursing homes [PROVISIONAL] |
| remediation_cost | N/A |
| roi_data | Cost-comparable to traditional nursing homes — no premium for dementia village model [PROVISIONAL] |
| financial_evidence_tier | Tier 5 |
| financial_data_quality | PROVISIONAL |
| evidence_contribution | Strongest outcome data in dementia village corpus (medication reduction); financial model demonstrating cost parity with traditional nursing homes; spawned Village Landais (FR) and Carpe Diem (NO) |
| part13_status | IN |
| sources | Cambridge International Psychogeriatrics 2020; Wikipedia (cost data GREY→PROVISIONAL); hogeweyk.dementiavillage.com |

---

### CS-10 — DSDC Audit Programme

| Field | Data |
|---|---|
| id | CS-10 |
| name | DSDC Dementia Design Audit Programme / EADDAT Tool |
| location | UK-wide (Stirling-based) |
| year | 2008 (first audit tool); EADDAT 2022 |
| populations_served | DEM · ALL (cognitive change + ageing) |
| design_intent | Systematic dementia-friendly design assessment and certification programme |
| building_type | Programme (assessment tool, not single building) |
| outcome_data | EADDAT validated by Transport for London and Kirklees Council. Research: "dementia design can sustain independence and support quality of life." Programme-level evidence [Co-2 — OT/design clinical practice] |
| conflict_documented | NO |
| failure_notes | Iridis app (2017): digital assessment tool; addresses scale challenge |
| construction_cost | Programme (not construction) [N/A] |
| accessible_design_premium | Not applicable |
| funding_sources | Charitable sources; University of Stirling |
| operational_cost_change | Not applicable |
| remediation_cost | Not applicable |
| roi_data | Not applicable |
| financial_evidence_tier | N/A |
| financial_data_quality | N/A |
| evidence_contribution | Provides the assessment methodology reference for dementia design evaluation; EADDAT is the most widely-used dementia design audit tool in the UK |
| part13_status | IN |
| sources | dementia.stir.ac.uk; stir.ac.uk/news (EADDAT 2022); Scottish Forestry case study |

---

### CS-11 — ASPECTSS Autism School

| Field | Data |
|---|---|
| id | CS-11 |
| name | ASPECTSS Autism Charter School (Magda Mostafa / Cairo) |
| location | Cairo, Egypt |
| year | 2014 (index); POE 2018 |
| populations_served | NDV/AUT (primary; pre-K-8) |
| design_intent | Purpose-built autism-spectrum school environment |
| building_type | Education |
| outcome_data | Mostafa 2018 (Archnet-IJAR): POE using ASPECTSS Design Index. Teacher surveys, in-class behavioural observation, parent/staff focus groups. Post-occupancy assessment informed retrofit proposal. Most rigorous single-population built environment POE methodology in the corpus. [Tier 2 — design research study] |
| conflict_documented | NO specific cross-population conflict (single NDV/AUT population) |
| failure_notes | POE identified ASPECTSS compliance issues; retrofit proposal produced |
| construction_cost | Not documented [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Not documented |
| operational_cost_change | Not documented |
| remediation_cost | Retrofit proposed post-POE; cost not documented |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Provides the methodological benchmark for disability-specific built environment POE; ASPECTSS is the design framework for NDV/AUT item specifications |
| part13_status | IN |
| sources | Mostafa M (2018). Archnet-IJAR 12:308-326 |

---

### CS-12 — Village Landais Alzheimer

| Field | Data |
|---|---|
| id | CS-12 |
| name | Village Landais Alzheimer |
| location | Dax, Landes, France |
| year | 2020 (opened June) |
| populations_served | DEM (severe Alzheimer's; 120 residents; youngest resident 40 years old) |
| design_intent | Normalised dementia village; de-medicalisation; research site |
| building_type | Residential (care facility; 16 houses, 120 residents) |
| outcome_data | Longitudinal evaluation by Prof. Hélène Amieva, Bordeaux University (Inserm). Early results: "improvement not only in the brain but also in behaviour" (ITV News 2023). Behavioural changes less typical vs expected. Formal comparative study vs traditional nursing homes ongoing. Public representation survey: stigma reduction in Dax community post-opening (PMC 2022). [Tier 2 — ongoing longitudinal; PROVISIONAL] |
| conflict_documented | NO cross-population conflict (single DEM population) |
| failure_notes | None documented yet; 3-month adjustment period typical for new residents |
| construction_cost | ~€28–36M construction (varying source estimates). €7M/year operating. ~€24,000/resident/year (~€82/day; comparable to French nursing homes) [PROVISIONAL] |
| accessible_design_premium | Not isolated |
| funding_sources | €10.3M grants: French government, Région Nouvelle-Aquitaine, Landes Department Council, Grand Dax agglomération |
| operational_cost_change | Cost comparable to traditional nursing homes [PROVISIONAL] |
| remediation_cost | N/A |
| roi_data | Cost-comparable claim [PROVISIONAL] |
| financial_evidence_tier | Tier 5 (official government grant documentation) |
| financial_data_quality | PROVISIONAL |
| evidence_contribution | Active longitudinal research site; strongest prospective evaluation of dementia village model; French replication of Hogeweyk; results pending but early signals positive |
| part13_status | IN |
| sources | villagealzheimer.landes.fr; Inserm/Amieva profile; Pech et al. 2022 PMC; ITV News 2023; Open Culture 2018 |

---

### CS-13 — Carpe Diem Bærum

| Field | Data |
|---|---|
| id | CS-13 |
| name | Carpe Diem Dementia Village |
| location | Bærum (Dønski), Norway |
| year | 2020 (opened autumn) |
| populations_served | DEM (158 residents, 17 housing units; Norway's first dementia village) |
| design_intent | Garden village for dementia; "Like a Home" concept; inspired by De Hogeweyk |
| building_type | Residential (care facility; 18,000 m²) |
| outcome_data | Healthcare Building of the Year 2020 (Nohrcon). DOGA Innovation Award for Inclusive Design 2024. Co-Val case study documents co-creation process and stakeholder involvement. Clinical outcome data not published. [Tier 5 — award recognition; Co-1 co-creation documentation] |
| conflict_documented | NO specific conflict (single DEM population). COVID delayed full operational pilot. |
| failure_notes | COVID pandemic prevented full launch as planned. Village inspiring similar projects across Norwegian municipalities. |
| construction_cost | Government-funded; 18,000 m². Specific cost not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Bærum Municipality (Norwegian government) |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Nordic exemplar of dementia village design; universal design integrated throughout; DOGA award reflects inclusive design quality; co-creation process documented for replication |
| part13_status | IN |
| sources | ArchDaily; CoVal case study; Nordic Office of Architecture; DOGA; Kinnarps; EFA Magazine |

---

### CS-14 — BC HAFI Programme

| Field | Data |
|---|---|
| id | CS-14 |
| name | BC Home Adaptations for Independence (HAFI) Programme / BC RAHA |
| location | British Columbia, Canada |
| year | 2012 (HAFI); 2021 (renamed BC RAHA) |
| populations_served | MOB · OFS · PAIN · DEM (ageing in place; diverse multi-disability programme) |
| design_intent | Government home adaptation grant programme; OT-assessed residential modifications |
| building_type | Residential (individual home adaptations; programme not single building) |
| outcome_data | Programme-level data: $15M over 3 years; up to $20,000/home. OT assessment required for non-standard adaptations. No published clinical outcomes (independence, falls reduction) found. [Tier 5 — government programme documentation] |
| conflict_documented | NO (individual adaptations, not cross-population by design) |
| failure_notes | HAFI (2012–2014) → BC RAHA (2021): programme improved by removing mandatory quotes for standard adaptations and improving OT/PT access |
| construction_cost | Up to $20,000/home (government grant; max lifetime rebate) [VERIFIED] |
| accessible_design_premium | Up to $20,000 per adaptation [VERIFIED] |
| funding_sources | Canada-BC Affordable Housing Initiative (equal federal/provincial split) |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | Tier 6 |
| financial_data_quality | VERIFIED |
| evidence_contribution | Largest Canadian residential home modification programme; OT-embedded model; demonstrates grant programme design for multi-disability population; $20,000 cost benchmark for residential adaptations |
| part13_status | IN |
| sources | BC Government news releases (2012, 2021); bchousing.org; Disability Alliance BC |

---

## New Case Study Candidates (Session 4 — Phase 2A)

---

### CS-15 — Enabling Village, Singapore

| Field | Data |
|---|---|
| id | CS-15 |
| name | Enabling Village |
| location | Redhill, Singapore |
| year | 2015 |
| populations_served | MOB · VIS · DEAF · NDV/AUT · IntD · ALL (explicit cross-disability community hub) |
| design_intent | Cross-disability community space; integration of persons with disabilities into society through employment, training, and inclusive amenities |
| building_type | Mixed-use (community, education, employment, healthcare, retail) |
| outcome_data | President's Design Award — Design of the Year 2016. BCA UD Mark Platinum 2016. DFA Design for Asia Grand Award 2017. ULI Global and Asia-Pacific Award for Excellence 2022. 10 years of operational evidence (2015–2025): inclusive gym, inclusive preschool (Kindle Garden), stroke rehabilitation centre (S3), Tech Able assistive technology centre operational. [Tier 5 — award recognition; programme operation evidence] |
| conflict_documented | Critical study (Onlinelibrary Wiley 2024): inclusive turn fuels entrepreneurial city; access closed by guards at 10:30pm (limits full community integration); guide dogs: no enforceable right despite UD intent. Some conflicts between rights-based and technocratic inclusion models. |
| failure_notes | Academic critique (Wiley 2024): Village closure at 10:30pm limits authentic community integration. Rights-based disability model underrepresented vs pragmatic/employment focus. Guide dog access not legally enforceable in Singapore. |
| construction_cost | Government-funded retrofit of former school compound; 30,000 m². Cost not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Singapore Ministry of Social and Family Development; SG Enable; various partnership funding |
| operational_cost_change | Not documented |
| remediation_cost | Not documented |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Strongest cross-disability operational case study over 10 years; demonstrates both achievements and tensions of state-led cross-disability inclusion. Failure/critique evidence (closure, guide dogs) supports §8.5. |
| part13_status | CANDIDATE |
| sources | SG Enable (2025) 10th anniversary report; Development Asia case study; ASEAN Magazine 2025; Wiley critical study (2024) |

---

### CS-16 — Summer Foundation Individualised Apartments, Australia

| Field | Data |
|---|---|
| id | CS-16 |
| name | Summer Foundation Individualised Apartments Programme |
| location | Melbourne, Victoria, Australia |
| year | 2022 (study published) |
| populations_served | NEU (neurological disorder; cerebral palsy; complex needs; n=15; aged 18–65) |
| design_intent | Purpose-built individualised apartments for people with complex disability and high support needs |
| building_type | Residential (apartment; community living) |
| outcome_data | Douglas et al. 2022 (Disabil Rehabil 45(8):1370–1378. PMID 35476612. DOI 10.1080/09638288.2022.2060343): significant wellbeing improvement (p=0.031, Eta=0.29); significant community integration gains (p=0.008, Eta=0.41); trend towards improved health (p=0.077, Eta=0.21); average −2.4 support hours/person/day. Pre-move settings: group homes, residential aged care, private rentals, living with parents. n=15. [Tier 1 — peer-reviewed pre/post study; PubMed confirmed] |
| conflict_documented | NO — single population study |
| failure_notes | None documented |
| construction_cost | Not documented [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Summer Foundation Limited; La Trobe University (Living with Disability Research Centre) |
| operational_cost_change | Average −2.4 support hours/person/day = documented cost reduction [PROVISIONAL] |
| remediation_cost | N/A |
| roi_data | Support hours reduction suggests ROI; not formally calculated |
| financial_evidence_tier | Tier 1 (support hours data in peer-reviewed study) |
| financial_data_quality | PROVISIONAL (support hours data) / GREY (construction cost) |
| evidence_contribution | HIGHEST-TIER outcome evidence in the corpus. Tier 1 pre/post study with n=15, standardised measures. Documents housing design → wellbeing, community integration, support needs outcomes. [REF candidate for Part 12 economics and Part 13 evidence hierarchy discussion] |
| part13_status | CANDIDATE |
| sources | Douglas J et al. (2022). Disabil Rehabil. PMID 35476612. DOI: 10.1080/09638288.2022.2060343. Based on articles retrieved from PubMed. |

---

### CS-17 — NHS CAMHS Sensory Ward Environment Review (UK, 2022)

| Field | Data |
|---|---|
| id | CS-17 |
| name | NHS England CAMHS Inpatient Sensory Environment Review |
| location | England, UK (NHS-wide) |
| year | 2022 |
| populations_served | NDV/AUT + NDV/MH (co-occurring in NHS inpatient settings) |
| design_intent | Standard NHS inpatient mental health ward — designed for NDV/MH, not NDV/AUT |
| building_type | Healthcare (inpatient mental health) |
| outcome_data | National Development Team for Inclusion (NDTi), commissioned by NHS England Children and Young People's Mental Health Taskforce: sensory environments present "sometimes extreme challenges" for autistic young people; at best hinder wellbeing, at worst exacerbate mental health problems; instigate cycle of progression to more restrictive settings. Autistic-led review. [Tier 1 — Co-1 autistic-led; peer-reviewed Tandfonline 2022] |
| conflict_documented | YES — paradigm cross-population failure case. NDV/MH ward design (communal areas, institutional lighting, stimulus-present environments) systematically conflicts with NDV/AUT sensory needs for the same patient cohort. |
| failure_notes | SYSTEMATIC FAILURE CASE. NHS inpatient environments designed without autism sensory awareness harm autistic young people admitted for mental health reasons. No single building; represents a class of buildings. Relevant to §8.5. |
| construction_cost | N/A (existing NHS estate, retrofit cost unknown) |
| accessible_design_premium | N/A |
| funding_sources | NHS England |
| operational_cost_change | Increased restrictive practices = increased cost; not quantified |
| remediation_cost | Not documented |
| roi_data | Not documented |
| financial_evidence_tier | N/A |
| financial_data_quality | N/A |
| evidence_contribution | CRITICAL §8.5 EVIDENCE. Paradigm case for unresolvable conflict between NDV/MH and NDV/AUT design requirements in shared inpatient environments. Documents real-world harm from cross-population design failure. |
| part13_status | CANDIDATE |
| sources | Tandfonline (2022). DOI: 10.1080/13575279.2022.2126437 |

---

### CS-18 — Zallio & Clarkson IDEA Audit POE (London, 2022)

| Field | Data |
|---|---|
| id | CS-18 |
| name | IDEA Audit Tool Pilot Study (London inclusive design firm) |
| location | London, UK |
| year | 2022 |
| populations_served | ALL (cross-disability POE methodology validation) |
| design_intent | 6-month pilot of IDEA Audit Tool for assessing built environment inclusivity across disability populations |
| building_type | Workplace (London-based inclusive design firm) |
| outcome_data | Zallio & Clarkson (2022, MDPI Buildings 14(9):3018): IDEA Audit Tool validated; evidence-based decision-making process; accelerated prioritisation of design improvements. [Tier 2 — pilot study; peer-reviewed] |
| conflict_documented | NO conflict in pilot; tool designed to identify cross-population barriers |
| failure_notes | 78.1% of building industry practitioners (n=89) have limited knowledge of existing POE tools for accessibility — structural barrier to cross-population design improvement |
| construction_cost | N/A (existing building, audit tool study) |
| accessible_design_premium | N/A |
| funding_sources | University of Cambridge Engineering Department |
| operational_cost_change | N/A |
| remediation_cost | N/A |
| roi_data | N/A |
| financial_evidence_tier | N/A |
| financial_data_quality | N/A |
| evidence_contribution | Provides the POE methodology evidence for Part 13 and supports §8.2 methodology note: IDEA Audit as one of only 2 validated multi-disability POE tools (alongside EADDAT). |
| part13_status | CANDIDATE |
| sources | Zallio M & Clarkson PJ (2022). MDPI Buildings 14(9):3018. DOI: 10.3390/buildings14093018 |

---

## Legend

**Evidence tiers:** ● evidence-based ○ expert consensus ◐ mixed

**Part 13 status:**
- IN = existing case study in v9.0 §13.xx; entered with available data
- CANDIDATE = new case study from Session 4 research; not yet in Part 13; recommend for inclusion
- EXCLUDED = assessed and excluded with reason

**Financial data quality:** VERIFIED | PROVISIONAL | GREY (see schema above)

---

---

### CS-19 — Il Paese Ritrovato

| Field | Data |
|---|---|
| id | CS-19 |
| name | Il Paese Ritrovato (The Rediscovered Country) |
| location | Monza, Lombardy, Italy |
| year | 2018 (opened February) |
| populations_served | DEM (mild-to-moderate Alzheimer's and dementia; 64 residents; age 56–93) |
| design_intent | Alzheimer's village; normalised community living; non-pharmacological approach; social engagement preservation |
| building_type | Residential (care facility; 14,000m²; 2 buildings × 8 apartments × 8 residents) |
| outcome_data | Mazzola et al. (2024, J Alzheimers Dis 97(2):741-752, PMID 38143344, DOI 10.3233/JAD-230229): Comprehensive Geriatric Assessment (CGA) at T0, T6, T12, T18. n=64. Pre-pandemic: "satisfactory performance during the first 18 months." Pandemic disruption documented: +11.7% antidepressants, MMSE decline (not statistically significant), activity engagement dropped. Pre-pandemic model "confirmed as beneficial." Cognitive decline rate: −3 points/year on MMSE (expected rate for Alzheimer's). Alongside, "improvement in well-being" (geriatrics specialist Zanetti, 18 months post-opening). [Tier 2 — prospective cohort with standardised CGA instruments; PubMed-confirmed] |
| conflict_documented | NO cross-population conflict (single DEM). |
| failure_notes | COVID pandemic significantly disrupted model. +11.7% antidepressant use during pandemic. Admission criteria: mild-to-moderate dementia only; not suitable for severe dementia. Cost (~€93/day) comparable to Italian nursing homes but not universally accessible. |
| construction_cost | ~€10M construction; raised through private donations from wealthy families and organisations [PROVISIONAL] |
| accessible_design_premium | Not isolated |
| funding_sources | La Meridiana Cooperative; private donations; regional healthcare funding |
| operational_cost_change | ~€93/day comparable to traditional nursing homes [PROVISIONAL] |
| remediation_cost | Not documented |
| roi_data | Cost-comparable to traditional nursing homes; no premium for village model [PROVISIONAL] |
| financial_evidence_tier | Tier 5 (organisational/press) |
| financial_data_quality | PROVISIONAL |
| evidence_contribution | Highest-tier peer-reviewed outcome study for Italian dementia village design. CGA instruments are standardised. Pre-pandemic data demonstrates cognitive trajectory + wellbeing improvement at 18 months. Adds IT jurisdiction (non-English). Part 13 candidate. |
| part13_status | CANDIDATE |
| sources | Mazzola P et al. (2024). J Alzheimers Dis 97(2):741-752. PMID 38143344. DOI: 10.3233/JAD-230229. Based on articles retrieved from PubMed. Alzheimer Europe (2018). Worldcrunch (2020). Visualeyed. |

---

### CS-20 — Verbeek et al. Small-Scale Dementia Facilities, NL

| Field | Data |
|---|---|
| id | CS-20 |
| name | Small-Scale Dementia Living Facilities (Verbeek et al. quasi-experimental study) |
| location | Netherlands (multiple sites) |
| year | 2014 (study published) |
| populations_served | DEM (long-term care; n=259; matched on cognitive and functional status) |
| design_intent | Small-scale homelike care environments as alternative to traditional psychogeriatric wards |
| building_type | Residential (care facility; multiple small-scale facilities) |
| outcome_data | Verbeek et al. (2014, Int Psychogeriatr 26(4):657-668, PMID 24411467, DOI 10.1017/S1041610213002512): n=259 (124 small-scale, 135 controls); 3 time points (baseline, 6mo, 12mo). Findings: significantly fewer physical restraints (p<0.05), significantly fewer psychotropic drugs (p<0.05), significantly more social engagement at baseline and 6 months (p<0.05), more physically non-aggressive behavior at 12 months (p<0.05). Mixed results for other behavioural outcomes. [Tier 2 — quasi-experimental comparator study; PubMed-confirmed] |
| conflict_documented | NO |
| failure_notes | Behavioural results mixed; not all neuropsychiatric outcomes improved. Authors note "more research is needed." |
| construction_cost | Not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Research support (non-US government, NL) |
| operational_cost_change | Not documented |
| remediation_cost | N/A |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Strongest comparator study for small-scale dementia environment design (quasi-experimental, n=259, NL). Documents physical restraint and medication reduction with comparator group — more rigorous than De Hogeweyk data. Adds NL academic jurisdiction. Supports §12.x (economics: care cost implications). |
| part13_status | CANDIDATE |
| sources | Verbeek H et al. (2014). Int Psychogeriatr 26(4):657-668. PMID 24411467. DOI: 10.1017/S1041610213002512. Based on articles retrieved from PubMed. |

---

### CS-21 — Mostafa ASPECTSS Post-Intervention Study, Els Center (US, 2024)

| Field | Data |
|---|---|
| id | CS-21 |
| name | ASPECTSS Design Intervention — Els Center of Excellence, Jupiter FL |
| location | Jupiter, Florida, USA |
| year | 2024 (study published); intervention post-2018 POE |
| populations_served | NDV/AUT (K-12 charter school for autism spectrum; pre-K–21) |
| design_intent | ASPECTSS-informed retrofit of existing school environment; autism-specific sensory design |
| building_type | Education (K-12 charter school) |
| outcome_data | Mostafa M et al. (2024, Archnet-IJAR 18(2):318-339, DOI 10.1108/ARCH-11-2022-0258): Post-intervention staff surveys + classroom observations + interviews. Design interventions: colour-coded navigation, acoustic treatments in circulation spaces, transition alcoves, compartmentalisation in classrooms. Findings: improvements in "overall learning experience of students with autism." Els for Autism confirms "ASPECTSS-based designs impact on autism school environments." [Tier 2 — pre/post design study with multiple evaluation methods] |
| conflict_documented | NO |
| failure_notes | 2018 POE identified ASPECTSS compliance issues; retrofit proposed and subsequently implemented. Demonstrates iterative POE → retrofit cycle. |
| construction_cost | Not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | American University in Cairo; Els for Autism Foundation |
| operational_cost_change | Not documented |
| remediation_cost | Retrofit cost not documented |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Most recent and rigorous ASPECTSS evidence. Demonstrates full POE → retrofit → post-intervention evaluation cycle. Confirms ASPECTSS Index as valid framework for NDV/AUT built environment assessment. Adds US jurisdiction for autism-specific design. Supersedes/supplements CS-11 (earlier ASPECTSS POE). |
| part13_status | CANDIDATE |
| sources | Mostafa M et al. (2024). Archnet-IJAR 18(2):318-339. DOI: 10.1108/ARCH-11-2022-0258. Els for Autism (2024) research summary. AUC (2024). |

---



---

## Residential-Scale Case Studies (Session 4 Research Pass — 2026-03-27 22:00)

*Note: these are programme-level and research-study residential cases, not single-building institutional settings. Single-family homes, home adaptations, purpose-built accessible housing.*

---

### CS-22 — CAPABLE Programme (US, Multi-Site)

| Field | Data |
|---|---|
| id | CS-22 |
| name | CAPABLE — Community Aging in Place, Advancing Better Living for Elders |
| location | Baltimore, Maryland, USA (original); replicated across 12 US sites |
| year | 2011 (pilot); 2019 (definitive RCT); 2021 (multi-site synthesis) |
| populations_served | MOB · OFS · PAIN · ALL (low-income older adults with disability; primarily Black, female, urban) |
| design_intent | OT + nurse + handyperson interdisciplinary residential programme. Environmental modifications + clinical support to reduce disability and support independent living in own home. |
| building_type | Residential (individual existing homes; adapted in situ) |
| outcome_data | **Definitive RCT (Szanton et al. 2019, JAMA Intern Med 179(2):204-211, PMID 30615024, DOI 10.1001/jamainternmed.2018.6026):** n=300. 30% reduction in ADL disability at 5 months (RR 0.70, 95% CI 0.54-0.93, p=0.01). **Multi-site synthesis (Szanton et al. 2021, J Am Geriatr Soc, PMID 34314516):** 6 trials, 1,087 participants, 12 US sites. All six studies: improved ADL and IADL limitations, effect sizes 0.41–1.47 (moderate to very strong). Falls efficacy improved in 4/4 studies reporting it. Depression improved in 3 studies. Pain results mixed. **Medicaid dissemination study (PMID 30548594):** ADL improvement p=0.01; IADL improvement p<0.01; falls reduced 14% (p<0.01); hospitalizations reduced (p=0.03). [Tier 1 — multiple RCTs; PubMed-confirmed] |
| conflict_documented | NO — single-programme residential modification. |
| failure_notes | Shorter doses of CAPABLE (reduced visits) showed smaller effects. ADL measurement inconsistent across sites. |
| construction_cost | Per-participant cost: ~$2,825 (2019 RCT); average home modifications ~$700–$1,400 per participant. [VERIFIED — published cost data] |
| accessible_design_premium | ~$700–$1,400 per home for modifications |
| funding_sources | CMMI Center for Medicare and Medicaid Services Innovation; NCHH National Center for Healthy Housing; Medicaid waiver programmes; Johns Hopkins |
| operational_cost_change | Medicaid study: hospitalizations reduced (0.43 → 0.23/year, p=0.03) = direct cost saving |
| remediation_cost | N/A |
| roi_data | Published cost modelling: programme cost ~$2,825 produces ~$10,000–$22,000 savings to Medicare/Medicaid [PROVISIONAL — modelled estimate] |
| financial_evidence_tier | Tier 1 (published in peer-reviewed trial with cost data) |
| financial_data_quality | VERIFIED (trial cost data) / PROVISIONAL (ROI modelling) |
| evidence_contribution | Strongest residential-scale OT-delivered home modification programme with clinical outcomes. Definitive RCT + 5 replications. Directly supports Part 5 (residential application matrices), Part 12 (economics of accessible construction), and BC HAFI comparator for CS-14. MOB, PAIN, OFS populations. |
| part13_status | CANDIDATE |
| sources | Szanton SL et al. (2019). JAMA Intern Med 179(2):204-211. PMID 30615024. DOI 10.1001/jamainternmed.2018.6026. Szanton SL et al. (2021). J Am Geriatr Soc. PMID 34314516. Breysse et al. (2019). J Am Geriatr Soc. PMID 30548594. Based on articles retrieved from PubMed. |

---

### CS-23 — LSE/Habinteg Wheelchair User Homes Cost-Benefit Study (UK, 2023)

| Field | Data |
|---|---|
| id | CS-23 |
| name | Living Not Existing: The Social and Economic Value of Wheelchair User Homes |
| location | UK (national cost-benefit analysis; 17 qualitative interviews with wheelchair users) |
| year | 2023 |
| populations_served | MOB (wheelchair users — working age, older age, households with disabled children) |
| design_intent | Cost-benefit modelling of new-build wheelchair user homes (M4(3) standard) vs accessible and adaptable standard (M4(2)) |
| building_type | Residential (new build; programme analysis not single building) |
| outcome_data | LSE Housing and Communities / Habinteg (2023). CASEreport 147. Cost-benefit analysis based on published evidence. Key findings: working-age wheelchair user benefit ~£94,000 over 10 years vs ~£22,000 additional build cost = 4:1 benefit-cost ratio. Annual local authority savings: ~£4,800 (working age) to ~£9,200 (later years) per wheelchair user household. Qualitative: 17 interviews — improved independence, ADL capacity, employment, family cohesion, mental wellbeing, community engagement documented. [Tier 2 — published cost-benefit model; Co-1 interview evidence] |
| conflict_documented | NO |
| failure_notes | ~400,000 wheelchair users in UK estimated to live in unsuitable accommodation. 20,000 on waiting lists for wheelchair user homes. |
| construction_cost | M4(3) wheelchair user standard: ~£22,000 additional build cost vs M4(2) standard (2021-22 prices) [VERIFIED — from Ministry of Housing data cited in report] |
| accessible_design_premium | ~£22,000 per unit above M4(2) baseline [VERIFIED] |
| funding_sources | Habinteg Housing Association (commissioned); LSE |
| operational_cost_change | Local authority savings: £4,800–£9,200/year per household [PROVISIONAL — modelled] |
| remediation_cost | N/A (preventative cost-benefit; remediation cost of inaccessible housing documented qualitatively) |
| roi_data | 2.5–5× return on additional build cost within 10 years [PROVISIONAL — modelled from published evidence base] |
| financial_evidence_tier | Tier 2 (published cost-benefit model with named evidence sources) |
| financial_data_quality | VERIFIED (build cost) / PROVISIONAL (savings modelling) |
| evidence_contribution | Best available UK cost-benefit evidence for wheelchair accessible residential design. Provides £22,000 premium figure and £94,000 benefit figure for Part 12 economics. Co-1 qualitative evidence from 17 wheelchair users. Supports economic case for M4(3) residential standard. |
| part13_status | CANDIDATE |
| sources | Provan B, Lane L, Horne Rowan J (2023). CASEreport 147. LSE Housing and Communities / Habinteg. eprints.lse.ac.uk/121508. Habinteg (2023). Living Not Existing summary report. |

---

### CS-24 — BATH-OUT Bathing Adaptation RCT (UK, 2016–2024)

| Field | Data |
|---|---|
| id | CS-24 |
| name | BATH-OUT: Bathing Adaptations in the Homes of Older Adults |
| location | England, UK (multi-centre) |
| year | 2016 (BATH-OUT-1 feasibility); 2024 (BATH-OUT-2 RCT protocol published) |
| populations_served | MOB · OFS (older adults with bathing disability; 60+) |
| design_intent | OT-assessed provision of accessible level-access shower in existing homes (local authority DFG-delivered) vs usual care waiting list |
| building_type | Residential (existing homes; single accessible bathroom adaptation) |
| outcome_data | BATH-OUT-2 RCT protocol published (PMID 38254164, DOI 10.1186/s13063-023-07677-3, 2024). Primary outcome: SF-36 Physical Component Summary 4 weeks post-shower installation. Secondary: SF-36 Mental Component Summary, falls, health and social care resource use, QoL. BATH-OUT-1 feasibility RCT (Whitehead et al. 2018): feasibility confirmed; accessible shower provision improved bathroom safety and QoL in qualitative analysis. [Tier 1 RCT protocol — results pending full publication] |
| conflict_documented | NO |
| failure_notes | Feasibility study documented: long waiting times for DFG provision in usual care — waiting is itself a harmful outcome. |
| construction_cost | Level-access shower installation: typically £1,000–£8,000 in DFG context [PROVISIONAL — DFG data] |
| accessible_design_premium | £1,000–£8,000 for single bathroom adaptation [PROVISIONAL] |
| funding_sources | UK NIHR (National Institute for Health Research) |
| operational_cost_change | Not yet documented from full RCT |
| remediation_cost | Waiting time harm quantified as secondary objective of BATH-OUT-2 |
| roi_data | Not yet documented |
| financial_evidence_tier | Tier 5 (DFG programme data for cost reference) |
| financial_data_quality | PROVISIONAL |
| evidence_contribution | Only RCT of a specific single-room residential adaptation (bathroom/shower) with physical wellbeing as primary outcome. OT-assessed and delivered. Directly supports Part 5 (residential room matrices: bathroom) and Part 12 (economics: single adaptation cost). |
| part13_status | CANDIDATE |
| sources | Whitehead PJ et al. (2024). Trials. PMID 38254164. DOI: 10.1186/s13063-023-07677-3. Based on articles retrieved from PubMed. Whitehead P, Golding-Day M (2019). BATH-OUT-1 qualitative. Disabil Rehabil. |

---

### CS-25 — UK Disabled Facilities Grant (DFG) Programme

| Field | Data |
|---|---|
| id | CS-25 |
| name | UK Disabled Facilities Grant (DFG) / Better Care Fund Home Adaptations Programme |
| location | England, Wales, Northern Ireland, UK |
| year | 1996 (statutory origin); current budget £573M (2023/24) |
| populations_served | MOB · DEM · VIS · ALL (any disabled person in own home; OT-assessed) |
| design_intent | Statutory residential adaptation grant; OT-assessed; £30,000 maximum; mandatory if eligible |
| building_type | Residential (existing homes; all adaptation types: ramps, wet rooms, stair lifts, grab bars, widened doorways, kitchen adaptations) |
| outcome_data | Independent DFG Review (2018, UK DHSC): "robust research beginning to show adaptations improve physical and mental wellbeing and reduce fear of falling." BRE cost-benefit modelling: adaptations produce savings through delayed residential care. Age UK (2023): walk-in shower installation documented "went way beyond ability to wash easily — gave autonomy and confidence with wider implications for participation." 53% of UK households needing adaptations do not have all they need (English Housing Survey 2019-20). [Tier 5 — government programme review; Tier 2 for individual outcome studies cited within] |
| conflict_documented | NO (single-occupant adaptations; no cross-population conflict documented) |
| failure_notes | Long waiting times documented nationally; 2018 review found 53% increase in unmet need. Administration described as "clunky" by Parliamentary committee. Means test creates access barriers. Private tenants systematically disadvantaged. |
| construction_cost | £1–£30,000 per adaptation (max grant £30,000 England, £36,000 Wales); £573M national budget 2023/24 [VERIFIED — statutory] |
| accessible_design_premium | Not applicable (existing housing modification) |
| funding_sources | Better Care Fund (pooled NHS England + local authority); central government |
| operational_cost_change | DFG avoids/delays residential care: £39,520/year residential care cost vs £13,200/year home care avoided [PROVISIONAL — BRE modelling cited in review] |
| remediation_cost | N/A |
| roi_data | Home adaptations produce "strong improvements" across cost-benefit metrics (Foundations, 2015). DFG produces savings even evaluating only subset of benefit types. [PROVISIONAL — modelled] |
| financial_evidence_tier | Tier 6 (statutory programme); Tier 2 for modelled economics |
| financial_data_quality | VERIFIED (statutory budget figures) / PROVISIONAL (cost-benefit models) |
| evidence_contribution | Largest residential adaptation programme in scope. £573M/year, £30,000 max grant, OT-assessed. UK comparator for BC HAFI (CS-14, Canada). Provides DFG cost benchmarks for Part 12. Documents programme-level failure/waiting time evidence for §8.5 or Part 13 methodology note. |
| part13_status | CANDIDATE |
| sources | DHSC (2018). Independent DFG Review. Foundations / DFG Evidence library. Age UK (2023). DFG Step Change report. House of Commons Library (2024, SN03011). UK DFG Guidance (2022). |

---

### CS-26 — Petersson et al. Swedish Housing Adaptation OT Outcome Study

| Field | Data |
|---|---|
| id | CS-26 |
| name | Swedish OT Housing Adaptation Outcome Study (Petersson et al.) |
| location | Sweden (multiple municipalities) |
| year | 2008 (primary study); 2009 (follow-up) |
| populations_served | MOB · OFS (older adults and adults with functional limitations; municipal housing adaptation programme) |
| design_intent | OT-assessed and delivered housing adaptations in existing homes; compared to wait-list control |
| building_type | Residential (existing homes; OT-prescribed modifications) |
| outcome_data | Petersson, Lilja, Hammel, and Kottorp (2008, Level II): significant improvement in self-rated daily activity performance compared with wait-list control. Petersson, Kottorp, Bergström and Lilja (2009): participants who received home modifications experienced fewer difficulties performing daily activities. Swedish Housing Enabler (Iwarsson & Slaug 2001): validated OT assessment tool; inter-rater reliability confirmed across Nordic countries (Helle et al. 2010, Scandinavian Journal of OT). Slaug et al. (2025, PMC): citizen science housing study — substantial accessibility barriers confirmed in Swedish housing stock. [Tier 2 — quasi-experimental with wait-list control] |
| conflict_documented | NO |
| failure_notes | Swedish government investigation (2015) found no evidence that recommended accessibility upgrade measures had come into effect. Slaug et al. 2025: accessibility problems persist 30 years after being first documented. |
| construction_cost | Municipal programme; individual adaptation costs not isolated [GREY] |
| accessible_design_premium | Not isolated |
| funding_sources | Swedish municipalities; research grants |
| operational_cost_change | Not documented |
| remediation_cost | Not documented |
| roi_data | Not documented |
| financial_evidence_tier | GREY |
| financial_data_quality | GREY |
| evidence_contribution | Nordic jurisdiction OT housing adaptation evidence. Tier 2 with wait-list control. Introduces SE jurisdiction. Housing Enabler is a key assessment tool for residential accessibility. |
| part13_status | CANDIDATE |
| sources | Petersson I et al. (2008). OTJR. Level II. Petersson I et al. (2009). Disabil Rehabil. Iwarsson S, Slaug B (2001). Housing Enabler. Slaug B et al. (2025). SAGE Open Med. PMC article. |

## Progress Notes (Updated)

**Session 4 research pass complete (2026-03-27 21:30):**
- All 14 existing case studies entered (CS-01–CS-14)
- 7 new candidates identified and documented (CS-15–CS-21)
- Gallaudet duplicate audit: CS-02 (campus programme) and CS-08 (SLCC building) are DISTINCT — two separate v9.0 ToC entries for legitimately different things. No change required.
- Village Landais duplicate audit: CS-12 = Village Landais Alzheimer. No other Village Landais entry exists in compendium. No duplicate.
- New case study CS-19 (Il Paese Ritrovato, IT) adds first Italian jurisdiction with peer-reviewed clinical outcomes
- New case study CS-20 (Verbeek et al., NL) adds strongest comparator study for DEM small-scale environments
- New case study CS-21 (ASPECTSS 2024, US) provides most recent ASPECTSS evidence; supplements CS-11

**Evidence gaps confirmed after full pass:**
- VIS: no purpose-built or home-modified environment case study with outcome data exists globally (CONFIRMED THIN)
- PAIN/OFS: no purpose-built environment case study found (CONFIRMED NOT FOUND — PAIN/OFS new evidence category with no documented case studies)
- NEU/PCS: no building-level case study beyond Douglas et al. found
- DEAF beyond Gallaudet: no new buildings found
- DE/SE/DK/FI/JP/KR/ZH/ES/PT/IT: all produced regulatory/policy content only; Il Paese Ritrovato = only IT case study with outcomes
- Cross-population with outcomes for both populations: CONFIRMED NOT FOUND globally

**Sessions 7 & 8 remaining targets:**
- AtkinsRéalis HQ (CS-05): targeted search required
- Lyngby-Taarbæk School (CS-06): Danish-language targeted search required
- PAIN/OFS built environment cases (3 new target): likely THIN BASE, accept with disclosure
- NDV/MH built environment cases (2 new target)
- Residential mixed-needs longitudinal programmes (2-3 new target)
- Cross-disciplinary collaboration process case studies (1-2 new target)
- Failure cases with documented remediation costs (Session 8 slug)