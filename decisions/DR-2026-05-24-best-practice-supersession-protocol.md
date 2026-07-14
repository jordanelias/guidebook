# DR-2026-05-24 — Best-Practice Supersession Protocol

**Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECORD-2026-07-13.md** *(was: PROPOSED — pending owner adoption and migration 015 application)*
**Authored:** 2026-05-25 (session_2026-05-23-bpc-rewrite-phase-b-closure)
**Doctrine SHA at authorship:** `61c7f95` (governance/mission-and-epistemics.md)
**Supersedes:** sets a new bar for `bpc_metadata.citation_mining_complete = 1` slug closure (previously meant "every Tier 1-3 source has a mining row"; under this DR, that is necessary but no longer sufficient for slug closure)

---

## Context

PI standing rule #6 (canonical workplan) and mission doctrinal commitments 2, 3, and 5 hold that best practice for the guidebook is determined by the evidence hierarchy, not by code consensus or by whatever evidence happened to be in the corpus when a slug was first scoped. The Phase B citation-mining protocol (skill: `citation-miner`) surfaces references that cite or are cited by an anchor source — a citation-graph operation. It does **not** check whether each anchor source remains the best current evidence for the parameter × population × outcome it supports.

A slug closed under the old citation_mining_complete=1 bar can have all anchor sources protocol-mined and still rest on stale best evidence — for example, citing the 2010 ANSI/ASA S12.60 revision when a 2024 revision exists, or citing 2018-era systematic reviews when 2024 Cochrane or JBI work supersedes the synthesis. That is exactly the failure mode mission doctrinal commitment 2 prohibits ("a best-practice claim derived solely from code consensus is in error" — and by symmetric reasoning, a best-practice claim derived from a *superseded* Tier-3 source is also in error, because the operative evidence hierarchy includes a temporal dimension).

This DR establishes the operational protocol for ensuring current best evidence is anchored, including pre-launch one-time audits and the post-launch maintenance cadence.

---

## Decision

### Per-slug supersession check (required for slug closure)

A slug is not closed until, for every evidence_sources row currently cited by the slug, a supersession check has been completed with one of these outcomes:

| outcome | meaning |
|---|---|
| `current_best` | No superseding work found in the targeted search; source remains current best as of check_date |
| `superseded_by` | A higher-tier work, or a more recent same-tier work, addresses the same parameter × population × outcome and should replace the anchor |
| `refined_by` | A subsequent work refines a parameter value, sub-population, or outcome dimension; original anchor still governs the unaffected dimensions |
| `divergent_no_supersession` | Multiple recent works exist; their findings diverge; the synthesis cell needs joint assessment rather than single-source replacement |
| `co1_addition_logged` | (Co-1 sources only) — accumulation, not replacement; new Co-1 evidence added to the parameter's corpus alongside the anchor |

### Co-1 supersession treatment

**[ASSUMPTION: pending owner confirmation]** Co-1 evidence accumulates rather than supersedes. A newer DPO position paper does not invalidate an older lived-experience study; each instance adds to the corpus rather than replacing prior instances. The `co1_addition_logged` outcome captures this. Tier 1 / Tier 2 / Tier 3 / Tier 4 / Tier 5 sources use the four supersession outcomes (current_best, superseded_by, refined_by, divergent_no_supersession). Tier 6 (statutory codes) are compliance-floor reference and are checked for regulatory updates separately.

If owner directs that Co-1 supersession is treated parallel to Tier 1 supersession, remove the `co1_addition_logged` outcome and add Co-1 to the standard four-outcome enum. Schema migration 015 includes the co1-accumulation outcome by default; reversing this is a one-line schema change.

### Search strategy per evidence type

| Evidence type | Primary search tool | Secondary | Tertiary |
|---|---|---|---|
| Tier 1 clinical (RCT, OT intervention) | PubMed (parameter+population query, filtered to date > anchor publication) | Cochrane Library direct | Scholar Gateway |
| Co-1 (lived experience, DPO position) | Scholar Gateway (lived-experience + parameter) | Direct DPO/NGO publication catalogs | n/a |
| Tier 2 (NGO/DPO guideline) | Direct organizational publication catalog | Web search for updated edition | n/a |
| Co-2 (OT CPG) | Direct OT body publication catalog (CAOT, AOTA, RCOT, COTEC, WFOT) | PubMed (filtered to CPG publication type) | n/a |
| Tier 3 (SR/meta-analysis) | PubMed (Systematic Review / Meta-Analysis publication types, parameter query) | Cochrane Library | Scholar Gateway |
| Tier 4 (international standard) | Direct standards-body catalog (ISO, IEC, EN) | Web search for revision history | n/a |
| Tier 5 (national beyond-code framework) | Direct national framework publication | multilingual-research skill | n/a |
| Tier 6 (statutory code) | Direct jurisdictional code publication; tracked separately under multilingual-research | n/a | n/a |

For each anchor source, the search produces 0–N supersession candidates. Each candidate's abstract is read; the human or Opus operator judges whether the candidate actually supersedes (or refines, or diverges). The check is closed with the outcome and the supersession_candidates list recorded.

### Cadence

1. **At slug closure** — Mandatory per-slug supersession check on every cited anchor source. Slug closure semantics: `citation_mining_complete = 1` (mining rows exist for every Tier 1-3 source) AND `supersession_check_complete = 1` (every cited source has a supersession_check row with an outcome).

2. **Semiannual sweep** — Across the full corpus, every six months, run a temporal-pass supersession check: for every anchor source whose last_checked_date is older than the sweep horizon, re-run the supersession search filtered to publication date > last_checked_date. Sweep dates: 2026-12-01 (first post-DR sweep, ~6 months after this DR) and every 6 months thereafter. The sweep cadence is itself a methodological declaration — between sweeps, the BPC's evidence base is correct as of the last sweep, not as of "today."

3. **Retroactive audit on 6 already-closed slugs** — Per owner directive (2026-05-25), the 6 slugs closed prior to this DR under the old definition do not get grandfathered. Each is retroactively audited under this protocol. The closure semantics on those slugs flip to "closed but supersession-pending" until the retroactive audits complete.

### Closure-version tracking

To distinguish slugs closed under the old bar from slugs closed under the new bar, add a `closure_definition_version` column to bpc_metadata:
- `v1` = closed under citation_mining_complete=1 only (pre-2026-05-25 definition)
- `v2` = closed under citation_mining_complete=1 AND supersession_check_complete=1 (this DR)

Slugs closed before 2026-05-25 are stamped `v1` at migration time. As each retroactive audit completes, the slug's `closure_definition_version` is bumped to `v2`.

---

## Out of scope (deferred to follow-up work)

- **Automated semiannual sweep tooling.** This DR names the cadence; the actual sweep automation (cron-driven PubMed query batches, candidate queuing for triage) is a follow-up implementation. Pre-launch, manual semiannual sweeps suffice.
- **Cross-jurisdictional supersession.** Workplan §1 cross-jurisdictional synthesis needs ≥3 jurisdictions per parameter. When a jurisdiction's code is superseded by a newer edition (e.g., DIN 18040 revision), that's a Tier-6 supersession — tracked separately under jurisdiction-tracker, not under this protocol. This DR covers Tier 1-5 + Co-1 + Co-2.
- **Intra-source refinement granularity.** A `refined_by` outcome currently records "refined on dimension X." Sub-dimension tracking (which population, which parameter value range, which outcome measure) is deferred until the first 2-3 retroactive audits reveal whether the coarse `refined_by` outcome is sufficient.

---

## Decision rationale per mission test (§Test against which all downstream decisions are evaluated)

1. **Helps readers ask better questions?** Yes — readers can see when an anchor source is current best vs superseded, and the supersession record gives them the post-anchor literature for follow-up.
2. **Acknowledges non-uniformity?** Yes — the `divergent_no_supersession` outcome preserves divergence rather than forcing a single-anchor replacement.
3. **Grounds best practice in evidence hierarchy?** Yes — supersession searches are tier-prioritized; a Tier-1 candidate supersedes a Tier-3 anchor regardless of recency, and within the same tier, recency tie-breaks.
4. **Surfaces convergence/divergence?** Yes — when Tier 1 and Co-1 evidence on the same parameter both update, the synthesis cell sees both updates rather than just one.
5. **Respects Co-1 operational reality?** Yes — Co-1 accumulation (the assumed default) acknowledges that lived experience is contextually situated and that single newer DPO position papers don't invalidate older ones.
6. **Teaches professional judgment?** Yes — the supersession record gives professionals the full post-anchor literature for the cell, not just the anchor.
7. **Verifiable?** Yes — every supersession_check row carries the search_strategy_record (query, date filter, tier filter, candidates_returned, candidates_reviewed) so the check is replayable.
8. **Aligns with audience priority?** Yes — designers and disabled people (primary audiences) read claims grounded in current best evidence; OTs and policymakers (secondary) get explicit supersession status for their jurisdictional/clinical handoffs.

---

## Implementation deliverables (this session)

1. **This DR** at `decisions/DR-2026-05-24-best-practice-supersession-protocol.md`.
2. **Migration 015** at `scripts/migrations/015_supersession_check.sql` adding the `supersession_check` table + `supersession_check_complete` and `closure_definition_version` columns to `bpc_metadata`.
3. **Skill file** at `skills/supersession-audit_SKILL.md` codifying the search protocol per evidence type and the closure-record schema.
4. **Retroactive audits** on 6 closed slugs — separate session-record artifacts per slug, materialized as data migrations.

PI bump deferred per architecture v2.3 `<migration_and_growth>`: this DR + the schema + the skill are sufficient armature. PI rule #6 (canonical workplan) is unchanged; the workplan §B-text already names "complete citation mining" as Phase B's end-state, and this DR refines what "complete" means without altering the workplan structure.

---

## Status

**ACCEPTED 2026-07-13** (see the header line above; this section was left un-synced at the ratification flip — corrected here, Q14 adversarial pass B-scope finding 2).

Adoption conditions, all now met: migration 015 applied (`user_version=27`) + `skills/supersession-audit_SKILL.md` committed + this DR's retroactive-audit deliverables completed (6/6 slugs at `closure_definition_version='v2'`: cognitive-wayfinding-design, mental-health-built-environment, mobility-built-environment, room-acoustic-performance, school-environment-autism, stair-ramp-threshold-biomechanics-accessibility — VERIFIED-BY: direct query against `data/guidebook.db`, this session).

Reversible by: a follow-up DR that downgrades the supersession-check requirement (would need to specify what failure mode the downgrade addresses, since this DR was authored specifically to address a doctrinal commitment 2 failure mode).

---

## References

- governance/mission-and-epistemics.md doctrinal commitment 2 (best practice from evidence hierarchy, not code consensus)
- governance/mission-and-epistemics.md doctrinal commitment 3 (Co-1 co-primary with Tier 1)
- governance/mission-and-epistemics.md §Evidence-state machine for best-practice claims
- governance/mission-and-epistemics.md §Test against which all downstream decisions are evaluated
- workplan/bpc-rewrite-workplan-2026-05-11.md §B.11 (citation mining)
- skills/citation-miner_SKILL.md (the protocol this DR supplements, not replaces)
- DR-2026-05-13 (evidence verification methodology — PI standing rule #10's existence-and-content gate, which this DR's `current_best` outcome complements with a recency-and-tier dimension)
