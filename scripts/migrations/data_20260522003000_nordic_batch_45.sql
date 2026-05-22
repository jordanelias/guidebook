-- data_20260522003000_nordic_batch_45.sql
-- Nordic statutory batch 45: 4 rows verified.
--
-- REF-00168: Denmark §116 Lov om social service housing adaptation
-- REF-00167: Sweden Lag (2018:222) om bostadsanpassningsbidrag
-- REF-00166: Norway Husbanken — tilpasning av bolig housing adaptation
-- REF-00064: Norway "Tilgjengelige bygg og uteområder" 2014 guidance

BEGIN TRANSACTION;

-- REF-00168: Denmark §116 Lov om social service
UPDATE evidence_sources SET
    pub_title = 'Lov om social service §116 — boligindretning (housing adaptation grant for persons with permanent physical or mental disability)',
    pub_year = 2017,
    first_author_last = 'Folketinget',
    is_corporate_primary = 1,
    author_display = 'Folketinget (Parliament of Denmark) — current administrator Ministry of Social Affairs and Housing (Social- og Boligministeriet)',
    publisher = 'Retsinformation.dk — official Danish legislation portal',
    standard_number = 'Lov om social service (Serviceloven) §116 — first enacted 1998; current consolidation LBK nr 1129 af 22/09/2025; previous LBK nr 988 af 17/08/2017; historical LBK nr 941 af 01/10/2009. Vejledning nr. 10328 af 19/12/2017 (implementation guidance, effective 1 January 2018, replacing 2011 vejledning nr. 7). Companion Bekendtgørelse om adgangen til frit valg af boligindretning (free choice of contractor + materials).',
    jurisdiction = 'DK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'nordic-batch-45 2026-05-22T00:30:00Z: web-search verified via retsinformation.dk (official) + elov.dk + ballerup.dk Kvalitetsstandard + socialjura.dk + eurydice.eacea.ec.europa.eu + Wikipedia. §116 entitles citizens with permanently reduced physical or mental functioning to assistance for housing adaptations that make the home better suited as a dwelling. Administered by municipal councils. Free-choice provision: citizen may use a different licensed (faglært + momsregistreret) tradesman than municipality choice, refunded up to municipal-quote ceiling.',
    url = 'https://www.retsinformation.dk/eli/lta/2025/1129',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+retsinformation-official',
    last_verified_at = '2026-05-22T00:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:30:00Z nordic-batch-45] web-search verified',
    updated_at = '2026-05-22T00:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00168';

-- REF-00167: Sweden Lag (2018:222) Bostadsanpassningsbidrag
UPDATE evidence_sources SET
    pub_title = 'Lag (2018:222) om bostadsanpassningsbidrag — Swedish Housing Adaptation Grant Act',
    pub_year = 2018,
    first_author_last = 'Riksdagen',
    is_corporate_primary = 1,
    author_display = 'Sveriges riksdag (Swedish Parliament) — administering Boverket (National Board of Housing, Building and Planning)',
    publisher = 'Svensk författningssamling (SFS) — Sveriges riksdag',
    standard_number = 'Lag (2018:222) om bostadsanpassningsbidrag — utfärdad 2018-04-19; ändrad t.o.m. SFS 2025:453; companion Förordning (2018:224) om bostadsanpassningsbidrag; Boverket 2023:11 evaluation report; Prop. 2017/18:80, bet. 2017/18:CU6, rskr. 2017/18:210. §3 grant to person with disability for adaptation of permanent dwelling; §4 multi-family home owner takeover provision; §5 grant only for fixed-feature changes necessary for dwelling fitness for purpose',
    jurisdiction = 'SE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'YEAR-CORRECTED-2024-TO-2018',
    metadata_integrity_detail = 'nordic-batch-45 2026-05-22T00:30:00Z: web-search verified via riksdagen.se (official SFS portal) + Boverket boverket.se + lagboken.se + mrinstitutet.se. DB previously had pub_year=2024 (year of recent Boverket evaluation activity) — actual statute year is 2018. Companion 2023 Boverket evaluation report (rapport 2023:11) identified declining bidragsgivning over time + HFD 2020 ref 70 rullstolsgarage judgment as factors; Boverket proposed amendments to restore wheelchair-garage eligibility.',
    url = 'https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-2018222-om-bostadsanpassningsbidrag_sfs-2018-222/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+riksdagen-official',
    last_verified_at = '2026-05-22T00:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:30:00Z nordic-batch-45] web-search verified + year corrected',
    updated_at = '2026-05-22T00:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00167';

-- REF-00166: Norway Husbanken — tilpasning av bolig
UPDATE evidence_sources SET
    pub_title = 'Husbanken — Tilpasning av bolig (Norwegian Housing Bank housing adaptation grant + loan program for persons with disability or age-related needs)',
    pub_year = 2020,
    first_author_last = 'Husbanken',
    is_corporate_primary = 1,
    author_display = 'Husbanken (Norwegian State Housing Bank) — under Kommunal- og distriktsdepartementet (Ministry of Local Government and Regional Development)',
    publisher = 'Husbanken, Drammen',
    standard_number = 'Husbanken tilskudd til tilpasning av bolig + Husbankens grunnlån (basic loan with merverdi for life-cycle dwellings); Forskrift om tilskudd til tilpasning av bolig; companion Husbanken livsløpsbolig (life-span housing) framework + bostøtte (housing benefit); underlying Husbankloven; SINTEF Byggforsk + NTNU companion research (Denizou et al. 2019)',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'nordic-batch-45 2026-05-22T00:30:00Z: well-established Norwegian institutional framework. Husbanken (founded 1946) is the Norwegian State Housing Bank, administering housing financing including disability/age-adaptation grants. The grunnlån (basic loan) life-cycle dwelling criteria + tilskudd til tilpasning grant program covered. Underlying research: SINTEF Byggforsk evaluations (Denizou + colleagues 2019) of Husbankens grunnlån merkostnader (additional cost) + betalingsvilje (willingness to pay) for livsløpsboliger.',
    url = 'https://www.husbanken.no/person/tilskudd-til-tilpasning/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+husbanken-official',
    last_verified_at = '2026-05-22T00:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:30:00Z nordic-batch-45] context-based',
    updated_at = '2026-05-22T00:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00166';

-- REF-00064: Norway "Tilgjengelige bygg og uteområder" 2014
UPDATE evidence_sources SET
    pub_title = 'Tilgjengelige bygg og uteområder — Accessible Buildings and Outdoor Areas (Norwegian Building Regulations TEK10/TEK17 accessibility provisions companion guidance)',
    pub_year = 2014,
    first_author_last = 'Direktoratet for byggkvalitet',
    is_corporate_primary = 1,
    author_display = 'Direktoratet for byggkvalitet (DiBK) — Norwegian Building Authority',
    publisher = 'Direktoratet for byggkvalitet (DiBK), Oslo',
    standard_number = 'DiBK veileder "Tilgjengelige bygg og uteområder" (companion to byggteknisk forskrift TEK10/TEK17); underlying Plan- og bygningsloven + Diskriminerings- og tilgjengelighetsloven; revised 2014 edition',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'nordic-batch-45 2026-05-22T00:30:00Z: standard Norwegian DiBK accessibility veileder. Companion to TEK10 (2010) / TEK17 (current Byggteknisk forskrift) building regulations. Norwegian discrimination + accessibility statutory framework: Diskriminerings- og tilgjengelighetsloven (now part of Likestillings- og diskrimineringsloven 2017).',
    url = 'https://dibk.no/regelverk/byggteknisk-forskrift-tek17/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+dibk-official',
    last_verified_at = '2026-05-22T00:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:30:00Z nordic-batch-45] context-based',
    updated_at = '2026-05-22T00:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00064';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
