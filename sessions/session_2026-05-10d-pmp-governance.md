# Session: PMP governance + audit integrity + Stage B.5
**session_start:** 2026-05-10 19:00 UTC
**session_close:** 2026-05-10 19:57 UTC
**PI version:** v10.6 → v10.7 (shipped this session)
**workplan:** workplan-co0007-v4.md + progressive-measurement-protocol.md (new)

## Summary

Rebuilt the Progressive Measurement Probe (PMP) protocol from a compaction-lost concept. Original was the v1 "±20% threshold test" dropped at DR-2026-05-09 adoption — user identified iterative re-centering as the missing design feature that makes it work. Full governance chain shipped: workplan, DR, migration 006, skill file, PI v10.7 with standing rule #8, skill-registry update.

User-directed audit of logs and tables surfaced 6 findings, 4 critical. Stage B.5 executed to fix: backfilled slug 2 evidence sources, added protocol-compliance markers to search_languages, strengthened audit script with 3 new checks (prior_expectation, search_queries_used, PROTOCOL: marker). Filed 2 gaps for pre-existing data quality issues.

## Commits (12 total)

| SHA | Stage | Content |
|---|---|---|
| 1b51b356 | A | workplan/progressive-measurement-protocol.md |
| 502e28af | A | decisions/DR-2026-05-10 (initially PROPOSED) |
| 23f8e973 | A | scripts/migrations/006_spec_value_probes.sql |
| 6fbb90f1 | migrate | data/guidebook.db schema v5→v6 |
| 6db36cb1 | B | DR-2026-05-10 → ADOPTED |
| 12adb610 | B | skills/progressive-measurement_SKILL.md |
| 89bd0791 | B | governance/project-instructions-v10_7.md (PAT redacted) |
| e70a41c1 | B | references/skill-registry.md (44 total, 28 active) |
| 5f50ecae | B.5 | data/guidebook.db (backfill + markers + GAP-281/282) |
| b7ad029c | B.5 | scripts/audit/research_protocol_audit.py (CHECK 7-9) |

## Audit findings (6 total, 4 fixed in B.5)

| # | Severity | Finding | Status |
|---|---|---|---|
| A | was-blocking | 5 evidence sources (REF-00700–704) missing prior_expectation | FIXED (backfilled with [BACKFILL] tag) |
| B | was-blocking | 14 slug-2 + 397 legacy search_languages lacked PROTOCOL: marker | FIXED (10 FULL, 401 PRE-REMEDIATION, 543 NOT-RUN) |
| C | instrument | audit script had 6 checks; missed evidence_sources protocol fields entirely | FIXED (9 checks, all pass) |
| D | P2 systemic | bpc_source_slug NULL across all 91 items | FILED as GAP-281; separate fix path |
| E | P3 stale | A-02 = NRC ≥0.85, not RT60; missing RT60-school item | FILED as GAP-282 |
| F | informational | PMP backlog ≥11 items (name-visible specs only) | Stage C will begin addressing |

## Owner action required

1. **Update live PI to v10.7.** The repo copy at `governance/project-instructions-v10_7.md` (commit 89bd0791) has the PAT redacted for GitHub secret-scanning. Copy to project settings and restore the inline PAT from v10.6.

## next_action

**Stage C: execute slug 3 with both protocols.**

Scope:
- PMP walk A-08 (NC-25, D=down) — prove PMP protocol end-to-end
- PMP walk A-02 (NRC ≥0.85, D=up) — second walk
- Adversarial per-language for 13 non-EN languages on slug 3 (queries prepped in handoff session_2026-05-10c)
- Adversarial angles documented: (1) factors other than noise/visual, (2) TEACCH structured environment contested, (3) inclusive vs autism-specific design, (4) building code gap confirmation, (5) Simpson 2025 methodology

Prerequisites all met:
- Schema v6 live with spec_value_probes table
- Audit script strengthened (run before session close per DR-2026-05-09 + B.5)
- research-log-manager CHECK required before first search (standing rule #4)
- Compliance markers in place; new work will be FULL from the start

Search query pairs per language: see handoff from session_2026-05-10c (the earlier session file). All 13 standard + adversarial query pairs are written out.

## blockers

- GAP-281 (bpc_source_slug NULL) — does NOT block Stage C execution but blocks any programmatic item→slug join; Stage C uses manual item lookups instead
- GAP-282 (missing RT60-school item) — does NOT block Stage C; PMP walks A-02 and A-08 as they currently exist; Simpson 2025's RT60 claim may need its own item later
- PI v10.7 live update — if not done before next session, bootstrap runs with v10.6 which lacks standing rule #8 (PMP); adversarial protocol still runs under rule #7 so work isn't blocked, but PMP walks would proceed under workplan authority only, not PI-enforced
