# Placeholder Decision Review — Triage

**Status:** Decision-support document (recommendations only)
**Authoring:** Opus 4.7 audit-remediation session 2026-05-01
**Audit basis:** audit_2026-04-30 R3 — 106 of 113 Decision records carry `legacy/none/none` model_routing and were seeded directly from project-standards rules at A12 register-launch (2026-04-30). They function operationally as queryable rule lookups but do not yet capture the A12 decision-protocol fields (`delegation`, `model_routing`, `authority`, `doctrinal_basis`, `linked_artifacts`).
**Recommendation type:** sequencing + scoping; the project owner makes the actual review decisions.

---

## 1. Snapshot

| Field | Value |
|---|---|
| Total Decision records | 113 |
| Placeholder records (`legacy/none/none`) | 106 |
| Non-placeholder records | 7 (D-0107 ci-integration; D-0108–D-0113 from B1 sessions 1–2) |
| Records with `summary == outcome` (extraction artifact) | 106 (all placeholders) |
| Records with <2-sentence rationale | 1 (D-0010) |
| Records flagged C3/C6 in audit | 1 (D-0010 — both flags) |

The placeholder records are extraction artifacts: they were generated mechanically from project-standards rule text at A12 register launch. Each has `summary == outcome` because both fields received the same rule-statement string. The rationale field carries the rule text itself, which is correct as preserved evidence but does not satisfy A12 §3.3 rationale-discipline (capture the *why*, not the rule).

The 7 non-placeholder records (D-0107 onward) are post-launch real decisions captured under A12 protocol with proper fields.

---

## 2. Distribution by category

| Category | Count | Likely review intensity |
|---|---|---|
| D-DOCT | 40 | HIGH — doctrinal commitments most affected by §3.3 rationale-discipline; many would benefit from authority field (project-owner vs Co-1 vs counsel) |
| D-METH | 42 | HIGH — methodology commitments; model_routing classification matters because methodology decisions are where Opus arbitration/synthesis vs Sonnet routing distinguish |
| D-OP | 12 | MEDIUM — operational rules; many can stay DG-AUTO with mechanical review notes |
| D-SCHEMA | 11 | LOW-MEDIUM — schema/structural rules; mostly mechanical; DG-AUTO appropriate |
| D-PRES | 5 | MEDIUM-HIGH — presentation/voice; A4 voice phase will dictate updates here |

---

## 3. Per-record state of the 7 non-placeholders (already compliant)

These do NOT require review per audit R3:

| ID | Category | Delegation | model_routing | Comment |
|---|---|---|---|---|
| D-0107 | D-OP | DG-REVIEW | sonnet/100/route | CI integration; 2026-04-30 |
| D-0108 | D-METH | DG-REVIEW | opus/150/synth | B1 derivation framework; 2026-05-01 |
| D-0109 | D-OP | DG-AUTO | opus/100/route | B1 session arc plan |
| D-0110 | D-METH | DG-REVIEW | opus/150/synth | B1 criteria weighting |
| D-0111 | D-METH | DG-REVIEW | opus/150/synth | B1 S-05 migration-out spec |
| D-0112 | D-METH | DG-REVIEW | opus/150/synth | B1 hybrid eliminator test |
| D-0113 | D-OP | DG-AUTO | opus/100/route | B1 requirements lock |

---

## 4. Records flagged in audit

### 4.1 D-0010 (D-DOCT) — both C3 and C6 warnings

```
summary: Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is from disability-led research
outcome: (same as summary)
rationale: (one sentence — same as outcome)
```

**Audit finding:** rationale matches outcome (C6 violation per A12 §3.3 — rationale must capture *why*, not restate *what*). Rationale is also single-sentence (C3 short-rationale warning).

**Recommended action at review:** Expand rationale to capture the actual deliberation: why is Co-1 testimony co-primary at Tier 3–4 specifically (vs. supplementary)? What evidence-tier-machine reasoning leads to that placement? Authority should likely be Co-1 (this is a Co-1-load-bearing rule). doctrinal_basis should cite governance/co1-operational.md. Recommended `delegation: DG-NON` (project owner authority); recommended `model_routing: opus/200/synth` (substantive doctrinal decision requiring Opus synthesis with Co-1 review hold).

### 4.2 No other C3/C6 violations found in current register

The audit's "4 records flagged" estimate over-counted slightly. The actual data shows 1 record (D-0010) with both flags. This does not invalidate the audit's recommendation that placeholder rationale-discipline is uneven; D-0010 is just the cleanest exemplar.

---

## 5. Proposed sequencing

The 106 placeholders do not all need review at the same depth. A tiered sequencing reduces effort:

### 5.1 Tier-A: 5–10 records (HIGH-leverage; review first)

Records governing CRPD posture, mission, evidence-tier hierarchy, Co-1 operational, and population taxonomy. These are doctrinally load-bearing; their authority and rationale fields most affect downstream agent behavior.

Candidates (from D-DOCT category):

- D-0001 (purpose-of-guidebook)
- D-0010 (Co-1 co-primary at Tier 3-4) — already flagged
- Records concerning T-03 (Tier 3 Co-1 inclusion), T-04 (Tier 4 evidence definition), D-03 (operational Co-1 vs review)
- Records concerning A1-A2 mission commitments
- Records concerning A7 population taxonomy

These are also the records most likely to land in `always-DG-NON` per A12 §2.4. Project owner should review delegation classification first; rationale and doctrinal_basis fill in once delegation is settled.

### 5.2 Tier-B: D-METH placeholders (~30 records; batch review)

Methodology rules: validator behaviors, reverse-citation discipline, evidence-state machine application, search protocol, Co-1 source admissibility test. These can be reviewed in batches of 5-10, grouped by topic. Most will receive `model_routing: sonnet/100/route` or `opus/100/route`; `delegation: DG-AUTO` or `DG-REVIEW` depending on whether the rule was originally project-owner-authored or Claude-derived.

### 5.3 Tier-C: D-OP and D-SCHEMA placeholders (~23 records; mechanical)

Structural and operational rules: file-naming conventions, registry record formats, validator wiring. Most can be reviewed mechanically: `delegation: DG-AUTO`, `model_routing: legacy/none/none` retained (the rule is mechanical; no real decision is being captured), or upgraded to `sonnet/50/extract` if any deliberation occurred. Authority is generally project-owner.

These records may be the strongest case for retaining `legacy/none/none` permanently — they are not "decisions" in the deliberative sense; they are seeded structural rules.

### 5.4 Tier-D: D-PRES placeholders (~5 records; defer to A4)

Presentation/voice rules. A4 voice-style phase will likely supersede or refine all of these. Defer review until A4 closes; reclassify or supersede en masse at that point.

---

## 6. Reviewer effort estimate

If the project owner adopts this sequencing:

| Tier | Records | Per-record effort | Total | Notes |
|---|---|---|---|---|
| A | 5–10 | 30–60 min | 5–10 hours | Each record is a real doctrinal decision; full A12 protocol applies. |
| B | ~30 | 10–15 min | 5–8 hours | Batched review with cross-record consistency. |
| C | ~23 | 2–5 min | 1–2 hours | Mostly mechanical; spot-check + accept. |
| D | ~5 | (deferred to A4) | (post-A4) | A4 disposition determines outcome. |
| **Total** | **63–68** | — | **11–20 hours** | Excluding Tier D pending A4 |

This is total reviewer time, not Claude-session time. The Claude side is ~5-8 sessions of placeholder-review work spread across the schedule, not a single dedicated arc.

---

## 7. Decoupling recommendation

The audit's R3 framing ("decide on the 106 placeholder records — schedule the rationale-review work, or accept that they ship as-seeded and document that") presumes that "ship as-seeded" is a viable path. This document recommends a hybrid:

- **Accept as-seeded** for Tiers C and D (28+ records). Document this acceptance in a single Decision record (one D-OP/DG-AUTO record stating "structural and presentation-tier seeded rules retain legacy/none/none model_routing as appropriate to their operational character").
- **Review per Tier A and B** for the remaining 70+ records, scheduled across 5-8 sessions over 2-3 months.

This avoids the false binary (review all 106 vs accept all 106) and matches review depth to record character.

---

## 8. What this document does not do

- It does not perform any of the placeholder reviews. Those require project-owner authority over delegation/authority/doctrinal_basis fields.
- It does not commit Tier-A/B/C/D classifications to the register. Those are review decisions, not pre-review classifications.
- It does not propose a specific calendar schedule. Sessions/cadence are project-owner determined.
- It does not pre-decide Tier-A delegation classifications. Each Tier-A record is doctrinally load-bearing and warrants individual review.
- It does not authorise mass-changes to the register. Any update goes through normal A12 protocol.

---

## 9. Status

| Field | Value |
|---|---|
| Status | DRAFT — project-owner-facing recommendation |
| Adoption | OPTIONAL — sequencing is recommendation, not requirement |
| Pairs with Decision | none until adopted |
| Author | opus_4.7_session_2026-05-01_audit-remediation |

End of triage document.
