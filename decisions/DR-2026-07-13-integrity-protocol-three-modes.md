# DR-2026-07-13: Integrity protocol — three-mode implementation of the adversarial-review lessons

- Status: **PROPOSED — pending owner ratification**
- Date: 2026-07-13
- Prepared by: Claude, on the owner's directive to implement the adversarial-pass lessons "as a preventative prior structuring, a live rules processing docket and a post processing integrity check."
- Creates: `skills/integrity-protocol_SKILL.md` (the three modes as operational session doctrine), `scripts/audit/claims_docket.py` (Mode-2 tooling; ships with its own mutation selftest per its own rule)
- Empirical basis: 41 findings across the two independent adversarial passes of 2026-07-12/13, on work that had passed its authors' own checks both times; fix-by-fix records in the unification and genealogy DRs' revision histories. The defect classes cluster at the seam between claims and artifacts: false absolutes/totals, verification verbs outrunning artifacts, caveats stripped in distillation, rules exempting their own documents, favoured conclusions receiving lenient scrutiny.
- Related: `decisions/DR-2026-07-12-evidence-architecture-unification.md` (revision history v2), `decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md` (revision history v2), ratification item C3 (CI enforcement)

## Proposed decision — three separately ratifiable items

**P1 — Mode 1, preventative prior structuring (authoring-time constraints).** Typed assertions with warrant classes (VERIFIED-BY / PREDICTED / REPORTED-BY / RECOUNTED / N/A); caveats welded to values at schema level; verifiers born with mutation selftests in the same commit; the self-application clause (every rule document applies its rule to itself and its flagship example before shipping); source artifacts committed before distillation begins. Specified in `skills/integrity-protocol_SKILL.md` §Mode 1.

**P2 — Mode 2, the live claims docket.** `scripts/audit/claims_docket.py` scans the working diff's added prose for the empirically-derived trigger classes (absolutes/totals, verification verbs, unmarked quantities) and gates commits on warrant annotations; processed at every phase commit, not session end; plus the author-processed live triggers (strictest-test-on-favoured-conclusions logged; retraction-grep before any corpus figure travels; no silent self-corrections). The scanner is a documented mechanical floor — claims phrased outside its lexicon escape it; lexicon additions are versioned in the script.

**P3 — Mode 3, the post-processing gate.** The mechanical battery run as a unit with outputs logged (never summarized from memory), and the standing rule: **no ratification request, no "done," no ready-for-review PR while an independent adversarial pass is unrun or its findings unapplied.** The pass's required structure: fresh context; brief to break; presumed ≥1 defect; re-run everything; enumerated attack lines including the audit of the author's chat statements to the owner; findings land in revision histories and attestation deviation logs.

## Consequences if ratified

`skills/integrity-protocol_SKILL.md` joins the active skill set (loaded by future sessions like the other 48); the claims docket becomes part of the phase-commit rhythm; P3's gate becomes the standing precondition for every future ratification package. Interaction with C3: if the owner restores blocking CI, `claims_docket.py check` and the battery join it; if not, they remain self-run gates whose outputs must be logged. The protocol's own limit is stated in the skill: it makes bias visible, not the model rigorous — the correction loop (Mode-3 findings feeding Mode-1 structure) is where rigour accumulates.

## Self-application (per its own Mode-1 clause)

This DR and skill were checked against themselves: the skill's verifier rule is satisfied by `claims_docket.py` shipping with a selftest that FIRED 3/3 on synthetic triggers, failed an unannotated docket, and passed an annotated one, before this DR was written; the demo run over this branch's own diff surfaced 228 triggered claims, including the exact absolute ("all 14 … none omitted") the second adversarial pass caught by hand — the tool would have gated it. RECOUNTED: with this DR the PROPOSED roster is **16** (grep count 16 over decisions/DR-*.md headers + the ratification package; the unification impact appendix rides with A5). PREDICTED: applying the docket to future sessions will raise authoring friction; the bet, falsifiable by use, is that annotation cost is far below post-hoc review cost — if the docket rots into ritual annotation, that is a finding against P2's design, to be revised rather than routinized.

## What would make this ACCEPTED

Owner review of P1–P3 (independently answerable). The substantive judgment call: P3's hard gate — ratification requests structurally blocked on adversarial passes — trades session speed for the one mechanism that has caught what self-checks missed, both times. Recommend ratifying it as written.
