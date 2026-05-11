# Session: BPC rewrite workplan design (8-phase audit + governance deliverable)
**session_start:** 2026-05-11 04:30 UTC (approx, continued from prior wayfinding session)
**session_close:** 2026-05-11 06:00 UTC
**PI version:** v10.6
**Workplan governance:** workplan-co0007-v4 ACTIVE (Stage C1–C11) + this session produced a parallel proposed governance workplan (`audits/bpc-rewrite-workplan-2026-05-11.md`) requiring user adoption decision before next session

---

## Summary

User commissioned an 8-phase audit of the BPC/connections/evidence/synthesis system after exposing that this session's Tier 2 multilingual remediation work was producing synthesis claims on a foundation of unverified evidence. Audit executed all 8 phases; produced a 494-line proposed workplan to rewrite every BPC and connection with full per-document reasoning transparency.

**Key conceptual deliverable:** a locked 9-step operational rule for cross-jurisdictional synthesis, with explicit handling of per-population conflict logging (no inline arbitration) and Tier-4/5 grouping with statutory codes for comparison-only purposes.

**Key integrity finding:** 567/661 sources (85%) are AUTHOR-TITLE-ONLY metadata; 14/661 (2%) VERIFIED. 177/245 connections empty. `citation_mining` table has 0 rows. The existing evidence base cannot reliably support Stage C content work without rehabilitation.

**Convergence with session_g:** independently, the prior citation-mining session surfaced GAP-283 (P1) — same finding, different entry point.

---

## Skills run

- (none formally invoked via SKILL.md protocol — this was a governance/audit session; deliverables produced by direct reasoning + file generation)
- session-consolidator: **THIS run** at close

## Gaps raised this session

- No new gap records added to `gaps` table (audit was meta-level; existing P1 GAP-283 from session_g captures the core finding)
- The 494-line workplan is itself the structural-gap deliverable

## Deliverables committed

| File | Path | SHA | Status |
|---|---|---|---|
| BPC rewrite workplan | `audits/bpc-rewrite-workplan-2026-05-11.md` | ce266114ef97 | PROPOSED — NOT ADOPTED |

## Decisions locked (this session)

| # | Decision | Outcome |
|---|---|---|
| 1 | AR/HI/ID/SW/BN native-language keyword verification | In-scope (Phase A.11) |
| 2 | Tier 4 (international standards) + Tier 5 (national frameworks) treatment | Grouped with statutory codes in Step 3 jurisdiction comparison; NOT cited as evidence in Step 5 |
| 3 | Phase G output generator timing | Built early (Phase A.12 stub mode) |
| 4 | MERGED/STUB slug handling | Minimal redirect-only reasoning docs for MERGED; gap-naming reasoning docs for STUB |
| 5 | Pre-Phase-E synthesis retraction | Immediate retraction banner on entering Phase B (~30 BPCs affected) |

## State snapshot (DB at session close)

| Metric | Value |
|---|---|
| BPC files on disk | 95 (root + subdirs, excluding _template/index) |
| bpc_metadata rows | 97 |
| slugs table rows | 81 (14 fewer than filesystem — A.1 reconciliation) |
| evidence_sources | 661 |
| AUTHOR-TITLE-ONLY | 567 |
| VERIFIED | 14 |
| connections | 245 |
| connections with empty description AND connection_type | 177 |
| citation_mining table | 0 rows |
| gaps P1 OPEN | 8 |
| gaps total OPEN | 32 |

## Blockers / decisions deferred to next session

- **User must decide workplan reconciliation** before next content work. Three paths:
  1. Adopt BPC rewrite workplan as new operative plan (supersedes Stage C; new PI version)
  2. Run BPC rewrite in parallel with Stage C
  3. Reject BPC rewrite workplan; continue Stage C accepting current evidence base
- No path is the default. PI v10.6 standing rule #6 still names workplan-co0007-v4 as operative.

## Pattern observations

- **Pattern: topic-evidence vs claim-evidence conflation.** Manifested twice this session: (a) my draft synthesis cited Iglehart 2020 / ANSI S12.60 etc. as evidence for specific RT values when those sources are about the topic-area, not validation of the specific claim; (b) Tier 2 multilingual work used practitioner blog summaries to substantiate jurisdiction-specific code values without retrieving the primary regulatory text. Standing rule #7 (adversarial protocol) is designed to catch this; was inactive on the affected closures.
- **Pattern: schema-exists, field-unpopulated.** Repeated across `evidence_type` (3% pop), `verification_status` (2%), `derivation_chain` (0%), `synthesis_attribution_required` (0%), `citation_mining` (0 rows). Schema design is rigorous but population discipline has lagged.
- **Pattern: skill-protocol-vs-implementation gap.** `multilingual-research_SKILL.md` mandates 19 langs × 46 jurisdictions; DB schema only supports 14 × 24. Protocol-vs-data drift not previously flagged in skill-registry.

## Recurring rules (proposed for project-standards.md addition, pending user approval)

- **RULE [new]:** Synthesis claims citing a source for support must specify whether the source provides claim-evidence or topic-evidence. Topic-evidence citation does not satisfy adversarial protocol's named_dissenter / falsification_condition requirements.
- **RULE [new]:** AUTHOR-TITLE-ONLY metadata_quality is insufficient for any source cited in best_practice_synthesis. Verification to COMPLETE required before synthesis publication.

## Next session opening

The next session must open with the user's workplan reconciliation decision. Do not start any content work until the decision is logged. Read this session file + `audits/bpc-rewrite-workplan-2026-05-11.md` + `workplan/workplan-co0007-v4.md §Current position` first.

---

## YAML session-close block

```yaml
session_id: session_2026-05-11h-bpc-rewrite-workplan-design
session_close: 2026-05-11 06:00 UTC
deliverables_committed:
  - audits/bpc-rewrite-workplan-2026-05-11.md
gaps_raised: 0
gaps_resolved: 0
skills_invoked:
  - session-consolidator (this close)
next_action: USER DECISION on workplan reconciliation (3 paths in handoff)
blockers:
  - Cannot resume Stage C content work until workplan reconciliation decided
workplan_state:
  operative: workplan-co0007-v4.md (Stage C1-C11 ACTIVE)
  proposed: audits/bpc-rewrite-workplan-2026-05-11.md (PROPOSED-NOT-ADOPTED)
```
