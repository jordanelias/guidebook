#!/usr/bin/env python3
"""Generate migration 065 -- seven-stage nomenclature + four lenses in one table.

This is a ONE-SHOT build tool, committed because the first version of it lived
only in a heredoc and was lost with the container. It reads the canonical schema
read-only and writes SQL to stdout; it never writes a database.

Three facts measured on SQLite 3.45.1 shape the output:
  1. ALTER TABLE RENAME rewrites REFERENCES clauses AND view bodies automatically.
  2. A table REBUILD (drop+create -- unavoidable, SQLite cannot ADD a table-level
     CHECK) does NOT. Views reading a rebuilt table must be dropped and recreated.
  3. RENAME COLUMN updates FK references in OTHER tables, so the three registry
     PKs can go uniform to `code` and their inbound keys follow.
  4. A generated column may NOT be part of a PRIMARY KEY, but may be in a UNIQUE
     index. That is what restores uniqueness after one NOT NULL taxonomy column
     becomes four nullable ones.
"""
import os, re, sqlite3, sys, collections

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

# ---------------------------------------------------------------- lens shape --
LENSES = [("identity_code", "base_taxonomy_identity"),
          ("icf_code",      "base_taxonomy_icf"),
          ("needs_code",    "base_taxonomy_needs"),
          ("medical_code",  "base_taxonomy_medical")]

def lens_cols(indent="  "):
    return [f'{indent}"{c}" TEXT REFERENCES "{t}"("code"),' for c, t in LENSES]

def lens_check(exactly):
    op = "= 1" if exactly else "<= 1"
    return ("  CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL)\n"
            f"       + (needs_code IS NOT NULL) + (medical_code IS NOT NULL) {op})")

GEN = ('  "taxonomy_code" TEXT GENERATED ALWAYS AS '
       '(COALESCE("identity_code","icf_code","needs_code","medical_code")) STORED,')

# --------------------------------------------------------------- the rename --
# Straight renames: no structural change, ALTER TABLE RENAME does the whole job.
RENAME = {
    "access_duration": "base_access_duration",
    "access_need_axis_map": "base_needs_icf_map",
    "access_need_icf": "base_access_need_icf_codes",
    "access_stakes": "base_access_stakes",
    "case_study_outcomes": "render_case_study_outcomes",
    "case_study_specs": "render_case_study_specification_links",
    "case_study_strategies": "render_case_study_strategies",
    "citation_mining": "research_mining_runs",
    "conflicts": "synthesis_conflicts",
    "connection_targets": "synthesis_connection_links",
    "connections": "synthesis_connections",
    "convergence_assessment": "synthesis_convergence",
    "data_migrations": "base_data_migrations",
    "decisions": "base_decisions",
    "economics_entries": "render_economics_entries",
    "economics_entry_specs": "render_economics_specification_links",
    "external_root_registry": "evidence_roots",
    "evidence_sources": "evidence_items",
    "gap_mining": "research_gap_mining_runs",
    "gaps": "research_gaps",
    "item_audit_runs": "judgment_audit_runs",
    "item_bpc_links": "synthesis_item_links",
    "items": "render_provisions",
    "jurisdictional_values": "research_code_leads",
    "lang_jur_map": "base_lang_jur_map",
    "life_stage_modifiers": "base_life_stage_modifiers",
    "pipeline_runs": "base_pipeline_runs",
    "population_axis_map": "base_identity_icf_map",
    "reference_stubs": "research_stubs",
    "room_items": "render_room_element_links",
    "rooms": "base_room_types",
    "search_admissions": "evidence_admission_links",
    "search_candidates": "research_candidates",
    "search_coverage": "research_coverage_links",
    "search_executions": "research_searches",
    "search_languages": "research_language_links",
    "situations": "base_situations",
    "slugs": "base_slugs",
    "source_locators": "research_items",
    "source_slug_links": "evidence_slug_links",
    "supersession_check": "evidence_supersession_runs",
    "term_aliases": "base_term_aliases",
    "term_item_links": "base_term_item_links",
    "terms": "base_terms",
    "url_verification_runs": "evidence_url_verification_runs",
    "weighting_profile": "base_weighting_profile",
}

# Columns renamed after their table is renamed. The base crossing maps hold two
# taxonomy references each; their column names must follow the registries they
# point at, or the retired words survive in the one layer whose whole job is
# lens-switching. `population` is retired vocabulary (D-0169), including in a
# free-text note column.
COLUMN_RENAME = [
    ("base_identity_icf_map", "population_code", "identity_code"),
    ("base_identity_icf_map", "axis_code", "icf_code"),
    ("base_needs_icf_map", "need_code", "needs_code"),
    ("base_needs_icf_map", "axis_code", "icf_code"),
    ("base_access_need_icf_codes", "need_code", "needs_code"),
    ("evidence_roots", "root_population_note", "root_group_note"),
    # §R8 retired the tokens serves_axes / attaches_axes. Renamed, not dropped:
    # slugs.serves_axes holds a JSON array of axis codes in 1 of 106 rows, which
    # is a rule-5 copy of a link table that does not exist yet. Dropping it would
    # lose the only live row; the link table is owed and is not a rename's job.
    ("base_slugs", "serves_axes", "serves_icf"),
    ("base_situations", "attaches_axes", "attaches_icf"),
]

REGISTRIES = [("populations", "base_taxonomy_identity", "population_code"),
              ("axes", "base_taxonomy_icf", "axis_code"),
              ("access_needs", "base_taxonomy_needs", "need_code")]

# ------------------------------------------------------------- the rebuilds --
# Each entry: new name, the taxonomy column being replaced (or None), whether the
# lens is MANDATORY on this row, columns to drop outright, columns to rename.
#
# "drop" is only ever used for two proven cases, both recorded in the header of
# the emitted SQL:
#   (a) a DUAL HOME -- an inline taxonomy column on a table that also has a link
#       table. Rule 5: the link table is the pointer, the column is the copy.
#   (b) a column measured 0-populated across every live row.
Rebuild = collections.namedtuple(
    "Rebuild", "new taxonomy mandatory drop rename gen_unique")

REBUILD = {
  # -- tables where the taxonomy is inline and there is NO link table ----------
  "evidence_population_match": Rebuild(
      "judgment_match_grades", "target_population", True, [],
      # study_population is the PAPER's own participants (R13 grading), not our
      # taxonomy. It stays free text; renamed because `population` is retired.
      {"study_population": "study_group"}, None),
  "specifications": Rebuild(
      "specification_items", "population_code", True, [], {}, None),
  "bpc_metadata": Rebuild(
      "synthesis_items", "population", True, [], {}, None),

  # -- tables with a DUAL HOME: inline column AND a link table (rule 5) --------
  "spec_value_probes": Rebuild(
      "specification_value_probes", None, False, ["population"], {}, None),
  "reasoning_doc_citations": Rebuild(
      "synthesis_citations", None, False, ["population"], {}, None),
  "source_value_extractions": Rebuild(
      "judgment_items", None, False,
      # population_label is the registry's NAME copied onto the row -- rule 5
      # twice over. population_code is the dual home with the link table.
      ["population_code", "population_label"],
      {"root_population_note": "root_group_note"}, None),
  "case_studies": Rebuild(
      "render_case_studies", None, False,
      ["populations_served_note"],           # copy of what the link table holds
      {"population_description": "participant_description"}, None),

  # -- the link tables: these are what GAIN the four lenses --------------------
  "extraction_population_links": Rebuild(
      "judgment_item_taxonomy_links", "population_code", True, [], {},
      ("extraction_id",)),
  "probe_population_links": Rebuild(
      "specification_probe_taxonomy_links", "population_code", True, [], {},
      ("probe_id",)),
  "citation_population_links": Rebuild(
      "synthesis_citation_taxonomy_links", "population_code", True, [], {},
      ("citation_id",)),
  "case_study_populations": Rebuild(
      "render_case_study_taxonomy_links", "population_code", True, [], {},
      ("case_study_id",)),
  "economics_entry_populations": Rebuild(
      "render_economics_taxonomy_links", "population_code", True, [], {},
      ("entry_id",)),
  "item_population_elaborations": Rebuild(
      "base_item_taxonomy_elaborations", "population_code", True, [], {}, None),
}

# item_population_links + item_axis_links model the SAME relation -- item to
# taxonomy -- with two divergent grading vocabularies (applicability: 2 values;
# strength_band: 3 values) and nothing reconciling them. Giving either one an
# icf_code column would make item-to-ICF expressible in two tables: the exact
# rule-5 dual home this change exists to remove. So the fold is compelled by the
# lens rule, not a widening of it.
FOLD_ITEM_LINKS = True

# ------------------------------------------------------- view repairs (rule 4) --
# A VIEW IS A CALLER. Four views name a taxonomy column that this migration moves.
# Two read `specifications.population_code`, which becomes four lens columns, so
# they take the generated coalesce. Two read
# `source_value_extractions.population_code`, which is DROPPED as a dual home with
# extraction_population_links -- so they must join the link table. That join is
# what "point, do not copy" means for a view: the taxonomy is reached, not held.
VIEW_PATCH = {
  "v_item_provenance":   [("ecs.population_code", "ecs.taxonomy_code")],
  "v_source_reach_all":  [("ecs.population_code", "ecs.taxonomy_code")],
  "v_item_extractions": [
      ("sve.population_code", "jtl.taxonomy_code AS taxonomy_code"),
      ('LEFT JOIN "evidence_items" es',
       'LEFT JOIN "judgment_item_taxonomy_links" jtl'
       ' ON jtl.extraction_id = sve.extraction_id\nLEFT JOIN "evidence_items" es')],
  "v_value_independence": [
      ("           population_code,", "           jtl.taxonomy_code,"),
      ('    FROM "judgment_items"',
       '    FROM "judgment_items" sve\n'
       '    LEFT JOIN "judgment_item_taxonomy_links" jtl'
       ' ON jtl.extraction_id = sve.extraction_id'),
      ("GROUP BY COALESCE(parameter_canonical, parameter), population_code",
       "GROUP BY COALESCE(parameter_canonical, parameter), jtl.taxonomy_code")],
}

# --------------------------------------------------------------- generation --
def checks_of(ddl):
    """Every CHECK(...) expression in a CREATE TABLE, balanced-paren scanned.

    PRAGMA table_info does not carry CHECK constraints, so a rebuild that
    reconstructs columns from it silently DROPS the whole refusal vocabulary --
    and dbcore.check_values() reads the column's own CHECK, so every db.py
    refusal would go quiet while still looking safe. The insurance harness found
    this; nothing else would have.
    """
    out, i = [], 0
    low = ddl.lower()
    while True:
        i = low.find("check", i)
        if i < 0: return out
        j = i + 5
        while j < len(ddl) and ddl[j] in " \t\n": j += 1
        if j >= len(ddl) or ddl[j] != "(":
            i += 5; continue
        depth, k = 0, j
        while k < len(ddl):
            if ddl[k] == "(": depth += 1
            elif ddl[k] == ")":
                depth -= 1
                if depth == 0: break
            k += 1
        out.append(ddl[j + 1:k].strip())
        i = k + 1


def indexes_of(con, table):
    """Named indexes only. An auto-index from a UNIQUE/PK clause has sql NULL and
    is carried by the DDL we re-emit, not by a CREATE INDEX statement."""
    return [(n, sql) for n, sql in con.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name=?"
        " AND sql IS NOT NULL ORDER BY name", (table,))]


def unique_constraints(con, table):
    """Table-level UNIQUE constraints, as column lists.

    These are auto-indexes: PRAGMA index_list gives origin 'u' and sqlite_master
    holds sql NULL, so replaying named indexes misses them entirely and a rebuild
    drops them. Three UNIQUE keys went that way before the insurance harness
    reported it -- the same blind spot as the lost CHECKs, one layer down.
    """
    out = []
    for r in con.execute('PRAGMA index_list("%s")' % table):
        if r[3] == "u" and r[2]:
            out.append([x[2] for x in con.execute('PRAGMA index_info("%s")' % r[1])])
    return out


def mentions(expr, cols):
    return any(re.search(r'\b' + re.escape(c) + r'\b', expr) for c in cols)


def apply_renames(expr, ren):
    for old, new in ren.items():
        expr = re.sub(r'\b' + re.escape(old) + r'\b', new, expr)
    return expr


def newname(t):
    if t in REBUILD:
        return REBUILD[t].new
    return RENAME.get(t, t)

def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    q = con.execute

    tables = [r[0] for r in q("SELECT name FROM sqlite_master WHERE type='table'"
                              " AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    views = [(r[0], r[1]) for r in q("SELECT name, sql FROM sqlite_master"
                                     " WHERE type='view' ORDER BY name")]
    # term_item_links is rebuilt too (step 5), so it belongs in this set.
    rebuilt = set(REBUILD) | {"term_item_links"} | (
        {"item_population_links", "item_axis_links"} if FOLD_ITEM_LINKS else set())

    # Which views read a table we are about to REBUILD? Those must be dropped and
    # recreated by hand -- fact 2. Resolve transitively: a view over a view over a
    # rebuilt table is equally broken.
    body = {n: (s or "") for n, s in views}
    reads = {n: {t for t in tables + [v for v, _ in views]
                 if t != n and t in b} for n, b in body.items()}
    def resolve(v, seen=None):
        seen = seen or set()
        out = set()
        for r in reads.get(v, ()):
            if r in seen: continue
            seen.add(r)
            out.add(r); out |= resolve(r, seen)
        return out
    doomed = sorted(v for v, _ in views if resolve(v) & rebuilt)

    o = []
    w = o.append
    w("-- 065: seven-stage nomenclature + four lenses in one table.")
    w("-- D-0167 spine | D-0168 hand-offs | D-0169 grammar | D-0170 four lenses |")
    w("-- D-0171 building | owner instruction 2026-08-28: all four lenses in the")
    w("-- same tables after the base phase, and loads of rows is fine.")
    w("--")
    w("-- Generated by scratchpad/session_2026-08-27-hook-audit/build_065.py.")
    w("-- Do not hand-edit: re-run the generator.")
    w("--")
    w("-- ORDER MATTERS, and the first draft had it wrong. RENAME COMES FIRST, then")
    w("-- the rebuilds happen IN PLACE under the new names. ALTER TABLE RENAME")
    w("-- repoints every inbound REFERENCES clause; DROP+CREATE does not. Rebuilding")
    w("-- case_studies before renaming it left three child tables pointing at a table")
    w("-- that no longer existed -- and PRAGMA foreign_key_check called it clean,")
    w("-- because all three hold 0 rows. Rule 4: a 0-row object is unproven, not clean.")
    w("--")
    w("-- WHAT IS DROPPED, AND ON WHAT EVIDENCE:")
    w("--   dual homes (rule 5 -- the link table is the pointer, the column the copy):")
    w("--     spec_value_probes.population        + probe_population_links")
    w("--     reasoning_doc_citations.population  + citation_population_links")
    w("--     source_value_extractions.population_code/_label + extraction_population_links")
    w("--     case_studies.populations_served_note + case_study_populations")
    w("--   measured 0-populated across every live row:")
    w("--     term_item_links.population            0 of 147")
    w("--     item_population_links.rationale_ref   0 of 372")
    w("--")
    w("-- NO LINK TABLE IS DROPPED. An earlier draft folded the five 0-row link")
    w("-- tables into their parents; that trades a many-to-many for one lens per")
    w("-- parent, which is a cardinality regression that 0 rows merely hides.")
    w("PRAGMA legacy_alter_table=OFF;")
    w("")
    w("-- 1. the fourth lens needs an FK target. Empty: a medical vocabulary is")
    w("--    content doctrine (DG-NON) and is the owner's to write.")
    w("CREATE TABLE IF NOT EXISTS base_taxonomy_medical (")
    w("  code TEXT PRIMARY KEY,")
    w("  name TEXT NOT NULL,")
    w("  definition TEXT,")
    w("  created_at TEXT,")
    w("  created_by_session TEXT")
    w(");")
    w("")
    w("-- 2. the three registries: rename table, then PK column to `code`.")
    w("--    RENAME COLUMN carries every inbound foreign key with it, and rewrites")
    w("--    view bodies -- measured on 3.45.1, and it correctly leaves a same-named")
    w("--    column on a DIFFERENT table alone.")
    for old, new_, pk in REGISTRIES:
        w(f'ALTER TABLE "{old}" RENAME TO "{new_}";')
        w(f'ALTER TABLE "{new_}" RENAME COLUMN "{pk}" TO "code";')
    w("")
    w("-- 3. every remaining rename, INCLUDING the tables about to be rebuilt.")
    allren = dict(RENAME)
    allren.update({t: sp.new for t, sp in REBUILD.items()})
    allren.pop("term_item_links", None)
    allren["term_item_links"] = RENAME["term_item_links"]
    for old in sorted(allren):
        w(f'ALTER TABLE "{old}" RENAME TO "{allren[old]}";')
    w("")
    w("-- 3b. columns carrying retired vocabulary, renamed once their table is.")
    for t, old, new_ in COLUMN_RENAME:
        w(f'ALTER TABLE "{t}" RENAME COLUMN "{old}" TO "{new_}";')
    w("")
    w(f"-- 4. drop the {len(doomed)} views that read a table about to be rebuilt.")
    for v in doomed:
        w(f'DROP VIEW "{v}";')
    w("")
    w("-- 5. rebuild IN PLACE: one taxonomy column becomes four nullable typed FK")
    w("--    columns, a CHECK, and a STORED coalesce. Every original CHECK and every")
    w("--    named index is carried across explicitly -- PRAGMA table_info carries")
    w("--    neither, and dbcore.check_values() reads the column's own CHECK, so a")
    w("--    lost CHECK silently disarms every db.py refusal while it still looks safe.")

    def emit_rebuild(t, spec):
        """t is the ORIGINAL name; the table is already renamed to spec.new."""
        new_ = spec.new
        tmp = f"{new_}__065"
        ddl = q("SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                (t,)).fetchone()[0]
        cols = q(f'PRAGMA table_info("{t}")').fetchall()
        fks  = q(f'PRAGMA foreign_key_list("{t}")').fetchall()
        drop = ({spec.taxonomy} | set(spec.drop)) - {None}
        keep = [c for c in cols if c[1] not in drop]
        ren  = dict(spec.rename)
        w("")
        w(f'CREATE TABLE "{tmp}" (')
        lines = []
        for c in keep:
            lines.append(f'  "{ren.get(c[1], c[1])}" {c[2] or "TEXT"}'
                         + (" NOT NULL" if c[3] else "")
                         + (f" DEFAULT {c[4]}" if c[4] is not None else ""))
        lines += [l.rstrip(",") for l in lens_cols()]
        lines.append(GEN.rstrip(","))
        pk = [ren.get(c[1], c[1])
              for c in sorted((c for c in keep if c[5]), key=lambda c: c[5])]
        if pk:
            lines.append("  PRIMARY KEY (" + ", ".join(f'"{x}"' for x in pk) + ")")
        for f in sorted(fks, key=lambda f: f[3]):
            if f[3] in drop: continue
            tgt  = newname(f[2])
            tcol = "code" if any(f[2] == r[0] for r in REGISTRIES) else f[4]
            lines.append(f'  FOREIGN KEY ("{ren.get(f[3], f[3])}")'
                         f' REFERENCES "{tgt}"("{tcol}")')
        for ck in checks_of(ddl):
            if mentions(ck, drop):
                w(f"-- CHECK dropped with its column: {ck.strip()[:70]}")
                continue
            lines.append(f"  CHECK ({apply_renames(ck, ren)})")
        lines.append(lens_check(spec.mandatory))
        w(",\n".join(lines))
        w(");")
        sel = ", ".join(f'"{c[1]}"' for c in keep)
        tgt = ", ".join(f'"{ren.get(c[1], c[1])}"' for c in keep)
        if spec.taxonomy:
            w(f'INSERT INTO "{tmp}" ({tgt}, "identity_code")'
              f' SELECT {sel}, "{spec.taxonomy}" FROM "{new_}";')
        else:
            w(f'INSERT INTO "{tmp}" ({tgt}) SELECT {sel} FROM "{new_}";')
        w(f'DROP TABLE "{new_}";')
        w(f'ALTER TABLE "{tmp}" RENAME TO "{new_}";')
        for iname, isql in indexes_of(con, t):
            if spec.taxonomy and mentions(isql, {spec.taxonomy}):
                # An index BUILT ON the taxonomy column is the reverse lookup --
                # "which rows serve AUT". Rebuilding it on the generated coalesce
                # keeps that walk and widens it to all four lenses. Dropping it
                # silently, as the first draft did, is a walkability regression
                # that nothing downstream would report.
                isql = apply_renames(isql, {spec.taxonomy: "taxonomy_code"})
            elif mentions(isql, drop):
                w(f"-- index dropped with its column: {iname}")
                continue
            isql = apply_renames(isql, ren)
            isql = re.sub(r'\bON\s+"?' + re.escape(t) + r'"?', f'ON "{new_}"', isql)
            isql = isql.replace(f"INDEX {iname}", f'INDEX "{iname}"', 1)
            w(isql.rstrip(";") + ";")
        # Table-level UNIQUE constraints, re-emitted as explicit indexes with the
        # taxonomy column mapped to the coalesce. As indexes rather than DDL
        # constraints because a generated column may not sit in a UNIQUE clause of
        # a CREATE TABLE, but may sit in a UNIQUE INDEX (measured, 3.45.1).
        for n, ucols in enumerate(unique_constraints(con, t)):
            if any(c in drop and c != spec.taxonomy for c in ucols): continue
            uc = [("taxonomy_code" if c == spec.taxonomy else ren.get(c, c))
                  for c in ucols]
            w(f'CREATE UNIQUE INDEX "uq_{new_}_{n}" ON "{new_}"'
              f' ({", ".join(chr(34)+c+chr(34) for c in uc)});')
        if spec.gen_unique:
            cu = list(spec.gen_unique) + ["taxonomy_code"]
            if any(c[1] == "subtype" for c in keep): cu.append("subtype")
            w(f'CREATE UNIQUE INDEX "ux_{new_}" ON "{new_}"'
              f' ({", ".join(chr(34)+c+chr(34) for c in cu)});')

    for t in sorted(REBUILD):
        emit_rebuild(t, REBUILD[t])

    if FOLD_ITEM_LINKS:
        w("")
        w("-- 5b. item_population_links + item_axis_links model the SAME relation.")
        w("--     Adding icf_code to one would make item-to-ICF expressible twice.")
        w("--     530 rows, one lens each. rationale_ref dropped: 0 of 372 populated.")
        w("--     Both CHECK vocabularies are carried; neither is reconciled here,")
        w("--     because reconciling applicability with strength_band is a content")
        w("--     judgement and this is a rename.")
        w('CREATE TABLE "base_item_taxonomy_links" (')
        w('  "item_code" TEXT NOT NULL,')
        w("  \"subtype\" TEXT NOT NULL DEFAULT '',")
        w('  "applicability" TEXT,')
        w('  "strength_band" TEXT,')
        w('  "use_mode" TEXT,')
        w('  "mechanism_note" TEXT,')
        w('  "source" TEXT,')
        w('  "created_at" TEXT,')
        w('  "created_by_session" TEXT,')
        for l in lens_cols(): w(l)
        w(GEN)
        w('  FOREIGN KEY ("item_code") REFERENCES "render_provisions"("item_code"),')
        for src in ("item_population_links", "item_axis_links"):
            ddl = q("SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                    (src,)).fetchone()[0]
            for ck in checks_of(ddl):
                if mentions(ck, {"population_code", "axis_code", "rationale_ref"}):
                    continue
                w(f"  CHECK ({ck}),")
        w(lens_check(True))
        w(");")
        w('INSERT INTO "base_item_taxonomy_links"'
          ' ("item_code","subtype","applicability","created_at","created_by_session","identity_code")'
          " SELECT \"item_code\", COALESCE(\"subtype\",''), \"applicability\","
          ' "created_at","created_by_session","population_code" FROM "item_population_links";')
        w('INSERT INTO "base_item_taxonomy_links"'
          ' ("item_code","subtype","strength_band","use_mode","mechanism_note","source",'
          '"created_at","created_by_session","icf_code")'
          " SELECT \"item_code\", '', \"strength_band\",\"use_mode\",\"mechanism_note\",\"source\","
          ' "created_at","created_by_session","axis_code" FROM "item_axis_links";')
        w('DROP TABLE "item_population_links";')
        w('DROP TABLE "item_axis_links";')
        w('CREATE UNIQUE INDEX "ux_base_item_taxonomy_links"'
          ' ON "base_item_taxonomy_links" ("item_code","taxonomy_code","subtype");')
        w('CREATE INDEX "idx_base_item_taxonomy_links_item"'
          ' ON "base_item_taxonomy_links" ("item_code");')
        w('CREATE INDEX "idx_base_item_taxonomy_links_code"'
          ' ON "base_item_taxonomy_links" ("taxonomy_code");')
        w("-- item_axis_links keyed UNIQUE(item_code, axis_code) with no subtype, so")
        w("-- the union key above is one column WIDER and therefore weaker for ICF")
        w("-- rows. A partial index restores the original constraint exactly.")
        w('CREATE UNIQUE INDEX "uq_base_item_taxonomy_links_icf"'
          ' ON "base_item_taxonomy_links" ("item_code","icf_code")'
          " WHERE \"icf_code\" IS NOT NULL;")

    w("")
    w("-- 6. term_item_links.population: 0 of 147 populated. Rebuilt to drop it")
    w("--    rather than carrying a proven-dead column into a fresh table.")
    tddl = q("SELECT sql FROM sqlite_master WHERE type='table' AND name='term_item_links'").fetchone()[0]
    tc = q('PRAGMA table_info("term_item_links")').fetchall()
    keep = [c for c in tc if c[1] != "population"]
    w('CREATE TABLE "base_term_item_links__065" (')
    lines = [f'  "{c[1]}" {c[2]}' + (" NOT NULL" if c[3] else "") for c in keep]
    lines.append('  PRIMARY KEY ("term_id", "item_code")')
    lines.append('  FOREIGN KEY ("item_code") REFERENCES "render_provisions"("item_code")')
    lines.append('  FOREIGN KEY ("term_id") REFERENCES "base_terms"("term_id")')
    for ck in checks_of(tddl):
        if not mentions(ck, {"population"}):
            lines.append(f"  CHECK ({ck})")
    w(",\n".join(lines))
    w(");")
    sel = ", ".join(f'"{c[1]}"' for c in keep)
    w(f'INSERT INTO "base_term_item_links__065" ({sel}) SELECT {sel} FROM "base_term_item_links";')
    w('DROP TABLE "base_term_item_links";')
    w('ALTER TABLE "base_term_item_links__065" RENAME TO "base_term_item_links";')
    for iname, isql in indexes_of(con, "term_item_links"):
        if mentions(isql, {"population"}): continue
        isql = re.sub(r'\bON\s+"?term_item_links"?', 'ON "base_term_item_links"', isql)
        isql = isql.replace(f"INDEX {iname}", f'INDEX "{iname}"', 1)
        w(isql.rstrip(";") + ";")

    w("")
    w(f"-- 7. recreate the {len(doomed)} views with every reference re-pointed.")
    ren = dict(RENAME)
    ren.update({t: sp.new for t, sp in REBUILD.items()})
    ren.update({o_: n_ for o_, n_, _ in REGISTRIES})
    if FOLD_ITEM_LINKS:
        ren["item_population_links"] = "base_item_taxonomy_links"
        ren["item_axis_links"] = "base_item_taxonomy_links"
    for v in doomed:
        sql = body[v]
        def sub(m):
            return f'"{ren[m.group(1)]}"'
        sql = re.sub(r'"?\b(' + "|".join(re.escape(k) for k in
                     sorted(ren, key=len, reverse=True)) + r')\b"?', sub, sql)
        for frm, to in VIEW_PATCH.get(v, ()):
            if frm not in sql:
                raise SystemExit(f"VIEW_PATCH miss: {v!r} has no {frm!r}")
            sql = sql.replace(frm, to)
        w(sql.rstrip().rstrip(";") + ";")

    w("")
    w("PRAGMA user_version = 65;")
    print("\n".join(o))
    print(f"-- doomed views: {len(doomed)} of {len(views)}", file=sys.stderr)

def declarations():
    """Emit the four JSON declarations rename_insurance.py needs.

    Derived from the SAME dicts that generate the SQL, so the declaration cannot
    drift from what the migration actually does -- a hand-written declaration
    would only prove that I wrote it to match my own expectation.
    """
    m = dict(RENAME)
    m.update({t: sp.new for t, sp in REBUILD.items()})
    m.update({o: n for o, n, _ in REGISTRIES})
    if FOLD_ITEM_LINKS:
        m["item_population_links"] = "base_item_taxonomy_links"
        m["item_axis_links"] = "base_item_taxonomy_links"
    lens = [c for c, _ in LENSES] + ["taxonomy_code"]
    added = {t: list(lens) for t, sp in REBUILD.items()}
    added["item_population_links"] = list(lens)
    added["item_axis_links"] = list(lens) + [
        "applicability", "subtype"]      # the fold's other half
    dropc = {t: ([sp.taxonomy] if sp.taxonomy else []) + list(sp.drop)
             for t, sp in REBUILD.items()}
    dropc["item_population_links"] = ["population_code", "rationale_ref"]
    dropc["item_axis_links"] = ["axis_code"]
    dropc["term_item_links"] = ["population"]
    renc = {t: dict(sp.rename) for t, sp in REBUILD.items() if sp.rename}
    for t, old, new in COLUMN_RENAME:
        src = next((k for k, v in m.items() if v == t), t)
        renc.setdefault(src, {})[old] = new
    for o, n, pk in REGISTRIES:
        renc.setdefault(o, {})[pk] = "code"
    idxc = {t: {sp.taxonomy: "taxonomy_code"} for t, sp in REBUILD.items() if sp.taxonomy}
    idxc["item_population_links"] = {"population_code": "taxonomy_code"}
    idxc["item_axis_links"] = {"axis_code": "taxonomy_code"}
    for o_, n_, pk in REGISTRIES:
        idxc.setdefault(o_, {})[pk] = "code"
    for t, old, new in COLUMN_RENAME:
        src = next((k for k, v in m.items() if v == t), t)
        idxc.setdefault(src, {})[old] = new
    chv = {"v_item_extractions": ["judgment_item_taxonomy_links"],
           "v_value_independence": ["judgment_item_taxonomy_links"]}
    # Every lens key, edge by edge. Derived from LENSES so the declaration cannot
    # under-state what the SQL emits.
    afk = sorted(f"{m.get(t, t)}.{c} -> {reg}.code"
                 for t in added for c, reg in LENSES if c in added[t])
    return m, [], added, dropc, renc, idxc, chv, afk

if __name__ == "__main__":
    if "--declarations" in sys.argv:
        import json
        m, dropped, added, dropc, renc, idxc, chv, afk = declarations()
        out = sys.argv[sys.argv.index("--declarations") + 1]
        for nm, obj in (("map", m), ("dropped", dropped), ("added-cols", added),
                        ("dropped-cols", dropc), ("renamed-cols", renc),
                        ("index-cols", idxc), ("changed-views", chv),
                        ("added-fks", afk)):
            json.dump(obj, open(f"{out}/{nm}.json", "w"), indent=1)
        print(f"declarations -> {out}/*.json ({len(m)} renames)")
    else:
        main()
