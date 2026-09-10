# B5(b) — the blind scope derivation, and the proof it was blind

**Recorded 2026-09-10.** Preserved out of ephemeral container storage into the repository,
where the migration it justifies can be read beside it. Nothing here is reconstructed from
memory; every line names the bytes it came from.

## 1. Why this file exists

`scripts/migrations/data_20260910071239_2026-09-10-project-status-overview.sql` writes five
`evidence_sources.scope` values and each one carries the sentence *"Derived before the stored
tier was read."* On its own that is **a self-assertion with no artefact behind it** — the
precise failure class `scripts/research/retrieval_log.py` was written to make impossible
(CLAUDE.md §5(c): *"Verification must leave an artefact"*).

The artefact existed. It was written to
`/tmp/claude-0/…/scratchpad/b5/DERIVED-BEFORE-TIER.txt` — ephemeral container storage that a
fresh clone does not inherit — and the migration shipped without it.

It is now `scratchpad/pr-131-project-status-overview/b5-DERIVED-BEFORE-TIER.txt`,
**copied byte-for-byte**, sha256
`05a5b10185ed327d9025ec84aa97a885b386dba78cff93bd50645ac51c2c0897`, mtime preserved at
`2026-09-10 07:07`. Its body is independently confirmed byte-identical to the heredoc that
wrote it, at line 118 of
`transcripts/harness_292c6e38/subagents/2026-09-10T07-02-23_antagonist_aa753316.jsonl`
(tool_use `toolu_015ag1uQq5KVSVmBAksMySYP`, timestamp `2026-09-10T07:07:21.612Z`), so the file
and the transcript corroborate each other rather than either standing alone.

## 2. The sharper problem this file has to answer

**Every row the migration wrote carries exactly the value the circular back-fill shortcut
would have produced.** The four rows where the honest derivation *differs* from
`expected_scope_from_tier()` are precisely the four that were left NULL.

So the independence evidence is carried entirely by rows that were **not** written. To a
reader who has only the migration, it is observationally indistinguishable from the shortcut
it was designed to avoid. The reveal below is the only thing that separates them, and until
2026-09-10 it lived nowhere in the repository.

## 3. The reveal, verbatim

Locked derivation timestamp `2026-09-10 07:07:22 UTC`; tiers revealed `2026-09-10 07:10:18
UTC`, ~3 minutes later. Captured from the tool_result at line 176 of the transcript named
above (the command is the tool_use at line 175).

```
### DERIVATION FILE TIMESTAMP (locked before this read):
2026-09-10 07:07:22 UTC

### NOW REVEALING STORED TIERS ###
2026-09-10 07:10:18 UTC
REF         type       stored tier  stored scope  MY DERIVED SCOPE  derives to  VERDICT
--------------------------------------------------------------------------------------------------------
REF-00784   clinical   1            None          None              -           GAP — payload does not establish design; scope stays NULL
REF-00971   clinical   3            None          high_control      1           *** CONTRADICT: derives T1, stored T3 ***
REF-00972   clinical   3            None          high_control      1           *** CONTRADICT: derives T1, stored T3 ***
REF-00973   clinical   1            None          high_control      1           AGREE
REF-00974   clinical   1            None          high_control      1           AGREE
REF-00975   clinical   3            None          lower_control     3           AGREE
REF-00976   clinical   3            None          None              -           GAP — payload does not establish design; scope stays NULL
REF-00977   sr_meta    2            None          intrinsic         2           AGREE
REF-00978   co1        1            None          intrinsic         1           AGREE

Cross-check — what expected_scope_from_tier() would have BACK-FILLED from the stored tier
(the shortcut this task forbids; shown only to prove the derivation was not that):
  REF-00784  backfill_would_give=high_control    my_derivation=None
  REF-00971  backfill_would_give=lower_control   my_derivation=high_control
  REF-00972  backfill_would_give=lower_control   my_derivation=high_control
  REF-00973  backfill_would_give=high_control    my_derivation=high_control
  REF-00974  backfill_would_give=high_control    my_derivation=high_control
  REF-00975  backfill_would_give=lower_control   my_derivation=lower_control
  REF-00976  backfill_would_give=lower_control   my_derivation=None
  REF-00977  backfill_would_give=intrinsic       my_derivation=intrinsic
  REF-00978  backfill_would_give=intrinsic       my_derivation=intrinsic
```

**Read the two blocks together.** Four of nine derivations disagree with what the stored tier
would have handed back, and all four are among the rows the migration declined to write. That
disagreement is the whole of the independence evidence. It is not visible in the DB, because
NULL records no derivation; it is visible only here.

## 4. Two characterisations in that artefact are wrong, and are corrected elsewhere

The artefact is preserved **as written**, errors included — it is the historical record of what
was derived at 07:07, and editing it would destroy the thing it proves. Two of its lines are
corrected on 2026-09-10, in `workplan/2026-09-10-b5b-scope-owner-escalation.md` and in the
compensating data migration of the same date:

- **REF-00784 "GAP … Design not established by any payload in hand."** True of the payloads and
  **false of the repository**, which has recorded the design since 2026-07-20. See §1 of the
  escalation note.
- **REF-00976 "Design not established."** True of the payloads, while
  `evidence_population_match` already describes the design from an abstract that is in no logged
  payload. See §3 of the escalation note.

Both corrections change what the owner is told. Neither changes the action: `scope` stays NULL
on both rows and no tier moves.
