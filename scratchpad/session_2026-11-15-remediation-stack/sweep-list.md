# Items reported and not repaired, for the end-of-batch sweep (owner instruction 2026-11-15, later)

Each line: task, the item, why it was left, what the sweep must do. Struck through when repaired. Derived facts are not typed here.

## T-041
- `_tables` in batch_capture_report.py and audit/graph/extract_db.py are identical; no shared home; neither imports dbcore. Sweep: decide merge (a stdlib-only audit helper) or record as intentional.
- Not merged, differing: next_gap_id, _jlist, glob_to_re, db_path. Sweep: confirm none is named by a later task as one-home; if one is, amend that task file.
## T-007
- F7: a present value outside the vocabulary passed through the Python entry reaches the INSERT as a raw CHECK IntegrityError (CLI shielded by argparse). Sweep: decide whether insert_evidence_source should refuse non-members by name.
## T-009
- Unspaced scripts are one token (`_near_terms('勾配')`). A dictionary is forbidden; owner question or decline in writing.
- False friends in `_near_terms` across Latin-script languages (`--distinct-from` is the way out).
- Numerals written as words are not refused in names; `dbcore.VALUE_BEARING` (definition screen) unchanged.
## T-010
- OWNER: may bodies of law (TERM-067, TERM-075) and cost terms (TERM-066) be declined (OD-53 vs the task file)?
- Any term can be moved to a quantity domain by `amend-term --field domain --reason` (designed second way out).
- `amend-term` cannot mint a domain; moving a sole-carrier term away cannot be undone by it.
## T-006
- Orphan `connection_targets` row would be refused with no verb to delete it (none live, none constructible via db.py). Check against T-050 (retire in place).
- CLI echoes the id typed; `--dry-run` on an existing id prints `{"deleted": ..., "dry_run": true}`.
- Frozen IDEMPOTENCY.md row calls the verb idempotent.
## T-011
- OWNER (lens L7): the engine links any newest retired row, including one retired for error (retirement_reason not read).
- migration_reproducibility (blocking) compares counts only; a lost UPDATE of an old row is seen only by --deep (rule 3).
## T-004
- none beyond the repairs.
## T-015
- OWNER: a source in a language lang_jur_map does not hold (HR has a logged search, exec 66) cannot state its language at add-source or observe-term; NULL is then read as English. Add HR (and others) to the map, or allow a flagged "other" language?
- Spelling split: term_aliases lower (15), observed_terms upper, evidence_sources.lang_detected mixed and every new write upper; K-9 declines the UPDATE. Decide: a reader-side fold everywhere (already in views/R5/unmined) or a data migration.
- OD-03 (every attested form in any language) sits against refusing the harvest by language.
## T-001 (critic, 2026-11-15)
- DEFECT in task file T-001 step 4.4: it says `emit_batch_sql.py` refuses a batch captured from an older base. It refuses only when `main` ADDED rows to a captured table; where `main` CORRECTED an existing value, the diff emits an UPDATE reverting it (scratch run by the critic). The skill sentence now says so. The wrong thing reaching the database is a stale batch reverting a correction. Sweep: decide a guard (compare the scratch's base hash to main's) or leave the sentence; owner/tooling question; check against T-075 and the research PR.
- DEFECT in task file T-001 step 5: it directs back-pointers into the ledger by SUPERSEDES pair; the ratified DR-2026-09-26 §4.2(c) and the ledger's own entry on OD-39 forbid that for a ledger target. Done as an appended record instead; amend the task file text.
- `run_checks.py --battery <misspelt> --kinds data` selects 0 checks and prints PASS with exit 0. A zero-selection run says PASS. Sweep: T-075 covers what the gate reports it examined; confirm it covers the selected-0 case.
- `ratified` in `governance/pipeline-contract.yaml` stays false until the owner's OD-17; the selftest no longer pins the header (status and ratified are not tied together by the model). Owner question: should the model refuse `ratified: true` with a status other than ACCEPTED?
- Ledger locators: the earlier in-place insertion is reverted, so line numbers after the 2026-03 entries are unchanged; the new entries are appended.
## T-003
- `scripts/generate/owner_browser.html` ignores `resolved_under_delegation`: `openDecisions()` still lists OW-1b, OW-1c and OR-10b as waiting, and there is no group that shows them apart from the owner's own answers. Task step 4.3 says repair only if one condition does it; it takes three (the open filter, a new group with a card that does not say "Your words", and the builder's `wants`). The page cannot be built here (needs the sql.js wasm download), so an untested JS edit was not made. Sweep: make the three edits if the page can be built, else name it to the owner.
- OR-5b: the ledger answer is quoted but marked "ANSWERED BY THE OWNER, PARTLY" with three open edges; left unmarked so the open edges stay visible. Owner question: close OR-5b, or split it.
- OR-17b: no ledger entry quotes an owner answer to it by name (only a blanket "every recommendation of the base-population plan is applied" statement and a table row); left unmarked. Owner question.
- `owner_browser_build.py` prints "table with no gloss: base_jurisdictions" on every build (pre-existing).
## T-052 — STOPPED at its step 2 (nothing changed)
- The task's paragraph names `db.py add-locator --jurisdiction`. `add-locator` has no `--jurisdiction` flag (`python3 scripts/db.py add-locator --help`), and `insert_locator`'s allowed columns omit it. `source_locators.jurisdiction` exists but `scripts/audit/jurisdiction_db_vocabulary.py` EXEMPTs it as legacy free text (GAP-008; most populated values are prose, '—', URLs or topic names), so adding a validated flag there would mean first cleaning that column (a research-kind PR). The task says: stop, it is a writer gap for its own tooling pull request.
- Options for the sweep / owner: (a) a `--jurisdiction` flag on add-locator validated by `dbcore.check_jurisdiction`, after the legacy column is cleaned; (b) stage an out-of-scope CODE or STANDARD (OD-34 narrows the order to instruments) in `research_code_leads` through `db.py add-code-lead`, which already carries a validated jurisdiction, and say so in the two skills. (b) needs no code but chooses a store for a lead: the owner's or the sweep's call. Until then the two mining skills remain silent on out-of-scope sources (the defect T-052 describes stays).
## T-002 / T-042 (critic, 2026-11-15) — reported, to be rectified or put to the owner in the sweep
- `governance/pipeline-contract.yaml` judgment stage `anchor:` still reads "the 4-state determination machine + convergence + directness" (determination before synthesis; machine-read by `scripts/audit/graph/extract_contract.py`). The task changed `entry:` strings only. OWNER/DOCTRINE: where the determination machine sits.
- `governance/pipeline-operations.md` row 5 has synthesis producing `specifications` (PROPOSED status header); same ordering question.
- The specification entry says it takes "the syntheses and governing figures for a parameter and lens", but `convergence_assessment` has no parameter or lens column and `assess_cell.py` writes it in the same function as the specification. Text and engine order differ; no check reads `entry:`. Owner question: the order the engine should have.
- The evidence criterion now reads "No source the work rests on …" while PI rule #10 and DR-2026-05-13 still say "BPC synthesis claim", and `metadata_integrity_audit.py` tests neither predicate (it is red for open integrity flags on COMPLETE rows). Phrase "the work rests on" has no ruling behind it beyond the task file. Owner question: the scope of the existence gate.
- The deleted "RED on main" sentence of `metadata_integrity_audit` was true when written; rule 7 forbids stating CI state, so it was not restored. Run the check to read it.
- DR-2026-09-26 line 452 (frozen) still runs the removed grep pair as "CLAUDE.md rule 8's own pair".
