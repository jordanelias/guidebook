# Scratchpad — session_2026-08-20-provenance-walk

## What this session did
Adversarial review of workplan/2026-08-20-provenance-walk-execution-plan.md (rev 1), corrections
applied as rev 2, then execution of the walk phase up to the point where it was halted.

## Provenance status — read this before trusting the record
The Phase A PostToolUse hook (plan §4, Phase A) was **not landed**: writing .claude/settings.json
was refused by the harness permission classifier, and the refusal was not routed around. So
`commands.jsonl` does not exist for this session and the command-level provenance the plan calls
for is ABSENT. This is stated rather than papered over — it is exactly the "remembered, not
mechanical" weakness the plan diagnoses, and this session is a live instance of it.

What IS durable:
- retrieval-log/session_2026-08-20-provenance-walk/ — 17 artefacts + manifest.jsonl, each written
  by retrieval_log.fetch() before return, sha256 + bytes + purpose per line. Includes every
  REFUSAL (Cloudflare challenges, an empty Bristol body, a CORE "no available server", an Elsevier
  coredata stub). The refusals are evidence, not noise.
- workplan/2026-08-20-adversarial-adjudication-a18-aut.md — the adjudication, quoting the
  load-bearing findings verbatim.
- correction-register.md (this directory) — the consolidated correction register for rev 1.
- Six subagent reports (4 read-only audits, 1 agonist, 1 antagonist) were produced. Their VERBATIM
  transcripts were written to ephemeral task-output files under /tmp and are NOT preserved; their
  findings are distilled into correction-register.md and the adjudication. Treat those two
  documents as the record, and treat the verbatim reports as lost.

## Canonical DB
sha256 ebab426f54ef45efb76db4c3f461a5ebdc6ce7c2966312b667f55c82168c692b — UNCHANGED throughout.
No migration was emitted. No rows were written. See adjudication §7 for why.

## Next act
Adjudication §8. A search round with the right frame, then a re-grade. Not a determination, and
not apparatus.
