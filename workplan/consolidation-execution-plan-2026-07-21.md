# Consolidation Execution Plan — for a new session

**Date:** 2026-07-21
**Status:** Plan / handoff. Forward execution plan, not a Decision Record and not a new audit.
**Prepared by:** Claude, after an adversarial pass on a (discarded) fresh consolidation register.
**Read-first anchors (do NOT re-sweep):** `audits/project-inventory-and-state-2026-07-12.md`, `audits/consolidation-sweep-2026-07-12.md`, `architecture/consolidation-remediation-roadmap-2026-07-12.md`, `decisions/DR-2026-07-12-versioning-and-archive-consolidation.md` (ACCEPTED), `decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md` (ACCEPTED).

---

## 0. The one thing to understand before doing anything

**The divergent-source problem is already catalogued, and the archival half is already ratified — it was just never executed.** A new session's job is **execution and the few genuinely-new items**, not another sweep. In fact, the session that produced this plan first wrote a brand-new 18-cluster consolidation register *without* finding the existing 2026-07-12 apparatus — i.e. it created a divergent source about divergent sources. That register was discarded. **Do not repeat it. Extend the existing docs; do not fork them.**

## 1. Corrected findings (adversarial pass — trust these over any older doc)

Every one of these was re-verified against current `main` this session; several older claims were stale:

| Claim in circulation | Corrected status |
|---|---|
| `specs/e-08.html` rests on a fabricated "Koontz 2017" anchor | **PURGED** (commit `139e05e`). Current "koontz" strings are the page *documenting its own past error*. Not a live issue. Residual: the four-value drift (tier-system §3 `2440` vs divergence-matrix `1800` vs item-name `≥1200` vs page) should be re-checked for reconciliation — **lower priority**. |
| The 8 `project-instructions-v10_*` files are a versioning bug | **Prescribed pattern** — PI is not API-writable; owner pastes a full doc into claude.ai. Fix = archive `v10_7`–`v10_13`, keep `v10_14` (already `DR-2026-07-12` item 1). |
| `mission-PROVISIONAL.md` can be deleted | **Referenced by ~6 live governance docs** → redirect stub only, never delete. |
| `armature_v3_review`→`v4*` is version-forking to archive | **Design-review sequence** (sweep correction C) → consolidate into one doc (roadmap P2), do not archive as "superseded." |
| Connection registers shadow the DB | `connection-register.md` is **already a redirect stub**. Live divergence that remains: `connection-register-active.md` (3486 lines, PENDING) + `references/connections/` topic dirs + DB `connections` (273 rows). |
| Verified-source JSON registries are retired | **Still live** (6 files, ~551 entries, `01/RAP-*` alt-id scheme). Retirement is owed (`DR-2026-07-13` H5). |

## 2. Execution sequence

Do these in order. Each phase is owner-gated where it moves or retires files (per `DR-2026-07-12` "Consequences": each move benefits from owner review, not a unilateral mechanical pass).

### Phase A — Execute the already-ratified archival consolidation (`DR-2026-07-12`; AUTHORIZED, undone)
- **A0 (gate):** confirm with owner which PI version is pasted-live in claude.ai (expected `v10_14`).
- **A1:** move `governance/project-instructions-v10_7.md`…`v10_13.md` → `_archived/governance/` (keep `v10_14`). No content rewrite.
- **A2:** fold the six archive-ish locations — `misc/archived/`, `_archived/misc-2026/`, `_archived/working-2026/`, `parts/_archived/`, `parts/deprecated/`, `parts/88_to_90/` (≈89 files) — under `_archived/`, mirroring origin path.
- **A3:** register-snapshot ban (item 2) — reduce `gap_register*.md` and the dated `audits/_archived/tier*-verification-*.md` snapshots to one live path each; redirect stubs elsewhere.
- **A4:** relocate the 10 handoff docs → `sessions/handoffs/handoff-<topic>-<date>.md` (item 4), redirect stubs at old paths.

### Phase B — DB source-of-truth retirements (`DR-2026-07-13` H5; genuinely open)
The DB is the single source of truth (`project-architecture-guidebook-v2.3.md` `<data_layer_pattern>`); md/yaml/json shadows were never retired. That is the root of most remaining divergence.
- **B1:** reconcile the 6 `references/{tier1,tier2,tier3,tier456,co1,co2}-verified-sources.json` against `evidence_sources` (disagreements are findings); migrate registry-only metadata (`original_tier`/`corrected_tier`, `01/RAP-*` aliases); then redirect-stub retire.
- **B2:** load `data/jurisdictional_values/*.yaml` (20) → DB `jurisdictional_values`; retire yaml.
- **B3:** reconcile `connection-register-active.md` (PENDING) + `references/connections/` dirs against DB `connections`; retire md to stubs (`connection-discovery` already writes the DB).

### Phase C — Doctrine / attestation coherence (`DR-2026-07-14` + `DR-2026-07-21`; mechanism half-built)
- **C1:** finish the re-attestation mechanism on branch **`claude/re-attestation-materiality-triage`** — `schemas/attestation.schema.json` (`reattestation` block) and `governance/doctrine-deltas.json` (state manifest with blob+commit aliases) are **committed**; still needed: the `check_7` materiality-scoping patch that reads the manifest, the `RE_ATTESTATION_WINDOW` justification (M5), then discharge the material backlog by genuine re-review (immaterial files auto-pass under the new check). See `decisions/DR-2026-07-21-re-attestation-materiality-and-window.md`.
- **C2:** canonicalize the doctrine SHA to the **blob-sha** convention (resolving the commit-sha↔blob-sha drift `DR-2026-07-14` flagged); `governance/doctrine-deltas.json` is the alias map.

### Phase D — Governance doctrine de-duplication (roadmap P2; the deepest fix)
- **D1:** one authoritative statement per doctrine (the three design modes; the seven tiers) with pointers instead of restatement, so a future reconciliation touches one file — not the "10+ canonical spots" the Person-Mode fix had to chase (`c6109ec`).
- **D2:** schema-doc currency markers (roadmap Principle 5 / companion DR) on `architecture/schema-spec.md`, `schema-reconciliation.md`.
- **D3:** consolidate the armature four-doc chain into one.

## 3. Guardrails (the failure modes this session hit)
1. **Re-verify every divergence claim against current files before acting.** The E-08 stale-anchor error came from trusting a prior document. Older audits describe a moving repo.
2. **Redirect-stub, never delete, anything still referenced.** (`mission-PROVISIONAL`, connection registers.)
3. **Do not create a new register/sweep.** Extend `audits/consolidation-sweep-2026-07-12.md` and this plan.
4. **Owner-gate file moves and retirements.** Ratified policy still calls for review before each execution pass.
5. **Prefer the DB.** When two stores disagree, the DB is canonical; the md/yaml/json is the thing to retire, after a reconciliation audit that treats disagreements as findings.

## 4. State at handoff
- Branch `claude/re-attestation-materiality-triage`: `schemas/attestation.schema.json` + `governance/doctrine-deltas.json` committed (Phase C1 substrate). No PR open (WIP).
- The 18-cluster consolidation register produced earlier this session is **discarded, not persisted** — it duplicated the 2026-07-12 apparatus. Its only non-redundant contributions are Phases B and C above.
- Nothing in Phases A–D has been executed yet; this is the plan, not the work.
