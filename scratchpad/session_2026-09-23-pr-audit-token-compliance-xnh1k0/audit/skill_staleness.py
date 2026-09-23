# Staleness of .claude/skills/*/SKILL.md against the live DB and db.py (run from repo root)
import re,glob,sqlite3
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
tables={r[0] for r in con.execute("select name from sqlite_master where type in('table','view')")}
cnt={t:con.execute(f'select count(*) from "{t}"').fetchone()[0] for t in tables if not t.startswith('sqlite_')}
subs=set(re.findall(r"add_parser\(\s*['\"]([a-z0-9-]+)",open('scripts/db.py').read()))
print('items rows:',cnt.get('items'),' item_audit_runs rows:',cnt.get('item_audit_runs'))
for f in sorted(glob.glob('.claude/skills/*/SKILL.md')):
    s=open(f).read()
    ic=len(re.findall(r'\bitem_code\b',s)); codes=len(re.findall(r'\b[A-Z]-\d{2}\b',s))
    dbsubs=set(re.findall(r'db\.py\s+([a-z][a-z0-9-]+)',s))
    missing=sorted(d for d in dbsubs if d not in subs)
    itemsub=sorted(d for d in dbsubs if d in('add-item','items','add-audit-run','update-audit-run','audit-runs'))
    tabs=set(re.findall(r'\b([a-z_]{4,})\b',s))&set(cnt)
    emptyt=sorted(t for t in tabs if cnt[t]==0)
    stale = ic or codes>2 or missing or itemsub
    if stale or emptyt:
        print(f"{f.split('/')[2]:34} item_code={ic:3} itemcodes={codes:3} missing_subcmds={missing} item_subcmds={itemsub} empty_tables_named={emptyt}")
