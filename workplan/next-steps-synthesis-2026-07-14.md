# Next-steps synthesis — 2026-07-14

**Method:** agonist–antagonist + adversarial critique. Four divergent next-steps strategies were each developed at max effort (agonist), each attacked by an independent max-effort adversary (antagonist), plus a meta-adversary attacking the shared frame of all four. This document is the adjudicated synthesis. It is a **plan, not an execution** — no migration, synthesis, or gate edit has been applied; those await owner go-ahead.

Deliberation artifacts: workflow `wf_d88cd7a9-284` (9 agents, 0 errors); per-agent results in that run's `journal.jsonl`.

---

## 1. The finding that anchors everything

The evidence **library** is mature (640 sources, 635 existence-verified, eligibility 92.6%). The evidence **judgment layer** — the syntheses that are the reason the project exists — **has not advanced in ~2 months.**

Live DB (2026-07-14) vs the Phase-E plan's own 2026-06-10 preflight:

| Synthesis substrate | 2026-06-10 | 2026-07-14 |
|---|---|---|
| `reasoning_doc_citations` | 7 (pilot) | **7** |
| `source_value_extractions` | 0 | **0** |
| `spec_value_probes` (PMP) | 21 | **21** |
| `evidence_cell_state` | pilot-only | **7 rows** |
| `conflicts` | 0 | **0** |
| BPCs re-synthesized | 0 | **0 of 82** |

The pilot (`references/bpc-reasoning/room-acoustic-performance.md`) is frozen at "RT60 steps 1–3" from **session 2026-05-15a**. Every substantive commit 2026-06-10→07-14 is governance/integrity/audit/attestation/schema/pipeline work; the scheduled verification jobs report **+0 on every metric every run**. Meanwhile the one hard external blocker — scholarly-connector approval (GAP-286 / D-4.3-C) — appears resolved: PubMed / Consensus / Scholar Gateway are live in-session. **Synthesis is effectively unblocked and simply not being done.** The 2-month pattern is consistent with the project's own documented failure mode: tractable, self-generating governance work displacing the expensive, judgment-heavy core (`audits/project-inventory-and-state-2026-07-12.md`).

**Credit where due (adversarial critique cuts both ways):** the corpus is real and solo-sound; the methodology is epistemically sophisticated — e.g. the pilot labels the autism RT60 value "conjecture rationally informed by literature" *inline*, with PMP *expected to fail* strict-termination, recording conjecture structurally rather than dictating a value. The problem below is not sloppiness; it is structural.

---

## 2. The four strategies and how they fared under attack

Every strategy survived only *with a fix* — none was fatal, none was clean. That convergence is itself the signal.

| # | Strategy | Verdict | The attack that landed |
|---|---|---|---|
| **S1** | EXECUTE NOW (run the waves) | survivable-with-fix | Places the irreversible **scale-and-publish** decision *before* the only instrument (external review) that can validate quality; the pilot proves only cost, self-certifies trustworthiness; kill-criterion is circular (a solo instrument can't demonstrate its own miss). |
| **S2** | VALIDATE BEFORE SCALE | survivable-with-fix | Defers `source_value_extractions`, which the plan's own rule ("no step-3 cell without a backing extraction row") makes non-skippable → the "calibrated" cost comes out biased **low**, a false green light on the exact decision it exists to inform. |
| **S3** | FINISH THE FOUNDATION (genealogy engine) | survivable-with-fix | Manufactures false urgency (a "retrofit trap" on a **0-row** table); inflates one migration into a 3-session program whose later steps are self-admittedly **off** the extraction critical path — the displacement pattern wearing a "foundation" label; its validation gate is circular (reproducing the worked example only proves a `GROUP BY` counts the author's own hand-assigned roots). |
| **S4** | RE-SCOPE to a small v0 | survivable-with-fix | Uniquely **publishes** to disabled end-users, but **no exit criterion enforces** "externally-reviewed / counsel-cleared"; a logged non-response satisfies the gate, so the modal outcome ships uncleared content carrying the 67% error rate wearing a "reviewed" halo it never earned. Its only real fix collapses it into S2. |

### What survived every attack (the robust core — adopt regardless of strategy)

These recurred across independent adversaries. They are the parts of the plan that are *not* contingent on which direction the owner chooses:

1. **Complete the frozen pilot end-to-end now.** Unanimous — every strategy requires it; it is a decaying, "not retroactively reconstructable" asset; it converts the speculative 950–1,300 h estimate into one measured input. This work is never wasted.
2. **Land migration 028 = H1 genealogy columns only** onto `source_value_extractions`, as a one-migration prepend *before extraction row 1* (S3's real kernel, stripped of its 3-session program). Retrofit genuinely is the expensive path (DR-2026-07-13:51) — but the fields go on an empty table, so the true cost is one same-session migration, not a foundation phase.
3. **Hand-populate `source_value_extractions` for the pilot** — bounded manual work for one parameter; the plan's own auditability rule forbids "stated" cells without a backing row, and skipping it is what biases the cost model low.
4. **Send the pilot-*independent* external-review batches at hour 0** — above all **counsel** (the binding launch gate per `governance/legal-regulatory.md`; 4–12 wk lead; reviews already-CANONICAL docs, needs nothing from the judgment layer). Starting this clock now is the fastest way to *empirically test* whether a second human will ever engage (see §3).
5. **Do not publish solo-adjudicated values as settled authority before external validation returns.** Complete the pilot but **hold it behind the existing PROVISIONAL / PRE-REHABILITATION banner** — do not overwrite the banner or mark `bpc_complete`. Split *ship* (machinery turns, cost measured) from *publish-as-authority*.
6. **Governance freeze for the duration.** No new DR / adversarial pass / attestation cycle unless it demonstrably blocks a synthesis slug. Real infra/integrity debt (doctrine-SHA blob-vs-commit; C3 Actions enforcement; pipeline-contract & attestation-registry ratification) is genuine but **non-blocking** → a separate parallel owner track, explicitly walled off so it cannot re-freeze the loop.

---

## 3. The reframe that dominates the whole tree (meta-adversary)

All four strategies keep the **same act** on the critical path: *a single, measurably-unreliable operator authoring adjudicated "best-practice" determinations.* They differ only in **volume** (S1: 82; S4: ~10), **sequence** (S3: build the jig first), or **wrapper** (S2: mail a review afterward). None removes the biased synthesis step from the critical path; none adds a standing second author; and all four quietly define review success as *gating-on-attempt*, where a logged non-response clears the gate — i.e. **they have already pre-conceded no second human will engage** (0 of 6 outreach batches sent since 2026-05-02; CI deleted 2026-06-09).

The governing constraint is an **over-determined triple** — at most two of three can hold:

> **permanently solo** · **ships adjudicated authority** · **distributes to strangers who rely on it**

The real decision is **which one to drop**, and it is the owner's alone. The dossier's "commit to 950–1,300 h vs re-scope" is still *inside* the frame (a size choice); this sits *above* it (an identity choice). It is also in live tension with the project's own mission (`governance/mission-and-epistemics.md:16`): *"It is not a prescription manual. It does not dictate values… It is a thinking tool."* — yet every one of S1–S4 ships dictated values.

**A genuinely distinct fifth option falls out of the reframe:**

**S5 — SHIP THE EVIDENCE MAP, NOT THE AUTHORITY.** Publish what already exists and is solo-sound: the 640-source, tier-graded, Co-1/Co-2-classified corpus as a navigable annotated index by item × population × jurisdiction, **surfacing where sources disagree** and declining to emit a single adjudicated "best-practice value." The reader performs the last-mile synthesis. This *subtracts* the adjudication layer where the 67% bias lives (the opposite move from S1–S4); it matches the mission's own language; it converts "permanently solo" from fatal to fine (indexing/grading is what solo+AI has already done to quality); the empty `conflicts` table stops being a blocker because **the disagreement becomes the product**; and it ships in weeks at a fraction of the cost. Honest boundary: tier-assignment is still a judgment, so S5 shrinks the risk surface rather than eliminating it — but it is a far smaller, more checkable surface than per-cell synthesis.

S5 is not "obviously correct" — its risk is under-serving a non-expert audience that wants an answer. That trade-off is exactly the owner's identity call.

---

## 4. Recommended plan — "prove, hold, and decide," with the identity choice elevated

The robust core (§2) is correct under **every** resolution of the identity question (§3), so run it now; surface the identity decision in parallel (it has the longest latency and the review clock informs it); converge at a pre-committed gate.

**Phase 0 — unfreeze the loop (now; no owner gate; days).**
- Declare the governance freeze; move doctrine-SHA / C3 / pipeline-contract / attestation-registry to a separate non-blocking track.
- Land the content-safe cheap gates the plan already scoped: **G4a** `metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')` (without it, Pass 3 wrongly disqualifies all 328 statutory sources), **G4b** multilingual thresholds re-based 24→46, **G4c** stale model pins, **G2** the single `AUTHOR-TITLE-ONLY` source, **G5** `lang_jur_map`.
- Land **migration 028** (H1 genealogy columns + root registry + `v_value_independence` view) — smoke-tested via `--rebuild`, **not** as a scaling gate.

**Phase 1 — complete the pilot as proof, held behind the banner (now; parallel).**
- Finish `room-acoustic-performance` end-to-end (RT60 steps 4–9 + rdc rows; PMP walks; NC/dB(A)/STI/NRC; first `evidence_cell_state` + `convergence_assessment` batch), **hand-authoring `source_value_extractions`** as you go. **Keep the PROVISIONAL banner; do not mark COMPLETE.**
- **Owner:** send the pilot-independent review batches now — **counsel first** (paid engagement acceptable), plus disability-studies and DPO. Fill placeholders; owner picks recipients. This starts the clock *and* tests whether external review is real.
- Extract a **decomposed** cost model: measured (pilot incl. extraction authoring) **plus** explicitly-unmeasured-wide-CI (engine build; per-cell extraction × ~82). Not a single low number.

**Phase 2 — small diverse calibration (still held behind the banner).**
- 2–3 more BPCs spanning dispositions — one convergent, one **conflict-bearing** (populates the first `conflicts` rows), one thin-evidence — because the pilot was chosen as the *strongest* case and calibrating on it alone over-optimizes.

**The gate (pre-committed).** With measured cost + the first real external-review signal + the owner's identity ruling, choose:
- **Scale the full adjudication program (S1)** — permitted *only if* external review has actually engaged, cost is feasible, and the owner accepts the reliance;
- **Ship successive externally-cleared thematic slices (S4-fixed = S2 at slice scale)**;
- **Ship the evidence-map / thinking-tool (S5)** — de-scope the claim, not the topic count.

The crossing to **public authoritative** is **un-crossable** until real external validation *returns* — convert the counsel + methodology/DPO batches from *gating-on-attempt* to *gating-on-engagement* for that branch specifically. If, at deadline + 2 wk, no second party engages, that is itself the answer: **permanently-solo + authority + public** is unavailable, and S5 (or a standing retained reviewer) is the honest path — not "scale as if validated."

**Anti-displacement tripwire (mechanical).** Until the pilot reaches "COMPLETE-behind-banner," **no new governance DR / adversarial pass / attestation cycle** may be opened unless it blocks a synthesis slug. If a week passes with `reasoning_doc_citations` unchanged and any governance commit landed, the freeze was breached — stop and re-read this section.

---

## 5. The decision only the owner can make (surface immediately)

**"Who may rely on an un-externally-validated, solo+AI 'best-practice' value — to set a real dimension in a real building — and am I willing to stand behind that reliance?"**

- **"No one should rely on it as authority"** → S1/S3 are moot; the product is S5 (or S2/S4 reframed as non-authoritative). Fastest, cheapest, mission-consistent.
- **"Yes, designers should"** → external review becomes genuinely **gating** (a real engaged reviewer, not send-and-log), and *permanently-solo is thereby disqualified as a launch posture* — a **standing second party** (retained counsel + ≥1 methodology/domain reviewer in an actual relationship) becomes a precondition.

Every other open owner fork (connector confirmation, doctrine-SHA/C3, PAYWALL budget, and even "950–1,300 h vs re-scope") is downstream of and dominated by this one.

---

## 6. Concrete next actions

| # | Action | Owner | Effort | Exit criterion |
|---|---|---|---|---|
| 0a | Declare governance freeze; wall off doctrine-SHA/C3/pipeline-contract as non-blocking | claude | trivial | This section committed; tripwire active |
| 0b | Land content-safe gates G4a/G4b/G4c, G2, G5 | claude | small | Test query admits a `COMPLETE-STATUTORY` source; `AUTHOR-TITLE-ONLY` count = 0 |
| 0c | Migration 028 (H1 columns + `v_value_independence`), `--rebuild`-verified | claude | small | `--rebuild` reproduces columns/view; no core invariant regresses |
| 1a | Complete pilot end-to-end **behind the banner**, hand-authoring extractions | claude | multi-session | `validate_reasoning@COMPLETE` + `validate_bpc` + `validate_evidence_state` exit 0; banner intact; `bpc_complete` **not** set |
| 1b | **Send counsel + disability-studies + DPO batches** (placeholders filled) | **owner** | medium | 3 batches dispatched; tracking row each; `legal-regulatory` moved to sent-pending |
| 1c | Decomposed cost model (measured + wide-CI unmeasured) | claude | small | Artifact with per-unit actuals + 82× projection + honest interval |
| 2 | Diverse calibration wave (convergent / conflict-bearing / thin) | claude | large | First `conflicts` rows written; cost variance recorded; all held behind banner |
| — | **Owner identity decision (§5)** + connector confirm + ratify pipeline-contract/Q23 or defer | **owner** | — | Recorded in a `decisions/DR-2026-07-…` file |
| G | Pre-committed scale/publish gate (§4) | owner + claude | — | Branch chosen on measured cost + real review signal; public-authority branch un-crossable until review returns |

---

## 7. What this synthesis deliberately does not do
- **Does not pick a single winner among S1–S4.** Each fails alone; the robust core + the elevated identity choice is what the deliberation actually supports.
- **Does not execute.** No migration, synthesis, gate edit, or outreach has been performed — Phase 0/1 begin on owner go-ahead (pilot completion also needs D-4.3-D ratification).
- **Does not treat the governance debt as abandoned** — real, but non-blocking and walled off, not worked before the loop restarts.
