#!/usr/bin/env python3
"""Regenerate the pipeline dossier from the live repo. Reads only; writes to OUT.

Rule 7a: every figure in the output is computed here, never typed. Re-run to refresh.
    python3 -I scratchpad/<STEM>/build_dossier.py
Stage attribution of code is DERIVED (which stage's tables a unit names), not judged;
table->stage is governance/stage-map.yaml (judged by the owner's sessions, not by this file).
"""
import ast, re, sqlite3, sys, yaml, subprocess, collections, datetime
from pathlib import Path

ROOT = Path("/home/user/guidebook")
OUT = ROOT / "scratchpad/session_2026-11-12-pipeline-bidirectional-audit/dossier"
OUT.mkdir(parents=True, exist_ok=True)

con = sqlite3.connect(f"file:{ROOT}/data/guidebook.db?mode=ro", uri=True)
UV = con.execute("pragma user_version").fetchone()[0]
stagemap = yaml.safe_load((ROOT / "governance/stage-map.yaml").read_text())["tables"]
contract = yaml.safe_load((ROOT / "governance/pipeline-contract.yaml").read_text())
STAGES = [s["id"] for s in contract["stages"]]
registry = yaml.safe_load((ROOT / "governance/check-registry.yaml").read_text())

tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
views = [r[0] for r in con.execute("select name from sqlite_master where type='view' order by name")]
rows = {t: con.execute(f'select count(*) from "{t}"').fetchone()[0] for t in tables}
ddl = dict(con.execute("select name, sql from sqlite_master where sql is not null"))
stage_of = {t: stagemap.get(t, "UNMAPPED") for t in tables}

def view_deps(v):
    sql = ddl[v]
    return sorted({t for t in tables if re.search(rf"\b{t}\b", sql)})

view_stages = {v: sorted({stage_of[t] for t in view_deps(v)}) for v in views}

def fk_list(t):
    return [(f[3], f[2], f[4]) for f in con.execute(f'pragma foreign_key_list("{t}")')]

def cols(t):
    return list(con.execute(f'pragma table_info("{t}")'))

tbl_pat = {t: re.compile(rf"\b{re.escape(t)}\b") for t in tables + views}

def tables_in(text):
    return {t for t, p in tbl_pat.items() if p.search(text)}

WRITE = re.compile(r"\b(INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM|REPLACE\s+INTO)\s+\"?(\w+)", re.I)
def writes_in(text):
    return {m.group(2) for m in WRITE.finditer(text)} & set(tables)

# ---------------------------------------------------------------- code index
def code_files():
    pats = ["scripts/*.py", "scripts/audit/*.py", "scripts/audit/graph/*.py", "scripts/research/*.py",
            "scripts/generate/*.py", "scripts/assess/*.py", "scripts/ci_helpers/*.py", "scripts/tests/*.py",
            "schemas/*.py", ".claude/hooks/*.py"]
    out = []
    for p in pats:
        out += sorted(ROOT.glob(p))
    return [p for p in out if p.name != "__init__.py"]

def doc1(path, src):
    try:
        d = ast.get_docstring(ast.parse(src)) or ""
    except SyntaxError:
        d = ""
    return " ".join(d.split())[:240]

units = []  # (relpath, nlines, doc, defs, read_tables, write_tables)
for f in code_files():
    src = f.read_text(errors="replace")
    try:
        tree = ast.parse(src)
        defs = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    except SyntaxError:
        defs = []
    w = writes_in(src)
    r = tables_in(src) - w
    units.append(dict(path=str(f.relative_to(ROOT)), n=src.count("\n") + 1, doc=doc1(f, src),
                      defs=defs, r=r, w=w))

def stage_profile(ts):
    c = collections.Counter(stage_of.get(t, "view") if t in stage_of else
                            "+".join(view_stages.get(t, ["?"])) for t in ts)
    return c

def primary_stage(u):
    ws = collections.Counter(stage_of[t] for t in u["w"])
    pool = ws or collections.Counter(stage_of[t] for t in u["r"] if t in stage_of)
    pool = {k: v for k, v in pool.items() if k in STAGES}
    return sorted(pool, key=lambda k: -pool[k]) if pool else []

# ---------------------------------------------------------------- db.py verbs
dbsrc = (ROOT / "scripts/db.py").read_text()
dbtree = ast.parse(dbsrc)
funcs = {n.name: ast.get_source_segment(dbsrc, n) for n in dbtree.body if isinstance(n, ast.FunctionDef)}
verb_help = {}
for m in re.finditer(r'sub\.add_parser\(\s*"([\w-]+)"(?:\s*,\s*help\s*=\s*("(?:[^"\\]|\\.)*"|\([^)]*\)))?', dbsrc):
    h = m.group(2) or ""
    verb_help[m.group(1)] = re.sub(r'["\s]+', " ", h).strip(" ()")[:120]
# handler blocks: `if/elif args.command == "x":` up to the next one
blocks = {}
pos = [(m.start(), m.group(1)) for m in re.finditer(r'(?:if|elif)\s+args\.command\s*==\s*"([\w-]+)"\s*:', dbsrc)]
for i, (s, v) in enumerate(pos):
    e = pos[i + 1][0] if i + 1 < len(pos) else len(dbsrc)
    seg = dbsrc[s:e]
    ls = dbsrc.rfind("\n", 0, s) + 1
    ind = s - ls  # indent of the if/elif; the block ends at the first line indented less
    keep = [seg.split("\n", 1)[0]]
    for ln in seg.split("\n")[1:]:
        if ln.strip() and (len(ln) - len(ln.lstrip())) < ind:
            break
        keep.append(ln)
    blocks[v] = "\n".join(keep)

def closure(text, depth=3):
    seen, todo, acc = set(), [(text, 0)], [text]
    while todo:
        t, d = todo.pop()
        if d >= depth:
            continue
        for fn in set(re.findall(r"\b([A-Za-z_]\w+)\(", t)):
            if fn in funcs and fn not in seen:
                seen.add(fn); acc.append(funcs[fn]); todo.append((funcs[fn], d + 1))
    return "\n".join(acc)

verbs = {}
for v, b in blocks.items():
    full = closure(b)
    verbs[v] = dict(help=verb_help.get(v, ""), w=writes_in(full), r=tables_in(full) - writes_in(full))

# ---------------------------------------------------------------- checks
chk = registry["checks"]
def check_tables(c):
    cmd = [x for x in c.get("cmd", []) if str(x).endswith(".py")]
    t = set()
    for x in cmd:
        p = ROOT / x
        if p.exists():
            t |= tables_in(p.read_text(errors="replace"))
    return t

def check_stage(c):
    s = collections.Counter(stage_of[t] for t in check_tables(c) if t in stage_of and stage_of[t] in STAGES)
    return sorted(s, key=lambda k: -s[k])

# contract criteria -> stage
crit_by_stage = {s["id"]: s.get("criteria", []) for s in contract["stages"]}

# ================================================================ writers
def w(name, text):
    (OUT / name).write_text(text)

def md_table(header, rws):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rws:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
STAMP = f"_Generated {now} at commit {sha}, schema user_version {UV}. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._\n"

# ---- 30 data tables
d = [f"# 30 — Data tables (Layer 3 container shape)\n\n{STAMP}\n"]
d.append(f"{len(tables)} tables, {len(views)} views, {sum(1 for t in tables if rows[t]==0)} empty tables. Stage = `governance/stage-map.yaml` (JUDGED by the owner's sessions; `infrastructure` is not a stage).\n")
d.append("## 30.1 Tables by stage\n")
for s in STAGES + ["infrastructure", "UNMAPPED"]:
    ts = [t for t in tables if stage_of[t] == s]
    if not ts:
        continue
    d.append(f"### {s} ({len(ts)} tables)\n")
    d.append(md_table(["table", "rows", "cols", "FK out (col→table.col)"],
                      [(t, rows[t], len(cols(t)), "; ".join(f"{a}→{b}.{c}" for a, b, c in fk_list(t)) or "—") for t in ts]))
    d.append("")
d.append("## 30.2 Views and the stages they span (a cross-stage view IS the pointer — CLAUDE.md §3)\n")
d.append(md_table(["view", "reads tables", "stages spanned"],
                  [(v, ", ".join(view_deps(v)) or "—", ", ".join(view_stages[v]) or "—") for v in views]))
d.append("\n## 30.3 Writable-set check (NOT NULL FK into an EMPTY table)\n")
empty = {t for t in tables if rows[t] == 0}
unw = []
for t in tables:
    dead = {f[3] for f in con.execute(f'pragma foreign_key_list("{t}")') if f[2] in empty}
    for c in cols(t):
        if c[1] in dead and c[3]:
            unw.append((t, c[1], [f[2] for f in con.execute(f'pragma foreign_key_list("{t}")') if f[3] == c[1]][0]))
d.append(md_table(["table", "column", "→ empty table"], unw) if unw else "None derived.")
d.append("\n## 30.4 Full DDL (verbatim from sqlite_master)\n")
for s in STAGES + ["infrastructure"]:
    for t in [t for t in tables if stage_of[t] == s]:
        d.append(f"### `{t}` — {s}, {rows[t]} rows\n\n```sql\n{ddl[t]}\n```\n")
d.append("### Views (verbatim)\n")
for v in views:
    d.append(f"#### `{v}`\n\n```sql\n{ddl[v]}\n```\n")
w("30-data-tables.md", "\n".join(d))

# ---- 20 per-stage files
STAGE_DOCS = {  # prose homes named by CLAUDE.md §3/§9 and contract; existence is verified below
    "base": ["governance/population-taxonomy.md", "governance/functional-taxonomy.md", "governance/jurisdiction-philosophy.md", "governance/retired-vocabulary.yaml", "governance/grounds.md"],
    "research": ["governance/pipeline-operations.md", "governance/research-contract.yaml", "governance/mining-screens.yaml", "governance/evidence-methodology.md"],
    "evidence": ["governance/evidence-architecture.md", "governance/tier-system.md", "governance/co1-operational.md", "governance/evidence-methodology.md"],
    "judgment": ["governance/evidence-architecture.md", "governance/time-model.md", "governance/held-tensions.md"],
    "synthesis": ["governance/evidence-architecture.md", "governance/held-tensions.md"],
    "specification": ["governance/evidence-architecture.md", "governance/conceptual-model.md"],
    "render": ["architecture/page-templates.md", "architecture/navigation-modes.md", "governance/evidence-architecture.md", "governance/audience-priority.md"],
}
for i, s in enumerate(STAGES):
    ts = [t for t in tables if stage_of[t] == s]
    vs = [v for v in views if s in view_stages[v]]
    out = [f"# 2{i} — Stage `{s}`\n\n{STAMP}\n"]
    anchor = next(x for x in contract["stages"] if x["id"] == s)
    out.append(f"**Contract anchor:** {anchor['anchor']}\n\n**Contract entry condition(s):** " + "; ".join(anchor["entry"]) + "\n")
    out.append(f"## Tables ({len(ts)})\n")
    out.append(md_table(["table", "rows", "columns"], [(t, rows[t], ", ".join(c[1] for c in cols(t))) for t in ts]) if ts else "_No tables mapped to this stage._ (render has only what the map holds; the renderers are not in the database.)")
    out.append(f"\n## Views touching this stage ({len(vs)})\n")
    out.append(md_table(["view", "all stages spanned"], [(v, ", ".join(view_stages[v])) for v in vs]) if vs else "None.")
    out.append("\n## Contract criteria\n")
    out.append(md_table(["id", "kind", "check", "criterion (first 200 chars)"],
                        [(c["id"], c["kind"], c.get("check") or "**NONE (unenforced)**", " ".join(c["criterion"].split())[:200]) for c in crit_by_stage[s]]) if crit_by_stage[s] else "None.")
    # db.py verbs: writers into this stage's tables
    vw = sorted(v for v, x in verbs.items() if x["w"] & set(ts))
    out.append(f"\n## `db.py` verbs that WRITE this stage's tables ({len(vw)})\n")
    out.append(md_table(["verb", "writes", "reads", "help"],
                        [(v, ", ".join(sorted(verbs[v]["w"])), ", ".join(sorted(verbs[v]["r"]))[:200], verbs[v]["help"]) for v in vw]) if vw else "None.")
    vr = sorted(v for v, x in verbs.items() if (x["r"] & set(ts)) and v not in vw)
    out.append(f"\n## `db.py` verbs that only READ this stage's tables ({len(vr)})\n")
    out.append(", ".join(f"`{v}`" for v in vr) or "None.")
    # code units
    cu = [u for u in units if (u["w"] & set(ts)) and not u["path"].startswith("scripts/tests") and u["path"] != "scripts/db.py"]
    out.append(f"\n## Other code that WRITES this stage's tables ({len(cu)})\n")
    out.append(md_table(["file", "lines", "writes", "purpose (docstring)"], [(u["path"], u["n"], ", ".join(sorted(u["w"] & set(ts))), u["doc"]) for u in cu]) if cu else "None.")
    cr = [u for u in units if (u["r"] & set(ts)) and not (u["w"] & set(ts)) and u["path"] != "scripts/db.py" and u["path"].startswith("scripts/") and not u["path"].startswith("scripts/tests")]
    out.append(f"\n## Code that READS this stage's tables, writing none of them ({len(cr)})\n")
    out.append(md_table(["file", "lines", "reads", "purpose (docstring)"], [(u["path"], u["n"], ", ".join(sorted(u["r"] & set(ts)))[:120], u["doc"]) for u in cr]) if cr else "None.")
    tt = [u for u in units if u["path"].startswith("scripts/tests") and (u["r"] | u["w"]) & set(ts)]
    out.append(f"\n## Tests naming this stage's tables ({len(tt)})\n" + (", ".join(f"`{u['path']}`" for u in tt) or "None."))
    ck = [c for c in chk if s in check_stage(c)[:1]]
    out.append(f"\n## Registry checks whose PRIMARY stage (by tables read) is `{s}` ({len(ck)})\n")
    out.append(md_table(["check id", "battery", "level", "basis"], [(c["id"], c.get("battery", ""), c.get("level", ""), c.get("basis", "")) for c in ck]) if ck else "None.")
    sk = sorted(p for p in (ROOT / ".claude/skills").glob("*/SKILL.md") if tables_in(p.read_text(errors="replace")) & set(ts))
    out.append(f"\n## Skills naming this stage's tables ({len(sk)})\n" + (", ".join(f"`{p.parent.name}`" for p in sk) or "None."))
    docs = [p for p in STAGE_DOCS[s] if (ROOT / p).exists()]
    out.append("\n## Prose homes for this stage\n" + "\n".join(f"- `{p}`" for p in docs))
    w(f"2{i}-stage-{s}.md", "\n".join(out))

# ---- 10 pipeline itself
p = [f"# 10 — The pipeline itself\n\n{STAMP}\n"]
p.append("## 10.1 Spine and contract\n\n```\n" + contract["spine"] + "\n```\n")
p.append(f"Contract status: `{contract['status']}`, ratified: `{contract['ratified']}`. Stages: {', '.join(STAGES)}.\n")
p.append("Cross-stage criteria:\n\n" + md_table(["id", "check", "criterion (first 200)"], [(c["id"], c.get("check") or "**NONE**", " ".join(c["criterion"].split())[:200]) for c in contract["cross_stage"]]))
unen = [(s, c["id"]) for s, cs in crit_by_stage.items() for c in cs if not c.get("check")]
p.append(f"\n\n**Contract criteria with `check: null` (unenforced): {len(unen)}** — " + ", ".join(f"{s}/{i}" for s, i in unen) + "\n")
p.append("## 10.2 Pipeline-level code\n")
core = ["scripts/db.py", "scripts/dbcore.py", "scripts/run_checks.py", "scripts/migrate_db.py", "scripts/emit_data_migration.py",
        "scripts/research/emit_batch_sql.py", "scripts/research/retrieval_log.py", "scripts/assess/assess_cell.py", "scripts/preflight.sh"]
for c in core:
    pp = ROOT / c
    if pp.exists():
        n = pp.read_text(errors="replace").count("\n") + 1
        u = next((u for u in units if u["path"] == c), None)
        p.append(f"- `{c}` ({n} lines){' — ' + u['doc'] if u and u['doc'] else ''}")
p.append(f"\n## 10.3 Migrations\n\n{len(list((ROOT/'scripts/migrations').glob('*.sql')))} files in `scripts/migrations/` ({len(list((ROOT/'scripts/migrations').glob('data_*.sql')))} `data_*`). Schema migrations (first 3 and last 3 by name): " +
         ", ".join(f"`{x.name}`" for x in sorted(f for f in (ROOT/'scripts/migrations').glob('[0-9]*.sql'))[:3] + sorted(f for f in (ROOT/'scripts/migrations').glob('[0-9]*.sql'))[-3:]) + "\n")
p.append("## 10.4 Check registry\n")
bat = collections.Counter(c.get("battery") for c in chk)
lev = collections.Counter(c.get("level") for c in chk)
p.append(f"{len(chk)} checks. By battery: {dict(bat)}. By level: {dict(lev)}.\n")
p.append(md_table(["id", "battery", "level", "kinds", "primary stage by tables", "basis"],
                  [(c["id"], c.get("battery", ""), c.get("level", ""), ",".join(c.get("kinds", [])), (check_stage(c) or ["—"])[0], c.get("basis", "")) for c in chk]))
p.append("\n## 10.5 Skills and project agents/commands\n")
p.append("Project skills (`.claude/skills/`): " + ", ".join(f"`{x.name}`" for x in sorted((ROOT/'.claude/skills').iterdir())) + "\n")
p.append("Agents: " + ", ".join(f"`{x.stem}`" for x in sorted((ROOT/'.claude/agents').glob('*.md'))) + ". Commands: " + ", ".join(f"`/{x.stem}`" for x in sorted((ROOT/'.claude/commands').glob('*.md'))) + "\n")
p.append("## 10.6 Operations (verbatim `governance/pipeline-operations.md` §1)\n\nSee that file. Stage-orchestration entry point: `.claude/skills/run-pipeline/SKILL.md` (verbatim copy appended in `11-run-pipeline-skill.md`).\n")
w("10-pipeline-itself.md", "\n".join(p))
w("11-run-pipeline-skill.md", "# 11 — run-pipeline skill (verbatim)\n\n" + (ROOT / ".claude/skills/run-pipeline/SKILL.md").read_text())

# ---- 12 db.py verb matrix (the executable surface, all of it)
v = [f"# 12 — `db.py` verb matrix (the CLI write path)\n\n{STAMP}\n", f"{len(verbs)} verbs. Reads/writes derived from the handler block plus up to 3 levels of called helpers; names a table wherever its name appears in the code, so a read column can over-report (it cannot under-report a literal table name).\n"]
v.append(md_table(["verb", "stage(s) written", "tables written", "tables read (≤12 shown)", "help"],
                  [(k, "+".join(sorted({stage_of[t] for t in x["w"]})) or "—", ", ".join(sorted(x["w"])) or "—", ", ".join(sorted(x["r"])[:12]), x["help"]) for k, x in sorted(verbs.items())]))
tbl_no_writer = [t for t in tables if t != "sqlite_sequence" and not any(t in x["w"] for x in verbs.values())]
v.append("\n\n## Tables no `db.py` verb writes (derived)\n\n" + md_table(["table", "stage", "rows"], [(t, stage_of[t], rows[t]) for t in tbl_no_writer]))
w("12-db-verb-matrix.md", "\n".join(v))

# ---- 13 code index
c = [f"# 13 — Code index (all Python under scripts/, schemas/, .claude/hooks)\n\n{STAMP}\n"]
c.append(md_table(["file", "lines", "primary stage (by tables written, else read)", "writes", "purpose"],
                  [(u["path"], u["n"], "+".join(primary_stage(u)[:2]) or "—", ", ".join(sorted(u["w"]))[:100], u["doc"]) for u in units]))
w("13-code-index.md", "\n".join(c))

print("dossier files:", sorted(x.name for x in OUT.iterdir()))
print("tables", len(tables), "views", len(views), "verbs", len(verbs), "checks", len(chk), "units", len(units), "unmapped", [t for t in tables if stage_of[t] == "UNMAPPED"])
