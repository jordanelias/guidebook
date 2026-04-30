# Pre-Stage-A Doctrinal Decisions
**Status:** CANONICAL — retroactively marked at A12 S2 finding RC-001 resolution (2026-04-30)
**Created:** 2026-04-26 02:42 UTC; **D-03 revised:** 2026-04-26 03:45 UTC
**Stage:** 0.5 (Pre-Stage-A doctrinal decisions)
**Decision authority:** Project owner
**Resolution principle:** Clean data + transparent methodology
**Resolves audit findings:** T-03, T-04, D-03 (all three Critical pre-Stage-A blockers per audit v2)
**Materials package:** `workplan/co0007-stage-0_5-decision-package.md` (committed `d4201b497b98`)

---

## Revision note (2026-04-26 03:45 UTC)

**D-03 is revised in this file.** The original D-03 resolution ("Operational Reviewer with documented Co-author trajectory clause") presupposed an operational structure — Co-1 collaborators engaged at review level, with triggers for Drafting upgrade. That structure does not exist. The project is pre-launch and solo. The original resolution described a fiction. The revised resolution is below; the original is preserved at the end of the D-03 section as audit trail.

**T-03 and T-04 are unchanged.** Both are decisions about evidence types and evidence states — not about operational structures. Their validity does not depend on whether collaborators exist.

---

## Resolution principle

Decisions made under the criterion: **so long as we have clean data, transparent methodology.**

Applied operationally:
- **Clean data** = each fact in the corpus is verifiable; each evidence basis is identified; each cell's status is recorded
- **Transparent methodology** = the project declares what it actually does, not what it aspirationally claims to do, with the gap between the two visible

These principles map to all three decisions below. The 2026-04-26 03:45 D-03 revision is itself an application of the principle: the original D-03 violated transparent methodology by describing a non-existent operational structure as if it were a current state with pending triggers.

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

### Status

DECIDED. Unchanged by 2026-04-26 03:45 revision (this decision is about evidence types, not operational structure).

---

## Decision T-04 · Sparse-evidence behavior

### Resolution

**Hybrid: `[BEST-PRACTICE-PENDING]` marker as default; reduced-confidence (`provisional`) state when one evidence dimension is rich.**

### Rationale

The doctrine requires best practice to be evidence-derived. When evidence is genuinely sparse — sparse Tier 1–3 *and* sparse Co-1 — the honest answer is "we don't know yet." The `[BEST-PRACTICE-PENDING]` marker pairs with a research-gap pointer (cross-link to `gap_register.md`), making the absence visible and traceable rather than silent.

When evidence is sparse in one dimension but rich in another (e.g., strong Co-1 narrative for a population without clinical RCTs), the synthesis IS made, marked `provisional` with confidence flag, citing the rich dimension explicitly. This does not violate the doctrine — Co-1 is co-primary with Tier 1 *as evidence*, so a strong Co-1-only synthesis is a legitimate evidence-based claim. The provisional flag tells readers what they're looking at.

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

### Status

DECIDED. Unchanged by 2026-04-26 03:45 revision (this decision is about evidence states, not operational structure).

---

## Decision D-03 · Co-1 operational role (REVISED 2026-04-26 03:45 UTC)

### Resolution (revised)

**Pre-launch: solo authorship; Co-1 engaged at evidence level only (published corpus). Post-launch (contingent): collaborative form co-designed with disabled people if and when launch and resources occur. Solo-only-permanent is a possible end-state.**

### Why the original framing failed

The audit v2 §D-03 finding diagnosed a "doctrine claims X, operations deliver Y" gap. The original D-03 resolution accepted that framing and tried to bridge it with trigger conditions (DPO partnerships, compensation infrastructure, named co-author lines, decision-authority specification). That implementation presupposed an operational structure to evaluate — Co-1 collaborators engaged at some level, with the level adjustable via triggers.

That presupposition was wrong. There is no operational structure pre-launch. There is no project yet for anyone to be a collaborator in. The original "Reviewer with trajectory" framing described a fictional Reviewer state and fictional triggers that could not fire because there was nothing for them to fire into.

The honest framing: **pre-launch is methodology development (solo); post-launch is methodology activation (participatory if feasible). The two phases are not bridged by triggers — they are bridged by launch itself.** Whether launch occurs at all is contingent. Whether resources support participatory production after launch is contingent. The project must hold integrity in the case where neither condition is met.

### Pre-launch operational reality

The project is currently authored by a single person. Co-1 *evidence* is engaged through the published corpus only:

- Peer-reviewed lived-experience literature
- Confirmed Co-1 advocacy positions from named organizations
- Co-1-authored academic narratives and DPO research outputs

This is evidence-level engagement, not participation-level engagement. There are no Co-1 collaborator panels, no DPO partnerships, no recruitment thread, no compensation infrastructure. There is no Reviewer state. There is no Drafting state. There is no transition between them. There are no triggers.

### Post-launch contingency

If the project launches and resources permit, the *form* of collaboration with disabled people becomes a co-design question — to be answered with disabled people, not for them. Specifying that form pre-launch, in the absence of participants, would reproduce the substantive problem CRPD Art. 4.3 exists to address.

The commitment is therefore: post-launch, *if* feasible, the collaborative form is co-designed with the people it concerns. A5 produces a design specification for that post-launch form (a how-it-would-work document) — not a recruitment thread, not a current operational specification, just a design that activates if and when conditions allow. This may never activate. **Solo-only-permanent is a possible end-state.**

### CRPD Art. 4.3 honoring (revised)

CRPD Art. 4.3 is the participation principle: meaningful participation of disabled people in policies and decisions affecting them. Pre-launch, the project honors Art. 4.3 in the available form — engagement with a Co-1 evidence corpus that was itself produced through participatory processes, treating that corpus as co-primary with Tier 1, never substituting non-disabled-derived evidence for Co-1 evidence where Co-1 evidence speaks.

This is **partial honoring**. Full Art. 4.3 honoring requires participation in the synthesis, not just engagement with the corpus. That requires people. Until launch and resourcing produce people, full Art. 4.3 honoring is not realised.

The project declares this honestly: pre-launch is partial Art. 4.3 honoring at the evidence level; full participatory honoring is contingent on launch occurring and resources being available, and may never be realised.

### Affected downstream artifacts

- **`governance/mission-PROVISIONAL.md`** — §3 revised with operational-reality replacement and post-launch contingency
- **A1-A2 (canonical mission and audience)** — produced solo from current corpus; CRPD Art. 4.3 partial-honoring declared in canonical mission language
- **A5 (Co-1 co-author relationship)** — re-scoped per Amendment 7 in `workplan/workplan-co0007-v3-amendments.md`: pre-launch produces post-launch collaboration model design (~2–3 sessions); recruitment thread is post-launch only and may never run
- **B4 multi-pilot construction** — Co-1-role cells inoperative pre-launch; pilot construction is solo authorship engaging the published Co-1 corpus
- **B6 pilot validation** — solo-author cross-checking against committed mission language; weaker rigor than external Co-1 review; declared in mission §6
- **CS2 (cross-stage Co-1 recruitment thread)** — null pre-launch; activates only if launch + resources occur
- **CS5 (Co-1 representation monitoring)** — re-scoped to corpus-representation monitoring (is the evidence base drawing from a sufficiently broad range of disabled voices?), distinct from collaborator-representation monitoring
- **C-stage phase tables** — collaborator-role columns inoperative pre-launch; corpus-evidence-engagement columns operate

### Rationale (clean data + transparent methodology applied)

- **Clean data:** Live state shows Co-1 evidence in the corpus (tier-JSON, BPC sources). Live state shows zero Co-1 collaborators. Declaring "pre-launch solo" matches verifiable state. Declaring "post-launch contingent" matches the actual decision space.
- **Transparent methodology:** The original D-03 violated this principle by describing a non-existent operational structure with pending triggers. The revised D-03 declares solo authorship as the operational state, post-launch collaboration as a contingent possibility, and solo-only-permanent as a defensible end-state. The project's claim to honor Art. 4.3 is calibrated honestly: partial pre-launch, full only if launched-and-resourced, possibly never full.

### Status

DECIDED (revised 2026-04-26 03:45 UTC). The original "Reviewer with trajectory" framing is SUPERSEDED.

### Audit-trail — original resolution (preserved for record)

The original D-03 resolution committed 2026-04-26 02:42 UTC stated:

> Operational Reviewer with documented Co-author trajectory clause.
>
> The project's current operational structure provides Co-1 review at key checkpoints. Co-1 *evidence* (the corpus of lived-experience research, confirmed advocacy positions, peer-reviewed Co-1 narratives) is co-primary with Tier 1 evidence. Co-1 *collaborators* (people) are currently engaged at the review level, not the drafting level.
>
> Trigger conditions for expanding Co-1 from review to drafting:
> - ≥1 secured DPO partnership per priority population (initial set: MOB, VIS, DEAF, NDV, OFS)
> - Per-collaborator compensation rates committed at meaningful scale
> - Authorship credit infrastructure operational
> - Decision-authority specification published
>
> When triggers met for a given population, A5 phase tables update from Review to Drafting for that population.

This original resolution is preserved as audit trail. It is **no longer operative**. It described a structure that did not exist. The revised resolution above replaces it.

---

## Decision capture metadata

| Decision | Selection | Recommendation matched? | Status |
|---|---|---|---|
| T-03 | Option B (`tier` + `evidence_type`) | Yes | DECIDED — unchanged |
| T-04 | Hybrid (PENDING + provisional + not_applicable + stated) | Yes (hybrid Option D as recommended) | DECIDED — unchanged |
| D-03 | Pre-launch solo; post-launch contingent; solo-only-permanent acknowledged as possible end-state | Resolution principle re-applied to corrected premises | DECIDED — REVISED 2026-04-26 03:45 |

| Field | Value |
|---|---|
| Decided | 2026-04-26 (T-03, T-04); 2026-04-26 03:45 (D-03 revised) |
| Decision authority | Project owner |
| Resolution principle | Clean data + transparent methodology |
| Decision capture | This file |
| Materials reviewed | `workplan/co0007-stage-0_5-decision-package.md` |
| Cross-decision coherence | T-03 Option B and T-04 hybrid require `evidence_type` field which they share. T-04 provisional state and revised D-03 are mutually consistent: pre-launch solo synthesis from Co-1 corpus produces `provisional`-flagged cells where Co-1 narrative is the only available dimension. The three decisions are mutually consistent under the resolution principle. |

---

## Audit-trail

- **T-03 (Co-1 tier encoding):** Audit v2 finding RESOLVED. Schema decision committed. B1/B2 implementation pending.
- **T-04 (Sparse-evidence behavior):** Audit v2 Critical finding RESOLVED. State machine specified. A6 implementation pending.
- **D-03 (Co-1 operational role):** Audit v2 Critical finding RESOLVED via transparency declaration of pre-launch solo reality. Original "Reviewer with trajectory" framing superseded; original framing preserved as audit trail above. A5 / A1-A2 implementation pending under revised framing.

All three pre-Stage-A blockers per audit v2 §Pre-adoption blockers section remain resolved under the revised D-03.

---

## What this file does not do

- **Does not specify A5 in full.** A5 produces post-launch collaborative form design (re-scoped per Amendment 7); the specification work itself is A5 content.
- **Does not commit mission language.** That is 0.6.
- **Does not implement the schema.** That is B1.
- **Does not build the validators.** That is C2.
- **Does not adopt workplan v3.** That is 0.9 (committed `0d72b35b`).
- **Does not pretend collaborator structures exist.** Pre-launch solo is the operational reality.

---

## Status

DECIDED (T-03, T-04 unchanged; D-03 revised 2026-04-26 03:45 UTC). Adopted as the basis for 0.6 mission commit, 0.7 synthesis re-issue, A6 evidence methodology, A5 design-only Co-1 specification, and B1/B2 architecture.
