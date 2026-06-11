# DR-2026-06-10 — Synthesis Model Floor (rule #2 is a capability floor, not a brand pin)

**Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", ratifying Stage 4.3 plan §9 D-4.3-A).
**Authored:** `session_2026-06-10-stage4-3-ratification`
**Doctrine SHA at authorship:** `3da73bd` (`governance/mission-and-epistemics.md`)
**Relates to:** PI v10.14 standing rule #2 (best-practice-synthesis routing); `skills/multilingual-research_SKILL.md` and sibling skill headers (model pins); Stage 4.3 execution plan §4 Pass 2.

---

## Context

PI standing rule #2 states: "Sonnet does NOT write `best_practice_synthesis` — only Opus." The skill headers concur, pinning specific model strings ("Sonnet 4.6 (search) · Opus 4.6 (best_practice_synthesis)"). These were authored when Opus was the most capable model available to the project.

Stage 4.3 (Phase E synthesis) is now executed under **Claude Fable 5**, a Mythos-class model that sits *above* Opus in capability. Read literally, rule #2's brand wording neither authorizes nor forbids a model more capable than Opus — it names "Opus" because, at authoring time, Opus *was* the capability ceiling. Executing 4.3 requires resolving this so synthesis is not blocked on a wording artifact.

## Decision

1. **Rule #2 is a capability floor, expressed as "Opus-class or above."** Any model at or above Opus's synthesis capability may write `best_practice_synthesis`. Claude Fable 5 (Mythos-class, above Opus) satisfies the floor.
2. **The facts/judgment split is unchanged.** The restriction continues to mean that the high-judgment synthesis step is reserved for the most capable tier; it never meant "the literal string *Opus*." Evidence inventories, reasoning-doc drafting, per-population logging, and all Pass-1 facts work remain unrestricted by model tier.
3. **PI clarification queued, not applied here.** A one-line rule-#2 clarification is queued in `decisions/PI-update-needed.md` for v10.15 (owner-paste; not API-writable). The repo-side record is this DR.
4. **Skill model-pins to be swept.** The stale "Sonnet 4.6 / Opus 4.6" header strings in the four protocol skills are corrected to "Opus-class or above" as a caller-sweep follow-up (Stage 4.3 plan G4c); tracked, not done in this DR.

## Rationale

The rule's purpose is **judgment quality**, not brand identity. Pinning synthesis to a now-superseded model name inverts the rule's intent: it would forbid the *more* capable model from doing the work the rule reserves for the *most* capable model. A capability-floor reading preserves the rule's protective function — keeping the high-stakes judgment step at the top tier — while tracking the model lineup as it advances.

## Consequences

- Stage 4.3 Pass-2 synthesis (E.2e–E.2g, cell-state and convergence authoring) may proceed under Fable 5 or any future Opus-or-above model.
- No change to the verification gates (rules #7/#8/#9/#10) — those bind regardless of model tier and remain the dominant cost and the real safeguard.
- `references/skill-registry.md` records the model-pin reconciliation when G4c lands.

## Verification

This DR records an owner ratification; it makes no DB or evidence claim. Compliance with rule #11 is the attestation `attestations/decisions_DR-2026-06-10-synthesis-model-floor.json`.
