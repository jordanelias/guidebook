# §3.8 Decision Tree Validation — Compound Scenario Tests
**Date:** 2026-04-09 05:25
**Status:** VALIDATED — no structural changes required

## Test Results

| Test | Scenario | Expected routing | Actual routing | Verdict |
|---|---|---|---|---|
| 1 | CMP-01: hemiplegia + chronic pain → transfer | Tier 2 EXIT (antagonistic) | Tier 2 EXIT | PASS |
| 2 | CMP-04: dementia + visual impairment → wayfinding | Tier 2 EXIT (antagonistic, spec limit) | Tier 2 EXIT | PASS |
| 3 | CMP-06: spasticity + orthostatic → sit-to-stand | No routing (convergence) | Variable conflation check → convergent, no routing | PASS |

## Findings

Step 0 correctly distinguishes three outcomes:
1. **True compound conflict** (non-additive antagonistic interaction) → Tier 2 EXIT with documented mechanism
2. **Specification limit** (no environmental specification can resolve) → Tier 2 EXIT + scope flag
3. **False conflict / convergence** (specifications align through different mechanisms) → Proceed normally or specify convergent requirement

No amendments to decision tree structure needed. Step 0 variable conflation check and compound functioning check operate as designed.

## Edge Case Identified

CMP-01 Test 1 revealed a subtlety: the variable conflation check found different variables (bar position vs approach angle), but these operate on the same physical action (the transfer). The compound check correctly caught this because it tests the *functional interaction*, not the *variable identity*. This confirms that Step 0's two-stage design is correct — variable conflation check alone would miss action-level interactions.
