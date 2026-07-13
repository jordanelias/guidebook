# Ratification execution register — 2026-07-13
**Authority:** `decisions/RATIFICATION-RECORD-2026-07-13.md` (owner directive "resolve all accept ratify all commit all"). Everything ratified is either EXECUTED (with its commit), STAGED (built, awaiting the one owner-run command), or QUEUED (tracked here; nothing implicit). Per the ratified P3 gate, each execution stage runs the mechanical battery and the whole execution is queued for an independent adversarial pass.

## EXECUTED this session

1. All 16 DR statuses + impact appendix flipped to ACCEPTED with ratification notes; `governance/evidence-architecture.md` → **CANONICAL**; `skills/integrity-protocol_SKILL.md` → **ACTIVE**; ratification package marked RESOLVED.
2. **Migrations authored and committed:** `027_regulatory_stratum_only.sql` (column + final `v_best_practice`), `data_20260713000000_pilot-cell-backfill.sql` (the 7 pilot determinations + GAP-297 + flag backfill; GAP-297 verified unallocated in canonical gaps), `data_20260713000100_weighting-profile-seed.sql` (5 audience profiles incl. advocacy-brief).
3. **Validator extended** (`scripts/validate_evidence_state.py`): G1b `stated`-never-regulatory-stratum-only check, column-aware with marker fallback for pre-027 DBs.
4. **Core doctrine edits (unification-DR execution items 1–3, 9–10; tier3 DR follow-up):** `evidence-methodology.md` §2.2 (G7 T2 anchors; T3-alone thresholds), §2.3 (G1b scale-tagging + `regulatory_stratum_only`), §3.2/§3.4 (G8 render rule; mandatory regulatory-stratum disclaimer on the convergence voice line), §4 vocabulary; `mission-and-epistemics.md` commitments 4/7 (Universal/Population/Person Mode); `audience-priority.md` (G5 advocacy-brief use-pattern row; Population-/Person-Mode wording); `armature_v4.md` §4.5/§4.6 (vocabulary; advocacy-brief cross-ref); `references/project-standards.md` (superseded-ladder RULE reconciled to canonical; two-marker RULE → ●/◐/○ with the G1b bar and the value-support requirement; Co-1 "co-primary at Tier 3–4" contradiction fixed; all Mode P/S removed); `schemas/evidence_state.py` L108 docstring; `governance/pre-stage-a-decisions.md` stated-threshold phrases (×2).
5. **C1 executed** (owner-run command, this session, direct owner authorization given in-conversation): `python3 scripts/migrate_db.py --session "session_2026-07-13-ratification-execution-C1"` — VERIFIED-BY: command run against `data/guidebook.db`, transcript below. A pre-migration copy of the DB was taken before running (rollback path, not needed).

   ```
   Current schema version: 25
   --- Schema migrations ---
     Applying 026_reconcile_evidence_cell_state.sql (→ version 26)...
     Applying 027_regulatory_stratum_only.sql (→ version 27)...
   --- Data migrations ---
     Applying data_20260712150000_jurisdictional-values-backfill.sql...
     Applying data_20260713000000_pilot-cell-backfill.sql...
     Applying data_20260713000100_weighting-profile-seed.sql...
   Done. Schema at version 27; 3 data migration(s) applied.
   ```

   Post-migration state — VERIFIED-BY: direct query against `data/guidebook.db`: `user_version=27`; `jurisdictional_values`=109 rows; `weighting_profile`=5 rows; `evidence_cell_state`=7 rows; `PRAGMA foreign_key_check`=0 rows; `regulatory_stratum_only=1` count=1 (E-06×MOB, the decisive G1 cell, matching the pilot manifest's prediction — RECOUNTED: exactly 1 of 7 cells).

   Mechanical battery — VERIFIED-BY, all run against the post-migration `data/guidebook.db` this session:
   - `validate_evidence_state.py --states-only --db data/guidebook.db` → PASS, 13 records checked, 0 errors, 0 warnings (7 cells, 6 convergence rows).
   - `register_integrity_check.py --selftest --db data/guidebook.db working/pilot/pilot-renderings.html` → 7/7 mutation invariants FIRED, clean pass on the real document, PASS I1–I5 across 7 cells × 6 registers with the DB cross-check on.
   - `scripts/audit/matrix_consistency.py` → PASS 10/10.
   - `scripts/tests/test_assess_cell_pilot.py` → PASS, 14/14 checks (run directly; `pytest` is not installed in this environment).
   - `scripts/doctrine_recheck.py` → 3 WARNINGS (`evidence-architecture.md` → `tier-system.md`/`armature_v4.md`; `migration-survival.md` → `repo-strategy.md`, all not CANONICAL-inventoried) — RECOUNTED: identical output confirmed via `git stash` against the pre-C1 tree. N/A: this check has no DB dependency (no `sqlite3` import in the script, no governance `.md` file touched by C1) and could not have detected a migration-introduced defect either way — the "before/after" framing in an earlier draft of this entry overstated what the stash/pop demonstrated; corrected here per the adversarial pass (finding 2, below).
   - `scripts/audit/schema_reference_drift_audit.py` → VERDICT: FAIL, 7 unresolved references, all pre-existing by-design (`room_page.py` ×6, `migrate_evidence_sources_v2.py` ×1) per `PILOT-MANIFEST.md` §v2 run log; the previously-expected `pilot_renderings.py`→`jurisdictional_values` line is now resolved (absent from the FAIL list), confirming migration 026 landed the referenced table.
   - `scripts/audit/source_slug_links_duplicates.py` → 0 duplicate sets, 0 excess rows.
   - `scripts/migrate_db.py --rebuild` (fresh DB from migration history alone) cross-checked against the committed DB on the 7 CI-invariant tables plus `evidence_cell_state`/`jurisdictional_values`/`weighting_profile` → PASS, all 10 counts match (migration-reproducibility gate, GAP-290).
   - `scripts/audit/adherence_log_audit.py --check presence --check schema --base c559d32` (base = the pre-PR#4 merge commit, i.e. cumulative diff for this whole evidence-architecture branch, not just this commit) → No issues (61 changed files, 12 attestations, 20 synthesis files). RECOUNTED, corrected from an earlier draft of this entry that quoted 59/12/20 without a recorded `--base` — unreproducible against any real point in this branch's history; see the adversarial pass's finding 1, below.
   - `claims_docket.py check` → no docket present for this update at check time (nothing to check); see below for the run against this update's own diff.

   C2 (site regeneration) is explicitly **not** run as part of C1 — it remains a separate owner-authorized step per the ratification record, queued below as it always was.

## Independent adversarial pass (Mode 3 item 2) — this C1 execution

Fresh-context agent, briefed to BREAK, presumption of ≥1 defect, re-ran the migration/battery from scratch rather than trusting the log above. Result: the DB migration itself (schema, row counts, FK integrity, and — the highest-stakes check — the from-scratch `--rebuild` comparison against the committed DB on all 10 invariant counts) reproduced exactly under independent re-verification. Two findings on the *documentation* of the work, both fixed in this entry (no findings unfixed or unrebutted, per the P3 gate):

1. **HIGH — unreproducible absolute claim, evaded the Mode-2 docket.** The first draft of the `adherence_log_audit.py` line above quoted "59 changed files, 12 attestations, 20 synthesis files" with no `--base` recorded; the reviewer swept every commit in this branch's real history as a candidate base and found no base produces that triple (closest: 61/12/20 at the pre-PR#4 merge point, which is the base a "branch to date" claim should have used). The line matched none of `claims_docket.py`'s four trigger regexes (bare counts with no unit/`N of M` phrasing aren't covered), so it slipped past Mode 2 entirely — the exact lexicon-gap failure the skill document names as a known limit of the scanner. **Fixed:** re-ran with the base made explicit (`c559d32`, the pre-PR#4 merge commit) and corrected the figures above to 61/12/20, RECOUNTED. **Follow-up (not done here, scope discipline):** `claims_docket.py`'s trigger lexicon could add a bare-integer-count pattern to catch this claim class in future sessions — queued as Q16 below rather than modified speculatively in this DB-migration-scoped commit.
2. **LOW/cosmetic — misleading rigor framing.** The `doctrine_recheck.py` line's original "run before and after C1" phrasing implied a targeted safety cross-check; the script has no DB dependency and C1 touched no governance files, so the stash/pop could not have produced a different result regardless of what the migration did. **Fixed:** reworded above to state the check's actual (lack of) relationship to the migration.

Everything else the reviewer attacked (GAP-297's absence pre-C1 / presence post-C1 pulled directly from the pre-C1 DB blob via `git show`; `convergence_assessment`↔`evidence_cell_state` join orphan check beyond the FK check; `v_best_practice` returning 5 rows none RSO; a read of the actual rendered HTML across all 6 audience registers for the CRPD/ethics lens, incl. the Co-1 solo-authorship caveat and the regulatory-stratum "convergence is not evidence" framing; scope check via `git show --stat` confirming only the 3 intended files changed) survived independent re-verification without a finding.

## C1 — COMPLETE (was: STAGED)

Executed this session under direct owner authorization (chat instruction, this session, from the owner's registered account). See item 5 above for the full run log. The register's original staging note is preserved below for the record.

> The permission layer (correctly) requires the canonical-DB mutation to be run under direct owner review; "[No preference]" on the explicit prompt was not sufficient authorization. Everything is built, committed, and CI-shaped; to complete C1 run:
>
> ```
> python3 scripts/migrate_db.py --session "session_2026-07-13-ratification-execution-C1"
> ```
>
> This applies, in order: 026 (evidence_cell_state rebuild + jurisdictional_values), 027 (regulatory_stratum_only + final view), then the data migrations (109 jurisdictional rows; 7 pilot determinations + GAP-297 + flag backfill; 5 weighting profiles), stamps user_version 27, and records the ledger. Then verify: `python3 scripts/validate_evidence_state.py --states-only --db data/guidebook.db` (expect PASS, 7 cells) and the CI reproducibility invariants go green on the next push. **C2 follows C1:** `python3 scripts/generate/population_page.py && python3 scripts/generate/spec_page.py` (+ vetting surface regeneration).

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
| Q16 | `claims_docket.py` trigger lexicon: add a bare-integer-count pattern (e.g. "N changed files / N attestations") — the C1 adversarial pass caught one such claim (59 vs. actual 61) that the scanner's four existing trigger regexes don't cover | C1 adversarial pass finding 1 | Mechanical scanner change; wants its own selftest addition per Mode 1's verifier-selftest rule, kept out of the DB-migration-scoped C1 commit |
