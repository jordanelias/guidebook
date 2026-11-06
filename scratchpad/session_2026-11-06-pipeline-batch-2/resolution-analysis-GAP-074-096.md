# Resolution analysis: GAP-074 to GAP-096

**Written:** 2026-11-06, read-only, against branch `ccr-f9662223-3a0e7g` (PR #212) at `5179025`, schema `user_version` 116 (`python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone())"`).
**Nothing here is a ruling or an implementation.** Every figure carries the command that computes it; re-run it rather than trust the figure (CLAUDE.md rule 7a). `MAIN` below is `git show origin/main:data/guidebook.db` copied to a read-only scratch file; `BRANCH` is `data/guidebook.db`.

---

## 0. Summary of verdicts

| Gap | Verdict | One line |
|---|---|---|
| 074 | CONFIRMED | Term undefined; misses GAP-068 and the missing direction on parameter 5 |
| 075 | PARTLY | Derivation gap real; "clinical would misstate the source" is contradicted by `governance/evidence-methodology.md:43`; the writer to reclassify already exists |
| 076 | PARTLY | Inconsistency real; "nothing rules the convention" is wrong: OR-1, OR-1b rule the consequences, OR-1c (open) is the gate; ICF and needs lenses are empty on every row, which the gap misses |
| 077 | PARTLY | Real, and wider than England: Flanders, Ontario, Madrid sources carry the national code |
| 078 | PARTLY | Zero rows true; remedy contradicts OR-16 and names a source already held |
| 079 | CONFIRMED | Same structure as GAP-049 (R1 passes on a targeted search with no source) |
| 080 | PARTLY | `tier_guess` columns still read 1 on 150 and 152; the DOI question is answerable from held payloads; admission of 151 is blocked by GAP-008/GAP-030 |
| 081 | CONFIRMED | The wrong page range is still on the `citation_mining` row; `pages` convention duplicates GAP-043(2) |
| 082 | PARTLY | One stated reason is false (the 210 cm sentence is whole on PDF page 167); the 360-degree square spaces (PDF page 103) are omitted from the list |
| 083 | CONFIRMED | |
| 084 | CONFIRMED | |
| 085 | PARTLY | Understated: every scan row in the database is `pre-screen`, and `v_scan_ledger` counts them as full readings (root cause not recorded) |
| 086 | PARTLY | `R16-scan` does read `source_scans`; three registered checks read `source_value_extractions`; one proposed rule already exists; the real residual is gate-time `claim_text` re-verification |
| 087 | PARTLY | Writer scope confirmed; candidate `harm_finding` re-opens GAP-059 (CLOSED-DECIDED); `contested` has no reader; value/unit/empty-setting is ruled (OR-3, T-1b step 8); lens re-key is gated by OR-1c |
| 088 | PARTLY | Mechanism confirmed; it is the ratified DR-2026-09-26 §2.2(b) refusal; the WebSearch half duplicates GAP-034 |
| 089 | PARTLY | `pages_read` = pages held is documented design; the defect is in `v_scan_ledger` |
| 090 | WRONG | The full Korean sentences verify; the quotes were truncated by the operator |
| 091 | PARTLY | A sanctioned two-step path exists; the proposed "targets with adversarial-pass" contradicts the owner's OQ-7 answer |
| 092 | PARTLY | Misses confirmed; same root cause as 085; a figure inventory is new apparatus with a cheaper alternative |
| 093 | PARTLY | Code confirmed; the overwritten values were NULL, so nothing was lost; finding 184 SURVIVED it as designed |
| 094 | PARTLY | Length mixing confirmed; force half WRONG (parameter 6 holds only N); duplicates GAP-072 and ruled workplan item T-1b step 9 |
| 095 | PARTLY | G01/G02 root cause found; all six advisory checks are red on `MAIN` too (none new); `scan_debt` is red by design |
| 096 | PARTLY | Passes 1, 2 and 5 are open as well; disposing finding 140 cannot unblock closure |

Counts (`grep -c` over the table above): CONFIRMED 5, PARTLY 17, WRONG 1.

---

## 1. Issues the author did not record

Found in the two session records, passes 8 and 9, and the diffs of PRs #211/#212 (`git log origin/main..HEAD`, `git show`). Each is referenced from the gap it affects.

- **U1. No determination is possible on any parameter these batches fed.** `base_parameters.accessibility_direction` is NULL on parameters 4 to 11 (`select parameter_id, accessibility_direction from base_parameters`); `compose_value` returns no interval when the direction is None (`scripts/assess/assess_cell.py:902`). So GAP-074's "consequence", GAP-094's "re-run the determination" and any synthesis on these rows are blocked before units or terms matter. The writer exists (`db.py set-parameter-direction`, `scripts/db.py:1558`); the held text states directions (REF-00468, ext 193: "would have to be increased to 2500 mm ... to accommodate our entire study sample"). Research-data work, no tooling.
- **U2. OR-1 ACTION (2) is unmet on every row of both batches.** "Fill every relevant model on a determination and on the figures under it; do not read the CHECK's 'at least one' as the aim" (`references/project-standards.md`, Owner rulings 2026-10-29). Identity only, ICF and needs NULL: `select created_by_session, count(*), sum(icf_code is not null), sum(needs_code is not null) from source_value_extractions where created_by_session like 'session_2026-11-06%' group by 1` → (batch, 25, 0, 0), (batch-2, 35, 0, 0). Corpus-wide `select count(*), sum(icf_code is not null), sum(needs_code is not null) from source_value_extractions` → (214, 1, 3). Gated by OR-1c (open on `governance/owner-browser.yaml`, `gates: true`) and workplan D-2/T-3.
- **U3. The reading ledger counts a pre-screen as a full reading.** `v_scan_ledger` (`scripts/migrations/114_extraction_slug_and_root.sql:231`) gives READ-NOTHING-FOUND whenever `text_scope = 'full'`, whatever `method`. `scan_debt.py` treats READ-NOTHING-FOUND as paid. Every scan row in the database is `pre-screen` with `open_pass_done = 0`: `select method, count(*), sum(open_pass_done) from source_scans group by 1` → ('pre-screen', 18, 0). `select status, method, count(*) from v_scan_ledger group by 1,2` → READ-NOTHING-FOUND/pre-screen 9 on `MAIN`, 22 on `BRANCH`. So the two batches discharged scan debt (`scan_debt.py` DEBT 477 on `MAIN`, 457 on `BRANCH`) on readings whose absence claims the critic disproved twice (findings 143, 144, 161, 162, 167, 168).
- **U4. GAP-078's remedy ignores OR-16 and names a held source.** OR-16: "read what we hold first". 47 held sources are NOT-READ for parameters 7 and 10: `select parameter_id, status, count(*) from v_scan_ledger where parameter_id in (7,10) group by 1,2`. The Irish TGD M 2022 the gap proposes to fetch is held with text (REF-01018; `grep -h '"ref_id": "REF-01018"' retrieval-log/*/manifest.jsonl`), as are REF-01015 (TGD M) and REF-01014 (ISO/CD 21542). The stash also holds room-acoustics leads from batch 01, three claimed Co-1 (`select ref_id, tier_claimed, substr(title,1,60) from source_locators where ref_id between 'REF-00965' and 'REF-00970'`); batch 01 is the batch whose co-authors were fabricated (CLAUDE.md §5(c)), so any re-admission needs `--verify-authors`.
- **U5. None of the four owner decisions is on the owner's page.** 2026-10-28 (second), ACTION (1): "Put every decision to the owner as a prompt with its full context and its options, never as a bare row". `grep -n 'REF-00468\|England\|GAP-07' governance/owner-browser.yaml` → nothing.
- **U6. GAP-074 does not cite GAP-068** (parameter 5 "may name a space, not a quantity ... a diameter or an area"), which is the same question. The report states square spaces for the 360-degree turn (160 × 160, 210 × 210, 250 × 250 cm, PDF page 103 and 166) beside diameters (ext 193, 2500 mm). Not filed, not in GAP-082.
- **U7. The sub-national class is wider than England.** REF-00995 (Flemish decree) is `BE`, REF-01013 (Ontario Building Code) is `CA`, REF-01029 (CERMI Comunidad de Madrid) is `ES`: `select ref_id, jurisdiction, substr(pub_title,1,60) from evidence_sources where ref_id in ('REF-00995','REF-01013','REF-01029')`. `JurisdictionCode` has no sub-national member (`python3 -c "import sys;sys.path.insert(0,'.');from schemas.enums import JurisdictionCode as J;print([m.value for m in J if '-' in m.value])"` → []).
- **U8. Four passes are open, not one.** `select pass_id, closed_at from adversarial_passes where closed_at is null` → 1, 2, 5, 7. Passes 1 and 2 are held open by ruling/plan (`scripts/db.py:4553` docstring). **Pass 5** (subject `session_2026-10-16-r29-compensating-revert`) has 11 SUSTAINED findings with no disposition (`select verdict, disposition, count(*) from adversarial_findings where pass_id=5 group by 1,2`), no session record under `sessions/` (`ls sessions | grep 2026-10-16` → nothing) and no gap (`select gap_id from gaps where description like '%r29%' or description like '%pass 5%'` → none).
- **U9. Typed columns contradict their own notes.** `tier_guess` is 1 on candidates 150 and 152 (`select candidate_id, tier_guess from search_candidates where candidate_id in (150,152)`), while their notes say "Tier guess 3, not 1". `search_executions.results_found` is 15 on exec 201 while its note says 17. All three candidates carry a "RESOLVED ... by session" marker while `disposition` is still `PENDING-VERIFICATION`: `resolve-candidate` was used as a note channel, which reads as a resolution.
- **U10. REF-00044's DOI is answerable from held payloads.** Its title string embeds `10.1080/10400430903496580` and its `doi` column is NULL; no held payload carries that DOI (`git grep -l 10400430903496580 -- retrieval-log` → none); PubMed's record (`retrieval-log/session_2026-11-06-pipeline-batch/edb5140e7b6d9611.xml`) and a Crossref-deposited reference list (`retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/crossref_10.3141_2145-08.json`, "Steinfeld E., Maisel J., Feathers D., and D'…") both give `10.1080/10400430903520280`. That DOI is on REF-00059 and REF-00192, so add-source would refuse an admission of candidate 151 under R9 until GAP-030's `correct-locator` exists.
- **U11. The `citation_mining` deferral row still states the wrong page range** ("PDF pages 159-173"; `select deferred_reason from citation_mining where local_ref_id='AWM-01'`) and carries `backward = 1, forward = 1` on a deferral (GAP-021's behaviour, decided by GAP-022). The correction is only in scan 15.
- **U12. A 271,499-byte duplicate is committed.** `scratchpad/session_2026-11-06-pipeline-batch-2/awm.txt` is byte-identical to `retrieval-log/session_2026-11-06-pipeline-batch-2/e664fb2f8174f4f8-full-text.txt` (`sha256sum` both → `bae3334434e4025d…`). Rule 5 in spirit; delete in the next commit.
- **U13. Pass 8's harm finding names a column with no meaning.** Finding 142 attacks `contested = 0` on ext 183, and both session records repeat that "no writer changes that column". `source_value_extractions.contested` has no reader: no view (`select name from sqlite_master where type='view' and sql like '%contested%'` → none), no script outside the writer (`git grep -n 'contested' -- scripts schemas | grep -v migrations`; only `scripts/db.py:1921` and `:2949`). Its last reader was a view in `scripts/migrations/057_baseline_2026-08-12.sql:6809`.

---

## 2. Per-gap analysis

Layers are CLAUDE.md §3 (0 = CLAUDE.md and checks; 1 = architecture/schema; 2 = stage tooling; 3 = rows; 4 = supplementary). Line estimates are physical lines in `scripts/ schemas/ .github/ skills/` excluding `scripts/migrations/` (the net-negative measure), tests included.

### GAP-074 — width at a turn (DEC, P1)

1. **CONFIRMED.** `select extraction_id, parameter_id, claimed_value, claimed_unit, setting from source_value_extractions where ref_id='REF-00468' and parameter_id in (4,5)` → 195, 196, 197, 219, 220 on parameter 4 (turn widths), 193, 194 on parameter 5. Adjudications 88, 89, 90 DEFERRED (`select adjudication_id, observation_id, outcome from term_adjudications where observation_id in (97,98)`). TERM-003's definition: "Space for wheelchair 360° rotation" (`select definition from terms where term_id='TERM-003'`).
2. **Root cause.** The parameter list was seeded from base vocabulary by name (owner direction 2026-10-09), not from the quantities sources state, so TERM-003 names a space, not a measure (GAP-068), and nothing names a passage width conditioned on a manoeuvre. The report treats 90°, 180° and 360° turns as alternative bases for one minimum manoeuvring space.
3. **Options.**
   - (a) New term and parameter "turning width" (owner defines; `add-term`, `add-parameter`; new rows re-pointing 195–197, 219, 220). Layer 3 plus an owner definition. More parameters, cleaner quantities.
   - (b) TERM-002 at a turn, expressed as a condition: keep rows on parameter 4, add condition rows/edges ("at a 90-degree turn") via `relate-extraction`. Layer 3 only. Matches OR-2 ("Branches, and an empty headline when all are conditioned").
   - (c) Redefine TERM-003 as a manoeuvring space with a stated measure (diameter or side), and move all turn figures to parameter 5 (`amend-term --field definition`; canonical_en not amendable). Resolves GAP-068 at the same time.
4. **Recommendation.** Put 074 and 068 to the owner as one prompt. The sources favour no option; the ledger's OT-2 pattern (owner approves a new term's definition) means the definition is the owner's under (a) and (c). (b) is the only option needing no new definition and no tooling, but it leaves the 360°/180° alternative bases on different parameters, which is finding 175's objection. Do not file further turn rows until decided.
5. **Cost.** No tooling. Callers to sweep on (c): `terms.definition` restatements in prose (`grep -rn "360" references/ governance/ | grep -i turning`).
   Acceptance: none mechanical; the adversarial lens L3 re-reads 175.
6. **Dependencies.** With GAP-068. Blocks the parameter-5 determination together with U1 (direction). Blocks part of GAP-082 (the square spaces).

### GAP-075 — tier of REF-00468 (DEC, P1)

1. **PARTLY.** True: `TIER_MAP[("grey","intrinsic")] = 3` (`schemas/tier_derivation.py:63`), so the "occasionally grey" T1 wording of `governance/tier-system.md:15` is unreachable, and `band(3,'grey')` is WEAK (`schemas/tier_derivation.py` `band`). False: "changing evidence_type to clinical ... would misstate what the source is". `governance/evidence-methodology.md:43`: "`grey` (grey literature, organizational reports **not classifiable above**) ... Both are transitional states — every source should eventually resolve to a classified type." Publication status is carried separately by `grey_flag`, which is orthogonal to type: `select evidence_type, grey_flag, count(*) from evidence_sources group by 1,2` → ('code', 1, 1) exists (REF-01016). `tier-system.md:19` also lists "grey-literature primary research" under T3, so the ladder text itself is two-sided. The writer exists: `amend-source --field evidence_type --replacement clinical --scope …` (`scripts/db.py:1437–1451`).
   Missing: the same class is already filed grey T3: REF-01005 (HUD 1979, the measurement GAP-037 relies on) and REF-01008 (FHWA 1980) (`select ref_id, evidence_type, tier from evidence_sources where grey_flag=1`).
2. **Root cause.** `grey` is used as a publication-route label when the doctrine defines it as a residual type; the ladder's T1 sentence was never reconciled with the derivation table.
3. **Options.**
   - (a) Reclassify by type: `clinical` with `grey_flag = 1` kept; scope `lower_control` (T3 clinical, band ●) or `high_control` (T1, band ●). Data PR, `amend-source`, no tooling. Applies to REF-00468, REF-01005, REF-01008. Then correct `tier-system.md:15` ("occasionally grey") by a ledger entry + DR mark.
   - (b) Keep grey T3, band ○. Correct `tier-system.md:15` to remove the T1 mention. Doctrine-only.
   - (c) Add `("grey","high_control") → 1` to the ladder. Tooling PR (schema CHECK parity, `VALID_SCOPES_BY_TYPE`, tests) then data. More apparatus; contradicts methodology §1.1's "transitional" reading.
4. **Recommendation.** Owner decision, because tier definitions are doctrine (CLAUDE.md §8). The existing texts favour (a): evidence-methodology.md:43 and the orthogonal `grey_flag`. Which scope (high/lower control) is a judgment for the reader with the warrant (an incremental mock-wall measurement study of 495 users: `tier-system.md:15` "biomechanical control on the parameter" against `:19` "cross-sectional, observational"); `amend-source` records the warrant. (c) is the most expensive and the least supported.
5. **Cost.** (a): 0 lines. (c): about +6/−0 in `schemas/tier_derivation.py`, a schema CHECK migration if scope is CHECKed, + tests. Sweep on any option: prose restating "grey → T3" (`grep -rn "grey" governance/tier-system.md governance/evidence-methodology.md references/project-standards.md governance/owner-browser.yaml`).
   Acceptance (a): `select ref_id, evidence_type, scope, tier, grey_flag from evidence_sources where ref_id in ('REF-00468','REF-01005','REF-01008')`, and `adjudication_integrity` / tier-consistency stays green.
6. **Dependencies.** None blocking. Affects every band on REF-00468's 10 rows (`select count(*) from source_value_extractions where ref_id='REF-00468'`).

### GAP-076 — lens convention (DEC, P1)

1. **PARTLY.** Inconsistency CONFIRMED: `select ref_id, identity_code, count(*) from source_value_extractions where ref_id in ('REF-00468','REF-00987','REF-00992','REF-01028','REF-01031','REF-01032') group by 1,2` → ALL and MOB mixed within REF-00987, REF-00992, REF-01028, REF-01031, REF-01032. "Nothing rules the filing convention" is wrong in part:
   - OR-1 (2026-10-29): "a figure reaches a determination only through the lens tags written on that figure"; ACTION (2) fill every relevant model.
   - OR-1b (2026-10-29 second): "No, ALL reaches only an ALL determination". So an ALL row on a Korean clause headed for persons with disabilities is invisible to every MOB determination. The convention is not cosmetic.
   - `governance/population-taxonomy.md` §1.3: ALL's "typical uses: Universal Mode code compliance values (e.g., minimum corridor width per code)". This favours ALL for code minima, against OR-1b's consequence.
   Missing: ICF and needs lenses are empty on all 60 rows (U2), and OR-1c (how a figure carries several codes of one model) is the open owner gate on the owner's page.
2. **Root cause.** The operator filed one lens column by a per-row reading with no stated rule, while the ruled requirement is all relevant models; the convention cannot be settled for identity alone while OR-1c is open.
3. **Options.**
   - (a) Rule: tag the population the clause or its heading names (MOB), else ALL. The later rows used this. OR-1 and OR-1b favour it (a figure reaches a group only through its own tag).
   - (b) Rule: code-compliance values are ALL (population-taxonomy §1.3). Consequence under OR-1b: no code figure reaches a MOB determination; MOB determinations would rest on studies only.
   - (c) Defer identity until OR-1c is answered, then do D-2 for all lenses at once.
   Re-keying: D-2 as planned "fills a NULL lens column ... only where a quote names the users" (`workplan/2026-10-23-pipeline-resolution-workplan.md:150`). Changing a non-NULL `identity_code` has no writer; a second row duplicates the figure (rule 5) and reads as a contest.
4. **Recommendation.** (c) with (a) as the stated proposal: ask OR-1c and the identity convention in one prompt, then re-key all lenses in one D-2 data PR. Do not build a lens re-key writer before OR-1c, because OR-1c may change the shape (row-per-combination or link table) and the writer would be built twice.
5. **Cost.** After OR-1c: a re-key writer is about +40/−0 (amend path with old-value ledger and the engine-column refusal, `scripts/db.py:8647`); or 0 if OR-1c chooses a link table that D-2 writes. Sweep: views reading `identity_code` (`select name from sqlite_master where type='view' and sql like '%identity_code%'`), `judgment_handoff_shape`, `assess_cell` lens routing.
   Acceptance: a query that fails today: `select count(*) from source_value_extractions where created_by_session like 'session_2026-11-06%' and icf_code is null and needs_code is null` → 60 now; target 0 or a recorded not-relevant warrant per OR-1.
6. **Dependencies.** Blocked by OR-1c. Blocks D-2, T-3, any synthesis on parameters 4–11. Related findings 147, 171, 172.

### GAP-077 — England-only instrument (DEC, P2)

1. **PARTLY.** True for REF-00992: `select count(*) from source_value_extractions where ref_id='REF-00992' and jurisdiction='UK'` → 25. Wider: U7.
2. **Root cause.** The jurisdiction vocabulary is national only (`schemas/enums.py JurisdictionCode`), while instruments are often sub-national.
3. **Options.**
   - (a) Sub-national codes (ISO 3166-2 style, e.g. `UK-ENG`, `BE-VLG`, `CA-ON`, `ES-MD`). Tooling: enum, `jurisdiction_db_vocabulary.py`, `jurisdiction-philosophy.md` §3.3, `lang_jur_map` keys and OR-8's bucket members (jurisdiction and language pairs). Then re-file by new rows.
   - (b) A scope statement on the source, not the row: `evidence_sources.notes` or `setting` already carry free text; render "England only". No tooling; not queryable.
   - (c) Leave national; record in the ledger that a national code means "an instrument of that state, possibly sub-national in reach".
4. **Recommendation.** Owner decision (jurisdiction is doctrine, CLAUDE.md §8). Ask it once for the class, not for England. No ruling favours a sub-national code; the 2026-09-28 jurisdiction-scope ruling and OR-8 are written in national buckets, which favours (b) or (c) unless the owner wants (a). Note the cost of (a): re-filing is new rows across four sources (rule 5 duplicates, unless an amend path for `jurisdiction` on extractions is built).
5. **Cost.** (a) about +20/−5 plus migrations and a data re-file; (b)/(c) 0.
6. **Dependencies.** Interacts with OR-8 buckets (T-6b). Blocks nothing else.

### GAP-078 — parameters 7 and 10 empty (EG, P1)

1. **PARTLY.** Zero rows true: `select parameter_id, count(*), count(distinct ref_id) from source_value_extractions group by 1` → no row for 7 or 10. "After four sources were read against the whole catalogue": those were pre-screens (U3). Remedy contradicts OR-16 and names a held source (U4).
2. **Root cause.** Reading order: the held corpus is mostly unread for these parameters, and the batches fetched rather than read held texts.
3. **Options.**
   - (a) D-3 first: full-read catalogue scans of held sources, starting with REF-01018, REF-01015, REF-01014 and the other held codes, recording READ-NOTHING-FOUND honestly. Research-data PR.
   - (b) Re-admit the batch-01/02 acoustic stash leads (REF-00965 to REF-00970 and others) with author verification.
   - (c) Fetch new acoustic and lighting standards (the gap's proposal), after (a).
4. **Recommendation.** (a), then (b), then (c), per OR-16. Parameter 8 resting on one numeric source is the same reading-debt problem.
5. **Cost.** No tooling. Depends on the ledger fix (PR-A) so that the debt figure is honest.
6. **Dependencies.** After PR-A (U3). Parameters 7 and 10 also lack a direction (U1).

### GAP-079 — no Co-1 source for door, corridor or turning dimensions (EG, P1)

1. **CONFIRMED.** `select exec_id, target_evidence_type, results_found, results_admitted from search_executions where target_evidence_type='co1' and created_by_session like 'session_2026-11-06%'` → (198, co1, 1, 0), (201, co1, 15, 0). Structurally the same defect as GAP-049 (R1 "passes when Co-1-targeted searches exist").
2. **Root cause.** R1's enforcer counts targeted searches, not Co-1 coverage; the searches used general indices where DPO guidance is not indexed (GAP-049's own 2026-09-28 note says: try a DPO's own repository instead).
3. **Options.** (a) Research: direct retrieval from the named DPO repositories (the gap's list), logged first, per `governance/co1-operational.md`. (b) Doctrine/tooling: make R1 report "targeted, none admitted" distinctly. GAP-049 already asks the structural question.
4. **Recommendation.** (a) as research; fold the structural point into GAP-049 with a cross-reference note rather than a second structural gap.
5. **Cost.** None for (a).
6. **Dependencies.** None. Its result feeds OR-5 ("academically sound" Co-1 figures set a value).

### GAP-080 — six candidates without full text (RP, P2)

1. **PARTLY.** Candidates confirmed (`select candidate_id, disposition, tier_guess from search_candidates where candidate_id between 150 and 155`). "Tier guesses ... corrected after the pass" is false in the column (U9). The DOI question is answerable (U10). Missing: admission of 151 is blocked by GAP-008/GAP-030 (no writer sets `source_locators.doi`).
2. **Root cause.** Paywalled primary studies; a stash with shuffled DOIs.
3. **Options.** (a) Owner library route, then admission reusing stash ids. (b) Read the open Steinfeld 2010 data through REF-00468 itself (same dataset, held), and admit the journal papers only if they add figures. (c) Leave staged.
4. **Recommendation.** (b) now, (a) when the owner provides a route. Settle 151's id as REF-00044 on title match; its title-embedded DOI is the pre-reset error (U10). Admission of 151 waits on GAP-030.
5. **Cost.** None; GAP-030's `correct-locator` is its own tooling item.
6. **Dependencies.** Blocked by GAP-030 (for 151). Koontz/Steinfeld share an author (finding 157): independence check before counting both.

### GAP-081 — citation mining of REF-00468 deferred (RP, P2)

1. **CONFIRMED.** `select backward, forward, deferred_reason from citation_mining where local_ref_id='AWM-01'`. U11: the row's page range is still wrong. The `pages` = PDF count point is GAP-043(2) (page-numbering convention), a duplicate.
2. **Root cause.** Scope choice; GAP-025 assignment mechanism.
3. **Options.** One: run backward (bibliography at PDF page 170) and forward passes; `log-mining --discharge-deferral` with notes, which also corrects the page range.
4. **Recommendation.** Assign to the next research batch (GAP-025 mechanism). OR-20 does not apply (REF-00468 is not T4–T6).
5. **Cost.** None.
6. **Dependencies.** None.

### GAP-082 — stated figures left unfiled (RP, P2)

1. **PARTLY.** Scan notes confirm most items (`select scan_id, ref_id, substr(notes,1,200) from source_scans where created_by_session like 'session_2026-11-06%'`). False reason: the 210 cm scooter figure is whole on PDF page 167 (`python3 -I` sweep of `e664fb2f8174f4f8-full-text.txt` by `[PDF page N of 173]` blocks: "at least 210 cm" on page 167). Omitted: 360-degree square spaces 160 × 160, 210 × 210, 250 × 250 cm (PDF pages 103, 166) (U6).
2. **Root cause.** Pre-screen keyword reading (085/092) and the undefined turn quantity (074/068).
3. **Options.** (a) File during D-3 full reads, rows or declinations with reasons. (b) Wait for 074/068 for the turn figures.
4. **Recommendation.** (a) for non-turn figures now; (b) for turn and square figures.
5. **Cost.** None.
6. **Dependencies.** Turn figures blocked by 074/068. After PR-A.

### GAP-083 — Portuguese decree held as 5 of 20 pages (EG, P2)

1. **CONFIRMED.** `select ref_id, text_scope, pages_read, pages_total from source_scans where ref_id in ('REF-01032','REF-01026')` → two rows (partial, 5, 20). REF-01026 is the same title, UNVERIFIED, not superseded (`select ref_id, verification_status, superseded_by_ref_id from evidence_sources where ref_id in ('REF-01026','REF-01032')`). Whether `test_db_integrity` D04 sees the pair is [UNVERIFIED]: verify with `python3 scripts/tests/test_db_integrity.py | grep D04` and its author+year+title key on both rows.
2. **Root cause.** Partial retrieval in batch 23.
3. **Options.** (a) Retrieve the full Diário da República issue (Wayback per §7 if blocked), `full_text.py`, full-read; then `supersede-source REF-01026` → REF-01032 if identical. (b) Leave partial.
4. **Recommendation.** (a); `supersede-source` exists (GAP-060 closed-fixed).
5. **Cost.** None.
6. **Dependencies.** None.

### GAP-084 — UK 1500 × 1500 mm spaces (EG, P3)

1. **CONFIRMED.** `select jurisdiction, claimed_value, claimed_unit from source_value_extractions where parameter_id=5 order by jurisdiction` → ES, ES, KR, SG, SG, US, US, US; no UK.
2. **Root cause.** The answer is in AD M diagrams not read and in BS 8300, not held; and the parameter-5 quantity is undefined (068).
3. **Options.** (a) Render AD M diagram pages with `scripts/research/page_image.py` (held source, OR-16). (b) Obtain BS 8300 (paywalled; owner route).
4. **Recommendation.** (a) during D-3; (b) only if (a) is silent.
5. **Cost.** None.
6. **Dependencies.** After 074/068 for what to file.

### GAP-085 — every reading is pre-screen (AUDT, P2)

1. **PARTLY (understated).** U3: all 18 scan rows in the database are pre-screen, not only these batches', and the ledger counts them as full readings.
2. **Root cause.** `v_scan_ledger`'s status rule reads `text_scope` and ignores `method`, so the cheap reading discharges the same debt as the full one; nothing makes the full read worth doing.
3. **Options.**
   - (a) Tooling: in `v_scan_ledger`, READ-NOTHING-FOUND only when `text_scope='full' AND method='full-read'`; a full-scope pre-screen falls to READ-PARTIAL (debt). One schema migration (view recreate), a test case. Then D-3 full reads (data).
   - (b) Process only: D-3 full reads; leave the view. Debt figure stays false meanwhile.
   - (c) Writer-retire `pre-screen` in `record-scan` (refuse new rows). Cannot verify a read happened; forces mislabelling.
4. **Recommendation.** (a) then D-3. It is the cheapest change that makes every later gate honest, and OR-11a ("`verified` requires a full-scope scan", T-1b step 10) will need exactly this distinction.
5. **Cost.** (a): view migration (excluded from count); `scripts/tests/test_scan_contract.py` +8 (a pre-screen full-scope reading leaves a pair READ-PARTIAL); `scan_debt.py` docstring +1. Sweep: `scan_debt.py`, `research_batch_dod.py` R16-scan (reads `source_scans` directly, unaffected), `governance/context-map.yaml` (regenerated), prose restating the ledger rule (`grep -rn "READ-NOTHING-FOUND" governance/ references/ architecture/ workplan/`).
   Acceptance: before the fix, on `BRANCH`: `select count(*) from v_scan_ledger where status='READ-NOTHING-FOUND' and method='pre-screen'` → 22 (the test asserting 0 is red); after, 0, and `scan_debt.py` DEBT rises by that amount.
6. **Dependencies.** Unblocks honest work on 078, 082, 083, 084, 089, 092, and T-1b step 10.

### GAP-086 — DoD gate does not read extractions (SW, P1)

1. **PARTLY.** "Reads neither source_scans" is false: R16-scan reads `source_scans` (`scripts/audit/research_batch_dod.py:1025`), for admissions only. "Checked only by db.py's write-time verbatim test" is false at corpus level: `extraction_relations_integrity` (blocking; its check 4 already enforces "a condition row has its edge"), `judgment_handoff_shape` (blocking), `test_db_integrity` (blocking) and `extraction_follow_up_audit` read `source_value_extractions` (`python3 scripts/run_checks.py --list | grep -E 'extraction_relations_integrity|judgment_handoff_shape|test_db_integrity'`; `GUIDEBOOK_DB_PATH=BRANCH python3 scripts/audit/extraction_relations_integrity.py | tail -3` → EXAMINED: 271, CLEAN). The DERIVE (`... | grep -c 'EXAMINED: 0'` → 2) counts R5 and R11, which are honest nothing-in-scope results (no non-English admission, no alias), not a defect.
   True residual: no gate re-verifies `claim_text` against bytes after write (`observation_verbatim_audit.py` does this for `observed_terms` only); a batch that reads but admits nothing gets no scan rule.
2. **Root cause.** The DoD script is admission-centred; extraction integrity lives in corpus checks, and the one backstop for quotes was built for observations only.
3. **Options.**
   - (a) Widen `observation_verbatim_audit.py` to also walk `source_value_extractions.claim_text` with the same `locate_quote`, classes and ratchet baseline. Reuse.
   - (b) New DoD rules (the gap's five). Two duplicate existing checks; "unit in the parameter's family" needs a curated parameter→unit map (rule 8) or the length family (094).
   - (c) Nothing; rely on the critic.
4. **Recommendation.** (a). Drop the condition-edge rule (exists), the unit rule (no derivable family yet), and the scan-note-cites-sweep rule (prose, unverifiable). Locator presence is a cheap SQL predicate that could join (a) as a reported class.
5. **Cost.** (a) about +25/−5 in `observation_verbatim_audit.py` (rename optional; a rename is a rule-4 sweep of the registry and `test_scan_contract` A04), two baseline keys in `governance/research-contract-baseline.json`.
   Acceptance: `test_scan_contract` gains a case inserting an extraction with an invented `claim_text` by SQL on the copy (the A04 pattern at `scripts/tests/test_scan_contract.py:856`) and asserting the audit exits 1; run it before the change to show it red.
6. **Dependencies.** None. Pairs with PR-A.

### GAP-087 — no writer corrects lens, locator, setting, contested, candidate harm/title, scan note (SW, P1)

1. **PARTLY.** True: `_AMENDABLE_SVE_FIELDS` is figure_role, comparator, extraction_method, extraction_status, root_type, root_ref_id (`scripts/db.py:8647`). Per item:
   - Candidate `harm_finding`: GAP-059 is CLOSED-DECIDED: "`search_candidates.harm_finding` has no reader outside `db.py` and adversarial lens S1, and the harm reached exec 171, where `amend-search` raises it and R7 reads it; nothing was built" (`sessions/session_2026-10-01-research-batch-23.md:133`). Here exec 197 and 203 carry the flag (`select exec_id, harm_finding from search_executions where exec_id in (197,203)`). Re-opening it needs a reason GAP-059 did not weigh; none is given.
   - Candidate `title`/`tier_guess`: no reader (`git grep -n tier_guess -- scripts schemas skills .claude governance | grep -v migrations` → writer only).
   - `contested`: no reader (U13).
   - Setting/value/unit reformat: ruled. OR-3: "Reformatting a figure's value, unit or empty setting in place ... narrows D-0168 ... for reformatting only"; T-1b step 8 "widens `amend-extraction` to unit, value and NULL `setting`" (`workplan/2026-10-23-pipeline-resolution-workplan.md:133`), not built. Ext 193's setting is a non-NULL wrong value, outside OR-3.
   - Locator (ext 211), `source_section`: no writer and no ruling.
   - Lens: GAP-076 / OR-1c.
   - Scan note: a corrected reading is a new `source_scans` row by design (append-only reading record, AUTOINCREMENT "must never come to mean a different reading", migration 103 DDL).
2. **Root cause.** The amend surface was grown field by field (GAP-013(1)), and the batch asked for writers for every column it got wrong, including unread ones.
3. **Options.**
   - (a) Build T-1b step 8 as ruled; add `loc_*`, `source_section` and non-NULL `setting` to `_AMENDABLE_SVE_FIELDS` with the old value ledgered (the root_type precedent in the same comment block). These are transcription fields, not the value or quote D-0168 protects.
   - (b) T-1b step 8 only; correct locators by notes.
   - (c) Writer-retire `--contested` on `add-extraction` (unread), leave candidate fields per GAP-059.
4. **Recommendation.** (a) + (c). Whether widening to locators and non-NULL setting needs an owner ruling: D-0168 is DG-NON, but the sentence the ledger quotes is about "a wrong claimed_value"; locators are not named. State it in the PR and ask only if the owner wants (owner-sheet Q8). Close the candidate items as decided by GAP-059.
5. **Cost.** (a) about +6/−1 (frozenset and help text) plus T-1b step 8's own estimate; (c) −2 (`scripts/db.py:1921` flag, `"contested"` in `_COLS` at `:8271` stays because data migrations INSERT the column, rule 5: writer-retire, not drop). Sweep: `test_db_amend_writers.py`, `--help` text, the "ONLY these two" help string at `scripts/db.py:2050` (already stale: six fields), `dbcore.ENGINE_EXTRACTION_COLUMNS` (setting and loc_* are not engine columns, so no live-determination refusal needed).
   Acceptance: a test that `amend-extraction --field loc_clause` is refused today and accepted after, with the old value in notes.
6. **Dependencies.** T-1b step 8 must merge before D-1 (workplan). Lens part blocked by OR-1c.

### GAP-088 — result payload linkable only if query names its host; WebSearch leaves no payload (SW, P2)

1. **PARTLY.** Mechanism confirmed (`scripts/research/retrieval_log.py:1238–1242`). It is the ratified DR-2026-09-26 §2.2(b) refusal ("now used as a refusal. … it is what refuses C9 as a result of exec 91", DR line 377; ratified 2026-09-27). The Europe PMC checks are availability lookups of their own, not results of the PubMed search; the existing model is to log each as its own execution (origin `incidental`, engine Europe PMC, query text = the URL), which links. The WebSearch half is GAP-034 (its 2026-11-06 correction note already says so).
2. **Root cause.** Operator logged the Europe PMC calls as notes on another search instead of as searches.
3. **Options.** (a) Data: log the two Europe PMC lookups as executions linking `198b3da3fb3d7b6a.json`, `c4c1f76df9877588.json`. (b) Tooling: link by manifest `ref_id`/purpose (weakens §2.2(b); needs a DR amendment).
4. **Recommendation.** (a); close GAP-088 as by-design plus duplicate of GAP-034.
5. **Cost.** 0.
6. **Dependencies.** None.

### GAP-089 — `pages_read` counts pages held (SW, P2)

1. **PARTLY.** True, and documented: `record_scan` docstring "pages read / pages total come from the file's own page markers" (`scripts/db.py:7113`); `--text-scope` help "how much of the document the file read holds". Ext row: `select scan_id, pages_read, pages_total, method from source_scans where ref_id='REF-00468'` → (10, 173, 173, pre-screen), (15, 173, 173, pre-screen). The column name misleads; the harm is in the ledger (U3).
2. **Root cause.** As 085.
3. **Options.** (a) The ledger fix (085a); no new column. (b) The gap's operator-set "pages read in full" field checked against quote page markers: new column, new writer flag, new check. (c) Rename `pages_read` → `pages_held` (rule 4 sweep across view, writer, tests, prose).
4. **Recommendation.** (a); close 089 into 085. (c) only if a reader is shown to be misled after (a).
5. **Cost.** 0 beyond 085.
6. **Dependencies.** 085.

### GAP-090 — Korean quote cannot cross a line break (SW, P2)

1. **WRONG.** `normalise_quote` keeps letters and digits only and drops all whitespace (`scripts/research/retrieval_log.py:598`, body ends `"".join(ch for ch in s if ch.isalnum())`). Computed: `retrieval_log.quote_in_artefacts(<full sentence>, ref_id='REF-01031')` → `(True, 'found in session_2026-10-01-research-batch-23/b71c64f1a9b3125f-text.txt, retrieved for REF-01031')` for both "휠체어사용자가 통행할 수 있도록 접근로의 유효폭은 1.2미터 이상으로 하여야 한다." (ext 215's sentence) and "복도의 유효폭은 1.2미터 이상으로 하되, 복도의 양옆에 거실이 있는 경우에는 1.5미터 이상으로 할 수 있다." (ext 209's). The quotes were cut by the operator. The CORRECTED note appended to GAP-056 is therefore also wrong.
2. **Root cause.** Operator assumption, not tested.
3. **Options.** (a) Data: second rows with the full sentences are contests by D-0168; OR-3 does not cover `claim_text`. Leave the rows, record the correct quotes in notes via `amend-extraction ... CONFIRMED` path. (b) Leave.
4. **Recommendation.** Close GAP-090 CLOSED-FALSE-POSITIVE (or the live CLOSED-% term, `select distinct status from gaps`), with the computation above as the reason; amend GAP-056's appended note. Teach the batch skill nothing new.
5. **Cost.** 0.
6. **Dependencies.** None.

### GAP-091 — critic-prompted search cannot be labelled at write time (SW, P2)

1. **PARTLY.** Literally true at `log-search` (`scripts/db.py:665`). A sanctioned path exists: log `incidental`, then `amend-search --set-origin adversarial-pass` (accepts NULL pass id, `scripts/db.py:3939`) and later `--set-origin-pass-id` (NULL → value, `:4000`). "Allow targets with origin adversarial-pass" contradicts the refusal "A lookup targets no tier -- that is what keeps it out of v_coverage_branch's Co-1 count" (`:660`) and the owner's OQ-7 answer "R1 no" (`references/project-standards.md:4161`).
2. **Root cause.** Operator did not use the two-step path; the coverage exclusion is ruled.
3. **Options.** (a) Data: `amend-search` execs 199 and 200 to `adversarial-pass` with pass id 8. (b) Tooling per the gap (contradicts OQ-7).
4. **Recommendation.** (a); close as decided by OQ-7.
5. **Cost.** 0.
6. **Dependencies.** None.

### GAP-092 — keyword screens missed figures (SW, P2)

1. **PARTLY.** Misses confirmed (findings 143, 144, 161, 162, 167, 168). No committed tool produces a pre-screen (`grep -rn pre-screen scripts/research/` → none); each session wrote its own grep. Same root cause as 085.
2. **Root cause.** As 085: a reading that cannot be checked is accepted as a reading.
3. **Options.** (a) 085a + D-3 full reads; the critic's sweep remains the check. (b) A figure inventory: `full_text.py --figures` printing every number with a unit or ratio, per page (about +35/−0), read by the operator and the critic. Net-positive; must name the exception. (c) Both.
4. **Recommendation (revised after the owner's 2026-11-06 steer to minimise code; see §E).** RULE-OR-PROSE first: put the sweep in the scan procedure as one command line (a `grep -noE` over the page-marked text for a number followed by a unit or ratio, e.g. `[0-9]+([.,][0-9]+)? ?(mm|cm|m|N|lbf|%|:)`), and require an absence statement in a scan note to quote the sweep it ran. That is the same derivation as (b) with zero code, and nothing smaller closes the defect (a rule without the command repeats the keyword failure). Build (b) only if the prose one-liner proves insufficient (non-Latin numerals, unit words). The earlier text of this item, kept for the record: (c), both. (a) makes the debt figure honest but does not make a reading catch a figure; (b) is what closes the defect this gap names, because both batches' misses were spelling variants of numbers that a mechanical number-and-unit sweep finds (the critic found them exactly that way, findings 144, 167, 168). It is a real addition, recommended. Section 8 test: it reads the derived page-marked text that `full_text.py` already writes; its readers are the operator writing `record-scan` and the antagonist checking absence claims; without it, a code's stated minimum is recorded as absent and the guidebook prints a determination that omits it (or says no code sets a value) while every gate is green. It is a derivation (rule 8), not a curated list. No deletion genuinely offsets it.
5. **Cost.** (b) about +35/−0 in `scripts/research/full_text.py`, no check entry (a reading aid, not a gate). Acceptance: run it on `retrieval-log/session_2026-10-30-rest-landing-parameter/0e5d4dee25b341f4-full-text.txt` and show it lists "2.1m" (para 1.13(a), p19) and "1500mm x 1500mm" (pp26, 35), the figures the first scan declared absent (finding 143).
6. **Dependencies.** 085.

### GAP-093 — update-locator rewrites created_* (SW, P3)

1. **PARTLY.** Code confirmed (`scripts/db.py:5684–5691`). On `MAIN`, REF-00468's `created_by_session` and `created_at` were NULL (`select created_by_session, created_at from source_locators where ref_id='REF-00468'` on `MAIN` → (None, None)), as on every stash row (`select status, created_by_session is null, count(*) from source_locators group by 1,2` on `MAIN` → REFERENCE-ONLY/1/880, RETIRED/1/13). Nothing was overwritten; the migration date stays in notes. Finding 184 SURVIVED it as designed.
2. **Root cause.** `source_locators` has no `updated_*` columns, and `batch_capture_report._resolve` attributes a table by its first session column only (`scripts/audit/batch_capture_report.py:54`), which is GAP-036.
3. **Options.** (a) Docstring fix only (0 net). (b) Add `updated_at`/`updated_by_session` (migration), write them in `update_locator`, and make `_resolve` OR over all session columns (closes GAP-036 too).
4. **Recommendation.** (b) in one small tooling PR with GAP-036, because it removes the misuse and the attribution blindness together; otherwise (a).
5. **Cost.** (b) about +6/−4 (writer, `_resolve`), migration excluded; sweep the source_locators pydantic model if one exists (`git grep -n source_locators -- schemas`), `validate_pydantic_schemas`, `pipeline_walk.py`.
   Acceptance: `batch_capture_report.py` for `session_2026-11-06-pipeline-batch-2` lists the PROMOTED update after the fix; a test on a copy that an UPDATE-only session is attributed.
6. **Dependencies.** With GAP-036.

### GAP-094 — mixed units on 4, 6, 9, 11 (ST, P2)

1. **PARTLY.** Length mixing confirmed: `select parameter_id, claimed_unit, count(*) from source_value_extractions where parameter_id in (4,5,9,11) and figure_role='claim' group by 1,2` → 4: m 9, mm 10; 5: m 3, mm 3; 9: cm 2, m 3, mm 11; 11: m 5, mm 2. Force half WRONG: parameter 6 holds N only (`select claimed_unit, count(*) from source_value_extractions where parameter_id=6 group by 1` → NULL 1 (an absence row), N 10). Duplicate of GAP-072, and of a ruled, planned item: OR-10 "Yes, convert and show both — Round to nearest 1/4" or 5mm" → T-1b step 9 "the length family; bumps RULE_VERSION" (`workplan/2026-10-23-pipeline-resolution-workplan.md:133`). "Derived from the unit table": no unit table exists (`select name from sqlite_master where type='table' and name like '%unit%'` → none); `NOTATION_FAMILIES` is explicitly a definition, not a curated fact (`scripts/assess/assess_cell.py:498–510`).
2. **Root cause.** T-1b step 9 not built.
3. **Options.** One: build T-1b step 9.
4. **Recommendation.** Close GAP-094 as duplicate of GAP-072; keep GAP-072 open as the pointer to T-1b step 9.
5. **Cost.** Workplan's estimate for step 9; acceptance as the workplan states (`('36','in','>=')` reads `(Fraction(4572,5), None)`).
6. **Dependencies.** Even when built, parameters 4–11 compose nothing until U1 (direction).

### GAP-095 — undiagnosed advisory failures; G01/G02 red on main (AUDT, P2)

1. **PARTLY.** G01/G02 red confirmed (`TMPDIR=<scratch> python3 scripts/tests/test_scan_contract.py | grep -E '✗|RESULTS'` → G01 ✗, G02 ✗, 107/109). Root cause found (below). The six advisory checks, run against `MAIN` and `BRANCH` databases (`GUIDEBOOK_DB_PATH=<db> python3 <cmd>`), are red on both, none introduced by #212:
   - `scan_debt`: rc 1 both; DEBT 477 `MAIN`, 457 `BRANCH`. Red by design ("advisory and red whenever debt > 0", its docstring).
   - `validate_schema --cross-check`: rc 1 both; 20 "absent from" lines both (`... | grep -ci 'absent from'`).
   - `retired_vocabulary`: rc 1; it reads the tree, and the four flagged tokens have equal counts on both trees (`git grep -c -- applicable_groups origin/main` vs `HEAD`, likewise `UNVERIFIED-1`, `VERIFIED-WITH-CORRECTION`, `evidence_cell_state`).
   - `research_dod --all`: rc 1 both; R12 ✗ both.
   - `research_protocol_audit`: rc 1 both; "TOTAL ISSUES: 23" both.
   - `metadata_integrity_audit`: rc 1 both; "[1] FAIL: 20 COMPLETE/COMPLETE-STATUTORY rows with open integrity flag" both.
2. **Root cause, G01/G02.** The fixture picks "the latest admitting session" (`scripts/tests/test_scan_contract.py:868–869`, `ORDER BY MAX(created_at) DESC LIMIT 1`) and assumes it predates `R16_SCAN_FROM = "2026-10-10"` (`research_batch_dod.py:194`). Since `session_2026-10-30-ramp-spec-pages-rebuild` admitted sources, it does not, so g1 has no grandfathered admission and G02 fails behind it. A fixture derived from live data that went stale (rule 7a's shape).
3. **Options.** (a) Fix the fixture: select the latest session whose admissions all predate `R16_SCAN_FROM` (one SQL change, ±2 lines). (b) For `scan_debt`: lower to `informational`, since a check red by construction teaches the reader to ignore it (CLAUDE.md rule 6's argument); or keep, as its docstring argues. (c) For the other five: one diagnosis each; each is debt with its own owner (R12 economics rows; research_protocol CHECK 1/2/8; metadata integrity flags; schema cross-check archive drift; retired vocabulary in prose).
4. **Recommendation.** (a) in PR-A. Put `scan_debt`'s level to the owner only if it matters; it is a registry edit (governance). Record the other five as already-known debt on `main` (this computation) rather than new gaps; any that no reader acts on is a deletion candidate under §8 with this evidence.
5. **Cost.** (a) ±2. Acceptance: G01/G02 pass on `BRANCH` after; red before (shown above).
6. **Dependencies.** None.

### GAP-096 — pass 7 open (AUDT, P3)

1. **PARTLY.** Pass 7 open, finding 140 SURVIVED with artefact `scripts/migrations/data_20261030214538_2026-10-30-ramp-spec-pages-rebuild.sql`, deleted in history (`git log --all --diff-filter=D --name-only --oneline | grep 20261030214`). Understated: passes 1, 2, 5 are also open (U8). "Owner decides whether to dispose finding 140 OWNER-RULED": that cannot unblock the close, which checks that every SURVIVED row's artefact resolves to an existing file and ignores dispositions (`scripts/db.py:4596–4606`).
2. **Root cause.** The migration rebuild deleted a committed file a finding cites; findings are immutable (the 2026-09-27 ruling forbids `amend-adversarial-finding`).
3. **Options.** (a) Tooling: let `close-adversarial-pass` accept an artefact that exists in git history (`path` present in `git log --all`), reported as `historical`. About +8/−0. Not an amend of the finding. (b) Owner: pass 7 stays open with a ledger note, as passes 1 and 2. (c) Restore the file: forbidden in practice, since the runner would apply a restored migration.
4. **Recommendation.** Owner choice between (a) and (b); the 2026-09-27 (second) ruling ("Do not ... chase pass 1 closed as its own effort; it stays open") favours (b) by analogy. Separately record pass 5's 11 undisposed SUSTAINED findings as their own gap (U8): that is a real loose end, unlike 7.
5. **Cost.** (a) +8 plus a `test_db_amend_writers.py` case (a deleted-path artefact refused today, accepted after).
6. **Dependencies.** None.

---

## A. PR sequence

Rule 10: tooling merges first; data PRs carry no tool change. `close-gap` writes rows, so gap closures ride in data PRs.

**Revised for the owner's 2026-11-06 steer (§E governs where it differs from this list):** PR-A carries only the ledger predicate (085/089), the fixture fix (095), the `claim_text` walk added to the existing audit (086), the two-field widening (087), the `--contested` deletion, and one line of scan procedure prose (092). The `update_locator`/GAP-036 change and the figure-inventory script are dropped (093 CLOSE-AS-ACCEPTED; 092 RULE-OR-PROSE).

1. **PR-A, tooling-only (no ruling needed), original draft.** `v_scan_ledger` requires `method='full-read'` for READ-NOTHING-FOUND (085/089/092, U3); `test_scan_contract` fixture fix and a pre-screen ledger case (095); `observation_verbatim_audit` walks `claim_text` (086); writer-retire `add-extraction --contested` (087c, U13); `update_locator` + `updated_*` + `_resolve` over all session columns (093 with GAP-036); delete `awm.txt` (U12). Add the figure inventory (`full_text.py --figures`, 092b). Estimated scripts delta: about +80/−12; the description names the exception and the one genuine deletion (the unread `--contested` flag) per CLAUDE.md §8, which is a reporting requirement, not a bar. Section 8 test for each addition: the ledger change reads `source_scans.method` (without it, unread pairs show as read and the book can say "no code sets a value" on a keyword skim); the `claim_text` walk reads persisted artefacts (without it, a quote altered after write governs a determination unseen); the inventory reads derived texts (without it, stated figures are recorded absent). Unblocks honest debt figures and every read-first research PR.
2. **PR-B, tooling-only, workplan T-1b steps 8 and 9 (ruled OR-3, OR-10).** Widen `amend-extraction` (value, unit, NULL setting; plus `loc_*`, `source_section`, non-NULL setting if Q8 is yes) (087); length family and `RULE_VERSION` bump (094/072). Separate PRs per WR-2 if both bump. Unblocks D-1 and composition.
3. **PR-C, doctrine.** Ledger entries for the owner's answers to Q1–Q7 below, with SUPERSEDES lines; `tier-system.md:15` correction; owner-browser prompts added first (U5). Attestation required for `decisions/` marks (rule 2).
4. **PR-D, research-data (after A).** `set-parameter-direction` for 4, 5, 6, 9, 11 from quoted source statements (U1); `amend-search` 199/200 to adversarial-pass/8 (091); log the two Europe PMC lookups (088); `amend-source` REF-00468, REF-01005, REF-01008 if Q3 = (a) (075); notes recording the full Korean quotes (090); gap closures with reasons: 088, 089, 090, 091, 093, 094, and candidate parts of 087; correct GAP-056's appended note; new gap for pass 5 (U8).
5. **PR-E, research-data (after A, and after Q1/Q2/Q4 for lens and turn rows).** D-3 full-read catalogue scans with open pass, held sources first: the five pre-screened sources, REF-01018, REF-01015, REF-01014, then the rest (078, 082, 084, 085); Portuguese full retrieval and `supersede-source` REF-01026 (083); REF-00468 mining (081); DPO-repository Co-1 retrieval (079 with GAP-049); acoustic stash leads with `--verify-authors` (078). Then D-2 lens fill (076) once OR-1c is answered. Candidates 150–155 (080) only after GAP-030's `correct-locator` (its own tooling PR) and a library route.

## B. Owner-decision sheet

Ordered by work unblocked. Each is phrased for a one-sentence answer.

1. **OR-1c (already on your page, unanswered):** "When one figure concerns several ICF codes or access needs (wheelchair users map to d410, d420, d450, d465 and more), should it be written once per combination, or once with a link table naming all of them?" Unblocks the lens fill on all 214 extraction rows (`select count(*) from source_value_extractions`), T-3, D-2, GAP-076. Row-per-combination duplicates the figure (rule 5 needs your exception); a link table is more schema but keeps one home.
2. **Identity lens for a clause under a disability heading:** "A code clause that names no one but sits under a heading for disabled people: tag it MOB, or ALL?" MOB: under OR-1b it reaches MOB determinations. ALL: per `population-taxonomy.md` §1.3 code values are ALL, and under OR-1b they then reach no MOB determination, so MOB determinations rest on studies alone. OR-1/OR-1b favour MOB; population-taxonomy §1.3 favours ALL.
3. **Tier of controlled research published as a government report (REF-00468, REF-01005, REF-01008):** "Should these be typed `clinical` (keeping the grey flag), staying `grey` tier 3, or should `grey` gain a T1 route?" `clinical`: band ● (T1 or T3-clinical by control level), no tooling, supported by `evidence-methodology.md:43`. `grey`: band ○, `tier-system.md:15` is corrected. New route: tooling and a ladder change.
4. **Turning quantities (GAP-074 with GAP-068):** "Is the width a passage needs at a turn (a) a new term, (b) corridor width conditioned on a turn, or (c) part of a redefined turning space, and is turning space measured as a diameter or as a square side?" Unblocks parameter 5's determination and the unfiled square-space figures.
5. **Sub-national instruments:** "Should England-only, Flemish, Ontario and Madrid instruments carry a sub-national jurisdiction code, or keep the national code with a scope note?" Sub-national: vocabulary and bucket (OR-8) changes plus re-filing. Scope note: no tooling.
6. **Pass 7:** "May an adversarial pass close on an artefact that exists only in git history, or does pass 7 stay open like passes 1 and 2?"
7. **Acquisition:** "Will you provide a library route for the Koontz, Steinfeld, King, Higuchi, Paquet and Savelsbergh papers and for BS 8300?" Without it, those stay staged and the UK turning question rests on AD M diagrams.
8. **Correcting transcription fields in place:** "May `amend-extraction` correct a figure's locator, section and a wrong (non-empty) setting in place, with the old value kept in notes, as OR-3 allows for value, unit and empty setting?" Asked only because D-0168 is DG-NON; the quoted D-0168 sentence names the value, not locators.

## C. Close with no work (or with a note only)

- **GAP-090:** wrong; `quote_in_artefacts` returns True for both full sentences (computation in §2). Also amend GAP-056's appended note.
- **GAP-094:** duplicate of GAP-072 and of ruled T-1b step 9 (OR-10); force half wrong (`select claimed_unit, count(*) from source_value_extractions where parameter_id=6 group by 1`).
- **GAP-088:** by design (DR-2026-09-26 §2.2(b), ratified 2026-09-27) plus duplicate of GAP-034 for WebSearch; the data step is to log the lookups as executions.
- **GAP-091:** the sanctioned two-step path exists (`scripts/db.py:3939`, `:4000`); targets on adversarial-pass are excluded by OQ-7 ("R1 no").
- **GAP-089:** folds into GAP-085 (documented design; the defect is the ledger).
- **GAP-087, candidate `harm_finding` and title parts:** decided by GAP-059 (CLOSED-DECIDED, `sessions/session_2026-10-01-research-batch-23.md:133`); `contested` has no reader (U13).
- **GAP-093:** nothing was lost (`MAIN` values NULL); close if (b) is not taken, else close with GAP-036.

## E. Tooling recommendations under the owner's steer (2026-11-06: "MINIMIZE code wherever possible ... the bare essentials in the most code efficient manner")

Order applied to each: does it reach the book; do nothing; rule or prose; reuse; delete; smallest new code. Lines are physical lines in `scripts/ schemas/ .github/ skills/`, migrations excluded.

| Gap | Reaches the book? | Mark | Smallest design that closes it, and why nothing smaller does |
|---|---|---|---|
| 085 (+089, symptom) | Yes: unread pairs count as read, so a page can say "no code sets a value" on a keyword skim | NEW-CODE, 1 predicate | Add `AND s.method = 'full-read'` to the READ-NOTHING-FOUND branch of `v_scan_ledger` (a schema migration recreating the view; 1 changed line of logic). Prose alone cannot fix a derived figure that is wrong. Test optional: the acceptance query in §2 is enough for the PR. |
| 086 | Weakly: only a row written past `db.py` (hand migration) could carry a false quote | REUSE, about +20 | Walk `source_value_extractions.claim_text` in `observation_verbatim_audit.py` with the same `locate_quote` and ratchet. Drop the gap's other four rules (one exists, three are unverifiable or need curated maps). Acceptable alternative: CLOSE-AS-ACCEPTED, since rule 3's capture path never hand-writes rows. |
| 087 | Locator: yes (the book cites the wrong clause). Setting/value/unit: yes (OR-3, ruled). Lens: yes, but owner-gated. Candidate fields, `contested`: no (no reader) | NEW-CODE +2 (locators), planned T-1b step 8 (setting/value/unit), DELETE −1 (`--contested`), CLOSE-AS-ACCEPTED (candidate harm/title/tier_guess, per GAP-059) | Add `loc_*` names and `source_section` to `_AMENDABLE_SVE_FIELDS` (`scripts/db.py:8647`); the existing verb, refusals and ledger do the rest. Lens: no code before OR-1c. |
| 088 | No | CLOSE-AS-ACCEPTED + REUSE | Log the Europe PMC lookups as their own executions with `log-search`; WebSearch half stays under GAP-034. |
| 089 | Only through 085 | Symptom of 085 | Closed by the 085 predicate. |
| 090 | No (claim was wrong) | CLOSE-AS-ACCEPTED | Wrong; no work. |
| 091 | No | CLOSE-AS-ACCEPTED + REUSE | `amend-search --set-origin adversarial-pass` then `--set-origin-pass-id`; OQ-7 excludes targets. |
| 092 | Yes: stated figures recorded as absent | RULE-OR-PROSE, 0 code | One sweep command line in the scan procedure and a rule that an absence note quotes its sweep. NEW-CODE (+35, `full_text.py --figures`) only if the one-liner fails on non-Latin numerals. |
| 093 | No (values replaced were NULL) | CLOSE-AS-ACCEPTED | Nothing lost; GAP-036 stays its own item. |
| 094 | Yes (no composition across m/cm/mm) | Duplicate of GAP-072; planned T-1b step 9 | No new design; build the ruled step (OR-10). Force family: none needed. |
| 095 | G01/G02: no, but a test red on `main` teaches readers to ignore tests | NEW-CODE ±2 (edit) | Fixture selects the latest session whose admissions predate `R16_SCAN_FROM`. The six advisory reds: CLOSE-AS-ACCEPTED as known debt, measured red on `main`. |
| 096 | No (closure state of a pass) | CLOSE-AS-ACCEPTED | Leave pass 7 open with a note, as passes 1 and 2. Pass 5's 11 undisposed SUSTAINED findings may reach the book and need a gap (data, not code). |

**Total new code for the whole set, excluding the already-planned T-1b steps 8 and 9:** about +23 / −1 (085: 1, 086: 20, 087: 2, 095: 0 net; minus 1 for `--contested`), and one view migration. With 086 closed as accepted instead: about +3 / −1. One mechanism (the ledger predicate) closes 085 and 089 and makes 078, 082, 083 and 084's research measurable; 092 then rides on prose.

## D. Risks

- **Ledger fix raises the debt figure sharply.** `scan_debt` will report more pairs; a reader may take it as regression. State the before/after in the PR (the 22 pairs).
- **Reclassifying `grey` reports to `clinical`** moves bands from ○ to ● on every row of three sources. If the owner later reads `grey` as a publication route, the reversal is three more amendments; get Q3 answered first and apply it to the class, not to REF-00468 alone.
- **A lens re-key writer built before OR-1c** may be the wrong shape and be built twice; and any re-key changes which determination a figure reaches (OR-1b). Do nothing on lenses before Q1/Q2.
- **Widening `amend-extraction`** to locator and setting makes in-place change cheap; without the old value ledgered it becomes the overwrite D-0168 exists to stop. Keep the old-value trailer and the engine-column refusal.
- **Setting directions for parameters 4–11** lets the engine compose for the first time; with the units still split (until T-1b step 9) and lenses incomplete, the first determinations will rest on a subset. Do not write specifications from them until PR-B and Q1 land.
- **Re-admitting batch-01 acoustic leads** repeats the 2026-08-19 fabricated-co-author failure if bibliographic fields come from the stash; write them only from payloads with `--verify-authors`.
- **A figure inventory (092b)** can become the new list readers trust instead of reading; a scan note should say the inventory was compared, not that the text was read. It does not see figures in images (diagrams, tables rendered as pictures), so `page_image.py` remains the route there.
- **Lowering `scan_debt` to informational** hides real debt from preflight; prefer leaving it and naming it as red by design in the registry note.
- **Closing pass 7 on a history artefact** weakens "attacked with a committed file" to "attacked with a file once committed"; report it as `historical`, never silently.
