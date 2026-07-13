"""
scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only).

Each check appends rows to the findings table. Severity is raw here; known-debt
suppression and the pass/fail decision live in scripts/audit/graph_audit.py.

Checks (data layer, increment 1):
  orphan.uncited_source        source with no inbound citation edge (WARN)
  orphan.dangling_citation     value-layer ref with no evidence_sources row (ERROR)
  ref.unresolved_conn_target   connection_target not resolving to item/slug (WARN),
                               split into phantom-item vs unresolved-identifier
  table.empty_mission_critical curated mission-critical table at/near 0 rows (INFO)
  connection.empty_description connection rows with empty description (INFO)
  cycle.population_parent      populations.parent_code cycle (ERROR)
  state.distribution           lifecycle state distributions (INFO)
  graph.components             connected-component / island count (INFO)
"""

# Mission-critical tables and the row-count floor below which we surface a finding.
MISSION_CRITICAL = {
    "source_value_extractions": 1,
    "conflicts": 1,
    "convergence_assessment": 1,
    "reasoning_doc_citations": 1,
    "gap_mining": 1,
    "extraction_population_links": 1,
    "lang_jur_map": 1,
    "evidence_cell_state": 20,   # 7 pilot rows today; full backfill is ~ hundreds
}

STATE_DIST = {
    "items": "status",
    "connections": "status",
    "gaps": "status",
    "slugs": "status",
    "evidence_sources": "verification_status",
    "evidence_cell_state": "state",
    "convergence_assessment": "status",
}


def check_all(store, gdb):
    orphan_sources(store)
    dangling_citations(store)
    unresolved_connection_targets(store)
    code_phantom_tables(store)
    content_phantom_identifiers(store)
    empty_mission_critical(store)
    empty_description_connections(store)
    population_parent_cycles(store)
    state_distribution(store, gdb)
    components(store)


def orphan_sources(store):
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT n.node_id, n.key FROM nodes n WHERE n.kind='source' "
        "AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.dst=n.node_id "
        "                AND e.etype='citation' AND e.resolved=1)"
    ).fetchall()
    for nid, key in rows:
        store.add_finding("orphan.uncited_source", "WARN",
                          f"Source {key} is cited by nothing (no source_slug_links / value-layer / mining edge).",
                          node_id=nid)
    store.add_finding("orphan.uncited_source", "INFO",
                      f"{len(rows)} evidence source(s) cited by nothing.", attrs={"count": len(rows)})


def dangling_citations(store):
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT dst, attrs FROM edges WHERE etype='citation' AND resolved=0"
    ).fetchall()
    for dst, attrs in rows:
        store.add_finding("orphan.dangling_citation", "ERROR",
                          f"Value-layer citation references non-existent source {dst.split(':',1)[-1]}.",
                          node_id=dst, attrs={"edge_attrs": attrs})
    store.add_finding("orphan.dangling_citation", "INFO",
                      f"{len(rows)} dangling value-layer citation(s) (orphan_links).",
                      attrs={"count": len(rows)})


def unresolved_connection_targets(store):
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT src, dst FROM edges WHERE etype='junction' AND resolved=0 AND src LIKE 'connection:%'"
    ).fetchall()
    phantom_items, unresolved = 0, 0
    for src, dst in rows:
        if dst.startswith("item:"):
            phantom_items += 1
            store.add_finding("ref.unresolved_conn_target", "WARN",
                              f"{src.split(':',1)[-1]} targets phantom item {dst.split(':',1)[-1]}.",
                              node_id=src)
        else:
            unresolved += 1
            store.add_finding("ref.unresolved_conn_target", "WARN",
                              f"{src.split(':',1)[-1]} target {dst.split(':',1)[-1]} does not resolve to an item or slug.",
                              node_id=src)
    store.add_finding("ref.unresolved_conn_target", "INFO",
                      f"{len(rows)} unresolved connection target(s): "
                      f"{phantom_items} phantom-item, {unresolved} unresolved.",
                      attrs={"total": len(rows), "phantom_items": phantom_items, "unresolved": unresolved})


def code_phantom_tables(store):
    """table_ref edges from code to a table that does not exist in guidebook.db."""
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT src_path, dst, src_line FROM edges "
        "WHERE etype='table_ref' AND resolved=0 ORDER BY src_path, dst"
    ).fetchall()
    for src_path, dst, line in rows:
        tok = dst.split(":", 1)[-1]
        store.add_finding("code.phantom_table", "WARN",
                          f"{src_path}:{line} references table '{tok}' which does not exist "
                          f"in guidebook.db (dormant / stale query).",
                          node_id=f"file:{src_path}", attrs={"table": tok, "line": line})
    files = len({r[0] for r in rows})
    store.add_finding("code.phantom_table", "INFO",
                      f"{len(rows)} phantom-table reference(s) across {files} script(s).",
                      attrs={"count": len(rows), "files": files})


def content_phantom_identifiers(store):
    """ref edges from prose to an identifier that resolves to no entity node."""
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT src_path, dst FROM edges WHERE etype='ref' AND resolved=0 ORDER BY dst, src_path"
    ).fetchall()
    by_kind = {}
    for src_path, dst in rows:
        kind, ident = dst.split(":", 1)
        by_kind[kind] = by_kind.get(kind, 0) + 1
        store.add_finding("ref.phantom_identifier", "WARN",
                          f"{src_path} references {kind} '{ident}' which resolves to no entity "
                          f"(candidate phantom/stale reference).",
                          node_id=dst, attrs={"kind": kind, "id": ident, "file": src_path})
    store.add_finding("ref.phantom_identifier", "INFO",
                      f"{len(rows)} candidate phantom identifier reference(s): {by_kind}.",
                      attrs={"count": len(rows), "by_kind": by_kind})


def empty_mission_critical(store):
    import json
    cur = store.conn.cursor()
    for table, floor in MISSION_CRITICAL.items():
        row = cur.execute("SELECT attrs FROM nodes WHERE node_id=?",
                          (f"db_table:{table}",)).fetchone()
        if not row or not row[0]:
            continue
        n = json.loads(row[0]).get("row_count", 0)
        if n < floor:
            store.add_finding("table.empty_mission_critical", "INFO",
                              f"Mission-critical table {table} has {n} rows (floor {floor}).",
                              node_id=f"db_table:{table}", attrs={"table": table, "row_count": n, "floor": floor})


def empty_description_connections(store):
    import json
    cur = store.conn.cursor()
    n = 0
    for (attrs,) in cur.execute("SELECT attrs FROM nodes WHERE kind='connection' AND attrs IS NOT NULL"):
        if json.loads(attrs).get("description_empty") == 1:
            n += 1
    store.add_finding("connection.empty_description", "INFO",
                      f"{n} connection(s) have an empty description.", attrs={"count": n})


def population_parent_cycles(store):
    cur = store.conn.cursor()
    parent = {}
    for src, dst in cur.execute("SELECT src, dst FROM edges WHERE etype='self_ref'"):
        parent[src] = dst
    for start in list(parent):
        seen, node = set(), start
        while node in parent:
            if node in seen:
                store.add_finding("cycle.population_parent", "ERROR",
                                  f"Population parent chain forms a cycle at {node.split(':',1)[-1]}.",
                                  node_id=node)
                break
            seen.add(node)
            node = parent[node]


def state_distribution(store, gdb):
    gc = gdb.cursor()
    tables = {r[0] for r in gc.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    for table, col in STATE_DIST.items():
        if table not in tables:
            continue
        cols = [r[1] for r in gc.execute(f"PRAGMA table_info({table})").fetchall()]
        if col not in cols:
            continue
        dist = {str(v): n for v, n in gc.execute(
            f"SELECT {col}, COUNT(*) FROM {table} GROUP BY {col}").fetchall()}
        store.add_finding("state.distribution", "INFO",
                          f"{table}.{col}: {dist}", attrs={"table": table, "column": col, "dist": dist})


def components(store):
    cur = store.conn.cursor()
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for (nid,) in cur.execute("SELECT node_id FROM nodes"):
        find(nid)
    for src, dst in cur.execute("SELECT src, dst FROM edges WHERE resolved=1"):
        find(src); find(dst); union(src, dst)
    roots = {find(x) for x in parent}
    store.add_finding("graph.components", "INFO",
                      f"{len(roots)} connected component(s) across {len(parent)} node(s).",
                      attrs={"components": len(roots), "nodes": len(parent)})
