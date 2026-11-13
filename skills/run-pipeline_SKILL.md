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
normal (a new lead goes back to research, a new concept to base); record why, at the moment of return, in the
session record `sessions/<STEM>.md` (with `attestations/sessions_<STEM>.json`, validated against
`schemas/attestation.schema.json`, CLAUDE.md rule 2), and commit both at the next natural break (rule 6). The
database holds no marker for a return; the record and `scratchpad/<STEM>/commands.jsonl` are the trace. `session-consolidator` is a prior-version procedure and is not
run. Derive every figure; paste no counts.

| Variant | Starts at | Skips |
|---|---|---|
| `full` (default) | stage 1 | nothing |
| `from-evidence` | stage 3 | discovery searching only; every later gate still applies |

**Open once:** `/session-open` first (it sets `CURRENT` before the first Bash call), then
`bash .claude/hooks/ensure-deps.sh`, then `/orient`. Work on a scratch DB (CLAUDE.md §4): `cp data/guidebook.db $S/guidebook.db`
and `GUIDEBOOK_DB_PATH=$S/guidebook.db` inline on every call. `--session` takes the bare stem, the content of
`scratchpad/CURRENT` (the writer strips a trailing `.md`). This file orders the work; the research contract
(`governance/research-contract.yaml`, rule ids `R1`…`R17`, rendered by the SessionStart hook), CLAUDE.md §2 and
`governance/pipeline-contract.yaml` are the law. **`python3 scripts/db.py <verb> --help` is the one home of a verb's
flags and vocabularies** (rule 8: every `choices=` is read from the column's own CHECK); this file names only the flags
that carry a rule. If a verb or field you need does not exist, stop and file a GAP with `add-gap` (rule 10); never hand
SQL. If two rulings conflict, stop, name both and ask; the later live owner statement wins (rule 0), recorded in the ledger.

**Posture (DR-2026-07-21; owner 2026-10-30: "simply PRESENTING information without claiming correctness").** The
guidebook is a thinking tool, not an authority. Describe and attribute; show derivation, strength and disagreement;
never call a value correct, safe or adequate.

**Scope (OR-8, OR-12a, ledger 2026-10-30).** Exhaustion is per parameter, per bucket member (a jurisdiction **with its
associated language**, a `lang_jur_map` row). In scope: P1+P2+P3 (ledger 2026-10-30 item 7; list in
`workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3); Arabic, Bengali, Hindi and Swahili are scoped out for now. What
is owed has one home, the view `v_research_scope`: every `lang_jur_map` row not recorded `scoped-out` in `scope_status`
(column added by migration 122; the view by migration 123); a NULL is owed, so an unrecorded scope never shrinks the requirement, and the fill of the column is a
data PR. `db.py coverage --slug` reads it and reports slug_status and merged_into, pairs_required, pairs_searched, pairs_unsearched (the
`[language, jurisdiction]` pairs still owed), searches_outside_scope (logged searches whose pair is not owed) and
jurisdictions_unreachable (owed rows `base_jurisdictions` does not hold: a search there cannot be logged, so
they stay unsearched). `complete` is false while anything owed is unsearched or refused by the declared vocabulary,
and false over an empty requirement (open owner question 5 of the 2026-11-06 round-3 adjudication,
`workplan/2026-11-06-run-pipeline-round-3-adjudication.md`). For a slug whose slug_status is neither `ACTIVE` nor
`STUB` it also reports owes_searches false: the slug named in merged_into owes them, so search there. **Current
editions only.** T4–T6 values are accepted as baselines; do not trace their history.

## 1. base — read before touching a source
The catalogue every source is read against: `base_parameters` + `terms`/`term_aliases`, the lenses
(`base_taxonomy_identity`, `access_needs`, `base_icf`, `base_taxonomy_medical` — empty until its owed rows land),
`slugs`, `lang_jur_map`. Codes AND names; no bare axis codes or population umbrellas.
- **Equivalence before minting.** Search terms and aliases first. A phrase a source uses for a term we hold is an
  alias, reached only through the chain `observe-term` (its `--context-quote` must be found byte-for-byte in a file
  saved for the source: a `scripts/research/full_text.py` derivation or the fetched page) → `adjudicate-term
  --outcome NAMES-EXISTING --term-id` → `add-alias --alias-type` (from the CHECK; it writes `attestation`, `other_source`
  unless `--attestation instrument`). A form read where no observation exists takes the base route (`add-alias --alias
  --language --jurisdiction --source-url --source-page|--source-clause --attestation`; the pair must be in `lang_jur_map`);
  a search aid with no locator takes `--seed owner_supplied|model_seed` and is never vocabulary. A search names the forms it
  fired with `log-search --form-id`. A comparator ("not steeper than")
  or a value is not a name for the concept: adjudicate it `NOT-OURS`. The name rule is the writer's own: `add-term
  --canonical-en` and `rename-term --canonical-en` refuse a name carrying a digit, a comparison symbol, a `min` or
  `max` word, or a comparator word (`than`, `at least`, `at most`, `no more`, `no less`, `no fewer`, `no greater`,
  `not exceeding`, `exceed`); a definition is checked for digits, symbols and `min`/`max` only, because a definition is
  ordinary English. A duplicate parameter → `merge-parameter`; otherwise a new concept.
- **A new concept arises while a source is in hand** (`observe-term` needs `--ref-id` and a persisted quote), so base
  is re-entered from stages 3–4. **Claude never generates a phrase, name or alias** (OR-17): it is the source's own
  wording, present in its jurisdiction and language. `add-term --from-observation` mints the term and its NAMES-NEW
  adjudication together; it refuses a near match (shared tokens with a term or alias) unless `--distinct-from
  TERM-ID` names it and the rationale says why. `adjudicate-term` never writes NAMES-NEW. Owner approval is the data
  PR the owner reads (OR-17: "bulk, with me reading the PR"); `add-parameter` and `decline-parameter` take no
  approval flag — `--approval-ref` belongs to the catalogue route (`mint-term-from-catalogue`, D3) only.
- `set-parameter-direction --ref-id` records which way is better **from an admitted source** that holds an
  extraction for the parameter (ledger 2026-10-30, ACTION 6; stored in `base_parameters.direction_ref_id`); a
  direction with no source is refused. Without a direction stage 6 cannot select a value and says so in its gap. A
  direction set before that rule carries no source (derive: `SELECT parameter_id FROM base_parameters WHERE
  accessibility_direction IS NOT NULL AND direction_ref_id IS NULL`): it stands as history, and whether it is
  backfilled, and whether `contested` takes a source, are open owner question 7 of the 2026-11-06 round-3 adjudication.
- Checks: `scripts/validate_parameters.py`, `scripts/audit/schema_reference_audit.py`,
  `scripts/audit/identifier_floor_audit.py`.

## 2. research — by topic, across languages and jurisdictions *(skipped by `from-evidence`)*
- Coverage is slug × bucket member, bounded by Scope above. In-language terms come from `term_aliases` and the source's
  own words (R11); never from memory or back-translation. Co-1 / T2 / Co-2 first (R1). Skills: `multilingual-research`,
  `functional-deficit-researcher`, `research-log-manager`.
- **Log every query before screening:** `log-search --prior-expectation … --slug … --language … --jurisdiction …`
  (R8). A search names what it looked for (`--slug`, `--parameter` or `--mined-ref-id`); `--slug` must exist and
  `--parameter` must be active. `--language` is a two-letter code from `lang_jur_map` (derive: `SELECT DISTINCT
  language FROM lang_jur_map`), folded to upper case on write, and a language the map does not hold is refused (the map is the vocabulary of research
  languages; a new one is a doctrine change, owner question 5); `--jurisdiction` is a code `base_jurisdictions`
  holds (a sub-national code counts toward its parent country in `coverage`; admit one with `add-jurisdiction`). The pair is not checked: a search in any declared jurisdiction is logged, and the result's
  in_research_scope says whether the pair counts toward what `coverage` owes (`v_research_scope`). A search outside it
  is counted apart (searches_outside_scope), never refused (R8). `--result-artefact retrieval-log/<session>/<file>`
  (repeatable) links a persisted payload whose URL carries the query's host and identifying value; the path is the
  manifest's own pointer shape, resolved against the repository's `retrieval-log/` whatever `GUIDEBOOK_RETRIEVAL_LOG`
  says. A WebSearch has no payload, and `scripts/audit/search_log_completeness.py --session <STEM>` reads the harness
  ledger for those. Keep empties. R14's class (query-shape / wrong index / genuine absence) is a column:
  `--absence-class` (or `amend-search --exec-id N --append-note … --set-absence-class` once judged; `--append-note` is
  required on every `amend-search`, the class is write-once, and only a search that found nothing takes it); the batch
  gate reads the column. `coverage --slug` and `v_coverage_priority` (the unsearched language × jurisdiction anti-join)
  show what is unsearched.
- **Citation mining** of every confirmed T1–T3 anchor, backward and forward, to the depth R2 requires: `citation-miner`,
  yields via `scripts/research/mining_screen.py`; open gaps via `gap-driven-mining`. `unmined --slug` prints each
  source's `ref_id`; `is-mined --slug … --ref REF-NNNNN` and `log-mining --slug … --ref REF-NNNNN --direction
  backward|forward` name the slug and the reference id (a label is refused). A `deferred` source
  with a `deferred_reason` is on the `unmined` worklist and is not a violation (owner 2026-09-18);
  `scripts/audit/citation_mining_completeness.py` reports violations only.
- Candidates: `add-candidate`, `resolve-candidate`; leads: `add-locator` (omit `--ref-id`: the writer computes it, as
  `db.py next-id ref` shows; a given id must equal it), `add-code-lead`.
- Checks: `scripts/audit/search_log_completeness.py --session <STEM>`, `scripts/audit/citation_mining_completeness.py`.

## 3. evidence — admit, then read the whole source against the whole catalogue
- **Admit** after R9 (DOI pre-check) and R10 (re-retrieve; a block is not terminal, Wayback per CLAUDE.md §7). Persist
  with `scripts/research/retrieval_log.py`. Omit `add-source --ref-id`: the writer computes it. If exactly one staged,
  non-`RETIRED` locator matches the new source (same DOI, PMID, PMCID, ISBN, standard number or URL, else the same
  normalised title) the source lands under that locator's id, so a lead staged by `add-locator` keeps the id it was
  given; none matches, it takes `db.py next-id ref`; several match, the writer refuses and names them (retire the
  duplicate lead with `update-locator --status RETIRED`). A given id must equal what omitting it yields, and any other
  id, another staged lead's included, is refused naming the lead it was staged for. Then `update-locator --ref-id …
  --status PROMOTED`.
  **Unretrievable:** admit with `--verification-status UNVERIFIED --processing-blocked-reason <from the CHECK>` and
  marker ○. The reason is for text that could not be obtained or read, and only the values the BLOCKED case of
  `v_scan_ledger` lists count as that (derive: `SELECT sql FROM sqlite_master WHERE name = 'v_scan_ledger'`, the header
  and the BLOCKED case); the view is the one home of that classification, and the writers and gates read its status,
  never the column. Such a source shows as `BLOCKED` rather than as reading debt, no extraction can be written on it
  until it is VERIFIED, and it is never described as read. Set the reason at admission, or later with `amend-source
  --ref-id … --field processing_blocked_reason --replacement <value> --reason <why>`. **Nothing clears it:** `record-scan`
  writes `source_scans` only, and the column stays as the retrieval record. The ledger alone says whether a pair is still
  blocked. A full reading outranks the block (the pair reads READ-NOTHING-FOUND, or EXTRACTED once a row is written). A
  partial, fragment or abstract reading does not: the pair reads `BLOCKED` with that reading's scan beside it, which is not
  reading debt. "Abstract read, full text paywalled" is recorded as the abstract `record-scan` plus the reason, and the
  full text stays owed while it can be obtained (Wayback first, CLAUDE.md §7). The writers refuse the two values that
  restate a typed fact: `no-quantified-claims` (a source read with nothing found is the reading, `record-scan
  --text-scope full`, and no extraction row; the ledger derives READ-NOTHING-FOUND from that) and `superseded` (the typed
  home is `evidence_sources.superseded_by_ref_id`, written by `supersede-source --ref-id A --by B --reason …`).
  `out-of-scope` and `tier-not-required`, and `no-doi` and `not-indexed`, are in the CHECK and the ledger reads them as no
  reason, so the source still owes its reading (open owner question 8, extended, of the 2026-11-06 round-3
  adjudication). Log the admission as a search (R17): `log-search --origin owner-supplied` or `lead-index`.
- **Bibliographic data.** `add-source` takes authors, year, title, standard number, institution, report and series
  number, publisher, book title, pages, DOI/PMID, URL, tier, evidence type, Co-1 provenance and verification.
  `correct-source --field <f> --log-session <retrieval-log session>` then sets the payload-backed fields **from the
  persisted payload** (the list is `correct-source --help`, derived from the payload-field table in
  `scripts/research/retrieval_log.py`), and `scripts/research/retrieval_log.py --verify-authors --session <that session>` diffs authors and those fields for
  every source whose payload the session logged (session-wide, not per source). A payload whose author array repeats a
  name is a malformed deposit (an affiliation filed as an author, or an author filed twice): `--verify-authors` reports it MALFORMED-PAYLOAD and
  still compares the stored rows against the payload's family-named (human) authors, so a damaged byline is a cross
  there too; `correct-source --field authors` refuses to write from it. Never type one of them from memory. A field
  the source does not carry stays empty and prints "not recorded". Every author is kept; Co-1 co-authors are the warrant.
- **`--verify-authors` checks only against a JSON payload.** Bytes it cannot parse (a `.doc`, say) are listed under
  NOT INGESTED, and a source with no DOI under UNEXAMINABLE; compare the bytes by hand and record that limit in the
  source's notes. It is not verification there.
- **The slug guides the search, not the reading.** Derive full text: `python3 scripts/research/full_text.py --ref-id R
  --session <STEM>` (PDF and HTML only; `--artefact <file>` when it reports AMBIGUOUS). It writes the derivation under
  `retrieval-log/<STEM>/`, which is tracked and committed — an R10 artefact, not scratch. Point `GUIDEBOOK_RETRIEVAL_LOG`
  at a scratch root only for a rehearsal, seed that root with the held session directories, and give the same variable to
  `record-scan`, `add-extraction` and `observe-term` alike (each reads its bytes from it); `log-search
  --result-artefact` does not, as above. Read the derivation against **every** parameter and lens, then `record-scan
  --mode catalogue --text-scope … --file-sha256 … --method …`; the other scopes are the column's CHECK (`record-scan
  --help`).
  `full` is refused over a fetched file (a landing page is a record about the document, not the document: derive the
  text first) and over a derived text carrying fewer pages than the document. Over a derived text with no page markers
  it lands as the operator's claim: the result says uncounted, the row keeps `pages_read` empty, and `scan_debt` prints
  a count of such readings ("full readings nothing counted") for the adversarial pass to read. Derive the text from the
  PDF with `full_text.py` where the pages can be counted. A second reading of a source is normal
  (ledger 2026-10-30, ACTION 2). A scan row records that a reading happened at a catalogue version, not what it found;
  what it found is in `observe-term` (verbatim), extractions (stage 4, including an `absent` extraction with its quoted
  passage for a parameter the source is silent on) and `link-source-slug --rationale` (the relevance note per slug;
  `add-source --slug` leaves it empty, this fills it once and refuses to overwrite grounds). Debt:
  `scripts/audit/scan_debt.py`, `v_scan_ledger`.
- Economics and case studies go in their tables (R12).
- Checks: `scripts/audit/metadata_integrity_audit.py`, `scripts/audit/provenance_artefact_audit.py`,
  `scripts/audit/observation_verbatim_audit.py`.

## 4. judgment — populations, access needs, ICF codes; figures stored so later stages can use them
*(Your "evidence stage" adjudication lives here: CLAUDE.md §6 records the owner's 2026-08-27 ruling that the lens
crossing is judgment's output. Moving it earlier needs a ruling and a `stage-map.yaml` change.)*
- `adjudicate-term` for every observed phrase (`NOT-OURS` and `DEFERRED` are answers). `add-extraction` per stated
  figure: parameter, at least one lens column (`--identity`, `--icf` code and name, `--needs`, `--medical`; an extraction
  is stated in at least one lens, D-0182), value and unit (a number the source writes in words, or with an ambiguous
  mark, is entered as a numeral in `--claimed-value` with the source's own wording in `--value-as-written`;
  `--comparator` for a numerical figure, `=` for a point), `--claim-text`
  verbatim, locator, `--figure-role`,
  `--claim-type`, and `--relation` (**required**; `none` for an absolute figure). `add-extraction --help` prints every
  vocabulary, each read from its own column: `claim_type`, `extraction_method`, `extraction_status`, `root_type`,
  `measurement_paradigm`, `device_class`, `figure_role` and `comparator` of `source_value_extractions`; `relation`,
  `to_kind`, `stated` and `input_role` of `extraction_relations`. **The writer refuses:** a source not `VERIFIED`; a
  (source, parameter) no `source_scans` row covers (record the reading first); `--extraction-status verified` without a
  full-scope covering reading (OR-11a; `amend-extraction` the same); a numerical or range row with no locator —
  `--source-section` suffices below tier 4, the locator hierarchy (`--loc-division` … `--loc-subclause`) is
  required from tier 4 — unless `[UNVERIFIED-QUANT]` is in `--notes` (R3); `--verbatim-exempt` when a decodable body is held for the source (a fetched `text/*` page, a derived text, or a PDF
  with a text layer) and no page render is persisted (`scripts/research/page_image.py`; the refusal names the files and the
  verb), and `observe-term --verbatim-exempt` is refused on the same ground; a `--claimed-unit` that is a sentence rather
  than a scale (the condition is its own row, `--relation condition_on`; applicability is `--setting`); a quantity figure
  the engine cannot place on a scale (`8.33%`, `1/12`, `12:1`, `1 in 12`, a decimal comma; the refusal names the fix); a
  value-supplying numerical row with no `--comparator`; a `derived` figure that disagrees with its own base + delta. The
  exemption is accepted on a persisted page render, or on a source holding nothing decodable; the marker it writes
  names the renders, so the adversarial pass can check the locator against them; a
  byte-identical second row (a divergent reading is a contest, D-0168, and is written).
- `relate-extraction` for comparators (`--cross-source <reason>` makes a condition drawn from another document an
  explicit synthesis act; the quote verifies the from-source only), `derive-extraction` for computed figures,
  `raise-follow-up` for doubtful rows — its `--reason` vocabulary is `extraction_follow_ups.reason` (`raise-follow-up
  --help` prints it, and says what each means: `absence-needs-tested-value` is only for a `claim_type='absent'` extraction whose tested value is still to find by backward citation mining; a doubt it cannot name is a GAP until the owner extends it).
- `add-population-match` grades **identity only** (R13; children, general population, no participants are PROXY); ICF
  and access-need attribution live on the extraction's lens columns. A second grade for the same source and
  population is a contest, written with a NOTE, never refused (CLAUDE.md §4).
- Failure, harm and inadequacy (R7) about a **parameter's value** are first-class rows: a `figure_role='finding'`
  extraction with the verbatim claim and `--harm-finding` (a typed flag; only a finding can carry it), **plus an
  `insufficient` edge in the same call** (`--relation insufficient`, with its quote, to the figure the source says is
  not enough, e.g. a code value, by `--to-extraction` or `--to-label` + `--to-kind`); the writer refuses the flag
  without the edge. Harm **not tied to a parameter** (a room-type or whole-route failure) has no judgment row, because
  judgment rows are keyed on a parameter: it is `log-search`'s or `add-candidate`'s `harm_finding` at research, plus
  a GAP naming it so it is not lost.
- Output must be usable without re-reading the source: render and determination read the typed row and its locator.
- Checks: `scripts/audit/judgment_handoff_shape.py`, `scripts/audit/extraction_relations_integrity.py`,
  `scripts/audit/adjudication_integrity.py`, and `scripts/audit/verified_scan_integrity.py`, which examines every live
  extraction and prints three classes, each with its remedy: VERIFIED-WITHOUT-FULL-READING, SOURCE-NOT-VERIFIED and
  NO-COVERING-READING.

## 5. synthesis — read rows against each other
- For each parameter cluster ask which **other** parameters, populations or equipment change it (swept-path figures for
  different wheelchairs set different turning spaces, corridor widths, door approaches). File each dependency as a
  **typed edge between extractions** where one figure is computed from or conditioned on another, which may cross
  parameters (`derive-extraction`, `relate-extraction` with `condition_on` / `derived_from`), and as a `connections` row
  (`connection-discovery`) for the narrative: its targets are typed flags (`--parameter`, `--target-slug`,
  `--identity`, `--extraction`, `--methodology`); four are foreign keys, `--methodology` is a name with no table. The
  id is computed (omit `--con-id`); the type sets the arity the writer holds (`CROSS-PARAMETER` and
  `COMPOUND-INTERACTION` two or more parameters, `CROSS-POPULATION` two or more identities, `METHODOLOGY` one
  `--methodology`), and a type the CHECK admits that the writer holds no arity for is refused by name; a duplicate type
  + target set is refused; a merged or retired parameter is refused; `--confidence` is `connections.confidence` (`add-connection
  --help` prints it) — a relationship with no direct evidence is a CR gap. `add-conflict --parameter-id` where populations pull opposite ways
  (`cross-population-conflict-mapper`; the pair is ordered by the writer). `connection-discovery` in
  category-crosstest mode (a prose mode, not a CLI) enumerates every pair in a cluster so none is skipped. An edge
  across two sources needs `--cross-source <reason>`. No code reads `connections`, `connection_targets` or `conflicts`:
  the reader of those rows is the operator at the adversarial pass, and whether the engine should consume them is open
  owner question 12 of the 2026-11-06 round-3 adjudication.
- **A lead met while reading rows against each other** (a source or standard named in passing) is recorded, never
  held in the session record alone: `add-locator` for the lead itself (omit `--ref-id`), and `log-search --origin
  incidental` for a query run to chase it (a non-planned origin takes no `--target-tier`, `--target-evidence-type` or
  `--target-scope`). It re-enters research (§2); say why in the session record.
- **Independence.** Sources sharing a root are one source. `v_value_independence` and `external_root_registry` hold few
  rows; where empty, trace shared roots from the citations by hand. `supersession-audit` → `add-supersession-check`.
- CLAUDE.md §6 reserves best-practice synthesis to Opus-class models; no database object of that name exists, so apply
  the floor to all prose you author at this stage [ASSUMPTION: its intended scope]. Reasoning documents need an attestation.

## 6. specification — the most accommodating value found, not the most common
- The state is **computed**: `python3 scripts/assess/assess_cell.py --db $S/guidebook.db --emit-sql <file>
  --parameter-id N --slug <slug> --identity|--icf|--needs|--medical <code> --session <STEM> --stamp <ISO instant>
  [--report-json <file>]` per cell on the scratch DB (it takes `--db`, not `GUIDEBOOK_DB_PATH`; it writes the convergence
  row and the determination together; `--slug` names an existing topic, `SELECT slug FROM slugs`, and selects no
  evidence, and a slug that does not exist is refused). **A cell** is a parameter × the lens codes given (`specifications`' unique
  row identity); today every lens of a parameter gathers the same extractions, and whether a lens should filter them
  is an open owner question. Do not hand-assign. Review its output against these tests; a failure is a gate or a
  GAP, never a hand edit. A re-run for the same cell is refused: `retire-specification` first.
  1. Name the **most accommodating** value found in practice, read by the parameter's direction. `contested` means no
     single value: show the spread with each population's direction. Frequency is never evidence; the steepest value a
     code allows is never highlighted. A cell with no direction stays `pending` and names `set-parameter-direction` in
     its gap. A parameter whose direction stands with no source (history from before the source rule; derive it as in
     stage 1) is read by that direction, and the report's `direction_ref_id` is NULL for it; whether that is
     backfilled is open owner question 7 of the 2026-11-06 round-3 adjudication.
  2. **Code is the weakest tier, not disqualified** (Option A, tier-system §8; ledger 2026-10-30, ratified). A
     determination resting on T4–T6 alone may be named, at the weak band **○**, with the code-derived flag and the
     convergence-not-evidence caveat, and is **never ●**. Read the report, not one flag: `regulatory_stratum_only` and
     `code_floor_only` are 1 on a code-only threshold with no direction; once an anchoring-tier finding supplies the
     direction the engine writes a proxy determination (`rests_on_proxy_inference` 1, `tier_basis` ending
     `(proxy_inference)`) and sets `regulatory_stratum_only` to 0, still at ○. Evidence that improves on it (academic
     research, clinical guidelines, advocacy and lived-experience work) replaces it and earns the stronger band. If
     the engine labels a code-only cell otherwise, that is an engine defect: tooling PR.
  3. The recorded rationale is the derivation (which sources, what they state, the rule version), not an endorsement.
- `raise-determination-gate` caps a cell at provisional.
- Checks: `scripts/validate_evidence_state.py`, `scripts/audit/derivation_handshake_integrity.py`,
  `scripts/audit/medical_lens_integrity.py`.

## 7. render — read from the database at render time; commit nothing generated
**Read first (merged PRs on the display of a specification item):** PR #205 (`workplan/2026-10-30-ramp-spec-pages/`:
`owner-rules/spec-page-requirements.md`, `reports/spec-page-design-requirements-2026-10-29.md` R1–R16, the WCAG audit
and defects reports); PRs #207 and #208 (`RENDER-DECISIONS-AND-PIPELINE.md` D1–D20 and the ledger entries "Owner
rulings 2026-10-30" and "Owner statement 2026-10-30 — radical transparency", `references/project-standards.md`);
PR #210 (`RENDER-CONTRACT-parameters-3-and-12.md`: elements E0–E16, rules C1–C11, invariants I1–I6). **No specification
renderer exists** (derive: `ls scripts/generate/`); `scripts/generate/owner_browser_build.py` builds the owner's
review page, not a specification page, and the page build (T-5 of `workplan/2026-10-23-pipeline-resolution-workplan.md`)
is not built. Until it lands, this stage is walking the contract by hand against the database and writing the
findings to the session record. The contract is a DRAFT; its section 8 positions are proposals. Apply, as ruled:
- **No committed file and no static generator.** The renderer selects, groups, counts and formats; it never composes a
  value (C2). Write previews outside the repository (the harness scratch directory), never to `scratchpad/<STEM>/`,
  which rule 6 commits; publish only if asked.
- **Voice (C9):** say what a source states, where, and in what state; no "should" or "must" of the guidebook's own.
  Quote the source's sentence verbatim with attribution. **Translation or paraphrase waits on the owner (OW-1b)**; the
  render table (OW-1) does not exist yet.
- **Lenses:** an audience lens and a disability lens (population, ICF, access need); controls come before the information.
- **Master comparison table:** one row per in-scope jurisdiction (the jurisdictions of `v_research_scope`),
  alphabetical, standard and edition under the row, detail one click away, every claim row
  listed with tier, evidence type, population-match grade, locator and `extraction_status`. **No row without a
  value**; the gap is stated under Gaps. A cell with no determination prints its gap. What the data cannot yet supply
  (jurisdictions with no extraction, tier 4+ sources with no `standard_number`, sources with no population match,
  untranslated quotes) is research, filed as GAPs, not patched in the renderer.
- **State:** "covered" means read, extracted and verified (`extraction_status` as stored, and
  `scripts/audit/verified_scan_integrity.py` prints, by class, VERIFIED-WITHOUT-FULL-READING (verified rows no full
  reading covers), SOURCE-NOT-VERIFIED and NO-COVERING-READING); provisional is a stage;
  print "read, none yet verified" while that is true. Markers in words beside the symbol (C3a); Co-1 labelled Co-1,
  co-primary with T1; superseded sources shown as superseded (C10); a Co-1 statement derived from the data, never typed.
- **Citations:** APA, alphabetical by first author's last name, full author lists, DOI links, each with its "cited on"
  list, from `evidence_sources` and `evidence_source_authors` (`bibliography-compiler`). A field with no writer
  (stage 3) prints "not recorded". Provenance footer: schema version and database sha256.
- **Accessibility:** WCAG 2.2 AA is a precondition and wins over aesthetics; never self-certify, state only the tests run.
- **Sources of rows:** `v_best_practice` (the live `stated`/`provisional` determinations; it shows a code-only one at ○
  since migration 117, per OR-7) and `v_determination_provenance`. A `pending` cell is live (`retired_at IS NULL`) but
  not in `v_best_practice`. The trace from a determination to its sources is `v_determination_provenance`, filtered on
  `role` (the values of `specification_extraction_links.role`: governing, conditioning and excluded, with
  `exclusion_reason`). `v_best_practice.governing_refs` is frozen history: it is set on rows written before its writer was
  retired (derive: `SELECT specification_id FROM specifications WHERE governing_refs IS NOT NULL`), and the column stays
  because committed data migrations insert it (derive: `grep -l governing_refs scripts/migrations/data_*`). The sources
  a determination rests on are its `specification_source_links` rows with role `governing`, read through
  the governing_refs function of `scripts/dbcore.py`; read those, and the view per row with its role, never the column. A view with 0 rows proves
  nothing; when no live specification exists the page can show only evidence and Gaps (contract section 7).
- **No check examines rendered output** (`register-invariants` has `check: null`): walk contract invariants I1–I6 by hand.

## 8. adversarial audit — a separate critic, then repair
`/adversarial` (the `antagonist` agent; never self-review). The critic's closing `json adversarial-findings` block,
the rule that its transcript is committed before the pass is recorded, and what "covered" means (a row per lens, at
least one `SURVIVED` row naming a committed artefact) are defined in `.claude/agents/antagonist.md` and
`.claude/commands/adversarial.md`: read both. Derive the lens set —
`python3 -c "import sys, sqlite3; sys.path.insert(0, 'scripts'); import dbcore; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True); print(sorted(dbcore.check_values(c, 'adversarial_findings', 'lens')))"`
— and assign each to a question, omitting none:
- **Accuracy:** stored bibliographic fields against the payload bytes, figures against locators, existence. L1, L2, S2.
- **Logic:** shared roots, tier, population fit, contrary evidence, frequency or code standing in for evidence,
  posture. L3–L7, L8 (was a zero-yield search well-formed), S1, S3.
- **Sequence:** every pointer resolves to an earlier stage's row; no extraction on an unadmitted or unverified source;
  no determination without direction and extractions; no stage verified after its consumer ran. `S4-sequence`.
`close-adversarial-pass --pass-id N` refuses a pass with a lens missing, with no SURVIVED row, or with a SURVIVED row
whose artefact resolves to no existing file (lead the artefact with one repo-relative path to a committed file). It does
not know which pass the owner holds open (pass 1 by the 2026-09-27 ruling, pass 2 by the plan approved 2026-10-01): you
are the gate. Then `/batch-done`. **`from-evidence` still faces its blocking gates:**
R17 (a logged search per admission), R1 (a Co-1/Co-2 search or source, or a reasoned `CO1-NOT-APPLICABLE` in a search's
`findings_note`) and R2 (`citation_mining` rows for admitted T1–T3 anchors). `scripts/audit/research_batch_dod.py
--session <STEM>` scopes R2 and R17 to this session's admissions; for a source admitted by an earlier session they
examine nothing here, so run `--all` (measured against the ratcheting baseline) to see them. Mine the anchors; R10
fetches leave WebFetch ledger lines that `search_log_completeness` reads.

## Resume and exceptions
Resume from live state, not memory: `/orient`; unadjudicated observations (`observed_terms` with no
`term_adjudications` row); `scripts/audit/scan_debt.py`; open follow-ups (`extraction_follow_ups` with `resolved_at`
NULL); parameters with extractions and no live specification (`specifications` with `retired_at IS NULL`; "best
practice" is the `v_best_practice` subset); terms adjudicated `NAMES-NEW` that are neither a parameter nor declined
(`term_adjudications` left-joined to `base_parameters` and to `parameter_declinations` where `revoked_at IS NULL`: a
revoked declination no longer declines the term). The scratch DB is disposable
and the canonical sha256 does not move until the migration applies, so a mid-batch failure costs only the unemitted
rows. A blocked source: Wayback, else admit UNVERIFIED with its `--processing-blocked-reason` (§3). A zero-yield search is
a completed unit of work. Finish: `scripts/preflight.sh` once, `run_checks.py --selftest` after any rename, commit
scratchpad and transcripts (rule 6), open the PR last and unsubscribe_pr_activity at once (rule 9); research rows
and tooling ship in separate PRs (rule 10).
