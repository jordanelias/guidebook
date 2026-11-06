"""Strip a law.go.kr HTML fragment to text, one block per line. Usage: python3 -I h2t.py IN.html OUT.txt"""
import re, sys, html
h = open(sys.argv[1], encoding='utf-8', errors='replace').read()
h = re.sub(r'(?is)<(script|style)\b.*?</\1>', '', h)
h = re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h\d|table)>', '\n', h)
t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
t = '\n'.join(re.sub(r'[ \t ]+', ' ', l).strip() for l in t.split('\n'))
t = re.sub(r'\n{2,}', '\n', t).strip() + '\n'
open(sys.argv[2], 'w', encoding='utf-8').write(t)
print(len(t))
