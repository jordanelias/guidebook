# PI Revision — Paste-Ready Text Patches

**Status:** Application-ready artifact (companion to governance/pi-revision-co.md)
**Authoring:** Opus 4.7 audit-remediation-cont session 2026-05-02
**Audit basis:** audit_2026-04-30 R6 + D-0117 (proposal-of-record) + D-0128 (this paste-ready issuance)
**Application:** project owner pastes each block in the claude.ai project-instructions editor
**Tracking:** project owner adds follow-up Decision record after application recording the date applied and any wording modifications

---

## How to use this document

1. Open the Claude.ai project settings → project instructions editor for `jordanelias/guidebook` project.
2. For each PI-CO entry below, locate the existing text in the PI body, replace it with the new text, save.
3. Apply all three in one save if desired (PI text is project-owner-edited; agent does not have edit access).
4. After applying, add a follow-up Decision record amending D-0117 / D-0128 with the application timestamp.

---

## PI-CO-01 — Add references/connections/_index.md to start-protocol read list

### Where in PI

Locate the section in PI titled (or semantically equivalent to):

> **Start (every conversation):**
> 1a. GraphQL `batch_read`: `sessions/LATEST` + `references/project-standards.md` + `skills/workplan-orchestrator_SKILL.md`. Parse LATEST for session filename.

Or wherever the session-start protocol enumerates the files to read at the start of every conversation.

### Find this text

```
**Start (every conversation):**
1a. GraphQL `batch_read`: `sessions/LATEST` + `references/project-standards.md` + `skills/workplan-orchestrator_SKILL.md`. Parse LATEST for session filename.
```

### Replace with this text

```
**Start (every conversation):**
1a. GraphQL `batch_read`: `sessions/LATEST` + `references/project-standards.md` + `skills/workplan-orchestrator_SKILL.md` + `references/connections/_index.md`. Parse LATEST for session filename.
```

### Rationale

CON-IDs (CON-NNNN) are referenced throughout BPCs, governance docs, and session logs. project-standards.md line 451 establishes that CON-IDs resolve via `references/connections/_index.md`. Adding this file to the start-protocol batch ensures CON-ID resolution is available without ad-hoc per-need fetches.

---

## PI-CO-02 — Update model identity from "Sonnet 4.6 / Opus 4.6" to family-only

### Where in PI

Locate any section in PI that pins specific Claude model versions (e.g., "Sonnet 4.6", "Opus 4.6"). The audit identified these as appearing in model_routing context, but actual location varies.

### Search PI for these strings

- `Sonnet 4.6`
- `Opus 4.6`
- `4.6`

### Replace pattern

For every reference to specific minor versions:

| Old | New |
|---|---|
| `Sonnet 4.6` | `Sonnet (current)` or `claude-sonnet-4-6` or simply `Sonnet` |
| `Opus 4.6` | `Opus (current)` or `claude-opus-4-7` (current) or simply `Opus` |
| `Sonnet 4.5 / Opus 4.6` | `Sonnet / Opus` |

### Recommended replacement strategy

Replace all specific minor-version references with the **family-only** form (Sonnet, Opus, Haiku) and let model_routing notation in the decision register carry the version-specificity. The decision register schema enforces `{opus|sonnet|haiku|human|legacy}/{150|125|100|75|50|none}/{synth|arbitrate|extract|format|route|none}` — the model identity is a family value, not a minor version.

### Rationale

Per `<model_identity>` advisory and audit_2026-04-30 R6: system context's model name lags deployment, so any specific minor version pinned in PI becomes stale on every model rollout. The decision register's family-level routing is the durable specification; PI should reference the family, not the minor version.

---

## PI-CO-03 — Replace co0007-audit-2.md reference

### Where in PI

Locate the section in PI titled (or semantically equivalent to):

> **Active version:** V9.0 2026-03-20

Or any reference in PI to `co0007-audit-2.md`, `audit-v2`, or `co0007-audit-2`.

### Background

The audit-v2 file was uploaded at one point during Stage 0 but never committed to the repo (per session_2026-04-26-co0007-stage0.md note D-01-D). PI references to this file are broken-reference items.

### Find this text (if present)

Search PI for any of: `co0007-audit-2.md`, `audit-v2`, `co0007 audit 2`, references to a "second audit" or "audit version 2"

### Replace with one of these

**Option 1 (preferred — supersession-aware):**

```
[Reference to co0007-audit-2.md removed 2026-05-02 per audit_2026-04-30 R6 + D-0117 — that file was uploaded at Stage 0 but never committed to repo and was operationally superseded by workplan/workplan-co0007-v3.md (the operative workplan post-2026-04-26). For audit reference, see references/audits/process-audit_2026-04-30.md (Opus 4.7 process audit) and references/audits/methodological-audit_2026-04-30.md (Sonnet methodological audit).]
```

**Option 2 (commit the file):**

If a copy of `co0007-audit-2.md` still exists locally and the project owner wants it in the repo for audit completeness:

1. Copy the file to `references/audits/co0007-audit-2_archive.md`
2. Add a header annotation: "Status: ARCHIVED — superseded by workplan/workplan-co0007-v3.md operative-plan; retained for audit trail"
3. Update PI to reference the new path

### Rationale

PI must not contain broken-reference paths because (a) every session-start reads PI, and (b) an unresolvable reference creates either silent skip or error noise. The audit found this in the staleness sweep.

---

## Application checklist

After applying these patches in claude.ai:

- [ ] PI-CO-01 applied (start-protocol read list now includes connections/_index.md)
- [ ] PI-CO-02 applied (no specific minor versions in PI text)
- [ ] PI-CO-03 applied (no reference to co0007-audit-2.md in PI text)
- [ ] Test: start a new conversation; verify session-start protocol reads connections/_index.md without error
- [ ] Add follow-up Decision record (D-NEXT) noting application date + any wording modifications

---

## What this document does not do

- Edit the PI text itself (that lives in claude.ai project settings, not in repo).
- Ship a new active PI version (the project owner may want to bump V9.0 → V9.1 on application; that is a project-owner choice).
- Pre-empt project-owner judgment on the PI-CO-02 family-only versus version-pinned trade-off.

---

## Status

| Field | Value |
|---|---|
| Status | APPLICATION-READY |
| Pairs with Decision | D-0128 |
| Application location | claude.ai project-instructions editor (outside repo) |
| Application owner | project owner (jordanelias) |
| Application status | PENDING (project owner applies; this artifact is the paste source) |

End of paste-ready document.
