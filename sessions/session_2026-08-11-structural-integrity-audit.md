# Session — Structural integrity audit: can the pipeline carry content?

**Date:** 2026-08-11
**Branch:** `claude/status-check-12728x` · **PR:** #91
**Doctrine SHA:** `0f2f525`
**Kind:** tooling / governance. **No content, no synthesis, no DB writes, no migrations.**
**Method:** agonist–antagonist, 12 agents, lens-separated adversarial review.

---

## Task

Began as "tell me where we are at". Widened by the owner across the session to: propose fixes
for every issue found; document the pipeline stage by stage; trace every hop, handshake,
cross-reference, pointer and key in both directions; audit every tool for write-correspondence;
confirm the state of rooms, economics and case studies; establish external verifiability
through GitHub; and produce a machine-readable context map.

**The owner's governing statement, which reframed everything:** *"Our goal, here, is to ensure
that our structure actually works before we do content."*

## Method

Ten agonist passes, six antagonist passes on separate lenses (factual, method, vacuity,
doctrine), and one decisive experiment. Adjudication was performed in the main session by
re-deriving contested claims from source. The protocol, its scaling rule and its five
adversarial quality checks are written up as Part 3 of the deliverable and proposed as standing
method.

**The protocol paid for itself repeatedly.** Eleven of the deliverable's own first-draft
proposals were corrected or killed by its antagonist passes, including two corrections to
corrections. Three times a pass reported a real defect with a **false mechanism** — a right
conclusion with a wrong cause, which produces the wrong fix. That pattern is recorded in Part 3
§3.7 as the main methodological lesson.

## The decisive experiment

One synthetic topic (`zz-walk-test`, `REF-99001`) pushed through all twelve stages in a scratch
copy of the database, alongside three deliberately illegal rows.

**No break point. The row traversed all twelve stages.** The chain joins by key end to end.

**The verdict is not "it works". It is: the structure can carry content today, and that is the
problem.** Enforcement is strong exactly where a foreign key happens to exist and absent
everywhere the evidence lives. In the walk, `tier=99` and a fabricated `evidence_type`
propagated untouched into `part13.md` as a tier band **"T99"** in the published bibliography;
the determined value (`value_min=1200.0`) **did not render at all**, because no generator reads
those columns. Seven validators stayed silent, four of them blocking. Of three illegal rows,
only one was caught — the `stated` cell whose `governing_refs` named a nonexistent REF-ID,
stopped cleanly by two independent blocking gates.

## What was found

**The apparatus is green and the green is not load-bearing.** `run_checks.py --all` reports
`PASS — 55 green, 9 advisory`; `test_db_integrity` reports 70/70. Meanwhile at least eleven
representations are measurably out of agreement, a fabricated corridor width passes every
blocking gate, and 7 of the last 30 `ci.yml` runs on `main` were red and merged.

The four findings that matter most, in the order they should be acted on:

1. **A fabricated measurement passes every blocking gate.** A corridor width rewritten
   1200 mm → 1800 mm in a copy of the committed DB: `migration_reproducibility` PASS,
   `test_db_integrity` 70/70. The blocking gate compares `user_version` plus six `COUNT(*)`s;
   an `UPDATE` changes no count. **`migration_reproducibility_deep` does the full comparison,
   is advisory, and passes today** (63 of 66 tables identical). Promoting it is one word.
2. **An unguarded replay script can silently undo the clean-room reset.**
   `scripts/migrations/session_2026_05_11g_replay.py` takes no required arguments, defaults to
   the canonical DB, has its 45 KB payload committed and present (64 pre-reset rows), sits in
   the directory named as the sanctioned write path, and leaves no `data_migrations` row.
   Seven of its nine siblings import `_legacy_guard`; three writers were missed.
3. **Two of the project's four constitutive legs cannot be recorded at all.** DR-2026-08-06 §1
   promises a walk back to values, sources, **the population served**, and **the doctrine that
   governed the judgement**. `target_population` has no key — it is matched by regex over
   prose. There is no doctrine column anywhere in the database. **No quantity of new rows fixes
   either; both need a migration, and both are free today.**
4. **The determination writer fills one side of a dual store while the readers read the other.**
   `assess_cell.py` writes `governing_refs` and never `cell_source_links`; three renderers read
   only the junction; the blocking parity checks compare two empty stores and pass. The first
   real determination will render with no governing sources while the gate stays green. And
   `regulatory_stratum_only` is never written while five readers read it — so every
   code-derived cell would render **anchored ●** rather than at the flagged weak band, the
   exact misrepresentation Option A exists to prevent.

**Rooms, economics and case studies** — the owner asked directly. All three have content in
markdown, a designed schema, and **no writer**. Rooms' missing writer already exists, archived:
`_archived/scripts/db/seed_room_items.py` holds 142 room↔item pairs. Case studies has a 56 KB,
~26-entry compendium and sixteen `ALTER TABLE` migrations against a table that has never held a
row. Economics has the most complete schema of the three, a research-contract rule (R12)
instructing sessions to file into `economics_entries`, and **no write path at all**.

**Census totals**, each derived by execution:

| Measure | Value |
|---|---|
| Blocking checks declaring a vacuity floor | 5 of 28 |
| Reconciliation points | 52 — 24 automatic (11 blocking *and* effective), 20 manual-undocumented, 3 impossible |
| Dual representations | 62 — 13 reconciled, 26 divergent now, 17 in the cheap window |
| Tools audited | 186 — 9 phantom, 30 orphan, 11 stale-contract |
| Tables | 66 — 39 empty, 11 with no writer at all |
| Identifier columns with no FK | 19, of which 7 load-bearing |
| Dangling documentary references | 116 occurrences across 51 targets |
| Attestations | 74; corpus-wide schema validity checked by nothing |

## What was delivered

- `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` — the three-part deliverable:
  remediation register with method/gate/evidence/falsification per issue; twelve-stage pipeline
  anatomy answering (a)–(h) per stage, where (h) is the acceptance conditions for a single row;
  and the agonist–antagonist protocol as standing method.
- `scripts/generate/context_map.py` + `governance/context-map.yaml` — the machine-readable
  orientation index, **generated not written**, registered as `context_map_fresh` so it cannot
  rot. Three defects were caught in the generator before it shipped, each an instance of what
  it exists to prevent.
- A `D` / `D(fk)` enforcement rung proposed for CLAUDE.md §2's spectrum, which has no rung for
  schema constraints — the systematic error two independent antagonists found separately.

## The doctrine lens, run last, found what four other lenses missed

Both outstanding doctrine passes were completed before close. They returned **3 doctrinal
breaches and 8 erosions** across stages 4-6 and 10-12, and one breach transferred to the
stages 1-3 segment that no doctrine lens ever covered.

- **The renderer makes evidence-thin populations disappear.** Doctrine: "Silence on
  evidence-thin populations is not the default"; a `pending` cell renders as
  `[BEST-PRACTICE-PENDING]` plus a gap link. Neither live generator selects `gap_register_id`;
  the token is emitted by one unexercised file and appears in **no** rendered page; and a
  population linked to an item but holding no cell is **absent from the determination table
  entirely**. That is the erasure this project exists to prevent, in shipped code. It has
  produced no wrong pages only because `evidence_cell_state` is empty.
- **Three passages of the deliverable stated a repealed rule as operative** —
  `tier-system.md` §3's binary, superseded 2026-07-20 by §8 + Option A.
- **And the mirror-image error elsewhere**: stating only Option A's ceiling, which restores the
  repealed absolute I3 by omission. Both directions are errors; suppression was itself the
  original failure.
- **Co-1 co-primacy is enforced by nothing.** `evidence_type='co1' ⇒ tier=1` has no CHECK, no
  test, no registry entry, and `validate_source_co1_fields()` has never run — it scans
  `data/sources/*.yaml`, which does not exist.

The lens's structural observation is the one to carry forward: no clinical-first *assertion*
anywhere, but a clinical-first *shape* — four of five erosions are omissions from acceptance
lists, and each omits a condition a Co-1, non-English or regulatory-stratum row would need and
a DOI-bearing English journal article would not.

## The sanctioned write path, now tested

`scripts/emit_data_migration.py` was exercised end to end against a scratch copy: emit → detect
as pending → apply → ledger increments in the copy only → canonical untouched → tree clean.
Every property held. **The migration system is the strongest component in the repository**, which
sharpens rather than softens the enforcement findings: the discipline is sound and the gates
around it are what fail.

It proves the mechanism, not that a real content change survives it — the payload was one row in
a table with no downstream readers.

## What was NOT done, deliberately

**Nothing in the remediation register has been executed.** No fix, no promotion, no migration,
no retirement, no file move. The deliverable proposes; it does not act. Every owner-gated item
is marked as such with a recommendation and its evidence.

**Stage segments 1-3 and 7-9 were never doctrine-reviewed.** Given that the one doctrine pass
which did run found a breach that had also propagated into segment 1-3 undetected, those two
segments should be assumed to carry similar defects.

## Bias and counterclaim

Recorded in `attestations/sessions_session_2026-08-11-structural-integrity-audit.json`.

## For the next session

Read the deliverable's §1.6 sequencing and the reconciliation map's twelve-item pre-content
checklist. The first three items need no decision: guard the three unguarded writers; wire the
registry's existing per-battery `deps:` field that `run_checks.py` has never read; fix the
`test_graph_audit` crash that hides every assertion behind it.

**The window argument matters more than any single fix.** The reset emptied the corpus, so
every migration proposed here — the population FK, the doctrine binding, the junction
retirements, the deep-gate promotion — is free right now and gets more expensive with every row
written. That is the case for doing structure before content, and it is the owner's own
instinct, measured.
