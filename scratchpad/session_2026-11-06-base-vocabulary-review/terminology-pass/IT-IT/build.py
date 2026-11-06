"""Build observations / coverage / reverse-harvest / instruments TSVs for the IT/IT terminology pass,
verifying every quote (after whitespace collapse) in the saved extracted text. Adapted from FR-FR/build.py.
Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/IT-IT/build.py
Exits 1 if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder.
Text files are produced from the persisted artefacts by tools/nt2txt.py (one Normattiva article page each)."""
import re, sys, csv, os, hashlib, json
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/IT-IT'
R = 'retrieval-log/session_2026-11-06-base-vocabulary-review'
DM_FILES = ['8389d1d659da538e', '1eb7803e30a719e5', 'f998067e0b9502d2', 'd4c287be39e505af', '559bbda34dd994c4',
            'f746723b9ab1ef8f', '62d133bb180ba6d0', 'c5174db912c656ef', '10903672f4ef0b70', '841a7df49ce08a21',
            '34e74cadad837463', '4a3e28f19eb45ac1']  # DM 236/1989 arts 1..12, in order
DPR_FILES = ['5d768f53eed9adaa', 'dcac722f0723c531', '2a51823b86a52452', '019bb2eeffedadc2', '79bee95bc3786d1c',
             '149d9d1559139a83', 'a23db3ea7886b120', '017ef814e2800a50', '92679757f3cc14fb', 'e08852f709c90155',
             'fe8a9108d721d14a', 'f61d1bd02cec3a0f', '740ec409442fb0a7', 'b71b29f5e7559356', 'f1541d33b3486404',
             'dd4e3e4ae69179c7', '8c7fbeae037f90cf', 'abfe4e7533f92e4b', '3e4efb4b6dcd2063', 'd93c9d9c918d5d87',
             '546ce28debc1b755', '18b78fbc9254da6a', '5cb1553788f51ba3', '9e3c8d5e019ea284', 'c25b0cfba310aee3',
             '2837db0f228b43d1', 'ce2e69c8abd4c8a6', '95ae2b831a1153c3', 'fbb2ad0766ace76c', '52ba2db9b77e8aba',
             'c13f16d7a51582e6']  # DPR 503/1996 arts 1..31 (art. 32 page, with the DM 236 appendix, is APP)
APP_FILES = ['6ce5a1b63a1225c1']  # DPR 503/1996 art. 32 page: art. 32, notes, and the "Appendice" reprinting DM 236
LAW_FILES = ['47cc14cd99f79e38', '0d6a7eb72f6773d8', 'ad04a53b14203300', '3cc46f2a1f91b682', '0b3cbf8b25735a14',
             '7f8dc0fcea0d6f1d', 'dbd06ed438507456']  # L. 13/1989 art. 1; DPR 380/2001 arts 77-82
INST = {
 'DM236': ("Decreto ministeriale 14 giugno 1989, n. 236 — Prescrizioni tecniche necessarie a garantire l'accessibilità, l'adattabilità e la visitabilità degli edifici privati e di edilizia residenziale pubblica sovvenzionata e agevolata, ai fini del superamento e dell'eliminazione delle barriere architettoniche", DM_FILES),
 'DPR503': ("Decreto del Presidente della Repubblica 24 luglio 1996, n. 503 — Regolamento recante norme per l'eliminazione delle barriere architettoniche negli edifici, spazi e servizi pubblici", DPR_FILES),
 'APP': ("DPR 503/1996, art. 32 page: 'Appendice' reprinting DM 236/1989 (second witness of the DM text)", APP_FILES),
 'LAW': ("Legge 9 gennaio 1989, n. 13, art. 1; DPR 6 giugno 2001, n. 380 (Testo unico edilizia), artt. 77-82", LAW_FILES),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {}
for k, (_, fs) in INST.items():
    TXT[k] = [(f, norm(open(f'{D}/text/{f}.txt', encoding='utf-8').read())) for f in fs]
def where(ins, q):
    for f, t in TXT[ins]:
        if norm(q) in t: return f + '.txt'
    return None

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note — ours)
L1 = "Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels"
SURF = "Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant"
OBS = [
 (L1, "illuminazione artificiale", "DM236", "punto 4.1.10, 5)", "è preferibile una illuminazione naturale laterale. Si deve dotare la scala di una illuminazione artificiale, anche essa laterale, con comando individuabile al buio e disposto su ogni pianerottolo.", "stairs only; lighting is stated by kind and position, never by illuminance"),
 (L1, "devono essere illuminati", "DPR503", "art. 6, comma 1", "Nelle strade ad alto volume di traffico gli attraversamenti pedonali devono essere illuminati nelle ore notturne o di scarsa visibilità.", "pedestrian crossings only"),
 ("Well illuminated (if required for expected usage)", "luce d'emergenza", "DM236", "punto 8.1.12", "una luce d'emergenza con autonomia minima di h.3", "lift car only"),
 (SURF, "pavimentazione antisdrucciolevole", "DM236", "punto 8.2.2", "Per pavimentazione antisdrucciolevole si intende una pavimentazione realizzata con materiali il cui coefficiente di attrito", "a defined term, with a friction coefficient and a named test method"),
 (SURF, "antisdrucciolevole", "DM236", "punto 4.2.2", "La pavimentazione del percorso pedonale deve essere antisdrucciolevole.", ""),
 (SURF, "bloccaggio duraturo", "DM236", "punto 8.2.2", "ad assicurare il bloccaggio duraturo degli elementi costituenti la pavimentazione stessa", "firmness/stability is expressed as durable fixing of the paving elements"),
 ("Floor surface is stable, firm, and non-slip", "non sdrucciolevoli", "DM236", "punto 4.1.2", "I pavimenti devono essere di norma orizzontali e complanari tra loro e, nelle parti comuni e di uso pubblico, non sdrucciolevoli.", "interior 'pavimenti' vs exterior 'pavimentazione': two words for floor and paving"),
 ("Seating", "posti a sedere", "DM236", "punto 4.1.4", "ove necessario deve essere predisposto un idoneo spazio d'attesa con posti a sedere.", "waiting-area seating"),
 ("Seating", "sedile ribaltabile", "DM236", "punto 8.1.6", "la doccia deve essere a pavimento, dotata di sedile ribaltabile e doccia a telefono", "shower seat; also a lift-car seat in 8.1.12"),
 ("Seating", "posti riservati", "DM236", "punto 5.2", "essere dotata di posti riservati per persone con ridotta capacità motoria", "reserved seats in assembly halls"),
 ("Handrails", "corrimano", "DM236", "punto 4.1.10", "Le scale devono essere dotate di parapetto atto a costituire difesa il vuoto e di corrimano.", "'corrimano' also names toilet grab rails (8.1.6) — one word, two elements"),
 ("Handrails", "corrimano centrale", "DPR503", "art. 7, comma 1", "I percorsi che superano i 6 metri di larghezza devono essere, di norma, attrezzati anche con corrimano centrale.", ""),
 ("Clear width|width", "larghezza utile di passaggio", "DM236", "punto 4.2.1", "privi di strozzature, arredi, ostacoli di qualsiasi natura che riducano la larghezza utile di passaggio", ""),
 ("Clear width|width", "larghezza minima", "DM236", "punto 8.2.1", "Il percorso pedonale deve avere una larghezza minima di 90 cm", ""),
 ("Accessible path of travel", "percorso agevolmente fruibile", "DM236", "punto 3.2, a)", "il requisito si considera soddisfatto se esiste almeno un percorso agevolmente fruibile anche da parte di persone con ridotte o impedite capacità motorie o sensoriali", ""),
 ("Accessible path of travel", "percorso accessibile", "DPR503", "art. 4, comma 1", "devono prevedere almeno un percorso accessibile in grado di consentire con l'utilizzo di impianti di sollevamento ove necessario", ""),
 ("Accessible path of travel", "percorso pedonale", "DM236", "punto 4.2.1", "Quando un percorso pedonale sia adiacente a zone non pavimentate", ""),
 ("Clear signage", "segnaletica", "DM236", "punto 4.3", "Negli edifici aperti al pubbico deve essere predisposta una adeguata segnaletica che indichi le attività principali ivi svolte ed i percorsi necessari per raggiungerle.", "the source text reads 'pubbico' (sic)"),
 ("Clear signage", "cartelli di indicazione", "DM236", "punto 4.3", "cartelli di indicazione che facilitino l'orientamento e la fruizione degli spazi costruiti", ""),
 ("Clear signage", "tabelle ed i dispositivi segnaletici", "DPR503", "art. 9, comma 2", "Le tabelle ed i dispositivi segnaletici devono essere installati in posizione tale da essere agevolmente visibili e leggibili.", ""),
 ("Audio accessibility and communication enhancement technologies", "apparecchi fonici", "DM236", "punto 4.3", "Per i non vedenti è opportuno predisporre apparecchi fonici per dette indicazioni", "for blind people, not for hearing enhancement"),
 ("Audio accessibility and communication enhancement technologies", "simbolo internazionale di accesso alla comunicazione per le persone sorde", "DPR503", "art. 2, comma 4", "apparecchiature quali ascensori e telefoni che assicurano servizi di comunicazione per sordi, devono recare in posizione agevolmente visibile il simbolo internazionale di accesso alla comunicazione per le persone sorde", "a marking duty, not a technology requirement; no induction loop is named"),
 ("Audio accessibility and communication enhancement technologies", "avvisatori acustici", "DPR503", "art. 6, comma 4", "devono essere dotati di avvisatori acustici che segnalano il tempo di via libera anche a non vedenti", "audible traffic signals"),
 ("Level landings with clear space|Level landings with clear space and at regular intervals", "ripiano orizzontale", "DM236", "punto 8.1.11", "Ogni 10 metri di lunghezza ed in presenza di interruzioni mediante porte, la rampa deve prevedere un ripiano orizzontale di dimensioni minime", "ramp landing; 'ripiano' (ramp, path) vs 'pianerottolo' (stair)"),
 ("Level landings with clear space and at regular intervals", "ripiano orizzontale di sosta", "DM236", "punto 8.2.1", "e' necessario prevedere un ripiano orizzontale di sosta, di profondita' almeno 1.50 m, ogni 15 m di lunghezza del percorso", "rest landing on a sloped path; interval tied to the slope"),
 ("Level landings with clear space", "ripiani orizzontali di riposo", "DM236", "punto 4.1.11", "Si devono interporre ripiani orizzontali di riposo per rampe particolarmente lunghe.", ""),
 ("Level landings with clear space", "pianerottoli", "DM236", "punto 4.1.10, 1)", "la larghezza delle rampe e dei pianerottoli deve permettere il passaggio contemporaneo di due persone", ""),
 ("Clear space for approach", "accostamento laterale", "DM236", "punto 4.1.6", "lo spazio necessario per l'accostamento laterale della sedia a ruote alla tazza", "approach is split by direction: laterale / frontale"),
 ("Clear space for approach", "accostamento frontale", "DM236", "punto 4.1.6", "lo spazio necessario per l'accostamento frontale della sedia a ruote al lavabo", ""),
 ("Clear space for approach", "spazi antistanti e retrostanti", "DM236", "punto 4.1.1", "Occorre dimensionare adeguatamente gli spazi antistanti e retrostanti, con riferimento alle manovre da effettuare con la sedia a ruote", "door approach space, front and back"),
 ("Shelter", "dotati di copertura", "DM236", "punto 8.2.3", "detti posti auto riservati sono, preferibilmente, dotati di copertura", "reserved parking spaces only, and only 'preferibilmente'"),
 ("Riser height and tread depth|riser|tread", "alzata e pedata", "DM236", "punto 4.1.10", "Per ogni rampa di scale i gradini devono avere la stessa alzata e pedata.", "a stair flight is a 'rampa di scale'"),
 ("Riser height and tread depth|riser|tread|ratio", "rapporto tra alzata e pedata", "DM236", "punto 8.1.10", "I gradini devono essere caratterizzati da un corretto rapporto tra alzata e pedata (pedata minima 30 cm)", "the rule is a relation (2a+p), not two separate limits"),
 ("Nosing design", "aggetto del grado rispetto al sottogrado", "DM236", "punto 8.1.10", "In caso di disegno discontinuo, l'aggetto del grado rispetto al sottogrado deve essere compreso fra un minimo di 2 cm e un massimo di 2,5 cm.", "nosing projection is named by the parts 'grado' and 'sottogrado'"),
 ("Nosing design", "spigoli arrotondati", "DM236", "punto 8.1.10", "Il profilo del gradino deve presentare preferibilmente un disegno continuo a spigoli arrotondati", ""),
 ("No open riser", "sottogrado inclinato", "DM236", "punto 8.1.10", "con sottogrado inclinato rispetto al grado, e formante con esso un angolo di circa 75 - 80", "a riser is assumed and its inclination preferred; open risers are not expressly prohibited"),
 ("Level threshold", "soglie", "DM236", "punto 4.1.2", "lo spigolo di eventuali soglie deve essere arrotondato", ""),
 ("Level threshold", "La soglia interposta tra balcone o terrazza e ambiente interno", "DM236", "punto 4.1.8", "La soglia interposta tra balcone o terrazza e ambiente interno non deve presentare un dislivello tale da costituire ostacolo al transito di una persona su sedia a ruote.", ""),
 ("Level threshold", "complanari", "DM236", "punto 4.1.1", "il vano della porta e gli spazi antistanti e retrostanti devono essere complanari", "'complanare' is the instrument's word for flush"),
 ("Height clearance (if sheltered or parkade)|Headroom clearance (parameter 11)", "non devono esistere ostacoli di nessun genere", "DM236", "punto 8.2.1", "Fino ad un'altezza minima di 2.10 m dal calpestio, non devono esistere ostacoli di nessun genere, quali tabelle segnaletiche o elementi sporgenti dai fabbricati", "pedestrian headroom stated as an obstacle-free height, not a noun; no parkade/vehicle headroom"),
 ("Edge protection", "cordolo", "DM236", "punto 8.1.11", "Qualora al lato della rampa sia presente un parapetto non pieno, la rampa deve avere un cordolo di almeno 10 cm di altezza.", ""),
 ("Edge protection", "ciglio", "DM236", "punto 4.2.1", "è necessario prevedere un ciglio da realizzare con materiale atto ad assicurare l'immediata percezione visiva nonché acustica se percosso con bastone", "the path edge is also a cane-detectable guide"),
 ("Edge protection", "difesa verso il vuoto", "DM236", "punto 8.1.10", "Il parapetto che costituisce la difesa verso il vuoto deve avere un'altezza minima di 1.00 m.", ""),
 ("Colour-contrasted and slip-resistant strip on nosing|Tactile attention indicators (truncated domes)", "segnale al pavimento", "DM236", "punto 8.1.10", "Un segnale al pavimento (fascia di materiale diverso o comunque percepibile anche da parte dei non vedenti), situato almeno a 30 cm dal primo e dall'ultimo scalino, deve indicare l'inizio e la fine della rampa.", "a floor band before the stair, not on the nosing; tactile only as 'percepibile anche da parte dei non vedenti'"),
 ("Colour-contrasted and slip-resistant strip on nosing", "pedata antisdrucciolevole", "DM236", "punto 4.1.10", "I gradini delle scale devono avere una pedata antisdrucciolevole", ""),
 ("Tactile attention indicators (truncated domes)", "segnalate anche ai non vedenti", "DM236", "punto 4.2.1", "Le intersezioni tra percorsi pedonali e zone carrabili devono essere oppurtunatamente segnalate anche ai non vedenti.", "no device named; 'oppurtunatamente' (sic)"),
 ("Slope|gradient", "pendenza longitudinale", "DM236", "punto 8.2.1", "La pendenza longitudinale non deve superare di norma il 5%", ""),
 ("Slope|gradient", "pendenza trasversale", "DM236", "punto 8.2.1", "La pendenza trasversale massima ammissibile e' dell'1%.", "cross slope"),
 ("Slope|gradient", "contropendenze", "DM236", "punto 8.2.1", "In presenza di contropendenze al termine di un percorso inclinato", "counter-slopes summed against the horizontal"),
 ("Sink faucet is easy to use or automatic", "rubinetti con manovra a leva", "DM236", "punto 4.1.6", "Si deve dare preferenza a rubinetti con manovra a leva", ""),
 ("Sink faucet is easy to use or automatic", "miscelatori termostatici", "DM236", "punto 4.1.6", "con erogazione dell'acqua calda regolabile mediante miscelatori termostatici", "the held alias 'valvola termostatica' is not this phrase"),
 ("Outlets and switches are at accessible heights", "interruttori e prese", "DM236", "punto 8.1.5", "Schema delle altezze consigliate per la collocazione di quadri, interruttori e prese.", "the heights themselves are in the graphic schema (not read)"),
 ("Outlets and switches are at accessible heights|height", "ALTEZZE APPARECCHI DI COMANDO, INTERRUTTORI, PRESE, PULSANTI", "DM236", "punto 8.0.1", "ALTEZZE APPARECCHI DI COMANDO, INTERRUTTORI, PRESE, PULSANTI Distanza misurata in verticale dall'asse del dispositivo di comando al piano di calpestio.", "a measurement convention"),
 ("Level landings with clear space and at regular intervals", "allargamenti", "DM236", "punto 8.1.9", "Questi allargamenti devono di preferenza essere posti nelle parti terminali dei corridoi e previsti comunque ogni 10 m di sviluppo lineare degli stessi.", "regular-interval passing/turning widenings on corridors; carve difference: interval rule on width, not on landings"),
 ("Colour-contrasted and slip-resistant strip", "variazioni cromatiche", "DM236", "punto 4.1.2", "Nel primo caso si deve segnalare il dislivello con variazioni cromatiche", ""),
 ("Colour-contrasted and slip-resistant strip|LRV contrast (parameter 8)", "differenziato per materiale e colore", "DM236", "punto 8.2.1", "essere differenziato per materiale e colore dalla pavimentazione del percorso", "kerb/edge; contrast never quantified"),
 ("LRV contrast (parameter 8)", "differenziazione nel materiale e nel colore", "DM236", "punto 4.1.2", "mediante una adeguata differenziazione nel materiale e nel colore delle pavimentazioni", ""),
 ("Accessible door hardware", "maniglie del tipo a leva", "DM236", "punto 4.1.1", "Sono da preferire maniglie del tipo a leva opportunamente curvate ed arrotondate.", ""),
 ("Accessible door hardware|height", "ALTEZZA MANIGLIA", "DM236", "punto 8.0.1", "ALTEZZA MANIGLIA Distanza misurata in verticale dall'asse di rotazione della manopola", ""),
 ("Accessible controls", "terminali degli impianti", "DM236", "punto 4.1.5", "4.1.5 TERMINALI DEGLI IMPIANTI", "one class for every operable building-services terminal"),
 ("Accessible controls", "bottoniera di comando", "DM236", "punto 4.1.12", "La bottoniera di comando interna ed esterna deve avere il comando più alto ad un'altezza adeguata alla persona su sedia a ruote ed essere idonea ad un uso agevole da parte dei non vedenti.", "lift controls"),
 ("Accessible controls", "facilmente individuabili anche in condizioni di scarsa visibilità", "DM236", "punto 4.1.5", "devono, inoltre, essere facilmente individuabili anche in condizioni di scarsa visibilità ed essere protetti dal danneggiamento per urto", ""),
 ("level", "differenze di livello", "DM236", "punto 4.1.2", "Eventuali differenze di livello devono essere contenute ovvero superate tramite rampe con pendenza adeguata", "level = difference in height"),
 ("level", "dislivello", "DM236", "punto 8.1.2", "Qualora i pavimenti presentino un dislivello, questo non deve superare i 2,5 cm.", ""),
 ("level", "livelli di qualità dello spazio costruito", "DM236", "punto 3.1", "In relazione alle finalità delle presenti norme si considerano tre livelli di qualità dello spazio costruito.", "DIFFERENT SENSE: 'livello' as a grade of accessibility; also 'livelli fuori terra' = storeys (3.2)"),
 ("clearance", "spazio libero", "DM236", "punto 8.1.7", "questi devono essere previsti con sottostante spazio libero per un'altezza minima di cm. 70 dal calpestio", "knee clearance under sink and hob"),
 ("clearance|Door width (parameter 9)", "luce netta", "DM236", "punto 8.0.1", "LUCE NETTA PORTA O PORTA-FINESTRA Larghezza di passaggio al netto dell'ingombro dell'anta mobile", "door clear width defined with its measurement convention (and glossed 'larghezza utile di passaggio')"),
 ("Door width (parameter 9)", "luce netta della porta", "DM236", "punto 8.1.1", "La luce netta della porta di accesso di ogni edificio e di ogni unita' immobiliare deve essere di almeno 80 cm.", "entrance doors vs 'altre porte' carry different minima"),
 ("number|ratio", "numero di stanze accessibili", "DM236", "punto 5.3", "Il numero di stanze accessibili in ogni struttura ricettiva deve essere di almeno due fino a 40 o frazioni di 40", "a count per tranche of rooms"),
 ("ratio", "almeno il 5% degli alloggi", "DM236", "punto 3.3, a)", "almeno il 5% degli alloggi previsti negli interventi di edilizia residenziale sovvenzionata", "share of accessible dwellings: the nearest sense to the register's room-type mix"),
 ("number", "nella misura minima di 1 ogni 50 o frazione di 50", "DM236", "punto 8.2.3", "nella misura minima di 1 ogni 50 o frazione di 50, posti auto di larghezza non inferiore a m. 3,20", "parking count"),
 ("depth", "profondita'", "DM236", "punto 8.1.12", "cabina di dimensioni minime di 1.40 m di profondita' e 1.10 m di larghezza", "art. 8 text writes accents as apostrophes"),
 ("depth", "profondità", "DM236", "punto 4.1.8", "deve avere una profondità tale da consentire la manovra di rotazione della sedia a ruote", ""),
 ("force|Operating force (parameter 6)", "esercitando una pressione non superiore a 8 kg", "DM236", "punto 8.1.1", "L'anta mobile deve poter essere usata esercitando una pressione non superiore a 8 kg.", "force is a 'pressione' stated in kg; 'forza' does not occur in this sense"),
 ("force|Operating force (parameter 6)", "lieve pressione", "DM236", "punto 4.1.3", "le parti mobili devono poter essere usate esercitando una lieve pressione", ""),
 ("time", "tempi di apertura e chiusura delle porte", "DM236", "punto 4.1.12", "I tempi di apertura e chiusura delle porte devono assicurare un agevole e comodo accesso alla persona su sedia a ruote.", ""),
 ("time", "temporizzati", "DM236", "punto 4.1.4", "eventuali sistemi di apertura e chiusura, se automatici, devono essere temporizzati", ""),
 ("time", "tempi sufficienti per l'attraversamento", "DPR503", "art. 6, comma 4", "di comandi manuali accessibili per consentire tempi sufficienti per l'attraversamento da parte di persone che si muovono lentamente", ""),
 ("size", "dimensioni minime", "DM236", "punto 8.1.12", "cabina di dimensioni minime di 1.30 m di profondita' e 0.95 m di larghezza", ""),
 ("capacity", "Portata", "DM236", "punto 8.1.13", "Portata: per le categorie a) b) e c) non inferiore a kg 100 e non superiore a kg. 200", "stair-lift load capacity; lift-car capacity is not stated"),
 ("capacity", "portata utile minima", "DM236", "punto 8.1.13", "La portata utile minima deve essere di kg. 130.", "platform lift"),
 ("distance", "distanza libera", "DM236", "punto 8.1.4", "La distanza libera anteriormente ad ogni tavolo deve essere di almeno 1,50 m", "GENERIC SENSE: clear distance at counters; no distance markers"),
 ("distance", "Distanza misurata in verticale", "DM236", "punto 8.0.1", "ALTEZZA CORRIMANO Distanza misurata in verticale dal lembo superiore dei corrimano al piano di calpestio.", "every height is defined as a vertical distance to the 'piano di calpestio'"),
 ("Ramp gradient (parameter 3)|Slope|gradient", "pendenza delle rampe", "DM236", "punto 8.1.11", "La pendenza delle rampe non deve superare l'8%.", "the held alias 'pendenza della rampa' is singular; the text is plural"),
 ("Ramp gradient (parameter 3)", "La pendenza di una rampa", "DM236", "punto 4.1.11", "La pendenza di una rampa va definita in rapporto alla capacità di una persona su sedia a ruote di superarla e di percorrerla senza affaticamento anche in relazione alla lunghezza della stessa.", "gradient is defined against fatigue and run length, with a pendenza/lunghezza graph for adaptation cases"),
 ("Corridor width (parameter 4)", "larghezza del corridoio", "DM236", "punto 4.1.9", "La larghezza del corridoio e del passaggio deve essere tale da garantire il facile accesso alle unità ambientali da esso servite", "corridor and 'passaggio' together"),
 ("Corridor width (parameter 4)", "I corridoi o i percorsi devono avere una larghezza minima", "DM236", "punto 8.1.9", "I corridoi o i percorsi devono avere una larghezza minima di 100 cm", "8.1.9 heading 'PERCORSI ORIZZONTALI E CORRIDOI'"),
 ("Turning circle (parameter 5)", "inversione di marcia", "DM236", "punto 8.1.9", "ed avere allargamenti atti a consentire l'inversione di marcia da parte di persona su sedia a ruote", "turning is a manoeuvre ('inversione di marcia', 'inversione di direzione'), with the spaces in graphic 8.0.2"),
 ("Turning circle (parameter 5)", "spazi di manovra", "DM236", "punto 8.0.2", "8.0.2 SPAZI DI MANOVRA CON SEDIA A RUOTE.", "the held alias 'spazio di manovra' (singular) does not occur; the diagrams were not read"),
 ("Turning circle (parameter 5)", "circonferenza di diametro 140 cm", "DM236", "punto 8.1.8", "dovranno avere almeno uno spazio entro il quale sia inscrivibile una circonferenza di diametro 140 cm", "balconies: an inscribable circle"),
 ("Turning circle (parameter 5)", "manovra di rotazione", "DM236", "punto 4.1.8", "la manovra di rotazione della sedia a ruote", ""),
 ("Ramp run length (parameter 12)", "LUNGHEZZA DI UNA RAMPA", "DM236", "punto 8.0.1", "LUNGHEZZA DI UNA RAMPA Distanza misurata in orizzontale tra due zone in piano dislivellate e raccordate dalla rampa.", "defined as a horizontal distance"),
 ("Ramp run length (parameter 12)", "sviluppo lineare effettivo della rampa", "DM236", "punto 8.1.11", "Sono ammesse pendenze superiori, nei casi di adeguamento, rapportate allo sviluppo lineare effettivo della rampa.", ""),
 ("Ramp run length (parameter 12)", "Non viene considerato accessibile il superamento di un dislivello superiore a 3,20 m", "DM236", "punto 8.1.11", "Non viene considerato accessibile il superamento di un dislivello superiore a 3,20 m. ottenuto esclusivamente mediante rampe inclinate poste in successione.", "a total-rise cap on ramp series; DPR 503 art. 25 relaxes it for stations"),
]

REGISTER = [  # catalogue 2.1 (32), 2.2 (18), base parameters (10), in that order — same set as FR-FR and DE-DE
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
]
ALIAS = {"slope": "Slope"}
PARTIAL = {  # concept -> why the Italian match is not the English concept (ours)
 "Well-illuminated (if site expected to be lit)": "PARTIAL: stairs and pedestrian crossings only, no quantity",
 "Well illuminated (if required for expected usage)": "PARTIAL: stairs, crossings and lift emergency light only",
 "lighting levels": "PARTIAL: no illuminance quantity anywhere ('illuminamento' and 'lux' 0)",
 "Audio accessibility and communication enhancement technologies": "PARTIAL: voice devices for blind people, audible signals and a deaf-communication symbol; no hearing-enhancement system",
 "Shelter": "NARROWER: reserved parking only, 'preferibilmente'",
 "No open riser": "NARROWER: a sloped riser is preferred; open risers not prohibited",
 "Colour-contrasted and slip-resistant strip on nosing": "DIFFERENT PLACE: a floor band 30 cm before the first and last step; tread slip resistance separately",
 "Tactile attention indicators (truncated domes)": "BROADER: 'percepibile anche da parte dei non vedenti', no device or pattern named",
 "Height clearance (if sheltered or parkade)": "DIFFERENT SENSE: pedestrian obstacle-free height, no vehicle headroom",
 "LRV contrast (parameter 8)": "BROADER: colour/material differentiation, never quantified",
 "force": "PARTIAL: expressed as 'pressione' in kg; the word 'forza' is absent in this sense",
 "distance": "GENERIC SENSE: measured distances; no distance markers",
 "ratio": "PARTIAL: accessible-unit shares and the riser/tread relation, not a room-type mix",
 "level": "SPLIT: 'dislivello' / 'differenze di livello' vs 'livelli di qualità' and 'livelli fuori terra'",
 "capacity": "NARROWER: stair-lift and platform load only",
}
ABSENT = {
 "Drainage": "no drainage rule; 'drenaggio' and 'acque' occur once, inside DPR 503's note quoting the Codice della strada definition of 'Cunetta' (not an accessibility rule)",
 "Microwave mounting height accessible and safe": "'microonde' 0, 'forno' 0; 8.1.7 treats only 'lavello' and 'apparecchio di cottura' with knee space",
 "Accessible lockers": "'armadiett*' 0; nearest are 'cassette per la posta' (4.1.4, 8.1.4) and 'spogliatoi' (4.5) — not lockers",
 "volume": "DIFFERENT SENSE ONLY: 'alto volume di traffico' (DPR 503 art. 6) and 'volumi aggiuntivi' (art. 13); no sound volume",
 "Reverberation time (parameter 7)": "'riverber*' 0; acoustics only as 'percezioni acustiche' (4.3) and an 'isolato sotto il profilo acustico' telephone (DPR 503 art. 31); UNI 11532-2 not attempted",
 "Colour temperature (parameter 10)": "'temperatura' 0, 'kelvin' 0",
}

# Reverse harvest: (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss — OURS)
REV = [
 ("accessibilità", "defined category", "DM236", "art. 2, G)", "Per accessibilità si intende la possibilità, anche per persone con ridotta o impedita capacità motoria o sensoriale, di raggiungere l'edificio e le sue singole unità immobiliari e ambientali, di entrarvi agevolmente e di fruirne spazi e attrezzature in condizioni di adeguata sicurezza e autonomia.", "top grade of three"),
 ("visitabilità", "defined category", "DM236", "art. 2, H)", "Per la visitabilità si intende la possibilità, anche da parte di persone con ridotta o impedita capacità motoria o sensoriale, di accedere agli spazi di relazione e ad almeno un servizio igienico di ogni unità immobiliare.", "partial-access grade; no English register row"),
 ("adattabilità", "defined category", "DM236", "art. 2, I)", "Per adattabilità si intende la possibilità di modificare nel tempo lo spazio costruito a costi limitati", "designed-in future conversion"),
 ("tre livelli di qualità dello spazio costruito", "drafting structure", "DM236", "punto 3.1", "si considerano tre livelli di qualità dello spazio costruito", "the three-grade system"),
 ("accessibilità differita", "defined category", "DM236", "punto 3.1", "l'adattabilità è, pertanto, un'accessibilità differita", "deferred accessibility"),
 ("spazi di relazione", "defined category", "DM236", "art. 2, H)", "Sono spazi di relazione gli spazi di soggiorno o pranzo dell'alloggio e quelli dei luoghi di lavoro, servizio ed incontro, nei quali il cittadino entra in rapporto con la funzione ivi svolta.", "the rooms where a visitor meets the building's function"),
 ("la mancanza di accorgimenti e segnalazioni", "defined category", "DM236", "art. 2, A)", "la mancanza di accorgimenti e segnalazioni che permettono l'orientamento e la riconoscibilità dei luoghi e delle fonti di pericolo per chiunque e in particolare per i non vedenti, per gli ipovedenti e per i sordi.", "a barrier includes the ABSENCE of orientation cues"),
 ("unità ambientale", "defined category", "DM236", "art. 2, B)", "Per unità ambientale si intende uno spazio elementare e definito, idoneo a consentire lo svolgimento di attività compatibili tra loro.", "room-level unit"),
 ("unità immobiliare", "defined category", "DM236", "art. 2, C)", "Per unità immobiliare si intende una unità ambientale suscettibile di autonomo godimento", "dwelling/premises unit"),
 ("parti comuni dell'edificio", "defined category", "DM236", "art. 2, E)", "Per parti comuni dell'edificio si intendono quelle unità ambientali che servono o che connettono funzionalmente più unità immobiliari.", ""),
 ("spazio esterno", "defined category", "DM236", "art. 2, F)", "Per spazio esterno si intende l'insieme degli spazi aperti, anche se coperti, di pertinenza dell'edificio", ""),
 ("adeguamento", "defined category", "DM236", "art. 2, M)", "Per adeguamento si intende l'insieme dei provvedimenti necessari a rendere gli spazi costruiti o di progetto conformi ai requisiti del presente decreto.", "bringing into conformity; triggers relaxed minima"),
 ("visitabilità condizionata", "defined category", "DM236", "punto 5.7", "5.7. VISITABILITÀ CONDIZIONATA.", "access through assisting staff, signalled by a call button"),
 ("pulsante di chiamata", "element", "DM236", "punto 5.7", "deve essere posto in prossimità dell'ingresso un apposito pulsante di chiamata al quale deve essere affiancato il simbolo internazionale di accessibilità", ""),
 ("sistema di chiamata per attivare un servizio di assistenza", "element", "DPR503", "art. 1, comma 5", "di un sistema di chiamata per attivare un servizio di assistenza tale da consentire alle persone con ridotta o impedita capacità motoria o sensoriale la fruizione dei servizi espletati", "interim duty for every public building"),
 ("accessibilità condizionata", "marking", "DPR503", "art. 2, comma 3", "contrassegnato con il simbolo di \"accessibilità condizionata\" secondo il modello di cui all'allegato B", ""),
 ("valore prescritto", "compliance route", "DM236", "punto 7.1", "Le specificazioni contenute nel capo IV art. 8 hanno valore prescritto, le soluzioni tecniche contenute all'art. 9, anche se non basate su tali specificazioni, sono ritenute rispondenti ai criteri di progettazione", "criteria (art. 4-6) / prescribed specifications (art. 8) / deemed-to-comply solutions (art. 9); the heading of art. 9 is 'SOLUZIONI TECNICHE CONFORMI'"),
 ("soluzioni alternative", "compliance route", "DM236", "punto 7.2", "possono essere proposte soluzioni alternative alle specificazioni e alle soluzioni tecniche, purché rispondano alle esigenze sottintese dai criteri di progettazione", "equivalent-outcome route"),
 ("equivalente o migliore qualità degli esiti ottenibili", "compliance route", "DM236", "punto 7.2", "l'alternativa proposta e l'equivalente o migliore qualità degli esiti ottenibili", ""),
 ("criteri di progettazione", "drafting structure", "DM236", "art. 4 heading", "CRITERI DI PROGETTAZIONE PER L'ACCESSIBILITÀ", "aim-level clauses (4.x) each pointing to a specification (8.x)"),
 ("dimostrata impossibilità tecnica", "compliance route", "DM236", "punto 7.5", "sono ammesse deroghe alle norme del presente decreto in caso di dimostrata impossibilità tecnica connessa agli elementi strutturali ed impiantistici", "derogation"),
 ("opere provvisionali", "compliance route", "DPR503", "art. 19, comma 3", "il soddisfacimento del requisito di accessibilità è realizzato attraverso opere provvisionali ovvero, in subordine, con attrezzature d'ausilio e apparecchiature mobili non stabilmente ancorate alle strutture edilizie", "heritage buildings: temporary works"),
 ("manovra combinata", "technique", "DM236", "punto 8.0.2", "sono ammissibili i seguenti spazi minimi di manovra (manovra combinata)", "reduced combined-manoeuvre spaces for adaptation"),
 ("trasferimento laterale", "technique", "DM236", "punto 8.1.6", "lo spazio necessario all'accostamento e al trasferimento laterale dalla sedia a ruote alla tazza w.c.", ""),
 ("raggiungimento dell'apparecchio sanitario", "defined category", "DM236", "punto 8.1.6", "Per raggiungimento dell'apparecchio sanitario si intende la possibilita' di arrivare sino alla diretta prossimita' di esso", "reaching a fixture without transfer: the visitability toilet"),
 ("attrezzabilita' con maniglioni e corrimano", "technique", "DM236", "punto 8.1.6", "deve inoltre essere prevista l'attrezzabilita' con maniglioni e corrimano orizzonatali e/o verticali in vicinanza degli apparecchi", "grab bars fitted to the tenant's needs at allocation; 'orizzonatali' (sic)"),
 ("maniglione", "element", "DM236", "punto 8.1.6", "un maniglione o corrimano per consentire il trasferimento", ""),
 ("lavabo ... del tipo a mensola", "element", "DM236", "punto 4.1.6", "al lavabo, che deve essere del tipo a mensola", "wall-hung basin"),
 ("tipo sospeso", "element", "DM236", "punto 8.1.6", "i w.c. e i bidet preferibilmente sono di tipo sospeso", ""),
 ("doccia deve essere a pavimento", "element", "DM236", "punto 8.1.6", "la doccia deve essere a pavimento", "level-entry shower"),
 ("campanello di emergenza", "element", "DM236", "punto 4.1.6", "la dotazione di opportuni corrimano e di un campanello di emergenza posto in prossimità della tazza e della vasca", ""),
 ("vano vuoto", "element", "DM236", "punto 4.1.7", "Al di sotto dei principali apparecchi e del piano di lavoro va previsto un vano vuoto", ""),
 ("piattaforma di distribuzione", "element", "DM236", "punto 4.1.9", "deve prevedere una piattaforma di distribuzione come vano di ingresso o piano di arrivo dei collegamenti verticali", "landing hub at vertical circulation"),
 ("servoscala", "element", "DM236", "punto 8.1.13", "Per servoscala si intende un'apparecchiatura costituita da un mezzo di carico opportunamente attrezzato per il trasporto di persone con ridotta o impedita capacita' motoria", "stair lift; five defined categories"),
 ("piattaforma servoscala a piattaforma ribaltabile", "element", "DM236", "punto 8.1.13", "d) piattaforma servoscala a piattaforma ribaltabile: per il trasporto di persona su sedia a ruote", ""),
 ("piattaforma elevatrice", "element", "DM236", "punto 4.1.13", "Per servoscala e piattaforma elevatrice si intendono apparecchiature atte a consentire, in alternativa ad un ascensore o rampa inclinata, il superamento di un dislivello", ""),
 ("vano corsa", "element", "DM236", "punto 8.1.13", "Il vano corsa deve avere dimensioni minime pari a m. 0,80x1,20.", ""),
 ("uomo presente", "technique", "DM236", "punto 8.1.13", "devono essere del tipo \"uomo presente\"", "hold-to-run controls"),
 ("marcia in sede propria", "technique", "DM236", "punto 8.1.13", "In alternativa alla marcia in sede propria e' consentita marcia con accompagnatore lungo tutto il percorso", ""),
 ("autolivellamento", "technique", "DM236", "punto 8.1.12", "L'arresto ai piani deve avvenire con autolivellamento", ""),
 ("placca di riconoscimento di piano in caratteri Braille", "element", "DM236", "punto 8.1.12", "in adiacenza alla bottoniera esterna deve essere posta una placca di riconoscimento di piano in caratteri Braille", ""),
 ("numerazione in rilievo", "element", "DM236", "punto 8.1.12", "I pulsanti di comando devono prevedere la numerazione in rilievo e le scritte con traduzione in Braille", ""),
 ("segnalazione sonora dell'arrivo al piano", "element", "DM236", "punto 4.1.12", "Deve essere prevista la segnalazione sonora dell'arrivo al piano e un dispositivo luminoso per segnalare ogni eventuale stato di allarme.", ""),
 ("transenne guida-persone", "element", "DM236", "punto 8.1.4", "Le transenne guida-persone devono essere rigidamente fissate al pavimento", "queue rails"),
 ("attesa sopportabile", "aim", "DM236", "punto 8.1.4", "deve essere consentita un'attesa sopportabile dalla generalita' del pubblico, al fine di evitare l'insorgere di situazioni patologiche di nervosismo e di stanchezza", "waiting stated as a fatigue/stress aim"),
 ("piano di utilizzo", "quantity", "DM236", "punto 8.1.4", "Almeno uno sportello deve evere il piano di utilizzo per il pubblico posto ad altezza pari a 0.90 m.", "counter working height; 'evere' (sic)"),
 ("banconi e i piani di appoggio", "element", "DM236", "punto 4.1.4", "i banconi e i piani di appoggio utilizzati per le normali operazioni del pubblico", ""),
 ("bussole, percorsi obbligati, cancelletti a spinta", "element", "DM236", "punto 4.1.4", "nel caso di adozione di bussole, percorsi obbligati, cancelletti a spinta etc.", ""),
 ("grigliati ... maglie", "element", "DM236", "punto 8.2.2", "I grigliati inseriti nella pavimentazione devono essere realizzati con maglie non attraversabili da una sfera di 2 cm di diametro", "gratings, defined by a sphere test"),
 ("zerbini devono essere incassati", "element", "DM236", "punto 4.1.2", "gli zerbini devono essere incassati e le guide solidamente ancorate", "recessed mats"),
 ("giunture", "quantity", "DM236", "punto 8.2.2", "Gli elementi costituenti una pavimentazione devono presentare giunture inferiori a 5 mm", "paving joints and 'risalti'"),
 ("coefficiente di attrito", "quantity", "DM236", "punto 8.2.2", "il cui coefficiente di attrito, misurato secondo il metodo della British Ceramic Research Association Ltd.", ""),
 ("inattraversabile da una sfera", "technique", "DM236", "punto 8.1.8", "Il parapetto deve avere una altezza minima di 100 cm. ed essere inattraversabile da una sfera di 10 cm. di diametro.", "sphere test for guards"),
 ("visuale anche alla persona seduta", "aim", "DM236", "punto 4.1.3", "Ove possibile si deve dare preferenza a finestre e parapetti che consentono la visuale anche alla persona seduta.", "view out for seated people"),
 ("piano di calpestio", "measurement datum", "DM236", "punto 8.0.1", "ALTEZZA CORRIMANO Distanza misurata in verticale dal lembo superiore dei corrimano al piano di calpestio.", "all heights are measured to the 'piano di calpestio'"),
 ("passo carrabile", "element", "DM236", "punto 4.2.1", "ogni qualvolta il percorso pedonale si raccorda con il livello stradale, o è interrotto da un passo carrabile", "driveway crossing"),
 ("svolte ortogonali", "technique", "DM236", "punto 8.2.1", "ove sia indispensabile effettuare svolte ortogonali al verso di marcia", "turns must be level"),
 ("punti di riferimento ben riconoscibili", "element", "DM236", "punto 4.3", "Per facilitarne l'orientamento è necessario prevedere punti di riferimento ben riconoscibili in quantità sufficiente ed in posizione adeguata.", "orientation landmarks"),
 ("tabelle integrative con scritte in Braille", "element", "DM236", "punto 4.3", "ovvero tabelle integrative con scritte in Braille", ""),
 ("percezioni acustiche che a quelle visive", "aim", "DM236", "punto 4.3", "ogni situazione di pericolo dev'essere resa immediatamente avvertibile anche tramite accorgimenti e mezzi riferibili sia alle percezioni acustiche che a quelle visive", "two-sense hazard warning"),
 ("luogo sicuro statico", "defined category (by reference)", "DM236", "punto 4.6", "La suddivisione in compartimenti, che costituiscono \"luogo sicuro statico\"", "refuge"),
 ("compartimenti antincendio", "technique", "DM236", "punto 4.6", "la suddivisione dell'insieme edilizio in \"compartimenti antincendio\" piuttosto che l'individuazione di \"sistemi di via d'uscita\"", "compartmentation preferred to escape stairs"),
 ("via di esodo accessibile", "element", "DM236", "punto 5.2", "possa essere agevolmente raggiunta una via di esodo accessibile", ""),
 ("spazi liberi riservati per persone su sedia a ruote", "element", "DM236", "punto 5.2", "spazi liberi riservati per persone su sedia a ruote, predisposti su pavimento orizzontale", "wheelchair spaces in halls"),
 ("unità di soggiorno temporaneo", "element", "DM236", "punto 5.3", "almeno il 5% delle superfici destinate alle unità di soggiorno temporaneo", "campsite pitches"),
 ("persone con ridotta o impedita capacità motoria o sensoriale", "population formula", "DM236", "art. 2, G)", "anche per persone con ridotta o impedita capacità motoria o sensoriale", "the instruments' standing population phrase"),
 ("persona su sedia a ruote", "population formula", "DM236", "punto 4.1.1", "anche da parte di persona su sedia a ruote", "the reference user of almost every dimension; held aliases 'carrozzina' / 'persona in carrozzina' do not occur"),
 ("elaborati tecnici", "procedure", "DM236", "punto 10.1", "Gli elaborati tecnici devono chiaramente evidenziare le soluzioni progettuali e gli accorgimenti tecnici adottati", ""),
 ("dichiarazione del professionista abilitato", "procedure", "LAW", "L. 13/1989 art. 1, comma 4", "È fatto obbligo di allegare al progetto la dichiarazione del professionista abilitato di conformità degli elaborati alle disposizioni adottate ai sensi della presente legge.", ""),
 ("almeno un accesso in piano", "element", "LAW", "L. 13/1989 art. 1, comma 3, c)", "almeno un accesso in piano, rampe prive di gradini o idonei mezzi di sollevamento", ""),
 ("inagibili", "procedure", "LAW", "DPR 380/2001 art. 82, comma 6", "nelle quali le difformità siano tali da rendere impossibile l'utilizzazione dell'opera da parte delle persone handicappate, sono dichiarate inagibili", "non-compliant public works declared unusable"),
 ("percorsi attrezzati", "element", "LAW", "DPR 380/2001 art. 78, comma 1", "la realizzazione di percorsi attrezzati e la installazione di dispositivi di segnalazione atti a favorire la mobilità dei ciechi all'interno degli edifici privati", ""),
 ("semafori acustici per non vedenti", "element", "LAW", "DPR 380/2001 art. 82, comma 8", "all'installazione di semafori acustici per non vedenti", ""),
 ("spazi pedonali", "element", "DPR503", "art. 4 heading", "Spazi pedonali", ""),
 ("marciapiede", "element", "DPR503", "art. 5, comma 2", "Il dislivello, tra il piano del marciapiede e zone carrabili ad esso adiacenti non deve comunque superare i 15 cm.", ""),
 ("piattaforme salvagente", "element", "DPR503", "art. 6, comma 3", "Le piattaforme salvagente devono essere accessibili alle persone su sedia a ruote.", "refuge islands"),
 ("persone che si muovono lentamente", "population formula", "DPR503", "art. 6, comma 4", "da parte di persone che si muovono lentamente", "a functional, not diagnostic, population"),
 ("arredo urbano", "element", "DPR503", "art. 9, comma 1", "Gli elementi di arredo nonché le strutture, anche commerciali, con funzione di arredo urbano da ubicare su spazi pubblici devono essere accessibili", "street furniture"),
 ("varchi di accesso con selezione del traffico pedonale", "element", "DPR503", "art. 9, comma 4", "I varchi di accesso con selezione del traffico pedonale devono essere sempre dotati di almeno una unità accessibile.", "turnstiles"),
 ("dissuasori", "element", "DPR503", "art. 10, comma 3", "I posti riservati possono essere delimitati da appositi dissuasori.", ""),
 ("speciale contrassegno", "procedure", "DPR503", "art. 12, comma 1", "Alle persone con capacità di deambulazione sensibilmente ridotta è rilasciato dai comuni, a seguito di apposita documentata istanza, lo speciale contrassegno", "parking permit; extended to blind people (comma 3)"),
 ("studenti non deambulanti o con difficoltà di deambulazione", "population formula", "DPR503", "art. 23, comma 1", "devono assicurare la loro utilizzazione anche da parte di studenti non deambulanti o con difficoltà di deambulazione", ""),
 ("volumi aggiuntivi ... non sono computabili", "procedure", "DPR503", "art. 13, comma 7", "gli eventuali volumi aggiuntivi relativi agli impianti tecnici di sollevamento non sono computabili ai fini della volumetria utile", "lift volumes exempt from floor-area counts"),
 ("simbolo di \"accessibilità\"", "marking", "DPR503", "art. 2, comma 1", "devono recare in posizione agevolmente visibile il simbolo di \"accessibilità\" secondo il modello di cui all'allegato A", ""),
 ("posti riservati disposti parallelamente al senso di marcia", "quantity", "DPR503", "art. 10, comma 2", "Per i posti riservati disposti parallelamente al senso di marcia, la lunghezza deve essere tale da consentire il passaggio di una persona su sedia a ruote tra un veicolo e l'altro.", ""),
]

def norm_ok_phrase(ph, q):
    # a reverse-harvest phrase with ' ... ' is checked part by part
    return all(norm(p).lower() in norm(q).lower() for p in ph.replace('/', '...').split('...') if p.strip())

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def write_instruments():
    man = {}
    for m in os.listdir(R):
        if m.endswith('.jsonl'):
            for line in open(os.path.join(R, m), encoding='utf-8'):
                try: d = json.loads(line)
                except Exception: continue
                if d.get('artefact'): man.setdefault(d['artefact'].split('.')[0], d)
    rows = []
    for k, (title, fs) in INST.items():
        urls = '; '.join(man.get(f, {}).get('url', '?') for f in fs)
        shas = '; '.join(f'{f}:{sha(os.path.join(R, f + ".html"))}' for f in fs)
        tsh = '; '.join(f'{f}.txt:{sha(f"{D}/text/{f}.txt")}' for f in fs)
        rows.append([k, title, len(fs), urls, shas, tsh])
    with open(D + '/instruments-artefacts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['key', 'instrument', 'n_artefacts', 'urls (manifest, in order)', 'artefact_sha256 (raw bytes)', 'text_sha256'])
        w.writerows(rows)

def main():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            tf = where(ins, q); ok = bool(tf) and norm_ok_phrase(ph, q)
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, bool(tf), file=sys.stderr)
            w.writerow([ph, kind, 'it', INST[ins][0], loc, q, tf or '-', 'yes' if ok else 'NO', g])
    rows = []
    for c, ph, ins, loc, q, note in OBS:
        tf = where(ins, q); ok_p = norm(ph).lower() in norm(q).lower()
        if not (tf and ok_p): bad += 1; print('FAIL', ins, loc, ph, bool(tf), ok_p, file=sys.stderr)
        rows.append([c, ph, 'it', INST[ins][0], loc, q, tf or '-', 'yes' if tf and ok_p else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else 'base_parameters')
            hit = [r for r in rows if c in r[0].split('|') or (c in ALIAS and ALIAS[c] in r[0].split('|'))]
            if c in ABSENT:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT[c]])
            elif hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', 'NO NOTE: check']); bad += 1
    write_instruments()
    print('observations', len(rows), 'reverse-harvest', len(REV), 'failures (obs+rev+coverage)', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
