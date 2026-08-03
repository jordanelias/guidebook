#!/usr/bin/env python3
"""
scripts/ci_helpers/repo_files.py — one traversal for the syntax checkers.

WHY THIS EXISTS. check_json.py, check_yaml.py and check_utf8_md.py each called
`glob.glob("**/*.ext", recursive=True)`. That pattern does not match paths under
dot-directories, so all three silently skipped `.github/` and `.claude/`:

  * `.claude/settings.json` — which carries the R1-R15 research contract and whose
    corruption disables both harness hooks — was never parsed.
  * The four LIVE workflows under `.github/workflows/` were never YAML-parsed,
    while the five RETIRED ones in `_archived/workflows/` were. The syntax gate
    checked the workflows that cannot run and skipped the ones that do.

Three copies of one traversal, all wrong the same way, is the shape this repo
already knows: it is why check-registry.yaml replaced four hand-kept check lists.
Fixing the glob in three places would have left three copies to drift again.

Excludes `.git` (not ours), `__pycache__` and `node_modules` (generated). Nothing
else — in particular, dot-directories are INCLUDED, which is the entire point.
"""

import os

EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache", ".ruff_cache"}


def repo_files(*extensions, root="."):
    """Every file under `root` with one of `extensions` (e.g. ".json", ".yaml").

    Walks with os.walk rather than glob so dot-directories are traversed. Returns
    sorted paths for stable, diffable output.
    """
    wanted = tuple(extensions)
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            if name.endswith(wanted):
                path = os.path.join(dirpath, name)
                found.append(path[2:] if path.startswith("./") else path)
    return sorted(found)
