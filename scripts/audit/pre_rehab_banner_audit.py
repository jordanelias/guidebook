"""
scripts/audit/pre_rehab_banner_audit.py — Level 2 audit for B.0 banner cohort.

Verifies the four invariants enumerated in DR-2026-05-23 § "Audit":

  1. Every cohort file (current [OPUS-SYNTHESIS*] tag scan, positive declaration)
     carries the **SYNTHESIS VALIDITY:** PRE-REHABILITATION banner.
  2. Every cohort slug has bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'.
  3. No file OUTSIDE the cohort carries the banner.
  4. No slug in bpc_metadata holds 'RETRACTED-PRE-REHAB' without a corresponding
     cohort file (DB-vs-markdown drift in either direction).

Rule provenance: PI v10.14 standing rule #10 (final paragraph), DR-2026-05-23.

Exit code 0 = pass, 1 = any drift found.

Defaults: DB at data/guidebook.db relative to repo root; override via
GUIDEBOOK_DB_PATH (mirrors scripts/migrate_db.py).
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
BPC_DIR = REPO_ROOT / "references" / "bpc"

TAG_RE = re.compile(r"\[OPUS-SYNTHESIS[^\]]*\]")
POS_RE = re.compile(r"opus[_ ]synthesis[\*\s:]*(true|YES)\b", re.I)
NEG_RE = re.compile(r"opus[_ ]synthesis[\*\s:]*(false|NO)\b", re.I)
BANNER_RE = re.compile(r"SYNTHESIS VALIDITY[:\*\s]*PRE-REHABILITATION", re.I)


def scan_files():
    """Return (cohort_paths, cohort_slugs, banner_paths) sets."""
    cohort_paths = set()
    cohort_slugs = set()
    banner_paths = set()
    for root, _, fnames in os.walk(BPC_DIR):
        for f in fnames:
            if not f.endswith(".md") or f.startswith("_template"):
                continue
            path = Path(root) / f
            slug = f[:-3]
            txt = path.read_text()
            in_cohort = bool(TAG_RE.search(txt)) and not (
                NEG_RE.search(txt) and not POS_RE.search(txt)
            )
            if in_cohort:
                cohort_paths.add(str(path.relative_to(REPO_ROOT)))
                cohort_slugs.add(slug)
            if BANNER_RE.search(txt):
                banner_paths.add(str(path.relative_to(REPO_ROOT)))
    return cohort_paths, cohort_slugs, banner_paths


def db_state():
    con = sqlite3.connect(DB_PATH)
    rows = set(
        r[0] for r in con.execute(
            "SELECT slug FROM bpc_metadata WHERE evidence_state = 'RETRACTED-PRE-REHAB'"
        )
    )
    con.close()
    return rows


def audit():
    cohort_paths, cohort_slugs, banner_paths = scan_files()
    db_retracted = db_state()

    issues = []

    # Invariant 1: every cohort file carries the banner
    missing_banner = cohort_paths - banner_paths
    if missing_banner:
        issues.append(("1", "cohort files missing banner", sorted(missing_banner)))

    # Invariant 2: every cohort slug has evidence_state = RETRACTED-PRE-REHAB
    missing_db = cohort_slugs - db_retracted
    if missing_db:
        issues.append(("2", "cohort slugs without DB banner state", sorted(missing_db)))

    # Invariant 3: no file outside the cohort carries the banner
    over_banner = banner_paths - cohort_paths
    if over_banner:
        issues.append(("3", "files with banner but outside current cohort", sorted(over_banner)))

    # Invariant 4: no DB row in RETRACTED-PRE-REHAB without a cohort slug
    over_db = db_retracted - cohort_slugs
    if over_db:
        issues.append(("4", "DB slugs in RETRACTED-PRE-REHAB without cohort file", sorted(over_db)))

    print("=" * 76)
    print("pre_rehab_banner_audit — DR-2026-05-23 / PI rule #10")
    print("=" * 76)
    print(f"cohort files:                {len(cohort_paths)}")
    print(f"cohort unique slugs:         {len(cohort_slugs)}")
    print(f"files with banner:           {len(banner_paths)}")
    print(f"DB slugs in RETRACTED-PRE-REHAB: {len(db_retracted)}")
    print()

    if not issues:
        print("VERDICT: PASS — all four invariants hold.")
        return 0

    print(f"VERDICT: FAIL — {len(issues)} invariant(s) violated.")
    print()
    for num, label, items in issues:
        print(f"--- Invariant {num}: {label} ({len(items)}) ---")
        for x in items[:20]:
            print(f"  {x}")
        if len(items) > 20:
            print(f"  ... +{len(items)-20} more")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(audit())
