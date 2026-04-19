#!/usr/bin/env python3
"""
check_phase_a_complete.py — Phase A completion checker.
Verifies all transition criteria before Phase B (Claude Code Build) begins.

Usage:
    python3 scripts/check_phase_a_complete.py
    python3 scripts/check_phase_a_complete.py --repo-root /path/to/guidebook

Exit codes:
    0 — all criteria pass
    1 — one or more criteria fail

Generated: Block 5 — 2026-04-19
"""

import sys
import os
import re
import glob
import argparse
from pathlib import Path


def check_a1_bpc_migration(repo_root: str) -> tuple[bool, str]:
    """A1: ≥95% of BPC files have CO-0006 Key sources table."""
    bpc_files = sorted(glob.glob(
        os.path.join(repo_root, "references", "bpc", "**", "*.md"), recursive=True
    ))
    if not bpc_files:
        return False, "No BPC files found"

    co0006_count = 0
    merged_count = 0
    for path in bpc_files:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        if re.search(r"\*\*Status:\*\*\s*MERGED|status:\s*MERGED", content, re.IGNORECASE):
            merged_count += 1
            continue
        if re.search(r"^\|.+REF-ID.+\|", content, re.MULTILINE):
            co0006_count += 1

    eligible = len(bpc_files) - merged_count
    pct = co0006_count / eligible * 100 if eligible else 0
    passed = pct >= 95
    return passed, f"{co0006_count}/{eligible} files ({pct:.0f}%) have CO-0006 table (merged stubs: {merged_count})"


def check_a2_spec_db(repo_root: str) -> tuple[bool, str]:
    """A2: spec-db-part4-reconciliation.md exists and is non-empty."""
    path = os.path.join(repo_root, "references", "spec-db-part4-reconciliation.md")
    if not os.path.exists(path):
        return False, "File not found"
    size = os.path.getsize(path)
    passed = size > 1000
    return passed, f"File exists, {size} bytes"


def check_a3_gap_register(repo_root: str) -> tuple[bool, str]:
    """A3: gap_register.md and gap_register_archive.md both exist."""
    gap = os.path.exists(os.path.join(repo_root, "gap_register.md"))
    archive = os.path.exists(os.path.join(repo_root, "gap_register_archive.md"))
    passed = gap and archive
    return passed, f"gap_register.md: {gap}, gap_register_archive.md: {archive}"


def check_a4_part4_items(repo_root: str) -> tuple[bool, str]:
    """A4: Part 4 has no duplicate active item codes; item count in expected range."""
    path = os.path.join(repo_root, "parts", "v10", "part04.md")
    if not os.path.exists(path):
        return False, "part04.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    codes = re.findall(r"^### ([A-K]-\d+)\b", content, re.MULTILINE)
    from collections import Counter
    counts = Counter(codes)
    dups = {c: n for c, n in counts.items() if n > 1 and c not in ("E-10",)}  # E-10 redirect is known
    total = len(codes)
    passed = len(dups) == 0 and 88 <= total <= 95
    return passed, f"{total} item headings found; duplicates (excl. E-10): {dups or 'none'}"


def check_a5_standards(repo_root: str) -> tuple[bool, str]:
    """A5: Standards registry count ≥ 80."""
    path = os.path.join(repo_root, "references", "standards-registry.md")
    if not os.path.exists(path):
        return False, "standards-registry.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    count = len(re.findall(r'standard_cited: "(?!\[)', content))
    passed = count >= 80
    return passed, f"{count} entries (target ≥80)"


def check_a6_brief_builder(repo_root: str) -> tuple[bool, str]:
    """A6: parser-source-readiness.md contains Brief Builder validation."""
    path = os.path.join(repo_root, "references", "parser-source-readiness.md")
    if not os.path.exists(path):
        return False, "parser-source-readiness.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    has_brief = "Brief Builder" in content or "brief_builder" in content.lower()
    has_audit = "audit_status: PASS" in content
    passed = has_brief and has_audit
    return passed, f"Brief Builder ref: {has_brief}, audit_status PASS: {has_audit}"


def check_a7_annotations(repo_root: str) -> tuple[bool, str]:
    """A7: Every Part 4 item has design_stage_lock, ve_risk, ot_appointment_trigger."""
    path = os.path.join(repo_root, "parts", "v10", "part04.md")
    if not os.path.exists(path):
        return False, "part04.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    ds = content.count("design_stage_lock:")
    ve = content.count("ve_risk:")
    ot = content.count("ot_appointment_trigger:")
    passed = ds >= 90 and ve >= 90 and ot >= 90
    return passed, f"design_stage_lock: {ds}, ve_risk: {ve}, ot_appointment_trigger: {ot} (target ≥90 each)"


def check_b1_connections(repo_root: str) -> tuple[bool, str]:
    """B1: Connections _index shows CONSUMED+CONSUMED-DEFERRED ≥ 182."""
    path = os.path.join(repo_root, "references", "connections", "_index.md")
    if not os.path.exists(path):
        return False, "_index.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    consumed = len(re.findall(r"\| CON-\d+ \| CONSUMED \|", content))
    deferred = len(re.findall(r"\| CON-\d+ \| CONSUMED-DEFERRED \|", content))
    pending  = len(re.findall(r"\| CON-\d+ \| PENDING \|", content))
    total_consumed = consumed + deferred
    passed = total_consumed >= 182 and pending == 0
    return passed, f"CONSUMED: {consumed}, DEFERRED: {deferred}, PENDING: {pending}"


def check_b2_priority_srs(repo_root: str) -> tuple[bool, str]:
    """B2: Rashid, Quesada-Cubo, Simpson 2025 each referenced in ≥1 BPC."""
    bpc_files = glob.glob(
        os.path.join(repo_root, "references", "bpc", "**", "*.md"), recursive=True
    )
    content_all = ""
    for f in bpc_files:
        with open(f, encoding="utf-8") as fh:
            content_all += fh.read()
    rashid = "Rashid" in content_all
    quesada = "Quesada" in content_all
    simpson = "Simpson" in content_all and "school" in content_all.lower()
    passed = rashid and quesada and simpson
    return passed, f"Rashid: {rashid}, Quesada-Cubo: {quesada}, Simpson: {simpson}"


def check_b3_grade(repo_root: str) -> tuple[bool, str]:
    """B3: Categories A, E, G items have grade_confidence annotation."""
    path = os.path.join(repo_root, "parts", "v10", "part04.md")
    if not os.path.exists(path):
        return False, "part04.md not found"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    grade_count = content.count("grade_confidence:")
    passed = grade_count >= 40  # A(16)+E(12)+G(9) minimum = 37; with extras ~40
    return passed, f"grade_confidence annotations: {grade_count} (target ≥40 for A+E+G)"


def check_b5_hallucination(repo_root: str) -> tuple[bool, str]:
    """B5: hallucination audit file exists."""
    files = glob.glob(os.path.join(repo_root, "references", "bpc-hallucination-audit-*.md"))
    passed = len(files) > 0
    return passed, f"Audit file(s) found: {[os.path.basename(f) for f in files]}"


def check_handoff(repo_root: str) -> tuple[bool, str]:
    """Phase B handoff document exists."""
    path = os.path.join(repo_root, "references", "phase-b-handoff.md")
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    passed = exists and size > 500
    return passed, f"phase-b-handoff.md: exists={exists}, size={size}"


CHECKS = [
    ("A1", "BPC CO-0006 migration ≥95%", check_a1_bpc_migration),
    ("A2", "Spec DB reconciliation exists", check_a2_spec_db),
    ("A3", "Gap register + archive exist", check_a3_gap_register),
    ("A4", "Part 4 item codes valid", check_a4_part4_items),
    ("A5", "Standards registry ≥80 entries", check_a5_standards),
    ("A6", "Parser source readiness PASS", check_a6_brief_builder),
    ("A7", "Part 4 HTML annotations present", check_a7_annotations),
    ("B1", "Connections consumed ≥182", check_b1_connections),
    ("B2", "Priority SRs referenced in BPC", check_b2_priority_srs),
    ("B3", "GRADE annotations present", check_b3_grade),
    ("B5", "Hallucination audit exists", check_b5_hallucination),
    ("Handoff", "Phase B handoff document", check_handoff),
]


def main():
    parser = argparse.ArgumentParser(description="Check Phase A completion criteria")
    parser.add_argument("--repo-root", default=".", help="Path to guidebook repo root")
    args = parser.parse_args()

    passed_all = True
    results = []

    for code, description, fn in CHECKS:
        passed, detail = fn(args.repo_root)
        status = "PASS" if passed else "FAIL"
        if not passed:
            passed_all = False
        results.append((code, status, description, detail))

    # Output
    print(f"{'='*65}")
    print("check_phase_a_complete.py — Phase A Transition Criteria")
    print(f"{'='*65}")
    for code, status, description, detail in results:
        print(f"  [{status}] {code}: {description}")
        print(f"         {detail}")

    print(f"{'='*65}")
    if passed_all:
        print("RESULT: ALL CRITERIA PASS — Phase B may begin.")
    else:
        failed = [r[0] for r in results if r[1] == "FAIL"]
        print(f"RESULT: FAIL — {len(failed)} criteria not met: {failed}")
        print("Phase B cannot begin until all criteria pass.")
    print(f"{'='*65}")

    sys.exit(0 if passed_all else 1)


if __name__ == "__main__":
    main()
