"""Equivalents pass PT-PT: append a prior to the search log, fetch through retrieval_log, extract text.
Usage (from repo root): python3 -I <this> ID URL "PURPOSE" "PRIOR"
Writes text to terminology-pass/PT-PT/text/<sha12>.txt and appends ID/URL/prior then the result to the log."""
import sys, json, re, html, subprocess, pathlib
sys.path.insert(0, 'scripts/research')
import retrieval_log as r
SID = 'session_2026-11-06-base-vocabulary-review'
P = pathlib.Path('scratchpad') / SID / 'terminology-pass/PT-PT'
LOG = P / 'equivalents-search-log.md'
qid, url, purpose, prior = sys.argv[1:5]
with LOG.open('a') as f:
    f.write(f"\n## {qid}\n- Fetch: `{url}`\n- Prior (written before the call): {prior}\n")
r.fetch(url, session=SID, purpose='equivalents PT-PT: ' + purpose)
man = pathlib.Path('retrieval-log') / SID / 'manifest.jsonl'
m = [json.loads(l) for l in man.read_text().splitlines() if l.strip()]
m = [x for x in m if x['url'] == url][-1]
src = man.parent / m['artefact']
b = src.read_bytes()
if b[:4] == b'%PDF':
    t = subprocess.run(['pdftotext', '-layout', str(src), '-'], capture_output=True).stdout.decode('utf-8', 'replace')
else:
    cs = re.search(rb'charset=["\']?([\w-]+)', b[:3000])
    enc = cs.group(1).decode() if cs else 'utf-8'
    try:
        s = b.decode(enc) if enc.lower()!="utf-8" else b.decode("utf-8")
    except Exception:
        s = b.decode("latin-1")
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)
    s = re.sub(r'(?i)<br\s*/?>|</(p|div|tr|li|h\d|table|td|th|dt|dd)>', '\n', s)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0', ' ')
    s = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in s.split('\n'))
    t = re.sub(r'\n{2,}', '\n', s)
out = P / 'text' / (m['sha256'][:12] + '.txt')
out.write_text(t, encoding='utf-8')
res = f"status {m['status']}, {m['bytes']} bytes, artefact {m['artefact']}, sha256 {m['sha256']}, text {len(t)} chars -> text/{out.name}"
print(res)
with LOG.open('a') as f:
    f.write(f"- Retrieval: {res}\n")
