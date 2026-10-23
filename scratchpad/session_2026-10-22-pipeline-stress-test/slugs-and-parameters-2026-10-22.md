# Search slugs and parameters, as the database holds them (2026-10-22)

Read-only listing. Re-derive, do not quote: every figure is the result of a query against `data/guidebook.db` (user_version 116). The screen is the one `db.py mint-term-from-catalogue` applies: `db._VALUE_BEARING` (a digit, a comparator or a min/max word) and `db._ITEM_CODE` (an old `[A-Z]-NN` code). Nothing here has been written to the database.

## 1. Parameters (`base_parameters`)

| id | term | name | status | direction | extractions | live determinations | fails value screen | item code |
|---|---|---|---|---|---|---|---|---|
| 3 | TERM-001 | ramp gradient | active | lower_is_better | 101 | 0 | no | no |
| 4 | TERM-002 | corridor width | active | - | 0 | 0 | no | no |
| 5 | TERM-003 | turning circle | active | - | 0 | 0 | YES: '3' | no |
| 6 | TERM-005 | operating force | active | - | 0 | 0 | no | no |
| 7 | TERM-007 | reverberation time | active | - | 0 | 0 | YES: '6' | no |
| 8 | TERM-011 | LRV contrast | active | - | 0 | 0 | no | no |
| 9 | TERM-021 | door width | active | - | 0 | 0 | no | no |
| 10 | TERM-024 | colour temperature | active | - | 0 | 0 | no | no |
| 11 | TERM-061 | headroom clearance | active | - | 0 | 0 | no | no |
| 12 | TERM-091 | ramp run length | active | - | 0 | 0 | no | no |

Declined as a parameter (`parameter_declinations`):
- TERM-089: An element, not a quantity under determination: its slope is TERM-001 (ramp gradient, parameter 3), its length TERM-091 and its landings TERM-092. A determination is keyed on a quantity; 'ramp' has no value to determine. The term stays in the vocabulary and keeps its adjudications.

## 2. The vocabulary the parameters come from (`terms`)

Only terms marked P are parameters. The rest are elements, concepts, conditions, populations and methods. V = the name or definition fails the value screen.


**acoustic**
- TERM-006 hearing loop  [-] aliases=33
- TERM-007 reverberation time  [P7 V('6')] aliases=26
- TERM-029 sound masking  [-] aliases=27
- TERM-049 acoustic absorption  [-] aliases=51
- TERM-050 speech intelligibility  [-] aliases=28

**bathroom**
- TERM-008 grab bar  [-] aliases=33
- TERM-009 accessible bathroom  [-] aliases=40
- TERM-023 anti-scald valve  [-] aliases=24
- TERM-058 Changing Places toilet  [-] aliases=32
- TERM-072 toileting provision planning  [-] aliases=31

**circulation**
- TERM-001 ramp gradient  [P3] aliases=37
- TERM-002 corridor width  [P4] aliases=32
- TERM-003 turning circle  [P5 V('3')] aliases=33
- TERM-014 accessible lift  [-] aliases=32
- TERM-021 door width  [P9] aliases=22
- TERM-022 level threshold  [-] aliases=22
- TERM-027 accessible parking  [-] aliases=23
- TERM-048 circulation route  [-] aliases=53
- TERM-052 rest point seating  [-] aliases=49
- TERM-061 headroom clearance  [P11] aliases=37
- TERM-079 mobility aid  [-] aliases=53
- TERM-089 ramp  [declined] aliases=0
- TERM-090 level difference  [-] aliases=0
- TERM-091 ramp run length  [P12] aliases=0
- TERM-092 intermediate landing  [-] aliases=0
- TERM-093 ramp usability  [-] aliases=0

**communication**
- TERM-025 captioning  [-] aliases=34
- TERM-026 vibrotactile alert  [-] aliases=23
- TERM-051 AAC (augmentative and alternative communication)  [-] aliases=23
- TERM-086 cognitive accessibility and easy read  [-] aliases=36

**economics**
- TERM-064 home adaptation grant  [-] aliases=23
- TERM-065 accessibility economics  [-] aliases=34
- TERM-066 construction cost  [-] aliases=26

**education**
- TERM-070 school learning environment  [-] aliases=44

**fire_safety**
- TERM-013 visual fire alarm  [-] aliases=33

**functional_axis**
- TERM-031 Ambulant movement  [-] aliases=6
- TERM-032 Arousal-safety demand  [-] aliases=3
- TERM-033 Auditory access & alerting demand  [-] aliases=6
- TERM-034 Balance & postural demand  [-] aliases=6
- TERM-035 Airborne-exposure demand  [-] aliases=3
- TERM-036 Toileting-proximity demand  [-] aliases=3
- TERM-037 Information-access demand  [-] aliases=3
- TERM-038 Orientation demand  [-] aliases=6
- TERM-039 Expressive-communication demand  [-] aliases=3
- TERM-040 Pain-load demand  [-] aliases=6
- TERM-041 Reach & manipulation  [-] aliases=6
- TERM-042 Sensory-load demand  [-] aliases=6
- TERM-043 Sustained-exertion demand  [-] aliases=3
- TERM-044 Thermal demand  [-] aliases=6
- TERM-045 Low-vision information demand  [-] aliases=6
- TERM-046 Non-visual information demand  [-] aliases=6
- TERM-047 Wheeled movement & transfer  [-] aliases=6

**hardware**
- TERM-004 lever handle  [-] aliases=31
- TERM-005 operating force  [P6] aliases=26
- TERM-084 laundry and utility room  [-] aliases=30
- TERM-088 upper limb function and grip  [-] aliases=45

**housing**
- TERM-068 accessible housing  [-] aliases=34

**legal**
- TERM-067 CRPD (Convention on the Rights of Persons with Disabilities)  [-] aliases=25
- TERM-075 jurisdictional accessibility standards  [-] aliases=38

**lighting**
- TERM-018 circadian lighting  [-] aliases=34
- TERM-024 colour temperature  [P10] aliases=17

**medical**
- TERM-015 thermoregulation impairment  [-] aliases=22
- TERM-020 sensory overload  [-] aliases=29
- TERM-053 fatigue and post-exertional malaise  [-] aliases=38
- TERM-054 dysautonomia and orthostatic intolerance  [-] aliases=34
- TERM-055 chronic pain  [-] aliases=33
- TERM-056 vestibular dysfunction  [-] aliases=46
- TERM-057 tremor and involuntary movement  [-] aliases=51
- TERM-080 neurological impairment  [-] aliases=50

**methodology**
- TERM-017 universal design  [-] aliases=34
- TERM-030 dementia-friendly design  [-] aliases=25
- TERM-059 visitability  [V('Minimum')] aliases=31
- TERM-060 post-occupancy evaluation  [-] aliases=26
- TERM-062 body dimensions (anthropometrics)  [-] aliases=35
- TERM-071 Design for Adaptable Readiness (DAR)  [-] aliases=32
- TERM-076 multilingual evidence convergence  [-] aliases=11
- TERM-077 cross-population design conflict  [-] aliases=13
- TERM-078 case study  [-] aliases=28
- TERM-081 occupational therapy (OT)  [-] aliases=33
- TERM-082 biophilic design  [-] aliases=23
- TERM-083 trauma-informed design  [-] aliases=20
- TERM-087 temporal accessibility and pacing  [-] aliases=42
- TERM-094 accessibility audit  [-] aliases=0

**population**
- TERM-016 wheelchair user  [-] aliases=31

**sensory**
- TERM-012 sensory room  [-] aliases=45
- TERM-073 neurodivergent sensory environment  [-] aliases=37
- TERM-074 withdrawal space and exit legibility  [-] aliases=20
- TERM-085 fragrance-free policy  [-] aliases=34

**thermal**
- TERM-063 thermal comfort  [-] aliases=40

**wayfinding**
- TERM-010 tactile walking surface indicator  [-] aliases=40
- TERM-011 LRV contrast  [P8] aliases=32
- TERM-019 pictogram signage  [-] aliases=30
- TERM-028 wayfinding  [-] aliases=25
- TERM-069 haptic affordance  [-] aliases=34

Terms failing the value screen: 3 of 94. The 17 terms in domain `functional_axis` are named "... demand" and are not quantities.

## 3. Search slugs (`slugs`, 106 rows)

A slug is a research TOPIC. It is not a parameter and no column links one to the other. Counts: sources linked (`source_slug_links`), searches logged (`search_executions`).

Status: ACTIVE=80, MERGED=3, STUB=23


**bathrooms-and-wet-areas** (5)
- accessible-bathroom-and-grab-bar  [ACTIVE] sources=0 searches=0
- bathroom-typology-global-south  [ACTIVE] sources=0 searches=0
- changing-places-adult-changing-facilities  [STUB] sources=0 searches=0
- fold-down-grab-bar-specification  [ACTIVE] sources=0 searches=0
- toileting-proximity-provision-planning  [STUB] sources=0 searches=0

**communication-and-alerts** (6)
- aac-speech-production-environments  [STUB] sources=0 searches=0
- assistive-listening-systems  [ACTIVE] sources=0 searches=0
- counter-intercom-communication-access  [STUB] sources=0 searches=0
- deaf-acoustic-built-environment  [ACTIVE] sources=0 searches=0
- deaf-classroom-reverberation-time  [ACTIVE] sources=0 searches=0
- deaf-spatial-design  [ACTIVE] sources=0 searches=0

**controls-and-hardware** (3)
- motor-precision-controls-and-targets  [STUB] sources=0 searches=0
- reach-range-and-accessible-controls  [ACTIVE] sources=0 searches=0
- short-stature-reach-envelope-design  [STUB] sources=0 searches=0

**economics** (7)
- accessibility-feature-market-value-uplift-framing  [ACTIVE] sources=0 searches=0
- accessible-design-economics-cost-premium  [ACTIVE] sources=0 searches=0
- case-study-economics-financial-data  [ACTIVE] sources=0 searches=0
- construction-cost-data  [ACTIVE] sources=0 searches=0
- economics-sources  [ACTIVE] sources=0 searches=0
- government-grant-programmes  [ACTIVE] sources=0 searches=0
- government-grant-programmes-home-adaptation  [ACTIVE] sources=0 searches=0

**entrances-and-circulation** (9)
- accessible-circulation-geometry  [ACTIVE] sources=53 searches=163
- fall-risk-flooring-handrail-design  [STUB] sources=0 searches=0
- floor-vibration-wheelchair-disability  [ACTIVE] sources=0 searches=0
- residential-entry-and-threshold  [ACTIVE] sources=0 searches=0
- stair-ramp-threshold-biomechanics-accessibility  [ACTIVE] sources=3 searches=0
- tall-stature-headroom-envelope  [STUB] sources=0 searches=0
- threshold-and-level-access  [ACTIVE] sources=2 searches=0
- threshold-door-hardware  [ACTIVE] sources=0 searches=0
- timed-access-and-pacing-built-environment  [STUB] sources=0 searches=0

**frameworks-and-methodology** (19)
- accessible-design-failures-poor-performance  [ACTIVE] sources=3 searches=0
- body-sizes-supplementary-populations  [ACTIVE] sources=0 searches=0
- co1-housing-research-global-south  [ACTIVE] sources=0 searches=0  V('1')
- cross-population-case-studies  [ACTIVE] sources=0 searches=0
- cross-population-conflict-resolutions  [ACTIVE] sources=0 searches=0
- crpd-implementation-built-environment  [ACTIVE] sources=0 searches=0
- design-framework-evidence-audit  [ACTIVE] sources=0 searches=0
- ecological-psychology-haptic-affordances-built-environment  [ACTIVE] sources=0 searches=0
- european-accessibility-act-scope-clarification  [ACTIVE] sources=0 searches=0
- jurisdiction-grant-programmes-comprehensive  [ACTIVE] sources=0 searches=0
- jurisdiction-matrix-accessibility-standards  [ACTIVE] sources=0 searches=0
- manoeuvring-footprint-vs-turning-radius-methodology  [ACTIVE] sources=0 searches=0
- multilingual-evidence-convergence-non-english  [ACTIVE] sources=0 searches=0
- ot-built-environment-interface  [ACTIVE] sources=0 searches=0
- ot-frameworks-built-environment  [ACTIVE] sources=0 searches=0
- post-occupancy-evaluation-global  [ACTIVE] sources=0 searches=0
- residential-accessible-home-case-studies  [ACTIVE] sources=0 searches=0
- residential-dar-provisions-priority-register  [ACTIVE] sources=0 searches=0
- visitability-residential-accessibility-minimum-standards  [ACTIVE] sources=0 searches=0  V('minimum')

**health-and-symptom-management** (10)
- chronic-pain-built-environment  [MERGED -> pain-ofs-built-environment-design] sources=0 searches=0
- fatigue-spectrum-built-environment  [MERGED -> pain-ofs-built-environment-design] sources=0 searches=0
- long-covid-dysautonomia-built-environment  [STUB] sources=0 searches=0
- movement-disorder-tremor-built-environment  [STUB] sources=0 searches=0
- ms-thermal-temperature-conflict-resolution  [ACTIVE] sources=0 searches=0
- ofs-built-environment  [ACTIVE] sources=0 searches=0
- pain-ofs-built-environment-design  [ACTIVE] sources=0 searches=0
- thermal-comfort-older-adults-care-settings  [ACTIVE] sources=0 searches=0
- thermoregulation-built-environment  [ACTIVE] sources=0 searches=0
- vestibular-balance-built-environment  [ACTIVE] sources=0 searches=0

**kitchens-and-workspaces** (1)
- residential-kitchen-and-task-surfaces  [ACTIVE] sources=0 searches=0

**population-general** (12)
- deafblind-built-environment-design  [ACTIVE] sources=0 searches=0
- dementia-built-environment  [ACTIVE] sources=0 searches=0
- hearing-impairment-built-environment  [MERGED -> deaf-acoustic-built-environment] sources=0 searches=0
- intellectual-disability-built-environment-design  [ACTIVE] sources=0 searches=0
- mental-health-built-environment  [ACTIVE] sources=0 searches=0
- mobility-built-environment  [ACTIVE] sources=4 searches=0
- ndv-aut-built-environment-quantified-thresholds  [ACTIVE] sources=0 searches=0
- neurodivergent-built-environment  [ACTIVE] sources=0 searches=0
- neurological-built-environment  [ACTIVE] sources=0 searches=0
- ot-cpg-built-environment  [ACTIVE] sources=0 searches=0
- upper-limb-impairment-built-environment  [ACTIVE] sources=0 searches=0
- visual-impairment-built-environment  [ACTIVE] sources=0 searches=0

**room-types** (1)
- accessible-laundry-room-design  [ACTIVE] sources=0 searches=0

**seating-and-rest** (2)
- bariatric-turning-radius-built-environment  [ACTIVE] sources=0 searches=0
- energy-conservation-rest-points-seating  [STUB] sources=0 searches=0

**sensory-environment** (19)
- acoustics-speech-intelligibility-disability  [ACTIVE] sources=0 searches=0
- air-quality-voc-chemical-sensitivity-built-environment  [ACTIVE] sources=0 searches=0
- arousal-safety-retreat-exit-legibility  [STUB] sources=0 searches=0
- biophilic-design-healthcare-workplace  [ACTIVE] sources=0 searches=0
- circadian-lighting-melanopic-edi  [ACTIVE] sources=0 searches=0
- flash-threshold-photosensitive-safety  [STUB] sources=0 searches=0
- fragrance-free-material-disclosure-design  [STUB] sources=0 searches=0
- open-plan-office-sensory-load  [STUB] sources=0 searches=0
- room-acoustic-performance  [ACTIVE] sources=0 searches=28
- school-environment-autism  [ACTIVE] sources=0 searches=0
- sensory-processing-model-design-application  [ACTIVE] sources=0 searches=0
- sensory-relief-space-design  [ACTIVE] sources=0 searches=0
- sensory-room-user-control  [ACTIVE] sources=0 searches=0
- sensory-space-global-south  [ACTIVE] sources=0 searches=0
- stimulus-density-control-turn-it-down  [STUB] sources=0 searches=0
- therapeutic-lighting-design  [ACTIVE] sources=0 searches=0
- trauma-informed-design-built-environment  [STUB] sources=0 searches=0
- visual-fire-alarm-seizure-safety  [ACTIVE] sources=0 searches=0
- visual-motion-sensitivity-specular-surfaces  [STUB] sources=0 searches=0

**wayfinding-and-signage** (12)
- cognitive-wayfinding-design  [ACTIVE] sources=0 searches=0
- deafblind-tactile-landmarks-built-environment  [STUB] sources=0 searches=0
- detectable-gradient-protocol-sensory-zones  [ACTIVE] sources=0 searches=0
- information-access-multilingual-scripts-literacy  [STUB] sources=0 searches=0
- luminance-contrast-and-pattern  [ACTIVE] sources=0 searches=0
- luminance-contrast-lrv-evidence-base  [ACTIVE] sources=0 searches=0
- plain-language-easy-read-signage  [STUB] sources=0 searches=0
- protactile-tactile-wayfinding  [STUB] sources=0 searches=0
- visual-alerting-and-wayfinding-light  [ACTIVE] sources=0 searches=0
- wayfinding-cognitive-science-spatial-design  [ACTIVE] sources=0 searches=0
- wayfinding-dementia-spatial-design  [ACTIVE] sources=0 searches=0
- wayfinding-global-south  [ACTIVE] sources=0 searches=0

Slugs failing the screen: 2 — co1-housing-research-global-south ('1'); visitability-residential-accessibility-minimum-standards ('minimum').
Slugs with at least one search: 2. Slugs with at least one linked source: 5.
