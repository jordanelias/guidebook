# F2 — read-only doctrinal audit: research / synthesis

**Model:** Fable 5, read-only. **Recorded by Opus** — the auditor's harness has file creation
disabled (my error in choosing a read-only agent type), and it correctly refused to work around the
constraint. Digest reproduced as returned. Its three headline findings are verified and actioned in
`OPUS-runbook-drift.md` PART 10 (D-18, D-19, D-20).

---

## B. Verification verdicts

1. **Handrail — REFUTED in half.** No `items` row (CONFIRMED), but `slugs` holds
   `fall-risk-flooring-handrail-design` (STUB, topic `entrances-and-circulation`, created
   2026-07-24). S1 §1.1's "#1 BLOCKING gap — one must be created" is **wrong at slug level**; the
   frame-first home §1.4 requires already exists. Neither S1, PROTOCOL, nor OPUS caught it.
2. **Cold start — CONFIRMED.** 10/10 `source_slug_links`, 10/10 `citation_mining`, 5/5 `gaps`,
   28/28 `search_executions` all on `room-acoustic-performance`; zero mobility rows anywhere. *But*
   29 REFERENCE-ONLY `jurisdictional_values` on E-01/E-03/E-08/G-04 and the 875-row clue store are
   real mobility capital.
3. **Adversarial fields — CONFIRMED.** Zero matches for the six columns in `scripts/db.py`; no
   `update-gap` / `update-source`. **NEW:** all 5 live gaps carry `falsification_condition` +
   `named_dissenter` but `confidence_interval` / `shift_conditions` NULL ×5 — legal while OPEN (the
   contract binds at CLOSED), and **no sanctioned writer exists to complete them at closure.**
4. **Retriever ABSENT, APIs live — CONFIRMED.** `scripts/research/` holds only `emit_batch_sql.py`
   and `retrieval_log.py`; curl returns 200 from Crossref / OpenAlex / Semantic Scholar. S1's "notes
   are pure hand-narration with no artefact" is **OVERSTATED for 2 of 10 rows**: the batch-2
   manifest logs `R2 backward mining: reference list of REF-00325` and `REF-00578` through
   `retrieval_log.fetch()`.
5. **`next_gap_id()` — CONFIRMED.** `db.py:135-144` GLOBs `GAP-[0-9]*` against live
   `GAP-B01-001…GAP-B02-001`; falls through to `GAP-001` forever.
6. **`update-bpc` first-write crash — CONFIRMED by code read** (no `--population` flag at
   `db.py:1039-1052`; `population` in `_BPC_META_COLS` :60-66; INSERT branch :1770-1778 → NOT NULL).
   Not executed (read-only).
7. **`opus_reviewed` — CONFIRMED dead** (`db.py:1374` hardcodes 0; no reader; `build_part05`
   :250-266 filters on status only). *Precision:* a PENDING connection's description renders
   verbatim in Part 5; a CONSUMED one renders as a count with provenance deferred to Part 4 —
   direction stands, S4's 5b detail slightly overstated.
8. **`register_integrity_check` — CONFIRMED.** "(DB cross-check on)" is keyed to `args.db`
   truthiness (:430-431); `db_rows` is built from 0-row `specifications`; the per-cell block is
   gated `if db_rows:`; the author's own comment :362-366 admits it; only `--selftest` injects a
   subject.
9. **`synthesis/opus-routing` — CONFIRMED zero enforcement** at every layer:
   `pipeline-contract.yaml:117 check: null`; no model column in `bpc_metadata`; no flag on
   `update-bpc`; no attestation-schema field; `decision_capture` C4 is format-only on the wrong
   table; DR-2026-06-10's own attestation calls the floor unfalsifiable.
10. **OPUS PART 7 — CONFIRMED exactly, re-derived.** 11 refs; admitted = 325/561/578; **8**
    lead-only; REF-00335 caveat ×3 / tier ×0; **exactly five** lead-only refs tier-labelled with
    zero caveats (576/577/589/726/727); 571 mixed; 580 a passing mention. S4's "7 of 11 flat-tiered"
    was wrong in both directions, as OPUS said.
11. **OPUS PART 3 D-10 — CONFIRMED.** 272 distinct mobility DOIs (89 + 184); 16 in
    `source_locators`; 0 admitted; **256 in neither**; 0 full titles; `title_short` truncated.
    (OPUS's per-record coverage counts 319/291/215 vs my 298/266/205 — different counting frame;
    load-bearing numbers identical.)
12. **OPUS D-12 withdrawal — CORRECT.** G2 real (`assess_cell.py:191-195`); `directness.py:225`
    None-is-full is latent only; the retained finding is real: `NOT_ASSESSED` → `COND_DOWN_WEIGHTED`
    → `anchoring()` admits it; `down_weighted` is record-only. OPUS D-1 / D-2 / D-4 also verified
    (`table_connectivity` deleted in `80a34d1`; H03/H04 deleted per `test_db_integrity.py:996`; no
    `update-search`).

## C. Doctrinal rulings

**C1 — R2 and the stranded harvest.** R2 exists so admitted anchors generate the next frame and
surface the contrary and Co-1-adjacent work keyword search misses. With 134/138 harvested DOIs
stranded in `connections_produced` JSON (4 in the clue store, 2 admitted — verified), R2 is reduced
to a per-anchor checkbox: the book's claim to have *"walked this claim's neighbourhood"* is attested
while its consequences never re-enter. **A stranded harvest is questions the thinking tool will
never ask.**

**C2 — R8/R14 and the epistemics of absence.** The distinction is real at row level and *already
practised*: exec 9 is a deliberate AX-PAI deferral; execs 26-28 classify their own zeros
("GENUINE WELL-FORMED ZERO", "ZERO FROM THIS INDEX, NOT ABSENCE"). But it is held by **authorial
virtue**: R14's gate checks non-emptiness only, an empty-string `deferred_reason` corrupts the
boundary, and cause is unstructured. Slug-level "never looked" *is* mechanical (`db.py coverage`:
48 jurisdictions / 19 languages required, 0 searched on every mobility slug). **Ruling:**
distinguishable where someone wrote the row; nothing compels the mobility batch to keep the virtue.

**C3 — Co-1 and CRPD Art 4.3 in a mobility batch.** Partial. R1 *ordering* IS enforced (the DoD's R1
fails a Co-1-less session — verified live). Co-1 **provenance** is not mechanically honourable: no
CLI flag; the validator never runs on the write path (`validate_evidence_state` validates files;
`validate_pydantic_schemas` compares columns); the 3 live `co1` rows got `published_corpus` by
hand-SQL. **Deeper:** `populations` has **no code for ambulant disabled people or part-time
wheelchair users** — `MOB` = "mobility needs; wheelchair users" is itself the umbrella. Axes
distinguish (AX-AMB / AX-WHM / AX-BAL) but cells key on item × population, **so the distinction
collapses at judgment unless the owner mints codes.** That is the batch's most doctrine-loaded
unasked decision, and D-12 means an ungraded Co-1-adjacent source anchors like a graded-partial one.

**C4 — the empty synthesis stage.** Empty synthesis is the *honest* state — 10 sources on one slug
cannot ground weighing, and `pending` exists for exactly this. The live failure is **off-book
synthesis**: the one reasoning doc does synthesis work outside the empty tables, citing 8 unadmitted
leads with tier labels, while gates dress the emptiness as coverage. It becomes a stage *failure*
the day `bpc_complete=1`, or a mobility reasoning doc lands with `specifications` /
`reasoning_doc_citations` still empty, or stub-mode render ships the off-book result.

**C5 — the freeze (OPUS D-9).** **Correct, not overstated — but incomplete.** "complete walk" occurs
exactly once in the whole repository (§2.2, undefined, unenforced), and the weak exit was **ratified
three times in the same instrument** (§2.5(c) signed, §5, §11.1). The check faithfully implemented
the signed clause; the drift is *intra-instrument*, and six adjudication passes missed it. **The
remedy is therefore an owner decision, not a check fix.**

**C6 — the strongest objection.** *This smoke test is the loop §2 diagnosed* — seven agents, ~6,000
log lines, now audits-of-audits, zero searches, zero movement on §4's only criterion; §11 property 5
brands the tree a termination failure. **It does not hold as prohibition:** the freeze is spent by
its ratified exit, and the subject is the write path and live data — not plans — so §7's abolition
does not reach it; pre-batch discovery of the `update-bpc` crash, the R8 writer gap and the unwired
canonical guard is far cheaper than mid-batch. **It holds as a price:** these findings are worth
exactly the batch they unblock, and only if triaged rather than becoming the next 318→389→418 curve.

## D. Top three things the traces missed

1. **The handrail slug.** All seven agents accepted PROTOCOL's premise; `slugs` refutes it. The
   doctrinally-correct question — *does the frame already have a home for handrails?* — was never
   asked. Answer: yes at slug level (STUB, with `sl_path` under the `.ignore`-hidden
   `references/search-log/` — trap §7 in action), no at item level, which is exactly the
   frame-before-item shape §1.4 mandates.
2. **Population-taxonomy adequacy.** No trace queried `populations` against the batch's
   populations-of-concern. Ambulant and part-time wheelchair users have no code, so the umbrella
   erasure CLAUDE.md §6 forbids at *search* time is currently **structural at cell time**.
   Owner-gated, and upstream of every R13 grade and every mobility cell.
3. **The live rows as practice, and the book-consequence question.** Nobody read execs 26-28 (the
   R14 three-way discipline already practised) or the two retrieval-logged R2 fetches — **the honest
   fix is codifying existing practice, not new apparatus.** And nobody ran the mission test, or
   tier-system §3's own corridor-width worked example (1800 mm floor vs 2440 mm Co-1/T2 anchor — the
   batch's exact subject), against the empty `conflicts` / `specifications` tables: **the traces
   audited the machine and never once asked what a disabled reader, an architect, or an advocate
   gets when the machine is green.**
