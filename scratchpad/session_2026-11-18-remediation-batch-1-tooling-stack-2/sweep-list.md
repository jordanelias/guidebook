# Sweep list of the second tooling stack (owner instructions 2026-11-15 sweep, 2026-11-18 "tooling only, one PR")

One section per task: what the critic found and the executor's repair commit repaired, then what is NOT repaired and why (a design question, an owner question, or a limit), each with the file that would change. Derive every count; none is typed here.

## T-028 (commit 4dc99ce3; critic repairs in the commit after it)

Repaired (the executor was sent the list): seed matches reach the writers' output; `v_term_names` ordering and origin rule (a compensating migration); the OD-68 cross-language regressions the tests could not catch; the NOT-OURS screen on `add-term --first-form`; `rename-term --from-form` language; the untested typed exclusion; the unread `near_screen_not_run`; `alias_provenance_audit`'s swallowed `OperationalError`.

Not repaired:
1. **OWNER'S: does the base point into the evidence stage?** `term_label_picks.observation_id` is a new foreign key from a base table into `observed_terms` (evidence, by `governance/stage-map.yaml`), and `add-term --from-observation` holds a base form `unrecorded` until its quote verifies in a saved file. The owner's statement of 2026-11-06 (seventh) (`references/project-standards.md`, "the base grounds itself") says the base "does not point into the evidence stage" and waits on no "quote being verified in a saved file"; its ACTION (3) keeps the observation verbs. The task file and its design specified both, so the executor followed them; whether they are superseded is the owner's (CLAUDE.md rule 0). Files that would change: `tasks/T-028-design.md` and `tasks/T-028-concept-identity.md`.
2. **The judge is any non-blank string** (`x`, `Claude` and a model id were all accepted) and the schema has no blank CHECK on `term_label_picks.judge` or `reason`; only the writer refuses a blank. A named-judge vocabulary is a design question for `tasks/T-028-design.md`; a CHECK would need a table rebuild.
3. **The junction remap has no committed proof**: the canonical `search_execution_forms` holds no row, so `--rebuild` and `migration_reproducibility --deep` examine nothing about it. The critic proved it on fixtures (eight rows remapped to the same key); a committed test needs a fixture database at the parent schema.
4. **No attested alias exists** (`select count(*) from term_aliases where attestation in ('instrument','other_source')`), so the base screens have no live subject: every OD-68 and E4 screen is proven on fixtures only, until T-107 attests forms from instruments.
