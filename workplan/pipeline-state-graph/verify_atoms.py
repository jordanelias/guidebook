#!/usr/bin/env python3
"""Check that every atom's `quote` occurs verbatim in its `source` file.

usage: verify_atoms.py atoms.jsonl [--repo /home/user/guidebook]
Whitespace is collapsed and a leading blockquote marker ('> ') on each source line is ignored.
Prints one line per failure and a summary. Exit 1 if any failure. It checks the QUOTE only --
whether the atom's `claim` is a fair reading of the quote is a judgment this script cannot make.
"""
import json, re, sys
from pathlib import Path

repo = Path("/home/user/guidebook")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--repo" in sys.argv:
    repo = Path(sys.argv[sys.argv.index("--repo") + 1]); args = [a for a in args if a != str(repo)]
REQ = {"id", "source", "quote", "modality", "subject", "claim", "scope", "speaker", "status"}
MOD = {"MUST", "MUST_NOT", "MAY", "DEFINES", "CARDINALITY", "ORDER", "EQUATES", "RESERVES", "OPEN"}
SPK = {"OWNER_QUOTED", "OWNER_RELAYED", "RATIFIED_DOC", "AGENT_PROPOSAL", "PROCESS_RULE"}
STA = {"ACTIVE", "SUPERSEDED", "AMENDED", "PROPOSED", "OPEN", "HISTORICAL"}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
cache = {}
def text(path):
    if path not in cache:
        raw = (repo / path).read_text(encoding="utf-8", errors="replace")
        cache[path] = norm("\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in raw.split("\n")))
    return cache[path]
bad = n = 0
ids = set()
for ln, line in enumerate(open(args[0], encoding="utf-8"), 1):
    if not line.strip():
        continue
    n += 1
    try:
        a = json.loads(line)
    except Exception as e:
        print(f"line {ln}: not JSON ({e})"); bad += 1; continue
    miss = REQ - set(a)
    if miss: print(f"{a.get('id', ln)}: missing keys {sorted(miss)}"); bad += 1; continue
    if a["id"] in ids: print(f"{a['id']}: duplicate id"); bad += 1
    ids.add(a["id"])
    if a["modality"] not in MOD: print(f"{a['id']}: bad modality {a['modality']}"); bad += 1
    if a["speaker"] not in SPK: print(f"{a['id']}: bad speaker {a['speaker']}"); bad += 1
    if a["status"] not in STA: print(f"{a['id']}: bad status {a['status']}"); bad += 1
    path = a["source"].split(":")[0]
    try:
        t = text(path)
    except Exception as e:
        print(f"{a['id']}: cannot read {path}: {e}"); bad += 1; continue
    if norm(re.sub(r"^\s*>\s?", "", a["quote"])) not in t:
        print(f"{a['id']}: QUOTE NOT FOUND in {path}: {a['quote'][:90]!r}"); bad += 1
print(f"{n} atoms checked, {bad} problem(s)")
sys.exit(1 if bad else 0)
