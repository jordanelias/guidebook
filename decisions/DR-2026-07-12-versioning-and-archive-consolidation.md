# DR-2026-07-12: Edit-in-place versioning, register-snapshot ban, and archive consolidation

- Status: **PROPOSED — pending owner ratification**
- Date: 2026-07-12
- Prepared by: Claude, following `audits/consolidation-sweep-2026-07-12.md`. This DR proposes policy only; it does not itself move, merge, or delete any file. Execution is explicitly deferred to a follow-up pass once ratified (see "Consequences" below).
- Affects (if ratified): `governance/project-instructions-v10_7.md`–`v10_14.md`, `governance/armature_v3_review.md`/`v4.md`/`v4_integration.md`/`v4_resolutions.md`, `_archived/gap_register*.md`, `audits/_archived/tier*-verification-*.md`, `misc/archived/`, `_archived/misc-2026/`, `_archived/working-2026/`, `parts/_archived/`, `parts/deprecated/`, `parts/88_to_90/`, 10 handoff documents across `sessions/`, `references/`, `workplan/`, `working/`
- Related: `architecture/consolidation-remediation-roadmap-2026-07-12.md` (Principles 1, 2, 6), `audits/consolidation-sweep-2026-07-12.md`, `architecture/project-architecture-guidebook-v2.3.md` `<migration_and_growth>` (already states the single-archive-location rule this DR asks to actually apply)

## Context

Three related fragmentation patterns recur across otherwise-unrelated parts of the repo, all stemming from the same root cause: git history not being trusted/used as the version record.

1. **Policy documents versioned as new files.** `governance/project-instructions-v10_7.md` through `v10_14.md` — 8 files, one per revision — and the four-document armature design chain (`armature_v3_review.md`, `v4.md`, `v4_integration.md`, `v4_resolutions.md`) both require a reader to know which file is current and reconstruct the delta themselves. `architecture/project-architecture-guidebook-v2.3.md` is a working counterexample: it is a single file, revised in place, with prior text recoverable via `git log`.
2. **Registers snapshotted to dated files instead of queried via git history.** The gap register exists as `_archived/gap_register.md`, `gap_register_archive.md`, and `gap_register_2026-03-20.md`; tier-verification exists as five dated files in `audits/_archived/`, one pair a single day apart. `references/connection-register.md` already demonstrates the alternative: it was replaced with a short redirect stub pointing to the two live files, rather than kept as a third parallel copy.
3. **Six archive-ish locations exist outside the two the architecture already names** (`_archived/`, `workplan/_superseded/`): `misc/archived/`, `_archived/misc-2026/`, `_archived/working-2026/`, `parts/_archived/`, `parts/deprecated/`, `parts/88_to_90/` (89 files total). `architecture/project-architecture-guidebook-v2.3.md` already states content should move to `_archived/` mirroring its origin path — this is a compliance question, not a new rule.

A fourth, smaller pattern: ten handoff documents with no consistent name or location (`sessions/handoff-next-session.md`, `sessions/HANDOFF-2026-05-10.md`, `references/phase-b-handoff.md`, three `workplan/*-handoff.md` files, `references/audits/handoff-2026-05-12-*.md`, `working/mobile-app-prototype-v9/HANDOFF.md`, plus two inside a session-artifacts folder).

## Proposed decision

1. **Edit-in-place policy.** Any document whose job is to state *current* policy (PI, architecture specs, tier system, mission, etc.) lives at one stable, un-suffixed filename going forward. Revisions are commits, not new files. This does not apply to documents whose job is to record a point-in-time decision or analysis (DRs, audits, session logs) — those are correctly dated and should not be retroactively edited.
2. **Register-snapshot ban.** A register (gap register, connection register, decision register, verification-status reports) has exactly one live path. A point-in-time comparison, if genuinely needed, cites a commit SHA or embeds a git-diff excerpt rather than committing a full dated copy.
3. **Single archive location.** All retired content consolidates under `_archived/`, subdirectories mirroring origin path, per the rule `architecture/project-architecture-guidebook-v2.3.md` already states. The six locations named above are folded into it as a follow-up execution pass (not part of this DR).
4. **Handoff convention.** Handoff documents live at `sessions/handoffs/handoff-<topic>-<date>.md`. Existing locations get a short redirect stub (the `connection-register.md` pattern), not silent deletion.

## Consequences if ratified

- **This DR does not execute the consolidation.** Ratification authorizes a follow-up pass to: (a) merge the 8 PI files into one `governance/project-instructions.md` with the v10_14 content as current; (b) produce one consolidated "current armature" document from the four source files, then move the sources to `_archived/`; (c) delete/redirect the register and verification snapshot files; (d) move the six archive-ish locations under `_archived/`; (e) relocate the 10 handoff documents. Each of these is a real content decision (which PI text is actually current if the files have diverged beyond simple numbering, whether any armature resolution was itself later reversed) that benefits from owner review before execution, not a mechanical file move Claude should do unilaterally in the same pass as proposing the policy.
- Going forward, new governance-document revisions and new registers follow this policy from the start, preventing the pattern from recurring even before the backlog above is cleared.
- No code, schema, or data changes.

## What would make this ACCEPTED

Owner review of the four policy points above (they are process rules, not judgment calls about specific evidence, so this is a lighter review than the P0 schema/threshold DRs), followed by an explicit ratification note or session directive authorizing the follow-up execution pass described in "Consequences."
