---
name: evidence-marker
description: >
  Classify and audit evidence specification markers (● filled circle / ○ empty circle) on
  all prescriptive specifications in the guidebook. ● = evidence-based specification
  (Tier 1–6 evidence exists). ○ = inferred from clinical reasoning or expert consensus
  (evidence gap disclosed). ALWAYS use this skill when asked to: add evidence markers,
  audit evidence markers, check which specs are marked, find unmarked specifications,
  verify marker accuracy, upgrade ○ to ● after new evidence, or classify specifications
  by evidence basis. Trigger on: "evidence markers", "filled circle", "empty circle",
  "mark the specs", "which specs have evidence", "evidence classification", "marker audit",
  "upgrade markers", "●/○ check". Used in Phase 3 (writing) and Phase 5 (QA).
---

**Model:** Sonnet 4.6 — evidence judgment required.
**Input:** Item specification text + evidence table + BPC entry for the item's slug(s).
**Output:** Marked specification text + marker audit log.
**Chunk ceiling:** ≤30 items per run. Full category → haiku-chunker first.

---

## Marker Definitions

| Marker | Meaning | Criteria |
|---|---|---|
| **●** (filled circle) | Evidence-based specification | At least one Tier 1–6 source directly supports the specification value. Source is cited in the evidence table. |
| **○** (empty circle) | Inferred specification | No direct evidence for the specification value. Derived from clinical reasoning, expert consensus, extrapolation from adjacent evidence, or analogical reasoning. Evidence gap is disclosed. |

The distinction is noted at the beginning of each volume containing specifications.

---

## Marker Placement

Markers are placed at the **sentence level** within the Specification section of each item. Every prescriptive sentence (one that states a dimension, material, arrangement, or performance requirement) carries exactly one marker.

```markdown
#### Specification

● Grab bars to be provided on both sides of the toilet, mounted at 700–800 mm AFFL.

○ Grab bar finish to be non-reflective matte to reduce visual distraction for NDV/SENS populations.

● Grab bar diameter to be 32–38 mm to accommodate grip strength variation across MOB/UPL populations.
```

**Rules:**
- One marker per prescriptive sentence. No unmarked prescriptive sentences.
- Non-prescriptive sentences (context, rationale, cross-references) do not carry markers.
- Headings never carry markers.
- Evidence table entries do not carry markers (they are the evidence, not the specification).
- Conflict notes, retrofit notes, and cross-reference sections do not carry markers.

---

## Classification Mode (Phase 3 — Writing)

When `item-specification-writer` produces a new or revised item:

1. For each prescriptive sentence in the Specification section:
   - Check the item's evidence table: does any cited source directly support this sentence's claim?
   - Check the BPC entry for the item's slug(s): does the `best_practice_synthesis` or `consensus_findings` provide direct evidence?
   - If YES to either → assign **●**
   - If NO to both → assign **○** and add disclosure: `[Expert consensus / clinical reasoning — no direct evidence; see gap register GAP-XXX]`
2. If a sentence's evidence is a case study only (Tier 2–3 from Part 13 evidence mining): assign **●** but note `[Case study evidence — Tier 2–3]` in the evidence table.
3. If a sentence extrapolates from evidence for a different population: assign **○** with note `[Extrapolated from {source population} evidence]`.

---

## Audit Mode (Phase 5 — QA)

Scan all prescriptive sentences in the defined scope:

| Check | Flag |
|---|---|
| Prescriptive sentence has no marker | 🔴 UNMARKED — must be classified |
| ● marker but no citation in evidence table | 🔴 UNSUPPORTED-● — downgrade to ○ or add citation |
| ○ marker but evidence exists in BPC | 🟡 UPGRADEABLE — may warrant ● after review |
| ● marker but cited source is UNVERIFIED | 🟡 UNVERIFIED-● — hold pending citation-verifier |
| ○ marker with no gap register entry | 🟡 UNDISCLOSED-GAP — add gap register entry |
| Non-prescriptive sentence has a marker | 🟢 MISPLACED — remove marker |

**Output:**

```
EVIDENCE MARKER AUDIT — [scope]
Date: YYYY-MM-DD HH:MM

Summary:
  Total prescriptive sentences: [N]
  ● (evidence-based): [N] ([%])
  ○ (inferred): [N] ([%])
  Unmarked: [N] 🔴
  Unsupported-●: [N] 🔴
  Upgradeable: [N] 🟡
  Unverified-●: [N] 🟡

Findings:
| ID | Item | Line | Marker | Flag | Detail |
```

---

## Upgrade Protocol

When new evidence is found (e.g., case study mining, new multilingual-research run):

1. Identify the prescriptive sentence(s) the new evidence supports.
2. Verify the evidence directly supports the specification value (not just the topic).
3. Add the citation to the item's evidence table.
4. Change ○ → ● on the supported sentence.
5. Log the upgrade: `UPGRADE: {item code} — ○→● — source: {citation} — [YYYY-MM-DD HH:MM]`
6. If the evidence is case-study-only: assign ● with tier note.

---

## Escalation Triggers

- >50% of specifications in a category are ○ → flag as THIN-EVIDENCE-CATEGORY; append to gap register
- Any safety-critical item (emergency evacuation, structural load, seizure risk) has ○ → 🔴 escalate immediately
- Marker audit finds >10 UNMARKED sentences → flag as systematic omission; likely a writing pass missed markers

---

**Preceded by:** `item-specification-writer` (classification) · `chunk-assembler` (audit)
**Feeds into:** `evidence-auditor` (marker accuracy cross-check) · `gap_register.md` (thin categories)
