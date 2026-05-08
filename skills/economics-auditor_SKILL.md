---
name: economics-auditor
description: >
  Per-item checklist audit of economic framing at item-spec level. Checks whether an item
  has a sound economic case: retrofit cost note evidenced, capital cost flagged, lifecycle
  framing present, economics volume linkage included, cost-of-omission documented, and
  framing compliant with economics-researcher framing rules. Distinct from
  economics-researcher, which conducts volume-level economics research. Auditor flags gaps
  (EC) and framing violations (AUDT); researcher runs in a separate session against those
  gaps. Auditor never triggers researcher inline. Runs as Step 7 of item-audit-pipeline.
  Trigger on: "audit economic framing", "check economics", "is the cost case sound",
  "economics review", "do we have a cost note".
  Decision: D-0148, 2026-05-05.
---

# Economics Auditor

**Model:** Sonnet 4.6 (checklist application — no Opus required)
**Intake:** Single item spec (≤500 lines). Full document → haiku-chunker first.
**Output target:** SQLite gaps table (EC for missing content; AUDT for framing violations)
**Feeds INTO:** economics-researcher (via EC gaps); ISW (via AUDT gaps)
**Does NOT feed inline:** economics-researcher is never called during an economics audit run

---

## Scope and Boundary

Economics-auditor operates at **item-spec level** — it audits what is present in the
item specification and flags what is missing or incorrectly framed.

Economics-researcher operates at **volume level** — it produces cost tables, grant
programme summaries, and ROI evidence for the economics volume (Part 11).

The auditor's trigger output (EC gap) routes to the researcher for a separate session.
The researcher's output feeds ISW for the authoring correction.

Do NOT call economics-researcher inline during an audit run.

---

## Framing Rules Reference (from economics-researcher §Framing Rules)

These apply to all economic language in item specs. Violations → AUDT gap.

| Rule | Requirement | Violation signal |
|---|---|---|
| FR-1 | Positive case first — lead with benefit, not compliance cost | "in order to comply with..." or "required under..." as opening framing |
| FR-2 | No compliance-burden language | "accessibility cost", "cost of compliance", "expense of meeting requirements" |
| FR-3 | Distinguish capital from lifecycle cost | Capital cost stated without lifecycle offset where cost-significant |
| FR-4 | No single-source cost claims | Specific cost figure with only one source citation |
| FR-5 | Jurisdiction-explicit | Cost data without named jurisdiction and date |
| FR-6 | No market-segment framing | "disabled people as market opportunity", "demographic" framing |

---

## Checklist Protocol

Run all 6 checks in sequence. Each check produces one of:
- ✅ PASS — criterion met
- ⚠️ PARTIAL — criterion partially met (note what is missing)
- ❌ ABSENT — criterion not met at all

Log gaps only for PARTIAL (where action improves the item) and ABSENT.

---

### Check 1: Retrofit cost note (EC or AUDT)

**Question:** Does the item have a retrofit cost note? Is it evidenced or asserted?

Look for: "Retrofit cost note", "Retrofit penalty", or equivalent language in the spec.

| State | Gap type | Action |
|---|---|---|
| Present + evidenced (cites a source or references Part 11) | ✅ PASS | None |
| Present + asserted (e.g. "LOW" with no basis) | ⚠️ PARTIAL → AUDT | Framing rule FR-4: asserted without evidence |
| Absent entirely | ❌ ABSENT → EC | Missing content; economics-researcher to supply |

---

### Check 2: Capital cost indicator (EC)

**Question:** Is a capital cost indicator present where the item is cost-significant?

Cost-significant signals: structural work, specialist installation, bespoke manufacture,
system-level provision (e.g. hearing loops, lift installation, HVAC modification).

Low-cost items (hardware swap, spec change only) are exempt from this check — note as
ACCEPTABLE-OMISSION with rationale.

| State | Gap type | Action |
|---|---|---|
| Cost-significant item with capital cost indicator | ✅ PASS | None |
| Cost-significant item without capital cost indicator | ❌ ABSENT → EC | Economics-researcher to supply cost range |
| Low-cost item (hardware, spec-only) | ✅ ACCEPTABLE-OMISSION | Note and skip |

---

### Check 3: Lifecycle framing (EC)

**Question:** Where capital cost is non-trivial, is lifecycle cost framing present?

Lifecycle framing = evidence that the total cost over time (including reduced maintenance,
reduced adaptation, reduced retrofit penalty) justifies the capital investment.

Only applies where Check 2 finds a cost-significant item without ACCEPTABLE-OMISSION.

| State | Gap type | Action |
|---|---|---|
| Lifecycle framing present and sourced | ✅ PASS | None |
| Lifecycle framing present but unsourced | ⚠️ PARTIAL → AUDT | FR-4 single-source or unsourced |
| Lifecycle framing absent on cost-significant item | ❌ ABSENT → EC | Economics-researcher to supply |
| Item is low-cost (Check 2 ACCEPTABLE-OMISSION) | N/A | Skip |

---

### Check 4: Economics volume linkage (EC)

**Question:** Does the item cross-reference the economics volume where relevant?

The economics volume is Part 11. Items with material economic content (retrofit cost,
capital cost, funding programme applicability) should cross-reference the relevant Part 11
section.

| State | Gap type | Action |
|---|---|---|
| Cross-reference to Part 11 present | ✅ PASS | None |
| Economic content present but no Part 11 reference | ⚠️ PARTIAL → AUDT | Missing cross-reference; ISW to add |
| No economic content + no reference | ✅ ACCEPTABLE-OMISSION | Note and skip |

---

### Check 5: Cost-of-not-doing (EC)

**Question:** Is there a documented consequence of omission?

Cost-of-not-doing = evidence of what happens when the item is absent (falls cost, retrofit
penalty multiplier, regulatory risk, resident harm, exclusion of population from space).

NOT required for every item — required where:
- The item has a documented retrofit penalty (cost multiplier when added late)
- The item addresses a significant safety risk (falls, thermal strain, etc.)
- The item is a statutory minimum in ≥1 jurisdiction

| State | Gap type | Action |
|---|---|---|
| Present and sourced | ✅ PASS | None |
| Present but unsourced | ⚠️ PARTIAL → AUDT | FR-4 |
| Required but absent | ❌ ABSENT → EC | Economics-researcher to supply |
| Not required for this item | ✅ ACCEPTABLE-OMISSION | Note rationale |

---

### Check 6: Framing compliance (AUDT)

**Question:** Does any economic language in the item violate the 6 framing rules?

Scan all economic language in the spec against FR-1 through FR-6.

| Violation | Gap type | Description format |
|---|---|---|
| FR-1 violation | AUDT | "FR-1 [item]: [quoted text] — reframe as benefit-led" |
| FR-2 violation | AUDT | "FR-2 [item]: [quoted text] — remove compliance-burden framing" |
| FR-3 violation | AUDT | "FR-3 [item]: capital cost stated without lifecycle offset" |
| FR-4 violation | AUDT | "FR-4 [item]: [claim] — single source or no citation" |
| FR-5 violation | AUDT | "FR-5 [item]: cost data lacks jurisdiction and/or date" |
| FR-6 violation | AUDT | "FR-6 [item]: [quoted text] — remove market-segment framing" |

---

## SQLite Logging

**EC gaps** (missing content — route to economics-researcher):

```bash
python3 scripts/db.py add-gap \
  --category EC \
  --priority P3 \
  --description "EA-C[1-5] [item_code]: [what is missing and what economics-researcher should provide]" \
  --skill economics-auditor \
  --section [item_code] \
  --session [session-name]
```

**AUDT gaps** (framing violations or asserted content — route to ISW):

```bash
python3 scripts/db.py add-gap \
  --category AUDT \
  --priority P3 \
  --description "EA-C[1-6]/FR-[1-6] [item_code]: [what is wrong and what ISW should correct]" \
  --skill economics-auditor \
  --section [item_code] \
  --session [session-name]
```

Default priority: P3. Upgrade to P2 if:
- Item is cost-significant and lifecycle framing absent (Check 3)
- Item has a safety risk and cost-of-not-doing absent (Check 5)
- FR-2 violation found (compliance-burden framing actively harms the economic case)

---

## Output summary (inline, parseable by audit-consolidator)

```
ECONOMICS-AUDITOR COMPLETE
Session: [session-name]
Item: [item_code] — [item_name]

Check 1 Retrofit cost note:     PASS | PARTIAL(AUDT) | ABSENT(EC)
Check 2 Capital cost indicator: PASS | ACCEPTABLE-OMISSION | ABSENT(EC)
Check 3 Lifecycle framing:      PASS | N/A | ABSENT(EC)
Check 4 Economics volume link:  PASS | PARTIAL(AUDT) | ACCEPTABLE-OMISSION
Check 5 Cost-of-not-doing:      PASS | REQUIRED-ABSENT(EC) | ACCEPTABLE-OMISSION
Check 6 Framing compliance:     PASS | [N] violations ([FR codes])

EC gaps logged:   [N] (GAP-NNN through GAP-MMM)
AUDT gaps logged: [N] (GAP-NNN through GAP-MMM)
Economics-researcher trigger: YES | NO
```

---

## Outputs

Per CO-0009 §5.10, this skill's output contract:

| Field | Value |
|---|---|
| Tables written | `gaps` (tracking DB) |
| Gap categories | EC (missing economic content, C1–C5); AUDT (framing violations, C1–C6) |
| source_skill | `economics-auditor` |
| citation-miner relevance filter | N/A — economics-auditor does not invoke citation-miner. Citation-miner runs as a separate cross-cutting step in item-audit-pipeline. |
| Idempotency mechanism | Wrapper-managed. Economics-auditor produces gaps with sequential GAP-NNN IDs; no natural dedup key exists at DB level. On re-run (`force_rerun`), the wrapper deletes prior gaps matching `(item_code, source_skill, created_by_session)` before invoking economics-auditor. Skill itself must not assume prior output has been cleared — always use `add-gap`, never `INSERT OR IGNORE`. |

---

## Rules

1. Economics-auditor never calls economics-researcher inline
2. All EC gaps route to economics-researcher in a separate session
3. All AUDT gaps route to ISW (framing correction or cross-reference addition)
4. Asserting a cost as "LOW" without citation is always a FR-4 violation → AUDT
5. Part 11 cross-reference absent where economic content exists → AUDT (not EC)
6. Check 6 scans all economic language in the spec — not just the cost note
7. ACCEPTABLE-OMISSION items must have a rationale noted in the output summary
8. Economics-researcher trigger is YES if any EC gap was logged with P2 priority
9. Feeds into: audit-consolidator (output summary); economics-researcher (EC gaps); ISW (AUDT gaps)
10. Boundary: auditor assesses item-spec economics; researcher produces volume-level content.
    Do not blur — an auditor finding ("retrofit cost note absent") is not itself a cost figure.
