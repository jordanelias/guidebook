# Decision Protocol
**Status:** CANONICAL — A12 Session 1
**Phase:** Stage A Phase 12 — Decision proxy and capture protocol
**Created:** 2026-04-30 03:00 UTC
**Doctrinal basis:** `workplan/workplan-co0007-v3.md` §A12 (decision proxy and capture protocol; resolves L-05 model-routing inconsistency) · `workplan/roadmap-2026-04-27.md` §A12 (Pattern: Governance + Code) · `references/project-standards.md` Architecture (Sonnet 4.6 conversational; Opus 4.6 best-practice synthesis) · `references/effort-guide.md` (effort levels 50–150) · CO-0008 Project Instructions update (Opus 4.6 primary)

---

## 0. What this document covers and what it does not

This document specifies how decisions are made and captured in the project. It does not enumerate the decisions themselves — those live in the owner ledger (`references/project-standards.md`) and in `decisions/`. It does not legislate which specific design or evidence questions resolve in which way — those are A6, A7, A8 territory. The protocol is a meta-layer that governs decision discipline: who decides, what gets written down, what model-routing notation is used in phase tables.

The document defines five decision categories (§1), three delegation categories (§2), the canonical capture format (§3), and the standardised model-routing notation that resolves audit finding L-05 (§4).

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

---

## 3. Capture protocol

### 3.1 Every decision produces a written rationale

The protocol's central requirement: every decision in any of the five categories produces a written rationale alongside the outcome. The rationale is brief but sufficient — a future agent (the same project owner returning months later, a new contributor onboarding, an Opus agent invoked for synthesis) reads the rationale and understands not just the decision but the reasoning. "We chose CC BY-SA 4.0" is not sufficient. "CC BY-SA 4.0 chosen because it permits derivatives and translations (rejected by ND), preserves attribution (required by mission), and prevents proprietary repackaging (rejected by share-alike)" is sufficient.

### 3.2 Rationale length norms

Rationale length is calibrated to decision weight:

| Category | Rationale norm |
|---|---|
| D-DOCT | 3–10 sentences. Captures the alternatives weighed and why this was chosen over them. |
| D-METH | 2–5 sentences. Captures the methodological principle the decision applies and the application context. |
| D-SCHEMA | 1–3 sentences. Captures the schema constraint and the round-trip / validation behaviour it preserves. |
| D-OP | 1 sentence. Captures the operational outcome. |
| D-PRES | 1–2 sentences. Captures the pattern conformance or departure. |

Rationale exceeding the norm is acceptable. Rationale below the norm is incomplete.

### 3.3 Rationale anti-patterns

Three rationale patterns are incomplete:

- **Tautology.** "Chose X because X is the right choice." No reasoning content.
- **Authority-without-content.** "Chose X because the spec says X." The spec citation should appear in `decision_artifacts`; the rationale should explain why X is what the spec says (or why the spec was followed in this case).
- **Outcome-as-rationale.** "Chose X because X." The rationale should explain the choice; the outcome field already records X.

### 3.4 What this is not

CS8 is not a "every minute decision needs a record" protocol. The five categories (§1) define the scope. A typing choice (`int` vs. `str` for a Pydantic field) is a schema implementation detail, not a Decision in the protocol's sense. A schema decision that survives review and codifies a pattern (e.g., "all enum-defaulted fields use string defaults to dodge the model_dump quirk") is a Decision. The discriminator: would a future agent need to read the rationale to understand why this is the way it is? If yes, it is a Decision. If no, it is implementation detail.

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
| `model_tier` | `opus`, `fable`, `sonnet`, `haiku`, `human` | Yes |
| `effort_level` | per `references/effort-guide.md`; `none` with `human` | Yes |
| `reasoning_modifier` | `synth`, `arbitrate`, `extract`, `format`, `route`, `none` | Yes |

**A tier names a class, never a version.** Write `opus`, not "Opus 4.6"; `sonnet`,
not "Sonnet 4.7". A version pin dates the moment it is written, and a rule pinned to
a retired number reads as excluding the model that replaced it — which is how a
routing floor silently becomes a routing ceiling. Any version number encountered in
model-routing text is stripped on touch (owner directive 2026-07-25; see
`DR-2026-07-25-rendered-document-integrity-gate` §3). `fable` is a synthesis-capable
tier alongside `opus`; `sonnet` and `haiku` are not.

Examples:

| Notation | Meaning |
|---|---|
| `opus/150/synth` | Opus-class, effort 150, reasoning modifier = best-practice synthesis |
| `fable/150/synth` | Fable-class, effort 150, reasoning modifier = best-practice synthesis |
| `opus/150/arbitrate` | Opus-class, effort 150, reasoning modifier = evidence arbitration between divergent positions |
| `sonnet/125/synth` | Sonnet-class, effort 125, reasoning modifier = synthesis (high-end Sonnet load; **not** best-practice synthesis) |
| `sonnet/100/route` | Sonnet-class, effort 100, reasoning modifier = workplan routing / orchestration |
| `sonnet/75/extract` | Sonnet-class, effort 75, reasoning modifier = single-pass extraction |
| `haiku/50/format` | Haiku-class, effort 50, reasoning modifier = mechanical format |
| `human/none/none` | Project owner decision; no model assigned |

### 4.3 Phase-table application

Every phase table that records model-routing uses this notation. Old notation forms ("Opus session", "Opus assigned", "best-practice synthesis", etc.) are deprecated — do not use them in new content.

### 4.4 Phase-level routing

A phase (e.g., A6 evidence-methodology, A12 decision-protocol) may have multiple decisions with different model-routing values. The phase's overall routing is recorded in its phase table using the same notation. Phases mostly run at one model-routing value; mixed-routing phases declare the routing per-deliverable.

---

## 5. Status

| Field | Value |
|---|---|
| Created | 2026-04-30 03:00 UTC |
| Phase | Stage A Phase 12 — Decision proxy and capture protocol — Session 1 |
| Status | CANONICAL |

### 5.1 Change log

| Date | Change |
|---|---|
| 2026-04-30 03:00 | Initial canonical version. Five categories, three delegation tiers, capture protocol, model-routing notation, register structure, CS8 activation, validator specification. |
| 2026-10-14 | Register (§5), CS8 activation (§6), validator (§7), the required-fields table and the decision-record notation deleted with the register (RULINGS R30, R47). |

---

**End of A12 governance document.**
