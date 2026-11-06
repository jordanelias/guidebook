---
name: run-pipeline
description: >
  Run the Accessible Built Environments pipeline end to end for a topic: research across languages and
  jurisdictions, evidence admission, judgment, synthesis, specification, render, then an adversarial audit
  of accuracy, logic and sequence. Variant `from-evidence` starts at evidence (sources already held, in
  hand or named by ref_id) and skips research. ALWAYS use when asked to "run the pipeline", "research
  <slug> end to end", "process these sources through to specifications", "evidence and beyond", or
  "from evidence onward". Not for single-stage work: use the stage's own skill or `db.py` verb.
---
**Invocation.** `/run-pipeline <slug-or-topic>` runs everything. `/run-pipeline from-evidence <ref_ids | file | DOI list>`
skips research. Everything below is the stage order; a stage is finished when its verification passes, not when its
rows are written. **Re-entry is normal** (new leads go back to research, a new concept back to base), but record
why. Every figure here is derived from the repo; do not paste counts.

**Open once, before the first Bash call:** `bash .claude/hooks/ensure-deps.sh`, `/session-open`, `/orient`. Work on a
scratch DB (CLAUDE.md §4 write path). Rules R1–R17 (SessionStart contract), CLAUDE.md §2 and
`governance/pipeline-contract.yaml` govern; this file orders the work, it does not restate them. Verbs are listed by
`python3 scripts/db.py --help`; if one is missing, stop and file a GAP (rule 10).

## 1. base — read it before touching a source
The catalogue every source is read against: `base_parameters` + `terms`/`term_aliases`, the four lenses
(`base_taxonomy_identity`, `access_needs`, `base_icf`, `base_taxonomy_medical`), `slugs`, `lang_jur_map`.
- Work from ICF/access-need frame, **codes AND names**; never bare axis codes or population umbrellas.
- **Equivalence before minting.** Search terms and aliases first. A synonym is `add-alias`; a duplicate parameter is
  `merge-parameter`; a new concept is `observe-term` → `adjudicate-term` → `add-parameter` (or `decline-parameter` with
  the reason). Claude may *propose* parameters or lens rows; the proposal is a written adjudication with its source,
  not a silent insert. A parameter needs `set-parameter-direction` before stage 6 can use it.
- Check: `scripts/validate_parameters.py`, `scripts/validate_schema.py`.

## 2. research — by topic, across languages and jurisdictions *(skipped by `from-evidence`)*
- Coverage is **slug × language × jurisdiction** from `lang_jur_map`; native-language terms come from the keyword
  compendium, never from memory (R11). Co-1 / T2 / Co-2 pass first (R1).
- **Every query is logged before screening** with `log-search --prior-expectation …` (R8); empties are kept and
  classified query-shape / wrong index / genuine absence (R14). `coverage` and the `v_coverage_*` views show what is
  unsearched. Skills: `multilingual-research`, `functional-deficit-researcher`, `research-log-manager`.
- **Citation mining** of every confirmed T1–T2 anchor, backward and forward, to the depth R2 requires:
  `citation-miner`, yields via `scripts/research/mining_screen.py`; open gaps via `gap-driven-mining`.
- Candidates go through `add-candidate` / `resolve-candidate`; leads into `add-locator`, `add-code-lead`.
- Check: `search_log_completeness.py`, `citation_mining_completeness.py`.

## 3. evidence — admit, then read the whole source against the whole catalogue
- **Admit** only after R9 (DOI pre-check, cross-file the existing ref_id) and R10 (re-retrieve; a publisher block is
  not terminal; Wayback per CLAUDE.md §7). Persist every payload with `scripts/research/retrieval_log.py`; write
  bibliographic fields **from the payload**, then `--verify-authors`. `add-source`; `link-source-slug` to every slug
  the source bears on.
- **Record all bibliographic data:** every author (Co-1 co-authors are the warrant, never dropped), year, title,
  venue, DOI/PMID/ISBN/standard number, URL, tier, retrieval and verification status. Unverified is a value; say it.
- **The slug guides the search, not the reading.** Derive full text (`scripts/research/full_text.py`), read it against
  **every** parameter and lens, not only the slug that found it, and `record-scan --mode catalogue`. That row, with
  `observe-term` for each phrase the source uses (verbatim, unjudged) and `link-source-slug` for each topic it
  touches, is the source's list of everything relevant it contains. Unscanned parameters are debt:
  `scripts/audit/scan_debt.py`, `v_scan_ledger`.
- File economics and case studies in their tables (R12), never in prose.
- Check: `metadata_integrity_audit.py`, `provenance_artefact_audit.py`, `observation_verbatim_audit.py`.

## 4. judgment — assign populations, access needs, ICF codes; store figures so later stages can use them
*(Your "evidence stage adjudication" lives here: CLAUDE.md §6 records the owner's 2026-08-27 ruling that the
lens crossing is judgment's output. Moving it earlier needs a ruling and a `stage-map.yaml` change.)*
- `adjudicate-term` for every observed phrase (NOT-OURS and DEFERRED are answers). `add-extraction` per stated
  figure: parameter, the lens columns (identity, access need, ICF code+name, medical), typed value and unit, verbatim
  claim, locator, `figure_role`, `claim_type`. No locator → `[UNVERIFIED-QUANT]` (R3).
- `relate-extraction` for comparators; `derive-extraction` for computed base+delta figures; `raise-follow-up` for
  doubtful rows. `add-population-match` grades population-of-study vs population-served (R13; children, general
  population and no-participants are PROXY); a dissenting grade is a second row.
- Capture failure, harm and inadequacy as first-class rows (R7).
- Output must be usable *without re-reading the source*: a render or a determination reads the typed row and its
  locator, nothing else.
- Check: `judgment_handoff_shape.py`, `extraction_relations_integrity.py`, `adjudication_integrity.py`.

## 5. synthesis — read rows against each other *(Opus-class only for `best_practice_synthesis`)*
- For each parameter cluster, ask which **other** parameters, populations or equipment change it. Example: swept-path
  figures for different wheelchairs set different turning spaces, corridor widths and door approaches. Make each such
  dependency a row: `add-connection` (mechanism stated), `derive-extraction` where one figure is computed from
  another, `add-conflict` where populations pull opposite ways (`cross-population-conflict-mapper`).
- **Independence:** sources sharing a root are one source (`v_value_independence`, `external_root_registry`).
  `connection-discovery`, `supersession-audit` (`add-supersession-check`), `add-gap` for what is missing.
- Reasoning documents under `references/connection-reasoning/` need an attestation (rule 2).

## 6. specification — best practice is the most accommodating, not the most common
- The state is **computed**: `scripts/assess/assess_cell.py` (see `--help`) per cell, on the scratch DB. Do not
  hand-assign. Then review the output against these tests; a failure is a gate or a GAP, never a hand edit:
  1. **Most accommodating, gentlest, most dignified** value, read by the parameter's direction
     (`higher_is_better` / `lower_is_better`). `contested` means no single value: render the spread with each
     population's direction stated. Frequency of a value is never evidence for it; mode, median and count appear
     nowhere in the rationale.
  2. **Code is a floor.** T4–T6 alone yields a regulatory-stratum claim (`code_floor_only` when T6-only), never best
     practice. A code value stands as best practice only when T1 / Co-1 / T2 / Co-2 evidence directly backs it.
     Expect best practice from academic research, clinical guidelines and advocacy groups.
  3. Rationale states what the value does for the disabled people it serves, with the marker (●/◐/○) and tier mix.
  4. An engine defect is fixed in a tooling-only PR (rule 10), not worked around in the batch.
- `raise-determination-gate` caps a cell at provisional; `retire-specification` reopens one.
- Check: `validate_evidence_state.py`, `derivation_handshake_integrity.py`, `medical_lens_integrity.py`.

## 7. render — read from the database at render time; commit nothing generated
There is no committed renderer; write output to the scratchpad (publish only if asked). From specifications and
`v_determination_provenance`, `v_source_reach_all`, `v_best_practice`:
- web-readable prose per specification, value first, then rationale;
- **a comparison table of all evidence** for the parameter: every extraction, dissent included, with tier, lens,
  population-match grade, locator and verification status, plus sources scanned and **left out, and why**;
- **radical transparency:** direction, rule version, derivation, gates, code-floor flags, gaps and `[UNVERIFIED]`
  items stated on the page, not omitted;
- bibliography via `bibliography-compiler` from `evidence_sources` and `evidence_source_authors`; full author lists,
  DOI links; no citation for a source not in the table.
- Check: `matrix_consistency.py`.

## 8. adversarial audit — a separate critic, then repair
Run `/adversarial` (the `antagonist` agent; never self-review). Brief it with three questions and have it return
`[NULL: …]` where it finds nothing:
- **Accuracy:** do stored bibliographic fields match the payload bytes; does each figure match its locator; do
  cited sources exist? Lenses `L1-existence`, `L2-fidelity`, `S2-mismatch-note-vs-payload`.
- **Logic:** do converging sources share a root; is the tier right; does population-of-study fit population-served;
  was contrary evidence found; does any determination rest on frequency or on code alone? `L3`–`L6`.
- **Sequence:** every row's pointers resolve to rows from an earlier stage; no extraction on an unadmitted or
  unverified source; no determination before direction, extractions and convergence exist; no stage verified
  after the stage that consumed it. **No recorded lens covers sequence** (derive the set with
  `dbcore.check_values(conn, 'adversarial_findings', 'lens')`); record these as method, and file a GAP if it should
  become a lens.
Then `/batch-done`. Under `from-evidence`, `search_log_completeness` correctly reports NOTHING-IN-SCOPE.

## Finish
`scripts/preflight.sh` once, `run_checks.py --selftest` after any rename, commit scratchpad and transcripts
(rule 6), open the PR last and `unsubscribe_pr_activity` at once (rule 9). Research rows and tooling ship in
separate PRs (rule 10).
