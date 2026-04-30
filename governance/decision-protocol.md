# Decision Protocol
**Status:** CANONICAL — A12 Session 1
**Phase:** Stage A Phase 12 — Decision proxy and capture protocol
**Created:** 2026-04-30 03:00 UTC
**Doctrinal basis:** `workplan/workplan-co0007-v3.md` §A12 (decision proxy and capture protocol; resolves L-05 model-routing inconsistency) · `workplan/roadmap-2026-04-27.md` §A12 (Pattern: Governance + Code; produces decision_capture.py; CS8 cross-stage decision capture activates here) · `references/project-standards.md` Architecture (Sonnet 4.6 conversational; Opus 4.6 best-practice synthesis) · `references/effort-guide.md` (effort levels 50–150) · CO-0008 Project Instructions update (Opus 4.6 primary)

---

## 0. What this document covers and what it does not

This document specifies how decisions are made, captured, and queried in the project. It does not enumerate the decisions themselves — those live in the decision register (§5). It does not legislate which specific design or evidence questions resolve in which way — those are A6, A7, A8 territory. The protocol is a meta-layer that governs decision discipline: who decides, what gets written down, what model-routing notation is used in phase tables, and how prior decisions are surfaced when subsequent work touches their scope.

The document defines five decision categories (§1), three delegation categories (§2), the canonical capture format (§3), the standardised model-routing notation that resolves audit finding L-05 (§4), the decision register's location and format (§5), the CS8 integration with session-consolidator (§6), and the validator's scope and CLI (§7).

---

## 1. Decision categories

### 1.1 Five categories

Decisions in this project fall into five categories, each with characteristic delegation rules and capture requirements.

| Code | Category | Examples |
|---|---|---|
| D-DOCT | Doctrinal | Mission framing; CRPD posture; "teaches not prescribes"; population taxonomy structure; evidence-tier hierarchy |
| D-METH | Methodological | Evidence-state machine; convergence assessment rules; jurisdiction-tier mapping; freshness windows; misuse-vector catalogue authoring |
| D-SCHEMA | Schema / data-structure | Pydantic entity definitions; enum value sets; YAML round-trip behaviour; format patterns |
| D-OP | Operational | Branch protection state; commit-message convention; session-file naming; CI matrix; PAT scope |
| D-PRES | Presentation | Voice patterns; section ordering; figure conventions; plain-language register; role-based content variants |

Categories are mutually exclusive at the level of the decision's primary effect. A decision that has cross-category effect (e.g., a schema change driven by a doctrinal commitment) records under the category of its primary effect and cross-references the secondary category in §3 capture fields.

### 1.2 Why these five

The categorisation tracks how decisions enter the project's gravitational field. Doctrinal decisions sit at the top: they reach into all downstream work. Methodological decisions translate doctrine into operative rules for synthesising evidence. Schema decisions translate methodology into machine-checkable structure. Operational decisions resolve infrastructure questions that do not change content. Presentation decisions resolve how the synthesised content reaches the reader. The taxonomy is not arbitrary — it tracks the project's actual flow from doctrine through methodology, schema, and operations to presentation.

The categorisation also tracks delegation gradient: doctrinal decisions are typically the least delegable; presentation decisions are the most delegable. §2 makes this explicit.

---

## 2. Delegation rules

### 2.1 Three delegation categories

| Code | Delegation | Meaning |
|---|---|---|
| DG-NON | Non-delegable | The project owner alone. Other agents (Sonnet, Opus, contributors) propose; the project owner decides. |
| DG-REVIEW | Delegable with review | An agent decides; the project owner reviews before the decision is treated as canonical. The review may be batched (multiple decisions reviewed together) or per-decision. |
| DG-AUTO | Delegable / automatic | An agent decides; no review gate. Decision is logged; surfaces for review only if a downstream check flags inconsistency. |

### 2.2 Default delegation by category

| Decision category | Default delegation | Rationale |
|---|---|---|
| D-DOCT | DG-NON | Doctrinal decisions reach into all downstream work; they cannot be delegated. |
| D-METH | DG-NON for new methodology; DG-REVIEW for application of existing methodology | The methodology itself is non-delegable; specific applications (e.g., classifying a new source's evidence tier) are delegable with review. |
| D-SCHEMA | DG-REVIEW | Schema choices that satisfy already-canonical methodology are delegable; novel schema patterns review-gated. |
| D-OP | DG-AUTO for routine operations; DG-REVIEW for first-of-kind | Branch-protection state, CI matrix updates, etc. are routine; the first commit-message convention or first session-file format is review-gated. |
| D-PRES | DG-AUTO within voice-style §§8.1–8.3 patterns; DG-REVIEW outside them | Pattern-conforming presentation decisions self-validate; novel patterns or pattern departures review-gated. |

### 2.3 Departure from default

A decision can depart from the default delegation. Departures are explicit: the decision record names the actual delegation and the reason. Common departure cases:

- A D-METH decision that has a doctrinal flow-through is recorded as DG-NON (delegation upgraded).
- A D-OP decision with material consequence (e.g., changing the PAT scope) is recorded as DG-REVIEW (delegation upgraded).
- A D-DOCT decision that merely operationalises a prior decision (e.g., adopting CC BY-SA 4.0 once the licensing-decision space was scoped) is recorded as DG-REVIEW (delegation downgraded).

Departures are visible in the decision record's `delegation` field and `delegation_rationale` field.

### 2.4 Non-delegable decisions explicitly

The following decision types are always DG-NON:

1. Mission, audience, and CRPD posture framing
2. Population taxonomy structure (codes, sub-codes, proxy decisions)
3. Evidence-tier definitions (1–6 + Co-1)
4. Inclusion/exclusion of jurisdictions
5. Inclusion/exclusion of major work-products (Volumes, Parts, Supplementary, Appendices)
6. Co-1 source corpus inclusion/exclusion
7. Licensing model (per A11 §4)
8. Trajectory positioning (per A11 §5)
9. Adversarial-use catalogue retirement (per A10 §5.4 — addition is DG-REVIEW)
10. Counsel-review queue resolution (per A11 §6)

The DG-NON list is itself a doctrinal decision and is added to the decision register as D-DOCT.DG-NON.

---

## 3. Capture protocol

### 3.1 Every decision produces a written rationale

The protocol's central requirement: every decision in any of the five categories produces a written rationale alongside the outcome. The rationale is brief but sufficient — a future agent (the same project owner returning months later, a new contributor onboarding, an Opus agent invoked for synthesis) reads the rationale and understands not just the decision but the reasoning. "We chose CC BY-SA 4.0" is not sufficient. "CC BY-SA 4.0 chosen because it permits derivatives and translations (rejected by ND), preserves attribution (required by mission), and prevents proprietary repackaging (rejected by share-alike)" is sufficient.

### 3.2 Required fields

Every decision record carries these required fields:

| Field | Description |
|---|---|
| `decision_id` | `D-NNNN` zero-padded sequential within the register |
| `category` | One of D-DOCT, D-METH, D-SCHEMA, D-OP, D-PRES |
| `delegation` | One of DG-NON, DG-REVIEW, DG-AUTO |
| `delegation_rationale` | Required if delegation departs from §2.2 default; optional otherwise |
| `summary` | One-sentence summary of the decision |
| `outcome` | The actual decision (e.g., "CC BY-SA 4.0", "convergence is divergent with synthesis_approach", "Tier 4–5 freshness window = 5 years") |
| `rationale` | The written reasoning (per §3.1) |
| `alternatives_considered` | Other options weighed; required for D-DOCT and D-METH; optional otherwise |
| `decision_date` | YYYY-MM-DD HH:MM, UTC |
| `decided_by` | Agent identifier (project owner; Opus session; Sonnet session; review batch) |
| `model_routing` | Standardised model-routing notation per §4 |
| `effort_level` | Per `references/effort-guide.md`; one of 150, 125, 100, 75, 50 |
| `decision_artifacts` | Cross-references to governance docs, schemas, validators, commits where the decision lives |
| `predecessors` | Other decision_ids this decision builds on or extends |
| `supersedes` | Other decision_ids this decision retires (uses A9 SupersedenceLink primitive) |
| `status` | One of ACTIVE, SUPERSEDED, RETIRED |
| `review_status` | One of PENDING (DG-REVIEW awaiting review), CONFIRMED, NA (DG-NON or DG-AUTO) |
| `notes` | Freeform addenda |

### 3.3 Rationale length norms

Rationale length is calibrated to decision weight:

| Category | Rationale norm |
|---|---|
| D-DOCT | 3–10 sentences. Captures the alternatives weighed and why this was chosen over them. |
| D-METH | 2–5 sentences. Captures the methodological principle the decision applies and the application context. |
| D-SCHEMA | 1–3 sentences. Captures the schema constraint and the round-trip / validation behaviour it preserves. |
| D-OP | 1 sentence. Captures the operational outcome. |
| D-PRES | 1–2 sentences. Captures the pattern conformance or departure. |

Rationale exceeding the norm is acceptable. Rationale below the norm is incomplete; the validator (§7) flags it.

### 3.4 Rationale anti-patterns

Three rationale patterns are flagged by the validator as incomplete:

- **Tautology.** "Chose X because X is the right choice." No reasoning content.
- **Authority-without-content.** "Chose X because the spec says X." The spec citation should appear in `decision_artifacts`; the rationale should explain why X is what the spec says (or why the spec was followed in this case).
- **Outcome-as-rationale.** "Chose X because X." The rationale should explain the choice; the outcome field already records X.

---

## 4. Standardised model-routing notation (resolves L-05)

### 4.1 The L-05 finding

Audit finding L-05 (per `workplan/workplan-co0007-v3.md` §L-05): model-routing notation is inconsistent across phase tables. Some phase tables write "Opus session"; some write "Opus 4.6"; some write "Opus assigned"; some write "best-practice synthesis"; some omit model-routing entirely. Readers cannot reliably tell which model is expected for a given phase.

### 4.2 Canonical notation

The canonical notation is a single field with three components:

```
{model_tier}/{effort_level}/{reasoning_modifier}
```

Where:

| Component | Allowed values | Required? |
|---|---|---|
| `model_tier` | `opus`, `sonnet`, `haiku`, `human` | Yes |
| `effort_level` | `150`, `125`, `100`, `75`, `50` | Yes |
| `reasoning_modifier` | `synth`, `arbitrate`, `extract`, `format`, `route`, `none` | Yes |

Examples:

| Notation | Meaning |
|---|---|
| `opus/150/synth` | Opus 4.6, effort 150, reasoning modifier = best-practice synthesis |
| `opus/150/arbitrate` | Opus 4.6, effort 150, reasoning modifier = evidence arbitration between divergent positions |
| `sonnet/125/synth` | Sonnet 4.6, effort 125, reasoning modifier = synthesis (high-end Sonnet load) |
| `sonnet/100/route` | Sonnet 4.6, effort 100, reasoning modifier = workplan routing / orchestration |
| `sonnet/75/extract` | Sonnet 4.6, effort 75, reasoning modifier = single-pass extraction |
| `haiku/50/format` | Haiku 4.5, effort 50, reasoning modifier = mechanical format |
| `human/none/none` | Project owner decision; no model assigned |

### 4.3 Phase-table application

Every phase table that records model-routing uses this notation. The skill index in `skills/workplan-orchestrator_SKILL.md` and the effort-guide table in `references/effort-guide.md` are updated to use the canonical notation. Old notation forms ("Opus session", "Opus assigned", "best-practice synthesis", etc.) are deprecated — surfacing them in new content is a validator error.

### 4.4 Notation in decision records

Every Decision record's `model_routing` field uses this notation. Decisions made by the project owner without model assistance use `human/none/none`. Decisions made by an Opus session at effort 150 producing best-practice synthesis use `opus/150/synth`. The validator (§7) checks the notation against the regex `^(opus|sonnet|haiku|human)/(150|125|100|75|50|none)/(synth|arbitrate|extract|format|route|none)$` and rejects anything else.

### 4.5 Phase-level routing

A phase (e.g., A6 evidence-methodology, A12 decision-protocol) may have multiple decisions with different model-routing values. The phase's overall routing is recorded in the workplan-orchestrator's Stage A Skill Build Schedule using the same notation. Phases mostly run at one model-routing value; mixed-routing phases declare the routing per-deliverable.

---

## 5. Decision register

### 5.1 Location

The canonical decision register lives at `data/decisions/decision_register.yaml`. Per-decision detail (where rationale exceeds register-summary length) lives at `data/decisions/{decision_id}.yaml` — one file per decision, optional. The register itself records the `decision_id`, summary fields, and a `detail_file` pointer if a detail file exists.

`workplan/v10-1-decision-register.md` (referenced in session-consolidator §1b) is a legacy path that was never populated. A12 supersedes that path: the canonical location is `data/decisions/decision_register.yaml`; the legacy reference in session-consolidator is updated to point to the new location at the next session-consolidator skill update.

### 5.2 Register structure

```yaml
register_version: 1
last_updated: 2026-04-30 03:00
decisions:
  - decision_id: D-0001
    category: D-DOCT
    delegation: DG-NON
    summary: "..."
    outcome: "..."
    rationale: "..."
    decision_date: 2026-XX-XX HH:MM
    decided_by: "..."
    model_routing: human/none/none
    effort_level: 150
    decision_artifacts:
      - "..."
    predecessors: []
    supersedes: []
    status: ACTIVE
    review_status: NA
  - decision_id: D-0002
    ...
```

### 5.3 Initial seeding

The register is initially seeded by extracting prior decisions from existing project artifacts:

| Source | What is extracted |
|---|---|
| `references/project-standards.md` Core Doctrine block | Each doctrinal commitment becomes one D-DOCT decision |
| `references/project-standards.md` per-session RULE blocks | Each rule becomes one decision (category by content) |
| `governance/*.md` "Decisions" sections (if present) | Each named decision becomes one record |
| `sessions/session_*.md` `session_close.next_action` blocks | Each session-end pivot becomes one D-OP decision |
| Workplan amendments (`workplan/workplan-co0007-v3-amendments.md` etc.) | Each amendment becomes one D-METH or D-OP decision |

Initial seeding produces an estimate of 80–120 records spanning A1 through A11. Extracted records carry `model_routing: legacy/none/none` and `effort_level: 100` as placeholder values until reviewed. A12 Session 2 runs the actual extraction; this session establishes the structure.

### 5.4 Querying

The register supports three primary query patterns:

1. **By decision_id**: direct lookup. Used by cross-references in governance docs (`see D-0042`).
2. **By category × status**: e.g., "all ACTIVE D-DOCT decisions". Used by audit phases (A13 doctrine-recheck loads all D-DOCT).
3. **By predecessors / supersedes**: dependency walks. Used when a decision is being superseded — surfaces all decisions that build on it for review.

The validator (§7) does not implement query operations beyond format validation; query is the application's job (manual grep, audit scripts, future website).

---

## 6. CS8 decision capture — cross-stage integration

### 6.1 What CS8 activates

CS8 (cross-stage 8) per `workplan/workplan-co0007-v3.md`: "decision capture activates here; every decision point thereafter produces written rationale alongside outcome." A12 is the activation point. Once A12 is canonical:

- Every new decision point in any subsequent session produces a Decision record at session close.
- Every governance document update appends or supersedes Decision records as appropriate.
- Every commit that introduces a new RULE in `project-standards.md` is paired with a Decision record (the RULE is the public-facing artifact; the Decision record is the queryable source).

### 6.2 session-consolidator integration

The session-consolidator skill (per `skills/session-consolidator_SKILL.md`) is updated to:

1. Detect decisions made in the session (proxy: any new RULE in project-standards.md, any new governance doc, any session_close.next_action change).
2. For each detected decision, produce a Decision record (decision_id, category, delegation, summary, outcome, rationale, decision_artifacts).
3. Append the new records to `data/decisions/decision_register.yaml`.
4. Validate the appended records against the validator (§7 C1, C2, C4) before commit.

The session-consolidator update is a separate task scheduled for A12 Session 2 (alongside seeding extraction). This Session 1 establishes the protocol; Session 2 wires the protocol into the consolidator.

### 6.3 What this is not

CS8 is not a "every minute decision needs a record" protocol. The five categories (§1) define the scope. A typing choice (`int` vs. `str` for a Pydantic field) is a schema implementation detail, not a Decision in the protocol's sense. A schema decision that survives review and codifies a pattern (e.g., "all enum-defaulted fields use string defaults to dodge the model_dump quirk") is a Decision. The discriminator: would a future agent need to read the rationale to understand why this is the way it is? If yes, it is a Decision. If no, it is implementation detail.

---

## 7. Validator specification (`scripts/decision_capture.py`)

### 7.1 Scope

The validator enforces register format and rationale completeness. It does not validate semantic content (i.e., it cannot tell whether a rationale is "good" — only whether it is present and meets length norms).

### 7.2 Inputs

| Path | Purpose |
|---|---|
| `data/decisions/decision_register.yaml` | The register itself |
| `data/decisions/D-NNNN.yaml` (optional) | Per-decision detail files |
| `references/project-standards.md` | Cross-reference: every CANONICAL RULE should map to one or more Decision records (after seeding) |

### 7.3 Checks

| Check | Severity | Description |
|---|---|---|
| C1 register well-formed | ERROR | Loads + validates against DecisionRegister schema |
| C2 unique decision_ids | ERROR | No duplicate D-NNNN |
| C3 rationale length compliant | WARNING | Per §3.3 norms; below norm flags warning |
| C4 model-routing format | ERROR | Matches §4.4 regex |
| C5 supersedes consistency | ERROR | If `supersedes` lists D-XXXX, then D-XXXX must exist and have status=SUPERSEDED |
| C6 rationale anti-pattern | WARNING | Detects §3.4 patterns: tautology, authority-without-content, outcome-as-rationale |
| C7 RULE coverage (post-seeding) | WARNING | Every CANONICAL RULE in project-standards has at least one Decision record |
| C8 review_status consistency | ERROR | DG-NON/DG-AUTO → review_status=NA; DG-REVIEW → review_status one of PENDING/CONFIRMED |

### 7.4 CLI

| Flag | Behaviour |
|---|---|
| `--register-only` | Run C1–C6 against the register; skip C7 RULE-coverage |
| `--decision-id D-NNNN` | Validate only the named decision |
| `--report` | Print summary; exit 0 always |

Exit codes: 0 = pass, 1 = errors, 2 = config error.

### 7.5 What the validator does NOT do

- It does not validate rationale quality (only length and anti-pattern).
- It does not detect missing decisions (it only checks coverage of existing CANONICAL RULEs in project-standards; it does not detect a decision that should have been recorded but was not).
- It does not enforce categorical correctness (it cannot tell whether a decision should be D-METH vs. D-DOCT).

These are human-judgment calls. The validator enforces format; doctrine-recheck (A13) audits semantic correctness.

---

## 8. Status

| Field | Value |
|---|---|
| Created | 2026-04-30 03:00 UTC |
| Phase | Stage A Phase 12 — Decision proxy and capture protocol — Session 1 |
| Status | CANONICAL |
| Forward dependencies | A12 Session 2 (seeding extraction + session-consolidator integration); A13 (doctrine-recheck consumes the register); CS8 activates with this document landing |
| Schema dependencies | `schemas/decision.py` (new); `schemas/enums.py` (extended) |
| Resolves | L-05 model-routing inconsistency (§4); CS8 activation (§6) |

### 8.1 Change log

| Date | Change |
|---|---|
| 2026-04-30 03:00 | Initial canonical version. Five categories, three delegation tiers, capture protocol, model-routing notation, register structure, CS8 activation, validator specification. |

### 8.2 Sessions remaining in A12

Per the armature integration §A12 expansion, A12 is 3–4 sessions. Session 1 (this) lands the protocol itself. Subsequent sessions:

- **Session 2:** Seeding extraction (project-standards → register; sessions → register; governance → register). Session-consolidator integration. Initial register publishes with 80–120 records.
- **Session 3 (if armature expansion in scope):** Role-based content variant decisions; carer role specification; plain-language register specification; Easy Read classification.
- **Session 4 (if armature expansion in scope):** Variable-conflation algorithm; §3.8 Step 0 UI surfacing; Capability Approach integration depth.

Sessions 3–4 are armature-driven and may be reordered, split, or deferred to Stage B if their scope is more architectural than doctrinal.

---

**End of A12 governance document.**
