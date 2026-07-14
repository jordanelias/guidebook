"""
scripts/audit/graph/extract_content.py — content layer (Tier 0, prose).

Scans repository markdown for references in the project's identifier scheme
(item A-01..K-NN, source REF-NNNNN / REF-VERIFIED-NNN / CoN-NN, connection CON-NNNN,
gap GAP-NNN, term TERM-NNN) and resolves each against the entity nodes built by extract_db.
A reference that does not resolve to a real entity surfaces as a dangling `ref`
edge — a phantom / stale identifier reference (e.g. item codes referenced in prose
that are absent from the 92-row items table, such as F-07). This is the prose<->data
seam a single-corpus tool can't see. (Archived/deprecated trees are excluded, so
retired identifiers kept only for git history are not flagged.)

Careful/lean policy for this increment: only PHANTOM (dangling) references are
materialised as edges; resolved references are counted per file (content-node
attrs) rather than exploded into tens of thousands of edges. Full resolved
content->entity edges are deferred to the embedding tier that needs them.

Archived / deprecated / superseded / frozen trees are excluded (they are kept
only for git history and legitimately cite retired identifiers).
"""
import re
from pathlib import Path

from model import node_id

CONTENT_ROOTS = ("parts", "references", "governance", "skills", "decisions",
                 "workplan", "architecture", "audits")
EXCLUDE_SUBSTR = ("/_archived/", "/deprecated/", "/_superseded/", "/versions/",
                  "/__pycache__/", "/88_to_90/")

# (kind, compiled pattern). Item pattern uses boundaries that reject alphanumerics
# and hyphens on both sides, so "COVID-19" / "ISO-9001" / "x-A-01" do not match.
PATTERNS = (
    ("item", re.compile(r"(?<![A-Za-z0-9/\-])[A-K]-\d{2}(?![0-9A-Za-z])")),
    ("source", re.compile(r"\bREF-VERIFIED-\d{3}\b")),   # tried before REF-\d{5} (disjoint anyway)
    ("source", re.compile(r"\bREF-\d{5}\b")),
    ("source", re.compile(r"\bCo[12]-\d{2,}\b")),
    ("connection", re.compile(r"\bCON-\d{4}\b")),
    ("gap", re.compile(r"\bGAP-\d{3,4}\b")),
    ("term", re.compile(r"\bTERM-\d{3,4}\b")),   # term_ids are 3-digit (TERM-001..TERM-030); \d{4} matched none
)

REGISTRY_KINDS = ("item", "source", "connection", "gap", "term")


def iter_identifier_refs(text):
    """Yield (kind, identifier) for every scheme reference in text. Pure/testable."""
    for kind, pat in PATTERNS:
        for m in pat.finditer(text):
            yield kind, m.group(0)


def _valid_ids(store):
    cur = store.conn.cursor()
    valid = {}
    for kind in REGISTRY_KINDS:
        valid[kind] = {r[0] for r in cur.execute(
            "SELECT key FROM nodes WHERE kind=?", (kind,)).fetchall()}
    return valid


def _scan_files(repo_root):
    for base in CONTENT_ROOTS:
        root = Path(repo_root) / base
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.md")):
            rel = "/" + str(p.relative_to(repo_root)).replace("\\", "/")
            if any(s in rel for s in EXCLUDE_SUBSTR):
                continue
            yield p


def extract(store, repo_root):
    valid = _valid_ids(store)
    for p in _scan_files(repo_root):
        rel = str(p.relative_to(repo_root)).replace("\\", "/")
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        resolved = 0
        phantom = {}  # (kind, id) -> 1  (dedupe within file)
        for kind, ident in iter_identifier_refs(text):
            if ident in valid.get(kind, ()):
                resolved += 1
            else:
                phantom[(kind, ident)] = 1
        if resolved == 0 and not phantom:
            continue
        store.add_node("content", rel, subtype="markdown", path=rel, label=p.name,
                       attrs={"resolved_refs": resolved, "phantom_refs": len(phantom)})
        for (kind, ident) in sorted(phantom):
            store.add_edge(node_id("content", rel), node_id(kind, ident), "ref",
                           src_path=rel, attrs={"kind": kind, "id": ident})
