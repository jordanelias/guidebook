# Repair plan — batch 04

**Rewritten 2026-09-02, from 255 lines to this.** The first version was a findings register wearing
the word "plan": it transcribed 42 adversarial findings at finding-granularity and never asked the
only question a plan answers — *does this stop the next act?* Sorted that way, one item did.

That mistake has a name in this repository. `references/project-standards.md:638` records that
*"critique → plan → critique became the tightest loop"* here, and forbids adversarial passes on
plans precisely so a critique cannot spawn a plan that spawns a critique. A 255-line repair plan
for a batch whose write path still works was one turn into that loop.

---

## The blocker — CLOSED 2026-09-02

**`dbcore.next_ref_id()` returned `REF-00965`.** Deleting `evidence_sources` in the retraction
dropped the ref_id union high-water mark from 970 to 964, because those six sources had no
`source_locators` row. Meanwhile 26 surviving research rows and two retrieval-log manifests still
name REF-00965–970. Nothing refused it: R9a/R9b could not fire because the stash tops out at
REF-00964, so the next `add-source` would have run green and quietly minted a live identifier for a
different paper. **The danger was that it did not block.**

**Fixed** by `data_20260902181820`: the six identities are parked in `source_locators` as
`status='REFERENCE-ONLY'`, `recovered_from='retracted-2026-09-01-owner-ruling'` — research-stage
LEADS, which owner ruling R-04 explicitly permits ("DOI leads are not evidence… they're for
research"). The allocator was never wrong; its inputs had been removed.

Verified: `next_ref_id → REF-00971` · `source_locators` 875 → 881 · `evidence_sources` still 0 ·
0 FK violations.

Two things surfaced while fixing it, both recorded rather than skipped:
- **`db.py --tier-claimed` was `type=int` against a TEXT column**, so `add-locator` refused every
  Co-1 and Co-2 lead — the class CRPD Art 4.3 makes co-primary with T1. Fixed in the same pass
  (D04-031); three of the six identities are Co-1 and none could be written before it.
- **REF-00966's byline reads `andsensory E`**, a mangled parse of a community co-author on a Co-1
  paper whose warrant *is* that co-production. Carried verbatim with a re-retrieve flag rather than
  guessed at.

## Also closed

**R12 ordered an impossible write.** `governance/research-contract.yaml` told every session *"Code
values → jurisdictional_values"*. D-0181 struck that clause from the runbook on 2026-08-31 but not
from this copy — and this is the copy injected into every session by the SessionStart hook, so the
fix reached the document nobody reads and missed the one everybody gets. Since 2026-09-01 the write
is also impossible: `db.py:2383` refuses on an FK to an empty `items`. Now reads *"Code values →
`search_candidates` as LEADS"*, with the full reasoning on the rule's `resolution:` field, and the
hook regenerated so both copies agree.

**`RULINGS.md` said the migration was never applied.** It was, about a minute later. Corrected by
appendix rather than rewrite — a superseded record is evidence of what was believed when.

---

## Everything else is debt, not a gate

The remaining 14 findings are in `DEFECT-REGISTER.md` as **D04-019 … D04-032**, each with its
evidence and the specific act that would close it. None blocks a research batch. The heaviest:

| | |
|---|---|
| **D04-027** (P1) | This session misread DR-2026-08-19 §1.4 *and breached it*, then reported the breach as a discovery. §1.4 rule 1 forbids taking the frame from the item list; rule 2 says "no value crosses" into a search row. `FRAME.md` came from `items`, and "22 newtons" and "pendulum test value" reached agonist queries. Owed: a correction in the session record |
| **D04-032** (P2) | `author_fidelity` reports `EXAMINED: 0`. The anti-fabrication check built after the 2026-08-19 invented-co-authors incident cannot see any of this session's 19 payloads, because no manifest was written. **Owed before any re-admission of this material** |
| **D04-030** (P2) | `db.py` cannot write `co1_provenance`, so no Co-1 admission can satisfy D-0178 through the sanctioned writer |
| **D04-020** (P2) | The retraction zeroed `results_admitted` on 7 research rows to satisfy H05. Restoring them is coupled to retiring H05 — rule 5 says retire the dual home, not rewrite the record to agree with it |

## Owner decisions — not a session's to make

1. **`jurisdictional_values`.** Measured: the 109 rows carry three non-null columns and reduce to
   **83 distinct `(jurisdiction, standard_name)` leads**; 26 rows are pure item-crossing
   duplication; only 11 of 83 exist elsewhere. So ~72 leads die with the archive. Recommendation on
   record: restore them as `research_code_leads` with `jurisdiction` NOT NULL and **no DOI column** —
   which makes structurally impossible the collision `source_locators` already carries in 24 rows
   holding both a `standard_number` and a DOI. This *executes* D-0181 rather than superseding it.
   Note D-0181's own pointer is stale: migration 065 was consumed by the lens work.
2. **`site/` (D04-022).** Frozen reference surface, or finish the sweep? 184 links still publish
   the deleted item pages.
3. **The instrument contradicts itself.** §1.4 rule 1 forbids the frame that §12.1 step 2 orders.
4. **Re-running the batch.** The material survives. It needs an ICF/access-need frame rather than an
   item frame, D04-032 closed first, and D'Souza's T1 re-argued (it was asserted on the same test
   the brief used to put Chang & Drury at T3).
