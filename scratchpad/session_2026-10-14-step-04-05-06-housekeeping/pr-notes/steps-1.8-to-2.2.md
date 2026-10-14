# PR body notes, steps 1.8 to 2.2e (stack/1.8-registry-prose through stack/2.2e-back-pointers)

Chain, each branch merged into the next, never rebased: 1.7 (repaired) → 1.8 → 1.8b → 1.9 (repaired) → 1.10 (repaired) → 1.11 (repaired) → 1.12 (repaired) → 2.2a → 2.2b → 2.2c → 2.2d → 2.2e.
Heads and gates are commands, not typed here: `git rev-parse --short stack/<name>`; `scripts/preflight.sh`; `python3 workplan/pipeline-state-graph/build_graph.py --check` and `--selftest`; `migrate_db.py --rebuild` then `scratchpad/.../gates/cmp_rebuild.py`.
At the 2.2e tip: preflight PASS with the six advisory failures every earlier step had (migration_reproducibility_deep, scan_debt, validate_schema_cross_check, retired_vocabulary, research_protocol_audit, metadata_integrity_audit); graph check 0 failures, selftest passes; rebuild identical to the blob except `data_migrations`, `evidence_source_authors`, `evidence_sources` (the ledger's own stamps and the two bot-written tables).

## The 1.7–1.12 adversarial pass (read-only Fable antagonist, detached worktree at 1ff6cfd) and what became of each finding
Every finding was confirmed against the artifact before it was repaired; repairs were made on the branch that introduced the defect and merged upward.

| finding | verdict | disposition |
|---|---|---|
| F1 rule 0 undischarged for the register, decision_capture, the Pydantic-mirror clause (DR-2026-09-26 RC-001) | sustained | ledger marks in 2.2d (lines 17, 26, 118, 504, 520, 545, 548, 2392), fifteen SUPERSEDES/BY pairs with local marks in 2.2e (the RC-001 clause among them) |
| F2 `doctrine_recheck` registered with `--cross-ref` cannot go red when a governance document is removed; the registry narrative still counted a decision register | sustained, reproduced (time-model.md removed: `--cross-ref` exit 0, `--baseline-against` exit 1) | narrative corrected in 1.12. The gate itself is unchanged: **owner item** below |
| F3 R45's retired rule ids validated for new attestations | sustained, reproduced | 1.7: retired ids valid only for an attestation file that exists at the base ref (a fabricated file citing structure-auditor now fails CHECK 3; the committed one passes) |
| F4 "five passes" over four rows; "13 CANONICAL" | sustained | 1.12: "four passes"; the figure removed (rule 7a) |
| F5 false sentences left in decision-protocol and architecture v2.3 | sustained | 1.12: section 5, 6.1, 6.2, the required-fields table, the decision-record notation and legacy tier, the validator pointers and the dead status rows deleted (R47: deleted, not bannered); architecture no longer claims DR files point at ledger entries (24 of the DR files cite the ledger; that was not "remain") |
| F6 live surfaces still state dropped objects as live | sustained in part | fixed: reference_stubs callers (1.9), deprecated-skills callers (1.7), schemas rows and the R12 anchor (1.10), tooling-register kinds table replaced by a pointer to the registry (1.11), two test comments (1.12). **Declined:** retired-vocabulary entries for the dropped names (the instrument directory names every retired object and would flood an advisory check; admission test 4 of that file fails). Left, because they narrate a past failure: `.claude/hooks/ensure-deps.sh` and `scripts/validate_schema.py` comments, the dated correction notes in tooling-register.md |
| F7 an active skill governs an archived layer | sustained | 1.11: `reasoning-doc-citations` deleted with its registry and effort rows |
| F8 callers of deleted skills | sustained | 1.7: workplan-orchestrator's Dormant Workflows, Skill Index and Stage A Skill Build Schedule deleted; pointers removed from five other skills; skill-registry no longer claims every active skill has an effort row. tier-system's pointers to guidebook-auditor were found later and are repaired in 2.2e (belongs to 1.7) |
| F9 migration 111 header and commit 57247bf | sustained, conclusions survive | header corrected in 1.9 (the grep cannot match `DELETE FROM reference_stubs;`, which is in data_20260823225142; both precede the 095 marker). Commit 57247bf said "three bot-written tables": the rebuild differs in `data_migrations`, `evidence_sources`, `evidence_source_authors` (`pipeline_runs` went with migration 110) |
| F10 attestation_presence cited as a gate over a diff that removed its scope | sustained | stated in the 1.11 repair commit; no change possible |
| F11 doctrine-recheck §4.3 deleted beyond R47's letter | withheld for the owner | kept deleted: it existed only as a flag on a Decision record, which the register's retirement removes. §4's heading and mitigation (4.1, 4.2) stand. **Owner item** |

Commit-message errata (history cannot be amended here): 1.6 says "four criteria" (three were deleted) and "20 re-anchored" (18); 1.7's preflight line is garbled (59 green, 7 advisory failures); 2.2d says "six of them checked" (all eight appended quotes were checked, seven against their line and one against its three-line span).

## 1.8 / 1.8b
1.8: 59 narrative fields over 300 characters removed from the check registry; nothing read them. 1.8b: dead text earlier steps left.

## 1.10, 1.11, 1.12
1.10 (R5): the Pydantic mirror requirement retired; 24 unread schemas modules and `validate_pydantic_schemas` deleted. 1.11 (R22): `references/bpc-reasoning` moved to `_archived`. 1.12 (R30, R47): the decisions register archived, `decision_capture.py` and `schemas/decision.py` deleted, `doctrine_recheck` stops reading the register.

## 2.2a – 2.2e: Phase 2 step 2.2, applied by deleting stale clauses
2.2a mission, tier-system, methodology (R6 to R10, R20, R31); 2.2b co-1 operational and jurisdiction §2.3 (R11, R12); 2.2c process contradictions (R38), precedence (C-047), hand-written counts (C-038, part); 2.2d ledger marks and the eight session-only statements (R10, R11, R13, R18); 2.2e back-pointers (rule 0, RC3).

**Owner merges in these steps** (CLAUDE.md §8: mission, tiers, jurisdiction, and the files the plan marks): `governance/mission-and-epistemics.md` (commitment 7 heading, test item 6, the Status line, the marker line, the `stated` row, "seven tiers", the cell key); `governance/tier-system.md` (a sentence separating band from state; "Anchors outright" → "Full strength"; the guidebook-auditor pointers); `governance/evidence-methodology.md` (many small edits and the §2.7 transition table replaced by one sentence); `governance/co1-operational.md` (§6.1, §6.3, §7.1, §7.2 deleted, §3.1 Part A rewritten); `governance/jurisdiction-philosophy.md` §2.3 (the "all 24 jurisdictions" conjunct deleted, the language conjunct kept); `CLAUDE.md` §7 (one sentence); `architecture/project-architecture-guidebook-v2.3.md` (the precedence sentence and row 4 except an invariant a ruling has superseded; the deprecated-skills sentence; the register sentence).

**What I did not do, and why**
- C-015: R34 reconciles by object (built in step 0.2), but the D-0168 and D-0174 sentences it reads are unmarked. C-016: the 2026-08-24 DR's "enforced by schema shape" and the "GENERATED from its register row" header on 22 DR files are false and unmarked. Marking either needs more SUPERSEDES pairs with ledger BY quotes and touches `decisions/`. Left open.
- C-030, C-041 to C-045 (instrument and architecture): the instrument is append-only by its own OPI-131, and R40's read-set has no ledger quote to anchor a BY on. Left open; CLAUDE.md §9 already states the chain.
- C-038 keeps three sides (jurisdiction counts, the language count, the markdown standards registry).
- C-049 is narrowed to the instrument's unmarked OD-2 line; C-050 to the open confirmation of LED-168.
- The six `decisions/` files marked in 2.2e each already have an attestation, so `attestation_presence` passes; none was added because the marks are appended records. Say so if you want one per file.

**Owner items**
1. F2: register `doctrine_recheck --baseline-against <snapshot>`, which would be red today on three documents whose Status is no longer CANONICAL? Or accept that the gate examines pass 2.3 only (the registry now says so).
2. F11: confirm doctrine-recheck §4.3 stays deleted.
3. The unresolved owner items from earlier steps: five served populations without population→ICF links; the 2026-09-11 medical-lens ruling still names `axes`; the 17 T4–T6 sources `code_currency_audit` flagged; research-contract R10 and the SessionStart hook still cite the deleted cron; the `_template.md` files under bpc-reasoning and connection-reasoning cite `validate_reasoning`; D-0170 and functional-taxonomy beyond the one consequence marked; `schemas/directness.py` reads a dropped table.
4. The next bot fires (2026-10-19 and 2026-11-01) conflict with any open DB pull request until 1.5 merges.
5. Migration numbers 107 to 111 must be re-pinned at pull-request open (106 is pending in #174).
