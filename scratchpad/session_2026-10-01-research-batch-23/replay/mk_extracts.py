import sys, pymupdf
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
from pathlib import Path
S='session_2026-10-01-research-batch-23'
S21='session_2026-09-28-research-batch-21-selection'
D=Path('retrieval-log')/S
jobs=[
 ('REF-01026', S, '5744dca7ef1cf836.pdf', [1,2,15,16,20,21], 'Decreto-Lei 163/2006 (Ordem dos Arquitectos transcription) pages 1-2 (title, index), 15-16 (Anexo start, 1.4-1.5), 20-21 (2.5 Rampas)'),
 ('REF-01027', S, '1bc0a3fe0bdf78f2.pdf', [1,2,27,28], 'CTE DB-SUA con comentarios pages 1-2 (title, amendment history, version list), 27-28 (SUA 1 4.3 Rampas)'),
 ('REF-01030', S, '46aa46c118ba1973.pdf', [1,2,3,12,13], 'DHUP illustrated guide ERP/IOP existants pages 1-3 (title, contents, preface), 12-13 (B-2 cheminements: pentes)'),
 ('REF-01024', S, 'd0e4842fc285e85f.pdf', list(range(1,9)), 'BFS 2011:5 ALM 2, all 8 pages'),
 ('REF-01023', S, 'b8d1102ac9bece6f.pdf', [1,4,9], 'BFS 2024:12 pages 1 (title), 4 (2 kap. 4 par.), 9 (ikrafttradande)'),
 ('REF-01020', S, '445edc74b42c3d94.pdf', [1,5,6,35], 'Staatsblad 2024 nr 368 pages 1 (title), 5-6 (art. 4.30 amendment, onderdelen R-S), 35 (nota van toelichting on onderdeel R)'),
 ('REF-01022', S, 'bb47a9cd9c77bd86.pdf', [1,2], 'Ieder(in) reply to internetconsultatie Verzamelbesluit Bbl 2024, both pages'),
 ('REF-01025', S, '488584f70967745f.pdf', list(range(1,8)), 'FUB yttrande 2007-01-10, all 7 pages'),
 ('REF-01029', S21, '76d6a5953998c402.pdf', [1,2,5,10,24,68], 'CERMI Comunidad de Madrid Metodologia (Dec 2018) pages 1-2 (title, index), 5 (philosophy), 10 (orografia, 6%/10%), 24 (rampas), 68 (con el apoyo de)'),
]
for ref, sess, pdf, pages, purpose in jobs:
    path = Path('retrieval-log')/sess/pdf
    d = pymupdf.open(path)
    out = []
    for p in pages:
        out.append(f'[PDF page {p} of {len(d)}]\n' + d[p-1].get_text())
    name = f'{pdf[:-4]}-text.txt'
    fp = D/name
    fp.write_text('\n'.join(out), encoding='utf-8')
    sha = rl.record_file(fp, S, source_artefact=pdf, purpose='PyMuPDF text extraction, '+purpose, ref_id=ref, kind='text-extraction')
    print(ref, name, len(out), sha[:12])
