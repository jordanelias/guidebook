# Claim-to-Reference Join Table
<!-- Generated 2026-04-19 — Step 3 of citation infrastructure -->
<!-- This is the BACKEND JOIN: every numeric claim in any Part → its supporting references -->

**Purpose:** Traceable mapping from each specification claim in Parts 1-12 to the references that support it. Phase B parsers read this table to render footnotes on the frontend.

**Generation:** Auto-extracted numeric specifications (values + units) from `parts/v10/part*.md`. Each entry has a unique CLAIM-ID. Human judgment required to populate `ref_ids` (Step 2 of build — see global-reference-registry.md for source IDs).

**Total claims enumerated:** 1382

**Status distribution:**
- `PENDING` — no references assigned (initial state)
- `TAGGED` — references assigned via Step 2 tagging
- `VERIFIED` — references confirmed accurate
- `DEFERRED` — claim is non-citable (definitional, cross-reference, or derived)

**Full machine-readable data:** `references/claim-reference-join.json`

**Schema:**
| Field | Description |
|---|---|
| `claim_id` | Globally unique: CLAIM-PXX-NNNN (part-sequence) |
| `part` | Part number (1-12) |
| `line` | Line number in source Part file |
| `scope` | Item code (Part 4) or section heading (other Parts) |
| `claim_type` | numeric_specification / textual_assertion / derived |
| `claim_value` | The specific value or statement |
| `context` | ≤120 chars of surrounding text |
| `ref_ids` | List of global REF-IDs from global-reference-registry.md |
| `status` | PENDING / TAGGED / VERIFIED / DEFERRED |

---

## Summary by Part

| Part | Claims | PENDING | TAGGED | VERIFIED |
|---|---|---|---|---|
| Part 1 | 7 | 7 | 0 | 0 |
| Part 2 | 83 | 83 | 0 | 0 |
| Part 3 | 42 | 42 | 0 | 0 |
| Part 4 | 558 | 558 | 0 | 0 |
| Part 5 | 79 | 79 | 0 | 0 |
| Part 6 | 115 | 115 | 0 | 0 |
| Part 7 | 111 | 111 | 0 | 0 |
| Part 8 | 116 | 116 | 0 | 0 |
| Part 9 | 10 | 10 | 0 | 0 |
| Part 10 | 23 | 23 | 0 | 0 |
| Part 11 | 191 | 191 | 0 | 0 |
| Part 12 | 47 | 47 | 0 | 0 |

---

## Sample Claims per Part

The full claim list lives in the JSON file. This markdown table shows the first 3 claims from each part as a representative sample.

### Part 1

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P01-0001 | 285 | §1.9.1 | `6 mm` | Every dimensional specification in this guidebook — threshold height, ramp gradi... |
| CLAIM-P01-0002 | 285 | §1.9.1 | `450–500 mm` | Every dimensional specification in this guidebook — threshold height, ramp gradi... |
| CLAIM-P01-0003 | 285 | §1.9.1 | `40%` | Every dimensional specification in this guidebook — threshold height, ramp gradi... |

### Part 2

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P02-0001 | 42 | §2.1 | `6 mm` | **Primary environmental barriers.** Steps; thresholds above 6 mm; gradients exce... |
| CLAIM-P02-0002 | 46 | §2.1 | `1524 mm` | Turning space is the most consequential single parameter. The ADA 1524 mm (5'0")... |
| CLAIM-P02-0003 | 46 | §2.1 | `1970s` | Turning space is the most consequential single parameter. The ADA 1524 mm (5'0")... |

### Part 3

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P03-0001 | 4 | part3-intro | `16%` | > **Evidence density: ▓ Moderate (methodology) / ░ Thin (compound effects)** — T... |
| CLAIM-P03-0002 | 15 | §3.1 | `≤18°C` | Designing for one population category at a time and then attempting to reconcile... |
| CLAIM-P03-0003 | 35 | §3.2.3 | `42.5%` | Epidemiological data confirms that the design assumption of a single-category us... |

### Part 4

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P04-0001 | 38 | part4-intro | `500 Hz` | All RT60 specifications are for the 500 Hz octave band in the occupied condition... |
| CLAIM-P04-0002 | 53 | A-01 | `5 m` | **Description:** 5 m deep acoustic buffer zone between any noise-generating adja... |
| CLAIM-P04-0003 | 56 | A-01 | `3 m` | Buffer zone depth: 3 m (minimum); 5 m (preferred)... |

### Part 5

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P05-0001 | 25 | §5.1 | `32–45 mm` | 4. **Range specifications are preferred over point specifications.** Where a par... |
| CLAIM-P05-0002 | 25 | §5.1 | `32 mm` | 4. **Range specifications are preferred over point specifications.** Where a par... |
| CLAIM-P05-0003 | 25 | §5.1 | `45 mm` | 4. **Range specifications are preferred over point specifications.** Where a par... |

### Part 6

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P06-0001 | 53 | §6.0 | `≥900 mm` | \| E-08 \| Corridor clear width ≥900 mm on all circulation routes \| SD \| Floor... |
| CLAIM-P06-0002 | 57 | §6.0 | `400–1100 mm` | \| H-01 \| All controls 400–1100 mm AFF \| CD \| Electrical drawings \|... |
| CLAIM-P06-0003 | 96 | §6.1 | `20 mm` | \| Smart lock conduit \| 20 mm conduit from external entry to consumer unit \| F... |

### Part 7

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P07-0001 | 23 | §7.0 | `≥3 m` | \| E-11 \| Automatic doors (primary entrance; motion ≥3 m) \| DD \| Floor plan; ... |
| CLAIM-P07-0002 | 24 | §7.0 | `≥1500 mm` | \| E-08 \| Corridor clear width ≥1500 mm (≥1800 mm HLT/TRP) \| SD \| Floor plan ... |
| CLAIM-P07-0003 | 24 | §7.0 | `≥1800 mm` | \| E-08 \| Corridor clear width ≥1500 mm (≥1800 mm HLT/TRP) \| SD \| Floor plan ... |

### Part 8

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P08-0001 | 75 | 9.1.2 | `500 Hz` | \| A-02 \| Acoustic Ceiling Panels (NRC ≥0.85) \| AC \| DD \| No \| RT60 at 500 ... |
| CLAIM-P08-0002 | 78 | 9.1.2 | `500 Hz` | \| A-06 \| Acoustic Wall Panels — Mid-Frequency Treatment \| AC \| DD \| No \| R... |
| CLAIM-P08-0003 | 80 | 9.1.2 | `<0.1 m` | \| A-09 \| HVAC Vibration Isolation (Floating Plant Room) \| AC, ME, SE \| SD \|... |

### Part 9

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P09-0001 | 280 | §9.9 | `≤18°C` | *Stage 3 (Technical Design):* Each specialist consultant issues their brief with... |
| CLAIM-P09-0002 | 336 | §9.11 | `≥1500 mm` | *Stage 2 (Schematic):* Review floor plan for: corridor widths ≥1500 mm on primar... |
| CLAIM-P09-0003 | 338 | §9.11 | `900–1200 mm` | *Stage 3 (Technical Design):* Specify: tactile building map content and update p... |

### Part 10

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P10-0001 | 4 | part10-intro | `39%` | > **Evidence density: ▓ Moderate** — DAR cost multiplier framework is grounded i... |
| CLAIM-P10-0002 | 28 | §10.1 | `≥3600 mm` | \| Ceiling hoist tracking blocking (continuous run ≥3600 mm, centred on bed zone... |
| CLAIM-P10-0003 | 29 | §10.1 | `1200 mm` | \| Through-floor lift structural zone (≥900×1200 mm, same position each floor) \... |

### Part 11

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P11-0001 | 4 | part11-intro | `4%` | > **Evidence density: ▓ Moderate (direction) / ░ Thin (precision)** — Direction ... |
| CLAIM-P11-0002 | 12 | part11-intro | `0004 Pa` | - Cross-part references updated to CO-0004 Part numbering... |
| CLAIM-P11-0003 | 29 | part11-intro | `4%` | - Accessibility decided at brief stage typically adds 1--4% to construction cost... |

### Part 12

| Claim ID | Line | Scope | Value | Context |
|---|---|---|---|---|
| CLAIM-P12-0001 | 38 | §12.01 | `≥75%` | **Key design strategies:** - Single-storey, step-free throughout (E-06, E-11) - ... |
| CLAIM-P12-0002 | 40 | §12.01 | `71%` | **Verified outcomes:** - Independent RHFAC Accessible Level certification (Tier ... |
| CLAIM-P12-0003 | 54 | §12.02 | `≥1800 mm` | **Key design strategies:** - DeafSpace 5 principles: sensory reach, space and pr... |

---

## How to populate `ref_ids` (Step 2 instructions)

For each claim:
1. Identify which BPC file(s) cover the topic area
2. Look up the claim's source in that BPC's Key sources table
3. Find the matching global REF-ID in `global-reference-registry.md`
4. Add the REF-ID(s) to this claim's `ref_ids` field
5. Set status to `TAGGED`

**Priority order:**
- Tier 1–2 sources cited first
- Multiple refs allowed per claim (primary + supporting)
- If no reference exists for a claim, flag as `status: ORPHANED` (important — indicates specification derived without direct citation)

**Verification:** After tagging, a second pass sets `status: VERIFIED` for claims where the cited ref genuinely supports the stated value (not just same topic).
