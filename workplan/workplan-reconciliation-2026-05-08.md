# Workplan Reconciliation — All COs, Workplans, and Governance Documents
**Generated:** 2026-05-08 04:15 UTC
**Session:** governance session (D-block fixes + block gate + reconciliation)
**Model:** [cannot self-verify per model_identity policy]
**Read:** CO-0001 through CO-0009, workplan-co0007 v3+amendments+v4, website-preparation.md v2.0, workplan-item-audit-pipeline-co0009, pi-update-co0008, opus-synthesis-queue, opus-missing-passes, roadmap-2026-04-27, governance/workplan-adoption.md, evidence_source.py, bpc_metadata.py, convert_sources.py, ci.yml, check_phase_a_complete.py, db.py

---

## 1. Change Order sequence (canonical governance decisions)

| CO | Date | Title | Status | Scope |
|---|---|---|---|---|
| CO-0001 | 2026-03-18 | Structural rename/renumber | EXECUTED | Volumes I/II/III, Parts 1–13, §x.y.z numbering |
| CO-0002 | 2026-03-25 | IntD elimination | EXECUTED | IntD becomes DEM/NDV proxy — no standalone code |
| CO-0003 | 2026-03-28 | Co-occurring disability reframe | EXECUTED (terminology); §8 SUPERSEDED by CO-0004 | "Cross-population" → "co-occurring" terminology |
| CO-0004 | 2026-03-29 | Volume merge + Part restructuring | EXECUTED | Vol I+II merge, Part 3+4 merge, new Part 5, 13→12 Parts |
| CO-0005 | 2026-04-05 | Evidence expansion programme | APPROVED, Phase 0 in progress | 24→46 jurisdictions, research programme |
| CO-0006 | 2026-04-08 | Ecosystem infrastructure | PARTIALLY EXECUTED | BPC REF-ID tables, connection register restructuring |
| CO-0007 | (implicit) | Master workplan | ADOPTED (v4, 2026-05-03) | Not a formal CO — the workplan itself (v1→v2→v3→v4) |
| CO-0008 | 2026-04-26 | Infrastructure overhaul | EXECUTED (8/8 deliverables) | Pydantic schemas, data/ YAML layer, Python-backed skills, CI |
| CO-0009 | 2026-05-04 | Threshold rule removal | SIGNED OFF | SQLite migration cleanup — removes obsolete check_thresholds.py rules |

### Notes on CO gaps
- No formal CO-0007 change order document exists. "CO-0007" refers to the workplan itself.
- CO-0008 scope doc is labeled DRAFT but has been fully executed (all 8 deliverables shipped).
- CO-0009 has TWO documents: `references/change-orders/CO-0009-2026-05-04-threshold-removal.md` (the formal CO) and `workplan/workplan-item-audit-pipeline-co0009.md` (an extension workplan, PROPOSED but not yet adopted).

---

## 2. Document supersession map

```
workplan-co0007-v3.md
  + workplan-co0007-v3-amendments.md (7 amendments)
  ↓ SUPERSEDED by
workplan-co0007-v4.md ← CANONICAL OPERATIVE PLAN (ADOPTED 2026-05-03)

website-preparation.md v2.0 (2026-04-17)
  ↓ PARTIALLY SUPERSEDED by workplan v4
  │  Phase A Blocks 0-5: tactical breakdown, now covered by v4 C-stages
  │  Phase B tech stack: deferred decision per v4 ("not a B2 decision")
  │  Block 2 citation work: STILL VALID as input to v4 C1
  │  26 parsers: TO BE RECONCILED per v4 C1 ("Map parsers to pipeline roles")
  │  §6 transition criteria: PARTIALLY REPLACED by v4 Stage C done criteria

roadmap-2026-04-27.md
  ↓ SUPERSEDED by workplan v4
  │  Roadmap showed A4-A13 as pending; v4 says all of Stage A is COMPLETE
  │  Roadmap structured A→B→C linearly; v4 restructured with resequencing

opus-synthesis-queue.md (2026-03-29)
  → OPERATIONAL but stale: 13 slugs listed as "ready for Opus synthesis"
  → Status unclear — some may have been synthesized in April/May sessions

opus-missing-passes.md (2026-04-03)
  → OPERATIONAL: OP-A COMPLETE; OP-B, OP-C, OP-D PENDING
  → OP-B (CON connections), OP-C (Part 10 DAR), OP-D (Part 11 Economics) need Opus

workplan-item-audit-pipeline-co0009.md (2026-05-05)
  → PROPOSED (not adopted). Extends v4 C1/C2/C3 with per-item audit pipeline.
  → Requires A12 decision records before implementation.

pi-update-co0008.md (2026-04-26)
  → READY TO APPLY (to claude.ai Project Instructions).
  → Status unclear: PI v10.4 (this session) does not include all these changes.
```

---

## 3. The critical supersession finding

**website-preparation.md and workplan v4 describe the same work in incompatible organizational structures:**

| website-preparation.md | workplan v4 | Alignment |
|---|---|---|
| Phase A Block 0: Enforcement infra | Stage 0 + CO-0008 infra pour | Same work, COMPLETE in both |
| Phase A Block 1: Cleanup + format audit | B2.2 format audit | Same work, COMPLETE in both |
| Phase A Block 2: Citation migration (6-8 sessions) | C1 Phase 3-4 + C7 | Same work, different scope/naming |
| Phase A Block 3: Specification completeness (5-8 sessions) | C3 (25-35 sessions, much larger scope) | Overlapping — C3 contains Block 3 plus more |
| Phase A Block 4: Connection consumption (12-18 sessions) | C3 ("36 CON-HIGH entries") + C7 | Subsumed into C3/C7 |
| Phase A Block 5: Final readiness audit | C10 (5-8 sessions) | Same concept, different location |
| Phase B: Claude Code build (26 parsers) | v4 does not commit to this architecture | DEFERRED / MAY BE SUPERSEDED |

**website-preparation.md is sequentially strict:** Block N must complete before Block N+1 starts.
**workplan v4 is page-type-organized:** C1-C11 can run in parallel to some extent; sequencing is by entity type, not by processing stage.

**Resolution:** workplan v4 is the canonical plan (later date, ADOPTED, broader scope). website-preparation.md provides useful tactical detail (per-file migration checklists, parser readiness audit template) that v4 references but does not reproduce. Treat website-preparation.md as a reference for HOW to do citation migration (Block 2's per-file pipeline), not for WHAT to do or WHEN.

---

## 4. Actual current state (per v4, verified against repository)

### What's complete
- Stage 0: 9 sessions, all 31 audit findings resolved
- Stage A: 24 sessions, 13 governance documents committed (A1-A13)
- B1: 9 sessions, Pydantic schemas designed and debated (4 candidates scored)
- B2-B4.1 + C0: 1 session (2026-05-04) — schemas implemented, 978 rows migrated, E-08 pipeline pilot rendered

### What's active (Stage C)
Per v4, **C1-C11 are all ACTIVE**. In practice, recent sessions have been doing:
- Citation verification (C7 territory)
- Connection synthesis/consumption (C3 territory)
- Source verification backlog (C7 + CO-0006 territory)
- Economics audit and research (C9 territory — 87KB workplan produced)

### What's deferred
- B4.2-B4.3 (additional pipeline pilots): until content is migrated
- B5-B7 (rendering, validation, arch lock): until content is migrated
- workplan-item-audit-pipeline-co0009: PROPOSED, requires decision records (A12) before adoption

### Operational queues
- **Opus synthesis queue:** 13 BPC slugs ready for synthesis (from March 2026; status may be stale)
- **Opus missing passes:** OP-B (10 CON connections), OP-C (Part 10 DAR), OP-D (Part 11 Economics) — all PENDING, all require Opus model
- **6 PENDING connections in SQLite:** need Opus synthesis before consumption
- **44 CONSUMED-DEFERRED connections:** flagged for application (v4 C3 territory)
- **CO-0006 BPC migration:** partially complete; validate_bpc.py passes on some files, not all

---

## 5. What needs doing — per canonical plan (v4), with CO-0006 commensurateness resolved

### Immediate (unblocks everything else)

1. **Adopt or reject workplan-item-audit-pipeline-co0009.** It's PROPOSED status. If adopted, it restructures C1/C2/C3 with a per-item audit pipeline. If rejected, C3 proceeds per v4's original scope. Decision needed before C3 work begins at scale.

2. **Apply pi-update-co0008 changes to PI v10.4.** The CO-0008 PI update was "READY TO APPLY" since April 26 but PI v10.4 (produced this session) doesn't include Standing Rules 11-14 or the model-identity change (Opus as primary). Either apply these to PI v10.5, or explicitly defer.

3. **Verify opus-synthesis-queue currency.** 13 slugs listed as "ready" in March — some may have been synthesized since. Run a check against BPC files for `opus_synthesis: true` to determine actual remaining count.

### C1 — Migration tooling (3-5 sessions per v4)

4. **Map 26 website-preparation.md parsers to v4 pipeline roles.** v4 item 142 explicitly calls this out. Some parsers become migration scripts, some become rendering queries, some are redundant. This mapping determines whether website-preparation.md's Phase B is still the build plan or whether v4's data-layer approach replaces it.

5. **Build convert_bpc_sources.py** (or equivalent). Closes the gap between CO-0006 REF-ID tables and CO-0008's global-reference-registry.json → data/evidence_sources/ YAML pipeline. Without this, Block 2 migration work doesn't flow into the data layer. (See §7 below for the CO-0006/CO-0008 bridge.)

6. **Complete C1 migration phases 3-13.** 531 evidence_source records, 78 BPC metadata records, specification extensions, connection migration, conflict migration, remaining entity types.

### C3 — Specification page content (25-35 sessions per v4)

7. **Resolve the 6 PENDING connections (Opus required).** These block the PENDING=0 gate. Until they're synthesized, the connection corpus isn't consumption-ready.

8. **Opus missing passes OP-B, OP-C, OP-D.** 10 CON connections + Part 10 DAR + Part 11 Economics need Opus adjudication before downstream C3 content work.

9. **CO-0006 BPC migration completion.** Migrate remaining BPC files to REF-ID table format. This is both CO-0006 completion AND C1/C7 input. Use website-preparation.md Block 2's per-file pipeline (the tactical detail is still valid even though the strategic plan is v4).

### Ongoing / parallel

10. **C7 evidence base:** Citation tagging (918 pending per GAP-CITE-01), source verification, hallucination audit.
11. **C9 cross-cutting prose (Opus):** Parts 1, 11, 12 framework content — the connection application work I was wrong to draft today. This is v4 C9, requires Opus, and depends on C3 being substantially complete.
12. **Economics audit research:** 87KB workplan produced 2026-05-03. This is C9 economics sub-work.

---

## 6. What is superseded (safe to archive)

| Document | Status | Archive? |
|---|---|---|
| workplan-co0007-v3.md | SUPERSEDED by v4 | Archive to workplan/deprecated/ |
| workplan-co0007-v3-amendments.md | SUPERSEDED by v4 | Archive (v4 absorbed all amendments) |
| workplan-co0007-synthesis.md | Historical (Stage 0 work product) | Archive |
| workplan-co0007-audit.md | Historical (Stage 0 work product) | Archive |
| roadmap-2026-04-27.md | SUPERSEDED by v4 current-position | Archive |
| v10-5_2026-03-29.md | SUPERSEDED by v4 | Archive |
| slug-triage-2026-03-28.md | Historical (pre-Stage-A) | Archive |
| co0003-amendment-2026-03-28.md | Historical (CO-0003 amendment) | Archive |
| co0004-body-propagation.md | Historical (CO-0004 execution plan) | Archive |
| references/project-instructions.md (v9.0) | SUPERSEDED by PI v10.4 | Archive or delete |
| references/connections/_index.md | ARCHIVED (data in SQLite) | Already archived per skills |

| Document | Status | Keep |
|---|---|---|
| workplan-co0007-v4.md | CANONICAL | Keep — operative plan |
| website-preparation.md | PARTIALLY SUPERSEDED but referenced by v4 | Keep — tactical reference for C1 parser mapping |
| workplan-item-audit-pipeline-co0009.md | PROPOSED | Keep — pending adoption decision |
| opus-synthesis-queue.md | OPERATIONAL (may be stale) | Keep — verify currency |
| opus-missing-passes.md | OPERATIONAL | Keep — OP-B/C/D pending |
| economics-audit-research-2026-05-03.md | OPERATIONAL | Keep — active C9 workplan |
| pi-update-co0008.md | READY TO APPLY | Keep — PI changes pending |

---

## 7. CO-0006 / CO-0008 bridge (commensurateness resolution)

CO-0006 and CO-0008 are sequential, not competing:
- CO-0006 defines the **markdown format** (BPC REF-ID tables) that website parsers and conversion scripts read FROM
- CO-0008 defines the **data layer** (Pydantic schemas, YAML entities) that conversion scripts populate INTO
- `bpc_metadata.py` has `co0006_migration: Optional[bool]` — explicit design compatibility

Three field-level gaps to resolve:
1. **Short-key orphaning:** CO-0006 says "retained for backward compatibility." CO-0008 EvidenceSource has no short_key field. Need decision: drop short-key from CO-0006 table spec, or add short_key to EvidenceSource.
2. **Lang field gap:** CO-0006 table has Lang (ISO 639-1). EvidenceSource has no language field. Source language is project-critical (14 research languages). Either extend EvidenceSource with a `language` field or document that language tracking lives exclusively in SQLite search_languages table.
3. **convert_bpc_sources.py does not exist.** CO-0006 table data does not flow into CO-0008's data layer after Block 2 migration. Need to build this bridge script (item 5 above).

Migration strategy: CO-0006 §1 says "do not mass-migrate." Website-preparation.md Block 2 says batch-migrate all 70. v4 doesn't specify. Recommendation: follow website-preparation.md's batch approach (it was written after CO-0006 and is closer to v4's C-stage pacing), but document this as an explicit override of CO-0006's on-first-touch policy.

---

## 8. Block gate correction needed

The block gate committed this session (workplan-orchestrator §4a, commits 18312385 + 58411e3) checks website-preparation.md's Block dependencies. This is the WRONG plan:

| Current gate checks | Should check |
|---|---|
| Block 0 → Block 1 → Block 3 → Block 4 (sequential) | v4 C1/C3/C7/C9 (partially parallel, dependency-graph based) |
| gap_register_archive.md existence (Block 1 gate) | C1 migration tooling readiness (v4 C1 dependencies) |
| PENDING=0 for Block 4 | PENDING=0 is correct but belongs in C3's connection consumption sub-gate, not a Block 4 gate |

The gate is still useful as a DIAGNOSTIC (it surfaces real state), but its enforcement rules (which blocks to lock/unlock) are based on website-preparation.md's Block model, not v4's C-stage model. Correcting this requires rewriting §4a to check v4 C-stage dependencies. This is a next-session task — the gate code itself (API HEAD requests + SQLite query) is reusable; only the dependency graph and workflow→stage mapping table need updating.

---

## 9. Recommended next session

1. Rewrite §4a gate against v4 C-stages (not website-preparation.md Blocks)
2. Adopt or defer workplan-item-audit-pipeline-co0009
3. Apply pi-update-co0008 to PI (produce v10.5)
4. Verify opus-synthesis-queue currency
5. Begin C1 Phase 3 (evidence_source migration) — the highest-priority unblocked work that feeds everything downstream
