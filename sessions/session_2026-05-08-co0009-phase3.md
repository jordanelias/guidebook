# Session: 2026-05-08/09 — CO-0009 + C1 + C3 + Adversarial Research Protocol
**Model:** Opus 4.6
**session_close:** 2026-05-09
**next_action:** PI v10.6 update (owner action — add standing rule #7 for protocol). Then: address 14 OPEN gaps under protocol-compliant research, OR start Tier 1 multilingual remediation under protocol.
**blockers:** PI update requires owner action in claude.ai project knowledge.

## Key methodological turn (2026-05-09)

Owner challenged consensus-confirmation bias in my research. After review:
- v1 protocol I drafted had 7 steps, 5 of them performance theater
- v2 protocol has 5 enforceable outputs, DB-enforced via audit query
- v2 dropped: "trace to primary data" (circular), "adversarial query templates" (finds straw-men), "±20% test" (lacks data), "recency check" (same bias shifted)
- v2 kept: stated prior, population match grade, named dissenter, confidence interval, falsification condition

DR-2026-05-09 ADOPTED per owner directive "long-term integrity and health."

## Honest backfill exposed shallow closures

Of 9 research gaps closed earlier this session:
- 6 closures justified (populated with CI 50-85%, honest dissenter notes)
- 3 closures REOPENED as premature:
  - GAP-045 B-10: I wrote a 30-second DBL detection threshold without source — likely fabricated
  - GAP-083 A-14: Schroeder & Steinfeld 1979 citation not verified — may not exist
  - GAP-084 A-14: same citation problem
- All 4 prior backfills (GAP-019, GAP-008, GAP-040, GAP-076) showed honest CI of 30-70%, much lower than my closing tone implied

## Final state

**Tracking DB:**
- 264 gaps (14 OPEN, was 11 before honest re-evaluation)
- 87 audit runs
- 30 terms, 438 multilingual aliases (12 languages)
- 1134 search_languages rows, 1863 search_coverage rows
- evidence_population_match table: 0 rows (no population matching done yet — flag for new research)

**Website DB:**
- 91 real items (after dedup), 614 population links
- 9 of 11 atom fields at 100% real-item coverage
- 30/91 items SPECULATIVE-flagged

**New schema (DR-adopted):**
- evidence_sources: +derivation_chain, +prior_expectation, +search_queries_used
- gaps: +confidence_interval, +shift_conditions, +named_dissenter, +falsification_condition
- evidence_population_match: new table

**Enforcement:**
- Level 2: scripts/audit/research_protocol_audit.py (clean: 0 deficient closures)
- Level 3 promotion: deferred until Phase 1 hooks ship

## What's blocked / pending

| Item | Blocker |
|---|---|
| PI v10.6 standing rule #7 | Owner edit in claude.ai project knowledge |
| 3 reopened gaps (GAP-045, 083, 084) | Need protocol-compliant re-research |
| 7 unresearched OPEN gaps | Need protocol-compliant first research |
| 4 prior backfilled gaps | CI 30-70% — may need re-research at higher rigor |
| Multilingual remediation | Requires protocol — plan updated |
| diagram_svg field (0%) | SVG authoring (separate work type) |

## Honest summary

The protocol works by making my shallow research VISIBLE. The cost is that the OPEN gap count went UP (11 → 14) because honest evaluation reopened premature closures. This is the protocol working as designed.

The reviewer (you) is the truth-source. The protocol creates legible artifacts you can spot-check. Without spot-checks, the fields will become noise just like everything else.
