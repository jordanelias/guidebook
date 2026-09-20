#!/usr/bin/env python3
"""Data atlas: every row in the database, which batch wrote it, what tool can write it,
and how far you can walk from any row to any other.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md §8's test).

Four dashboards already stand over this database and not one of them shows the rows.
`spec-curation-vetting-surface.html` is per-topic, `pipeline-completeness-dashboard.html`
grades how much is done, `evidentiary-audit-dashboard.html` grades what is there, and
`schema-walkability.html` walks the SCHEMA -- tables and views, not rows. So the question
a session actually asks before planning a write -- "what is already in here, who put it
there, and what does it already point at" -- had no surface at all, and the answer was
reconstructed by hand from sqlite3 one-liners every time. That reconstruction is where
rule 7a's hand-typed counts come from.

It also derives the one fact rule 8 says goes blind: WHICH TOOL WRITES EACH TABLE.
`dbcore.WRITABLE_TABLES` was a curated list of exactly that and it went blind eight
times, capturing a `gap_mining` row written through the sanctioned CLI as nothing. This
module never asks anyone; it parses the scripts tree and reports the writers it finds,
so a table no tool can reach shows up as an empty writer column rather than as silence.
A table whose only writer is a migration is a different fact from a table with a CLI
subcommand, and both are different from a table nothing writes at all.

EVERYTHING IS DERIVED (rule 7a: a number is the command that computes it, never its
result). No table list, no row count, no edge list, no writer list and no session list is
written down in this file. Tables and views come from `sqlite_master`, edges from
`PRAGMA foreign_key_list`, vocabularies from each column's own CHECK, batches from the
`created_by_session` columns the schema actually carries, stage ids from
`governance/pipeline-contract.yaml` and table->stage from `governance/stage-map.yaml`
(read, never copied -- and every live table missing from that map is REPORTED on the
page rather than quietly defaulted, which is the falsifier its own header asks for).

Read-only on the DB. Writes one self-contained HTML file.

    python3 tools/data_atlas.py                  # write tools/data-atlas.html
    python3 tools/data_atlas.py --check          # exit 1 if the committed copy is stale
    python3 tools/data_atlas.py --out PATH       # write elsewhere
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = pathlib.Path(os.environ.get("GUIDEBOOK_DB_PATH", ROOT / "data/guidebook.db"))
OUT = ROOT / "tools/data-atlas.html"

# SQL write forms. Matched against every string constant in the scripts tree, then
# intersected with the LIVE table list -- so prose that happens to read like SQL
# ("insert into this") cannot invent a table, and a real table cannot be missed for
# being absent from any list here.
WRITE_RE = re.compile(
    r'\b(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|REPLACE\s+INTO)\s+["\'`]?([A-Za-z_][A-Za-z0-9_]*)'
    r'|\bUPDATE\s+["\'`]?([A-Za-z_][A-Za-z0-9_]*)["\'`]?\s+SET'
    r'|\bDELETE\s+FROM\s+["\'`]?([A-Za-z_][A-Za-z0-9_]*)',
    re.I,
)


# ---------------------------------------------------------------- schema + rows

def connect():
    if not DB.exists():
        sys.exit(f"no database at {DB}")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def check_vocab(sql: str, col: str):
    """The column's own CHECK vocabulary, from the CREATE TABLE text (rule 8:
    a vocabulary comes from the schema, never from a list beside it)."""
    if not sql:
        return None
    pat = re.compile(
        r'\b' + re.escape(col) + r'\b[^,]*?CHECK\s*\(\s*' + re.escape(col)
        + r'\s+IN\s*\(([^)]*)\)', re.I | re.S)
    m = pat.search(sql)
    if not m:
        pat2 = re.compile(
            r'CHECK\s*\(\s*' + re.escape(col) + r'\s+IN\s*\(([^)]*)\)', re.I | re.S)
        m = pat2.search(sql)
    if not m:
        return None
    return [v.strip().strip("'\"") for v in m.group(1).split(",") if v.strip()]


# ---------------------------------------------------------------- writers (AST)

def _sql_writes(node):
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            for m in WRITE_RE.finditer(n.value):
                ins, upd, dele = m.group(1), m.group(2), m.group(3)
                if ins:
                    out.add((ins, "INSERT"))
                elif upd:
                    out.add((upd, "UPDATE"))
                elif dele:
                    out.add((dele, "DELETE"))
    return out


def _called(node):
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.add(f.id)
            elif isinstance(f, ast.Attribute):
                out.add(f.attr)
    return out


def is_fixture(path, fname):
    """A write into a throwaway test schema, not into the canonical database.

    `selftest` and `test_*` functions build `:memory:` fixtures; counting them as
    writers tells a reader a table has a way in when it has none -- which is the
    WRITABLE_TABLES failure with the sign flipped. Verified by reading the six
    modules that tripped it: every one opens its own connection.
    """
    rel = str(path)
    return (fname == "selftest" or fname.startswith("test_")
            or "/tests/" in rel or pathlib.Path(rel).name.startswith("test_"))


def derive_writers(live_tables):
    """Which tool writes which table. Parsed, never listed.

    Four kinds, and the difference matters to a reader planning a write:
      cli       -- a `db.py <subcommand>` an operator can run
      script    -- a module that writes without a subcommand of its own
      migration -- the only writer is a committed SQL migration (rule 3's real path)
      fixture   -- a selftest building its own schema; NOT a way into the real database
    """
    modules = {}
    for p in sorted(ROOT.glob("scripts/**/*.py")) + sorted(ROOT.glob("tools/**/*.py")):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        funcs = {}
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs[n.name] = (_sql_writes(n), _called(n))
        modules[p] = funcs

    index = {}
    for p, funcs in modules.items():
        for name in funcs:
            index.setdefault(name, []).append(p)

    def resolve(fname, seen=None):
        if seen is None:
            seen = set()
        if fname in seen:
            return set()
        seen.add(fname)
        out = set()
        for p in index.get(fname, []):
            direct, calls = modules[p][fname]
            out |= direct
            for c in calls:
                out |= resolve(c, seen)
        return out

    writers = {t: [] for t in live_tables}

    # db.py subcommands: split main()'s if/elif chain on `args.command == "..."`.
    dbpy = ROOT / "scripts/db.py"
    if dbpy.exists():
        tree = ast.parse(dbpy.read_text(encoding="utf-8", errors="replace"))
        main = next((n for n in ast.walk(tree)
                     if isinstance(n, ast.FunctionDef) and n.name == "main"), None)
        cmd_writes = {}

        def walk_if(node):
            if not isinstance(node, ast.If):
                return
            names = []
            for c in ast.walk(node.test):
                if (isinstance(c, ast.Compare) and isinstance(c.left, ast.Attribute)
                        and c.left.attr == "command"):
                    for comp in c.comparators:
                        if isinstance(comp, ast.Constant):
                            names.append(comp.value)
                        elif isinstance(comp, (ast.List, ast.Tuple)):
                            names += [e.value for e in comp.elts
                                      if isinstance(e, ast.Constant)]
            if names:
                body = ast.Module(body=node.body, type_ignores=[])
                w = _sql_writes(body)
                for c in _called(body):
                    w |= resolve(c)
                for nm in names:
                    cmd_writes.setdefault(nm, set()).update(w)
            for o in node.orelse:
                walk_if(o)

        if main:
            for n in main.body:
                walk_if(n)
        for cmd, ws in cmd_writes.items():
            for tbl, op in ws:
                if tbl in writers:
                    writers[tbl].append({"tool": f"db.py {cmd}", "op": op, "kind": "cli"})

    # Scripts that write without a subcommand of their own.
    for p, funcs in modules.items():
        rel = str(p.relative_to(ROOT))
        if rel == "scripts/db.py":
            continue
        agg = {}
        for fname, (direct, _) in funcs.items():
            kind = "fixture" if is_fixture(rel, fname) else "script"
            for tbl, op in direct:
                if tbl in writers:
                    agg.setdefault((tbl, op, kind), set()).add(fname)
        for (tbl, op, kind), fns in sorted(agg.items()):
            writers[tbl].append({"tool": rel, "op": op, "kind": kind,
                                 "fns": sorted(fns)[:4]})

    # Migrations. Rule 3's real landing path: nothing reaches the committed blob
    # except through one of these files.
    for p in sorted(ROOT.glob("scripts/migrations/*.sql")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        seen = set()
        for m in WRITE_RE.finditer(txt):
            tbl = m.group(1) or m.group(2) or m.group(3)
            if tbl in writers and tbl not in seen:
                seen.add(tbl)
                writers[tbl].append({"tool": p.name, "op": "INSERT",
                                     "kind": "migration"})
    for t in writers:
        writers[t].sort(key=lambda w: (w["kind"], w["tool"], w["op"]))
    return writers


# ---------------------------------------------------------------- governance reads

def read_stage_contract():
    """Stage ids from the contract; table->stage from the stage map. Both READ, and the
    map's coverage of the live schema is checked rather than trusted (its own header
    asks for exactly this falsifier)."""
    stages, table_stage, judged = [], {}, {}
    cpath = ROOT / "governance/pipeline-contract.yaml"
    if cpath.exists():
        instages = False
        for line in cpath.read_text(encoding="utf-8").splitlines():
            if re.match(r"^stages:\s*$", line):
                instages = True
                continue
            if instages:
                if line and not line[0].isspace() and not line.startswith("-"):
                    instages = False
                    continue
                m = re.match(r"^- id:\s*(\S+)\s*$", line)
                if m:
                    stages.append(m.group(1))
    spath = ROOT / "governance/stage-map.yaml"
    if spath.exists():
        intab = False
        for line in spath.read_text(encoding="utf-8").splitlines():
            if re.match(r"^tables:\s*$", line):
                intab = True
                continue
            if intab:
                m = re.match(r"^  ([A-Za-z_][A-Za-z0-9_]*):\s*(\S+)\s*$", line)
                if m:
                    table_stage[m.group(1)] = m.group(2)
                elif line and not line.startswith(" "):
                    intab = False
            m = re.match(r"^judged_(by|on):\s*'?([^'\n]+)'?\s*$", line)
            if m:
                judged[m.group(1)] = m.group(2).strip()
    return stages, table_stage, judged


# ---------------------------------------------------------------- build

def build():
    con = connect()
    cur = con.cursor()

    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    views = [(r[0], r[1]) for r in cur.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' ORDER BY name")]
    tsql = {r[0]: (r[1] or "") for r in cur.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table'")}

    counts = {t: cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}
    empty = {t for t in tables if counts[t] == 0}

    stage_ids, table_stage, judged = read_stage_contract()
    stage_order = stage_ids + ["infrastructure", "internal", "unassigned"]

    writers = derive_writers(set(tables))

    # ---- columns, unwritability, batches
    meta_tables, sessions_total = [], {}
    for t in tables:
        cols = []
        pk = []
        info = list(cur.execute(f'PRAGMA table_info("{t}")'))
        fkcols = {}
        for fk in cur.execute(f'PRAGMA foreign_key_list("{t}")'):
            fkcols[fk[3]] = (fk[2], fk[4])
        for c in info:
            cid, name, ctype, notnull, dflt, ispk = c
            if ispk:
                pk.append(name)
            entry = {"n": name, "t": ctype or "", "nn": bool(notnull), "pk": bool(ispk)}
            v = check_vocab(tsql.get(t, ""), name)
            if v:
                entry["vocab"] = v
            if name in fkcols:
                entry["fk"] = list(fkcols[name])
            cols.append(entry)

        # A NOT NULL foreign key into an EMPTIED table makes the table unwritable:
        # the refusal comes at INSERT, never at migration time, so every gate stays
        # green over a table that cannot accept a row (CLAUDE.md §4).
        unwritable = [
            {"col": c["n"], "into": c["fk"][0]}
            for c in cols
            if c.get("fk") and c["nn"] and c["fk"][0] in empty
        ]

        sess = {}
        colnames = {c["n"] for c in cols}
        if "created_by_session" in colnames:
            for s, n in cur.execute(
                    f'SELECT created_by_session, COUNT(*) FROM "{t}" GROUP BY 1'):
                key = s if s is not None else "— unattributed"
                sess[key] = n
                sessions_total[key] = sessions_total.get(key, 0) + n

        internal = t.startswith("sqlite_")
        meta_tables.append({
            "name": t,
            "stage": table_stage.get(t, "internal" if internal else "unassigned"),
            "mapped": t in table_stage or internal,
            "internal": internal,
            "rows": counts[t],
            "cols": cols,
            "pk": pk,
            "unwritable": unwritable,
            "writers": writers.get(t, []),
            "sessions": sess,
        })

    # ---- edges, with real traffic measured rather than assumed
    edges = []
    for t in tables:
        # Materialized deliberately: re-executing on `cur` inside this loop resets
        # the cursor mid-iteration and silently drops edges. Measured at 53 of 108.
        for fk in list(cur.execute(f'PRAGMA foreign_key_list("{t}")')):
            _, _, parent, fcol, pcol, *_ = fk
            if parent not in counts:
                continue
            if pcol is None:
                ppk = [c[1] for c in cur.execute(f'PRAGMA table_info("{parent}")') if c[5]]
                pcol = ppk[0] if ppk else None
            if pcol is None:
                continue
            nn = cur.execute(
                f'SELECT COUNT(*) FROM "{t}" WHERE "{fcol}" IS NOT NULL').fetchone()[0]
            res = 0
            if nn:
                res = cur.execute(
                    f'SELECT COUNT(*) FROM "{t}" c JOIN "{parent}" p '
                    f'ON c."{fcol}" = p."{pcol}"').fetchone()[0]
            edges.append({
                "src": t, "col": fcol, "dst": parent, "dcol": pcol,
                "child": counts[t], "nn": nn, "res": res, "orph": nn - res,
                "dead": counts[parent] == 0,
                "sstage": table_stage.get(t, "unassigned"),
                "dstage": table_stage.get(parent, "unassigned"),
            })

    # ---- views: which stages each one spans. A cross-stage view IS the pointer
    # (CLAUDE.md §3), so what it spans is derived from the tables its SQL names.
    vinfo = []
    for vname, vsql in views:
        named = sorted({t for t in tables
                        if re.search(r'\b' + re.escape(t) + r'\b', vsql or "")})
        sp = sorted({table_stage.get(t, "unassigned") for t in named} - {"base"})
        try:
            vrows = cur.execute(f'SELECT COUNT(*) FROM "{vname}"').fetchone()[0]
        except sqlite3.Error:
            vrows = None
        vinfo.append({"name": vname, "tables": named, "stages": sp,
                      "crosses": len(sp) > 1, "rows": vrows})

    # ---- rows, column-array form (repeating 97 keys per evidence_sources row is
    # the difference between a page that ships and one that does not)
    data = {}
    for t in tables:
        names = [c["n"] for c in next(m for m in meta_tables if m["name"] == t)["cols"]]
        rows = []
        for r in cur.execute(f'SELECT * FROM "{t}"'):
            rows.append([r[n] for n in names])
        data[t] = rows

    dbbytes = DB.read_bytes()
    asof = None
    for t in tables:
        cn = {c[1] for c in cur.execute(f'PRAGMA table_info("{t}")')}
        for col in ("updated_at", "created_at"):
            if col in cn:
                v = cur.execute(f'SELECT MAX("{col}") FROM "{t}"').fetchone()[0]
                if v and (asof is None or str(v) > asof):
                    asof = str(v)

    payload = {
        "meta": {
            "db": str(DB.relative_to(ROOT)) if DB.is_relative_to(ROOT) else str(DB),
            "sha256": hashlib.sha256(dbbytes).hexdigest()[:12],
            "bytes": len(dbbytes),
            "user_version": cur.execute("PRAGMA user_version").fetchone()[0],
            "asof": asof,
            "tables": len(tables),
            "views": len(views),
            "rows": sum(counts.values()),
            "edges": len(edges),
            "stage_order": stage_order,
            "judged_by": judged.get("by", ""),
            "judged_on": judged.get("on", ""),
        },
        "tables": meta_tables,
        "edges": edges,
        "views": vinfo,
        "sessions": sorted(
            ({"id": k, "rows": v} for k, v in sessions_total.items()),
            key=lambda d: (-d["rows"], d["id"])),
        "data": data,
    }
    con.close()
    return payload


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed page is stale")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--json", action="store_true", help="emit the payload only")
    args = ap.parse_args()

    payload = build()
    if args.json:
        print(json.dumps(payload, default=str))
        return

    tpl = (ROOT / "tools/data_atlas_template.html").read_text(encoding="utf-8")
    blob = json.dumps(payload, default=str, separators=(",", ":"), sort_keys=False)
    html = tpl.replace("/*__ATLAS_PAYLOAD__*/null", blob)

    out = pathlib.Path(args.out)
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != html:
            print(f"STALE: {out} does not match the live database", file=sys.stderr)
            sys.exit(1)
        print(f"current: {out}")
        return
    out.write_text(html, encoding="utf-8")
    m = payload["meta"]
    print(f"wrote {out}  ({out.stat().st_size/1e6:.2f} MB)")
    print(f"  {m['tables']} tables, {m['views']} views, {m['rows']} rows, "
          f"{m['edges']} edges, {len(payload['sessions'])} batches, schema v{m['user_version']}")


if __name__ == "__main__":
    main()
