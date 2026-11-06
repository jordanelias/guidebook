# Equivalents record — FR-FR (France), session_2026-11-06-base-vocabulary-review

**Verdict.** Partial, by design. 30 register-v2 concepts were attempted, plus one concept the register lacks: the parking permit. All three owner classes are covered from French sources of tiers 1, 3, 4 and 5. Every quote verifies in the saved text (`python3 -I $D/equiv_build.py` exits 0). Parking, which the first pass and SYNTHESIS 3(e) left as a [GAP] for FR, now has a class. No Belgian, Swiss or Québec source was used. Three were excluded on sight (CMHC, ITM Luxembourg, Gatineau). The RHFAC French edition was not used. Nothing was written to the database.

## Counts (re-run; from the repository root, `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FR-FR`)
- Rebuild and verify: `python3 -I $D/equiv_build.py`. Rows by usage type: `awk -F'\t' 'NR>1{print $6}' $D/equivalents.tsv | sort | uniq -c`. Rows by tier: `awk -F'\t' 'NR>1{print $8}' $D/equivalents.tsv | sort | uniq -c`. At writing the totals were 91 rows, 54 code term, 15 qualifier, 12 colloquial, 5 outdated, 5 product name. By tier: 48 tier 1, 3 tier 3, 27 tier 4, 8 tier 5, 5 product.
- Concepts attempted: `awk -F'\t' 'NR>1 && $1!=""{print $1}' $D/equivalents.tsv | sort -u`. These are R2-007 008 021 022 050 072 076 083 084 087 089 163 164 165 166 168 169 170 174 175 176 178 186 198 201 208 247 281 333 553, plus the permit rows, which have an empty id. Not attempted: every other row of `register-v2/concepts.tsv`, including the FR-origin performance-criterion, trigger and outcome rows.
- Conflation notes: `awk -F'\t' 'NR>1 && $12!=""' $D/equivalents.tsv | wc -l`.

## The owner classes in French (France)
- **Parking.** Code term: "place de stationnement adaptée", "places … adaptées et réservées aux personnes handicapées", "emplacements adaptés et réservés" (A17 art. 3). Signage manual: "emplacements … réservés aux véhicules utilisés par les personnes titulaires de la carte de stationnement" (IISR 4e partie p.16, panonceau M6h). State and municipal prose: "places réservées", "place pour personne handicapée", "places de parking réservées aux personnes handicapées", "emplacement réservé". DPO: "places de stationnement réservées", "places réservées PMR". Outdated: "macaron … (GIG-GIC)", "Interdit sauf GIG-GIC", "carte européenne de stationnement". The French bay is defined by its permit holder, not by the umbrella word.
- **Umbrella qualifier.** The code uses two words, "accessible" and "adapté", interchangeably. The legal population is "personnes handicapées". "PMR" (personnes à mobilité réduite) is State and trade usage and does not occur in either arrêté. "en situation de handicap" is the person-first form in Cerema, Lille and APF. Universal and inclusive forms come from the DPO: "accessibilité universelle", "conception universelle", "société inclusive", plus the label "haute qualité d’usage® (HQU®)". "accessibles à tous" and "pour tous" also occur.
- **Vertical transport.** "ascenseur" (with "cabine") is the lift. "élévateur" / "appareil élévateur vertical" is the platform lift, and "plate-forme élévatrice" is its platform. "équipement mobile" is the class of "tapis roulant", "escalier mécanique" and "plan incliné mécanique". Trade usage: "Plateforme élévatrice", "plateforme monte‑escaliers inclinée", "Elévateur monte-escaliers à plateforme", "Elévateurs PMR".

## Conflations recorded (not resolved)
1. Reserved vs designed. A17 joins "adaptées … et réservées" in one object. The 2012 ministry guide asks "place … réservée" (the mayor's legal act) and "place … aménagée" (the design) as two questions (pp. 6–7). The register has one row.
2. "adapté" = "accessible". A17 art. 12 uses both for one cabinet d'aisances, art. 16 has "cheminement adapté", and ecologie.gouv.fr writes "adaptées et réservées" and "réservés et accessibles" on one page.
3. PMR vs handicap. The ministry names the two groups side by side. Cerema states the disability law of 2005 in PMR terms.
4. "élévateur" in the trade covers vertical and stair-following devices. A17's "plate-forme élévatrice" is a part, not the device.
5. "cabine" is both the lift car (art. 7-2) and a changing cubicle (art. 18). "palier" is the ramp rest, the stair landing and the lift landing. "cabinet d'aisances" is a stall or a room. A "garde-corps" may stand in for the "main courante".

## Not obtained
Code de la route R417-11 and CGCT L2213-2: Légifrance 403, and no article id in hand. Arrêté du 15 janvier 2007: the Wayback snapshot exists but the connection reset twice. Arrêté du 8 décembre 2014: no snapshot. RATP and IDFM: 403, no snapshot. Also not obtained: the MDPH Isère stub, the Melun anti-scraper shell, and the DMA leaflet (404). "UFR" (wheelchair user) is therefore not attested. "place handicapé" occurs only in file names (Loisin, Val-d'Oise) and was not recorded, because the quote must come from the document's text.

## Self-attack
1. Sense mapping is my judgment, for example "palier d'ascenseur" to elevator lobbies and "cabinet d'aisances" to toilet stalls. Each such row carries a scope note.
2. Tier 4 includes a 2012 guide and a 2010–2011 Paris guide that may be superseded. The IISR copy (VC20190109) predates the 2024–2025 amendments, and its own avertissement says it has documentary value only.
3. Quotes verify against our extractions. The Mérignac text is an OCR layer, and the HTML was tag-stripped (one quote carries a space before its full stop). The raw-byte check `retrieval_log.locate_quote` was not run.
4. The breadth is thin: 30 of 560 concepts. Most rows are tier 1, so they repeat what the first pass found rather than adding colloquial forms.
5. The trade pages are outside tiers 1–5 and marked `product`. Recording them as attestation of product names, not of any code term, is a choice the owner may reject.
