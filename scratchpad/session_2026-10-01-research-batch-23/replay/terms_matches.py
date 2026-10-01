import os, subprocess, sys
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
def run(args):
    r=subprocess.run(['python3','scripts/db.py']+args,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print('  ',r.returncode,' | '.join(out[-3:])[:300],flush=True)
T=[
 ('REF-01019','경사로','KO','별표 1 제12호 나목(1)','경사로의 기울기는 12분의 1 이하로 하여야 한다.'),
 ('REF-01020','hellingbaan','NL','nota van toelichting, onderdeel R','In deze artikelen is, net als in de artikelen 4.25 en 4.192, sprake van een benodigde hellingbaan bij hoogteverschillen van meer dan 20 mm.'),
 ('REF-01021','hellingbaan','NL','IPLO, Hoogteverschillen overbruggen voor personen','Een hellingbaan in het Bbl is bedoeld voor personen om hoogteverschillen mee te kunnen overbruggen.'),
 ('REF-01022','hellingbanen','NL','Letter p. 1, third bullet','De eisen voor hellingbanen worden aangepast zodat ze in lijn zijn met de NEN- norm 9120 die in ontwikkeling is.'),
 ('REF-01023','ramp','SV','2 kap. 4 §','En ramp, som är till för att uppfylla kraven enligt 1 § och 2 § andra stycket, ska luta högst 1:12.'),
 ('REF-01024','utjämning till 0-nivå','SV','8 §, Allmänt råd','En utjämning till 0-nivå bör inte ha större lutning än 1:12.'),
 ('REF-01025','ramplutning','SV','punkt 3:1222','En ramplutning på 1:12 är en säkerhetsrisk.'),
 ('REF-01026','inclinação','PT','Anexo 2.5.1 1)','Ter uma inclinação não superior a 6%, vencer um desnível não superior a 0,6 m'),
 ('REF-01027','pendiente','ES','SUA 1, 4.3.1(1)','Las rampas tendrán una pendiente del 12%, como máximo, excepto:'),
 ('REF-01028','pendiente longitudinal','ES','art. 14.2 c)','La pendiente longitudinal máxima será del 10% para tramos de hasta 3,00 m de longitud'),
 ('REF-01029','Pendientes longitudinales máximas','ES','p. 24','Pendientes longitudinales máximas Rampas de menos de 3 m. pendiente máxima 10%.'),
 ('REF-01030','plan incliné','FR','Guide p. 12, B-2 2° a)','un plan incliné de pente inférieure ou égale à 6 % est aménagé'),
]
for ref,sf,lang,loc,q in T:
    f,w=rl.quote_in_artefacts(q,ref_id=ref)
    print(ref,sf,'quote found' if f else 'QUOTE MISSING')
    run(['observe-term','--ref-id',ref,'--surface-form',sf,'--language',lang,'--locator',loc,'--context-quote',q,'--session',S])
NOTE_CODE="PROXY by construction: a code or standard asserts a figure; it does not study a population, so there is no population-of-study to compare against mobility-device users. Same grading as REF-00987 (ADA), REF-00994 (IPC) and REF-00995 (Flemish decree). The 2026-09-25 owner ruling on PARTIAL applies to a facility AUDIT's measured sample and does not transfer to a statute (batch 22 finding 0e)."
M=[
 ('REF-01019','PROXY','no participants; a regulatory text (Korean enforcement-rule annex)',NOTE_CODE),
 ('REF-01020','PROXY','no participants; a regulatory amending decree (Dutch Staatsblad)',NOTE_CODE),
 ('REF-01021','PROXY','no participants; a government guidance page restating a regulation',NOTE_CODE.replace('a code or standard asserts','a guidance page restating a regulation asserts')),
 ('REF-01022','PARTIAL','no participants; the position of Ieder(in), a national network of people with any disability or chronic illness, stated in a consultation letter',"The author body speaks for people with any disability or chronic illness, which includes mobility-device users but is not specific to them; no sample, no members named, a position and not a measurement. PARTIAL for MOB, not EXACT."),
 ('REF-01023','PROXY','no participants; a binding regulation (Boverket BFS)',NOTE_CODE),
 ('REF-01024','PROXY','no participants; regulation with general advice (Boverket BFS 2011:5 ALM 2)',NOTE_CODE),
 ('REF-01025','PROXY','no participants; consultation reply by an organisation for people with intellectual disability and their families (Riksförbundet FUB)',"The author organisation's stated constituency is intellectual disability, not manual wheelchair users, and the retrieved bytes evidence no wheelchair-user authorship (D-0178). The claim concerns wheelchair ramp safety, so it is advocacy about MOB by a non-MOB body: PROXY, not Co-1."),
 ('REF-01026','PROXY','no participants; a regulatory text (Portuguese decree, transcription)',NOTE_CODE),
 ('REF-01027','PROXY','no participants; a regulatory technical document (Spanish CTE DB-SUA)',NOTE_CODE),
 ('REF-01028','PROXY','no participants; a regulatory order (Spanish BOE)',NOTE_CODE),
 ('REF-01029','PARTIAL','no participants stated; methodology document authored by CERMI Comunidad de Madrid, a cross-disability platform',"A cross-disability platform's methodology covering universal accessibility in public space, which includes mobility; no sample, no named authors, no statement that disabled people wrote it (D-0178). PARTIAL for MOB."),
 ('REF-01030','PROXY','no participants; a ministry guide reproducing a regulation and commenting on it',NOTE_CODE.replace('a code or standard asserts','a ministry guide reproducing a regulation asserts')),
]
for ref,g,sp,note in M:
    print(ref,g,end=' ->')
    run(['add-population-match','--ref-id',ref,'--target-population','MOB','--study-population',sp,'--match-grade',g,'--mismatch-note',note,'--session',S])
