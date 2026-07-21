# DR-2026-07-20 — Reconcile evidence-architecture.md with the weighted-strength anchor model

**Status:** SUPERSEDED-BY `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` — owner ruled **Option A** (with direction-aware most-accommodating floor selection) on 2026-07-21; this DR's framing function is complete. (Was: PROPOSED — pending owner ratification.)
**Category:** D-METH / doctrine reconciliation
**Raised by:** Session `project-pipeline-overview-xfpid1` adjudication pass (finding F1), 2026-07-20.
**Blocks:** promotion of `governance/pipeline-contract.yaml` to ratified; any render of regulatory-stratum-only cells.
**Does NOT amend anything on its own** — this DR only frames the decision and enumerates the edits each option entails. No canonical doc, view, or invariant is changed until the owner rules.

---

## 1. The divergence

On 2026-07-20 the owner enshrined the **weighted-strength anchor model** in `DR-2026-07-20-weighted-strength-anchor-model.md`, which amended **only** `governance/tier-system.md`:

- `tier-system.md §8` (:89–99): *"Every tier can anchor a best-practice claim; the claim's strength is weighted by the tier of its evidence"* — three strength bands via `●◐○`; T4/T5 anchor at `◐` ("current standards practice"), T6/grey at `○` (weak, code-floor).
- `tier-system.md §3` line 45 binary rule superseded; supersession banner at `:47`.

`governance/evidence-architecture.md` (CANONICAL, ratified 2026-07-13) was **not** amended and still hard-codes the prior binary wall:

| Locus | Current text (pre-reconciliation) |
|---|---|
| §2 (:44) | regulatory stratum sources "do not anchor best-practice claims … convergence of codes is convergence-not-evidence" |
| §3 matrix (:77–78) | `code×population` / `code×person` → **NON-ANCHORING** |
| §5 (:103) | a `regulatory_stratum_only` determination "is never rendered as best practice, in any register, for any audience. `v_best_practice` excludes it." |
| §6 invariant **I3** (:139) | "No best-practice language on regulatory-stratum-only cells, in any register, under any weighting profile." |
| §6 register map (:130) | row 3 renders regulatory-stratum cells with the "**convergence is not evidence**" anti-laundering language only. |

And the engine encodes the exclusion mechanically:

- `scripts/assess/assess_cell.py:~554` — `CREATE VIEW v_best_practice … WHERE state IN ('stated','provisional') AND code_floor_only = 0 AND tier_basis NOT LIKE '%(regulatory_stratum_only)'`.

## 2. What is already resolved (do not re-litigate)

**Precedence is not ambiguous.** `evidence-architecture.md:4` carries the clause "where this document and a cited source ever diverge, the cited source governs," and `tier-system.md §8` post-dates the 2026-07-13 ratification. So **in the interim `tier-system.md §8` governs**: every tier may anchor at graded strength *today*. The divergence is therefore not a live behavioral contradiction in doctrine — it is an **unreconciled-text + stale-code** state: the canonical architecture doc and the `v_best_practice` view still describe and enforce the superseded wall.

The one substantive thing precedence does **not** silently fix: `v_best_practice` still *mechanically excludes* regulatory-stratum-only cells. Code behavior and §8 already disagree the moment such a cell would be rendered.

## 3. The decision the owner must make

`tier-system.md §8`'s weighted-strength model can be read two ways where it meets `evidence-architecture.md §5/§6`. The owner must pick one, and the choice is genuinely load-bearing because it decides whether a code-only cell can ever carry best-practice framing:

### Option A — Weak-anchor: regulatory-stratum cells enter the best-practice surface at the weak band, with mandatory honesty flags
§8 is read as fully repealing the anchoring gate. A `regulatory_stratum_only` cell becomes a `○`-strength best-practice determination — surfaced, but always labelled weak/code-floor and carrying the anti-laundering language.

**Edits this entails (all deferred to a follow-up execution DR, none applied here):**
- `evidence-architecture.md §2` (:44): rewrite the "do not anchor" wall to the graded-strength rule.
- `evidence-architecture.md §3` matrix (:77–78): `code×population` / `code×person` move from NON-ANCHORING to a weak/`◐`–`○` band.
- `evidence-architecture.md §5` (:103): drop "never rendered as best practice, in any register"; replace with the weak-band rendering rule.
- `evidence-architecture.md §6` **I3** (:139): **repeal the absolute form** — I3 becomes "no *unflagged* / no *strong-band* best-practice language on regulatory-stratum-only cells," not "no best-practice language at all." Re-check I5 for consistency.
- Register map row 3 (:130): allow weak-band best-practice phrasing alongside the convergence-not-evidence caveat.
- `assess_cell.py` `v_best_practice`: drop (or reweight) the `regulatory_stratum_only` exclusion; add a strength-band column so the weak band is queryably distinct.

### Option B — Rendering-strength-only: §8 governs *how strongly* an already-anchored cell is rendered, and regulatory-stratum-only cells stay excluded from `v_best_practice`
§8's "every tier can anchor" is read as applying within the evidence-anchored population determination (grading confidence of T1/T2/T3-backed values), while a cell whose **entire** basis is T4–T6 remains a Universal-Mode regulatory determination that is not a best-practice claim. The wall stands for *code-only* cells; the weighting applies to *evidence-backed* cells.

**Edits this entails:**
- `evidence-architecture.md`: **no change to §5/§6/I3 or `v_best_practice`.** Add a clause to §2/§6 that scopes §8's weighting to anchored cells and explicitly preserves I3 for `regulatory_stratum_only`.
- `tier-system.md §8`: add a scoping sentence that T4/T5's `◐` "current standards practice" rendering is *standards-practice* framing, not *best-practice* framing, for cells with no evidence-tier anchor — closing the apparent contradiction from the tier-system side.

## 4. Why this is owner-gated (not a mechanical fix)

Both options edit a **ratified canonical document** (`evidence-architecture.md`) and one repeals or rescopes a **ratified integrity invariant** (I3) and changes a determination-surface view. That is doctrine, not hygiene. Per the governance model, canonical docs are "edited only after ratification," and the choice between A and B is a values call about whether a code-only requirement may ever wear best-practice language — precisely the "convergence-is-not-evidence" concern I3 was built to protect. It is the owner's to make.

## 5. Recommendation (advisory only)

Not offered — this DR deliberately stops at framing. The adjudication that raised F1 did not rank A vs B, and doing so here would substitute the author's judgment for the owner's on a doctrine call. The owner rules; a follow-up execution DR then applies exactly the edit set for the chosen option under the normal attestation/CI path.

---

## Appendix — provenance

- Divergence surfaced by the adversarial + adjudication passes in session `project-pipeline-overview-xfpid1` (Fable 5 max-effort adjudication, finding F1, verdict OWNER-GATED, CONFIRMED).
- Interim governing authority: `tier-system.md §8` via the `evidence-architecture.md:4` precedence clause.
- No evidence source is cited and no synthesis claim is asserted by this DR (rule #10 not exercised).
