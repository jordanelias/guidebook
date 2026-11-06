"""Build observations / coverage / reverse-harvest TSVs for the NO/NO terminology pass and VERIFY every
quote (after whitespace collapse) in the saved extracted text. Adapted from the FR/FR build.py.
Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NO-NO/build.py
Exits 1 if any quote, or any phrase within its quote, fails to verify. Read-only apart from the TSVs here.
Instrument keys: TEK = Lovdata consolidated TEK17 (Wayback snapshot 2026-06-20); Vx-y = the DiBK page
'Byggteknisk forskrift (TEK17) med veiledning' for section x-y (regulation text + DiBK guidance on one page);
V12-0 = DiBK 'Innledning til kapittel 12'. Locators say whether the quote is regulation text ('forskrift'),
DiBK guidance ('veiledning') or a DiBK 'preakseptert ytelse'. Written standard of every text: Bokmål (see pass-record)."""
import re, sys, csv, os
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NO-NO'
LANG = 'no (Bokmål)'
T_TEK = "Forskrift om tekniske krav til byggverk (Byggteknisk forskrift), FOR-2017-06-19-840 (Lovdata)"
T_DIBK = "Byggteknisk forskrift (TEK17) med veiledning (Direktoratet for byggkvalitet, dibk.no)"
INST = {'TEK': (T_TEK, D + '/text/ea23447c3072.txt'),
        'V12-0': (T_DIBK + ', Innledning til kapittel 12', D + '/text/cc6cab122620.txt')}
for line in open(D + '/tools/dibk_artefacts.tsv', encoding='utf-8'):
    sec, art, _sha = line.rstrip('\n').split('\t')
    INST['V' + sec] = (T_DIBK + ', § ' + sec, D + '/text/' + art[:12] + '.txt')
def norm(s): return re.sub(r'\s+', ' ', s.replace('​', '')).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

S1 = "Surface is firm, stable and slip resistant|Floor surface is stable, firm, and non-slip|Surface is stable, firm, and slip resistant"
LL = "Level landings with clear space|Level landings with clear space and at regular intervals"
WI = "Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)"
# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note (ours))
OBS = [
 ("Well-illuminated (if site expected to be lit)", "nødvendig belysning", "V8-6", "§ 8-6 (1) h (forskrift)", "ha nødvendig belysning.", "walkway lighting; purpose given as making the route and its edge visible"),
 ("Well-illuminated (if site expected to be lit)", "tilfredsstillende belysning", "V8-8", "§ 8-8 (1) b (forskrift)", "Parkeringsplassen skal ha tilfredsstillende belysning.", "parking for forflytningshemmede"),
 ("Well illuminated (if required for expected usage)", "god belysning", "V12-14", "§ 12-14 (1) f (forskrift)", "Trapperom skal ha god belysning slik at trappetrinn er synlige.", ""),
 ("Well illuminated (if required for expected usage)", "nødvendig belysning", "V12-6", "§ 12-6 (3) (forskrift)", "Nivåforskjeller skal være tydelig merket og ha nødvendig belysning.", ""),
 (WI + "|lighting levels", "Belysningsstyrken", "V12-4", "§ 12-4 (2) a, preakseptert ytelse", "Belysningsstyrken tilpasses material- og fargebruken slik at inngangspartiet og hovedinngangsdøren blir synlig i forhold til omliggende flater med luminanskontrast minimum 0,4.", "illuminance is named but never given a value; it is tuned to reach a luminance contrast"),
 (S1, "fast og sklisikkert dekke", "V8-6", "§ 8-6 (1) f (forskrift)", "ha fast og sklisikkert dekke", "'fast' (firm) and 'sklisikkert' (slip-safe); no separate 'stable' word"),
 (S1, "fast og sklisikkert dekke", "V8-5", "§ 8-5 (4) c (forskrift)", "fast og sklisikkert dekke", "housing with lift requirement"),
 (S1, "jevnt og sklisikkert dekke", "V12-16", "§ 12-16 (2) (forskrift)", "Rampe skal ha jevnt og sklisikkert dekke", "ramp surface: 'jevnt' (even) replaces 'fast'"),
 (S1, "uten at hjulene synker ned i dekket", "V8-6", "§ 8-6 (1) f, preakseptert ytelse", "gjør det mulig å kjøre med rullestol og rullator uten at hjulene synker ned i dekket,", "firmness defined functionally, by wheels not sinking in"),
 ("Floor surface is stable, firm, and non-slip", "overflatebelegg", "V12-5", "§ 12-5, preakseptert ytelse", "Det må benyttes overflatebelegg som i tørr eller våt frostfri tilstand ikke er så glatt at det er fare for fallskade ved forutsatt bruk.", "interior floor finish; slip defined dry and wet"),
 ("Floor surface is stable, firm, and non-slip", "sklisikker overflate", "V12-14", "§ 12-14 (1) g (forskrift)", "Inntrinn skal ha sklisikker overflate.", "stair treads only"),
 ("Seating", "sitteplasser", "V8-3", "§ 8-3 (5) d (forskrift)", "Det skal være plass for rullestol der det anlegges sitteplasser.", "regulates wheelchair space BESIDE seating, not the provision of seating"),
 ("Seating", "benker", "V8-3", "§ 8-3 (5) d, veiledning", "Ved benker kan det frie areal plasseres ved siden av eller overfor benk.", ""),
 ("Handrails", "håndløper", "V12-14", "§ 12-14 (1) a (forskrift)", "Trappen skal ha sikker avgrensing og håndløper på begge sider.", "'håndløper' is the handrail; 'rekkverk' is the guard (balustrade)"),
 ("Handrails", "håndløper", "V12-16", "§ 12-16 (3) (forskrift)", "Ramper skal ha håndløper på begge sider", ""),
 ("Handrails", "håndløper", "V8-9", "§ 8-9 (2) b (forskrift)", "håndløper på begge sider som følger hele trappeløpet og avsluttes med avrundet kant etter første og siste trinn", "outdoor stairs"),
 ("Handrails", "godt grep", "V12-14", "§ 12-14 (4) (forskrift)", "skal håndløperen utformes slik at den gir et godt grep.", "graspability as a requirement"),
 ("Clear width|width|Corridor width (parameter 4)", "fri bredde", "V12-6", "§ 12-6 (5) b (forskrift)", "Korridor og svalgang skal ha fri bredde på minimum 1,5 m.", "corridor and access balcony (svalgang) share one rule"),
 ("Clear width|width", "fri bredde", "V8-6", "§ 8-6 (1) d (forskrift)", "ha fri bredde minimum 1,8 m, unntatt for strekninger inntil 5,0 m som kan ha fri bredde minimum 1,4 m", "walkway width justified by two wheelchairs meeting"),
 ("Clear width|clearance", "fri passasje", "V12-7", "§ 12-7 (4) c (forskrift)", "Rom for varig opphold skal ha fri passasje på minimum 0,9 m til dør og vindu utenfor møbleringssone.", "passage measured outside the furnishing zone"),
 ("Clear width|clearance", "fri passasjebredde", "V12-9", "§ 12-9 (1) a (forskrift)", "Det skal være fri passasjebredde på minimum 0,9 m fram til fri plass ved siden av toalettet.", ""),
 ("Accessible path of travel", "gangatkomst", "TEK", "§ 1-3 d (definisjon)", "gangatkomst: gangvei fra kjørbar vei og parkering til inngangsparti til byggverk og uteoppholdsareal, og mellom disse", "EXTERIOR route only; a defined term"),
 ("Accessible path of travel", "Kommunikasjonsveier", "V12-6", "§ 12-6 (1) (forskrift)", "Kommunikasjonsveier skal være sikre og brukbare for den ferdsel og transport som forventes.", "INTERIOR route; not used for the approach or inside a dwelling (V12-0)"),
 ("Accessible path of travel", "Kommunikasjonsvei", "V12-0", "Begreper brukt i kapittel 12", "Atkomst- og forbindelsesveier i byggverk omfatter blant annet korridor, svalgang og trapperom. Begrepet brukes ikke om atkomstveien til byggverk eller arealer internt i en boenhet.", ""),
 ("Drainage", "fall til sluk", "TEK", "§ 13-15 (2) b (forskrift)", "Gulv skal ha tilstrekkelig fall til sluk slik at bruksvann ledes bort.", "PARTIAL: wet-room floors only; no route drainage"),
 ("Drainage", "overvann", "V12-4", "§ 12-4 (2) d, veiledning", "For håndtering av overvann, se § 13-11.", "PARTIAL: surface water at the entrance level area is a pointer to § 13-11 (not read)"),
 ("Clear signage", "skilt og merking", "V12-6", "§ 12-6 (6) c (forskrift)", "Det skal være skilt og merking som gir nødvendig informasjon. Skilt og merking skal være lette å lese og oppfatte.", ""),
 ("Clear signage", "lett å lese og oppfatte", "V12-18", "§ 12-18 (2) (forskrift)", "Informasjon skal være lett å lese og oppfatte.", ""),
 ("Audio accessibility and communication enhancement technologies", "lyd- og taleoverføringsutstyr", "V13-6", "§ 13-6 (4) (forskrift)", "I byggverk for publikum og arbeidsbygning skal det være lyd- og taleoverføringsutstyr", "required unless documented as unnecessary for 'god taleforståelse'"),
 ("Audio accessibility and communication enhancement technologies", "teleslynge", "V13-6", "§ 13-6 (4), preakseptert ytelse", "installeres teleslynge eller annet mikrofonbasert trådløst overføringsutstyr", "hearing loop; 1/10 of like meeting rooms suffices"),
 ("Audio accessibility and communication enhancement technologies", "Auditiv informasjon", "V12-6", "§ 12-6 (6) d (forskrift)", "Auditiv informasjon skal suppleres med visuell informasjon.", ""),
 (LL, "horisontalt hvileplan", "V12-16", "§ 12-16 (2) (forskrift)", "For hver 1,0 m høydeforskjell skal det være et horisontalt hvileplan med lengde minimum 1,5 m.", "ramp landing interval set by HEIGHT gained, not by run length"),
 (LL, "hvileplan", "V8-6", "§ 8-6 (1) c (forskrift)", "ha hvileplan på minimum 1,6 m x 1,6 m for hver 1,0 m høydeforskjell", "walkway rest landing; also by height difference"),
 ("Level landings with clear space", "Repos", "V12-14", "§ 12-14 (1) e (forskrift)", "Repos skal ha tilstrekkelig størrelse til å hindre og stanse fall.", "stair landing is a separate word; purpose is to stop falls"),
 ("Level landings with clear space|Clear space for approach", "horisontalt felt", "V12-4", "§ 12-4 (2) d (forskrift)", "Utenfor hovedinngangsdører skal det være et horisontalt felt på minimum 1,5 m x 1,5 m.", "level area outside entrance doors, outside the door swing"),
 ("Clear space for approach", "fri gulvplass", "V12-9", "§ 12-9 (2) b (forskrift)", "minimum 0,9 m fri gulvplass på begge sider av toalettet", ""),
 ("Clear space for approach", "fri sideplass", "V12-13", "§ 12-13 (3) d (forskrift)", "Ved skyvedør og sidehengslet dør skal det være tilstrekkelig fri sideplass til at personer i rullestol kan åpne og lukke døren.", "latch-side clear space"),
 ("Clear space for approach", "Betjeningsarealet", "V12-7", "§ 12-7 (4), veiledning", "Betjeningsarealet og snuarealet kan overlappe hverandre", "operating area vs turning area"),
 ("Shelter", "skjerming mot vær og klima", "V8-3", "§ 8-3 (1), veiledning", "felles uteoppholds- og lekearealer med solinnfall, skjerming mot vær og klima, og vern mot støy.", "PARTIAL: weather screening of outdoor amenity areas; no shelter at entrances or stops"),
 ("Riser height and tread depth|riser", "opptrinn", "V12-14", "§ 12-14 (1) c (forskrift)", "Trappen skal ha jevn stigning og samme høyde på opptrinn i hele trappens lengde.", ""),
 ("Riser height and tread depth|tread", "Inntrinn i ganglinjen", "V12-14", "§ 12-14 (1) d (forskrift)", "Inntrinn i ganglinjen skal være minimum 0,25 m.", "tread measured on the walking line (ganglinje)"),
 ("Riser height and tread depth", "trappeformelen", "V12-14", "§ 12-14 (1) c og d, preakseptert ytelse", "Trapper som utformes i samsvar med trappeformelen", "riser and tread governed jointly by a formula"),
 ("Nosing design", "utspring på trinnforkant", "V12-14", "§ 12-14 (1), veiledning", "Trapper med tette opptrinn og uten utspring på trinnforkant reduserer faren for snubling og fall.", "guidance, not a requirement"),
 ("No open riser", "tette opptrinn", "V12-14", "§ 12-14 (1), veiledning", "Trapper med tette opptrinn og uten utspring på trinnforkant reduserer faren for snubling og fall.", "PARTIAL: closed risers are advice, not required"),
 ("Level threshold", "Terskler skal være trinnfrie", "V12-13", "§ 12-13 (3) c (forskrift)", "Terskler skal være trinnfrie.", ""),
 ("Level threshold", "trinnfri", "TEK", "§ 1-3 m (definisjon)", "trinnfri: flate som kan ha terskel eller nivåforskjell på maksimum 25 mm.", "'step-free' is a DEFINED term with a tolerance; level threshold is an instance of it"),
 ("Height clearance (if sheltered or parkade)", "tilstrekkelig høyde under takutbygg", "V12-4", "§ 12-4 (1), preakseptert ytelse", "Det må være tilstrekkelig høyde under takutbygg og utstikkende bygningsdeler", "no parkade height found"),
 ("Height clearance (if sheltered or parkade)|Headroom and protruding objects", "takutspring", "TEK", "§ 10-3 (3) (forskrift)", "Avstanden fra underliggende terreng til takutspring og andre overliggende faste eller bevegelige deler av byggverket skal være tilfredsstillende slik at sammenstøt unngås.", "structural-safety chapter, not the accessibility chapters"),
 ("Headroom clearance (parameter 11)|Headroom|clearance", "fri høyde", "V12-13", "§ 12-13 (2) e (forskrift)", "Dører skal ha fri høyde på minimum 2,0 m.", ""),
 ("Headroom clearance (parameter 11)|Headroom", "fri høyde", "V12-14", "§ 12-14 (1) h (forskrift)", "Trapper med rette løp skal ha bredde på trappeløpet på minimum 0,90 m og fri høyde minimum 2,1 m.", ""),
 ("Headroom|Headroom and protruding objects", "underkanten av skilt", "V12-6", "§ 12-6 (1), preakseptert ytelse", "Avstanden fra underkanten av skilt som henger fra tak eller stikker ut fra vegg, må være minimum 2,25 meter til underliggende gulv.", ""),
 ("Edge protection", "Nivåforskjeller skal sikres", "V8-3", "§ 8-3 (3) b (forskrift)", "Nivåforskjeller skal sikres slik at fallskader forebygges.", "the trigger is the level difference; the means (rekkverk, gjerde, tett vegetasjon) is open"),
 ("Edge protection", "Rekkverk", "V12-15", "§ 12-15 (1) (forskrift)", "Rekkverk skal ha høyde og utforming som sikrer mot fall og sammenstøt, og skal utformes slik at det forhindrer klatring.", "guard; anti-climb is part of it"),
 ("Edge protection", "visuell og taktil avgrensing", "V8-6", "§ 8-6 (1) g (forskrift)", "ha visuell og taktil avgrensing", "walkway edge must be seen and felt (foot or mobility cane)"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "Inntrinn skal markeres", "V12-14", "§ 12-14 (2) c (forskrift)", "Inntrinn skal markeres slik at det oppnås luminanskontrast på minimum 0,8 i forhold til trinnfargen.", "PARTIAL: contrast and depth of the marking are set; slip resistance of the strip is not"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "synlig kontrastmarkering på trappeforkanten", "V8-9", "§ 8-9 (2) e (forskrift)", "synlig kontrastmarkering på trappeforkanten på de øvrige inntrinnene.", "outdoor stairs"),
 ("Colour-contrasted and slip-resistant strip", "rampens begynnelse være markert", "V12-16", "§ 12-16 (4) (forskrift)", "skal rampens begynnelse være markert i hele rampens bredde med luminanskontrast på minimum 0,8 mellom markering og bakgrunn.", "ramp start marking"),
 ("Tactile attention indicators (truncated domes)", "farefelt", "V12-14", "§ 12-14 (3) c (forskrift)", "Det skal være et farefelt foran det øverste trappetrinnet og et oppmerksomhetsfelt foran og inntil det nederste trinnet i hele trappens bredde.", "TWO fields: hazard (top) vs attention (bottom); domes not named"),
 ("Tactile attention indicators (truncated domes)", "oppmerksomhetsfelt", "V12-4", "§ 12-4 (2) b (forskrift)", "Det skal være et visuelt og taktilt oppmerksomhetsfelt foran hovedinngangsdører.", "attention field at entrances"),
 ("Tactile attention indicators (truncated domes)", "ikke forveksles med et farefelt", "V8-9", "§ 8-9 (2) d, preakseptert ytelse", "Oppmerksomhetsfeltet må ha en taktil utforming som ikke forveksles med et farefelt.", "the two fields must be tactilely distinct"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "stigning", "V12-16", "§ 12-16 (2) (forskrift)", "Rampe skal ha jevnt og sklisikkert dekke og stigning maksimum 1:15.", "ratio form 1:n"),
 ("Slope|slope|gradient", "Stigningsforhold", "V8-6", "§ 8-6 (1) b, veiledning", "Stigningsforhold på 1:15 på gangatkomst gir de beste forholdene for de fleste.", ""),
 ("Slope|slope", "tverrfall", "V8-6", "§ 8-6 (1) e (forskrift)", "ha tverrfall på maksimum 1:50", "cross slope is its own word"),
 ("gradient", "stigningsvinkel", "V8-9", "§ 8-9 (2) a, preakseptert ytelse", "Trapper i uteareal må ha stigningsvinkel mindre enn 30 grader.", "stair pitch, in degrees"),
 ("Sink faucet is easy to use or automatic", "Armaturen på servanter", "V12-18", "§ 12-18 (3) c (forskrift)", "Armaturen på servanter og i dusjer skal kunne betjenes med én hånd.", ""),
 ("Sink faucet is easy to use or automatic", "berøringsfri betjening", "V12-18", "§ 12-18 (3) c, preakseptert ytelse", "Armaturen på servanter må ha ettgreps hendel eller ha berøringsfri betjening.", "single lever or touch-free"),
 ("Outlets and switches are at accessible heights", "stikkontakter", "V12-18", "§ 12-18 (3) e (forskrift)", "skal tilstrekkelig antall stikkontakter plasseres slik at de kan betjenes av personer med funksjonsnedsettelse.", "outlets located by distance from corners (preakseptert ytelse), not by height"),
 ("Outlets and switches are at accessible heights", "Brytere", "V12-4", "§ 12-4 (2) e, preakseptert ytelse", "Brytere må ikke plasseres nærmere enn 0,5 meter fra innvendige hjørner.", "door-opener switches"),
 ("Accessible controls|height|Outlets and switches are at accessible heights", "betjeningshøyde", "V12-18", "§ 12-18 (3) a (forskrift)", "Betjeningspaneler skal være plassert med betjeningshøyde mellom 0,8 m og 1,2 m over det ferdige gulvet.", "operating height, a defined band"),
 ("Accessible lockers|ratio", "garderobene", "V12-8", "§ 12-8 (2) (forskrift)", "skal minst 1/10 av garderobene ha betjeningshøyde på maksimum 1,2 m.", "PARTIAL: cloakroom hanging, not lockers"),
 ("Accessible door hardware", "Håndtak", "V12-18", "§ 12-18 (3) b (forskrift)", "Håndtak skal være plassert med betjeningshøyde mellom 0,8 m og 1,2 m, være utformet med funksjonelt grep og ha en betjeningskraft slik at de er enkle å bruke.", "covers door, window and similar handles (veiledning (1))"),
 ("Accessible door hardware", "dørlås", "V12-4", "§ 12-4 (1), preakseptert ytelse", "Sikker betjening av ringeklokke, dørlås, samt åpning eller lukking av dør må være mulig fra rullestol.", ""),
 ("Accessible door hardware|Accessible controls", "Automatisk døråpner", "V12-13", "§ 12-13 (3) b (forskrift)", "Automatisk døråpner skal monteres utenfor dørens slagradius.", ""),
 ("Accessible controls", "styrings- og betjeningspanel", "V12-18", "§ 12-18 (1) (forskrift)", "Skilt, styrings- og betjeningspanel, håndtak, armaturer og lignende skal være enkle å forstå og betjene.", "signs, panels, handles and taps are one provision"),
 ("height|size", "romhøyde", "V12-7", "§ 12-7 (1) (forskrift)", "Rom og annet oppholdsareal skal ha utforming, romhøyde og størrelse tilpasset sin funksjon.", ""),
 ("level", "Nivåforskjeller", "V12-6", "§ 12-6 (3) (forskrift)", "Nivåforskjeller skal være tydelig merket og ha nødvendig belysning.", "level as a difference in height"),
 ("level", "inngangsplan", "V12-0", "Begreper brukt i kapittel 12", "Bygningens inngangsplan er det planet der bygningens hovedinngang er plassert.", "level as a floor plane; a defined term with a 1.2 m rule"),
 ("level", "Etasjetall", "V12-6", "§ 12-6 (6) c (forskrift)", "Etasjetall skal være visuelt og taktilt lesbart i alle etasjer.", "level as storey"),
 ("width", "bredde", "V12-16", "§ 12-16 (1) (forskrift)", "Rampe skal ha en bredde som er tilpasset forventet transport.", ""),
 ("number", "tilstrekkelig antall", "V8-8", "§ 8-8 (1) (forskrift)", "skal ha tilstrekkelig antall parkeringsplasser for forflytningshemmede", ""),
 ("depth", "dybde", "V12-14", "§ 12-14 (1) e, preakseptert ytelse", "Repos må ha minst samme dybde som bredden i det tilknyttede trappeløpet.", ""),
 ("depth", "dybde", "V12-9", "§ 12-9 (2) c, preakseptert ytelse", "Én servant må være høyderegulerbar eller ha fri høyde minimum 0,67 m i en dybde på minimum 0,5 m fra fronten av servanten.", "knee space"),
 ("force|Operating force (parameter 6)", "åpningskraft", "V12-13", "§ 12-13 (3) a (forskrift)", "Dører som er beregnet for manuell åpning til og i atkomst- og rømningsveier, skal kunne åpnes med åpningskraft på maksimum 30 N.", "door opening force"),
 ("force|Operating force (parameter 6)", "betjeningskraft", "V12-18", "§ 12-18 (3) d (forskrift)", "Hendelen skal kreve liten betjeningskraft og være plassert slik at den kan nås fra sittende stilling.", "window lever; no value"),
 ("size", "innvendig størrelse", "V12-3", "§ 12-3 (1) a (forskrift)", "skal minst én heisstol ha innvendig størrelse på minimum 1,1 m x 2,1 m.", "lift car size set by stretcher transport"),
 ("capacity", "tilstrekkelig kapasitet", "V15-9", "§ 15-9 (2), veiledning", "Ved prosjektering av en heis må heisstolen tilpasses slik at den gir tilstrekkelig kapasitet.", "lift capacity, the same sense as RHFAC's"),
 ("distance", "Avstand", "V8-8", "§ 8-8 (1) a, veiledning", "Avstand mellom hovedinngang og parkeringsplass må være så kort som mulig.", "DIFFERENT SENSE from RHFAC's trail distance"),
 ("ratio", "1/10 av rommene", "V12-7", "§ 12-7 (7) (forskrift)", "er det tilstrekkelig at 1/10 av rommene er universelt utformet i henhold til bestemmelser i forskriften.", "PARTIAL: share of like rooms (guest rooms, fitting rooms); no shower/bath mix"),
 ("Turning circle (parameter 5)", "snusirkel", "V12-7", "§ 12-7 (4) a, preakseptert ytelse", "en snusirkel med diameter på 1,5 m eller", ""),
 ("Turning circle (parameter 5)", "snurektangel", "V12-7", "§ 12-7 (4) a, preakseptert ytelse", "et snurektangel på 1,3 m x 1,8 m.", "a rectangle is an accepted alternative in housing only"),
 ("Turning circle (parameter 5)", "snuareal for rullestol", "V12-7", "§ 12-7 (4) a (forskrift)", "Rom skal ha trinnfri tilgang og snuareal for rullestol.", "the regulation word; circle and rectangle are its accepted forms"),
 ("Reverberation time (parameter 7)", "romakustiske forhold", "V13-6", "§ 13-6 (1), veiledning", "romakustiske forhold, inkludert taleforståelse", "BROADER: room acoustics incl. speech intelligibility; the quantity is delegated to NS 8175 lydklasse C (not read)"),
 ("LRV contrast (parameter 8)", "Luminanskontrast", "V12-0", "Begreper brukt i kapittel 12", "Luminanskontrast Kontrast som oppstår grunnet synlige forskjeller mellom objektets og bakgrunnens luminans", "DIFFERENT QUANTITY: luminance contrast (values 0,4 / 0,8), not an LRV difference"),
 ("LRV contrast (parameter 8)", "Synlig kontrast", "V12-9", "§ 12-9 (2) a, preakseptert ytelse", "Synlig kontrast innebærer at luminanskontrasten må være minimum 0,4.", "'synlig kontrast' in a regulation is read through a luminance-contrast value"),
 ("Door width (parameter 9)", "fri bredde", "V12-13", "§ 12-13 (2) a (forskrift)", "Inngangsdør og dører i kommunikasjonsveier skal ha fri bredde på minimum 0,86 m.", ""),
 ("Door width (parameter 9)", "Fri bredde måles når døren har maksimal åpning", "V12-13", "§ 12-13, veiledning", "Fri bredde måles når døren har maksimal åpning", "measurement rule; one quantity, not a nominal/clear pair"),
 ("Ramp run length (parameter 12)", "strekninger", "V12-16", "§ 12-16 (2) (forskrift)", "For strekninger under 3,0 m kan stigningen være maksimum 1:12.", "PARTIAL: run length appears only as the condition for a steeper gradient"),
 ("Gratings", "skraperist", "V12-4", "§ 12-4 (2) b, veiledning", "En nedfelt skraperist foran inngangsdøren er et eksempel på et oppmerksomhetsfelt.", "PARTIAL: a grating used AS an attention field; no opening-size rule found"),
 ("Headroom and protruding objects|Protruding objects", "Utstikkende bygningsdeler", "V12-5", "§ 12-5, preakseptert ytelse", "Utstikkende bygningsdeler og kanter som kan skade personer ved sammenstøt, må merkes og sikres.", ""),
 ("Protruding objects", "utstikkende elementer", "V8-4", "§ 8-4 (1), veiledning", "Det er viktig at gangatkomsten er fri for hindre og utstikkende elementer fra byggverket", ""),
 ("Lavatories", "servanten", "V12-9", "§ 12-9 (2) c (forskrift)", "Det skal være tilstrekkelig fri plass under servanten.", "B651 'lavatory' = washbasin = 'servant'"),
 ("Enclosures", "dusjkabinett", "V12-9", "§ 12-9 (1) b, veiledning", "Kravet forhindrer ikke montering av dusjkabinett, badekar eller lignende", "PARTIAL: the shower is a 'dusjsone' that must work WITHOUT an enclosure"),
 ("Bollards", "Stolper", "V8-3", "§ 8-3 (5) c (forskrift)", "Stolper, rekkverk og lignende skal ha synlig kontrast til omgivelsene.", "PARTIAL: posts generally, for contrast"),
 ("Landscaping elements|Vegetation", "tett vegetasjon", "V8-3", "§ 8-3 (3) b, preakseptert ytelse", "må sikres med rekkverk, gjerde, tett vegetasjon eller lignende slik at fallskader forebygges.", "PARTIAL: vegetation as a fall barrier, not as a hazard or amenity"),
 ("Landscaping elements|Flower or shrub planters", "fastmontert blomsterkasse", "V12-15", "§ 12-15 (4), veiledning", "Eksempel på annen forsvarlig anordning er en fastmontert blomsterkasse", "PARTIAL: planter as edge protection"),
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
PARTIAL = {  # concept -> why the Norwegian match is not the English concept (ours; a judgment, not a derivation)
 "Seating": "NARROWER: wheelchair space beside seating; provision of seating not required",
 "Drainage": "NARROWER: wet-room falls to drain; route drainage only by pointer (§ 13-11 not read)",
 "Shelter": "DIFFERENT: weather screening of outdoor amenity areas (guidance)",
 "No open riser": "WEAKER: closed risers are guidance, not a requirement",
 "Colour-contrasted and slip-resistant strip on nosing": "NARROWER: contrast marking only; slip resistance not attached to the strip",
 "Colour-contrasted and slip-resistant strip": "NARROWER: contrast marking only",
 "Accessible lockers": "DIFFERENT: cloakroom (garderobe) hanging height, not lockers",
 "distance": "DIFFERENT SENSE: parking-to-entrance distance, not trail distance",
 "ratio": "PARTIAL: 1/10 of like rooms; no shower/bath mix",
 "Reverberation time (parameter 7)": "BROADER: 'romakustiske forhold'; value delegated to NS 8175",
 "LRV contrast (parameter 8)": "DIFFERENT QUANTITY: luminance contrast, not LRV",
 "Ramp run length (parameter 12)": "PARTIAL: run length only conditions the gradient; landings set by height gained",
 "Gratings": "DIFFERENT FUNCTION: grating as attention field",
 "Enclosures": "DIFFERENT CARVE: shower zone that must work without an enclosure",
 "Bollards": "BROADER: posts generally",
 "Landscaping elements": "DIFFERENT FUNCTION: vegetation and planters as fall barriers",
 "Flower or shrub planters": "DIFFERENT FUNCTION: planter as edge protection",
 "Vegetation": "DIFFERENT FUNCTION: dense vegetation as fall barrier",
}
ABSENT = {
 "Microwave mounting height accessible and safe": "'mikrobølge' 0/0; § 12-18 veiledning excludes kitchen hood panels; § 12-10 treats the kitchen only as food storage",
 "time": "no opening, hold-open or closing time for automatic doors; 'lukketid' 0/0; 'åpningstid' only as building opening hours (§ 12-9 veiledning)",
 "volume": "'volum' only as building volume (NS 3940 area and volume calculation, ch. 5); no sound volume; 'lydnivå' 0/0",
 "Colour temperature (parameter 10)": "'fargetemperatur' 0/0, 'kelvin' 0/0; § 13-7 regulates daylight factor only",
 "Spouts": "'drikkefontene' 0/0, 'vannpost' 0/0; drinking fountains not regulated",
 "Speed bumps": "'fartsdump' 0/0, 'fartshump' 0/0",
 "Guy wires": "'barduner' 0/0",
 "Scaffolding": "'stillas' 0/0",
 "Gradation limits": "'gradering' 0/0; the only aggregate named is 'steinmel (subus)' as an example of a firm surface",
}

# Reverse harvest: (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss OURS, not an equivalence)
REV = [
 ("Universell utforming", "defined term", "V12-0", "Begreper brukt i kapittel 12", "Utforming eller tilrettelegging av hovedløsningen i de fysiske forholdene slik at virksomhetens alminnelige funksjon kan benyttes av flest mulig.", "defined through the main solution"),
 ("Hovedløsning", "defined term", "V12-0", "Begreper brukt i kapittel 12", "Løsningen som gjør byggverk for publikum eller arbeidsbygning brukbar for flest mulig, uten at det er nødvendig å etablere særlige tiltak for enkelte grupper.", "the main solution must itself be usable; no separate entrances"),
 ("tilgjengelig", "defined quality level", "V12-0", "Innledning", "Uttrykket tilgjengelig brukes om et kvalitetsnivå der ikke alle kravene til universell utforming gjelder.", "a lower tier than universal design, used for housing"),
 ("dimensjoneringsgrunnlaget", "design basis", "V12-0", "Innledning", "En person som bruker manuell rullestol, eller elektrisk rullestol for kombinert inne- og utebruk, er utgangspunkt for dimensjoneringsgrunnlaget.", ""),
 ("full førlighet i overkroppen", "design basis", "V12-0", "Begreper brukt i kapittel 12", "Dimensjoneringsgrunnlaget er person med full førlighet i overkroppen i manuell rullestol.", "the 'tilgjengelig' level assumes full upper-body function"),
 ("Tilgjengelig boenhet", "defined term (dwelling)", "V12-0", "Begreper brukt i kapittel 12", "Alle hovedfunksjoner finnes på inngangsplanet, og", ""),
 ("hovedfunksjoner", "defined term", "TEK", "§ 1-3 e", "hovedfunksjoner: stue, kjøkken, soverom, bad og toalett.", ""),
 ("Øvrige plan", "defined term", "V12-0", "Begreper brukt i kapittel 12", "Øvrige plan er de plan som har en høydeforskjell på mer enn 1,2 meter fra inngangsplanet.", ""),
 ("Byggverk for publikum", "building typology", "V12-0", "Begreper brukt i kapittel 12", "Bygninger, anlegg og konstruksjoner der publikum har tilgang.", "includes bridges, piers and viewing platforms"),
 ("Arbeidsbygning", "building typology", "V12-0", "Begreper brukt i kapittel 12", "Bygning med arbeidsplasser.", ""),
 ("uegnet for personer med funksjonsnedsettelse", "exemption category", "V12-1", "§ 12-1 (2) (forskrift)", "med mindre byggverket eller deler av byggverket etter sin funksjon er uegnet for personer med funksjonsnedsettelse.", "exemption must be documented"),
 ("funksjonskrav", "drafting category", "TEK", "§ 1-3 c", "funksjonskrav: overordnet formål eller oppgave som skal oppfylles i det ferdige byggverket", "functional requirement"),
 ("preakseptert ytelse", "drafting category", "TEK", "§ 1-3 j", "preakseptert ytelse: ytelse angitt av Direktoratet for byggkvalitet, og som vil oppfylle, eller bidra til å oppfylle, ett eller flere funksjonskrav i byggteknisk forskrift", "deemed-to-satisfy performance set by the directorate"),
 ("likestilt deltakelse", "concept", "V12-7", "§ 12-7 (5) a (forskrift)", "utforming og størrelse slik at likestilt deltakelse er mulig", "equal participation, not only access"),
 ("likestilt bruk", "concept", "V8-3", "§ 8-3 (5) a (forskrift)", "som muliggjør deltakelse og likestilt bruk.", ""),
 ("horisontalt felt med fast dekke", "space", "V8-3", "§ 8-3 (5) a (forskrift)", "Opparbeidet areal avsatt til lek og rekreasjon skal ha et horisontalt felt med fast dekke på minimum 1,6 m x 1,6 m", "level pad at play equipment for wheelchair users and parents"),
 ("Opparbeidet badeplass", "space", "V8-3", "§ 8-3 (5) e (forskrift)", "Opparbeidet badeplass skal være utstyrt eller utformet slik at det er lett å komme seg ned i og opp av vannet.", "bathing place"),
 ("Opparbeidet utendørs nivåforskjell", "element", "V8-3", "§ 8-3 (5) b (forskrift)", "Opparbeidet utendørs nivåforskjell skal være merket visuelt og taktilt.", ""),
 ("følbart med føttene", "technique", "V8-3", "§ 8-3 (5) b, preakseptert ytelse", "Den taktile merkingen må utføres slik at merkingen er følbart med føttene.", "tactile = felt underfoot"),
 ("Uteoppholdsareal", "space", "V8-3", "§ 8-3 (1) (forskrift)", "Uteoppholdsarealer skal etter sin funksjon være egnet for rekreasjon, lek og aktiviteter for ulike aldersgrupper.", ""),
 ("uteareal for allmennheten", "space", "V8-2", "§ 8-2 (1) a (forskrift)", "uteareal for allmennheten", ""),
 ("gangsone", "technique", "V8-4", "§ 8-4 (2) (forskrift)", "skal ha tydelig avgrenset gangsone eller ledelinje.", "walking zone"),
 ("ledelinje", "element", "V8-4", "§ 8-4 (2) (forskrift)", "skal ha tydelig avgrenset gangsone eller ledelinje.", "guidance line; register has no guidance-path row"),
 ("villedende retningsinformasjon", "hazard", "V8-4", "§ 8-4 (2) (forskrift)", "Mønstre i gategrunnen skal ikke gi villedende retningsinformasjon.", "misleading paving patterns"),
 ("Arkitektoniske virkemidler", "technique", "V12-6", "§ 12-6 (6) h, veiledning", "Arkitektoniske virkemidler for veifinning er normalt et bedre valg enn kunstige ledelinjer.", "architectural means preferred over artificial guidance lines"),
 ("retningsinformasjonen", "technique", "V12-6", "§ 12-6 (6) g (forskrift)", "Ved endring av gangretning skal retningsinformasjonen angis dersom det er nødvendig.", ""),
 ("Repeterende informasjon", "technique", "V12-6", "§ 12-6 (6) g (forskrift)", "Repeterende informasjon skal være mest mulig lik i hele bygningen.", "consistency of repeated information"),
 ("Blendende motlys", "hazard", "V12-6", "§ 12-6 (6) e (forskrift)", "Blendende motlys skal unngås i kommunikasjonsveier.", "glare from backlight; register has no glare row"),
 ("Søyler", "element", "V12-6", "§ 12-6 (6) f (forskrift)", "Søyler og lignende skal plasseres slik at de ikke er til hinder i kommunikasjonsveier.", "columns"),
 ("merkes i to høyder", "technique", "V12-6", "§ 12-6 (6) f (forskrift)", "merkes i to høyder med luminanskontrast på minimum 0,8 til bakgrunnsfargen.", ""),
 ("Taktile etasjetall", "element", "V12-6", "§ 12-6 (6) c, preakseptert ytelse", "Taktile etasjetall må plasseres i høyde mellom 0,8 meter og 1,2 meter over gulvet", "tactile floor numbers"),
 ("etasjeangivelse", "technique", "V12-14", "§ 12-14 (3) b (forskrift)", "Ved begynnelsen av hver etasje skal etasjeangivelse markeres.", "floor marking on the handrail"),
 ("møteplasser", "space", "V12-6", "§ 12-6 (5) b, preakseptert ytelse", "må det være møteplasser med en bredde på 1,8 meter i en lengde på minimum 2,0 meter.", "passing places in long corridors"),
 ("svalgang", "element", "V12-6", "§ 12-6 (5) b (forskrift)", "Korridor og svalgang skal ha fri bredde på minimum 1,5 m.", "access balcony/gallery"),
 ("dørens slagradius", "defined space", "V12-13", "§ 12-13 (3) b, veiledning", "Med dørens slagradius forstår vi området som døren slår ut over når den åpnes eller lukkes.", ""),
 ("slagarealet", "space", "V12-7", "§ 12-7 (4) a, preakseptert ytelse", "Snuarealet må ikke overlappe slagarealet til den døren som skal betjenes.", ""),
 ("møbleringssone", "space", "V12-7", "§ 12-7 (4) c (forskrift)", "til dør og vindu utenfor møbleringssone.", "furnishing zone"),
 ("trinnfri dusjsone", "space", "V12-9", "§ 12-9 (1) b (forskrift)", "Det skal være mulighet for trinnfri dusjsone.", "a possibility, in housing"),
 ("festemulighet for ettermontering", "technique", "V12-9", "§ 12-9 (1) c (forskrift)", "Vegg i dusj- og toalettsonen skal gi festemulighet for ettermontering av nødvendig utstyr.", "blocking for later grab bars"),
 ("håndstøtte", "element", "V12-9", "§ 12-9 (2) b (forskrift)", "Toalettet skal ha håndstøtte på begge sider.", "toilet support rail; register has no grab-bar row"),
 ("høyderegulerbar", "technique", "V12-9", "§ 12-9 (2) c, preakseptert ytelse", "Én servant må være høyderegulerbar", ""),
 ("Dusjhodet skal være regulerbart i høyden", "technique", "V12-9", "§ 12-9 (2) d (forskrift)", "Dusjhodet skal være regulerbart i høyden", ""),
 ("termostat", "element", "V12-18", "§ 12-18 (3) c (forskrift)", "Armaturen i dusjen skal ha termostat.", ""),
 ("ettgreps hendel", "element", "V12-18", "§ 12-18 (3) c, preakseptert ytelse", "Armaturen på servanter må ha ettgreps hendel eller ha berøringsfri betjening.", "single-lever mixer"),
 ("betjenes med én hånd", "technique", "V12-18", "§ 12-18 (3) d (forskrift)", "skal minst ett vindu kunne betjenes med én hånd.", ""),
 ("Felles avfallssystem", "element", "V12-12", "§ 12-12 (2) (forskrift)", "Felles avfallssystem for boligbygninger med krav om tilgjengelig boenhet og for byggverk med krav om universell utforming, skal være lett tilgjengelig, ha trinnfri atkomst og ha innkasthøyde på maksimum 1,2 m.", "shared waste system"),
 ("innkasthøyde", "quantity", "V12-12", "§ 12-12 (2) (forskrift)", "ha innkasthøyde på maksimum 1,2 m.", "waste-chute insert height"),
 ("parkeringsplasser for forflytningshemmede", "space", "V8-8", "§ 8-8 (1) (forskrift)", "skal ha tilstrekkelig antall parkeringsplasser for forflytningshemmede", "population word 'forflytningshemmede'"),
 ("rullestolsymbol", "element", "V8-8", "§ 8-8 (1) c, preakseptert ytelse", "merkes med rullestolsymbol på dekket.", ""),
 ("oppstillingsareal for rullestol, barnevogn og lignende", "space", "V8-8", "§ 8-8 (2) (forskrift)", "skal ha tilstrekkelig oppstillingsareal for rullestol, barnevogn og lignende", "parking for wheelchairs and prams"),
 ("kjøreatkomst", "element", "V8-8", "§ 8-8 (3) (forskrift)", "skal ha tilfredsstillende kjøreatkomst.", "vehicle approach; normally sized for a taxi (veiledning)"),
 ("tilgang for drosje", "provision rule", "V8-8", "§ 8-8 (3), veiledning", "normalt må det planlegges for tilgang for drosje.", ""),
 ("mobilitetsstokk", "user aid", "V8-6", "§ 8-6 (1) g, preakseptert ytelse", "Det må være mulig å kjenne avgrensingen på gangatkomsten med føttene eller med mobilitetsstokk.", ""),
 ("Kantstein", "element", "V8-6", "§ 8-6 (1) g, preakseptert ytelse", "Kantstein kan være en taktil og visuell avgrensing", "kerb as edge cue"),
 ("trinnfrie", "concept", "V8-6", "§ 8-6 (1) a (forskrift)", "være trinnfrie", "step-free as an attribute of the walkway"),
 ("uforholdsmessige terrenginngrep", "exemption condition", "V8-6", "§ 8-6 (2), veiledning", "Når situasjonen tilsier at et stigningsforhold på 1:15 vil kreve uforholdsmessige terrenginngrep", "disproportionate terrain works"),
 ("Inneklemte tomter", "exemption condition", "V8-5", "§ 8-5 (2), veiledning", "Inneklemte tomter i etablerte boligområder.", ""),
 ("løfteplattform", "element", "V12-3", "§ 12-3 (1) (forskrift)", "I byggverk med inntil tre etasjer og med liten persontrafikk kan løfteplattform erstatte heis.", "platform lift"),
 ("liten persontrafikk", "condition", "V12-3", "§ 12-3 (1) (forskrift)", "med liten persontrafikk kan løfteplattform erstatte heis.", "defined by number of workplaces (preakseptert ytelse)"),
 ("båretransport", "design basis", "V12-3", "§ 12-3 (1) a, veiledning", "Kravet til minimumsstørrelse på heisstoler er fastsatt ut fra hensynet til båretransport.", "stretcher transport"),
 ("heisstol", "element", "V12-3", "§ 12-3 (1) b (forskrift)", "I byggverk med to etasjer skal minst én heisstol ha innvendig størrelse på minimum 1,1 m x 1,6 m.", "lift car"),
 ("døgnbemannet vakt", "element", "V15-9", "§ 15-9 (5) (forskrift)", "Heisen skal ha en alarm som er tilknyttet døgnbemannet vakt.", ""),
 ("toveis kommunikasjonsmidler", "element", "V15-9", "§ 15-9 (5), veiledning", "Heisstoler må være utstyrt med toveis kommunikasjonsmidler", ""),
 ("De omliggende veggene skal være tilstrekkelig synlige", "technique", "V15-9", "§ 15-9 (2) (forskrift)", "De omliggende veggene skal være tilstrekkelig synlige i forhold til heisen.", "contrast moved from the lift door to the surrounding walls"),
 ("glassmarkør", "element", "V12-17", "§ 12-17 (2) (forskrift)", "skal være kontrastmerket med glassmarkør, som er synlig fra begge sider og i to høyder", ""),
 ("Mønsteret i glassmarkøren", "technique", "V12-17", "§ 12-17 (2) (forskrift)", "Mønsteret i glassmarkøren i døren skal være forskjellig fra glassmarkøren i nærliggende glassfelt.", "door and adjacent glass marked differently"),
 ("personsikkerhetsrute", "element", "V12-17", "§ 12-17 (1) (forskrift)", "Sikringen kan være brystning, personsikkerhetsrute eller en annen forsvarlig metode.", "safety glazing"),
 ("Rullende tekst", "hazard", "V12-18", "§ 12-18 (2), veiledning", "Rullende tekst er derfor ikke egnet for å gi viktig informasjon.", "scrolling text"),
 ("Berøringsskjermer", "element", "V12-18", "§ 12-18 (1), veiledning", "Berøringsskjermer er lite tilgjengelige for svaksynte og umulig å bruke for blinde.", "touchscreens"),
 ("Taktile tegn", "technique", "V12-18", "§ 12-18 (2) (forskrift)", "Viktig informasjon skal være tilgjengelig med tekst og lyd. Taktile tegn kan erstatte lyd.", "two-sense rule for important information"),
 ("Punktstørrelse", "quantity", "V12-18", "§ 12-18 (2), preakseptert ytelse", "Punktstørrelse på skjermer eller displayer må tilpasses forventet leseavstand.", "type size related to reading distance"),
 ("Standardiserte piktogrammer", "technique", "V12-18", "§ 12-18 (2), preakseptert ytelse", "Standardiserte piktogrammer kan erstatte tekst på enkelte skilt.", ""),
 ("god taleforståelse", "concept", "V13-6", "§ 13-6 (4) (forskrift)", "med mindre det kan dokumenteres at dette er unødvendig for å oppnå god taleforståelse.", "speech intelligibility"),
 ("forsterket lyd- og taleoverføring", "technique", "V13-6", "§ 13-6 (4) (forskrift)", "Inngangen til rom med forsterket lyd- og taleoverføring skal være tydelig merket.", ""),
 ("lydklasse C", "compliance route", "V13-6", "§ 13-6 (1) (forskrift)", "kan oppfylles ved å tilfredsstille lydklasse C i Norsk Standard NS 8175:2012", "sound class by reference to a standard"),
 ("resepsjon eller informasjonstavle", "element", "V12-7", "§ 12-7 (6) (forskrift)", "I byggverk med krav om universell utforming skal det være resepsjon eller informasjonstavle der dette er nødvendig.", ""),
 ("nedsatt kognitivitet (forståelsestap)", "population carve", "V12-1", "§ 12-1 (2), veiledning", "Nedsatt fysisk kraft og bevegelse, nedsatt syn, nedsatt hørsel, nedsatt kognitivitet (forståelsestap) og allergier påvirker evnen til å mestre utfordringer.", "five-way list incl. allergies"),
 ("ømfintlige for inneklimafaktorer", "population carve", "V12-1", "§ 12-1 (2), veiledning", "Personer som ikke kan kommunisere ved stemmebruk og personer som er ømfintlige for inneklimafaktorer, inngår også i dimensjoneringsgrunnlaget.", "indoor-climate sensitivity and non-speaking people in the design basis"),
 ("returrekkverk", "element", "V12-15", "§ 12-15 (2), veiledning", "Med returrekkverk menes rekkverk rundt trappehullet.", ""),
 ("barnesikring", "technique", "V12-17", "§ 12-17 (3) (forskrift)", "skal vindu ha barnesikring hvis vinduet er plassert fra 3,3 m over terrenget", ""),
 ("assistert rømning (evakueringsplaner)", "operational rule", "V12-13", "§ 12-13 (4) a, veiledning", "planlegging av assistert rømning (evakueringsplaner)", "assisted evacuation, tied to the door-force rule"),
 ("indre ganglinje", "defined line", "V12-14", "§ 12-14 (2) e, veiledning", "Indre ganglinje er 0,3 meter fra håndløper langs trappens indre begrensing.", ""),
 ("svingt trapp", "element", "V12-14", "§ 12-14 (2) e (forskrift)", "For svingt trapp skal inntrinn i den indre ganglinje være minimum 0,15 m.", "winding stair"),
 ("avrundet avslutning", "technique", "V12-14", "§ 12-14 (2) b (forskrift)", "føres utover øverste og nederste trinn med avrundet avslutning", "rounded handrail ends"),
 ("Taktil", "defined term", "V12-0", "Begreper brukt i kapittel 12", "Det som er følbart, som kan oppleves gjennom berøringssansen.", ""),
 ("Auditiv", "defined term", "V12-0", "Begreper brukt i kapittel 12", "Det som angår hørselen.", ""),
 ("Luminans", "defined quantity", "V12-0", "Begreper brukt i kapittel 12", "Et objekts lyshet. Luminans måles i candela/m2.", ""),
]

def write_rev():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and (norm(ph).lower() in norm(q).lower() or norm(ph) in TXT[ins])
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, file=sys.stderr)
            w.writerow([ph, kind, LANG, INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    print('reverse-harvest', len(REV), 'verified', len(REV) - bad)
    return bad

def main():
    bad = write_rev(); rows = []
    for c, ph, ins, loc, q, note in OBS:
        ok_q = norm(q) in TXT[ins]
        ok_p = norm(ph).lower() in norm(q).lower()
        if not (ok_q and ok_p): bad += 1; print('FAIL', ins, loc, ph, ok_q, ok_p, file=sys.stderr)
        for x in c.split('|'):
            if x not in REGISTER: bad += 1; print('UNKNOWN CONCEPT', x, file=sys.stderr)
        # a regulation quote taken from a DiBK page must also be in the Lovdata text (currency cross-check)
        lov = ''
        if ins != 'TEK' and '(forskrift)' in loc:
            lov = 'yes' if norm(q) in TXT['TEK'] else 'NO'
            if lov == 'NO': print('NOTE: forskrift quote not in Lovdata snapshot', ins, loc, file=sys.stderr)
        rows.append([c, ph, LANG, INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok_q and ok_p else 'NO', lov, note])
    with open(D + '/observations.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'forskrift_quote_also_in_lovdata_snapshot', 'note (ours)'])
        w.writerows(rows)
    with open(D + '/coverage.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else ('base_parameters' if i < 60 else 'b651-headings RHFAC-does-not-name'))
            hit = [r for r in rows if c in r[0].split('|')]
            if hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[9] for r in hit if r[9]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE: check')])
                if c not in ABSENT: bad += 1; print('ABSENT WITHOUT NOTE', c, file=sys.stderr)
    print('observations', len(rows), 'failures (obs+rev)', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
