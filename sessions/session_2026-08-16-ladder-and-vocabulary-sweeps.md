# session_2026-08-16-ladder-and-vocabulary-sweeps

**Purpose.** Orient against current plans and open items, then execute the ratified work that needs
no owner input. Two items were executed — Q3's doctrinal-content half and Q1's `references/` corpus
remainder. Six findings were produced along the way, four of them in no register.

**Not a research session.** No evidence admitted, no source verified, no synthesis authored, no DB
write, no migration. `user_version` 60 at open and at close. `sessions/LATEST-RESEARCH` unchanged.

**Baseline, measured before any edit** (`scripts/preflight.sh --all`): PASS — 46 green, 13
nothing-in-scope (5 of them blocking and vacuous), 6 advisory failures, 0 blocking. Every claim below
about "no regression" is against that number, not against memory.

---

## 1. The one thing I did not do, and why it is first

`workplan/2026-08-15-adversarial-brief-pr103.md` is the highest-priority open item in the repo: an
undischarged P3 gate condition that Q22's own register row set, that the authoring session could not
meet, and that the owner directed. I was a fresh session and could have run it.

I had already disqualified myself by the time I noticed. Orienting as instructed, I read
`sessions/session_2026-08-15-ratified-unimplemented-sweep.md` including its §8 self-review, and both
ratification registers — which is precisely what the brief's §0 says not to do before attacking the
work. My independence on A1 (doctrine wording) and A5 (framing and selection), the two surfaces the
brief calls hardest, was spent before I read a line of the diff.

I surfaced that rather than running a pass whose independence was already compromised and calling it
discharged. The owner chose to hold the pass for a session that starts cold. **The brief is
unchanged and still binding.** One finding produced anyway (F1 below) is recorded in the brief so
that pass does not spend effort rediscovering it.

The order matters and is worth stating: had I swept first and offered the pass second, I would have
edited the tripwire the pass exists to audit before it was audited.

## 2. Q3 — three skills were teaching the superseded evidence ladder

Ratified 2026-07-13 (A5 item 8); the vocabulary half landed 2026-08-15, the doctrinal half did not.
Every correction is traced to a line in an operative document. None rests on my judgment about what
the ladder *should* say.

| Skill | What it said | What is operative |
|---|---|---|
| `literature-review-planner` §4 | systematic reviews / meta-analyses at **Tier 3**; Tier 2 as "NGO/advocacy"; Tier 4 among "evidence of effect" | `tier-system.md` §2 is titled *"sr_meta placement — T2, not T3"*; `schemas/tier_derivation.py:57` maps `sr_meta` → 2; T4–T6 are the regulatory stratum (§3, §8) |
| `supersession-audit` §2 | the whole search-strategy matrix keyed to the old ladder — **and self-contradictory**: `national_fw` appeared under both Tier 2 and Tier 5 | `tier-system.md` §1: T2 is `sr_meta` / `standard_eb`; `national_fw` is T5 |
| `evidence-auditor` | the retired two-marker ●/○ scheme, plus a note reading *"a claim citing only a systematic review or RCT … is MODERATE, not STRONG"* | `tier-system.md` §5 has three markers (●/◐/○); §8 puts T1 and T2 in the ● full band, anchoring outright |

**These are not cosmetic.** `supersession-audit` drives which database gets searched for a superseding
source, keyed by tier. `evidence-auditor`'s note downgrades T1 and T2 evidence at the point where a
session decides whether a claim is overclaimed. A skill that grades evidence with a ladder the
project retired fifteen months of doctrine ago produces confident wrong answers, and does it silently.

**A hole the correction created, and filled rather than left silent.** Relabelling `sr_meta` from
Tier 3 to Tier 2 in `supersession-audit` would have left the tier that *actually* holds
lower-control `clinical` and `grey` with no search strategy at all — silently dropping every genuine
T3 anchor out of supersession scope. I added a Tier 3 section and marked it in place as derived from
the skill's own existing T1 and organizational-catalogue strategies rather than researched fresh,
open to owner revision on that basis. Writing it unmarked would have passed off a mechanical
derivation as method.

**Two of the row's four named targets were stale.** `item-specification-writer` was already swept
(it carries the three-marker table and a note retiring the two-marker scheme). `cell-curator`, the
row's *first* target, no longer exists — renamed `specification-curator` per DR-2026-08-12. I
corrected the row rather than re-doing work that was done.

**What I did not sweep, having checked.** `skills/multilingual-research_SKILL.md:62` reads "Tier 2
(disability-led NGO/advocacy)", which looks like the same defect. It is not: `governance/research-
contract.yaml:70` — operative — uses the same formulation deliberately. Consistent with the contract
is not the same as wrong, and I left it.

## 3. Q1 — the `references/` corpus remainder

Counted, not remembered. **RV-025/026 read 33 occurrences before the sweep and 2 after; the register
total went 101 → 70.** Sixteen files across BPC, conflict-matrices, fdr, connection registers and the
throughline documents.

**The two survivors are one line of `site/rooms/r_ba.html`** — generated output. `CLAUDE.md` §10
forbids hand-editing it, and its regeneration is entangled with the room-stratum retirement question
(remediation workplan §6, HOLD). Reported, not touched. A sweep that reported 33 → 0 by editing a
generated file would have been a worse outcome that read better.

**Four sites carried the other half of Item V** — "Tier 1" and "Tier 2" used *as design-mode names*,
which is the evidence-ladder collision the item exists to end, not merely the Mode P/S spelling. Each
was resolved from the sentence's own gloss, never inferred:

- `bpc-scope-review.md:138` — "Tier 1 → Person-Mode handoff point: **the BPC provides population
  medians**" → Population Mode.
- `throughline-audit-notes.md:21` — "**OT assessment** is the Tier 2 resolution" → Person Mode.
- `workplan/a6-handoff.md:75` — "what governs at Tier 1 **(population-informed)**" → Population Mode.
- `governance/armature_v3_review.md:129` — a visual-distinction question between the two design modes.

**Three dated-but-live records were swept, and I am naming them because it is a judgment call.**
`bpc-scope-review.md` (2026-03-29), `governance/armature_v3_review.md` (2026-04-27) and
`workplan/a6-handoff.md` (2026-04-29) are dated analyses. They sit in *live* locations, not in the
frozen directories the root `.ignore` covers, so a session greps them and gets an answer; the rename
is ratified in full. The opposite argument — that a dated record should read as it read on its date —
is real, and if the owner takes it, these three revert. Stated so it is arguable rather than silent.

## 4. Findings

**F1 — the tripwire under-counts, and the probe that should have caught it was read backwards.**
RV-025/026 use `match: phrase`, so the hyphenated adjectival forms **`Mode-P` / `Mode-S` match
nothing**. A live use sat uncounted at
`references/bpc/kitchens-and-workspaces/residential-kitchen-and-task-surfaces.md` — *"Mode-S
co-design assesses the user's specific chair geometry"* — plus two more in a file the audit saw only
for its unhyphenated hits. The sharper half: the 2026-08-15 session's 14 boundary probes **included
`Mode-P`** and recorded "no false positive or false negative". The probe fired and its result was
read as confirming the matcher, when what it showed was a blind spot. That is a finding about probe
design, not only about a regex. Uses swept; **tripwire unchanged** — adding the variants needs a
file-level exemption for an immutable committed migration comment, the coarse instrument F2 warned
about, and that is a call the pending adversarial pass should weigh. Severity: **medium**.

**F2 — the migration-number allocation on the active remediation plan is stale, and would collide.**
`workplan/2026-08-14-remediation-workplan.md` §1 allocates 058/059/060 to `constraint_floor` /
`jurisdictional_values_provenance` / `claim_capture_uniformity`. Those slots are taken on `main` by
`058_status_vocabulary_ratification`, `059_tier1_retirements`, `060_restore_superseded_status`. A
session executing that table collides on its first migration. Worse, `workplan/2026-08-15-instrument-
status-backfill-plan.md` §6 **already observed** "058–060 are used" — and did not correct the table it
was reading from, so the defect survived the one pass that saw it. Corrected in place with a
re-allocation (058→061 … 063→066) flagged as not re-prototyped at the new numbers. One row needs more
than renumbering: `059_tier1_retirements.sql` on `main` **is** the Tier-1 batch the table listed at
065, so that row must be re-derived against what shipped. Severity: **medium**.

**F3 — the live PI's synthesis gate matches nothing.** `governance/project-instructions-v10_14.md`
gates Phase-B ordering and rule #10 on `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.
`UNVERIFIED-1` was retired 2026-08-04 (RV-012). The identical defect was swept out of
`gap-driven-mining_SKILL.md`; the PI kept it. The PI is not API-writable, so this is a **proposal for
owner decision #9 (PI v10.15)**, not something to execute. Severity: **medium** — a synthesis gate
that matches nothing is the repo's named recurring failure mode, in the document every session loads.

**F4 — the corpus still carries source-level tier labels from the pre-2026-05-25 ladder.** The
`sr_meta` → T2 canonicalization migrated four DB rows in May. The *prose* was never swept:
`references/bibliography-v11-draft.md` (×2), `references/bpc/ALL-ENV.md`, `references/bpc/DEM.md`,
`references/theory-gap-analysis.md` and others label named systematic reviews "Tier 3". This is
**not** a vocabulary sweep — it is re-grading evidence, source by source, and `evidence_sources` is
0 rows after the clean-room reset, so the prose is the only place these gradings survive. Recorded,
not touched: re-tiering sources is research/owner territory, not a mechanical fix. Severity: **low
as to urgency, high as to eventual scope.**

**F5 — `governance/mission-PROVISIONAL.md` teaches the old ladder from a live location.** Lines 49
and 59 give "Tier 3 | Systematic reviews and meta-analyses". The file is marked PROVISIONAL and is
superseded by `mission-and-epistemics.md`, but it sits in `governance/` where it is greppable and is
named in `CLAUDE.md` §9 guardrail 2 as a redirect-stub case. Retiring or stubbing it is owner-gated
(guardrail 4), so it is reported. Severity: **low**.

**F6 — a fourth vocabulary is still live.** `references/bpc/cross-population/cross-population-
conflict-resolutions.md:57` reads "Mode-6 / Tier-7 arguments" — the legacy guidebook-auditor
seven-tier scheme, which is neither the current ladder nor the design-mode vocabulary. Out of scope
here; registered as a finding rather than swept, because a fourth vocabulary needs a decision about
which entry retires it, not an ad-hoc substitution. Severity: **low**.

## 5. What I deliberately did not touch

Everything owner-gated stayed untouched, and nothing here needed a Change Order: Q5-H2/H3/H4 and Q6
`instrument_status` (D-SCHEMA), E10 ICCT (same), E9, E11 (doctrine-SHA cascade), Q15,
`schema-reconciliation.md`'s currency value, §5 of DR-2026-07-25, and owner decisions #1–#10 in the
remediation workplan. No migration was authored; the numbering remains spoken for by a batch queued
for owner decision, and slipping one in is the unilateral structural move `CLAUDE.md` §5 names.

## 6. State at close

| | |
|---|---|
| Schema | `user_version` 60 — unchanged; no migration, no DB write |
| `retired_vocabulary` | 101 → **70** occurrences; RV-025/026 33 → **2** (both on generated output) |
| `run_checks --changed-from origin/main` | PASS, 0 blocking |
| Advisory failures | unchanged from the pre-work baseline; none introduced |

## 7. Next

The PR #103 adversarial pass, by a session that starts cold — it is still the top item, and F1 is
waiting in the brief for it. Then owner decisions #1–#10, with F2's renumbering folded into #4 and F3
into #9. Then the remaining executable ratified work: Q13, Q19, and E10 if its migration slot is
ratified.
