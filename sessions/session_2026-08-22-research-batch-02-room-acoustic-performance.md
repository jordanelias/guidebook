# session_2026-08-22-research-batch-02-room-acoustic-performance

**Span.** 2026-08-22. **Branch.** `claude/provenance-walk-review-dyw1xk`, PR #113.
**Form.** DR-2026-08-19 §12 runbook, executed step by step. Acts 2 and 4 of
`workplan/2026-08-22-agonist-antagonist-execution-plan.md`, unblocked by owner decisions D-0164/D-0166
and explicitly *not* blocked by D-0165.

**This is a research session, and the first compliant one.** `research_batch_dod.py` returns
**COMPLIANT, exit 0, all fifteen rules**, with a non-zero subject on every rule that has one.
`sessions/LATEST-RESEARCH` is moved to this session — it has subjects.

**State.** `evidence_sources` 5 → **10** · `search_executions` 9 → **18** · `search_candidates` 30 →
**44** · `evidence_population_match` 12 → **25** · `citation_mining` 5 → **7** · `gaps` 4 → **5** ·
`specifications` **0** (D-0165 blocks it) · `user_version` 60 · six data migrations, canonical
`abc71e24…` → `84b3ca41…`, every write through `emit_batch_sql`/hand-SQL → `emit_data_migration` →
`migrate_db`. `test_db_integrity` **72/72**; reproducibility PASS including `--deep`.

---

## 1. What the batch found, and why it matters

**Batch 1's central claim is refuted by retrieval, not by argument.** It held that no numeric value
was authorable for A-18 × AUT. The corrected frame — parameter × setting × population, the three-way
cross that none of batch 1's nine queries made — returned an A-B-A single-case study that
**explicitly tests RT = 0.4 s Tmf with ASD children** (RT modulated 1.1 → 0.39 s), measured RT/C50/STI
in classrooms built for autistic pupils across two countries, a special-needs classroom field study,
and a 50-country survey of national targets. R14: the earlier null was a **batch-frame query-shape
failure**, and no row in `search_executions` could have expressed it, because every individual query
was well formed.

**MH and BRAIN were searched for the first time.** `GAP-B01-003` recorded that MH — 5 of 13 items on
this slug — was never searched, never deferred and never mentioned, a larger unrecorded hole than the
SCI absence that *was* elaborately recorded. Both yielded. So both silences were coverage failures,
not absence.

**BRAIN yields on the population and not on the parameter, and that distinction is the finding.**
Interview and IPA studies of noise sensitivity after brain injury are plentiful; not one carries an
RT60, NRC, STC or NC value. BRAIN is well evidenced for acoustic *vulnerability* and unevidenced for
acoustic *performance*. Admitting any of it against a room-acoustic item would have repeated exactly
the REF-00967 error the 2026-08-20 pass caught, so none was admitted.

**OD-5 was demonstrated three separate times in one batch.**
1. The R9 pre-check — run by hand, because R9 cannot — found **three of five** candidate DOIs already
   held as `source_locators` leads: REF-00561, REF-00578, REF-00325.
2. REF-00561 reached admission through that stash lookup and **appeared in the top results of none of
   the six literature queries**. It is logged as its own retrieval act (exec 16) rather than
   misattributed to a search that did not surface it.
3. Backward mining from REF-00325 surfaced **four more** held-but-invisible leads — REF-00579,
   REF-00327, REF-00577, REF-00576 — of which Neuman 2010 and Wroblewski 2012 are named Tier-1
   anchors in this project's own reasoning document, and **REF-00327 is Finitzo-Hieber & Tillman
   1978**, the foundational room-acoustics-and-hearing-impaired-children paper and the ancestor of the
   entire Iglehart line. The project has held it, unseeable, since the reset.

## 2. The five admissions, and the grade that matters most

| ref | source | tier | derivation |
|---|---|---|---|
| REF-00561 | Bettarello, Caniato, Scavuzzo & Gasparella 2021, *Applied Sciences* 11(9):3942 | 3 | `clinical`/`lower_control` |
| REF-00578 | Iglehart 2016, *Am J Audiology* 25(2):100–109 | 1 | `clinical`/`high_control` |
| REF-00325 | Iglehart **2020**, *Am J Audiology* 29(1):6–17 | 1 | `clinical`/`high_control` |
| REF-00969 | Rosas-Pérez, Galbrun, Stewart & Payne 2023, *POMA* 51:015001 | 3 | `clinical`/`lower_control` |
| REF-00970 | Markussen, Sentop Dumen, Harbak & Rasten 2024, *INTER-NOISE* 270(4):7759–7768 | 3 | `grey`/`intrinsic` |

Every tier is **derivable** from `schemas/tier_derivation.py`, not asserted — the defect this session's
predecessor found on all five of batch 1's rows.

**The central R13 finding, which must not be softened.** The strongest Tier-1 evidence this project
holds on its flagship parameter studies **deaf and hard-of-hearing children**, and `DEAF` carries
**zero** `item_population_links` on this slug. So MB2-004 and MB2-007 are capped at **PROXY** — graded
against COM as the nearest served population — on two independent mismatches: children against
adult-serving cells, and a population the item layer does not connect to this slug at all.
**A Tier-1 study with a hard number is still PROXY when its population is not the one served.**
That is D-0165's taxonomy question now visible in the data rather than only in prose.

Grades written: 1 EXACT · 4 PARTIAL · 2 PROXY · 6 MISMATCH. The six MISMATCH rows are deliberate —
they exist to stop the 0.3 s figure drifting into NDV or DEM cells on the strength of being the only
hard number available.

**REF-00969 was tiered DOWN on purpose.** Same team and same 12-adult cohort as REF-00965, which
carries `co1`/T1. **OD-D disputes exactly that lineage's co-production warrant**, so admitting a
sibling at Co-1 would compound a disputed grade. Graded T3. If OD-D sustains Co-1, re-grade it up.

**No numeric value was written to any value column.** The 0.4–0.7 s and 0.3 s figures are
`[UNVERIFIED-QUANT]` and live in notes, because no full text was read. `GAP-B02-001` records that
exposure by name.

## 3. What the machinery did, and what it did not

`scratchpad/<this session>/machinery-trace.md` measures it, derived from the schema, the registry and
the pipeline map — **not from grep**, per the rule ratified today.

The batch wrote **8 tables of 65**. **33 of 65 hold no rows at all**, and the emptiness divides three
ways that should never be conflated: blocked on the owner (`specifications` and the determination
stratum — D-0165), correctly empty (`economics_entries`, `case_studies` — R12 routes findings there
and none occurred, which the DoD gate *confirmed* rather than assumed), and structurally unreachable
or superseded (`item_bpc_links` at 0/93, `reasoning_doc_citations` FK-blocked by OD-5, the frozen
legacy coverage tables). **All 17 views were unused again**, including `v_coverage_priority` at 7,208
rows — the largest derived object in the database, read by nothing.

**Three gates caught real defects in this batch, and each was fixed rather than argued with:**
- The blocking `citation_mining_completeness` gate refused the batch because a confirmed T1 source had
  no mining row. It was right; the omission was mine. Mined, and the gate went CLEAN with `Examined: 2`.
- `test_db_integrity` **I1** refused five VERIFIED rows with `verification_disposition` NULL —
  *verified with effort still owed*. That refusal is what forced `GAP-B02-001` to be **written rather
  than assumed**.
- `test_db_integrity` **C08** caught that two mined sources still read `citation_mining_status='pending'`.

## 4. My own errors

| error | how it was caught |
|---|---|
| Wrote in exec 14's note that Iglehart's second paper was **2019**, inferring from the DOI slug `2019_AJA-19-0010` | The retrieved payload says **2020**. The reasoning doc was right and I was wrong. Corrected in the row **before any admission was written**, so no bibliographic field inherited it |
| `db.py log-mining --ref REF-00325` — passed the **global** id to a flag that writes `local_ref_id` | The blocking gate kept reporting a PROTOCOL VIOLATION for mining that had actually been performed. A write path that silently mis-keys a row makes a blocking gate **under-report**, which is the same class as the R9 blindness this batch documented three times |
| Tried to fix that by re-keying through `emit_batch_sql` | The tool **correctly refused** — `local_ref_id` is part of the primary key, so the change read as a deletion and the capture path is additive-only. Redone as hand SQL, which is the path CLAUDE.md §4 names for exactly this |
| Two `search_candidates` inserts rejected on column type and CHECK constraint (`tier_guess` INTEGER; `locator_status` ∈ UNVERIFIED/RESOLVED/DEAD) | The constraints. Noted because the *fix* mattered: two leads had no captured title and `title` is NOT NULL, so rather than inventing titles I retrieved them — which is how **Finitzo-Hieber & Tillman 1978** was identified |

The generalisable one is the first: **a bibliographic claim written from anything other than the
bytes**. That is the failure this whole line of work exists to close, and it recurred in the session
auditing it. It was caught only because R10 forces a re-retrieval before admission.

## 5. The adversarial pass — it sustained four findings against me

Run blind-then-compare per DR-2026-08-19 §7, by a fresh context that re-derived tiers and population
grades from the payload bytes **before** reading any of my notes. This is the **one** pass this batch
gets, and its subject is a diff that wrote research rows — so unlike the 2026-08-22 review, it is
lawful under `references/project-standards.md`.

**Divergence log.** Tiers: no divergence on any of the five — the antagonist's blind derivation
matched every stored tier, and `check_tier_consistency()` returns True for all five triples.
Population grades diverged on three rows, and **the antagonist was right on all three**:

| row | I graded | blind grade | outcome |
|---|---|---|---|
| MB2-001 / MB2-002 — REF-00561 → AUT/NDV | PARTIAL | **PROXY** | **corrected.** R13's ratified hook says *"no-participants = PROXY"*, and this study has no autistic participants — it measures seven rooms. My own mismatch_note said exactly that and then graded a step above the rubric anyway: a grade contradicting its own stated reason |
| MB2-012 — REF-00970 → DEM | PARTIAL | **PROXY** | **corrected.** Participation is not established in the retrieved record, and my note admitted it. The antagonist named the motive precisely: `GAP-B01-002` wants a DEM admission *above* PROXY, which is the incentive to round up |
| MB2-004 / MB2-007 — Iglehart → COM | PROXY | PARTIAL-vs-DEAF | **resolved against the antagonist.** DEAF is not in the served set, so there is nothing to grade against; PROXY-vs-COM is the honest encoding |

Two more sustained, both corrected in the same pass by migration:
- **Venue typing was inconsistent.** REF-00969 and REF-00970 are both conference proceedings and were
  typed differently within minutes — so no stable rule was being applied. Rule now written down and
  applied to both: **evidence_type follows the study design; `grey_flag` records the venue.** Tier is
  unchanged at 3 either way. Note the trap avoided: Crossref types one `proceedings-article` and the
  other `journal-article` though both are proceedings, so typing off the payload's `type` field would
  have produced the opposite and equally unstable answer.
- **`target_scope='national'` on exec 15 is not a ratified pair** — `national_fw` admits only
  `intrinsic`. Corrected. The `target_*` columns are not covered by the CHECK constraint that guards
  `evidence_sources.scope`, so an unratified literal was accepted silently. That validation gap is a
  finding in its own right.

Grades after correction: **1 EXACT · 1 PARTIAL · 5 PROXY · 6 MISMATCH** — materially more
conservative than what I wrote. `research_batch_dod` still COMPLIANT, `test_db_integrity` 72/72,
`adjudication_integrity` PASS.

**Two findings deliberately NOT actioned in this session, and why:**
- **The DoD gate prints PASS over empty subject sets.** The antagonist measured 4–5 of the 15 rules as
  gating nothing this batch (R3 saw 0 regulatory sources, R11 0 aliases, R12 0 economics findings,
  R14 0 zero-yield rows). *"COMPLIANT — all rules met"* is therefore stronger than what was tested.
  This is CLAUDE.md §2(a)'s signature failure living inside the research gate itself. The fix is not
  cosmetic: `ok(code, msg)` takes no subject count, so instrumenting it means threading one through
  all fifteen rules of a **blocking** gate whose selftest asserts 15/15. **Next act, done deliberately
  with the selftest in front of you — not hastily at the end of a long session.**
- **A-18 has zero `item_population_links`**, which is a structural defect *distinct* from the DEAF
  question and belongs in the D-0165 packet explicitly. The flagship item of this slug serves no one
  in the item layer.

The antagonist's own summary is worth keeping: *"a batch that mostly out-audited its auditor"* — and
the single best judgement in it was mine only by refusal, the BRAIN call that vulnerability evidence
is not performance evidence.

## 6. HANDOFF

**Still blocked on the owner:** the population-taxonomy pass (**D-0165**) — no cell on this slug is
authorable until it lands, and this batch has now made the cost concrete: the best Tier-1 evidence on
the parameter is capped at PROXY because the population it studies is not served here. **OD-D**
(REF-00965/00968 Co-1 → T3) now also governs REF-00969. **OD-F**, **OD-G** open.

**Unblocked next, no decision needed:**
1. **Promote the four mining-surfaced leads** — REF-00327 (Finitzo-Hieber & Tillman 1978), REF-00577,
   REF-00576, REF-00579 — through R1–R15. All held, all invisible to R9.
2. **Resolve the ten staged candidates**, starting with Ghazanfar 2026 (the RT 0.4 s ASD threshold
   test) and Tardini 2025 (50-country targets), which between them could verify or refute a dozen
   cells of the reasoning doc's 16-jurisdiction table in one pass.
3. **Read the five full texts** and close `GAP-B02-001`. Until then the 0.4–0.7 s and 0.3 s figures
   stay `[UNVERIFIED-QUANT]`.
4. **A genuine Italian-language sweep.** Exec 15 was posed in Italian and answered in English; the row
   says so, and `languages_searched` must not count it as IT coverage.
