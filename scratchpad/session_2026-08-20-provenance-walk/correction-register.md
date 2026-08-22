# Correction register — 2026-08-20 provenance-walk execution plan
Three read-only Fable 5 passes (factual / strategic / executability) + Opus 5 adjudication.
Every item below was re-measured against the live repo at 83b5b40. Numbered by severity.

## FATAL — plan cannot execute as written

**F1. `emit_batch_sql.py` is blind to every table Phase 0 writes.**
`scripts/research/emit_batch_sql.py:37-49` TABLES list has none of `specifications`,
`specification_source_links`, `convergence_assessment`, `item_bpc_links`. Step 0.3 exits
"no delta". Found independently by two lanes.
FIX: use `scripts/assess/assess_cell.py --db $SCRATCH --emit-sql` (see F2) or feed hand-SQL
straight to `emit_data_migration.py --input`. Do NOT widen TABLES (see F5).

**F2. A determination engine already exists and the plan does not know about it.**
`scripts/assess/assess_cell.py` (34KB) INSERTs `specifications` + `convergence_assessment`,
is pydantic-validated, refuses the canonical DB by design (`:492`), requires `--db` +
`--emit-sql`, emits replayable SQL, and is REGISTERED as check `test_assess_cell_pilot`
(check-registry.yaml:1234). `determine(conn,item_code,population,slug,note)` at `:284` is
general; `PILOT_CELLS` at `:114` is a hardcoded 7-cell roster not incl. A-18xAUT;
`CELL_ID_BASE = 9000`.
CONSEQUENCE: plan's §0 claim "there is no production writer for specifications" is FALSE as
stated (true only as "no writer against canonical"), and Phase 4's ~90-LOC `add-cell` is
partly redundant. The plan's own gate — "if this phase needs a new script, the diagnosis is
wrong" — must confront this prior art.
NOTE: this engine computes state/tier_basis/governing_refs/falsification BY RULE. It cannot
author the requirement-class judgment. Distinguish mechanical derivation from judgment.

**F3. Phase 1 rests on full texts the repo does not hold; no retrieval step is named.**
All 5 retrieval-log artefacts are Crossref METADATA JSON (12-35KB), 2 with a JATS abstract.
No full text anywhere. Phase 1 commands "read in full - not the abstracts, not the payload
metadata" and provides no mechanism.
FIX (verified live this session, all three Co-1 sources ARE obtainable):
  REF-00965 10.1016/j.apacoust.2025.110581 - OpenAlex is_oa=true, hybrid, CC-BY, Applied
            Acoustics vol 233 art 110581. Elsevier linkinghub blocks scraping; needs a
            repository/DOAJ route.
  REF-00966 10.1089/aut.2022.0024 - Europe PMC PMC10726197, free HTML + PDF; also Durham
            repository worktribe.com/output/1189424. EPMC gives vol 5 issue 4 pp 411-422.
            (EPMC fullTextXML endpoint returned 404 - use the HTML/PDF route.)
  REF-00968 10.1080/23311886.2026.2645738 - OpenAlex gold OA CC-BY, T&F PDF + Bristol
            repository + DOAJ. vol 12 issue 1.
Every fetch must land in retrieval-log/<session>/ with a manifest line (mechanism exists).
Define a recorded DEGRADED MODE for any source whose full text is unreachable: authored from
abstract+payload, flagged in confidence_dimensions_absent, stated per-source.

**F4. Phase 0 and Phase 1 are one phase drawn as two, with the gate reversed.**
Phase 0's SQL carries <placeholders> Phase 1 authors; §12 gates Phase 1 BEHIND Phase 0;
Phase 0 applies its migration to append-only canonical (CLAUDE.md rule 3). Phase 1 contains
NO write step at all. Also: `'<JSON array - ...>'` is not valid JSON, so
`validate_evidence_state.py:253-258` FAILs a 'provisional' cell -> preflight cannot go green.
FIX: merge into ONE phase: retrieve full texts -> read -> author prose -> write scratch rows
-> emit -> apply -> render -> walk. Keep the zero-apparatus diff test on the merged phase.

## HIGH — would corrupt execution or the record

**F5. The recursion tripwire is evadable by wording.** Acceptance 4 says "zero NEW scripts";
widening an existing TABLES list or PILOT_CELLS passes literally while violating the spirit.
And §9 cond.2 ("zero new ... in the batch's commits") vs Phase 3 registry lines + Phase 4's
300 LOC are consistent only via an undefined term "the batch".
FIX: define "the batch" = the commits of one R1-R15 admission-to-determination walk; state
Phases 2-4 are apparatus commits outside it under a named whole-plan net-LOC ceiling; rewrite
acceptance 4 as "no apparatus added OR MODIFIED except <named exceptions>".

**F6. Scratchpad hook is sequenced after the acts it exists to make reproducible.**
§5.1's own justification says without it Phase 1 is "as auditable as the author lists were on
2026-08-19". Owner ruling is "saved ALWAYS". FIX: land the hook BEFORE the merged walk phase.

**F7. Backward walk is factually wrong.** REF-00968 is admitted under exec_id **6**
("unpredictable intermittent sound and sensory load...") not exec 1. Verified in
search_admissions. The scripted transcript will not resolve. Walk must traverse exec 1 AND 6,
two query texts, and REF-00968's own artefact + DOI.

**F8. Sideways walk is factually wrong.** DEM does NOT map to AX-AUD or AX-SPR.
population_axis_map: AX-SPR -> NDV/AUT/ADHD (PRIMARY), MH/BRAIN/VES (SECONDARY), EPI
(SITUATIONAL); AX-AUD -> DEAF (ALIAS), DEAFBLIND (PRIMARY). DEM -> AX-COG-O (PRIMARY),
AX-ARO/AX-VIS-L/AX-AMB (SECONDARY). DEM reaches the slug via item_population_links (8/13
items), NOT via the axis map. Correct the hop or the walk falsely fails.

**F9. Phase 4 `add-cell` contradicts the unsuperseded DR.** DR-2026-08-19 §12.5 lists
"Permanently manual: anything touching `specifications` or the reasoning doc". The plan
declares it does not supersede that DR. FIX: argue the mechanical-write/judgment distinction
explicitly or record a one-line DR amendment. Do not leave it silent.

**F10. Stale scratch path.** Plan line 199 hardcodes session UUID 191e3639-...; does not
exist. Parameterise; do not hardcode any session UUID.

## MEDIUM — accuracy of the record

F11. "B-before-E appears ONLY in two comments" is FALSE - also in the DR itself (:879) and
     references/search-log/...:249, both .ignore-hidden. The CONCLUSION survives (check: null
     verified, no enforcing gate); the evidentiary sentence and the "exhaustively verified"
     claim do not. The plan fell into the CLAUDE.md §7 ripgrep trap it cites.
F12. "gap_mining_audit is NOTHING-IN-SCOPE" is FALSE - it prints EXAMINED: 4, PASS, with an
     actionable informational (4 OPEN gaps lack mining_addressability).
F13. "triggers zero of the 66 checks" is not literal - 9 registry checks carry kind `always`
     and do run on the file. "Unchecked for MEANING" is the fair claim.
F14. `research_batch_dod.py --session` will exit 1 on R1 for a fresh session with no Co-1
     searches. State "EXPECT exit 1, R1 only" or drop it from the walk phase.
F15. `validate_evidence_state` will print EXAMINED: 2 (1 cell + 1 convergence), not 1.
F16. Line-number drift: `check: null` at pipeline-contract.yaml:117 (not 116); `def citation`
     spec_page.py:131 (not 132); single_axis check validate_evidence_state.py:328 (not 333);
     registry is 1,655 lines (not 1,656); .git is 16M (not 18).
F17. Counts not reproducible as stated: "68 dangling workplan refs" measures 67-72 depending
     on scope; "27 unmarked quantified claims" measures ~29. Phase 3/5 must RE-DERIVE their
     own lists, not target these numbers.
F18. NEW (found by Opus 5, no lane): `co1_source_type` is NULL on all three Co-1 sources.
     This drives assess_cell.py's G3 grain rule (:` source_grain`), which would silently fall
     to "individual-grain co1" default. Must be set from the sources before any engine run.
F19. NEW: volume/issue NULL on ALL FIVE rows while external sources hold them (REF-00965
     vol 233; REF-00966 vol 5 iss 4 pp 411-422; REF-00968 vol 12 iss 1). B5-a proven from a
     second independent source (Europe PMC / OpenAlex), not just the stored payload.
F20. Owner quotes in §2 "standing authorisations" appear NOWHERE in the repo except the plan
     itself. They may be genuine chat instructions, but they are unverifiable from the record
     and are load-bearing for every Class-B fix. Flag as such; do not launder into evidence.
F21. §11.5 of the DR permits only "search logs, migrations, or the rendered determination" as
     successor artifacts. A 602-line workplan is none. Own the breach in one sentence.

## SURVIVES — verified correct, do not re-litigate
Pipeline census (5/5/5/12, all answer-side tables 0 rows); user_version 60; 0 REF- ids in
site/ or parts/; 93 spec pages "not yet computed"; jurisdictional_values 109 rows / 0 values;
_ES_COLS gap (all 11 columns); next-id domains; REF high-water 00964; 11/11 orphan citations
in bpc-reasoning; site/index.html:28 dangling anchor; parts/v10/part13.md:12 "0 sources";
source_locators 835 rows unread by any live script; epm.gap_id 12/12 NULL; serves_axes 1/106;
terms_used 0/9; connections_produced [] 5/5; regenerate_derived.sh:15-17; spec_page SELECT
lacks doi/url; generate_parts.py:330 stub; classify() blind spots; verify_authors surnames-
only; all 5 payloads BACKFILL; A-18 identity + slug + 13 items; AUT the only 2xEXACT
population; DEM 8/13 nothing above PROXY; REF-00607 T2 PROXY; all three GAP-B01 conditions;
REF-00966 community co-authors (Woolley, andsensory/Emily) now correct in DB; all four
Step 0.2 INSERTs column-correct with every CHECK vocabulary admitting the literals used and
every FK resolving; build_site.py --only writes site/specs/a-18.html; all 9 scripts honour
GUIDEBOOK_DB_PATH.
