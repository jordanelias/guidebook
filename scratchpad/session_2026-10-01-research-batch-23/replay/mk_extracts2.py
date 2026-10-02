import sys, re, html, pymupdf
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
from pathlib import Path
S='session_2026-10-01-research-batch-23'
D=Path('retrieval-log')/S
def pdf_text(name, pages=None):
    d=pymupdf.open(D/name); n=len(d)
    ps=pages or list(range(1,n+1))
    return '\n'.join(f'[PDF page {p} of {n}]\n'+d[p-1].get_text() for p in ps)
def html_text(name):
    raw=(D/name).read_bytes().decode('utf-8',errors='strict')
    s=re.sub(r'(?is)<(script|style|noscript).*?</\1>','',raw)
    s=re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|td|th|table|ul|ol|section)>','\n',s)
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    return '\n'.join(l for l in (re.sub(r'[ \t ]+',' ',x).strip() for x in s.split('\n')) if l)
jobs=[('24b5e81b0f4a0928.pdf',pdf_text,None,'BFS 2024:13 (Boverket, requirements on plots), all 5 pages'),
      ('6ce224bbadd7b205.pdf',pdf_text,None,'Stockholm Gatu- och fastighetskontoret tjansteutlatande 2001-08-02 (insynsverige), all 4 pages'),
      ('a426a8c5ff9b197e.pdf',pdf_text,None,'CEN/CLC JTC 11 EN 17210 workshop deck (UNE), all 18 slides'),
      ('f9b1b4f92ea0ebc2.html',html_text,None,'ABCB NCC 2022 Vol. 2 Part H8 page, visible text'),
      ('ce7c5fdc63f3bb2c.html',html_text,None,'BOE Orden VIV/561/2010 consolidated page, visible text')]
for art,fn,_,purpose in jobs:
    txt=fn(art)
    name=art.rsplit('.',1)[0]+'-text.txt'
    (D/name).write_text(txt,encoding='utf-8')
    sha=rl.record_file(D/name,S,source_artefact=art,purpose='Visible-text extraction, '+purpose,kind='text-extraction')
    print(name,len(txt),sha[:12])
