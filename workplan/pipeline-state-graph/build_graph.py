#!/usr/bin/env python3
"""build_graph.py -- derive the pipeline state graph from the live repository and check every hand-authored claim.

    python3 workplan/pipeline-state-graph/build_graph.py            # regenerate the outputs
    python3 workplan/pipeline-state-graph/build_graph.py --check    # verify only; writes nothing; exit 1 on any failure
    python3 workplan/pipeline-state-graph/build_graph.py --selftest # prove the checks can fail (mutation tests)
    python3 workplan/pipeline-state-graph/build_graph.py --compare /path/to/other/tree   # add a tree-vs-tree delta

Inputs it READS and never writes: data/guidebook.db (read-only), scripts/db.py, scripts/assess/assess_cell.py,
governance/{stage-map,pipeline-contract,check-registry}.yaml, .github/workflows/*.yml, CLAUDE.md, and this
directory's atoms/*.jsonl, conflicts.yaml, machines.yaml, capabilities.yaml.

What is DERIVED (CLAUDE.md rules 7, 7a, 8): stages, table->stage, row counts, foreign keys, the UNWRITABLE set, views and
the stages they span, state vocabularies (from each column's own CHECK), verb->table writers, tables nobody writes,
probe verdicts, capability verdicts. What is HAND-AUTHORED: the atoms (each with a verbatim quote, verified here), the
conflict adjudications, the transition guards (each with a needle re-read here), and the capability predicates.
Every `EXAMINED:` line below is a count of subjects a check actually looked at; a zero is reported, not passed over.
"""
import argparse, ast, collections, copy, datetime, glob, hashlib, json, os, re, shutil, sqlite3, subprocess, sys, tempfile
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

MOD = {"MUST", "MUST_NOT", "MAY", "DEFINES", "CARDINALITY", "ORDER", "EQUATES", "RESERVES", "OPEN"}
SPK = {"OWNER_QUOTED", "OWNER_RELAYED", "RATIFIED_DOC", "AGENT_PROPOSAL", "PROCESS_RULE"}
STA = {"ACTIVE", "SUPERSEDED", "AMENDED", "PROPOSED", "OPEN", "HISTORICAL"}
REQ = {"id", "source", "quote", "modality", "subject", "claim", "scope", "speaker", "status"}
CLASSES = {"RULING-RULING", "RULING-DOC", "RULING-MECHANISM", "DOC-DOC", "UNRECORDED", "PROVENANCE", "OPEN-QUESTION"}
SEVERITY = {"S1", "S2", "S3"}
RESOLVERS = {"OWNER", "AGENT", "OWNER+AGENT", "NONE"}
VERDICTS = {"PASS", "FAIL", "NOT-BUILT", "UNKNOWN", "INFO"}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
as_list = lambda v: [] if v is None else (v if isinstance(v, list) else [v])


# ----------------------------------------------------------------------------------------------- source reading
_text = {}
def read(repo, rel):
    k = (str(repo), rel)
    if k not in _text:
        _text[k] = (Path(repo) / rel).read_text(encoding="utf-8", errors="replace")
    return _text[k]


def func_source(repo, rel, func):
    """Source of a function (any nesting) in a .py file; the whole file if func is None or the file is not Python."""
    txt = read(repo, rel)
    if not func or not rel.endswith(".py"):
        return txt
    for n in ast.walk(ast.parse(txt)):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func:
            return ast.get_source_segment(txt, n) or ""
    return None


def needle_ok(repo, ev):
    """(ok, why). An `absent: true` needle must NOT match."""
    try:
        src = func_source(repo, ev["file"], ev.get("func"))
    except FileNotFoundError:
        return False, f"file not found: {ev['file']}"
    if src is None:
        return False, f"function {ev.get('func')!r} not found in {ev['file']}"
    hit = re.search(ev["needle"], src, re.S) is not None
    if ev.get("absent"):
        return (not hit), ("pattern present but claimed absent" if hit else "")
    return hit, ("" if hit else "needle not found")


# ----------------------------------------------------------------------------------------------- atoms
def load_atoms():
    atoms, problems = {}, []
    for f in sorted(glob.glob(str(HERE / "atoms" / "atoms-*.jsonl"))):
        for ln, line in enumerate(open(f, encoding="utf-8"), 1):
            if not line.strip():
                continue
            a = json.loads(line)
            a["_file"] = Path(f).name
            if a["id"] in atoms:
                problems.append(f"{a['id']}: duplicate id ({Path(f).name})")
            atoms[a["id"]] = a
    return atoms, problems


def verify_atoms(atoms, repo=REPO, only=None, stats=None):
    """Every quote must occur verbatim (whitespace collapsed, leading '> ' ignored) in its source file.

    `only`, when given, limits the QUOTE and line checks to those atom ids (the atoms something still
    cites); the structural checks (keys, modality, speaker, status) run on every atom. `stats`, when
    given, receives `verified`: how many atoms had their quote actually read, which is what an
    EXAMINED line must report (the size of the input set is not that figure).
    """
    bad, cache = [], {}
    def doc(path):
        if path not in cache:
            raw = read(repo, path)
            cache[path] = norm("\n".join(re.sub(r"^\s*>\s?", "", l) for l in raw.split("\n")))
        return cache[path]
    for a in atoms.values():
        miss = REQ - set(a)
        if miss:
            bad.append(f"{a.get('id')}: missing keys {sorted(miss)}"); continue
        if a["modality"] not in MOD: bad.append(f"{a['id']}: bad modality {a['modality']}")
        if a["speaker"] not in SPK: bad.append(f"{a['id']}: bad speaker {a['speaker']}")
        if a["status"] not in STA: bad.append(f"{a['id']}: bad status {a['status']}")
        if only is not None and a["id"] not in only: continue
        if stats is not None: stats["verified"] = stats.get("verified", 0) + 1
        path = a["source"].split(":")[0]
        try:
            ok = norm(re.sub(r"^\s*>\s?", "", a["quote"])) in doc(path)
        except FileNotFoundError:
            bad.append(f"{a['id']}: source not found {path}"); continue
        if not ok:
            bad.append(f"{a['id']}: QUOTE NOT FOUND in {path}: {a['quote'][:80]!r}"); continue
        lm = re.search(r":(\d+)$", a["source"])
        if lm:                                   # the cited line must be where the quote starts (+-3 lines)
            ln = int(lm.group(1)); lines = read(repo, path).split("\n")
            window = norm("\n".join(re.sub(r"^\s*>\s?", "", x) for x in lines[max(0, ln - 4): ln + 3]))
            head = norm(re.sub(r"^\s*>\s?", "", a["quote"]))[:50]
            if head not in window:
                bad.append(f"{a['id']}: quote found in {path} but not near cited line {ln}")
    return bad


# ----------------------------------------------------------------------------------------------- the live tree
class Tree:
    """Everything derived from one checkout. Read-only."""
    def __init__(self, root):
        self.root = Path(root)
        self.con = sqlite3.connect(f"file:{self.root}/data/guidebook.db?mode=ro", uri=True)
        self.con.row_factory = sqlite3.Row
        q = lambda s, *a: self.con.execute(s, a).fetchall()
        self.q = q
        self.user_version = self.con.execute("pragma user_version").fetchone()[0]
        self.tables = [r[0] for r in q("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by 1")]
        self.ddl = {r[0]: r[1] or "" for r in q("select name, sql from sqlite_master where type in ('table','view','index','trigger')")}
        self.views = {r[0]: r[1] or "" for r in q("select name, sql from sqlite_master where type='view' order by 1")}
        self.rows = {t: self.con.execute(f'select count(*) from "{t}"').fetchone()[0] for t in self.tables}
        self.stagemap = yaml.safe_load(read(self.root, "governance/stage-map.yaml"))
        self.contract = yaml.safe_load(read(self.root, "governance/pipeline-contract.yaml"))
        self.stages = [s["id"] for s in self.contract["stages"]]
        self.t2s = self.stagemap["tables"]
        self.registry = yaml.safe_load(read(self.root, "governance/check-registry.yaml"))
        self._derive_fks(); self._derive_vocab(); self._derive_verbs()

    def cols(self, t):
        return [c[1] for c in self.con.execute(f'pragma table_info("{t}")')]

    def notnull(self, t, c):
        return any(x[1] == c and x[3] for x in self.con.execute(f'pragma table_info("{t}")'))

    def _derive_fks(self):
        self.fks = []
        for t in self.tables:
            for f in self.con.execute(f'pragma foreign_key_list("{t}")'):
                self.fks.append(dict(child=t, col=f[3], parent=f[2], notnull=self.notnull(t, f[3])))
        self.empty = {t for t, n in self.rows.items() if n == 0}
        self.unwritable_fk = [f for f in self.fks if f["parent"] in self.empty and f["notnull"]]

    def _derive_vocab(self):
        self.vocab = {}
        for t in self.tables:
            ddl = self.ddl.get(t, "")
            if self.ddl.get(t, "").lstrip().upper().startswith("CREATE VIEW"): continue
            for m in re.finditer(r"\b\"?(\w+)\"?\s+IN\s*\(\s*((?:'[^']*'\s*,?\s*)+)\)", ddl, re.I | re.S):
                vals = re.findall(r"'([^']*)'", m.group(2))
                if vals: self.vocab.setdefault(t, {}).setdefault(m.group(1), vals)

    def _derive_verbs(self):
        src = read(self.root, "scripts/db.py")
        tree = ast.parse(src)
        funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        sqlw = re.compile(r'\b(INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM)\s+"?(\w+)"?', re.I)
        real = set(self.tables)
        def strings(node):
            for n in ast.walk(node):
                if isinstance(n, ast.Constant) and isinstance(n.value, str): yield n.value
                elif isinstance(n, ast.JoinedStr):
                    yield "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in n.values)
        def writes(fn, seen=None, depth=0):
            seen = seen or set(); out = {}
            if fn.name in seen or depth > 3: return out
            seen.add(fn.name)
            for s in strings(fn):
                for m in sqlw.finditer(s):
                    op, t = m.group(1).split()[0].upper(), m.group(2)
                    if t in real: out.setdefault(t, set()).add(op)       # prose words ('that', 'below') are not tables
            for n in ast.walk(fn):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in funcs and n.func.id != fn.name:
                    for t, ops in writes(funcs[n.func.id], seen, depth + 1).items(): out.setdefault(t, set()).update(ops)
            return out
        refus = lambda fn: sum(1 for n in ast.walk(fn) if isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call)
                               and getattr(n.exc.func, "id", getattr(n.exc.func, "attr", "")) == "Refusal")
        dispatch = {}
        for n in ast.walk(funcs["main"]):
            if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and isinstance(n.test.left, ast.Attribute) \
                    and n.test.left.attr == "command":
                cmp_ = n.test.comparators[0]
                names = [cmp_.value] if isinstance(cmp_, ast.Constant) else [e.value for e in getattr(cmp_, "elts", []) if isinstance(e, ast.Constant)]
                called = []
                for st in n.body:
                    for c in ast.walk(st):
                        if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in funcs: called.append(c.func.id)
                for v in names:
                    dispatch.setdefault(v, list(dict.fromkeys(called)))
        self.verbs = {}
        for v in re.findall(r'add_parser\(\s*"([^"]+)"', src):
            w, r, fs = {}, 0, dispatch.get(v, [])
            for f in fs:
                for t, ops in writes(funcs[f]).items(): w.setdefault(t, set()).update(ops)
                r += refus(funcs[f])
            self.verbs[v] = dict(functions=fs, writes={t: sorted(o) for t, o in sorted(w.items())}, refusals=r)
        self.writers = collections.defaultdict(list)
        for v, d in self.verbs.items():
            for t in d["writes"]: self.writers[t].append(v)

    # ---- derived structure
    def stage(self, t):
        return self.t2s.get(t, "?")

    def unwritable_set(self):
        """(child.col -> parent) NOT NULL FKs into an emptied table, with whether a verb writes the parent too."""
        out = []
        for f in self.unwritable_fk:
            vc = set(self.writers.get(f["child"], [])); vp = set(self.writers.get(f["parent"], []))
            out.append(dict(f, verbs_child=sorted(vc), parent_written_by_same_verb=sorted(vc & vp)))
        return out

    def no_writer_tables(self):
        return sorted(t for t in self.tables if t not in self.writers)

    def view_info(self):
        info = {}
        for v, sql in self.views.items():
            reads = sorted(t for t in self.tables if re.search(rf"\b{re.escape(t)}\b", sql))
            stages = sorted({self.stage(t) for t in reads if self.stage(t) not in ("?", "infrastructure")})
            try: n = self.con.execute(f'select count(*) from "{v}"').fetchone()[0]
            except Exception as e: n = f"ERR {str(e)[:50]}"
            info[v] = dict(reads=reads, stages=stages, crosses=len(stages) > 1, rows=n)
        return info


# ----------------------------------------------------------------------------------------------- probes
def make_probes():
    P = {}
    def probe(pid, tests, atoms):
        def deco(fn):
            P[pid] = dict(fn=fn, tests=tests, atoms=atoms); PROBE_DEFS[pid] = P[pid]; return fn
        return deco

    LENS = ["identity_code", "icf_code", "needs_code", "medical_code"]

    @probe("P-A", "the five splinter population_* link tables are deleted (owner 2026-08-28)", ["LED-132"])
    def _(T):
        sp = ["extraction_population_links", "probe_population_links", "citation_population_links", "case_study_populations", "economics_entry_populations"]
        live = [t for t in sp if t in T.tables]
        return ("FAIL" if live else "PASS"), {"still_present": live, "rows": [T.rows[t] for t in live]}

    @probe("P-B", "every non-base table attaching a determination to a group has the four lens columns; population_code retired", ["LED-128", "CLM-042"])
    def _(T):
        bad = {}
        for t in T.tables:
            if T.stage(t) == "base": continue          # base holds the lens registries and crossing maps, which attach nothing to a determination
            c = T.cols(t); have = [l for l in LENS if l in c]
            if (have and len(have) < 4) or "population_code" in c:
                bad[t] = have + (["population_code"] if "population_code" in c else [])
        return ("FAIL" if bad else "PASS"), bad

    @probe("P-C", "no table or column is named with the retired word 'population' (owner 2026-08-28; the rename is not applied)", ["LED-127", "ADD-001"])
    def _(T):
        tabs = [t for t in T.tables if "population" in t]
        cols = {t: [c for c in T.cols(t) if "population" in c] for t in T.tables if any("population" in c for c in T.cols(t))}
        return ("PASS" if not tabs and not cols else "NOT-BUILT"), {"tables": tabs, "columns": cols}

    @probe("P-D", "no UNIQUE index on source_value_extractions(ref_id)", ["LED-101", "PIP-10"])
    def _(T):
        u = [r[0] for r in T.q("select name from sqlite_master where type='index' and tbl_name='source_value_extractions' and sql like 'CREATE UNIQUE%'")]
        return ("PASS" if not u and T.notnull("source_value_extractions", "ref_id") else "FAIL"), {"unique_indexes": u}

    @probe("P-F", "the tier verdict is a judgment output, not a column on evidence_sources", ["LED-108", "OPS-06"])
    def _(T):
        have = {t: [c for c in T.cols(t) if c in ("tier", "scope")] for t in T.tables if any(c in ("tier", "scope") for c in T.cols(t))}
        return ("FAIL" if "evidence_sources" in have else "PASS"), have

    @probe("P-G", "no ICF-typed column holds an 'AX-' code (owner 2026-09-13: 'AX-' for ICF should never ever exist anywhere)", ["LED-166"])
    def _(T):
        hits, other, icf_cols = {}, {}, []
        for t in T.tables:
            for c in T.cols(t):
                is_icf = bool(re.search(r"icf", c)) and c != "notes"
                if is_icf: icf_cols.append(f"{t}.{c}")
                try: n = T.con.execute(f'select count(*) from "{t}" where "{c}" GLOB \'*AX-*\'').fetchone()[0]
                except Exception: continue
                if not n: continue
                (hits if is_icf else other)[f"{t}.{c}"] = n
        return ("FAIL" if hits else "PASS"), {"icf_typed_columns_examined": len(icf_cols), "icf_columns_holding_AX": hits, "AX_elsewhere_not_tested_by_this_ruling": other}

    @probe("P-AXIS", "'axis' is not a vocabulary-layer name (owner 2026-08-24: 'I don't want axis to be used')", ["LED-076", "DRS-006"])
    def _(T):
        tabs = [t for t in T.tables if re.search(r"axis|axes", t)]
        cols = {t: [c for c in T.cols(t) if re.search(r"axis|axes", c)] for t in T.tables if any(re.search(r"axis|axes", c) for c in T.cols(t))}
        return ("FAIL" if tabs or cols else "PASS"), {"tables": tabs, "columns": cols}

    @probe("P-H", "every view reading a retirable table names its lifecycle column", ["LED-171", "LED-170"])
    def _(T):
        # \bstatus\b, not `status`: `verification_status` and `convergence_status` in a view
        # that reads base_parameters were counted as its lifecycle filter (step 0.3).
        life = {"base_parameters": r"\bstatus\b", "specifications": r"retired_at|superseded_by", "evidence_sources": r"superseded_by_ref_id"}
        bad = {}
        for v, sql in T.views.items():
            for t, pat in life.items():
                if re.search(rf"\b{t}\b", sql) and not re.search(pat, sql): bad.setdefault(v, []).append(t)
        return ("FAIL" if bad else "PASS"), {"views_not_naming_lifecycle": bad, "note": "lexical test, views only: it reads view SQL, so a view that merely names the column passes and no non-view reader is examined"}

    @probe("P-K", "a live renderer can read specifications keyed on parameter_id x lens", ["PIP-06", "LED-103", "POS-03"])
    def _(T):
        fails, scanned, keyed = {}, 0, []
        for p in ("scripts/generate/build_site.py", "scripts/generate/spec_page.py", "scripts/generate/pilot_renderings.py", "scripts/generate_parts.py"):
            if not (T.root / p).exists(): continue
            scanned += 1
            for n in ast.walk(ast.parse(read(T.root, p))):
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(r"\b(FROM|JOIN)\s+specifications\b", n.value, re.I):
                    if "parameter_id" in n.value: keyed.append(p)
                    try: T.con.execute("explain " + n.value.replace("?", "NULL"))
                    except Exception as e: fails.setdefault(p, []).append(str(e)[:80])
        v = "FAIL" if fails else ("PASS" if keyed else ("NOT-BUILT" if not scanned else "UNKNOWN"))   # step 1.1 deleted every renderer: none to scan
        return v, {"renderers_scanned": scanned, "queries_failing_on_live_schema": fails, "renderers_whose_specification_query_names_parameter_id": sorted(set(keyed))}

    @probe("P-L", "no workflow `git add`s the database blob", ["CLM-012", "LED-153", "OPI-124"])
    def _(T):
        hits = []
        for p in sorted((T.root / ".github/workflows").glob("*.yml")):
            body = "\n".join(l for l in p.read_text(encoding="utf-8", errors="replace").split("\n") if not l.lstrip().startswith("#"))
            if re.search(r"git add[^\n]*data/guidebook\.db", body): hits.append(p.name)
        return ("FAIL" if hits else "PASS"), {"workflows_that_git_add_the_db": hits}

    @probe("P-M", "a search can record which slug x lens cells it covered", ["LED-084", "RES-04"])
    def _(T):
        c = T.cols("search_executions")
        linked = [t for t in T.tables if T.stage(t) == "research" and any(l in T.cols(t) for l in LENS + ["population_code"])]
        return ("PASS" if (any(l in c for l in LENS) or linked) else "FAIL"), {"lens_columns_on_search_executions": [x for x in c if x in LENS], "tables": linked}

    @probe("P-O", "every base vocabulary table is reachable by a sanctioned (db.py) writer", ["LED-182", "CLM-031", "LED-116"])
    def _(T):
        nw = sorted(t for t in T.tables if T.stage(t) == "base" and t not in T.writers)
        return ("FAIL" if nw else "PASS"), {"base_tables_with_no_db_py_writer": nw}

    @probe("P-R", "the engine can reach a determination from findings plus a threshold (owner 2026-09-16)", ["LED-174", "LED-172"])
    def _(T):
        ac = read(T.root, "scripts/assess/assess_cell.py")
        gf = re.search(r"def gather_findings\(", ac) is not None
        roles = re.search(r"DIRECTION_SUPPLYING_ROLES\s*=\s*\(([^)]*)\)", ac)
        det = func_source(T.root, "scripts/assess/assess_cell.py", "determine") or ""
        proxy = "rests_on_proxy_inference = 1" in det and "finding_anchors" in det
        ok = gf and bool(roles and "finding" in roles.group(1)) and proxy
        return ("PASS" if ok else "NOT-BUILT"), {"gather_findings_defined": gf, "direction_supplying_roles": roles.group(1) if roles else None, "determine_has_a_proxy_branch_from_finding_anchors": proxy}

    @probe("P-V", "a (source x parameter) read-state ledger exists", ["LED-195", "LED-199"])
    def _(T):
        return ("PASS" if "source_scans" in T.tables else "NOT-BUILT"), {"source_scans": "source_scans" in T.tables, "v_scan_ledger": "v_scan_ledger" in T.views}

    @probe("P-V2", "add-extraction accepts a slug the source was not admitted to", ["LED-196", "LED-201"])
    def _(T):
        body = func_source(T.root, "scripts/db.py", "insert_extraction") or ""
        guard = "is not admitted to slug" in body and "source_slug_links" in body
        return ("FAIL" if guard else "PASS"), {"admission_guard_present_in_insert_extraction": guard, "function_found": bool(body)}

    @probe("P-W", "an observation is one sighting (phrase at a place), so a second sense is not folded", ["LED-197"])
    def _(T):
        idx = [(r[0], r[1] or "") for r in T.q("select name, sql from sqlite_master where type='index' and tbl_name='observed_terms'")]
        sighting = any("locator" in s for _, s in idx if "UNIQUE" in s)
        return ("PASS" if sighting else "FAIL"), {"unique_indexes": [n for n, s in idx if "UNIQUE" in s], "locator_in_key": sighting}

    @probe("P-X", "some synthesis-stage structure can relate more than one parameter", ["LED-097", "LED-098", "MIS-06"])
    def _(T):
        syn = {t: T.cols(t) for t in T.tables if T.stage(t) == "synthesis"}
        with_pid = [t for t, c in syn.items() if "parameter_id" in c]
        rel = T.con.execute("select count(*) from extraction_relations r join source_value_extractions a on a.extraction_id=r.from_extraction_id join source_value_extractions b on b.extraction_id=r.to_extraction_id where a.parameter_id<>b.parameter_id").fetchone()[0] if "extraction_relations" in T.tables else None
        return ("PASS" if with_pid else "FAIL"), {"synthesis_tables": sorted(syn), "with_parameter_id": with_pid, "extraction_relations_edges_between_different_parameters_live": rel, "distinct_parameter_ids_among_extractions": T.con.execute("select count(distinct parameter_id) from source_value_extractions").fetchone()[0], "extraction_relations_stage": T.stage("extraction_relations"),
                                                        "connection_targets_columns": T.cols("connection_targets"),
                                                        "conflicts_key_columns": [c for c in T.cols("conflicts") if c in ("item_code", "pop_a", "pop_b", "parameter_id")]}

    @probe("P-Y", "specifications: parameter_id NOT NULL and the at-least-one-lens CHECK", ["LED-130", "LED-091"])
    def _(T):
        d = T.ddl.get("specifications", "")
        a = bool(re.search(r"COALESCE\s*\(\s*identity_code", d, re.I)); b = T.notnull("specifications", "parameter_id")
        return ("PASS" if a and b else "FAIL"), {"coalesce_check": a, "parameter_id_not_null": b}

    @probe("P-AB", "source_value_extractions.parameter_id is NOT NULL", ["LED-093"])
    def _(T):
        return ("PASS" if T.notnull("source_value_extractions", "parameter_id") else "FAIL"), {}

    @probe("P-GT", "determination_gates carries all four lens columns", ["LED-128"])
    def _(T):
        have = [c for c in T.cols("determination_gates") if c in LENS]
        return ("PASS" if len(have) == 4 else "FAIL"), {"lens_columns": have}

    @probe("P-ENG-T3", "the engine: T3-clinical alone -> provisional; T3-grey alone -> pending (the assignment, not only the comment)", ["LED-010", "PIP-03", "LED-151"])
    def _(T):
        s = func_source(T.root, "scripts/assess/assess_cell.py", "determine") or ""
        a = re.search(r'T3-clinical-alone -> provisional\s*\n\s*state = "provisional"', s) is not None
        b = re.search(r'T3-grey-alone does not even reach provisional\s*\n\s*state = "pending"', s) is not None
        return ("PASS" if a and b else "FAIL"), {"t3_clinical_alone_assigns_provisional": a, "t3_grey_alone_assigns_pending": b}

    @probe("P-ENG-STATE", "the engine assigns every value of specifications.state", ["EVI-172", "LED-151"])
    def _(T):
        s = func_source(T.root, "scripts/assess/assess_cell.py", "determine") or ""
        vals = (T.vocab.get("specifications") or {}).get("state", [])
        assigned = {v: bool(re.search(rf'state\s*=\s*"{v}"', s)) for v in vals}
        return ("FAIL" if not all(assigned.values()) else "PASS"), {"assigned_by_engine": assigned}

    @probe("P-TIER-DERIVE", "the tier-derivation consistency check is live (not quarantined)", ["EVI-301", "EVI-303", "LED-108"])
    def _(T):
        q = {x["id"]: x.get("status") for x in (T.registry.get("quarantine") or [])}
        live = [c["id"] for c in T.registry["checks"] if "tier" in c["id"] and "deriv" in c["id"]]
        st = q.get("adjudication_integrity")
        return ("PASS" if st != "quarantined" else "FAIL"), {"adjudication_integrity": st, "other_tier_derivation_checks_registered": live}

    @probe("P-STAGE-SVE", "stage-map and the contract place source_value_extractions in the same stage", ["LED-106", "PIP-10"])
    def _(T):
        placed = T.t2s.get("source_value_extractions"); disputed = "source_value_extractions" in (T.stagemap.get("disputed") or {})
        return ("FAIL" if disputed else "PASS"), {"stage_map_places_it_at": placed, "stage_map_marks_it_disputed": disputed}

    @probe("P-UNWRITABLE", "no NOT NULL foreign key points into an emptied table", ["CLM-034", "CLM-048"])
    def _(T):
        u = [x for x in T.unwritable_set() if not x["parent_written_by_same_verb"]]    # a verb that writes the parent and child together makes the pair writable
        return ("FAIL" if u else "PASS"), {"count": len(u), "pairs": [f"{x['child']}.{x['col']} -> {x['parent']}" for x in u],
                                           "with_a_db_py_verb": sorted({v for x in u for v in x["verbs_child"]}),
                                           "parent_written_by_same_verb": {f"{x['child']}.{x['col']}": x["parent_written_by_same_verb"] for x in u if x["parent_written_by_same_verb"]}}

    @probe("P-MEDICAL", "a medical-lens value can be written (the lens registry holds a row)", ["LED-154", "LED-156", "DRS-229"])
    def _(T):
        n = T.rows.get("base_taxonomy_medical", 0)
        return ("PASS" if n else "FAIL"), {"base_taxonomy_medical_rows": n, "writer_verbs": T.writers.get("base_taxonomy_medical", [])}

    @probe("P-CO1-TYPE", "every live co1_source_type value is in schemas.enums.Co1SourceType", ["DRS-248"])
    def _(T):
        try:
            tree = ast.parse(read(T.root, "schemas/enums.py"))
            cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "Co1SourceType")
            en = sorted(x.value.value for x in cls.body if isinstance(x, ast.Assign) and isinstance(x.value, ast.Constant))
        except Exception as e:
            return "UNKNOWN", {"reason": f"could not read Co1SourceType: {e}"}
        live = [r[0] for r in T.q("select distinct co1_source_type from evidence_sources where co1_source_type is not null")]
        out = [v for v in live if v not in en]
        return ("FAIL" if out else "PASS"), {"enum": en, "live_values": live, "outside_enum": out}

    @probe("P-CO1-PROV", "every Co-1 source's co1_provenance is non-empty free text and none holds only the co1-operational value 'published_corpus' (D-0178 requires it to name the co-production)", ["DRS-146", "DRS-263", "CLM-037"])
    def _(T):
        rows = T.q("select ref_id, co1_provenance from evidence_sources where evidence_type='co1'")
        empty = [r[0] for r in rows if not (r[1] or "").strip()]
        only_vocab = [r[0] for r in rows if (r[1] or "").strip() in ("published_corpus", "participatory_synthesis")]
        has_check = "co1_provenance" in (T.vocab.get("evidence_sources") or {})
        return ("PASS" if rows and not empty and not only_vocab else "FAIL"), {"co1_sources_examined": len(rows), "empty": empty, "hold_only_the_co1_operational_vocabulary": only_vocab, "column_has_CHECK_vocabulary": has_check}

    @probe("P-FWD-FK", "foreign keys that point FORWARD along the spine (an earlier stage's table depends on a later stage's table)", ["LED-080", "LED-125", "CLM-029"])
    def _(T):
        order = {s: i for i, s in enumerate(T.stages)}
        fwd = [dict(fk=f"{f['child']}.{f['col']} -> {f['parent']}", from_stage=T.stage(f["child"]), to_stage=T.stage(f["parent"]), child_rows=T.rows[f["child"]])
               for f in T.fks if T.stage(f["child"]) in order and T.stage(f["parent"]) in order and order[T.stage(f["child"])] < order[T.stage(f["parent"])]]
        return "INFO", {"count": len(fwd), "with_live_rows": [x["fk"] for x in fwd if x["child_rows"]], "all": fwd}

    @probe("P-VERIF-VOCAB", "evidence_sources.verification_status admits only VERIFIED / UNVERIFIED (D-0157)", ["EVI-369", "LED-028"])
    def _(T):
        v = (T.vocab.get("evidence_sources") or {}).get("verification_status", [])
        return ("PASS" if sorted(v) == ["UNVERIFIED", "VERIFIED"] else "FAIL"), {"vocabulary": v}

    @probe("P-QUARANTINE", "the checks that guard rendering and tier derivation are live (an active registry check each)", ["PIP-06", "POS-03"])
    def _(T):
        level = {c["id"]: c.get("level") for c in T.registry["checks"]}
        crit = next((c for s in T.contract["stages"] for c in s.get("criteria", []) if c["id"] == "register-invariants"), {})
        rcheck = crit.get("check")
        render_live = bool(rcheck) and any(rcheck in (c.get("cmd") or []) for c in T.registry["checks"])
        tier_live = level.get("adjudication_integrity") == "blocking"
        return ("PASS" if render_live and tier_live else "FAIL"), {"tier_derivation_check_level": level.get("adjudication_integrity"), "register_invariants_check": rcheck, "register_invariants_check_registered": render_live}

    @probe("P-LEDGER-GREP", "the owner statements recorded only in session records appear verbatim in the owner ledger", ["SES-022", "SES-023", "SES-024", "SES-025", "SES-032", "SES-045", "LED-195"])
    def _(T):
        led = norm(read(T.root, "references/project-standards.md"))
        sq = {}
        for sid in ("SES-022", "SES-023", "SES-024", "SES-025", "SES-032", "SES-045"):
            a = ATOMS_FOR_PROBES.get(sid)
            if a: sq[sid] = norm(a["quote"])[:120] in led
        ctl = ATOMS_FOR_PROBES.get("LED-195")
        control = bool(ctl) and norm(ctl["quote"])[:120] in led      # a quote that IS in the ledger must be found, or the test is blind
        absent = [k for k, v in sq.items() if not v]
        if not control: return "UNKNOWN", {"reason": "control quote (LED-195) not found in the ledger; the test cannot see", "ledger_bytes": len(led)}
        return ("FAIL" if absent else "PASS"), {"control_found_in_ledger": control, "verbatim_present_in_ledger": sq, "verbatim_absent": absent}

    @probe("P-STATUS-WRITERS", "every non-default value of evidence_sources.data_capture_status is named beside the column in a writer", ["OPS-04"])
    def _(T):
        vals = (T.vocab.get("evidence_sources") or {}).get("data_capture_status", [])
        dm = re.search(r"data_capture_status[^,]*DEFAULT\s*'([^']+)'", T.ddl.get("evidence_sources", ""), re.I | re.S)
        default = dm.group(1) if dm else None
        lines = [l for p in ("scripts/db.py", "scripts/dbcore.py") if (T.root / p).exists() for l in read(T.root, p).split("\n") if "data_capture_status" in l]
        named = {v: any(re.search(rf"['\"]{re.escape(v)}['\"]", l) for l in lines) for v in vals if v != default}
        miss = sorted(v for v, ok in named.items() if not ok)
        return ("FAIL" if miss else "PASS"), {"default": default, "values_with_no_writer_line": miss, "lexical": True}

    @probe("P-PARAM-LIFECYCLE", "base_parameters.status 'merged' and 'retired' are written by some db.py function", ["LED-169", "LED-170"])
    def _(T):
        vals = (T.vocab.get("base_parameters") or {}).get("status", [])
        reached = {v: [] for v in vals if v != "active"}
        for vb, d in T.verbs.items():
            if "base_parameters" not in d["writes"]: continue
            for fn in d["functions"]:
                src = func_source(T.root, "scripts/db.py", fn) or ""
                for v in reached:
                    if re.search(rf"['\"]{v}['\"]", src) and re.search(r"UPDATE\s+base_parameters", src, re.I): reached[v].append(f"{vb}:{fn}")
        miss = [v for v, w in reached.items() if not w]
        return ("FAIL" if miss else "PASS"), {"vocabulary": vals, "reached_by": reached, "values_with_no_writing_function": miss}

    return P


ATOMS_FOR_PROBES = {}
PROBE_DEFS = {}


def run_probes(T, P):
    res = {}
    for pid, d in P.items():
        try:
            v, ev = d["fn"](T)
        except Exception as e:
            v, ev = "UNKNOWN", {"error": f"{type(e).__name__}: {e}"}
        res[pid] = dict(verdict=v, tests=d["tests"], atoms=d["atoms"], evidence=ev)
    return res


# ----------------------------------------------------------------------------------------------- capabilities
def eval_pred(pred, T, probes, T1=None):
    """-> (verdict, why). Kinds: probe / verb / needle / vocab / rows / hand."""
    k = pred["kind"]
    if k == "probe":
        r = probes[pred["probe"]]["verdict"]
        want = pred.get("expect", "PASS")
        return ("PASS" if r == want else (r if r in ("FAIL", "NOT-BUILT") else "UNKNOWN")), f"{pred['probe']} = {r}"
    if k == "verb":
        ok = pred["verb"] in T.verbs
        return ("PASS" if ok else "NOT-BUILT"), f"verb {pred['verb']} {'declared' if ok else 'absent'} on this tree"
    if k == "needle":
        ok, why = needle_ok(T.root, pred)
        return ("PASS" if ok else "FAIL"), why or "matched"
    if k == "vocab":
        v = (T.vocab.get(pred["table"]) or {}).get(pred["column"], [])
        ok = pred["value"] in v
        return ("PASS" if ok else "FAIL"), f"{pred['table']}.{pred['column']} {'admits' if ok else 'does not admit'} {pred['value']}"
    if k == "rows":
        n = T.rows.get(pred["table"], 0); ok = n >= pred.get("min", 1)
        return ("PASS" if ok else "FAIL"), f"{pred['table']} holds {n} row(s)"
    if k == "writable":
        bad = [x for x in T.unwritable_set() if x["child"] == pred["table"] and not x["parent_written_by_same_verb"]]
        return ("PASS" if not bad else "FAIL"), (f"{pred['table']} has no NOT NULL FK into an emptied table" if not bad else "unwritable: " + ", ".join(f"{x['col']} -> {x['parent']}" for x in bad))
    if k == "hand":
        return pred["verdict"], "HAND-ASSESSED: " + pred["why"]
    return "UNKNOWN", f"unknown predicate kind {k}"


def capability_verdicts(caps, T, probes):
    out = {}
    for cid, c in caps["capabilities"].items():
        preds = []
        for p in c["predicates"]:
            v, why = eval_pred(p, T, probes)
            preds.append(dict(id=p["id"], says=p["says"], verdict=v, why=why, atoms=p.get("atoms", [])))
        vs = [p["verdict"] for p in preds]
        overall = "CAN" if all(v == "PASS" for v in vs) else ("BLOCKED" if any(v in ("FAIL", "NOT-BUILT") for v in vs) else "UNKNOWN")
        out[cid] = dict(name=c["name"], overall=overall, predicates=preds)
    return out


# ----------------------------------------------------------------------------------------------- checks
def cited_atom_ids(probes, conflicts, machines, caps):
    """The atoms something still cites: a conflict, a status correction, a machine, a capability
    predicate or a probe. Only these have their quote verified (W9); ATOMS.tsv marks them."""
    cited = set()
    for c in conflicts["conflicts"]: cited |= set(c["atoms"]) | {i for s in c["sides"] for i in s["atoms"]}
    for sc in conflicts.get("status_corrections", []): cited |= {sc["atom"], *sc["by"]}
    for m in machines["machines"]: cited |= set(m.get("atoms", []))
    for c in caps["capabilities"].values():
        for p in c["predicates"]: cited |= set(p.get("atoms", []))
    for p in probes.values(): cited |= set(p["atoms"])
    return cited


def check_all(T, atoms, probes, conflicts, machines, caps):
    fails, warns, examined = [], [], {}
    # 1 atoms
    # A quote is verified only for an atom a conflict, status correction, machine, predicate or probe
    # still cites (W9): an atom nothing cites is a record, and a resolved entry stops needing its source.
    cited = cited_atom_ids(probes, conflicts, machines, caps)
    stats = {}
    bad = verify_atoms(atoms, only=cited, stats=stats); fails += bad
    examined["atoms in all (structure checked)"] = len(atoms)
    examined["atoms whose quote was read (cited by a conflict, status correction, machine, predicate or probe)"] = stats.get("verified", 0)
    examined["distinct quotes among all atoms"] = len({norm(a["quote"]) for a in atoms.values()})
    # 2 conflicts
    n = 0
    for c in conflicts["conflicts"]:
        n += 1
        if c["class"] not in CLASSES: fails.append(f"{c['id']}: bad class {c['class']}")
        if c["severity"] not in SEVERITY: fails.append(f"{c['id']}: bad severity")
        if c["resolver"] not in RESOLVERS: fails.append(f"{c['id']}: bad resolver")
        for pr in as_list(c.get("probe")):
            if pr not in probes: fails.append(f"{c['id']}: unknown probe {pr}")
        cited = set(c["atoms"]) | {i for s in c["sides"] for i in s["atoms"]}
        for i in cited:
            if i not in atoms: fails.append(f"{c['id']}: atom {i} does not exist")
        if not {i for s in c["sides"] for i in s["atoms"]} <= set(c["atoms"]):
            fails.append(f"{c['id']}: a side cites an atom missing from the top-level atoms list")
        if len(c["sides"]) < 2 and c["class"] not in ("OPEN-QUESTION", "UNRECORDED") and not as_list(c.get("probe")):
            fails.append(f"{c['id']}: a conflict needs two sides")
        for i in cited & set(atoms):
            if atoms[i]["status"] in ("HISTORICAL",):
                warns.append(f"{c['id']}: cites HISTORICAL atom {i}")
    ids = [c["id"] for c in conflicts["conflicts"]]
    if len(ids) != len(set(ids)): fails.append("duplicate conflict ids")
    for sc in conflicts.get("status_corrections", []):
        a = atoms.get(sc["atom"])
        if a is None: fails.append(f"status_corrections: atom {sc['atom']} does not exist"); continue
        if a["status"] != sc["current"]: fails.append(f"status_corrections: {sc['atom']} is now {a['status']}, not {sc['current']} -- the correction was applied or the atom changed; remove or update the entry")
        if sc["should_be"] not in STA or sc["should_be"] == sc["current"]: fails.append(f"status_corrections: {sc['atom']} has a bad should_be")
        for b in sc["by"]:
            if b not in atoms: fails.append(f"status_corrections: {sc['atom']} cites missing atom {b}"); continue
            da, db_ = a.get("date"), atoms[b].get("date")
            if da and db_ and db_ < da: fails.append(f"status_corrections: {sc['atom']} ({da}) is decided by {b} ({db_}), which is EARLIER")
            if atoms[b]["status"] in ("SUPERSEDED", "HISTORICAL"): fails.append(f"status_corrections: {sc['atom']} is decided by {b}, which is itself {atoms[b]['status']}")
    examined["status corrections owed (each atom's status re-read)"] = len(conflicts.get("status_corrections", []))
    examined["conflicts (atoms, class, probe exist)"] = n
    # 3 machines
    nt = ne = vocab_cmp = abstract = 0
    for m in machines["machines"]:
        for a in m.get("atoms", []):
            if a not in atoms: fails.append(f"{m['id']}: atom {a} does not exist")
        if m.get("probe") and m["probe"] not in probes: fails.append(f"{m['id']}: unknown probe {m['probe']}")
        h = m["holder"]
        mm = re.fullmatch(r"(\w+)\.(\w+)", h)
        if mm:
            t, col = mm.groups(); v = (T.vocab.get(t) or {}).get(col)
            if v is None:
                if m.get("abstract"): abstract += 1
                else: warns.append(f"{m['id']}: no CHECK vocabulary found for {h} (states not compared)")
            else:
                derived = set(v) | {"NULL"} if "NULL" in m["states"] else set(v)
                vocab_cmp += 1
                if set(m["states"]) != derived:
                    fails.append(f"{m['id']}: states {sorted(m['states'])} != the column's own CHECK {sorted(derived)}")
        elif m.get("abstract"):
            abstract += 1
        elif not m.get("vocabs"):
            abstract += 1
            warns.append(f"{m['id']}: abstract machine (holder {h!r} is not one column) and declares no `vocabs:`; its states are not compared with any CHECK")
        for vv in m.get("vocabs", []):
            t, col = vv["holder"].split(".")
            v = (T.vocab.get(t) or {}).get(col)
            vocab_cmp += 1
            if v is None: fails.append(f"{m['id']}: vocabs holder {vv['holder']} has no CHECK vocabulary")
            elif set(vv["values"]) != set(v): fails.append(f"{m['id']}: vocabs {vv['holder']} {sorted(vv['values'])} != the column's own CHECK {sorted(v)}")
        for t in m["transitions"]:
            nt += 1
            for e in t["evidence"]:
                ne += 1
                ok, why = needle_ok(T.root, e)
                if not ok: fails.append(f"{t['id']}: {e['file']}[{e.get('func','')}] {why}: {e['needle'][:70]}")
    examined["machine transitions"] = nt; examined["transition evidence needles re-read"] = ne
    examined["state vocabularies compared with a column's own CHECK"] = vocab_cmp; examined["abstract machines (no single column holder)"] = abstract
    # 4 capabilities
    for cid, c in caps["capabilities"].items():
        for p in c["predicates"]:
            if p["kind"] == "probe" and p["probe"] not in probes: fails.append(f"{cid}.{p['id']}: unknown probe {p['probe']}")
            for a in p.get("atoms", []):
                if a not in atoms: fails.append(f"{cid}.{p['id']}: atom {a} does not exist")
    examined["capability predicates"] = sum(len(c["predicates"]) for c in caps["capabilities"].values())
    # 5 probes
    for pid, p in probes.items():
        if p["verdict"] not in VERDICTS: fails.append(f"{pid}: bad verdict {p['verdict']}")
        for a in p["atoms"]:
            if a not in atoms: fails.append(f"{pid}: atom {a} does not exist")
    examined["probes run"] = len(probes)
    # a probe that cannot return PASS (or INFO) makes any capability that expects PASS from it BLOCKED by construction
    import inspect
    for pid, d in PROBE_DEFS.items():
        srcp = inspect.getsource(d["fn"])
        if '"PASS"' not in srcp and '"INFO"' not in srcp: fails.append(f"{pid}: the probe has no path that returns PASS or INFO")
    examined["probes linted for a reachable PASS"] = len(PROBE_DEFS)
    # 6 stage coverage and spine
    miss = sorted(set(T.tables) - set(T.t2s)); stale = sorted(set(T.t2s) - set(T.tables))
    unk = sorted({s for s in T.t2s.values() if s not in T.stages and s != "infrastructure"})
    if miss: fails.append(f"tables in the schema but not in stage-map: {miss}")
    if stale: fails.append(f"tables in stage-map but not in the schema: {stale}")
    if unk: fails.append(f"stage ids in stage-map that the contract does not define: {unk}")
    spine = "SPINE: " + " -> ".join(T.stages)
    if spine not in read(T.root, "CLAUDE.md"): fails.append(f"CLAUDE.md spine line differs from the contract: {spine}")
    examined["tables placed in a stage"] = len(T.tables)
    # 7 unwritable x verbs: a verb that writes a table the derivation lists as unwritable
    return fails, warns, examined


def selftest(T, atoms, probes, conflicts, machines, caps):
    """Show each class of check can fail. CLAUDE.md section 5(a): a gate that cannot go red tells you nothing."""
    results = []
    # a) a mutated quote is caught
    a2 = copy.deepcopy(atoms); k = next(iter(a2)); a2[k]["quote"] = "zzz this sentence is not in any source zzz"
    results.append(("mutated atom quote is caught", bool(verify_atoms({k: a2[k]}))))
    # b) a bad atom id in a conflict is caught
    c2 = copy.deepcopy(conflicts); c2["conflicts"][0]["atoms"].append("ZZZ-999")
    f, _, _ = check_all(T, atoms, probes, c2, machines, caps)
    results.append(("conflict citing a missing atom is caught", any("ZZZ-999" in x for x in f)))
    # c) a falsified needle is caught
    m2 = copy.deepcopy(machines); m2["machines"][0]["transitions"][0]["evidence"][0]["needle"] = "zzz-not-present-zzz"
    f, _, _ = check_all(T, atoms, probes, conflicts, m2, caps)
    results.append(("falsified transition needle is caught", any("zzz-not-present" in x for x in f)))
    # d) an `absent` needle that matches is caught
    m3 = copy.deepcopy(machines)
    ev = m3["machines"][0]["transitions"][0]["evidence"][0]; ev["absent"] = True
    f, _, _ = check_all(T, atoms, probes, conflicts, m3, caps)
    results.append(("claimed-absent pattern that is present is caught", any("claimed absent" in x for x in f)))
    # e) a state vocabulary that drifts from the column's CHECK is caught
    m4 = copy.deepcopy(machines)
    for m in m4["machines"]:
        if m["holder"] == "search_candidates.disposition": m["states"] = m["states"][:-1]
    f, _, _ = check_all(T, atoms, probes, conflicts, m4, caps)
    results.append(("machine states that differ from the CHECK are caught", any("column's own CHECK" in x for x in f)))
    # a2) mutated quotes on a random sample (seed fixed), not only the first atom
    import random
    rng = random.Random(7); sample = rng.sample(sorted(atoms), 5); caught = 0
    for i in sample:
        a3 = copy.deepcopy(atoms[i]); a3["quote"] = "zzz mutated zzz " + a3["quote"]
        caught += bool(verify_atoms({i: a3}))
    results.append((f"verify_atoms catches mutated quotes on 5 random atoms ({caught}/5; the function, not the --check gate: see m)", caught == 5))
    # m) THE GATE (check_all), not the function: a bad quote on an atom something cites is caught; on one nothing cites it is
    #    not read (W9); and the EXAMINED figure is the number of quotes actually read, so a gate wired to read none cannot pass.
    cited_ids = cited_atom_ids(probes, conflicts, machines, caps)
    ci = sorted(cited_ids & set(atoms))[0]; ui = sorted(set(atoms) - cited_ids)[0]
    for tag, i, want in (("cited", ci, True), ("uncited", ui, False)):
        a4 = copy.deepcopy(atoms); a4[i]["quote"] = "zzz mutated zzz " + a4[i]["quote"]
        f, _, ex = check_all(T, a4, probes, conflicts, machines, caps)
        results.append((f"--check {'catches' if want else 'does not read'} a mutated quote on a {tag} atom", any(i in x for x in f) == want))
    f, _, ex = check_all(T, atoms, probes, conflicts, machines, caps)
    results.append(("the EXAMINED quote count equals the cited atoms actually read",
                    ex["atoms whose quote was read (cited by a conflict, status correction, machine, predicate or probe)"] == len(cited_ids & set(atoms))))
    # g) a table dropped from the stage map is caught
    saved = T.t2s.pop("specifications")
    f, _, _ = check_all(T, atoms, probes, conflicts, machines, caps); T.t2s["specifications"] = saved
    results.append(("a table missing from stage-map is caught", any("not in stage-map" in x for x in f)))
    # h) a probe that cannot return PASS/INFO is caught by the lint
    PROBE_DEFS["P-FAKE"] = dict(fn=(lambda T: ("FAIL", {})), tests="x", atoms=[])
    pr2 = dict(probes); pr2["P-FAKE"] = dict(verdict="FAIL", tests="x", atoms=[], evidence={})
    f, _, _ = check_all(T, atoms, pr2, conflicts, machines, caps); del PROBE_DEFS["P-FAKE"]
    results.append(("a probe with no reachable PASS is caught", any("P-FAKE" in x and "no path" in x for x in f)))
    # i) capability verdicts can say both CAN and BLOCKED, and a predicate can say both PASS and FAIL
    #    The probe verdicts are planted: a case that reads a live probe turns "n/a" the day that probe flips.
    planted_probes = {"P-PASS": dict(verdict="PASS"), "P-FAIL": dict(verdict="FAIL")}
    cap = lambda pid: {"capabilities": {"X": {"name": "x", "asks": "", "predicates": [{"id": "X.1", "kind": "probe", "probe": pid, "says": "s"}]}}}
    results.append(("a capability can come out CAN and can come out BLOCKED",
                    capability_verdicts(cap("P-PASS"), T, planted_probes)["X"]["overall"] == "CAN"
                    and capability_verdicts(cap("P-FAIL"), T, planted_probes)["X"]["overall"] == "BLOCKED"))
    # the FAIL case is planted in a scratch copy of the database, so `unwritable_set` itself derives it (the live schema may hold no such pair)
    with tempfile.TemporaryDirectory() as td:
        for d in ("governance", "scripts", ".github"): os.symlink(REPO / d, Path(td) / d)      # what Tree reads besides the database
        (Path(td) / "data").mkdir(); shutil.copy(REPO / "data" / "guidebook.db", Path(td) / "data" / "guidebook.db")
        cx = sqlite3.connect(Path(td) / "data" / "guidebook.db")
        cx.executescript("create table zzz_parent(id integer primary key); create table zzz_child(p integer not null references zzz_parent(id));"); cx.commit(); cx.close()
        w1 = eval_pred({"kind": "writable", "table": "specifications"}, T, probes)[0]; w2 = eval_pred({"kind": "writable", "table": "zzz_child"}, Tree(td), probes)[0]
    results.append(("the `writable` predicate can say PASS and can say FAIL", {w1, w2} == {"PASS", "FAIL"}))
    # j) a machine `vocabs` entry that differs from the CHECK is caught
    m5 = copy.deepcopy(machines)
    for m in m5["machines"]:
        if m["id"] == "M08": m["vocabs"][0]["values"] = m["vocabs"][0]["values"][:-1]
    f, _, _ = check_all(T, atoms, probes, conflicts, m5, caps)
    results.append(("a machine `vocabs` list that differs from the CHECK is caught", any("M08: vocabs" in x for x in f)))
    # k) a stale status correction (the atom is no longer in the stated state) is caught.
    #    Applied corrections are deleted (W9), so the list may be empty: the test plants its own.
    dated = sorted((a for a in atoms.values() if a.get("date") and a["status"] == "ACTIVE"), key=lambda a: a["date"])
    late, early = dated[-1], dated[0]
    def planted(**kw):
        c = copy.deepcopy(conflicts)
        c["status_corrections"] = [dict({"atom": late["id"], "current": late["status"], "should_be": "SUPERSEDED", "by": [early["id"]], "why": "planted by the selftest"}, **kw)]
        return c
    c4 = planted(current="HISTORICAL")
    f, _, _ = check_all(T, atoms, probes, c4, machines, caps)
    results.append(("a stale status correction is caught", any("status_corrections" in x for x in f)))
    # l) a quote cited at the wrong line is caught
    a6 = copy.deepcopy(atoms[sorted(atoms)[0]]); path_, _, ln_ = a6["source"].rpartition(":")
    a6["source"] = f"{path_}:{int(ln_) + 40}" if ln_.isdigit() else a6["source"]
    results.append(("a quote cited 40 lines away from where it occurs is caught", bool(verify_atoms({a6['id']: a6})) if ln_.isdigit() else True))
    # m) a status correction decided by an EARLIER atom is caught
    c5 = planted()
    f, _, _ = check_all(T, atoms, probes, c5, machines, caps)
    results.append(("a status correction decided by an earlier atom is caught", any("EARLIER" in x for x in f)))
    # f) an unknown probe id is caught
    c3 = copy.deepcopy(conflicts); c3["conflicts"][0]["probe"] = "P-NOPE"
    f, _, _ = check_all(T, atoms, probes, c3, machines, caps)
    results.append(("unknown probe id is caught", any("P-NOPE" in x for x in f)))
    return results


# ----------------------------------------------------------------------------------------------- rendering
def mdtable(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def mer_id(s):
    return re.sub(r"[^A-Za-z0-9]", "_", s)


def render_state_graph(T, atoms, probes, machines, cmp_info, stamp):
    L = [f"# Pipeline state graph", "",
         f"_GENERATED by `build_graph.py` -- do not edit. {stamp}. Re-run rather than trust any number below (CLAUDE.md rule 7a)._", "",
         "Source tree: `" + str(T.root) + f"` at schema version `{T.user_version}`.", "",
         "## 1. The spine, and what each stage holds", "",
         "`SPINE: " + " -> ".join(T.stages) + "`  (derived from `governance/pipeline-contract.yaml`; checked against `CLAUDE.md`)", ""]
    by_stage = collections.defaultdict(list)
    for t in T.tables: by_stage[T.stage(t)].append(t)
    rows = []
    for s in T.stages + ["infrastructure"]:
        ts = by_stage.get(s, [])
        rows.append((s, len(ts), sum(T.rows[t] for t in ts), len([t for t in ts if T.rows[t] == 0]), len([t for t in ts if t not in T.writers])))
    L.append(mdtable(["stage", "tables", "rows", "empty tables", "tables no db.py verb writes"], rows)); L.append("")
    # mermaid: stages and the cross-stage FK edge counts
    cross = collections.Counter()
    for f in T.fks:
        a, b = T.stage(f["child"]), T.stage(f["parent"])
        if a != b and "infrastructure" not in (a, b): cross[(a, b)] += 1
    L += ["## 2. Stage graph (arrow = child table's foreign key points at the parent stage)", "", "```mermaid", "flowchart LR"]
    for s in T.stages: L.append(f"  {mer_id(s)}[\"{s}\\n{len(by_stage.get(s, []))} tables\"]")
    for (a, b), n in sorted(cross.items()): L.append(f"  {mer_id(a)} -->|{n} fk| {mer_id(b)}")
    L += ["```", ""]
    L += ["Cross-stage FKs are the pointers (CLAUDE.md rule 5). Count by direction:", "",
          mdtable(["child stage", "points at", "FKs"], [(a, b, n) for (a, b), n in sorted(cross.items())]), ""]
    order = {s: i for i, s in enumerate(T.stages)}
    fwd = [(f"{f['child']}.{f['col']} -> {f['parent']}", T.stage(f["child"]), T.stage(f["parent"]), T.rows[f["child"]]) for f in T.fks
           if T.stage(f["child"]) in order and T.stage(f["parent"]) in order and order[T.stage(f["child"])] < order[T.stage(f["parent"])]]
    L += ["### 2a. Forward-pointing foreign keys (earlier stage's table -> later stage's table)", "",
          "Pointers are meant to run from a later stage back to an earlier one (CLAUDE.md rule 5; re-entrancy, CLAUDE.md section 3, allows a walk to come back). These run the other way. A row count of 0 on the child means the dependency is structural only.", "",
          mdtable(["foreign key", "child stage", "parent stage", "child rows"], fwd) if fwd else "_None._", ""]
    # machines
    L += ["## 3. State machines (hand-verified transitions; vocabularies derived from each column's own CHECK)", ""]
    for m in machines["machines"]:
        L += [f"### {m['id']} {m['name']}  _(stage: {m['stage']})_", "", f"State holder: `{m['holder']}`" + (f"  ·  probe `{m['probe']}` = **{probes[m['probe']]['verdict']}**" if m.get("probe") else ""), ""]
        if all(re.fullmatch(r"[A-Za-z0-9_\-]+", s) for s in m["states"]):
            L += ["```mermaid", "stateDiagram-v2"]
            for t in m["transitions"]:
                if t.get("claim") and t["to"] in ("merged | retired", "not_applicable"): continue
                fr = "[*]" if t["from"].startswith("(none)") else mer_id(t["from"]) if t["from"] in m["states"] else None
                to = mer_id(t["to"]) if t["to"] in m["states"] else None
                if fr and to: L.append(f"  {fr} --> {to}: {t['via'].split(' ')[0] + ' ' + t['via'].split(' ')[1] if t['via'].startswith('db.py') else t['id']}")
            L += ["```", ""]
        L.append(mdtable(["edge", "from", "to", "via", "guards / claim", "evidence"],
                         [(t["id"], t["from"], t["to"], t["via"], "; ".join(t["guards"]) or t.get("claim", ""),
                           "; ".join(f"{e['file']}" + (f"::{e['func']}" if e.get("func") else "") + (" (absent)" if e.get("absent") else "") for e in t["evidence"])) for t in m["transitions"]]))
        if m.get("unreachable_note"): L += ["", f"_Note: {m['unreachable_note']}_"]
        L.append("")
    # tables
    L += ["## 4. Table inventory (derived)", ""]
    unw = {(x["child"]): x for x in T.unwritable_set()}
    rows = []
    for t in T.tables:
        flags = []
        if T.rows[t] == 0: flags.append("EMPTY")
        if t not in T.writers: flags.append("NO-WRITER")
        if t in unw: flags.append("UNWRITABLE" + ("*" if unw[t]["parent_written_by_same_verb"] else ""))
        lens = [c for c in T.cols(t) if c in ("identity_code", "icf_code", "needs_code", "medical_code", "population_code")]
        rows.append((t, T.stage(t), T.rows[t], ", ".join(T.writers.get(t, [])) or "--", ", ".join(lens) or "--", " ".join(flags)))
    L.append(mdtable(["table", "stage", "rows", "db.py verbs that write it", "lens / population columns", "flags"], rows))
    L += ["", "`UNWRITABLE` = a NOT NULL foreign key points into an emptied table (CLAUDE.md section 4). `*` = a verb that writes the child also writes the parent in one call, so the table is writable through that verb. `NO-WRITER` = no `db.py` verb names the table in an INSERT/UPDATE/DELETE (lexical; a table written by another script is listed too).", ""]
    # views
    L += ["## 5. Views and the stages they span", ""]
    vi = T.view_info()
    L.append(mdtable(["view", "stages read", "crosses stages", "rows"], [(v, ", ".join(i["stages"]) or "--", "YES" if i["crosses"] else "", i["rows"]) for v, i in vi.items()]))
    L += ["", "A view with 0 rows is unproven, not clean (CLAUDE.md rule 4).", ""]
    # verbs
    L += ["## 6. Verbs that write nothing a table can hold, and verbs whose targets are unwritable", ""]
    dead = []
    for v, d in T.verbs.items():
        tw = list(d["writes"])
        if tw and all(t in unw and not unw[t]["parent_written_by_same_verb"] for t in tw): dead.append((v, ", ".join(tw)))
    L.append(mdtable(["verb", "tables it writes (all unwritable)"], dead) if dead else "_None._"); L.append("")
    # probes
    L += ["## 7. Ruling-versus-mechanism probes (re-run on every build)", "",
          mdtable(["probe", "verdict", "tests", "atoms", "evidence"], [(pid, f"**{p['verdict']}**", p["tests"], ", ".join(p["atoms"]), json.dumps(p["evidence"], ensure_ascii=False, default=str)[:330]) for pid, p in probes.items()]), ""]
    L += ["Verdicts: `PASS` the mechanism carries the ruling; `FAIL` it contradicts it; `NOT-BUILT` the ruled construct does not exist; `UNKNOWN` the probe cannot decide; `INFO` descriptive.", ""]
    # quarantine
    q = [x for x in (T.registry.get("quarantine") or []) if x.get("status") == "quarantined"]
    L += ["## 8. Quarantined and retired checks (what is NOT gating)", "",
          mdtable(["check", "status", "first sentence of the recorded reason"], [(x["id"], x["status"], norm(x.get("reason", ""))[:200]) for x in (T.registry.get("quarantine") or [])]), ""]
    if cmp_info:
        L += ["## 9. Delta against the comparison tree", ""] + cmp_info + [""]
    return "\n".join(L)


def render_conflicts(conflicts, atoms, probes):
    L = ["# Active-conflicts register", "",
         "_Rendered from `conflicts.yaml` by `build_graph.py`. A conflict here is an adjudicated disagreement between ACTIVE atoms, or between an atom and a measured mechanism; "
         "the mechanical detector's candidate pairs are not conflicts until they are written into `conflicts.yaml`. Nothing here is a ruling._", ""]
    cs = conflicts["conflicts"]
    c = collections.Counter(x["severity"] for x in cs); k = collections.Counter(x["class"] for x in cs)
    L += [f"{len(cs)} entries. Severity: " + ", ".join(f"{s} {c[s]}" for s in sorted(c)) + ". Class: " + ", ".join(f"{s} {k[s]}" for s in sorted(k)) + ".", "",
          "## Index", "", mdtable(["id", "sev", "class", "resolver", "probe -> live verdict", "title"],
                              [(x["id"], x["severity"], x["class"], x["resolver"], (", ".join(f"{p} -> {probes[p]['verdict']}" for p in as_list(x.get("probe"))) or "--"), x["title"]) for x in sorted(cs, key=lambda y: (y["severity"], y["id"]))]), ""]
    sc = conflicts.get("status_corrections", [])
    if sc:
        L += ["## Status corrections owed", "", "Atoms whose recorded status is behind a later statement. The atom files record each document's own markers; these are the supersessions the documents themselves do not carry. Applying one means editing the atom's `status` and `superseded_by`; the check then fails until the entry here is removed.", "",
              mdtable(["atom", "now", "should be", "decided by", "why"], [(x["atom"], x["current"], x["should_be"], ", ".join(x["by"]), x["why"]) for x in sc]), ""]
    for x in sorted(cs, key=lambda y: (y["severity"], y["id"])):
        L += [f"## {x['id']} [{x['severity']}] {x['title']}", "", f"**Class** {x['class']}  ·  **Resolver** {x['resolver']}  ·  **Confidence** {x['confidence']}" +
              ("".join(f"  ·  **Probe** `{p}` = **{probes[p]['verdict']}**" for p in as_list(x.get("probe")))), ""]
        for s in x["sides"]:
            L.append("- " + s["says"] + "  \n  _atoms:_ " + ", ".join(f"`{i}`({atoms[i]['status'][:3].lower()})" for i in s["atoms"]))
        L += ["", "**Direction.** " + x["direction"], ""]
        if x.get("note"): L += [f"_Note: {x['note']}_", ""]
    return "\n".join(L)


def render_caps(caps, cv, caps_t1, probes):
    L = ["# Capability interrogation", "",
         "_Rendered from `capabilities.yaml` by `build_graph.py`. Each predicate is evaluated against the live tree (a probe, a verb, a needle in code, a column's CHECK, a row count) or marked HAND-ASSESSED. "
         "`CAN` = every predicate passes; `BLOCKED` = at least one fails or its construct does not exist; `UNKNOWN` = no failure but a predicate could not be decided._", ""]
    L += [caps["intro"].strip(), ""]
    L += ["## Summary", "", mdtable(["capability", "this tree" ] + (["comparison tree"] if caps_t1 else []),
                                    [(f"{cid} {c['name']}", f"**{c['overall']}**") + ((f"**{caps_t1[cid]['overall']}**",) if caps_t1 else ()) for cid, c in cv.items()]), ""]
    for cid, c in cv.items():
        L += [f"## {cid} {c['name']}", "", caps["capabilities"][cid]["asks"].strip(), ""]
        t1 = {p["id"]: p for p in caps_t1[cid]["predicates"]} if caps_t1 else {}
        L.append(mdtable(["pred", "says", "verdict" ] + (["comparison"] if caps_t1 else []) + ["why", "atoms"],
                         [(p["id"], p["says"], f"**{p['verdict']}**") + ((t1[p["id"]]["verdict"],) if caps_t1 else ()) + (p["why"], ", ".join(p["atoms"])) for p in c["predicates"]]))
        L.append("")
    L += ["## Components against the four capabilities", "",
          mdtable(["component", "stage", "C1", "C2", "C3", "C4", "what it does for the capability / what stops it"],
                  [(x["name"], x["stage"], *(x.get(k, "--") for k in ("C1", "C2", "C3", "C4")), x["note"]) for x in caps["components"]]), ""]
    return "\n".join(L)


# ----------------------------------------------------------------------------------------------- tree comparison
def tree_delta(A, B):
    L = [f"Comparison tree `{B.root}` at schema version `{B.user_version}` against `{A.root}` at `{A.user_version}`.", ""]
    ta, tb = set(A.tables), set(B.tables)
    L += [f"- tables only in comparison: {sorted(tb - ta) or 'none'}", f"- tables only in this tree: {sorted(ta - tb) or 'none'}",
          f"- views only in comparison: {sorted(set(B.views) - set(A.views)) or 'none'}", f"- views only in this tree: {sorted(set(A.views) - set(B.views)) or 'none'}",
          f"- db.py verbs only in comparison: {sorted(set(B.verbs) - set(A.verbs)) or 'none'}", f"- db.py verbs only in this tree: {sorted(set(A.verbs) - set(B.verbs)) or 'none'}"]
    ca = {t: set(A.cols(t)) for t in ta & tb}; cb = {t: set(B.cols(t)) for t in ta & tb}
    chg = {t: dict(added=sorted(cb[t] - ca[t]), dropped=sorted(ca[t] - cb[t])) for t in ca if ca[t] != cb[t]}
    L += [f"- tables whose columns differ: {json.dumps(chg) if chg else 'none'}"]
    return L


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify only; write nothing")
    ap.add_argument("--selftest", action="store_true", help="mutation tests of the checks")
    ap.add_argument("--compare", default=None, help="a second checkout to diff against (e.g. the unreleased tooling branch)")
    ap.add_argument("--repo", default=str(REPO))
    args = ap.parse_args()

    atoms, dups = load_atoms()
    ATOMS_FOR_PROBES.update(atoms)
    conflicts = yaml.safe_load(open(HERE / "conflicts.yaml", encoding="utf-8"))
    machines = yaml.safe_load(open(HERE / "machines.yaml", encoding="utf-8"))
    caps = yaml.safe_load(open(HERE / "capabilities.yaml", encoding="utf-8"))
    T = Tree(args.repo); P = make_probes(); probes = run_probes(T, P)
    fails, warns, examined = check_all(T, atoms, probes, conflicts, machines, caps)
    fails += dups

    if args.selftest:
        res = selftest(T, atoms, probes, conflicts, machines, caps)
        for name, ok in res: print(("PASS  " if ok else "FAIL  ") + name)
        print(f"EXAMINED: {len(res)} mutation tests")
        sys.exit(0 if all(ok for _, ok in res) else 1)

    for k, v in examined.items(): print(f"EXAMINED: {v:>5}  {k}")
    for w in warns: print("WARN  ", w)
    for f in fails: print("FAIL  ", f)
    print(f"{len(fails)} failure(s), {len(warns)} warning(s)")
    if args.check:
        sys.exit(1 if fails else 0)

    T2 = Tree(args.compare) if args.compare else None
    probes2 = run_probes(T2, P) if T2 else None
    cv = capability_verdicts(caps, T, probes); cv2 = capability_verdicts(caps, T2, probes2) if T2 else None
    cmp_info = tree_delta(T, T2) if T2 else None
    if T2:
        cmp_info += ["", "Probe verdicts that differ:", "", mdtable(["probe", "this tree", "comparison tree"], [(p, probes[p]["verdict"], probes2[p]["verdict"]) for p in probes if probes[p]["verdict"] != probes2[p]["verdict"]] or [("--", "--", "--")])]
    head = subprocess.run(["git", "-C", str(T.root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    stamp = f"Generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC from git HEAD {head or 'unknown'} (working tree, uncommitted changes included)"
    (HERE / "STATE-GRAPH.md").write_text(render_state_graph(T, atoms, probes, machines, cmp_info, stamp) + "\n", encoding="utf-8")
    (HERE / "CONFLICTS.md").write_text(render_conflicts(conflicts, atoms, probes) + "\n", encoding="utf-8")
    (HERE / "CAPABILITIES.md").write_text(render_caps(caps, cv, cv2, probes) + "\n", encoding="utf-8")

    def tsv(name, rows, hdr):
        with open(HERE / name, "w", encoding="utf-8") as fh:
            fh.write("\t".join(hdr) + "\n")
            for r in rows: fh.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    A = list(atoms.values()); cited = cited_atom_ids(probes, conflicts, machines, caps)
    tsv("ATOMS.tsv", [(a["id"], a["status"], a["modality"], a["speaker"], a.get("date") or "", a["source"], ",".join(a["scope"].get("stages", [])) if isinstance(a.get("scope"), dict) else "", a["subject"], a["claim"], a.get("enforcement") or "", "yes" if a["id"] in cited else "no") for a in A],
        ["id", "status", "modality", "speaker", "date", "source", "stages", "subject", "claim", "enforcement", "quote_checked"])
    tsv("OPEN-QUESTIONS.tsv", [(a["id"], a["source"], a["subject"], a["claim"]) for a in A if a["status"] in ("OPEN", "PROPOSED")], ["id", "source", "subject", "claim"])
    tsv("AMBIGUITIES.tsv", [(a["id"], a["status"], a["source"], a["subject"], a["ambiguity"]) for a in A if a.get("ambiguity")], ["id", "status", "source", "subject", "ambiguity"])
    graph = dict(generated=stamp, tree=str(T.root), user_version=T.user_version, stages=T.stages,
                 tables={t: dict(stage=T.stage(t), rows=T.rows[t], writers=T.writers.get(t, []), cols=T.cols(t)) for t in T.tables},
                 fks=T.fks, unwritable=T.unwritable_set(), views=T.view_info(), vocab=T.vocab, verbs=T.verbs,
                 probes={k: dict(verdict=v["verdict"], tests=v["tests"], atoms=v["atoms"], evidence=v["evidence"]) for k, v in probes.items()},
                 probes_comparison=({k: v["verdict"] for k, v in probes2.items()} if probes2 else None),
                 capabilities=cv, capabilities_comparison=cv2, examined=examined,
                 atoms_by_status=dict(collections.Counter(a["status"] for a in A)), atoms_total=len(A), conflicts_total=len(conflicts["conflicts"]))
    (HERE / "graph.json").write_text(json.dumps(graph, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("wrote STATE-GRAPH.md CONFLICTS.md CAPABILITIES.md graph.json ATOMS.tsv OPEN-QUESTIONS.tsv AMBIGUITIES.tsv")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
