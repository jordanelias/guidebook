---
description: Adversarial pass over work just done — a read-only critic that attacks the claim, then a writer that repairs
argument-hint: "[what to attack — a diff, a batch, a document]"
---

Run the pair. Do not let one model check its own work; that is the failure this
exists to prevent.

**1. Critic.** Launch the `antagonist` agent (Fable, read-only) against: $1

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

**3. Gate before claiming done.**

```
scripts/preflight.sh
python3 scripts/run_checks.py --selftest      # mandatory after ANY rename
```

Report the findings and their disposition. Do not report the critique as the
deliverable — the repair is the deliverable.
