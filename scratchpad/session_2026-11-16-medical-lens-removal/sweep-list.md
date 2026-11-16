# Items reported and not repaired in the stacked batch (medical-lens deletion, T-061, T-063, T-067, T-074, T-075, T-079, T-088)

Owner instruction 2026-11-15 (later): sweep forward and backward, repair, and name each owner question. Each line: item, why left, the file(s) that would change. Derived facts are not typed here: re-run the command in the pull request body.

## Owner questions (doctrine or a ruling the record does not hold)
- **SCI after the medical lens (OI-77).** OI-48 and the seventh set's ACTION (4) placed an injury's level in the medical lens; the lens is deleted and `SCI` is still active. T-102 must not retire `SCI` until answered. Ledger: "Correction 2026-11-16 — to the entry that deletes the medical lens".
- **`terms.domain = 'medical'`** (8 live terms, search vocabulary): reached by "medical codes" or not? Kept. Files: none unless reached (`scripts/dbcore.py` NON_QUANTITY_DOMAINS is a different rule).
- **Does the latest adjudication govern (T-074)?** `adjudicate_term` and DR-2026-08-19 §7 say a disagreement is a contest / caps a cell; the writers now treat the latest as standing. No ruling found by `grep -r` over sessions/, decisions/, the ledger. `add-term --from-observation` may still mint a term over a NOT-OURS (prints a NOTE).
- **Does "reached" count an UNVERIFIED source, and does one admission reach every parameter the source holds (T-067)?** OR-8 says neither. Kept as reaching. File: `scripts/migrations/` (a view migration).
- **May a reading be deferred at all (T-079)?** The 2026-09-18 ruling is about citation mining; the task extends it "by extension"; the scan contract says every admitted source is read against the whole parameter list.
- **Should the generic `notes` amend trail stand (T-061)?** The owner's 2026-11-06 schema-shape ruling says a correction appended to a note is data in the wrong cell; OR-3 kept the old text in notes. `amend_extraction` writes `|| date field SET old -> new` for every amendable field.
- **OD-53** (may bodies of law and cost terms be declined), OR-1c / OI-55, OR-5b, `ratified: true` with a status other than ACCEPTED, where the determination machine sits relative to synthesis, and the existence gate's scope: carried from the previous stack's sweep list; unchanged.
- **T-088:** is `retried` or `waived` the disposition of a crash that is a defect to fix; should `emit_batch_sql.py` (no `--session`) capture under CURRENT; should full_text's "NOTHING TO DERIVE" exits be routed; the flag-name rule for the scrub (whole words, because `--tokens`, `--pass-id` are real flags).

## Design questions (tooling; nothing hangs, each is bounded)
- **ci.yml battery jobs pass no base**, so `@BASE@` is `origin/main` in CI; classify computes the base and does not hand it on. File: `.github/workflows/ci.yml` (the task forbade editing a workflow; a CI change cannot be run here).
- **The blocking `migration_reproducibility` compares row counts only**; `--deep` (advisory) compares rows and stored DDL, and does not run on a tooling-only diff. A cache file at its path is trusted on quick_check and six table names (local only).
- **Three checks print no EXAMINED** (`attestation_evidence`, `research_dod`, `research_dod_session`; the last is blocking); their registry entries say so on purpose.
- **A derived row still adds a `derived_calculation` root to `v_value_independence`**; `add-extraction --figure-role derived` is offered at the parser and cannot be completed on the CLI; `v_determination_provenance` shows a NULL `claim_text` for a derived row. Files: `scripts/db.py` (`p_ax`), a view migration.
- **The 30 admissions outside the owed pairs** and the 190 structurally-zero rows (unregistered jurisdictions) are not reported by any reader (`v_coverage_parameter_via_admission` carries `jurisdiction_registered`; `coverage --slug` counts searches by slug). `scope_status` is NULL on all pairs, so Arabic, Bengali, Hindi and Swahili rows are carried (T-101's data task).
- **A source admitted for one parameter reaches every parameter it holds a figure for; summing `sources_admitted` over pairs double counts a source.**
- **`merge-parameter` / `supersede-source` and a deferral**: repaired by following `merged_into` / `superseded_by_ref_id` in the view (see the T-079 repair); `gap_mining.outcome = 'deferred'` is not a fifth kind (0 rows; unproven).
- **The scan contract's arithmetic of "stages" for `gaps` (cross-stage)** from the previous stack stays unmet: `walkability.py` does not count a cross-stage table in each stage it carries.
- **`validate_jurisdiction`'s warning hard-codes "canonical 24"** (base_jurisdictions holds more); a case holds its output identical.
- **Applied DDL comments** in `source_value_extractions` still say "four columns" (`medical_code` among them): an applied migration is not edited; a rebuild keeps the text.
- **Task files that name the old verbs**: T-008 (merged) and T-055 still grep the removed `_AMENDABLE_SVE_FIELDS`; historical, left.

## Repaired in this batch (for the reader of the pull request)
Everything each critic called HIGH and every MEDIUM it called reproducible; the commits are `git log --oneline origin/main..HEAD`, the per-finding accounts are in their bodies.
