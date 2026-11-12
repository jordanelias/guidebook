# 01 antagonist — BLIND run (before the draft was opened), 2026-11-12

Repo HEAD at start: `4feb3c0` (the audit files say `186defb`; `git status` showed only `commands.jsonl` modified).
`sha256sum data/guidebook.db` before: c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d
`sha256sum data/guidebook.db` after:  c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d (unchanged)
Scratch: /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ant01/ (fresh `cp data/guidebook.db` per engine run)

## B1 verdict distribution (hs-handshake-matrix.md §0 command)
```
grep -o -E '^\| (REQ-[0-9]{3}|HS-A[0-9]{2}) \| \*\*[A-Z]+\*\*' .../hs-handshake-matrix.md | awk '{print $NF}' | sort | uniq -c
      8 CONTRADICTED
      9 MET
     61 PARTIAL
     33 UNMET
      7 UNPROVEN          (sum 118 = 100 REQ + 18 HS-A)
```
Boundary: MET 1, PARTIAL 9, UNMET 7 (17 rows).

## B2 walkability.py (exit 0)
tables 56, views 23, fk 90. Zigzag (all-FK): every pair involving `render` = `NO PATH` (5 pairs: research, evidence, judgment, synthesis, specification <-> render). Orphans (9): access_duration, access_stakes, data_migrations, decisions, life_stage_modifiers, research_code_leads, rooms, source_locators, weighting_profile.
Re-entrant FK edges (non-null rows): evidence_population_match.gap_id 0; term_aliases.observation_id 0; gap_mining.gap_id 0; search_admissions.ref_id 61; base_parameters.direction_ref_id 0; search_executions.mined_ref_id 11; search_candidates.resolved_ref_id 7; source_value_extractions.promoted_to_rdc_id 0.
Views spanning >1 stage: 12. Confined: 11. `research->evidence` is the only research pair with recvFK/sendFK; `research->judgment`, `research->synthesis` etc. 0 direct FK.
`grep -c walkability governance/check-registry.yaml` = 0.
Lateral: base 6 components; research 4 (isolated gap_mining, research_code_leads, source_locators); judgment 2 (isolated term_adjudications); render 1 table (weighting_profile).

## B3 BU §Z queries (python3 -I, mode=ro)
- user_version 125; sqlite_master tables 57 (incl. sqlite_sequence; walkability counts 56); views 23.
- Q1 specifications: (8, 0, 'pilot-3', '3xMOB')
- Q5: (196, 7, 11, 0, 0) of 203; origins adversarial-pass 1, incidental 4, lead-index 3, planned 195
- Q9: (59, 57, 11, 1)
- Q32: lang_jur_map (70, 19, 48, 0); v_research_scope has 70 rows (cols language, jurisdiction, role); rows whose jurisdiction not an enum member: 19 rows over 17 jurisdictions
- Q31: JurisdictionCode members 36
- Q33: term_aliases (2382, 0, 15, 249); TRANSLATION 996, SYNONYM 1119, NARROWER 146, BROADER 70, DOMAIN 49, DEPRECATED 2
- specifications.governing_refs non-null: 5
- source_value_extractions identity_code: NULL 2, ALL 34, BLIND 3, MOB 170, MS 2, SCI 3 (total 214). base_taxonomy_identity has 23 codes, all `active`; no AMB, no WHEEL.
- pipeline-contract: ratified: false; status: PROPOSED (YAML header). Stage ids = base, research, evidence, judgment, synthesis, specification, render. Criteria per stage (len/with check null): base 9/1, research 1/0, evidence 2/0, judgment 5/2, synthesis 1/1, specification 5/0, render 2/1.  (HS-1 REQ-016 says "five carry check: null" — my count of check:null is 5: 1+0+0+2+1+0+1 = 5. OK.)
- check-registry: 75 checks; blocking 30, advisory 43, informational 2; 5 requires_session.
- claude_md_spine: PASS, EXAMINED 7 stages against 1 SPINE line.
- DR-2026-07-13 line 3: "Status: ACCEPTED (doctrine) — owner ratification "Yes, ratify ALL recent work", 2026-07-21; owner-action precondition OUTSTANDING ...".

## B4 Engine runs (assess_cell.py, fresh copy each; stamp '2026-11-12 05:00')
- 3 x DEAF: provisional, ○, basis T4-6-only-threshold+CO1+T2-direction(proxy_inference), refs=27 sources=31 extractions=122, governing links by x.identity_code on the new specification: [('MOB', 35)]
- 3 x MOB: identical basis/figures; governing links [('MOB', 35)]; sha differs only.
- 3 x BLIND: identical; [('MOB', 35)].
- 12 x MOB: provisional, ○, T4-6-only(regulatory_stratum_only), refs=10 extractions=21, no value.
- 4 x MOB: pending, refs=0 sources=1 extractions=24 (gap written).
- 7 x DEAF: pending, 0 sources (cold entry accepted).
- Gates on the 3 x DEAF copy: validate_evidence_state.py -> "OK cell-state machine: 9 cells, 6 convergence rows" PASS 15 records, EXAMINED 15, exit 0; derivation_handshake_integrity -> determinations 1, EXAMINED 2, VERDICT CLEAN; extraction_follow_up_audit -> PASS, live determinations 1, EXAMINED 1.
- Untouched copy: validate_evidence_state PASS 13 records, EXAMINED 13 (8 cells, 5 convergence rows).
  => the 15 vs 13 difference is the added DEAF determination and its rows; the gate examined the wrong-lens determination and passed it.

## Predictions for comparison against the draft
Anything stating a different distribution than 8/9/61/33/7, a different MET count, `walkability` registry count != 0, MOB-only governing links for DEAF/BLIND, PASS 15, 3 other than what is above, or typing "27" governing sources vs my "refs=27 sources=31" should be checked.
