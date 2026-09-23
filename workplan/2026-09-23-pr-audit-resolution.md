# PR audit, 2026-08-23 → 2026-09-23 (#116–#157): findings and agreed resolution

**Generated 2026-09-23. Every figure below was measured on that date by the scripts in
`scratchpad/session_2026-09-23-pr-audit-token-compliance-xnh1k0/audit/`. Re-run them rather than
trust a number here (CLAUDE.md rule 7a).** The full audits, with the command beside each figure, are
in that folder: `audit_tokens.md`, `audit_protocol.md`, `audit_architecture.md`, `audit_claudemd.md`.
The two resolution perspectives and their handshake are in `resolution_holistic.md` (root causes
R1–R7) and `resolution_granular.md` (fixes G1–G18, the per-check merit table and a 32-item
verification ledger).

**Coverage gap.** Transcripts start on 2026-09-01. #116–#125, #148 and the batch-08 execution have
no transcript, so token and tool findings do not cover them.

## Verdicts

| Dimension | Verdict |
|---|---|
| Token efficiency | **Poor.** At least a third of orchestrator tokens went to turns that did no work. The two biggest causes were CI wake-ups on subscribed PRs that only reported green, and the stop-hook commit/push loop. Half of all main-session tokens were spent at context above 500k. These are token counts; most are cache reads, billed at a fraction of the input rate, so they are not a cost figure. |
| Skill/tool invocation | **Bypassed.** The Skill tool was barely used, and no project skill could load before 2026-09-18. Nine skills still presuppose the deleted item layer. `repo-sweep` was never used. Most antagonist runs used general-purpose agents rather than the `antagonist` agent. Suites were re-run with no change since the last run hundreds of times. |
| Data architecture | **Write path held; design churned.** Every PR that touched the DB blob shipped a migration. But roughly a quarter of the period's schema migrations corrected earlier ones from the same period. There were rule-5 copies (080), DDL built on the retired `axes` vocabulary and on `item_code` after both were ruled out, and a module that no longer imports (`schemas/bpc_metadata.py`). The scheduled bot rewrote `evidence_sources` outside any migration (`c4c8463`). |
| Protocol conformance | **Partial.** Attestations were present, R10 and R13 held, and the DoD was green before merge. But the search log's identifiers were reissued after a hand DELETE: `exec_id`, and also `candidate_id`. Forward mining never ran on 7 of 12 T1–T2 anchors, yet they are marked `mined`. There was no adversarial pass on five data PRs. R1 order was inverted in three batches, and no PR had a GitHub review. |
| CLAUDE.md | **Mechanically sound, but it broke its own rules.** It stated stale facts in the present tense, carried correction histories, never mentioned the project's agents and commands, and gave a stop-hook remedy the agent cannot run. *Fixed in this PR.* |

## Root causes (holistic), with severities recalibrated in the handshake

1. **The provenance logs live on the work branch.** They append on every turn, so the stop hook's
   clean-tree demand can never be met, and each answer to it is a push that triggers CI.
2. **The PR is opened early and watched live.** Each push runs CI, each run wakes the session, and
   each wake re-reads a context of several hundred thousand tokens.
3. **Sessions have no scope and no reset.** Open-ended status prompts turn into days of
   infrastructure rework in one context, which runs until the automatic compaction at about 784k.
4. **Gates check that something exists, not that it was done correctly.** Suites are also run for
   reassurance rather than to answer a question.
5. **Writers and retractions run outside the sanctioned path.** The scheduled bots write the blob
   directly, and owner-ruled clears were done as hand DELETEs.
6. **The schema is designed by trial migration.** Rulings bind the prose before they bind the DDL.
7. **Scaffolding is stale or bypassed:** item-layer skills, and an adversarial pass that has no
   record.

Severities agreed in the handshake:
- Identifier reissue: **HIGH** (not CRITICAL), but first in execution order.
- Early merges and no GitHub review: **MEDIUM**.
- Determinations framed only on MOB: a direction-of-travel signal, not yet a §6 defect, since all 8
  specifications are retired.
- REF-01006: the author rows are byte-identical before and after the bot commit. The defect is the
  unevidenced `author_count_is_complete` flag and the path it took, not fabricated authors.

## Done in this PR

- **CLAUDE.md corrected.** The stale facts are fixed and the correction histories moved to commit
  messages. A suite-frequency rule was added (owner instruction), the agents and commands are named,
  the stop-hook trap was fixed, and the rule-3 bot paragraph corrected (`e3846fa`, `2a8baf6`).
- **Rule 9:** do not watch PRs; open the PR last (owner instruction).
- **`ci.yml` `concurrency`:** superseded PR runs are cancelled. This saves runner time only.
  `paths-ignore` was dropped because path filters are evaluated against the whole three-dot PR diff,
  and a skipped workflow would block merges once required checks exist.

## Agreed resolution, in execution order

Items marked **owner** need an owner decision; everything else is code or process under CLAUDE.md §8.

**Phase 0: stop the bleeding (S)**
- **Owner pastes** the `.claude/settings.json` given in-session. It adds `permissions.deny` for both
  `subscribe_pr_activity` tools, `send_later` and `create_trigger`, which is the mechanism that makes
  rule 9 hold. It also appends a SessionStart hook that runs `scripts/fix_stop_hook_loop.sh` in every
  new container. [UNVERIFIED: whether the harness installs its stop hook before SessionStart hooks run.]
- G13-1 (supersedes holistic R1's orphan branch, agreed by both passes):
  - The live logs write to gitignored paths.
  - `preserve_transcripts.py` copies them into tracked paths only at `/batch-done` and session close,
    never between opening a PR and merging it.
- G13-2: scope the project Stop hook's `research_batch_dod --all`. It should run only for a
  research-batch session whose scratch DB has changed.
- G13-4: add a one-deliverable-per-session norm to CLAUDE.md: hand off at about 300k context rather
  than riding to auto-compaction.

**Phase 1: small, no owner decision (S)**
- G5: `schemas/bpc_metadata.py:78` `last_updated` → `updated_at`; drop it from `db.py:90`
  `_BPC_META_COLS`.
- G7: fold `rename_insurance.py`'s view-execution loop into the blocking `schema_reference_audit`.
- G18: delete the `commit-msg` CI job, which is push-only and skipped every PR. Rule 1 stays as text,
  marked NOT ENFORCED.
- G11-2: the `Classify change` job needs a single retry on runner-allocation failure.
- G15: `db.py add-decision`.
- Replace the stale "N today" figures in `governance/check-registry.yaml` with the commands that
  compute them.

**Phase 2: identifiers and gates (M)**
- G8:
  - Rebuild `search_executions`, `search_candidates`, `observed_terms` and `term_adjudications` with
    AUTOINCREMENT, seeded from the historical high-water mark across `data_*` migrations.
  - Derive `identifier_floor_audit._INT_KEYS` instead of curating it.
  - R8 checks against `sqlite_sequence`.
  - An erratum records which batch-05/07 exec ids now point at reissued rows.
- G9-2: the R2 gate works per anchor and requires both directions or a `deferred_reason`.
- G12-2: an R8 timing check.
- G10:
  - `independent_reviewer_counterclaim` becomes a pointer to an `antagonist` transcript.
  - The attestation trigger widens to `scripts/migrations/data_*.sql`.
  - `/batch-done` runs `/adversarial` once, using the `antagonist` agent.
- G3: point the rule-5 copies instead of storing them (`specifications.functional_basis`,
  `determination_gates.trigger_*`). Writer-retire, then reader-retire, then NULL forward. No parity
  check.

**Phase 3: one write path (M)**
- G1: `resolve-dois.yml` and `verify-urls.yml` write through `emit_batch_sql` →
  `emit_data_migration`.
  - `resolve_dois.py` stops the DELETE-then-reinsert of authors.
  - It stops setting `author_count_is_complete=1` from Crossref, or persists the payload first.
  - Then promote `migration_reproducibility_deep` and retire the count-only gate. **Owner:** confirm
    "require migrations" over "widen the exemption" (the registry reserves this).
- Triage `author_fidelity`, then promote it to blocking.
- `source_locators_integrity`: build `db.py amend-locator`, repair the backlog, then promote.

**Phase 4: deletions (M–L)**
- G4: drop the 13 unwritable item-era tables after the rule-4 sweep.
  - Keep `icf_medical_map` and `identity_medical_map`, which are pending medical-lens content.
  - Investigate `citation_population_links` and `connection_targets`.
- G14:
  - Delete `item-audit-pipeline`, `audit-consolidator` and `item-consolidation-analyzer`.
  - Rewrite or delete the three item-keyed auditors.
  - Sweep four more skills for item codes.
- G2: retire `axes`, `population_axis_map` and `access_need_axis_map`, and delete `validate_axes`.
  **Owner:** content re-homing check only.
- G16: derive the Pydantic `MODEL_TABLE_MAP`.
- G9-3: derive `citation_mining_status` via a view, then delete parity test C08.
- G6: `db.py retract-slug`, retiring rows in place rather than deleting them.

**Phase 5: content**
- G9-1: forward-mine the 7 anchors, or record a deferral.
- G17-1: adjudicate the 57 observed terms before any determination is stated.

**Check merit** (full table in `resolution_granular.md` §3):
- **Delete:** `validate_axes`, `site_pages_fresh`, `validate_schema_cross_check`, `pmp_audit`,
  `population_integrity_audit`, the `commit-msg` job, and `citation_mining_session` after G9.
- **Demote to advisory:** `claude_md_spine`, `audit_adversarial_use`, and the two blocking render
  `*_fresh` checks.
  - The passes accepted each other's call on `claude_md_spine`, so this document decides: demote,
    since it is nearly free and reversible.
- **Promote:** `author_fidelity` and `migration_reproducibility_deep` (both after repair), and
  `attestation_evidence` after G10.
- **Merge:**
  - the jurisdiction pair into one check;
  - `source_slug_links_duplicates` into `test_db_integrity`.
- **Repair:** `research_dod_session`, `identifier_floor_audit`, `schema_reference_audit`,
  `attestation_presence`, the basis of `validate_evidence_state`, `validate_pydantic_schemas`,
  `test_verification_pipeline`, `metadata_integrity_audit` and `retired_vocabulary`.

**Suite policy** (now CLAUDE.md §1): suites run at three points only.
1. The diff-scoped gate, once, before the PR.
2. CI on the PR.
3. `research_batch_dod --session`, once, inside `/batch-done`.

Never re-run a check when nothing it reads has changed.

## Owner decisions outstanding

1. Paste the `.claude/settings.json` (deny list and stop-hook patch).
2. Enable the `main` ruleset with required status checks.
3. For G1, the route for bot writes: require migrations (recommended), or widen the exemption.
4. For G12-1, whether chain-following batches are an exception to R1's "Co-1/T2/Co-2 first — no
   exceptions".
5. For G17-2, whether to make an ICF or needs lens mandatory for stated cells. This tightens D-0182.
6. For G14/R7, whether `multilingual-research`'s CHECK/LOG steps are run or retired. Three
   research-contract rules are anchored on that skill.
7. For G2 and G4, content re-homing: the `axes` maps and D-0184's crossing onto `parameter_id`.
