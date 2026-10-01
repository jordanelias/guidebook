import json, os, subprocess, sys
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
SLUG='accessible-circulation-geometry'
man=[json.loads(l) for l in open(f'retrieval-log/{S}/manifest.jsonl')]
def art(url):
    ok=[m for m in man if m['url']==url and m.get('status') and 200<=m['status']<300 and m['bytes']>0 and not m.get('derived')]
    return ok[-1]['artefact'] if ok else None
P={}
for line in open(SCR+'/priors.txt'):
    if ':' in line and line.split(':')[0] in ('KR','SG','PT','EU','FR','ES','NL','SE','AU','CO1-KR'):
        P[line.split(':')[0]]=line.split(':',1)[1].strip()
EX=[]
def ex(query, lang, juris, ttype, prior, found, note, admitted=(), fetch=None, harm=0, sat='none', ttier=None, screened=None):
    EX.append(dict(query=query,lang=lang,juris=juris,ttype=ttype,prior=prior,found=found,screened=found if screened is None else screened,note=note,admitted=list(admitted),fetch=fetch,harm=harm,sat=sat,ttier=ttier))

# ---------- KR
ex('편의증진 보장에 관한 법률 시행규칙 별표 1 경사로 기울기 1/12 이하 편의시설의 구조 재질 세부기준','KO','KR','code',P['KR'],9,
 "WEB-SEARCH SUMMARY CONTRADICTED BY THE BYTES LATER RETRIEVED: the tool's summary said 'approach path gradient 1/18 or less, relaxed to 1/12 where terrain is difficult' under the ramp question. That is item 1 of Annex 1 (접근로, approach path); the RAMP (경사로) item is item 12 and reads 12분의 1 or less. The conflation is the hazard here, so it is recorded. Hits were one legal-wiki page (NEPLA), several installer-marketplace pages (qnaqc, soomgo) and a 1997 press item; no official host in the list.")
ex('Enforcement Rule of the Act on Guarantee of Promotion of Convenience of Persons with Disabilities, the Elderly and Pregnant Women Annex 1 ramp slope 1/12 elaw.klri.re.kr','EN','KR','code','Expect the KLRI English translation (elaw.klri.re.kr) to carry the Enforcement Rule with its Annex 1 ramp clause, as it does for many Korean statutes; the prior for KR is otherwise as logged for the first KR search.',10,
 "WRONG INDEX / TRANSLATION NOT FOUND, NOT ABSENCE OF THE RULE: elaw.klri.re.kr listed the Act and decrees (hseq 53020, 46425 retrieved this session and identified as Acts on welfare of persons with disabilities / prohibition of discrimination, not the Enforcement Rule). No English translation of the Enforcement Rule's Annex 1 was located. Results otherwise were ADA material.")
ex('장애인·노인·임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 1] 편의시설의 구조·재질 등에 관한 세부기준 경사로 기울기 1/12 법령 전문','KO','KR','code','Expect the second, fuller phrasing to surface the rule text on law.go.kr or a faithful mirror; if only mirrors, the value 1/12 should still appear verbatim.',8,
 "Surfaced the NEPLA wiki page (a mirror of Annex 1 with the amendment stamp) and a Seoul facilities manual hosted on nld.go.kr; official law.go.kr not in the list.")
ex('https://www.nepla.ai/wiki/복지와-건강/사회복지/-유권해석-장애인-노인-임산부-등의-편의증진-보장에-관한-법률-시행규칙-별표-1-편의시설의-구조·재질등에-관한-세부기준-제2조제1항관련-1509xgx0mnol','KO','KR','code',
 'Follow-up direct retrieval of the NEPLA mirror found by the preceding search: expect Annex 1 in full with 12분의 1 for 경사로 (item 12) and 18분의 1 for 접근로 (item 1).',1,
 "RETRIEVED, 200, 172 kB HTML. Annex 1 text under the stamp <개정 2023. 12. 11.>. Item 12 나목: (1) 경사로 기울기 12분의 1 이하 ('하여야 한다'); (2) relaxable to 8분의 1 only if the ramp is in an EXISTING facility, height <= 1 m, 1/12 structurally difficult, AND the facility manager provides continuous assistance (상시보조서비스). Item 1 나목(1): 접근로 18분의 1 or less, relaxable to 12분의 1 where terrain is difficult (NOT a ramp; not extracted). The page's 비고 says '…할 수 있다' items are recommendations. Mirror, not the official host; issuing ministry not stated. Admitted GREY/UNVERIFIED as REF-01019.",
 admitted=['REF-01019'], fetch=['https://www.nepla.ai/wiki/복지와-건강/사회복지/-유권해석-장애인-노인-임산부-등의-편의증진-보장에-관한-법률-시행규칙-별표-1-편의시설의-구조·재질등에-관한-세부기준-제2조제1항관련-1509xgx0mnol'], sat='saturated')
ex('https://www.law.go.kr/법령/장애인ㆍ노인ㆍ임산부등의편의증진보장에관한법률시행규칙','KO','KR','code','Expect the official Korean legal-information host (law.go.kr) to serve the Enforcement Rule; it is a dynamic site, so retrieval, not the value, is the risk.',0,
 "RETRIEVAL FAILURE, NOT ABSENCE: curl exit 35 (connection reset by peer) on the law page and on the DRF OpenAPI search URL; nld.go.kr (Seoul manual) answered 400 'Request Blocked'. Consistent with geo-filtering of foreign cloud addresses; not confirmed. These attempts were made outside retrieval_log.fetch (curl probes) and are therefore NOT in the manifest -- recorded here only.")
ex('휠체어 이용자 장애인 당사자 경사로 기울기 12분의 1 너무 가파르다 장애인단체 경사로 기준 개선 요구','KO','KR','co1',P['CO1-KR'],9,
 "ZERO CO-1 YIELD, AND NOT CONCLUSIVE ABSENCE (R14): the query is a long Korean multi-concept phrasing run on a general web index; the nine hits were an IT-Q&A page and installer-marketplace pages (soomgo). The tool summary itself said it found no disability-organisation demand about 1/12. No Korean DPO repository (e.g. a disability-organisation site search) was queried, so this is wrong-index / query-shape, not genuine absence.",ttier=1)
# ---------- SG
ex('BCA Code on Accessibility in the Built Environment 2019 ramp gradient maximum 1:12 Singapore','EN','SG','code',P['SG'],9,
 "Surfaced the BCA Code PDF (www1.bca.gov.sg/docs/default-source/universaldesign/accessibilitycode2019.pdf), the BCA Code page, a 2018 REACH consultation DRAFT, a 2025 BCA consultation circular and Philippine BP 344 material. The tool summary said the gradient was 'not visible in the excerpt'. No value taken from any summary.")
ex('Singapore Code on Accessibility in the Built Environment 2019 ramps gradient 1:12 maximum "1:12" BCA','EN','SG','code','Expect the same BCA PDF; a quoted-figure query might surface a mirror or a law-firm summary quoting the clause.',9,
 "Same BCA PDF and page; the only '1:12' hits were Philippine BP 344. No Singapore mirror carrying the clause.")
ex('Singapore accessibility code 2019 ramp gradient not steeper than 1:12 landing wheelchair BCA Universal Design Guide ramp slope','EN','SG','code','Expect secondary Singapore pages (agency or consultant guides) restating the ramp gradient.',9,
 "Nothing restating the clause from a reachable host; fliphtml5 and ncda.gov.ph hits concern the Philippines. GENUINE NO-MIRROR FINDING for the reachable index.")
ex('https://www1.bca.gov.sg/docs/default-source/universaldesign/accessibilitycode2019.pdf','EN','SG','code','Expect the official BCA PDF to download; bot-challenge gating was the logged risk in the SG prior.',0,
 "RETRIEVAL FAILURE, NOT ABSENCE: HTTP 403 (919-byte interstitial) on the PDF, on the BCA Code page, on the REACH 2018 draft and on the 2025 consultation circular (four 403 artefacts persisted in this session's manifest). Wayback: archive.org/wayback/available lists a 2026-01-14 snapshot, but replay on web.archive.org failed twice (curl exit 35; the proxy status shows ws_closed_mid_exchange for web.archive.org:443) in both the if_ and plain /web/<ts>/ forms -- the same session-level limit batch 22 recorded for CSA B651. Nothing admitted; SG stays searched with NO retrievable text.")
# ---------- PT
ex('Decreto-Lei 163/2006 acessibilidades rampas inclinação máxima anexo normas técnicas','PT','PT','code',P['PT'],9,
 "Surfaced an Ordem dos Arquitectos PDF of the decree, municipal slide decks, an LNEC repository file and architect blogs. Tool summary: sidewalks and routes 6% longitudinal max; ramp specifics 'in the annex'. Nothing taken from the summary.")
ex('https://ordemdosarquitectos.org/backend/uploads/decretolei_163_2006_a8acccc42f.pdf','PT','PT','code','Follow-up direct retrieval: expect the decree text including Anexo 2.5 Rampas with a tiered percentage table by rise and run.',1,
 "RETRIEVED, 200, 651 kB PDF, 41 pp. Page 1 says it TRANSCRIBES the decree and 'não substitui a consulta da sua publicação em Diário da República'. Anexo 2.5.1: <=6% with rise <=0.6 m and projection <=10 m, or <=8% with rise <=0.4 m and projection <=5 m, interpolated values permitted; 2.5.2 (alteration of existing buildings only): 10% (rise <=0.2 m, projection <=2 m) or 12% (rise <=0.1 m, projection <=0.83 m). Admitted GREY/UNVERIFIED as REF-01026 (transcription, not the DR original).",
 admitted=['REF-01026'], fetch=['https://ordemdosarquitectos.org/backend/uploads/decretolei_163_2006_a8acccc42f.pdf'], sat='saturated')
ex('Decreto-Lei n.º 163/2006 de 8 de agosto Diário da República 1.ª série-A n.º 152 acessibilidade texto original files.diariodarepublica.pt','PT','PT','code','Expect the official Diario da Republica to carry the decree and let the transcription be checked against it.',9,
 "Surfaced diariodarepublica.pt consolidated legislation, vlex and municipal copies. Retrieval of the DRE page returned HTTP 200 but only a 2.3 kB 'JavaScript is required' shell (artefact 0794abe5f8088cfd.html): NO TEXT. The transcription therefore stays UNVERIFIED against the original.",
 fetch=['https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2006-108253479'])
# ---------- EU
ex('EN 17210:2021 accessibility and usability of the built environment ramp gradient requirement','EN','EU','standard_eb',P['EU'],10,
 "THE TOOL SUMMARY ASSERTED 'Clause 7.5: max gradient 1:12 for rises up to 500 mm and 1:20 for longer ramps, 1500 mm landings every 10 m'. NOT USED. A CEN/CLC JTC 11 workshop deck retrieved from UNE (below) lists the standard's chapters and puts ramps under chapter 10 'Vertical circulation', not 7 ('Access in the outdoor environment') -- so the summary's clause number is contradicted by the one primary-adjacent artefact obtained. No clause text of EN 17210 is freely available in the result list (BSI, Genorma, UNE catalogue pages).",ttier=4)
ex('https://www.une.org/normalizacion_documentos/PT%20EN%2017210.pdf','EN','EU','standard_eb','Follow-up: expect the UNE preview file to carry catalogue or scope pages only, possibly the table of contents.',1,
 "RETRIEVED, 200, 1.96 MB, 18 slides: 'Towards common European criteria on accessibility of the built environment: Outcomes of Mandate M/420' (CEN/CLC JTC 11, 22 March 2021). Contents only: chapter 10 'Vertical circulation (ramps, stairs, handrails, lifts, escalators)'. NO gradient value. Not admitted. EU therefore stays SEARCHED / PAYWALLED: lead filed for EN 17210:2021. The Dutch Bbl nota (REF-01020) says the new Dutch small-rise tiers come from NEN 9120, the Dutch elaboration of EN 17210 -- the only route by which an EN 17210 figure is visible in this corpus.",
 fetch=['https://www.une.org/normalizacion_documentos/PT%20EN%2017210.pdf'],sat='partial')
# ---------- NL
ex('Besluit bouwwerken leefomgeving hellingbaan toegankelijkheid helling ten hoogste 1:12 rolstoel wetten.overheid.nl','NL','NL','code',P['NL'],10,
 "Tool summary gave 1:12 (<=0.25 m rise), 1:16 (<=0.5 m), 1:20 (>0.5 m): that is the PRE-1-JULY-2025 table. The retrieved IPLO page and Staatsblad show two further tiers below 1:12 (1:6, 1:10) in force since 2025-07-01. Hits: IPLO, inview.nl, omgevingsweb.nl, a BZK infographic.")
ex('Besluit bouwwerken leefomgeving artikel 4.30 hellingbaan "hoogteverschil" helling tabel wetten.overheid.nl BWBR0041297','NL','NL','code','Expect wetten.overheid.nl art. 4.30 text to be reachable and to carry the current tiers.',9,
 "wetten.overheid.nl NOT RETRIEVABLE from here: curl exit 92 (HTTP/2 PROTOCOL_ERROR) then exit 52 (empty reply) over HTTP/1.1; inview.nl art. 4.30 answered 403 (118-byte body). So the legal text of art. 4.30 itself was not obtained; the amendment text was, from the Staatsblad.")
ex('Staatsblad 2025 wijziging Besluit bouwwerken leefomgeving artikel 4.30 hellingbaan 1:6 1:10 NEN 9120 verzamelbesluit zoek.officielebekendmakingen.nl','NL','NL','code','Expect the official gazette (officielebekendmakingen.nl) to carry the amending decree and its explanatory note.',9,
 "Surfaced Stb. 2025, 432 (retrieved: a DIFFERENT decree, of 4 Dec 2025, on environmental-performance requirements -- screened out, not ramp-relevant) and, by the tool's text, Stb. 2024, 368 as the carrier of the July 2025 art. 4.30 change. Direct retrieval of Stb. 2024, 368 follows.")
ex('https://zoek.officielebekendmakingen.nl/stb-2024-368.pdf','NL','NL','code','Expect the Verzamelbesluit Bbl 2024 to contain onderdeel R amending art. 4.30 with new small-rise slope tiers and an explanatory note naming their source.',1,
 "RETRIEVED, 200, 448 kB, 39 pp. Besluit van 25 november 2024. Art. I onderdeel R / art. 4.30 lid 2: a. 1:6 if rise <=0.05 m; b. 1:10 if >0.05 and <=0.10 m; c. 1:12 if >0.10 and <=0.25 m (the former a-c re-lettered c-e, so 1:16 and 1:20 are unchanged text not reproduced). Art. II lid 2: onderdeel R in force 1 July 2025. Nota: the added dimensions are taken over from NEN 9120, 'Nederlandse uitwerking van NEN-EN 17210', in development; the nota writes 'mm' where the operative text is metres (slip, flagged). Admitted as REF-01020.",
 admitted=['REF-01020'], fetch=['https://zoek.officielebekendmakingen.nl/stb-2024-368.pdf'], sat='saturated')
ex('https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/hellingbaan/','NL','NL','national_fw','Follow-up: expect the government guidance page to restate art. 4.30 with a steepness table.',1,
 "RETRIEVED, 200, 51 kB HTML, dcterms:modified 2026-06-10. Table 'steilte hellingbaan': <=5 cm 1:6; >5-10 cm 1:10; >10-25 cm 1:12; >25-50 cm 1:16; >50-100 cm 1:20; ramp max 1 m high, width >=1.1 m; says the <=10 cm rows come from NEN 9120:2025 (Dutch elaboration of NEN-EN 17210). Admitted T5 as REF-01021; only the 1:16 and 1:20 rows are extracted (the rest duplicate REF-01020).",
 admitted=['REF-01021'], fetch=['https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/hellingbaan/'], sat='saturated')
ex('Ieder(in) hellingbaan helling rolstoelgebruikers standpunt Bbl toegankelijkheid hellingpercentage te steil','NL','NL','co1','Expect the Dutch national disability network (Ieder(in)) to have commented on the Bbl ramp rules in a consultation reply; unsure it states a figure.',9,
 "Surfaced Ieder(in)'s internetconsultatie reply on the Verzamelbesluit Bbl 2024 and local-council pages on ramp complaints. Tool summary mentioned wheelchair users finding ramps tiring; those were municipal documents, not DPO statements, and are not used.",ttier=1)
ex('https://internetconsultatie.nl/verzamelbesluit_bouwwerken_leefomgeving_2024/reactie/237535/bestand','NL','NL','co1','Follow-up: expect the Ieder(in) reply to endorse or criticise the revised ramp requirements.',1,
 "RETRIEVED, 200, 75 kB, 2 pp. Letter of 9 November 2023 (ref. 23-0915/AvdV/SvK), signed by the director, from 'Ieder(in), het netwerk van mensen met een beperking of chronische ziekte'. Supports the ramp requirements being aligned with NEN 9120 in development; states NO figure and no criticism. Admitted Co-1 as REF-01022 with the limit that organisational standing, not participatory production, is what the bytes evidence.",
 admitted=['REF-01022'], fetch=['https://internetconsultatie.nl/verzamelbesluit_bouwwerken_leefomgeving_2024/reactie/237535/bestand'], sat='saturated', ttier=1)
# ---------- SE
ex('Boverket BBR rampens lutning högst 1:12 tillgänglighet ramp avsnitt 3:14 föreskrifter','SV','SE','code',P['SE'],9,
 "Surfaced Boverket BBR comparison PDFs, municipal guidelines and BFS 2011:5 ALM 2 hosted by Varbergs kommun. Tool summary: 'public places ramp 1:20 between >=2 m landings'. A prior that Sweden states one ~1:12 figure is partly wrong: two settings, two figures (below).")
ex('Boverket ALM 2 BFS 2011:5 allmänna platser tillgänglighet ramp gäller fortfarande ändring upphävd','SV','SE','code','Expect ALM 2 to be current; check Boverket own page.',9,
 "CURRENCY CHECK: Boverket's own PBL-kunskapsbanken page 'Tillgänglighet på allmänna platser och områden för andra anläggningar' (retrieved, 200, artefact 54cbad3421ee4f37.html) names BFS 2011:5 - ALM 2 as the applicable regulation. No repeal found.",
 fetch=['https://www.boverket.se/sv/PBL-kunskapsbanken/regler-om-byggande/krav-pa-byggnadsverk-tomter-mm/allmanna/tillganglighet/'])
ex('https://www.varberg.se/download/18.2b514d9b18a92e6fafc230fb/1387272663974/BFS2011-5-ALM2.pdf','SV','SE','code','Follow-up: expect ALM 2 to state the public-places ramp advice 1:20 as general advice (allmänt råd), not as a binding föreskrift.',1,
 "RETRIEVED, 200, 48 kB, 8 pp. Title page: Boverkets författningssamling BFS 2011:5 ALM 2, 'Utkom från trycket den 26 april 2011'. 9 §, Allmänt råd: 'En ramp bör luta högst 1:20 mellan minst 2 meter långa vilplan', rise <=0.5 m between landings; 8 §, Allmänt råd: 'En utjämning till 0-nivå bör inte ha större lutning än 1:12'. ADVICE ('bör'), not binding. Copy hosted by a municipality; Boverket's page confirms the instrument. Admitted as REF-01024.",
 admitted=['REF-01024'], fetch=['https://www.varberg.se/download/18.2b514d9b18a92e6fafc230fb/1387272663974/BFS2011-5-ALM2.pdf'], sat='saturated')
ex('DHR Funktionsrätt Sverige ramp lutning 1:20 rullstolsanvändare synpunkter tillgänglighet ramper Boverket remissvar','SV','SE','co1','Expect Swedish disability-movement consultation replies to Boverket (Funktionsratt Sverige / DHR) to comment on ramp gradient.',9,
 "Surfaced Boverket-hosted remissvar PDFs (Funktionsratt Sverige, Orebro kommun, TILRF, Arbetsmiljoverket). THE TOOL SUMMARY ATTRIBUTED THE '1:12 IS A SAFETY RISK / REQUEST 1:20' POSITION TO FUNKTIONSRATT SVERIGE; the bytes later retrieved show that text is in a FUB reply, not Funktionsratt's. Direct fetches of three Boverket contentassets URLs returned 404 (794 kB Boverket not-found page each) -- the files have moved or been removed.",ttier=1)
ex('https://insynsverige.se/documentHandler.ashx?did=52240','SV','SE','co1','Follow-up on a hit assumed to be a Swedish consultation document.',1,
 "RETRIEVED, 200, 14 kB, but IRRELEVANT TO THE EXPECTATION: a 2001 Stockholm Gatu- och fastighetskontoret tjänsteutlåtande on ramps to shops in the old city. Incidentally states the office's own ramp requirement as 1:20 'for persons to be able to get up on their own' (municipal, 2001). Not admitted; noted as a possible municipal Swedish source for a later pass.",
 fetch=['https://insynsverige.se/documentHandler.ashx?did=52240'])
ex('Funktionsrätt Sverige remissvar Boverket förslag föreskrifter tomter ramp lutning 1:12 synpunkter pdf','SV','SE','co1','Expect the extended search to find the Funktionsratt Sverige reply or a sibling DPO reply stating a ramp-gradient position.',10,
 "Surfaced the FUB yttrande (fub.se) and Boverket PBL-kunskapsbanken pages on stairs/ramps and walkways. FUB = Riksforbundet FUB (organisation for people with intellectual disability): a Co-1-ADJACENT consultation reply, not wheelchair-user-led.",ttier=1)
ex('https://www.fub.se/files/bilagor/b8_fs_1-07_boverket.pdf','SV','SE','grey','Follow-up: expect a remissvar that may comment on ramp gradient.',1,
 "RETRIEVED, 200, 105 kB, 7 pp., Stockholm 2007-01-10, signed by the kanslichef. Point 3:1222: 'En ramplutning på 1:12 är en säkerhetsrisk. Det kräver kraft i armarna och stor manöverskicklighet för att inte rullstolen ska rulla bakåt och välta' and a request that the maximum be 1:20 or a lift be required. R7 HARM FINDING. The ceiling stayed 1:12 until BFS 2024:12. Admitted T3 grey (Co-1 not claimed: wheelchair-user authorship not evidenced, D-0178) as REF-01025.",
 admitted=['REF-01025'], fetch=['https://www.fub.se/files/bilagor/b8_fs_1-07_boverket.pdf'], harm=1, sat='saturated')
ex('BFS 2024:12 Boverkets föreskrifter om byggnaders tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga pdf ikraftträdande','SV','SE','code','Expect the current Boverket regulation on building accessibility to carry the binding ramp gradient.',9,
 "Surfaced rinfo.boverket.se/BFS2024-12/pdf/BFS2024-12.pdf and Boverket comparison tables (BFS 2024:12 replaces the accessibility provisions of BBR BFS 2011:6).")
ex('https://rinfo.boverket.se/BFS2024-12/pdf/BFS2024-12.pdf','SV','SE','code','Follow-up: expect 2 kap. to set a binding maximum ramp gradient near 1:12.',1,
 "RETRIEVED, 200, 224 kB, 9 pp. 'Utkom från trycket den 20 november 2024'. 2 kap. 4 §: 'En ramp, som är till för att uppfylla kraven enligt 1 § och 2 § andra stycket, ska luta högst 1:12.' In force 1 July 2025 (older BBR provisions applicable only as BFS 2024:14 point 3 allows). Admitted as REF-01023.",
 admitted=['REF-01023'], fetch=['https://rinfo.boverket.se/BFS2024-12/pdf/BFS2024-12.pdf'], sat='saturated')
ex('https://rinfo.boverket.se/BFS2024-13/pdf/BFS2024-13.pdf','SV','SE','code','Follow-up: expect the plots regulation to carry a walkway gradient rule.',1,
 "RETRIEVED, 200, 203 kB, 5 pp., in force 1 July 2025. 2 kap. 3 §: 'Gångvägar ... ska ... luta högst 1:12'. A WALKWAY-on-plot rule, not a ramp rule; not admitted or extracted (route-vs-ramp scope, GAP-033); staged as a candidate.",
 fetch=['https://rinfo.boverket.se/BFS2024-13/pdf/BFS2024-13.pdf'])
# ---------- FR
ex('arrêté du 20 avril 2017 accessibilité ERP neufs article 2 cheminement rampe pente 5 % 8 % 10 % texte officiel','FR','FR','code',P['FR'],9,
 "Surfaced prefecture PDFs of the arrêté (maine-et-loire.gouv.fr, drome.gouv.fr) and DDT notices. The tool summary refused to give the values and pointed to Légifrance. THE 5%/8%/10% IN THE QUERY WERE MY PRIOR, NOT A FINDING; none is asserted.")
ex('"arrêté du 20 avril 2017" relatif à l\'accessibilité aux personnes handicapées des établissements recevant du public lors de leur construction pdf ecologie.gouv.fr OR cohesion-territoires.gouv.fr OR accessibilite.gouv.fr','FR','FR','code','Expect a ministry-hosted PDF of the arrêté on ecologie.gouv.fr or a sister domain.',10,
 "No ministry-hosted copy of the NEW-ERP arrêté located; ecologie.gouv.fr hosts guides. Direct fetches of the two prefecture PDFs failed: maine-et-loire.gouv.fr and drome.gouv.fr closed the connection (curl exit 92 HTTP/2 stream error ENHANCE_YOUR_CALM / PROTOCOL_ERROR, then exit 52 empty reply over HTTP/1.1); legifrance.gouv.fr/eli/.../LHAL1704269A answers 403 (5.6 kB). RETRIEVAL FAILURE, NOT ABSENCE. Leads 86 and 92 stand.")
ex('arrêté 20 avril 2017 accessibilité ERP construction texte intégral article 2 cheminements rampe','FR','FR','code','Expect domain-limited search to surface ministry pages with the arrêté or its illustrated guide.',10,
 "Domain-limited (ecologie.gouv.fr etc.) results: ministry guides (existing ERP, stations, commands) and the ERP accessibility page; no new-ERP arrêté text. The existing-ERP illustrated guide is the one document that reproduces ramp slope rules with their legal basis.")
ex('https://www.ecologie.gouv.fr/sites/default/files/publications/2019%2007%20guide_DHUP_erp-existants.pdf','FR','FR','national_fw','Follow-up: expect the DHUP illustrated guide to reproduce the existing-ERP arrêté of 8 December 2014 including ramp slopes.',1,
 "RETRIEVED, 200, 9.6 MB, 65 pp. p. 12 reproduces 'Arrêté du 8 décembre 2014, Article 2': slope <=6% for an inclined plane; tolerated exceptionally 10% over <=2 m and 12% over <=0.50 m; landing every 10 m from 5%. Margin commentary: 'À partir de 6 % sur plusieurs mètres, un nombre important de personnes en fauteuil roulant manuel vont perdre leur autonomie et devoir demander de l'aide'; recommends <=5%. R7 HARM FINDING. EXISTING-ERP REGIME ONLY. Admitted T5 as REF-01030.",
 admitted=['REF-01030'], fetch=['https://www.ecologie.gouv.fr/sites/default/files/publications/2019%2007%20guide_DHUP_erp-existants.pdf'], harm=1, sat='partial')
# ---------- ES
ex('Código Técnico de la Edificación DB-SUA Seguridad de utilización y accesibilidad SUA 1 rampas pendiente 10% 8% 6% pdf codigotecnico.org','ES','ES','code',P['ES'],9,
 "Surfaced codigotecnico.org PDFs (DccSUA.pdf, DA_SUA_2) and consultant pages restating the 10/8/6 tiers (the lead-91 vendor restatements). The percentages in the query were my prior.")
ex('https://www.codigotecnico.org/pdf/Documentos/SUA/DccSUA.pdf','ES','ES','code','Follow-up: expect SUA 1 4.3.1 to state a general 12% ramp maximum and 10/8/6 tiers for accessible routes.',1,
 "RETRIEVED, 200, 1.68 MB, 79 pp. Ministerio de Vivienda y Agenda Urbana, DB-SUA 'con comentarios del Ministerio', consolidated, version list ends 15 julio 2024. SUA 1 4.3.1(1): ramps 12% maximum, EXCEPT ramps on accessible itineraries: 10% if run <3 m, 8% if <6 m, 6% otherwise. Ministry comments are non-regulatory. Admitted as REF-01027; lead 91 (vendor-restated) is now confirmed against the primary.",
 admitted=['REF-01027'], fetch=['https://www.codigotecnico.org/pdf/Documentos/SUA/DccSUA.pdf'], sat='saturated')
ex('Orden VIV/561/2010 artículo 14 rampas pendiente longitudinal máxima 10% menos de 3 m 8% BOE espacios públicos urbanizados','ES','ES','code','CERMI Madrid cites Orden VIV/561/2010 for urban public spaces; expect art. 14 to give 10% to 3 m and 8% to 10 m and to be in force.',9,
 "THE TOOL SUMMARY SAID 8% UP TO 9 M; the BOE text of VIV/561/2010 says up to 10 m. More important, the BOE page of VIV/561/2010 (retrieved below) shows 'Fecha de derogación: 02/01/2022' -- it is NO LONGER IN FORCE.",
 fetch=['https://www.boe.es/diario_boe/txt.php?id=BOE-A-2010-4057'])
ex('Orden TMA/851/2021 de 23 de julio espacios públicos urbanizados rampas artículo pendiente longitudinal máxima boe.es','ES','ES','code','Expect the successor order to carry the current urban-space ramp rule.',10,
 "Surfaced the BOE ELI pages of TMA/851/2021. The tool summary said the order's maximum longitudinal slope is 6%: CONTRADICTED by the retrieved BOE text (6% is the definition threshold of a ramp, art. 14.1; the maximum is 10%/8% by run).")
ex('https://www.boe.es/eli/es/o/2021/07/23/tma851/con','ES','ES','code','Follow-up: expect art. 14 to keep the 2010 order structure with possible changes to the run cap.',1,
 "RETRIEVED, 200, 154 kB, BOE núm. 187 of 06/08/2021, in force 02/01/2022 (BOE-A-2021-13488). Art. 14.2 c): 10% for runs up to 3.00 m, 8% for runs up to 9.00 m (horizontal projection); b): run capped at 9.00 m. Art. 14.1: a ramp is a plane above 6%. Admitted as REF-01028.",
 admitted=['REF-01028'], fetch=['https://www.boe.es/eli/es/o/2021/07/23/tma851/con'], sat='saturated')
ex('CERMI Comunidad de Madrid quiénes somos plataforma representativa entidades personas con discapacidad y sus familias','ES','ES','co1','Expect CERMI Comunidad de Madrid to describe itself as a platform of disability organisations; asks whether it is DPO-led (D-0178).',9,
 "Tool summary: constituted 1999 as a unitary platform of the Madrid federations 'representativas de personas con discapacidad' (about 350 associations), mission to represent persons with disabilities AND their families. NOT retrieved as bytes (own site cermicomunidadmadrid.org closed the connection, curl exit 56), so it cannot evidence Co-1 provenance; the Metodología is therefore filed T3 grey, Co-1-adjacent.",ttier=1)
ex('https://www.madrid.es/UnidadesDescentralizadas/Discapacidad/publicaciones/MetodologiaAccesibilidadEspaciosPublicos/metodologiaaccesibilidadespaciospublicos.pdf','ES','ES','grey','R10 re-retrieval of candidate 132 (batch 21): expect byte-identical to the batch-21 retrieval and to carry p. 24 ramp tiers and a statement of authorship.',1,
 "RE-RETRIEVED, 200, 2.0 MB, sha256 prefix 76d6a5953998c402 IDENTICAL to batch 21's artefact. Authorship: title page and every footer 'CERMI Comunidad de Madrid'; last page 'Con el apoyo de' the Ayuntamiento (supporter, not author -- candidate 132's title 'Ayuntamiento de Madrid / CERMI' over-attributed). p. 24: 10% for ramps <3 m, 8% for 3-10 m (an ECHO of Orden VIV/561/2010, derogated 2022-01-02). p. 10: slopes above 6% 'empiezan a tener problemas importantes' and above 10% 'impracticable'. R7 HARM FINDING. Admitted T3 grey as REF-01029.",
 admitted=['REF-01029'], fetch=['https://www.madrid.es/UnidadesDescentralizadas/Discapacidad/publicaciones/MetodologiaAccesibilidadEspaciosPublicos/metodologiaaccesibilidadespaciospublicos.pdf'], harm=1, sat='partial')
# ---------- AU
ex('Livable Housing Design Standard NCC 2022 H8 ramp gradient maximum 1:14 step-free path of travel ABCB','EN','AU','code',P['AU'],9,
 "Tool summary: step-free path gradient <=1:14 (or 1:20 over runs up to 15 m), 1200 mm landings. NOT USED as a value. Retrieved the ABCB NCC 2022 Vol. 2 Part H8 page: H8D2 refers to 'Clause 1.1 of the ABCB Standard for Livable Housing Design' for the gradient and uses 1:14 only as an exemption trigger for average ground slope; the ramp-gradient clause lives in the separate ABCB Standard document, NOT retrieved. NCC 2025 currency unchecked.",
 fetch=['https://abcb.gov.au/editions/ncc-2022/adopted/volume-two/h-class-1-and-10-buildings/part-h8-livable-housing-design'])
# ---------- UK/US/DE/JP/CA etc. not searched this batch (already covered)

only_check = len(sys.argv)>1 and sys.argv[1]=='check'
for i,e in enumerate(EX):
    arts=[]
    for u in (e['fetch'] or []):
        a=art(u)
        if a: arts.append('retrieval-log/%s/%s'%(S,a))
        else: print('   (no 2xx artefact for', u[:80],')')
    cmd=['python3','scripts/db.py','log-search','--slug',SLUG,'--language',e['lang'],'--query-text',e['query'],'--engine','web','--depth-method','scoping',
         '--jurisdiction',e['juris'],'--target-evidence-type',e['ttype'],'--prior-expectation',e['prior'],
         '--results-found',str(e['found']),'--results-screened',str(e['screened']),'--results-admitted',str(len(e['admitted'])),
         '--saturation-signal',e['sat'],'--harm-finding',str(e['harm']),'--findings-note',e['note'],'--origin','planned','--session',S]
    if e['ttier']: cmd+=['--target-tier',str(e['ttier'])]
    for r in e['admitted']: cmd+=['--admitted-ref-id',r]
    # link artefacts only on the direct-retrieval execs (query_text IS the URL)
    if e['query'].startswith('http'):
        for a in arts: cmd+=['--result-artefact',a]
    print(i, e['juris'], e['lang'], e['query'][:70].replace('\n',' '), '| artefacts:',len(arts) if e['query'].startswith('http') else 0, flush=True)
    if only_check: continue
    env=dict(os.environ, GUIDEBOOK_DB_PATH=SCR+'/batch23.db')
    r=subprocess.run(cmd,env=env,capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print('   ->', r.returncode, ' | '.join(out[-4:])[:420], flush=True)
