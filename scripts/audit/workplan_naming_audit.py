#!/usr/bin/env python3
"""
scripts/audit/workplan_naming_audit.py — new workplans sort by date.

CLAUDE.md §9 tells every session how to find out where things stand: "sort
`workplan/`, `sessions/` and `audits/` by date and read the newest." That
instruction only works if the names carry the date in a position that sorts.
Today most of `workplan/` does not — `roadmap-2026-04-27.md`,
`a5-handoff.md`, `opus-synthesis-queue.md` — so a directory listing puts a
March file above an August one and a session following the documented procedure
reads a superseded plan. Several already have, which is why §9 warns that
"several dated workplans coexist" instead of naming the current one.

The convention (W4.3): `YYYY-MM-DD-slug.md` at the top level of `workplan/`.

FORWARD-ONLY, AND THAT IS A COMPROMISE, NOT A DESIGN.
The ~45 pre-convention names are GRANDFATHERED — listed in this file, checked for
existence, and not otherwise judged. Renaming them is a bulk file move, which
CLAUDE.md §9 guardrail 4 puts under owner sign-off, and the sweep would have to
repoint every caller (guardrail: a rename is not done until the caller sweep is).
So this check stops the problem GROWING and does not pretend to have solved it.
The grandfathered list is the backlog, in the open, with a count.

The list is checked for existence in both directions: an entry naming a file that
no longer exists is stale and reported, and a NEW file is anything on disk that is
neither conformant nor grandfathered. That is what makes the amnesty finite —
a list nobody validates becomes the place non-conformant names go to be forgiven.

Subdirectories (`_superseded/`, `deprecated/`) are out of scope: they are cold
storage, hidden from search by `.ignore`, and renaming a retired file buys
nothing.

Exit 0 when every new top-level workplan is dated, 1 otherwise.

Usage:
    python3 scripts/audit/workplan_naming_audit.py
    python3 scripts/audit/workplan_naming_audit.py --list-grandfathered
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
WORKPLAN = REPO / "workplan"

CONVENTION = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# Files predating the convention, captured 2026-08-06. Do not add to this list to
# make a new file pass — that is the one thing it must not become. Entries leave
# it only by being renamed or retired.
GRANDFATHERED = {
    "P1-D2-D3-co0004-remapping.md",
    "a1-a2-iteration-plan.md",
    "a4-part01-audit-2026-04-27.md",
    "a5-handoff.md",
    "a6-handoff.md",
    "adherence-attestation-build-2026-05-17.md",
    "b1-candidate-a-markdown-yaml.md",
    "b1-candidate-b-relational.md",
    "b1-candidate-c-graph.md",
    "b1-candidate-d-hybrid.md",
    "b1-comparative-scoring.md",
    "b1-criteria-weighting.md",
    "b1-derivation-framework.md",
    "best-practices-assessment-system.md",
    "bpc-rewrite-workplan-2026-05-11.md",
    "category-E-clean-room-evidence-synthesis-2026-07-23.md",
    "co0008-scope-infrastructure-overhaul.md",
    "co0008-throughline-analysis.md",
    "co0009-phase0-handoff.md",
    "comprehensive-plan-2026-08-02.md",
    "consolidation-execution-plan-2026-07-21.md",
    "coverage-completion-loop-methodology-2026-07-21.md",
    "coverage-loop-routine-instructions-corrected-2026-07-24.md",
    "de-grade-remediation-and-coverage-extension-2026-07-21.md",
    "dedup-audit-same-doi-multi-refid-2026-07-21.md",
    "economics-audit-research-2026-05-03.md",
    "evidence-expansion-2026-04-03.md",
    "evidentiary-base-research-plan-2026-07-19.md",
    "external-review-outreach-drafts.md",
    "external-review-queue.md",
    "gap-p1-reclassification-recommendation.md",
    "methodology-and-pipeline-enforcement-plan-2026-07-23.md",
    "multilingual-search-remediation.md",
    "next-steps-synthesis-2026-07-14.md",
    "opa-adjudication.md",
    "opb-adjudication.md",
    "opg-methodology-review.md",
    "opus-missing-passes.md",
    "opus-synthesis-queue.md",
    "phase-e-execution-log-2026-07-14.md",
    "phase-e-execution-plan-v1.md",
    "phase1b-part01-s15-expansion.md",
    "placeholder-review-triage.md",
    "progressive-measurement-protocol.md",
    "ratification-execution-register-2026-07-13.md",
    "ratification-execution-register-2026-07-21.md",
    "research-matrix-completion-execution-plan-2026-07-24.md",
    "research-protocol-adversarial.md",
    "roadmap-2026-04-27.md",
    "search-coverage-completion-workplan.md",
    "slug-triage-2026-03-28.md",
    "struck-claim-research-attempt_2026-05-01.md",
    "website-preparation.md",
    "website-v0-path-forward-2026-07-12.md",
    "workplan-item-audit-pipeline-co0009.md",
    "workplan-jurisdiction-sweep.md",
    "workplan-reconciliation-2026-05-08.md",
}


def audit():
    present = {p.name for p in WORKPLAN.glob("*.md")}
    conformant = sorted(n for n in present if CONVENTION.match(n))
    offenders = sorted(present - set(conformant) - GRANDFATHERED)
    stale = sorted(GRANDFATHERED - present)
    return conformant, offenders, stale


def main():
    if "--list-grandfathered" in sys.argv:
        for name in sorted(GRANDFATHERED):
            print(name)
        return 0

    if not WORKPLAN.is_dir():
        print(f"ERROR: {WORKPLAN} is not a directory", file=sys.stderr)
        return 1

    conformant, offenders, stale = audit()
    remaining = len(GRANDFATHERED) - len(stale)

    print("=" * 70)
    print("workplan_naming_audit.py — YYYY-MM-DD-slug.md at workplan/ top level")
    print("=" * 70)
    print(f"  EXAMINED: {len(conformant) + len(offenders) + remaining} top-level workplan(s)")
    print(f"  conformant:    {len(conformant)}")
    print(f"  grandfathered: {remaining}  (pre-convention; bulk rename is owner-gated)")

    if stale:
        print()
        for name in stale:
            print(f"  STALE   grandfathered entry {name!r} no longer exists — "
                  f"drop it from GRANDFATHERED")

    if offenders:
        print()
        for name in offenders:
            print(f"  FAIL    {name} — not dated, and not on the grandfathered list")
        print()
        print("Rename to YYYY-MM-DD-slug.md. CLAUDE.md §9 tells sessions to find the "
              "current plan by sorting this directory by date; a name that does not "
              "sort sends them to a superseded one. Do NOT add it to GRANDFATHERED — "
              "that list is a closed record of what predates the convention, not a "
              "waiver queue.")
        return 1

    print()
    print(f"RESULTS: {len(conformant)} conformant, {remaining} grandfathered, "
          f"0 new offenders")
    return 0


if __name__ == "__main__":
    sys.exit(main())
