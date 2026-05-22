-- data_20260522012000_eu_dk_batch_47.sql
-- EU + Denmark statutory batch 47: 2 rows verified.
--
-- REF-00124: AccessibleEU Centre — European Accessibility Resource Centre (EC, launched 4 July 2023)
-- REF-00469: SBi-anvisning 230 — Statens Byggeforskningsinstitut, Aalborg University (BUILD)

BEGIN TRANSACTION;

-- REF-00124: AccessibleEU Centre
UPDATE evidence_sources SET
    pub_title = 'AccessibleEU Centre — European Accessibility Resource Centre',
    pub_year = 2023,
    first_author_last = 'European Commission',
    is_corporate_primary = 1,
    author_display = 'European Commission, DG Employment, Social Affairs & Inclusion — consortium led by Fundación ONCE (Spain) with ENAT + EASPD + Johannes Kepler University Linz + UNE (Asociación Española de Normalización)',
    publisher = 'European Commission, DG Employment, Social Affairs & Inclusion',
    standard_number = 'AccessibleEU Centre — launched 4 July 2023 at European Economic and Social Committee, Brussels (event chaired by EU Equality Commissioner Helena Dalli); flagship of European Commission Strategy for the Rights of Persons with Disabilities 2021–2030; project implementation period 2023–2026; 4 working domains: built environment, transport, ICT (information + communication technologies), accessibility policies; underlying European Accessibility Act + Web Accessibility Directive + Audiovisual Media + Electronic Communications directives; rail accessibility TSI-PRM. EDF (European Disability Forum) partner; AGE Platform Europe participates in launch.',
    jurisdiction = 'EU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'eu-dk-batch-47 2026-05-22T01:20:00Z: web-search verified via accessible-eu-centre.ec.europa.eu (official EC portal) + EDF + EUD + AGE Platform Europe + Alzheimer Europe. One-stop-shop offering: online library on accessibility (direct links, databases, standards, guides, studies, good practices, support materials), trainings, awareness events, network of experts.',
    url = 'https://accessible-eu-centre.ec.europa.eu/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+european-commission-official',
    last_verified_at = '2026-05-22T01:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:20:00Z eu-dk-batch-47] web-search verified',
    updated_at = '2026-05-22T01:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00124';

-- REF-00469: Denmark SBi-anvisning 230
UPDATE evidence_sources SET
    pub_title = 'SBi-anvisning 230 — Anvisning om Bygningsreglement 2010 (BR10) (interpretive guidance for Danish Building Regulations 2010, including accessibility provisions)',
    pub_year = 2014,
    first_author_last = 'Statens Byggeforskningsinstitut',
    is_corporate_primary = 1,
    author_display = 'Statens Byggeforskningsinstitut (SBi) — now BUILD, Aalborg University Department of the Built Environment',
    publisher = 'Statens Byggeforskningsinstitut (SBi) — under Aalborg Universitet (Aalborg University) since 2007',
    standard_number = 'SBi-anvisning 230 — 4th revised edition January 2014; interpretive guidance for Bygningsreglement 2010 (BR10); status alment teknisk fælleseje (common technical knowledge — not legally binding but courts + insurance use as reference; building parties have de facto obligation to know); companion SBi-anvisning 249 (Tilgængelige boliger — Accessible dwellings) for accessibility specifics; successor SBi-anvisning 272 for BR18 (Ernst Jan De Place Hansen, 630pp, ISBN 978-87-563-1870-9, 2018). SBi/BUILD is part of the Sektorforskningsinstitutioner; underlying Bygningsreglementet + Byggeloven.',
    jurisdiction = 'DK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DOORS-DESCRIPTION-LIKELY-INACCURATE-OWNER-QUEUE',
    metadata_integrity_detail = 'eu-dk-batch-47 2026-05-22T01:20:00Z: web-search verified via traeinfo.dk + anvisninger.dk + ucnbib.dk + studiesalg.dk + byggeriogenergi.dk + Wikipedia Statens Byggeforskningsinstitut. DB description "Danish doors guidance" is misleading — SBi-anvisning 230 is the general BR10 interpretation, not a doors-specific guide. Door + accessibility specifics are predominantly in SBi-anvisning 249 (Tilgængelige boliger). Owner-queue: confirm whether REF-00469 should be rebound to SBi-anvisning 249, or whether the citation context is in fact about a BR10 chapter dealing with doors (chapter 3.2.1 BR10).',
    url = 'https://anvisninger.dk/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+sbi-aalborg-official',
    last_verified_at = '2026-05-22T01:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:20:00Z eu-dk-batch-47] web-search verified + doors-description flagged',
    updated_at = '2026-05-22T01:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00469';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
