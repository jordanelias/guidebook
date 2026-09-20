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
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))
import dbcore                          # noqa: E402
import pipeline_walk as pw             # noqa: E402

# THE SIBLINGS ARE THE HOME FOR ALL OF THIS, and re-deriving it cost measured errors --
# the same ones `tools/schema_walkability.py:50-64` already records paying for. The first
# version of this module defined its own connect_ro, CHECK-vocabulary parser, YAML stage
# reader, §4 unwritable probe and as-of stamp. Four of the five were wrong:
#   * the vocabulary parser missed every `CHECK (c IS NULL OR c IN (...))` column -- 28 of
#     them live, including both vocabularies migrations 091/092 had just declared -- and
#     returned a comment fragment as a value for `gap_mining.outcome`, because it did not
#     strip SQL line comments. `dbcore.check_values()` handles both forms and a third one
#     migration 078 introduced, and its docstring says outright that a new form "would need
#     adding here, not working around at the call site" -- which a private second parser
#     silently defeats;
#   * the UNWRITABLE probe used the flat form and reported 19 columns where
#     `pw.unwritable()` reports 6 empty-parent ROOTS, including the three that module's
#     docstring names as writable anyway (one db.py call inserts parent and child in the
#     same transaction). The page rendered that beside prose saying the table cannot accept
#     a row: CLAUDE.md 5(b), prose contradicting the database, on a page whose whole claim
#     is that nothing on it is maintained by hand;
#   * `as_of` compared raw timestamp strings, so a midnight `...T00:00:00Z` stamp sorted
#     above a same-day `... 23:59` one -- `pw._norm_stamp` exists for exactly the three
#     shapes this corpus stores;
#   * the view scan matched table names in raw view SQL, comments included, which is the
#     false positive `schema_walkability.py:110` already fixed with the stripper.
# The YAML reader was merely duplicated rather than wrong, and is gone with the rest.
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


def _judged_by(path: pathlib.Path) -> dict:
    """Who judged the stage map, and when.

    `pw.load_stage_map` returns the assignments and the disputed block, not the
    attribution -- and rule 8 says a judged fact must name its judge, so the page
    carries it. Read with the same parser, never a second hand-rolled one.
    """
    import yaml
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    return {"by": str(doc.get("judged_by", "")), "on": str(doc.get("judged_on", ""))}


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

    # RESOLVE WITHIN db.py ONLY. The first version indexed every function name in
    # scripts/ and tools/ and unioned the writes of every module defining that name.
    # Names collide, so the walk escaped db.py: `add-icf-code` resolved
    # insert_icf_code -> stamp_for -> audit -> rebuild -> run -> `fresh`, a fixture in
    # scripts/tests/test_validate_evidence_state_2_4.py, and 33 of 47 subcommands were
    # reported as CLI writers of `gaps`. The column this module exists for was unusable
    # on the busiest tables. A bare name is not an import graph; db.py's own functions
    # are, so the dispatch resolves against them and nothing else.
    dbpy_funcs = modules.get(ROOT / "scripts/db.py", {})

    def resolve(fname, seen=None):
        if seen is None:
            seen = set()
        if fname in seen or fname not in dbpy_funcs:
            return set()
        seen.add(fname)
        direct, calls = dbpy_funcs[fname]
        out = set(direct)
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
        agg = set()
        for fname, (direct, _) in funcs.items():
            kind = "fixture" if is_fixture(rel, fname) else "script"
            for tbl, op in direct:
                if tbl in writers:
                    agg.add((tbl, op, kind))
        for tbl, op, kind in sorted(agg):
            writers[tbl].append({"tool": rel, "op": op, "kind": kind})

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



# ---------------------------------------------------------------- build

def build():
    con = pw.connect_ro(DB)
    # con.execute() returns a FRESH cursor per call, so a query issued inside a loop over
    # another query cannot reset it. The first version shared one cursor and lost 53 of 108
    # FK edges to exactly that, then carried a list() workaround and a comment about it.
    cur = con

    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    views = [(r[0], r[1]) for r in cur.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' ORDER BY name")]
    tsql = {r[0]: (r[1] or "") for r in cur.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table'")}

    counts = {t: cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}
    empty = {t for t in tables if counts[t] == 0}

    stage_ids = pw.load_stages(pw.CONTRACT)
    table_stage, _disputed = pw.load_stage_map(pw.STAGE_MAP)
    judged = _judged_by(pw.STAGE_MAP)
    stage_order = stage_ids + [pw.INFRA, "internal", "unassigned"]
    # ROOTS, not leaves. pw.unwritable() collapses rule 4's probe to the empty PARENTS, and
    # its docstring names three children it still over-reports because one db.py call
    # inserts parent and child in the same transaction. The flat form this module used
    # before reported 19 columns against those 6 roots, beside prose asserting the table
    # cannot accept a row -- the error schema_walkability.py already recorded paying for.
    unwritable_roots = pw.unwritable(con, tables)
    blocked_by: dict = {}
    for _parent, _cols in unwritable_roots.items():
        for _c in _cols:
            _t, _col = _c.split(".", 1)
            blocked_by.setdefault(_t, []).append({"col": _col, "into": _parent})

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
            v = dbcore.check_values(con, t, name)
            if v:
                entry["vocab"] = sorted(v)
            if name in fkcols:
                entry["fk"] = list(fkcols[name])
            cols.append(entry)

        unwritable = blocked_by.get(t, [])

        # EVERY session-column spelling, derived from the schema. Reading only
        # `created_by_session` missed `applied_by_session` (data_migrations, 433 rows),
        # `raised_by_session`, `resolved_by_session`, `retired_by_session` and
        # `amended_by_session` -- whole batches' worth of attribution reported as none.
        # `updated_by_session` is excluded deliberately: it records who last touched a row,
        # not who wrote it, and counting both double-counts every amended row.
        sess: dict = {}
        for _sc in sorted(c["n"] for c in cols if c["n"].endswith("_by_session")
                          and not c["n"].startswith("updated")):
            for _s, _n in cur.execute(f'SELECT "{_sc}", COUNT(*) FROM "{t}" GROUP BY 1'):
                key = _s if _s is not None else "— unattributed"
                sess[key] = sess.get(key, 0) + _n
                sessions_total[key] = sessions_total.get(key, 0) + _n

        internal = t.startswith("sqlite_")
        meta_tables.append({
            "name": t,
            "stage": table_stage.get(t, "internal" if internal else "unassigned"),
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
        _clean = dbcore._strip_sql_line_comments(vsql or "")
        named = sorted({t for t in tables
                        if re.search(r'\b' + re.escape(t) + r'\b', _clean)})
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
    # pw.as_of normalises via _norm_stamp. Comparing the raw strings, as this module did,
    # sorts 'T' (0x54) above ' ' (0x20), so a midnight `...T00:00:00Z` stamp beat a same-day
    # `... 23:59` one and the page could date itself earlier than its newest row.
    asof = pw.as_of(con, tables)

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
            # The ROOTS are the finding; the blocked columns are their consequence. Carried
            # so the page can count 6 empty parents rather than 18 children, three of which
            # are writable anyway (pw.unwritable's docstring names them).
            "unwritable_roots": {k: v for k, v in unwritable_roots.items()},
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
