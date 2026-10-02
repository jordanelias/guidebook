import sys, re, html
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
from pathlib import Path
S='session_2026-10-01-research-batch-23'
D=Path('retrieval-log')/S
jobs=[
 ('REF-01019','7952f862b1bf1825.html','NEPLA wiki page reproducing Enforcement Rule Annex 1 (Korea): visible text'),
 ('REF-01021','92deface20c53409.html','IPLO hellingbaan page (NL): visible text including the steilte table, one cell per line'),
 ('REF-01028','9f561626b2028bed.html','BOE consolidated Orden TMA/851/2021: visible text'),
]
for ref, art, purpose in jobs:
    raw = (D/art).read_bytes().decode('utf-8', errors='strict')
    s = re.sub(r'(?is)<(script|style|noscript).*?</\1>','',raw)
    s = re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|td|th|table|ul|ol|section)>','\n',s)
    s = re.sub(r'<[^>]+>','',s)
    s = html.unescape(s)
    lines = [re.sub(r'[ \t ]+',' ',l).strip() for l in s.split('\n')]
    txt = '\n'.join(l for l in lines if l)
    name = f'{art[:-5]}-text.txt'
    (D/name).write_text(txt, encoding='utf-8')
    sha = rl.record_file(D/name, S, source_artefact=art, purpose='HTML visible-text extraction (regex tag strip, html.unescape), '+purpose, ref_id=ref, kind='text-extraction')
    print(ref, name, len(txt), sha[:12])
