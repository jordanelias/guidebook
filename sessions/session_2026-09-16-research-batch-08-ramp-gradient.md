# Batch 08 — ramp gradient (TERM-001, parameter 3) × MOB

**Session id:** `session_2026-09-16-research-batch-08-ramp-gradient`
**Branch:** `claude/research-safety-ny8pl0` · **PR** #137
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry`
**Outcome:** `specification_id 1` — **`pending`**, governing set EMPTY,
`derivation_sha e435ca0551e2…`, `value_min/max/unit` all NULL.

Every figure below was derived from `data/guidebook.db` after the migrations applied (rule 7).
Re-derive before relying on any of it.

## What this batch is

The first re-run of the corpus the owner cleared on 2026-09-13 — *"all the circulation rows that
have been produced are not able to be trusted, so we have to redo them all from the start."*
It starts at the first cleared cell.

| | |
|---|---|
| searches logged | 4 (1 zero-yield, 46 results screened) |
| sources admitted | 4, with 4 `search_admissions` edges |
| authors stored | 15, every one diffed against Crossref payload bytes |
| candidates staged | 7 |
| concept observations | 4 |
| population matches | 4 |
| citation-mining passes | 4 (all deferred, all with a reason) |
| extractions on parameter 3 | 4 |
| extraction relations | 4 |
| parameters minted | 1 (promoted from base vocabulary, not coined) |
| determinations | 1 |
| data migrations | 5 |

## The substantive finding: nothing states a ramp gradient

**Not one admitted source asserts a gradient value.** All four extractions are `condition` or
`finding`; the governing set is empty, and that is why the cell is `pending` rather than because
the search was thin.

- **REF-00985** (Marchiori 2023, T1, 17 SCI wheelchair users) — treadmill *"the inclination of
  which varied between (0° to 4.8°)"*. That is a **rig setting**, not a recommendation: the study
  measures articular discomfort rising 14→36% across it.
- **REF-00983** (Bertocci 2018, T1) — *"propelled a MWC on ramps of slope 3.5°, 9.5° and 15°"*,
  finding pushrim force more than doubling. Its own conclusion is directional — *"imperative that
  bus operators minimize ramp slope"* — and names no permitted value.
- **REF-00986** (Arnet 2025, T1) — graded `absent`. It measures shoulder load for ramp ascent and
  descent and **never states the incline it used**. The batch-06 runbook warns by name against
  manufacturing a gradient for this source; it is not manufactured here.
- **REF-00984** (Kilkens 2003, **T2** synthesis) — graded `absent`. A review of 24 wheelchair
  skills tests in which *"ascending slopes"* is among the most frequently included tasks, and no
  gradient is stated anywhere in it.

So the reachable literature measures the **effect** of gradient rather than prescribing one. That
is content for the guidebook, not only a gap in the corpus — and it is the same shape batch 07
found for corridor width.

**This outcome was predicted before the searches ran.** `scratchpad/pr-137-research-batch-08/PRIORS.md`,
written before the first query: *"I expect the literature to measure the EFFECT of slope rather than
to state a permitted slope… I would not be surprised by `provisional`."* Recorded in advance so a
`stated` outcome would have had to argue against a prior rather than confirm one.

## The Co-1 leg is a real zero, and the control is what proves it

0 hits with the co-production clause; **63** with the identical subject terms and the clause
removed (exec 31, which serves as the control). PubMed AND-chains every term, so the clause is what
zeroes it. That is a fact about **publication venue**, not about query shape — R14's distinction —
and explicitly **not** a claim that disabled people have produced no knowledge about ramp slope.
Co-1 on this parameter has to be sought in DPO, housing and participatory-design venues.

## What the adversarial pass changed

An antagonist ran read-only and independently, arming itself from CLAUDE.md, the contract and the
gate before reading any of the batch's own conclusions. It found the batch sound on the things that
matter most — **zero fabrication** across all 15 author rows diffed against payload bytes, every
`claim_text` an exact byte-substring of a persisted artefact, population grades correctly refusing
EXACT for proxy samples, tiers consistent with `derive_tier()` — and it found two real defects:

1. **Two extractions were re-graded `finding` → `condition`.** The schema's own definitions decide
   it: `finding` *"supplies DIRECTION, never value"* and these rows carry a `claimed_value`, while
   `condition` is defined as *"a rig setting or a limit the value is conditioned by"* — which is
   exactly what a treadmill inclination and a set of laboratory ramp slopes are. `db.py`'s refusal
   text names this very failure: *"a tested slope read as a claim is how '1:20, 1:16, 1:12, 1:8'
   became a range no source ever asserted."* Corrected by `amend-extraction`. **The determination is
   unaffected** — both roles are excluded from the governing set — so this corrects the record, not
   the answer.
2. **The retrieval manifest's free-text `purpose` field mislabelled four rows.** Corrected.

## Two defects this batch found in the apparatus, both fixed in the same PR

- **`R9a` and `db.py add-source` both read RETIRED tombstones as live DOI claims.** The re-run could
  not admit a single cleared source by any route: the only remedy either offered was to cross-file a
  retired identifier, which migration 076 exists to prevent. Two of this batch's four sources
  (REF-00985, REF-00986) sit on tombstoned DOIs, so this was not a corner case.
- **`emit_data_migration.py` would emit the same payload twice**, and `migrate_db.py` keys on the
  filename, so both would apply — a whole batch inserted twice. Now refused.

## One defect of this batch's own making

**REF-00984 and REF-00986 were given the same per-slug `local_ref_id`.** The admission ran in two
passes (the first two admissions were refused by the tombstone bug above), and the retry restarted
its counter, so two sources shared label `4`. `citation_mining` is UNIQUE on `(slug, local_ref_id)`
and looks the label up rather than inventing it, so **REF-00986 could not be given a mining row at
all** and R2 was unsatisfiable for it by any route. Fixed forward by a compensating migration.

**And one false green worth recording.** Both gates were first run with `GUIDEBOOK_DB_PATH`
exported to the scratch DB, so they reported COMPLIANT and CLEAN **against `walk.db`, not
canonical** — while canonical was in fact missing two mining rows. This is CLAUDE.md §7's "scopes a
gate to nothing and it passes green" wearing a different hat: wrong database rather than wrong
session id. Both gates were re-run with `env -u GUIDEBOOK_DB_PATH` and the DB path printed.

## Gates, against canonical

```
python3 scripts/audit/research_batch_dod.py --session session_2026-09-16-research-batch-08-ramp-gradient
    COMPLIANT — all research definition-of-done rules met.
python3 scripts/audit/citation_mining_completeness.py --session session_2026-09-16-research-batch-08-ramp-gradient.md
    Examined 4 · Outstanding 0 · VERDICT: CLEAN
python3 scripts/audit/batch_capture_report.py --session session_2026-09-16-research-batch-08-ramp-gradient
    16 tables written · EXAMINED 77 · unattributable 3
```

## Owed

- **Mining is deferred, not done.** All four rows carry a reason. REF-00984, the T2 review, is named
  as the highest-value backward target: a review of 24 skills tests has a reference list of primaries
  and is the likeliest place a stated gradient exists.
- **A Co-1 pass outside PubMed** for this parameter.
- **`metadata_quality` reads COMPLETE on all four sources while `journal_name` is NULL** — there is
  no `--journal` flag on `add-source` and nothing writes that column, so COMPLETE is currently an
  overclaim for any source in this corpus. A tooling gap, recorded not silently accepted.
