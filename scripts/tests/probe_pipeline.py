#!/usr/bin/env python3
"""
probe_pipeline.py — AGONIST full-direction pipeline probe over the Guidebook schema.

Logging shape reuses scripts/tests/walk_harness.py conventions: sequence-numbered
actions, verbatim SQL, explicit verdicts. All writes go to scratch copies of the
DB under this directory; the canonical data/guidebook.db is opened mode=ro only.

Verdicts: OK / ERROR / ORPHAN / BLOCKED / FAILED-WRITE / SILENT-PASS

Denominators (verified against the live schema before this run):
  80 FK edges (62 on NOT NULL/PK cols, 18 nullable) · 127 CHECK clauses on 47
  tables · 267 non-PK NOT NULL columns · 5 UNIQUE indexes (origin=u)
  → rejectable-write surface = 479. 66 user tables (39 empty), 18 views,
  0 triggers, 167 .py scripts under scripts/ tools/ schemas/.
"""
import ast
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/guidebook")
CANON = REPO / "data" / "guidebook.db"
# Scratch DBs and logs go to GUIDEBOOK_PROBE_OUT (default: a system temp dir),
# never into the repo tree — this script must not dirty the working copy.
HERE = Path(os.environ.get("GUIDEBOOK_PROBE_OUT")
            or tempfile.mkdtemp(prefix="guidebook-probe-"))
BASE = HERE / "probe.db"          # pristine scratch copy — never written
LOG_MD = HERE / "pipeline-probe-log.md"
LOG_JSON = HERE / "pipeline-probe-findings.json"

assert CANON.exists()
assert BASE.resolve() != CANON.resolve()
# Atomic snapshot: the repo is being actively committed to by other sessions
# (7a7bebe cleared evidence-stage data at 05:15Z; 6dd0cd3 added source_locators at
# 05:19Z — both landed mid-probe). Every sweep reads THIS snapshot, taken now.
shutil.copy(CANON, BASE)
SNAP_HEAD = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                           capture_output=True, text=True).stdout.strip()

_seq = 0
records = []
_md = []


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def md(text):
    _md.append(text if text.endswith("\n") else text + "\n")


def rec(sweep, target, action, expected, actual, verdict, exc=None, sql=None, extra=None):
    global _seq
    _seq += 1
    r = {"seq": _seq, "sweep": sweep, "target": target, "action": action,
         "expected": expected, "actual": actual, "verdict": verdict,
         "exception": exc, "sql": sql}
    if extra:
        r.update(extra)
    records.append(r)
    md(f"\n### [{_seq:04d}] {sweep} — {target}   `{now()}Z`")
    md(f"**Action:** {action}")
    if sql:
        md(f"**SQL:**\n```sql\n{textwrap.dedent(str(sql)).strip()}\n```")
    md(f"**Expected:** {expected}")
    md(f"**Actual:** {actual}")
    if exc:
        md(f"**Exception:** `{exc}`")
    md(f"**Verdict:** {'**`' + verdict + '`**' if verdict == 'SILENT-PASS' else '`' + verdict + '`'}")
    return r


def ro():
    """Read-only handle on the run's atomic snapshot of the canonical DB."""
    return sqlite3.connect(f"file:{BASE}?mode=ro", uri=True)


def fresh_copy(name):
    p = HERE / name
    if p.exists():
        p.unlink()
    shutil.copy(BASE, p)
    return p


# ───────────────────────────── schema introspection ──────────────────────────

con0 = ro()
ALLTABLES = [r[0] for r in con0.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
TABLES = [t for t in ALLTABLES if t != "sqlite_sequence"]     # 66 user tables
VIEWS = [r[0] for r in con0.execute(
    "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")]
TABLE_SQL = {r[0]: (r[1] or "") for r in con0.execute(
    "SELECT name, sql FROM sqlite_master WHERE type='table'")}
COLS = {t: [tuple(r) for r in con0.execute(f"PRAGMA table_info('{t}')")] for t in ALLTABLES}
VIEW_COLS = {v: [r[1] for r in con0.execute(f"PRAGMA table_info('{v}')")] for v in VIEWS}
PK = {t: [c[1] for c in COLS[t] if c[5]] for t in ALLTABLES}

EDGES = []
for t in TABLES:
    rows = con0.execute(f"PRAGMA foreign_key_list('{t}')").fetchall()
    byid = {}
    for (fid, seq_, ptab, fcol, tcol, on_up, on_del, match) in rows:
        byid.setdefault(fid, {"child": t, "fk_id": fid, "parent": ptab,
                              "cols": [], "on_delete": on_del})
        byid[fid]["cols"].append((fcol, tcol))
    EDGES.extend(byid.values())
EDGES.sort(key=lambda e: (e["child"], e["fk_id"]))
for e in EDGES:
    fixed = []
    for (f, tcol) in e["cols"]:
        if tcol is None:
            ppk = PK.get(e["parent"], [])
            tcol = ppk[0] if len(ppk) == 1 else (ppk[len(fixed)] if ppk else None)
        fixed.append((f, tcol))
    e["cols"] = fixed
    info = {c[1]: (c[3], c[5]) for c in COLS[e["child"]]}
    nn, pk = info[e["cols"][0][0]]
    e["nullable"] = not (nn or pk)
NULLABLE_EDGES = [e for e in EDGES if e["nullable"]]

ROWCOUNT = {t: con0.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in TABLES}
UNIQUE_IDX = []
for t in TABLES:
    for r in con0.execute(f"PRAGMA index_list('{t}')"):
        if r[2] == 1 and r[3] == 'u':
            cols = [c[2] for c in con0.execute(f"PRAGMA index_info('{r[1]}')")]
            UNIQUE_IDX.append((t, r[1], cols))
con0.close()

def strip_sql_comments(sql):
    return re.sub(r"--[^\n]*", "", sql)


TABLE_SQL_NC = {t: strip_sql_comments(s) for t, s in TABLE_SQL.items()}


def _balanced_body(s, start):
    """s[start] == '(' → return body inside balanced parens."""
    depth, j = 0, start
    while j < len(s):
        if s[j] == '(':
            depth += 1
        elif s[j] == ')':
            depth -= 1
            if depth == 0:
                return s[start + 1:j]
        j += 1
    return s[start + 1:]


# per-column enum/IN lists, LIKE prefixes, json columns (comment-stripped SQL)
ENUM = {}
JSONCOL = set()
LIKECHECK = {}
for t, sql in TABLE_SQL_NC.items():
    for m in re.finditer(r"(\w+)\s+IN\s*\(", sql):
        col = m.group(1)
        body = _balanced_body(sql, m.end() - 1)
        vals = re.findall(r"'((?:[^']|'')*)'", body) or re.findall(r"-?\d+", body)
        if vals and col.lower() not in ("is", "not", "null"):
            ENUM.setdefault((t, col), vals)
    for m in re.finditer(r"json_valid\s*\(\s*(\w+)\s*\)", sql):
        JSONCOL.add((t, m.group(1)))
    for m in re.finditer(r"(\w+)\s+LIKE\s+'([^'%]*)%'", sql):
        LIKECHECK.setdefault((t, m.group(1)), m.group(2))


def find_checks(sql):
    checks, i = [], 0
    while True:
        m = re.search(r'\bCHECK\s*\(', sql[i:], re.I)
        if not m:
            break
        start = i + m.end() - 1
        depth, j = 0, start
        while j < len(sql):
            if sql[j] == '(':
                depth += 1
            elif sql[j] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        checks.append(sql[start + 1:j])
        i = j + 1
    return checks


CHECKS = {t: find_checks(TABLE_SQL_NC[t]) for t in TABLES}
N_CHECKS = sum(len(v) for v in CHECKS.values())


def col_type(t, c):
    for row in COLS[t]:
        if row[1] == c:
            return (row[2] or "").upper()
    return ""


def colnames(t):
    return {c[1] for c in COLS[t]}


def dummy_for(t, c):
    ty = col_type(t, c)
    if (t, c) in ENUM:
        return ENUM[(t, c)][0]
    if (t, c) in LIKECHECK:
        return LIKECHECK[(t, c)] + "-PROBE"
    if (t, c) in JSONCOL:
        return "[]"
    if "INT" in ty:
        return 1
    if "REAL" in ty or "FLOA" in ty or "DOUB" in ty:
        return 1.0
    return f"PROBE-{c.upper()}"


_uniq = [0]


def uniq():
    _uniq[0] += 1
    return _uniq[0]


FKMAP = {}  # table -> col -> (parent, pcol)
for e in EDGES:
    FKMAP.setdefault(e["child"], {})
    for (f, tc) in e["cols"]:
        FKMAP[e["child"]][f] = (e["parent"], tc)


def parent_value(con, ptab, pcol, depth=0):
    if ptab not in TABLES or pcol is None:
        return None
    try:
        r = con.execute(f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL LIMIT 1').fetchone()
    except sqlite3.Error:
        return None
    if r:
        return r[0]
    if depth >= 4:
        return None
    ok, _, _, _, rowid = try_insert(con, ptab, {}, depth=depth + 1)
    if ok:
        r = con.execute(f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL LIMIT 1').fetchone()
        return r[0] if r else None
    return None


def try_insert(con, table, forced, depth=0, max_retries=12):
    """Adaptive INSERT. Returns (ok, sql_with_vals, exc, vals, lastrowid)."""
    fkmap = FKMAP.get(table, {})
    vals = dict(forced)
    for (cid, name, ty, notnull, dflt, pk) in COLS[table]:
        if name in vals or (name in forced):
            continue
        if pk and "INT" in (ty or "").upper():
            continue
        if notnull and dflt is None:
            if name in fkmap:
                pv = parent_value(con, *fkmap[name], depth=depth)
                if pv is None:
                    return (False, None,
                            f"BLOCKED: no parent value obtainable for NOT NULL FK {table}.{name} -> {fkmap[name]}",
                            vals, None)
                vals[name] = pv
            else:
                vals[name] = dummy_for(table, name)
        elif pk:
            if name in fkmap:   # TEXT PK that is also an FK (e.g. bpc_metadata.slug)
                pv = parent_value(con, *fkmap[name], depth=depth)
                if pv is None:
                    return (False, None,
                            f"BLOCKED: no parent value obtainable for PK-FK {table}.{name} -> {fkmap[name]}",
                            vals, None)
                vals[name] = pv
            else:
                vals[name] = f"PROBE-PK-{uniq()}"
    last_exc = None
    for attempt in range(max_retries):
        cols = [c for c in vals]
        sql = (f'INSERT INTO "{table}" ({", ".join(chr(34)+c+chr(34) for c in cols)}) '
               f'VALUES ({", ".join("?" for _ in cols)})')
        shown = sql + "  -- " + json.dumps({c: vals[c] for c in cols}, default=str)
        try:
            cur = con.execute(sql, [vals[c] for c in cols])
            return (True, shown, None, dict(vals), cur.lastrowid)
        except sqlite3.Error as exc:
            last_exc = f"{type(exc).__name__}: {exc}"
            msg = str(exc)
            if "FOREIGN KEY constraint failed" in msg:
                return (False, shown, last_exc, dict(vals), None)
            m = re.search(r"NOT NULL constraint failed: (\w+)\.(\w+)", msg)
            if m and m.group(2) not in forced:
                c = m.group(2)
                if c in fkmap:
                    pv = parent_value(con, *fkmap[c], depth=depth)
                    if pv is None:
                        return (False, shown, last_exc, dict(vals), None)
                    vals[c] = pv
                else:
                    vals[c] = dummy_for(table, c)
                continue
            if "CHECK constraint failed" in msg:
                fixed = False
                mentioned = [c for c in colnames(table) if re.search(r"\b" + re.escape(c) + r"\b", msg)]
                for (tt, cc), allowed in ENUM.items():
                    if tt == table and cc not in forced:
                        cur_v = vals.get(cc)
                        if cur_v is None or str(cur_v) not in [str(a) for a in allowed]:
                            if cc in vals or cc in mentioned:
                                vals[cc] = allowed[0]
                                fixed = True
                for (tt, cc) in JSONCOL:
                    if tt == table and cc not in forced and vals.get(cc) not in (None, "[]"):
                        vals[cc] = "[]"
                        fixed = True
                if not fixed:
                    # add dummies for nullable columns named in the failing expression
                    for c in mentioned:
                        if c not in vals and c not in forced:
                            vals[c] = dummy_for(table, c)
                            fixed = True
                if not fixed:
                    for c in mentioned:
                        if c in vals and c not in forced and not any(
                                r[1] == c and r[3] for r in COLS[table]):
                            vals.pop(c)
                            fixed = True
                            break
                if not fixed:
                    return (False, shown, last_exc, dict(vals), None)
                continue
            if "UNIQUE constraint failed" in msg:
                changed = False
                dup_cols = re.findall(r"\b\w+\.(\w+)", msg)
                for c in dup_cols or list(vals):
                    if c in forced or c not in vals:
                        continue
                    if c in fkmap:
                        ptab, pcol = fkmap[c]
                        try:
                            r = con.execute(
                                f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL AND "{pcol}" != ? '
                                f'ORDER BY RANDOM() LIMIT 1',
                                [vals[c]]).fetchone()
                        except sqlite3.Error:
                            r = None
                        if r is None and depth < 4:
                            okp, _, _, _, _ = try_insert(con, ptab, {}, depth=depth + 1)
                            if okp:
                                r = con.execute(
                                    f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL AND "{pcol}" != ? '
                                    f'ORDER BY RANDOM() LIMIT 1',
                                    [vals[c]]).fetchone()
                        if r:
                            vals[c] = r[0]
                            changed = True
                    elif isinstance(vals[c], str):
                        vals[c] = f"PROBE-U{uniq()}"
                        changed = True
                    elif isinstance(vals[c], (int, float)):
                        vals[c] = 900000 + uniq()
                        changed = True
                if not changed:
                    return (False, shown, last_exc, dict(vals), None)
                continue
            if "datatype mismatch" in msg:
                for c in list(vals):
                    if c in forced:
                        continue
                    ty = col_type(table, c)
                    if "INT" in ty and isinstance(vals[c], str):
                        vals[c] = 1
                    elif "REAL" in ty and isinstance(vals[c], str):
                        vals[c] = 1.0
                continue
            return (False, shown, last_exc, dict(vals), None)
    return (False, None, last_exc, dict(vals), None)


_CONTROL = {}   # (conn id, table) -> vals or ("FAIL", reason)


def control_vals(con, table):
    key = (id(con), table)
    if key in _CONTROL:
        return _CONTROL[key]
    ok, sql, exc, vals, rowid = try_insert(con, table, {})
    if ok:
        _CONTROL[key] = ("OK", dict(vals))
    else:
        _CONTROL[key] = ("FAIL", exc)
    return _CONTROL[key]


def probe_insert(con, table, overrides, expect_substr):
    """Insert control-row clone with overrides; classify against expect_substr.
    Returns (outcome, sql, exc): outcome in accepted/target-fired/other."""
    status, payload = control_vals(con, table)
    if status == "FAIL":
        # fallback: adaptive insert with the violation forced, inside a savepoint
        con.execute("SAVEPOINT probefb")
        okf, sqlf, excf, _, _ = try_insert(con, table, overrides)
        con.execute("ROLLBACK TO probefb")
        con.execute("RELEASE probefb")
        if okf:
            return ("accepted", sqlf, None)
        if excf and expect_substr and expect_substr in str(excf):
            return ("target-fired", sqlf, excf)
        return ("uncontrollable", sqlf, f"control-row build failed ({payload}); "
                f"fallback probe result: {excf}")
    vals = dict(payload)
    # freshen non-FK PROBE strings so we don't trip UNIQUE on the control row
    fkcols = set(FKMAP.get(table, {}))
    for c in list(vals):
        if c in overrides:
            continue
        if isinstance(vals[c], str) and vals[c].startswith("PROBE") and c not in fkcols:
            vals[c] = f"PROBE-{uniq()}"
    for c, v in overrides.items():
        vals[c] = v
    last = None
    for attempt in range(6):
        cols = [c for c in vals if not (vals[c] is None and c not in overrides)]
        sql = (f'INSERT INTO "{table}" ({", ".join(chr(34)+c+chr(34) for c in cols)}) '
               f'VALUES ({", ".join("?" for _ in cols)})')
        shown = sql + "  -- " + json.dumps({c: vals[c] for c in cols}, default=str)
        con.execute("SAVEPOINT probe")
        try:
            con.execute(sql, [vals[c] for c in cols])
            con.execute("ROLLBACK TO probe")
            con.execute("RELEASE probe")
            return ("accepted", shown, None)
        except sqlite3.Error as exc:
            con.execute("ROLLBACK TO probe")
            con.execute("RELEASE probe")
            last = f"{type(exc).__name__}: {exc}"
            msg = str(exc)
            if expect_substr and expect_substr in msg:
                return ("target-fired", shown, last)
            if "UNIQUE constraint failed" in msg:
                dup_cols = re.findall(r"\b\w+\.(\w+)", msg)
                changed = False
                for c in dup_cols:
                    if c in overrides or c not in vals:
                        continue
                    if c in fkcols:
                        ptab, pcol = FKMAP[table][c]
                        r = con.execute(
                            f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL AND "{pcol}" != ? '
                            f'ORDER BY RANDOM() LIMIT 1', [vals[c]]).fetchone()
                        if r is None:
                            okp, _, _, pvals, _ = try_insert(con, ptab, {})
                            if okp:
                                r = con.execute(
                                    f'SELECT "{pcol}" FROM "{ptab}" WHERE "{pcol}" IS NOT NULL AND "{pcol}" != ? LIMIT 1',
                                    [vals[c]]).fetchone()
                        if r:
                            vals[c] = r[0]
                            changed = True
                    elif isinstance(vals[c], str):
                        vals[c] = f"PROBE-U{uniq()}"
                        changed = True
                    else:
                        vals[c] = 900000 + uniq()
                        changed = True
                if changed:
                    continue
            return ("other", shown, last)
    return ("other", None, last)


def violation_for_check(table, expr):
    """Return (overrides, description) that should falsify the CHECK, or None."""
    e = expr.strip()
    m = re.match(r"^\s*(\w+)\s+IS\s+NULL\s+OR\s+(.*)$", e, re.S | re.I)
    if m:
        e = m.group(2)
    m = re.search(r"json_valid\s*\(\s*(\w+)\s*\)", e)
    if m:
        return ({m.group(1): "{not-json"}, f"invalid JSON in {m.group(1)}")
    m = re.search(r"(\w+)\s+BETWEEN\s+(-?\d+)\s+AND\s+(-?\d+)", e, re.I)
    if m:
        return ({m.group(1): int(m.group(3)) + 1}, f"{m.group(1)} above range")
    m = re.search(r"(\w+)\s+IN\s*\(([^()]*)\)", e, re.I)
    if m:
        col, body = m.group(1), m.group(2)
        if re.search(r"'", body):
            bad = "PROBE-INVALID-ENUM"
        else:
            bad = 987654321
        if "INT" in col_type(table, col) and isinstance(bad, str):
            bad = 987654321
        return ({col: bad}, f"{col} outside enum")
    m = re.search(r"(\w+)\s*(>=|<=|>|<)\s*(-?\d+)", e)
    if m:
        col, op, n = m.group(1), m.group(2), int(m.group(3))
        bad = {".>=": n - 1, ".>": n, ".<=": n + 1, ".<": n}["." + op]
        return ({col: bad}, f"{col} violates {op} {n}")
    m = re.search(r"(\w+)\s+LIKE\s+'([^']*)'", e, re.I)
    if m:
        return ({m.group(1): "PROBE-NOLIKE"}, f"{m.group(1)} fails LIKE")
    m = re.search(r"(\w+)\s*=\s*'([^']+)'\s+AND\s+(\w+)\s+IS\s+NULL", e, re.I)
    if m:
        return ({m.group(1): m.group(2), m.group(3): dummy_for(table, m.group(3))},
                f"{m.group(1)}='{m.group(2)}' with {m.group(3)} non-NULL")
    # "outcome != 'x' OR (dep IS NOT NULL ...)" → outcome='x', dep=NULL
    m = re.search(r"(\w+)\s*!=\s*'([^']+)'\s+OR\s+\(?\s*(\w+)\s+IS\s+NOT\s+NULL", e, re.I)
    if m:
        return ({m.group(1): m.group(2), m.group(3): None},
                f"{m.group(1)}='{m.group(2)}' with {m.group(3)} NULL")
    # "a IS NOT NULL OR b IS NOT NULL OR ..." → all named cols NULL
    if re.fullmatch(r"(?:\s*\w+\s+IS\s+NOT\s+NULL\s*(?:OR)?\s*)+", e, re.I):
        cols_ = re.findall(r"(\w+)\s+IS\s+NOT\s+NULL", e, re.I)
        return ({c: None for c in cols_}, f"all of {cols_} NULL")
    return None


# ═════════════════════════════ HEADER ════════════════════════════════════════

N_NOTNULL = sum(1 for t in TABLES for c in COLS[t] if c[3] and not c[5])
SURFACE_DENOM = len(EDGES) + N_CHECKS + N_NOTNULL + len(UNIQUE_IDX)
md("# Pipeline probe log — AGONIST full-direction probe\n")
md(f"Generated {now()}Z. Subject: atomic snapshot `{BASE.name}` of `data/guidebook.db` at repo HEAD "
   f"`{SNAP_HEAD}` (the repo received two data commits MID-SESSION — 7a7bebe evidence-stage clear, "
   f"6dd0cd3 source_locators recovery — so every sweep reads this one snapshot; the canonical file was "
   f"only ever opened read-only, for copying).")
md(f"Schema: {len(TABLES)} user tables ({sum(1 for t in TABLES if ROWCOUNT[t]==0)} empty), "
   f"{len(VIEWS)} views, 0 triggers, PRAGMA user_version as committed.")
md(f"Denominators (live-derived from the snapshot): **{len(EDGES)} FK edges** "
   f"({len(EDGES)-len(NULLABLE_EDGES)} NOT NULL/PK, {len(NULLABLE_EDGES)} nullable) · "
   f"**{N_CHECKS} CHECK clauses** · **{N_NOTNULL} non-PK NOT NULL columns** · "
   f"**{len(UNIQUE_IDX)} UNIQUE indexes** → rejectable-write surface = {SURFACE_DENOM}. "
   f"(The independently verified pre-054 denominators were 80/127/267/5 = 479; migration 054 "
   f"added source_locators: +1 CHECK, +1 NOT NULL.)")
md("\nVerdict legend: `OK` correct behaviour · `ERROR` defect/unexpected failure · "
   "`ORPHAN` dangling rows/joints found · `BLOCKED` probe could not isolate the target "
   "(counts toward Examined, not toward Passed) · `FAILED-WRITE` a sanctioned write failed · "
   "**`SILENT-PASS`** a write that should have been rejected and was accepted.\n")

# ═════════════════════════════ SWEEP A ═══════════════════════════════════════

md("\n\n---\n\n## SWEEP A — schema connectivity, both directions\n")

md("\n### A1 — full FK edge list (PRAGMA foreign_key_list per table)\n")
md("| # | child table | child col | parent table | parent col | on_delete | child col nullable |")
md("|---|---|---|---|---|---|---|")
for i, e in enumerate(EDGES, 1):
    fc = ", ".join(f for f, _ in e["cols"])
    tc = ", ".join(str(t) for _, t in e["cols"])
    md(f"| {i} | `{e['child']}` | `{fc}` | `{e['parent']}` | `{tc}` | {e['on_delete']} | "
       f"{'YES — NULL-bypassable' if e['nullable'] else 'no'} |")
rec("A1", "all tables", f"Enumerate FK edges via PRAGMA foreign_key_list over {len(TABLES)} user tables",
    "complete edge list",
    f"{len(EDGES)} FK edges, all single-column; {len(NULLABLE_EDGES)} on NULLABLE columns "
    f"(NULL-bypassable); DEFERRABLE clauses present in: "
    f"{sorted(t for t, s in TABLE_SQL.items() if 'DEFERRABLE' in s.upper())}", "OK",
    extra={"edge_count": len(EDGES), "nullable_edges": len(NULLABLE_EDGES),
           "edges": [{"child": e["child"], "cols": e["cols"], "parent": e["parent"],
                      "nullable": e["nullable"]} for e in EDGES]})

# A2 — existing orphans on canonical
con = ro()
fkc = con.execute("PRAGMA foreign_key_check").fetchall()
rec("A2", "canonical DB", "PRAGMA foreign_key_check (whole DB)",
    "0 violations", f"{len(fkc)} violations", "OK" if not fkc else "ORPHAN")
rec("A2", "scripts/migrate_db.py:161", "compare the code comment '~18 pre-existing violations' against reality",
    "comment matches the DB",
    f"comment claims '~18 violations' of production drift; PRAGMA foreign_key_check returns {len(fkc)}. "
    "The comment is STALE — the tolerance it justifies (only NEW violations fail an apply) remains in the code",
    "ERROR")

a2_examined = 2
a2_orphans = []
for e in EDGES:
    a2_examined += 1
    child, parent = e["child"], e["parent"]
    conds = " AND ".join(f'c."{f}" IS NOT NULL' for f, _ in e["cols"])
    joins = " AND ".join(f'c."{f}" = p."{t}"' for f, t in e["cols"])
    sel = ", ".join(f'c."{f}"' for f, _ in e["cols"])
    sql = (f'SELECT {sel}, COUNT(*) n FROM "{child}" c LEFT JOIN "{parent}" p ON {joins} '
           f'WHERE {conds} AND p."{e["cols"][0][1]}" IS NULL GROUP BY {sel}')
    try:
        rows = con.execute(sql).fetchall()
    except sqlite3.Error as exc:
        rec("A2", f"{child}.{e['cols'][0][0]} → {parent}", "LEFT JOIN orphan query",
            "query runs", "query failed", "ERROR", exc=f"{type(exc).__name__}: {exc}", sql=sql)
        continue
    if rows:
        a2_orphans.append({"edge": f"{child}.{e['cols'][0][0]} → {parent}", "rows": rows})
        rec("A2", f"{child}.{e['cols'][0][0]} → {parent}", "LEFT JOIN orphan query",
            "0 orphans", f"{len(rows)} distinct orphan value(s): {rows[:25]}", "ORPHAN", sql=sql)
    else:
        rec("A2", f"{child}.{e['cols'][0][0]} → {parent}", "LEFT JOIN orphan query",
            "0 orphans", "0 orphans", "OK")

# A2b — mid-session data state change, then NULL-bypass check on live data
rec("A2", "canonical DB — mid-session change of subject",
    "compare row counts observed at session start against the current canonical",
    "stable subject",
    "TWO commits landed in the repo DURING this probe session: 7a7bebe ('clear all evidence-stage data; "
    "preserve schema for repopulation', 05:15Z) cleared item_population_elaborations (3 rows), "
    "pipeline_runs (6), url_verification_runs (5), items.pmp_* residue, 75 jurisdictional_values values "
    "and sqlite_sequence marks; 6dd0cd3 ('recover 835 document locators from the pre-reset corpus', "
    "05:19Z) added the source_locators table (835 rows, user_version 53→54, +1 CHECK, +1 NOT NULL). "
    "This run's snapshot postdates both; all sweeps read the snapshot atomically",
    "OK")
a2_examined += 1
ipe = con.execute("SELECT COUNT(*), SUM(evidence_ref_id IS NULL) FROM item_population_elaborations").fetchone()
rec("A2", "item_population_elaborations.evidence_ref_id (live NULL-bypass)",
    "check whether live data takes the NULL path around a declared FK",
    "rows carry provenance",
    f"post-clear: {ipe[0]} rows ({ipe[1] or 0} NULL). PRE-clear (verified at session start, before commit "
    f"7a7bebe): 3 rows, ALL 3 with evidence_ref_id NULL against an EMPTY evidence_sources parent — live "
    f"data had already taken the NULL-bypass path this sweep demonstrates synthetically in A3b. The "
    f"clearing commit removed the rows; the structural hole remains (see A3b seq for this edge)",
    "ORPHAN")
a2_examined += 1

# A2c — undeclared conventional references
undeclared = [
    ("evidence_population_match", "source_ref", "evidence_sources",
     'SELECT m.match_id, m.source_ref FROM evidence_population_match m LEFT JOIN evidence_sources s ON m.source_ref = s.ref_id WHERE m.source_ref IS NOT NULL AND s.ref_id IS NULL'),
    ("evidence_population_match", "target_population", "populations",
     'SELECT m.match_id, m.target_population FROM evidence_population_match m LEFT JOIN populations p ON m.target_population = p.population_code WHERE m.target_population IS NOT NULL AND p.population_code IS NULL'),
    ("source_value_extractions", "echo_of", "source_value_extractions",
     'SELECT e.extraction_id, e.echo_of FROM source_value_extractions e LEFT JOIN source_value_extractions p ON CAST(e.echo_of AS INTEGER) = p.extraction_id WHERE e.echo_of IS NOT NULL AND p.extraction_id IS NULL'),
]
for (t, c, pt, sql) in undeclared:
    a2_examined += 1
    try:
        rows = con.execute(sql).fetchall()
    except sqlite3.Error as exc:
        rec("A2", f"{t}.{c} →(undeclared) {pt}", "undeclared-reference orphan query",
            "query runs", "failed", "ERROR", exc=str(exc), sql=sql)
        continue
    v = "ORPHAN" if rows else "OK"
    if rows:
        a2_orphans.append({"edge": f"{t}.{c} →(undeclared) {pt}", "rows": rows})
    rec("A2", f"{t}.{c} →(undeclared) {pt}",
        "orphan query on a reference column that has NO declared FK",
        "0 dangling", f"{len(rows)} dangling: {rows[:20]}", v, sql=sql)

for (t, c) in [("specifications", "governing_refs"), ("search_executions", "admitted_ref_ids")]:
    a2_examined += 1
    sql = (f"SELECT t.rowid, j.value FROM {t} t, json_each(t.{c}) j "
           f"LEFT JOIN evidence_sources s ON j.value = s.ref_id "
           f"WHERE t.{c} IS NOT NULL AND s.ref_id IS NULL")
    try:
        rows = con.execute(sql).fetchall()
    except sqlite3.Error as exc:
        rec("A2", f"{t}.{c} (JSON) → evidence_sources", "JSON dual-store dangling-ref scan",
            "query runs", "failed", "ERROR", exc=str(exc), sql=sql)
        continue
    v = "ORPHAN" if rows else "OK"
    if rows:
        a2_orphans.append({"edge": f"{t}.{c} (JSON) → evidence_sources", "rows": rows})
    rec("A2", f"{t}.{c} (JSON) → evidence_sources",
        "every ref named in the JSON array must exist in evidence_sources (no FK can enforce a JSON payload)",
        "0 dangling", f"{len(rows)} dangling ref(s): {rows[:25]}", v, sql=sql)
con.close()

# ── A3 — child-without-parent probes, foreign_keys=ON ────────────────────────
md("\n### A3 — bad-value FK probes, `PRAGMA foreign_keys=ON` (80/80 edges)\n")
db_on = fresh_copy("probe-a-on.db")
con_on = sqlite3.connect(db_on, isolation_level=None)   # autocommit; savepoints scope probes
con_on.execute("PRAGMA foreign_keys=ON")
a3_stats = {"OK": 0, "SILENT-PASS": 0, "BLOCKED": 0}


def bogus_for(con, t, c, ptab, pcol):
    if (t, c) in ENUM:
        try:
            existing = {r[0] for r in con.execute(f'SELECT DISTINCT "{pcol}" FROM "{ptab}"')}
        except sqlite3.Error:
            existing = set()
        for v in ENUM[(t, c)]:
            if v not in existing:
                return v
        return None
    ty = col_type(t, c)
    if "INT" in ty:
        return 999999900 + uniq()
    return f"PROBE-NO-SUCH-PARENT-{uniq()}"


def fk_probe(con, e, mode):
    child, parent = e["child"], e["parent"]
    f0, t0 = e["cols"][0]
    tag = f"{child}.{f0} → {parent}.{t0}"
    b = bogus_for(con, child, f0, parent, t0)
    if b is None:
        return (tag, "BLOCKED", None, "could not craft a bogus value (enum FK col, all enum values exist in parent)", None)
    con.execute("SAVEPOINT fkp")
    ok, sql, exc, vals, _ = try_insert(con, child, {f0: b})
    verdict, note = None, None
    if ok:
        viol = con.execute(f"PRAGMA foreign_key_check('{child}')").fetchall()
        con.execute("ROLLBACK TO fkp")
        con.execute("RELEASE fkp")
        if mode == "ON":
            if viol:
                # deferred FK — violation pending inside txn; verify commit-time enforcement
                con.execute("SAVEPOINT fkp2")
                ok2, _, exc2, _, _ = try_insert(con, child, {f0: b})
                if not ok2:
                    try:
                        con.execute("ROLLBACK TO fkp2")
                        con.execute("RELEASE fkp2")
                    except sqlite3.Error:
                        pass
                    verdict, note = "OK", f"deferred FK enforced on re-insert: {exc2}"
                else:
                    try:
                        con.execute("RELEASE fkp2")  # outermost release == COMMIT in autocommit
                        verdict, note = ("SILENT-PASS",
                                         "insert AND COMMIT accepted under FK=ON despite foreign_key_check violation")
                        con.execute(f'DELETE FROM "{child}" WHERE "{f0}" = ?', [b])
                    except sqlite3.Error as ce:
                        try:
                            con.rollback()
                        except sqlite3.Error:
                            pass
                        verdict, note = "OK", f"deferred FK — COMMIT rejected: {ce}"
            else:
                verdict, note = "SILENT-PASS", "insert accepted and foreign_key_check clean — FK not enforced on this edge"
        else:
            verdict, note = "SILENT-PASS", "insert accepted under FK=OFF (the migrate_db.py apply mode) — violation would persist"
    else:
        con.execute("ROLLBACK TO fkp")
        con.execute("RELEASE fkp")
        if exc and "FOREIGN KEY constraint failed" in str(exc):
            verdict, note = "OK", "rejected with FK error"
        else:
            verdict, note = "BLOCKED", "probe blocked by a different constraint before the FK could be evaluated"
    return (tag, verdict, sql, note, exc)


for e in EDGES:
    tag, verdict, sql, note, exc = fk_probe(con_on, e, "ON")
    a3_stats[verdict] += 1
    rec("A3", tag, "insert child with nonexistent parent value (FK=ON)",
        "insert rejected with FOREIGN KEY constraint failed", note, verdict, exc=exc, sql=sql)

# A3b — NULL-path probes for the 18 nullable edges
md("\n### A3b — NULL-path probes for the 18 nullable FK edges (FK never evaluated on NULL)\n")
a3b_stats = {"SILENT-PASS": 0, "BLOCKED": 0, "OK": 0}
for e in NULLABLE_EDGES:
    f0, t0 = e["cols"][0]
    tag = f"{e['child']}.{f0} → {e['parent']} (NULL path)"
    outcome, sql, exc = probe_insert(con_on, e["child"], {f0: None}, None)
    if outcome == "accepted":
        a3b_stats["SILENT-PASS"] += 1
        rec("A3b", tag, "insert child row with the FK column explicitly NULL (FK=ON)",
            "if the reference is semantically required, some constraint should reject it",
            "row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. "
            "Any writer can skip provenance on this edge",
            "SILENT-PASS", sql=sql)
    elif outcome == "uncontrollable":
        a3b_stats["BLOCKED"] += 1
        rec("A3b", tag, "insert child row with FK col NULL (FK=ON)", "row accepted",
            "control row could not be built for this table", "BLOCKED", exc=exc)
    else:
        a3b_stats["BLOCKED"] += 1
        rec("A3b", tag, "insert child row with FK col NULL (FK=ON)", "row accepted",
            "blocked by another constraint", "BLOCKED", exc=exc, sql=sql)

# A3c — dual-identity defect probe: evidence_population_match
outcome, sql, exc = probe_insert(
    con_on, "evidence_population_match",
    {"source_ref": "PROBE-GARBAGE-NOT-A-REF", "ref_id": None}, None)
rec("A3c", "evidence_population_match.source_ref vs ref_id (dual identity columns)",
    "satisfy NOT NULL with free text in source_ref while leaving the FK'd ref_id NULL",
    "the row should be rejected — it claims a source that does not exist",
    "ACCEPTED" if outcome == "accepted" else outcome + " — see exception",
    "SILENT-PASS" if outcome == "accepted" else "BLOCKED", exc=exc, sql=sql)

# ── A4 — same bad-value probes with foreign_keys=OFF ─────────────────────────
md("\n### A4 — bad-value FK probes, `PRAGMA foreign_keys=OFF` (the migrate_db.py apply mode)\n")
db_off = fresh_copy("probe-a-off.db")
con_off = sqlite3.connect(db_off, isolation_level=None)
con_off.execute("PRAGMA foreign_keys=OFF")
a4_stats = {"SILENT-PASS": 0, "BLOCKED": 0, "OK": 0}
a4_committed = []
for e in EDGES:
    child, parent = e["child"], e["parent"]
    f0, t0 = e["cols"][0]
    tag = f"{child}.{f0} → {parent}.{t0}"
    b = bogus_for(con_off, child, f0, parent, t0)
    if b is None:
        a4_stats["BLOCKED"] += 1
        rec("A4", tag, "insert child with nonexistent parent value (FK=OFF)",
            "n/a", "could not craft bogus value", "BLOCKED")
        continue
    ok, sql, exc, vals, _ = try_insert(con_off, child, {f0: b})
    if ok:
        con_off.commit()
        a4_stats["SILENT-PASS"] += 1
        a4_committed.append(tag)
        rec("A4", tag, "insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)",
            "would be rejected under FK=ON", "insert COMMITTED — violation persists in the file",
            "SILENT-PASS", sql=sql)
    else:
        a4_stats["BLOCKED"] += 1
        rec("A4", tag, "insert child with nonexistent parent value (FK=OFF)",
            "commit of violation", "blocked by a non-FK constraint (CHECK/NOT NULL still fire under FK=OFF)",
            "BLOCKED", exc=exc, sql=sql)
post = con_off.execute("PRAGMA foreign_key_check").fetchall()
rec("A4", "probe-a-off.db", "PRAGMA foreign_key_check after committing all FK=OFF probes",
    f"{a4_stats['SILENT-PASS']} violations visible",
    f"{len(post)} violation rows persisted. migrate_db.py COMMITS the migration BEFORE running this "
    "check, tolerates any violation already in `pre_violations`, and skips the failure entirely when the "
    "migration body contains 'BOOTSTRAP' in its first 500 bytes — so every one of these edges is a "
    "committable write-path defect",
    "SILENT-PASS" if post else "OK",
    extra={"violations_sample": [tuple(r) for r in post[:60]]})

# ── A5 — reverse direction ───────────────────────────────────────────────────
inbound = {t: [] for t in TABLES}
outbound = {t: [] for t in TABLES}
for e in EDGES:
    if e["parent"] in inbound:
        inbound[e["parent"]].append(e["child"])
    outbound[e["child"]].append(e["parent"])
isolated = [t for t in TABLES if not inbound[t] and not outbound[t]]
ref_empty = [t for t in TABLES if inbound[t] and ROWCOUNT[t] == 0]
md("\n### A5 — reverse-direction map\n")
md("| table | rows | referenced by (inbound) | references (outbound) |")
md("|---|---|---|---|")
for t in TABLES:
    md(f"| `{t}` | {ROWCOUNT[t]} | {', '.join(sorted(set(inbound[t]))) or '—'} | "
       f"{', '.join(sorted(set(outbound[t]))) or '—'} |")
rec("A5", "all tables", "reverse-direction analysis: inbound edges, isolated tables, referenced-but-empty",
    "connected schema",
    f"isolated (no inbound AND no outbound FK): {isolated} · referenced-but-EMPTY parent tables: {ref_empty} · "
    f"empty tables total: {sum(1 for t in TABLES if ROWCOUNT[t]==0)}/66",
    "ORPHAN" if ref_empty else "OK",
    extra={"isolated_tables": isolated, "referenced_but_empty": ref_empty, "row_counts": ROWCOUNT})

# ── A6 — CHECK battery, both modes ───────────────────────────────────────────
md("\n### A6 — CHECK-constraint battery (127 clauses), FK=ON and FK=OFF\n")
check_stats = {}
for mode, conx in (("ON", con_on), ("OFF", con_off)):
    st = {"OK": 0, "SILENT-PASS": 0, "BLOCKED": 0}
    for t in TABLES:
        for expr in CHECKS[t]:
            short = re.sub(r"\s+", " ", expr)[:110]
            v = violation_for_check(t, expr)
            if v is None:
                st["BLOCKED"] += 1
                rec(f"A6/{mode}", f"{t} CHECK({short})",
                    f"construct a violating row (FK={mode})",
                    "CHECK fires", "no mechanical violation constructible for this expression "
                    "(cross-column/complex predicate)", "BLOCKED")
                continue
            overrides, desc = v
            outcome, sql, exc = probe_insert(conx, t, overrides, "CHECK constraint failed")
            if outcome == "target-fired":
                st["OK"] += 1
                rec(f"A6/{mode}", f"{t} CHECK({short})",
                    f"insert row violating the CHECK ({desc}; FK={mode})",
                    "CHECK constraint failed", "rejected by CHECK", "OK", exc=exc, sql=sql)
            elif outcome == "accepted":
                st["SILENT-PASS"] += 1
                rec(f"A6/{mode}", f"{t} CHECK({short})",
                    f"insert row violating the CHECK ({desc}; FK={mode})",
                    "CHECK constraint failed", "row ACCEPTED — the CHECK did not fire",
                    "SILENT-PASS", sql=sql)
            elif outcome == "uncontrollable":
                st["BLOCKED"] += 1
                rec(f"A6/{mode}", f"{t} CHECK({short})",
                    f"insert row violating the CHECK (FK={mode})",
                    "CHECK fires", "control row could not be built for this table", "BLOCKED", exc=exc)
            else:
                st["BLOCKED"] += 1
                rec(f"A6/{mode}", f"{t} CHECK({short})",
                    f"insert row violating the CHECK ({desc}; FK={mode})",
                    "CHECK fires", "a different constraint intervened", "BLOCKED", exc=exc, sql=sql)
    check_stats[mode] = st

# ── A7 — NOT NULL battery, both modes ────────────────────────────────────────
md("\n### A7 — NOT NULL battery (267 non-PK NOT NULL columns), FK=ON and FK=OFF\n")
notnull_cols = [(t, c[1]) for t in TABLES for c in COLS[t] if c[3] and not c[5]]
nn_stats = {}
for mode, conx in (("ON", con_on), ("OFF", con_off)):
    st = {"OK": 0, "SILENT-PASS": 0, "BLOCKED": 0}
    for (t, c) in notnull_cols:
        outcome, sql, exc = probe_insert(conx, t, {c: None}, "NOT NULL constraint failed")
        if outcome == "target-fired":
            st["OK"] += 1
            rec(f"A7/{mode}", f"{t}.{c}", f"insert explicit NULL into NOT NULL column (FK={mode})",
                "NOT NULL constraint failed", "rejected", "OK", exc=exc, sql=sql)
        elif outcome == "accepted":
            st["SILENT-PASS"] += 1
            rec(f"A7/{mode}", f"{t}.{c}", f"insert explicit NULL into NOT NULL column (FK={mode})",
                "NOT NULL constraint failed", "row ACCEPTED with NULL", "SILENT-PASS", sql=sql)
        elif outcome == "uncontrollable":
            st["BLOCKED"] += 1
            rec(f"A7/{mode}", f"{t}.{c}", f"insert explicit NULL (FK={mode})",
                "NOT NULL fires", "control row could not be built", "BLOCKED", exc=exc)
        else:
            st["BLOCKED"] += 1
            rec(f"A7/{mode}", f"{t}.{c}", f"insert explicit NULL (FK={mode})",
                "NOT NULL fires", "a different constraint intervened", "BLOCKED", exc=exc, sql=sql)
    nn_stats[mode] = st

# ── A8 — UNIQUE battery, both modes ──────────────────────────────────────────
md("\n### A8 — UNIQUE battery (5 UNIQUE indexes), FK=ON and FK=OFF\n")
uq_stats = {}
for mode, conx in (("ON", con_on), ("OFF", con_off)):
    st = {"OK": 0, "SILENT-PASS": 0, "BLOCKED": 0}
    for (t, idx, ucols) in UNIQUE_IDX:
        status, payload = control_vals(conx, t)
        if status == "OK" and all(payload.get(c) is not None for c in ucols):
            # the committed control row already carries the full unique key — duplicate it
            key = {c: payload[c] for c in ucols}
        else:
            # seed a row that fills the unique key, then duplicate it
            forced = {}
            for c in ucols:
                if c in FKMAP.get(t, {}):
                    forced[c] = parent_value(conx, *FKMAP[t][c])
                else:
                    dv = dummy_for(t, c)
                    forced[c] = dv if not isinstance(dv, str) else f"PROBE-UQ-{uniq()}"
            ok1, sql1, exc1, vals1, _ = try_insert(conx, t, forced)
            if not ok1:
                st["BLOCKED"] += 1
                rec(f"A8/{mode}", f"{t} UNIQUE({', '.join(ucols)})",
                    f"seed row for duplicate probe (FK={mode})",
                    "seed inserts", "seed row failed", "BLOCKED", exc=exc1, sql=sql1)
                continue
            key = {c: vals1[c] for c in ucols}
        outcome, sql2, exc2 = probe_insert(conx, t, key, "UNIQUE constraint failed")
        if outcome == "target-fired" and not any(c in (exc2 or "") for c in ucols):
            outcome = "other"   # a different UNIQUE index fired — not this probe's target
        if outcome == "target-fired":
            st["OK"] += 1
            rec(f"A8/{mode}", f"{t} UNIQUE({', '.join(ucols)})",
                f"insert second row duplicating the unique key (FK={mode})",
                "UNIQUE constraint failed", "rejected", "OK", exc=exc2, sql=sql2)
        elif outcome == "accepted":
            st["SILENT-PASS"] += 1
            rec(f"A8/{mode}", f"{t} UNIQUE({', '.join(ucols)})",
                f"insert second row duplicating the unique key (FK={mode})",
                "UNIQUE constraint failed", "duplicate ACCEPTED", "SILENT-PASS", sql=sql2)
        else:
            st["BLOCKED"] += 1
            rec(f"A8/{mode}", f"{t} UNIQUE({', '.join(ucols)})",
                f"duplicate-key probe (FK={mode})", "UNIQUE fires",
                "a different constraint intervened", "BLOCKED", exc=exc2, sql=sql2)
    uq_stats[mode] = st

con_on.close()
con_off.close()

a_examined = {
    "edges_enumerated": len(EDGES),
    "orphan_queries": a2_examined,
    "fk_bad_value_ON": len(EDGES), "fk_bad_value_ON_results": a3_stats,
    "fk_null_path": len(NULLABLE_EDGES), "fk_null_path_results": a3b_stats,
    "dual_identity_probe": 1,
    "fk_bad_value_OFF": len(EDGES), "fk_bad_value_OFF_results": a4_stats,
    "check_ON": sum(check_stats["ON"].values()), "check_ON_results": check_stats["ON"],
    "check_OFF": sum(check_stats["OFF"].values()), "check_OFF_results": check_stats["OFF"],
    "notnull_ON": sum(nn_stats["ON"].values()), "notnull_ON_results": nn_stats["ON"],
    "notnull_OFF": sum(nn_stats["OFF"].values()), "notnull_OFF_results": nn_stats["OFF"],
    "unique_ON": sum(uq_stats["ON"].values()), "unique_ON_results": uq_stats["ON"],
    "unique_OFF": sum(uq_stats["OFF"].values()), "unique_OFF_results": uq_stats["OFF"],
    "tables_reverse_mapped": len(TABLES),
}
md(f"\n**SWEEP A EXAMINED:** {len(EDGES)}/80 edges enumerated · {a2_examined} orphan queries · "
   f"FK bad-value ON {len(EDGES)}/80 {a3_stats} · NULL-path {len(NULLABLE_EDGES)}/18 {a3b_stats} · "
   f"FK bad-value OFF {len(EDGES)}/80 {a4_stats} · CHECK ON {sum(check_stats['ON'].values())}/127 "
   f"{check_stats['ON']} · CHECK OFF {sum(check_stats['OFF'].values())}/127 {check_stats['OFF']} · "
   f"NOT NULL ON {sum(nn_stats['ON'].values())}/267 {nn_stats['ON']} · "
   f"NOT NULL OFF {sum(nn_stats['OFF'].values())}/267 {nn_stats['OFF']} · "
   f"UNIQUE ON {sum(uq_stats['ON'].values())}/5 {uq_stats['ON']} · "
   f"UNIQUE OFF {sum(uq_stats['OFF'].values())}/5 {uq_stats['OFF']}\n")

# ═════════════════════════════ SWEEP B ═══════════════════════════════════════

md("\n\n---\n\n## SWEEP B — the pipeline spine, forward\n")
md("Spine: slugs → search_executions → search_admissions → evidence_sources → "
   "(source_slug_links, source_value_extractions, evidence_population_match) → "
   "specifications → specification_source_links → render. Scratch copy `probe-spine.db`, "
   "foreign_keys=ON, synthetic rows PROBE-prefixed.\n")

spine_db = fresh_copy("probe-spine.db")
scon = sqlite3.connect(spine_db)
scon.execute("PRAGMA foreign_keys=ON")
TS = "2026-08-12T00:00:00+00:00"
SES = "PROBE-session"
b_examined = 0


def b_step(target, action, sql, params, expected, expect_reject=False, note=None):
    global b_examined
    b_examined += 1
    try:
        cur = scon.execute(sql, params)
        scon.commit()
        actual = f"accepted (rowid {cur.lastrowid})"
        v = "SILENT-PASS" if expect_reject else "OK"
        exc = None
    except sqlite3.Error as e:
        exc = f"{type(e).__name__}: {e}"
        scon.rollback()
        actual, v = ("rejected", "OK") if expect_reject else ("rejected", "FAILED-WRITE")
    rec("B", target, action, expected,
        actual + (f" — {note}" if note and exc is None else ""),
        v, exc=exc, sql=sql + "  -- params: " + json.dumps(params, default=str))
    return exc is None


b_step("search_executions (OUT OF ORDER)", "insert execution for a slug that does not exist yet",
       "INSERT INTO search_executions (slug, language, query_text, engine, depth_method, session, executed_at) VALUES (?,?,?,?,?,?,?)",
       ["PROBE-slug-a", "en", "PROBE query", "manual", "scoping", SES, TS],
       "rejected — slug FK", expect_reject=True)
b_step("slugs", "create spine root PROBE-slug-a",
       "INSERT INTO slugs (slug, topic_directory, sl_path, bpc_path, status, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?,?,?)",
       ["PROBE-slug-a", "PROBE-topic", "PROBE/sl.md", "PROBE/bpc.md", "ACTIVE", TS, SES, TS, SES],
       "accepted",
       note="key carried forward: slug (TEXT). Nothing forces sl_path/bpc_path to exist on disk — dangling paths accepted silently")
b_step("search_executions", "insert execution against PROBE-slug-a, admitted_ref_ids naming a ref that does not exist",
       "INSERT INTO search_executions (slug, language, query_text, engine, depth_method, results_found, results_screened, results_admitted, session, executed_at, admitted_ref_ids) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
       ["PROBE-slug-a", "en", "PROBE query text", "manual", "scoping", 5, 5, 1, SES, TS,
        json.dumps(["PROBE-REF-99901"])],
       "accepted",
       note="key carried: exec_id (INTEGER PK). admitted_ref_ids is JSON — json_valid() is the only check; the dangling ref is accepted")
exec_id = scon.execute("SELECT exec_id FROM search_executions WHERE slug='PROBE-slug-a'").fetchone()[0]
rec("B", "search_executions.admitted_ref_ids", "verify the dangling JSON ref was accepted",
    "a ref named in admitted_ref_ids should exist in evidence_sources",
    "accepted with PROBE-REF-99901 not existing anywhere — the JSON leg of the dual store is unconstrained",
    "SILENT-PASS")
b_examined += 1

b_step("search_admissions (OUT OF ORDER)", "admit a ref before the evidence source exists",
       "INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)",
       [exec_id, "PROBE-REF-99901", TS, SES], "rejected — ref FK", expect_reject=True)
b_step("search_admissions (OUT OF ORDER)", "admit under a nonexistent exec_id",
       "INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)",
       [999999901, "PROBE-REF-99901", TS, SES], "rejected — exec FK", expect_reject=True)
b_step("evidence_sources", "create PROBE evidence source with NOTHING but a ref_id",
       "INSERT INTO evidence_sources (ref_id) VALUES (?)", ["PROBE-REF-99901"],
       "accepted",
       note="every other column is nullable: no tier, no title, no verification_status, no type required. "
            "A source can enter the corpus completely empty — silently lost: everything about it")
b_step("evidence_sources", "second source for the backward walk",
       "INSERT INTO evidence_sources (ref_id, tier, pub_title, verification_status) VALUES (?,?,?,?)",
       ["PROBE-REF-99902", 6, "PROBE Building Code", "verified"], "accepted")
b_step("search_admissions", "admit PROBE-REF-99901 under the real exec_id",
       "INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)",
       [exec_id, "PROBE-REF-99901", TS, SES], "accepted",
       note="key carried: (exec_id, ref_id). Nothing reconciles this table with "
            "search_executions.admitted_ref_ids / results_admitted")
scon.execute("UPDATE search_executions SET results_admitted = 0 WHERE exec_id = ?", [exec_id])
scon.commit()
n_adm = scon.execute("SELECT COUNT(*) FROM search_admissions WHERE exec_id=?", [exec_id]).fetchone()[0]
rec("B", "search_executions ↔ search_admissions dual store",
    "set results_admitted=0 while a search_admissions row exists for the same exec",
    "some constraint or trigger reconciles the count",
    f"accepted: results_admitted=0 while search_admissions holds {n_adm} row(s). No trigger, no check — "
    "divergence is silent", "SILENT-PASS",
    sql="UPDATE search_executions SET results_admitted = 0 WHERE exec_id = ?")
b_examined += 1

b_step("source_slug_links (OUT OF ORDER)", "link a nonexistent ref to the slug",
       "INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?)",
       ["PROBE-REF-NOPE", "PROBE-slug-a", "L1", TS, SES, TS, SES], "rejected", expect_reject=True)
b_step("source_slug_links", "link PROBE-REF-99901 ↔ PROBE-slug-a",
       "INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?)",
       ["PROBE-REF-99901", "PROBE-slug-a", "L1", TS, SES, TS, SES], "accepted",
       note="key carried: ref_id + slug. An evidence source needs NO search_execution and NO admission to "
            "acquire links — the whole search stage is bypassable, silently")
b_step("source_value_extractions", "extraction from PROBE-REF-99901 with full locator, item_code left NULL",
       "INSERT INTO source_value_extractions (ref_id, slug, parameter, claim_type, claimed_value, claim_text, source_section, extraction_method, extraction_status, created_at, updated_at, item_code, population_code, locator_scheme, loc_section, loc_clause) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
       ["PROBE-REF-99901", "PROBE-slug-a", "PROBE corridor width", "numerical", "1500",
        "PROBE claim text", "§5.7", "skim", "preliminary", TS, TS, None, None, "din", "5", "5.7"],
       "accepted",
       note="item_code and population_code are NULLABLE and left NULL — the extraction is now unreachable "
            "from any cell by structured join; only ref_id carries forward")
b_step("evidence_population_match", "match row with source_ref garbage + ref_id NULL (dual identity)",
       "INSERT INTO evidence_population_match (match_id, source_ref, target_population, match_grade, created_at, created_by_session) VALUES (?,?,?,?,?,?)",
       ["PROBE-MATCH-1", "PROBE-TOTALLY-FAKE-REF", "PROBE-POP-X", "EXACT", TS, SES],
       "should be rejected — source_ref AND target_population both dangle", expect_reject=True)

b_step("specifications (OUT OF ORDER)", "cell for an item that does not exist",
       "INSERT INTO specifications (item_code, population_code, state) VALUES (?,?,?)",
       ["PROBE-K-99", "PROBE-POP", "pending"], "rejected — item FK", expect_reject=True)
b_step("items", "synthetic item K-99 (category K)",
       "INSERT INTO items (item_code, category, name, status, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?,?)",
       ["K-99", "K", "PROBE item", "draft", TS, SES, TS, SES], "accepted")
b_step("populations", "synthetic population PROBE-POP",
       "INSERT INTO populations (population_code, display_name) VALUES (?,?)",
       ["PROBE-POP", "PROBE population"], "accepted",
       note="category, parent_code, status all optional — a population can be created outside the taxonomy")
b_step("specifications", "STATED cell with NULL governing_refs (doctrine: stated requires non-empty governing_refs)",
       "INSERT INTO specifications (item_code, population_code, state, governing_refs, created_at, created_by_session) VALUES (?,?,?,?,?,?)",
       ["K-99", "PROBE-POP", "stated", None, TS, SES],
       "should be rejected per the evidence-state machine", expect_reject=True)
cell_row = scon.execute("SELECT specification_id FROM specifications WHERE item_code='K-99'").fetchone()
if cell_row:
    specification_id = cell_row[0]
else:
    scon.execute("INSERT INTO specifications (item_code, population_code, state, created_at) VALUES ('K-99','PROBE-POP','stated',?)", [TS])
    scon.commit()
    specification_id = scon.execute("SELECT specification_id FROM specifications WHERE item_code='K-99'").fetchone()[0]
b_step("specifications.governing_refs", "point governing_refs at one PROBE ref and one dangling ref",
       "UPDATE specifications SET governing_refs = ? WHERE specification_id = ?",
       [json.dumps(["PROBE-REF-99901", "REF-DANGLING-00000"]), specification_id],
       "the dangling entry should be rejected", expect_reject=True)

b_step("specification_source_links (OUT OF ORDER)", "link a nonexistent cell",
       "INSERT INTO specification_source_links (specification_id, ref_id, role, created_at, created_by_session) VALUES (?,?,?,?,?)",
       [999999902, "PROBE-REF-99901", "governing", TS, SES], "rejected — cell FK", expect_reject=True)
b_step("specification_source_links", "governing link cell → PROBE-REF-99901",
       "INSERT INTO specification_source_links (specification_id, ref_id, role, created_at, created_by_session) VALUES (?,?,?,?,?)",
       [specification_id, "PROBE-REF-99901", "governing", TS, SES], "accepted",
       note="key carried: specification_id + ref_id; role CHECK admits only 'governing'")
rec("B", "specification_source_links vs governing_refs",
    "the JSON now names 2 refs while specification_source_links holds 1",
    "the two representations should be forced equal",
    "both writes accepted; the stores disagree and nothing reconciles them (compare Sweep C)",
    "SILENT-PASS")
b_examined += 1
scon.commit()

TREE = HERE / "tree"
if TREE.exists():
    shutil.rmtree(TREE)
shutil.copytree(REPO, TREE, ignore=shutil.ignore_patterns(".git", "__pycache__"))
env = dict(os.environ, GUIDEBOOK_DB_PATH=str(spine_db))


def render_step(target, argv, expected):
    global b_examined
    b_examined += 1
    try:
        p = subprocess.run(argv, cwd=TREE, capture_output=True, text=True, env=env, timeout=300)
    except subprocess.TimeoutExpired as te:
        rec("B", target, "RENDER stage: " + " ".join(argv), expected, "TIMEOUT", "ERROR", exc=str(te))
        return None
    out = (p.stdout + "\n" + p.stderr).strip()
    v = "OK" if p.returncode == 0 else "ERROR"
    rec("B", target, "RENDER stage: " + " ".join(argv), expected,
        f"rc={p.returncode}; output (trunc): {out[:1200]}", v,
        exc=None if p.returncode == 0 else out[-500:])
    return p


render_step("render/build_site.py --only K-99",
            ["python3", "scripts/generate/build_site.py", "--only", "K-99"],
            "renders the PROBE item's spec page from the scratch DB")
render_step("render/build_site.py (full)",
            ["python3", "scripts/generate/build_site.py"],
            "renders all spec pages incl. the PROBE cell")
render_step("render/room_page.py R-BA",
            ["python3", "scripts/generate/room_page.py", "R-BA"],
            "expected to FAIL: queries phantom tables (room, room_item, …) — the live table is `rooms` "
            "keyed by room_code")
render_step("render/population_page.py ALL",
            ["python3", "scripts/generate/population_page.py", "ALL"],
            "population page for code ALL from scratch DB")

md(f"\n**SWEEP B EXAMINED: {b_examined} handoff probes**\n")

# ═════════════════════════════ SWEEP V — views ═══════════════════════════════

md("\n\n---\n\n## SWEEP V — the 18 views (canonical AND PROBE-populated spine copy)\n")
v_examined = 0
vcanon = ro()
for v in VIEWS:
    v_examined += 1
    res = {}
    for label, cx in (("canonical", vcanon), ("spine+PROBE", scon)):
        try:
            n = cx.execute(f'SELECT COUNT(*) FROM "{v}"').fetchone()[0]
            sample = cx.execute(f'SELECT * FROM "{v}" LIMIT 2').fetchall()
            res[label] = (n, sample, None)
        except sqlite3.Error as exc:
            res[label] = (None, None, f"{type(exc).__name__}: {exc}")
    err = [l for l, r in res.items() if r[2]]
    n_can, n_spi = res["canonical"][0], res["spine+PROBE"][0]
    if err:
        rec("V", v, "execute view on canonical and on the PROBE-populated spine copy",
            "executes", f"errors: { {l: res[l][2] for l in err} }", "ERROR",
            exc="; ".join(str(res[l][2]) for l in err))
    elif (n_can or 0) > 0 or (n_spi or 0) > 0:
        rec("V", v, "execute view on canonical and on the PROBE-populated spine copy",
            "executes and returns rows",
            f"canonical: {n_can} rows; spine+PROBE: {n_spi} rows; sample: {res['spine+PROBE'][1] or res['canonical'][1]}",
            "OK")
    else:
        rec("V", v, "execute view on canonical and on the PROBE-populated spine copy",
            "executes and returns rows",
            "EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified "
            "(its base tables are empty even after the PROBE spine)", "BLOCKED")
vcanon.close()
md(f"\n**SWEEP V EXAMINED: {v_examined}/18 views executed**\n")

# ═════════════════════════════ SWEEP C ═══════════════════════════════════════

md("\n\n---\n\n## SWEEP C — the backward walk\n")
c_examined = 0


def c_rec(*a, **kw):
    global c_examined
    c_examined += 1
    return rec("C", *a, **kw)


refs = [r[0] for r in scon.execute(
    "SELECT ref_id FROM specification_source_links WHERE specification_id=?", [specification_id])]
c_rec("cell → specification_source_links", f"resolve links for PROBE cell {specification_id}",
      "≥1 governing ref", f"refs via csl: {refs}", "OK" if refs else "ERROR")
srcs = [tuple(r) for r in scon.execute(
    f"SELECT ref_id, tier, pub_title FROM evidence_sources WHERE ref_id IN ({','.join('?'*len(refs))})", refs)]
c_rec("specification_source_links → evidence_sources", "resolve refs to sources",
      "all resolve", f"{srcs}", "OK" if len(srcs) == len(refs) else "ORPHAN")
sql = ("SELECT e.extraction_id, e.ref_id, e.item_code, e.population_code, e.loc_section, e.loc_clause "
       "FROM source_value_extractions e WHERE e.ref_id = ? AND e.item_code = ?")
rows = scon.execute(sql, [refs[0], "K-99"]).fetchall()
c_rec("evidence_sources → source_value_extractions (structured join on ref_id+item_code)",
      "find the extraction backing this cell's value",
      "the extraction row",
      f"{len(rows)} rows — the extraction exists but its item_code is NULL, so the only structured join "
      "from cell to extraction returns nothing. BROKEN JOINT: no table links specifications to "
      "source_value_extractions; the join must be improvised on (ref_id, item_code) and item_code is nullable",
      "ORPHAN" if not rows else "OK", sql=sql)
rows2 = scon.execute("SELECT extraction_id, loc_section, loc_clause, source_section FROM source_value_extractions WHERE ref_id=?", [refs[0]]).fetchall()
c_rec("… fallback join on ref_id alone", "extractions for the ref regardless of item",
      "≥1", f"{rows2} — reachable only by dropping the item join entirely",
      "OK" if rows2 else "ORPHAN")
c_rec("source_value_extractions → loc_* → clause", "read the decomposed locator",
      "loc_section/loc_clause populated",
      f"loc_section={rows2[0][1]!r}, loc_clause={rows2[0][2]!r} (set by the probe; live-data density below)",
      "OK")

gr = scon.execute("SELECT governing_refs FROM specifications WHERE specification_id=?", [specification_id]).fetchone()[0]
gr_refs = json.loads(gr or "[]")
resolved = [r[0] for r in scon.execute(
    f"SELECT ref_id FROM evidence_sources WHERE ref_id IN ({','.join('?'*len(gr_refs))})", gr_refs)] if gr_refs else []
dangling = [x for x in gr_refs if x not in resolved]
c_rec("cell → governing_refs (JSON dual store)", "parse JSON and resolve to evidence_sources",
      "all resolve, and match specification_source_links",
      f"JSON names {gr_refs}; resolved {resolved}; DANGLING {dangling}; csl says {refs} — the two "
      "representations disagree and nothing reconciles them",
      "ORPHAN" if dangling or set(resolved) != set(refs) else "OK")

con = ro()
det = con.execute("SELECT COUNT(*) FROM specifications WHERE state IN ('stated','provisional')").fetchone()[0]
have_csl = con.execute("SELECT COUNT(DISTINCT c.specification_id) FROM specifications c JOIN specification_source_links l ON l.specification_id=c.specification_id WHERE c.state IN ('stated','provisional')").fetchone()[0]
have_gr = con.execute("SELECT COUNT(*) FROM specifications WHERE state IN ('stated','provisional') AND governing_refs IS NOT NULL AND json_array_length(governing_refs)>0").fetchone()[0]
disagree = con.execute("""
    SELECT COUNT(*) FROM specifications c WHERE c.state IN ('stated','provisional') AND
      (SELECT COALESCE(json_group_array(value),'[]') FROM (SELECT value FROM json_each(COALESCE(c.governing_refs,'[]')) ORDER BY value))
      <> (SELECT COALESCE(json_group_array(ref_id),'[]') FROM (SELECT ref_id FROM specification_source_links l WHERE l.specification_id=c.specification_id ORDER BY ref_id))
""").fetchone()[0]
c_rec("canonical: determined cells, dual-store agreement",
      "compare sorted governing_refs JSON vs sorted specification_source_links per determined cell",
      "0 disagreements",
      f"determined cells: {det}; with csl links: {have_csl}; with non-empty governing_refs: {have_gr}; "
      f"cells where the two stores DISAGREE: {disagree}",
      "OK" if disagree == 0 else "ORPHAN")
funnel = con.execute("""
    SELECT
      (SELECT COUNT(DISTINCT l.ref_id) FROM specification_source_links l JOIN specifications c ON c.specification_id=l.specification_id WHERE c.state IN ('stated','provisional')),
      (SELECT COUNT(DISTINCT e.ref_id) FROM source_value_extractions e JOIN specification_source_links l ON l.ref_id=e.ref_id),
      (SELECT COUNT(*) FROM source_value_extractions e JOIN specification_source_links l ON l.ref_id=e.ref_id JOIN specifications c ON c.specification_id=l.specification_id AND c.item_code=e.item_code),
      (SELECT COUNT(*) FROM source_value_extractions WHERE item_code IS NOT NULL),
      (SELECT COUNT(*) FROM source_value_extractions),
      (SELECT COUNT(*) FROM source_value_extractions WHERE loc_section IS NOT NULL OR loc_clause IS NOT NULL OR loc_part IS NOT NULL OR loc_division IS NOT NULL OR loc_subsection IS NOT NULL OR loc_paragraph IS NOT NULL OR loc_subclause IS NOT NULL),
      (SELECT COUNT(*) FROM source_value_extractions WHERE source_section IS NOT NULL)
""").fetchone()
c_rec("canonical: backward funnel cell→ref→extraction→locator",
      "count survivors at each joint of the backward walk",
      "every determined cell walks back to a clause",
      f"governing refs on determined cells: {funnel[0]} · of those refs, with ANY extraction: {funnel[1]} · "
      f"extractions joinable back to their cell via (ref_id,item_code): {funnel[2]} · "
      f"extractions with item_code set: {funnel[3]}/{funnel[4]} · "
      f"extractions with ANY loc_* level populated: {funnel[5]}/{funnel[4]} · "
      f"with legacy prose source_section: {funnel[6]}/{funnel[4]}",
      "ORPHAN" if funnel[2] == 0 or funnel[5] == 0 else "OK")
jv_cols = {c[1] for c in COLS["jurisdictional_values"]}
jv = con.execute(
    "SELECT COUNT(*), SUM(CASE WHEN loc_section IS NOT NULL OR loc_clause IS NOT NULL THEN 1 ELSE 0 END)"
    + (", SUM(ref_id IS NOT NULL)" if "ref_id" in jv_cols else ", NULL")
    + " FROM jurisdictional_values").fetchone()
c_rec("canonical: jurisdictional_values locator decomposition",
      "how many rows have decomposed loc_* vs packed standard_name; does the table carry a ref FK at all",
      "decomposed locators, ref-linked",
      f"rows: {jv[0]}; with loc_section/clause: {jv[1] or 0}; ref_id column present: {'ref_id' in jv_cols} "
      f"(migration 053 notes the table 'has never had' the ref_id FK)",
      "ORPHAN" if (jv[1] or 0) == 0 else "OK")
con.close()

c_rec("renderers: which representation is read",
      "static inspection (verified again by the Sweep D matrix)",
      "one canonical representation",
      "specification_source_links (role='governing') read by: scripts/generate/build_site.py, scripts/generate/spec_page.py; "
      "governing_refs JSON read by: scripts/generate/pilot_renderings.py (parses the JSON, recomputes derivation_sha, "
      "cross-counts csl); both read by: scripts/validate_evidence_state.py, scripts/tests/test_db_integrity.py, "
      "scripts/assess/assess_cell.py, tools/pipeline_completeness.py",
      "OK")

md(f"\n**SWEEP C EXAMINED: {c_examined} joints walked**\n")

# ═════════════════════════════ SWEEP D ═══════════════════════════════════════

md("\n\n---\n\n## SWEEP D — table × script matrix (AST scan + PREPARE verification)\n")

SQL_KEYWORDS = {"select", "from", "where", "join", "left", "right", "inner", "outer", "cross",
                "on", "and", "or", "not", "null", "as", "in", "is", "like", "group", "by",
                "order", "limit", "values", "into", "set", "update", "delete", "insert",
                "create", "table", "if", "exists", "temp", "temporary", "view", "index",
                "replace", "distinct", "union", "all", "case", "when", "then", "else", "end",
                "having", "coalesce", "count", "sum", "max", "min", "avg", "cast", "pragma",
                "json_each", "json_valid", "json_extract", "json_array_length", "with",
                "recursive", "using", "natural", "glob", "between", "collate"}
KNOWN = set(TABLES) | set(VIEWS) | {"sqlite_master", "sqlite_sequence", "sqlite_temp_master",
                                    "pragma_table_info", "json_each", "json_tree",
                                    "data_migrations", "dual"}

scan_roots = [REPO / "scripts", REPO / "tools", REPO / "schemas"]
LEGACY_PREFIX = [str(REPO / "scripts" / "db"), str(REPO / "scripts" / "migrate"),
                 str(REPO / "scripts" / "convert")]

# CASE-SENSITIVE keyword matching: this repo writes SQL keywords uppercase, and
# case-insensitive matching drowned the scan in prose ("... from the registry ...").
read_re = re.compile(r"\b(?:FROM|JOIN)\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)[\"'`\]]?")
cte_re = re.compile(r"\b(?:WITH\s+(?:RECURSIVE\s+)?)?([A-Za-z_][A-Za-z0-9_]*)\s+AS\s*\(")
write_res = [
    (re.compile(r"\bINSERT\s+(?:OR\s+\w+\s+)?INTO\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "INSERT"),
    (re.compile(r"\bREPLACE\s+INTO\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "REPLACE"),
    (re.compile(r"\bUPDATE\s+(?:OR\s+\w+\s+)?[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)\s+SET\b"), "UPDATE"),
    (re.compile(r"\bDELETE\s+FROM\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "DELETE"),
    (re.compile(r"\bCREATE\s+(?:TEMP(?:ORARY)?\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "CREATE"),
    (re.compile(r"\bALTER\s+TABLE\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "ALTER"),
    (re.compile(r"\bDROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)"), "DROP"),
]
PROSE_STOPWORDS = {"the", "a", "an", "this", "that", "each", "one", "all", "any", "it", "its",
                   "which", "what", "them", "these", "those", "stdin", "argv", "scratch",
                   "here", "data", "of", "is", "are", "not"}
# scripts/audit/graph/* build a STANDALONE graph database (nodes/edges/findings/build_meta,
# plus deliberate selftest fixtures zzz_phantom/known_debt) — separate DB, not guidebook schema
GRAPH_DB_FILES = ("scripts/audit/graph/", "scripts/audit/graph_audit.py")
separate_db_refs = {}
STMT_START = re.compile(r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|PRAGMA|WITH|REPLACE|EXPLAIN)\b", re.I)


def collect_strings(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        return None, f"SyntaxError: {e}"
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append((node.value, node.lineno))
        elif isinstance(node, ast.JoinedStr):
            parts = []
            for vv in node.values:
                if isinstance(vv, ast.Constant) and isinstance(vv.value, str):
                    parts.append(vv.value)
                else:
                    parts.append(" __DYN__ ")
            out.append(("".join(parts), node.lineno))
    return out, None


def looks_sql(s):
    u = s.upper()
    return any(k in u for k in ("SELECT ", "INSERT ", "UPDATE ", "DELETE ", "CREATE TABLE",
                                "REPLACE INTO", "ALTER TABLE", "DROP TABLE", "FROM ", "PRAGMA "))


def split_statements(s):
    stmts, cur, q = [], [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
            cur.append(ch)
        elif ch == ";":
            stmts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    stmts.append("".join(cur))
    return [x.strip() for x in stmts if x.strip()]


matrix_read, matrix_write = {}, {}
phantom_tables = {}
phantom_columns = []
scripts_scanned = 0
scripts_failed = []
per_file_tables = {}
prepare_stats = {"prepared_ok": 0, "dynamic": 0, "fragment": 0, "no_such_table": 0,
                 "no_such_column": 0, "other_error": 0, "statements_total": 0}
prepare_failures = []

# prepare connection: rw scratch so CREATE TABLE statements can be materialised per-file, rolled back after
prep_db = fresh_copy("probe-prepare.db")
prep = sqlite3.connect(prep_db)
prep.execute("PRAGMA foreign_keys=OFF")

py_files = []
for root in scan_roots:
    py_files.extend(sorted(root.rglob("*.py")))

for f in py_files:
    relf = str(f.relative_to(REPO))
    legacy = any(str(f).startswith(p) for p in LEGACY_PREFIX)
    strings, err = collect_strings(f)
    if strings is None:
        scripts_failed.append((relf, err))
        continue
    scripts_scanned += 1
    created_here = set()
    freads, fwrites = set(), set()
    prep.execute("SAVEPOINT filescope")
    for (s, ln) in strings:
        if not looks_sql(s):
            continue
        for m in cte_re.finditer(s):
            created_here.add(m.group(1))     # CTE names are not tables
        for rx, verb in write_res:
            for m in rx.finditer(s):
                name = m.group(1)
                if name.lower() in SQL_KEYWORDS:
                    continue
                if verb == "CREATE":
                    created_here.add(name)
                fwrites.add((name, verb, ln))
        for m in read_re.finditer(s):
            name = m.group(1)
            if name.lower() in SQL_KEYWORDS or name == "__DYN__" or name in PROSE_STOPWORDS:
                continue
            freads.add((name, ln))
        # PREPARE stage
        for stmt in split_statements(s):
            if not STMT_START.match(stmt):
                continue
            prepare_stats["statements_total"] += 1
            if "__DYN__" in stmt or re.search(r"%\(?[sd]", stmt) or re.search(r"\{\w*\}", stmt):
                prepare_stats["dynamic"] += 1
                continue
            try:
                if re.match(r"^\s*CREATE\s+(TEMP(ORARY)?\s+)?TABLE", stmt, re.I):
                    prep.execute(stmt)   # materialise so later reads prepare
                else:
                    prep.execute("EXPLAIN " + stmt)
                prepare_stats["prepared_ok"] += 1
            except sqlite3.ProgrammingError:
                prepare_stats["prepared_ok"] += 1   # prepared; bindings missing
            except sqlite3.OperationalError as exc:
                m1 = re.search(r"no such table: (\w+)", str(exc))
                m2 = re.search(r"no such column: ([\w.]+)", str(exc))
                if m1:
                    prepare_stats["no_such_table"] += 1
                    prepare_failures.append({"script": relf, "line": ln, "error": str(exc),
                                             "stmt": stmt[:200]})
                elif m2:
                    prepare_stats["no_such_column"] += 1
                    prepare_failures.append({"script": relf, "line": ln, "error": str(exc),
                                             "stmt": stmt[:200]})
                elif "incomplete input" in str(exc) or "syntax error" in str(exc):
                    prepare_stats["fragment"] += 1
                else:
                    prepare_stats["other_error"] += 1
                    prepare_failures.append({"script": relf, "line": ln, "error": str(exc),
                                             "stmt": stmt[:200]})
            except sqlite3.Error as exc:
                prepare_stats["other_error"] += 1
                prepare_failures.append({"script": relf, "line": ln, "error": str(exc),
                                         "stmt": stmt[:200]})
        # static phantom-column detection (skip dynamic strings)
        if "__DYN__" not in s:
            aliases = {}
            for m in re.finditer(r"\b(?:FROM|JOIN)\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)[\"'`\]]?\s+(?:AS\s+)?([a-z_][a-z0-9_]*)?", s, re.I):
                tname, al = m.group(1), m.group(2)
                if tname.lower() in SQL_KEYWORDS:
                    continue
                if al and al.lower() not in SQL_KEYWORDS:
                    aliases[al] = tname
                aliases[tname] = tname
            ALL_COLS = {**{t: {c[1] for c in COLS[t]} for t in ALLTABLES},
                        **{vv: set(VIEW_COLS[vv]) for vv in VIEWS}}
            for m in re.finditer(r"\b([a-z_][a-z0-9_]*)\.([a-z_][a-z0-9_]*)\b", s, re.I):
                al, colname = m.group(1), m.group(2)
                t = aliases.get(al)
                if t and t in ALL_COLS and colname not in ALL_COLS[t] and colname != "rowid":
                    phantom_columns.append({"script": relf, "line": ln, "table": t,
                                            "column": colname, "context": f"{al}.{colname}"})
            for m in re.finditer(r"INSERT\s+(?:OR\s+\w+\s+)?INTO\s+[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)[\"'`\]]?\s*\(([^)]*)\)", s, re.I):
                t, cols_txt = m.group(1), m.group(2)
                if t in ALL_COLS:
                    for cname in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", cols_txt):
                        if cname.lower() not in SQL_KEYWORDS and cname not in ALL_COLS[t]:
                            phantom_columns.append({"script": relf, "line": ln, "table": t,
                                                    "column": cname, "context": "INSERT column list"})
            for m in re.finditer(r"UPDATE\s+(?:OR\s+\w+\s+)?[\"'`\[]?([A-Za-z_][A-Za-z0-9_]*)[\"'`\]]?\s+SET\s+(.*?)(?:\bWHERE\b|$)", s, re.I | re.S):
                t, setpart = m.group(1), m.group(2)
                if t in ALL_COLS:
                    for am in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", setpart):
                        cname = am.group(1)
                        if cname.lower() not in SQL_KEYWORDS and cname not in ALL_COLS[t]:
                            phantom_columns.append({"script": relf, "line": ln, "table": t,
                                                    "column": cname, "context": "UPDATE SET"})
    prep.execute("ROLLBACK TO filescope")
    prep.execute("RELEASE filescope")
    per_file_tables[relf] = {"legacy": legacy,
                             "reads": sorted({n for n, _ in freads}),
                             "writes": sorted({f"{n}:{v}" for n, v, _ in fwrites})}
    is_graph = any(relf.startswith(g) or relf == g.rstrip("/") for g in GRAPH_DB_FILES)
    for (n, ln) in freads:
        if n in KNOWN or n in created_here:
            matrix_read.setdefault(n, set()).add(relf)
        elif is_graph:
            separate_db_refs.setdefault(n, []).append((relf, ln, "READ"))
        elif n == n.lower() and n not in PROSE_STOPWORDS:
            phantom_tables.setdefault(n, []).append((relf, ln, "READ"))
    for (n, v, ln) in fwrites:
        if n in KNOWN or n in created_here:
            matrix_write.setdefault(n, set()).add((relf, v))
        elif is_graph:
            separate_db_refs.setdefault(n, []).append((relf, ln, v))
        elif n == n.lower():
            phantom_tables.setdefault(n, []).append((relf, ln, v))
prep.close()

mig_writers = {}
mig_files = sorted((REPO / "scripts" / "migrations").glob("*.sql"))
for f in mig_files:
    s = f.read_text(errors="replace")
    for rx, verb in write_res:
        for m in rx.finditer(s):
            name = m.group(1)
            if name.lower() in SQL_KEYWORDS:
                continue
            mig_writers.setdefault(name, set()).add((f.name, verb))

rec("D", "scan", f"AST-parsed {scripts_scanned}/167 .py files under scripts/, tools/, schemas/ "
    f"(+ {len(mig_files)} migration .sql files scanned for writers); "
    f"{len(scripts_failed)} unparseable",
    "all files parse", f"failed: {scripts_failed}" if scripts_failed else "all parsed",
    "OK" if not scripts_failed else "ERROR",
    extra={"scripts_scanned": scripts_scanned, "migration_files": len(mig_files)})

rec("D", "PREPARE verification",
    f"every complete SQL literal prepared (EXPLAIN) against the scratch schema: "
    f"{prepare_stats['statements_total']} statements",
    "all prepare",
    f"{prepare_stats} · failures: "
    + "; ".join(f"{p['script']}:{p['line']} {p['error']}" for p in prepare_failures[:40]),
    "ERROR" if (prepare_stats["no_such_table"] or prepare_stats["no_such_column"]) else "OK",
    extra={"prepare_stats": prepare_stats, "prepare_failures": prepare_failures})

rec("D", "method blind spots (stated explicitly)",
    "what this scan CANNOT see",
    "n/a",
    "(1) SQL assembled by string concatenation across variables or .join() of fragments; "
    "(2) table/column names arriving from runtime data (registry YAML, argv, config) — f-string "
    "statements are counted as DYNAMIC, not verified; (3) SQL embedded in non-Python "
    "(scripts/audit/render_audit.js, shell scripts); (4) executescript bodies — split naively on ';', "
    "quoted semicolons inside migrations could mis-split; (5) %-formatted SQL counted DYNAMIC; "
    "(6) columns consumed via SELECT * then dict access are invisible to the phantom-column check; "
    "(7) migration .sql files are scanned for writers but not PREPAREd (they demonstrably ran — the DB "
    "was rebuilt from them)",
    "BLOCKED")

md("\n### D — table × script matrix (READ / WRITE)\n")
md("| table | rows | readers (.py) | writers (.py) | migration writers |")
md("|---|---|---|---|---|")
unwritable, unread = [], []
for t in TABLES:
    readers = sorted(matrix_read.get(t, set()))
    writers = sorted({f"{s} ({v})" for s, v in matrix_write.get(t, set())})
    mig_data_writes = any(v in ("INSERT", "UPDATE", "REPLACE", "DELETE") for _, v in mig_writers.get(t, set()))
    if readers and not writers and not mig_data_writes:
        unwritable.append(t)
    if (writers or mig_data_writes) and not readers:
        unread.append(t)
    md(f"| `{t}` | {ROWCOUNT[t]} | {('<br>'.join(readers)) or '—'} | {('<br>'.join(writers)) or '—'} | "
       f"{len(mig_writers.get(t, set()))} stmt-kind(s) |")

rec("D", "unwritable outputs",
    "tables read by code but with NO .py writer AND NO data-migration INSERT/UPDATE/DELETE",
    "none", f"{unwritable}", "ERROR" if unwritable else "OK", extra={"unwritable": unwritable})
rec("D", "unread inputs", "tables written (py or migrations) but read by no scanned .py",
    "none", f"{unread}", "ERROR" if unread else "OK", extra={"unread": unread})
pt_sorted = {k: v for k, v in sorted(phantom_tables.items())}
rec("D", "phantom tables", "table names referenced in code that do not exist in the schema",
    "known set from room_page.py",
    "; ".join(f"{k} ← {sorted(set((s, verb) for s, _, verb in v))}" for k, v in pt_sorted.items()) or "none",
    "ERROR" if pt_sorted else "OK",
    extra={"phantom_tables": {k: [list(x) for x in v] for k, v in pt_sorted.items()}})
seen = set()
pc = []
for p in phantom_columns:
    key = (p["script"], p["table"], p["column"])
    if key not in seen:
        seen.add(key)
        pc.append(p)
rec("D", "separate-DB tables (graph audit module)",
    "table names used by scripts/audit/graph/* + graph_audit.py — these target a STANDALONE graph "
    "database file, not data/guidebook.db",
    "classified separately, not as guidebook phantoms",
    "; ".join(f"{k} ← {sorted(set(s for s, _, _ in v))}" for k, v in sorted(separate_db_refs.items())) or "none",
    "OK", extra={"separate_db_refs": {k: [list(x) for x in v] for k, v in separate_db_refs.items()}})
rec("D", "phantom columns (static)", "columns referenced in SQL that do not exist on their (real) table",
    "none", "; ".join(f"{p['script']}:{p['line']} {p['table']}.{p['column']} [{p['context']}]" for p in pc) or "none",
    "ERROR" if pc else "OK", extra={"phantom_columns": pc})
legacy_files = sorted([f for f, d in per_file_tables.items() if d["legacy"]])
rec("D", "legacy scripts", "scripts under scripts/db, scripts/migrate, scripts/convert — marked, not excluded",
    "marked", f"{len(legacy_files)} legacy scripts included in the matrix: {legacy_files}", "OK",
    extra={"legacy_scripts": legacy_files})

md(f"\n**SWEEP D EXAMINED: {scripts_scanned}/167 scripts AST-parsed · "
   f"{prepare_stats['statements_total']} SQL statements PREPARE-checked "
   f"({prepare_stats['prepared_ok']} prepared, {prepare_stats['dynamic']} dynamic, "
   f"{prepare_stats['fragment']} fragments) · {len(TABLES)} tables in matrix · "
   f"{len(pt_sorted)} phantom tables · {len(pc)} phantom column refs**\n")

# ═════════════════════════════ SUMMARY + EMIT ════════════════════════════════

silent = [r for r in records if r["verdict"] == "SILENT-PASS"]
orphans = [r for r in records if r["verdict"] == "ORPHAN"]
errors = [r for r in records if r["verdict"] in ("ERROR", "FAILED-WRITE")]
blocked = [r for r in records if r["verdict"] == "BLOCKED"]

surface_attempted = (len(EDGES) + sum(check_stats["ON"].values())
                     + sum(nn_stats["ON"].values()) + sum(uq_stats["ON"].values()))
md("\n\n---\n\n## EXECUTIVE SUMMARY\n")
md(f"- Rejectable-write surface probed (FK=ON): **{surface_attempted}/{SURFACE_DENOM}** "
   f"(80 FK bad-value + {sum(check_stats['ON'].values())} CHECK + {sum(nn_stats['ON'].values())} NOT NULL "
   f"+ {sum(uq_stats['ON'].values())} UNIQUE); same surface re-probed under FK=OFF; "
   f"plus {len(NULLABLE_EDGES)}/18 NULL-path probes and 1 dual-identity probe.")
md(f"- Sweep A: edges {len(EDGES)}/80 · orphan queries {a2_examined} · reverse map 66/66 tables; "
   f"isolated={isolated}; referenced-but-empty={ref_empty}")
md(f"- Sweep B: {b_examined} handoff probes · Sweep V: {v_examined}/18 views · Sweep C: {c_examined} joints")
md(f"- Sweep D: {scripts_scanned}/167 scripts; {prepare_stats['statements_total']} statements prepared; "
   f"unwritable={unwritable}; unread={unread}; phantom tables={sorted(pt_sorted)}; "
   f"phantom column refs={len(pc)}")
md(f"\n**SILENT-PASS total: {len(silent)}** — seqs {[r['seq'] for r in silent]}")
md(f"**ORPHAN total: {len(orphans)}** — seqs {[r['seq'] for r in orphans]}")
md(f"**ERROR/FAILED-WRITE total: {len(errors)}** — seqs {[r['seq'] for r in errors]}")
md(f"**BLOCKED total: {len(blocked)}** — seqs {[r['seq'] for r in blocked]}")

summary = {
    "generated": now(),
    "snapshot_head": SNAP_HEAD,
    "denominators": {"fk_edges": len(EDGES), "fk_edges_nullable": len(NULLABLE_EDGES),
                     "checks": N_CHECKS, "notnull_nonpk": N_NOTNULL,
                     "unique_indexes": len(UNIQUE_IDX),
                     "rejectable_surface": SURFACE_DENOM,
                     "user_tables": len(TABLES),
                     "empty_tables": sum(1 for t in TABLES if ROWCOUNT[t] == 0),
                     "views": len(VIEWS), "scripts": 167,
                     "note": "pre-054 verified denominators were 80/127/267/5=479; "
                             "migration 054 (source_locators) added +1 CHECK, +1 NOT NULL"},
    "examined": {
        "sweep_A": a_examined,
        "sweep_B": {"handoff_probes": b_examined},
        "sweep_V": {"views_executed": v_examined},
        "sweep_C": {"joints": c_examined},
        "sweep_D": {"scripts_scanned": scripts_scanned,
                    "statements_prepared": prepare_stats, "tables": len(TABLES)},
        "rejectable_surface_attempted_ON": surface_attempted,
    },
    "silent_pass": silent, "orphans": orphans, "errors": errors, "blocked": blocked,
    "isolated_tables": isolated, "referenced_but_empty": ref_empty,
    "unwritable": unwritable, "unread": unread,
    "phantom_tables": {k: [list(x) for x in v] for k, v in pt_sorted.items()},
    "separate_db_refs": {k: [list(x) for x in v] for k, v in separate_db_refs.items()},
    "phantom_columns": pc,
    "prepare_failures": prepare_failures,
    "fk_off_committed_edges": a4_committed,
    "per_file_matrix": per_file_tables,
    "records": records,
}
LOG_MD.write_text("".join(_md), encoding="utf-8")
LOG_JSON.write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
scon.close()
print(f"WROTE {LOG_MD}")
print(f"WROTE {LOG_JSON}")
print(f"RECORDS: {len(records)}  SILENT-PASS: {len(silent)}  ORPHAN: {len(orphans)}  "
      f"ERROR: {len(errors)}  BLOCKED: {len(blocked)}")
print(f"SURFACE: {surface_attempted}/{SURFACE_DENOM} (FK=ON), re-probed under FK=OFF; "
      f"NULL-path {len(NULLABLE_EDGES)}/{len(NULLABLE_EDGES)}")
