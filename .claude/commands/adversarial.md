---
description: Adversarial pass over work just done — a read-only critic that attacks the claim, then a writer that repairs
argument-hint: "[what to attack — a diff, a batch, a document]"
---

Run the pair. Do not let one model check its own work; that is the failure this
exists to prevent.

**0. No agent-launching tool?** Say so in your handback and stop. Do not run the
antagonist's checklist yourself and call it a pass — batch 20 did exactly that ("the
authoring subagent had no agent-launching tool, so it ran a self-administered pass")
and it "missed every one of the independent pass's findings." A self-administered pass
is not a pass, and `db.py record-adversarial-pass` refuses one whose reviewer and
author transcripts are the same file (RC4).

**1. Critic.** Before launching it, capture `SUBJECT_COMMIT="$(git rev-parse HEAD)"` — the
sha the reviewer will actually read. Capturing it AFTER step 2's repair names the wrong
commit (the repaired state, not what was reviewed). Launch the `antagonist` agent
(Fable, read-only) against: $1

It attacks the claim. It does not summarize the work, and it does not propose
the repair — proposing a fix is how a critic talks itself into accepting the
thing. Require of it:

- every finding names the artifact and the line, and states the failure case
- a finding that a gate "should" have caught is checked against whether that gate
  had a SUBJECT — a check that passed having examined nothing is this
  repository's most-produced defect (CLAUDE.md §5a)
- every count it cites is one it just computed
- `[NULL: <scope> — examined, nothing found]` where it found nothing, rather than
  silence

**2. Adjudicate, then repair.** Take its findings one at a time. For each: confirm
it against the artifact yourself, then fix or reject with a reason. A finding you
cannot reproduce is not a finding — say so and move on.

**3. Record the pass (RC4).** Once the critic's transcript is committed (rule 6) and
carries the closing ` ```json adversarial-findings ``` ` block, on a SCRATCH copy of the
DB (CLAUDE.md §4 — this writer, like every db.py subcommand, refuses to open the
canonical DB read-write):

```
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py record-adversarial-pass \
  --subject-session "$(cat scratchpad/CURRENT)" --subject-commit "$SUBJECT_COMMIT" \
  --reviewer-transcript transcripts/<...>/<critic-transcript>.jsonl \
  --author-transcript transcripts/<...>/<your-own-transcript>.jsonl \
  --session "$(cat scratchpad/CURRENT)"
```

The row then travels the ordinary write path (emit_batch_sql → emit_data_migration →
migrate_db) with the rest of this batch's rows — it is research data (RC6), not tooling,
and ships in the batch's data migration, never hand-applied to the canonical DB.

Then, for each finding: `db.py dispose-adversarial-finding --finding-id N --disposition
REPAIRED|REJECTED|PROVISIONAL-DISPUTED|OWNER-RULED [--ref ... | --reason ...]` — REPAIRED
names the data migration path that fixed it; OWNER-RULED names the exact ledger quote,
occurring once. Finally `db.py close-adversarial-pass --pass-id N --session ...`, which
refuses until every lens is covered and at least one row is SURVIVED. **Never run it on
pass 1:** the owner ruling of 2026-09-27 (second, `references/project-standards.md`,
ACTION (2)) holds pass 1 OPEN. Pass 2 was left open by its own session and the
process-gap plan approved 2026-10-01 keeps it open. Nothing refuses either; you are the
gate. A finding admitted only on the database file is closed but printed as REPORTED:
the database is not an artefact of attack.

**4. Gate before claiming done.**

```
scripts/preflight.sh
python3 scripts/run_checks.py --selftest      # mandatory after ANY rename
```

Report the findings and their disposition. Do not report the critique as the
deliverable — the repair is the deliverable.
