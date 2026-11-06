"""coverage.tsv: one row per register concept (catalogue 2.1 x32, 2.2 x18, base active parameters x10).
n = observations.tsv rows whose concept field contains the register label (shared rows counted for each
label they name). Run from repo root after build.py:  python3 -I <this file>"""
import csv, os
BASE='scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DE-DE'
obs=list(csv.DictReader(open(os.path.join(BASE,'observations.tsv'),encoding='utf-8'),delimiter='\t'))
F='FOUND'; A='SEARCHED-ABSENT'
D_NOTE='DIN 18040 body NOT-OBTAINABLE (paid); headings only.'
R=[
('2.1 Well-illuminated (if site expected to be lit)',F,'ASR treats lighting only as display/text legibility in canteens (Ausleuchtung, Beleuchtung); no level. Lighting is ASR A3.4, not read.'),
('2.1 Surface is firm, stable and slip resistant',F,'ASR frames it as Rutschgefahr for Rollator/Rollstuhl/Gehhilfe plus Rollwiderstand; "firm/stable" has no single German phrase in ASR.'),
('2.1 Seating',F,'Sitzgelegenheiten (ASR); Feste Bestuhlung (DIN heading); BayTB Besucherplätze.'),
('2.1 Handrails',F,'Handläufe (ASR A1.8).'),
('2.1 Clear width',F,'lichte Durchgangsbreite (doors), lichte Breite (escape routes).'),
('2.1 Accessible path of travel',F,'German splits Erschließung (DIN headings) from Verkehrsweg (ASR, includes vehicle routes); BayBO "barrierefrei erreichbar".'),
('2.1 Drainage',F,'Ablaufrinnen (ASR A1.5) only; no site drainage.'),
('2.1 Clear signage',F,'ASR: Sicherheits- und Gesundheitsschutzkennzeichnung, Informations- und Leitsystem; DIN heading Warnen/Orientieren/Informieren/Leiten.'),
('2.1 Audio accessibility and communication enhancement technologies',F,'Headings only (DIN Kommunikationsanlagen, Informations- und Kommunikationshilfen). ASR names no assistive listening system (no Induktion/Höranlage) — that half is SEARCHED-ABSENT in ASR.'),
('2.1 Level landings with clear space',F,'Podeste (ASR A1.8 ramps).'),
('2.1 Floor surface is stable, firm, and non-slip',F,'Same observations as "Surface is firm, stable and slip resistant": a near-duplicate register statement.'),
('2.1 Clear space for approach',F,'Bewegungsfläche + seitliche/frontale Anfahrbarkeit: German carves area and approach direction separately.'),
('2.1 Well illuminated (if required for expected usage)',F,'Shares the observations of "Well-illuminated (if site expected to be lit)".'),
('2.1 Surface is stable, firm, and slip resistant',F,'Near-duplicate; shares observations.'),
('2.1 Shelter',A,'ASR, BayBO Art. 48, BayTB A 4 read in full: no weather shelter. Only Witterungseinflüsse for keeping markings clear. '+D_NOTE),
('2.1 Riser height and tread depth',F,'Phrases Auftritt, Setzstufe present; neither as a stated quantity in ASR. Stair geometry sits in DIN 18065 (BayTB A 4.2.1), not retrieved.'),
('2.1 Nosing design',F,'Stufenvorderkante; Unterschneidung.'),
('2.1 No open riser',F,'geschlossene Stufen.'),
('2.1 Level threshold',F,'schwellenlos; Schwellen.'),
('2.1 Height clearance (if sheltered or parkade)',F,'lichte Höhe appears, but as protection against walking under stairs/escalators (unterlaufen), not vehicle headroom. Parkade headroom SEARCHED-ABSENT.'),
('2.1 Edge protection',F,'seitliche Begrenzung (Radabweiser) on ramps; Absturzsicherungen.'),
('2.1 Colour-contrasted and slip-resistant strip on nosing',F,'Contrast half only (Stufenvorderkante visuell kontrastierend); slip-resistant strip SEARCHED-ABSENT.'),
('2.1 Tactile attention indicators (truncated domes)',F,'Bodenindikatoren, Rippen- oder Noppenplatten; taktil erfassbare Bodenstrukturen. No warning/guidance split in ASR.'),
('2.1 Slope',F,'Längsneigung and Querneigung named separately.'),
('2.1 Sink faucet is easy to use or automatic',F,'Weak: Zapfstelle as a Bedienelement (ASR A4.2); Waschplätze (DIN heading). ASR has no sanitary-room annex at all.'),
('2.1 Outlets and switches are at accessible heights',F,'Schalter yes; outlets (Steckdose) SEARCHED-ABSENT in ASR. German class is Bedienelemente.'),
('2.1 Microwave mounting height accessible and safe',F,'Mikrowelle named, but within a reach area on a work surface, not a mounting height.'),
('2.1 Level landings with clear space and at regular intervals',F,'Shares Podeste observation; interval stated as a length threshold (P12 row).'),
('2.1 Colour-contrasted and slip-resistant strip',F,'Shares the nosing-strip observation; contrast half only.'),
('2.1 Accessible lockers',A,'ASR read in full: no Schließfach/Spind/Garderobe. DIN heading Umkleidebereiche is nearest; body NOT-OBTAINABLE.'),
('2.1 Accessible door hardware',F,'Türgriffe, Beschläge, Drücker; BayTB Greifhöhe für Türdrücker.'),
('2.1 Accessible controls',F,'Bedienelemente is the general German class (any operable element).'),
('2.2 height',F,'Höhe, Greifhöhe, Augenhöhe.'),
('2.2 level',F,'Ambiguous in English (flat / storey / lighting level). Sighted only as niveaugleich (flush).'),
('2.2 width',F,'Breite, Mindestbreite, Verkehrswegbreite.'),
('2.2 clearance',F,'Ambiguous in English: Unterfahrbarkeit (knee), lichte Weite (crush gap), lichte Höhe (headroom) are three German phrases.'),
('2.2 number',F,'Anzahl (BayBO, ASR); BayTB "1 v. H., mindestens jedoch einer".'),
('2.2 slope',F,'Shares P3 observations (Neigung).'),
('2.2 depth',F,'Greiftiefe.'),
('2.2 riser',F,'Setzstufe.'),
('2.2 tread',F,'Auftritt; An- bzw. Austrittsfläche.'),
('2.2 force',F,'Kraftaufwand; aufzuwendende Kraft. Torque (Drehmoment) is separate — see reverse harvest.'),
('2.2 time',F,'Minuten erreichbar (distance as walking time); Schließverzögerung.'),
('2.2 gradient',F,'Shares P3; English slope/gradient are one German word (Neigung).'),
('2.2 size',F,'Mindestgröße der Bewegungsfläche; Schriftgröße.'),
('2.2 volume',A,'ASR read in full: no sound volume or room volume. Lärm (noise) appears without a quantity.'),
('2.2 capacity',F,'BayTB only: Nennlast of a platform lift.'),
('2.2 distance',F,'Sehabstand; Entfernung.'),
('2.2 lighting levels',A,'ASR V3a.2 read in full: no illuminance. Belongs to ASR A3.4, not retrieved.'),
('2.2 ratio',A,'ASR read in full: contrast stated qualitatively only (visuell kontrastierend, kontrastreich); no ratio.'),
('P3 ramp gradient',F,'ASR separates Schrägrampe (geneigter Verkehrsweg, in its scope) from Rampe gemäß DIN 18040-1 Nr. 4.3.8 (out of its scope).'),
('P4 corridor width',F,'DIN headings Flure und sonstige Verkehrsflächen; Flure innerhalb von Wohnungen; ASR Gänge/Verkehrswege.'),
('P5 turning circle',F,'Wendemöglichkeit, Wendevorgang; the area is a square Bewegungsfläche, no circle is named.'),
('P6 operating force',F,'Kraftaufwand für das Öffnen; plus Moment/Drehmoment.'),
('P7 reverberation time',A,'ASR read in full: only "raumakustische Maßnahmen", no reverberation time. DIN 18041 (lead) NOT-READ.'),
('P8 LRV contrast',F,'Contrast found as concept; no LRV or luminance metric. DIN 32975 (lead) NOT-READ.'),
('P9 door width',F,'lichte Durchgangsbreite; DIN heading Türen.'),
('P10 colour temperature',A,'ASR, BayBO, BayTB A 4 read in full: not treated.'),
('P11 headroom clearance',F,'lichte Höhe, in the under-running sense.'),
('P12 ramp run length',F,'Länge (as the trigger for Podeste).'),
]
with open(os.path.join(BASE,'coverage.tsv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f,delimiter='\t',lineterminator='\n')
    w.writerow(['register_concept','status','n_observations','note'])
    for lab,st,note in R:
        n=sum(1 for o in obs if lab in o['concept'])
        assert (n>0)==(st==F), (lab,n,st)
        w.writerow([lab,st,n,note])
from collections import Counter
print(len(R), Counter(st for _,st,_ in R))
