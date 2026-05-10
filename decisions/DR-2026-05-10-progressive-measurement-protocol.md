# Decision Record: Adopt Progressive Measurement Probe (PMP) Protocol
**Date:** 2026-05-10
**Status:** ADOPTED 2026-05-10 — owner directive: "proceed" (session 2026-05-10c)
**Supersedes:** Partially overturns DR-2026-05-09 §"What Was Dropped From v1" — specifically the deletion of the "±20% threshold test." Reinstates the concept under a corrected design.

## Context

DR-2026-05-09 adopted the adversarial-research protocol v2 and explicitly dropped four v1 steps including a "±20% threshold test" with the rationale "requires dose-response data Claude doesn't have access to."

Session 2026-05-10c surfaced the loss while the owner was directing resumption of multilingual remediation across BPC slugs. Owner asked: "don't we have a protocol where we do searches with progressively [harsher] numbers for measurements to check?" — describing iterative walk-up testing of specification values such as 1500 → 1600 → 1700 mm turning radius until evidence stops.

Two findings:
1. The static ±20% bracket was correctly identified as inadequate: a fixed bracket cannot map an empirical ceiling lying outside it.
2. The dropped-rationale conflated dose-response sensitivity (clinical, dose-keyed) with specification-value validation (does any peer-reviewed source validate this number for this population). The latter does not require dose-response data — it requires literature search at the specific value.

The owner's correction — "20% threshold isn't adequate UNLESS it continually updates to the newest higher value" — is the missing design feature. Iterative re-centering at the latest-supported value, not a static bracket, is what discovers the empirical boundary.

## Decision

Adopt the Progressive Measurement Probe (PMP) protocol as governance for all BPC items asserting numerical specifications. Full spec: `workplan/progressive-measurement-protocol.md`.

## Design choices locked (per session 2026-05-10c owner directive)

1. **Increment rule: 1c (hybrid)** — proportional 20% per step in outer phase; linear δ_min refinement near the boundary. Owner-selected over linear-only and proportional-only.
2. **Termination criterion: 2bc (strict + alt-phrasing)** — a value is unsupported only when (b) no peer-reviewed source specifically validates it for the target population AND (c) two independently-phrased searches both fail. Both conditions must hold; (b) alone is insufficient because a single search might miss known literature; (c) alone is insufficient because topic-mention does not constitute claim-validation (PI standing rule #7 anti-pattern).
3. **Direction (D)** — fixed per item, logged at invocation. Reference table in workplan §"D reference table." Determining D mid-walk is forbidden — mistakes compound.
4. **Scope** — numerical specs only. Qualitative claims (e.g., "user control is the primary design variable") run adversarial-research alone.
5. **Multilingual scope** — PMP runs once per item in EN by default; target-language probes are evidence-driven add-ons, not symmetric defaults. Without this rule, fan-out is combinatorially ruinous.

## Why this does not contradict DR-2026-05-09

DR-2026-05-09 dropped the v1 step on a stated rationale that, on review, was wrong. It is not a precedent overruled — it is a rationale corrected. The original drop logic ("requires dose-response data") still applies to dose-response testing; PMP does not test dose-response. PMP tests specification-value support in the published literature, which is search-tractable.

## Schema changes (migration 006)

```sql
CREATE TABLE spec_value_probes (
  probe_id TEXT PRIMARY KEY,
  walk_id TEXT NOT NULL,           -- groups all steps of one walk
  slug TEXT NOT NULL,
  item_code TEXT NOT NULL,
  spec_value_origin REAL NOT NULL,
  spec_unit TEXT NOT NULL,
  direction TEXT NOT NULL CHECK (direction IN ('up','down')),
  population TEXT NOT NULL,
  claim_type TEXT NOT NULL CHECK (claim_type IN ('minimum','maximum','target','range_low','range_high')),
  step_index INTEGER NOT NULL,
  phase TEXT NOT NULL,
  step_value REAL NOT NULL,
  step_value_unit TEXT NOT NULL,
  search_query TEXT,
  search_query_alt TEXT,
  passes_strict INTEGER,
  ref_id TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  created_by_session TEXT NOT NULL,
  FOREIGN KEY (item_code) REFERENCES items (item_code),
  FOREIGN KEY (ref_id) REFERENCES evidence_sources (ref_id)
);

ALTER TABLE items ADD COLUMN pmp_delta_min REAL;
ALTER TABLE items ADD COLUMN pmp_direction TEXT;
ALTER TABLE items ADD COLUMN pmp_last_walk_at TEXT;
ALTER TABLE items ADD COLUMN pmp_empirical_ceiling REAL;
ALTER TABLE items ADD COLUMN pmp_gap_signed REAL;
```

Full migration: `scripts/migrations/006_spec_value_probes.sql`.

## Enforcement level

Default: **Level 2** (audit query at `scripts/audit/pmp_audit.py`). Matches adversarial-research enforcement. Promotion to level 3 (pre-commit hook) requires Phase 1 hooks to ship first per `hook-workplan-guidebook.md`.

## What this won't fix

Acknowledged in workplan. Summary:
- Claude can fabricate step-pass citations. Audit C3 (passes_strict=1 with NULL ref_id) and human spot-check are the safeguards.
- δ_min defaults are judgment calls. Wrong defaults produce false termination.
- Alt-phrasing rule is bypassable by near-synonymous phrasings. Per-session human spot-check of one walk is mitigation.
- The reviewer is the truth-source.

## Honest test (this session, no execution yet)

Worked example for A-08 (NC-25 maximum, sensitive spaces) sketched in workplan. Hypothesis stated before any walk: empirical floor between NC-15 and NC-20. This is the prior expectation per adversarial protocol, logged in advance to expose confirmation bias if the walk happens to land exactly on the prior. First actual execution will produce the test — a result of NC-15 or NC-20 with strong evidence will be a flag, not confirmation.

## Open items

- [x] Owner sign-off on this DR (received 2026-05-10, session 2026-05-10c, directive: "proceed")
- [x] Run migration 006 (commit 6fbb90f1, schema_version 5→6, applied 2026-05-10)
- [ ] Stage B: write `skills/progressive-measurement_SKILL.md`
- [ ] Stage B: PI v10.7 standing rule #8 invoking PMP for numerical specs
- [ ] Stage C: first execution on slug 3 A-02 (NRC ≥0.85, D=up) and A-08 (NC-25, D=down)
- [ ] [GAP: items.bpc_source_slug is NULL for A-02 and A-08 — explicit linkage to slug=school-environment-autism is missing in DB; resolve before or during Stage C]
- [ ] [GAP: handoff document says A-02=RT60 but items DB shows A-02=NRC ≥0.85 — verify which is authoritative; may indicate a separate stale-handoff issue]
- [ ] Backfill plan for prior numerically-specified BPC closures (after Stage C calibrates effort)

## Related

- `workplan/progressive-measurement-protocol.md` — full spec
- `decisions/DR-2026-05-09-adversarial-research-protocol.md` — companion DR; partially superseded by this one (rationale only, not protocol)
- `workplan/research-protocol-adversarial.md` — companion protocol
- `workplan/multilingual-search-remediation.md` — execution context
- `scripts/migrations/006_spec_value_probes.sql` — schema migration
