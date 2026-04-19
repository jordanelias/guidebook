# Phase B Handoff Document
<!-- Block 5 Task 5.3 — 2026-04-19 -->

## Overview

This document is the handoff artifact from Phase A (Website Preparation) to Phase B (Claude Code Build).
All Phase A workplan criteria are met. The guidebook repo is ready for Phase B parser reads.

**Handoff date:** 2026-04-19
**Phase A commit tag:** phase-a-complete-20260419 (see Task 5.4)
**Conducted by:** Sonnet 4.6 (Blocks 2–5) with Opus 4.6 synthesis passes

---

## 1. Canonical Source List Per Parser

| Parser | Primary source file(s) | Format | Notes |
|---|---|---|---|
| p01_populations_references | `parts/v10/part01.md`, `references/standards-registry.md` | H2/H3 prose + YAML blocks | Standards registry: 80 entries, 26 jurisdictions |
| p02_populations | `parts/v10/part02.md` | H3 per population code | 11 populations; §2.N CODE heading format |
| p03_synthesis | `parts/v10/part03.md` | H2/H3 prose; conflict tables | co-occurrence framework; 9 resolved conflicts |
| p04_item_specs | `parts/v10/part04.md` | ### X-NN heading per item; HTML annotation comments | 91 active items; E-10 canonical at L3205 |
| p04_item_index | `references/part04-item-index.md` | Markdown table: Code\|Title\|Start\|End\|Lines | Use to slice Part 4 without loading full file |
| p_bpc_sources | `references/bpc/**/*.md` | CO-0006 REF-ID table in ## Key sources | 78 files; 3 MERGED stubs; 3 DEFERRED stubs |
| p_spec_db | `references/spec-db-part4-reconciliation.md` | Markdown sections A–F | Item→BPC mapping; field discrepancies |
| p_standards | `references/standards-registry.md` | YAML fenced blocks | 80 entries; skip template block (first entry) |
| p_connections | `references/connections/_index.md` | Markdown table | CONSUMED=140, DEFERRED=42, PENDING=0 |
| p_slug_registry | `references/slug-registry.md` | Markdown table | 70+ slugs; BPC/SL paths; MERGED slugs noted |
| p_grade | `parts/v10/part04.md` | HTML comments: grade_confidence | 90/90 items rated; filter by <!-- grade_confidence: --> |
| p_annotations | `parts/v10/part04.md` | HTML comments: design_stage_lock, ve_risk, ot_appointment_trigger | 91/91 annotated |
| p_evidence_density | `parts/v10/part*.md` opening | HTML comment + blockquote | 12/12 Parts; <!-- evidence_density: --> |
| p_gap_register | `gap_register.md` | Pipe-table with status column | 1 P1 OPEN (GAP-079 GRADE — partially resolved); filter OPEN only |

---

## 2. Known Edge Cases

| File | Edge case | Parser action |
|---|---|---|
| `part04.md` | E-10 appears at L1737 (redirect) and L3205 (canonical) | Use L3205; skip L1737 redirect block |
| `part04.md` | A-17, B-04, C-06, F-05 headings exist but are ABSORBED/MERGED | Exclude from active item count; flag as deprecated |
| `part04.md` | F-06 is a new item written at Block 3 A4 — full spec present | Include normally |
| `references/bpc/` | 3 MERGED redirect stubs: chronic-pain, fatigue-spectrum, hearing-impairment | Skip or redirect to canonical slug |
| `references/bpc/` | 3 DEFERRED stubs: bathroom-typology-global-south, fold-down-grab-bar, bariatric-turning-radius | Flag as STUB; content pending |
| `references/bpc/` | ~45 [GREY — DOI required] flags in Key sources tables | Flag for pre-publication; do not reject |
| `standards-registry.md` | First YAML block is template (jurisdiction: "[2-letter code...]") | Skip template; parse from second block |
| `connections/_index.md` | Status summary table rows (| CONSUMED | 140 |) | Distinguish from data rows (| CON-XXXX |) |
| `gap_register.md` | CLOSED-CONSUMED entries dominate; OPEN P1 = 1 (GAP-079 GRADE) | Filter by OPEN + P1 for session-start load |
| `pain-ofs-built-environment-design.md` | Had duplicate ### Key sources (now fixed) | Single ## Key sources table is canonical |

---

## 3. Gap Register Snapshot

**Date:** 2026-04-19

| Category | Count |
|---|---|
| P1 OPEN | 1 (GAP-079 — GRADE ratings; partially resolved in B3) |
| P1 CLOSED-CONSUMED | 3 (GAP-078 SRs, GAP-079 GRADE partially, GAP-080 density) |
| P2 OPEN | ~5 (A-02 STI criterion, G-03 grab bar spec, and others) |
| P3 OPEN | ~8 (bibliography, standards gaps, global south slugs) |

**GAP-079 partial resolution:** GRADE ratings applied to 90/90 Part 4 items (B3 complete). Original GAP-079 scope was broader (125 items including all Part 7/8 matrices not yet written) — remaining scope deferred to Phase B content writing sessions.

---

## 4. Spec DB Reconciliation Summary

- **File:** `references/spec-db-part4-reconciliation.md`
- **Coverage:** 91/91 Part 4 items have ≥1 BPC mapping (100%)
- **Open discrepancies:** 4 (A-09 vibration threshold, A-02 NRC vs STI, G-03 grab bar type, B-01 → resolved)
- **P1 fixes applied:** A-09 UNVERIFIED flag, B-01 melanopic EDI update, D-03 47% flag
- **Deferred non-standard BPC files:** 3 (bathroom-typology-global-south, fold-down-grab-bar, bariatric-turning-radius)

---

## 5. Standards Registry State

- **File:** `references/standards-registry.md`
- **Entries:** 80 (A5 target ≥80 — PASS)
- **Jurisdictions:** 26 (AU, BR, CA, CH, CN, DE, DK, ES, EU, FI, FR, IE, INT, ISO, IT, JP, KR, NL, NO, NZ, PT, SE, SG, UK, UN, US)
- **Template block:** First entry is a schema template — parsers must skip

---

## 6. Connection Register State

- **File:** `references/connections/_index.md`
- **CONSUMED:** 140 (direct application — Part 4 and prior sessions)
- **CONSUMED-DEFERRED:** 42 (target Parts 1, 5, 6, 7, 9, 10, 11, 12 — not yet written)
- **PENDING:** 0 (all cleared in Block 4 B1)
- **Next CON-ID:** CON-0181

---

## 7. Commit OID at Handoff

**Handoff commit (Phase A complete):** See Git tag `phase-a-complete-20260419`

Key commits in Phase A:
- Block 2 complete (BPC CO-0006 migration): Sessions 2.1–2.7
- Block 3 complete (Part 4 enrichment): `c697152e6d35` (A7), `a77b576049ac` (A2), `572b9d67b471` (A5)
- Block 4 complete (connections + SRs + density): `28b11fb9ec77` (B1), `5c53550f008f` (B2), `f442b48be021`–`24b5e05e3709` (B4)
- Block 5 complete (CI validation): `bde086644cc7` (validator), `418a3a283920` (ci.yml), `3a9272b9de9d` (final BPC fix)

---

## 8. Validator Status at Handoff

| Validator | Command | Result |
|---|---|---|
| BPC schema | `python3 scripts/validate_bpc.py --all` | 78/78 PASS |
| Cross-references | `python3 scripts/validate_cross_refs.py` | PASS (warn-only removed) |
| Thresholds | `python3 scripts/check_thresholds.py --report` | 5/5 PASS |
| Phase A complete | `python3 scripts/check_phase_a_complete.py` | See script (created Block 5) |

---

## 9. Phase B Session 1 Loading Protocol

At Phase B Session 1 start:
1. Checkout tag `phase-a-complete-20260419`
2. Load `references/phase-b-handoff.md` (this document)
3. Load `references/parser-source-readiness.md` §Final audit_status summary
4. Load `references/part04-item-index.md` for item code→line range lookups
5. Do NOT load `parts/v10/part04.md` in full — use item index to slice

---

*Generated by Sonnet 4.6, Block 5 Task 5.3, 2026-04-19.*

---

## 10. Phase B Standing Decisions (logged 2026-04-19)

| # | Question | Decision |
|---|---|---|
| 1 | 3 deferred non-standard BPC files | **Defer all 3 to Phase B** — stubs remain; full content deferred |
| 2 | GAP-079 (GRADE ratings) | **Keep OPEN** — B3 complete for Part 4; Part 7/8 matrix work in Phase B |
| 3 | A-09 vibration threshold 0.1 m/s RMS | **Keep UNVERIFIED flag** — likely BS 6472-1:2008 (building vibration, velocity-based) not ISO 2631-1 (acceleration-based); source unconfirmed |
| 4 | GREY DOI flags (~45) | **Resolve before publication** — DOI resolution session to be scheduled |
| 5 | Multilingual UI | **EN + one other language at launch** (language TBD before Phase B Phase 2) |
| 6 | Website vs document | **Replace the document eventually** — website is long-term canonical form; document maintained during transition |

### Decision notes

**Decision 3 (A-09):** ISO 2631-1 uses frequency-weighted acceleration (m/s²) over 8h exposure, not RMS velocity (m/s). The 0.1 m/s RMS value is characteristic of building vibration standards (BS 6472-1:2008; DIN 4150-2) which do use velocity-based thresholds for human exposure in buildings. PubMed search found no wheelchair-disability-specific source. UNVERIFIED flag correctly placed. Pre-publication action: confirm source is BS 6472-1:2008 or equivalent; if so, cite correctly and remove UNVERIFIED flag.

**Decision 4 (GREY DOI flags):** ~45 entries across BPC Key sources tables carry [GREY — DOI required]. Priority order for resolution session:
1. Tier 1 citations without DOI (OTI-02 Wellecke 2022, OTI-03 Russell 2018, POD-03/04)
2. Mental health BPC remaining 10 GREY flags (MHB-02, 04, 05, 09, 10, 16, 18, 11)
3. Thermal comfort BPC (TCO-01 through TCO-04)
4. MS-thermal BPC (MST-02 through MST-06)

**Decision 5 (multilingual):** Second language not yet selected. Candidates: DE (strongest non-EN evidence base in BPC corpus), FR (CEREMA, PCH, APF), NL (NEN 9120:2025, ME/cvs Stichting). Decide before Phase B Phase 2 (i18n architecture).

**Decision 6 (replace vs supplement):** Document (.docx/.pdf) maintained during Phase B build. Website becomes canonical at launch. Post-launch: document updated by derivation from website content, not independently authored. This affects Phase B content pipeline design.
