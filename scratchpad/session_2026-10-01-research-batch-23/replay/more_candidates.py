import os, subprocess, sys, re, html, json
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
import pymupdf
from pathlib import Path
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
D=Path('retrieval-log')/S
man=[json.loads(l) for l in open(D/'manifest.jsonl')]
def art(u):
    ok=[m for m in man if m['url']==u and m.get('status') and 200<=m['status']<300 and m['bytes']>0 and not m.get('derived')]
    return ok[-1]['artefact']
def run(args):
    r=subprocess.run(['python3','scripts/db.py']+args,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print('  ',r.returncode,' | '.join(out[-3:])[:260],flush=True)
    return r
def html_text(name):
    raw=(D/name).read_bytes().decode('utf-8',errors='strict')
    s=re.sub(r'(?is)<(script|style|noscript).*?</\1>','',raw)
    s=re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|td|th|table|ul|ol|section)>','\n',s)
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    return '\n'.join(l for l in (re.sub(r'[ \t ]+',' ',x).strip() for x in s.split('\n')) if l)
def pdf_text(name):
    d=pymupdf.open(D/name); n=len(d)
    return '\n'.join(f'[PDF page {p} of {n}]\n'+d[p-1].get_text() for p in range(1,n+1))
J=[
 dict(url='https://www.boverket.se/sv/PBL-kunskapsbanken/regler-om-byggande/tomter/gangvagar/',lang='SV',juris='SE',tt='national_fw',
  prior='Follow-up on a Boverket guidance page surfaced by the Funktionsratt search: expect it to restate the plot walkway rule and say how a ramp is distinguished from a sloped walkway.',
  found_note='RETRIEVED, 200, 861 kB HTML. Restates BFS 2024:13 2 kap. 3 § (gångvägar luta högst 1:12) and says the regulations set no slope at which a walkway must become a ramp: "Reglerna anger inte någon viss lutning som gräns för när vägen ska vara utförd som en ramp." A real GAP-033 datum: Sweden does not separate ramp from sloped walkway at this point.',
  disp='PENDING-VERIFICATION',title='Boverket PBL-kunskapsbanken: Tillgängliga, användbara och säkra gångvägar (guidance on BFS 2024:13)',tier='5',
  quote='Reglerna anger inte någon viss lutning som gräns för när vägen ska vara utförd som en ramp.',
  why='NOT ADMITTED: guidance restating a rule already staged as candidate 136 (BFS 2024:13); admit the two together only if GAP-033 resolves route slope into parameter 3.',
  notes='HYPOTHESIS (R15): a T5 national_fw guidance page. Its distinctive content is the statement that no slope marks the ramp/walkway boundary, plus "Lutningen ... får vara som brantast 1:12, vilket är ungefär 8 procent."'),
 dict(url='https://www.boverket.se/sv/PBL-kunskapsbanken/regler-om-byggande/sakerhet-anvandning/trappor-ramper/',lang='SV',juris='SE',tt='national_fw',
  prior='Follow-up on a Boverket guidance page on stairs and ramps: expect it to point to the accessibility regulation for the ramp gradient.',
  found_note='RETRIEVED, 200, 1.1 MB HTML. Restates BFS 2024:12 2 kap. 4 § (ramp luta högst 1:12, the rule admitted as REF-01023) and BFS 2024:9 on fall and run-off protection (other parameters). Nothing new for the gradient.',
  disp='OUT-OF-SCOPE',title='Boverket PBL-kunskapsbanken: Säkra trappor och ramper (guidance; restates BFS 2024:12 2 kap. 4 §)',tier='5',
  quote='En ramp, som är till för att uppfylla kraven enligt 1 § och 2 § andra stycket, ska luta högst 1:12.',
  why='NOT ADMITTED: duplicates the regulation already admitted as REF-01023; the page adds only safety-of-use provisions (guards, run-off protection) that belong to other parameters.',
  notes='Recorded so a later pass does not re-screen it.'),
 dict(url='https://www.boverket.se/sv/PBL-kunskapsbanken/regler-om-byggande/krav-pa-byggnadsverk-tomter-mm/allmanna/tillganglighet/',lang='SV',juris='SE',tt='national_fw',
  prior='Currency check for BFS 2011:5 ALM 2: expect Boverket to name it as the applicable regulation for public places.',
  found_note='RETRIEVED, 200, 851 kB HTML. Names BFS 2011:5 - ALM 2 as the applicable Boverket regulation on accessibility on public places; no repeal noted. Used as the currency evidence for REF-01024.',
  disp='OUT-OF-SCOPE',title='Boverket PBL-kunskapsbanken: Tillgänglighet på allmänna platser och områden för andra anläggningar (currency page for BFS 2011:5 ALM 2)',tier='5',
  quote='BFS 2011:5 – ALM 2',
  why='NOT ADMITTED as a source: it states no gradient; it is the currency evidence for REF-01024 and is cited from that source\'s extraction notes.',
  notes='The page also notes PBL 1 kap. 4 § "Upphör att gälla U:2027-01-01" in an embedded statute extract -- the planning act is scheduled to be replaced; a currency risk for all Swedish PBL-based instruments from 2027.'),
 dict(url='https://zoek.officielebekendmakingen.nl/stb-2025-432.pdf',lang='NL',juris='NL',tt='code',
  prior='Surfaced by a Bbl amendment search: expect it to be the Staatsblad carrying an art. 4.30 change.',
  found_note='RETRIEVED, 200, 186 kB, 30 pp. Staatsblad 2025, 432, Besluit of 4 December 2025: tightens the environmental-performance (milieuprestatie) requirement for offices. NOT a ramp instrument; the art. 4.30 change is in Stb. 2024, 368 (REF-01020).',
  disp='OUT-OF-SCOPE',title='Staatsblad 2025, 432: Besluit van 4 december 2025 tot wijziging van het Besluit bouwwerken leefomgeving (milieuprestatie-eis kantoorfuncties)',tier='6',
  quote='Besluit van 4 december 2025 tot wijziging van het Besluit bouwwerken leefomgeving ten behoeve van het aanscherpen van de milieuprestatie-eis voor kantoorfuncties',
  why='NOT ADMITTED: a different amending decree (environmental performance); no ramp provision.',
  notes='Screened because a search listed it for the art. 4.30 query.'),
 dict(url='https://www.ecologie.gouv.fr/politiques-publiques/laccessibilite-etablissements-recevant-du-public-erp',lang='FR',juris='FR',tt='national_fw',
  prior='Expect the ministry ERP-accessibility portal to host or link the new-ERP arrêté and a guide for new ERP.',
  found_note='RETRIEVED, 200, 908 kB HTML. A portal page that LINKS the arrêté du 20 avril 2017 to Légifrance (legifrance.gouv.fr/eli/arrete/2017/4/20/LHAL1704269A/jo/texte, which answers 403 here) and hosts guides, among them the existing-ERP guide admitted as REF-01030. No text of the new-ERP arrêté and no new-ERP guide is hosted on the ministry domain.',
  disp='OUT-OF-SCOPE',title='Ministère (ecologie.gouv.fr): L\'accessibilité des établissements recevant du public (ERP) — portal page',tier='5',
  quote='arrêté du 20 avril 2017',
  why='NOT ADMITTED: a portal page; states no gradient. Its useful finding is negative: the new-ERP arrêté is reachable only via Légifrance, which blocks automated retrieval, so FR new-ERP stays a lead (86, 92).',
  notes='The page links the arrêté du 8 décembre 2014 and the circulaire of 30 novembre 2007 as well.'),
 dict(url='https://elaw.klri.re.kr/eng_service/lawViewTitle.do?hseq=53020',lang='EN',juris='KR',tt='code',
  prior='Surfaced by an English-language search for the Enforcement Rule: expect KLRI to carry the Rule or an Annex 1 translation.',
  found_note='RETRIEVED, 200, 62 kB. Statutes of the Republic of Korea No. 30288, promulgated 2019-12-31 (Ministry of Health and Welfare): its Article 2 is "Types and Standards of Disabilities" -- an Enforcement Decree of the welfare Act, NOT the convenience-promotion Enforcement Rule.',
  disp='OUT-OF-SCOPE',title='KLRI elaw hseq=53020: Statutes of the Republic of Korea No. 30288 (promulgated 2019-12-31), Ministry of Health and Welfare — types and standards of disabilities',tier='6',
  quote='Statutes of the Republic of Korea No. 30288 Promulgation Date 2019-12-31',
  why='NOT ADMITTED: wrong instrument; no ramp provision.',notes='Recorded so the elaw hseq is not re-fetched for this purpose.'),
 dict(url='https://elaw.klri.re.kr/eng_service/lawViewTitle.do?hseq=46425',lang='EN',juris='KR',tt='code',
  prior='Same expectation as for hseq 53020.',
  found_note='RETRIEVED, 200, 43 kB. Statutes of the Republic of Korea No. 15272, promulgated 2017-12-19: chapters on prohibition of discrimination (employment, education, goods and services) -- the anti-discrimination Act, not the convenience-promotion Enforcement Rule.',
  disp='OUT-OF-SCOPE',title='KLRI elaw hseq=46425: Statutes of the Republic of Korea No. 15272 (promulgated 2017-12-19), prohibition of discrimination against persons with disabilities',tier='6',
  quote='Statutes of the Republic of Korea No. 15272 Promulgation Date 2017-12-19',
  why='NOT ADMITTED: wrong instrument; no ramp provision.',notes='Recorded so the elaw hseq is not re-fetched for this purpose.'),
]
for j in J:
    a=art(j['url'])
    tname=a.rsplit('.',1)[0]+'-text.txt'
    txt = pdf_text(a) if a.endswith('.pdf') else html_text(a)
    (D/tname).write_text(txt,encoding='utf-8')
    rl.record_file(D/tname,S,source_artefact=a,purpose='Visible-text extraction for candidate staging',kind='text-extraction')
    f,w=rl.quote_in_artefacts(j['quote'])
    print(j['juris'],j['url'][-60:],'| quote',f,flush=True)
    r=run(['log-search','--slug','accessible-circulation-geometry','--language',j['lang'],'--query-text',j['url'],'--engine','web','--depth-method','scoping','--jurisdiction',j['juris'],'--target-evidence-type',j['tt'],'--prior-expectation',j['prior'],'--results-found','1','--results-screened','1','--results-admitted','0','--saturation-signal','partial','--harm-finding','0','--findings-note',j['found_note'],'--origin','planned','--result-artefact','retrieval-log/%s/%s'%(S,a),'--session',S])
    # exec id of the row just written
    import sqlite3
    con=sqlite3.connect('file:%s/batch23.db?mode=ro'%SCR,uri=True)
    eid=con.execute("select max(exec_id) from search_executions where query_text=?",(j['url'],)).fetchone()[0]
    run(['amend-search','--exec-id',str(eid),'--add-result-artefact','retrieval-log/%s/%s'%(S,tname),'--append-note','Linked a derived visible-text extraction so the candidate row can quote it.','--session',S])
    run(['add-candidate','--exec-id',str(eid),'--found-under-slug','accessible-circulation-geometry','--disposition',j['disp'],'--title',j['title'],'--locator',j['url'],'--locator-status','RESOLVED','--tier-guess',j['tier'],'--harm-finding','0','--why-not-admitted',j['why'],'--notes',j['notes'],'--surfaced-in','retrieval-log/%s/%s'%(S,tname),'--surfaced-quote',j['quote'],'--session',S])
# R5: re-target the two Co-1-channel follow-ups
import sqlite3
con=sqlite3.connect('file:%s/batch23.db?mode=ro'%SCR,uri=True)
for q in ('https://www.fub.se/files/bilagor/b8_fs_1-07_boverket.pdf','https://www.madrid.es/UnidadesDescentralizadas/Discapacidad/publicaciones/MetodologiaAccesibilidadEspaciosPublicos/metodologiaaccesibilidadespaciospublicos.pdf'):
    eid=con.execute("select exec_id from search_executions where query_text=? and created_by_session like '%batch-23%'",(q,)).fetchone()[0]
    run(['amend-search','--exec-id',str(eid),'--set-target-evidence-type','co1','--append-note',"target_evidence_type grey -> co1: this follow-up retrieved a candidate surfaced by a Co-1-channel search (disability-sector organisation output); 'grey' was the tier it was later ADMITTED at (T3), not what it was aimed at, and labelling a Swedish/Spanish search 'grey' reads as the language-based down-tiering R5 forbids. The admitted tier stays T3 grey: Co-1 provenance is not evidenced in the bytes (D-0178).",'--session',S])
