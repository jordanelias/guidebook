# Equivalents search log — FR-FR (France), session_2026-11-06-base-vocabulary-review

Every web query and fetch, in order. The prior line is written before the call (fetches: by the same shell command, before `fetch()`). Results are what came back; notes on query shape follow. Empties kept. Jurisdiction of every source is recorded in `equivalents.tsv`.

## Tier 1: second reading of the two arrêtés already held (local text, no fetch)
- Prior: parking will be named "places de stationnement adaptées" (A17 art. 3); lifts "ascenseur" and "appareil élévateur vertical"; "PMR" will not occur in either arrêté; the umbrella word will be both "accessible" and "adapté".
- Method: `grep -o -i` over `text/43802a8ee631.txt` (A17) and `text/014af9f59daf.txt` (A15) for stationnement, ascenseur, élévat, plate-forme, mobilité réduite, PMR, handicap, fauteuil roulant, adapt, symbole, pictogramme, cabine, escalier mécanique, plan incliné mécanique, trottoir roulant.
- Result: parking forms "place(s) de stationnement adaptée(s)", "places adaptées", "emplacements adaptés et réservés", "espace de stationnement adapté"; lift forms "ascenseur", "élévateur", "appareil élévateur vertical", "plate-forme élévatrice", "escalier mécanique", "plan incliné mécanique", "équipement mobile"; "PMR" 0 hits in both; "personne(s) à mobilité réduite" occurs (doors, landings); "adapté" and "accessible" are both applied to "cabinet d'aisances" within A17 art. 12. Prior confirmed except "équipement mobile" (not expected).

## Tier 2-5 discovery queries (WebSearch, US-hosted index)

### QUERY "code de la route R417-11 stationnement réservé carte mobilité inclusion"
- Prior: Légifrance article page for R417-11 (stationnement très gênant on places réservées) and service-public.fr pages.
- Result: 20 links, no Légifrance or service-public page; mostly municipal arrêtés (Melun, Avignon, Amboise, Mérignac) titled "emplacement(s) réservé(s) aux personnes à mobilité réduite" and one "place pmr" file name. Search-engine summary not used as attestation.
- Note: the article number pulled municipal orders that cite it, not the code; useful for tier 4.

### FETCH https://www.ville-melun.fr/images/2026.288-Création_demplacement_réservé_aux_personnes_à_mobilité_réduite.pdf
- Prior (written before the call): title form 'emplacement réservé aux personnes à mobilité réduite' plus 'carte mobilité inclusion' 'stationnement pour personnes handicapées' and R417-11 wording; possibly GIG-GIC as old card
- Result: status 404, 2003 bytes, sha256 12438c5464296efa90234e2870a77731913d61936b1488039c0cbe3e6ea62aed, artefact 12438c5464296efa.html, text 12438c546429.txt (561 chars)

### FETCH https://www.merignac.com/sites/default/files/2025-11/39-bis-gerard-blot-place-pmr.pdf
- Prior (written before the call): body text likely 'emplacement réservé' / 'personnes handicapées'; 'PMR' maybe only in the file name
- Result: status 200, 181195 bytes, sha256 e3251a287b96cc43a1cd0f81c7a2fd57fa537e68e87cb5f96d63ba6bdbf721e1, artefact e3251a287b96cc43.pdf, text e3251a287b96.txt (2958 chars)
- Note: Melun 404 likely from unencoded accents in the URL; Mérignac is an OCR text layer (typos like "intenninistérielle"); body uses "emplacement réservé", "PMR" only in the file name.

### FETCH https://www.melun.fr/images/01-DOC/ARRETES/2023/2023682_-_Creation_de_quatre_emplacements_reserves_aux_personnes_a_mobilite_reduite.pdf
- Prior (written before the call): title 'emplacements réservés aux personnes à mobilité réduite'; body cites CMI 'stationnement pour personnes handicapées'
- Result: status 200, 3862 bytes, sha256 a3d7cdfa6d1bc41d3b0eb89fa6e5b41b2924826a26da49156554e0c0fa42d5c4, artefact a3d7cdfa6d1bc41d.html, text a3d7cdfa6d1b.txt (190 chars)
- Note: Melun returned a JavaScript anti-scraper shell (190 chars). Empty; not retried via Wayback (budget).

### QUERY "service-public.fr carte mobilité inclusion stationnement places réservées"
- Prior: a service-public.fr vosdroits page using "places réservées aux personnes handicapées" and "CMI stationnement"; possibly the old "carte de stationnement" and "GIG/GIC".
- Result: no service-public.fr page; ecologie.gouv.fr "L'accessibilité du stationnement" pages, MDPH leaflets (Tarn-et-Garonne, Isère), a Lille Métropole "Pmr" leaflet, municipal orders. Summary text not used.
- Note: the ministry page is the better tier-4 target.

### FETCH https://www.ecologie.gouv.fr/politiques-publiques/laccessibilite-du-stationnement
- Prior (written before the call): 'places adaptées et réservées', 'carte mobilité inclusion mention stationnement', maybe 'GIG-GIC' as former card, 'PMR' possible
- Result: status 200, 185884 bytes, sha256 50baec70a17f951b94ecc020062d22bdfc3d982fd7ecc440be45f3b8829590ab, artefact 50baec70a17f951b.html, text 50baec70a17f.txt (79169 chars)

### FETCH https://competences.isere.fr/mda38/Lists/FichesPratiques/Attachments/39/carte_mobilite_inclusion_stationnement_B.1.11.pdf
- Prior (written before the call): 'places réservées', 'CMI-S' or 'CMI stationnement', 'carte européenne de stationnement' as former name
- Result: status 200, 980 bytes, sha256 4bfb6bfd455646bfaca8bcd8fd6b8e9d2e80a5f3e233ee3b6335ee002c6fd651, artefact 4bfb6bfd455646bf.html, text 4bfb6bfd4556.txt (1 chars)

### FETCH https://www.lillemetropole.fr/sites/default/files/2020-12/Pmr%206p%20triptyque%20210x100mm%2007.pdf
- Prior (written before the call): 'PMR' as label, 'places PMR' or 'stationnement PMR'
- Result: status 200, 977613 bytes, sha256 aab7e4c3621d2f444690618a9252d8a61520caea1ae4853ea59795f6372e7e82, artefact aab7e4c3621d2f44.pdf, text aab7e4c3621d.txt (6377 chars)
- Note: ministry page (ecologie.gouv.fr) is rich: "places réservées", "places adaptées et réservées", "CMI stationnement (CMI S)", "carte européenne de stationnement", "personnes handicapées et des personnes à mobilité réduite (PMR)". MDPH Isère returned a 980-byte HTML stub (empty). Lille leaflet: "places de stationnement réservées aux personnes en situation de handicap", "emplacements réservés", "une place avec une « bande bleue »"; "PMR" only in the file name. PDFs re-extracted without -layout (column interleaving); helper changed for later PDFs.

### QUERY "instruction interministérielle signalisation routière panonceau M6h stationnement handicapés pdf"
- Prior: IISR 4e partie (signalisation de prescription) PDF on equipementsdelaroute or securite-routiere; the panonceau names the users ("GIG-GIC" in older editions; "personnes handicapées" now) and the symbol "fauteuil roulant".
- Result: IISR parts on Cerema and DDT hosts (1re, 4e, 5e partie), a ministry leaflet "Stationnement réservé handicapés" (Val-d'Oise prefecture copy), an Essonne prefecture note, a Paris PDF, sign vendors and driving-school pages (not used). Summary claims (art. 55-3, M6h) unverified until bytes read.

### FETCH https://www.msr25.doubs.developpement-durable.gouv.fr/IMG/pdf/iisr_4eme_partie_signalisation_de_prescription.pdf
- Prior (written before the call): art. 55 on reserved parking for disabled users with B6d + M6h; panonceau wording; version may be dated
- Result: status 200, 8232756 bytes, sha256 fbef33f84044bc3a6406bfa6ba64ffc23413b57d6f38d3174545d7d4482d5c50, artefact fbef33f84044bc3a.pdf, text fbef33f84044.txt (87260 chars)

### FETCH https://www.val-doise.gouv.fr/index.php/contenu/telechargement/9146/69815/file/Stationnement_reserve_handicapes_MEDDE.pdf
- Prior (written before the call): 'emplacement réservé', 'GIG-GIC' as former mention, 'symbole international d accessibilité' maybe
- Result: status 200, 1604737 bytes, sha256 d7fc387e4d14ea7639085af1376e326ebae2784d916e015dc547fca7380d0d18, artefact d7fc387e4d14ea76.pdf, text d7fc387e4d14.txt (26427 chars)

### FETCH https://cdn.paris.fr/paris/2019/07/24/b1df9af3fe20382ffef1858dffb0c4aa.pdf
- Prior (written before the call): 'places GIG-GIC' or 'places réservées aux personnes handicapées'; unknown content
- Result: status 200, 7705799 bytes, sha256 e0b800abda3469fc7ce012480b6c0674aff7be96914ce69c30859bbe2bbb9bd7, artefact e0b800abda3469fc.pdf, text e0b800abda34.txt (58607 chars)
- Note: IISR 4e partie consolidated VC20190109 (documentary value only, per its own avertissement), p.16 art. 55 C-2: "emplacements … réservés aux véhicules utilisés par les personnes titulaires de la carte de stationnement" (M6h). Ministry guide "Le stationnement réservé aux personnes handicapées ou à mobilité réduite" (MEDDE/METL, parution octobre 2012) distinguishes "place de stationnement réservée" (legal) from "place de stationnement aménagée" (dimensioned) and records outdated "macaron GIG-GIC" and panonceau "Interdit sauf GIG-GIC". Ville de Paris "Guide de la signalisation verticale à Paris" (2010, validated 29/08/2011) p.16 "(ex GIG-GIC)". Prior partly wrong: the current M6h carries the wheelchair symbol, not a user-group text.

### QUERY "arrêté du 15 janvier 2007 accessibilité voirie espaces publics emplacement réservé légifrance"
- Prior: Légifrance JORFTEXT URL (403 direct) or a DDT/Cerema PDF copy; the arrêté uses "emplacements réservés" and "places de stationnement adaptées" is not expected.
- Result: no Légifrance page; prefecture PDFs (Essonne, Seine-et-Marne, Hautes-Pyrénées, Vosges), a 2023 DMA voirie leaflet, a Cerema fiche, municipal PAVE guides. Summary not used.

### FETCH https://www.ecologique-solidaire.gouv.fr/sites/default/files/2023%20DMA%20d%C3%A9pliant%20voirie%20.pdf
- Prior (written before the call): kerb ramp forms 'abaissé de trottoir' or 'bateau', 'bande d'éveil de vigilance', 'places de stationnement réservées', maybe 'PMR'
- Result: status 404, 146 bytes, sha256 55f7d9e99b8e2d4e0e193b2f0275501e6d9c1ebd29cadbea6a0da48a8587e3e0, artefact 55f7d9e99b8e2d4e.html, text 55f7d9e99b8e.txt (35 chars)

### FETCH https://www.cerema.fr/sites/default/files/inline-files/2._fiche_se_deplacer_vf_individuelle-1_0.pdf
- Prior (written before the call): 'cheminement', 'personnes à mobilité réduite', 'PMR', parking and transport terms
- Result: status 200, 1206232 bytes, sha256 53cd114d21b4d0a4d5e6facbb384643ec2ce5872c4f20deee09d451b9b33beeb, artefact 53cd114d21b4d0a4.pdf, text 53cd114d21b4.txt (5454 chars)
- Note: DMA leaflet URL 404 (empty). Cerema fiche "Se déplacer" (undated) read in full: "personnes en situation de handicap" and "personnes à mobilité réduite" for the same 2005 law; "chaîne de déplacement", "PAVE".

### QUERY "legifrance JORFTEXT arrêté 15 janvier 2007 prescriptions techniques accessibilité voirie"
- Prior: a Légifrance URL with a JORFTEXT id I can route through Wayback.
- Result: an Aveugles de France fiche (DPO, tier 5), a 2013 copy of the 2007 arrêté on a party commission site (not used: secondary host of an outdated version), commentary sites (not used). Search summary cites JORFTEXT000000246253; unverified until fetched.

### FETCH http://archive.org/wayback/available?url=www.legifrance.gouv.fr/loda/id/JORFTEXT000000246253
- Prior: a snapshot exists; the text is either the arrêté of 15 January 2007 or décret 2006-1658.
- Result: snapshot 20241206173354 available (status 200).

### FETCH https://web.archive.org/web/20241206173354if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000246253/
- Prior (written before the call): arrêté 15 janvier 2007 consolidated; 'emplacements réservés', 'places', 'abaissé de trottoir' or 'ressaut', 'bande d'éveil de vigilance'
- Result: status None, 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, artefact e3b0c44298fc1c14.txt, text e3b0c44298fc.txt (0 chars)

### FETCH https://aveuglesdefrance.org/app/uploads/2022/03/Fiche-sur-les-Prescriptions-techniques-PDF-Accessible.pdf
- Prior (written before the call): 'bande d'éveil de vigilance (BEV)', 'bandes de guidage', 'personnes aveugles et malvoyantes'
- Result: status 200, 303041 bytes, sha256 eba98e28c35da81fede447e977d2c33d11d5ea19be1da68b42ca2477d14d33fa, artefact eba98e28c35da81f.pdf, text eba98e28c35d.txt (2835 chars)
- Note: 0 bytes, no HTTP status (connection-level failure). Retry once with the if_ form, then the plain form (CLAUDE.md section 7).

### FETCH https://web.archive.org/web/20241206173354if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000246253/
- Prior (written before the call): same as above
- Result: status None, 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, artefact e3b0c44298fc1c14.txt, text e3b0c44298fc.txt (0 chars)
- Result: second Wayback attempt also 0 bytes; plain form not tried after two resets (budget). The voirie arrêté is NOT OBTAINED this pass. Aveugles de France fiche "Prescriptions techniques pour l'accessibilité de la voirie" (CFPSAA commission accessibilité, juin 2021) read in full: "voirie, des espaces publics accessibles à tous", "chaîne de déplacement"; no parking or lift form beyond "stationnement".

### QUERY "plateforme élévatrice monte-escalier ascenseur ERP accessibilité personnes handicapées guide ministère"
- Prior: ministry or Cerema guidance distinguishing "plate-forme élévatrice" (vertical) from "plate-forme monte-escalier" (inclined), and colloquial "élévateur PMR"; possibly the arrêté of 8 décembre 2014 (existing ERP) allows "plate-forme élévatrice inclinée".
- Result: commercial pages (hellopro, travaux.com, batiproduits), a Paris Region tourism PDF, and three OUT-OF-JURISDICTION sources excluded by jurisdiction: CMHC/SCHL (Canada), ITM (Luxembourg), Ville de Gatineau (Québec). No ministry guide. Product-name forms seen in titles: "élévateur PMR", "plateforme monte-escalier", "Elévateur monte-escaliers à plateforme pour personnes à mobilité réduite".
- Note: the lift product vocabulary lives in trade catalogues, not in public guidance; one catalogue page fetched as product-name attestation only.

### FETCH https://www.batiproduits.com/amp/fiche/produits/elevateur-monte-escaliers-a-plateforme-pour-pers-p278784752.html
- Prior (written before the call): product title 'Elévateur monte-escaliers à plateforme pour personnes à mobilité réduite'; 'PMR' in body
- Result: status 200, 174038 bytes, sha256 7dd8bd37f40be8309a57c2bd7df98bb283135c37639a716d7e9b9eb031e1edd3, artefact 7dd8bd37f40be830.html, text 7dd8bd37f40b.txt (8212 chars)

### FETCH https://www.hellopro.fr/plateforme-elevatrice-monte-escaliers-courbe-multi-etages-pour-acces-pmr-garaventa-lift-artira-2017092-19491344-produit.html
- Prior (written before the call): 'plateforme élévatrice monte-escaliers', 'accès PMR', brand 'Garaventa Lift'
- Result: status 200, 218451 bytes, sha256 dac3ab87d00e4593df85fd81ad1a23ecc28af93627b74cddaa2400ac7a822004, artefact dac3ab87d00e4593.html, text dac3ab87d00e.txt (16871 chars)

### FETCH http://archive.org/wayback/available?url=www.legifrance.gouv.fr/loda/id/JORFTEXT000029925726
- Prior: a snapshot exists of the existing-ERP arrêté (8 décembre 2014) consolidated; it will name lifts "élévateur" and possibly "plate-forme élévatrice inclinée".
- Result (product pages): batiproduits/ABC LIFT: "Elévateurs PMR", "Elévateur monte-escaliers à plateforme pour personnes à mobilité réduite"; hellopro/Garaventa: "Plateforme élévatrice monte-escaliers courbe multi-étages pour accès PMR", "plateforme monte‑escaliers inclinée" (U+2011 hyphen in the bytes), category list puts "Monte-escalier mobile", "Élévateur PMR", "Rampe pour PMR" side by side. Prior confirmed.
- Wayback availability for JORFTEXT000029925726: no snapshot (empty). Existing-ERP arrêté not obtained.

### QUERY "APF France handicap stationnement places réservées guide accessibilité"
- Prior: an APF France handicap page or PDF using "places de stationnement réservées", possibly criticising the term "PMR" or "handicapé" as a noun.
- Result: no APF page; INC (Institut national de la consommation, public body) pages, Banque des Territoires, handicap.fr (media; not used), Assemblée nationale written questions, the Essonne prefecture note. Prior wrong (no DPO hit).

### FETCH https://www.inc-conso.fr/content/personnes-handicapees-ou-mobilite-reduite-le-stationnement-reserve
- Prior (written before the call): 'stationnement réservé', 'places réservées', 'carte mobilité inclusion', perhaps 'places handicapées'
- Result: status 200, 84758 bytes, sha256 e2bd0332dca6e189859c8d409bc6eb1f26e31bf63942585f3fca08ae38bb9018, artefact e2bd0332dca6e189.html, text e2bd0332dca6.txt (7766 chars)

### QUERY (allowed_domains apf-francehandicap.org) "places de stationnement réservées accessibilité"
- Prior: APF pages on parking and on accessibility using "personnes en situation de handicap"; maybe "places handicapées" as a colloquial form quoted critically.
- Result: 10 APF pages: a 2022 policy note on accessibility, an article on two Conseil d'État rulings, local delegation pages (Loire-Atlantique "Informations pratiques"). Summary claims unverified.

### FETCH https://actionspolitiques.apf-francehandicap.org/sites/default/files/documents/Note-Politique-Accessibilite%CC%81-2022.pdf
- Prior (written before the call): 'accessibilité universelle' or 'conception universelle', 'personnes en situation de handicap', 'places de stationnement réservées', 'ascenseurs'
- Result: status 200, 2575710 bytes, sha256 89caf376d32ac89b29787cf92c6eae4d04d84084251140c1bde9d218b8a4430d, artefact 89caf376d32ac89b.pdf, text 89caf376d32a.txt (49518 chars)

### FETCH https://loire-atlantique.apf-francehandicap.org/informations-pratiques
- Prior (written before the call): 'places réservées PMR' on the delegation's car park
- Result: status 200, 78299 bytes, sha256 be68d944b265353f487aed92165d481fc4441e14af4a9e53fbfc489d85a2b9a6, artefact be68d944b265353f.html, text be68d944b265.txt (5096 chars)

### FETCH https://www.apf-francehandicap.org/actualite/deux-arrets-du-conseil-etat-sur-le-stationnement-des-personnes-en-situation-de-handicap
- Prior (written before the call): 'stationnement des personnes en situation de handicap', 'places réservées', 'carte européenne de stationnement'
- Result: status 200, 117517 bytes, sha256 45ca7a8d30adeb252861db4f0d768de88f3970d2456fe1505ecbf36801266c1c, artefact 45ca7a8d30adeb25.html, text 45ca7a8d30ad.txt (6537 chars)
- Result: APF note "Pour un environnement, des biens, services et activités accessibles" (2022) read: "l'accessibilité et la conception universelles" (p.2), "conception universelle et de haute qualité d'usage® (HQU®)" (p.5), "places de stationnement réservées" (p.9), "accessibilité universelle" (p.11); also "personnes en situation de handicap" beside "personnes handicapées". APF Loire-Atlantique page: "places réservées PMR". APF Conseil d'État article: the fetched HTML holds site chrome only, no article body (empty for forms). INC page: "stationnement réservé aux personnes handicapées ou à mobilité réduite"; it links an APF blog copy of the ministry guide. Prior partly confirmed: APF does use "PMR" locally; no rejection of "PMR" found.

### QUERY "RATP accessibilité UFR ascenseurs stations personnes à mobilité réduite"
- Prior: RATP pages using "UFR" (utilisateurs de fauteuil roulant), "PMR", "ascenseur", maybe "élévateur"; jurisdiction Île-de-France operator.
- Result: RATP pages ("Le plan des stations … accessibles aux Personnes à Mobilité Réduite (PMR)"), an IDFM accessibility press kit (2024), media (not used).

### FETCH https://www.ratp.fr/services-aux-voyageurs/plan-des-stations-accessibles-pmr
- Prior (written before the call): 'Personnes à Mobilité Réduite (PMR)', 'UFR', 'ascenseur', 'stations accessibles'
- Result: status 403, 5580 bytes, sha256 9a12e86432c550bf0bb587a4f05573415f6df859431bd9f9e0fdc6ee3868839f, artefact 9a12e86432c550bf.html, text 9a12e86432c5.txt (59 chars)

### FETCH https://www.iledefrance-mobilites.fr/medias/portail-idfm/ZtnVsrzzk9ZrXDl2_DP_accessibilite_IDFM_050924.pdf
- Prior (written before the call): 'UFR', 'PMR', 'ascenseurs', 'personnes en situation de handicap'; possibly 'accessibilité universelle'
- Result: status 403, 4560 bytes, sha256 0befa9a383616fb1866dedfcd0f0e30420c321198c94365840a5cd497ef11d2f, artefact 0befa9a383616fb1.html, text 0befa9a38361.txt (774 chars)
- Note: both 403 (publisher block). Wayback availability checked next.
- Result: no Wayback snapshot for either (empty). RATP and IDFM NOT OBTAINED.

### QUERY (allowed_domains service-public.gouv.fr, service-public.fr) "carte mobilité inclusion stationnement places réservées"
- Prior: a vosdroits fiche using "places de stationnement réservées aux personnes handicapées" and "CMI stationnement".
- Result: service-public.gouv.fr fiches F34049 (CMI), F2891 (carte européenne de stationnement), F34212 (stationnement très gênant). Links given with ?lang=en; the French page (no parameter) is fetched.

### FETCH https://www.service-public.gouv.fr/particuliers/vosdroits/F34049
- Prior (written before the call): 'places réservées', 'CMI stationnement', 'carte européenne de stationnement'
- Result: status 200, 282383 bytes, sha256 554a5d94228d1f435c2267f45900259fd0d87a1109c0587ea0b0d3fa0c38cf2a, artefact 554a5d94228d1f43.html, text 554a5d94228d.txt (47140 chars)

### FETCH https://www.service-public.gouv.fr/particuliers/vosdroits/F34212
- Prior (written before the call): 'emplacements réservés aux véhicules portant une carte mobilité inclusion' or 'places handicapées'
- Result: status 200, 186128 bytes, sha256 abdacfed15787b5cae4747fb70d369eaa2ab03b79575578b323fa40cfcae9222, artefact abdacfed15787b5c.html, text abdacfed1578.txt (31475 chars)
- Note: F34049: "places de parking réservées aux personnes handicapées", "CMI Stationnement remplace l'ancienne carte de stationnement"; F34212: "emplacements réservés aux véhicules portant une carte mobilité inclusion stationnement ou l'ancienne carte de stationnement" and, in the summary list, "Sur une place pour personne handicapée". Prior confirmed; "parking" (anglicism) appears in State prose.

### FETCH https://www.loisin.fr/wp-content/uploads/2021/12/ARRETE-PLACE-HANDICAPE-ECOLE-2014-08.pdf
- Prior (written before the call): body 'place de stationnement réservée aux personnes handicapées' or GIG-GIC (2014); title 'place handicapé' only in file name
- Result: status 200, 252285 bytes, sha256 2a9d7da5a277538f80adf21581f4101a5532b3f5f27deec51a759b3745e47919, artefact 2a9d7da5a277538f.pdf, text 2a9d7da5a277.txt (2808 chars)
