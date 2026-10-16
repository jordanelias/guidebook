import sqlite3, sys
blob, chain = sys.argv[1], sys.argv[2]
a = sqlite3.connect(f"file:{blob}?mode=ro", uri=True); b = sqlite3.connect(f"file:{chain}?mode=ro", uri=True)
VOL = {"created_at","updated_at","last_updated","updated_by_session","created_by_session"}
def rows(c, t, pk):
    cols=[r[1] for r in c.execute(f'pragma table_info("{t}")')]
    return cols, {tuple(r[cols.index(k)] for k in pk): dict(zip(cols,r)) for r in c.execute(f'select * from "{t}"')}
cols, A = rows(a,"evidence_sources",["ref_id"]); _, B = rows(b,"evidence_sources",["ref_id"])
print("evidence_sources only-in-blob", [k for k in A if k not in B], "only-in-chain", [k for k in B if k not in A])
n=0
for k in sorted(A):
    if k in B:
        d={c:(A[k][c],B[k][c]) for c in cols if A[k][c]!=B[k][c] and c not in VOL}
        if d:
            print(k, len(d), {c:v for c,v in d.items()}); n+=len(d)
print("substantive values differing:", n)
cols, A = rows(a,"evidence_source_authors",["id"]); _, B = rows(b,"evidence_source_authors",["id"])
print("authors: blob", len(A), "chain", len(B), "only-in-blob", sorted(k[0] for k in A if k not in B), "only-in-chain", sorted(k[0] for k in B if k not in A))
print("authors in both ids that differ:", [k for k in A if k in B and any(A[k][c]!=B[k][c] for c in cols if c not in VOL)])
