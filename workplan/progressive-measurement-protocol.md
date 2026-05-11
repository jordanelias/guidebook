<!-- SUBORDINATE 2026-05-11 -->
> **SUBORDINATE PROTOCOL:** This document is the operating protocol for PI v10.8 standing rule #8 (Progressive Measurement Probe). It is NOT superseded by `audits/bpc-rewrite-workplan-2026-05-11.md`; it operates underneath that workplan as a sub-protocol. Remains in force until a future PI revision modifies rule #8.

---

# Progressive Measurement Probe (PMP) Protocol
**Status:** PROPOSED 2026-05-10. Pending decision record `DR-2026-05-10-progressive-measurement-protocol.md`.
**Companions:** `research-protocol-adversarial.md` (claim validation), `multilingual-search-remediation.md` (per-language adversarial).
**Reverses:** the v1 "±20% threshold test" dropped at adoption of adversarial v2 (DR-2026-05-09 §"What Was Dropped"). v1 was static; PMP is iterative with re-centering.

## Purpose

Test numerical specification values empirically. Walk the value from the BPC stating-point toward the more accessible end, re-center after each supported step, halt when evidence stops validating the new value. Output is the empirically-supported range, not a single point. The gap between the BPC value and the empirical ceiling/floor is the discovery the protocol exists to surface.

## Why v1 was wrong

DR-2026-05-09 dropped the threshold test on the rationale "requires dose-response data Claude doesn't have access to." That rationale conflated dose-response (clinical sensitivity per dose) with specification-value validation (does any peer-reviewed source validate this number for this population). Validation does not require dose-response data; it requires literature search at specific values. The static ±20% bracket failure was real — fixed bracket around a fixed center cannot map an empirical ceiling that lies outside it. The fix is iterative re-centering, not abandonment.

## When to invoke

For any item with a numerical specification (units of mm, s, NC, lux, °C, %, N, LRV points, ratio, count). Triggered:
- During BPC closure when a numerical spec is being asserted
- During audit phase when a previously-asserted spec is being re-evaluated
- During multilingual remediation when a target-language source cites the spec at a value different from the BPC

NOT triggered for qualitative specs (e.g., "user control is the primary design variable" — slug 2 sensory-room-user-control). Adversarial-research alone covers those.

## Invocation requires three inputs

1. **V₀** — BPC specification value in native units
2. **D** — accessibility direction (`up` if higher = more accessible; `down` if lower = more accessible)
3. **claim type** — `minimum` | `maximum` | `target` | `range_low` | `range_high`

D is a property of the spec, not a property of the search. Determine and log once per item; do not recompute mid-walk.

### D reference table (extend as items are added)

| Spec type | Direction | Rationale |
|---|---|---|
| Turning radius / clear floor space | up | larger radius accommodates more devices |
| Door clear width | up | wider passes more devices |
| Illuminance (lux) | up | brighter aids low-vision users (with glare-control caveat) |
| Contrast ratio (LRV difference) | up | higher contrast is more perceptible |
| Grab bar length | up | longer accommodates more grip positions |
| RT60 reverberation | down | lower aids speech intelligibility |
| NC noise criterion | down | lower aids hearing-impaired users |
| Door opening force (N) | down | lower force accommodates weaker grip |
| Threshold height | down | lower reduces trip/wheel-strike hazard |
| Ramp gradient | down | gentler is more accessible |
| HVAC dB(A) | down | quieter aids hearing access |
| NRC (acoustic absorption) | up | higher absorption reduces reverb |
| Anti-scald valve max temp | down | lower reduces burn risk |

For items combining multiple direction-claims (e.g., "between 700–900 mm"), run two probes — `range_low` walks D=down from lower bound, `range_high` walks D=up from upper bound.

## Algorithm

```
INPUTS: V₀, U, D, pop, claim_type
INIT:   V_curr ← V₀; phase ← "outer"; log ← []

# OUTER PHASE — proportional 20% steps
WHILE phase == "outer":
  V_test ← step_proportional(V_curr, 0.20, D)        # +20% if D=up; −20% if D=down
  hit_1  ← strict_search(V_test, pop, claim_type, query_form="primary")
  IF hit_1.passes_strict:
    log.append(probe_row(V_test, hit_1.refs, "outer-pass-1st"))
    V_curr ← V_test
    CONTINUE
  hit_2  ← strict_search(V_test, pop, claim_type, query_form="alt-phrasing")
  IF hit_2.passes_strict:
    log.append(probe_row(V_test, hit_2.refs, "outer-pass-2nd"))
    V_curr ← V_test
    CONTINUE
  # both failed — outer terminator
  log.append(probe_row(V_test, [], "outer-stop", search_query, search_query_alt))
  V_outer_floor ← V_curr        # last supported
  V_outer_fail  ← V_test        # first unsupported
  phase ← "refinement"

# REFINEMENT PHASE — linear δ steps, bisection toward boundary
δ ← δ_min(U, item_override)
WHILE distance(V_outer_fail, V_outer_floor, D) > δ:
  V_test ← step_toward(V_outer_floor, V_outer_fail, δ, D)
  hit_1  ← strict_search(V_test, pop, claim_type, query_form="primary")
  IF hit_1.passes_strict:
    log.append(probe_row(V_test, hit_1.refs, "refinement-pass-1st"))
    V_outer_floor ← V_test
    CONTINUE
  hit_2  ← strict_search(V_test, pop, claim_type, query_form="alt-phrasing")
  IF hit_2.passes_strict:
    log.append(probe_row(V_test, hit_2.refs, "refinement-pass-2nd"))
    V_outer_floor ← V_test
    CONTINUE
  log.append(probe_row(V_test, [], "refinement-stop"))
  V_outer_fail ← V_test

# FINAL
V_empirical_ceiling ← V_outer_floor
gap_signed ← (V_empirical_ceiling − V₀) signed for D
log.append(probe_row(V_empirical_ceiling, [], "final", gap_signed))
```

`strict_search.passes_strict = True` iff at least one peer-reviewed source specifically validates value V_test for the target population AND the claim type — not merely mentions the topic. This is termination criterion (b): topic-evidence does not count as claim-evidence (PI standing rule #7).

`query_form="alt-phrasing"` is mandatory and must use independent terms — synonyms, alternate units, alternate population descriptors, alternate citation databases. The two-form rule is termination criterion (c): two genuinely different searches must both fail before declaring "no evidence."

## δ_min defaults (refinement minimum step)

| Unit | δ_min | Rationale |
|---|---|---|
| mm | 50 | finer than typical building tolerance |
| s (RT60) | 0.05 | half of perceptually-just-noticeable difference |
| NC integer | 1 | smallest meaningful unit |
| dB(A) | 1 | ditto |
| lux | max(10, 5% of V₀) | proportional at high values |
| °C | 0.5 | finer than thermal comfort variance |
| % (slope, NRC, contrast) | 0.5 | finer than building-tolerance |
| N (force) | 5 | finer than ISO 21542 step granularity |
| LRV points | 5 | smaller than the 30-pt accessibility threshold |

Per-item override stored on `items.pmp_delta_min`. Defaults must be revisited annually.

## Population/claim match — strict definition

A peer-reviewed source supports value V_test iff ALL of:
1. Source studies (or systematically reviews studies of) the target population
2. Source addresses the same claim type — minimum / maximum / target — not merely mentions the variable
3. Source specifies a value that is V_test ± δ_min(U) — not "approximately," not a range that includes V_test, not "at least" or "no more than" some boundary

Sources that fail condition 1 → grade `MISMATCH`, do not count toward passes_strict.
Sources that pass 1 but fail 2 → grade `PROXY`, do not count.
Sources that pass 1+2 but specify a range → grade `PARTIAL`, count as pass only if V_test is within the validated range.
Sources passing all three → grade `EXACT`, count as pass.

This grading is logged in `evidence_population_match` per the existing protocol — PMP does not introduce a new grading scheme, only stricter application.

## Integration with adversarial-research

Adversarial-research validates the claim ("RT60 should be ≤ 0.4s for autistic students"). PMP probes the value within the validated claim ("at what RT60 value does evidence stop supporting this claim?"). Both run for any numerical spec.

Order:
1. Run adversarial-research first. If named_dissenter is "NONE FOUND" with no qualified search trail OR confidence_interval is below 50%, do NOT run PMP — the underlying claim is unsupported, probing values is premature.
2. If adversarial passes, run PMP. The probe walk extends the audit trail; the empirical ceiling/floor populates `items.pmp_empirical_ceiling`.
3. If PMP finds the empirical ceiling far from V₀ (gap > 50% of V₀), reopen the gap on the original claim — the BPC value may be conservatively or aggressively miscentered.

## Integration with multilingual-search-remediation

PMP runs **once per item, EN by default**. Target-language probes are added only when:
- Adversarial-research per-language found cited values diverging from V₀ (e.g., "European RT60 norms specify 0.5s, not 0.4s" → run PMP also in DE/NL/SV/NO)
- Item domain has known non-EN-dominant research base (e.g., DE/NL/SV for housing; JA for visual contrast/LRV)

Without this scope rule, PMP fan-out is N items × 14 languages × ~6 walk steps = combinatorially ruinous. The rule forces target-language probes to be evidence-driven, not symmetric-by-default.

## DB schema

New table `spec_value_probes` and item-level columns. See migration `006_spec_value_probes.sql`.

Probe rows are append-only. Re-running a probe creates a new walk identified by `walk_id`; old walks remain for audit.

## Audit query

`scripts/audit/pmp_audit.py` (level 2). Flags:
- C1. Items with numerical specs lacking any walk in `spec_value_probes` → backlog
- C2. Walks with `phase='outer-pass-1st'` rows but no `phase='final'` → incomplete walk
- C3. `passes_strict=1` rows with NULL `ref_id` → ungrounded pass claim
- C4. Walks where empirical ceiling is identical to V₀ and outer phase had only 1 step → likely shallow probe, flag for re-run with stricter alt-phrasing
- C5. Walks where final gap > 200% of V₀ → flag for plausibility review

## Worked example — A-08 (HVAC Noise Control, NC-25 maximum, sensitive spaces)

- V₀ = 25 (NC scale)
- U = NC integer
- D = down (lower noise is more accessible)
- claim_type = maximum
- pop = "occupants of healthcare/educational sensitive spaces, hearing-impaired or autistic"

Outer walk (−20% per step):
- step 1: V_test = 20 → search "NC-20 noise criterion sensitive spaces hearing impaired" + alt phrasing → if both find at least one peer-reviewed source recommending ≤ NC-20 for this population, V_curr ← 20
- step 2: V_test = 16 → ditto
- step 3: V_test = 13 → ditto

Refinement (δ=1) once outer phase terminates. Output: V_empirical_floor and the gap from NC-25.

Hypothesis: empirical floor will sit between NC-15 and NC-20 (PTAR / WHO community noise guideline territory). If true, the BPC NC-25 is conservatively-centered relative to evidence — finding worth surfacing.

## What this won't fix

Same as adversarial-research:
- Cannot prevent fabrication of step-pass citations. Audit C3 and human spot-check are the safeguards.
- δ_min defaults are judgment calls. Wrong defaults produce false termination at the boundary.
- Two-failed-search alt-phrasing rule is bypassable by Claude using near-synonymous phrasings. Spot-check 1 walk per session (per audit query output).
- The reviewer is the truth-source. PMP makes shallow probing visible.

## Adoption checklist

- [ ] Owner sign-off
- [ ] Decide enforcement level (default: 2, audit query)
- [ ] Run migration 006_spec_value_probes.sql
- [ ] Add `skills/progressive-measurement_SKILL.md` (Stage B)
- [ ] PI v10.7 standing rule #8 invoking PMP for numerical specs (Stage B)
- [ ] First execution: slug 3 A-02 (NRC ≥0.85, D=up) and A-08 (NC-25, D=down)
- [ ] Backfill plan for prior numerically-specified BPC closures (estimate per Stage D)

## Related

- `decisions/DR-2026-05-10-progressive-measurement-protocol.md` — formal decision
- `workplan/research-protocol-adversarial.md` — companion protocol
- `decisions/DR-2026-05-09-adversarial-research-protocol.md` — the decision PMP partially supersedes
- `workplan/multilingual-search-remediation.md` — execution context
