# DR-2026-07-21: Re-attestation by materiality triage — discharging the doctrine-change attestation debt without laundering

- Status: **RATIFIED (mechanism) — owner directive 2026-07-21.** M1 (materiality triage), M3 (schema `reattestation` block — shipped PR #43), M4 (doctrine-delta manifest — shipped PR #43; the check #7 materiality-scoping patch — this branch), and M5 (flat window superseded by materiality-scoping) are executed. **M2 (backlog discharge) is deferred to a separate, explicitly-approved pass:** the safety classifier correctly blocked a bulk re-stamp, and per this DR's own anti-laundering guidance the material re-groundings are done as a reviewed batch, not an automated migration. (Authored on owner directive 2026-07-21 ("propose methodology to resolve all issues"), where "all issues" = the standing CHECK-7 re-attestation backlog surfaced repeatedly by the non-blocking Level-2 evidence job on PR #42. Was: PROPOSED — pending owner ratification.)
- Date: 2026-07-21
- Prepared by: Claude. This DR **proposes and does not enact** the backlog discharge — matching the `DR-2026-07-14` precedent of investigating a doctrine-attestation issue and leaving the mass action for an explicit owner decision, precisely because a blanket re-stamp is the laundering failure mode the attestation system exists to prevent.
- Affects (if ratified): `scripts/audit/adherence_log_audit.py` (check #7 becomes materiality-scoped); `schemas/attestation.schema.json` (optional `reattestation` block); `workplan/adherence-attestation-build-2026-05-17.md` §5 (closes the flagged-open `RE_ATTESTATION_WINDOW` justification, line 594); a one-time backlog-discharge pass over ~21 stale attestations.
- Related: `workplan/adherence-attestation-build-2026-05-17.md` (the system's design; line 56 "what matters is downstream re-grounding", line 594 "default 5 is unjustified; author a DR"); `DR-2026-07-14-person-mode-governance-reconciliation` (the doctrine change that opened this window; its commit `c6109ec` explicitly names the debt as a deferred "Stage 4.1 sweep" it "resets the window but does not discharge"); `DR-2026-07-13-attestation-rule-identifier-registry-gap` (prior attestation-mechanism DR); the six-tier / convergence-not-evidence doctrine (materiality reasoning is the same discipline applied to the audit layer).

## Context — one blunt check, two real problems

CHECK 7 fires when the last doctrine-touching commit is `> RE_ATTESTATION_WINDOW` (=5) commits back and any attestation's last-modifying commit predates it (`scripts/audit/adherence_log_audit.py` check #7). On PR #42's head it reports **~21 stale attestations, "148 commits ago."** Two problems, both already flagged-open in the project's own record:

1. **The window cannot absorb a corpus-wide re-grounding.** A doctrine edit instantly makes the *entire* attestation corpus "stale," and a 5-commit window is structurally impossible to satisfy for dozens of files — so the Level-2 job is red on *every* PR after any doctrine change (which is why it ships `continue-on-error`). The workplan already concedes the number is a placeholder: *"Default 5 is first-pass… Adopt with explicit caveat that the number is unjustified; revisit… author a DR justifying the final value"* (§5, line 594). The doctrine commit `c6109ec` itself records the debt as a known, deferred **Stage 4.1 sweep** it "does not discharge."

2. **The check is materiality-blind — and the obvious "fix" is laundering.** check #7 globs every `*.json` and flags any file older than the doctrine commit, regardless of whether the doctrine *delta* has anything to do with that artifact. The delta here is narrow: the Person Mode reconciliation removed the "population range **bounds** the person" framing (`c6109ec`: *"population informs the process, never bounds the answer"*). That bears on `person-mode`/`three-modes`/range artifacts and on essentially nothing in `DR-2026-06-11-remove-colonial-role` or a citation-mining session record. Bulk-updating 21 `doctrine_sha` values to `373255e` would turn the check green while asserting "I re-grounded this against the new doctrine" for artifacts nobody re-read — the exact convergence-laundering / rubber-stamp failure the whole tier system is built to refuse. Re-attestation means *re-grounding* (workplan line 56); a stamp that records no reasoning is not re-grounding.

A side finding worth recording: the check is **history-depth sensitive** — on a shallow clone `_last_doctrine_sha` resolves to the file's apparent creation commit and under-reports (1 stale locally vs ~21 in CI's `fetch-depth: 0` run). CI is authoritative; any tooling built on check #7 must run against full history.

## Proposed methodology — five items

### M1 — Materiality triage, not blanket re-stamp *(the core)*

A re-attestation obligation is real only where the **doctrine delta intersects the attestation's scope** (its `rules_in_scope` and the subject its artifact governs). Each stale attestation is classified against the *specific* delta:

- **MATERIAL** — the delta bears on the artifact → **genuine re-review**; the re-attestation reason cites the delta and what was re-checked; the **verdict may change** (that is the point). Never a mechanical bump.
- **IMMATERIAL** — the delta does not touch the artifact → a **currency refresh**: a minimal, *honest* re-attestation whose reason states the reasoning for immateriality (*"delta = Person-Mode range-bounding; this artifact governs X, which the delta does not touch; no material change, verdict unchanged"*). This records a checkable judgment, so it is re-grounding, not laundering.

### M2 — The current backlog, triaged (the worked demonstration)

Delta = the Person Mode "range does not bound the person" reconciliation (`c6109ec` / `DR-2026-07-14`). The ~21 stale attestations classify as:

| Class | Attestations | Discharge |
|---|---|---|
| **MATERIAL** (Person-Mode / three-modes / mode-conditioned adjudication) | `DR-2026-07-13-person-mode-functional-capacity-not-population-range`; `DR-2026-07-14-person-mode-governance-reconciliation`; `DR-2026-07-13-integrity-protocol-three-modes`; `DR-2026-07-13-value-genealogy-and-derivation-handshake` + `session_2026-07-13-value-genealogy-mining-dossier` (Person-Mode handshake); `RATIFICATION-PACKAGE-2026-07-12` + `RATIFICATION-RECORD-2026-07-13` (bundles ratifying the Person-Mode DRs) | Genuine re-review against the delta; re-attest with a delta-specific reason; verdict re-evaluated |
| **IMMATERIAL** (no Person-Mode bearing) | `DR-2026-06-11-remove-colonial-role`; `DR-2026-07-12-{decision-tracking-naming-and-schema-doc-currency, evidence-architecture-unification(+impact-appendix), evidence-cell-state-schema-reconciliation, tier3-stated-threshold, versioning-and-archive-consolidation, website-architecture-lock}`; `DR-2026-07-13-attestation-rule-identifier-registry-gap`; `PI-update-needed`; `session_2026-05-{19-deployment-state-reconciliation, 20-ato-rehab, 23-bpc-rewrite-phase-b-closure, 26-gap-driven-mining-protocol-design}` | Currency refresh with recorded immateriality reason |

(Borderline calls — e.g. `evidence-architecture-unification` — resolve to MATERIAL if in doubt; the asymmetry favors re-review over stamping. The exact list is drawn from CI's full-history run, not the shallow local clone.)

### M3 — Forward-only re-attestation record (respect immutability)

Attestations are forward-only/immutable (`DR-2026-07-14` §Doctrine-SHA identity: *"because attestations are forward-only/immutable, it is not edited"*). Re-attestation must therefore **append, not overwrite intent**. Extend `attestation.schema.json` (currently `additionalProperties:false`) with an optional `reattestation` block: `{prior_doctrine_sha, delta_ref (the doctrine commit/DR), materiality: MATERIAL|IMMATERIAL, verdict_change: none|<new>, reason}`. A re-attestation updates `doctrine_sha` to current **and** pushes a `reattestation` entry — so the currency bump always carries its justification, and the audit trail shows *why* each file was cleared. Until the schema ships, the interim honest form is: update `doctrine_sha`, rewrite the affected `per_rule` reason / counterclaim to state the re-grounding, commit with the `[DOCTRINE: <current>]` token (the currency proof).

### M4 — Make check #7 materiality-scoped, and put the obligation on the doctrine-changer

Two coupled fixes so this stops recurring:

- **Doctrine-delta manifest.** A doctrine-touching commit records a small delta scope (which commitments/sections changed + affected rule-ids), e.g. in the commit body or a sidecar the check reads. check #7 then flags only attestations whose scope **intersects** the delta — immaterial artifacts never trip it.
- **Obligation lands on the doctrine-change session, not every future PR.** The session that edits doctrine knows the delta; it is responsible for the MATERIAL re-reviews and the IMMATERIAL currency batch **before window expiry**, discharging the debt at the source. An unrelated downstream PR is never gated by a doctrine edit it had nothing to do with. This is the H5 pattern from `DR-2026-07-13`: turn the debt into a scoped, owned work-queue rather than an ambient tripwire.

### M5 — Justify the window (closes workplan §5 line 594)

Replace the unjustified flat `RE_ATTESTATION_WINDOW=5` with a **materiality-scoped obligation**: MATERIAL attestations re-attest within N commits **or by next session close** (whichever first); IMMATERIAL cleared by the doctrine-change session's currency batch. The remaining free parameter (N for the material set — a handful, not the corpus) is now small enough to be satisfiable, and its value is set here with the cadence caveat the workplan asked for.

## What this extends (and deliberately does not do)

Extends: the attestation system's own stated intent (*"what matters is downstream re-grounding"*), `DR-2026-07-14`'s forward-only principle, `DR-2026-07-13-attestation-rule-identifier-registry-gap` (rule-id scoping is the substrate M4's intersection test queries), and the project's core anti-laundering discipline (materiality is the same test the tier system applies to convergence).

Does **not**: rewrite any historical attestation's verdict (forward-only); auto-clear the backlog on ratification (the MATERIAL set requires real re-review, which is work, not a migration); or touch the ICCT work on the same branch — this is a **separable concern** and should ideally land as its own PR.

## Consequences if ratified

One backlog-discharge pass (M2: ~7 MATERIAL re-reviews + ~14 IMMATERIAL currency refreshes, each with a recorded reason); a check #7 patch (M4) + schema extension (M3, one migration-free JSON-schema edit); the Level-2 evidence job goes green *honestly* and **stays** green through future doctrine edits because immaterial artifacts no longer trip it. The non-blocking job can then be promoted toward blocking (its shakedown goal) without a permanent red floor.

## Flagged judgment calls (owner attention)

1. **M1/M2 — the materiality line.** Recommendation: re-review the ~7 MATERIAL set, currency-refresh the rest, borderline→MATERIAL. Alternative: treat *all* as MATERIAL (maximally conservative, but ~21 genuine re-reviews for a narrow Person-Mode delta is disproportionate and invites fatigue-stamping — the failure mode dressed as rigor).
2. **M4 — where the delta manifest lives** (commit-body convention vs a sidecar the check parses) and **who owns discharge** (proposed: the doctrine-change session). 
3. **Scope/branch** — this DR is separable from the ICCT PR; recommend it move to its own branch/PR on your word (current branch policy kept it here as a proposal).

## Revision history

- v1 (2026-07-21): initial proposal on owner directive.
