#!/usr/bin/env python3
"""Regenerate equivalents.tsv for FR-FR and verify every quote.

Run from the repository root:  python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FR-FR/equiv_build.py
Exits 1 if any quote is not found verbatim (whitespace-collapsed) in its saved text, if the form is not inside
its quote, or if a quote exceeds 25 words. Locators are derived here: for the two arrêtés, the enclosing
article or annex plus the line of the saved text; for PDFs, the page on which pdftotext finds the quote;
for HTML pages, the line of the saved text.
"""
import csv, re, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, 'text')
RL = os.path.join(HERE, '..', '..', '..', '..', 'retrieval-log', 'session_2026-11-06-base-vocabulary-review')
REG = os.path.join(HERE, '..', '..', 'register-v2', 'concepts.tsv')

# key: (title as written, issuer, URL, jurisdiction, tier, text file, artefact or None, kind)
S = {
 'A17': ("Arrêté du 20 avril 2017 relatif à l'accessibilité aux personnes handicapées des établissements recevant du public lors de leur construction et des installations ouvertes au public lors de leur aménagement",
         "ministres chargés de l'environnement et du logement (NOR LHAL1704269A)",
         "https://web.archive.org/web/20241109234132if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034485459/",
         "FR (national)", "1", "43802a8ee631.txt", None, 'arrete'),
 'A15': ("Arrêté du 24 décembre 2015 relatif à l'accessibilité aux personnes handicapées des bâtiments d'habitation collectifs et des maisons individuelles lors de leur construction",
         "ministres chargés de l'écologie et du logement (NOR ETLL1511145A)",
         "https://web.archive.org/web/20250208093733if_/https://www.legifrance.gouv.fr/loda/id/JORFTEXT000031692481",
         "FR (national)", "1", "014af9f59daf.txt", None, 'arrete'),
 'IISR4': ("Instruction interministérielle sur la signalisation routière – 4ème partie – Signalisation de prescription (VC20190109; 'n'a qu'une valeur documentaire')",
         "DSR/BSC – DGITM/DIT/MARRN (State copy hosted by DDT du Doubs)",
         "https://www.msr25.doubs.developpement-durable.gouv.fr/IMG/pdf/iisr_4eme_partie_signalisation_de_prescription.pdf",
         "FR (national)", "3", "fbef33f84044.txt", "fbef33f84044bc3a.pdf", 'pdf'),
 'PARIS': ("Guide de la signalisation verticale à Paris (rédaction 12 avril 2010, validation 29/08/2011)",
         "Ville de Paris, Direction de la Voirie et des Déplacements",
         "https://cdn.paris.fr/paris/2019/07/24/b1df9af3fe20382ffef1858dffb0c4aa.pdf",
         "FR (Ville de Paris)", "3", "e0b800abda34.txt", "e0b800abda3469fc.pdf", 'pdf'),
 'MEDDE': ("Le stationnement réservé aux personnes handicapées ou à mobilité réduite. Guide juridique et pratique à l'usage des collectivités territoriales (parution octobre 2012)",
         "Ministère de l'Égalité des territoires et du Logement; Ministère de l'Écologie, du Développement durable et de l'Énergie (copy hosted by Préfecture du Val-d'Oise)",
         "https://www.val-doise.gouv.fr/index.php/contenu/telechargement/9146/69815/file/Stationnement_reserve_handicapes_MEDDE.pdf",
         "FR (national)", "4", "d7fc387e4d14.txt", "d7fc387e4d14ea76.pdf", 'pdf'),
 'ECOL': ("L'accessibilité du stationnement",
         "Ministères Transition écologique, Aménagement du Territoire, Transports, Ville et Logement",
         "https://www.ecologie.gouv.fr/politiques-publiques/laccessibilite-du-stationnement",
         "FR (national)", "4", "50baec70a17f.txt", None, 'html'),
 'SP1': ("Carte mobilité inclusion (CMI) (fiche F34049)", "service-public.gouv.fr (Direction de l'information légale et administrative)",
         "https://www.service-public.gouv.fr/particuliers/vosdroits/F34049", "FR (national)", "4", "554a5d94228d.txt", None, 'html'),
 'SP2': ("Stationnement interdit, gênant, très gênant ou dangereux (fiche F34212)", "service-public.gouv.fr (Direction de l'information légale et administrative)",
         "https://www.service-public.gouv.fr/particuliers/vosdroits/F34212", "FR (national)", "4", "abdacfed1578.txt", None, 'html'),
 'INC': ("Personnes handicapées ou à mobilité réduite : le stationnement réservé", "Institut national de la consommation",
         "https://www.inc-conso.fr/content/personnes-handicapees-ou-mobilite-reduite-le-stationnement-reserve", "FR (national)", "4", "e2bd0332dca6.txt", None, 'html'),
 'LILLE': ("La mobilité pour tous – Les aménagements – Stationnement pour personnes en situation de handicap (leaflet)", "Métropole Européenne de Lille",
         "https://www.lillemetropole.fr/sites/default/files/2020-12/Pmr%206p%20triptyque%20210x100mm%2007.pdf", "FR (Métropole Européenne de Lille)", "4", "aab7e4c3621d.txt", "aab7e4c3621d2f44.pdf", 'pdf'),
 'MERIG': ("Arrêté municipal portant réglementation du stationnement, rue Gérard Blot (MER-2025-00106-P; OCR text layer)", "Ville de Mérignac (Gironde)",
         "https://www.merignac.com/sites/default/files/2025-11/39-bis-gerard-blot-place-pmr.pdf", "FR (commune de Mérignac)", "4", "e3251a287b96.txt", "e3251a287b96cc43.pdf", 'pdf'),
 'LOISIN': ("Arrêté municipal n° 2014-08 désignant un emplacement réservé aux personnes handicapées ou à mobilité réduite", "Commune de Loisin (Haute-Savoie)",
         "https://www.loisin.fr/wp-content/uploads/2021/12/ARRETE-PLACE-HANDICAPE-ECOLE-2014-08.pdf", "FR (commune de Loisin)", "4", "2a9d7da5a277.txt", "2a9d7da5a277538f.pdf", 'pdf'),
 'CEREMA': ("Se déplacer (fiche)", "Cerema",
         "https://www.cerema.fr/sites/default/files/inline-files/2._fiche_se_deplacer_vf_individuelle-1_0.pdf", "FR (national)", "4", "53cd114d21b4.txt", "53cd114d21b4d0a4.pdf", 'pdf'),
 'APFN': ("Pour un environnement, des biens, services et activités accessibles (note politique accessibilité 2022)", "APF France handicap",
         "https://actionspolitiques.apf-francehandicap.org/sites/default/files/documents/Note-Politique-Accessibilite%CC%81-2022.pdf", "FR (national DPO)", "5", "89caf376d32a.txt", "89caf376d32ac89b.pdf", 'pdf'),
 'APF44': ("Informations pratiques", "APF France handicap, délégation de Loire-Atlantique",
         "https://loire-atlantique.apf-francehandicap.org/informations-pratiques", "FR (Loire-Atlantique DPO delegation)", "5", "be68d944b265.txt", None, 'html'),
 'ADF': ("Prescriptions techniques pour l'accessibilité de la voirie (création juin 2021)", "Aveugles de France / CFPSAA commission accessibilité",
         "https://aveuglesdefrance.org/app/uploads/2022/03/Fiche-sur-les-Prescriptions-techniques-PDF-Accessible.pdf", "FR (national DPO)", "5", "eba98e28c35d.txt", "eba98e28c35da81f.pdf", 'pdf'),
 'BATI': ("Elévateur monte-escaliers à plateforme pour personnes à mobilité réduite | BCSP - ABC LIFT (catalogue page)", "Batiproduits (trade catalogue); maker ABC LIFT",
         "https://www.batiproduits.com/amp/fiche/produits/elevateur-monte-escaliers-a-plateforme-pour-pers-p278784752.html", "FR (trade catalogue)", "product", "7dd8bd37f40b.txt", None, 'html'),
 'HELLO': ("Plateforme élévatrice monte-escaliers courbe multi-étages pour accès PMR - Garaventa Lift Artira (catalogue page)", "Hellopro (trade catalogue)",
         "https://www.hellopro.fr/plateforme-elevatrice-monte-escaliers-courbe-multi-etages-pour-acces-pmr-garaventa-lift-artira-2017092-19491344-produit.html", "FR (trade catalogue)", "product", "dac3ab87d00e.txt", None, 'html'),
}

PERMIT = ('', 'parking permit (no register-v2 row; label ours)')

# (concept_id, form, usage_type, scope_note, source, quote, conflation_note)
R = [
 # ---- parking: the bay (R2-050) ----
 ('R2-050', "place de stationnement adaptée", 'code term', "the bay as designed; A17 couples it with reservation", 'A17',
  "Une place de stationnement adaptée est aisément repérable par tous à partir de l'entrée du parc de stationnement",
  "A17 art. 3 I joins two properties in one object, 'adaptées pour les personnes handicapées et réservées à leur usage'; MEDDE 2012 p.6-7 treats 'réservée' (legal act of the mayor) and 'aménagée' (design) as separate questions"),
 ('R2-050', "places de stationnement adaptées et réservées aux personnes handicapées", 'code term', "design plus reservation", 'A17',
  "les places de stationnement adaptées et réservées aux personnes handicapées peuvent être concentrées sur les deux niveaux les plus proches de la surface", ''),
 ('R2-050', "emplacements adaptés et réservés", 'code term', "synonym the same article uses for the bays", 'A17',
  "les emplacements adaptés et réservés sont signalés", ''),
 ('R2-050', "espace de stationnement adapté", 'code term', "used where no accessible route from outside the plot can be built", 'A17',
  "un espace de stationnement adapté tel que défini à l'article 3 est prévu à proximité de l'entrée du bâtiment", ''),
 ('R2-050', "places adaptées", 'code term', "short form; housing text", 'A15',
  "doit comporter une ou plusieurs places adaptées répondant aux conditions du II ci-après", ''),
 ('R2-050', "place de stationnement réservée", 'code term', "the LEGAL reservation by municipal order (CGCT L2213-2), not the design", 'MEDDE',
  "Que signifie « place de stationnement réservée » ?",
  "the guide states that designing a bay for disabled people 'n’est pas suffisant' for it to be reserved: reserved and designed are two concepts the register's one row holds as one"),
 ('R2-050', "place de stationnement aménagée", 'code term', "the DESIGN property (width, slope, surface) of a reserved bay", 'MEDDE',
  "Que signifie « place de stationnement aménagée » ?", "see the row above"),
 ('R2-050', "emplacements de stationnement aménagés", 'code term', "statute wording (CGCT L2213-2) as quoted by the ministry guide; the statute itself not retrieved", 'MEDDE',
  "des emplacements de stationnement aménagés aux véhicules utilisés par les personnes titulaires de la carte de stationnement", ''),
 ('R2-050', "emplacements situés sur chaussée et hors chaussée réservés aux véhicules utilisés par les personnes titulaires de la carte de stationnement", 'code term',
  "signage-manual term; keyed to the permit, not to a user group or the umbrella word", 'IISR4',
  "sur les emplacements situés sur chaussée et hors chaussée réservés aux véhicules utilisés par les personnes titulaires de la carte de stationnement", ''),
 ('R2-050', "emplacements réservés aux titulaires de la carte de stationnement", 'code term', "municipal signage guide's term", 'PARIS',
  "pour emplacements réservés aux titulaires de la carte de stationnement (ex GIG-GIC).", ''),
 ('R2-050', "places réservées", 'colloquial', "short form in State prose", 'ECOL',
  "Stationnement gratuit en voirie sur toutes les places pas uniquement les places réservées", ''),
 ('R2-050', "places adaptées et réservées", 'code term', "ministry restates the A17 pairing", 'ECOL',
  "Les communes doivent créer un minimum de 2% de places adaptées et réservées", ''),
 ('R2-050', "places réservés et accessibles", 'colloquial', "verbatim with the page's agreement error ('réservés'); 'accessibles' replaces 'adaptées'", 'ECOL',
  "d'utiliser les places réservés et accessibles", "the same page uses 'adaptées et réservées' and 'réservés et accessibles' for one object: adapté and accessible are treated as one qualifier here"),
 ('R2-050', "places de parking réservées aux personnes handicapées", 'colloquial', "anglicism 'parking' in State prose", 'SP1',
  "de vous garer sur les places de parking réservées aux personnes handicapées", ''),
 ('R2-050', "place pour personne handicapée", 'colloquial', "summary-list form", 'SP2',
  "Sur une place pour personne handicapée", ''),
 ('R2-050', "emplacements réservés aux véhicules portant une carte mobilité inclusion stationnement", 'code term', "keyed to the permit", 'SP2',
  "Sur les emplacements réservés aux véhicules portant une carte mobilité inclusion stationnement ou l'ancienne carte de stationnement", ''),
 ('R2-050', "places de stationnement réservées aux personnes en situation de handicap", 'colloquial', "person-first qualifier 'en situation de handicap'", 'LILLE',
  "L’aménagement de places de stationnement réservées aux personnes en situation de handicap contribue à faciliter la vie quotidienne", ''),
 ('R2-050', "emplacements réservés", 'colloquial', "short form", 'LILLE',
  "stratégie de répartition des emplacements réservés", ''),
 ('R2-050', "une place avec une « bande bleue »", 'colloquial', "NARROWER: the derogated bay where the norms could not be met", 'LILLE',
  "une dérogation (le plus souvent, une place avec une « bande bleue »)", ''),
 ('R2-050', "emplacement réservé", 'code term', "municipal order's term; the file name calls it 'place-pmr', which is not in the document's text", 'MERIG',
  "ont un emplacement réservé 39bis Rue Gerard Blot", ''),
 ('R2-050', "emplacement réservé aux personnes handicapées ou à mobilité réduite", 'code term', "municipal order title", 'LOISIN',
  "Désignant un emplacement réservé aux personnes handicapées ou à mobilité réduite", ''),
 ('R2-050', "emplacements de stationnement signalés pour personnes handicapées", 'code term', "municipal order", 'LOISIN',
  "les emplacements de stationnement signalés pour personnes handicapées sur le parking du groupe scolaire", ''),
 ('R2-050', "places de stationnement réservées", 'colloquial', "DPO usage", 'APFN',
  "ces places de stationnement réservées sont de plus en plus convoitées", ''),
 ('R2-050', "places réservées PMR", 'colloquial', "DPO local delegation uses the acronym as a qualifier", 'APF44',
  "Un parking est à votre disposition devant la délégation avec des places réservées PMR.", ''),
 ('R2-050', "stationnement réservé", 'colloquial', "WIDER: names the regime, not the bay", 'INC',
  "Personnes handicapées ou à mobilité réduite : le stationnement réservé", ''),
 # ---- the car park (R2-281) ----
 ('R2-281', "parc de stationnement", 'code term', "the car park as a whole", 'A17',
  "Le présent article s'applique à tout parc de stationnement automobile intérieur ou extérieur à l'usage du public", ''),
 ('R2-281', "parcs de stationnement en ouvrage, enterrés ou aériens", 'code term', "NARROWER: structured car parks", 'A17',
  "ainsi qu'aux parcs de stationnement en ouvrage, enterrés ou aériens", ''),
 ('R2-281', "parking", 'colloquial', "anglicism", 'APF44',
  "Un parking est à votre disposition devant la délégation avec des places réservées PMR.", ''),
 # ---- the permit (no register row) ----
 (PERMIT, "carte \" mobilité inclusion \" portant la mention \" stationnement pour personnes handicapées \"", 'code term', "the current permit; the French bay is defined by its holder", 'A17',
  "titulaires de la carte \" mobilité inclusion \" portant la mention \" stationnement pour personnes handicapées \"", ''),
 (PERMIT, "CMI Stationnement (CMI S)", 'colloquial', "administrative abbreviation", 'ECOL',
  "La carte française CMI Stationnement (CMI S) et les droits associés", ''),
 (PERMIT, "carte européenne de stationnement", 'outdated or disfavoured', "superseded for French residents by the CMI; valid to 31 Dec 2026 per SP1", 'ECOL',
  "La carte de stationnement ou carte Européenne de stationnement reste valable en France.", ''),
 (PERMIT, "ancienne carte de stationnement", 'outdated or disfavoured', "the State's own name for the superseded card", 'SP1',
  "La CMI Stationnement remplace l'ancienne carte de stationnement .", ''),
 (PERMIT, "macaron « grand invalide de guerre-grand invalide civil » (GIG-GIC)", 'outdated or disfavoured', "replaced by the European card by 31 Dec 2010 (guide p.5); still met in 'places GIG-GIC'", 'MEDDE',
  "titulaires de l’ancien macaron « grand invalide de guerre-grand invalide civil » (GIG-GIC)", ''),
 (PERMIT, "carte de stationnement de modèle communautaire pour personnes handicapées", 'outdated or disfavoured', "2014 municipal order", 'LOISIN',
  "carte de stationnement de modèle communautaire pour personnes handicapées", ''),
 # ---- signage for the bay ----
 ('R2-201', "panonceau M6h", 'code term', "NARROWER: the sign plate under B6d that reserves the bay", 'IISR4',
  "réservés aux véhicules utilisés par les personnes titulaires de la carte de stationnement définie par le code de l’action sociale et des familles (panonceau M6h)", ''),
 ('R2-201', "« Interdit sauf GIG-GIC »", 'outdated or disfavoured', "former wording of the M6h plate; to be replaced before 31 Dec 2014", 'MEDDE',
  "Le panonceau M6h « Interdit sauf GIG-GIC » doit être remplacé", ''),
 ('R2-208', "figurine normalisée « Fauteuil roulant »", 'code term', "the wheelchair figure in ground marking (IISR art. 118-2-C per the guide)", 'MEDDE',
  "de la figurine normalisée « Fauteuil roulant » sur les limites ou le long de la place de stationnement", ''),
 # ---- the umbrella qualifier (R2-333) ----
 ('R2-333', "accessible", 'qualifier', "the code's state word (cheminement accessible, sortie accessible)", 'A17',
  "Le cheminement accessible est le cheminement usuel, ou l'un des cheminements usuels.", ''),
 ('R2-333', "adapté", 'qualifier', "the code's word for provisions made for disabled people (places, cabinets d'aisances, chambres, cabines)", 'A17',
  "comporte au moins un cabinet d'aisances adapté pour les personnes handicapées circulant en fauteuil roulant",
  "A17 art. 12 calls the same compartment 'cabinet d'aisances adapté' and 'cabinet d'aisances accessible' within six lines (text lines 563-573)"),
 ('R2-333', "accessible", 'qualifier', "same object as the row above", 'A17',
  "un cabinet d'aisances accessible séparé pour chaque sexe est aménagé par étage", "see the row above"),
 ('R2-333', "cheminement adapté", 'qualifier', "'adapté' applied to the route the code elsewhere calls 'accessible'", 'A17',
  "des emplacements accessibles par un cheminement adapté sont aménagés", "A17 art. 16 uses 'cheminement adapté' where articles 2 and 6 define 'cheminement accessible'"),
 ('R2-333', "personnes handicapées", 'qualifier', "the legal population of every FR accessibility title", 'A17',
  "Tous les ascenseurs peuvent être utilisés par les personnes handicapées.", ''),
 ('R2-333', "personne à mobilité réduite", 'qualifier', "used by A17 for door and landing provisions; WIDER than disability in ministry usage", 'A17',
  "il permet à toute personne à mobilité réduite d'atteindre la porte", ''),
 ('R2-333', "personnes à mobilité réduite (PMR)", 'qualifier', "the PMR expansion; WIDER than 'personnes handicapées'", 'ECOL',
  "des personnes handicapées et des personnes à mobilité réduite (PMR)",
  "the ministry names two groups side by side, while Cerema (fiche p.2) states the 2005 disability law requires the travel chain accessible 'aux personnes à mobilité réduite': PMR used for the disability population"),
 ('R2-333', "personnes à mobilité réduite", 'qualifier', "Cerema reading of the 2005 law", 'CEREMA',
  "La loi de 2005 impose que toute la chaîne de déplacement soit accessible aux personnes à mobilité réduite.", "see the row above"),
 ('R2-333', "PMR", 'qualifier', "acronym used adjectivally ('accès PMR')", 'HELLO',
  "Plateforme élévatrice monte-escaliers courbe multi-étages pour accès PMR", ''),
 ('R2-333', "en situation de handicap", 'qualifier', "person-first form in public-body and DPO prose", 'CEREMA',
  "Les personnes en situation de handicap, comme tous les citoyens, doivent pouvoir se rendre d’un endroit à un autre", ''),
 ('R2-333', "accessibles à tous", 'qualifier', "universal sense ('to all')", 'ADF',
  "d’avoir une voirie, des espaces publics accessibles à tous", ''),
 ('R2-333', "pour tous", 'qualifier', "universal slogan", 'LILLE',
  "LA MOBILITÉ POUR TOUS", ''),
 ('R2-333', "l’accessibilité et la conception universelles", 'qualifier', "DPO pairs the umbrella state with universal design", 'APFN',
  "l’accessibilité et la conception universelles sont des conditions sine qua non de l’effectivité des droits", ''),
 ('R2-333', "accessibilité universelle", 'qualifier', "DPO usage, describing a transport charter", 'APFN',
  "de confort d’usage, d’accessibilité universelle, d’adaptation de la communication", ''),
 ('R2-333', "société inclusive", 'qualifier', "WIDER: society-level, not an object qualifier", 'APFN',
  "d’une société inclusive et durable", ''),
 ('R2-333', "haute qualité d’usage® (HQU®)", 'product name', "a registered label beside universal design", 'APFN',
  "développer l’approche de conception universelle et de haute qualité d’usage® (HQU®)", ''),
 # ---- vertical transport ----
 ('R2-163', "ascenseur", 'code term', "the lift car in a shaft; NF EN 81-70 deemed to satisfy", 'A17',
  "Tous les ascenseurs peuvent être utilisés par les personnes handicapées.", ''),
 ('R2-163', "ascenseur", 'code term', "housing text; types 2 or 3 of NF EN 81-70", 'A15',
  "Les ascenseurs sont de type 2 ou 3.", ''),
 ('R2-165', "cabine", 'code term', "the lift car", 'A17',
  "commandes extérieures et intérieures à la cabine",
  "the same text uses 'cabine' for changing and care cubicles (art. 18, 'cabines d'habillage ou de déshabillage, de soins ou de douche')"),
 ('R2-164', "équipement mobile", 'code term', "NARROWER than 'Elevating devices': A17's class for moving walks, escalators and inclined moving walks, listed apart from ascenseur and élévateur", 'A17',
  "Lorsque l'ascenseur, l'élévateur, l'escalier ou l'équipement mobile n'est pas visible", ''),
 ('R2-168', "élévateur", 'code term', "short form beside 'ascenseur'; in A17 the platform device", 'A17',
  "Lorsque l'ascenseur, l'élévateur, l'escalier ou l'équipement mobile n'est pas visible",
  "trade catalogues use 'élévateur' for vertical and stair-following devices alike (BATI, HELLO rows)"),
 ('R2-170', "appareil élévateur vertical", 'code term', "a platform travelling vertically; sub-typed by nacelle, gaine, porte", 'A17',
  "a) Un appareil élévateur vertical peut être installé dans les cas suivants :", ''),
 ('R2-170', "appareil élévateur vertical avec gaine fermée et avec porte", 'code term', "NARROWER: the enclosed type allowed to 3,20 m", 'A17',
  "un appareil élévateur vertical avec gaine fermée et avec porte peut être installé", ''),
 ('R2-168', "plate-forme élévatrice", 'code term', "the carrying platform of an 'appareil élévateur vertical', not the device's name", 'A17',
  "la plate-forme élévatrice a une dimension utile", "A17 names the device 'appareil élévateur' and its part 'plate-forme élévatrice'; the trade uses 'plateforme élévatrice' as the device name (HELLO)"),
 ('R2-168', "Plateforme élévatrice", 'product name', "device name in the trade", 'HELLO',
  "Plateforme élévatrice monte-escaliers courbe multi-étages pour accès PMR - Garaventa Lift Artira", ''),
 ('R2-169', "plateforme monte‑escaliers inclinée", 'product name', "printed with U+2011 non-breaking hyphen", 'HELLO',
  "est une plateforme monte‑escaliers inclinée conçue pour faciliter le déplacement des personnes en fauteuil roulant", ''),
 ('R2-169', "Elévateur monte-escaliers à plateforme", 'product name', "stair platform lift", 'BATI',
  "Elévateur monte-escaliers à plateforme pour personnes à mobilité réduite | BCSP", ''),
 ('R2-168', "Elévateurs PMR", 'product name', "WIDER: the catalogue category holds stair platforms and vertical platforms", 'BATI',
  "Elévateurs PMR à entraînement électrique", "one category name covers R2-168, R2-169 and R2-170 devices"),
 ('R2-174', "escalier mécanique", 'code term', "", 'A17',
  "Un escalier mécanique ou un plan incliné mécanique ne peut en aucun cas remplacer un ascenseur obligatoire.", ''),
 ('R2-175', "tapis roulant", 'code term', "horizontal moving walk", 'A17',
  "Dispositions relatives aux tapis roulants, escaliers et plans inclinés mécaniques.", ''),
 ('R2-175', "plan incliné mécanique", 'code term', "NARROWER: inclined moving walk", 'A17',
  "Un tapis roulant, un escalier mécanique ou un plan incliné mécanique est",
  "'plan incliné' alone is the fixed ramp (R2-533); the qualifier 'mécanique' moves it to moving equipment"),
 # ---- other concepts, second reading of A17/A15 ----
 ('R2-083', "plan incliné", 'code term', "the fixed ramp", 'A17',
  "un plan incliné de pente inférieure ou égale à 5 % est aménagé", ''),
 ('R2-083', "rampe amovible", 'code term', "NARROWER: a removable device, not built fabric", 'A15',
  "pour permettre l'installation ultérieure d'une rampe amovible ou d'un appareil élévateur vertical", "owner's ramp conflation (slope vs device): French carves the two with two words"),
 ('R2-089', "main courante", 'code term', "", 'A17',
  "L'escalier, quelle que soit sa conception, comporte une main courante de chaque côté.", ''),
 ('R2-089', "main courante", 'code term', "a guardrail may stand in for it", 'A17',
  "lorsqu'un garde-corps tient lieu de main courante", "the text lets a 'garde-corps' (guardrail) serve as the handrail: two register elements as one object"),
 ('R2-198', "boucle à induction magnétique", 'code term', "", 'A17',
  "au moins une de ces salles est équipée d'une boucle à induction magnétique", ''),
 ('R2-198', "boucle magnétique", 'code term', "short form, housing text", 'A15',
  "Les combinés sont équipés d'une boucle magnétique", ''),
 ('R2-198', "système de transmission du signal acoustique par induction magnétique", 'code term', "long form", 'A17',
  "il est équipé d'un système de transmission du signal acoustique par induction magnétique", ''),
 ('R2-186', "barre d'appui", 'code term', "", 'A17',
  "une barre d'appui latérale est prévue à côté de la cuvette", ''),
 ('R2-084', "palier de repos", 'code term', "rest landing of a ramp", 'A17',
  "Un palier de repos est nécessaire en haut et en bas de chaque plan incliné", "'palier' also names the stair landing ('palier intermédiaire', art. 7-1) and the lift landing ('palier d'ascenseur', A15 art. 6)"),
 ('R2-084', "palier intermédiaire", 'code term', "stair landing", 'A17',
  "En haut de l'escalier et sur chaque palier intermédiaire", ''),
 ('R2-166', "palier d'ascenseur", 'code term', "the lift landing", 'A15',
  "est installé sur chaque palier d'ascenseur", ''),
 ('R2-087', "nez de marche", 'code term', "singular form", 'A17',
  "mesurée depuis le nez de marche", ''),
 ('R2-553', "giron", 'code term', "the going as a unit of distance", 'A17',
  "Cette distance peut être réduite à un giron", ''),
 ('R2-553', "largeur du giron", 'code term', "the going is a 'largeur' in French", 'A17',
  "la largeur du giron est supérieure ou égale à 28 cm", ''),
 ('R2-008', "dévers", 'code term', "", 'A17',
  "Lorsqu'un dévers est nécessaire, il est inférieur ou égal à 2 %.", ''),
 ('R2-007', "Profil en long", 'code term', "the heading under which running slope is set", 'A17',
  "a) Profil en long :", ''),
 ('R2-072', "cheminement accessible", 'code term', "", 'A17',
  "Un cheminement accessible permet d'accéder à l'entrée principale", ''),
 ('R2-076', "circulations intérieures horizontales", 'code term', "WIDER than corridor: every interior horizontal route", 'A17',
  "Les circulations intérieures horizontales sont accessibles et sans danger pour les personnes handicapées.", ''),
 ('R2-021', "espace de manœuvre de porte", 'code term', "door manoeuvring space", 'A15',
  "Un espace de manœuvre de porte est nécessaire de part et d'autre de", ''),
 ('R2-022', "espace de manœuvre avec possibilité de demi-tour", 'code term', "turning space", 'A15',
  "Un espace de manœuvre avec possibilité de demi-tour est nécessaire", ''),
 ('R2-178', "cabinet d'aisances adapté", 'code term', "the WC compartment for wheelchair users; a room or a cubicle", 'A17',
  "Un cabinet d'aisances adapté pour les personnes handicapées présente les caractéristiques suivantes :",
  "'cabinet d'aisances' covers both the toilet stall (R2-178) and the toilet room (R2-552); A17 does not separate them"),
 ('R2-176', "sanitaires adaptés", 'code term', "", 'A17',
  "aux prestations offertes par l'établissement et aux sanitaires adaptés", ''),
 ('R2-247', "fauteuil roulant", 'code term', "", 'A17',
  "pour une personne circulant en fauteuil roulant", ''),
]

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def load(fn):
    return open(os.path.join(TXT, fn), encoding='utf-8', errors='replace').read()

HDR = re.compile(r'^\s*(?:Replier )?(Article \d[\d-]*|Annexe \d+)\b')

def arrete_loc(fn, quote):
    lines = load(fn).splitlines()
    first = 222
    q = norm(quote)
    for i, l in enumerate(lines):
        if i > first and q in norm(l):
            art = ''
            for j in range(i, first, -1):
                m = HDR.match(lines[j])
                if m:
                    art = m.group(1).replace('Article ', 'art. ').replace('Annexe ', 'annexe ')
                    break
            return f"{art}; text line {i+1} of {fn}"
    return None

_pages = {}
def pdf_loc(art, quote):
    p = os.path.join(RL, art)
    if p not in _pages:
        info = subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout
        n = int(re.search(r'Pages:\s+(\d+)', info).group(1))
        _pages[p] = [norm(subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), p, '-'], capture_output=True, text=True).stdout) for i in range(1, n+1)]
    q = norm(quote)
    hits = [str(i+1) for i, t in enumerate(_pages[p]) if q in t]
    return ('p. ' + ','.join(hits)) if hits else None

def html_loc(fn, quote):
    q = norm(quote)
    for i, l in enumerate(load(fn).splitlines()):
        if q in norm(l):
            return f"text line {i+1} of {fn}"
    return f"text of {fn} (spans lines)"

def main():
    labels = {}
    for r in csv.reader(open(REG, encoding='utf-8'), delimiter='\t'):
        labels[r[0]] = r[2] or r[5]
    out, fails = [], 0
    for cid, form, ut, scope, src, quote, conf in R:
        title, issuer, url, jur, tier, fn, art, kind = S[src]
        if isinstance(cid, tuple):
            cid, label = cid
        else:
            label = labels.get(cid)
            if label is None:
                print('UNKNOWN CONCEPT', cid); fails += 1; label = ''
        text = norm(load(fn))
        ok = norm(quote) in text
        fin = norm(form).lower() in norm(quote).lower()
        words = len(quote.split())
        if not ok or not fin or words > 25:
            fails += 1
            print('FAIL', cid, form, src, 'quote_in_text' if not ok else '', 'form_not_in_quote' if not fin else '', f'{words} words' if words > 25 else '')
            continue
        if kind == 'arrete':
            loc = arrete_loc(fn, quote) or f"text of {fn} (spans lines)"
        elif kind == 'pdf':
            loc = pdf_loc(art, quote) or 'page not resolved (quote spans pages or columns)'
        else:
            loc = html_loc(fn, quote)
        out.append([cid, label, form, 'fr', jur, ut, scope, tier, f"{title} | {issuer} | {url}", loc, quote, conf])
    with open(os.path.join(HERE, 'equivalents.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note',
                    'attestation_tier', 'source', 'locator', 'quote', 'conflation_note'])
        w.writerows(out)
    print(f'rows written: {len(out)}; failures: {fails}')
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
