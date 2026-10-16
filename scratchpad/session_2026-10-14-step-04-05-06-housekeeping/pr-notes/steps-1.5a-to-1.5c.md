# PR body notes, steps 1.5a, 1.5b, 1.5c (the R29 divergence), built after the 1.5 PR was open

These three plan steps were missed in the first pass: my earlier "not built" notes did not name them.
Branches (all pushed): `stack/1.5a-replay-safe-capture` -> `stack/1.5b-r29-compensating-revert` ->
`stack/1.5c-authors-not-exempt`, each on top of `stack/1.5-scheduled-workflows`. Open as three PRs in
that order, after 1.5 (#180) merges: 1.5a tooling, 1.5b data only (rule 10), 1.5c tooling. 1.6 onward
are not in this lineage; each later stack branch that changes the blob will need one
`migrate_db.py` re-apply after merging main (the 1.5b and pass-record data migrations).

Net-negative exception, 1.5a: `git diff --shortstat origin/main -- scripts ...` rises (adds ~85 lines, 45 of
them selftest fixture, replaces none); it is the precondition of 1.5b, whose emitted file would otherwise
need hand-added SQL (CLAUDE.md section 4, rule 10). 1.5c is net-negative in the same file (+15/-33).

1.5b loses, to state in the PR: 27 payload-backed values and one ORCID (REF-01007 position 2).
Owner items: DR-2026-05-28 option 3a has no supersession pointer (a ratified decision; needs an
attestation); the registry note on `migration_reproducibility_deep` is deleted by 1.8; the adversarial
pass is recorded and open (list its limits: REPAIRED accepts only data-migration refs).
At PR time for 1.5b, extract and run `context_map --check` and `migration_reproducibility --deep`.
