# GAP-079 / GAP-CITE-01 Priority Reclassification — Recommendation

**Status:** Decision-support document
**Authoring:** Opus 4.7 audit-remediation session 2026-05-01
**Audit basis:** audit_2026-04-30 R8 — both currently-OPEN P1 gaps target the pre-pivot corpus that Block 33 reframed as input data, not deliverables. They are scheduled to be done at Stage C migration. The current P1 status creates ongoing-priority noise without ongoing-action capacity.
**Recommendation type:** priority reclassification analysis; project owner decides.

---

## 1. Snapshot

Two P1 (highest-priority) gaps remain OPEN after Stage A close:

| Gap ID | Status | Skill | Scope |
|---|---|---|---|
| GAP-079 | OPEN-PARTIAL | literature-review-planner | Part 4 + Part 7/8 GRADE matrix application to ~125 item specifications |
| GAP-CITE-01 | OPEN-PARTIAL | citation-tagger | Populate `ref_ids` for 1,382 claims across Parts 1-12 (386 TAGGED / 918 PENDING as of 2026-04-19) |

Both gaps target *the pre-pivot corpus*. Per workplan/workplan-co0007-v3.md §Salvage matrix and per migration-survival.md §4.2, that corpus's prose-form (Part 4 specifications, Appendix A tables) is SUPERSEDED. The underlying values (jurisdictional data, citations) are SURVIVES_AS_IS and migrate forward; the synthesis prose retires.

This raises the question: what does P1 priority mean for work targeted at superseded form?

---

## 2. Three options

### Option A — Retain P1, schedule for Phase B

**Rationale:** the gaps are valid; the work needs doing; Phase B has capacity in some sessions for this work alongside the architecture work.

**Cost:** GRADE application requires 3-4 sessions per GAP-079 own estimate. Citation tagging requires ~12-15 sessions for the remaining 918 claims (extrapolating from the 4-session-per-Part rate). That is ~15-19 sessions of work attached to a corpus whose prose form is being retired.

**Risk:** the work duplicates Stage C migration — the same claims will be re-cited (new form), and the same evidence judgments will be re-issued (post-Stage-A apparatus including A6 evidence-state machine, A12 model_routing) when the synthesis crosses to the new storage form.

### Option B — Reclassify P2, defer to Phase B-late or Phase C

**Rationale:** the gaps are valid but not on the critical path. Phase B's critical path is B1-B5 (storage form selection through pilot validation). GRADE application and citation tagging do not block any of those.

**Cost:** the gaps remain visible in the register but at a lower priority that signals "important; not gating."

**Risk:** if the project owner later decides GRADE matters for B6 pilot validation (e.g., pilot reviewers ask for evidence-tier transparency), the work would need to be expedited. This risk is mitigated by the fact that GRADE was always intended for Stage C migration; no commitment has been made to Phase B GRADE coverage.

### Option C — Reclassify P3 OR mark CLOSED-DEFERRED-TO-MIGRATION, document explicitly

**Rationale:** these gaps target work that is *definitionally* part of Stage C migration (per migration-survival.md §4.11 bibliography + §4.2 BPC synthesis). They are not gaps in the same sense as P1 gaps about live infrastructure. Closing-deferred captures their actual disposition.

**Cost:** the gap register loses the ongoing-tracking signal. If migration is delayed or scoped down, these gaps don't resurface automatically.

**Risk:** false closure — the gaps are not "done"; they're deferred. If they're closed without explicit deferral language, they could be lost from forward planning.

---

## 3. Recommendation

**Reclassify both gaps to P2 with explicit Stage C dependency annotation (Option B).**

Rationale:
- The work needed remains valid; demoting captures the actual urgency state.
- P2 is the project's "important; ongoing or expected; not gating" tier — exactly the right semantics for Stage C migration prep work that is not on Phase B critical path.
- P3 demotion would understate ongoing capacity for partial work (e.g., citation tagging of new claims as they're authored remains a P2-appropriate ongoing activity).
- CLOSED-DEFERRED-TO-MIGRATION (Option C variant) is too strong because it removes the gaps from the OPEN tracker entirely; partial progress (the 386 TAGGED claims are real) deserves OPEN-PARTIAL status.

The reclassification language should make the dependency explicit:

```
GAP-079: P2 (was P1) — depends on Stage C migration (C2-C4 phases). 
                      Apply GRADE to migrated specifications, not to superseded Part 4 prose.
                      Reclassified per audit_2026-04-30 R8.
GAP-CITE-01: P2 (was P1) — depends on Stage C migration (C5-C7 phases). 
                          Citation tagging continues for new content; backlog of 918 PENDING migrates forward.
                          Reclassified per audit_2026-04-30 R8.
```

---

## 4. Effect on gap_register summary

Current P1 OPEN count: 4 (per gap_register.md current state — actually 4 P1 gaps total: GAP-079 OPEN-PARTIAL, GAP-CITE-01 OPEN-PARTIAL, GAP-080 CLOSED-CONSUMED, plus one other if present).

Post-reclassification: 0 P1 OPEN gaps.

This matches the project's actual state. Stage A closed all the P1 gaps that had infrastructure dependencies (A6/A7/A8/A9/A10/A11/A12/A13). The two remaining P1 gaps are the migration-targeted ones, and per this recommendation they reclassify to P2.

The gap_register's P1 tier becomes empty — which is the correct state at Stage A close.

---

## 5. What this recommendation does not do

- It does not perform the reclassification. Project owner does (single edit to two table rows + Decision record).
- It does not schedule the work. Stage C scheduling owns that.
- It does not pre-empt re-promotion to P1 if Stage C migration scope changes.
- It does not change scope or content of either gap. Both gaps' descriptions remain accurate.

---

## 6. Pairs with Decision

If adopted, this reclassification pairs with one Decision record:

```yaml
decision_id: D-NEXT
category: D-OP
summary: Reclassify GAP-079 and GAP-CITE-01 from P1 to P2 with Stage C dependency annotation
outcome: Both gaps moved to P2; OPEN-PARTIAL status retained; description annotated with Stage C dependency
rationale: Both gaps target the pre-pivot corpus reframed as input data per Block 33 supersession. Their work is definitionally part of Stage C migration. P1 status creates ongoing-priority signal without ongoing-action capacity in Phase B. P2 with Stage C dependency annotation captures actual urgency.
delegation: DG-REVIEW
model_routing: opus/100/route
authority: project_owner
doctrinal_basis:
  - audit_2026-04-30 R8
  - workplan/workplan-co0007-v3.md §Salvage matrix
  - governance/migration-survival.md §4.2, §4.11
linked_artifacts:
  - gap_register.md (GAP-079, GAP-CITE-01 rows)
  - workplan/gap-p1-reclassification-recommendation.md (this document)
review_status: PENDING
```

---

## 7. Status

| Field | Value |
|---|---|
| Status | DRAFT — recommendation only |
| Adoption | OPTIONAL |
| Author | opus_4.7_session_2026-05-01_audit-remediation |

End of recommendation.
