# session_2026-08-19-ratification-and-write-path-fixes

**Purpose.** Read the most recent commit in full, verify what it asserts against the live
repository, and execute the ratified program. The owner ratified OD-1; §3 steps 2 and 3 were then
executed. This is the PR that clears the way for the first research batch.

**Not a research session.** No evidence admitted, no source verified, no synthesis authored, no
migration committed. `user_version` 60 at open and at close. `evidence_sources` 0 at open and at
close. **`sessions/LATEST-RESEARCH` deliberately unchanged** — this session logged no search, and
moving that pointer would aim the blocking `citation_mining_session` gate at a session with no
subjects, which is the exact failure this repository has produced four times.

**`data/guidebook.db` sha256 unchanged across the whole session**, verified after every phase:
`99fb2e58c70af6ff8341357edb513cbc5ab5f1cfd1801d937fe613b3e38b08b9` at open and at close.

---

## 1. Verification before execution

The instrument's load-bearing claims were re-derived from the live repo rather than trusted. All
reproduced: `slugs.status` already permits `PROVISIONAL` with zero rows using it (so §1.4 rule 3
needs no migration); `source_locators` holds 835 rows and lacks all five §6 columns; `db.py:61` set
`journal_mode=WAL` unconditionally; `migrate_db.py` committed before its FK check; the DoD selftest
asserted 12 of 15 rules; `scripts/research/` did not exist. The empty-session gate exits 1 on R1
alone, exactly as §12.1 step 0 predicts.

**One measurement error of my own, caught and corrected in the same session.** My first reading of
the gate's exit code was `tail`'s, not the gate's, because the command was piped. Re-measured
without the pipe. That is this repository's signature failure — a number read from the wrong
place — and it appeared on my first command.

## 2. What was executed (§3 steps 2 and 3, F3–F6 and F9)

Each fix is proved by execution, not by inspection.

| Defect | Fix | Proof |
|---|---|---|
| **F4** — every `db.py` invocation, including pure reads and `--dry-run`, flipped `journal_mode` and rewrote the committed blob | `connect()` no longer sets `journal_mode`; new `readonly=True` opens `mode=ro` with `query_only=ON`; 16 pure-read call sites flipped | Reproduced the mutation against a scratch copy under the old code (hash changed), then showed it unchanged under the new. All 16 sites verified write-free by AST scan first — they are exactly the bare `connect()` calls |
| **F5** — body committed *before* the FK check, so a "rolled back" failure left bad data committed | body, FK verdict and ledger row now commit in one `BEGIN IMMEDIATE` transaction | `migrate_db.py --selftest`, 14 cases. Old path reproduced: 2 bad rows **and** the ledger row committed despite raising |
| **F6** — schema migrations had no wrapper, and `PRAGMA foreign_keys` is a silent no-op inside a transaction | pragmas hoisted and re-issued in autocommit; `user_version` stamped inside the transaction | Verified empirically that the FK pragma no-ops in a transaction and that `user_version` is transactional |
| **F3** — no capture path from a scratch DB | new `scripts/research/emit_batch_sql.py`, both DBs `mode=ro`, FK-ordered walk, additive-only | `--selftest`, 9 cases, including a replay that reproduces the scratch exactly. Rehearsed end to end on the real schema |
| **F9** — R9, R12, R15 implemented since inception, never once observed to fire | seeded; `expected` widened to all fifteen | Selftest prints 15/15. The R7 interaction is stated in the source **and proved**: lowering the R12 fixture below 50 silences R7 and the selftest fails naming it |

A rebuild from migration history under the new runner reproduces the old one exactly — same
`user_version`, same DDL, identical counts across all 66 tables — and runs about 15× faster.

## 3. Two corrections to the record

**(a) The DR's F5 description understates the defect.** It says rollback "discards only the ledger
row". Reproduced against the old code path, the ledger row was **also** committed, because
`conn.commit()` followed the ledger INSERT. That is worse: the migration is recorded as applied, so
a re-run skips it and the FK violation becomes permanent. §12.0's own wording ("leaves bad data
committed") is the accurate one.

**(b) The 2026-08-19 rename left two dangling paths inside the attestation.** The rename commit
recorded a caller sweep of "one file, the attestation". It moved the file and updated the `artifact`
field but not the two `evidence_path` values inside it, both of which named the pre-rename slug and
pointed at files that no longer existed. Corrected here. A caller sweep that stops at the filename
is precisely what CLAUDE.md §0 rule 5 forbids.

## 4. One departure from the instrument, and why

§2.2 prescribes the freeze check as `kinds: [governance]`. **`workplan/**` matches no work kind in
`check-registry.yaml`**, so a commit that only adds a plan classifies to the empty set and a
governance-gated check would never run — the check against new plans would have been silent on
exactly the commit it exists to refuse. Verified by running `run_checks.classify()` on a workplan
path before wiring it, not inferred.

Registered as `kinds: [always]` instead. It is one `git diff` plus one `COUNT(*)`, well under the
~2s bar the registry sets for gating being worth its own cost. The alternative — adding `workplan/**`
to the `governance` kind — would have widened the trigger surface of seven unrelated checks.

The check exempts its own id: §2.5(c) requires it to land in the same commit as the ratification it
enforces, so counting itself would have made the ratifying PR unmergeable on day one.

## 5. State at close, and the next act

`§3` steps 1–3 are done. **Step 4 — the first research batch — is the next act, and nothing remains
above it.** The runbook is §12.1, scope at §12.2 **minimum viable** rather than target: step 7's
enrichment is hand-written this time, and a failed batch of 30 remediates far worse than one of 10.

OD-2 through OD-12 remain **open**. Nothing gated behind them was executed — in particular no
`items` archival, no `jurisdictional_values` re-key, no `source_locators` widening, and no cull.

**The freeze is live from this commit.** It expires by its own terms at `evidence_sources >= 1`.
The next artifact this project owes is a search log, not a plan.
