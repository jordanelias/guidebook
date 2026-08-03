#!/usr/bin/env python3
"""
scripts/audit/matrix_consistency.py — mechanical check that the mode × evidence-stratum
matrix in governance/evidence-architecture.md §3 matches schemas/directness.py.

Regenerates every grain × scale outcome (plus the generalizes-beyond-measured branch)
from scale_directness() and diffs against the expected outcomes the document states.
Exit 1 on any mismatch. Referenced by evidence-architecture.md §10 check 1.
"""
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

from schemas.directness import ALL_GRAINS, ALL_SCALES, scale_directness  # noqa: E402

# The §3/§10 doctrine table, transcribed. If doctrine changes, change BOTH the
# document and this table in the same commit — that is the point of the check.
EXPECTED = {
    ("aggregate", "population"): "DIRECT",
    ("aggregate", "person"): "DOWN-WEIGHTED",
    ("aggregate", "universal"): "ADJACENT",
    ("code", "universal"): "DIRECT",
    ("code", "population"): "NON-ANCHORING",
    ("code", "person"): "NON-ANCHORING",
    ("specific", "person"): "DIRECT",
    ("specific", "population"): "DIRECT",
    ("specific", "universal"): "ADJACENT",
}
EXPECTED_GENERALIZING = "DOWN-WEIGHTED"  # specific × population, generalizes_beyond_measured


def main():
    failures = []
    for grain in sorted(ALL_GRAINS):
        for scale in sorted(ALL_SCALES):
            got = scale_directness(grain, scale)
            want = EXPECTED.get((grain, scale))
            status = "OK" if got == want else "MISMATCH"
            if got != want:
                failures.append((grain, scale, want, got))
            print(f"  {grain:>10} × {scale:<11} doc={want:<14} code={got:<14} {status}")
    got = scale_directness("specific", "population", generalizes_beyond_measured=True)
    status = "OK" if got == EXPECTED_GENERALIZING else "MISMATCH"
    if got != EXPECTED_GENERALIZING:
        failures.append(("specific(generalizing)", "population", EXPECTED_GENERALIZING, got))
    print(f"  {'specific*':>10} × {'population':<11} doc={EXPECTED_GENERALIZING:<14} "
          f"code={got:<14} {status}   (*generalizes_beyond_measured)")
    if failures:
        print(f"\nFAIL: {len(failures)} doctrine/code mismatches")
        sys.exit(1)
    print(f"\nPASS: {len(EXPECTED) + 1}/{len(EXPECTED) + 1} outcomes match "
          f"evidence-architecture.md §3")


if __name__ == "__main__":
    main()
