"""Convert a BWB 'toestand' XML (wetten.overheid.nl repository) into located plain text.
Usage: python3 -I x2t.py <in.xml> <out.txt>
Each structural heading (hoofdstuk/afdeling/paragraaf/artikel) is written on its own line prefixed by
'##'; lid numbers and list numbers are kept; table rows are written one per line with cells joined by ' | '.
meta-data blocks (publication history) are dropped. Text content is otherwise unchanged."""
import sys, re
import xml.etree.ElementTree as ET

src, dst = sys.argv[1], sys.argv[2]
root = ET.parse(src).getroot()
out = []
DROP = {'meta-data', 'jcis'}
STRUCT = {'hoofdstuk', 'afdeling', 'paragraaf', 'artikel', 'bijlage', 'divisie'}

def text_of(e):
    """All text of e, minus dropped children, with whitespace collapsed."""
    parts = []
    def walk(x):
        if x.tag in DROP:
            if x.tail: parts.append(x.tail)
            return
        if x.text: parts.append(x.text)
        for c in x: walk(c)
        if x.tail: parts.append(x.tail)
    if e.text: parts.append(e.text)
    for c in e: walk(c)
    return re.sub(r'\s+', ' ', ''.join(parts)).strip()

def emit(e):
    tag = e.tag
    if tag in DROP: return
    if tag in STRUCT:
        kop = e.find('kop')
        head = text_of(kop) if kop is not None else ''
        out.append('')
        out.append('## ' + (tag.upper() + ' ' if not head.lower().startswith(tag) else '') + head)
        for c in e:
            if c.tag != 'kop': emit(c)
        return
    if tag in ('lid', 'li'):
        # children in DOCUMENT ORDER; the lid/list number prefixes the first line that follows it
        nrtag = 'lidnr' if tag == 'lid' else 'li.nr'
        nr = e.find(nrtag)
        prefix = (('[lid ' + text_of(nr) + '] ') if tag == 'lid' else ('  ' + text_of(nr) + ' ')) if nr is not None else ('' if tag == 'lid' else '  ')
        first = True
        for c in e:
            if c.tag == nrtag: continue
            if c.tag == 'al':
                out.append((prefix if first else ('' if tag == 'lid' else '  ')) + text_of(c)); first = False
            else:
                if first and prefix.strip(): out.append(prefix.rstrip()); first = False
                emit(c)
        return
    if tag == 'al':
        out.append(text_of(e)); return
    if tag == 'row':
        out.append('  | ' + ' | '.join(text_of(c) for c in e if c.tag == 'entry')); return
    if tag == 'title':
        out.append('  [tabel] ' + text_of(e)); return
    if tag in ('intitule', 'citeertitel', 'considerans.al'):
        out.append(text_of(e)); return
    if tag == 'illustratie':
        out.append('  [illustratie: ' + (e.get('naam') or '') + ' — image, not read]'); return
    for c in e: emit(c)

emit(root)
open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out), 'lines')
