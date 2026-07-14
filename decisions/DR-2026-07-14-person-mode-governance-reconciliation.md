# DR-2026-07-14: Person Mode reconciliation — completing the governance-file sweep the prior correction under-scoped

- Status: **APPLIED (governance-only pass) — owner-directed** ("Governance-only first"). Completes the canonical-governance reconciliation of the Person Mode correction that `DR-2026-07-13-person-mode-functional-capacity-not-population-range.md` began but under-scoped. Skills, locked `project-standards.md` RULEs, `armature_v4.md`, and reference/pilot artifacts are deferred to a tracked second pass. The doctrine-SHA identity issue is investigated below and left for an owner decision, not enacted.
- Date: 2026-07-14
- Prepared by: Claude, after an adversarial Fable-5 max-effort audit (owner-requested, the antagonist pass of the agonist–antagonist methodology) found the prior correction materially incomplete: it claimed "three canonical spots" / "both canonical files corrected atomically," but the rejected "within the range" doctrine survived in 10+ canonical and forward-looking locations — including inside the two files the prior commit edited. Ten findings were confirmed by independent fresh-context skeptics.
- Affects (applied here): `governance/mission-and-epistemics.md` (§"orthogonal axes" line 107 — **the doctrine-SHA anchor; second re-baseline `8a5a717` → `373255e`**), `governance/evidence-methodology.md` (§1.6 line 81 — **the canonical home of decision D-D**; §3.3 item 6 line 272), `governance/evidence-architecture.md` (§8.1 line 157, §8.4 line 163), `governance/co1-operational.md` (line 140). Q12 pin sweep re-run `8a5a717` → `373255e` (same 5 files).
- Related: supersedes the completeness claim of `DR-2026-07-13-person-mode-functional-capacity-not-population-range.md`; `workplan/ratification-execution-register-2026-07-13.md`; the Fable-5 audit run `wf_90cef0a9-934`.

## Why this was needed — the prior correction's blast radius was undercounted

The prior DR corrected exactly three spots (mission commitment-4 cell; evidence-architecture.md §3 cell + §5 bullet) and asserted that was the full canonical scope. The audit proved otherwise. Most damning: the effacing framing survived **inside the two files the prior commit edited**, and in the **canonical home of decision D-D** (`evidence-methodology.md` §1.6), which — by `evidence-architecture.md`'s own precedence clause (line 4, "the cited source governs until reconciled by DR") — *governs*. The §3 G4 asymmetry principle explicitly claims to be "the already-ratified content of §1.6 plus co1-operational.md's Person-scale rule," yet both of those still stated the opposite. So the corrected doctrine was, until this DR, the minority position in the authoritative text and formally subordinate to an uncorrected source it cited.

## What was corrected (governance-only, this pass)

Each edit removes the bounding claim and preserves the correct machinery (Person-scale governing evidence is assessment/clinical-reasoning, not parameter-value-ranking; Person Mode stores no determinations; population evidence conditions the *process*). All align to the ratified wording: the individual's own functional needs, **informed by but not bounded by** a related disability population, a resolved value **may fall outside** the range.

1. `mission-and-epistemics.md` §"orthogonal axes" (107): "process-resolution *within* the established range" → "resolution of the individual's own functional needs … the population range informs the assessment but does not bound the answer, which may fall outside it (commitment 4)." Removes the doctrine-anchor file's self-contradiction with its own commitment 4.
2. `evidence-methodology.md` §1.6 (81): the canonical D-D statement, "OT process-resolution *within* the Population-scale range" → informed-by-not-bounded-by wording. This is the load-bearing fix — it is the source the corrected architecture text cites.
3. `evidence-methodology.md` §3.3 item 6 (272): "resolves the individual's position within the range" → "resolves the individual's own functional needs — informed by, but not bounded by, the range."
4. `evidence-architecture.md` §8.1 (157): "assessment resolves within the population range" → "scaffolded by — not bounded by — the population range (… the full 2440mm envelope, or more)."
5. `evidence-architecture.md` §8.4 (163): "resolves the value within the range" → "resolves the value; the population range informs the assessment but does not bound it."
6. `co1-operational.md` (140): the divergence voice convention, "OT assessment at Tier 2 resolves position within range" → informed-by-not-bounded-by wording.

VERIFIED-BY, this session: repo-wide grep of the four files for every bounding phrasing returns CLEAN; the G4 asymmetry principle's claim to "restate §1.6 + co1-operational" is now true (the sources agree).

## Doctrine-SHA re-baseline (second one — the cost the prior incomplete sweep forced)

Editing `mission-and-epistemics.md` again moved its blob hash `8a5a717` → `373255e`. This commit carries `[DOCTRINE: 373255e]` (the **new blob**, per the ci.yml / Stage-1.1 convention — done correctly this time), is exempt from the ci.yml doctrine-token gate (doctrine-self-modification, `ci.yml:85`), and the Q12 pins were re-swept `8a5a717` → `373255e`.

## Doctrine-SHA identity — investigation (per owner "investigate further first"; NOT enacted)

The audit flagged that `3fb2882` is not a blob hash. Confirmed by direct git archaeology this session:

- `git cat-file -t 3fb2882` → **commit** ("governance: reconcile evidence hierarchy … 2026-06-09").
- The doctrine-SHA convention is the **blob hash** of `mission-and-epistemics.md` (`ci.yml`: `git rev-parse HEAD:governance/mission-and-epistemics.md`; Stage 1.1 precedent `sessions/session_2026-06-11-artifacts/1.1-doctrine-revision-summary.md:5`).
- Blob history: `61c7f95` → (commit `3fb2882`) `3da73bd` → (commit `92122f2`) `dbd26e4` → (commit `1147384`) `e508657` → (commit `32f3c49`) `8a5a717` → (this DR) `373255e`.
- The drift: commit `3fb2882` *produced* blob `3da73bd`, and the `[DOCTRINE: 3da73bd]` token era was correct. Beginning at `92122f2` (the ratification-execution session), commits switched to stamping the **commit sha `3fb2882`** as the token while the live blob had moved on (`dbd26e4`, then `e508657`). So the entire `[DOCTRINE: 3fb2882]` era (through this session's own earlier commits and the separately-merged PR #7 commits `955ad60`/`3c1a69f`) carries a value that is neither the commit's own blob nor the current blob. It went uncaught because the ci.yml token gate is `push`-only on `main` and Actions enforcement is not restored (register Q15).

**Proposal for the owner (not enacted here):** standardize on blob-hash as the single convention (already what ci.yml enforces); add a forward-only register note recording that `3fb2882` is the 2026-06-09 reconciliation *commit*, that the intervening blobs were `dbd26e4`/`e508657`, and that current is `373255e`; keep all `[DOCTRINE: 3fb2882]`-era commit tokens and attestation `doctrine_sha` values immutable (forward-only), annotated as commit-sha-era artifacts. No historical record is rewritten. Awaiting the owner's decision before enacting.

## Integrity-record correction

The prior DR's `Affects` line described the anchor edit as "held" — stale plan-stage text; the anchor edit was in fact applied in that same commit. Corrected in `DR-2026-07-13-person-mode-functional-capacity-not-population-range.md` (a living decision doc) with a pointer to this DR. The prior *attestation* carries the same stale "held" reason under a CLEAN verdict; because attestations are forward-only/immutable, it is **not** edited — it is recorded here as a known defect, to be handled by the forward-only correction mechanism together with the SHA-identity decision above.

## Deferred to a tracked second pass (owner-directed scope split)

Not touched this pass; the rejected framing still lives in these **forward-looking** surfaces and will regenerate/enforce it until fixed:
- Skills: `guidebook-auditor_SKILL.md:170`, `voice-style_SKILL.md:218/224`, `item-specification-writer_SKILL.md:113`.
- Locked Core Doctrine RULEs: `references/project-standards.md:14` (verbatim old sentence), `:202` (handoff-flag template), `:170`.
- `armature_v4.md` §4.6 (the handoff definition the corrected §5 bullet cites — currently divergent).
- Reference/pilot artifacts: `references/bpc-scope-review.md:202`, `references/website/schema/unified-data-schema.md:57`, `scripts/generate/pilot_renderings.py` + generated HTML, `scripts/db/seed_e08_pilot.py:57/92`, historical `data/decisions/decision_register.yaml` rows (forward-only, left as-is).

## What would ratify this

Owner confirms (a) the corrected governance wording; (b) the deferred second-pass scope; (c) the doctrine-SHA convention proposal above (or directs otherwise). This pass makes the canonical governance internally consistent on the owner's most-important principle; the second pass stops the forward-looking surfaces from re-seeding the rejected framing.
