#!/usr/bin/env python3
"""
scripts/generate/context_map.py — emit governance/context-map.yaml.

WHAT THIS IS. A machine-readable orientation index: where everything is, what it
is, who writes it, who reads it, and whether it is canonical or derived. It exists
so a fresh session can answer "what is this and can I trust it?" from one query
instead of by grepping a tree that hides six directories from ripgrep.

WHY IT IS GENERATED AND NOT WRITTEN. This repository's signature defect is a
document that is readable and wrong: a comment asserting a protection that was
retired, a register whose stated reasons did not survive their first audit, a
count in prose that the database contradicts. A hand-maintained context map would
join that set within a month. So every volatile field here is DERIVED at generation
time -- row counts from the live DB, check levels from the registry, writers from
the source. Nothing volatile is typed by hand.

  CLAUDE.md is the human map and says of itself "a derived map, not a source of
  truth". This is the machine map, and the same disclaimer applies with more force:
  regenerate it, do not edit it.

DETERMINISM IS THE CONTRACT. Output is a pure function of (git HEAD, the DB, the
filesystem). No wall-clock time is recorded -- the provenance line carries the
commit sha and a DB fingerprint instead, following the precedent set by
scripts/generate_parts.py. Re-running against an unchanged repo yields a
byte-identical file, which is what makes --check meaningful.

USAGE
  python3 scripts/generate/context_map.py              # write governance/context-map.yaml
  python3 scripts/generate/context_map.py --check      # exit 1 if the committed file is stale
  python3 scripts/generate/context_map.py --stdout     # print, write nothing

Exit codes: 0 ok; 1 --check found staleness; 2 config error.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
OUT = REPO / "governance" / "context-map.yaml"

# --- the one hand-maintained table, kept deliberately small ------------------
# Only STABLE facts belong here: what a directory is FOR, and its authority class.
# Anything countable is derived below. Adding a volatile field here is the failure
# mode this generator exists to prevent.
DIRECTORY_ROLES = {
    "governance":    ("doctrine, protocols, the check registry", "canonical"),
    "decisions":     ("decision records -- the governance changelog", "canonical"),
    "schemas":       ("Pydantic models mirroring the SQLite layout", "canonical"),
    "scripts":       ("tooling: migrations, audits, validators, generators", "canonical"),
    "data":          ("the SQLite database and entity YAML stores", "canonical"),
    "references":    ("working corpus: BPCs, reasoning docs, registers", "canonical"),
    "attestations":  ("per-artifact adherence logs", "canonical"),
    "architecture":  ("architecture specifications", "canonical"),
    "skills":        ("project-domain authoring protocols (not harness skills)", "canonical"),
    "workplan":      ("dated plans; several coexist -- read the newest", "canonical"),
    "sessions":      ("per-session records and the continuity pointers", "frozen-record"),
    "audits":        ("dated audit reports", "frozen-record"),
    "parts":         ("the guidebook as chaptered markdown", "generated"),
    "site":          ("the generated static site", "generated"),
    "specs":         ("hand-authored spec briefs (reference since the 2026-08-06 reset)", "reference"),
    "_archived":     ("retired-but-preserved content, mirroring origin paths", "frozen-record"),
    "versions":      ("version snapshots", "frozen-record"),
    "tools":         ("surface regenerators", "canonical"),
    ".github":       ("CI workflows and CODEOWNERS", "canonical"),
}

# Directories hidden from ripgrep by the root .ignore (DR-2026-08-06-cold-storage-search-scope).
# Derived from the file itself so this cannot drift.
def ignored_dirs():
    p = REPO / ".ignore"
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!"):
            out.append(line)
    return sorted(out)


def sh(*args):
    try:
        return subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        return ""


def db_facts():
    """Row counts, schema version, and a deterministic fingerprint."""
    if not DB_PATH.exists():
        return None
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    c = con.cursor()
    uv = c.execute("PRAGMA user_version").fetchone()[0]
    names = [r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    views = [r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")]
    counts, fks = {}, {}
    for t in names:
        counts[t] = c.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        edges = []
        for r in c.execute(f'PRAGMA foreign_key_list("{t}")'):
            edges.append({"column": r[3], "references": f"{r[2]}.{r[4] or 'rowid'}"})
        if edges:
            fks[t] = sorted(edges, key=lambda e: e["column"])
    fp = hashlib.sha256(
        json.dumps({"uv": uv, "counts": counts}, sort_keys=True).encode()
    ).hexdigest()[:12]
    con.close()
    return {"schema_version": uv, "tables": counts, "views": views,
            "foreign_keys": fks, "fingerprint": fp}


# FILL_RE matches only statements that can PUT ROWS IN a table. UPDATE and
# DELETE are deliberately excluded: a table that appears only in the clean-room
# reset's DELETE statements is not "written" in any sense that matters, and
# counting it as written hid the one table nothing can fill. The distinction is
# the whole value of the tables_with_no_writer_at_all field.
FILL_RE = re.compile(r'\b(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|REPLACE\s+INTO)\s+["\']?(\w+)', re.I)
# MUTATE_RE is the wider set, used only to describe direct-writer scripts.
MUTATE_RE = re.compile(
    r'\b(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM|REPLACE\s+INTO)\s+["\']?(\w+)',
    re.I)


def script_facts(table_names):
    """Which code writes which tables, split by MECHANISM.

    The split is the point. A table written only by `scripts/migrations/*.sql` is on
    the sanctioned path; a table written by a `.py` under `scripts/` or `tools/` is a
    direct writer, which CLAUDE.md §0 rule 4 forbids; a table nothing writes is either
    dead or waiting on unwritten code, and those two look identical in a schema dump.
    An earlier draft scanned Python only and therefore reported 38 tables as having no
    writer when most are migration-written — a readable-and-wrong field of exactly the
    kind this generator exists to avoid.
    """
    want = set(table_names)
    py, sql = {}, {}
    for root in ("scripts", "tools"):
        base = REPO / root
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            try:
                src = p.read_text(errors="ignore")
            except Exception:
                continue
            hits = {m.group(1) for m in MUTATE_RE.finditer(src)} & want
            if hits:
                py[str(p.relative_to(REPO))] = sorted(hits)
    mig = REPO / "scripts" / "migrations"
    if mig.exists():
        for p in sorted(mig.glob("*.sql")):
            try:
                src = p.read_text(errors="ignore")
            except Exception:
                continue
            hits = {m.group(1) for m in FILL_RE.finditer(src)} & want
            for t in sorted(hits):
                sql.setdefault(t, []).append(p.name)
    # sort keys: `hits` is a set, so insertion order varies per run and would
    # otherwise leak non-determinism into the emitted dict, breaking --check.
    return py, {t: sorted(sql[t]) for t in sorted(sql)}


def registry_facts():
    try:
        import yaml
    except ImportError:
        return None
    p = REPO / "governance" / "check-registry.yaml"
    if not p.exists():
        return None
    d = yaml.safe_load(p.read_text())
    checks = []
    for ch in d.get("checks", []):
        checks.append({
            "id": ch.get("id"),
            "level": ch.get("level"),
            "battery": ch.get("battery"),
            "kinds": ch.get("kinds"),
            "min_items": ch.get("min_items"),
            "cmd": " ".join(ch.get("cmd", [])),
        })
    return {
        "checks": sorted(checks, key=lambda c: (c["level"] or "", c["id"] or "")),
        "quarantined": sorted(q.get("id") for q in d.get("quarantine", [])),
        "batteries": sorted(d.get("batteries", {})),
        "kinds": sorted(d.get("kinds", [])),
    }


def pointer_facts():
    def read(p):
        f = REPO / p
        return f.read_text().strip() if f.exists() else None

    latest = read("sessions/LATEST")
    latest_research = read("sessions/LATEST-RESEARCH")
    doctrine_sha = sh("git", "rev-parse", "HEAD:governance/mission-and-epistemics.md")[:7]
    return {
        "sessions_latest": latest,
        "sessions_latest_resolves": bool(latest and (REPO / "sessions" / latest).exists()),
        "sessions_latest_research": latest_research,
        "sessions_latest_research_resolves": bool(
            latest_research and (REPO / "sessions" / latest_research).exists()),
        "doctrine_sha": doctrine_sha,
        "doctrine_file": "governance/mission-and-epistemics.md",
        "newest_workplan": sorted(
            (p.name for p in (REPO / "workplan").glob("2*.md")), reverse=True)[:1],
        "live_project_instructions": sorted(
            (p.name for p in (REPO / "governance").glob("project-instructions-v*.md")))[-1:],
    }


def build():
    db = db_facts()
    reg = registry_facts()
    tables = list(db["tables"]) if db else []
    py_writers, sql_writers = script_facts(tables)
    direct = {t for ts in py_writers.values() for t in ts}
    migrated = set(sql_writers)

    doc = {
        "_README": (
            "GENERATED by scripts/generate/context_map.py. Do not edit -- regenerate. "
            "Every volatile field here is derived from the live repo at generation time. "
            "A stale entry is a bug in the generator or an unregenerated commit, "
            "never something to patch by hand."
        ),
        # NO HEAD SHA HERE, DELIBERATELY. An earlier draft recorded `git rev-parse HEAD`.
        # That is self-defeating: committing the map changes HEAD, so a fresh generation
        # would differ from the committed file on every commit forever, and --check would
        # be permanently red for a reason no diff could fix. Provenance is established by
        # the DB fingerprint (content-derived) plus --check itself, which compares the
        # whole document against a fresh generation. A recorded sha would add nothing
        # that comparison does not already prove.
        "provenance": {
            "db_fingerprint": db["fingerprint"] if db else None,
            "generator": "scripts/generate/context_map.py",
            "freshness": "established by `context_map.py --check`, not by a recorded sha",
        },
        "authority": {
            "canonical_data_store": "data/guidebook.db",
            "schema_version_marker": "PRAGMA user_version",
            "schema_version": db["schema_version"] if db else None,
            "write_path": "migrations only (scripts/emit_data_migration.py -> scripts/migrate_db.py)",
            "note": (
                "Outer layers win unless an inner layer names an explicit override; "
                "code-enforced checks trump text rules for the matching invariant. "
                "When two stores disagree the DB is canonical."
            ),
        },
        "search_visibility": {
            "hidden_from_ripgrep": ignored_dirs(),
            "note": (
                "The root .ignore hides these from ripgrep/Grep by design "
                "(DR-2026-08-06-cold-storage-search-scope). 'No matches' does NOT mean "
                "absent -- confirm with ls or Glob. git grep and grep -r do NOT honour it. "
                "Nothing is hidden from code: every Python tool here walks with glob/pathlib."
            ),
        },
        "directories": {
            name: {"role": role, "authority": auth,
                   "hidden_from_ripgrep": any(name == d.strip("/") for d in ignored_dirs())}
            for name, (role, auth) in sorted(DIRECTORY_ROLES.items())
            if (REPO / name).exists()
        },
        "pointers": pointer_facts(),
        "database": {
            "tables": db["tables"] if db else {},
            "views": db["views"] if db else [],
            "foreign_keys": db["foreign_keys"] if db else {},
            "empty_tables": sorted(t for t, n in (db["tables"] if db else {}).items() if n == 0),
            # Split by mechanism -- see script_facts(). "no writer at all" is the
            # interesting set: a table nothing can fill.
            "tables_written_by_migration_only": sorted(migrated - direct),
            "tables_written_directly_by_code": sorted(direct),
            "tables_with_no_writer_at_all": sorted(set(tables) - direct - migrated),
        },
        "writers": {
            "_note": (
                "direct_python writers write the canonical DB outside the migration path, "
                "which CLAUDE.md §0 rule 4 forbids; they are listed so the divergence "
                "between the rule and the practice is visible rather than asserted."
            ),
            "direct_python": py_writers,
            "by_migration": sql_writers,
        },
        "checks": reg,
    }
    return doc


def dump(doc):
    try:
        import yaml
    except ImportError:
        sys.exit("ERROR: PyYAML required. pip install -r requirements.txt")
    return yaml.safe_dump(doc, sort_keys=False, width=100, allow_unicode=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed map differs from a fresh generation")
    ap.add_argument("--stdout", action="store_true", help="print, write nothing")
    args = ap.parse_args()

    text = dump(build())

    if args.stdout:
        print(text)
        return 0
    if args.check:
        if not OUT.exists():
            print(f"FAIL: {OUT.relative_to(REPO)} does not exist. Run without --check.",
                  file=sys.stderr)
            return 1
        if OUT.read_text() != text:
            print(f"STALE: {OUT.relative_to(REPO)} differs from a fresh generation.\n"
                  f"Run: python3 scripts/generate/context_map.py", file=sys.stderr)
            return 1
        n = len(text.splitlines())
        print(f"EXAMINED: 1 context map ({n} lines) — fresh against HEAD and the live DB")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text)
    print(f"Wrote {OUT.relative_to(REPO)} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
