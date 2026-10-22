import sys, json
sys.path.insert(0,'/home/user/guidebook/scripts/tests'); sys.path.insert(0,'/home/user/guidebook/scripts/assess'); sys.path.insert(0,'/home/user/guidebook/scripts'); sys.path.insert(0,'/home/user/guidebook')
import test_assess_cell_pilot as t
from assess_cell import determine

def S(tier, et, val, cmp_=">=", unit="mm", ref=None, jur=None, **k):
    d={"tier":tier,"evidence_type":et,"claimed_value":str(val),"claimed_unit":unit,"comparator":cmp_}
    if ref: d["ref_id"]=ref
    if jur: d["jurisdiction"]=jur
    d.update(k); return d

T1=lambda v,**k: S(1,"clinical",v,**k)
T2=lambda v,**k: S(2,"sr_meta",v,**k)
CO1=lambda v,**k: S(1,"co1",v,**k)
T3C=lambda v,**k: S(3,"clinical",v,scope="lower_control",**k)
T4=lambda v,**k: S(4,"standard_eb",v,scope="international",**k)
T5=lambda v,**k: S(5,"national_fw",v,**k)
T6=lambda v,j,**k: S(6,"code",v,jur=j,**k)

def run(label, srcs, direction="higher_is_better", extra=None):
    conn=t.synth_db(srcs, direction=direction)
    if extra: extra(conn)
    d=determine(conn,1,{"identity_code":"MOB"},"s","n")
    by={r["ref_id"]:r for r in d["source_records"]}
    vals={r[0]:(r[1],r[2],r[3]) for r in conn.execute("select ref_id,claimed_value,comparator,claimed_unit from source_value_extractions")}
    print(f"\n== {label}  [{direction}]")
    print(f"   state={d['state']} marker={d['marker']} basis={d['tier_basis']} rso={d['regulatory_stratum_only']} proxy={d['rests_on_proxy_inference']}")
    print(f"   VALUE min={d['value_min']} max={d['value_max']} {d['value_unit']}  note={d['value_note']!r}")
    gov=d['governing_refs']
    print("   governing:", [(r, by[r]['tier'], by[r]['evidence_type'], vals[r][1]+vals[r][0]) for r in gov])
    print("   supporting:", d['supporting_refs'])
    ex=[l for l in d['links'] if l['role']=='excluded']
    seen=set()
    for l in ex:
        if l['ref_id'] in seen: continue
        seen.add(l['ref_id']); print(f"   excluded {l['ref_id']} (T{by[l['ref_id']]['tier'] if l['ref_id'] in by else '?'} {vals[l['ref_id']][1]}{vals[l['ref_id']][0]}): {l['exclusion_reason'][:110]}")
    print("   convergence:", (d['convergence'] or {}).get('status'), "|", ((d['convergence'] or {}).get('rationale') or '')[:90])
    print("   falsification:", (d['falsification'] or '')[:100])
    print("   mentions conflict/divergence anywhere:", any(w in json.dumps(d,default=str).lower() for w in ("conflict","diverg","contest","disagree")) and 'only in falsification boilerplate' )
    return d

run("G1 gradient across all tiers: T1 1500 / T2 1200 / T3c 1000 / T4 1100 / T5 1300 / T6 900,1000,1100",
    [T1(1500,ref="R-T1"),T2(1200,ref="R-T2"),T3C(1000,ref="R-T3C"),T4(1100,ref="R-T4"),T5(1300,ref="R-T5"),
     T6(900,"US",ref="R-T6a"),T6(1000,"GB",ref="R-T6b"),T6(1100,"AU",ref="R-T6c")])
run("G2 evidence says LESS than the code: T1 900 vs T6 codes 1200/1200/1200",
    [T1(900,ref="R-T1"),T6(1200,"US",ref="R-T6a"),T6(1200,"GB",ref="R-T6b"),T6(1200,"AU",ref="R-T6c")])
run("G3 same tier disagree: T1 900 vs T1 1500",
    [T1(900,ref="R-T1a"),T1(1500,ref="R-T1b")])
run("G4 three anchoring strata disagree: T1 1000 / Co-1 1500 / T2 1200",
    [T1(1000,ref="R-T1"),CO1(1500,ref="R-CO1",co1_source_type="dpo_annual_survey"),T2(1200,ref="R-T2")])
run("G5 T3-clinical alone vs codes: T3c 1500 vs T6 900,1000,1100",
    [T3C(1500,ref="R-T3C"),T6(900,"US",ref="R-T6a"),T6(1000,"GB",ref="R-T6b"),T6(1100,"AU",ref="R-T6c")])
run("G6 no anchors, regulatory stratum only, T4 1800 vs T5 1300 vs T6 900,1000",
    [T4(1800,ref="R-T4"),T5(1300,ref="R-T5"),T6(900,"US",ref="R-T6a"),T6(1000,"GB",ref="R-T6b")])
run("G7 units conflict across tiers: T1 mm vs T2 in",
    [T1(1000,ref="R-T1"),T2(40,unit="in",ref="R-T2")])
run("G8 comparators oppose: T1 >=1200 vs T2 <=1000",
    [T1(1200,ref="R-T1"),T2(1000,cmp_="<=",ref="R-T2")])
run("G9 lower_is_better ramp max: T1 8% / T2 5% / T6 8.33,8.33,6",
    [T1(8,unit="%",cmp_="<=",ref="R-T1"),T2(5,unit="%",cmp_="<=",ref="R-T2"),
     T6(8.33,"US",unit="%",cmp_="<=",ref="R-T6a"),T6(8.33,"GB",unit="%",cmp_="<=",ref="R-T6b"),T6(6,"AU",unit="%",cmp_="<=",ref="R-T6c")],
    direction="lower_is_better")
run("G10 contested direction with a gradient",
    [T1(900,ref="R-T1a"),T1(1500,ref="R-T1b")], direction="contested")
def addrow(conn):
    conn.execute("insert into source_value_extractions (ref_id,slug,parameter_id,identity_code,claim_type,claimed_value,claimed_unit,figure_role,comparator) values ('R-T1','s',1,'MOB','numerical','1500','mm','claim','>=')")
run("G11 SAME SOURCE contests itself (D-0168): one T1 source, rows 900 and 1500",
    [T1(900,ref="R-T1")], extra=addrow)
