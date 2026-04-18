#!/usr/bin/env python3
"""Check all .yaml/.yml files in repo parse."""
import sys, yaml, glob

errors = []
files = [p for f in ["**/*.yaml", "**/*.yml"] for p in glob.glob(f, recursive=True)
         if "/.git/" not in p]
for path in files:
    try:
        with open(path, encoding="utf-8") as f:
            yaml.safe_load(f)
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

if errors:
    sys.exit(1)
else:
    print(f"All .yaml/.yml files parse ({len(files)} checked)")
