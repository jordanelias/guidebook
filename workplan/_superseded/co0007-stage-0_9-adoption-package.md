# CO-0007 Stage 0.9 — Workplan Adoption Decision Package
**Created:** 2026-04-26 03:18 UTC
**Stage:** 0.9 (Workplan adoption)
**Decision authority:** Project owner
**Inputs reviewed:** All Stage 0.1–0.8 outputs

---

## The decision

Workplan v3 (`workplan/workplan-co0007-v3.md`, committed `3385209d`) is the path forward, OR is it revised based on Stage 0 findings?

Per workplan v3 §0.9: *"If adopted, Stage A begins. If revised, workplan v5 issued."*

---

## Three options

### Option A · Adopt v3 as-is

Adopt the committed workplan v3 verbatim. Track the Stage 0 findings as known limitations to be addressed within the existing phase structure rather than amending the workplan document.

**Defensible because:**
- Workplan v3 is structurally sound; Stage 0 found no architectural reason to revise
- The findings are budget adjustments and disposition refinements, not structural rework
- Phases A1–A13, B1–B7, C0–C11 absorb the findings within their normal scope (A8 disambiguates jurisdictions, A6 absorbs sparse-evidence implementation, C2 absorbs skill responsibility-matrix work, C7 absorbs the larger residual)

**Not defensible because:**
- Three explicit budget adjustments are known and unincorporated, which silently understates effort
- "Workplan v3 says 12–17 sessions for C7; actual scope is now 15–22" is the kind of arithmetic gap audit B-01 was meant to surface

### Option B · Adopt v3 with documented amendments (RECOMMENDED)

Adopt workplan v3 as the structural plan; commit a paired amendments document capturing the six specific adjustments Stage 0 surfaced. The combination becomes the operative plan.

**Six amendments:**

| # | Amendment | From | To | Source |
|---|---|---|---|---|
| 1 | C7 session budget | 12–17 | **15–22** | 0.2 §M2 (584 sources / 81 unverified residual; was 557/33) |
| 2 | C2 session budget | 12–16 | **20–28** OR defer some NEW skills to mid-Stage-C with explicit cut-list | 0.3 (75 skill-tasks; ~33 NEW skills require full construction) |
| 3 | C3 task structure | "Each parameter migrated independently" | Explicit STUB / MERGED / AMBIGUOUS / CLEAN disposition track per BPC | 0.4 §F3 |
| 4 | Salvage matrix | "BPC `best_practice_synthesis` fields where contamination sample shows clean" (Reusable conditionally) | "≥92% Fully reusable; ~8% Reusable conditionally; ~7% Pending Opus; ~7% Redirect" | 0.4 |
| 5 | A8 jurisdiction philosophy scope | "Worldview as first-class entity. 24-vs-46 inconsistency resolved" | Plus: define glossary distinguishing **registered standards (49)** vs **canonical research coverage (24)** vs **prior synthesis cite (46)** | 0.2 §M5 |
| 6 | A13 doctrine-recheck cadence | "Periodic operational audit cadence" | Plus: add contamination-sampling methodology from 0.4 as a recheck procedure (every N sessions or stage transition, sample N≥15 BPCs and re-classify) | 0.4 lessons-learned |

**Total budget impact:**
- C7: +3 to +5 sessions (above 12–17)
- C2: +8 to +12 sessions if Option-B-full-build, OR +0 sessions if defer some skills to mid-Stage-C with cut-list
- Net: +11 to +17 sessions if both budgets revised upward; +3 to +5 if C2 cut-list approach taken

**Total revised range:** 224–334 → **227–351** (Option-B-full) or **227–339** (Option-B-with-cut-list)

**Real-world months impact:** marginal; 15–24 months remains the binding range because Co-1 cadence dominates session count.

**Defensible because:**
- Workplan v3 structure is preserved; only specific budget cells and salvage matrix update
- Each amendment is traced to a specific Stage 0 finding
- The amendments document IS the audit trail for "v3 was adopted, with these known adjustments"
- Lower transaction cost than reissuing as v5

**Not defensible because:**
- Two committed documents (v3 + amendments) is one more thing to track
- A future reader needs both files to understand the operative plan

### Option C · Revise to workplan v5

Re-issue the entire workplan as v5 incorporating all Stage 0 findings inline, superseding v3. v3 marked superseded.

**Defensible because:**
- Single canonical document
- No reader needs to combine multiple files
- Cleaner audit-trail at next stage

**Not defensible because:**
- The structural changes are minor; reissuing 700 lines of workplan to update six cells is heavier than the change demands
- v3 is only 1 day old; high churn rate on workplan documents weakens their authority
- Adoption-and-amend is the standard pattern for documents of this kind in standards bodies (RFCs, ISO standards)

---

## Recommendation

**Option B** with the C2 cut-list approach (defer `web-renderer`, `respect-visibility-renderer`, `navigation-mode-renderer` to mid-Stage-C, building only `markdown-renderer`, `questions-renderer`, `rendering-refresh-coordinator` in C2 proper). This keeps C2 budget within original 12–16 range while honestly tracking the deferral.

C7 must move to 15–22 sessions; the residual scope has tripled and silent compression isn't honest.

The salvage matrix and A8 jurisdiction-glossary amendments are zero-budget adjustments — just clarifications.

A13 doctrine-recheck contamination-sampling adds a few sessions over the project's life but is paid for by the early-warning value.

---

## What committing this decision does

When you decide:

1. I write `governance/workplan-adoption.md` capturing your selection and rationale.
2. If Option B chosen, I write `workplan/workplan-co0007-v3-amendments.md` capturing the six amendments and the C2 cut-list.
3. Commit both.
4. Stage 0 done criteria check (all 9 met) and Stage A is unblocked.

After that, the next session begins **Stage A** with A1-A2 (Audience + Mission canonical, merged per audit L-07). Per `governance/mission-PROVISIONAL.md`, the Coda's "sit with the mission ≥1 day" test should run before A1-A2 starts. Earliest defensible Stage A start: 2026-04-27.

---

## Stage 0 done criteria — final check

| Criterion | Status |
|---|---|
| Live project state grounded | ✓ 0.1 |
| Quantitative claims verified | ✓ 0.2 |
| Current skill set inventoried | ✓ 0.3 |
| Contamination ratio estimated | ✓ 0.4 |
| Three Critical doctrinal decisions made | ✓ 0.5 |
| Mission committed PROVISIONAL | ✓ 0.6 |
| Synthesis re-issued | ✓ 0.7 (synthesis v2; roadmap-2 deferred per file disposition note) |
| Repo strategy decided | ✓ 0.8 |
| Workplan adopted | **PENDING — this decision** |

8 of 9 met. Single remaining gate is your adoption call.

---

## What this report does not do

- **Does not adopt or revise the workplan.** That is your decision.
- **Does not commit `governance/workplan-adoption.md`.** That commits *after* you decide.
- **Does not start Stage A.** A1-A2 is the first Stage A phase; it cannot start until 0.9 commits and the mission "sit-with" period elapses.
- **Does not commit a roadmap-2.** Per 0.7 disposition note: roadmap-1 was a conversation artifact not committed to repo; producing roadmap-2 de novo would essentially restate Part V of synthesis-2. If you want a separate roadmap document, request it explicitly and I'll write one keyed to workplan v3 + amendments.

---

## What I recommend you do next

1. **Read `governance/mission-PROVISIONAL.md`.** Sit with it. Adopt the doctrinal commitments or revise them. If you'd revise, that triggers a fresh A1-A2 mission-and-epistemics work session, not a 0.6 redraft.
2. **Choose A / B / C** from this package.
3. **If Option B**, confirm the C2 cut-list (which NEW skills defer to mid-Stage-C).
4. **If Option C**, the v5 workplan-issue will be heavy work — schedule a session for it.

The simplest valid response: *"Option B with C2 cut-list."* I commit, Stage 0 closes, Stage A unblocks.
