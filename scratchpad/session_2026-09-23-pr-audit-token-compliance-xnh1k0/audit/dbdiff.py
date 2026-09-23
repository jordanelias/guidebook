import sqlite3,sys,hashlib,subprocess,os
def load(rev,path):
    b=subprocess.run(['git','show',f'{rev}:data/guidebook.db'],capture_output=True).stdout
    open(path,'wb').write(b); return sqlite3.connect(path)
S=os.environ['S']
a=load(sys.argv[1],S+'/a.db'); b=load(sys.argv[2],S+'/b.db')
def tabs(c): return {r[0] for r in c.execute("select name from sqlite_master where type='table'")}
ta,tb=tabs(a),tabs(b)
for t in sorted(ta|tb):
    if t not in ta or t not in tb: print('TABLE', t, 'only in', 'a' if t in ta else 'b'); continue
    ra=set(a.execute(f'select * from "{t}"')); rb=set(b.execute(f'select * from "{t}"'))
    if ra!=rb: print(t, 'removed',len(ra-rb),'added',len(rb-ra))
print('uv', a.execute('pragma user_version').fetchone(), b.execute('pragma user_version').fetchone())
