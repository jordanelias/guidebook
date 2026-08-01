#!/usr/bin/env python3
"""Check all .json files in repo parse.

Uses repo_files() rather than glob("**/*.json"): the glob form skipped
dot-directories, so .claude/settings.json — which carries the R1-R15 research
contract and whose corruption silently disables both harness hooks — was never
parsed. See scripts/ci_helpers/repo_files.py.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_files import repo_files  # noqa: E402

files = repo_files(".json")
errors = []
for path in files:
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

print(f"EXAMINED: {len(files)} .json file(s)")
if errors:
    sys.exit(1)
print(f"All .json files parse ({len(files)} checked)")
