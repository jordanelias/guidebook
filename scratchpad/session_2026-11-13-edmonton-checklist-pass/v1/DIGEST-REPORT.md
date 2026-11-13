# Digest report: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The PDF was digested through the pipeline's `from-evidence` variant, stages 3 to 6, on a scratch copy of the database; it yielded 16 extractions against 10 parameters and 86 harvested phrases, and **no determination**: every cell the engine could compute is `pending`, because the only in-lens source is grey, tier 3, and cannot anchor a value. Nothing is committed to the canonical database and no migration was written; the batch is held for the owner's data pull request. The adversarial pass is running and its findings are in section 9 once it returns.

*Session `session_2026-11-13-edmonton-checklist-pass`, a research session. Every count below is the output of a command shown beside it, re-run on the scratch database (a copy of `data/guidebook.db`, schema 131, kept outside the repository; the drivers are in `scratchpad/session_2026-11-13-edmonton-checklist-pass/helpers/`); re-run rather than trust.*

---

## 1. What the document is

| Field | As read from the document or its payload |
|---|---|
| Title | Checklist for Accessibility & Universal Design (printed on PDF p. 1) |
| Issuer | The City of Edmonton Accessibility Advisory Committee (AAC), which the text says "has created this checklist"; the page carries the Edmonton logo and the AAC logo |
| Date | **None printed.** The PDF's own `CreationDate` is 2022-03-24 (`fitz` metadata); the stored year 2022 is that, and the self-link carries a cache-buster `cb=1631580961` (an earlier fetch of the same URL) |
| Form | 9 PDF pages, 504 x 612 pt, Adobe InDesign 17, a text layer, no form fields (`pdfinfo`, `fitz`) |
| Retrieved | `curl`, HTTP 200, 204,209 bytes, sha256 `1a117aff4c5947a86d8a8061b8cd49d8060c56b03a55583e0ab342d0d5e8d525`, logged by `retrieval_log.fetch` under `retrieval-log/session_2026-11-13-edmonton-checklist-pass/manifest.jsonl` |
| Language | English |
| Self-description | "promote the concepts of Universal Design"; "Alberta Building Code requires the minimum standards for accessibility"; aims to "exceed minimum standards where possible"; the AAC mandate is advice to City Council |

**Structure.** Eleven sections (parking, entrances, signage, stairs/escalators, elevators, ramps, handrails, washrooms, interior elements, alarm systems, furniture), each a table of numbered checklist items with a Y/N N/A column. Derive the item count: `python3 scratchpad/session_2026-11-13-edmonton-checklist-pass/helpers/items.py (it reads the harness scratch copy; the result is saved as scratchpad/session_2026-11-13-edmonton-checklist-pass/items.json)` prints one line per item; the table in section 8 has them all. As measured today there are 75 numbered items.

**The document colour-codes each statement.** Its legend (PDF p. 1) names two classes, in its own words: **Code (required)** in blue and **Best Practice** in magenta. "Best Practice" is the committee's label, an input's attribution, not a guidebook finding: in the guidebook best practice is what the specifications pass determines across all values for a term (the most accommodating or forgiving), so nothing here is stored as best practice. The distinction that matters to the guidebook is **code floor versus above code floor**: the blue statements restate what the document attributes to the Alberta building code, the magenta ones are the committee's own recommendations beyond it. The text layer does not carry the distinction; it is in the colour of each run of text. I classified every run by its text-layer colour (`025087` blue, `9e2064` magenta, via PyMuPDF) and checked it against the page renders. A single item often mixes both: item 1.2 is Code for the path and Best Practice for "minimum width of 1500mm/59"". Counts by class of item (`python3 scratchpad/session_2026-11-13-edmonton-checklist-pass/helpers/items.py (it reads the harness scratch copy; the result is saved as scratchpad/session_2026-11-13-edmonton-checklist-pass/items.json)`): {'CODE': 29, 'BEST/CODE': 16, 'BEST': 30}.

**Things in the payload a text-only reading would miss**
- The legend names four access categories (Physical Access, Deaf or Hard of Hearing Access, Blind or Low Vision Access, Cognitive Limitations Access) in **white text** on the white page (PDF p. 1, zero-based index 0): they are in the text layer and invisible in the render, and no item carries a per-category mark. So the document gives no item-level group tag; groups are named only in running words (blind, Deaf or hard of hearing, wheelchairs, cane users, visual processing difficulties).
- The PDF names four documents by hyperlink or in text: the Alberta Building Code, City Policy C602, the City's Access Design Guide, and the Safety Codes Council Barrier-Free Design Guide (August 2019 PDF); the Code figures are the document's own attribution to "AB building code" (item 6.1) and none is retrieved here.
- Text defects as printed: item 6.2 "With the ramp at any point shall not be less than 1500mm/60"" has no subject noun; item 5.3 prints "at least 910 – 915mm" and calls a 1500x1500 mm square a "turning radius"; item 2.10 prints a corridor width under the entrances heading; handrail rules repeat in 4.7 and 7.1.

---

## 2. How it was run (the pipeline's own order)

The owner supplied this document, so this is `/run-pipeline from-evidence` (skips discovery searching only; every later gate applies). The session was opened with `/session-open` and `/orient`, work was done on a scratch copy of the database with the canonical sha256 (`3c575c89c1a6af4b…`) unchanged, and every writer was the sanctioned `db.py` verb.

| Stage | Done |
|---|---|
| 1 base | Read against the live catalogue: ten active parameters, the identity lens, the 94 terms. The catalogue gave the vocabulary; no phrase was coined (OR-17). |
| 2 research | Skipped by the variant. The admission is logged as `log-search --origin owner-supplied` (R17). |
| 3 evidence | R9 pre-check (no URL or title match in `evidence_sources`), R10 persisted retrieval, admission, the nine page renders, full-text derivation, a catalogue scan at full scope. |
| 4 judgment | 86 phrases observed and adjudicated; 16 extractions with lens links; population match; follow-ups; gaps. |
| 5 synthesis | No cross-parameter dependency is stated by the source; no connection written (a relationship with no direct evidence is a gap, not a row). |
| 6 specification | The engine run for ten cells. |
| 7 render | No renderer exists; nothing to render (all cells pending). |
| 8 adversarial | The `antagonist` agent, read-only, with the 12 lenses. |

### Stage 3 in detail
1. **R9/R10.** No row in `evidence_sources` carries the URL or an Edmonton title. The retrieval was persisted (`1a117aff4c5947a8.pdf`) before use. A Crossref bibliographic query was also run and persisted; it returned five unrelated items (a sweep-style step the owner's framing did not call for, see section 7).
2. **Admission.** `add-source` gave REF-01037: source type `guideline`, evidence type `grey`, scope `intrinsic`, **tier 3 (derived by the writer, marker ○)**, grey flag 1 with the reason "municipal advisory committee checklist … neither a code, a standard nor a study", jurisdiction CA, no DOI (outcome NO-MATCH), verification VERIFIED by direct-render (pages read on the renders), URL accessed 2026-11-13. The classification as grey rests on the document being neither a code nor a study; it is my judgment and an owner question (GAP in section 6).
3. **Slug links** (with the claim that bears on each): `stair-ramp-threshold-biomechanics-accessibility`, `threshold-door-hardware`, `accessible-bathroom-and-grab-bar`, `reach-range-and-accessible-controls`, `luminance-contrast-and-pattern`. The slug `accessible-circulation-geometry` was refused (its labels mix schemes, GAP-013) and was not forced.
4. **Reading.** All nine page renders were read and the derived text (`full_text.py`, nine of nine pages, with page markers) against every active parameter and lens; `record-scan --mode catalogue --text-scope full --method full-read --open-pass-done`, then two `--mode targeted` scans after two terms were promoted mid-run.

### Stage 4 in detail
**Observations (R11 harvest, R16).** Every phrase the source uses for a concept, in its own words with the sentence verbatim and a locator, then adjudicated. Totals today: `select outcome,count(*) from term_adjudications a join observed_terms o using(observation_id) where o.ref_id='REF-01037' group by 1` → {'DEFERRED': 57, 'NAMES-EXISTING': 29}, over 86 observations. 23 name an existing term; the rest were **DEFERRED** (a quantity or element the catalogue holds no term for; not minted, because OR-17 leaves minting to the data pull request the owner reads). The list is derived by `select o.surface_form, o.locator from observed_terms o join term_adjudications a using(observation_id) where o.ref_id='REF-01037' and a.outcome='DEFERRED'`.

**Parameters.** R16 requires every term an adjudication names to be a parameter or declined with its reason. 14 existing terms were declined as elements (precedent: TERM-089 `ramp`); two were **promoted** to parameters because the source states a figure for them: TERM-022 `level threshold` (parameter 13, item 2.9) and TERM-092 `intermediate landing` (parameter 14, item 6.5). Nothing new was minted.

**Lens.** Each extraction needs at least one lens code, with a warrant in the figure's own or its source's words. Where the item names no group, the figure is tagged `ALL` ("applies to everyone") on the source's purpose statement "meet the needs of all users"; the door-width and elevator-turning figures are tagged `MOB` on the source's sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today". These are judgments the owner confirms or corrects (GAP).

**Population.** `add-population-match` for ALL and MOB, grade **PROXY** (no participants, no measurement; R13).
### The 16 extractions

Colour class is the source's own marking, read from the text-layer colour and checked on the render. `root_type` is `committee_assertion`, measurement paradigm `stated_unmeasured` on every row. Comparator is the one the writer's vocabulary allows; where the source writes no comparator ("should be 1100mm") `=` is used and the note says so.

| id | parameter | item | source's own class (blue = its Code (required), magenta = its Best Practice) | value | lens | claim text (verbatim) |
|---|---|---|---|---|---|---|
| 228 | 3 ramp gradient | 6.1 | Best Practice (magenta) | > 1:20 rise:run ratio | ALL | “Ramps are used for any slope steeper than 1 in 20 in a path of travel.” |
| 229 | 3 ramp gradient | 6.1 | Best Practice (magenta) | <= 1:16 rise:run ratio | ALL | “Preferred maximum slope is 1 in 16” |
| 230 | 3 ramp gradient | 6.1 | Code (blue) | <= 1:12 rise:run ratio | ALL | “(1 in 12 in AB building code)” |
| 231 | 4 corridor width | 1.2 | Best Practice (magenta) | >= 1500 mm | ALL | “Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)” |
| 232 | 4 corridor width | 2.10 | Code (blue) | = 1100 mm | ALL | “Corridors should be 1100mm/43”” |
| 233 | 4 corridor width | 2.10 | Best Practice (magenta) | = 1800 mm | ALL | “(recommend 1800mm/71”)” |
| 234 | 9 door width | 2.3 | Code (blue) | = 850 mm | MOB | “Doorway clearance is 850mm when the door is in the open 90 degree position” |
| 235 | 9 door width | 2.3 | Best Practice (magenta) | = 920 mm | MOB | “(920mm/36” preferred)” |
| 236 | 9 door width | 5.3 | Best Practice (magenta) | between 910 to 915 mm | MOB | “with elevator door at least 910 – 915mm/36” wide” |
| 237 | 5 turning circle | 5.3 | Best Practice (magenta) | = 1500 mm | MOB | “Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60”” |
| 238 | 11 headroom clearance | 1.8 | Code (blue) | >= 2750 mm | ALL | “a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes” |
| 239 | 12 ramp run length | 6.2 | Code (blue) | = 9 m | ALL | “Level landings/ resting areas provided at 9m/10yd intervals along ramp” |
| 240 | 8 LRV contrast | 7.2 | Best Practice (magenta) | absent (finding) | ALL | “Handrails in contrasting colour to wall or surrounding area” |
| 241 | 6 operating force | 2.4 | Code (blue) | absent (finding) | ALL | “Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)” |
| 242 | 13 level threshold | 2.9 | Code (blue) | <= 13 mm | ALL | “Level, or beveled doorway threshold (maximum of 13mm/0.5” rise)” |
| 243 | 14 intermediate landing | 6.5 | Code (blue) | >= 1200 mm | ALL | “Landings must be min 1200mm/47”long and same width as the ramp” |
**Readings that carry ambiguity** (recorded in each row's notes and in the last gap): item 6.1's `1 in 20` is a threshold above which the source says ramps are used, not a stated maximum; item 5.3's `910 – 915mm` is a range with no stated reason and its `1500x1500mm` is a square, not a radius (only the side is the value); item 6.2's 9 m is "at 9m intervals", the sense of maximum being the reader's; item 2.3's 850 mm is "is 850mm", not "minimum".

**Absent findings** (R7: the source was read for the parameter and states no figure, which is itself a result): extraction 240 for LRV contrast (the source requires contrasting colour in many items and states no luminance or reflectance figure) and 241 for operating force (item 2.4 states a grip requirement and no force). Both carry an `absence-needs-tested-value` follow-up: the figure, if any, is to be sought in the guides the source names.

### Stage 5 and 6
No cross-parameter dependency is stated by the source (the nearest, item 5.3's turning space and door width in one item, shares a sentence, not a stated dependency), so no `connections` row and no relation edge was written.

The engine (`assess_cell.py`) was run for the ten cells the new figures reach. Result, read from the written `specifications` rows and the engine's `--report-json`:
| spec | parameter | lens | state | marker | value | regulatory_stratum_only | code_floor_only | rule_version |
|---|---|---|---|---|---|---|---|---|
| 9 | 3 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 10 | 4 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 11 | 5 | MOB | pending |  |  | 1 | 1 | pilot-6 |
| 17 | 6 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 18 | 8 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 12 | 9 | MOB | pending |  |  | 1 | 1 | pilot-6 |
| 13 | 11 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 14 | 12 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 15 | 13 | ALL | pending |  |  | 0 | 0 | pilot-6 |
| 16 | 14 | ALL | pending |  |  | 0 | 0 | pilot-6 |
Every cell is **pending**. The gap the engine writes for 3×ALL: "3 extraction(s) of parameter 3 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope)." REF-01037 reads `grain specific`, `scale_directness DIRECT`, `population_directness PROXY`, `conditioning DOWN-WEIGHTED`: a grey tier-3 source cannot anchor, as the tier system fixes it. Parameter 3 does have a direction (`lower_is_better`); parameters 4, 5, 6, 8, 9, 11, 12, 13 and 14 have none recorded, which the gap names. Nothing here is a finding about what the best-practice values are.

**Stage 7.** No renderer exists (`ls scripts/generate/`), and a pending cell is not in `v_best_practice`; the contract's walk by hand finds only a gap to print.

---

## 3. Checks run, and what each examined
All on the scratch database (`GUIDEBOOK_DB_PATH` inline); a check is quoted with the `EXAMINED:` line it printed.
| check | result |
|---|---|
| research_batch_dod --session session_2026-11-13-edmonton-checklist-pass | COMPLIANT; R16-adjudicate examined 86 observations; R16 examined 23 terms; R17 and R16-scan examined 1 admission |
| judgment_handoff_shape | EXAMINED 3 invariants, clean |
| extraction_relations_integrity | EXAMINED 287, CLEAN |
| adjudication_integrity | EXAMINED 60, PASS, 0 tier inconsistencies |
| observation_verbatim_audit | PASS: no class above its baseline (it also reports the existing debt paid down by this batch's observations) |
| test_db_integrity | K01 and K02 each examined the ten engine-written cells (10 examined), PASS; 57 checks |
| derivation_handshake_integrity | EXAMINED 11, CLEAN |
| validate_evidence_state | EXAMINED 23 |
| medical_lens_integrity | EXAMINED 0, CLEAN (the medical lens is empty: examined nothing) |
| schema_reference_audit | EXAMINED 1353 references, PASS |
| verified_scan_integrity | FAIL on rows that existed before this batch; none concerns REF-01037 (`grep -c REF-01037` on its output prints 0) |
| search_log_completeness --session | NOTHING-IN-SCOPE: no WebSearch or WebFetch line in this session ledger; the owner-supplied admission is listed unwitnessed |
`emit_batch_sql.py --scratch … --canonical data/guidebook.db` captured the batch: additive inserts only, 0 updates, 0 deletes (re-run it: it prints its own counts; the SQL is `scratchpad/session_2026-11-13-edmonton-checklist-pass/batch.sql`). It is **not** applied and **not** committed.

---

## 4. Gaps filed, leads, follow-ups
`select gap_id, category, priority, substr(description,1,140) from gaps where created_by_session='session_2026-11-13-edmonton-checklist-pass'` (the engine also wrote one parameter-scoped gap per pending cell):
| gap | cat | pri | description |
|---|---|---|---|
| GAP-103 | SW | P2 | The source marks every statement as Code (required) or Best Practice by text colour (legend on its PDF p. 1), and the figure-level distinction it draws (for example item 1.2: the path is Code, the 1500 mm minimum width is Best Practice) has no typed column on  |
| GAP-104 | SW | P3 | log-search demands a subject (--slug, --parameter or --mined-ref-id) even for --origin owner-supplied, where no search ran; REF-01037 was logged against parameter 3 only to satisfy the writer. Also log-mining cannot record a deferred forward direction once the |
| GAP-105 | DEC | P2 | Does the source colour contrast (the source requires it at many elements, with no figure) name the catalogue LRV contrast concept? Adjudicated DEFERRED on REF-01037 (observed term colour contrast); the owner decides whether it is TERM-011 or a distinct concept |
| GAP-106 | DEC | P2 | Which identity code states a figure when the item names no group: REF-01037 figures for ramp slope, corridor width, headroom and landing interval were tagged ALL on the warrant "meet the needs of all users" (the source purpose statement on its PDF p. 1), and t |
| GAP-107 | EG | P2 | REF-01037 states figures and requirements for many concepts the catalogue holds no parameter for, adjudicated DEFERRED and not minted (OR-17 leaves minting to the data pull request the owner reads). Derive the list: select o.surface_form, o.locator from observ |
| GAP-108 | EG | P3 | REF-01037 is a City of Edmonton document and its figures are recorded under country code CA: base_jurisdictions holds no sub-national code for Alberta or Edmonton (T-024 built the registry; add-jurisdiction admits one with an approval reference). |
| GAP-109 | RP | P2 | Backward-mining leads named by REF-01037 and staged REFERENCE-ONLY, not retrieved: the Safety Codes Council Barrier-Free Design Guide (Aug 2019 PDF), the City of Edmonton Access Design Guide, Policy C602, and the Alberta Building Code (no edition stated). The  |
| GAP-110 | SW | P3 | REF-01037 text defects as printed, recorded without correction: item 6.2 "With the ramp at any point shall not be less than 1500mm/60" has no subject noun (it reads like a ramp width); item 5.3 gives "at least 910 - 915mm" and "1500x1500mm" turning radius; ite |
| GAP-111 | EG | P2 | Evidence gap (parameter-scoped): 3 extraction(s) of parameter 3 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 122 further ext |
| GAP-112 | EG | P2 | Evidence gap (parameter-scoped): 14 extraction(s) of parameter 4 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 13 further ext |
| GAP-113 | EG | P2 | Evidence gap (parameter-scoped): 7 extraction(s) of parameter 5 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 2 further extra |
| GAP-114 | EG | P2 | Evidence gap (parameter-scoped): 7 extraction(s) of parameter 9 stated in the lens (identity_code=MOB), from 2 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 12 further extr |
| GAP-115 | EG | P2 | Evidence gap (parameter-scoped): 6 extraction(s) of parameter 11 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 2 further extr |
| GAP-116 | EG | P2 | Evidence gap (parameter-scoped): 1 extraction(s) of parameter 12 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). 21 further ext |
| GAP-117 | EG | P2 | Evidence gap (parameter-scoped): 1 extraction(s) of parameter 13 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). No accessibili |
| GAP-118 | EG | P2 | Evidence gap (parameter-scoped): 1 extraction(s) of parameter 14 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope). No accessibili |
| GAP-119 | EG | P2 | Evidence gap (parameter-scoped): 4 extraction(s) of parameter 6 stated in the lens (identity_code=ALL), but NONE COUNTS: none states a value, and every finding is skimmed (owing a dedicated reading) or reports an absence, so none supplies direction. 8 further  |
| GAP-120 | EG | P2 | Evidence gap (parameter-scoped): 2 extraction(s) of parameter 8 stated in the lens (identity_code=ALL), but NONE COUNTS: none states a value, and every finding is skimmed (owing a dedicated reading) or reports an absence, so none supplies direction. 4 further  |
**Backward-mining leads** staged with `add-locator` (REFERENCE-ONLY, not retrieved or read): `Access Design Guide`, `Barrier-Free Design Guide`, `Accessibility for People with Disabilities Policy C602`, `Alberta Building Code`. The backward pass is recorded (`log-mining`); a forward (cited-by) pass is not run and could not be recorded as deferred (the writer refuses once backward set the one `citation_mining_status` flag, GAP-015/GAP-022 unruled).

---

## 5. Every item of the document and what became of it
Class is the source's own colour marking of the item's text (CODE = Code (required), BEST = Best Practice). Obs = observation ids; Ext = extraction ids.
| item | PDF p. | class | text (start) | Obs (E existing term, D deferred) | Ext |
|---|---|---|---|---|---|
| 1.1 | 2 | CODE | Designated barrier-free parking spaces located closest to barrier-free entrance | 114E |  |
| 1.2 | 2 | BEST/CODE | Barrier-free unobstructed path of travel ( minimum width of 1500mm/59” ) from parking area to building entranc… | 99E, 122D | 231 |
| 1.3 | 2 | CODE | Curb ramp to sidewalk located between parking spaces | 154E |  |
| 1.4 | 2 | CODE | Access aisle painted on pavement between barrier-free parking spaces | 155D |  |
| 1.5 | 2 | BEST/CODE | Accessible parking symbols painted on pavement at the entrance of each stall. The symbol and any associated ba… | 156E |  |
| 1.6 | 2 | CODE | Vertically mounted sign showing accessibility symbol located near the centre line of each designated stall (mi… | 124D |  |
| 1.7 | 2 | CODE | Number of designated accessible parking spaces per number of parking stalls: 1 accessible stall per 2-10 space… | 125D |  |
| 1.8 | 2 | CODE | Passenger loading zones need: an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parall… | 107E, 123D | 238 |
| 1.9 | 2 | BEST | If the location of designated parking stalls is not easily visible from the approach viewpoint, appropriate di… | 157E |  |
| 1.10 | 3 | BEST | Ensure there is a clear accessible path between accessible stalls and the payment machine | 158E |  |
| 1.11 | 3 | BEST | Information for parking payment is easy to understand and clearly visible for accessible stalls | 159D |  |
| 2.1 | 3 | CODE | Barrier-free path of travel from parking and/or drop off zone to entrance | 160E |  |
| 2.2 | 3 | BEST | Signage at all non-accessible entrances should clearly indicate location of barrier-free entrance | 161E |  |
| 2.3 | 3 | BEST/CODE | Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred) | 101E | 234, 235 |
| 2.4 | 3 | CODE | Door operating device should not require tight grasping or twisting of the wrist (doors should have lever hand… | 108E | 241 |
| 2.5 | 3 | BEST/CODE | The primary entrance is barrier-free (automatic sliding doors are optimal; power doors with large paddle/push … | 162D |  |
| 2.6 | 3 | CODE | In addition to the barrier-free entrances required, not less than 50% of the pedestrian entrances, including t… | 128D |  |
| 2.7 | 3 | CODE | If entrance is through doors in a series, leave enough room (1200mm/47” plus the width of the door) for a whee… | 126D |  |
| 2.8 | 3 | BEST | Automatic door operator button is 800mm/31.5”-1500mm/59” from the ground and is located 1500mm/59” back from t… | 127D |  |
| 2.9 | 3 | CODE | Level, or beveled doorway threshold (maximum of 13mm/0.5” rise) | 117E | 242 |
| 2.10 | 3 | BEST/CODE | Colour contrast to identify doorway threshold, frame or entrance. Corridors should be 1100mm/43” (recommend 18… | 100E | 232, 233 |
| 3.1 | 4 | CODE | Facilities and services for persons with disabilities identified with appropriate symbols (e.g. availability o… | 163D |  |
| 3.2 | 4 | BEST | Signage available in symbol form for those with visual processing difficulties or who are unable to read | 112E |  |
| 3.3 | 4 | BEST | Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps … | 148D |  |
| 3.4 | 4 | BEST | General and way-finding signage consistent in design and easily identifiable | 115E |  |
| 3.5 | 4 | BEST | Braille signage mounted at appropriate height (chest level) and location | 164D |  |
| 3.6 | 4 | BEST/CODE | Signage font in Sans Serif (e.g., Verdana, Arial) for reading ease. Signage should be 1350mm/51” high from flo… | 129D |  |
| 4.1 | 4 | CODE | Slip-resistant, tactile finish or strips contrasting in colour and texture on all landings, tread edges/stair … | 111E |  |
| 4.2 | 4 | CODE | Step demarcation in yellow on sides and back of escalator steps | 165D |  |
| 4.3 | 4 | BEST | Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11” (should not be… | 130D |  |
| 4.4 | 4 | CODE | Illumination shall be positioned to minimize glare and shadow | 166D |  |
| 4.5 | 4 | BEST | Ensure any open area beneath the stairs is enclosed with planters, railings, benches, fencing etc to ensure no… | 167D |  |
| 4.6 | 5 | BEST | Carpet is securely attached | 168D |  |
| 4.7 | 5 | BEST/CODE | A stairway shall have a handrail on at least one side, but if it is 1100mm/43” or more wide, it shall have han… | 131D |  |
| 4.8 | 5 | BEST | Handrails should have a system of tactile cues (texture changes) within 300mm/12” from each end | 132D |  |
| 5.1 | 5 | BEST | Doors have clear colour contrast from door surroundings | 169D |  |
| 5.2 | 5 | BEST | Location of elevators clearly identified at main entrance | 119E |  |
| 5.3 | 5 | BEST/CODE | Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator do… | 102E, 103E | 236, 237 |
| 5.4 | 5 | CODE | Elevator buttons and emergency controls mounted at an accessible height (1045mm/41”-1095mm/43” from ground) | 133D |  |
| 5.5 | 5 | BEST/CODE | Elevator buttons and emergency controls incorporate large print tactile numbers and Braille mounted in a raise… | 170D |  |
| 5.6 | 5 | CODE | Braille and tactile numbers placed on both sides of door jambs at appropriate height to identify floor level | 171D |  |
| 5.7 | 5 | BEST | Visual indicator in elevators to indicate “help on the way” for use in an emergency | 152D |  |
| 5.8 | 5 | BEST | Audible communication system shall be available for accessing elevators, inside the car and have an announceme… | 153D |  |
| 5.9 | 5 | BEST | Elevator waiting areas should have seating in close proximity | 172D |  |
| 5.10 | 5 | BEST | Elevator doors shall begin to close after a minimum of 8 seconds from the fully open position | 134D |  |
| 6.1 | 6 | BEST/CODE | Ramps are used for any slope steeper than 1 in 20 in a path of travel. Preferred maximum slope is 1 in 16 (1 i… | 104E | 228, 229, 230 |
| 6.2 | 6 | BEST/CODE | With the ramp at any point shall not be less than 1500mm/60” ; 870mm/34” min clearspace between handrails. Lev… | 105E, 135D, 136D | 239 |
| 6.3 | 6 | BEST | Minimize or avoid tight turns or switch-backs | 173D |  |
| 6.4 | 6 | BEST | Strong colour contrast and tactile surfacing on all ramp landings and a 15mm/0.6” wide strip in contrasting co… | 137D |  |
| 6.5 | 6 | CODE | Landings designed to accommodate larger chairs and scooters (able to open doors without backing onto ramp). La… | 106E | 243 |
| 7.1 | 6 | BEST/CODE | A stairway should have a handrail on at least one side but if it is 1100mm or more wide it shall have handrail… | 138D |  |
| 7.2 | 6 | BEST | Handrails in contrasting colour to wall or surrounding area |  | 240 |
| 7.3 | 6 | CODE | Handrails provided at two heights with an unobscured view between. Handrail height should be 865mm/34” and no … | 139D |  |
| 7.4 | 6 | BEST | Handrails extend horizontally beyond last stair and terminate to wall or ground | 174D |  |
| 8.1 | 7 | BEST | Single door entrance is optimal. Have a wave to open or push button available | 175D |  |
| 8.2 | 7 | BEST | For washrooms without entrance door, there is only one turn with clear corner so persons who are blind do not … | 176D |  |
| 8.3 | 7 | BEST | Proper signage located outside the entrance and stall door | 177D |  |
| 8.4 | 7 | BEST | Sinks, garbage cans, etc. located around perimeter rather than in the centre of the room | 178D |  |
| 8.5 | 7 | BEST | Accessible sink (minimum knee space of 735mm/29”) with soap and towel dispenser close to sink at preferred hei… | 140D, 141D, 142D |  |
| 8.6 | 7 | BEST/CODE | ACCESSIBLE WASHROOM STALL: • minimum 1700mm x 1500mm/70 x 60” • door that swings outward so person with limite… | 110E, 116E, 143D |  |
| 8.7 | 7 | CODE | Self-contained, gender inclusive/family washroom available, with proper signage provided in an accessible loca… | 151D |  |
| 9.1 | 8 | CODE | Public and emergency phones mounted at an accessible height with a minimum of 865mm/34” and a maximum of 1370m… | 144D |  |
| 9.2 | 8 | BEST/CODE | TTY (built in typewriter) phone for users who are Deaf or hard of hearing. Video Relay Service (VRS), Video Re… | 113E, 147D |  |
| 9.3 | 8 | CODE | At least one drinking fountain at accessible height (610mm/24” from ground preferred) spout located near front… | 145D |  |
| 9.4 | 8 | CODE | One accessible section of counter in all areas that serve the public. A barrier-free counter surface shall not… | 146D |  |
| 9.5 | 8 | CODE | Shelving, coat hooks and light switches at an accessible height | 179D |  |
| 9.6 | 8 | BEST/CODE | Have a variety of seating options available, including space for persons using wheelchairs to sit/park in all … | 180D |  |
| 9.7 | 8 | CODE | Level wheelchair seating area (in theatres, lecture halls, sports arenas, etc), to also include companion seat… | 150D |  |
| 9.8 | 8 | CODE | Glass doors or partitions include a contrasting strip of colour across at eye-level | 181D |  |
| 9.9 | 8 | BEST | Hearing loops provided (counter loop or portable hearing loop) | 109E |  |
| 10.1 | 8 | CODE | All alarm systems to include an audible and visual signal | 118E |  |
| 11.1 | 9 | BEST/CODE | Well anchored furniture should only be placed outside the main path of travel (inside or outside) and is detec… | 182D |  |
| 11.2 | 9 | CODE | There should be good colour contrast between street furniture and background surfaces (generally, grey colours… | 183D |  |
| 11.3 | 9 | CODE | Variety of benches should be provided (some including a back and an arm rest) | 184D |  |
| 11.4 | 9 | BEST | Have a quiet space available | 149D |  |
Items with neither an observation nor an extraction: derive with the table above (an empty Obs and Ext cell). The qualitative requirements that name no group and no figure were observed, adjudicated DEFERRED and not extracted, because an extraction needs a parameter and a stated value or an absence for it.

---

## 6. Questions this pass leaves for the owner (each also filed as a gap)
1. **Tier and evidence type.** Is a municipal advisory-committee checklist `grey` (tier 3, ○), as classified here, or does the owner place it elsewhere? It restates Alberta building code requirements in blue and adds the committee's recommendations in magenta.
2. **Which identity states a figure when the item names no group.** `ALL` on the purpose statement "meet the needs of all users" was used for ramp slope, corridor width, headroom, landing interval and threshold figures; `MOB` for door width and elevator turning. Confirm or correct.
3. **Minting.** 57 phrases are DEFERRED, many of them quantities the source states (stair rise and run, handrail height and diameter, elevator button height, washroom stall size, counter and phone heights, sign height, accessible stall ratio). Which become parameters is the owner's reading in the data pull request (OR-17).
4. **Is the source's colour contrast the catalogue's LRV contrast?** Left DEFERRED.
5. **Code floor versus above code floor.** The document draws this distinction per statement (by colour) and the digest holds it only in each extraction's notes, quoting the source's own labels. A typed Code-versus-Best-Practice column was first proposed (GAP-103) and is withdrawn: best practice is the guidebook's determination, not a label on an input, so a column by that name would presume the result. Open: whether code floor versus above code floor is a typed property of a figure at all, or is derived against the code stratum (rule 8), and what to call a figure from a non-regulatory source that restates the floor.
6. **Sub-national jurisdiction.** Alberta and Edmonton are not in `base_jurisdictions`; the figures are recorded under CA.
7. **The two promoted parameters** (13 level threshold, 14 intermediate landing) and the 14 declinations are standing decisions about shared vocabulary.

---

## 7. What I did wrong or changed my mind about, and what I could not do
- **A discovery-style step.** I first ran a Crossref bibliographic query and treated the admission as a research find. The owner supplied the PDF, so there is no search; the Crossref payload is persisted and harmless, and the admission is logged `owner-supplied`. The writer nevertheless demands a subject for the logged search, and I gave it parameter 3 only to satisfy it (a tooling gap).
- **The artefact went to the wrong directory.** I fetched from `scripts/research/`, so `retrieval-log/` landed under it; I moved it to the repository's `retrieval-log/` before using the page renderer and the full-text derivation.
- **The session was opened late.** The first fetch commands ran before `/session-open`; their command-log lines went to the previous session folder (`session_2026-11-13-t019-lens-gather`) and need moving by `session_id`. `scratchpad/CURRENT` now names this session.
- **An overclaim, corrected.** The first catalogue-scan note said every requirement phrase had been observed; 31 items had none. I completed the open pass (31 more observations, ids from 154) and the claim is now true, but the sentence in scan 19's note predates it.
- **Value wording.** `--value-as-written "1 in 16"` was refused (the quote writes both numbers as numerals); the figure is stored as `1:16` with unit `rise:run ratio`.
- **Absent rows.** `figure_role` for an absent claim must be `finding`; first attempt as `claim` was refused.
- **A framing error, corrected on the owner's point.** I proposed a typed "Code vs Best Practice" column; the owner pointed out that best practice is the most accommodating value across all values for a term, so naming a stored column that is presumptuous. GAP-103 carries the correction (`amend-gap`), the table header above says the class is the source's own, and the proposal is replaced by the code-floor versus above-code-floor question in section 6. The extraction notes still quote the source's labels and say so; they are attribution, not a classification.
- **Not done.** No Co-1, T2 or Co-2 pass (the log-search findings note says `CO1-NOT-APPLICABLE` for this document and that such a pass was outside this run); no retrieval of the four named documents; no forward citation pass; no data migration; the adversarial pass is not yet recorded in the database (`record-adversarial-pass` needs the critic's transcript committed first); the extraction status is left `preliminary` (no second reading has verified a row).

## 8. Ship state
Everything above exists only on the scratch database and under `retrieval-log/{STEM}/` (the PDF, nine renders, derived text and manifest, untracked). To ship: commit the retrieval-log session folder and `scratchpad/{STEM}/` (rule 6), emit and apply the batch through `emit_data_migration` and `migrate_db`, and open the data pull request last (rules 9 and 10), on a branch separate from the tooling work. **Collision to fix first:** `scripts/tests/test_run_pipeline_refusals.py` uses `REF-01037` as its fixture source id; with this batch's derived text registered under that id, its cases X02 and X03 are refused (`--verbatim-exempt` is refused over a decodable text). That is a defect in the fixtures (they should derive a free id, rule 8) and will break permanently once REF-01037 is real.

## 9. Adversarial pass
*Running at the time of writing. The critic is the `antagonist` agent, read-only, assigned accuracy (L1, L2, S2), logic (L3 to L8, S1, S3) and sequence (S4) with the 12 lenses; its findings and my disposition of each will be appended here.*
