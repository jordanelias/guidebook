#!/usr/bin/env python3
"""Check all .md files in repo are valid UTF-8.

Uses repo_files() rather than glob("**/*.md") — see scripts/ci_helpers/repo_files.py
for why the glob form was blind to dot-directories.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_files import repo_files  # noqa: E402

files = [p for p in repo_files(".md") if "/sessions/_archive/" not in p]
errors = []
for path in files:
    try:
        with open(path, encoding="utf-8") as f:
            f.read()
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

print(f"EXAMINED: {len(files)} .md file(s)")
if errors:
    print(f"\n{len(errors)} file(s) failed UTF-8 check", file=sys.stderr)
    sys.exit(1)
print(f"All .md files are valid UTF-8 ({len(files)} checked)")
