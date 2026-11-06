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

WHAT IT CHECKS. Every BACKTICKED token in a skill, command or agent file that is SHAPED like a
vocabulary value or an identifier (contains `_` or `-`, or is all capitals) must resolve to one
of the homes the repository holds, and to nothing else: a table, view, column, `table.column` or
CHECK vocabulary value (dbcore.check_values over every column) or a view's CASE literal; a
`db.py` verb (from `--help`) or flag (from the parser source); a registered check id; a
pipeline-contract stage or criterion id; an R-rule label (governance/research-contract.yaml); a
skill, command or agent stem; a tracked path or basename; an identity, ICF, access-need, slug,
term or gap id live in its registry; `sqlite_master` / `sqlite_sequence`; a placeholder (a token
carrying NNN/XXX/YYYY/<>); or a token the file defines in its own table. Everything else is
UNRESOLVED and printed with its file. Bare ALL-CAPS words in prose are not examined: only a
backticked token is a value the skill tells the operator to type.

WHAT IS DELIBERATELY NOT A HOME. Strings the audit scripts, the writers or CLAUDE.md happen to
quote (their markers, dictionary keys, module-level names, environment variables), and the
registry's own keys. Harvesting them made `item_code`, `E-08`, `population_code` and `axis_code`
resolve, so the check could not go red on the retired item layer it exists to catch. The markers
the gates read out of note cells (`[UNVERIFIED-QUANT]`, `CO1-NOT-APPLICABLE`,
`NOTHING-IN-SCOPE`) are therefore reported wherever a skill backticks them. That is correct:
they are conventions the 2026-11-06 ruling on joined cells queues for typed columns, not
vocabulary.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT IT. An operator following a skill that names a
retired container or a column that does not exist writes the fact into a note cell, which no
later stage can join (the 2026-11-06 ruling on joined cells), or is refused by a writer the
skill said would accept the value. It reads the schema, `db.py --help`, the parser source and
the registries; nothing is curated here.

ADVISORY, with a per-file report: skills written before the vocabulary moved carry prior-
version tokens, and the remedy is a prose edit under rule 4, not an allow-list here. EXAMINED
is the number of tokens tested. Exit 0 when every token resolves, 1 otherwise, 2 when it
cannot run.

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
TOKEN = re.compile(r"`([^`\n]+)`")
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
    # Verbs: the subcommand list argparse prints. Flags: db.main() builds its parser inside the
    # function, so they are read from the source rather than by importing the module.
    helptext = subprocess.run([sys.executable, str(REPO / "scripts/db.py"), "--help"],
                              capture_output=True, text=True, cwd=REPO).stdout
    verbs = re.search(r"\{([^}\n]+)\}", helptext)
    out |= set(verbs.group(1).split(",")) if verbs else set()
    out |= set(re.findall(r'add_argument\("(--[a-z0-9-]+)"',
                          (REPO / "scripts/db.py").read_text(encoding="utf-8")))
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
    out |= {"sqlite_master", "sqlite_sequence"}
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
        for t in TOKEN.findall(text):
            t = t.strip()
            if not SHAPED.match(t) or len(t) < 3 or PLACEHOLDER.search(t):
                continue
            if t.startswith("--") or "/" in t:
                continue
            if not (t.isupper() or "_" in t or "-" in t):
                continue
            toks.add(t)
        for t in sorted(toks):
            examined += 1
            if t in known or t in own:
                continue
            unresolved.setdefault(str(f.relative_to(REPO) if f.is_relative_to(REPO) else f), []).append(t)
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
