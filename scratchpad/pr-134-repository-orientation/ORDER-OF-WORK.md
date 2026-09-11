# Order of work — produced by a read-only Fable 5.1 pass, 2026-09-10

Commissioned under the owner's standing posture (*"I want it to decide as much as possible. I'm an
overseer"*). The agent was steered mid-run to DECIDE rather than present options, and to minimise the
escalation set to what `CLAUDE.md` §8 genuinely reserves. It wrote nothing; this file is the
orchestrator's persistence of its report.

## The order

```
W0  Batch 06 — ramp gradient (TERM-001) × MOB           <- FIRST. Nothing precedes it.
    |- parallel, code-only, no DB touch:
    |    P1 delete the two dead specification-stage skills + prose sweep (B6)
    |    P2 CLAUDE.md §4/§6 residue (audit Task 6)
    |    P3 jurisdiction normalisation (audit Task 4)
    |    P4 grain promotion into schemas/directness.py (audit Task 1)
    |    P5 delete validate_items; one non-vacuous parameter invariant (Task 7)
    |    P6 db.py refusal residue (Task 8.1/8.2/8.3/8.5; 8.4/8.7 closed; 8.6 verify)
    |    P7 cull the by-construction-vacuous blocking gates and item-keyed renderers
W0a Batch 06 antagonist (fresh session, read-only)      <- after W0's migration commits
W1  B5b completion: scope on the four NULL rows, REF-00784 re-grade  <- after W0 (DB; serialise)
W2  Supersede design (schema + engine)                  <- on W0a sustaining a finding
```

DB-touching work (W0, W1, W2) is strictly serial: every open PR touching `data/guidebook.db`
inherits a binary conflict when the scheduled cron fires (`CLAUDE.md` rule 3). P1–P7 touch no DB.

## The decision that matters — batch 06 goes FIRST

The agent tested this rather than asserting it. It enumerated everything that could change the
outcome of `ramp gradient × MOB` and checked each against the open register:

| Could change the cell | Open item | Effect |
|---|---|---|
| grain of an anchor | P4 | **none** — both anchors are `clinical`; both implementations return `specific` |
| jurisdiction richness | P3 | **none** — no T4–T6 source extracted; that branch is unreachable |
| tier gate | W1 / B5b | **none** — both anchors already `high_control`, consistent |
| value directness | — | `NOT_ASSESSED` by rule; no open item touches it |
| re-determination | W2 | irrelevant to a first determination |
| skills / CLAUDE.md prose | P1, P2 | not read on the walk; the runbook is the procedure |

**The cell's outcome is invariant under every open apparatus item.** So the unrepeatability of a
first determination — the strongest argument for waiting — is answered not by waiting but by choosing
a cell whose outcome cannot be moved by the waiting. Ordering apparatus first would make this the
fourth session this month to commit something other than search logs, migrations or a rendered
determination, which `DR-2026-08-19` §11 property 5 names as the plan failing its own termination
test.

## The parameter — `ramp gradient` (TERM-001), promoted not minted

**And this supersedes the `turning diameter` choice in `BATCH-06-PLAN.md`, which carried a defect.**
`TERM-003 'turning circle'` already exists ("Minimum space for wheelchair 360° rotation"). The plan's
`add-term "turning diameter"` would have minted a near-duplicate beside it — the clash check is an
exact `lower()` match (`db.py:3103`) and sees nothing — and step 4 would then have adjudicated
observation 9, whose surface form *is* TERM-003's canonical name, to the new term. **A rule-5 dual
home created through the sanctioned writer.** Verified: `select term_id, canonical_en from terms where
canonical_en in ('ramp gradient','corridor width','turning circle')` returns TERM-001/002/003, and an
exact-match count for `'turning diameter'` returns 0.

`TERM-001 'ramp gradient'` — "Slope of an accessible ramp expressed as ratio or percentage", value
free, 37 aliases including EN `incline` and `gradient`. Its two anchors both **measured this parameter
as their independent variable** and both are `clinical / high_control / T1`, consistent under
`check_tier_consistency`:

- **REF-00973** varied treadmill inclination 0°→4.8°; its Conclusions name "slope steepness for
  entering a building" as the design recommendation it informs.
- **REF-00974**'s protocol is propulsion at different speeds and inclines, ascending and descending
  ramps, with descending the second-highest shoulder load measured.

`add-parameter` accepts a base-vocabulary term with no adjudication by design, so "minted" includes
promoting TERM-001. **Note `term_aliases.language` is stored lowercase (`'en'`) while
`search_executions.language` is uppercase (`'EN'`)** — a query filtered on the wrong case returns
nothing and reads as absence.

**One lens, MOB.** A second lens is a *different cell* under `idx_spec_row_identity`, and with no
supersede path two half-cells for one determination is a fragmentation the repository would carry
forever. The access-need cell is a later cell in its own right.

**`corridor width` (TERM-002) is batch 07's cell**, after W1 makes REF-00784/971/972 anchorable —
today it would anchor only on a Co-1 survey option phrase while the three sources that actually
measured corridor geometry sit non-anchoring. It is also the E-08 name.

## The one apparatus edit that IS on the batch's path

**The runbook has no `add-extraction` step** — verified, 0 occurrences. A session following it
literally writes no extractions, and after B4 `gather_sources(conn, parameter_id)` returns only
sources holding an extraction, so the cell comes out `pending` on an empty governing set. Fixed
inside the batch's own first commit, executed before written.

## Escalated — one "yes" ratifies both; nothing waits on either

1. **`high_control` means experimental control over PARTICIPANTS, not over the rig.** Device bench
   tests with no disabled participant are `lower_control` (T3). *Reason:* every exemplar in
   `governance/tier-system.md` §1 and `schemas/tier_derivation.py:13-19` is a design on people, and
   these rows' own population grades say nobody participated. *Cost if wrong:* REF-00971/972 sit at T3
   when they should be T1 — one compensating migration promotes them, no cell is lost.
2. ~~**`base_taxonomy_medical` stays empty; the medical lens is explicitly deferred.** *Reason:*
   population taxonomy is owner-reserved, no batch needs it, and D-0182's at-least-one CHECK keeps
   every table writable without it. *Cost if wrong:* none — a medical-lens cell is a new lens tuple
   addable later without touching existing cells.~~
   **WITHDRAWN 2026-09-11 — it escalated a question already ruled.** D-0170 adopted the medical lens
   on 2026-08-27 (*"yes we include the medical model too. we give our users the choice of what model
   they want to use to browse the site"*), so this was never an open item and the "cost if wrong" was
   not none: it was eight hours of a ratified lens staying empty. Struck in place rather than deleted,
   because the failure is the instructive part — the search stopped at the first answer it found, and
   the first answer was an empty table. `CLAUDE.md` §6 documents the identical failure on the subject
   half of the cell key. Recorded in D-0188's `notes`; the text above is preserved unedited.

**De-escalated, with reasons** — the agent tested each against §8 and dropped it:

- **B5b's four `scope` rows and REF-00784's tier.** `scope` is a session-set field at admission and
  `amend-source --field scope` is the sanctioned late path; setting it from bytes is the same act.
  Only the *reading* of `high_control` is a tier-definition question, and that is escalated above as
  item 1. Applying the ladder per row is what batch sessions do at every admission.
- **The supersede design.** A supersession column and an engine flag are schema and code, which §8
  does not reserve. `grep -rn -i 'supersede design\|re-determination' sessions/ decisions/
  references/project-standards.md` returns **no owner ruling** — the "owner decision" wording in the
  runbook and road-to-batch-06 is session-authored. *This corrects my own earlier statement that it
  was an owner call.*
- **The batch's parameter and lens.** A session's research judgment under an ACTIVE slug.
- **A new slug.** None is proposed, so there is nothing to ratify.
- **The two skill deletions.** Process apparatus; §8 lists code, checks and scripts as deletable on
  evidence rather than permission.

## Delete rather than fix

| Object | Evidence |
|---|---|
| `skills/item-specification-writer_SKILL.md` | wholly item-keyed (`:40,52,59`); subject emptied 2026-09-01; callers are retired prose only |
| `skills/specification-curator_SKILL.md` | teaches hand-populating state per (item × population); the owner ruled the state computed |
| `scripts/validate_schema.py` | **blocking**, and `ENTITY_REGISTRY = {}` (`:63`) — vacuous on *every possible input*, a different defect class from "corpus empty by decision" |
| `scripts/audit/check_rendered_docs.py` | blocking; subject is reference-only `specs/*.html`; the live render path is DB → generator, so it can never gain a subject |
| `population_page.py`, `spec_page.py`, `pilot_renderings.py`, `register_integrity_check.py` | raise or fake against the live DB; none called by `regenerate_derived.sh`. **`room_page.py` stays** — owner-parked on decision 8 |
| `scripts/validate_items.py` | reads `items`, 0 rows by ruling, red forever with `EXAMINED: 0` |
| audit tasks 8.4, 8.7 | no reader for the index; no defect in the view |

Named but NOT deleted: `evidence_sources.tier` and `specifications.governing_refs` — both rule-5
copies, both hashed or read by K01. Writer-retire → reader-retire → NULL forward, after W2.

## Where it corrected the orchestrator

1. The supersede design is **not** owner-gated — no ruling exists.
2. B5b's four rows are **mostly not** owner-gated — application of the ladder, not definition.
3. `turning diameter` would have created a dual home with TERM-003. **The defect was in my plan.**
4. "The only two sources stating turning geometry" is true of the *logged payloads* only; REF-00784's
   abstract was never retrieved, and the repository's own records describe it measuring passage width
   and manoeuvring.
5. `validate_schema`'s vacuity is by construction, not by corpus — which makes it a deletion rather
   than a wait.

## Open uncertainties it flagged rather than papered over

- Whether `assess_cell.py` refuses an unknown `--slug` (task 8.6) — settled by one grep.
- Whether `validate_evidence_state` / `validate_verification_consistency` are green on their first
  non-vacuous row — only W0 answers it.
- Why `validate_pydantic_schemas` and `test_verification_pipeline` fail advisory today — not examined;
  neither is on the walk.
- Whether the owner regards SKILL files as doctrine rather than process apparatus (P1's STOP).

---

## CORRECTION to escalation item 1 — found by reading the payloads, 2026-09-10

**Item 1 as drafted is wrong, and it is withdrawn in that form.** It read: *"`high_control` means
experimental control over PARTICIPANTS, not over the rig. Device bench tests with no disabled
participant are `lower_control` (T3)."*

**What the ratified ladder actually says** (`schemas/tier_derivation.py:16-21`, citing
`governance/tier-system.md` doctrine SHA 373255e and decisions D-A/D-D/D-E):

> `high_control` → Tier 1 — *intervention / RCT / **biomechanical** / sensory-threshold studies. Per
> D-E, directly-relevant high-control non-OT primary research is admitted at T1, not demoted.*
> `lower_control` → Tier 3 — *cross-sectional, observational, qualitative, single-centre.*

The discriminator is **study DESIGN control**. It says nothing about who the participants are.

**The case that exposed it.** REF-00974's payload (`44993333b75d5477.xml`) reads *"Ten able-bodied
participants performed these activities while their upper extremity kinematics and exerted forces
were measured."* Under item 1 as drafted — participants, but none disabled — REF-00974 becomes
`lower_control`/T3, which contradicts its stored T1, which makes it **tier-inconsistent and therefore
NON-ANCHORING under B5a**, which removes one of the two anchors from the very cell this order of work
selects. The escalation would have knocked out the batch it was written alongside.

**Why the drafted reading is wrong rather than merely inconvenient.** It conflates two axes the
architecture separates on purpose:

- **Design control** → `scope` → tier. A biomechanical protocol with instrumented measurement is
  `high_control` whoever performs it.
- **Population of study vs population served** → `evidence_population_match` → conditioning and
  weight. REF-00974 is already graded **PROXY on MOB** for exactly this reason
  (`select ref_id,target_population,match_grade from evidence_population_match where ref_id='REF-00974'`).

Demoting the tier *as well* would count one fact twice — once as a tier demotion and once as a match
grade. That is rule 5's dual-home objection in a different guise: the fact that no disabled person
participated already has a home, and it is the match row.

**So REF-00974 stays T1 / `high_control`, and the cell keeps both anchors.** REF-00973 independently
verifies: `19194f9d0d6f8fe6.xml` carries DOI `10.3390/s23218659`, *"inclination of which varied
between (0° to 4.8°)"*, *"recommendations, such as those regarding slope steepness for entering a
building"*, and **17 spinal cord injury participants** — a controlled biomechanical protocol on
disabled participants, `high_control` under any reading.

### Escalation item 1, RE-DRAFTED

**`scope` discriminates study DESIGN control only; whether the study population is the served
population is graded separately and never moves the tier.** So the question for REF-00971/972 (the
Toronto mobility-scooter pair, and the actual subject of the original item) is not who participated
but what design was run: a bench measurement of device geometry is `lower_control`/T3 as
*observational*; an instrumented protocol with a controlled independent variable is
`high_control`/T1 as *biomechanical*. W1 must answer that from the payloads, not from participant
identity.

*Reason:* it is what the ratified ladder says, in the file that implements it.
*Cost if wrong:* one compensating migration on two rows; no cell is lost either way, because
REF-00971/972 are not anchors of the ramp-gradient cell.

**This is a smaller ask than the original, and it may not be an owner question at all** — it is the
ladder read as written rather than a new tier definition. It is left in the escalation block only
because the original was put there, and because W1 needs the reading settled before it writes.
