# Equivalents record: FI/FI, session_2026-11-06-base-vocabulary-review

**Verdict.** Finnish has a separate equivalence class for each of the three owner classes, and each class shows a different carve. 23 register concepts were attempted with forms found, plus R2-051 attempted with none found. 537 of the 560 concepts were not attempted. All 72 attested rows verify: `python3 -I $D/build_equivalents.py` exits 0, where `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FI-FI` and the command runs from the repository root. Each quote is checked in the saved extraction and each form inside its quote. Nothing was written to the database, and nothing was committed.

## Counts (re-run; do not trust the figures beside them)
- Rows by tier: `awk -F'\t' 'NR>1{print $8}' $D/equivalents.tsv | sort | uniq -c`. At writing: tier 1 = 38, tier 2 = 11, tier 3 = 1, tier 4 = 13, tier 5 = 9, seeds = 3.
- Rows by usage type: `awk -F'\t' 'NR>1{print $6}' $D/equivalents.tsv | sort | uniq -c`. At writing: code term 41, qualifier 12, colloquial 12, outdated or disfavoured 6, product name 1, seeds 3.
- Concepts: `awk -F'\t' 'NR>1{print $1}' $D/equivalents.tsv | sort -u | wc -l` gave 23. Owner-class rows: `awk -F'\t' 'NR>1{print $1}' $D/equivalents.tsv | grep -cE 'R2-(050|333|16[389]|170)'`.
- Conflation notes: `awk -F'\t' 'NR>1 && $12 ~ /CONFLATION/' $D/equivalents.tsv | wc -l` gave 10. Any note at all: `awk -F'\t' 'NR>1 && $12!=""' $D/equivalents.tsv | wc -l`.
- Concepts attempted. Owner classes: R2-050, R2-051 (none found), R2-333, R2-163, R2-168, R2-169, R2-170.
- Linked to the owner classes: R2-207 (the symbol), R2-072 (route sign).
- Breadth, from the second reading of tier 1: R2-083, 089, 186, 248, 198, 161, 022, 020, 177, 176, 201, 094, 095, 074, 005.

## The owner classes in Finnish
- **Parking.** The decree has no noun for the bay. It has a purpose clause: "autopaikka … tarkoitettu liikkumis- ja toimimisesteisen henkilön käyttöön". The guide uses "Esteetön autopaikka". The road signs name the vehicle, not the bay: "Invalidin ajoneuvo" (H12.7, M12, still in force at 20260281). Invalidiliitto asked in 2018 that this become "esteetön pysäköintipaikka". Municipal use includes "invapysäköintipaikka", "liikuntaesteisten pysäköintipaikka", "le-paikka" and "pysäköintiruutu". A Tampere guide uses "Liikkumisesteisen autopaikka".
- **Qualifier.** "esteetön/esteettömyys" is the building word (241/2017; rakentamislaki 35 §). "saavutettavuus" is the digital word (306/2019 2 § 4). In planning law, "saavutettavuus" also means geographic reachability (rakentamislaki 46 §). "kaikille sopiva suunnittelu", "Design for All" and "Universal design" appear in the guide's foreword. "sopii pyörätuolille" is narrower, the wheelchair-friendly analogue. So are "Pyörätuolilla saavutettavuus" and "Portaattomuus" (Fintraffic). The F53 sign was renamed to "Esteetön reitti"; the bill had "Vammaiselle tarkoitettu reitti".
- **Vertical transport.** "hissi" is the decree's word. The decree does not define it. Hissiturvallisuuslaki 4 § 1 defines it widely: it includes guides inclined more than 15°. The decree's non-elevator device is "henkilöiden nostoon tarkoitettu laite", which the guide's annex shortens to "nostin". The guide calls these devices "kevythissit". The Lift Safety Act defines "kevythissi" as shafted ("kuilullista pystyhissiä"). Stair devices are "lavallinen porrasnostin" (guide) and "porrashissi" (Tampere). Tampere's "pystyhissi" may be shafted or shaftless.

## Conflations (recorded, not resolved; locators in the TSV)
1. "liikkumisesteisen pysäköintitunnus" is the permit, while "liikkumisesteisen (henkilön) tunnus" is the symbol. 241/2017 itself has both "liikkumisesteisen henkilön tunnuksella" (2 §) and "liikkumisesteisen tunnuksella" (10 §).
2. Tieliikennelaki spells the permit two ways: "liikuntaesteisen" in Liite 3.8 and "liikkumisesteisen" in 39 § and 190 §.
3. **The most surprising:** 306/2019 10 c § is headed "Saavutettavuusvaatimukset", but its body cites the same EU requirements as "esteettömyysvaatimuksista". The two umbrella words name one requirement set in one Act.
4. "henkilöiden nostoon tarkoitettu laite" names both the platform-lift alternative (2 § and 8 §) and the pool-access device (11 § mom. 3).
5. "kevythissi" falls under a "hissi" word but is a machinery-directive device. It straddles R2-163 and R2-170.
6. "esteetön" in rakentamislaki 142 § means "unobstructed", not "accessible".
7. Fintraffic uses "saavutettavuus" for physical access. This is the use that Invalidiliitto (2021, p. 6) asks not to be made for the built environment.
8. Lohja's initiative uses "invapysäköintipaikka", "esteettömät pysäköintipaikat" and "esteettömät autopaikat" for one set of bays.

## Could not obtain
- The HSL park-and-ride guide: 403 directly; the Wayback route reset twice, and the NO-NO pass hit the same reset at about the same time.
- The Kankaanpää grant guide: its URL now returns HTML.
- RT cards: subscription; read only second-hand through IL20.
- Not attempted: Näkövammaisten liitto, Kuuloliitto, Kynnys ry and hel.fi permit pages.

## Self-attack (the five likeliest ways this is wrong)
1. The sense mappings are mine. "Wc-tila" was mapped to universal washroom, "kevythissi" to vertical lift and "Vapaa tila" to clear space. Detect: read each quote against `concepts.tsv`'s `discriminating_test`.
2. Usage types are forced into the brief's vocabulary. Calling the DPO-preferred "esteetön pysäköintipaikka" "colloquial", and calling "liikuntaesteinen" "outdated", are judgments the vocabulary cannot express precisely.
3. Tier 1 is guidance-heavy: OH18 is advice, not law. Filter `$9` for "241/2017" to get the binding layer only.
4. Locator lines come from pdftotext pages. A different extractor would shift line numbers, and two-column PDFs (ILB, FTR) interleave text. Only short quotes from those PDFs were used.
5. Recency: IL18 (2018) and IL20 (2020) predate later sign revisions. The claim that H12.7 is unchanged rests on one consolidated version, 20260281.
