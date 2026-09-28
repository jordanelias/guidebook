# Session 2026-09-28: DR-2026-09-26 phase 2b — connections_produced retires, GAP-053 fixed

**Session id:** `session_2026-09-28-phase-2b-connections-produced-retirement` (branch
`claude/research-batch-apparatus-fnnd5b`). Tooling session — no research batch run, no
row written to any of the 2026-08-19 RULE's eleven named research tables. The one data
change is bookkeeping: closing GAP-053 and, twice, correcting the closure's own text.

## Why this session ran

The user first asked whether all apparatus required for the next research batch (batch
21) was built. Orientation found DR-2026-09-26 v2 (RATIFIED 2026-09-27) not fully
constructed: phases 0/1a/1b/1c/1d/2/2-data were merged (PRs #159-#163), but phase 2b —
`citation_mining.connections_produced`'s retirement, named by the DR's own §7 sequence
table as the last gate before phase 3 (batch 21) may open — was not started. The user
then asked to build it.

## What this session built

1. **Migration 099** rebuilds `citation_mining` (migration 067's own precedent) to relax
   `connections_produced`'s `NOT NULL DEFAULT '[]'`, so a retired writer can leave it
   NULL instead of a value every reader has read as "found nothing."
2. **`log_mining`'s writer retirement**, then a second pass after an adversarial finding.
   The first cut kept `--connections` as an accepted-but-discarded argument, reasoning it
   still proved a call "did something." An adversarial pass caught that as the exact
   anti-pattern the function's own `doi`-removal precedent names: validating a value,
   using it to satisfy a refusal, reporting it as logged, and persisting none of it.
   `--connections` is now REMOVED (signature, CLI flag, and the dispatcher's JSON
   parsing) rather than kept-and-ignored. A pass that ran now always uses `--notes`,
   whether it found something or nothing.
3. **Migration 100** adds `updated_at`/`updated_by_session` to `search_executions` and
   `search_candidates` (GAP-053: `adversarial_pass_audit.py` scopes a session's subject
   rows by matching every `_by_session` column on the RULE's eleven tables, and these two
   carried only `created_by_session`). Five writers now stamp both on every real write —
   `amend_search`, `reattribute_candidate` (GAP-053's two named specimens), plus
   `resolve_candidate`, `link_admission` and `unlink_admission`, found by the same
   adversarial pass to UPDATE the same two tables and be equally invisible without it.
4. **GAP-053 closed CLOSED-FIXED**, then corrected twice more (see Deviations) — a
   numeric claim in the original filing and in this session's own migration 100 header
   ("the other 9 of the RULE's 11 tables already carry the pair") was wrong; the true
   figure, re-derived, is 8 of the RULE's other 9 tables (`evidence_population_match` has
   neither column).
5. **Reader sweep and prose corrections** across `governance/pipeline-contract.yaml`,
   `architecture/sqlite-data-layer.md`, `scripts/dbcore.py`, `schemas/search_execution.py`,
   `scripts/tests/test_db_integrity.py`, and the `citation-miner`/`bibliography-compiler`/
   `adversarial-research` skills — some done as part of the initial build (per the DR's
   own named reader list), several more found and fixed by the adversarial pass (a false
   attribution of migration 100 to the retirement it has nothing to do with; a stale
   "13 of 25 bare integers" claim that direct query — and then `git log -S` against its
   introducing commit — shows was never demonstrably true, not merely gone stale; a dead
   script's spec still teaching `connections_produced='[]'` as a live signal).
6. **Two `SUPERSEDES`/`BY` markers** (RC3's mechanism, built in an earlier phase of this
   same DR) recording that two `scripts/db.py` comments arguing against ever adding
   `search_candidates.updated_*` are superseded, for a different reader (a machine
   audit, not the human narrative those comments addressed), by GAP-053's ratified fix.
   Both verified green against `supersession_backpointer_audit.py` (`EXAMINED: 4`).

## Process followed

`/code-review`, then four parallel `/simplify` agents (reuse, simplification, efficiency,
altitude), then a comprehensive adversarial critique — matching the owner's 2026-09-27
ratification instruction for this DR's construction ("...a comprehensive adversarial
critique that sweeps and propagates code implications then audits both top-down holistic
and bottom-up granular requiring handshakes to resolve all issues"). Each pass's findings
were verified (not taken on faith) and either fixed or explicitly skipped with a stated
reason. No pass was recorded to `adversarial_passes`/`adversarial_findings`: this diff
writes no row into any of the RULE's eleven tables, so `adversarial_pass_recorded`
correctly reports NOTHING-IN-SCOPE for this session, and forcing a DB record for a
code-quality review the mechanism was not built to scope would itself be the spurious-
apparatus pattern CLAUDE.md warns against.

## Deviations and honesty about this record

- **`research_tooling_separation` (RC6, advisory) FAILS on this changeset.** Closing
  GAP-053 (a data write) rode in the same PR as the schema/tooling build, and the two
  numeric corrections to that closure did too. Named, not hidden, on the immediately
  prior session's own precedent for the identical trade-off
  (`sessions/session_2026-09-27-repo-data-status-check-ht2rsn.md`, its own "Deviations"
  section).
- **This session's own first migration-100 header was wrong, and so was the commit
  message that shipped it.** "The other 9 of the RULE's 11 tables already carry the
  pair" named only 8 while claiming 9, in the same paragraph that excludes the 9th
  (`evidence_population_match`) for lacking both columns — an internally inconsistent
  claim this session wrote and did not catch itself; caught by the adversarial pass.
  Fixed in migration 100's own text (unmerged, comment-only, DDL unaffected) and via a
  second `amend-gap` correction on GAP-053. The commit message that first shipped the
  wrong figure (`02c5ec5`) is not editable without rewriting pushed history, and was not
  rewritten; this record and the follow-up commit are where the correction lives.
- **The same commit's rebuild-reproducibility claim overstated its own finding.** It said
  a full `--rebuild` reproduces every table "except `pipeline_runs`" — but this session's
  own `migration_reproducibility_deep` run, minutes earlier, had already shown
  `evidence_sources` diverging too (the scheduled `source-verification` cron's known,
  pre-existing, CLAUDE.md-documented write-on-a-timer). The sentence contradicted
  evidence this session had already produced. Not caused by this diff; still misstated.
  Left as a commit-message error, corrected here.
- **One `SUPERSEDES`/`BY` quote is sourced from a session's relayed account, not a
  verbatim owner quote**, inside a ledger entry whose own owner-quoted words are
  "Execute as ratified? Proceed all." The adversarial pass flagged this
  `WITHHELD-FOR-OWNER` as doctrinal. OQ-4's ratified answer ("May a session write
  SUPERSEDES lines for a ruling it relays in its own words? ... Yes, with the relayed
  ruling quoted back to you in the PR") appears to cover exactly this case, so nothing
  was changed — flagged here for the owner to overrule if the reading is wrong.
- **The `--connections` removal is a second design pass, not the first-cut answer.**
  The first cut (accept-and-discard) was wrong; recorded above and in `log_mining`'s own
  docstring, not smoothed over.

## What is still open

- Phase 2b's own DR text (§7's sequence table) is unedited — this session did not mark
  it done in place, matching the observed convention that phases 0 through 2-data were
  also never marked in that table despite being merged; completion is tracked here and
  in the ledger/commit history instead, not by editing the ratified DR.
- Phase 3 (research batch 21) is now unblocked by this session's own reading of the
  DR's sequence table (phases 1-2b merged is its stated precondition), but that reading
  is this session's, not a fresh confirmation — the next session opening batch 21 should
  re-verify rather than trust this sentence (rule 7a).
- `research_tooling_separation`'s FAIL and the two commit-message errors above are named
  here for whoever reviews this PR; none blocks merge on its own terms (both are
  advisory / historical-record issues, not correctness defects in the shipped code).

## State at close

- Branch: `claude/research-batch-apparatus-fnnd5b`.
- New migrations: `099_citation_mining_connections_produced_retires.sql`,
  `100_search_execution_candidate_update_stamps.sql`, and two data migrations closing
  and then correcting GAP-053.
- `scratchpad/CURRENT`: `session_2026-09-28-phase-2b-connections-produced-retirement`
  (folder created to match, at session open, before any writer call).
