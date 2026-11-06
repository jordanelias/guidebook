"""Strip an HTML artefact to text: block elements become line breaks, script/style/nav dropped.
Usage: python3 -I h2t.py IN.html OUT.txt   (prints sha256 of OUT)"""
import sys, html, re, hashlib
from html.parser import HTMLParser
BLOCK = {'p','div','br','li','h1','h2','h3','h4','h5','h6','tr','td','th','section','article','dt','dd','table','ul','ol','header','footer','blockquote'}
SKIP = {'script','style','noscript','svg','template'}
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in SKIP: s.skip+=1
        if t in BLOCK: s.o.append('\n')
    def handle_endtag(s,t):
        if t in SKIP and s.skip: s.skip-=1
        if t in BLOCK: s.o.append('\n')
    def handle_data(s,d):
        if not s.skip: s.o.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=''.join(p.o).replace('\xa0',' ')
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' *\n *','\n',t); t=re.sub(r'\n{3,}','\n\n',t)
open(sys.argv[2],'w',encoding='utf-8').write(t)
print(hashlib.sha256(t.encode()).hexdigest(), len(t))
