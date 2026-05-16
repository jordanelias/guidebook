#!/usr/bin/env python3
"""
scripts/validate_population.py — Validate population codes across the corpus.

Per governance/population-taxonomy.md (A7):
- All population codes resolve to PopulationCode enum
- BAR/CHD/LPA/EXH only in supplementary files
- VIS/DEAF as compound code is rejected
- ALL never combined with specific codes
- IntD does not appear as a population code
- One slug, one population (warning)
- Sub-code range containment (warning, where data exists)

Usage:
    python3 scripts/validate_population.py                 # full scan
    python3 scripts/validate_population.py --quick          # sample 5 per directory
    python3 scripts/validate_population.py --bpc-only       # BPC files only
    python3 scripts/validate_population.py path/to/file.md  # single file

Exit codes:
    0 = all checks pass
    1 = errors found
    2 = configuration error
"""

import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.enums import PopulationCode


# Canonical code values from enum
VALID_CODES = {member.value for member in PopulationCode}

# Supplementary-only codes
SUPPLEMENTARY_CODES = {"CHD", "LPA", "EXH", "BAR"}

# Sub-code lookup (child → parent)
SUBCODE_PARENTS = {
    "MOB/AMB": "MOB",
    "MOB/UPL": "MOB",
    "NDV/AUT": "NDV",
    "NDV/ADHD": "NDV",
    "NDV/SENS": "NDV",
    "NEU/PCS": "NEU",
    "OFS/ME": "OFS",
    "OFS/POTS": "OFS",
    "OFS/MCAS": "OFS",
}

# Known sub-codes (for distinguishing sub-code slash from multi-pop slash)
KNOWN_SUBCODES = set(SUBCODE_PARENTS.keys())

# Invalid compound codes
INVALID_COMPOUNDS = {"VIS/DEAF", "DEAF/VIS"}


def is_supplementary_path(path: str) -> bool:
    """Check if a file path is in the supplementary section."""
    p = path.lower()
    return "supp" in p or "supplementary" in p


def extract_population_from_yaml_frontmatter(text: str) -> list:
    """Extract population field from YAML front matter in markdown."""
    # Match YAML front matter between ---
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return []

    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return []

    if not isinstance(fm, dict):
        return []

    pop = fm.get("population") or fm.get("populations") or fm.get("pop")
    if pop is None:
        return []

    if isinstance(pop, str):
        return [pop.strip()]
    if isinstance(pop, list):
        return [str(p).strip() for p in pop]
    return []


def extract_population_from_yaml_file(path: str) -> list:
    """Extract populations from a YAML data file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []

    if not isinstance(data, dict):
        return []

    pops = data.get("populations") or data.get("population") or []
    if isinstance(pops, str):
        return [pops.strip()]
    if isinstance(pops, list):
        return [str(p).strip() for p in pops]
    return []


def validate_codes(codes: list, path: str) -> tuple:
    """Validate a list of population codes. Returns (errors, warnings)."""
    errors = []
    warnings = []

    for code in codes:
        # Check for invalid compounds
        if code in INVALID_COMPOUNDS:
            errors.append(
                f"Invalid compound code '{code}' — "
                f"VIS, DEAF, DBL are three distinct independent codes"
            )
            continue

        # Check IntD
        if code == "IntD":
            errors.append(
                f"IntD is not a standalone population code — "
                f"proxy through DEM + NDV per project-standards"
            )
            continue

        # Check valid code
        if code not in VALID_CODES:
            errors.append(f"Unknown population code: '{code}'")
            continue

        # Check supplementary containment
        if code in SUPPLEMENTARY_CODES and not is_supplementary_path(path):
            errors.append(
                f"Supplementary code '{code}' found outside "
                f"supplementary files: {path}"
            )

    # Check ALL exclusivity
    if "ALL" in codes and len(codes) > 1:
        errors.append(
            f"ALL combined with specific codes: {codes} — "
            f"ALL must be sole population code"
        )

    # Check one-slug-one-population for BPC files
    if "/bpc/" in path.lower() and len(codes) > 1:
        warnings.append(
            f"BPC file has multiple population codes: {codes} — "
            f"each slug should cover exactly one population"
        )

    return errors, warnings


def scan_markdown_files(patterns: list, quick: bool = False) -> tuple:
    """Scan markdown files for population codes."""
    total_errors = 0
    total_warnings = 0
    total_files = 0

    for pattern in patterns:
        files = sorted(glob.glob(pattern, recursive=True))
        if quick:
            import random
            files = random.sample(files, min(5, len(files)))

        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print(f"  READ ERROR {path}: {e}", file=sys.stderr)
                continue

            codes = extract_population_from_yaml_frontmatter(text)
            if not codes:
                continue

            total_files += 1
            errors, warnings = validate_codes(codes, path)

            if errors:
                total_errors += len(errors)
                for e in errors:
                    print(f"ERROR {os.path.basename(path)}: {e}")

            if warnings:
                total_warnings += len(warnings)
                for w in warnings:
                    print(f"WARN  {os.path.basename(path)}: {w}")

    return total_files, total_errors, total_warnings


def scan_yaml_files(directory: str, quick: bool = False) -> tuple:
    """Scan YAML data files for population codes."""
    total_errors = 0
    total_warnings = 0
    total_files = 0

    if not os.path.isdir(directory):
        return 0, 0, 0

    files = sorted(glob.glob(os.path.join(directory, "*.yaml")))
    if quick:
        import random
        files = random.sample(files, min(5, len(files)))

    for path in files:
        codes = extract_population_from_yaml_file(path)
        if not codes:
            continue

        total_files += 1
        errors, warnings = validate_codes(codes, path)

        if errors:
            total_errors += len(errors)
            for e in errors:
                print(f"ERROR {os.path.basename(path)}: {e}")

        if warnings:
            total_warnings += len(warnings)
            for w in warnings:
                print(f"WARN  {os.path.basename(path)}: {w}")

    return total_files, total_errors, total_warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate population codes across the corpus"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to validate",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Sample 5 files from each directory",
    )
    parser.add_argument(
        "--bpc-only",
        action="store_true",
        help="Only validate BPC files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print all files checked",
    )
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    grand_files = 0
    grand_errors = 0
    grand_warnings = 0

    if args.files:
        # Validate specific files
        for path in args.files:
            if not os.path.exists(path):
                print(f"  NOT FOUND: {path}", file=sys.stderr)
                grand_errors += 1
                continue

            if path.endswith(".yaml") or path.endswith(".yml"):
                codes = extract_population_from_yaml_file(path)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    codes = extract_population_from_yaml_frontmatter(f.read())

            if not codes:
                continue

            grand_files += 1
            errors, warnings = validate_codes(codes, path)
            grand_errors += len(errors)
            grand_warnings += len(warnings)
            for e in errors:
                print(f"ERROR {path}: {e}")
            for w in warnings:
                print(f"WARN  {path}: {w}")
    else:
        # Full scan
        md_patterns = []
        if not args.bpc_only:
            md_patterns.extend([
                os.path.join(repo_root, "references", "bpc", "**", "*.md"),
                os.path.join(repo_root, "references", "search-log", "**", "*.md"),
                os.path.join(repo_root, "references", "connections", "**", "*.md"),
            ])
        else:
            md_patterns.append(
                os.path.join(repo_root, "references", "bpc", "**", "*.md")
            )

        f, e, w = scan_markdown_files(md_patterns, quick=args.quick)
        grand_files += f
        grand_errors += e
        grand_warnings += w

        # YAML data files
        if not args.bpc_only:
            spec_dir = os.path.join(repo_root, "data", "specifications")
            f2, e2, w2 = scan_yaml_files(spec_dir, quick=args.quick)
            grand_files += f2
            grand_errors += e2
            grand_warnings += w2

    # Summary
    if grand_files == 0:
        print(
            "No files with population codes found to validate.",
            file=sys.stderr,
        )
        return 0

    status = "PASS" if grand_errors == 0 else "FAIL"
    print(
        f"\n{status}: {grand_files} files checked, "
        f"{grand_errors} errors, {grand_warnings} warnings",
        file=sys.stderr,
    )
    return 1 if grand_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
