"""Build observations / coverage / reverse-harvest TSVs for the DA/DK terminology pass (adapted from the FR/FR
pilot's build.py), verifying every quote (after whitespace collapse) in the saved extracted text, and every
phrase inside its quote. Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/build.py
Exits 1 if any quote or phrase fails to verify. Writes only the TSVs in this folder; reads data/guidebook.db
read-only for the held-alias report."""
import re, sys, csv, os, glob, sqlite3
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK'
T = D + '/text/'
# BR18 text files: the chapter index pages (headings) plus every ?ajax=1 section fragment of kap. 2, 6, 7, 9, 10, 16, 17, 18, 20
BR_FILES = ['6c228b01d23c4517', '05e23126b35be89f', '8b2fdb936be27189', 'a8c8769744993cac', 'e5dfce53bfa6fa42',
            '68b3b28c9736e02b', '5813d1f4a1f5d917', '36e844f67c2dbd5c', '77e8076657c406cf',   # kap. 2
            '5a8cacbf0dc6e4f2', 'd97b42c3caf04ba2',                                            # kap. 6
            '9b4f7e2af0b13132',                                                                # kap. 7
            '5ffa9f2473ab1f15', '3faf6bd58bd81583', 'e78b61f5b4b89665', '5d525b6233ea1586', 'a62e0887da12d2c1',
            'f5c949abd9025711', '55ce31c9fb79ab4e', 'd3576f2697d79970',                        # kap. 9
            'd2cba1d408bcc2b4',                                                                # kap. 10
            'bc233dcdc36f4314', 'e203d43b07cebf50', 'c8e1a71fe2d58441', 'fa87f68a73391845', 'b3da4a49d4c3843e',  # kap. 16
            '90e00feba7726ff3', '4ecf3d70cf4ac1ab', 'ac0e113f58f47563',                        # kap. 17
            '4084ec00c7997181', '758dc349820a8cd4', 'fc035b853a079d8f', '84e8a6d2817dfbc9',    # kap. 18
            'c6535628a027b9a7', '1fd4e81e407d5f6f', '6338142f9058c6b9']                        # kap. 20
INST = {
 'BR': ("Bygningsreglement 2018 (BR18), 'BR18 (Aktuelt)' as published on bygningsreglementet.dk", BR_FILES),
 'VB': ("Vejledning til brugerbegreb (BR18 guidance, kap. 2)", ['029aff4d6226c18d']),
 'VT': ("Bygningsreglementets vejledning om tilgængelighed ved transportable konstruktioner, 1. udgave, 3. september 2020", ['ebea177522213742']),
 'VA': ("Bygningsreglementets vejledning om adgangsforhold (one-page pointer)", ['b2bfd0d4e6f685f0']),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: {f: norm(open(T + f + '.txt', encoding='utf-8').read()) for f in v[1]} for k, v in INST.items()}
ALL = ' '.join(t for d in TXT.values() for t in d.values())

def where(ins, q):
    return [f for f, t in TXT[ins].items() if norm(q) in t]

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note OURS)
OBS = [
 ("Well-illuminated (if site expected to be lit)|lighting levels", "belyses", "BR", "kap. 2, § 49, stk. 2, nr. 1", "Adgangs- og tilkørselsarealerne skal belyses. Trapper og ramper skal belyses stærkest.", "graded, not quantified: stairs and ramps lit 'most strongly'"),
 ("Well illuminated (if required for expected usage)", "tilstrækkelig elektrisk belysning i forhold til anvendelsen", "BR", "kap. 18, § 377", "Det skal sikres, at der er tilstrækkeligt dagslys og udsyn samt tilstrækkelig elektrisk belysning i forhold til anvendelsen.", "lighting is a general health and comfort chapter, not an access provision"),
 ("Well illuminated (if required for expected usage)", "elektrisk belysning i fornødent omfang", "BR", "kap. 18, § 382, stk. 1", "Have elektrisk belysning i fornødent omfang.", "applies to 'Arbejdsrum mv. og fælles adgangsveje'"),
 ("Well-illuminated (if site expected to be lit)", "god retningsgivende og blændfri belysning", "VT", "p. 2", "bør adgangstier forsynes med god retningsgivende og blændfri belysning", "guidance only ('bør')"),
 ("lighting levels", "belysningsstyrke", "BR", "kap. 18, § 379, stk. 2", "den indvendige belysningsstyrke fra dagslys er 300 lux eller mere", "PARTIAL: illuminance appears only for daylight and for the lighting installation test (§ 384), never for an access route"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "jævn fast belægning", "BR", "kap. 2, § 49, stk. 2, nr. 2", "Adgangsforhold fra vej og parkeringsarealer til ejendommen skal være mindst 1,3 m bredt og med jævn fast belægning.", "even and firm; slip resistance is not in BR18 text read"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "Belægningen er fast og jævn", "BR", "kap. 20, § 401, stk. 2", "Belægningen er fast og jævn.", "parking bay surface"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "vandret, fast og plant areal", "BR", "kap. 2, § 51, stk. 2, nr. 2", "Uden for yderdøre skal der være et vandret, fast og plant areal på 1,5 m x 1,5 m målt fra dørens hængselside.", "level, firm and plane: the area outside an entrance door"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "fast, skrid hæmmende belægning", "VT", "p. 2", "Det anbefales at etablere egentlige adgangsstier frem til konstruktionen med fast, skrid hæmmende belægning", "slip resistance appears only in this guidance; 'skrid hæmmende' is as extracted by pdftotext (likely 'skridhæmmende' with a layout space)"),
 ("Handrails", "Gribeegnede håndlister", "BR", "kap. 2, § 49, stk. 2, nr. 5", "Gribeegnede håndlister skal opsættes i en højde på ca. 0,8 m i begge sider af ramper og trapper.", ""),
 ("Handrails", "håndlister", "BR", "kap. 2, § 61, stk. 1", "Gange, trapper og ramper i fælles adgangsveje, hvor der ikke er opsat værn, skal forsynes med håndlister i begge sider under hensyn til bygningens udformning og anvendelse.", ""),
 ("Handrails", "Håndlister skal føres ubrudt forbi repos og afsluttes vandret", "BR", "kap. 2, § 61, stk. 1", "Håndlister skal føres ubrudt forbi repos og afsluttes vandret.", "continuity and horizontal termination"),
 ("Handrails", "nemme at gribe om og holde fast i", "BR", "kap. 2, § 58, nr. 5", "Håndlister skal være nemme at gribe om og holde fast i.", "graspability stated as a performance, no profile dimension"),
 ("Clear width|width", "fri bredde", "BR", "kap. 2, § 56, nr. 2", "Den fri bredde skal være mindst 1,30 m.", ""),
 ("Clear width|width", "passeres uhindret i deres fulde bredde", "BR", "kap. 2, § 56, nr. 2", "De har en tilstrækkelig bredde i forhold til anvendelsen, og skal kunne passeres uhindret i deres fulde bredde.", "aim (sufficient for the use) then minimum"),
 ("Clear width|width", "Trappens fri bredde", "BR", "kap. 2, § 57, nr. 1", "Trappens fri bredde er mindst 1,0 m", ""),
 ("Clear width|width|Door width (parameter 9)", "fri passagebredde", "BR", "kap. 2, § 52, stk. 1", "Yderdøre skal have en fri passagebredde på mindst 0,77 m.", "one door quantity (clear passage width); no nominal leaf width"),
 ("Accessible path of travel", "Fælles adgangsveje", "BR", "kap. 2, § 56", "Fælles adgangsveje, der fører til to eller flere boliger, kontorer, mødelokaler, udstillinger, salgsarealer eller andre enheder og funktioner på de enkelte etager", "the route object; 'tilgængelig' is not used for it"),
 ("Accessible path of travel", "adgangsarealer", "BR", "kap. 2, § 49, stk. 2", "For grundens adgangsarealer skal følgende være opfyldt:", "site access areas, outside"),
 ("Accessible path of travel", "adgangsstier", "VT", "p. 2", "Det anbefales at etablere egentlige adgangsstier frem til konstruktionen", ""),
 ("Clear signage", "letlæselig og letforståelig", "BR", "kap. 2, § 62, stk. 1", "I offentligt tilgængelige bygninger med en borgerrettet servicefunktion, skal væsentlig information om orientering i og brug af bygningen være letlæselig og letforståelig.", "information, not 'skiltning'; held alias 'skiltning' does not occur"),
 ("Clear signage", "piktogrammer", "BR", "kap. 2, § 62, stk. 3", "Informationen skal, under hensyn til bygningens anvendelse, være i form af punktskrift, lyd, piktogrammer, skrift og grafik i relief og ledelinjer.", ""),
 ("Audio accessibility and communication enhancement technologies", "teleslyngeanlæg", "BR", "kap. 9, § 218, stk. 1", "skal der være fast installation af teleslyngeanlæg eller lignende installationer på minimum samme niveau som teleslyngeanlæg", "assembly rooms; equivalent-level route"),
 ("Audio accessibility and communication enhancement technologies", "tekniske hjælpemidler, som eksempelvis teleslynger", "BR", "kap. 9, § 217", "så personer med behov for tekniske hjælpemidler, som eksempelvis teleslynger, ved egen hjælp kan deltage i aktiviteter i bygningen", ""),
 ("Audio accessibility and communication enhancement technologies", "auditivt og visuelt er angivet", "BR", "kap. 6, § 160, nr. 1", "Det auditivt og visuelt er angivet, at anlægget er aktiveret, og at forbindelse til modtageren er etableret.", "door-entry and call systems"),
 ("Level landings with clear space", "vandret plads", "BR", "kap. 2, § 49, stk. 2, nr. 3", "For hver ende af rampen skal der være en vandret plads på mindst 1,3 x 1,3 m.", ""),
 ("Level landings with clear space and at regular intervals|Ramp run length (parameter 12)", "reposer for hver 12 m", "BR", "kap. 2, § 49, stk. 2, nr. 4", "Ramper med en hældning på mere end 1:25 (4 cm pr. m.) skal have reposer for hver 12 m.", "outside: interval by LENGTH"),
 ("Level landings with clear space and at regular intervals", "vandret repos for hver 0,60 m stigning", "BR", "kap. 2, § 56, nr. 4", "Ramper, der udligner højdeforskelle på mere end 0,60 m, skal desuden forsynes med en vandret repos for hver 0,60 m stigning.", "inside common routes: interval by RISE, not length"),
 ("Clear space for approach|clearance", "fri afstand", "BR", "kap. 9, § 214, stk. 2, nr. 4", "Der skal være en fri afstand på mindst 0,90 m ved den side af wc'et, der vender bort fra håndvask.", "transfer space beside the WC"),
 ("Clear space for approach|clearance", "fri afstand", "BR", "kap. 9, § 202, nr. 1", "Der ud for arbejdspladser og opbevaringspladser er en fri afstand på mindst 1,10 m.", "kitchen, in front of worktops"),
 ("Clear space for approach", "ved siden af døren modsat hængselsiden", "BR", "kap. 2, § 52, stk. 2", "På den side af døren, der åbner imod personen, skal der være mindst 0,50 m ved siden af døren modsat hængselsiden.", "latch-side space at a door"),
 ("Riser height and tread depth|riser", "stigning (lodrette højde på trinnet)", "BR", "kap. 2, § 57, nr. 2", "Trappens stigning (lodrette højde på trinnet) må ikke være større end 0,18 m.", "riser height is 'stigning'; the same word is the rise of a ramp in § 56, nr. 4"),
 ("Riser height and tread depth|tread|depth", "Grunden (trinnets vandrette dybde)", "BR", "kap. 2, § 57, nr. 3", "Grunden (trinnets vandrette dybde) på ligeløbs-, kvart- og halvsvingstrapper ikke er mindre end 0,28 m.", "tread is 'grund', defined as a depth"),
 ("Riser height and tread depth|riser|tread", "stigning på højst 0,15 m og en grund", "BR", "kap. 2, § 49, stk. 2, nr. 3", "der kan suppleres med trin med en stigning på højst 0,15 m og en grund på mindst 0,3 m", "outdoor steps alongside a ramp"),
 ("Nosing design", "trinkanter", "BR", "kap. 2, § 49, stk. 2, nr. 7", "Det yderste af trinflader og trinkanter skal markeres med kontrastfarve.", ""),
 ("Nosing design", "trinforkanter", "BR", "kap. 2, § 58, nr. 4", "Højden på værn skal måles over trinforkanter og ramper samt fra overkant af gulv/dæk.", "nosing as the measuring reference for guard height"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip|LRV contrast (parameter 8)", "markeres med kontrastfarve", "BR", "kap. 2, § 49, stk. 2, nr. 7", "Det yderste af trinflader og trinkanter skal markeres med kontrastfarve.", "contrast colour only; no slip-resistant strip; no quantity"),
 ("Level threshold", "niveaufri adgang", "BR", "kap. 2, § 51, stk. 2, nr. 1", "Ved alle yderdøre skal der være niveaufri adgang til bygningen.", "held alias 'niveaufri adgang' occurs"),
 ("Level threshold", "Dørtrin må højst være 2,5 cm", "BR", "kap. 2, § 51, stk. 2, nr. 3", "Dørtrin må højst være 2,5 cm.", "a threshold up-stand is permitted within 'niveaufri'"),
 ("Level threshold|level", "i samme niveau som det indvendige gulv", "BR", "kap. 2, § 51, stk. 2, nr. 4", "Arealet ud for yderdøre skal være i samme niveau som det indvendige gulv.", ""),
 ("Height clearance (if sheltered or parkade)|clearance|Headroom clearance (parameter 11)|Headroom and protruding objects|Headroom", "fri højde", "BR", "kap. 2, § 57, nr. 1", "den fri højde målt lodret over hvert trins forkant og i trappens ganglinje er mindst 2,10 m", "stair headroom only; no parkade or shelter case"),
 ("Headroom clearance (parameter 11)|Headroom", "fri højde", "BR", "kap. 9, § 202, nr. 2", "I rum med skråt loft kan kravet opfyldes med en fri højde på mindst 2,10 m ved forkant af arbejdspladser og opbevaringspladser.", "kitchen under a sloping ceiling"),
 ("Headroom clearance (parameter 11)", "fri loftshøjde", "BR", "kap. 2, § 57", "Trapper i fælles adgangsveje skal udformes med tilstrækkelig bredde og fri loftshøjde i forhold til den tilsigtede brug", ""),
 ("Edge protection", "værn", "BR", "kap. 2, § 58", "Alle typer af værn eller rækværk skal under hensyn til bygningens anvendelse udformes, således at deres højde, udformning, frie åbninger i værnet mv. sikrer personer mod at falde ud over eller igennem dem.", "PARTIAL: a fall guard (guarding), not a kerb or wheel stop at a ramp edge"),
 ("Tactile attention indicators (truncated domes)", "belægningsskift i farve og følbarhed", "BR", "kap. 2, § 49, stk. 2, nr. 7", "Ovenfor trapper skal der udføres et belægningsskift i farve og følbarhed 0,90 m før trappens begyndelse.", "a change of paving in colour and feel; no domes, no product"),
 ("Tactile attention indicators (truncated domes)", "markeres taktilt", "BR", "kap. 2, § 51, stk. 2, nr. 5", "Arealet ud for yderdøre skal markeres taktilt eller ved anden farve end den omkringliggende belægning.", "tactile OR colour: either suffices"),
 ("Slope|gradient|Ramp gradient (parameter 3)", "hældning", "BR", "kap. 2, § 49, stk. 2, nr. 4", "Ramper må højst have en hældning på 1:20 (5 cm pr. m.)", "slope stated as a ratio and as cm per m; held alias 'rampehældning' does not occur"),
 ("Slope|gradient|Ramp gradient (parameter 3)", "hældning", "BR", "kap. 2, § 56, nr. 4", "Ramper må ikke udføres med en større hældning end 1:20 (5 cm pr. m)", ""),
 ("Slope|gradient", "hældning", "BR", "kap. 2, § 57", "samt have en hældning, der gør dem lette og sikre at gå på", "the same word for a stair's pitch"),
 ("Accessible controls", "Brugerbetjente anlæg", "BR", "kap. 6, § 159", "Brugerbetjente anlæg, herunder indkast til affaldssystemer, IT-standere, betalings- og selvbetjeningsautomater og lignende anlæg med offentligt tilgængelige servicefunktioner, skal opsættes, så brugerne kan betjene dem ved egen hjælp.", "one class for every user-operated installation"),
 ("Accessible controls|height", "placeret i en højde", "BR", "kap. 6, § 159, nr. 2", "Anlægget er placeret i en højde, så det kan benyttes af brugerne ved egen hjælp eller ved, at det kan hæves og sænkes.", "height by performance, or height-adjustable"),
 ("Accessible controls", "taktil identifikation", "BR", "kap. 6, § 160, nr. 2", "5-tallet i betjeningspanelet er markeret med taktil identifikation.", "keypad 5-key"),
 # quantity-bearing words (catalogue 2.2)
 ("height", "højde", "BR", "kap. 2, § 61, stk. 2", "Håndlister skal opsættes i en højde på ca. 0,80 m.", ""),
 ("level", "Niveauforskelle", "BR", "kap. 2, § 49, stk. 2, nr. 3", "Niveauforskelle i adgangsarealet skal udlignes i terræn eller ved rampe", "'level' as difference in height"),
 ("level", "niveauspring og højdeforskelle", "BR", "kap. 2, § 56, nr. 4", "Eventuelle niveauspring og højdeforskelle skal udlignes med ramper.", "three words for a change of level"),
 ("level", "vandret", "BR", "kap. 2, § 49, stk. 2, nr. 3", "For hver ende af rampen skal der være en vandret plads på mindst 1,3 x 1,3 m.", "'level' as flat"),
 ("width", "bredde", "BR", "kap. 9, § 207", "Boligens døre skal have en hensigtsmæssig bredde i forhold til boligens indretning.", ""),
 ("clearance|Turning circle (parameter 5)", "frit manøvreareal med en diameter", "BR", "kap. 9, § 214, stk. 2, nr. 5", "Der skal være et frit manøvreareal med en diameter på 1,5 m foran wc'et og fri af dørens opslagsareal.", "the only turning space in BR18 text read is in the WC; held alias 'vendeplads' does not occur"),
 ("number", "antallet af wc'er", "BR", "kap. 9, § 222, nr. 4", "Antallet af wc'er skal tilpasses antallet af beskæftigede.", ""),
 ("number", "et passende antal parkeringspladser", "BR", "kap. 20, § 401, stk. 1", "skal et passende antal parkeringspladser udformes, så de kan anvendes af handicapegnede køretøjer", "number left to judgment ('passende')"),
 ("number|ratio", "for hver yderligere 20. sengeplads", "BR", "kap. 9, § 235", "skal der for hver yderligere 20. sengeplads indrettes mindst 1 sengeplads med egne bade- og wc-faciliteter", "for 'ratio': proportional provision; no shower/bath mix"),
 ("depth", "rumdybder", "BR", "kap. 9, § 205", "Loftshøjden skal fastsættes i forhold til boligens rumdybder, rumstørrelser og vinduers placering.", "room depth, a daylight quantity"),
 ("force", "personer med reduceret kraft", "VT", "p. 2", "dårligt gående og personer med reduceret kraft har et jævnt og vandret areal at stå på", "DIFFERENT SENSE: the user's strength, not a fitting's operating force"),
 ("time", "brugstiden", "BR", "kap. 18, § 378", "der kan opretholdes udsyn til omgivelserne i en tilfredsstillende del af brugstiden", "DIFFERENT SENSE: share of the time in use (view out)"),
 ("size", "hensigtsmæssig størrelse og udformning", "BR", "kap. 9, § 199", "så boligen som helhed samt de enkelte rum har en hensigtsmæssig størrelse og udformning under hensyn til anvendelsen", ""),
 ("size", "Brugsarealet", "BR", "kap. 20, § 401, stk. 2", "Brugsarealet er 3,5 m x 5,0 m, og placeret så nær indgangen som muligt.", "parking bay"),
 ("volume", "rumindhold", "BR", "kap. 9, § 229, nr. 2", "Et rumindhold på mindst 6 m3 pr. person i normalklasserum i skoler og lignende.", "DIFFERENT SENSE: spatial volume, not sound volume"),
 ("capacity", "mærkelast af elevatorstol", "BR", "kap. 10, § 248, stk. 2", "Bestemmelsen gælder for elevatorer med mærkelast af elevatorstol på op til 2.000 kg.", "lift rated load; named in the energy rule, not an access rule"),
 ("distance", "indbyrdes afstand mellem alle typer balustre", "BR", "kap. 2, § 59", "Værn skal udføres, så den indbyrdes afstand mellem alle typer balustre, både lodrette og vandrette ikke giver anledning til personskader.", "DIFFERENT SENSE: baluster spacing; no distance markers"),
 ("ratio", "1:20 (5 cm pr. m.)", "BR", "kap. 2, § 49, stk. 2, nr. 4", "Ramper må højst have en hældning på 1:20 (5 cm pr. m.)", "ratio as slope notation"),
 # base parameters
 ("Corridor width (parameter 4)", "Vindfang, forstuer, gange og lignende skal have en fri bredde", "BR", "kap. 9, § 209", "Vindfang, forstuer, gange og lignende skal have en fri bredde på mindst 1,0 m.", "dwelling; 'gange' (plural of 'gang'), never 'korridor'"),
 ("Corridor width (parameter 4)", "gangarealet", "BR", "kap. 9, § 210", "Hvis der er døre eller skabsdøre i siderne af gangarealet, skal gangarealet være mindst 1,30 m i bredden.", "width tied to doors opening off the passage"),
 ("Corridor width (parameter 4)", "gange", "BR", "kap. 2, § 56", "som omfatter vindfang, forrum, gange, altangange, svalegange, plads foran elevatorer, ramper og reposer såvel i som uden for bygningen", "corridors are one member of the 'fælles adgangsveje' list"),
 ("Reverberation time (parameter 7)", "Efterklangstid", "BR", "kap. 17, § 368, stk. 2", "Efterklangstid.", "listed among acoustic considerations"),
 ("Reverberation time (parameter 7)", "Rums efterklangstid", "BR", "kap. 17, § 372, stk. 1", "Rums efterklangstid skal være reguleret i overensstemmelse med deres anvendelse.", "pointer to DS 490 class C and the vejledning om lydforhold; not an access provision"),
 ("Door width (parameter 9)", "fri passagebredde", "BR", "kap. 9, § 208", "Døre til vindfang, forstuer, gange, beboelsesrum, køkken, bade- og wc-rum i boligens adgangsetage skal have en fri passagebredde på mindst 0,77 m.", ""),
 ("Door width (parameter 9)", "fri passagebredde på mindst 77 cm", "VT", "p. 2", "Dørpassager eller døre i konstruktionen skal alle have en fri passagebredde på mindst 77 cm", ""),
 ("Lavatories", "Håndvask", "BR", "kap. 9, § 214, stk. 2, nr. 8", "Håndvask skal placeres i en højde på ca. 0,80 m med afløb under vask trukket tilbage.", ""),
 ("Lavatories", "Håndvask og wc skal placeres over et hjørne", "BR", "kap. 9, § 214, stk. 2, nr. 3", "Håndvask og wc skal placeres over et hjørne på hver sin sammenstødende væg, så håndvask kan nås af person siddende på wc'et.", "basin reachable from the WC seat"),
 ("Guy wires", "Barduner", "VT", "p. 3", "Barduner, store pløkker eller andre konstruktionsmæssige afstivninger", "guidance for temporary structures only"),
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
ALIAS = {"slope": "Slope"}
PARTIAL = {  # concept -> why the Danish match is not the English concept (ours)
 "lighting levels": "PARTIAL: illuminance only for daylight and installation test, never for routes",
 "Height clearance (if sheltered or parkade)": "NARROWER: stair headroom only; no shelter or parkade case",
 "Edge protection": "DIFFERENT CARVE: 'værn' is a fall guard, no kerb or wheel stop",
 "Colour-contrasted and slip-resistant strip on nosing": "PARTIAL: contrast colour only; no slip-resistant strip",
 "Colour-contrasted and slip-resistant strip": "PARTIAL: contrast colour only; no slip-resistant strip",
 "LRV contrast (parameter 8)": "BROADER: contrast never quantified; no luminance or LRV term",
 "force": "DIFFERENT SENSE: user's strength (guidance only)",
 "time": "DIFFERENT SENSE: share of time in use",
 "volume": "DIFFERENT SENSE: spatial volume",
 "distance": "DIFFERENT SENSE: baluster spacing; no distance markers",
 "ratio": "PARTIAL: slope notation and proportional room count; no room-type mix",
 "Headroom and protruding objects": "PARTIAL: headroom only; protruding objects not treated",
 "Turning circle (parameter 5)": "NARROWER: a 1.5 m diameter manoeuvring area in the WC only",
 "Guy wires": "NARROWER: guidance for temporary structures, not BR18 text",
}
ABSENT = {  # concept -> (note, regexes counted over ALL saved texts, case-insensitive)
 "Seating": ("no rest seating; § 220 'publikumspladser' are spaces for wheelchair users in fixed-seat venues (reverse harvest)", [r'bænk', r'hvile', r'siddeplads']),
 "Drainage": ("no surface drainage on routes; 'afløb' occurs only as the drain under a basin (§ 214, nr. 8); kap. 4 Afløb NOT-READ", [r'afvand', r'\bafløb\b']),
 "Floor surface is stable, firm, and non-slip": ("no interior floor-surface rule in the chapters read; kap. 14 Fugt og vådrum NOT-READ", [r'skridsik', r'skrid', r'glat', r'gulvbelægning']),
 "Shelter": ("no canopy or shelter at entrances; 'overdækket' occurs once, for a roofed courtyard (§ 395)", [r'overdæk', r'læskur', r'\bly\b']),
 "No open riser": ("open risers not treated", [r'setstykk', r'åbne trin', r'stødtrin']),
 "Sink faucet is easy to use or automatic": ("no tap rule", [r'armatur', r'blandingsbatteri', r'vandhane']),
 "Outlets and switches are at accessible heights": ("no socket or switch rule", [r'stikkontakt', r'afbryder', r'kontakt']),
 "Microwave mounting height accessible and safe": ("no appliance rule; kitchens treated only by free distance and headroom (§ 202)", [r'mikro', r'ovn']),
 "Accessible lockers": ("no lockers; nearest is § 212 storage for 'rollatorer' (reverse harvest)", [r'\bskab(e)?\b', r'bokse', r'garderobe']),
 "Accessible door hardware": ("no door-handle rule", [r'dørgreb', r'håndtag', r'\bgreb\b']),
 "Operating force (parameter 6)": ("no opening-force quantity; 'kraft' only as the user's strength (VT)", [r'åbningskraft', r'betjeningskraft', r'\bN\b']),
 "Colour temperature (parameter 10)": ("no colour-temperature term; lighting regulated by daylight share, illuminance test and energy", [r'farvetemperatur', r'kelvin']),
 "Gratings": ("no grating rule", [r'\brist', r'dæksel']),
 "Protruding objects": ("no protruding-object rule; § 238 treats collision with glass panes (reverse harvest)", [r'fremspring', r'udhæng', r'udragende']),
 "Spouts": ("no drinking fountain", [r'drikke', r'fontæne']),
 "Enclosures": ("no accessible shower enclosure; § 226 'brusepladser' are workplace shower counts", [r'brusenich', r'bruseplads']),
 "Speed bumps": ("not treated", [r'vejbump', r'bump']),
 "Bollards": ("not treated", [r'pullert']),
 "Landscaping elements": ("not treated", [r'beplant', r'landskab']),
 "Flower or shrub planters": ("not treated", [r'plantekass', r'krukke']),
 "Vegetation": ("not treated", [r'vegetation', r'træer', r'buske']),
 "Scaffolding": ("kap. 7 (byggepladsen) read in full: no scaffolding or route-through-works rule", [r'stillads']),
 "Gradation limits": ("not treated", [r'kornkurve', r'gradering']),
}

# Reverse harvest: (phrase verbatim, kind OURS, instrument, locator, quote verbatim, gloss OURS — not an equivalence)
REV = [
 ("Adgangsforhold", "domain name (chapter title)", "BR", "kap. 2 (heading)", "Adgangsforhold (§ 48 - § 62)", "the accessibility chapter is named 'access conditions'; 'tilgængelighed' is not used in the BR18 text read except in § 246 (the EN 81-70 title and the clause after it)"),
 ("ved egen hjælp", "performance standard", "BR", "kap. 2, § 48, stk. 1", "skal have adgangsforhold, der sikrer, at brugerne ved egen hjælp kan komme frem til dem, ind i dem samt frem til deres funktioner", "independent use, repeated as the aim of kap. 2, 6, 9, 10 and 20"),
 ("komme frem til dem, ind i dem samt frem til deres funktioner", "functional chain", "BR", "kap. 2, § 48, stk. 1", "kan komme frem til dem, ind i dem samt frem til deres funktioner", "reach, enter, reach the functions: the three section groups of kap. 2"),
 ("Adgangsforhold frem til bygningen", "section heading (stage of chain)", "BR", "kap. 2, §§ 49-50 (heading)", "Adgangsforhold frem til bygningen", ""),
 ("Adgangsforhold ved bygningen", "section heading (stage of chain)", "BR", "kap. 2, §§ 51-54 (heading)", "Adgangsforhold ved bygningen", ""),
 ("Fælles adgangsveje i bygningen", "section heading (stage of chain)", "BR", "kap. 2, §§ 55-56 (heading)", "Fælles adgangsveje i bygningen", "only COMMON routes are regulated; routes inside a dwelling fall under kap. 9"),
 ("Sommerhuse er ikke omfattet", "scope exclusion", "BR", "kap. 2, § 48, stk. 2", "Sommerhuse er ikke omfattet af bestemmelserne i kapitel 2 om adgangsforhold.", ""),
 ("Fritliggende enfamiliehuse", "scope exclusion (building class)", "BR", "kap. 2, § 48, stk. 3", "Fritliggende enfamiliehuse, der udelukkende anvendes til boligformål, er ikke omfattet af bestemmelserne i kapitel 2 om adgangsforhold", "except one step-free entrance door (§ 51, stk. 3)"),
 ("uforenlig med hensynet til klimasikring", "named conflict and exemption route", "BR", "kap. 2, § 51, stk. 4", "såfremt det vurderes, at bestemmelsen er uforenlig med hensynet til klimasikring, eller hvor terrænmæssige forhold umuliggør etablering af niveaufri adgang", "flood protection may override step-free access, by municipal permission"),
 ("forberedt til niveaufri adgang", "deferred-provision concept", "VB", "1.0.0", "mindst en yderdør skal være forberedt til niveaufri adgang", ""),
 ("målt fra dørens hængselside", "measuring reference", "BR", "kap. 2, § 51, stk. 2, nr. 2", "areal på 1,5 m x 1,5 m målt fra dørens hængselside", ""),
 ("markant taktil adskillelse til andre trafikformer", "technique", "BR", "kap. 2, § 49, stk. 2, nr. 6", "Gangarealerne til bebyggelsen skal anlægges med markant taktil adskillelse til andre trafikformer.", "tactile separation of the footway from other traffic"),
 ("vindfang, forrum, gange, altangange, svalegange, plads foran elevatorer", "enumerated route members", "BR", "kap. 2, § 56", "som omfatter vindfang, forrum, gange, altangange, svalegange, plads foran elevatorer, ramper og reposer", "deck-access galleries are named route members"),
 ("direkte og uhindret adgang", "route quality", "BR", "kap. 2, § 56, nr. 1", "Der er direkte og uhindret adgang til elevatorer, beboelsesenheder og funktioner i erhvervsbyggerier", ""),
 ("markeret ved forskellige materialer, farver eller belysning", "wayfinding technique", "BR", "kap. 2, § 56, nr. 3", "De er markeret ved forskellige materialer, farver eller belysning.", "routes marked by material, colour OR lighting"),
 ("Bestemmelsen anses som opfyldt når", "drafting structure (deemed-to-satisfy)", "BR", "kap. 2, § 57", "Bestemmelsen anses som opfyldt når:", "functional rule, then values that are deemed to satisfy it; also 'Kravet anses som opfyldt' (§§ 159, 160, 401)"),
 ("ganglinje", "geometric reference", "BR", "kap. 2, § 57, nr. 1", "i trappens ganglinje er mindst 2,10 m", "the stair's walking line"),
 ("spindel- og vindeltrapper", "element type", "BR", "kap. 2, § 57, nr. 4", "På spindel- og vindeltrapper må grunden ikke være mindre end 0,20 m.", "spiral and winding stairs permitted in common routes with their own tread"),
 ("ligeløbs-, kvart- og halvsvingstrapper", "element type", "BR", "kap. 2, § 57, nr. 3", "på ligeløbs-, kvart- og halvsvingstrapper", ""),
 ("frie åbninger i værnet", "quantity", "BR", "kap. 2, § 58", "frie åbninger i værnet mv. sikrer personer mod at falde ud over eller igennem dem", ""),
 ("børn ikke må kunne klatre på værnet", "user (children)", "BR", "kap. 2, § 59", "at børn ikke må kunne klatre på værnet eller komme i klemme mellem balustre", ""),
 ("luftsluser", "element", "BR", "kap. 2, § 58", "altaner, franske altandøre, altangange, luftsluser, tagterrasser, udvendige trapper", ""),
 ("borgerrettet servicefunktion", "building class trigger", "BR", "kap. 2, § 62, stk. 1", "I offentligt tilgængelige bygninger med en borgerrettet servicefunktion", "public-facing service function; triggers the information rule"),
 ("punktskrift, lyd, piktogrammer, skrift og grafik i relief og ledelinjer", "information modalities", "BR", "kap. 2, § 62, stk. 3", "være i form af punktskrift, lyd, piktogrammer, skrift og grafik i relief og ledelinjer", "braille, sound, pictograms, raised text and graphics, guidance lines"),
 ("ledelinjer", "element", "BR", "kap. 2, § 62, stk. 3", "skrift og grafik i relief og ledelinjer", "held alias 'ledelinjer' occurs; 'taktile ledelinjer' does not"),
 ("handicaptoiletter", "room (named once)", "BR", "kap. 2, § 62, stk. 2", "som wc-rum, handicaptoiletter, elevatorer, trapper, fordelingsveje mv.", "the WC rules themselves never use the word: they say 'wc-rum, der overholder følgende krav'"),
 ("offentligt tilgængelige bygninger", "building class", "BR", "kap. 9, § 214, stk. 1", "Offentligt tilgængelige bygninger skal indrettes, så de enkelte rum har en størrelse og udformning", "'tilgængelig' here means open to the public, not accessible"),
 ("over et hjørne på hver sin sammenstødende væg", "layout technique", "BR", "kap. 9, § 214, stk. 2, nr. 3", "Håndvask og wc skal placeres over et hjørne på hver sin sammenstødende væg", ""),
 ("friholdes fra fastmonteret inventar", "clear-wall rule", "BR", "kap. 9, § 214, stk. 2, nr. 4", "Væggen ved siden af wc'et, der vender bort fra håndvasken, skal friholdes fra fastmonteret inventar.", ""),
 ("fri af dørens opslagsareal", "space rule", "BR", "kap. 9, § 214, stk. 2, nr. 5", "foran wc'et og fri af dørens opslagsareal", "manoeuvring area must lie outside the door swing"),
 ("Toiletsæde", "element", "BR", "kap. 9, § 214, stk. 2, nr. 6", "Toiletsæde skal placeres i en højde på 0,48 m.", ""),
 ("opklappelige armstøtter", "element", "BR", "kap. 9, § 214, stk. 2, nr. 7", "Der skal være opklappelige armstøtter i en højde på 0,80 m på begge sider af wc'et.", "fold-up arm supports; held alias 'støttegreb' does not occur"),
 ("afløb under vask trukket tilbage", "technique", "BR", "kap. 9, § 214, stk. 2, nr. 8", "med afløb under vask trukket tilbage", "knee space by setting the trap back"),
 ("forsamlingslokaler", "room class", "BR", "kap. 9, § 218, stk. 2", "De nævnte forsamlingslokaler omfatter forsamlingshuse, kirker, biografer, biblioteker, aulaer og koncertsale samt mødelokaler, der er offentligt tilgængelige for publikum.", ""),
 ("personer med særlige pladsbehov", "user carve", "BR", "kap. 9, § 220", "skal der afsættes pladser, der sikrer adgang for personer med særlige pladsbehov, eksempelvis kørestolsbrugere", ""),
 ("fastmonterede publikumspladser", "room feature", "BR", "kap. 9, § 220", "I offentligt tilgængelige lokaler og anlæg med fastmonterede publikumspladser", ""),
 ("sengepladser med egne bade- og wc- faciliteter", "provision rule (hotels)", "BR", "kap. 9, § 233", "skal der indrettes minimum 2 sengepladser med egne bade- og wc- faciliteter", "counted in BEDS, not rooms"),
 ("indretningsplan, møbleringsplan", "documentation", "BR", "kap. 9, § 199", "Opfyldelse heraf skal dokumenteres i en indretningsplan, møbleringsplan eller lignende.", ""),
 ("opbevaring af større brugsgenstande", "space", "BR", "kap. 9, § 212", "et tilstrækkeligt og aflukket areal til opbevaring af større brugsgenstande, f.eks. cykler, barnevogne og rollatorer", "mobility-aid storage in housing"),
 ("wc-rum i adgangsetagen", "dwelling requirement", "BR", "kap. 9, § 204", "skal der indrettes mindst et wc-rum i adgangsetagen", ""),
 ("lempelser", "renovation relief", "BR", "kap. 9, § 197", "Ved ombygning kan kommunalbestyrelsen på bygningsejerens foranledning skønne, at der kan ske lempelser til bestemmelserne i kapitel 9", ""),
 ("kan benyttes af alle brugere af bygningen", "renovation rule", "BR", "kap. 9, § 216, stk. 1", "Wc-rum omfattet af § 214 stk. 2, skal ved ombygning indrettes, så det kan benyttes af alle brugere af bygningen.", ""),
 ("glaspartier", "hazard element", "BR", "kap. 9, § 238, stk. 1", "risiko for, at personer kan kollidere med større glaspartier i bygningen", ""),
 ("opsætning af markering på glasset", "technique", "BR", "kap. 9, § 238, stk. 2", "opsætning af markering på glasset", ""),
 ("type 2 elevator", "element (by standard)", "BR", "kap. 10, § 246", "skal mindst én elevator designes og udføres som type 2 elevator i overensstemmelse med DS/EN 81-70", "lift accessibility is delegated to a standard"),
 ("I bygninger med 3 etager og derover", "trigger", "BR", "kap. 10, § 244", "I bygninger med 3 etager og derover skal der installeres mindst én elevator", "basement not counted"),
 ("handicapegnede køretøjer", "carve: parking by vehicle", "BR", "kap. 20, § 401, stk. 1", "så de kan anvendes af handicapegnede køretøjer", "the accessible bay is defined by the vehicle, not the person"),
 ("Niveauspring i adgangsarealet fra parkeringsarealet", "quantity", "BR", "kap. 20, § 401, stk. 2", "Niveauspring i adgangsarealet fra parkeringsarealet til andet areal højst er 2,5 cm.", ""),
 ("betalings- og selvbetjeningsautomater", "element", "BR", "kap. 6, § 159", "IT-standere, betalings- og selvbetjeningsautomater", ""),
 ("kan hæves og sænkes", "technique", "BR", "kap. 6, § 159, nr. 2", "eller ved, at det kan hæves og sænkes", ""),
 ("Porttelefoner og tilkaldeanlæg", "element", "BR", "kap. 6, § 160", "Porttelefoner og tilkaldeanlæg skal have en sådan udformning", ""),
 ("Gener ved blænding minimeres", "hazard", "BR", "kap. 18, § 377, stk. 2", "Gener ved blænding minimeres.", "glare; general lighting chapter"),
 ("klasse C i DS 490 Lydklassifikation af boliger", "compliance pointer", "BR", "kap. 17, § 369, stk. 2", "klasse C i DS 490 Lydklassifikation af boliger", "acoustics delegated to a sound-class standard"),
 ("Brugerbegrebet", "defined concept (guidance)", "VB", "2.0.0", "Brugerbegrebet anlægger en bred ramme for dette samspil", "the 'user concept' that frames who the access rules serve"),
 ("alle mennesker, med ingen, mindre eller større funktionsnedsættelser", "population carve", "VB", "3.0.0", "Brugerne kan være alle mennesker, med ingen, mindre eller større funktionsnedsættelser.", ""),
 ("kørestolsbrugere, gangbesværede og synshandicappede", "population carve (whom detail rules serve)", "VB", "3.0.0", "overvejende udformet med henblik på kørestolsbrugere, gangbesværede og synshandicappede", "the guidance itself says the detail rules mainly serve these three groups"),
 ("personer med ADHD, syns- eller hørehandicappede, psykisk udviklingshæmmede", "population carve", "VB", "3.0.0", "personer med ADHD, syns- eller hørehandicappede, psykisk udviklingshæmmede, børn og ældre", ""),
 ("ligeværdighed i adgangsforhold og indretning", "aim", "VB", "0.0.0", "Kapitlernes formålsparagraffer tilsigter ligeværdighed i adgangsforhold og indretning for brugere", "equal standing as the stated aim"),
 ("detailløsninger", "drafting category", "VB", "1.0.0", "der som udgangspunkt ikke kan opfyldes på andre måder end med de detailløsninger", "detail requirements vs the purpose ('hensynene bag') behind them"),
 ("dispensation", "compliance route", "VB", "1.0.0", "Der kan meddeles dispensation, hvis det dokumenteres, at hensynene bag kravene opfyldes igennem andre løsninger", "equivalent-effect route via municipal dispensation"),
 ("forhåndsdialog", "procedure", "VB", "2.0.0", "kan det være en god idé at indlede en forhåndsdialog med kommunen", ""),
 ("Danske Handicaporganisationer", "standing to appeal", "VB", "1.0.0", "Danske Handicaporganisationer og medlemsorganisationer også klageberettiget", "disabled people's organisations have standing to appeal municipal building decisions"),
 ("universelt design", "concept", "VB", "2.0.0", "Fremvoksende metodikker inden for arkitekturen såsom universelt design muliggør en bred brugeranskuelse", "held alias 'universelt design' occurs, in guidance only"),
 ("Tilgængelighed for alle", "concept (guidance)", "VT", "Forord", "Tilgængelighed for alle betyder, at alle, uanset om man er kørestolsbruger", "the word 'tilgængelighed' lives in the guidance, not the regulation"),
 ("har orienteringsbesvær", "population carve", "VT", "Forord", "dårligt gående med rollator, har orienteringsbesvær eller et andet handicap", ""),
 ("Løse ramper kan ikke anbefales", "advice", "VT", "p. 2", "Løse ramper kan ikke anbefales, da kørestolsbrugere ofte oplever dem usikre.", "portable ramps advised against, with the users' experience as reason"),
 ("ledningsføringer", "hazard element", "VT", "p. 2", "Hvis der er ledningsføringer liggende oven på terræn, der krydser adgangsvejen", "cables across a route"),
 ("kiler hen over ledningsføringen", "technique", "VT", "p. 3", "ved kiler hen over ledningsføringen", "cable-crossing wedges"),
 ("Tilgængelighedskrav i BR18 holdt op mod DS/ISO 21542", "compliance pointer", "VA", "page body", "DS Håndbog 186: Tilgængelighedskrav i BR18 holdt op mod DS/ISO 21542.", "the official guidance for kap. 2 is a pointer to a paid DS handbook"),
]

def regen_check():
    """Each saved text must be a deterministic function of the raw persisted artefact: re-extract it
    (tools/h2t.py's transform for HTML/XML, `pdftotext -layout` for PDF) and compare. Returns failures."""
    import subprocess, html as H
    R = 'retrieval-log/session_2026-11-06-base-vocabulary-review/'
    bad = n = 0
    for f in sorted({x for v in INST.values() for x in v[1]}):
        raw = [g for g in glob.glob(R + f + '.*')]
        if len(raw) != 1: bad += 1; print('REGEN: no unique artefact for', f, file=sys.stderr); continue
        raw = raw[0]
        if raw.endswith('.pdf'):
            out = subprocess.run(['pdftotext', '-layout', raw, '-'], capture_output=True, text=True).stdout
        else:
            t = open(raw, encoding='utf-8').read()
            t = re.sub(r'(?is)<(script|style|noscript|svg|header|footer|nav)\b.*?</\1>', ' ', t)
            t = re.sub(r'(?i)<br\s*/?>', '\n', t)
            t = re.sub(r'(?i)</?(p|div|h[1-6]|li|tr|table|section|article|ul|ol|dt|dd)\b[^>]*>', '\n', t)
            t = re.sub(r'(?i)</t[dh]>', ' | ', t)
            t = re.sub(r'<[^>]+>', ' ', t)
            t = H.unescape(t).replace('\xa0', ' ')
            t = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n'))
            out = re.sub(r'\n{3,}', '\n\n', t).strip() + '\n'
        n += 1
        if out != open(T + f + '.txt', encoding='utf-8').read():
            bad += 1; print('REGEN MISMATCH', f, file=sys.stderr)
    print('text files re-derived from raw artefacts', n, 'mismatches', bad)
    return bad

def alias_report():
    try:
        con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
        al = sorted({a for (a,) in con.execute("select distinct alias from term_aliases where lower(language)='da'")})
    except Exception as e:
        print('alias report skipped:', e); return
    low = ALL.lower()
    hit = [a for a in al if a.lower() in low]
    print('held DA aliases', len(al), 'occurring as substrings of saved texts', len(hit), ':', ', '.join(hit))

def main():
    bad = 0; rows = []
    for c, ph, ins, loc, q, note in OBS:
        fs = where(ins, q); okp = norm(ph).lower() in norm(q).lower()
        if not (fs and okp): bad += 1; print('FAIL', ins, loc, ph, bool(fs), okp, file=sys.stderr)
        rows.append([c, ph, 'da', INST[ins][0], loc, q, (fs[0] + '.txt') if fs else '', 'yes' if fs and okp else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    rrows = []
    for ph, kind, ins, loc, q, g in REV:
        fs = where(ins, q); okp = norm(ph).lower() in norm(q).lower()
        if not (fs and okp): bad += 1; print('REV FAIL', ins, loc, ph, bool(fs), okp, file=sys.stderr)
        rrows.append([ph, kind, 'da', INST[ins][0], loc, q, (fs[0] + '.txt') if fs else '', 'yes' if fs and okp else 'NO', g])
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        w.writerows(rrows)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else ('base_parameters' if i < 60 else 'b651-headings (RHFAC-does-not-name)'))
            hit = [r for r in rows if c in r[0].split('|') or (c in ALIAS and ALIAS[c] in r[0].split('|'))]
            if hit:
                if c in ABSENT: bad += 1; print('CONFLICT: concept both observed and ABSENT', c, file=sys.stderr)
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                w.writerow([c, src, st, len(hit), ' / '.join(sorted({r[1] for r in hit})), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                note, pats = ABSENT.get(c, ('NO NOTE: check', []))
                counts = ', '.join(f"/{p}/i={len(re.findall(p, ALL, re.I))}" for p in pats)
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', note + (' [counts over all saved texts: ' + counts + ']' if counts else '')])
    bad += regen_check()
    print('observations', len(rows), 'reverse-harvest', len(rrows), 'failures', bad)
    alias_report()
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
