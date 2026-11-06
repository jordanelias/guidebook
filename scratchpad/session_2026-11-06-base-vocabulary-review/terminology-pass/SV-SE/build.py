"""Build observations / coverage / reverse-harvest TSVs for the SV-SE terminology pass, verifying every
quote (after whitespace collapse) in the saved extracted text. Adapted from FR-FR/build.py. Run from the
repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/SV-SE/build.py
Exits non-zero if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder."""
import re, sys, csv
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/SV-SE'
INST = {
 'P12': ("Boverkets föreskrifter om byggnaders tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga (BFS 2024:12)", D + '/text/b8d1102ac9bece6f.txt'),
 'P9': ("Boverkets föreskrifter om säkerhet vid användning av byggnader (BFS 2024:9)", D + '/text/dea239e870469ba8.txt'),
 'P13': ("Boverkets föreskrifter om krav på tomter m.m. (BFS 2024:13)", D + '/text/24b5e81b0f4a0928.txt'),
 'HIN': ("Boverkets föreskrifter och allmänna råd (2011:13) om avhjälpande av enkelt avhjälpta hinder till och i lokaler dit allmänheten har tillträde och på allmänna platser, omtryck BFS 2013:9 (HIN 3)", D + '/text/c40b915d36d9d797.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()

def chain():
    """The saved text must be exactly `pdftotext -layout` of the persisted PDF (retrieval_log.locate_quote
    cannot decode PDFs, so this is the raw-byte link). Returns the number of mismatches."""
    import subprocess, hashlib
    bad = 0
    for k, (_t, path) in INST.items():
        stem = path.split('/')[-1][:-4]
        pdf = 'retrieval-log/session_2026-11-06-base-vocabulary-review/' + stem + '.pdf'
        out = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, check=True).stdout
        same = out == open(path, 'rb').read()
        if not same: bad += 1
        print('chain', k, stem, 'pdf sha256', hashlib.sha256(open(pdf, 'rb').read()).hexdigest()[:16], 'text matches pdftotext' if same else 'TEXT DIFFERS', file=sys.stderr)
    return bad
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}
AR = ' (allmänt råd)'  # HIN advice text, not binding; marked in the locator

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note)
OBS = [
 # lighting
 ("Well-illuminated (if site expected to be lit)", "Belysningen på gångytor", "HIN", "15 §" + AR, "Belysningen på gångytor och vid viktiga målpunkter bör anpassas så att den är jämn", "public places (allmänna platser); advice tier"),
 ("Well illuminated (if required for expected usage)|lighting levels", "belysningen vara så stark och jämn", "P9", "2 kap. 1 §", "I kommunikationsutrymmen ska belysningen vara så stark och jämn att personer kan röra sig säkert i byggnaden.", "for 'lighting levels': strength and evenness stated as a function; no illuminance quantity"),
 ("Well illuminated (if required for expected usage)", "Belysningen ska vara projekterad och utförd", "P12", "3 kap. 2 §", "Belysningen ska vara projekterad och utförd så att personer med nedsatt rörelse- eller orienteringsförmåga kan orientera sig.", "lighting framed as an orientation aid, not a level"),
 ("Well illuminated (if required for expected usage)", "bristande eller bländande belysning", "HIN", "9 §", "Hinder i form av bristande eller bländande belysning ska avhjälpas.", "insufficient or glaring lighting is a named obstacle"),
 ("Well illuminated (if required for expected usage)", "Belysningen i kommunikationsutrymmen", "HIN", "9 §" + AR, "Belysningen i kommunikationsutrymmen bör anpassas så att den är jämn", ""),
 # surfaces
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "jämna och fasta", "P13", "2 kap. 3 § 2", "2. vara jämna och fasta,", "walkways on a plot; 'fast' (firm) and 'jämn' (even); slip resistance is not in this clause"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "fast, jämn och halkfri", "HIN", "17 §" + AR, "Markbeläggningen bör vara fast, jämn och halkfri.", "parking places for disabled permit holders"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "jämn och halkfri yta", "HIN", "6 §" + AR, "Rampen bör ha jämn och halkfri yta", "ramp surface"),
 ("Floor surface is stable, firm, and non-slip", "risken för att halka begränsas", "P9", "2 kap. 2 §", "Ytor som är avsedda att gå på ska vara utformade så att risken för att halka begränsas.", "functional: risk of slipping limited; 'ytor som är avsedda att gå på' covers floor and ground"),
 ("Floor surface is stable, firm, and non-slip", "halkegenskaper", "P9", "2 kap. 3 §", "ojämnheter, låga hinder eller förändringar i ytmaterialens halkegenskaper, som är oväntade eller svåra att upptäcka", "unexpected change in slip properties is itself the hazard"),
 ("Floor surface is stable, firm, and non-slip", "ojämn markbeläggning", "HIN", "12 §", "Fysiska hinder såsom mindre nivåskillnader, ojämn markbeläggning, svårforcerade ränndalar och trottoarkanter ska avhjälpas.", "public places"),
 # seating
 ("Seating", "publikplatser", "P12", "2 kap. 6 §", "En samlingslokal i en publik lokal får utformas och dimensioneras utan att alla publikplatser är tillgängliga och användbara för personer med nedsatt rörelseförmåga.", "DIFFERENT SENSE: audience places in an assembly hall; rest seating along a route is not treated"),
 # handrails
 ("Handrails", "ledstänger", "P9", "2 kap. 12 §", "Trappor och ramper ska ha ledstänger på båda sidor som stöd för balansen.", "handrail is defined by purpose: support for balance"),
 ("Handrails", "Ledstänger ska", "P9", "2 kap. 13 §", "Ledstänger ska", ""),
 ("Handrails", "balansstöd i form av ledstång", "P13", "4 kap. 2 §", "Trappor och ramper på en tomt ska ha balansstöd i form av ledstång, om det behövs för att skydda mot fall.", "'balansstöd' is the class, 'ledstång' one form of it"),
 ("Handrails", "balansstöd", "HIN", "10 §", "Hinder i form av brist på och bristande utformning av balansstöd ska avhjälpas.", ""),
 ("Handrails", "Ledstänger bör sitta", "HIN", "10 §" + AR, "Ledstänger bör sitta på 0,9 meters höjd och vara lätta att gripa om.", ""),
 # width
 ("Clear width|Door width (parameter 9)|width", "öppningsmåttet för fri passage", "P12", "1 kap. 6 § 3", "3. öppningsmåttet för fri passage minst 0,80 meter.", "an opening measure for free passage, not a door-leaf width; dwellings have their own figure (6 § second para.)"),
 ("Clear width|width", "öppningsmåttet för fri passage", "P13", "2 kap. 1 § 3", "3. öppningsmåttet för fri passage minst 0,90 meter.", "the plot instrument states its own figure for the same named measure"),
 ("Clear width|Corridor width (parameter 4)|width", "Breddmått i kommunikationsutrymme", "P12", "2 kap. 2 §", "Breddmått i kommunikationsutrymme ska dessutom bestämmas utifrån utformningen och längden av utrymmet.", "width is to be determined from layout and length; no figure stated"),
 ("Clear width|width", "minst 1,3 m bred", "HIN", "6 §" + AR, "vara minst 1,3 m bred och ha avåkningsskydd", "ramp width"),
 # path of travel
 ("Accessible path of travel", "gångvägar", "P13", "2 kap. 2 §", "En tomt som ska vara tillgänglig och användbar, ska ha gångvägar mellan tillgängliga och användbara entréer till byggnader på tomten och andra tillgängliga och användbara målpunkter", "outdoor route on the plot; indoors the route is the 'kommunikationsutrymme'"),
 ("Accessible path of travel", "lätta att upptäcka och följa", "P13", "2 kap. 3 § 4", "4. vara lätta att upptäcka och följa.", "the route must be findable and followable, an orientation criterion"),
 ("Accessible path of travel|Corridor width (parameter 4)", "kommunikationsutrymme", "P12", "1 kap. 5 §", "kommunikationsutrymme: ett utrymme i byggnad som huvudsakligen används till förflyttning,", "defined term: any space mainly used for moving; corridor is an instance of it"),
 ("Corridor width (parameter 4)", "korridorer", "HIN", "4 §", "Exempel på kommunikationsutrymmen är korridorer, hallar, passager, ramper, trappor och kommunikationsytor i rum.", "'korridor' is an example of the defined class, never the regulated object"),
 ("Accessible path of travel", "Logiska ledstråk", "HIN", "7 §" + AR, "Logiska ledstråk som leder till och mellan målpunkterna bör anordnas till ledning för personer med nedsatt orienteringsförmåga.", "a guidance route, aimed at orientation, not a mobility path"),
 # drainage
 ("Drainage", "vattenavrinningen", "HIN", "12 §" + AR, "Tvärlutningen bör inte vara mer än vad som krävs för vattenavrinningen och inte överstiga 1:50", "drainage is the stated limit on cross-fall"),
 ("Drainage|Gratings", "avrinningsgaller", "HIN", "12 §" + AR, "bytas ut mot t.ex. avrinningsgaller eller ränndalar som utan svårighet kan passeras av personer i rullstol eller med rollator", "for Gratings: drainage grating that wheelchairs can pass"),
 ("Drainage", "golvbrunn i duschutrymme", "P9", "2 kap. 2 §", "Lutningen mot en golvbrunn i duschutrymme får inte vara så stor att det innebär risk att halka", "floor drain in a shower space"),
 # signage
 ("Clear signage", "orienterande skyltar", "P12", "3 kap. 4 §", "Om det finns orienterande skyltar ska de vara tillgängliga och användbara.", "conditional: no duty to sign, only a duty on signs that exist"),
 ("Clear signage", "orienterande skyltning", "HIN", "8 §", "Hinder i form av bristande utformning av orienterande skyltning ska avhjälpas.", ""),
 ("Clear signage", "lättbegripliga och lättlästa", "HIN", "14 §" + AR, "Skyltar bör vara lättbegripliga och lättlästa, ha ljushetskontrast", ""),
 # audio
 ("Audio accessibility and communication enhancement technologies", "system för ljudöverföring till hörhjälpmedel", "P12", "3 kap. 6 §", "I samlingssalar och receptioner ska system för ljudöverföring till hörhjälpmedel finnas", "generic system; no loop named in the binding text"),
 ("Audio accessibility and communication enhancement technologies", "teleslinga", "HIN", "8a §" + AR, "Receptioner bör utrustas med teleslinga eller någon annan teknisk lösning", "the loop is named only in advice"),
 ("Audio accessibility and communication enhancement technologies", "talad information", "HIN", "8 §" + AR, "samt i vissa fall med talad information och tydliga, lättförståeliga och välkända symboler", ""),
 ("Audio accessibility and communication enhancement technologies", "talförbindelse och ljud- och ljusanordning", "HIN", "11 §" + AR, "att komplettera system med talförbindelse och ljud- och ljusanordning så att personer med nedsatt orienteringsförmåga kan ta del av information", ""),
 # landings
 ("Level landings with clear space|Level landings with clear space and at regular intervals", "vilplan", "P12", "2 kap. 4 §", "Ett vilplan ska vara utformat med hänsyn till användningen. Längden på vilplanet ska minst medge plats för en rullstol som manövreras av hjälpare.", "length set by a wheelchair pushed by a helper; no interval stated (so 'at regular intervals' is PARTIAL)"),
 ("Level landings with clear space", "vilplanets längd", "P13", "2 kap. 4 §", "ska vilplanets längd minst medge plats för en rullstol som manövreras av en hjälpare", ""),
 ("Level landings with clear space", "ett plan, mellan en dörr och en nedåtgående trappa", "P9", "2 kap. 7 §", "Det ska finnas ett plan, mellan en dörr och en nedåtgående trappa, ramp eller enstaka trappsteg", "landing at a door before a descent; 'plan' here is a landing, elsewhere a storey"),
 # approach space
 ("Clear space for approach", "tillräcklig plats för att kunna öppna och stänga dörren från en rullstol", "P12", "2 kap. 3 §", "Vid en dörr som ska vara tillgänglig och användbar ska det finnas tillräcklig plats för att kunna öppna och stänga dörren från en rullstol.", "door approach space stated by function, no dimensions"),
 ("Clear space for approach", "förflyttning i sidled", "P12", "2 kap. 7 §", "för förflyttning i sidled mellan en toalettstol och en rullstol på båda sidor", "transfer space on both sides of the WC"),
 ("Clear space for approach|size", "planmåttet för rullstol", "P12", "1 kap. 6 § 1", "1. planmåttet för rullstol 0,70 x 1,30 meter,", "the reference wheelchair footprint is a governing measure"),
 ("Clear space for approach", "lätt kan nås från rullstol", "HIN", "6 §" + AR, "Manöverdon bör placeras så att de lätt kan nås från rullstol.", ""),
 # stairs
 ("Riser height and tread depth|riser|tread", "nedersta plansteget", "HIN", "7 §" + AR, "exempelvis genom att nedersta plansteget och framkanten på trappavsatsen vid översta sättsteget i varje trapplopp ges en ljushetskontrast på minst 0,40 enligt NCS", "'plansteg' (tread) and 'sättsteg' (riser) are named only as places to mark; no rise or going rule"),
 ("Riser height and tread depth|riser", "trappsteg med avvikande höjd", "P9", "2 kap. 8 §", "Krav på tydlig markering gäller även för trappsteg med avvikande höjd där ett sådant inte kan undvikas.", "a step of deviating height is to be marked, not prohibited"),
 ("No open riser|tread", "Öppningar mellan plansteg", "P9", "2 kap. 6 §", "Öppningar mellan plansteg i trappor ska vara högst 100 mm.", "DIFFERENT PURPOSE: limit so young children cannot fall through (6 § first sentence), not a foot-catch or cane rule"),
 ("Nosing design", "stegnos", "P9", "2 kap. 11 § 3", "mellan ett trappräckes underkant och trappstegens stegnos, ska vara högst 50 mm", "nosing named only as a reference point for a child-safety railing gap; no nosing design rule"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "varje trapplopps början och slut tydligt markeras", "P9", "2 kap. 8 §", "I en trappa ska varje trapplopps början och slut tydligt markeras.", "start and end of each flight, not every nosing; exempted in one- and two-dwelling houses and in flats (second para.)"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "kontrasterande mot omgivande ytor", "P9", "2 kap. 8 §", "Markeringarna ska vara kontrasterande mot omgivande ytor och utformade så att personer med nedsatt syn kan uppfatta nivåskillnaderna.", "contrast only; slip resistance of the marking is not stated"),
 ("Colour-contrasted and slip-resistant strip on nosing", "Trappor bör förses med kontrastmarkeringar", "HIN", "7 §" + AR, "Trappor bör förses med kontrastmarkeringar så att personer med nedsatt syn kan uppfatta nivåskillnaderna", ""),
 # threshold / level
 ("Level threshold", "Trösklar bör tas bort", "HIN", "6 §" + AR, "Trösklar bör tas bort om det är tekniskt möjligt", ""),
 ("Level threshold|level", "mindre nivåskillnader", "HIN", "6 §", "Fysiska hinder i form av mindre nivåskillnader, tunga dörrar och olämpligt placerade eller olämpligt utformade manöverdon ska avhjälpas.", ""),
 ("Level threshold|level", "nivåförändringar", "P9", "2 kap. 3 §", "Ytor som är avsedda att gå på ska vara utformade utan nivåförändringar", "qualified: only those 'som är oväntade eller svåra att upptäcka'"),
 ("level", "nivåskillnader", "P12", "2 kap. 2 §", "Kommunikationsutrymmen som har nivåskillnader ska förutom trappa även ha ramp eller hiss.", "'level' as difference in height"),
 ("level|number", "fler än tio plan", "P12", "2 kap. 5 §", "I en byggnad som har fler än tio plan ska byggnadens användare ha tillgång till mer än en personhiss.", "'plan' as storey; for 'number': a count of lifts"),
 ("level", "entréplanet", "P12", "2 kap. 12 §", "I en bostad som har flera plan ska minst entréplanet vara tillgängligt och användbart.", ""),
 # headroom
 ("Height clearance (if sheltered or parkade)|Headroom clearance (parameter 11)|clearance|Headroom and protruding objects|Headroom", "Den fria höjden", "P9", "2 kap. 25 §", "Den fria höjden ska vara minst 2,00 meter i utrymningspassager, trappor, dörrar och andra kommunikationsutrymmen.", "no parkade case; 'fri höjd' is the sub-heading under 'Skydd mot sammanstötning och klämning'"),
 ("Headroom and protruding objects|Protruding objects|Headroom clearance (parameter 11)", "Utskjutande byggnadsdelar", "P9", "2 kap. 26 § (heading)", "Utskjutande byggnadsdelar", ""),
 ("Headroom and protruding objects|Protruding objects", "lägre än 2,20 meter över en gångyta", "P9", "2 kap. 26 §", "Delar av byggnader och andra fasta anordningar som är placerade lägre än 2,20 meter över en gångyta ska vara utformade på ett sätt som begränsar risken för sammanstötning.", ""),
 ("Headroom and protruding objects|Protruding objects", "Utstickande byggnadsdelar", "HIN", "7 §" + AR, "Utstickande byggnadsdelar, exempelvis trappor eller kapphyllor, lägre än", "HIN uses 'utstickande', BFS 2024:9 'utskjutande' for the same object; HIN gives 2,00 m indoors (7 §) and 2,20 m outdoors (13 §)"),
 # edge protection
 ("Edge protection", "skydd som motverkar avåkning", "P9", "2 kap. 10 §", "Ramper ska dessutom ha skydd som motverkar avåkning.", "edge protection on ramps is anti-roll-off, separate from fall protection"),
 ("Edge protection", "avåkningsskydd", "HIN", "6 §" + AR, "vara minst 1,3 m bred och ha avåkningsskydd", ""),
 ("Edge protection", "skydd mot fall", "P9", "2 kap. 10 §", "där det finns särskild risk för personskador till följd av fall, ska ha skydd mot fall", ""),
 # tactile
 ("Tactile attention indicators (truncated domes)", "varningsmarkering", "HIN", "13 §", "Hinder i form av bristande kontrastmarkering och varningsmarkering ska avhjälpas.", "warning marking as a named obstacle class; no dome geometry"),
 ("Tactile attention indicators (truncated domes)", "tydligt kännbara plattor i asfaltyta", "HIN", "13 §" + AR, "t.ex. tydligt kännbara plattor i asfaltyta", "the only tactile surface element named; truncated domes not named"),
 ("Tactile attention indicators (truncated domes)", "taktil kontrast", "HIN", "7 §" + AR, "Kontrastlinjer i golv bör anordnas med både ljushetskontrast och taktil kontrast för personer med kraftigare nedsatt syn.", ""),
 # slope
 ("Slope|Ramp gradient (parameter 3)|gradient", "ska luta högst 1:12", "P12", "2 kap. 4 §", "En ramp, som är till för att uppfylla kraven enligt 1 § och 2 § andra stycket, ska luta högst 1:12.", "verb 'luta' (to slope); ratio notation, not %"),
 ("Slope|gradient", "luta högst 1:12", "P13", "2 kap. 3 § 3", "3. luta högst 1:12, och", "walkways on a plot"),
 ("Slope|gradient", "lutningen inte vara brantare än 1:12", "HIN", "6 §" + AR, "Även om rampen är kort bör lutningen inte vara brantare än 1:12", ""),
 ("Slope", "Tvärlutningen", "HIN", "12 §" + AR, "Tvärlutningen bör inte vara mer än vad som krävs för vattenavrinningen och inte överstiga 1:50", "cross-fall has its own word"),
 ("Slope", "Lutningen i längs- och sidled", "HIN", "17 §" + AR, "Lutningen i längs- och sidled bör inte vara mer än vad som krävs för vattenavrinningen och inte överstiga 1:50.", ""),
 ("Ramp run length (parameter 12)", "Även om rampen är kort", "HIN", "6 §" + AR, "Även om rampen är kort bör lutningen inte vara brantare än 1:12", "PARTIAL: no run-length limit anywhere; a short ramp is expressly not relieved of the gradient"),
 # sanitary / kitchen
 ("Sink faucet is easy to use or automatic", "förväxlar varmvatten och kallvatten", "P9", "2 kap. 33 §", "En anordning för att reglera tappvarmvatten ska vara utformad så att risken för personskador orsakade av att någon förväxlar varmvatten och kallvatten begränsas.", "PARTIAL: hot/cold confusion only; ease of operation and sensor taps not treated"),
 ("Enclosures", "duschutrymme", "P9", "2 kap. 2 §", "Lutningen mot en golvbrunn i duschutrymme får inte vara så stor att det innebär risk att halka med hänsyn till golvmaterialet och duschutrymmets avsedda användning.", "PARTIAL: the shower space is named only for floor fall; no enclosure dimensions"),
 # controls / hardware
 ("Outlets and switches are at accessible heights|Accessible controls", "manöverdon", "HIN", "6 §" + AR, "Olämpligt placerade porttelefoner samt manöverdon till exempelvis dörr-", "BROADER: 'manöverdon' is one class for all operating devices; outlets and light switches are not named"),
 ("Accessible controls", "manöverpaneler", "HIN", "6 §" + AR, "Olämpligt placerade manöverpaneler i och utanför hissar bör flyttas", "lift panels; points to SS-EN 81-70"),
 ("Accessible controls", "knappsatser", "HIN", "11 §" + AR, "för att personer med nedsatt syn ska kunna använda knappsatser där siffer-", "quote ends at a line-end hyphen in the text"),
 ("Accessible door hardware", "handtag och lås", "HIN", "6 §" + AR, "Olämpligt utformade handtag och lås bör bytas mot sådana som kan hanteras även av personer med nedsatt styrka eller nedsatt grip- eller precisionsförmåga.", ""),
 ("Accessible door hardware", "automatisk dörröppnare", "HIN", "6 §" + AR, "Dörrar med dörrstängare bör förses med automatisk dörröppnare.", ""),
 ("Accessible door hardware", "Dörrar som ska vara tillgängliga och användbara", "P12", "3 kap. 3 §", "Dörrar som ska vara tillgängliga och användbara ska vara projekterade och utförda så att de kan användas av", "door usability for reduced mobility AND reduced orientation; no hardware named"),
 # force
 ("force|Operating force (parameter 6)", "tunga dörrar", "HIN", "6 §", "Fysiska hinder i form av mindre nivåskillnader, tunga dörrar och olämpligt placerade", "PARTIAL: a heavy door is an obstacle; no opening-force quantity; remedy is an automatic opener"),
 ("force", "nedsatt styrka", "HIN", "6 §" + AR, "kan hanteras även av personer med nedsatt styrka", "force framed as the user's reduced strength"),
 # height
 ("height", "höjd", "HIN", "10 §" + AR, "Ledstänger bör sitta på 0,9 meters höjd", ""),
 ("height", "ha sådan höjd", "P9", "2 kap. 11 §", "Ett skydd mot fall ska vara utformat och ha sådan höjd att det med hänsyn till ytans avsedda användning och fallhöjden begränsar risken", ""),
 ("height", "i höjd- och sidled", "HIN", "6 §" + AR, "Manöverdon till dörröppnare bör i höjd- och sidled placeras", ""),
 # clearance
 ("clearance", "Fritt mått", "P9", "2 kap. 11 § 3", "Fritt mått mellan ett balkongräckes underkant och balkonggolv", "a clear gap, for child safety"),
 ("clearance", "fritt utrymme", "P12", "2 kap. 5 §", "Hissen ska ha ett fritt utrymme med en kortsida på minst", ""),
 ("clearance", "fritt utrymme för hjälp", "P12", "2 kap. 10 §", "I en bostad ska det gå att ordna fritt utrymme för hjälp, längs båda långsidorna samt vid fotändan av minst en säng", "clearance for an assistant beside a bed"),
 # number / size / capacity / distance
 ("number", "minst ett vara tillgängligt och användbart", "P12", "2 kap. 7 §", "Om det finns toalettrum för allmänheten i en publik lokal, ska minst ett vara tillgängligt och användbart.", ""),
 ("size|Turning circle (parameter 5)", "vändmåttet av en cirkel med diametern", "P12", "1 kap. 6 § 2", "2. vändmåttet av en cirkel med diametern 1,50 meter, och", "the turning measure is a circle; dwellings have a smaller one (second para.)"),
 ("Turning circle (parameter 5)", "Plats ska finnas för att vända med en rullstol", "P12", "2 kap. 7 §", "Plats ska finnas för att vända med en rullstol", ""),
 ("size", "tillräckligt stort", "P9", "2 kap. 7 §", "Planet ska vara tillräckligt stort med hänsyn till trappans eller rampens utformning", ""),
 ("capacity", "ska minst rymma en person som använder rullstol och en hjälpare", "P12", "2 kap. 5 §", "ska minst rymma en person som använder rullstol och en hjälpare", "lift capacity stated in persons, not mass"),
 ("distance", "inom 25 meters gångavstånd", "P13", "2 kap. 5 §", "minst en angöringsplats för fordon inom 25 meters gångavstånd från en tillgänglig och användbar entré", "DIFFERENT SENSE from the English 'distance markers': walking distance to a set-down place"),
 ("distance", "läsavståndet", "HIN", "8 §" + AR, "Textstorleken bör vara anpassad efter läsavståndet", ""),
 # contrast
 ("LRV contrast (parameter 8)", "ljushetskontrast på minst 0,40 enligt NCS", "HIN", "7 §" + AR, "En ljushetskontrast på minst 0,40 enligt NCS (Natural Colour System) ökar avsevärt möjligheten för personer med nedsatt syn att uppfatta markeringen.", "contrast IS quantified, but as NCS lightness contrast, not LRV; advice tier only"),
 ("LRV contrast (parameter 8)", "kontrastmarkering", "HIN", "7 §", "Hinder i form av bristande kontrastmarkering och bristande varnings-", "quote ends at a line-end hyphen"),
 ("LRV contrast (parameter 8)", "kontrasterande mot omgivande ytor", "P9", "2 kap. 13 §", "I publika lokaler och trapphus i flerbostadshus ska ledstängerna dessutom vara kontrasterande mot omgivande ytor.", "binding text: contrast unquantified"),
 # reverberation
 ("Reverberation time (parameter 7)", "god hörbarhet, god taluppfattbarhet och god orienterbarhet", "P12", "3 kap. 6 §", "ska ljudmiljön vara projekterad och utförd för god hörbarhet, god taluppfattbarhet och god orienterbarhet", "BROADER: the sound environment is regulated by three qualities; no reverberation term"),
 ("Reverberation time (parameter 7)", "rumsakustiken", "HIN", "8a §" + AR, "Dålig hörbarhet bör förbättras genom att anpassa rumsakustiken till lokalens avsedda användning, exempelvis genom komplettering med", ""),
 # B651-only headings
 ("Gratings", "skrapgaller", "HIN", "6 §" + AR, "Dörrmattor och skrapgaller, som är tunga att passera eller medför snub-", "entrance scraper grating; quote ends at line-end hyphen"),
 ("Gratings", "lock och galler på brunnar", "P13", "5 kap. 6 §", "Skydd i form av lock och galler på brunnar och fasta behållare ska", "child-safety sense, not wheel or cane passage"),
 ("Bollards", "Stolpar i gångbanor", "HIN", "13 §" + AR, "Stolpar i gångbanor, fallkanter och andra detaljer bör kontrastmarkeras", "posts in footways; contrast marking only"),
 ("Landscaping elements|Vegetation", "gräskanter", "HIN", "13 §" + AR, "Naturliga ledytor som gräskanter, murar, staket, kanter och fasader kan kompletteras med konstgjorda ledytor till sammanhängande ledstråk.", "DIFFERENT SENSE: landscape edges as natural guidance surfaces, not landscape hazards"),
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
 "Speed bumps", "Bollards", "Landscaping elements", "Flower or shrub planters", "Vegetation", "Guy wires", "Scaffolding",
 "Gradation limits",
]
SRC = [('catalogue 2.1', 32), ('catalogue 2.2', 18), ('base_parameters', 10), ('b651-headings RHFAC-does-not-name', 15)]
ALIAS = {"slope": "Slope"}  # the 2.2 word 'slope' counts the 2.1 concept's observations
PARTIAL = {  # concept -> why the Swedish match is not the English concept (ours)
 "Seating": "DIFFERENT SENSE: audience places only; no rest seating",
 "Riser height and tread depth": "PARTIAL: tread and riser named as places to mark; no rise/going rule",
 "Nosing design": "PARTIAL: nosing only a reference point for a railing gap",
 "No open riser": "DIFFERENT PURPOSE: child fall-through limit",
 "Colour-contrasted and slip-resistant strip on nosing": "PARTIAL: contrast at start and end of flight; slip resistance not stated",
 "Colour-contrasted and slip-resistant strip": "PARTIAL: contrast only",
 "Level landings with clear space and at regular intervals": "PARTIAL: no interval",
 "Sink faucet is easy to use or automatic": "PARTIAL: hot/cold confusion only",
 "Outlets and switches are at accessible heights": "BROADER: 'manöverdon' only",
 "force": "PARTIAL: heavy door and user strength; no force quantity",
 "Operating force (parameter 6)": "PARTIAL: 'tunga dörrar', no force quantity",
 "distance": "DIFFERENT SENSE: walking and reading distance",
 "lighting levels": "PARTIAL: 'stark och jämn', no illuminance",
 "Reverberation time (parameter 7)": "BROADER: ljudmiljö / rumsakustik; term absent",
 "Ramp run length (parameter 12)": "PARTIAL: no run-length rule",
 "Enclosures": "PARTIAL: shower space named for floor fall only",
 "Gratings": "PARTIAL: drainage and scraper gratings; no opening-size rule",
 "Landscaping elements": "DIFFERENT SENSE: guidance edges",
 "Vegetation": "DIFFERENT SENSE: grass edges as guidance",
 "Bollards": "PARTIAL: posts, contrast only",
}
ABSENT = {
 "Shelter": "no weather shelter or canopy; 'skärmtak' 0, 'väder' 0 in all four texts; nearest is P9 2 kap. 24 § protection from falling ice and snow at entrances, a different purpose",
 "Microwave mounting height accessible and safe": "'mikrov' 0; P12 2 kap. 8 § and 3 kap. 8 § require space and usability of kitchen fittings, no appliance",
 "Accessible lockers": "'skåp' 0; 'förvaring' occurs once (P12 1 kap. 5 §) as a dwelling function, a different sense",
 "depth": "'djup' 0 in all four texts",
 "time": "'tid' hits are 'tidigare', 'tidpunkt' etc.; no duration quantity (door hold-open, timed lighting) in any text",
 "volume": "TEXT MATCH, NOT SENSE: 'volym' occurs only in 'proportioner, form och volym' (P12 4 kap. 6 §, P9 3 kap. 4 §), building massing; no sound volume",
 "ratio": "no proportional provision; counts are 'minst ett' / 'mer än en'",
 "Colour temperature (parameter 10)": "'färgtemp' 0, 'kelvin' 0",
 "Spouts": "no drinking fountain; 'dricks' 0",
 "Lavatories": "'tvättställ' 0; washbasins are inside 'fast inredning och utrustning' of the 'rum för personhygien', never named",
 "Speed bumps": "'farthinder' 0",
 "Flower or shrub planters": "no planters; 'växt' 0",
 "Guy wires": "no stay wires",
 "Scaffolding": "'byggnadsställ' 0; 'byggarbetsplatsen' occurs only for product reception control",
 "Gradation limits": "no trails; HIN 12 § treats public-place ramps only",
}

# Reverse harvest: (phrase verbatim, kind, instrument, locator, quote verbatim, gloss — OURS)
REV = [
 ("nedsatt rörelse- eller orienteringsförmåga", "population carve", "P12", "title / 1 kap. 1 §", "utformningskrav avseende byggnaders tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga", "the law's two-way carve: reduced mobility or reduced orientation capacity"),
 ("Nedsatt orienteringsförmåga kan exempelvis vara nedsatt syn, hörsel", "population carve", "HIN", "2 §" + AR, "Nedsatt orienteringsförmåga kan exempelvis vara nedsatt syn, hörsel", "orientation capacity spans sight, hearing and cognition"),
 ("nedsatt funktion i armar, händer, bål och ben liksom dålig balans", "population carve", "HIN", "2 §" + AR, "Nedsatt rörelseförmåga kan exempelvis vara nedsatt funktion i armar, händer, bål och ben liksom dålig balans.", ""),
 ("rullstol, rollator eller käpp", "mobility devices named", "HIN", "2 §" + AR, "Personer med nedsatt rörelse- förmåga kan behöva använda t.ex. rullstol, rollator eller käpp.", ""),
 ("tillgänglig och användbar", "defined term (paired criterion)", "P12", "1 kap. 5 §", "tillgänglig och användbar: tillgänglig och användbar för personer med nedsatt rörelse- eller orienteringsförmåga, och", "'accessible AND usable' is the unit of every requirement"),
 ("publik lokal", "defined category", "P12", "1 kap. 5 §", "publik lokal: en lokal dit allmänheten har tillträde,", ""),
 ("boendeenhet", "defined term", "P12", "1 kap. 5 §", "boendeenhet: del av en bostad som är upplåten för enskilt bruk i bostäder där vissa bostadsfunktioner delas,", "unit in shared housing"),
 ("bostadsfunktioner", "defined term", "P12", "1 kap. 5 §", "bostadsfunktioner: funktionerna sömn och vila, samvaro, matlagning, måltider, hygien och förvaring", "dwelling functions; rooms are carved by function"),
 ("är följande mått dimensionerande", "drafting device (governing dimensions)", "P12", "1 kap. 6 §", "är följande mått dimensionerande", "three governing measures stated once and reused by every clause"),
 ("I enskilda bostäder är dock följande mått dimensionerande", "differentiated regime", "P12", "1 kap. 6 §", "I enskilda bostäder är dock följande mått dimensionerande", "a smaller governing set inside individual dwellings"),
 ("Utformningskrav vid uppförande av nya byggnader", "drafting structure", "P12", "2 kap. (heading)", "2 kap. Utformningskrav vid uppförande av nya byggnader", "design requirements (layout) are a separate chapter from technical-property requirements"),
 ("Tekniska egenskapskrav", "drafting structure", "P12", "3 kap. (heading)", "3 kap. Tekniska egenskapskrav vid uppförande av nya byggnader", ""),
 ("Mindre avvikelse", "compliance route", "P12", "1 kap. 3 §", "Mindre avvikelse får göras från föreskrifterna i denna författning i enskilda fall om", "minor deviation, documented"),
 ("provning, mätning eller besiktning", "verification method", "P12", "1 kap. 16 §", "Vid kontroll i den färdiga byggnaden ska kontroll göras genom provning, mätning eller besiktning.", ""),
 ("Huvudentréer", "element", "P12", "2 kap. 1 §", "Huvudentréer till en byggnad ska vara placerade och utformade så att de är tillgängliga och användbara.", ""),
 ("tydligt uppfattbara", "performance criterion", "P12", "3 kap. 1 §", "Tillgängliga och användbara entréer ska vara tydligt uppfattbara.", "entrance must be clearly perceivable"),
 ("ramp eller hiss", "rule (level change)", "P12", "2 kap. 2 §", "ska förutom trappa även ha ramp eller hiss", "every level change needs a stair plus a ramp or lift"),
 ("Om nivåskillnaden är större än 1 meter ska det finnas en hiss", "rule (lift threshold)", "P12", "2 kap. 2 §", "Om nivåskillnaden är större än 1 meter ska det finnas en hiss.", ""),
 ("en rullstol som manövreras av hjälpare", "reference body", "P12", "2 kap. 4 §", "plats för en rullstol som manövreras av hjälpare", "an assisted wheelchair as a design body"),
 ("personhiss", "element", "P12", "2 kap. 5 §", "mer än en personhiss", ""),
 ("samlingslokal", "space type", "P12", "2 kap. 6 §", "En samlingslokal i en publik lokal får utformas", ""),
 ("toalettrum för allmänheten", "room", "P12", "2 kap. 7 §", "Om det finns toalettrum för allmänheten i en publik lokal", "conditional duty: only if public toilets exist"),
 ("utrymmet för matlagning", "room (by function)", "P12", "2 kap. 8 §", "I utrymmet för matlagning i en bostad ska det finnas plats för fast inredning och utrustning", ""),
 ("rum för personhygien", "room (by function)", "P12", "2 kap. 9 §", "Minst ett rum för personhygien i en bostad ska vara tillgängligt och användbart", ""),
 ("fotändan av minst en säng", "element", "P12", "2 kap. 10 §", "vid fotändan av minst en säng", ""),
 ("studentbostäder", "building typology (exempted)", "P12", "2 kap. 10 §", "Första och andra styckena gäller inte för studentbostäder.", ""),
 ("takterrass", "element", "P12", "2 kap. 11 §", "För en takterrass i en bostad räcker det att det går att ordna en tillgänglig och användbar ramp", "'det går att ordna' = can be arranged later; an adaptability route"),
 ("det går att ordna", "compliance route (arrangeable later)", "P12", "2 kap. 1 §", "För en- och tvåbostadshus räcker det att det går att ordna tillgängliga och användbara ramper", ""),
 ("begränsad dimensionering", "concept", "P12", "2 kap. 12 §", "får bostadsfunktionerna på entréplanet ha begränsad dimensionering", ""),
 ("hitta fram till målpunkter", "performance criterion (wayfinding)", "P12", "3 kap. 2 §", "Personer med nedsatt orienteringsförmåga ska kunna hitta fram till målpunkter i byggnaden.", ""),
 ("Transport med sjukbår", "rule", "P12", "3 kap. 2 §", "Transport med sjukbår ska kunna ske från varje bostad.", "stretcher transport from every dwelling"),
 ("ljudmiljön", "concept", "P12", "3 kap. 6 §", "där ljudmiljön är väsentlig för att personer med nedsatt orienteringsförmåga ska kunna ta del av betydelsefull information", ""),
 ("samlingssalar och receptioner", "space types", "P12", "3 kap. 6 §", "I samlingssalar och receptioner ska system för ljudöverföring till hörhjälpmedel finnas", ""),
 ("Anpassning vid ändring av byggnader", "compliance route (alteration)", "P12", "4 kap. 1 § (heading)", "Anpassning vid ändring av byggnader", "seven grounds on which requirements may be adapted"),
 ("kostnaden är oskäligt hög i förhållande till den förväntade nyttan", "adaptation ground", "P12", "4 kap. 1 § 5", "kostnaden är oskäligt hög i förhållande till den förväntade nyttan", ""),
 ("Försämring av tillgängligheten och användbarheten", "rule (non-deterioration)", "P12", "4 kap. 2 §", "Försämring av tillgängligheten och användbarheten får endast ske om", ""),
 ("Ändrad användning", "concept", "P12", "4 kap. 3 §", "Ändrad användning", ""),
 ("kan göras tillgänglig och användbar i efterhand", "compliance route (deferred)", "P12", "4 kap. 4 § 3", "nivåskillnaden utan svårighet kan göras tillgänglig och användbar i efterhand", ""),
 ("varsamhet", "heritage constraint", "P12", "4 kap. 6 §", "Vid en bedömning om kravet på varsamhet är uppfyllt", ""),
 ("förvanskning", "heritage constraint", "P12", "4 kap. 7 §", "För att en åtgärd inte ska anses medföra en förvanskning av en särskilt värdefull byggnad", ""),
 ("enkelt avhjälpta hinder", "legal category (retroactive duty)", "HIN", "title / 5 §", "avhjälpande av enkelt avhjälpta hinder", "obstacles in existing public premises that must be removed when easy"),
 ("praktiska och ekonomiska förutsättningarna", "test", "HIN", "5 §", "så snart det inte är orimligt med hänsyn till de praktiska och ekonomiska förutsättningarna", ""),
 ("fastighetsägaren, lokalhållaren eller näringsidkaren", "duty-holders", "HIN", "5 §", "orimligt betungande för fastighetsägaren, lokalhållaren eller näringsidkaren.", ""),
 ("Allmänt råd", "drafting structure (binding vs advice)", "HIN", "3 §", "De allmänna råden föregås av texten Allmänt Råd och är tryckta med mindre och indragen text.", "every HIN quantity is in non-binding advice; the binding text names only obstacle classes"),
 ("Plan- och byggtermer 1994, TNC 95", "terminology source", "HIN", "4 §", "har den betydelse som anges i Terminologicentrums publikation Plan- och byggtermer 1994, TNC 95.", "the instrument names its own term bank"),
 ("Dörrmattor", "element", "HIN", "6 §" + AR, "Dörrmattor och skrapgaller", ""),
 ("porttelefoner", "element", "HIN", "6 §" + AR, "Olämpligt placerade porttelefoner", ""),
 ("träffas av dörrbladet", "hazard", "HIN", "6 §" + AR, "kan använda dem utan att träffas av dörrbladet", ""),
 ("i ogynnsammaste läge", "geometric reference", "HIN", "6 §" + AR, "dörrblads framkant eller annat hinder i ogynnsammaste läge", ""),
 ("säkerhetssensorer", "element", "HIN", "6 §" + AR, "dörrar förses med säkerhetssensorer", ""),
 ("Utgångsknappen", "element", "HIN", "6 §" + AR, "Utgångsknappen bör ha form och ljushet som avviker mot omgivningen.", "lift exit button"),
 ("grip- eller precisionsförmåga", "user capacity", "HIN", "6 §" + AR, "nedsatt grip- eller precisionsförmåga", ""),
 ("Viktiga målpunkter", "concept", "HIN", "7 §" + AR, "Viktiga målpunkter, t.ex. entrédörrar, manöverdon till automatiska", "a set of priority destinations to be contrast-marked"),
 ("ljushetskontrast", "quantity", "HIN", "7 §" + AR, "kan uppnås med avvikande material och ljushetskontrast.", "lightness contrast"),
 ("NCS (Natural Colour System)", "measurement system", "HIN", "7 §" + AR, "enligt NCS (Natural Colour System)", ""),
 ("Kontrastlinjer i golv", "element", "HIN", "7 §" + AR, "Kontrastlinjer i golv bör anordnas", ""),
 ("logiska färgsystem", "technique", "HIN", "7 §" + AR, "För personer med nedsatt kognitiv förmåga underlättas orienteringen av logiska färgsystem.", ""),
 ("i ögonhöjd för både stående och sittande personer", "use condition", "HIN", "7 §" + AR, "placeras i ögonhöjd för både stående och sittande personer", ""),
 ("teknikkäpp", "device", "HIN", "7 §" + AR, "personer med nedsatt syn som använder teknikkäpp", "long cane"),
 ("kapphyllor", "element", "HIN", "7 §" + AR, "exempelvis trappor eller kapphyllor", ""),
 ("upphöjd relief eller punktskrift", "technique", "HIN", "8 §" + AR, "bokstäver i antingen upphöjd relief eller punktskrift eller båda", ""),
 ("Elektronisk skyltning", "element", "HIN", "8 §" + AR, "Elektronisk skyltning bör anpassas så att personer med nedsatt orienteringsförmåga kan uppfatta och förstå den.", ""),
 ("ytan bör inte ge upphov till reflexer", "hazard", "HIN", "8 §" + AR, "ytan bör inte ge upphov till reflexer", ""),
 ("brister i ljudmiljön", "obstacle class", "HIN", "8a §", "Hinder i form av brister i ljudmiljön ska avhjälpas.", ""),
 ("ljudabsorbenter", "element", "HIN", "8a §" + AR, "ljudabsorbenter", ""),
 ("Störande bakgrundsljud", "hazard", "HIN", "8a §" + AR, "Störande bakgrundsljud från tekniska installationer, hissar eller trafik kan behöva avskärmas.", ""),
 ("läsa teckenspråk och läsa på läppar", "use condition (lighting)", "HIN", "9 §" + AR, "läsa teckenspråk och läsa på läppar", "lighting for sign language and lip-reading"),
 ("motverka bländning", "technique", "HIN", "9 §" + AR, "bör kunna skärmas av för att motverka bländning", ""),
 ("kontrasten i ljushet mellan angränsande utrymmen eller mellan ute och inne", "hazard (adaptation)", "HIN", "9 §" + AR, "att kontrasten i ljushet mellan angränsande utrymmen eller mellan ute och inne inte är för stor", ""),
 ("förbi infästningarna", "technique", "HIN", "10 §" + AR, "Det bör vara möjligt att hålla i ledstången även förbi infästningarna.", ""),
 ("5:an förses med en taktilt märkbar punkt", "technique", "HIN", "11 §" + AR, "att 5:an förses med en taktilt märkbar punkt", ""),
 ("hygienrum", "room", "HIN", "11 §" + AR, "I hygienrum avsett för personer med nedsatt rörelseförmåga", ""),
 ("Bristfällig larmutrustning", "element", "HIN", "11 §" + AR, "Bristfällig larmutrustning bör komp-", "quote ends at line-end hyphen"),
 ("svårforcerade ränndalar och trottoarkanter", "hazard", "HIN", "12 §", "svårforcerade ränndalar och trottoarkanter ska avhjälpas", ""),
 ("avfasas till 0-", "technique", "HIN", "12 §" + AR, "bör avfasas till 0-", "kerb chamfered to zero; text breaks '0-kant' over a line"),
 ("parkeringsplatser för rörelsehindrade med särskilt tillstånd", "legal category", "HIN", "12 §" + AR, "parkeringsplatser för rörelsehindrade med särskilt tillstånd", ""),
 ("kantstenen ligga kvar", "technique", "HIN", "12 §" + AR, "Vid sidan av avfasningen bör kantstenen ligga kvar så att personer med nedsatt syn kan ta ut riktningen över gatan.", "keep a kerb beside the drop for direction-finding"),
 ("konstgjorda ledytor", "element", "HIN", "13 §" + AR, "kan kompletteras med konstgjorda ledytor till sammanhängande ledstråk", ""),
 ("upphöjda gångpassager", "element", "HIN", "13 §" + AR, "upphöjda gångpassager över gator", ""),
 ("Fasta hinder i gångytor", "hazard", "HIN", "13 §" + AR, "Fasta hinder i gångytor bör, om det inte är möjligt att flytta dem bort från gångytan, tydligt markeras visuellt", ""),
 ("Oskyddade glasytor", "element", "HIN", "13 §" + AR, "Oskyddade glasytor bör markeras.", ""),
 ("ta in och ut rullstol baktill på fordonet", "use condition", "HIN", "17 §" + AR, "Vissa platser kan göras extra långa för att ta in och ut rullstol baktill på fordonet.", ""),
 ("lekplatsers utformning eller utrustning", "obstacle class", "HIN", "18 §", "Hinder i form av brister i lekplatsers utformning eller utrustning ska avhjälpas.", ""),
 ("föräldrar med nedsatt rörelse- eller", "user", "HIN", "18 §" + AR, "för föräldrar med nedsatt rörelse- eller", "disabled parents as users of a playground"),
 ("Ljusförhållanden", "sub-heading category", "P9", "2 kap. (sub-heading before 1 §)", "Ljusförhållanden", ""),
 ("oväntade eller svåra att upptäcka", "hazard criterion", "P9", "2 kap. 3 §", "som är oväntade eller svåra att upptäcka", "a level change is a hazard when unexpected, not by size"),
 ("väta, spill eller nedisning", "conditions", "P9", "2 kap. 2 §", "på grund av till exempel lutning, väta, spill eller nedisning", ""),
 ("utrymme där yngre barn kan vistas", "defined category", "P9", "1 kap. 5 §", "utrymme där yngre barn kan vistas: rum, delar av rum eller utrymmen där det med hänsyn till den avsedda användningen kan förväntas att barn som är yngre än sex år vistas utan ständig tillsyn av vuxna", ""),
 ("utrymningspassage", "space type", "P9", "2 kap. 7 §", "I utrymningspassage ska avståndet mellan dörr och trappa eller ramp vara minst 0,8 meter.", ""),
 ("loftgångar", "element", "P9", "2 kap. 10 §", "Trappor, ramper, balkonger, loftgångar, takterrasser och andra vistelseytor", ""),
 ("dynamisk påverkan av en människa", "performance criterion", "P9", "2 kap. 11 §", "Skyddet ska tåla dynamisk påverkan av en människa.", ""),
 ("ger stöd innan man påbörjar och när man avslutar förflyttningen", "technique (handrail extension)", "P9", "2 kap. 13 § 3", "vara utformade så att de ger stöd innan man påbörjar och när man avslutar förflyttningen i trappan eller rampen", "handrail extension stated as function, no length"),
 ("Skydd mot sammanstötning och klämning", "sub-heading category", "P9", "2 kap. (sub-heading before 25 §)", "Skydd mot sammanstötning och klämning", ""),
 ("Markering av glas", "element", "P9", "2 kap. 29 § (heading)", "Markering av glas", ""),
 ("synliga för både stående och sittande personer", "use condition", "P9", "2 kap. 29 §", "som är synliga för både stående och sittande personer", ""),
 ("skållningsskador", "hazard", "P9", "2 kap. 33 §", "Om det finns särskild risk för skållningsskador", ""),
 ("lätta att öppna inifrån", "rule", "P9", "2 kap. 36 §", "ska dörrar, luckor och lock vara lätta att öppna inifrån", ""),
 ("angöringsplats", "defined term", "P13", "1 kap. 5 §", "angöringsplats: en plats för kortare tillfällig uppställning av bil eller annat fordon för på- och avstigning eller i- och urlastning,", "set-down place"),
 ("självständigt använda parkeringsplatsen", "performance criterion", "P13", "2 kap. 6 §", "självständigt använda parkeringsplatsen", "independent use"),
 ("stötdämpande", "property", "P13", "5 kap. 2 §", "ska vara stötdämpande", "impact-absorbing play surfacing"),
]

def write_rev():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, norm(q) in TXT[ins], file=sys.stderr)
            w.writerow([ph, kind, 'sv', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    print('reverse-harvest', len(REV), 'verified', len(REV) - bad)
    return bad

def main():
    bad = chain() + write_rev(); rows = []
    for c, ph, ins, loc, q, note in OBS:
        for x in c.split('|'):
            if x not in REGISTER: bad += 1; print('UNKNOWN CONCEPT', x, file=sys.stderr)
        ok_q = norm(q) in TXT[ins]
        ok_p = norm(ph).lower() in norm(q).lower()
        if not (ok_q and ok_p): bad += 1; print('FAIL', ins, loc, ph, ok_q, ok_p, file=sys.stderr)
        rows.append([c, ph, 'sv', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok_q and ok_p else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    bounds = []; n = 0
    for s, k in SRC: bounds.append((n + k, s)); n += k
    assert n == len(REGISTER), (n, len(REGISTER))
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = next(s for b, s in bounds if i < b)
            hit = [r for r in rows if c in r[0].split('|') or (c in ALIAS and ALIAS[c] in r[0].split('|'))]
            if hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                if c not in ABSENT: bad += 1; print('NO ABSENT NOTE', c, file=sys.stderr)
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE: check')])
    for c in list(PARTIAL) + list(ABSENT):
        if c not in REGISTER: bad += 1; print('STRAY KEY', c, file=sys.stderr)
    print('observations', len(rows), 'failures (obs+rev+checks)', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
