---
name: functional-deficit-auditor
description: >
  Per-item audit of functional deficit framing — checks whether an item's claimed
  populations, ICF codes, mechanism of action, and threshold values are correctly
  scoped before research is commissioned or atoms are authored. Distinct from
  functional-deficit-researcher (FDR): FDA audits scope accuracy; FDR conducts research.
  FDA runs as Step 6 of item-audit-pipeline. Also invoked standalone when item scoping
  is questioned. Trigger on: "audit this item's populations", "is the functional framing
  correct", "should this population be here", "check the mechanism of action",
  "does this need FDR research".
  Decision: D-0147, 2026-05-05.
---

# Functional Deficit Auditor

**Model:** Sonnet 4.6 (extraction, coverage mapping) · Opus 4.6 (mechanism validity judgment
and FDR trigger decision — Steps 3b and 5 require Opus)
**Intake:** Single item spec (≤500 lines). Longer items → haiku-chunker first.
**Output target:** SQLite gaps table (AUDT for scope errors; RP for FDR triggers)
**Feeds INTO:** item-audit-pipeline Step 6 output; functional-deficit-researcher (FDR) via RP gaps

---

## Purpose and Scope

FDA asks: *Is the functional deficit framing of this item correct?*

It does NOT ask: *Is the evidence for this item sufficient?* (that is evidence-auditor)
It does NOT conduct research. (that is FDR)

FDA fires before FDR to ensure research is commissioned against the right populations,
mechanisms, and threshold values. A FDR run against an incorrectly scoped item produces
wasted research. FDA is the gate.

---

## Section 1 — ICF Tier A Reference (imported from FDR §2.1)

FDA uses FDR's spatial dependency tiers to check threshold-population linkage (Question 4)
and FDR trigger criteria (Question 6). These tiers classify *whether an architect can
specify something* for a given ICF activity.

**Tier A — High spatial dependency (always in FDA scope for threshold audit):**

| ICF | Activity |
|---|---|
| d410 | Changing basic body position |
| d420 | Transferring oneself |
| d440 | Fine hand use |
| d445 | Hand and arm use |
| d450 | Walking |
| d455 | Moving around |
| d460 | Moving around in different locations |
| d465 | Moving around using equipment |
| d470 | Using transportation |
| d510 | Washing oneself |
| d520 | Caring for body parts |
| d530 | Toileting |
| d540 | Dressing |
| d550 | Eating |
| d620 | Acquisition of goods/services |
| d630 | Preparing meals |
| d640 | Doing housework |

**Tier B — Moderate spatial dependency (in scope for FDA where item spec addresses them):**
d230, d310–d349, d475, d570, d610, d650, d660, d710–d729, d910–d920

**Out of scope for FDA threshold audit:** d110–d199 (learning), d240 (stress/handling demands),
d810–d899 (education/work beyond common areas)

For ICF codes outside Tier A/B scope encountered in an item spec: note as
`[OUT-OF-FDA-SCOPE: {code} — manual OT review required]` and do not apply Questions 3–4.

---

## Section 2 — Population↔ICF Mapping

FDA uses this mapping to check whether listed Applicable Groups match the ICF codes implied
by the item spec, and whether any affected populations are absent.

This mapping is distinct from FDR's spatial dependency tiers. It answers:
*Which populations have functional deficits in which ICF activities?*

**Primary ICF codes per population:**

| Population | Primary ICF codes | Mechanism |
|---|---|---|
| UPL (upper limb) | d440, d445, d510, d520, d540, d630 | Biomechanical — grip, force, range of motion, bilateral function |
| MOB (mobility) | d410, d420, d450, d455, d460, d465, d470, d510, d530 | Biomechanical — ambulation, balance, transfer, wheelchair use |
| DEM (dementia) | d230, d460, d710–d729 | Cognitive — memory, attention, wayfinding, sequencing |
| PAIN | d410, d450, d455, d640 | Pain-limited activity endurance; fatigue accumulation |
| NDV (neurodivergent) | d230, d710–d729, d910–d920 | Sensory processing, predictability, social navigation |
| VIS (visual impairment) | d460, d310–d329 | Sensory — spatial orientation, information access |
| DEAF | d310–d329, d330–d349 | Sensory — communication, alert receipt |
| SCI (spinal cord injury) | d410, d420, d450, d455, d465, d510, d520, d530, d630 | Biomechanical + autonomic |
| OFS (orthostatic/fatigue syndromes) | d450, d455, d470, d920 | Autonomic — activity tolerance, exertion limits, thermal |
| ABI (acquired brain injury) | d230, d440, d450, d460, d710–d729 | Cognitive + motor — variable |
| MH (mental health) | d230, d570, d710–d729, d910 | Psychological — routine, retreat, sensory safety |
| ASD (autism spectrum) | d230, d710–d729, d910–d920 | Sensory + predictability — environment consistency |
| LOW-VISION | d460, d310–d329, d620 | Sensory — partial vision, contrast, lighting dependency |
| PCS (post-COVID syndromes) | d450, d455, d570, d920 | Fatigue + autonomic — exertion limits |

**Note:** Most populations have secondary codes beyond those listed. The table shows primary
mapping only. Use clinical judgment (Opus) for secondary code assessment in Questions 1–2.

---

## Section 3 — Mechanism of Action Types

FDA Question 3 checks whether the claimed mechanism is correct. Valid mechanism types:

| Mechanism | Definition | Typical populations |
|---|---|---|
| Biomechanical | Force, range of motion, reach, balance, transfer geometry | UPL, MOB, SCI |
| Sensory-visual | Visual field, acuity, contrast sensitivity, glare | VIS, LOW-VISION, DEM |
| Sensory-auditory | Sound level, frequency, reverberation, alert type | DEAF, NDV, DEM |
| Sensory-proprioceptive | Surface texture, vestibular, spatial orientation | MOB, NDV, VIS |
| Sensory-olfactory | Fragrance, air quality | NDV, OFS |
| Cognitive | Memory, attention, executive function, sequencing | DEM, ABI, ASD, NDV |
| Autonomic-thermal | Temperature regulation, heat sensitivity (Uhthoff's) | SCI, OFS, PAIN, MH |
| Autonomic-orthostatic | Blood pressure regulation, exertion tolerance | OFS, PAIN, PCS |
| Communication | Information modality, format, density | DEAF, VIS, DEM, NDV |
| Social | Proximity, eye contact, circulation predictability | ASD, NDV, DEM |

An item spec may legitimately claim multiple mechanisms. The audit checks whether the
mechanism stated is *real and sufficient* — not merely possible.

---

## Audit Protocol

### Step 0 — Load item

Read the full item specification. Extract:
- Item code and name
- **Applicable Groups** field (as stated in spec)
- **Description/specification** body
- **Evidence basis** markers (●/○) and cited sources
- **Mode S** notes (if present)
- Any explicit population caveats

```bash
# Confirm item exists in items table
python3 scripts/db.py items | python3 -c "
import sys, json
items = json.load(sys.stdin)
item = next((i for i in items if i['item_code']=='I-01'), None)
print(item)
"
```

---

### Step 1 — Question 1: Population-ICF alignment (Sonnet)

*Do the listed Applicable Groups match the ICF codes implied by the spec?*

Procedure:
1. Identify the spatial parameter the item specifies (e.g., ≤22N operating force, ≥900mm width)
2. Map the parameter to its ICF code(s) from §1 Tier A/B
3. For each ICF code, look up which populations have that code in §2
4. Compare against listed Applicable Groups

**Findings:**

| Parameter | ICF code | Populations implied by ICF | Populations listed | Match? |
|---|---|---|---|---|

Flag MATCH, PARTIAL (some populations missing), or MISMATCH (wrong populations listed).

---

### Step 2 — Question 2: Population completeness (Sonnet)

*Are any affected populations absent from the Applicable Groups list?*

Procedure:
1. For each population in §2 whose primary ICF codes overlap the item's ICF codes:
   - Is the population listed? → PRESENT
   - Is the population absent despite having a deficit in this ICF code? → ABSENT-CANDIDATE
2. For ABSENT-CANDIDATEs: assess whether the item would *meaningfully* affect that
   population. Populations with secondary overlap where the item is not their primary
   access barrier = ACCEPTABLE-OMISSION (note, not a gap).

**Output:**
- ABSENT-CRITICAL: population should be listed; their access is materially affected
- ABSENT-SECONDARY: population affected but not primarily (ACCEPTABLE-OMISSION)
- OVER-INCLUDED: population listed but item does not materially affect their access

---

### Step 3a — Question 3: Mechanism validity (Sonnet extracts; Opus judges)

*Is the claimed mechanism of action correct and sufficient?*

**Sonnet:** Extract the stated mechanism from the spec (explicit or implied). Map to §3 taxonomy.

**Opus judgment required for:**
- Items claiming multiple mechanisms without resolving precedence
- Items where the stated mechanism conflicts with the populations listed
  (e.g., "Biomechanical FOR" claimed for a spec that primarily affects DEM via cognitive load)
- Items with no stated mechanism (implicit only)

**Output per mechanism claim:**
- CONFIRMED: stated mechanism is correct and sufficient for listed populations
- INCOMPLETE: mechanism correct but incomplete (secondary mechanism unstated)
- INCORRECT: stated mechanism is wrong — actual mechanism is different
- MISSING: no mechanism stated; item cannot be audited for threshold linkage

Flag INCORRECT and MISSING as AUDT gaps.

---

### Step 3b — Question 4: Threshold-population linkage (Opus required)

*Are threshold values tied to a specific population's functional limit?*

For each numeric threshold in the item spec (force, dimension, lux level, temperature, etc.):
1. Identify which population's functional limit the threshold derives from
2. Check whether that population is listed in Applicable Groups
3. Check whether the threshold is appropriate for *all* listed populations
   (a threshold derived from one population may be inadequate for another)

This step requires Opus because threshold appropriateness is a clinical judgment, not
a lookup. Sonnet may extract the thresholds; Opus determines whether they are correctly
derived and population-appropriate.

**Output:**
- LINKED: threshold traceable to named population's functional limit; population listed
- UNLINKED: threshold present but no population basis stated
- MISLINKED: threshold derived from population X but population X is not listed
- UNDER-CONSERVATIVE: threshold appropriate for the stated population but not for another
  listed population with a more severe deficit
- OUT-OF-FDA-SCOPE: threshold involves ICF code outside Tier A/B — note and skip

---

### Step 4 — Question 5: Over-inclusion check (Sonnet)

*Is there a population for whom the item is inapplicable or potentially harmful?*

Check each listed population against the item's parameters:
- Would applying this item's specification to a space serving this population produce
  a neutral, beneficial, or adverse outcome for that population?

Examples of over-inclusion:
- A grab bar requirement applied to a space serving only DEM (no mobility issue) where
  the bar creates a navigation hazard or confusion
- A high-contrast colour requirement applied to a space serving NDV where the high
  contrast is visually distressing

Flag OVER-INCLUDED populations with rationale. Do not remove populations without
evidence of harm — flag for Opus review in session notes.

---

### Step 5 — Question 6: FDR trigger assessment (Opus required)

*Does this item need a FDR research pass?*

FDR trigger criteria (any one is sufficient):

| Criterion | Signal in spec |
|---|---|
| THIN flag | Evidence basis contains [THIN] marker |
| Zero evidence | "zero indexed studies", "no published evidence" in BPC or spec notes |
| Clinical reasoning only | Co-2 sourcing for a Tier A threshold value (no Tier 1–3 support) |
| Single-source threshold | Threshold value cites only one study for a cross-jurisdictional claim |
| Analogical population | Threshold derived from Population X and applied to Population Y without direct evidence |
| Missing population evidence | ABSENT-CRITICAL population from Question 2 has no evidence for this ICF code |

**Opus judgment required:** Opus determines whether the trigger criteria genuinely apply
or whether the evidence base is adequate despite signals. A single THIN flag in a section
with otherwise adequate evidence may not warrant FDR.

**FDR trigger output format (if YES):**
One structured string per scenario needed:
```
FDR-TRIGGER: {d-code} + {functional constraint} → {environment context} [{population}]
```

Examples:
```
FDR-TRIGGER: d440 + UPL hemiplegia → hardware operability [UPL]
FDR-TRIGGER: d450 + PAIN fibromyalgia → corridor rest provision [PAIN]
```

---

### Step 6 — SQLite logging

**Scope errors (Questions 1–5) → AUDT gaps:**

```bash
python3 scripts/db.py add-gap \
  --category AUDT \
  --priority P2 \
  --description "FDA [question_code] [item_code]: [finding — what is wrong and what correction is needed]" \
  --skill functional-deficit-auditor \
  --section [item_code] \
  --session [session-name]
```

Question codes for description prefix:
- `FDA-Q1`: population-ICF mismatch
- `FDA-Q2`: absent or over-included population
- `FDA-Q3`: mechanism incorrect or missing
- `FDA-Q4`: threshold unlinked or mislinked
- `FDA-Q5`: population over-inclusion

**FDR triggers → RP gaps:**

```bash
python3 scripts/db.py add-gap \
  --category RP \
  --priority P2 \
  --description "FDA-Q6 FDR trigger [item_code]: {FDR-TRIGGER scenario string} — [rationale for trigger]" \
  --skill functional-deficit-auditor \
  --section [item_code] \
  --session [session-name]
```

After all gaps logged, confirm count:
```bash
python3 scripts/db.py gaps --status OPEN | python3 -c "
import sys, json
gaps = json.load(sys.stdin)
this_session = [g for g in gaps if g.get('created_by_session')=='SESSION_NAME']
print(f'Gaps logged this session: {len(this_session)}')
"
```

---

### Step 7 — Output summary (inline, parseable by audit-consolidator)

```
FUNCTIONAL-DEFICIT-AUDITOR COMPLETE
Session: [session-name]
Item: [item_code] — [item_name]
Populations audited: [listed Applicable Groups]

Q1 Population-ICF alignment:  PASS | [N] MISMATCH flags
Q2 Population completeness:   [N] ABSENT-CRITICAL | [N] OVER-INCLUDED | [N] ACCEPTABLE-OMISSION
Q3 Mechanism validity:        CONFIRMED | [N] INCORRECT | [N] MISSING
Q4 Threshold linkage:         [N] LINKED | [N] UNLINKED | [N] MISLINKED
Q5 Over-inclusion:            CLEAR | [N] flagged
Q6 FDR trigger:               NO | YES ([N] scenarios)

AUDT gaps logged: [N] (GAP-NNN through GAP-MMM)
RP gaps logged:   [N] (GAP-NNN through GAP-MMM)
Opus sections completed: Q3b, Q4, Q5-review, Q6
```

---

## Rules

1. FDA never commissions research — it flags RP gaps that route to FDR
2. FDA never removes populations without evidence of harm — flag for review, not deletion
3. Questions 3b, 4, and 6 require Opus — Sonnet may not determine mechanism validity
   or FDR trigger assessment
4. ICF codes outside Tier A/B are noted as OUT-OF-FDA-SCOPE and excluded from Questions 3–4
5. AUDT gaps route to ISW for authoring correction — not to FDR
6. RP gaps route to FDR — include the full FDR-TRIGGER scenario string in the description
7. A single item may produce both AUDT and RP gaps from the same audit run
8. Items with no evidence basis at all (no markers, no citations) → FDR trigger regardless
   of other questions; flag FDA-Q6 with ALL applicable Tier A ICF codes for the item
9. Population↔ICF mapping in §2 is the FDA's ground truth for Questions 1–2.
   Clinical judgment (Opus) may extend it for unusual items but must document the extension.
10. Feeds into: audit-consolidator (Step 7 output); FDR (via RP gaps); ISW (via AUDT gaps)
11. When reading `applicable_groups` from the items table, strip whitespace from each
    population code before comparison (stored values may have spaces after commas).
    Use: `[p.strip() for p in applicable_groups.split(',')]`
