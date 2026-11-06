"""
scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data).

Reads data/guidebook.db READ-ONLY and materialises it into the audit graph:
  - one db_table node per table (with row_count),
  - one entity node per row of each primary entity table (with its lifecycle/state
    columns captured as attrs, for the state-machine layer),
  - citation edges (every FK into evidence_sources.ref_id) so uncited/orphan sources
    are countable,
  - connection_targets slug edges (resolved against slug nodes) so a slug target that
    resolves to no slug surfaces as a dangling edge,
  - a handful of primary structural FK edges (item->slug, item<->population).

Column truth is read from the live DB (sqlite_master / PRAGMA), never from the
Pydantic models, which are a lossy subset.
"""
import re
from model import node_id

# table -> (node kind, primary-key column)
PRIMARY = {
    "evidence_sources": ("source", "ref_id"),
    "base_taxonomy_identity": ("population", "identity_code"),
    "connections": ("connection", "con_id"),
    "gaps": ("gap", "gap_id"),
    "slugs": ("slug", "slug"),
    "terms": ("term", "term_id"),
}

# lifecycle / CHECK-enum columns worth capturing per table for the state-machine layer
STATE_COLS = {
    "connections": ["status", "confidence"],
    "gaps": ["status", "priority"],
    "slugs": ["status"],
    "base_taxonomy_identity": ["status"],
    "evidence_sources": ["verification_status", "metadata_quality", "metadata_integrity_status"],
    "specifications": ["state", "design_scale"],
    "convergence_assessment": ["status"],
    "conflicts": ["status"],
}


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

    # 4. connection_targets -> slug node. A target names ONE kind per column (migration 120); the
    # parameter, identity and extraction kinds are foreign keys and cannot dangle, so the slug is the
    # one kind a graph node is built for. A slug the slugs table lacks (a write with foreign keys off)
    # becomes an unresolved identifier edge. Guarded: a DB without a slugs table must not crash the build.
    if "connection_targets" in tables and "slug" in _columns(cur, "connection_targets"):
        for con_id, slug in cur.execute(
                "SELECT con_id, slug FROM connection_targets WHERE slug IS NOT NULL").fetchall():
            if "slugs" in tables and slug in _slug_cache(cur):
                dst = node_id("slug", slug)
            else:
                dst = node_id("identifier", slug)   # unresolved target
            store.add_edge(node_id("connection", str(con_id)), dst, "junction",
                           attrs={"raw": str(slug)})

    # 5. a primary structural FK edge (population self-reference)
    if "base_taxonomy_identity" in tables and "parent_code" in _columns(cur, "base_taxonomy_identity"):
        for pop, parent in cur.execute(
                "SELECT identity_code, parent_code FROM base_taxonomy_identity WHERE parent_code IS NOT NULL"):
            store.add_edge(node_id("population", pop), node_id("population", parent), "self_ref",
                           attrs={"via": "base_taxonomy_identity.parent_code"})

    # 6. controlled-vocabulary edges (added 2026-07-25).
    # `terms` was already registered in PRIMARY, so 47 term nodes existed, but
    # term_aliases emitted no edges, leaving every term node an isolated island.
    if "term_aliases" in tables:
        # One edge per (term, language) rather than per alias: the audit needs to
        # know which terms carry which language coverage, not to re-store 2k aliases.
        for term_id, lang, n in cur.execute(
                "SELECT term_id, language, COUNT(*) FROM term_aliases "
                "GROUP BY term_id, language"):
            store.add_edge(node_id("term", term_id), node_id("db_table", "term_aliases"),
                           "junction", attrs={"via": "term_aliases", "language": lang,
                                              "alias_count": n})

    store.set_meta("guidebook_user_version",
                   cur.execute("PRAGMA user_version").fetchone()[0])
    return row_counts


_SLUGS = None


def _slug_cache(cur):
    global _SLUGS
    if _SLUGS is None:
        _SLUGS = {r[0] for r in cur.execute("SELECT slug FROM slugs").fetchall()}
    return _SLUGS
