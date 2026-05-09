# Decision Record: Adopt Adversarial Research Protocol v2
**Date:** 2026-05-09
**Status:** PROPOSED — pending owner sign-off
**Supersedes:** None

## Context

Session 2026-05-09 surfaced a methodological problem: Claude's research mode defaults to consensus confirmation. Specific failures identified:
- Found "supporting" evidence for ramp 1:20, door force 22N, hearing loops
- Did not search for contradictory evidence
- Did not verify cited study populations matched guidebook target populations
- Did not trace threshold values to primary data
- May have generated plausible-sounding citations rather than retrieving them

Owner challenged: "How do we stop you from pattern matching, defaulting to training data, opting for consensus?"

## Decision

Adopt research protocol v2 (`workplan/research-protocol-adversarial.md`) as governance for all research-generating gap closures.

## What v2 Requires

Every gap closure that involves research must populate five fields:
1. `evidence_sources.prior_expectation` — what Claude expected before searching
2. `evidence_population_match.match_grade` — EXACT/PARTIAL/PROXY/MISMATCH per cited study
3. `gaps.named_dissenter` — specific contrary view OR "NONE FOUND" with logged queries
4. `gaps.confidence_interval` — numerical range with shift conditions
5. `gaps.falsification_condition` — specific finding that would invalidate

## What Was Dropped From v1

- "Trace to primary data" (circular — Claude can't critically evaluate citation chains)
- "Adversarial search queries" (performance theater — finds straw-men)
- "±20% threshold test" (requires data Claude lacks access to)
- "Recency check" (same bias shifted)

## Schema Changes Applied (2026-05-09)

```sql
ALTER TABLE evidence_sources ADD COLUMN derivation_chain TEXT;
ALTER TABLE evidence_sources ADD COLUMN prior_expectation TEXT;
ALTER TABLE evidence_sources ADD COLUMN search_queries_used TEXT;
ALTER TABLE gaps ADD COLUMN falsification_condition TEXT;
ALTER TABLE gaps ADD COLUMN confidence_interval TEXT;
ALTER TABLE gaps ADD COLUMN shift_conditions TEXT;
ALTER TABLE gaps ADD COLUMN named_dissenter TEXT;
CREATE TABLE evidence_population_match (...);
```

## Backfill Test (Honest)

Backfilled 4 recent RP gap closures (E-03 ramp, I-01 force, B-10 alarm, A-12 Auracast). Findings:
- Honest confidence intervals: 30–70% (much lower than my closing tone implied)
- 3 of 4 dissenter entries: "NONE FOUND — but no adversarial search conducted"
- 1 admitted citation may be fabricated (Chaffin grip force example I cited in protocol v1)

The backfill is the protocol's first finding: shallow research is now visible.

## Enforcement Level

Currently level 1 (text). Promotion path:
- Level 2: scheduled audit query that flags closed gaps without protocol fields
- Level 3: pre-commit hook blocks commits closing gaps without all 4 fields
- Level 4: code hook with RuntimeError if closed gap lacks fields

Ship at level 2 first, calibrate, promote to level 3 if false-positive rate is acceptable.

## Human Spot-Check Schedule

Per session: 1 random gap, "trace this to primary data" + "what would change your mind"
Per 10 sessions: audit population_match grade distribution; pick 3 NONE FOUND entries for re-search
Per 50 sessions: external domain expert review of 5 closed gaps

## What This Doesn't Solve

Acknowledged in protocol document. Summary:
- Claude can fabricate citations (named-dissenter requirement helps but doesn't prevent)
- Confidence intervals can be miscalibrated
- Match grades depend on rubric application which is itself biased
- The reviewer is the truth-source; protocol creates legible artifacts only

## Open Items

- [ ] Owner sign-off
- [ ] Decide enforcement level (2 vs 3)
- [ ] Decide spot-check responsibility
- [ ] Update PI v10.5 standing rules to reference protocol
- [ ] Update userPreferences `<accuracy_and_uncertainty>` to reference protocol for research tasks
- [ ] Backfill remaining 22 research gaps to protocol fields (estimated 2-3 sessions)

## Related

- `workplan/research-protocol-adversarial.md` — full protocol v2
- `workplan/multilingual-search-remediation.md` — research execution plan that should adopt this protocol
- v1 protocol → v2 supersession in same file (commit 806b50c)
