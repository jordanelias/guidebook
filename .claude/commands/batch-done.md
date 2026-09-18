---
description: The gate that decides whether a research batch is actually finished
---

Never claim a batch is done from your own reading of it. Run the gate the
SessionStart contract names:

```
python3 scripts/audit/research_batch_dod.py --session "$(cat scratchpad/CURRENT)"
```

**The session id is the bare stem in the DB and carries `.md` in pointer files.**
Wrong form scopes the gate to zero rows and every rule reports PASS over an empty
subject — green, and meaningless.

If it fails, the batch is not done. Fix the rows, re-emit, re-run. Do not
baseline the failure away: `governance/research-contract-baseline.json` ratchets
DOWN only, and raising a count there forgives fresh violations invisibly.

When it passes, confirm the corpus posture has not regressed:

```
python3 scripts/audit/research_batch_dod.py --all
```

Then commit the scratchpad and the agent transcripts (`scripts/preserve_transcripts.py`)
— a read-only subagent writes nothing at all, so its entire workings live in
ephemeral container storage until they are copied out.
