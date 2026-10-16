# session_2026-10-16-r29-compensating-revert

Plan step 1.5b (RULINGS R29 as amended by R49(a)): put `evidence_sources` and `evidence_source_authors`
back to the migration chain's state after the scheduled job that rewrote them was deleted (step 1.5).
A data-only compensating revert through the sanctioned path. Orchestrating session:
`session_2026-10-14-step-04-05-06-housekeeping` (its `scratchpad/CURRENT`; this stem exists because the
rows and the migration are stamped with it).

## Reproduce

1. `python3 scripts/migrate_db.py --rebuild $S/chain.db` at the parent of the migration.
2. `python3 r29_diff.py data/guidebook.db $S/chain.db` prints the divergence (4 rows, 27 values, 24 author
   rows each side); `r29_prep.py <blob> <chain> <scratch> <session>` sets the scratch from the chain's
   values, read not typed, and stamps the four rows with `dbcore.upd(session)`.
3. `python3 scripts/research/emit_batch_sql.py --scratch <scratch> --allow-delete evidence_source_authors --out batch.sql`
   (step 1.5a's replay-safe capture), then `emit_data_migration.py --session <stem>.md --input batch.sql`,
   then `migrate_db.py --session <stem>`.

## Adversarial pass

One read-only pass (a Fable-class reviewer, the `antagonist` agent) over steps 1.5a to 1.5c, recorded with
`db.py record-adversarial-pass` in `data_*_r29-adversarial-pass-record`. Its report is the last message of
`transcripts/harness_f366a537/subagents/2026-10-16T00-18-10_other_a18bef3f.jsonl`. Findings 2, 3, 5, 7, 9
and 10 are tooling or prose defects, repaired or stated in the step 1.5a and 1.5c repair commits; they are
not dispositioned in the database because `dispose-adversarial-finding --disposition REPAIRED` accepts only
a data-migration ref. Findings 1 and 4 (this session had no record, and the gate examined nothing because
`CURRENT` names the orchestrating session) are repaired by this folder and the pass record. Finding 6
(`sqlite_sequence` for `evidence_source_authors`: 258 on the blob, 244 on the chain) is harmless because
every migration carries explicit ids, and is not reverted. The pass stays open (RULINGS R38(1), LED-192).

Run `python3 scripts/audit/adversarial_pass_audit.py --session session_2026-10-16-r29-compensating-revert`
to see the gate examine this batch's rows; with `CURRENT` naming the orchestrating session it examines none.
