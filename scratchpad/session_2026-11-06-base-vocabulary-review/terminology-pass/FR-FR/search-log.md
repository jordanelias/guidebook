# Search log — terminology pass FR/FR (session_2026-11-06-base-vocabulary-review)

Every query or retrieval verbatim. "Prior" is written before the result. Shape note per R14. Empties kept.

## Instrument derivation (database, read-only)

- D1 `select * from research_code_leads where jurisdiction like '%FR%'` — Prior: one or two leads naming the ERP arrêtés. Result: 4 rows (lead_id 43 "Arrêté 2014", 48 "Arrêté 2017", 86 "Arrêté du 20 avril 2017 (accessibilité ERP neufs)" URL legifrance JORFTEXT000034485459, 92 arrêtés 2014+2017). Lead 86 records Légifrance HTTP 403 on every route in session 2026-09-17 and a JS shell at accessibilite-batiment.fr. No lead for logements, IOP-only, or voirie. Shape: exact jurisdiction filter; well-formed.
- D2 `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='FR'` — Prior: 0–2 rows. Result: 1 row, REF-01030 "Guide illustré — Accessibilité des établissements recevant du public et installations ouvertes au public existants" (a ministry guide on EXISTING ERP; commentary, not the instrument). Shape: well-formed.
- D3 `grep -n FR references/standards-registry.md` — Prior: one ERP entry. Result: one entry, "Arrêté du 20 avril 2017 (ERP)", source_url legifrance JORFTEXT000029925726 (that id is the 8 décembre 2014 arrêté, so the entry's URL and its title name different texts — recorded as a registry defect, not corrected here).

## Retrievals
- R1 fetch `https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034485459` (arrêté du 20 avril 2017, ERP neufs/IOP, consolidated). Prior: HTTP 403, as lead 86 recorded on 2026-09-17. Result: 403, artefact 06b29f80ecb9bb6f.html (5528 bytes, block page). Shape: correct identifier; the block is the publisher's, not the query's.
- R2 `http://archive.org/wayback/available?url=www.legifrance.gouv.fr/loda/id/JORFTEXT000034485459` and the `/jorf/id/` form. Prior: a snapshot exists for the consolidated (loda) URL; uncertain whether it carries server-rendered article text. Result: loda snapshot 20241109234132; jorf snapshot 20241111041137.
- R3 fetch `https://web.archive.org/web/20241109234132if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034485459/`. Prior: 200 with full article text (Légifrance renders loda pages on the server). Result: 200, 256842 bytes, artefact 43802a8ee6314644.html; the extracted text holds articles 1 to 24 and annexes 1 to 9, "Version en vigueur au 09 novembre 2024", "Dernière mise à jour des données de ce texte : 03 mai 2019". Annexes 4 and 5 point to images at `legifrance.gouv.fr/jo_pdf.do?id=JORFTEXT000034485459`, not fetched [SKIPPED: diagrams].
- R4 `wayback/available?...JORFTEXT000034485459&timestamp=20261101`. Prior: a 2025 or 2026 snapshot, which would let currency be checked. Result: the nearest is still 20241109. Currency after 2024-11-09 is therefore UNVERIFIED from bytes (the page's own "Dernière mise à jour … 03 mai 2019" suggests no amendment between 2019 and 2024).
- W1 WebSearch `arrêté 24 décembre 2015 accessibilité bâtiments d'habitation neufs legifrance JORFTEXT` (standard). Prior: the Légifrance page for the arrêté du 24 décembre 2015 on new housing (BHC and individual houses), with its JORFTEXT id. Result: see below.
  Result W1: 18 links, none a Légifrance page for the arrêté; prefecture and DREAL leaflets, a Gers prefecture PDF titled "Arrêté du 27 décembre 2015 BHC et MI neufs" (the date of the JO, not of the arrêté), and secondary reports of amendments on 23 March 2016 and 11 September 2020. Shape: the search engine is US-only and the query mixed title words with an identifier prefix; under-specified for an id lookup. Not evidence of absence.
- W2 WebSearch `"Arrêté du 24 décembre 2015 relatif à l'accessibilité aux personnes handicapées des bâtiments d'habitation collectifs et des maisons individuelles neufs"` restricted to legifrance.gouv.fr. Prior: the loda page with its JORFTEXT id.
  Result W2: 10 Légifrance links; the text is JORFTEXT000031692481, official title "… des bâtiments d'habitation collectifs et des maisons individuelles lors de leur construction" (my quoted title, ending "neufs", was wrong: "neufs" belongs to the companion décret n° 2015-1770, JORFTEXT000031692453). Shape: an exact-phrase query with a mistaken title still hit through the domain restriction. The search engine's summary is not a source; nothing is taken from it.
- R5 `wayback/available?url=www.legifrance.gouv.fr/loda/id/JORFTEXT000031692481`. Prior: a snapshot exists.
  Result R5: snapshot 20250208093733.
- R6 fetch `https://web.archive.org/web/20250208093733if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000031692481`. Prior: 200 with full consolidated text. Result: 200, 229163 bytes, artefact 014af9f59dafdd0b.html; "Version en vigueur au 08 février 2025", "Dernière mise à jour des données de ce texte : 18 septembre 2020", articles 1 to 21 and annexes 1 to 7, with amendment markers (arrêtés of 23 March 2016, 11 October 2019, 11 September 2020; Conseil d'État decision 397360-397361 annulling the sas d'isolement dimensions of annexe 2). Annexes 4 and 5 images not fetched [SKIPPED: diagrams]. No direct Légifrance attempt was made for this text: R1 already showed the 403 for the same host and route.

## Absence checks inside the read texts (grep, case-insensitive, on the extracted text; counts are A17/A15)
Each is a check of a concept I expected might be named under a word other than the seed; prior written before running.
- G1 `couloir` — Prior: absent (the arrêtés say "circulation"). Result 0/0.
- G2 `abri`, `couvert` — Prior: no shelter rule. Result abri 0/0; couvert 0/2, both "locaux … couverts" in A15 art. 10 (lighting), not shelter.
- G3 `casier`, `consigne` — Prior: absent. Result 0/0, 0/0.
- G4 `micro-ondes` — Prior: absent (no kitchen-equipment rule in ERP). Result 0/0.
- G5 `température de couleur`, `kelvin` — Prior: absent. Result 0/0, 0/0.
- G6 `luminance`, `réflexion lumineuse` — Prior: absent; contrast is qualitative. Result 0/0, 0/0.
- G7 `banc`, `assise` — Prior: no rest seating on routes. Result banc 0/0; assise 1/1, both "surface d'assise de la cuvette" (WC seat), not seating.
- G8 `rampe` — Prior: absent in A17 (which uses "plan incliné"), present in A15. Result 0/4.
- G9 `ratio`, `rapport` — Prior: no ratio noun. Result: the counts (7/9 and 24/19) are substring and "par rapport à" hits; badly formed (substring) query; the reading itself is what supports "no ratio noun".
- G10 the 169 distinct French aliases held in `term_aliases` (lower(language)='fr'), checked as case-insensitive substrings of both texts — Prior: a handful occur, most do not. Result: 17 occur. A substring hit is not attestation: "inclinaison" occurs only as the inclination of a lift's control support (A17 art. 7-2), not ramp slope; "orientation" occurs only in "relatifs à l'orientation" (signage). Command in pass-record.md.

## Not attempted (logged, not hidden)
- Arrêté du 8 décembre 2014 (ERP existants), arrêté du 15 janvier 2007 and décret n° 2006-1658 (voirie et espaces publics), arrêté du 14 mars 2014 (logements à occupation temporaire ou saisonnière), and the CCH articles themselves: not retrieved, by the budget (depth on two principal instruments).
- The AFNOR standards the arrêtés deem to satisfy their requirements (NF P 98-351:2010, NF P 98-352:2015, NF EN 81-70:2003, NF EN 60118-4, NF S 32-002:2004): not attempted; they are sold by AFNOR. NOT-OBTAINABLE is not claimed, because no attempt was made.
