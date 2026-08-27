# session_2026-08-27-nomenclature-reconciliation

**Opened and closed 2026-08-27.** A terminology exercise that turned into a schema audit, four owner
rulings, and an adversarial pass that broke most of what the session had just proposed.

**No research, no evidence admitted, no migration, no schema change, no code change.**
`sessions/LATEST-RESEARCH` does not move. `git diff --name-only origin/main HEAD -- data/guidebook.db`
returns nothing: this branch introduces no change to the database of its own. Every measurement was
taken read-only against `user_version` 64.

Working record: `scratchpad/session_2026-08-27-nomenclature-reconciliation/` — `NOMENCLATURE.md`
(921 lines, Parts A–L) and four audit reports (1,172 lines). Reading surface: the *Naming Register*
artifact. Ledger: **six** new entries in `references/project-standards.md`, two recording rulings and
four recording corrections to those records.

## What the owner asked, in order

An outline of names and keys per stage and of everything referred to across stages · then, on seeing
it: *"our nomenclature is all over the place"* — interrogate every table name against its stage and
the project vocabulary, and give each a stage prefix · how a rebuild from scratch would work and why ·
whether citation mining and cross-synthesis comparison need tables or columns · *"I am really
questioning why we have so many tables"* · how rendering should manage diagrams, prose, comparative
tables, precedents and citations · whether a script or skill could generate pages · then the
adversarial pass, and close.

## Owner rulings recorded on contact

- **The pipeline is SIX stages** — *"you research slugs, evidence research, judge evidence, synthesize
  judgments, specify syntheses, and render specifications."* `specification` is a stage again, after
  synthesis. Supersedes the five-stage list of 2026-08-25 and restores `conceptual-model.md:90`'s own
  arrow, unchanged in the entity model since the baseline.
- **Every stage's hand-off object is `<stage>_items`** — *"we don't need to iterate different words
  for item. we just append '-item'."* This superseded the session's own first pass, which had coined
  a distinct noun per table.
- **The cardinality**, quoted in full in the ledger: one slug fans out to many evidence rows, each
  evidence row provides **one** judgment row, and judgments then fan **in** to syntheses and
  specifications.
- **The rename creates the hand-off keys**, rather than deferring them to a second migration.

## The finding the exercise produced

**Not one foreign key in the schema lands on any stage's hand-off object.** `source_locators` and
`bpc_metadata` have zero inbound keys at all; `source_value_extractions` and `specifications` have one
each, both same-stage. Every cross-stage key points at a substrate vocabulary, at `evidence_sources`,
or sideways. Each stage is joined to the next through a shared topic label, not through the thing the
previous stage produced. **The walk has no keys**, which is a deeper defect than the naming and was
not visible until the names were interrogated.

Also surfaced: `best_practice_synthesis` is named in eight governance files and is **not a column** —
`bpc_metadata`'s sixteen columns are all process metadata, and the synthesis itself lives in a file at
`slugs.bpc_path`. No diagram, figure or alt-text column exists in any table, in a guidebook whose
subject is access. And seventeen tables do three things: a lead under four names, an act under four
naming conventions, and six ways to say "X applies to population P" — while **33 of 66 tables hold
zero rows.**

## The adversarial pass, and what it did to the above

Four Fable 5 auditors, read-only, one lens each, each writing its own report — which repairs the
provenance weakness the 2026-08-25 session recorded, where auditors could not write and their findings
were transcribed by hand.

**They broke the proposal, and that is the session's most useful output.**

- **A rule-0 violation in the session auditing rule compliance.** The owner said *"each row of evidence
  provides one row for judgment"* — 1:1. The record said 1:N, justified by citing `DR-2026-08-19` §7's
  dissent mechanism: weighing a ratified record against a live ruling, which rule 0 forbids in the
  plainest terms. A third option satisfying the ruling exactly — a junction with
  `UNIQUE(judgment_item_id)` — was never considered. **Reopened; the owner's.**
- **`ren_items` withdrawn — the owner had already ruled against it.** It re-creates `render_manifest`,
  dropped by migration 046 quoting *"the entire pipeline is dynamic rendering on site"*. That
  migration's header names the pattern it was itself repeating; **this proposal was the third
  instance.**
- **Rule 0 in the other direction: attribution expansion.** `CLAUDE.md` carried "the hand-off is a NOT
  NULL foreign key. Owner ruling" — the owner ruled naming and cardinality; the key mechanics were
  agent design under an owner banner. Corrected, with the derived parts labelled derived.
- **The baseline argument was false on its mechanism**, and untested. Measured on SQLite 3.45.1:
  `ALTER TABLE RENAME` rewrites REFERENCES clauses **and view bodies** automatically. The real limit
  is narrower — you cannot *add* a NOT NULL FK to an existing table — and that touches two tables,
  both empty. Recommendation downgraded to "price a migration series against a baseline."
- **A new baseline would break a blocking gate on first run**: `migration_reproducibility.py:55-63`
  hardcodes counts on `citation_mining`, `connections` and `items`, all renamed or retired here.
- **Parts E and J of the document contradict each other** and both shipped; Part E also still carries
  the NOT NULL back-pointers that Part B replaced with junctions.
- **A live rule-5 violation missed while auditing rule 5**: `evidence_population_match` carries both
  `source_ref` and `ref_id`, identical in all 25 rows.
- **I violated my own standing ACTION within the hour**, leaving a ruled-against item as the worked
  example in five places after writing that it must not be used as an example of anything.

**What held:** all 38 row counts, the zero inbound hand-off keys, the three forward pointers, the
5,318-row stage split and roughly 25 other figures reproduced exactly.

## Corrections this session made to itself

Six ledger entries, four of them corrections. Beyond those above: the cross-stage key count was a
**five**-stage measurement asserted inside the six-stage frame (43/37 on eight columns, not 41/39 on
seven); the cross-stage **view** count depended on a convention never stated (five, not seven, since
substrate is not a stage); `site_pages_fresh` is invoked by `ci.yml:251` and merely advisory, so
"nothing calls it" was false and conflated two different defects; and three smaller figures were wrong
(15 `loc_*` columns, `jurisdiction` on 11 tables, 17 skill files).

## Handoff — what the next session inherits

**Nothing here is executable yet, and that is the honest state.** The naming grammar and the six-stage
spine survive. The key shapes, the rebuild plan and Part E do not.

**Owed by the owner, blocking:**
1. **evidence→judgment cardinality.** 1:1 as ruled, or 1:N to carry dissent — and if 1:1, whether
   dissent lives as a second *graded* row elsewhere.
2. **`judgment_items`' column set.** The only genuinely new table; nothing in the schema prefigures
   it.
3. **Prose in files or in rows** (the `K.6` question), which decides where `syn_items.synthesis` lives.

**Owed by the next session, not blocked:**
4. Reconcile **Parts E and J**, which are a contradiction rather than a plan.
5. Re-derive the caller set for retiring `items` — still incomplete after three passes.
6. Pay §1's burden of proof for `jud_items`, `syn_judgment_links`, `spe_synthesis_links`, or drop
   them: spine integrity is an argument about the apparatus, which §1 rejects.
7. Land the **six-stage spine in the machine** — `governance/pipeline-contract.yaml` and
   `tools/pipeline_completeness.py` still enforce five, so the declared single home of the stage ids
   disagrees with `CLAUDE.md` today.

**Cheap and unblocked, if wanted:** wire `build_site.py` into `regenerate_derived.sh` and promote
`site_pages_fresh` to blocking — green today, no schema change — noting the registry's recorded
condition that it stay advisory until the committed-versus-generated policy is settled.

## next_action

None owed by me. The mobility batch remains the next action, still behind the four DG-NON items in the
2026-08-25 record and now behind items 1–3 above. **A second adversarial pass on the corrected
document would be the loop**; the corrections should be executed, not re-audited.
