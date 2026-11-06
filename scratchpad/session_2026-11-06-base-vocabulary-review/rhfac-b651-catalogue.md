# Catalogue: RHFAC Rating Survey v4.0 and the CSA/ASC B651 listing, as a basis for the base register

Session `session_2026-11-06-base-vocabulary-review`. **A lead catalogue, not evidence and not a specification.** Nothing here is admitted, no database row is written, and every figure below is computed by `scratchpad/session_2026-11-06-base-vocabulary-review/tools/doc.py` from the persisted survey text (re-run, do not trust the prose). Governing statements: the three 2026-11-06 owner entries in `references/project-standards.md` (the third is this task's).

## 0. How to read this

- **Guideline in approach, not exacting.** The RHFAC survey is a Canadian rating instrument: it lists criteria and weights them by points. It states **no dimension, force, slope or time**. Those live in the codes it rates against (CSA/ASC B651, the National Building Code of Canada and provincial codes), so this catalogue yields concepts and techniques to search for, never values to adopt. A criterion's point weight is RHF's weighting, not a finding about importance for disabled people.
- **English first is preparation, not the register.** The text below is Canadian English from one jurisdiction (CA), one programme and one author. It is the search plan for the other 13 languages of P1+P2+P3 and a seed for the reverse path: concepts that English does not name are added from native-language readings, by the instrument's own phrase (owner E1).
- **Two category axes, one table.** Every criterion carries technique tags and sits in a section that is a room, element or building typology. Both views in section 3 are generated from `rhfac-criteria.tsv`; neither is kept by hand. The technique tags are rule-assigned from the criterion's own words (regexes in `tools/build.py`): a lead for review, with multiple tags allowed because categories overlap by design.

## 1. Sources and what was and was not read

| Source | Retrieved | Read | Not read |
|---|---|---|---|
| RHFAC Rating Survey v4.0 (September 2024), `rickhansen.com/sites/default/files/downloads/2024-10/rhfacratingsurveyv40sept20244r.pdf`, 66 pages, sha256 `94f80b1b6677…` | `retrieval-log/session_2026-11-06-base-vocabulary-review/94f80b1b66776c72.pdf` | In full, as text (`pdftotext -layout`): every criterion title and point weight; the prerequisites; the certification levels. | Page images, if any carry content the text layer lacks. The survey names no figures, so the loss is judged small, **[UNVERIFIED]**. |
| CSA/ASC B651:23 (January 2023, revised June 2025), 283 pages, supplied by the owner as a Google Drive file `1_mvami5rXIBzyBNOZ7fR-blAp42GAUb8`, sha256 `4fae63595a10…`; the first two attempts returned Google's sign-in page, the retry after the owner changed the sharing returned the PDF | `4fae63595a101516.pdf` (**in the retrieval log's manifest only; the file is excluded from git**, section 2.4) | **By headers only:** table of contents, defined-term names, clause 1.6, headings and opening lines of 4.7, headings of Annexes A to F (section 2.4). | **The body clauses and every figure, table and value. [SKIPPED: B651:23 body text — by instruction (read by headers); not read.]** The publisher's own direct URL (`csagroup.org/wp-content/uploads/2430328-1.pdf`) returned a Cloudflare 403 and has no Wayback snapshot; no block-evasion was attempted. |
| ASC database listing for CSA/ASC B651, `accessible.canada.ca/…/csa-asc-b651-accessible-design-built-environment`, sha256 `b0ca9f638851…` | `b0ca9f6388515ded.html` | The listing page: a scope paragraph and five change headings. | Nothing further; it is a summary page. |
| CSA Group store page for CSA/ASC B651:23, `csagroup.org/store/product/csa-asc%20b651%3a23/`, sha256 `a038f0903154…` | `a038f09031540a36.html` | Edition history (1990, 1995, 2004, 2012, 2018 withdrawn; 2023 current), languages (English, French), and a nine-item list of changes in the 2023 edition (anthropometric dimensions, interpretation notes, luminance contrast, tactile direction indicator positioning, functional and cognitive barriers, power-assisted door controls, platform-lift minimum size, water-bottle filling stations, water-fountain controls). | The standard. |

The French RHFAC survey and guide and the French ASC page were retrieved before the owner said they are not needed here; they are in the retrieval log and nothing is drawn from them.

**Parse integrity (computed):** 640 criteria across 74 sections in 12 chapters; 70 stated section totals read, 70 sections with criteria summed (chapter 12 scored differently); mismatches (section, sum of the criterion points, the total the survey states): [('8.12', 17, 19), ('8.13', 22, 24)]. A mismatch is the SURVEY's own arithmetic, kept as printed: the criteria were re-read against the text and none was dropped.

## 2. The register this seeds

The base holds 94 terms and 10 active parameters (`select count(*) from terms`; `… from base_parameters where status='active'`). The 640 criteria collapse to 430 distinct normalised statements, of which 32 recur in three or more sections. Those recurring statements are the technique concepts that every typology shares; the long tail is typology-specific. Rows for the register are written only after the tooling PR merges (CLAUDE.md rule 10).

### 2.1 Concepts recurring in three or more sections (the shared technique vocabulary)

| Sections | Statement as the survey words it (first occurrence) | Held in the base today (term, EN name or alias) |
|---|---|---|
| 37 | Well-illuminated (if site expected to be lit) | none |
| 12 | Surface is firm, stable and slip resistant | none |
| 10 | Seating | TERM-052 rest point seating |
| 10 | Handrails | TERM-069 haptic affordance |
| 10 | Clear width | TERM-002 corridor width, TERM-021 door width, TERM-048 circulation route |
| 9 | Accessible path of travel | not checked |
| 6 | Drainage | none |
| 6 | Clear signage | TERM-019 pictogram signage |
| 6 | Audio accessibility and communication enhancement technologies | not checked |
| 5 | Level landings with clear space | not checked |
| 5 | Floor surface is stable, firm, and non-slip | not checked |
| 5 | Clear space for approach | not checked |
| 4 | Well illuminated (if required for expected usage) | not checked |
| 4 | Surface is stable, firm, and slip resistant | not checked |
| 4 | Shelter | none |
| 4 | Riser height and tread depth | none |
| 4 | Nosing design | none |
| 4 | No open riser | not checked |
| 4 | Level threshold | TERM-022 level threshold |
| 4 | Height clearance (if sheltered or parkade) | TERM-061 headroom clearance |
| 4 | Edge protection | none |
| 4 | Colour-contrasted and slip-resistant strip on nosing | not checked |
| 3 | Tactile attention indicators (truncated domes) | TERM-010 tactile walking surface indicator, TERM-026 vibrotactile alert, TERM-069 haptic affordance |
| 3 | Slope | TERM-001 ramp gradient |
| 3 | Sink faucet is easy to use or automatic | not checked |
| 3 | Outlets and switches are at accessible heights | none |
| 3 | Microwave mounting height accessible and safe | not checked |
| 3 | Level landings with clear space and at regular intervals | not checked |
| 3 | Colour-contrasted and slip-resistant strip | not checked |
| 3 | Accessible lockers | not checked |
| 3 | Accessible door hardware | none |
| 3 | Accessible controls | TERM-057 tremor and involuntary movement |

'Held' is a case-insensitive substring match on the head word in English names and English aliases only; "none" means no English hit, not that no concept exists. A held term can be narrower or wider than the survey's criterion.

### 2.2 Criteria that name something measurable (quantity-bearing words)

The survey gives no values, but its words name the quantities a code would set. Word → number of sections whose criteria use it (regex `QB` in `tools/doc.py`; a lead for the open pass, not a parameter list).

| Word | Sections |
|---|---|
| height | 26 |
| level | 21 |
| width | 21 |
| clearance | 10 |
| number | 10 |
| slope | 5 |
| depth | 4 |
| riser | 4 |
| tread | 4 |
| force | 3 |
| time | 3 |
| gradient | 2 |
| size | 2 |
| volume | 2 |
| capacity | 1 |
| distance | 1 |
| lighting levels | 1 |
| ratio | 1 |

### 2.4 CSA/ASC B651:23, digested by headers

**Read by headers only** (owner instruction): the table of contents, the 58 defined-term names of clause 3.1, clause 1.6 (the shall/should/may convention), the three headings and opening lines of 4.7 (functional and cognitive barriers; environmental intolerances; acoustics), and the headings of Annexes A to F. The standard's body clauses were not read, so **no dimension, force, slope or time is recorded here** and none should be inferred. Full heading list with pages: `b651-headings.tsv` (232 headings, generated by `tools/b651.py`).

**Document facts (title page and revision block):** CSA/ASC B651:23, National Standard of Canada, 'Accessible design for the built environment', January 2023, REVISED JUNE 2025 (errata to clause 5.2.2, Tables 8 a) to d) and Figures 20 a) to d); earlier errata of July 2023 to clauses 1.4, 5.5.1, 6.8.2, 9.4.1 and A.10); 283 pages; English and French editions exist; developed under Accessibility Standards Canada with a technical committee that includes persons with disabilities; the document says it focuses on national and international best practice 'as opposed to focusing on minimum technical requirements'; clause 1.6 separates requirement, recommendation and option by 'shall', 'should' and 'may', and Annexes A to F are informative.

**Legal notice:** the PDF's notice allows loading for review, search, browse and print, and says users may not 'make an electronic copy of this document'. The retrieval log's rule that every source be persisted (R10) conflicts with that for this one file. **The PDF is therefore not committed**: it is excluded locally (`.git/info/exclude`) and only its retrieval line, sha256 and this heading-level digest are kept. Whether the project may hold the PDF in the repository is a licensing question for the owner (DG-NON).

### B651 clause families (heading counts, computed)

| Clause family | Headings |
|---|---|
| general requirements (technique clauses) | 33 |
| interior circulation | 47 |
| interior facilities | 43 |
| residential accommodation | 3 |
| exterior circulation, spaces and amenities | 57 |
| vehicular access | 13 |
| annex A anthropometrics | 14 |
| annex B slip potential | 1 |
| annex C residential references | 1 |
| annex D trails and beach access | 15 |
| annex E outdoor recreation references | 4 |
| annex F other resources | 1 |

### B651 headings the RHFAC survey does not name (crude word-stem test; a lead for the register, not a judgement)

| Clause | Heading | Family | Technique tags |
|---|---|---|---|
| 4.4.4 | Gratings | general requirements (technique clauses) |  |
| 4.5 | Headroom and protruding objects | general requirements (technique clauses) | tactile_and_detectable |
| 4.5.1 | Headroom | general requirements (technique clauses) |  |
| 4.5.2 | Protruding objects | general requirements (technique clauses) | tactile_and_detectable |
| 6.1.2 | Spouts | interior facilities |  |
| 6.2.3 | Lavatories | interior facilities |  |
| 6.5.3 | Enclosures | interior facilities |  |
| 8.3.8 | Speed bumps | exterior circulation, spaces and amenities |  |
| 8.3.9 | Bollards | exterior circulation, spaces and amenities |  |
| 8.7 | Landscaping elements | exterior circulation, spaces and amenities |  |
| 8.7.1 | Flower or shrub planters | exterior circulation, spaces and amenities |  |
| 8.7.3 | Vegetation | exterior circulation, spaces and amenities |  |
| 8.7.4 | Guy wires | exterior circulation, spaces and amenities |  |
| 8.8.2 | Scaffolding | exterior circulation, spaces and amenities |  |
| D.6.1 | Gradation limits | annex D trails and beach access |  |

### B651 defined terms (names as the standard writes them; Canadian English)

Accessible, Accessible route, Adaptable seating, Amenity, Amenity zone, Braille, Cane-detectable, Change bench, Crosswalk, Dwelling, Glare, Gutter, Illumination, Intersection, Lavatory, Light reflectance value, Luminance, Luminance (colour) contrast, Michelson contrast, Passenger pick-up area, Pedestrian area, Pedestrian clearance interval, Pedestrian crossing, Pedestrian right-of-way, Pedestrian route, Permanent, Platform lift, Enclosed stair lift, Enclosed vertical lift, Unenclosed stair lift, Unenclosed vertical lift, Public right-of-way, Raised crossing, Raised intersection (or zero grade crosswalk), Ramp, Shared-use walkway, Short-term accommodation, Sign-controlled intersection, Signage, Signal-controlled intersection, Slip lane/uncontrolled access ramp, Slope, Counter slope, Cross slope, Gutter slope, Running slope, Splitter island, Tactile markings, Tactile walking surface indicator, Tactile attention indicator, Tactile direction indicator, Transfer space, Vehicular right-of-way, Visitable, Visual contrast, Walk signal interval, Wayfinding, Wheeled mobility device.

**The overlap test is crude and over-reports gaps** (it matches word stems, so 'Headroom' is flagged although RHFAC's 'Height clearance' is the same concept in other words). **What the digest shows.** B651 frames the *exterior and public realm* far more fully than RHFAC (pedestrian crossings, intersections, transit stops, urban furniture, landscaping, temporary works, trails and beach access in Annex D), treats several technique topics as clauses of their own where RHFAC scores them as single criteria (luminance contrast with a formula and a light-reflectance definition, tactile walking surface indicators, headroom and protruding objects, door-opening force, power-assisted doors, handrail grip, slip potential in Annex B), and puts the human body into the standard through Annex A (reach ranges, walkway widths for crutch users, the detection space for a long white cane, a service dog, dimensions of wheeled mobility devices, turning areas). Clause 4.7 names functional and cognitive barriers, environmental intolerances and acoustics as 'additional considerations' in recommendation form, which is the same ground as RHFAC chapter 11 and criteria 4.5 and 4.6. Whether other jurisdictions' instruments frame those topics as clauses, as recommendations or not at all is exactly what the native-language readings must find out.


## 3. The two views, generated from one table

### 3.1 Technique category × kind of place (criterion counts)

| Technique tag | site element | building element | room / space | system | building typology / room | dwelling room / element | outdoor typology | cross-cutting | Total |
|---|---|---|---|---|---|---|---|---|---|
| provision_and_quantity | 8 | 1 | 8 | 3 | 14 | 3 | 4 | 6 | 47 |
| surfaces_and_slip | 8 | 9 | 15 | 2 | 17 | 7 | 8 | 2 | 68 |
| reach_and_heights | 9 | 12 | 39 | 5 | 57 | 26 | 5 | 7 | 160 |
| seating_and_furniture | 7 | 6 | 19 | 1 | 43 | 6 | 5 | 3 | 90 |
| wayfinding_and_signage | 4 | 1 | 4 | 17 | 7 | 3 | 10 | 4 | 50 |
| circulation_geometry | 12 | 14 | 11 | 4 | 29 | 14 | 8 | 1 | 93 |
| outdoor_and_site | 13 | 0 | 1 | 0 | 9 | 3 | 4 | 2 | 32 |
| vertical_transitions | 12 | 19 | 1 | 0 | 5 | 11 | 8 | 1 | 57 |
| tactile_and_detectable | 6 | 7 | 0 | 4 | 1 | 2 | 4 | 0 | 24 |
| lighting_and_glare | 5 | 9 | 15 | 3 | 20 | 7 | 4 | 5 | 68 |
| operation_and_technology | 4 | 2 | 6 | 0 | 3 | 0 | 0 | 6 | 21 |
| doors_and_entries | 17 | 23 | 11 | 1 | 10 | 24 | 1 | 1 | 88 |
| colour_and_contrast | 4 | 13 | 10 | 3 | 1 | 4 | 5 | 1 | 41 |
| emergency_and_life_safety | 1 | 4 | 2 | 15 | 6 | 1 | 0 | 2 | 31 |
| sanitary_and_fixtures | 0 | 1 | 43 | 0 | 13 | 16 | 0 | 2 | 75 |
| communication_and_information | 0 | 3 | 7 | 4 | 15 | 1 | 1 | 5 | 36 |
| acoustic_and_audio | 0 | 2 | 7 | 2 | 9 | 1 | 0 | 3 | 24 |
| thermal_and_air | 0 | 0 | 1 | 1 | 5 | 0 | 0 | 3 | 10 |
| sensory_and_cognitive | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 11 | 13 |

### 3.2 Technique → where it appears (top places by criterion count)

- **provision_and_quantity** (47 criteria in 32 sections): 8.4 Lodging and Temporary Accommodation (5); 1.1 Parking Points (4); 12.3 Innovation (3); 4.4 Kitchens (2); 7.1 Emergency Exits and Areas of Refuge (2); 8.6 Cafeterias, Restaurants, and Bars (2); 9.4 Unit Kitchens (2); 10.1 Trail and Pathway Features (2)
- **surfaces_and_slip** (68 criteria in 40 sections): 2.3 Exterior Stairs (3); 3.6 Interior Stairs (3); 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (3); 5.1 Accessible Washrooms (3); 8.20 Specialized Learning Spaces (3); 9.6 Unit Interior Stairs (3); 10.3 Trail and Pathway Stairs (3); 2.1 Exterior Pathways to Facilities on Site (2)
- **reach_and_heights** (160 criteria in 61 sections): 5.3 Universal Washrooms (10); 5.1 Accessible Washrooms (9); 9.4 Unit Kitchens (9); 4.4 Kitchens (6); 5.2 Showers (6); 8.19 Family and Nursing Rooms (6); 8.4 Lodging and Temporary Accommodation (5); 8.20 Specialized Learning Spaces (5)
- **seating_and_furniture** (90 criteria in 47 sections): 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (5); 8.2 Assembly Areas and Lecture Theatres (5); 5.2 Showers (4); 8.20 Specialized Learning Spaces (4); 2.1 Exterior Pathways to Facilities on Site (3); 3.3 Corridors and Hallways (3); 5.3 Universal Washrooms (3); 8.1 Office Spaces (3)
- **wayfinding_and_signage** (50 criteria in 27 sections): 6.1 General Wayfinding and Signage (10); 10.4 Trail and Pathway Wayfinding and Signage (9); 6.2 Room Identification Signage (5); 2.4 Building Entrances (2); 9.2 Unit Entrance and Entrance to Outdoor Spaces (2); 1.1 Parking Points (1); 2.1 Exterior Pathways to Facilities on Site (1); 3.1 Interior Doors and Doorways (not including Washrooms) (1)
- **circulation_geometry** (93 criteria in 57 sections): 2.1 Exterior Pathways to Facilities on Site (4); 3.1 Interior Doors and Doorways (not including Washrooms) (3); 3.2 Path of Travel (3); 5.1 Accessible Washrooms (3); 8.2 Assembly Areas and Lecture Theatres (3); 8.20 Specialized Learning Spaces (3); 9.8 Unit Toilet Rooms (3); 1.1 Parking Points (2)
- **outdoor_and_site** (32 criteria in 16 sections): 1.1 Parking Points (6); 1.2 General Vehicular Access (3); 8.18 Outdoor Eating Areas (3); 9.2 Unit Entrance and Entrance to Outdoor Spaces (3); 10.1 Trail and Pathway Features (3); 2.1 Exterior Pathways to Facilities on Site (2); 2.4 Building Entrances (2); 8.16 Viewpoints (2)
- **vertical_transitions** (57 criteria in 27 sections): 3.5 Elevators (7); 2.3 Exterior Stairs (5); 3.6 Interior Stairs (5); 9.6 Unit Interior Stairs (5); 10.3 Trail and Pathway Stairs (5); 2.1 Exterior Pathways to Facilities on Site (2); 2.2 Exterior Ramps (2); 2.4 Building Entrances (2)
- **tactile_and_detectable** (24 criteria in 19 sections): 2.1 Exterior Pathways to Facilities on Site (2); 2.3 Exterior Stairs (2); 3.6 Interior Stairs (2); 6.2 Room Identification Signage (2); 10.1 Trail and Pathway Features (2); 1.1 Parking Points (1); 2.2 Exterior Ramps (1); 3.2 Path of Travel (1)
- **lighting_and_glare** (68 criteria in 53 sections): 4.6 Illumination and Building Systems (5); 11.2 Sensory Experience (4); 3.3 Corridors and Hallways (2); 3.5 Elevators (2); 3.8 Platform Lifts (2); 4.1 Lobby and Reception Areas (2); 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (2); 6.1 General Wayfinding and Signage (2)
- **operation_and_technology** (21 criteria in 12 sections): 4.2 Reception Desks, Service Counters, and Self-Service Transaction Kiosks (4); 12.3 Innovation (4); 2.4 Building Entrances (3); 3.1 Interior Doors and Doorways (not including Washrooms) (2); 1.1 Parking Points (1); 5.1 Accessible Washrooms (1); 5.3 Universal Washrooms (1); 8.6 Cafeterias, Restaurants, and Bars (1)
- **doors_and_entries** (88 criteria in 25 sections): 3.1 Interior Doors and Doorways (not including Washrooms) (17); 2.4 Building Entrances (16); 9.2 Unit Entrance and Entrance to Outdoor Spaces (11); 3.5 Elevators (5); 5.1 Accessible Washrooms (5); 5.3 Universal Washrooms (5); 9.8 Unit Toilet Rooms (5); 8.4 Lodging and Temporary Accommodation (4)
- **colour_and_contrast** (41 criteria in 28 sections): 3.3 Corridors and Hallways (4); 5.1 Accessible Washrooms (3); 3.1 Interior Doors and Doorways (not including Washrooms) (2); 3.5 Elevators (2); 3.6 Interior Stairs (2); 3.7 Escalators and Moving Walkways (2); 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (2); 5.3 Universal Washrooms (2)
- **emergency_and_life_safety** (31 criteria in 17 sections): 7.1 Emergency Exits and Areas of Refuge (6); 7.2 Fire Alarm Systems and Equipment (5); 7.3 Evacuation Instructions (4); 3.8 Platform Lifts (2); 8.20 Specialized Learning Spaces (2); 2.4 Building Entrances (1); 3.1 Interior Doors and Doorways (not including Washrooms) (1); 3.5 Elevators (1)
- **sanitary_and_fixtures** (75 criteria in 19 sections): 5.1 Accessible Washrooms (17); 5.3 Universal Washrooms (13); 5.2 Showers (8); 9.8 Unit Toilet Rooms (7); 9.9 Unit Showers and Bathtubs (5); 8.20 Specialized Learning Spaces (4); 9.4 Unit Kitchens (4); 4.4 Kitchens (3)
- **communication_and_information** (36 criteria in 20 sections): 4.2 Reception Desks, Service Counters, and Self-Service Transaction Kiosks (4); 8.3 Exhibit Spaces (4); 6.3 Directory Boards and Information Kiosks (3); 8.21 Libraries (3); 12.2 Website Information (3); 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (2); 8.4 Lodging and Temporary Accommodation (2); 8.17 Visitor Centre and Kiosk (2)
- **acoustic_and_audio** (24 criteria in 17 sections): 4.2 Reception Desks, Service Counters, and Self-Service Transaction Kiosks (2); 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges (2); 4.5 Acoustic Considerations (2); 8.2 Assembly Areas and Lecture Theatres (2); 8.4 Lodging and Temporary Accommodation (2); 8.21 Libraries (2); 11.2 Sensory Experience (2); 3.5 Elevators (1)
- **thermal_and_air** (10 criteria in 7 sections): 11.2 Sensory Experience (3); 8.10 Pools (2); 4.6 Illumination and Building Systems (1); 7.1 Emergency Exits and Areas of Refuge (1); 8.1 Office Spaces (1); 8.2 Assembly Areas and Lecture Theatres (1); 8.20 Specialized Learning Spaces (1)
- **sensory_and_cognitive** (13 criteria in 6 sections): 11.2 Sensory Experience (4); 11.1 Space (3); 8.23 Respite and Sensory Rooms (2); 11.3 Restoration (2); 12.1A ? (1); 12.2 Website Information (1)

### 3.3 Place → techniques it uses

| Section (room, element or typology) | Kind | Criteria | Technique tags present (count) |
|---|---|---|---|
| 1.1 Parking Points | site element | 12 | outdoor_and_site 6, provision_and_quantity 4, reach_and_heights 2, circulation_geometry 2, surfaces_and_slip 1, seating_and_furniture 1, wayfinding_and_signage 1, vertical_transitions 1, tactile_and_detectable 1, lighting_and_glare 1, operation_and_technology 1 |
| 1.2 General Vehicular Access | site element | 3 | outdoor_and_site 3, provision_and_quantity 1 |
| 2.1 Exterior Pathways to Facilities on Site | site element | 13 | circulation_geometry 4, seating_and_furniture 3, surfaces_and_slip 2, reach_and_heights 2, vertical_transitions 2, outdoor_and_site 2, tactile_and_detectable 2, wayfinding_and_signage 1, provision_and_quantity 1, doors_and_entries 1, colour_and_contrast 1, lighting_and_glare 1 |
| 2.2 Exterior Ramps | site element | 9 | vertical_transitions 2, circulation_geometry 2, surfaces_and_slip 2, reach_and_heights 1, seating_and_furniture 1, colour_and_contrast 1, tactile_and_detectable 1, lighting_and_glare 1, provision_and_quantity 1 |
| 2.3 Exterior Stairs | site element | 12 | vertical_transitions 5, surfaces_and_slip 3, reach_and_heights 3, circulation_geometry 2, tactile_and_detectable 2, seating_and_furniture 1, colour_and_contrast 1, lighting_and_glare 1, provision_and_quantity 1 |
| 2.4 Building Entrances | site element | 19 | doors_and_entries 16, operation_and_technology 3, wayfinding_and_signage 2, circulation_geometry 2, vertical_transitions 2, outdoor_and_site 2, reach_and_heights 1, emergency_and_life_safety 1, colour_and_contrast 1, lighting_and_glare 1, seating_and_furniture 1 |
| 3.1 Interior Doors and Doorways (not including Washrooms) | building element | 17 | doors_and_entries 17, circulation_geometry 3, operation_and_technology 2, colour_and_contrast 2, reach_and_heights 1, emergency_and_life_safety 1, wayfinding_and_signage 1, vertical_transitions 1, surfaces_and_slip 1, sanitary_and_fixtures 1 |
| 3.2 Path of Travel | building element | 5 | circulation_geometry 3, vertical_transitions 1, tactile_and_detectable 1 |
| 3.3 Corridors and Hallways | building element | 9 | colour_and_contrast 4, seating_and_furniture 3, surfaces_and_slip 2, reach_and_heights 2, lighting_and_glare 2, circulation_geometry 1, tactile_and_detectable 1 |
| 3.4 Interior Ramps | building element | 9 | vertical_transitions 2, circulation_geometry 2, surfaces_and_slip 2, reach_and_heights 1, seating_and_furniture 1, colour_and_contrast 1, tactile_and_detectable 1, lighting_and_glare 1 |
| 3.5 Elevators | building element | 19 | vertical_transitions 7, doors_and_entries 5, reach_and_heights 3, circulation_geometry 2, lighting_and_glare 2, colour_and_contrast 2, surfaces_and_slip 1, tactile_and_detectable 1, communication_and_information 1, emergency_and_life_safety 1, acoustic_and_audio 1 |
| 3.6 Interior Stairs | building element | 12 | vertical_transitions 5, surfaces_and_slip 3, reach_and_heights 3, circulation_geometry 2, tactile_and_detectable 2, colour_and_contrast 2, seating_and_furniture 1, lighting_and_glare 1 |
| 3.7 Escalators and Moving Walkways | building element | 6 | colour_and_contrast 2, reach_and_heights 1, tactile_and_detectable 1, seating_and_furniture 1, vertical_transitions 1, acoustic_and_audio 1, communication_and_information 1, lighting_and_glare 1 |
| 3.8 Platform Lifts | building element | 8 | vertical_transitions 2, emergency_and_life_safety 2, lighting_and_glare 2, circulation_geometry 1, doors_and_entries 1, provision_and_quantity 1, reach_and_heights 1, communication_and_information 1 |
| 4.1 Lobby and Reception Areas | room / space | 6 | lighting_and_glare 2, circulation_geometry 1, wayfinding_and_signage 1, sanitary_and_fixtures 1, surfaces_and_slip 1, colour_and_contrast 1, seating_and_furniture 1 |
| 4.2 Reception Desks, Service Counters, and Self-Service Transaction Kiosks | room / space | 10 | operation_and_technology 4, communication_and_information 4, reach_and_heights 3, seating_and_furniture 2, circulation_geometry 2, acoustic_and_audio 2, provision_and_quantity 1, doors_and_entries 1, wayfinding_and_signage 1, colour_and_contrast 1, lighting_and_glare 1 |
| 4.3 Waiting Areas, General Seating, Meeting Rooms, and Lounges | room / space | 9 | seating_and_furniture 5, surfaces_and_slip 3, colour_and_contrast 2, reach_and_heights 2, acoustic_and_audio 2, communication_and_information 2, lighting_and_glare 2, provision_and_quantity 1, circulation_geometry 1 |
| 4.4 Kitchens | room / space | 11 | reach_and_heights 6, sanitary_and_fixtures 3, circulation_geometry 2, provision_and_quantity 2, surfaces_and_slip 1, seating_and_furniture 1, lighting_and_glare 1 |
| 4.5 Acoustic Considerations | room / space | 3 | acoustic_and_audio 2, surfaces_and_slip 1, reach_and_heights 1, seating_and_furniture 1, lighting_and_glare 1 |
| 4.6 Illumination and Building Systems | room / space | 8 | lighting_and_glare 5, surfaces_and_slip 2, reach_and_heights 2, vertical_transitions 1, thermal_and_air 1, provision_and_quantity 1, outdoor_and_site 1, acoustic_and_audio 1, sanitary_and_fixtures 1 |
| 5.1 Accessible Washrooms | room / space | 23 | sanitary_and_fixtures 17, reach_and_heights 9, doors_and_entries 5, circulation_geometry 3, surfaces_and_slip 3, colour_and_contrast 3, seating_and_furniture 2, provision_and_quantity 1, wayfinding_and_signage 1, operation_and_technology 1, emergency_and_life_safety 1, lighting_and_glare 1 |
| 5.2 Showers | room / space | 11 | sanitary_and_fixtures 8, reach_and_heights 6, seating_and_furniture 4, surfaces_and_slip 2, provision_and_quantity 1, colour_and_contrast 1, lighting_and_glare 1 |
| 5.3 Universal Washrooms | room / space | 22 | sanitary_and_fixtures 13, reach_and_heights 10, doors_and_entries 5, seating_and_furniture 3, circulation_geometry 2, surfaces_and_slip 2, colour_and_contrast 2, provision_and_quantity 1, wayfinding_and_signage 1, operation_and_technology 1, communication_and_information 1, emergency_and_life_safety 1, lighting_and_glare 1 |
| 6.1 General Wayfinding and Signage | system | 10 | wayfinding_and_signage 10, lighting_and_glare 2, circulation_geometry 1, tactile_and_detectable 1, provision_and_quantity 1, surfaces_and_slip 1, colour_and_contrast 1 |
| 6.2 Room Identification Signage | system | 5 | wayfinding_and_signage 5, tactile_and_detectable 2, reach_and_heights 1, circulation_geometry 1 |
| 6.3 Directory Boards and Information Kiosks | system | 6 | communication_and_information 3, tactile_and_detectable 1, wayfinding_and_signage 1, circulation_geometry 1, reach_and_heights 1, acoustic_and_audio 1 |
| 7.1 Emergency Exits and Areas of Refuge | system | 6 | emergency_and_life_safety 6, provision_and_quantity 2, circulation_geometry 1, wayfinding_and_signage 1, doors_and_entries 1, colour_and_contrast 1, seating_and_furniture 1, thermal_and_air 1 |
| 7.2 Fire Alarm Systems and Equipment | system | 5 | emergency_and_life_safety 5, reach_and_heights 2, acoustic_and_audio 1, communication_and_information 1 |
| 7.3 Evacuation Instructions | system | 4 | emergency_and_life_safety 4, surfaces_and_slip 1, lighting_and_glare 1, colour_and_contrast 1, reach_and_heights 1 |
| 8.1 Office Spaces | building typology / room | 6 | reach_and_heights 3, seating_and_furniture 3, surfaces_and_slip 2, circulation_geometry 1, thermal_and_air 1, provision_and_quantity 1, lighting_and_glare 1 |
| 8.2 Assembly Areas and Lecture Theatres | building typology / room | 11 | seating_and_furniture 5, circulation_geometry 3, acoustic_and_audio 2, vertical_transitions 1, thermal_and_air 1, communication_and_information 1, reach_and_heights 1, lighting_and_glare 1 |
| 8.3 Exhibit Spaces | building typology / room | 9 | communication_and_information 4, circulation_geometry 1, seating_and_furniture 1, reach_and_heights 1, acoustic_and_audio 1, lighting_and_glare 1 |
| 8.4 Lodging and Temporary Accommodation | building typology / room | 18 | provision_and_quantity 5, reach_and_heights 5, doors_and_entries 4, seating_and_furniture 3, sanitary_and_fixtures 2, acoustic_and_audio 2, communication_and_information 2, lighting_and_glare 2, wayfinding_and_signage 1, emergency_and_life_safety 1, outdoor_and_site 1 |
| 8.5 Outdoor Recreation Areas | building typology / room | 4 | circulation_geometry 1, seating_and_furniture 1, outdoor_and_site 1, lighting_and_glare 1 |
| 8.6 Cafeterias, Restaurants, and Bars | building typology / room | 11 | reach_and_heights 4, seating_and_furniture 2, provision_and_quantity 2, circulation_geometry 1, communication_and_information 1, operation_and_technology 1, lighting_and_glare 1 |
| 8.7 Retail Outlets | building typology / room | 9 | reach_and_heights 4, circulation_geometry 1, surfaces_and_slip 1, seating_and_furniture 1, communication_and_information 1, lighting_and_glare 1 |
| 8.8 Playgrounds | building typology / room | 4 | circulation_geometry 1, surfaces_and_slip 1, seating_and_furniture 1, outdoor_and_site 1 |
| 8.9 Fitness and Sports Facilities | building typology / room | 7 | reach_and_heights 2, circulation_geometry 1, provision_and_quantity 1, tactile_and_detectable 1, sanitary_and_fixtures 1, lighting_and_glare 1 |
| 8.10 Pools | building typology / room | 12 | reach_and_heights 3, circulation_geometry 2, seating_and_furniture 2, vertical_transitions 2, thermal_and_air 2, surfaces_and_slip 1, colour_and_contrast 1, doors_and_entries 1, emergency_and_life_safety 1, lighting_and_glare 1 |
| 8.11 Change Rooms | building typology / room | 6 | reach_and_heights 3, seating_and_furniture 3, circulation_geometry 1, surfaces_and_slip 1, sanitary_and_fixtures 1, lighting_and_glare 1 |
| 8.12 Mail Areas | building typology / room | 5 | reach_and_heights 3, circulation_geometry 1, wayfinding_and_signage 1, surfaces_and_slip 1, lighting_and_glare 1 |
| 8.13 Shared Laundry Rooms | building typology / room | 6 | reach_and_heights 2, circulation_geometry 1, provision_and_quantity 1, operation_and_technology 1, wayfinding_and_signage 1, sanitary_and_fixtures 1, seating_and_furniture 1, lighting_and_glare 1 |
| 8.14 Storage Facilities and Lockers | building typology / room | 5 | reach_and_heights 2, circulation_geometry 1, wayfinding_and_signage 1, vertical_transitions 1, doors_and_entries 1, lighting_and_glare 1 |
| 8.15 Garbage Rooms | building typology / room | 3 | circulation_geometry 1, reach_and_heights 1, lighting_and_glare 1 |
| 8.16 Viewpoints | building typology / room | 9 | circulation_geometry 2, outdoor_and_site 2, surfaces_and_slip 2, seating_and_furniture 2, emergency_and_life_safety 1, reach_and_heights 1, vertical_transitions 1, wayfinding_and_signage 1 |
| 8.17 Visitor Centre and Kiosk | building typology / room | 7 | reach_and_heights 2, communication_and_information 2, circulation_geometry 1, doors_and_entries 1, wayfinding_and_signage 1, provision_and_quantity 1, seating_and_furniture 1, outdoor_and_site 1 |
| 8.18 Outdoor Eating Areas | building typology / room | 6 | reach_and_heights 3, seating_and_furniture 3, outdoor_and_site 3, circulation_geometry 2, provision_and_quantity 1, surfaces_and_slip 1, emergency_and_life_safety 1, lighting_and_glare 1 |
| 8.19 Family and Nursing Rooms | building typology / room | 9 | reach_and_heights 6, seating_and_furniture 3, sanitary_and_fixtures 2, circulation_geometry 1, doors_and_entries 1, surfaces_and_slip 1, lighting_and_glare 1 |
| 8.20 Specialized Learning Spaces | building typology / room | 15 | reach_and_heights 5, seating_and_furniture 4, sanitary_and_fixtures 4, circulation_geometry 3, surfaces_and_slip 3, emergency_and_life_safety 2, doors_and_entries 1, thermal_and_air 1, acoustic_and_audio 1, communication_and_information 1 |
| 8.21 Libraries | building typology / room | 10 | seating_and_furniture 3, communication_and_information 3, acoustic_and_audio 2, circulation_geometry 1, reach_and_heights 1, provision_and_quantity 1, operation_and_technology 1, lighting_and_glare 1 |
| 8.22 Ablution Stations | building typology / room | 8 | reach_and_heights 4, seating_and_furniture 3, surfaces_and_slip 2, sanitary_and_fixtures 2, circulation_geometry 1, doors_and_entries 1, lighting_and_glare 1 |
| 8.23 Respite and Sensory Rooms | building typology / room | 8 | sensory_and_cognitive 2, provision_and_quantity 1, wayfinding_and_signage 1, circulation_geometry 1, surfaces_and_slip 1, seating_and_furniture 1, reach_and_heights 1, acoustic_and_audio 1, lighting_and_glare 1 |
| 9.1 Unit Security and Entry Systems | dwelling room / element | 3 | wayfinding_and_signage 1, reach_and_heights 1, communication_and_information 1 |
| 9.2 Unit Entrance and Entrance to Outdoor Spaces | dwelling room / element | 13 | doors_and_entries 11, outdoor_and_site 3, wayfinding_and_signage 2, circulation_geometry 2, vertical_transitions 2, reach_and_heights 1, lighting_and_glare 1 |
| 9.3 Unit Interior Doors | dwelling room / element | 4 | doors_and_entries 3, circulation_geometry 2, vertical_transitions 1 |
| 9.4 Unit Kitchens | dwelling room / element | 16 | reach_and_heights 9, sanitary_and_fixtures 4, provision_and_quantity 2, circulation_geometry 1, doors_and_entries 1, tactile_and_detectable 1, lighting_and_glare 1 |
| 9.5 Unit Hallways | dwelling room / element | 4 | lighting_and_glare 2, circulation_geometry 1, colour_and_contrast 1, vertical_transitions 1 |
| 9.6 Unit Interior Stairs | dwelling room / element | 11 | vertical_transitions 5, surfaces_and_slip 3, reach_and_heights 3, circulation_geometry 2, colour_and_contrast 2, seating_and_furniture 1, tactile_and_detectable 1, lighting_and_glare 1 |
| 9.7 Unit Bedrooms and Closets | dwelling room / element | 5 | circulation_geometry 2, doors_and_entries 2, reach_and_heights 2, seating_and_furniture 2, surfaces_and_slip 1, vertical_transitions 1 |
| 9.8 Unit Toilet Rooms | dwelling room / element | 13 | sanitary_and_fixtures 7, doors_and_entries 5, reach_and_heights 5, circulation_geometry 3, surfaces_and_slip 1, seating_and_furniture 1 |
| 9.9 Unit Showers and Bathtubs | dwelling room / element | 8 | sanitary_and_fixtures 5, surfaces_and_slip 2, reach_and_heights 2, seating_and_furniture 1, doors_and_entries 1, colour_and_contrast 1 |
| 9.10 Unit Laundry | dwelling room / element | 4 | circulation_geometry 1, reach_and_heights 1, lighting_and_glare 1 |
| 9.11 Unit General Requirements | dwelling room / element | 5 | reach_and_heights 2, seating_and_furniture 1, provision_and_quantity 1, acoustic_and_audio 1, emergency_and_life_safety 1, vertical_transitions 1, doors_and_entries 1, lighting_and_glare 1 |
| 10.1 Trail and Pathway Features | outdoor typology | 11 | outdoor_and_site 3, seating_and_furniture 3, provision_and_quantity 2, circulation_geometry 2, surfaces_and_slip 2, reach_and_heights 2, tactile_and_detectable 2, wayfinding_and_signage 1, doors_and_entries 1, vertical_transitions 1, colour_and_contrast 1, lighting_and_glare 1 |
| 10.2 Trail and Pathway Ramps | outdoor typology | 8 | vertical_transitions 2, circulation_geometry 2, surfaces_and_slip 2, colour_and_contrast 2, reach_and_heights 1, seating_and_furniture 1, tactile_and_detectable 1, lighting_and_glare 1, provision_and_quantity 1 |
| 10.3 Trail and Pathway Stairs | outdoor typology | 11 | vertical_transitions 5, surfaces_and_slip 3, circulation_geometry 2, reach_and_heights 2, seating_and_furniture 1, tactile_and_detectable 1, colour_and_contrast 1, lighting_and_glare 1, provision_and_quantity 1 |
| 10.4 Trail and Pathway Wayfinding and Signage | outdoor typology | 9 | wayfinding_and_signage 9, circulation_geometry 2, communication_and_information 1, outdoor_and_site 1, surfaces_and_slip 1, lighting_and_glare 1, colour_and_contrast 1 |
| 11.1 Space | cross-cutting | 4 | sensory_and_cognitive 3, provision_and_quantity 2, circulation_geometry 1, wayfinding_and_signage 1, sanitary_and_fixtures 1, operation_and_technology 1 |
| 11.2 Sensory Experience | cross-cutting | 8 | lighting_and_glare 4, sensory_and_cognitive 4, reach_and_heights 3, thermal_and_air 3, surfaces_and_slip 2, acoustic_and_audio 2, seating_and_furniture 2, colour_and_contrast 1, wayfinding_and_signage 1, emergency_and_life_safety 1, provision_and_quantity 1 |
| 11.3 Restoration | cross-cutting | 3 | sensory_and_cognitive 2, lighting_and_glare 1, outdoor_and_site 1 |
| 12.1A ? | cross-cutting | 5 | communication_and_information 2, reach_and_heights 1, emergency_and_life_safety 1, sensory_and_cognitive 1 |
| 12.1B ? | cross-cutting | 5 | acoustic_and_audio 1, reach_and_heights 1, wayfinding_and_signage 1, operation_and_technology 1 |
| 12.2 Website Information | cross-cutting | 6 | communication_and_information 3, vertical_transitions 1, doors_and_entries 1, outdoor_and_site 1, sanitary_and_fixtures 1, wayfinding_and_signage 1, sensory_and_cognitive 1 |
| 12.3 Innovation | cross-cutting | 4 | operation_and_technology 4, provision_and_quantity 3, reach_and_heights 2, seating_and_furniture 1 |

### 3.4 Against the project's own categories

Technique-like categories the base already has — topic directories of `slugs`: bathrooms-and-wet-areas (5), communication-and-alerts (6), controls-and-hardware (3), economics (7), entrances-and-circulation (9), frameworks-and-methodology (19), health-and-symptom-management (10), kitchens-and-workspaces (1), population-general (12), room-types (1), seating-and-rest (2), sensory-environment (19), wayfinding-and-signage (12); term domains: functional_axis (17), circulation (16), methodology (14), medical (8), wayfinding (5), bathroom (5), acoustic (5), sensory (4), hardware (4), communication (4), economics (3), lighting (2), legal (2), thermal (1), population (1), housing (1), fire_safety (1), education (1).

Rooms the base holds (`rooms`, uncategorised, no reader): R-ASM Assembly and Event Space, R-BA Bathroom, R-BED Bedroom, R-CAN Canteen and Dining, R-CHW Changing Places / Changing Room, R-COR Corridor and Circulation, R-ENT Entry, R-GAR Garage and Vehicle Space, R-HAL Hallway and Circulation, R-KIT Kitchen, R-LAU Laundry, R-LIV Living Room, R-MTG Meeting Room, R-OFC Open-Plan Office, R-REC Reception and Lobby, R-STA Staircase, R-WC Accessible WC. The survey frames 23 building typologies or rooms in its chapter 8 and 11 dwelling rooms in chapter 9; the base's 17 rooms cover few of them (no pool, library, laboratory, lodging room, retail outlet, playground, fitness space, trail, viewpoint). **A typology/room axis in the base needs a source-derived list, not the current 17 rooms** (owner E8 froze `rooms`; that stands until a page reads them).

## 4. Beyond these two sources (leads, each [UNVERIFIED] until a source in hand states it)

- **Named by the B651 listing but not by RHFAC:** luminance (colour) contrast as a method; tactile direction indicator positioning; platform size for platform lifts; controls and sizes of power-assisted doors; water-bottle filling stations and fountain controls; anthropometric dimensions as the basis of clearances; functional and cognitive barriers as a category.
- **Categories the survey scores thinly or not at all**, from the project's own vocabulary and ICF frame: sound insulation between spaces and plant noise as measured quantities; vibration; air quality and ventilation (the survey asks only that scents be absent or contained); thermal setpoints; flicker and photosensitive thresholds (the survey asks for none identified); wayfinding for people who are Deafblind; sign-language and captioning provision as a space requirement; evacuation for people who cannot use stairs beyond "area of refuge" and "evacuation chair"; bariatric and short or tall stature ranges (owner-ruled body-size frame, access need A-SIZE); tactile and haptic communication zones; ceiling hoists; adult changing facilities beyond the washroom item; queuing and timed access.
- **Not in either source:** building typologies the survey does not frame (transit stations and vehicles, hospitals and clinics, schools beyond "specialized learning spaces", prisons, places of worship, cemeteries, temporary event structures). Whether a P1+P2+P3 instrument frames them is a question for the native-language readings, not for this list.

## 5. Research coverage, derived from the base

**Principle (owner, 2026-11-06): the base sets the research coverage.** Coverage is one measure of a (concept × language-and-jurisdiction pair) cell, computed from the base and the reading records; no separate list of what has been searched is kept (rules 5 and 8). The pairs are `lang_jur_map` rows for the P1+P2+P3 jurisdictions:

39 pairs (`select language, jurisdiction from lang_jur_map where jurisdiction in (…P1+P2+P3…)`): EN/AU, DE/BE, FR/BE, NL/BE, EN/CA, FR/CA, DE/CH, FR/CH, IT/CH, ZH/CN, DE/DE, DA/DK, ES/ES, DA/EU, DE/EU, EN/EU, ES/EU, FI/EU, FR/EU, IT/EU, NL/EU, PT/EU, SV/EU, FI/FI, SV/FI, FR/FR, EN/IE, IT/IT, JA/JP, KO/KR, NL/NL, NO/NO, EN/NZ, PT/PT, SV/SE, EN/SG, ZH/SG, EN/UK, EN/US.

**Today:** the reading ledger (`v_scan_ledger`) holds, for the 10 active parameters only: NOT-READ 417, EXTRACTED 94, READ-PARTIAL 40, READ-NOTHING-FOUND 22, STATED-ABSENT 7. Not one of the 32 recurring concepts above and none of the long tail has a cell, because none is a term yet; and the language half of a pair cannot be derived for any source, since `evidence_sources.language` is NULL on every row (plan defect A6). **Coverage of the new register is 0 until the first native-language reading is recorded.**

**Cell states** (proposed; the bucket table T-6b is the home): NOT-SEARCHED; SEARCHED-FOUND (phrase, locator, quote, instrument); SEARCHED-ABSENT (the instrument was read in full and states nothing); SEARCHED-QUERY-FAILED (the search shape failed, R14); NOT-OBTAINABLE (instrument held back by paywall or block, with the attempt logged).

## 6. The terminology research pass

This is research, and it needs passes that read instruments in their own language. One pass per language-and-jurisdiction pair:

1. **Instrument list** for the pair: the primary accessibility instrument(s) in force, current editions only (workplan HANDOFF section 3), from `research_code_leads`, `references/standards-registry.md` and what is held. Retrieve each through `retrieval_log.fetch`; a block goes to the Wayback `if_` route (CLAUDE.md section 7); a failure is logged, not hidden.
2. **Search seeds.** The English register is rendered into the language as **flagged, model-generated search seeds** (owner OR-12b, third 2026-11-06 statement): terms the model believes are in use in that jurisdiction, never word for word, recorded as seeds and never as aliases. Seeds only point the reading.
3. **Read the instrument in full in its own language** (OR-13 open pass), not only for the seeds. For each concept found: the phrase **as the instrument writes it**, locator, a verbatim quote that verifies in the saved text, and the instrument. For each concept the instrument treats that the register lacks: the same record, in the instrument's phrase (reverse harvest, E1). For each register concept not found after a full reading: SEARCHED-ABSENT.
4. **Observe → adjudicate → attest** with the verbs that exist (`observe-term`, `adjudicate-term`, `add-alias` or `add-term --from-observation`); a seed whose phrase is found becomes an attested alias in place (migration 117). Rows ship in a research PR after the tooling PR merges.
5. **No pair is second-read before every pair is first-read**, so English does not become the frame (plan C.3).

## 7. What this needs from the owner

- Whether to run the first terminology passes now (research with retrieval and logging, no database rows until the tooling PR merges), and for which pairs first. Recommended: one pilot pass in three structurally different languages (Japanese, German, French) to expose method defects before all 14.
