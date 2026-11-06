# Verifies every non-seed quote and form in equivalents.tsv against the retrieved bytes (pdftotext layout/raw/plain, or HTML/XML unescaped). Run from the repository root: python3 -I <this file>. Exits 1 on any failure.
import csv,re,html,subprocess,sys,pathlib
T='scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/SV-SE/'
R='retrieval-log/session_2026-11-06-base-vocabulary-review/'
n=lambda s:re.sub(r'\s+',' ',s).strip()
cache={}
def texts(art):
    if art in cache: return cache[art]
    p=pathlib.Path(R+art); out=[]
    loc=pathlib.Path(T+'text/'+art.split('.')[0]+'.txt')
    if loc.exists(): out.append(loc.read_text())
    if p.suffix=='.pdf':
        for mode in (['-layout'],['-raw'],[]):
            out.append(subprocess.run(['pdftotext',*mode,str(p),'-'],capture_output=True,text=True).stdout)
    else:
        b=p.read_bytes().decode('utf-8','replace'); out.append(b)
        u=html.unescape(re.sub(r'<[^>]+>',' ',html.unescape(b))); out.append(u)
        out.append(html.unescape(re.sub(r'<[^>]+>',' ',b)))
    cache[art]=[n(x) for x in out]; return cache[art]
bad=0;k=0
for r in csv.DictReader(open(T+'equivalents.tsv'),delimiter='\t'):
    if r['attestation_tier']=='seed': continue
    k+=1; art=re.search(r'artefact (\S+)$',r['source']).group(1)
    q=n(r['quote']); ok=any(q in t for t in texts(art))
    fm=any(n(r['form']).replace(' (prefix)','').lower() in t.lower() for t in texts(art))
    if not ok or not fm: bad+=1; print('FAIL',r['concept_id'],r['form'],'quote' if not ok else '', 'form' if not fm else '')
    if len(r['quote'].split())>25: print('LONG',r['form'],len(r['quote'].split()))
print('EXAMINED:',k,'failures:',bad); sys.exit(1 if bad else 0)
