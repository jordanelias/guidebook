---
name: sensory-coherence-checker
description: >
  Audit sensory environment consistency across room type matrices in the guidebook.
  Checks that acoustic, visual, thermal, and olfactory specifications do not contradict
  each other within or across room types, and that cross-population sensory conflicts
  are identified and resolved. ALWAYS use this skill when asked to: check sensory
  consistency, audit room matrices for sensory conflicts, verify that lighting specs
  don't conflict with acoustic specs, check thermal and ventilation coherence, or
  audit the sensory environment provisions across building types. Trigger on: "sensory
  coherence", "sensory consistency", "room matrix audit", "do the sensory specs
  conflict", "acoustic vs visual check", "thermal coherence", "sensory environment
  audit". Phase 5 skill — runs during QA on content-final matrices.
---

**Model:** Sonnet 4.6 — cross-domain judgment required.
**Input:** Room type matrices (Parts 5 and 6) + K-category items (Part 7) + Part 8 conflict resolutions
**Output:** Sensory coherence report + conflict register
**Chunk ceiling:** ≤10 room types per run.

---

## 1. Sensory Domains

| Domain | Key parameters | Typical spec locations |
|---|---|---|
| Acoustic | Background noise (dB), reverberation time (s), speech intelligibility (STI), sound insulation (dB) | K-items, room matrices, DEAF/NEU/NDV provisions |
| Visual | Illuminance (lux), colour temperature (K), glare control, LRV contrast (≥30), flicker rate | K-items, room matrices, VIS/DEM/NEU provisions |
| Thermal | Temperature range (°C), ventilation rate, humidity, radiant heat | K-items, room matrices, OFS/NEU provisions |
| Olfactory | Fragrance-free zones, ventilation adequacy, chemical sensitivity | F-02 (if retained), room matrices, NDV/SENS/OFS provisions |
| Tactile | Surface finish, texture contrast, temperature of contact surfaces | Floor/wall items, wayfinding items, VIS/DBL provisions |

---

## 2. Coherence Checks

### Within-room coherence
For each room type in the matrix:
- Do acoustic specs and thermal/ventilation specs conflict? (e.g., high ventilation rate for OFS vs. low background noise for DEAF)
- Do lighting specs and NDV sensory specs conflict? (e.g., high illuminance for VIS vs. low stimulation for NDV/SENS)
- Do thermal specs conflict across populations? (e.g., Uhthoff's phenomenon for NEU/MS vs. cold sensitivity for PAIN)
- Is the specified acoustic environment achievable given the specified ventilation and mechanical systems?

### Across-room coherence
- Do adjacent room types have incompatible sensory profiles? (e.g., quiet room next to high-noise activity space without adequate sound insulation)
- Do transition zones between sensory environments have gradual change provisions?
- Are sensory refuges/retreats accessible from high-stimulation spaces?

### Cross-population coherence
- For each room type: identify all population codes served
- For each population pair: check whether their sensory needs conflict
- For each conflict: verify Part 8 §8.4 has a documented resolution
- Unresolved conflicts → flag for Part 8 development

---

## 3. Known Conflict Patterns

| Conflict | Populations | Domain | Typical resolution |
|---|---|---|---|
| Illuminance level | VIS (high) vs NDV/SENS (low) | Visual | Zoned lighting; adjustable; task vs ambient |
| Background noise | DEAF (low) vs OFS/thermal (ventilation noise) | Acoustic | Low-noise HVAC; displacement ventilation |
| Temperature | NEU/MS Uhthoff's (cool) vs PAIN/fibro (warm) | Thermal | Zoned thermal; personal control; Tier 2 |
| Fragrance | NDV/SENS/OFS (zero) vs general (cleaning products) | Olfactory | Fragrance-free policy; ventilation schedule |
| Surface texture | VIS/DBL (tactile contrast) vs MOB/UPL (smooth for wheeling) | Tactile | Raised tactile at decision points only; smooth elsewhere |
| Acoustic treatment | DEAF (hard surfaces for visual cues/reflection) vs NEU/NDV (soft surfaces for absorption) | Acoustic | Zoned; absorptive ceiling + reflective lower wall |

---

## 4. Output Format

```markdown
## Sensory Coherence Report — [scope]
**Date:** YYYY-MM-DD HH:MM

### Summary
- Room types audited: [N]
- Within-room conflicts found: [N]
- Across-room conflicts found: [N]
- Cross-population conflicts found: [N]
- Resolved in Part 8: [N]
- Unresolved: [N]

### Conflict Register
| ID | Room/Scope | Domain | Populations | Conflict | Part 8 ref | Status |
|---|---|---|---|---|---|---|

Status: RESOLVED (Part 8 ref exists) · UNRESOLVED (needs Part 8 entry) · ZONED (spatial resolution) · TIER-2 (requires co-design)

### Recommendations
[Prioritised list of unresolved conflicts requiring Part 8 entries or specification revision]
```

---

## 5. Escalation Triggers

- >3 unresolved conflicts in a single room type → flag as SENSORY-OVERLOAD risk; escalate to workplan-orchestrator
- Any safety-critical sensory conflict (e.g., fire alarm audibility vs. acoustic treatment) → 🔴 immediate escalation
- Conflict between K-item spec and room matrix spec for same room type → 🔴 specification inconsistency

---

**Upstream dependency:**  — runs at Phase 2B–3 to produce conflict domain matrix and resolution evidence. This skill's §3 Known Conflict Patterns table should be updated from cross-population-conflict-mapper output before Phase 5 runs.

**Preceded by:** All Phase 3 writing complete · `evidence-marker` audit complete
**Feeds into:** Part 8 §8.4 development · `gap_register.md` (unresolved conflicts) · `cross-reference-resolver` (new Part 8 refs)
