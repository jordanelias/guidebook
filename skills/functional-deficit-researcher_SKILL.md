---
name: functional-deficit-researcher
description: >
  Bottom-up OT intervention research by functional deficit. Retrieves OT literature organized
  by ICF activity code + functional constraint + environment context, then categorizes findings
  into the guidebook's population framework. Complements multilingual-research (top-down) —
  does not replace it. ALWAYS use when: a slug's BPC has ≥2 THIN flags, item-specification-writer
  reports insufficient evidence for a spatial parameter, connection-scout identifies a cross-population
  gap that top-down search didn't fill, or user requests explicitly. Trigger on: "bottom-up search",
  "functional deficit", "OT intervention search", "what does the OT literature say about [specific
  functional task]", "search by function not population", "ICF search". CHECK before / LOG after
  every run. Runs AFTER multilingual-research top-down pass is COMPLETE for target slugs.
---

**Model:** Sonnet 4.6 (search, scenario execution) · Opus 4.6 (synthesis, NOVEL/REFINES classification)
**Opus routing:** Sonnet runs scenarios → Opus synthesizes findings into BPC.
**Practical constraint:** No programmatic Opus path from claude.ai artifact proxy. Opus requires model picker set to Opus.  
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API  
**Methodology:** `/mnt/user-data/outputs/methodology-functional-deficit-research-2026-03-26.md`  
**Every source confirmed real. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

---

## 1. Concept

OT clinical literature is organized by functional deficit — a finer grain than the guidebook's population codes. Top-down search (population → slug → evidence) misses intervention studies indexed by specific functional tasks. This skill works in reverse: functional deficit → OT intervention → spatial/environmental requirement → population code assignment → BPC integration.

---

## 2. Search Unit: Functional Scenario

The search unit is a **functional scenario** — not a bare ICF code.

Format: `{ICF-d code} + {functional constraint} → {environment context}`

Example: `d420 + hemiplegia → bathroom` searches for hemiplegic toilet transfer techniques and extracts spatial parameters (lateral clearance, grab bar configuration).

### 2.1 Scoped ICF Activity Codes

Only ICF-d (Activities and Participation) codes with built-environment spatial dependency are in scope. Filter: **can an architect specify something for this activity?**

**Tier A — High spatial dependency (always in scope):**

| ICF | Activity | Spatial nexus |
|---|---|---|
| d410 | Changing basic body position | Floor space, grab bars, surface height, transfer clearances |
| d420 | Transferring oneself | Transfer geometry, fixture adjacency, grab bar config |
| d440 | Fine hand use | Control type, reach envelope, mounting height, operating force |
| d445 | Hand and arm use | Counter depth, shelf height, hardware, reach range |
| d450 | Walking | Corridor width, gradient, surface, rest points |
| d455 | Moving around | Turning radii, thresholds, floor surface |
| d460 | Moving around in different locations | Wayfinding, level changes, transitions |
| d465 | Moving around using equipment | Clear widths, charging/storage, turning space |
| d470 | Using transportation | Entrance approach, drop-off, parking adjacency |
| d510 | Washing oneself | Shower/bath geometry, seat, controls reach, drainage |
| d520 | Caring for body parts | Mirror, basin clearance, outlet placement |
| d530 | Toileting | WC clearances, grab bars, privacy, bidet |
| d540 | Dressing | Bench/seat, closet reach, lighting |
| d550 | Eating | Table clearance, serving reach, seating stability |
| d620 | Acquisition of goods/services | Door width, counter height, queuing, display reach |
| d630 | Preparing meals | Worktop height/depth, cooktop clearance, appliance reach, knee space |
| d640 | Doing housework | Storage reach, floor access, laundry ergonomics |

**Tier B — Moderate spatial dependency (in scope where specified):**

d230 (daily routine — spatial sequencing), d310–d329 (receiving communication — acoustics, visual alerts, signage), d330–d349 (producing communication — intercom, quiet rooms), d475 (driving — parking, vehicle-building transition), d570 (health management — medication storage, emergency alert, lighting), d610 (acquiring a place to live — adaptability, DAR), d650 (caring for household objects — storage, maintenance reach), d660 (assisting others — carer circulation, dual-occupancy), d710–d729 (interpersonal — social space, retreat, sensory zoning), d910–d920 (community/recreation — common areas, outdoor).

**Out of scope:** d110–d199 (learning — except wayfinding), d240 (stress — except retreat space under NDV/MH), d810–d899 (education/work beyond common areas).

---

## 3. Pre-Run (mandatory)

1. **Confirm top-down baseline exists.** Target slug(s) must have a COMPLETE or near-COMPLETE BPC entry from `multilingual-research`. If not → stop; run top-down first.

2. **Select functional scenarios.** Intersect:
   - Gap register OPEN items and BPC THIN flags for target environment context
   - ICF codes from §2.1 that map to that environment context
   - Functional constraints relevant to the slug's population codes

3. **Cap:** ≤12 functional scenarios per session.

4. **Load Keyword Compendium** ICF functional scenario terms (when available; generate inline if Part 3 extension not yet done — flag as INLINE-GENERATED).

5. **Load existing BPC entry** for target slug(s) — this is the baseline against which `specification_delta` is assessed.

---

## 4. Search Sequence

**Step 1 — OT intervention databases (primary)**

For each functional scenario, search:

| Database | Filter |
|---|---|
| OTseeker | Intervention studies with environmental modification outcomes |
| PubMed | MeSH: "Self-Help Devices" OR "Environmental Design" OR "Home Modification" + ICF activity term |
| CINAHL | OT subject heading + functional scenario terms |

**Spatial filter (mandatory):** Does the study describe a spatial dimension, clearance, fixture specification, layout recommendation, or environmental modification that an architect could implement? YES → extract. NO → discard.

**Step 2 — OT practice guidelines and home modification resources**

| Source | Target |
|---|---|
| AOTA home modification resources | US practice guidelines for functional scenario |
| RCOT / RCOTSS | UK — Housing Adaptations Without Delay; GenHOME |
| CAOT | Canadian OT practice resources |
| OT Australia / Home Mod Clearinghouse (UNSW) | Australian home modification evidence |
| DVE (DE), EVS (CH) | German-language OT practice resources |

Priority: home modification guides > general CPGs. These describe specific adaptations with spatial dimensions.

**Step 3 — Assistive technology databases**

| Database | When |
|---|---|
| REHADAT (DE) | All runs; especially OFS/AT scenarios |
| AbleData / ATwiki (US) | All runs |
| AT databases by jurisdiction | When scenario involves device with spatial envelope (hoist, stair lift, standing frame) |

Target: not the device itself — the **spatial envelope** the device requires (clear floor zone, structural reinforcement, power supply location, storage).

**Step 4 — Cross-language targeted check**

For any finding with a specific spatial specification: check whether the same specification appears in non-English OT literature. Targeted, not a full 14-language sweep.

Priority languages by OT tradition strength:
- Home modification: SE, NO, DK, FI (Nordic model), AU, UK
- Rehabilitation engineering: DE, CH, JP
- Aging-in-place: JP, KR, DE

**Diminishing-return gate:** If 3 consecutive scenarios in the same environment context yield no new spatial specifications beyond existing BPC content → stop that environment context, move to next.

### Checkpoint (after each scenario):
```
CHECKPOINT [YYYY-MM-DD HH:MM] — scenario: {scenario} — sources found: {N} — novel: {N} — refines: {N} — contradicts: {N}
```

---

## 5. Extraction Template

For each finding that passes the spatial filter:

```yaml
scenario: "{ICF code} + {functional constraint} → {environment context}"
source: "{author, year, title, journal/publisher}"
source_tier: "{evidence hierarchy tier}"
language: "{source language}"
jurisdiction: "{if jurisdiction-specific}"

spatial_findings:
  - parameter: "{what is specified}"
    value: "{dimension, range, or qualitative specification}"
    condition: "{when this applies — functional constraint}"
    confidence: "{HIGH | MODERATE | LOW}"

population_mapping:
  primary: "{population code}"
  secondary: ["{additional codes}"]
  cross_population_note: "{why secondary populations benefit}"

existing_bpc_match: "{slug — or NEW}"
specification_delta: "{NOVEL | CONFIRMS | REFINES | CONTRADICTS}"
```

### Extraction rules:
- ≤6 sources per scenario (prioritize by tier, then spatial specificity).
- CONFIRMS: 1-line log only, no full extraction.
- CONTRADICTS: full extraction + flag for `evidence-auditor`.
- LOW confidence (single small-N study): cannot enter BPC without corroboration. Hold in extraction log.

---

## 6. Categorization Protocol

### 6.1 Population Code Assignment

| Rule | Description |
|---|---|
| **Primary** | Population code whose defining functional profile most closely matches the functional deficit |
| **Secondary** | Population codes with partial functional overlap that benefit from same spatial specification |
| **Cross-pop flag** | Finding serves ≥3 codes → candidate for `connection-scout` internal mode; potential Tier 0 provision |
| **No-code** | Deficit doesn't map to any existing code → log as taxonomy gap; do not force-fit |

### 6.2 BPC Integration

| `specification_delta` | Action |
|---|---|
| CONFIRMS | 1-line append to `### Consensus findings`. No further action. |
| REFINES | Full append to BPC. Feed to `item-specification-writer` as update brief. |
| NOVEL | Append to `### Bottom-up findings` subsection. Feed to `item-specification-writer` as new spec candidate. |
| CONTRADICTS | Append with flag. Route to `evidence-auditor` before BPC integration. |
| NEW (no slug) | Propose new slug → user approval → `research-log-manager`. |

### 6.3 Tier 0 Escalation

Same spatial specification from ≥3 functional scenarios across ≥2 population codes, no conflict with any population-specific need → `TIER-0-CANDIDATE`. These are universal design provisions where bottom-up evidence converges regardless of the originating deficit.

---

## 7. Post-Run (mandatory)

1. **Write findings to BPC** — GET `references/best-practices-compendium.md` + SHA. Append to relevant slug(s) under `### Bottom-up findings`. PUT back. Commit: `functional-deficit-researcher: append bottom-up findings [{YYYY-MM-DD HH:MM}]`

2. **Update search-log** — GET `references/search-log.md` + SHA. Update relevant slug entry `functional_deficit_pass` block. PUT back. Commit: `functional-deficit-researcher: update search-log [{YYYY-MM-DD HH:MM}]`

3. **Feed downstream:**
   - REFINES + NOVEL → briefing list for `item-specification-writer`
   - CONTRADICTS → queue for `evidence-auditor`
   - Cross-pop flags → queue for `connection-scout` internal mode
   - TIER-0-CANDIDATES → append to `gap_register.md` as P2 items

4. **Checkpoint summary:**
```
COMPLETE [YYYY-MM-DD HH:MM] — scenarios: {N} — novel: {N} — refines: {N} — contradicts: {N} — tier0 candidates: {N} — sources extracted: {N}
```

---

## 8. Token Rules

- ≤12 functional scenarios per session.
- ≤6 sources extracted per scenario.
- CONFIRMS = 1 line. No full extraction.
- Diminishing-return gate: 3 consecutive no-yield → stop environment context.
- Checkpoint per scenario: 1–2 lines.
- Do not re-run a scenario already marked COMPLETE in search-log `functional_deficit_pass`.

---

## 9. Priority Targets (confirmed first-run batch)

| Environment | Scenario | Rationale |
|---|---|---|
| Bathroom | d420 + hemiplegia → WC transfer | Large OT base; lateral clearance by transfer side |
| Bathroom | d510 + seated → shower | Shower seat, controls reach, spray direction |
| Bathroom | d530 + bilateral UPL → toileting | Bidet/wash-dry spatial gap |
| Kitchen | d630 + seated → meal prep | Worktop, knee clearance, appliance reach |
| Kitchen | d440 + unilateral UPL → food prep | One-handed techniques; tap type, stabilization |
| Bedroom | d540 + trunk instability → dressing | Dressing bench, closet geometry |
| Entrance | d465 + powered wheelchair → threshold | Threshold transition, gradient, turning at door |
| General | d450 + fatigue → rest points | Rest intervals, alcove dimensions; spans MOB/OFS/PAIN/DEM |

---

## 10. Dependencies

| Dependency | Status | Required before first run |
|---|---|---|
| ≥1 slug with COMPLETE top-down BPC | Near-complete (bathroom/kitchen backfill in progress) | YES |
| Keyword Compendium Part 3 ICF terms | NOT AVAILABLE — generate inline, flag INLINE-GENERATED | NO (workaround exists) |
| Search-log schema `functional_deficit_pass` block | NOT DONE — add on first LOG | YES (auto-extends on first run) |
| BPC schema `### Bottom-up findings` subsection | NOT DONE — add on first write | YES (auto-extends on first run) |
