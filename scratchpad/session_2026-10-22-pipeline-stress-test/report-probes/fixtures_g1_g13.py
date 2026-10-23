"""G1-G13 conflicting-value fixtures over the engine (in-memory synth_db). Read-only on the repo.
Usage: python3 -I fixtures_g1_g13.py /home/user/guidebook"""
import sys, json
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/user/guidebook"
for p in ("scripts/tests", "scripts/assess", "scripts", ""):
    sys.path.insert(0, f"{REPO}/{p}".rstrip("/"))
import test_assess_cell_pilot as t
from assess_cell import determine

def S(tier, et, val, cmp_=">=", unit="mm", ref=None, jur=None, **k):
    d = {"tier": tier, "evidence_type": et, "claimed_value": str(val), "claimed_unit": unit, "comparator": cmp_}
    if ref: d["ref_id"] = ref
    if jur: d["jurisdiction"] = jur
    d.update(k); return d
T1 = lambda v, **k: S(1, "clinical", v, **k)
T2 = lambda v, **k: S(2, "sr_meta", v, **k)
CO1 = lambda v, **k: S(1, "co1", v, co1_source_type="dpo_annual_survey", **k)
T3C = lambda v, **k: S(3, "clinical", v, scope="lower_control", **k)
T4 = lambda v, **k: S(4, "standard_eb", v, scope="international", **k)
T5 = lambda v, **k: S(5, "national_fw", v, **k)
T6 = lambda v, j, **k: S(6, "code", v, jur=j, **k)

def run(gid, srcs, direction="higher_is_better", extra=None):
    conn = t.synth_db(srcs, direction=direction)
    if extra: extra(conn)
    d = determine(conn, 1, {"identity_code": "MOB"}, "s", "n")
    ex = sorted({(l["ref_id"], (l["exclusion_reason"] or "")[:60]) for l in d["links"] if l["role"] == "excluded"})
    out = {"id": gid, "state": d["state"], "marker": d["marker"], "basis": d["tier_basis"],
           "min": d["value_min"], "max": d["value_max"], "unit": d["value_unit"],
           "note": (d["value_note"] or "")[:70], "conv": (d["convergence"] or {}).get("status"),
           "governing": d["governing_refs"], "excluded": [e[0] for e in ex],
           "excl_reason_sample": ex[0][1] if ex else None}
    print(json.dumps(out, ensure_ascii=False))
    return d

run("G1", [T1(1500, ref="R-T1"), T2(1200, ref="R-T2"), T3C(1000, ref="R-T3C"), T4(1100, ref="R-T4"),
           T5(1300, ref="R-T5"), T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b"), T6(1100, "AU", ref="R-T6c")])
run("G2", [T1(900, ref="R-T1"), T6(1200, "US", ref="R-T6a"), T6(1200, "GB", ref="R-T6b"), T6(1200, "AU", ref="R-T6c")])
run("G3", [T1(900, ref="R-T1a"), T1(1500, ref="R-T1b")])
run("G4", [T1(1000, ref="R-T1"), CO1(1500, ref="R-CO1"), T2(1200, ref="R-T2")])
run("G5", [T3C(1500, ref="R-T3C"), T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b"), T6(1100, "AU", ref="R-T6c")])
run("G6", [T4(1800, ref="R-T4"), T5(1300, ref="R-T5"), T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b")])
run("G7", [T1(1000, ref="R-T1"), T2(40, unit="in", ref="R-T2")])
run("G8", [T1(1200, ref="R-T1"), T2(1000, cmp_="<=", ref="R-T2")])
run("G9", [T1(8, unit="%", cmp_="<=", ref="R-T1"), T2(5, unit="%", cmp_="<=", ref="R-T2"),
           T6(8.33, "US", unit="%", cmp_="<=", ref="R-T6a"), T6(8.33, "GB", unit="%", cmp_="<=", ref="R-T6b"),
           T6(6, "AU", unit="%", cmp_="<=", ref="R-T6c")], direction="lower_is_better")
run("G10", [T1(900, ref="R-T1a"), T1(1500, ref="R-T1b")], direction="contested")
def addrow(conn):
    conn.execute("insert into source_value_extractions (ref_id,slug,parameter_id,identity_code,claim_type,"
                 "claimed_value,claimed_unit,figure_role,comparator) values "
                 "('R-T1','s',1,'MOB','numerical','1500','mm','claim','>=')")
run("G11", [T1(900, ref="R-T1")], extra=addrow)
# G12/G13: monotone gradients down and up the ladder (re-specified here; the 2026-10-22 run's script did not persist them)
run("G12", [T1(1000, ref="R-T1"), CO1(1100, ref="R-CO1"), T2(1200, ref="R-T2"), T3C(1300, ref="R-T3C"),
            T4(1400, ref="R-T4"), T5(1500, ref="R-T5"), T6(1600, "US", ref="R-T6a"), T6(1700, "GB", ref="R-T6b"),
            T6(1800, "AU", ref="R-T6c")])
run("G13", [T1(1800, ref="R-T1"), CO1(1700, ref="R-CO1"), T2(1600, ref="R-T2"), T3C(1500, ref="R-T3C"),
            T4(1400, ref="R-T4"), T5(1300, ref="R-T5"), T6(1200, "US", ref="R-T6a"), T6(1100, "GB", ref="R-T6b"),
            T6(1000, "AU", ref="R-T6c")])
