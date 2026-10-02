---
description: The gate that decides whether a research batch is actually finished
---

Never claim a batch is done from your own reading of it. Run the gate the
SessionStart contract names:

```
python3 scripts/audit/research_batch_dod.py --session "$(cat scratchpad/CURRENT)"
python3 scripts/audit/adversarial_pass_audit.py --session "$(cat scratchpad/CURRENT)"
python3 scripts/audit/search_log_completeness.py --session "$(cat scratchpad/CURRENT)"
```

The second line is RC4: it FAILs if this session wrote to any of the 2026-08-19 RULE's
research tables and no closed adversarial pass names it. Run it on `CURRENT`, not via
`run_checks.py --battery research` — that battery's other session-scoped checks
(`research_dod_session`, `author_fidelity`, `citation_mining_session`) are still pointed
at `LATEST-RESEARCH`, which names the PREVIOUS session for the whole life of this one.

The third line is I5, also on `CURRENT`: it reads the WebSearch/WebFetch ledger the
harness hook wrote and FAILs a WebSearch query that no `search_executions.query_text` of
this session contains — a search you ran and did not log (R8). Log it with
`db.py log-search --backfill 1`: the row is a reconstruction, not a log made as the search
ran, and the `--prior-expectation` it still requires is written after the results, so it
is post hoc and must say so. Its REPORTED lines (unpersisted WebFetch URLs, bare curl/wget
hosts, and web rows logged with no web line on the ledger — a hook that may not have
fired) belong in the session record; they do not fail, and a NOTHING-IN-SCOPE verdict does
not clear them. It witnesses WebSearch and WebFetch only: a search run through an MCP tool
(Consensus, PubMed, Scholar Gateway) leaves no line, so a PASS says nothing about those.

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
