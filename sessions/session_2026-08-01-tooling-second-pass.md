# Session — Tooling second pass: the apparatus audits its auditor

**Date:** 2026-08-01
**Branch:** `claude/resume-infrastructure-work-zvl5ft`
**PR:** #76
**Doctrine SHA:** `0f2f525`
**Kind:** tooling / governance. **No content, no synthesis, no DB writes, no migrations.**

## Task

"Resume all ongoing infrastructure work… Ensure focus on code, hooks, scripts, CI. Work with
regular adversarial reviews, crawlers with logs and executing pipeline traces in all
direction."

This picks up the task list left by `session_2026-08-01-ecosystem-tooling-consolidation.md`.

## Method

Four read-only audits ran in parallel — schema-drift ownership, quarantine triage, an
adversarial hunt for silent no-ops in the new CI apparatus, and a DATA-vs-TOOL triage of the
red `test_db_integrity`. **Every conclusion each of them reached was re-verified here before
being acted on**, and that mattered: two of my own probes were wrong in the same way twice
(`$?` after a pipe reads `tail`'s exit code, not the command's), and one audit reported an
exit code I had to re-measure to correct.

The governing instruction was the previous session's own: **re-run, don't re-read.**

## What was found

The previous session's headline finding (F1) was a CI condition that could never evaluate
true, so three jobs never ran on any PR in the repo's history. This session hunted the *next*
bug of that class, in the code that session had just written. It found four, plus two more in
the older apparatus. **Every one was confirmed by execution.**

- **F7 — docs-only diffs crashed three CI jobs and ran nothing.** A diff matching no work kind
  becomes `--kinds ""`, which `run_checks.py` tested for *truthiness* — so an empty kinds
  string was indistinguishable from an absent one and fell to `ap.error()`, exit 2. The
  selector was never wrong; the selftest asserts *"empty kind set selects exactly the
  always-on checks"* and passes. **The bug was in the entry point, which is why a selftest
  exercising internals could not see it.** New `C6` cases drive the real command line.
- **F8 — every push run of `ci.yml` on `main` was red for a fake reason.** No merge or bot
  exemption in `check_commit_msg.py`, while every human integration on `main` is a merge
  commit. Six of six recent push runs red; every PR run green. The script also took no
  arguments at all, so the `--selftest` the record credited it with silently re-checked HEAD
  and printed PASS.
- **F9 — the blocking doctrine gate was skipped, not evaluated, on every push to `main`,**
  because it runs after F8's failing step in the same job and GitHub skips later steps after a
  failure.
- **F10 — the gate enforcing "never write the DB directly" compares seven scalars.** An
  `UPDATE` changes no `COUNT`, so value edits are invisible, as is everything in the other 55
  tables. Demonstrated by tampering with a scratch copy — rewriting a row's `tier` and title,
  and inserting a forged `stated` cell — and watching `VERDICT: PASS`.
- **F11 — `citation_mining_session` is blocking and vacuous:** 191 sources in scope, 9 (4.7%)
  covered, `Outstanding: 0`, exit 0.
- **F12 — a crash in the render audit was reported as a skip,** because its top-level `catch`
  reused the exit code that means "no browser here".

Separately, **five of the twenty quarantine reasons were factually wrong**, and the headline
figure for the red `test_db_integrity` was wrong in both its count and its verdict.

## Corrections to the record

Three claims in the durable record did not survive verification. All are corrected in place
and marked.

1. **`validate_pydantic_schemas` has `--strict`.** It was quarantined as a
   "not-really-a-gate… same shape as `validate_reasoning`" for exiting 0. That is *precisely*
   the error the register had just corrected for `validate_reasoning` — repeated one paragraph
   later about a different tool. Recorded as such: **the lesson did not generalise by being
   written down.** It generalised only when a later pass re-ran every tool's `--help`.
2. **Standing task 9 was false on both sides.** `schema_reference_drift_audit` does not detect
   `schemas/*.py` vs SQLite drift — its own docstring disclaims exactly that. The two tools
   never overlapped, so "decide who owns schema drift" had no subject.
3. **`test_db_integrity`: 81 out-of-enum rows, not 106,** and the verdict is split rather than
   uniform. 106 was `863 − 757`, which counts the 25 `UNVERIFIED-1` rows that *are* in the
   enum. `B01`/`B06` are a stale test — `DISPUTED` and `CLOSED-DECIDED` came from an
   owner-approved DR in July, while the test's list was last curated in May. `C01`–`C04`/`G02`
   are the genuine content backlog. This matters because "it is all content backlog" is the
   premise on which branch protection defers requiring that job.

## What was built

- Four checks de-quarantined and wired advisory; three quarantine reasons corrected in place.
- `--deep` on `migration_reproducibility.py`: every table, every row, with timestamp-only
  divergence separated from content so it does not cry wolf. Wired **advisory**.
- `check_commit_msg.py` rewritten with `E3`/`E4` exemptions and a real 9-case selftest.
- `test_validate_evidence_state_2_4.py`'s fixture now discovers its DDL from the migrations
  and guards against falling behind again; wired, 12/12.
- `pipefail` on `ci.yml`'s plan step — the one pipe through which the entire gating plan flows.

Every new selftest leg was **mutation-tested against its own pre-fix code** to confirm it
would have failed. A selftest that has never been watched fail is not a selftest.

## What `--deep` found, and why it was left advisory

Exactly two tables diverge substantively: `evidence_sources` (277 rows — `subtype`,
`citation_count`, `pages`, `pub_month`) because `resolve_dois.py` writes Crossref enrichment
straight into it, and `url_verification_runs` because `verify-urls.yml` inserts its run record.
**Both are written by the same scheduled workflows that DR-2026-05-28 already exempted two
other tables for.** So this reads as an incomplete exemption list, not a hand-edited DB.

Left advisory deliberately. Resolving it is an owner choice between widening the DR's
exemption list and requiring those jobs to emit migrations, and promoting it first would block
every data PR on a divergence the project may well consider legitimate.

## Not done / honest limits

- **The `verification_status` enum was NOT widened**, though doing so would turn `B01`/`B06`
  green. It has no CHECK constraint and four vocabularies coexist; ratifying one is a D-SCHEMA
  decision. Widening a blocking gate's accepted values unilaterally is the shape of making a
  gate agree with reality rather than the reverse.
- **`schema_reference_drift_audit` was NOT retired** despite its one gating check being carried
  with better precision by the wired `graph_audit`. Retirement is owner-gated.
- **`sessions/LATEST` was again NOT advanced**, for the same reason the last session gave.
- Branch protection still not enabled — no available tool exposes it.
- The 236 `validate_pydantic_schemas` findings are **not** all adjudicated as real drift. Whether
  `schemas/*.py` mirrors SQLite or the YAML entity layer is a genuine open question; §10 says
  SQLite, and the check is wired on that reading.

---

# Planning instructions for the next session

**Read first:** `references/tooling-register.md` §4.1 (the corrected `test_db_integrity`
triage), §4.2 (F7–F12), and §5. Then `governance/check-registry.yaml`.

**Orient mechanically:**
```
pip install --ignore-installed PyYAML -r requirements.txt jsonschema
python3 scripts/run_checks.py --selftest
scripts/preflight.sh --all
```
Expect red: `test_db_integrity` (blocking), and advisories `validate_pydantic_schemas`,
`migration_reproducibility_deep`, `pmp_audit`, `reasoning_doc_citations_audit`,
`research_protocol_audit`, `metadata_integrity_audit`, `population_integrity_audit`,
`validate_reasoning`. **All known and pre-existing — not your regression.**

**Owner decisions now blocking real work, in the order they unblock the most:**

1. **Ratify the `verification_status` vocabulary** (D-SCHEMA). Unblocks `B01`/`B06` honestly and
   shrinks standing task 12 to its genuine content core (`C01`–`C04`/`G02`).
2. **Rule on `--deep`'s two divergences** — widen DR-2026-05-28's exemption list, or require
   the scheduled jobs to emit migrations. Until then the DB's reproducibility guarantee is
   weaker than CLAUDE.md described.
3. **Decide what `schemas/*.py` canonically mirrors.** Decides how much of 236 is real.
4. **Decide what `sessions/LATEST` is for** — F11 is a blocking gate passing on 4.7% coverage.

**Candidate next tasks:**

1. **Clear the real `test_db_integrity` backlog** — `C01`–`C04`/`G02`, ~105 rows from one July
   citation-mining batch, via migrations. Note the scheduled resolver **cannot** self-heal
   these: every phase targets `WHERE doi IS NULL`, and Phase-4 author enrichment filters on a
   `source_type` these rows lack.
2. **Repair `validate_commits.py`'s three rotted lists** (skill prefixes lack `governance`,
   author regex, no merge exemption), then decide whether it earns wiring beside
   `check_commit_msg.py`.
3. **Adjudicate the 6-slug banner/DB mismatch** behind `pre_rehab_banner_audit` — it becomes a
   real anti-drift gate the moment that is settled.
4. **Move `full_db_metadata_verification.py` onto the source-verification schedule.**

**The generalisable lesson, since two sessions running have now hit it:** before calling a tool
broken, run `--help`. Before trusting a figure in a register, re-derive it. Before trusting a
green check, ask what it does when its input is missing — that single question found three
distinct vacuous-green mechanisms here.
