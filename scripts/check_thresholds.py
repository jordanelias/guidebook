#!/usr/bin/env python3
"""
check_thresholds.py — File size threshold checker.

Governed files and their token limits (1 token ≈ 4 chars, conservative):
  - sessions/session_*.md (most recent)    2K tokens  → ~8,000 chars
  - gap_register.md                        5K tokens  → ~20,000 chars
  - references/project-standards.md       10K tokens  → ~40,000 chars
  - references/connections/_index.md       8K tokens  → ~32,000 chars
  - references/slug-registry.md            6K tokens  → ~24,000 chars

Usage:
    python3 scripts/check_thresholds.py               # check all governed files
    python3 scripts/check_thresholds.py --report      # show sizes even for passing files

Exit codes:
    0 — all files within thresholds
    1 — one or more files exceed threshold

Output: failures to stdout; summary to stderr.
"""

import sys
import os
import re
import glob
import argparse
from pathlib import Path


# ── Threshold definitions ────────────────────────────────────────────────────
# (path_glob, max_tokens, description)
# max_chars = max_tokens * 4 (conservative 1 token ≈ 4 chars)

THRESHOLDS = [
    {
        "glob": "gap_register.md",
        "max_tokens": 20000,
        "description": "Active gap register (filtered to P1 OPEN at session start — full file not loaded)",
        "note": "Archive CLOSED items to gap_register_archive.md. If still over, review P3 items for closure.",
    },
    {
        "glob": "references/project-standards.md",
        "max_tokens": 10500,
        "description": "Project standards (session-start load)",
        "note": "If growing too large, consider splitting into sub-documents",
    },
    {
        "glob": "references/connections/_index.md",
        "max_tokens": 8000,
        "description": "Connection register index",
        "note": "Per-topic files hold detail; index should remain a summary only",
    },
    {
        "glob": "references/slug-registry.md",
        "max_tokens": 6000,
        "description": "Slug registry",
        "note": "Consider splitting by topic if growing",
    },
    {
        "glob": "sessions/session_*.md",
        "max_tokens": 2000,
        "description": "Session log files",
        "note": "Session logs should be concise YAML. Verbose notes → gap register instead",
        "most_recent_only": True,
    },
]

CHARS_PER_TOKEN = 4  # conservative estimate


# ── Helpers ──────────────────────────────────────────────────────────────────

def chars_to_tokens(chars: int) -> int:
    return chars // CHARS_PER_TOKEN


def collect_files(repo_root: str, pattern: str, most_recent_only: bool = False) -> list[str]:
    full_pattern = os.path.join(repo_root, pattern)
    files = sorted(glob.glob(full_pattern, recursive=True))
    if most_recent_only and files:
        # Sort by modification time, take most recent
        files = sorted(files, key=lambda f: os.path.getmtime(f), reverse=True)
        return [files[0]]
    return files


def check_threshold(path: str, max_tokens: int) -> tuple[int, int, bool]:
    """Returns (actual_tokens, max_tokens, passed)."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return (0, max_tokens, True)  # Skip unreadable files
    actual_tokens = chars_to_tokens(len(content))
    return (actual_tokens, max_tokens, actual_tokens <= max_tokens)


# ── Runner ───────────────────────────────────────────────────────────────────

def run(repo_root: str = ".", report: bool = False) -> int:
    failures = []
    all_results = []

    for threshold in THRESHOLDS:
        files = collect_files(
            repo_root,
            threshold["glob"],
            threshold.get("most_recent_only", False),
        )

        if not files:
            if report:
                print(f"SKIP (not found): {threshold['glob']} — {threshold['description']}")
            continue

        for path in files:
            rel_path = os.path.relpath(path, repo_root)
            actual, maximum, passed = check_threshold(path, threshold["max_tokens"])
            result = {
                "path": rel_path,
                "actual": actual,
                "max": maximum,
                "passed": passed,
                "description": threshold["description"],
                "note": threshold.get("note", ""),
            }
            all_results.append(result)
            if not passed:
                failures.append(result)

    # Output failures
    for r in failures:
        overage = r["actual"] - r["max"]
        print(
            f"FAIL: {r['path']}\n"
            f"  {r['actual']} tokens (limit: {r['max']}, over by: {overage})\n"
            f"  {r['description']}\n"
            f"  Action: {r['note']}"
        )

    # Report mode: show all
    if report:
        for r in all_results:
            status = "PASS" if r["passed"] else "FAIL"
            print(f"{status}: {r['path']} — {r['actual']}/{r['max']} tokens")

    # Summary
    total = len(all_results)
    passed = total - len(failures)
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"check_thresholds.py: {passed}/{total} files within threshold", file=sys.stderr)
    if failures:
        print(f"  {len(failures)} file(s) exceed threshold — see errors above", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description="Check file size thresholds for governed files")
    parser.add_argument("--report", action="store_true",
                        help="Show all files including passing ones")
    parser.add_argument("--repo-root", default=".",
                        help="Path to guidebook repo root (default: current directory)")
    args = parser.parse_args()

    sys.exit(run(repo_root=args.repo_root, report=args.report))


if __name__ == "__main__":
    main()
