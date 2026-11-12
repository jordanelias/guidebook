#!/usr/bin/env python3
"""Collect the owner's prose: verbatim, with a keyword-tagged index. Reads only.
    python3 -I scratchpad/<STEM>/build_owner_prose.py
Topic tags are KEYWORD HEURISTICS (counts of stems in the section) — an aid to finding, never a
classification of record. Selection of sections = heading names an owner act.
"""
import re, subprocess, datetime
from pathlib import Path

ROOT = Path("/home/user/guidebook")
OUT = ROOT / "scratchpad/session_2026-11-12-pipeline-bidirectional-audit/dossier"
sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
STAMP = f"_Generated {now} at commit {sha} by build_owner_prose.py; verbatim text is copied, never paraphrased._\n"

TOPICS = {
    "language/multilingual": r"language|multilingual|translat|English|native|non-English|alias|P1|P2|P3|vernacular",
    "jurisdiction": r"jurisdiction|national|regulat|\bUK\b|Canada|code value|standard\b|country|international",
    "direction/re-entrancy": r"re-entr|backward|bidirection|direction|forward|walk|any stage|start (?:at|from)|re-run|rerun",
    "evidence/tier": r"tier|T1|Co-1|Co-2|evidence|marker|●|◐|○|verified|retriev",
    "judgment/adjudication": r"adjudicat|judg|extraction|term|observed|parameter",
    "synthesis/convergence": r"synthes|convergen|independen|genealog|root|weighted|conflict",
    "specification/determination": r"determination|specification|computed|derived|state\b|stated|provisional",
    "render/presentation": r"render|page|surface|present|transparen|reader|interface|display|book",
    "lens/taxonomy": r"lens|ICF|identity|medical|access.need|population|taxonom|ICD",
    "code-minimalism/governance": r"minimi|code\b|delete|check|gate|enforce|owner-gated|net-negative",
    "mission/ethos": r"mission|ethos|advocacy|thinking tool|CRPD|disabled people|lived experience|co-?produc|authority",
}

src = (ROOT / "references/project-standards.md").read_text()
lines = src.split("\n")
starts = [i for i, l in enumerate(lines) if l.startswith("## ")] + [len(lines)]
secs = []
for a, b in zip(starts, starts[1:]):
    secs.append((a + 1, b, lines[a][3:], "\n".join(lines[a:b])))

OWNERISH = re.compile(r"owner|RULING|RULE |ruling|statement|instruction|delegation|clarification|SUPERSESSION|Recording|doctrine|five layers|Layer 0|lens|CHECK is", re.I)
sel = [s for s in secs if re.search(r"Owner|OWNER|RULING|RULE |ruling|SUPERSESSION|Recording|Core Doctrine|five layers|lens CHECK|parameter registry is BASE|statement|instruction|delegation|clarification", s[2])]

idx = [f"# 40 — Owner prose index (`references/project-standards.md`)\n\n{STAMP}\n",
       f"{len(sel)} of {len(secs)} `##` sections of `references/project-standards.md` record an owner act or the locked doctrine; "
       f"their full text is in `41-owner-rulings-verbatim.md`. Line numbers are in `references/project-standards.md` at the commit above.\n",
       "Tags = top keyword families by hit-count in the section (heuristic).\n",
       "| # | lines | heading | bytes | tags |", "|---|---|---|---|---|"]
verb = [f"# 41 — Owner rulings, verbatim\n\n{STAMP}\n"]
for n, (a, b, h, body) in enumerate(sel, 1):
    sc = {t: len(re.findall(p, body, re.I)) for t, p in TOPICS.items()}
    tags = ", ".join(t for t, c in sorted(sc.items(), key=lambda kv: -kv[1])[:3] if c >= 3) or "—"
    idx.append(f"| O{n:02d} | {a}-{b} | {h.replace('|', '/')[:150]} | {len(body)} | {tags} |")
    verb.append(f"\n\n<!-- O{n:02d} references/project-standards.md:{a}-{b} -->\n\n" + body)
(OUT / "40-owner-prose-index.md").write_text("\n".join(idx) + "\n")
(OUT / "41-owner-rulings-verbatim.md").write_text("\n".join(verb))

# 42 doctrine documents, verbatim
docs = ["governance/mission-and-epistemics.md", "governance/jurisdiction-philosophy.md", "governance/audience-priority.md",
        "governance/mission-PROVISIONAL.md", "references/owner-notes/2026-08-27-architecture-note.md"]
d = [f"# 42 — Doctrine, mission and ethos documents (verbatim)\n\n{STAMP}\n",
     "Authorship note: these are the repository's mission documents. `mission-PROVISIONAL.md` is provisional by its own name; whether a given sentence is the owner's own words or an assistant's drafting is stated (or not) inside each file — the audit must not assume.\n"]
for p in docs:
    f = ROOT / p
    if f.exists():
        d.append(f"\n\n---\n\n<!-- BEGIN {p} -->\n\n" + f.read_text() + f"\n\n<!-- END {p} -->\n")
(OUT / "42-doctrine-verbatim.md").write_text("\n".join(d))

# 43 other prose homes of owner statements: where they are, counted — not copied
g = subprocess.run("grep -rIlE 'owner (said|ruled|ruling|statement|instruction|directive|clarif)|OWNER:|Owner ruling' sessions decisions governance architecture workplan references --include=*.md --include=*.yaml 2>/dev/null | sort",
                   shell=True, capture_output=True, text=True, cwd=ROOT).stdout.split()
byt = {}
for p in g:
    byt.setdefault(p.split("/")[0], []).append(p)
o = [f"# 43 — Other files that record owner acts (located, not copied)\n\n{STAMP}\n",
     "`.ignore` hides `sessions/`, `_archived/`, `audits/`, `versions/` from ripgrep and the Grep tool — use `grep -r` / `git grep` (CLAUDE.md §7).\n",
     "Counts by top directory: " + ", ".join(f"`{k}` {len(v)}" for k, v in sorted(byt.items())) + "\n",
     "Decisions (`decisions/DR-*`) that mention owner acts, and the operative instrument's section headings:\n"]
dr = ROOT / "decisions/DR-2026-08-19-research-restart-operative-instrument.md"
o.append("\n```\n" + "\n".join(l for l in dr.read_text().split("\n") if l.startswith("#"))[:6000] + "\n```\n")
o.append("\n## Files\n\n" + "\n".join(f"- `{p}`" for p in g))
(OUT / "43-owner-acts-elsewhere.md").write_text("\n".join(o))
print(len(sel), "owner sections;", sum(len(x) for x in verb), "bytes verbatim;", len(g), "files elsewhere")
