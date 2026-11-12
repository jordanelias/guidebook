# HS-3 — Improvement programme

_Handshake leg, 2026-11-12 (UTC), HEAD `186defb`. Nothing here is implemented; the repository, the canonical database and git state are untouched. Every figure cites a command in `hs-handshake-matrix.md` (HS-1) or `hs-adversarial-findings.md` (HS-2); re-run before relying on one._

## 0. Verdict first

_Amended 2026-11-12 after an independent antagonist pass (`fa-antagonist-objections.md`). What changed, and why, is in §6 (resolution record) and in `fa-corrections-for-suite.md`. The first version of this section was wrong on what can start now and on what must precede a first determination._

**No determination should be made canonical until three things hold.**
1. **The engine gathers by the lens tags on the figure.** No gate tests the lens today (HS-2 F-01). This is the prior workplan's task T-3 (`workplan/2026-10-23-pipeline-resolution-workplan.md`), which needs T-2, which needs T-1a (IMP-08). The owner has also ruled a link table for several codes of one model (PS:4926; IMP-40); building it before or inside T-3 is this leg's sequencing, which the ledger does not state. It is not a first-wave item.
2. **The blocking `test_db_integrity` criterion C10 is green for the cell.** Every `provisional` cell determined on a scratch copy fails it today (only parameters 3 and 12 determine `provisional`): parameter 3 on four governing sources that are not `VERIFIED`, parameter 12 on one (R-6). The ledger records this as intended (PS:4544).
3. **The mobility split is executed.** It is ratified (PS:1291-1296); it is a research change with one execution question left to the owner (IMP-20, OD-14).

The specification validators do examine a live row when one exists. Their defect on `main` is narrower than first stated: they count retired rows as their subject (IMP-04).

**What can start now, with no owner word, no unmet dependency and nothing turning red on `main`** (§3 gives the dependencies): IMP-02, IMP-03a, IMP-04 (report-only form), IMP-06, IMP-12 (columns only; it deletes nothing), IMP-13 (two of its values), IMP-23, IMP-43, IMP-44, IMP-45 (the last three from the stress audit, §7), and the two tasks the prior workplan marks "needs nothing" and whose done-when is still unmet, T-1a and T-6a (IMP-24 is T-6a). IMP-01 needs one owner reply. Everything else waits on a dependency or on the owner.

**The programme is blocked behind the owner at eight points that matter:** what a jurisdiction is to a determination (OD-01), what language a page is in (OD-02), how a concept is held without English (OD-03), what the scope answer of 2026-10-30 covers (OD-04), how a later parameter reaches a source already read (OD-23), how coarse a parameter is (OD-24), what a synthesis row is (OD-07), and how render is produced and stored (OD-12).

Counts: improvements `grep -c '^### IMP-' <this file>`; of which withdrawn `grep -c '^### IMP-.*WITHDRAWN' <this file>`; owner decisions `grep -c '^### OD-' <this file>`; of which withdrawn `grep -c '^### OD-.*WITHDRAWN' <this file>`; new acceptance tests `grep -c -E '^\| AT-([5-9][0-9]|1[0-9]{2}) ' <this file>`.

## 0.1 How to read an entry

- **Change type**, in the order CLAUDE.md §8 prefers: `NOTHING` (and why) · `CONVENTION` (a rule, a record, a mark) · `REUSE` · `DELETE` · `CODE` (the smallest that closes the defect).
- **TD** = the requirement(s) it serves (REQ, HS-A, C-). **BU** = the defect it closes (BU section, HS-2 finding). An entry with only one side is not justified and is not listed.
- **Reads it** / **Wrong thing reaching the guidebook without it**: the two questions CLAUDE.md §8 requires.
- **Kind**: `TOOLING` or `RESEARCH` (rule 10: separate pull requests; tooling merges first). **Layer** per the 2026-09-09 ruling.
- **AT** = the acceptance test that is red today (TD's AT-01 to AT-49; this file's AT-50 onward, §4).
- **Owner gate**: `none` · `OD-nn` (blocked until answered) · `ruled, confirm` (the owner has ruled; execution detail is the owner's).
- Authority for `none` items: the owner's grant of 2026-11-12 (PS:5228, PS:5234) to design, author, curate, orchestrate, delete, stress test, patch and iterate on the code pipeline. It does not reach doctrine.

---

## 1. Improvements

### Wave 0 — records, marks and reporting

### IMP-01 Record what the plan will cite
- **Change:** CONVENTION. Ledger entry quoting O1–O8 of 2026-10-12 (relayed, IG:11) with the owner's confirmation of the wording; supersession back-pointers for C-05 (PS:123, PS:129), C-16 (the 2026-08-19 rule against adversarial review of plans, superseded for this audit) and C-20 (PS:120).
- **TD:** REQ-005, C-05, C-16, C-17, C-20. **BU:** none measurable; `supersession_backpointer_audit` covers only named supersessions.
- **Reads it:** every later session, through CLAUDE.md §9 "Latest rulings". **Wrong thing:** a plan built on relayed sentences that bind nothing mechanical (PS:2763-2765).
- **Files:** `references/project-standards.md` (append only). **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-75 (partly). **Risk:** low. **Owner gate:** the owner confirms the O1–O8 wording in one reply; not doable before it. The objective itself is already recorded (PS:5218-5241).

### IMP-02 Mark what is superseded where a session will read it
- **Change:** CONVENTION. Correct the pipeline contract header to what its decision record says (accepted on the owner's ratification of 2026-07-21, with an owner-action precondition outstanding; `decisions/DR-2026-07-13-pipeline-contract.md:3`; PS:584 ACTION (4) does not let a mark skip a named precondition) (HS-A06); supersession banners on `architecture/navigation-modes.md` and `architecture/page-templates.md` (C-14); correct CLAUDE.md §5(c) "persists every payload" to the 2026-11-06 ruling (C-15).
- **TD:** HS-A06, C-14, C-15. **BU:** HS-2 F-04; BU §E (render prose homes describe a deleted model).
- **Reads it:** sessions orienting from CLAUDE.md §9 and the contract. **Wrong thing:** a renderer built to route by old item codes and to read `●` as "stated".
- **Files:** `governance/pipeline-contract.yaml:2-3`, the two architecture files, `CLAUDE.md`. **Deps:** none. **Layer:** 0–1. **Kind:** TOOLING. **AT:** AT-43. **Risk:** `research_contract_sync` and `claude_md_spine` read these files; run both after. **Owner gate:** none for marks; ratifying the corrected contract is OD-17.

### IMP-03 Make the contract say what the owner's order says, in both directions
Two parts, because they have different gates.
- **IMP-03a — text.** Change: CONVENTION. Rewrite the synthesis and specification `entry:` strings (C-11), the research entry's "item" and the evidence criterion's "BPC synthesis claim". No key is added and no criterion id changes.
  - **TD:** REQ-002, C-11. **BU:** BU §A.5 (circular entries). **Reads it:** `pipeline_contract_audit`, `/run-pipeline`. **Wrong thing:** a session takes "a determination with a resolved value" as the input to synthesis.
  - **Files:** `governance/pipeline-contract.yaml`. **Deps:** none. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-43 (first half). **Risk:** `run_checks.py --selftest` if a basis id is touched; none is. **Owner gate:** none (the owner's order is ruled, PS:1454).
- **IMP-03b — a `re_entry:` list per stage.** Change: CODE. Every model in `schemas/pipeline_contract.py` sets `extra="forbid"` (lines 14, 23, 31, 39), so a new key is a schema change, not a convention.
  - **TD:** REQ-003, REQ-016. **BU:** BU §B.4. **Reads it:** `pipeline_contract_audit`. **Wrong thing:** a re-entrant run has no stated precondition.
  - **Files:** `schemas/pipeline_contract.py`, the contract. **Deps:** IMP-12 to IMP-14 name the carriers. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-43 (second half), AT-44. **Owner gate:** OD-18. Sequenced in Wave 2, not Wave 0.

### IMP-04 Make the specification checks report what they examined, without changing what the runner counts
- **Change:** CODE, report-only. Four checks examine or count retired determinations on a database with no live one: `validate_evidence_state` ("8 cells", `EXAMINED: 13`), `validate_verification_consistency` ("5 stated/provisional specification(s)", `EXAMINED: 5`), `adjudication_integrity` (a readiness line "8 determination(s)"; its `EXAMINED: 59` is sources and is not affected), `derivation_handshake_integrity` (a sentence that says the table is empty). Each prints one further line stating how many of the rows it read are live and how many retired, in the manner `test_db_integrity` already uses for its own criteria ("PASSED HAVING EXAMINED NOTHING (…)"), and the false sentence is derived from the tables.
- **What it must not do.** It must not change what the `EXAMINED:` token counts. `validate_evidence_state`, `validate_verification_consistency` and `adjudication_integrity` are blocking with `min_items: 1`; `run_checks.vacuity_failure` (`scripts/run_checks.py:300-336`) returns a failure below the floor and `run_check` returns `FAIL` before it tests for nothing-in-scope. A live-only count would print 0 and turn blocking checks red on untouched `main` until the first live determination. The first version of this entry proposed exactly that and was wrong (FA-01).
- **TD:** REQ-020, CLAUDE.md §5(a), §5(b). **BU:** BU problem 2; HS-2 F-11, F-19.
- **Reads it:** a person or session reading the check's output. `run_checks.py` does not read the new line. **Wrong thing:** a reader takes "8 cells validated" as evidence about live determinations. This is a reporting defect; it is not a precondition of a first determination, because each of these checks reads a live row when one exists (observed on a scratch copy: "9 cells").
- **Files:** `scripts/validate_evidence_state.py`, `scripts/validate_verification_consistency.py`, `scripts/audit/adjudication_integrity.py`, `scripts/audit/derivation_handshake_integrity.py`. No registry change. **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-54. **Risk:** low. **Owner gate:** none.
- **Deferred, stated:** whether retired rows should be validated at all, and whether the floor should count live rows, is decided in one change with the registry entry once a live row exists; before that, any such change is red on `main`.

### IMP-05 Deletion candidates, each behind a caller sweep (nothing is deleted in Wave 0)
- **Change:** NOTHING now. The first version ordered five deletions as having no reader. Three were wrong and two were unproven (FA-03, FA-20, FA-32):
  - **The four unlinked skill files are not candidates.** Each has readers: `.claude/agents/antagonist.md:71` and `governance/pipeline-contract.yaml:105,113` (`adversarial-research`); `governance/pipeline-contract.yaml:312-314`, `scripts/audit/claims_docket.py:3,134`, `scripts/validate_verification_consistency.py:94` (`integrity-protocol`); `governance/decision-protocol.md:59`, `data/adversarial_use/catalog.yaml:16` (`voice-style`); `governance/retired-vocabulary.yaml` (`evidence-metadata-rehabilitation`). They are unlinked because each lacks a frontmatter `description:` line, which `python3 scripts/sync_claude_skills.py --check` says a person must write. That is a small owed edit, not a deletion.
  - **`assess_cell --slug` is read.** It is validated (`scripts/assess/assess_cell.py:1963-1969`) and written into each gap the engine files (`:2224-2228`). It selects no evidence; it is not vestigial.
  - **`v_item_provenance` is not a subset of another view.** It reads `specification_source_links`; `v_determination_provenance` reads `specification_extraction_links`. On a scratch copy with four live cells they return different row sets. It is a cross-stage pointer and stays.
  - **`reasoning_doc_citations` and `connections.opus_reviewed` have callers** (`git grep -l reasoning_doc_citations -- scripts schemas governance skills .claude`; `grep -n opus_reviewed scripts/db.py governance/conceptual-model.md`). They remain candidates only after a rule-4 sweep names every caller and its disposition; `opus_reviewed` goes with IMP-32.
  - **`gap_mining`, its three verbs and its audit** remain a candidate tied to IMP-12, behind the same sweep (callers include `skills/gap-driven-mining_SKILL.md`).
- **TD:** REQ-092, HS-A16. **BU:** §G.1, §G.2.
- **Deps:** a `repo-sweep` agent run per object (views, skills, registry and prose are callers, CLAUDE.md rule 4). **Layer:** 2. **Kind:** TOOLING. **AT:** `run_checks.py --selftest` and `schema_reference_audit` after any deletion. **Owner gate:** none for code; the four `description:` lines are a person's to write.

### IMP-06 One home for "answered"
- **Change:** REUSE. `governance/owner-browser.yaml` derives each prompt's answered state from the ledger heading that answers it, or drops the field.
- **TD:** REQ-046. **BU:** HS-2 F-19 (OR-1c).
- **Reads it:** `owner_browser_build.py`, the owner. **Wrong thing:** the owner is asked again, or a session treats an answered question as open.
- **Files:** `governance/owner-browser.yaml`, the builder. **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-75. **Risk:** low. **Owner gate:** none.

### Wave 1 — gates that can go red, and the engine's subject

### IMP-07 Register the stage-pair gate, when it can be green
- **Change:** REUSE. The ruling is "one registry entry that fails when a stage pair has no path" (PS:4761); the prior workplan defines the test as no `NO PATH` line in either zigzag section of `walkability.py` (§8 items 6–7).
- **Why it is not a first-wave item (FA-12).** The instrument prints `NO PATH` on ten lines today (five pairs ending at render, in each of two sections). Registered now, at any level, the check is red on untouched `main`. The ledger's own note says so: registering before the views key lands "would fail at once" (PS:4761). The first version of this entry proposed a different test (non-zero only when an existing path is lost) with the absent pairs "derived from the stage map's empty stages"; that is not the ruled gate, and the derivation does not work, because the stage map gives render one table (`weighting_profile`), so no stage is empty.
- **TD:** REQ-006, REQ-017. **BU:** HS-2 F-03.
- **Reads it:** `run_checks.py`, once registered. **Wrong thing:** a migration severs a stage from the spine unseen.
- **Files:** `governance/check-registry.yaml`, `governance/stage-map.yaml` (`views:` key, OW-1), the instrument. **Deps:** a render view mapped to the render stage (IMP-38; workplan T-5). [U: that a mapped view gives the render pairs a path cannot be run, because the instrument has no `views:` support yet; the ledger's own note is only that the entry is added once the views key has landed.] Until then the instrument is a command run at the end of each phase, which is the alternative the workplan names. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-01, AT-53. **Owner gate:** none for the ruled gate; an interim form is OD-26.

### IMP-08 The engine gathers by the lens tags on the figure (the prior workplan's T-3)
- **Change:** CODE. A figure reaches a cell only through the lens codes written on it; a figure tagged for everyone reaches only a cell for everyone; no traversal through a crossing map.
- **Warrant, stated by class (FA-21).** OWNER for the `ALL` half: "No, ALL reaches only an ALL determination" (PS:4657). LEDGER reading for the general rule: PS:4630 is the assistant's reading, "Taken from the prompt's 'yes'" (the owner's own OR-1 answer contains no "yes"), marked as the assistant's at PS:4628, with D-0184 ACTIVE. It is not owner speech.
- **This is task T-3 of `workplan/2026-10-23-pipeline-resolution-workplan.md`**, and its dependencies are that plan's, which the first version of this entry dropped (FA-05): T-3 needs T-2 (conditions); T-2 needs T-1a (reading), whose done-when is unmet (`grep -rn "def parse_bound" scripts` still returns `scripts/assess/assess_cell.py:624`); and "how a determination and its figures carry several codes of one model is settled by OR-1c before this PR opens", which is the link table of IMP-40. T-3 also changes the attestation (the hash covers every lens code), makes a pending cell claim no derivation path, and lets a NULL lens be filled with warrant. D-2 (filling a NULL lens where a quote names the users) follows T-3.
- **TD:** HS-A02, REQ-077, REQ-074. **BU:** BU problem 3; HS-2 F-01.
- **Reads it:** every determination. **Wrong thing:** "ramp gradient for Deaf people: at most 5 %", governed by 35 code provisions tagged `MOB`.
- **Files:** `scripts/assess/assess_cell.py` (the gather functions, `sha`); tests. **Deps:** T-1a → T-2 → IMP-40 → this. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-50, AT-51, AT-34, and the workplan's L1–L5 and M9–M12. **Risk:** changes every answer the engine gives; none is live. **Owner gate:** none. The rule-version label is not an open question: the workplan derives a bump for T-3 (WR-2) and the owner set the precedent (PS:4546).

### IMP-09 No stored row for a lens no figure carries (part of T-3)
- **Change:** CODE, inside T-3, whose done-when already reads "no row is stored for a lens no figure carries". With no figure tagged for the lens the engine writes nothing.
- **Warrant.** OWNER: "Do not store table rows for parameters when there is a missing lens … for when the parameter is not relevant" (PS:4614). LEDGER `[ASSUMPTION]`, unratified by its own ACTION (6): relevance is shown by the figures that carry a lens, and "the gaps table still records a missing figure for a lens that is relevant" (PS:4630).
- **TD:** REQ-074, C-13. **BU:** scratch run parameter 3 × `DEAF` stored a `provisional` row although no figure of parameter 3 carries `DEAF`. (The first version also cited parameter 7 × `DEAF`. Parameter 7 is reverberation time, which plainly concerns Deaf and hard-of-hearing people; that run breaks only the unratified assumption, and the gap it wrote is what the same assumption keeps. FA-13.)
- **Reads it:** render's empty-state rule. **Wrong thing:** rows for people a parameter does not concern.
- **Deps:** IMP-08. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-52, AT-33. **Owner gate:** OD-08 for what an absent cell means and whether a relevant lens with no figure keeps a stored row.

### IMP-10 The two seeded-defect tests that are missing
- **Change:** CODE, two fixtures. Of the five other defects the first version listed, four already have a seeded test (FA-08); the fifth, a retired row surfaced by a view, has none, and the first amendment of this entry wrongly said it had (the existing test is that a retired determination is not *stale*, a different defect): `scripts/tests/test_validate_evidence_state_2_4.py` (eleven seeded defects, the first "stated without a governing source"); `scripts/tests/test_evidence_cell_state_2_3.py:221` (a regulatory-only row above the weakest marker, also refused by the schema CHECK); `scripts/tests/test_assess_cell_pilot.py:843-858` (a demoted confirmer found by its marker; a corrected comparator found by its bounds; a retired row treated as history). All three are registered in the `tests` battery at advisory level. Absent: a determination whose linked figures carry another lens (inside T-3's tests), and a retired determination surfaced by a determination view (TD's AT-19).
- **TD:** HS-A02, REQ-077. **BU:** HS-2 F-01.
- **Reads it:** the `tests` battery. **Wrong thing:** the lens fix regresses unseen.
- **Deps:** written before IMP-08 merges, so it is seen red first. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-55. **Owner gate:** none.

### IMP-11 WITHDRAWN — identifiers allocated where rows land
- **Change:** NOTHING. The first version said the engine "cannot determine two cells independently" and that "dynamic" meant one cell per merged pull request. That was wrong (FA-09). Four cells determined one after another on one scratch copy took `specification_id` 9 to 12 and gaps `GAP-103` and `GAP-104`, and `emit_batch_sql.py` captured them as one delta. Ids collide only between two separate copies of the same base, which is true of every id a `db.py` verb allocates on a scratch copy; the engine's emitted header already says to regenerate against the canonical database before replay (`scripts/assess/assess_cell.py:2183-2187`), and the workplan merges one pull request at a time (WR-1).
- **Now known (stress run, `crosstopic.005`):** three separately captured batches fail at rebuild on `UNIQUE constraint failed: evidence_sources.ref_id`. The collision is real for parallel batches and is taken up, in its corrected form, as IMP-41.
- **Convention that stands in its place:** one scratch copy per batch of cells; regenerate before replay.

### Wave 2 — typed causes for backward travel

### IMP-12 A gap that says what it is a gap in, and a search that says which gap caused it
- **Change:** CODE (schema). `gaps` gains `parameter_id`, the four lens columns, `jurisdiction`, `language` (FKs where a table exists); `search_executions` gains `gap_id`. Nothing is deleted by this entry: `gap_mining`, its verbs and its audit become a deletion candidate under IMP-05's caller sweep, and they have callers (`git grep -l gap_mining -- scripts schemas governance skills .claude ':(exclude)scripts/migrations'`: the registry entry `gap_mining_audit`, two test files, `scripts/audit/graph/topology.py`, `scripts/audit/graph_audit.py`, `scripts/db.py`, `scripts/dbcore.py`, `skills/gap-driven-mining_SKILL.md` and governance files).
- **TD:** REQ-040, REQ-014, B10, C-21. **BU:** BU §B.4; RENDER-CONTRACT E8 "BLOCKED: `gaps` has no parameter key".
- **Reads it:** the engine (writes), `coverage`, render's Gaps element, IMP-35's cell status. **Wrong thing:** the book's stated gaps cannot be listed for a parameter or a group.
- **Files:** a schema migration; `db.py add-gap`, `log-search`; `assess_cell.py:2225`. **Deps:** OD-11 only for which stage's contract carries it. **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-10, AT-73. **Risk:** 110 existing gaps have prose subjects; backfill is a RESEARCH task, not a migration guess. **Owner gate:** none.

### IMP-13 Follow-ups that cover the ruled backward edges
- **Change:** CODE (one CHECK widened). `extraction_follow_ups.reason` gains values for a skimmed figure owed a full read (REQ-037), an absence finding owed its tested value (REQ-039) and a question raised by the owner or a reader. "Provisional owed a re-read" waits on OD-10.
- **TD:** REQ-037, REQ-038, REQ-039, B8, B11. **BU:** BU §A.4 (one reason, 0 rows).
- **Reads it:** `extraction_follow_up_audit`, the engine (already excludes rows under an open follow-up), render's "state of each reading". **Wrong thing:** a skimmed or doubtful figure is forgotten and later treated as read.
- **Files:** schema migration; `db.py raise-follow-up`. **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-08, AT-11, AT-72. **Risk:** vocabulary by CHECK, derived by `dbcore.check_values` (rule 8). **Owner gate:** OD-10 for the provisional value; OD-21 for reader questions.

### IMP-14 A question about a cell
- **Change:** REUSE first. Options: (a) widen `determination_gates` (three more lens columns to match the cell key; a verdict for "questioned"; tier nullable); (b) reuse `adversarial_findings(subject_table, subject_key)`, which is generic but untyped and needs a pass row. Recommendation: (a), because the engine and one view already read open gates.
- **TD:** B17, the edge render → specification TD could not warrant. **BU:** BU §B.4 "render → judgment: No".
- **Reads it:** the engine (caps a cell under an open gate), render. **Wrong thing:** a reader's or the owner's objection to a published value lives in a session file and the value stays up unflagged.
- **Files:** schema migration; `raise-determination-gate`. **Deps:** OD-21. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-72. **Risk:** low. **Owner gate:** OD-21.

### IMP-15 A marker for "why the run came back": do nothing
- **Change:** NOTHING. The cause of a return is the gap, follow-up or gate row of IMP-12 to IMP-14 joined on session. A separate marker would be a second home for the same fact.
- **TD:** REQ-003. **BU:** BU §B.4 last row. **Owner gate:** none.

### IMP-16 WITHDRAWN — staleness
- **Change:** NOTHING. The first version proposed that `stale_determinations` also recompute the marker and that three unguarded routes be closed, citing PS:4508. Both halves were wrong (FA-06). The marker is already in the recomputed answer (`STORED_ANSWER`, `scripts/assess/assess_cell.py:1772`) and is tested (`scripts/tests/test_assess_cell_pilot.py:843-858`). PS:4560 says the routes listed in the earlier corrections "no longer stand as listed": `db.py` refuses a change to any column the engine reads of a source or a row under a live determination (`dbcore.ENGINE_SOURCE_COLUMNS`, `ENGINE_EXTRACTION_COLUMNS`, `scripts/dbcore.py:406-409`), and a finding added later is not refused by design; K02 reports it.
- **What remains true:** these guards and K01/K02 have a zero live subject on `main` (AT-76, unproven until a live row exists).

### Wave 3 — the base, as data (REQ-097)

### IMP-17 Jurisdictions in a table, read by the writers
- **Change:** CODE that deletes code. A base table of jurisdiction codes (kind: country, supranational, standards body, sub-national; parent; the ledger entry that admitted it); `dbcore.check_jurisdiction` reads it; the Python enum is generated from it or removed; `lang_jur_map.jurisdiction` gains the FK.
- **TD:** REQ-065, REQ-093, C-08, HS-A16 ("the less hard coded, the better"). **BU:** BU problem 6; Q32 (17 codes the enum lacks). PC:49 already says "base.jurisdictions, which has no table yet".
- **Reads it:** six writer call sites, `jurisdiction_db_vocabulary`, `coverage`. **Wrong thing:** research for a declared pair cannot be logged with its jurisdiction, so coverage can never read complete and a comparison table has holes that look like absence.
- **Files:** schema migration; `scripts/dbcore.py:945`; `schemas/enums.py`; the table's own writer ships in this change. **Deps:** none (IMP-19 does not cover this table). **Layer:** 1. **Kind:** TOOLING. **AT:** AT-28, AT-58. **Risk:** admitting a code is a scope decision (PS:3714): the table carries the approval pointer and the writer refuses without it. **Owner gate:** none for the mechanism; OD-04 for membership; OD-01 for sub-national rows.

### IMP-18 The scope, recorded
- **Change:** data. Fill `lang_jur_map.scope_status` for every pair from the owner-confirmed set.
- **TD:** REQ-063, REQ-064. **BU:** HS-2 F-14.
- **Reads it:** `v_research_scope`, `coverage`, render's E2.scope. **Wrong thing:** research is asked for from places the owner excluded, and the comparison table has no list to be cut to.
- **Deps:** IMP-19 (no writer today), OD-04. **Layer:** 3. **Kind:** RESEARCH (data PR). **AT:** AT-27, AT-57. **Owner gate:** OD-04.

### IMP-19 Writers for the base tables that have none
- **Change:** CODE, only for tables a ruled task must write: `lang_jur_map` (add pair, set scope) and `base_taxonomy_identity` (IMP-20). The jurisdiction table's writer ships with IMP-17. The capture derivation includes them. Each verb lands with the task that reads it (IMP-18, IMP-20), not before.
- **TD:** REQ-090 ("never hand-edit"), REQ-097. **BU:** BU §A.1, Q11.
- **Reads it:** `emit_batch_sql.py`. **Wrong thing:** base changes arrive as hand SQL that bypasses every refusal (CLAUDE.md §4).
- **Files:** `scripts/db.py`, `scripts/dbcore.py:1075`. **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-28. **Risk:** each verb needs the refusals that are its value. **Owner gate:** none.

### IMP-20 Execute the mobility split
- **What is ruled (not asked again):** the codes are `AMB` and `WHEEL`, and `MOB` is superseded (PS:1291-1296, "Settles the two questions the split design … put to the owner"). The ruling fanned the item-link rows out to both codes mechanically, as "a mechanical carry of the umbrella's union, not a judgement", each row "pending synthesis re-derivation", and said a grade of a study's participants is never fanned out (PS:1302-1311).
- **Change:** data, after the registry writer exists. Add the two codes. Carry the rows written under `MOB` since the ruling: `select count(*) from source_value_extractions where identity_code='MOB'` figures, of which `… join evidence_sources e using(ref_id) where x.identity_code='MOB' and e.tier>=4` come from T4–T6 instruments, which have no participants to judge by. How those rows are carried is the one execution question (OD-14). All eight stored determinations are already retired (`select count(*), sum(retired_at is not null) from specifications`); nothing needs retiring.
- **TD:** HS-A01. **BU:** HS-2 F-02.
- **Reads it:** every lens-keyed table. **Wrong thing:** one ramp gradient for two groups the owner split because their needs oppose.
- **Deps:** IMP-19 (identity writer), IMP-40 (how a figure carries two codes of one model). **Layer:** 3. **Kind:** RESEARCH, Opus-class or above. **AT:** AT-62. **Owner gate:** OD-14 (narrowed).

### IMP-21 A concept that is not an English string
- **Change:** blocked on OD-03. The smallest shape that meets REQ-055, REQ-056 and REQ-060 together: the term keeps an id; every name is a form row (language, jurisdiction, kind of attestation, locator); the term points at its display form; `canonical_en` becomes a tombstone.
- **TD:** REQ-055, REQ-056, REQ-057, REQ-061, C-04. **BU:** BU §A.1, §D.3.
- **Reads it:** every writer that screens or matches a name; render labels. **Wrong thing:** a concept that exists only in Japanese or French is named by a model's English gloss and searched for by it.
- **Deps:** IMP-22. **Layer:** 1. **Kind:** TOOLING, then RESEARCH. **AT:** AT-25. **Owner gate:** OD-03.

### IMP-22 Forms that say how they are attested, and searches that say what they used
- **Change:** CODE (schema). `term_aliases` gains a typed attestation (found in an instrument, owner-supplied, model seed, unrecorded) and locator columns (URL, page, line); the `notes` markers are migrated mechanically. `search_executions.terms_used` (JSON) becomes a junction to the forms used, so "this search ran on a model seed" is a join.
- **TD:** REQ-058, REQ-059, REQ-060, HS-A14, B13. **BU:** Q33; BU §D.6 (alias table and adjudications disagree).
- **Reads it:** `_near_terms`, `alias_provenance_audit`, `multilingual-research`, `coverage`. **Wrong thing:** a zero-result search on an invented word is recorded as an absent literature (PS:624).
- **Deps:** OD-03 for names; the columns do not wait. **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-23, AT-24, AT-26. **Owner gate:** none.

### IMP-23 Guards that work in every script the scope names
- **Change:** CODE, small and general, no per-language word lists (rule 8). `normalise_quote` drops marks only where they are not lexical and folds every decimal digit; `_name_tokens` tokenises on Unicode word characters with case folding; the value screen rejects any digit or comparator in any script and leaves words to the owner's approval of each name (PS:4398).
- **TD:** REQ-034, REQ-055, REQ-023. **BU:** BU problem 8; HS-2 F-10.
- **Reads it:** `add-extraction`, `observe-term`, `add-term`, `add-parameter`. **Wrong thing:** a misquoted clause verifies; a name stating its answer becomes a container.
- **Files:** `scripts/research/retrieval_log.py:605-644`, `scripts/db.py:6407-6441`, `8559-8622`. **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-59, AT-60. **Risk:** existing verified quotes must still verify; re-run `observation_verbatim_audit`. **Owner gate:** none.

### IMP-24 Language codes with one spelling at the writers and in the views (the prior workplan's T-6a, extended)
- **Change:** REUSE. T-6a ("needs nothing") folds and shape-checks the language at `log-search` and folds with `UPPER()` in the coverage views, with no UPDATE of history. Its done-when is unmet: `SELECT COUNT(DISTINCT language) FROM v_coverage_language` and `SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL` differ today. This entry adds only that the same refusal is applied at `observe-term`, `add-alias` and `add-source`.
- **Corrected (FA-19).** The first version said the "retired `lang_detected` copies are written forward to `language`". `lang_detected` is the live column (`add-source` writes it, `scripts/db.py:3387-3388`); `language` is the one never written. The workplan declines backfilling `evidence_sources.language` (K-9) and any UPDATE of `search_executions` (K-10). This entry does not reverse either; stored history keeps its spellings and readers fold.
- **TD:** REQ-071, REQ-092. **BU:** BU §D.2; Q34.
- **Reads it:** the coverage views, `get_unmined_for_all_slugs`. **Wrong thing:** English sources sorted as non-English and the reverse.
- **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-74. **Owner gate:** none; script and regional variants are OD-04.

### IMP-25 The source's own identity and edition
- **Change:** REUSE of columns that exist and are never written: `original_title`, `edition`, `code_currency_*` (not `language`: see IMP-24; a backfill of it is declined by the workplan, K-9); one verb field each; `v_evidence_authors` shows a full given name where the script has no initials.
- **TD:** REQ-067, REQ-071, HS-A11. **BU:** BU §D.6, §G.4.
- **Reads it:** render's evidence list; `jurisdiction-tracker`. **Wrong thing:** a superseded edition cited as current; an author rendered as one character.
- **Deps:** OD-02 (whether translated titles are shown). **Layer:** 2. **Kind:** TOOLING, then RESEARCH backfill. **AT:** AT-03, AT-61. **Owner gate:** none for the columns.

### Wave 4 — read once, unify, find (REQ-098, REQ-099, REQ-100)

### IMP-26 The clause as a unit of evidence
- **Change:** CODE (schema), the smallest table: one row per clause read (source, typed locator, verbatim text in the source's language, the file hash). Extractions, observations and relations point at it; `claim_text` and the `loc_*` columns on judgment rows become tombstones.
- **TD:** REQ-097 ("clauses in order to group"), REQ-013, REQ-098. **BU:** HS-1 §5.1 (a clause is repeated per parameter and nothing can point at one).
- **Reads it:** `add-extraction` (pointer instead of copied text), the verbatim check, IMP-28's sweep, IMP-34's candidates, render's "what the source says, where". **Wrong thing:** the same clause quoted three ways in three rows; no way to say two jurisdictions' clauses are the same provision.
- **Deps:** OD-23 (how much text is held, and whether held clause text may be shown). **Layer:** 1. **Kind:** TOOLING. **AT:** AT-66. **Risk:** largest schema change in the programme; the judgment hand-off stays 1:N on the source. **Owner gate:** OD-23.

### IMP-27 A reading that is a full read, with its open pass
- **Change:** CONVENTION and REUSE. `record-scan` already has `method` and `open_pass_done`; the pipeline skill makes a full read with the open pass the only reading that discharges a source, and the open pass writes clause rows (IMP-26) for every quantitative or normative clause, catalogue or not.
- **TD:** REQ-098, REQ-027, REQ-079. **BU:** HS-1 §5.2 (no `full-read` scan; no open pass).
- **Reads it:** `v_scan_ledger`, `scan_debt`, `verified_scan_integrity`. **Wrong thing:** a value in a held source is never found; the book states a gap that the library fills.
- **Deps:** IMP-26. **Layer:** 2–3. **Kind:** TOOLING (skill, check), then RESEARCH (the reading itself, the largest standing debt). **AT:** AT-64. **Owner gate:** none.

### IMP-28 Catalogue growth without re-retrieval
- **Change:** blocked on OD-23. Whichever option is chosen, the ledger rule changes from "a scan covers parameter ids up to its version" to "a scan covers the parameter set recorded with it, and a later parameter is matched against the clause inventory", with the owed sweep listed by one query.
- **TD:** REQ-098 (PS:5239 ACTION 2). **BU:** HS-1 §5.2.
- **Reads it:** `v_scan_ledger`. **Wrong thing:** each new parameter silently re-opens the whole library, or is assumed covered.
- **Deps:** IMP-26, IMP-27. **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-65. **Owner gate:** OD-23.

### IMP-29 Pointers between terms
- **Change:** CODE (schema), one table: term → term with a typed kind (broader, part of, element has parameter, adjacent, equivalent). Replaces `NARROWER`/`BROADER` alias strings and the prose in `scope_note`.
- **TD:** REQ-099 (family), REQ-045 ("typed term pointer"), REQ-097 (linkages), HS-A14. **BU:** `base_parameters` is flat; no relation table (HS-1 §5.3).
- **Reads it:** render's element page (ramp → gradient, run length), the synthesis candidates (IMP-34), the scan inheritance rule. **Wrong thing:** parameters that belong together cannot be shown or unified together.
- **Deps:** OD-24 for how it is used to set grain. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-46, AT-67. **Owner gate:** none for the table; OD-24 for the policy.

### IMP-30 What a parameter measures, as data
- **Change:** CODE that deletes code. A parameter states its quantity kind; units and their exact conversions are rows; the engine's `NOTATION_FAMILIES` list is replaced by a read. Length conversion (ruled, OR-10) follows.
- **TD:** REQ-068, REQ-093, REQ-099 (comparable dimension). **BU:** BU problem 5.
- **Reads it:** the engine's composer; `add-extraction` (refuses a unit of another kind). **Wrong thing:** a parameter with evidence in three units has no value.
- **Deps:** OD-22 (rounding direction, OR-10b). **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-30, AT-68. **Owner gate:** OD-22 for rounding.

### IMP-31 Conditions out of the unit cell
- **Change:** REUSE (`condition_on` edges and `amend-extraction`'s reformat-in-place, OR-3), as a data repair. Each condition now written inside `claimed_unit` becomes a condition row or edge.
- **TD:** REQ-092, REQ-099. **BU:** Q23; 24 of 35 governing claims unparsed.
- **Reads it:** the engine; render's "applies when" lines. **Wrong thing:** most of the evidence is left out of the value, silently.
- **Deps:** IMP-30. **Layer:** 3. **Kind:** RESEARCH. **AT:** AT-69. **Owner gate:** none.

### IMP-32 Relations synthesis can record
- **Change:** CODE (schema, on a table with 0 rows). `connections.connection_type` gains equivalence, adjacency and similarity; `filed_in` stops being a required slug; targets may be a clause or a term.
- **TD:** REQ-100, REQ-043, REQ-097. **BU:** HS-1 §5.4.
- **Reads it:** IMP-34, the engine (IMP-33), render's discussion. **Wrong thing:** a discussion that cannot say two provisions are the same, or that one constrains another.
- **Deps:** IMP-26, IMP-29; OD-25. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-70. **Owner gate:** OD-25 for the vocabulary.

### IMP-33 What a synthesis is, and whether the engine reads it
- **Change:** blocked on OD-07 and OD-19.
- **TD:** C-12, REQ-010, HS-A10. **BU:** BU problem 9. **Owner gate:** OD-07, OD-19.

### IMP-34 Candidates on demand
- **Change:** CODE, read-only: one query verb that, for a parameter or a term, lists candidate relations from rows already held (figures equal on a common scale across jurisdictions; parameters stated in the same clause or section; terms sharing forms; parameters sharing a parent). It proposes; an Opus-class or above session judges and records (IMP-32). Nothing is written by the finder.
- **TD:** REQ-100 ("very dynamic in finding"), REQ-093 (derive, then name who judged). **BU:** no finder exists (HS-1 §5.4).
- **Reads it:** `/run-pipeline` synthesis step; `connection-discovery`. **Wrong thing:** relations depend on what a session happened to notice.
- **Deps:** IMP-29 and IMP-30 for candidates drawn from figures and terms; candidates drawn from clauses wait on IMP-26 and so on OD-23. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-71. **Owner gate:** none for the first kind; OD-23 through IMP-26 for the second.

### IMP-35 One read-only answer for a cell at every stage
- **Change:** CODE, read-only: a `db.py` query verb that, for a parameter and optional lens, jurisdiction and language, reports per stage what is held, what was examined and found empty, what was never examined, and what is owed, each with its row ids.
- **TD:** REQ-001, REQ-021, C-13, TD §3.9 (the part that needs no new object). **BU:** BU §C.1 (a cell can be run; nothing says where it stands).
- **Reads it:** `/run-pipeline` at entry at any stage; the owner. **Wrong thing:** a run started mid-pipeline repeats or skips work because nothing states the cell's standing.
- **Deps:** IMP-12. Until IMP-18 lands (OD-04) the verb reports the scope of a pair as unrecorded. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-07, AT-23. **Owner gate:** none; a stored request record is OD-09.

### IMP-36 Skills that describe the database that exists
- **Change:** DELETE and edit. `multilingual-research`, `cross-population-conflict-mapper`, `gap-driven-mining` and the other files failing `skill_vocabulary_audit` are corrected or retired; `connection-discovery` gains the relation kinds of IMP-32.
- **TD:** REQ-053, REQ-100. **BU:** HS-2 F-18.
- **Reads it:** every research session. **Wrong thing:** research run to a procedure that names tables and codes that are gone.
- **Deps:** none for correcting tokens that name nothing; the relation kinds in `connection-discovery` wait on IMP-32 (OD-25). **Layer:** 2. **Kind:** TOOLING. **AT:** `skill_vocabulary_audit` exits 0. **Owner gate:** none for the corrections.

### Wave 5 — jurisdiction downstream, and render

### IMP-37 The jurisdiction comparison as a view
- **Change:** CODE, one cross-stage view over judgment rows (parameter, lens, jurisdiction, figure, source). No new table; the key of a determination is unchanged.
- **TD:** REQ-069, C-03 as read. **BU:** BU §B.3 (no typed comparison).
- **Reads it:** render E2. **Deps:** IMP-17, IMP-18. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-31. **Owner gate:** OD-01 if a determination is to vary by jurisdiction.

### IMP-38 Render
- **Change:** blocked on OD-02, OD-08, OD-12. Then REUSE of `RENDER-CONTRACT-parameters-3-and-12.md` (elements, rules, invariants) and of the gate split recorded at PS:588.
- **TD:** REQ-083 to REQ-089, HS-A09. **BU:** BU §E. **AT:** AT-35 to AT-39. **Owner gate:** OD-02, OD-08, OD-12.

### IMP-39 The owner's edits
- **Change:** blocked on OD-20 (the ledger's reading at PS:4586: proposals through the write path, no second path).
- **TD:** REQ-009. **BU:** browser is read-only. **AT:** AT-20, AT-42. **Owner gate:** OD-20.

### IMP-40 The link table for several codes of one model
- **Change:** CODE (schema), ruled and unbuilt. Owner: "link table unless that is more prone to errors" (PS:4926); ACTION (1) "Carry several codes of one model on a figure by a link table; do not write the figure once per combination" (PS:4941). The ledger gives "the shape of the table, and what happens to the four lens columns" to "the tooling PR" (PS:4934) and says T-3 and D-2 "can be designed, as a tooling pull request first" (PS:4938), which puts tooling before data. It does not say a link-table pull request precedes T-3, and the workplan's condition on T-3 ("settled by OR-1c before this PR opens") is met by the owner's answer. **Placing this entry before T-3, or inside it, is this leg's sequencing, not a citation.** The first version of this programme marked the requirement UNMET (HS-1 REQ-076) and carried no improvement for it (FA-05).
- **TD:** REQ-076, REQ-073. **BU:** one column per model on figures and determinations.
- **Reads it:** the engine's gather (IMP-08), `add-extraction`, D-2, IMP-20, render's lens controls. **Wrong thing:** a figure about two ICF codes is written twice or carries only one.
- **Files:** a schema migration; `db.py add-extraction`, `amend-extraction`. **Deps:** none stated by the ledger or the workplan; this leg proposes it land with or just before T-3 so the gather is written once against the final shape. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-32. **Risk:** the owner's condition ("unless that is more prone to errors") was met by a measurement the ledger marks as the assistant's. **Owner gate:** none (ruled).

### Research tasks the tooling unlocks (each its own pull request)
- **R-1** Fill the medical lens by correspondence (HS-A03; `add-medical` exists). Owner gate: OD-15.
- **R-2** Read what is held, in full, with the open pass (IMP-27).
- **R-3** Re-tag figures with every relevant model (REQ-073; the workplan's D-2), after IMP-08 and IMP-40.
- **R-4** Attest forms per language and jurisdiction pair from instruments (REQ-058, REQ-060), after IMP-22.
- **R-6** Verify the governing sources that are not `VERIFIED`. For parameter 3 they are listed by `select e.ref_id from specification_source_links j join evidence_sources e using(ref_id) where j.role='governing' and coalesce(e.verification_status,'')<>'VERIFIED'` on a scratch copy holding the determination. Until they are verified, C10 refuses the cell, as the ledger intends (PS:4544).
- **R-5** First live determinations, only after IMP-08 and IMP-40 (lens), IMP-20 (mobility codes), and R-6 for the cell's sources, and with the blocking battery green on the scratch copy, `test_db_integrity` included.

---

## 2. Owner decision register (summary; the Sonnet suite writes the full register)

Each is `OWNER DECISION REQUIRED`. Options and a recommendation are offered; nothing is decided here.

### OD-01 Does a determination vary by jurisdiction, and what is a jurisdiction below the country?
Options: (a) one determination per parameter × lens, jurisdictions shown as a spread (TD's reading); (b) a determination per jurisdiction; (c) (a) plus typed conditions for climate and cultural context (HS-A12). Sub-national: codes with a parent, or stay at country. **Recommendation:** (c), with sub-national rows; `REF-01013` shows the need.

### OD-02 What language is a page in, and may a source's sentence be translated?
Options: (i) English pages citing each source in its own language; (ii) pages in several languages. **Recommendation:** (i) for this edition, quotes shown in the original with a marked translation only where the owner permits one.

### OD-03 How is a concept held without an English name?
Options: (a) forms table with a display pointer (IMP-21); (b) keep `canonical_en`, add a label kind; (c) nothing until a non-English-origin concept is minted. **Recommendation:** (a); (c) is defensible today (no such term exists, Q39) and defers the cost to the first such concept.

### OD-04 What the scope answer of 2026-10-30 covers
**On the record (the later statement governs):** "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now" (PS:4835), restated at PS:5026 with the set marked as an assumption. The earlier standing order names buckets 1–2 (PS:4295-4313); the two sets differ by `UN` on one side and `BE, CH, CN, DK, IT` on the other; doctrine names 24 jurisdictions with a Global South floor. **Open:** whether the 2026-10-30 answer, given about the specification page, also sets the research scope and the base's languages; whether `UN` stays; whether the set recorded at PS:5026 is the set meant; whether script and regional variants (Chinese scripts; Bokmål and Nynorsk, E7) are separate pairs. **Recommendation:** confirm the PS:5026 set as the one scope for research, base and page, and rule on `UN`.

### OD-05 Evidence from outside the scope that citation mining surfaces
Options: admit, stage as a lead, refuse. **Recommendation:** stage as a lead with its origin, admit only T1–T3 on the owner's word (JP:62 says such evidence is cited).

### OD-06 Which stage assigns the lenses
Confirm that "evidence stage" in the 2026-11-06 list means evidence and judgment together (PS:4999). **Recommendation:** confirm; judgment assigns.

### OD-07 What is one synthesis row, and must a determination point at it?
Options: (a) synthesis stays a step inside the engine and its narrative tables are deleted; (b) synthesis becomes a separable stage with its own rows that a determination points at. **Recommendation:** (b) for relations (REQ-100 requires findings that outlive a run), with convergence left in the engine.

### OD-08 What an absent cell means
Not relevant, not yet researched, researched and empty. **Recommendation:** store none of them as determination rows; derive the three from searches, readings and gaps (IMP-09, IMP-35).

### OD-09 What "dynamically" may do unattended, and whether a request is recorded
**Recommendation:** on-demand orchestration with judgment acts made and warranted by the model; no request table (the cause rows are the record).

### OD-10 `provisional`: strength of evidence, or a re-read owed
**Recommendation:** keep the state for strength; record the owed re-read as a follow-up (IMP-13).

### OD-11 Which stage owns the gap register
**Recommendation:** a cross-stage register written by the stage that finds the gap, named so in the stage map.

### OD-12 How render's prose is produced and whether it is stored (OW-1b, OW-1c)
**Recommendation:** fixed templates from typed rows; rebuilt, not stored, until a measured cost says otherwise (this also resolves TD's AT-04 against REQ-084).

### OD-13 The "≥9 languages" rule of March 2026
**Recommendation:** mark superseded by the pair-based rulings.

### OD-14 Carrying the rows written under `MOB` since the split was ratified
**Not asked:** the codes and the fate of `MOB` are ratified (PS:1291-1296). **Open, two things.** (1) How figures and grades written under `MOB` after 2026-08-25 are carried. Options: (a) fan each out to both codes, flagged as awaiting re-derivation, as the ruling did for the link rows; (b) judge each row, a study's rows by its participants and a code's rows only where its text names the users (the workplan's D-2 rule), leaving the rest untagged for identity; (c) (a) for T4–T6 provisions and (b) for studies. A grade of a study's own participants is never fanned out (PS:1309-1311). (2) How part-time wheelchair users and balance are named in a gap, which the ruling leaves owed (PS:1189-1192). **Recommendation:** (c).

### OD-15 Filling the medical lens
Confirm the corrected ruling (by correspondence, roughly the size of the registries held) and the WHO licence position (E5). **Recommendation:** proceed, English anchors only until the licence is read.

### OD-16 WITHDRAWN — does a change in engine behaviour bump the rule version?
Answered on the record, and the first version cited the item the answer replaced (FA-07). "`RULE_VERSION` is `pilot-4`. This answers the 'Owner to decide' in the first correction above and replaces its item 4" (PS:4546); the prior workplan derives a bump for each of T-1b, T-2, T-3 and T-4 (WR-2). Nothing is asked.

### OD-17 Ratify the corrected pipeline contract
**Recommendation:** after IMP-03.

### OD-18 What "all directions" covers
Confirm the cold-entry and re-entry conditions for judgment, synthesis, specification and render (TD §3 is inference), and whether an earlier stage's row may be updated to record later use (REQ-012 against live writers). The forward entry strings that IMP-03a corrects follow the owner's stated order (PS:1454) and are not part of this question. **Recommendation:** allow status updates on earlier rows; forbid copying later facts into them.

### OD-19 Conflict between groups in the engine
Harm asymmetry and broadest benefit are canonical doctrine the engine does not apply. **Recommendation:** record conflicts and the rule applied as rows; the engine reads them only after the owner approves the rule's mechanical form.

### OD-20 The owner's edits
Confirm the ledger's reading: proposals applied through the write path (PS:4586).

### OD-21 Are a reader's or the owner's questions about a published cell recorded in the database?
**Recommendation:** yes, as an open gate that flags the cell (IMP-14).

### OD-22 Rounding direction for converted lengths (OR-10b), and the other open prompts
List them from the file's `decisions` list: `python3 -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['decisions'] if 'answered' not in q])"`, then cross-check each against the ledger (IMP-06; OR-1c is answered at PS:4922 and unmarked in the file).

### OD-23 How a parameter defined later reaches a source already read
Options: (a) **re-read**: keep only what was extracted; each new parameter owes a targeted reading of every source; simplest, costliest, and needs the bytes again (how many live sources hold an artefact, and of what kind, is derived in HS-2 §2.7; a derived text-extraction record and a retrieved text-like file are not the same thing, and which artefacts are a source's full text is not established); (b) **retained text**: keep each source's text layer and page images, addressed by hash, in the repository where size allows and by location otherwise (PS:5110-5112: retrieved standards may be held; PS:5126: large files are logged by location); a new parameter is swept over held text, re-retrieval only where nothing is held; (c) **clause inventory**: the open pass records every normative or quantitative clause as a row; a new parameter is matched against rows; text is held only for those clauses. Trade-offs: holding retrieved copies is already ruled acceptable (PS:5110-5112); (c) puts clause text into a database that the site is to read, and showing that text publicly is a further act the owner has not ruled on (licensing); (c) is queryable and lets equivalence groups point at clauses (REQ-097), and misses whatever the open pass did not judge to be a clause; (a) misses nothing in principle and never ends. **Recommendation:** (c) with (b) as its backing, and a recorded re-read where neither is possible.

### OD-24 How coarse a parameter is
Options: (a) flat and coarse: one parameter per measured quantity of an element, every clause variation a typed condition on its figures; (b) hierarchy: a parent parameter with children for materially different cases; (c) flat and fine with equivalence groups above. The trap: too fine cannot unify; too coarse hides the divergence the book exists to show. **Recommendation:** (a) with the term pointers of IMP-29 for families, and a written test for a split (two cases become two parameters only when they cannot be placed on one scale, or their directions differ). Whether that test is doctrine or convention is the owner's.

### OD-25 Which relations synthesis records, and who may judge them
The owner's four words map to three kinds (equivalence, adjacency, similarity or commonality) plus the two that exist (conflict, convergence). **Recommendation:** those five; found by query, judged at the synthesis capability floor (Opus-class or above), each recorded as pointers with its warrant.

### OD-26 An interim stage-pair gate before render exists
The ruled gate fails on any pair with no path and is red today for the five pairs ending at render (IMP-07). Options: (a) wait, and run the instrument as a command at the end of each phase until a render view exists (the ledger's own note at PS:4761 and the workplan's §8 item 7); (b) register an interim check that fails only when a path that exists is lost, which needs a stored baseline of today's paths, a curated list of the kind rule 8 forbids. **Recommendation:** (a).

---

## 3. Sequencing

_Amended (FA-04, FA-18). T-n and D-n are tasks of `workplan/2026-10-23-pipeline-resolution-workplan.md`; they are cited, not restated._

**Doable now: no owner word, no unmet dependency, nothing red on `main`.**

| Item | Why it is free | Carries |
|---|---|---|
| IMP-06 | derives a field from the ledger | none |
| IMP-02 | marks and corrected header text | run `claude_md_spine` and `research_contract_sync` after |
| IMP-03a | contract entry text only; no key, no id | `pipeline_contract_audit` after |
| IMP-04 | report-only; the `EXAMINED:` token and the registry are untouched | none |
| T-1a | workplan: "Needs nothing"; done-when unmet | first link of the chain to the lens fix |
| T-6a (= IMP-24) | workplan: "Needs nothing"; done-when unmet | no UPDATE of history |
| IMP-23 | script-aware guards; no list, no gate | coordinate with T-1a's numeral gloss; re-run `observation_verbatim_audit` |
| IMP-12 | typed columns on `gaps`, `gap_id` on a search | existing gaps (`select count(*) from gaps`) are not back-filled by migration |
| IMP-13 (two values) | the skimmed-figure and absence-finding reasons | the provisional and reader-question values wait on OD-10, OD-21 |
| IMP-43 | `add-source` requires a verification standing and a source type | existing callers and skills that omit them (rule 4 sweep) |
| IMP-44 | the claimed-number check compares numbers | coordinate with T-1a (the writer's refusals) and IMP-23; re-verify stored figures by report, not by rewrite |
| IMP-45 | `delete-connection` refuses an id that is not a row | none |

**Needs one owner reply:** IMP-01 (the O1–O8 wording).

**The chain to the lens fix (tooling, in this order):** T-1a → T-2 → IMP-40 (link table) → IMP-08 with IMP-09 and IMP-10 (= T-3) → then D-2 / R-3 (data).

| Wave | Contents | Kind | Waits on |
|---|---|---|---|
| **0** | IMP-02, 03a, 04, 06; IMP-01 after the owner's reply | TOOLING | IMP-01: one reply |
| **1** | T-1a, T-6a/IMP-24, IMP-23, IMP-43, IMP-44, IMP-45; IMP-42 with the quantity-kind column of IMP-30, before any further parameter is minted; then T-2, IMP-40, IMP-08/09/10 | TOOLING | the chain above; IMP-09's stored-row question on OD-08; IMP-42's policy on OD-24 |
| **2** | IMP-12, IMP-13; IMP-14 and IMP-03b | TOOLING | IMP-14: OD-21; IMP-03b: OD-18 and IMP-12 to 14; two IMP-13 values: OD-10, OD-21 |
| **3** | IMP-17, IMP-22, IMP-25 (tooling); IMP-19 with its readers; then IMP-18, IMP-20, R-1, R-4 (data) | both, tooling first | IMP-18: OD-04; IMP-20: OD-14, IMP-40; R-1: OD-15; IMP-21: OD-03; IMP-25's shown titles: OD-02 |
| **4** | IMP-29, IMP-30 (tables); IMP-34 (figure and term candidates), IMP-35, IMP-36 (token corrections) | TOOLING | IMP-30's rounding: OD-22; IMP-34 needs IMP-29, IMP-30; IMP-35 needs IMP-12 |
| **4, gated** | IMP-26, 27, 28; IMP-32, 33; clause candidates of IMP-34; relation kinds in IMP-36; then IMP-31, R-2 (data) | both | OD-23 (IMP-26 to 28); OD-07, OD-19, OD-25 (IMP-32, 33); OD-24 for how IMP-29 sets grain |
| **5** | IMP-37; IMP-38, IMP-39; IMP-07 once a render view exists | TOOLING | OD-01, OD-02, OD-08, OD-12, OD-20; OD-26 if an interim gate is wanted |
| last | R-6, then R-5 | RESEARCH | IMP-08, IMP-40, IMP-20; C10 green for the cell |

Withdrawn: IMP-11 (its subject returns, corrected, as IMP-41), IMP-16, OD-16. IMP-05 deletes nothing until a caller sweep has run.

**Order rules.** Tooling before the rows that use it (rule 10). One pull request merges at a time (workplan WR-1). A schema change runs `joined_cells_census.py` before and after (CLAUDE.md §4) and `run_checks.py --selftest` after any rename. The gate is run once, when the diff is ready (CLAUDE.md §1). Nothing is added without the reader named in its entry existing or landing with it. The order T-1a → T-2 → T-3 is taken from the workplan (§5, §7); this leg did not test independently that it is forced.

---

## 4. New acceptance tests (each red on today's `main`, or stated otherwise)

TD's AT-01 to AT-49 stand, with AT-04 made conditional on OD-12. Red today was observed by this leg unless marked. Amended after the antagonist pass: AT-50, AT-51, AT-52, AT-54, AT-55, AT-65, AT-69, AT-74 restated; AT-56 withdrawn (§6).

| ID | For | Test | Red today because |
|---|---|---|---|
| AT-50 | IMP-08 | On a scratch copy, every figure linked (any role) to the determination for parameter 3 × `MOB` carries the lens `MOB`, and the linked set is not empty. A fixture with two lens tags on one parameter asserts the same (IMP-10). | 122 linked figures, 6 of them not tagged `MOB` (`select l.role, x.identity_code, count(*) from specification_extraction_links l join source_value_extractions x using(extraction_id) … group by 1,2`). The first version tested parameter 3 × `DEAF`, which has no tagged figure and would pass having examined nothing after the fix (FA-17). |
| AT-51 | IMP-08 | On a scratch copy, every figure linked to parameter 9 × `ALL` carries `ALL`, the set is not empty, and no `ALL`-tagged figure is linked to parameter 9 × `MOB`. | parameter 9 × `ALL`: 12 `ALL` figures and 4 `MOB` figures linked. (Parameter 3 holds no `ALL` figure.) |
| AT-52 | IMP-09 | A cell whose lens no figure of the parameter carries yields no determination row (parameter 3 × `DEAF`). | a `provisional` row is stored. Rests on the ledger's unratified assumption for the general rule (PS:4630); the relevant-lens case is OD-08. |
| AT-53 | IMP-07 | The registry holds the stage-pair gate, and it exits non-zero while any stage pair prints `NO PATH` in either zigzag section of the instrument (the workplan's §8 items 6–7; the ruling at PS:4761). | no registry entry names the instrument (YAML load in HS-1 REQ-006); the instrument exits 0 over ten `NO PATH` lines. It cannot be green until the render pairs have a path (IMP-07), so it is red by construction if registered today. |
| AT-54 | IMP-04 | Each of the four checks prints how many of the determinations it read are live and how many retired, and on `main` the live figure is 0; the `EXAMINED:` line and the registry floors are unchanged, and `run_checks.py --battery schema` gives the same verdict before and after. | no such line; `validate_evidence_state` prints "8 cells", `validate_verification_consistency` "5 stated/provisional specification(s)" |
| AT-55 | IMP-10 | Two seeded defects each turn a named test red: a determination whose linked figures carry another lens; a retired determination surfaced by a determination view. | neither fixture exists (`grep -rn "v_best_practice\|v_pending" scripts/tests` returns a fixture stub only); the other four seeded defects are already caught (`python3 scripts/tests/test_validate_evidence_state_2_4.py`; `test_evidence_cell_state_2_3.py:221`; `test_assess_cell_pilot.py:843-858`) |
| AT-56 | — | WITHDRAWN (FA-09). Four cells on one scratch copy take distinct ids and capture as one delta; that is green today. Replay of two separate copies was not tested. | — |
| AT-57 | IMP-18 | Every `lang_jur_map` row has a scope, and `v_research_scope` returns no scoped-out pair. | scope NULL on every row; view returns all |
| AT-58 | IMP-17 | Every jurisdiction in `lang_jur_map` resolves in the vocabulary the writers read. | 17 do not |
| AT-59 | IMP-23 | Two sentences that differ only in vowel signs or voicing marks do not normalise to the same string. | Devanagari and kana pairs collide |
| AT-60 | IMP-23 | A name containing a digit in any script is refused; a non-Latin name yields a non-empty token set. | `幅１２００` passes; `勾配` yields none |
| AT-61 | IMP-17, 25 | No source issued by a sub-national body carries a bare country code. | `REF-01013` |
| AT-62 | IMP-20 | The identity registry holds the split codes, and no live figure carries a superseded one. | `MOB` on 170 rows; no `AMB`, `WHEEL` |
| AT-63 | R-1 | The medical registry and its two crossing maps are non-empty. | 0 rows each |
| AT-64 | IMP-27 | Every live source has a full-scope `full-read` scan with its open pass done, or a typed blocked reason. | no `full-read` scan; no open pass |
| AT-65 | IMP-28 | After a parameter is added on a scratch copy, the owed sources are listed by one query and each has held text or clause rows, or a recorded re-read. | the list exists; what a later sweep could read is not established: of the live sources, the HS-2 §2.7 command counts those with a derived `text-extraction` or `extraction` record and those with any artefact on disk, and some hold none |
| AT-66 | IMP-26 | A clause stating two parameters is stored once and pointed at by both figures. | no clause table |
| AT-67 | IMP-29 | For an element term, one query returns its parameters through a typed pointer. | no pointer table |
| AT-68 | IMP-30, 31 | For each parameter, every governing claim is placed on the parameter's scale or carries a typed reason. | 11 of 35 for parameter 3 (BU); none for parameter 12 |
| AT-69 | IMP-31 | No `claimed_unit` holds a condition: `select count(*) from source_value_extractions where length(claimed_unit)>20 or claimed_unit like '%(%' or claimed_unit like '% where %'` returns 0, read with a sample of what it matches. | the query returns rows today. `joined_cells_census.py` is not a sufficient instrument for this: it flags far fewer `claimed_unit` cells (FA-29). |
| AT-70 | IMP-32 | Each relation kind has a vocabulary value and at least one row with a pointer at each end, and something reads it. | 0 rows; no such values |
| AT-71 | IMP-34 | For a parameter, one read-only command returns candidate relations with the rows that suggest them. | no such command |
| AT-72 | IMP-13, 14 | A question on a figure and on a cell can be raised, flags the cell, and can be resolved. | no carrier |
| AT-73 | IMP-12 | Every gap the engine writes carries its parameter and lens; a search can name the gap that caused it. | no such columns |
| AT-74 | IMP-24 | T-6a's done-when: `SELECT COUNT(DISTINCT language) FROM v_coverage_language` equals `SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL`; and `observe-term`, `add-alias`, `add-source` refuse a language the map does not hold. Stored history is not rewritten. | the two counts differ; the three writers do not refuse |
| AT-75 | IMP-06 | Every prompt the ledger answers is marked answered. | OR-1c |
| AT-76 | — (was IMP-16, withdrawn) | Every live determination carries the current rule version and recomputes to its stored answer. | not red: 0 live rows; it is UNPROVEN until one exists |

---

## 5. What this programme declines

- A `requests` table, a "return" marker, per-language word lists for name screening, a per-stage service interface, id allocation at replay (IMP-11), a further staleness guard (IMP-16), a back-fill of `evidence_sources.language` or an UPDATE of `search_executions` (the workplan's K-9, K-10). Each is apparatus; the entries above say what replaces it or why nothing does.
- Any change to tiers, markers, the lens set, the scope or the mission.
- Restating `workplan/2026-10-23-pipeline-resolution-workplan.md` (T-1 to T-7) or the draft render contract. Where an improvement is a task there (IMP-08, IMP-09 and IMP-10 are T-3; IMP-24 is T-6a; R-3 is D-2) the entry says so and carries that plan's dependencies. Where one overlaps (IMP-30 with T-1 step 9; IMP-37 and IMP-38 with T-5 and T-7; IMP-18 with T-6b; IMP-07 with §8 items 6–7), the suite cites the task and says what changed.

---

## 6. Resolution record (antagonist pass of 2026-11-12)

The complete record, one row per objection with this leg's re-run evidence, is in `hs-adversarial-findings.md` §5. The rows below are the objections that touch this file. Disposition vocabulary: **upheld** (the objection failed), **amended**, **withdrawn**, **referred to owner**.

| FA id | What it touched here | Disposition |
|---|---|---|
| FA-01 | IMP-04, AT-54, §0 | **amended**: report-only form; token and floors untouched |
| FA-02 | §0, IMP-04 "wrong thing", R-5 | **amended**: C10 named; R-6 added; R-5 preconditions restated |
| FA-03 | IMP-05 | **withdrawn**: the four skill files have readers |
| FA-04 | §0, §3 | **amended**: the doable-now list rebuilt from each entry's own gate and dependencies |
| FA-05 | IMP-08; no entry for the link table | **amended**: IMP-08 carries the T-1a → T-2 → T-3 chain; IMP-40 added |
| FA-06 | IMP-16 | **withdrawn** |
| FA-07 | OD-16, IMP-08 | **withdrawn** |
| FA-08 | IMP-10, AT-55 | **amended**: one fixture, not six |
| FA-09 | IMP-11, AT-56 | **withdrawn** |
| FA-10 | IMP-08 "wrong thing" | **amended**: "code provisions tagged `MOB`" |
| FA-11 | OD-23, AT-65 | **amended**: the "text layer" figure removed |
| FA-12 | IMP-07, AT-53 | **amended**, and the interim form **referred to owner** (OD-26) |
| FA-13 | IMP-09, AT-52 | **amended**: parameter 7 example removed; assumption named |
| FA-14 | OD-14, IMP-20 | **amended**: the ratified codes are not re-asked |
| FA-17 | AT-50, AT-51 | **amended**: non-vacuous subjects |
| FA-18 | §3, IMP-17, IMP-19, IMP-34, IMP-35, IMP-36 | **amended** |
| FA-19 | IMP-24, IMP-25, AT-74 | **amended**: T-6a, no back-fill |
| FA-20 | IMP-05 | **withdrawn** for `--slug`; the other two become sweep-gated candidates |
| FA-21 | §0, IMP-08 | **amended**: warrant classes stated |
| FA-22 | IMP-04 | **amended**: fourth check added; `adjudication_integrity` described correctly |
| FA-23 | IMP-07, IMP-12, IMP-26, IMP-39 | **amended**: cross-references corrected |
| FA-28 | OD-22 | **amended**: command corrected |
| FA-29 | AT-69 | **amended** |
| FA-30 | OD-04 | **amended**: PS:4835 carried |
| FA-31 | §0 | **amended** |
| FA-32 | IMP-05 | **withdrawn**: the view is not a subset |
| FA-34 | IMP-03 | **amended**: split into 03a (text) and 03b (schema change, Wave 2) |

---

## 7. Stress-test deltas (from `hs-stress-audit.md`, HS-5)

Evidence tags are scenario names in `stress/results/<topic>/log.jsonl` and `stress/results2/*/log.jsonl`; behaviour ids (B-nn) are HS-5 §1.

### IMP-41 Research batches are serial; say so where the second one is stopped
- **Change:** CONVENTION, then the smallest CODE if the capture does not already refuse. Every id a verb allocates on a scratch copy is written into the batch as an explicit value, so two batches captured from one base collide (B-40: `UNIQUE constraint failed: evidence_sources.ref_id` at rebuild). The workplan already merges one pull request at a time (WR-1); what is missing is that a later research batch cannot be "renumbered" like a schema migration: its rows must be regenerated by re-running its verbs on a copy of the new `main`. The stop should come at capture, with that step named.
- **TD:** REQ-001 (dynamic), REQ-019, REQ-090. **BU:** BU §C.1; HS-5 B-40. This is IMP-11's subject; IMP-11 was withdrawn on the ground that replay was untested, and the test has now been run.
- **Reads it:** `emit_batch_sql.py`, `/run-pipeline`, `/session-open`. **Wrong thing:** two sessions research in parallel and the second session's verified rows are lost or re-typed from memory.
- **Files:** `skills/run-pipeline_SKILL.md`; `scripts/research/emit_batch_sql.py` only if AT-101 is red. **Deps:** none. **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-101. **Risk:** low. **Owner gate:** none for the convention; OD-27 if parallel batches are wanted (that needs ids allocated at replay, which this programme does not propose unasked).

### IMP-42 A term becomes a parameter only when it states what it measures
- **Change:** CODE, small, with the quantity-kind column of IMP-30 (now split: IMP-30a the column and its vocabulary, IMP-30b units and conversion). `add-parameter` refuses a term with no quantity kind.
- **TD:** REQ-034, REQ-099, HS-A14 (a parameter and its element are distinct terms, PS:612), REQ-098. **BU:** HS-5 B-05: `grab bar`, `Reach & manipulation`, `thermal comfort`, `jurisdictional accessibility standards` and `wheelchair propulsion` each became an active parameter in one command.
- **Reads it:** `add-parameter`; `v_scan_ledger` (each parameter is one owed reading per source); the engine (each parameter is a determinable cell per lens). **Wrong thing:** an element or a method concept is "determined", fills the ledger with readings nobody owes, and appears as a pending cell with a gap.
- **Files:** schema migration (one column, CHECK vocabulary); `scripts/db.py insert_parameter`. **Deps:** none. **Layer:** 1–2. **Kind:** TOOLING. **AT:** AT-77. **Risk:** the ten live parameters need a kind each, a small data change in its own pull request. **Owner gate:** none for the refusal; the vocabulary of kinds and the granularity policy are OD-24.

### IMP-43 A source is written with its verification standing and its type, or not at all
- **Change:** CODE, small. `add-source` refuses when `--verification-status` or `--source-type` is absent.
- **TD:** REQ-051, REQ-023; `governance/research-contract.yaml:217-219` ("UNVERIFIED is a real value - say it"). **BU:** HS-5 B-12: two fixture sources written with `verification_status` NULL, one with `source_type` NULL.
- **Reads it:** C10 of `test_db_integrity`, the engine's `_verified`, `metadata_integrity_audit`. **Wrong thing:** a source whose standing nobody stated is read as neither verified nor unverified.
- **Files:** `scripts/db.py` (`add-source` dispatch). **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-78. **Risk:** skills and tests that call `add-source` without them (sweep first). **Owner gate:** none.

### IMP-44 The claimed number is checked as a number
- **Change:** CODE, small. `_require_verbatim` (`scripts/db.py:8559-8563`) takes the digit runs of `claimed_value` and asks whether each occurs anywhere in the quote after punctuation has been stripped. Compare instead the numbers the quote states, with their decimal position and grouping read before normalisation.
- **TD:** REQ-023, CLAUDE.md §5(c). **BU:** HS-5 §2.3 item 1, tested on the live functions: `12` accepted against "1.2 m", `0.6` against "6.0 s", `8.33` against "83.3 %", `5` against "1:15 in 2015".
- **Reads it:** `add-extraction`, `amend-extraction`, `derive-extraction`. **Wrong thing:** a figure with a shifted decimal point, under a quote that verifies, governs a determination.
- **Files:** `scripts/db.py` (`_require_verbatim`, the CJK helpers), `scripts/research/retrieval_log.py` only for a number tokeniser. **Deps:** none; coordinate with T-1a and IMP-23. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-79. **Risk:** locale formats (`1.234,56`, `1,50,000`, `12 500`) must be read, not refused; stored figures are re-checked by a report, not rewritten. **Owner gate:** none.

### IMP-45 A delete that deletes nothing says so
- **Change:** CODE, one refusal. `delete-connection` on an id that is not a row prints `{"deleted": …}` and exits 0 (B-42); `update-connection` on the same id refuses.
- **TD:** REQ-021 ("not done" and "done" are different states), REQ-018. **BU:** HS-5 B-42.
- **Reads it:** sessions that act on the printed result. **Wrong thing:** a session believes a wrong connection was removed.
- **Files:** `scripts/db.py`. **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-100. **Owner gate:** none (whether hard deletion of a connection should exist at all is REQ-018's question and is not reopened here).

### Changes to existing entries
- **IMP-02** gains one mark: CLAUDE.md §1 "Use `--battery <name>`" becomes the form that runs (`--battery <name>` with `--kinds`, `--all` or `--changed-from`; B-53). AT-102.
- **IMP-30** is split: IMP-30a (quantity kind on a parameter; Wave 1, with IMP-42) and IMP-30b (units and exact conversion as rows; OD-22 for rounding).
- **IMP-04** is confirmed as a reporting fix: the diff-scoped gate on a copy of `main` is green with these checks counting retired rows (B-54).
- **IMP-09, IMP-12, IMP-17, IMP-18, IMP-23, IMP-28** each now cite a stress reproduction (B-17, B-16, B-33, B-01 and B-34, B-31 and B-32, B-06).

### OD-27 Are parallel research batches wanted?
Today a batch's ids are fixed when it is captured, so two sessions working from one base cannot both land (B-40). Options: (a) serial batches, each later one regenerated on the new `main` (IMP-41); (b) ids allocated at replay, a change to the capture and migration tools and to how the engine's hash treats ids. **Recommendation:** (a) for now; (b) only if the owner wants several topics researched at once.

### OD-24, extended
The stress run shows the question is live at the writer: what may be promoted to a parameter (B-05). The vocabulary of quantity kinds, and whether a parameter must belong to an element, are part of the granularity policy.

### New acceptance tests

| ID | For | Test | Red today because |
|---|---|---|---|
| AT-77 | IMP-42 | On a scratch copy, `add-parameter --term-id TERM-008` (grab bar) and `--term-id TERM-075` (a legal concept) are refused. | both accepted (`base.add-parameter-existing-term` in the grabbar and method topics) |
| AT-78 | IMP-43 | `add-source` with no `--verification-status`, or no `--source-type`, is refused; `select count(*) from evidence_sources where verification_status is null` stays 0. | accepted; two rows written with NULL (`cold.evidence.add-source-minimal`, `lateral.add-source-jurisdiction-UK`) |
| AT-79 | IMP-44 | With a scan recorded, a claimed `12` against a quote stating "1.2 m", `0.6` against "6.0 s" and `5` against "1:15" are each refused; `1.2` against "1,2 m" is accepted. | the check accepts all four of the first kind (tested on the live functions; not yet through the writer, which needs a scan first) |
| AT-100 | IMP-45 | `delete-connection` on an id that is not a row exits non-zero. | exits 0 and prints `{"deleted": "CON-1"}` (`chain.031`) |
| AT-101 | IMP-41 | After batch A is applied to a clone's canonical copy, `emit_batch_sql.py` for batch B (captured from the old base) refuses and names regeneration. | UNPROVEN: not run; today the collision surfaces at rebuild (`crosstopic.005`) |
| AT-102 | IMP-02 | Every command CLAUDE.md §1 prints runs as written on a scratch copy. | `run_checks.py --battery <name>` alone exits 2 (`tools.055` to `.064`) |

### Preconditions, restated
- **Before any further parameter is minted:** IMP-42 with IMP-30a.
- **Before new extractions are written (R-2, R-3):** IMP-44, and IMP-23 for sources outside Latin script.
- **Before a first live determination (R-5):** unchanged from §0: IMP-08 with IMP-40, IMP-20, R-6, and the blocking battery green on the scratch copy.
- **Research batches:** one at a time (IMP-41).

### Resolution record, confirmation pass (`fa-confirmation.md`)
The rows of that file marked inaccurate that touch this programme, each re-run or re-read before disposal. The complete list is in `hs-adversarial-findings.md` §6.

| Confirmation row | Disposition |
|---|---|
| D-04 · IMP-12 still ordered a deletion | **amended**: IMP-12 deletes nothing; callers listed by command |
| D-04 · IMP-03a ungated while OD-18 asked the same strings | **amended**: OD-18 asks cold-entry and re-entry conditions only |
| D-05 · IMP-40 and §0 attributed an order to the ledger | **amended**: stated as this leg's sequencing; PS:4934 and PS:4938 quoted for what they say |
| D-06 · AT-76 "For: IMP-16" | **amended** |
| D-08 · "already seeds the other defects" | **amended**: four of five; IMP-10 is two fixtures; AT-55 restated |
| D-12 · AT-53 not restated | **amended** to the ruled gate |
| D-02 · "four governing sources" for every provisional cell | **amended**: parameter 3 four, parameter 12 one |
| D-21 · "the owner's 'yes'" | **amended**: "Taken from the prompt's 'yes'" |
| D-12 · IMP-07's dependency on a mapped view | **upheld as unverifiable**: marked [U] in the entry |
