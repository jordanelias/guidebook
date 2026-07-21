# DR-2026-07-21 — Evidence-architecture Option A execution: weak-anchor reconciliation with the weighted-strength model

**Status:** OPERATIVE — by owner directive 2026-07-21 (finding F1, Option A ratified).
**Category:** D-METH / doctrine reconciliation — execution.
**Decision by:** Owner directive 2026-07-21, ruling on finding F1 as framed by
`decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md` §3:
**Option A** (weak-anchor), plus **direction-aware most-accommodating floor selection**.
**Amends:** `governance/evidence-architecture.md` (CANONICAL; amendment marker added to both status loci).
**Supersedes:** `decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md`
(the framing DR — now marked SUPERSEDED-BY this DR; its framing function is complete).
**Implements:** `governance/tier-system.md` §8 (weighted-strength anchor model,
`decisions/DR-2026-07-20-weighted-strength-anchor-model.md`), at the render/state layer of the
evidence architecture.
**Repeals:** invariant **I3's absolute form** ("no best-practice language on regulatory-stratum-only
cells"). I3 survives in amended form: no *unflagged* and no *above-weak-band* best-practice language
on regulatory-stratum-only cells, in any register, under any weighting profile; I5 applies with the
register map's ○ row as ceiling.

---

## 1. The decision

1. **Weak-band anchoring (Option A).** A determination whose entire evidence basis is the
   regulatory stratum (T4–T6, `regulatory_stratum_only`) **is a best-practice determination at the
   weak band (○)** — best available *as currently known, given that nothing stronger says
   otherwise*. It is always rendered flagged weak/code-derived, with the convergence-not-evidence
   caveat, in every register, for every audience — never unflagged, never at anchoring strength.
   Convergence-not-evidence is retained as the honesty rule within the weak band
   (`tier-system.md` §3 banner + §8), not as a suppression rule.
2. **Direction-aware most-accommodating floor selection.** Where jurisdictions' code floors differ
   on a parameter, the regulatory-stratum determination anchors on the most accommodating available
   value, read per the parameter's accessibility direction — best-for-the-user, not largest-number:
   widest minimum corridor, but *lowest* maximum threshold height and *gentlest* maximum ramp
   slope. The parameter's direction is recorded with the determination; passed-over floors remain
   visible as the jurisdiction spread.

## 2. Interpretive resolutions recorded with the ruling

1. **Render/state layer only.** Option A changes rendering and best-practice-surface membership.
   It does **not** change `schemas/directness.py`: grain-directness `code×population →
   NON-ANCHORING` remains a mechanical fact (code grain cannot *directly* support a
   population-specific value) and the §10 sweep (`scripts/audit/matrix_consistency.py`) continues
   to own those values. Any directness re-grain is a separately reviewed follow-up (§5).
2. **State machine unchanged.** `regulatory_stratum_only` cells remain `provisional`, never
   `stated`; `scripts/validate_evidence_state.py` and evidence-architecture §10 check 4 are
   deliberately untouched.
3. **Band assignment.** The determination-level band for any `regulatory_stratum_only` cell is
   ○ weak — per the owner's 2026-07-21 wording and `tier-system.md` §8's closing paragraph —
   even where T4/T5 sources are present; the ◐ "current standards practice" band of §8's table
   applies to individual T4/T5 citations contributing to an otherwise-anchored cell, and to
   source-level `●◐○` markers (`tier-system.md` §5), which are unchanged.
4. **Deviation from the framing DR's edit list:** `code×person` gains **no** render-anchoring.
   Person Mode stores no determinations (evidence-architecture §5) and no code value resolves an
   individual's assessed need (`co1-operational.md`); the framing DR's "code×person moves to a
   weak band" clause is not executed, and the §3 matrix Person-Mode cells stay NON-ANCHORING in
   both senses. (Consistent with the live DB: all three current `regulatory_stratum_only` cells are
   `design_scale = universal`.)

## 3. Doc edits applied (this DR's execution set)

`governance/evidence-architecture.md`: header status + closing status table (amendment markers);
§1 scatter row "Best-practice ≠ convergence"; §2 T4–T6 bullet (wall → graded weak anchoring);
§3 matrix code-grain Population cells + new footnote †† (grain-directness vs render-anchoring;
mechanical values unchanged); §5 scale-tagging bullets (phrase-exclusivity repealed; weak-band
rendering rule; new direction-aware most-accommodating bullet); §5 laundering paragraph (closure
by mandatory flagging, not suppression); §6 register map row 3 (weak-band best-practice phrasing
at ○, caveat retained, policy register strongest); §6 I3 (amended form); §8.1 and §8.3 worked
examples. `decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md`:
status → SUPERSEDED-BY. Every doc statement that outruns the engine carries an inline
`[ENGINE-LAG → DR-2026-07-21 §5]` marker; markers are removed only by the follow-up that lands
the behavior.

## 4. What this DR does NOT change

`schemas/directness.py`; `scripts/audit/matrix_consistency.py` EXPECTED table; the §10 sweep
comment block; the four-state determination machine; `code_floor_only`/`regulatory_stratum_only`
column semantics (migrations 026/027 schema); tier assignments of any source; `tier-system.md`
(already carries the model).

## 5. Engine follow-up (tracked; doc markers point here)

1. **`v_best_practice`** — migration 028 + `scripts/assess/assess_cell.py` interim view: drop the
   `regulatory_stratum_only` exclusion (both the column predicate and the `tier_basis` marker
   guard, migration 027; assess_cell.py view); add a queryable strength-band column so
   weak-band rows are distinct, never silently mixed with anchored rows.
2. **Most-accommodating selection** — implement direction-aware floor selection in
   `assess_cell.py`; add per-parameter accessibility-direction metadata; render the jurisdiction
   spread alongside the anchored value.
3. **`scripts/audit/register_integrity_check.py`** — rework the I3 lexicon check to the amended
   form (unflagged / above-band, not absolute) and update the tamper-injection suite so it fires
   on a *missing flag* and on *above-○ phrasing*, and passes on compliant weak-band renderings.
4. **Renderers** — `scripts/generate/spec_page.py`, `population_page.py`, `pilot_renderings.py`
   pick up the new register-map row 3; `tools/evidentiary_audit.py` band rework already tracked in
   DR-2026-07-20-weighted-strength-anchor-model §5.
5. **Optional directness re-grain** — if the owner later wants the grain layer itself to encode
   weighted anchoring, change `schemas/directness.py` + matrix_consistency.py EXPECTED + §3
   parentheses + §10 comment in one reviewed commit. Explicitly out of scope here.
6. **Re-derive the live cells** under a bumped `RULE_VERSION` (pilot-2 → post-Option-A), so the
   three `regulatory_stratum_only` cells carry the new band semantics
   and fresh `derivation_sha` values; regenerate renderings.
7. **Revalidate:** matrix sweep (must still pass unchanged), determinism (byte-identical
   `derivation_sha` on re-run), I1–I5 via the reworked checker shown firing on injected
   violations, `validate_evidence_state.py`, and re-attestation of the superseded framing DR's
   attestation record.

---

## Appendix — provenance

- Owner ratification 2026-07-21 of finding F1, Option A, per the framing DR's §3 option set;
  direction-aware most-accommodating rule ratified in the same directive.
- Interim-precedence note: between 2026-07-20 and this DR, `tier-system.md` §8 already governed
  via evidence-architecture.md:4's precedence clause; this DR reconciles the text, it does not
  create the doctrine.
- No evidence source is cited and no synthesis claim is asserted by this DR (rule #10 not
  exercised).
