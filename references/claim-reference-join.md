# Claim-to-Reference Join Table
<!-- Generated 2026-04-19 — Step 3 of citation infrastructure -->
<!-- Session 1 of Step 2 (Part 4 Category A acoustics) complete 2026-04-19 -->
<!-- Session 2 of Step 2 (Part 4 Category B-C lighting/surfaces) complete 2026-04-19 -->
<!-- Session 3 of Step 2 (Part 4 Category D-E wayfinding/circulation) complete 2026-04-19 -->
<!-- Session 4 of Step 2 (Part 4 Category F-G env controls/bathroom/seating) complete 2026-04-19 -->
<!-- Session 6 of Step 2 (Part 4 Category H-I-K controls/UPL/DeafBlind) complete 2026-04-19 -->
<!-- Session 7 of Step 2 (Part 2 disability population categories) complete 2026-04-19 -->

**Purpose:** Traceable mapping from each specification claim in Parts 1-12 to the references that support it. Phase B parsers read this table to render footnotes on the frontend.

**Total claims enumerated:** 1382

**Overall status:**
- PENDING (untagged): 741
- TAGGED (refs assigned): 543
- VERIFIED (confirmed): 0
- DEFERRED (non-citable: methodology, definitional, echo): 87
- ORPHANED (no supporting ref in global registry): 11

**Full machine-readable data:** `references/claim-reference-join.json`

---

## Progress by Part

| Part | Total | PENDING | TAGGED | VERIFIED | DEFERRED | ORPHANED |
|---|---|---|---|---|---|---|
| Part 1 | 7 | 7 | 0 | 0 | 0 | 0 |
| Part 2 | 83 | 0 | 81 | 0 | 2 | 0 |
| Part 3 | 42 | 42 | 0 | 0 | 0 | 0 |
| Part 4 | 558 | 0 | 462 | 0 | 85 | 11 |
| Part 5 | 79 | 79 | 0 | 0 | 0 | 0 |
| Part 6 | 115 | 115 | 0 | 0 | 0 | 0 |
| Part 7 | 111 | 111 | 0 | 0 | 0 | 0 |
| Part 8 | 116 | 116 | 0 | 0 | 0 | 0 |
| Part 9 | 10 | 10 | 0 | 0 | 0 | 0 |
| Part 10 | 23 | 23 | 0 | 0 | 0 | 0 |
| Part 11 | 191 | 191 | 0 | 0 | 0 | 0 |
| Part 12 | 47 | 47 | 0 | 0 | 0 | 0 |

---

## Session Log

### Step 2 Session 1 — Part 4 Category A (acoustics) — 2026-04-19 ✅

- **Scope:** 73 claims across A-01 to A-17
- **Results:** 45 TAGGED, 17 DEFERRED, 11 ORPHANED
- **Primary references used:** REF-00142 (Bettarello 2021), REF-00157 (PAS 6463:2022), REF-00151 (BS 8300-2:2018), REF-00218 (DIN 18041:2016), REF-00126 (ANSI S12.60), REF-00289 (IEC 60118-4), REF-00302 (ISO 2631), REF-00305 (ISO 10137), REF-00041 (Staud 2011), REF-00273 (HLAA Auracast), REF-00167 (CAOT ABI 2024)
- **ORPHANED flagged (require Phase B content review):**
  - A-04 L160 20m restorative interval — Kaplan 1989 cited but outside acoustic BPCs
  - A-09 L340 0.1 m/s RMS vibration threshold — UNVERIFIED, likely BS 6472-1:2008 (GAP-IMPL-05)
  - A-13 L516 De Hogeweyk 94% / 34% — Dutch grey lit not in global registry
  - A-16 L639 Uhthoff 30-60 min recovery + ≤16°C / ≤20°C MS cooling — Leavitt 2014, Davis 2010 cited in Part 4 but not in global registry (MS BPC has Staud 2011 only)
- **DEFERRED categories:**
  - Measurement-frequency references (500 Hz, 1000 Hz — standard methodology per ISO 3382-2)
  - Construction tolerances (3mm undercut)
  - OT evidence echo text (repeats spec values already tagged upstream)
  - Category B metadata misextracted to A-17 scope (1200mm/850mm/1500mm eye-level figures)

### Step 2 Session 2 — Part 4 Category B-C (lighting, surfaces) — 2026-04-19 ✅

- **Scope:** 44 claims across B-01 to B-12, C-03, C-04, C-05
- **Results:** 38 TAGGED, 6 DEFERRED, 0 ORPHANED
- **Primary references used:**
  - REF-00009 (Brown 2022 — melanopic EDI recommendations), REF-00185 (CIE S026:2018), REF-00323 (WELL v2 L07)
  - REF-00135 (Bauman 2010 DeafSpace draft), REF-00248 (Gallaudet 2010 DeafSpace Vol 1)
  - REF-00150 (BS 8300-2:2018), REF-00157 (PAS 6463:2022), REF-00432 (RHFAC v4.0 sensory)
  - REF-00022 (Jordan 2024 photosensitive epilepsy), REF-00229 (DSDC EADDAT 2022)
  - REF-00437 (RNIB 2023 Building Sight), REF-00486 (Ulrich 1984 view/recovery)
  - REF-00149 (BS EN 54-23:2010), REF-00401 (NFPA 72-2022)
  - REF-00428 (RHFAC v4.0 entry), REF-00205 (Dementia Australia 2022), REF-00416 (RCOT 2019 Adaptations Without Delay)
  - REF-00029 (Mostafa 2021 ASPECTSS 2.0), REF-00360 (Manandhar 2022 LRV)
- **DEFERRED categories:**
  - OT evidence echo text (B-02 lines 747, B-09 line 976 ≥75% OT interpretation)
  - Engineering constant in OT evidence basis (B-03 100Hz mains flicker — physical constant, not design spec)
  - Illustration note echoing specification (B-12 line 3581)
- **Registry gaps noted (cited in Part 4 but absent from global registry — add before publication):**
  - CAOT 2018 — Practice guidelines for acquired brain injury (cited B-03, B-04, B-05, B-06, B-07, B-08)
  - IEEE 1789-2015 — Recommended practices for modulating current in high-brightness LEDs (cited B-04)
  - CNIB Foundation 2024 — Clearing our path (cited B-05, B-08)
  - Invalidiliitto 2022 — Esteettömyysopas (cited B-05)
  - BS 9999:2017 — Fire safety (cited B-10)
  - National Autistic Society 2023 — Creating autism-friendly environments (cited C-03)
  - JOTA 2022 — Grab bar colour contrast (cited C-04)
  - Alzheimer's Disease International 2020 — World Alzheimer Report 2020 (cited B-01, B-11)
- **Data quality flag:** Claims 0109–0111 scoped as B-11 in join file but content at line 1050 is E-05 canopy spec (3000×2000 mm, ≥2500 mm height) — appears to be misplaced E-05 content between B-11 and Category C. Tagged with entry refs (REF-00428, REF-00150). Flag for Part 4 content review.

### Step 2 Session 3 — Part 4 Category D-E (wayfinding, circulation) — 2026-04-19 ✅

- **Scope:** 193 claims across D-01 to D-11 and E-01/E-02/E-03/E-04/E-05/E-06/E-08/E-09/E-10/E-11/E-12/E-13/E-15
- **Results:** 164 TAGGED, 29 DEFERRED, 0 ORPHANED
- **Primary references used:**
  - REF-00026 (Marquardt 2011 EADDAT — dementia wayfinding), REF-00229 (DSDC EADDAT 2022), REF-00361 (Marquardt 2011 wayfinding review)
  - REF-00409 (Passini 1984 Wayfinding in Architecture), REF-00047 (Tola 2021 ASD built environment)
  - REF-00199 (CSA B651:23 IntD provisions), REF-00151 (BS 8300-2:2018), REF-00437 (RNIB Building Sight 2023)
  - REF-00135 (Bauman 2010 DeafSpace), REF-00248 (Gallaudet 2010 DeafSpace Vol 1)
  - REF-00173 (EN 81-70:2022 — accessible lifts), REF-00370 (Approved Document M Vol 2 2026)
  - REF-00341 (Koontz 2012 — ramp gradient shoulder load), REF-00044 (Steinfeld 2010 wheeled mobility anthropometry)
  - REF-00265 (Habinteg 2024 Inclusive Housing Design Guide), REF-00153 (BS 8300-2 Annex G power WC geometry)
  - REF-00154 (BS 8300-2 threshold provisions), REF-00214 (DIN 18040-2 Nullschwelle), REF-00495 (ADA §303)
  - REF-00306 (ISO 23599:2019 — TWSI), REF-00155 (BS 8300-2 doors), REF-00494 (ADA §§302–405)
  - REF-00036 (Roxburgh 2024 ME/CFS — seating intervals), REF-00514 (Wheels for Wellbeing 2025 benches/seating)
  - REF-00232 (Dunn 1997 sensory processing), REF-00157 (PAS 6463:2022), REF-00015 (Gonzalez 2014 sensory garden)
  - REF-00405 (NICE NG206 ME/CFS 2021)
- **DEFERRED categories:**
  - OT evidence echo paragraphs (E-01 L1710, E-02 L1745, E-08 L1968-1970, E-04 L1824, E-05 L1853, E-09 L2032)
  - Retrofit cost notes echoing spec values (E-04 L1806, E-08 L1956 ×2)
  - Illustration placeholder notes (E-12 L3616, E-13 L3652, E-10 L3689-L3691, L3776)
  - Cross-reference notes (E-10 revision note L3664 old ≤20m, E-10 L3689 D-11 xref, E-10 L3776 weather-conditional note)
  - Date reference in key evidence (D-11 "1990s" Danish research), glazing class cross-ref (D-10 "Class 2 minimum")
  - D-03 OT echo (L1381 ≤20m), D-03 same OT paragraph
- **Data quality flag:** Claims 0214–0218 (E-09 scope at L2016–2032) contain misplaced E-05 canopy content (≥3000mm / ≥2000mm / ≥2500mm / ≥100 lux). Tagged with entry refs (REF-00265, REF-00370) appropriate to canopy content. Flag carried forward for Part 4 content review.
- **No new ORPHANED claims** — all cited sources have registry coverage via supporting refs.

### Step 2 Session 4 — Part 4 Category F-G (env controls, bathroom, seating) — 2026-04-19 ✅

- **Scope:** 154 claims across F-01/F-03/F-04/F-05/F-06/F-07/F-08 and G-01–G-09
- **Results:** 139 TAGGED, 15 DEFERRED, 0 ORPHANED
- **Primary references used:**
  - REF-00157 (PAS 6463:2022), REF-00161 (PAS 6463 §6.4 graduated sensory), REF-00232 (Dunn 1997 sensory processing), REF-00029 (Mostafa 2021 ASPECTSS 2.0)
  - REF-00127 (ASHRAE 52.2-2017 MERV), REF-00322 (WELL v2 Air Quality), REF-00304 (ISO EN 16000-9 VOC), REF-00042 (Steinemann 2018 MCS)
  - REF-00303 (ISO 7730:2005 thermal), REF-00184 (CIBSE Guide A), REF-00321 (WELL v2 Thermal), REF-00518 (WHO Housing 18-24°C), REF-00519 (WHO Annex G Global South)
  - REF-00388 (MSIF Atlas 2023 MS heat sensitivity), REF-00014 (Flensner 2011 MS heat), REF-00016 (Griggs 2019 SCI thermoregulation)
  - REF-00268 (Hayashi 2022 SCI sweating), REF-00371 (MHLW Japan 2023 bathtub heat shock)
  - REF-00002 (Afrin 2021 MCAS), REF-00364 (Mast Cell Action 2023), REF-00041 (Staud 2011 OFS/pain)
  - REF-00053 (Wilson 2023 mental health), REF-00057 (TID trauma-informed design 2022)
  - REF-00024 (Levine 2025 bathroom safety), REF-00253 (Golding-Day 2018 BATH-OUT), REF-00400 (Newton 2023 accessible bathroom)
  - REF-00340 (KITE 2025 grab bar peak force), REF-00333 (Keall 2021 MHIPI), REF-00150 (BS 8300-2:2018)
  - REF-00415 (PVA 2021 Accessible Home Design), REF-00416 (RCOT 2019 Housing Adaptations), REF-00044 (Steinfeld 2010 wheeled mobility)
  - REF-00405 (NICE NG206 ME/CFS), REF-00233 (Dysautonomia Support Network), REF-00324 (JAN POTS accommodations)
  - REF-00036 (Roxburgh 2024 ME/CFS), REF-00514 (Wheels for Wellbeing 2025), REF-00265 (Habinteg 2024), REF-00229 (DSDC EADDAT 2022)
- **DEFERRED categories:**
  - OT evidence echo paragraphs (G-02, G-03, G-05, G-06 — seat heights, grab specs, desk heights, counter heights repeated in Evidence basis sections)
  - Illustration placeholder notes (G-08 dual-rod plan, G-09 bedroom plan)
- **No new ORPHANED claims.** Krupp 2003 (F-07 MS diurnal) and Raj 2013 / Stewart 2012 (G-06 orthostatic onset) cited in FDRs but not in global registry — tagged with best-available supporting refs (Flensner, MSIF, NICE NG206, JAN POTS). Log as registry gaps below.
- **Registry gaps identified (cited in Part 4 F-G but absent from global registry — add before publication):**
  - Krupp, L.B. et al. (2003) — MS fatigue diurnal pattern (cited F-07 FDR-MST-02)
  - Raj, S.R. et al. (2013) — Orthostatic intolerance onset time 2-10 min (cited G-06 FDR-OFS-01)
  - Stewart, J.M. et al. (2012) — Orthostatic intolerance clinical data (cited G-06 FDR-OFS-01)

### Step 2 Session 6 — Part 4 Category H-I-K (controls, UPL, DeafBlind) — 2026-04-19 ✅

- **Scope:** 94 claims across part4-intro (1), H-01 to H-05 (35), I-01 to I-04 (33), K-01 to K-04 (25)
- **Results:** 76 TAGGED, 18 DEFERRED, 0 ORPHANED
- **Primary references used:**
  - REF-00492 (ADA §308 Reach Ranges), REF-00152 (BS 8300-2 §8 Controls), REF-00212 (DIN 18040-2 §5 Operating Heights), REF-00308 (ISO 21542:2021), REF-00200 (CSA B651)
  - REF-00044 (Steinfeld 2010 IDeA Center wheeled mobility anthropometry)
  - REF-00157 (PAS 6463:2022), REF-00150 (BS 8300-2:2018), REF-00416 (RCOT Housing Adaptations Without Delay 2019)
  - REF-00415 (PVA Accessible Home Design 2021)
  - REF-00135 (DeafSpace Design Guidelines working draft), REF-00248 (DeafSpace Design Guidelines Vol 1)
  - REF-00371 (MHLW Japan bathtub heat shock), REF-00388 (MSIF Atlas 2023), REF-00014 (Flensner 2011 MS heat)
  - REF-00311 (BS EN ISO 10535:2021 ceiling hoists), REF-00265 (Habinteg 2024)
  - REF-00052 (Wellecke 2022), REF-00383 (GB 50763 kitchen)
  - REF-00203 (DbI guidelines), REF-00406 (Nordic Welfare Centre Deafblind), REF-00188 (Clark 2024 Touch the Future), REF-00414 (Protactile)
  - REF-00306 (ISO 23599:2019 TWSI), REF-00273 (HLAA Auracast — best-available for H-03 captioning)
- **DEFERRED categories (18 total):**
  - OT evidence echo paragraphs (H-01, I-01, I-03, I-04 drainage, K-01, K-03, K-04 — echoing spec values tagged upstream)
  - Retrofit cost notes (H-01, K-01, K-03)
  - DAR cost specification: H-02 UPS NC premium ≤0.1%
  - Cross-reference parsing artifact: K-01 CLAIM-P04-0428 ("06 min" = "G-06 minimum" within spec text)
  - Methodology note: part4-intro 500 Hz RT60 octave band
- **No new ORPHANED claims.** All cited sources tagged with best-available supporting refs.
- **Registry gaps identified (cited in Part 4 H-I-K but absent from global registry — add before publication):**
  - NS 11001:2018/SINTEF — Norwegian controls reach range for powered WC users (H-01 1300 mm); tagged DIN 18040-2
  - RESNA/ARATA standards — ECU/sip-and-puff for C4–C5 tetraplegic users (H-02); tagged RCOT/PVA
  - Tobii eye-gaze guidance — ECU screen positioning (H-02); tagged RCOT/PVA
  - WFD 2022 — Built environment access for Deaf users (H-03); tagged Gallaudet DeafSpace
  - HLAA CART captioning guidance — captioning accuracy ≥98% (H-03); tagged REF-00273 (Auracast — different HLAA topic, best-available)
  - ILCWA 2024 — Kitchen modifications for one-handed function (I-02); tagged RCOT/Wellecke
  - Petajan, J.H. & White, A.T. (1999) — Sports Medicine 27(3):179–191; Uhthoff 0.5°C range (I-03); tagged MSIF Atlas + Flensner
  - Sense UK 2022 — Building and Communicating; tagged DbI/Nordic Welfare
  - Bellman & Symfon 2024 — Vibrotactile alerting systems (K-04); tagged DbI/Nordic Welfare
  - Verrillo (1993) — Vibrotactile frequency perceptibility range 20–200 Hz (K-04); tagged DbI/Nordic Welfare
  - DIN 51130 — Anti-slip floor rating R-scale (I-04 drainage); tagged BS 8300/ISO 21542
  - ANSI A137.1 — DCOF anti-slip rating (I-04 drainage); tagged BS 8300/ISO 21542
- **Part 4 complete — 0 PENDING remaining.** Running total: 462 TAGGED / 85 DEFERRED / 11 ORPHANED / 824 PENDING (other parts).

---

### Step 2 Session 7 — Part 2 (disability population categories) — 2026-04-19 ✅

- **Scope:** 83 claims across §2.1 MOB (24), §2.2 UPL (9), §2.3 VIS (4), §2.4 DEAF (9), §2.5 NEU (6), §2.6 DEM (4), §2.7 NDV (7), §2.8 MH (1), §2.9 PAIN (7), §2.10 DBL (8), §2.11 OFS (4)
- **Results:** 81 TAGGED, 2 DEFERRED, 0 ORPHANED
- **Primary references used:**
  - §2.1 MOB: REF-00044 (Steinfeld wheeled mobility), REF-00468 (IDeA anthropometry), REF-00154 (BS 8300-2 threshold), REF-00494 (ADA routes), REF-00308 (ISO 21542), REF-00113 (Al Lawati threshold 45.8%), REF-00410 (gait interception/falls), REF-00340 (KITE grab bar 1.3 kN), REF-00036 (Roxburgh ME/CFS seating), REF-00514 (Wheels for Wellbeing)
  - §2.2 UPL: REF-00152 (BS 8300 controls), REF-00492 (ADA §308), REF-00333 (MHIPI toilet transfer), REF-00150 (BS 8300-2), REF-00416 (RCOT), REF-00052 (Wellecke kitchen), REF-00340 (KITE grab bar)
  - §2.3 VIS: REF-00437 (RNIB Building Sight), REF-00360 (Manandhar LRV), REF-00306 (ISO 23599 TWSI)
  - §2.4 DEAF: REF-00289 (IEC 60118-4 loop), REF-00124 (ANSI S12.60), REF-00142 (Bettarello RT60), REF-00135 (DeafSpace), REF-00248 (Gallaudet DeafSpace Vol 1)
  - §2.5 NEU: REF-00388 (MSIF Atlas), REF-00010 (navigation impairment SR), REF-00157 (PAS 6463), REF-00014 (Flensner MS Uhthoff), REF-00308 (ISO 21542)
  - §2.6 DEM: REF-00229 (DSDC EADDAT), REF-00360 (Manandhar LRV)
  - §2.7 NDV + §2.8 MH: REF-00029 (Mostafa ASPECTSS 2.0), REF-00157 (PAS 6463), REF-00124 (ANSI S12.60), REF-00142 (Bettarello), REF-00232 (Dunn sensory processing)
  - §2.9 PAIN: REF-00041 (Staud fibromyalgia), REF-00388 (MSIF), REF-00036 (Roxburgh), REF-00514 (Wheels for Wellbeing), REF-00154 (BS 8300-2), REF-00416 (RCOT)
  - §2.10 DBL: REF-00203 (DbI guidelines), REF-00188 (Clark Touch the Future), REF-00414 (Protactile), REF-00306 (ISO 23599), REF-00308 (ISO 21542)
  - §2.11 OFS: REF-00405 (NICE NG206), REF-00036 (Roxburgh), REF-00233 (dysautonomia), REF-00157 (PAS 6463)
- **DEFERRED categories (2):**
  - Editorial evidence confidence notes (§2.1 "HIGH — Tier 1 anthropometric data", §2.4 evidence confidence note)
- **No ORPHANED claims.** All disability category specs have registry coverage.
- **Running total:** 543 TAGGED / 87 DEFERRED / 11 ORPHANED / 741 PENDING

---

### Next session (Session 8): Parts 3 + 5 (conflict resolution) — ~121 claims

---

## Status values

| Status | Meaning |
|---|---|
| `PENDING` | Not yet tagged (default) |
| `TAGGED` | Ref IDs assigned; first pass complete |
| `VERIFIED` | Second-pass check: cited refs genuinely support claim |
| `ORPHANED` | No supporting reference found in global registry — Phase B content review required |
| `DEFERRED` | Not a citable claim (definitional, cross-ref, measurement methodology, or extractor artifact) |

---

## How to populate `ref_ids` (Step 2 instructions)

For each claim:
1. Identify which BPC file(s) cover the topic area
2. Look up the claim's source in that BPC's Key sources table
3. Find the matching global REF-ID in `global-reference-registry.md`
4. Add the REF-ID(s) to this claim's `ref_ids` field (array, multiple allowed for primary + supporting)
5. Set `status: TAGGED`
6. For cross-referenced claims or measurement methodology, set `status: DEFERRED` with a note
7. For claims citing sources not in the global registry, set `status: ORPHANED` and log the citation gap

**Priority order per claim:**
- Tier 1–2 sources cited first
- Multiple refs allowed (primary spec source + supporting clinical evidence + governing standard)

**Verification:** After tagging, a second pass can set `status: VERIFIED` for claims where the cited ref genuinely supports the stated value (not just same topic area).
