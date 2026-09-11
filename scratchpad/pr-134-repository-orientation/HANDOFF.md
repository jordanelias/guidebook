# Handoff — PR #134, branch `claude/repository-orientation-9380wp`

Written at session close. Everything below is derived; re-derive anything you intend to rely on
(`CLAUDE.md` rule 7).

## THE NEXT SINGLE ACTION

**Re-run batch 06 steps 1–2 on a fresh scratch copy of canonical, emit the data migration, and commit
it.** Four hours of walk work exists **only** in a container scratch DB that dies with the container.
Nothing was emitted through `emit_batch_sql → emit_data_migration → migrate_db`.

The loss is bounded, not total: **the retrieval-log payloads for both new papers are committed**
(`retrieval-log/session_2026-09-10-research-batch-06-circulation-geometry/`, 15 manifest lines), so
re-running is cheap and the bibliography comes from bytes rather than memory. The scratch is at schema
73 and canonical is now **74**, so start from a fresh copy — do not carry the old scratch forward.

One thing to re-check when you do: commit `bd0d08c` says Sanford (REF-00980) was staged-not-admitted,
and the scratch admitted it six minutes later with `scope=high_control` **after** the last manifest
fetch. Confirm that scope came from bytes before emitting it.

## State of the pipeline, measured

Canonical `data/guidebook.db`, `PRAGMA user_version` **74**:

| Table | Rows |
|---|---|
| `evidence_sources` | 9 |
| `base_parameters` | **0** |
| `source_value_extractions` | **0** |
| `convergence_assessment` | **0** |
| `specifications` | **0** |
| `base_taxonomy_medical` | **0** |

**Batch 06's determination is NOT written.** The PR body's claim that "a data migration is applied; the
specification stage is writable for the first time" describes the **scratch**, not canonical — correct
that sentence.

## Landed (44+ commits over `bd59fd4`; PR #134 open, mergeable, 12/12 green at `b3eaf7b`)

- **Apparatus cull, four agonist/antagonist pairs.** Blocking-and-vacuous 6 → 2. One ratified grain
  rule now has one implementation (336-triple equivalence proof). Three deletions **refused** on live
  callers the brief had missed.
- **`D-0188`** — the owner delegation, in all three homes (`727a000`, migration
  `data_20260911012015…`, DR file, attestation).
- **Migration 074** (`e89b8d2`) — `identity_medical_map`, `icf_medical_map`, the two anchor columns.
- **`db.py add-medical`** (`6bb2f71`) with nine refusals, plus the archive-aware verification fix.
- **WHO ICD-11 MMS 2024-01 release file persisted** (`6360a22`), `sha256 b92212138c67738a…`.
- Ledger entries for every ruling, including the corrections below.

## Five corrections the session made to itself — read these before trusting anything above

1. **The escalation contradicting `D-0170`.** "The medical lens stays deferred" was escalated as an
   open question six hours after the owner had ratified the lens. An empty table was read as "nobody
   decided" rather than "a ruling awaits execution."
2. **`source_locators`' corruption direction.** Reported as "the DOI is wrong"; the **title** is the
   corrupted half. REF-00037 genuinely is the Rouvier review. 31 of 36 differ, not 36.
3. **"ICD-11 cannot be verified from this container."** False. WHO's CDN release files are
   unauthenticated. I generalised from a 401 API and a JavaScript browser to a closed building, which
   is what R10 forbids.
4. **The 29-disease-entity grain.** Wrong shape; MB5 is a block and the owner said "high level".
5. **The archive-aware verification defect** — and this is the one to internalise. `add-medical`'s
   payload check substring-matched raw bytes, and the only artefact it will ever see is a
   **deflate-compressed zip**, in which no code occurs literally. So it refused the very payload that
   proves the anchor, and the ruling "verified against the persisted release file at write time" was
   **unexecutable**. The MB5 verification shown at 02:47 was done by hand in Python, never through the
   writer, while the record claimed otherwise. Fixed and proved: `--icd11 BlockL3-MB5,MB56,MB57` now
   returns `anchor_verified: true`, and `ZZ99` is still refused.

**A sixth was found by the pass that confirmed the fifth**: the "demand-populated" ruling was itself a
rationalisation, re-instating the deferral the owner had overruled. Corrected in the ledger — the lens
is populated by **correspondence from `populations` and `axes`**, ~15–20 rows, then on demand. And its
demand count was measured against the committed table while ignoring the scratch, which already held
**REF-00979 "…for Young Men With Paraplegia"** — MB56 in its own title.

## Owner-gated and unanswered

1. **"We have a PR that touches on sourcing medical codes from international database."** All 30 PRs in
   this repo were checked; none does. Which repository?
2. **WHO reuse terms for block *titles* in a CC BY-SA 4.0 work.** The ledger says item 7 is "answered";
   that is true as to *source* and not as to *titles*. Bare identifiers keep exposure minimal.
3. **B5b's four `scope` rulings** — `workplan/2026-09-10-b5b-scope-owner-escalation.md`.
4. **Whether the correspondence-populated correction is accepted** (ruled under D-0188 clause 3).

## Owed

- ~~Write `scratchpad/pr-134-repository-orientation/ADJUDICATION.md` from
  `transcripts/harness_94859b50/subagents/2026-09-11T00-54-46_other_a382a8ba.jsonl` (search
  `Ruling 1.1`). **Three homes cite it and it was never committed** — including an immutable
  `decisions` row, which cannot be corrected.~~ **DONE 2026-09-11.** Written verbatim from the
  transcript's final message rather than paraphrased, with a header naming the source bytes and a
  command that reproduces the body byte-for-byte. Its header also records which of the report's
  rulings landed and which did not — §1.1's 29-row vocabulary is still unwritten, and §2.3's
  `source_locators_integrity` gate was never built.
- ~~Correct the PR body's "data migration is applied" sentence.~~ **ALREADY DONE**, verified
  2026-09-11 against the live body: it reads *"The only data migration applied here is `D-0188`'s
  decisions row"*, and `git diff --name-status origin/main...HEAD -- scripts/migrations/` confirms
  exactly two additions, `074_medical_lens_crossings.sql` and
  `data_20260911012015_…circulation-geometry.sql`. **NOT done, and deliberately:** the body does not
  mention the `ADJUDICATION.md` repair. `update_pull_request` takes no patch — only a whole new body
  — so adding one line means hand-retyping ~4.4 KB of a reviewer-facing record. That is the
  hand-copied dual home this project already carries three of per decision, and a transcription slip
  in it would be worse than the omission. The commit message carries the full account.
- ~~A contract criterion stating **"the medical lens is offered, not adopted"**. Layer 2 enforces it
  (`add-medical`, 074's CHECK); Layer 1 never states it.~~ **DONE 2026-09-11**, as two criteria
  rather than one, because it is two facts at two stages: `base/base-medical-lens-offered-not-adopted`
  (MD- shape, no value-bearing name, every row crossed) and
  `specification/no-diagnosis-only-determination` (a determination is never keyed on a diagnosis
  alone). `medical_lens_integrity`'s registry `basis:` moved off the borrowed
  `base-population-vocabulary` onto the first; `basis` is singular, so selftest C7 lists the second
  among criteria no check claims — enforced, unclaimed, and recorded in the entry rather than left
  to be rediscovered. Two stale rationales in the same entry were corrected in the pass: the
  demand-populated no_floor (superseded by the correspondence correction, whose own CONDITION names
  "any session citing the demand-populated entry") and the "no WHO credentials" note.
- `sessions/LATEST` / `LATEST-RESEARCH` still name batch 05. They move at CLOSE with a session record,
  and **the D-0188 attestation already names `session_2026-09-10-research-batch-06-circulation-geometry`**
  — so the record must be written under exactly that id.

## Traps a fresh session will otherwise rediscover

- **Migration 074's header still says the content is licensing-blocked.** Migrations are immutable
  (rule 3); the ledger supersedes it. Do not edit it.
- **Two session ids are in play**: `…batch-06-circulation-geometry` (data) and
  `…medical-lens-icd11` (the WHO retrieval log). Gates scope by id, and the wrong one passes green
  having examined nothing.
- **`scratchpad/CURRENT`** = `pr-134-repository-orientation` (correct).
- **The b-anchor join over-reaches.** MB56 → b730 → AX-AMB/REA/WHM → carries BAR, LPA, TALL, who
  attach anthropometrically. No mechanical guard exists and `CLAUDE.md` §8's bar does not justify
  building one; `identity_medical_map.relationship` forcing `identity_first` is the schema's own prune.
  Author rows per identity; never generate them from the join.
- **`adherence_log_audit.py:517`** defaults `base=HEAD~1 head=HEAD`, so the two blocking attestation
  gates examine one commit regardless of `--changed-from`.
- **`term_aliases.language` is lowercase** (`'en'`) while `search_executions.language` is uppercase.
  A case-wrong filter returns nothing and reads as absence.
