#!/usr/bin/env python3
"""
scripts/audit/skill_vocabulary_audit.py — every value a skill names must have a home.

WHY THIS EXISTS (CLAUDE.md rule 8; owner 2026-11-06: "ensure all terminologies and
vocabularies are correct"). A skill is a prose caller: it tells an operator which words to
type into a writer. Two walk-throughs of skills/run-pipeline_SKILL.md (2026-11-06) found the
conflict mapper naming a column that no table has (`mode_s_trigger`) and population codes
the identity lens does not hold (`VIS`, `DBL`, `OFS`), and the connection skill naming
verdicts (`SUBSUMES`, `CONFLATED_VARIABLE`) with no typed home. An operator who follows
such a sentence writes prose into a free-text cell, or is refused by a writer the skill
said would accept the value -- either way the page downstream cannot join what was typed.

WHAT IT CHECKS. Every backticked token and every ALL-CAPS hyphenated token in a skill,
command or agent file that is SHAPED like a vocabulary value or an identifier (contains
`_` or `-`, or is all capitals) must resolve to one of the homes the repository holds:
a CHECK vocabulary value (dbcore.check_values over every column), a table, view or column
name, a `db.py` verb or flag, a registered check id, a pipeline-contract criterion id, a
file the tree holds, an R-rule label (R1..R99, from governance/research-contract.yaml), an
identity, ICF, access-need, slug or term id live in its registry, or a placeholder (a token
carrying NNN/XXX/YYYY/MM/DD). Everything else is UNRESOLVED and printed with its file.

ADVISORY, with a per-file report: skills written before the vocabulary moved carry prior-
version tokens, and the remedy is a prose edit under rule 4, not a curated allow-list here.
EXAMINED is the number of tokens tested. Exit 0 when every token resolves, 1 otherwise,
2 when it cannot run.

Usage: python3 scripts/audit/skill_vocabulary_audit.py [--paths skills .claude/commands ...]
"""
import argparse
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
sys.path.insert(0, str(REPO / "scripts"))
import dbcore  # noqa: E402

DEFAULT_PATHS = ("skills", ".claude/commands", ".claude/agents")
PLACEHOLDER = re.compile(r"NNN|XXX|YYYY|<|>|\.\.\.|-ID$")
TOKEN = re.compile(r"`([^`\n]+)`|\b([A-Z][A-Z0-9]{2,}(?:[-_][A-Z0-9]+)+)\b")
SHAPED = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")


def homes(conn):
    out = set()
    for (t,) in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')"):
        out.add(t)
        for c in conn.execute(f'PRAGMA table_info("{t}")'):
            out.add(c[1])
            out.add(f"{t}.{c[1]}")
            out |= dbcore.check_values(conn, t, c[1])
    # A view's own CASE literals are a derived vocabulary (v_scan_ledger's statuses).
    for (sql,) in conn.execute("SELECT sql FROM sqlite_master WHERE type='view' AND sql IS NOT NULL"):
        out |= set(re.findall(r"THEN\s+'([^']+)'", sql))
    for sql, col in (("SELECT identity_code FROM base_taxonomy_identity", 0),
                     ("SELECT icf_code FROM base_icf", 0),
                     ("SELECT need_code FROM access_needs", 0),
                     ("SELECT slug FROM slugs", 0),
                     ("SELECT term_id FROM terms", 0),
                     ("SELECT gap_id FROM gaps", 0)):
        try:
            out |= {r[col] for r in conn.execute(sql)}
        except sqlite3.Error:
            pass
    helptext = subprocess.run([sys.executable, str(REPO / "scripts/db.py"), "--help"],
                              capture_output=True, text=True, cwd=REPO).stdout
    out |= set(re.findall(r"\b([a-z]+(?:-[a-z]+)+)\b", helptext))
    # Every flag of every verb: db.main() builds its parser inside the function, so the flags
    # are harvested from the source rather than by importing the module.
    try:
        src = (REPO / "scripts/db.py").read_text(encoding="utf-8")
        out |= {m for m in re.findall(r'add_argument\("(--[a-z0-9-]+)"', src)}
    except OSError:
        pass
    import yaml  # noqa: E402
    reg = yaml.safe_load((REPO / "governance/check-registry.yaml").read_text(encoding="utf-8"))
    out |= {c["id"] for c in reg.get("checks", []) if isinstance(c, dict) and "id" in c}
    contract = yaml.safe_load((REPO / "governance/pipeline-contract.yaml").read_text(encoding="utf-8"))
    for stage in contract.get("stages", []):
        out.add(stage.get("id"))
        out |= {c.get("id") for c in stage.get("criteria", [])}
    out |= {c.get("id") for c in contract.get("cross_stage", [])}
    rc = (REPO / "governance/research-contract.yaml").read_text(encoding="utf-8")
    out |= set(re.findall(r"^\s*-\s*id:\s*(R\d+[a-z-]*)", rc, re.M))
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=REPO).stdout.split()
    out |= set(tracked) | {p.rsplit("/", 1)[-1] for p in tracked}
    # A skill, command or agent is named by its stem (`citation-miner`, `/orient`, `antagonist`).
    for p in tracked:
        if p.startswith("skills/") and p.endswith("_SKILL.md"):
            out.add(p.rsplit("/", 1)[-1][:-len("_SKILL.md")])
        if p.startswith((".claude/commands/", ".claude/agents/")) and p.endswith(".md"):
            out.add(p.rsplit("/", 1)[-1][:-3])
    # The markers the gates and writers READ out of note cells and output lines
    # (`CO1-NOT-APPLICABLE`, `[UNVERIFIED-QUANT]`, `NOTHING-IN-SCOPE`): derived from the code
    # that reads them, never listed here, so a marker the code stops reading stops resolving.
    for p in tracked:
        if p.startswith(("scripts/audit/", "scripts/research/", "scripts/assess/")) and p.endswith(".py") \
                or p in ("scripts/db.py", "scripts/dbcore.py", "scripts/run_checks.py"):
            try:
                src = (REPO / p).read_text(encoding="utf-8")
            except OSError:
                continue
            # ALL-CAPS markers anywhere in the gate's source (printed states, note markers),
            # the snake_case keys and flags it quotes, and its module-level names as
            # `<module>.NAME` (a skill may point at `retrieval_log.PAYLOAD_FIELDS`).
            out |= set(re.findall(r"\b([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b", src))
            out |= set(re.findall(r"['\"]([a-z][a-z0-9_]+)['\"]", src))
            stem = p.rsplit("/", 1)[-1][:-3]
            for name in re.findall(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=", src, re.M):
                out.add(name)
                out.add(f"{stem}.{name}")
            out |= set(re.findall(r"environ(?:\.get)?\(\s*['\"]([A-Z_]+)['\"]", src))
    # Registry entry keys (`min_items`, `no_floor`) and SQLite's own schema tables.
    for c in reg.get("checks", []):
        if isinstance(c, dict):
            out |= set(c)
    out |= {"sqlite_master", "sqlite_sequence"}
    # CLAUDE.md is Layer 0: a token it names in backticks (a harness tool, a reserved object
    # name such as best_practice_synthesis) is sanctioned vocabulary for every skill.
    try:
        out |= {t.strip() for t in re.findall(r"`([^`\n]+)`", (REPO / "CLAUDE.md").read_text(encoding="utf-8"))}
    except OSError:
        pass
    # Per-slug labels and staged ids are homes too.
    for sql in ("SELECT local_ref_id FROM source_slug_links", "SELECT ref_id FROM source_locators",
                "SELECT local_ref_id FROM citation_mining"):
        try:
            out |= {r[0] for r in conn.execute(sql)}
        except sqlite3.Error:
            pass
    return {x for x in out if x}


def defined_in(text):
    """Tokens a file defines itself: the first cell of a markdown table row (| `mode` |),
    which is how a skill states its own modes, verdicts and statuses. A token so defined is
    the file's own vocabulary, reported only when it is also claimed to be stored."""
    return {m.strip("`").strip() for m in re.findall(r"^\|\s*(`[^`|]+`|[A-Z][A-Z0-9_-]+)\s*\|", text, re.M)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--paths", nargs="*", default=list(DEFAULT_PATHS))
    args = ap.parse_args()
    if not DB_PATH.exists():
        print(f"skill_vocabulary_audit: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        known = homes(conn)
    finally:
        conn.close()
    files = []
    for p in args.paths:
        root = REPO / p
        files += sorted(f for f in root.rglob("*.md") if f.is_file() and not f.is_symlink())
    examined, unresolved = 0, {}
    texts = {f: re.sub(r"```.*?```", "", f.read_text(encoding="utf-8", errors="replace"), flags=re.S)
             for f in files}                                     # fenced commands are shown, not named
    # A vocabulary one skill defines in its own table (a mode, a status) is nameable by another.
    own = set().union(*(defined_in(t) for t in texts.values())) if texts else set()
    for f in files:
        text = texts[f]
        toks = set()
        for a, b in TOKEN.findall(text):
            t = (a or b).strip()
            if not SHAPED.match(t) or len(t) < 3 or PLACEHOLDER.search(t):
                continue
            if t.startswith("--") or "/" in t:
                continue
            if not (t.isupper() or "_" in t or "-" in t):
                continue
            toks.add(t)
        for t in sorted(toks):
            examined += 1
            if t in known or t.rstrip("s") in known or t in own:
                continue
            unresolved.setdefault(str(f.relative_to(REPO)), []).append(t)
    print("skill_vocabulary_audit — every value a skill, command or agent names resolves to a home")
    print(f"EXAMINED: {examined} token(s) across {len(files)} file(s)")
    if not unresolved:
        print("PASS: every token resolves to a CHECK value, a schema name, a verb, a flag, a check, a "
              "contract criterion, a rule label, a registry row or a file")
        return 0
    for path, toks in unresolved.items():
        print(f"  {path}: {', '.join(toks)}")
    n = sum(len(v) for v in unresolved.values())
    print(f"FAIL: {n} token(s) in {len(unresolved)} file(s) name a value, column or code the repository "
          f"holds nowhere. Correct the sentence (rule 4: prose is a caller), or give the value a typed "
          f"home first.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
