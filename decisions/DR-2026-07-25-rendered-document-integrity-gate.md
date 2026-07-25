# DR-2026-07-25 — Rendered-document integrity gate, and four rules the E-08 audits earned

- Status: **PROPOSED — DG-REVIEW for §2–§4 (agent decides, owner reviews); §5 is
  DG-NON and is raised, not decided.**
- Date: 2026-07-25
- Category: **D-METH** (how a derived surface is validated) with a **D-PRES** component
  (what a rendered page must show) and one **D-OP** item (§3.4, model-routing notation).
- Delegation: **DG-REVIEW** — this applies already-canonical doctrine (the DB is
  authoritative; every other store derives from it) to a surface that had no gate, and
  promotes existing text rules up the enforcement spectrum (level 1 → level 2/3). It
  originates no doctrine. The one item that *would* touch doctrine is quarantined in §5.
- Prepared by: Claude, `opus/150/synth`, session 2026-07-24/25 (E-08 corridor-width
  prototype).
- Affects: `scripts/audit/check_rendered_docs.py` (new), `scripts/audit/render_audit.js`
  (new), `scripts/preflight.sh`, `assets/guidebook.css`, `specs/e-08.html`,
  `specs/e-08-brief.html`, `governance/decision-protocol.md` §4.2/§4.4,
  `schemas/decision.py`, 43 files under `skills/`, `references/project-standards.md`.
- Related: `DR-2026-06-10-synthesis-model-floor` (§4 of which owed the skill model-pin
  sweep this DR completes), `DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation`
  (the reproducibility gate this is modelled on), `governance/tier-system.md` §5
  (evidence markers), `governance/mission-and-epistemics.md` (thinking tool, not authority).

---

## 1. Context — what happened, stated plainly

A single specifications page on corridor clear width (item E-08) was built to test whether
the project's doctrine can survive contact with a real deliverable. It was then put through
three independent adversarial audits: a machine-vision pass at four viewports, a
contemporary-design-and-UX pass, and four role-perspective passes (design catalogue, lived
experience/advocate, policymaker research, occupational-therapy consultant).

The audits found roughly ninety defects. The finding that matters is not the count:

> **Every serious defect was mechanically checkable, and not one of them was caught by
> re-reading the prose.**

The serious ones, as a class:

| Defect | Class |
|---|---|
| Three Deaf authors misnamed on the sources carrying the Co-1 grade; the Deaf Studies collaborators dropped from the citation entirely | citation infidelity |
| A citation list showing 3 of 7 governing refs plus one non-governing ref — silently hiding a Tier-6 statute and a non-ASL ethnography | asymmetric disclosure |
| A print stylesheet that hid every source, tier, caveat and legal disclaimer | display-contingent integrity |
| A population marked `applies` in the page and `context_dependent` in the register | doc↔DB drift |
| A full-strength ● rendered over a determination whose own record reads `pending_assessment` with every governing source down-weighted | grade overclaim |
| A source's finding restated more narrowly than the source itself states it | scope narrowing |

Consolidated, these have six root causes, all of which are failure modes of *judgment under
confidence* rather than of knowledge:

1. drawing a conclusion from partial evidence and presenting it at full strength;
2. generating a plausible fact instead of retrieving the recorded one;
3. treating a fix as safe because it was small;
4. disclosing rivals' weaknesses more fully than one's own;
5. letting integrity depend on how the document happens to be displayed;
6. laundering an upstream error by restating it downstream.

None of these is fixed by resolving to be more careful. Each is fixed by a check that runs
whether or not anyone remembers to be careful.

## 2. Decision — the gate

**A rendered document is a derived surface. It may summarise the record; it may not
contradict the record, and it may not present the record as stronger than it is.**

That sentence is already implied by the layer model (`architecture/project-architecture-guidebook-v2.3.md`:
the DB is authoritative, everything else derives). It had no enforcement. It has two now,
both wired into `scripts/preflight.sh`.

**`scripts/audit/check_rendered_docs.py` — the document against the record.** Stdlib only,
honours `GUIDEBOOK_DB_PATH`, exits 1 on any FAIL.

- **C1 citation fidelity** — every rendered `REF-NNNNN` exists in `evidence_sources`;
  surnames stated beside a ref match the register; the governing set of a determination is
  neither padded with non-governing refs nor silently thinned.
- **C2 epistemic persistence** — sources, tiers, caveats and the disclaimer survive print,
  and provenance is not script-contingent.
- **C3 doc↔DB drift** — population applicability hardcoded in a page matches
  `item_population_links`.
- **C4 grade preconditions** — no ● over a `pending_assessment` convergence, wholesale
  down-weighting, or a T4–T6 governing ref, unless the document itself surfaces it.

**`scripts/audit/render_audit.js` — the document as a reader receives it.** Playwright;
exits 2 when it cannot run, which `preflight.sh` reports as a loud SKIP rather than a pass.

- **R1 print** · **R2 no-JS** · **R3 reflow** at 320/768/1280 px and under the WCAG 1.4.12
  text-spacing override · **R4 target size** (2.2 SC 2.5.8) · **R5 focus not obscured**
  (2.2 SC 2.4.11).

**Why two.** Static CSS text cannot resolve the cascade, cannot read an external stylesheet,
and cannot say what a reader with JavaScript disabled gets. The first version of the Python
check FAILED three classes that the renderer proved visible — overclaiming in the opposite
direction from the defect it was written to catch. The browser is therefore the authority on
visibility, and the Python check that touches print was demoted to a WARN pointing at it.
This is the general shape: *a checker that cannot see the whole system must not render a
verdict on the whole system.*

**What the gates then found, on first run.** `specs/e-08.html` — the internal page, never
audited because attention was on the shareable brief — carried none of the seven governing
refs of the cell it grades ●, and disclosed neither the pending assessment nor the
down-weighting. `assets/guidebook.css` hid `.colophon` in print and left source panels
hidden, so *every* page built on it lost its sources and its not-a-legal-authority
disclaimer when printed. `.sr-only` lacked `left:0`, so a visually hidden span inside a
scrolling table escaped its container and widened the whole document — a WCAG 1.4.10 reflow
failure caused by an invisible element. All fixed in the same commit as the gate.

## 3. Decision — four operative rules

Recorded in full in `references/project-standards.md` (append-only ledger); summarised here.

**3.1 Derived-surface integrity.** As §2. Enforcement: level 3 (preflight + the two audit
scripts). Any new hand-authored page under `specs/` is in scope automatically — the gate
globs the directory rather than a list, so a page cannot be added *outside* it.

**3.2 Symmetric disclosure.** Disclose the status of your own governing sources as fully as
you disclose the weaknesses of the sources you down-weight, discount or exclude. The E-08
brief characterised the regulatory stratum's provenance problem in detail while rendering
its own anchor as settled — a Tier-6 statute among the governing refs, `pending_assessment`
on the convergence, every source down-weighted, none of it visible. Asymmetric candour is
not candour; it is advocacy wearing candour's clothes. Partially mechanised by C4.

**3.3 No scope narrowing in restatement.** When restating a source, restate the scope the
source itself claims. If a narrower scope is asserted, the narrowing is the guidebook's
claim and is marked as such. Chaikhot's manoeuvring finding was restated in an earlier draft
as applying to a subset of turns the source does not so limit. Narrowing looks like caution
and functions as misattribution: it puts the guidebook's caveat in the author's mouth.
Not mechanisable; C1 catches the adjacent failure (wrong name beside a ref), not this one.

**3.4 Model routing names a class, never a version.** `DR-2026-06-10-synthesis-model-floor`
already ratified that rule #2 is a capability floor — "Opus-class or above" — and §4 of that
DR owed a caller sweep it did not perform. Owner directive 2026-07-25 restated it: *if it
specifies a model number, strip that going forward.* Done here: 80 version pins stripped
across 43 skill files; `fable` added as a synthesis-capable tier in
`governance/decision-protocol.md` §4.2 and `schemas/decision.py`
(`^(opus|fable|sonnet|haiku|human|legacy)/…`); §4.4's regex and the "Opus 4.6" examples
corrected. A version pin dates the moment it is written, and a rule pinned to a retired
number reads as excluding the model that replaced it — which is how a routing *floor*
silently becomes a routing *ceiling*.

## 4. Adversarial pass (one pass, this version — R2 / DR-2026-05-09)

- **Objection: this is a gate for one page.** Two documents exist under `specs/`; a
  four-check apparatus for two files is scaffolding-for-scaffolding, the repo's named
  failure mode. **Answer:** the checks are written against the *record*, not against E-08 —
  C1/C3/C4 resolve the item code from the filename and query the DB, so they apply unchanged
  to every future specifications page, which is the whole point of building the prototype
  first. The alternative on offer was re-reading, which has now been measured at ninety
  misses.
- **Objection: C2 was demoted to WARN, so the print defect could recur silently.** **Answer:**
  it could not — R1 in the browser harness FAILs on it, and that is the check that caught the
  `assets/guidebook.css` defect this DR fixes. The demotion moved authority to the checker
  that can actually see the cascade; it did not remove the check. The residual risk is a
  CI environment with no browser, which is why `run_opt` prints `[SKIP] … this check did NOT
  run` instead of a silent pass.
- **Objection: §3.2 and §3.3 are unenforceable prose, i.e. exactly the level-1 rules that
  the §1 finding says do not work.** **Answer:** conceded, and stated rather than hidden.
  §3.2 is partly mechanised (C4 fires on the specific case that produced it); §3.3 is not
  mechanisable with current tooling and is recorded as a level-1 rule *labelled* level-1.
  A rule that cannot be gated is worth recording only if its status is honest, and the
  enforcement spectrum exists precisely to say so.
- **Objection: the ● on E-08 should have been demoted rather than disclosed.** **Answer:**
  that is a live question and it is not this DR's to settle — the cell's state is governed by
  evidence strength, and `convergence_assessment` 9001 is queued for value-level extraction.
  What this DR fixes is the page asserting more than the record holds. Whether the record
  itself should hold less is §5.
- **Refutation test.** Falsifiable: revert any one of the four fixed defects and
  `scripts/preflight.sh` must go red. Verified for all four before commit.

## 5. Raised, not decided — DG-NON

One rule was drafted and is **withheld** because it is doctrine, and doctrine is owner-only
(`governance/decision-protocol.md` §2.2; mission/audience posture is a named always-DG-NON
type):

> *Proposed:* the non-prescription stance binds **contested values**, not the reporting of
> what a source says. Reporting a source's own figure at the source's own scope is not
> prescription; settling a contested figure on the guidebook's authority is.

It is raised because the audits found the stance being applied asymmetrically — hedging on
uncontested reportage while an actually contested figure stood unhedged, which inverts the
protection the stance exists to give. It is not enacted: the guidebook's relationship to
prescription is the load-bearing commitment of the mission, and an agent tightening its own
definition of it is precisely the move the delegation rules forbid. **Owner decision owed.**

## 6. What this DR does NOT do

- Does **not** touch `data/guidebook.db` — no migration, no row written; the gates are
  read-only against it.
- Does **not** change any evidence state, grade, or cell. The E-08 ● stands as recorded; only
  its *disclosure* changed.
- Does **not** wire the gates into `.github/workflows/` — preflight only, this pass. CI
  wiring is a follow-on that needs a browser decision for `render_audit.js`.
- Does **not** reconcile `specs/e-08.html` against `specs/e-08-brief.html`. The two carry
  divergent figures (1830/3050 vs 1800) with no supersession declared. Known, tracked, and
  out of scope here — flagged so it is not mistaken for something the gate now covers.
- Does **not** decide §5.
