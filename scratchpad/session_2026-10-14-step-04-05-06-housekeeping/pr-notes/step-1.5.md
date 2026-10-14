# PR body notes, step 1.5 (scheduled DB-writing workflows) -- branch stack/1.5-scheduled-workflows (stacked on 1.4)
Deleted resolve-dois.yml, verify-urls.yml, resolve_dois.py, verify_urls.py, test_url_verifier.py, test_verification_pipeline.py + 2 registry entries.
Migration drop_scheduled_run_tables drops pipeline_runs (6 rows quoted in migration header and commit) and url_verification_runs (0).
NEXT BOT FIRES if not merged first: Monday 2026-10-19 06:00 UTC (resolve-dois); 2026-11-01 06:00 UTC (verify-urls). Each commits the blob and conflicts with any open DB PR. Merge 1.5 early.
Edits: test_db_integrity E02/E03/F01-F04; stage-map (2); machines.yaml M02.t2; migration_reproducibility EXEMPT_TABLES -> evidence_source_authors only; contract reproducibility-invariant text;
dbcore.NOT_CAPTURED; research_batch_dod (R10b keeps firing, rationale reworded); CLAUDE.md rule 3 timer paragraph deleted (owner merge); C-029 deleted; 21 atoms re-anchored.
Owner items: research-contract.yaml:218 and the SessionStart hook in .claude/settings.json still say the cron claims the NULL-status pool (must be edited together; hook is the owner's).
Not cleared: evidence_sources / evidence_source_authors divergence (1.5a-1.5c).
Process note: a forward-fix commit (83275d5) removes three 1.6 doc files that a `git add -A` swept into the 1.5 merge commit; net diff is unaffected.

## After the adversarial pass (dc858c4)
F5 provenance sentence corrected in migration 110 (four bot commits; two rows first appear at root commit 55ae5c1). F8 REJECTED (divergence owned by 1.5b/1.5c; deep check stays red).
F10: owner decision #5 (the cron) is closed by R2 and the 2026-10-14 delegation; nothing else names it closed.
