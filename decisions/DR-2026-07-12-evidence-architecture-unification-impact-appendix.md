# Impact appendix — DR-2026-07-12 evidence-architecture unification
**Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECORD-2026-07-13.md** *(was: appendix to `decisions/DR-2026-07-12-evidence-architecture-unification.md` (PROPOSED))*
**Method:** full-repo sweep, 2026-07-12 — 66 code files individually classified; DB inspected read-only; book/site/skills/governance censused. Scenario keys: **(a)** scale-tagging + `regulatory_stratum_only` (G1/G1b); **(b)** vocabulary normalization (Item V); **(c)** grain from co1_source_type / (type × tier) (G3/G6).

## Load-bearing state facts

- Committed `data/guidebook.db` is `user_version=25`; migration 026 + jurisdictional backfill exist but are **unapplied**. `evidence_cell_state` / `convergence_assessment`: 0 rows.
- `scripts/validate_evidence_state.py` (CI-wired at `ci.yml:141`) and `scripts/generate/{spec,population}_page.py` already SELECT post-026 columns (`governing_refs`, `tier_basis`, `code_floor_only`) — **they crash against the committed DB until 026 is applied**. Every scenario-(a) change stacks on an unratified, unapplied migration: sequencing risk #1.
- Two tier ladders are live in prose: NEW (sr_meta@T2, per `tier-system.md`/DR-2026-05-29) and OLD (T2=NGO, T3=SR) — the OLD ladder survives in `references/project-standards.md` (as standing RULES, L17/L26/L35), `references/methodology-evidence-hierarchy-mapping.md`, `skills/literature-review-planner_SKILL.md`, `skills/supersession-audit_SKILL.md`, `schemas/enums.py` docstring, `decisions/DR-2026-05-24-*` search table.
- Evidence distribution (640 sources): T1=64 clinical + 29 Co-1; T2=9 sr_meta + 55 standard_eb + 3 Co-2; T3=181 clinical + 25 grey; T4=66; T5=119; T6=89. All 29 Co-1 rows carry `co1_source_type` (academic_narrative 11, advocacy_position 8, peer_reviewed 5, validated_tool 3, dpo_research 2) — **G3's input data is complete**.
- `evidence_population_match`: 27 rows covering 26 of 640 sources (G2's target); `source_value_extractions`: 0 rows.

## Direction summaries

**Code.** (a) primary edit sites: `scripts/validate_evidence_state.py` (extend code_floor_only checks), `schemas/evidence_state.py` (add field; fix L108 docstring still stating the OLD `stated` threshold), generators + `generate_parts.py` legend, `tools/regenerate_vetting_surface.py` per-tier blurbs (T5 blurb pre-dates G1), `index.html:725` doctrine sentence. (c) primary edit site: `schemas/directness.py` `GRAIN_FROM_EVIDENCE_TYPE` → (type × tier × co1_source_type) function; `scripts/tests/test_directness_2_2.py` breaks by design. New tools now exist (built by the pilot): `scripts/assess/assess_cell.py`, `scripts/generate/pilot_renderings.py`, `scripts/audit/register_integrity_check.py`. Legacy replay paths (`scripts/convert/*`, `scripts/db/*`, `scripts/migrations/session_*`) must **not** be edited — mark deprecated.

**Database.** (a): apply 026, then follow-on 027 (`regulatory_stratum_only` + view updates + `weighting_profile` seed). Zero backfill (0 cells). (b): **one real data+schema migration** — `conflicts.status` CHECK includes `MODE-S-ONLY` (SQLite CHECK ⇒ table rebuild), coordinated with `schemas/conflict.py`, `scripts/validate_conflict{,s}.py`, `cross-population-conflict-mapper_SKILL.md`. (c): no migration; grain is computed, not stored.

**Book.** `parts/v10/` are DB-generated — fix generators, regenerate; never hand-edit. v9 corpus (`versions/current/`, `parts/88_to_90/`, `parts/deprecated/`) uses Tier-1/2-as-design-modes and "Three-Tier Hierarchy" — remediation is Phase E re-synthesis (per DR-2026-06-10-e2g), not find-and-replace. `references/bpc/**` prose contains in-corpus collisions (e.g. "280mm above seat at Tier 2" [design-mode sense] in `accessible-bathroom-and-grab-bar.md`) — re-synthesis scope.

**Site.** `site/specs/*` (89), `site/populations/*` (11), `site/rooms/*` (17) are stale generated pages carrying Mode P/S strings and old tier badges — superseded by regeneration via the rewritten generators post-026. `architecture/page-templates.md` + `navigation-modes.md` display labels "Mode P/Mode S" → (b) edits.

**Skills.** Must change with doctrine: `cell-curator` (**states OLD T3-alone⇒stated threshold — conflicts with tier3 DR**), `evidence-auditor`, `guidebook-auditor` (vocab L78/L164/L169–170), `item-specification-writer` ("● = Tier 1–6" conflicts with the ●/◐/○ split; Mode P/S ×5), `voice-style` (register-map I1–I5 lands here; Mode P/S ×10), `literature-review-planner` + `supersession-audit` (OLD ladder, unfixed), `multilingual-research` (SHA pin). Vocab-only: `connection-auditor`, `connection-discovery`, `cross-population-conflict-mapper`, `functional-deficit-auditor`, `sensory-coherence-checker`.

**Governance/references.** Beyond the canonical six: `references/project-standards.md` (**highest-risk single file** — standing-rules register agents load, restating the superseded ladder as RULEs + 16 Mode P/S uses; feeds `doctrine_recheck.py`); `governance/pre-stage-a-decisions.md` L49/L81 (OLD stated threshold); `architecture/schema-spec.md` L78–98 (**wrong co1_source_type enum + phantom 'co1-collaborator' evidence_type — (c) hard conflict**); `references/global-reference-registry.md` (hybrid "Co-1/N" labels defeating tier+type encoding); (b)-colliding: `adversarial-use-framework.md`, `legal-regulatory.md` (also L29 lumps T4–5 into best-practice synthesis — (a) conflict), `population-taxonomy.md`, `armature_v4_resolutions.md`, `armature_v4_integration.md` (adds a 4th vocabulary, "Tier A/B/C"), `jurisdiction-philosophy.md` L75 (mild (a) conflict).

## Vocabulary collision census (feeds `evidence-architecture.md` §7)

- **"Tier 1/Tier 2" as design modes:** ~22 live files + v9 corpus. Canonical sites: `mission-and-epistemics.md` L61–64/78; `armature_v4.md` L41,124,138,168,299,314–317; `audience-priority.md` L68,74; `evidence-methodology.md` L309,352; `co1-operational.md`; 5 skills; plus secondary governance listed above.
- **"Mode P/Mode S/MODE-S":** 96 files (excl. `_archived`). Data-level: `conflicts.status` CHECK `'MODE-S-ONLY'` — the only place vocabulary is load-bearing in data. Top prose sites: `references/project-standards.md` (16), `skills/voice-style_SKILL.md` (10), `schemas/conflict.py` (7), `governance/evidence-methodology.md` §4 (7).

## Five highest-risk touchpoints

1. **Unapplied migration 026 vs post-026 tooling** — validator + both rewritten generators crash on the committed DB; everything in scenario (a) stacks on this. Owner ratification + application is the unblocking act.
2. **`references/project-standards.md`** — propagates the superseded ladder into all future agent work if skipped; also `doctrine_recheck.py` input.
3. **The `stated`-threshold triangle** — `evidence-methodology.md` §2.2/§2.7 + `schemas/evidence_state.py:108` + `cell-curator_SKILL.md` + `pre-stage-a-decisions.md` still say T3-alone ⇒ stated, while the validator already enforces the opposite (per PROPOSED tier3 DR). Whichever text a Phase-E synthesis agent reads determines the central table's content.
4. **`conflicts.status='MODE-S-ONLY'` CHECK** — vocabulary normalization without a coordinated migration breaks conflict validation and the mapper skill simultaneously.
5. **Auto-propagation machinery** — `tools/regenerate_vetting_surface.py` blurbs republish stale doctrine on every DB push; doctrine SHA 3da73bd pins in `schemas/{directness,tier_derivation,evidence_state}.py`, `skills/multilingual-research_SKILL.md`, `workplan/phase-e-execution-plan-v1.md` + `doctrine_recheck.py` snapshots fail drift checks unless updated in the same change as any doctrine edit.

Runner-up: `references/methodology-evidence-hierarchy-mapping.md` — academic-facing justification still arguing the superseded ladder (rewritten to v2 in this change-set; see DR execution notes).

## Pilot-surfaced drift findings (new; for the ratification package)

- `schemas/enums.PopulationCode` (25 values, compound style `NDV/AUT`) ≠ live `populations` table (22 flat codes; SCI/UPL/AUT/ADHD etc. missing from the enum). Cell identity truth is the table (per schema-reconciliation DR); the enum needs reconciliation.
- `bpc_metadata.population` data-quality: `deaf-spatial-design` carries NDV; content is DEAF.
- `evidence_population_match` 27/640 and `source_value_extractions` 0/640 — the G2 exposure quantified.
