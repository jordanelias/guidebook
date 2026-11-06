---
name: run-pipeline
description: >
  Run the Accessible Built Environments pipeline end to end for a topic: research across languages and
  jurisdictions, evidence admission, judgment, synthesis, specification, render, then an adversarial audit
  of accuracy, logic and sequence. Variant `from-evidence` starts at evidence (sources already held, in
  hand or named by ref_id) and skips discovery searching only. ALWAYS use when asked to "run the pipeline",
  "research <slug> end to end", "process these sources through to specifications", "evidence and beyond", or
  "from evidence onward". Not for single-stage work: use the stage's own skill or `db.py` verb.
---
**Invocation.** `/run-pipeline <slug-or-topic>` runs everything. `/run-pipeline from-evidence <ref_ids | file | DOI list>`
starts at stage 3. A stage is finished when its verification passes, not when its rows are written. Re-entry is
normal (a new lead goes back to research, a new concept to base); record why in the session record
(`session-consolidator`). Derive every figure; paste no counts.

**Open once:** `/session-open` first (it sets `CURRENT` before the first Bash call), then
`bash .claude/hooks/ensure-deps.sh`, then `/orient`. Work on a scratch DB (CLAUDE.md §4). This file orders the work;
R1–R17 (SessionStart contract), CLAUDE.md §2 and `governance/pipeline-contract.yaml` are the law. If a verb or field you
need does not exist (`python3 scripts/db.py --help`), stop and file a GAP with `add-gap` (rule 10); never hand SQL.
If two rulings conflict, stop, name both and ask; the later live owner statement wins (rule 0), recorded in the ledger.

**Posture (DR-2026-07-21; owner 2026-10-30: "simply PRESENTING information without claiming correctness").** The
guidebook is a thinking tool, not an authority. Describe and attribute; show derivation, strength and disagreement;
never call a value correct, safe or adequate.

**Scope (OR-8, OR-12a, ledger 2026-10-30).** Exhaustion is per parameter, per bucket member (a jurisdiction **with its
associated language**). In scope: P1+P2+P3 (ledger 2026-10-30 item 7; list in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3); Arabic, Bengali, Hindi and
Swahili are scoped out for now. **Current editions only.** T4–T6 values are accepted as baselines; do not trace their history.

## 1. base — read before touching a source
The catalogue every source is read against: `base_parameters` + `terms`/`term_aliases`, the lenses
(`base_taxonomy_identity`, `access_needs`, `base_icf`, `base_taxonomy_medical`), `slugs`, `lang_jur_map`. Codes AND names;
no bare axis codes or population umbrellas.
- **Equivalence before minting.** Search terms and aliases first. Synonym → `add-alias`; duplicate parameter →
  `merge-parameter`; otherwise a new concept.
- **A new concept arises while a source is in hand** (`observe-term` needs `--ref-id` and a quote from a persisted file),
  so base is re-entered from stages 3–4. Claude may *propose* a parameter or lens row; the owner names it. **Claude never
  generates a phrase, name or alias** (OR-17): it is the source's own wording, present in its jurisdiction and language.
  Put the proposal (source, quote, candidate equivalents) to the owner; `adjudicate-term`, `add-term`, `add-parameter` or
  `decline-parameter` follow their answer.
- `set-parameter-direction` records which way is better, **from an admitted source, never hand-set** (ledger 2026-10-30).
  Without it stage 6 cannot select a value.
- Checks: `validate_parameters.py`, `schema_reference_audit.py`, `identifier_floor_audit.py`.

## 2. research — by topic, across languages and jurisdictions *(skipped by `from-evidence`)*
- Coverage is slug × bucket member, bounded by Scope above. In-language terms come from `term_aliases` and the source's
  own words (R11); never from memory or back-translation. Co-1 / T2 / Co-2 first (R1). Skills: `multilingual-research`,
  `functional-deficit-researcher`, `research-log-manager`.
- **Log every query before screening:** `log-search --prior-expectation … --result-artefact <payload>` (R8). Without
  `--result-artefact` the query→payload link is missing. Keep empties. R14's class (query-shape / wrong index / genuine
  absence) is a column: `--absence-class` (or `amend-search --set-absence-class` once judged; write-once, zero-yield
  searches only). `coverage` and the `v_coverage_*` views show what is unsearched.
- **Citation mining** of every confirmed T1–T3 anchor, backward and forward, to the depth R2 requires: `citation-miner`,
  yields via `scripts/research/mining_screen.py`; open gaps via `gap-driven-mining`.
- Candidates: `add-candidate`, `resolve-candidate`; leads: `add-locator`, `add-code-lead`.
- Checks: `search_log_completeness.py`, `citation_mining_completeness.py`.

## 3. evidence — admit, then read the whole source against the whole catalogue
- **Admit** after R9 (DOI pre-check) and R10 (re-retrieve; a block is not terminal, Wayback per CLAUDE.md §7). Persist
  with `scripts/research/retrieval_log.py`. **Unretrievable:** admit with `verification_status` UNVERIFIED and marker ○,
  no scan row, and never describe it as read. Log the admission as a search (R17): `log-search --origin owner-supplied`
  or `lead-index`.
- **Bibliographic data.** `add-source` takes authors, year, title, journal name, edition, standard number, ISBN, ISSN,
  institution, report and series number, publisher, book title, pages, DOI/PMID, URL, tier, evidence type, Co-1
  provenance and verification; `correct-source` sets volume, issue, article number, pages, title, year and authors
  **from the payload**. Take each field from the payload in hand, never from memory. A field the source does not
  carry stays empty and prints "not recorded". Every author is kept; Co-1 co-authors are the warrant.
- **`--verify-authors` checks only against a JSON payload.** On a `.doc` or other undecodable payload it reports NOT
  SEARCHED; compare the bytes by hand and record that limit in the source's notes. It is not verification there.
- **The slug guides the search, not the reading.** Derive full text (`scripts/research/full_text.py`: PDF and HTML only),
  read it against **every** parameter and lens, `record-scan --mode catalogue --text-scope … --file-sha256 …`. A scan
  row records that a reading happened at a catalogue version, not what it found; what it found is in `observe-term`
  (verbatim), extractions (stage 4, including an `absent` extraction with its quoted passage for a parameter the source
  is silent on) and `link-source-slug` with a relevance note per slug it bears on. Where the text cannot reach `full`,
  record `partial`. Debt: `scripts/audit/scan_debt.py`, `v_scan_ledger`.
- Economics and case studies go in their tables (R12).
- Checks: `metadata_integrity_audit.py`, `provenance_artefact_audit.py`, `observation_verbatim_audit.py`.

## 4. judgment — populations, access needs, ICF codes; figures stored so later stages can use them
*(Your "evidence stage" adjudication lives here: CLAUDE.md §6 records the owner's 2026-08-27 ruling that the lens
crossing is judgment's output. Moving it earlier needs a ruling and a `stage-map.yaml` change.)*
- `adjudicate-term` for every observed phrase (NOT-OURS and DEFERRED are answers). `add-extraction` per stated figure:
  parameter, lens columns (identity, access need, ICF code+name, medical), value and unit, verbatim claim, locator,
  `figure_role`, `claim_type`, and `--relation` (**required**; `none` for an absolute figure). No locator →
  `[UNVERIFIED-QUANT]` (R3). `extraction_status` is `verified` only with a full-scope scan (OR-11a).
- `relate-extraction` for comparators, `derive-extraction` for computed figures, `raise-follow-up` for doubtful rows.
- `add-population-match` grades **identity only** (R13; children, general population, no participants are PROXY); ICF
  and access-need attribution live on the extraction's lens columns.
- Failure, harm and inadequacy (R7) are first-class rows: a `figure_role='finding'` extraction with the verbatim
  claim and `--harm-finding` (a typed flag; only a finding can carry it), plus an `insufficient` edge
  (`--relation insufficient`, to the figure the source says is not enough, e.g. a code value) so the inadequacy is
  joinable. Harm a search surfaced is also `log-search`'s `harm_finding`.
- Output must be usable without re-reading the source: render and determination read the typed row and its locator.
- Checks: `judgment_handoff_shape.py`, `extraction_relations_integrity.py`, `adjudication_integrity.py`.

## 5. synthesis — read rows against each other
- For each parameter cluster ask which **other** parameters, populations or equipment change it (swept-path figures for
  different wheelchairs set different turning spaces, corridor widths, door approaches). File each dependency as a
  **typed edge between extractions** where one figure is computed from or conditioned on another, which may cross
  parameters (`derive-extraction`, `relate-extraction` with `condition_on` / `derived_from`), and as a `connections` row
  (`connection-discovery`) for the narrative: its targets are typed flags (`--parameter`, `--target-slug`,
  `--identity`, `--extraction`, `--methodology`), each a foreign key. `add-conflict` where populations pull opposite ways (`cross-population-conflict-mapper`).
  `connection-discovery --mode cluster-crosstest` enumerates every pair in a cluster so none is skipped.
- **Independence.** Sources sharing a root are one source. `v_value_independence` and `external_root_registry` hold few
  rows; where empty, trace shared roots from the citations by hand. `supersession-audit` → `add-supersession-check`.
- CLAUDE.md §6 reserves `best_practice_synthesis` to Opus-class models; no object of that name exists, so apply the
  floor to all prose you author at this stage [ASSUMPTION: its intended scope]. Reasoning documents need an attestation.

## 6. specification — the most accommodating value found, not the most common
- The state is **computed**: `scripts/assess/assess_cell.py` per cell on the scratch DB (it writes the convergence row
  and the determination together). Do not hand-assign. Review its output against these tests; a failure is a gate or a
  GAP, never a hand edit. A re-run for the same cell is refused: `retire-specification` first.
  1. Name the **most accommodating** value found in practice, read by the parameter's direction. `contested` means no
     single value: show the spread with each population's direction. Frequency is never evidence; the steepest value a
     code allows is never highlighted.
  2. **Code is the weakest tier, not disqualified** (Option A, tier-system §8; ledger 2026-10-30, ratified). A
     determination resting on T4–T6 alone may be named, at the weak band **○**, with the code-derived flag and the
     convergence-not-evidence caveat, and is **never ●**. Evidence that improves on it (academic research, clinical
     guidelines, advocacy and lived-experience work) replaces it and earns the stronger band. If the engine labels a
     code-only cell otherwise, that is an engine defect: tooling PR.
  3. The recorded rationale is the derivation (which sources, what they state, the rule version), not an endorsement.
- `raise-determination-gate` caps a cell at provisional.
- Checks: `validate_evidence_state.py`, `derivation_handshake_integrity.py`, `medical_lens_integrity.py`.

## 7. render — read from the database at render time; commit nothing generated
**Read first (merged PRs on the display of a specification item):** PR #205 (`workplan/2026-10-30-ramp-spec-pages/`:
`owner-rules/spec-page-requirements.md`, `reports/spec-page-design-requirements-2026-10-29.md` R1–R16, the WCAG audit
and defects reports); PRs #207 and #208 (`RENDER-DECISIONS-AND-PIPELINE.md` D1–D20 and the ledger entries "Owner
rulings 2026-10-30" and "Owner statement 2026-10-30 — radical transparency", `references/project-standards.md`);
PR #210 (`RENDER-CONTRACT-parameters-3-and-12.md`: elements E0–E16, rules C1–C11, invariants I1–I6). PR #204 is the
only renderer on main (`scripts/generate/owner_browser_build.py`). The contract is a DRAFT; its section 8 positions
are proposals. Apply, as ruled:
- **No committed file and no static generator.** The renderer selects, groups, counts and formats; it never composes a
  value (C2). Write previews outside the repository (the harness scratch directory), never to `scratchpad/<STEM>/`,
  which rule 6 commits; publish only if asked.
- **Voice (C9):** say what a source states, where, and in what state; no "should" or "must" of the guidebook's own.
  Quote the source's sentence verbatim with attribution. **Translation or paraphrase waits on the owner (OW-1b)**; the
  render table (OW-1) does not exist yet.
- **Lenses:** an audience lens and a disability lens (population, ICF, access need); controls come before the information.
- **Master comparison table:** one row per in-scope jurisdiction, alphabetical, standard and edition under the row,
  detail one click away, every claim row listed with tier, evidence type, population-match grade, locator and
  `extraction_status`. **No row without a value**; the gap is stated under Gaps. A cell with no determination prints its gap.
- **State:** "covered" means read, extracted and verified; provisional is a stage; print "read, none yet verified" while
  that is true. Markers in words beside the symbol (C3a); Co-1 labelled Co-1, co-primary with T1; superseded sources
  shown as superseded (C10); a Co-1 statement derived from the data, never typed.
- **Citations:** APA, alphabetical by first author's last name, full author lists, DOI links, each with its "cited on"
  list, from `evidence_sources` and `evidence_source_authors` (`bibliography-compiler`). A field with no writer
  (stage 3) prints "not recorded". Provenance footer: schema version and database sha256.
- **Accessibility:** WCAG 2.2 AA is a precondition and wins over aesthetics; never self-certify, state only the tests run.
- **Sources of rows:** `v_best_practice` (live, flagged determinations; it shows a code-only one at ○ since migration
  117, per OR-7) and `v_determination_provenance`. A view with 0 rows proves nothing; when no live specification exists
  the page can show only evidence and Gaps (contract section 7).
- **No check examines rendered output** (`register-invariants` has `check: null`): walk contract invariants I1–I6 by hand.

## 8. adversarial audit — a separate critic, then repair
`/adversarial` (the `antagonist` agent; never self-review). Derive the lens set
(`dbcore.check_values(conn, 'adversarial_findings', 'lens')`); **a pass closes only when every lens is covered**, so
assign each to a question and omit none:
- **Accuracy:** stored bibliographic fields against the payload bytes, figures against locators, existence. L1, L2, S2.
- **Logic:** shared roots, tier, population fit, contrary evidence, frequency or code standing in for evidence,
  posture. L3–L7, L8 (was a zero-yield search well-formed), S1, S3.
- **Sequence:** every pointer resolves to an earlier stage's row; no extraction on an unadmitted or unverified source;
  no determination without direction and extractions; no stage verified after its consumer ran. `S4-sequence`.
Then `/batch-done`. **`from-evidence` still faces its blocking gates:** R17 (a logged search per admission), R1 (a
Co-1/Co-2 search or source, or a reasoned `CO1-NOT-APPLICABLE` in a search's `findings_note`) and R2 (`citation_mining`
rows for admitted T1–T3 anchors). Mine the anchors; R10 fetches leave WebFetch ledger lines that
`search_log_completeness` reads.

## Resume and exceptions
Resume from live state, not memory: `/orient`; unadjudicated observations (`observed_terms` with no
`term_adjudications` row); `scan_debt.py`; open follow-ups; parameters with extractions and no live specification.
The scratch DB is disposable and the canonical sha256 does not move until the migration applies, so a mid-batch failure
costs only the unemitted rows. A blocked source: Wayback, else admit UNVERIFIED. A zero-yield search is a completed
unit of work. Finish: `scripts/preflight.sh` once, `run_checks.py --selftest` after any rename, commit scratchpad and
transcripts (rule 6), open the PR last and `unsubscribe_pr_activity` at once (rule 9); research rows and tooling ship in
separate PRs (rule 10).
