# Change Order — project-instructions (PI) revision sweep

**Status:** PROPOSAL — project-owner-applied; not auto-applied
**Authoring:** Opus 4.7 audit-remediation session 2026-05-01
**Audit basis:** audit_2026-04-30 R6 — three stale items identified in PI text. PI is owned by the project owner (lives in claude.ai project context block, not in repo); this Change Order proposes replacement text for project-owner application.
**Type:** D-OP / DG-NON (PI text edits are always project-owner authority).

---

## 1. Scope

Three stale items identified in audit. This Change Order proposes a single revision sweep.

| ID | Item | Severity | Action |
|---|---|---|---|
| PI-CO-01 | Start-protocol omits `references/connections/_index.md` | LOW (operational) | Add to start-protocol read list |
| PI-CO-02 | Model-identity references "Sonnet 4.6" / "Opus 4.6" | LOW (currency) | Update to reflect current Claude family (4.7) per `<model_identity>` advisory |
| PI-CO-03 | References to `co0007-audit-2.md` (uploaded but never committed to repo) | LOW (broken-reference) | Remove reference OR commit the audit-v2 file |

---

## 2. PI-CO-01: connections/_index.md in start-protocol

### Current state (audit observation)

PI's start-protocol section enumerates the files Claude reads at session start. The list omits `references/connections/_index.md`, even though A12 §6.2 / session-consolidator §1c references it as part of the standard read set, and `references/project-standards.md` line 451 establishes that "CON-IDs (CON-NNNN) resolve to entries in `references/connections/_index.md`".

### Proposed revision

In PI's start-protocol read list (location: PI section "On every session start, read these files in order"), add this line at the appropriate position (after `references/project-standards.md` and before `gap_register.md`):

```
- references/connections/_index.md (CON-NNNN resolution; 8K tokens; per project-standards line 451)
```

### Rationale

CON-IDs are referenced throughout BPCs, governance docs, and session logs. Without `_index.md` in the start-read set, Claude either (a) silently fails CON-ID resolution, (b) re-derives the index inline (token cost), or (c) reads the file ad-hoc when needed (latency and reads on demand fall outside the start-protocol audit trail). Including it canonically aligns PI with project-standards line 451.

---

## 3. PI-CO-02: Model-identity currency

### Current state (audit observation)

PI's model-routing section (or an inline reference, per audit) names "Sonnet 4.6" and "Opus 4.6" as the default model family. The current Claude family in this conversation is Claude 4.7 (Opus 4.7). Per system-prompt model_identity advisory: "System prompt's model name may not match deployed model. Anthropic uses a shared system prompt that lags deployment."

### Proposed revision

Two options:

**Option A — name the family without version pin.** Replace "Sonnet 4.6" / "Opus 4.6" with "Sonnet" / "Opus" throughout PI. This avoids future re-revision when the family bumps to 4.8/5.0.

**Option B — name the current family explicitly.** Replace "Sonnet 4.6" / "Opus 4.6" with "Sonnet 4.6 or 4.7 (whichever is in use)" / "Opus 4.6 or 4.7 (whichever is in use)". This keeps the family pin but acknowledges the currency.

**Recommended: Option A.** PI is project-owner-edited infrequently; version-pin maintenance creates ongoing edits. The family-only naming relies on the user-preferences `<model_identity>` advisory ("System context doesn't reliably indicate model — check UI selector") to handle versioning.

### Rationale

Decision-register entries (D-0107 onward) use family-only model_routing values like `opus/150/synth` and `sonnet/100/route`, which already follow Option A's pattern. PI's continued reference to "4.6" creates a documentation/practice mismatch.

The `model_routing` enum in schemas/decision.py (per A12) does not pin version either. Aligning PI with the schema is the natural target.

---

## 4. PI-CO-03: audit-v2 reference

### Current state (audit observation)

PI references `co0007-audit-2.md` as an upstream input to Stage 0 verification. Per `session_2026-04-26-co0007-stage0.md` D-01-D note (or wherever recorded), the file was uploaded to the chat but the upload was released between turns; the file was never committed to repo. The reference in PI is therefore a broken pointer for any future session reading PI from canonical state.

### Proposed revision

Two options:

**Option A — remove the reference.** PI text mentioning `co0007-audit-2.md` revises to remove the file and acknowledge `workplan/workplan-co0007-v3.md` as the operative successor. Sample replacement:

```
(remove) co0007-audit-2.md as Stage 0 verification anchor
(replace with) workplan/workplan-co0007-v3.md as operative-plan-after-audit-and-supersession
```

**Option B — commit a placeholder document.** Author `references/audits/co0007-audit-2-summary.md` summarising what audit-v2 said (per session notes from 2026-04-26 stage-0), enough that PI's reference resolves to a real file. Mark the placeholder as RECONSTRUCTED and note that the original upload was lost.

**Recommended: Option A.** Audit v2's content is captured in workplan v3 (which incorporated the audit's findings into the resolution map per workplan v3 §What changed from prior versions). The standalone audit document is functionally superseded; PI should reference the operative successor.

### Rationale

Broken references in PI cause silent failure: a session reads PI, follows a reference to a missing file, fails open, and proceeds without the missing context. Updating PI to reference workplan v3 (which exists and is canonical) ensures every PI-driven read resolves successfully.

---

## 5. Application protocol

PI lives in the claude.ai project context block. Updating PI requires:

1. Project owner edits PI text in claude.ai project settings.
2. The edit propagates to all subsequent conversations in that project.
3. The edit is visible to Claude as the new PI on next session start; no commit is needed.

There is no version-control mechanism for PI text inside claude.ai (per project-owner observation). To create an audit trail for this revision:

- This Change Order document (`governance/pi-revision-co.md`) commits to repo as the proposal-of-record.
- A Decision record (D-OP / DG-NON) commits at the same time, recording that PI was revised per this Change Order.
- The Decision record's `outcome` field captures the post-revision PI snippets (or links to a PI-snapshot file if the project owner wishes to keep one).

This creates a queryable audit trail for the PI revision even though PI itself does not version.

---

## 6. Pairs with Decision (template)

If applied, the following Decision record commits at PI revision time:

```yaml
decision_id: D-NEXT
category: D-OP
summary: Apply PI revision sweep per pi-revision-co.md (PI-CO-01, PI-CO-02 Option A, PI-CO-03 Option A)
outcome: PI-CO-01 — added references/connections/_index.md to start-protocol read list. 
         PI-CO-02 — replaced "Sonnet 4.6"/"Opus 4.6" with "Sonnet"/"Opus" throughout.
         PI-CO-03 — replaced co0007-audit-2.md reference with workplan/workplan-co0007-v3.md reference.
rationale: PI staleness sweep per audit_2026-04-30 R6. _index.md omission caused silent fail of CON-ID resolution at session start; model-identity pin created documentation/schema mismatch; audit-v2 reference was broken (upload released between turns and never committed). All three resolved by single revision sweep.
delegation: DG-NON
model_routing: opus/100/route
authority: project_owner
doctrinal_basis:
  - audit_2026-04-30 R6
  - governance/pi-revision-co.md (this document)
linked_artifacts:
  - project-instructions (claude.ai project settings — text revised)
  - references/project-standards.md line 451 (CON-NNNN resolution authority)
  - workplan/workplan-co0007-v3.md (audit-v2 successor)
  - schemas/decision.py model_routing enum (alignment basis)
review_status: NA
```

---

## 7. What this Change Order does not do

- It does not edit PI directly. Project owner applies in claude.ai project settings.
- It does not modify project-standards.md or any in-repo document.
- It does not affect any session's behavior in this conversation. PI applies on next session.
- It does not pre-empt project owner adoption of different replacement text. The recommended options are recommendations.

---

## 8. Status

| Field | Value |
|---|---|
| Status | PROPOSAL |
| Application | PENDING — project-owner action |
| Pairs with Decision | D-NEXT (D-OP / DG-NON) at application time |
| Author | opus_4.7_session_2026-05-01_audit-remediation |

End of Change Order.
