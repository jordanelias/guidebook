# DR-2026-07-13: Person Mode is the individual's own functional capacity — not a position on a population range

- Status: **APPLIED — owner-directed correction of the project's most-important principle. Both canonical files corrected atomically in one commit: `governance/evidence-architecture.md` §3 + §5, and `governance/mission-and-epistemics.md` commitment 4 (the doctrine-SHA anchor). CI-safety of the anchor edit verified before applying (see "Cascade — verified CI-safe"). The doctrine-SHA re-baseline is enacted; the Q12 pin sweep is the immediate follow-up.**
- Date: 2026-07-13
- Prepared by: Claude, on the owner's directive. The owner has stated this correction repeatedly ("I have been trying to explain this for months") and framed the existing wording as **"disingenuous and effacing while ignoring comorbidities and individual-specific matters."** This DR records the correction, its exact wording, and its blast radius.
- Affects: `governance/mission-and-epistemics.md` commitment 4 table (doctrine-SHA anchor — held); `governance/evidence-architecture.md` §3 mode table + §5 scale-tagging bullet (applied); `scripts/generate/pilot_renderings.py` OT-role string + its generated `working/pilot/pilot-renderings.html` (follow-up, flagged below); `data/decisions/decision_register.yaml` seeded records (historical, left as-is — see item 5).
- Related: `workplan/ratification-execution-register-2026-07-13.md` (new queue item); queue item Q12 (doctrine-SHA pin sweep — this correction, when applied to `mission-and-epistemics.md`, is exactly the doctrine commit Q12 is waiting on).

## The owner's articulation of the full ladder (verbatim, 2026-07-13)

The correction is anchored in the owner's own statement of all three modes, recorded here as the authoritative articulation:

- **Universal design** — "tries to make something as available as reasonably possible for all persons constituting a disability population."
- **Population-specific** (Population Mode) — "tailors itself to a range of considerations specific to a disability population."
- **Person-specific** (Person Mode) — "is about the individual's specific functional needs, and the design answers for those needs **may be informed by a related disability population**."

The load-bearing phrase for this DR is the last one: at Person Mode the population is *informing input to the assessment*, and it is "a **related**" population — the individual need not cleanly belong to it. The answer is driven by the individual's specific functional needs, not read off a population range. (This DR corrects Person Mode. Whether the owner's Universal-mode phrasing — "as available as reasonably possible" — should also revise the current doctrine, which equates Universal Mode with code compliance / "the floor, not an aspiration" per `mission-and-epistemics.md` commitment 5, is flagged as an open question at the end, not decided here.)

## The correction

**Old framing (the error).** Across three canonical spots, the *Resolution* of Person Mode is stated as:

> "OT assessment resolves position **within the Population-Mode range**."

and, in `evidence-architecture.md` §5:

> "Person Mode … is process-resolution **within the Population range**."

**Why it is wrong.** Person-specific / Person Mode is the **individual's own functional capacity** — unique to their specific circumstances, capabilities, and impairments, including **comorbidities and presentations that do not classify into any single disability population**. At this stratum the person is *no longer* treated as a member of a disability population, because that is precisely the level at which population scaffolding stops describing anyone. Framing the person's resolved answer as a *position on a population-derived range* is effacing: it subordinates the individual to the population abstraction and silently assumes their answer is bounded by, and interpolated within, a range built for a population they may not cleanly belong to.

**Why the doctrine already agrees — this corrects an internal contradiction, not a settled position.** The "within the range" wording contradicts the document's own foundations, which already state the corrected view:

- `mission-and-epistemics.md` **commitment 1**: *"Population codes are organizing scaffolding, not a description of any individual within the population. **Co-occurring conditions are the norm, not the exception.**"*
- `mission-and-epistemics.md` **commitment 7**: *"Population-level specifications … are necessary but insufficient. Person-Mode co-design … resolves the individual case."*
- `evidence-architecture.md` §3 **asymmetry principle** (already ratified, DR-gated G4): *"at Person Mode, the person themselves … with published evidence **conditioning the assessment process, never overriding the assessed answer** … no population-level source — including population-grain Co-1 — overrides an individual's assessed position."*

The asymmetry principle says the population range **conditions the assessment process** and never bounds the answer. The *Resolution* cells say the answer **is a position within the range**. Both cannot hold. This DR resolves the contradiction in favor of the axiom (and of commitments 1 and 7).

## Corrected wording

**`mission-and-epistemics.md` commitment 4 table — Person Mode / Resolution cell (APPLIED):**

> The individual's own specific functional needs — their circumstances, capabilities, impairments, and comorbidities. OT co-design resolves the individual case; the design answers may be informed by a related disability population, but that population neither bounds nor defines the person.

**`evidence-architecture.md` §3 mode table — Person Mode / Resolution cell (APPLIED):**

> OT co-design resolves the individual's own specific functional needs — their circumstances, capabilities, impairments, and comorbidities; the design answers may be informed by a related disability population, but that population does not bound the answer, which may fall outside any population range.

**`evidence-architecture.md` §5 scale-tagging bullet (APPLIED):**

> Person Mode produces no stored determinations at all: the assessed answer addresses the individual's own specific functional needs — their circumstances, capabilities, impairments, and comorbidities — and may be *informed by* a related disability population without being *bounded by* it (§3); a resolved value may fall outside any population range, and comorbid or hard-to-classify presentations routinely require exactly that. What the guidebook stores for Person Mode is the *handoff* — the functional parameter driving assessment and the population-range scaffold the assessment starts from (`armature_v4.md` §4.6 "Mode S handoff" — vocabulary normalized to "Person-Mode handoff" per §7).

The correct machinery is preserved unchanged: Person Mode still stores **no determinations**, only the **handoff**; population evidence still **conditions the process**; and the anti-laundering scale-tagging in §5 is untouched. The only change is removing the claim that the person's answer lives *inside* the population range.

## Cascade — verified CI-safe before applying the anchor edit

The doctrine SHA is the **blob hash of `governance/mission-and-epistemics.md`** (`ci.yml` computes `EXPECTED=$(git rev-parse "HEAD:governance/mission-and-epistemics.md" | cut -c1-7)`), so editing the file changes the SHA from `3fb2882` to a new value. Before applying, each gate that could turn red was checked:

1. **Doctrine-token gate (`ci.yml` job `doctrine`) — EXEMPT.** Lines 84–88 explicitly exempt any commit that touches `governance/mission-and-epistemics.md`: *"Doctrine commit -- token exempt. Re-attestation required within RE_ATTESTATION_WINDOW commits."* The chicken-and-egg (a doctrine-self-modifying commit cannot reference its own future blob hash) is anticipated in the workflow. This commit carries the prior token `[DOCTRINE: 3fb2882]` — the doctrine state the change was reasoned under, the same pattern by which `3fb2882` was itself created — and the attestation's `doctrine_sha` matches it (adherence check 2 compares attestation ↔ commit token, both `3fb2882`).
2. **A13 doctrine recheck (`ci.yml` job `governance`, `doctrine_recheck.py --cross-ref`) — SAFE.** In `--cross-ref` mode the script runs only passes 2.2 (snapshot build) and 2.3 (`check_cross_references`); the snapshot-**drift** comparison against a stored prior snapshot (2.4) runs only in non-`--cross-ref` scheduled rechecks. So the edit is not diffed against a frozen doctrine hash here. No cross-reference was added or broken (§3, §7, `armature_v4.md` §4.6 all pre-existing).
3. **Q12 pin sweep — follow-up, not a gate.** The pinned SHA in `schemas/directness.py`, `tier_derivation.py`, `evidence_state.py`, `skills/multilingual-research_SKILL.md`, `workplan/phase-e-execution-plan-v1.md`, plus `regenerate_vetting_surface.py` blurbs, `index.html:725`, and `generate_parts.py`'s legend now read the prior value. No CI check validates these pins against the current doctrine blob, so drift does not turn CI red. Q12's own note ("update after the doctrine commit lands") confirms the intended order: **doctrine commit first, pins follow** — this commit is that doctrine commit; the pin sweep is the immediate next step.
4. **Re-attestation window (adherence check 7)** re-baselines to the new SHA; immediately after the bump `commits-since = 0`, so nothing fails on landing, but the window clock restarts for all synthesis artifacts (future work re-attests against the new value).

Because every gate is either exempt, drift-free in the mode CI runs, or ungated, the anchor edit is applied in the same atomic commit as the `evidence-architecture.md` correction — a split state (origin still effacing, downstream corrected) is not acceptable for the project's most-important principle.

## What is deliberately NOT changed

5. **`data/decisions/decision_register.yaml` seeded records** (DEC rows quoting "OT assessment resolves position within Tier 1 range") are the project's historical decision log. Per the same forward-only, append-only convention that governs migrations and attestations (and the Q23 DR's item 2), historical records are not retroactively rewritten — they record what was decided at the time. The correction is carried forward in the governance docs, not backdated into the log.
6. **`working/pilot/pilot-renderings.html`** and its generator string are a pilot artifact, not canonical doctrine. The generator's OT-role line already carries the correct half ("conditions the assessment process, never the assessed answer") but keeps "within the Population-Mode range." Fixing it requires editing `scripts/generate/pilot_renderings.py` **and** regenerating the HTML in the same step (determinism). Flagged as a follow-up so the doctrine correction lands cleanly without dragging a renderer regeneration into this commit.

## Open items and what would ratify this

Applied and pending owner confirmation on:

1. **Wording** — that the corrected cells say what the owner has been conveying: Person Mode is the individual's own specific functional needs (comorbidities included), informed by but not bounded by a related disability population. A single revert restores the prior text if any phrasing is off.
2. **Q12 pin sweep** — the immediate follow-up now that the doctrine SHA is re-baselined (pinned SHA in `schemas/directness.py`, `tier_derivation.py`, `evidence_state.py`, `skills/multilingual-research_SKILL.md`, `workplan/phase-e-execution-plan-v1.md`, plus the `regenerate_vetting_surface.py` / `index.html` / `generate_parts.py` references). Not a CI gate, but real drift to close.
3. **Follow-up artifacts** — `scripts/generate/pilot_renderings.py` OT-role string + regenerated `working/pilot/pilot-renderings.html` (item 6 above).
4. **OPEN — Universal / Population reconciliation.** The owner's Universal-mode phrasing ("as available as reasonably possible for all persons constituting a disability population") reads more aspirational than the current doctrine's commitment 5 ("Universal design is co-extensive with code compliance — the floor, not an aspiration"). This DR did **not** touch Universal or Population definitions; whether the owner's articulation should revise them is a separate question with its own blast radius, flagged here, not decided.
5. **PR placement** — this doctrine change currently rides PR #6 ("follow-up cleanup"). If the owner prefers, the two governance files + this DR + attestation are trivially separable to a dedicated doctrine PR.
