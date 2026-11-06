"""Regenerate equivalents.tsv for NL-NL and verify every row against the saved text.
Run from anywhere: python3 -I build_equiv.py
Exits 1 if a quote is not found verbatim (whitespace-normalised) in its text file, if the form is not in
its quote, if a quote exceeds 25 words, or if a concept_id is not in register-v2/concepts.tsv.
PDF page numbers are DERIVED here (form feeds before the quote), never typed."""
import csv, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(H, '..', '..', 'register-v2', 'concepts.tsv')
lab = {r[0]: (r[2] or r[5]) for r in csv.reader(open(REG, encoding='utf-8'), delimiter='\t')}

BWB = 'https://repository.officiele-overheidspublicaties.nl/bwb/'
# key: (title as written, issuer, url, jurisdiction, text file, tier)
SRC = {
 'BBL': ('Besluit bouwwerken leefomgeving (consolidated 2026-09-24_0)', 'Minister van BZK (Stb. 2018, 291; BWBR0041297)',
         BWB + 'BWBR0041297/2026-09-24_0/xml/BWBR0041297_2026-09-24_0.xml', 'NL', '52ef1dbbf8d109ba.txt', '1'),
 'BB12': ('Bouwbesluit 2012 (last expression 2023-09-07_0; repealed 2024-01-01)', 'Minister (BWBR0030461)',
          BWB + 'BWBR0030461/2023-09-07_0/xml/BWBR0030461_2023-09-07_0.xml', 'NL', '56c4f96582c47206.txt', '1'),
 'RVV': ('Reglement verkeersregels en verkeerstekens 1990 (RVV 1990), consolidated 2026-07-01_0', 'Minister van IenW (BWBR0004825)',
         BWB + 'BWBR0004825/2026-07-01_0/xml/BWBR0004825_2026-07-01_0.xml', 'NL', 'bcf7b0e5b90a6a86.txt', '2'),
 'RVVB1': ('RVV 1990, bijlage 1 (sign catalogue annexed to the regulation)', 'Minister van IenW (BWBR0004825)',
           BWB + 'BWBR0004825/2026-07-01_0/xml/BWBR0004825_2026-07-01_0.xml', 'NL', 'bcf7b0e5b90a6a86.txt', '3'),
 'BABW': ('Besluit administratieve bepalingen inzake het wegverkeer (BABW), consolidated 2026-01-01_0', 'Minister van IenW (BWBR0004826)',
          BWB + 'BWBR0004826/2026-01-01_0/xml/BWBR0004826_2026-01-01_0.xml', 'NL', '072e6096b733e935.txt', '2'),
 'WGBH': ('Wet gelijke behandeling op grond van handicap of chronische ziekte, consolidated 2026-01-01_0', 'Staten-Generaal (BWBR0014915)',
          BWB + 'BWBR0014915/2026-01-01_0/xml/BWBR0014915_2026-01-01_0.xml', 'NL', 'f2bb24d614389252.txt', '2'),
 'CRPD': ('Verdrag inzake de rechten van personen met een handicap (Dutch text in the BWB treaty base)', 'Tractatenblad / BWBV0004045 (translation origin not checked)',
          BWB + 'BWBV0004045/2006-12-13_0/xml/BWBV0004045_2006-12-13_0.xml', 'NL', 'a620e88c170cc0b7.txt', '2'),
 'WWL': ('Warenwetbesluit liften 2016 (consolidated 2020-02-01_0)', 'Minister van SZW (BWBR0037650)',
         BWB + 'BWBR0037650/2020-02-01_0/xml/BWBR0037650_2020-02-01_0.xml', 'NL', '036268576badc231.txt', '2'),
 'LRL': ('Richtlijn 2014/33/EU (liften), Dutch-language text', 'Europees Parlement en Raad (EUR-Lex CELEX 32014L0033)',
         'https://eur-lex.europa.eu/legal-content/NL/TXT/HTML/?uri=CELEX:32014L0033', 'EU', 'ec4e43db64a43b08.txt', '2'),
 'BZK': ("Toegankelijk bouwen (web page)", 'Ministerie van BZK, volkshuisvestingnederland.nl',
         'https://www.volkshuisvestingnederland.nl/onderwerpen/verduurzamen-en-verbeteren/besluit-bouwwerken-leefomgeving/toegankelijk-bouwen', 'NL', '8be21dedbca82962.txt', '4'),
 'DONGEN': ('VERKEERSBESLUIT Aanwijzen gehandicaptenparkeerplaats op kenteken in Donk, Dongen (Gemeenteblad 2026, 396491)', 'Gemeente Dongen',
            'https://zoek.officielebekendmakingen.nl/gmb-2026-396491.html', 'NL', 'a67c85906a493daf.txt', '4'),
 'ZUID': ('Gemeentelijk beleid gehandicaptenparkeerplaatsen 2020-2030', 'Gemeente Zuidplas',
          'https://www.zuidplas.nl/_flysystem/media/gemeentelijk-beleid-gehandicaptenparkeerplaatsen.pdf', 'NL', '5cb72c8ad18810ae.txt', '4'),
 'TK': ('Kamervragen (Aanhangsel) 2023-2024, nr. 1894 (antwoord Minister van VWS)', 'Tweede Kamer / Minister van VWS',
        'https://zoek.officielebekendmakingen.nl/ah-tk-20232024-1894.html', 'NL', 'fd763ab54d048fb3.txt', '4'),
 'UVA': ('Maagdenhuis (location page)', 'Universiteit van Amsterdam', 'https://www.uva.nl/locaties/binnenstad/maagdenhuis.html', 'NL', '92088b31e230fd2b.txt', '4'),
 'IAMW': ('Rolstoelvriendelijke activiteiten op een regenachtige dag', 'I amsterdam (city marketing body); text by the founder of Able Amsterdam, per the page',
          'https://www.iamsterdam.com/zien-en-doen/rolstoelvriendelijke-activiteiten-op-een-regenachtige-dag', 'NL', 'f637ffa9a25efe23.txt', '4'),
 'IAMM': ('Musea en galeries: mensen met een fysieke beperking', 'I amsterdam (city marketing body)',
          'https://www.iamsterdam.com/zien-en-doen/musea-en-galeries/mensen-met-een-fysieke-beperking', 'NL', '6cdd96d0df782780.txt', '4'),
 'PRORAIL': ('Eenduidige en voorspelbare routegeleiding op stations (brochure)', 'ProRail (with Oogvereniging Nederland, per the brochure)',
             'https://www.prorail.nl/siteassets/homepage/reizen/documenten/brochure-routegeleiding-op-stations-zonder-afbeeldingen.pdf', 'NL', 'dfda9a6aaa2a4396.txt', '4'),
 'IEDH': ('Zwembad Helperbad nu helemaal toegankelijk', 'Ieder(in)', 'https://iederin.nl/zwembad-helperbad-nu-helemaal-toegankelijk/?print-posts=print', 'NL', '65af978787961732.txt', '5'),
 'IEDP': ('Woning toegankelijk maar pad ernaartoe niet', 'Ieder(in)', 'https://iederin.nl/woning-toegankelijk-maar-pad-ernaartoe-niet/', 'NL', 'a0dd52a639c7c3fd.txt', '5'),
 'IEDR': ('Toegankelijke woningen: een verborgen wooncrisis (rapport, juni 2021)', 'Ieder(in) with the Woonbond',
          'https://iederin.nl/onderzoeken/wonen-toegankelijk-wonen-een-verborgen-wooncrisis/', 'NL', '6754c96a40298e7c.txt', '5'),
 'VLA': ('persoon met een handicap / gehandicapte / andersvalide / mindervalide / invalide (taaladvies)', 'Vlaamse overheid, Team Taaladvies (BE CONTRAST, not an NL attestation)',
         'https://www.vlaanderen.be/team-taaladvies/taaladviezen/persoon-met-een-handicap-gehandicapte-andersvalide-mindervalide-invalide', 'BE', '138e5cce9df184f3.txt', '4'),
}
PDF = {'ZUID', 'PRORAIL', 'IEDR'}

C, CO, R, OD, Q, P, S = 'code term', 'colloquial', 'regional variant', 'outdated or disfavoured', 'qualifier', 'product name', 'unattested seed'
# concept_id, form, usage_type, scope_note, source key, locator (pdf: page is appended), quote, conflation_note
ROWS = [
 # --- parking (owner class 1) ---
 ('R2-050', 'gehandicaptenparkeerplaats', C, 'the statute term for the bay; defined by who may park there (card or vehicle), not by geometry', 'RVV', 'art. 26 lid 1',
  'Op een gehandicaptenparkeerplaats mag slechts worden geparkeerd:', ''),
 ('R2-050', 'Gehandicaptenparkeerplaats', C, 'sign E6, the signage name of the same bay', 'RVVB1', 'bijlage 1, hoofdstuk E, bord E6 (Omschrijving)',
  'Gehandicaptenparkeerplaats', ''),
 ('R2-050', 'gehandicaptenparkeerplaats op kenteken', C, 'NARROWER: a bay reserved for one vehicle by its registration, signed E6 with an onderbord', 'DONGEN', 'besluit (dictum)',
  'Aanwijzen van een gehandicaptenparkeerplaats op kenteken in de directe nabijheid van Donk 53 in Dongen door middel van het plaatsen van het verkeersbord E6', ''),
 ('R2-050', 'gereserveerde gehandicaptenparkeerplaats op kenteken', C, 'NARROWER, as above; "gereserveerd" echoes RVV art. 26 lid 1 c', 'DONGEN', 'overwegingen',
  'een aanvraag heeft ingediend om in aanmerking te komen voor een gereserveerde gehandicaptenparkeerplaats op kenteken', ''),
 ('R2-050', 'algemene gehandicaptenparkeerplaats', C, 'NARROWER: the general bay open to every card holder, opposed to "op kenteken"; municipal policy term', 'ZUID', '',
  'Een algemene gehandicaptenparkeerplaats is bestemd voor het', ''),
 ('R2-050', 'individuele gehandicaptenparkeerplaatsen', OD, 'the 2008 policy name for the vehicle-bound bay, repealed by this policy; superseded municipal wording', 'ZUID', '',
  'de inhoud van ‘Beleid inzake individuele gehandicaptenparkeerplaatsen (Nieuwerkerk aan den IJssel,', ''),
 ('R2-050', 'parkeercapaciteit aan mindervaliden', OD, '"mindervaliden" is judged outdated and pejorative in the BE language advice (row below); here in a 2020 municipal title', 'ZUID', 'subtitle',
  'Kaders voor het toekennen van parkeercapaciteit aan mindervaliden', ''),
 ('R2-050', 'Rolstoeltoegankelijke parkeerplaatsen', CO, 'NARROWER: names the wheelchair user, not the card; a museum\'s bays as described by the city', 'IAMM', 'museum entry (paragraph on a museum with a lift)',
  'Rolstoeltoegankelijke parkeerplaatsen op het terrein kunnen tot één dag van tevoren worden gereserv', ''),
 ('R2-050', 'gehandicaptenparkeerplaats', C, 'Co-1 usage: the DPO uses the code term and contrasts it with an ordinary bay', 'IEDH', 'section "Gehandicaptenparkeerplaats"',
  'Eind maart is de gehandicaptenparkeerplaats gerealiseerd aan de Moddermanlaan.', 'NOTE: the same page says "Het is niet zomaar een algemene parkeerplaats geworden": "algemene parkeerplaats" here is an ordinary bay, while Zuidplas "algemene gehandicaptenparkeerplaats" is the general disabled bay; same adjective, two senses'),
 ('R2-050', 'gehandicaptenparkeerkaart', C, 'the PERMIT, not the bay; the bay is defined through it (RVV art. 26 lid 1 b); kept because other pairs file permit forms here', 'BABW', 'Hoofdstuk IV, art. 49 lid 1',
  'een gehandicaptenparkeerkaart worden verstrekt.', 'CONFLATION risk: permit and bay share the compound stem gehandicaptenparkeer-'),
 ('R2-050', 'parkeerkaarten voor gehandicapten', C, 'foreign-issued permits treated as equal to the Dutch card; the permit, not the bay', 'RVV', 'art. 86',
  'afgegeven parkeerkaarten voor gehandicapten, voor zover deze bij ministeriële regeling zijn aangewezen', ''),
 ('R2-281', 'parkeervakken', C, 'the Bbl names parking only for EV charging points; it has NO disabled-parking rule (Q1)', 'BBL', 'art. 4.160b lid 1',
  'met een parkeergelegenheid in het gebouw of buiten het gebouw op hetzelfde bouwwerkperceel met meer dan vijf parkeervakken', ''),
 ('R2-281', 'Parkeergelegenheid', C, 'sign E4, the general parking place', 'RVVB1', 'bijlage 1, hoofdstuk E, bord E4', 'Parkeergelegenheid', ''),
 # --- umbrella qualifier (owner class 2) ---
 ('R2-333', 'toegankelijk', Q, 'the building code\'s umbrella word, always with "voor personen met een functiebeperking" in the aim articles', 'BBL', 'art. 4.183 lid 1 (aansturingsartikel)',
  'Een bouwwerk heeft ruimten die voldoende toegankelijk zijn voor personen met een functiebeperking.', ''),
 ('R2-333', 'integraal toegankelijke', Q, 'NARROWER: fixes a defined room standard (toilet, bath), not a general state', 'BBL', 'art. 4.186 lid 3',
  'In een toegankelijkheidssector ligt een integraal toegankelijke toiletruimte.', ''),
 ('R2-333', 'toegankelijk', Q, 'same word, other sense', 'BBL', 'Bijlage I, divisie A, "openbaar toegankelijk gebied"',
  'ander openbaar gebied dat voor publiek algemeen toegankelijk is', 'CONFLATION: toegankelijk = open to the public (as DA tilgængelig, SYNTHESIS 3e); also art. 4.225 "toegankelijk voor hulpverleningsdiensten" (emergency access)'),
 ('R2-333', 'toegankelijk', Q, 'same word, other sense', 'BBL', 'art. 4.225 lid 1',
  'Een bouwwerk is zodanig toegankelijk voor hulpverleningsdiensten dat tijdig bluswerkzaamheden kunnen worden uitgevoerd', 'CONFLATION: access for emergency services'),
 ('R2-333', 'toegankelijk', Q, 'same word, other sense', 'RVVB1', 'bijlage 1, onderbord C22e (milieuzone)',
  'milieuzone voor vrachtauto’s, toegankelijk voor vrachtauto’s emissieklasse 6', 'CONFLATION: toegankelijk = permitted to enter a low-emission zone'),
 ('R2-333', 'voor rolstoelen toegankelijke', Q, 'NARROWER: a wheelchair-accessible VEHICLE (registration code SH), not a place', 'RVV', 'art. 86c',
  'voor rolstoelen toegankelijke personen- of bedrijfsauto: personen- of bedrijfsauto die in het kentekenregister is voorzien', ''),
 ('R2-333', 'toegankelijk', Q, 'same word, other sense', 'LRL', 'art. 1 lid 1 c)',
  'alleen goederen indien de drager toegankelijk is, dat wil zeggen dat een persoon deze zonder probleem kan betreden', 'CONFLATION: a lift carrier any person can step into (EU, nl text)'),
 ('R2-333', 'algemene toegankelijkheid', Q, 'the equal-treatment statute\'s umbrella for goods, services and places; legal duty "geleidelijk"', 'WGBH', 'art. 2a lid 1',
  'draagt daarnaast tenminste geleidelijk zorg voor de algemene toegankelijkheid voor personen met een handicap of chronische ziekte', ''),
 ('R2-333', 'universeel ontwerp', Q, 'WIDER: design usable by everyone without adaptation; the treaty\'s term, not used by the Bbl (Q1: universeel 0)', 'CRPD', 'art. 2',
  '„universeel ontwerp”: ontwerpen van producten, omgevingen, programma’s en diensten die door iedereen in de ruimst mogelijke zin gebruikt kunnen worden', ''),
 ('R2-333', 'Toegankelijkheid', Q, 'the treaty article heading', 'CRPD', 'art. 9 (heading)', 'Artikel 9 Toegankelijkheid', ''),
 ('R2-333', 'inclusieve', Q, 'WIDER: qualifies society, not a building element; the ministry ties it to accessible buildings', 'BZK', 'intro',
  'Toegankelijke gebouwen zijn belangrijk voor een inclusieve samenleving.', ''),
 ('R2-333', 'rolstoeltoegankelijk', Q, 'NARROWER: wheelchair users only', 'IAMW', 'De Hallen entry',
  'In de Filmhallen zijn alle zalen rolstoeltoegankelijk en is er in elke zaal een rolstoelplek beschikbaar.', ''),
 ('R2-333', 'rolstoelvriendelijk', Q, 'NARROWER: wheelchair users only; the owner\'s "wheelchair friendly" has a Dutch analogue attested here', 'IAMW', 'intro',
  'De stad zit vol met rolstoelvriendelijke plekken waar je droog én comfortabel kunt genieten.', ''),
 ('R2-333', 'rolstoeltoegankelijke woning', Q, 'NARROWER; a housing LABEL in a letting system, per a Co-1 respondent (the same page: "het label rolstoeltoegankelijke woning")', 'IEDR', 'section 7.3',
  'Er is geen rolstoeltoegankelijke woning beschikbaar.', ''),
 ('R2-333', 'rolstoelgeschikt', Q, 'NARROWER; respondent\'s word for a path', 'IEDR', 'list of adaptations',
  'tegelpad rolstoelgeschikt naar voordeur en achterom (hoekhuis).', ''),
 ('R2-333', 'gelijkvloerse woning', Q, 'NARROWER: one floor level, no stairs; a housing class, not a full accessibility state', 'IEDR', 'summary',
  'Een derde van de mensen met een beperking woont in een gelijkvloerse woning', ''),
 ('R2-333', 'levensloopbestendige', Q, 'WIDER/OTHER: "life-course-proof" housing; respondents report it allocated by age (55+)', 'IEDR', 'section 7.3',
  'In mijn gemeente zijn geen levensloopbestendige huizen voor mensen jonger', 'CONFLATION (Co-1, recorded not resolved): accessible housing labelled 55+ woning; the same page says "toegankelijke woningen gelabeld worden als 55+ woning"'),
 ('R2-333', 'aangepaste woning', Q, 'OTHER: "adapted" dwelling; a Co-1 respondent rejects its stretch', 'IEDR', 'section 7.3',
  'De term \'aangepaste woning\' is een rekbaar. Een gelijkvloerse woning zonder', 'CONFLATION (Co-1): a step-free dwelling with grab-bar fixings already counts as "aangepast"'),
 ('R2-333', 'mindervalide', OD, 'BE CONTRAST: disfavoured in Flemish usage; the NL municipal title above still uses it', 'VLA', 'paragraph 3',
  'De woorden invalide , mindervalide en andersvalide worden als verouderd beschouwd.', ''),
 ('R2-333', 'gehandicapte', OD, 'BE CONTRAST: the noun is disfavoured, compounds with gehandicapte stay in use (as the NL statutes do: gehandicaptenparkeerplaats)', 'VLA', 'paragraph 2',
  'Het zelfstandig naamwoord gehandicapte wordt tegenwoordig opgevat als een aanduiding die mensen verengt tot hun handicap', ''),
 ('R2-333', 'gehandicapten', OD, 'superseded within one decree: the afdeling heading kept "gehandicapten" while its article says "personen met een functiebeperking"', 'BB12', 'afd. 6.10 (heading)',
  'Bereikbaarheid van gebouwen voor gehandicapten, nieuwbouw en bestaande bouw', ''),
 # --- vertical transport (owner class 3) ---
 ('R2-163', 'lift', C, 'defined by pointer: a lift for persons in the lift decree\'s sense, which points on to directive 2014/33/EU', 'BBL', 'Bijlage I, divisie A',
  'lift: lift voor personen als bedoeld in artikel 1 van het Warenwetbesluit liften 2016;', ''),
 ('R2-163', 'liften', C, 'defined only by pointer to the directive', 'WWL', 'art. 1 lid 1 n',
  'liften: hetgeen de artikelen 1, eerste lid, en 2 van de richtlijn daaronder verstaan;', ''),
 ('R2-163', 'lift', C, 'WIDER than an elevator in a shaft: includes inclined lifts on guides over 15 degrees', 'LRL', 'art. 2 punt 1',
  '„lift” : een hijs- of hefwerktuig dat bepaalde niveaus bedient met behulp van een drager', 'CARVE: excludes "hijs- en hefwerktuigen met een maximumsnelheid van 0,15 m/s" (art. 1 lid 2 a), so the Bbl\'s "lift" (by pointer) does not cover most platform lifts'),
 ('R2-163', 'kooi van een lift', C, 'the car', 'BBL', 'art. 4.190 lid 1', 'De kooi van een lift als bedoeld in artikel 4.189 heeft een vloeroppervlakte', ''),
 ('R2-163', 'brandweerlift', C, 'NARROWER: firefighters\' lift', 'BBL', 'Bijlage I, divisie A',
  'brandweerlift: lift die met een eenvoudige handeling ter beschikking van de brandweer kan worden gesteld', ''),
 ('R2-163', 'lift voor vluchten bij brand', C, 'NARROWER: evacuation lift (column heading of the use-class table)', 'BBL', 'tabel 4.212 (column heading)', 'lift voor vluchten bij brand', ''),
 ('R2-163', 'lift bij brand', CO, 'Co-1 concern: which lifts are usable in fire', 'IEDP', 'section "Gebruik van liften bij brand"',
  'Mensen met een mobiliteitsbeperking weten vaak niet of de lift bij brand bruikbaar is.', ''),
 ('R2-163', 'lift', CO, 'ordinary usage on a station: a passenger lift', 'PRORAIL', 'section on platforms',
  'Soms zijn er wel twee liften nodig: in dat geval brengt de eerste lift u naar de', ''),
 ('R2-164', 'hijs- of hefwerktuig', C, 'the class over lifts and other lifting devices (cf. B651 "Elevating devices")', 'LRL', 'art. 2 punt 1',
  'een hijs- of hefwerktuig dat bepaalde niveaus bedient', ''),
 ('R2-166', 'voorportaal lift', C, 'NARROWER: a fire-safety lobby in front of a lift', 'BBL', 'art. 4.77a (heading)', 'Artikel 4.77a (voorportaal lift)', ''),
 ('R2-168', 'plateaulift', CO, 'a platform for wheelchair users at an entrance', 'UVA', 'Toegankelijkheid gebouw',
  'De ingang via de Voetboogsteeg heeft een plateaulift voor rolstoelgebruikers.', ''),
 ('R2-168', 'platformlift', CO, 'a stair that converts into a platform lift', 'IAMW', 'Grachtenmuseum entry',
  'door een druk op de knop verandert de trap in een platformlift.', 'NOTE: the same paragraph continues "De lift kan naar alle verdiepingen toe": "lift" names the platform device here'),
 ('R2-168', 'lift voor rolstoelen', CO, 'ambiguous: a lift "for wheelchairs" at an entrance; device type not stated', 'IAMW', 'library entry',
  'Bij de ingang is een lift voor rolstoelen, van de entreehal naar de bibliotheek.', 'CONFLATION: platform lift or passenger lift; not settled by the text'),
 ('R2-169', 'traplift', C, 'the stair lift funded under the Wmo; the minister\'s own term', 'TK', 'antwoord op vraag 2',
  'Het infoblad Trapliften op bestaande trappen 2 geeft de mogelijkheid om een traplift aan de muurzijde te plaatsen', ''),
 ('R2-169', 'Traplift', CO, 'Co-1 survey: the second most named home adaptation', 'IEDR', 'table of adaptations', 'Traplift', ''),
 ('R2-171', 'liften die voorhanden zijn of worden gebruikt in de particuliere huishouding', C, 'scope clause, not a name: lifts in private homes are lifts under the decree', 'WWL', 'art. 1 lid 3',
  'Dit besluit is mede van toepassing op liften die voorhanden zijn of worden gebruikt in de particuliere huishouding.', ''),
 ('R2-172', 'badlift', CO, 'pool lift', 'IEDH', 'last paragraph before "Sticker"',
  'In het nieuwste baddeel was al een badlift aangebracht', ''),
 ('R2-173', 'tillift aan het plafond', CO, 'ceiling hoist; "tillift" alone also names mobile hoists', 'IEDR', 'list of adaptations',
  'tillift aan het plafond (meerdere keren genoemd).', ''),
 # --- second-priority concepts ---
 ('R2-083', 'hellingbaan', C, 'the code term; capped by rise (first pass)', 'BBL', 'art. 4.189',
  'overbrugd door een lift of een hellingbaan', 'NOTE: the Bbl offers lift and hellingbaan as alternatives for one rule'),
 ('R2-083', 'hellingbaan', CO, 'ordinary usage', 'IAMM', 'museum entry', 'Via de hellingbaan naast de', ''),
 ('R2-083', 'rolstoelbanen', CO, 'wheelchair ramps or tracks in a museum; sense not defined', 'IAMM', 'Rijksmuseum entry',
  'van liften en rolstoelbanen en van toegankelijkheidsplattegronden', ''),
 ('R2-083', 'oprijplaten', CO, 'NARROWER: ramp plates, usually short or removable (cf. R2-534 rampe amovible, not judged equal)', 'IAMW', 'Grachtenmuseum entry',
  'En er zijn oprijplaten geplaatst waar het nodig', ''),
 ('R2-083', 'helling', CO, 'a respondent\'s word for a ramp to be built in a home', 'IEDR', 'section 7.3', 'een helling bouwen', 'CONFLATION: in the Bbl "helling" is the gradient (art. 4.30), here the ramp itself'),
 ('R2-161', 'hoogteverschil groter dan 0,02 m', C, 'the code expresses the threshold as a level difference (first pass carve 3)', 'BBL', 'art. 4.182 lid 5',
  'is een hoogteverschil groter dan 0,02 m, gemeten vanaf de vloer met aankleding, overbrugd door een lift of een hellingbaan.', ''),
 ('R2-161', 'drempel', CO, 'the ministry\'s plain word for the same rule', 'BZK', 'section "Minimumeisen in het Besluit bouwwerken leefomgeving (Bbl)"',
  'de drempel naar een tuin of balkon van nieuwbouwwoningen niet hoger mag zijn dan twee centimeter', ''),
 ('R2-161', 'drempel', CO, 'Co-1 usage', 'IEDP', 'intro', 'een keurig toegankelijke deur – met een drempel van maximaal 20 mm', ''),
 ('R2-161', 'zonder drempels', CO, 'figurative and literal at once ("barrier-free" as an idiom)', 'IAMW', 'intro', 'er is altijd iets leuks te doen, zonder drempels.', 'CONFLATION: drempel = physical sill and figurative barrier in one phrase'),
 ('R2-161', 'drempelhulp', P, 'a threshold ramp device, not a level threshold; generic product word', 'IEDR', 'table of adaptations', 'Drempels laten verwijderen of drempelhulp', ''),
 ('R2-551', 'gelijkvloers', CO, 'on one level, no steps; not judged equal to NO trinnfri', 'IAMM', 'Van Eesteren Museum entry',
  'Het museum is gelijkvloers en is daardoor goed toegankelijk.', ''),
 ('R2-179', 'integraal toegankelijke toiletruimte', C, 'the code\'s defined accessible toilet room', 'BBL', 'art. 4.187 lid 2',
  'Een integraal toegankelijke toiletruimte heeft een vloeroppervlakte van ten minste 1,65 m x 2,2 m.', ''),
 ('R2-179', 'invalidentoilet', OD, 'disfavoured stem (invalide, per BE advice); still on a city page', 'IAMW', 'De Hallen entry',
  'kunnen gebruikmaken van het invalidentoilet bij de Filmhallen', ''),
 ('R2-179', 'toilet voor mensen met een handicap', CO, 'person-first descriptive form', 'IAMW', 'museum entry',
  'daarbij is er een toilet voor mensen met een handicap aanwezig', ''),
 ('R2-179', 'rolstoeltoilet', CO, 'NARROWER by name (wheelchair users)', 'IAMM', 'museum entry', 'Dit museum is goed toegankelijk met liften en een rolstoeltoilet.', ''),
 ('R2-186', 'beugels', CO, 'grab bars (fixings for them) in a shower', 'IEDR', 'section 7.3', 'met (mogelijkheid tot) beugels in de douche', ''),
 ('R2-094', 'noppentegels', C, 'warning tiles (dots); the brochure\'s term for the hazard warning', 'PRORAIL', 'stairs',
  'harde noppentegels van minimaal zestig centimeter breed bovenaan de trap.', ''),
 ('R2-094', 'waarschuwingsmarkering', C, 'the warning field as a whole, part of the guidance line; also printed hyphenated waarschuwings-markering', 'PRORAIL', 'route section',
  'dat aan een speciale waarschuwingsmarkering. De waarschuwings-markering maakt onderdeel uit', 'CARVE: the warning is part of the geleidelijn, not a separate indicator'),
 ('R2-094', 'noppenvlak', C, 'the dotted field', 'PRORAIL', 'platform section', 'Dit noppenvlak mag u niet missen.', ''),
 ('R2-095', 'geleidelijn', C, 'the guidance line, felt by its ribbels', 'PRORAIL', 'route section', 'De geleidelijn is ook te voelen aan de ribbels.', ''),
 ('R2-095', 'attentievlak', C, 'a FLAT square without ribbels at a branch or decision point', 'PRORAIL', 'route section',
  'een vierkant attentievlak. U voelt dan even geen ribbels meer.', 'FALSE FRIEND: "attentie" suggests the attention (warning) indicator R2-094, but the NL attentievlak is a flat decision point; the warning is the noppenvlak'),
 ('R2-247', 'scootmobielen', C, 'mobility scooter, named for storage', 'BBL', 'art. 4.172 lid 1', 'een afsluitbare bergruimte om fietsen of scootmobielen beschermd tegen weer en wind', ''),
 ('R2-247', 'gehandicaptenvoertuig', C, 'NARROWER and legal: a vehicle for a disabled person, at most 1,10 m wide, at most 45 km/h', 'RVV', 'art. 1',
  'gehandicaptenvoertuig: voertuig dat is ingericht voor het vervoer van een gehandicapte, niet breder is dan 1,10 meter', ''),
 ('R2-072', 'toegankelijke aansluiting op de openbare weg', CO, 'the accessible route from the door to the public road', 'IEDP', 'intro',
  'maar vervolgens geen toegankelijke aansluiting op de openbare weg.', ''),
]

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

fails = []
out = [['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note', 'attestation_tier',
        'source', 'locator', 'quote', 'conflation_note']]
cache = {}
for cid, form, ut, sn, k, loc, q, cn in ROWS:
    title, issuer, url, jur, tf, tier = SRC[k]
    if cid not in lab: fails.append(f'unknown concept {cid}')
    if len(q.split()) > 25: fails.append(f'quote over 25 words: {q[:40]}')
    if form.lower() not in q.lower(): fails.append(f'form not in quote: {form}')
    if tf not in cache: cache[tf] = open(os.path.join(H, 'text', tf), encoding='utf-8', errors='replace').read()
    raw = cache[tf]
    n = norm(raw).find(norm(q))
    if n < 0:
        fails.append(f'QUOTE NOT FOUND in {tf}: {q[:60]}')
    elif k in PDF:
        # derive the page: count form feeds in the raw text before the first quote token occurrence near the match
        pages = raw.split('\f')
        pg = next((i + 1 for i, p in enumerate(pages) if norm(q) in norm(p)), None)
        loc = (loc + '; ' if loc else '') + (f'p. {pg}' if pg else 'page not derivable (quote spans pages)')
    out.append([cid, lab.get(cid, ''), form, 'nl', jur, ut, sn, tier, f'{title} — {issuer} — {url}', loc, q, cn])

with open(os.path.join(H, 'equivalents.tsv'), 'w', encoding='utf-8', newline='') as f:
    csv.writer(f, delimiter='\t', lineterminator='\n').writerows(out)
print(f'rows {len(out) - 1}; failures {len(fails)}')
for x in fails: print(' ', x)
sys.exit(1 if fails else 0)
