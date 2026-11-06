"""Build equivalents.tsv for the FI/FI equivalents pass, verifying every quote verbatim (after whitespace
collapse) in the saved extracted text, every form verbatim inside its quote, and every quote at most 25 words.
Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FI-FI/build_equivalents.py
Exits 1 on any failure. Writes only equivalents.tsv in this folder. Text files are local extractions (not committed;
owner ruling 2026-11-06, fifth); the manifest line under retrieval-log/ carries URL and sha256."""
import re, sys, csv
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FI-FI'
FIN = 'https://opendata.finlex.fi/finlex/avoindata/v1/akn/fi/act/statute-consolidated/'
# key: (title as written, issuer, URL, text file, tier)
S = {
 'E17': ("Valtioneuvoston asetus rakennuksen esteettömyydestä 241/2017 (consolidated 20240683)", "Valtioneuvosto", FIN + "2017/241/fin@20240683", "c03ce4cfbc8f", "1"),
 'OH18': ("Esteettömyys. Ympäristöministeriön ohje rakennuksen esteettömyydestä (2018)", "Ympäristöministeriö (municipal mirror)", "https://www.kauniainen.fi/wp-content/uploads/2021/04/Ohje_esteettomyys_2018.pdf", "4595d66364eb", "1"),
 'K17': ("Ympäristöministeriön asetus rakennuksen käyttöturvallisuudesta 1007/2017", "Ympäristöministeriö", FIN + "2017/1007/fin@", "e4a15c1d2d22", "1"),
 'TLL': ("Tieliikennelaki 729/2018 (consolidated 20260281)", "Eduskunta", FIN + "2018/729/fin@20260281", "6ba00fb384b0", "2"),
 'HTL': ("Hissiturvallisuuslaki 1134/2016 (consolidated 20250194)", "Eduskunta", FIN + "2016/1134/fin@20250194", "ebc0f2153f9f", "2"),
 'RL': ("Rakentamislaki 751/2023 (consolidated 20260787)", "Eduskunta", FIN + "2023/751/fin@20260787", "0dc0bca6e068", "2"),
 'DPL': ("Laki digitaalisten palvelujen tarjoamisesta 306/2019 (consolidated 20260813)", "Eduskunta", FIN + "2019/306/fin@20260813", "961df2bc87c9", "2"),
 'EAA': ("Laki eräiden tuotteiden esteettömyysvaatimuksista 102/2023", "Eduskunta", FIN + "2023/102/fin@", "f7b1e7a8e851", "2"),
 'TRA9': ("LIITE 9 Tieliikennelain merkkiryhmän H liikennemerkkien mitoitus (2025)", "Traficom", "https://traficom.fi/sites/default/files/media/regulation/LIITE_9_Tieliikennelain_merkkiryhm%C3%A4n_H_liikennemerkkien_mitoitus%202025.pdf", "e90c128e7872", "3"),
 'TRE': ("Rakennussuunnitteluohje. Esteettömyysohje 1.11.2018", "Tampereen Tilapalvelut Oy (City of Tampere)", "https://tampereentilapalvelut.fi/wp-content/materiaalit/suunnitteluohjeet/Rakennussuunnitteluohje_2018_Esteettomyysohje.pdf", "05df15e144da", "4"),
 'TKU': ("Vastaus valtuutettu Matti Vähä-Heikkilän ym. aloitteeseen Liikkumisesteisten pysäköinnin lisääminen Turun ydinkeskusta-alueella (Dnro 4807-2023, 28.2.2025)", "Turun kaupunki", "https://www.turku.fi/paatoksenteko/kaupunginvaltuusto/vastaus/hae/2387310", "07b0cdd0cf02", "4"),
 'LOH': ("Lohjan vammaisneuvoston aloite invapysäköintipaikasta Monkolan eteen (8.5.2025)", "Lohjan vammaisneuvosto (City of Lohja)", "https://www.lohja.fi/wp-content/uploads/2025/05/lohjan-vammaisneuvoston-aloite-invapysakointipaikasta-monkolan-eteen-.pdf", "c8c3213a7c7d", "4"),
 'FTR': ("Pysäkin esteettömyystiedot sekä palvelut ja varusteet", "Fintraffic", "https://www.fintraffic.fi/sites/default/files/2026-03/Esteett%C3%B6myys%20ja%20varusteet.pdf", "84a55101f15a", "4"),
 'IL18': ("Lausunto hallituksen esityksestä tieliikennelaiksi (HE 180/2017 vp), 14.3.2018", "Invalidiliitto ry", "https://www.invalidiliitto.fi/sites/default/files/2018-03/Lausunto%20Tieliikennelaki%20Hallituksen%20esitys%20HE%20180.pdf", "40f96c2c0204", "5"),
 'IL20': ("Esteettömien autopaikkojen riittävyys ja oikeanlainen käyttö (to Kuntaliitto), 29.10.2020", "Invalidiliitto ry", "https://www.invalidiliitto.fi/sites/default/files/2020-11/Kuntaliitto_kirjelma_esteettomatautopaikat.pdf", "c662507b483d", "5"),
 'IL21': ("Lausunto VN/3884/2020 Korkeakoulutuksen saavutettavuussuunnitelma, 07.05.2021", "Invalidiliitto ry", "https://api.hankeikkuna.fi/asiakirjat/a645ce12-4f33-4df4-8d76-b5e729d1dfb2/6991f260-bca1-4104-a825-b8f1eccae1c8/LAUSUNTO_20210507101046.PDF", "dd59afa76b91", "5"),
 'IL24': ("Invalidiliiton lausunto asetusluonnoksesta ... esteettömyysasetuksen 1 §:n muuttamista (VN/10418/2024), 20.6.2024", "Invalidiliitto ry", "https://invalidiliitto.fi/sites/default/files/2024-06/YM_Invalidiliiton%20lausunto%20Esteett%C3%B6myysasetuksen%20teknisest%C3%A4%20p%C3%A4ivityksest%C3%A4_20062024%20.pdf", "0e6b7a8fa8b4", "5"),
 'ILB': ("Invalidiliiton esteettömyystyö (brochure, 2025)", "Invalidiliitto ry", "https://www.invalidiliitto.fi/sites/default/files/2025-09/Invalidiliiton%20esteett%C3%B6myysty%C3%B6%20-esite%20web.pdf", "1389885cba32", "5"),
}
P, Q, Y, L, V = 'R2-050', 'R2-333', 'R2-163', 'R2-168', 'R2-170'
LAB = {'R2-050': 'designated accessible spaces', 'R2-333': 'Accessible', 'R2-163': 'Elevators', 'R2-168': 'Platform lifts',
 'R2-169': 'stair lift', 'R2-170': 'vertical lift', 'R2-207': 'Pictograms and symbols', 'R2-072': 'Accessible route',
 'R2-083': 'Ramp', 'R2-089': 'Handrails', 'R2-186': 'Grab bars', 'R2-248': 'walkers', 'R2-198': 'Assistive listening systems',
 'R2-161': 'Level threshold', 'R2-022': 'Turning areas', 'R2-020': 'Clear space', 'R2-177': 'Universal washrooms',
 'R2-176': 'Washroom facilities', 'R2-201': 'Signage', 'R2-094': 'Tactile attention indicator', 'R2-095': 'Tactile direction indicator',
 'R2-074': 'Accessible path of travel', 'R2-005': 'Clear opening width'}
# (concept_id, form verbatim, usage_type, scope_note, source key, locator, quote verbatim <=25 words, conflation_note)
R = [
 # ---- parking (owner class 1)
 (P, "tarkoitettu liikkumis- ja toimimisesteisen henkilön käyttöön", "code term", "a purpose clause on 'autopaikka', not a compound name; the decree has no noun for the bay", 'E17', "2 § mom. 3", "niistä riittävän määrän, kuitenkin vähintään yhden, on oltava tarkoitettu liikkumis- ja toimimisesteisen henkilön käyttöön.", ""),
 (P, "Esteetön autopaikka", "code term", "guidance-tier heading (ministry guide), not the decree's wording; carries the umbrella qualifier", 'OH18', "2.2.3 heading (p. 14, l. 17)", "2.2.3 Esteetön autopaikka", ""),
 (P, "Invalidin ajoneuvo", "outdated or disfavoured", "in-force sign name (additional panel H12.7); names the VEHICLE, not the bay; Invalidiliitto (IL18 p. 2) asked for it to be replaced", 'TLL', "Liite 3.8, H12.7", "Lisäkilpi H12.7. Invalidin ajoneuvo on ajoneuvo, joka on erityisesti varustettu vammaisen henkilön käyttöön tai kuljetukseen taikka jossa on liikuntaesteisen pysäköintitunnus.", "CONFLATION: the vehicle class is defined by equipment OR by a permit, and the panel is what marks the bay; the same definition spells the permit 'liikuntaesteisen' while 39 § and 190 § spell it 'liikkumisesteisen' (TLL Liite 3.8 vs 39 §)"),
 (P, "invalidin ajoneuvolle tarkoitetulla pysäköintipaikalla", "outdated or disfavoured", "in-force road-marking text (M12); the bay named through the vehicle", 'TLL', "Liite 4.3, M12", "Valkoista invalidin ajoneuvo -merkintää voidaan käyttää liikennemerkillä osoitetulla invalidin ajoneuvolle tarkoitetulla pysäköintipaikalla.", ""),
 ("R2-050", "Invalidin ajoneuvo", "outdated or disfavoured", "sign-drawing register; also a bilingual variant H12.7_2_2 (drawing image unread)", 'TRA9', "p. 2, l. 27", "Invalidin ajoneuvo H12.7 1.6.2020", ""),
 (P, "esteetön pysäköintipaikka", "colloquial", "the form a disabled people's organisation asks the law to use for the bay; not adopted for H12.7 or M12 as of 20260281", 'IL18', "p. 2, ll. 22-23", "on nimetty ”Invalidin ajoneuvo” –käsitteellä, joka on muutettava muotoon esteetön pysäköintipaikka.", "the organisation rejects a vehicle-named sign for a bay-named one"),
 (P, "Esteettömien autopaikkojen", "colloquial", "DPO letter title; 'autopaikka' with the umbrella qualifier", 'IL20', "p. 1, title", "Esteettömien autopaikkojen riittävyys ja oikeanlainen käyttö", ""),
 (P, "Liikkumisesteisille varattujen autopaikkojen", "code term", "quoted by Invalidiliitto from RT card 98-11235 Pysäköintialueet (the card itself not read: second-hand)", 'IL20', "p. 1", "” Liikkumisesteisille varattujen autopaikkojen määrästä määrätään yleensä asemakaavassa.", ""),
 (P, "invapysäköintipaikasta", "colloquial", "the 'inva-' prefix (from 'invalidi') in a municipal disability council's own title", 'LOH', "title (p. 1, l. 1)", "Lohjan vammaisneuvoston aloite invapysäköintipaikasta Monkolan eteen", "the same document calls the same bays 'esteettömät pysäköintipaikat' and 'esteettömät autopaikat' (p. 1): three forms treated as one"),
 (P, "esteettömät pysäköintipaikat", "colloquial", "", 'LOH', "p. 1, l. 3", "esteettömät pysäköintipaikat ovat sisäpihalla", ""),
 (P, "liikuntaesteisten pysäköintipaikkaa", "regional variant", "'liikuntaesteinen' is the older adjective the Road Traffic Act body replaced with 'liikkumisesteinen'; still in municipal use", 'TKU', "p. 1", "Nykytilanteen ydinkeskustan 18 liikuntaesteisten pysäköintipaikkaa sijoittuvat seuraavasti:", ""),
 (P, "le-paikkaa", "colloquial", "abbreviation of 'liikuntaesteisten/liikkumisesteisen' + 'paikka'", 'TKU', "p. 1", "torin alla olevassa maanalaisessa pysäköinti- laitoksessa on kahdessa kerroksessa14 le-paikkaa.", "'le-luvan' in the same answer abbreviates the permit: one prefix for bay and permit"),
 (P, "Liikuntaesteisten pysäköintiruutujen", "colloquial", "'ruutu' = the marked rectangle", 'TKU', "p. 1", "Liikuntaesteisten pysäköintiruutujen lisäksi luvalla voi pysäköidä", ""),
 (P, "Liikkumisesteisen autopaikka", "code term", "municipal design-guide heading", 'TRE', "p. 2, l. 6", "1. Liikkumisesteisen autopaikka", ""),
 # ---- symbol (R2-207), recorded because the parking forms are keyed to it
 ("R2-207", "liikkumisesteisen henkilön tunnuksella", "code term", "the symbol required on the bay", 'E17', "2 § mom. 3", "se on merkittävä liikkumisesteisen henkilön tunnuksella", "CONFLATION: 'liikkumisesteisen pysäköintitunnus' (TLL 39 §) names the PERMIT; 'liikkumisesteisen (henkilön) tunnus' names the SYMBOL; one noun 'tunnus' for both"),
 ("R2-207", "liikkumisesteisen tunnuksella", "code term", "shortened form for the WC sign, in the same decree", 'E17', "10 § mom. 1", "ne on merkittävä liikkumisesteisen tunnuksella.", ""),
 ("R2-207", "kansainvälisellä pyörätuolitunnuksella", "code term", "guidance glosses the decree's symbol as the international wheelchair symbol", 'OH18', "p. 14, l. 25", "on merkittävä liikkumisesteisen tunnuksella eli kansainvälisellä pyörätuolitunnuksella.", "the guide makes 'liikkumisesteisen tunnus' and 'kansainvälinen pyörätuolitunnus' one ('eli')"),
 ("R2-207", "ISA-tunnuksella", "colloquial", "acronym of the English 'International Symbol of Access' inside Finnish", 'TRE', "p. 2, l. 15", "autopaikat varustetaan ISA-tunnuksella", ""),
 # ---- qualifier (owner class 2)
 (Q, "esteettömän", "qualifier", "the instrument's umbrella word (esteetön, lit. 'without obstacle'); scope set by the decree's population carve 'liikkumis- ja toimimisesteinen henkilö'", 'E17', "2 § mom. 1", "jos esteettömän kulkuväylän toteuttaminen olisi rakennuspaikka ja korkeuserot huomioon ottaen mahdotonta", ""),
 (Q, "esteettömyys ja käytettävyys", "qualifier", "the Building Act pairs the umbrella noun with usability; scope WIDER than disabled people: children and older people named", 'RL', "35 §", "että esteettömyys ja käytettävyys otetaan huomioon erityisesti lasten, ikääntyneiden, vammaisten ja liikkumis- ja toimimisesteisten henkilöiden kannalta.", ""),
 (Q, "liikkumiselle esteettöminä", "qualifier", "NOT the accessibility sense: paths kept free of obstruction (maintenance)", 'RL', "142 § mom. 2", "jalankulun ja pyöräilyn väylät säilytetään liikkumiselle esteettöminä ja turvallisina.", "CONFLATION: the same Act uses 'esteetön' for accessibility (35 §) and for 'unobstructed' (142 §)"),
 (Q, "saavutettavuuden", "qualifier", "NOT the disability sense: reachability of services in siting rules", 'RL', "46 §", "liikenneturvallisuuden ja palveluiden saavutettavuuden kannalta.", "CONFLATION: 'saavutettavuus' = geographic reachability here, digital accessibility in DPL 2 § 4"),
 (Q, "saavutettavuudella", "code term", "the digital-services umbrella word, defined for websites and apps; scope: digital only", 'DPL', "2 § 4 kohta", "saavutettavuudella periaatteita ja tekniikoita, joita on noudatettava digitaalisten palvelujen suunnittelussa, kehittämisessä, ylläpidossa ja päivittämisessä", ""),
 (Q, "Saavutettavuusvaatimukset", "code term", "section heading for European Accessibility Act requirements on digital services", 'DPL', "10 c § heading", "Saavutettavuusvaatimukset eräille digitaalisille palveluille", "CONFLATION: the body of 10 c § names the same directive's requirements 'esteettömyysvaatimuksista'; two umbrella words for one requirement set in one Act"),
 (Q, "esteettömyysvaatimuksista", "code term", "products (European Accessibility Act), not buildings", 'EAA', "title", "Laki eräiden tuotteiden esteettömyysvaatimuksista", ""),
 (Q, "kaikille sopiva suunnittelua", "qualifier", "the guide's rendering of CRPD universal design; WIDER scope ('kaikki ihmiset')", 'OH18', "p. 2, ll. 28-29", "Sopimus korostaa kaikille sopiva suunnittelua (Design for All tai Universal design)", "the guide treats 'kaikille sopiva suunnittelu', 'Design for All' and 'Universal design' as one"),
 (Q, "Design for All", "qualifier", "English term used inside the Finnish guide", 'OH18', "p. 2, l. 28", "kaikille sopiva suunnittelua (Design for All tai", ""),
 (Q, "Universal design", "qualifier", "English term used inside the Finnish guide", 'OH18', "p. 2, l. 29", "Universal design), mikä tarkoittaa tilojen ja ympäristöjen suunnitteluvaiheessa tapahtuvaa", ""),
 (Q, "saavutettavuutta", "qualifier", "the guide's word for CRPD minimum standards on access to facilities and services", 'OH18', "p. 2, l. 34", "voimaan tilojen ja palvelujen saavutettavuutta koskevia vähimmäisstandardeja ja -ohjeita", "the guide's own umbrella word is 'esteettömyys'; here 'saavutettavuus' names the CRPD Art. 9 duty for the same facilities"),
 (Q, "fyysisestä saavutettavuudesta", "outdated or disfavoured", "rejected by a disabled people's organisation for the built environment in favour of 'esteettömyys'", 'IL21', "p. 6, ll. 52-53", "Invalidiliitto ei ymmärrä, miksi puhutaan fyysisestä saavutettavuudesta, kun käytettävissä olisi tunnettu ja laajasti käytetty termi ”esteettömyys”.", ""),
 (Q, "esteettömyys ja saavutettavuus", "qualifier", "the DPO's rendering of the CRPD Art. 9 title: both words together", 'IL24', "p. 1, l. 52", "(Artikla 9, esteettömyys ja saavutettavuus)", ""),
 (Q, "Yhdenvertaista palvelua kaikille", "product name", "a label (mark) operated for accessibility communication", 'ILB', "p. 2, ll. 20-21", "Autamme esteettömyydestä viestimisessä mm. Yhdenvertaista palvelua kaikille -merkin avulla.", ""),
 (Q, "sopii pyörätuolille", "qualifier", "NARROWER: wheelchair users only (the analogue of 'wheelchair friendly'), a data value", 'FTR', "p. 8", "tallentuu pysäkkitasolle tieto ”sopii pyörätuolille”.", ""),
 (Q, "Pyörätuolilla saavutettavuus", "qualifier", "NARROWER: wheelchair users; uses 'saavutettavuus' for PHYSICAL access, the use IL21 rejects", 'FTR', "p. 10", "Pyörätuolilla saavutettavuus tuntematon", "CONFLATION with IL21: a public body uses the form the DPO asks not to use for the built environment"),
 (Q, "Portaattomuus", "qualifier", "NARROWER: step-freeness (data field; value 'Portaaton')", 'FTR', "p. 10", "Portaattomuus Ovatko kaikki reitit tälle pysäkille esteettömiä?", "the field 'Portaattomuus' is asked as 'esteettömiä': step-free and accessible treated as one"),
 # ---- accessible route (R2-072): the sign
 ("R2-072", "Esteetön reitti", "code term", "guide sign F53 in the Road Traffic Act", 'TLL', "Liite 3.6, F53", "F53 Esteetön reitti", ""),
 ("R2-072", "Vammaiselle tarkoitettu reitti", "outdated or disfavoured", "the bill's sign name, asked by Invalidiliitto to be renamed; the enacted F53 reads 'Esteetön reitti'", 'IL18', "p. 2, ll. 18-19", "Opastusmerkeissä F53 Vammaiselle tarkoitettu reitti –merkin nimi ja selite tulee vaihtaa esteettömäksi reitiksi.", ""),
 # ---- vertical transport (owner class 3)
 (Y, "hissi", "code term", "the decree's word; it does not define it (OH18 2.8.1)", 'E17', "7 § mom. 1", "Asuinrakennuksessa on oltava portaiden lisäksi hissi", ""),
 (Y, "hissillä nostolaitetta", "code term", "legal definition; WIDER than an elevator in a vertical shaft: guides inclined more than 15 degrees, or a fixed track", 'HTL', "4 § 1 kohta", "hissillä nostolaitetta, joka liikkuu määrättyjen tasojen välillä ja jolla on kuorman kantava yksikkö", ""),
 (Y, "Jälkiasennushissi", "code term", "NARROWER: a lift retrofitted to an existing residential building; may fall below the car minimum", 'OH18', "2.7.3 heading (p. 23, l. 1)", "2.7.3 Jälkiasennushissi asuinrakennuksessa", ""),
 (Y, "henkilöhissin", "code term", "municipal guide: the passenger elevator, beside 'standardihissi'", 'TRE', "p. 3", "Liikkumisesteisille henkilöille soveltuvan henkilöhissin, 8 hengen standardihissin, korin vähimmäismitat", ""),
 (V, "henkilöiden nostoon tarkoitettu laite", "code term", "the decree's alternative to ramp or elevator, fitted for wheelchair and rollator users; type left open", 'E17', "2 § mom. 1", "kiinteästi asennettu pyörätuolin ja pyörillä varustetun kävelytelineen käyttäjälle soveltuva henkilöiden nostoon tarkoitettu laite.", "CONFLATION: the same form names the pool-access device in 11 § mom. 3 ('henkilöiden nostoon tarkoitetulla, itsenäisesti käytettävissä olevalla laitteella'), i.e. a hoist"),
 (V, "henkilöiden nostoon tarkoitetulla, itsenäisesti käytettävissä olevalla laitteella", "code term", "pool access: a hoist or lift into the pool; recorded only for the conflation", 'E17', "11 § mom. 3", "uima-altaaseen 2 momentissa tarkoitetussa rakennuksessa on järjestettävä henkilöiden nostoon tarkoitetulla, itsenäisesti käytettävissä olevalla laitteella.", "see the 2 § mom. 1 row"),
 (V, "kevythissien", "code term", "guidance names the vertical lifting device for wheelchair and rollator users a 'light lift'", 'OH18', "2.8.1 (p. 24, ll. 1-2)", "pystysuoraan nostavaa laitetta. Näiden kevythissien lisäksi on", "CONFLATION: OH18 calls the decree's non-elevator device a kind of 'hissi'; HTL 4 § 3 defines 'kevythissi' as shafted ('kuilullista'), which the CA/US platform-lift sense (R2-168) is not"),
 (V, "kevythissillä kuilullista pystyhissiä", "code term", "legal definition: shafted vertical lift, speed at most 0,15 m/s, machinery-directive device; straddles R2-163 (shaft) and R2-170 (low-speed lift)", 'HTL', "4 § 3 kohta", "kevythissillä kuilullista pystyhissiä, joka on tarkoitettu henkilöiden kuljettamiseen, joka liikkuu rakennuksen kerrostasojen välillä", ""),
 (V, "Pystyhissit", "code term", "municipal guide: vertical lifts with or without a shaft", 'TRE', "p. 3", "Pystyhissit kulkevat tasolta toiselle pystysuoraan ja voivat olla kuilullisia tai kuiluttomia.", "'pystyhissi' covers shafted and shaftless devices, so it spans R2-170 and R2-168"),
 (L, "nostin", "colloquial", "short form in the guide's summary table for the decree's 'henkilöiden nostoon tarkoitettu laite'", 'OH18', "annex table (p. 37, l. 15)", "jos kulkuväylällä on porras, sen yhteydessä on oltava luiska tai nostin", ""),
 (L, "Hisseihin verrattavista henkilöiden nostolaitteista", "code term", "guidance: lifting appliances comparable to lifts, under the machinery directive", 'OH18', "2.8.1 (p. 23)", "Hisseihin verrattavista henkilöiden nostolaitteista säädetään mm. konedirektiivissä", ""),
 ("R2-169", "lavallisia porrasnostimia", "code term", "platform stair lift for wheelchair users, for renovations where a vertical device is impossible", 'OH18', "2.8.1 (p. 24, l. 3)", "pyörätuolin käyttäjälle tarkoitettuja porrasta pitkin nostavia lavallisia porrasnostimia", ""),
 ("R2-169", "Porrashissi", "colloquial", "municipal guide: travels along the stair, no shaft; a temporary solution", 'TRE', "p. 3", "Porrashissi kulkee portaiden suuntaisesti eikä tarvitse omaa hissikuilua.", "CONFLATION: 'porrashissi' (a 'hissi' word) and 'porrasnostin' (a 'nostin' word) name the stair device in two public texts"),
 # ---- breadth: other register concepts, tier 1 second reading and one tier-5 brochure
 ("R2-083", "Luiskalla", "code term", "defined by purpose (replacing a stair) and as part of the route, not by a slope threshold", 'OH18', "1.3 (p. 7)", "Luiskalla tarkoitetaan liikkumis- ja toimimisesteisille tarkoitettua (portaan korvaavaa) kulkuyhteyttä tasojen välillä. Luiska on kulkuväylän osa.", ""),
 ("R2-089", "käsijohde", "code term", "", 'K17', "9 § mom. 1", "Portaassa ja luiskassa on oltava käsijohde koko pituudella ja molemmilla puolilla syöksyä.", ""),
 ("R2-186", "tukikaiteet", "code term", "grab bars; 'kaide' is also the guard (K17), and 'käsituet' are the fold-down arm supports", 'OH18', "2.10 (p. 29, l. 22)", "Liikkumisesteisen henkilön tarvitsemia varusteita ovat mm. wc-istuimen käsituet sekä tukikaiteet.", ""),
 ("R2-186", "käsituet", "code term", "arm supports at the WC; a second grab-bar form", 'OH18', "2.10 (p. 29, l. 22)", "wc-istuimen käsituet sekä tukikaiteet.", ""),
 ("R2-248", "pyörillä varustetun kävelytelineen", "code term", "the decree's word for the rollator, always beside the wheelchair", 'E17', "2 § mom. 1", "pyörätuolin ja pyörillä varustetun kävelytelineen käyttäjälle soveltuva", ""),
 ("R2-248", "rollaattoria", "colloquial", "marked 'ns.' (so-called) by the guide itself", 'OH18', "1.3 (p. 7, l. 15)", "koskee myös pyörillä varustettua kävelytelinettä kuten esimerkiksi ns. rollaattoria.", "the same sentence folds the rollator into every rule about the wheelchair ('Mitä ... sanotaan pyörätuolista, koskee myös')"),
 ("R2-198", "äänensiirtojärjestelmä", "code term", "WIDER class; the induction loop is one kind", 'E17', "12 § mom. 1", "siinä on oltava induktiosilmukka tai muu vastaava äänensiirtojärjestelmä", ""),
 ("R2-198", "induktiosilmukka", "code term", "NARROWER: the hearing loop", 'E17', "12 § mom. 1", "induktiosilmukka tai muu vastaava äänensiirtojärjestelmä", ""),
 ("R2-161", "Kynnyksettömissä", "code term", "inflected 'kynnyksetön' (threshold-free); guidance", 'OH18', "2.4.3 (p. 18, l. 15)", "Kynnyksettömissä ovissa voidaan käyttää erilaisia tiivisteitä", ""),
 ("R2-161", "tasoeroa tai kynnystä", "code term", "the decree states the threshold rule as a prohibition with a 20 mm exception", 'E17', "4 § mom. 3", "Oven yhteydessä ei saa olla tasoeroa tai kynnystä", ""),
 ("R2-022", "kääntymistila", "code term", "a disc given by its diameter", 'E17', "6 § mom. 2", "on asunnon eteisessä ja keittiössä oltava kääntymistila, jonka halkaisija on vähintään 1 300 millimetriä.", ""),
 ("R2-020", "Vapaa tila", "code term", "defined as a volume to 2000 mm height", 'OH18', "2.10.4 (p. 28)", "Vapaa tila tarkoittaa esteistä vapaata tilaa lattiatasosta 2000 mm korkeuteen saakka.", ""),
 ("R2-177", "wc-tilojen", "code term", "a WC room usable regardless of the user's and assistant's sex, marked with the symbol: the single-user room sense", 'E17', "10 § mom. 1", "Edellä tarkoitettujen wc-tilojen on sijaittava siten, ettei käyttäjän ja avustajan sukupuoli vaikuta mahdollisuuteen käyttää niitä", "the guide lets some such rooms sit inside sex-separated WC groups (OH18 2.10.1, p. 28), so the single-user sense is not fixed"),
 ("R2-176", "wc- ja pesutila", "code term", "the dwelling WC-and-washing room; the guide extends it to dry and chemical toilets", 'OH18', "1.3 (p. 7, l. 17)", "Mitä tässä ohjeessa sanotaan wc- ja pesutilasta, koskee myös kuivakäymälää", "CONFLATION: a dry toilet ('kuivakäymälä') is treated as a 'wc- ja pesutila'"),
 ("R2-176", "hygieniatila", "code term", "other hygiene rooms (changing, washing, sauna) outside dwellings", 'E17', "11 § (heading)", "Muu hygieniatila muussa kuin asuinrakennuksessa", ""),
 ("R2-201", "pystyopasteen", "code term", "vertical sign at the bay, beside a marking on the surface", 'OH18', "2.2.3 (p. 14, l. 26)", "suositellaan sijoitettavaksi pystyopasteen lisäksi myös autopaikan pintaan.", ""),
 ("R2-095", "ohjaavaa", "code term", "guiding (direction) marking felt with the white cane; no profile named", 'OH18', "2.5.1 (p. 19)", "näkövammaisen valkoisen kepin avulla tuntuvaa ohjaavaa tai varottavaa merkintää", "the guide files both kinds under 'tuntokontrasti' (touch contrast), with underfoot material difference"),
 ("R2-094", "varottavaa", "code term", "warning (attention) marking; no dome profile named", 'OH18', "2.5.1 (p. 19)", "tuntuvaa ohjaavaa tai varottavaa merkintää", ""),
 ("R2-095", "koholistalla", "code term", "a continuous raised strip fixed to the floor as a guidance line", 'OH18', "2.5.1 (p. 19)", "pintaan kiinnitetyllä yhtenäisellä koholistalla", ""),
 ("R2-074", "Kulkureittien", "colloquial", "DPO brochure uses 'kulkureitti' where the decree says 'kulkuväylä'", 'ILB', "p. 1", "Kulkureittien pinnat ovat tasaisia", ""),
 ("R2-005", "vapaa kulkuaukko", "colloquial", "DPO brochure; the decree says 'oven vapaa leveys'", 'ILB', "p. 1", "Ovien vapaa kulkuaukko on", ""),
 ("R2-005", "oven ja kulkuaukon vapaan leveyden", "code term", "", 'E17', "4 § mom. 2", "johtavan oven ja kulkuaukon vapaan leveyden on oltava vähintään 800 millimetriä.", ""),
]
SEEDS = [  # flagged model-generated; never findings
 ("R2-083", "ramppi", "colloquial ramp word in ordinary Finnish; 0 hits (stem 'ramppi') in E17, K17, OH18"),
 ("R2-050", "invapaikka", "colloquial bay word; the attested form is 'invapysäköintipaikka' (LOH); the short form is not attested by these texts"),
 ("R2-169", "tuolihissi", "seated stair lift; named in a municipal grant guide per the search engine's summary (Kankaanpää 2019), which could not be retrieved (HTML returned)"),
]
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {}
fail = 0
for k, v in S.items():
    TXT[k] = norm(open(f'{D}/text/{v[3]}.txt', encoding='utf-8').read())
out = []
for c, form, ut, sc, src, loc, q, conf in R:
    t, iss, url, tf, tier = S[src]
    problems = []
    if norm(q) not in TXT[src]: problems.append('quote not in text')
    if form not in q: problems.append('form not in quote')
    if len(q.split()) > 25: problems.append(f'quote {len(q.split())} words')
    if c not in LAB: problems.append('no label')
    if problems: fail += 1; print('FAIL', src, loc, form, problems)
    out.append([c, LAB.get(c, ''), form, 'fi', 'FI', ut, sc, tier, f'{t}; {iss}; {url}', loc, q, conf])
for c, form, note in SEEDS:
    out.append([c, LAB[c], form, 'fi', 'FI', 'unattested seed', 'MODEL-GENERATED, flagged: ' + note, 'seed', '', '', '', ''])
with open(f'{D}/equivalents.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note', 'attestation_tier', 'source', 'locator', 'quote', 'conflation_note'])
    w.writerows(out)
print(f'rows {len(out)} (attested {len(R)}, seeds {len(SEEDS)}), failures {fail}')
sys.exit(1 if fail else 0)
