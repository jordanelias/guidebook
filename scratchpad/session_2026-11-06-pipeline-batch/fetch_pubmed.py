import sys, urllib.parse
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SESS='session_2026-11-06-pipeline-batch'
q1='wheelchair AND (turning space OR turning radius OR maneuvering space) AND (dimensions OR anthropometry OR clearance)'
q2='(wheelchair OR "people with disabilities") AND (doorway OR "door width" OR "corridor width") AND (participatory OR "focus group" OR "lived experience")'
base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
for tag,q in (('Q1',q1),('Q2',q2)):
    u=base+'esearch.fcgi?db=pubmed&retmode=json&retmax=50&term='+urllib.parse.quote(q)
    r=rl.fetch(u,session=SESS,purpose=f'PubMed esearch, search {tag} of the batch (re-run of the MCP search, persisted)')
    print(tag, r and r.get('esearchresult',{}).get('count'), r and r['esearchresult']['idlist'])
u=base+'efetch.fcgi?db=pubmed&retmode=xml&id=20434614,20402047,21657823,18002971,36038463'
r=rl.fetch(u,session=SESS,purpose='PubMed efetch of the five PMIDs returned by Q1/Q2')
print('efetch', type(r))
