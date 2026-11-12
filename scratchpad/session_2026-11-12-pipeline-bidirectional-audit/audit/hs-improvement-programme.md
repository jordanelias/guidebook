# HS-3 — Improvement programme

_Handshake leg, 2026-11-12 (UTC), HEAD `186defb`. Nothing here is implemented; the repository, the canonical database and git state are untouched. Every figure cites a command in `hs-handshake-matrix.md` (HS-1) or `hs-adversarial-findings.md` (HS-2); re-run before relying on one._

## 0. Verdict first

**No determination should be made canonical until three things are fixed, and all three are tooling the owner has already ruled on:** the engine must gather by lens tag (IMP-08), the specification gates must examine live rows and be able to go red (IMP-04, IMP-10), and the mobility split must be executed or explicitly re-confirmed (OD-14). Everything else in the programme widens what the pipeline can do; those three stop it from publishing a value for the wrong people.

**The first wave is doable now with no owner decision:** records and marks (IMP-01 to IMP-03, IMP-06), the false and vacuous check output (IMP-04), deletion of dead apparatus (IMP-05), registering the stage-pair gate as ordered (IMP-07), the lens-tag gather (IMP-08), and red-going tests (IMP-10). It is tooling only (rule 10), touches no doctrine, and each item names a test that fails on today's `main`.

**The programme is blocked behind the owner at eight points that matter:** what a jurisdiction is to a determination (OD-01), what language a page is in (OD-02), how a concept is held without English (OD-03), which jurisdictions are in scope (OD-04), how a later parameter reaches an already-read source (OD-23), how coarse a parameter is (OD-24), what a synthesis row is (OD-07), and how render is produced and stored (OD-12).

Counts: improvements `grep -c '^### IMP-' <this file>`; owner decisions `grep -c '^### OD-' <this file>`; new acceptance tests `grep -c '^| AT-[5-9][0-9] ' <this file>`.

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

### Wave 0 — records, marks and deletions (no behaviour changes)

### IMP-01 Record what the plan will cite
- **Change:** CONVENTION. Ledger entry quoting O1–O8 of 2026-10-12 (relayed, IG:11) with the owner's confirmation of the wording; supersession back-pointers for C-05 (PS:123, PS:129), C-16 (the 2026-08-19 rule against adversarial review of plans, superseded for this audit) and C-20 (PS:120).
- **TD:** REQ-005, C-05, C-16, C-17, C-20. **BU:** none measurable; `supersession_backpointer_audit` covers only named supersessions.
- **Reads it:** every later session, through CLAUDE.md §9 "Latest rulings". **Wrong thing:** a plan built on relayed sentences that bind nothing mechanical (PS:2763-2765).
- **Files:** `references/project-standards.md` (append only). **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-75 (partly). **Risk:** low. **Owner gate:** owner confirms O1–O8 wording in one reply.

### IMP-02 Mark what is superseded where a session will read it
- **Change:** CONVENTION. Flip the pipeline contract header to its ratified status (HS-A06); supersession banners on `architecture/navigation-modes.md` and `architecture/page-templates.md` (C-14); correct CLAUDE.md §5(c) "persists every payload" to the 2026-11-06 ruling (C-15).
- **TD:** HS-A06, C-14, C-15. **BU:** HS-2 F-04; BU §E (render prose homes describe a deleted model).
- **Reads it:** sessions orienting from CLAUDE.md §9 and the contract. **Wrong thing:** a renderer built to route by old item codes and to read `●` as "stated".
- **Files:** `governance/pipeline-contract.yaml:2-3`, the two architecture files, `CLAUDE.md`. **Deps:** none. **Layer:** 0–1. **Kind:** TOOLING. **AT:** AT-43. **Risk:** `research_contract_sync` and `claude_md_spine` read these files; run both after. **Owner gate:** none for marks; ratifying the corrected contract is OD-17.

### IMP-03 Make the contract say what the owner's order says, in both directions
- **Change:** CONVENTION, then the smallest CODE if the schema refuses it. Rewrite the synthesis and specification `entry:` lines (C-11), the research entry's "item" and the evidence criterion's "BPC synthesis claim"; add a `re_entry:` list per stage naming each ruled backward edge (HS-1 B7–B14) with its carrier row.
- **TD:** REQ-002, REQ-003, REQ-016, C-11. **BU:** BU §A.5 (circular entries), §B.4.
- **Reads it:** `pipeline_contract_audit`, `/run-pipeline`. **Wrong thing:** a re-entrant run has no stated precondition, so each session invents one.
- **Files:** `governance/pipeline-contract.yaml`; `schemas/pipeline_contract.py` only if it rejects the new key. **Deps:** IMP-12 to IMP-14 name the carriers. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-43, AT-44. **Risk:** selftest C7 on a basis rename (CLAUDE.md §1). **Owner gate:** OD-18 for entries at judgment, synthesis, specification and render, which no owner sentence describes.

### IMP-04 Make the specification gates tell the truth about their subject
- **Change:** CODE, a few lines each. `validate_evidence_state.py` reports live and retired rows separately and prints `EXAMINED:` as the live count; `adjudication_integrity` counts live determinations; `derivation_handshake_integrity` derives its explanatory sentence from the tables it describes.
- **TD:** REQ-020, REQ-024, CLAUDE.md §5(a). **BU:** BU problem 2; HS-2 F-11, F-19.
- **Reads it:** `run_checks.py` (its NOTHING-IN-SCOPE escalation works only on a true zero). **Wrong thing:** the first live determination ships under three blocking criteria that have only ever examined retired rows.
- **Files:** `scripts/validate_evidence_state.py`, `scripts/audit/adjudication_integrity.py`, `scripts/audit/derivation_handshake_integrity.py`. **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-54. **Risk:** a blocking check turning NOTHING-IN-SCOPE on `main`; that is the correct reading. **Owner gate:** none.

### IMP-05 Delete what nothing reads and no requirement asks for
- **Change:** DELETE, each with its evidence in the commit. `assess_cell --slug`; `reasoning_doc_citations`; `connections.opus_reviewed`; the four unlinked skill files; `v_item_provenance` (its span is a subset of `v_determination_provenance`'s; state the stages before deleting, CLAUDE.md §3). `gap_mining`, its three verbs and its audit go with IMP-12.
- **TD:** REQ-092, HS-A16; none of these objects is asked for by any requirement (HS-1 §7). **BU:** §G.1, §G.2, §G.5, §A.6.
- **Reads it:** nothing, which is the evidence. **Wrong thing:** not about the book; the cost is a session filing work into a dead table (CLAUDE.md §8 puts the burden on keeping).
- **Files/tables:** as named; a column a committed migration INSERTs is tombstoned, not dropped (rule 5; check with `grep -l "INSERT.*INTO \"\?<table>" scripts/migrations/*`). **Deps:** rule 4 sweep with the `repo-sweep` agent, views and registry included. **Layer:** 2. **Kind:** TOOLING. **AT:** `run_checks.py --selftest` and `schema_reference_audit` after. **Risk:** a prose caller. **Owner gate:** none (code).

### IMP-06 One home for "answered"
- **Change:** REUSE. `governance/owner-browser.yaml` derives each prompt's answered state from the ledger heading that answers it, or drops the field.
- **TD:** REQ-046. **BU:** HS-2 F-19 (OR-1c).
- **Reads it:** `owner_browser_build.py`, the owner. **Wrong thing:** the owner is asked again, or a session treats an answered question as open.
- **Files:** `governance/owner-browser.yaml`, the builder. **Deps:** none. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-75. **Risk:** low. **Owner gate:** none.

### Wave 1 — gates that can go red, and the engine's subject

### IMP-07 Register the stage-pair gate
- **Change:** REUSE + smallest CODE. `walkability.py` returns non-zero when a pair that has a path today loses it; one registry entry; `stage-map.yaml` gains the `views:` key.
- **TD:** REQ-006, REQ-017 ("Yes, register it", PS:4731). **BU:** BU §H was hand-built; HS-2 F-03.
- **Reads it:** `run_checks.py`. **Wrong thing:** a migration severs a stage from the spine and nothing notices until render is built on it.
- **Files:** `workplan/pipeline-state-graph/walkability.py` (or its move under `scripts/audit/`), `governance/check-registry.yaml`, `governance/stage-map.yaml`. **Deps:** none to register as advisory with the render pairs reported; blocking for render pairs waits on IMP-31. A check red on untouched `main` teaches nothing (CLAUDE.md §1), so the expected-absent pairs are derived from the stage map's empty stages, not listed. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-01, AT-53. **Risk:** low. **Owner gate:** none (ruled).

### IMP-08 The engine gathers by the lens tags on the figure
- **Change:** CODE. `gather_sources`, `gather_findings`, `gather_confirmers` and `gather_extraction_links` take the cell's lens and select rows carrying that code; `ALL` reaches only an `ALL` cell; no traversal through a crossing map (D-0184).
- **TD:** HS-A02 (PS:4630), REQ-077 (PS:4657), REQ-074. **BU:** BU problem 3; HS-2 F-01.
- **Reads it:** every determination. **Wrong thing:** "ramp gradient for Deaf people: at most 5 %", built from wheelchair evidence, marked and published.
- **Files:** `scripts/assess/assess_cell.py:235-420`; fixtures under the existing tests. **Deps:** IMP-10 for the test; interacts with OD-14 (which codes exist) and REQ-073 (most figures carry one model, so most cells empty until figures are re-tagged, a RESEARCH task). **Layer:** 2. **Kind:** TOOLING. **AT:** AT-50, AT-51, AT-34. **Risk:** changes every answer the engine gives; none is live. **Owner gate:** none for the behaviour (ruled); OD-16 for the rule-version bump.

### IMP-09 No stored row for a lens no figure carries
- **Change:** CODE in the engine's writer: with no figure tagged for the lens, write nothing and report which of "not relevant", "not yet researched", "researched, nothing found" applies, derived from lens-scoped searches and readings.
- **TD:** REQ-074, C-13. **BU:** scratch run 7 × `DEAF` wrote `pending` + a gap (HS-2 V17).
- **Reads it:** render's empty-state rule (RENDER-CONTRACT C4). **Wrong thing:** pages of "pending" rows for people a parameter does not concern.
- **Files:** `assess_cell.py` (`determine`, `main`). **Deps:** IMP-08, IMP-12; lens-scoped research data does not exist yet (HS-1 REQ-032). **Layer:** 2. **Kind:** TOOLING. **AT:** AT-52, AT-33. **Risk:** conflicts with REQ-040 (a pending cell has a gap) until OD-08. **Owner gate:** OD-08.

### IMP-10 Tests that fail on a seeded defect
- **Change:** CODE, in the existing tests. One fixture database per defect, each asserting that a named check exits non-zero: wrong-lens governing rows; a `stated` row with no governing link; regulatory-only marked above `○`; an unverified governing source under a full marker; a retired row surfaced by a view; a stale determination after a comparator change.
- **TD:** REQ-020, REQ-024, REQ-025, REQ-082, AT-19 to AT-22. **BU:** BU §F (no negative case anywhere); HS-2 F-01.
- **Reads it:** the `tests` battery. **Wrong thing:** a gate that has never been red is trusted on the first live rows.
- **Files:** `scripts/tests/`. **Deps:** IMP-04. **Layer:** 0. **Kind:** TOOLING. **AT:** AT-55. **Risk:** low. **Owner gate:** none.

### IMP-11 Identifiers allocated where rows land
- **Change:** CODE. Determination and gap ids are assigned at capture or replay against the canonical high-water mark, not from the scratch copy.
- **TD:** REQ-019, REQ-001 (dynamic). **BU:** BU §C.1; HS-2 F-15.
- **Reads it:** `emit_batch_sql.py`, `migrate_db.py`. **Wrong thing:** two sessions' determinations cannot both merge; one is redone from memory.
- **Files:** `scripts/assess/assess_cell.py` (emit), `scripts/research/emit_batch_sql.py`. **Deps:** none. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-56. **Risk:** `derivation_sha` must not depend on the id; verify. **Owner gate:** none.

### Wave 2 — typed causes for backward travel

### IMP-12 A gap that says what it is a gap in, and a search that says which gap caused it
- **Change:** CODE (schema). `gaps` gains `parameter_id`, the four lens columns, `jurisdiction`, `language` (FKs where a table exists); `search_executions` gains `gap_id`. Then DELETE `gap_mining`, its verbs and audit.
- **TD:** REQ-040, REQ-014, B10, C-21. **BU:** BU §B.4; RENDER-CONTRACT E8 "BLOCKED: `gaps` has no parameter key".
- **Reads it:** the engine (writes), `coverage`, render's Gaps element, IMP-30's cell status. **Wrong thing:** the book's stated gaps cannot be listed for a parameter or a group.
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

### IMP-16 Staleness that is caught, not hoped for
- **Change:** CODE, small. `stale_determinations` also recomputes the marker; `db.py` refuses, or the check reports, the three unguarded routes recorded at PS:4508 (a change of `verification_status`, of a governing row's comparator, a new finding). The check becomes blocking when the live count is non-zero, derived at run time.
- **TD:** REQ-025, REQ-009 (propagate). **BU:** BU §B.2.
- **Reads it:** `run_checks.py`. **Wrong thing:** a published value whose evidence changed underneath it.
- **Files:** `assess_cell.py:1777`, `db.py` guards, registry. **Deps:** IMP-10. **Layer:** 0–2. **Kind:** TOOLING. **AT:** AT-20, AT-21, AT-76. **Owner gate:** OD-16.

### Wave 3 — the base, as data (REQ-097)

### IMP-17 Jurisdictions in a table, read by the writers
- **Change:** CODE that deletes code. A base table of jurisdiction codes (kind: country, supranational, standards body, sub-national; parent; the ledger entry that admitted it); `dbcore.check_jurisdiction` reads it; the Python enum is generated from it or removed; `lang_jur_map.jurisdiction` gains the FK.
- **TD:** REQ-065, REQ-093, C-08, HS-A16 ("the less hard coded, the better"). **BU:** BU problem 6; Q32 (17 codes the enum lacks). PC:49 already says "base.jurisdictions, which has no table yet".
- **Reads it:** six writer call sites, `jurisdiction_db_vocabulary`, `coverage`. **Wrong thing:** research for a declared pair cannot be logged with its jurisdiction, so coverage can never read complete and a comparison table has holes that look like absence.
- **Files:** schema migration; `scripts/dbcore.py:945`; `schemas/enums.py`. **Deps:** IMP-19. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-28, AT-58. **Risk:** admitting a code is a scope decision (PS:3714): the table carries the approval pointer and the writer refuses without it. **Owner gate:** none for the mechanism; OD-04 for membership; OD-01 for sub-national rows.

### IMP-18 The scope, recorded
- **Change:** data. Fill `lang_jur_map.scope_status` for every pair from the owner-confirmed set.
- **TD:** REQ-063, REQ-064. **BU:** HS-2 F-14.
- **Reads it:** `v_research_scope`, `coverage`, render's E2.scope. **Wrong thing:** research is asked for from places the owner excluded, and the comparison table has no list to be cut to.
- **Deps:** IMP-19 (no writer today), OD-04. **Layer:** 3. **Kind:** RESEARCH (data PR). **AT:** AT-27, AT-57. **Owner gate:** OD-04.

### IMP-19 Writers for the base tables that have none
- **Change:** CODE, only for tables a ruled task must write: `lang_jur_map` (add pair, set scope), `base_taxonomy_identity` (OD-14), the jurisdiction table. The capture derivation includes them.
- **TD:** REQ-090 ("never hand-edit"), REQ-097. **BU:** BU §A.1, Q11.
- **Reads it:** `emit_batch_sql.py`. **Wrong thing:** base changes arrive as hand SQL that bypasses every refusal (CLAUDE.md §4).
- **Files:** `scripts/db.py`, `scripts/dbcore.py:1075`. **Deps:** none. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-28. **Risk:** each verb needs the refusals that are its value. **Owner gate:** none.

### IMP-20 Execute the mobility split
- **Change:** data, after the registry writer exists. Add the two codes; re-tag each `MOB` figure and grade by judgment (which group the study's participants are), never by mechanical fan-out of evidence; retire the eight determinations' cell.
- **TD:** HS-A01. **BU:** HS-2 F-02.
- **Reads it:** every lens-keyed table. **Wrong thing:** one ramp gradient for two groups the owner split because their needs oppose.
- **Deps:** IMP-19, IMP-08. **Layer:** 3. **Kind:** RESEARCH, Opus-class or above. **AT:** AT-62. **Risk:** 170 rows need a reading each. **Owner gate:** OD-14.

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

### IMP-24 Language codes with one spelling and one check
- **Change:** REUSE. The refusal `log-search` already applies is applied at `observe-term`, `add-source` and `add-alias`; one case; the retired `lang_detected` copies are written forward to `language`.
- **TD:** REQ-071, REQ-092. **BU:** BU §D.2; Q34.
- **Reads it:** `get_unmined_for_all_slugs`, coverage views. **Wrong thing:** English sources sorted as non-English and the reverse.
- **Deps:** OD-04 for script and regional variants (E7). **Layer:** 2. **Kind:** TOOLING. **AT:** AT-74. **Owner gate:** none.

### IMP-25 The source's own identity and edition
- **Change:** REUSE of columns that exist and are never written: `language`, `original_title`, `edition`, `code_currency_*`; one verb field each; `v_evidence_authors` shows a full given name where the script has no initials.
- **TD:** REQ-067, REQ-071, HS-A11. **BU:** BU §D.6, §G.4.
- **Reads it:** render's evidence list; `jurisdiction-tracker`. **Wrong thing:** a superseded edition cited as current; an author rendered as one character.
- **Deps:** OD-02 (whether translated titles are shown). **Layer:** 2. **Kind:** TOOLING, then RESEARCH backfill. **AT:** AT-03, AT-61. **Owner gate:** none for the columns.

### Wave 4 — read once, unify, find (REQ-098, REQ-099, REQ-100)

### IMP-26 The clause as a unit of evidence
- **Change:** CODE (schema), the smallest table: one row per clause read (source, typed locator, verbatim text in the source's language, the file hash). Extractions, observations and relations point at it; `claim_text` and the `loc_*` columns on judgment rows become tombstones.
- **TD:** REQ-097 ("clauses in order to group"), REQ-013, REQ-098. **BU:** HS-1 §5.1 (a clause is repeated per parameter and nothing can point at one).
- **Reads it:** `add-extraction` (pointer instead of copied text), the verbatim check, IMP-27's sweep, IMP-34's candidates, render's "what the source says, where". **Wrong thing:** the same clause quoted three ways in three rows; no way to say two jurisdictions' clauses are the same provision.
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
- **Deps:** IMP-26, IMP-29, IMP-30. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-71. **Owner gate:** none.

### IMP-35 One read-only answer for a cell at every stage
- **Change:** CODE, read-only: a `db.py` query verb that, for a parameter and optional lens, jurisdiction and language, reports per stage what is held, what was examined and found empty, what was never examined, and what is owed, each with its row ids.
- **TD:** REQ-001, REQ-021, C-13, TD §3.9 (the part that needs no new object). **BU:** BU §C.1 (a cell can be run; nothing says where it stands).
- **Reads it:** `/run-pipeline` at entry at any stage; the owner. **Wrong thing:** a run started mid-pipeline repeats or skips work because nothing states the cell's standing.
- **Deps:** IMP-12, IMP-18. **Layer:** 2. **Kind:** TOOLING. **AT:** AT-07, AT-23. **Owner gate:** none; a stored request record is OD-09.

### IMP-36 Skills that describe the database that exists
- **Change:** DELETE and edit. `multilingual-research`, `cross-population-conflict-mapper`, `gap-driven-mining` and the other files failing `skill_vocabulary_audit` are corrected or retired; `connection-discovery` gains the relation kinds of IMP-32.
- **TD:** REQ-053, REQ-100. **BU:** HS-2 F-18.
- **Reads it:** every research session. **Wrong thing:** research run to a procedure that names tables and codes that are gone.
- **Deps:** IMP-32. **Layer:** 2. **Kind:** TOOLING. **AT:** `skill_vocabulary_audit` exits 0. **Owner gate:** none.

### Wave 5 — jurisdiction downstream, and render

### IMP-37 The jurisdiction comparison as a view
- **Change:** CODE, one cross-stage view over judgment rows (parameter, lens, jurisdiction, figure, source). No new table; the key of a determination is unchanged.
- **TD:** REQ-069, C-03 as read. **BU:** BU §B.3 (no typed comparison).
- **Reads it:** render E2. **Deps:** IMP-17, IMP-18. **Layer:** 1. **Kind:** TOOLING. **AT:** AT-31. **Owner gate:** OD-01 if a determination is to vary by jurisdiction.

### IMP-38 Render
- **Change:** blocked on OD-02, OD-08, OD-12. Then REUSE of `RENDER-CONTRACT-parameters-3-and-12.md` (elements, rules, invariants) and of the gate split recorded at PS:588.
- **TD:** REQ-083 to REQ-089, HS-A09. **BU:** BU §E. **AT:** AT-35 to AT-39. **Owner gate:** OD-02, OD-08, OD-12.

### IMP-39 The owner's edits
- **Change:** blocked on OD-09's sibling reading (C-19): proposals through the write path, no second path.
- **TD:** REQ-009. **BU:** browser is read-only. **AT:** AT-20, AT-42. **Owner gate:** OD-20.

### Research tasks the tooling unlocks (each its own pull request)
- **R-1** Fill the medical lens by correspondence (HS-A03; `add-medical` exists). Owner gate: OD-15.
- **R-2** Read what is held, in full, with the open pass (IMP-27).
- **R-3** Re-tag figures with every relevant model (REQ-073), after IMP-08.
- **R-4** Attest forms per language and jurisdiction pair from instruments (REQ-058, REQ-060), after IMP-22.
- **R-5** First live determinations, only after IMP-04, IMP-08, IMP-10 and OD-14.

---

## 2. Owner decision register (summary; the Sonnet suite writes the full register)

Each is `OWNER DECISION REQUIRED`. Options and a recommendation are offered; nothing is decided here.

### OD-01 Does a determination vary by jurisdiction, and what is a jurisdiction below the country?
Options: (a) one determination per parameter × lens, jurisdictions shown as a spread (TD's reading); (b) a determination per jurisdiction; (c) (a) plus typed conditions for climate and cultural context (HS-A12). Sub-national: codes with a parent, or stay at country. **Recommendation:** (c), with sub-national rows; `REF-01013` shows the need.

### OD-02 What language is a page in, and may a source's sentence be translated?
Options: (i) English pages citing each source in its own language; (ii) pages in several languages. **Recommendation:** (i) for this edition, quotes shown in the original with a marked translation only where the owner permits one.

### OD-03 How is a concept held without an English name?
Options: (a) forms table with a display pointer (IMP-21); (b) keep `canonical_en`, add a label kind; (c) nothing until a non-English-origin concept is minted. **Recommendation:** (a); (c) is defensible today (no such term exists, Q39) and defers the cost to the first such concept.

### OD-04 Which jurisdictions and languages are in scope?
Buckets 1–2 (PS:4312) and P1+P2+P3 (PS:5026) differ by `UN` on one side and `BE, CH, CN, DK, IT` on the other; doctrine names 24 with a Global South floor. **Recommendation:** confirm P1+P2+P3 as the research scope, rule on `UN`, and say whether script and regional variants (Chinese scripts; Bokmål and Nynorsk, E7) are separate pairs.

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

### OD-14 Executing the mobility split
Confirm the two codes; say whether `MOB` survives as an additive tag; say how part-time wheelchair users are named in a gap. **Recommendation:** execute before any determination on a mobility parameter.

### OD-15 Filling the medical lens
Confirm the corrected ruling (by correspondence, roughly the size of the registries held) and the WHO licence position (E5). **Recommendation:** proceed, English anchors only until the licence is read.

### OD-16 Does a change in engine behaviour bump the rule version?
**Recommendation:** yes, always; otherwise `derivation_sha` cannot tell two rules apart (PS:4491 item 4).

### OD-17 Ratify the corrected pipeline contract
**Recommendation:** after IMP-03.

### OD-18 What "all directions" covers
Confirm the entry and re-entry conditions for judgment, synthesis, specification and render (TD §3 is inference), and whether an earlier stage's row may be updated to record later use (REQ-012 against live writers). **Recommendation:** allow status updates on earlier rows; forbid copying later facts into them.

### OD-19 Conflict between groups in the engine
Harm asymmetry and broadest benefit are canonical doctrine the engine does not apply. **Recommendation:** record conflicts and the rule applied as rows; the engine reads them only after the owner approves the rule's mechanical form.

### OD-20 The owner's edits
Confirm the ledger's reading: proposals applied through the write path (PS:4586).

### OD-21 Are a reader's or the owner's questions about a published cell recorded in the database?
**Recommendation:** yes, as an open gate that flags the cell (IMP-14).

### OD-22 Rounding direction for converted lengths (OR-10b), and the other open prompts
List them: `python3 -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['queue'] if 'answered' not in q])"` (adjust the key to the file's shape; cross-check each against the ledger, IMP-06).

### OD-23 How a parameter defined later reaches a source already read
Options: (a) **re-read**: keep only what was extracted; each new parameter owes a targeted reading of every source; simplest, costliest, and needs the bytes again (10 of 58 live sources hold none); (b) **retained text**: keep each source's text layer and page images, addressed by hash, in the repository where size allows and by location otherwise (PS:5110-5112: retrieved standards may be held; PS:5126: large files are logged by location); a new parameter is swept over held text, re-retrieval only where nothing is held; (c) **clause inventory**: the open pass records every normative or quantitative clause as a row; a new parameter is matched against rows; text is held only for those clauses. Trade-offs: holding retrieved copies is already ruled acceptable (PS:5110-5112); (c) puts clause text into a database that the site is to read, and showing that text publicly is a further act the owner has not ruled on (licensing); (c) is queryable and lets equivalence groups point at clauses (REQ-097), and misses whatever the open pass did not judge to be a clause; (a) misses nothing in principle and never ends. **Recommendation:** (c) with (b) as its backing, and a recorded re-read where neither is possible.

### OD-24 How coarse a parameter is
Options: (a) flat and coarse: one parameter per measured quantity of an element, every clause variation a typed condition on its figures; (b) hierarchy: a parent parameter with children for materially different cases; (c) flat and fine with equivalence groups above. The trap: too fine cannot unify; too coarse hides the divergence the book exists to show. **Recommendation:** (a) with the term pointers of IMP-29 for families, and a written test for a split (two cases become two parameters only when they cannot be placed on one scale, or their directions differ). Whether that test is doctrine or convention is the owner's.

### OD-25 Which relations synthesis records, and who may judge them
The owner's four words map to three kinds (equivalence, adjacency, similarity or commonality) plus the two that exist (conflict, convergence). **Recommendation:** those five; found by query, judged at the synthesis capability floor (Opus-class or above), each recorded as pointers with its warrant.

---

## 3. Sequencing

| Wave | Contents | Kind | Needs the owner first? |
|---|---|---|---|
| **0** | IMP-01, 02, 03 (text), 04, 05, 06 | TOOLING | IMP-01 needs one confirmation; the rest none |
| **1** | IMP-07, 08, 10, 11; IMP-09 after OD-08 | TOOLING | OD-16 for the version label only |
| **2** | IMP-12, 13, 14, 16 | TOOLING | OD-10, OD-21 for two vocabulary values |
| **3** | IMP-17, 19, 22, 23, 24, 25 (tooling); then IMP-18, 20, R-1, R-4 (data) | both, in that order | OD-04, OD-14, OD-15; IMP-21 on OD-03 |
| **4** | IMP-29, 30, 34, 35, 36 (no gate); IMP-26, 27, 28 on OD-23; IMP-32, 33 on OD-07, OD-25; then IMP-31, R-2, R-3 (data) | both | OD-23, OD-24, OD-07, OD-25 |
| **5** | IMP-37; IMP-38, 39 | TOOLING | OD-01, OD-02, OD-08, OD-12, OD-20 |
| last | R-5: first live determinations | RESEARCH | OD-14 |

**First wave doable now:** Wave 0 and, in the same or the next tooling pull request, IMP-07, IMP-08, IMP-10 and IMP-11 of Wave 1. Dependencies inside it: IMP-04 before IMP-10; IMP-10's wrong-lens fixture before IMP-08 is merged, so the test is seen red first.

**Order rules.** Tooling before the rows that use it (rule 10). A schema change runs `joined_cells_census.py` before and after (CLAUDE.md §4) and `run_checks.py --selftest` after any rename. The gate is run once, when the diff is ready (CLAUDE.md §1). Nothing in Waves 2–5 is added without the reader named in its entry existing or landing with it.

---

## 4. New acceptance tests (each red on today's `main`, or stated otherwise)

TD's AT-01 to AT-49 stand, with AT-04 made conditional on OD-12. Red today was observed by this leg unless marked.

| ID | For | Test | Red today because |
|---|---|---|---|
| AT-50 | IMP-08 | On a scratch copy, a determination for parameter 3 × `DEAF` has no governing row whose lens tag is not `DEAF`. | 35 governing rows tagged `MOB` |
| AT-51 | IMP-08 | A figure tagged `ALL` governs only an `ALL` cell, and an `ALL` cell is governed only by `ALL` figures. | parameter 3 × `ALL` governed by `MOB` rows |
| AT-52 | IMP-09 | A cell whose lens no figure carries yields no determination row. | parameter 7 × `DEAF` wrote `pending` and a gap |
| AT-53 | IMP-07 | The registry holds the stage-pair gate and it exits non-zero when a path that exists is removed. | `grep -c walkability governance/check-registry.yaml` = 0 |
| AT-54 | IMP-04 | With zero live determinations, each specification check reports zero examined. | `validate_evidence_state` prints `EXAMINED: 13` |
| AT-55 | IMP-10 | Each seeded defect turns its named check red. | the wrong-lens fixture passes three checks |
| AT-56 | IMP-11 | Two cells determined on two scratch copies both replay into one database. | both allocate the same ids |
| AT-57 | IMP-18 | Every `lang_jur_map` row has a scope, and `v_research_scope` returns no scoped-out pair. | scope NULL on every row; view returns all |
| AT-58 | IMP-17 | Every jurisdiction in `lang_jur_map` resolves in the vocabulary the writers read. | 17 do not |
| AT-59 | IMP-23 | Two sentences that differ only in vowel signs or voicing marks do not normalise to the same string. | Devanagari and kana pairs collide |
| AT-60 | IMP-23 | A name containing a digit in any script is refused; a non-Latin name yields a non-empty token set. | `幅１２００` passes; `勾配` yields none |
| AT-61 | IMP-17, 25 | No source issued by a sub-national body carries a bare country code. | `REF-01013` |
| AT-62 | IMP-20 | The identity registry holds the split codes, and no live figure carries a superseded one. | `MOB` on 170 rows; no `AMB`, `WHEEL` |
| AT-63 | R-1 | The medical registry and its two crossing maps are non-empty. | 0 rows each |
| AT-64 | IMP-27 | Every live source has a full-scope `full-read` scan with its open pass done, or a typed blocked reason. | no `full-read` scan; no open pass |
| AT-65 | IMP-28 | After a parameter is added on a scratch copy, the owed sources are listed by one query and each has held text or clause rows, or a recorded re-read. | the list exists; 35 of 58 live sources hold no text layer |
| AT-66 | IMP-26 | A clause stating two parameters is stored once and pointed at by both figures. | no clause table |
| AT-67 | IMP-29 | For an element term, one query returns its parameters through a typed pointer. | no pointer table |
| AT-68 | IMP-30, 31 | For each parameter, every governing claim is placed on the parameter's scale or carries a typed reason. | 11 of 35 for parameter 3 (BU); none for parameter 12 |
| AT-69 | IMP-31 | No `claimed_unit` holds a condition. | `joined_cells_census.py`; 32 distinct unit strings for parameter 3 |
| AT-70 | IMP-32 | Each relation kind has a vocabulary value and at least one row with a pointer at each end, and something reads it. | 0 rows; no such values |
| AT-71 | IMP-34 | For a parameter, one read-only command returns candidate relations with the rows that suggest them. | no such command |
| AT-72 | IMP-13, 14 | A question on a figure and on a cell can be raised, flags the cell, and can be resolved. | no carrier |
| AT-73 | IMP-12 | Every gap the engine writes carries its parameter and lens; a search can name the gap that caused it. | no such columns |
| AT-74 | IMP-24 | Every language value in the five tables that carry one resolves, in one case. | mixed case; `HR` on a search |
| AT-75 | IMP-06 | Every prompt the ledger answers is marked answered. | OR-1c |
| AT-76 | IMP-16 | Every live determination carries the current rule version and recomputes to its stored answer. | not red: 0 live rows; it is UNPROVEN until one exists |

---

## 5. What this programme declines

- A `requests` table, a "return" marker, per-language word lists for name screening, a per-stage service interface. Each is apparatus; the entries above say what replaces it or why nothing does.
- Any change to tiers, markers, the lens set, the scope or the mission.
- Restating `workplan/2026-10-23-pipeline-resolution-workplan.md` (T-1 to T-7) or the draft render contract. Where an improvement overlaps a task there (IMP-30 with T-1 step 9; IMP-08 with T-3; IMP-37 and IMP-38 with T-5 and T-7; IMP-18 with T-6b), the suite cites the task and says what changed.
