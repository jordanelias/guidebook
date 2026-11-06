"""Strip an HTML artefact to text (block tags become newlines). Usage: python3 -I h2t.py IN.html OUT.txt"""
import re, sys, html
s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
s = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', s)
s = re.sub(r'(?is)<!--.*?-->', ' ', s)
s = re.sub(r'(?i)<(br|/p|/div|/li|/h[1-6]|/tr|/td|/th|/caption|/figcaption|/section|/article|/table|/dt|/dd)\b[^>]*>', '\n', s)
s = re.sub(r'(?s)<[^>]+>', ' ', s)
s = html.unescape(s).replace('\xa0', ' ')
s = re.sub(r'[ \t]+', ' ', s)
s = re.sub(r'\n\s*\n+', '\n', s)
open(sys.argv[2], 'w', encoding='utf-8').write(s.strip() + '\n')
