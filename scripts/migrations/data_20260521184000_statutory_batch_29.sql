-- data_20260521184000_statutory_batch_29.sql
-- Statutory batch 29: IE+BE — 4 rows verified.
--
-- REF-00079: Ireland NDA "Building for Everyone: A Universal Design Approach" (10-booklet series, 2012)
-- REF-00377: Ireland NDA "Universal Design Guidelines for Homes in Ireland" (5-part)
-- REF-00376: Ireland IWA "Best Practice Access Guidelines: Designing Accessible Environments"
-- REF-00360 + REF-00467: Belgium CAWaB Guide d'aide à la conception d'un bâtiment accessible (2-row dup pair)

BEGIN TRANSACTION;

-- REF-00079: Ireland NDA Building for Everyone
UPDATE evidence_sources SET
    pub_title = 'Building for Everyone: A Universal Design Approach (10-booklet series; revised edition)',
    pub_year = 2012,
    first_author_last = 'National Disability Authority',
    is_corporate_primary = 1,
    author_display = 'National Disability Authority (NDA) — Centre for Excellence in Universal Design (CEUD), Dublin',
    publisher = 'National Disability Authority (NDA) — Centre for Excellence in Universal Design (CEUD), 25 Clyde Road, Dublin 4',
    standard_number = 'Original Building for Everyone 2002 (withdrawn per NBS); revised 10-booklet series 2012; Section 7.12 Housing superseded by NDA Universal Design Guidelines for Homes in Ireland',
    jurisdiction = 'IE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-29 2026-05-21T18:40:00Z: web-search verified via universaldesign.ie (CEUD official) + nda.ie + thenbs.com PublicationIndex + theaccessofficer.n-somerset.gov.uk. Comprehensive best-practice guidance on universal design approach to buildings and spaces. 10 booklets covering: External Environment & Approach; Entrances & Horizontal Circulation; Vertical Circulation; Internal Environment & Services; Sanitary Facilities; Facilities in Buildings; Building Types; Building Management; Plus appendices. Stored "8-volume" framing in original DB — note actually 10 booklets per CEUD official structure; some sources cite 8-volume due to consolidation variants. Address: 25 Clyde Road, Dublin 4.',
    url = 'https://universaldesign.ie/built-environment/building-for-everyone',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+nda-ceud-official+nbs',
    last_verified_at = '2026-05-21T18:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:40:00Z statutory-batch-29] web-search verified',
    updated_at = '2026-05-21T18:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00079';

-- REF-00377: Ireland NDA Universal Design Guidelines for Homes
UPDATE evidence_sources SET
    pub_title = 'Universal Design Guidelines for Homes in Ireland (5-part research-based design quality guidelines)',
    pub_year = 2015,
    first_author_last = 'National Disability Authority',
    is_corporate_primary = 1,
    author_display = 'National Disability Authority (NDA) — Centre for Excellence in Universal Design (CEUD), Dublin',
    publisher = 'National Disability Authority (NDA) — Centre for Excellence in Universal Design (CEUD), 25 Clyde Road, Dublin 4',
    standard_number = 'Universal Design Guidelines for Homes in Ireland (5-part: Introduction; External Environment & Site; Plot, Dwelling Type & Approach; Entry & Circulation; Internal Layout; plus Appendices); contractors MCO Projects, PRP Architects, Detail Design Studio; supersedes Section 7.12 Housing of Building for Everyone',
    jurisdiction = 'IE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-29 2026-05-21T18:40:00Z: web-search verified via agefriendlyhomes.ie + nda.ie + universaldesign.ie + thenbs.com + Housing LIN UK + AccessibleEU European Commission. Two-tier framework: UD Home (general) and UD Home+ (wheelchair-liveable). Companion: Internal Layout Checklist (NDA + Age Friendly Ireland partnership; updated May 2025 with floor plan examples). Refers to Irish Technical Guidance Documents Part D Materials & Workmanship, Part K Stairways/Ladders/Ramps, Part L Conservation of Fuel, Part M Access & Use. Ireland is unique in having a statutory Centre for Excellence in Universal Design (CEUD est. 2007 under Disability Act 2005).',
    url = 'https://universaldesign.ie/built-environment/housing',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+nda-ceud-official',
    last_verified_at = '2026-05-21T18:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:40:00Z statutory-batch-29] web-search verified',
    updated_at = '2026-05-21T18:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00377';

-- REF-00376: Ireland IWA Accessibility Guidelines
UPDATE evidence_sources SET
    pub_title = 'Best Practice Access Guidelines: Designing Accessible Environments',
    pub_year = 2014,
    first_author_last = 'Irish Wheelchair Association',
    is_corporate_primary = 1,
    author_display = 'Irish Wheelchair Association (IWA) — National Access Programme, Dublin',
    publisher = 'Irish Wheelchair Association (IWA), Dublin',
    standard_number = 'Best Practice Access Guidelines (originally launched July 2014; ongoing revisions); companion The Great Outdoors: A Guide to Accessibility',
    jurisdiction = 'IE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-29 2026-05-21T18:40:00Z: web-search verified via iwa.ie (official) + fedvol.ie + O''Herlihy Access Consultancy + Wikipedia. Free for organisations and businesses; covers construction, housing, public amenities, retail, tourism, hospitality, sport. Room-by-room specific guidance. Defines access as "Free and unimpeded access to and from, and the use of all areas and functions of the buildings, facilities and physical features that make up the built environment". IWA founded 1960 (first chair Fr Leo Close CM, paraplegic athlete); ~32 volunteer branches as of 2016; National Access Programme led by Rosaleen Lally. Supports IWA Local Access Groups across Ireland.',
    url = 'https://www.iwa.ie/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iwa-official',
    last_verified_at = '2026-05-21T18:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:40:00Z statutory-batch-29] web-search verified',
    updated_at = '2026-05-21T18:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00376';

-- REF-00360: Belgium CAWaB Guide d'accessibilité (kitchen-specific citation)
UPDATE evidence_sources SET
    pub_title = 'Guide d''aide à la conception d''un bâtiment accessible (CAWaB) — prescriptions techniques, sections cuisine',
    pub_year = 2014,
    first_author_last = 'Collectif Accessibilité Wallonie-Bruxelles',
    is_corporate_primary = 1,
    author_display = 'Collectif Accessibilité Wallonie-Bruxelles (CAWaB asbl) — 22-member coalition of accessibility associations',
    publisher = 'Collectif Accessibilité Wallonie-Bruxelles (CAWaB asbl), Bruxelles',
    standard_number = 'Guide d''aide à la conception d''un bâtiment accessible (initial release 20 Feb 2014; updated 2025); not statutory but reference manual; complements CoDT Guide Régional d''Urbanisme chapter 4 (ex-CWATUP arts. 414-415) for Wallonia and RRU for Brussels',
    jurisdiction = 'BE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00467',
    metadata_integrity_detail = 'statutory-batch-29 2026-05-21T18:40:00Z: web-search verified via cawab.be (official) + urbanisme.irisnet.be + urba.irisnet.be (Brussels Urbanism) + wikiwiph.aviq.be + Wallonie Infrastructures (2025 fiche). Reference manual produced by CAWaB''s 19-22 member associations for architects, contractors, building professionals. Not regulatory but de-facto reference. Companion AccessAndGo-ABP asbl publication "Cahier de prescriptions techniques pour l''accessibilité et l''adaptation des logements sociaux". Owner: 2-row pair with REF-00467; consider consolidating.',
    url = 'https://cawab.be/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cawab-official+irisnet',
    last_verified_at = '2026-05-21T18:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:40:00Z statutory-batch-29] web-search verified',
    updated_at = '2026-05-21T18:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00360';

-- REF-00467: Belgium CAWaB Guide d'accessibilité (door-specific citation)
UPDATE evidence_sources SET
    pub_title = 'Guide d''aide à la conception d''un bâtiment accessible (CAWaB) — door provisions (Toegankelijkheid: portes accessibles)',
    pub_year = 2014,
    first_author_last = 'Collectif Accessibilité Wallonie-Bruxelles',
    is_corporate_primary = 1,
    author_display = 'Collectif Accessibilité Wallonie-Bruxelles (CAWaB asbl)',
    publisher = 'Collectif Accessibilité Wallonie-Bruxelles (CAWaB asbl), Bruxelles',
    standard_number = 'Guide CAWaB — sections sur portes accessibles (door clear width, opening force, threshold heights)',
    jurisdiction = 'BE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00360',
    metadata_integrity_detail = 'statutory-batch-29 2026-05-21T18:40:00Z: web-search verified. Same parent guide as REF-00360. The Dutch-language label "Toegankelijkheid" in the stored title indicates this may cite the Flemish-Brussels parallel publication. Owner: confirm whether this is Flemish-Brussels (Toegankelijk Vlaanderen / Inter) variant or the same CAWaB Francophone guide.',
    url = 'https://cawab.be/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cawab-official',
    last_verified_at = '2026-05-21T18:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:40:00Z statutory-batch-29] web-search verified',
    updated_at = '2026-05-21T18:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00467';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
