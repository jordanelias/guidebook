"""
scripts/audit/graph/extract_code.py — code layer (Tier 0, code).

AST-parses the repo's Python scripts and records, as graph edges, every SQL table
reference (FROM / JOIN / INTO / UPDATE <table>) found inside string literals.
Resolved against the db_table nodes from extract_db, a reference to a table that
does not exist in guidebook.db surfaces as a dangling `table_ref` edge — i.e. a
phantom-table reference (e.g. scripts/generate/room_page.py querying `room`,
`room_item`, ... which were never migrated). This generalises
scripts/audit/schema_reference_drift_audit.py from whole-file regex to AST string
constants (no comments / prose false positives).

Deliberately EXCLUDED from the scan (they address a different schema or are noise):
  - scripts/audit/graph/** and scripts/audit/graph_audit.py (operate on audit_graph.db)
  - scripts/migrations/** (tables are created within migration history)
  - **/__pycache__/**, scripts/test(s)/**
"""
import ast
import re
from pathlib import Path

from model import node_id

# audit_graph.db tables — never treated as guidebook tables even if they leak in
AUDIT_TABLES = {"nodes", "edges", "findings", "build_meta"}
# SQLite pragma-ish / builtin tokens that can follow the keywords but aren't tables
NON_TABLE = {"sqlite_master", "sqlite_sequence", "pragma"}
# English / SQL words that can survive as a token but are never a table name
STOP = {"the", "this", "that", "these", "those", "them", "where", "set", "values",
        "table", "tables", "into", "from", "select", "and", "or", "not", "null",
        "dual", "all", "each", "a", "an", "it", "its", "their", "your", "our"}

# Keywords are matched UPPERCASE-only: the repo's SQL is uppercase, whereas English
# prose ("Update ... from the tables") is not — this is the single most effective
# noise filter (mirrors schema_reference_drift_audit.py's uppercase-SQL assumption).
_SQL_VERB = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|REPLACE)\b")
_TABLE_REF = re.compile(r"\b(?:FROM|JOIN|INTO|UPDATE)\s+[\"'`]?([a-z_][a-z0-9_]{2,})")

EXCLUDE_SUBSTR = ("/audit/graph/", "/migrations/", "/__pycache__/", "/tests/", "/test/")
EXCLUDE_NAMES = {"graph_audit.py", "schema_reference_drift_audit.py"}


def iter_table_refs(text):
    """Yield lower-cased table tokens referenced in a SQL-bearing string. Pure/testable."""
    if not _SQL_VERB.search(text):
        return
    for m in _TABLE_REF.finditer(text):
        tok = m.group(1)
        if tok not in STOP:
            yield tok


def _iter_string_constants(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            yield node.value, getattr(node, "lineno", None)
        elif isinstance(node, ast.JoinedStr):
            # f-string: scan each literal part SEPARATELY. Never bridge across a
            # dropped {interpolation} (that would fabricate "FROM  WHERE" -> "where").
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    yield v.value, getattr(node, "lineno", None)


def _scan_files(repo_root):
    for base in ("scripts", "tools"):
        root = Path(repo_root) / base
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.py")):
            rel = "/" + str(p.relative_to(repo_root)).replace("\\", "/")
            if any(s in rel for s in EXCLUDE_SUBSTR) or p.name in EXCLUDE_NAMES:
                continue
            yield p


def extract(store, repo_root):
    seen = set()  # (file, token) dedupe
    for p in _scan_files(repo_root):
        rel = str(p.relative_to(repo_root)).replace("\\", "/")
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError):
            continue
        file_added = False
        for text, lineno in _iter_string_constants(tree):
            for tok in iter_table_refs(text):
                if tok in AUDIT_TABLES or tok in NON_TABLE:
                    continue
                if (rel, tok) in seen:
                    continue
                seen.add((rel, tok))
                if not file_added:
                    store.add_node("file", rel, subtype="python", path=rel, label=p.name)
                    file_added = True
                store.add_edge(node_id("file", rel), node_id("db_table", tok), "table_ref",
                               src_path=rel, src_line=lineno, attrs={"token": tok})
