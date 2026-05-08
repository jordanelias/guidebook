<!-- DEPRECATED 2026-05-08 — excised from workplan/website-preparation.md -->
<!-- Contains all Phase A Block sequencing, Phase B tech stack, session estimates, -->
<!-- gap register breakdown, parser readiness audit, and other content superseded -->
<!-- by workplan-co0007-v4.md (ADOPTED 2026-05-03). -->
<!-- Tactical reference for Block 2 per-file pipeline remains in the active file. -->
# Website Preparation — Excised Content (Archive)
**Original document:** workplan/website-preparation.md v2.0 (2026-04-17)
**Excised:** 2026-05-08 per workplan-reconciliation-2026-05-08.md
**Reason:** Content superseded by workplan-co0007-v4.md Stage C structure. Phase A Block sequencing (0→1→2→3→4→5) replaced by v4 C-stage page-type organization. Phase B tech stack deferred per v4.

---

## Excised §0 — Changelog (historical)

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-17 | Initial integration of website-preparation v2 + build guide + ecosystem guide |
| 2.0 | 2026-04-17 | Audit remediation: enforcement-first sequencing, gate definitions, per-block token budgets, pipeline specs, conflict resolution, checkpoints, rollback protocol |

---

## Excised §2 — Staging Logic

Three documents governed this workplan (now superseded by v4):
- Website-preparation v2: 8 entity types, 5 interactive tools, 20 page types, 3 community layers, 4 navigation axes.
- Build guide: Claude Code + Next.js + PostgreSQL + Directus + Meilisearch + Vercel. 26 parsers.
- Ecosystem guide: code enforces, prose suggests.

Phase A (Blocks 0-5, 28-42 sessions) → Phase B (Claude Code, 43-70 sessions). Total 71-112 sessions.

**Superseded by:** v4 Stage C (121-177 sessions) + deferred B5-B7.

---

## Excised §3 — Parser Readiness Audit

26 parsers + 4 v2 additions. Full detail in commit 1551dcc52553.

| Tier | Parsers | Readiness |
|---|---|---|
| 1 (reference) | 5 | 4 need format audit; 1 manual |
| 2 (core) | 4 | 1 major gap (p11 sources — BPC migration needed) |
| 3 (complex) | 5 | Spec DB reconciliation needed; 6 stub items |
| v2 additions | 4 | Standards registry expansion; Brief Builder logic validation |
| 4 (dependent) | 6 | Gap register split needed |
| 5 (join tables) | 6 | Depend on A1 + A7 |

**Status:** Pending reconciliation per v4 C1 ("Map the 26 website-preparation.md parsers to post-D-0138 pipeline roles").

---

## Excised §4 — Gap Register Breakdown

### Category A: Must complete (parser blockers)

| # | Gap | Sessions | Status (2026-05-08) |
|---|---|---|---|
| A1 | BPC Key sources migration (70 files → CO-0006 REF-ID) | 6-8 | IN PROGRESS (some files migrated) |
| A2 | Spec DB ↔ Part 4 reconciliation | 2-3 | COMPLETE (file exists) |
| A3 | Gap register split | 0.5 | COMPLETE (2026-05-08 this session) |
| A4 | 6 stub item specs + E-10 duplicate | 1-2 | Status unclear |
| A5 | Standards registry expansion (29 → 100-150) | 1-2 | Status unclear |
| A6 | Brief Builder logic validation | 1 | Status unclear |
| A7 | Part 4 v2 field enrichment | 2-3 | Status unclear |

### Category B: Should complete

| # | Gap | Status |
|---|---|---|
| B1 | Consume 96 PENDING connections | 6 PENDING remain; 215 CONSUMED; 44 CONSUMED-DEFERRED |
| B2 | Priority SRs (Rashid, Quesada-Cubo, Simpson) | Status unclear |
| B3 | GRADE ratings Categories A, E, G | Status unclear |
| B5 | Hallucination audit (60 BPC files) | Status unclear |

### Category C: Ecosystem hardening — covered by CO-0008 infrastructure pour.

---

## Excised §5 — Phase A Schedule (Blocks 0, 1, 3, 4, 5)

### Block 0: Enforcement Infrastructure — COMPLETE
validate_bpc.py, validate_cross_refs.py, ci.yml all exist. CI running.

### Block 1: Cleanup + Format Audit — COMPLETE (per v4 B2)
parser-source-readiness.md exists. gap_register_archive.md created 2026-05-08.

### Block 2: Session Batching (excised from active doc; per-file pipeline retained)

| Session | Topic directories | File count |
|---|---|---|
| 2.1 | bathrooms + seating + room-types + controls + kitchens | 7 |
| 2.2 | communication + economics | 8 |
| 2.3 | entrances + wayfinding | 14 |
| 2.4 | sensory-environment | 11 |
| 2.5 | health + population-general first half | 13 |
| 2.6 | population-general second half + frameworks first half | 15 |
| 2.7 | frameworks second half | 9 |
| 2.8 | Buffer | — |

Token budgets: session-start ~40K, per-session ~70K.

### Block 3: Specification Completeness — superseded by v4 C3 (25-35 sessions, larger scope)

### Block 4: Evidence Quality + Connection Consumption — superseded by v4 C3/C7

B1 Connection Consumption Pipeline (per connection):
1. READ connection from topic file
2. RESOLVE primary_target(s) to Part 4 item codes
3. READ each target Part 4 item
4. READ evidence BPC slug(s)
5. DETERMINE synthesis direction
6. WRITE cross-reference to Part 4 item
7. UPDATE connection status
8-12. Status updates + validate + commit

### Block 5: Final Readiness Audit — superseded by v4 C10

---

## Excised §8 — Phase B: Claude Code Build

Deferred per v4 ("Does not commit to a website technology stack"). Phase B follows build guide: Next.js + PostgreSQL + Directus + Meilisearch + Vercel. 26 parsers. Phase B enforcement: PostgreSQL constraints, parser tests, axe-core + Lighthouse, CI.

---

## Excised §9 — Session Estimates

Phase A: 28-42 sessions. Phase B: 43-70 sessions. Total: 71-112 sessions.
**Superseded by:** v4 budget arithmetic (188-253 sessions total, 146-211 remaining).

---

## Excised §10 — Open Decisions

| # | Question | Status (2026-05-08) |
|---|---|---|
| 1 | Domain name | Phase B — deferred |
| 2 | V9 vs V10 at launch | RESOLVED: V10 only (CO-0004 renumbering) |
| 3 | Supplementary populations in MVP | RESOLVED: deferred (11 main populations per v4) |
| 4-9 | Phase B questions | All deferred |

---

## Excised §11 — Data Artifacts Produced in Phase A

Superseded by v4's data/ directory structure (Pydantic schemas, YAML entities, SQLite).

---

## Excised §12 — Cancelled Work

Historical record of scope superseded by this workplan. Now doubly superseded by v4.
