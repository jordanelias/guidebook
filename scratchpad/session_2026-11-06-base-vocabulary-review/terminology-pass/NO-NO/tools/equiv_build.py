"""Build equivalents.tsv for NO-NO and verify every quote verbatim (whitespace-collapsed) in the saved text.
Run from anywhere: python3 -I <this file>. Exits 1 on any quote not found or longer than 25 words.
PDF locators: the page number is COMPUTED here (form feeds in the pdftotext output), never typed."""
import csv, os, re, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(D, 'text')
DIBK = 'https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/'
TEK = 'Byggteknisk forskrift (TEK17) med veiledning, Direktoratet for byggkvalitet'
LOV = ('Forskrift om tekniske krav til byggverk (Byggteknisk forskrift), FOR-2017-06-19-840, Lovdata via Wayback',
       'https://web.archive.org/web/20260620041236if_/https://lovdata.no/dokument/SF/forskrift/2017-06-19-840')
# text file prefix -> (source title as written + issuer, URL, written standard)
S = {
 '9d37f5577e17': (TEK + ', § 8-8', DIBK + '8-8', 'Bokmål'),
 '1ba1e7d900ad': (TEK + ', § 8-3', DIBK + '8-3', 'Bokmål'),
 '69ad69a00a1d': (TEK + ', § 12-9', DIBK + '12-9', 'Bokmål'),
 'cc6cab122620': (TEK + ', Innledning til kapittel 12', DIBK + '12', 'Bokmål'),
 'ce37f178609c': (TEK + ', § 12-1', DIBK + '12-1', 'Bokmål'),
 '5dc3b5719563': (TEK + ', § 12-3', DIBK + '12-3', 'Bokmål'),
 '704b422a78c4': (TEK + ', § 12-14', DIBK + '12-14', 'Bokmål'),
 'ef90f3bc6233': (TEK + ', § 12-16', DIBK + '12-16', 'Bokmål'),
 '81a4557bfaa0': (TEK + ', § 12-13', DIBK + '12-13', 'Bokmål'),
 '91de115cdec1': (TEK + ', § 13-6', DIBK + '13-6', 'Bokmål'),
 '81e3517c278a': (TEK + ', § 15-9', DIBK + '15-9', 'Bokmål'),
 '4d4b347a9c62': (TEK + ', § 15-10', DIBK + '15-10', 'Bokmål'),
 '19fbd13c7304': (TEK + ', § 15-12', DIBK + '15-12', 'Bokmål'),
 'ee277d0188f7': (TEK + ', § 1-3', DIBK + '1-3', 'Bokmål'),
 'ea23447c3072': (LOV[0], LOV[1], 'Bokmål'),
 '8770dbfac182': ('Parkeringstillatelse for forflytningshemmede, Asker kommune', 'https://www.asker.kommune.no/vei-trafikk-og-parkering/parkering/hc-parkering/', 'Bokmål'),
 'ea337b327400': ('Parkeringstillatelsens formål og formelle krav, Bærum kommune', 'https://www.baerum.kommune.no/tjenester/vei-trafikk-og-parkering/parkering/utdypende-informasjon-om-hva-som-vektlegges-i-vurdering-av-soknad-om-parkeringstillatelse/', 'Bokmål'),
 '037448274667': ('Kriteria for søknad om parkeringsløyve for rørslehemma, HC-parkering, Årdal kommune (12.11.2024)', 'https://www.ardal.kommune.no/_f/p1/i4c36604d-f820-4b42-81a6-67cc1157b6bf/kriteria-for-soknad-om-parkeringssloyve-for-rorslehemma.pdf', 'Nynorsk'),
 'a6e08a04f68d': ('Parkeringsløyve, erklæring frå lege, Volda kommune', 'https://volda.kommune.no/_f/p39/i313723b2-ad41-4706-8de2-3ca071aca2ea/parkeringsloyve-erklaring-fra-lege.pdf', 'Nynorsk (mixed with Bokmål forms)'),
 'cfa6795e9ea5': ('Søknad om parkeringslettelse for forflytningshemmede, Nesodden kommune', 'https://nesodden.kommune.no/_f/p86/ide608b41-22cf-452a-aeba-90920b5d823a/soknad-om-parkeringslettelse-for-forflytningshemmede.pdf', 'Bokmål'),
 '444156699d96': ('Parkeringstillatelse for forflytningshemmede, Statens vegvesen', 'https://www.vegvesen.no/trafikkinformasjon/vei-og-skilt/parkering/parkeringstillatelse-for-forflytningshemmede/', 'Bokmål'),
 'd34cae217b97': ('Parkeringsløyve for forflyttingshemma, Statens vegvesen', 'https://www.vegvesen.no/nn/fag/trafikk/parkering/parkeringsloyve-for-forflyttingshemma/', 'Nynorsk'),
 '07e126947678': ('Skilting (parkering), Statens vegvesen', 'https://www.vegvesen.no/fag/trafikk/parkering/skilting/', 'Bokmål'),
 '3ded9d67e541': ('Løfteplattform, nav.no (Arbeids- og velferdsetaten)', 'https://www.nav.no/lofteplattform (served lang="nn"; identical bytes for /lofteplattform/nn)', 'Nynorsk (mixed with Bokmål forms)'),
 '94ace5d8d578': ('Trappeheis og støttesystem i trapp, nav.no (Arbeids- og velferdsetaten)', 'https://www.nav.no/trappeheis (served lang="nn"; identical bytes for /trappeheis/nn)', 'Nynorsk (mixed with Bokmål forms)'),
 'df81349c78b3': ('Universell utforming – hva ser vi etter. Opparbeidet uteareal – kartlegging, tips og råd, KS, hosted by Trondheim kommune', 'https://www.trondheim.kommune.no/contentassets/ea3c893a404c479da01426f809c9576c/opparbeidetuteareal.pdf', 'Bokmål'),
 '622646142631': ('Universell utforming - Notat med innspill til plan for gatenett og gatebruk i Halden sentrum 01.11.24, Halden kommune', 'https://www.halden.kommune.no/_f/p1/i43cb63dc-c805-4f76-9c6c-9f765f2e5211/universell-utforming.pdf', 'Bokmål'),
 'c68df9a7ec30': ('Overordnet klassifisering av tilgjengelighet (bevegelseshemmede) - tettsted, Kartverket (dato 03.03.2022)', 'https://www.kartverket.no/globalassets/geodataarbeid/tilgjengelegheit/klassifikasjoner/klassifisering-av-tilgjengelegheit-i-tettstadar-for-manuelle-rullestolar.pdf', 'Bokmål (URL path Nynorsk, text Bokmål)'),
 'd9931b284a16': ('Universell utforming i kommunal planlegging, Fylkesmannen i Oppland og Hedmark', 'https://innlandetfylke.no/_f/p1/iaaa4cb1e-7f46-4b80-bfbc-c51c37999138/universell-utforming-i-kommuneplanlegging.pdf', 'Bokmål'),
 '9df09132ce0d': ('Merknad til samlet Campus, Norges Handikapforbund Trøndelag (2. mai 2018), hosted by NTNU', 'https://www.ntnu.no/documents/1268425101/1279607513/180502+Norges+Handikapforbund+Tr%C3%B8ndelag.pdf/77696732-f07d-428b-aeea-0dfa2311927e', 'Bokmål'),
}
CL = {'R2-050': 'designated accessible spaces', 'R2-333': 'Accessible', 'R2-163': 'Elevators', 'R2-168': 'Platform lifts',
      'R2-169': 'stair lift', 'R2-170': 'vertical lift', 'R2-174': 'Escalators', 'R2-089': 'Handrails', 'R2-059': 'Curb ramps',
      'R2-083': 'Ramp', 'R2-110': 'Rest area seating', 'R2-109': 'Seating', 'R2-162': 'Entrances', 'R2-549': '(gangatkomst; exterior route)',
      'R2-198': 'Assistive listening systems', 'R2-208': 'Pictogram of accessibility', 'R2-181': 'Toilets', 'R2-551': '(trinnfri; step-free state)',
      'R2-161': 'Level threshold', 'R2-464': '(tilgjengelig; outcome level)', 'R2-463': '(Universell utforming; outcome level)',
      'NOT-IN-REGISTER': 'parking permit for disabled people (gloss ours; no register row)',
      'NOT-IN-REGISTER-2': 'wheelchair lift fitted to a vehicle (gloss ours; no register row)'}
# rows: concept, form, usage_type, scope_note, tier, text prefix, locator (PDF: heading only; page computed), quote, conflation_note
R = [
 # ---- parking: the space
 ('R2-050','parkeringsplasser for forflytningshemmede','code term','names the user group (people with reduced mobility in moving about), not the umbrella word; the space, keyed to where parking is required by plan',1,'9d37f5577e17','§ 8-8 (1) (forskrift)','skal ha tilstrekkelig antall parkeringsplasser for forflytningshemmede der det er stilt krav om parkering',''),
 ('R2-050','Tilrettelagte parkeringsplasser for forflytningshemmede','code term','guidance form with the qualifier "tilrettelagt" (arranged for) on the same object',1,'9d37f5577e17','§ 8-8, veiledning til første ledd','Tilrettelagte parkeringsplasser for forflytningshemmede er en viktig forutsetning for tilgjengelighet til byggverk',''),
 ('R2-050','forbeholdt forflytningshemmede','code term','sign-content phrase (reserved for); the sign must say it',1,'9d37f5577e17','§ 8-8 (1) c, preakseptert ytelse','må ha skilt med informasjon om at plassen er forbeholdt forflytningshemmede, og',''),
 ('R2-050','parkeringsplasser reservert for forflytningshemmede','code term','road-authority form for the same space, defined by what the permit allows',4,'444156699d96','Hvor gjelder parkeringstillatelsen?','kan du parkere på parkeringsplasser reservert for forflytningshemmede.',''),
 ('R2-050','reservert parkeringsplass','colloquial','municipal plain-language form; sign named "HC- symbol"',4,'8770dbfac182','page lead','Tillatelsen gir deg rett til å parkere på offentlig skiltet og reservert parkeringsplass, som er skiltet med HC- symbol',''),
 ('R2-050','plass for forflytningshemmede','colloquial','short form in municipal guidance',4,'ea337b327400','Forflytningshemmet passasjer?','en må flytte motorvognen når det finnes en ledig plass for forflytningshemmede',''),
 ('R2-050','plass for rørslehemma','regional variant','Nynorsk user-group word "rørslehemma" for Bokmål "forflytningshemmede"; same object',4,'037448274667','Rørslehemma passasjer?','når det er ein ledig plass for rørslehemma',''),
 ('R2-050','dei reserverte plassane','colloquial','Nynorsk; reserved spaces',4,'037448274667','Rørslehemma passasjer?','dersom dei reserverte plassane er opptekne av',''),
 ('R2-050','HC-parkering','colloquial','municipal guidance heading for the space; HC from "handikap" (gloss ours); 0 occurrences in TEK17 texts read',4,'df81349c78b3','HC-parkering','Innendørs og utendørs HC-parkering.',''),
 ('R2-050','HC-parkeringsplass','colloquial','single space',4,'df81349c78b3','HC-parkering','Størrelse og skilting av HC-parkeringsplass',''),
 ('R2-050','HC-Parkeringsplass','colloquial','national mapping agency field name; capitalisation as printed',4,'c68df9a7ec30','table, Parkeringsområde','HC-Parkeringsplass',''),
 ('R2-050','HC-parkering','colloquial','street-level note',4,'622646142631','HC-parkering','HC-parkering langs fortau må ha tilstrekkelig areal bak',''),
 ('R2-050','HC plasser','colloquial','DPO usage (Co-1): no hyphen; the national DPO uses the HC- prefix itself',5,'9df09132ce0d','Parkering og trafikk','stiller krav om et minimumsantall HC plasser for viklårsparkering',''),
 ('R2-050','HC-parkering','colloquial','Nynorsk document title; here the heading names the permit scheme',4,'037448274667','title','Kriteria for søknad om parkeringsløyve for rørslehemma, HC-parkering','CONFLATION: "HC-parkering" is used for the space (KS/Trondheim p.7 heading, Halden) and, in this title, for the permit scheme; recorded, not resolved'),
 ('R2-050','Kapasitet UU','code term','mapping field: count of spaces meeting universell utforming; "UU" abbreviation',4,'c68df9a7ec30','table, Parkeringsområde','Kapasitet UU','NOTE: "UU" (universell utforming) used as a qualifier of parking spaces; the parking form elsewhere in the same table is "HC-Parkeringsplass"'),
 # ---- parking: the permit (no register row)
 ('NOT-IN-REGISTER','parkeringstillatelse for forflytningshemmede','code term','the permit, not the space; title term of FOR-2016-03-18-264 as cited by the road authority (statute itself not obtained)',4,'444156699d96','page heading','Parkeringstillatelse for forflytningshemmede blir iblant omtalt som HC‑kort.',''),
 ('NOT-IN-REGISTER','HC-kort','colloquial','the road authority states the equivalence itself ("iblant omtalt som")',4,'444156699d96','page end','Parkeringstillatelse for forflytningshemmede blir iblant omtalt som HC‑kort.','CONFLATION: the card (HC-kort) and the permit (parkeringstillatelse) are treated as one; quote uses U+2011 non-breaking hyphen'),
 ('NOT-IN-REGISTER','HC-kort','colloquial','municipal usage',4,'8770dbfac182','page lead','Du kan søke om parkeringstillatelse, også kalt HC-kort',''),
 ('NOT-IN-REGISTER','Parkeringsløyve for forflyttingshemma','regional variant','Nynorsk official form of the road authority (forflyttingshemma, not rørslehemma)',4,'d34cae217b97','page heading','Parkeringsløyve for forflyttingshemma',''),
 ('NOT-IN-REGISTER','parkeringsløyve for rørslehemma','regional variant','Nynorsk municipal form',4,'037448274667','title','Kriteria for søknad om parkeringsløyve for rørslehemma',''),
 ('NOT-IN-REGISTER','parkeringsløyve for forflytningshemma','regional variant','Nynorsk ending on a Bokmål stem; the same document also writes "rørslehemma"',4,'a6e08a04f68d','header','Som vedlegg til søknad om parkeringsløyve for forflytningshemma','CONFLATION (orthographic): one document mixes forflytningshemma and rørslehemma, and cites the regulation misspelt "forflyttningshemmede"'),
 ('NOT-IN-REGISTER','parkeringslettelse for forflytningshemmede','colloquial','names the relief the permit gives; used as the form title',4,'cfa6795e9ea5','form title','Skjema for søknad om parkeringslettelse for forflytningshemmede','CONFLATION: relief (lettelse) and permit (tillatelse) used for one application: the same form also heads itself "Søknad om parkeringstillatelse for"'),
 ('NOT-IN-REGISTER','kommunalt bevis','outdated or disfavoured','permit form carried from the parking regulation wording; usage note: older term, kept because the road authority still prints it (our reading, unratified)',3,'07e126947678','Krav om skilting av betalingsplikt for forflytningshemmede','gratis for forflytningshemmede med kommunalt bevis',''),
 # ---- umbrella qualifier
 ('R2-333','universell utforming','code term','the instrument\'s umbrella; defined as a LEVEL for public and work buildings (main solution usable by as many as possible, on equal terms); wider than "tilgjengelig"',1,'cc6cab122620','Begreper brukt i kapittel 12','Utforming eller tilrettelegging av hovedløsningen i de fysiske forholdene slik at virksomhetens alminnelige funksjon kan benyttes av flest mulig.',''),
 ('R2-333','universelt utformet','code term','adjectival form of the same level',1,'ce37f178609c','§ 12-1 (2) (forskrift)','Byggverk for publikum og arbeidsbygninger skal være universelt utformet slik det følger av bestemmelsene i forskriften',''),
 ('R2-333','tilgjengelig','code term','a LOWER defined level for some dwellings; narrower than universell utforming',1,'cc6cab122620','Innledning til kapittel 12','Uttrykket tilgjengelig brukes om et kvalitetsnivå der ikke alle kravene til universell utforming gjelder.','CONFLATION within one page: the design basis for "tilgjengelig" is given as a manual or combined indoor-outdoor electric wheelchair user in the introduction, and as a manual wheelchair user with full upper-body function under Begreper; recorded, not resolved'),
 ('R2-333','tilgjengelig','code term','second definition on the same page',1,'cc6cab122620','Begreper brukt i kapittel 12','Dimensjoneringsgrunnlaget er person med full førlighet i overkroppen i manuell rullestol.','see the row above'),
 ('R2-333','tilgjengelig','qualifier','non-disability sense: reachable for maintenance',1,'4d4b347a9c62','§ 15-10 (1) a (forskrift)','være lett tilgjengelig for drift, vedlikehold og sikkerhetskontroll','CONFLATION: same form, ordinary sense "reachable"; a text match here is not a sense match'),
 ('R2-333','tilgjengelighet','qualifier','noun; the guide states it asks less than universell utforming',4,'d9931b284a16','2.2 Universell utforming og tilgjengelighet','Tilgjengelighetsbegrepet stiller ikke så store krav som universell utforming.',''),
 ('R2-333','tilgjengelig parkeringstilbud','qualifier','"tilgjengelig" on parking in the permit regulation § 1, quoted by a municipality (statute not obtained); not TEK17\'s defined level',4,'ea337b327400','page body, quoting forskriften § 1','å gi forflytningshemmede med et reelt behov for parkeringslette et tilgjengelig parkeringstilbud','CONFLATION: "tilgjengelig" as TEK17 defined level vs as a general qualifier in road-traffic regulation'),
 ('R2-333','tilrettelagt','qualifier','"arranged for"; applied to the parking object in guidance',1,'9d37f5577e17','§ 8-8, veiledning til første ledd','Tilrettelagte parkeringsplasser for forflytningshemmede',''),
 ('R2-333','Delvis tilgjengelig','qualifier','a graded middle class (green/yellow/red) for manual wheelchairs; scope: one user group',4,'c68df9a7ec30','table header','Egenskap Tilgjengelig Delvis tilgjengelig Ikke tilgjengelig',''),
 ('R2-333','Tilgjengelighet for alle','outdated or disfavoured','title of the earlier policy circular T-5/99 B, cited in a 2024 note; usage note: an older national framing before universell utforming (our reading)',4,'622646142631','list of references','T-5/99 B Tilgjengelighet for alle',''),
 ('R2-333','HC','colloquial','prefix used as a qualifier: HC-parkering, HC toalett, HC løsninger; from "handikap" (gloss ours); used by the DPO itself',5,'9df09132ce0d','Tilgjengelighet','erfarer at midlertidige HC løsninger ikke dekker kravet for universell utforming','CONFLATION: the DPO contrasts "HC løsninger" with "universell utforming", treating HC as a lower or ad-hoc standard'),
 ('R2-333','universelt utformede','qualifier','DPO usage applied to routes',5,'9df09132ce0d','Tilgjengelighet','fordrer at det etableres universelt utformede traseer på hele campusområdet',''),
 ('R2-333','rullestolvennlig','unattested seed','MODEL-GENERATED, flagged; W5 found no Norwegian public source using it; narrower (wheelchair users only)','seed','','','',''),
 ('R2-333','handikapvennlig','unattested seed','MODEL-GENERATED, flagged; W5 found no Norwegian public source; if attested, likely disfavoured','seed','','','',''),
 ('R2-463','universell utforming','code term','definitional statement in TEK17 guidance: equal terms, no separate entrances',1,'cc6cab122620','Hovedløsning – universell utforming','Det skal for eksempel ikke være egne innganger for personer i rullestol.',''),
 ('R2-464','Tilgjengelig boenhet','code term','defined dwelling class',1,'cc6cab122620','Begreper brukt i kapittel 12','Tilgjengelig boenhet',''),
 # ---- vertical transport
 ('R2-163','heis','code term','the passenger elevator; requirement heading',1,'ea23447c3072','§ 12-3 (1)','Det er krav om heis i byggverk for publikum og i arbeidsbygninger med to etasjer eller flere.',''),
 ('R2-163','Heiser','code term','section heading for elevators',1,'81e3517c278a','§ 15-9 heading','§ 15-9. Heiser',''),
 ('R2-163','heisstol','code term','the car only (part of the elevator), not the installation',1,'ea23447c3072','§ 12-3 (1) a','skal minst én heisstol ha innvendig størrelse på minimum 1,1 m x 2,1 m.',''),
 ('R2-163','Personheiser','code term','in a cited EN 81 title; narrower (passenger only)',1,'81e3517c278a','§ 15-9, Henvisninger','Fjernalarm på personheiser og vare- og personheiser',''),
 ('R2-163','vanleg heis','colloquial','Nynorsk; the ordinary elevator, named by contrast with sjaktheis',4,'3ded9d67e541','page body','Den skil seg frå vanleg heis ved at ein må halde inne ein knapp heile tida under forflytning.',''),
 ('R2-163','løfteinnretning','code term','WIDER umbrella: elevators, platform lifts, escalators, moving walks and stair lifts',1,'81e3517c278a','§ 15-9, veiledning til bestemmelsene om løfteinnretninger','omfatter begrepet “løfteinnretning” heiser, løfteplattformer, rulletrapper, rullende fortau og trappeheiser.','CONFLATION: one umbrella word covers the register\'s Elevators, Platform lifts, stair lift and Escalators'),
 ('R2-168','løfteplattform','code term','platform lift; may replace an elevator in low-traffic buildings of up to three storeys',1,'ea23447c3072','§ 12-3 (1)','I byggverk med inntil tre etasjer og med liten persontrafikk kan løfteplattform erstatte heis.',''),
 ('R2-168','Løfteplattformer','code term','section heading',1,'19fbd13c7304','§ 15-12 heading','§ 15-12. Løfteplattformer',''),
 ('R2-168','sjaktheis','colloquial','Nynorsk public-body form: a platform lift in a shaft, named "heis"',4,'3ded9d67e541','page body','nyttast løfteplattform med sjakt, også kalt sjaktheis.','CONFLATION: "heis" is used for a platform lift (sjaktheis) and distinguished in the same sentence from "vanleg heis"; the CA/US lift-vs-elevator split runs the other way here'),
 ('R2-168','løfteplattform utan sjakt','code term','Nynorsk; unenclosed platform lift; outdoors an alternative to a ramp',4,'3ded9d67e541','page body','Løfteplattform utan sjakt kjem i ulike utgåver for å utjamne mindre nivåforskjellar.',''),
 ('R2-170','Vertikal løfteplattform','code term','cited NS-EN 81-41 title; the platform travelling vertically',1,'19fbd13c7304','§ 15-12, Henvisninger','NS-EN 81-41:2010 Vertikal løfteplattform for bruk av personer med svekket bevegelighet',''),
 ('R2-169','trappeheiser','code term','stair lifts, listed under the umbrella',1,'81e3517c278a','§ 15-9, veiledning','heiser, løfteplattformer, rulletrapper, rullende fortau og trappeheiser.',''),
 ('R2-169','trappeheis med sete','code term','Nynorsk public-body form; seated stair lift',4,'94ace5d8d578','page body','Trappeheis med sete går på ei skinne.',''),
 ('R2-169','trappeheis med plattform','code term','Nynorsk; platform stair lift (wheelchair drives on)',4,'94ace5d8d578','page body','kan trappeheis med plattform vere eit alternativ.','CONFLATION: a platform stair lift is a stair lift and a platform; the page also calls the whole class "Heis med sete eller plattform"'),
 ('R2-169','Heis med sete eller plattform','colloquial','page lead: "heis" used for a stair lift',4,'94ace5d8d578','page lead','Heis med sete eller plattform slik at du kan bruke trapp sjølv om du har nedsatt gangfunksjon.','CONFLATION: "heis" names a stair lift here and an elevator in TEK17'),
 ('R2-174','rulletrapper','code term','escalators, listed under løfteinnretning',1,'81e3517c278a','§ 15-9, veiledning','heiser, løfteplattformer, rulletrapper, rullende fortau og trappeheiser.',''),
 ('NOT-IN-REGISTER-2','rullestolheis','colloquial','a wheelchair lift in a car, not a building lift',4,'ea337b327400','page body','har ofte rullestolheis/rampe i bilen','CONFLATION: "rullestolheis" (vehicle device) and "rampe" (vehicle device) sit beside the building senses of heis and rampe'),
 # ---- other concepts (breadth)
 ('R2-089','håndløper','code term','handrail (TEK17 wording; terminology per NS-EN 14076)',1,'704b422a78c4','§ 12-14 (1) a (forskrift)','Trappen skal ha sikker avgrensing og håndløper på begge sider.',''),
 ('R2-089','håndlist','outdated or disfavoured','handrail in TEK10 wording, quoted in a planning guide; TEK17 uses håndløper (usage note: superseded code term, still current in public-body tables)',4,'d9931b284a16','TEK10 extract (TEK10 numbering: § 12-16. Trapp)','Trapp skal ha sikker avgrensing og ha håndlist på begge sider.',''),
 ('R2-089','Håndlist','colloquial','national mapping field name for ramp handrails',4,'c68df9a7ec30','table, Om det finnes en rampe','Håndlist Begge sider Minst en side ingen',''),
 ('R2-059','nedsenket kantstein','code term','a lowered kerb at a crossing, set at a height above street level; municipal planning text',4,'d9931b284a16','planning provisions, gangareal','Det skal anlegges nedsenket kantstein med høyde på 20 mm fra gatenivå','NOTE: TEK17 texts read name "kantstein" only as an edge boundary (§ 8-5, 8-6, 8-7 veiledning), not as a ramp'),
 ('R2-059','Nedsenk','code term','mapping field for the lowered kerb at a crossing',4,'c68df9a7ec30','table, Om "gatetype" er "gangfelt"','Nedsenk1 ≤ 2,5 cm > 2,5 cm',''),
 ('R2-083','Rampe','code term','defined as a construction giving a step-free link between two levels; a path following the terrain is not a ramp',1,'ef90f3bc6233','§ 12-16, veiledning til bestemmelsen','En gangvei eller atkomst som følger terrenget regnes ikke som rampe.','CONFLATION (owner example, ramp = slope vs device): TEK17 separates the ramp element from a sloped walkway; "rampe i bilen" (Bærum) is a vehicle device'),
 ('R2-110','Hvilebenk','code term','rest bench; mapping field (first pass found 0 "hvilebenk" in TEK17 texts)',4,'c68df9a7ec30','table','Sittegruppe/Hvilebenk',''),
 ('R2-109','sitteplasser','code term','seating',1,'1ba1e7d900ad','§ 8-3 (5) d (forskrift)','',''),
 ('R2-162','hovedinngang','code term','the main entrance (parking near it)',1,'9d37f5577e17','§ 8-8 (1) a (forskrift)','Parkeringsplassen skal være nær hovedinngang.',''),
 ('R2-162','InngangBygg','code term','mapping object name for a building entrance',4,'c68df9a7ec30','table','InngangBygg',''),
 ('R2-549','Atkomstvei','code term','mapping field for the approach route; compare TEK17 defined "gangatkomst"',4,'c68df9a7ec30','table, InngangBygg','Atkomstvei stigning',''),
 ('R2-551','trinnfri atkomst','qualifier','step-free access, cited as information about services',4,'d9931b284a16','extract on tilgjengelighet','for eksempel om det er trinnfri atkomst, heis osv.',''),
 ('R2-161','Terskler skal være trinnfrie','code term','threshold defined by the trinnfri state',1,'81a4557bfaa0','§ 12-13 (3) c (forskrift)','Terskler skal være trinnfrie.',''),
 ('R2-161','Terskelhøyde','code term','mapping field (threshold height)',4,'c68df9a7ec30','table','Terskelhøyde ≤ 2,5 cm > 2,5 cm',''),
 ('R2-198','teleslynge','code term','hearing loop; NARROWER than assistive listening systems',1,'91de115cdec1','§ 13-6 (4), preakseptert ytelse','installeres teleslynge eller annet mikrofonbasert trådløst overføringsutstyr',''),
 ('R2-208','rullestolsymbol','code term','the wheelchair symbol marked on the parking surface',1,'9d37f5577e17','§ 8-8 (1) c, preakseptert ytelse','merkes med rullestolsymbol på dekket.',''),
 ('R2-208','piktogram for Rullestol','colloquial','municipal guidance form for the same symbol',4,'df81349c78b3','HC-parkering','Skilting med piktogram for Rullestol.',''),
 ('R2-208','HC- symbol','colloquial','municipal form, spacing as printed',4,'8770dbfac182','page lead','som er skiltet med HC- symbol',''),
 ('R2-181','HC toalett','colloquial','DPO usage; whether single-user room or WC is not stated (sense not judged)',5,'9df09132ce0d','Studenter og ansatte','nødvendige fasiliteter foruten HC toalett må være i nærheten',''),
]
def norm(s): return re.sub(r'\s+', ' ', s).strip()
out, bad = [], 0
for c, form, ut, scope, tier, tf, loc, q, conf in R:
    if tier == 'seed':
        out.append([c, CL[c], form, 'no', 'NO', ut, scope, 'seed', '', '', '', conf, '']); continue
    if not q: q = form  # quote the form itself where the row carries no longer quote
    fn = os.path.join(T, tf + '.txt'); raw = open(fn, encoding='utf-8').read()
    if len(q.split()) > 25: print('TOO LONG', form); bad += 1
    if norm(q) not in norm(raw): print('QUOTE NOT FOUND', tf, q); bad += 1; continue
    src, url, ws = S[tf]
    if '\f' in raw:  # pdftotext: compute page
        pages = raw.split('\f'); pg = next(i for i, p in enumerate(pages, 1) if norm(q) in norm(p) or norm(q)[:40] in norm(p))
        loc = f'p. {pg}' + (f', {loc}' if loc else '')
    out.append([c, CL[c], form, f'no ({ws})', 'NO', ut, scope, str(tier), f'{src}, {url}', loc, q, conf, tf + '.txt'])
hdr = ['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note', 'attestation_tier', 'source', 'locator', 'quote', 'conflation_note', 'text_file']
with open(os.path.join(D, 'equivalents.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(hdr); w.writerows(out)
print(f'rows {len(out)}, failures {bad}')
sys.exit(1 if bad else 0)
