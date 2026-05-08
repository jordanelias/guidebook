<!-- PARTIAL-SUPERSESSION NOTICE 2026-05-08 04:16 -->
> **⚠ PARTIAL SUPERSESSION:** PARTIALLY SUPERSEDED by workplan-co0007-v4.md (ADOPTED 2026-05-03). Phase A Blocks 0-5 are subsumed into v4 Stage C. Phase B tech stack is a deferred decision per v4. Block 2 per-file migration pipeline remains valid as tactical reference for C1/C7 work. 26-parser architecture is pending reconciliation per v4 C1 item. Do not use Block sequencing (0→1→2→3→4→5) for session planning — use v4 C-stage structure instead. See workplan-reconciliation-2026-05-08.md §3.

# Workplan: Research Processing → Website Build
**Version:** 2.0
**Created:** 2026-04-17
**Revised:** 2026-04-17 (v2.0 — integrated audit remediation)
**Supersedes:** v1.0 (commit 1551dcc52553)
**Sources:** Website-preparation v2 + Build guide + Ecosystem guide + Ecosystem restructure guidelines
**Staging:** All Claude.ai research processing completes before Claude Code begins.
**Status:** DRAFT — requires user review before execution

---

## 0. Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-17 | Initial integration of website-preparation v2 + build guide + ecosystem guide |
| 2.0 | 2026-04-17 | Audit remediation: enforcement-first sequencing (Block 0 added); gate definitions; programmatic transition criteria; per-block token budgets; pipeline specs for A1 and B1; conflict resolution for concurrent Part 4 work; per-block checkpoints; rollback protocol; data artifact filepaths |

---

## 1. Glossary

| Term | Meaning |
|---|---|
| **BPC** | Best Practices Compendium — per-topic research files in `references/bpc/{topic}/{slug}.md` |
| **FDR** | Functional Deficit Researcher — skill that generates specifications from ICF functional needs |
| **ISW** | Item Specification Writer — skill that produces Part 4 item spec entries |
| **Opus synthesis** | Cross-evidence judgment produced by Opus sessions; Sonnet never determines best practice |
| **CO-0006** | Change Order that restructured connection register and established BPC Key sources REF-ID schema |
| **REF-ID** | Sequential integer (01, 02, …) identifying a source within a single BPC entry's Key sources table |
| **CON-ID** | Global connection identifier (CON-0001 through CON-0180+) |
| **GRADE** | Grading of Recommendations Assessment, Development and Evaluation — evidence confidence framework |
| **Co-1** | First-tier lived experience evidence (CRPD Art. 4.3 aligned) |
| **DAR** | Design for Adaptable Readiness |
| **Universal Mode/1/2** | Universal / Population-informed / Person-specific design hierarchy |
| **Parser source** | A file in `guidebook` repo that Phase B parsers read |

---

## 2. Staging Logic

Three documents govern this workplan:

- **Website-preparation v2** defines what the website contains: 8 entity types, 5 interactive tools, 20 page types, 3 community layers, 4 navigation axes.
- **Build guide** defines how it gets built: Claude Code + Next.js + PostgreSQL + Directus + Meilisearch + Vercel. 26 parsers.
- **Ecosystem guide** defines enforcement patterns: code enforces, prose suggests.

**Two phases, one transition:**

```
PHASE A: CLAUDE.AI (guidebook repo)                      28–42 sessions
  Block 0: Enforcement infrastructure          (2–3 sessions)
  Block 1: Cleanup + format audit              (2–3 sessions)
  Block 2: Citation migration                  (6–8 sessions)  ┐
  Block 3: Specification completeness          (5–8 sessions)  ├ sequential with
  Block 4: Evidence + connection consumption   (12–18 sessions)┘ coordination
  Block 5: Final readiness audit               (1–2 sessions)

      ↓ transition: programmatic criteria pass

PHASE B: CLAUDE CODE (website repo)                      43–70 sessions
  Build guide S1 onward
```

**Total: 71–112 sessions.** Phase A work runs in Claude.ai because it depends on the existing guidebook project ecosystem (skills, session protocol, Opus model routing) which does not exist in Claude Code.

---

## 3. Parser Readiness Audit

The build guide defines 26 parsers plus 4 v2 additions (functional tasks, extended standards, engineering coordination, Brief Builder logic). Full parser/source/readiness audit is preserved from v1.0 §2 — unchanged. See commit `1551dcc52553` for detail. Summary:

| Tier | Parsers | Readiness |
|---|---|---|
| 1 (reference) | 5 parsers | 4 need format audit; 1 manual |
| 2 (core) | 4 parsers | 1 major gap (p11 sources — BPC migration needed) |
| 3 (complex) | 5 parsers | Spec DB reconciliation needed; 6 stub items |
| v2 additions | 4 parsers | Standards registry expansion; Brief Builder logic validation |
| 4 (dependent) | 6 parsers | Gap register split needed |
| 5 (join tables) | 6 parsers | Depend on A1 + A7 |

---

## 4. Gap Register

### Category A: Must complete (parser blockers)

| # | Gap | Sessions | Priority |
|---|---|---|---|
| A1 | BPC Key sources migration (70 files → CO-0006 REF-ID schema) | 6–8 | P1 |
| A2 | Spec DB ↔ Part 4 reconciliation | 2–3 | P1 |
| A3 | Gap register split (active/archive) | 0.5 | P1 |
| A4 | 6 stub item specs in Part 4 (and E-10 duplicate resolution) | 1–2 | P2 |
| A5 | Standards registry expansion (29 → 100–150) | 1–2 | P2 |
| A6 | Brief Builder logic validation (Part 3 §3.8 + Part 9 §9.2.2) | 1 | P2 |
| A7 | Part 4 v2 field enrichment (design_stage_lock, ve_risk, ot_appointment_trigger) | 2–3 | P1 |

### Category B: Should complete (data quality — all required per user decision)

| # | Gap | Sessions | Priority |
|---|---|---|---|
| B1 | Consume all 96 PENDING connections | 10–14 | P2 |
| B2 | Integrate priority Tier 3 SRs (Rashid 2025, Quesada-Cubo 2025, Simpson 2025) | 3–4 | P2 |
| B3 | Apply GRADE confidence ratings to priority categories (A, E, G) | 3–4 | P2 |
| B4 | Evidence density statements (voice-style pass + insertion) | 1 | P3 |
| B5 | BPC hallucination audit (remaining 20 of 60 files) | 2–3 | P2 |

### Category C: Ecosystem hardening

| # | Gap | Sessions | Priority |
|---|---|---|---|
| C1 | Guidebook repo CI (syntax, register sizes, commit message format) | 1 | P1 — moved to Block 0 |
| C2 | Session archive (pre-April sessions) | 0.5 | P3 |
| C3 | Source format standardisation (fix issues found in Block 1 audit) | 2 | P2 |

---

## 5. Phase A Schedule

### Block 0: Enforcement Infrastructure (2–3 sessions) — NEW, runs first

**Purpose:** Establish validation gates before any content modification. Following the ecosystem guide's principle: "Start with hooks + CI from day one. Retrofitting enforcement is 10× harder."

**Session-start loading budget:** ~15K tokens (workplan-orchestrator 8K + project-standards 2K + github-io skill 3K + existing gap_register skim 2K — no full-file loads).

| Task | Description | Output |
|---|---|---|
| 0.1 | Write `scripts/validate_bpc.py` — standalone validator that reads a BPC file and confirms: all 8 mandatory sections present (per research-log-manager Pre-LOG Completeness Check); Key sources section has valid CO-0006 REF-ID table OR legacy flat format (transition state); Metadata YAML parses. Returns exit code 0 on pass, non-zero with structured error message on fail. | `scripts/validate_bpc.py` |
| 0.2 | Write `scripts/validate_cross_refs.py` — scans repo for references and validates targets exist. Checks: slug references resolve via slug-registry.md; CON-IDs resolve to connection index; Part section references (§X.Y) resolve to existing headings; BPC ↔ search-log co-existence (every BPC has matching search-log, vice versa). | `scripts/validate_cross_refs.py` |
| 0.3 | Write `scripts/check_thresholds.py` — file size checker. Thresholds: session log 2K tokens, gap_register (active) 5K, project-standards 10K, connections/_index.md 8K, slug-registry 6K. Exit non-zero on overage. | `scripts/check_thresholds.py` + threshold definitions |
| 0.4 | Write `.github/workflows/ci.yml` — three jobs: `syntax` (all .md/.json/.yaml parseable), `structure` (runs 0.1 on changed BPC files, 0.2 on full repo, 0.3 on all governed files), `commit-msg` (validates `{skill}: {action} [{YYYY-MM-DD HH:MM}]` format on HEAD commit). | `.github/workflows/ci.yml` |
| 0.5 | Test CI: make a deliberately invalid commit (malformed BPC section) → confirm CI blocks. Make a valid commit → confirm CI passes. Enable branch protection on `main` requiring all three jobs. | Branch protection configured |
| 0.6 | Document validators in `references/project-standards.md` under new section: **Enforcement Gates**. List each validator, what it checks, how to interpret failure output. | project-standards.md update |

**Checkpoint at Block 0 end:**
- [ ] All 3 validators exist and tested locally
- [ ] CI passes on clean main
- [ ] CI blocks deliberate violations
- [ ] Branch protection enabled
- [ ] Rollback: if any validator proves too strict during Block 1, relax via PR (don't remove validation entirely)

### Block 1: Cleanup + Format Audit (2–3 sessions)

**Purpose:** Produce the parser source readiness report and execute safe file moves. Now protected by Block 0 CI.

**Session-start loading budget:** ~40K tokens. Per session: workplan-orchestrator + gap_register + connections/_index + 3–5 parser source files at a time.

**Path mapping discipline** (from ecosystem restructure guidelines §3.1–3.2): before any file move, build complete old→new path mapping. Scan for references in: slug-registry, connections/_index, skills/*.md, workplan/*.md, gap_register, project-standards.

| Task | Description | Output | Session |
|---|---|---|---|
| A3 | Gap register split. Path map: `gap_register.md` → `gap_register.md` (active) + `gap_register_archive.md` (CLOSED). Validate references in session files, skills, workplan files. Atomic commit. | 2 files + reference updates | S1 |
| C2 | Session archive. Move pre-2026-04-01 sessions to `sessions/_archive/`. Verify LATEST pointer unaffected. Atomic batch commit. | Reduced sessions/ directory | S1 |
| Audit 1/3 | Source format audit: standards-registry, glossary (back matter), Part 2, Part 3 §3.3/§3.9/§3.11. Write findings to `references/parser-source-readiness.md`. | `parser-source-readiness.md` (part 1) | S1 |
| Audit 2/3 | Source format audit: Part 4, Part 5, Part 6, Part 7. Append to `parser-source-readiness.md`. | `parser-source-readiness.md` (part 2) | S2 |
| Audit 3/3 | Source format audit: Part 8 (§8.1, §8.3.3), Part 9 (§9.2.2), Part 10 (§10.1), Part 12, bibliography-v9. Append to `parser-source-readiness.md`. | `parser-source-readiness.md` complete | S2 or S3 |
| A5 (audit) | During Part audits: count standards in BPC jurisdiction_coverage sections not in standards-registry. Append to readiness report as "Standards registry gap: N missing". | Quantified gap in readiness report | within S2–S3 |
| A6 | Part 3 §3.8 decision tree + Part 9 §9.2.2 OT trigger audit. Test every population pair combination. Flag gaps or contradictions. Append to readiness report. | Validation matrix in readiness report | S3 |

**Parser source readiness report schema** — written to `references/parser-source-readiness.md`:
```yaml
# Per file/section
file: parts/v10/part04.md
section: §4.X or full file
parser_consumer: p09_specifications, p18_categories
format_summary: "### heading per item code, YAML-like fields, HTML comment CON annotations"
known_patterns:
  - item_code_format: "### {A-K}-NN (title)"
  - parameters_format: "...|...|..."
edge_cases:
  - "6 items lack quantified Specifications block (stubs)"
  - "CON annotations appear in HTML comments"
audit_status: PASS | PASS-WITH-NOTES | FAIL
audit_date: 2026-04-17
```

**Checkpoint at Block 1 end:**
- [ ] `gap_register.md` (active) < 5K tokens
- [ ] `gap_register_archive.md` contains all CLOSED items
- [ ] `sessions/_archive/` contains pre-April sessions
- [ ] `references/parser-source-readiness.md` complete for all 18 source sections
- [ ] Standards registry gap quantified
- [ ] Brief Builder logic validation matrix complete
- [ ] CI passes

### Block 2: Citation Infrastructure (6–8 sessions)

**Purpose:** Migrate all 70 BPC files from flat Key sources lists to CO-0006 REF-ID table schema. This is the largest blocker for p11_sources and p25_spec_sources.

**Session-start loading budget:** ~40K tokens (standard).

**Per-session loading budget:** ~70K tokens
- Session-start: 40K
- 10 BPC files × ~2K tokens each: 20K
- CO-0006 schema reference: 2K
- Corresponding search-log files (for disposition update): 5K
- Working room: 13K

**Batch plan:** ~10 files per session, organised by topic directory.

| Session | Topic directories | File count |
|---|---|---|
| 2.1 | bathrooms-and-wet-areas (3) + seating-and-rest (1) + room-types (1) + controls-and-hardware (1) + kitchens-and-workspaces (1) | 7 |
| 2.2 | communication-and-alerts (4) + economics (4) | 8 |
| 2.3 | entrances-and-circulation (6) + wayfinding-and-signage (8) | 14 |
| 2.4 | sensory-environment (11) | 11 |
| 2.5 | health-and-symptom-management (7) + population-general first half (6) | 13 |
| 2.6 | population-general second half (6) + frameworks-and-methodology first half (9) | 15 |
| 2.7 | frameworks-and-methodology second half (9) | 9 |
| 2.8 | Buffer session for oversize files and validation retries | — |

**A1 Migration Pipeline (per file):**
```
1. READ current BPC file
2. EXTRACT existing Key sources section (flat list or partial table)
3. IDENTIFY each source: authors, year, title, publisher, DOI/URL, tier, language, jurisdictions
4. NORMALIZE into CO-0006 table rows with sequential REF-IDs (01, 02, 03...)
5. VALIDATE: every source has all required fields (or [GREY] for missing DOI)
6. WRITE new Key sources section replacing old
7. UPDATE corresponding search-log disposition field
8. ATOMIC COMMIT: BPC + search-log in same commit (co-file rule)
9. VALIDATE: run validate_bpc.py locally before commit
10. CI RUN: confirms structure gate passes
```

**Error handling:**
- Source has missing fields → [GREY] placeholder + gap register entry GAP-CITE-NNN
- Source cannot be parsed → session-local blocker, move to next file, flag in session close
- validate_bpc.py fails → fix inline, re-commit (CI re-runs automatically)
- Tier classification ambiguous → default to lowest applicable tier, flag for Opus review

**Per-session checkpoint:**
- [ ] All files in session's batch migrated
- [ ] CI green on all session commits
- [ ] Search-log dispositions updated
- [ ] Session log records: files migrated, REF-IDs assigned, gaps raised

### Block 3: Specification Completeness (5–8 sessions)

**Purpose:** Complete Part 4 item specs, annotate with v2 fields, reconcile against spec DB, expand standards registry.

**Part 4 coordination note:** Both Block 3 (A4, A7) and Block 4 (B1) modify Part 4. To prevent conflicts:
- **Block 3 and Block 4 do not run in the same session.**
- **Block 3 A4 + A7 must complete before Block 4 begins any B1 work.**
- After Block 3 closes, Part 4 is stable for Block 4's connection-based enrichment.
- This means Block 2 and Block 3 can run in parallel (different files: BPC vs Part 4), but Block 4 waits for Block 3.

**Session-start loading budget:** ~40K tokens.

**Per-session loading budget:** ~100K tokens
- Session-start: 40K
- Part 4 (63K) required for A4 (stubs scattered), A7 (every item), A2 (all items)
- Working room: variable

**Note:** Part 4 at 63K tokens is the dominant load. To mitigate: create a **Part 4 item index** at start of Block 3 — a file listing `{item_code: line_range}` for every item (~2K tokens). Future sessions load only the item ranges they need. Item count resolved during Block 1 audit (raw count 91 with E-10 duplicate — see A4).

| Task | Description | Session | Loading |
|---|---|---|---|
| 3.0 | Create `references/part04-item-index.md` — machine-readable index of item_code → line_range. | 3.1 | Full Part 4 (one-time) |
| A4 | Complete 6 stub item specs (identifiers to be determined in Block 1 audit). Resolve E-10 duplicate (Part 4 lines 1736 and 3204 have two entries for "E-10 Rest Seating on Circulation Routes" with different content — merge or rename). Use ISW at effort 125. | 3.1–3.2 | item-index + stub ranges + relevant BPC |
| A7 | Enrich every item with design_stage_lock (from Part 8), ve_risk (Part 8 §8.3.3), ot_appointment_trigger (Part 9 §9.2.2). Use HTML comment annotation format: `<!-- design_stage_lock: SD -->` etc. | 3.3–3.5 | item-index + Part 8 + Part 9 |
| A2 | Spec DB reconciliation: identify (a) Part 4 items without BPC coverage, (b) spec DB records without Part 4 mapping, (c) field-level discrepancies. Write to `references/spec-db-part4-reconciliation.md`. | 3.6 | item-index + spec DB + slug-registry |
| A5 (exec) | Consolidate BPC jurisdiction standards into standards-registry.md. Target ≥80% of standards referenced in BPC files. | 3.7 | standards-registry + BPC jurisdiction sections |
| B3 (partial) | GRADE confidence ratings for Category A, E, G items. Use evidence-auditor at effort 125. | 3.7–3.8 | item-index + ratings criteria + relevant BPC |

**A7 annotation format decision:** HTML comments. Rationale: (a) invisible in rendered markdown so Part 4 remains readable, (b) parseable by Claude Code with simple regex `<!--\s*{field}:\s*(.+?)\s*-->`, (c) survives markdown-to-anything transformation. Example:

```markdown
### A-01 (Acoustic Buffer Zones at Noisy Adjacencies)

<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional: NDV|DEM|NEU -->
<!-- engineering_disciplines: acoustic -->
<!-- functional_tasks: concentration, rest -->

**Applicable Groups:** ...
```

**Checkpoint at Block 3 end:**
- [ ] All Part 4 items have quantified Specifications block
- [ ] All Part 4 items have v2 HTML comment annotations
- [ ] `references/spec-db-part4-reconciliation.md` exists
- [ ] Standards registry contains ≥80% of BPC-referenced standards
- [ ] GRADE ratings applied to Categories A, E, G
- [ ] CI passes
- [ ] Part 4 is now FROZEN for Block 4 editing (only B1 cross-reference additions permitted)

### Block 4: Evidence Quality + Connection Consumption (12–18 sessions)

**Purpose:** Consume all 96 PENDING connections into Part 4; integrate priority SRs; complete BPC hallucination audit.

**Sequence dependency:** Block 4 starts AFTER Block 3 end checkpoint passes. Block 3 stabilizes Part 4; Block 4 enriches it with connection cross-references.

**Session-start loading budget:** ~40K tokens.

**Per-session loading budget:** ~100K tokens
- Session-start: 40K
- Connection topic file: 3K (of 14 topic files — load one per session)
- Part 4 item index: 2K (from Block 3.0)
- Relevant Part 4 items (~4 items × 720 tokens): 3K
- Relevant BPC slugs (2 × 2K): 4K
- Working room: 48K per connection × ~10 connections

**Model routing:**
- B1 connection consumption: Sonnet session performs ISW write-up. Opus session required if new connections are discovered OR if cross-population synthesis is needed. User explicitly selects Opus for those sessions.
- B5 hallucination audit: Sonnet with web search.
- B2 SR integration: Sonnet (synthesis already done in source SRs).
- B3 remaining: Opus for synthesis across evidence; Sonnet for mechanical application.

**B1 Connection Consumption Pipeline (per connection):**
```
1. READ connection from topic file
2. RESOLVE primary_target(s) to Part 4 item codes
3. READ each target Part 4 item (via item-index)
4. READ evidence BPC slug(s) referenced in connection
5. DETERMINE synthesis direction (from connection description)
6. WRITE cross-reference to Part 4 item (under "Cross-reference" field)
7. UPDATE connection status: PENDING → CONSUMED
8. UPDATE connection register entry: session_applied field
9. UPDATE connections/_index.md status column
10. ATOMIC COMMIT: Part 4 + connection topic file + _index.md
11. VALIDATE: validate_cross_refs.py locally
12. CI RUN: structure + cross-ref gates pass
```

**Batch plan:** ~10 connections per session (conservative; max observed 23 possible).

| Session | Focus | Connections |
|---|---|---|
| 4.1–4.2 | bathrooms-and-wet-areas + seating-and-rest topic files | ~12 |
| 4.3–4.4 | entrances-and-circulation topic file | ~15 |
| 4.5 | sensory-environment | ~12 |
| 4.6 | wayfinding-and-signage | ~10 |
| 4.7 | kitchens-and-workspaces + controls-and-hardware | ~8 |
| 4.8 | communication-and-alerts + cross-cutting | ~10 |
| 4.9 | health-and-symptom-management + population-general | ~10 |
| 4.10–4.11 | frameworks-and-methodology + economics + room-types | ~15 |
| 4.12 | Remaining + B5 hallucination audit | Buffer |
| 4.13–4.15 | B2 (3 SRs) + B3 remaining + B4 density statements | — |

**Error handling:**
- Connection cannot be consumed (target Part 4 item missing) → flag in gap register, skip
- Connection proposes new specification (CON confidence HIGH, target NONE) → raise gap for ISW follow-up in a later session, don't consume in B1
- CI fails → fix inline before moving to next connection
- Opus synthesis required but session is Sonnet → flag for Opus session, skip connection

**Per-session checkpoint:**
- [ ] All connections in session's batch consumed OR flagged with reason
- [ ] Connection register status updated
- [ ] _index.md status counts updated
- [ ] CI green
- [ ] Session log records: connections consumed, gaps raised, Opus-flagged items

### Block 5: Final Readiness Audit (1–2 sessions)

**Purpose:** Verify every transition criterion passes. Produce Phase B handoff artifact.

**Session-start loading budget:** ~40K tokens.

| Task | Description | Output |
|---|---|---|
| 5.1 | Re-run parser source readiness report. Confirm every source in §3 is parser-ready. Update edge cases and known patterns based on what was discovered during Blocks 2–4. | Updated `parser-source-readiness.md` |
| 5.2 | Run validate_bpc.py on every BPC file. Run validate_cross_refs.py on full repo. Run check_thresholds.py on all governed files. Fix any failures. | Clean validator runs |
| 5.3 | Write Phase B handoff document `references/phase-b-handoff.md`: canonical source list per parser; known edge cases; gap register snapshot; spec DB reconciliation summary; standards registry state; connection register state; commit OID at handoff. | `phase-b-handoff.md` |
| 5.4 | Freeze guidebook repo for Phase B reads. Tag commit: `phase-a-complete-YYYYMMDD`. Parsers will read from this tag throughout Phase B. | Git tag |
| C3 | Fix any format issues found during Block 1 audit that weren't resolved in content work. | Source file cleanup commits |

**Checkpoint at Block 5 end:**
- [ ] All transition criteria (§6) pass programmatically
- [ ] CI green on frozen commit
- [ ] Phase B handoff document exists
- [ ] Tag created

---

## 6. Transition Criteria (programmatic)

Claude Code begins (build guide S1) when ALL pass via automated check:

```bash
# Run from guidebook repo
python3 scripts/validate_bpc.py --all                    # 0: all BPC files valid
python3 scripts/validate_cross_refs.py                   # 0: no broken references
python3 scripts/check_thresholds.py                      # 0: all files within thresholds
python3 scripts/check_phase_a_complete.py                # new — see below
```

`scripts/check_phase_a_complete.py` checks:

| # | Criterion | Check |
|---|---|---|
| 1 | A1 complete | ≥95% of BPC files have CO-0006 Key sources table (by schema validation) |
| 2 | A2 complete | `references/spec-db-part4-reconciliation.md` exists and is non-empty |
| 3 | A3 complete | `gap_register.md` and `gap_register_archive.md` both exist |
| 4 | A4 complete | All Part 4 item specs have parseable Specifications block; no duplicate item codes; item count matches Block 1 audit |
| 5 | A5 complete | Standards registry count ≥ 80 |
| 6 | A6 complete | `parser-source-readiness.md` contains Brief Builder validation matrix section |
| 7 | A7 complete | Every Part 4 item spec has `design_stage_lock`, `ve_risk`, `ot_appointment_trigger` HTML comments |
| 8 | B1 complete | Connections/_index.md shows CONSUMED count ≥ 184 (all 96 PENDING converted; 88 existing CONSUMED + 96 newly consumed) |
| 9 | B2 complete | Priority SRs (Rashid, Quesada-Cubo, Simpson) referenced in ≥1 BPC each |
| 10 | B3 complete | Categories A, E, G items have `evidence_tier` field populated |
| 11 | B5 complete | `references/hallucination-audit-*.md` shows all 60 files marked scanned |
| 12 | Parser source readiness | `parser-source-readiness.md` has `audit_status: PASS` or `PASS-WITH-NOTES` for all sections |
| 13 | No P1 OPEN gaps | `gap_register.md` contains zero `P1 | OPEN` lines |

**Partial satisfaction handling:** Any criterion failing = no Phase B start. No waiver mechanism. If a criterion is impractical, the workplan is revised (new version) rather than bypassed.

All Phase A work — Category A, B, and C — must complete before Phase B begins.

---

## 7. Error Management

### Session-local errors
Fix within session. Log in session close YAML. No gap register entry needed unless recurring.

### Cross-session errors
Raise gap register entry (P1 if blocks next block, P2 otherwise). Session-consolidator propagates blocker through sessions until closed.

### Architectural errors
If a block-end checkpoint fails in ways the gap register cannot resolve (e.g., A7 annotation format proves unparseable): stop, revise workplan (new version), resume. Do not execute further blocks.

### Rollback protocol

**Session-level rollback:** Use `git revert <commit_oid>` on the failing commit. Session-consolidator records the revert in session close YAML with rationale.

**Block-level rollback:** If an entire block introduces systemic error (detected at block checkpoint):
1. Tag current state: `block-N-broken-YYYYMMDD`
2. Identify last good commit before block started
3. Create branch `block-N-rollback` from last good commit
4. Cherry-pick any work that should survive
5. Merge rollback branch to main via PR (CI must pass)
6. Session-consolidator documents the rollback + lessons learned rule

**Never:** delete commits, force-push, modify already-shared history.

### Hallucination prevention
Block 4 B5 audit is historical. To prevent new hallucinations during Block 2 A1 migration:
- Every REF-ID entry must cite a source that appeared in the original BPC's flat Key sources list. No new sources invented during migration.
- DOIs/URLs must be verifiable — if not in original BPC, mark [GREY] rather than fabricate.
- validate_bpc.py can optionally cross-check REF-ID count against original list length.

---

## 8. Phase B: Claude Code Build

Phase B follows the build guide sequentially. Mapping to v2 website-preparation phases is preserved from v1.0 §6 — unchanged.

**Phase B starts from:** Git tag `phase-a-complete-YYYYMMDD` in guidebook repo. Phase A work is frozen at that tag. Any further research updates to guidebook repo (post-tag) are not reflected in Phase B parsers unless a new tag is issued and parsers re-run.

**Phase B enforcement** (unchanged from v1.0):
- PostgreSQL constraints (CHECK, FK, NOT NULL, ENUM)
- Parser test suites + cross-entity validation
- CI: axe-core + Lighthouse + type checking + unit tests
- Git pre-commit hooks for commit message format + linting
- Database as single source of truth for data

Block 0 validators from Phase A can be reused as reference — they validate the parser sources Phase B reads.

---

## 9. Session Estimates

### Phase A

| Block | Sessions | Model |
|---|---|---|
| Block 0: Enforcement infrastructure | 2–3 | Sonnet |
| Block 1: Cleanup + format audit | 2–3 | Sonnet |
| Block 2: Citation migration | 6–8 | Sonnet |
| Block 3: Specification completeness | 5–8 | Sonnet + Opus (B3) |
| Block 4: Evidence + connections | 12–18 | Sonnet + Opus (B1 synthesis subset) |
| Block 5: Final readiness audit | 1–2 | Sonnet |
| **Phase A total** | **28–42** | |

### Phase B

| Phase | Sessions |
|---|---|
| Setup + scaffold (build guide S1–S5) | 2–3 |
| Database + parsers (Phase 1) | 8–15 |
| Frontend MVP (Phase 2 + v2 additions) | 15–25 |
| Decision engine + viz (Phase 3 + v2 tools) | 10–15 |
| Community (Phase 4) | 8–12 |
| **Phase B total** | **43–70** |

**Combined total: 71–112 sessions.**

---

## 10. Open Decisions

Questions affecting Phase A scope are flagged. Questions affecting only Phase B can be resolved later.

| # | Question | Phase | When needed |
|---|---|---|---|
| 1 | Domain name | B | Before Phase B (Vercel custom domain) |
| 2 | V9 vs V10 content at launch | **A** | **Before Block 2** (determines which Part files parsers read; affects Block 1 audit scope) |
| 3 | Supplementary populations (CHD/LPA/EXH/BAR) in MVP | **A** | **Before Block 2** (determines whether supplementary BPC files need A1 migration) |
| 4 | Dimensioned drawings | B | Before Phase B Phase 2 |
| 5 | Multilingual UI | B | Before Phase B Phase 2 (i18n architecture) |
| 6 | AI integration (Claude API assistant) | B | Before Phase B Phase 7 |
| 7 | Website replaces or supplements document | B | Before Phase B launch |
| 8 | Budget / hosting | B | Before Phase B S1 |
| 9 | Community features MVP or post-launch | B | Before Phase B Phase 8 |

**Blocking for Phase A: Q2 and Q3.** These must be resolved before Block 2 starts. Defaults:
- Q2 default: V10 content only (per current Part 10 numbering scheme)
- Q3 default: Defer supplementary populations (focus MVP on 11 main populations)

---

## 11. Data Artifacts Produced in Phase A

All artifacts produced in Phase A that Phase B parsers will read:

| Artifact | Path | Produced in | Consumed by |
|---|---|---|---|
| Migrated BPC files (70) | `references/bpc/{topic}/{slug}.md` | Block 2 | p11, p25, p09 |
| Completed Part 4 | `parts/v10/part04.md` | Block 3 | p09, p18 |
| Part 4 item index | `references/part04-item-index.md` | Block 3.0 | Phase B convenience |
| Spec DB reconciliation | `references/spec-db-part4-reconciliation.md` | Block 3 | Phase B Session D (build guide §1.5) |
| Expanded standards registry | `references/standards-registry.md` | Block 3 | p01, p_standards_ext |
| Gap register split | `gap_register.md` + `gap_register_archive.md` | Block 1 | p03 |
| Session archive | `sessions/_archive/` | Block 1 | Phase B reference |
| Parser source readiness report | `references/parser-source-readiness.md` | Blocks 1, 5 | Phase B parser tuning |
| Phase B handoff document | `references/phase-b-handoff.md` | Block 5 | Phase B Session 1 |
| Block 0 validators | `scripts/validate_*.py`, `scripts/check_*.py` | Block 0 | Phase B reuse (optional) |
| CI workflow | `.github/workflows/ci.yml` | Block 0 | Ongoing (guidebook repo) |
| Consumed connection register | `references/connections/_index.md` + per-topic | Block 4 | p05 |
| Enriched BPC files (SR integration) | `references/bpc/{topic}/{slug}.md` | Block 4 | All BPC-reading parsers |

---

## 12. Cancelled Work (prior scope superseded by this workplan)

| Item | Superseded by |
|---|---|
| v1 website-preparation.md Phases 0.3/0.5/0.6 (JSON extraction) | Phase B parsers read markdown directly |
| v1 website-preparation.md Phase 1 (spec DB batches 2–5 to JSON) | Phase B parsers |
| Ecosystem workplan two-repo data promotion pipeline | Single-repo clone during Phase B |
| Ecosystem workplan hooks.py for website repo | PostgreSQL + CI replace it |
| Prior v1.0 sequencing (Block 5 last) | Block 0 first (enforcement before content) |
