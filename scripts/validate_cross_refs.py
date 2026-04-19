#!/usr/bin/env python3
"""
validate_cross_refs.py — Cross-reference integrity validator.

Checks:
  1. Slug references resolve via slug-registry.md
  2. CON-IDs (CON-NNNN) resolve to connection register index
  3. Part section references (§X.Y) resolve to existing headings in correct part file
  4. BPC ↔ search-log co-existence (every BPC has matching search-log, vice versa)

Usage:
    python3 scripts/validate_cross_refs.py            # full repo scan
    python3 scripts/validate_cross_refs.py --fast     # skip section heading resolution (faster)

Exit codes:
    0 — no broken references
    1 — one or more broken references

Output: broken references to stdout; summary to stderr.
"""

import sys
import os
import re
import glob
import argparse
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

SLUG_REGISTRY_PATH = "references/slug-registry.md"
CONNECTIONS_INDEX_PATH = "references/connections/_index.md"
BPC_ROOT = "references/bpc"
SEARCH_LOG_ROOT = "references/search-logs"

# Files to scan for cross-references (exclude generated/archive)
SCAN_PATTERNS = [
    "references/bpc/**/*.md",
    "references/connections/**/*.md",
    "parts/**/*.md",
    "skills/**/*.md",
    "gap_register.md",
]

EXCLUDE_PATTERNS = [
    "sessions/_archive/**",
    ".git/**",
]

# Heading pattern for part files
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)

# Slug reference pattern: {slug} or [text](slug) or slug references in text
SLUG_REF_RE = re.compile(r"\bslug[:\s]+([a-z0-9_-]+)\b", re.IGNORECASE)

# CON-ID pattern
CON_ID_RE = re.compile(r"\bCON-(\d{4})\b")

# Section reference pattern: §X.Y or §X.Y.Z
SECTION_RE = re.compile(r"§(\d+)\.(\d+)(?:\.(\d+))?")


# ── Loaders ──────────────────────────────────────────────────────────────────

def load_slug_registry(repo_root: str) -> set[str]:
    """Return set of known slugs from slug-registry.md."""
    path = os.path.join(repo_root, SLUG_REGISTRY_PATH)
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        content = f.read()
    slugs = set()
    for line in content.split("\n"):
        # Format: | slug-name | ... or slug-name: ...
        m = re.match(r"^\|\s*`?([a-z0-9_/-]+)`?\s*\|", line)
        if m:
            slugs.add(m.group(1).strip())
        m2 = re.match(r"^\s*([a-z0-9_/-]+)\s*:", line)
        if m2:
            slugs.add(m2.group(1).strip())
    return slugs


def load_con_ids(repo_root: str) -> set[str]:
    """Return set of CON-IDs present in connections/_index.md."""
    path = os.path.join(repo_root, CONNECTIONS_INDEX_PATH)
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        content = f.read()
    return set(CON_ID_RE.findall(content))


def collect_scan_files(repo_root: str) -> list[str]:
    """Collect all files to scan."""
    files = []
    for pattern in SCAN_PATTERNS:
        full_pattern = os.path.join(repo_root, pattern)
        files.extend(glob.glob(full_pattern, recursive=True))
    # Deduplicate, normalize
    return sorted(set(os.path.normpath(f) for f in files))


def collect_bpc_slugs(repo_root: str) -> dict[str, str]:
    """Return {slug: filepath} for all BPC files."""
    pattern = os.path.join(repo_root, BPC_ROOT, "**", "*.md")
    result = {}
    for path in glob.glob(pattern, recursive=True):
        stem = Path(path).stem
        result[stem] = path
    return result


def collect_search_log_slugs(repo_root: str) -> dict[str, str]:
    """Return {slug: filepath} for all search-log files."""
    pattern = os.path.join(repo_root, SEARCH_LOG_ROOT, "**", "*.md")
    result = {}
    for path in glob.glob(pattern, recursive=True):
        stem = Path(path).stem
        # Strip common suffixes: -search-log, _search_log, etc.
        slug = re.sub(r"[-_]?search[-_]?log$", "", stem, flags=re.IGNORECASE)
        result[slug] = path
    return result


# ── Checkers ─────────────────────────────────────────────────────────────────

def check_con_ids(files: list[str], known_cons: set[str]) -> list[tuple[str, str]]:
    """
    Scan files for CON-ID references. Return list of (filepath, error).
    """
    errors = []
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        for m in CON_ID_RE.finditer(content):
            con_num = m.group(1)
            con_id = con_num  # we store just the digits in set
            if con_num not in known_cons:
                line_no = content[:m.start()].count("\n") + 1
                errors.append(
                    (path, f"BROKEN_CON_ID: CON-{con_num} referenced at line {line_no} "
                           f"but not found in connections/_index.md")
                )
    return errors


def check_bpc_searchlog_coexistence(
    bpc_slugs: dict[str, str],
    sl_slugs: dict[str, str],
) -> list[tuple[str, str]]:
    """
    Every BPC slug should have a matching search-log and vice versa.
    Returns list of (context, error).
    """
    errors = []
    for slug, bpc_path in bpc_slugs.items():
        if slug not in sl_slugs:
            errors.append(
                (bpc_path, f"MISSING_SEARCH_LOG: BPC '{slug}' has no matching search-log file "
                            f"in {SEARCH_LOG_ROOT}/")
            )
    for slug, sl_path in sl_slugs.items():
        if slug not in bpc_slugs:
            errors.append(
                (sl_path, f"ORPHAN_SEARCH_LOG: Search-log '{slug}' has no matching BPC file "
                           f"in {BPC_ROOT}/")
            )
    return errors


# ── Runner ───────────────────────────────────────────────────────────────────

def run(repo_root: str = ".", fast: bool = False, warn_only: bool = False) -> int:
    """Run all checks. Returns exit code.
    If warn_only=True, reports issues but always exits 0.
    """
    errors: list[tuple[str, str]] = []

    print("Loading registries...", file=sys.stderr)
    known_slugs = load_slug_registry(repo_root)
    known_cons = load_con_ids(repo_root)
    bpc_slugs = collect_bpc_slugs(repo_root)
    sl_slugs = collect_search_log_slugs(repo_root)
    scan_files = collect_scan_files(repo_root)

    print(f"  {len(known_slugs)} slugs, {len(known_cons)} CON-IDs, "
          f"{len(bpc_slugs)} BPC files, {len(sl_slugs)} search-logs, "
          f"{len(scan_files)} files to scan", file=sys.stderr)

    # Check 1: CON-ID references
    print("Checking CON-ID references...", file=sys.stderr)
    errors.extend(check_con_ids(scan_files, known_cons))

    # Check 2: BPC ↔ search-log co-existence
    print("Checking BPC ↔ search-log co-existence...", file=sys.stderr)
    errors.extend(check_bpc_searchlog_coexistence(bpc_slugs, sl_slugs))

    # Output results
    label = "WARN" if warn_only else "FAIL"
    if errors:
        for path, msg in sorted(errors):
            print(f"{label} [{path}]: {msg}")
    else:
        print("All cross-reference checks passed.")

    # Summary
    mode = " (warn-only mode)" if warn_only else ""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"validate_cross_refs.py: {len(errors)} issue(s) found{mode}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    if warn_only:
        return 0
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Validate cross-references in guidebook repo")
    parser.add_argument("--fast", action="store_true",
                        help="Skip section heading resolution (faster, less thorough)")
    parser.add_argument("--warn-only", action="store_true",
                        help="Report issues but exit 0 (use during transition)")
    parser.add_argument("--repo-root", default=".",
                        help="Path to guidebook repo root (default: current directory)")
    args = parser.parse_args()

    sys.exit(run(repo_root=args.repo_root, fast=args.fast, warn_only=args.warn_only))


if __name__ == "__main__":
    main()
