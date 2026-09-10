# Orientation — derived 2026-09-10, against `bd59fd4` (origin/main)

Every figure below was measured at that commit. **Do not quote them forward** (`CLAUDE.md` rule 7);
each block carries the command that re-derives it.

---

## 1. Where the pipeline actually stands

    SPINE: base -> research -> evidence -> judgment -> synthesis -> specification -> render

Live table state (`PRAGMA user_version` = 73; 71 tables, 17 views):

| Stage | Live? | Evidence |
|---|---|---|
| **base** | vocabularies yes, **parameters no** | `slugs` 106 · `terms` 88 · `term_aliases` 2382 · `axes` 17 · `access_needs` 17 · `populations` 23 — but **`base_parameters` holds 0 rows** |
| **research** | yes | `search_executions` 43 across 4 sessions · `search_candidates` 75 · `citation_mining` 15 |
| **evidence** | yes, thinly | `evidence_sources` 9 · `evidence_source_authors` 38 · `source_slug_links` 9 · `observed_terms` 33 |
| **judgment** | vocabulary only | `evidence_population_match` 14 · **`source_value_extractions` 0** |
| **synthesis** | no | `convergence_assessment` 0 |
| **specification** | no | `specifications` 0 — and **unwritable**: `parameter_id` is NOT NULL into an empty `base_parameters` |
| **render** | prior-version only | the `[A-E]-NN` item surface now sits under `_archived/` |

Re-derive:

    python3 - <<'PY'
    import sqlite3
    con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
    print("user_version:", con.execute("PRAGMA user_version").fetchone()[0])
    for (t,) in con.execute("select name from sqlite_master where type='table' order by name"):
        n = con.execute('select count(*) from "%s"' % t).fetchone()[0]
        if n: print("%7d  %s" % (n, t))
    PY

**The unwritable set is the honest headline.** 23 columns are NOT NULL foreign keys into empty
tables. Almost all of them chain off `items` (emptied by owner ruling 2026-09-01) — but the two
that matter for a batch chain off `base_parameters`: `specifications.parameter_id` and
`source_value_extractions.parameter_id`. **Both clear the moment a parameter is minted**, which is
step 1 of the runbook. This is no longer the standing block `CLAUDE.md` §4 describes; it is a
first-write-of-the-session condition. Re-derive with `CLAUDE.md` §4's own UNWRITABLE probe.

---

## 2. The live procedure

`decisions/DR-2026-08-19-…-operative-instrument.md` is still the binding instrument, but **its §12.1
runbook is superseded**, by its own header, as of today:

> **`workplan/2026-09-10-batch-06-runbook.md`** — base → research → evidence → judgment →
> specification, every command executed for real on a scratch copy.

Its companion `workplan/2026-09-10-road-to-batch-06.md` listed seven blockers. Measured today:

| | Blocker | State |
|---|---|---|
| B1 | research contract says the cell key is an open decision | **CLOSED** — the line is gone from `governance/research-contract.yaml` |
| B2 | no runbook for the walk | **CLOSED** — the runbook above; **one defect found and fixed today, §4 below** |
| B3 | a NULL `verification_status` on a URL-bearing admission wakes the verify-urls cron | **CLOSED** — `R10b` in `research_batch_dod.py:562-596` |
| B4 | no extraction writer; the engine gathered by slug | **CLOSED** — migration 073, `db.py add-extraction`, `gather_sources(conn, parameter_id)` |
| B5a | the engine anchored on tiers it reported underivable | **CLOSED** — `non_anchoring_on_tier` in the report, tier gate excludes |
| B5b | `scope` NULL on all 9 sources | **PARTIAL — 5 of 9 written, 4 escalated to the owner** (REF-00784, 971, 972, 976). See `workplan/2026-09-10-b5b-scope-owner-escalation.md`; two are payload gaps, two are tier contradictions the blind derivation refused to write over |
| B6 | two specification-stage skills teach the retired `(item_code, population_code)` key | **OPEN** — 7 hits in `skills/specification-curator_SKILL.md` (`:59-100`), 3 in `skills/item-specification-writer_SKILL.md` (**`:40,52,59` — not `:91`, which road-to-batch-06 cites and where nothing matches**). Also open in prose: `governance/evidence-architecture.md:114` |
| B7 | `regenerate_derived.sh` between `migrate_db.py` and the gate | process, in the runbook |

**No blocker of that list stands open against a batch except B6**, which is a rule-4 sweep debt
that bites only a session reading those two skills at the specification stage. **That is a claim
about the blocker register, not about the walk**: this session read the closures, it did not
re-execute base → specification end to end. The last recorded execution is the runbook's own
rehearsal, which reports `research_batch_dod.py --session` returning `COMPLIANT`. The first real
batch is what tests it, and the runbook's own header says a COMPLIANT gate is not a sound
determination — it proves the 19 mechanical rules, which is a different claim.

---

## 3. The subject of batch 06

Continuing `accessible-circulation-geometry` needs **no owner decision** (road-to-batch-06 STOP
CONDITION #5); a *new* slug is content and does.

Batch 05 (`session_2026-09-02-research-batch-05-circulation-icf`) left this state on the slug:

- **15 searches** (exec 29–43), **9 admissions**, 10 `PENDING-VERIFICATION` candidates still staged.
- Tier spread of the 9: T1 ×4 (3 clinical, 1 `co1`), T2 ×1 (`sr_meta`), T3 ×4.
- Languages fired: EN, DE, JA. The JA leg (exec 41, J-STAGE, 49 results, 0 admitted) is recorded as
  **the R5 finding of the batch** — non-English peer-reviewed work is academic, not grey.
- Zero-yield rows are kept and diagnosed, several as R14 query-shape failures rather than absence.
- `search_executions` #42 is a deliberate non-search: vertical circulation, deferred with a reason.

`room-acoustic-performance` carries 28 searches and **0 sources** — batches 01 and 02 admitted 10
between them and every one was retracted (the 2026-08-19 fabrication). 56 candidates sit staged
there. That slug is a real backlog; it is not batch 06's subject.

---

## 4. A defect found and fixed while preparing

**The runbook told the operator to retrieve with a flag that does not exist.**

`workplan/2026-09-10-batch-06-runbook.md` step 2 read
`retrieval_log.py --fetch --doi "$DOI" --session "$SESS"` and
`retrieval_log.py --verify-authors --ref-id "$REF"`. `retrieval_log.py`'s entire CLI is `--session`
plus one of `--verify-authors` / `--backfill` / `--reconstruct-manifest` (`:729-733`). There is no
`--fetch`, no `--doi`, no `--ref-id`.

This matters more than a typo. That block is the **one** step standing between this project and a
repeat of the 2026-08-19 fabrication, and following it literally fails twice — the fetch errors out,
and the verification is then run with a flag that errors out too. The correct forms are the module's
own (`retrieval_log.py:31-42`): `fetch()` imported in Python, and `--verify-authors --session`.
`workplan/2026-08-20-provenance-walk-execution-plan.md:485` had already recorded *"`retrieval_log.py`
has **no fetch subcommand**"* — the knowledge existed and did not reach the file that needed it.

Corrected in this commit, with both forms executed before being written down.

---

## 5. What that execution found — a fidelity re-check of the admitted corpus

Both corrected commands were run for real against the live corpus, under session id
`session_2026-09-10-repository-orientation`:

    8 of 8 DOI-bearing sources re-retrieved from Crossref, payloads persisted to
    retrieval-log/session_2026-09-10-repository-orientation/

    CLEAN FOR THE 8 OF 9 SOURCE(S) EXAMINED — their stored authors and asserted
    bibliographic fields match the retrieved payloads

**REF-00978 is unexaminable and is reported, not passed over.** It is the Co-1 source (Euan's Guide
Access Survey 2025, a disability-led Scottish charity) and it carries no DOI, so the author diff
cannot reach it. Its retrieval trail *does* exist — under batch 05's log, five `euansguide.com`
manifest lines — but the URL stored on the row is the charity's S3 object, which matches none of
them, so the locator test finds nothing. **That is an artefact-matching gap, not evidence of a
defect**, and it sits on precisely the tier where erasure would be worst (`CLAUDE.md` §6: *"the
disabled people who produced the work are part of the evidence, not metadata"*). Worth closing by
re-retrieving the S3 URL under a batch session; not closed here.

---

## 6. Gate state at this commit

- `run_checks.py --selftest` → **PASS**, registry coherent.
- `scripts/preflight.sh` → **PASS**. One advisory failure, `retired_vocabulary`, 64 occurrences on
  the live surface, examined 26. Pre-existing on untouched `main`; not this branch's.
- 5 contract criteria have no check claiming them; 22 of 67 checks state no authority; 34 of 67
  carry a real floor. All three are `--selftest` INFO lines and all three are ratchets, not failures.
