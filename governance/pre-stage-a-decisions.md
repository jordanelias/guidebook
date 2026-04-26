# Pre-Stage-A Doctrinal Decisions
**Created:** 2026-04-26 02:42 UTC
**Stage:** 0.5 (Pre-Stage-A doctrinal decisions)
**Decision authority:** Project owner
**Resolution principle:** Clean data + transparent methodology
**Resolves audit findings:** T-03, T-04, D-03 (all three Critical pre-Stage-A blockers per audit v2)
**Materials package:** `workplan/co0007-stage-0_5-decision-package.md` (committed `d4201b497b98`)

---

## Resolution principle

Decisions made under the criterion: **so long as we have clean data, transparent methodology.**

Applied operationally:
- **Clean data** = each fact in the corpus is verifiable; each evidence basis is identified; each cell's status is recorded
- **Transparent methodology** = the project declares what it actually does, not what it aspirationally claims to do, with the gap between the two visible

These principles map to all three decisions below.

---

## Decision T-03 · Co-1 tier encoding

### Resolution

**Option B: `tier` + `evidence_type` taxonomy.**

### Rationale

The 2026-04-24 23:46 doctrinal rule states Co-1 is "co-primary with Tier 1." Option A (single `tier` field with Co-1 as Tier-1 marker) flattens "co-primary" into "is-Tier-1" — semantically different claims. Option C (separate dimensions) preserves doctrinal fidelity but adds operational complexity without clear benefit at the schema layer.

**Option B is the encoding that says clearly what the doctrine says.** Two fields: `tier` (1–6) holds the clinical-evidence position; `evidence_type` (one of: `clinical`, `co1`, `co2`, `sr_meta`, `standard_evidence_based`, `national_framework`, `code`) holds the kind of evidence. Co-1 records have `tier: 1, evidence_type: co1`. Co-2 records have `tier: 2, evidence_type: co2`. The encoding preserves co-primary parallelism without flattening or doubling the schema.

This is the cleanest data structure that preserves the transparent methodology test: rendering can distinguish clinical-T1 from Co-1-T1 cleanly; validators read both fields; queries return what they should without inferring evidence type from tier alone.

### Affected downstream artifacts

- **B1 schema design** — entity records carry both `tier` and `evidence_type` fields
- **B2 evidence-tier-validator (Co-1-aware)** — reads both fields; enforces "best-practice claims must cite ≥Tier 3 OR Co-1 OR Co-2"
- **A6 evidence methodology** — specifies `evidence_type` taxonomy and authoring rules per type
- **C2 builds** — validators, renderers, authoring skills consult both fields

---

## Decision T-04 · Sparse-evidence behavior

### Resolution

**Hybrid: `[BEST-PRACTICE-PENDING]` marker as default; reduced-confidence (`provisional`) state when one evidence dimension is rich.**

### Rationale

The doctrine requires best practice to be evidence-derived. When evidence is genuinely sparse — sparse Tier 1–3 *and* sparse Co-1 — the honest answer is "we don't know yet." The `[BEST-PRACTICE-PENDING]` marker pairs with a research-gap pointer (cross-link to `gap_register.md`), making the absence visible and traceable rather than silent.

When evidence is sparse in one dimension but rich in another (e.g., strong Co-1 narrative for a population without clinical RCTs), the synthesis IS made, marked `provisional` with confidence flag, citing the rich dimension explicitly. This does not violate the doctrine — Co-1 is co-primary with Tier 1, so a strong Co-1-only synthesis is a legitimate evidence-based claim. The provisional flag tells readers what they're looking at.

**Doctrinal silence (Option C) was rejected** because silent intersections produce silent harm. Designers reading the guidebook conclude "no provision needed" rather than "evidence is thin." The audit v2 §T-04 yardstick (Cochrane practice distinguishing absence-of-evidence from evidence-of-absence from primary-non-clinical-tier evidence) supports the hybrid approach: each empirical state gets its own output.

This is the cleanest data because each cell records its own evidence state explicitly; this is transparent methodology because the synthesis declares its confidence and basis.

### Operational state machine

A best-practice cell at any (parameter × population) intersection holds one of:

| State | Display | Meaning | Validator behavior |
|---|---|---|---|
| `stated` | normal | Best practice derived from ≥Tier 3 OR Co-1 OR Co-2 evidence | Schema-validated; passes evidence-tier-validator |
| `provisional` | flagged with confidence | Synthesis based on partial evidence dimension; rich in at least one dimension | Schema-validated; renders with confidence flag |
| `pending` | `[BEST-PRACTICE-PENDING]` + gap link | Evidence sparse across all dimensions | Validator requires gap-register entry |
| `not_applicable` | "Not applicable" | Parameter has no design implication for this population | Validator requires explicit rationale |

### Affected downstream artifacts

- **A6 evidence methodology** — specifies the state machine and transitions
- **B1 schema** — `best_practice_status` field with the four states above
- **B2 validators** — enforce state machine; cross-check gap-register links for `pending`
- **C3 parameter migration** — every parameter records its state per population

---

## Decision D-03 · Co-1 operational role

### Resolution

**Operational Reviewer with documented Co-author trajectory clause.**

The project's current operational structure provides Co-1 review at key checkpoints. Co-1 *evidence* (the corpus of lived-experience research, confirmed advocacy positions, peer-reviewed Co-1 narratives) is co-primary with Tier 1 evidence. Co-1 *collaborators* (people) are currently engaged at the review level, not the drafting level.

This is declared honestly in mission language. The audit v2 §D-03 finding ("doctrine claims something the operational structure does not deliver") is resolved by **declaring the operational reality at mission level rather than papering it over**.

### Trajectory clause

Where DPO partnerships, dedicated funding, and per-collaborator compensation infrastructure can be secured, the project will expand Co-1 from review to drafting. Trigger conditions:

- ≥1 secured DPO partnership per priority population (initial set: MOB, VIS, DEAF, NDV, OFS)
- Per-collaborator compensation rates committed at meaningful scale (≥$X/hour or session — to be specified in A5)
- Authorship credit infrastructure operational (named co-author lines, contribution attribution)
- Decision-authority specification published (which decisions Co-1 collaborators have final authority over)

When triggers met for a given population, A5 phase tables update from Review to Drafting for that population. Until then, the Reviewer status is the operational reality.

### Why this is not the audit's "ambiguity" state

The audit identifies ambiguity as the unacceptable state. Ambiguity = doctrine claims X, operations deliver Y, neither is documented. This decision resolves to a documented operational reality (Reviewer) with documented expansion conditions (Co-author trajectory). Both states are documented; transitions are documented; the methodological limit is declared.

This is consistent with the audit's "either is defensible; ambiguity is not" framing.

### Rationale (clean data + transparent methodology applied)

- **Clean data:** Live state shows Co-1 evidence in the corpus (tier-JSON, BPC sources) but no Co-1 drafting of BPC sections. Declaring "Reviewer" matches verifiable state.
- **Transparent methodology:** Mission language declares the operational state. The CRPD Art. 4.3 commitment is preserved as the trajectory; current state is honestly described as not-yet-realizing-it. Project users and external critics can evaluate the methodology against what it claims.

### Affected downstream artifacts

- **0.6 mission language** — explicitly declares Reviewer as current state with trajectory clause
- **A1-A2 canonical mission** — refines language; possibly elevates trajectory triggers as binding commitments
- **A5 Co-1 co-author relationship phase** — produces operational specification under Reviewer state, with parallel drafting-mode specification activated by trigger conditions
- **B4 multi-pilot Co-1 role** — Reviewer at minimum (audit v2 §D-03 wording: "Drafting if recruitment supports; Decision at minimum")
- **C-stage phase tables** — show Co-1 role per phase; transitions logged

---

## Decision capture metadata

| Decision | Selection | Recommendation matched? |
|---|---|---|
| T-03 | Option B (`tier` + `evidence_type`) | Yes |
| T-04 | Hybrid (PENDING + provisional + not_applicable + stated) | Yes (hybrid Option D as recommended) |
| D-03 | Reviewer with Co-author trajectory clause | Resolution principle applied (transparency); not pre-committed to either pure Reviewer or pure Co-author |

| Field | Value |
|---|---|
| Decided | 2026-04-26 |
| Decision authority | Project owner |
| Resolution principle | Clean data + transparent methodology |
| Decision capture | This file |
| Materials reviewed | `workplan/co0007-stage-0_5-decision-package.md` |
| Cross-decision coherence | T-03 Option B and T-04 hybrid require `evidence_type` field which they share. T-04 provisional state and D-03 Reviewer-with-trajectory both depend on confidence-and-status flagging. The three decisions are mutually consistent under the resolution principle. |

---

## Audit-trail

- **T-03 (Co-1 tier encoding):** Audit v2 finding RESOLVED. Schema decision committed. B1/B2 implementation pending.
- **T-04 (Sparse-evidence behavior):** Audit v2 Critical finding RESOLVED. State machine specified. A6 implementation pending.
- **D-03 (Co-1 operational role):** Audit v2 Critical finding RESOLVED via transparency declaration. A5 / A1-A2 implementation pending.

All three pre-Stage-A blockers per audit v2 §Pre-adoption blockers section are now resolved.

---

## What this file does not do

- **Does not specify A5 in full.** A5 produces operational specification under the Reviewer state and parallel drafting-mode specification. Triggers are listed; the specification work itself is A5 content.
- **Does not commit mission language.** That is 0.6.
- **Does not implement the schema.** That is B1.
- **Does not build the validators.** That is C2.
- **Does not adopt workplan v3.** That is 0.9.

---

## Status

DECIDED. Adopted as the basis for 0.6 mission commit, 0.7 synthesis re-issue, A6 evidence methodology, A5 Co-1 specification, and B1/B2 architecture.
