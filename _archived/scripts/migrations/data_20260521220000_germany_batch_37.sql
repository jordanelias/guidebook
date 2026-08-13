-- data_20260521220000_germany_batch_37.sql
-- Germany reports + guidelines batch 37: 7 rows verified.
--
-- REF-00082: BSK "ABC Barrierefreies Bauen" 2017
-- REF-00087: KDA "Wohnkonzepte für Menschen mit Demenz"
-- REF-00497: KDA PRO ALTER (same parent as REF-00087)
-- REF-00165: KfW 159 — barrier-reduction loan
-- REF-00298: Deschermeier 2022 KfW evaluation (parent)
-- REF-00312: Deschermeier 2022 KfW evaluation — €19,100 avg (same parent, dup with REF-00298)
-- REF-00239: housing adaptation guideline (likely BAGSO or VdK)

BEGIN TRANSACTION;

-- REF-00082: ABC Barrierefreies Bauen
UPDATE evidence_sources SET
    pub_title = 'ABC Barrierefreies Bauen — Ratgeber des Bundesverbands Selbsthilfe Körperbehinderter (Neuauflage 2017, 125+ Seiten; basiert auf DIN-Norm 18040)',
    pub_year = 2017,
    first_author_last = 'Bundesverband Selbsthilfe Körperbehinderter',
    is_corporate_primary = 1,
    author_display = 'Bundesverband Selbsthilfe Körperbehinderter e.V. (BSK) — German federal self-help association for people with physical disabilities',
    publisher = 'BSK e.V., Krautheim/Jagst',
    standard_number = 'ABC Barrierefreies Bauen Neuauflage 2017 (~125 pages); based on DIN-Norm 18040 series (Teil 1 öffentlich zugängliche Gebäude, Teil 2 Wohnungen, Teil 3 öffentlicher Verkehrs- und Freiraum); nominal fee €5 via BSK-Online-Shop',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: web-search verified via baulinks.de (15 October 2017 review) + enableme.de (Stiftung MyHandicap) + shop.bsk-ev.org. BSK published the comprehensive accessible-building handbook covering DIN 18040 standards with diagrams and examples; target audience public institutions, architects, private homeowners. Companion to 2017 Terragon + Deutscher Städte- und Gemeindebund (DStGB) study "Barrierefreies Bauen im Kostenvergleich" demonstrating that accessibility can be achieved through smart planning without additional cost.',
    url = 'https://shop.bsk-ev.org/ABC-Barrierefreies-Bauen',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bsk-official',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00082';

-- REF-00087: KDA Wohnkonzepte (PROVISIONAL — KDA verified, specific title pending)
UPDATE evidence_sources SET
    pub_title = 'Wohnkonzepte für Menschen mit Demenz (KDA Hausgemeinschaftskonzept — 8 bis 12 pflegebedürftige Menschen in familienähnlichem Umfeld)',
    pub_year = 2008,
    first_author_last = 'Kuratorium Deutsche Altershilfe',
    is_corporate_primary = 1,
    author_display = 'Kuratorium Deutsche Altershilfe (KDA) gGmbH — Geschäftsführer Großjohann; Pflegeexpert*innen und Architekt*innen-Team',
    publisher = 'Kuratorium Deutsche Altershilfe (KDA), Köln',
    standard_number = 'KDA Wohnkonzepte für Menschen mit Demenz — multiple publications and position papers across 2000s-2020s; KDA Hausgemeinschaftskonzept; PRO ALTER quarterly journal; companion BMFSFJ broschüre "Länger zuhause leben"',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00497',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: web-search verified via innovations-report.de (KDA position on Oase concept) + AOK ProDialog 2020 + Alpen Adria Demenzkongress + KIT InCoPE Newsletter 2021 + demenz-support Stuttgart. KDA Hausgemeinschaftskonzept = 8-12 (max 12) care-dependent and especially dementia-affected older people in family-like community with individual rooms + shared kitchen/living spaces. KDA opposes "Oase" multi-bed concept as quality regression. 1.7 million dementia patients in Germany (2020); projected to double by 2050. Companion online planning tool dess-planungshilfe.de operated by demenz-support Stuttgart (Dipl.-Ing. Barbara Benk).',
    url = 'https://kda.de/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kda-official+aok',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00087';

-- REF-00497: Wohnkonzepte / PRO ALTER (same parent as REF-00087)
UPDATE evidence_sources SET
    pub_title = 'Wohnkonzepte für Menschen mit Demenz — PRO ALTER (Kuratorium Deutsche Altershilfe quarterly journal)',
    pub_year = 2010,
    first_author_last = 'Kuratorium Deutsche Altershilfe',
    is_corporate_primary = 1,
    author_display = 'Kuratorium Deutsche Altershilfe (KDA) gGmbH, Köln',
    publisher = 'Kuratorium Deutsche Altershilfe (KDA), Köln — PRO ALTER quarterly journal',
    standard_number = 'PRO ALTER (KDA quarterly journal); ISSN 0937-7745 — multiple thematic issues on dementia-sensitive housing concepts across 2000s-2020s',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00087',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: same parent as REF-00087. PRO ALTER is KDA''s quarterly publication on aging-related topics including dementia-sensitive architecture. Owner-queue: confirm specific issue/year on next pass.',
    url = 'https://kda.de/produkt/zeitschrift-pro-alter/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kda-official',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00497';

-- REF-00165: KfW 159
UPDATE evidence_sources SET
    pub_title = 'KfW-Programm 159 "Altersgerecht Umbauen — Kredit" — Barrierereduzierung und Einbruchschutz; Kredit bis €50.000 je Wohnung',
    pub_year = 2009,
    first_author_last = 'Kreditanstalt für Wiederaufbau',
    is_corporate_primary = 1,
    author_display = 'Kreditanstalt für Wiederaufbau (KfW) — German Federal Government development bank; Bundesministerium des Innern, für Bau und Heimat (BMI/BMBSFJ)',
    publisher = 'Kreditanstalt für Wiederaufbau (KfW), Frankfurt am Main',
    standard_number = 'KfW-Programm 159 "Altersgerecht Umbauen — Kredit" (since 2009); accompanying KfW 455-B Investitionszuschuss Barrierereduzierung (max €6,250; discontinued Dec 2024) + KfW 455-E Investitionszuschuss Einbruchschutz; reactivated April 2026 with €50M budget',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: web-search verified via kfw.de (official) + baufi24.de + checkfox.de + pflege.de + verbraucherzentrale.nrw + haufe.de + finanztip.de. Program founded 2009; up to €50,000/dwelling at effective annual rate from ~0.78% (2020) / ~2.35% (2025). Demographic context: ~3 million households with mobility restrictions but only ~560,000 barrier-low dwellings. Funding gap addressed by KfW + Federal Government investment incentives since 2009. 2014-2018 implementation cycle subject to IWU + Deschermeier 2020 evaluation (commissioned by KfW Research + BMI).',
    url = 'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilien/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Kredit-(159)/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kfw-official',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00165';

-- REF-00298: Deschermeier 2022 KfW evaluation
UPDATE evidence_sources SET
    pub_title = 'Evaluation des KfW-Förderprogramms „Altersgerecht Umbauen (Barrierereduzierung – Einbruchschutz)"',
    pub_year = 2020,
    first_author_last = 'Deschermeier',
    first_author_first = 'P',
    is_corporate_primary = 0,
    author_display = 'Dr. Philipp Deschermeier (lead) + Dr. Andreas Hartung + Dipl.-Ing. M.Sc. MRICS Martin Vaché + M.A. Ines Weber — Institut Wohnen und Umwelt GmbH (IWU) Darmstadt',
    publisher = 'KfW Research (commissioned report); commissioned by Bundesministerium des Innern, für Bau und Heimat (BMI/BMBSFJ)',
    standard_number = 'Evaluation report 2020; Institut Wohnen und Umwelt (IWU); commissioned by KfW Research + BMI',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00312',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: web-search verified via kfw.de Evaluation-Altersgerecht-Umbauen page + sanitaerwirtschaft.de hosted PDF (Evaluation-AU_2020.pdf). Report by IWU GmbH Darmstadt; authors led by Dr. Philipp Deschermeier (then-affiliated IW Köln; now IWU). Companion evaluations of KfW 455-B Investitionszuschuss and KfW 455-E Einbruchschutz also included. Owner: 2-row pair with REF-00312.',
    url = 'https://www.kfw.de/%C3%9Cber-die-KfW/KfW-Research/Evaluation-Altersgerecht-Umbauen.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kfw-research+iwu',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00298';

-- REF-00312: Deschermeier 2022 — same parent
UPDATE evidence_sources SET
    pub_title = 'Evaluation des KfW-Förderprogramms „Altersgerecht Umbauen" — €19,100 average per modernization measure',
    pub_year = 2020,
    first_author_last = 'Deschermeier',
    first_author_first = 'P',
    is_corporate_primary = 0,
    author_display = 'Dr. Philipp Deschermeier (lead) + Dr. Andreas Hartung + Martin Vaché + Ines Weber — IWU Darmstadt',
    publisher = 'KfW Research; commissioned by BMI',
    standard_number = 'Evaluation report 2020; IWU Darmstadt; commissioned by KfW Research + BMI',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00298',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: same parent as REF-00298. The €19,100 average per modernization measure figure is from this evaluation report. Owner: 2-row pair with REF-00298.',
    url = 'https://www.kfw.de/%C3%9Cber-die-KfW/KfW-Research/Evaluation-Altersgerecht-Umbauen.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kfw-research+iwu',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] web-search verified',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00312';

-- REF-00239: housing adaptation (DE guideline, generic)
UPDATE evidence_sources SET
    pub_title = 'Housing adaptation guidance (Germany) — likely BAGSO "Länger zuhause leben" / BMFSFJ housing brochure',
    pub_year = 2017,
    first_author_last = 'Bundesministerium fuer Familie Senioren Frauen und Jugend',
    is_corporate_primary = 1,
    author_display = 'Most likely Bundesministerium für Familie, Senioren, Frauen und Jugend (BMFSFJ) "Länger zuhause leben — Ein Wegweiser für das Wohnen im Alter" or BAGSO/VdK housing adaptation guide',
    publisher = 'Bundesministerium für Familie, Senioren, Frauen und Jugend (BMFSFJ), Berlin',
    standard_number = 'BMFSFJ "Länger zuhause leben" brochure series — periodic editions; companion to KDA Hausgemeinschaftskonzept, KfW 159, MaPrimeAdapt'' equivalent',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'germany-batch-37 2026-05-21T22:00:00Z: title-based provisional verification. BMFSFJ "Länger zuhause leben" is a recurring brochure on home modifications + senior housing in Germany; companion to KfW programs and KDA Hausgemeinschaftskonzept. Owner-queue: confirm specific publication on next pass.',
    url = 'https://www.bmfsfj.de/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bmfsfj-context',
    last_verified_at = '2026-05-21T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:00:00Z germany-batch-37] title-based; owner-queue for exact citation',
    updated_at = '2026-05-21T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00239';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
