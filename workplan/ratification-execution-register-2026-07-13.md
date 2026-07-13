# Ratification execution register — 2026-07-13
**Authority:** `decisions/RATIFICATION-RECORD-2026-07-13.md` (owner directive "resolve all accept ratify all commit all"). Everything ratified is either EXECUTED (with its commit), STAGED (built, awaiting the one owner-run command), or QUEUED (tracked here; nothing implicit). Per the ratified P3 gate, each execution stage runs the mechanical battery and the whole execution is queued for an independent adversarial pass.

## EXECUTED this session

1. All 16 DR statuses + impact appendix flipped to ACCEPTED with ratification notes; `governance/evidence-architecture.md` → **CANONICAL**; `skills/integrity-protocol_SKILL.md` → **ACTIVE**; ratification package marked RESOLVED.
2. **Migrations authored and committed:** `027_regulatory_stratum_only.sql` (column + final `v_best_practice`), `data_20260713000000_pilot-cell-backfill.sql` (the 7 pilot determinations + GAP-297 + flag backfill; GAP-297 verified unallocated in canonical gaps), `data_20260713000100_weighting-profile-seed.sql` (5 audience profiles incl. advocacy-brief).
3. **Validator extended** (`scripts/validate_evidence_state.py`): G1b `stated`-never-regulatory-stratum-only check, column-aware with marker fallback for pre-027 DBs.
4. **Core doctrine edits (unification-DR execution items 1–3, 9–10; tier3 DR follow-up):** `evidence-methodology.md` §2.2 (G7 T2 anchors; T3-alone thresholds), §2.3 (G1b scale-tagging + `regulatory_stratum_only`), §3.2/§3.4 (G8 render rule; mandatory regulatory-stratum disclaimer on the convergence voice line), §4 vocabulary; `mission-and-epistemics.md` commitments 4/7 (Universal/Population/Person Mode); `audience-priority.md` (G5 advocacy-brief use-pattern row; Population-/Person-Mode wording); `armature_v4.md` §4.5/§4.6 (vocabulary; advocacy-brief cross-ref); `references/project-standards.md` (superseded-ladder RULE reconciled to canonical; two-marker RULE → ●/◐/○ with the G1b bar and the value-support requirement; Co-1 "co-primary at Tier 3–4" contradiction fixed; all Mode P/S removed); `schemas/evidence_state.py` L108 docstring; `governance/pre-stage-a-decisions.md` stated-threshold phrases (×2).

## STAGED — one command for the owner (C1)

The permission layer (correctly) requires the canonical-DB mutation to be run under direct owner review; "[No preference]" on the explicit prompt was not sufficient authorization. Everything is built, committed, and CI-shaped; to complete C1 run:

```
python3 scripts/migrate_db.py --session "session_2026-07-13-ratification-execution-C1"
```

This applies, in order: 026 (evidence_cell_state rebuild + jurisdictional_values), 027 (regulatory_stratum_only + final view), then the data migrations (109 jurisdictional rows; 7 pilot determinations + GAP-297 + flag backfill; 5 weighting profiles), stamps user_version 27, and records the ledger. Then verify: `python3 scripts/validate_evidence_state.py --states-only --db data/guidebook.db` (expect PASS, 7 cells) and the CI reproducibility invariants go green on the next push. **C2 follows C1:** `python3 scripts/generate/population_page.py && python3 scripts/generate/spec_page.py` (+ vetting surface regeneration).

## QUEUED (tracked, sequenced; nothing lost)

| # | Item | Authority | Notes |
|---|---|---|---|
| Q1 | Item V full sweep: remaining "Mode P/S" (~90 files: skills ×8, architecture/page-templates + navigation-modes, secondary governance, conflict-matrices, fdr) + "Tier 1/Tier 2"-as-design-modes (~18 remaining files) | A5-V | Canonical core done (this session); site html regenerates at C2; replay migrations + v9 corpus deliberately untouched (impact appendix) |
| Q2 | `conflicts.status` CHECK rebuild: `MODE-S-ONLY` → `PERSON-MODE-ONLY` + `schemas/conflict.py` + `validate_conflict{,s}.py` + mapper skill, one coordinated migration | A5-V | The single data-level vocabulary dependency; conflicts table is 0 rows — cheap now |
| Q3 | Skills sweep: `cell-curator` (OLD stated threshold), `evidence-auditor`, `guidebook-auditor`, `item-specification-writer` (●-rule), `voice-style` (register map lands here), `literature-review-planner` + `supersession-audit` (OLD ladder) | A5 items 8; impact appendix | Lock-step precedent: tier-system.md §6 |
| Q4 | `schemas/directness.py` promotion: G1/G2/G3/G6 from engine-side pilot-2 paths to module defaults under a new rule_version; `test_directness_2_2.py` updates (breaks by design) | A5 G2/G3/G6 item 5 | After C1 |
| Q5 | Genealogy build: migration for H1 fields + root registry + `v_value_independence`; H3 `population_icf_links` with the FDA-code→population-code crosswalk; H4 gates in the engine | A6 H1–H4 | Before the extraction pass is commissioned (columns-now cost argument) |
| Q6 | H5 harvest: `instrument_status` on jurisdictional_values (A5 item 15); JSON-registry reconciliation audit → metadata migration → redirect stubs; FDR extraction rows | A6 H5; A5 item 15 | Registry-only metadata (tier-correction history, notes, alias ref-ids) migrates BEFORE stub-out |
| Q7 | H6: rename `schemas/fdr_specialist.py` → `failure_demand_recovery.py` + callers | A6 H6 | Mechanical |
| Q8 | `specs/e-08.html`: Koontz 2017 verify-or-purge (external mining item 1); archive to `_archived/` per B9 conventions pending the verdict; fix/regenerate from DB post-C2 | A6 integrity finding 1; B9 | Public-integrity item — first in the external-mining queue |
| Q9 | B9 execution: PI archival (v10_7–v10_13 → `_archived/`), register-snapshot stubs, six archive locations consolidated, handoff convention | B9 | Policy ratified; file moves are its explicitly-deferred follow-up pass |
| Q10 | B8 execution: decision-tracking clause in architecture guidebook; currency headers — `schema-spec.md`: "NO — historical record" (authorized in the ratification record, evidence: wrong co1 enum L78–98); `schema-reconciliation.md`: owner to confirm value | B8 | |
| Q11 | B4 follow-through: confirm migration 015 application status | B4 | One query + note |
| Q12 | SHA-pin + drift hygiene: doctrine edits this session change the doctrine SHA — update pins (`schemas/directness.py`, `tier_derivation.py`, `evidence_state.py`, `skills/multilingual-research_SKILL.md`, `workplan/phase-e-execution-plan-v1.md`), `doctrine_recheck.py` snapshots, `regenerate_vetting_surface.py` blurbs, `index.html:725`, `generate_parts.py` legend | A5 items 12, 14 | Pins reference the doctrine commit sha — update after the doctrine commit lands |
| Q13 | External-mining queue (worked example §9): pre-1980 roots, 1800mm derivation, wheelchair-user turning biomechanics, cross-signed-language spatial grammar, owner-hypothesised counter-strands, GAP-295 anthropometry | A6 | Feeds the first genealogy-driven search-coverage cycle |
| Q14 | Adversarial pass on this ratification execution (per ratified P3) | A7 P3 | Fresh context; attack lines include execution-vs-DR-text divergences |
| Q15 | C3/C4 (owner, outside this repo): restore Actions enforcement or keep self-run gates; scholarly-connector approval (GAP-286); `lang_jur_map` 5 jurisdictions | C3/C4 | Restated so they don't vanish |
