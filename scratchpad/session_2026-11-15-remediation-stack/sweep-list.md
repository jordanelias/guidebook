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
