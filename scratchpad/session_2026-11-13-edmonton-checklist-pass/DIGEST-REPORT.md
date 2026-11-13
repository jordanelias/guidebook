# Digest report, third run: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The third run wrote 8 extractions on 4 parameters (5 value figures, 2 page-1 harm findings, 1 absent finding), each with every lens link its words warrant (21 links: identity, access need and ICF), 132 observations adjudicated once each, no `exceeds` edge, no `ALL`, no promotion, no declination and no minted term; 8 figures whose clause names no one and 3 source pairings no relation kind can state are parked as exact argv. **The batch is NON-COMPLIANT on R16 pending OD-53, deliberately**: 10 held terms the source's phrases name are adjudicated `NAMES-EXISTING` and are neither parameters nor declined; the 9 cells the lens links reach are all `pending`; nothing is applied, and the canonical database's sha256 did not move.

*Session `session_2026-11-13-edmonton-checklist-pass`, research, `from-evidence` (owner-supplied PDF). A fresh scratch copy of `data/guidebook.db` (`$SC` = `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay3`), worked as `REPLAY-V3-BRIEF.md` orders over `REPLAY-BRIEF.md` and `ADJUDICATION.md`. The first run is in `v1/`, the second in `v2/`. Every count below is printed with the query that produced it; re-run rather than trust. Canonical sha256 before and after: `3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb`. Decision numbers are the register's (`grep -n -E '^### OD-(4[7-9]|5[0-5])' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`): OD-47 lens for a clause naming no one, OD-48 design_scale, OD-49 building type and elements, OD-50 may a non-code source add a parameter, OD-51 Co-1 standing of the committee, OD-52 "barrier-free path of travel", OD-53 bulk declination, OD-54 hand-written canonical rows.*

---

## 1. Stages

| Stage | Done |
|---|---|
| base | Read only. No term minted, promoted or declined. |
| research | Skipped by the variant. Owner-supplied admission logged (`--origin owner-supplied`; the writer demands a subject, so `--slug stair-ramp-threshold-biomechanics-accessibility`: gap GAP-103). Its `CO1-NOT-APPLICABLE` waiver says only that this batch runs no search and so owes no Co-1 or Co-2 search; the topic's Co-1, T2 and Co-2 pass was not performed (gap GAP-116). |
| evidence | `add-source`: guideline, grey, intrinsic, tier 3 derived, CA, no DOI, no `publisher_location` (not in the payload), VERIFIED `direct-render` (all nine renders p0000 to p0008 read in this run), five slug links. `pub_year` 2022's basis has no writer (gap GAP-106). |
| judgment | 132 observations in one pass, each adjudicated once; the catalogue scan recorded after them; 8 extractions; 21 lens links; two `insufficient` edges on the harm findings; population match PROXY for MOB, the only identity linked. |
| synthesis | Nothing written: the source's pairings have no relation kind (parked; gap GAP-115). |
| specification | `assess_cell.py` once per cell the lens links reach, after every write: 9 cells. |
| render | None; every cell pending. |

## 2. Extractions written
Source class is the source's own colour (its legend, PDF p. 1: blue "Code (required)", magenta "Best Practice"; text layer in `items.json`, checked on the renders in this run). It is an attribution, not a guidebook classification.

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select e.extraction_id, e.parameter_id, t.canonical_en, e.source_section, e.figure_role, e.claim_type, coalesce(e.comparator,''), coalesce(e.claimed_value,''), coalesce(e.claimed_unit,''), e.root_type, coalesce(e.device_class,''), e.harm_finding, e.claim_text from source_value_extractions e join base_parameters p using(parameter_id) join terms t using(term_id) where e.ref_id='REF-01037' order by 1`

| id | parameter | item | source's class | role | bound / value | lens links | root | device | edges | claim text (start) |
|---|---|---|---|---|---|---|---|---|---|---|
| 228 | 9 door width | 2.3 | Code (required), blue | claim | >= 850 mm | d465, A-REACH, MOB | untraced | mixed |  | “Doorway clearance is 850mm when the door is in the open 90 degree posi” |
| 229 | 9 door width | 2.3 | Best Practice, magenta | claim | >= 920 mm | d465, A-REACH, MOB | committee_assertion | mixed |  | “(920mm/36” preferred)” |
| 230 | 9 door width | 5.3 | Best Practice, magenta | claim | >= 910 mm | d465, A-REACH, MOB | committee_assertion | mixed |  | “with elevator door at least 910 – 915mm/36” wide” |
| 231 | 5 turning circle | 5.3 | Best Practice, magenta | claim | >= 1500 mm | d465, A-REACH, MOB | committee_assertion | mixed |  | “Preferred dimension of elevator car to allow for optimal turning radiu” |
| 232 | 12 ramp run length | 6.2 | Code (required), blue | claim | <= 9 m | A-EFFORT | untraced |  |  | “Level landings/ resting areas provided at 9m/10yd intervals along ramp” |
| 233 | 6 operating force | 2.4 | Code (required), blue | finding | absent | d440, d445 | untraced |  |  | “Door operating device should not require tight grasping or twisting of” |
| 234 | 9 door width | p1 | page 1 (no class) | finding (harm) | minimum-standard door widths are insufficient for many wheel… | d465, A-REACH, MOB | committee_assertion | mixed | insufficient → 228 | “there is a need to exceed minimum standards for accessibility where po” |
| 235 | 5 turning circle | p1 | page 1 (no class) | finding (harm) | a minimum-standard turning radius is insufficient for many w… | d465, A-REACH, MOB | committee_assertion | mixed | insufficient → "Alberta Building Code" | “there is a need to exceed minimum standards for accessibility where po” |

Every live lens link of these rows, as the brief asks it printed:
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select extraction_id, identity_code, needs_code, icf_code, basis from v_live_lens_links where extraction_id >= 228 order by 1, 2, 3, 4`

| extraction | identity | access need | ICF | basis |
|---|---|---|---|---|
| 228 |  |  | d465 | named_in_text |
| 228 |  | A-REACH |  | named_in_text |
| 228 | MOB |  |  | named_in_text |
| 229 |  |  | d465 | named_in_text |
| 229 |  | A-REACH |  | named_in_text |
| 229 | MOB |  |  | named_in_text |
| 230 |  |  | d465 | named_in_text |
| 230 |  | A-REACH |  | named_in_text |
| 230 | MOB |  |  | named_in_text |
| 231 |  |  | d465 | named_in_text |
| 231 |  | A-REACH |  | named_in_text |
| 231 | MOB |  |  | named_in_text |
| 232 |  | A-EFFORT |  | named_in_text |
| 233 |  |  | d440 | named_in_text |
| 233 |  |  | d445 | named_in_text |
| 234 |  |  | d465 | named_in_text |
| 234 |  | A-REACH |  | named_in_text |
| 234 | MOB |  |  | named_in_text |
| 235 |  |  | d465 | named_in_text |
| 235 |  | A-REACH |  | named_in_text |
| 235 | MOB |  |  | named_in_text |

- **Lens rule applied throughout (F4):** the words must name the function or need, not merely the feature. The page-1 sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today" names wheelchair and scooter users (MOB), the need whose design obligation names "doorway/turning clearance" and which absorbs wheelchair users (A-REACH), and moving around using equipment (ICF d465); each row's notes mark the page-1 warrant [ASSUMPTION] (W1, OD-47). Item 2.4's "tight grasping or twisting of the wrist" names hand functions: ICF d440 "Fine hand use" and d445 "Hand and arm use"; no access-need design obligation names grip or the wrist, so no need link. "Level landings/ resting areas" keeps A-EFFORT on "resting areas", marked [ASSUMPTION] as the judge's reading that the words name the resting function. No ICF code is linked to it: b455 has no registry title to read a warrant against. No identity `ALL`: `select count(*) from v_live_lens_links where extraction_id >= 228 and identity_code='ALL'` → 0.
- **No `exceeds` edge (F1):** `select count(*) from extraction_relations r join source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037' and r.relation='exceeds'` → 0. The edges written are the two harm findings' `insufficient` edges, whose meaning ("the referent's value is NOT ENOUGH for the population or task") is the source's.
- **Bounds, not points:** blue "is"/"should be" figures are `>=` (the source's page 1 calls the code "the minimum standards"); magenta "preferred"/"recommend" figures are `>=` with the reading in notes; the 9 m interval is `<=`; "at least 910 – 915mm" is `>=` 910 with 915 in notes; item 5.3's "1500x1500mm" is stored as the side, as canonical extraction 211 stores "1.4미터×1.4미터" as 1.4 m (`select ref_id, setting from source_value_extractions where extraction_id=211`).
- **Roots:** blue figures `untraced` with the OR-19 echo sentence (precedent canonical extractions 57 and 64); magenta figures `committee_assertion` with the basis sentence F12 gives.
- **Absent findings:** 1 written (item 2.4, parameter 6, with its ICF links); none parked. The parameter-8 (LRV) absent row is not written.

## 3. Parked writes (not written)
`scratchpad/session_2026-11-13-edmonton-checklist-pass/parked-writes.jsonl`. Two kinds, counted separately (`grep -c '"kind": "extraction"'` and `grep -c '"kind": "pairing"'` on the file): **8 figure lines** waiting on OD-47, each the exact `db.py add-extraction` argv with the lens blank, and **3 pairing lines** waiting on "no relation kind states a recommended figure beside a stated floor", each the `relate-extraction` argv with the relation left as a marked hole. No absent finding is parked. Every figure line was dry-run twice against the scratch copy (nothing written): as parked it is refused only by D-0182 ("an extraction must be stated in at least one lens"); with a probe lens (`--identity MOB` on its own first word) it is accepted. The probe is a dry run and says nothing about which lens is right. The written pairing line (2.3) was dry-run and is refused by argparse for its hole, as intended; the two pairings between parked rows cannot be dry-run until those rows exist. Gap GAP-109 points at the file.

| key | kind | parameter | bound | edges / pair | waits on | source words | dry-run exit as parked | with probe lens |
|---|---|---|---|---|---|---|---|---|
| 6.1-1in20 | extraction | 3 | (condition) 1:20 |  | OD-47 | “Ramps are used for any slope steeper than 1 in 20 in a path of travel.” | 1 | 0 |
| 6.1-1in16 | extraction | 3 | <= 1:16 | condition_on → 6.1-1in20 | OD-47 | “Preferred maximum slope is 1 in 16” | 1 | 0 |
| 6.1-1in12 | extraction | 3 | <= 1:12 | condition_on → 6.1-1in20 | OD-47 | “(1 in 12 in AB building code)” | 1 | 0 |
| 1.2-1500 | extraction | 4 | >= 1500 |  | OD-47; OD-52 (which route term the path is; its width observation is DEFERRED on it) | “Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)” | 1 | 0 |
| 2.10-1100 | extraction | 4 | >= 1100 |  | OD-47 | “Corridors should be 1100mm/43”” | 1 | 0 |
| 2.10-1800 | extraction | 4 | >= 1800 |  | OD-47 | “(recommend 1800mm/71”)” | 1 | 0 |
| 6.2-870 | extraction | 4 | >= 870 |  | OD-47 | “870mm/34” min clearspace between handrails” | 1 | 0 |
| 1.8-2750 | extraction | 11 | >= 2750 |  | OD-47 | “a clear height of not less than 2750mm/108” at the pull-up space and a” | 1 | 0 |
| pair-2.3-920-850 | pairing |  |  | 229 → 228 | no relation kind states a recommended figure beside a stated floor | “Doorway clearance is 850mm when the door is in the open 90 degree posi” | 2 |  |
| pair-2.10-1800-1100 | pairing |  |  | <extraction_id of parked 2.10-1800> → <extraction_id of parked 2.10-1100> | no relation kind states a recommended figure beside a stated floor | “Corridors should be 1100mm/43” (recommend 1800mm/71”)” | not run |  |
| pair-6.1-1in16-1in12 | pairing |  |  | <extraction_id of parked 6.1-1in16> → <extraction_id of parked 6.1-1in12> | no relation kind states a recommended figure beside a stated floor | “Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)” | not run |  |

Item 6.2's "With the ramp at any point shall not be less than 1500mm/60”" is decided once (F9): its sentence has no subject noun, so what the 1500 mm measures cannot be settled on this source; it is an observation adjudicated `DEFERRED` with that reason and is neither written nor parked. Figures for quantities with no parameter (threshold rise, landing length, stall size, stair rise and run, handrail height and diameter, control, phone, counter, sign and fountain heights, elevator car sizes, door dwell time) are observations only.

## 4. Observations, by latest adjudication

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where o.ref_id='REF-01037' group by 1`

| outcome | observations |
|---|---|
| DEFERRED | 106 |
| NAMES-EXISTING | 25 |
| NOT-OURS | 1 |

Every observation:
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select o.observation_id, o.locator, o.surface_form, l.outcome, coalesce(l.term_id,''), substr(l.rationale,1,110) from observed_terms o join latest l using(observation_id) where o.ref_id='REF-01037' order by o.observation_id`

| obs | locator | surface form (as printed) | outcome | term | rationale (start) |
|---|---|---|---|---|---|
| 99 | PDF p. 1 | Universal Design | NAMES-EXISTING | TERM-017 | The source promotes the concepts of Universal Design; TERM-017 universal design is "Design usable by all peopl |
| 100 | PDF p. 1 | wider turning radius | NAMES-EXISTING | TERM-003 | The space a wheelchair or scooter needs to turn; TERM-003 turning circle (parameter 5) is the space for wheelc |
| 101 | PDF p. 1 | wider doors | NAMES-EXISTING | TERM-021 | The width of doors as the source contrasts it with the minimum standards; TERM-021 door width (parameter 9). |
| 102 | PDF p. 1 | Strollers for children | NOT-OURS |  | A real phrase, not one of the project's concepts: strollers are not a disability group or an access need. The  |
| 103 | PDF p. 1 | people with low vision | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as BLIND ('bli |
| 104 | PDF p. 1 | mobility devices | NAMES-EXISTING | TERM-079 | The source names "different mobility devices (scooters/ walkers/wheelchairs)"; TERM-079 mobility aid is a "Dev |
| 105 | PDF p. 1 | Physical Access | DEFERRED |  | An access category label, naming no single identity group or access need held in the registries. The four acce |
| 106 | PDF p. 1 | Deaf or Hard of Hearing Access | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as DEAF ('Deaf |
| 107 | PDF p. 1 | Blind or Low Vision Access | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as BLIND ('bli |
| 108 | PDF p. 1 | Cognitive Limitations Access | DEFERRED |  | An access category label naming cognitive access; no single identity code holds "cognitive limitations" (ID, B |
| 109 | PDF p. 2, item 1.1 | barrier-free parking spaces | NAMES-EXISTING | TERM-027 | Designated barrier-free parking spaces; TERM-027 accessible parking is "Designated parking for disabled driver |
| 110 | PDF p. 2, item 1.2 | Barrier-free unobstructed path of travel | DEFERRED |  | OT-1 and OT-2 place the owner's term 'Barrier-free path of travel' as a circulation route through a building,  |
| 111 | PDF p. 2, item 1.2 | minimum width | DEFERRED |  | The width of the item 1.2 path. Not adjudicated to TERM-002 corridor width while the owner has not said which  |
| 112 | PDF p. 2, item 1.2 | colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 113 | PDF p. 2, item 1.3 | Curb ramp | NAMES-EXISTING | TERM-089 | A curb ramp is an inclined surface built as a discrete element to bridge a level difference on a route; TERM-0 |
| 114 | PDF p. 2, item 1.4 | Access aisle painted on pavement | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 115 | PDF p. 2, item 1.5 | Accessible parking symbols | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 116 | PDF p. 2, item 1.6 | Vertically mounted sign | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 117 | PDF p. 2, item 1.7 | Number of designated accessible parking spaces per number of parking stalls | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 118 | PDF p. 2, item 1.8 | access aisle | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 119 | PDF p. 2, item 1.8 | clear height | NAMES-EXISTING | TERM-061 | An unobstructed vertical dimension above a route; TERM-061 headroom clearance (parameter 11). |
| 120 | PDF p. 2, item 1.9 | directional signs | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 121 | PDF p. 3, item 1.10 | clear accessible path | DEFERRED |  | A route between the stalls and the payment machine. Which route term this document's paths name is before the  |
| 122 | PDF p. 3, item 1.11 | Information for parking payment | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 123 | PDF p. 3, item 2.1 | Barrier-free path of travel | DEFERRED |  | OT-1 and OT-2 place the owner's term 'Barrier-free path of travel' as a circulation route through a building,  |
| 124 | PDF p. 3, item 2.2 | Signage at all non-accessible entrances | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 125 | PDF p. 3, item 2.3 | Doorway clearance | NAMES-EXISTING | TERM-021 | The clear opening of a doorway with the door open to 90 degrees; TERM-021 door width (parameter 9). |
| 126 | PDF p. 3, item 2.4 | Door operating device | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 127 | PDF p. 3, item 2.4 | tight grasping or twisting of the wrist | NAMES-EXISTING | TERM-088 | The clause names a grip and a wrist movement the door hardware must not demand; TERM-088 upper limb function a |
| 128 | PDF p. 3, item 2.4 | lever handles | NAMES-EXISTING | TERM-004 | TERM-004 lever handle is "Door handle operable without grip/twist motion", which is what the clause asks for.  |
| 129 | PDF p. 3, item 2.5 | automatic sliding doors | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 130 | PDF p. 3, item 2.6 | pedestrian entrances | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 131 | PDF p. 3, item 2.7 | vestibule | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 132 | PDF p. 3, item 2.8 | Automatic door operator button | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 133 | PDF p. 3, item 2.9 | doorway threshold | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 134 | PDF p. 3, item 2.10 | Colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 135 | PDF p. 3, item 2.10 | Corridors should be 1100mm/43” | NAMES-EXISTING | TERM-002 | The width of corridors; TERM-002 corridor width (parameter 4). |
| 136 | PDF p. 4, item 3.1 | assistive listening devices | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 137 | PDF p. 4, item 3.2 | Signage available in symbol form | NAMES-EXISTING | TERM-019 | Signage in symbol form; TERM-019 pictogram signage is "Simplified graphic symbols for wayfinding". TERM-019 (p |
| 138 | PDF p. 4, item 3.2 | those with visual processing difficulties or who are unable to read | DEFERRED |  | A group named by two functions (visual processing; reading), not an element or a quantity. No identity code ho |
| 139 | PDF p. 4, item 3.3 | braille | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 140 | PDF p. 4, item 3.3 | high colour contrast tactile lettering | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 141 | PDF p. 4, item 3.4 | way-finding signage | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 142 | PDF p. 4, item 3.5 | Braille signage | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 143 | PDF p. 4, item 3.6 | Signage font in Sans Serif | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 144 | PDF p. 4, item 3.6 | Signage should be 1350mm/51” high from floor level | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 145 | PDF p. 4, item 3.6 | tactile signage | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 146 | PDF p. 4, item 4.1 | Slip-resistant | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 147 | PDF p. 4, item 4.1 | tactile finish or strips | NAMES-EXISTING | TERM-010 | A tactile finish or strips on landings, nosings and at the ends of a ramp; TERM-010 is a "Ground surface detec |
| 148 | PDF p. 4, item 4.1 | tactile strips | NAMES-EXISTING | TERM-010 | Strips indicating a change in elevation at a stairwell; TERM-010 is a "Ground surface detectable by foot or ca |
| 149 | PDF p. 4, item 4.2 | Step demarcation in yellow | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 150 | PDF p. 4, item 4.3 | rise between 125mm/5” and 180mm/7” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 151 | PDF p. 4, item 4.3 | run of not less than 280mm/11” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 152 | PDF p. 4, item 4.3 | Avoid single isolated steps | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 153 | PDF p. 4, item 4.4 | Illumination | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 154 | PDF p. 4, item 4.5 | open area beneath the stairs | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 155 | PDF p. 4, item 4.5 | Tactile strips under the stairs on the ground | NAMES-EXISTING | TERM-010 | Tactile strips on the ground under the stairs, to alert a hazard; TERM-010 is a "Ground surface detectable by  |
| 156 | PDF p. 4, item 4.5 | contrasting colour on the back of the stairwell | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 157 | PDF p. 5, item 4.6 | Carpet | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 158 | PDF p. 5, item 4.7 | handrails on both sides | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 159 | PDF p. 5, item 4.7 | colour contrast from wall and surrounding environment | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 160 | PDF p. 5, item 4.8 | tactile cues | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 161 | PDF p. 5, item 5.1 | clear colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 162 | PDF p. 5, item 5.2 | Location of elevators | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 163 | PDF p. 5, item 5.3 | turning radius | NAMES-EXISTING | TERM-003 | The source calls a 1500 x 1500 mm car the space for a turning radius; TERM-003 turning circle (parameter 5) is |
| 164 | PDF p. 5, item 5.3 | elevator door at least 910 – 915mm/36” wide | NAMES-EXISTING | TERM-021 | The clear width of an elevator door; TERM-021 door width (parameter 9). |
| 165 | PDF p. 5, item 5.3 | stretcher | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 166 | PDF p. 5, item 5.4 | Elevator buttons and emergency controls mounted at an accessible height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 167 | PDF p. 5, item 5.5 | large print tactile numbers and Braille | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 168 | PDF p. 5, item 5.5 | Colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 169 | PDF p. 5, item 5.6 | Braille and tactile numbers | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 170 | PDF p. 5, item 5.7 | Visual indicator in elevators | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 171 | PDF p. 5, item 5.8 | Audible communication system | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 172 | PDF p. 5, item 5.9 | Elevator waiting areas should have seating | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 173 | PDF p. 5, item 5.10 | Elevator doors shall begin to close | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 174 | PDF p. 6, item 6.1 | Ramps | NAMES-EXISTING | TERM-089 | TERM-089 ramp, declined as a parameter (an element). |
| 175 | PDF p. 6, item 6.1 | Preferred maximum slope | NAMES-EXISTING | TERM-001 | The slope of a ramp; TERM-001 ramp gradient (parameter 3). |
| 176 | PDF p. 6, item 6.2 | With the ramp at any point | DEFERRED |  | The sentence as printed has no subject noun, so what its 1500 mm measures (a ramp width is the likeliest readi |
| 177 | PDF p. 6, item 6.2 | clearspace between handrails | NAMES-EXISTING | TERM-002 | The clear width of a ramp between its handrails; TERM-002 corridor width (parameter 4), which already holds a  |
| 178 | PDF p. 6, item 6.2 | Level landings/ resting areas provided at 9m/10yd intervals along ramp | NAMES-EXISTING | TERM-091 | The interval between landings along a ramp is the length of a flight between landings; TERM-091 ramp run lengt |
| 179 | PDF p. 6, item 6.3 | tight turns or switch-backs | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 180 | PDF p. 6, item 6.4 | 15mm/0.6” wide strip | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 181 | PDF p. 6, item 6.4 | Strong colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 182 | PDF p. 6, item 6.5 | able to open doors without backing onto ramp | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 183 | PDF p. 6, item 6.5 | Landings must be min 1200mm/47”long | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 184 | PDF p. 6, item 7.1 | diameter | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 185 | PDF p. 6, item 7.1 | handrails on both sides | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 186 | PDF p. 6, item 7.2 | contrasting colour | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 187 | PDF p. 6, item 7.3 | Handrails provided at two heights | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 188 | PDF p. 6, item 7.3 | Handrail height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 189 | PDF p. 6, item 7.4 | Handrails extend horizontally | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 190 | PDF p. 7, item 8.1 | wave to open or push button | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 191 | PDF p. 7, item 8.2 | only one turn with clear corner | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 192 | PDF p. 7, item 8.2 | persons who are blind | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as BLIND ('bli |
| 193 | PDF p. 7, item 8.3 | Proper signage | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 194 | PDF p. 7, item 8.4 | located around perimeter | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 195 | PDF p. 7, item 8.5 | knee space | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 196 | PDF p. 7, item 8.5 | soap and towel dispenser | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 197 | PDF p. 7, item 8.5 | low mounted or tilt mirror | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 198 | PDF p. 7, item 8.5 | insulate any exposed pipes | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 199 | PDF p. 7, item 8.5 | Automatic or sensor operated faucets | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 200 | PDF p. 7, item 8.6 | ACCESSIBLE WASHROOM STALL | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 201 | PDF p. 7, item 8.6 | minimum 1700mm x 1500mm/70 x 60” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 202 | PDF p. 7, item 8.6 | person with limited mobility | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as MOB ('disab |
| 203 | PDF p. 7, item 8.6 | grab bars | NAMES-EXISTING | TERM-008 | TERM-008 grab bar is a "Support rail for transfer and balance in bathrooms". TERM-008 (grab bar) is held and i |
| 204 | PDF p. 7, item 8.6 | large, sliding latch (not thumb-turning) | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 205 | PDF p. 7, item 8.6 | toilet paper reachable without leaning too far off toilet | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 206 | PDF p. 7, item 8.6 | accessible toilet height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 207 | PDF p. 7, item 8.6 | various toilet size and heights | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 208 | PDF p. 7, item 8.6 | vertically mounted grab bar | NAMES-EXISTING | TERM-008 | A grab bar at a urinal; TERM-008 grab bar is a "Support rail for transfer and balance in bathrooms". TERM-008  |
| 209 | PDF p. 7, item 8.6 | Call buttons | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 210 | PDF p. 7, item 8.7 | gender inclusive/family washroom | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 211 | PDF p. 8, item 9.1 | Public and emergency phones | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 212 | PDF p. 8, item 9.2 | TTY | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 213 | PDF p. 8, item 9.2 | users who are Deaf or hard of hearing | DEFERRED |  | A group of disabled people, not an element or a quantity. The identity registry holds the group as DEAF ('Deaf |
| 214 | PDF p. 8, item 9.2 | live captioning | NAMES-EXISTING | TERM-025 | A live captioning app; TERM-025 captioning is "Real-time text display of speech". TERM-025 (captioning) is hel |
| 215 | PDF p. 8, item 9.3 | drinking fountain | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 216 | PDF p. 8, item 9.4 | One accessible section of counter | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 217 | PDF p. 8, item 9.4 | barrier-free counter surface | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no term or parameter for it. Whether a source t |
| 218 | PDF p. 8, item 9.5 | Shelving, coat hooks and light switches | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 219 | PDF p. 8, item 9.6 | variety of seating options | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 220 | PDF p. 8, item 9.6 | seats with a variety of widths, adjustable armrests and backrests | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 221 | PDF p. 8, item 9.7 | Level wheelchair seating area | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 222 | PDF p. 8, item 9.8 | contrasting strip of colour | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 223 | PDF p. 8, item 9.9 | Hearing loops | NAMES-EXISTING | TERM-006 | TERM-006 hearing loop is an "Audio frequency induction loop system for hearing aid users". TERM-006 (hearing l |
| 224 | PDF p. 8, item 10.1 | audible and visual signal | DEFERRED |  | The source requires an audible and a visual signal on all alarm systems. Whether this names TERM-013 visual fi |
| 225 | PDF p. 9, item 11.1 | detectable by someone who uses a cane | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 226 | PDF p. 9, item 11.1 | someone who uses a cane | DEFERRED |  | A group named by its device, not an element or a quantity. Which group cannot be settled on this source alone: |
| 227 | PDF p. 9, item 11.2 | good colour contrast | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 228 | PDF p. 9, item 11.2 | grey colours should be avoided | DEFERRED |  | The source asks for colour contrast and states no figure and no measure. Whether this colour contrast names TE |
| 229 | PDF p. 9, item 11.3 | Variety of benches | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |
| 230 | PDF p. 9, item 11.4 | quiet space | DEFERRED |  | An element or provision the source requires, with no figure; the catalogue holds no term for it. This batch mi |

Item coverage against `items.json`: 75 numbered items, items with no observation: none (computed by this script).

**R16 is red, deliberately (F2).** A phrase that names a held term is adjudicated `NAMES-EXISTING` to it; R16 then requires the term to be a parameter or declined, and this batch does neither (OD-53 asks whether a single-source batch may decline). The terms:
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select distinct a.term_id, t.canonical_en from term_adjudications a join observed_terms o using(observation_id) join terms t using(term_id) where o.ref_id='REF-01037' and not exists (select 1 from base_parameters p where p.term_id=a.term_id) and not exists (select 1 from parameter_declinations d where d.term_id=a.term_id and d.revoked_at is null) order by 1`

| term | name |
|---|---|
| TERM-004 | lever handle |
| TERM-006 | hearing loop |
| TERM-008 | grab bar |
| TERM-010 | tactile walking surface indicator |
| TERM-017 | universal design |
| TERM-019 | pictogram signage |
| TERM-025 | captioning |
| TERM-027 | accessible parking |
| TERM-079 | mobility aid |
| TERM-088 | upper limb function and grip |

## 5. Which groups the document reaches, and what reached a row
The groups the document's own words name are observations of their own (F7):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select o.locator, o.surface_form, l.outcome, coalesce(l.term_id,'') from observed_terms o join latest l using(observation_id) where o.ref_id='REF-01037' and (o.surface_form like '%blind%' or o.surface_form like '%Deaf%' or o.surface_form like '%low vision%' or o.surface_form like '%Low Vision%' or o.surface_form like '%cane%' or o.surface_form like '%mobility%' or o.surface_form like '%read%' or o.surface_form like '%Access' or o.surface_form like '%Strollers%') order by o.observation_id`

| locator | group phrase as printed | outcome | term |
|---|---|---|---|
| PDF p. 1 | Strollers for children | NOT-OURS |  |
| PDF p. 1 | people with low vision | DEFERRED |  |
| PDF p. 1 | mobility devices | NAMES-EXISTING | TERM-079 |
| PDF p. 1 | Physical Access | DEFERRED |  |
| PDF p. 1 | Deaf or Hard of Hearing Access | DEFERRED |  |
| PDF p. 1 | Blind or Low Vision Access | DEFERRED |  |
| PDF p. 1 | Cognitive Limitations Access | DEFERRED |  |
| PDF p. 4, item 3.2 | those with visual processing difficulties or who are unable to read | DEFERRED |  |
| PDF p. 7, item 8.2 | persons who are blind | DEFERRED |  |
| PDF p. 7, item 8.6 | person with limited mobility | DEFERRED |  |
| PDF p. 8, item 9.2 | users who are Deaf or hard of hearing | DEFERRED |  |
| PDF p. 9, item 11.1 | detectable by someone who uses a cane | DEFERRED |  |
| PDF p. 9, item 11.1 | someone who uses a cane | DEFERRED |  |
What reached a row, by lens code:
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select coalesce(l.identity_code, l.needs_code, l.icf_code) code, count(distinct e.extraction_id), group_concat(distinct e.parameter_id) from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.ref_id='REF-01037' group by 1 order by 1`

| lens code | extractions | parameters |
|---|---|---|
| A-EFFORT | 1 | 12 |
| A-REACH | 6 | 9,5 |
| MOB | 6 | 9,5 |
| d440 | 1 | 6 |
| d445 | 1 | 6 |
| d465 | 6 | 9,5 |
Stated plainly: **this source's blind, low-vision, Deaf, hard-of-hearing, cognitive and quiet-space content reached no extraction.** It reached rows only as observations adjudicated `DEFERRED` (the group phrases; colour contrast; braille, tactile and audible provisions; signage in symbol form for "those with visual processing difficulties or who are unable to read"; the quiet space) or `NAMES-EXISTING` to element terms the catalogue holds as neither parameter nor declined (hearing loop, captioning, pictogram signage, tactile walking surface indicator). Every extraction is a mobility, reach, effort or hand-function figure. A group phrase cannot be adjudicated to its identity code (an adjudication names only a term, and the catalogue holds no term for these groups), so DEFERRED is the only outcome that fits; the four access category names stand in white text on page 1 and are not visible on the render.

## 6. Cells (the engine, once per cell, after every write)

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select specification_id, parameter_id, coalesce(identity_code, needs_code, icf_code), state, design_scale, regulatory_stratum_only, code_floor_only, gap_register_id from specifications where created_by_session='session_2026-11-13-edmonton-checklist-pass' order by 1`

| spec | parameter | lens | state | design_scale | regulatory_stratum_only | code_floor_only | gap (engine-written) |
|---|---|---|---|---|---|---|---|
| 9 | 5 | MOB | pending | universal | 1 | 1 | GAP-118 |
| 10 | 5 | A-REACH | pending | population | 0 | 0 | GAP-119 |
| 11 | 5 | d465 | pending | population | 0 | 0 | GAP-120 |
| 12 | 9 | MOB | pending | universal | 1 | 1 | GAP-121 |
| 13 | 9 | A-REACH | pending | population | 0 | 0 | GAP-122 |
| 14 | 9 | d465 | pending | population | 0 | 0 | GAP-123 |
| 15 | 12 | A-EFFORT | pending | population | 0 | 0 | GAP-124 |
| 16 | 6 | d440 | pending | population | 0 | 0 | GAP-125 |
| 17 | 6 | d445 | pending | population | 0 | 0 | GAP-126 |
Per cell, from this run's own counts and the engine's `--report-json` (`/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay3/emit/cell-<parameter>-<code>.json`), not from the gap sentence. In-lens rows:
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select e.ref_id, s.tier, s.evidence_type, e.figure_role, e.extraction_method, count(*) from source_value_extractions e join v_live_lens_links l using(extraction_id) join evidence_sources s using(ref_id) where e.parameter_id=? and l.<lens column>=? group by 1,2,3,4,5`

| cell | distinct in-lens sources | in-lens rows (ref, tier, type, role/method, n) | engine n_sources | engine source_records | skimmed_findings | excluded_not_publishable | needs_population_assessment | gap sentence says |
|---|---|---|---|---|---|---|---|---|
| 5 × MOB | 5 | REF-00139 T6 code claim/full-read ×2; REF-00468 T3 grey finding/skim ×2; REF-00987 T6 code claim/skim ×1; REF-01031 T6 code claim/skim ×1; REF-01037 T3 grey claim/full-read ×1; REF-01037 T3 grey finding/full-read ×1 | 2 | REF-00139 T6 code pop=PROXY cond=NON-ANCHORING tier_consistent=True; REF-01037 T3 grey pop=PROXY cond=DOWN-WEIGHTED tier_consistent=True | [193, 194] | [183, 211] |  | from 2 source(s); "disqualified, or tier not derivable" |
| 5 × A-REACH | 1 | REF-01037 T3 grey claim/full-read ×1; REF-01037 T3 grey finding/full-read ×1 | 1 | REF-01037 T3 grey pop=NOT_ASSESSED cond=DOWN-WEIGHTED tier_consistent=True |  |  | ['REF-01037'] | from 1 source(s); "disqualified, or tier not derivable" |
| 5 × d465 | 1 | REF-01037 T3 grey claim/full-read ×1; REF-01037 T3 grey finding/full-read ×1 | 1 | REF-01037 T3 grey pop=NOT_ASSESSED cond=DOWN-WEIGHTED tier_consistent=True |  |  | ['REF-01037'] | from 1 source(s); "disqualified, or tier not derivable" |
| 9 × MOB | 5 | REF-00139 T6 code claim/full-read ×1; REF-00468 T3 grey claim/skim ×1; REF-00987 T6 code claim/skim ×1; REF-01031 T6 code claim/skim ×1; REF-01037 T3 grey claim/full-read ×3; REF-01037 T3 grey finding/full-read ×1 | 2 | REF-00139 T6 code pop=PROXY cond=NON-ANCHORING tier_consistent=True; REF-01037 T3 grey pop=PROXY cond=DOWN-WEIGHTED tier_consistent=True |  | [185, 216, 224] |  | from 2 source(s); "disqualified, or tier not derivable" |
| 9 × A-REACH | 1 | REF-01037 T3 grey claim/full-read ×3; REF-01037 T3 grey finding/full-read ×1 | 1 | REF-01037 T3 grey pop=NOT_ASSESSED cond=DOWN-WEIGHTED tier_consistent=True |  |  | ['REF-01037'] | from 1 source(s); "disqualified, or tier not derivable" |
| 9 × d465 | 1 | REF-01037 T3 grey claim/full-read ×3; REF-01037 T3 grey finding/full-read ×1 | 1 | REF-01037 T3 grey pop=NOT_ASSESSED cond=DOWN-WEIGHTED tier_consistent=True |  |  | ['REF-01037'] | from 1 source(s); "disqualified, or tier not derivable" |
| 12 × A-EFFORT | 2 | REF-01033 T1 clinical finding/skim ×1; REF-01037 T3 grey claim/full-read ×1 | 1 | REF-01037 T3 grey pop=NOT_ASSESSED cond=DOWN-WEIGHTED tier_consistent=True | [167] |  | ['REF-01037'] | from 1 source(s); "disqualified, or tier not derivable" |
| 6 × d440 | 1 | REF-01037 T3 grey finding/full-read ×1 | 0 | (none gathered) |  |  |  | (no source count); "NONE COUNTS" |
| 6 × d445 | 1 | REF-01037 T3 grey finding/full-read ×1 | 0 | (none gathered) |  |  |  | (no source count); "NONE COUNTS" |

What each cell actually is:
- **5 × MOB and 9 × MOB.** Five distinct sources hold rows in each lens; two are grey tier 3 (REF-00468 and REF-01037) and three are tier-6 codes. The engine gathers two "sources" (REF-00139 and REF-01037): the codes REF-00987 and REF-01031 hold only skimmed rows (`excluded_not_publishable`), and REF-00468's parameter-5 rows are skimmed findings (`skimmed_findings`) while its parameter-9 row is a skimmed claim. Nothing is disqualified: every source record reads `tier_consistent true`; REF-01037 is `DOWN-WEIGHTED`, REF-00139 `NON-ANCHORING`. No anchor exists, no T3-clinical source exists, and a T4-6 source is present, so the engine's regulatory branch ran and wrote `regulatory_stratum_only = 1`, `code_floor_only = 1` and `design_scale = universal` although a grey tier-3 source is in the lens; the cell is still `pending` because the branch found the regulatory evidence not rich enough and parameters 5 and 9 have no direction.
- **5 × A-REACH, 5 × d465, 9 × A-REACH, 9 × d465.** REF-01037 alone. `population_directness NOT_ASSESSED`: the population match writer takes an identity only (`evidence_population_match.target_population` references `base_taxonomy_identity`), so no match row can reach a need or ICF cell. Pending; no direction.
- **12 × A-EFFORT.** Two sources: REF-01033 (tier 1, clinical) holds a finding the engine lists in `skimmed_findings` and leaves out (it owes a dedicated reading), and REF-01037's 9 m ceiling, `NOT_ASSESSED` for the same reason. Parameter 12 has a direction (`lower_is_better`); the cell is pending because its one value-supplying source is grey tier 3.
- **6 × d440 and 6 × d445.** Only REF-01037's absent finding; `n_sources = 0`. The engine's text here ("NONE COUNTS: none states a value") is true.

**Which gap sentences are untrue.** In the seven cells whose text says "none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope)", that cause is untrue: no source is disqualified and every one is tier-consistent; the cause is that the only value-supplying sources are a grey tier-3 checklist and (in the MOB cells) one code. In the two MOB cells "from 2 source(s)" understates five in-lens sources (it counts gathered value-supplying sources). The regulatory flags of the MOB cells say the cell rests on codes only while a grey source is in the lens. The gap texts are in the batch as the engine wrote them; the defect is gap GAP-105 (rule 10: not patched).

## 7. Coverage reads (ADJUDICATION section 3)

**Lens by parameter, identity lens** (live value-supplying figures per code and active parameter, zeros included):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select identity_code from base_taxonomy_identity where status='active' order by 1 ; cross select l.identity_code code, e.parameter_id, count(distinct e.extraction_id) n from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.figure_role in ('claim','derived') and l.identity_code is not null group by 1,2`

| identity | p3 | p4 | p5 | p6 | p7 | p8 | p9 | p10 | p11 | p12 |
|---|---|---|---|---|---|---|---|---|---|---|
| ADHD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ALL | 0 | 9 | 2 | 2 | 0 | 0 | 12 | 0 | 5 | 0 |
| AUT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BAR | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BLIND | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| BRAIN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| COM | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DEAF | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DEAFBLIND | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DEM | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| EPI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ID | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LMB | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LPA | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MH | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MOB | 46 | 10 | 5 | 8 | 0 | 0 | 7 | 0 | 2 | 20 |
| MOVE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| NDV | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PAIN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SCI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| TALL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| VES | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Lens by parameter, access need lens** (live value-supplying figures per code and active parameter, zeros included):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select need_code from access_needs order by 1 ; cross select l.needs_code code, e.parameter_id, count(distinct e.extraction_id) n from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.figure_role in ('claim','derived') and l.needs_code is not null group by 1,2`

| access need | p3 | p4 | p5 | p6 | p7 | p8 | p9 | p10 | p11 | p12 |
|---|---|---|---|---|---|---|---|---|---|---|
| A-AT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-CALM | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-EFFORT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| A-LOWLOAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-NOSIGHT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-NOSOUND | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-NOSPEECH | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-PLAIN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-PRECISION | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-REACH | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| A-SELFCARE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-SIZE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-STABLE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-STIMULUS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TACTILE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TIME | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TRIGGER | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**ICF lens** (value-supplying figures): [('d465', 5, 1), ('d465', 9, 3)]; codes with none: `select count(*) from base_icf` minus that → 71. The d440/d445 links sit on an absent finding, not a value. Medical lens rows: `select count(*) from base_taxonomy_medical` → 0.
**Lens by figure**: value-supplying figures whose only live links are identities, every one `ALL` or a parent code: 127; of them REF-01037's: 0.
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select e.extraction_id, e.ref_id, e.parameter_id from source_value_extractions e join v_live_lens_links l using(extraction_id) where e.figure_role in ('claim','derived') group by 1 having sum(l.identity_code is null)=0 and sum(l.identity_code='ALL' or l.identity_code in (select identity_code from base_taxonomy_identity where parent_code is null))=count(*)`

**Words without a parameter** (observations whose latest adjudication is DEFERRED, NOT-OURS or absent; top rows):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select o.ref_id, coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where coalesce(l.outcome,'UNADJUDICATED') in ('DEFERRED','NOT-OURS','UNADJUDICATED') group by 1,2 order by 3 desc limit 8`

| ref | outcome | observations |
|---|---|---|
| REF-01037 | DEFERRED | 106 |
| REF-00977 | NOT-OURS | 3 |
| REF-00468 | DEFERRED | 2 |
| REF-00990 | DEFERRED | 2 |
| REF-00994 | NOT-OURS | 2 |
| REF-00998 | DEFERRED | 2 |
| REF-00999 | DEFERRED | 2 |
| REF-01000 | NOT-OURS | 2 |

## 8. Gaps filed (the engine's included)

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select gap_id, category, priority, substr(description,1,150) from gaps where created_by_session='session_2026-11-13-edmonton-checklist-pass' order by 1`

| gap | cat | pri | description (start) |
|---|---|---|---|
| GAP-103 | SW | P3 | log-search demands a subject (--slug, --parameter or --mined-ref-id) even for --origin owner-supplied, where no search ran. The owner-supplied admissi |
| GAP-104 | SW | P3 | log-mining cannot record a deferred forward (cited-by) direction once a backward pass has set evidence_sources.citation_mining_status to mined: the wr |
| GAP-105 | SW | P2 | The engine (scripts/assess/assess_cell.py, gap_account) writes into a pending cell's gap text three things a reader takes as facts and that are not: ( |
| GAP-106 | SW | P3 | No sanctioned writer holds the basis of evidence_sources.pub_year, and add-source takes no notes: add-source has no flag for pub_year_note, amend-sour |
| GAP-107 | SW | P3 | raise-follow-up accepts only two reasons (absence-needs-tested-value, read-outside-admitting-purpose), so an extraction whose printed figure is ambigu |
| GAP-108 | EG | P2 | R7: harms or hazards REF-01037 states, tied to no held parameter, in the source's own words: item 1.5 "The more painted surface, the more likely pavem |
| GAP-109 | DEC | P2 | OD-47 (open): what lens a figure carries when its clause names no person, function or need. REF-01037 figures whose clause names no one are NOT writte |
| GAP-110 | EG | P2 | Accessibility direction for parameters 5 (turning circle) and 9 (door width) is not set (select parameter_id from base_parameters where accessibility_ |
| GAP-111 | EG | P2 | R4: REF-01037 phrases adjudicated DEFERRED have no reader yet (T-079's v_deferred_acts is to gain an adjudication arm). Each rationale says why it is  |
| GAP-112 | EG | P3 | REF-01037 is a City of Edmonton document and its figures are recorded under country code CA: base_jurisdictions holds no sub-national code for Alberta |
| GAP-113 | RP | P2 | Backward-mining leads named by REF-01037 and staged REFERENCE-ONLY, not retrieved: the Safety Codes Council Barrier-Free Design Guide (Aug 2019 PDF),  |
| GAP-114 | SW | P3 | REF-01037 text defects as printed, recorded without correction: item 6.2 "With the ramp at any point shall not be less than 1500mm/60”" has no subject |
| GAP-115 | SW | P2 | No relation kind in extraction_relations.relation states a source's pairing of a higher figure it recommends with the floor (or a stricter ceiling wit |
| GAP-116 | EG | P2 | The Co-1, Tier 2 and Co-2 pass for the topic of slug stair-ramp-threshold-biomechanics-accessibility (and the other four slugs REF-01037 is linked to) |
| GAP-117 | DEC | P2 | R16 is red for the REF-01037 batch, deliberately: observations that name a held term which is neither a parameter nor declined are adjudicated NAMES-E |
| GAP-118 | EG | P2 | Evidence gap (parameter-scoped): 8 extraction(s) of parameter 5 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qu |
| GAP-119 | EG | P2 | Evidence gap (parameter-scoped): 2 extraction(s) of parameter 5 stated in the lens (needs_code=A-REACH), from 1 source(s), but none of those sources q |
| GAP-120 | EG | P2 | Evidence gap (parameter-scoped): 2 extraction(s) of parameter 5 stated in the lens (icf_code=d465), from 1 source(s), but none of those sources qualif |
| GAP-121 | EG | P2 | Evidence gap (parameter-scoped): 8 extraction(s) of parameter 9 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qu |
| GAP-122 | EG | P2 | Evidence gap (parameter-scoped): 4 extraction(s) of parameter 9 stated in the lens (needs_code=A-REACH), from 1 source(s), but none of those sources q |
| GAP-123 | EG | P2 | Evidence gap (parameter-scoped): 4 extraction(s) of parameter 9 stated in the lens (icf_code=d465), from 1 source(s), but none of those sources qualif |
| GAP-124 | EG | P2 | Evidence gap (parameter-scoped): 2 extraction(s) of parameter 12 stated in the lens (needs_code=A-EFFORT), from 1 source(s), but none of those sources |
| GAP-125 | EG | P2 | Evidence gap (parameter-scoped): 1 extraction(s) of parameter 6 stated in the lens (icf_code=d440), but NONE COUNTS: none states a value, and every fi |
| GAP-126 | EG | P2 | Evidence gap (parameter-scoped): 1 extraction(s) of parameter 6 stated in the lens (icf_code=d445), but NONE COUNTS: none states a value, and every fi |

Gap ids were assigned by the writer on this fresh copy (this run's own keys to ids: `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay3/gap-ids.json`); they do not mean what earlier runs' ids meant. Leads: `select ref_id, title from source_locators where recovered_from like 'REF-01037%'`. Backward mining recorded; the forward pass was not run (an owner-supplied, from-evidence batch), no probe was made, and its deferral was refused by the writer (gap GAP-104).

## 9. Checks, run once after the engine
Full output: `scratchpad/session_2026-11-13-edmonton-checklist-pass/checks-after-engine-v3.txt`.
```
===== scripts/audit/research_batch_dod.py --session session_2026-11-13-edmonton-checklist-pass
==============================================================================
==============================================================================
  R1: PASS — 0 co1/co2-targeted searches, 0 co1/co2 sources, 1 reasoned waivers
  R5: PASS — EXAMINED: 0 non-English admissions, so this asserts nothing. REPORTED, not asserted: 0 admission(s) waived by 'R5-GREY-WARRANTED:' in grey_reason; 0 non-English search(es) targeted 'grey' (a target is what was sought, not how a source was filed); 
  R7: PASS — EXAMINED: 1 search(es); every one screened no more than it found and admitted no more than it screened. REPORTED, not asserted: 0 candidate(s) registered for 1 screened; 1 row(s) carry harm_finding=1. Whether harm and off-slug material reached a r
  R10b: PASS — EXAMINED: 1 admitted source(s) carrying a URL; none left verification_status NULL
  R11: PASS — EXAMINED: 0 aliases. This batch wrote none, so this asserts nothing about the corpus
  R16-adjudicate: PASS — EXAMINED: 132 observation(s) on this batch's admissions; every one adjudicated
  R16-scan: PASS — EXAMINED: 1 admission(s); every one carries a catalogue-mode reading. Whether the reading saw everything is NOT tested here -- adversarial standing subject 4
  R17: PASS — EXAMINED: 1 admission(s); every one has a search behind it
  ✗ R16: 10 of 17 term(s) named by adjudications of this batch's observations hold neither a parameter nor a declination: TERM-004, TERM-006, TERM-008, TERM-010, TERM-017, TERM-019, TERM-025, TERM-027. A concept a source states a figure for is filed against a 
  NON-COMPLIANT: 1 rule(s) unmet.
  Per owner directive 2026-07-24: RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH
==============================================================================
exit=1
===== scripts/audit/judgment_handoff_shape.py
EXAMINED: 3 invariant(s) of the evidence->judgment hand-off
PASS: shape holds (source_value_extractions currently 222 rows — shape is checked, not content).
exit=0
===== scripts/audit/extraction_relations_integrity.py
EXAMINED: 281  (222 source_value_extractions row(s), 59 extraction_relations edge(s), 0 v_derived_figure_check row(s))
VERDICT: CLEAN
exit=0
===== scripts/audit/adjudication_integrity.py
======================================================================
======================================================================
======================================================================
EXAMINED: 60
VERDICT: PASS   (tier inconsistencies=0)
======================================================================
exit=0
===== scripts/audit/observation_verbatim_audit.py
EXAMINED: 228
PASS: no class above its baseline
exit=0
===== scripts/tests/test_db_integrity.py
  [✓] K01: every recorded derivation_sha verifies against its own row  (9 examined)
  [✓] K02: every determination written since migration 077 accounts for every extraction of its parameter  (9 examined)
======================================================================
RESULTS: 57/57 checks passed
PASSED HAVING EXAMINED NOTHING (8): B04, I3, I3b, B09, C10, C05, D02, G03
EXAMINED: 4009 subject-inspections across 49 instrumented check(s) of 57
======================================================================
exit=0
===== scripts/audit/derivation_handshake_integrity.py
======================================================================
======================================================================
EXAMINED: 10
VERDICT: CLEAN
exit=0
===== scripts/validate_evidence_state.py
PASS: 22 records checked, 0 errors, 0 warnings
EXAMINED: 22
exit=0
===== scripts/audit/verified_scan_integrity.py
EXAMINED: 220
FAIL: 140 (row, class) pair(s) across 220 live extraction(s); each class above names its remedy.
exit=1
===== scripts/audit/schema_reference_audit.py
EXAMINED: 1353 SQL identifier references in 188 files against 85 live tables and views
RESULT: PASS — every table and view a caller names exists
exit=0
```
`research_batch_dod` is red on R16 alone, for the 10 terms of section 4 (its message truncates the list at eight). `R1` passes on the waiver token: its predicate is `findings_note LIKE '%CO1-NOT-APPLICABLE%'` and does not read the reason (`grep -n "CO1-NOT-APPLICABLE%" scripts/audit/research_batch_dod.py`). `extraction_relations_integrity` is CLEAN and would have been CLEAN with the second run's reversed `exceeds` edge: it reads shape, not meaning. `verified_scan_integrity` is red with the same count on untouched canonical (`python3 scripts/audit/verified_scan_integrity.py`), and no line of its output here names REF-01037.

## 10. The second critic's findings F1 to F13 and the withheld W1 to W3
| | Disposition | Shown by |
|---|---|---|
| F1 | Done: no `exceeds` edge anywhere, none in a parked line; no relation kind fits the pairing (`exceeds` = referent more than needed; `delta_over` = an increment; `confirms` = an independent measurement), so 3 pairings are parked with the relation as a marked hole and gap GAP-115 names the missing kind and that `extraction_relations_integrity` checks shape, not meaning. Harm findings keep `insufficient`. | §2, §3 |
| F2 | Done: 10 terms adjudicated `NAMES-EXISTING` where the phrase names them; R16 is red and kept red (gap GAP-117); no decline. DEFERRED rationales now say why each is held; none cites AQ-7/OD-53 for what it does not ask. The conflict is in section 11. | §4 |
| F3 | Done: observations for item 4.5's hazard sentence, 6.5, 8.5 pipes, 11.2 grey colours, 4.3 isolated steps, 8.6 toilet paper; the R7 gap GAP-108 quotes only the source; the search note lists them. | §4; `select findings_note from search_executions where exec_id=204` |
| F4 | Done: one rule (the words must name the function or need). 2.4's absent finding written with ICF d440, d445 (no need definition names grip or wrist); 9 m keeps A-EFFORT, [ASSUMPTION] in its notes. | §2 |
| F5 | Done: A-REACH and d465 beside MOB on every page-1-warranted row, from the registries' own definitions; no link the words do not name. | §2 lens table |
| F6 | Done: population match PROXY for MOB (the only identity linked); a need or ICF cell cannot take one (its target is an identity), so it stays NOT_ASSESSED. Cells explained from counts and JSON; untrue gap sentences named; engine not patched (gap GAP-105). | §6 |
| F7 | Done: observations for 4.1's first sentence, 4.7's handrail contrast, 8.6's bullets, 9.6's seats, 7.3's two heights, 3.6's font, 8.5's faucets, 9.4's counter section, page 1's strollers (NOT-OURS) and four access categories (white text), and the six group phrases. Section 5 added. | §4, §5 |
| F8 | Done: the waiver now says only that this batch owes no search; gap GAP-116 records the topic pass not performed (EG, P2; `add-gap` has no `--slug`, so the slug is in its text). R1's substring predicate is a gate-design finding (section 11). | `select findings_note from search_executions where exec_id=204` |
| F9 | Done: each parked `notes` states what the page prints; 6.2's 1500 decided once (observation DEFERRED, not parked); parked lines and absent findings counted separately. | §3 |
| F10 | Done: no row cites a disposable database, an earlier run's gap id or "this replay"; precedents cite canonical rows by query; gap ids are the writer's from this run. | the text-column queries of section 12 |
| F11 | Done: no `publisher_location`; renders p0000 to p0008 read in this run and the methods say so; `pub_year` basis in gap GAP-106 (no writer takes notes), with the stamp said only to be on the URL and to decode to 2021-09-14. | `select publisher_location, lang_detection_method, verification_method from evidence_sources where ref_id='REF-01037'` |
| F12 | Done: magenta root basis as given. | §2 |
| F13 | Done: the forward pass is said only not to have been run and no probe made. | gap GAP-104 |
| W1 | Recorded: MOB kept on the page-1 sentence for the 850 mm it calls inadequate; [ASSUMPTION] in the notes; OD-47. | §2 |
| W2 | Recorded: item 1.2's "minimum width" adjudicated DEFERRED waiting on OD-52, not TERM-002. | §4 |
| W3 | Recorded: Co-1 standing not judged (OD-51); the source is grey. | §1 |

## 11. Conflicts between the rules, the adjudication and the writers
1. **R16 against DEFERRED.** R16 reads only adjudications that name a term (`a.term_id IS NOT NULL`, `grep -n 'undisposed = _rows' -A8 scripts/audit/research_batch_dod.py`); no gate, view or skill reads a DEFERRED row (`git grep -n -E "'DEFERRED'" -- scripts governance/check-registry.yaml ':!scripts/migrations'`). So the honest act (NAMES-EXISTING to an element term the catalogue holds undeclined) turns R16 red, and the dishonest one (DEFERRED with a reason that is not one) keeps it green. R16 also reads every adjudication, not the latest (no `max(adjudication_id)` in its join), so a later re-adjudication cannot clear an earlier one. And the plan's own OD-53 entry says T-087's observations naming such a term "are adjudicated DEFERRED, naming the term and this question, instead of NAMES-EXISTING" (`grep -n -F 'are adjudicated `DEFERRED`' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`): this run follows REPLAY-V3-BRIEF F2, which reverses that, so the plan text and this batch disagree.
2. **DEFERRED is the only outcome left for settled content this batch may not mint.** An element or quantity with no held term can be recorded only as NAMES-NEW (which needs a term, so `add-term`) or DEFERRED. With minting withheld, the rationale says DEFERRED records a withheld act, against the schema's "cannot be settled on this source alone". Likewise a group phrase has no term to name: the group is an identity code, and `term_adjudications.term_id` references `terms` only (`select sql from sqlite_master where name='term_adjudications'`).
3. **R1's substring.** `R1` passes on `findings_note LIKE '%CO1-NOT-APPLICABLE%'` whatever the reason says (`grep -n "CO1-NOT-APPLICABLE%" scripts/audit/research_batch_dod.py`); here it passes on a waiver that concedes the pass was not done.
4. **The relation vocabulary.** No kind for "a recommended figure beside a stated floor" (`select sql from sqlite_master where name='extraction_relations'`); `extraction_relations_integrity` checks shape, so a reversed meaning passes CLEAN (gap GAP-115).
5. **The engine's gap text** (gap GAP-105): "from N source(s)" counts gathered value-supplying sources; "disqualified, or tier not derivable" is printed for tier-consistent, down-weighted sources; the regulatory branch writes code-only flags with a grey source in the lens (`grep -n 'elif regulatory:' scripts/assess/assess_cell.py`).
6. **Population match against non-identity lenses.** A need or ICF cell's `population_directness` is always `NOT_ASSESSED`: `evidence_population_match.target_population` references `base_taxonomy_identity` (`select sql from sqlite_master where name='evidence_population_match'`).
7. **`add-gap` has no `--slug`** (`python3 scripts/db.py add-gap --help`), though the brief asked for one on the Co-1 pass gap; the slug is in the description.

## 12. What was not done
- No figure whose clause names no one was written (OD-47); no term minted, promoted or declined (OD-50, OD-53); the route phrases wait on OD-52; no direction set for parameters 5 and 9 (gap GAP-110).
- No Co-1, T2 or Co-2 pass (gap GAP-116); no lead retrieved; no forward citation pass.
- `pub_year`'s basis not written (no writer); `data_capture_status` not moved (no `db.py` verb writes it).
- `batch.sql` emitted, not applied; nothing committed; no adversarial pass on this run.
- Text-column self-check (F10): `select count(*) from source_value_extractions where ref_id='REF-01037' and (notes like '%this replay%' or notes like '%first run%' or notes like '%scratch database%')` → 0; the same over this session's gaps → 0; over this batch's adjudication rationales → 0.
