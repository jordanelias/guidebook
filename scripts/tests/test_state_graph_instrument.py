#!/usr/bin/env python3
"""
test_state_graph_instrument.py — the state-graph instrument finds an atom by its quote, not its line number,
and draws the ruled returns (T-134).

Reads: workplan/pipeline-state-graph/build_graph.py (verify_atoms, Tree, the renderer), the atoms it holds,
scripts/audit/graph/extract_contract.py and governance/pipeline-contract.yaml. Every fixture is a temporary
copy of a cited file (TASK-FIXTURE); no atom, line or count is typed here: each is derived from the live files.

    python3 scripts/tests/test_state_graph_instrument.py
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workplan" / "pipeline-state-graph"))
sys.path.insert(0, str(REPO / "scripts" / "audit" / "graph"))
import build_graph as B          # noqa: E402
import extract_contract          # noqa: E402
import sqlite3                   # noqa: E402
from model import GraphStore     # noqa: E402

N = 0
OK = True


def case(cid, name, passed, detail=""):
    global N, OK
    N += 1
    OK = OK and bool(passed)
    print(f"[{'PASS' if passed else 'FAIL'}] {cid} {name}" + ("" if passed else f"  -- {detail}"))


def placed_atom(atoms):
    """The first atom (by id) that cites a line and whose quote is found once, at that line, in its file."""
    for i in sorted(atoms):
        a = atoms[i]
        if not re.search(r":\d+$", a["source"]) or not (REPO / a["source"].rsplit(":", 1)[0]).exists():
            continue
        mv = []
        if not B.verify_atoms({i: a}, moved=mv) and not mv:
            return a
    return None


def fixture(a, shift=0, append_quote=False):
    """TASK-FIXTURE: a temporary tree holding a copy of the atom's source file with `shift` blank lines inserted
    above the cited line and, if asked, the quote's text appended once more at the end of the file."""
    rel, ln = a["source"].rsplit(":", 1)
    td = Path(tempfile.mkdtemp(prefix="guidebook-t134-"))
    (td / rel).parent.mkdir(parents=True, exist_ok=True)
    lines = (REPO / rel).read_text(encoding="utf-8").split("\n")
    k = int(ln) - 1
    lines = lines[:k] + [""] * shift + lines[k:]
    if append_quote:
        lines += ["", a["quote"], ""]
    (td / rel).write_text("\n".join(lines), encoding="utf-8")
    B._text.clear()
    return td


def verdict(a, repo, stats=None):
    mv = []
    bad = B.verify_atoms({a["id"]: a}, repo=repo, moved=mv, stats=stats)
    return bad, mv


def main():
    atoms, _ = B.load_atoms()
    a = placed_atom(atoms)
    case("T134-00", "an atom cited at its line, quote found once, exists to build the fixtures", a is not None)
    if a is None:
        print(f"EXAMINED: {N} assertion(s)"); print("RESULT: FAIL"); return 1
    far = B.LINE_TOLERANCE + 1                   # one line beyond the tolerance: the cited line no longer marks the hit
    tmp = []
    try:
        # T134-01: the quote moved beyond the tolerance passes and prints MOVED; with its text changed it fails.
        td = fixture(a, shift=far); tmp.append(td)
        bad, mv = verdict(a, td)
        case("T134-01a", "a quote found once, moved beyond the tolerance, passes", not bad, bad)
        case("T134-01b", "... and prints a MOVED line naming the cited and the found line",
             len(mv) == 1 and mv[0] == f"MOVED {a['id']}: cited line {a['source'].rsplit(':', 1)[1]}, found at line {int(a['source'].rsplit(':', 1)[1]) + far}", mv)
        st = {}; verdict(a, td, st)
        row = B.atom_rows([a], {a["id"]}, st)[0]
        case("T134-05a", "ATOMS.tsv publishes the line the quote was found on, and quote_checked yes",
             row[5] == f"{a['source'].rsplit(':', 1)[0]}:{int(a['source'].rsplit(':', 1)[1]) + far}" and row[-1] == "yes", row)
        a2 = copy.deepcopy(a); a2["quote"] = a2["quote"] + " zzz-task-fixture-zzz"
        st = {}; bad, mv = verdict(a2, td, st)
        case("T134-01c", "a quote whose text is changed (absent from the file) fails", any("QUOTE NOT FOUND" in x for x in bad), bad)
        row = B.atom_rows([a2], {a2["id"]}, st)[0]
        case("T134-05b", "ATOMS.tsv marks a cited atom whose check failed as not checked-yes", row[-1] != "yes" and row[5] == a2["source"], row)
        td = fixture(a, shift=100 * far); tmp.append(td)
        bad, mv = verdict(a, td)
        case("T134-01d", "a quote found once, moved far (hundreds of lines), still passes with MOVED", not bad and len(mv) == 1, (bad, mv))
        # T134-03: a quote found twice, neither hit near the cited line, fails; one hit near the cited line passes.
        td = fixture(a, shift=far, append_quote=True); tmp.append(td)
        bad, mv = verdict(a, td)
        case("T134-03a", "a quote found twice, neither near the cited line, fails", any("times in" in x and a["id"] in x for x in bad), bad)
        td = fixture(a, shift=0, append_quote=True); tmp.append(td)
        bad, mv = verdict(a, td)
        case("T134-03b", "a quote found twice, one hit at the cited line, passes with no MOVED line", not bad and not mv, (bad, mv))
        td = fixture(a, shift=B.LINE_TOLERANCE, append_quote=True); tmp.append(td)
        bad, mv = verdict(a, td)
        case("T134-03c", "a quote found twice, one hit exactly LINE_TOLERANCE lines below the cited line, passes", not bad, bad)
        td = fixture(a, shift=0, append_quote=True); tmp.append(td)
        a3 = copy.deepcopy(a); rel, ln = a3["source"].rsplit(":", 1); a3["source"] = f"{rel}:{int(ln) + far}"
        bad, mv = verdict(a3, td)
        case("T134-03d", "a quote found twice, one hit beyond the tolerance ABOVE the cited line, fails", any(B.NEAR_FAIL in x for x in bad), bad)
    finally:
        for d in tmp:
            shutil.rmtree(d, ignore_errors=True)
        B._text.clear()

    # T134-02: one ruled_return edge per `re_entry` entry of the committed contract, and the builder draws each.
    doc = yaml.safe_load((REPO / "governance" / "pipeline-contract.yaml").read_text(encoding="utf-8"))
    want = sorted((r["from_stage"], s["id"], r["id"], r["carrier_table"], r["carrier_column"], r.get("carrier_value"))
                  for s in doc["stages"] for r in (s.get("re_entry") or []))
    store = GraphStore(":memory:"); store.init_schema()
    extract_contract.extract(store, REPO)
    got = []
    for src, dst, at in store.conn.execute("select src, dst, attrs from edges where etype=?", (extract_contract.RULED_RETURN,)):
        at = json.loads(at)
        got.append((src.split(":", 1)[1], dst.split(":", 1)[1], at["id"], at["carrier_table"], at["carrier_column"], at["carrier_value"]))
    got.sort()
    case("T134-02a", "the extractor emits one ruled_return edge per re_entry entry, later stage to the stage it re-enters",
         bool(want) and got == want, (want, got))
    T = B.Tree(REPO)
    tup = lambda r: (r["from_stage"], r["to_stage"], r["id"], r["carrier_table"], r["carrier_column"], r["carrier_value"])
    case("T134-02b", "the builder's tree holds the same returns", sorted(map(tup, T.returns)) == want)
    machines = yaml.safe_load(open(B.HERE / "machines.yaml", encoding="utf-8"))
    probes = B.run_probes(T, B.make_probes())
    md = B.render_state_graph(T, atoms, probes, machines, None, "test")
    case("T134-02c", "STATE-GRAPH.md draws each return as a dotted edge",
         all(f"{B.mer_id(f)} -.->|return {i}| {B.mer_id(t)}" in md for f, t, i, *_ in want))
    con = sqlite3.connect(f"file:{REPO / 'data' / 'guidebook.db'}?mode=ro", uri=True)
    def rows(tb, col, val):                      # the live carrier rows, by this test's own query
        q = f'select count(*) from "{tb}" where "{col}" is not null' + ("" if val is None else f' and "{col}" = ?')
        return con.execute(q, () if val is None else (val,)).fetchone()[0]
    sec = md.split("### 2b.", 1)[1].split("\n#", 1)[0] if "### 2b." in md else ""
    case("T134-02d", "section 2b holds one row per return: id, from stage, re-enters, carrier, value, live carrier rows",
         bool(sec) and all(f"| {i} | {f} | {t} | {tb}.{col} | {v or '--'} | {rows(tb, col, v)} |" in sec for f, t, i, tb, col, v in want), sec[:300])
    conf = yaml.safe_load(open(B.HERE / "conflicts.yaml", encoding="utf-8"))
    g = json.loads(json.dumps(B.graph_doc(T, "test", probes, None, {}, None, {}, list(atoms.values()), conf), default=str))
    case("T134-02e", "graph.json carries `returns`, one per re_entry entry, with its live carrier rows",
         sorted(map(tup, g.get("returns", []))) == want and all(r["carrier_rows"] == rows(r["carrier_table"], r["carrier_column"], r["carrier_value"]) for r in g.get("returns", [])))

    # T134-04: on the live tree, no --check failure is a quote found once (a moved quote is a MOVED line, not a failure),
    # and every line-placement failure (the builder's own NEAR_FAIL wording) names more than one hit.
    r = subprocess.run([sys.executable, str(B.HERE / "build_graph.py"), "--check"], cwd=REPO, capture_output=True, text=True)
    near = [l for l in r.stdout.splitlines() if l.startswith("FAIL") and B.NEAR_FAIL in l]
    case("T134-04", "build_graph.py --check fails no quote found once for its line alone",
         re.search(r"\d+ failure\(s\)", r.stdout) and all(int(re.search(r"found (\d+) times", l).group(1)) > 1 for l in near), near[:3])

    print(f"EXAMINED: {N} assertion(s)")
    print("RESULT:", "PASS" if OK else "FAIL")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
