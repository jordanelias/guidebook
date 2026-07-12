# Ratification package — 2026-07-12
**Purpose:** one memo, one sitting. Every PROPOSED decision record in the repository (all 11, verified by grep — none omitted), grouped, each with a one-paragraph statement, a recommendation, what changes on ratification, and the one-line reply that ratifies it. Reply in any form you like; a session directive quoting the item ID with "ratified" / "ratified with amendment: …" / "deferred" is sufficient and will be recorded per decision-capture protocol.

**Why now:** the evidence-hierarchy × design-mode × audience question that shelved the project is resolved in this change-set — doctrinally (`governance/evidence-architecture.md`), operationally (the pilot: 7 real cells through the engine, rendered in six registers, integrity invariants mechanically enforced), and forensically (full-repo impact map). What remains is exactly the class of act only you can perform: ratification.

**The demonstration to look at first:** `working/pilot/pilot-renderings.html` — the same determinations rendered for designer, OT, policymaker, disabled person, carer, and advocacy-brief, with the invariant checks logged in `working/pilot/PILOT-MANIFEST.md` §7. The decisive case is E-06 Level Entry × MOB: fifteen standards/codes converge and the machinery still refuses to call it best practice in any register — that is the intellectual-integrity property you were unable to find a design for, running.

---

## Group A — the evidence-architecture group (blocking the central table)

### A1. `DR-2026-05-29-evidence-hierarchy-reconciliation` — the three-way-fork closure
The oldest keystone: reconciles the sr_meta-at-T2 ladder (owner directive 2026-05-25, "t2>t3 this is enshrined") across mission/methodology prose, closing reconciliation-register item R9. Its doctrine is already executed in `governance/tier-system.md` and the database; only the record is unratified.
**Recommendation:** ratify. **On ratification:** R9 closes; the ladder's governance trail is complete. **Reply:** "A1 ratified."

### A2. `DR-2026-07-12-evidence-cell-state-schema-reconciliation` (v2, adversarially reviewed)
Merges the two incompatible `evidence_cell_state` schemas: keeps `(item_code, population_code)` identity and the directness-aware `convergence_assessment` table; adds `governing_refs` (anti-hallucination), `rule_version`/`derivation_sha` (reproducibility), structured value columns; jurisdiction lives in a separate `jurisdictional_values` table (jurisdiction-in-key was caught reproducing the code-floor conflation). Implemented as migration 026 + backfill, tested twice against throwaway copies — and now exercised end-to-end by the pilot.
**Recommendation:** ratify. **On ratification:** unblocks C1 (applying 026 to the canonical DB). **Reply:** "A2 ratified."

### A3. `DR-2026-07-12-tier3-stated-threshold`
Resolves the question DR-2026-05-29 explicitly declined: Tier-3-alone (either species) does not reach `stated` — T3-clinical-alone ⇒ `provisional`, T3-grey-alone ⇒ `pending`; convergence (≥2 axes) remains the path to `stated`. Validator check already implemented; pilot cell C-02×DEM demonstrates the rule on real data.
**Recommendation:** ratify. **On ratification:** small follow-up prose edits to `evidence-methodology.md` §2.2/§2.7 (execution list, unification DR items). **Reply:** "A3 ratified."

### A4. `DR-2026-07-12-website-architecture-lock`
Rejects the Postgres/Directus/Meilisearch/Vercel stack in favour of extending the working static-generation pattern; defers the armature_v4 axis model to v2.
**Recommendation:** ratify. **On ratification:** website v0 path (`workplan/website-v0-path-forward-2026-07-12.md`) is unblocked behind C1/C2. **Reply:** "A4 ratified."

### A5. `DR-2026-07-12-evidence-architecture-unification` — the new keystone (items separately answerable)
Adopts `governance/evidence-architecture.md` as the canonical single entry point, and resolves the six gaps adversarial review found at the edges of the existing D-D resolution:
- **G1** — close the convergence-laundering channel: scale-tagged determinations; `regulatory_stratum_only` (T4–6-only, extending `code_floor_only`); T4/T5 re-graining only with documented T1/T2 traceability. *The deepest integrity fix; demonstrated by pilot cell E-06.*
- **G2** — NOT_ASSESSED ≠ not-applicable in directness consolidation (verified bug at `schemas/directness.py:225`; 27/640 sources have population-match rows — without this fix ~96% would silently grade DIRECT).
- **G3** — Co-1 grain follows `co1_source_type` (DPO positions are population-grain: they anchor Population-Mode claims and never override an individual at Person Mode; narratives are the reverse).
- **G4** — the asymmetry principle, stated: *at each scale the anchoring authority is the entity whose grain is that scale — the code at Universal, the evidence ladder at Population, the person themselves at Person.* Declarative; unifies what D-D already decided.
- **G5** — "advocate" becomes an advocacy-brief use-pattern within the disabled-person primary audience (emphasis: code-vs-evidence delta + rights framing + citable strength), not a fifth audience.
- **G6** — grain derives from (evidence_type × tier): `standard_eb` at T2 is synthesis-grain, at T4/T5 code-grain (verified latent contradiction with §1.6 otherwise).
- **Item V** — vocabulary normalization: Universal/Population/Person Mode as sole design-scale names; "Tier N" reserved for evidence; "Mode P/S" deprecated (96 files; one real data migration: `conflicts.status` CHECK).
- **Item R** — the claim-strength register map + invariants I1–I5 as the testable form of "role changes register, never data."
**Recommendation:** ratify all; each item independently answerable (dependencies: G1c needs G6; R needs G1). **Reply:** "A5 ratified in full" or per item, e.g. "A5: G1–G4, G6, V, R ratified; G5 amended: …".

## Group B — outstanding May-era proposals (ratify or explicitly defer; none should stay in limbo)

### B1. `DR-2026-05-19-channel-2-manual-verification`
Manual verification track for standards-body/government-portal sources pending the V2-automated scrapers. Self-authored-bias caveat is declared in the DR itself.
**Recommendation:** ratify — the manual track has been the de-facto practice since May. **Reply:** "B1 ratified."

### B2. `DR-2026-05-20-evidence-metadata-rehabilitation`
Type-routed metadata rehabilitation protocol with mandatory cross-check, motivated by 40% metadata drift in the probed cohorts (note-as-title, journal-as-title, programme-as-standard).
**Recommendation:** ratify — the verification workflows already run on it. **Reply:** "B2 ratified."

### B3. `DR-2026-05-23-pre-rehab-banner-cohort-definition`
Operational sharpening of standing rule #10's banner cohort (which BPCs carry `PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION`). The 68 RETRACTED-PRE-REHAB rows in `bpc_metadata` already follow it.
**Recommendation:** ratify (retrospective alignment of record with practice). **Reply:** "B3 ratified."

### B4. `DR-2026-05-24-best-practice-supersession-protocol`
Slug closure requires supersession checking (best *current* evidence), not just citation-mining completeness; 134 `supersession_check` rows exist. Notes migration 015 application as a pending condition — verify its status when ratifying.
**Recommendation:** ratify, with a one-line confirmation of migration 015 state. **Reply:** "B4 ratified; 015 status confirmed as …".

### B5. `DR-2026-05-26-gap-driven-mining-protocol`
Gap-keyed (rather than anchor-keyed) citation mining; closes GAP-283 per your 2026-05-23 direction. Worked-example pilot was the stated pending condition.
**Recommendation:** ratify or explicitly defer pending the worked example — either ends the limbo. **Reply:** "B5 ratified" / "B5 deferred pending worked example."

### B6. `DR-2026-05-28-b-source-value-extractions-schema`
The value-directness substrate (migration 018, applied; adopted-in-effect). Note: the table has **0 rows** — the pilot records this as the reason value-level convergence is honestly `pending_assessment` rather than claimed. Ratification + an extraction workplan makes the value dimension real.
**Recommendation:** ratify the schema; commission the extraction pass as Phase-E work. **Reply:** "B6 ratified."

### B7. `DR-2026-05-28-c-population-junctions-governance-close`
Retrospective governance record for migration 021 (population junctions on the value-claim tables; FK-enforced, applied).
**Recommendation:** ratify (pure governance hygiene). **Reply:** "B7 ratified."

## Group C — owner-only actions (cannot be performed by an agent)

1. **C1 — apply to the canonical DB** (after A2/A3/A5): migration 026 + `data_20260712150000_jurisdictional-values-backfill.sql` + the pilot-rows artifact `working/pilot/data_20260712_pilot-cell-backfill.sql` (deterministic, replayable; or defer pilot rows and let Phase-E backfill produce them at scale under the ratified rules). Until 026 is applied, `validate_evidence_state.py` DB mode and the rewritten site generators cannot run against the committed DB (impact appendix, risk #1).
2. **C2 — regenerate** `site/populations/`, `site/specs/`, and the vetting surface after C1.
3. **C3 — attestation/CI decision:** the new DRs have no attestation JSONs; two CI checks are expected red pending your call (per `workplan/website-v0-path-forward-2026-07-12.md`; you removed Actions enforcement 2026-06-09 — decide whether to restore or keep self-run gates).
4. **C4 — standing external blockers** (unchanged, restated so they don't vanish): scholarly-connector approval (GAP-286 / D-4.3-C, outstanding since 2026-05-11, claude.ai project-settings action); `lang_jur_map` PRIMARY/SECONDARY criteria ratification + the 5 unmapped jurisdictions (NG, GH, ZA, PH, SG).

## Drift findings surfaced by the pilot (for awareness; fixes are execution items in A5)

- `schemas/enums.PopulationCode` (25 values, compound style) ≠ live `populations` table (22 flat codes; SCI/UPL/AUT/ADHD FK-valid but enum-absent).
- `bpc_metadata.population` = NDV for `deaf-spatial-design` (content is DEAF).
- Directness substrate coverage: `evidence_population_match` 27/640; `source_value_extractions` 0/640 — under G2 the engine caps unassessed dimensions at DOWN-WEIGHTED rather than pretending directness; coverage growth is Phase-E work.
