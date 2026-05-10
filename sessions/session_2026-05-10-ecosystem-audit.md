# Session: 2026-05-10 — Ecosystem Audit + Integrity Fixes
**Model:** [MODEL-CONFLICT: system Opus 4.6 — not independently verifiable]
**session_close:** 2026-05-10 08:30 UTC
**next_action:** (1) C3 items.bpc_source_slug population via CO-0009 item audit pipeline; (2) S3 populate conflicts table from cross-pop BPC; (3) 2A.1/2A.3/2A.4/2A.5 BPC remediation drafts (carried from prior session); (4) MH BPC citation corrections (Faerden, Weltens, van der Schaaf).
**blockers:** C3 requires domain judgment (91 items → slug mapping); not automatable.

**github_writes:**
- `references/audits/ecosystem-audit-2026-05-10.md` — full audit report
- `references/audits/ecosystem-resolution-summary.md` — resolution summary
- `data/guidebook.db` — C1 fix (701 dup ssl deleted), C2 fix (16 orphans), S1 (jurisdiction normalized), minor (3 targetless conn)

**commit_oids:**
- Audit + C2: `768ecb78`
- C1 + S1 + minor: `353101c8`
- Resolution summary + session: (this commit)

---

## What was done

### Ecosystem audit
Full integrity audit of 19 SQLite tables (~6,400 rows): FK constraints, cross-table pipeline traces, jurisdictional coverage (23→33 codes), multilingual coverage (14 languages), evidence tier distribution, connection pipeline, gap consistency.

### Fixes applied
- **C1 (critical):** 701 orphaned source_slug_links rows were duplicates — same source linked via both local_ref_id and global ref_id. Deleted duplicates. FK violations: 717 → 0.
- **C2 (critical):** 16 bpc_metadata rows for population/utility files without slug entries. Deleted.
- **S1 (structural):** 30 non-standard jurisdiction codes normalized. Compound codes split to primary. Language codes (DA/JA/ZH) mapped to country codes. Regional groups → INT.
- **Minor:** 3 targetless connections deleted.

### Deferred
- C3: items.bpc_source_slug — all 91 NULL. Needs CO-0009 item audit pipeline.
- S3: citation_mining, conflicts, decisions tables empty. Pipeline not started.
- 12 unlinked REF-VERIFIED-* sources. 1 NULL-tier internal ref. 11 unlinked terms.

## Post-fix state
- 0 FK violations
- 33 clean jurisdiction codes
- 654 evidence sources (58% Tier 1-3)
- 81 slugs with full coverage tracking

---
**End session.**
