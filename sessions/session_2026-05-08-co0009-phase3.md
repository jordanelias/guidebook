# Session: 2026-05-08/09 — CO-0009 + C1 + C3 + Adversarial Research Protocol Implementation
**Model:** Opus 4.6
**session_close:** 2026-05-09
**next_action:** PI v10.6 update (owner action — add standing rule #7 referencing adversarial-research_SKILL.md). Then: continue protocol-compliant verification of remaining 4 prior backfills (GAP-040, GAP-076, GAP-097, GAP-260 still have shallow research notes), OR begin Tier 1 multilingual remediation under protocol.
**blockers:** PI update requires owner action in claude.ai project knowledge.

## What this session built (cumulative)

### Infrastructure (CO-0009 + C1)
- CO-0009 pipeline: COMPLETE
- C1 migration: COMPLETE (both DBs)
- C3 calibration: COMPLETE (0.50 median, budget 184–296)
- C3 pre-pass: 86/86 items audited
- 9 of 11 atom fields at 100% real-item coverage
- 91 items × 525 population links across both DBs

### Methodological (Adversarial Research Protocol)
- DR-2026-05-09 ADOPTED
- 7 schema fields + 1 new table (`evidence_population_match`)
- Audit script at scripts/audit/research_protocol_audit.py (level 2)
- adversarial-research_SKILL.md (skill file for portability across sessions)
- Multilingual remediation plan updated to require protocol fields
- v2 protocol replaced v1 (dropped 4 performance-theater steps)

### What the protocol caught (its first deployment)

FOUR fabrications:
1. "Yang et al." standalone with 2.09× force figure — Yang is real co-author on Koontz 2005, no standalone study
2. "Japanese cervical SCI normalized power 0.23-0.26 W/kg" — not located
3. "Chaffin et al. 2006" RA grip force — used as example IN protocol v1, protocol caught its own fabrication
4. "30 second" DBL alarm detection threshold — confirmed fabricated against NFPA 72

ONE silent bug:
- INSERT OR IGNORE hid evidence_sources schema mismatch
- Audit query exposed: "0 verified citations" after I claimed 4 in commits
- Each enforcement layer catches different failure modes

SIX verified citations now in evidence_sources with full protocol fields:
- REF-VERIFIED-001: Schroeder & Steinfeld 1979 (HUD)
- REF-VERIFIED-002: Koontz et al. 2005 (PMID 16320141)
- REF-VERIFIED-003: Lalumiere 2022 systematic review (PLOS One)
- REF-VERIFIED-004: Björk et al. 1997 (PMID 9021280)
- REF-VERIFIED-005: IEC 60118-4 Ed 3.0 2014
- REF-VERIFIED-006: ISO 23599:2019

5 population_match records (2 EXACT for standards, 2 PARTIAL, 1 PROXY).

## Final state

| Domain | Metric |
|---|---|
| Gaps logged | 263 (in addition to 1 systemic at GAP-264) |
| Gaps OPEN | 13 (was 11; reopened 3 prematures, 1 reversed → +2 net) |
| Gaps resolved | 253 (96.2%) |
| 30/91 items SPECULATIVE-flagged in failures_json | |
| Multilingual coverage logged | 1134 search_languages + 1863 search_coverage rows |
| Terms + aliases | 30 terms × 12 languages × 438 aliases |
| Verified citations with protocol fields | 6 |
| Population matches | 5 (2 EXACT, 2 PARTIAL, 1 PROXY) |
| Audit deficiencies | 0 |
| Commits | ~55 |

## Honest assessment

The protocol works by making shallow research VISIBLE, not by making me adversarial. The cost is that OPEN gap count went UP (11 → 13) because honest evaluation reopened premature closures. This is correct.

Of 11 closures attempted in this session that involved research:
- 6 closures justified after verification (citations real, populations matched, gaps remain CLOSED with full protocol fields)
- 3 closures REOPENED as premature (citations unverifiable or thresholds fabricated)
- 2 closures had shallow research that was then improved through verification round

The reviewer (you) is the truth-source. The DB schema, audit query, and skill file are layers that make different kinds of failure visible. None of them are fully self-enforcing.

## Pending owner actions

| Item | Action |
|---|---|
| PI v10.6 update | Add standing rule #7 referencing skill file (cannot be edited from repo) |
| Spot-check schedule | Decide who reviews what when |
| Enforcement promotion | Level 2 (audit) → Level 3 (pre-commit) once Phase 1 hooks ship |
| Tier 1 multilingual remediation | 8 SPECULATIVE slugs × multiple languages, 3-5 sessions estimated |

The protocol is the most important artifact of this session. Everything else is data work that can be redone; the methodological correction is the durable change.
