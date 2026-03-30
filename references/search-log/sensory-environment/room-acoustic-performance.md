```yaml
slug: room-acoustic-performance
query: "room acoustic performance RT60 reverberation disability hearing impairment autism dementia"
last_searched: 2026-03-19 00:00
last_bpc_update: 2026-03-29 00:00
early_close_triggered: false

native_aliases:
  SV: efterklangstid / rumakustik [THIN — SS 25268 covers schools; disability differentiation not confirmed]
  NO: etterklangstid / romakustikk [CLEAN]
  DA: efterklangstid / rumakustik [CLEAN — SBi-anvisning 218]
  FI: jälkikaiunta-aika [CLEAN]
  FR: temps de réverbération / acoustique intérieure [CLEAN — CEREMA/DMA source confirmed]
  DE: Nachhallzeit / Hörsamkeit [CLEAN — DIN 18041:2016 explicitly addresses inclusion/Behinderung]
  ZH: 混响时间 / 室内声学 [CLEAN — GB 50118-2010]
  JA: 残響時間 / 室内音響 [PARTIAL — disability provisions in Barrier-Free Law framework, not acoustic standard]
  NL: nagalmtijd / ruimteakoestiek [THIN]
  ES: tiempo de reverberación / acústica de interiores [CLEAN]
  PT: tempo de reverberação [CLEAN]
  KO: 잔향시간 [NO-DATA — no dedicated search completed]
  IT: tempo di riverberazione [CLEAN — UNI 11532-2:2020 explicitly addresses students with hearing deficits, categoria A3.1/A4]
concept_boundary_warnings:
  - SV: SS 25268 disability-specific differentiation not confirmed; THIN coverage
  - JA: disability-specific RT60 provisions in Barrier-Free Law framework, not acoustic standards
  - KO: no search completed; NO-DATA

languages:
  EN: {status: SEARCHED, results: 17, db: [PubMed, web], co1_pass: partial, native_standards_pass: complete}
  DE: {status: SEARCHED, results: 4, db: [web], co1_pass: not-run, native_standards_pass: complete}
  SV: {status: THIN, results: 2, db: [training-knowledge], co1_pass: not-run, native_standards_pass: partial}
  NO: {status: SEARCHED, results: 3, db: [web], co1_pass: not-run, native_standards_pass: complete}
  DA: {status: SEARCHED, results: 2, db: [web], co1_pass: not-run, native_standards_pass: complete}
  FI: {status: SEARCHED, results: 2, db: [web], co1_pass: not-run, native_standards_pass: partial}
  FR: {status: SEARCHED, results: 3, db: [web], co1_pass: not-run, native_standards_pass: complete}
  ZH: {status: SEARCHED, results: 2, db: [training-knowledge], co1_pass: not-run, native_standards_pass: complete}
  JA: {status: PARTIAL, results: 2, db: [training-knowledge], co1_pass: not-run, native_standards_pass: partial}
  NL: {status: THIN, results: 1, db: [training-knowledge], co1_pass: not-run, native_standards_pass: partial}
  ES: {status: SEARCHED, results: 2, db: [training-knowledge], co1_pass: not-run, native_standards_pass: complete}
  PT: {status: SEARCHED, results: 2, db: [training-knowledge], co1_pass: not-run, native_standards_pass: partial}
  KO: {status: NO-DATA, results: 0, db: [], co1_pass: not-run, native_standards_pass: not-run}
  IT: {status: SEARCHED, results: 3, db: [web], co1_pass: not-run, native_standards_pass: complete}

jurisdiction_coverage:
  US: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  UK: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  DE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  AU: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  CA: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  IE: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  NZ: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  SG: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  CH: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  FR: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  BE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  NL: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  SE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  NO: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  DK: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  FI: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  JP: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  KR: {status: NO-DATA, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CN: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  BR: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ES: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  PT: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  IT: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  EU: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ISO: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}

jurisdiction_coverage_summary:
  searched: [US, UK, DE, AU, CA, NZ, FR, BE, SE, NO, DK, FI, JP, CN, ES, IT, ISO]
  thin: [IE, SG, CH, NL, BR, PT, EU]
  no_data: [KR]
  not_run: []
  co1_complete: []
  co1_partial: [UK, CA]
  co1_not_attempted: [US, DE, AU, IE, NZ, SG, CH, FR, BE, NL, SE, NO, DK, FI, JP, KR, CN, BR, ES, PT, IT, EU, ISO]
  tier5_complete: [US, UK, DE, AU, CA, NZ, FR, BE, SE, NO, DK, FI, JP, IT, ISO]
  tier5_not_attempted: [IE, SG, CH, NL, BR, ES, PT, EU, CN, KR]

co1_pass_summary: {complete: [], partial: [EN, UK, CA], not-run: [DE, SV, NO, DA, FI, FR, ZH, JA, NL, ES, PT, KO, IT]}
native_standards_pass_summary: {complete: [EN, DE, NO, DA, FR, ZH, ES, IT], partial: [SV, JA, NL, PT, FI], not-run: [KO]}
companion_networks: {loaded: [PubMed], scholar_targets: 3, retrieved: 16}
citation_mining: {backward: 16, forward: 3, sources_added: 7}
at_database_pass: not-run

top_sources:
  - ANSI/ASA S12.60-2010/Part 1 (US Tier 6) — RT60 ≤0.3 s DEAF mandatory
  - BB93:2015 Acoustic Design of Schools (UK Tier 5)
  - DIN 18041:2016 Hörsamkeit in Räumen (DE Tier 5)
  - PAS 6463:2022 §10 (UK Tier 5)
  - UNI 11532-2:2020 (IT Tier 5) — most explicit NDV provisions in non-EN standard
  - NS 8175:2019 (NO Tier 5)
  - SBi-anvisning 218 (DK Tier 5)
  - AS/NZS 2107:2016 (AU/NZ Tier 5)
  - GB 50118-2010 §5.3.4 (CN Tier 6)
  - AIJ AIJES-S001-2008 (JP Tier 5)
  - Iglehart 2020 PMC 7229780 (Tier 1) — RT60 ≤0.3 s DEAF
  - Devos et al. 2019 PMC 6950055 (Tier 1/2) — DEM acoustic intervention
  - Bettarello et al. 2021 DOI 10.3390/app11093942 (Tier 3) — NDV/AUT classroom
  - Caniato et al. 2024 (Tier 3) — NDV acoustic, incremental noise exposure
  - Murgia et al. 2022 LSHSS (Tier 3 systematic review)
  - BrainXchange DMA (2011) (CA Tier 2 Co-1)
  - CEREMA/DMA (2019) (FR Tier 2)
  - Amlani & Russo 2016 [REF-RAP-22] — STI compliance ≠ adequate listening (ESCALATED to evidence-auditor)
bpc_ref: "room-acoustic-performance"
thin_flags: [IE, SG, CH, NL, BR, PT, EU, SV, KR]
no_data_flags: [KR]
opus_synthesis_triggered: true
opus_synthesis_ref: "2026-03-29"

functional_deficit_pass:
  status: NOT-RUN
  last_run: null
  scenarios_searched: 0
  novel_findings: 0
  refines_findings: 0
  contradicts_findings: 0
  tier0_candidates: 0
  environments_covered: []
  environments_remaining: [classroom, residential, healthcare-ward, open-plan-office, sensory-room]

bpc_changes_logged:
  - date: 2026-03-29
    items_affected: [A-08, A-13]
    change_summary: >
      A-08 (HVAC NC-25): NC-25 target for DEM and NDV spaces confirmed by Tier 1/2 evidence
      (Devos et al. 2019 PMC 6950055 — Belgian nursing home acoustic intervention; BrainXchange
      DMA 2011 — DEM background noise management). NC-25 (≤35 dB(A)) and RT60 ≤0.5 s in
      occupied common areas established as DEM best-practice target. PCS/OFS population absent
      from all reviewed standards — THIN-BASE disclosure applies to those populations.
      A-13 (RT60 ≤0.4 s / no sound masking): RT60 ≤0.4 s confirmed across 18 jurisdictions.
      No-sound-masking doctrine for NDV/AUT explicitly named in BPC (PAS 6463:2022 §10 + Bettarello
      2021 + Caniato 2024). DEAF population: RT60 ≤0.3 s is now Tier 1 (Iglehart 2020) — stronger
      than A-13's current ≤0.4 s; A-13 spec is below best practice for hearing device users.
      REF-RAP-22 (Amlani & Russo 2016) escalated to evidence-auditor: STI compliance ≠ adequate
      listening conditions; caveat required on A-13 acoustic treatment specification language.
      Citation mining: 7 new sources added (REF-RAP-11 through REF-RAP-17 partial; RAP-30/31).
      RAP-ID reconciliation completed 2026-03-29 (canonical IDs REF-RAP-18–31 established).
    opus_synthesis: true
    gaps_raised: [GAP-RAP-01]
```
