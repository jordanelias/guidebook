import sys, re, html
src, dst = sys.argv[1], sys.argv[2]
b = open(src,'rb').read()
m = re.search(rb'charset=["\']?([\w-]+)', b[:3000])
enc = (m.group(1).decode() if m else 'utf-8')
t = b.decode(enc, errors='replace')
t = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', t)
t = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>', '\n', t)
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'[ \t\xa0]+', ' ', t)
t = re.sub(r'\n\s*\n+', '\n', t)
open(dst,'w',encoding='utf-8').write(t.strip()+'\n')
print(enc, len(t))
