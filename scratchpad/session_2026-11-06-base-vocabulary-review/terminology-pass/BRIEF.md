# Terminology research pass: shared brief

You run ONE terminology pass for the Accessible Built Environments Guidebook (`/home/user/guidebook`) for the language-and-jurisdiction pair your instruction names. It is part of a wave over the P1+P2+P3 languages. Pilot passes already exist (`terminology-pass/FR-FR/`, and DE-DE and JA-JP if finished); read `FR-FR/pass-record.md` and look at its `build.py`, which you may copy and adapt as your verifier.

Read `CLAUDE.md` first (rules 0, 5, 7a, 8, 10; section 5 failure modes; section 7 traps incl. the Wayback route), and the three entries headed "Owner statements 2026-11-06" and the fourth in `references/project-standards.md`.

## What this is and is not
- The English register is the SEARCH PLAN, not the vocabulary, and it is Canadian English from one rating instrument (RHFAC), digested in `rhfac-b651-catalogue.md` (sections 2 to 6), `rhfac-criteria.tsv` (640 criteria) and `b651-headings.tsv` (the CSA/ASC B651:23 clause structure). It is a guideline, not definitive.
- Rendering the register into your language produces FLAGGED, MODEL-GENERATED SEARCH SEEDS (owner OR-12b: terms you believe are IN USE in that jurisdiction, never word for word). Seeds point the reading and are never findings, never aliases, never vocabulary.
- A FINDING is a phrase VERBATIM in a retrieved text of that jurisdiction in its own language, with locator and a quote that verifies in the saved bytes.
- The register must not end where English ends: read the instrument IN FULL in its own language and record every design quantity, element, technique and defined category it treats, including ones the register lacks (reverse harvest; owner E1: a concept first met outside English is named by the instrument's own phrase, never an English gloss).
- Terminology only: do not extract values as findings.

## Concept list
Use the 32 concepts recurring in three or more sections (catalogue 2.1), the quantity-bearing words (2.2), the base's active parameters (`select p.parameter_id, t.canonical_en from base_parameters p join terms t using(term_id)`), and the B651 clause headings that RHFAC does not name (`b651-headings.tsv`, last column). Existing aliases in your language (`select alias, alias_type, jurisdiction, notes from term_aliases where lower(language)='<code>'`) are MODEL-GENERATED SEEDS, never findings.

## Lessons from the French pilot (apply them)
1. A text match is not a sense match. Record FOUND only where the instrument uses the phrase in the register concept's sense; say so in the note. "inclinaison" appearing in an unrelated sense is not a finding.
2. The register is criterion-shaped: near-duplicate rows share observations. Count distinct phrases as well as observations, and do not let near-duplicates inflate FOUND.
3. The instrument may split or merge concepts differently (the French fixed ramp is a different word from "rampe"; its corridor is not "couloir"). Record the carve difference; do not force a one-to-one map.
4. The drafting structure itself may differ (aim then prescription, defined categories, equivalent-effect routes). Note it in the pass record.
5. Held aliases that are word-for-word translations and occur in no instrument should be reported as such.
6. Instrument lists cannot be derived from the base for most pairs. Say how you built yours and what you could not derive.

## Procedure
1. **Instruments.** Primary accessibility instruments for buildings in force, current editions only, free official texts first (the national law and regulation portal, the building authority's published code). Derive candidates from `research_code_leads`, `references/standards-registry.md` and `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='<J>'`, then search. A paywalled standard you cannot retrieve is NOT-OBTAINABLE: log the attempt; do not substitute memory of its content.
2. **Retrieve and persist** from the repository ROOT (retrieval_log writes relative to cwd; running it elsewhere misplaces artefacts):
   `cd /home/user/guidebook && python3 - <<'PY'` / `import sys; sys.path.insert(0,'scripts/research'); import retrieval_log as r; r.fetch(URL, session='session_2026-11-06-base-vocabulary-review', purpose='terminology pass <PAIR>: <what>')` / `PY`.
   fetch() returns None for non-JSON but persists the bytes and a manifest line under `retrieval-log/session_2026-11-06-base-vocabulary-review/`. A publisher block or a JavaScript shell: use the Wayback `if_` route (CLAUDE.md section 7), as the French pass did for Légifrance. Extract text with `pdftotext -layout` or by stripping tags; save the text to `terminology-pass/<PAIR>/text/<artefact-sha-prefix>.txt` and record its sha256. Never disable TLS verification or unset the proxy. The owner has ruled that retrieved standards may be held in the repository.
3. **Read each retrieved instrument in full**, in its own language. Locate with scripts, read the located passages yourself, and record honestly what you read and what you did not [SKIPPED: part, why]. Image-only diagrams are unread.
4. **Record** under `scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/<PAIR>/` (PAIR like `DA-DK`):
   - `search-log.md`: every query verbatim, a prior expectation written BEFORE the result, the result, and a note on query shape (R14). Keep empties.
   - `instruments.tsv`: title as written, issuing body, edition in force, URL, sha256 of retrieved bytes, retrieval status, read in full yes/no/partly with what was skipped.
   - `observations.tsv`: concept (register label or REVERSE-HARVEST), phrase VERBATIM, language, instrument, locator, context quote verbatim, text file, quote_verified_in_text, note (ours).
   - `coverage.tsv`: one row per register concept: FOUND / FOUND-PARTIAL / SEARCHED-ABSENT (instrument read in full, concept not treated) / NOT-OBTAINABLE / NOT-READ, with a note.
   - `reverse-harvest.tsv`: what the instrument treats that no register row names, in its own phrase; any gloss clearly marked as ours.
   - `seeds.tsv`: model-generated seeds for register concepts NOT found, flagged MODEL-GENERATED, with the jurisdiction they are meant to be in use in. Short.
   - `build.py` (adapted from the French pass) that regenerates the TSVs and exits 1 on any quote not found verbatim in the saved text.
   - `pass-record.md` (verdict first, at most 80 lines): retrieved and read, not read and why, counts by script (command beside each), where this language's instrument carves the field differently from English, method defects, and a self-attack of the five likeliest ways the record is wrong.
5. **Hard prohibitions.** Do not write `data/guidebook.db` or run any `db.py` write verb or migration. Do not commit or push. Do not edit `CLAUDE.md` or any file outside your `terminology-pass/<PAIR>/` folder and `retrieval-log/session_2026-11-06-base-vocabulary-review/`. Invent no citation, article number, URL or quotation; every locator and quote must come from bytes you retrieved. Use no pre-reset item codes (a letter, a hyphen, two digits). Do not use the French RHFAC edition. Canadian English in your own prose; objective tone, no flattery.

Budget: depth on the one or two principal instruments over breadth. Stop when they are read in full and recorded, or when an unavoidable block is logged. Reply in at most 12 lines: verdict, instruments read in full vs not, counts (FOUND / FOUND-PARTIAL / ABSENT / REVERSE-HARVEST), the two most surprising carve differences with English, method defects, and the folder path.
