import sys, sqlite3
sys.path.insert(0,'/home/user/guidebook'); sys.path.insert(0,'/home/user/guidebook/scripts'); sys.path.insert(0,'/home/user/guidebook/scripts/assess')
import assess_cell as A
conn=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True)
cells=set()
for pid,i,c,n in conn.execute("select x.parameter_id,l.identity_code,l.icf_code,l.needs_code from extraction_lens_links l join source_value_extractions x using(extraction_id) where l.retired_at is null and x.retired_at is null"):
    for k,v in (("identity_code",i),("icf_code",c),("needs_code",n)):
        if v: cells.add((pid,k,v))
for pid,k,v in sorted(cells):
    lens={"identity_code":None,"icf_code":None,"needs_code":None}; lens[k]=v
    try: d=A.determine(conn,pid,lens,"probe","")
    except Exception as e:
        print(pid,k,v,"REFUSED",type(e).__name__, str(e)[:80]); continue
    links=d["links"]
    dirn=d["accessibility_direction"]
    add=[dict(l,role="governing") for l in links if l["role"]=="excluded" and "not in the governing set" in (l.get("exclusion_reason") or "")]
    after=A.compose_value(conn,[l for l in links if l["role"]=="governing"]+add,dirn)
    print(pid,k,v,d["state"],d["design_scale"],d["marker"],"rso",d["regulatory_stratum_only"],"today",(d["value_min"],d["value_max"],d["value_unit"]),"| union-candidates",len(add),sorted({l['ref_id'] for l in add}),"after",after[:3])
