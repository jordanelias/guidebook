"""
scripts/audit/graph/build.py — build audit_graph.db from the repository.

Deterministic and read-only with respect to data/guidebook.db. The audit graph is
a throwaway build artifact (git-ignored): a fresh one is built every run.
"""
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import GraphStore   # noqa: E402
import extract_db              # noqa: E402
import extract_code            # noqa: E402
import extract_content         # noqa: E402
import extract_contract        # noqa: E402
import topology                # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
GUIDEBOOK_DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
DEFAULT_AUDIT_DB = Path(os.environ.get("AUDIT_GRAPH_DB_PATH", REPO_ROOT / "data" / "audit_graph.db"))


def build(audit_db=None, guidebook_db=None) -> GraphStore:
    audit_db = str(audit_db or DEFAULT_AUDIT_DB)
    guidebook_db = str(guidebook_db or GUIDEBOOK_DB)
    if audit_db != ":memory:" and Path(audit_db).exists():
        Path(audit_db).unlink()
    store = GraphStore(audit_db)
    store.init_schema()
    gdb = sqlite3.connect(f"file:{guidebook_db}?mode=ro", uri=True)
    gdb.row_factory = sqlite3.Row
    try:
        extract_db.extract(gdb, store)          # data layer
        extract_code.extract(store, REPO_ROOT)  # code layer (AST table refs)
        extract_content.extract(store, REPO_ROOT)  # content layer (identifier refs)
        extract_contract.extract(store, REPO_ROOT)  # governance contract (stages + checks)
        store.resolve_edges()
        topology.check_all(store, gdb)
        store.set_meta("guidebook_db", guidebook_db)
        store.commit()
    finally:
        gdb.close()
    return store


if __name__ == "__main__":
    s = build()
    print(s.counts())
    s.close()
