import sys, urllib.parse
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SESS='session_2026-11-06-pipeline-batch'
base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
qs={'B2':'wheelchair AND (doorway OR "door width" OR "corridor width") AND (qualitative OR interview OR "focus group" OR participatory OR "lived experience" OR barriers)',
    'B3':'wheelchair AND doorway AND width'}
ids=set()
for tag,q in qs.items():
    r=rl.fetch(base+'esearch.fcgi?db=pubmed&retmode=json&retmax=50&term='+urllib.parse.quote(q),session=SESS,purpose=f'PubMed esearch, second-shape search {tag} after the adversarial pass')
    l=r['esearchresult']['idlist']; print(tag,r['esearchresult']['count'],l); ids|=set(l)
rl.fetch(base+'efetch.fcgi?db=pubmed&retmode=xml&id='+','.join(sorted(ids)),session=SESS,purpose='PubMed efetch of the hits of B2 and B3')
for pm in ('20434614','20402047'):
    rl.fetch(f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{pm}%20AND%20SRC:MED&format=json&resultType=core',session=SESS,purpose=f'Europe PMC open-access status of PMID {pm} (the check that findings_note of exec 197 reports)')
