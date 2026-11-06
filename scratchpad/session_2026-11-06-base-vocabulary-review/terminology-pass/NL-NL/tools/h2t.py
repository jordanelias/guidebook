"""Strip an HTML page to plain text (scripts/styles dropped, tags removed, entities unescaped, whitespace collapsed per block).
Usage: python3 -I h2t.py <in.html> <out.txt>"""
import sys, re, html
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = re.sub(r'<(script|style|noscript)\b.*?</\1>', ' ', t, flags=re.S | re.I)
t = re.sub(r'<(br|/p|/div|/li|/h[1-6]|/tr)\b[^>]*>', '\n', t, flags=re.I)
t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
lines = [re.sub(r'[ \t\xa0]+', ' ', l).strip() for l in t.split('\n')]
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(l for l in lines if l) + '\n')
