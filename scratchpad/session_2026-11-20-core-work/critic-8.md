# Critic pass on adjudication-8.md (read-only; DB user_version 164, HEAD 1ac3054, 2026-11-20)

Not run: no scratch-copy dry run of any verb (one-file write limit). Executability was tested by calling the
writers' own precondition functions against the live rows on a mode=ro connection, and by reading the verbs.

## Ranked findings (worst first)

### 1. BLOCKS - GAP-368: `add-extraction` refuses all 11 re-adds, and the retire comes first and is irreversible
Claim (s.5 Mechanism): "`retire-extraction` then `add-extraction` for the 11 rows ... existing verbs only".
Ran `db._covering_scan(con, ref, pid)` and `db._require_full_scan_for_verified` for rows 20 21 27 31 32 80 93 102 104 106 112:
- covering source_scans row: False for all 11 -> "add-extraction: no source_scans row covers REF.. for parameter 3" (db.py insert_extraction, "the reading record").
- rows 20 21 27 31 32 are `extraction_status='verified'`: a re-add as verified needs a FULL-scope reading (OR-11a); none exists. Re-adding as preliminary downgrades five verified figures.
- rows 31 32 (REF-00996, tier 5 >= REGULATORY_FROM_TIER 4) hold no loc_* pinpoint and no clause_id: R3 refuses a regulatory row without a structured locator.
- every live lens link on the 11 is basis `carried`, which `_require_lens_warrant` does not accept on a new write: each re-add needs a newly judged warrant, not a copy.
`retire-extraction` itself accepts all 11 (0 live determinations, no live edge leans on them), and a retired figure is never un-retired (trigger). So the stated order retires 11 figures and then cannot write their replacements until 9 sources are re-read and scanned (`record-scan`, a verb the resolution does not name and a reading it does not plan).

### 2. MUST-AMEND - GAP-368: "Every one has a current translation of its claim_text" is false for 102 and 112, and GAP-372 collides
`select translation_id,status,superseded_by_translation_id from translations where source_row_key in ('102','112') and source_column='claim_text'`
-> 102: (27 reviewed, superseded by 133), (133 REJECTED, current). 112: (37 reviewed -> 143), (143 REJECTED, current).
Both are on GAP-372's truncated-claim_text list. `claim_text` is in `_NOT_AMENDABLE_SVE` ("a different one is a SECOND ROW"), so GAP-372's repair is also retire + re-add of the same rows. The adjudication's Interactions and work order never mention GAP-372. Done as written, 102 and 112 are re-added with a truncated quote (a "literal span" of a cut-off sentence), then retired and re-added again.

### 3. MUST-AMEND - GAP-368: nothing stops English going into a qualitative `claimed_value` again
The resolution adds "one ledger convention". Ran `db._require_stated_numbers(claim_text, value, 'qualitative', None, ...)`:
- row 93 with 'a 1:12 ramp gradient is a safety risk' -> numbers OK (accepted)
- row 27 with 'mandatory standard insufficient for smooth use' -> numbers OK (accepted)
No code compares a qualitative value with its claim_text; `--value-as-written` is refused for a value with no number. `claimed_unit` is guarded on new writes (`dbcore.unit_refusal`); `claimed_value` is not. Owner ACTION (2) of 2026-11-20 stays enforced by nobody.
Also unaddressed: `v_determination_provenance` reads `claimed_value`; a Japanese span there has no translation pointer of its own (translations are keyed to claim_text), and s.7 does not make it owed.

### 4. MUST-AMEND - GAP-374: the test as named refuses 4 currently VERIFIED sources, is not "the stored title", and does not prove the bytes hold the source's text
Ran `_row_haystacks` + the title half of `_presence_missing` over all 51 VERIFIED sources:
- pass 47; no readable haystack 2 (REF-01000: nothing reached by `_presence_artefacts`; REF-01001: PDF bytes, no text extraction); title absent 2 (REF-01007, REF-01011). All four are DOI sources that `verify_corpus` sends down its JSON-byline branch, which the resolution does not name.
- the test asserts `_title_head` (text before the first separator), not the stored title. The FULL stored title is absent from the bytes for 14 of 51 (REF-00468 00977 00990 00991 00992 00995 00996 01007 01011 01012 01015 01017 01022 01032). This answers the report's own [GAP]: REF-00990/00991 pass only because the head is cut before the era-number tail. Heads that carry the proof include 'Building Regulations 2010' and 'Byggteknisk forskrift'.
- presence is per source over the union of its artefacts, so the 800-byte shell stays a usable manifest line; a landing page, abstract page or Crossref record contains a title and none of the source's text.
- `_refuse_unlogged_verified(ref_id, url, doi, verb)` receives no title and no authors; `_presence_missing` also fails on surnames.
- "It is the same test s.6 uses: one home" is false: s.6 names `_verbatim` -> `retrieval_log.quote_in_artefacts`, a different function with a different scope (finding 5).

### 5. MUST-AMEND - GAP-371: the occurs-in-bytes test cannot choose a title, accepts other sources' bytes, and reverses a recorded design decision
- `quote_in_artefacts(q, ref_id='REF-00994')` returns found for 'Accessibility Guide', for 'IPC Accessibility Guide' and for 'Key Measurement Reference Table'. Any phrase of the document passes as its title.
- its docstring: "A hit in some other source's payload is still returned as found ... UNSCOPED". `_verbatim` returns `kind != 'missing'`, so a title found only in another source's artefact (a citing paper's reference list) passes.
- the cover text is in no text artefact: page 1 of the extraction is blank, the cover is a PNG, and no transcription is logged for REF-00994. In the text 'ACCESSIBILITY GUIDE' occurs only inside "STRUCTURE AND CONTENT OF THE IPC / ACCESSIBILITY GUIDE" (line 559) and "IPC Accessibility Guide" running text. The bytes the test reads say "IPC Accessibility Guide".
- a transcription "by eye" (manifest line 21, REF-01005) is model-typed text then read back as logged bytes: the writer verifying itself.
- `correct_source` docstring: "There is deliberately no way to pass a value ... A `--title` flag here would rebuild that hole one level up" (REF-00973's title bent toward its slug). The resolution adds the value argument. It also refuses a DOI-less source, and REF-00994 has no DOI; `corporate_name` is not a column of evidence_sources at all.
- Interaction 3 says correcting REF-00994 "removes the red that author_fidelity shows on main". `python3 scripts/research/retrieval_log.py --verify-authors --all-sessions` exits 0 today (REF-00994 is UNVERIFIED and only reported). The gap text was trusted over the command.

### 6. MUST-AMEND - GAP-373: owed set by first request; existing column ignored; source_section mis-sorted
- `_open_translation_request` refuses no column. One request on `observed_terms.surface_form`, a `loc_*` or `notes` opens that whole column as owed; `translations` is append-only, so it never closes. The adjudicator's Owed / Not-owed list is a judgment recorded nowhere the machine reads (CLAUDE.md rule 8: derive it, or name who judged it). The live pairs are only (evidence_sources, pub_title) and (source_value_extractions, claim_text).
- `evidence_source_authors` already has `corporate_name_en` and `corporate_name_note` (NULL on all 23 non-English corporate rows). s.7 sends the English to `translations` without mentioning the column that names that fact.
- 'Republic of Korea' (REF-01019/01031) and 'Portugal' (REF-01026) are English-only glosses; REF-01019's own notes say the issuing ministry is not stated in the retrieved text. No as-written name exists for an occurs-in-bytes correction to find.
- `source_section` fails the report's own test ("the source's own words") on the rows sampled: 'Letter p. 1, third bullet', 'Guide p. 12, commentary beside the arr...', 'Yttrande, punkt 3:1222 (PDF pp. 2-3)'. `_cell_language` returns the source's language, so all 80 live non-English rows become owed, the English ones included.
- FK hop: `extraction_relations` has TWO FKs to source_value_extractions (from, to). 0 cross-source edges today (`cross_source_reason` exists as a parameter), so which hop gives the quote's language is unproven, not clean.
- "its English is the adjudicated term": 4 of 33 non-English observed_terms have no term_adjudications row.
- The "circular" claim is overstated (see notes).

### 7. MUST-AMEND (owner's) - T-145 Q1: three NOT NULL keys
- "nullable keys ... break UNIQUE ... duplicates land": falsified by the live schema. `ux_extraction_lens_live` is a UNIQUE index over `COALESCE(identity_code,'')`, `COALESCE(icf_code,'')`, `COALESCE(needs_code,'')`.
- "D-0182 governs a different object and does not bind here" is asserted, not shown. The 2026-08-28 ruling's CONDITION reads "Any session designing a table after the base phase, or attaching ..."; D-0182's words are general ("it is OKAY for a link to be absent in a related taxonomy column", "but a link MUST be tied to at least one", "and ideally it ties into many"). The same ruling says the base crossing maps are "pairwise by nature". Which side T-145's table falls on is not examined. This is an interpretation of the owner's words (condition (c)) used to set aside a ruling (condition (e)).
- The task's own reason for "at least two" was two facts; the report answers one. Recomputed: 11 of 23 active identities have no ICF code; the two maps share 2 ICF codes (identities map to d-codes, needs to e-codes). A row holds one icf_code, so most identity-need pairs have no single code both maps hold.
- "Knowledge of only two coordinates is a gaps row": `gaps` has the three FK columns (13 of 384 rows use one) but no warrant, state or review. A judged identity-need pair cannot become `stated` there.
- Held for the report: the owner's "3D matrix" and the confirmed description's "judged triples: identity, need and ICF code" do support three coordinates.
- T-145 section 2 requires the four answers "in the ledger in the owner's words" and section 9 says stop otherwise; the task recommended the opposite answer. `decision-protocol.md` 2.4 item 2 (population taxonomy structure) is always DG-NON.

### 8. MUST-AMEND - T-145 Q2 and Q4 are labelled "ALREADY ANSWERED by the owner" on an unratified [ASSUMPTION]
Ledger ACTION (4) of the second 2026-11-20 statement: "Treat the two assumptions above as unratified except where the owner's words state them." The owner's words are the matrix sentence and "yes, correct". "each with a warrant" and the not_applicable reading are the coordinator's wording. Transcript `transcripts/harness_12490a0b/main.jsonl`: "yes, correct" arrived at 05:47:31, 18 s after the description, which closed on one question (propose and review per batch). Q4 rests on nothing else. The precedent column `specifications.not_applicable_rationale` exists.

### 9. MUST-AMEND - the authority sentence cites a grant that does not reach these decisions
Header: "Under the delegation of 2026-11-12 ('I guess opus can do it')". That grant named twenty decisions by number, OD-01 to OD-30. `sed -n 6296p references/project-standards.md` records this same misattribution as defect C0 of an earlier pass and corrects it. What reaches today's items is the owner's question of 21:19 in `transcripts/harness_de695d5a/main.jsonl` ("How many of these blockers and gaps can be actively resolved right now by having Opus carefully adjudicate ...") and 21:37 ("Once we resolve the decision ..."). Neither is in the ledger (`grep -c -F "blockers and gaps" references/project-standards.md`), and the first is a question.

### 10. MUST-AMEND - GAP-376 / GAP-368: retired figures' translations stay on the owner's reading surface
`translations_shown()` (db.py) selects `status='reviewed' AND superseded_by_translation_id IS NULL` with no retired-figure filter. After the retirements, translations 197 198 207 208 209 (figures 82 83 95 96 97) are still printed by `db.py translations --show` beside 107-111's, so each clause still shows twice; the same for the 11 GAP-368 rows. `translations_due` has the filter; `translations_shown` does not.

### Notes
- N1. s.5 "The English conditions ... already live in claim_text and its translation" is false for rows 72 and 73: the unit cell says "% of all 90 audited buildings (NOT of the ~43 with a ramp ...) (n=27/90)", the claim_text says "destas 30,0%" (of these). 32 live non-English rows have whitespace in claimed_unit; a `base_units` spelling leads 31 of them (row 80 is the exception), so the amend path works where a live determination does not block it (0 live specifications).
- N2. Interaction 5 "circular for extraction_relations.quote": `claim_text` is a judgment-stage cell too (CLAUDE.md s.3 table), and the owner's ACTION already reads "before judgment reads it". `translations_due` lists; it refuses nothing. Not unsatisfiable.
- N3. s.3 command `git grep -l absorbs -- 'scripts/migrations/data_*'` returns one file, a gaps-filing migration that mentions the word. `access_needs` rows are INSERTed by `057_baseline_2026-08-12.sql`, a schema migration. The command does not measure what the sentence says.
- N4. "Convention: a mirror found beside its official text is superseded at admission" is held by no code. The precedent shows the limit: REF-01019 has been superseded since 2026-10-02 and its figures 82 and 83 are still live. D-0168 is registered DG-NON; s.5 sets what a column of the D-0168 item holds.

## What survived
- Row 80: `_require_stated_numbers(text, '5', 'numerical', 'viisi prosenttia')` passes and refuses without the wording; `figure_refusal('5','%')` is None; owner ruling 2026-11-12 (ledger lines 5337-5350) orders exactly this.
- `retire-extraction` accepts 20 21 27 31 32 80 93 102 104 106 112 and, in the stated order, 83 97 then 82 96 95: links only to RETIRED specifications 3-8, 0 live specifications, edges 39 (83->82) and 41 (97->96) only.
- `supersede-source` exists (parser and dispatch) and by its code accepts REF-01026 -> REF-01032: neither is superseded, no live determination rests on REF-01026.
- Mirror and official payloads: every mirror figure's quote occurs, normalised, in both text extractions (5744dca7 / 5b800bfb; 7952f862 / b71c64f1); value and unit cells equal pairwise; both Korean texts carry only the 2023-12-11 stamp.
- Keeping both rows: `identifier_floor_audit.py` CLEAN (EXAMINED 3 floors, 269 files); no DOI on either pair, so R9 is not engaged.
- `v_live_lens_links` joins `x.retired_at IS NULL`: a retired figure's links drop (the report's [GAP]).
- GAP-371 facts: the cover PNG reads ACCESSIBILITY GUIDE / OCTOBER 2020 / INTERNATIONAL PARALYMPIC COMMITTEE; `grep -c -i edition` prints 0.
- GAP-374 facts: title stem 6 times in a4390f9b.xml, 0 in d984761f.html; 800 bytes; two manifest lines, one sha.
- T-145 figures: 11 of 23, 61 and 43 map rows, 2 shared codes; `gaps` carries the three lens columns; `absorbs` is read at db.py `_lens_...` (line 11495).
- `dbcore.single_key('evidence_source_authors')` = `id` (the report's [GAP]); contract `translation: default_stage: judgment`.
