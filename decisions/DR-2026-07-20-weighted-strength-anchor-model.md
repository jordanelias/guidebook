# DR-2026-07-20 — Weighted-strength anchor model, review-species tiering, practitioner practice-stream

**Status:** OPERATIVE — 2026-07-20
**Decision by:** Owner directive 2026-07-20 ("all evidence tiers can be used to anchor a best practice claim,
but the strength of the claim is weighted by their tier … T1/2/3 full, T4/5 partial, T6/grey weak"; and
"I don't trust most architects etc to understand the way an OT would or someone with lived experience"),
approved 2026-07-20 ("approve my decisions like tier model").
**Amends:** `governance/tier-system.md` (adds §8, §9, §10; supersedes the binary rule in §3 line 45).
**Closes:** GAP-298 (review-species tiering); GAP-299 (practitioner practice-stream).

---

## 1. Weighted-strength anchoring (supersedes §3's binary rule)

Prior doctrine (`tier-system.md` §3): *"Best-practice claims require T1, Co-1, T2, or Co-2 evidence."* That
binary is replaced. **Every tier can anchor a best-practice claim; the claim's strength is weighted by the
tier of the evidence behind it.** The tiers exist precisely so a reader can grade the confidence behind each
proposal — not to gate whether a proposal may be stated at all.

Three strength bands — the existing `●◐○` markers (§5), now given anchoring semantics:

| Band | Tiers | Anchoring behaviour |
|---|---|---|
| **● Full** | T1, Co-1, T2, Co-2, **T3-clinical** | Anchors a best-practice claim outright (adjudicated evidence). |
| **◐ Partial** | T4, T5 | Anchors, but the claim is rendered as *current standards practice* — flagged "standards basis, not primary evidence." |
| **○ Weak** | **T3-grey, T6** (code-floor), expert-consensus / thin base | Anchors only a floor/convergence claim, rendered with an explicit honesty flag: *"best available given current regulation/practice, NOT academically adjudicated."* |

**Convergence-not-evidence (§3) is preserved** as an honesty rule *within* the weak band: multiple T4–T6
codes agreeing on a value is convergence of floors, stated as regulatory practice at weak strength — never
relabelled "preferred/best practice." The change is only that such a claim is *stated and flagged*, not
suppressed, when no stronger evidence exists.

## 2. Review-species tiering (closes GAP-298)

- **Systematic reviews / meta-analyses → T2** (`sr_meta`) — unchanged (2026-05-25 enshrinement).
- **Scoping reviews and narrative / literature reviews → T3.** They map literature breadth without graded
  critical-appraisal synthesis, so they do not sit at the T2 synthesis tier. They are peer-reviewed secondary
  work: **supporting** evidence (● band, but *not* a T2 synthesis anchor). evidence_type stays `clinical`
  (secondary) or `grey`; it is NOT `sr_meta`.
- **Rapid reviews → case-by-case.** If a rapid review retained a systematic search + appraisal (only
  accelerated), it may sit at T2; if it dropped appraisal for speed, T3. Default T3 unless the method
  demonstrably retained systematic rigour.

Consequence: the PR #32 re-tier was correct to move only the *genuine* systematic reviews to T2; the 8
scoping reviews + 1 rapid review held at T3, and the narrative review REF-00589 reverted to T3, are all
**confirmed correct** by this decision. No further DB change is required for those rows.

## 3. Practitioner / firm practice-stream (closes GAP-299)

Practitioner and firm design work (architects, accessibility consultants, e.g. HCMA) is placed **by method,
not by authorship**, and sits **below Co-1 and Co-2 in authority**:

- Firm **post-occupancy evaluation / measured study** of a built project (with outcome or cost data) →
  primary evidence at its method's tier (T1 or T3). This is the firm's competent domain — *what was built
  and measured*.
- Firm **design framework / index** aggregating evidence across projects → T2-adjacent only if it
  genuinely synthesises evidence; otherwise supporting (T3).
- Firm **guidance / white-paper** without method → T3-grey (○ weak).

**Role-appropriate-authority gate (owner's trust directive).** A firm/architect source can anchor a
**descriptive / measured** claim (what was built, what it cost, what was measured) at its method strength,
but **cannot anchor a functional-need claim** ("disabled people need X / X works because Y") on its own —
that requires **Co-1** (lived experience) or **Co-2** (OT). A firm asserting a functional-need claim alone is
flagged *"designer assertion, unadjudicated"* (weak). Lived experience and OT judgment outrank designer
assertion on what works for a disabled person — consistent with the corridor-width precedent (§3), where
Co-1 (DSDG/DeafScape) anchors 2440 mm over code convergence.

**Encoding.** A dedicated practice-stream marker (a `practice` evidence_type, conceptually a "Co-3" authority
stream) is defined here; its formal representation in the audit is deferred to the audit rework (see §5). As
the first concrete application, **REF-00300** (HCMA + Rick Hansen Foundation *RHFAC Retrofits and Upgrades
Cost Study*) is corrected from **T6 `code` → T3** empirical firm cost data (a descriptive/measured output in
the firm's competent domain) — it is emphatically **not** statutory code.

## 4. Unverifiable anchor sources (from the correctness sweep)

The anchor-correctness sweep (`audits/anchor-correctness-sweep-2026-07-20.md`) flagged **7 anchor sources as
unverifiable / possibly non-existent**, each adversarially upheld: REF-00055 (no RCOT publication with the
stored title), REF-00058 (no such joint COTEC+WFOT statement), REF-00111 (no identifiable source), REF-00152,
REF-00381, REF-00549, REF-00641 (unresolvable placeholder citations). Per the anti-fabrication discipline
these are set `verification_status = 'DISPUTED'` with the sweep evidence recorded — stripping their VERIFIED
standing and their ability to anchor a claim until a real source is located or they are retired. They are
**not deleted** (a disputed row is a recorded finding). REF-00045 and REF-00140, which merely could not be
re-retrieved this session (tooling), are left unchanged — unverified-this-session is not disputed.

## 5. Follow-up (not in this DR's migration)

- **Audit rework** — `tools/evidentiary_audit.py` to report the strength band + weak-only flag instead of the
  binary `no-anchor` flag, and to encode the practice-stream. Tracked as the next engineering step.
- **Held sweep corrections** — the ~44 tier/type reclassifications and 71 model-dependent defects are now
  unblocked by this DR and applied in follow-on migrations; the ~76 author/title string corrections applied
  in careful reviewed batches.
