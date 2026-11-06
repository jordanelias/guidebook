"""Extract one Normattiva article page (uri-res/N2Ls ...~artN) to plain text.
Usage: python3 -I nt2txt.py <artefact.html>  -> text on stdout.
Takes the slice from the 'Testo in vigore dal' marker to the first 'articolo precedente' or 'articolo successivo' link, parses it with
html.parser (a regex tag-strip eats the '<----' graphic markers and the text after them),
keeps line breaks, collapses runs of spaces. Graphic parts are kept as the marker text."""
import sys, re
from html.parser import HTMLParser
s = open(sys.argv[1], encoding='utf-8').read()
i = s.find('Testo in vigore dal')
j = min(x for x in (s.find('articolo precedente', i), s.find('articolo successivo', i), len(s)) if x > 0)
seg = s[max(0, s.rfind('<', 0, i)):j]
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.out=[]; s.skip=0
    def handle_starttag(s, t, a):
        if t in ('script','style'): s.skip+=1
        if t in ('br','p','div','li','h1','h2','h3','h4','tr'): s.out.append('\n')
    def handle_endtag(s, t):
        if t in ('script','style'): s.skip-=1
        if t in ('p','div','li','h1','h2','h3','h4','tr'): s.out.append('\n')
    def handle_data(s, d):
        if not s.skip: s.out.append(d)
    def handle_comment(s, d): pass
p = P(); p.feed(seg)
t = ''.join(p.out)
t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r' *\n *', '\n', t); t = re.sub(r'\n{2,}', '\n', t)
# drop the metadata comment residue lines (flagTipoArticolo etc.)
t = '\n'.join(l for l in t.split('\n') if not re.match(r'^(flagTipoArticolo|descrizione|descrizioneConParte|descrizioneCommiParte|progressivo|version|tipoArticolo):|^-->$', l))
print(t.strip())
