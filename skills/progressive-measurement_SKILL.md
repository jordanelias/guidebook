---
name: progressive-measurement
title: Progressive Measurement Probe (PMP) Protocol
purpose: Map the empirically-supported range of a numerical specification value via iterative walk-up/walk-down with re-centering, surfacing the gap between the stated BPC value and the actual evidence boundary
status: active
adopted: 2026-05-10
decision_record: decisions/DR-2026-05-10-progressive-measurement-protocol.md
governs: All BPC items asserting a numerical specification (mm, s, NC, lux, °C, %, N, LRV points, ratio, count)
enforcement: Level 2 (audit query at scripts/audit/pmp_audit.py)
companion: adversarial-research (claim validation; PMP is value validation)
---

# Skill: Progressive Measurement Probe (PMP)

## When to invoke

Trigger this skill for ANY of:
- BPC closure where the closure asserts a specific numerical value (e.g., "RT60 ≤ 0.4s", "turning radius 1500 mm", "NC-25", "300 lux")
- Audit phase re-evaluation of a previously-closed numerical-spec item
- Multilingual remediation surfacing a target-language source citing a value different from the BPC value
- Adversarial-research closure with passing CI on a claim that contains a number — PMP probes the value within that claim

Do NOT invoke for:
- Qualitative claims (e.g., "user control is the primary design variable")
- Claims where adversarial-research returned `named_dissenter = "NONE FOUND"` with shallow search history — PMP probes within a validated claim, so the underlying claim must clear adversarial first
- Range claims where only one bound is in the BPC (run two walks instead, one per bound, with `claim_type` = `range_low` and `range_high`)

## What this skill does NOT solve

Read this first. Do not skip:
- Cannot prevent fabricated step-pass citations. Audit C3 (passes_strict=1 with NULL ref_id) flags ungrounded passes; human spot-check is the truth-source.
- Cannot calibrate δ_min defaults. Wrong defaults produce false termination at the boundary; defaults are revisited annually.
- Cannot make alt-phrasing genuinely independent. Claude can use near-synonymous phrasings that fail in correlated ways. Spot-check 1 walk per session is the mitigation.
- The reviewer is the truth-source. PMP makes shallow probing visible.

## Required inputs (per walk)

| Input | Source | Notes |
|---|---|---|
| V₀ | BPC text | original specification value, native units |
| U | item metadata | unit string (`mm`, `s`, `NC`, `lux`, `°C`, `%`, `N`, `LRV`, `dB(A)`, `NRC`, etc.) |
| D | items.pmp_direction | `up` if higher value = more accessible; `down` if lower = more accessible |
| pop | bpc_metadata.population | target population statement |
| claim_type | walker decision | `minimum` / `maximum` / `target` / `range_low` / `range_high` |
| δ_min | items.pmp_delta_min OR table default | refinement minimum step (see workplan §"δ_min defaults") |

D is a property of the spec. Determine once at item registration. Do NOT recompute mid-walk.

## Algorithm

Two phases — outer (proportional 20%) and refinement (linear δ_min).

```
V_curr ← V₀
phase  ← outer
walk_id ← uuid()
step_index ← 0

# OUTER
loop:
  V_test ← step_proportional(V_curr, 0.20, D)
  step_index += 1

  hit_1 ← strict_search(V_test, pop, claim_type, query_form="primary")
  if hit_1.passes_strict:
    log_row("outer-pass-1st", V_test, hit_1.refs)
    V_curr ← V_test
    continue

  hit_2 ← strict_search(V_test, pop, claim_type, query_form="alt-phrasing")
  if hit_2.passes_strict:
    log_row("outer-pass-2nd", V_test, hit_2.refs)
    V_curr ← V_test
    continue

  # both forms failed — outer terminator
  log_row("outer-stop", V_test, [])
  V_outer_floor ← V_curr     # last supported value
  V_outer_fail  ← V_test     # first unsupported
  break

phase ← refinement

# REFINEMENT (bisection toward boundary, step ≥ δ_min)
loop:
  if distance(V_outer_fail, V_outer_floor, D) ≤ δ_min:
    break
  V_test ← step_toward(V_outer_floor, V_outer_fail, δ_min, D)
  step_index += 1

  hit_1 ← strict_search(V_test, pop, claim_type, query_form="primary")
  if hit_1.passes_strict:
    log_row("refinement-pass-1st", V_test, hit_1.refs)
    V_outer_floor ← V_test
    continue

  hit_2 ← strict_search(V_test, pop, claim_type, query_form="alt-phrasing")
  if hit_2.passes_strict:
    log_row("refinement-pass-2nd", V_test, hit_2.refs)
    V_outer_floor ← V_test
    continue

  log_row("refinement-stop", V_test, [])
  V_outer_fail ← V_test

# FINAL
V_empirical_ceiling ← V_outer_floor
gap_signed ← signed_gap(V_empirical_ceiling, V₀, D)
log_row("final", V_empirical_ceiling, [], gap_signed)
update_item(item_code, pmp_empirical_ceiling = V_empirical_ceiling, pmp_gap_signed = gap_signed, pmp_last_walk_at = now())
```

## strict_search definition

`passes_strict = True` requires AT LEAST ONE peer-reviewed source that:
1. Studies (or systematically reviews studies of) the target population
2. Addresses the same `claim_type` (minimum/maximum/target/range)
3. Specifies a value within ±δ_min(U) of V_test — not "approximately," not a containing range, not a one-sided boundary

Implementation in this environment:
- Use `web_search` for general literature
- Use `PubMed` MCP if and only if the user has explicitly opted in for the session (per preferences `<mcp_connectors>`)
- Log query exactly as run, in `spec_value_probes.search_query`
- Cited refs go through `evidence_sources` + `source_slug_links` + `evidence_population_match` per existing protocol (no special path)

`query_form="alt-phrasing"` MUST use independently-chosen terms — synonyms, alternate units (mm vs cm; s vs ms; NC vs dB), alternate population descriptors (autistic / autism spectrum / ASD), alternate database emphasis (PubMed vs general web). Do NOT use minor variants of the primary query (e.g., adding/removing a stopword).

## Required DB writes (per walk)

Per step:
```sql
INSERT INTO spec_value_probes (
  probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit,
  direction, population, claim_type, step_index, phase, step_value,
  step_value_unit, search_query, search_query_alt, passes_strict,
  ref_id, notes, created_at, created_by_session
) VALUES (...);
```

Per cited source (in addition to the probe row):
```sql
-- existing protocol; PMP does not introduce a new path
INSERT INTO evidence_sources (...) ON CONFLICT DO UPDATE ...;
INSERT INTO source_slug_links (...) ON CONFLICT DO NOTHING;
INSERT INTO evidence_population_match (...);
```

After final row:
```sql
UPDATE items
SET pmp_empirical_ceiling = ?,
    pmp_gap_signed        = ?,
    pmp_last_walk_at      = ?
WHERE item_code = ?;
```

## Integration with adversarial-research

| Question | Skill | Output |
|---|---|---|
| Is the underlying claim valid for this population? | adversarial-research | named_dissenter, CI, falsification |
| At what value does the evidence stop validating the claim? | progressive-measurement | empirical_ceiling, gap_signed |

Order: adversarial-research first. PMP runs only when adversarial passes.

If PMP finds a gap > 50% of V₀, reopen the gap on the original claim — the BPC value may be miscentered (too conservative or too aggressive relative to evidence). Note in `gaps.notes` that PMP found the boundary far from V₀.

## Multilingual scope

PMP runs ONCE per item, in EN, by default. Add target-language probes only when:
- Adversarial-research per-language found cited values diverging from V₀ in target-language sources
- Item domain has known non-EN-dominant research base (DE/NL/SV for housing, JA for visual contrast/LRV, etc.)

Without this rule, fan-out is N items × 14 langs × ~6 walk steps. The rule forces target-language probes to be evidence-driven, not symmetric-by-default.

## Audit query

`scripts/audit/pmp_audit.py` (level 2). Flags:
- **C1.** Items with numerical specs lacking any `spec_value_probes` row → backlog
- **C2.** Walks with pass rows but no `phase='final'` row → incomplete walk
- **C3.** Rows with `passes_strict=1` but `ref_id` is NULL → ungrounded pass claim
- **C4.** Walks where empirical ceiling = V₀ AND outer phase had only 1 step → likely shallow probe; flag for re-run with stricter alt-phrasing
- **C5.** Walks where `pmp_gap_signed` > 200% of V₀ → flag for plausibility review

Run before session close:
```bash
python3 scripts/audit/pmp_audit.py
```

Exit 0 = clean. Exit 1 = deficient walks present.

## Detection question (mandatory before declaring a walk complete)

> **"At V_test, does the cited evidence specifically validate the value, or does it just speak to the topic?"**

If the answer is "speaks to the topic," the row's `passes_strict` MUST be 0, regardless of how many results the search returned. This is the topic-vs-claim conflation guard from PI standing rule #7, applied per-step.

## Worked example — A-08 HVAC Noise Control (NC-25 maximum)

- V₀ = 25, U = NC, D = down, claim_type = maximum, pop = "occupants of healthcare/educational sensitive spaces, hearing-impaired or autistic"
- δ_min = 1 (NC integer)
- Outer step 1: V_test = 25 × 0.8 = 20 → "NC-20 noise criterion sensitive spaces hearing impaired" + alt-phrasing in dB(A) terms
- Outer step 2 (if step 1 passes): V_test = 20 × 0.8 = 16 → ditto
- Outer step 3 (if step 2 passes): V_test = 16 × 0.8 = 13 → ditto
- Refinement: bisect between last-supported and first-unsupported, step ≥ 1
- Output: empirical floor (likely between NC-15 and NC-20 based on PTAR/WHO community noise guidelines — this is the prior, logged in advance per adversarial protocol)

## Spot-check schedule (human responsibility)

Per session: 1 random walk closed in this session. Ask Claude "trace this step-pass to primary data" and "would the alt-phrasing query you used really reach a different literature pocket?"

Per 10 sessions: audit `passes_strict` distribution; pick 3 outer-stop or refinement-stop rows and re-run with deliberately different phrasing — see if a value that was declared unsupported has support.

Per 50 sessions: external domain expert review of 5 closed walks; compare expert's empirical ceiling to PMP output.

## See also

- `decisions/DR-2026-05-10-progressive-measurement-protocol.md` — adoption record
- `workplan/progressive-measurement-protocol.md` — full protocol spec with worked examples
- `skills/adversarial-research_SKILL.md` — companion skill (claim validation)
- `workplan/multilingual-search-remediation.md` — execution context
- `scripts/migrations/006_spec_value_probes.sql` — schema migration
