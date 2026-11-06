# Base-table population plan: a multilingual, multijurisdictional base without an English pivot

Session `session_2026-11-06-base-vocabulary-review`. **A proposal; it approves nothing and writes no rows** (owner statement
2026-11-06, item 5). Planner: `opus/150/synth`. Every figure carries the label of the command in the appendix that derives
it, with its 2026-11-06 result; **re-run the appendix (`python3 <appendix script>` from the repository root) rather than
trust any figure here** (CLAUDE.md rule 7a). Rulings are cited by their ledger heading in `references/project-standards.md`,
not restated.

## 0. Verdict

The base cannot yet be made free of English bias by adding rows, because three mechanisms put English in the pivot:
`terms.canonical_en` is NOT NULL while OR-17 forbids the model to coin a name, so a concept first met in a non-English source
cannot become a term without an invented English name (it has already happened twice, D8); an alias's provenance is a substring
of a free-text `notes` field, and no route can promote an existing model-generated alias by attesting it (D5, D6); and the
other base vocabularies have no home for a label in any language but English. Fix those three in one small tooling PR, then
populate in this order: the screened item-subject catalogue (fast, English, explicitly a seed), then native-language open passes
over each P1-3 jurisdiction's own instruments, interleaved so every language-jurisdiction pair gets its first full reading before
any gets a second. **The one thing that most reduces the chance of missing a quantity is the open pass, in the instrument's own
language, over the full text of each P1-3 jurisdiction's primary accessibility instrument, run to a derived fixed point** (section C.3).
No scan has done an open pass yet: D14 → 9 scans, 0 open passes, 0 full-reads (2026-11-06).

## A. Diagnosis check

Ranked by what wrong thing reaches the guidebook if left. "Brief" means the base review (`base-review.md`) or the orchestrator's
commission.

| # | Defect | Verdict on the brief | Evidence (appendix label → 2026-11-06 result) | What reaches the book if left |
|---|---|---|---|---|
| A1 | Parameter list is thin | **Confirmed.** | D1 → 10 active; D2 → 94 terms, 1 declined | Silence on quantities nobody listed: the book misses stairs, handrails, controls and the rest, and nothing says so |
| A2 | English pivot in term origin | **Confirmed, and sharper than stated.** The schema requires an English name (`terms.canonical_en NOT NULL`, `PRAGMA table_info(terms)`); `insert_term` never checks the name against the observed phrase (`grep -n 'def insert_term' scripts/db.py`); OR-17 ("It is not acceptable for the model to generate its own phrases/names/aliases", ledger "Owner rulings 2026-10-29 (third)") forbids the only way to satisfy it. Already violated: two terms minted from Dutch observations carry English names no source used, and their Dutch origin phrases are not aliases at all | D8 → TERM-090 from NL *niveauverschillen*, TERM-092 from NL *tussenbordes*, both with typed English names; D9 → 4 NAMES-NEW terms whose name is not inside the observed phrase | Model-coined English labels presented as concepts; concepts that exist only in a non-English instrument are unrecordable, so the book is structurally limited to what English already names |
| A3 | Alias layer nominal | **Confirmed, with corrections.** The counts reproduce (`python3 scripts/audit/alias_provenance_audit.py`: 2382 aliases; 15 verified, all ID; 1163 model-generated; 880 UNKNOWN; 304 curated EN). Missed: (a) provenance is a substring of `notes`, so the blocking gate passes any row whose free text contains a marker (D5); (b) `add-alias` has never run (D6 → 0) although 45 NAMES-EXISTING adjudications exist (D7); (c) `add-alias` refuses an alias already held in that language (`grep -n 'def add_alias' scripts/db.py`), so a model-generated alias can never be promoted by attesting it; (d) 996 rows are typed `TRANSLATION` (D10), which frames every non-English name as a rendering of the English one, the R11 inversion; (e) two alias jurisdictions are not jurisdictions (D23, reported by `jurisdiction_db_vocabulary`) | D4 → 2133 NULL jurisdiction | Searches run on model guesses presented as vocabulary; "native term" claims the database cannot support |
| A4 | ICF English-only and thin | **Confirmed; the titled rows are worse than stated.** None of the 29 titles came from WHO bytes: 17 cite a skill file deleted on 2026-10-14 (`ls skills/functional-deficit-auditor_SKILL.md` fails; `git log --diff-filter=D -- skills/functional-deficit-auditor_SKILL.md`), 12 cite repository prose (D11). `set-icf-title` refuses to overwrite, so there is no correction route. Chapters e4, e5 and d8 are absent (D12) | D11, D12 | ICF titles from memory laundered through repository files: CLAUDE.md 5(c) on a classification |
| A5 | Identity, need, room, medical labels English-only | **Confirmed, and the documented route does not exist.** `governance/functional-taxonomy.md` ("Naming", `grep -n 'Person-first' governance/functional-taxonomy.md`) defers native-language conventions to `term_aliases`, but `term_aliases.term_id` references `terms` only; identity, need, room and medical codes are not terms | `PRAGMA foreign_key_list(term_aliases)` | Identity-first or person-first conventions of each language community cannot be recorded; any non-English rendering would be a translation of English prose |
| A6 | (missed) The language half of a bucket member cannot be derived for a source | **New.** `evidence_sources.language` is NULL on every row; `lang_detected` mixes case and is NULL on 8 (D13). OR-8 makes a bucket member a jurisdiction-and-language pair, so coverage per pair is not computable. The bucket table itself (T-6b steps 4-5, `workplan/2026-10-23-pipeline-resolution-workplan.md`) is not built | D13; `grep -n 'T-6b' workplan/2026-10-23-pipeline-resolution-workplan.md` | A "covered" pair read only in English (e.g. a Swiss instrument read in one of its languages) |
| A7 | (missed) No open pass, all scans pre-screen | **New.** | D14 → 9 / 0 / 0; `python3 scripts/audit/scan_debt.py` → DEBT 477 pairs | Every quantity outside the 10 is unread in every held source |
| A8 | (missed) Prose callers contradict the database | **New.** `references/native-alias-verification.md` and `references/methodology-native-alias-verification.md` carry hand-typed counts, call search-time acceptance "CLEAN … verified", and use "P1/P2" for language priority, which collides with the P1-3 jurisdiction scope. `skills/multilingual-research_SKILL.md` hard-codes 19 languages × 46 jurisdictions with numeric floors and "Synthesises findings in English" (`grep -n '46 jurisdictions' skills/multilingual-research_SKILL.md`), against OR-12a and the P1-3 scope. `scripts/generate_alias_chart.py`, named in the commission, does not exist | the greps shown | A session follows the prose, not the database (CLAUDE.md 5(b)) |
| A9 | Mixed kinds in `terms` | **Confirmed.** Lens terms (17 `functional_axis`), methods (14), medical (8), economics, legal and population terms sit beside quantities (D18). The 2026-10-09 seed ruling made "the terms registry" the seed; read literally, every row is a parameter candidate | D18 | Elements and lens terms minted as parameters, or the scan contract measured against terms that can never hold a value, inflating scan debt |
| A10 | Medical lens empty | **Confirmed, with two corrections.** `medical_lens_integrity` is **advisory**, not blocking (`python3 scripts/run_checks.py --list \| grep medical`). The binding ruling is the ledger entry "CORRECTION, same day — 'demand-populated' re-instated a position the owner had overruled" (2026-09-11): populate by correspondence from the identity registry and functional axes first, at block grain, then on demand. The empty table is an unexecuted ruling, not a deferral | D21 → 0/0/0; both crossing maps appear in the UNWRITABLE set (CLAUDE.md section 4 script) until a medical row exists; `add-medical` writes row and crossing together, so this is not a trap | A reader arriving with a diagnosis has no route in |
| A11 | Rooms uncategorised | **Confirmed, and rooms have no reader.** No foreign key points at `rooms` and no script queries it (D19; `git grep -n 'FROM rooms\|JOIN rooms' -- scripts ':!scripts/migrations'` → nothing). Two rows read as near-duplicates (circulation corridor versus hallway) | D19 | Low: nothing renders it. Populating it before a reader exists is apparatus (CLAUDE.md section 8) |
| A12 | (missed) Stakes unassigned and vocabulary held twice | **New.** 16 of 17 needs lack `typical_stakes` (D20); `access_stakes` is a table holding the same three values as the CHECK on `access_needs.typical_stakes`, with no foreign key (rule 8) | D20; `PRAGMA foreign_key_list(access_needs)` | Low until determinations weigh stakes |
| A13 | Direction coverage | **Confirmed.** | D3 → 2 of 10 | The most-accommodating rule (OR-4) cannot pick for 8 parameters |
| A14 | (missed) Language varieties and in-scope official languages | **New, partly DG-NON.** `lang_jur_map` uses one code for Norwegian (no Bokmål/Nynorsk split) and one for Chinese (no script); AT is mapped but not in `schemas/enums.py`; official languages of P1-3 jurisdictions outside the 14 are absent. D15 → 39 P1-3 pairs over 14 languages | D15; `python3 scripts/audit/jurisdiction_db_vocabulary.py` | Two written standards of one language conflated; jurisdictions whose instrument exists in a language the map lacks are read in none |
| A15 | (missed) Three P1-3 jurisdictions have nothing to read | **New.** No code lead and no held instrument for DK, IT, CN (D16) | D16 | Their quantities can only arrive through other jurisdictions' framing |
| A16 | Slug topic gaps | **Confirmed, low.** The 2026-10-09 scan contract makes slugs plan searches only; they do not bound vocabulary | base review table, `slugs` row | Only search planning |
| A17 | (missed) Stage assignment: an alias copies an evidence-stage fact | **New.** A source-attested alias stores the observation's surface form and points back only in prose (`notes`). Under CLAUDE.md section 3 the phrase belongs to evidence (`observed_terms`); the base row should point, not copy (rule 5) | `PRAGMA table_info(term_aliases)` | The alias and its observation drift apart, and only the alias is read |

**The canonical_en question, answered.** True as stated, and OR-17 turns it from a bias into a contradiction: the schema
demands an English string for every concept, and the rulings forbid the model to supply one that no source used. What follows is
design question B.1. A rename or drop is ruled out: six committed data migrations name the column
(`grep -l canonical_en scripts/migrations/data_*`) and two INSERT into `terms` (`grep -l 'INSERT INTO "terms"' scripts/migrations/*`),
so the column can never be dropped (rule 5), and readers are numerous
(`grep -c canonical_en scripts/db.py`; `grep -rln canonical_en scripts --include=*.py`).

**One correction to the 2026-11-06 ledger entry.** Its item 3 says admitting the item subjects is "a schema change plus a
resolver". No schema change is needed: `terms.catalogue`'s CHECK already admits `_archived/data/corpus-pre-reset-2026-08-06.db`
(`PRAGMA table_info(terms)` / `select sql from sqlite_master where name='terms'`); only `_resolve_catalogue_entry` refuses
anything but `terms:<TERM-ID>`. The session should record that correction in the ledger (rule 0's record-keeping; no owner
decision needed).

## B. Population design, per table

Principles applied to every row of the table below:

- **No row in language X is derived from a row in English.** Every non-English label or alias points at an in-language
  artefact (an observation whose quote verifies in a saved file, or a persisted payload). English is one language among 14
  and gets the same pointer requirement for its jurisdiction variants.
- **Language and jurisdiction are read, not typed** (rule 8): from the observation and its source, as `add-alias` already does.
- **No language CHECK is added.** The language vocabulary is `lang_jur_map`, so a language admitted later is a row, not a migration.

| Table | Target end-state | Single source of truth | Derived, not curated | Pointer | Writer (existing verb, or gap) |
|---|---|---|---|---|---|
| `terms` | Every concept any P1-3 instrument treats as a design quantity, element, method or setting, each with provenance: an origin observation (NAMES-NEW) or an approved catalogue entry | the origin observation, or the catalogue entry plus approval heading | The label's language: from the origin observation; `en` for a catalogue mint | `term_adjudications` → `observed_terms` → `evidence_sources` | `add-term --from-observation`; `mint-term-from-catalogue`. **Gap T2:** bind the name to the observed phrase |
| `base_parameters` | Every term that names a quantity under determination; every other term declined with a reason | `terms` + the promotion or declination | Nothing curated; status from verbs | `term_id` (UNIQUE) | `add-parameter`, `decline-parameter`, `merge-parameter`, `set-parameter-direction` |
| `term_aliases` | For each term and each P1-3 pair: the phrase that jurisdiction's own instrument uses, attested; model-generated rows held as flagged search aids only | `observed_terms` row (phrase, language, locator, quote) | alias text, language, jurisdiction: read from the observation and source | **Gap T3:** a nullable `observation_id` foreign key | `add-alias`; **gap T3:** attach a pointer to an already-held alias instead of refusing |
| `base_icf` | Every code a held need, identity or parameter crosses to, plus chapters d4, d5, e1, e2, e3, e4, e5 as a completeness frame; English title from WHO bytes | persisted WHO payload | title verified as a substring of the payload | `title_source = payload:<file>` | `add-icf-code`, `set-icf-title --title-payload`; **gap T4:** replace a non-payload title with a payload-verified one, recording the old |
| Labels in other languages (ICF titles, identity, need, room, medical display names) | One label per code per language (and per jurisdiction where usage differs), each pointing at its in-language artefact | the artefact | language, jurisdiction from the artefact | **Proposed T5:** one table, five nullable foreign keys (identity, need, ICF, medical, room), CHECK exactly one, mirroring the ruled four-lens-column shape (ledger, 2026-08-28 lens ruling as amended by D-0182) | none today; T5 waits on owner decisions E5, E6, E8 |
| `base_taxonomy_identity` | Unchanged (DG-NON). Labels per language through T5 | owner rulings | — | — | none, deliberately |
| `access_needs` / `access_need_icf` | Stakes assigned with warrant; ICF crossings `confirmed` only against WHO bytes | owner-approved table for stakes | stakes vocabulary from the column CHECK; retire `access_stakes` if nothing reads it (§8) | `access_need_icf` | **[GAP]** no verb found for `typical_stakes`; confirm with `grep -n 'typical_stakes' scripts/db.py` before planning one |
| `base_taxonomy_medical` + maps | The correspondence set the 2026-09-11 correction bounds, then on demand | WHO ICD-11 release file, persisted | anchors verified from bytes (`icd11_verified_at`) | crossings to identity and ICF | `add-medical --icd11-payload` |
| `rooms` | Frozen until a reader exists (E8) | — | — | none points at it | none needed |
| `lang_jur_map` | The 39 P1-3 pairs (D15) approved as bucket members; varieties per E7 | owner approval per row (T-6b) | — | bucket table points at pairs (OR-8) | T-6b, already ruled; not new here |

### B.1 How a concept that originates in a non-English source becomes a term

| Option | What it does | For | Against |
|---|---|---|---|
| **A (recommended).** The term's label is the source's own phrase, in its own language; `canonical_en` holds it verbatim; the label's language is derived from the NAMES-NEW observation | No schema change. `add-term` gains one refusal: the name must occur, case-folded, in the observation's `surface_form` (T2). An English name is added only when an English-language instrument of a P1-3 jurisdiction is observed naming the same concept; then `rename-term --from-observation` | Satisfies OR-17 and R11 at once; English loses its privilege; the reader sees the concept as the instrument names it | The column name lies; every reader that renders `canonical_en` must show the label's language. `rename-term` turns the old name into a DEPRECATED alias, which is wrong for a native label: T2 must make it a live SYNONYM in its own language instead |
| B. Rebuild `terms` with `canonical_en` nullable, plus a derived per-language label view | Honest column semantics | Clean model | A table rebuild against every reader (`grep -c canonical_en scripts/db.py`) and the views that name it; net code grows; no ruling needs it yet |
| C. A typed English gloss | — | — | Forbidden by OR-17; listed only to reject |

The definition and scope note may describe the concept in English prose, because prose is ours (the 2026-09-11 reasoning,
"identifiers are facts while prose is ours"); a name may not be invented. Remediation of D8 and D9: flag the four terms now; correct
each in a data PR by `rename-term` to the observed phrase, on the owner's word for the parameter among them (TERM-091 is parameter 12).

### B.2 Native term versus translation

- **Rule.** An attested alias is a phrase a jurisdiction's own instrument uses, observed in that instrument in its own language.
  It is typed SYNONYM, NARROWER or BROADER, never TRANSLATION (T3 refuses TRANSLATION on an attested alias). An officially
  published English version of a non-English instrument is a translation: its phrases are observed with the language they appear
  in, but they attest the English-language usage of nobody's jurisdiction and are excluded from `add-alias` for an EN alias unless
  the instrument is authoritative in English in that jurisdiction (T3 refuses where the alias language is not paired with the
  source's jurisdiction in `lang_jur_map`).
- **Jurisdiction tagging** is the source's jurisdiction, read by `add-alias`. That already separates DE/AT/CH German, FR/BE/CH/CA
  French, NL/BE Dutch, PT usage, and US/UK/AU/CA/IE/NZ/SG English. It does not separate two written standards inside one
  jurisdiction (Norwegian Bokmål and Nynorsk) or scripts (Chinese), which is E7.
- **Legal designations** (a JA, KO or ZH statutory term of art) are terms in their own right under B.1, not aliases of an English
  concept, wherever the instrument defines them.

### B.3 Verifying the 880 unrecorded and 1163 model-generated aliases

Status meanwhile: **usable only as flagged search aids** (OR-12b), **never vocabulary** (OR-17), pending the owner's OR-17b (E4).
The route is not a separate glossary-verification protocol but the ordinary evidence path, which removes the need for
`VERIFIED-GLOSSARY` as a hand marker (rule 8):

1. Per language, the glossary is the P1-3 instrument's own definitions clause, or a national standards body's terminology
   standard, admitted as a source (`add-source`), its text persisted with `scripts/research/retrieval_log.py` `fetch()` and
   registered with `scripts/research/full_text.py`. Wayback `if_` fallback per CLAUDE.md section 7 for a block.
2. Each phrase found is `observe-term`'d with locator and verbatim quote, `adjudicate-term`'d NAMES-EXISTING, then `add-alias`.
   With T3, a held model-generated alias whose text matches gains the pointer in place and becomes attested; an attested phrase
   not held becomes a new row.
3. A model-generated alias the instrument contradicts, or never uses after a full open pass of that pair, stays flagged; whether it
   is deleted is E4. No alias is ever generated to fill a gap (OR-17).

Order: one language at a time, the instrument with the largest definitions section first. `alias_provenance_audit` reports
progress per language; it must classify from the pointer (T3), or it measures text, not attestation.

### B.4 ICF and ICD-11 titles in each language

- **English titles first**, from a WHO ICF payload persisted under `retrieval-log/`, through `set-icf-title --title-payload`; T4
  replaces the 29 non-payload titles. Before T4 ships, confirm the payload check anchors the title to its code, not just anywhere in
  the file ([GAP]: `set_icf_title` tests `title in body`, a substring match a neighbouring code's title can satisfy).
- **Other languages** go to the T5 label table, each label pointing at a persisted WHO or national-body payload in that language.
  Which of the 14 languages WHO or national bodies publish for ICF and for ICD-11 is **[UNVERIFIED]**; measure by retrieval, never
  by recollection. The ICD-11 English release file is already held (`ls retrieval-log/session_2026-09-11-medical-lens-icd11`).
- **Is a translation table a second home?** No, if it holds only non-derivable facts: WHO's published title in language X is a
  different fact from its English title, keyed on the same code (a pointer, rule 5). It becomes a second home if it also holds the
  English title already in `base_icf.title`; T5 therefore refuses an English row for a code that `base_icf` titles. Whether the
  titles may be stored verbatim under the guidebook's licence is E5 (DG-NON, licensing).

### B.5 Identity, access-need, room and stakes labels

- Identity codes and English display names are untouched (DG-NON). A label in language X is the community's own designation,
  attested in an in-language Co-1 source of a P1-3 jurisdiction, never a translation of the English display name. Where communities
  in one language differ (identity-first versus person-first), the label carries its jurisdiction; where no attestation exists the
  code has no label in X and the gap is visible. Mechanism and certifier are E6.
- Need labels and medical display names are our prose; a non-English rendering is a translation of our prose, which R11 does not
  forbid for prose but must be marked as ours. Defer until a reader in that language exists (no render work is in scope).
- Rooms: frozen (E8). Stakes: one owner-approved table (E9).

### B.6 The medical lens

Populate, in this order: (1) the correspondence set under the 2026-09-11 CORRECTION entry, from the identity registry and the
functional-axis terms, excluding the identity-first and umbrella codes that entry and `governance/functional-taxonomy.md` name;
anchor on the block whose title states the presentation; every anchor verified against the persisted release file through
`add-medical --icd11-payload`; (2) then on demand from admitted sources. Leave empty: entity-level codes, any chapter mirror, and
any row whose anchor cannot be verified from bytes (`icd11_verified_at` stays NULL and the row is not written). Medical display
names are our prose (the `insert_medical` docstring). This is Opus-class judgment (pruning the derived join, per the 2026-09-11
ruling) and its own research PR.

## C. Route to a comprehensive parameter list

### C.1 The screened catalogue of item subjects (route i)

A read-only subcommand (T1) prints one table for the owner. It never writes the database. Per row:

| Column | Filled by | Rule |
|---|---|---|
| pointer | machine | `items:<rowid>` into the pre-reset database; the old code is not shown (the 2026-11-06 ruling: "with their codes removed") |
| stripped name | machine | parentheticals and bracketed text removed; then `_VALUE_BEARING` and `_ITEM_CODE` re-tested (imported, not retyped) |
| still value-bearing | machine | D22 → 2 of 93 after stripping (2026-11-06) |
| prescription-bearing | judgment | condition clauses the regex cannot see (DR-2026-08-19 section 1.1 counted names carrying prescriptive conditions); a yes means reject or reword from a source, never mint |
| nearest held term | machine | `_name_holder` on name and aliases; D22 → 8 exact matches |
| kind | judgment, from `quantity / element / intervention / method / setting / lens` | |
| quantity implied | judgment | **a lead only.** The implied quantity's name is not in the item name, so minting it would be coining; it goes to the open-pass lead list |
| recommendation and reason | judgment | mint as term and promote (quantity); mint as term and decline (element, intervention: `decline-parameter --reason`); hold as lead; reject (held, prescription-bearing, or not ours) |

The owner approves the table in a dated ledger entry; then `mint-term-from-catalogue --catalogue _archived/data/corpus-pre-reset-2026-08-06.db
--entry-ref items:<rowid> --approval-ref "<heading>"` per approved row, followed by `add-parameter` or `decline-parameter`.
An element is a term, never a parameter (OR-14: element pages derive from parameters through a typed pointer). The catalogue
seeds English names only; it decides nothing about whether a concept exists, and every term it mints enters the alias coverage
metric with zero attested pairs.

### C.2 The open pass over held codes (route ii, OR-13 and OR-16)

Held texts are derived, not listed: for each instrument, `grep -l '"<ref_id>"' retrieval-log/*/manifest.jsonl` and
`select * from v_scan_ledger where ref_id = ?`. Most held non-English codes are single clauses retrieved for the ramp work (titles
naming one section, e.g. `select ref_id, original_title from evidence_sources where evidence_type='code'`). So route ii gives
full texts mainly for SG, UK, US and IE; it is the fastest first step and the most English one, which is why C.3 interleaves.
Each reading: `record-scan --mode catalogue --method full-read --text-scope full --open-pass-done`, with every new design quantity
`observe-term`'d verbatim.

### C.3 Native-language open passes over P1-3 instruments (route iii)

1. **Instrument list per pair**, derived from `research_code_leads`, `references/standards-registry.md` and the held codes,
   restricted to current editions (HANDOFF section 3). DK, IT and CN have nothing (D16): their first act is a search for the primary
   instrument, logged per R8.
2. **Order:** one full open pass per pair before any pair's second; within that, free official full texts before paywalled ones
   (availability per instrument is [UNVERIFIED] until fetched); English pairs are not first. A block goes to the Wayback route of
   CLAUDE.md section 7, with its recorded limit (the CSA B651 failure).
3. **Stopping rule, derived.** A pair is exhausted when every current instrument on its list has a full-read, full-scope, open-pass
   scan at the current `catalogue_version`, and the last such round produced no NAMES-NEW and no DEFERRED observation for that pair.
   A new parameter raises the catalogue version and `scan_debt` re-opens targeted readings, so the list closes only at a fixed point
   where a whole round adds nothing. No count is set by hand.

### C.4 Completeness checks from the other direction (route iv)

ICF chapters d4, d5, d6, d9 and e1 to e5 (from the WHO payload), `research_code_leads`, and the standards registries are read as
**checks**, not name sources: for each ICF activity or environmental code, ask whether any parameter's term addresses it; a miss is a
lead for the open pass, recorded as a gap. No ruling permits naming a parameter from ICF text.

### C.5 Coverage metric (OR-8), computed from the database

For each active parameter *p* and each approved bucket member (*L*, *J*):

- **read(p, L, J)**: some current instrument of *J* whose text language is *L* has a `v_scan_ledger` status of EXTRACTED,
  STATED-ABSENT or READ-NOTHING-FOUND for *p*. Needs A6 fixed (source language populated) and T-6b built.
- **named(p, L, J)**: an attested alias (pointer, T3) of *p*'s term in *L* from a source of *J*.

Report both per parameter and per pair, as counts with the command, never as a stored figure. It ships as one view in the T-6b PR,
which already plans `v_coverage_parameter_via_admission`; extend that rather than add a second view.

### C.6 Priority order

1. T1-T4 tooling PR. 2. Screened catalogue table, owner approval, mints and declinations. 3. Decline the non-quantity terms
already held (lens, method, economics and similar, D18) with reasons. 4. Route ii open passes. 5. Route iii, interleaved.
6. Alias attestation (B.3) rides on 4 and 5; nothing is attested separately from a reading. 7. ICF English titles, then labels.
8. Medical correspondence set. 9. Directions (`set-parameter-direction`) for each parameter as it is promoted.

## D. Sequencing and pull requests

Rule 10 splits tooling from rows; rule 9: each PR opened once, last, unsubscribed immediately, never watched. The gate for every PR
is CLAUDE.md section 1: `scripts/preflight.sh`, then `python3 scripts/run_checks.py --changed-from origin/main --explain`, plus
`--selftest` if anything is renamed. The checks below are the ones that read what each PR changes
(`python3 scripts/run_checks.py --list`); for each, the question is whether it could go red on that PR's defect.

| PR | Content | Depends on | Checks that read it | Adversarial pass |
|---|---|---|---|---|
| **PR-1 tooling** | T1 resolver for `items:<rowid>` plus the read-only screen subcommand; T2 name-bound-to-phrase refusal in `add-term` and native-label handling in `rename-term`; T3 migration adding `term_aliases.observation_id`, `add-alias` writing it, attaching a pointer to an already-held alias, refusing TRANSLATION and refusing an alias language not paired with the source's jurisdiction, `alias_provenance_audit` classifying from the pointer; T4 `set-icf-title` replacement of a non-payload title, with the code-anchoring fix; tests in `scripts/tests/test_db_amend_writers.py`. Deletions: the two alias-verification documents to `_archived/` (reader-facing content), the hard-coded language and jurisdiction lists and floors in `skills/multilingual-research_SKILL.md`, the `functional-taxonomy.md` sentence's false route corrected (doctrine text: show the owner) | E1, E3, E4 | `schema_reference_audit`, `migration_reproducibility` (counts only: run `migration_reproducibility_deep` too, because T3 attaches pointers by UPDATE), `alias_provenance_audit`, `column_vocabulary_audit`, `derived_not_curated_audit`, `test_db_integrity`, `test_db_amend_writers`, `validate_parameters`, `retired_vocabulary` | `antagonist` on the diff before opening: can a typed name still be minted; can a pointer be attached to an alias whose text differs from the phrase; does the audit still count notes text |
| **PR-2 research: the catalogue** | The approved screen table, its mints, promotions and declinations; declinations of held non-quantity terms; ledger entry recording the approval | PR-1 merged; owner approval of the table | `validate_parameters`, `alias_provenance_audit`, `research_dod_session`, `migration_reproducibility`, `research_tooling_separation` | `/adversarial` after the rows; `/batch-done` |
| **PR-3 tooling: labels and buckets** | T5 label table and its writer; T-6b steps 4-5 and the coverage view (C.5), if the pipeline-resolution workplan has not shipped them; a writer for source language if none exists | PR-1; E5, E6, E7, E8, E11 | as PR-1, plus `jurisdiction_db_vocabulary` | `antagonist` on the diff |
| **PR-4…n research: open passes** | One PR per batch of pairs: readings, observations, adjudications, new terms (NAMES-NEW), promotions, attested aliases | PR-1 (and PR-3 for the metric) | `scan_debt`, `observation_verbatim_audit`, `provenance_artefact_audit`, `research_dod_session`, `adversarial_pass_recorded` | `/adversarial` per batch; the antagonist samples aliases against their quotes |
| **PR-m research: ICF titles, labels, medical** | English ICF titles from payload; labels per language; the medical correspondence set | PR-1 (T4); PR-3 (T5); E5 | `medical_lens_integrity` (advisory), `adjudication_integrity`, `column_vocabulary_audit` | `antagonist`: re-derive each title and anchor from the payload bytes |

**What tooling is genuinely required, and what is not.** T1 is required by the 2026-11-06 ruling. T2 and T3 are required because
without them OR-17 and R11 are unenforceable and the alias gate measures text (the wrong thing reaching the book is an invented name
or a model alias presented as native). T4 is required because the 29 titles cannot otherwise be corrected. T5 is required only if
E5 and E6 are answered yes; otherwise it has no reader and is not built. **Rejected additions:** a separate glossary-verification
marker or table (the evidence path already attests; rule 8); a `label_language` column (derivable from the origin observation); a
language CHECK (would block later languages; the vocabulary is `lang_jur_map`); a database table for the screen (the judgment lives
in the approved ledger table and the mint's three columns); a new coverage check before T-6b exists (it would examine nothing).
**Net-negative:** PR-1 and PR-3 measure `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`;
the skill deletions offset part of T1-T4, and the PR description names any remaining exception and what it replaces.

## E. Owner decisions

**Blocking PR-1**

1. **E1 [DG-NON: audience].** *A concept appears first in a Dutch, Japanese or other non-English code, and no English source names it.
   The database requires an English name, and you ruled the model may not invent one (OR-17). What is the term called?*
   **(A, recommended)** The code's own phrase, in its language, until an English-language code is found naming the same thing; the
   English reader sees the native phrase with its language. Consequence: honest, no invented names; English readers meet non-English
   labels. **(B)** Rebuild the table so the English name can be empty. Consequence: same result, much more code. **(C)** Let the model
   write an English gloss. Consequence: breaks OR-17; not recommended.
2. **E3.** *The 93 item subjects are pointed at by row number in the archived database, so no old code appears in a live row, and no
   schema change is needed (the archived database is already a permitted catalogue). Accept?* **(A, recommended)** Yes. **(B)** Point by
   old code, shown only in the review table. Consequence: the code reappears in live rows, against the item-layer deletion.
3. **E4 (OR-17b).** *1163 model-generated and 880 unrecorded aliases exist (`python3 scripts/audit/alias_provenance_audit.py`).
   What are they?* **(A, recommended)** Flagged search aids only; each becomes vocabulary only when a code in its language is found
   using it. Consequence: search recall kept, nothing claimed. **(B)** Delete them. Consequence: 13 languages lose all search terms
   until readings attest them. **(C)** Keep them as vocabulary. Consequence: contradicts OR-17.

**Can wait**

4. **E2.** *Four terms carry names no source used (two from Dutch phrases). Rename each to its source's phrase?* **(A, recommended)**
   Yes, in a data PR, with your quote for parameter 12. **(B)** Leave and flag.
5. **E5 [DG-NON: licensing].** *May WHO's published ICF and ICD-11 titles in other languages be stored verbatim in a CC BY-SA book?*
   **(A)** Yes, each with its payload. **(B, recommended until the licence is read from WHO's own terms)** Store the pointer to the
   persisted payload only. **(C)** English only. Consequence of C: the ICF lens is English-only.
6. **E6 [DG-NON: population taxonomy].** *Identity names in other languages: may the base record each language community's own
   designation, attested in its own Co-1 sources, beside the English name, with no change to codes?* **(A, recommended)** Yes; gaps
   stay visible. **(B)** Only after a named native community reviewer per language. **(C)** Translate the English names. Consequence of C:
   breaks R11.
7. **E7 [DG-NON: jurisdiction].** *Norwegian Bokmål and Nynorsk, Chinese script, and official languages of in-scope countries missing
   from the map (for example Singapore's Malay and Tamil, Irish, Romansh): split, add, or leave?* **(A, recommended)** Split Norwegian
   only where an instrument is published in both; leave the rest out of scope for now. **(B)** Add them all.
8. **E8.** *Rooms have no reader. Freeze, wire to element pages (OR-14), or retire?* **(A, recommended)** Freeze until a page reads them.
9. **E9.** *Typical stakes for 16 needs: the model proposes each with its warrant in one table; you approve?* **(A, recommended)** Yes.
10. **E10.** *Native-speaker review (VERIFIED-NATIVE) needs named people. Name reviewers per language, or accept that this edition
    relies on attestation from codes only?* **(A, recommended)** Attestation only for now.
11. **E11 (OR-8, T-6b).** *Approve the 39 P1-3 language-jurisdiction pairs (D15) as bucket members?* **(A, recommended)** Yes.
12. **E12.** *The 17 functional-axis terms and 14 method terms are not quantities. Decline them as parameters, with reasons, keeping the
    terms?* **(A, recommended)** Yes; no taxonomy changes.

## F. Model routing and effort

| Step | Routing | Why |
|---|---|---|
| Counts, UNWRITABLE set, scan debt, coverage reports | `db-census` agent; `haiku/50/format` | mechanical |
| Caller sweeps for T2, T3 and the deleted documents | `repo-sweep` agent; `sonnet/75/extract` | mechanical, rule 4 |
| T1-T5 code | `sonnet/100/route` with an `opus/125/arbitrate` antagonist pass | refusals are the value; the attack matters more than the write |
| Screen table judgment columns (kind, prescription, implied quantity) | `opus/150/arbitrate` | an element minted as a parameter is the item-layer defect again |
| Open-pass reading, observation, adjudication | `opus/125/extract`, adjudication `opus/150/arbitrate` | NAMES-NEW versus NAMES-EXISTING across languages is judgment |
| Medical correspondence pruning | `opus/150/arbitrate` | the 2026-09-11 ruling requires pruning the derived join |
| Directions | `opus/150/synth` | rationale for disabled people per parameter |
| Native-speaker certification | `human/none/none` | **No model can certify that a phrase is in use.** A model-read phrase found verbatim in a jurisdiction's own instrument is *attested* (the bytes certify presence, not the model); a phrase the model supplies is *model-generated* and stays flagged. Only attestation or a named human reviewer promotes it |

## G. Self-attack

1. **The screen passes a prescription.** `_VALUE_BEARING` sees digits and min/max words, not condition clauses. *Guard:* the
   judgment column "prescription-bearing" and the owner's table. *Detection:* the antagonist re-reads every minted name;
   `validate_parameters` cannot see it.
2. **An attested alias that is really a translation.** A government's English version of a Japanese code, or a bilingual glossary,
   puts a translated phrase in a saved file, and `add-alias` accepts it. *Guard:* T3's refusal where the alias language is not paired
   with the source's jurisdiction. *Detection:* `select` aliases whose language is not in `lang_jur_map` for the source's jurisdiction
   (should be empty).
3. **The coverage metric examines nothing.** Before T-6b exists the pair set is empty and any check over it passes. *Guard:* no coverage
   check registers until the bucket table holds approved rows; the view prints EXAMINED. *Detection:* `run_checks.py` NOTHING-IN-SCOPE.
4. **Prose contradicts the database.** This plan, the 2026-11-06 ledger item 3, the documents PR-1 archives, and the skill. *Guard:*
   commands beside figures; the ledger correction; `repo-sweep` over `governance/`, `references/`, `architecture/`, `skills/` with
   `git grep` after PR-1. *Detection:* none mechanical (rule 7a's ungated third shape).
5. **A classification title from memory.** Already happened (A4). *Guard:* payload only, anchored to its code (T4 fix). *Detection:*
   the antagonist re-derives each title from bytes; `base_icf`'s CHECK only proves a source string exists.

**Also likely:** the catalogue's English names set the frame before native passes run. *Guard:* C.3's interleave and the per-language
metric, which shows the imbalance.

**Could not verify:** which ICF and ICD-11 languages WHO or national bodies publish, and their licences [UNVERIFIED]; which P1-3
instruments are free in full text [UNVERIFIED]; whether a verb writes `evidence_sources.language` or `access_needs.typical_stakes`
[GAP]; whether T-6b is under way on another branch [GAP: `git log origin/main --oneline -- scripts/migrations | head`].

**Later languages (AR, BN, HI, SW).** The design admits them without a schema change, provided no language CHECK is added: languages
come from `lang_jur_map` (they are already rows, `select * from lang_jur_map where language in ('AR','BN','HI','SW')`), aliases and
labels carry free language codes, and B.1 lets a term originate in any script. What they need is research, not structure: instruments
in those languages, read under the same rules. OR-12a still scopes them out.

## Appendix: the derivation script (read-only; run from the repository root)

```python
import sqlite3, re
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
old = sqlite3.connect('file:_archived/data/corpus-pre-reset-2026-08-06.db?mode=ro&immutable=1', uri=True)
q = lambda s, *a: con.execute(s, a).fetchall()
P = "US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN".split(); ph = ",".join("?"*len(P))
print("D1", q("select count(*) from base_parameters where status='active'"))
print("D2", q("select count(*) from terms"), q("select count(*) from parameter_declinations where revoked_at is null"))
print("D3", q("select count(*) from base_parameters where accessibility_direction is not null"))
print("D4", q("select count(*) from term_aliases where jurisdiction is null"))
print("D5", 'observation_id' not in [c[1] for c in con.execute("pragma table_info(term_aliases)")])
print("D6", q("select count(*) from term_aliases where notes like '%source-attested%'"))
print("D7", q("select count(*) from term_adjudications where outcome='NAMES-EXISTING'"))
print("D8", q("select t.term_id,o.language,o.surface_form,t.canonical_en from term_adjudications a join observed_terms o "
              "using(observation_id) join terms t on t.term_id=a.term_id where a.outcome='NAMES-NEW' and upper(o.language)<>'EN'"))
print("D9", q("select count(*) from term_adjudications a join observed_terms o using(observation_id) join terms t "
              "on t.term_id=a.term_id where a.outcome='NAMES-NEW' and instr(lower(o.surface_form),lower(t.canonical_en))=0"))
print("D10", q("select count(*) from term_aliases where alias_type='TRANSLATION'"))
print("D11", q("select coalesce(title_source,'(untitled)'),count(*) from base_icf group by 1"))
print("D12", q("select component||substr(icf_code,2,1),count(*) from base_icf group by 1"))
print("D13", q("select sum(language is null),count(*) from evidence_sources"), q("select lang_detected,count(*) from evidence_sources group by 1"))
print("D14", q("select count(*),sum(open_pass_done),sum(method='full-read') from source_scans"))
print("D15", q(f"select count(*),count(distinct language) from lang_jur_map where jurisdiction in ({ph})", *P))
held = {r[0] for r in con.execute("select distinct jurisdiction from research_code_leads")} | {r[0] for r in con.execute(
    "select distinct jurisdiction from evidence_sources where evidence_type in ('code','standard_eb','national_fw')")}
print("D16", [j for j in P if j not in held])
print("D18", q("select coalesce(domain,'(none)'),count(*) from terms group by 1 order by 2 desc"))
print("D19", [t for (t,) in con.execute("select name from sqlite_master where type='table'")
              for f in con.execute(f'PRAGMA foreign_key_list("{t}")') if f[2] == 'rooms'], q("select sum(category is null),count(*) from rooms"))
print("D20", q("select sum(typical_stakes is null),count(*) from access_needs"))
print("D21", q("select (select count(*) from base_taxonomy_medical),(select count(*) from icf_medical_map),(select count(*) from identity_medical_map)"))
heldn = {r[0].lower() for r in con.execute("select canonical_en from terms")} | {r[0].lower() for r in con.execute(
    "select alias from term_aliases where lower(language)='en'")}
VB = re.compile(r"[0-9≥≤<>=]|\b(min|max|minimum|maximum)\b", re.I)
s = [re.sub(r"\s*[\(\[].*?[\)\]]", "", n).strip() for (n,) in old.execute("select name from items order by rowid")]
print("D22", len(s), sum(x.lower() in heldn for x in s), sum(bool(VB.search(x)) for x in s))
print("D23", q("select jurisdiction,count(*) from term_aliases where jurisdiction in ('TW','colloquial') group by 1"))
```

Results on 2026-11-06, for orientation only (re-run): D1 10 · D2 94, 1 · D3 2 · D4 2133 · D5 True · D6 0 · D7 45 · D8 TERM-090,
TERM-092 · D9 4 · D10 996 · D11 untitled 43, repo prose 12, deleted skill 17 · D12 no d8, e4, e5 · D13 58 of 58 NULL · D14 9, 0, 0 ·
D15 39 pairs, 14 languages · D16 DK, IT, CN · D19 no reader, 17 of 17 uncategorised · D20 16 of 17 · D21 0, 0, 0 · D22 93, 8, 2 ·
D23 TW 1, colloquial 1. D17 (held instruments by jurisdiction) is omitted from the script; derive it with
`select jurisdiction,count(*) from evidence_sources where evidence_type in ('code','standard_eb','national_fw') group by 1`.
