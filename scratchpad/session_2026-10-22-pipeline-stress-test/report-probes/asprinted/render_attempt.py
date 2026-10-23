import sqlite3, json, sys
db=sys.argv[1]
c=sqlite3.connect(f"file:{db}?mode=ro",uri=True); c.row_factory=sqlite3.Row
print("v_best_practice rows:", c.execute("select count(*) from v_best_practice").fetchone()[0],
      "| v_pending:", c.execute("select count(*) from v_pending").fetchone()[0],
      "| v_code_floor_only:", c.execute("select count(*) from v_code_floor_only").fetchone()[0],
      "| v_determination_provenance:", c.execute("select count(*) from v_determination_provenance").fetchone()[0])
def term(pid):
    r=c.execute("select t.canonical_en from base_parameters p join terms t on t.term_id=p.term_id where p.parameter_id=?",(pid,)).fetchone(); return r[0] if r else f"parameter {pid}"
def lens(r):
    parts=[]
    for col,tab,key,lab in (("identity_code","base_taxonomy_identity","identity_code","label_en"),("icf_code","base_icf","icf_code","label_en"),("needs_code","access_needs","need_code","design_obligation"),("medical_code","base_taxonomy_medical","medical_code","label_en")):
        if r[col]:
            cols=[x[1] for x in c.execute(f"pragma table_info({tab})")]
            use=lab if lab in cols else cols[1]
            n=c.execute(f"select {use} from {tab} where {key}=?",(r[col],)).fetchone()
            parts.append(f"{r[col]} ({str(n[0])[:50] if n else '?'})")
    return " + ".join(parts)
rows=c.execute("select * from v_best_practice order by specification_id").fetchall()
print()
for r in rows[:2]:
    print("─"*78)
    print(f"RENDER of specification {r['specification_id']}")
    print(f"  Parameter : {term(r['parameter_id'])}")
    print(f"  Lens      : {lens(r)}")
    v=[]
    if r['value_min'] is not None: v.append(f"min {r['value_min']:g}")
    if r['value_max'] is not None: v.append(f"max {r['value_max']:g}")
    print(f"  Value     : {', '.join(v) or '(none)'} {r['value_unit'] or ''}   notations={r['value_notations']}")
    print(f"  Marker    : {r['marker']}   State: {r['state']}   scale: {r['design_scale']}")
    print(f"  Flags     : proxy={r['rests_on_proxy_inference']} regulatory_stratum_only={r['regulatory_stratum_only']} unverified={r['has_unverified_sources']} code_floor_only={r['code_floor_only']}")
    print(f"  Basis     : {r['tier_basis']}")
    print(f"  Note      : {r['value_note']}")
    print(f"  Falsifier : {(r['falsification_condition'] or '')[:120]}")
    print(f"  Functional: {r['derivation_paths']} ({len(json.loads(r['functional_basis'])) if r['functional_basis'] else 0} ICF entries)")
    prov=c.execute("select * from v_determination_provenance where specification_id=? limit 3",(r['specification_id'],)).fetchall()
    print(f"  provenance view rows for it: {c.execute('select count(*) from v_determination_provenance where specification_id=?',(r['specification_id'],)).fetchone()[0]}; columns: {list(prov[0].keys()) if prov else '-'}")
    n_cond=c.execute("select count(*) from specification_extraction_links where specification_id=? and role='conditioning'",(r['specification_id'],)).fetchone()[0]
    n_gov=c.execute("select count(*) from specification_extraction_links where specification_id=? and role='governing'",(r['specification_id'],)).fetchone()[0]
    print(f"  governing rows={n_gov} conditioning rows={n_cond} (conditions are linked, not attached to the value)")
print("─"*78)
print("PENDING cells a renderer must also show (v_pending):")
for r in c.execute("select * from v_pending limit 3"): print("  ", dict(r) if len(dict(r))<9 else list(dict(r).items())[:6])
