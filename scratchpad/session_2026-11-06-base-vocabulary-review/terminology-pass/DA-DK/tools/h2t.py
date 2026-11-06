"""Strip a persisted HTML artefact to text: drop script/style/nav/header/footer, keep block breaks.
Usage: python3 -I h2t.py <artefact.html> <out.txt>   (prints sha256 of the output)"""
import re, sys, html, hashlib
t = open(sys.argv[1], encoding='utf-8', errors='strict').read()
t = re.sub(r'(?is)<(script|style|noscript|svg|header|footer|nav)\b.*?</\1>', ' ', t)
t = re.sub(r'(?i)<br\s*/?>', '\n', t)
t = re.sub(r'(?i)</?(p|div|h[1-6]|li|tr|table|section|article|ul|ol|dt|dd)\b[^>]*>', '\n', t)
t = re.sub(r'(?i)</t[dh]>', ' | ', t)
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(t).replace('\xa0', ' ')
t = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n'))
t = re.sub(r'\n{3,}', '\n\n', t).strip() + '\n'
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print(hashlib.sha256(t.encode()).hexdigest(), len(t))
