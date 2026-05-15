# Handoff — Resume Data-Integrity Verification

**Repo:** `jordanelias/guidebook`
**Branch:** `main`
**HEAD:** `de364a88` ("governance: add data-integrity verification plan…")
**Last session record:** `sessions/session_2026-05-13b-evidence-verification-methodology.md`
**Latest PI version in repo:** `governance/project-instructions-v10_10.md` (live in claude.ai still = v10.6 unless you've pasted v10.10)

---

## Paste this into the new conversation

> I'm resuming the Guidebook data-integrity verification work. Bootstrap normally per PI. Then read these three files in order, fully:
>
> 1. `audits/data-integrity-verification-plan.md` — the operative plan; 6 phases, sequenced.
> 2. `audits/verification-coverage-catalog-2026-05-13b.md` — what was verified vs claimed at end of session_2026-05-13b. Plan supersedes catalog for forward work; catalog kept for evidence.
> 3. `architecture/project-architecture-guidebook-v2.3.md` — universal patterns, especially `<enforcement_spectrum>` and `<migration_and_growth>`.
>
> Then execute **Phase 1.1** of the plan: push a trivial commit to trigger CI, watch `.github/workflows/audit.yml`, confirm the migration-reproducibility job passes. If it fails, fix before doing anything else. If it passes, proceed to Phase 1.2 (confirm FK integrity is a blocking CI check; add the job if it isn't) then Phase 1.3 (write `scripts/audit/validate_pydantic_schemas.py`).
>
> Do not skip phases. Do not start Phase 2 until Phase 1 closes.

---

## Current state at handoff

**Phase 1 (Data layer sound) — not started**
- 1.1 trigger CI run: **next action**
- 1.2 FK integrity blocking in CI: unknown — need to inspect `.github/workflows/audit.yml`
- 1.3 Pydantic-vs-SQLite drift audit: known drift exists in `schemas/evidence_source.py` (5 fields in Pydantic gone from DB; 64 DB columns missing from Pydantic). Audit script not yet written.
- 1.4 Direct-write detection test: not started

**Phase 2 (Rows grounded) — partially in place**
- 2.1 evidence verification gate audit `scripts/audit/audit_evidence_metadata.py`: NOT written
- 2.2 `evidence_population_match` audit: NOT written
- 2.3 PMP walks: `scripts/audit/pmp_audit.py` exists and runs; known finding PMP-A02-001-S2 cites REF-00335 which is AUTHOR-TITLE-ONLY (cross-rule signal between rules 8 and 10)
- 2.4 `reasoning_doc_citations`: audit script exists at `scripts/audit/reasoning_doc_citations_audit.py`; corpus not yet populated (Phase E.1 pilot hasn't started)

**Phase 3 (Pipeline faithful) — not started**
- 3.1 generate scripts: paths fixed this session but never executed end-to-end against current DB

**Phase 4 (Sources real) — partial**
- 4.1 DOI resolution workflow `.github/workflows/resolve-dois.yml` exists; never inspected this session
- 4.3 Track 1: 41 records done (Pass 1); ~600 remaining

**Phase 5–6 — depends on 1–4**

---

## Repo state set during session_2026-05-13b

- DB: `data/guidebook.db`, user_version=11, schema_version=11, FK violations=0
- 3 SQL migrations in `scripts/migrations/`: `010_fk_integrity_legacy_to_evidence_sources.sql`, `011_reasoning_doc_citations.sql`, `data_20260513025900_track1_versioning_backfill_pass1.sql` — verified locally to reproduce committed DB state on 14 invariants
- Repo reorg: 134 file moves; top-level reduced to 4 files; `_archived/` populated; `misc/` and `research/` emptied of dated work
- Architecture v2.3 authored (was phantom across v10.3–v10.9), now lives at `architecture/project-architecture-guidebook-v2.3.md`. Pure framing; no logging.
- PI v10.10 drafted at `governance/project-instructions-v10_10.md`. Currently live in claude.ai = v10.6.

---

## Decision queue (do not auto-execute; surface to owner)

- **Paste PI v10.10 to claude.ai project knowledge.** Live = v10.6. v10.10 supersedes v10.7-v10.9 in one paste. Path: claude.ai → Project Settings → Custom Instructions. The PI file is at `governance/project-instructions-v10_10.md`.
- **~14 working-doc files still in `references/`** (theory-gap-analysis.md, throughline-*.md, methodology-*.md, parser-source-readiness.md, phase-b-handoff.md, etc.) — looked stale during session, left for owner triage.
- **Pilot BPC selection for Phase E.1** (`reasoning_doc_citations` workflow) — owner directive needed.
- **`mobile-app-prototype-v9/` in `working/`** — left in place pending owner confirmation it's active.

---

## Known issues to address opportunistically (P1, not blocking)

- `skills/workplan-orchestrator_SKILL.md` has universality violations: 1 hardcoded DB path, 1 absolute path, 8 embedded dates, plus stale embedded skill-index taxonomy (classifies `toc-editor` as deprecated despite PI rule #3 invoking it; missing 11 newer skills). Fix when touching that skill for any reason.
- `scripts/convert/` (18 scripts) never inspected end-to-end this session. JSON inputs in `references/*.json` may be stale.
- 3 rows in `data_migrations` table have row-IDs from the Python migrations that don't match the new SQL filenames. Cosmetic only; doesn't affect CI.

---

## Tools and access

- PAT visible per owner (in PI bootstrap, `gap_register*.md`, and this handoff): `[REDACTED — see PI bootstrap or owner-side notes]`
- Git Data API helper at `/tmp/git_data_api.py` — recreate from session_2026-05-13b transcript if needed
- Effort-level default: `max` per user preferences

---

## Sequencing reminder

Phase 1 is the precondition for everything. If 1.1 fails on first CI run, stop and fix before doing 1.2 or anything in Phase 2. The plan's acceptance criterion (the 6-step claim-verification chain) is the destination, not the next step.
