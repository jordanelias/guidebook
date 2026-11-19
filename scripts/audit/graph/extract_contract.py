"""
scripts/audit/graph/extract_contract.py — ingest the pipeline contract into the graph.

Reads governance/pipeline-contract.yaml and materialises its stages and the
enforcer each stage criterion names, as `stage` nodes and `stage_check` edges to
the enforcer `file` nodes, and each ruled return (a stage's `re_entry` entry) as a
`ruled_return` edge from the later stage it comes from to the stage it re-enters. This closes the loop the contract was designed for: the
governance contract's own structure becomes edges the vectorized audit traverses,
and an enforcer path that does not exist on disk surfaces as a dangling edge just
like any other phantom reference.

Deliberately dependency-light and fully graceful: parses YAML directly (never
pydantic, so the graph spine keeps its stdlib+PyYAML footprint) and skips silently
on any missing/malformed contract, so a contract problem can never break the graph.
"""
from pathlib import Path

from model import node_id


def extract(store, repo_root):
    try:
        import yaml
    except ImportError:
        return
    path = Path(repo_root) / "governance" / "pipeline-contract.yaml"
    if not path.exists():
        return
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        _ingest(store, repo_root, doc)
    except Exception:  # noqa: BLE001 — a contract problem must never break the graph build
        return


def _check_edge(store, repo_root, src_node, check, attrs):
    if not check:
        return
    if (Path(repo_root) / check).exists():
        store.add_node("file", check, subtype="python", path=check)
    store.add_edge(src_node, node_id("file", check), "stage_check", attrs=attrs)


def returns(doc):
    """The ruled returns: one dict per `re_entry` entry of a stage, in contract order. Both graphs read the
    returns here (this one and workplan/pipeline-state-graph/build_graph.py)."""
    for st in doc.get("stages", []) or []:
        for r in st.get("re_entry", []) or []:
            yield dict(id=r.get("id"), from_stage=r.get("from_stage"), to_stage=st.get("id"),
                       carrier_table=r.get("carrier_table"), carrier_column=r.get("carrier_column"),
                       carrier_value=r.get("carrier_value"))


def _ingest(store, repo_root, doc):
    for st in doc.get("stages", []) or []:
        sid = st.get("id")
        if not sid:
            continue
        s_node = store.add_node("stage", sid, subtype="pipeline",
                                attrs={"anchor": st.get("anchor"),
                                       "n_criteria": len(st.get("criteria", []) or [])})
        for c in st.get("criteria", []) or []:
            _check_edge(store, repo_root, s_node, c.get("check"),
                        {"criterion": c.get("id"), "kind": c.get("kind")})
    for g in doc.get("cross_stage", []) or []:
        gid = g.get("id")
        if not gid:
            continue
        g_node = store.add_node("stage", f"cross_stage:{gid}", subtype="cross_stage",
                                attrs={"gate": gid})
        _check_edge(store, repo_root, g_node, g.get("check"), {"gate": gid})
    for r in returns(doc):
        store.add_edge(node_id("stage", r["from_stage"]), node_id("stage", r["to_stage"]), "ruled_return",
                       attrs={k: v for k, v in r.items() if k not in ("from_stage", "to_stage")})
