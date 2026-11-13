# R2 probes (OI-20): AT-15, AT-16, AT-17, AT-18, AT-34 (first half), AT-47

Date 2026-11-13 02:5x UTC. Base: commit 4978132, branch r2-baseline cut from origin/claude/peaceful-noether-kvf3sf, schema user_version 125.
Every write ran on a COPY (`probe.db`, copied from data/guidebook.db in the scratch clone) with `GUIDEBOOK_DB_PATH` inline. Canonical sha256 before and after: c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d (identical).
Test text: scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md lines 523-555 (AT table). hs-improvement-programme.md mentions AT-34 only as a dependency of the assess_cell task.

| AT | Verdict | EXAMINED |
|---|---|---|
| AT-15 | GREEN | 4 write cases + 203 live rows |
| AT-16 | RED (state/stated-cause clause); delete-refusal clause GREEN | 13 live zero-result searches + 3 delete paths |
| AT-17 | RED | 14 deferred subjects (1 search + 13 mining), 0 for readings |
| AT-18 | RED (figure; and ref_id under hard delete); parameter, determination, source GREEN | 4 object kinds |
| AT-34 (first half) | RED | 1 injected medical-only row; canonical audit EXAMINED: 0 |
| AT-47 | GREEN on state; writer unguarded (note) | 24 non-English sources; 5 write cases |

## AT-15  A search can be logged for a parameter with no slug and is refused when it names neither a slug, a parameter nor a mined source.
Probe: `db.py log-search` on the copy, three ways, plus a raw INSERT in a rolled-back transaction. Parameter id was chosen by query (lowest active `parameter_id`); the mined ref was chosen by query.
- `--parameter <id>` and no slug: accepted (rc 0), `slug` null in the row.
- `--mined-ref-id <ref>` and no slug: accepted (rc 0).
- none of the three: `REFUSING: A search names what it looked for: pass --slug, --parameter ... or --mined-ref-id` (rc 1), no row written.
- raw INSERT bypassing the CLI: `CHECK constraint failed: COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL`.
- Live data: 203 rows in search_executions, 0 with none of the three, 7 slug-less rows all carrying a parameter.
EXAMINED: 4 write cases + 203 live rows. Verdict GREEN.
Note for the next prober: `log-search` refuses first on a missing `--prior-expectation`, which masks the subject refusal; supply the prior or the test refuses for the wrong reason.

## AT-16  A zero-result search is stored, cannot be deleted through the sanctioned path, and states which of three causes applies.
Probe: live query for zero-result rows; `log-search --results-found 0` with and without `--absence-class`; `dbcore.deletable_tables`; `emit_batch_sql.py` on a scratch with one zero-result row deleted.
- Stored: yes. 13 live search_executions rows have results_found = 0.
- Not deletable through the sanctioned path: GREEN. `search_executions` is not in `dbcore.deletable_tables` (only connection_targets, connections, evidence_source_authors, search_admissions). `emit_batch_sql.py` refuses the deletion ("rows were deleted ... Refusing to emit"), and `--allow-delete search_executions` is refused ("no sanctioned writer deletes from that table"). There is no db.py delete-search verb. Caveat: there is no trigger, so a raw DELETE on the table is accepted by SQLite itself.
- States which of three causes: RED. The typed column `absence_class` (query_shape_failure | wrong_index | genuine_absence) exists and is refused on a non-zero search, but 0 of the 13 live zero-result searches carry it (12 carry only a free-text findings_note, 1 is a deliberate deferral). `log-search --results-found 0` with no `--absence-class` is ACCEPTED (rc 0), so the cause is optional at write time; `amend-search --set-absence-class` is the after-the-fact path. R14 in research_dod accepts a note in place of the class.
EXAMINED: 13 zero-result rows + 3 delete paths. Verdict RED. Defect: the writer does not require a cause for a zero-result search, and no live zero-result search states one in the typed column; expected: every zero-result row states exactly one of the three.

## AT-17  The set of deferred acts (mining, searches, readings) older than a stated age can be listed by one query.
Probe: read-only SQL on the copy. A UNION over `search_executions` (deferred_reason not null) and `citation_mining` (deferred_reason not null), filtered `created_at < date('now','-30 days')`, runs as one query and returned 9 of 14 subjects (1 search, 13 mining).
- Readings: no representation. `source_scans` has no deferred state, `v_scan_ledger` has no timestamp column (ref_id, parameter_id, status, scan_id, text_scope, method), its BLOCKED status has 0 rows, and NOT-READ (417 pairs) carries no age or deferral stamp. `evidence_sources.data_capture_status = 'deferred'` has 0 rows and no deferral date (only a rewritable updated_at).
- No view, verb or registered check lists deferred acts; the three-class query is something a reader would have to write.
EXAMINED: 14 deferred subjects across 2 tables; 0 reading subjects reachable. Verdict RED. Defect: "one query" over searches, mining and readings is not possible, because a deferred reading is not a recorded state and has no date; expected: all three classes list with an age from one query.

## AT-18  Retiring a source, a figure, a parameter and a determination leaves each row present with a status, and the next identifier issued is higher than any ever used.
Probe on the copy, each by the sanctioned verb, row counts compared before and after:
- Source: `supersede-source` on the highest live ref (ids chosen by query). Row count 59 before and after, `superseded_by_ref_id` set. GREEN.
- Parameter: `retire-parameter` on the highest parameter with no live determination and no gate (id chosen by query). Row count 10 before and after, status `retired`, its 21 extractions kept as history; `sqlite_sequence` for base_parameters stays at 12 (AUTOINCREMENT, no reissue). GREEN.
- Determination: all 8 live specifications rows are already retired in place (8 rows, max id 8, sequence 8). A fresh retirement could not be staged: the table's CHECK refuses un-retiring a row, and no live determination exists. `retire-specification` on a retired row refuses ("already retired"). Judged GREEN from live rows, not from a fresh act.
- Figure: RED. No verb retires a figure. `source_value_extractions` has no status or retired column (extraction_status covers review state: preliminary/reviewed/verified/contradicted/absent-confirmed), `amend-extraction` changes only figure_role and comparator, and 13 extraction ids (sequence 227, 214 rows) were hard-deleted by a data migration (`2026-09-13-clear-circulation-corpus`). AUTOINCREMENT keeps those ids from being reissued, but the rows are gone.
- Next identifier: parameter, specification and extraction ids are AUTOINCREMENT, so GREEN. `ref_id` is not: `dbcore.next_ref_id` is the max over live rows of 13 tables + 1. Superseding the highest source leaves it at REF-01037 (GREEN), but a hard delete of the highest ref (raw SQL, FKs off, rolled back) made `next_ref_id` fall from REF-01037 back to REF-01036, i.e. an identifier once used would be reissued. Today the highest REF in any migration equals the highest live ref (REF-01036), so no reissue has occurred yet.
EXAMINED: 4 object kinds (source, parameter, determination, figure). Verdict RED. Defect: a figure has no retire-in-place path (hard-deleted in the past), and ref_id monotonicity depends on never hard-deleting the highest row.

## AT-34 (first half)  A determination with only a medical code is refused.
Probe: on the copy, a raw INSERT into `specifications` with `medical_code` only (parameter chosen by query, no identity/icf/needs). `base_taxonomy_medical` holds 0 rows, so:
- FKs ON: refused with `FOREIGN KEY constraint failed`, a refusal for the wrong reason (empty medical table), not for the frame.
- FKs OFF (isolates the schema's own checks): ACCEPTED. The CHECK is `COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL` (at least one lens, D-0182), so a medical-only key satisfies it. No trigger touches the table except retire-reason. `assess_cell.py` has no medical-only refusal (its docstring says it "should never emit one").
- The only gate is `medical_lens_integrity` (registered advisory): run against the copy it prints FAIL for the injected row (rc 1), but on the canonical DB it prints `EXAMINED: 0` and passes; on the copy it also prints `EXAMINED: 0` while failing, because its EXAMINED counts medical-registry rows, not specifications.
EXAMINED: 1 injected row (canonical audit EXAMINED: 0, NOTHING-IN-SCOPE). Verdict RED. Defect: nothing refuses a medical-only determination at write time; the after-the-fact detector is advisory and its subject count does not count what it tests; expected: a write refusal.

## AT-47  No non-English journal article is filed as grey without a recorded warrant.
Probe: read-only SQL for the live state; `db.py add-source --dry-run` and one real write on the copy for the writer; `research_batch_dod.py --all` against the copy for the detector.
- State: of 59 sources, `language` is null on all 59 and `lang_detected` holds the language (mixed case: 'en' and 'EN'). 24 are non-English. 3 of them are filed grey or flagged grey, and none carries a journal mark (journal_name, DOI or source_type journal_article); 0 carry the `R5-GREY-WARRANTED:` token. One grey source (REF-01016, a standard) has no language recorded and is outside the 24.
- Writer: `add-source` ACCEPTS a Dutch `journal_article` with a DOI, `evidence_type grey`, `grey_flag 1` and no `grey_reason` (dry-run and real write both rc 0); it also accepts one with a reason lacking the token. Nothing refuses at write time.
- Detector: `research_dod` R5 (registered advisory) caught the injected row ("1 of 25 non-English admission(s) filed evidence_type 'grey' while carrying a mark of journal publication ... unwaived"), so the detector can go red.
EXAMINED: 24 non-English sources, 5 write cases. Verdict GREEN on state (0 violations). Note: unguarded at write time; it relies on an advisory post-hoc check.
