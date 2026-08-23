# Wave 6 — Method

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Six live rules land in `references/project-standards.md`, with one paired Decision Record.**
**They must not land in a workplan document again — three of them already lived there and died.**

---

## Status ledger

| # | Status | Disposition |
|---|---|---|
| W6.1 | **DONE** | `scripts/tests/walk_harness.py` exists; Wave L generalises it. L4 imports its log as `plan_item: W6.1` |
| W6.2 | **DONE** | the review's log-identifier citation |
| W6.3 | **DONE** for the harness | `ast.parse()`-as-green fixed there; the general rule survives inside W6.6/I4 |
| W6.4 | **LIVE, but not a standards rule** | folds into **W5.4(c)** — `--corpus` mode plus `attestation_corpus` registered advisory with `EXAMINED:` |
| **W6.5** | **PENDING and unrouted** | the plan marks it pending and sends it nowhere. **Record it as a scope note in the paired DR** rather than losing it a fifth time |
| W6.6–W6.11 | **LIVE** | six RULE blocks + one DR, below |

---

## The house style, verified

`references/project-standards.md:2` — *"Append new RULE blocks at bottom. Never overwrite existing
entries."* It is append-only, managed by `session-consolidator`. The recent 2026-07-25 cohort at
`L584-629` uses the shape: `RULE:` (long body naming provenance and the paired DR) / `CONDITION:`
/ `ACTION:` (numbered) / `DATE: YYYY-MM-DD — provenance`, appended with no section heading,
blank-line separated.

**Append after `L630` (current EOF).** The full drafted text of all six blocks — in that exact
format, each naming its provenance instances and its paired DR — was produced by this
decomposition and should be transcribed verbatim at execution; the substance of each is below.

---

## The six rules

### W6.6 — A regex classification is a candidate list, never a finding
**Six instances in one review cycle, each inflated until the real thing was run:** 14 "unknown
rule ids" (really 8 — the regex ignored `EXTRA_RULE_IDS`, the allowlist the real check consults) ·
77 "avoidable" f-string SQL interpolations (really ~0 — all safe identifier-interpolation idioms;
a security-shaped non-finding) · a table-type classifier putting 56 of 66 tables in one bucket ·
a source document nearly dropped from a reconciliation because it uses prose headings, not IDs —
**which silently drops any source that does not use IDs** · "4 attestations cite
`integrity-protocol`" (really **zero** — a whole-file string grep hitting artifact paths and
`bias_direction` prose) · an 82-file "unreferenced" list (really 26).

**ACTION:** label the output CANDIDATE until each member is adjudicated by the real mechanism;
record candidates in the ledger's `cull_candidates_raised` and confirmations in
`cull_candidates_adjudicated` with the confirming command; **never let a candidate count into a
headline, a register row, or a plan item's evidence column.**

### W6.7 — Before building a detector, check whether one exists — quarantine list included
**The repository has paid twice.** `assess_cell.py` re-implemented `next_gap_id` and got the
schema wrong (`GAP-1` against `^GAP-\d{3,4}$`) while `db.py:149` already held the correct
zero-padding version. And `jurisdictional_divergence.py` sat quarantined — *correctly*, as a
surfacing tool whose exit code carries no verdict — while its defect class was re-reported as new.
**"Not a gate" was read as "not run."** Quarantine is terminal for **retirement**, not for
activation; de-quarantine-to-active is an established move performed five times.

**ACTION:** search `check-registry.yaml` **including its `quarantine:` block** and `scripts/`
(`db.py` first) before writing a mechanism; record the search command and result in
`detector_checked` / `detector_search_command`.

### W6.8 — A proposed detector states its confound; not registry-expressible is evidence not to build it
The ~75%-with-enforcer vs ~50%-without correlation is **consistent with the enforcement spectrum
working, not proof of it**: enforcers may have gone to conventions already judged important and
partly fixed by hand. **And the build test is registry-expressibility** — a check that cannot be
an entry in `check-registry.yaml` invoked by `run_checks.py` is a fifth register wearing a
script's clothes (guardrail 3).

### W6.9 — Every supersession publishes a loss-audit
**Four consolidation generations each lost findings**, and every loss was a supersession that
recorded what it kept and not what it dropped: an owner gate dropped in transit, a re-enumerated
fix list folded away, a lower-effort variant carried only in prose. §0.4, §0.6 and §0.7 are the
worked instances.

**Mechanised:** a correcting entry is forward-only, carries `supersedes:`, and its `loss_audit:`
block is **mandatory — enforced by a CHECK constraint in the `work_log` DDL.**
**"Nothing lost" is a claim requiring the enumeration that proves it, not a default.**

### W6.10 — A correction that does not propagate is not a correction
**This is CLAUDE.md §0 rule 5 — the caller sweep — applied to prose claims.** "Five false values"
propagated through three documents while the true count moved to six, then eight, then nine. The
×27 headline outlived its own recalibration.

**ACTION:** sweep with `git grep` (**ripgrep honours `.ignore` and will miss frozen dirs — which
are legitimately left as written**); fix every live carrier or list it in `deliberately_not_swept`
with a reason each; record falsified documents in `prose_orphaned`.

### W6.11 — Re-derive facts, not only arithmetic
**Revisions 1–3 each recomputed the predecessor's sums and inherited its observations.** Revision
4 re-ran the observations and **31 claims did not survive, four premise-level** — the plan was
ordering work against a repository that no longer existed. **Trusting a report instead of running
the detector is the same defect at document scale.**

**And this decomposition is the rule's next instance:** running it again moved W5.1 from 8 rows
to **9**, W7.4's sweep from 12 files to **26**, W7.9 from one broken view to **three**, and W7.8's
baseline from 74 files to **75** — the last of which went stale *during authorship*.

---

## The Wave-L block mapping — and the gap the plan leaves

| Rule | Ledger block |
|---|---|
| W6.6 | `cull_candidates_raised` / `cull_candidates_adjudicated` |
| W6.7 | `detector_checked` + `detector_search_command` |
| W6.9 | forward-only `supersedes:` + `loss_audit:` |
| W6.10 | `prose_orphaned` + `deliberately_not_swept` |
| W6.11 | the `intent_written_at` / `executed_at` delta + `checks_before`/`checks_after` |
| **W6.8** | **none — and that is deliberate.** Its enforcement locus is `check-registry.yaml` itself (the rule's own registry-expressibility test). **Record it in the DR so the omission reads as a decision rather than a drop** |

---

## The one paired Decision Record

**The CS8 pairing requirement is verified at two sites:** `references/project-standards.md:545`
(*"every new RULE in project-standards pairs with a Decision record from this point forward"*) and
`governance/decision-protocol.md` §6.1. **One DR covers all six rules** — the plan says so, and
the protocol's own discriminator is one rationale, one record.

- **Filename:** `decisions/DR-2026-08-12-method-rules-and-execution-ledger.md`
- **Category:** **D-METH**
- **Delegation:** **DG-REVIEW** — a *recorded departure* from the D-METH new-methodology default
  of DG-NON, with the `delegation_rationale` that the substance descends from an owner
  requirement already given (the 2026-08-11 ledger directive), so the session is **capturing
  owner-directed method, not originating methodology.** Review completes via the ratified
  merge-implies-ratification rule (`project-standards.md:578`). `review_status: PENDING` until
  merge.
- **Body sections:** the decision (six rules) · rationale, with the three alternatives refused
  (leave them in workplans — refuted by their own history; encode only as ledger fields —
  insufficient, because these bind *documents* and *measurements* made outside any change;
  one-DR-per-rule — six records for one decision event) · the mechanisation map above, **including
  W6.8's deliberate absence** · scope notes carrying **W6.4's discharge at W5.4(c)** and **W6.5's
  unrouted PENDING status**, so it survives W7.12's retirements · reversal by a new dated block,
  never a rewrite.

**Commit hygiene:** the DR touches `decisions/` — **synthesis path: doctrine token plus
`attestations/dr-2026-08-12-method-rules-and-execution-ledger.json`.** The
`references/project-standards.md` commit does **not** (not a synthesis path). They may share a
commit only if the token is carried.

**Risk to name in the DR itself:** DG-REVIEW vs DG-NON is arguable. If the owner regards these as
*new* methodology rather than capture of the 2026-08-11 directive, the delegation upgrades to
DG-NON and the DR waits for explicit sign-off instead of merge-ratification. **The
`delegation_rationale` field exists precisely to make that visible for review.**

---

## Verification

`python3 scripts/decision_capture.py` passes (C7's RULE-coverage sees the pairing; note CS8 also
expects a `data/decisions/decision_register.yaml` row via session-consolidator — the DR's field
set maps 1:1 onto protocol §3.2, so the register row is mechanical).
`grep -c "DR-2026-08-12-method-rules" references/project-standards.md` → **6**.

## Falsifier

`decision_capture.py` C7 warns that a new CANONICAL RULE lacks a Decision record — meaning the
register row was skipped. **Or any of the six blocks edits an existing entry rather than
appending**, which violates the file's own header contract.
