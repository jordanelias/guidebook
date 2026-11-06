"""Build observations / coverage / reverse-harvest TSVs for the FI/FI terminology pass (adapted from FR-FR/build.py),
verifying every quote (after whitespace collapse) in the saved extracted text, and every phrase inside its quote.
Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FI-FI/build.py
Exits 1 if any quote or phrase fails to verify. Read-only apart from the three TSVs in this folder."""
import re, sys, csv
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FI-FI'
INST = {
 'E17': ("Valtioneuvoston asetus rakennuksen esteettömyydestä 241/2017 (consolidated, as amended by 683/2024)", D + '/text/c03ce4cfbc8f.txt'),
 'K17': ("Ympäristöministeriön asetus rakennuksen käyttöturvallisuudesta 1007/2017", D + '/text/e4a15c1d2d22.txt'),
 'OH18': ("Esteettömyys. Ympäristöministeriön ohje rakennuksen esteettömyydestä (2018)", D + '/text/4595d66364eb.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

LIT = "Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)"
SURF = "Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant"
# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note — ours)
OBS = [
 (LIT, "valaistu", "K17", "10 § mom. 1", "Rakennuksen ja sen ympäristön on oltava käytön ja huollon turvallisuuden mahdollistavalla tavalla valaistu.", "a performance duty (lit so as to allow safe use and maintenance); no illuminance quantity"),
 (LIT + "|lighting levels", "Valoisuus ja valaistus", "K17", "10 § (heading)", "Valoisuus ja valaistus", "'valoisuus' (brightness/luminance of surfaces) paired with 'valaistus' (lighting)"),
 ("lighting levels|LRV contrast (parameter 8)", "valoisuuserot", "K17", "10 § mom. 2", "Rakennuksen pintojen ja valaistuksen on oltava sellaiset, että havaitsemisen kannalta tarvittavat valoisuuserot saavutetaan.", "luminance differences of surfaces and lighting needed for perception; unquantified"),
 (LIT, "häikäisemättömällä valaistuksella", "OH18", "2.2.1 (p. 12)", "riittävän voimakkaalla, mutta häikäisemättömällä valaistuksella", "guidance: strong but glare-free lighting improves perceivability of the route"),
 (SURF, "pinnaltaan tasainen, kova ja luistamaton", "E17", "2 § mom. 1", "Rakennukseen on oltava vähintään 1 200 millimetriä leveä, helposti havaittava, pinnaltaan tasainen, kova ja luistamaton kulkuväylä", "even, hard and non-slip; adds 'helposti havaittava' (easily perceivable) to the surface triple"),
 ("Floor surface is stable, firm, and non-slip", "pinnaltaan tasainen ja luistamaton", "E17", "5 § mom. 1", "on oltava helposti havaittava, pinnaltaan tasainen ja luistamaton.", "interior route drops 'kova' (hard)"),
 ("Floor surface is stable, firm, and non-slip", "kompastumis- ja liukastumisriski on pieni", "K17", "12 § (Lattiapinnat)", "Lattiapinnan on oltava tasainen ja valmistettu tilan käyttötarkoitus huomioiden soveltuvasta materiaalista siten, että kompastumis- ja liukastumisriski on pieni.", "stated as low trip and slip risk, not as a surface property"),
 (SURF, "liukas märkänä", "OH18", "2.2.1 (p. 12)", "Pinnaltaan tasainen ja kova kulkuväylä ei myöskään saa olla liukas märkänä.", "wet-slip condition, guidance"),
 ("Seating", "Kokoontumistilan istuimet", "K17", "22 § (heading)", "Kokoontumistilan istuimet", "assembly seating (fixing and coupling of chairs), not rest seating"),
 ("Seating", "kiinteät istuimet", "E17", "12 § mom. 2", "Jos 1 momentissa tarkoitetussa tilassa on kiinteät istuimet, esteettömien sisääntuloväylien on johdettava useammalle kuin yhdelle istuinriville", "fixed seats in assembly spaces"),
 ("Handrails", "käsijohde", "K17", "9 § mom. 1", "Portaassa ja luiskassa on oltava käsijohde koko pituudella ja molemmilla puolilla syöksyä.", "both sides, full length of the flight ('syöksy')"),
 ("Handrails", "kaksi käsijohdetta päällekkäin", "K17", "9 § mom. 1", "Tarvittaessa on oltava kaksi käsijohdetta päällekkäin lasten ja pyörätuolilla liikkuvien huomioon ottamiseksi.", "a second, lower handrail for children and wheelchair users"),
 ("Clear width|Door width (parameter 9)|width", "vapaan leveyden", "E17", "4 § mom. 1", "oven vapaan leveyden on oltava vähintään 850 millimetriä", "'vapaa leveys' inflected; the clear width of the opening"),
 ("Clear width|Door width (parameter 9)", "Oven vapaalla leveydellä", "OH18", "2.4.1 (p. 17)", "Oven vapaalla leveydellä tarkoitetaan kulkuaukon todellista leveyttä avatun ovilevyn kohdalla.", "defined as the actual width of the opening at the opened leaf"),
 ("Accessible path of travel", "esteettömän kulkuväylän", "E17", "2 § mom. 1", "jos esteettömän kulkuväylän toteuttaminen olisi rakennuspaikka ja korkeuserot huomioon ottaen mahdotonta", "'kulkuväylä' is the route object for outdoor approach, interior circulation and ramp alike"),
 ("Accessible path of travel", "Rakennukseen johtava kulkuväylä", "E17", "2 § (heading)", "Rakennukseen johtava kulkuväylä", "the approach route, from the plot boundary and from spaces serving the building"),
 ("Clear signage", "Selkeä ja loogisesti etenevä opastus", "OH18", "2.6.1 (p. 20)", "Selkeä ja loogisesti etenevä opastus auttaa selviytymään tiloissa itsenäisesti.", "guidance only; the decree requires only the wheelchair symbol"),
 ("Clear signage", "liikkumisesteisen henkilön tunnuksella", "E17", "2 § mom. 3", "se on merkittävä liikkumisesteisen henkilön tunnuksella", "the only signage the decree mandates (parking, WC, hygiene spaces)"),
 ("Audio accessibility and communication enhancement technologies", "induktiosilmukka tai muu vastaava äänensiirtojärjestelmä", "E17", "12 § mom. 1", "on äänentoistojärjestelmä, siinä on oltava induktiosilmukka tai muu vastaava äänensiirtojärjestelmä", "triggered by the presence of a sound-reinforcement system"),
 ("Audio accessibility and communication enhancement technologies", "palvelupistesilmukka", "OH18", "2.12.2 (p. 31)", "Tällainen tilanne on esimerkiksi ns. palvelupistesilmukka yleisön palvelutilassa.", "counter loop"),
 ("Level landings with clear space", "vaakasuora tasanne", "E17", "2 § mom. 2", "Luiskan ala- ja yläpäässä on oltava vähintään 1 500 millimetriä pitkä vaakasuora tasanne.", ""),
 ("Level landings with clear space", "Ulko-oven edessä olevan tasanteen", "E17", "3 § mom. 2", "Ulko-oven edessä olevan tasanteen on oltava vähintään 1 500 millimetriä leveä ja vähintään 1500 millimetriä pitkä.", ""),
 ("Level landings with clear space", "tasanteen", "K17", "6 § mom. 1", "Rakennuksen ja sen ulkotilojen tasanteen on oltava turvallinen, riittävän väljä ja tarkoitukseensa soveltuva.", ""),
 ("Level landings with clear space and at regular intervals", "välitasanne", "E17", "2 § mom. 2", "jonka jälkeen kulkuväylällä on oltava vaakasuora vähintään 2 000 millimetriä pitkä välitasanne", "intermediate landing triggered by rise per run, not by run length"),
 ("Level landings with clear space and at regular intervals|Turning circle (parameter 5)", "vähintään 15 metrin välein kääntymistila", "E17", "5 § mom. 2", "kulkuväylällä on oltava vähintään 15 metrin välein kääntymistila, jonka halkaisija on vähintään 1 500 millimetriä", "turning spaces at intervals on narrow interior routes"),
 ("Clear space for approach|clearance", "avautumispuolen etäisyys seinän sisänurkasta", "E17", "3 § mom. 1", "Rakennuksen ulko-oven avautumispuolen etäisyys seinän sisänurkasta tai muusta kiinteästä esteestä on oven ulkopuolella oltava vähintään 400 millimetriä.", "latch-side clearance from an inside corner"),
 ("Clear space for approach|clearance", "vapaa tila", "E17", "10 § mom. 2", "Edellä 1 momentissa tarkoitetussa wc-tilassa on oltava halkaisijaltaan vähintään 1 500 millimetriä vapaa tila.", "'vapaa tila' = clear floor space, given as a circle diameter"),
 ("clearance", "esteistä vapaata tilaa lattiatasosta 2000 mm korkeuteen saakka", "OH18", "2.10.4 (p. 28)", "Vapaa tila tarkoittaa esteistä vapaata tilaa lattiatasosta 2000 mm korkeuteen saakka.", "clear space is a volume to a stated height"),
 ("Shelter", "suojattu kinostumiselta katoksella", "K17", "18 § mom. 1", "Sisäänkäynnin on lisäksi oltava suojattu kinostumiselta katoksella.", "entrance canopy against snow drift; a safety-decree rule, not in the accessibility decree"),
 ("Shelter", "lumelta ja jäältä lumiestein", "K17", "18 § mom. 1", "on oltava suojattu rakennuksen katolta putoavalta lumelta ja jäältä lumiestein", "snow guards over entrances and routes"),
 ("Riser height and tread depth|riser|tread|height|depth", "askelman nousun ja etenemän", "K17", "4 § mom. 1", "Portaan askelman nousun ja etenemän suhteen on oltava portaan käyttötarkoitukseen nähden helppokulkuinen.", "'nousu' = rise (quantity), 'etenemä' = going; the rule is their ratio, then tabulated per building use"),
 ("Riser height and tread depth|riser|tread", "ulkoportaiden etenemän", "K17", "5 §", "Katettujen tai lämmitettyjen ulkoportaiden etenemän on oltava vähintään 300 millimetriä", "outdoor stairs differ by covered/heated vs not"),
 ("No open riser", "Porrasaskelmien välistä", "K17", "8 § mom. 4", "Porrasaskelmien välistä saa mahtua enintään 100 millimetrin mittainen kuutio.", "a gap limit by test cube, not a closed-riser rule"),
 ("Level threshold", "ei saa olla tasoeroa tai kynnystä", "E17", "4 § mom. 3", "Oven yhteydessä ei saa olla tasoeroa tai kynnystä, ellei se ole ääni-, kosteus- tai muiden vastaavien olosuhteiden vuoksi välttämätöntä.", "default is no threshold; an exception route for acoustic and moisture reasons"),
 ("Level threshold", "Kynnyksettömissä ovissa", "OH18", "2.4.3 (p. 18)", "Kynnyksettömissä ovissa voidaan käyttää erilaisia tiivisteitä", ""),
 ("Height clearance (if sheltered or parkade)|Headroom clearance (parameter 11)|Headroom", "kulkuväylän vähimmäiskorkeus", "K17", "14 § mom. 1 (heading: Kulkukorkeus)", "Huonetilan kulkuväylän vähimmäiskorkeus on 2 100 millimetriä", "headroom of a route; no parkade rule"),
 ("Height clearance (if sheltered or parkade)|Headroom clearance (parameter 11)|Headroom and protruding objects|Protruding objects", "alareunan vapaa korkeus", "K17", "19 § (heading: Ulkonevien rakennusosien korkeusasema)", "Rakennuksesta ulkonevan rakennusosan, laitteen tai varusteen kuten parvekkeen, erkkerin, katoksen, opasteen, valaisinlaitteen ja markiisin alareunan vapaa korkeus", "overhead projections: 'vapaa korkeus' unless protected against collision"),
 ("Edge protection", "suojareuna", "E17", "2 § mom. 2", "sen reunassa on oltava vähintään 50 millimetriä korkea suojareuna, jos luiska ei rajaudu kiinteään rakenteeseen", "ramp edge upstand"),
 ("Edge protection", "suojareunan tarkoitus", "OH18", "2.2.2 (p. 13)", "Asetuksen toisen momentin edellyttämän suojareunan tarkoitus on estää pyörätuolin tai muun pyörillä varustetun apuvälineen pyörien suistuminen luiskan reunan yli.", "purpose stated: stop wheels running off the edge"),
 ("Edge protection", "korotuksella, joka estää luistamisen reunan yli", "K17", "6 § mom. 1", "Portaan ja tasanteen sivureunat on varustettava korotuksella, joka estää luistamisen reunan yli", "stair and landing side-edge upstand"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "tummuuserojen tai huomiomerkintöjen avulla", "K17", "10 § mom. 3", "Kulkureitillä olevat luiskat, askelmat, kynnykset ja tasoerot on osoitettava selvästi valaistuksen ja pintojen tummuuserojen tai huomiomerkintöjen avulla.", "steps, ramps, thresholds and level changes marked by lighting, luminance difference or attention markings; no strip and no slip property"),
 ("Tactile attention indicators (truncated domes)", "valkoisen kepin avulla tuntuvaa ohjaavaa tai varottavaa merkintää", "OH18", "2.5.1 (p. 19)", "näkövammaisen valkoisen kepin avulla tuntuvaa ohjaavaa tai varottavaa merkintää", "guiding OR warning marking felt with the white cane; no dome geometry"),
 ("Tactile attention indicators (truncated domes)", "tuntokontrastein", "OH18", "2.2.1 (p. 12)", "kun ne erottuvat ympäristöstään tummuus- ja tuntokontrastein", "'tuntokontrasti' (tactile contrast) paired with 'tummuuskontrasti'"),
 ("Slope|gradient", "kulkuväylän kaltevuus", "E17", "2 § mom. 1", "Ulkotilassa sijaitsevan kulkuväylän kaltevuus saa olla enintään viisi prosenttia.", "route slope; same word as ramp slope"),
 ("Ramp gradient (parameter 3)|Slope|gradient", "Luiskan kaltevuus", "E17", "2 § mom. 2", "Luiskan kaltevuus saa olla enintään viisi prosenttia.", "a second, steeper limit applies when total rise is limited"),
 ("Outlets and switches are at accessible heights|Accessible controls", "Painikkeet, kytkimet ja säätimet", "OH18", "2.6.1 (p. 20)", "Painikkeet, kytkimet ja säätimet soveltuvat käyttäjille, kun ne ovat helppokäyttöisiä ja sijaitsevat sopivalla korkeudella.", "switches and controls only; socket-outlets ('pistorasia') 0/0/0"),
 ("Accessible door hardware", "ovenkahvaan", "OH18", "2.3.1 (p. 15)", "pääsee tarpeeksi lähelle ulottuakseen ovenkahvaan ja avaamaan oven", "door handle as a reach target; the decree states only 'helposti avata'"),
 ("Accessible door hardware|Operating force (parameter 6)|force", "oven avaamiseen tarvittavan voiman suuruuden", "OH18", "2.4.2 (p. 17)", "oven avaamiseen tarvittavan voiman suuruuden tai hallintalaitteiden", "opening force named but not quantified"),
 ("Accessible door hardware", "voi sen helposti avata", "E17", "4 § mom. 4", "liikkumis- tai toimimisesteinen henkilö voi sen helposti avata", "performance wording"),
 ("Accessible controls", "Hissin hallintalaitteisto", "OH18", "2.8.2 (p. 24)", "Hissin hallintalaitteisto sijoitetaan myös liikkumis- ja toimimisesteisille soveltuvalle korkeudelle.", ""),
 ("level", "tasoero", "E17", "8 § mom. 1", "Jos muussa rakennuksessa kuin asuinrakennuksessa oleva tasoero on pienempi kuin rakennuksen kerroskorkeus", "level difference, compared with the storey height to choose ramp/lift"),
 ("level", "Yhteys tasojen välillä", "E17", "7 § (heading)", "Yhteys tasojen välillä asuinrakennuksessa", "'taso' = level; also 'kerrostaso', 'sisäänkäyntitaso'"),
 ("number", "riittävä määrä pyörätuolipaikkoja", "E17", "12 § mom. 2", "ja niille on sijoitettava riittävä määrä pyörätuolipaikkoja", "an unquantified 'sufficient number'"),
 ("number|ratio", "vähintään viisi prosenttia majoitustiloista", "E17", "13 §", "on vähintään viisi prosenttia majoitustiloista, kuitenkin vähintään yhden majoitustilan", "proportional count with a floor of one"),
 ("depth", "1 400 millimetriä syvä", "E17", "7 § mom. 3", "vähintään 1 400 millimetriä syvä", "lift car depth"),
 ("size", "korin suositeltu vähimmäiskoko", "OH18", "2.7.2 (p. 22)", "korin suositeltu vähimmäiskoko on 1400 mm x 1400 mm", "lift car size, guidance"),
 ("capacity", "Kokoontumistilan henkilömäärä", "K17", "21 § (heading)", "Kokoontumistilan henkilömäärä", "occupant number of an assembly space, not lift capacity"),
 ("distance", "etäisyydelle takaseinästä", "E17", "10 § mom. 2", "Wc-istuin on sijoitettava 200–300 millimetrin etäisyydelle takaseinästä.", "WC-pan distance from back wall"),
 ("ratio", "nousun ja etenemän suhteen", "K17", "4 § mom. 1", "Portaan askelman nousun ja etenemän suhteen", "rise-to-going ratio"),
 ("Corridor width (parameter 4)", "kulkuväylä on leveydeltään alle 1 500 millimetriä", "E17", "5 § mom. 2", "Jos 1 momentissa tarkoitettu kulkuväylä on leveydeltään alle 1 500 millimetriä", "no minimum interior route width; width below a threshold triggers turning spaces"),
 ("Corridor width (parameter 4)", "pitkällä kapealla käytävällä", "OH18", "2.5.1 (p. 19)", "sujuva sivuuttaminen pitkällä kapealla käytävällä", "'käytävä' in the corridor sense appears in the guide only"),
 ("Turning circle (parameter 5)", "kääntymistila, jonka halkaisija", "E17", "6 § mom. 2", "on asunnon eteisessä ja keittiössä oltava kääntymistila, jonka halkaisija on vähintään 1 300 millimetriä", "turning space given by diameter; two sizes by dwelling type"),
 ("LRV contrast (parameter 8)", "tummuuskontrasti", "OH18", "2.10.2 (p. 28)", "jossa on selkeä tummuuskontrasti ja joka on myös tuntoaistilla havaittava", "darkness contrast; never quantified, no LRV/luminance term"),
 ("Ramp run length (parameter 12)", "yhtäjaksoisen luiskan korkeusero", "E17", "2 § mom. 2", "Tällöin yhtäjaksoisen luiskan korkeusero saa olla enintään 500 millimetriä", "run limited by rise per continuous ramp, not by length"),
 ("Enclosures", "kiinteää suihkuseinää", "OH18", "2.9.2 (p. 26)", "esimerkiksi suihkun ilman suihkuallasta ja kiinteää suihkuseinää", "fixed shower screen, mentioned only as absent from the transfer space"),
 ("Landscaping elements|Vegetation", "sopivin istutuksin", "K17", "17 § mom. 1", "on osoitettava tarkoituksenmukaisin kaitein tai sopivin istutuksin", "plantings as edge protection near play areas"),
]
REGISTER = [  # catalogue 2.1 (32), 2.2 (18), base parameters (10), B651 headings RHFAC does not name (15)
 "Well-illuminated (if site expected to be lit)", "Surface is firm, stable and slip resistant", "Seating", "Handrails", "Clear width",
 "Accessible path of travel", "Drainage", "Clear signage", "Audio accessibility and communication enhancement technologies",
 "Level landings with clear space", "Floor surface is stable, firm, and non-slip", "Clear space for approach",
 "Well illuminated (if required for expected usage)", "Surface is stable, firm, and slip resistant", "Shelter",
 "Riser height and tread depth", "Nosing design", "No open riser", "Level threshold", "Height clearance (if sheltered or parkade)",
 "Edge protection", "Colour-contrasted and slip-resistant strip on nosing", "Tactile attention indicators (truncated domes)", "Slope",
 "Sink faucet is easy to use or automatic", "Outlets and switches are at accessible heights", "Microwave mounting height accessible and safe",
 "Level landings with clear space and at regular intervals", "Colour-contrasted and slip-resistant strip", "Accessible lockers",
 "Accessible door hardware", "Accessible controls",
 "height", "level", "width", "clearance", "number", "slope", "depth", "riser", "tread", "force", "time", "gradient", "size", "volume",
 "capacity", "distance", "lighting levels", "ratio",
 "Ramp gradient (parameter 3)", "Corridor width (parameter 4)", "Turning circle (parameter 5)", "Operating force (parameter 6)",
 "Reverberation time (parameter 7)", "LRV contrast (parameter 8)", "Door width (parameter 9)", "Colour temperature (parameter 10)",
 "Headroom clearance (parameter 11)", "Ramp run length (parameter 12)",
 "Gratings", "Headroom and protruding objects", "Headroom", "Protruding objects", "Spouts", "Lavatories", "Enclosures",
 "Speed bumps", "Bollards", "Landscaping elements", "Flower or shrub planters", "Vegetation", "Guy wires", "Scaffolding", "Gradation limits",
]
ALIAS = {"slope": "Slope"}
PARTIAL = {  # concept -> why the Finnish match is not the English concept (ours)
 "Seating": "DIFFERENT SENSE: assembly seating only; no rest seating on routes ('penkki' only as tiered benches, 'levähd*' 0/0/0)",
 "No open riser": "NARROWER: a 100 mm test-cube gap limit between steps, not a closed-riser rule",
 "Height clearance (if sheltered or parkade)": "NARROWER: general headroom and overhead projections; no parking-garage clearance",
 "Colour-contrasted and slip-resistant strip on nosing": "BROADER: steps marked by luminance difference or attention marking; no strip, no nosing, no slip property",
 "Colour-contrasted and slip-resistant strip": "BROADER: as above",
 "Tactile attention indicators (truncated domes)": "BROADER: guidance names guiding or warning cane-detectable marking; no domes, nothing in either decree",
 "Outlets and switches are at accessible heights": "NARROWER: switches and controls at 'sopivalla korkeudella' in guidance; no socket-outlets",
 "Accessible door hardware": "PARTIAL: the decree states only ease of opening; handle named in guidance as reach target",
 "Operating force (parameter 6)": "PARTIAL: opening force named in guidance, never quantified",
 "force": "PARTIAL: as parameter 6",
 "LRV contrast (parameter 8)": "BROADER: 'tummuuskontrasti'/'valoisuuserot' never quantified; no LRV or luminance-contrast term",
 "lighting levels": "PARTIAL: no illuminance quantity; only 'valoisuuserot' (luminance differences)",
 "capacity": "DIFFERENT SENSE: assembly occupant number, not lift capacity",
 "ratio": "PARTIAL: rise-to-going ratio and a 5 % room share; no room-type mix",
 "Ramp run length (parameter 12)": "CARVED DIFFERENTLY: limited by rise of a continuous ramp (500 mm), not by its length",
 "Enclosures": "NARROWER: only a fixed shower screen, named as something not to place in the transfer space",
 "Landscaping elements": "DIFFERENT PURPOSE: plantings as fall protection near play areas, not as route obstacles",
 "Vegetation": "DIFFERENT PURPOSE: as above",
 "Clear signage": "PARTIAL in the decrees (wheelchair symbol only); FOUND in guidance ('opastus')",
}
ABSENT = {
 "Drainage": "no drainage rule; 'kuivat*', 'sadeve*', 'kaivo' 0/0/0; 'vede*' in OH18 only as waterproofing and water-pressure lift",
 "Nosing design": "'nokka' 0/0/0; K17 10 § marks steps by contrast but does not treat the nosing",
 "Sink faucet is easy to use or automatic": "'hana', 'pesuallas' 0/0/0",
 "Microwave mounting height accessible and safe": "'mikro*' 0/0/0; kitchen treated only as a turning space",
 "Accessible lockers": "'lokero', 'kaappi' 0/0/0; storage appears only as 'säilytystila' (rooms serving the building)",
 "time": "no timing quantity in any of the three texts",
 "volume": "'äänenvoim*' 0/0/0",
 "Reverberation time (parameter 7)": "'kaiunta' 0/0/0; OH18 2.6.1 and 2.12.2 defer room acoustics ('huoneakustiikasta') to decree 796/2017, NOT READ",
 "Colour temperature (parameter 10)": "'värilämpö*', 'kelvin' 0/0/0",
 "Gratings": "'ritil*' only as 'puuritilällä' (timber decking to raise a balcony floor, OH18 2.4.4): different sense",
 "Spouts": "0/0/0 (no drinking fountain)",
 "Lavatories": "no wash-basin rule; 'pesuallas' 0/0/0 ('wc- ja pesutila' is a room, not a basin)",
 "Speed bumps": "'hidast*', 'töyssy' 0/0/0",
 "Bollards": "'pollari' 0/0/0; K17 13 § 'puomi' is a barrier arm (different element)",
 "Flower or shrub planters": "no planter element; only 'istutuksin' (see Landscaping elements)",
 "Guy wires": "0/0/0",
 "Scaffolding": "only 'riipputelineiden kiinnitysrakenteet' (K17 25 §, facade maintenance fixings): different sense",
 "Gradation limits": "0/0/0",
}
REV = [  # (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss — OURS)
 ("liikkumis- ja toimimisesteisen henkilön", "population carve (defined)", "E17", "2 § mom. 3", "on oltava tarkoitettu liikkumis- ja toimimisesteisen henkilön käyttöön", "two-part carve: impaired in moving / impaired in functioning"),
 ("Toimimisesteisiä ovat", "population carve (definition)", "OH18", "1.3 (p. 7)", "Toimimisesteisiä ovat mm. henkilöt, joilla on näkemisen, kuulemisen, muistamisen, ymmärtämisen tai hahmottamisen haasteita.", "sensory and cognitive needs folded into one defined category"),
 ("Liikkumisesteisiä henkilöitä", "population carve (definition)", "OH18", "1.3 (p. 7)", "Liikkumisesteisiä henkilöitä ovat mm. pyörätuolin ja pyörillä varustetun kävelytelineen tai muun liikkumisen apuvälineen käyttäjät sekä henkilöt, joilla on rajoitteita käsien käyttämisessä.", "includes people with limited hand use"),
 ("pyörillä varustetun kävelytelineen", "reference user / device", "E17", "2 § mom. 1", "pyörätuolin ja pyörillä varustetun kävelytelineen käyttäjälle soveltuva henkilöiden nostoon tarkoitettu laite", "the wheeled walker (rollator) is a named design user alongside the wheelchair throughout"),
 ("henkilöiden nostoon tarkoitettu laite", "element", "E17", "2 § mom. 1", "kiinteästi asennettu pyörätuolin ja pyörillä varustetun kävelytelineen käyttäjälle soveltuva henkilöiden nostoon tarkoitettu laite", "platform lift as an alternative to a ramp"),
 ("porrasnostimia", "element", "OH18", "2.8.1 (p. 24)", "lavallisia porrasnostimia", "inclined platform stair lifts, for renovation only"),
 ("kevythissien", "element", "OH18", "2.8.1 (p. 24)", "Näiden kevythissien lisäksi", "light lifts"),
 ("helposti havaittava", "performance quality", "E17", "2 § mom. 2", "Edellä 1 momentissa tarkoitetun luiskan on oltava helposti havaittava, suora", "perceivability is a stated property of routes and ramps"),
 ("suora", "geometry rule", "OH18", "2.2.2 (p. 13)", "Luiskan kaltevien osuuksien tulee olla suoravartiset ja kääntymisen tulee tapahtua vain välitasanteiden kohdalla.", "straight ramp flights, turning only at landings"),
 ("sisätilassa olevaan luiskaan verrattavassa kunnossa", "climate condition", "E17", "2 § mom. 2", "Ulkotilassa luiska saa kuitenkin olla kaltevuudeltaan yli viisi prosenttia vain, jos se voidaan pitää sisätilassa olevaan luiskaan verrattavassa kunnossa.", "winter condition of outdoor ramps"),
 ("katettu tai sulanapidetty", "technique (climate)", "OH18", "2.2.2 (p. 14)", "esimerkiksi kun se on katettu tai sulanapidetty", "covered or kept ice-free (heated)"),
 ("Kattamattomien ja lämmittämättömien ulkoportaiden", "climate condition", "K17", "5 §", "Kattamattomien ja lämmittämättömien ulkoportaiden etenemän on oltava vähintään 390 millimetriä", "stair geometry changes with cover and heating"),
 ("autopaikan", "element", "E17", "2 § mom. 3", "Tällaisen autopaikan on oltava vähintään 3 600 millimetriä leveä", "accessible parking space"),
 ("liikkumisesteisen tunnuksella eli kansainvälisellä pyörätuolitunnuksella", "symbol", "OH18", "2.2.3 (p. 14)", "Autopaikka on merkittävä liikkumisesteisen tunnuksella eli kansainvälisellä pyörätuolitunnuksella.", ""),
 ("sukupuolesta riippumatta", "provision rule", "E17", "11 § mom. 2", "käyttää liikkumis- tai toimimisesteisen henkilön ja hänen avustajansa sukupuolesta riippumatta", "location independent of the sex of user and assistant"),
 ("avustaja", "user", "E17", "13 §", "sovelluttava liikkumis- ja toimimisesteiselle henkilölle sekä hänen avustajalleen", "the assistant is a design user"),
 ("turvahälytysyhteys valvontaan", "element", "E17", "10 § mom. 3", "Jos rakennuksessa on valvontajärjestelmä, wc-tilasta on oltava turvahälytysyhteys valvontaan.", "emergency alarm link to a monitored system"),
 ("ääni- ja valomerkki", "technique", "OH18", "2.10.5 (p. 30)", "kuuluva ja näkyvä ääni- ja valomerkki", "audible and visual alarm signal"),
 ("vapaata tilaa vähintään 800 millimetriä", "space", "E17", "10 § mom. 2", "Lisäksi wc-istuimen kummallakin puolella on oltava vapaata tilaa vähintään 800 millimetriä.", "transfer space each side of the WC"),
 ("kätisyys", "concept", "OH18", "2.10.2 (p. 28)", "Wc-tilojen kätisyys eli kummalla puolella wc-istuinta on pyörätuolille tarkoitettu vapaa tila", "handedness of a WC (side of transfer)"),
 ("sivuttaisen siirtymisen", "technique (transfer)", "OH18", "2.10.4 (p. 28)", "wc-istuimen viereen sivuttaisen siirtymisen mahdollistamiseksi", "side transfer"),
 ("varustettavissa", "defined state (adaptability)", "E17", "9 § mom. 1", "Tällaisen wc- ja pesutilan on oltava varustettavissa liikkumisesteiselle henkilölle sopivaksi.", "equippable later, distinguished from 'varustettava' (to be equipped)"),
 ("tukikaiteiden kiinnittämisen", "technique", "OH18", "2.9.1 (p. 26)", "kun seinän rakenne mahdollistaa tukikaiteiden kiinnittämisen", "walls built to take grab bars later"),
 ("wc-istuimen käsituet", "element", "OH18", "2.10.5 (p. 29)", "Liikkumisesteisen henkilön tarvitsemia varusteita ovat mm. wc-istuimen käsituet sekä tukikaiteet.", "WC armrests, distinct from grab bars"),
 ("Kiinteillä kalusteilla", "defined term", "OH18", "2.9.1 (p. 25)", "Kiinteillä kalusteilla tarkoitetaan kalusteita, joiden kiinnitys", "fixed fixtures defined by penetration of the waterproofing"),
 ("selviytymiskerroksena", "defined term (dwelling)", "OH18", "2.2.1 (p. 12)", "sisääntulokerros toimii ns. selviytymiskerroksena", "entry-storey 'coping floor' with WC, kitchen-living and sleeping"),
 ("Hissivaraus", "technique (future provision)", "OH18", "2.7.1 (p. 22)", "on suositeltavaa tehdä siihen suunnitteluvaiheessa hissivaraus", "reserved lift shaft"),
 ("Jälkiasennushissi", "element", "OH18", "2.7.3 (p. 23)", "2.7.3 Jälkiasennushissi asuinrakennuksessa", "retrofitted lift with permitted smaller car"),
 ("sisääntulon kerrostaso mukaan lukien kolmannessa", "trigger rule", "E17", "7 § mom. 1", "on sisääntulon kerrostaso mukaan lukien kolmannessa tai sitä ylemmässä kerroksessa", "lift required from the third storey counting the entry storey"),
 ("leveä ovisivultaan", "quantity", "E17", "7 § mom. 3", "vähintään 1 100 millimetriä leveä ovisivultaan", "lift car width measured on the door side"),
 ("kerroskorkeus", "quantity (threshold)", "E17", "8 §", "Jos tasoero on yhtä suuri kuin kerroskorkeus tai sitä suurempi", "storey height as the ramp/lift threshold"),
 ("palveluasumiseen tai liikkumis- tai toimimisesteisen henkilön tuettuun asumiseen", "building/dwelling category", "E17", "6 § mom. 3", "Asunnossa, joka on tarkoitettu palveluasumiseen tai liikkumis- tai toimimisesteisen henkilön tuettuun asumiseen", "service and supported housing gets larger turning and WC space"),
 ("apuvälineiden käyttö ja avustaminen", "design aim", "E17", "6 § mom. 3", "että apuvälineiden käyttö ja avustaminen on mahdollista", "use of aids and assisting"),
 ("opintotukeen oikeuttavaan koulutukseen", "exemption category", "E17", "9 § mom. 3", "mukaiseen opintotukeen oikeuttavaan koulutukseen osallistuville henkilöille tai ainoastaan 18–29-vuotiaille", "student and youth housing exemption"),
 ("kaupunkipientaloa", "building category", "E17", "2 § mom. 1", "ei koske omakotitaloa, paritaloa eikä kaupunkipientaloa", "detached, semi-detached and urban small houses exempted where impossible"),
 ("Pientalon", "building category", "E17", "1 § mom. 1", "Pientalon rakentamiseen sovelletaan kuitenkin ainoastaan 2–4 §:ää", "small houses get only §§ 2-4"),
 ("asumista palveleviin välttämättömiin tiloihin", "defined space class", "E17", "4 § mom. 2", "asumista palveleviin välttämättömiin tiloihin ja rakennuksen käyttöä palveleviin tiloihin", "essential dwelling spaces / spaces serving the building"),
 ("esteettömyyden parantaminen", "compliance route (renovation)", "E17", "1 § mom. 2", "siltä osin kuin esteettömyyden parantaminen on rakennuksen ominaisuudet sekä toimenpiteen laatu ja laajuus huomioon ottaen tarkoituksenmukaista", "proportionality test for renovation and change of use"),
 ("Tarkoituksenmukaisuusarviointiin", "compliance route", "OH18", "2.1.1 (p. 10)", "Tarkoituksenmukaisuusarviointiin vaikuttavia rakennuksen", "expediency assessment"),
 ("kunnan rakennusvalvontaviranomainen", "decision authority", "OH18", "2.1.1 (p. 9)", "ratkaisee rakentamisen ohjauksesta ja valvonnasta vastaava kunnan rakennusvalvontaviranomainen", "the municipal building control decides application"),
 ("äänensiirtojärjestelmä", "element", "E17", "12 § mom. 1", "induktiosilmukka tai muu vastaava äänensiirtojärjestelmä", "assistive listening system as a class"),
 ("yleisön palvelutilassa", "space category", "E17", "12 § mom. 1", "tai muussa vastaavassa kokoontumistilassa tai yleisön palvelutilassa", "public service space (counters, waiting rooms)"),
 ("esteettömien sisääntuloväylien", "element", "E17", "12 § mom. 2", "esteettömien sisääntuloväylien on johdettava useammalle kuin yhdelle istuinriville", "choice of seat row"),
 ("paikanvalinnan mahdollisuuden", "design aim", "OH18", "2.12.3 (p. 32)", "paikanvalinnan mahdollisuuden turvaamiseksi", "choice of place"),
 ("koho- ja pistekirjoituksella", "technique", "OH18", "2.12.4 (p. 33)", "Majoitushuoneen numero suositellaan merkittäväksi koho- ja pistekirjoituksella.", "raised characters and braille"),
 ("uima-altaaseen", "element", "E17", "11 § mom. 3", "Liikkumisesteisen henkilön pääsy uima-altaaseen", "pool access by an independently usable hoist"),
 ("suihkupyörätuolilla", "device", "OH18", "2.11.2 (p. 31)", "itsenäisesti suihkupyörätuolilla", "shower wheelchair"),
 ("sauna-, pesu- ja pukuhuonetilan", "room", "E17", "9 § mom. 4", "asukkaiden yhteisen sauna-, pesu- ja pukuhuonetilan on sovelluttava", "shared sauna suite in housing"),
 ("äänimajakat", "element", "OH18", "2.5.1 (p. 19)", "kuten esimerkiksi äänimajakat", "audio beacons for blind people"),
 ("koholistalla", "element", "OH18", "2.5.1 (p. 19)", "lattian pintaan kiinnitetyllä yhtenäisellä koholistalla", "continuous raised guide strip"),
 ("kohomerkinnät", "element", "OH18", "2.4.2 (p. 18)", "suunnistautumista ohjaavat kohomerkinnät kulkuväylän pinnassa", "raised guidance markings leading to a revolving-door alternative"),
 ("Pyöröoven", "element", "OH18", "2.4.2 (p. 18)", "Pyöröoven lisäksi suositellaan asennettavaksi myös esteetön vaihtoehto", "revolving door needs an accessible alternative"),
 ("Sivuun liukuva ovi", "element", "OH18", "2.4.2 (p. 18)", "Sivuun liukuva ovi on turvallinen ratkaisu", "sliding door preferred over swing-toward automatic doors"),
 ("merkkivalo", "element", "OH18", "2.4.2 (p. 17)", "äänimerkin lisäksi tarvitaan merkkivalo, joka ilmaisee lukon avautumisen", "visual signal for remote door release"),
 ("puheopastus", "element", "OH18", "2.8.2 (p. 24)", "kerrokselle saapumisesta ilmoittava äänimerkki, puheopastus ja induktiosilmukka", "lift voice announcement"),
 ("Hissikorin takaseinälle sijoitettu peili", "element", "OH18", "2.8.2 (p. 24)", "Hissikorin takaseinälle sijoitettu peili", "mirror for reversing out"),
 ("kynnyksen särmät on viistetty", "technique", "OH18", "2.4.3 (p. 18)", "kun kynnyksen särmät on viistetty", "chamfered threshold edges"),
 ("asuntokohtaisen ulkotilan", "space", "E17", "4 § mom. 3", "Tasoero asuntokohtaisen ulkotilan oven yhteydessä oven ulkopuolella saa olla yli 20 millimetriä", "balcony/terrace exception, if removable by fitting out"),
 ("suojakaide tai avokaide", "element (two types)", "K17", "7 § mom. 1", "Kaide voi olla suojakaide tai avokaide.", "protective (child-safe) vs open guard"),
 ("putoamiskorkeus", "quantity", "K17", "7 § mom. 1", "kun putoamiskorkeus ylittää puoli metriä", "fall height triggering a guard"),
 ("harhaan astumisen", "hazard", "K17", "2 Luku (heading)", "Putoamisen ja harhaan astumisen estäminen", "mis-stepping, paired with falling"),
 ("kuutio", "test method", "K17", "8 § mom. 2", "sen aukoista saa mahtua läpi särmältään enintään 100 millimetrin mittainen kuutio", "gap sizes tested with a cube"),
 ("syöksy", "element (stair/ramp flight)", "K17", "9 § mom. 1", "sen on jatkuttava syöksyn alkamis- ja loppumiskohdan ohi", "the flight; handrail extension past its start and end"),
 ("lasiseinät ja lasiovet", "element", "K17", "11 § mom. 3", "Ikkunat, lasiseinät ja lasiovet, joihin on vaara törmätä, on merkittävä siten, että ne havaitaan helposti.", "glazing marking"),
 ("häikäisyä", "hazard", "K17", "10 § mom. 1", "Valaistus ei saa aiheuttaa turvallisuutta vaarantavaa häikäisyä.", "glare"),
 ("seisomarivin syvyyden", "quantity", "K17", "23 § mom. 2", "Katsomon seisomarivin syvyyden on oltava vähintään puoli metriä.", "standing terrace row depth"),
 ("Istuinrivin kulkuvälin vapaa leveys", "quantity (table)", "K17", "24 §, taulukko 1", "Istuinrivin kulkuvälin vapaa leveys suhteessa paikkalukuun", "seatway clear width by seats per row"),
 ("ajoväylä", "element", "K17", "16 § mom. 1", "Tontin ja rakennuspaikan ajoväylä ja pysäköintialue on erotettava jalankulku-, leikki-, ja oleskelualueesta.", "separation of vehicle routes from pedestrian areas"),
 ("Kaikille sopiva suunnittelua", "doctrine term", "OH18", "Esipuhe (p. 2)", "Sopimus korostaa kaikille sopiva suunnittelua (Design for All tai", "Design for All, cited to the CRPD"),
]

def check(q, ph, ins):
    return norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()

def main():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = check(q, ph, ins)
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, file=sys.stderr)
            w.writerow([ph, kind, 'fi', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    rows = []
    for c, ph, ins, loc, q, note in OBS:
        ok = check(q, ph, ins)
        if not ok: bad += 1; print('FAIL', ins, loc, ph, norm(q) in TXT[ins], file=sys.stderr)
        rows.append([c, ph, 'fi', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    unknown = {c for r in rows for c in r[0].split('|')} - set(REGISTER)
    if unknown: bad += 1; print('UNKNOWN CONCEPT', unknown, file=sys.stderr)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else ('base_parameters' if i < 60 else 'b651-headings (RHFAC-does-not-name)'))
            hit = [r for r in rows if c in r[0].split('|') or (c in ALIAS and ALIAS[c] in r[0].split('|'))]
            if hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                if c not in ABSENT: bad += 1; print('NO ABSENT NOTE', c, file=sys.stderr)
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE: check')])
    print('observations', len(rows), 'reverse-harvest', len(REV), 'failures', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
