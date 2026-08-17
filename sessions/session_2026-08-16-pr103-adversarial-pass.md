# session_2026-08-16-pr103-adversarial-pass

**Purpose.** Discharge the P3 gate condition Q22's register row set and the owner directed:
the independent adversarial pass on PR #103, per `workplan/2026-08-15-adversarial-brief-pr103.md`.
Focus, per owner direction: **logic, correctness, applicability, interdependencies.**

**Not a research session.** No evidence admitted, no source verified, no synthesis authored, no DB
write, no migration. `user_version` 60 at open and close. `sessions/LATEST-RESEARCH` unchanged.

**Findings first.** Nothing found here is fixed here, per the brief's §4. Six findings; four claims
attacked and survived.

---

## 0. Independence — stated, not assumed

The brief's §0 makes independence the thing that makes the pass worth running, so it is declared
rather than claimed.

**Spent before I started:** I had read the brief itself (including the F1 handed forward on
2026-08-16), and the register's *summary* of the author's own self-review. **Not read before forming
my own view:** `sessions/session_2026-08-15-ratified-unimplemented-sweep.md`, the two doctrine
sections under attack, or `DR-2026-07-13-value-genealogy-and-derivation-handshake`. A1 and A4 are
therefore genuinely cold; **A5 (framing and selection) is partly spent and I do not claim
independence on it** — my verdict there is recorded as an opinion, not a finding.

The previous session declined this pass on exactly these grounds. The owner has now directed it
run. Two deferrals is the point at which the cost of not running exceeds the cost of imperfect
independence, and the honest response is to run it and say which surfaces are weaker.

**What I did that the self-review did not** (the brief requires this, or a zero means nothing): I
read the *ratified DR* clause-by-clause against the doctrine text rather than checking that named
objects resolve; I queried the live DDL for the constraints the doctrine claims; I `git grep`ped for
enforcement code behind each stated discipline; and I tested the vocabulary substitution against the
*semantic* correction it sits on top of, which is a different ratified decision.

---

## 1. Findings

### P1 — HIGH. §4.5 claims structural enforcement that does not exist.

`governance/evidence-architecture.md` §4.5 heads its anti-gaming paragraph:

> **Three anti-gaming disciplines, structural rather than editorial.**

**That phrase is the author's addition.** `DR-2026-07-13-value-genealogy-and-derivation-handshake`
H1 says only "three anti-gaming disciplines (adversarial-review hardening)". The upgrade to
"structural rather than editorial" is a paraphrase that strengthens the claim — and it is false for
all three as built:

| Discipline, as §4.5 states it | As built |
|---|---|
| (a) "a `root_id` **must resolve** either to a `root_ref_id` in `evidence_sources` or to a registered external-root stub" | No FK to `external_root_registry`, no CHECK naming it. Enforcement is a `WHERE` clause inside `v_value_independence`. |
| (b) "*Untraced rows carry NULL `root_id`*" | No CHECK couples `root_type = 'untraced'` to `root_id IS NULL`. It is a convention. |
| (c) "`root_classification_basis` + `contested` — recordably disputable, **not free-text folklore**" | `root_classification_basis` is a nullable free-text `TEXT` column. `contested` has a 0/1 CHECK and defaults 0. |

Verified: `PRAGMA`/`sqlite_master` DDL read directly; and `git grep -l` for
`external_root_registry|root_type|v_value_independence` across `scripts/` returns **exactly one
file** — `scripts/migrations/057_baseline_2026-08-12.sql`, the migration that created them. **No
audit, no check, no validator, no registry entry watches any of this.**

**The logic error is the failure direction.** §4.5 justifies discipline (a) by an *inflation* threat
("so two extractors cannot mint two ids for one root and double the count"). As built, inflation is
indeed hard — but the realistic failure is the opposite and is invisible: a genuine independent
root recorded with an unregistered `root_id` does not error, it **silently drops out of the count**.
The discriminator then reports *lower* independence than the corpus holds, which reads exactly like
a consensus-not-evidence verdict. A mechanism whose whole purpose is to separate best practice from
precedent can currently be made to under-report precisely that, by a typo, with nothing raising.

**Applicability: nil today, which is the argument for fixing it now.** `source_value_extractions`
holds 0 rows. Every constraint above is free to add before the extraction pass and expensive after —
the same cost argument the DR makes for H2's columns, which this document states twice.

### P2 — MEDIUM. §4.5 describes a `v_value_independence` that is not the one in the database.

§4.5: "The discriminator is the view `v_value_independence`: independent roots per (parameter,
population), **counting DISTINCT roots and excluding `committee_assertion`**."

Live view:

```sql
COUNT(DISTINCT COALESCE(root_ref_id, root_id))
WHERE root_type IN ('measurement_primary','participatory_finding','derived_calculation')
  AND (root_ref_id IS NOT NULL OR root_id IN (SELECT root_id FROM external_root_registry))
```

Two divergences, both undocumented:

1. **It is an allowlist of three, not an exclusion of one.** `untraced` is therefore excluded *by
   type* as well as by discipline (b) — safer than described. But any root type added to the
   vocabulary later is **silently excluded**, while the doctrine's wording says it would count. The
   DR's own revision history records these vocabularies being extended once already.
2. **The dedup key is `COALESCE(root_ref_id, root_id)`, not `root_id`.** For in-corpus roots this is
   *stronger* than the DR's `COUNT(DISTINCT root_id)` — two minted ids for one `REF-` collapse to
   one. For external roots the key is `root_id`, so discipline (a) is only as strong as registry
   curation.

Neither divergence is harmful; both are undisclosed, in a document whose §10 sets falsification
conditions for itself. Doctrine should describe the artifact that exists, not the one the DR
proposed.

**Sub-note, inherited from the DR and not introduced here:** `derived_calculation` counts as an
*independent* root. A derivation is by definition dependent on its inputs, so a figure recorded as
`derived_calculation` from the same 1970s anthropometric root can add a second "independent" root to
the very corridor case §4.5 uses as its worked proof. Raised against the DR, not against this PR;
§4.5 restating it without flagging it is a missed catch, not a fidelity breach.

### P3 — HIGH. The Person-Mode semantic correction is applied inconsistently, and this PR's own edit walked past it.

The brief's A3 asks whether the `co1-operational.md` meaning change was ratified in those words, and
whether it was applied consistently. **The first answer is yes** — `DR-2026-07-13-person-mode-
functional-capacity-not-population-range` ratifies "informed by … without being *bounded by*"
verbatim, on a direct owner directive that calls the old wording **"disingenuous and effacing."**
The author's justification is sound.

**The second answer is no.** Four live locations still carry the rejected framing:

| Location | Text | Why it matters |
|---|---|---|
| `references/project-standards.md:14` | "Person Mode = Person-Specific Co-Design (OT assessment **resolves position within the Population-Mode range**)" | The operative rule ledger's *definition* of Person Mode. The vocabulary has been swept to "Population-Mode"; the rejected semantics survive underneath it. |
| `references/project-standards.md:170` | "Person Mode — 'OT assessment **determines position within [range]**'" | The specification **voice convention** — what gets rendered to a reader. |
| `references/project-standards.md:202` | "Tier 2: OT assessment **resolves position within range** based on [functional parameter]" | A mandated **format string**. This is the brief's harder sub-question — *did any behavioural rule key on the old phrasing?* Yes. Every Part 4 specification with a range is required to emit it. It also still uses "Tier 2" as a design-mode name, which is Item V's own target. |
| `skills/item-specification-writer_SKILL.md:129` | "Person Mode: **position within range** determined through co-design" | **This PR edited this line.** The diff changes `- Mode S: position within range…` to `- Person Mode: position within range…`. The author's hand was on the line. |

That last row is the finding. Sweeping the vocabulary off a sentence while leaving the semantics the
owner personally rejected — on the line you are editing — produces a document that *reads as
reconciled*. Before the sweep, "Mode S" was a visible flag that the passage predated the correction.
After it, nothing signals that line is wrong.

### P4 — HIGH, interdependency. The obligation that governs P3 is untracked, and this PR is the third pass to walk past it.

`DR-2026-07-14-person-mode-governance-reconciliation` — itself written because a Fable-5 audit found
the prior correction "materially incomplete" in 10+ locations — closes by deferring:

> Skills, locked `project-standards.md` RULEs, `armature_v4.md`, and reference/pilot artifacts are
> deferred to **a tracked second pass**.

`git grep -l "DR-2026-07-14-person-mode"` outside `decisions/` returns **one file: its own
attestation.** No workplan row. No register row. No `retired-vocabulary.yaml` entry. No check.
**The "tracked second pass" is tracked nowhere.**

PR #103 then edited skills and `armature_v4.md` — that exact deferred file set — for the *vocabulary*
half, without touching the *semantic* half and without noticing the two obligations shared a target.

This is PR #103's own thesis failing on PR #103's own work. Its tripwire exists because "a ratified
decision that named its own single implementation step and did not take it for a month" is this
repo's signature failure, and RV-025's note states the lesson exactly: *"Prose does not check itself,
and a workplan row is not a check."* Here the obligation did not even reach a workplan row.

**The remedy is the one the PR already built**, which is why this is a finding and not a complaint:
the rejected formulations are mechanically matchable (`position within .* range`, `resolves position`,
`determines position within`), so they belong in `retired-vocabulary.yaml` as *repealed formulations*
— which is precisely the extension the 2026-08-14 remediation workplan's commit H already proposes.

### P5 — MEDIUM. A2: the self-review fixed the mechanism and not the judgment.

Converting five file-level exemptions to six line-scoped `[RETIRED-VOCAB-OK]` escapes narrowed the
hole. It did **not** re-adjudicate whether each escaped line is a licensed *mention* or a live *use*.
The same wrong call was re-expressed at finer granularity. Two of the escapes the brief named are
uses:

- **`architecture/page-templates.md:262`.** The table's columns are `№ | section heading | data
  fields | notes`. Row 8 reads `| 8 | Mode S trigger | c.mode_s_trigger, c.mitigation | … |`. The
  column **is** named — in the *next cell*. The escaped text is the **section heading**, i.e. what a
  reader sees on a rendered conflict page. Sibling rows confirm the pattern ("Unresolvable residual"
  ↔ `c.unresolvable_residual`). "Naming the column" is false for this line.
- **`architecture/navigation-modes.md:184`.** A bare `**Sections:**` list with **no field column at
  all**: "7. Mode S trigger and mitigation". There is nothing on that line for the justification to
  point at.
- **`architecture/navigation-modes.md:320`** — `| D-NAV-012 | Mode S framed as expansion (ethics
  rule 7) | D-NAV | DG-MANDATORY |`. A live, mandatory design rule in a live architecture document.
  Possibly defensible as an immutable decision title, but not on the stated grounds.

RV-026's own note prescribes the fix and the PR did not apply it: rename the *heading* to
"Person-Mode trigger", keep the *column* `mode_s_trigger`, and delete the escape when the column
rename lands.

On the brief's other A2 question — is `severity: doctrine` right, or should it be `broken`? —
`doctrine` is correct. Nothing raises on read; the text is simply wrong about what the project calls
its own design scales. `broken` is reserved for identifiers that fail at runtime.

### P6 — MEDIUM. A4: Q21's "DISSOLVED" is a deferral wearing a closure's name, and the deferral is untracked.

`gaps` = 0 rows, confirmed by direct query — the row's factual premise is right. But B5's adoption
gate, as this register's own finding 7 records it, has **four** conditions: migration 017 applied +
skill file committed + **worked-example pilot completed** + ≥1 `gap_mining` row per non-error
outcome. Only the fourth depends on gaps existing. The pilot obligation is about demonstrating the
protocol works, and it is unmet for a reason that is temporary.

The row concedes this two sentences after calling it DISSOLVED — *"B5's adoption gate should be
re-stated against the post-reset gap register when gaps exist again"* — and no tracking row exists
for that re-statement. Same shape as P4.

---

## 2. Claims attacked that survived

A pass that reports only defects has not been run.

- **A4 / Q8 — SURVIVES, independently re-derived.** `git grep -i koontz` across all live paths
  returns **no `Koontz 2017` anchor anywhere**. Every live hit is Koontz **2012** (MOB.md,
  stair-ramp BPC) or Koontz **2010** (`REF-00784`, Tier 3, VERIFIED, with DOI and PMID) — different,
  legitimately cited sources. The row's scoping to "Koontz-**2017**" is precise, not evasive. The
  brief suspected the check stopped at `specs/`; it did not.
- **A4 / Q2 — SURVIVES, and the distinction the brief worried about is preserved structurally.**
  `schemas/conflict.py`'s `unresolvable_consistency` model validator requires every `UNRESOLVED`
  conflict to carry a non-empty `mode_s_trigger`. So "routed to Person Mode" is not lost when the
  status word stops saying it — it is *enforced* at the schema layer, which is stronger than the
  status word ever was. The substitution is owner-ratified (DR-2026-08-14, D-0161, migration 058),
  so the superseding path is legitimate rather than improvised.
- **A1 / "precedent counts documents; evidence counts roots" is NOT new doctrine smuggled in as
  restatement.** It is verbatim in the ratified DR's problem statement. The brief's suspicion fails.
- **A1 / the cultural-claim protection is faithful to what H2 ratified.** Diffed clause by clause.
  The boundary criterion is near-verbatim, including the `co1_source_type` values — and those values
  resolve (`schemas/enums.py:253–262` carries `dpo_research`, `advocacy_position`,
  `peer_reviewed_literature`). The one widening, "flatten" → "flatten, **reduce**, or override", is
  supported by the DR's own language elsewhere ("never require mechanical reduction"). The one
  genuinely unsupported addition is the scope assertion *"it binds every register, every audience,
  and the engine"*, which has no counterpart in the DR — low severity, and consistent with the
  document's own I3, but it is an addition.
- **The `[ENGINE-LAG]` and `[BUILD STATE]` markers re-derive as true.** `specifications` carries
  neither `functional_basis` nor `derivation_paths` (27 columns, checked); `population_icf_links`
  does not exist; `source_value_extractions` holds 0 rows; `external_root_registry` and
  `v_value_independence` do exist. Every build-state claim in the new doctrine is accurate.

## 3. A5 — framing and selection, recorded as opinion not finding

My independence here was partly spent (§0), so this is offered as judgment, not as a verified
finding. The brief asks whether closing Q1/Q3/Q7/Q8/Q9/Q10/Q21/Q22/Q23 while leaving Q5 and Q6 —
the two with the largest consequence for the guidebook's honesty — optimised for closures.

I think the selection was **defensible and the reasoning given is honest**: Q5 and Q6 are D-SCHEMA,
Change-Order gated, and authoring a migration into a numbering range already spoken for is the
unilateral structural move `CLAUDE.md` §5 forbids. That is a real bar, not a convenient one.

What I would say instead is that the *cost* of the selection is understated. Q22 shipped doctrine
that is binding on authors and unenforceable by query, and P1 and P4 above are both instances of the
same thing: this pass closed the items whose deliverable is *text*, and text is the medium in which
this repo's obligations reliably go missing. That is not an argument for having done Q5/Q6 instead.
It is an argument that every text-only closure owes a mechanical tracker in the same commit, and
four of them here did not get one.

## 4. State at close

| | |
|---|---|
| Schema | `user_version` 60 — unchanged; no migration, no DB write |
| Findings | 6 (2 high, 4 medium); 4 attacked claims survived; 1 opinion recorded as opinion |
| Fixes applied | **none** — per the brief's §4, findings precede fixes |
| `run_checks --changed-from origin/main` | PASS, 0 blocking |

## 5. Next

The brief's status moves to DISCHARGED. P1 and P2 are cheap now and expensive after the extraction
pass — they belong with the Group 3 schema batch. P3 and P4 are one piece of work: register the
repealed Person-Mode formulations in `retired-vocabulary.yaml` and give DR-2026-07-14's second pass
a row. P5 is three line-level adjudications. P6 is one register-row rewording plus a tracker.

One process note the brief did not ask for and that outlives it: **PR #103 merged on 2026-08-15
with this gate undischarged.** Everything above is now a fix-forward on `main`, not the revert the
brief's §2 contemplates. Either P3 is a gate and the merge is a deviation to record, or it is
advisory and should stop describing itself in blocking language.

**A near-miss of my own, recorded because a pass that hides them is worth less.** I very nearly filed
a HIGH finding that `source_value_extractions.root_type`'s CHECK was missing `measurement_primary`
and `participatory_finding` — which would have meant the independence view could only ever count
`derived_calculation`. It came from a regex that had silently dropped a line of the DDL. I checked
the raw DDL before writing it down; the CHECK carries all five values and there is no defect. This
is the same truncated-read failure this repo keeps producing, reached from inside the pass written
to catch it.
