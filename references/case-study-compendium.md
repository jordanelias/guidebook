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

## Progress Notes

**Session 4 (2026-03-27):**
- All 14 existing case studies entered (CS-01–CS-14)
- 4 new candidates identified (CS-15–CS-18)
- AtkinsRéalis HQ (CS-05) and Lyngby-Taarbæk School (CS-06) require targeted research in Sessions 5/6/7
- Financial fields: majority GREY for existing cases; CS-03 (Kelsey) VERIFIED; CS-14 (BC HAFI) VERIFIED; CS-09/CS-12 PROVISIONAL
- CS-16 (Summer Foundation) is the highest-tier outcome evidence in the corpus (Tier 1, PubMed-confirmed)
- CS-17 (NHS CAMHS) is the paradigm §8.5 failure case
- Sessions 7 & 8 targets: AtkinsRéalis, Lyngby-Taarbæk, PAIN/OFS cases, IntD cases, NDV/MH cases, residential mixed-needs, cross-disciplinary collaboration, failure cases with remediation costs

