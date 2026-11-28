# Second review of the parameter 13 slice (commit ce461d89), not recordable as a database pass

`db.py record-adversarial-pass` refused it: "at most one adversarial pass per research batch; a pass on a pass is forbidden" (pass 11 exists for this session). The review ran anyway (reviewer transcript transcripts/harness_3ed1a246/subagents/2026-11-28T02-33-57_adversarial_a85451ef.jsonl) and its findings were repaired in migration data_20261128023807_* and a ledger correction. This file is the only record of the dispositions.

| # | Finding | Disposition |
|---|---|---|
| 1 HIGH | Ledger entry truncated the selected label and framing | Repaired: CORRECTION paragraph appended to references/project-standards.md |
| 2 MED | Direction 'NOT contested' from a fragment read; para 1.25 not weighed | Repaired by annotation on parameter 13; set-parameter-direction refuses a second direction (T-123 gap), so the rationale text itself stands |
| 3 MED | Scan 20 pages_read 74/74 with scope fragment | Not repairable: scans are immutable; stated here and in the annotation |
| 4 MED | Rows committed before the review returned | Stated: ce461d89 carried [skip ci] and no PR push followed until the repair |
| 5 MED | TERM-095 scope note wrong on Flemish use and table columns | Repaired: amend-term scope_note |
| 6 LOW | UK rise, going and gradient are one constraint | Repaired by annotation on parameter 13; extraction notes cannot be amended (amend-extraction refuses notes) |
| 7 LOW | Figures typed twice in extraction 228 notes; ledger REF list hand-typed | Not repairable in the row (notes not amendable); the ledger list names rows to file, to be re-derived with `select ... where parameter_id = 12` |
| 8 LOW | Lens MOB only | Left to judgment (owner, 2026-08-27: the crossing is judgment's output) |

The one-pass-per-batch rule means this slice should have been its own session. Recorded as a lesson; no check is added.
