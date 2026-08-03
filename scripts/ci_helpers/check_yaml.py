#!/usr/bin/env python3
"""Check all .yaml/.yml files in repo parse.

Uses repo_files() rather than glob("**/*.yaml"): the glob form skipped
dot-directories, so the four LIVE workflows under .github/workflows/ were never
parsed while the five retired ones in _archived/workflows/ were. The syntax gate
checked the workflows that cannot run and skipped the ones that do.
See scripts/ci_helpers/repo_files.py.
"""
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_files import repo_files  # noqa: E402

files = repo_files(".yaml", ".yml")
errors = []
for path in files:
    try:
        with open(path, encoding="utf-8") as f:
            yaml.safe_load(f)
    except Exception as e:
        errors.append(f"FAIL: {path} — {e}")

for e in errors:
    print(e)

print(f"EXAMINED: {len(files)} .yaml/.yml file(s)")
if errors:
    sys.exit(1)
print(f"All .yaml/.yml files parse ({len(files)} checked)")
