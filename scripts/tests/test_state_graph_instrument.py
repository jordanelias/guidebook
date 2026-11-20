#!/usr/bin/env python3
"""
test_state_graph_instrument.py — the state-graph instrument finds an atom by its quote, not its line number,
and draws and checks the ruled returns (T-134).

Reads: workplan/pipeline-state-graph/build_graph.py (verify_atoms, atom_rows, Tree, the renderer, graph_doc,
returns_problems, main), its atoms and yaml files, scripts/audit/graph/extract_contract.py and
governance/pipeline-contract.yaml. Every fixture is a temporary copy (TASK-FIXTURE); no atom, line or count is typed
here: each is derived from the live files. Every case asserts that its subject is not empty, and the fixture cases
carry a negative control (a deleted or changed quote fails; drift MOVES and does not fail).

    python3 scripts/tests/test_state_graph_instrument.py
"""
import contextlib
import copy
import io
import json
import re
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workplan" / "pipeline-state-graph"))
sys.path.insert(0, str(REPO / "scripts" / "audit" / "graph"))
import build_graph as B          # noqa: E402
import extract_contract          # noqa: E402
from model import GraphStore     # noqa: E402

N = 0
OK = True
TMP = []


def case(cid, name, passed, detail=""):
    global N, OK
    N += 1
    OK = OK and bool(passed)
    print(f"[{'PASS' if passed else 'FAIL'}] {cid} {name}" + ("" if passed else f"  -- {str(detail)[:300]}"))


def _nt(text):                   # this test's own oracle for "how often is the quote in the file" (blockquote marks off)
    return B.norm("\n".join(re.sub(r"^\s*>\s?", "", l) for l in text.split("\n")))


def occurrences(a, root):
    q, t = _nt(a["quote"]), _nt((Path(root) / a["source"].rsplit(":", 1)[0]).read_text(encoding="utf-8"))
    n, p = 0, t.find(q)
    while p >= 0:
        n += 1; p = t.find(q, p + 1)
    return n


def exactly_placed(atoms, ids):
    """The first atom (by id) whose quote is found once and exactly at its cited line (derived, not typed)."""
    for i in sorted(ids):
        a = atoms[i]
        if not re.search(r":\d+$", a["source"]) or not (REPO / a["source"].rsplit(":", 1)[0]).exists():
            continue
        st = {}
        if not B.verify_atoms({i: a}, stats=st) and st.get("found", {}).get(i) == a["source"]:
            return a
    return None


def fixture(a, shift=0, appends=0):
    """TASK-FIXTURE: a temporary tree holding a copy of the atom's source file with `shift` blank lines inserted above
    the cited line and the quote appended `appends` more times at the end. Returns (root, [lines of each planted hit])."""
    rel, ln = a["source"].rsplit(":", 1)
    td = Path(tempfile.mkdtemp(prefix="guidebook-t134-")); TMP.append(td)
    (td / rel).parent.mkdir(parents=True, exist_ok=True)
    lines = (REPO / rel).read_text(encoding="utf-8").split("\n")
    k = int(ln) - 1
    lines = lines[:k] + [""] * shift + lines[k:]
    hits = [int(ln) + shift]
    for _ in range(appends):
        lines += ["", a["quote"], ""]; hits.append(len(lines) - 1)
    (td / rel).write_text("\n".join(lines), encoding="utf-8")
    B._text.clear()
    return td, hits


def verdict(a, repo, stats=None):
    mv = []
    return B.verify_atoms({a["id"]: a}, repo=repo, moved=mv, stats=stats), mv


def cited_at(a, line):
    b = copy.deepcopy(a); b["source"] = f"{a['source'].rsplit(':', 1)[0]}:{line}"; return b


def quote_cases(atoms):
    a = exactly_placed(atoms, atoms)
    case("T134-00", "an atom whose quote is found once, exactly at its cited line, exists (the fixtures' subject)",
         a is not None and occurrences(a, REPO) == 1)
    if a is None:
        return
    rel, ln = a["source"].rsplit(":", 1); ln = int(ln)
    far, tol = B.LINE_TOLERANCE + 1, B.LINE_TOLERANCE

    td, h = fixture(a, shift=far)
    sub = occurrences(a, td) == 1
    st = {}; bad, mv = verdict(a, td, st)
    case("T134-01a", "a quote found once, moved beyond the tolerance, passes", sub and not bad, bad)
    case("T134-01b", "... and prints MOVED naming the cited and the found line",
         sub and mv == [f"MOVED {a['id']}: cited line {ln}, found at line {h[0]}"], mv)
    row = B.atom_rows([a], {a["id"]}, st)[0]
    case("T134-05a", "ATOMS.tsv publishes the line the quote was found on, quote_checked yes",
         sub and row[5] == f"{rel}:{h[0]}" and row[-1] == "yes", row)
    case("T134-05d", "ATOMS.tsv publishes an uncited atom as quote_checked no", sub and B.atom_rows([a], set(), st)[0][-1] == "no")
    a2 = copy.deepcopy(a); a2["quote"] += " zzz-task-fixture-zzz"
    st = {}; bad, mv = verdict(a2, td, st)
    case("T134-01c", "a quote whose text is changed fails (negative control)",
         occurrences(a2, td) == 0 and any(x.startswith(f"{a['id']}: QUOTE NOT FOUND") for x in bad) and not mv, bad)
    row = B.atom_rows([a2], {a2["id"]}, st)[0]
    case("T134-05b", "ATOMS.tsv publishes a cited atom that failed as `failed`, at its cited line", row[-1] == "failed" and row[5] == a2["source"], row)
    a3 = copy.deepcopy(a); a3["quote"] = a3["quote"].upper()
    bad, mv = verdict(a3, td)
    case("T134-01e", "a quote whose letters differ in case only fails (matching is case-sensitive)",
         a3["quote"] != a["quote"] and occurrences(a3, td) == 0 and any("QUOTE NOT FOUND" in x for x in bad), bad)

    td, h = fixture(a, shift=100 * far)
    bad, mv = verdict(a, td)
    case("T134-01d", "a quote found once, moved hundreds of lines, passes with MOVED", occurrences(a, td) == 1 and not bad and len(mv) == 1, (bad, mv))
    td, h = fixture(a, shift=tol)
    bad, mv = verdict(a, td)
    case("T134-01f", "a quote found once within the tolerance passes with no MOVED line", occurrences(a, td) == 1 and not bad and not mv, (bad, mv))

    td, h = fixture(a, shift=far, appends=1)
    sub = occurrences(a, td) == 2
    bad, mv = verdict(a, td)
    case("T134-03a", "a quote found twice, neither near the cited line, fails", sub and any(B.NEAR_FAIL in x and a["id"] in x for x in bad), bad)
    st = {}; bad, mv = verdict(cited_at(a, h[1]), td, st)
    case("T134-03e", "a quote found twice, the SECOND hit at the cited line, passes", sub and not bad and not mv, (bad, mv))
    row = B.atom_rows([cited_at(a, h[1])], {a["id"]}, st)[0]
    case("T134-05c", "ATOMS.tsv keeps the cited line of an atom whose quote is found more than once", sub and row[5] == f"{rel}:{h[1]}", row)
    td, h = fixture(a, shift=far, appends=2)
    bad, mv = verdict(a, td)
    case("T134-03f", "a quote found three times, none near the cited line, fails",
         occurrences(a, td) == 3 and any("found 3 times" in x and B.NEAR_FAIL in x for x in bad), bad)
    td, h = fixture(a, shift=0, appends=1)
    sub = occurrences(a, td) == 2
    bad, mv = verdict(a, td)
    case("T134-03b", "a quote found twice, one hit at the cited line, passes with no MOVED line", sub and not bad and not mv, (bad, mv))
    bad, mv = verdict(cited_at(a, ln + far), td)
    case("T134-03d", "a quote found twice, the near-side hit beyond the tolerance ABOVE the cited line, fails", sub and any(B.NEAR_FAIL in x for x in bad), bad)
    td, h = fixture(a, shift=tol, appends=1)
    bad, mv = verdict(a, td)
    case("T134-03c", "a quote found twice, one hit exactly LINE_TOLERANCE lines below the cited line, passes", occurrences(a, td) == 2 and not bad, bad)


def return_cases(atoms):
    doc = yaml.safe_load((REPO / "governance" / "pipeline-contract.yaml").read_text(encoding="utf-8"))
    want = sorted((r["from_stage"], s["id"], r["id"], r["carrier_table"], r["carrier_column"], r.get("carrier_value"))
                  for s in doc["stages"] for r in (s.get("re_entry") or []))
    store = GraphStore(":memory:"); store.init_schema()
    extract_contract.extract(store, REPO)
    got = []
    for src, dst, at in store.conn.execute("select src, dst, attrs from edges where etype=?", (extract_contract.RULED_RETURN,)):
        at = json.loads(at)
        got.append((src.split(":", 1)[1], dst.split(":", 1)[1], at["id"], at["carrier_table"], at["carrier_column"], at["carrier_value"]))
    case("T134-02a", "the extractor emits one ruled_return edge per re_entry entry, later stage to the stage it re-enters",
         bool(want) and sorted(got) == want, (want, got))
    tup = lambda r: (r["from_stage"], r["to_stage"], r["id"], r["carrier_table"], r["carrier_column"], r["carrier_value"])
    T = B.Tree(REPO)
    case("T134-02b", "the builder's tree holds the same returns", bool(want) and sorted(map(tup, T.returns)) == want)
    probes = B.run_probes(T, B.make_probes())
    md = B.render_state_graph(T, atoms, probes, yaml.safe_load(open(B.HERE / "machines.yaml", encoding="utf-8")), None, "test")
    case("T134-02c", "STATE-GRAPH.md draws each return as a dotted edge",
         bool(want) and all(f"{B.mer_id(f)} -.->|return {i}| {B.mer_id(t)}" in md for f, t, i, *_ in want))
    con = sqlite3.connect(f"file:{REPO / 'data' / 'guidebook.db'}?mode=ro", uri=True)
    def rows(tb, col, val):                      # the live carrier rows, by this test's own query
        q = f'select count(*) from "{tb}" where "{col}" is not null' + ("" if val is None else f' and "{col}" = ?')
        return con.execute(q, () if val is None else (val,)).fetchone()[0]
    sec = md.split("### 2b.", 1)[1].split("\n#", 1)[0] if "### 2b." in md else ""
    case("T134-02d", "section 2b: one row per return (id, from stage, re-enters, carrier, value, live carrier rows)",
         bool(want) and all(f"| {i} | {f} | {t} | {tb}.{col} | {v or '--'} | {rows(tb, col, v)} |" in sec for f, t, i, tb, col, v in want), sec[:300])
    conf = yaml.safe_load(open(B.HERE / "conflicts.yaml", encoding="utf-8"))
    g = json.loads(json.dumps(B.graph_doc(T, "test", probes, None, {}, None, {}, list(atoms.values()), conf), default=str))
    case("T134-02e", "graph.json carries `returns`, one per re_entry entry, with its live carrier rows",
         bool(want) and sorted(map(tup, g.get("returns", []))) == want
         and all(r["carrier_rows"] == rows(r["carrier_table"], r["carrier_column"], r["carrier_value"]) for r in g["returns"]))
    case("T134-02f", "a carrier column the schema does not hold is reported as missing, not as 0 rows",
         bool(T.returns) and B.carrier_rows(T, dict(T.returns[0], carrier_column="zzz_task_fixture")) == "no such column")
    # T134-02g: --check's ruled-return check (returns_problems) on contract copies held in memory; graph.json is a temp file
    td = Path(tempfile.mkdtemp(prefix="guidebook-t134-")); TMP.append(td)
    gp = td / "graph.json"; gp.write_text(json.dumps(g, default=str), encoding="utf-8")
    def variant(mut):
        T2 = copy.copy(T); T2.contract = copy.deepcopy(T.contract); mut(T2.contract)
        T2.returns = list(extract_contract.returns(T2.contract)); return B.returns_problems(T2, gp)
    holder = next(s for s in T.contract["stages"] if s.get("re_entry"))
    def drop(c): next(s for s in c["stages"] if s["id"] == holder["id"])["re_entry"].pop(0)
    def rename(c): next(s for s in c["stages"] if s["id"] == holder["id"])["re_entry"][0]["carrier_column"] = "zzz_task_fixture"
    case("T134-02g", "the live returns raise no problem against a graph.json built from them (control)", bool(want) and B.returns_problems(T, gp) == [])
    case("T134-02h", "a ruled return deleted from the contract makes --check fail until graph.json is regenerated",
         any("graph.json `returns` differ" in x for x in variant(drop)))
    case("T134-02i", "a carrier column renamed to one the schema lacks makes --check fail",
         any("has no column 'zzz_task_fixture'" in x for x in variant(rename)))
    case("T134-02j", "a missing graph.json makes --check fail", any("graph.json" in x for x in B.returns_problems(T, td / "absent.json")))


def check_cases(atoms):
    """T134-04: build_graph.py --check itself (main), run in-process on a copy of the instrument folder."""
    probes = B.run_probes(B.Tree(REPO), B.make_probes())
    load = lambda f: yaml.safe_load(open(B.HERE / f, encoding="utf-8"))
    cited = B.cited_atom_ids(probes, load("conflicts.yaml"), load("machines.yaml"), load("capabilities.yaml")) & set(atoms)
    a = exactly_placed(atoms, cited)
    b = exactly_placed(atoms, cited - {a["id"]}) if a else None
    case("T134-04a", "two cited atoms exactly at their cited line exist (the --check fixtures' subject)", a is not None and b is not None)
    if not (a and b):
        return
    here = B.HERE
    def run(edit=None, drop_return=False):
        td = Path(tempfile.mkdtemp(prefix="guidebook-t134-")); TMP.append(td)
        for f in ("conflicts.yaml", "machines.yaml", "capabilities.yaml", "graph.json"): shutil.copy(here / f, td / f)
        shutil.copytree(here / "atoms", td / "atoms")
        if drop_return:                          # the published graph.json lacks one return the contract rules
            g = json.loads((td / "graph.json").read_text(encoding="utf-8")); g["returns"] = g["returns"][1:]
            (td / "graph.json").write_text(json.dumps(g), encoding="utf-8")
        if edit:
            for f in (td / "atoms").glob("atoms-*.jsonl"):
                ls = f.read_text(encoding="utf-8").split("\n")
                f.write_text("\n".join(json.dumps(edit(json.loads(l)), ensure_ascii=False) if l.strip() else l for l in ls), encoding="utf-8")
        out, argv = io.StringIO(), sys.argv
        B.HERE, sys.argv = td, ["build_graph.py", "--check"]
        try:
            with contextlib.redirect_stdout(out):
                try: B.main(); rc = 0
                except SystemExit as e: rc = e.code
        finally:
            B.HERE, sys.argv = here, argv; B._text.clear()
        return rc, out.getvalue()
    rc, out = run()
    m = re.search(r"EXAMINED:\s+(\d+)\s+atoms whose quote was read", out); nf = re.search(r"(\d+) failure\(s\)", out)
    case("T134-04b", "--check reads the quote of every cited atom (EXAMINED equals the cited atoms, and is not 0)",
         bool(m) and int(m.group(1)) == len(cited) > 0, (m and m.group(1), len(cited)))
    case("T134-04c", "--check exits 1 exactly when it prints a failure", bool(nf) and rc == (1 if int(nf.group(1)) else 0), (rc, nf and nf.group(0)))
    r = re.search(r"EXAMINED:\s+(\d+)\s+ruled returns", out)
    case("T134-04f", "--check examines every ruled return, and none fails on the live tree (control)",
         bool(r) and int(r.group(1)) == len(B.Tree(REPO).returns) > 0 and "graph.json `returns` differ" not in out, r and r.group(0))
    rc, out = run(drop_return=True)
    case("T134-04g", "--check fails and exits 1 when the published graph.json draws a return fewer than the contract rules",
         rc == 1 and any(l.startswith("FAIL") and "graph.json `returns` differ" in l for l in out.splitlines()), out[-300:])
    far = B.LINE_TOLERANCE + 1
    def seed(x):
        if x["id"] == a["id"]: x = dict(x, quote=x["quote"] + " zzz-task-fixture-zzz")
        if x["id"] == b["id"]: x = cited_at(x, int(x["source"].rsplit(":", 1)[1]) + far)
        return x
    rc, out = run(seed)
    case("T134-04d", "a cited atom whose quote is no longer in its file fails --check and exits 1",
         rc == 1 and any(l.startswith("FAIL") and f"{a['id']}: QUOTE NOT FOUND" in l for l in out.splitlines()), out[-300:])
    case("T134-04e", "a cited atom whose quote drifted prints MOVED and does not fail",
         any(l.startswith(f"MOVED {b['id']}:") for l in out.splitlines()) and not any(l.startswith("FAIL") and f" {b['id']}:" in l for l in out.splitlines()))


def selection_case():
    """T134-06: a diff to the builder, the verifier, the extractor or the contract selects this test (run_checks' own classify/select)."""
    sys.path.insert(0, str(REPO / "scripts"))
    import run_checks
    reg = yaml.safe_load((REPO / "governance" / "check-registry.yaml").read_text(encoding="utf-8"))
    me = Path(__file__).name
    subj = ["workplan/pipeline-state-graph/build_graph.py", "workplan/pipeline-state-graph/verify_atoms.py",
            "scripts/audit/graph/extract_contract.py", "governance/pipeline-contract.yaml"]
    def picked(path):
        kinds, _ = run_checks.classify([path], reg)
        return any(ok and me in " ".join(c["cmd"]) for c, ok, _ in run_checks.select(reg, kinds))
    case("T134-06", "a diff to the builder, the verifier, the extractor or the contract selects this test",
         all(map(picked, subj)), [p for p in subj if not picked(p)])


def main():
    atoms, _ = B.load_atoms()
    try:
        quote_cases(atoms)
        return_cases(atoms)
        check_cases(atoms)
        selection_case()
    finally:
        for d in TMP:
            shutil.rmtree(d, ignore_errors=True)
        B._text.clear()
    print(f"EXAMINED: {N} assertion(s)")
    print("RESULT:", "PASS" if OK else "FAIL")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
