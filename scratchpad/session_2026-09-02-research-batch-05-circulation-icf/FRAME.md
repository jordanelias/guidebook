# FRAME — batch 05, ICF-first

Built under DR-2026-08-19 §12.1 step 2 **as struck and replaced 2026-09-02 (D-0187)**.
The old step 2 pulled the frame from `items`; that contradicted §1.4 rules 1-2 and is gone.
Nothing below is derived from an item code, and no item value appears anywhere in it.

## Subject: slug `accessible-circulation-geometry`

- topic_directory: **entrances-and-circulation** · status: ACTIVE
- serves_axes: **NULL**  ← see the gap note below
- search log: `references/search-log/entrances-and-circulation/accessible-circulation-geometry.md`
- bpc: `references/bpc/entrances-and-circulation/accessible-circulation-geometry.md`

## ⚠ TWO GAPS THIS FRAME MUST DECLARE

1. **`slugs.serves_axes` is populated on 1 of 106 rows**, and not on this one. So the ICF
   cross-product below is the FULL vocabulary, not a slug-specific selection. Nothing in the
   database says which axes this slug serves. Treat the axis list as candidates to test, never
   as a scoped set — and do not infer scope from the slug's name.
2. **No term↔slug link exists.** `term_item_links` was the only route from `terms`/`term_aliases`
   to a subject and was item-keyed, so it is empty. R11's `terms_used` cannot be populated from
   this slug. Choose terms by `terms.domain`, record which you fired, and treat the absence as
   owed work rather than a reason to skip R11.

## ICF axes — codes AND names (CLAUDE.md §6: never bare axis codes)

| axis | name | ICF b-anchors | ICF d-anchors |
|---|---|---|---|
| `AX-AMB` | Ambulant movement | b770,b730 | d450,d455,d460 |
| `AX-ARO` | Arousal-safety demand | b152 | d240 |
| `AX-AUD` | Auditory access & alerting demand | b230 | d310,d115 |
| `AX-BAL` | Balance & postural demand | b235,b240 | d415,d410 |
| `AX-CHM` | Airborne-exposure demand | b435,b440 | d230 |
| `AX-CNT` | Toileting-proximity demand | b620,b525 | d530 |
| `AX-COG-L` | Information-access demand | b117,b167 | d166,d310,d315 |
| `AX-COG-O` | Orientation demand | b114,b144 | d460,d175 |
| `AX-COM-E` | Expressive-communication demand | b320,b330 | d330,d335,d350 |
| `AX-PAI` | Pain-load demand | b280 | d410,d450,d640 |
| `AX-REA` | Reach & manipulation | b730,b710 | d440,d445 |
| `AX-SPR` | Sensory-load demand | b156,b140 | d230,d160 |
| `AX-STA` | Sustained-exertion demand | b455,b130 | d230,d450,d455 |
| `AX-THR` | Thermal demand | b550 | d230 |
| `AX-VIS-L` | Low-vision information demand | b210 | d460,d166 |
| `AX-VIS-N` | Non-visual information demand | b210 | d460 |
| `AX-WHM` | Wheeled movement & transfer | b730,b710 | d465,d420,d410 |

## Access needs

| need | family | obligation (abbreviated) |
|---|---|---|
| `A-NOSPEECH` | communicating | Never require speech or voice; text alternatives to calls, AAC-compatible interaction, no voice-… |
| `A-PLAIN` | communicating | Use plain, predictable language and structure; controlled reading level, no unexplained jargon, … |
| `A-CALM` | environment_safety | Not manufacture pressure; no artificial urgency or dark patterns, forgiving of errors, private b… |
| `A-SIZE` | environment_safety | Fit the range of bodies present; reach ranges at short and tall ends, seat width and weight rati… |
| `A-STIMULUS` | environment_safety | Let the user turn it down; reduce default stimulus density; mute, dim, reduce-motion, hide decor… |
| `A-TRIGGER` | environment_safety | Not emit the trigger; under flash thresholds; fragrance-free; material/ingredient disclosure; no… |
| `A-AT` | operating | Work with assistive technology; programmatically-determinable structure, standard controls, no c… |
| `A-PRECISION` | operating | Tolerate imprecise input; large targets, generous spacing, no fine-motor/drag-only interaction, … |
| `A-REACH` | operating | Be physically reachable; step-free routes, seated-height controls, doorway/turning clearance, on… |
| `A-SELFCARE` | operating | Support personal care and daily tasks; accessible toilets and changing places, operable fixtures… |
| `A-EFFORT` | pacing | Cost little energy; short paths, seated options, save/resume, rest points, no forced continuous … |
| `A-LOWLOAD` | pacing | Keep memory and attention demand low; chunking, save/resume, no reliance on recall across steps,… |
| `A-TIME` | pacing | Impose no time pressure; no session timeouts without extension, no timed inputs, no penalty for … |
| `A-NOSIGHT` | perceiving | Be perceivable and operable without sight; text alternatives, audio description, braille, logica… |
| `A-NOSOUND` | perceiving | Never carry meaning in sound alone; captions, transcripts, visual alerts, sign-language provisio… |
| `A-STABLE` | perceiving | Hold the visual reference still; no auto-playing motion/parallax; handrails, signalled level cha… |
| `A-TACTILE` | perceiving | Offer touch as a first-class channel, not a fallback; tactile signage/maps, hand-under-hand guid… |

## Populations (the full cross-product; applicability is an OUTPUT of synthesis)

`ADHD` ADHDers; people with ADHD · `ALL` applies to all populations (scope marker) · `AUT` autistic people · `BAR` fat people; people in larger bodies · `BLIND` blind and low-vision people · `BRAIN` people with acquired brain injury · `COM` people with complex conditions · `DEAF` Deaf and hard-of-hearing people · `DEAFBLIND` DeafBlind people · `DEM` people living with dementia · `EPI` people with epilepsy · `ID` people with intellectual disability · `LMB` people with limb differences; upper-limb disabilities · `LPA` little people; people with dwarfism · `MH` people with mental health conditions · `MOB` disabled people with mobility needs; wheelchair users · `MOVE` people with movement disorders · `MS` people with MS · `NDV` neurodivergent people · `PAIN` people with chronic pain · `SCI` people with spinal cord injuries · `TALL` tall people · `VES` people with vestibular disorders

## Access-need ↔ ICF crossings available

- `access_need_axis_map`: 21 rows
- `access_need_icf`: 43 rows
- `population_axis_map`: 53 rows
- `lang_jur_map`: 70 rows (language × jurisdiction planning)

## Code leads already held for this territory (research_code_leads)

These name which document to retrieve, never what it says (2026-08-12 REFERENCE-ONLY ruling).

- AU · AS 1428.1
- AU · AS 1428.1 / AS 4032.1
- AU · AS 1428.1 / NCC
- AU · AS 1428.1:2021
- AU · AS 1428.1:2021 §15
- AU · AS 1735 / NCC
- AU · AS 1735.12
- AU · AS 4586:2013
- AU · AS/NZS 1428.4.1:2009
- AU · AS/NZS 2107:2016
- AU · NCC
- CA · CSA B651:2023
- CH · SIA 500
- DE · DIN 18040 + DIN EN 81-41
- DE · DIN 18040 / DVGW W 551
- DE · DIN 18040 / EN 81-70
- DE · DIN 18040-1
- DE · DIN 18040-1 (public)
- DE · DIN 18040-1 §4.3.6
- DE · DIN 18040-2
- DE · DIN 18040-2 R (residential, wheelchair)
- DE · DIN 18040-2 §5.7
- DE · DIN 18040-2:2011
- DE · DIN 18041:2016

(83 held — derived, not asserted. An earlier draft of this line read "84 total; 83 held", a
hardcoded count contradicting the derived one in the same sentence: CLAUDE.md §2(b), caught
before it reached an agent brief.)

## Prior work on this slug

- search_executions: 0
- evidence: 0 (corpus-wide evidence_sources = 0)
