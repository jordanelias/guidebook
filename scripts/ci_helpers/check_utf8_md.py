#!/usr/bin/env python3
"""Check all .md files in repo are valid UTF-8."""
import sys, os, glob

errors = []
for path in glob.glob("**/*.md", recursive=True):
    if "/.git/" in path or "/sessions/_archive/" in path:
        continue
    try:
        with open(path, encoding="utf-8") as f:
            f.read()
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

if errors:
    print(f"\n{len(errors)} file(s) failed UTF-8 check", file=sys.stderr)
    sys.exit(1)
else:
    print(f"All .md files are valid UTF-8 ({len(glob.glob('**/*.md', recursive=True))} checked)")
