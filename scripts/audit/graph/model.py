"""
scripts/audit/graph/model.py — the audit_graph.db store.

A thin wrapper over the derived graph database (nodes / edges / findings /
build_meta). Read-only with respect to data/guidebook.db; the graph DB itself is
a throwaway build artifact rebuilt by build.py.

Node id convention: "<kind>:<key>". Edges may point at a dst node_id that does
not exist yet — resolve_edges() marks those edges resolved=0 (dangling), which is
how dangling identifier references and phantom-table references are detected.
"""
import json
import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def node_id(kind: str, key: str) -> str:
    return f"{kind}:{key}"


class GraphStore:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys=ON")

    def init_schema(self):
        # Fresh build every time: drop any prior artifact content.
        for tbl in ("edges", "nodes", "findings", "build_meta"):
            self.conn.execute(f"DROP TABLE IF EXISTS {tbl}")
        self.conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    def add_node(self, kind, key, subtype=None, path=None, label=None, attrs=None) -> str:
        nid = node_id(kind, key)
        self.conn.execute(
            "INSERT OR REPLACE INTO nodes(node_id,kind,key,subtype,path,label,attrs) "
            "VALUES(?,?,?,?,?,?,?)",
            (nid, kind, key, subtype, path, label, json.dumps(attrs) if attrs is not None else None),
        )
        return nid

    def add_edge(self, src, dst, etype, src_path=None, src_line=None, attrs=None):
        self.conn.execute(
            "INSERT INTO edges(src,dst,etype,src_path,src_line,attrs) VALUES(?,?,?,?,?,?)",
            (src, dst, etype, src_path, src_line, json.dumps(attrs) if attrs is not None else None),
        )

    def resolve_edges(self):
        """Mark every edge whose dst has no node row as dangling (resolved=0)."""
        self.conn.execute(
            "UPDATE edges SET resolved = "
            "CASE WHEN dst IN (SELECT node_id FROM nodes) THEN 1 ELSE 0 END"
        )

    def add_finding(self, check_id, severity, message, node_id=None, known_debt=None, attrs=None):
        self.conn.execute(
            "INSERT INTO findings(check_id,severity,node_id,message,known_debt,attrs) "
            "VALUES(?,?,?,?,?,?)",
            (check_id, severity, node_id, message, known_debt,
             json.dumps(attrs) if attrs is not None else None),
        )

    def set_meta(self, key, value):
        self.conn.execute(
            "INSERT OR REPLACE INTO build_meta(key,value) VALUES(?,?)", (key, str(value))
        )

    def counts(self) -> dict:
        cur = self.conn.cursor()
        return {
            "nodes": cur.execute("SELECT COUNT(*) FROM nodes").fetchone()[0],
            "edges": cur.execute("SELECT COUNT(*) FROM edges").fetchone()[0],
            "dangling_edges": cur.execute("SELECT COUNT(*) FROM edges WHERE resolved=0").fetchone()[0],
            "findings": cur.execute("SELECT COUNT(*) FROM findings").fetchone()[0],
        }

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
