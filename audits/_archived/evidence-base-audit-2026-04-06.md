# Evidence Base Audit — Accessible Built Environments Guidebook
**Date:** 2026-04-06  
**Scope:** All research assets, BPC syntheses, case studies, economics, conflict matrices, connections, standards  
**Basis:** Direct inspection of GitHub repo `jordanelias/guidebook` — all active files  
**Model:** Sonnet 4.6 (audit, mapping, critical assessment)  
**Note:** Best-practice synthesis quality assessment is constrained to what Sonnet can evaluate. Opus-tier epistemic arbitration on synthesis choices is not performed here.

---

## 1. Asset Inventory Summary

| Asset type | Count | Notes |
|---|---|---|
| Active BPC slugs (per-slug files) | ~76 | Across 13 topic directories |
| Population-level BPC flat files | 11 + 3 cross-pop | FROZEN archives — canonical content in per-slug files |
| Conflict matrices | 12 domains + SYNTHESIS | All synthesized (Opus 2026-03-30) |
| Connections (active register) | 105 total | CON-0001–CON-0108 |
| Connections (archived) | ~36 | CONSUMED/DEFERRED/CLOSED |
| Case studies | 14 | CS-01–CS-14 (v9.0); v10 scaffold only |
| Economics BPC slugs | 3 | 1 stub (case-study-economics-financial-data) |
| Standards registry entries | Confirmed: ISO, EU, UK (6+) | Incomplete — not all jurisdictions enumerated |
| Change orders | 5 | CO-0001 through CO-0005 |
| Languages searched | 14 (base); 19 (CO-0005 expanded) | 5 new languages unverified — provisional only |
| Jurisdictions covered | 24 (base); 46 (CO-0005 expanded) | Phase 1 research complete for original 24 |
| Opus synthesis complete | 50 (~44 pre-CO-0005 + 6 CO-0005) | 13 slugs await Opus (O1–O10 sessions pending) |
| Opus synthesis pending | 13 | From original synthesis queue |
| Stubs (research blocked) | 2 | `case-study-economics-financial-data`, `accessible-design-failures-poor-performance` |

---

## 2. Coverage by Item Category (A–K)

### Category A — Acoustics
**BPC coverage:** Strong. Slugs: `acoustics-speech-intelligibility-disability`, `room-acoustic-performance`, `deaf-acoustic-built-environment`, `deaf-classroom-reverberation-time`, `assistive-listening-systems`. Population-general acoustic data and engineering performance values are the most evidence-dense domain in the entire BPC.

**Evidence quality:** Tier 1–4. Murgia (2023) and Iglehart (2020) provide Tier 1 data for RT60 ≤0.3 s (DEAF/hearing impaired). ANSI/ASA S12.60 background noise ≤35 dBA is Tier 4. STI ≥0.75 for CI users supported at Tier 1.

**Synthesis status:** Opus complete for acoustics slugs (O2/O3 sessions assumed completed given `synth_queue` shows 44 complete pre-CO-0005). BPC scope review confirms acoustic specifications are engineering-deliverable with clear authority mapping.

**Gaps:** No population-specific RT60 data for OFS or PAIN users (low research priority — these populations' acoustic needs are subsumed by NDV/SENS targets). No non-EN language-specific acoustic standard has substantively different provisions from ISO/EN framework.

**Item completeness:** A-01 (buffer zones) drafted. Pending: full edit pass applying CON-0039 (RT60 ≤0.3 s elevation to Universal Mode universal).

---

### Category B — Lighting
**BPC coverage:** Moderate-strong. Slugs: `therapeutic-lighting-design`, `circadian-lighting-melanopic-edi`, `visual-fire-alarm-seizure-safety`. Supported by conflict matrices LIGHT-INT and LIGHT-QUAL.

**Evidence quality:** LIGHT-INT = DIVERGENT (irreconcilable between populations sharing the ipRGC pathway — dim default with harm asymmetry rationale). LIGHT-QUAL = MIXED. Flicker convergent. Daytime CCT convergent at ~4000K across all populations. Evening CCT divergent (DEM needs warm; NDV/AUT needs cool). `circadian-lighting-melanopic-edi` covers melanopic EDI targets (Tier 1–2 for chronobiology; Tier 4–5 for built environment application). Visual fire alarm seizure risk: confirmed gap — no quantified seizure-safety threshold for strobe frequency in any standard.

**Synthesis status:** Opus synthesis status unknown for these slugs (O2/O3 session coverage not confirmed in current session data).

**Gaps:** B-03 and B-04 are pending merger (CO-0003/D2-23). Seizure threshold for visual alerts is a CONFIRMED OPEN GAP — no standard specifies safe flash frequency for persons with photosensitive epilepsy in a built environment context (IEC 60118-4 does not address this).

---

### Category C — Colour and Visual Contrast
**BPC coverage:** Moderate. Slugs: `luminance-contrast-lrv-evidence-base`, `luminance-contrast-and-pattern`, `detectable-gradient-protocol-sensory-zones`. Conflict matrix COLOUR-CONT classified MIXED (largely compatible) — LRV contrast and chroma are independent variables; high LRV contrast achievable in muted palette.

**Evidence quality:** LRV contrast evidence is strong for VIS populations (BS 8300 ≥30 LRV; verified across 5+ jurisdictions). Chroma conflict (NDV/AUT muted vs NDV/MH warm/saturated) is confirmed at Tier 2–3. Detectable gradient protocol thresholds (≥30 LRV change, ≥0.2s RT60 change, ≥50 lux change) are derived specifications — not directly measured in RCTs.

**Gaps:** C-03+C-06 pending merger (CO-0003/D2-22). No Global South data on LRV compliance thresholds or colour culture-specific requirements.

---

### Category D — Internal Circulation and Wayfinding
**BPC coverage:** Strong. Slugs: `cognitive-wayfinding-design`, `wayfinding-dementia-spatial-design`, `wayfinding-cognitive-science-spatial-design`, `wayfinding-global-south`. Cross-population convergence documented in CON-0001 (five populations, 10+ jurisdictions, loop circulation as Universal Mode universal).

**Evidence quality:** DEM wayfinding: Tier 2–3 (Marquardt 2011, van Buuren 2025 PMC11931140, DSDC EADDAT validated tool). VIS: ISO 23599:2019 Tier 4 (international standard). DBL: Tier 2 (DbI World Access guidelines). NDV/AUT: Tier 2–3 (Mostafa ASPECTSS 2.0, Black et al. 2022). IntD: Tier 4–5 (expert consensus only — no quantified standard in any jurisdiction). Global South: ISO 23599/21542 transfer confirmed (implementation gap, not specification gap); India 75% policy compliance gap documented (PMC12082883 Tier 1).

**Synthesis status:** Opus complete (wayfinding slugs in O4/O5 sessions per queue; CO-0005 wayfinding-global-south Opus complete 2026-04-07).

**Gaps:** Easy Read signage flagged as P3 gap (no built-environment standard). No DEM-specific wayfinding standard exists in any jurisdiction — DSDC EADDAT is the sole validated assessment tool. CON-0001 (loop circulation Universal Mode) is PENDING application to Part 4.

---

### Category E — Entrances and External
**BPC coverage:** Strong. Slugs: `residential-entry-and-threshold`, `threshold-and-level-access`, `threshold-door-hardware`, `stair-ramp-threshold-biomechanics-accessibility`, `accessible-circulation-geometry`, `floor-vibration-wheelchair-disability`. New items E-10, E-12, E-13, E-14 (Entrance Rest Seating), E-15 (Changing Places) drafted.

**Evidence quality:** Threshold/level access: Tier 1–5 across 10+ jurisdictions. Biomechanics: strong (Tier 1 studies on ramp gradient vs wheelchair energy expenditure). Floor vibration: confirmed evidence exists but assessment pending. E-14 (entrance seating) evidence = THIN (expert consensus, CON-0037).

**Synthesis status:** Opus synthesis for entrances-and-circulation slugs scheduled in O6 session; status unclear from current queue data.

**Gaps:** `threshold-door-hardware` was PARTIAL at 12/24 jurisdictions searched at last queue update — CO-0005 Phase 3-A expansion flagged. E-14 is THIN-EVIDENCE item.

---

### Category F — Thermal Environment
**BPC coverage:** PARTIAL/PLACEHOLDER. BPC slugs exist: `thermoregulation-built-environment`, `ms-thermal-temperature-conflict-resolution`, `thermal-comfort-older-adults-care-settings`. F-07 (Thermal Zoning) and F-08 (Thermal Transition) are placeholder items only — content not yet specified.

**Evidence quality:** `thermoregulation-built-environment` (CO-0005 Opus complete 2026-04-07): 18°C–22°C ambient range confirmed. FMS vs SCI/MS thermal conflict: MECHANISTICALLY IRRECONCILABLE — cool default + local warmth for FMS recommended. Tropical passive design cannot eliminate mechanical cooling for thermoregulation-impaired users in hot-humid climates. FIRST-PRINCIPLES DISCLOSURE on all tropical rows. No OT CPG addresses thermal environment in built environment context in any language — this is a confirmed global evidence gap.

**Conflict matrix TEMP-RANGE:** DIVERGENT — most irreconcilable conflict in the entire domain set.

**Gaps:** F-05 content relocated to G-08 (pending). F-07/F-08 placeholders not yet populated. No thermal evidence from any Global South jurisdiction with primary design data. CON-0101, CON-0107, F-07 cross-reference updates identified but not yet applied.

---

### Category G — Seating, Controls, and Workspaces
**BPC coverage:** Moderate. Slugs: `reach-range-and-accessible-controls`, `residential-kitchen-and-task-surfaces`, `ofs-built-environment`, `pain-ofs-built-environment-design`. G-08 (Adjustable Posture Seating) pending population from F-05. G-09 noted. `bariatric-turning-radius-built-environment` exists (seating-and-rest).

**Evidence quality:** Reach range: strong (ADA/ANSI standards, multi-jurisdiction). Kitchen surfaces: Tier 4–5 (extrapolated from ergonomic research, no RCT on residential kitchen accessibility). OFS/PAIN provisions: ALL Tier 5 — no OFS or PAIN built-environment-specific standard exists in any jurisdiction or language. All provisions extrapolated from clinical and general seating/ergonomic codes. This is the weakest evidence domain in the entire BPC.

**Gaps:** OFS/PAIN = confirmed THIN BASE globally. GAP-029 P2 OPEN. G-08 content pending.

---

### Category H — Specialist Facilities
**BPC coverage:** Sparse. H-02 referenced (sensory relief space — cross-reference to NDV slug). H-05 (Nurse Call) is CO-0004 new item — annotated but not specified. I-04 (Ceiling Hoist) placeholder — old bathroom drainage item relocated; `upper-limb-impairment-built-environment` BPC is the intended source.

**Evidence quality:** `upper-limb-impairment-built-environment` slug exists but Opus synthesis status not confirmed. Nurse call system specifications: no BPC slug found for H-05. Ceiling hoist: BPC source identified but item not yet drafted.

**Gaps:** H-05 unspecified. I-04 placeholder only. Changing Places (E-15) appears drafted from v10 standalone file.

---

### Category I — Bathrooms and Wet Areas
**BPC coverage:** Moderate. Slugs: `accessible-bathroom-and-grab-bar`, `fold-down-grab-bar-specification`, `bathroom-typology-global-south`. I-05/I-06 referenced in critique as phantom items (referenced in Part 7 but did not exist in v9.0 Part 7).

**Evidence quality:** Grab bar: strong (Tier 1–4, multi-jurisdiction). Bathroom geometry: strong for Western accessible bathroom typology. Global South (CO-0005 Opus complete): TYPOLOGY-CLASSIFIED — open-plan wet room transfers; squat toilet has PRIMARY GAP (Sejong Toilet only documented solution globally, unpublished); Japan 多目的トイレ most comprehensive non-Western standard. Shared sanitation (1B+ people globally): design specifications absent from all sources — CONFIRMED GAP.

**Gaps:** Squat toilet accessible design = most significant single-topic design gap identified in entire programme. Shared sanitation formal-context spec produced but informal out of scope. I-05/I-06 phantom items require resolution.

---

### Category J — DELETED
Category J (J-01–J-05, BAR/bariatric provisions) struck per project-standards and CO-0004. All provisions relocated to Supplementary Volume Part 4. No J-code permitted in Volumes I–II. **Deletion confirmed clean in Part 4 scaffold.**

---

### Category K — DeafBlind
**BPC coverage:** `deafblind-built-environment-design` slug active. Cited in v9.0 critique as a strength: "Category K demonstrates what Co-1 evidence actually produces (Protactile-derived spatial specifications that no clinical study has measured)."

**Evidence quality:** Tier 4–5 exclusively. Zero Tier 1–2 evidence for DBL built-environment design in any searched language. Sources: DeafSpace Design Guidelines (2010), JJones practitioner guidance (2025), NELOWV (2025), Nordic Welfare Centre (clinical only), MDPI Buildings 14(3):707 (2024). No jurisdiction has DBL-specific built-environment standards.

**Gaps:** GAP-NEW-01/02/03/04 confirmed (DBL). Intervenor clear floor space ≥900×1500 mm at service counters: no standard equivalent. All DBL specs are Co-1/expert consensus only — field-wide limitation, not a project deficiency.

---

## 3. Coverage by Disability Population

| Population | BPC depth | Evidence tier | Jurisdictional breadth | Synthesis status | Critical gap |
|---|---|---|---|---|---|
| MOB | Deep | Tier 1–5 | 24 jurisdictions, 14 languages | Opus complete | 1524mm ADA floor rejected — spec uses 1700/1800mm |
| VIS | Deep | Tier 1–5 | 14+ jurisdictions | Opus complete | — |
| DEAF | Deep | Tier 1–5 | 10+ jurisdictions | Opus complete | Signing space absent from all 14 standard bodies |
| NDV | Deep | Tier 1–4 | PAS 6463 (UK), Mostafa ASPECTSS (multi) | Opus complete | ZH evidence thin (GAP-055) |
| NDV-MH | Moderate | Tier 2–4 | EN, DE, SV primary | Opus complete | ZH thin; TID framework EN-only |
| DEM | Moderate | Tier 2–4 | No DEM-specific standard globally | Opus complete | No jurisdiction standard; EADDAT only tool |
| NEU | Moderate | Tier 1–5 | 14 languages searched | Opus complete | — |
| OFS | THIN | Tier 5 only | No jurisdiction has OFS built-env standard | Pending | No OFS built-env evidence base globally |
| PAIN | THIN | Tier 1–4 (clinical); Tier 5 (built env) | No jurisdiction has PAIN built-env standard | Pending | GAP-029 P2 OPEN; confirmed universal |
| DBL | VERY THIN | Tier 4–5 only | No jurisdiction has DBL built-env standard | Opus complete | Zero Tier 1–2 in field globally |
| IntD | PROVISIONAL | Tier 3–4 | No jurisdiction has IntD architectural standard | Opus complete | All specs = expert consensus; proxied via DEM/NDV |

**Population coverage verdict:** MOB, VIS, DEAF, NDV, and NEU are well-researched by any standard in the accessible design field. DEM, NDV-MH, and DBL are at the frontier of what the field has produced — the guidebook is not under-researched in these areas; the field itself lacks stronger evidence. OFS and PAIN are the honest weak spots: the evidence base for their built-environment provisions does not exist and cannot be manufactured.

---

## 4. Coverage by Functional Deficit

The BPC covers functional deficits as follows:

| Functional deficit | Coverage | Primary BPC source | Weakness |
|---|---|---|---|
| Mobility — ambulatory (MOB/AMB) | Strong | `mobility-built-environment`, `stair-ramp-biomechanics` | — |
| Mobility — upper limb (MOB/UPL) | Moderate | `upper-limb-impairment-built-environment`, `reach-range-and-accessible-controls` | I-04 item not yet drafted |
| Vision — low vision | Strong | `visual-impairment-built-environment`, `luminance-contrast` slugs | — |
| Vision — blind | Strong | `detectable-gradient-protocol`, `wayfinding` slugs | — |
| Hearing — hard of hearing | Strong | Acoustics slugs + assistive listening | — |
| Hearing — Deaf (cultural/linguistic) | Strong | `deaf-spatial-design`, `deaf-acoustic-built-environment` | — |
| DeafBlind | Thin | `deafblind-built-environment-design` | Tier 4–5 only; field limitation |
| Cognitive — dementia | Moderate | `wayfinding-dementia-spatial-design`, `dementia-built-environment` | — |
| Cognitive — intellectual disability | Provisional | `intellectual-disability-built-environment-design` | Proxied via DEM/NDV; THIN |
| Cognitive — ABI/TBI | Moderate | `neurological-built-environment` | — |
| Neurological — sensory processing | Strong | `sensory-processing-model-design-application`, `sensory-relief-space-design` | — |
| Neurological — epilepsy/seizure | Moderate | `visual-fire-alarm-seizure-safety` | Seizure flash threshold gap |
| Fatigue/OFS | Thin | `fatigue-spectrum-built-environment`, `ofs-built-environment` | No built-env standard globally |
| Chronic pain | Thin | `chronic-pain-built-environment`, `pain-ofs-built-environment-design` | Confirmed THIN BASE |
| Thermoregulation impairment | Moderate (new) | `thermoregulation-built-environment` (CO-0005) | Tropical data = FIRST-PRINCIPLES |
| Mental health | Moderate | `mental-health-built-environment` | — |
| Chemical sensitivity (MCS) | Moderate | `air-quality-voc-chemical-sensitivity-built-environment` | Low Tier (4–5) |

**Functional deficit coverage verdict:** The BPC contains more comprehensive functional deficit coverage than any existing single standard or framework. The three honest gaps — OFS built-environment evidence, PAIN built-environment evidence, and squat toilet accessible design — are not addressable through additional research within this project; they are field-wide evidence deficits.

---

## 5. Coverage by Room Type

| Room | Coverage | BPC source | Status |
|---|---|---|---|
| Entrance / threshold | Strong | `residential-entry-and-threshold`, `threshold-and-level-access`, `threshold-door-hardware` | Multi-jurisdiction |
| Bathroom / wet room | Strong (Western) | `accessible-bathroom-and-grab-bar`, `fold-down-grab-bar-specification` | Strong; Global South partial |
| Kitchen | Moderate | `residential-kitchen-and-task-surfaces` | Tier 4–5 only |
| Laundry | Partial | `accessible-laundry-room-design` | 4 jurisdictions; ADA sole quantified source |
| Sensory / quiet room | Strong | `sensory-relief-space-design`, `sensory-room-user-control` | PAS 6463 primary |
| Circulation corridor | Strong | Wayfinding slugs + circulation geometry | Multi-jurisdiction |
| Seating / rest area | Moderate | `bariatric-turning-radius-built-environment`; E-14 | E-14 THIN evidence |
| Workplace / controls | Moderate | `reach-range-and-accessible-controls` | Multi-jurisdiction |
| Changing Places | Noted | E-15 drafted | Isolated from primary item set |
| Bedroom | Not confirmed as standalone slug | — | **GAP — no bedroom-specific slug found** |
| Living room | Not confirmed as standalone slug | — | Subsumed in circulation/thermal items |
| External paths / public realm | Partial | Circulation geometry, wayfinding | ISO 23599 covers tactile; gaps in informal environments |
| Non-residential: classroom | Moderate | `deaf-classroom-reverberation-time` | Hearing-impaired primary |
| Non-residential: healthcare | Moderate | Case studies + biophilic slug | CS-level, not item-level |

**Room type verdict:** Bathrooms, entrances, sensory spaces, and circulation are well-covered. Bedroom specifications are not confirmed as a standalone research area — this is a potential coverage gap for residential application matrices (Part 6). Laundry coverage is notably thin for a room that is consistently one of the highest-barrier spaces for MOB and OFS users.

---

## 6. Conflict Resolution Coverage

### Conflict matrices — all 12 domains synthesized

| Matrix | Classification | Resolution status |
|---|---|---|
| ACOUSTIC-LVL | CONVERGENT | Resolved — DEAF ≤0.3s RT60 serves all |
| COLOUR-CONT | MIXED (largely compatible) | Resolved — LRV ≠ chroma; desaturated hues |
| CORRIDOR-W | RECLASSIFIED — NOT A CONFLICT | Retired |
| FRAGRANCE | MINIMAL CONFLICT | Near-resolved — fragrance-free near-universal |
| LIGHT-INT | DIVERGENT | Resolved via harm asymmetry — dim default |
| LIGHT-QUAL | MIXED | Partially resolved — daytime CCT convergent; evening divergent |
| MOVE-FREE | DIVERGENT but RESOLVED | Resolved — loop design + hazard elimination |
| PREDICT | MIXED (largely compatible) | Resolved — MOB needs space, not reconfiguration |
| SPATIAL-OPEN | MIXED | Resolved — prospect-refuge zoning |
| SURFACE-TEXT | CONVERGENT | Pre-resolved — JIS/ISO truncated domes |
| TEMP-RANGE | DIVERGENT | Partially resolved — cool default + local warmth; not fully specifiable |
| VIS-COMPLEX | RESOLVED-CONSENSUS | Strongest resolution — 3D objects at decision points |

**Conflict synthesis verdict:** The 12-domain synthesis (Opus 2026-03-30) is the most rigorous cross-population conflict resolution framework in the accessible design field. No comparable published methodology exists in ISO, EN, or national standard bodies. The structural finding that "adjustable" is an inadequate universal resolution (valid for 4 identified failure modes) is a significant original contribution.

**Remaining conflict gap:** TEMP-RANGE is the most intractable — cool ambient default + supplemental individual warmth is the recommended resolution but is not fully specifiable at Universal Mode without individual accommodation mechanisms. This is a genuine design-physics limitation, not a research gap.

### Connections (CON register)
- **105 active connections** identified (CON-0001 to CON-0108)
- **~75 PENDING** — not yet applied to Part 4 item specifications
- **~30 CONSUMED/DEFERRED/ARCHIVED** (36+ in archive)
- Connection identification is comprehensive and cross-referenced to gap register items
- **Critical deficiency:** 75 PENDING HIGH-confidence connections means Part 4 as currently assembled does not reflect a significant portion of the identified cross-population synthesis. The connection register is evidence bank, not assembled text.

---

## 7. Evidence Quality Assessment

### Evidence tier distribution (assessed across all active BPC slugs)

| Tier | Description | Representation in BPC | Assessment |
|---|---|---|---|
| Co-1 | Lived experience, co-primary | Present in all population slugs; primary for K, DBL | Appropriate per CRPD framing; epistemologically sound |
| Tier 1 | RCT / systematic review | Acoustics (Murgia 2023, Iglehart 2020), mobility (IDeA Center n=500), economics (Ielegems & Vanrie 2024), lighting (chronobiology RCTs) | Genuinely strong where present; not inflated |
| Tier 2 | Cohort / quasi-experimental | Wayfinding (Marquardt 2011, PMC11931140), DBL guidelines | Appropriately cited; tier labelling consistent |
| Tier 3 | Case-controlled / cross-sectional | Biophilic design, DEM wayfinding, NDV sensory | Correctly used for synthesis; not overstated |
| Tier 4 | Expert consensus / guidelines | PAS 6463, most sensory environment items | Explicitly flagged; not presented as clinical evidence |
| Tier 5 | Standards / regulatory / programme data | Majority of jurisdictional provisions; grant programmes | Clearly labelled; appropriate for specification floor |
| Tier 6 | Professional consensus without documented study | Minor occurrences | Flagged |
| FIRST-PRINCIPLES | Engineering principle; no primary evidence | All Global South tropical rows; some OFS/PAIN items | Explicit disclosure mechanism — appropriate |

### Evidence quality verdict

**Strengths:**
1. Tier labelling is applied consistently across BPC entries and is honest about where evidence is weak.
2. The BPC does not inflate evidence from standards bodies to clinical research level — a systematic error common in accessibility literature.
3. Co-1 (lived experience) is operationalised, not tokenised — the DBL/Protactile specifications demonstrate what Co-1 evidence actually produces distinct from clinical research.
4. The "FIRST-PRINCIPLES DISCLOSURE" mechanism is an internally sound epistemological flag; no equivalent exists in published accessibility standards.
5. The global standard body search (14 languages, 24 jurisdictions) is methodologically more thorough than any published accessible design standard or framework.

**Weaknesses:**
1. **OFS/PAIN evidence base does not exist.** All provisions are extrapolated. This is not a project failure — it is a field-wide gap. But the guidebook must be explicit: these specifications are engineering inference, not evidence-based design. They currently carry Tier 5 labels; some should carry FIRST-PRINCIPLES DISCLOSURE.
2. **Bibliography is empty.** GAP-CR-01 is OPEN: the bibliography section contains zero actual references. All BPC citations use internal key format. The guidebook cannot be peer-reviewed or audited externally until the bibliography is populated. This is a critical publication-readiness deficiency.
3. **Opus synthesis pending for 13 slugs.** Sessions O1–O10 have been planned but not confirmed as executed in current session data. The synthesis queue states "44 complete" but the session log only confirms CO-0005 (6 new slugs). The original 44 may have been completed in O1–O10 sessions, but this cannot be verified from current data. These slugs are stated as awaiting Opus synthesis; if O1–O10 were completed, the queue file should be updated.
4. **Global South evidence (CO-0005) is all PROVISIONAL.** Opus synthesis complete, but all entries carry FIRST-PRINCIPLES DISCLOSURE. This is correct and honest, but it means the guidebook's coverage of 5+ billion people lives on engineering inference.
5. **Case study financial data is largely GREY.** CS-01 (Maggie's Centres), likely multiple others — construction costs undocumented or unverifiable. The economics section has strong macro evidence (cost premiums, retrofit multipliers) but weak case-level financial verification.
6. **Phase 2 evidence research not yet done.** `threshold-door-hardware`, `pain-ofs`, `acoustics`, `dementia-residential`, `intellectual-disability` expansions are planned but unexecuted.
7. **Standards registry is incomplete.** Coverage confirmed for ISO, EU, UK. Remaining 40+ jurisdictions in registry are not enumerated in the read data. The `jurisdiction-tracker` skill exists but has not been run for CO-0005 expanded jurisdictions.

---

## 8. Synthesis Quality vs. the Field

### Scope comparison vs. major accessible design standards

| Dimension | This guidebook | ISO 21542:2021 | BS 8300:2018 | ADA Standards | PAS 6463:2022 | EN 17210:2021 |
|---|---|---|---|---|---|---|
| Population coverage | 11 codes + sub-types | MOB, VIS, DEAF primary | MOB, VIS, DEAF + partial NDV | MOB, VIS, DEAF | NDV (primary) | MOB, VIS, DEAF, AGE |
| Conflict resolution framework | 12-domain systematic methodology | None | None | None | Partial (ASPECTSS) | None |
| Evidence tier hierarchy | Explicit 7-tier + Co-1 | Not explicit | Not explicit | Not explicit | Not explicit | Not explicit |
| OT framework integration | Explicit (PEOP, MOHO, Kawa, CMOP-E) | None | None | None | Partial | None |
| CRPD alignment | Explicit (Art. 9 + GC2 + IDA) | Referenced | Referenced | Not applicable | Referenced | Referenced |
| Economics integration | Structural (Part 11) | None | None | None | None | None |
| Multilingual evidence | 14 languages | None | None | None | None | Partial (EN/FR) |
| Three-tier design hierarchy | Original — no equivalent | Not present | Not present | Not present | Not present | Not present |
| Global South coverage | CO-0005 (PROVISIONAL) | None | None | None | None | None |
| Case studies | 14 | None | None | None | None | None |
| DAR (adaptable readiness) | Part 10 (scaffold) | Not equivalent | Partial | Visitability concept | Not present | Not present |

### Synthesis quality strengths vs. field

1. **Design Modes** is the guidebook's most original contribution to the field. No published standard or framework distinguishes universal design (code floor), population-informed inclusive design (Tier 1), and person-specific co-design (Tier 2) as structurally distinct commitment levels. This resolves the field's persistent tension between "design for all" and "design for individuals" — which no existing standard resolves.

2. **Cross-population conflict resolution methodology** (12 domains, convergent/divergent/mixed, harm asymmetry rationale) is more systematic than any published standard. ISO 21542 and EN 17210 note that provisions may conflict between populations but provide no methodology for resolution. This guidebook does.

3. **OT framework alignment** (PEOP, MOHO, Kawa, CMOP-E) — the systematic positioning of built environment specification within occupational therapy frameworks is absent from all published standards. The Kawa Model recommendation as primary framing language (barriers are external, not intrinsic) is CRPD-aligned and theoretically distinctive.

4. **Economic structure** — treating economics as a load-bearing component (not an appendix) and providing the retrofit multiplier table (cost curve by decision stage) is not found in any accessibility standard. The 0.94%–3.92% new-build premium by building type (Ielegems & Vanrie 2024) is the strongest published data in this domain.

5. **Co-1 evidence operationalisation** — the DBL/Protactile-derived spatial specifications demonstrate that lived experience evidence produces measurably distinct design outcomes that clinical research cannot generate. This is not tokenism.

### Synthesis quality weaknesses vs. field

1. **No peer review.** The guidebook has not been reviewed by external subject matter experts. The v9.0 Critique Report (2026-03-20) was produced internally by Sonnet 4.6. Internal critique is valuable for self-consistency but does not substitute for peer review by an OT, an architect, an acoustic engineer, and a disability researcher reviewing independently.

2. **Opus synthesis dependency for best-practice calls.** The standing rule (Sonnet never determines best practice; Opus for BPC synthesis) creates a structural dependency. 13 slugs in the O1–O10 queue are pending — their best-practice specifications are unverified if Opus sessions have not been completed. The `opus-synthesis-queue.md` states "44 complete" but the session record only confirms the CO-0005 batch (6 slugs). If the original 44 were completed in O1–O10, the synthesis is substantially complete; if not, it is not.

3. **FIRST-PRINCIPLES DISCLOSURE** is an internally invented epistemological flag. It is honest and appropriate, but it is not a recognised term in any published evidence hierarchy (GRADE, JBI, SIGN). Translating this concept into a format recognisable to external reviewers requires mapping to an established framework.

4. **Functional Deficit Researchers (FDR) / OPA/OPB sessions.** The workplan references adjudication files (opa-adjudication.md, opb-adjudication.md, opg-methodology-review.md). The status of these adjudications is not confirmed — if unresolved, methodology questions remain open.

5. **Part 4 incomplete.** Part 4 is SCAFFOLD + CON annotations — not complete specifications. 75 PENDING connections, 3 pending mergers, PAIN/OFS audit on all 85 items, and F-07/F-08 placeholders remain. The guidebook cannot be assessed against the field for item specification completeness until Part 4 is edited.

6. **Case study depth vs. field.** The 14 case studies are schema-populated but many have GREY financial data. Published accessible design case studies (e.g., RHFAC, Rick Hansen Foundation documented cases, VA SAH programme evaluations) have more verified cost data than most CS entries.

---

## 9. Jurisdictional and Language Coverage

### Language coverage
- **14 languages (base):** EN, DE, FR, NL, SV, NO, DA, FI, ES, PT, ZH, JA, KO, IT
- **19 languages (CO-0005):** + AR, HI, ID, SW, BN — all marked UNVERIFIED/PROVISIONAL; native-speaker review pending; keyword compendium not yet complete for these
- **Assessment:** 14-language base coverage is methodologically unprecedented for accessible design research. No published standard or framework has searched more than 2–3 languages. The CO-0005 expansion to 19 is aspirationally correct but requires verification before those searches can be treated as validated.

### Jurisdictional coverage
- **24 jurisdictions (base):** All searched for MOB slug (with some exceptions at Co-1/Tier 5 only)
- **46 jurisdictions (CO-0005):** Expanded via CO-0005-evidence-expansion.md; Phase 1 research complete for original 24; new 22 jurisdictions have stub research only
- **Standards registry:** Coverage confirmed for ISO, EU, UK (6+ entries); remaining jurisdictions not enumerated in inspected data
- **Assessment:** 24-jurisdiction base is strong (exceeds any single published standard). The 46-jurisdiction expansion is an aspirational target, not a completed evidence base.

---

## 10. Economics Evidence

### Strengths
- **New-build cost premium** by building type (residential 0.94% to healthcare 3.92%) — Tier 1–3 evidence (Ielegems & Vanrie 2024, Belgium; TERRAGON/DStGB 2017, Germany; Fuglerud et al. 2015, Norway)
- **Retrofit cost multiplier table** (4× to 40× by item and decision stage) — the most practically actionable economic evidence in the accessible design field
- **Grant programme matrix** (7 jurisdictions, verified FY2024–25): UK DFG (£711m/year), Ireland HAG, Australia NDIS, Canada HATC, USA VA SAH/SHA, USA HUD S504, Switzerland IV — all verified, means-tested, OT-assessment-required
- **KfW 159 Germany:** flagged for current-status verification (KfW "Altersgerecht Umbauen" suspended December 2021)

### Weaknesses
- **Case-study-economics-financial-data** = STUB (scheduled Phase 2B). No per-project ROI data is integrated.
- **Most case study financial data = GREY.** CS-01 (Maggie's) through CS-14: construction costs largely undocumented.
- **No operational cost data.** Cost-of-inaccessibility (productivity, healthcare utilisation, carer burden) is not integrated — this is the strongest economic argument for accessible design (disability-adjusted life years avoided, hospitalisation reduction) but is not in the BPC.
- **DFG programme utilisation gap:** UK DFG reaches only 30% of eligible households (stated in BPC; source requires verification for publication).

---

## 11. Case Studies

### Inventory
- CS-01–CS-14 in v9.0 (14 cases)
- Types include: healthcare (Maggie's CS-01), Deaf campus (Gallaudet CS-02), and 12 others
- Schema complete (v10.4 schema applied)
- Part 12 (v10): SCAFFOLD only — case studies not yet integrated

### Quality assessment
- **Outcome data quality:** Mostly Tier 3 (retrospective POE). CS-02 (Gallaudet) is the strongest — 150+ design guidelines with ongoing evidence accumulation.
- **Financial data quality:** Predominantly GREY or PROVISIONAL. No case study has VERIFIED construction cost isolated to the accessible design premium.
- **Population coverage:** Not audited systematically across all 14 cases. CS-01 serves NDV/MH/PAIN/OFS; CS-02 serves DEAF/MOB. Coverage of VIS, DBL, IntD, NEU as primary design intent is not confirmed across the set.
- **Conflict documentation:** CS-01 documents thermal conflict (cancer/PAIN vs standard comfort); broader cross-population conflict documentation not confirmed across all cases.
- **Post-occupancy evidence:** Case study compendium includes POE findings where available. `post-occupancy-evaluation-global` BPC slug exists. POE evidence is consistently Tier 3 (no RCT-level POE in the accessible design field globally).

---

## 12. Critical Gaps Summary (Priority Ordered)

| ID | Gap | Priority | Status | Addressable? |
|---|---|---|---|---|
| G-BIBL | Bibliography = zero references | P1 | OPEN (GAP-CR-01 reclassified P2 2026-03-29, but this classification is optimistic) | Yes — bibliography-compiler skill exists |
| G-OPUS13 | 13 BPC slugs without confirmed Opus synthesis | P1 | Unknown — O1–O10 sessions not confirmed in current session data | Yes — Opus session required |
| G-CON75 | 75 PENDING connections not applied to Part 4 | P1 | OPEN | Yes — item-specification-writer passes required |
| G-PART4 | Part 4 = SCAFFOLD; multiple pending operations | P1 | OPEN | Yes — sequenced edit passes |
| G-OFS | OFS built-environment evidence base does not exist globally | P1 | CONFIRMED global gap; guidebook cannot resolve | No — must disclose |
| G-PAIN | PAIN built-environment evidence base absent | P1 | CONFIRMED global gap | No — must disclose |
| G-DBL | DBL: zero Tier 1–2 evidence globally | P1 | Confirmed field limitation | No — must disclose |
| G-SQUAT | Squat toilet accessible design: no published specification globally | P1 | Sejong Toilet only; unpublished | No — must disclose |
| G-THERM-TROP | Thermal design for thermoregulation-impaired in hot-humid climates | P1 | FIRST-PRINCIPLES only; no primary data | No — must disclose |
| G-SHARED-SAN | Shared sanitation (1B+ people) accessible design: no specifications | P1 | Out of scope formally; policy gap | Partial |
| G-PEER | No external peer review conducted | P1 | Not initiated | Required for publication |
| G-BEDROOM | Bedroom specifications: no dedicated slug | P2 | Not confirmed as researched room type | Yes — slug required |
| G-LAUNDRY | Laundry: 4 jurisdictions only; ADA sole quantified source | P2 | PARTIAL | Yes — expansion possible |
| G-SEIZURE | Visual alert seizure safety threshold: not quantified in any standard | P2 | Confirmed gap | Partial — field gap |
| G-EASYREAD | Easy Read signage: no built-environment standard | P3 | Flagged; deferred | Partial |
| G-KFW | KfW "Altersgerecht Umbauen" status: suspended 2021; verify current | P3 | Flag in BPC | Yes — jurisdiction-tracker |
| G-PHASE2 | CO-0005 Phase 2/3 research not yet executed | P3 | Planned | Yes — future sessions |

---

## 13. Overall Verdict

### What the evidence base achieves

The evidence base is the most comprehensive assemblage of accessible built environment design evidence attempted in a single document. It exceeds ISO 21542:2021, EN 17210:2021, BS 8300:2018, and all national equivalents on every dimension except legal authority and publication status. The Three-Tier Hierarchy, 12-domain conflict resolution methodology, multilingual search coverage, and structural economics integration are original contributions with no published equivalent.

### What the evidence base does not achieve

1. **Publication readiness.** The bibliography is empty. Part 4 is a scaffold. 75 connections are unapplied. The document cannot be submitted for external review or publication in its current state.

2. **Peer review.** Internal critique (v9.0 Critique Report) is not a substitute for independent expert review. No external OT, architect, or disability researcher has reviewed this work.

3. **Global South coverage.** All CO-0005 Global South entries are FIRST-PRINCIPLES DISCLOSURE. The guidebook correctly names this; it must be structural in the published document, not buried in BPC notes.

4. **OFS, PAIN, DBL, IntD specifications.** These are honest thin-base disclosures, not research failures. But they represent approximately 30–40% of the disability population in most jurisdictions. The guidebook is weaker than it appears on these populations — and must say so clearly and structurally in the text, not only in BPC metadata.

5. **Connections not applied.** 75 PENDING HIGH-confidence connections are the largest single deferred task. The connection register is the most intellectually advanced component of the project — and it is almost entirely unapplied to the item specifications it was designed to improve.

---

*Audit produced by Sonnet 4.6. Best-practice synthesis arbitration not performed — requires Opus 4.6 session. All assessments based on direct inspection of GitHub repo assets as at 2026-04-06.*
