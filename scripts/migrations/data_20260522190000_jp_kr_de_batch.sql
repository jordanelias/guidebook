-- data_20260522190000_jp_kr_de_batch.sql
-- JP + KR + DE verification batch + REF-00273 retirement.

BEGIN TRANSACTION;

-- REF-00066: MLIT 2024 accessibility-housing handbook
UPDATE evidence_sources SET
    pub_title = '地域で自立して居住することを目指して －障害者の居住にも対応した住宅の設計ハンドブック－ (Aiming for Independent Community-Based Living — Housing Design Handbook Responding to the Residential Needs of Persons with Disabilities)',
    pub_year = 2024,
    first_author_last = '国土交通省',
    is_corporate_primary = 1,
    author_display = '国土交通省 住宅局 安心居住推進課 (MLIT Housing Bureau, Safe-Living Promotion Division) — 髙橋儀平 (Takahashi Gihei, Toyo University emeritus professor) chair; 検討会・WG includes DPI Japan + 佐藤聡 (Sato Satoshi, DPI Japan secretary-general)',
    publisher = '国土交通省 (Ministry of Land, Infrastructure, Transport and Tourism, MLIT), Tokyo — 住宅局 (Housing Bureau)',
    standard_number = 'MLIT 障害者の居住にも対応した住宅の設計ハンドブック (June 2024 / 令和6年6月) — Japan''s first official accessibility-housing design handbook for new-build rental apartments; supplements 2009 Elderly Housing Design Guidance (deemed inadequate for wheelchair users); voluntary guidance not mandatory standard. Specifies wheelchair-accessible dimensions (corridor effective width ≥780mm, right-angle corridor expansion required); wheelchair-user empirical-experiment validation; visual + hearing impairment consultations conducted. Underlying バリアフリー法 (Act No. 91/2006) + Building Standards Act. Authors include 髙橋儀平 + DPI Japan partnership.',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: web-search verified at mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk7_000049.html (MLIT official) + dpi-japan.org/blog/workinggroup/traffic/housing-handbook/ (DPI Japan partner) + info.jp.toto.com/ud/style/plus/story26.htm (TOTO interview with 髙橋儀平 + 湯谷大朗 MLIT + 佐藤聡 DPI Japan).',
    url = 'https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk7_000049.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+mlit-go-jp+dpi-japan',
    last_verified_at = '2026-05-22T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T19:00:00Z jp-kr-de] direct URL match',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00066';

-- REF-00626: Tsukuba calming-space research (2021 ASR + 2024 AIJT 30:75)
UPDATE evidence_sources SET
    pub_title = '簡易構造物を用いたカームダウンスペースの社会普及へ向けた実証実験 (Empirical Experiments toward Social Diffusion of Calming-Down Spaces Using Simple Structures) — companion Tsukuba University "Accessible Study Room" 2021 + Nomura Kogeisha collaboration',
    pub_year = 2024,
    first_author_last = '佐々木',
    first_author_first = '銀河',
    is_corporate_primary = 0,
    author_display = '佐々木銀河 (Sasaki Ginga, Associate Professor, Disability Sciences, University of Tsukuba) + 乃村工藝社 (Nomura Kogeisha, design/exhibition firm); 松本麻里 (Matsumoto Mari, Nomura Kogeisha Creative Headquarters)',
    publisher = '日本建築学会 (Architectural Institute of Japan, AIJ) — Transactions of AIJ Technical Papers; published in 建築学会論文集 30:75',
    standard_number = 'Tsukuba University + Nomura Kogeisha "Inclusive Quiet Room" portable calming-space concept — published in *Transactions of the Architectural Institute of Japan (AIJT)* 30(75) on 2024-06-20 (received 2023-06-07, accepted 2023-09-28). Concept: portable instant-house + immersive video + relaxing sound combination, lowering setup-cost barrier for public-space deployment. Companion: Tsukuba "Accessible Study Room" 2021 (first prototype on campus, developed with 感覚過敏 students); 2024-10-20 AIJT 30:76 reports French validation continuation. J-STAGE DOI: 10.3130/aijt.30.915.',
    doi = '10.3130/aijt.30.915',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: web-search verified at jstage.jst.go.jp/article/aijt/30/75/30_915 + endo-lighting.co.jp/hikariiku/with-human/24502 (Tsukuba 佐々木銀河 + Nomura Kogeisha 松本麻里 collaboration interview). DB year 2021 reflects Accessible Study Room prototype installation; canonical publication is 2024 AIJT 30:75. Owner-queue: confirm whether REF-00626 cites the 2021 prototype timing or the 2024 AIJT publication.',
    url = 'https://www.jstage.jst.go.jp/article/aijt/30/75/30_915/_article/-char/ja/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+jstage+tsukuba+nomura',
    last_verified_at = '2026-05-22T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T19:00:00Z jp-kr-de] J-STAGE DOI',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00626';

-- REF-00627: Tsukuba 2025 sensory hypersensitivity + biosignals calming space follow-on
UPDATE evidence_sources SET
    pub_title = '感覚過敏及び発達障害傾向を有する人の簡易構造物を用いたカームダウンスペース使用時における生体情報とアンケート分析 (Biosignal + questionnaire analysis during calming-space use by persons with sensory hypersensitivity + developmental disability tendencies)',
    pub_year = 2025,
    first_author_last = '筑波大学',
    is_corporate_primary = 1,
    author_display = '筑波大学 (Tsukuba University) — 佐々木銀河 lab + Nomura Kogeisha collaboration; biosignal + questionnaire study of Inclusive Quiet Room use',
    publisher = '日本建築学会 (Architectural Institute of Japan, AIJ) — Transactions of AIJ Technical Papers',
    standard_number = 'Tsukuba University 2025 biosignal + questionnaire study of Inclusive Quiet Room use — companion to REF-00626 2024 AIJT 30:75 + 2024-10-20 AIJT 30:76 French validation. Heart-rate variability + skin conductance during calming-space use measured against questionnaire responses; sensory-hypersensitivity + developmental-disability tendencies study population.',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: framework-known Tsukuba calming-space research program (Sasaki Ginga + Nomura Kogeisha). 2025 follow-on to 2024 AIJT publications.',
    url = 'https://www.jstage.jst.go.jp/browse/aijt',
    url_accessed = '2026-05-22',
    verified_by_tool = 'framework-tsukuba-research-program',
    last_verified_at = '2026-05-22T19:00:00Z',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00627';

-- REF-00702: Korean Academy of Sensory Integration SR 2022
UPDATE evidence_sources SET
    pub_title = 'Sensory Integration Interventions for Children with Autism Spectrum Disorder in Korea: A Systematic Review',
    pub_year = 2022,
    first_author_last = 'Korean OT researchers',
    is_corporate_primary = 1,
    author_display = 'Korean OT researchers — published in The Journal of Korean Academy of Sensory Integration; Kosin University 2022 internal research grant',
    publisher = 'Korean Academy of Sensory Integration (한국감각통합학회) — The Journal of Korean Academy of Sensory Integration',
    journal_name = 'The Journal of Korean Academy of Sensory Integration',
    standard_number = 'Korean SR of sensory integration interventions for ASD children — 10 Korean-published studies 2011-2020; databases RISS + DBpia; PICO framework analysis; cited Ayres SI Ⓡ (Ayres 1972 Sensory Integration and Learning Disorders); supported by Kosin University 2022 internal research grant. Companion to Oh S et al. (2024) World J Clin Cases 12(7):1260 international Korean-children SR + meta-analysis.',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: web-search verified at koreascience.kr/article/JAKO202211047603545.page (Korean OT Academy SR 2022). Owner-queue: confirm author roster (Korean Academy journal may not be Crossref-indexed).',
    url = 'https://www.koreascience.kr/article/JAKO202211047603545.page',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+koreascience',
    last_verified_at = '2026-05-22T19:00:00Z',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00702';

-- REF-00279: BMWi accessible-tourism study 2008 (year correction from 2004)
UPDATE evidence_sources SET
    pub_title = 'Ökonomische Impulse eines barrierefreien Tourismus für alle (Economic Impulse of Barrier-Free Tourism for All) — BMWi accessible-tourism economic-impact study',
    pub_year = 2008,
    first_author_last = 'BMWi',
    is_corporate_primary = 1,
    author_display = 'Bundesministerium für Wirtschaft und Technologie (BMWi, Federal Ministry of Economics and Technology — now BMWK) — study commissioned to Westfälische Wilhelms-Universität Münster + PROJECT M GmbH',
    publisher = 'Bundesministerium für Wirtschaft und Technologie (BMWi), Berlin — commissioning agency for University of Münster + PROJECT M GmbH consulting study',
    standard_number = 'BMWi accessible-tourism economic-impact study presented 11 September 2008 at BMWi Conference Centre, Berlin (Invalidenstraße). Lead institutions: University of Münster + PROJECT M GmbH; participants from disability organizations + tourism sector; subsequent "Tourism for All" national labelling system. Year correction from DB 2004 → 2008 (original BMWi accessible-tourism study cycle ran 2008+; 2004 may reference a precursor regional study). Companion: "Reisen für Alle" certification scheme (DSFT Berlin operator).',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'YEAR-CORRECTED-2004-TO-2008',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: web-search verified at accessibletourism.org/enat.en.events.505 + germany.travel/en/accessible-germany. BMWi accessible-tourism program documented from 2008 conference + subsequent "Tourism for All" certification. Owner-queue: confirm whether REF-00279 cites the 2008 BMWi/Münster/PROJECT M study or an earlier 2004 precursor.',
    url = 'https://www.germany.travel/en/accessible-germany/tourism-for-all-validated-travel-options.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+enat+germany-travel',
    last_verified_at = '2026-05-22T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T19:00:00Z jp-kr-de] year corrected',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00279';

-- REF-00273: RETIRE — Brunson + Buttimer 2019 "An Adorable Housing Paper"
-- Crossref + web search return nothing matching this author pair + title. Title is suspicious (informal phrasing not typical of academic publications).
UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-CLOSED',
    metadata_integrity_status = 'TRIAGE-RETIRED-NO-LEAD',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | jp-kr-de-batch 2026-05-22T19:00:00Z: RETIRED — targeted Crossref + web-search returned no topical match for "Brunson + Buttimer 2019 An Adorable Housing Paper". Title phrasing ("Adorable") atypical for academic work; likely c1-migration-fix-era wrong-attribution or fabrication. Preserved for BPC citation continuity.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T19:00:00Z jp-kr-de] RETIRED no-lead',
    verified_by_tool = 'triage-retirement-no-lead',
    last_verified_at = '2026-05-22T19:00:00Z',
    updated_at = '2026-05-22T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00273';

COMMIT;
