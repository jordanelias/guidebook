"""Strip a PGDL (ISO-8859-1) HTML page to text, one block per line. Usage: python3 -I h2t.py IN OUT"""
import re, html, sys
b = open(sys.argv[1], 'rb').read().decode('latin-1')
b = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', b)
b = re.sub(r'(?i)<br\s*/?>|</(p|div|tr|li|h\d|table|td)>', '\n', b)
t = html.unescape(re.sub(r'<[^>]+>', ' ', b)).replace('\xa0', ' ')
t = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n'))
t = re.sub(r'\n{2,}', '\n', t)
open(sys.argv[2], 'w', encoding='utf-8').write(t)
