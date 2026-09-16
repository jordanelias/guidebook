# ANTAGONIST log — batch 08 (session_2026-09-16-research-batch-08-ramp-gradient)

Arming: CLAUDE.md, governance/research-contract.yaml (R1-R15), scripts/audit/research_batch_dod.py
(read what it actually tests, not its docstring), workplan/2026-09-10-batch-06-runbook.md.
Scratch DB read read-only at `/tmp/claude-0/.../scratchpad/batch08/walk.db`; canonical
`data/guidebook.db` opened read-only for comparison only, never touched.

**NOTE ON METHOD:** the DB changed under me mid-session (orchestrator actively walking it — as
warned). Figures below are a coherent last-read snapshot taken together at ~05:00; anything I
looked at earlier and found empty (extractions, specifications) had since been populated, so I
re-read and re-verified before writing findings 1-3.

---

## BLOCKING

**1. Two extractions carry a rig-setting range mislabeled `figure_role='finding'`, which by its
own schema definition may carry no value — the exact anti-pattern migration 075 exists to stop,
recurring inside this batch.**
`source_value_extractions` (walk.db): extraction_id 11 (REF-00985, ex-REF-00973, DOI
10.3390/s23218659) `claim_type='range' claimed_value='0-4.8' claim_text='the inclination of which
varied between (0° to 4.8°)' figure_role='finding'`; extraction_id 12 (REF-00983, DOI
10.1080/17483107.2018.1465602) `claim_type='range' claimed_value='3.5-15' claim_text='propelled a
MWC on ramps of slope 3.5°, 9.5° and 15°' figure_role='finding'`. Both values are the study's
controlled independent variable (treadmill/ramp slopes the researchers set), not an assertion of
what ramp gradient is or should be — `scripts/db.py:5081-5085`'s own refusal text names this
precisely: *"a tested slope read as a claim is how '1:20, 1:16, 1:12, 1:8' became a range no source
ever asserted"* — and `assess_cell.py:257-276`'s docstring independently describes the earlier real
failure as *"the slopes a treadmill was set to; the ADA range a study tested"* wrongly governing.
`figure_role='finding'` is defined as *"reports something ABOUT the parameter without asserting a
value... Supplies DIRECTION, never value"* (assess_cell.py:270-272) — contradicted by these two
rows carrying a numeric range. The correct role is `condition` (rig setting, never anchors), not
`finding`. **Consequence, not just bookkeeping:** `specifications` row 1 (parameter_id=3, MOB) has
already been written (`state='pending'`, `governing_refs=NULL`, `functional_basis='function_only'`)
and `idx_spec_row_identity` refuses a second `assess_cell.py` run for this parameter×lens forever
(runbook HAZARD, confirmed in this file). If `figure_role` is corrected via `amend-extraction`
*after* migration, it cannot change the already-frozen specification. Fix the two rows with
`db.py amend-extraction --field figure_role` to `condition` before this batch is migrated to
canonical — not after.
Mitigating fact, stated for balance: because `finding` is (like `condition`) excluded from
`gather_sources()`'s `figure_role IN ('claim','derived')` filter, the mislabeling does **not**
currently corrupt the determination — `pending` is in fact the honest answer here, since across all
four sources none actually states what accessible ramp gradient should be (REF-00984/00986 are
correctly `absent`). The defect is in the extraction record's internal consistency, not (yet) in
the specification.

**2. `research_batch_dod.py --session session_2026-09-16-research-batch-08-ramp-gradient` (run live,
GUIDEBOOK_DB_PATH pointed at walk.db) currently exits 1, NON-COMPLIANT:**
`R7: only 0 candidates registered for 46 screened results (expect >= 1)`. `search_candidates` for
this session is empty even though S3/S4 screened 25 and 20 results respectively. This is a live,
non-vacuous failure of the gate the batch itself must pass before merge (may be resolved if the
orchestrator has not yet reached that step — re-check before declaring the batch done).

---

## SERIOUS

**3. `journal_name`/`journal_abbrev` left NULL on all four admitted sources despite
`metadata_quality='COMPLETE'` and the Crossref payload carrying `container-title` for every one**
(e.g. REF-00983's payload `container-title: ["Disability and Rehabilitation: Assistive
Technology"]`, `journal_name` in DB: `None`). Not fabrication (no wrong value asserted) but a
COMPLETE claim contradicted by an available, unwritten field. **Corpus-wide, not batch-specific:**
`grep -n "journal_name" scripts/db.py` returns nothing — `add-source` has no `--journal` flag at
all, so no sanctioned writer for this column exists; this batch could not have filled it through
the CLI. Flagging as a tooling gap rather than an operator failure, but the `COMPLETE` label is an
overclaim regardless of cause.

**4. `retrieval-log/.../manifest.jsonl`'s free-text `purpose` field is wrong on 4 of 8 rows** — rows
for REF-00985's DOI (10.3390/s23218659) and REF-00986's DOI (10.1016/j.jelekin.2025.103027) both say
`"purpose": "... for REF-00983"` / `"... for REF-00984"` respectively. The machine-read `ref_id`
field on every row is correct (verified against evidence_sources and the Crossref payload's own
DOI), so this does not affect `--verify-authors` (which matches by DOI/ref_id, not by the purpose
string) — prose-only, but exactly the kind of drift CLAUDE.md §7's traps warn compounds silently.

---

## SURVIVED (checked and found sound — reported per instructions, not padding)

- **Fabrication (item 1, the project's worst failure class): NONE FOUND.** All 4 sources' authors
  (names, given names, order), titles, years and journals were diffed against the Crossref artefact
  bytes for that DOI (`retrieval-log/.../20515281a437ca18.json`, `0ed2a344cc2417c3.json`,
  `4062c068e5f7280f.json`, `125a5b31e7051cbf.json`) and match exactly, author-by-author, position-
  by-position. This is a real, verified re-retrieval, not the 2026-08-19 shape.
- **Claim/observation text (item 2): all 4 `observed_terms.context_quote` values and all 4
  `source_value_extractions.claim_text` values are exact byte-substrings of their sessions'
  EuropePMC abstract artefacts** (checked individually, e.g. REF-00985's `"the inclination of which
  varied between (0° to 4.8°)"` appears verbatim in `cb2a5e19c5447106.json`'s `abstractText`).
- **Population grading (item 4): no over-claim.** REF-00983 (able-bodied n=7, no propulsion
  experience) → PROXY; REF-00984 (SR, no participants of its own) → PROXY; REF-00986 (ten
  able-bodied) → PROXY; REF-00985 (17 SCI participants, own manual wheelchairs) → EXACT for MOB.
  All grades match the abstract text exactly and none inflate an able-bodied/no-participant sample
  to EXACT.
- **Tier consistency (item 5):** all four (evidence_type, scope, tier) triples equal
  `derive_tier()`'s output (clinical/high_control→1 ×3, sr_meta/intrinsic→2 ×1), and `scope
  =high_control` is defensible from the payloads (instrumented biomechanical lab studies with
  controlled ramp/treadmill slopes), not a field survey inflated.
- **Zero-yield honesty (item 6, R14):** the one 0-result search (S1, Co-1 pass) carries a
  `findings_note` that names its own control search (S3, identical subject terms minus the
  co-production clause, 63 results) as proof this was genuine absence in-index, not a query-shape
  artefact — exactly the R14 discipline, done correctly and legibly.
- **Duplicate/tombstone handling (R9/R9a):** REF-00985 and REF-00986 are re-admissions of
  DOI-identical, previously-RETIRED REF-00973/REF-00974 (`source_locators`, status RETIRED) — new
  ref_ids were correctly minted rather than illegally cross-filing to a retired identity.

---

## COULD NOT / DID NOT FULLY CHECK

- **Item 8 (the determination) beyond structural fields.** `specifications` row 1 appeared only in
  the last few minutes of this pass (`state=pending`, `value_min/max/unit=NULL`,
  `governing_refs=NULL`). Given honest extraction (see finding 1's mitigating note), `pending` looks
  like the right answer, but I have not seen a final, settled state — re-check once the orchestrator
  confirms this cell is done, especially whether finding 1 is corrected first.
- **Term adjudication completeness (CLAUDE.md §6, "zero links after judgment is a defect").**
  4 `observed_terms` rows exist for this batch's sources; `term_adjudications` has 0 rows scoped to
  this session (TERM-001 was promoted from existing vocabulary rather than coined, so the
  add-term/adjudicate-term path was skipped by design per `base_parameters.notes` — but whether the
  4 harvested surface forms individually still need a crossing decision was not resolvable from the
  DoD script, which explicitly declines to check this (comment at research_batch_dod.py:634-642)
  and defers it to the adversarial pass). Flagging as unresolved rather than asserting either way.
- **Vacuous DoD passes (item 7), named as asked:** `R3` (0 tier≥4 sources in this batch — nothing to
  clause-cite), `R5` (0 non-English searches), `R6` (0 deferred_reason rows), `R12` (0/0) are all
  structurally vacuous PASSes — true statements about an empty set, not defects, but not informative
  either. `R11` self-labels its own vacuity correctly ("EXAMINED: 0 aliases").
