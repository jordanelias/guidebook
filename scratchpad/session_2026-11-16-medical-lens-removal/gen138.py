#!/usr/bin/env python3
"""Generate migration 138 from sqlite_master of the schema-137 database: drop the medical lens.

Drops base_taxonomy_medical, identity_medical_map, icf_medical_map, and the medical_code column of six tables, by
rebuilding each (SQLite cannot drop a column that carries a foreign key, a CHECK or an index). Every other column,
CHECK, default, comment, index, trigger and view is carried as it stands, text-for-text; the only edits are the
medical-lens ones, each asserted to apply exactly once.
"""
import re, sqlite3, sys
from pathlib import Path

DB = "file:/home/user/guidebook/data/guidebook.db?mode=ro"
OUT = Path(sys.argv[1])
c = sqlite3.connect(DB, uri=True)
VER = c.execute("PRAGMA user_version").fetchone()[0]
assert VER == 137, VER
NEW = VER + 1

MED_TABLES = ["base_taxonomy_medical", "identity_medical_map", "icf_medical_map"]
REBUILD = ["gaps", "specifications", "search_executions", "extraction_lens_links",
           "determination_gates", "source_value_extractions"]
master = c.execute("select type,name,tbl_name,sql,rowid from sqlite_master where sql is not null order by rowid").fetchall()
byname = {n: (t, tb, s) for t, n, tb, s, _ in master}
auto = {n for (n,) in c.execute("select name from sqlite_sequence")}


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old), old)
    return text.replace(old, new)


# ---- table text -----------------------------------------------------------------------------------------------
COL = re.compile(r"[ \t]*medical_code[ \t]+TEXT[ \t]+REFERENCES[ \t]+base_taxonomy_medical\(medical_code\),?[ \t]*\n?")
INLINE = " medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),"


def table_sql(t):
    s = byname[t][2]
    if INLINE in s:                                    # gaps, search_executions carry it inside one line
        s = once(s, INLINE, "", t)
    else:
        s, n = COL.subn("", s)
        assert n == 1, (t, n)
    if t == "specifications":
        s = once(s, "COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL",
                 "COALESCE(identity_code, icf_code, needs_code) IS NOT NULL", t)
    if t == "source_value_extractions":
        s = once(s, "COALESCE(identity_code, icf_code, needs_code, medical_code) IS NULL",
                 "COALESCE(identity_code, icf_code, needs_code) IS NULL", t)
    if t == "extraction_lens_links":
        s = once(s, "+ (needs_code IS NOT NULL) + (medical_code IS NOT NULL) = 1)",
                 "+ (needs_code IS NOT NULL) = 1)", t)
    s = s.replace("THE FOUR LENSES", "THE THREE LENSES")
    assert "medical" not in s.lower(), (t, [l for l in s.splitlines() if "medical" in l.lower()])
    return s


# ---- views: the closure of those that name a rebuilt or dropped table, or each other -----------------------------
names = set(REBUILD) | set(MED_TABLES)
views = [(n, s) for t, n, tb, s, _ in master if t == "view"]
hit = set()
changed = True
while changed:
    changed = False
    for n, s in views:
        if n in hit:
            continue
        if any(re.search(r'\b%s\b|"%s"' % (x, x), s) for x in names | hit):
            hit.add(n); changed = True
view_sql = {}
for n, s in views:
    if n not in hit:
        continue
    if "medical" in s.lower():
        s = {
            "v_coverage_lens": lambda s: once(once(s, "needs_code, medical_code,", "needs_code,", n),
                                              "GROUP BY 1, 2, 3, 4, 5, 6, 7, 8", "GROUP BY 1, 2, 3, 4, 5, 6, 7", n),
            "v_live_lens_links": lambda s: once(s, "needs_code, medical_code,", "needs_code,", n),
            "v_open_determination_gates": lambda s: once(s, "g.needs_code, g.medical_code,", "g.needs_code,", n),
            "v_determination_provenance": lambda s: once(s, "s.needs_code, s.medical_code)", "s.needs_code)", n),
            "v_item_provenance": lambda s: once(s, "ecs.needs_code, ecs.medical_code)", "ecs.needs_code)", n),
            "v_source_reach_all": lambda s: once(s, "ecs.needs_code, ecs.medical_code)", "ecs.needs_code)", n),
            "v_gap_subject": None,
        }[n]
        if s is None:
            s = dict(views)[n]          # v_gap_subject: edited below, each edit asserted
        else:
            s = s(dict(views)[n])
    else:
        s = dict(views)[n]
    view_sql[n] = s
# v_gap_subject needs its own pass: written out so each edit is asserted
gs = dict(views)["v_gap_subject"]
gs = once(gs, "g.needs_code, g.medical_code,\n           g.jurisdiction", "g.needs_code,\n           g.jurisdiction", "gs1")
gs = once(gs, "s.needs_code, s.medical_code,\n           NULL, NULL,", "s.needs_code,\n           NULL, NULL,", "gs2")
assert gs.count("g.needs_code, g.medical_code,\n                    g.jurisdiction") == 3, gs.count("g.medical_code")
gs = gs.replace("g.needs_code, g.medical_code,\n                    g.jurisdiction", "g.needs_code,\n                    g.jurisdiction")
gs = once(gs, "SELECT g.gap_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'none', NULL",
          "SELECT g.gap_id, NULL, NULL, NULL, NULL, NULL, NULL, 'none', NULL", "gs3")
view_sql["v_gap_subject"] = gs
for n, s in view_sql.items():
    assert "medical" not in s.lower(), (n, [l for l in s.splitlines() if "medical" in l.lower()])

# ---- indexes ---------------------------------------------------------------------------------------------------
idx = {}
for t, n, tb, s, _ in master:
    if t == "index" and tb in REBUILD:
        if n == "idx_spec_row_identity":
            s = once(s, "COALESCE(needs_code, ''),    COALESCE(medical_code, '')", "COALESCE(needs_code, '')", n)
        if n == "ux_extraction_lens_live":
            s = once(s, "COALESCE(needs_code, ''), COALESCE(medical_code, '')", "COALESCE(needs_code, '')", n)
        assert "medical" not in s.lower(), n
        idx.setdefault(tb, []).append((n, s))
trig = {}
for t, n, tb, s, _ in master:
    if t == "trigger" and tb in REBUILD:
        assert "medical" not in s.lower(), n
        trig.setdefault(tb, []).append((n, s))
for t, n, tb, s, _ in master:        # nothing else may still name a dropped object
    if n in view_sql or n in MED_TABLES or tb in REBUILD and t in ("table", "index", "trigger"):
        continue
    assert "medical" not in s.lower() or t == "view" and n in view_sql, (t, n)

# ---- emit ------------------------------------------------------------------------------------------------------
o = []
o.append(f"""-- {NEW}_drop_medical_lens.sql
-- SCHEMA migration, GENERATED from sqlite_master of the schema-{VER} database. Owner instruction 2026-11-16, quoted in
-- references/project-standards.md ("Owner instruction 2026-11-16 -- the medical taxonomy, the medical maps and the
-- medical codes are deleted"): the medical lens is removed. Dropped: base_taxonomy_medical, identity_medical_map and
-- icf_medical_map (no row in any of them), and the medical_code column of {', '.join(REBUILD)} (NULL on every row of
-- every one of them). Tooling; no research row, no row changed or lost.
--
-- SQLite cannot drop a column that carries a foreign key, a CHECK or an index, so each of the six tables is rebuilt as
-- 114, 131 and 136 rebuilt theirs: the sequence floor of an AUTOINCREMENT table is captured (DROP TABLE takes its
-- row), every view that names a rebuilt or dropped table (and every view that names such a view) is dropped, each new
-- table is created, filled by column name, the old one dropped and the new one renamed, its indexes and trigger are
-- recreated, the floors are restored and the views are recreated from their stored text. The only edits to any stored
-- text are the medical-lens ones: the column, the term in the three CHECKs and the two unique indexes that carried it,
-- and the term in the six views that selected it. The foreign keys of other tables into a rebuilt table name it by
-- text and resolve to the new table.
CREATE TEMP TABLE _{NEW}_seq AS SELECT name, seq FROM sqlite_sequence;
""")
order = [n for t, n, tb, s, _ in master if t == "view" and n in view_sql]
for n in reversed(order):
    o.append(f'DROP VIEW "{n}";')
o.append("")
for t in REBUILD:
    cols = [r[1] for r in c.execute(f'pragma table_info("{t}")') if r[1] != "medical_code"]
    sql = table_sql(t)
    head = re.match(r'CREATE TABLE\s+("?)%s\1' % t, sql)
    assert head, t
    new = f'"_{NEW}_new_{t}"'
    sql = sql[:head.start()] + f"CREATE TABLE {new}" + sql[head.end():]
    o.append(sql + ";\n")
    cl = ", ".join(f'"{x}"' for x in cols)
    o.append(f'INSERT INTO {new} ({cl}) SELECT {cl} FROM "{t}";')
    o.append(f'DROP TABLE "{t}";')
    o.append(f'ALTER TABLE {new} RENAME TO "{t}";')
    for n, s in idx.get(t, []):
        o.append(s + ";")
    for n, s in trig.get(t, []):
        o.append(s + ";")
    o.append("")
for t in MED_TABLES:
    o.append(f'DROP TABLE "{t}";')
o.append("")
o.append(f"""DELETE FROM sqlite_sequence WHERE name IN ({', '.join(repr(t) for t in sorted(auto & set(REBUILD)))});
INSERT INTO sqlite_sequence (name, seq) SELECT name, seq FROM _{NEW}_seq WHERE name IN ({', '.join(repr(t) for t in sorted(auto & set(REBUILD)))});
DROP TABLE _{NEW}_seq;
""")
for n in order:
    o.append(view_sql[n].rstrip().rstrip(";") + ";\n")
o.append(f"PRAGMA user_version = {NEW};")
OUT.write_text("\n".join(o) + "\n")
print("views rebuilt:", len(order), "| tables:", len(REBUILD), "| auto:", sorted(auto & set(REBUILD)))
