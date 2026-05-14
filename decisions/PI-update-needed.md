# PI v10.9 Update Required — DEPLOYMENT TO LIVE PROJECT SETTINGS

**Status:** v10.9 committed to repo as `governance/project-instructions-v10_9.md` @ session_2026-05-13b
**Action:** Owner must manually paste v10.9 content into claude.ai project knowledge / Custom Instructions to make it live.

Note: v10.8 was never deployed (live remained at v10.6 throughout session 2026-05-12 and 2026-05-13a). v10.9 supersedes v10.8 and folds in everything v10.8 staged plus DR-2026-05-13 changes. Single paste replaces v10.6 → v10.9 in one step.

## What v10.9 changes vs live v10.6 (cumulative)

### Standing rule #6 — REWRITTEN (from v10.8)
**Before (v10.5/v10.6):** Operative plan = `workplan/workplan-co0007-v4.md`. All content work maps to Stage C1–C11.
**After (v10.9):** Operative plan = `audits/bpc-rewrite-workplan-2026-05-11.md`. workplan-co0007-v4 SUPERSEDED. All work maps to Phases A–G. STRICT SEQUENTIAL B before E. Aggregate effort ~2300 hours.

### Standing rule #7 — UNCHANGED from v10.6
Adversarial research protocol (per DR-2026-05-09). Already in v10.6.

### Standing rule #8 — INHERITED from v10.7 (never deployed live)
Progressive Measurement Probe (PMP) protocol for numerical-spec items (per DR-2026-05-10). `progressive-measurement` is one of the PI-invoked skills. Migration 006 applied tracking-DB changes for this rule (`spec_value_probes` table + `items.pmp_*` columns + `v_pmp_latest_walk` view).

### Standing rule #9 — NEW (from v10.8)
Cross-jurisdictional synthesis 9-step rule (locked in session_2026-05-11h). Every parameter with ≥3 jurisdictions specifying different values must apply 9 explicit steps. Tier 4 / Tier 5 grouped with statutory codes in Step 3 jurisdiction comparison; not used as Step 5 evidence. Multilingual coverage 19 langs × 46 jurisdictions per `multilingual-research_SKILL.md`. Disability-centric framing locked.

### Standing rule #10 — SHARPENED in v10.9 per DR-2026-05-13

Was (v10.8 staged): existence verification gate only — `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.

Now (v10.9): existence gate **plus** content-verification sub-rules by claim type:
1. **Numerical-spec claims**: must additionally cite a `spec_value_probes` walk passing strict termination (rule #8) or a logged `pmp_waiver`.
2. **Jurisdiction-comparison cells (rule #9 step 3)**: must have a corresponding `reasoning_doc_citations` row with `value_match ∈ {EXACT, WITHIN-TOLERANCE}` from a re-read. `PAYWALL` requires downgrade or non-paywalled corroborating source.
3. **Qualitative/definitional claims**: must have a `reasoning_doc_citations` row with `claim_match ∈ {SUPPORTED, PARTIAL}`. `CONTRADICTED` invalidates.

Plus Track 3 pilot mandate: first Phase E.1 BPC under reasoning_doc_citations workflow runs as formal pilot with inline review before scaling.

### Skills — EXTENDED
`reasoning-doc-citations` added to PI-invoked skills (per DR-2026-05-13 Track 3). Placeholder; `skills/reasoning-doc-citations_SKILL.md` to be authored in Phase A parallel-track.

### Bootstrap status block — EXTENDED (cumulative v10.8 + v10.9)
Now reports: P1 OPEN, PMP backlog, AUTHOR-TITLE-ONLY count, verification_status NULL count, BPC reasoning doc coverage, connection reasoning doc coverage, **versioning backfilled count** (new v10.9), **reasoning_doc_citations row count** (new v10.9), **PAYWALL purchase candidates flagged** (new v10.9). Operative workplan line shows `bpc-rewrite-workplan-2026-05-11 (LIVE)`.

### Bootstrap status block — fix for backend portability
v10.9 bootstrap section uses both `gh` and `curl` paths for `references/bpc-reasoning/` and `references/connection-reasoning/` counts (was `gh`-only in v10.8). Bootstrap now works on machines without the `gh` CLI installed.

### Reference files — UNCHANGED from v10.8
Three reference directories from Phase A:
- `references/bpc-reasoning/<slug>.md`
- `references/connection-reasoning/<con-id>.md`
- `references/keyword-compendiums/<lang>.md`

## Files affected (already committed to repo this session)

- `decisions/DR-2026-05-13-evidence-verification-methodology.md` — the decision record adopted under owner delegation
- `governance/project-instructions-v10_9.md` — v10.9 PI staged
- `scripts/migrations/010_fk_integrity_legacy_to_evidence_sources.py` — FK fix migration
- `scripts/migrations/011_reasoning_doc_citations.py` — Track 3 schema
- `scripts/migrations/data_20260513_track1_versioning_backfill_pass1.py` — Track 1 first pass
- `scripts/audit/pmp_audit.py` — written this session (was a placeholder in v10.8 rule #8)
- `scripts/audit/reasoning_doc_citations_audit.py` — new audit for Track 3
- `sessions/session_2026-05-13b-evidence-verification-methodology.md` — session record
- `data/guidebook.db` — schema_version 6→11; user_version 9→11

## Owner action checklist

- [ ] Open claude.ai → Project Settings → Custom Instructions / Project Knowledge
- [ ] Replace live PI (currently v10.6) with content of `governance/project-instructions-v10_9.md`
- [ ] Verify version line reads "V10.9 · Revised 2026-05-13"
- [ ] Verify standing rules now go 1 through 10 (rule #10 includes the three content-verification sub-rules per claim type)
- [ ] Save; next chat will bootstrap under v10.9
- [ ] Optional: archive `decisions/PI-update-needed.md` (this file) once v10.9 is live

## Prior queue items (now rolled into v10.9)

- DR-2026-05-09 adversarial protocol → in v10.6 rule #7 (already live)
- DR-2026-05-10 PMP protocol → v10.7 rule #8 (was drafted, never deployed; now in v10.9)
- BPC rewrite workplan adoption → v10.8 rules #6/#9/#10 (was drafted, never deployed; now in v10.9)
- DR-2026-05-13 evidence verification methodology → v10.9 rule #10 sharpening + skills extension

This document supersedes the prior v10.6-only and v10.8 deployment instructions.
