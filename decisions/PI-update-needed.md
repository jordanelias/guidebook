# PI v10.8 Update Required — DEPLOYMENT TO LIVE PROJECT SETTINGS

**Status:** v10.8 committed to repo as `governance/project-instructions-v10_8.md` @ a3bafb23199c (2026-05-11 06:30 UTC, session_2026-05-11h-bpc-rewrite-workplan-design)
**Action:** Owner must manually paste v10.8 content into claude.ai project knowledge / Custom Instructions to make it live.

## What v10.8 changes vs live v10.6

### Standing rule #6 — REWRITTEN
**Before (v10.5/v10.6):** Operative plan = `workplan/workplan-co0007-v4.md`. All content work maps to Stage C1–C11.
**After (v10.8):** Operative plan = `audits/bpc-rewrite-workplan-2026-05-11.md`. workplan-co0007-v4 SUPERSEDED. All work maps to Phases A–G. STRICT SEQUENTIAL B before E. Aggregate effort ~2300 hours.

### Standing rule #8 — UNCHANGED from v10.7
PMP protocol for numerical-spec items (per DR-2026-05-10). This rule was introduced in v10.7 (drafted in repo as `governance/project-instructions-v10_7.md` but never deployed to live). v10.8 inherits it unchanged.

### Standing rule #9 — NEW
Cross-jurisdictional synthesis 9-step rule (locked in session_2026-05-11h). Every parameter with ≥3 jurisdictions specifying different values must apply 9 explicit steps. Tier 4 / Tier 5 grouped with statutory codes in Step 3 jurisdiction comparison; not used as Step 5 evidence. Multilingual coverage 19 langs × 46 jurisdictions per `multilingual-research_SKILL.md`. Disability-centric framing locked.

### Standing rule #10 — NEW
Evidence verification gate. No synthesis claim may cite `metadata_quality = AUTHOR-TITLE-ONLY` or `verification_status = NULL`. Current state: 86% of sources are ineligible (must be rehabilitated in workplan Phase B before Phase E synthesis can run). 2026-03-30 Opus syntheses (~30 BPCs) carry retraction banner until Phase E.2g overwrites.

### Reference files — EXTENDED
Three new directories created in Phase A:
- `references/bpc-reasoning/<slug>.md`
- `references/connection-reasoning/<con-id>.md`
- `references/keyword-compendiums/<lang>.md`

### Bootstrap status block — EXTENDED
Now reports: AUTHOR-TITLE-ONLY count, verification_status NULL count, BPC reasoning doc coverage, connection reasoning doc coverage. Operative workplan line shows `bpc-rewrite-workplan-2026-05-11 (LIVE) | superseded: workplan-co0007-v4`.

## Files affected (already in repo)

- `audits/bpc-rewrite-workplan-2026-05-11.md` — the new operative workplan
- `governance/project-instructions-v10_8.md` — v10.8 PI staged
- `sessions/session_2026-05-11h-bpc-rewrite-workplan-design.md` — session record of adoption
- `decisions/DR-2026-05-10-progressive-measurement-protocol.md` — PMP decision record (v10.7)
- `decisions/DR-2026-05-09-adversarial-research-protocol.md` — adversarial protocol decision record (v10.6)

## Owner action checklist

- [ ] Open claude.ai → Project Settings → Custom Instructions / Project Knowledge
- [ ] Replace live PI (currently v10.6) with content of `governance/project-instructions-v10_8.md`
- [ ] Verify version line reads "V10.8 · Revised 2026-05-11"
- [ ] Verify standing rules now go 1 through 10
- [ ] Save; next chat will bootstrap under v10.8
- [ ] Optional: archive `decisions/PI-update-needed.md` (this file) once v10.8 is live

## Prior queue items (now resolved or rolled into v10.8)

- DR-2026-05-09 adversarial protocol → folded into v10.6 rule #7 (already live)
- DR-2026-05-10 PMP protocol → folded into v10.7 rule #8 (was drafted, never deployed; now in v10.8)
- BPC rewrite workplan adoption → new in v10.8 rules #6/#9/#10

This document supersedes the prior v10.6-only deployment instructions.
