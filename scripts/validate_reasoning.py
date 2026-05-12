#!/usr/bin/env python3
"""Validate BPC and connection reasoning documents against the workplan templates.

Per Phase A.9 of audits/bpc-rewrite-workplan-2026-05-11.md.
PI v10.8 §hooks_status records this as level-2 enforcement (validator runs but is
not yet a hard hook; promotion to hook follows Phase 1 calibration).

Usage:
  python scripts/validate_reasoning.py                       # validate all
  python scripts/validate_reasoning.py --slug grab-bar       # one BPC reasoning doc
  python scripts/validate_reasoning.py --con CON-0042        # one connection doc
  python scripts/validate_reasoning.py --mode bpc            # all BPC docs only
  python scripts/validate_reasoning.py --mode connection     # all connection docs only
  python scripts/validate_reasoning.py --strict              # exit 1 on any error
  python scripts/validate_reasoning.py --json                # machine-readable output

Exit codes:
  0 — all valid (or --strict not set and warnings only)
  1 — validation errors found and --strict was set
  2 — invocation error
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BPC_REASONING_DIR = REPO_ROOT / "references" / "bpc-reasoning"
CON_REASONING_DIR = REPO_ROOT / "references" / "connection-reasoning"

# ── Required structure for BPC reasoning documents ──────────────────────────

BPC_REQUIRED_SECTIONS = [
    "A. Evidence inventory",
    "A.1 Sources formally linked",
    "A.2 Sources cited in this BPC but NOT formally linked",
    "A.3 Practitioner / secondary sources",
    "A.4 Primary regulatory documents retrieved",
    "A.5 Gaps in the evidence inventory",
    "B. Per-parameter reasoning",
    "C. Synthesis claims that did NOT survive evidence review",
    "D. Cross-references",
    "E. Adversarial protocol pass",
    "F. Provenance trail",
]

BPC_REQUIRED_HEADER_FIELDS = ["BPC file", "BPC population", "Generated", "Status"]
BPC_STATUS_ENUM = {"DRAFT", "OPUS-PENDING", "COMPLETE"}

# The 9 steps that every B.N parameter block must contain.
NINE_STEPS = [
    "Step 1 — Direction",
    "Step 2 — Per-population worst-case user",
    "Step 3 — Jurisdiction comparison",
    "Step 4 — Lowest-barrier code per population",
    "Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence",
    "Step 6 — Guidebook chosen value per population",
    "Step 7 — Rationale",
    "Step 8 — Trade-offs",
    "Step 9 — Cross-population conflict flag",
]

ADVERSARIAL_FIELDS = [
    "Confidence interval",
    "Shift conditions",
    "Named dissenter",
    "Falsification condition",
]

# ── Required structure for connection reasoning documents ──────────────────

CON_REQUIRED_SECTIONS = [
    "A. What this connection asserts",
    "B. Targets verified",
    "C. Evidence supporting the connection",
    "D. Confidence rationale",
    "E. Opus review decision",
    "F. Application",
]
CON_REQUIRED_HEADER_FIELDS = ["Status", "Confidence", "Connection type"]
CON_STATUS_ENUM = {"CONSUMED", "CONSUMED-DEFERRED", "PENDING", "CLOSED"}
CON_CONFIDENCE_ENUM = {"HIGH", "MODERATE", "SPECULATIVE"}


def validate_bpc_doc(path: Path) -> dict:
    """Validate one BPC reasoning document. Returns {file, errors, warnings}."""
    errors = []
    warnings = []
    content = path.read_text(encoding="utf-8", errors="replace")

    # Skip template / empty stubs
    if path.name == "_template.md":
        return {"file": str(path), "skipped": True, "reason": "template"}
    if len(content) < 200:
        errors.append("File is empty or near-empty (<200 chars)")
        return {"file": str(path), "errors": errors, "warnings": warnings}

    # Header fields
    for field in BPC_REQUIRED_HEADER_FIELDS:
        if not re.search(rf"^\*\*{re.escape(field)}:\*\*", content, re.M):
            errors.append(f"Missing required header field: **{field}**")

    # Status value check
    status_m = re.search(r"^\*\*Status:\*\*\s*(\S+)", content, re.M)
    if status_m:
        status_val = status_m.group(1).strip()
        if status_val not in BPC_STATUS_ENUM:
            errors.append(f"Status '{status_val}' not in {sorted(BPC_STATUS_ENUM)}")

    # Required sections
    for section in BPC_REQUIRED_SECTIONS:
        # Match as ## or ### header line containing the section label
        pat = re.compile(rf"^#{{2,4}}\s+{re.escape(section)}", re.M)
        if not pat.search(content):
            errors.append(f"Missing required section: '{section}'")

    # B section: parameter blocks must each have all 9 steps
    b_section_m = re.search(
        r"^## B\..*?(?=^## C\.|^## [D-Z]\.|\Z)", content, re.M | re.S
    )
    if b_section_m:
        b_body = b_section_m.group(0)
        # Find each parameter block (### B.N Parameter: ...)
        param_blocks = re.findall(
            r"^### B\.\d+ Parameter:.*?(?=^### B\.\d+ Parameter:|^## [C-Z]\.|\Z)",
            b_body, re.M | re.S
        )
        if not param_blocks:
            warnings.append(
                "Section B has no `### B.N Parameter:` blocks — "
                "no parameters reasoned about yet"
            )
        for i, block in enumerate(param_blocks, 1):
            # Skip the literal "<next parameter>" placeholder block
            if "<next parameter>" in block:
                continue
            param_name_m = re.search(r"^### (B\.\d+ Parameter:[^\n]+)", block, re.M)
            param_label = param_name_m.group(1) if param_name_m else f"block #{i}"
            for step in NINE_STEPS:
                # Allow the step text to be on a bold-formatted line or in a header
                step_pat = re.compile(re.escape(step), re.I)
                if not step_pat.search(block):
                    errors.append(
                        f"{param_label}: missing step `{step}`"
                    )

    # E section adversarial fields
    e_section_m = re.search(
        r"^## E\..*?(?=^## F\.|^## [G-Z]\.|\Z)", content, re.M | re.S
    )
    if e_section_m:
        e_body = e_section_m.group(0)
        for field in ADVERSARIAL_FIELDS:
            if field.lower() not in e_body.lower():
                warnings.append(f"E section missing reference to '{field}'")

    return {"file": str(path), "errors": errors, "warnings": warnings}


def validate_connection_doc(path: Path) -> dict:
    errors = []
    warnings = []
    content = path.read_text(encoding="utf-8", errors="replace")

    if path.name == "_template.md":
        return {"file": str(path), "skipped": True, "reason": "template"}
    if len(content) < 100:
        errors.append("File is empty or near-empty (<100 chars)")
        return {"file": str(path), "errors": errors, "warnings": warnings}

    # Header
    for field in CON_REQUIRED_HEADER_FIELDS:
        if not re.search(rf"^\*\*{re.escape(field)}:\*\*", content, re.M):
            errors.append(f"Missing required header field: **{field}**")

    # Status / Confidence enums
    status_m = re.search(r"^\*\*Status:\*\*\s*(\S+)", content, re.M)
    if status_m:
        val = status_m.group(1).strip()
        if val not in CON_STATUS_ENUM:
            errors.append(f"Status '{val}' not in {sorted(CON_STATUS_ENUM)}")
    conf_m = re.search(r"^\*\*Confidence:\*\*\s*(\S+)", content, re.M)
    if conf_m:
        val = conf_m.group(1).strip()
        if val not in CON_CONFIDENCE_ENUM:
            errors.append(f"Confidence '{val}' not in {sorted(CON_CONFIDENCE_ENUM)}")

    # Required sections
    for section in CON_REQUIRED_SECTIONS:
        pat = re.compile(rf"^#{{2,4}}\s+{re.escape(section)}", re.M)
        if not pat.search(content):
            errors.append(f"Missing required section: '{section}'")

    # Section A length check (≥1 sentence, ≤500 chars rule from workplan §3)
    a_m = re.search(
        r"^## A\. What this connection asserts(.*?)(?=^## B\.|\Z)",
        content, re.M | re.S
    )
    if a_m:
        a_body = a_m.group(1).strip()
        # Strip the boilerplate placeholder line
        a_clean = re.sub(r"^Free-text description.*?\.", "", a_body, flags=re.M).strip()
        if len(a_clean) < 20:
            warnings.append("A section is empty or contains only template placeholder")
        elif len(a_clean) > 500:
            warnings.append(
                f"A section is {len(a_clean)} chars; workplan §3 limit is ≤500"
            )

    return {"file": str(path), "errors": errors, "warnings": warnings}


def collect_files(mode: str, slug: str | None, con: str | None) -> list:
    files = []
    if mode in ("all", "bpc"):
        if slug:
            target = BPC_REASONING_DIR / f"{slug}.md"
            if target.exists():
                files.append(("bpc", target))
            else:
                print(f"ERROR: BPC reasoning doc not found: {target}", file=sys.stderr)
                return []
        elif BPC_REASONING_DIR.exists():
            files += [("bpc", p) for p in BPC_REASONING_DIR.glob("*.md")]
    if mode in ("all", "connection"):
        if con:
            target = CON_REASONING_DIR / f"{con}.md"
            if target.exists():
                files.append(("connection", target))
            else:
                print(f"ERROR: Connection reasoning doc not found: {target}", file=sys.stderr)
                return []
        elif CON_REASONING_DIR.exists():
            files += [("connection", p) for p in CON_REASONING_DIR.glob("*.md")]
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--slug", help="Validate one BPC reasoning doc by slug")
    ap.add_argument("--con", help="Validate one connection reasoning doc by CON-ID")
    ap.add_argument("--mode", choices=["all", "bpc", "connection"], default="all")
    ap.add_argument("--strict", action="store_true",
                    help="Exit 1 on any validation error")
    ap.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = ap.parse_args()

    files = collect_files(args.mode, args.slug, args.con)
    if not files:
        if args.json:
            print(json.dumps({"checked": 0, "results": [], "summary": {}}, indent=2))
        else:
            print(f"No reasoning docs found in mode={args.mode}.")
            print(f"  Expected location: {BPC_REASONING_DIR.relative_to(REPO_ROOT)}")
            print(f"  Expected location: {CON_REASONING_DIR.relative_to(REPO_ROOT)}")
        return 0

    results = []
    for kind, path in sorted(files, key=lambda x: str(x[1])):
        if kind == "bpc":
            r = validate_bpc_doc(path)
        else:
            r = validate_connection_doc(path)
        r["kind"] = kind
        results.append(r)

    skipped = sum(1 for r in results if r.get("skipped"))
    err_files = [r for r in results if not r.get("skipped") and r.get("errors")]
    warn_files = [r for r in results if not r.get("skipped") and r.get("warnings")]
    clean = [r for r in results if not r.get("skipped")
             and not r.get("errors") and not r.get("warnings")]

    if args.json:
        print(json.dumps({
            "checked": len(results),
            "skipped": skipped,
            "errors": len(err_files),
            "warnings": len(warn_files),
            "clean": len(clean),
            "results": results,
        }, indent=2))
    else:
        print(f"Reasoning-doc validation — {len(results)} docs checked\n")
        for r in results:
            if r.get("skipped"):
                continue
            tag = "ERROR" if r.get("errors") else ("WARN" if r.get("warnings") else "OK")
            rel = Path(r["file"]).relative_to(REPO_ROOT) if r["file"].startswith(str(REPO_ROOT)) else r["file"]
            print(f"  [{tag:<5}] {rel}")
            for e in r.get("errors", []):
                print(f"          ERROR: {e}")
            for w in r.get("warnings", []):
                print(f"          warn:  {w}")
        print(
            f"\nSummary: {len(clean)} clean, {len(warn_files)} with warnings, "
            f"{len(err_files)} with errors, {skipped} skipped (templates)"
        )

    if args.strict and err_files:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
