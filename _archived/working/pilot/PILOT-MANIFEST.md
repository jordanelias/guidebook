# Pilot manifest — evidence-architecture operational proof
**Created:** 2026-07-12 · **Scope:** working-copy DB only (`working/pilot/guidebook-pilot.db`). The canonical `data/guidebook.db` is never touched by any step recorded here.
**Purpose:** demonstrate, on real cells, the full architecture of `governance/evidence-architecture.md` — determination engine (G1/G2/G3/G6 fixes active under `rule_version="pilot-1"`), scale-tagging, and the audience register layer under invariants I1–I5 — before any of it is applied to canonical state.

## 1. Working-copy setup

```
cp data/guidebook.db working/pilot/guidebook-pilot.db          # user_version 25
# applied to the COPY only (canonical untouched), matching the twice-stopped
# precedent in workplan/website-v0-path-forward-2026-07-12.md:
#   scripts/migrations/026_reconcile_evidence_cell_state.sql
#   scripts/migrations/data_20260712150000_jurisdictional-values-backfill.sql
# verified: evidence_cell_state 0 rows / jurisdictional_values 109 rows /
# all four views execute (v_best_practice, v_pending, v_divergence, v_code_floor_only)
```

Note: migration 026's table already carries a `design_scale` column (universal/population/person) — G1's scale-tagging lands there with no schema change; only `regulatory_stratum_only` needs the follow-on migration proposed in the unification DR (the pilot computes it engine-side and records it in `tier_basis`/confidence fields pending that column).

## 2. Evidence-attribution join (the "one structural dependency to nail")

Evidence reaches a cell as: `evidence_sources` → `source_slug_links (ref_id ↔ slug)` → `bpc_metadata (slug → population)`. Selection profile query:

```sql
SELECT b.slug, b.population,
  SUM(CASE WHEN e.tier=1 AND e.evidence_type='clinical' THEN 1 ELSE 0 END) t1,
  SUM(CASE WHEN e.evidence_type='co1' THEN 1 ELSE 0 END) co1,
  SUM(CASE WHEN e.tier=2 AND e.evidence_type IN ('sr_meta','standard_eb') THEN 1 ELSE 0 END) t2,
  SUM(CASE WHEN e.evidence_type='co2' THEN 1 ELSE 0 END) co2,
  SUM(CASE WHEN e.tier=3 THEN 1 ELSE 0 END) t3,
  SUM(CASE WHEN e.tier IN (4,5) THEN 1 ELSE 0 END) t45,
  SUM(CASE WHEN e.tier=6 THEN 1 ELSE 0 END) t6
FROM source_slug_links l
JOIN evidence_sources e ON e.ref_id=l.ref_id
JOIN bpc_metadata b ON b.slug=l.slug
WHERE e.superseded_by_ref_id IS NULL
GROUP BY b.slug, b.population;
```

**Known dependency, routed around — not silently solved:** `item_bpc_links` (the intended item↔BPC bridge) is populated for **1 of 92 items** (A-18 only). The slug→item mapping below is therefore **manual, pilot-cells-only**, and each mapping is a recorded judgment. Phase-1 backfill at full scale requires populating `item_bpc_links` first (flagged in DR-2026-07-12-evidence-cell-state §Consequences as a forward risk; unchanged here).

**Population-code mapping notes:** `bpc_metadata.population` includes non-FK values (`MULTI`, `IntD`, `ABI`) that are not in `populations` (22 codes). Where a pilot slug carries `MULTI`, the cell's population is assigned manually with justification below. One correction applied: `deaf-spatial-design` carries `population=NDV` in bpc_metadata; its content (DeafSpace / Bauman) is DEAF — assigned DEAF, and the bpc_metadata value flagged as a data-quality note for the owner.

## 3. Pilot cells (7 real + 3 synthetic-only branches)

| # | Cell (item × population) | Source slug | Evidence profile (T1/Co1/T2/Co2/T3/T4–5/T6) | Doctrinal branch exercised | Expected state |
|---|---|---|---|---|---|
| 1 | E-08 Corridor Clear Width × DEAF | `deaf-spatial-design` | 0/4/3/0/2/1/0 | Co-1-anchored best practice; the canonical corridor case (`tier-system.md` §3); floor delta vs 7 jurisdictional_values rows | `stated` |
| 2 | E-12 Entrance Landing / Manoeuvring × MOB | `mobility-built-environment` | 6/5/2/0/2/4/5 | Full mix; T1+Co-1 convergence assessment; regulatory floor present (6 jurisdictional rows) | `stated` |
| 3 | G-03 Grab Bars × MOB | `ot-cpg-built-environment` | 0/0/4/2/0/0/0 | Co-2 (OT CPG) + T2 anchoring (§2.2 condition 3). **No pure Co-2-only cell exists in the corpus** — that exact branch is exercised by `scripts/tests/test_assess_cell_pilot.py` (added after adversarial review caught v1 of this manifest claiming a test that did not yet exist) | `stated` |
| 4 | C-02 Colour-Coded Wayfinding Zones × DEM | `wayfinding-cognitive-science-spatial-design` | 0/0/0/0/7/0/0 | T3-alone — exercises `DR-2026-07-12-tier3-stated-threshold` | per threshold DR |
| 5 | E-06 Level Entry (Zero Step) × MOB | `threshold-and-level-access` | 0/0/0/0/0/5/10 | **The decisive G1 test**: T4–6 only, zero anchoring evidence → `regulatory_stratum_only`; excluded from v_best_practice; map row 3 language in every register (8 jurisdictional floor rows for the delta) | `provisional` + regulatory_stratum_only |
| 6 | G-03 Grab Bars × SCI | `fold-down-grab-bar-specification` | zero linked sources (slug ACTIVE) | `pending` + gap link. **Slug-scoped absence only:** item G-03 has substantial evidence under sibling slug `accessible-bathroom-and-grab-bar` (19 sources incl. 5×T1) that is unreachable at cell grain until `item_bpc_links` is backfilled — the gap text says exactly this (adversarial finding 3), and the pending state records "no evidence *linked for this cell*," never corpus-level ignorance | `pending` |
| 7 | B-10 Visual Fire Alarm × NEU | `visual-fire-alarm-seizure-safety` | 0/0/1/0/3/2/1 | Mixed with a T2 anchor — tests that one anchoring source lifts the cell out of the regulatory stratum while T4–6 stay non-anchoring | `stated` |

Manual mapping judgments: cell 1 DEAF (see §2 note); cell 3 population MOB (grab-bar CPGs address mobility-related transfer; `ot-cpg-built-environment` is MULTI); cell 5 population MOB (level entry is the MOB-paradigm parameter; slug is MULTI); cell 6 population SCI (fold-down grab bars are transfer-dependent-user provisions; slug is MULTI).

**Branches with no real cell — covered by `scripts/tests/test_assess_cell_pilot.py` (synthetic in-memory DB; runnable, not merely claimed):** pure Co-2-only; pure T6-only (`code_floor_only` + jurisdiction-distinctness richness, both directions); all-sources-disqualified and UNVERIFIED-1 flags (§2.8); `not_applicable`-requires-rationale and `divergent`-requires-synthesis_approach (model enforcement). Cell 2's convergence is assessed from real data; whether it diverges is an empirical outcome, not a scripted one.

## 4. Engine

`scripts/assess/assess_cell.py` — pure determination function (`workplan/best-practices-assessment-system.md` §3) under `rule_version="pilot-1"`.

**Full module roster used (per owner directive — no silent omissions):** `schemas/directness.py` (grain-matching + consolidation; G2 NOT_ASSESSED cap applied engine-side), `schemas/tier_derivation.py` (tier-from-anchor-type), `schemas/evidence_state.py` (four-state machine semantics), `schemas/enums.py` (evidence-type/recommendation vocab), `schemas/evidence_source.py` (source-record semantics incl. verification_status gates), `schemas/source_value_extraction.py` (value/range substrate), `schemas/population.py` + `schemas/population_links.py` (population codes/joins), `schemas/slug.py` (slug status), `schemas/bpc_metadata.py` (slug→population), `schemas/gap.py` (pending→gap linkage). **Deliberately not used:** `schemas/room.py` (no room data model exists — named open gap per `workplan/website-v0-path-forward-2026-07-12.md`), `schemas/adversarial_use.py`/`schemas/case_study.py`/`schemas/economics.py`/`schemas/fdr_specialist.py`/`schemas/question.py`/`schemas/throughline.py`/`schemas/temporal.py`/`schemas/conflict.py`/`schemas/decision.py`/`schemas/doctrine*.py`/`schemas/specialist.py`/`schemas/specification.py`/`schemas/item.py`/`schemas/attestation.schema.json` (not part of the determination function's input or output surface; item existence is validated against the live `items` table directly).

G-fix implementation (all additive; no existing schema function modified):
- **G2:** population-directness for a source with no `evidence_population_match` row and a population-specific claim = `NOT_ASSESSED` → consolidation capped at DOWN-WEIGHTED, source flagged `needs_population_assessment`.
- **G3:** Co-1 grain from `co1_source_type` (dpo_research/advocacy_position → aggregate; academic_narrative → specific; peer_reviewed_literature/validated_tool → specific unless the record's scope indicates aggregate design).
- **G6:** `standard_eb` grain = aggregate at tier 2, code at tiers 4–5.
- **G1:** T4/T5 sources keep GRAIN_CODE (no re-graining is claimed for any pilot source — no documented T1/T2 traceability exists in the corpus metadata yet); determinations whose entire admitted basis is T4–6 get `regulatory_stratum_only` (engine-computed), `design_scale='universal'`, and are barred from `stated`.

Output: `working/pilot/data_20260712_pilot-cell-backfill.sql` (migration-formatted; replayable onto canonical DB after owner ratification) + applied to the pilot DB.

## 5. Renderings and integrity checks

- `scripts/generate/pilot_renderings.py` → `working/pilot/pilot-renderings.html`: each cell side-by-side in five roles (designer / disabled person / OT / policymaker / carer) + the advocacy-brief variant; every rendering carries its determination tuple in `data-*` attributes.
- `scripts/audit/register_integrity_check.py`: asserts I1–I5 over the rendered HTML.
- `scripts/validate_evidence_state.py` run against the populated pilot DB.

## 6. Verification log (commands + outcomes recorded as run)

| Check | Discipline | Result |
|---|---|---|
| Matrix–code sweep (`evidence-architecture.md` §10) | diff vs doc table | recorded below |
| Engine determinism | two runs, identical `derivation_sha` set | recorded below |
| Mutation tests | every gate shown firing on injected bad row (exit 1) before its clean pass counts | recorded below |
| I1–I5 register check | over pilot-renderings.html | recorded below |

(Results appended by the run log in §7 as executed.)

## 7. Run log

- 2026-07-12 — setup + migrations applied to copy; counts verified (§1). Matrix–code sweep run: 9/9 grain×scale outcomes + generalizes-beyond-measured branch match `evidence-architecture.md` §3/§10 exactly.
- 2026-07-12 — engine run (`scripts/assess/assess_cell.py`, rule_version pilot-1). All 7 cells produced the manifest-predicted states: E-08×DEAF `stated` (CO1+T2+T3, 7 governing refs); E-12×MOB `stated` (T1+CO1+T2+T3, 13 refs, multi-axis → convergence honestly recorded `pending_assessment` since source_value_extractions is empty — axis co-presence is real, value-level convergence is not claimed unassessed); G-03×MOB `stated` (T2+CO2); C-02×DEM `provisional` (T3-only, per tier3-threshold DR); **E-06×MOB `provisional` + regulatory_stratum_only, design_scale=universal — the decisive G1 test passed**; G-03×SCI `pending` + GAP-297; B-10×NEU `stated` (T2 anchor lifts the cell out of the regulatory stratum; T4–6 sources graded NON-ANCHORING).
- 2026-07-12 — **determinism:** full rebuild + double run ⇒ byte-identical SQL artifacts.
- 2026-07-12 — **validator:** `validate_evidence_state.py --states-only --db pilot` → PASS, 7 cells / 6 convergence rows, 0 errors.
- 2026-07-12 — **mutation suite (validator):** 6/6 injected violations fired (stated+code_floor_only; empty governing_refs; pending without gap; provisional without confidence flag; convergent<2 axes; stated single-axis Tier-3-alone); clean pass after cleanup.
- 2026-07-12 — **register integrity (I1–I5):** `register_integrity_check.py --selftest` — 4/4 tampered invariants fired (tuple divergence, best-practice-on-RSO, claim inflation, floor-without-anchor); clean pass on the real document, 7 cells × 6 registers. **Self-caught defect:** the first REGISTER_MAP draft used "no evidence-anchored best practice exists" in RSO rows — strict I3 flagged the phrase even in negation; wording corrected to "no anchoring evidence (T1/Co-1/T2/Co-2) exists" in both the renderer and `evidence-architecture.md` §6 row 3. The invariant is deliberately a total phrase ban: strongest mechanical rule, negation conveyed by other words.
- 2026-07-12 — **drift findings surfaced by the pilot** (for the ratification package): (1) `schemas/enums.PopulationCode` (25 values) does not match the live `populations` table (22 codes) — SCI, UPL, AUT etc. missing from the enum while FK-enforced in the DB; engine validates identity against the table (canonical per schema-reconciliation DR) and records the drift. (2) `bpc_metadata.population` = NDV for `deaf-spatial-design` (content is DEAF) — data-quality note. (3) `evidence_population_match` covers 26 of 640 sources (27 rows) and `source_value_extractions` is empty — under G2 every unassessed dimension is capped DOWN-WEIGHTED, never silently DIRECT; anchors still anchor (only DISCOUNTED/NON-ANCHORING cannot), so determinations are honest without pretending assessed directness. (4) `jurisdictional_values` stores voluntary standards (BS 8300-2, ISO 21542, CSA B651) as `evidence_tier=6`/`is_code_minimum=1` alongside statutory codes — no instrument-status dimension, so no rendering may say "the law requires X" without a caveat (unification DR execution item 15).

### v2 run log — after independent adversarial review (18 findings; unification DR revision history v2)

- **Engine rebumped to `rule_version="pilot-2"`** (behavior changes: governing-set-only `tier_basis` with supporting strata listed separately; cell-scoped `derivation_sha`; §2.8 `has_unverified_sources`/`all_sources_disqualified` implemented; population-match rows attributed per population or NOT_ASSESSED; §2.3 richness enforces T6 jurisdiction distinctness and names its unchecked clauses; slug-scoped gap text). Full rebuild + double-run: **byte-identical artifacts**, validator PASS (7 cells / 6 convergence rows / 0 errors).
- **CRITICAL fix verified by query:** the replay artifact now amends `v_best_practice` (marker-based interim exclusion; migration 027 adds the real column) — `SELECT ... FROM v_best_practice` returns 5 rows, none `regulatory_stratum_only`. v1 of this manifest claimed this exclusion while migration 026's view provided only the `code_floor_only` filter; the claim was false and is now true.
- **Checker hardened against the three demonstrated bypasses:** tuple-class recomputed from (state, conv, rso-marker) and cross-checked against `data-tuple-class`; `data-rso` must agree with the `(regulatory_stratum_only)` tier-basis marker; `--db` cross-checks every rendered tuple against `evidence_cell_state`; I3 extended to a synonym lexicon over claim+body on RSO cells; I5 inflation lexicon over every rendering. Selftest now 7 mutations — all FIRED, clean pass on the real document with `--db` on. Lexicon checks are documented as a mechanical floor, not a proof of unexpressible inflation.
- **`scripts/tests/test_assess_cell_pilot.py` added** (14 checks, all PASS) — and immediately caught a real bug: `assess_source` records lacked `jurisdiction`, so richness's distinctness check always saw one jurisdiction (masked in the real cells by E-06's T4 branch). Fixed; test suite green.
- **`scripts/audit/matrix_consistency.py` added** (the §10 check-1 script the doctrine referenced): 10/10 PASS.
- **Renderer honesty fixes:** no floor-delta direction claims before value extraction; "legal minimum" → "recorded code minimums" with instrument-status caveat; all floors rendered (no silent truncation); Co-1 solo-authorship limit rendered in every register of Co-1-governed cells; pilot DB stamped `PRAGMA user_version=26`.
- **PR #3 reconciliation:** consolidation sweep merged in; its `schema_reference_drift_audit.py` gains one expected line from this branch (`pilot_renderings.py` → `jurisdictional_values`, resolved when 026 applies at C1) on top of its own by-design FAILs (`room_page.py`, `migrate_evidence_sources_v2.py`); its two new PROPOSED DRs join the ratification package (B8/B9).
