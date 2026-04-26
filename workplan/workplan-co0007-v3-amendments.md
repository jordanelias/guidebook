# Workplan CO-0007 v3 — Amendments
**Created:** 2026-04-26 03:30 UTC
**Stage:** 0.9 (Workplan adoption)
**Status:** OPERATIVE — paired with `workplan/workplan-co0007-v3.md`
**Adoption record:** `governance/workplan-adoption.md` (Option B + C2 cut-list)
**Resolution principle:** Clean data + transparent methodology

---

## Reading order

This file is **not** a standalone workplan. It is the operative companion to `workplan/workplan-co0007-v3.md`. Where a cell in v3 conflicts with a cell here, **this file governs**. Where v3 is silent, v3 governs (no inference).

The six amendments are cell-level updates, not architectural rewrites. Phase structure (A1–A13, B1–B7, C0–C11) is unchanged.

---

## Amendment 1 · C7 session budget

| Field | v3 value | Amended value |
|---|---|---|
| C7 session budget | 12–17 sessions | **15–22 sessions** |

**Source:** `workplan/co0007-quantitative-verification.md` §M2 (Stage 0.2).

**Rationale:** Stage 0.2 verification found bibliography count is **584 sources / 86% verified / 81 unverified residual**, not the 557/94%/33 that synthesis v1 claimed. The unverified residual scope drives C7 (citation-tagging completion), and the residual scaled by ~2.5×. Compressing the budget into the original 12–17 range would silently absorb the scope increase — exactly the failure mode audit B-01 was designed to surface.

The 15–22 range covers:
- Lower bound (15): if remaining 81 verifications proceed at the average rate observed in the citation-tagger Sessions 1–3 logged in `gap_register.md` (GAP-CITE-01).
- Upper bound (22): if a residual subset requires deep-source recovery (DOI hunt, edition disambiguation, interlibrary recovery for older Tier-3 sources).

**Project-total impact:** +3 to +5 sessions.

---

## Amendment 2 · C2 session budget — with C2 cut-list

| Field | v3 value | Amended value |
|---|---|---|
| C2 session budget | 12–16 sessions | **12–16 sessions (with cut-list applied)** |
| C2 scope | "build all NEW skills required for C-stage operation" | "build the three C2-blocking renderers; defer three to mid-Stage-C" |

**Source:** `workplan/co0007-skill-inventory.md` (Stage 0.3).

**Rationale:** Stage 0.3 identified ~33 NEW skills required to operationalize §C2 of v3. C2-full-build would extend the budget to 20–28 sessions (+8 to +12). The cut-list approach defers three renderer skills to mid-Stage-C, where their first consumers exist, keeping C2 within the original 12–16 range.

### C2 cut-list

**BUILD in C2 proper:**

| Skill | C2 priority | Justification |
|---|---|---|
| `markdown-renderer` | P0 | Required for Stage-C content production; baseline output format |
| `questions-renderer` | P0 | Required for questions-led pedagogy per `mission-PROVISIONAL.md` §6 |
| `rendering-refresh-coordinator` | P0 | Required to keep generated outputs consistent during C-stage parameter migration churn |

**DEFER to mid-Stage-C:**

| Skill | First consumer | Trigger condition |
|---|---|---|
| `web-renderer` | Public-facing surface | Stable content exists for ≥1 navigation mode |
| `respect-visibility-renderer` | Co-1 cell-data display | Parameter migration produces stable Co-1 evidence_type cell data for ≥1 population |
| `navigation-mode-renderer` | Reader-facing modes | Parameter migration produces sufficient content to navigate via ≥1 non-default mode |

**Cut-list audit-trail requirement:** when each deferred renderer is built mid-Stage-C, the build session must log (a) the trigger condition that fired, (b) the C-stage phase in which construction occurred, and (c) the absorbed-into-C-stage-budget cost.

**Project-total impact:** 0 sessions in C2; +6 to +10 absorbed within C0–C11 cadence (tracked but not added).

---

## Amendment 3 · C3 task structure

| Field | v3 value | Amended value |
|---|---|---|
| C3 per-parameter task structure | "Each parameter migrated independently" | "Each parameter migrated independently AND assigned an explicit disposition track: STUB / MERGED / AMBIGUOUS / CLEAN" |

**Source:** `workplan/co0007-contamination-sample.md` §F3 (Stage 0.4).

**Rationale:** Stage 0.4's N=15 contamination sample surfaced four corpus states, not the binary clean/contaminated split synthesis v1 implied:

- **CLEAN** (~78% of evaluable BPCs): doctrinally aligned; migrate parameter-by-parameter as v3 specifies
- **AMBIGUOUS** (~7% of evaluable BPCs): Tier-5-only derivations or self-flagged PROVISIONAL; migration requires confidence-flag review per amended schema (Decision T-04 `provisional` state)
- **STUB** (~7%): synthesis pending Opus pass; migration blocked until Opus refresh
- **MERGED** (~7%): CO-0006 redirect files; migration requires resolving redirect target before parameter pass

C3 must record disposition per BPC at session entry, not infer it. The disposition track determines migration path:

| Disposition | C3 path | Validator behavior |
|---|---|---|
| CLEAN | Standard parameter migration | Schema-validated; passes evidence-tier-validator |
| AMBIGUOUS | Migration with `provisional` flag per population × parameter cell | Validator records confidence; passes if flag is honest |
| STUB | Routed to Opus refresh queue before C3 migration | Migration blocked; tracked in queue |
| MERGED | Redirect-target resolved first; parameter migration follows from resolved target | Migration blocked; tracked separately |

**Project-total impact:** 0 sessions added (the disposition-track work is operational discipline within existing C3 budget); migration sequencing changes per-BPC.

---

## Amendment 4 · Salvage matrix

| Field | v3 value | Amended value |
|---|---|---|
| BPC salvage classification | "BPC `best_practice_synthesis` fields where contamination sample shows clean: Reusable conditionally" | "≥92% Fully reusable; ~8% Reusable conditionally; ~7% Pending Opus; ~7% Redirect" |

**Source:** `workplan/co0007-contamination-sample.md` (Stage 0.4) — N=15, 0/13 evaluable BPCs frankly contaminated.

**Rationale:** Audit v2 hypothesized widespread BPC contamination requiring extensive rebuild. Stage 0.4 sampling did not support the hypothesis. The salvage scope is dominated by reuse, not rebuild. The four-state classification (Fully reusable / Reusable conditionally / Pending Opus / Redirect) replaces the binary salvage-vs-rebuild assumption that drove parts of v3's C3 budgeting.

**Operational consequence:** C3 effort distribution shifts from "rebuild-heavy" to "migrate-heavy." The disposition-track requirement (Amendment 3) is the operational enforcement of this shift.

**Project-total impact:** 0 sessions added directly; effort redistribution within C3 budget. Net effect on C3 timeline is neutral-to-favorable (migration is faster than rebuild per BPC; the limiting factor is Opus refresh queue throughput for STUB items).

---

## Amendment 5 · A8 jurisdiction-philosophy scope

| Field | v3 value | Amended value |
|---|---|---|
| A8 scope | "Worldview as first-class entity. 24-vs-46 inconsistency resolved" | "Worldview as first-class entity. 24-vs-46 inconsistency resolved. **Plus: define glossary distinguishing registered standards (49) vs canonical research coverage (24) vs prior synthesis cite (46) — three undisambiguated denominators**" |

**Source:** `workplan/co0007-quantitative-verification.md` §M5 (Stage 0.2).

**Rationale:** Stage 0.2 surfaced three jurisdictional denominators in current project state, each measuring something different:

| Denominator | Count | What it measures |
|---|---|---|
| Registered standards | 49 | Standards documents formally registered in the project's standards-registry |
| Canonical research coverage | 24 | Jurisdictions for which the project has done canonical (deep) evidence research |
| Prior synthesis cite | 46 | Jurisdictions cited at least once in prior synthesis documents |

Conflating these three produces incoherent claims (e.g., "the guidebook covers 24 jurisdictions" vs "the guidebook references 46 jurisdictions" vs "49 standards are registered"). A8 must produce the glossary distinguishing the three and specify which denominator is operative for which downstream claim.

**Project-total impact:** 0 sessions added. Glossary work is absorbed within A8's existing scope.

---

## Amendment 6 · A13 doctrine-recheck cadence

| Field | v3 value | Amended value |
|---|---|---|
| A13 scope | "Periodic operational audit cadence" | "Periodic operational audit cadence. **Plus: contamination-sampling methodology from 0.4 as a recheck procedure (every N sessions or at stage transition, sample N≥15 BPCs and re-classify)**" |

**Source:** `workplan/co0007-contamination-sample.md` lessons-learned (Stage 0.4).

**Rationale:** Stage 0.4 demonstrated that a 15-BPC sample with explicit classification rubric (frankly contaminated / ambiguous / aligned-but-thin / EXEMPLARY / etc.) produced actionable corpus-state intelligence in a single session. Embedding this as a recheck procedure within A13 gives the project an early-warning instrument against doctrinal drift — the same instrument audit v2 wished it had had earlier.

**Recheck cadence (provisional, A13 finalizes):**

| Trigger | Sample size | Output |
|---|---|---|
| Every 25 working sessions | N≥15 BPCs | Re-classification + drift report |
| At stage transition (A→B, B→C) | N≥15 BPCs | Pre-transition baseline classification |
| On request (doctrinal-rule revision) | N≥15 BPCs | Targeted classification against revised rule |

**Project-total impact:** absorbed within A13's existing scope; rechecks themselves cost ~1 session each, paid for by the early-warning value of catching drift before it accumulates.

---

## Amendment 7 · Co-1 collaborator framing — pre-launch solo reality

| Field | v3 value | Amended value |
|---|---|---|
| Co-1 operational role across A1-A2, A4, A5, B4, B6 | "Reviewer," "Drafting if recruitment supports," recruitment thread, with triggers | **Pre-launch: inoperative — no Co-1 collaborators exist.** Co-1 *evidence* engagement through published corpus only. **Post-launch contingent**, may never activate. |
| A5 scope and budget | "Co-1 co-author relationship — operational specification + recruitment thread · 5–7 sessions for design; recruitment is parallel cross-stage thread" | Pre-launch: A5 produces design specification for post-launch collaborative form (a how-it-would-work document) · **~2–3 sessions**. Recruitment thread does not run pre-launch. |
| CS2 (Co-1 recruitment thread) | "Active from A5 forward. Gates C4 per population." | **Inoperative pre-launch.** Activates only if launch + resources occur. C4 per-population gating becomes per-launch-state, not per-population. |
| CS5 (Co-1 representation monitoring) | "Dashboard updated as corpus grows. Drift triggers recruitment." | Re-scoped to **corpus-representation monitoring** (is the evidence base drawing from a sufficiently broad range of disabled voices?), distinct from collaborator-representation monitoring. Drift triggers expanded literature search, not recruitment. |
| B6 (pilot validation against mission) | "4–5 sessions" | Solo-author cross-checking against committed mission language, not external Co-1 review. Validation rigor is correspondingly weaker; **declared in mission §6**, not budgetarily compensated. |
| B4 multi-pilot construction Co-1 role | "Drafting if recruitment supports; Decision at minimum" | Solo authorship engaging the published Co-1 corpus. No Co-1 collaborator role pre-launch. |

**Source:** Project-owner correction 2026-04-26 03:35–03:45 UTC; new RULE in `references/project-standards.md` 2026-04-26 03:45 UTC; revised D-03 in `governance/pre-stage-a-decisions.md`.

**Rationale:** Workplan v3 was authored under the assumption that the project has a current operational structure (Co-1 collaborators at Reviewer level) with pending triggers for Drafting-state expansion. That structure does not exist. The project is pre-launch and authored by one person. Co-1 *evidence* is engaged through the published corpus — peer-reviewed lived-experience research, DPO position papers, named advocacy organizational positions, Co-1-authored academic narratives. There are no Co-1 collaborator panels, no DPO partnerships, no recruitment thread, no compensation infrastructure. There is no Reviewer state. There is no Drafting state. There are no triggers. Post-launch collaboration is contingent and may never occur. **Solo-only-permanent is a possible end-state.**

The Co-1 *evidence* commitment (co-primary with Tier 1 per the seven-tier hierarchy) is unaffected. That is a methodology commitment about evidence types, valid regardless of solo-vs-team production. T-03 (`tier` + `evidence_type` encoding) and T-04 (sparse-evidence state machine) — both about evidence — remain in effect unchanged.

**What changes operationally:**
- A5 becomes a 2–3 session design exercise: specify the post-launch collaborative form as a contingency document (how it would work *if* activated), not as an operational specification of current state. The design itself is solo authorship informed by Co-1 evidence on participatory design practice (CRPD Art. 4.3 implementation literature, named DPO position papers on co-design models).
- A1-A2 produces canonical mission and audience priority documents *as solo work*, with the partial-Art-4.3-honoring limit declared in mission language (per revised mission-PROVISIONAL §3 and the Test §5 update).
- B4/B6 pilots are solo-authored, validated by solo cross-checking against committed mission. Validation rigor is weaker than external Co-1 review would provide; this is a declared methodological limit, not a budget cost.
- CS2 and the recruitment-thread coordination overhead drop out pre-launch entirely.
- CS5 re-scopes to corpus diversity monitoring (an evidence-base question) rather than collaborator-pool monitoring (a participation question that doesn't apply pre-launch).

**Project-total budget impact:** The binding constraint changes. v3 had Co-1 cadence (review windows, DPO recruitment timing, collaborator scheduling) as the binding real-world constraint. With no Co-1 cadence to bind to, single-author pace becomes the binding constraint. Session-count savings: A5 reduces by 3–4 sessions; CS2 coordination overhead drops out (estimated ~0–3 sessions across the project); B6 budget is unchanged in session count but rigor cost is non-budgetary and declared. Net session-count delta: **-3 to -7 sessions** (savings from removed-fictional-coordination overhead). Combined with Amendments 1–6, project total range becomes **220–336 sessions** (was 227–339 under Amendments 1–6 alone; was 224–334 in v3 baseline).

**Real-world months:** the v3 binding range of 15–24 months was set by Co-1 cadence dominance. With Co-1 cadence removed, the binding constraint is the single author's working pace and external research access. The 15–24 month range no longer applies on its original logic. **Re-budgeting is deferred** — pace estimation under solo authorship is not reliably derivable from current materials and is left for a future amendment when working rhythm is established.

**What Amendment 7 does NOT do:**
- Does not change v3's phase structure (A1-A13, B1-B7, C0-C11). Phases remain.
- Does not delete A5. A5 is re-scoped, not removed.
- Does not commit a fictional "post-launch will happen" plan. Post-launch is contingent and may never activate.
- Does not substitute solo synthesis for Co-1 evidence engagement. The published Co-1 corpus is engaged at evidence level throughout.

---

## Consolidated budget impact

| Stage / Phase | v3 budget | Amended budget | Delta |
|---|---|---|---|
| C2 (with cut-list) | 12–16 | 12–16 | 0 |
| C7 | 12–17 | **15–22** | **+3 to +5** |
| Mid-Stage-C (cut-list absorption) | implicit | +6 to +10 absorbed | tracked, not added |
| C3 (disposition tracks) | as-is | as-is | 0 (within-scope operational discipline) |
| A8 (glossary) | as-is | as-is | 0 (within-scope) |
| A13 (recheck) | as-is | as-is | 0 (within-scope; rechecks paid by drift-detection value) |
| A5 (Amendment 7 — re-scoped) | 5–7 | **2–3** | **-3 to -4** |
| CS2 (Amendment 7 — inoperative pre-launch) | recurring overhead | 0 pre-launch | **-0 to -3** (estimated) |
| B6 (Amendment 7 — solo cross-check) | 4–5 | 4–5 | 0 (rigor cost non-budgetary) |
| **Project total** | 224–334 | **220–336** | **-4 to +2** |

Real-world months: the v3 binding range of 15–24 months was set by Co-1 cadence dominance. With Amendment 7's removal of Co-1 cadence, the binding constraint shifts to single-author pace. **The 15–24 month range no longer applies on its original logic and is not re-stated here.** Re-budgeting is deferred until working rhythm is established.

---

## Cross-references

- **Adoption record:** `governance/workplan-adoption.md`
- **Operative companion:** `workplan/workplan-co0007-v3.md`
- **Mission (sit-with):** `governance/mission-PROVISIONAL.md`
- **Pre-Stage-A doctrinal decisions:** `governance/pre-stage-a-decisions.md`
- **Stage 0 source artifacts (per amendment):**
  - Amendment 1 → `workplan/co0007-quantitative-verification.md` §M2
  - Amendment 2 → `workplan/co0007-skill-inventory.md`
  - Amendment 3 → `workplan/co0007-contamination-sample.md` §F3
  - Amendment 4 → `workplan/co0007-contamination-sample.md`
  - Amendment 5 → `workplan/co0007-quantitative-verification.md` §M5
  - Amendment 6 → `workplan/co0007-contamination-sample.md` lessons-learned
  - Amendment 7 → project-owner correction 2026-04-26 03:35–03:45 UTC; new RULE in `references/project-standards.md` 2026-04-26 03:45 UTC; revised D-03 in `governance/pre-stage-a-decisions.md`

---

## What this file does not do

- **Does not supersede v3.** v3 remains the structural plan. This file amends specific cells.
- **Does not re-issue as v5.** v5 issuance was rejected at 0.9 in favor of adopt-and-amend.
- **Does not pre-empt the mission sit-with.** Sit-with was WAIVED 2026-04-26 03:35 UTC by project owner (recorded in `governance/workplan-adoption.md`).
- **Does not implement the amendments.** Implementation occurs in the named phases (A1-A2, A5, A8, A13, B4, B6, C2, C3, C7) and cross-stage threads (CS2, CS5). This file specifies what those phases must deliver.

---

## Status

OPERATIVE. v3 + this file = the operative CO-0007 plan from this commit forward.

| Field | Value |
|---|---|
| Adopted | 2026-04-26 03:30 UTC; Amendment 7 added 2026-04-26 03:45 UTC |
| Adoption record | `governance/workplan-adoption.md` |
| Operative pair | `workplan/workplan-co0007-v3.md` (this file's companion) |
| Amendment count | **7** (cell-level; phase structure unchanged) |
| Net session impact | **-4 to +2 sessions** (project total **220–336**); was +3 to +5 under Amendments 1–6 alone |
| Real-world impact | binding constraint shifted from Co-1 cadence to single-author pace; original 15–24 month range no longer applies; re-budgeting deferred |
| Resolution principle | Clean data + transparent methodology |
| Operational frame | Pre-launch solo synthesis; post-launch collaboration contingent and may never occur |
