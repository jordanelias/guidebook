import sqlite3, sys, shutil
sys.path.insert(0, "scripts")
import dbcore
blob, chain, scratch, session = sys.argv[1:5]
shutil.copy(blob, scratch)
s = sqlite3.connect(scratch); c = sqlite3.connect(f"file:{chain}?mode=ro", uri=True)
VOL = {"created_at","updated_at","last_updated","updated_by_session","created_by_session"}
cols = [r[1] for r in c.execute('pragma table_info("evidence_sources")')]
chain_rows = {r[0]: dict(zip(cols, r)) for r in c.execute('select * from evidence_sources')}
n = 0
for r in s.execute('select * from evidence_sources').fetchall():
    row = dict(zip(cols, r)); ref = row["ref_id"]
    diff = [k for k in cols if k not in VOL and row[k] != chain_rows[ref][k]]
    if diff:
        sets = {k: chain_rows[ref][k] for k in diff}
        sets.update(dbcore.upd(session))
        s.execute('update evidence_sources set ' + ", ".join(f'"{k}"=?' for k in sets) + ' where ref_id=?', [*sets.values(), ref]); n += 1
acols = [r[1] for r in c.execute('pragma table_info("evidence_source_authors")')]
cids = {r[0] for r in c.execute('select id from evidence_source_authors')}
sids = {r[0] for r in s.execute('select id from evidence_source_authors')}
s.executemany('delete from evidence_source_authors where id=?', [(i,) for i in sorted(sids - cids)])
for i in sorted(cids - sids):
    row = c.execute('select * from evidence_source_authors where id=?', (i,)).fetchone()
    s.execute('insert into evidence_source_authors (' + ",".join(f'"{k}"' for k in acols) + ') values (' + ",".join("?" * len(acols)) + ')', row)
s.commit()
print("evidence_sources rows reverted:", n, "| authors deleted:", len(sids - cids), "restored:", len(cids - sids))
