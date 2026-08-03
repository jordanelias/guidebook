-- data_20260522014000_jp_eu_batch_48.sql
-- Statutory + report batch 48: 2 rows verified.
--
-- REF-00252: Japan 厚生労働省 vital statistics — 2023 bathtub drowning (6,073 deaths aged 65+)
-- REF-00277: Eichhorn et al. 2014 — Economic Impact and Travel Patterns of Accessible Tourism in Europe (EC DG ENTR Final Report)

BEGIN TRANSACTION;

-- REF-00252: Japan MHLW bathtub drowning statistics
UPDATE evidence_sources SET
    pub_title = '令和5年(2023)人口動態統計 — Vital Statistics 2023: bathtub drowning deaths in older adults (ICD-10 W65) — 6,073 deaths aged 65+ at home or in residential facilities',
    pub_year = 2023,
    first_author_last = '厚生労働省',
    is_corporate_primary = 1,
    author_display = '厚生労働省 (Ministry of Health, Labour and Welfare, MHLW), Government of Japan — vital statistics (人口動態統計)',
    publisher = '厚生労働省 (MHLW) — Statistics Bureau, Ministry of Internal Affairs and Communications (e-Stat portal)',
    standard_number = 'Vital Statistics令和5年 (2023) — 6,073 deaths aged 65+ in bathtubs at home or in residential facilities (ICD-10 W65, drowning in bathtub); ~2.3× traffic fatalities (2,678) that year; >90% bathtub drowning victims are 65+. Companion: 厚生労働省 令和3年 (2021) figures showed 5,459 bathtub deaths (vs 3,536 traffic). Consumer Affairs Agency estimates ~17,000-20,000 annual bath-related deaths when including bath-induced cardiovascular events (MI, stroke from ヒートショック heat shock).',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'jp-eu-batch-48 2026-05-22T01:40:00Z: web-search verified via nippon.com (English-language MHLW reportage) + barrierfreejapan.com + research literature. Companion peer-reviewed scholarship cites this dataset: Suzuki H et al. 2017 Circ J DOI 10.1253/circj.CJ-16-1066 sudden death phenomenon while bathing; Tai Y et al. 2025 Front Public Health DOI 10.3389/fpubh.2025.1715622 forecasting bathtub-drowning mortality; Tai et al. 2025 Environ Health Prev Med DOI 10.1265/ehpm.25-00286 seasonal variation analysis (99,930 home bathtub drowning deaths 1995-2020 nationwide); Katsuyama et al. 2023 Sci Rep 13:2277 Kagoshima Prefecture prevention strategies; TMIG (Tokyo Metropolitan Institute of Gerontology) survey ~17,000 sudden bath deaths/year. Heat shock prevention guidance: pre-warm bathroom + dressing area, water ≤41°C, immersion <15 min, never bathe alone, hydrate before bathing.',
    url = 'https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/kakutei23/index.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+mhlw-vital-statistics-official',
    last_verified_at = '2026-05-22T01:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:40:00Z jp-eu-batch-48] web-search verified',
    updated_at = '2026-05-22T01:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00252';

-- REF-00277: Eichhorn et al. 2014 EC accessible tourism final report
UPDATE evidence_sources SET
    pub_title = 'Economic Impact and Travel Patterns of Accessible Tourism in Europe — Final Report',
    pub_year = 2014,
    first_author_last = 'Eichhorn',
    first_author_first = 'V',
    is_corporate_primary = 0,
    author_display = 'Eichhorn V, Li G, Miller G, Chen J — University of Surrey School of Hospitality and Tourism Management; consortium: GfK Belgium + University of Surrey + Neumann Consult + ProAsolutions',
    publisher = 'European Commission, Directorate-General Enterprise and Industry (DG ENTR), Brussels',
    standard_number = 'Economic Impact and Travel Patterns of Accessible Tourism in Europe — Final Report; 12-month research study commissioned by EC DG ENTR (Enterprise and Industry); 2012 baseline: 17.6 million accessible-tourism trips in EU (7.2M by PwDs + 10.4M by elderly); companion summary report; companion UNWTO 1st Conference on Accessible Tourism in Europe (San Marino 19-20 Nov 2014) DOI 10.18111/9789284417902; underlying OSSATE project (Buhalis + Eichhorn + Michopoulou + Miller 2005, University of Surrey); ENAT (European Network for Accessible Tourism) partnership',
    jurisdiction = 'EU',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'jp-eu-batch-48 2026-05-22T01:40:00Z: web-search verified via researchgate + academia + ENAT + accessibletourism.org + surrey.ac.uk + euromontana + overton + ec.europa.eu (docsroom). 4-author consortium led by Dr Victoria Eichhorn (Surrey lead investigator). 5 research objectives: examine current/future demand, investigate travel patterns + info provision, evaluate tourist experience demand/supply, estimate economic contribution + employment, propose recommendations. EC report DOI not assigned; rely on author + EC-publisher attribution.',
    url = 'https://ec.europa.eu/docsroom/documents/5566',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+ec-docsroom+enat-official',
    last_verified_at = '2026-05-22T01:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:40:00Z jp-eu-batch-48] web-search verified',
    updated_at = '2026-05-22T01:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00277';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
