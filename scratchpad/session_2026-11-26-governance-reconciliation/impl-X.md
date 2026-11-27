# Implementer X log (CLAUDE.md, governance/stage-map.yaml), 2026-11-26

No git writes. Files edited: CLAUDE.md, governance/stage-map.yaml only.

## A1 DONE
- CLAUDE.md:270 deleted "Convention: `base` is not a stage, so a view reading one stage plus base crosses nothing." Nothing replaces it; the rest of the protected-view paragraph is unchanged.
- stage-map.yaml:28 "`cross-stage` is not a stage either." -> "`cross-stage` is not a stage." (the "either" leaned on the dead base convention).
- stage-map.yaml:83 "foreign keys point into `base`, which is not a stage, so the table crosses no stage." -> "foreign keys point into `base`."
- Basis verified: references/project-standards.md:2306 "This ends the "not a stage" convention entirely ... `base` is stage 1."
- Callers swept: workplan/pipeline-state-graph/AMBIGUITIES.tsv:60 and atoms-drs.jsonl DRS-132 discuss the CLAUDE.md convention (quote the DR, not CLAUDE.md; not my files; left). T-018-link-table.md:65 quotes the old stage-map wording (task file; left).

## A2 DONE
- CLAUDE.md:372 (now 371) marker line replaced with:
  "Markers (owner, 2026-11-14; `governance/tier-system.md` §5): **●** T1, T2, Co-1, Co-2 · **◐** T3, T4 · **○** T5, T6 · **⚠** (U+26A0, no U+FE0F) in place of the circle, never beside it, for a grey, unverified or thin basis. Unmarked is an error."
- Glyph checked: U+26A0 with no U+FE0F. Tier line, T3 gloss and cell-states line untouched.
- Ledger verified: L6944 / L6973 / L6989 (table), L7053 "Unicode one", L7071-7078 "triangle instead ... do not write both", "thin too" ACTION, L7317 OD-57, L7424 OD-64.
- Note: tier-system.md §5 itself is still stale until T-120 item 2a lands (other implementer / later); the CLAUDE.md line states the table so it is right regardless.
- Prose callers still carrying the old gloss (not my files): governance/mission-and-epistemics.md:136; workplan atoms CLM-038, MIS-03.

## A3 DONE
- CLAUDE.md:381-382 "Only Opus-class models write `best_practice_synthesis`." -> "Only a model at the Opus-class-or-above floor (DR-2026-06-10; owner 2026-07-25: Fable included) authors judged synthesis text; a determination is computed, not written (owner, 2026-09-09)." (antagonist-2 correction 8). No version pin.
- Verified: ledger L608-609 (class floor, Fable), L2690 "you have to compute it", L2712 "Nor does this touch the Opus floor"; decisions/DR-2026-06-10-synthesis-model-floor.md exists.
- Callers (not my files): DELEGATED-RESOLUTIONS.md:284, ATOMS.tsv CLM-041, atoms-claude.jsonl CLM-041, research-matrix plan :72, skills/run-pipeline_SKILL.md:370 (still roughly true).

## A5 DONE (i, ii, iii)
- (i) CLAUDE.md:68-70 "... CI runs the selftest and your local gate does not." -> "A bare `run_checks.py --changed-from` does not run `--selftest`, and the selftest is where a rename fails. ... CI and `scripts/preflight.sh` run the selftest first." Verified: preflight.sh:81 `python3 scripts/run_checks.py --selftest || exit 1` before the diff-scoped run; ci.yml:123 runs --selftest.
- (ii) Verified db.py:3403 (add-source --tier: derived, disagreeing value refused) and db.py:2119 (amend-source --tier: ladder-derived, disagreeing refused). CLAUDE.md:177 "`add-source --tier` asking an operator to retype ..." -> "A flag asking an operator to retype what `derive_tier(evidence_type, scope)` already knows ..." (keeps the principle, drops the false example; derive_tier exists at schemas/tier_derivation.py:85). CLAUDE.md:192-193 "Also outstanding: `amend-source --tier` asking for a value the machine can derive." deleted.
- (iii) Verified .claude/settings.json SessionStart[1] runs `scripts/fix_stop_hook_loop.sh >/dev/null 2>&1 || true`. In this container it did not take: `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh` prints 0; the script's anchor no longer occurs (hook line 85 now has `branch_moved_under_checkout`). Minimal edit: kept the whole sentence including "An agent cannot apply it: the harness classifier blocks it as self-modification", appended "SessionStart also runs it silently (`.claude/settings.json`); whether it took: `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh`." Did not say it fails (container-specific; audit marks other containers UNVERIFIED).

## B1 DONE
- CLAUDE.md:90 "(`ci.yml:257`)" -> "(`ci.yml` job `commit-msg`)". Verified ci.yml:262 job `commit-msg`, :265 `if: github.event_name == 'push'`, :274 the call. Job name used instead of a line number.
- CLAUDE.md:349 "Counts in this file, in `index.html`, in manifests ..." -> "Counts in this file, in manifests and in audits ...". `git ls-files index.html` empty; only _archived copies; render is read from the DB (§3), so no live surface to repoint to. (governance/check-registry.yaml:34 lists `index.html` as a render path glob; not my file, harmless.)
- PI trap (CLAUDE.md:466): verified `ls ... | sort | tail -1` prints v10_9, `sort -V` prints v10_14. "highest-numbered `...v*.md` is live" -> "the numerically highest `...v*.md` (`ls governance/project-instructions-v*.md | sort -V | tail -1`; plain `sort` picks the wrong one) is live". "PI versioning is intentional" (quoted by retired-vocabulary.yaml:230) kept.

## B2 PARTIAL (nothing further applied)
- §8 sign-off pointer: SKIPPED. There is no broken pointer; claude-md-audit C-45 replaces the sign-off list with a pointer to decision-protocol §2.4, which changes content (approval-list E(4) objects that it makes §2.4 the whole owner list). More than a pointer repair.
- States line (CLAUDE.md:372): SKIPPED. Not broken: its four values match the live `specifications.state` CHECK. C-32 adds an OR-1 ruling: more than a pointer repair.
- L538 "what to do now" and orient.md: untouched by instruction (C4 routing).
- §9 table paths all exist (checked). No other broken path pointers found beyond those fixed in B1.

## Verification
- `python3 scripts/audit/claude_md_spine.py`: PASS (EXAMINED 7 stages, 1 SPINE line).
- No rule or section numbering changed; no headings touched.
- `build_graph.py --check`: 1 failure (PIP-01, pipeline-contract quote; pre-existing, not mine), unchanged.
- FOUND: `verify_atoms.py workplan/pipeline-state-graph/atoms/atoms-claude.jsonl` goes 0 -> 2 problems (CLM-038 marker quote, status AMENDED; CLM-041 floor quote, status ACTIVE) because those atoms quote the replaced CLAUDE.md text. Not a registered check (registry lists the script only as a tooling path). The atoms file is outside my assignment: whoever owns workplan/pipeline-state-graph should re-quote or mark them.
- wc -w CLAUDE.md: 5809 before, 5847 after.

## git diff --stat (my files)
 CLAUDE.md                 | 35 ++++++++++++++++++-----------------
 governance/stage-map.yaml |  4 ++--
 2 files changed, 20 insertions(+), 19 deletions(-)
