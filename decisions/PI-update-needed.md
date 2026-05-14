# PI v10.10 Deployment

**Status:** v10.10 committed to repo as `governance/project-instructions-v10_10.md` @ session_2026-05-13b
**Action:** Owner must manually paste v10.10 content into claude.ai project knowledge.

## What changed vs live v10.6

v10.6 → v10.10 in one paste. Cumulative changes:

- **Architecture pointer corrected**: now references `architecture/project-architecture-guidebook-v2.3.md` which actually exists in repo (was phantom in v10.3-v10.9).
- **Standing rule #6** (workplan): operative plan = `audits/bpc-rewrite-workplan-2026-05-11.md`. `workplan-co0007-v4.md` SUPERSEDED. Strict sequential B before E. (v10.8)
- **Standing rule #7** (adversarial research): per DR-2026-05-09. Four required fields per closed gap. (v10.6, already live)
- **Standing rule #8** (PMP): per DR-2026-05-10. PMP walks for numerical specs. Migration 006 applied. (v10.7)
- **Standing rule #9** (9-step cross-jurisdictional synthesis): per BPC rewrite workplan §1. Multilingual 19×46. (v10.8)
- **Standing rule #10** (evidence verification gate): per DR-2026-05-13. Existence verification (Phase B) distinguished from content verification. Three sub-rules by claim type (numerical via PMP; jurisdiction-comparison + qualitative via `reasoning_doc_citations`). (v10.9 → sharpened in v10.10)
- **`<hooks_status>`** rewritten in v10.10: references actual CI workflows (`ci.yml`, `audit.yml`) instead of the phantom `hook-workplan-guidebook.md`.
- **`<skills_assigned>`** clarifies 5 placeholder skills (no file) vs 8 real PI-invoked skills.
- **Bootstrap status block** extended with versioning backfill, reasoning_doc_citations count, PAYWALL candidate count.
- **PI size**: 307 lines (v10.9) → 259 lines (v10.10). State content moved to DRs/DB.

## Schema changes already in DB

- Migration 010: FK integrity (4 tables / 782 rows from `evidence_sources_v1_legacy` → `evidence_sources`)
- Migration 011: `reasoning_doc_citations` table (Track 3 of DR-2026-05-13)
- Data migration: Track 1 first pass — `edition` populated on 41 catalog-fetch records
- user_version 9 → 11; schema_version 6 → 11

## Owner action

- [ ] Open claude.ai → Project Settings → Custom Instructions
- [ ] Replace live PI (currently v10.6) with content of `governance/project-instructions-v10_10.md`
- [ ] Verify version line reads "V10.10 · Revised 2026-05-13"
- [ ] Save; next chat will bootstrap under v10.10
