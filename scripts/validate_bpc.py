#!/usr/bin/env python3
"""
validate_bpc.py — BPC file structure validator for the Accessible Built Environments Guidebook.

Usage:
    python3 scripts/validate_bpc.py <file.md>       # validate one file
    python3 scripts/validate_bpc.py --all           # validate all BPC files in references/bpc/
    python3 scripts/validate_bpc.py --changed       # validate files passed via stdin (one per line)

Exit codes:
    0 — all files pass
    1 — one or more files failed

Output: structured error messages to stdout; summary to stderr.
"""

import sys
import os
import re
import json
import argparse
import glob
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────

# CO-0006 schema mandatory sections (Block 2 migration complete 2026-04-19)
# Pre-CO-0006 schema: PICO, Search strategy, Best practice synthesis,
#   Evidence gaps, Jurisdiction coverage, Co-1 pass — these sections are
#   optional enrichment in CO-0006 files and should not be validated as mandatory.
# CO-0006 mandatory: Key sources (REF-ID table) + Metadata (slug/population/last_updated)
MANDATORY_SECTIONS = [
    "## Key sources",
    "## Metadata",
]

# Optional sections — present in fully-enriched files but not required for validation
OPTIONAL_SECTIONS = [
    "### Best-practice synthesis",
    "### Consensus findings",
    "### Divergent findings",
    "### NO-DATA / THIN",
    "### Bottom-up findings",
]

# CO-0006 REF-ID table schema: at minimum these columns must be present
CO0006_REQUIRED_COLUMNS = ["REF-ID", "Authors", "Year", "Title"]

# Legacy flat format markers — accepted during transition
LEGACY_MARKERS = [
    r"^\d+\.",          # numbered list items
    r"^-\s",            # bullet list items
    r"^\*\s",           # asterisk list items
]

METADATA_REQUIRED_KEYS = ["slug", "population", "last_updated"]


# ── Validators ───────────────────────────────────────────────────────────────

def validate_file(path: str) -> list[str]:
    """
    Validate a single BPC file.
    Returns a list of error strings. Empty list = pass.
    """
    errors = []

    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"READ_ERROR: Cannot read file: {e}"]

    lines = content.split("\n")

    # Redirect/merge stubs: exempt from mandatory section checks
    # Identifiers: **Status:** MERGED or status: MERGED in Metadata
    if re.search(r"\*\*Status:\*\*\s*MERGED|status:\s*MERGED", content, re.IGNORECASE):
        return []  # Redirect stubs pass validation unconditionally

    # STUB-NOT-RUN files: Key sources section may be empty/placeholder — exempt
    is_stub_not_run = bool(re.search(r"status:\s*STUB.NOT.RUN|STATUS:\s*STUB.NOT.RUN|STUB.*NOT.RUN", content, re.IGNORECASE))

    # 1. Mandatory sections present
    for section in MANDATORY_SECTIONS:
        # Accept case-insensitive and minor heading level variants (## or ###)
        pattern = re.compile(
            r"^#{1,4}\s+" + re.escape(section.lstrip("#").strip()),
            re.IGNORECASE | re.MULTILINE,
        )
        if not pattern.search(content):
            errors.append(f"MISSING_SECTION: '{section}' not found")

    # 2. Key sources section — CO-0006 table OR legacy flat format
    key_sources_match = re.search(
        r"^#{1,4}\s+Key sources\s*$(.+?)(?=^#{1,4}\s|\Z)",
        content,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if key_sources_match:
        ks_body = key_sources_match.group(1)
        has_co0006_table = _is_co0006_table(ks_body)
        has_legacy = _is_legacy_flat(ks_body)
        is_empty = not ks_body.strip()

        if is_empty:
            errors.append("KEY_SOURCES_EMPTY: Key sources section has no content")
        elif not has_co0006_table and not has_legacy:
            errors.append(
                "KEY_SOURCES_FORMAT: Key sources section is neither a CO-0006 REF-ID table "
                "nor a recognisable legacy flat list. Content must begin with a markdown table "
                "(CO-0006 schema) or a numbered/bulleted list (legacy transition format)."
            )
        # CO-0006 table: validate required columns exist
        if has_co0006_table:
            col_errors = _validate_co0006_columns(ks_body)
            errors.extend(col_errors)

    # 3. Metadata YAML parses and contains required keys
    meta_errors = _validate_metadata(content)
    errors.extend(meta_errors)

    return errors


def _is_co0006_table(text: str) -> bool:
    """True if text contains a markdown table with a header row."""
    return bool(re.search(r"^\|.+\|.+\|", text, re.MULTILINE))


def _is_legacy_flat(text: str) -> bool:
    """True if text contains a numbered or bulleted list."""
    for pattern in LEGACY_MARKERS:
        if re.search(pattern, text, re.MULTILINE):
            return True
    return False


def _validate_co0006_columns(text: str) -> list[str]:
    """
    Check that a CO-0006 table contains the required column headers.
    Returns list of error strings.
    """
    errors = []
    # Find the header row (first table row)
    header_match = re.search(r"^\|(.+)\|", text, re.MULTILINE)
    if not header_match:
        return ["KEY_SOURCES_TABLE_MALFORMED: Cannot find table header row"]

    header = header_match.group(1)
    cols = [c.strip() for c in header.split("|")]

    for required in CO0006_REQUIRED_COLUMNS:
        if not any(required.lower() in c.lower() for c in cols):
            errors.append(
                f"KEY_SOURCES_MISSING_COLUMN: CO-0006 table missing required column '{required}'"
            )
    return errors


def _validate_metadata(content: str) -> list[str]:
    """
    Find and validate the Metadata section.
    Accepts YAML fenced block or key: value lines.
    Returns list of error strings.
    """
    errors = []
    meta_match = re.search(
        r"^#{1,4}\s+Metadata\s*$(.+?)(?=^#{1,4}\s|\Z)",
        content,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if not meta_match:
        # Already caught by mandatory section check
        return []

    meta_body = meta_match.group(1)
    found_keys = set()

    # Try to extract key: value pairs (YAML-like or plain)
    for line in meta_body.split("\n"):
        kv = re.match(r"^\s*[`*_]*([a-z_]+)[`*_]*\s*[:=]\s*(.+)", line, re.IGNORECASE)
        if kv:
            found_keys.add(kv.group(1).lower().strip("`*_ "))

    # Also try fenced YAML block
    yaml_block = re.search(r"```ya?ml(.+?)```", meta_body, re.DOTALL)
    if yaml_block:
        for line in yaml_block.group(1).split("\n"):
            kv = re.match(r"^\s*([a-z_]+)\s*:", line, re.IGNORECASE)
            if kv:
                found_keys.add(kv.group(1).lower())

    for key in METADATA_REQUIRED_KEYS:
        if key.lower() not in found_keys:
            errors.append(f"METADATA_MISSING_KEY: Metadata section missing required key '{key}'")

    return errors


# ── Runner ───────────────────────────────────────────────────────────────────

def collect_bpc_files(repo_root: str = ".") -> list[str]:
    """Return all .md files under references/bpc/."""
    pattern = os.path.join(repo_root, "references", "bpc", "**", "*.md")
    return sorted(glob.glob(pattern, recursive=True))


def run(files: list[str], verbose: bool = False, warn_only: bool = False) -> int:
    """
    Validate all files. Returns exit code (0 = all pass, 1 = failures).
    If warn_only=True, reports failures but always exits 0.
    """
    total = len(files)
    failed = 0
    all_results = {}

    for path in files:
        errors = validate_file(path)
        all_results[path] = errors
        if errors:
            failed += 1

    # Output results
    label = "WARN" if warn_only else "FAIL"
    for path, errors in all_results.items():
        if errors:
            print(f"{label}: {path}")
            for e in errors:
                print(f"  {e}")
        elif verbose:
            print(f"PASS: {path}")

    # Summary
    passed = total - failed
    mode = " (warn-only mode — exit 0 regardless)" if warn_only else ""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"validate_bpc.py: {passed}/{total} files passed{mode}", file=sys.stderr)
    if failed:
        print(f"  {failed} file(s) with issues — see output above", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    if warn_only:
        return 0
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description="Validate BPC files")
    parser.add_argument("files", nargs="*", help="File path(s) to validate")
    parser.add_argument("--all", action="store_true", help="Validate all BPC files in references/bpc/")
    parser.add_argument("--changed", action="store_true", help="Read file paths from stdin")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show PASS results too")
    parser.add_argument("--warn-only", action="store_true",
                        help="Report failures but exit 0 (use during transition before Block 2)")
    args = parser.parse_args()

    if args.all:
        files = collect_bpc_files()
        if not files:
            print("No BPC files found under references/bpc/", file=sys.stderr)
            sys.exit(0)
    elif args.changed:
        files = [line.strip() for line in sys.stdin if line.strip().endswith(".md")]
    elif args.files:
        files = args.files
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(run(files, verbose=args.verbose, warn_only=args.warn_only))


if __name__ == "__main__":
    main()
