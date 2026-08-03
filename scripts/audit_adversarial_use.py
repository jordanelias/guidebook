#!/usr/bin/env python3
"""
scripts/audit_adversarial_use.py — Pre-release adversarial-use review gate.

Per governance/adversarial-use-framework.md (A10) §4.4 + §6.

Three checks:
  - C1 catalogue well-formed: data/adversarial_use/catalog.yaml validates as MisuseVectorCatalog
  - C2 review coverage complete: every ACTIVE/IN_PREP guidebook version has a
       review_log/{version_tag}.yaml; every catalogue vector is reviewed for that version
  - C3 review entries well-formed: each review entry validates as MisuseReview;
       VersionReviewLog version_tag matches its file's intent

Usage:
    python3 scripts/audit_adversarial_use.py                    # full audit
    python3 scripts/audit_adversarial_use.py --catalog-only     # C1 only
    python3 scripts/audit_adversarial_use.py --version v9.0     # one version
    python3 scripts/audit_adversarial_use.py --report           # summary; exit 0

Exit codes: 0 = pass, 1 = errors, 2 = config error.

This validator does NOT perform automated content scanning for misuse patterns.
Most adversarial-use vectors (V-01 through V-09) are not mechanically detectable
in prose. The pre-release review is a human-judgment exercise; this script
confirms the review has occurred and is well-recorded.
"""

import argparse
import glob
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.adversarial_use import (
    MisuseVectorCatalog,
    VersionReviewLog,
    ReleaseOverride,
)
from schemas.enums import MisuseVectorStatus

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(REPO_ROOT, "data", "adversarial_use", "catalog.yaml")
REVIEW_LOG_DIR = os.path.join(REPO_ROOT, "data", "adversarial_use", "review_log")
OVERRIDE_DIR = os.path.join(REPO_ROOT, "data", "adversarial_use", "overrides")
VERSIONS_DIR = os.path.join(REPO_ROOT, "data", "temporal", "guidebook_versions")


# --- C1: Catalogue ---

def check_catalog() -> tuple[list[str], list[str], MisuseVectorCatalog | None]:
    """C1: data/adversarial_use/catalog.yaml validates as MisuseVectorCatalog."""
    errors: list[str] = []
    warnings: list[str] = []

    if not os.path.exists(CATALOG_PATH):
        errors.append(
            f"C1: catalogue missing at {os.path.relpath(CATALOG_PATH, REPO_ROOT)}"
        )
        return errors, warnings, None

    try:
        catalog = MisuseVectorCatalog.from_yaml(CATALOG_PATH)
    except Exception as e:
        errors.append(f"C1: catalogue does not validate: {e}")
        return errors, warnings, None

    # Soft warnings
    active_count = sum(
        1 for v in catalog.vectors
        if (v.status if isinstance(v.status, str) else v.status.value) == "ACTIVE"
    )
    if active_count == 0:
        warnings.append(
            "C1: catalogue has no ACTIVE vectors; review will check zero items"
        )

    return errors, warnings, catalog


# --- Helper: load active+in_prep versions from A9 records ---

def load_versions_to_review() -> list[str]:
    """Return version_tags of ACTIVE and IN_PREP GuidebookVersion records."""
    if not os.path.isdir(VERSIONS_DIR):
        return []
    tags: list[str] = []
    seen: set[str] = set()
    for path in sorted(glob.glob(os.path.join(VERSIONS_DIR, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        status = data.get("status")
        tag = data.get("version_tag")
        if status in {"ACTIVE", "IN_PREP"} and tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


# --- C2 + C3: Review coverage and well-formedness ---

def check_review_coverage(
    catalog: MisuseVectorCatalog,
    only_version: str | None = None,
) -> tuple[list[str], list[str]]:
    """C2 + C3: every required version has well-formed coverage of all ACTIVE vectors."""
    errors: list[str] = []
    warnings: list[str] = []

    # Determine which versions need review_log coverage
    if only_version:
        target_versions = [only_version]
    else:
        target_versions = load_versions_to_review()

    if not target_versions:
        # No versions to review — emit info, not error
        warnings.append(
            "C2: no ACTIVE/IN_PREP guidebook versions found "
            "(data/temporal/guidebook_versions/ may be unbuilt)"
        )
        return errors, warnings

    # Active vectors that must be reviewed at each release
    active_vector_ids = {
        v.vector_id for v in catalog.vectors
        if (v.status if isinstance(v.status, str) else v.status.value) == "ACTIVE"
    }

    # Load overrides (so ESCALATE reviews with overrides aren't double-flagged)
    overrides: dict[tuple[str, str], ReleaseOverride] = {}
    if os.path.isdir(OVERRIDE_DIR):
        for path in sorted(glob.glob(os.path.join(OVERRIDE_DIR, "*.yaml"))):
            try:
                ov = ReleaseOverride.from_yaml(path)
                overrides[(ov.version_tag, ov.vector_id)] = ov
            except Exception as e:
                warnings.append(
                    f"C3: override at {os.path.relpath(path, REPO_ROOT)} "
                    f"does not validate: {e}"
                )

    # For each target version, check the review_log
    for vt in target_versions:
        # Filename safe: replace . with -
        log_name = vt.replace(".", "-").replace("v", "v") + ".yaml"
        log_path = os.path.join(REVIEW_LOG_DIR, log_name)

        if not os.path.exists(log_path):
            errors.append(
                f"C2 {vt}: review log missing at "
                f"{os.path.relpath(log_path, REPO_ROOT)}"
            )
            continue

        try:
            log = VersionReviewLog.from_yaml(log_path)
        except Exception as e:
            errors.append(f"C3 {vt}: review log does not validate: {e}")
            continue

        if log.version_tag != vt:
            errors.append(
                f"C3 {vt}: review log version_tag='{log.version_tag}' does not "
                f"match expected '{vt}' (filename: {log_name})"
            )

        # Per-vector coverage
        reviewed_ids = {r.vector_id for r in log.reviews}
        missing = active_vector_ids - reviewed_ids
        for m in sorted(missing):
            errors.append(
                f"C2 {vt}: ACTIVE vector {m} has no review entry"
            )

        # Reviews that reference unknown vectors
        unknown = reviewed_ids - {v.vector_id for v in catalog.vectors}
        for u in sorted(unknown):
            errors.append(
                f"C2 {vt}: review entry for {u} but vector not in catalogue"
            )

        # ESCALATE reviews must have an override or be flagged
        for r in log.reviews:
            status_val = (
                r.status if isinstance(r.status, str) else r.status.value
            )
            if status_val == "ESCALATE":
                if (vt, r.vector_id) not in overrides:
                    errors.append(
                        f"C2 {vt}: review for {r.vector_id} is ESCALATE; "
                        f"no ReleaseOverride record exists. Either resolve the "
                        f"escalation or commit a release_override.yaml."
                    )

        # Catalog version mismatch warning
        if log.catalog_version_at_review != catalog.catalog_version:
            warnings.append(
                f"C2 {vt}: review used catalogue version "
                f"{log.catalog_version_at_review}, current is "
                f"{catalog.catalog_version}; consider re-review"
            )

    return errors, warnings


# --- Main ---

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--catalog-only", action="store_true",
                    help="run only C1 (catalogue well-formed)")
    ap.add_argument("--version", default=None,
                    help="audit a single version_tag (e.g., v9.0)")
    ap.add_argument("--report", action="store_true",
                    help="print summary; exit 0 always")
    args = ap.parse_args()

    all_errors: list[str] = []
    all_warnings: list[str] = []

    # C1 always runs
    e1, w1, catalog = check_catalog()
    all_errors.extend(e1)
    all_warnings.extend(w1)

    if catalog and not args.catalog_only:
        e2, w2 = check_review_coverage(catalog, only_version=args.version)
        all_errors.extend(e2)
        all_warnings.extend(w2)

    # Report
    if catalog:
        active = sum(
            1 for v in catalog.vectors
            if (v.status if isinstance(v.status, str) else v.status.value) == "ACTIVE"
        )
        retired = sum(
            1 for v in catalog.vectors
            if (v.status if isinstance(v.status, str) else v.status.value) == "RETIRED"
        )
        print(
            f"Adversarial-use audit: catalogue v{catalog.catalog_version} — "
            f"{active} ACTIVE / {retired} RETIRED vectors"
        )
    else:
        print("Adversarial-use audit: catalogue not loaded")

    if all_errors:
        print(f"\nERRORS ({len(all_errors)}):")
        for e in all_errors:
            print(f"  {e}")
    if all_warnings:
        print(f"\nWARNINGS ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"  {w}")
    if not all_errors and not all_warnings:
        print("All checks passed.")

    if args.report:
        return 0
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
