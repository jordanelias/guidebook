#!/usr/bin/env python3
"""Sweep callers for migration 065's renames. One-shot, committed for the record.

Rule 4: a rename is not done until the callers are swept, and a sweep that stops
at the filename is not a sweep. This does the part that is MECHANICAL and safe,
and REPORTS everything else rather than guessing -- because the dangerous half of
this rename is not the table names, it is `population_code`, which is a registry
primary key in one place (-> `code`) and a link column in another
(-> `identity_code`), and no regex can tell those apart.

  --apply     rewrite files in place
  (default)   report only

Scope, and why: the SQL regions the schema_reference_audit gate can see, plus
quoted string literals that are EXACTLY a table name (the `TABLES = [...]` and
`table_info("slugs")` forms the region rule cannot see). Prose is not a caller.
Frozen records are not callers. Generated output is regenerated, not swept.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "scripts", "audit"))
import schema_reference_audit as A          # the region detector, shared not copied

DECL = os.environ.get("DECL_DIR", "/tmp/decl")
MAP = json.load(open(f"{DECL}/map.json"))
RENC = json.load(open(f"{DECL}/renamed-cols.json"))
DROPC = json.load(open(f"{DECL}/dropped-cols.json"))

EXACT = re.compile(r'^[a-z][a-z0-9_]*$')
TOKEN = re.compile(r'\b(' + "|".join(re.escape(k) for k in
                   sorted(MAP, key=len, reverse=True)) + r')\b')
# A quoted string whose ENTIRE content is a table name.
QUOTED = re.compile(r'(["\'])([a-z][a-z0-9_]*)\1')


def rewrite_regions(txt):
    """Rewrite renamed tables inside SQL regions only. Returns (text, n)."""
    out, last, n = [], 0, 0
    for region in A.SQL_REGION.finditer(txt):
        body = region.group(0)
        if not A.SQL_VERB.search(body):
            continue
        # `... GROUP_CONCAT(x) as slugs` is a column ALIAS inside a SQL region,
        # not a table reference. Renaming it produced `as base_slugs`, which is
        # harmless (the read-back was renamed too) but reads as a table and is
        # simply wrong.
        def one(mm):
            head = body[max(0, mm.start() - 4):mm.start()]
            if re.search(r"\b[Aa][Ss]\s+$", head):
                return mm.group(0)
            return MAP[mm.group(1)]
        new, cnt = TOKEN.subn(one, body)
        cnt = sum(1 for mm in TOKEN.finditer(body)) - sum(1 for mm in TOKEN.finditer(new))
        if cnt:
            out.append(txt[last:region.start()]); out.append(new)
            last = region.end(); n += cnt
    out.append(txt[last:])
    return "".join(out), n


# A quoted string that LOOKS like a table name but is not. All four measured on
# the first apply, all four wrong:
#   @field_validator("populations")   -- a Pydantic FIELD name
#   ... AS slugs / as slugs           -- a SQL column ALIAS
#   r["slugs"]                        -- reading back that alias
#   CONTENT_ROOTS = (..., "decisions") -- a DIRECTORY name
NOT_A_TABLE = re.compile(
    r'(?:field_validator|field_serializer|alias|Field)\s*\(\s*$'
    r'|AS\s+$|as\s+$'
    r'|CONTENT_ROOTS|_ROOTS\s*=|DIRS\s*=|PATHS\s*=')


def rewrite_quoted(txt, rel):
    """Rewrite a quoted string that is EXACTLY a renamed table name."""
    if rel.startswith("schemas/"):
        return txt, 0      # Pydantic field names collide with table names by design
    n = 0
    def sub(m):
        nonlocal n
        if m.group(2) not in MAP:
            return m.group(0)
        head = txt[max(0, m.start() - 60):m.start()]
        line0 = txt.rfind("\n", 0, m.start()) + 1
        line = txt[line0:txt.find("\n", m.start())]
        if NOT_A_TABLE.search(head) or NOT_A_TABLE.search(line):
            return m.group(0)
        n += 1
        return f"{m.group(1)}{MAP[m.group(2)]}{m.group(1)}"
    return QUOTED.sub(sub, txt), n


# Files that hold a genuine LIST or MAP of table names outside any SQL region.
# Each was read before being listed here; the sweep rewrites table names in these
# files' quoted strings only.
QUOTED_TARGETS = {
    "scripts/audit/graph/extract_db.py",
    "scripts/audit/graph/topology.py",
    "scripts/audit/migration_reproducibility.py",
    "scripts/generate/build_site.py",
    "scripts/audit/validate_pydantic_schemas.py",
    "scripts/validate_schema.py",
    "scripts/audit/graph/known_debt.yaml",
    "governance/retired-vocabulary.yaml",
}


def rewrite_targets(txt, rel):
    if rel not in QUOTED_TARGETS:
        return txt, 0
    n = 0
    def sub(m):
        nonlocal n
        if m.group(2) not in MAP:
            return m.group(0)
        n += 1
        return f"{m.group(1)}{MAP[m.group(2)]}{m.group(1)}"
    return QUOTED.sub(sub, txt), n


def residue(txt):
    """Bare occurrences left over -- reported, never rewritten."""
    return [m.group(1) for m in TOKEN.finditer(txt)]


def main():
    apply = "--apply" in sys.argv
    changed, report = {}, {}
    for path in sorted(A.scan(A.ROOT)):
        rel = os.path.relpath(path, A.ROOT)
        try:
            txt = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        new, a = rewrite_regions(txt)
        # rewrite_quoted is DISABLED. It rewrote dict keys and a filesystem path
        # -- room_dict["items"], {"populations": pop_map}, site/rooms -- because a
        # quoted lowercase word is not evidence of a table reference in Python.
        # The handful of genuine table-name LISTS (CORE_INVARIANTS, FP_TABLES, the
        # graph extractor's table map) are named in QUOTED_TARGETS and rewritten
        # by exact line, which is auditable in a way the general rule was not.
        new, b = rewrite_targets(new, rel)
        if a + b:
            changed[rel] = a + b
            if apply:
                open(path, "w", encoding="utf-8").write(new)
        left = residue(new)
        if left:
            report[rel] = left

    print(f"{'APPLIED' if apply else 'WOULD REWRITE'}:"
          f" {sum(changed.values())} sites in {len(changed)} files")
    for f, n in sorted(changed.items(), key=lambda x: -x[1]):
        print(f"   {n:>4}  {f}")

    print(f"\nRESIDUE — bare occurrences the mechanical pass will not touch:"
          f" {sum(len(v) for v in report.values())} in {len(report)} files")
    import collections
    tok = collections.Counter(t for v in report.values() for t in v)
    for t, n in tok.most_common():
        files = sorted(f for f, v in report.items() if t in v)
        print(f"   {n:>4}  {t:<32} {files[0]}"
              + (f" (+{len(files)-1} more)" if len(files) > 1 else ""))

    print("\nCOLUMN WORK, REPORTED NOT REWRITTEN — a regex cannot tell a registry")
    print("primary key from a link column, and both are spelled population_code:")
    cols = collections.Counter()
    for path in sorted(A.scan(A.ROOT)):
        try: txt = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError): continue
        for c in {c for d in RENC.values() for c in d} | {c for v in DROPC.values() for c in v}:
            n = len(re.findall(r'\b' + re.escape(c) + r'\b', txt))
            if n: cols[c] += n
    for c, n in cols.most_common():
        print(f"   {n:>4}  {c}")


if __name__ == "__main__":
    main()
