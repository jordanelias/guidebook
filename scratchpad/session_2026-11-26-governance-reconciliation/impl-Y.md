# Implementer Y log (2026-11-26)

Nothing was committed or staged. The database was not touched.

## A2: tier-system.md marker rule. DONE
Every rule was checked against the ledger with `git grep -n -F` (references/project-standards.md):
- the table: L6944, L6973, L6989, L7303/L7328
- the triangle: L7053, L7071, L7039, L7062/L7078
- OD-64: L7401/L7425
- thin: L7087, L7105, L7123, L7141, L7159
- OD-59: L7307
- T4 only: L7195
- OR-22b and OR-23b: L6164-6190
- OR-23: L4725/L4758
- the derived figure: L3306
- OD-10: L5980

What changed:
- §5 (was :61-68, now :61-81): the dead `skills/guidebook-auditor_SKILL.md` pointer and the old ●/◐/○ lists are replaced by:
  - the owner's table, with a ⚠ row (U+26A0, no FE0F) and "never both";
  - thin, with the owner's exemptions; the project's own inferences and mixed values count as thin;
  - OD-59, the one-stratum rule, OR-22b (correction 4) and OR-23/OR-23b (correction 5);
  - the derived figure;
  - "Not yet ruled" (correction 6: OD-10 added; provision of presence left out);
  - the band()/CHECK sentence (correction 3).
  The heading and section number are unchanged.
- §1 T6 row (:22): "⚠ Superseded" became "Superseded", "weak-band (○)" became "○ … (§5)", and "weak-band honesty rule" became "honesty rule". Lines :15, :19 and :21 are untouched.
- §8 (was :88-100):
  - The band table and the OR-23 callout are replaced by a pointer to §5. The sentence on unretrievable sources is kept (tier, OR-23/OR-23b, the D-0157 return pass, `has_unverified_sources`).
  - :98 now reads "T3-clinical alone is `provisional`; T3-grey alone is `pending`" (band words removed).
  - :100: "weak band" and "never above ○" are removed, "takes ○ even where T4/T5" became "T4 alone ◐, T5 or T6 alone ○ (§5)", and the tail citing the deleted table is gone.
- §9 (:105): "(● band)" removed.
- §10 (:113): "(○ weak)" became "(⚠)".

## A2: T-120 task file. DONE
- Item 2a now names §5, §1 T6 row, §8, §9 and §10. It records that they were applied on 2026-11-26 with corrections 3-5, and tells the task to check and correct them in place, never to write a second text.
- Test T120-04: the before/after ⚠ count would now prove nothing, so it is replaced by "§5 carries the ⚠ row and no banner uses ⚠".
- §3 "Expected output today": CLAUDE.md is removed from the expected hits for `best_practice_synthesis` and the ○ gloss. Another implementer has already changed CLAUDE.md:379-381 and :370; without this edit the task's own stop condition would trip.

## A3: synthesis floor. DONE
- pipeline-contract.yaml:275, synthesis anchor: "Opus-only (rule #2)" became "Opus-class or above, Fable included (rule #2)". The rest of the anchor and `ratified:` are untouched (C6).
- :281-283 opus-routing: "best_practice_synthesis … (Opus-class)" became "Judged synthesis text is authored at the ratified capability floor (Opus-class or above, Fable included), never by a lower tier (rule #2); a determination is computed, not written (owner, 2026-09-09)."
- T-120 item 3: a sentence stating the floor becomes "judged synthesis text", never `specifications`. It quotes the CLAUDE.md floor sentence as already applied and says never to make it read "Only Opus-class models write `specifications`".

## A4 and B9: decision-protocol.md. DONE
- :5 has three version pins ("4.6" ×3), each replaced by the model class: Sonnet-class / Opus-class / Opus-class. The co0007 path now goes to `_superseded/` (B3).
- :13 "the canonical capture format (§3)" became "the capture protocol (§3)".
- :31 "in §3 capture fields" deleted.
- :69 became "Departures are stated in the ledger entry that records the decision."
- Not touched: §2.4, item 3's Co-2 omission, any order-of-authority text.
- Reports wrong: `decisions` still has `delegation` and `delegation_rationale` columns. The table is frozen (D-0188, 2026-09-11) and R30 makes the ledger the single home, so the repoint is right, but "fields deleted" is loose.

## B3: decision-protocol only. DONE
:5 and :126 now point to `workplan/_superseded/workplan-co0007-v3.md` (checked with `git ls-files`).

## B5. DONE
- pipeline-contract.yaml doctrine-recheck: the cadence clause is removed. The criterion now states only what the code checks, the `--cross-ref` pass (scripts/doctrine_recheck.py `check_cross_references`; retained by DR-2026-08-19 §10). References now point to doctrine-recheck.md §2.3 and DR-2026-08-19 §10 instead of §1 and STAGE_TRANSITION.
- pipeline-operations.md:57: "Opus-class authorship" became "Opus-class-or-above authorship, Fable included".
- skills/evidence-metadata-rehabilitation_SKILL.md:26 and skills/functional-deficit-researcher_SKILL.md:201 (heading) and :203 ("an Opus synthesis pass"): changed to the same floor wording.
- Sweep: `git grep -i 'opus.only|opus only' -- governance skills .claude` now finds nothing. Nothing else cites the 6.3 heading.

## B7. DONE
The dead :63 pointer went out with the §5 rewrite. Other mentions of guidebook-auditor (:5 header, §6, §7 table) are historical provenance and were left (B7 names only :63). The skill was never in git history.

## Not done (outside my assignment; reported)
- tier-system.md:49 still uses "⚠ Superseded" and "partial/weak strength" (§3, not in the named sections).
- These still contradict the new §5; they belong to T-120 item 2a, not my items:
  - pipeline-contract.yaml :302 and :326 (weak-band statements for the regulatory stratum)
  - evidence-architecture.md
  - mission-and-epistemics.md:136
  - skills/evidence-auditor_SKILL.md:55-56
  - skills/run-pipeline_SKILL.md
  - references/methodology-evidence-hierarchy-mapping.md:157-165
- T-120 item 2a still lists the CLAUDE.md §6 marker-line edit, which another implementer has already applied.
- State-graph atoms (not my files) no longer match. `build_graph.py --check` gains EVI-052, EVI-055 and EVI-058 (the deleted tier-system §8 rows and the :100 sentence); PIP-01 was already failing before my edits. Re-quoting them is T-120 item 6. PIP-12 and PIP-22 quote changed contract text but are not reported as failures.

## Verification
- matrix_consistency: PASS, EXAMINED 10.
- doctrine_recheck --cross-ref: rc 0, EXAMINED 9.
- test_pipeline_contract: PASS.
- claude_md_spine: PASS.
- schema_reference_audit: PASS.
- test_state_graph_instrument: PASS.
- pipeline-contract.yaml parses as YAML.
- skill_vocabulary_audit and retired_vocabulary are red. Their hits in my two skill files are tokens already there (e.g. `best-practice-synthesis-routing`, IS-PAYWALL); I added no token.
- No section was renumbered.

## git diff --stat (my files)
```
 governance/decision-protocol.md                    | 10 ++---
 governance/pipeline-contract.yaml                  | 13 ++++---
 governance/pipeline-operations.md                  |  2 +-
 governance/tier-system.md                          | 43 ++++++++++++----------
 skills/evidence-metadata-rehabilitation_SKILL.md   |  2 +-
 skills/functional-deficit-researcher_SKILL.md      |  4 +-
 .../T-120-doctrine-amendments-and-deletions.md     |  8 ++--
 7 files changed, 44 insertions(+), 38 deletions(-)
```
