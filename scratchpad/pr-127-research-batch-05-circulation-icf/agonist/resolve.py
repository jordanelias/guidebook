#!/usr/bin/env python3
"""R10 rung 2: resolve a known reference by title via Crossref, logged."""
import sys, urllib.parse
sys.path.insert(0, "scripts/research")
from retrieval_log import fetch
S = "session_2026-09-02-research-batch-05-circulation-icf"
q = sys.argv[1]
url = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q)
p = fetch(url, session=S, purpose=f"crossref reference-resolution for: {q[:80]}")
if not p or p.get("status") != "ok":
    print("NO PAYLOAD"); sys.exit(1)
for m in p["message"]["items"]:
    au = m.get("author") or []
    names = [f"{a.get('family','')}, {a.get('given','')}".strip(", ") if a.get('family') else a.get('name','?') for a in au]
    print("DOI :", m.get("DOI"))
    print("  T :", (m.get("title") or ["?"])[0][:150])
    print("  A :", " | ".join(names)[:400], f"(n={len(names)})")
    print("  C :", (m.get("container-title") or ["?"])[0], "|", ((m.get("issued") or {}).get("date-parts") or [[None]])[0],
          "|", m.get("volume"), "/", m.get("issue"), "/", m.get("page"), "| art", m.get("article-number"))
    print("  ISSN:", m.get("ISSN"), "| type:", m.get("type"), "| pub:", m.get("publisher"))
    print()
