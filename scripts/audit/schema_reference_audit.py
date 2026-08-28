#!/usr/bin/env python3
"""
scripts/audit/schema_reference_audit.py — every table a caller names must exist.

WHY THIS EXISTS (CLAUDE.md §1 burden of proof). Rule 4 says a rename is not done
until the callers are swept, and that "a 0-row object is unproven, not clean":
33 of 66 tables hold no rows, so a reader left pointing at a table that no longer
exists renders NOTHING and every downstream diff certifies it. Migration 064 was
needed because 063 swept eight Python readers and six skills and missed
v_item_provenance. This check is the mechanical form of that sweep: it reads the
live schema, reads every SQL identifier a caller names, and fails on any name the
schema does not have.

What reaches the guidebook if it does not exist: a rendered page that silently
drops a section, because the query behind it named a table that was renamed and
nobody ran the one query that would have said so.

Scope is deliberately the EXECUTABLE and INSTRUCTIONAL surface -- scripts, tools,
schemas, governance YAML, skills. Prose is not a caller. Frozen records are not
callers either, and are excluded by the same list §7 gives for .ignore.
"""
import os, re, sqlite3, sys, argparse, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.environ.get("GUIDEBOOK_DB_PATH", os.path.join(ROOT, "data", "guidebook.db"))

SCAN = ("scripts/", "tools/", "schemas/", "governance/", "skills/", ".github/workflows/")
SKIP = ("scripts/migrations/", "skills/deprecated/", "_archived/", "versions/",
        "audits/", "sessions/", "scratchpad/", "workplan/", "working/")
EXTS = (".py", ".sh", ".yaml", ".yml", ".md", ".sql")
EXEMPTIONS = os.path.join("governance", "schema-reference-exemptions.yaml")

# TWO filters, and the first one is what makes this check usable. A first draft
# matched FROM/INTO/UPDATE anywhere and reported 2,003 references to 516 names --
# English prose in skill files, `from x import y` in Python, "update the register"
# in a workplan. A gate that reports everything reports nothing, which is §2(a)'s
# sibling failure. So: find SQL REGIONS first, then look for identifiers in them.
#
# A SQL region is a string literal, code fence or YAML value that contains a
# CAPITALISED SQL verb. This repository writes SQL in caps throughout; requiring
# that alone removes every prose false positive measured.
SQL_REGION = re.compile(
    r"""(?xs)
    (?: \"\"\" .*? \"\"\"                   # python triple-quoted
      | \'\'\' .*? \'\'\'
      | ```      .*? ```                       # markdown fence
      | `[^`\n]+`                              # markdown inline code
      | "[^"\n]*"                              # single-line strings
      | '[^'\n]*'
    )""")
SQL_VERB = re.compile(r"\b(?:SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+"
                      r"(?:TABLE|VIEW|INDEX)|ALTER\s+TABLE|DROP\s+(?:TABLE|VIEW)|"
                      r"PRAGMA|REFERENCES)\b")
# Inside a SQL region, THESE positions hold a table or view name.
CTX = re.compile(
    r"(?:FROM|JOIN|INTO|UPDATE|REFERENCES|CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?|"
    r"CREATE\s+VIEW|ALTER\s+TABLE|DROP\s+TABLE|DROP\s+VIEW|"
    r"table_info\(|table_xinfo\(|foreign_key_list\(|index_list\()"
    r"\s*[\"'`]?([a-z][a-z0-9_]{3,})")
IDENT = re.compile(r"^[a-z][a-z0-9_]{3,}$")


def live(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    return {r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}


def scan(root):
    for base in SCAN:
        for dirpath, _, names in os.walk(os.path.join(root, base)):
            rel = os.path.relpath(dirpath, root) + os.sep
            if any(rel.startswith(s) for s in SKIP) or "__pycache__" in dirpath:
                continue
            for n in names:
                if n.endswith(EXTS):
                    yield os.path.join(dirpath, n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    schema = live(a.db)
    # SQL keywords and CTE/alias names that sit in the same grammatical slot.
    noise = {"select", "where", "as", "on", "set", "values", "if", "not", "exists",
             "sqlite_master", "sqlite_sequence", "pragma", "temp", "main", "and",
             "or", "by", "order", "group", "limit", "distinct", "case", "when",
             "then", "else", "end", "null", "left", "inner", "outer", "cross",
             "union", "all", "count", "sum", "table", "view", "index", "f",
             "json_each", "json_tree"}

    findings, examined, files = [], 0, 0
    for path in sorted(scan(ROOT)):
        try:
            txt = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        files += 1
        for region in SQL_REGION.finditer(txt):
            body = region.group(0)
            if not SQL_VERB.search(body):
                continue
            for m in CTX.finditer(body):
                name = m.group(1)
                if name in noise or not IDENT.match(name) or "__" in name:
                    continue
                # A bare English word after an uppercase SQL verb inside a
                # DOCSTRING is prose, not a table: "an UPDATE statement's SET
                # clause", "an UPDATE changes no count". Every real table name in
                # this schema is snake_case or a plain plural, so report a bare
                # word only when it is a near-miss of a live name -- which is
                # precisely the class that matters (`specification` for
                # `specifications`, `room` for `rooms`).
                if "_" not in name and name not in schema and not (
                        name + "s" in schema or name + "es" in schema
                        or name.rstrip("s") in schema):
                    continue
                examined += 1
                if name not in schema:
                    line = txt.count("\n", 0, region.start() + m.start()) + 1
                    findings.append({"file": os.path.relpath(path, ROOT),
                                     "line": line, "name": name})

    # A name DEFINED nearby is not a schema miss. Locality is DIRECTORY-scoped,
    # not per-file: scripts/audit/graph/ builds its own SQLite from schema.sql and
    # queries it from six other modules, so a per-file rule reported 32 of those
    # references as missing tables. Three real cases, all measured -- a sibling
    # database, selftest fixtures, and CTEs.
    defined = {}
    for path in sorted(scan(ROOT)):
        try:
            txt = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        names = (set(re.findall(r"CREATE\s+(?:TEMP\s+)?(?:TABLE|VIEW)\s+"
                                r"(?:IF\s+NOT\s+EXISTS\s+)?[\"'`]?(\w+)", txt, re.I))
                 | set(re.findall(r"\bWITH\s+(?:RECURSIVE\s+)?(\w+)\s+AS", txt, re.I))
                 | set(re.findall(r"[,)]\s*(\w+)\s+AS\s*\(", txt)))
        defined.setdefault(os.path.dirname(path), set()).update(names)

    def visible(f):
        """Names defined in this file's directory, its ancestors, or its
        subpackages. Both directions, because scripts/audit/graph/schema.sql
        defines the graph database that scripts/audit/graph_audit.py -- its
        PARENT -- queries. A package and its subpackages share a schema."""
        d = os.path.dirname(os.path.join(ROOT, f))
        out = set(defined.get(d, set()))
        for other, names in defined.items():
            if other.startswith(d + os.sep):
                out |= names
        up = d
        while up.startswith(ROOT) and up != ROOT:
            up = os.path.dirname(up)
            out |= defined.get(up, set())
        return out

    findings = [x for x in findings if x["name"] not in visible(x["file"])]

    # Exemptions carry a REASON and are reported when nothing matches them, so an
    # exemption cannot outlive the thing it exempts. Same discipline as the
    # insurance harness's waivers, for the same reason.
    ex, stale = {}, []
    exp = os.path.join(ROOT, EXEMPTIONS)
    if os.path.exists(exp):
        try:
            import yaml
            ex = yaml.safe_load(open(exp)) or {}
        except Exception as e:
            print(f"  NOTE: could not read {EXEMPTIONS}: {e}")
    known = []
    if ex:
        used = {x["name"] for x in findings} & set(ex)
        stale = sorted(set(ex) - used)
        known = [x for x in findings if x["name"] in ex]
        findings = [x for x in findings if x["name"] not in ex]

    if a.json:
        print(json.dumps(findings, indent=1)); return 1 if findings else 0

    print(f"EXAMINED: {examined} SQL identifier references in {files} files"
          f" against {len(schema)} live tables and views")
    for name in sorted({x["name"] for x in known}):
        sites = [f"{x['file']}:{x['line']}" for x in known if x["name"] == name]
        print(f"  KNOWN: {name}  ({len(sites)} site(s)) — {' '.join(ex[name].split())}")
    for name in stale:
        findings.append({"file": EXEMPTIONS, "line": 0, "name": name})
        print(f"  STALE EXEMPTION: {name!r} is exempted but nothing references it"
              f" — reason on file: {ex[name]}")
    if not findings:
        print("RESULT: PASS — every table and view a caller names exists")
        return 0
    by = {}
    for x in findings:
        by.setdefault(x["name"], []).append(f"{x['file']}:{x['line']}")
    for name in sorted(by, key=lambda k: -len(by[k])):
        print(f"  MISSING: {name}  ({len(by[name])} site(s))")
        for s in by[name][:6]:
            print(f"      {s}")
        if len(by[name]) > 6:
            print(f"      ... and {len(by[name]) - 6} more")
    print(f"RESULT: FAIL — {len(findings)} reference(s) to"
          f" {len(by)} name(s) the schema does not have")
    return 1


if __name__ == "__main__":
    sys.exit(main())
