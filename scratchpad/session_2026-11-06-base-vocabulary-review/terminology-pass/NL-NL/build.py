"""Build observations / coverage / reverse-harvest TSVs for the NL/NL terminology pass, verifying every
quote (after whitespace collapse) in the saved extracted text. Adapted from FR-FR/build.py. Run from the
repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NL-NL/build.py
Exits 1 if any quote or phrase fails to verify. Writes only the three TSVs in this folder.
Text files were produced by tools/x2t.py (BWB XML) and tools/h2t.py (HTML) from the persisted artefacts."""
import re, sys, csv

D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NL-NL'
INST = {
 'BBL': ("Besluit bouwwerken leefomgeving (Besluit van 3 juli 2018, Stb. 2018, 291), geconsolideerde tekst geldend vanaf 2026-09-24", D + '/text/52ef1dbbf8d109ba.txt'),
 'BB12': ("Bouwbesluit 2012 (BWBR0030461), laatste geconsolideerde tekst 2023-09-07 t/m 2023-12-31 (vervallen)", D + '/text/56c4f96582c47206.txt'),
 'BZK': ("volkshuisvestingnederland.nl, 'Toegankelijk bouwen' (ministry web page; guidance, not an instrument)", D + '/text/8be21dedbca82962.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note ours)
OBS = [
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)", "verlichtingsinstallatie", "BBL", "art. 4.193 lid 1", "Een bouwwerk heeft een zodanige verlichtingsinstallatie dat het bouwwerk veilig kan worden gebruikt en verlaten.", "aim is safe use and escape, not visual access"),
 ("lighting levels|Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)", "verlichtingssterkte", "BBL", "art. 4.194 lid 1", "Een verblijfsruimte heeft een verlichtingsinstallatie die een op een vloer, een tredevlak of een hellingbaan gemeten verlichtingssterkte kan geven", "illuminance measured on floor, tread or ramp"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "verhard pad", "BBL", "art. 4.192 lid 1", "grenst aan een route naar de openbare weg die over een verhard pad of steiger voert met:", "paved path only; no firmness or slip-resistance term"),
 ("Seating", "zitplaatsen", "BBL", "art. 6.22 lid 2", "In een ruimte met meer dan 100 zitplaatsen zijn de zitplaatsen gekoppeld of aan de vloer bevestigd", "assembly seating for crowd and fire safety, not rest seating"),
 ("Handrails", "leuning", "BBL", "art. 4.28 lid 1", "heeft aan ten minste een zijkant een leuning", "stairs only; ramps carry a geleiderand, not a leuning"),
 ("Handrails", "horizontaal doorloopt", "BBL", "art. 4.28 lid 2", "Een trap als bedoeld in het eerste lid heeft aan beide zijkanten een leuning die aan het begin en aan het einde van de trap ten minste 30 cm horizontaal doorloopt.", "handrail extension"),
 ("Clear width|width|Corridor width (parameter 4)|Door width (parameter 9)", "vrije breedte", "BBL", "Bijlage I, divisie A", "vrije breedte: kleinste afstand tussen constructieonderdelen aan weerskanten van een doorgang;", "defined term; measured between construction parts at a doorgang"),
 ("Door width (parameter 9)|Clear width", "doorgang", "BBL", "art. 4.180 lid 1", "Een doorgang heeft een vrije breedte van ten minste 0,85 m", "the regulated object is the doorgang (opening), not the deur"),
 ("Corridor width (parameter 4)|Accessible path of travel", "gemeenschappelijke verkeersruimte", "BBL", "art. 4.181 lid 2", "Als de in het eerste lid bedoelde ruimte een gemeenschappelijke verkeersruimte is, is de vrije breedte ten minste 1,2 m.", "corridor is a shared circulation space; 'gang' does not occur"),
 ("Accessible path of travel", "verkeersroute", "BBL", "Bijlage I, divisie A", "verkeersroute: route die begint bij een doorgang van een ruimte, alleen voert over vloeren, trappen of hellingbanen en eindigt bij de doorgang van een andere ruimte;", "defined term"),
 ("Accessible path of travel", "route naar de openbare weg", "BBL", "art. 4.192 lid 2", "Een hoofdtoegang van een woongebouw zonder toegankelijkheidssector grenst aan de openbare weg of grenst aan een route naar de openbare weg die over een verhard pad voert met:", "exterior route from public road"),
 ("Shelter", "regenwerend", "BBL", "art. 4.29", "Een gemeenschappelijke verkeersruimte met een trap voor het overbruggen van een hoogteverschil van meer dan 1,5 m is ter plaatse van die trap, bepaald volgens NEN 2778, regenwerend.", "rain-proof stair in shared circulation; no canopy at entrances"),
 ("Clear signage", "vluchtrouteaanduiding", "BBL", "art. 4.215 lid 1", "Een ruimte waardoor een verkeersroute voert en een ruimte voor meer dan 50 personen hebben een vluchtrouteaanduiding die voldoet aan NEN 3011", "escape-route signs only"),
 ("Clear signage", "objecten voor bewegwijzering", "BBL", "art. 6.15a lid 3", "objecten voor bewegwijzering en informatie aan de bewoners;", "wayfinding objects named only as exempt from a fire-load rule"),
 ("Audio accessibility and communication enhancement technologies", "spreekinstallatie", "BBL", "art. 4.239 lid 2", "heeft een spreekinstallatie die vanuit ten minste een niet-gemeenschappelijke ruimte van een op die toegang aangewezen woonfunctie kan worden bediend", "entry intercom, in a crime-prevention paragraph; no assistive listening"),
 ("Level landings with clear space", "hellingbaanbordes", "BBL", "art. 4.31 (heading and text)", "Artikel 4.31 (hellingbaanbordes) Een hellingbaan als bedoeld in de artikelen 4.25, 4.172, 4.182, 4.189 en 4.192 sluit aan de bovenzijde, over de breedte van de hellingbaan, aan op een vloer met een oppervlakte van ten minste 1,4 m x 1,4 m", "top landing only"),
 ("Level landings with clear space", "trapbordes", "BBL", "art. 4.27 (heading)", "Artikel 4.27 (trapbordes)", ""),
 ("Level landings with clear space and at regular intervals|Ramp run length (parameter 12)", "een hoogte van niet meer dan 1 m", "BBL", "art. 4.30", "Een hellingbaan als bedoeld in de artikelen 4.25, 4.172, 4.182, 4.189 en 4.192 heeft een breedte van ten minste 1,1 m, een hoogte van niet meer dan 1 m", "a ramp is capped by its rise; no intermediate landing and no run length are named"),
 ("Clear space for approach|Turning circle (parameter 5)", "vloeroppervlakte van ten minste 1,5 m x 1,5 m", "BBL", "art. 4.181 lid 4", "Aan een doorgang van een liftschacht grenst een ruimte met een vloeroppervlakte van ten minste 1,5 m x 1,5 m.", "space stated as a floor area in front of the lift"),
 ("Turning circle (parameter 5)", "zonder te keren", "BBL", "art. 4.181 lid 5", "Dit geldt niet als een rolstoelgebruiker vanuit die verkeersruimte zonder te keren het aansluitende terrein kan bereiken.", "turning named as an act of the wheelchair user, not as a circle"),
 ("Riser height and tread depth|riser", "optrede", "BBL", "tabel 4.26", "Maximum hoogte van een optrede", ""),
 ("Riser height and tread depth|tread|depth", "aantrede", "BBL", "tabel 4.26", "Minimum aantrede ter plaatse van de klimlijn, gemeten loodrecht op de voorkant van de trede", "going measured on the klimlijn"),
 ("tread|Riser height and tread depth", "tredevlak", "BBL", "tabel 4.26", "Minimum breedte van het tredevlak ter plaatse van de klimlijn, gemeten loodrecht op de voorkant van dat vlak", "tread surface is a 'breedte', like French 'largeur du giron'"),
 ("Nosing design|Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip|LRV contrast (parameter 8)", "markering van ten minste 50 mm met een hoog contrast", "BBL", "art. 4.26a", "Een trap als bedoeld in artikel 4.25, is op de bovenste en onderste trederand over de volle breedte voorzien van een markering van ten minste 50 mm met een hoog contrast.", "contrast unquantified; no slip resistance; no nosing profile"),
 ("Level threshold|level", "hoogteverschil groter dan 0,02 m", "BBL", "art. 4.182 lid 1", "is een hoogteverschil groter dan 0,02 m, gemeten vanaf de vloer met aankleding, overbrugd door een hellingbaan", "the threshold is a hoogteverschil; 'drempel' occurs 0 times in the Bbl"),
 ("Level threshold", "drempel", "BZK", "section 'Minimumeisen in het Besluit bouwwerken leefomgeving (Bbl)'", "Een voorbeeld hiervan is dat de drempel naar een tuin of balkon van nieuwbouwwoningen niet hoger mag zijn dan twee centimeter.", "the ministry's plain-language word for what the Bbl calls a hoogteverschil; guidance, not instrument"),
 ("Height clearance (if sheltered or parkade)|Headroom clearance (parameter 11)|Headroom and protruding objects|Headroom|clearance", "vrije hoogte", "BBL", "art. 4.188 lid 3", "Een verkeersroute in een toegankelijkheidssector loopt door een ruimte met een vrije breedte van ten minste 1,2 m en een vrije hoogte van ten minste 2,1 m.", "defined by pointer to NEN 2580"),
 ("Headroom clearance (parameter 11)|Headroom", "Minimum vrije hoogte boven de trap", "BBL", "tabel 4.26", "Minimum vrije hoogte boven de trap", ""),
 ("clearance", "vrije doorgang", "BBL", "art. 4.179, tabel 4.179 column heading", "vrije doorgang: verkeersroute", "clearance is a free passage"),
 ("Edge protection", "afscheiding", "BBL", "art. 4.20 lid 1", "Een voor personen bestemde vloer heeft bij een rand een niet-beweegbare afscheiding als die rand meer dan 1 m hoger ligt dan een aansluitende vloer", "fall barrier"),
 ("Edge protection", "geleiderand", "BBL", "art. 4.32", "Een hellingbaan als bedoeld in artikel 4.25 heeft aan de zijkant een aaneengesloten geleiderand", "ramp edge kerb; also in Bouwbesluit 2012 art. 2.45"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "helling", "BBL", "art. 4.30", "een hoogte van niet meer dan 1 m en een helling van ten hoogste:", "graded by rise"),
 ("Slope|slope|Ramp gradient (parameter 3)", "hellingbaan", "BBL", "art. 4.182 lid 1", "overbrugd door een hellingbaan", "'hellingbaan' is not defined in Bijlage I"),
 ("Accessible door hardware|force|Operating force (parameter 6)", "lichte druk tegen de deur", "BBL", "art. 4.217 lid 1", "door een lichte druk tegen de deur; of", "escape-route doors; force is qualitative, no newtons"),
 ("Accessible door hardware", "ontsluitingsmechanisme", "BBL", "art. 4.217 lid 1", "met behulp van een ontsluitingsmechanisme dat voldoet aan NEN-EN 179 of NEN-EN 1125.", "escape hardware"),
 ("Accessible door hardware", "panieksluiting", "BBL", "art. 4.217 lid 2", "een lichte druk tegen een op circa 1 m boven de vloer over de volle breedte van de deur aangebrachte panieksluiting", ""),
 ("height", "hoogte", "BBL", "art. 4.21 lid 1", "Een vloerafscheiding als bedoeld in artikel 4.20, eerste lid, heeft een hoogte van ten minste 1 m, gemeten vanaf de vloer.", ""),
 ("level", "meetniveau", "BBL", "Bijlage I, divisie A", "meetniveau: hoogte van het aansluitende terrein, gemeten ter plaatse van de toegang van het gebouw;", "datum level; 'niveau' otherwise means quality level ('rechtens verkregen niveau')"),
 ("number|ratio", "aantal integraal toegankelijke badruimten", "BBL", "art. 4.186 lid 6", "Een gebruiksfunctie met een toegankelijkheidssector heeft een aantal integraal toegankelijke badruimten van ten minste de getalswaarde van het aantal aanwezige badruimten gedeeld door 20", "count as proportion"),
 ("ratio", "percentage van de vloeroppervlakte", "BBL", "art. 4.185 lid 1", "ligt ten minste het in tabel 4.183 aangegeven percentage van de vloeroppervlakte aan verblijfsgebied van de gebruiksfunctie in een toegankelijkheidssector", "share of floor area that must be accessible"),
 ("time", "binnen 15 seconden", "BBL", "art. 4.195 lid 5", "Noodverlichting als bedoeld in het eerste tot en met vierde lid geeft binnen 15 seconden na het uitvallen van de voorziening voor elektriciteit", "emergency lighting response time"),
 ("size", "afmetingen", "BBL", "art. 4.190 (heading)", "Artikel 4.190 (lift: afmetingen en loopafstand)", ""),
 ("volume", "inhoud", "BBL", "art. 4.111", "die niet kleiner is dan 1/8 van de getalswaarde van de inhoud van die ruimte", "spatial volume, not audio volume"),
 ("capacity", "capaciteit", "BBL", "§ 4.2.11 (heading)", "Vluchtroutes: inrichting en capaciteit", "escape-route capacity in persons, not lift capacity"),
 ("distance", "loopafstand", "BBL", "art. 4.190 lid 3", "De loopafstand tussen de toegang van een woonfunctie en de toegang van ten minste een lift als bedoeld in artikel 4.189 is ten hoogste 90 m.", "walking distance to a lift; defined in Bijlage I"),
 ("Reverberation time (parameter 7)", "galm", "BBL", "art. 4.110 lid 1", "Een woongebouw heeft in een gemeenschappelijke verkeersruimte een geluidsabsorptie, waarmee geluidhinder door galm wordt beperkt.", "aim stated as nuisance from reverberation"),
 ("Reverberation time (parameter 7)", "totale geluidsabsorptie", "BBL", "art. 4.111", "heeft een volgens NEN-EN 12354-6 bepaalde totale geluidsabsorptie", "quantity is absorption area per room volume, not reverberation time"),
 ("Protruding objects|Headroom and protruding objects", "beweegbaar constructieonderdeel", "BBL", "art. 4.35 lid 2", "Een beweegbaar constructieonderdeel dat zich in geopende stand kan bevinden boven een niet voor motorvoertuigen openstaande weg, ligt, gemeten vanaf de onderzijde van dat onderdeel, meer dan 2,2 m boven die weg.", "only moving parts over a public way"),
 ("Clear space for approach", "integraal toegankelijke toiletruimte", "BBL", "art. 4.187 lid 2", "Een integraal toegankelijke toiletruimte heeft een vloeroppervlakte van ten minste 1,65 m x 2,2 m.", "room size, no transfer or approach space named"),
 # Bouwbesluit 2012, for carve comparison only (repealed)
 ("Level threshold|level", "afgewerkte vloer", "BB12", "art. 4.27 lid 1", "is een hoogteverschil groter dan 0,02 m, gemeten vanaf de afgewerkte vloer, overbrugd door een lift of een hellingbaan", "the Bbl replaced this with 'vloer met aankleding'"),
 ("Colour-contrasted and slip-resistant strip on nosing|LRV contrast (parameter 8)", "hoog contrast", "BB12", "art. 2.33a", "voorzien van een markering van ten minste 50 mm met een hoog contrast", "same phrase as Bbl art. 4.26a"),
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
PARTIAL = {  # concept -> why the Dutch match is not the English concept (ours, a judgment)
 "Surface is firm, stable and slip resistant": "NARROWER: 'verhard pad' (paved) only; no firm/stable/slip term",
 "Surface is stable, firm, and slip resistant": "NARROWER: 'verhard pad' (paved) only; no firm/stable/slip term",
 "Seating": "DIFFERENT SENSE: assembly seating for crowd safety",
 "Shelter": "NARROWER: rain-proofing of a stair in shared circulation",
 "Clear signage": "NARROWER: escape-route signs; wayfinding objects named only in a fire rule",
 "Audio accessibility and communication enhancement technologies": "DIFFERENT SENSE: entry intercom only",
 "Level landings with clear space and at regular intervals": "NARROWER: top landing only; no intermediate landing",
 "Clear space for approach": "PARTIAL: floor areas of rooms and lift lobbies; no approach-side space",
 "Nosing design": "NARROWER: edge marking only",
 "Colour-contrasted and slip-resistant strip on nosing": "NARROWER: contrast marking, no slip resistance",
 "Colour-contrasted and slip-resistant strip": "NARROWER: contrast marking, no slip resistance",
 "Accessible door hardware": "DIFFERENT SENSE: escape-route opening hardware",
 "depth": "PARTIAL: only as 'aantrede'; the word 'diepte' carries no design quantity",
 "force": "PARTIAL: qualitative 'lichte druk', no newtons",
 "time": "DIFFERENT SENSE: emergency-lighting response time",
 "volume": "DIFFERENT SENSE: spatial volume",
 "capacity": "DIFFERENT SENSE: escape-route capacity",
 "distance": "DIFFERENT SENSE: walking distance to a lift",
 "ratio": "PARTIAL: share of floor area and of bathrooms",
 "Turning circle (parameter 5)": "DIFFERENT CARVE: square floor area plus 'zonder te keren'",
 "Operating force (parameter 6)": "PARTIAL: qualitative, escape doors only",
 "Reverberation time (parameter 7)": "DIFFERENT QUANTITY: absorption area, not reverberation time",
 "LRV contrast (parameter 8)": "BROADER: 'hoog contrast' never quantified",
 "Ramp run length (parameter 12)": "DIFFERENT CARVE: ramp capped by rise (1 m), not by length",
 "Protruding objects": "NARROWER: moving parts above a public way",
 "Headroom and protruding objects": "headroom FOUND; protruding objects only for moving parts",
}
ABSENT = {
 "Drainage": "'afwatering' 0; 'hemelwater' only as drainage plumbing (art. 4.204 ff.), not walking-surface drainage",
 "Floor surface is stable, firm, and non-slip": "'stroef' 0, 'slip' 0; no indoor floor-surface rule",
 "No open riser": "'stootbord' 0, 'open trede' 0",
 "Tactile attention indicators (truncated domes)": "'tactiel' 0, 'noppen' 0, 'ribbel' 0; held aliases 'geleidestrook' and 'noppen- en ribbeltegels' not in text",
 "Sink faucet is easy to use or automatic": "'kraan' occurs only as a noise source (art. 4.107 and 4.108); 'wastafel' 0",
 "Outlets and switches are at accessible heights": "'wandcontactdoos' only in road-tunnel hulpposten; 'schakelaar' 0",
 "Microwave mounting height accessible and safe": "'magnetron' 0; nearest is 'opstelplaats voor een kooktoestel' (reverse harvest)",
 "Accessible lockers": "'kluis' only as 'sleutelkluis' in the gebruiksmelding data list (art. 6.8)",
 "Accessible controls": "no reach or operability rule; 'bediend' only for intercom location (art. 4.239)",
 "Colour temperature (parameter 10)": "'kleurtemperatuur' 0; 'kleur' only for tunnel doors (RAL 6024) and building appearance",
 "Gratings": "'rooster' 0",
 "Spouts": "no fittings rule",
 "Lavatories": "'wastafel' 0; 'toiletruimte' is the room, not the basin",
 "Enclosures": "no enclosure term; 'badruimte' is the room",
 "Speed bumps": "'verkeersdrempel' 0",
 "Bollards": "'paal' as a word 0; 'palen' only as 'seinpalen' in permit lists",
 "Landscaping elements": "no landscaping term", "Flower or shrub planters": "no planter term",
 "Vegetation": "'beplanting' 0", "Guy wires": "no term",
 "Scaffolding": "'steiger' occurs in permit lists (construction scaffold) and as a jetty for floating buildings (art. 4.192), never as an obstacle on a pedestrian route",
 "Gradation limits": "no term",
}

# Reverse harvest: (phrase verbatim, kind ours, instrument, locator, quote verbatim, gloss OURS)
REV = [
 ("toegankelijkheidssector", "defined category (space)", "BBL", "Bijlage I, divisie A", "toegankelijkheidssector: voor personen met een functiebeperking zelfstandig bruikbaar en toegankelijk gedeelte van een gebouw;", "the accessible sector: the part of a building that must be independently usable; its presence is triggered by floor area and height"),
 ("zelfstandig bruikbaar en toegankelijk", "criterion", "BBL", "Bijlage I, divisie A", "voor personen met een functiebeperking zelfstandig bruikbaar en toegankelijk gedeelte van een gebouw", "independent use is in the definition"),
 ("personen met een functiebeperking", "population carve", "BBL", "art. 4.183 lid 1", "Een bouwwerk heeft ruimten die voldoende toegankelijk zijn voor personen met een functiebeperking.", "the only population term in the accessibility rules; one umbrella, no impairment list"),
 ("rolstoelgebruiker", "population (named once)", "BBL", "art. 4.181 lid 5", "Dit geldt niet als een rolstoelgebruiker vanuit die verkeersruimte zonder te keren het aansluitende terrein kan bereiken.", "the single named user"),
 ("integraal toegankelijke toiletruimte", "defined space", "BBL", "art. 4.186 lid 3", "In een toegankelijkheidssector ligt een integraal toegankelijke toiletruimte.", "wholly accessible WC; not defined in Bijlage I"),
 ("integraal toegankelijke badruimte", "defined space", "BBL", "art. 4.187 lid 3", "Een integraal toegankelijke badruimte heeft een vloeroppervlakte van ten minste 1,6 m x 1,8 m.", ""),
 ("integraal toegankelijke badruimte die is samengevoegd met een toiletruimte", "space", "BBL", "art. 4.187 lid 4", "Een integraal toegankelijke badruimte die is samengevoegd met een toiletruimte heeft een vloeroppervlakte van ten minste 2,2 m x 2,2 m.", "combined room as its own case"),
 ("gebruiksfunctie", "legal category (use class)", "BBL", "Bijlage I, divisie A", "gebruiksfunctie: gedeelten van een of meer bouwwerken die dezelfde gebruiksbestemming hebben en die samen een gebruikseenheid vormen;", "every rule is applied per use function through a table"),
 ("woonfunctie voor zorg", "use class", "BBL", "Bijlage I, divisie B", "woonfunctie voor zorg: woonfunctie waarbij aan de bewoners professionele zorg wordt verleend met een vanuit het zorgaanbod georganiseerde koppeling tussen wonen en zorg;", "care housing has its own accessibility trigger (>500 m2)"),
 ("woonfunctie voor particulier eigendom", "use class (exemption)", "BBL", "art. 4.9", "Op het bouwen van een woonfunctie voor particulier eigendom zijn afdeling 4.6 en de paragrafen 4.5.4, 4.5.5 en 4.5.6 niet van toepassing.", "owner-built or owner-occupied dwellings are exempt from the whole accessibility division"),
 ("aansturingsartikel", "drafting device", "BBL", "art. 4.183 (heading)", "Artikel 4.183 (aansturingsartikel)", "each paragraph opens with a functional aim; compliance with the tabled rules is deemed to meet it"),
 ("voldoende toegankelijk", "functional aim", "BBL", "art. 4.191 lid 1", "Een bouwwerk is vanaf de openbare weg voldoende toegankelijk voor personen met een functiebeperking.", ""),
 ("voldoende bereikbaar", "functional aim", "BBL", "art. 4.179 lid 1", "Een bouwwerk heeft ruimten die voldoende bereikbaar zijn.", "reachability is a separate aim from accessibility"),
 ("gelijkwaardige maatregel", "compliance route", "BBL", "art. 2.5", "Een gelijkwaardige maatregel die betrekking heeft op een in de hoofdstukken 3 tot en met 6 gestelde regel wordt bij het gebruik van het bouwwerk in stand gehouden.", "equivalent-measure route"),
 ("maatwerkvoorschrift", "compliance route", "BBL", "art. 4.5 lid 2", "Met een maatwerkvoorschrift of vergunningvoorschrift kan worden afgeweken van de in het eerste lid bedoelde afdelingen, waarbij afwijken alleen versoepelen kan inhouden.", "a local tailored rule may only relax"),
 ("rechtens verkregen niveau", "compliance level (alterations)", "BBL", "art. 5.4 lid 1", "waarbij in plaats van het in die regels bedoelde niveau van eisen wordt uitgegaan van het in artikel 5.5 bedoelde rechtens verkregen niveau", "alterations keep the lawfully acquired level, not the new-build level"),
 ("hoofdtoegang", "defined element", "BBL", "Bijlage I, divisie A", "hoofdtoegang: toegang van een gebouw of een gebruiksfunctie die is bedoeld om door een ieder te worden gebruikt om het gebouw of de gebruiksfunctie binnen te gaan;", "'door een ieder': the main entrance is defined by universal use"),
 ("aansluitend terrein", "defined place", "BBL", "Bijlage I, divisie A", "aansluitend terrein: aan een bouwwerk grenzend onbebouwd gedeelte van een bouwwerkperceel of openbaar toegankelijk gebied;", ""),
 ("vloer met aankleding", "measurement datum", "BBL", "art. 4.189", "gemeten vanaf de vloer met aankleding, overbrugd door een lift of een hellingbaan", "level differences measured on the finished floor including finishes"),
 ("aankleding", "defined term", "BBL", "Bijlage I, divisie A", "aankleding: op of aan een constructieonderdeel bevestigd materiaal;", ""),
 ("klimlijn", "defined geometry", "BBL", "Bijlage I, divisie A", "klimlijn: denkbeeldige, vloeiend verlopende lijn die de voorkanten van de treden van een trap met elkaar verbindt;", "walking line; stair geometry is stated on it"),
 ("Minimum afstand van de klimlijn tot de zijkanten van de trap", "quantity", "BBL", "tabel 4.26", "Minimum afstand van de klimlijn tot de zijkanten van de trap", ""),
 ("trap uitsluitend voor ontvluchten", "category", "BBL", "tabel 4.26", "trap uitsluitend voor ontvluchten", "escape-only stair has its own dimensions"),
 ("verblijfsgebied", "defined space", "BBL", "Bijlage I, divisie A", "verblijfsgebied: gebruiksgebied of een gedeelte daarvan voor het verblijven van personen;", "rooms are carved by occupancy, not by name"),
 ("verblijfsruimte", "defined space", "BBL", "art. 4.187 lid 1", "In een in artikel 4.186, eerste lid, bedoeld verblijfsgebied is ten minste een verblijfsruimte met een vloeroppervlakte van ten minste 14 m2 bij een breedte van ten minste 3,2 m.", "a larger habitable room is required inside the accessible sector"),
 ("lifttoegang", "element", "BBL", "art. 4.180 lid 2", "Een lifttoegang heeft een vrije breedte van ten minste 0,85 m", ""),
 ("kooi van een lift", "element", "BBL", "art. 4.190 lid 1", "De kooi van een lift als bedoeld in artikel 4.189 heeft een vloeroppervlakte van ten minste 1,05 m x 1,35 m.", "car size, with a stretcher-size case in lid 2"),
 ("opstelplaats voor een lift", "provision for later", "BBL", "art. 4.182 lid 6", "heeft op elke bouwlaag een opstelplaats voor een lift, met een liftkooi met een vloeroppervlakte van ten minste 1,05 m x 2,05 m", "space reserved for a future lift"),
 ("bergruimte om fietsen of scootmobielen", "space", "BBL", "art. 4.171 lid 1", "heeft een afsluitbare bergruimte om fietsen of scootmobielen beschermd tegen weer en wind te kunnen opbergen", "mobility-scooter storage as a dwelling requirement"),
 ("rechtstreeks bereikbare buitenruimte", "space", "BBL", "art. 4.174 lid 1", "heeft een rechtstreeks bereikbare buitenruimte", "private outdoor space, threshold rule applies to it"),
 ("opstelplaats voor een aanrecht", "space", "BBL", "art. 4.178 lid 1", "Een opstelplaats voor een aanrecht als bedoeld in artikel 4.177, eerste lid, heeft een vloeroppervlakte van ten minste 1,5 m x 0,6 m.", "kitchen worktop treated as a floor area"),
 ("overbrugging van hoogteverschillen", "technique", "BBL", "art. 4.182 (heading)", "Artikel 4.182 (overbrugging van hoogteverschillen)", "bridging a level difference by lift or ramp"),
 ("Veilig overbruggen van hoogteverschillen", "technique (safety paragraph)", "BBL", "§ 4.2.4 (heading)", "Veilig overbruggen van hoogteverschillen", "stairs and ramps sit under SAFETY, not under accessibility"),
 ("voorkomen overklauteren", "hazard", "BBL", "art. 4.23 (heading)", "Artikel 4.23 (voorkomen overklauteren)", "anti-climb rule for barriers"),
 ("geen openingen waardoor een bol kan passeren", "test", "BBL", "art. 4.22 lid 1", "heeft geen openingen waardoor een bol kan passeren met een doorsnede groter dan de in tabel 4.19 aangegeven diameter", "sphere test for barrier openings"),
 ("deuren in vluchtroutes: draairichting", "element", "BBL", "art. 4.216 (heading)", "Artikel 4.216 (deuren in vluchtroutes: draairichting)", ""),
 ("automatisch werkende deur", "element", "BBL", "art. 4.217 lid 4", "Een automatisch werkende deur en een voorziening voor toegangs- of uitgangscontrole op een vluchtroute mogen het vluchten niet belemmeren.", "automatic doors appear only under escape"),
 ("noodverlichting", "element", "BBL", "art. 4.195 lid 1", "Een verblijfsruimte voor meer dan 75 personen en een ruimte waardoor een vluchtroute uit die verblijfsruimte voert, hebben noodverlichting.", ""),
 ("redelijke oriëntatie", "criterion", "BBL", "art. 4.197", "Een ruimte bestemd om te worden verduisterd tijdens het gebruik door meer dan 50 personen heeft zodanige voorzieningen dat tijdens de verduistering een redelijke oriëntatie mogelijk is.", "orientation in darkened rooms (cinemas, theatres)"),
 ("ontruimingsalarminstallatie", "element", "BBL", "art. 4.213 lid 1", "Een gebruiksfunctie met een brandmeldinstallatie als bedoeld in artikel 4.208 heeft een ontruimingsalarminstallatie als bedoeld in NEN 2575.", "alarm modality deferred to NEN 2575"),
 ("leefzone", "defined zone", "BBL", "Bijlage I, divisie A", "leefzone: gedeelte van een verblijfsgebied waarbij de ruimte gelegen binnen 1 m van een uitwendige scheidingsconstructie, binnen 0,2 m van een inwendige scheidingsconstructie en hoger gelegen dan 1,8 m boven de vloer buiten beschouwing blijft;", "occupied zone (used for indoor-climate rules)"),
 ("huisvesting in verband met mantelzorg", "defined term", "BBL", "Bijlage I, divisie A", "huisvesting in verband met mantelzorg: huisvesting in of bij een woning van één huishouden van ten hoogste twee personen, van wie ten minste één persoon mantelzorg verleent aan of ontvangt van een bewoner van de woning;", "housing for informal carers or cared-for persons"),
 ("steiger", "element (floating buildings)", "BBL", "art. 4.192 lid 1", "ii. bij een steiger: een hellingbaan als bedoeld in paragraaf 4.2.4.", "a jetty route to a floating building must use a ramp"),
 ("geluidhinder door galm", "hazard", "BBL", "art. 4.110 lid 1", "waarmee geluidhinder door galm wordt beperkt", ""),
 ("VN-gehandicaptenverdrag", "legal basis", "BBL", "considerans", "de verordening bouwproducten en het VN-gehandicaptenverdrag en de artikelen 4.3, eerste lid, en 5.1 van de Omgevingswet", "the decree names the CRPD as one of its legal bases"),
 ("lucht-geluidniveauverschil", "quantity (acoustics)", "BBL", "art. 4.113 lid 1", "Het volgens NEN 5077 bepaalde karakteristieke lucht-geluidniveauverschil voor de geluidsoverdracht", "the only occurrence of 'niveauverschil' in the Bbl is acoustic; the Flemish ramp sense of TERM-090 is 'hoogteverschil' here"),
 ("ervaringsdeskundigen", "co-production actor", "BZK", "section 'NEN 9120: richtlijn voor toegankelijk bouwen'", "Daarom heeft het ministerie van BZK de afgelopen jaren samen met ervaringsdeskundigen en belangengroepen gewerkt aan de NEN 9120.", "experts by experience named as co-authors of the national guideline; guidance page, not an instrument"),
 ("vrijwillige norm", "instrument status", "BZK", "section 'NEN 9120: richtlijn voor toegankelijk bouwen'", "De NEN 9120 is een vrijwillige norm en aanvulling op de minimumeisen van het Bbl.", "NEN 9120 is voluntary, on top of the Bbl minimum"),
]

def write_rev():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, file=sys.stderr)
            w.writerow([ph, kind, 'nl', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    print('reverse-harvest', len(REV), 'verified', len(REV) - bad)
    return bad

def main():
    bad = write_rev(); rows = []
    for c, ph, ins, loc, q, note in OBS:
        for x in c.split('|'):
            if x not in REGISTER: bad += 1; print('UNKNOWN CONCEPT', x, file=sys.stderr)
        ok_q = norm(q) in TXT[ins]
        ok_p = norm(ph).lower() in norm(q).lower()
        if not (ok_q and ok_p): bad += 1; print('FAIL', ins, loc, ph, ok_q, ok_p, file=sys.stderr)
        rows.append([c, ph, 'nl', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok_q and ok_p else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    for k in list(PARTIAL) + list(ABSENT):
        if k not in REGISTER: bad += 1; print('UNKNOWN KEY', k, file=sys.stderr)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else ('base_parameters' if i < 60 else 'b651 heading RHFAC-does-not-name'))
            hit = [r for r in rows if c in r[0].split('|')]
            # status is decided on the IN-FORCE instrument (Bbl) only; Bouwbesluit 2012 and the ministry page do not make a concept FOUND
            live = [r for r in hit if r[6] == INST['BBL'][1].split('/')[-1]]
            if live:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL.get(c, '') + '; ' if c in PARTIAL else '') + notes])
            else:
                if c not in ABSENT: bad += 1; print('NO ABSENT NOTE', c, file=sys.stderr)
                w.writerow([c, src, 'SEARCHED-ABSENT', len(hit), ' / '.join(sorted({r[1] for r in hit})), ABSENT.get(c, 'NO NOTE: check')])
    print('observations', len(rows), 'failures (obs+rev+keys)', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
