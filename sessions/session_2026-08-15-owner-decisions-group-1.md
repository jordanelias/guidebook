# session_2026-08-15-owner-decisions-group-1

**Purpose.** Present the owner-decision queue from `workplan/2026-08-14-remediation-workplan.md` §7
in plain English, then execute what the owner ruled. Group 1 of four: the two enum vocabularies, the
Tier-1 retirement batch, and the required-check set.

**Not a research session.** No evidence was admitted, no source verified, no synthesis authored.
`sessions/LATEST-RESEARCH` is therefore unchanged and still points at
`session_2026-07-26-energy-conservation-rest-points-seating-b3.md`.

---

## 1. What the owner decided

**Decision 1 — the status vocabulary.** Ruled in five parts across two messages. Eight words:
`ACTIVE`, `PROPOSED`, `DEFERRED`, `RESOLVED-EVIDENCE`, `RESOLVED-CONSENSUS`, `UNRESOLVED`, `CLOSED`,
`RETIRED`. `RETIRED` replaces `WITHDRAWN`; `PROPOSED` absorbs `PROVISIONAL`; `ACTIVE` replaces `OPEN`
("only one survives"); the two `RESOLVED-*` words are reserved for direct evidence or claims directly
derived from it, with `CLOSED` for anything else that finishes; `DEFERRED` stays distinct because it
counts the times something was passed over. → **D-0161**, migration 058.

**Decision 2 — the Tier-1 retirement batch.** Approved whole. → **D-0162**, migration 059.

**Decision 3 — the required-check set.** Not executable from here: no tool in this session exposes
branch-protection settings. Left with the owner, with the recommendation and its three traps written
out in the brief.

## 2. What I decided, and flagged as mine

- **`SUPERSEDED` retired on a reading, not an instruction.** The ratified list did not name it. The
  reading was put to the owner before implementing and implemented in the same turn: zero rows use
  it, and `decisions.supersedes` carries the relation on all 160 rows. One line to reverse in each
  layer. Logged as a deviation in the D-0161 attestation.
- **One shared list on both tables** rather than per-field subsets, on reversibility grounds.
- **`MODE-S-ONLY` → `UNRESOLVED` is not a pure rename**, so the meaning it carried was moved rather
  than dropped — the Person-Mode handoff lives in `mode_s_trigger` / `unresolvable_residual`, and the
  five swept matrices say it in words beside the status.

## 3. What I did not do

- **The deferral counter.** Offered, not taken up. No column added — building it unasked would be a
  schema decision made by the implementer.
- **The `mode_s_trigger` field rename.** Still retired vocabulary. A structural rename with its own
  caller sweep and Change-Order; the ruling was about status values.
- **Anything in Groups 2–4**, Track B/C/D, or the remaining owner decisions.

## 4. Errors made and caught, in sequence

Recorded because this repo's audits keep finding that the corrections matter more than the results.

1. **A contaminated baseline.** `git stash` without `-u` leaves untracked files, so migration 058
   stayed on disk while the database reverted, and the reproducibility gate compared a v58 replay
   against a v57 database. It reported a blocking failure that did not exist. Re-run with `-u`; the
   real baseline was identical to the working tree.
2. **`model_routing: opus/200/implement`** — refused by `decision_capture` C1, which enforces a
   grammar where `implement` is not a legal third segment. Because nothing had been committed, the
   data migration was rolled back and re-emitted rather than fixed forward: a compensating migration
   for a value that never reached history would be noise in an append-only ledger.
3. **L01 caught my own dual-store divergence** — the DB moved D-0139 to `PROPOSED` while the YAML
   still said `PROVISIONAL`. This is exactly what last session widened L01 to catch, one session
   later, against the session that widened it. Reconciled toward the DB per `CLAUDE.md` §9-5.
4. **Two call sites the sweep found that I had not predicted:** `scripts/validate_conflicts.py`
   (plural — a second registered validator) and `audit_consolidator.py`, where "resolved" was defined
   as *not* `UNRESOLVED`, so widening the vocabulary would have silently counted `ACTIVE`, `PROPOSED`
   and `DEFERRED` conflicts as resolved.
5. **Two false claims shipped into the record, found only on the owner asking me to re-derive.**
   Neither was caught by any gate — all five commits were green and pushed.
   - **`decisions.supersedes` does not carry the successor relation.** I wrote that "every one of
     the 160 rows populates it". It is `'[]'` on all 162 and has never been written to; the inverse
     column `predecessors` is populated on 51. The check that produced the claim tested
     `supersedes != ''` — and `'[]'` is a non-empty *string*. **I queried string emptiness and
     reported array population**, which is the same shape as the failure `CLAUDE.md` §10 warns about
     and the same shape as the F4 error one session earlier (grepping for a name, concluding about a
     behaviour). This weakens the stated grounds for retiring `SUPERSEDED`; the surviving ground is
     that no row ever used the status.
   - **The Mode-S retirement is dated 2026-07-13, not 2026-07-21**, and its authority is Item V of
     `RATIFICATION-PACKAGE-2026-07-12`, ratified in full (`RATIFICATION-RECORD-2026-07-13`, A5) —
     not a `[NEW — DR-gated]` proposal section of `evidence-architecture.md`, which is what I cited.
     **The corrected fact is worse than the claim it replaces.** Item V named its own implementation
     — *"96 files; one real data migration: `conflicts.status` CHECK"* — and that migration was never
     run. A ratified decision enumerated its single step and did not take it, for a month, until 058.

## 5. State at close

| | |
|---|---|
| Schema | `user_version` 59 |
| Decisions | 162 rows, both stores in full-field agreement (L01) |
| `--all` | 43 green, 16 nothing-in-scope, 6 advisory failures, **0 blocking** |
| Baseline comparison | identical to a clean `origin/main` — same six advisory failures, none added, none cleared |
| Reproducibility | shallow and `--deep` both PASS |

**A number that rose for no good reason, stated so it is not read as progress:** green went 43 → 46
mid-session and back to 43. `attestation_presence`, `_schema` and `_verdict` are changeset-scoped, so
they stop being vacuous whenever the immediately preceding commit happens to carry an attestation.
They were fed, not fixed.

## 6. Next

Group 3 — the six prototyped schema migrations, including the determination→claim edge. It is the
one whose cost grows as soon as content lands. Then Group 2 (the two live parity divergences and the
third write path), then Group 4 (jurisdiction scope, the `cross-population` term, the PI paste, and
the 28 item names that state their own answers).
