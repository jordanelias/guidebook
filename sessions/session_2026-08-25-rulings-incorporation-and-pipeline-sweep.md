# session_2026-08-25-rulings-incorporation-and-pipeline-sweep

**Opened 2026-08-25 22:00 UTC, closed 2026-08-26.** The immediate successor to
`session_2026-08-25-pipeline-smoke-test-mobility`, and it does the thing that session's findings
demanded: put the owner's rulings into the ledger, and turn "The Severed Walk" from a report into a
plan an implementer can follow.

**No research, no evidence admitted, no migration, no code change.** `sessions/LATEST-RESEARCH` does
not move. `git diff --name-only origin/main HEAD -- data/guidebook.db` returns nothing: this branch
introduces no change to the database of its own. Every measurement below was taken read-only
(`mode=ro`) against the committed DB at `user_version` 64.

Working record: `scratchpad/session_2026-08-25-rulings-incorporation-and-pipeline-sweep/notes.md`
(findings F1–F13) plus the document set under the previous session's scratchpad — see **Provenance**
below, which is a weakness, not a filing convenience.

## What the owner asked, in order

Interrogate the "work from axes" rule, because the owner kept disagreeing with the terminology ·
incorporate the rulings of the preceding week, which a prior presentation had failed to reflect ·
return to the Severed Walk and plan every code deficiency preventing the pipeline from walking ·
adversarially review those plans read-only (Fable 5) for logic, sequence, factuality, walkability,
correctness, with Opus writing · split "mobility" into ambulatory and wheelchair user to start ·
reason out the corrections with specific instructions and code lines · repeat the pipeline and list
the tables specific to each stage with their meaning in project context · then options, commit,
merge, close.

## Owner rulings recorded on contact

Rule 0 says a live owner statement supersedes every prior ratified record it touches, and that the
job on hearing one is to **record the supersession**. Each is now a RULE entry in
`references/project-standards.md` with its quoted wording, its measured basis, and its CONDITION /
ACTION:

- **The person-side demand layer is `icf_demands`, and is NOT folded into `access_needs`.** Resolves
  the two items `DR-2026-08-24` §R8 left explicitly NOT DECIDED. The refusal to fold is measured:
  `axes` anchors ICF **b**/**d** and carries `mechanism`; `access_needs` anchors ICF **e** and
  carries `design_obligation`. The 17/17 row coincidence is a coincidence; folding them would
  collapse person and environment into one table.
- **`MOB` splits into `AMB` and `WHEEL`, and the 31 links fan out to 62.** The fan-out is a
  mechanical carry of the umbrella's union — explicitly *not* a judgement that every demand applies
  equally to both, because resolving them by hand now would decide applicability before synthesis,
  which `DR-2026-08-24` §2.4 forbids.
- **A specification keys from the judgment object and cross-references all three modes** —
  populations, access needs, ICF. Population is demoted from identity to cross-reference. This
  supersedes the `(item × population)` grain that `DR-2026-08-12` renamed but never revisited.
- **The judgment object is the canonical parameter** (2026-08-26), closing the question the ruling
  above left open in the owner's own parenthesis, *"(if we use the word item)"*. `items` is demoted
  to the Part-4 render rollup `conceptual-model.md:92` already calls it, derived from specifications
  rather than keyed by them.
- **The §R8 rename executes together with a retired-vocabulary register entry** (2026-08-26), so the
  token is caught mechanically rather than by remembering.

Two supersessions the owner's directives effected over the 2026-08-19 adversarial-review RULE were
also recorded, scoped to the sessions they cover; the RULE itself is unamended.

## What the plan became

`REPAIR-PLAN.md` supersedes `WALK-REPAIR-PLAN.md` and its three amendments: Phase 0 safety, Phase 1
the forward walk, Phases 2–4 the re-entrant edges, render truthfulness and apparatus honesty, with
an acceptance test that **fails by construction today** — passing it is the definition of Phase 1
done. Code-level detail is not duplicated into it; it lives in `logs/F6-code-fix-design.md` (exact
line numbers, current code, replacement code, refusal sets, migration SQL) and
`logs/F5-population-split-design.md`. The plan adds no register, no workplan file and no check, with
one declared exception whose burden of proof is met in place — §1's test applied to the plan itself.

`STAGE-TABLE-MAP.md` derives every table to its stage under the 2026-08-25 pipeline ruling, as
`CLAUDE.md` requires (*"derive the table-to-stage assignment; do not read one out of a document"*),
with three arguable assignments declared rather than hidden. Its shape is the finding:
**judgment and synthesis hold thirteen tables between them and not one row**, while substrate
outweighs the entire pipeline about three to one.

## Findings this session produced while doing that

- **The command-log hook misfiles a third time, by a new mechanism.** `open_session()` has two
  failing paths: the fast path cannot bootstrap, and the fallback treats a session as closed the
  moment `sessions/<stem>.md` exists — which rule 6 encourages writing early. Then it pins. My own
  first fix had the same defect one door over. Written up in `HOOK-REGRESSION.md`, planned as P0.3
  with two owed test cases.
- **Twelve retired population codes are still taught by live skills.** `validate_population.py:79`
  holds the complete crosswalk and validates the *database*, not the skills. `VIS` is absent from
  `populations` and taught by 12 live skill files. P0 because the mobility batch loads exactly those
  skills.
- **"Delete the 11 unread views" was refused on evidence.** Empty is not dead: a 0-row object is
  unproven, not clean, and a cross-stage view *is* the pointer rule 5 requires. Two of the eleven
  are live pointers.
- **The extraction layer already carries the grain the owner ruled for.**
  `source_value_extractions` has `parameter` NOT NULL with `parameter_canonical`, `population_code`
  and `item_code` all nullable; `specifications` inverts that and holds no parameter column at all.
  `v_value_independence` — the input to `convergence_assessment` — has grouped on
  `COALESCE(parameter_canonical, parameter), population_code` since the baseline
  (`057_baseline_2026-08-12.sql:6693-6701`) with no `item_code` in it. Only `specifications`
  disagreed.
- **The new key has no vocabulary.** `parameter_canonical` has no CHECK, no registry table and no
  writer; its entire specification is a code comment at `schemas/source_value_extraction.py:89`. The
  ruling is recorded with that obligation attached rather than assumed away.

## Corrections this session made to itself

- **I used the retired demand vocabulary in my own prose, four times, in the session that recorded
  its retirement.** The owner caught it. That is the evidence behind the register-entry half of the
  §R8 ruling: a rule enforced only by remembering is the pattern `CLAUDE.md` §2 exists to end.
- **A ledger entry cited §R6 four times; the section is §R8.** Corrected in place and the correction
  itself recorded, because a rule record pointing at a section that does not exist is precisely the
  defect class this ledger catches.
- **A measurement claimed four tables carry a `parameter` column; two do.** Produced by reusing one
  SQLite cursor for an inner query inside an outer iteration, which silently truncates the outer
  loop and reports a subset as the whole. The same bug had reported `axes`, `item_axis_links` and
  `population_axis_map` as absent from the schema.
- **A count of `AX-` values used `LIKE`, which is case-insensitive for ASCII in SQLite**, and
  returned two `source_locators` rows that were `tax-return` inside a URL. The recorded figures are
  `GLOB`: 288 live cells, 249 of them in the four `axis_code` key columns and 39 in free text.
- **A hand-written "Three ordering claims" stood over four.** Removed rather than corrected — §2(b)
  forbids the number, not just the wrong number.

## Provenance, recorded because it is a weakness

This session's **documents live under the previous session's scratchpad directory**
(`session_2026-08-25-pipeline-smoke-test-mobility/`) because they continue that session's document
set, while its **command log lives in its own**. A reader opening this session's directory finds
notes and a log and none of the deliverables. It is the same defect class as the misfiling hook this
session diagnosed: the record of what happened and the record of where it happened disagree.

## next_action

None owed. The batch remains the next action, behind one owner sitting on the four DG-NON items in
the preceding session's record and one PR executing `REPAIR-PLAN.md` Phase 0. **P0.6 — the §R8
rename — now precedes the batch**, because `search_executions.query_text` already carries `AX-` in a
live row: a batch run first writes new rows in retired vocabulary, into rendered search logs sitting
under an `.ignore`d path where the sweep's own grep cannot see them.
