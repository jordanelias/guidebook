#!/usr/bin/env python3
"""Table connectivity audit — can every table be reached, and does every
pointer resolve?

Four sections:

  A  ISLANDS        tables no declared foreign key reaches, in or out
  B  EDGES          orphan rate on every declared FK and every declared soft edge
  C  SPINE          can the product pipeline actually be walked end to end
  D  MISSING        schema that cannot express what the data is attempting

Section D is the one that does not fit a normal integrity check. A free-text
column holding 'All C-items' is not corrupt data — it is a *feature the schema
lacks*, showing up as prose because there was nowhere else to put it. Those are
reported separately from defects, because the fix is a column, not a cleanup.

The SOFT_EDGES table below is the deliberate, hand-maintained part: relationships
the data relies on that SQLite does not declare. Everything else is derived from
PRAGMA at run time. Do not transcribe anything here that PRAGMA already knows —
a private copy of the schema is how a checker starts lying.

Usage:
    python3 scripts/audit/table_connectivity.py [--verbose] [--strict]

--strict makes soft-edge orphans and unreachable spine hops fail the run.
Default is report-only for those; declared-FK violations always fail.
"""
import argparse
import collections
import os
import sqlite3
import sys

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

# ── the declared soft edges ───────────────────────────────────────────────────
# (child_table, child_col, parent_table, parent_col, enforce)
#   enforce='required' — should be a real FK; an orphan here is a defect
#   enforce='waived'   — known not to resolve today, with the reason
SOFT_EDGES = [
    ("citation_mining", "global_ref_id", "evidence_sources", "ref_id", "required"),
    ("evidence_population_match", "ref_id", "evidence_sources", "ref_id", "required"),
    ("evidence_population_match", "source_ref", "evidence_sources", "ref_id", "waived"),
    ("evidence_population_match", "target_population", "populations", "population_code", "waived"),
    ("population_reclass", "population_code", "populations", "population_code", "waived"),
    ("population_reclass", "canonical_code", "populations", "population_code", "waived"),
    ("evidence_sources", "jurisdiction", "lang_jur_map", "jurisdiction", "waived"),
    ("connection_targets", "target", "items", "item_code", "waived"),
    ("economics_entries", "ref_id", "evidence_sources", "ref_id", "required"),
    ("spec_value_probes", "ref_id", "evidence_sources", "ref_id", "required"),
    ("source_value_extractions", "root_ref_id", "evidence_sources", "ref_id", "required"),
    ("source_value_extractions", "root_id", "external_root_registry", "root_id", "waived"),
    ("jurisdictional_values", "item_code", "items", "item_code", "required"),
    ("bpc_metadata", "slug", "slugs", "slug", "required"),
]

WAIVER_REASON = {
    ("evidence_population_match", "source_ref"):
        "legacy free-text citations ('Koontz et al. 2005'); ref_id is the live key",
    ("evidence_population_match", "target_population"):
        "holds population prose, not codes — needs a coded column (section D)",
    ("population_reclass", "population_code"):
        "records codes that were RETIRED; by design they no longer resolve",
    ("population_reclass", "canonical_code"):
        "target vocabulary lives in governance/population-taxonomy.md, not a table",
    ("evidence_sources", "jurisdiction"):
        "jurisdiction vocabulary is wider than the 48-row lang_jur_map",
    ("connection_targets", "target"):
        "free text mixing item codes, class selectors and commentary (section D)",
    ("source_value_extractions", "root_id"):
        "external_root_registry is empty scaffolding",
}

# ── the spine is NOT a line ───────────────────────────────────────────────────
# Evidence and demand are two axes that MEET at evidence_cell_state, which is
# keyed on (item_code, population_code) precisely because the cell is the
# meeting point. Population is not downstream of the specification — it
# qualifies the evidence at stage 5 and the specification is derived per
# population. An earlier version of this file listed
# "specification → population applicability" as the last hop, which inverts the
# causality and made a 99% number look like success when the underlying claim
# is unjustified 96.5% of the time (see [C2]).
SPINE_EVIDENCE = [
    ("slugs", "topic → its sources",
     "SELECT COUNT(DISTINCT slug) FROM source_slug_links"),
    ("source_slug_links", "source link → the source",
     "SELECT COUNT(DISTINCT ref_id) FROM source_slug_links"),
    ("evidence_sources", "source → captured values",
     "SELECT COUNT(DISTINCT ref_id) FROM source_value_extractions"),
    ("evidence_sources", "source → synthesis cell (via governing_refs)",
     "SELECT COUNT(*) FROM evidence_cell_state WHERE COALESCE(governing_refs,'[]') <> '[]'"),
]
SPINE_DEMAND = [
    ("axes", "functional axis → population",
     "SELECT COUNT(DISTINCT axis_code) FROM population_axis_map"),
    ("populations", "population → matched evidence (stage 5)",
     "SELECT COUNT(DISTINCT target_population) FROM evidence_population_match "
     "WHERE target_population IN (SELECT population_code FROM populations)"),
    ("populations", "population → specification applicability",
     "SELECT COUNT(DISTINCT population_code) FROM item_population_links"),
]
SPINE_MEET = [
    ("evidence_cell_state", "cell → specification",
     "SELECT COUNT(DISTINCT item_code) FROM evidence_cell_state"),
    ("items", "specification → rendered page",
     "SELECT COUNT(DISTINCT item_code) FROM evidence_cell_state"),
]


def q1(con, sql, default=0):
    try:
        return con.execute(sql).fetchone()[0]
    except sqlite3.Error:
        return default


def declared_edges(con, tables):
    out = []
    for t in tables:
        for r in con.execute(f"PRAGMA foreign_key_list({t})"):
            out.append((t, r[3], r[2], r[4] or "rowid"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    rows = {t: q1(con, f"SELECT COUNT(*) FROM {t}") for t in tables}
    fks = declared_edges(con, tables)
    examined = 0
    hard_fail, soft_fail = [], []

    # ── A: islands ────────────────────────────────────────────────────────────
    print("[A] Islands — tables no declared foreign key reaches")
    adj = collections.defaultdict(set)
    for c, _, p, _ in fks:
        adj[c].add(p)
        adj[p].add(c)
    soft_adj = collections.defaultdict(set)
    for c, _, p, _, _ in SOFT_EDGES:
        soft_adj[c].add(p)
        soft_adj[p].add(c)

    LEDGERS = {"data_migrations", "db_meta", "pipeline_runs", "url_verification_runs"}
    islands = [t for t in tables if not adj[t]]
    examined += len(tables)
    for t in sorted(islands):
        kind = ("ledger, standalone by design" if t in LEDGERS else
                "empty scaffolding" if rows[t] == 0 else
                f"reachable only by a SOFT edge ({', '.join(sorted(soft_adj[t]))})" if soft_adj[t] else
                "DISCONNECTED — holds data, nothing points at it")
        flag = "!!" if kind.startswith("DISCONNECTED") else "  "
        print(f"  {flag} {t:28s} {rows[t]:>6} rows  — {kind}")
        if kind.startswith("DISCONNECTED"):
            soft_fail.append(f"{t} is disconnected with {rows[t]} rows")

    # ── B: edges ──────────────────────────────────────────────────────────────
    print("\n[B] Edges — does every pointer resolve?")
    bad_declared = 0
    for c, ccol, p, pcol in fks:
        n = q1(con, f"SELECT COUNT(*) FROM {c} WHERE {ccol} IS NOT NULL "
                    f"AND {ccol} NOT IN (SELECT {pcol} FROM {p})")
        examined += 1
        if n:
            bad_declared += 1
            hard_fail.append(f"declared FK {c}.{ccol} → {p}.{pcol}: {n} orphan(s)")
            print(f"  !! {c}.{ccol} → {p}.{pcol}: {n} orphan(s)")
    print(f"  {len(fks)} declared foreign keys, {bad_declared} with orphans")

    print(f"  {len(SOFT_EDGES)} declared soft edges:")
    for c, ccol, p, pcol, enforce in SOFT_EDGES:
        total = q1(con, f"SELECT COUNT(*) FROM {c} WHERE {ccol} IS NOT NULL AND {ccol} <> ''")
        n = q1(con, f"SELECT COUNT(*) FROM {c} WHERE {ccol} IS NOT NULL AND {ccol} <> '' "
                    f"AND {ccol} NOT IN (SELECT {pcol} FROM {p})")
        examined += 1
        pct = f"{n}/{total}"
        if enforce == "required" and n:
            soft_fail.append(f"soft edge {c}.{ccol} → {p}.{pcol}: {pct} unresolved")
            print(f"  !! {c}.{ccol:22s} → {p:26s} {pct:>10} unresolved  [required]")
        elif args.verbose or n:
            why = WAIVER_REASON.get((c, ccol), "")
            print(f"     {c}.{ccol:22s} → {p:26s} {pct:>10} unresolved  "
                  f"[{enforce}]{' — ' + why if why else ''}")

    # ── C: the end-to-end walk ────────────────────────────────────────────────
    # The requirement is not "each hop has decent coverage" — it is that a
    # topic can be walked all the way to a best practice. Per-hop percentages
    # hide this: 79% and 99% look healthy while the COMPOSITION is near zero.
    print("\n[C] End-to-end walk — topic → … → best practice, per topic")
    STAGES = [
        ("1 topic",            "SELECT 1"),
        ("2 has sources",      "SELECT 1 FROM source_slug_links l WHERE l.slug=:s LIMIT 1"),
        ("3 sources mined",    "SELECT 1 FROM source_slug_links l JOIN evidence_sources e ON e.ref_id=l.ref_id "
                               "WHERE l.slug=:s AND e.citation_mining_status='mined' LIMIT 1"),
        ("4 values captured",  "SELECT 1 FROM source_slug_links l JOIN evidence_sources e ON e.ref_id=l.ref_id "
                               "WHERE l.slug=:s AND e.data_capture_status='captured' LIMIT 1"),
        ("5 population match", "SELECT 1 FROM source_slug_links l JOIN evidence_population_match m ON m.ref_id=l.ref_id "
                               "WHERE l.slug=:s AND m.target_population IN (SELECT population_code FROM populations) LIMIT 1"),
        ("6 has a spec",       "SELECT 1 FROM items i WHERE i.bpc_source_slug=:s LIMIT 1"),
        ("7 spec has a cell",  "SELECT 1 FROM items i JOIN evidence_cell_state c ON c.item_code=i.item_code "
                               "WHERE i.bpc_source_slug=:s LIMIT 1"),
        ("8 BEST PRACTICE",    "SELECT 1 FROM items i JOIN evidence_cell_state c ON c.item_code=i.item_code "
                               "WHERE i.bpc_source_slug=:s AND c.state IN ('stated','provisional') LIMIT 1"),
    ]
    slugs = [r[0] for r in con.execute("SELECT slug FROM slugs WHERE status='ACTIVE'")]
    furthest = collections.Counter()
    complete = []
    for s in slugs:
        got = 0
        for i, (_, sql) in enumerate(STAGES):
            try:
                hit = con.execute(sql, {"s": s}).fetchone() if ":s" in sql else (1,)
            except sqlite3.Error:
                hit = None
            if hit is None:
                break
            got = i
        furthest[got] += 1
        if got == len(STAGES) - 1:
            complete.append(s)
    examined += len(slugs)
    running = len(slugs)
    for i, (label, _) in enumerate(STAGES):
        reached = sum(v for k, v in furthest.items() if k >= i)
        pct = 100.0 * reached / len(slugs) if slugs else 0
        lost = furthest.get(i - 1, 0) if i else 0
        mark = "!!" if reached == 0 else "  "
        print(f"  {mark} {label:22s} {reached:>4}/{len(slugs)} ACTIVE topics  {pct:5.1f}%"
              f"{'   ← ' + str(lost) + ' stop here' if lost else ''}")
    print(f"\n  TOPICS COMPLETING THE FULL WALK: {len(complete)} of {len(slugs)}"
          f"{'  → ' + ', '.join(complete[:5]) if complete else ''}")
    if not complete:
        soft_fail.append("no ACTIVE topic can be walked from topic to best practice")

    print("\n[C2] Is spec↔population applicability justified by matched evidence?")
    just = q1(con, """SELECT COUNT(*) FROM item_population_links ipl WHERE EXISTS (
        SELECT 1 FROM items i
        JOIN source_slug_links l ON l.slug = i.bpc_source_slug
        JOIN evidence_population_match m ON m.ref_id = l.ref_id
        WHERE i.item_code = ipl.item_code AND m.target_population = ipl.population_code)""")
    tot = rows.get("item_population_links", 0)
    examined += 1
    print(f"     {just} of {tot} spec↔population claims trace to population-matched evidence"
          f"  ({100.0*just/tot if tot else 0:.1f}%)")
    if tot and just < tot:
        soft_fail.append(f"{tot-just} spec↔population claims unjustified by evidence")

    # ── D: missing features ───────────────────────────────────────────────────
    print("\n[D] Missing features — data attempting what the schema cannot express")
    findings = []

    n = q1(con, "SELECT COUNT(*) FROM connection_targets WHERE target NOT IN "
                "(SELECT item_code FROM items) AND target NOT LIKE 'item:%'")
    tot = q1(con, "SELECT COUNT(*) FROM connection_targets")
    if n:
        findings.append((f"connection_targets.target", f"{n}/{tot}",
                         "one free-text column carrying item codes, CLASS selectors "
                         "('All C-items') and commentary. Needs target_type + target_code; "
                         "class selectors are a missing feature, not bad data"))

    n = q1(con, "SELECT COUNT(*) FROM evidence_population_match WHERE target_population "
                "NOT IN (SELECT population_code FROM populations)")
    tot = q1(con, "SELECT COUNT(*) FROM evidence_population_match")
    if n:
        findings.append(("evidence_population_match.target_population", f"{n}/{tot}",
                         "population written as prose; no coded column exists"))

    n = q1(con, "SELECT COUNT(*) FROM jurisdictional_values")
    if n and "ref_id" not in [r[1] for r in con.execute("PRAGMA table_info(jurisdictional_values)")]:
        findings.append(("jurisdictional_values", f"{n} rows",
                         "no ref_id column at all — provenance is free-text standard_name, "
                         "so no row can be traced to a source"))

    n = q1(con, "SELECT COUNT(*) FROM conflicts")
    cols = [r[1] for r in con.execute("PRAGMA table_info(conflicts)")]
    if "resolution_type" not in cols:
        findings.append(("conflicts.resolution", f"{n} rows",
                         "resolution is free text with no coded type, so 'dissolved — the "
                         "populations measure different variables' is indistinguishable from "
                         "'genuine opposition, unresolved'"))

    if "term_relations" not in tables:
        findings.append(("term_relations", "MISSING",
                         "concept→concept relations have no table. terms→items and items→axes "
                         "exist; nothing relates one concept to another, so no walk can find "
                         "which specifications to test against each other"))

    if "cross_examinations" not in tables:
        n = q1(con, "SELECT COUNT(*) FROM connections")
        findings.append(("cross_examinations", "MISSING",
                         f"connections ({n}) records relationships FOUND; nothing records pairs "
                         "EXAMINED, so 'unrelated' and 'never looked' are the same absence"))

    for name, scale, why in findings:
        print(f"  ~~ {name:42s} {scale:>10}  {why}")
    examined += len(findings)

    # ── verdict ───────────────────────────────────────────────────────────────
    print(f"\nEXAMINED: {examined}")
    print("=" * 70)
    for f in hard_fail:
        print(f"  FAIL   {f}")
    for f in soft_fail:
        print(f"  REPORT {f}")
    print(f"  {len(findings)} missing-feature finding(s)")
    failed = bool(hard_fail) or (args.strict and bool(soft_fail))
    print(f"VERDICT: {'FAIL' if failed else 'PASS'}"
          f"  (declared-FK violations: {len(hard_fail)}; reported: {len(soft_fail)})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
