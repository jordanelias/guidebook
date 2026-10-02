import json, os, subprocess, sys
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
SESSION='session_2026-10-01-research-batch-23'
SLUG='accessible-circulation-geometry'
E=[]
def add(ref, juris, ctype, cv, unit, cmp_, role, text, section, notes, locs=None, device='not_device_scoped', root_type='committee_assertion', paradigm='stated_unmeasured', setting=None, rpn=None):
    E.append(dict(ref=ref, juris=juris, ctype=ctype, cv=cv, unit=unit, cmp=cmp_, role=role, text=text, section=section, notes=notes, locs=locs or {}, device=device, root_type=root_type, paradigm=paradigm, setting=setting, rpn=rpn))

# ---- KR REF-01019
add('REF-01019','KR','numerical','1:12','rise:run ratio (maximum; the rule writes 12분의 1)','<=','claim',
 '경사로의 기울기는 12분의 1 이하로 하여야 한다.','별표 1 제12호 나목(1)',
 "MANDATORY, NOT ADVISORY: the page's own 비고 states that items phrased '…할 수 있다' are recommendations (권장사항); this item is phrased '하여야 한다' (shall). A DISTINCT ELEMENT NOT EXTRACTED HERE: item 1 나목(1) sets the gradient of an 접근로 (approach path) at 18분의 1 or less, relaxed to 12분의 1 where terrain makes that difficult -- an approach path, not a 경사로 (ramp); route-vs-ramp scope is GAP-033's open question. SOURCE QUALITY: retrieved from a non-governmental legal wiki (NEPLA) reproducing the rule text under the amendment stamp <개정 2023. 12. 11.>; the official host (law.go.kr) was unreachable from this environment (TLS connection reset, curl exit 35), hence verification UNVERIFIED and metadata GREY. The issuing ministry is not stated in the retrieved page, and currency after the 2023-12-11 stamp is unconfirmed.",
 dict(scheme='section', section='별표 1 제12호', subsection='나', paragraph='1'))
add('REF-01019','KR','numerical','1:8','rise:run ratio (conditional relaxation ceiling; all three conditions required)','<=','condition',
 '다음의 요건을 모두 충족하는 경우에는 경사로의 기울기를 8분의 1까지 완화할 수 있다. (가) 신축이 아닌 기존시설에 설치되는 경사로일 것 (나) 높이가 1미터 이하인 경사로로서 시설의 구조 등의 이유로 기울기를 12분의 1이하로 설치하기가 어려울 것 (다) 시설관리자 등으로부터 상시보조서비스가 제공될 것',
 '별표 1 제12호 나목(2)',
 "THE ONLY RELAXATION IN THE RULE IS CONDITIONED ON HUMAN ASSISTANCE. All of: (가) an existing, not new, facility; (나) ramp height 1 m or less and 1/12 structurally difficult; (다) continuous assistance service provided by the facility manager (상시보조서비스). No other source in this corpus makes a steeper ramp conditional on a staffing provision. The verb is 완화할 수 있다 (may be relaxed): a permission, read as a permission and not as a 비고 recommendation.",
 dict(scheme='section', section='별표 1 제12호', subsection='나', paragraph='2'))

# ---- NL REF-01020 Staatsblad
stb_note_common = " TIER ADDED BY THE 2024 AMENDING DECREE; in force 1 July 2025 (Artikel II lid 2 lists onderdeel R). The operative text is an AMENDMENT, so the lead-in of art. 4.30 lid 2 is not reproduced in it: the comparator '<=' is read from the tiers' function and from IPLO's statement of the article ('De hellingbaan mag niet te steil zijn (artikel 4.30 Bbl)', REF-01021)."
add('REF-01020','NL','numerical','1:6','rise:run ratio (maximum) where the height difference is <= 0.05 m','<=','claim',
 '1 : 6 als het hoogteverschil niet groter is dan 0,05 m','Stb. 2024, 368, art. I onderdeel R, art. 4.30 lid 2 onder a (nieuw)',
 "STEEPEST RAMP TIER IN ANY SOURCE OF THIS CORPUS, for a threshold-scale rise." + stb_note_common,
 dict(scheme='section', section='Stb. 2024, 368 art. I onderdeel R', subsection='art. 4.30 lid 2', paragraph='a'))
add('REF-01020','NL','numerical','1:10','rise:run ratio (maximum) where the height difference is > 0.05 m and <= 0.10 m','<=','claim',
 '1 : 10 als het hoogteverschil groter is dan 0,05 m, maar niet groter dan 0,10 m','Stb. 2024, 368, art. I onderdeel R, art. 4.30 lid 2 onder b (nieuw)',
 "RISE-CONDITIONED TIER." + stb_note_common,
 dict(scheme='section', section='Stb. 2024, 368 art. I onderdeel R', subsection='art. 4.30 lid 2', paragraph='b'))
add('REF-01020','NL','numerical','1:12','rise:run ratio (maximum) where the height difference is > 0.10 m and <= 0.25 m','<=','claim',
 '1 : 12 als het hoogteverschil groter is dan 0,10 m, maar niet groter dan 0,25 m','Stb. 2024, 368, art. I onderdeel R, art. 4.30 lid 2 onder c (nieuw)',
 "REWORDED FROM THE FORMER FIRST TIER ('Onderdeel c (nieuw) komt te luiden'; the former a-c are re-lettered c-e). The 1:16 and 1:20 tiers for larger rises are unchanged text and are NOT in this decree's pages; they are stated in REF-01021 (IPLO)." + stb_note_common,
 dict(scheme='section', section='Stb. 2024, 368 art. I onderdeel R', subsection='art. 4.30 lid 2', paragraph='c'))
add('REF-01020','NL','qualitative','the added small-rise tiers (1:6, 1:10) were taken from draft NEN 9120, the Dutch elaboration of NEN-EN 17210','','','finding',
 'De toegevoegde afmetingen van de helling zijn overgenomen uit de in ontwikkeling zijnde NEN 9120 «Nederlandse uitwerking van NEN-EN 17210 Prestatie eisen voor toegankelijkheid en bruikbaarheid van gebouwen».',
 'Stb. 2024, 368, nota van toelichting, onderdeel R (PDF p. 35)',
 "LINEAGE OF THE SMALL-RISE VALUES: they do not originate with the Dutch legislator; the nota says they come from NEN 9120 (then in development), itself the Dutch elaboration of EN 17210 (European). NEN 9120:2025 and EN 17210:2021 are paywalled and were not retrieved (research_code_leads). A DISCREPANCY INSIDE THE SOURCE: the nota says 'tot 5 mm en tussen 5 en 10 mm' where the operative text reads 0,05 m and 0,10 m (5 and 10 cm); the operative text governs and the nota's 'mm' is read as a slip -- flagged, not corrected.",
 dict(scheme='section', section='Stb. 2024, 368 nota van toelichting', subsection='onderdeel R'))
# ---- NL REF-01021 IPLO
iplo_note = " Government guidance page (Informatiepunt Leefomgeving) restating Bbl art. 4.30. NOT an independent source for the 1:6, 1:10 and 1:12 rows, which are the Staatsblad's (REF-01020) and are not re-extracted here (point, do not copy). The 1:16 and 1:20 rows rest on IPLO's restatement alone: the legal text of those two rows was not retrieved (wetten.overheid.nl closed the connection, HTTP/2 PROTOCOL_ERROR then empty reply; inview.nl returned 403). The same page states maximum ramp height 1 m and minimum width 1.1 m (other parameters)."
add('REF-01021','NL','numerical','1:16','rise:run ratio (maximum) where the height difference is > 0.25 m and <= 0.50 m','<=','claim',
 '> 25 cm en ≤ 50 cm 1 : 16 Bij een hoogteverschil van 40 cm, moet de lengte minstens 640 cm zijn','IPLO, Helling, Tabel: steilte hellingbaan (art. 4.30 Bbl)',
 "RISE-CONDITIONED TIER." + iplo_note, dict(scheme='section', section='Tabel: steilte hellingbaan', paragraph='rij 4'))
add('REF-01021','NL','numerical','1:20','rise:run ratio (maximum) where the height difference is > 0.50 m and <= 1.00 m','<=','claim',
 '> 50 cm en ≤ 100 cm 1 : 20 Bij een hoogteverschil van 60 cm, moet de lengte minstens 1200 cm zijn','IPLO, Helling, Tabel: steilte hellingbaan (art. 4.30 Bbl)',
 "GENTLEST TIER; THE ONLY ONE THAT GOVERNS A RAMP OF NORMAL RISE (0.5-1.0 m)." + iplo_note, dict(scheme='section', section='Tabel: steilte hellingbaan', paragraph='rij 5'))
# ---- NL REF-01022 Ieder(in)
add('REF-01022','NL','qualitative','supports adjusting the ramp (hellingbaan) requirements to align with draft NEN 9120; hopes other parts of the regulation follow once the standard is finished','','','claim',
 'De eisen voor hellingbanen worden aangepast zodat ze in lijn zijn met de NEN- norm 9120 die in ontwikkeling is. Ieder(in) ondersteunt de implementatie van deze NEN-norm','Letter p. 1, third bullet',
 "A DPO ENDORSEMENT WITHOUT A FIGURE: the letter states no gradient value and voices no criticism of the Bbl tiers. It is evidence that the national disability network was consulted on, and supported, the ramp tiers Stb. 2024/368 (REF-01020) took from NEN 9120; it is NOT evidence that those tiers are acceptable to wheelchair users in use (contrast REF-01025, FUB 2007, which calls 1:12 a safety risk). The same letter supports a 2 cm maximum threshold height for balconies -- out of scope. Dated 9 November 2023, i.e. before the amendment was made (25 November 2024).",
 dict(scheme='section', section='Letter p. 1', paragraph='bullet 3'),
 rpn="Ieder(in) describes itself in the retrieved letter as 'het netwerk van mensen met een beperking of chronische ziekte' -- people with any disability or chronic illness, not wheelchair users in particular. No individual authors or consulted members are named; the letter is signed by the director.")
# ---- SE REF-01023
add('REF-01023','SE','numerical','1:12','rise:run ratio (maximum; a ramp provided to meet the accessibility requirements in a new building)','<=','claim',
 'En ramp, som är till för att uppfylla kraven enligt 1 § och 2 § andra stycket, ska luta högst 1:12.','BFS 2024:12, 2 kap. 4 §',
 "BINDING FÖRESKRIFT ('ska'), in force 1 July 2025 (PDF p. 9, point 1); applies under '2 kap. Utformningskrav vid uppförande av nya byggnader'. It replaces the accessibility provisions of the former BBR (BFS 2011:6); the transitional point 2 lets older BBR provisions be applied only as BFS 2024:14 point 3 allows. The same 1:12 ceiling is set for plot walkways in BFS 2024:13 2 kap. 3 § (retrieved, staged as a candidate and not extracted: route-vs-ramp scope, GAP-033). The public-places regulation (REF-01024) carries a GENERAL ADVICE of 1:20 -- Sweden holds two figures for two settings.",
 dict(scheme='section', section='2 kap.', paragraph='4 §'))
add('REF-01024','SE','numerical','1:20','rise:run ratio (advised maximum between landings at least 2 m long; at most 0.5 m rise between landings)','<=','claim',
 'En ramp bör a) luta högst 1:20 mellan minst 2 meter långa vilplan, b) ha en höjdskillnad på högst 0,5 meter mellan vilplanen','BFS 2011:5 ALM 2, 9 §, Allmänt råd (PDF p. 4)',
 "GENERAL ADVICE (allmänt råd), NOT A BINDING FÖRESKRIFT: 'bör' (should). Scope: public places and areas for facilities other than buildings (ALM 2, 1 §). Currency: Boverket's own PBL-kunskapsbanken page on accessibility on public places, retrieved this session (artefact 54cbad3421ee4f37.html), names BFS 2011:5 - ALM 2 as the applicable regulation. Year: title page 'Utkom från trycket den 26 april 2011'. The binding föreskrift beside it (9 §, first paragraph) states no gradient.",
 dict(scheme='section', section='9 §', subsection='Allmänt råd', paragraph='a'))
add('REF-01024','SE','numerical','1:12','rise:run ratio (advised maximum for an utjämning till 0-nivå, a kerb-type levelling ramp at crossings and similar places)','<=','claim',
 'En utjämning till 0-nivå bör inte ha större lutning än 1:12. Bredden bör vara 90–100 cm.','BFS 2011:5 ALM 2, 8 §, Allmänt råd (PDF p. 4)',
 "GENERAL ADVICE ('bör'); the element is a dropped-kerb type ramp (utjämning till 0-nivå) between walking surfaces, not a ramp of travel, hence setting 'kerb ramp'.",
 dict(scheme='section', section='8 §', subsection='Allmänt råd'), setting='kerb ramp (utjämning till 0-nivå)')
# ---- SE REF-01025 FUB
add('REF-01025','SE','qualitative','a 1:12 ramp gradient is a safety risk: it demands arm strength and great manoeuvring skill to keep the wheelchair from rolling backwards and tipping over','','','claim',
 'En ramplutning på 1:12 är en säkerhetsrisk. Det kräver kraft i armarna och stor manöverskicklighet för att inte rullstolen ska rulla bakåt och välta.','Yttrande, punkt 3:1222 (PDF pp. 2-3)',
 "R7 HARM / INADEQUACY FINDING WITH A STATED MECHANISM (backward roll and tip-over; arm strength; manoeuvring skill) -- asserted, not measured; harm_finding=1. DATE AND TARGET: Stockholm 2007-01-10, a remissvar to Boverket's proposal to revise BBR sections 3 and 8; the provision criticised was then BBR 3:1222. THE 1:12 CEILING WAS NOT CHANGED IN THE 17 YEARS TO BFS 2024:12 (REF-01023, in force 2025-07-01), which still reads 'ska luta högst 1:12'. Device inferred from the stated mechanism (arm strength): manual, self-propelled.",
 dict(scheme='section', section='3:1222'), device='manual_self_propelled',
 rpn="Riksförbundet FUB is an organisation for people with intellectual disability (its name: För Utvecklingsstörda Barn, Ungdomar och Vuxna); no wheelchair-user authorship is evidenced in the retrieved bytes (D-0178), which is why the source is filed T3 grey rather than Co-1. The topic population (manual wheelchair users) is not the author organisation's stated constituency.")
add('REF-01025','SE','numerical','1:20','rise:run ratio (requested maximum; a lifting device where it cannot be achieved)','<=','claim',
 'Eftersom utgångspunkten för föreskrifterna är att en person självständigt ska kunna förflytta sig anser vi det absolut nödvändigt att lutningen 1:20 införs som standard. Vi yrkar att högsta tillåtna ramplutning anges till 1:20. Går inte detta att åstadkomma krävs lyftanordning.','Yttrande, punkt 3:1222 (PDF pp. 2-3)',
 "A REQUESTED STANDARD (an advocacy demand), not a code value and not a measurement. Its stated warrant is independence of movement ('en person självständigt ska kunna förflytta sig'), the starting point the organisation reads into the regulation. The same 1:20 figure is the Swedish public-places general advice (REF-01024).",
 dict(scheme='section', section='3:1222'), device='manual_self_propelled')
# ---- PT REF-01026
pt_note = " Source quality: a transcription hosted by the Ordem dos Arquitectos whose first page says it 'não substitui a consulta da sua publicação em Diário da República'; diariodarepublica.pt returned only a JavaScript shell (no text), so the legal original was not retrieved -- GREY / UNVERIFIED. Portugal has no JurisdictionCode value (jurisdiction_db_vocabulary class, owner decision). Lead-in of 2.5.1: 'As rampas devem ter a menor inclinação possível' -- the code states the least-possible-slope principle itself."
add('REF-01026','PT','numerical','6%','% longitudinal gradient (maximum) where the rise is <= 0.6 m and the horizontal projection <= 10 m; interpolated values permitted','<=','claim',
 '1) Ter uma inclinação não superior a 6%, vencer um desnível não superior a 0,6 m e ter uma projecção horizontal não superior a 10 m;','Anexo, 2.5.1 1)',
 "TIERED BY RISE AND RUN, with explicit permission to use interpolated values ('ou valores interpolados dos indicados')." + pt_note,
 dict(scheme='section', section='Anexo 2.5', subsection='2.5.1', paragraph='1'))
add('REF-01026','PT','numerical','8%','% longitudinal gradient (maximum) where the rise is <= 0.4 m and the horizontal projection <= 5 m; interpolated values permitted','<=','claim',
 '2) Ter uma inclinação não superior a 8%, vencer um desnível não superior a 0,4 m e ter uma projecção horizontal não superior a 5 m.','Anexo, 2.5.1 2)',
 "SECOND TIER OF THE NEW-BUILD RULE (steeper for shorter, lower ramps)." + pt_note,
 dict(scheme='section', section='Anexo 2.5', subsection='2.5.1', paragraph='2'))
add('REF-01026','PT','numerical','12%','% longitudinal gradient (maximum) in buildings under alteration or conservation only, where the rise is <= 0.1 m and the projection <= 0.83 m; a 10% step allows rise <= 0.2 m and projection <= 2 m','<=','condition',
 'No caso de edifícios sujeitos a obras de alteração ou conservação, se as limitações de espaço impedirem a utilização de rampas com uma inclinação não superior a 8%, as rampas podem ter inclinações superiores se satisfizerem uma das seguintes situações ou valores interpolados dos indicados: 1) Ter uma inclinação não superior a 10%, vencer um desnível não superior a 0,2 m e ter uma projecção horizontal não superior a 2 m; 2) Ter uma inclinação não superior a 12%, vencer um desnível não superior a 0,1 m e ter uma projecção horizontal não superior a 0,83 m.','Anexo, 2.5.2',
 "EXISTING-BUILDING CONCESSION, available only where space prevents 8%." + pt_note,
 dict(scheme='section', section='Anexo 2.5', subsection='2.5.2'))
# ---- ES REF-01027 DB-SUA
add('REF-01027','ES','numerical','12%','% longitudinal slope (general maximum for ramps)','<=','claim',
 'Las rampas tendrán una pendiente del 12%, como máximo, excepto:','DB-SUA, SUA 1, 4.3.1 apartado 1',
 "GENERAL RAMP RULE; ramps on accessible routes are the stricter exception (next row). The text is the Ministry's consolidated articulado (as modified through RD 450/2022; correction of errors BOE 2/02/2023); the Ministry's comments in the same PDF are 'orientativo e informativo ... no teniendo carácter reglamentario' (p. 2) and are not extracted.",
 dict(scheme='section', section='SUA 1', subsection='4.3.1', paragraph='1'))
add('REF-01027','ES','numerical','6%','% longitudinal slope for ramps on accessible routes: <=10% where the run is < 3 m, <=8% where < 6 m, <=6% otherwise','<=','claim',
 'las que pertenezcan a itinerarios accesibles, cuya pendiente será, como máximo, del 10% cuando su longitud sea menor que 3 m, del 8% cuando la longitud sea menor que 6 m y del 6% en el resto de los casos.','DB-SUA, SUA 1, 4.3.1 apartado 1 a)',
 "THE ACCESSIBLE-ROUTE TIERING (10/8/6 by run length). Run lengths are measured in horizontal projection, per section; on a curved ramp the slope is measured on the least favourable side. Section 4.3.2(1) caps accessible-route ramp sections at 9 m (a length parameter, not extracted).",
 dict(scheme='section', section='SUA 1', subsection='4.3.1', paragraph='1', clause='a'))
# ---- ES REF-01028 TMA
add('REF-01028','ES','numerical','8%','% longitudinal slope for ramps linked to an accessible pedestrian itinerary in urbanised public space: <=10% for runs up to 3.00 m, <=8% for runs up to 9.00 m (horizontal projection); run capped at 9.00 m','<=','claim',
 'La pendiente longitudinal máxima será del 10% para tramos de hasta 3,00 m de longitud, y del 8% para tramos de hasta 9,00 m de longitud, medidos en proyección horizontal.','Orden TMA/851/2021, art. 14 apartado 2 c)',
 "IN FORCE FROM 2022-01-02 AND THE SUCCESSOR OF ORDEN VIV/561/2010, which BOE shows as derogated on 2022-01-02 (retrieved: BOE-A-2010-4057, 'Fecha de derogación: 02/01/2022', 'SE DEROGA, por Orden TMA/851/2021'). The 2010 order's art. 14.1 b) read 10% to 3 m and 8% to 10 m; the 2021 order keeps the percentages and shortens the run cap from 10 m to 9 m. A ramp is DEFINED here as a plane above 6% (art. 14.1) -- a classification threshold, not a limit. AN UNVERIFIED WEB-SEARCH SUMMARY this session said the order sets a 6% maximum; the retrieved BOE text does not.",
 dict(scheme='section', section='art. 14', subsection='2', paragraph='c'))
# ---- ES REF-01029 CERMI
add('REF-01029','ES','numerical','8%','% longitudinal slope: <=10% for ramps under 3 m, <=8% for ramps of 3-10 m','<=','claim',
 'Rampas de menos de 3 m. pendiente máxima 10%. Rampas de entre 3 y 10 m. pendiente máxima 8%.','Metodología p. 24, Pendientes longitudinales máximas',
 "AN ECHO, NOT AN INDEPENDENT FIGURE: it reproduces the figures of Orden VIV/561/2010 art. 14.1 b) (retrieved from BOE this session, BOE-A-2010-4057), in force when the Metodología was written (December 2018) and DEROGATED on 2022-01-02 by Orden TMA/851/2021 (REF-01028). Spain's current urban-space rule keeps 10%/8% but caps the 8% tier at 9 m. The same page states a 2% maximum cross-slope: a different axis, not extracted.",
 dict(scheme='section', section='p. 24', subsection='Pendientes longitudinales máximas'))
add('REF-01029','ES','qualitative','above 6% (the legal limit) a sloping street is already seriously difficult for many people to travel, and from 10% it is impracticable','','','claim',
 'pendientes superiores al 6% (límite que marca la ley) empiezan a tener problemas importantes para ser recorridas por muchas personas y a partir del 10% es impracticable.','Metodología p. 10, 3.2 Condiciones orográficas',
 "R7 HARM / INADEQUACY FINDING: a practical-use threshold stated by a disability-sector platform, asserted not measured; harm_finding=1. It concerns STREET slope (calles en pendiente), a route and not a ramp -- GAP-033's scope question -- so it is filed as a finding beside the ramp row, not as a ramp value. 'Límite que marca la ley' is read as the 6% definition threshold of Orden VIV/561/2010 art. 14.1 (an inference; the Metodología does not cite the article at this point).",
 dict(scheme='section', section='p. 10', subsection='3.2'),
 rpn="CERMI Comunidad de Madrid authored the document (title page and every footer) and the municipality is credited on the last page only as 'Con el apoyo de'. The retrieved bytes do not state who within CERMI wrote it or that disabled people did (D-0178), so Co-1 is NOT claimed: filed T3 grey, Co-1-adjacent.")
# ---- FR REF-01030
fr_note = " EXISTING-BUILDING REGIME ONLY (ERP/IOP in an existing built frame; arrêté du 8 décembre 2014). The NEW-ERP regime (arrêté du 20 avril 2017) was NOT retrieved: Légifrance returns 403 and two prefecture copies closed the connection (HTTP/2 stream errors, empty reply); research_code_leads 86 and 92 stay REFERENCE-ONLY and no figure for new ERP is asserted here. The guide's preface says a companion guide on new ERP was still to come. Year 2019 is read from the URL ('2019 07') and the PDF creationDate (2019-05-29); no date appears in the pages retrieved."
add('REF-01030','FR','numerical','6%','% (maximum slope of an inclined plane on an accessible route in existing ERP/IOP; tolerated exceptionally up to 10% over <= 2 m and 12% over <= 0.50 m)','<=','claim',
 "Lorsqu'une dénivellation ne peut être évitée, un plan incliné de pente inférieure ou égale à 6 % est aménagé afin de la franchir. Les valeurs de pentes suivantes sont tolérées exceptionnellement : jusqu'à 10 % sur une longueur inférieure ou égale à 2 m ; jusqu'à 12 % sur une longueur inférieure ou égale à 0,50 m.",'Guide, B-2 2° a) Profil en long, Pentes (Arrêté du 8 décembre 2014, art. 2), p. 12',
 "REPRODUCES THE ARRÊTÉ'S TEXT (the guide prints it in a block headed 'Arrêté du 8 décembre 2014, Article 2')." + fr_note,
 dict(scheme='section', section='Arrêté du 8 décembre 2014, art. 2', subsection='2° a) Pentes'))
add('REF-01030','FR','qualitative',"from 6% over several metres, many manual wheelchair users lose their autonomy and must ask for help; many other people with reduced mobility suffer comparable difficulty",'','','claim',
 "À partir de 6 % sur plusieurs mètres, un nombre important de personnes en fauteuil roulant manuel vont perdre leur autonomie et devoir demander de l'aide. De nombreuses autres personnes à mobilité réduite subiront une gêne comparable.",'Guide p. 12, commentary beside the arrêté text',
 "THE MINISTRY'S OWN STATEMENT OF WHERE AUTONOMY IS LOST, asserted not measured (no study is cited in the pages retrieved); harm_finding=1. It sits in the commentary margin, not in the arrêté text. The requirement itself is 6%, so the arrêté's ceiling is the point at which this guide says manual wheelchair users begin to lose independence." + fr_note,
 dict(scheme='section', section='Guide p. 12', subsection='commentary'), device='manual_self_propelled')
add('REF-01030','FR','numerical','5%','% (recommended, not required)','<=','claim',
 'on préférera un plan incliné dont la pente est inférieure ou égale à 5 %','Guide p. 12, commentary (ressauts successifs)',
 "A MINISTRY COMMENTARY RECOMMENDATION (the guide's 'R : Recommandé' convention), made while advising against successive small steps (ressauts); it is not the arrêté's requirement, which is 6%." + fr_note,
 dict(scheme='section', section='Guide p. 12', subsection='commentary'))

only = sys.argv[1:] 
ok=0
for i,e in enumerate(E):
    found, where = rl.quote_in_artefacts(e['text'], ref_id=e['ref'])
    scoped = found and ('retrieved for '+e['ref']) in where
    print(i, e['ref'], 'FOUND' if found else 'MISSING', 'scoped' if scoped else 'UNSCOPED/none', where[:90] if not found or not scoped else '')
    if only and only[0]=='check': continue
    cmd=['python3','scripts/db.py','add-extraction','--ref-id',e['ref'],'--slug',SLUG,'--parameter-id','3','--identity','MOB',
         '--claim-type',e['ctype'],'--claimed-value',e['cv'],'--claim-text',e['text'],'--source-section',e['section'],
         '--jurisdiction',e['juris'],'--extraction-method','full-read','--extraction-status','preliminary',
         '--root-type',e['root_type'],'--root-ref-id',e['ref'],'--measurement-paradigm',e['paradigm'],'--device-class',e['device'],
         '--figure-role',e['role'],'--relation','none','--notes',e['notes'],'--session',SESSION]
    if e['unit']: cmd+=['--claimed-unit',e['unit']]
    if e['cmp']: cmd+=['--comparator',e['cmp']]
    if e['setting']: cmd+=['--setting',e['setting']]
    if e['rpn']: cmd+=['--root-population-note',e['rpn']]
    l=e['locs']
    if l:
        cmd+=['--locator-scheme',l['scheme']]
        for k,flag in (('division','--loc-division'),('part','--loc-part'),('section','--loc-section'),('subsection','--loc-subsection'),('paragraph','--loc-paragraph'),('clause','--loc-clause')):
            if k in l: cmd+=[flag,l[k]]
    env=dict(os.environ, GUIDEBOOK_DB_PATH=SCR+'/batch23.db')
    r=subprocess.run(cmd,env=env,capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print('   ->', r.returncode, ' | '.join(out[-3:])[:300])
