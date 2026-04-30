#!/usr/bin/env python3
"""
scripts/decision_capture.py — Decision-register validator (per governance/decision-protocol.md, A12).

Eight checks per §7.3:
  C1 register well-formed: data/decisions/decision_register.yaml validates as DecisionRegister
  C2 unique decision_ids (covered at schema level; surfaced here for clarity)
  C3 rationale length compliant: §3.3 norms (warning, not error)
  C4 model-routing format (covered at schema level; surfaced here)
  C5 supersedes consistency (covered at schema level; surfaced here)
  C6 rationale anti-pattern: §3.4 patterns (warning)
  C7 RULE coverage: every CANONICAL RULE in project-standards has at least one Decision (warning)
  C8 review_status consistency (covered at schema level; surfaced here)

Usage:
    python3 scripts/decision_capture.py                       # full audit
    python3 scripts/decision_capture.py --register-only       # skip C7
    python3 scripts/decision_capture.py --decision-id D-0042  # single record
    python3 scripts/decision_capture.py --report              # exit 0

Exit codes: 0 = pass, 1 = errors, 2 = config error.
"""

import argparse
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.decision import DecisionRegister, Decision

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER_PATH = os.path.join(REPO_ROOT, "data", "decisions", "decision_register.yaml")
PROJECT_STANDARDS_PATH = os.path.join(REPO_ROOT, "references", "project-standards.md")

# Per §3.3 rationale length norms, sentence count
RATIONALE_NORMS = {
    "D-DOCT":   (3, 10),
    "D-METH":   (2, 5),
    "D-SCHEMA": (1, 3),
    "D-OP":     (1, 1),
    "D-PRES":   (1, 2),
}

# §3.4 anti-patterns (regex against rationale text)
ANTI_PATTERN_TAUTOLOGY = re.compile(
    r"^\s*(chose|adopted|selected|decided)\s+\S+\s+because\s+\S+\s+is\s+the\s+(right|correct|best)\s+choice",
    re.IGNORECASE,
)
ANTI_PATTERN_AUTHORITY = re.compile(
    r"^\s*(chose|adopted|selected|decided)\s+\S+\s+because\s+the\s+spec\s+says\s+\S+\s*\.?\s*$",
    re.IGNORECASE,
)


def count_sentences(text: str) -> int:
    """Approximate sentence count: split on . ! ? followed by space or EOL."""
    sentences = [s.strip() for s in re.split(r"[.!?]+(?:\s+|$)", text) if s.strip()]
    return len(sentences)


# --- C1 + C2 + C4 + C5 + C8: register loads + schema validates ---

def check_register() -> tuple[list[str], list[str], DecisionRegister | None]:
    errors: list[str] = []
    warnings: list[str] = []

    if not os.path.exists(REGISTER_PATH):
        errors.append(
            f"C1: register missing at {os.path.relpath(REGISTER_PATH, REPO_ROOT)}"
        )
        return errors, warnings, None

    try:
        register = DecisionRegister.from_yaml(REGISTER_PATH)
    except Exception as e:
        errors.append(f"C1: register does not validate: {e}")
        return errors, warnings, None

    # Soft observability
    if not register.decisions:
        warnings.append(
            "C1: register loaded but is empty; A12 Session 2 will seed it"
        )

    return errors, warnings, register


# --- C3: rationale length norms (warnings) ---

def check_rationale_lengths(register: DecisionRegister) -> list[str]:
    warnings: list[str] = []
    for d in register.decisions:
        cat = d.category if isinstance(d.category, str) else d.category.value
        if cat not in RATIONALE_NORMS:
            continue
        lo, hi = RATIONALE_NORMS[cat]
        n = count_sentences(d.rationale)
        if n < lo:
            warnings.append(
                f"C3 {d.decision_id}: rationale has {n} sentence(s); category {cat} norm is {lo}-{hi}"
            )
        # Above norm is acceptable per §3.3
    return warnings


# --- C6: rationale anti-patterns (warnings) ---

def check_rationale_antipatterns(register: DecisionRegister) -> list[str]:
    warnings: list[str] = []
    for d in register.decisions:
        rat = d.rationale.strip()
        if ANTI_PATTERN_TAUTOLOGY.match(rat):
            warnings.append(
                f"C6 {d.decision_id}: rationale matches tautology anti-pattern (§3.4)"
            )
        if ANTI_PATTERN_AUTHORITY.match(rat):
            warnings.append(
                f"C6 {d.decision_id}: rationale matches authority-without-content anti-pattern (§3.4)"
            )
        # Outcome-as-rationale: rationale is a near-substring of outcome
        outcome = d.outcome.strip().lower()
        rat_lower = rat.lower()
        if outcome and (rat_lower == outcome or rat_lower == f"{outcome}."):
            warnings.append(
                f"C6 {d.decision_id}: rationale is identical to outcome (§3.4 outcome-as-rationale)"
            )
    return warnings


# --- C7: project-standards RULE coverage (post-seeding warning) ---

def extract_canonical_rules(text: str) -> list[str]:
    """Extract RULE blocks marked CANONICAL from project-standards.md.

    Returns a list of RULE summaries — first sentence of each CANONICAL rule.
    """
    canonical = []
    lines = text.split("\n")
    current_rule = None
    for line in lines:
        if line.startswith("RULE:"):
            current_rule = line[len("RULE:"):].strip()
        elif current_rule and "CANONICAL" in current_rule:
            # Take the first sentence as the summary
            summary = current_rule.split(". ", 1)[0]
            canonical.append(summary[:120])
            current_rule = None
        elif line.startswith("DATE:") or line.strip() == "":
            current_rule = None
    return canonical


def check_rule_coverage(register: DecisionRegister) -> list[str]:
    warnings: list[str] = []
    if not os.path.exists(PROJECT_STANDARDS_PATH):
        warnings.append(
            f"C7: project-standards.md missing at "
            f"{os.path.relpath(PROJECT_STANDARDS_PATH, REPO_ROOT)}"
        )
        return warnings

    with open(PROJECT_STANDARDS_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    canonical_rules = extract_canonical_rules(text)

    # Heuristic: any decision_artifacts entry mentioning the rule's keyword
    # counts as coverage. This is intentionally loose pre-seeding; A12 Session 2
    # tightens it after seeding.
    if not register.decisions:
        warnings.append(
            f"C7: register is empty; {len(canonical_rules)} CANONICAL rules in "
            f"project-standards await seeding (per §5.3)"
        )
        return warnings

    # Check whether each CANONICAL rule has at least one decision artifact
    # referencing it. Match on substring of the artifact path.
    covered_count = 0
    for rule_summary in canonical_rules:
        # Attempt to extract a governance-doc path from the rule summary
        m = re.search(r"governance/[\w\-]+\.md", rule_summary)
        if not m:
            continue
        rule_path = m.group(0)
        for d in register.decisions:
            if any(rule_path in art for art in d.decision_artifacts):
                covered_count += 1
                break

    uncovered = len(canonical_rules) - covered_count
    if uncovered > 0:
        warnings.append(
            f"C7: {uncovered} of {len(canonical_rules)} CANONICAL rules have no "
            f"matching Decision record (heuristic: governance/*.md path in "
            f"decision_artifacts). Run seeding extraction per A12 Session 2."
        )

    return warnings


# --- Main ---

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--register-only", action="store_true",
                    help="run C1-C6/C8; skip C7 (RULE coverage)")
    ap.add_argument("--decision-id", default=None,
                    help="audit a single decision_id (e.g., D-0042)")
    ap.add_argument("--report", action="store_true",
                    help="print summary; exit 0 always")
    args = ap.parse_args()

    all_errors: list[str] = []
    all_warnings: list[str] = []

    e1, w1, register = check_register()
    all_errors.extend(e1)
    all_warnings.extend(w1)

    if register and args.decision_id:
        # Restrict to one decision
        register.decisions = [
            d for d in register.decisions if d.decision_id == args.decision_id
        ]
        if not register.decisions:
            all_errors.append(
                f"--decision-id {args.decision_id} not found in register"
            )

    if register and register.decisions:
        all_warnings.extend(check_rationale_lengths(register))
        all_warnings.extend(check_rationale_antipatterns(register))
        if not args.register_only and not args.decision_id:
            all_warnings.extend(check_rule_coverage(register))

    # Report
    if register:
        active = sum(
            1 for d in register.decisions
            if (d.status if isinstance(d.status, str) else d.status.value) == "ACTIVE"
        )
        superseded = sum(
            1 for d in register.decisions
            if (d.status if isinstance(d.status, str) else d.status.value) == "SUPERSEDED"
        )
        retired = sum(
            1 for d in register.decisions
            if (d.status if isinstance(d.status, str) else d.status.value) == "RETIRED"
        )
        print(
            f"Decision-capture audit: register v{register.register_version} — "
            f"{active} ACTIVE / {superseded} SUPERSEDED / {retired} RETIRED"
        )
    else:
        print("Decision-capture audit: register not loaded")

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
