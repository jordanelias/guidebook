# Stage 2.0 — Directness-Primitive Pipeline Trace
**Date:** 2026-06-09 · **Session:** proceed-2026-06-09 · **Gate:** D-D · **Closes:** `[GAP: schemas/evidence_state.py not line-read]`, `[GAP: directness primitives not traced]`
**Status:** EXECUTED (reads-only; no DB mutation). Hard prerequisite to Stage 2.2 (consolidate) and 2.3 (build cell-state directness-aware).
**Verified against:** committed `data/guidebook.db` @ HEAD 928c438, line-reads of `schemas/evidence_state.py` + `scripts/resolve_dois.py`, repo-wide grep of the five named primitives.

---

## 1. Verdict
The five directness primitives the workplan names are **real but scattered across five tables written by three distinct workflows, with no unifying model**. One named writer (`resolve_dois.py`) writes **none** of them. The new `scale_directness` dimension does **not exist** anywhere. The Pydantic cell-state models exist but are **not directness-aware**. 2.2 is a genuine consolidation-and-extension job, not a relabel; 2.3 must **revise** `evidence_state.py`, not author it greenfield.

## 2. Primitive map (where each lives, who writes it, live population)
| Primitive | Table.column | Type | Defined in | Written by | Read by | Live rows |
|---|---|---|---|---|---|---|
| `match_grade` | `evidence_population_match.match_grade` | EXACT/PARTIAL/PROXY/MISMATCH | mig 012 baseline | citation-miner / verification **data migrations** | `audit/research_protocol_audit.py` (rule #7) | 27/27 populated |
| `value_match` | `reasoning_doc_citations.value_match` | EXACT/WITHIN-TOLERANCE/PAYWALL/CONTRADICTED/NOT-FOUND | mig 011 → re-baselined 012 | reasoning-doc / pass-3 **data migrations** (rule #10 sub-2/3) | `audit/reasoning_doc_citations_audit.py` | 3/7 populated |
| `passes_strict` | `spec_value_probes.passes_strict` | 0/1 | mig 012 baseline | **PMP walk** (rule #8) | `audit/pmp_audit.py` | 6/21 = strict-pass |
| `relevance_note` | `source_slug_links.relevance_note` | free-text | mig **019** | (nothing) | (nothing) | **0/689 — dormant** |
| `applicability` | `room_item_population.applicability` | applies/… | `scripts/db/init_db.py`, mig 012 | `scripts/db/migrate_all.py`, `enrich_all_c_stage.py`, `seed_b41_pilot.py` | `scripts/generate/room_page.py` | **table ABSENT from canonical DB** |
| `scale_directness` | — | — | — | — | — | **does not exist (new in 2.2)** |
| *(value substrate)* | `source_value_extractions` (whole table) | mig **018** (DR-2026-05-28-b) | (nothing yet) | — | **0 rows — present, unpopulated (R10-c)** |

## 3. Pipeline ownership (the three workflows + the misattributed one)
- **PMP walk** (rule #8, `skills/progressive-measurement`, `scripts/probes/`) → writes `spec_value_probes` (`passes_strict`, step/phase, search queries) + `evidence_sources`/`source_slug_links`/`evidence_population_match` per cited study. This is **value-directness + strict-termination**.
- **citation-miner** (Phase B.11) → writes `evidence_population_match.match_grade` + `mismatch_note` (**population-directness**) and `source_slug_links` rows. The live free-text relevance lives in `mismatch_note`, **not** in `relevance_note`.
- **reasoning-doc-citations** (rule #10 sub-2/3, `skills/reasoning-doc-citations`) → writes `reasoning_doc_citations.value_match`/`claim_match` (**claim/value-directness against a re-read section**).
- **`resolve_dois.py` — NOT a directness writer.** It is the DOI/source-existence pipeline: writes `evidence_sources` (doi, pmcid, verification fields), `evidence_source_authors`, `pipeline_runs`. It sits **upstream** of directness (it establishes the rule #10 *existence* gate). **§2.0's framing of it as a primitive-writer is incorrect** — corrected here so 2.2 does not go looking for directness writes it will never find.

## 4. `schemas/evidence_state.py` — line-read result (172 lines)
Three Pydantic models, all population-anchored, **none directness-aware**:
- `ProvisionalConfidenceFlag` — dimensions_present/absent + synthesis_basis.
- `ConvergenceAssessment` — status (ConvergenceStatus) + clinical/co1/co2 REF-ID lists + rationale/synthesis_approach, with status-keyed validators.
- `EvidenceStateRecord` — spec_id (SPEC-NNNN) × population × state (4-state enum) + state-keyed required-field validators.

No `scope`, `scale`, `directness`, `match_grade`, or grain field exists. Backing tables `evidence_cell_state` and `convergence_assessment` are **absent from the DB** (R2 confirmed). So:
- **2.3 revises these models** to carry the scale × directness conditioning (design principle #2: bidirectional grain-matching), then creates the two tables to match.
- The models reference `governance/evidence-methodology.md §2/§2.3/§3.2` — which **Stage 1.1 is rewriting** (scale-conditioned weighting, directness layer). The docstrings are therefore part of the re-attestation surface when 1.1 lands.

## 5. Consequences for the Stage-2 build (carry into 2.2/2.3)
1. **2.2 consolidation target is six sources, not the five named:** `match_grade`, `value_match`, `passes_strict`, the live free-text in `mismatch_note`/`spec_value_probes.notes`/`reasoning_doc_citations.notes`, plus the empty `source_value_extractions` substrate. Unify into one rule-based directness model; add `scale_directness` as the genuinely new axis.
2. **`relevance_note` (mig 019) is dormant (0/689).** Decide: populate structurally, or retire with a caller-sweep (architecture `<migration_and_growth>`). It is **not** the de-facto relevance store; `mismatch_note` is.
3. **`applicability` / `room_item_population` is a legacy `scripts/db/` artifact** absent from the canonical migration-built DB. Confirm whether the `scripts/db/` build path is superseded by `scripts/migrate_db.py` before treating `applicability` as a live primitive — otherwise 2.2 consolidates a ghost.
4. **`source_value_extractions` is the intended value-directness home (DR-2026-05-28-b).** 2.2 should route value-directness through it; populating it is Stage 2.2/3.3 work, not new schema work.
5. **2.3 is revise-then-build:** amend `evidence_state.py` for directness, then create `evidence_cell_state` + `convergence_assessment` tables matching the revised models, wired to migration-021 population junctions (not scalar population cols).

## 6. Open / deferred
- `[GAP: scripts/db/ vs scripts/migrate_db.py provenance — not fully reconciled]` — needed before 2.2 treats `applicability` as live. Bounded; do at head of 2.2.
- `[CONFIDENCE: high — every claim grounded in a line-read or a live-DB query at HEAD 928c438. The one inference (citation-miner as the mismatch_note writer) rests on the data-migration INSERT targets, which are explicit.]`
- `[NULL: scale_directness — repo-wide grep across *.py and *.sql returned zero; the dimension is genuinely new, not hidden under an alias I searched (scope/applicability/match_grade all checked).]`
