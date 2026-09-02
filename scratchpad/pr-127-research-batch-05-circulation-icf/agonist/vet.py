#!/usr/bin/env python3
"""Retrieve Crossref metadata via the project logger and print the fields we store."""
import sys, json
sys.path.insert(0, "scripts/research")
from retrieval_log import fetch
S = "session_2026-09-02-research-batch-05-circulation-icf"

def show(doi):
    p = fetch(f"https://api.crossref.org/works/{doi}", session=S,
              purpose=f"crossref metadata for {doi}")
    print(f"\n=== {doi}")
    if not p or p.get("status") != "ok":
        print("  NO PAYLOAD / not ok:", (str(p)[:200] if p else "None")); return
    m = p["message"]
    au = m.get("author") or []
    names = [f"{a.get('family','')}, {a.get('given','')}".strip(", ") if a.get('family') else a.get('name','?') for a in au]
    print("  title    :", (m.get("title") or ["?"])[0])
    print("  authors  :", " | ".join(names), f"  (n={len(names)})")
    print("  container:", (m.get("container-title") or ["?"])[0])
    print("  year     :", ((m.get("issued") or {}).get("date-parts") or [[None]])[0])
    print("  vol/iss/pg:", m.get("volume"), "/", m.get("issue"), "/", m.get("page"), "| art-no:", m.get("article-number"))
    print("  type     :", m.get("type"), "| publisher:", m.get("publisher"))
    print("  ISSN     :", m.get("ISSN"), "| ISBN:", m.get("ISBN"))
    print("  licence  :", [l.get("URL") for l in (m.get("license") or [])][:2])

for d in sys.argv[1:]:
    show(d)
