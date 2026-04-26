# CO-0007 Workplan Adoption Decision
**Created:** 2026-04-26 03:30 UTC
**Stage:** 0.9 (Workplan adoption — Stage 0 closing gate)
**Decision authority:** Project owner
**Resolution principle:** Clean data + transparent methodology
**Closes:** Stage 0 (8 of 9 prior sub-phases committed; this file is the 9th)
**Materials reviewed:** `workplan/co0007-stage-0_9-adoption-package.md` (committed `9a536a64dd42`)
**Predecessor session:** `sessions/session_2026-04-26-co0007-stage0.md` (closed 2026-04-26 03:22 UTC)

---

## Selection

**Option B · Adopt workplan v3 with documented amendments — with C2 cut-list applied.**

Workplan v3 (`workplan/workplan-co0007-v3.md`, committed `3385209da72c`) is the operative structural plan. The paired amendments file (`workplan/workplan-co0007-v3-amendments.md`, this commit) records the seven budget and methodology adjustments Stage 0 surfaced (six committed initially; Amendment 7 added 2026-04-26 03:45 UTC under pre-launch operational correction). The combination — v3 + amendments — is the operative plan from this commit forward.

Rejected options:
- **Option A (adopt v3 as-is):** rejected because three explicit budget adjustments (C2, C7, salvage matrix) and two methodology refinements (A8 jurisdiction glossary, A13 contamination-sampling cadence) are known and would otherwise be silently absorbed. Audit B-01 surfaced silent compression as a recurring failure mode; carrying it forward defeats the audit's purpose.
- **Option C (re-issue as v5):** rejected as overkill. Workplan v3 is one day old. Six cell-level updates do not justify reissuing ~700 lines. Adopt-and-amend is the standard pattern for documents at this stage.

---

## Rationale

The Option B + cut-list combination satisfies the resolution principle on both axes:

**Clean data.** Each amendment traces to a specific Stage 0 finding with its source artifact:
- C7 budget revision traces to 0.2 §M2 quantitative verification (584 sources / 81 unverified residual; was 557/33).
- C2 budget revision traces to 0.3 skill inventory (75 skill-tasks; ~33 NEW skills required).
- C3 disposition track and salvage matrix trace to 0.4 contamination sample (0/13 evaluable BPCs frankly contaminated; corpus-state rebalance).
- A8 jurisdiction glossary traces to 0.2 §M5 (49 registered / 24 canonical / 46 prior synthesis cite — three undisambiguated denominators).
- A13 contamination-sampling cadence traces to 0.4 lessons-learned.

**Transparent methodology.** The adopted plan declares what it actually is — v3 plus seven amendments — rather than papering over the deltas. A future reader consults two files; the audit trail is intact. Amendment 7 (added 2026-04-26 03:45 UTC) is itself an application of the principle: the v3 + Amendments 1–6 adopted state described a Co-1 collaborator operational structure that did not exist; Amendment 7 corrects the framing to pre-launch solo authorship with post-launch collaboration as contingent possibility.

The C2 cut-list approach is selected over C2-full-build because it preserves the original 12–16 session range while honestly tracking deferral. The deferred renderers are mid-Stage-C concerns, not C2-blocking concerns — this is a sequencing choice, not a scope reduction.

---

## C2 Cut-List

C2 (skill-builds) constructs three renderer skills in C2 proper. Three additional renderers are deferred to mid-Stage-C, where their first consumers exist.

| Skill | C2 disposition | Rationale |
|---|---|---|
| `markdown-renderer` | **BUILD in C2** | Required for Stage-C content production; baseline output format |
| `questions-renderer` | **BUILD in C2** | Required for questions-led pedagogy per mission §6 (D-03 dependency) |
| `rendering-refresh-coordinator` | **BUILD in C2** | Required to keep generated outputs consistent during C-stage churn |
| `web-renderer` | **DEFER to mid-Stage-C** | First consumer is the public-facing surface; constructs against stable content, not C-stage drafts |
| `respect-visibility-renderer` | **DEFER to mid-Stage-C** | Co-1 visibility surfacing is meaningful only after parameter migration produces stable cell data |
| `navigation-mode-renderer` | **DEFER to mid-Stage-C** | Per audit v2 §T-02/D-01, navigation modes are a visible-product concern; constructed when content is sufficient to navigate |

**C2 budget under cut-list:** stays within original 12–16 session range. The three deferred skills add ~6–10 sessions when built mid-Stage-C, but those sessions are absorbed in the C-stage's existing C0–C11 cadence rather than added to C2.

**Cut-list trigger:** when the first parameter migration cohort completes in C3 and stable content exists for ≥1 navigation mode and ≥1 population's Co-1 cell set, mid-Stage-C unlocks construction of the deferred renderers. The trigger is recorded in C-stage progress logs.

---

## Budget impact (consolidated)

| Phase | Original | Adopted | Delta |
|---|---|---|---|
| C2 | 12–16 | 12–16 (with cut-list) | 0 |
| C7 | 12–17 | 15–22 | +3 to +5 |
| Mid-Stage-C (cut-list absorption) | implicit in C0–C11 | +6 to +10 absorbed | nominally +0; tracked |
| A5 (Amendment 7 — re-scoped) | 5–7 | 2–3 | -3 to -4 |
| CS2 (Amendment 7 — inoperative pre-launch) | recurring overhead | 0 | -0 to -3 |
| **Project total range** | 224–334 | **220–336** | **-4 to +2** |

Real-world months: the v3 binding range of 15–24 months was set by Co-1 cadence dominance. With Amendment 7's correction (pre-launch solo authorship), Co-1 cadence is no longer a binding constraint. The original 15–24 month range no longer applies on its original logic. **Re-budgeting is deferred until working rhythm is established.**

---

## Cross-references

- **Mission:** `governance/mission-PROVISIONAL.md` — adopted under the same resolution principle. Coda "sit-with ≥1 day" period operates against this file from 2026-04-26 03:22 UTC.
- **Pre-Stage-A doctrinal decisions:** `governance/pre-stage-a-decisions.md` — T-03, T-04, D-03 resolved.
- **Repo strategy:** `governance/repo-strategy.md` — committed Stage 0.8.
- **Synthesis re-issue v2:** `workplan/co0007-synthesis-workplan-2.md` — committed Stage 0.7.
- **Stage 0 materials package:** `workplan/co0007-stage-0_9-adoption-package.md` — this decision's input.
- **Amendments operative companion:** `workplan/workplan-co0007-v3-amendments.md` — paired with this file.

---

## Stage 0 done criteria — final

| Criterion | Status | Artifact |
|---|---|---|
| Live project state grounded | ✓ | `workplan/co0007-session-grounding-report.md` (0.1) |
| Quantitative claims verified | ✓ | `workplan/co0007-quantitative-verification.md` (0.2) |
| Current skill set inventoried | ✓ | `workplan/co0007-skill-inventory.md` (0.3) |
| Contamination ratio estimated | ✓ | `workplan/co0007-contamination-sample.md` (0.4) |
| Three Critical doctrinal decisions made | ✓ | `governance/pre-stage-a-decisions.md` (0.5) |
| Mission committed PROVISIONAL | ✓ | `governance/mission-PROVISIONAL.md` (0.6) |
| Synthesis re-issued | ✓ | `workplan/co0007-synthesis-workplan-2.md` (0.7) |
| Repo strategy decided | ✓ | `governance/repo-strategy.md` (0.8) |
| Workplan adopted | **✓ this file** | `governance/workplan-adoption.md` (0.9) |

**Stage 0: COMPLETE.**

---

## Stage A unblock conditions

Stage A (A1-A2 Audience + Mission canonical, merged per audit L-07) is gated by two independent conditions, both of which must be met:

1. **Stage 0 closed** — met as of this commit.
2. **Mission sit-with elapsed** — Coda's "sit with the mission ≥1 day before adopting" test runs against `governance/mission-PROVISIONAL.md`. Sit-with period began at predecessor session close (2026-04-26 03:22 UTC). Earliest defensible Stage A start: **2026-04-27 03:22 UTC**.

Until both conditions are met, no Stage A phase may begin.

---

## What this commit does not do

- **Does not start Stage A.** A1-A2 begins in a separate session, after the sit-with elapses. Project owner triggers it.
- **Does not canonicalize the mission.** A1-A2 produces the canonical mission. `mission-PROVISIONAL.md` is the artifact under sit-with.
- **Does not produce a roadmap document.** Per 0.7 disposition note, roadmap-2 is deferred. If the project owner wants a separate roadmap, request triggers a session keyed to v3 + amendments.
- **Does not commit `co0007-audit-2.md`.** Optional re-upload per project-owner discretion; not required for Stage A unblock since v3+amendments supersedes the audit's recommendations operationally.

---

## Status

DECIDED. Adopted as the operative plan, paired with `workplan/workplan-co0007-v3-amendments.md`.

| Field | Value |
|---|---|
| Decided | 2026-04-26 03:30 UTC |
| Decision authority | Project owner |
| Selection | Option B + C2 cut-list |
| Resolution principle | Clean data + transparent methodology |
| Stage 0 status | CLOSED (9 of 9 sub-phases committed) |
| Stage A status | GATED on mission sit-with (≥2026-04-27 03:22 UTC) |
| Operative plan | `workplan/workplan-co0007-v3.md` + `workplan/workplan-co0007-v3-amendments.md` |


---

## Waiver record — Mission sit-with (2026-04-26 03:35 UTC)

**Status:** WAIVED by project owner direction.

The Coda's "sit with the mission ≥1 day before adopting" period — declared in the Stage A unblock conditions above as gating until 2026-04-27 03:22 UTC — has been waived. Project owner directed proceeding to Stage A immediately following Stage 0 close.

**Operational consequence:**
- Stage A is unblocked from this entry forward.
- `governance/mission-PROVISIONAL.md` retains its PROVISIONAL status until A1-A2 produces the canonical `governance/mission-and-epistemics.md`.
- The reflective-period methodology declared in the synthesis Coda is documented as not exercised for this transition.

**Rationale captured:** project-owner discretion; no sub-rationale recorded at waiver time.

**Test against mission integrity:** A1-A2 will canonicalize the mission. Any drift from `mission-PROVISIONAL.md` doctrinal commitments will be visible in the canonical version's diff against this file. The sit-with waiver does not bypass that diff visibility.

| Field | Value |
|---|---|
| Waived | 2026-04-26 03:35 UTC |
| Waiver authority | Project owner |
| Original gate | Mission sit-with ≥2026-04-27 03:22 UTC |
| Stage A status as of waiver | UNBLOCKED |
| Doctrinal commitments | Carry forward to A1-A2 canonical version |
