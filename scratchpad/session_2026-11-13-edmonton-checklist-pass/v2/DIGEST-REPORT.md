# Digest report, second run: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The replay wrote only what the rules allow while the owner's questions AQ-1 to AQ-8 are open: 7 extractions (5 value figures on parameters 5, 9, 12 with a lawful lens, 2 page-1 harm findings), 103 observations covering every numbered item and every printed figure, and no identity `ALL`, no promotion, no declination and no minted term; the figures whose clause names no one are parked as exact writer argv (10 lines, waiting on AQ-1), not written. The 3 cells the new lens links reach are pending (no in-lens source can anchor and parameters 5 and 9 have no direction); nothing is applied to the canonical database, whose sha256 did not move.

*Session `session_2026-11-13-edmonton-checklist-pass`, a research session, `from-evidence` variant (owner-supplied PDF). Replay of the first run on a fresh scratch copy of `data/guidebook.db` (`$SC` = `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay`), applying `ADJUDICATION.md` as `REPLAY-BRIEF.md` orders it. The first run's report, batch, cell reports and check outputs are in `v1/`. Every count below is printed with the query that produced it, run against `$SC/guidebook.db`; re-run rather than trust. Canonical sha256 before and after: `3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb`.*

---

## 1. Stages

| Stage | Done in this replay |
|---|---|
| base | Read the live catalogue: `select term_id from base_parameters` and `select term_id from parameter_declinations where revoked_at is null` are the only terms an adjudication names. Nothing promoted, declined or minted. |
| research | Skipped by the variant. The admission is logged `--origin owner-supplied` (search exec 204, `--slug stair-ramp-threshold-biomechanics-accessibility`, the subject the writer demands; GAP-103). |
| evidence | `add-source` gave REF-01037 as in the first run (guideline, grey, intrinsic, tier 3 derived, CA, no DOI, VERIFIED by direct-render); five slug links; no re-fetch (the PDF, nine renders, derived text and manifest are the first run's, in `retrieval-log/session_2026-11-13-edmonton-checklist-pass/`). `pub_year` 2022 has no writer for its basis: GAP-106. |
| judgment | Observations in one pass, then adjudication; the catalogue scan recorded after them (scan 19, `--mode catalogue --text-scope full --open-pass-done`); extractions with lawful lens only; relation edges; page-1 harm findings; population match PROXY for MOB. |
| synthesis | No cross-parameter relation stated by the source beyond the edges below; nothing written. |
| specification | `assess_cell.py` once per cell the new lens links reach, after every write. |
| render | No renderer; all cells pending. |

## 2. Extractions written
Source class is the source's own colour marking (its legend, PDF p. 1: blue "Code (required)", magenta "Best Practice"), read from `items.json`; it is an attribution, not a guidebook classification (best practice is the determination's output). Lens is the live link and its basis.

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select e.extraction_id, e.parameter_id, t.canonical_en, e.source_section, e.figure_role, e.claim_type, coalesce(e.comparator,''), coalesce(e.claimed_value,''), coalesce(e.claimed_unit,''), e.root_type, coalesce(e.device_class,''), e.harm_finding, e.claim_text from source_value_extractions e join base_parameters p using(parameter_id) join terms t using(term_id) where e.ref_id='REF-01037' order by 1`


| id | parameter | item | source's class | role | bound / value | lens (basis) | root | device | edges | claim text (verbatim, start) |
|---|---|---|---|---|---|---|---|---|---|---|
| 228 | 9 door width | 2.3 | Code (required), blue | claim | >= 850 mm | MOB (named_in_text) | untraced | mixed |  | “Doorway clearance is 850mm when the door is in the open 90 degree position” |
| 229 | 9 door width | 2.3 | Best Practice, magenta | claim | >= 920 mm | MOB (named_in_text) | committee_assertion | mixed | exceeds → 228 | “(920mm/36” preferred)” |
| 230 | 9 door width | 5.3 | Best Practice, magenta | claim | >= 910 mm | MOB (named_in_text) | committee_assertion | mixed |  | “with elevator door at least 910 – 915mm/36” wide” |
| 231 | 5 turning circle | 5.3 | Best Practice, magenta | claim | >= 1500 mm | MOB (named_in_text) | committee_assertion | mixed |  | “Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x” |
| 232 | 12 ramp run length | 6.2 | Code (required), blue | claim | <= 9 m | A-EFFORT (named_in_text) | untraced |  |  | “Level landings/ resting areas provided at 9m/10yd intervals along ramp” |
| 233 | 9 door width | p1 | page 1 (no class) | finding (harm) | minimum-standard door widths are insufficient for many wheelchairs and | MOB (named_in_text) | committee_assertion | mixed | insufficient → 228 | “there is a need to exceed minimum standards for accessibility where possible. For example,” |
| 234 | 5 turning circle | p1 | page 1 (no class) | finding (harm) | a minimum-standard turning radius is insufficient for many wheelchairs | MOB (named_in_text) | committee_assertion | mixed | insufficient → "Alberta Building Code" | “there is a need to exceed minimum standards for accessibility where possible. For example,” |


- Bounds, not points (ADJUDICATION R8): the Code-marked 850 mm is `>=` (the source's page 1 frames its Code class as "the minimum standards"); the magenta 920 and 910 and the 1500 car figure are `>=` with the warrant in notes; the 9 m landing interval is `<=`, a ceiling on a run. "at least 910 – 915mm" is `>=` 910 with 915 in notes.
- Roots: blue figures are `untraced` with a `root_classification_basis` sentence (OR-19 presumed echo of the Alberta code; precedent extractions 57 and 64); magenta figures are `committee_assertion`. Edge 920 `exceeds` 850 is the source's own pairing.
- Lens: MOB for door width and turning rests on the page-1 sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today", which names exactly those two quantities; each row's notes mark it [ASSUMPTION] (a stricter D-2 reading is AQ-1). The 9 m interval carries the access need `A-EFFORT` on "resting areas" (it exists: `select need_code, family, absorbs from access_needs where need_code='A-EFFORT'`). No identity `ALL` anywhere (`select count(*) from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.ref_id='REF-01037' and l.identity_code='ALL'` → 0).
- Item 5.3's 1500 car figure: `--value-as-written 1500x1500mm` was refused ("the quote states every claimed number as a numeral", which is right) and `raise-follow-up` has no reason for an ambiguous printed figure; the ambiguity is in the row's notes and in GAP-107.
- The parameter-8 (LRV) absent row was not written (F8). The parameter-6 absent finding is parked (no lens).

## 3. Parked writes (not written; waiting on AQ-1)
`scratchpad/session_2026-11-13-edmonton-checklist-pass/parked-writes.jsonl`, one line per figure, each the exact `db.py add-extraction` argv with the lens left blank and `"waits_on": "AQ-1"`, plus the relation edges it would carry (named by the other parked line's key). Each argv was dry-run with a probe lens and accepted, and without one is refused only by D-0182 ("must be stated in at least one lens"). Count: `wc -l` on that file. GAP-109 points to it.

| key | parameter | comparator | value | edges | also waits on | claim text |
|---|---|---|---|---|---|---|
| 6.1-1in20 | 3 | (condition) | 1:20 |  |  | “Ramps are used for any slope steeper than 1 in 20 in a path of travel.” |
| 6.1-1in16 | 3 | <= | 1:16 | condition_on → 6.1-1in20; exceeds → 6.1-1in12 |  | “Preferred maximum slope is 1 in 16” |
| 6.1-1in12 | 3 | <= | 1:12 | condition_on → 6.1-1in20 |  | “(1 in 12 in AB building code)” |
| 1.2-1500 | 4 | >= | 1500 |  | AQ-6 (which route term the path is) | “Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)” |
| 2.10-1100 | 4 | >= | 1100 |  |  | “Corridors should be 1100mm/43”” |
| 2.10-1800 | 4 | >= | 1800 | exceeds → 2.10-1100 |  | “(recommend 1800mm/71”)” |
| 6.2-1500 | 4 | >= | 1500 |  |  | “With the ramp at any point shall not be less than 1500mm/60”” |
| 6.2-870 | 4 | >= | 870 |  |  | “870mm/34” min clearspace between handrails” |
| 1.8-2750 | 11 | >= | 2750 |  |  | “a clear height of not less than 2750mm/108” at the pull-up space and along the v” |
| 2.4-absent-force | 6 | (absent) |  |  |  | “Door operating device should not require tight grasping or twisting of the wrist” |


Figures for quantities with no parameter (the 13 mm threshold, the 1200 mm landing, the 1700 x 1500 mm stall, stair rise and run, handrail height and diameter, control, phone, counter, sign and fountain heights, elevator car sizes, door dwell time) are observations only and are not parked (brief step 5).

## 4. Observations, by latest adjudication

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where o.ref_id='REF-01037' group by 1`


| outcome | observations |
|---|---|
| DEFERRED | 90 |
| NAMES-EXISTING | 13 |


Every observation, with what its DEFERRED rationale waits on (AQ-4 a quantity; AQ-7 an element or feature; OR-17 colour contrast against TERM-011; AQ-6 the two "barrier-free path of travel" phrases):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select o.observation_id, o.locator, o.surface_form, l.outcome, coalesce(l.term_id,''), substr(l.rationale,1,95) from observed_terms o join latest l using(observation_id) where o.ref_id='REF-01037' order by o.observation_id`


| obs | locator | surface form (as printed) | outcome | term | rationale (start) |
|---|---|---|---|---|---|
| 99 | PDF p. 1 | Universal Design | DEFERRED |  | A design concept, not a quantity or an element. The catalogue holds TERM-017 (universal design) |
| 100 | PDF p. 1 | wider turning radius | NAMES-EXISTING | TERM-003 | The space a wheelchair or scooter needs to turn; TERM-003 turning circle (parameter 5) is the s |
| 101 | PDF p. 1 | wider doors | NAMES-EXISTING | TERM-021 | The width of doors as the source contrasts it with the minimum standards; TERM-021 door width ( |
| 102 | PDF p. 1 | mobility devices | DEFERRED |  | A class of assistive devices, an element. The catalogue holds TERM-079 (mobility aids), which i |
| 103 | PDF p. 2, item 1.1 | barrier-free parking spaces | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 104 | PDF p. 2, item 1.2 | Barrier-free unobstructed path of travel | DEFERRED |  | OT-1 and OT-2 (references/project-standards.md, 'OT-1: "Barrier-free path of travel. It is a ci |
| 105 | PDF p. 2, item 1.2 | minimum width | NAMES-EXISTING | TERM-002 | The minimum clear width of an accessible route; TERM-002 corridor width is the clear width of a |
| 106 | PDF p. 2, item 1.2 | colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 107 | PDF p. 2, item 1.3 | Curb ramp | NAMES-EXISTING | TERM-089 | A curb ramp is an inclined surface built as a discrete element to bridge a level difference on  |
| 108 | PDF p. 2, item 1.4 | Access aisle painted on pavement | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 109 | PDF p. 2, item 1.5 | Accessible parking symbols | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 110 | PDF p. 2, item 1.6 | Vertically mounted sign | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 111 | PDF p. 2, item 1.7 | Number of designated accessible parking spaces per number of parking stalls | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 112 | PDF p. 2, item 1.8 | access aisle | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 113 | PDF p. 2, item 1.8 | clear height | NAMES-EXISTING | TERM-061 | An unobstructed vertical dimension above a route; TERM-061 headroom clearance (parameter 11). |
| 114 | PDF p. 2, item 1.9 | directional signs | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 115 | PDF p. 3, item 1.10 | clear accessible path | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 116 | PDF p. 3, item 1.11 | Information for parking payment | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 117 | PDF p. 3, item 2.1 | Barrier-free path of travel | DEFERRED |  | OT-1 and OT-2 (references/project-standards.md, 'OT-1: "Barrier-free path of travel. It is a ci |
| 118 | PDF p. 3, item 2.2 | Signage at all non-accessible entrances | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 119 | PDF p. 3, item 2.3 | Doorway clearance | NAMES-EXISTING | TERM-021 | The clear opening of a doorway with the door open to 90 degrees; TERM-021 door width (parameter |
| 120 | PDF p. 3, item 2.4 | Door operating device | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 121 | PDF p. 3, item 2.4 | lever handles | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 122 | PDF p. 3, item 2.5 | automatic sliding doors | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 123 | PDF p. 3, item 2.6 | pedestrian entrances | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 124 | PDF p. 3, item 2.7 | vestibule | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 125 | PDF p. 3, item 2.8 | Automatic door operator button | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 126 | PDF p. 3, item 2.9 | doorway threshold | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 127 | PDF p. 3, item 2.10 | Colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 128 | PDF p. 3, item 2.10 | Corridors should be 1100mm/43” | NAMES-EXISTING | TERM-002 | The width of corridors; TERM-002 corridor width (parameter 4). |
| 129 | PDF p. 4, item 3.1 | assistive listening devices | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 130 | PDF p. 4, item 3.2 | symbol form | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 131 | PDF p. 4, item 3.3 | braille | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 132 | PDF p. 4, item 3.3 | high colour contrast tactile lettering | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 133 | PDF p. 4, item 3.4 | way-finding signage | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 134 | PDF p. 4, item 3.5 | Braille signage | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 135 | PDF p. 4, item 3.6 | Signage should be 1350mm/51” high from floor level | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 136 | PDF p. 4, item 3.6 | tactile signage | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 137 | PDF p. 4, item 4.1 | tactile strips | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 138 | PDF p. 4, item 4.2 | Step demarcation in yellow | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 139 | PDF p. 4, item 4.3 | rise between 125mm/5” and 180mm/7” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 140 | PDF p. 4, item 4.3 | run of not less than 280mm/11” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 141 | PDF p. 4, item 4.4 | Illumination | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 142 | PDF p. 4, item 4.5 | open area beneath the stairs | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 143 | PDF p. 5, item 4.6 | Carpet | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 144 | PDF p. 5, item 4.7 | handrails on both sides | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 145 | PDF p. 5, item 4.8 | tactile cues | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 146 | PDF p. 5, item 5.1 | clear colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 147 | PDF p. 5, item 5.2 | Location of elevators | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 148 | PDF p. 5, item 5.3 | turning radius | NAMES-EXISTING | TERM-003 | The source calls a 1500 x 1500 mm car the space for a turning radius; TERM-003 turning circle ( |
| 149 | PDF p. 5, item 5.3 | elevator door at least 910 – 915mm/36” wide | NAMES-EXISTING | TERM-021 | The clear width of an elevator door; TERM-021 door width (parameter 9). |
| 150 | PDF p. 5, item 5.3 | stretcher | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 151 | PDF p. 5, item 5.4 | Elevator buttons and emergency controls mounted at an accessible height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 152 | PDF p. 5, item 5.5 | large print tactile numbers and Braille | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 153 | PDF p. 5, item 5.5 | Colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 154 | PDF p. 5, item 5.6 | Braille and tactile numbers | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 155 | PDF p. 5, item 5.7 | Visual indicator in elevators | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 156 | PDF p. 5, item 5.8 | Audible communication system | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 157 | PDF p. 5, item 5.9 | Elevator waiting areas should have seating | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 158 | PDF p. 5, item 5.10 | Elevator doors shall begin to close | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 159 | PDF p. 6, item 6.1 | Ramps | NAMES-EXISTING | TERM-089 | TERM-089 ramp, declined as a parameter (an element). |
| 160 | PDF p. 6, item 6.1 | Preferred maximum slope | NAMES-EXISTING | TERM-001 | The slope of a ramp; TERM-001 ramp gradient (parameter 3). |
| 161 | PDF p. 6, item 6.2 | With the ramp at any point | DEFERRED |  | The sentence as printed has no subject noun: it reads like a ramp width (TERM-002 corridor widt |
| 162 | PDF p. 6, item 6.2 | clearspace between handrails | NAMES-EXISTING | TERM-002 | The clear width of a ramp between its handrails; TERM-002 corridor width (parameter 4), which a |
| 163 | PDF p. 6, item 6.2 | Level landings/ resting areas provided at 9m/10yd intervals along ramp | NAMES-EXISTING | TERM-091 | The interval between landings along a ramp is the length of a flight between landings; TERM-091 |
| 164 | PDF p. 6, item 6.3 | tight turns or switch-backs | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 165 | PDF p. 6, item 6.4 | 15mm/0.6” wide strip | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 166 | PDF p. 6, item 6.4 | Strong colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 167 | PDF p. 6, item 6.5 | Landings must be min 1200mm/47”long | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 168 | PDF p. 6, item 7.1 | diameter | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 169 | PDF p. 6, item 7.1 | handrails on both sides | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 170 | PDF p. 6, item 7.2 | contrasting colour | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 171 | PDF p. 6, item 7.3 | Handrail height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 172 | PDF p. 6, item 7.4 | Handrails extend horizontally | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 173 | PDF p. 7, item 8.1 | wave to open or push button | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 174 | PDF p. 7, item 8.2 | only one turn with clear corner | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 175 | PDF p. 7, item 8.3 | Proper signage | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 176 | PDF p. 7, item 8.4 | located around perimeter | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 177 | PDF p. 7, item 8.5 | knee space | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 178 | PDF p. 7, item 8.5 | soap and towel dispenser | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 179 | PDF p. 7, item 8.5 | low mounted or tilt mirror | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 180 | PDF p. 7, item 8.6 | ACCESSIBLE WASHROOM STALL | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 181 | PDF p. 7, item 8.6 | minimum 1700mm x 1500mm/70 x 60” | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 182 | PDF p. 7, item 8.6 | person with limited mobility | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 183 | PDF p. 7, item 8.6 | grab bars | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 184 | PDF p. 7, item 8.6 | accessible toilet height | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 185 | PDF p. 7, item 8.6 | various toilet size and heights | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 186 | PDF p. 7, item 8.7 | gender inclusive/family washroom | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 187 | PDF p. 8, item 9.1 | Public and emergency phones | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 188 | PDF p. 8, item 9.2 | TTY | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 189 | PDF p. 8, item 9.2 | live captioning app | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 190 | PDF p. 8, item 9.3 | drinking fountain | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 191 | PDF p. 8, item 9.4 | barrier-free counter surface | DEFERRED |  | A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, n |
| 192 | PDF p. 8, item 9.5 | Shelving, coat hooks and light switches | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 193 | PDF p. 8, item 9.6 | variety of seating options | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 194 | PDF p. 8, item 9.7 | Level wheelchair seating area | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 195 | PDF p. 8, item 9.8 | contrasting strip of colour | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 196 | PDF p. 8, item 9.9 | Hearing loops | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 197 | PDF p. 8, item 10.1 | audible and visual signal | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 198 | PDF p. 9, item 11.1 | detectable by someone who uses a cane | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 199 | PDF p. 9, item 11.2 | good colour contrast | DEFERRED |  | The source requires colour contrast and states no figure. Whether its colour contrast names the |
| 200 | PDF p. 9, item 11.3 | Variety of benches | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |
| 201 | PDF p. 9, item 11.4 | quiet space | DEFERRED |  | An element or feature the source requires, with no figure. The catalogue holds no parameter for |


Item coverage, derived from `items.json` against the observations' locators: 75 numbered items, items with no observation: none (computed by this script; re-run it).


## 5. Cells (the engine, once, after every write)

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select specification_id, parameter_id, coalesce(identity_code, needs_code), state, design_scale, regulatory_stratum_only, code_floor_only, gap_register_id, rule_version from specifications where created_by_session='session_2026-11-13-edmonton-checklist-pass' order by 1`


| spec | parameter | lens | state | design_scale | regulatory_stratum_only | code_floor_only | gap | rule |
|---|---|---|---|---|---|---|---|---|
| 9 | 5 | MOB | pending | universal | 1 | 1 | GAP-115 | pilot-6 |
| 10 | 9 | MOB | pending | universal | 1 | 1 | GAP-116 | pilot-6 |
| 11 | 12 | A-EFFORT | pending | population | 0 | 0 | GAP-117 | pilot-6 |


In-lens sources counted by query, against the engine's own sentence (F11):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select count(distinct e.ref_id), count(distinct e.extraction_id) from source_value_extractions e join v_live_lens_links l using(extraction_id) where e.parameter_id=? and l.identity_code | l.needs_code=?`


| spec | parameter | lens | distinct in-lens sources (query) | in-lens extractions (query) | sources | engine's gap sentence says |
|---|---|---|---|---|---|---|
| 9 | 5 | MOB | 5 | 8 | REF-00139,REF-00987,REF-00468,REF-01031,REF-01037 | 8 extraction(s), 2 source(s) |
| 10 | 9 | MOB | 5 | 8 | REF-00139,REF-00987,REF-00468,REF-01031,REF-01037 | 8 extraction(s), 2 source(s) |
| 11 | 12 | A-EFFORT | 2 | 2 | REF-01033,REF-01037 | 2 extraction(s), 1 source(s) |


The engine's "from N source(s)" disagrees with the distinct in-lens sources wherever the cell holds other sources' figures: the defect F11 names, filed as GAP-105 and not patched here (rule 10). A MOB cell built on codes reads `design_scale = universal` while `regulatory_stratum_only` also says so: the collision of AQ-2. Parameters 5 and 9 have no direction (`select parameter_id from base_parameters where accessibility_direction is null`); `set-parameter-direction` was deliberately not run (GAP-110: the judging session's call, to be named in the pull request).

## 6. Coverage reads (ADJUDICATION section 3)


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
| A-REACH | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-SELFCARE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-SIZE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-STABLE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-STIMULUS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TACTILE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TIME | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A-TRIGGER | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


**ICF lens**: codes with any live value-supplying figure: none; `select count(*) from base_icf` codes with none: 72. Medical lens rows: `select count(*) from base_taxonomy_medical` → 0.


**Lens by figure**: value-supplying figures whose only live links are identities and every identity is `ALL` or a parent code: 131 (by ref: {'REF-00987': 7, 'REF-00988': 2, 'REF-00990': 1, 'REF-00991': 1, 'REF-00992': 23, 'REF-00994': 1, 'REF-00995': 2, 'REF-00997': 1, 'REF-01002': 1, 'REF-01004': 1, 'REF-01005': 2, 'REF-01008': 4, 'REF-01010': 1, 'REF-01012': 1, 'REF-01013': 1, 'REF-01014': 1, 'REF-01015': 1, 'REF-01016': 2, 'REF-01017': 1, 'REF-01018': 4, 'REF-01019': 1, 'REF-01020': 3, 'REF-01021': 2, 'REF-01023': 1, 'REF-01025': 1, 'REF-01026': 2, 'REF-01027': 3, 'REF-01028': 11, 'REF-01029': 1, 'REF-01030': 4, 'REF-01031': 9, 'REF-01032': 8, 'REF-01024': 2, 'REF-00139': 16, 'REF-00468': 5, 'REF-01037': 4}).
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select e.extraction_id, e.ref_id, e.parameter_id, group_concat(coalesce(l.identity_code,'')||'/'||coalesce(l.needs_code,'')||'/'||coalesce(l.icf_code,'')) from source_value_extractions e join v_live_lens_links l using(extraction_id) where e.figure_role in ('claim','derived') group by 1 having sum(l.identity_code is null)=0 and sum(l.identity_code='ALL' or l.identity_code in (select identity_code from base_taxonomy_identity where parent_code is null))=count(*)`



**Group words without a parameter** (observations whose latest adjudication is DEFERRED, NOT-OURS or absent, by source):
`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select o.ref_id, coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where coalesce(l.outcome,'UNADJUDICATED') in ('DEFERRED','NOT-OURS','UNADJUDICATED') group by 1,2 order by 3 desc`


| ref | outcome | observations |
|---|---|---|
| REF-01037 | DEFERRED | 90 |
| REF-00977 | NOT-OURS | 3 |
| REF-00468 | DEFERRED | 2 |
| REF-00990 | DEFERRED | 2 |
| REF-00994 | NOT-OURS | 2 |
| REF-00998 | DEFERRED | 2 |
| REF-00999 | DEFERRED | 2 |
| REF-01000 | NOT-OURS | 2 |
| REF-01001 | DEFERRED | 2 |
| REF-01003 | DEFERRED | 2 |
| REF-01005 | DEFERRED | 2 |
| REF-01006 | DEFERRED | 2 |
| REF-01017 | UNADJUDICATED | 2 |
| REF-00984 | DEFERRED | 1 |
| REF-00985 | DEFERRED | 1 |
| REF-00989 | DEFERRED | 1 |
| REF-00991 | NOT-OURS | 1 |
| REF-00996 | NOT-OURS | 1 |
| REF-00997 | NOT-OURS | 1 |
| REF-00998 | NOT-OURS | 1 |
| REF-01001 | NOT-OURS | 1 |
| REF-01007 | NOT-OURS | 1 |
| REF-01008 | NOT-OURS | 1 |
| REF-01009 | UNADJUDICATED | 1 |
| REF-01011 | UNADJUDICATED | 1 |
| REF-01012 | UNADJUDICATED | 1 |
| REF-01013 | UNADJUDICATED | 1 |
| REF-01014 | UNADJUDICATED | 1 |
| REF-01016 | UNADJUDICATED | 1 |
| REF-01033 | DEFERRED | 1 |
| REF-01035 | DEFERRED | 1 |
| REF-01036 | DEFERRED | 1 |


## 7. Gaps filed by this session (the three engine gaps included)

`GUIDEBOOK_DB_PATH=$SC/guidebook.db` · query: `select gap_id, category, priority, substr(description,1,170) from gaps where created_by_session='session_2026-11-13-edmonton-checklist-pass' order by 1`


| gap | cat | pri | description (start) |
|---|---|---|---|
| GAP-103 | SW | P3 | log-search demands a subject (--slug, --parameter or --mined-ref-id) even for --origin owner-supplied, where no search ran. The owner-supplied admission of REF-01037 (sea |
| GAP-104 | SW | P3 | log-mining cannot record a deferred forward (cited-by) direction once a backward pass has set evidence_sources.citation_mining_status to mined: the writer refuses, "That  |
| GAP-105 | SW | P2 | The engine (scripts/assess/assess_cell.py) writes into a pending cell's gap text "from N source(s)", and on the first digest run's scratch database N disagreed with the n |
| GAP-106 | SW | P3 | No sanctioned writer holds evidence_sources.pub_year_note: add-source has no flag for it, amend-source refuses it ("not an amendable judgement field"), and correct-source |
| GAP-107 | SW | P3 | raise-follow-up accepts only two reasons (absence-needs-tested-value, read-outside-admitting-purpose), so an extraction whose printed figure is ambiguous has no follow-up |
| GAP-108 | EG | P2 | R7 harm statements in REF-01037 tied to no parameter, each held as an observation (DEFERRED) and flagged on the owner-supplied search (exec_id 204, harm_finding raised):  |
| GAP-109 | DEC | P2 | AQ-1 (ADJUDICATION 5.3, OPEN): what lens a figure carries when its clause names no person, function or need. REF-01037 figures whose clause names no one were NOT written  |
| GAP-110 | EG | P2 | Accessibility direction for parameters 5 (turning circle) and 9 (door width) is not set (select parameter_id from base_parameters where accessibility_direction is null).  |
| GAP-111 | EG | P2 | R4: REF-01037 phrases adjudicated DEFERRED, with no reader yet (ADJUDICATION R4, P3: T-079 v_deferred_acts gains an adjudication arm). Each rationale names what it waits  |
| GAP-112 | EG | P3 | REF-01037 is a City of Edmonton document and its figures are recorded under country code CA: base_jurisdictions holds no sub-national code for Alberta or Edmonton (T-024  |
| GAP-113 | RP | P2 | Backward-mining leads named by REF-01037 and staged REFERENCE-ONLY, not retrieved: the Safety Codes Council Barrier-Free Design Guide (Aug 2019 PDF), the City of Edmonton |
| GAP-114 | SW | P3 | REF-01037 text defects as printed, recorded without correction: item 6.2 "With the ramp at any point shall not be less than 1500mm/60”" has no subject noun (it reads like |
| GAP-115 | EG | P2 | Evidence gap (parameter-scoped): 8 extraction(s) of parameter 5 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qualified to anchor —  |
| GAP-116 | EG | P2 | Evidence gap (parameter-scoped): 8 extraction(s) of parameter 9 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qualified to anchor —  |
| GAP-117 | EG | P2 | Evidence gap (parameter-scoped): 2 extraction(s) of parameter 12 stated in the lens (needs_code=A-EFFORT), from 1 source(s), but none of those sources qualified to anchor |


Gap ids GAP-103 onward are reissued on the fresh copy and do not mean what the first run's GAP-103 to GAP-120 meant (the first run's GAP-103, a column proposal, is not refiled: ADJUDICATION Q1). Leads (`add-locator`, REFERENCE-ONLY, not retrieved): `select ref_id, title from source_locators where recovered_from like 'REF-01037%'`. Backward mining recorded; the forward deferral was refused (GAP-104).

## 8. Checks, run once after the engine
Full output: `scratchpad/session_2026-11-13-edmonton-checklist-pass/checks-after-engine-v2.txt`.

```
===== scripts/audit/research_batch_dod.py --session session_2026-11-13-edmonton-checklist-pass
==============================================================================
==============================================================================
  R5: PASS — EXAMINED: 0 non-English admissions, so this asserts nothing. REPORTED, not asserted: 0 admission(s) waived by 'R5-GREY-WARRANTED:' in grey_reason; 0 non-English search(es) targeted 'grey' (a target is what was sought,
  R7: PASS — EXAMINED: 1 search(es); every one screened no more than it found and admitted no more than it screened. REPORTED, not asserted: 0 candidate(s) registered for 1 screened; 1 row(s) carry harm_finding=1. Whether harm and
  R10b: PASS — EXAMINED: 1 admitted source(s) carrying a URL; none left verification_status NULL
  R11: PASS — EXAMINED: 0 aliases. This batch wrote none, so this asserts nothing about the corpus
  R16-adjudicate: PASS — EXAMINED: 103 observation(s) on this batch's admissions; every one adjudicated
  R16: PASS — EXAMINED: 7 term(s) named by adjudications of this batch's observations; every one is a parameter or declined. REPORTED, not asserted: 90 adjudication(s) name no term (DEFERRED 90). A figure stated for a concept neve
  R16-scan: PASS — EXAMINED: 1 admission(s); every one carries a catalogue-mode reading. Whether the reading saw everything is NOT tested here -- adversarial standing subject 4
  R17: PASS — EXAMINED: 1 admission(s); every one has a search behind it
  COMPLIANT — all research definition-of-done rules met.
==============================================================================
exit=0
===== scripts/audit/judgment_handoff_shape.py
EXAMINED: 3 invariant(s) of the evidence->judgment hand-off
PASS: shape holds (source_value_extractions currently 221 rows — shape is checked, not content).
exit=0
===== scripts/audit/extraction_relations_integrity.py
EXAMINED: 281  (221 source_value_extractions row(s), 60 extraction_relations edge(s), 0 v_derived_figure_check row(s))
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
EXAMINED: 199
PASS: no class above its baseline
exit=0
===== scripts/tests/test_db_integrity.py
  [✓] K01: every recorded derivation_sha verifies against its own row  (3 examined)
  [✓] K02: every determination written since migration 077 accounts for every extraction of its parameter  (3 examined)
======================================================================
RESULTS: 57/57 checks passed
PASSED HAVING EXAMINED NOTHING (8): B04, I3, I3b, B09, C10, C05, D02, G03
EXAMINED: 3987 subject-inspections across 49 instrumented check(s) of 57
======================================================================
exit=0
===== scripts/audit/derivation_handshake_integrity.py
======================================================================
======================================================================
EXAMINED: 4
VERDICT: CLEAN
exit=0
===== scripts/validate_evidence_state.py
PASS: 16 records checked, 0 errors, 0 warnings
EXAMINED: 16
exit=0
===== scripts/audit/verified_scan_integrity.py
EXAMINED: 219
FAIL: 140 (row, class) pair(s) across 219 live extraction(s); each class above names its remedy.
exit=1
===== scripts/audit/schema_reference_audit.py
EXAMINED: 1353 SQL identifier references in 188 files against 85 live tables and views
RESULT: PASS — every table and view a caller names exists
exit=0
```

`verified_scan_integrity` is red with the same count on untouched canonical (`python3 scripts/audit/verified_scan_integrity.py` on `data/guidebook.db`); no line of its replay output names REF-01037 or an extraction it wrote (`grep -c REF-01037` on its section → 0).

## 9. The critic's findings F1 to F16
| F | Disposition | Shown by |
|---|---|---|
| F1 | done: "Barrier-free unobstructed path of travel" (1.2) and "Barrier-free path of travel" (2.1) DEFERRED on AQ-6 citing OT-1 and OT-2; not TERM-048, not minted | §4 list, surface forms at items 1.2 and 2.1 |
| F2 | parked: 6.2's 1500 and 870 on parameter 4, verbatim, waiting on AQ-1; observation "With the ramp at any point" DEFERRED as unsettled | §3 keys 6.2-1500, 6.2-870 |
| F3 | done: harm findings on parameters 9 and 5 with `insufficient` edges (to the 850 extraction; to the label "Alberta Building Code", kind standard); search exec 204 harm flag raised; GAP-108 names items 1.5, 4.5, 8.2; directions not set (GAP-110) | §2 rows with (harm); `select harm_finding from search_executions where exec_id=204` |
| F4 | done: no `ALL`; MOB only on the page-1 sentence for door and turning; A-EFFORT on "resting areas"; every other figure parked on AQ-1 | §2 lens column; §3 |
| F5 | not repeated: no `add-parameter`, no `decline-parameter` | `select count(*) from base_parameters` equals canonical; `select count(*) from parameter_declinations` equals canonical |
| F6 | done for written rows (850, 9 m: `untraced` with basis); edge 920 exceeds 850 written; parked rows carry the same | §2 root column |
| F7 | done: bounds, not `=`; 1:20 parked as a `condition` with `condition_on` edges from 1:16 and 1:12; 910 `>=`; 1500 car kept on parameter 5 as its side | §2, §3 |
| F8 | not repeated: no parameter-8 absent row | `select count(*) from source_value_extractions where ref_id='REF-01037' and parameter_id=8` → 0 |
| F9 | done: one pass, scan recorded after it; 8.6 stall, 5.3 stretcher and 1828 by 2032 figures in observation quotes | `select observation_id from observed_terms where ref_id='REF-01037' and (context_quote like '%1700mm%' or context_quote like '%2010mm%' or context_quote like '%1828mm%')` |
| F10 | refused by the writers: no verb holds `pub_year_note` (amend-source: "'pub_year_note' is not an amendable judgement field"; correct-source refuses a DOI-less source); basis recorded in GAP-106 | GAP-106 |
| F11 | done in the report (query beside the engine's sentence, §5); tool defect filed, not patched | GAP-105 |
| F12 | done: no "payment machine" route, no TERM-013 for alarm signals, the stall not TERM-009; every non-parameter term DEFERRED | §4 |
| F13 | moot: no targeted scans (nothing promoted) | `select mode from source_scans where ref_id='REF-01037'` |
| F14 | done: "braille" lower case at 3.3; "mobility devices" as printed with the quote's "(scooters/ walkers/wheelchairs)"; 1.2's phrase in full | §4 |
| F15 | done for `device_class` (mixed, on the page-1 words naming wheelchairs and scooters), `locator_scheme`, `file_anchor`; `data_capture_status` stays `pending` (no `db.py` verb writes it: `grep -c data_capture_status scripts/db.py` → 0) | §2 |
| F16 | answered by not minting at all in this run: the brief's DEFERRED-with-question replaces the OR-17 misreading; minting the terms (A2) conflicts with R16 while AQ-4 and AQ-7 are open (see report section 4 of the hand-back) | §4 rationales |

## 10. What the first run got wrong (from the adjudication)
- It wrote the identity `ALL` on the page-1 preamble "meet the needs of all users", against OD-31, and wrote no ICF or access-need link at all: the fatigue reading of the 9 m resting interval and the blind reading of the route were lost.
- It adjudicated both "barrier-free path of travel" phrases to TERM-048, pre-empting OT-1 and OT-2, and recorded one of them cut short.
- It promoted TERM-022 and TERM-092 to parameters (13 and 14) while declining fourteen held terms as elements; TERM-092 belongs to E2 and T-072 item 6, and TERM-022's definition states its own answer.
- It stored `=` on figures its source calls minimum standards, a ramp threshold as a gradient claim, and "at least 910 – 915mm" as a closed `between`.
- It stored Code-marked figures as `committee_assertion` with no root, and wrote no relation edge for the source's own pairings.
- It wrote an LRV `absent` row on a concept it had itself deferred.
- It wrote no harm row for the page-1 inadequacy statement and took neither R7 route for the hazards tied to no parameter.
- It recorded the catalogue scan before the open pass was complete, missed three figures, ran the engine and checks before its last writes, and reported "the only in-lens source is grey" from the engine's sentence, which counts something else.
- It proposed a best-practice column (GAP-103); best practice is the determination's output, and the source's marking is root attribution and edges.

## 11. What was not done
- No figure whose clause names no one was written (AQ-1); no term minted, promoted or declined (AQ-4, AQ-7); the route phrases wait on AQ-6.
- No direction set for parameters 5 and 9; no Co-1, T2 or Co-2 pass (AQ-5 open on the committee's standing); no retrieval of the four leads; no forward citation pass (and its deferral could not be recorded).
- `pub_year_note` not written (no verb); `data_capture_status` not moved (no verb).
- No migration emitted from `batch.sql`, nothing applied, nothing committed; no adversarial pass on this replay.
- First attempt discarded: the observation driver was run twice against the first fresh copy, which wrote every adjudication twice; that copy was discarded, a new copy taken, and admission and observations run once. Its log is kept outside the repository (`$SC/discarded-attempt1.jsonl`).
