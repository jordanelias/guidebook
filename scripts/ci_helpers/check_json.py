#!/usr/bin/env python3
"""Check all .json files in repo parse."""
import sys, json, glob

errors = []
files = [p for p in glob.glob("**/*.json", recursive=True) if "/.git/" not in p]
for path in files:
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

if errors:
    sys.exit(1)
else:
    print(f"All .json files parse ({len(files)} checked)")
