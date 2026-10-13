# Proposed rulings on the open questions

**Status:** PROPOSED rulings, delivered 2026-10-12 on the owner's instruction ("Fable 5.1 r read-only to resolve as many open questions as possible, ie deliver rulings, based upon logic and premises"). **Not entered in the ledger.** The ledger (`references/project-standards.md`) is where a ruling becomes effective; nothing here edits it, the plan, a contract or a doctrine text. The plan's §4 recommended column predates this file; where they differ, this file is later (list in "Differences from the plan" below).

**Authority.** Two bases: the owner's commission above, and the standing delegation LED-154 (owner-quoted 2026-09-11, `references/project-standards.md:2858`): "Fable 5.1 adjudicates and resolves all items presented to the owner, Opus executes in the agonist-antagonist method, and the medical lens is to be filled out." A ruling that LED-169 action (4) reserves to the owner (row-bearing deletions, R3) or that CLAUDE.md §8 reserves (mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction, licensing, trajectory) is marked *owner merge* and takes effect only when the owner enters it.

## Reviewer's notes (mine, after reading the report below)

- **Premises I re-checked and found as cited:** OD-7 is OPEN (`OPI-105`; the instrument records "OD-2 through OD-12 are still open" at `decisions/DR-2026-08-19-research-restart-operative-instrument.md:90–92`); LED-015, 016, 017 give three markers and MIS-03 gives two; `schemas/enums.py` `EvidenceMarker` holds two; LED-154, LED-024, LED-202 (OPEN), WRK-178 and EVI-003 read as quoted. The rest of the premises I did not re-run.
- **Correction to my own earlier text:** the plan and `COMPARISON.md` said the instrument's OD-6, OD-7, OD-8 and OD-9 were "approved". They are the instrument's *recommended* answers and are OPEN. Corrected in both files. This removes the ratified support the plan cited for the Pydantic mirror requirement, the gate merge and the workplan move.
- **A premise that does not carry R3 as written:** R3 cites LED-166 as ordering the axis codes out of existence. LED-166 forbids an `AX-` code *denoting an ICF code*, and `P-G` finds none, so it does not reach the axes table's own codes. R3 stands on WRK-178 to WRK-181 (the owner's R3 of 2026-08-18: axes retired, the map re-derived), DRS-024 (one act) and the reconstructibility of the rows, and still needs the owner's entry under LED-169 (4).
- **R5's confidence is medium, not high.** The mirror requirement is stated in CLAUDE.md §4 and §7; retiring it rests on the tie-break "less code and one home per fact" applied after "the specific over the general".
- **Four questions the premises do not decide** (R12's language conjunct, R23, R26, R27) are left undetermined, as the report says.
- **The report reads several records by interpretation** (R9, R33, R34, R38, R40 are medium for that reason). A ruling is only as good as that reading.

## Differences from the plan's recommended answers (not applied to the plan)

| ruling | plan | this file |
|---|---|---|
| R5 Pydantic mirrors | keep for now | retire the requirement; delete unread mirrors and `validate_pydantic_schemas`; keep six imported modules |
| R7 markers | open (C-002); gates the ladder and the marker | three; source of the band is tier-system §5 and Option A §3 |
| R9 T3-grey alone | open | band only; engine's `pending` stands |
| R14 population names | deferred to the owner | `base_taxonomy_identity`, `identity_icf_map`, `evidence_identity_match`, `identity_code`; one act in Phase 3 base; owner nod recorded |
| R22 BPC layer | ask | not a live deliverable; retire validators, criterion, `bpc_metadata`, `update-bpc`; archive `bpc-reasoning/` |
| R24 root pointer | design owed | nullable FK by rebuild under `AFTER_DATA`; registry writer filed as a GAP |
| R25 `term_catalogue_origins` | owner's accept-or-strike | three nullable columns on `terms`; the owner's accept-or-strike still applies |
| R29 deep divergence | owner call | compensating migration, never a wider exemption |
| R30 decisions register | ask | retire both stores; table frozen as infrastructure residual |
| R1, R2, R3, R4, R16, R17, R18, R19, R20, R21, R28 | as recommended | as recommended (R3 and R30 flagged for the owner's entry) |

---

## (A) Summary

Forty-two distinct questions were put once the three lists (plan §4 sheet incl. the ten-item doctrine sheet; COMPARISON §7's fourteen and its six DEFERRED rows; the twenty-nine OWNER/OWNER+AGENT conflicts) were de-duplicated. Thirty-eight are ruled from premises; four are UNDETERMINED (R23 bytes-pointer design, R26 case-study/economics fold, R27 LED-202 preliminary figures, and the ≥9-language sub-fork inside R12), each with the single owner premise that would close it. The most consequential ruling is R7: three markers govern (LED-015/016/017 as reconciled 2026-07-13, tier-system §5/§8, Option A §3), which gives `tier_ladder`'s band and the determination's `marker` their source and so unblocks the specification and render stages (P6, P18, 3.R) without re-ruling the build sequencing the antagonist passes fixed. A finding incidental to the rulings: the plan's premise that "OD-7 approved schemas mirror SQLite" is false — OD-7 is OPEN (instrument :92; OPI-105), which removes the only ratified support for the Pydantic mirror requirement (R5).

Read-only pass, 2026-10-12. Every figure below is the output of a read-only query run that pass; re-run before quoting (CLAUDE.md rule 7a). Owner statements of 2026-10-12 are cited to `transcripts/harness_db856d85/main.jsonl` lines 4931, 4950, 4965, 4976, 4991; the commissioning sentence itself has no repository record yet [UNVERIFIED as to file:line].

## (B) Table

| id | question | RULING | conf. | authority | steps |
|---|---|---|---|---|---|
| R1 | Render apparatus; "static now" claim (C-027) | Delete all of 1.1; one view + one renderer reading the DB at render time; no committed HTML as a pipeline object; `render-freshness` deleted; "static now" is UNVERIFIED and does not bind | high | agent (code); e-08 brief to `_archived/` agent (§8) | 1.1, 3.R, 0.5 |
| R2 | Scheduled workflows (C-029) | Delete both workflows, scripts, tests, tables | high | agent | 1.5 |
| R3 | Drop row-bearing retired tables + `slugs.serves_axes` value (Q1, C-017) | Yes, all five; record in the ledger per LED-169(4); column drop only under an AFTER_DATA marker with `--rebuild` proof, else writer-retire | high (axes), medium (`pipeline_runs`) | **owner entry required** (LED-169 (4)) | 1.4, 1.5 |
| R4 | Quarantined gates (C-028) | Delete three; promote `adjudication_integrity` to blocking with the two script edits | high | agent | 1.6, 3.R |
| R5 | Pydantic mirrors (Q8, P19) | Retire the requirement; delete unread mirrors and `validate_pydantic_schemas`; keep the six imported modules | **medium** (reviewer) | agent (code); CLAUDE.md lines owner merge | 1.2, 1.6, 4.2 |
| R6 | (a) mission "teaches professional judgment" (C-001) | LED-024 governs; MIS-02 and test item 6 stale; MIS-08 status line stale | high | owner merge | 2.2 |
| R7 | (b) markers two or three (C-002, Q11) | Three; band map = tier-system §5 (source) and Option A §3 (determination) | high | owner merge (mission line); agent (enum, ladder) | 2.2, 3 spec, 3.R |
| R8 | (c) "seven tiers", tier-number-vs-quality (C-006) | tier-system §1 governs; "seven tiers" and "higher = weaker" stale | high | owner merge | 2.2 |
| R9 | (d) T3-grey alone: state or band (C-004, C-003, Q6) | Band only; engine's `pending` stands; wording repair of "anchors"/MIS-04 | medium-high | owner merge (wording) | 3 spec |
| R10 | (e) LED-018 amended by Option A (C-005) | Yes: AMENDED; methodology 3.4 bare form needs the flag | high | agent (status); owner merge (text) | 2.2 |
| R11 | (f) Co-1 warrant (C-024, C-025) | D-0178 governs; co1-operational §6 stale; enum fixed from the CHECK | high | owner merge (doc); agent (enum) | 2.2, 3 evidence |
| R12 | (g) jurisdiction §2.3 (C-049) | "All 24 jurisdictions" conjunct superseded (R6 + LED-193); replacement text owner's; ≥9-language conjunct UNDETERMINED | high / sub-fork open | owner merge | 2.2 |
| R13 | (h) append session-only rulings (C-036) | Yes, verbatim with file:line; nothing for atoms without the owner's words | high | agent (recording) | 2.2 |
| R14 | (i) "population" replacement; registry names (C-018, Q4, P15) | `base_taxonomy_identity`; `population_icf_links` → `identity_icf_map`; one act in Phase 3 base | medium | agent-derived; owner one-word confirmation recorded in the ledger | 3 base |
| R15 | (j) review D-0184 (C-023) | In force (implements LED-128/130); review discharged by owner nod; BY pointer on D-0170 | high | owner merge (the nod) | 2.1 |
| R16 | Medical lens (C-022) | Yes; clause 3 is unconditional; fill by correspondence from persisted WHO payloads via `add-medical` | high | agent (owner-ordered) | 5 |
| R17 | Cross-parameter synthesis (C-035, P1) | Build nothing; merge deferred; trigger = second parameter with an extraction | high | agent | 3 synthesis |
| R18 | Slug-by-lens (C-033, P2) | Affirmed: four nullable lens FKs + coverage view; LED-029 SUPERSEDED | high | agent | 3 research |
| R19 | Base-vocabulary writers (C-034) | Yes, migration-only for owner-gated vocabularies; `slugs` is the one GAP | high | agent | C-034 |
| R20 | `not_applicable` (C-007) | Keep value and rationale column, unbuilt and flagged; exclusion governs the "any →" row | medium-high | owner merge (methodology lines) | C-007 |
| R21 | Dead criterion (a) locator-title | Retire criterion and `source_locators_integrity` | high | agent (contract is PROPOSED) | 1.6 |
| R22 | Dead criteria (b) BPC layer | Not a live deliverable; retire the three validators, the criterion, `bpc_metadata`, `update-bpc`; archive `bpc-reasoning/` | medium | agent; CLAUDE.md rule 2 path list owner merge | 1.6, 1.9 |
| R23 | Bytes-pointer design (Q13, P11) | UNDETERMINED (design): constraints and favoured shape given | — | rehearsal, not a premise | 5 |
| R24 | Root pointer (Q14) | Nullable FK by table rebuild under AFTER_DATA; writer for the registry filed as GAP | medium-high | agent | 3 judgment |
| R25 | T1 extras `term_catalogue_origins` (Q2) | Keep the fact as three nullable columns on `terms`; approval as a pointer, not a quote copy | medium | owner accept-or-strike (SES-063) | 0.2 |
| R26 | `case_studies`/`economics_entries` fold (Q3, P5) | UNDETERMINED: RES-12 governs today; fold needs an R12 amendment | — | owner merge | 1.3 |
| R27 | LED-202 preliminary full-read figure (Q5, P16) | UNDETERMINED | — | owner | — |
| R28 | Re-baseline migrations (Q7) | No | high | agent | §2 |
| R29 | `migration_reproducibility_deep` divergence (Q9) | Compensating migration, never a wider exemption | medium | agent | 1.5 |
| R30 | Decisions register (Q12, OQ-5) | Retire both stores; table frozen as infrastructure residual; ledger the single home | high | agent; decision-protocol §5 owner merge | 1.2, 2.2 |
| R31 | national_fw tier mapping (C-009) | TIER_MAP governs; methodology 1.5 sentence stale | high | owner merge (sentence) | 3 evidence |
| R32 | `source_value_extractions` stage (C-012) | Judgment | high | agent (map); CLAUDE.md §3 row owner merge | 3 judgment |
| R33 | Crossing at judgment vs synthesis (C-014) | LED-113 governs; D-0174's clause read as "never presupposed, never defaulted" | medium | agent | 2.2 |
| R34 | Cursory scan vs relevance vs scan contract (C-015) | Reconciled by object: admission (collection), listing (evidence), derivation (judgment); `source_scans` = evidence | medium-high | agent | 0.2 |
| R35 | Axes (C-017) | Ruled retired; executed as one act with the sweep | high | agent | 1.4 |
| R36 | Item layer (C-019) | Ruled; drop empty cluster; archive condition already met | high | agent; taxonomy docs owner merge | 1.2 |
| R37 | Scan contract vs writer guard (C-032) | Delete the slug-admission refusal after T1; `source_slug_links` stays; `sve.slug` NULL-forward | high | agent | 3 judgment |
| R38 | Process contradictions (C-037) | Six pairs ruled by later/specific (below) | medium | agent | 2.2 |
| R39 | C-039 residue: LED-159 band; LED-168 lens set; LED-208 cap | Confirming study's band; four lenses stand; no cap carries | medium | owner merge (band); owner confirm (cap) | 2.2 |
| R40 | Instrument scope and read-set (C-041) | CLAUDE.md's chain and §9 table govern; instrument's read-set and OPERATIVE labels stale | medium | agent | 2.2 |
| R41 | Column-retirement order (C-044) | No conflict: specific (NOT NULL DEFAULT) over general; spent | high | agent | — |
| R42 | Forward FKs (C-046) | All fourteen classified; none needs the owner | medium-high | agent | 3 synthesis |

## (C) Rulings

**R1 Render apparatus.**
PREMISES: LED-103, LED-104 (owner-quoted 2026-08-27, `references/project-standards.md:1654`): "the entire pipeline is dynamic rendering on site", "do not rely on artifacts for rendering the site". ADD-002/003 (OWNER_RELAYED; sole home `_archived/scripts/migrations/046_drop_render_manifest.sql:16-17`); `git grep -n -i -E 'static (build|now|site|render)' -- sessions references/project-standards.md decisions workplan` finds no other home. P-I FAIL, P-K FAIL (STATE-GRAPH.md:412-413: every renderer's query fails on the live schema). CLAUDE.md §8 (delete on evidence; `_archived/` is for retired reader content); §3 "a cross-stage view IS the pointer". Owner 2026-10-12: minimize code; rely on pointers. DR-2026-07-12 (website lock, static generator) predates LED-103.
INFERENCE: The stopgap rests on an agent's relay with no primary record, and the apparatus it describes no longer runs, so there is nothing functioning to keep. The owner-quoted target is reading the database at render time with no artefact reliance; a freshness gate exists only to police committed artefacts, which that target forbids.
RULING: Delete everything 1.1 names; `specs/e-08-brief.html` to `_archived/`; delete `render-freshness` (PIP-07) and CLM-050 rather than repair them. 3.R builds one view and one renderer that reads it; generated HTML may be produced at deploy time but is not committed as a pipeline object. The "static now" claim is not confirmed and does not bind.
OVERTURN: an owner statement that per-page HTML is to be committed and gated.

**R2 Scheduled workflows.**
PREMISES: CLM-012/013; PIP-18 (job-owned tables the only exemption); CLAUDE.md:90-96 (bot commit c4c8463 UPDATEd `evidence_sources` and rewrote `evidence_source_authors` with no migration and no payload); `scripts/resolve_dois.py:557-597` (DELETE+INSERT authors, writes `author_count_is_complete`); CLAUDE.md 5(c). Live `pipeline_runs` (5 rows): `total_resolved` 0 in all; `doi_before=doi_after`, `verified_before=verified_after`, `metadata_complete_before=after` in every run (10/10, 8/8, 20/20, 22/22, 26/26); `phase_4_enriched` 0,0,1,1,2. `url_verification_runs` 0 rows; no NULL `verification_status`.
INFERENCE: Five runs resolved nothing and verified nothing; the only non-zero effect is the payload-less author rewrite, which 5(c) forbids. The workflows' net product is rule-3 violations and binary conflicts.
RULING: Delete `resolve-dois.yml`, `verify-urls.yml`, their scripts and tests, `pipeline_runs`, `url_verification_runs`; shrink `EXEMPT_TABLES` and the `reproducibility-invariant` text. Author enrichment re-enters only through `add-source --verify-authors` with persisted payloads (Phase 5).
OVERTURN: a reader of a phase-4 write that reaches the book (none found: readers are `test_db_integrity` E02/E03 and the exempt list).

**R3 Row-bearing retired tables and the `serves_axes` value.**
PREMISES: LED-169 (owner-quoted 2026-09-16, `:3534-3580`): CONDITION covers "any migration that would empty a table"; ACTION (4) reserves genuine departures to the owner case by case, "recorded here"; the ruling's own boundary: "§8's 'dead tables: delete them' stands unchanged… governs DATA ROWS AND IDENTIFIERS, where deleting destroys provenance the project cannot reconstruct". Rule 3 (migrations immutable; `--rebuild`): `axes`, the two maps and `["AX-BAL"]` replay from `057_baseline` and `data_20260902220357`. LED-166 (owner 2026-09-13, MUST_NOT): "AX- must never denote an ICF code anywhere" *(reviewer: does not reach the axes table's own codes; see notes)*. WRK-178–181 (owner R3 2026-08-18): axes retired; `population_axis_map` re-derived mechanically — `population_icf_links` (61 rows) is that derivation. DRS-024: one act. Owner 2026-10-12 commission touches ACTION (4) for these items (rule 0). `pipeline_runs`: bot-written, in no migration (EXEMPT), no inbound reference.
INFERENCE: The axis rows are reconstructible, so they are not the provenance LED-169 protects; a status column added to retire 91 rows of a retired vocabulary is apparatus with no reader (§8). The `pipeline_runs` rows are logs of a workflow R2 deletes; quoting them in the deletion commit preserves that they existed.
RULING: Yes to all five. The ledger entry LED-169(4) requires is written with the ruling. `serves_axes`: the value may be destroyed; the column is dropped only by a schema migration carrying `-- AFTER_DATA:` later than `data_20260902220357` with a green `--rebuild` (R6), otherwise writer-retire and NULL-forward (rule 5, LED-079).
OVERTURN: an owner statement that the axis rows are to be kept as history.

**R4 Quarantined gates.**
PREMISES: `governance/check-registry.yaml:2415-2520`: `register_integrity_check` red by construction (frozen pilot); `adjudication_integrity` green, "nothing mechanical blocks promotion… waits on OD-E", and OD-E was ruled 2026-08-31 (D-0179); `code_currency_audit` red content backlog; `pre_rehab_banner_audit` red, a BPC-file drift gate. P-QUARANTINE, P-TIER-DERIVE FAIL. CLAUDE.md §8 (a check must name what reaches the book), rule 6 (red by construction teaches ignoring), 5(a) (EXAMINED). tier-system §4 names `code_currency_audit` as the currency rule's enforcement; `code_currency_*` columns exist on `evidence_sources`.
INFERENCE: A quarantined check gates nothing; only `adjudication_integrity` guards something every `stated` cell depends on and is green. The currency FACT survives in its columns and is surfaced by the 3.R view; a gate over a content backlog is not a gate.
RULING: Delete `register_integrity_check`, `code_currency_audit`, `pre_rehab_banner_audit` (and the retired `validate_db` entry). Promote `adjudication_integrity` as blocking after it prints `EXAMINED:` and fails on a NULL tier. tier-system §4's enforcement sentence is stale (owner merge, one sentence).
OVERTURN: evidence that a currency-stale T4–T6 citation reached a rendered figure with no other guard.

**R5 Pydantic mirrors.**
PREMISES: CLAUDE.md:307 ("mirror the Pydantic model"), :460 (drift is a bug). OD-7 is OPEN: instrument :92 ("OD-2 through OD-12 are still open"), OPI-105 OPEN; no ratification found (`grep -n OD-7 references/project-standards.md decisions/*.md`). DR-2026-09-26 §1.3 added one mirror under the standing rule and itself calls `MODEL_TABLE_MAP` a rule-8 violation. Rules 5, 8; §8 ("nothing is added without naming what reads it"). Owner 2026-10-12 (less code; deduplicate). Sweep `git grep -n -E '^\s*(from|import) schemas' -- scripts tools .claude skills governance ':!scripts/tests'`: runtime readers import `enums`, `tier_derivation`, `directness`, `pipeline_contract`, `decision` (R30), `evidence_source` and `evidence_state` (`validate_evidence_state`, blocking); every other table mirror is read only by `validate_pydantic_schemas` (red, 213 findings, import error) and tests.
INFERENCE: The mirrors are a hand-kept second home of the schema whose only reader is a red check keyed on a curated map; a generated mirror is still a second home with no reader. The plan's "OD-7 approved" premise fails, so no ratified text holds the requirement other than CLAUDE.md's own lines.
RULING: Retire the requirement. Delete the unread mirrors, `validate_pydantic_schemas.py` and its map; keep the six imported modules (`evidence_source`/`evidence_state` for as long as `validate_evidence_state` reads them). Strike CLAUDE.md :307/:460 (owner merge). `enums.py`'s curated code lists remain rule-8 debt, not ruled here.
OVERTURN: a runtime reader of a table mirror the sweep missed (tests are deleted with their subject).

**R6 Mission: "teaches professional judgment"; MIS-08.**
PREMISES: MIS-02 (`governance/mission-and-epistemics.md:76`, locked 2026-04-26 05:29); LED-024 (`:53`, 2026-04-26 19:25: "does not teach professional judgment, does not confer competence… supersedes any language elsewhere that implies institutional authority"); POS-04; CLAUDE.md §9 ("thinking tool and advocacy project, not an authority"); §8 mission = owner sign-off.
INFERENCE: Later, explicit supersession clause, and the Purpose paragraph already reads "does not substitute… a thinking tool".
RULING: LED-024 governs; commitment 7's heading, its "teaches" sentence and test item 6 are the stale text; the Status section's "not yet operative" is stale against the header and CLAUDE.md §9's use. Owner merge.
OVERTURN: an owner statement restoring "teaches".

**R7 Markers.**
PREMISES: MIS-03 (`:136`, two markers, 2026-04-26). LED-015/016/017 (`:26`; reconciled to three 2026-07-13: "the prior two-marker rule graded T4–6-only as ● — the convergence-laundering failure mode"). tier-system §5 and §8 (OPERATIVE, amended 2026-07-20). DR-2026-07-21 Option A §3 (`:47-51`): band at determination level; ◐ for individual T4/T5 citations in an anchored cell. CLM-038. LED-159 (owner 2026-09-13). `scripts/generate/pilot_renderings.py` REGISTER_MAP renders [●][◐][○]; `schemas/enums.py:237-245` `EvidenceMarker` holds two (drift).
INFERENCE: Every later and more specific record says three; the only two-marker text is the oldest and is the recorded failure mode.
RULING: Three. Source level (tier-system §5): ● T1, Co-1, T2, Co-2, T3-clinical; ◐ T4, T5; ○ T3-grey, T6, thin/expert. Determination level (Option A §3): a T4–T6-only cell takes ○; otherwise the governing anchor's band; a code value confirmed by a study takes the study's band (R39). The mission line is owner merge; `EvidenceMarker` is fixed in code. P6/P18 are not re-ruled: this ruling supplies the band's source (tier-system §5/§8) that the fifth pass found missing; the plan's sequencing (ladder, then marker + CHECK + engine INSERT in one PR) stands.
OVERTURN: an owner statement choosing two.

**R8 Seven tiers.**
PREMISES: EVI-002/003 (`governance/tier-system.md:11`, OPERATIVE 2026-05-25, "canonical definition", amended 2026-07-20: T1–T6 plus two tracks; "Tier number reflects what kind of claim… not how good"). EVI-085 (evidence-architecture :38, ratified 2026-07-13), EVI-269/PRC-100/ENT-392 ("seven tiers"); EVI-284 (methodology 1.2, "higher numbers = weaker"). Schema: `tier` integer 1–6 + `evidence_type`; `TIER_MAP` (`schemas/tier_derivation.py:53-64`) keys on (type, scope). tier-system §10 places practice by method.
INFERENCE: The canonical definition is the specific text and its 07-20 amendment is later than the architecture's ratification; the machine encodes six integers plus a type; "seven" counts Co-1 as a rung the schema does not have; "higher = weaker" contradicts both EVI-003 and Co-1 at tier 1.
RULING: tier-system §1 governs. "Seven-tier"/"seven tiers" and "higher numbers = weaker" are stale restatements to delete (owner merge). EVI-010/275 (T2 "below international standards") is positional prose, left. EVI-076/069/070 is resolved by §10 (by method); no conflict.
OVERTURN: an owner redefinition of the ladder.

**R9 T3-grey state; "anchors" wording.**
PREMISES: EVI-049/052/055 (tier-system §8, owner directive 2026-07-20). DR-2026-07-21 Option A `:44` "State machine unchanged"; `:47-51` band at determination level (owner directive, later). EVI-325/326/338, LED-010, PIP-03 (methodology 2.2: T3-grey alone → pending; single T6 → pending). Engine: `scripts/assess/assess_cell.py:1436-1438` (T3-grey → pending), `:1432-1434` (regulatory below richness → pending), `:1510` (regulatory at richness → provisional); P-ENG-T3 PASS. IDEAL-GRAPH §12 Q1 recommends provisional at ○.
INFERENCE: The only later owner directive expressly leaves the state machine alone, so the 07-20 directive reaches the band and not the state; the engine matches the ratified methodology, and parity holds inside the weak band (one source → pending, converged sources → provisional).
RULING: Band only. The engine stands; the ideal's change is a doctrine change not adopted. C-003 is a wording repair: "anchors" in EVI-052 and MIS-04 names the band; MIS-04's "stated = ≥Tier 3" is stale against EVI-325 (owner merge).
OVERTURN: an owner statement that a lone T3-grey source yields `provisional`.

**R10 LED-018 amended.**
PREMISES: LED-018 (2026-07-13); LED-013/014, EVI-058/094 (Option A, owner directive 2026-07-21); EVI-241 (anchored cells: floor value never "best practice"); EVI-394 (methodology 3.4 bare "Code requires…") against EVI-194/229/230 (flag binds every rendering); `status_corrections` entry for LED-018.
RULING: Option A governs; LED-018 → AMENDED (agent, status correction). EVI-034/035 stand for cells with anchoring evidence. The bare form in 3.4 is permitted only with the flag and caveat; that sentence is stale (owner merge).
OVERTURN: none short of withdrawing Option A.

**R11 Co-1 warrant; Co-1 enum.**
PREMISES: DRS-146/147/148 (D-0178, owner relayed 2026-08-31); DRS-264/265/251 (co1-operational, 2026-04-29); CLM-037; P-CO1-PROV PASS (data conforms; no CHECK). Live `co1_source_type` values: dpo_position_statement, lived_experience_publication, participatory_research; `schemas/enums.py:310-318` lists five others; rule 8.
RULING: D-0178 governs; co1-operational §6.1/§6.3 and "every pre-launch Co-1 citation is published_corpus" are stale (owner merge). The enum is corrected from the column's CHECK if one exists, else from the live sample with the writer constrained to it (agent).
OVERTURN: an owner statement that publication venue is a warrant.

**R12 Jurisdiction §2.3.**
PREMISES: WRK-084 (owner 2026-08-18: Global South no longer needed to leave PROVISIONAL). LED-193/SES-047 (owner 2026-09-28: buckets 1–2 only until categorically exhausted; the entry itself leaves the Global South tension open). `governance/jurisdiction-philosophy.md:93`: "PROVISIONAL until all 24 jurisdictions are recorded AND the Co-1 pass covers ≥9 languages". WRK-199/200/201/204 are AGENT_PROPOSAL. OPI-100 (OD-2) OPEN. CLAUDE.md §8: jurisdiction = owner.
INFERENCE: Two owner statements touch the first conjunct and none touches the second; the author's "buckets 1–3" wording is not the owner's.
RULING: The "all 24 jurisdictions" conjunct is superseded on contact; LED-193 is the research floor; the decision record owed for R6/OD-2 carries the owner's words with the author's derivations marked (WRK-204); the replacement sentence is owner merge. UNDETERMINED sub-fork: whether "≥9 languages" survives (favoured: survives — no owner statement touched it, LED-031 still requires language coverage).
OVERTURN: the owner's answer on the language conjunct.

**R13 Session-only rulings.**
PREMISES: C-036 list; CLAUDE.md:66-69 rule 0 "Record the supersession"; ledger practice is agent-authored recording ("Recorded on contact per rule 0", e.g. `:3534`, the 2026-09-28 entry); P-LEDGER-GREP FAIL; §7 (`sessions/` hidden from ripgrep).
RULING: Append SES-022, 023, 024, 025, 027, 032, 045, 047 verbatim with `sessions/<file>:<line>`, dated, with no ACTION text beyond the quote and its condition. SES-015/018/020 (words not quoted; HISTORICAL) are not appended — an entry without the owner's words would be a fabrication. Recording is not ruling; agent.
OVERTURN: an owner instruction that only the owner appends.

**R14 The word "population"; registry and map names.**
PREMISES: ADD-001/LED-127 (owner-quoted 2026-08-28, `:2453`: "we don't use the word 'population'… 'base_taxonomy' instead of 'population', i think"). LED-121 (owner 2026-08-27: the four taxonomies keep parallel `base_taxonomy_*` names). Live `base_taxonomy_medical`. CLAUDE.md:391-392 already composes "`populations` IS the identity lens (`base_taxonomy_identity`)". Live crossing-map family `identity_medical_map`, `icf_medical_map`, `access_need_icf` (`sqlite_master`). `:2478-2481` "confirmation pending". P-C NOT-BUILT. Rule 8 (an identifier from the union of its homes). DRS-024 (one act).
INFERENCE: The family name and the lens name are both owner words; the only hedge was on `base_taxonomy` as the substitute word, which LED-121 had already fixed. The companion names of 2026-08-25 (`item_demand_links` etc.) attach to tables 1.2–1.4 drop.
RULING: `populations` → `base_taxonomy_identity`; `population_icf_links` → `identity_icf_map`; `evidence_population_match` → `evidence_identity_match`; remaining `population_code` columns → `identity_code`. One act in Phase 3 base after 1.2–1.4, with the rule-4 sweep. The ledger asked for a one-word confirmation of `identity`; record the owner's nod against this ruling.
OVERTURN: the owner naming a different head noun.

**R15 D-0184 review.**
PREMISES: DRS-200 (ADOPTED, REVIEW PENDING; AGENT_PROPOSAL). LED-128, LED-130 (owner-quoted) are what it implements; migration 065 built the CHECK; 8 live `specifications` rows carry the four columns. LED-133; the 2026-09-11 ledger ACTION ("Cite D-0184 for the lens mechanism, not D-0170", `:2894`). decision-protocol: D-SCHEMA → DG-REVIEW, review may be batched.
RULING: In force. The review is discharged by the owner's nod on this sheet; since the register is retired (R30), the nod is recorded in the ledger. D-0170 gains a BY back-pointer (agent). DRS-194 ("owner's alone") is superseded by LED-154 (R16).
OVERTURN: an owner rejection of lens-as-column.

**R16 Medical lens.**
PREMISES: D-0170 (owner 2026-08-27, quoted at `:2869`: "yes we include the medical model too"). LED-154/DRS-231 (owner-quoted 2026-09-11: "Ensure that medical gets filled out"). D-0188 clause 3 "enforces D-0170"; DRS-232/233 limit clause 1 (the delegation), not clause 3. DRS-194 is an agent proposal (rule 0). LED-156 (ICD-11, block grain), LED-157 (never from recollection; persisted WHO payload), LED-158 (correspondence from held registries, on demand). P-MEDICAL FAIL; `add-medical --icd11-payload` exists.
INFERENCE: The "all items presented to me" scope attaches to clause 1; clause 3 is an unconditional imperative, bounded only by LED-156–158.
RULING: Yes. Populate `base_taxonomy_medical` by correspondence from the held registries through `add-medical --icd11-payload`, each row from a persisted payload, `icd11_verified_at` NULL otherwise; ships in the research PR (Phase 5).
OVERTURN: an owner statement narrowing clause 3.

**R17 Cross-parameter synthesis; the eight-table merge.**
PREMISES: LED-097/098; MIS-06; PIP-08; P-X FAIL. Live: extractions on one parameter only (101 rows, parameter 3); `specification_extraction_links` 151 (governing 38, conditioning 19, excluded 94); `convergence_assessment` 5 rows = `convergence_id` of specifications 4–8. Rules 5, 8; LED-169; P1's row-level failures (64 key collisions, 46 role refusals).
RULING: Build nothing; the merge stays deferred; `P-X` and C3.5 stay failing by design. The N:1 judgment→synthesis cardinality is carried through the determination today, which satisfies the walk; whether inputs should hang on the convergence row is deferred with the merge. Revisit when a second parameter holds ≥1 extraction (a derived trigger).
OVERTURN: a second parameter's data and a passing row-level rehearsal.

**R18 Slug-by-lens.**
PREMISES: LED-084/RES-04 (owner/contract 2026-08-24); LED-029 (2026-03-18); P-M FAIL; P2 ADOPTED (checked twice).
RULING: Affirmed under the R14 names (`identity_code`→`base_taxonomy_identity`, `icf_code`→`base_icf`, `needs_code`→`access_needs`, `medical_code`→`base_taxonomy_medical`), nullable, with one coverage view; LED-029 → SUPERSEDED; keep `P-M`/C1.8; the bucket refusal waits on LED-193's exhaustion view.

**R19 Base-vocabulary writers.**
PREMISES: LED-182, CLM-031; P-O FAIL (15 tables: `access_duration, access_need_axis_map, access_need_icf, access_needs, access_stakes, axes, lang_jur_map, life_stage_modifiers, population_axis_map, populations, room_items, rooms, situations, slugs, term_aliases`). CLAUDE.md §8 (taxonomy = owner content). LED-204/205 (prepopulated names screened and owner-approved). Research-stage growth already has verbs (`observe-term`, `add-term`, `add-parameter`, `add-medical`, `add-icf-code`, `add-population-icf-link`).
INFERENCE: LED-182 governs what a batch must write; an owner-doctrine vocabulary is written by a migration under sign-off, and a verb for it is a writer with no sanctioned caller (§8). Of the fifteen, only `slugs` is something research must mint.
RULING: Yes. Delete `P-O` and C2.8. `slugs` is filed as a Layer-1 GAP (rule 10), not patched. The axis trio, `situations`, `room_items`, `rooms` follow R3/1.2/LED-169.
OVERTURN: an owner order to write a doctrine vocabulary from a batch.

**R20 `not_applicable`.**
PREMISES: EVI-361 vs EVI-364 (methodology 2.7); mission `:118` (not_applicable needs an explicit rationale; ratified); LED-151/152; P-ENG-STATE FAIL; `specifications.not_applicable_rationale` exists (PRAGMA); C-007 direction (engine stores no from-state); §8.
INFERENCE: The table is not a relation the engine enforces, so its contradiction has no mechanism; the specific exclusion governs the general "any →" row; a not_applicable cell is a judgment with a rationale, not tier arithmetic, and no rule requires the engine to assign it today.
RULING: Keep the value and the column; the engine does not assign it; flagged unbuilt. "any → not_applicable" is read as "any state but stated". The "§2.2 condition (3)" cross-reference becomes "(4)". Owner merge for the methodology lines; no code.
OVERTURN: an owner order that a cell be declared non-intersecting by the engine.

**R21 `locator-title-matches-identifier`.**
PREMISES: LED-082/083 (clue store exempt; duplication out of it expected); `pipeline-contract.yaml:2-3` (`status: PROPOSED`, `ratified: false`); `source_locators_integrity` advisory, red on 31 titles; §8's test: a lead's title reaches nothing — admission re-verifies against the payload (5(c)).
RULING: Retire criterion and check. Agent; the contract is not a ratified document.

**R22 BPC reasoning-document layer.**
PREMISES: OPI-229 (reasoning doc manual; survives in part per C-040). LED-151/152 (owner 2026-09-09: "you have to compute it. I can't handle this load manually"). `convergence_assessment` (5 rows) holds the synthesis narrative and the divergence lists MIS-06 requires. `reasoning_doc_citations` 0 rows; `promoted_to_rdc_id` NULL on 101/101; `references/bpc-reasoning/` = `_template.md` + one file; `bpc_metadata` 0 rows; `validate_bpc` blocking, basis `hygiene`, named by no criterion; `nine-step-synthesis` → `validate_reasoning` advisory red; `pre_rehab_banner_audit` quarantined. CLAUDE.md §6 "Only Opus-class models write `best_practice_synthesis`" is routing, not a deliverable.
INFERENCE: The reasoning document was the pre-reset synthesis vehicle; the engine's convergence row now holds the synthesis and nothing reads a document; a blocking check with no criterion and a red check over templates gate nothing that reaches the book.
RULING: Not a live deliverable. Retire `nine-step-synthesis`, `validate_reasoning`, `validate_bpc`, `reasoning_doc_citations_audit`, `pre_rehab_banner_audit`; drop `bpc_metadata` (1.9); writer-retire `update-bpc`; NULL-forward `promoted_to_rdc_id` (25 data migrations INSERT it); `references/bpc-reasoning/` → `_archived/`; CLAUDE.md rule 2's path list shrinks (owner merge). OPI-229's Opus floor attaches to prose the render view surfaces.
OVERTURN: an owner statement that a reasoning document per determination is owed.

**R23 Bytes pointer.** UNDETERMINED (a design, decided by rehearsal). CONSTRAINTS (P11, verified by the fifth pass): junction many-to-many (DR-2026-09-26 §2.2(b)); 433 manifest events, 21 recurring paths; no rename of the junction; backfill under `AFTER_DATA`; 15 of 53 sources keyed on no manifest line. PREMISES bearing on shape: rule 5 (the manifest line is the fact's home today); 5(c). FAVOURED SHAPE: `retrievals` = one row per manifest event, UNIQUE(path, sha256, retrieved_at), loaded by an `AFTER_DATA` schema migration; `search_execution_artefacts` unchanged plus nullable `retrieval_id`; `evidence_sources.retrieval_id` and `source_value_extractions.retrieval_id` nullable until Phase 5 clears the backlog, then NOT NULL by a last migration. What closes it: a row-level rehearsal reproducing 433 rows and a green `--rebuild`, not an owner premise.

**R24 Root pointer.**
PREMISES: `root_id` NULL on 101/101 (query); `external_root_registry` 0 rows, read by three views; CLAUDE.md §4 (a NOT NULL FK into an emptied table is unwritable; a nullable one is not); R6 marker; rule 4.
RULING: Add `root_id REFERENCES external_root_registry(root_id)` nullable, by table rebuild under an `AFTER_DATA` marker (no row carries a value, so none can fail); keep the registry (K23 substrate); file its missing writer as a GAP (rule 10). The only design choice was nullable versus NOT NULL, and §4 excludes NOT NULL on an empty parent. Agent.

**R25 T1 extras.**
PREMISES: LED-204/205 (names from the selected catalogues; screened; listed with source; owner-approved before minting). LED-116. SES-063 (owner accept-or-strike). T1 DDL `/home/user/guidebook-t1/scripts/migrations/104_vocabulary_lifecycle.sql:61-75`: `term_catalogue_origins(term_id PK → terms, catalogue CHECK(5 paths), entry_ref, approval_quote, rationale, …)`; the same file's all-or-none CHECK pattern on `parameter_declinations.revoked_*`. Rule 5 (`approval_quote` copies ledger text whose home is the ledger); rule 8 ("name who judged it": the owner selected the five catalogues, so the CHECK is a judged list). Owner 2026-10-12: less code.
INFERENCE: The fact is required and not derivable (which entry a name came from is recorded at minting), so it cannot be struck; it is 1:1 with `terms` (PK term_id), so a table adds a join and a second key for no cardinality.
RULING: Keep the fact as three nullable columns on `terms` (`catalogue`, `catalogue_entry_ref`, `catalogue_approval_ref` pointing at the ledger entry by date/anchor) with an all-or-none CHECK; NULL = minted from observation. `extraction_follow_ups` kept (P3). Owner's accept-or-strike applies.
OVERTURN: a term with two catalogue origins (then a table is the right shape).

**R26 `case_studies` / `economics_entries` fold.** UNDETERMINED. PREMISES: RES-12 (ratified research contract: structured tables); no later owner statement names them; the 2026-10-09 scan contract reaches design quantities, and a cost is not one; `case_studies` 0 rows, `economics_entries` 1 row (ECON-001, a research-gap statement); 1.3 already drops the case-study children as extractions with `figure_role=finding`. FAVOURED: keep both today under RES-12; fold `case_studies` (a source is a source; outcomes are findings) when R12 is amended; keep `economics_entries`. NEEDS: the owner's amendment of research-contract R12.

**R27 LED-202.** UNDETERMINED. PREMISES: LED-201 (owner: cross-slug figure allowed, tagged; "skimmed values are not publishable"); LED-202 OPEN by the ledger's own record; `extraction_status`/`extraction_method` are distinct columns (PRAGMA). FAVOURED: a full-read figure marked `preliminary` may set a value when tagged for follow-up — the tag is the device the owner attached to the uncertain case and skim is the only exclusion stated. NEEDS: the owner's yes/no on "full read, still preliminary".

**R28 Re-baseline.** PREMISES: rule 3; `--rebuild` 1.6–1.8 s (plan §2); the 458-row `data_migrations` ledger, attestations and session records name migration files; both documents say no. RULING: No; revisit only on a measured cost.

**R29 Deep reproducibility divergence.**
PREMISES: rule 3 (fix forward with a compensating migration); PIP-18; rule 5 ("a parity check is not a fix — survivable, therefore permanent"); 5(c); CLAUDE.md:90-96 (c4c8463); `migration_reproducibility.py:72` EXEMPT_TABLES; R2 removes the cause.
INFERENCE: A wider exemption makes an unreproducible blob the permanent state; the bot's bibliographic values are untrusted under 5(c); the chain is the home of truth.
RULING: Compensating migration, not exemption: after 1.5, rebuild and diff; any bot-written value wanted re-enters through `amend-source`/`--verify-authors` from a persisted payload as a data migration (Phase 5); the rest is reverted to the chain's state by a compensating data migration through the sanctioned path; then OD-9's merge (deep as the sole blocking gate). [UNVERIFIED: the divergence set is the plan's statement; a `--deep` run writes a rebuild file and was not run.]
OVERTURN: a divergent value shown to be payload-backed and not reproducible by any verb.

**R30 Decisions register (OQ-5).**
PREMISES: LED-191, RC-224 (OPEN; recommended retire; "fresh owner answer" required); OPI-105 (OD-7 D2, open, recommended retire); the 2026-10-12 commission is the fresh answer channel. Live: `decisions` 188 rows, last `D-0188` 2026-09-11, while the ledger runs to 2026-10-09. Readers: `scripts/decision_capture.py`, `scripts/doctrine_recheck.py`, `schemas/decision.py`, `test_db_integrity`, `run_checks.py:713` (path classification only). Only inbound FK `item_taxonomy_links.rationale_ref` (dropped in 1.2). D-0188's own text: three homes per decision = rule-5 dual home. `decision-protocol.md:210` names the YAML canonical (ratified process text; not in §8's doctrine list). LED-169.
RULING: Retire both stores: writer-retire the table; move the YAML to `_archived/`; delete `decision_capture.py`, the register reads in `doctrine_recheck.py`, `schemas/decision.py`; keep `decisions` as a frozen infrastructure residual (reproducible; never hard-deleted). The ledger is the single home of rulings; DR files remain as records cited by attestations and point at their ledger entry. decision-protocol §5 is stale (owner merge of one sentence).
OVERTURN: an owner statement reviving the register.

**R31 `national_fw` mapping.** PREMISES: EVI-301/302/303 vs EVI-303/280; `TIER_MAP` (`schemas/tier_derivation.py:53-64`): `national_fw`→5, `standard_eb` national→2, international→4; rule 8; R4 promotes the derivation check. RULING: `TIER_MAP` is the one home; methodology 1.5's "Tier 2 organizational guidelines… or national_fw" is stale (a T2 guideline is `standard_eb` at national scope). Owner merge for the sentence.

**R32 `source_value_extractions` stage.** PREMISES: LED-106 (`:1890`, adopted owner ruling: "a JUDGMENT table, not an evidence-collection table"); LED-108 (owner-quoted: judgment delivers the tier verdict); DRS-098; PIP-10; `stage-map.yaml:138` (evidence, disputed); CLAUDE.md §3 row (evidence holds "extraction"); the plan's evidence step removes the cross-stage write to `data_capture_status`. RULING: Judgment; `extraction_relations` follows its parent; the map and CLAUDE.md §3 are what to correct (CLAUDE.md owner merge).

**R33 Crossing at judgment.** PREMISES: LED-113 (owner-quoted 2026-08-27, `:1998`: "overrule Aug 24 DR. we go evidence>judgment>synthesis"); LED-118; CLM-040. DRS-117 (D-0174, same register timestamp 13:52; its subject is relevance, its applicability sentence restates the 08-24 deferral). D-0184 relies on D-0174 only for "NULL means not adjudicated" (never default a lens code). INFERENCE: On the crossing itself the owner's words are specific and D-0174's clause is a restatement of the overruled deferral; D-0184's reliance concerns defaulting, which is consistent with writing the crossing at judgment with warrant. RULING: LED-113 governs: the crossing is judgment's output, written on the extraction's lens columns, never presupposed and never defaulted; D-0174's sentence is read in that sense; D-0175–0177 are inert (item layer). Agent.

**R34 Cursory scan / relevance / scan contract.** PREMISES: DRS-097, LED-114 (owner: evidence lists concepts; judgment deep-reads); DRS-116/120/121 (D-0174: relevance adjudicated at collection against a topic); LED-195–199 (2026-10-09 scan contract); T1 `103_source_scans_and_ledger.sql:27` and T1 `stage-map.yaml:147` place `source_scans` at evidence. RULING: Three acts on three objects: admission of a source to a topic (collection, D-0174); listing what it contains (`observe-term`, evidence, D-0168); deriving what it states for a parameter (`add-extraction`, judgment). The 2026-10-09 "scan" is the read-state of (source × parameter), recorded at evidence as T1 builds it; its outputs are judgment. No contradiction once named. Agent.

**R35 Axes.** PREMISES: WRK-178–181, LED-076, LED-166 (owner), DRS-006/024; P-AXIS, P-G. RULING: Ruled retired; executed as one act (1.4, R3) with the rule-4 sweep; sentences in D-0170, D-0184, functional-taxonomy and the instrument that treat axes as live are stale; AX- strings in `references/` fall under 1.6(c)'s retired-vocabulary triage.

**R36 Item layer.** PREMISES: WRK-169/170 (owner R1: codes bias research; rows archived not deleted); OD-12 (archival suspended); CLAUDE.md §7 (rows gone from the live DB); `_archived/data/corpus-pre-reset-2026-08-06.db` and the migrations hold the rows; P-UNWRITABLE (16); LED-091; CLM-048. RULING: WRK-170's condition is met by the archive and the chain, so OD-12's suspension is spent; drop the empty cluster (1.2); the four standing documents are stale on contact — functional-taxonomy/conceptual-model edits are owner merge (taxonomy), process texts agent.

**R37 Scan contract vs writer guard.** PREMISES: LED-195/196/201 (owner); P-V2 FAIL (`insert_extraction` refuses a slug the source was not admitted to); P13 (keep `source_slug_links`); `source_value_extractions.slug` is INSERTed by data migrations (rule 5). RULING: Delete the slug-admission refusal once T1 lands; `source_slug_links` stays as the admission record; `sve.slug` is writer-retired and NULL-forwarded. Agent.

**R38 Process contradictions (C-037).** PREMISES and RULINGS by pair, each later/specific over general: (1) PRC-169 vs `/adversarial` vs LED-192 (owner 2026-09-27): pass 1 stays OPEN, RC4 stays advisory; `/adversarial`'s "never to be closed" is corrected to "held open by LED-192". (2) PRC-259 "eleven": rule 7a — replace with the command. (3) PRC-184/203: CLAUDE.md §1 fixes the order (`/orient` to start; `/session-open` before the first Bash call of a batch); both texts say so. (4) PRC-207/214/216: CLAUDE.md §7 (later, specific) governs — folder and `CURRENT` change in one action; the "rename after the PR number exists" clause is subordinate. (5) PRC-160/182: `/batch-done` lists the §1 diff-scoped gate. (6) PRC-176 (I5 unwitnessed MCP searches) vs R8: R8 governs — an MCP search is logged through `log-search` and its result persisted through `record_file` (DR-2026-09-26 §2.2b); I5's text is stale (research-contract edit: owner merge, it is ratified).

**R39 C-039 residue.** (a) LED-159 band: PREMISES: owner 2026-09-13 (`:3120-3124`): a code value confirmed "according to studies" is upgraded; the empty circle is for code "without research backing"; LED-020 (● needs value-level support); owner 2026-09-16 proxy route (direction-only). RULING: the band of the confirming study when it confirms the value; direction-only confirmation stays on the proxy route. Owner merge (markers). (b) LED-168: PREMISES: LED-110, LED-128, LED-154 (specific, four lenses; medical ordered filled) vs a later unqualified three-item enumeration made in the demand-layer context, which the ledger itself did not read as a retirement. RULING: four lenses stand; owner confirm. (c) LED-208 pilot cap: PREMISES: the pilot's scope is replaced (ledger item 7); a fixed count is a hard-coded figure (rule 7a; owner 2026-10-12 "the less hard coded, the better"); LED-208 reserved the question. RULING: no cap carries; the one-source review unit is practice, not rule; owner confirm because LED-208 reserved it. (d) SES-029 (deferral ageing) and SES-041 are gaps, not conflicts; SES-041 was answered by the owner's 2026-09-27 (second) ruling.

**R40 Instrument scope.** PREMISES: CLAUDE.md:5-11 (ruling > instrument > CLAUDE.md); OPI-003; OPI-013 AMENDED; RC-001 (DR-2026-09-26 ratified 2026-09-27, later than the instrument); CLAUDE.md §9 table. RULING: The chain is as CLAUDE.md states; the instrument's four-document read set and its OPERATIVE labels on files its own table supersedes are stale against later ratified records; the read set is §9's table; the instrument remains operative for what no later record touches (its §3 order, §4 acceptance, OD-1). Agent.

**R41 Column-retirement order.** PREMISES: RC-153 (`DR-2026-09-26 … :604-612`: order changed for a `NOT NULL DEFAULT '[]'` column, reason N5 recorded; executed — `citation_mining.connections_produced` is now nullable, PRAGMA); LED-079 (`:884`: general order; never drop). RULING: No conflict: LED-079 is the order for a nullable column; RC-153 is the recorded order for a NOT NULL DEFAULT column (specific over general) and is spent.

**R42 Forward foreign keys.** PREMISES: derived from the live schema and `stage-map.yaml` (command in that pass): 14 edges between spine stages — six into `items` (0 live; dropped by 1.2; a seventh, `item_audit_runs`, is infrastructure and outside the spine); `citation_population_links.citation_id`, `probe_population_links.probe_id` (dropped by 1.2/1.3); `search_executions.mined_ref_id` (11 live), `search_admissions.ref_id` (55), `search_candidates.resolved_ref_id` (7): research recording what became evidence — the re-entrancy CLM-029 licenses; `gap_mining.gap_id → gaps` (0): synthesis→research re-entry (gap-driven search); `evidence_population_match.gap_id → gaps` (0): a judgment that found nothing names the gap it opened; `source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations` (NULL on 101/101): dead under R22, NULL-forward. RULING: No misclassification requires the owner; `gaps` stays at synthesis (what synthesis found absent); the `disputed:` entries for `gaps` and `extraction_relations` close with R32 and this ruling. Agent.

## (D) UNDETERMINED

- R23 bytes pointer: closed by a row-level rehearsal of the favoured shape (433 manifest events, green `--rebuild`), not by an owner premise.
- R26 fold of `case_studies`/`economics_entries`: needs the owner's amendment (or re-affirmation) of research-contract R12.
- R27 LED-202: needs the owner's yes/no on "a figure read in full but still marked `preliminary` may set a published value when tagged".
- R12 sub-fork: needs the owner's yes/no on whether the "Co-1 pass covers ≥9 languages" conjunct of jurisdiction-philosophy §2.3 survives.

## (E) Internal contradictions found and reconciled

- R1 deletes `render-freshness` while R4 keeps a blocking gate: reconciled by §8's test — a freshness gate guards committed artefacts (forbidden by LED-104), the tier gate guards every `stated` cell.
- R3 drops row-bearing tables while R30 refuses to drop `decisions` (188 rows): reconciled by LED-169's own boundary — the axis rows are retired vocabulary the owner ordered out of existence (WRK-178 to 181) and are reconstructible; the decision rows are provenance with no superseding order, so they are frozen, not deleted.
- R7 supplies the band's source while P6/P18 remain deferred: reconciled by ruling only on which text governs (three markers; tier-system §5/§8) and leaving the build sequencing the antagonist passes fixed untouched.
- R19 says vocabulary writers are migration-only while R16 orders a research-PR write to `base_taxonomy_medical`: reconciled because the owner ordered that write (LED-154) and its verb exists; R19 covers tables with no such order.
- R22 retires the reasoning-document layer while C-040 keeps OPI-229's "reasoning doc permanently manual": reconciled by object — OPI-229 attaches to prose a human writes; with no document, it binds the prose the render view surfaces.

## (F) Tags

[ASSUMPTION] The owner's 2026-10-12 commission ("deliver rulings") is read as reaching LED-169(4)'s case-by-case exceptions for the five items on the sheet (R3) and as the "fresh owner answer" LED-191 requires (R30); if the owner intended the sheet as advice only, R3 and R30 revert to owner merge.
[ASSUMPTION] "Owner merge" for contract criteria follows the plan's labelling; `governance/pipeline-contract.yaml` declares itself PROPOSED/unratified, so §8 does not itself require it (R21).
[CORRECTION] The commissioning sentence of 2026-10-12 does have a repository record: `transcripts/harness_db856d85/main.jsonl:5752` ("Fable 5.1 r read-only to resolve as many open questions as possible, ie deliver rulings, based upon logic and premises"), as does the antagonist commission (`:4139`, absorbed mid-turn); an earlier scan of typed turns missed them because mid-turn messages are stored as `queued_command` attachments. The five earlier statements are also in the record (`transcripts/harness_db856d85/main.jsonl:4931-4991`).
[CORRECTION] R42's first draft said seven into `items`; the enumeration then summed to fifteen. `workplan/pipeline-state-graph/walkability.py` (see `WALKABILITY.md`) measures lateral, skip and re-entrant walks and finds fourteen between spine stages, six of them into `items`; R42's headline stands, its count of `items` edges is corrected.
[GAP] Whether `validate_evidence_state` has a live subject was not checked; R5 keeps its two mirrors conditionally.
[CONFIDENCE] medium on R29: the divergence set behind `migration_reproducibility_deep` is taken from the plan; a `--deep` run requires writing a rebuild file and was not run.
[CONFIDENCE] medium on R14 and R25: derived names and shapes the ledger (R14) and SES-063 (R25) explicitly reserve for the owner's confirmation.
[NULL] No file, row or ledger entry was written by the adjudicating pass; every command was read-only (`mode=ro`, `git grep`, `sed -n`, `grep`).
[UNVERIFIED] The plan's claim that OD-7 was "approved": the instrument (:92) and OPI-105 record it OPEN; no ratification was found in the ledger or decisions. *(Reviewer: confirmed above; the plan is corrected.)*
[UNVERIFIED] The "static build now, dynamic later" relay (ADD-002): no primary record found in `sessions/`, `decisions/`, `workplan/` or the ledger.
