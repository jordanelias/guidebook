# DR-2026-08-06 — Clean-room evidence reset: the frame stays, the corpus becomes reference

**Category:** D-OP (with D-DOCT consequences) · **Delegation:** DG-NON — work-product
inclusion/exclusion and trajectory are owner-only
**Status:** ADOPTED, 2026-08-06 · **Decided by:** owner
**Executed by:** `scripts/migrations/data_20260806222208_2026-08-06-clean-room-reset.sql`

---

## Decision

The project proceeds **as though no research has been performed.** The frame stays
live; everything research produced is preserved and demoted to reference.

**The frame, as the owner defined it:**

1. **Research topics** — `slugs`, organised by disability population / access need /
   functional impairment against the built environment, design and architecture
2. **Languages**
3. **Aliases and terminologies within languages** — for topics and for the concepts
   associated with topics
4. **Jurisdictions**, national and international

Plus the taxonomy that gives those topics their axes (`populations`, `axes`,
`access_needs` and their maps), the design-parameter categories (`items`), and
`jurisdictional_values` — the recorded code values, which are cited correctly for
their class and are **not** research output (see §3).

**Live after the reset: 4,250 rows across 21 tables.** Reset: 11,849 rows across
38 tables.

---

## §1 Why

Not because the work was poor. Because the corpus could not show its work.

| | |
|---|---|
| sources with no recorded admission | **824 of 863** |
| item×population cells determined | **15 of 2,139** |
| governing references carrying a population grade | **3 of 61** |
| reasoning docs (the primary deliverable) | **1** |
| fully-evidenced walks, topic → best practice | **0 of 306** |

The project's constitutive claim is that any published best practice can be walked
backwards to the values it rests on, the sources those came from, the population it
serves, and the doctrine that governed the judgement. Not one cell could do that.
A corpus that cannot show its work is **reference** — useful to consult, not ours
to assert.

Setting it aside costs nothing that was load-bearing and removes the single largest
source of wrong answers in the repository. The measure is immediate: the blocking
`test_db_integrity` gate had carried six owner-gated content failures for weeks
(I2, C02, C03, C04, D05, G02). **Every one was evidence-metadata debt. The suite is
now 70/70**, and `scripts/preflight.sh` passes with zero blocking failures for the
first time since the check registry was built.

## §2 Nothing is lost

Preserved twice, in full:

- **`archive/pre-reset-corpus-2026-08-06`** — a branch holding the complete
  pre-reset commit, `data/guidebook.db` included. Authoritative.
- **`_archived/data/corpus-pre-reset-2026-08-06.db`** — the same database,
  queryable without a checkout. Deliberately not named `guidebook.db`: nothing in
  the toolchain resolves that path, no script globs `*.db`, and `_archived/` is
  covered by the root `.ignore`, so repo-wide search returns zero files from it.
  Reachable only by naming it, which is what an archive should require.

A matching **tag could not be pushed** — the session integration returns HTTP 403
on tag creation. Creating `archive/pre-reset-corpus-2026-08-06` as a tag, and
protecting that branch, are owner actions in repository settings.

**The file surfaces are untouched.** `references/bpc/**`, `references/bpc-reasoning/**`,
`references/connections/**`, `specs/`, `site/` and `parts/` remain exactly as they
were, as reference.

## §3 Why `jurisdictional_values` stayed

It was nearly reset on the reasoning that it "has no `ref_id`, so it is
unprovenanced." That reasoning was wrong, and the owner caught it.

**The source of a code value is the code standard itself.** All 109 rows carry
`standard_name` *and* `source_section` — 109/109 on both. Contract rule **R3**
already says so explicitly: *"Code/standard values: clause/section/page. Outcome
claims: DOI + page/table, or a direct URL."* Two classes, two locator types. A
standard cited by clause is fully located; demanding a DOI of it imports an
academic model onto a class that never used one.

This generalises, and it is the doctrinal consequence of this DR. The project's
sources span at least five classes — English-language academic work; academic work
in other languages outside the same cataloguing systems; professional-body
publications; codes and standards from national and international bodies; and
NGO/advocacy research. **Adequacy of identification and verification is
class-relative.** Doctrine already says this (R3 on locators, R5 that non-indexation
in PubMed/Scopus is an indexing fact and not an evidence-quality fact, Co-1
co-primary with T1 and never DOI-bearing). The tooling and the audits drifted
toward an academic default anyway. Correcting that drift is follow-on work, not
this decision.

## §4 What the reset obliges

1. **Research resuming does not restore these rows.** It writes new ones under the
   logged-search discipline (`db.py log-search`), carrying the admission edge that
   95% of the frozen corpus lacked.
2. **Checks that measured the corpus now report `EXAMINED: 0`.** That is the honest
   state of a clean-room restart, not a gate passing by accident — the difference
   being that this emptiness is *declared here*. Two `min_items` vacuity guards
   (`check_rendered_docs`, `source_slug_links_duplicates`) were retired for exactly
   this reason, each with the reason recorded in the registry. Re-declare them the
   day their subjects are repopulated.
3. **Reference surfaces are out of scope for DB-backed reference resolution.**
   `validate_cross_refs` reported 1,191 failures the moment the reset landed, every
   one of them a reference file citing an entity the reset removed beneath it. The
   check now declares `REFERENCE_ONLY` and scopes to live surfaces. A broken
   reference inside a *live* file still fails.
4. **The frame has two quarters with no canonical table.** The owner's definition
   names languages and jurisdictions as frame; neither has a table. Languages exist
   as a column in three places (15 values in `term_aliases`, all lowercase, against
   19 uppercase in `lang_jur_map`); jurisdictions exist as free text with `UK`(88),
   `GB`(5), `GB-SCT`(1) and 12 compound values for the same axis. Building those two
   vocabularies is the first frame work after this reset.

## §5 Reversal

One migration restores any table from `_archived/data/corpus-pre-reset-2026-08-06.db`.
The decision is reversible in mechanism and deliberate in intent; reversing it
should be a decision recorded here, not a quiet re-import.
