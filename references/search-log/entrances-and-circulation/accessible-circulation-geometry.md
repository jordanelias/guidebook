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
  US: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "ADA 2010 §403: accessible route min 915mm clear width. §304: turning space 1524mm diameter or T-shaped. ICC A117.1-2017: 1702mm turning for powered chairs."}
  UK: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "BS 8300-2:2018 §7: corridor min 1200mm (1800mm passing). Turning circle 1500mm. AD M Vol 2."}
  AU: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "AS 1428.1:2021 §7: circulation 1000mm min, 1800mm passing. Turning 2070mm for powered chairs. NCC Section D."}
  CA: {status: THIN, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "CSA B651:2023: turning 1700mm. CSA B652. RHFAC assessment includes circulation."}
  DE: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "DIN 18040-1:2010 §4.3: corridor 1500mm (1800mm in care). Turning 1500mm. Movement area 1500×1500mm."}
  NO: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "TEK17 §12-6: corridor 1500mm for wheelchair. §12-7 manoeuvring area 1500×1500mm."}
  SE: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  ISO: {status: THIN, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "ISO 21542:2021: wheelchair footprint 800×1300mm. Turning 1524mm. Gap with ANSI 1702mm."}
  EU: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true, note: "EN 17210:2021 §7: functional requirement for adequate circulation width. No specific values."}
  FR: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  CH: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  NL: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  DK: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  FI: {status: SEARCHED, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  JP: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  SG: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  NZ: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  KR: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  BR: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ES: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  IT: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  PT: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  IE: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CN: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  IN: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ZA: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  MX: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CL: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CR: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ID: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  BD: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  NG: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  PH: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  EG: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  KE: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  TH: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  CO: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  AR: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  PE: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  GT: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  EC: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  UY: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  MA: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  GH: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  TZ: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}
  ET: {status: NOT-RUN, co1_attempted: false, tier5_attempted: false, tier6_attempted: false}

jurisdiction_summary: >
  KEY DIVERGENCE: turning space — ISO 1524mm vs ANSI/A117.1 1702mm vs CSA 2100mm (U-turn) vs AU 2070mm (powered). Corridor width — UK 1200mm min vs DE 1500mm vs AU 1000mm.

```
