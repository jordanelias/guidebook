```yaml
slug: accessible-circulation-geometry
query: "lift elevator dimensions wheelchair corridor width passing rest seating automatic door accessible circulation"
last_searched: 2026-03-19 23:00
early_close_triggered: false

native_aliases:
  SV: Hisskorgens mått / korridor fribredd / vilplatser / snusyta / automatiska dörrar [CLEAN]
  NO: Hissdimensjoner / korridor friareal / hvilebenker / snusrom / automatiske dørrer [CLEAN]
  DA: Elevatordimensioner / korridor fribredde / hvilepladser / vendeplads [CLEAN]
  FI: Hissin mitat / käytävän vapaa leveys / levähdyspaikat / kääntymistila [CLEAN]
  FR: Dimensions ascenseur / largeur libre de couloir / aires de repos [CLEAN]
  DE: Aufzugmaße / Flurbreite / Ruhebänke / Bewegungsfläche / DIN 18040 [CLEAN]
  ZH: 电梯尺寸 / 走廊净宽 / 休息座椅 / 轮椅回转空间 [CLEAN]
  JA: エレベーター寸法 / 廊下有効幅員 / 休憩ベンチ / 車いす転回スペース [CLEAN]
  NL: Liftafmetingen / gangbreedte / rustplaatsen / draaicirkel / NEN 9120 [CLEAN]
  ES: Dimensiones ascensor / anchura libre de pasillo / zonas de descanso [CLEAN]
  PT: Dimensões elevador / largura livre de corredor / áreas de descanso [CLEAN]
  KO: 엘리베이터 치수 / 복도 유효 폭 / 휴식 공간 / 편의시설 설치 기준 [CLEAN]
  IT: Dimensioni ascensore / larghezza netta corridoio / aree di sosta [CLEAN]

concept_boundary_warnings:
  - ALL: Rest seating interval has no equivalent statutory concept in any language — derived from OT clinical energy conservation literature only

languages:
  EN: {status: SEARCHED, results: 18, db: [web, ADA, BS8300, Part M, EN 81-70], co1_pass: partial, native_standards_pass: complete}
  SV: {status: SEARCHED, results: 5, db: [Boverket, web], co1_pass: not-run, native_standards_pass: complete}
  NO: {status: SEARCHED, results: 2, db: [web], co1_pass: not-run, native_standards_pass: complete}
  DA: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  FI: {status: SEARCHED, results: 3, db: [web, Finnish F1], co1_pass: not-run, native_standards_pass: complete}
  FR: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  DE: {status: SEARCHED, results: 4, db: [DIN 18040 proxy, web], co1_pass: not-run, native_standards_pass: complete}
  ZH: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  JA: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  NL: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  ES: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  PT: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  KO: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}
  IT: {status: THIN, results: 1, db: [web], co1_pass: not-run, native_standards_pass: partial}

jurisdiction_coverage:
  US: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  UK: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  CA: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  AU: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  IE: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  NZ: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  SG: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  DE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  CH: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  FR: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  BE: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  NL: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  SE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  NO: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  DK: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  FI: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  JP: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  KR: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CN: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  BR: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ES: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  PT: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  IT: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  EU: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  ISO: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}

jurisdiction_coverage_summary:
  searched: [US, UK, AU, DE, SE, NO, FI, EU]
  thin: [CA, IE, NZ, SG, CH, FR, BE, NL, DK, JP, KR, CN, ES, PT, IT, ISO]
  no_data: []
  not_run: [BR]
  co1_complete: []
  co1_not_attempted: [ALL — EN 81-70 is a technical standard; no DPO org produces separate lift dimension guidance]
  tier5_complete: [US, UK, DE, SE, EU]
  tier5_not_attempted: [CA, IE, NZ, SG, CH, FR, BE, NL, NO, DK, FI, JP, KR, CN, BR, ES, PT, IT, ISO]

co1_pass_summary:
  complete: []
  partial: [EN - OFS OT clinical literature only]
  not-run: [SV, NO, DA, FI, FR, DE, ZH, JA, NL, ES, PT, KO, IT]
native_standards_pass_summary:
  complete: [EN, SV, FI, DE]
  partial: [NO, DA, FR, ZH, JA, NL, ES, PT, KO, IT]
  not-run: []
companion_networks: {loaded: [], scholar_targets: 0, retrieved: 0}
citation_mining: {backward: 2, forward: 1, sources_added: 2}
at_database_pass: not-run

top_sources: [EN-81-70-2021, BS-8300-2018, DIN-18040-1-2010, Boverket-BFS-2024, ADA-2010, AS-1428-1-2021, Part-M-2026, Roxburgh-2024-OFS, Omura-2022-energy-conservation, LEIA-2016]
bpc_ref: "accessible-circulation-geometry"
thin_flags: [CA, IE, NZ, SG, CH, FR, BE, NL, DK, JP, KR, CN, ES, PT, IT, ISO — EN 81-70 applies universally via EU adoption; individual jurisdictional standards not retrieved]
no_data_flags: [rest-seating-interval — confirmed NO-DATA across all 14 languages; OT clinical derivation only]
PROVISIONAL: true
ACCEPTED_GAPS: [Co-1 not run — DPO orgs do not produce separate lift dimension guidance; rest seating NO-DATA accepted — no building standard exists in any jurisdiction; 16 jurisdictions THIN for specific lift/corridor standards — EN 81-70 universal applicability accepted as proxy]
```

---

## Backfill Annotation — 2026-03-26 21:45

**Session:** Jurisdiction backfill for PROVISIONAL slugs
**Working document:** `research/all-rooms-backfill-2026-03-26.md`
**Jurisdictions searched this session:** IE, NZ, SG, CH, BE, DK, FI, KR, CN, ES, IT (all 4 slugs) + FR, NL, SE, NO, PT (reach-range only)

**Status changes pending inline update (next session):**
- `residential-entry-and-threshold`: IE/NZ/SG/CH/BE/DK/FI/KR/CN/ES/IT → SEARCHED (Tier 6 confirmed for all; Co-1 partial; Tier 5 partial). PT remains THIN.
- `threshold-and-level-access`: same as above
- `reach-range-and-accessible-controls`: IE/NZ/SG/CH/BE/DK/FI/KR/CN/ES/IT/FR/NL/SE/NO/PT → SEARCHED. JP remains THIN.
- `residential-kitchen-and-task-surfaces`: NO/SE/DK/FI/SG → SEARCHED (mostly THIN/NO-DATA for kitchen-specific). BR remains NOT-RUN.

**Key new sources:**
- BCA Accessibility Code 2025 (SG) — major update from 2019; adds anthropometric data, reach ranges, control device requirements
- NEN 9120:2025 (NL) — new Dutch accessibility standard
- BFS 2024:12 (SE) — recent Swedish update
- TGD M 2022 (IE) — updated from 2010 with rationale statements
- IWA Best Practice Access Guidelines (IE) — strong Co-1 source with values exceeding Part M
- BRANZ Issue Bulletin 662 (NZ) — residential level entry detailing guide
- DALCO Aprehensión criterion (ES) — operable force framework directly relevant to reach-range

**Cross-jurisdiction convergence (threshold/entry):**
- Ramp max: 1:12 universal; preferred: 1:20 (IE IWA, AU, UK BS 8300, ISO 21542)
- Threshold: zero preferred universal; max 13mm (US) / 20mm (NZ, EU) / 25mm with ramp (CH)
- Landing: 1500–1800mm (varies by jurisdiction)

**Cross-jurisdiction convergence (reach-range/controls):**
- US ADA: 380–1220mm
- EN 17210 / most EU: 400–1100mm
- DIN 18040 (DE): 400–1200mm
- AS 1428.1 (AU): 900–1200mm operating devices
- NZ NZS 4121: 1400–1700mm (signs only — higher than all others)

**Cross-jurisdiction convergence (kitchen):**
- Kitchen counter accessibility: no statutory specification in most jurisdictions
- DIN 18040-2 (DE) adjustable 680–1040mm is the only statutory range
- Kitchen is primarily a Tier 5/OT guidance domain

## functional_deficit_pass
status: COMPLETE
session: 2026-03-28
scenarios_run: 2 (d450+fatigue interval [prior session], d450+fatigue alcove geometry [this session])
novel_findings: 3
refines: 0
contradicts: 0
tier0_candidates: 1
note: Interval finding already in BPC. Alcove geometry added this session. Diminishing-return gate fired for interval; did NOT fire for alcove geometry. Tier 0 candidate: rest seating alcove recess geometry.
