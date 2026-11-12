# FA — blind outputs (antagonist, run before reading the handshake leg's conclusions)

Generated 2026-11-12 03:43 UTC. Read-only against `data/guidebook.db`; engine runs on fresh scratch copies under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/fa/` (outside the repository). Every figure below is command output, not typed. `sha256sum data/guidebook.db` before: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`; `PRAGMA user_version` = 125. HEAD at run: `0a17309`.

## 1. Section-Z queries of bu-capability-inventory.md, re-run as written (Q1–Q41 where a query line is given)

```
user_version (125,)
Q1 :: [(8, 0, 'pilot-3', '3xMOB')]
Q1 v_best_practice :: [(0,)]
Q1 v_determination_provenance :: [(0,)]
Q1 v_item_provenance :: [(0,)]
Q1 v_pending :: [(0,)]
Q1 v_divergence :: [(0,)]
Q1 v_code_floor_only :: [(0,)]
Q2 ntables 56 empty ['base_taxonomy_medical', 'case_studies', 'conflicts', 'connection_targets', 'connections', 'external_root_registry', 'extraction_follow_ups', 'gap_mining', 'icf_medical_map', 'identity_medical_map', 'reasoning_doc_citations', 'supersession_check']
Q2 counts [('access_duration', 3), ('access_need_icf', 43), ('access_needs', 17), ('access_stakes', 3), ('adversarial_findings', 193), ('adversarial_passes', 9), ('base_icf', 72), ('base_parameters', 10), ('base_taxonomy_identity', 23), ('base_taxonomy_medical', 0), ('case_studies', 0), ('citation_mining', 38), ('conflicts', 0), ('connection_targets', 0), ('connections', 0), ('convergence_assessment', 5), ('convergence_sources', 69), ('data_migrations', 476), ('decisions', 188), ('determination_gates', 1), ('economics_entries', 1), ('evidence_population_match', 61), ('evidence_source_authors', 142), ('evidence_sources', 59), ('external_root_registry', 0), ('extraction_follow_ups', 0), ('extraction_relations', 57), ('gap_mining', 0), ('gaps', 110), ('icf_medical_map', 0), ('identity_icf_map', 61), ('identity_medical_map', 0), ('lang_jur_map', 70), ('life_stage_modifiers', 2), ('observed_terms', 96), ('parameter_declinations', 1), ('reasoning_doc_citations', 0), ('research_code_leads', 96), ('rooms', 17), ('search_admissions', 61), ('search_candidates', 155), ('search_execution_artefacts', 117), ('search_executions', 203), ('slugs', 106), ('source_locators', 893), ('source_scans', 18), ('source_slug_links', 71), ('source_value_extractions', 214), ('specification_extraction_links', 151), ('specification_source_links', 38), ('specifications', 8), ('supersession_check', 0), ('term_adjudications', 90), ('term_aliases', 2382), ('terms', 94), ('weighting_profile', 5)]
Q3 :: [(3, 'active', 'lower_is_better', None), (4, 'active', None, None), (5, 'active', None, None), (6, 'active', None, None), (7, 'active', None, None), (8, 'active', None, None), (9, 'active', None, None), (10, 'active', None, None), (11, 'active', None, None), (12, 'active', 'lower_is_better', None)]
Q5a :: [(196, 7, 11, 0, 0, 203)]
Q5b :: [('adversarial-pass', 1), ('incidental', 4), ('lead-index', 3), ('planned', 195)]
Q6a :: [('NOT-ADDRESSABLE', 4), ('NULL', 106)]
Q6b :: [(0,)]
Q7 :: [(12,)]
Q8 :: [(105,)]
Q9 :: [(59, 57, 11, 1)]
Q12 :: [(70,)]
Q13 :: [(18, 29, 214)]
Q14 :: [(2, 5, 106)]
Q15 :: [(32, 17, 0)]
Q16a :: [(76, 0)]
Q16b :: [(3, 'ramp gradient', 14)]
Q17 :: [(38, 13)]
Q18a :: [(476,)]
Q18b :: [('2026-09-11 01:20', 188)]
Q21 :: [(23,)]
Q21n :: [('v_registry_duplicate_descriptions',), ('v_open_determination_gates',), ('v_divergence',), ('v_pending',), ('v_evidence_authors',), ('v_convergence_sources',), ('v_code_floor_only',), ('v_item_provenance',), ('v_source_reach_all',), ('v_coverage_jurisdiction',), ('v_coverage_language',), ('v_coverage_branch',), ('v_source_admission',), ('v_coverage_lens',), ('v_root_id_conflicts',), ('v_derived_figure_check',), ('v_value_independence',), ('v_determination_provenance',), ('v_unregistered_roots',), ('v_best_practice',), ('v_research_scope',), ('v_coverage_priority',), ('v_scan_ledger',)]
Q23 :: [(32,)]
Q24 :: [(72, '30,0'), (80, 'viisi prosenttia')]
Q25 :: [('REF-00989', '車椅子の勾配基準は法律で決まってる！スロープがあれば大丈夫と思ってませんか？', None, 'ja', 'VERIFIED', '白倉 栄'), ('REF-00990', '高齢者、障害者等の移動等の円滑化の促進に関する法律施行令（平成十八年政令第三百七十九号）', None, 'ja', 'VERIFIED', '内閣（Cabinet of Japan）'), ('REF-00991', '高齢者、障害者等が円滑に利用できるようにするために誘導すべき建築物特定施設の構造及び配置に関する基準を定める省令（平成十八年国土交通省令第百十四号）', None, 'ja', 'VERIFIED', '国土交通省（Ministry of Land, Infrastructure, Transport and Tourism）'), ('REF-00993', '【バリアフリー】DPI日本会議 総括所見の分析と行動計画②', None, 'ja', 'VERIFIED', 'DPI日本会議（DPI-Japan, Japan National Assembly of Disabled Peoples International）'), ('REF-01019', '장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 1] <개정 2023. 12. 11.> 편의시설의 구조·재질등에 관한 세부기준 (제2조제1항관련)', None, 'ko', 'UNVERIFIED', 'Republic of Korea'), ('REF-01031', '장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 1] <개정 2023. 12. 11.> 편의시설의 구조·재질등에 관한 세부기준(제2조제1항관련)', None, 'ko', 'VERIFIED', 'Republic of Korea')]
Q26a :: [(4, 'cm', 1), (4, 'm', 11), (4, 'mm', 12), (12, None, 1), (12, 'cm', 1), (12, 'm', 13), (12, 'mm', 6)]
Q26b :: [('915', 'mm', 'the clear width of walking surfaces shall be 36 inches (915 mm) minimum.')]
Q27 :: [(22, 'JP', '1:12', 'rise:run ratio', '<=', '勾配は、十二分の一を超えないこと。'), (23, 'JP', '1:8', 'rise:run ratio', '<=', 'ただし、高さが十六センチメートル以下のものにあっては、八分の一を超えないこと。')]
Q29b :: [(18, 11)]
Q32 :: [(70, 19, 48, 0)]
Q33a :: [(2382, 0, 15, 249)]
Q33b :: [('BROADER', 70), ('DEPRECATED', 2), ('DOMAIN', 49), ('NARROWER', 146), ('SYNONYM', 1119), ('TRANSLATION', 996)]
Q34a :: [('DE', 2), ('EN', 112), ('ES', 13), ('FI', 1), ('FR', 8), ('HR', 1), ('IT', 1), ('JA', 1), ('KO', 7), ('NL', 13), ('NO', 2), ('PT', 6), ('SV', 15), ('en', 13), ('fr', 2), ('ja', 3), ('nl', 3)]
Q34b :: [(None, 8), ('EN', 6), ('FI', 1), ('de', 1), ('en', 21), ('es', 3), ('fr', 1), ('ja', 4), ('ko', 2), ('nl', 5), ('no', 1), ('pt', 3), ('sv', 3)]
Q35a :: [(None, 403), ('—', 89), ('INT', 26), ('US', 15), ('mental-health-built-environment', 9), ('https://www.bsigroup.com/en-GB/standards/pas-6463/', 5), ('UK', 5), ('https://www.rickhansen.com/make-change/accessibility-certification-rhfac', 4)]
Q35b :: [('PROMOTED', 1), ('REFERENCE-ONLY', 879), ('RETIRED', 13)]
Q36 :: [('MOB', 'EXACT', 4), ('MOB', 'PARTIAL', 23), ('MOB', 'PROXY', 32), ('MS', 'PARTIAL', 1), ('SCI', 'PARTIAL', 1)]
Q37a :: [(34, 33, 10)]
Q37b :: [('DEFERRED', 24), ('NAMES-EXISTING', 46), ('NAMES-NEW', 6), ('NOT-OURS', 14)]
Q37c :: [(8,)]
Q38 :: [(3, 15), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 13), (10, 13), (11, 14), (12, 0)]
Q39 :: [(0, 94)]
Q40 :: [('TERM-001', 'hellingbaan', 'nl', 'SYNONYM'), ('TERM-001', '傾斜路', 'ja', 'SYNONYM')]
Q41 UNWRITABLE  identity_medical_map.medical_code -> empty table
Q41 UNWRITABLE  icf_medical_map.medical_code -> empty table
Q41 UNWRITABLE  connection_targets.con_id -> empty table
```

## 2. (a) Lens routing: assess_cell.py on fresh scratch copies

Command shape, one fresh `cp data/guidebook.db` per cell: `GUIDEBOOK_DB_PATH=<scratch> python3 scripts/assess/assess_cell.py --db <scratch> --emit-sql <f>.sql --parameter-id <p> --slug stair-ramp-threshold-biomechanics-accessibility <lens flag> --session session_2026-11-12-fa-antagonist --stamp '2026-11-12 00:00:00' --report-json <f>.json`

```
param 3×MOB      provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=f9331c6d7d54
param 3×DEAF     provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=4177fbdf644f
param 3×AUT      provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=cffa29ad15fa
param 3×SCI      provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=7399c075dcd2
param 3×b210     provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=5ce5a1c610c3
param 3×A-NOSOUND provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions=122 nonanchor=0 rso=0 marker=○ cfo=0 sha=87afb6b26659
param 4×MOB      pending      basis=-                                scale=universal  refs=0 sources=1 extractions=24 nonanchor=0 rso=1 marker=- cfo=1 sha=974c12362c9d
param 4×DEAF     pending      basis=-                                scale=universal  refs=0 sources=1 extractions=24 nonanchor=0 rso=1 marker=- cfo=1 sha=7ef424b27111
param 12×BLIND    provisional  basis=T4-6-only(regulatory_stratum_only) scale=universal  refs=10 sources=10 extractions=21 nonanchor=0 rso=1 marker=○ cfo=0 sha=e2833ed14d60
param 9×EPI      pending      basis=-                                scale=universal  refs=0 sources=1 extractions=16 nonanchor=0 rso=1 marker=- cfo=1 sha=de506695137d
param 7×MOB      pending      basis=-                                scale=population refs=0 sources=0 extractions=0 nonanchor=0 rso=0 marker=- cfo=0 sha=4da806a1a2a8
```

Report-JSON diff, parameter 3, every lens against MOB: keys that differ are only `lens`, `lens_key`, `derivation_sha`, `needs_population_assessment`, `source_records` (per-source `population_directness`). State, tier_basis, value_min/max/unit/notations, governing_refs, supporting_refs, confidence, marker, link roles (governing 35 / conditioning 22 / excluded 65) are identical for MOB, DEAF, AUT, SCI, ICF b210 and need A-NOSOUND. Population directness: MOB = PROXY 17, PARTIAL 8, NOT_ASSESSED 5, EXACT 1; every other lens = NOT_ASSESSED 31. Conditioning identical in all six (NON-ANCHORING 27, DOWN-WEIGHTED 4). Parameter 4 MOB vs DEAF: same five keys differ, nothing else.

Code: `gather_sources(conn, parameter_id)`, `gather_findings(conn, parameter_id)`, `gather_confirmers(conn, parameter_id)`, `gather_extraction_links(conn, parameter_id, governing_refs)` take no lens argument (`grep -n 'def gather' scripts/assess/assess_cell.py`). The lens reaches `population_match()` (identity lens only), `derivation_handshake()`, the gate lookup, `sha()` and the row key. So: the GATHER ignores the lens; the engine as a whole does not (population directness and the sha move).

## 3. (b) Retired-only specifications and what the validators examine

```
specifications total / live: (8, 0)
by state: [('pending', 3), ('provisional', 5)]
convergence_assessment rows: (5,)
--- python3 scripts/validate_evidence_state.py | tail -4
OK cell-state machine: 8 cells, 5 convergence rows validated from guidebook.db

PASS: 13 records checked, 0 errors, 0 warnings
EXAMINED: 13
--- python3 scripts/validate_verification_consistency.py | tail -4
OK verification-consistency: 5 stated/provisional specification(s) consistent (data/guidebook.db)
EXAMINED: 5
--- python3 scripts/audit/derivation_handshake_integrity.py | tail -4

  determinations: 0  gates: 1 (1 open)  distinct (population, ICF code) pairs: 56
EXAMINED: 1
VERDICT: CLEAN
--- python3 scripts/audit/judgment_handoff_shape.py | tail -4
  - source_value_extractions.ref_id NOT NULL
  - no UNIQUE index on source_value_extractions
  - source_value_extractions.ref_id -> evidence_sources(ref_id)
PASS: shape holds (source_value_extractions currently 214 rows — shape is checked, not content).
--- python3 scripts/audit/adjudication_integrity.py | tail -4
======================================================================
EXAMINED: 59
VERDICT: PASS   (tier inconsistencies=0)
======================================================================
```

Reading: `validate_evidence_state` (blocking) EXAMINED 13 = 8 cells + 5 convergence rows, all 8 cells retired; `validate_verification_consistency` (blocking) EXAMINED 5 = the five retired provisional rows; `derivation_handshake_integrity` (advisory) prints 'determinations: 0' and EXAMINED 1 (the gate). No live determination is examined by any of them because none exists.

## 4. Probes (c)–(g), own design

```
## (c) mobility split
c1 base_taxonomy_identity codes :: [('ADHD', None, 'active'), ('ALL', None, 'active'), ('AUT', None, 'active'), ('BAR', None, 'active'), ('BLIND', None, 'active'), ('BRAIN', None, 'active'), ('COM', None, 'active'), ('DEAF', None, 'active'), ('DEAFBLIND', None, 'active'), ('DEM', None, 'active'), ('EPI', None, 'active'), ('ID', None, 'active'), ('LMB', None, 'active'), ('LPA', None, 'active'), ('MH', None, 'active'), ('MOB', None, 'active'), ('MOVE', None, 'active'), ('MS', None, 'active'), ('NDV', None, 'active'), ('PAIN', None, 'active'), ('SCI', None, 'active'), ('TALL', None, 'active'), ('VES', None, 'active')]
c2 MOB/AMB/WHEEL-like codes :: [('MOB',)]
c3 tables carrying identity_code :: [('base_taxonomy_identity',), ('identity_medical_map',), ('determination_gates',), ('specifications',), ('identity_icf_map',), ('search_executions',), ('source_value_extractions',), ('connection_targets',)]
c4 extractions by identity_code :: [(None, 2), ('ALL', 34), ('BLIND', 3), ('MOB', 170), ('MS', 2), ('SCI', 3)]
c5 extractions lens columns populated (identity, icf, needs, medical, total) :: [(212, 1, 3, 0, 214)]
c6 device_class :: [(None, 149), ('manual_self_propelled', 18), ('mixed', 7), ('not_device_scoped', 40)]
c7 MOB extractions by device_class :: [(None, 105), ('manual_self_propelled', 18), ('mixed', 7), ('not_device_scoped', 40)]
c8 population match targets :: [('MOB', 'EXACT', 4), ('MOB', 'PARTIAL', 23), ('MOB', 'PROXY', 32), ('MS', 'PARTIAL', 1), ('SCI', 'PARTIAL', 1)]
c9 identity_icf_map for MOB :: [('d410', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d420', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d450', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d455', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d460', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d465', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d470', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d510', 'Biomechanical — ambulation, balance, transfer, wheelchair use'), ('d530', 'Biomechanical — ambulation, balance, transfer, wheelchair use')]
c10 specifications :: [(1, 3, 'MOB', 'pending', 'pilot-3', '2026-09-16 06:01', 2), (2, 3, 'MOB', 'pending', 'pilot-3', '2026-09-16 23:29', 3), (3, 3, 'MOB', 'pending', 'pilot-3', '2026-09-17 21:02', 4), (4, 3, 'MOB', 'provisional', 'pilot-3', '2026-09-17 22:46', 5), (5, 3, 'MOB', 'provisional', 'pilot-3', '2026-09-18 01:48', 6), (6, 3, 'MOB', 'provisional', 'pilot-3', '2026-09-18 02:35', 7), (7, 3, 'MOB', 'provisional', 'pilot-3', '2026-09-18 04:17', 8), (8, 3, 'MOB', 'provisional', 'pilot-3', '2026-09-18 20:12', None)]
c11 determination_gates lens :: [(1, 3, 'MOB', 'UNLINKED', None)]
c12 search_executions identity_code :: [(None, 203)]
## (d) read-once / scan state
d1 scans by mode/scope/method (n, open_pass_done) :: [('catalogue', 'abstract', 'pre-screen', 4, 0), ('catalogue', 'full', 'pre-screen', 12, 0), ('catalogue', 'partial', 'pre-screen', 2, 0)]
d2 catalogue_version / target :: [(12, None, 18)]
d3 scans, distinct sources, with file_sha256, with pages_read :: [(18, 11, 18, 10)]
d4 v_scan_ledger rows and status :: [('EXTRACTED', 94), ('NOT-READ', 417), ('READ-NOTHING-FOUND', 22), ('READ-PARTIAL', 40), ('STATED-ABSENT', 7)]
d5 v_scan_ledger total = live sources x active parameters :: [(580, 58, 10)]
d6 live sources never scanned :: [(47,)]
d7 processing_blocked_reason :: [(None, 59)]
d8 data_capture_status :: [('captured', 53), ('pending', 6)]
d9 extractions with file_anchor / method :: [('full-read', 'absent-confirmed', 1, 1), ('full-read', 'preliminary', 85, 0), ('full-read', 'reviewed', 12, 12), ('full-read', 'verified', 31, 4), ('re-read', 'reviewed', 1, 1), ('skim', 'absent-confirmed', 2, 0), ('skim', 'preliminary', 82, 0)]
d10 extraction_follow_ups :: [(0,)]
## (e) language / jurisdiction
e1 lang_jur_map (rows, languages, jurisdictions, scope_status set) :: [(70, 19, 48, 0)]
e2 lang_jur_map languages :: [('AR', 2), ('BN', 1), ('DA', 2), ('DE', 5), ('EN', 20), ('ES', 11), ('FI', 2), ('FR', 6), ('HI', 1), ('ID', 1), ('IT', 3), ('JA', 1), ('KO', 1), ('NL', 3), ('NO', 1), ('PT', 3), ('SV', 3), ('SW', 2), ('ZH', 2)]
e3 case of language codes: search_executions :: [('DE', 2), ('EN', 112), ('ES', 13), ('FI', 1), ('FR', 8), ('HR', 1), ('IT', 1), ('JA', 1), ('KO', 7), ('NL', 13), ('NO', 2), ('PT', 6), ('SV', 15), ('en', 13), ('fr', 2), ('ja', 3), ('nl', 3)]
e4 evidence_sources.lang_detected :: [(None, 8), ('EN', 6), ('FI', 1), ('de', 1), ('en', 21), ('es', 3), ('fr', 1), ('ja', 4), ('ko', 2), ('nl', 5), ('no', 1), ('pt', 3), ('sv', 3)]
e5 evidence_sources.language (second column) :: [(None, 59)]
e6 term_aliases.language :: [('da', 157), ('de', 191), ('en', 415), ('es', 171), ('fi', 160), ('fr', 170), ('id', 15), ('it', 121), ('ja', 150), ('ko', 157), ('nl', 140), ('no', 132), ('pt', 114), ('sv', 134), ('zh', 155)]
e7 observed_terms.language :: [('DE', 1), ('EN', 63), ('ES', 3), ('FI', 2), ('FR', 1), ('JA', 7), ('KO', 2), ('NL', 10), ('NO', 1), ('PT', 3), ('SV', 3)]
e8 jurisdictions on extractions :: [('US', 39), ('UK', 28), ('SG', 22), (None, 19), ('ES', 18), ('KR', 15), ('PT', 13), ('NL', 7), ('IE', 7), ('FR', 7), ('JP', 6), ('SE', 5), ('BE', 5), ('AU', 4), ('BR', 3), ('UG', 2), ('NZ', 2), ('ISO', 2), ('INT', 2), ('HR', 2), ('DE', 2), ('NO', 1), ('IN', 1), ('FI', 1), ('CA', 1)]
e9 canonical_en non-ASCII / terms :: [(0, 94)]
e10 pub_title_en on non-English sources :: [(24, 0)]
e11 non-Latin authors and their view display :: [('REF-00989', '白倉', '栄一', '白倉 栄')]
e12 non-ASCII claim_text count :: [(82,)]
e13 JurisdictionCode members 36 ['AU', 'BD', 'BR', 'CA', 'CH', 'CN', 'DE', 'DK', 'EG', 'FR', 'ID', 'IE', 'IN', 'JP', 'KE', 'KR', 'NG', 'NL', 'NO', 'NZ', 'SE', 'SG', 'UK', 'US', 'ZA', 'BE', 'ES', 'HR', 'IT', 'PT', 'FI', 'UN', 'UG', 'ISO', 'EU', 'INT']
e14 map jurisdictions not in enum 17 ['AR', 'AT', 'CL', 'CO', 'CR', 'CY', 'EC', 'ET', 'GH', 'GT', 'MA', 'MX', 'PE', 'PH', 'TH', 'TZ', 'UY']
e15 v_research_scope rows whose jurisdiction is not an enum member (19,)
e16 enum members absent from the map ['HR', 'INT', 'ISO', 'UG', 'UN']
e17 retrieval_log name normaliser (NFKD + strip combining), re-implemented from scripts/research/retrieval_log.py:89-90:
    'ガ' -> 'カ'
    'が' -> 'か'
    'パ' -> 'ハ'
    '김' -> '김'
    'Lovrić' -> 'lovric'
    '白倉' -> '白倉'
    'ي' -> 'ي'
    'é' -> 'e'
    'ö' -> 'o'
    'й' -> 'и'
## (f) synthesis tables
convergence_assessment 5 has parameter_id: False | lens cols: [] | jurisdiction: False
convergence_sources 69 has parameter_id: False | lens cols: [] | jurisdiction: False
connections 0 has parameter_id: False | lens cols: [] | jurisdiction: False
connection_targets 0 has parameter_id: True | lens cols: ['identity_code'] | jurisdiction: False
conflicts 0 has parameter_id: True | lens cols: [] | jurisdiction: False
gaps 110 has parameter_id: False | lens cols: [] | jurisdiction: False
reasoning_doc_citations 0 has parameter_id: False | lens cols: [] | jurisdiction: True
supersession_check 0 has parameter_id: False | lens cols: [] | jurisdiction: False
f1 convergence rows reached from specifications (spec, conv, retired?) :: [(1, None, 1), (2, None, 1), (3, None, 1), (4, 4, 1), (5, 5, 1), (6, 6, 1), (7, 7, 1), (8, 8, 1)]
f2 convergence rows not reached from any live specification :: [(5,)]
f3 extraction_relations by relation :: [('audited_against', 8), ('condition_on', 31), ('confirms', 3), ('exceeds', 1), ('insufficient', 4), ('tested_at', 10)]
f4 gaps by status :: [('CLOSED-DECIDED', 9), ('CLOSED-DUPLICATE', 2), ('CLOSED-FIXED', 11), ('OPEN', 88)]
f5 best_practice_synthesis anywhere in schema :: []
## (g) render
g1 views and row counts :: [('v_best_practice',), ('v_code_floor_only',), ('v_convergence_sources',), ('v_coverage_branch',), ('v_coverage_jurisdiction',), ('v_coverage_language',), ('v_coverage_lens',), ('v_coverage_priority',), ('v_derived_figure_check',), ('v_determination_provenance',), ('v_divergence',), ('v_evidence_authors',), ('v_item_provenance',), ('v_open_determination_gates',), ('v_pending',), ('v_registry_duplicate_descriptions',), ('v_research_scope',), ('v_root_id_conflicts',), ('v_scan_ledger',), ('v_source_admission',), ('v_source_reach_all',), ('v_unregistered_roots',), ('v_value_independence',)]
    v_best_practice 0
    v_code_floor_only 0
    v_convergence_sources 69
    v_coverage_branch 89
    v_coverage_jurisdiction 28
    v_coverage_language 21
    v_coverage_lens 41
    v_coverage_priority 7189
    v_derived_figure_check 0
    v_determination_provenance 0
    v_divergence 0
    v_evidence_authors 59
    v_item_provenance 0
    v_open_determination_gates 1
    v_pending 0
    v_registry_duplicate_descriptions 0
    v_research_scope 70
    v_root_id_conflicts 0
    v_scan_ledger 580
    v_source_admission 61
    v_source_reach_all 88
    v_unregistered_roots 0
    v_value_independence 1
g2 weighting_profile rows :: [(5,)]
```

## 5. (g) Walkability instrument, re-run live

`python3 workplan/pipeline-state-graph/walkability.py` (read-only; defaults to `data/guidebook.db` and `governance/stage-map.yaml`). Note the committed `WALKABILITY.md` describes `user_version 101`, 82 tables, 115 foreign keys, 21 views (its own Status line, dated 2026-10-13); the live run below is `user_version 125`, and prints its own counts.

```
tables 56  views 23  fk 90

STAGE-PAIR MATRIX (tables in later stage that reach an earlier stage / tables in earlier stage that reach later; skip = reach without crossing the intermediate stages)
pair                           up  down  skip  recvFK  sendFK  views
base->research                  5     7  None       9       0  v_coverage_priority
base->evidence                  3     3     3       3       2  v_item_provenance,v_source_reach_all,v_value_independence,v_
base->judgment                  4     7     4       7       0  v_value_independence,v_determination_provenance,v_unregister
base->synthesis                 5     7     5       9       0  
base->specification             4     7     4       7       0  v_code_floor_only,v_item_provenance,v_source_reach_all,v_det
base->render                    0     0     0       0       0  
research->evidence              0     0  None       0       3  v_source_admission
research->judgment              0     0     0       0       0  
research->synthesis             0     0     0       0       1  
research->specification         0     0     0       0       0  
research->render                0     0     0       0       0  
evidence->judgment              5     3  None       5       0  v_value_independence,v_determination_provenance,v_unregister
evidence->synthesis             5     2     5       3       0  v_convergence_sources
evidence->specification         4     2     4       2       0  v_item_provenance,v_source_reach_all,v_determination_provena
evidence->render                0     0     0       0       0  
judgment->synthesis             1     1  None       1       2  
judgment->specification         1     1     1       1       0  v_determination_provenance
judgment->render                0     0     0       0       0  
synthesis->specification        3     3  None       2       0  v_divergence,v_pending
synthesis->render               0     0     0       0       0  
specification->render           0     0  None       0       0  

ZIGZAG WALK between non-base stages (shortest undirected path over FKs and view co-reads, not passing through base, infrastructure or unmapped tables; - is a foreign key, ~v~ a view that reads both):
  research<->evidence            search_admissions - evidence_sources
  research<->judgment            gap_mining - gaps - evidence_population_match
  research<->synthesis           gap_mining - gaps
  research<->specification       gap_mining - gaps - specifications
  research<->render              NO PATH
  evidence<->judgment            evidence_sources - evidence_population_match
  evidence<->synthesis           evidence_sources - convergence_sources
  evidence<->specification       evidence_sources - determination_gates
  evidence<->render              NO PATH
  judgment<->synthesis           evidence_population_match - gaps
  judgment<->specification       source_value_extractions - specification_extraction_links
  judgment<->render              NO PATH
  synthesis<->specification      convergence_assessment - specifications
  synthesis<->render             NO PATH
  specification<->render         NO PATH

ZIGZAG, POPULATED EDGES ONLY (an FK counts if some child row has a non-NULL pointer; a view if it returns a row):
  research<->evidence            search_admissions - evidence_sources
  research<->judgment            search_admissions - evidence_sources - evidence_population_match
  research<->synthesis           search_admissions - evidence_sources - convergence_sources
  research<->specification       search_admissions - evidence_sources - determination_gates
  research<->render              NO PATH
  evidence<->judgment            evidence_sources - evidence_population_match
  evidence<->synthesis           evidence_sources - convergence_sources
  evidence<->specification       evidence_sources - determination_gates
  evidence<->render              NO PATH
  judgment<->synthesis           evidence_population_match - evidence_sources - convergence_sources
  judgment<->specification       source_value_extractions - specification_extraction_links
  judgment<->render              NO PATH
  synthesis<->specification      convergence_assessment - specifications
  synthesis<->render             NO PATH
  specification<->render         NO PATH

LATERAL (components of same-stage tables joined through a shared parent or child)
  base            tables 18 components  6  isolated: access_duration, access_stakes, lang_jur_map, life_stage_modifiers, rooms
  research        tables  8 components  4  isolated: gap_mining, research_code_leads, source_locators
  evidence        tables  8 components  1  isolated: 
  judgment        tables  5 components  2  isolated: term_adjudications
  synthesis       tables  8 components  1  isolated: 
  specification   tables  4 components  1  isolated: 
  render          tables  1 components  1  isolated: weighting_profile
  infrastructure  tables  4 components  3  isolated: data_migrations, decisions

RE-ENTRANT FK edges (child stage earlier than parent stage):
  evidence_population_match.gap_id -> gaps  non-null rows 0
  term_aliases.observation_id -> observed_terms  non-null rows 0
  gap_mining.gap_id -> gaps  non-null rows 0
  search_admissions.ref_id -> evidence_sources  non-null rows 61
  base_parameters.direction_ref_id -> evidence_sources  non-null rows 0
  search_executions.mined_ref_id -> evidence_sources  non-null rows 11
  search_candidates.resolved_ref_id -> evidence_sources  non-null rows 7
  source_value_extractions.promoted_to_rdc_id -> reasoning_doc_citations  non-null rows 0

ORPHANS (no FK in/out, no view reads): access_duration, access_stakes, data_migrations, decisions, life_stage_modifiers, research_code_leads, rooms, source_locators, weighting_profile

unFK id columns:

VIEWS spanning >1 stage: 12
  v_code_floor_only: base + specification
  v_convergence_sources: evidence + synthesis
  v_coverage_priority: base + research
  v_determination_provenance: base + evidence + judgment + specification
  v_divergence: synthesis + specification
  v_item_provenance: base + evidence + specification
  v_pending: synthesis + specification
  v_scan_ledger: base + evidence + judgment
  v_source_admission: research + evidence
  v_source_reach_all: base + evidence + specification
  v_unregistered_roots: base + evidence + judgment
  v_value_independence: base + evidence + judgment
views confined to one stage or none: v_best_practice, v_coverage_branch, v_coverage_jurisdiction, v_coverage_language, v_coverage_lens, v_derived_figure_check, v_evidence_authors, v_open_determination_gates, v_registry_duplicate_descriptions, v_research_scope, v_root_id_conflicts
```

Render surfaces in code: `grep -c 'add_parser(' scripts/db.py` lines; no verb named render (`grep -n '"render' scripts/db.py` → none); `ls scripts/generate` = context_map.py owner_browser.html owner_browser_build.py research_contract_hook.py ; stage-map render tables = weighting_profile only.
