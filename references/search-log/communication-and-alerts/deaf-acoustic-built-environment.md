```yaml
slug: deaf-acoustic-built-environment
query: "Deaf hard of hearing acoustic environment reverberation hearing loop STI cochlear implant built environment"
last_searched: 2026-03-19 01:45
supplement_run: 2026-03-28
early_close_triggered: false

native_aliases:
  SV: hörselslingor / akustik för hörselskadade / efterklangstid [CLEAN]
  NO: teleslynge / romakustikk for hørselshemmede / etterklangstid [CLEAN]
  DA: høreteleslynge / rumakustik for hørehæmmede / efterklangstid [CLEAN]
  FI: induktiosilmukka / kuulovammaisten akustiikka / jälkikaiunta-aika [CLEAN]
  FR: boucle magnétique / acoustique pour malentendants / temps de réverbération [CLEAN]
  DE: Induktionsschleife / Raumakustik für Schwerhörige / Nachhallzeit / DIN 18041 [CLEAN]
  ZH: 感应线圈 (gǎnyìng xiànquān) / 听力障碍声学 / 混响时间 [CLEAN]
  JA: ヒアリングループ / 聴覚障害者用音響 / 残響時間 [CLEAN]
  NL: ringleiding / akoestiek voor slechthorenden / nagalmtijd [CLEAN]
  ES: bucle magnético / bucle de inducción / acústica para hipoacúsicos [CLEAN]
  PT: loop de indução / acústica para deficientes auditivos / tempo de reverberação [CLEAN]
  KO: 청각장애인용 루프 시스템 / 청각 환경 / 잔향 시간 [CLEAN]
  IT: anello ad induzione / acustica per sordi / tempo di riverberazione [CLEAN]

concept_boundary_warnings:
  - ZH: GB 50763 addresses hearing loop provision but RT60 targets for hearing-impaired not specified; Chinese research uses 混响时间 (hùnxiǎng shíjiān) for reverberation time; CI acoustic environment research published in Chinese rehabilitation medicine journals not built-environment databases. Co-1 supplement pass 2026-03-28: 中国聋人协会 (CDPF) searched; no acoustic built-environment design guidance found; THIN confirmed.
  - JA: バリアフリー法 specifies hearing loop (ヒアリングループ) provision but not RT60 targets; Japanese CI acoustic research predominantly in audiology not built environment; MLIT does not specify acoustic performance targets for DEAF population. 全日本ろうあ連盟 searched; hearing loop advocacy confirmed; no RT60/STI guidance.

languages:
  EN: {status: SEARCHED, results: 20, db: [IEC-60118-4, BS8300, PubMed-CI-acoustics, HearingLoss-HLAA, RNID, Center-for-Hearing-Access, Bluetooth-SIG-Auracast], co1_pass: complete, native_standards_pass: complete}
  SV: {status: SEARCHED, results: 4, db: [HRF, BBR-acoustics, SS-EN-60118-4], co1_pass: partial, native_standards_pass: complete}
  NO: {status: SEARCHED, results: 3, db: [HLF, NS-8175, TEK17-acoustics], co1_pass: partial, native_standards_pass: complete}
  DA: {status: SEARCHED, results: 3, db: [DanmarksAudiologiska, BR18-acoustics, DS-EN-60118-4], co1_pass: partial, native_standards_pass: complete}
  FI: {status: SEARCHED, results: 3, db: [Kuuloliitto, Asetus241-acoustics, SFS-EN-60118-4], co1_pass: partial, native_standards_pass: complete}
  FR: {status: SEARCHED, results: 4, db: [FNSF, CEREMA-acoustique, NF-EN-60118-4, arrêté-ERP], co1_pass: partial, native_standards_pass: complete}
  DE: {status: SEARCHED, results: 6, db: [DGB, DIN18041, DIN-VDE-0834, REHADAT-check, ScienceDirect-CI-DIN18041], co1_pass: partial, native_standards_pass: complete}
  ZH: {status: THIN, results: 2, db: [GB50763-check, CNKI-check, CDPF-2026], co1_pass: attempted-no-data, native_standards_pass: complete}
  JA: {status: THIN, results: 2, db: [全日本ろうあ連盟-check, MLIT-check], co1_pass: partial, native_standards_pass: complete}
  NL: {status: SEARCHED, results: 3, db: [NEN9120-2025, NEN-EN-60118-4, Patiëntenvereniging], co1_pass: partial, native_standards_pass: complete}
  ES: {status: SEARCHED, results: 3, db: [CNSE, CTE-HR, UNE-EN-60118-4], co1_pass: partial, native_standards_pass: complete}
  PT: {status: SEARCHED, results: 3, db: [FENEIS, NBR9050-acoustics, NBR-IEC-60118-4], co1_pass: partial, native_standards_pass: complete}
  KO: {status: SEARCHED, results: 3, db: [한국농아인협회, 편의증진법-acoustics, KS-IEC-60118-4], co1_pass: partial, native_standards_pass: complete}
  IT: {status: SEARCHED, results: 3, db: [ENS, DM236-acoustics, CEI-EN-60118-4], co1_pass: partial, native_standards_pass: complete}

co1_pass_summary:
  complete: [EN]
  partial: [SV, NO, DA, FI, FR, DE, JA, NL, ES, PT, KO, IT]
  attempted-no-data: [ZH]
  not-run: []

native_standards_pass_summary:
  complete: [EN, SV, NO, DA, FI, FR, DE, ZH, JA, NL, ES, PT, KO, IT]
  partial: []
  not-run: []

companion_networks:
  loaded: [Network-A-Deaf-Design]
  scholar_targets: 5
  retrieved: 4

citation_mining:
  backward: 8
  forward: 5
  sources_added: 2

at_database_pass: complete

top_sources:
  - IEC-60118-4-2014-AMD1-2017
  - DIN-18041-2016
  - Badajoz-Davila-2020-JASA
  - HLAA-Auracast-2025
  - BS8300-2-2018

thin_flags: [ZH, JA, BE, BR, CH, SG, NZ]
no_data_flags: []
bpc_ref: "deaf-acoustic-built-environment"

supplement_actions:
  - Added jurisdiction_coverage block — 24-jurisdiction schema back-mapped from language data
  - Verified Auracast IEC 60118-17 status: still expected late 2027 (unchanged; BPC dual-provision recommendation current)
  - NL standard updated: NEN 9120:2025 supersedes NEN 1814:2001 (standards-registry.md)
  - SE standard updated: BFS 2024:12 / ALM 2 in force 1 September 2024 (standards-registry.md)
  - ZH Co-1 supplement pass: 中国聋人协会 (CDPF) searched; no acoustic built-environment guidance; THIN confirmed
  - JA Co-1 partial confirmed: 全日本ろうあ連盟 loop advocacy confirmed; no RT60/STI guidance

jurisdiction_coverage:
  DE: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  BE: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  NO: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  FR: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  BR: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  JA: {status: THIN, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  CA: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  CH: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  AU: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  UK: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  US: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  EU: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  ISO: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  SG: {status: THIN, co1_attempted: false, tier5_attempted: true, tier6_attempted: true}
  SE: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  DK: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  FI: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  CN: {status: THIN, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  IE: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  NZ: {status: THIN, co1_attempted: false, tier5_attempted: false, tier6_attempted: true}
  KR: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  ES: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  NL: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}
  IT: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: true}

jurisdiction_coverage_summary:
  searched: [DE, NO, FR, CA, AU, UK, US, EU, ISO, SE, DK, FI, IE, KR, ES, NL, IT]
  thin: [BE, BR, JA, CH, SG, CN, NZ]
  no_data: []
  not_run: []
  co1_complete: [EN]
  co1_attempted: [DE, NO, FR, CA, AU, UK, US, SE, DK, FI, IE, KR, ES, NL, IT, JA, CN]
  co1_not_attempted: [BE, BR, CH, SG, NZ, EU, ISO]
  tier5_complete: [DE, NO, FR, CA, AU, UK, US, SE, DK, FI, IE, KR, ES, NL, IT, JA, CN, SG]
  tier5_not_attempted: [BE, BR, CH, NZ]

completeness_gate_post_supplement:
  jurisdictions_present: 24
  co1_attempted_count: 17
  co1_gate_threshold: 12
  co1_gate_pass: true
  tier5_attempted_count: 20
  tier5_gate_threshold: 8
  tier5_gate_pass: true
  best_practice_synthesis: POPULATED
  citation_mining: POPULATED
  native_aliases: POPULATED
  gate_result: PASS

status_post_supplement: COMPLETE
```
