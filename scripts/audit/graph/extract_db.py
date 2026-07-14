"""
scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data).

Reads data/guidebook.db READ-ONLY and materialises it into the audit graph:
  - one db_table node per table (with row_count),
  - one entity node per row of each primary entity table (with its lifecycle/state
    columns captured as attrs, for the state-machine layer),
  - citation edges (every FK into evidence_sources.ref_id) so uncited/orphan sources
    are countable,
  - connection_targets edges (resolved against item/slug nodes) so unresolved and
    phantom targets surface as dangling edges,
  - a handful of primary structural FK edges (item->slug, item<->population).

Column truth is read from the live DB (sqlite_master / PRAGMA), never from the
Pydantic models, which are a lossy subset.
"""
import re
from model import node_id

# table -> (node kind, primary-key column)
PRIMARY = {
    "items": ("item", "item_code"),
    "evidence_sources": ("source", "ref_id"),
    "populations": ("population", "population_code"),
    "connections": ("connection", "con_id"),
    "gaps": ("gap", "gap_id"),
    "slugs": ("slug", "slug"),
    "terms": ("term", "term_id"),
}

# lifecycle / CHECK-enum columns worth capturing per table for the state-machine layer
STATE_COLS = {
    "items": ["status"],
    "connections": ["status", "confidence"],
    "gaps": ["status", "priority"],
    "slugs": ["status"],
    "populations": ["status"],
    "evidence_sources": ["verification_status", "metadata_quality", "metadata_integrity_status"],
    "evidence_cell_state": ["state", "design_scale"],
    "convergence_assessment": ["status"],
    "conflicts": ["status"],
}

ITEM_CODE_RE = re.compile(r"^[A-K]-\d{2}$")
AUDIT_COLS = {"created_at", "created_by_session", "updated_at", "updated_by_session"}


def _columns(cur, table):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()]


def _tables(cur):
    return [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()]


def _fk_list(cur, table):
    # (id, seq, parent_table, from_col, to_col, on_update, on_delete, match)
    return cur.execute(f"PRAGMA foreign_key_list({table})").fetchall()


def extract(gdb, store):
    """gdb: read-only sqlite3.Connection on guidebook.db. store: GraphStore."""
    global _SLUGS
    _SLUGS = None  # reset the per-build slug memo (never carry it across DBs)
    cur = gdb.cursor()
    tables = _tables(cur)

    # 1. db_table nodes with row counts
    row_counts = {}
    for t in tables:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        row_counts[t] = n
        store.add_node("db_table", t, subtype="table", label=t, attrs={"row_count": n})
    # Views are legitimate query targets too — register them so code that reads
    # v_best_practice / v_divergence / ... resolves instead of looking phantom.
    for (v,) in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name").fetchall():
        store.add_node("db_table", v, subtype="view", label=v)

    # 2. primary entity nodes (with state attrs)
    for table, (kind, pk) in PRIMARY.items():
        if table not in tables:
            continue
        cols = _columns(cur, table)
        keep = [c for c in STATE_COLS.get(table, []) if c in cols]
        extra = ""
        if table == "connections" and "description" in cols:
            keep = keep + ["description"]
        sel = ", ".join([pk] + keep) if keep else pk
        for row in cur.execute(f"SELECT {sel} FROM {table}").fetchall():
            key = row[pk]
            if key is None:
                continue
            attrs = {c: row[c] for c in keep} if keep else None
            if attrs and "description" in attrs:
                # store only emptiness, not the whole body
                d = attrs.pop("description")
                attrs["description_empty"] = 1 if (d is None or str(d).strip() == "") else 0
            store.add_node(kind, str(key), subtype=table, attrs=attrs)

    # 3. citation edges: every FK into evidence_sources.ref_id
    for t in tables:
        for fk in _fk_list(cur, t):
            parent, from_col, to_col = fk[2], fk[3], fk[4]
            if parent == "evidence_sources" and to_col == "ref_id":
                refs = cur.execute(
                    f"SELECT DISTINCT {from_col} FROM {t} WHERE {from_col} IS NOT NULL"
                ).fetchall()
                for (ref,) in refs:
                    store.add_edge(node_id("db_table", t), node_id("source", str(ref)),
                                   "citation", attrs={"via": f"{t}.{from_col}"})

    # 4. connection_targets -> resolved item/slug (dangling => phantom/unresolved)
    if "connection_targets" in tables:
        ct_cols = _columns(cur, "connection_targets")
        tgt_col = "target" if "target" in ct_cols else next(
            (c for c in ct_cols if c not in ("con_id",) and c not in AUDIT_COLS), None)
        if tgt_col:
            for con_id, raw in cur.execute(
                    f"SELECT con_id, {tgt_col} FROM connection_targets").fetchall():
                if raw is None:
                    continue
                token = str(raw).split(":", 1)[-1].strip()  # strip "item:"/"section:" prefix
                if ITEM_CODE_RE.match(token):
                    dst = node_id("item", token)
                elif "slugs" in tables and token in _slug_cache(cur):
                    dst = node_id("slug", token)   # guarded: a DB without a slugs table
                else:                              # must not crash the whole build
                    dst = node_id("identifier", token)   # unresolved target
                store.add_edge(node_id("connection", str(con_id)), dst, "junction",
                               attrs={"raw": str(raw)})

    # 5. a few primary structural FK edges (item->slug, item<->population)
    if "items" in tables and "bpc_source_slug" in _columns(cur, "items"):
        for item_code, slug in cur.execute(
                "SELECT item_code, bpc_source_slug FROM items WHERE bpc_source_slug IS NOT NULL"):
            store.add_edge(node_id("item", item_code), node_id("slug", slug), "fk",
                           attrs={"via": "items.bpc_source_slug"})
    if "item_population_links" in tables:
        for item_code, pop in cur.execute(
                "SELECT item_code, population_code FROM item_population_links"):
            store.add_edge(node_id("item", item_code), node_id("population", pop), "junction",
                           attrs={"via": "item_population_links"})
    if "populations" in tables and "parent_code" in _columns(cur, "populations"):
        for pop, parent in cur.execute(
                "SELECT population_code, parent_code FROM populations WHERE parent_code IS NOT NULL"):
            store.add_edge(node_id("population", pop), node_id("population", parent), "self_ref",
                           attrs={"via": "populations.parent_code"})

    store.set_meta("guidebook_user_version",
                   cur.execute("PRAGMA user_version").fetchone()[0])
    return row_counts


_SLUGS = None


def _slug_cache(cur):
    global _SLUGS
    if _SLUGS is None:
        _SLUGS = {r[0] for r in cur.execute("SELECT slug FROM slugs").fetchall()}
    return _SLUGS
