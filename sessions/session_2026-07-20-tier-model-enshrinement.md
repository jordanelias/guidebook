# Session — tier-model enshrinement (2026-07-20)

Branch: `claude/evidence-base-state-slug-lz8up0`

## Ask

Owner: "approve my decisions like tier model, keep working." Approves the tier-model recommendations laid out
across this session; proceed.

## Enshrined (DR-2026-07-20-weighted-strength-anchor-model.md; tier-system.md §8–§10)

1. **Weighted-strength anchor model** — supersedes §3's binary "best-practice claims require T1/Co-1/T2/Co-2."
   Every tier can anchor a claim; strength is weighted by tier, in three bands (the existing `●◐○`):
   ● full (T1/Co-1/T2/Co-2/T3-clinical), ◐ partial (T4/T5, "standards basis"), ○ weak (T3-grey/T6,
   "best available given current practice, not academically adjudicated"). Convergence-not-evidence retained
   as the weak-band honesty rule.
2. **Review-species (closes GAP-298)** — SR/meta = T2; scoping + narrative/literature reviews = T3
   (supporting, never `sr_meta`); rapid reviews case-by-case. Confirms PR #32's outcome and the REF-00589
   revert as correct.
3. **Practitioner practice-stream (closes GAP-299)** — firm/architect work placed by method, below Co-1/Co-2;
   role-appropriate-authority gate (can anchor descriptive/measured claims, not functional-need claims
   without Co-1/Co-2). Dedicated `practice`/Co-3 encoding defined; audit representation deferred to the audit
   rework.

## Applied (migration data_20260720135718)

- GAP-298 → CLOSED-DECIDED; GAP-299 created → CLOSED-DECIDED.
- **REF-00300** (HCMA + Rick Hansen Foundation *RHFAC Retrofits and Upgrades Cost Study*): T6 `code` → T3
  `grey` — empirical firm cost data, not statutory code. First practice-stream application.
- **7 unverifiable anchor sources → `verification_status='DISPUTED'`** (REF-00055, -00058, -00111, -00152,
  -00381, -00549, -00641) — flagged by the correctness sweep, adversarially upheld; VERIFIED standing stripped
  and anchor use suspended until re-sourced or retired. Not deleted. (REF-00045/-00140, merely
  unretrievable-this-session, left unchanged.)

`PRAGMA foreign_key_check` / `integrity_check` clean; audit regenerated.

## Follow-up (next steps, now unblocked by this DR)

- **Audit rework** (`tools/evidentiary_audit.py`) — report strength-band + weak-only flag instead of the
  binary `no-anchor` flag; exclude DISPUTED rows from anchor counts; encode the practice-stream.
- **Held sweep corrections** — ~44 tier/type reclassifications + 71 model-dependent defects (now unblocked),
  and ~76 author/title string corrections (reviewed batches).
- **English grey subset** (~24 rows); **extend correctness sweep to the full 779**.
