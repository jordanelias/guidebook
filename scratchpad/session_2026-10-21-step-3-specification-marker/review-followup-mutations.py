import subprocess, sys, shutil, json, os
REPO="/home/user/guidebook"
M=[
 ("MU1 confirmers read off the direction set", "scripts/assess/assess_cell.py",
  "confirmed = _confirmed_bands(conn, parameter_id, links, confirmer_anchors)",
  "confirmed = _confirmed_bands(conn, parameter_id, links, finding_anchors)", "scripts/tests/test_assess_cell_pilot.py"),
 ("MU2 unverified finding/confirming sources not flagged", "scripts/assess/assess_cell.py",
  "not _verified(r) for r in finding_recs + confirmer_recs if not _is_disqualified(r))",
  "not _verified(r) for r in finding_anchors if not _is_disqualified(r))", "scripts/tests/test_assess_cell_pilot.py"),
 ("MU3 mixed supersession not named", "scripts/assess/assess_cell.py",
  "if det_at == 0 and 0 < n_superseded < det_x:", "if False:", "scripts/tests/test_assess_cell_pilot.py"),
 ("MU4 staleness compares nothing", "scripts/assess/assess_cell.py",
  "diff = [f for f, was in zip(STORED_ANSWER, rest[len(LENS_ORDER):]) if det[f] != was]", "diff = []", "scripts/tests/test_assess_cell_pilot.py"),
 ("MU5 left-out findings not marked on the junction", "scripts/assess/assess_cell.py",
  'if frole in DIRECTION_SUPPLYING_ROLES and not superseded:', 'if False:', "scripts/tests/test_assess_cell_pilot.py"),
 ("MU6 amend-source engine-column guard removed", "scripts/db.py",
  "if field in dbcore.ENGINE_SOURCE_COLUMNS:", "if False:", "scripts/tests/test_db_amend_writers.py"),
 ("MU7 third junction removed", "scripts/dbcore.py",
  '"SELECT \'specification_extraction_links\', l.specification_id "', '"SELECT \'specification_extraction_links\', -1 "', "scripts/tests/test_db_amend_writers.py"),
 ("MU8 comparator not guarded", "scripts/dbcore.py",
  'ENGINE_EXTRACTION_COLUMNS = ("figure_role", "claim_type", "extraction_method", "claimed_value",\n                             "claimed_unit", "comparator")',
  'ENGINE_EXTRACTION_COLUMNS = ("figure_role", "extraction_method")', "scripts/tests/test_db_amend_writers.py"),
]
for name, path, old, new, test in M:
    f=os.path.join(REPO,path); orig=open(f,encoding="utf-8").read()
    assert orig.count(old)==1,(name, orig.count(old))
    open(f,"w",encoding="utf-8").write(orig.replace(old,new))
    try:
        r=subprocess.run([sys.executable, os.path.join(REPO,test)], capture_output=True, text=True, cwd=os.path.join(REPO,"scripts","tests"))
        out=r.stdout+r.stderr
        failed=[l.strip() for l in out.splitlines() if "FAIL:" in l or "[✗]" in l][:3]
        print(f"{'KILLED ' if r.returncode else 'SURVIVED'} {name}: rc={r.returncode} {failed[:2]}")
    finally:
        open(f,"w",encoding="utf-8").write(orig)
