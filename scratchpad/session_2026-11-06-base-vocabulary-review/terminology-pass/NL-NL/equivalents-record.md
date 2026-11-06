# Equivalents record: NL/NL (second pass)

**Verdict.** I recorded 76 form rows (67 distinct forms) for 20 register-v2 concepts. Every quote verifies verbatim in bytes retrieved through `retrieval_log.fetch`, and the build exits 0. All three owner classes are covered in Dutch. The Dutch building code (Bbl) has no disabled-parking rule, so the parking class comes from road-traffic law and municipal decisions. "lift" in the Bbl is defined by pointer to EU law, and that law excludes most platform lifts. No unattested seed was added. Nothing was committed, and the database was not touched.

**Counts.** Re-run these; do not trust the figures. From this folder: `python3 -I build_equiv.py`, then:
- Rows: `tail -n +2 equivalents.tsv | wc -l` gives 76. Distinct forms: `cut -f3 equivalents.tsv | tail -n +2 | sort -u | wc -l` gives 67. Concepts: `cut -f1 equivalents.tsv | tail -n +2 | sort -u | wc -l` gives 20.
- By usage type: `tail -n +2 equivalents.tsv | cut -f6 | sort | uniq -c` gives 30 code term, 21 colloquial, 18 qualifier, 6 outdated or disfavoured, 1 product name, 0 seeds.
- By tier and jurisdiction: `tail -n +2 equivalents.tsv | awk -F'\t' '{print $8"\t"$5}' | sort | uniq -c` gives T1 15 NL; T2 10 NL and 3 EU; T3 3 NL; T4 28 NL and 2 BE (contrast only); T5 15 NL (Ieder(in)).
- Conflation notes: `awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l` gives 16.

**Concepts attempted (20):** R2-050, R2-281, R2-333, R2-163, R2-164, R2-166, R2-168, R2-169, R2-171, R2-172, R2-173, R2-083, R2-161, R2-551, R2-179, R2-186, R2-094, R2-095, R2-247, R2-072. **Not attempted:** the other 540 rows, including every quantity row that the first pass marked FOUND (widths, riser and going, headroom). For those, the second reading of the Bbl found no variant forms beyond what the first pass already recorded. That claim was not tested row by row.

**The three owner classes in Dutch**
- **Parking.** The code term is gehandicaptenparkeerplaats (RVV 1990 art. 26; sign E6). There are two municipal subtypes: algemene gehandicaptenparkeerplaats (open to every card holder) and gehandicaptenparkeerplaats op kenteken (reserved for one vehicle). Superseded and disfavoured forms are "individuele gehandicaptenparkeerplaatsen" and "mindervaliden" (in Zuidplas's 2020 policy title). A colloquial form is "Rolstoeltoegankelijke parkeerplaatsen". The permit forms (gehandicaptenparkeerkaart) are kept with a scope note. The Bbl has parkeervakken only for EV charging points.
- **Qualifier.** The code's word is toegankelijk ("voor personen met een functiebeperking"), and "integraal toegankelijk" names a defined room standard. The equal-treatment law uses "algemene toegankelijkheid" and the CRPD text uses "universeel ontwerp". The ministry page has "inclusieve samenleving". Wheelchair-scoped forms are rolstoeltoegankelijk, rolstoelvriendelijk (the analogue of "wheelchair friendly") and rolstoelgeschikt. Housing classes are gelijkvloers, levensloopbestendig and aangepast. Disfavoured forms are mindervalide, invalide- (as in invalidentoilet) and the noun gehandicapte; the disfavoured verdict comes from BE advice only. Compounds with gehandicapten- remain the statute form.
- **Vertical transport.** The code's lift is "lift voor personen" (Bbl Bijlage I). That definition points to the Warenwetbesluit liften 2016, which points to directive 2014/33/EU art. 2. The directive covers inclined lifts over 15 degrees but excludes devices at or below 0,15 m/s. Colloquial forms are plateaulift (UvA), platformlift and "lift voor rolstoelen" (I amsterdam), and traplift (Minister of VWS; Ieder(in)). Further forms are badlift, "tillift aan het plafond", brandweerlift and "lift voor vluchten bij brand".

**Conflations (recorded, not resolved)**
- toegankelijk carries four senses: disability access, "openbaar toegankelijk gebied" (open to the public), access for emergency services, and permitted entry to a milieuzone. A fifth occurs in the EU lift text: "drager toegankelijk", a carrier a person can step into.
- "lift" names both the platform device (I amsterdam, Grachtenmuseum) and the EU-defined lift. Under the code's pointer, the platform device is not a lift.
- "attentievlak" (ProRail) is a false friend for the attention indicator. It is a flat decision square; the warning is the noppenvlak, which is part of the geleidelijn.
- "helling" means the gradient in the Bbl but the ramp itself for a Co-1 respondent.
- "drempel" is both a physical sill and a figurative barrier ("zonder drempels").
- Co-1 (Ieder(in) survey) states that "aangepaste woning" is stretchable, and that accessible homes are labelled "55+ woning".
- Bouwbesluit 2012 has a "gehandicapten" heading over a "personen met een functiebeperking" article.

**Flemish separation.** Every row carries its jurisdiction. Only the vlaanderen.be language advice is BE, and it is labelled CONTRAST. The TERM-090 point from the first pass stands: NL uses "hoogteverschil" (Bbl, 0,02 m rule), and no NL source read here uses "niveauverschil" in the level sense.

**Could not obtain.** NEN 9120 (geo-blocked and DRM), CROW publications (paid), the Oogvereniging's own guidance, the stair-lift infoblad, the Rijksoverheid parking-card page (404) and a Haarlemmermeer tender (404). The search log keeps each attempt.

**Self-attack**
1. Tier 4 is heavy (28 rows), and I amsterdam is a city marketing body whose wheelchair page is written by one person. Its forms show usage, not a norm.
2. The CRPD Dutch text may be a joint NL/BE translation; its jurisdiction "NL" rests on where it was published, not on who translated it.
3. Assigning the platform-lift forms (R2-168) and oprijplaten / rolstoelbanen (R2-083) to concepts is my sense judgment from short passages.
4. The judgment that the disfavoured forms are disfavoured rests on BE advice. No NL DPO language guide was obtained, so NL "outdated" labels are inferred.
5. Breadth: 20 of 560 concepts, and no tactile source for NL beyond rail stations. Public-realm forms (CROW) are absent.
